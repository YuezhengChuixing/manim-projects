from __future__ import annotations
from manimlib import *
import numpy as np

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from manimlib.mobject.mobject import Mobject


#####################################################################

#整段垮掉，排不出是哪里出了bug

class MyShowCreation(ShowPartial):
    CONFIG = {
        "lag_ratio": 1,
    }

    def get_bounds(self, alpha: float) -> tuple[float, float]:
        return (0, alpha)

class ShowDestruction(ShowPartial):
    CONFIG = {
        "lag_ratio": 1,
        "remover" : True
    }

    def get_bounds(self, alpha: float) -> tuple[float, float]:
        print(alpha)
        return (alpha, 1)
        # tw = 0.5
        # upper = interpolate(0, 1 + tw, alpha)
        # lower = upper - tw
        # upper = min(upper, 1)
        # lower = max(lower, 0)
        # return (lower, upper)

    def finish(self) -> None:
        super().finish()
        for submob, start in self.get_all_families_zipped():
            submob.pointwise_become_partial(start, 0, 1)

class Flash_1(ShowPartial):
    CONFIG = {
        "remover" : True
    }

    def get_bounds(self, alpha: float) -> tuple[float, float]:
        tw = 0.5
        upper = interpolate(0, 1 + tw, alpha)
        lower = upper - tw
        upper = min(upper, 1)
        lower = max(lower, 0)
        return (lower, upper)

class Flash_2(ShowPartial):
    CONFIG = {
        "remover" : True
    }

    def get_bounds(self, alpha: float) -> tuple[float, float]:
        tw = 0.5
        upper = interpolate(0, 1 + tw, alpha)
        lower = upper - tw
        upper = min(upper, 1)
        lower = max(lower, 0)
        return (lower, 1)

class Flash_3(ShowPartial):
    CONFIG = {
        "remover" : True
    }

    def get_bounds(self, alpha: float) -> tuple[float, float]:
        tw = 0.5
        upper = interpolate(0, 1 + tw, alpha)
        lower = upper - tw
        upper = min(upper, 1)
        lower = max(lower, 0)
        return (lower, 0.999)


class Test_1(Scene):
    def construct(self):

        circle_1 = Circle().shift(3*LEFT)
        circle_2 = Circle()
        circle_3 = Circle().shift(3*RIGHT)

        self.wait(1)
        self.play(Flash_1(circle_1), Flash_2(circle_2), Flash_3(circle_3))
        self.wait(1)

        dot = Dot().shift(2*RIGHT)

        # self.play(MyShowCreation(circle), dot.animate.shift(UP))
        # self.wait(1)
        # self.play(ShowDestruction(circle), dot.animate.shift(DOWN))
        # self.wait(1)
        

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Cover_2(Scene):

    def construct(self):
        title = Text("凸透镜", font = "FZDaHei-B02S").scale(4).shift(2.7*UP)
        title[0].set_color(interpolate_color(PURPLE, RED, 0.5)).shift(LEFT)
        title[1].set_color(RED)
        title[2].set_color(interpolate_color(RED, ORANGE, 0.5)).shift(RIGHT)
        self.add(title)

        thelen = ArcBetweenPoints(DOWN*2.5, UP*2.5, PI/6, color = GREEN, fill_opacity = 1, fill_color = average_color(GREEN, BLACK), stroke_width = 8).append_points(ArcBetweenPoints(UP*2.5, DOWN*2.5, PI/6).get_points()).shift(DOWN)
        dot_center = Dot(color = YELLOW).shift(DOWN)
        bench = Rectangle(width = 12, height = 0.2, fill_opacity = 1, fill_color = average_color(BLUE, BLACK)).add(*[Line(0.1*UP, 0.1*DOWN).shift((i-3)*1.5*RIGHT) for i in range(7)]).set_stroke(color = BLUE, width = 8).shift(DOWN)
        
        circle = Circle(radius = 1.2, color = PURPLE, n_components = 24, stroke_width = 8).shift(3.3*LEFT)
        def len_trans(point: np.ndarray, focus: float = 1.5):
            return focus/(point[0]+focus)*point
        ellipse = circle.copy().apply_function(len_trans).set_color(ORANGE).shift(DOWN)
        circle.shift(DOWN)
        # circle_2 = Circle(radius = 0.8, color = PURPLE, n_components = 24, stroke_width = 8).shift(4*LEFT + UP)
        # def len_trans(point: np.ndarray, focus: float = 2):
        #     return focus/(point[0]+focus)*point
        # ellipse_2 = circle_2.copy().apply_function(len_trans).set_color(ORANGE).shift(DOWN)
        # circle_2.shift(DOWN)
        self.add(bench, thelen, dot_center, circle, ellipse)#, circle_2, ellipse_2

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

class FixedText(VMobject):
    def __init__(self, text, **kwargs):
        super().__init__(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True)
        notice = Text(text, **kwargs)
        #self.set_points(notice.get_all_points())
        for mob in notice.submobjects:
            new_submob = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(mob.get_all_points())
            self.add(new_submob)

class Cover(Scene):

    def construct(self):
        back_left = Rectangle(height = 8, width = 8, fill_color = BLACK, fill_opacity = 1, stroke_width = 0).shift(4*LEFT).rotate(PI/2, UP, about_point = ORIGIN)
        back_right = Rectangle(height = 8, width = 8, fill_color = BLACK, fill_opacity = 1, stroke_width = 0).shift(4*RIGHT)
        len = Line(3*UP, 3*DOWN).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN).rotate(PI/4, UP, about_point = ORIGIN)
        ideal_piece = NumberLine([0, 6, 2], stroke_width = 8, color = BLUE)
        ideal_piece.set_stroke(width = 4).scale(np.array([1, 2, 1]))
        x_bench = ideal_piece.copy().shift(3*RIGHT)
        z_bench = ideal_piece.copy().shift(3*LEFT).rotate(PI/2, UP, about_point = ORIGIN)
        dot = Dot(color = YELLOW).rotate(PI/4, UP, about_point = ORIGIN)
        line_z = DashedLine(2*OUT, 2*OUT+2*RIGHT, color = BLUE, stroke_width = 2)
        line_x = DashedLine(2*RIGHT, 2*OUT+2*RIGHT, color = BLUE, stroke_width = 2)
        focus = Sphere(radius = 0.08, color = BLUE).shift(2*RIGHT+2*OUT)
        circle = Circle(radius = 0.8, color = PURPLE).shift(4*LEFT).rotate(PI/2, UP, about_point = ORIGIN)
        def focus_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[2]-focus)*np.array([point[2], -point[1], 0])
        lines = []
        for i in range(8):
            start = 4*OUT + 0.8*np.array([0, np.sin(TAU*i/8), np.cos(TAU*i/8)])
            end = focus_trans(start)
            line_i = Line(start, end, color = YELLOW)
            lines.append(line_i)
        def parameter(u: float, v: float):
            start = 4*OUT + 0.8*np.array([0, np.sin(u), np.cos(u)])
            end = focus_trans(start)
            ratio = (np.cos(v)*end[0], np.sin(v)*start[2])
            ratio /= (ratio[0] + ratio[1])
            return ratio[0]*start + ratio[1]*end
        cone = ParametricSurface(parameter, u_range = (0, TAU), v_range = (0, PI/2), opacity = 0.2, color = YELLOW)
        ellipse = circle.copy().apply_function(focus_trans).set_color(ORANGE)
        
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, PI/4))
        camera.move_to(2*OUT+2*RIGHT + 0.6*DL).set_orientation(Rotation(quadternion)).set_focal_distance(8.0)
        camera.quadternion = quadternion

        def function(t):
            return np.array([np.cos(t) - t/3,  - np.sin(t) - t/3, 0])
        arrow_line = ParametricCurve(function, t_range = [-0.2*PI, 2.6*PI], is_fixed_in_frame = True).set_color(BLUE_B).scale(0.3).next_to(1.6*RIGHT, UR, buff = 0)
        arrow_tip = ArrowTip(height = 0.2, is_fixed_in_frame = True).set_color(BLUE_B).shift(arrow_line.get_end())
        arrow_tip.rotate(PI, about_point = arrow_tip.get_base())
        text_1 = FixedText("焦点？", font = "LXGW WenKai", weight = "bold").scale(2).set_color(BLUE_B).next_to(arrow_line.get_corner(UR), UP)
        text_2 = FixedText("凸透镜", font = "LXGW WenKai", weight = "bold").scale(2).set_color(YELLOW).next_to(2*UP + 6.3*LEFT)
        text_3 = FixedText("是 这 么", font = "LXGW WenKai", weight = "bold").scale(2).set_color(YELLOW).next_to(0.5*UP + 5.8*LEFT)
        text_4 = FixedText("成像的？", font = "LXGW WenKai", weight = "bold").scale(2).set_color(YELLOW).next_to(1*DOWN + 5.3*LEFT)
        for i in range(3):
            text_2[i].shift(i*0.1*RIGHT)
            text_3[i].shift(i*0.1*RIGHT)
            text_4[i].shift(i*0.1*RIGHT)
        text_4[3].shift(0.3*RIGHT)
        text_3[1].scale(1.5).rotate(PI/12).set_color(YELLOW)
        text_3[2].scale(1.5).rotate(-PI/12).shift(0.3*RIGHT).set_color(YELLOW)
        self.add(camera, back_left, back_right, len, x_bench, z_bench, dot, line_z, line_x, circle, ellipse, cone, *lines, focus, arrow_line, arrow_tip, text_1, text_2, text_3, text_4)

###########################################################

class Template(Scene):
    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)