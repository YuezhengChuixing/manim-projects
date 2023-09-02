from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Trailer(CoverScene):
    def construct(self):
        self.camera.anti_alias_width = 0
        rectangle_0 = Rectangle(height = 2, width = 12, color = BLUE, stroke_width = 0, fill_opacity = 0.5).shift(2*UP)
        corner_left = 3*DOWN + 6*LEFT
        corner_right = 3*DOWN + 6*RIGHT
        centers_1 = [corner_left, corner_right]
        rectangles_1 = [rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[0]).set_color(interpolate_color(GREEN, BLUE, 0.5)), rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[1]).set_color(interpolate_color(BLUE, GREEN, 0.5))]
        self.add(*rectangles_1, rectangle_0)
        last_centers = centers_1
        last_rectangles = rectangles_1
        for i in range(2, 10):
            centers = [*(last_centers-corner_left)/3+corner_left, *(last_centers-corner_right)/3+corner_right]
            rectangles = [last_rectangles[j//2].copy().scale(np.array([1/3, 1/2, 0]), about_point = centers[j]).set_color(interpolate_color(GREEN, BLUE, 1/2**i)) for j in range(2**i)]
            self.add(*rectangles)
            last_centers = centers
            last_rectangles = rectangles

        text = MTex(r"0.\dot9\ne 1").scale(7).set_stroke(width = 20, color = BLACK, background = True)
        order_text = VGroup(*text[0:4], text[5], text[4], text[6], anti_alias_width = 1.5)
        text[0:4].set_fill(color = YELLOW)
        text[4].set_fill(color = RED)
        text[6].set_fill(color = YELLOW)
        self.add(order_text)

class Test1(FrameScene):
    # failed
    def construct(self):
        rectangle_0 = Rectangle(height = 2, width = 10, color = BLUE, stroke_width = 0, fill_opacity = 1).shift(1.5*UP)
        corner_left = 2*DOWN + 5*LEFT
        corner_right = 2*DOWN + 5*RIGHT
        centers_1 = [corner_left, corner_right]
        rectangles_1 = [rectangle_0.copy().scale(np.array([1/3, 2/5, 0]), about_point = centers_1[0]).set_color(interpolate_color(GREEN, BLUE, 0.5)), rectangle_0.copy().scale(np.array([1/3, 2/5, 0]), about_point = centers_1[1]).set_color(interpolate_color(BLUE, GREEN, 0.5))]
        cantor = VGroup(*rectangles_1, rectangle_0)
        last_centers = centers_1
        last_rectangles = rectangles_1
        for i in range(2, 10):
            centers = [*(last_centers-corner_left)/3+corner_left, *(last_centers-corner_right)/3+corner_right]
            rectangles = [last_rectangles[j//2].copy().scale(np.array([1/3, 2/5, 0]), about_point = centers[j]).set_color(interpolate_color(GREEN, BLUE, 1/2**i)) for j in range(2**i)]
            cantor.add(*rectangles)
            last_centers = centers
            last_rectangles = rectangles
        board = Rectangle(height = 8.4, width = 15.2, fill_opacity = 1, fill_color = BACK, stroke_color = YELLOW_E)
        inner = Rectangle(height = 8.4, width = 15, fill_opacity = 0, fill_color = BLACK, stroke_color = WHITE)
        self.add(cantor.shift(15*RIGHT), board, inner).play(cantor.animate.shift(15*LEFT), board.animate.shift(7.6*LEFT), inner.animate.shift(7.6*LEFT), run_time = 2)

class Test2(FrameScene):
    # almostly failed
    def construct(self):
        rectangle_0 = Rectangle(height = 2, width = 10, color = BLUE, stroke_width = 0, fill_opacity = 1).shift(1.5*UP)
        corner_left = 2*DOWN + 5*LEFT
        corner_right = 2*DOWN + 5*RIGHT
        centers_1 = [corner_left, corner_right]
        rectangles_1 = [rectangle_0.copy().scale(np.array([1/3, 2/5, 0]), about_point = centers_1[0]).set_color(interpolate_color(GREEN, BLUE, 0.5)), rectangle_0.copy().scale(np.array([1/3, 2/5, 0]), about_point = centers_1[1]).set_color(interpolate_color(BLUE, GREEN, 0.5))]
        cantor = VGroup(*rectangles_1, rectangle_0)
        last_centers = centers_1
        last_rectangles = rectangles_1
        for i in range(2, 10):
            centers = [*(last_centers-corner_left)/3+corner_left, *(last_centers-corner_right)/3+corner_right]
            rectangles = [last_rectangles[j//2].copy().scale(np.array([1/3, 2/5, 0]), about_point = centers[j]).set_color(interpolate_color(GREEN, BLUE, 1/2**i)) for j in range(2**i)]
            cantor.add(*rectangles)
            last_centers = centers
            last_rectangles = rectangles
        board = Rectangle(height = 8.4, width = 15.2, fill_opacity = 1, fill_color = BACK, stroke_width = 0).shift(15.1*RIGHT)
        inner = Rectangle(height = 8.4, width = 0.1, fill_opacity = 1, fill_color = BLACK, stroke_width = 0).shift(7.5*RIGHT)
        line_1 = Line(4.2*UP, 4.2*DOWN).shift(0.05*LEFT + 7.5*RIGHT)
        line_2 = Line(4.2*UP, 4.2*DOWN, color = YELLOW_E).shift(0.05*RIGHT + 7.5*RIGHT)
        inner.add(line_1, line_2)
        alpha = ValueTracker(0.0)
        rectangles = cantor.submobjects
        func = lambda mob: mob.restore().shift(15*alpha.get_value()*LEFT).set_points(Intersection(mob, board).get_points())
        for rect in rectangles:
            rect.shift(15*RIGHT).save_state().add_updater(func)
        self.add(board, *rectangles, inner).play(alpha.animate.set_value(1), board.animate.shift(7.6*LEFT), inner.animate.shift(7.6*LEFT), run_time = 2)

#################################################################### 

class Cut(Animation):
    def __init__(self, position: np.ndarray = ORIGIN, length: float = 2, **kwargs):
        width = [length*4/2500*i*(100-i) for i in range(50)]
        mobject = Line(position + length/2*UP, position + length/2*DOWN, stroke_width = width + width[::-1]).insert_n_curves(99)
        super().__init__(mobject, **kwargs)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        start, end = starting_submobject.get_start(), starting_submobject.get_end()
        head, tail = interpolate(start, end, alpha*(3-alpha**2)/2), interpolate(start, end, alpha**2*(3-alpha)/2)
        submobject.become(starting_submobject).put_start_and_end_on(head, tail)

class Test3(FrameScene):
    def construct(self):
        line = UnitInterval()
        self.add(line).play(Cut())
        self.play(Cut(RIGHT), Cut(LEFT, 1))
        self.wait(1)


#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]