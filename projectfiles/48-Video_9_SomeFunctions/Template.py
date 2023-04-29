from __future__ import annotations

from manimlib import *
import numpy as np

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

#################################################################### 

class SquareCross(Polygon):
    def __init__(self, side_length: float = 2, **kwargs):
        self.side_length = side_length
        super().__init__(*self.create_points(), **kwargs)
    pass

    def create_points(self) -> None:
        points = np.zeros((12, 3))
        points[0::3] = np.array([DR, UR, UL, DL])*self.side_length/2
        points[1::3] = np.array([DR+2*RIGHT, UR+2*UP, UL+2*LEFT, DL+2*DOWN])*self.side_length/2
        points[2::3] = np.array([UR+2*RIGHT, UL+2*UP, DL+2*LEFT, DR+2*DOWN])*self.side_length/2
        return points

class CubeCross(SGroup):
    CONFIG = {
        "reflectiveness": 0,
        "gloss": 0.3,
        "shadow": 0.6,
    }

    def __init__(self, side_length: float = 2, **kwargs):
        self.side_length = side_length
        super().__init__(*self.square_to_cube_faces(), **kwargs)

    def square_to_cube_faces(self) -> list[Square3D]:
        radius = self.side_length
        face = Square3D(side_length=radius).shift(radius/2*OUT)
        cube = SGroup(face, *[face.copy().rotate(PI / 2, axis=direction, about_point=ORIGIN) for direction in [RIGHT, UP, LEFT, DOWN]]).shift(radius*OUT)
        result = [cube]
        result.extend([
            cube.copy().rotate(PI / 2, axis=vect, about_point=ORIGIN)
            for vect in compass_directions(4)
        ])
        result.append(cube.copy().rotate(PI, RIGHT, about_point=ORIGIN))
        return result
    
class Test_1(FrameScene):

    def construct(self):

        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/8), quad(RIGHT, 0.4*PI))
        camera.set_orientation(Rotation(quadternion)).shift(0.5*IN)# .set_focal_distance(12.0)
        side_length = 0.5
        vector_1 = np.array([2, -1, 0])*side_length
        vector_2 = np.array([1, 3, 0])*side_length
        cross_0 = CubeCross(side_length = side_length)
        crosses = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                offset = i*vector_1 + j*vector_2
                color = BLUE if (i+j)%2 else GREEN
                cross_ij = cross_0.copy().shift(offset).set_color(color)
                cross_ij[0].shift(side_length*IN)
                cross_ij[5].shift(side_length*OUT)
                crosses.append(cross_ij)
        self.add(*crosses)

class SharpImage(VGroup):
    CONFIG = {
        "height": 2,
        "draw_stroke_behind_fill": True,
    }

    def __init__(self, filename, **kwargs):

        self.filename = filename
        super().__init__(*self.get_pixels(), **kwargs)
        self.arrange_in_grid(self.size[0], self.size[1], buff = 0, aligned_edge = UP, fill_rows_first = False).set_height(self.height)

    def get_pixels(self):
        image = Image.open(self.filename)
        self.size = image.size
        pixels = []
        for i in range (self.size[0]):
            for j in range (self.size[1]):
                colorij = image.getpixel((i, j))
                opacity = colorij[3]/255 if len(colorij)>3 else 1
                pixelij = Square(stroke_width = 0, fill_opacity = opacity, color = rgb_to_color(np.array([colorij[0], colorij[1], colorij[2]])/255))
                pixels.append(pixelij)
        return pixels

class Test_2(FrameScene):
    CONFIG = {
        "for_pr": False,
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):

        self.camera.anti_alias_width = 0
        camera = self.camera.frame

        cane = SharpImage("sugar_cane.png", height = 3.6)
        canes = [cane[0:64], cane[64:128], cane[128:192], cane[192:256]]
        water = SharpImage("water.png", height = 1.8)
        self.play(*[FadeIn(canes[i], 0.5*DOWN, rate_func = squish_rate_func(rush_from, 0.1*i, 0.7+0.1*i)) for i in range(4)])
        self.bring_to_back(water).play(FadeIn(water, scale = 0.5), cane.animate.scale(0.5).shift(2*LEFT), camera.animate.shift(LEFT))
        canes = [cane.copy().shift(2*RIGHT), cane.copy().shift(2*RIGHT), cane.copy().shift(2*RIGHT)]
        directions = [UP, RIGHT, DOWN]
        self.bring_to_back(*canes).play(*[canes[i].animate.scale(0.5).shift(directions[i]) for i in range(3)], cane.animate.scale(0.5).shift(RIGHT), water.animate.scale(0.5), camera.animate.shift(RIGHT))
        element = VGroup(cane, *canes, water)
        cross_0 = SquareCross(side_length = 1, stroke_width = 4, fill_opacity = 0, stroke_color = BLUE, fill_color = BLUE)
        self.add(element).play(ShowCreation(cross_0))
        self.play(cross_0.animate.set_style(stroke_width = 0, fill_opacity = 1).scale(0.5), element.animate.scale(0.5))
        self.remove(element)

        side_length = 0.5
        vector_1 = np.array([2, -1, 0])*side_length
        vector_2 = np.array([1, 2, 0])*side_length
        crosses = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i != 0 or j != 0:
                    offset = i*vector_1 + j*vector_2
                    color = GREEN if (i+j)%2 else BLUE
                    cross_ij = cross_0.copy().shift(offset).set_color(color)
                    cross_ij.position = (i, j)
                    crosses.append(cross_ij)
        def sorting(mob: VMobject):
            i, j = mob.position
            radius = max(abs(i), abs(j))
            angle = np.arctan2(j, i)/TAU
            angle = (angle + 0.375)%1 -0.5
            return radius - angle
        crosses.sort(key = sorting)
        def fade_shift(mob: VMobject):
            i, j = mob.position
            if i <= j and i > -j:
                return LEFT
            elif i+1 < j and i <= -j:
                return DOWN
            elif i+1 >= j and i < -j:
                return RIGHT
            else:
                return UP

        self.play(LaggedStart(*[FadeIn(mob, 0.25*fade_shift(mob)) for mob in crosses], lag_ratio = 0.1), run_time = 2)
        self.remove(*crosses, cross_0)

        camera = self.camera.frame
        quadternion = quaternion_mult(quad(OUT, PI/3), quad(RIGHT, PI/2-PI/20))
        vector_1 = np.array([2, -1, 0])*side_length
        vector_2 = np.array([1, 2, 0])*side_length
        cross_0 = CubeCross(side_length = side_length, gloss = 0, shadow = 0)
        crosses = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                offset = i*vector_1 + j*vector_2
                color = GREEN if (i+j)%2 else BLUE
                cross_ij = cross_0.copy().shift(offset + 0.5*side_length*IN).set_color(color)
                cross_ij.position = (i, j)
                cross_ij[0].shift(side_length*IN)
                cross_ij[5].shift(side_length*OUT)
                crosses.append(cross_ij)
        self.add(*crosses).play(*[mob.animate.shift(mob.position[1]*RIGHT).set_gloss(0.3).set_shadow(0.6) for mob in crosses],
                                camera.animate.set_height(12).set_focal_distance(30))
        
        self.play(camera.animate.set_orientation(Rotation(quadternion)),
                  *[mob[0].animate.shift(side_length*OUT) for mob in crosses], 
                  *[mob[5].animate.shift(side_length*IN) for mob in crosses])
        
        
        cross_up = []
        cross_down = []
        for cross in crosses:
            parity = (cross.position[0] + cross.position[1]) % 2
            cross_up.append(cross.copy().shift(np.array([-1, -1, 5])*side_length).set_color(PURPLE_A if parity else RED))
            cross_down.append(cross.copy().shift(np.array([1, 1, -4])*side_length).set_color(ORANGE if parity else YELLOW))
        cross_down = SGroup(*cross_down)
        shade = Shade(is_fixed_in_frame = True, fill_color = BLACK)
        self.bring_to_back(cross_down, shade).play(cross_down.animate.shift(2*OUT*side_length), FadeOut(shade))
        self.play(cross_down.animate.shift(OUT*side_length))
        self.bring_to_back(*cross_up, shade).play(*[mob.animate.shift(IN*side_length) for mob in cross_up], FadeOut(shade))
        self.play(*[cross_up[i].animating(rate_func = squish_rate_func(smooth, i/27, (i+3)/27)).shift(3*IN*side_length) for i in range(25)], run_time = 5)
        self.wait(1)
        self.play(FadeIn(shade))
        self.wait(1)

#################################################################### 

class Trailer(Scene):
    def construct(self):

        size_pixel = 1/7
        pixels = 6
        size = pixels*size_pixel

        icons = [ImageMobject("cane_left.png", height = size), 
                 ImageMobject("water_enlarged.png", height = size), 
                 ImageMobject("cane_right.png", height = size)]
        list_icons = []
        rows, cols = 7, 7
        for i in range(rows):
            for j in range(cols):
                offset = size*(i-(rows-1)/2)*DOWN + size*(j-(cols-1)/2)*RIGHT + 2.5*RIGHT
                if (i + j*2) % 5 == 4:
                    mob = icons[1].copy().shift(offset)
                else:
                    mob = icons[0].copy().shift(offset)
                list_icons.append(mob)
        
        angle = PI/20
        text = Text(r"但复数可以用来种甘蔗", font = "LXGW WenKai", color = YELLOW).scale(1.1)
        text[1].scale(1.7).rotate(angle).set_color(BLUE)
        text[2].scale(1.7).rotate(-angle).set_color(BLUE)
        text[7].scale(1.7).rotate(-2*angle).set_color(GREEN)
        text[8].scale(1.7).rotate(-angle).set_color(GREEN)
        text[9].scale(1.7).set_color(GREEN)
        text.arrange(buff = 0.1).shift(2.5*UP + 0.5*RIGHT)
        text[7].shift(0.2*UP)
        text[8].shift(0.05*UP)
        text_1, text_2, text_3 = [text[0:3], text[3:7], text[7:]]
        text_2.shift(text.get_height()*0.9*DOWN + 4*LEFT).rotate(-angle)
        text_3.shift(text.get_height()*1.8*DOWN + 8*LEFT)
        self.add(*list_icons, text)

        offset = LEFT+0.5*DOWN
        point_1 = 1.5*unit(PI+PI/15) + offset
        point_2 = 1.5*unit(PI*3/2-PI/15) + offset
        point_3 = 1.5*DOWN + 4*LEFT + offset
        seg_1 = (2*point_1+point_2)/3
        seg_2 = (point_1+2*point_2)/3
        arrow = ArcBetweenPoints(point_3, seg_1, angle = PI/2, fill_color = YELLOW, fill_opacity = 1, stroke_width = 0).add_points_as_corners([point_1, offset, point_2, seg_2]
                                                            ).append_points(ArcBetweenPoints(seg_2, point_3, angle = -PI/2).get_all_points()).rotate(-PI/6).scale(0.9)
        triangle = Polygon(offset, point_1, point_2)

        self.add(arrow)


#################################################################### 

class Template(FrameScene):
    def construct(self):
        pass