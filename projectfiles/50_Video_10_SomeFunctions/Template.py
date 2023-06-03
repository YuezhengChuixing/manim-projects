from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Toy_1(FrameScene):
    CONFIG = {
        "for_pr": False,
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        clock_12 = 3/2*np.sqrt(3)*UP
        clock_2 = 1.5*RIGHT
        clock_4 = 3*RIGHT + 3/2*np.sqrt(3)*DOWN
        clock_6 = 3/2*np.sqrt(3)*DOWN
        clock_8 = 3*LEFT + 3/2*np.sqrt(3)*DOWN
        clock_10 = 1.5*LEFT
        triangle = Polygon(clock_8, clock_4, clock_12, fill_color = BACK, fill_opacity = 1, stroke_width = 8)
        eye = ArcBetweenPoints(clock_12, clock_6, PI/3, color = GREEN, fill_opacity = 0.2, stroke_width = 8).append_points(ArcBetweenPoints(clock_6, clock_12, PI/3).get_all_points()).save_state()

        alpha = ValueTracker(0.0)
        def eye_updater(mob: VMobject):
            value = (alpha.get_value())%PI
            if value <= PI/3:
                mob.restore().rotate(value, about_point = 3*clock_10).shift(value/(PI/3)*(clock_4 - clock_12))
            elif value <= 2*PI/3:
                mob.restore().rotate(value - PI/3, about_point = 3*clock_10).shift((value/(PI/3)-1)*(clock_4 - clock_12)).rotate(-2*PI/3, about_point = np.sqrt(3)/2*DOWN)
            else:
                mob.restore().rotate(value - 2*PI/3, about_point = 3*clock_10).shift((value/(PI/3)-2)*(clock_4 - clock_12)).rotate(-4*PI/3, about_point = np.sqrt(3)/2*DOWN)
        eye.add_updater(eye_updater)
        self.add(triangle, eye)
        self.play(alpha.animate.set_value(PI), run_time = 3, rate_func = linear)
        
class Reuleaux(VMobject):
    CONFIG = {
        "radius": np.sqrt(3),
        "start_angle": PI/2
    }
    def init_points(self) -> None:
        vertices = self.radius*unit(self.start_angle), self.radius*unit(self.start_angle+TAU/3), self.radius*unit(self.start_angle+2*TAU/3)
        points = [*ArcBetweenPoints(vertices[0], vertices[1], PI/3).get_all_points(), *ArcBetweenPoints(vertices[1], vertices[2], PI/3).get_all_points(), *ArcBetweenPoints(vertices[2], vertices[0], PI/3).get_all_points()]
        self.set_points(points)

class Trailer(Scene):
    def construct(self):
        vertices_0 = [UP, DOWN+2/np.sqrt(3)*LEFT, DOWN+2/np.sqrt(3)*RIGHT]
        midpoints_0 = [(vertices_0[1]+vertices_0[2])/2, (vertices_0[2]+vertices_0[0])/2, (vertices_0[0]+vertices_0[1])/2]
        vertices_1 = [2*vertices_0[0]-midpoints_0[1], 2*vertices_0[0]-midpoints_0[2]]
        midpoints_1 = [(vertices_1[0]+midpoints_0[2])/2, vertices_0[0], (vertices_1[1]+midpoints_0[1])/2]
        vertices_2 = [2*vertices_1[0]-midpoints_1[1], 2*vertices_1[0]-midpoints_1[0], 2*vertices_1[1]-midpoints_1[2], 2*vertices_1[1]-midpoints_1[1]]
        triangle_0 = Polygon(*vertices_0).set_stroke(width = 0).set_fill(color = RED, opacity = 1)
        triangles_1_0 = VGroup(Polygon(vertices_0[0], midpoints_0[1], vertices_1[1]), Polygon(vertices_0[0], midpoints_0[2], vertices_1[0]))
        triangles_1 = VGroup(triangles_1_0, triangles_1_0.copy().rotate(TAU/3, about_point = 1/3*DOWN), triangles_1_0.copy().rotate(-TAU/3, about_point = 1/3*DOWN)).set_stroke(width = 0).set_fill(color = ORANGE, opacity = 1)
        triangles_2_0 = VGroup(Polygon(vertices_2[0], vertices_1[0], midpoints_1[0]), Polygon(vertices_2[1], vertices_1[0], midpoints_1[1]), Polygon(vertices_2[2], vertices_1[1], midpoints_1[1]), Polygon(vertices_2[3], vertices_1[1], midpoints_1[2]))
        triangles_2 = VGroup(triangles_2_0, triangles_2_0.copy().rotate(TAU/3, about_point = 1/3*DOWN), triangles_2_0.copy().rotate(-TAU/3, about_point = 1/3*DOWN)).set_stroke(width = 0).set_fill(color = YELLOW, opacity = 1)
        triangles = VGroup(triangles_2, triangles_1, triangle_0).shift(3.5*LEFT)
        self.add(triangles.scale(0.9).shift(0.75*DOWN))

        radius = 4
        subsector_1 = Arc(-PI/6, PI/9, radius = radius).add_line_to(ORIGIN).close_path()
        subsector_2 = Arc(-PI/18, PI/9, radius = radius).add_line_to(ORIGIN).close_path()
        subsector_3 = Arc(PI/18, PI/9, radius = radius).add_line_to(ORIGIN).close_path()
        subsector_2.rotate(PI, about_point = (radius/2*np.cos(PI/18))*RIGHT)
        subsector_1.shift(radius*np.sin(PI/18)*UP), subsector_3.shift(radius*np.sin(PI/18)*DOWN)
        center = radius*2/3*(1+np.sin(PI/18))*np.cos(PI/6)*RIGHT
        offset = 3.5*RIGHT+1/3*DOWN-center
        center = 3.5*RIGHT+1/3*DOWN
        subsectors_1 = VGroup(subsector_1, subsector_3, subsector_2).shift(offset).rotate(-PI/2, about_point = center)
        subsectors_2 = subsectors_1.copy().rotate(TAU/3, about_point = center)
        subsectors_3 = subsectors_1.copy().rotate(2*TAU/3, about_point = center)
        subsectors = VGroup(subsectors_1, subsectors_2, subsectors_3).set_stroke(width = 0).set_fill(color = YELLOW, opacity = 1)
        reuleaux = Reuleaux(radius = 2*radius/3*(1-2*np.sin(PI/18))*np.cos(PI/6)).shift(center).set_stroke(width = 0).set_fill(color = ORANGE, opacity = 1)
        semicircle = ArcBetweenPoints(reuleaux.get_points()[48], reuleaux.get_points()[24], angle = PI, color = RED, stroke_width = 0, fill_opacity = 1)
        sectors = VGroup(subsectors, reuleaux, semicircle)
        self.add(sectors.scale(0.9).shift(0.75*DOWN))
        text_1 = Text("一百年前", font = "FZDaHei-B02S", stroke_width = 4, stroke_color = BACK, fill_color = WHITE).set_style(stroke_background = True).scale(2).shift(3.5*LEFT+3*UP)
        text_2 = Text("一百年后", font = "FZDaHei-B02S", stroke_width = 4, stroke_color = BACK, fill_color = WHITE).set_style(stroke_background = True).scale(2).shift(3.5*RIGHT+3*UP)
        line = Line(4*UP, 4*DOWN)
        arrow = Polygon(1.5*LEFT+0.6*UP, 0.4*RIGHT+0.6*UP, 0.4*RIGHT+1.2*UP, 2*RIGHT, 0.4*RIGHT+1.2*DOWN, 0.4*RIGHT+0.6*DOWN, 1.5*LEFT+0.6*DOWN, color = RED, fill_opacity = 1, stroke_width = 0).close_path()
        self.add(text_1, text_2, line, arrow.scale(0.7))


class Cover(Scene):
    def construct(self):
        self.camera.anti_alias_width = 0
        LIMEGREEN = interpolate_color(LIME, GREEN, 0.75)

        vertices_0 = [UP, DOWN+2/np.sqrt(3)*LEFT, DOWN+2/np.sqrt(3)*RIGHT]
        midpoints_0 = [(vertices_0[1]+vertices_0[2])/2, (vertices_0[2]+vertices_0[0])/2, (vertices_0[0]+vertices_0[1])/2]
        vertices_1 = [2*vertices_0[0]-midpoints_0[1], 2*vertices_0[0]-midpoints_0[2]]
        midpoints_1 = [(vertices_1[0]+midpoints_0[2])/2, vertices_0[0], (vertices_1[1]+midpoints_0[1])/2]
        vertices_2 = [2*vertices_1[0]-midpoints_1[1], 2*vertices_1[0]-midpoints_1[0], 2*vertices_1[1]-midpoints_1[2], 2*vertices_1[1]-midpoints_1[1]]
        midpoints_2 = [(vertices_2[0]+midpoints_1[0])/2, vertices_1[0], vertices_1[0], (vertices_2[1]+midpoints_1[1])/2, (vertices_2[2]+midpoints_1[1])/2, vertices_1[1], vertices_1[1], (vertices_2[3]+midpoints_1[2])/2]
        vertices_3 = [2*vertices_2[0]-midpoints_2[1], 2*vertices_2[0]-midpoints_2[0], 2*vertices_2[1]-midpoints_2[3], 2*vertices_2[1]-midpoints_2[2], 2*vertices_2[2]-midpoints_2[5], 2*vertices_2[2]-midpoints_2[4], 2*vertices_2[3]-midpoints_2[7], 2*vertices_2[3]-midpoints_2[6]]
        triangle_0 = Polygon(*vertices_0).set_stroke(width = 0).set_fill(color = RED, opacity = 1)
        triangles_1_0 = VGroup(Polygon(vertices_0[0], midpoints_0[1], vertices_1[1]), Polygon(vertices_0[0], midpoints_0[2], vertices_1[0]))
        triangles_1 = VGroup(triangles_1_0, triangles_1_0.copy().rotate(TAU/3, about_point = 1/3*DOWN), triangles_1_0.copy().rotate(-TAU/3, about_point = 1/3*DOWN)).set_stroke(width = 0).set_fill(color = ORANGE, opacity = 1)
        triangles_2_0 = VGroup(Polygon(vertices_2[0], vertices_1[0], midpoints_1[0]), Polygon(vertices_2[1], vertices_1[0], midpoints_1[1]), Polygon(vertices_2[2], vertices_1[1], midpoints_1[1]), Polygon(vertices_2[3], vertices_1[1], midpoints_1[2]))
        triangles_2 = VGroup(triangles_2_0, triangles_2_0.copy().rotate(TAU/3, about_point = 1/3*DOWN), triangles_2_0.copy().rotate(-TAU/3, about_point = 1/3*DOWN)).set_stroke(width = 0).set_fill(color = YELLOW, opacity = 1)
        triangles_3_0 = VGroup(*[Polygon(vertices_3[i], vertices_2[int(i/2)], midpoints_2[i]) for i in range(8)])
        triangles_3 = VGroup(triangles_3_0, triangles_3_0.copy().rotate(TAU/3, about_point = 1/3*DOWN), triangles_3_0.copy().rotate(-TAU/3, about_point = 1/3*DOWN)).set_stroke(width = 0).set_fill(color = LIMEGREEN, opacity = 1)
        triangles = VGroup(triangles_3, triangles_2, triangles_1, triangle_0).scale(0.8, about_point = ORIGIN).shift(3.2*LEFT)
        self.add(triangles.scale(0.8).shift(0.75*DOWN))

        ratio_2 = 1 - 2*np.sin(PI/18)
        radius_2 = np.sqrt(3) * ratio_2
        ratio_3 = 1 - np.sin(PI/72)/np.sin(PI/18)
        radius_3 = radius_2 * ratio_3
        iter_0 = ArcBetweenPoints(np.sqrt(3)*unit(-PI/6), np.sqrt(3)*unit(7*PI/6), angle = PI, n_components = 24, stroke_width = 0, fill_opacity = 1, color = RED).scale(ratio_2*ratio_3, about_point = ORIGIN)
        iter_1 = Reuleaux(color = ORANGE, stroke_width = 0, fill_opacity = 1).scale(ratio_2*ratio_3, about_point = ORIGIN)
        sectors_2 = [Arc(radius = 3, start_angle = -TAU/3 + i*PI/9, angle = PI/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path() for i in range(3)]
        sectors_2[0].shift(3*RIGHT*np.sin(PI/18)), sectors_2[1].rotate(PI, about_point = 3/2*np.cos(PI/18)*DOWN), sectors_2[2].shift(3*LEFT*np.sin(PI/18))
        group_2 = VGroup(*sectors_2).shift((3*np.sqrt(3)*np.sin(PI/18) + radius_2)*UP)
        iter_2 = VGroup(group_2, group_2.copy().rotate(TAU/3, about_point = ORIGIN), group_2.copy().rotate(-TAU/3, about_point = ORIGIN)).scale(ratio_3, about_point = ORIGIN)
        verticies_1 = [3*ratio_2/np.sqrt(3)*unit(PI/2), 3*ratio_2/np.sqrt(3)*unit(7*PI/6), 3*ratio_2/np.sqrt(3)*unit(-PI/6)]
        r = 3*np.cos(PI/18) - np.sqrt(3)*(1+np.sin(PI/18))
        verticies_2 = [verticies_1[2]+3*LEFT, r*unit(PI/6), verticies_1[0]+3*unit(-TAU/3), verticies_1[1]+3*unit(PI/3), r*unit(-PI/2), verticies_1[2]+3*unit(TAU/3), verticies_1[0]+3*unit(-PI/3), r*unit(5*PI/6), verticies_1[1]+3*RIGHT]
        sectors_3 = [Arc(radius = 3, start_angle = 4*PI/9, angle = PI/24, n_components = 24, color = LIMEGREEN, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path(), 
                   Arc(radius = 3, start_angle = 4*PI/9 + PI/24, angle = PI/36, n_components = 24, color = LIMEGREEN, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path(), 
                   Arc(radius = 3, start_angle = 5*PI/9 - PI/24, angle = PI/24, n_components = 24, color = LIMEGREEN, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path()]
        sectors_3[0].shift(3*np.sin(PI/72)*LEFT), sectors_3[1].rotate(PI, about_point = 3/2*np.cos(PI/72)*UP), sectors_3[2].shift(3*np.sin(PI/72)*RIGHT)
        group_3 = VGroup(*sectors_3).shift(3*np.sin(PI/72)/np.tan(PI/18)*DOWN)
        angles = [-4*PI/9, 2*PI/3, -2*PI/9, 8*PI/9, 0, -8*PI/9, 2*PI/9, -2*PI/3, 4*PI/9]
        iter_3 = VGroup(*[group_3.copy().rotate(angles[i], about_point = ORIGIN).shift(ratio_3*verticies_2[i]) for i in range(9)])
        sectors = VGroup(iter_3, iter_2, iter_1, iter_0).scale(4/3, about_point = ORIGIN)
        self.add(sectors.scale(0.8).shift(3.2*RIGHT + 0.75*DOWN))
        text_1 = Text("一百年前", font = "FZDaHei-B02S", stroke_width = 4, stroke_color = BACK, fill_color = WHITE).set_style(stroke_background = True).scale(2).shift(3.2*LEFT+2.8*UP)
        text_2 = Text("一百年后", font = "FZDaHei-B02S", stroke_width = 4, stroke_color = BACK, fill_color = WHITE).set_style(stroke_background = True).scale(2).shift(3.2*RIGHT+2.8*UP)
        line = Line(4*UP, 4*DOWN)
        arrow = Polygon(1.5*LEFT+0.6*UP, 0.4*RIGHT+0.6*UP, 0.4*RIGHT+1.2*UP, 2*RIGHT, 0.4*RIGHT+1.2*DOWN, 0.4*RIGHT+0.6*DOWN, 1.5*LEFT+0.6*DOWN, color = RED, fill_opacity = 1, stroke_width = 0).close_path()
        self.add(text_1, text_2, line, arrow.scale(0.7))

#################################################################### 

class Template(FrameScene):
    def construct(self):
        pass