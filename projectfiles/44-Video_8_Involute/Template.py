from __future__ import annotations

from manimlib import *
import numpy as np

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def ratio_color(colors: list, ratio: float):

    number_colors = len(colors) - 1
    if ratio >= 1:
        index = number_colors - 1
        interpolate = 1
    else:
        ratio = number_colors * ratio
        index = int(ratio)
        interpolate = ratio - index

    return interpolate_color(colors[index], colors[index+1], interpolate)


OMEGA = unit(-PI/6)

BACK = "#333333"



#################################################################### 

class Digit(VGroup):
    def __init__(self, digit):

        super().__init__()
        self.number = []
        self.digit = digit
        for i in range (10):
            numberi = Tex(r"%d"%i).set_opacity(0)
            self.add(numberi)
            self.number.append(numberi)
        self.number[self.digit].set_opacity(1)

    def set_number(self, digit, opacity):
        self.number[self.digit].set_opacity(0)
        self.digit = digit
        self.number[self.digit].set_opacity(opacity)
        return self

class Value(VGroup):
    def __init__(self, decimal):

        super().__init__()
        distance = 0.12
        self.one = Digit(0).shift(2*distance*LEFT)
        self.point = MTex(r"\cdot").shift(0.5*distance*LEFT + distance*DOWN)
        self.dec = Digit(0).shift(distance*RIGHT)
        self.cent = Digit(0).shift(3*distance*RIGHT)
        self.add(self.one, self.point, self.dec, self.cent)
        self.set_year(decimal)

    def set_year(self, year, opacity = 1):
        self.cent.set_number(year % 10, opacity)
        year = int(year / 10)
        self.dec.set_number(year % 10, opacity)
        year = int(year / 10)
        self.one.set_number(year % 10, opacity)

class SwallowIn(Homotopy):
    CONFIG = {
        "run_time": 2,
        "remover": True
    }

    def __init__(self, mobject, target = None, **kwargs):
        digest_config(self, kwargs, locals())
        if target is None:
            target = mobject.get_center()
        distance = max(
            get_norm(mobject.get_corner(UL)-target), 
            get_norm(mobject.get_corner(UR)-target), 
            get_norm(mobject.get_corner(DL)-target), 
            get_norm(mobject.get_corner(DR)-target),
            )
        
        def homotopy(x, y, z, t):
            position = np.array([x, y, z])
            vect = position - target
            length = get_norm(vect)
            move = t * distance
            if move >= length:
                return target
            else:
                ratio = 1 - move/length
                return target + np.array([ratio * vect[0], np.sqrt(ratio) * vect[1], 0])

        super().__init__(homotopy, mobject, **kwargs)

class Notice(VGroup):
    def __init__(self, m_text1, m_text2, **kwargs):

        super().__init__(**kwargs)
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        if self.line1.get_height() < 0.5:
            self.line1.scale(1.25)
        if self.line2.get_height() < 0.5:
            self.line2.scale(1.25)
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

class RadCurve(VMobject):
    CONFIG = {
        "t_range": [0, TAU, TAU/100],
        "epsilon": 1e-8,
        # TODO, automatically figure out discontinuities
        "use_smoothing": True,
    }

    def __init__(
        self,
        t_func: Callable[[float], float],
        t_range: Sequence[float] | None = None,
        **kwargs
    ):
        digest_config(self, kwargs)
        if t_range is not None:
            self.t_range[:len(t_range)] = t_range
        # To be backward compatible with all the scenes specifying t_min, t_max, step_size
        self.t_range = [
            kwargs.get("t_min", self.t_range[0]),
            kwargs.get("t_max", self.t_range[1]),
            kwargs.get("step_size", self.t_range[2]),
        ]
        self.t_func = t_func
        VMobject.__init__(self, **kwargs)

    def init_points(self):
        t_min, t_max, step = self.t_range
        tail = ORIGIN
        self.start_new_path(tail)

        if step == 0:
            return self
        else:
            for time in np.arange(t_min, t_max, step):
                nudge = unit(time+step/2) * (self.t_func(time+step) - self.t_func(time))
                new_tail = tail + nudge
                self.add_line_to(new_tail)
                tail = new_tail
            if self.use_smoothing:
                self.make_approximately_smooth()
            if not self.has_points():
                self.set_points([self.t_func(t_min)])
            return self
        
class RadParameterCurve(VMobject):
    CONFIG = {
        "t_range": [0, TAU, TAU/100],
        "epsilon": 1e-8,
        # TODO, automatically figure out discontinuities
        "use_smoothing": True,
    }

    def __init__(
        self,
        t_func: Callable[[float], np.ndarray],
        t_range: Sequence[float] | None = None,
        **kwargs
    ):
        digest_config(self, kwargs)
        if t_range is not None:
            self.t_range[:len(t_range)] = t_range
        # To be backward compatible with all the scenes specifying t_min, t_max, step_size
        self.t_range = [
            kwargs.get("t_min", self.t_range[0]),
            kwargs.get("t_max", self.t_range[1]),
            kwargs.get("step_size", self.t_range[2]),
        ]
        self.t_func = t_func
        VMobject.__init__(self, **kwargs)

    def init_points(self):
        t_min, t_max, step = self.t_range
        tail = ORIGIN
        self.start_new_path(tail)

        if step == 0:
            return self
        else:
            for time in np.arange(t_min, t_max, step):

                nudge = unit(self.t_func(time+step/2)[1]) * (self.t_func(time+step)[0] - self.t_func(time)[0])
                new_tail = tail + nudge
                self.add_line_to(new_tail)
                tail = new_tail
            if self.use_smoothing:
                self.make_approximately_smooth()
            if not self.has_points():
                self.set_points([ORIGIN])
            return self
        
class Shade(Rectangle):
    CONFIG = {
        "height": FRAME_HEIGHT,
        "width": FRAME_WIDTH,
        "fill_opacity": 1,
        "fill_color": BACK, 
        "stroke_width": 0,
        "buff": 0
    }
    def __init__(
        self,
        mobject: Mobject = None, 
        **kwargs
    ):
        if mobject is not None:
            BackgroundRectangle.__init__(self, mobject, **kwargs)
        else:
            super().__init__(**kwargs)
        
class Grow(FadeInFromPoint):
    def __init__(
        self,
        mobject: Arrow, 
        **kwargs
    ):
        point = mobject.get_start()
        super().__init__(mobject, point, **kwargs)

class SnowFlake(VGroup):
    def __init__(self):

        super().__init__()
        snowhex1 = SnowHex(2,1)
        snowhex2 = SnowHex(6,2)
        snowhex3 = SnowHex(6,3)
        snowhex4 = SnowHex(6,4)
        snowring2 = VGroup(snowhex1)
        snowring3 = SnowRing(3)
        snowring4 = SnowRing(4)
        snowring5 = SnowRing(5)
        snowring6 = VGroup(snowhex2, snowhex3, snowhex4)

        outer_radius = 12
        arcs = VGroup()
        arc = ArcBetweenPoints(outer_radius * unit(TAU/12), outer_radius * unit(-TAU/12), angle = PI + PI/12).insert_n_curves(16)
        width = arc.get_width()
        ratio = 2/3
        arc.set_width(width*ratio, stretch = True).shift(width*RIGHT*(1-ratio)/2)
        for i in range (6):
            arc_i = arc.copy().rotate(i*TAU/6, about_point = ORIGIN)
            arcs.add(arc_i)
        
        self.add(snowring2, snowring3, snowring4, snowring5, snowring6, arcs)
        self.scale(0.3)

class SnowRing(VGroup):
    def __init__(self, radius):

        super().__init__()
        for i in range(radius):
            snowhexi = SnowHex(radius, i)
            self.add(snowhexi)

class SnowHex(VGroup):
    def __init__(self, x_position, omega_position):

        super().__init__()
        x = x_position
        omega = omega_position
        for i in range(6):
            snowi = Snow(x, omega)
            self.add(snowi)
            (x, omega) = (x-omega, x)

class Snow(RegularPolygon):
    def __init__(self, x_position, omega_position):

        super().__init__(n = 6, stroke_width = 2)
        self.scale(0.5)
        self.shift( x_position*UP + omega_position*OMEGA)

class SpreadOut(Animation):
    # 本部分代码来自一碗星空汤（b站ID：一碗星空咕）
    # 另外感谢不愿意透露姓名的群友（群内ID：嘤）的帮助，虽然他的代码最后没用上（）
    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, **kwargs)

        self.center = mobject.get_center()
        self.radius = get_norm(mobject.get_corner(UL) - self.center)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        points = starting_submobject.data["points"] - self.center
        dr = self.radius * alpha

        to_delete = np.where(np.linalg.norm(points[::3], axis = 1) > dr)
        deleted = np.delete(points.reshape((int(points.shape[0]/3), 3, 3)), to_delete, axis = 0) + self.center
        submobject.data["points"] = deleted.reshape(deleted.shape[0]*3, 3)


#################################################################### 

class Intro0(Scene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("费心思编什么大道理，\n开摆！", font = 'simsun', t2c={("大道理"): GREEN, ("开摆"): BLUE})
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DR), DL)
        ##  Showing object
        self.play(Write(quote), runtime = 2)
        self.play(Write(author), Write(notice0))
        self.wait(2)
        self.play(FadeOut(quote), FadeOut(author))
        self.wait(1)


class Intro1(Scene):
    def construct(self):

        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        notice1 = Notice("视频前言", "请听介绍")
        notice2 = Notice("我乐正垂星", "就算饿死")
        notice3 = Notice("真香", "")
        notice4 = Notice("同行评审", "请　模仿")
        notice5 = Notice("视频前言", "请听介绍")
        notice6 = Notice("传统艺能", "请　三连")

        self.play(ReplacementTransform(notice0, notice1))
        self.waiting(0, 16) #去年暑假的时候

        mathemaniac = ImageMobject("mathemaniac.jpg").shift(0.5*DOWN)
        bv = Text("BV1wT411w7Ht", font = "Times New Roman").scale(0.5).next_to(mathemaniac, UP, buff = 0.3)
        self.play(FadeIn(mathemaniac, 0.5*UP), FadeIn(bv, 0.5*UP))
        self.waiting(0, 21) #我刷到了这么一部视频
        self.waiting(0, 13) #（空闲）

        self.play(WiggleOutThenIn(mathemaniac), run_time = 2)
        texts = r"\sin(x)", r"=x", r"-\frac{x^3}{3!}", r"+\frac{x^5}{5!}", r"-\frac{x^7}{7!}", r"+\frac{x^9}{9!}", r"-\cdots"
        taylor = MTex(r"".join(texts), isolate = texts, tex_to_color_map = {r"\sin(x)": BLUE, r"=": WHITE}, color = GREEN).scale(0.8).shift(3.3*UP)
        parts = VGroup(*[taylor.get_part_by_tex(text) for text in texts])
        rectangles = [SurroundingRectangle(parts[:i+2]) for i in range(6)]
        self.play(Write(taylor))
        self.waiting(0, 26) #从封面看 这部视频讲的是正弦函数泰勒展开的几何含义
        self.waiting(0, 19) #（空闲）

        arrow_x = Arrow(4*LEFT, 4*RIGHT, buff = 0, stroke_width = 3)
        arrow_y = Arrow(1.2*DOWN, 1.2*UP, buff = 0, stroke_width = 3)
        axes = VGroup(arrow_x, arrow_y).shift(2.8*LEFT)
        self.play(mathemaniac.animate.shift(4*RIGHT), bv.animate.shift(4*RIGHT), FadeIn(axes, 2*RIGHT))
        shade_0 = Rectangle(height = 1.5, width = 16, fill_opacity = 1, stroke_width = 0, fill_color = BACK).shift(3.25*UP)
        shade = VGroup(shade_0, shade_0.copy().shift(6.5*DOWN))
        graph = FunctionGraph(np.sin, [-4, 4, 0.01], color = BLUE).shift(2.8*LEFT)
        graph_0 = FunctionGraph(lambda t: t, [-4, 4, 0.01], color = GREEN).shift(2.8*LEFT)
        graph_1 = FunctionGraph(lambda t: t-t**3/6, [-4, 4, 0.01], color = GREEN).shift(2.8*LEFT)
        graph_2 = FunctionGraph(lambda t: t-t**3/6+t**5/120, [-4, 4, 0.01], color = GREEN).shift(2.8*LEFT)
        graph_3 = FunctionGraph(lambda t: t-t**3/6+t**5/120-t**7/5040, [-4, 4, 0.01], color = GREEN).shift(2.8*LEFT)
        graph_4 = FunctionGraph(lambda t: t-t**3/6+t**5/120-t**7/5040+t**9/362880, [-4, 4, 0.01], color = GREEN).shift(2.8*LEFT)
        graph_5 = graph.copy().set_color(GREEN)
        self.add(graph, graph_0, shade, taylor, notice1, mathemaniac, bv).play(ShowCreation(graph), ShowCreation(graph_0), ShowCreation(rectangles[0]), ReplacementTransform(notice1, notice2))
        self.wait(1)
        self.play(Transform(graph_0, graph_1), Transform(rectangles[0], rectangles[1]))
        self.wait(1)
        self.play(Transform(graph_0, graph_2), Transform(rectangles[0], rectangles[2]))
        self.wait(1)
        self.play(Transform(graph_0, graph_3), Transform(rectangles[0], rectangles[3]))
        self.wait(1)
        self.play(Transform(graph_0, graph_4), Transform(rectangles[0], rectangles[4]))
        self.wait(1)
        self.play(Transform(graph_0, graph_5), Transform(rectangles[0], rectangles[5]))
        self.waiting(3+3+2+0+1-12, 26+1+26+15+26) #说实话 这种题材的视频没什么好看的 无非就是给泰勒展开硬找个几何含义 然后把泰勒展开的推导过程生搬过去 （空闲） 不过这种题材观众爱看
        self.waiting(2, 21) #播放量嘛 数学频道 不寒碜
        self.waiting(0, 21) #（空闲）
        
        arrow_x = Arrow(0.6*LEFT, 3.6*RIGHT, buff = 0, stroke_width = 3).shift(RIGHT + 2*DOWN)
        arrow_y = Arrow(0.6*DOWN, 4*UP, buff = 0, stroke_width = 3).shift(RIGHT + 2*DOWN)
        angle = 5/12*PI
        point = Dot(color = r"#EE0000", radius = 0.04).shift(3*unit(angle)).shift(RIGHT + 2*DOWN)
        arrows = VGroup(arrow_x, arrow_y)
        involute_0 = ParametricCurve(lambda t: 3*unit((angle-t)), [0, angle, DEGREES], color = ORANGE, stroke_width = 3).shift(RIGHT + 2*DOWN)
        involute_1 = ParametricCurve(lambda t: 3*(unit((angle-t))+(t*unit((angle-t)+PI/2))), [0, angle, DEGREES], color = YELLOW, stroke_width = 3).shift(RIGHT + 2*DOWN)
        involute_2 = ParametricCurve(lambda t: 3*(unit((angle-t))+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI))), [0, angle, DEGREES], color = ORANGE, stroke_width = 3).shift(RIGHT + 2*DOWN)
        involute_3 = ParametricCurve(lambda t: 3*(unit((angle-t))+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI))+(t**3/6*unit((angle-t)+PI*3/2))), [0, angle, DEGREES], color = YELLOW, stroke_width = 3).shift(RIGHT + 2*DOWN)
        involute_4 = ParametricCurve(lambda t: 3*(unit((angle-t))+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI))+(t**3/6*unit((angle-t)+PI*3/2))+(t**4/24*unit((angle-t)))), [0, angle, DEGREES], color = ORANGE, stroke_width = 3).shift(RIGHT + 2*DOWN)
        point_0 = 3*RIGHT
        point_1 = point_0 + 3*angle*UP
        point_2 = point_1 + 3*(angle)**2/2*LEFT
        point_3 = point_2 + 3*(angle)**3/6*DOWN
        point_4 = point_3 + 3*(angle)**4/24*RIGHT
        point_5 = point_4 + 3*(angle)**5/120*UP
        line_0 = Line(point_0, point_1, color = GREEN, stroke_width = 3).shift(RIGHT + 2*DOWN)
        line_1 = Line(point_1, point_2, color = BLUE, stroke_width = 3).shift(RIGHT + 2*DOWN)
        line_2 = Line(point_2, point_3, color = GREEN, stroke_width = 3).shift(RIGHT + 2*DOWN)
        line_3 = Line(point_3, point_4, color = BLUE, stroke_width = 3).shift(RIGHT + 2*DOWN)
        line_4 = Line(point_4, point_5, color = GREEN, stroke_width = 3).shift(RIGHT + 2*DOWN)
        angle = DashedLine(ORIGIN, 3*unit(angle), color = "#FFA7D7", stroke_width = 3).shift(RIGHT + 2*DOWN) #FF689B
        involutes = VGroup(arrows, involute_0, involute_1, involute_2, involute_3, involute_4, line_0, line_1, line_2, line_3, line_4, angle)
        self.play(*[FadeOut(mob, 3.5*LEFT, rate_func = rush_into) for mob in [axes, graph, graph_0]], 
                  FadeOut(shade), FadeOut(rectangles[0]), ReplacementTransform(notice2, notice3), 
                  ApplyMethod(mathemaniac.shift, 7*LEFT, run_time = 2), ApplyMethod(bv.shift, 7*LEFT, run_time = 2), 
                  *[FadeIn(mob, 3.5*LEFT, rate_func = squish_rate_func(rush_from, 0.5, 1), run_time = 2) for mob in [involutes, point]])
        self.waiting(1+3-2, 16+1) #但在六分钟后 我就完全沉浸于这期视频的美妙洞见之中了
        self.waiting(0, 19) #（空闲）

        text_0 = MTex(r"\frac{x^0}{0!}", color = BLUE).scale(0.8).next_to(1.5*RIGHT, DOWN, buff = 0.1).shift(RIGHT + 2*DOWN)
        text_1 = MTex(r"\frac{x^1}{1!}", color = GREEN).scale(0.7).next_to(line_0, RIGHT, buff = 0.1)
        text_2 = MTex(r"\frac{x^2}{2!}", color = BLUE).scale(0.6).next_to(line_1, UP, buff = 0.1)
        text_3 = MTex(r"\frac{x^3}{3!}", color = GREEN).scale(0.5).next_to(line_2, LEFT, buff = 0.1)
        text_4 = MTex(r"\frac{x^4}{4!}", color = BLUE).scale(0.4).next_to(line_3, DOWN, buff = 0.1)
        text_5 = MTex(r"\frac{x^5}{5!}", color = GREEN).scale(0.3).next_to(line_4, RIGHT, buff = 0.1)
        self.play(Write(text_0))
        self.play(Write(text_1))
        self.play(Write(text_2))
        self.play(Write(text_3))
        self.play(Write(text_4))
        self.play(Write(text_5))
        self.waiting(2+2-6, 21+27+22) #它的几何含义完全不是硬找的 而是渐开线的一个十分自然的性质的应用 （空闲）
        involutes.add(text_0, text_1, text_2, text_3, text_4, text_5)

        self.play(ReplacementTransform(notice3, notice4))
        self.waiting(0, 20) #当时看到这里
        self.waiting(3, 12) #我已经忍不住要看后面十六分钟又会有什么内容了
        self.waiting(0, 18) #（空闲）

        self.waiting(1, 17) #比较可惜的是
        self.play(FadeOut(mathemaniac, 1.25*LEFT, rate_func = rush_into), FadeOut(bv, 1.25*LEFT, rate_func = rush_into), 
                  ApplyMethod(involutes.shift, 2.5*LEFT, run_time = 2), ApplyMethod(point.shift, 2.5*LEFT, run_time = 2))
        self.waiting(2, 4) #后面十六分钟只是用微元法把渐开线的性质证了一遍
        self.waiting(1, 28) #并没有什么新东西
        self.waiting(1, 23) #这让我直呼浪费

        self.play(FadeOut(involutes), FadeOut(point), FadeOut(taylor), ReplacementTransform(notice4, notice5))
        function_1 = lambda t: np.array([2*t + np.sin(2*t), 1 - np.cos(2*t), 0])
        function_2 = lambda t: np.array([2*t - np.sin(2*t), np.cos(2*t) - 1, 0])
        cycloid = ParametricCurve(function_1, [0, PI, PI/100], color = YELLOW).shift(PI*LEFT)
        point = Dot(color = RED).shift(PI*LEFT)
        line = Line(PI/2*LEFT, PI/2*LEFT, color = [YELLOW, RED]).shift(0.5*UP)
        self.play(ShowCreation(cycloid), FadeIn(point, scale = np.infty))
        alpha = ValueTracker(0.0)
        def line_updater(mob: Line):
            value = alpha.get_value()
            start = function_1(value) + PI*LEFT
            end = function_2(value) + PI*LEFT
            mob.put_start_and_end_on(start, end)
        def point_updater(mob: Dot):
            value = alpha.get_value()
            position = function_2(value) + PI*LEFT
            mob.move_to(position)
        point.add_updater(point_updater)
        line.add_updater(line_updater)
        trace = TracedPath(point.get_center)
        self.add(trace, line, point).play(alpha.animate.set_value(PI), run_time = 2)
        point.clear_updaters()
        line.clear_updaters()
        trace.clear_updaters()
        cycloid.add(trace, line, point)
        self.play(cycloid.animate.scale(0.5).shift(4*LEFT))

        function_1 = lambda t: 2*np.exp(-t)*(np.sin(t) - np.cos(t))
        function_2 = lambda t: 2*np.exp(-t)*(-np.sin(t) - np.cos(t))
        function_3 = lambda t: 2*np.exp(-t)*(-np.sin(t) + np.cos(t))
        function_4 = lambda t: 2*np.exp(-t)*(np.sin(t) + np.cos(t))
        point_1 = Dot(color = RED).shift(2*DOWN)
        point_2 = Dot(color = RED).shift(2*DOWN + 4* RIGHT)
        point_3 = Dot(color = RED).shift(2*UP + 4* RIGHT)
        point_4 = Dot(color = RED).shift(2*UP)
        square = Square(side_length = 4, color = YELLOW).shift(2*RIGHT)
        self.play(ShowCreation(square))
        self.play(*[FadeIn(mob) for mob in [point_1, point_2, point_3, point_4]])

        alpha = ValueTracker(1.0)
        def point_updater_1(mob: Dot):
            value = alpha.get_value()
            if value == 0:
                position = 2*RIGHT
            else:
                value = -np.log(value)
                position = np.array([function_1(value) + 2, function_2(value), 0])
            mob.move_to(position)
        def point_updater_2(mob: Dot):
            value = alpha.get_value()
            if value == 0:
                position = 2*RIGHT
            else:
                value = -np.log(value)
                position = np.array([function_2(value) + 2, function_3(value), 0])
            mob.move_to(position)
        def point_updater_3(mob: Dot):
            value = alpha.get_value()
            if value == 0:
                position = 2*RIGHT
            else:
                value = -np.log(value)
                position = np.array([function_3(value) + 2, function_4(value), 0])
            mob.move_to(position)
        def point_updater_4(mob: Dot):
            value = alpha.get_value()
            if value == 0:
                position = 2*RIGHT
            else:
                value = -np.log(value)
                position = np.array([function_4(value) + 2, function_1(value), 0])
            mob.move_to(position)
        point_1.add_updater(point_updater_1)
        point_2.add_updater(point_updater_2)
        point_3.add_updater(point_updater_3)
        point_4.add_updater(point_updater_4)
        trace_1 = TracedPath(point_1.get_center)
        trace_2 = TracedPath(point_2.get_center)
        trace_3 = TracedPath(point_3.get_center)
        trace_4 = TracedPath(point_4.get_center)

        self.add(trace_1, trace_2, trace_3, trace_4, point_1, point_2, point_3, point_4).play(alpha.animate.set_value(0.0), run_time = 2, rate_func = linear)
        for mob in [trace_1, trace_2, trace_3, trace_4, point_1, point_2, point_3, point_4]:
            mob.clear_updaters()
        self.waiting(2+3+3-9, 29+13+11) #因为这部视频的思路确实能走得更远 可以和好几类有趣的曲线都扯上关系 而这 就是我接下来要分享给大家的内容
        self.waiting(0, 19) #（空闲）
        self.remove(cycloid, square, trace_1, trace_2, trace_3, trace_4, point_1, point_2, point_3, point_4)

        like = Text("", font = 'vanfont').shift(3*LEFT).scale(2)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT).scale(2)
        sanlian = VGroup(like, coin, star)

        self.play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, np.array([0,0,0])), FadeInFromPoint(star, 3*RIGHT), ReplacementTransform(notice5, notice6))
        self.play(Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), sanlian.animate.set_color("#00A1D6"))
        self.waiting(1+1-2,19+24) #长按点赞一键三连 我们开始吧
        
        self.waiting(2, 26)
        self.play(FadeOut(notice6), FadeOut(sanlian))
        self.waiting(3, 0) #到此共72秒
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)


####################################################################  

class Chapter1_0(Scene):

    def construct(self):

        text1 = Text("第一节 三角函数与圆的渐开线", font = 'simsun', t2c={"第一节": YELLOW, "三角函数": GREEN, "圆的渐开线": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))
        
class Chapter1_1(Scene):
    def construct(self):
        notice1 = Notice("本节内容", "请　期待")
        notice2 = Notice("高中知识", "请　复习")
        notice3 = Notice("思路介绍", "请　专注")

        mathemaniac = ImageMobject("mathemaniac.jpg")
        self.play(Write(notice1), FadeIn(mathemaniac, UP))
        self.waiting(1, 19) #为了表示我对这个思路的喜爱
        self.waiting(2, 9) #我决定把它再向大家介绍一遍
        self.waiting(0, 21) #（空闲）

        arrow_x = Arrow(2.4*LEFT, 2.4*RIGHT, buff = 0)
        arrow_y = Arrow(2.4*DOWN, 2.4*UP, buff = 0)
        axes = VGroup(arrow_x, arrow_y)
        self.remove(mathemaniac).play(ReplacementTransform(notice1, notice2), ShowCreation(axes, run_time = 2))
        self.waiting(0, 12) #我们在高一就已经学到过
        self.waiting(2, 20) #三角函数是可以用单位圆来表示的
        self.waiting(0, 21) #（空闲）

        origin = Dot(color = RED)
        circle = Circle(radius = 2, color = YELLOW)
        dot = Dot(color = RED).shift(2*RIGHT)
        radius = Line(ORIGIN, 2*RIGHT, color = RED)
        angle = MTex(r"\alpha").scale(0.7).save_state()
        label = MTex(r"(\cos\alpha, \sin\alpha)").scale(0.8).next_to(2*unit(PI/3), UR, buff = 0.1)
        alpha = ValueTracker(0.0)
        def angle_updater(mob: MTex):
            value = alpha.get_value()
            mob.restore().shift(0.4*unit(value*PI/6)).scale(value).set_opacity(value)
        angle.add_updater(angle_updater)
        self.play(FadeIn(origin, scale = np.infty))
        self.waiting(1, 0) #以坐标系原点为圆心
        self.play(ShowCreation(circle))
        self.waiting(0, 28) #作一个半径为1的圆
        self.add(radius, origin).play(ShowCreation(radius))
        self.play(FadeIn(dot, scale = np.infty))
        self.waiting(0, 3) #再从x轴正半轴出发
        self.add(angle).play(Rotate(dot, PI/3, about_point = ORIGIN), Rotate(radius, PI/3, about_point = ORIGIN), alpha.animate.set_value(1.0))
        angle.clear_updaters()
        self.waiting(0, 25) #转过α角
        self.play(Write(label))
        self.waiting(3, 22) #这一点的横纵坐标 就分别是cosα和sinα
        self.waiting(1, 1) #（空闲）

        function_1 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2)))
        function_2 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2))+(t**2/2*unit(t-PI)))
        curve = ParametricCurve(function_1, [0, PI, DEGREES], color = YELLOW, stroke_width = 6).shift(2*LEFT+2*DOWN)
        curve_base = curve.copy().set_stroke(color = WHITE, width = 4)
        involute = ParametricCurve(function_2, [0, PI, DEGREES], color = ORANGE, stroke_width = 6).shift(2*LEFT+2*DOWN)
        shade = Square(side_length = 7, color = BACK, stroke_width = 0, fill_opacity = 1)
        self.play(FadeIn(shade))
        self.remove(axes, origin, circle, dot, radius, angle, label, shade)
        shade = Square(side_length = 0.1, color = BACK, stroke_width = 0, fill_opacity = 1).shift(np.array([-3.5, -2+1.5*PI, 0]))
        self.waiting(2, 13) #如果数学老师讲选修比较尽心尽力的话
        self.add(curve_base, shade).play(ShowCreation(curve_base), rate_func = rush_from)
        self.waiting(1, 4) #我们在高二还会学到渐开线
        self.waiting(0, 21) #（空闲）

        self.add(curve, shade).play(ShowCreation(curve), rate_func = rush_from)
        self.waiting(2, 9) #我们把曲线当成是一条不可伸缩的绳子
        curve_base.set_stroke(color = GREY, width = 3)
        alpha = ValueTracker(0.0)
        def curve_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_1, [value, PI, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(function_1(value), function_2(value)).shift(2*LEFT+2*DOWN)
        def dot_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(function_2(value)).shift(2*LEFT+2*DOWN)
        def involute_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_2, [0, value, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        curve.add_updater(curve_updater)
        line = Line(color = [YELLOW, RED], stroke_width = 6).add_updater(line_updater)
        dot = Dot(color = RED).add_updater(dot_updater)
        involute_base = involute.copy().set_stroke(color = WHITE, width = 4).add_updater(involute_updater)
        self.add(involute_base, line, dot, shade).play(ShowCreation(dot))
        self.waiting(1, 10) #并且从曲线上的一点出发
        self.play(alpha.animate.set_value(PI), run_time = 3)
        for mob in [curve, line, dot, involute_base]:
            mob.clear_updaters()
        self.waiting(1+0+1-3, 22+15+11) #把曲线逐渐拉直 （空闲） 在这个过程中
        self.add(involute, dot).play(ShowCreation(involute), rate_func = rush_from, run_time = 3)
        self.waiting(0, 18) #端点的轨迹 就被叫做这条曲线的渐开线
        self.waiting(0, 29) #（空闲）

        big_shade = Rectangle(height = 8, width = 10, color = BACK, fill_opacity = 1, stroke_width = 0)
        self.play(FadeIn(big_shade), ReplacementTransform(notice2, notice3))
        arrow_x = Arrow(0.8*LEFT, 4.8*RIGHT, buff = 0, stroke_width = 4).shift(2*DOWN+2*LEFT)
        arrow_y = Arrow(0.8*DOWN, 5.2*UP, buff = 0, stroke_width = 4).shift(2*DOWN+2*LEFT)
        angle = 5/12*PI
        point = Dot(color = r"#EE0000", radius = 0.06).shift(4*unit(angle)).shift(2*DOWN+2*LEFT)
        arrows = VGroup(arrow_x, arrow_y)
        unit_vec = DashedLine(ORIGIN, 4*unit(angle), color = "#FFA7D7", stroke_width = 3).shift(2*DOWN+2*LEFT)
        angle_alpha = MTex(r"\alpha", color = "#FFA7D7").scale(0.7).shift(0.4*unit(angle/2)).shift(2*DOWN+2*LEFT)
        function_1 = lambda t: 4*unit(t)
        function_2 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2)))
        involute_base_0 = ParametricCurve(function_1, [0, angle, DEGREES], color = ORANGE).shift(2*DOWN+2*LEFT)
        involute_1 = ParametricCurve(function_2, [0, angle, DEGREES], color = BLUE).shift(2*DOWN+2*LEFT)
        involute_0 = involute_base_0.copy().set_color(GREEN)
        self.clear().add(arrows, involute_base_0, unit_vec, angle_alpha, point, big_shade, notice2)
        self.play(FadeOut(big_shade))
        self.waiting(0, 15) #我们可以从单位圆上一点出发

        alpha = ValueTracker(angle)
        def curve_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_1, [0, value, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(function_1(value), function_2(value)).shift(2*LEFT+2*DOWN)
        def involute_updater(mob: ParametricCurve):
            value = angle - alpha.get_value()
            curve = ParametricCurve(lambda t: function_2(angle - t), [0, value, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        involute_0.add_updater(curve_updater)
        involute_base_1 = involute_1.copy().set_color(YELLOW).add_updater(involute_updater)
        line_0 = Line(color = GREEN).add_updater(line_updater)
        self.add(involute_0, point).play(ShowCreation(involute_0))
        self.waiting(1, 6) #把单位圆逐渐展开
        self.add(involute_base_1, line_0, point).play(alpha.animate.set_value(0.0), run_time = 2)
        self.waiting(1+2-2, 14+26) #在这个思路中 我们只需要展到x轴正半轴就足够了
        self.waiting(0, 17) #（空闲）

        for mob in [involute_0, line_0, involute_base_1]:
            mob.clear_updaters()
        point_0 = 2*LEFT + 2*DOWN + 4*RIGHT
        point_1 = point_0 + 4*angle*UP
        point_2 = point_1 + 4*(angle)**2/2*LEFT
        point_3 = point_2 + 4*(angle)**3/6*DOWN
        point_4 = point_3 + 4*(angle)**4/24*RIGHT
        point_5 = point_4 + 4*(angle)**5/120*UP
        text_0 = MTex(r"\frac{\alpha^1}{1!}", color = GREEN).scale(0.7).next_to(line_0, RIGHT, buff = 0.1)
        text_1 = MTex(r"\frac{\alpha^2}{2!}", color = BLUE).scale(0.6).next_to((point_1+point_2)/2, UP, buff = 0.1)
        text_2 = MTex(r"\frac{\alpha^3}{3!}", color = GREEN).scale(0.5).next_to((point_2+point_3)/2, LEFT, buff = 0.1)
        text_3 = MTex(r"\frac{\alpha^4}{4!}", color = BLUE).scale(0.4).next_to((point_3+point_4)/2, DOWN, buff = 0.1)
        text_4 = MTex(r"\frac{\alpha^5}{5!}", color = GREEN).scale(0.3).next_to((point_4+point_5)/2, RIGHT, buff = 0.1)
        self.remove(involute_0).waiting(1, 20) #被拉直的这条线段
        self.play(Write(text_0)) 
        self.waiting(2, 2) #长度和没展开前一样 都是α
        self.waiting(0, 20) #（空闲）
        self.waiting(1, 20) #而比较神奇的是
        self.add(involute_1, point).play(ShowCreation(involute_1))
        self.waiting(1, 23) #这条渐开线是可以求长度的
        self.play(Write(text_1))
        self.waiting(1, 18) #算下来的结果是α^2/2
        self.waiting(0, 17) #（空闲）

        self.waiting(3, 6) #下一步 我们继续从这一点出发
        function_1 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2)))
        function_2 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI)))
        involute_2 = ParametricCurve(function_2, [0, angle, DEGREES], color = GREEN).shift(2*DOWN+2*LEFT)
        
        alpha = ValueTracker(angle)
        def curve_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_1, [0, value, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(function_1(value), function_2(value)).shift(2*LEFT+2*DOWN)
        def involute_updater(mob: ParametricCurve):
            value = angle - alpha.get_value()
            curve = ParametricCurve(lambda t: function_2(angle - t), [0, value, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        involute_1.add_updater(curve_updater)
        involute_base_2 = involute_2.copy().set_color(ORANGE).add_updater(involute_updater)
        line_1 = Line(color = BLUE).add_updater(line_updater)
        self.add(involute_base_2, line_1, point).play(alpha.animate.set_value(0.0), run_time = 2)
        self.waiting(0, 14) #把这条渐开线也拉直
        self.waiting(1, 18) #拉直后的渐开线
        self.waiting(2, 19) #仍然长α^2/2
        self.add(involute_2, point).play(ShowCreation(involute_2))
        self.waiting(0, 10) #并且这次
        self.play(Write(text_2))
        self.waiting(2, 21) #渐开线的渐开线 长度是α^3/6
        self.waiting(0, 19) #（空闲）
        for mob in [involute_1, line_1, involute_base_2]:
            mob.clear_updaters()

        function_1 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI)))
        function_2 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2)))
        involute_3 = ParametricCurve(function_2, [0, angle, DEGREES], color = BLUE).shift(2*DOWN+2*LEFT)
        alpha = ValueTracker(angle)
        def curve_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_1, [0, value, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(function_1(value), function_2(value)).shift(2*LEFT+2*DOWN)
        def involute_updater(mob: ParametricCurve):
            value = angle - alpha.get_value()
            curve = ParametricCurve(lambda t: function_2(angle - t), [0, value, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        involute_2.add_updater(curve_updater)
        involute_base_3 = involute_3.copy().set_color(YELLOW).add_updater(involute_updater)
        line_2 = Line(color = GREEN).add_updater(line_updater)
        self.add(involute_base_3, line_2, point).play(alpha.animate.set_value(0.0), run_time = 2)
        self.add(involute_3, point).play(ShowCreation(involute_3))
        self.play(Write(text_3))
        for mob in [involute_2, line_2, involute_base_3]:
            mob.clear_updaters()

        function_1 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2)))
        function_2 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2))+((angle-t)**4/24*unit(t)))
        involute_4 = ParametricCurve(function_2, [0, angle, DEGREES], color = GREEN).shift(2*DOWN+2*LEFT)
        alpha = ValueTracker(angle)
        def curve_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_1, [0, value, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(function_1(value), function_2(value)).shift(2*LEFT+2*DOWN)
        def involute_updater(mob: ParametricCurve):
            value = angle - alpha.get_value()
            curve = ParametricCurve(lambda t: function_2(angle - t), [0, value, DEGREES]).shift(2*LEFT+2*DOWN)
            mob.set_points(curve.get_all_points())
        involute_3.add_updater(curve_updater)
        involute_base_4 = involute_4.copy().set_color(YELLOW).add_updater(involute_updater)
        line_3 = Line(color = BLUE).add_updater(line_updater)
        self.add(involute_base_4, line_3, point).play(alpha.animate.set_value(0.0), run_time = 2)
        self.add(involute_4, point).play(ShowCreation(involute_4))
        self.play(Write(text_4))
        for mob in [involute_3, line_3, involute_base_4]:
            mob.clear_updaters()

        self.waiting(1, 22) #到此共93秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

        
class Chapter1_2(Scene):
    def construct(self):
        notice3 = Notice("思路介绍", "请　专注")
        notice4 = Notice("介绍完毕", "请　鼓掌")
        notice5 = Notice("完善证明", "请　模仿")

        offset = 2*DOWN+2*LEFT
        arrow_x = Arrow(0.8*LEFT, 4.8*RIGHT, buff = 0, stroke_width = 4).shift(offset)
        arrow_y = Arrow(0.8*DOWN, 5.2*UP, buff = 0, stroke_width = 4).shift(offset)
        arrows = VGroup(arrow_x, arrow_y)
        angle = 5/12*PI
        point = Dot(color = r"#EE0000", radius = 0.06).shift(4*unit(angle)).shift(offset)
        unit_vec = DashedLine(ORIGIN, 4*unit(angle), color = "#FFA7D7", stroke_width = 3).shift(offset)
        angle_alpha = MTex(r"\alpha", color = "#FFA7D7").scale(0.7).shift(0.4*unit(angle/2)).shift(offset)
        # function_0 = lambda t: 4*unit(angle-t)
        # function_1 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2)))
        # function_2 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI)))
        # function_3 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI))+(t**3/6*unit((angle-t)+PI*3/2)))
        # function_4 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI))+(t**3/6*unit((angle-t)+PI*3/2))+(t**4/24*unit(angle-t)))
        function_0 = lambda t: 4*unit(t)
        function_1 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2)))
        function_2 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI)))
        function_3 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2)))
        function_4 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2))+((angle-t)**4/24*unit(t)))
        involute_0 = ParametricCurve(function_0, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_1 = ParametricCurve(function_1, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_2 = ParametricCurve(function_2, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_3 = ParametricCurve(function_3, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_4 = ParametricCurve(function_4, [0, angle, DEGREES], color = ORANGE).shift(offset)
        point_0 = offset + 4*RIGHT
        point_1 = point_0 + 4*angle*UP
        point_2 = point_1 + 4*(angle)**2/2*LEFT
        point_3 = point_2 + 4*(angle)**3/6*DOWN
        point_4 = point_3 + 4*(angle)**4/24*RIGHT
        point_5 = point_4 + 4*(angle)**5/120*UP
        line_0 = Line(point_0, point_1, color = GREEN)
        line_1 = Line(point_1, point_2, color = BLUE)
        line_2 = Line(point_2, point_3, color = GREEN)
        line_3 = Line(point_3, point_4, color = BLUE)
        line_4 = Line(point_4, point_5, color = GREEN)
        text_0 = MTex(r"\frac{\alpha^0}{0!}", color = BLUE).scale(0.8).next_to(offset+2*RIGHT, DOWN, buff = 0.1).shift(3*LEFT)
        text_1 = MTex(r"\frac{\alpha^1}{1!}", color = GREEN).scale(0.7).next_to(line_0, RIGHT, buff = 0.1)
        text_2 = MTex(r"\frac{\alpha^2}{2!}", color = BLUE).scale(0.6).next_to(line_1, UP, buff = 0.1)
        text_3 = MTex(r"\frac{\alpha^3}{3!}", color = GREEN).scale(0.5).next_to(line_2, LEFT, buff = 0.1)
        text_4 = MTex(r"\frac{\alpha^4}{4!}", color = BLUE).scale(0.4).next_to(line_3, DOWN, buff = 0.1)
        text_5 = MTex(r"\frac{\alpha^5}{5!}", color = GREEN).scale(0.3).next_to(line_4, RIGHT, buff = 0.1)
        involutes = [arrows, unit_vec, angle_alpha, involute_0, involute_1, involute_2, involute_3, involute_4, line_0, line_1, line_2, line_3, line_4]
        texts = VGroup(text_1, text_2, text_3, text_4, text_5)
        self.add(*involutes, texts, point, notice3)
        self.waiting(3, 0) #最后 我们会获得这样的一个螺旋
        self.waiting(0, 18) #（空闲）

        spiral = Line(offset, point_0, color = YELLOW, stroke_width = 6).add_points_as_corners([point_1, point_2, point_3, point_4, point_5])
        self.add(spiral, point).play(ShowPassingFlash(spiral), run_time = 3)
        self.waiting(1+1-3, 25+29) #螺旋从原点出发 顺着横平竖直的方向
        
        circle_start = Circle(radius = 0.4, color = YELLOW).shift(4*unit(angle)+offset).save_state()
        alpha = ValueTracker(0.0)
        def circle_start_updater(mob: Circle):
            value = alpha.get_value()
            mob.restore().scale(value).pointwise_become_partial(mob, 0, value)
        circle_start.add_updater(circle_start_updater)
        self.add(circle_start).play(alpha.animate.set_value(1.0), rate_func = rush_from)
        circle_start.clear_updaters()
        self.play(circle_start.animate.scale(0), rate_func = rush_into)
        self.remove(circle_start)
        self.waiting(1, 18) #最终走到了(cosα, sinα)这一点处
        self.waiting(0, 21) #（空闲）

        self.play(*[mob.animate.shift(3*LEFT) for mob in [*involutes, texts, point]], FadeIn(text_0, 3*LEFT), run_time = 1.5)
        self.waiting(1.5, 12) #我们只需要把这些线段的长度按方向加起来
        texts_sin = r"\sin\alpha", r"=\frac{\alpha^1}{1!}", r"-\frac{\alpha^3}{3!}", r"+\frac{\alpha^5}{5!}", r"-\cdots"
        mtex_sin = MTex(r"".join(texts_sin), isolate = texts_sin).scale(0.8).next_to(1.5*UP+0.5*RIGHT)
        parts_sin = [mtex_sin.get_part_by_tex(text) for text in texts_sin]
        symbols_sin = [term[0] for term in parts_sin[1:]]
        terms_sin = [term[1:].set_color(GREEN) for term in parts_sin[1:]]
        parts_sin[0].set_color(GREEN)
        texts_cos = r"\cos\alpha", r"=\frac{\alpha^0}{0!}", r"-\frac{\alpha^2}{2!}", r"+\frac{\alpha^4}{4!}", r"-\cdots"
        mtex_cos = MTex(r"".join(texts_cos), isolate = texts_cos).scale(0.8).next_to(0.5*DOWN+0.5*RIGHT)
        parts_cos = [mtex_cos.get_part_by_tex(text) for text in texts_cos]
        symbols_cos = [term[0] for term in parts_cos[1:]]
        terms_cos = [term[1:].set_color(BLUE) for term in parts_cos[1:]]
        parts_cos[0].set_color(BLUE)
        self.play(Write(parts_sin[0]), Write(parts_cos[0]))
        self.waiting(2, 8) #就可以获得sinα和cosα的表达式
        self.waiting(0, 17) #（空闲）

        self.waiting(1, 20) #sinα的各项分别是......
        self.play(Write(symbols_sin[0]), TransformFromCopy(text_1, terms_sin[0])) #......α......
        self.play(Write(symbols_sin[1]), TransformFromCopy(text_3, terms_sin[1])) 
        self.waiting(1, 9) #......-α^3/3!......
        self.play(Write(symbols_sin[2]), TransformFromCopy(text_5, terms_sin[2])) 
        self.waiting(0, 21) #......α^5/5!......
        self.play(Write(parts_sin[4]))
        self.waiting(0, 6) #......这些
        self.waiting(2, 26) #这正好就是sinα的麦克劳林展开
        self.waiting(0, 17) #（空闲）

        self.play(Write(symbols_cos[0]), TransformFromCopy(text_0, terms_cos[0]))
        self.play(Write(symbols_cos[1]), TransformFromCopy(text_2, terms_cos[1])) 
        self.play(Write(symbols_cos[2]), TransformFromCopy(text_4, terms_cos[2])) 
        self.play(Write(parts_cos[4]))
        self.waiting(1+2-4, 25+13) #而cosα的各项 也正好就是它的麦克劳林展开
        self.waiting(0, 25) #（空闲）

        self.play(ReplacementTransform(notice3, notice4))
        self.waiting(1, 14) #这真是一个相当漂亮的过程
        self.waiting(3, 14) #它不但证明了正弦函数和余弦函数的展开式
        self.waiting(2, 15) #甚至还给每一项都找了几何意义
        self.waiting(0, 19) #（空闲）

        shade = Rectangle(height = 3, width = 6, color = BACK, fill_opacity = 1, stroke_width = 0).next_to(0.5*UP + 6.5*RIGHT)
        def shade_updater(mob, dt):
            mob.shift(2.4*dt*LEFT)
        shade.add_updater(shade_updater)
        inverse_into = lambda t: rush_into(1-t)
        inverse_from = lambda t: rush_from(1-t)
        inverse_linear = lambda t: linear(1-t)
        self.add(shade).play(FadeIn(point, scale = np.infty, remover = True), Uncreate(line_4), Uncreate(involute_4), Uncreate(text_5), rate_func = inverse_from, run_time = 0.5)
        self.play(Uncreate(line_3), Uncreate(involute_3), Uncreate(text_4), rate_func = inverse_linear, run_time = 0.3)
        self.play(Uncreate(line_2), Uncreate(involute_2), Uncreate(text_3), rate_func = inverse_linear, run_time = 0.4)
        self.play(Uncreate(line_1), Uncreate(involute_1), Uncreate(text_2), rate_func = inverse_linear, run_time = 0.55)
        self.play(Uncreate(line_0), Uncreate(involute_0), Uncreate(unit_vec), Uncreate(text_1), rate_func = inverse_linear, run_time = 0.75)
        self.remove(shade, mtex_sin, mtex_cos)
        self.play(*[Uncreate(mob, rate_func = inverse_into) for mob in [arrow_x, arrow_y, angle_alpha, text_0]], ReplacementTransform(notice4, notice5), run_time = 1.5)
        self.waiting(3+2-4, 7+13) #当然 这个过程是不完整的 我刚才跳过了求长度的步骤

        offset = 5*LEFT+2*DOWN
        function_1 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2)))
        function_2 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2))+(t**2/2*unit(t-PI)))
        curve = ParametricCurve(function_1, [0, PI, DEGREES], color = YELLOW, stroke_width = 6).shift(offset)
        involute = ParametricCurve(function_2, [0, PI, DEGREES], color = ORANGE, stroke_width = 6).shift(offset)
        self.play(ShowCreation(curve))
        self.waiting(0, 20) #现在得把它补上
        self.waiting(0, 22) #（空闲）

        self.waiting(4, 28) #为了求长度 我们需要一个比较奇怪的表达式来描述曲线
        start = Dot(color = GREY).shift(offset+1.5*RIGHT)
        point = Dot(color = RED).shift(offset+1.5*RIGHT)
        direction = Arrow(offset+1.5*RIGHT, offset+2.5*RIGHT, buff = 0, color = RED)
        start_direction = Arrow(offset+1.5*RIGHT, offset+2.5*RIGHT, buff = 0, color = GREY)
        alpha = ValueTracker(0.0)
        def point_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(function_1(angle) + offset)
        def direction_updater(mob: Arrow):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_1(angle) + offset, function_1(angle) + offset + unit(angle))
        self.play(ShowCreation(point))
        self.add(start, point)
        self.waiting(1, 7) #我们首先选定一个起始点
        self.play(FadeInFromPoint(direction, offset+1.5*RIGHT))
        self.add(start_direction, start, direction, point)
        point.add_updater(point_updater)
        direction.add_updater(direction_updater)
        self.play(alpha.animate.set_value(2*PI/3), run_time = 4)
        point.clear_updaters()
        direction.clear_updaters()
        self.waiting(2+3-5, 20+11) # 然后让它曲线上运动 这个时候 有两个值也在变化

        group_start = VGroup(start, start_direction)
        group_point = VGroup(point, direction)
        fixed_start = group_start.copy().shift(2*UL+0.5*DOWN)
        fixed_direction = group_point.copy().shift(function_1(0) - function_1(2*PI/3) + 2*UL+0.5*DOWN)
        self.play(TransformFromCopy(group_start, fixed_start), TransformFromCopy(group_point, fixed_direction))
        self.waiting(1, 15) #一个是这个点运动的方向

        angle_notation = Arc(radius = 0.2, angle = 2*PI/3, color = YELLOW).shift(offset + 1.5*UP + 0.5*LEFT)
        angle_theta = MTex(r"\theta", color = YELLOW).scale(0.6).shift(offset + 1.5*UP + 0.5*LEFT + 0.4*unit(PI/3))
        self.bring_to_back(angle_notation, angle_theta).play(ShowCreation(angle_notation), ShowCreation(angle_theta))
        self.waiting(1, 17) #对应着曲线已经转过的角度

        part_curve = ParametricCurve(function_1, [0, 2*PI/3, DEGREES], color = ORANGE, stroke_width = 6).shift(offset)
        text_length = MTex(r"s", color = ORANGE).scale(0.6).next_to(offset + function_1(PI/2), RIGHT)
        self.add(part_curve, group_start, group_point).play(ShowCreation(part_curve))
        self.waiting(1, 16) #另一个是它已经走过的路程
        self.play(Write(text_length))
        self.waiting(0, 24) #对应着曲线的长度
        self.waiting(0, 20) #（空闲）

        text_func = MTex(r"s(\theta)", tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW}).shift(4*LEFT + 3*UP)
        self.play(Write(text_func))
        self.waiting(1, 26) #这两个值之间存在一个函数关系
        circle = Circle(radius = 2, color = YELLOW, stroke_width = 6).shift(3*RIGHT)
        center = Dot().shift(3*RIGHT)
        radius = Line(3*RIGHT, 5*RIGHT, stroke_width = 6)
        text = MTex(r"1").scale(0.8).next_to(radius, UP)
        example = VGroup(radius, center, circle, text)
        value_angle = Value(0).next_to(2.98*UP + 0.5*RIGHT, buff = 0)
        value_length = Value(0).next_to(2.22*UP + 0.5*RIGHT, buff = 0)
        theta = MTex(r"\theta=", tex_to_color_map = {r"\theta": YELLOW}).next_to(3*UP + 0.5*RIGHT, LEFT)
        s = MTex(r"s=", tex_to_color_map = {r"s": ORANGE}).next_to(2.2*UP + 0.5*RIGHT, LEFT)
        arrow = group_start.copy().set_color(RED).shift(5*RIGHT - offset - function_1(0)).save_state()
        alpha = ValueTracker(0.0)
        def arrow_updater(mob: VGroup):
            value = alpha.get_value()
            mob.restore().set_opacity(value).rotate(value*PI/2, about_point = 5*RIGHT)
        arrow.add_updater(arrow_updater)
        shade = Rectangle(width = 2, height = 2, fill_opacity = 1, fill_color = BACK, stroke_width = 0).shift(2.6*UP + 0.5*RIGHT)
        shade_2 = Rectangle(width = 5, height = 5, fill_opacity = 1, fill_color = BACK, stroke_width = 0).shift(3*RIGHT)
        self.add(theta, s, value_angle, value_length, shade)
        self.play(FadeIn(example, scale = np.infty), FadeOut(shade))
        self.add(arrow).play(alpha.animate.set_value(1.0))
        arrow.clear_updaters().save_state()
        alpha = ValueTracker(0.0)
        def arrow_updater(mob: VGroup):
            value = alpha.get_value()
            mob.restore().rotate(value, about_point = 3*RIGHT)
        arrow.add_updater(arrow_updater)
        def value_updater(mob: Value):
            value = alpha.get_value()
            mob.set_year(int(100*value))
        value_angle.add_updater(value_updater)
        value_length.add_updater(value_updater)
        path = Arc(radius = 2, angle = 0, color = ORANGE, stroke_width = 6).shift(3*RIGHT)
        def path_updater(mob: Value):
            value = alpha.get_value()
            trace = Arc(radius = 2, angle = value, color = ORANGE, stroke_width = 6, ).shift(3*RIGHT)
            mob.become(trace)
        path.add_updater(path_updater)
        self.add(path, arrow).play(alpha.animate.set_value(PI/10), rate_func = rush_into)
        self.play(alpha.animate.set_value(3*PI/10), rate_func = linear)
        self.play(alpha.animate.set_value(5*PI/10), rate_func = linear)
        self.play(alpha.animate.set_value(7*PI/10), rate_func = linear)
        self.play(alpha.animate.set_value(9*PI/10), rate_func = linear)
        self.play(alpha.animate.set_value(11*PI/10), rate_func = linear)
        self.play(alpha.animate.set_value(13*PI/10), rate_func = linear)
        self.play(alpha.animate.set_value(15*PI/10), rate_func = linear)
        self.add(shade_2, notice5).play(alpha.animate.set_value(17*PI/10), FadeIn(shade), FadeIn(shade_2), rate_func = linear)
        path.clear_updaters()
        self.waiting(0, 12) #到此共90秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_3(Scene):
    def construct(self):
        notice5 = Notice("完善证明", "请　模仿")
        notice6 = Notice("证明完毕", "请　鼓掌")

        offset = 5*LEFT+2*DOWN
        function_1 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2)))
        function_2 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2))+(t**2/2*unit(t-PI)))
        curve = ParametricCurve(function_1, [0, PI, DEGREES], color = YELLOW, stroke_width = 6).shift(offset)
        curve_base = curve.copy().set_stroke(color = GREY, width = 4).set_fill(color = BACK, opacity = 1)
        involute = ParametricCurve(function_2, [0, PI, DEGREES], color = BLUE, stroke_width = 6).shift(offset)
        
        start = Dot(color = GREY).shift(offset + function_1(0))
        point = Dot(color = RED).shift(offset + function_1(2*PI/3))
        direction = Arrow(offset + function_1(2*PI/3), offset + function_1(2*PI/3) + unit(2*PI/3), buff = 0, color = RED)
        start_direction = Arrow(offset+1.5*RIGHT, offset+2.5*RIGHT, buff = 0, color = GREY)
        group_start = VGroup(start, start_direction)
        group_point = VGroup(point, direction)
        fixed_start = group_start.copy().shift(2*UL+0.5*DOWN)
        fixed_direction = group_point.copy().shift(function_1(0) - function_1(2*PI/3) + 2*UL+0.5*DOWN).rotate(-2*PI/3, about_point = 5.5*LEFT + 0.5*DOWN).save_state()
        angle_notation = Arc(radius = 0.2, angle = 2*PI/3, color = YELLOW).shift(offset + 1.5*UP + 0.5*LEFT)
        angle_theta = MTex(r"\theta", color = YELLOW).scale(0.6).shift(offset + 1.5*UP + 0.5*LEFT).save_state().shift(0.4*unit(PI/3))
        text_func = MTex(r"s(\theta)", tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW}).shift(4*LEFT + 3*UP)
        part_curve = ParametricCurve(function_1, [0, 2*PI/3, DEGREES], color = ORANGE, stroke_width = 6).shift(offset)
        text_length = MTex(r"s", color = ORANGE).scale(0.6).next_to(offset + function_1(PI/2), RIGHT)
        
        alpha = ValueTracker(2*PI/3)
        def point_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(function_1(angle) + offset)
        def direction_updater(mob: Arrow):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_1(angle) + offset, function_1(angle) + offset + unit(angle))
        def part_updater(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(function_1, [0, angle, DEGREES]).shift(offset)
            mob.set_points(curve.get_all_points())
        def fixed_updater(mob: VGroup):
            angle = alpha.get_value()
            mob.restore().rotate(angle, about_point = 5.5*LEFT + 0.5*DOWN)
        def arc_updater(mob: Arc):
            angle = alpha.get_value()
            trace = Arc(radius = 0.2, angle = angle, color = YELLOW).shift(offset + 1.5*UP + 0.5*LEFT)
            mob.become(trace)
        def theta_updater(mob: MTex):
            angle = alpha.get_value()
            ratio = clip(angle/(PI/2), 0, 1)
            mob.restore().shift(0.4*unit(angle/2)).scale(ratio)
        self.add(angle_notation, angle_theta, fixed_start, fixed_direction, curve, part_curve, text_length, group_start, group_point, text_func, notice5)
        point.add_updater(point_updater)
        direction.add_updater(direction_updater)
        part_curve.add_updater(part_updater)
        fixed_direction.add_updater(fixed_updater)
        angle_notation.add_updater(arc_updater)
        angle_theta.add_updater(theta_updater)
        self.play(ApplyMethod(alpha.set_value, 0, run_time = 2), FadeOut(text_length))
        part_curve.clear_updaters()
        self.waiting(1, 10) #这种表达式乍一看会让人很摸不着头脑
        self.remove(part_curve).add(curve_base)

        def curve_updater(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(lambda t: function_1(PI-t), [0, PI - angle, DEGREES]).shift(offset)
            mob.set_points(curve.get_all_points())
        curve.add_updater(curve_updater)
        line = Line(color = ORANGE, stroke_width = 6)
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(function_1(value), function_2(value)).shift(offset)
        line.add_updater(line_updater)
        def involute_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_2, [0, value, DEGREES]).shift(offset)
            mob.set_points(curve.get_all_points())
        involute.add_updater(involute_updater)
        self.bring_to_back(curve_base).add(curve, line, involute, group_start, group_point).play(alpha.animate.set_value(2*PI/3), run_time = 2)
        self.waiting(0, 8) #但它和渐开线特别搭
        self.waiting(2, 15) #可以很方便地求出渐开线的长度
        self.waiting(0, 18) #（空闲）

        line_base = line.copy().set_stroke(color = interpolate_color(GREY, ORANGE, 0.5), width = 4).clear_updaters()
        self.bring_to_back(line_base).play(alpha.animate.set_value(5*PI/6), run_time = 2)
        for mob in [curve, point, direction, fixed_direction, angle_notation, angle_theta, line]:
            mob.clear_updaters()
        self.waiting(0, 7) #在多展开一个小角度的时候
        sector = Line(function_1(5*PI/6), function_2(5*PI/6)).append_points(
            ParametricCurve(function_2, [2*PI/3, 5*PI/6, DEGREES]).reverse_points().get_all_points()
            ).add_line_to(function_1(2*PI/3)).append_points(ParametricCurve(function_1, [2*PI/3, 5*PI/6, DEGREES]).get_all_points()
            ).shift(offset).set_stroke(width = 0).set_fill(color = interpolate_color(GREY, ORANGE, 0.5), opacity = 0.2)
        self.bring_to_back(sector).play(ShowCreation(sector))
        self.waiting(2, 7) #两条边夹成的区域可以近似看作扇形

        copy_func = text_func.copy().scale(0.7).move_to(offset + (2*function_1(5*PI/6) + 3*function_2(5*PI/6))/5 +0.4*unit(PI/3))
        dtheta = MTex(r"d\theta", color = YELLOW).scale(0.5).shift(offset + function_1(5*PI/6) + 0.9*unit(-PI/6) + 0.7*unit(-PI/4))
        arc = ArcBetweenPoints(offset + function_1(130*DEGREES), offset + function_1(5*PI/6) + 1.3*unit(-PI/6), angle = PI/6, color = YELLOW)
        s_dtheta = MTex(r"sd\theta", tex_to_color_map = {r"s": ORANGE, r"d\theta": YELLOW}).scale(0.8).move_to(offset + function_2(3*PI/4) + 0.5*unit(-PI/4))
        self.play(ReplacementTransform(text_func, copy_func))
        self.waiting(1, 21) #扇形的半径是已经展开的长度
        self.bring_to_back(sector, arc).play(ShowCreation(arc), Write(dtheta))
        self.waiting(1, 22) #而扇形的圆心角记为dθ
        self.play(Write(s_dtheta)) 
        self.waiting(2, 5) #于是 扇形的弧长就是sdθ
        self.waiting(0, 14) #（空闲）

        lines = [Line(offset + function_1(angle), offset + function_2(angle), color = interpolate_color(GREY, ORANGE, 0.5)) for angle in [PI/6, PI/3, PI/2, PI]]
        self.bring_to_back(*lines).play(LaggedStart(*[ShowCreation(line) for line in lines], group = VGroup(), run_time = 1.5), alpha.animate.set_value(PI))
        self.waiting(1.5, 10) #渐开线就是这样一小段一小段弧拼起来的

        involute_point = group_start.copy()
        beta = ValueTracker(0)
        def involute_point_updater(mob: VGroup):
            angle = beta.get_value()
            mob.restore().rotate(angle, about_point = offset + function_1(0)).shift(function_2(angle) - function_2(0))
        right_angle = Line(0.2*RIGHT, 0.2*UR).add_line_to(0.2*UP)
        right_angle_1 = right_angle.copy().rotate(PI/6, about_point = ORIGIN).shift(offset + function_2(2*PI/3))
        self.play(involute_point.animate.rotate(-PI/2, about_point = offset + function_1(0)).set_color(PURPLE))
        involute_point.save_state().add_updater(involute_point_updater)
        self.play(beta.animate.set_value(2*PI/3), rate_func = rush_from)
        self.bring_to_back(sector, right_angle_1).play(ShowCreation(right_angle_1))
        self.waiting(0, 12) #而且 渐开线总是垂直于原始曲线

        involute_point_copy = involute_point.copy().clear_updaters()
        right_angle_2 = right_angle.copy().rotate(PI/3, about_point = ORIGIN).shift(offset + function_2(5*PI/6))
        self.add(involute_point_copy).play(beta.animate.set_value(5*PI/6))
        self.bring_to_back(sector, right_angle_2).play(ShowCreation(right_angle_2))
        self.waiting(1, 1) #所以当原曲线多展开了dθ的时候
        self.waiting(2, 3) #渐开线也转过了dθ
        self.waiting(0, 13) #（空闲）

        involute_func = MTex(r"t(\theta)", tex_to_color_map = {r"t": BLUE, r"\theta": YELLOW}).next_to(offset + function_2(PI), UP)
        integral = MTex(r"dt&=sd\theta\\\Rightarrow t(\theta)&=\int s(\theta)\,d\theta", tex_to_color_map = {(r"dt", r"t"): BLUE, r"s": ORANGE, (r"\theta", r"d\theta"): YELLOW}).scale(0.8).shift(3*RIGHT)
        parts_integral = [integral[0:6], integral[6:]]
        self.play(Write(involute_func))
        self.waiting(2, 2) #如果设渐开线的奇怪表达式为t(θ)
        self.play(Write(parts_integral[0]))
        self.waiting(1, 12) #那么我们就能得到这么一个结论
        self.play(Write(parts_integral[1]))
        self.waiting(1, 7) #t(θ)是s(θ)的积分
        self.waiting(0, 15) #（空闲）

        self.waiting(2, 27) #这个性质可以被用在每条渐开线上
        shade = Rectangle(height = FRAME_HEIGHT, width = FRAME_WIDTH, fill_opacity = 1, fill_color = BACK, stroke_width = 0)
        self.add(shade, notice5).play(FadeIn(shade))
        self.remove(curve, curve_base, involute, point, direction, fixed_direction, angle_notation, angle_theta, line, *lines, line_base, sector, fixed_start, group_start, right_angle_1, right_angle_2, copy_func, dtheta, arc, s_dtheta, involute_point, involute_point_copy, involute_func, integral)

        offset = 2*DOWN+5*LEFT
        arrow_x = Arrow(0.8*LEFT, 4.8*RIGHT, buff = 0, stroke_width = 4).shift(offset)
        arrow_y = Arrow(0.8*DOWN, 5.2*UP, buff = 0, stroke_width = 4).shift(offset)
        arrows = VGroup(arrow_x, arrow_y)
        angle = 5/12*PI
        point = Dot(color = r"#EE0000", radius = 0.06).shift(4*unit(angle)).shift(offset)
        unit_vec = DashedLine(ORIGIN, 4*unit(angle), color = "#FFA7D7", stroke_width = 3).shift(offset)
        angle_alpha = MTex(r"\alpha", color = "#FFA7D7").scale(0.7).shift(0.4*unit(angle/2)).shift(offset)
        # function_0 = lambda t: 4*unit(angle-t)
        # function_1 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2)))
        # function_2 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI)))
        # function_3 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI))+(t**3/6*unit((angle-t)+PI*3/2)))
        # function_4 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI))+(t**3/6*unit((angle-t)+PI*3/2))+(t**4/24*unit(angle-t)))
        function_0 = lambda t: 4*unit(t)
        function_1 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2)))
        function_2 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI)))
        function_3 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2)))
        function_4 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2))+((angle-t)**4/24*unit(t)))
        involute_0 = ParametricCurve(function_0, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_1 = ParametricCurve(function_1, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_2 = ParametricCurve(function_2, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_3 = ParametricCurve(function_3, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_4 = ParametricCurve(function_4, [0, angle, DEGREES], color = ORANGE).shift(offset)
        point_0 = offset + 4*RIGHT
        point_1 = point_0 + 4*angle*UP
        point_2 = point_1 + 4*(angle)**2/2*LEFT
        point_3 = point_2 + 4*(angle)**3/6*DOWN
        point_4 = point_3 + 4*(angle)**4/24*RIGHT
        point_5 = point_4 + 4*(angle)**5/120*UP
        line_0 = Line(point_0, point_1, color = GREEN)
        line_1 = Line(point_1, point_2, color = BLUE)
        line_2 = Line(point_2, point_3, color = GREEN)
        line_3 = Line(point_3, point_4, color = BLUE)
        line_4 = Line(point_4, point_5, color = GREEN)
        text_0 = MTex(r"\frac{\alpha^0}{0!}", color = BLUE).scale(0.8).next_to(offset + 2*RIGHT, DOWN, buff = 0.1)
        text_1 = MTex(r"\frac{\alpha^1}{1!}", color = GREEN).scale(0.7).next_to(line_0, RIGHT, buff = 0.1)
        text_2 = MTex(r"\frac{\alpha^2}{2!}", color = BLUE).scale(0.6).next_to(line_1, UP, buff = 0.1)
        text_3 = MTex(r"\frac{\alpha^3}{3!}", color = GREEN).scale(0.5).next_to(line_2, LEFT, buff = 0.1)
        text_4 = MTex(r"\frac{\alpha^4}{4!}", color = BLUE).scale(0.4).next_to(line_3, DOWN, buff = 0.1)
        text_5 = MTex(r"\frac{\alpha^5}{5!}", color = GREEN).scale(0.3).next_to(line_4, RIGHT, buff = 0.1)
        involutes = VGroup(arrows, unit_vec, angle_alpha, involute_0, involute_1, involute_2, involute_3, involute_4, line_0, line_1, line_2, line_3, line_4)
        texts = VGroup(text_0, text_1, text_2, text_3, text_4, text_5)
        func_0 = MTex(r"\theta", color = ORANGE).scale(0.8).shift(offset + function_0(5*PI/24) - 0.3*unit(5*PI/24))
        func_1 = MTex(r"\frac{\theta^2}{2!}", color = YELLOW).scale(0.6).shift(offset + function_1(PI/6) - 0.4*unit(PI/6 + PI/2))
        func_2 = MTex(r"\frac{\theta^3}{3!}", color = ORANGE).scale(0.4).shift(offset + function_2(PI/10) - 0.2*unit(PI/10 + PI))
        func_3 = MTex(r"\frac{\theta^4}{4!}", color = YELLOW).scale(0.25).shift(offset + function_3(PI/20) - 0.2*unit(PI/20 + 3*PI/2))
        func_4 = MTex(r"\frac{\theta^5}{5!}", color = ORANGE).scale(0.05).shift(offset + function_4(PI/30) - 0.05*unit(PI/30))
        funcs = VGroup(func_0, func_1, func_2, func_3, func_4)
        equivalence = MTexText(r"渐开线$\Leftrightarrow$积分", tex_to_color_map = {r"渐开线": BLUE, r"积分": YELLOW}).next_to(3*UP, RIGHT)
        self.add(involutes, point, func_0, equivalence, shade, notice5).play(FadeOut(shade))
        self.waiting(2, 6) #也就是说 每条渐开线都是原来曲线的积分
        self.play(Write(func_1))
        self.waiting(1, 23) #θ积一次分是θ^2/2
        self.play(Write(func_2))
        self.waiting(2, 10) #再积一次分是θ^3/3!
        self.play(Write(func_3))
        self.waiting(0, 19) #依次这么积下去
        self.play(Write(func_4))
        self.waiting(1, 8) #我们就能得到每条曲线的表达式了
        self.waiting(0, 14) #（空闲）

        self.waiting(1, 20) #而它们各自的长度
        self.play(LaggedStart(FadeIn(text_0), TransformFromCopy(func_0, text_1), TransformFromCopy(func_1, text_2), TransformFromCopy(func_2, text_3), TransformFromCopy(func_3, text_4), TransformFromCopy(func_4, text_5), lag_ratio = 0.5), run_time = 3)
        self.waiting(0, 29) #就是把θ=α代进表达式中 得到的结果
        self.waiting(0, 19) #（空闲）

        mtex_sin = MTex(r"\sin\alpha=\frac{\alpha^1}{1!}-\frac{\alpha^3}{3!}+\frac{\alpha^5}{5!}-\cdots", color = GREEN, tex_to_color_map = {(r"=", r"+", r"-"): WHITE}).scale(0.8).next_to(1.5*UP+0.5*RIGHT)
        mtex_cos = MTex(r"\cos\alpha=\frac{\alpha^0}{0!}-\frac{\alpha^2}{2!}+\frac{\alpha^4}{4!}-\cdots", color = BLUE, tex_to_color_map = {(r"=", r"+", r"-"): WHITE}).scale(0.8).next_to(0.5*DOWN+0.5*RIGHT)
        
        self.play(Write(mtex_sin), Write(mtex_cos))
        self.waiting(0, 21) #再把螺旋的横纵坐标分别加起来
        self.play(ReplacementTransform(notice5, notice6))
        self.waiting(2, 13) #就能得到正弦函数和余弦函数的展开式了
        self.waiting(2, 5) #这就是全部的证明过程
        self.waiting(1, 4) #到此共77秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_4(Scene):
    def construct(self):
        notice6 = Notice("证明完毕", "请　鼓掌")
        notice7 = Notice("下节预告", "敬请期待")

        offset = 2*DOWN+5*LEFT
        arrow_x = Arrow(0.8*LEFT, 4.8*RIGHT, buff = 0, stroke_width = 4).shift(offset)
        arrow_y = Arrow(0.8*DOWN, 5.2*UP, buff = 0, stroke_width = 4).shift(offset)
        arrows = VGroup(arrow_x, arrow_y)
        angle = 5/12*PI
        point = Dot(color = r"#EE0000", radius = 0.06).shift(4*unit(angle)).shift(offset)
        unit_vec = DashedLine(ORIGIN, 4*unit(angle), color = "#FFA7D7", stroke_width = 3).shift(offset)
        angle_alpha = MTex(r"\alpha", color = "#FFA7D7").scale(0.7).shift(0.4*unit(angle/2)).shift(offset)
        function_0 = lambda t: 4*unit(t)
        function_1 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2)))
        function_2 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI)))
        function_3 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2)))
        function_4 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2))+((angle-t)**4/24*unit(t)))
        involute_0 = ParametricCurve(function_0, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_1 = ParametricCurve(function_1, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_2 = ParametricCurve(function_2, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_3 = ParametricCurve(function_3, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_4 = ParametricCurve(function_4, [0, angle, DEGREES], color = ORANGE).shift(offset)
        point_0 = offset + 4*RIGHT
        point_1 = point_0 + 4*angle*UP
        point_2 = point_1 + 4*(angle)**2/2*LEFT
        point_3 = point_2 + 4*(angle)**3/6*DOWN
        point_4 = point_3 + 4*(angle)**4/24*RIGHT
        point_5 = point_4 + 4*(angle)**5/120*UP
        line_0 = Line(point_0, point_1, color = GREEN)
        line_1 = Line(point_1, point_2, color = BLUE)
        line_2 = Line(point_2, point_3, color = GREEN)
        line_3 = Line(point_3, point_4, color = BLUE)
        line_4 = Line(point_4, point_5, color = GREEN)
        text_0 = MTex(r"\frac{\alpha^0}{0!}", color = BLUE).scale(0.8).next_to(offset + 2*RIGHT, DOWN, buff = 0.1)
        text_1 = MTex(r"\frac{\alpha^1}{1!}", color = GREEN).scale(0.7).next_to(line_0, RIGHT, buff = 0.1)
        text_2 = MTex(r"\frac{\alpha^2}{2!}", color = BLUE).scale(0.6).next_to(line_1, UP, buff = 0.1)
        text_3 = MTex(r"\frac{\alpha^3}{3!}", color = GREEN).scale(0.5).next_to(line_2, LEFT, buff = 0.1)
        text_4 = MTex(r"\frac{\alpha^4}{4!}", color = BLUE).scale(0.4).next_to(line_3, DOWN, buff = 0.1)
        text_5 = MTex(r"\frac{\alpha^5}{5!}", color = GREEN).scale(0.3).next_to(line_4, RIGHT, buff = 0.1)
        involutes = VGroup(arrows, unit_vec, angle_alpha, involute_0, involute_1, involute_2, involute_3, involute_4, line_0, line_1, line_2, line_3, line_4)
        texts = VGroup(text_0, text_1, text_2, text_3, text_4, text_5)
        func_0 = MTex(r"\theta", color = ORANGE).scale(0.8).shift(offset + function_0(5*PI/24) - 0.3*unit(5*PI/24))
        func_1 = MTex(r"\frac{\theta^2}{2!}", color = YELLOW).scale(0.6).shift(offset + function_1(PI/6) - 0.4*unit(PI/6 + PI/2))
        func_2 = MTex(r"\frac{\theta^3}{3!}", color = ORANGE).scale(0.4).shift(offset + function_2(PI/10) - 0.2*unit(PI/10 + PI))
        func_3 = MTex(r"\frac{\theta^4}{4!}", color = YELLOW).scale(0.25).shift(offset + function_3(PI/20) - 0.2*unit(PI/20 + 3*PI/2))
        func_4 = MTex(r"\frac{\theta^5}{5!}", color = ORANGE).scale(0.05).shift(offset + function_4(PI/30) - 0.05*unit(PI/30))
        funcs = VGroup(func_0, func_1, func_2, func_3, func_4)

        mtex_sin = MTex(r"\sin\alpha=\frac{\alpha^1}{1!}-\frac{\alpha^3}{3!}+\frac{\alpha^5}{5!}-\cdots", color = GREEN, tex_to_color_map = {(r"=", r"+", r"-"): WHITE}).scale(0.8).next_to(1.5*UP+0.5*RIGHT)
        mtex_cos = MTex(r"\cos\alpha=\frac{\alpha^0}{0!}-\frac{\alpha^2}{2!}+\frac{\alpha^4}{4!}-\cdots", color = BLUE, tex_to_color_map = {(r"=", r"+", r"-"): WHITE}).scale(0.8).next_to(0.5*DOWN+0.5*RIGHT)
        equivalence = MTexText(r"渐开线$\Leftrightarrow$积分", tex_to_color_map = {r"渐开线": BLUE, r"积分": YELLOW}).next_to(3*UP, RIGHT)
        
        self.add(involutes, point, texts, funcs, mtex_sin, mtex_cos, equivalence, notice6)
        self.waiting(2, 10) #这方法真的很神奇 对吧
        self.waiting(0, 19) #（空闲）

        self.waiting(1, 25) #无论你是不是第一次看
        self.waiting(1, 24) #大概都会这么觉得吧
        self.waiting(0, 17) #（空闲）

        self.play(ReplacementTransform(notice6, notice7))
        self.waiting(2, 7) #但我相信一定有一部分观众想问问“为什么”
        self.waiting(0, 21) #（空闲）
        exp = MTex(r"e^\alpha=\frac{\alpha^0}{0!}+\frac{\alpha^1}{1!}+\frac{\alpha^2}{2!}+\cdots", color = TEAL, tex_to_color_map = {(r"=", r"+", r"-"): WHITE}).scale(0.8)
        offset = mtex_sin[4].get_center() - exp[2].get_center()
        exp.shift(offset + DOWN)
        self.play(Write(exp))
        question = MTex(r"?", color = TEAL).next_to(0.5*UP+0.5*RIGHT, LEFT, buff = 0)
        self.play(Write(question))
        self.waiting(0, 29) #可能有人在好奇这个方法能不能推广到别的泰勒展开
        self.waiting(1, 27) #比如e的x次方
        self.waiting(3, 13) #还有人对这个方法的严谨性有一定要求
        self.waiting(2, 26) #但我打算把这些话题放到第三节再说
        self.waiting(0, 19) #（空闲）

        shade = Rectangle(height = FRAME_HEIGHT, width = FRAME_WIDTH, fill_opacity = 1, fill_color = BACK, stroke_width = 0)
        self.add(shade, notice6).play(FadeIn(shade))
        self.remove(involutes, point, texts, funcs, mtex_sin, mtex_cos, equivalence, exp, question)

        function_1 = lambda t: np.array([2*t + np.sin(2*t), 1 - np.cos(2*t), 0])
        function_2 = lambda t: np.array([2*t - np.sin(2*t), np.cos(2*t) - 1, 0])
        cycloid = ParametricCurve(function_1, [0, PI, PI/100], color = YELLOW).shift(PI*LEFT)
        involute = ParametricCurve(function_2, [0, PI, PI/100], color = RED).shift(PI*LEFT)
        point = Dot(color = RED).shift(PI*LEFT)
        line = Line(PI/2*LEFT, PI/2*LEFT, color = [YELLOW, RED]).shift(0.5*UP)
        alpha = ValueTracker(PI/2)
        def line_updater(mob: Line):
            value = alpha.get_value()
            start = function_1(value) + PI*LEFT
            end = function_2(value) + PI*LEFT
            mob.put_start_and_end_on(start, end)
        def point_updater(mob: Dot):
            value = alpha.get_value()
            position = function_2(value) + PI*LEFT
            mob.move_to(position)
        point.add_updater(point_updater)
        line.add_updater(line_updater)
        self.add(cycloid, involute, line, point, shade, notice6).play(ApplyMethod(alpha.set_value, 0, rate_func = linear), FadeOut(shade))
        self.play(alpha.animate.set_value(PI), rate_func = linear, run_time = 2)
        self.play(alpha.animate.set_value(0), rate_func = linear, run_time = 2)
        self.play(alpha.animate.set_value(PI), rate_func = linear, run_time = 2)
        self.play(FadeIn(shade), ApplyMethod(alpha.set_value, PI/2, rate_func = linear))
        self.waiting(2, 3) #到此共35秒
        

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

####################################################################  

class Chapter2_0(Scene):

    def construct(self):

        text2 = Text("第二节 摆线与其它曲线", font = 'simsun', t2c={"第二节": YELLOW, "摆线": GREEN, "其它曲线": BLUE})

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(Scene):
    def construct(self):
        notice1 = Notice("上节回顾", "请　复习")
        notice2 = Notice("村规私设", "请勿模仿")
        notice3 = Notice("上节回顾", "请　复习")
        notice4 = Notice("简单例子", "请　欣赏")

        offset = 5*LEFT+2*DOWN
        function_1 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2)))
        function_2 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2))+(t**2/2*unit(t-PI)))
        curve = ParametricCurve(function_1, [0, PI, DEGREES], color = ORANGE, stroke_width = 6).shift(offset)
        curve_base = curve.copy().set_stroke(color = GREY, width = 4)
        text_func = MTex(r"s(\theta)", tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW}).shift(4*LEFT)
        involute = ParametricCurve(function_2, [0, PI, DEGREES], color = BLUE, stroke_width = 6).shift(offset)
        involute_func = MTex(r"t(\theta)&=\int s(\theta)\,d\theta", tex_to_color_map = {r"t": BLUE, r"s": ORANGE, (r"\theta", r"d\theta"): YELLOW}).scale(0.8).shift(2.2*RIGHT)

        title = Text(r"弧度方程", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        titele_line = Line(3*UP, 3*UP)
        
        self.play(Write(notice1), ShowCreation(curve))
        self.waiting(0, 20) #我们在第一节中
        self.play(Write(text_func))
        self.waiting(1, 16) #引入了这样一个表达式来表达曲线
        self.waiting(0, 16) #（空闲）

        self.waiting(2, 18) #它是长度关于旋转角度的函数
        self.waiting(0, 16) #（空闲）
        
        alpha = ValueTracker(0)
        def curve_updater(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(lambda t: function_1(PI-t), [0, PI - angle, DEGREES]).shift(offset)
            mob.set_points(curve.get_all_points())
        curve.add_updater(curve_updater)
        line = Line(color = ORANGE, stroke_width = 6)
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(function_1(value), function_2(value)).shift(offset)
        line.add_updater(line_updater)
        def involute_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_2, [0, value, DEGREES]).shift(offset)
            mob.set_points(curve.get_all_points())
        involute.add_updater(involute_updater)
        self.bring_to_back(curve_base).add(curve, line, involute).play(alpha.animate.set_value(PI), run_time = 2)
        for mob in []:
            mob.clear_updaters(curve, line, involute)
        self.waiting(0, 23) #这种表示算渐开线特别容易
        self.play(Write(involute_func))
        self.waiting(1, 28) #渐开线的表达式 是原来曲线的积分
        self.waiting(0, 13) #（空闲）
        
        self.play(ReplacementTransform(notice1, notice2))
        self.waiting(0, 14) #为了方便起见
        self.waiting(1, 16) #在之后的视频中
        self.play(Write(title), titele_line.animate.put_start_and_end_on(3*UP + 6*LEFT, 3*UP + 6*RIGHT))
        self.waiting(1, 12) #我会把它称为弧度方程
        self.waiting(2, 7) #对应的曲线称为弧度曲线
        self.waiting(0, 24) #（空闲）

        shade = Rectangle(height = FRAME_HEIGHT, width = FRAME_WIDTH, fill_opacity = 1, fill_color = BACK, stroke_width = 0)
        self.add(shade, title, titele_line, notice2).play(FadeIn(shade), ReplacementTransform(notice2, notice3))
        self.remove(curve, curve_base, text_func, involute, involute_func, line)

        offset = 2.5*DOWN+2*LEFT
        arrow_x = Arrow(0.5*LEFT, 4.8*RIGHT, buff = 0, stroke_width = 4).shift(offset)
        arrow_y = Arrow(0.5*DOWN, 5.2*UP, buff = 0, stroke_width = 4).shift(offset)
        arrows = VGroup(arrow_x, arrow_y)
        angle = 5/12*PI
        point = Dot(color = r"#EE0000", radius = 0.06).shift(4*unit(angle)).shift(offset)
        unit_vec = DashedLine(ORIGIN, 4*unit(angle), color = "#FFA7D7", stroke_width = 3).shift(offset)
        angle_alpha = MTex(r"\alpha", color = "#FFA7D7").scale(0.7).shift(0.4*unit(angle/2)).shift(offset)
        function_0 = lambda t: 4*unit(t)
        function_1 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2)))
        function_2 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI)))
        function_3 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2)))
        function_4 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2))+((angle-t)**4/24*unit(t)))
        involute_0 = ParametricCurve(function_0, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_1 = ParametricCurve(function_1, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_2 = ParametricCurve(function_2, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_3 = ParametricCurve(function_3, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_4 = ParametricCurve(function_4, [0, angle, DEGREES], color = ORANGE).shift(offset)
        point_0 = offset + 4*RIGHT
        point_1 = point_0 + 4*angle*UP
        point_2 = point_1 + 4*(angle)**2/2*LEFT
        point_3 = point_2 + 4*(angle)**3/6*DOWN
        point_4 = point_3 + 4*(angle)**4/24*RIGHT
        point_5 = point_4 + 4*(angle)**5/120*UP
        line_0 = Line(point_0, point_1, color = GREEN)
        line_1 = Line(point_1, point_2, color = BLUE)
        line_2 = Line(point_2, point_3, color = GREEN)
        line_3 = Line(point_3, point_4, color = BLUE)
        line_4 = Line(point_4, point_5, color = GREEN)
        involutes = VGroup(arrows, unit_vec, angle_alpha, involute_0, involute_1, involute_2, involute_3, involute_4, line_0, line_1, line_2, line_3, line_4)
        func_0 = MTex(r"\theta", color = ORANGE).scale(0.8).shift(offset + function_0(5*PI/24) - 0.3*unit(5*PI/24))
        func_1 = MTex(r"\frac{\theta^2}{2!}", color = YELLOW).scale(0.6).shift(offset + function_1(PI/6) - 0.4*unit(PI/6 + PI/2))
        func_2 = MTex(r"\frac{\theta^3}{3!}", color = ORANGE).scale(0.4).shift(offset + function_2(PI/10) - 0.2*unit(PI/10 + PI))
        func_3 = MTex(r"\frac{\theta^4}{4!}", color = YELLOW).scale(0.25).shift(offset + function_3(PI/20) - 0.2*unit(PI/20 + 3*PI/2))
        func_4 = MTex(r"\frac{\theta^5}{5!}", color = ORANGE).scale(0.05).shift(offset + function_4(PI/30) - 0.05*unit(PI/30))
        funcs = VGroup(func_0, func_1, func_2, func_3, func_4)
        self.add(involutes, point, funcs, shade, title, titele_line, notice3).play(FadeOut(shade))
        self.waiting(2, 14) #在第一节里 我们实际上已经见到了幂函数的弧度曲线
        self.waiting(0, 17) #（空闲）

        self.waiting(1, 29) #那别的函数的弧度曲线
        self.waiting(1, 11) #又会长什么样呢
        self.waiting(0, 17) #（空闲）

        self.waiting(2+0-1, 17+25)
        self.add(shade, title, titele_line, notice3).play(FadeIn(shade), ReplacementTransform(notice3, notice4)) #我们来找几个好积分的函数看看吧 （空闲）
        self.remove(shade, involutes, point, funcs)

        func = MTex(r"s(\theta)=\sin\theta", tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW, r"\sin": ORANGE}).next_to(3*UP, DOWN)

        offset_1 = TAU*LEFT + 2.5*DOWN
        function_1 = lambda t: np.array([2*t + np.sin(2*t), 1 - np.cos(2*t), 0])
        cycloid_0 = ParametricCurve(function_1, [0, PI/2, DEGREES], color = ORANGE).shift(offset_1)
        cycloid_1 = ParametricCurve(function_1, [PI/2, PI*3/2, DEGREES], color = PURPLE).shift(offset_1)
        cycloid_2 = ParametricCurve(function_1, [PI*3/2, PI*2, DEGREES], color = ORANGE).shift(offset_1)
        cycloid = VGroup(cycloid_0, cycloid_1, cycloid_2)
        
        offset_2 = UP
        arrow_x = Arrow(0.5*LEFT, 7*RIGHT, buff = 0, stroke_width = 3)
        arrow_y = Arrow(1.2*DOWN, 1.2*UP, buff = 0, stroke_width = 3)
        notation_x = MTex(r"\theta", color = YELLOW).scale(0.6).next_to(6.8*RIGHT, UP, buff = 0.1)
        notation_y = MTex(r"s", color = ORANGE).scale(0.6).next_to(1*UP, RIGHT, buff = 0.1)
        axes = VGroup(arrow_x, arrow_y, notation_x, notation_y).shift(offset_2)
        graph = FunctionGraph(np.sin, [0, TAU, DEGREES], color = BLUE).shift(offset_2)
        graph_point = Dot(color = YELLOW).shift(offset_2)

        start = Dot(color = GREY).shift(offset_1)
        point = Dot(color = RED).shift(offset_1)
        direction = Arrow(offset_1, offset_1 + RIGHT, buff = 0, color = RED)
        start_direction = Arrow(offset_1, offset_1 + RIGHT, buff = 0, color = GREY)
        group_start = VGroup(start, start_direction)
        group_point = VGroup(point, direction)
        fixed_start = group_start.copy().shift(3.5*UP + 2.5*RIGHT)
        fixed_direction = group_point.copy().shift(3.5*UP + 2.5*RIGHT).save_state()
        angle_notation = Arc(radius = 0.2, angle = 2*PI/3, color = YELLOW).shift(offset_1 + 3.5*UP + 2.5*RIGHT)
        angle_theta = MTex(r"\theta", color = YELLOW).scale(0.6).shift(offset_1 + 3.5*UP + 2.5*RIGHT).save_state()
        
        self.play(Write(func), FadeIn(axes), FadeIn(point, scale = np.infty))
        self.play(ShowCreation(graph), 
                  FadeIn(graph_point, scale = np.infty, rate_func = squish_rate_func(smooth, 0, 0.5)), FadeInFromPoint(direction, offset_1, rate_func = squish_rate_func(smooth, 0, 0.5)), 
                  TransformFromCopy(group_point, fixed_direction, rate_func = squish_rate_func(smooth, 0.5, 1)), 
                  run_time = 2)
        self.waiting(2+1-3, 3+14) #我们先来试试正弦函数 在画图过程中

        alpha = ValueTracker(0.0)
        def point_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(function_1(angle) + offset_1)
        point.add_updater(point_updater)
        def direction_updater(mob: Arrow):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_1(angle) + offset_1, function_1(angle) + offset_1 + unit(angle))
        direction.add_updater(direction_updater)
        def part_updater_0(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(function_1, [0, angle, DEGREES]).shift(offset_1)
            mob.set_points(curve.get_all_points())
        cycloid_0.add_updater(part_updater_0)
        def fixed_updater(mob: VGroup):
            angle = alpha.get_value()
            mob.restore().rotate(angle, about_point = offset_1 + 3.5*UP + 2.5*RIGHT)
        fixed_direction.add_updater(fixed_updater)
        def arc_updater(mob: Arc):
            angle = alpha.get_value()
            trace = Arc(radius = 0.2, angle = angle, color = YELLOW).shift(offset_1 + 3.5*UP + 2.5*RIGHT)
            mob.become(trace)
        angle_notation.add_updater(arc_updater)
        def theta_updater(mob: MTex):
            angle = alpha.get_value()
            ratio = clip(angle/(PI/4), 0, 1)
            mob.restore().shift(0.4*unit(angle/2)).scale(ratio)
        angle_theta.add_updater(theta_updater)
        def graph_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(np.array([angle, np.sin(angle), 0]) + offset_2)
        graph_point.add_updater(graph_updater)
        self.bring_to_back(angle_notation, angle_theta, fixed_start, cycloid_0).add(group_start, group_point).play(alpha.animate.set_value(PI/2), run_time = 4)
        cycloid_0.clear_updaters()
        self.waiting(3+1-4, 13+15) #从0到π/2的这一段不会出任何问题 一点一点画就是了
        self.waiting(0, 19) #（空闲）

        self.waiting(1, 21) #但从π/2之后
        decrease_graph = FunctionGraph(np.sin, [PI/2, 3*PI/2, DEGREES], color = YELLOW, stroke_width = 8).shift(offset_2)
        self.play(ShowPassingFlash(decrease_graph))
        self.play(ShowPassingFlash(decrease_graph))
        self.waiting(0, 7) #函数开始单调递减了
        self.waiting(2, 15) #这个时候就需要一条新的规则
        self.waiting(2, 15) #允许曲线长度是负的
        self.waiting(2, 17) #负值曲线朝向为反方向
        def part_updater_1(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(function_1, [PI/2, angle, DEGREES]).shift(offset_1)
            mob.set_points(curve.get_all_points())
        cycloid_1.add_updater(part_updater_1)
        self.bring_to_back(cycloid_1).play(alpha.animate.set_value(3*PI/2), run_time = 8)
        cycloid_1.clear_updaters()
        self.waiting(4+0+3+2-8, 0+19+7+26) #简单来说就是 我们可以在画曲线的时候倒车 （空闲） 从π/2一路倒车倒到3π/2 这时候曲线总长度都成-1了
        increase_graph = FunctionGraph(np.sin, [3*PI/2, TAU, DEGREES], color = YELLOW, stroke_width = 8).shift(offset_2)
        self.play(ShowPassingFlash(increase_graph))
        self.play(ShowPassingFlash(increase_graph))
        self.waiting(0, 28) #正弦函数终于重新开始单调递增了

        shade = Square(side_length = 2.5, fill_opacity = 1, fill_color = BACK, stroke_width = 0).shift(offset_1 + 3.5*UP + 2.5*RIGHT)
        def part_updater_2(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(function_1, [3*PI/2, angle, DEGREES]).shift(offset_1)
            mob.set_points(curve.get_all_points())
        cycloid_2.add_updater(part_updater_2)
        def graph_updater(mob: FunctionGraph):
            angle = alpha.get_value()
            curve = FunctionGraph(np.sin, [0, angle, DEGREES], color = BLUE).shift(offset_2)
            mob.set_points(curve.get_all_points())
        self.bring_to_back(cycloid_2).play(ApplyMethod(alpha.set_value, TAU, run_time = 3, rate_func = rush_into), FadeIn(shade, run_time = 3, rate_func = squish_rate_func(smooth, 2/3, 1)))
        graph.add_updater(graph_updater)
        self.remove(shade, fixed_direction, fixed_start, angle_notation, angle_theta).play(alpha.animate.set_value(5*PI/2), run_time = 3, rate_func = rush_from)
        self.waiting(2+0+2+2-6, 24+15+6+16) #于是倒车结束 我们接着正着走 （空闲） 接下来就是周期性的重复了 这条曲线会不断这么向右边延伸
        self.waiting(0, 16) #（空闲）
        
        for mob in [point, direction, graph_point, cycloid_2, graph]:
            mob.clear_updaters()
        self.play(FadeOut(axes, scale = np.array([1, 0, 0]), shift = 1.2*UP), FadeOut(graph, scale = np.array([1, 0, 0]), shift = 1.2*UP), cycloid.animate.shift(1.5*UP), FadeOut(group_start, 1.5*UP))
        self.waiting(1, 0) #最终我们得到了什么呢

        offset = TAU*LEFT + DOWN
        line = Line(8*LEFT + UP, 8*RIGHT + UP)
        circle = Circle(color = WHITE).shift(3*PI)
        point = Dot(color = YELLOW).shift(offset + function_1(-PI/2))
        cycloid_3 = ParametricCurve(function_1, [-PI/2, 0, DEGREES], color = ORANGE).shift(offset)
        
        alpha = ValueTracker(-PI/2)
        def point_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(offset + function_1(angle))
        point.add_updater(point_updater)
        def circle_updater(mob: Circle):
            angle = alpha.get_value()
            mob.move_to((2*angle-TAU) * RIGHT)
        circle.add_updater(circle_updater)
        def part_updater_3(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(function_1, [-PI/2, angle, DEGREES]).shift(offset)
            mob.set_points(curve.get_all_points())
            if angle >= 0:
                mob.clear_updaters()
        cycloid_3.add_updater(part_updater_3)
        self.bring_to_back(line).add(cycloid_3, circle, point).play(ShowCreation(line), ApplyMethod(alpha.set_value, 5*PI/2, rate_func = linear, run_time = 6))
        self.waiting(0, 11) #到此共85+1秒
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_2(Scene):
    def construct(self):
        notice4 = Notice("简单例子", "请　欣赏")
        notice5 = Notice("摆线性质", "请　欣赏")
        notice6 = Notice("旋轮线族", "请　欣赏")

        title = Text(r"弧度方程", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        titele_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        func = MTex(r"s(\theta)=\sin\theta", tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW, r"\sin": ORANGE}).next_to(3*UP, DOWN)

        offset = TAU*LEFT + DOWN
        line = Line(8*LEFT + UP, 8*RIGHT + UP)
        function_1 = lambda t: np.array([2*t + np.sin(2*t), 1 - np.cos(2*t), 0])
        function_2 = lambda t: np.array([2*t - np.sin(2*t), np.cos(2*t) - 1, 0])
        cycloid_0 = ParametricCurve(function_1, [-PI/2, PI/2, DEGREES], color = ORANGE).shift(offset)
        cycloid_1 = ParametricCurve(function_1, [PI/2, PI*3/2, DEGREES], color = PURPLE).shift(offset)
        cycloid_2 = ParametricCurve(function_1, [PI*3/2, 5*PI/2, DEGREES], color = ORANGE).shift(offset)
        cycloid = VGroup(line, cycloid_0, cycloid_1, cycloid_2)

        cycloid_part = ParametricCurve(function_1, [PI/2, PI*7/6, DEGREES], color = PURPLE).shift(offset)
        start = 1.5*(function_1(PI/2) + offset) + PI/2*RIGHT
        end = 1.5*(function_1(PI*7/6) + offset) + PI/2*RIGHT
        point_a = Dot(color = YELLOW).shift(start)
        point_b = Dot(color = YELLOW).shift(end)

        self.add(title, titele_line, func, line, cycloid, cycloid_part, notice4)
        self.waiting(1, 25) #摆线也算是各大科普视频里的常客了
        self.waiting(0, 15) #（空闲）

        self.play(ReplacementTransform(notice4, notice5))
        self.waiting(1, 19) #它有很多大家耳熟能详的性质
        self.play(FadeOut(cycloid, shift = PI/2*RIGHT, scale = 1.5), cycloid_part.animate.scale(1.5, about_point = ORIGIN).shift(PI/2*RIGHT))
        
        angle = np.arctan2(end[1]-start[1], end[0]-start[0])
        trace_1 = Line(start, end, color = GREEN)
        radius = - get_norm(end - start)/(2*np.sin(angle))
        center = end + radius*UP
        trace_2 = ArcBetweenPoints(start, end, angle = -2*angle, color = BLUE)
        height = start[1] - end[1]
        trace_3 = Line(start, np.array([start[0], end[1] + 0.1, 0]), color = RED).append_points(
            [np.array([start[0], end[1] + 0.1, 0]), np.array([start[0], end[1], 0]), np.array([start[0] + 0.1, end[1], 0])]
            ).add_line_to(end).insert_n_curves(20)
        
        self.bring_to_back(trace_1, trace_2, trace_3).play(*[ShowCreation(mob) for mob in [trace_1, trace_2, trace_3, point_a, point_b]])
        self.waiting(1, 0)

        alpha = ValueTracker(PI/2)
        run_time = 3
        v = 2*np.sqrt(2*1.5) * (2*PI/3) / run_time
        def point_0_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(1.5*(function_1(angle) + offset) + PI/2*RIGHT)
        point_0 = point_a.copy().add_updater(point_0_updater)
        def point_1_updater(mob: Dot, dt):
            y = max(start[1] - mob.get_center()[1], 0.01)
            mob.shift(dt*v*np.sqrt(y)*unit(angle))
            if mob.get_center()[0] >= end[0]:
                mob.move_to(end).clear_updaters()
        point_1 = point_a.copy().add_updater(point_1_updater)
        def point_2_updater(mob: Dot, dt):
            y = max(start[1] - mob.get_center()[1], 0.01)
            dtheta = dt*v*np.sqrt(y)/radius
            mob.rotate(dtheta, about_point = center)
            if mob.get_center()[0] >= end[0]:
                mob.move_to(end).clear_updaters()
        point_2 = point_a.copy().add_updater(point_2_updater)
        def point_3_updater(mob: Dot, dt):
            y = max(start[1] - mob.get_center()[1], 0.01)
            if y < height:
                mob.shift(dt*v*np.sqrt(y)*DOWN)
                if mob.get_center()[1] <= end[1]:
                    mob.set_y(end[1])
            else:
                mob.shift(dt*v*np.sqrt(height)*RIGHT)
            if mob.get_center()[0] >= end[0]:
                mob.move_to(end).clear_updaters()
        point_3 = point_a.copy().add_updater(point_3_updater)
        self.add(point_0, point_1, point_2, point_3).play(alpha.animate.set_value(PI*7/6), rate_func = linear, run_time = run_time)
        self.wait(2)
        self.remove(alpha, point_0, point_1, point_2, point_3)
        self.waiting(0, 28) #比如它是最速降线

        cycloid = VGroup(line, cycloid_0.shift(PI*RIGHT), cycloid_1.shift(PI*RIGHT))
        for mob in [point_a, point_b, trace_1, trace_2, trace_3]:
            mob.generate_target()
            mob.target.shift(PI/2*RIGHT).scale(2/3, about_point = PI*RIGHT).set_color(BACK)
        self.play(FadeIn(cycloid, shift = PI*RIGHT, scale = 2/3), cycloid_part.animate.shift(PI/2*RIGHT).scale(2/3, about_point = PI*RIGHT), *[MoveToTarget(mob, remover = True) for mob in [point_a, point_b, trace_1, trace_2, trace_3]])
        self.remove(cycloid_part)
        self.waiting(0, 19) #又或者它是等时摆
        self.waiting(0, 17) #（空闲）

        offset = PI*LEFT + DOWN
        arch = ParametricCurve(function_1, [0, PI, DEGREES], color = YELLOW).shift(offset)
        alpha = ValueTracker(0.0)
        def arch_updater(mob: ParametricCurve):
            ratio = alpha.get_value()
            curve = ParametricCurve(function_1, [0, ratio*PI, DEGREES]).shift(offset + ratio*0.5*UP)
            mob.set_points(curve.get_all_points())
        arch.add_updater(arch_updater)
        self.add(arch).play(alpha.animate.set_value(1.0), FadeOut(cycloid, 0.5*UP))
        arch.clear_updaters()
        self.waiting(1, 12) #如果我们准备两个摆线形的拱

        line = Line(1.5*UP, 2.5*DOWN, color = [YELLOW, RED])
        point = Dot(color = RED).shift(2.5*DOWN)
        self.play(ShowCreation(line))
        self.play(ShowCreation(point))
        self.waiting(0, 7) #再在中间挂一个摆锤

        offset = PI*LEFT + 0.5*DOWN
        alpha = ValueTracker(PI/2)
        beta = ValueTracker(0.0)
        def left_line_updater(mob: Line):
            angle = alpha.get_value()
            move = beta.get_value()
            start = function_1(angle) + offset + move*LEFT
            end = function_2(angle) + offset + move*LEFT
            mob.put_start_and_end_on(start, end)
        def left_point_updater(mob: Dot):
            angle = alpha.get_value()
            move = beta.get_value()
            position = function_2(angle) + offset + move*LEFT
            mob.move_to(position)
        def right_line_updater(mob: Line):
            angle = np.arccos(np.cos(alpha.get_value())/2)
            move = beta.get_value()
            start = function_1(angle) + offset + move*RIGHT
            end = function_2(angle) + offset + move*RIGHT
            mob.put_start_and_end_on(start, end)
        def right_point_updater(mob: Dot):
            angle = np.arccos(np.cos(alpha.get_value())/2)
            move = beta.get_value()
            position = function_2(angle) + offset + move*RIGHT
            mob.move_to(position)
        
        arch_r = arch.copy()
        line_r = line.copy().add_updater(right_line_updater)
        point_r = point.copy().add_updater(right_point_updater)
        line.add_updater(left_line_updater)
        point.add_updater(left_point_updater)
        self.add(arch_r, line_r, point_r).play(arch.animate.shift(3.5*LEFT), arch_r.animate.shift(3.5*RIGHT), alpha.animate.set_value(PI), beta.animate.set_value(3.5), run_time = 2)
        def alpha_updater(mob: ValueTracker):
            time = (self.time - (20 + 22/30) + 0.6)%4 #这里的+0.6是视频渲染中self.time计时异常的bug的补正，对齐零点22.133秒
            if time > 2:
                time = 4 - time
            mob.set_value(time * PI/2)
        alpha.add_updater(alpha_updater)
        self.waiting(0, 3) #那么当摆锤振动的时候
        
        period = MTex(r"T=2\pi\sqrt{\frac{4R}{g}}", tex_to_color_map = {r"T": TEAL, r"4R": BLUE, r"g": ORANGE}).scale(0.6).next_to(3*UP + 3.5*RIGHT, DOWN)
        self.play(Write(period))
        self.waiting(0, 23) #它的周期和振幅无关
        self.waiting(0, 16) #（空闲）

        gamma = ValueTracker(0.0)
        def right_lines_updater(ratio: float):
            def util(mob: Line):
                angle = np.arccos(np.cos(alpha.get_value())*ratio)
                move = beta.get_value()
                start = function_1(angle) + offset + move*RIGHT
                end = function_2(angle) + offset + move*RIGHT
                mob.put_start_and_end_on(start, end).set_opacity(gamma.get_value())
            return util
        def right_points_updater(ratio: float):
            def util(mob: Dot):
                angle = np.arccos(np.cos(alpha.get_value())*ratio)
                move = beta.get_value()
                position = function_2(angle) + offset + move*RIGHT
                mob.move_to(position).set_opacity(gamma.get_value())
            return util
        mobs = []
        colors = [GREEN, BLUE, PURPLE, RED, ORANGE, YELLOW]
        for i in [1, 2, 4, 5]:
            line_i = Line(color = [YELLOW, colors[i]]).add_updater(right_lines_updater(i/6))
            point_i = Dot(color = colors[i]).add_updater(right_points_updater(i/6))
            mobs.append(line_i)
            mobs.append(point_i)
        self.waiting(2, 13) #这不是单摆那种小角度近似
        self.add(*mobs, line_r, point_r).play(gamma.animate.set_value(1.0))
        self.waiting(0, 22) #而是严格成立的性质
        self.waiting(0, 15) #（空闲）

        involute = ParametricCurve(function_2, [0, PI, DEGREES], color = RED).shift(offset + 3.5*RIGHT)
        self.waiting(0, 28) #并且......
        self.bring_to_back(involute).play(FadeIn(involute))
        self.waiting(1, 18) #......摆锤的运动轨迹同样是一条摆线
        self.waiting(0, 17) #（空闲）

        parameter_func = MTex(r"\begin{cases}x=R(\phi + \sin\phi)\\y=R(1 - \cos\phi)\end{cases}", tex_to_color_map = {(r"x",r"y"): GREEN, r"R": BLUE, r"\phi": YELLOW}).scale(0.8).next_to(func, DOWN)
        self.play(Write(parameter_func))
        self.waiting(0, 17) #这个性质要是用参数方程硬算
        self.waiting(1, 17) #那计算量就太大了
        self.waiting(0, 16) #（空闲）

        self.play(SwallowIn(parameter_func))
        self.waiting(1, 0) #既然我们有弧度方程这个趁手的工具
        self.waiting(1, 21) #不妨拿它来试一试
        self.waiting(0, 19) #（空闲）

        self.waiting(1, 13) #这里是卡alpha的归零
        def involute_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_2, [0, value, DEGREES]).shift(offset + 3.5*LEFT)
            mob.set_points(curve.get_all_points())
        involute_left = ParametricCurve(function_2, [0, PI, DEGREES], color = RED).shift(offset + 3.5*LEFT).add_updater(involute_updater)
        self.bring_to_back(involute_left).waiting(2, 0)
        involute_left.clear_updaters().become(ParametricCurve(function_2, [0, PI, DEGREES], color = RED).shift(offset + 3.5*LEFT))
        self.waiting(0, 12) #等时摆摆动的时候 摆锤会画出摆线的渐开线
        self.waiting(0, 15) #（空闲）

        self.waiting(2, 16) #既然摆线的弧度方程是sinθ
        texts = r"t(\theta)=\int s(\theta)\,d\theta=-\cos\theta", r"=\sin(\theta - \frac{\pi}{2})"
        involute_func = MTex(texts[0] + texts[1], isolate = texts, tex_to_color_map = {(r"t", r"\cos", r"\sin"): RED, r"s": ORANGE, (r"\theta", r"d", r"\frac{\pi}{2}"): YELLOW}).scale(0.6).shift(1.5*UP)
        parts_involute_func = [involute_func.get_part_by_tex(text) for text in texts]
        self.play(Write(parts_involute_func[0]))
        self.waiting(0, 22) #渐开线的弧度方程就是-cosθ
        self.waiting(0, 15) #（空闲）

        self.play(Write(parts_involute_func[1]))
        self.waiting(2, 13) #这无非又是一条从θ=-π/2开始的摆线
        self.waiting(0, 19) #（空闲）

        self.waiting(3, 3) #如果我们求一下弧长关于时间的方程
        harmonic = MTex(r"\ddot{t}+\frac{g}{4R}t=0", tex_to_color_map = {r"t": RED, r"g": ORANGE, r"4R": BLUE}).scale(0.8).shift(0.6*UP)
        self.play(Write(harmonic))
        self.waiting(1, 0) #就能发现它就是简谐振动
        self.waiting(0, 20) #（空闲）

        self.waiting(2, 26) #用弧度方程来证明 就是这么简单
        self.waiting(2, 9-2) #到此共63（+7-1）秒, 扣除浮点误差2帧

        shade = Rectangle(height = 5, width = FRAME_WIDTH, fill_opacity = 1, fill_color = BACK, stroke_width = 0).shift(0.5*DOWN)
        self.add(shade, harmonic, involute_func, period).play(FadeIn(shade), FadeOut(harmonic), FadeOut(involute_func), FadeOut(period), ReplacementTransform(notice5, notice6))
        
        print(self.num_plays, self.time - 6)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_3(Scene):
    def construct(self):
        notice6 = Notice("旋轮线族", "请　欣赏")

        title = Text(r"弧度方程", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        texts = r"s(\theta)=\sin", r"{\theta}"
        func = MTex(r"s(\theta)=\sin{\theta}", isolate = texts, tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW, r"\sin": ORANGE}).next_to(3*UP, DOWN)
        parts_func = [func.get_part_by_tex(text) for text in texts]
        self.add(notice6, title, title_line, func)
        self.waiting(2, 1) #当然 正弦函数不止能画出摆线来
        self.waiting(0, 18) #（空闲）

        texts = r"s(\theta)=\sin", r"(a\theta)"
        general_func = MTex(r"s(\theta)=\sin(a\theta)", isolate = texts, tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW, r"\sin": ORANGE, r"a": TEAL}).next_to(3*UP, DOWN)
        parts_general_func = [general_func.get_part_by_tex(text) for text in texts]
        cycloid_out = RadCurve(lambda t: 1.5*np.sin(t), [0, 2*TAU, TAU/1000], color = YELLOW)
        cycloid_in = cycloid_out.copy().apply_function(lambda t: np.array([-t[0], t[1], 0]))

        self.play(Transform(parts_func[0], parts_general_func[0]), Transform(parts_func[1], parts_general_func[1]), ShowCreation(cycloid_out, run_time = 2), ShowCreation(cycloid_in, run_time = 2))
        self.waiting(0, 15) #我们只要改变θ变换的速率

        list_out = [YELLOW, ORANGE, RED, PURPLE_A]
        mu_out = ValueTracker(0.0)
        def out_updater(mob: RadCurve):
            value = mu_out.get_value()
            k = 1 + 1/(2*max(value, 0.2))
            alpha = 1/(1+2*value)
            curve = RadCurve(lambda t: 1.5*np.sin(alpha*t), [0, k*PI, k*TAU/1000])
            curve_left = curve.copy().apply_function(lambda t: np.array([-t[0], t[1], 0])).reverse_points().append_points(curve.get_points())
            mob.set_points(curve_left.get_points()).set_color(ratio_color(list_out, value))
        cycloid_out.add_updater(out_updater)
        list_in = [YELLOW, GREEN, TEAL, BLUE]
        mu_in = ValueTracker(0.0)
        def in_updater(mob: RadCurve):
            value = mu_in.get_value()
            k = -(1 + 1/(2*min(value, -0.1)))
            if value == -0.5:
                alpha = 0
            else:
                alpha = 1/(1+2*value)
            curve = RadCurve(lambda t: 1.5*np.sin(alpha*t), [0, k*PI, k*TAU/1000])
            curve_left = curve.copy().apply_function(lambda t: np.array([-t[0], t[1], 0])).reverse_points().append_points(curve.get_points())
            mob.set_points(curve_left.get_points()).set_color(ratio_color(list_in, -3*value))
        cycloid_in.add_updater(in_updater)

        shade_up = Rectangle(height = 1.9, width = FRAME_WIDTH, fill_opacity = 1, fill_color = BACK, stroke_width = 0).next_to(4*UP, DOWN, buff = 0)
        shade_down = Rectangle(height = 1, width = FRAME_WIDTH, fill_opacity = 1, fill_color = BACK, stroke_width = 0).next_to(4*DOWN, UP, buff = 0)
        shade = VGroup(shade_up, shade_down)
        self.bring_to_back(cycloid_in, cycloid_out, shade).play(mu_out.animate.set_value(1.0), mu_in.animate.set_value(-1/3), run_time = 3)
        cycloid_out.clear_updaters()
        cycloid_in.clear_updaters()
        cycloid_out.become(RadCurve(lambda t: 1.5*np.sin(t/3), [0, 3*PI, DEGREES], color = PURPLE_A))
        cycloid_in.become(RadCurve(lambda t: 1.5*np.sin(3*t), [0, PI, DEGREES], color = BLUE))
        
        self.waiting(2+0-3, 29+18) #就能把所有的外摆线和内摆线都画出来 （空闲）

        start = Dot(color = GREY)
        start_direction = Arrow(ORIGIN, RIGHT, buff = 0, color = GREY)
        group_start = VGroup(start, start_direction)
        texts = r"s(\theta)=\sin(", r"{a}", r"{\theta})"
        general_func.become(MTex(r"s(\theta)=\sin({a}{\theta})", isolate = texts, tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW, r"\sin": ORANGE, r"{a}": TEAL}).next_to(3*UP, DOWN))
        parts_general_func = [general_func[0:9], general_func[9], general_func[10:]] #.get_part_by_tex(texts[1]) 和 .get_part_by_tex(texts[2]) 会报错

        offset_l = 2*DOWN + 3.5*LEFT
        function_l_1 = lambda t: np.array([np.sin(4*t/3)/4+np.sin(2*t/3)/2, 3/4-np.cos(4*t/3)/4-np.cos(2*t/3)/2, 0]) #s(\theta)=2sin(\theta/3)
        function_l_2 = lambda t: np.array([-3*np.sin(4*t/3)/4+3*np.sin(2*t/3)/2, 3/4+3*np.cos(4*t/3)/4-3*np.cos(2*t/3)/2, 0])
        cardioid = ParametricCurve(function_l_1, [0, 3*PI, DEGREES], color = PURPLE_A).shift(offset_l)
        cardioid_involute = ParametricCurve(function_l_2, [0, 3*PI, DEGREES], color = BLUE).shift(offset_l)
        texts = r"s(\theta)=\sin(", r"\frac{1}{3}", r"{\theta})"
        formula_l = MTex(r"s(\theta)=\sin(\frac{1}{3}{\theta})", isolate = texts, tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW, r"\sin": ORANGE, r"\frac{1}{3}": TEAL}).scale(0.8).shift(2*UP + 3.5*LEFT)
        parts_l = [formula_l.get_part_by_tex(text) for text in texts]
        point_l = Dot(color = RED).shift(offset_l)
        direction_l = Arrow(ORIGIN, RIGHT, buff = 0, color = RED).shift(offset_l)
        start_l = group_start.copy().shift(offset_l)
        alpha = ValueTracker(0.0)
        def point_l_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(function_l_1(angle) + offset_l)
        def direction_l_updater(mob: Arrow):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_l_1(angle) + offset_l, function_l_1(angle) + offset_l + unit(angle))
        
        offset_r = 0.25*UP + 3.5*RIGHT
        function_r_1 = lambda t: np.array([3*np.sin(4*t)/4+3*np.sin(2*t)/2, -3/4-3*np.cos(4*t)/4+3*np.cos(2*t)/2, 0]) #s(\theta)=2sin(3\theta)
        function_r_2 = lambda t: np.array([-np.sin(4*t)/4+np.sin(2*t)/2, -3/4+np.cos(4*t)/4+np.cos(2*t)/2, 0])
        deltoid = ParametricCurve(function_r_1, [0, PI, DEGREES], color = BLUE).shift(offset_r)
        deltoid_involute = ParametricCurve(function_r_2, [0, PI, DEGREES], color = PURPLE_A).shift(offset_r)
        texts = r"s(\theta)=\sin(", r"3", r"{\theta})"
        formula_r = MTex(r"s(\theta)=\sin(3{\theta})", isolate = texts, tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW, r"\sin": ORANGE, r"3": TEAL}).scale(0.8).shift(2*UP + 3.5*RIGHT)
        parts_r = [formula_r.get_part_by_tex(text) for text in texts]
        point_r = Dot(color = RED).shift(offset_r)
        direction_r = Arrow(ORIGIN, RIGHT, buff = 0, color = RED).shift(offset_r)
        start_r = group_start.copy().shift(offset_r)
        beta = ValueTracker(0.0)
        def point_r_updater(mob: Dot):
            angle = beta.get_value()
            mob.move_to(function_r_1(angle) + offset_r)
        def direction_r_updater(mob: Arrow):
            angle = beta.get_value()
            mob.put_start_and_end_on(function_r_1(angle) + offset_r, function_r_1(angle) + offset_r + unit(angle))
        
        self.play(Transform(cycloid_out, cardioid), Transform(cycloid_in, deltoid), 
                  FadeIn(direction_l, offset_l), FadeIn(point_l, offset_l), FadeIn(direction_r, offset_r), FadeIn(point_r, offset_r),
                  *[TransformFromCopy(parts_general_func[i], parts_l[i], path_arc = PI/6) for i in range(3)], *[TransformFromCopy(parts_general_func[i], parts_r[i], path_arc = -PI/6) for i in range(3)])
        self.remove(cycloid_out, cycloid_in).add(cardioid, deltoid, start_l, direction_l, point_l, start_r, direction_r, point_r)
        point_l.add_updater(point_l_updater)
        direction_l.add_updater(direction_l_updater)
        point_r.add_updater(point_r_updater)
        direction_r.add_updater(direction_r_updater)
        self.play(alpha.animate.set_value(3*PI), beta.animate.set_value(PI), run_time = 6)
        for mob in [point_l, direction_l, point_r, direction_r]:
            mob.clear_updaters()
        self.waiting(4+2+0-7, 1+28+25) #比如说 sinθ/3对应的是心脏线 而sin3θ则对应的是三尖瓣线 （空闲）

        fixed_l = Circle(radius = 0.25, color = WHITE).shift(offset_l + 0.75*UP)
        rolling_l = Circle(radius = 0.25, color = GREEN).shift(offset_l + 0.25*UP)
        fixed_r = Circle(radius = 2.25, color = WHITE).shift(offset_r + 0.75*DOWN)
        rolling_r = Circle(radius = 0.75, color = GREEN).shift(offset_r + 0.75*UP)
        formula_1 = MTex(r"a=\frac{1}{1+2\lambda}", tex_to_color_map = {r"a": TEAL, r"\lambda": GREEN}).scale(0.8).next_to(general_func, DOWN)
        formula_2 = MTexText(r"$\lambda$：动圆和定圆的半径比", tex_to_color_map = {r"\lambda": GREEN}).scale(0.4).next_to(formula_1, DOWN)
        formula = VGroup(formula_1, formula_2)
        ratio_l = MTex(r"\lambda = 1", color = GREEN).scale(0.6).shift(UP+6*LEFT)
        ratio_r = MTex(r"\lambda = -\frac{1}{3}", color = GREEN).scale(0.6).shift(UP+6*RIGHT)

        self.bring_to_back(fixed_l, rolling_l, fixed_r, rolling_r).play(*[ShowCreation(mob) for mob in [fixed_l, rolling_l, fixed_r, rolling_r]], 
                point_l.animate.set_color(YELLOW), point_r.animate.set_color(YELLOW), *[FadeOut(mob) for mob in [direction_l, direction_r, start_l, start_r]], )
        self.play(Write(ratio_l), Write(ratio_r))
        self.waiting(2, 15) #θ的速率由摆线族里面定圆和动圆的半径关系决定
        alpha.set_value(0)
        beta.set_value(0)
        point_l.add_updater(point_l_updater)
        point_r.add_updater(point_r_updater)
        self.play(ApplyMethod(alpha.set_value, 3*PI, run_time = 6), ApplyMethod(beta.set_value, PI, run_time = 6), 
                  Rotate(rolling_l, TAU, about_point = offset_l + 0.75*UP, run_time = 6), Rotate(rolling_r, -TAU, about_point = offset_r + 0.75*DOWN, run_time = 6), 
                  FadeIn(formula, 0.5*UP))
        point_l.clear_updaters()
        point_r.clear_updaters()
        self.waiting(1+0+2+3-6, 20+19+22+1) #具体是这么一个式子 （空闲） 而反过来 每条内外摆线 无论闭不闭合 都有一个对应的速率
        self.waiting(0, 17) #（空闲）

        self.play(*[FadeOut(mob) for mob in [formula, ratio_l, ratio_r, fixed_l, rolling_l, fixed_r, rolling_r]])
        self.waiting(1, 21) #所有这些函数都是好积分的
        self.waiting(3, 4) #而且积分的结果就是自己缩放了一定倍数
        self.waiting(0, 14) #（空闲）

        alpha.set_value(0)
        beta.set_value(0)
        def point_l_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(function_l_2(angle) + offset_l)
        point_l.add_updater(point_l_updater)
        line_l = Line(offset_l, offset_l, color = [PURPLE_A, BLUE])
        def line_l_updater(mob: Line):
            angle = alpha.get_value()
            mob.put_start_and_end_on(offset_l + function_l_1(angle), offset_l + function_l_2(angle))
        line_l.add_updater(line_l_updater)
        def involute_l_updater(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(function_l_2, [0, angle, DEGREES], color = BLUE).shift(offset_l)
            mob.set_points(curve.get_all_points())
        cardioid_involute.add_updater(involute_l_updater)
        self.bring_to_back(line_l, cardioid_involute).play(alpha.animate.set_value(3*PI), run_time = 5)
        self.waiting(3+2-5, 26+16) #也就是说 心脏线的渐开线还是心脏线 比起原曲线来放大了三倍
        def point_r_updater(mob: Dot):
            angle = beta.get_value()
            mob.move_to(function_r_2(angle) + offset_r)
        point_r.add_updater(point_r_updater)
        line_r = Line(offset_r, offset_r, color = [BLUE, PURPLE_A])
        def line_r_updater(mob: Line):
            angle = beta.get_value()
            mob.put_start_and_end_on(offset_r + function_r_1(angle), offset_r + function_r_2(angle))
        line_r.add_updater(line_r_updater)
        def involute_r_updater(mob: ParametricCurve):
            angle = beta.get_value()
            curve = ParametricCurve(function_r_2, [0, angle, DEGREES], color = BLUE).shift(offset_r)
            mob.set_points(curve.get_all_points())
        deltoid_involute.add_updater(involute_r_updater)
        self.bring_to_back(line_r, deltoid_involute).play(beta.animate.set_value(PI), run_time = 5)
        for mob in [line_l, cardioid_involute, line_r, deltoid_involute]:
            mob.clear_updaters()
        self.waiting(3+1+0-5, 1+28+17) #而三尖瓣线的渐开线还是三尖瓣线 比原曲线缩小了三分之二 （空闲）

        self.waiting(1, 25) #其它所有的内外摆线
        self.waiting(2, 3) #渐开线也都是自己的缩放
        self.waiting(1, 5) #到此共54秒 + 浮点误差1帧

        shade = Rectangle(height = FRAME_HEIGHT, width = FRAME_WIDTH, fill_opacity = 1, fill_color = BACK, stroke_width = 0)
        self.add(shade, title, title_line, notice6).play(FadeIn(shade))
         
        print(self.num_plays, self.time + 1)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_4(Scene):
    def construct(self):
        notice6 = Notice("旋轮线族", "请　欣赏")
        notice7 = Notice("等角螺线", "请　欣赏")

        title = Text(r"弧度方程", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        func = MTex(r"s(\theta)=e^\theta", tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW, r"e": ORANGE}).next_to(3*UP, DOWN)
        self.add(title, title_line, notice6).waiting(0, 25) #正弦函数看完了
        self.play(Write(func), ReplacementTransform(notice6, notice7))
        self.waiting(0, 19) #来看看指数函数吧
        self.waiting(0, 24) #（空闲）

        offset = 2*DOWN + 3.5*LEFT
        arrow_x = Arrow(2*LEFT, 2*RIGHT, buff = 0, stroke_width = 3).shift(offset)
        arrow_y = Arrow(0.5*DOWN, 4.5*UP, buff = 0, stroke_width = 3).shift(offset)
        graph = FunctionGraph(np.exp, [-2, 1.5, 0.01], color = BLUE).shift(offset)
        self.play(ShowCreation(arrow_x), ShowCreation(arrow_y), ShowCreation(graph))
        self.waiting(1, 21) #指数函数有一个比较麻烦的地方
        self.waiting(2, 16) #它的零点不在θ=0处
        arrow = Arrow(offset + UL + 0.2*UL, offset + 2*LEFT + 0.2*UL)
        limit = MTex(r"\lim_{\theta\to-\infty}e^\theta=0", tex_to_color_map = {r"\theta": YELLOW, r"e": ORANGE}).scale(0.7).next_to(offset + UL + 0.2*UL, UP, buff = 0)
        self.play(Write(limit), FadeInFromPoint(arrow, offset + UL + 0.2*UL))
        self.waiting(0, 11) #而是在负无穷
        self.waiting(0, 15) #（空闲）

        offset = 2*RIGHT + 0.25*DOWN
        func_1 = lambda t: 2*np.exp(t)*(np.sin(t) + np.cos(t))
        func_2 = lambda t: 2*np.exp(t)*(np.sin(t) - np.cos(t))
        func_3 = lambda t: 2*np.exp(t)*(-np.sin(t) - np.cos(t))
        func_4 = lambda t: 2*np.exp(t)*(-np.sin(t) + np.cos(t))
        funcs = [func_1, func_2, func_3, func_4]
        def functions(index: int):
            def util(length: float):
                if length == 0:
                    return ORIGIN
                else:
                    angle = np.log(length)
                    return np.array([funcs[index](angle), funcs[(index + 1)%4](angle), 0])
            return util
        
        point_1 = Dot(color = RED).shift(2*DR + offset).save_state()
        point_2 = Dot(color = RED).shift(2*DL + offset).save_state()
        point_3 = Dot(color = RED).shift(2*UL + offset).save_state()
        point_4 = Dot(color = RED).shift(2*UR + offset).save_state()
        arrow_1 = Arrow(2*DR + offset, 2*DR + 0.75*RIGHT + offset, color = RED, buff = 0).save_state()
        arrow_2 = Arrow(2*DL + offset, 2*DL + 0.75*DOWN + offset, color = RED, buff = 0).save_state()
        arrow_3 = Arrow(2*UL + offset, 2*UL + 0.75*LEFT + offset, color = RED, buff = 0).save_state()
        arrow_4 = Arrow(2*UR + offset, 2*UR + 0.75*UP + offset, color = RED, buff = 0).save_state()
        trace_1 = TracedPath(point_1.get_center, stroke_width = 5, stroke_color = RED)
        trace_2 = TracedPath(point_2.get_center, stroke_width = 4, stroke_color = GREEN)
        trace_3 = TracedPath(point_3.get_center, stroke_width = 4, stroke_color = BLUE)
        trace_4 = TracedPath(point_4.get_center, stroke_width = 4, stroke_color = PURPLE)
        start_1 = VGroup(arrow_1, point_1).copy().set_color(GREY)
        
        alpha = ValueTracker(1.0)
        def point_updater(index: int):
            def util(mob: Dot):
                value = alpha.get_value()
                position = functions(index)(value) + offset
                mob.restore().set_height(value**0.5*0.16).move_to(position)
            return util
        def arrow_updater(index: int):
            def util(mob: Arrow):
                value = alpha.get_value()
                angle = 0 if value == 0 else np.log(value)
                position = functions(index)(value) + offset
                mob.restore().put_start_and_end_on(position, position + 0.75*value**0.5 * unit(angle - PI/2*index))
            return util
        
        self.play(FadeInFromPoint(arrow_1, 2*DR + offset), FadeInFromPoint(point_1, 2*DR + offset))
        self.add(start_1, arrow_1, point_1).waiting(1, 4) #当然这不是什么大问题
        point_1.add_updater(point_updater(0))
        arrow_1.add_updater(arrow_updater(0))
        self.bring_to_back(trace_1).play(alpha.animate.set_value(0.0), run_time = 4)
        trace_1.clear_updaters()
        self.waiting(2+2-4, 6+2) #我们可以从θ=0开始 反向倒回负无穷
        self.waiting(2, 22) #这样画出来的 是一条等角螺线
        self.waiting(0, 21) #（空闲）

        trace_1.become(ParametricCurve(functions(0), [0, 1, 0.001], color = YELLOW)).shift(offset)
        trace_0 = ParametricCurve(functions(0), [0, 1, 0.01], color = RED, stroke_width = 5).shift(offset)
        def trace_0_updater(mob: VMobject):
            value = alpha.get_value()
            curve = ParametricCurve(lambda t: functions(0)(1-t), [0, 1-value, 0.01]).shift(offset)
            mob.set_points(curve.get_all_points())
        trace_0.add_updater(trace_0_updater)
        line_0 = Line(offset, offset, color = RED, stroke_width = 5)
        def line_0_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(functions(0)(value) + offset, functions(1)(value) + offset)
        line_0.add_updater(line_0_updater)
        point_2.add_updater(point_updater(1))
        arrow_2.add_updater(arrow_updater(1))
        self.bring_to_back(trace_2, trace_1, trace_0, line_0).add(arrow_2, point_2).play(alpha.animate.set_value(1.0), run_time = 4)
        line_0.clear_updaters()
        trace_2.clear_updaters().become(ParametricCurve(functions(1), [0, 1, 0.001], color = GREEN)).shift(offset)
        self.remove(trace_0, start_1).waiting(2+2-4, 7+21) #指数函数的积分是它自身 于是它的渐开线也是一条等角螺线
        self.waiting(0, 22) #（空闲）
        for mob in [point_1, arrow_1, point_2, arrow_2]:
            mob.clear_updaters()

        point_3.add_updater(point_updater(2))
        point_4.add_updater(point_updater(3))
        arrow_3.add_updater(arrow_updater(2))
        arrow_4.add_updater(arrow_updater(3))
        alpha.set_value(0.0)
        square = Line(2*DL + offset, 2*UL + offset, stroke_width = 5, color = RED).add_line_to(2*UR + offset).add_line_to(2*DR + offset)
        self.bring_to_back(trace_3, trace_4).add(arrow_3, arrow_4, point_3, point_4).play(ShowCreation(square), alpha.animate.set_value(1.0), run_time = 4)
        #如果我们再做出两条渐开线出来 就会发现
        for mob in [point_3, arrow_3, point_4, arrow_4]:
            mob.clear_updaters()
        trace_3.clear_updaters().become(ParametricCurve(functions(2), [0, 1, 0.001], color = BLUE)).shift(offset)
        trace_4.clear_updaters().become(ParametricCurve(functions(3), [0, 1, 0.001], color = PURPLE)).shift(offset)
        self.remove(line_0, square)
        square = Square(side_length = 4, stroke_width = 5, color = RED).shift(offset).save_state()
        self.add(square, arrow_1, arrow_2, arrow_3, arrow_4, point_1, point_2, point_3, point_4)
        
        positions = [functions(i)(2/3) + offset for i in range(4)]
        dogs = [Dot(color = YELLOW).shift(position) for position in positions]
        beta = ValueTracker(0.0)
        fore = lambda t: t*(3-t**2)/2
        back = lambda t: t**2*(3-t)/2
        def dog_arrow_updater(index: int):
            def util(mob: Arrow):
                ratio = beta.get_value()
                start = interpolate(positions[index], positions[(index+1)%4], back(ratio))
                end = interpolate(positions[index], positions[(index+1)%4], fore(ratio))
                mob.restore().put_start_and_end_on(start, end)
            return util
        dog_arrows = [Arrow(positions[i], positions[(i+1)%4], color = YELLOW, buff = 0).save_state().add_updater(dog_arrow_updater(i)) for i in range(4)]
        self.play(*[ShowCreation(mob) for mob in dogs])
        self.add(*dog_arrows).play(beta.animate.set_value(1.0), rate_func = linear, run_time = 4/3)
        beta.set_value(0.0)
        self.play(beta.animate.set_value(1.0), rate_func = linear, run_time = 4/3)
        beta.set_value(0.0)
        self.play(beta.animate.set_value(1.0), rate_func = linear, run_time = 4/3)
        self.waiting(1+3+0-5, 16+5+17) #在四条曲线上 地位对应的每一点 都在追逐着下一个点 （空闲）

        positions = [2*DR + offset, 2*DL + offset, 2*UL + offset, 2*UR + offset]
        arrows = [arrow_1, arrow_2, arrow_3, arrow_4]
        self.play(*[FadeOutToPoint(arrows[i], positions[i]) for i in range(4)], *[FadeOut(mob, scale = 0) for mob in [*dogs, point_1, point_2, point_3, point_4]])
        self.waiting(0, 9) #也就是说......

        alpha.set_value(1.0)
        doge = ImageMobject("doge.webp", height = 0.5)
        def doge_updater(index: int):
            def util(mob: Dot):
                value = alpha.get_value()
                angle = 0 if value == 0 else np.log(value)
                position = functions(index)(value) + offset
                mob.restore().set_height(value**0.5*0.5).rotate(angle-index*PI/2).move_to(position)
            return util
        doges = [doge.copy().shift(positions[i]).save_state().rotate(-i*PI/2) for i in range(4)]
        def doge_arrow_updater(index: int):
            def util(mob: Arrow):
                value = alpha.get_value()
                angle = 0 if value == 0 else np.log(value)
                position = functions(index)(value) + offset
                mob.restore().put_start_and_end_on(position, position - 0.75*value**0.5 * unit(angle - PI/2*index))
            return util
        doge_arrows = [Arrow(positions[i], positions[i] - 0.75*unit(-PI/2*i), color = ORANGE, buff = 0).save_state() for i in range(4)]
        self.add(*doges).play(LaggedStart(*[FadeIn(mob, scale = np.infty) for mob in doges], group = VGroup(), lag_ratio = 1/3, run_time = 2))
        self.waiting(1, 19) #......如果我们在正方形的四个顶点处各放一条狗
        self.add(*doge_arrows, *doges).play(LaggedStart(*[FadeInFromPoint(doge_arrows[i], positions[i]) for i in range(4)], group = VGroup(), lag_ratio = 1/3, run_time = 2))
        for i in range(4):
            doges[i].add_updater(doge_updater(i))
            doge_arrows[i].add_updater(doge_arrow_updater(i))
        self.play(alpha.animate.set_value(0.0), run_time = 4)
        self.waiting(4+3-6, 7+1) #每条狗始终朝着下一条狗运动 速度不变 那么四条狗就会画出这样的四条曲线来
        self.waiting(0, 18) #（空闲）
        self.remove(*doge_arrows, *doges)

        alpha.set_value(1.0)
        def string_updater(index: int):
            def util(mob: Arrow):
                value = alpha.get_value()
                curve = ParametricCurve(lambda t: functions(index)(1-t), [0, 1-value, 0.01]).shift(offset)
                mob.set_points(curve.get_all_points())
            return util
        strings = [ParametricCurve(functions(i), [0, 1, 0.001], color = RED, stroke_width = 5).add_updater(string_updater(i)) for i in range(4)]
        def square_updater(mob: Square):
            value = alpha.get_value()
            angle = 0 if value == 0 else np.log(value)
            mob.restore().scale(value).rotate(angle)
        square.add_updater(square_updater)
        self.add(*strings).play(alpha.animate.set_value(0.0), run_time = 4) #而曲线的总长度 恰好就是正方形的边长
        self.remove(square, trace_1, trace_2, trace_3, trace_4)
        for mob in strings:
            mob.clear_updaters()
        self.waiting(0, 23) #（空闲）
        
        general_func = MTex(r"s(\theta)=e^{a\theta}", tex_to_color_map = {(r"s", r"e"): ORANGE, r"\theta": YELLOW, r"a": TEAL}).next_to(3*UP, DOWN)
        self.play(Transform(func[0:6], general_func[0:6]), FadeIn(general_func[6], scale = np.infty), Transform(func[6], general_func[7]), 
                  *[FadeOut(mob) for mob in [*strings, arrow_x, arrow_y, graph, arrow, limit]])
        self.remove(func).add(general_func)
        self.waiting(1, 29) #当然这样的巧合也不是追逐曲线都有的
        self.waiting(0, 17) #（空闲）

        def functions(n: int, index: int):
            ratio = np.tan(PI/n)
            # coefficient = ratio/(1+ratio**2)
            # coefficient = np.sin(PI/n)*np.cos(PI/n)
            coefficient = np.cos(PI/n)
            def util(length: float):
                phase = -index*TAU/n
                if length == 0:
                    return ORIGIN
                else:
                    angle = np.log(length)/ratio + phase
                    return 2*coefficient*length * np.array([np.sin(angle)+ratio*np.cos(angle), -np.cos(angle)+ratio*np.sin(angle), 0])
            return util
        coefficient_l = MTex(r"a = \tan(\frac{\pi}{3})", tex_to_color_map = {r"a": TEAL, (r"\pi", r"3"): BLUE}).scale(0.8).next_to(2.8*UP + 3*LEFT, DOWN)
        coefficient_r = MTex(r"a = \tan(\frac{\pi}{5})", tex_to_color_map = {r"a": TEAL, (r"\pi", r"5"): PURPLE_A}).scale(0.8).next_to(2.8*UP + 3*RIGHT, DOWN)
        offset_l = 3*LEFT + 0.75*DOWN
        offset_r = 3*RIGHT + 0.5*DOWN
        positions_l = [functions(3, i)(1) + offset_l for i in range(3)]
        positions_r = [functions(5, i)(1) + offset_r for i in range(5)]
        polygon_l = Polygon(*positions_l, color = RED, stroke_width = 5)
        polygon_r = Polygon(*positions_r, color = RED, stroke_width = 5)
        self.play(Write(coefficient_l), Write(coefficient_r), ShowCreation(polygon_l), ShowCreation(polygon_r))
        self.waiting(0, 24) #如果不是四条狗
        
        doges_l = [doge.copy().shift(positions_l[i]).save_state().rotate(-i*TAU/3) for i in range(3)]
        doges_r = [doge.copy().shift(positions_r[i]).save_state().rotate(-i*TAU/5) for i in range(5)]
        doge_arrows_l = [Arrow(positions_l[i], positions_l[i] - 0.75*unit(-i*TAU/3), color = BLUE, buff = 0).save_state() for i in range(3)]
        doge_arrows_r = [Arrow(positions_r[i], positions_r[i] - 0.75*unit(-i*TAU/5), color = PURPLE_A, buff = 0).save_state() for i in range(5)]
        self.play(*[FadeIn(mob, scale = np.infty) for mob in doges_l + doges_r])
        self.add(*doge_arrows_l, *doge_arrows_r, *doges_l, *doges_r).play(*[FadeInFromPoint(doge_arrows_l[i], positions_l[i]) for i in range(3)], *[FadeInFromPoint(doge_arrows_r[i], positions_r[i]) for i in range(5)])
        self.waiting(0, 2) #而是其它数量的狗

        alpha.set_value(1.0)
        def doge_l_updater(index: int):
            def util(mob: Dot):
                value = alpha.get_value()
                angle = 0 if value == 0 else np.log(value)/np.tan(PI/3)
                position = functions(3, index)(value) + offset_l
                mob.restore().set_height(value**0.5*0.5).rotate(angle-index*TAU/3).move_to(position)
            return util
        for i in range(3):
            doges_l[i].add_updater(doge_l_updater(i))
        def doge_r_updater(index: int):
            def util(mob: Dot):
                value = alpha.get_value()
                angle = 0 if value == 0 else np.log(value)/np.tan(PI/5)
                position = functions(5, index)(value) + offset_r
                mob.restore().set_height(value**0.5*0.5).rotate(angle-index*TAU/5).move_to(position)
            return util
        for i in range(5):
            doges_r[i].add_updater(doge_r_updater(i))
        def doge_arrow_l_updater(index: int):
            def util(mob: Arrow):
                value = alpha.get_value()
                angle = 0 if value == 0 else np.log(value)/np.tan(PI/3)
                position = functions(3, index)(value) + offset_l
                mob.restore().put_start_and_end_on(position, position - 0.75*value**0.5 * unit(angle - TAU/3*index))
            return util
        for i in range(3):
            doge_arrows_l[i].add_updater(doge_arrow_l_updater(i))
        def doge_arrow_r_updater(index: int):
            def util(mob: Arrow):
                value = alpha.get_value()
                angle = 0 if value == 0 else np.log(value)/np.tan(PI/5)
                position = functions(5, index)(value) + offset_r
                mob.restore().put_start_and_end_on(position, position - 0.75*value**0.5 * unit(angle - TAU/5*index))
            return util
        for i in range(5):
            doge_arrows_r[i].add_updater(doge_arrow_r_updater(i))
        def string_l_updater(index: int):
            def util(mob: Arrow):
                value = alpha.get_value()
                curve = ParametricCurve(lambda t: functions(3, index)(1-t), [0, 1-value, 0.01]).shift(offset_l)
                mob.set_points(curve.get_all_points())
            return util
        def string_r_updater(index: int):
            def util(mob: Arrow):
                value = alpha.get_value()
                curve = ParametricCurve(lambda t: functions(5, index)(1-t), [0, 1-value, 0.01]).shift(offset_r)
                mob.set_points(curve.get_all_points())
            return util
        traces_l = [ParametricCurve(functions(3, i), [0, 1, 0.001], color = BLUE).shift(offset_l).add_updater(string_l_updater(i)) for i in range(3)]
        traces_r = [ParametricCurve(functions(5, i), [0, 1, 0.001], color = PURPLE_A).shift(offset_r).add_updater(string_r_updater(i)) for i in range(5)]
        self.bring_to_back(*traces_l, *traces_r).play(alpha.animate.set_value(0.0), run_time = 4)
        self.remove(*doge_arrows_l, *doge_arrows_r, *doges_l, *doges_r)
        for mob in traces_l+traces_r:
            mob.clear_updaters()
        self.waiting(2+2-4, 16+24) #曲线的总长度就要另算了 这个时候的曲线是别的的等角螺线
        self.waiting(2, 14) #相互不是渐开线的关系

        def involute_function(length: float):
            ratio = np.tan(PI/3)
            coefficient = np.cos(PI/3)
            phase = -PI/2
            if length == 0:
                return ORIGIN
            else:
                angle = np.log(length)/ratio + phase
                return 2*coefficient*length/ratio * np.array([np.sin(angle)+ratio*np.cos(angle), -np.cos(angle)+ratio*np.sin(angle), 0])
        special_function = functions(3, 0)
        def involute_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(involute_function, [0, value, 0.01]).shift(offset_l)
            mob.set_points(curve.get_all_points())
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(special_function(value) + offset_l, involute_function(value) + offset_l)
        trace_special = ParametricCurve(special_function, [0, 1, 0.001], color = YELLOW).shift(offset_l).add_updater(string_l_updater(0))
        involute = ParametricCurve(involute_function, [0, 1, 0.001], color = ORANGE).shift(offset_l).add_updater(involute_updater)
        line = Line(special_function(1), involute_function(1), color = YELLOW).shift(offset_l).add_updater(line_updater)
        alpha.set_value(1.0)
        self.add(trace_special).play(alpha.animate.set_value(0.0), run_time = 2)
        self.add(involute, line).play(alpha.animate.set_value(1.0), run_time = 2)
        for mob in [trace_special, involute, line]:
            mob.clear_updaters()
        self.remove(trace_special).waiting(1+1+1-4, 21+27+24) #它们真正的渐开线 就像它们的积分那样 会多出一个缩放比例来
        self.waiting(0, 19) #（空闲）

        self.waiting(1, 16) #不过再怎么说
        self.waiting(2, 8) #曲线的总长度还是好算的
        self.waiting(3, 8) 
        shade = Rectangle(height = FRAME_HEIGHT, width = FRAME_WIDTH, fill_color = BACK, fill_opacity = 1, stroke_width = 0)
        self.play(FadeIn(shade))
        self.waiting(3, 0) #到此共86秒
        
        print(self.num_plays, self.time + 1)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

####################################################################  

class Chapter3_0(Scene):

    def construct(self):

        text3 = Text("第三节 弧度方程", font = 'simsun', t2c={"第三节": YELLOW, "弧度方程": GREEN})

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(Scene):
    def construct(self):
        notice1 = Notice("本节内容", "敬请期待")
        notice2 = Notice("严格性处理", "请　量力")
        notice3 = Notice("函数变换", "请记结论")
        
        self.play(Write(notice1))
        self.waiting(0, 20) #看完了这些例子

        title = Text(r"弧度方程", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP, 3*UP)
        shade = Shade()

        offset = 5*LEFT+2*DOWN
        function_1 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2)))
        function_2 = lambda t: 1.5*(unit(t)+(t*unit(t-PI/2))+(t**2/2*unit(t-PI)))
        curve = ParametricCurve(function_1, [0, PI, DEGREES], color = YELLOW, stroke_width = 6).shift(offset)
        curve_base = curve.copy().set_stroke(color = GREY, width = 4).set_fill(color = BACK, opacity = 1)
        involute = ParametricCurve(function_2, [0, PI, DEGREES], color = BLUE, stroke_width = 6).shift(offset)
        
        start = Dot(color = GREY).shift(offset + function_1(0))
        point = Dot(color = RED).shift(offset + function_1(2*PI/3))
        direction = Arrow(offset + function_1(2*PI/3), offset + function_1(2*PI/3) + unit(2*PI/3), buff = 0, color = RED)
        start_direction = Arrow(offset+1.5*RIGHT, offset+2.5*RIGHT, buff = 0, color = GREY)
        group_start = VGroup(start, start_direction)
        group_point = VGroup(point, direction)
        fixed_start = group_start.copy().shift(2*UL+0.5*DOWN)
        fixed_direction = group_point.copy().shift(function_1(0) - function_1(2*PI/3) + 2*UL+0.5*DOWN).rotate(-2*PI/3, about_point = 5.5*LEFT + 0.5*DOWN).save_state()
        angle_notation = Arc(radius = 0.2, angle = 2*PI/3, color = YELLOW).shift(offset + 1.5*UP + 0.5*LEFT)
        angle_theta = MTex(r"\theta", color = YELLOW).scale(0.6).shift(offset + 1.5*UP + 0.5*LEFT).save_state().shift(0.4*unit(PI/3))
        text_func = MTex(r"s(\theta)", tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW}).next_to(3*UP, DOWN)
        part_curve = ParametricCurve(function_1, [0, 2*PI/3, DEGREES], color = ORANGE, stroke_width = 6).shift(offset)
        text_length = MTex(r"s", color = ORANGE).scale(0.6).next_to(offset + function_1(PI/2), RIGHT)
        
        alpha = ValueTracker(0)
        def point_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(function_1(angle) + offset)
        def direction_updater(mob: Arrow):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_1(angle) + offset, function_1(angle) + offset + unit(angle))
        def part_updater(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(function_1, [0, angle, DEGREES]).shift(offset)
            mob.set_points(curve.get_all_points())
        def fixed_updater(mob: VGroup):
            angle = alpha.get_value()
            mob.restore().rotate(angle, about_point = 5.5*LEFT + 0.5*DOWN)
        def arc_updater(mob: Arc):
            angle = alpha.get_value()
            trace = Arc(radius = 0.2, angle = angle, color = YELLOW).shift(offset + 1.5*UP + 0.5*LEFT)
            mob.become(trace)
        def theta_updater(mob: MTex):
            angle = alpha.get_value()
            ratio = clip(angle/(PI/2), 0, 1)
            mob.restore().shift(0.4*unit(angle/2)).scale(ratio)
        point.add_updater(point_updater)
        direction.add_updater(direction_updater)
        part_curve.add_updater(part_updater)
        fixed_direction.add_updater(fixed_updater)
        angle_notation.add_updater(arc_updater)
        angle_theta.add_updater(theta_updater)
        self.add(angle_notation, angle_theta, fixed_start, fixed_direction, curve, part_curve, text_length, group_start, group_point, shade, text_func, title, title_line, notice1
            ).play(ApplyMethod(alpha.set_value, 2*PI/3, run_time = 2), FadeIn(text_length, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)), FadeOut(shade), Write(title), Write(text_func), title_line.animate.put_start_and_end_on(3*UP + 6*LEFT, 3*UP + 6*RIGHT))
        for mob in [point, direction, part_curve, fixed_direction, angle_notation, angle_theta]:
            mob.clear_updaters()
        self.waiting(0, 5) #我们来看一看弧度方程本身
        self.waiting(0, 20) #（空闲）

        self.waiting(3, 0) #如果大家对严格性有一定要求的话
        self.waiting(1, 23) #在看完第二节以后
        self.waiting(2, 12) #对弧度方程的疑惑一定变多了吧
        self.waiting(0, 19) #（空闲）
        self.waiting(2, 1) #这一节我们就来干点脏活
        self.waiting(0, 27) #（空闲）

        arrows_t = []
        n = 18
        for i in range(n+1):
            angle = i*PI/n
            arrow = Arrow(function_1(angle), function_1(angle) + 0.1*np.sqrt(i)*unit(angle+PI/2), buff = 0, color = ORANGE).shift(offset)
            arrows_t.append(arrow)
        
        half_brace = RadParameterCurve(lambda t: PI/2*np.array([np.sin(t), np.cos(t)]), [PI/2, PI*3/2, TAU/1000], color = PURPLE)
        offset = half_brace.get_end()
        brace = RadParameterCurve(lambda t: PI/2*np.array([np.sin(t), np.cos(t)]), [-PI/2, PI*3/2, PI/1800], color = ORANGE).shift(-offset + 3*RIGHT)
        start_point = brace.get_start()
        end_point = brace.get_end()
        half_brace.shift(end_point-offset)
        points = list(brace.get_points()[::600].copy())
        points.append(end_point)
        
        text = Text("没有弧度方程", font = "simsun").scale(0.4).next_to(0.5*DOWN + 3.6*RIGHT, UP)
        arrow_text = Arrow(0.5*DOWN + 3.6*RIGHT, DOWN + 4.1*RIGHT, buff = 0)

        arrows_f = []
        for i in range(19):
            t = i/n*TAU - PI/2
            cost = PI/2*np.cos(t)
            angle = cost - PI/2
            radius = cost
            curvature = 1 if np.sin(t)>0 else 0
            direction = 0.3*radius*(2*curvature-1)*unit(angle)
            arrow_i = Arrow(points[i], points[i]+direction, buff = 0, color = PURPLE if curvature else ORANGE)
            arrows_f.append(arrow_i)
        
        self.play(ShowCreation(brace, rate_func = linear, run_time = 2), ShowCreation(half_brace, rate_func = squish_rate_func(linear, 0.5, 1), run_time = 2), ReplacementTransform(notice1, notice2))
        self.waiting(2, 0) #首先 是所有的曲线都有对应的弧度方程吗
        self.play(Write(text), Grow(arrow_text))
        self.waiting(0, 9) #答案是否定的
        self.waiting(0, 20) #（空闲）
        
        self.bring_to_back(*arrows_f, *arrows_t).play(LaggedStart(*[Grow(mob) for mob in arrows_t], group = VGroup()), LaggedStart(*[Grow(mob) for mob in arrows_f], group = VGroup()), lag_ratio = 0.3, run_time = 2)
        self.waiting(0, 27) #只有那些向着一个方向弯曲的曲线
        self.waiting(2, 21) #才能保证角度在整条曲线上单调
        self.waiting(0, 20) #（空闲）

        offset = ORIGIN
        arrow_x = Arrow(2*LEFT, 2*RIGHT, buff = 0, stroke_width = 4).shift(offset)
        arrow_y = Arrow(2*DOWN, 2*UP, buff = 0, stroke_width = 4).shift(offset)
        notation_x = MTex(r"\theta", color = YELLOW).scale(0.6).next_to(2*RIGHT, UP, buff = 0.1)
        notation_y = MTex(r"s", color = ORANGE).scale(0.6).next_to(2*UP, RIGHT, buff = 0.1)
        circle = Circle(color = YELLOW, radius = PI/2).shift(offset)
        point_phase = Dot(PI/2*DOWN, color = RED)
        start_brace = Dot(color = GREY).shift(start_point)
        point_brace = Dot(color = RED).shift(start_point)
        direction_brace = Arrow(start_point, start_point + 0.6*unit(0), buff = 0, color = RED)
        start_direction_brace = Arrow(start_point, start_point + 0.6*unit(0), buff = 0, color = GREY)

        def get_curve_position(t: float):
            ratio = t/TAU
            index, residue = integer_interpolate(0, 18, ratio)
            point = interpolate(points[index], points[index+1], residue)
            return point
        alpha = ValueTracker(0.0)
        def point_brace_updater(mob: Dot):
            t = alpha.get_value()
            mob.move_to(get_curve_position(t))
        def direction_brace_updater(mob: Arrow):
            t = alpha.get_value()
            angle = PI/2*np.cos(t-PI/2)
            mob.put_start_and_end_on(get_curve_position(t), get_curve_position(t) + 0.6*unit(angle))
        point_brace.add_updater(point_brace_updater)
        direction_brace.add_updater(direction_brace_updater)
        
        self.play(ShowCreation(arrow_x), ShowCreation(arrow_y), ShowCreation(notation_x), ShowCreation(notation_y))
        self.play(ShowCreation(circle), FadeIn(point_phase, scale = np.infty), FadeIn(point_brace, scale = np.infty), Grow(direction_brace))
        self.add(start_direction_brace, start_brace, direction_brace, point_brace).play(Rotate(point_phase, about_point = ORIGIN, angle = TAU), alpha.animate.set_value(TAU), run_time = 6)
        self.waiting(3+3+2-8, 11+1+16) #一般的曲线虽然也能定义角度和弧长 但一个弧长不一定只对应一个角度 还得通过别的参数把它们统一起来
        self.waiting(0, 26) #（空闲）

        shade = Shade().next_to(2.1*LEFT, RIGHT, buff = 0)
        self.add(shade, title, title_line, text_func, notice2).play(FadeIn(shade), *[FadeOut(mob) for mob in arrows_t])
        self.remove(shade, arrow_x, arrow_y, notation_x, notation_y, circle, point_phase, start_direction_brace, start_brace, point_brace, direction_brace, half_brace, brace, text, arrow_text, *arrows_f)
        self.waiting(2, 4) #其次 我们怎么从弧度方程出发
        self.waiting(1, 20) #推导出曲线的方程呢
        self.waiting(0, 19) #（空闲）

        texts = r"\begin{cases}", r"\ x(\theta)=\int_{0}^\theta\cos(\phi+\phi_0)\ {s}'(\phi)\,d\phi", r"\\", r"\ y(\theta)=\int_{0}^\theta\,\sin(\phi+\phi_0)\ {s}'(\phi)\,d\phi", r"\end{cases}"
        definition = MTex(r"".join(texts), 
                          isolate = [r"\cos(\phi+\phi_0)", r"\sin(\phi+\phi_0)", r"{s}'(\phi)\,d\phi", texts[1], texts[3]], 
                          tex_to_color_map = {(r"x", r"y"): GREEN, (r"{0}", r"\theta"): YELLOW, (r"\phi", r"\phi_0"): RED, r"{s}": ORANGE}).scale(0.8).next_to(ORIGIN)
        definition.get_part_by_tex(texts[1]).shift(0.2*UP)
        definition.get_part_by_tex(texts[3]).shift(0.2*DOWN)
        surr_unit_vector = SurroundingRectangle(VGroup(definition.get_part_by_tex(r"\cos(\phi+\phi_0)"), definition.get_part_by_tex(r"\sin(\phi+\phi_0)")), buff = 0.05, color = YELLOW_A)
        surr_ds = SurroundingRectangle(definition.get_parts_by_tex(r"{s}'(\phi)\,d\phi"), buff = 0.05, color = YELLOW_A)
        text_unit_vector = MTexText(r"朝向$\phi+\phi_0$\\的单位向量", tex_to_color_map = {(r"\phi", r"\phi_0"): RED}).scale(0.5).next_to(surr_unit_vector, DOWN, buff = 1)
        arrow_unit_vector = Arrow(text_unit_vector, surr_unit_vector)
        text_unit_vector.add(arrow_unit_vector)
        text_ds = MTexText(r"弧长微元\\$ds=s'(\phi)d\phi$", tex_to_color_map = {r"\phi": RED, r"{s}": ORANGE}).scale(0.5).next_to(surr_ds, DOWN, buff = 1)
        arrow_ds = Arrow(text_ds, surr_ds)
        text_ds.add(arrow_ds)
        self.play(FadeIn(definition))
        self.waiting(1, 5) #这靠的是这个公式
        self.waiting(3, 10) #它给出了用θ表示x和y的参数方程
        self.waiting(0, 22) #（空闲）

        self.play(LaggedStart(ShowCreation(surr_unit_vector), ShowCreation(surr_ds), lag_ratio = 0.3), run_time = 1.5)
        self.play(LaggedStart(FadeIn(text_unit_vector, 0.5*UP), FadeIn(text_ds, 0.5*UP), lag_ratio = 0.3), run_time = 1.5)
        self.waiting(2+2-3, 15+17) #这个公式的思路其实很简单 就是把这条曲线一段一段地拼起来
        self.waiting(0, 21) #（空闲）
        
        text_phi_0 = MTex(r"\phi_0=0", color = GREY).scale(0.8).next_to(start_direction)
        self.play(Write(text_phi_0))
        self.waiting(1, 3) #公式里还有一个起始角
        self.waiting(1, 26) #它表示我们开始的方向
        self.waiting(0, 26) #（空闲）

        offset = TAU*LEFT + 0.2*LEFT
        function_1 = lambda t: np.array([2*t + np.sin(2*t), 1 - np.cos(2*t), 0])
        function_2 = lambda t: np.array([2*t - np.sin(2*t), np.cos(2*t) - 1, 0])
        cycloid_0 = ParametricCurve(function_1, [0, PI/2, DEGREES], color = ORANGE, stroke_width = 6).shift(offset)
        cycloid_1 = ParametricCurve(function_1, [PI/2, PI, DEGREES], color = PURPLE, stroke_width = 6).shift(offset)
        cycloid = VGroup(cycloid_0, cycloid_1)
        involute = ParametricCurve(function_2, [0, PI, DEGREES], color = RED, stroke_width = 6).shift(offset)
        arrow_1 = Dot(offset, color = ORANGE).add(Arrow(offset, offset+RIGHT, color = ORANGE, buff = 0))
        arrow_2 = Dot(offset, color = RED).add(Arrow(offset, offset+DOWN, color = RED, buff = 0))
        text_1 = MTex(r"\phi_0=0", color = ORANGE, tex_to_color_map = {r"=": WHITE}).scale(0.6).next_to(offset+RIGHT, DOWN, buff = 0.1)
        text_2 = MTex(r"\phi_0=-\frac{\pi}{2}", color = RED, tex_to_color_map = {r"=": WHITE}).scale(0.6).next_to(offset+DOWN, DOWN, buff = 0.1)
        radian_1 = MTex(r"s(\theta)=\sin(\theta)", tex_to_color_map = {(r"s", r"\sin"): ORANGE, r"\theta": YELLOW}).scale(0.6).next_to(offset+PI*RIGHT+2*UP, UP, buff = 0.1)
        radian_2 = MTex(r"t(\theta)=\cos(\theta)", tex_to_color_map = {(r"t", r"\cos"): RED, r"\theta": YELLOW}).scale(0.6).next_to(offset+PI*RIGHT+2*DOWN, DOWN, buff = 0.1)
        shade.next_to(ORIGIN, LEFT, buff = 0)
        self.add(shade, title, title_line, text_func).play(FadeIn(shade))
        self.remove(angle_notation, angle_theta, fixed_start, fixed_direction, curve, part_curve, text_length, group_start, group_point, text_phi_0
                    ).bring_to_back(cycloid, involute, arrow_2, arrow_1, text_1, text_2, radian_1, radian_2).play(FadeOut(shade))
        self.waiting(1+2-2, 13+10) #有了这个公式 之前的那些奇奇怪怪的约定
        highlight = cycloid_1.copy().set_stroke(width = 10, color = YELLOW)
        self.play(ShowPassingFlash(highlight))
        self.play(ShowPassingFlash(highlight))
        self.waiting(0, 12) #比如负数长度要倒车什么的
        self.waiting(1, 25) #就都是很自然的推论了
        self.waiting(0, 18) #（空闲）

        self.waiting(1, 3) #实际上......
        definition.refresh_bounding_box()
        self.play(ShowPassingFlashAround(definition, buff = 0.3), run_time = 2)
        self.waiting(0, 24) #......我就是这么定义弧度方程对应的曲线的
        self.waiting(0, 29+1) #到此共73秒+误差-1帧

        shade.move_to(ORIGIN)
        self.add(shade, cycloid_0, cycloid_1, radian_1, title, title_line, text_func, notice2).play(FadeIn(shade), ReplacementTransform(notice2, notice3))
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_2(Scene):
    def construct(self):
        notice3 = Notice("函数变换", "请记结论")
        notice4 = Notice("积分运算", "请　量力")

        title = Text(r"弧度方程", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        text_func = MTex(r"s(\theta)", tex_to_color_map = {r"s": ORANGE, r"\theta": YELLOW}).next_to(3*UP, DOWN)
        offset = TAU*LEFT + 0.2*LEFT
        function_1 = lambda t: np.array([2*t + np.sin(2*t), 1 - np.cos(2*t), 0])
        function_2 = lambda t: np.array([2*t - np.sin(2*t), np.cos(2*t) - 1, 0])
        cycloid_0 = ParametricCurve(function_1, [0, PI/2, DEGREES], color = ORANGE, stroke_width = 6).shift(offset)
        cycloid_1 = ParametricCurve(function_1, [PI/2, PI, DEGREES], color = PURPLE, stroke_width = 6).shift(offset)
        cycloid = VGroup(cycloid_0, cycloid_1).save_state()
        radian_1 = MTex(r"s(\theta)=\sin(\theta)", tex_to_color_map = {(r"s", r"\sin"): ORANGE, r"\theta": YELLOW}).scale(0.6).next_to(offset+PI*RIGHT+2*UP, UP, buff = 0.1)
        self.add(title, title_line, text_func, cycloid, radian_1, notice3).waiting(1, 3) #在解决了这些基础问题之后

        shade_1 = Shade(radian_1, buff = 0.05)
        width_1 = shade_1.get_width()*LEFT
        shade_1.shift(width_1)
        func_sin = MTex(r"s(\theta)=\sin(\theta)", tex_to_color_map = {(r"s", r"\sin"): ORANGE, r"\theta": YELLOW}, isolate = [r"s(\theta)", r"=\sin(\theta)"]).next_to(3*UP, DOWN)
        parts_sin = [func_sin.get_part_by_tex(text).save_state() for text in [r"s(\theta)", r"=\sin(\theta)"]]
        shade_2 = Shade(func_sin, buff = 0.05)
        width_2 = text_func.get_center() - parts_sin[0].get_center()
        parts_sin[0].shift(width_2)
        parts_sin[0].refresh_bounding_box()
        parts_sin[1].refresh_bounding_box()
        width_3 = parts_sin[0].get_corner(RIGHT) - parts_sin[1].get_corner(RIGHT)
        shade_2.shift(width_3)
        parts_sin[1].shift(width_3)
        self.add(parts_sin[1], shade_2, parts_sin[0], radian_1, shade_1).remove(text_func
            ).play(shade_1.animate.shift(-width_1*0.6), radian_1.animate.shift(width_1*0.4), parts_sin[0].animate.restore(), shade_2.animate.shift(-width_2), parts_sin[1].animate.shift(-width_3), run_time = 2)
        self.remove(radian_1, shade_1, shade_2).waiting(0, 11) #我们来看一看弧度方程的性质
        self.waiting(0, 17) #（空闲）
        
        self.waiting(3, 0) #首先我们给弧度方程施加几个变换看看
        self.waiting(0, 17) #（空闲）

        self.remove(func_sin)
        func_sin_0 = MTex(r"s(\theta)=\sin(\theta)", tex_to_color_map = {(r"s", r"\sin"): ORANGE, r"\theta": YELLOW}, isolate = [r"s(\theta)=", r"\sin(\theta)"]).next_to(3*UP, DOWN)
        self.add(func_sin_0)
        parts_func_0 = [func_sin_0.get_part_by_tex(text).save_state() for text in [r"s(\theta)=", r"\sin(\theta)"]]
        func_sin_1 = MTex(r"s(\theta)=k\sin(\theta)", tex_to_color_map = {(r"s", r"\sin"): ORANGE, r"\theta": YELLOW, r"k": BLUE}, isolate = [r"s(\theta)=", r"k", r"\sin(\theta)"]).next_to(3*UP, DOWN)
        parts_func_1 = [func_sin_1.get_part_by_tex(text) for text in [r"s(\theta)=", r"k", r"\sin(\theta)"]]
        graph_scale = Value(100).scale(0.8).next_to(2.9*UP + 3.6*RIGHT, DOWN)
        k = MTex(r"k=", tex_to_color_map = {r"k": BLUE}).scale(0.8).next_to(graph_scale, LEFT)
        alpha = ValueTracker(1)
        def value_updater(mob: Value):
            value = alpha.get_value()
            mob.set_year(int(100*value))
        self.play(Transform(parts_func_0[0], parts_func_1[0]), Write(parts_func_1[1]), Transform(parts_func_0[1], parts_func_1[2]), FadeIn(k), FadeIn(graph_scale))
        self.waiting(1, 24) #最简单的变换大家都很熟悉了
        graph_scale.add_updater(value_updater)
        self.play(alpha.animate.set_value(2.0), cycloid.animate.scale(2.0).move_to(0.5*DOWN), run_time = 2)
        self.waiting(1, 7) #如果我们给弧度方程整体乘上一个值
        self.play(alpha.animate.set_value(3/8), cycloid.animate.scale(3/16).next_to(2*DOWN, UR, buff = 0).set_stroke(width = 3), run_time = 2)
        graph_scale.clear_updaters()
        self.waiting(0, 24) #它对应的曲线就会缩放相应的倍数
        self.waiting(0, 16) #（空闲）

        self.play(FadeOut(k), FadeOut(graph_scale), cycloid.animate.set_stroke(color = WHITE), Uncreate(parts_func_1[1]), parts_func_0[0].animate.restore(), parts_func_0[1].animate.restore())
        self.waiting(0, 8) #这相当好理解
        self.waiting(0, 19) #（空闲）

        cycloid_out = RadCurve(lambda t: 1.5*np.sin(t), [0, 2*TAU, TAU/1000]).shift(2*DOWN)
        cycloid_in = cycloid_out.copy().apply_function(lambda t: np.array([-t[0], t[1], 0]))
        parts_func_0 = [func_sin_0[0:9].save_state(), func_sin_0[9:].save_state()]
        func_sin_2 = MTex(r"s(\theta)=\sin(a\theta)", tex_to_color_map = {(r"s", r"\sin"): ORANGE, r"\theta": YELLOW, r"a": TEAL}).next_to(3*UP, DOWN)
        parts_func_2 = [func_sin_2[0:9], func_sin_2[9], func_sin_2[10:]]
        graph_rate = Value(100).scale(0.8).next_to(2.9*UP + 3.6*RIGHT, DOWN)
        a = MTex(r"a=", tex_to_color_map = {r"a": TEAL}).scale(0.8).next_to(graph_scale, LEFT, buff = 0.15).shift(0.05*DOWN)
        
        self.play(ShowCreation(cycloid_out), ShowCreation(cycloid_in), run_time = 2)
        self.remove(cycloid).waiting(0, 16) #之前我们还见过另外一种变换
        self.play(Transform(parts_func_0[0], parts_func_2[0]), Write(parts_func_2[1]), Transform(parts_func_0[1], parts_func_2[2]), FadeIn(a), FadeIn(graph_rate))
        self.waiting(1, 9) #那就是给自变量乘上一个值
        self.waiting(0, 16) #（空闲）
        
        alpha.set_value(1)
        graph_rate.add_updater(value_updater)
        def out_updater(mob: RadCurve):
            value = alpha.get_value()
            k = 1/(1-min(value, 0.9))
            curve = RadCurve(lambda t: 1.5*np.sin(value*t), [0, k*PI, k*TAU/1000]).shift(2*DOWN)
            curve_left = curve.copy().apply_function(lambda t: np.array([-t[0], t[1], 0])).reverse_points().append_points(curve.get_points())
            mob.set_points(curve_left.get_points())
        cycloid_out.add_updater(out_updater)
        shade = Shade(height = 2).shift(3*UP)
        self.remove(cycloid_in).bring_to_back(cycloid_out, shade).play(alpha.animate.set_value(1/3), run_time = 4)
        self.wait(0.5)
        self.play(alpha.animate.set_value(1.0), run_time = 4)
        cycloid_out.clear_updaters()
        graph_rate.clear_updaters()
        self.waiting(1+2+2+2-8.5, 17+6+16+27) #这种变换下来 对应的曲线会完全变掉 换成同族的另外一条曲线 这就没有任何规律性 只能靠试了
        self.waiting(1, 0) #（空闲）

        cycloid.restore().scale(3/8).set_stroke(width = 3).next_to(2*DOWN, UL, buff = 0)
        self.bring_to_back(cycloid).play(FadeOut(graph_rate), FadeOut(a), FadeOut(parts_func_2[1], scale = 0), parts_func_0[0].animate.restore(), parts_func_0[1].animate.restore(), 
                cycloid_out.animating(run_time = 2).scale(4/3, about_point = 5*DOWN).set_opacity(0), cycloid.animating(run_time = 2).scale(4/3, about_point = 5*DOWN).set_stroke(width = 6)
                ) #.animating()是自制方法，在 .animate 的基础上实现了可传参，从而彻底取代了ApplyMethod()
        self.remove(cycloid_out).waiting(1, 2) #除此之外 还有另一种变换

        parts_func_0 = [func_sin_0[0:10].save_state(), func_sin_0[10:].save_state()]
        func_sin_3 = MTex(r"s(\theta)=\sin(\theta+\phi_0)", tex_to_color_map = {(r"s", r"\sin"): ORANGE, r"\theta": YELLOW, r"\phi_0": RED}).next_to(3*UP, DOWN)
        parts_func_3 = [func_sin_3[0:10], func_sin_3[10:13], func_sin_3[13:]]
        graph_phase = Value(0).scale(0.8).next_to(2.9*UP + 3.8*RIGHT, DOWN)
        phi = MTex(r"\phi_0=", tex_to_color_map = {r"\phi_0": RED}).scale(0.8).next_to(graph_phase, LEFT, buff = 0.15)
        offset = DOWN + PI*LEFT
        function_1 = lambda t: np.array([2*t + np.sin(2*t), 1 - np.cos(2*t), 0])/2
        function_2 = lambda t: np.array([2*t - np.sin(2*t), np.cos(2*t) - 1, 0])/2
        point = Dot(offset,color = RED)
        direction = Arrow(offset, offset+0.6*RIGHT, buff = 0, color = RED)
        self.play(Transform(parts_func_0[0], parts_func_3[0]), FadeIn(parts_func_3[1], scale = np.infty), Transform(parts_func_0[1], parts_func_3[2]), FadeIn(phi), FadeIn(graph_phase), FadeIn(point), Grow(direction))
        self.waiting(1, 9) #那就是给自变量加上一个值
        self.waiting(0, 16) #（空闲）

        underline = Underline(func_sin_3[9:13], color = YELLOW)
        texts = r"\begin{cases}", r"\ x(\theta)=\int_{0}^\theta\cos(\phi+\phi_0)\ {s}'(\phi)\,d\phi", r"\\", r"\ y(\theta)=\int_{0}^\theta\,\sin(\phi+\phi_0)\ {s}'(\phi)\,d\phi", r"\end{cases}"
        definition = MTex(r"".join(texts), 
                          isolate = [r"{s}'(\phi)", texts[1], texts[3]], 
                          tex_to_color_map = {(r"x", r"y"): GREEN, (r"{0}", r"\theta"): YELLOW, (r"\phi", r"\phi_0"): RED, r"{s}": ORANGE}).scale(0.8).next_to(ORIGIN)
        definition.get_part_by_tex(texts[1]).shift(0.2*UP)
        definition.get_part_by_tex(texts[3]).shift(0.2*DOWN)
        surr_ds = [SurroundingRectangle(mob, buff = 0.05, color = YELLOW) for mob in definition.get_parts_by_tex(r"{s}'(\phi)")]
        self.waiting(1, 3) #这样一来......
        self.play(ShowPassingFlash(underline))
        self.play(ShowPassingFlash(underline))
        self.waiting(0, 8) #......起始值就不一定是0了
        self.play(FadeIn(definition, 0.5*UP))
        self.waiting(1, 5) #但这不算什么问题
        self.play(*[ShowPassingFlash(mob) for mob in surr_ds])
        self.waiting(1, 14) #定义式里面只需要用到导数
        alpha.set_value(0)
        def cycloid_updater(mob: Mobject):
            angle = alpha.get_value()
            mob.restore().shift(-function_1(angle)).rotate(-angle, about_point = offset)
        cycloid.save_state().add_updater(cycloid_updater)
        graph_phase.add_updater(value_updater)
        self.play(alpha.animate.set_value(PI), run_time = 4)
        cycloid.clear_updaters()
        graph_phase.clear_updaters()
        self.waiting(2+1-4, 16+26) #这个变换只会使曲线旋转 不会造成形状上的改变
        self.waiting(0, 22) #（空闲）
        
        graph_phase_1 = Value(0).scale(0.8).next_to(2.9*UP + 3.8*RIGHT, DOWN)
        cycloid_out.apply_function(lambda t: np.array([t[0], -t[1], 0]), about_point = DOWN)
        self.bring_to_back(cycloid_out).play(FadeOut(definition, 0.5*UP, rate_func = rush_into), FadeOut(graph_phase, rate_func = rush_into), FadeIn(graph_phase_1, rate_func = squish_rate_func(rush_from, 0.5, 1), run_time = 2), 
                  cycloid.animating(rate_func = rush_into, remover = True).apply_function(lambda t: np.array([t[0], 0, 0]), about_point = 0.5*DOWN).set_stroke(width = 0), 
                  cycloid_out.animating(run_time = 2).apply_function(lambda t: np.array([t[0], -t[1], 0]), about_point = 0.5*DOWN).set_stroke(opacity = 1), 
                  point.animating(run_time = 2).shift(UP), direction.animating(run_time = 2).shift(UP))
        offset = PI*LEFT
        involute_left = ParametricCurve(function_2, [0, 2*TAU, DEGREES], color = RED).shift(offset)
        involute_right = ParametricCurve(function_2, [-TAU, 0, DEGREES], color = RED).reverse_points().shift(offset)
        self.bring_to_back(involute_left, involute_right).play(ShowCreation(involute_left, run_time = 2), ShowCreation(involute_right, rate_func = rush_into))
        self.remove(involute_right)
        alpha.set_value(0)
        def involute_updater(mob: ParametricCurve):
            angle = alpha.get_value()
            curve = ParametricCurve(lambda t: function_2(t) + np.sin(angle)*2*unit(t), [-2*TAU, 2*TAU, DEGREES]).shift(offset)
            mob.set_points(curve.get_points())
        def point_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(function_1(angle) + offset)
        def direction_updater(mob: Arrow):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_1(angle) + offset, function_1(angle) + offset + 0.6*unit(angle))
        involute_left.add_updater(involute_updater)
        graph_phase_1.add_updater(value_updater)
        point.add_updater(point_updater)
        direction.add_updater(direction_updater)
        reminder = Text("*为了方便观察，忽略了曲线的转动", font = "simsun").scale(0.4).next_to(func_sin_3, DOWN)
        self.play(alpha.animating(run_time = 4).set_value(PI), FadeIn(reminder, run_time = 1, lag_ratio = 0.3))
        for mob in [involute_left, graph_phase_1, point, direction]:
            mob.clear_updaters()
        self.waiting(2+0-3, 29+23) #起始值的改变只会影响到渐开线的形状

        point_1 = Dot(offset, color = RED)
        direction_1 = Arrow(offset, offset+0.6*RIGHT, buff = 0, color = RED)
        group_point = VGroup(direction_1, point_1)
        start = group_point.copy().set_color(GREY)
        group_point.rotate(-PI/2, about_point = offset).save_state()
        self.play(*[FadeOut(mob) for mob in [graph_phase_1, phi, point, direction, reminder]], FadeOut(involute_left, rate_func = there_and_back, remover = False, run_time = 2), 
                  FadeOut(parts_func_3[1], scale = 0), parts_func_0[0].animate.restore(), parts_func_0[1].animate.restore(), 
                  *[FadeIn(mob, rate_func = squish_rate_func(rush_from, 0.5, 1), run_time = 2) for mob in [start, group_point]])
        self.waiting(0, 21) #当然 我们要是不动自变量

        func_sin_0.save_state()
        func_sin_4 = MTex(r"s(\theta)=\sin(\theta)+l", tex_to_color_map = {(r"s", r"\sin", r"l"): ORANGE, r"\theta": YELLOW}).next_to(3*UP, DOWN)
        parts_func_4 = [func_sin_4[0:11], func_sin_4[11:]]
        graph_length = Value(0).scale(0.8).next_to(2.9*UP + 3.8*RIGHT, DOWN)
        l = MTex(r"l=", tex_to_color_map = {r"l": ORANGE}).scale(0.8).next_to(graph_length, LEFT, buff = 0.15).shift(0.01*UP)
        self.play(Transform(func_sin_0, parts_func_4[0]), FadeIn(parts_func_4[1], scale = np.infty), FadeIn(graph_length), FadeIn(l))
        self.waiting(0, 20) #直接改变起始值

        line = Line(offset, offset, color = ORANGE)
        self.add(line, start, group_point)
        alpha.set_value(0)
        def direction_updater(mob: VMobject):
            value = alpha.get_value()
            mob.restore().shift(2*value*LEFT)
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(offset, offset + 2*value*LEFT)
        def involute_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(lambda t: function_2(t) - value*2*unit(t), [-2*TAU, 2*TAU, DEGREES]).shift(offset)
            mob.set_points(curve.get_points())
        group_point.add_updater(direction_updater)
        line.add_updater(line_updater)
        involute_left.add_updater(involute_updater)
        graph_length.add_updater(value_updater)

        self.play(alpha.animate.set_value(1), run_time = 4)
        self.waiting(1+0-2, 27+21) #也能达成相似的效果 （空闲）

        shade = Shade()
        self.add(shade, title, title_line, notice3).play(FadeIn(shade))
        self.remove(func_sin_0, parts_func_4[1], group_point, line, start, involute_left, graph_length, l, cycloid_out)
        func_1 = MTex(r"s(\theta)=1", tex_to_color_map = {(r"s", r"1"): ORANGE, r"\theta": YELLOW}).next_to(3*UP, DOWN)
        point = Dot(1.5*RIGHT, color = RED)
        arrow = Arrow(1.5*RIGHT, 1.5*RIGHT + 0.75*UP, buff = 0, color = RED)
        direction = VGroup(arrow, point)
        start = direction.copy().set_color(GREY).shift(1.5*LEFT).rotate(PI/2, about_point = ORIGIN)
        line = Line(ORIGIN, 1.5*RIGHT, color = ORANGE)
        self.add(line, start, direction, func_1, shade, title, title_line, notice3).play(FadeOut(shade))
        self.waiting(2, 22) #我们甚至可以认为s(θ)=1就表示一个不动的点
        circle = TracedPath(point.get_center, color = WHITE, stroke_width = 4)
        self.bring_to_back(circle).play(*[Rotate(mob, TAU, about_point = ORIGIN) for mob in [direction, start, line]], run_time = 5)
        self.waiting(1, 3) #到此共76+7秒

        self.add(shade, title, title_line, notice3).play(FadeIn(shade), ReplacementTransform(notice3, notice4))
        

        print(self.num_plays, self.time+1-7)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)
        
class Chapter3_3(Scene):
    def construct(self):
        notice4 = Notice("积分运算", "请　量力")
        notice5 = Notice("积分运算", "请　跳过")
        notice6 = Notice("原理展示", "请记笔记")

        title = Text(r"弧度方程", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        self.add(title, title_line, notice4)

        texts = r"\begin{cases}", r"\ x(\theta)=\int_{0}^\theta\cos(\phi+\phi_0){s}'(\phi)\,d\phi", r"\  =\ ", r"{s}(\phi)\cos(\phi+\phi_0)|_{\phi={0}}^\theta", r"\  +\ ", r"\int_{0}^\theta\cos(\phi+\phi_0-\frac{\pi}{2}){s}(\phi)\,d\phi", r"\\", r"\ y(\theta)=\int_{0}^\theta\,\sin(\phi+\phi_0){s}'(\phi)\,d\phi", r"\ =\  ", r"{s}(\phi)\,\sin(\phi+\phi_0)|_{\phi={0}}^\theta", r"\ +\  ", r"\int_{0}^\theta\,\sin(\phi+\phi_0-\frac{\pi}{2}){s}(\phi)\,d\phi", r"\end{cases}"
        definition = MTex(r"".join(texts), 
                          isolate = [*texts[1:6], *texts[7:12], r"\cos", r"\sin"], 
                          tex_to_color_map = {(r"x", r"y"): GREEN, (r"{0}", r"\theta"): YELLOW, (r"\phi", r"\phi_0", r"\frac{\pi}{2}"): RED, r"{s}": ORANGE}).scale(0.6).next_to(2*UP + 6.5*LEFT, buff = 0)
        definition.get_parts_by_tex(texts[1:6]).shift(0.2*UP)
        definition.get_parts_by_tex(texts[7:12]).shift(0.2*DOWN)
        definition.get_parts_by_tex(texts[10]).set_x(definition.get_parts_by_tex(texts[4]).get_x())

        text_involute = SurroundingRectangle(definition.get_parts_by_tex([texts[5], texts[11]]), color = BLUE)
        text_string = SurroundingRectangle(definition.get_parts_by_tex([texts[3], texts[9]]), color = ORANGE).stretch_to_fit_height(text_involute.get_height()).set_y(text_involute.get_y())
        self.play(*[FadeIn(mob) for mob in [definition[0], definition.get_parts_by_tex([texts[1], texts[7]])]]) #在有了定义式以后

        offset = PI**2/4*LEFT+2.45*DOWN
        function_1 = lambda t: (unit(t)+(t*unit(t-PI/2)))
        function_2 = lambda t: (unit(t)+(t*unit(t-PI/2))+(t**2/2*unit(t-PI)))
        curve = ParametricCurve(function_1, [0, PI, DEGREES], color = YELLOW, stroke_width = 6).shift(offset)
        curve_base = curve.copy().set_stroke(color = GREY, width = 4).set_fill(color = BACK, opacity = 1)
        involute = ParametricCurve(function_2, [0, PI, DEGREES], color = BLUE, stroke_width = 6).shift(offset)
        point = Dot(offset + function_1(0), color = RED)
        involute_point = Dot(offset + function_2(0), color = PURPLE_A)
        arrow_length = 0.5
        direction = Arrow(offset + function_1(0), offset + function_1(0) + arrow_length*unit(0), buff = 0, color = RED)
        involute_direction = Arrow(offset + function_2(0), offset + function_2(0) + arrow_length*unit(-PI/2), buff = 0, color = PURPLE_A)
        group_involute = VGroup(involute_point, involute_direction)
        group_point = VGroup(point, direction)
        line = Line(offset + function_1(0), offset + function_1(0), color = ORANGE)
        self.play(ShowCreation(curve), Grow(involute_direction), Grow(direction), FadeIn(point, scale = np.infty))
        self.add(line, involute_point, point).waiting(1, 8) #我们甚至可以通过变形

        alpha = ValueTracker(0)
        def point_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(function_1(angle) + offset)
        def direction_updater(mob: Arrow):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_1(angle) + offset, function_1(angle) + offset + arrow_length*unit(angle))
        def involute_point_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(function_2(angle) + offset)
        def involute_direction_updater(mob: Arrow):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_2(angle) + offset, function_2(angle) + offset + arrow_length*unit(angle-PI/2))
        def line_updater(mob: Line):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_1(angle) + offset, function_2(angle) + offset)
        point.add_updater(point_updater)
        direction.add_updater(direction_updater)
        involute_point.add_updater(involute_point_updater)
        involute_direction.add_updater(involute_direction_updater)
        line.add_updater(line_updater)
        curve.reverse_points()
        self.bring_to_back(curve_base, involute).play(ShowCreation(involute), Uncreate(curve), alpha.animate.set_value(PI), run_time = 3) #把渐开线的绘制过程展示出来 （空闲）
        for mob in [point, direction, involute_point, involute_direction, line]:
            mob.clear_updaters()
        
        self.play(Write(definition.get_parts_by_tex(texts[2:6])), Write(definition.get_parts_by_tex(texts[8:12])))
        self.waiting(0, 22) #这只需要一次简单的分部积分
        self.waiting(1+1-2, 20+25)
        self.play(*[WiggleOutThenIn(mob, scale_value = 1.8, rotation_angle = PI/10) for mob in definition.get_parts_by_tex(r"{s}")], run_time = 2) #我们把定义式中 弧度方程项积分
        self.play(*[WiggleOutThenIn(mob, scale_value = 1.2, rotation_angle = PI/20) for mob in definition.get_parts_by_tex([r"\cos", r"\sin"])], run_time = 2) #三角函数项求导
        self.play(ShowCreation(text_involute), ShowCreation(text_string))
        self.waiting(0, 20) #就会得到两个不同的项
        self.waiting(0, 22) #（空闲）

        copy_surr = text_involute.copy().set_stroke(color = YELLOW, width = 8)
        copy_curve = involute.copy().set_stroke(color = YELLOW, width = 8)
        self.add(copy_curve, involute_point).play(ShowPassingFlash(copy_surr), ShowPassingFlash(copy_curve, rate_func = rush_from), run_time = 1.5)
        self.add(copy_curve, involute_point).play(ShowPassingFlash(copy_surr), ShowPassingFlash(copy_curve, rate_func = rush_from), run_time = 1.5)
        self.waiting(1+2-3, 16+3) #带积分的那一项 正好描述的是渐开线
        copy_surr = text_string.copy().set_stroke(color = YELLOW, width = 8)
        copy_curve = line.copy().set_stroke(color = YELLOW, width = 8).reverse_points()
        self.add(copy_curve, involute_point, point).play(ShowPassingFlash(copy_surr), ShowPassingFlash(copy_curve), run_time = 1.5)
        self.add(copy_curve, involute_point, point).play(ShowPassingFlash(copy_surr), ShowPassingFlash(copy_curve), run_time = 1.5)
        self.waiting(1+2-3, 28+20) #而不带积分的那一项 正好就是从曲线上这一点出发的切线
        self.waiting(0, 20) #（空闲）

        shade = Shade()
        offset = 2*DOWN+5*LEFT
        arrow_x = Arrow(0.8*LEFT, 4.8*RIGHT, buff = 0, stroke_width = 4).shift(offset)
        arrow_y = Arrow(0.8*DOWN, 5.2*UP, buff = 0, stroke_width = 4).shift(offset)
        arrows = VGroup(arrow_x, arrow_y)
        angle = 5/12*PI
        point_limit = Dot(color = r"#EE0000", radius = 0.06).shift(4*unit(angle)).shift(offset)
        unit_vec = DashedLine(ORIGIN, 4*unit(angle), color = "#FFA7D7", stroke_width = 3).shift(offset)
        angle_alpha = MTex(r"\alpha", color = "#FFA7D7").scale(0.7).shift(0.4*unit(angle/2)).shift(offset)
        function_0 = lambda t: 4*unit(t)
        function_1 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2)))
        function_2 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI)))
        function_3 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2)))
        function_4 = lambda t: 4*(unit(t)+((angle-t)*unit(t+PI/2))+((angle-t)**2/2*unit(t+PI))+((angle-t)**3/6*unit(t+PI*3/2))+((angle-t)**4/24*unit(t)))
        involute_0 = ParametricCurve(function_0, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_1 = ParametricCurve(function_1, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_2 = ParametricCurve(function_2, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_3 = ParametricCurve(function_3, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_4 = ParametricCurve(function_4, [0, angle, DEGREES], color = ORANGE).shift(offset)
        point_0 = offset + 4*RIGHT
        point_1 = point_0 + 4*angle*UP
        point_2 = point_1 + 4*(angle)**2/2*LEFT
        point_3 = point_2 + 4*(angle)**3/6*DOWN
        point_4 = point_3 + 4*(angle)**4/24*RIGHT
        point_5 = point_4 + 4*(angle)**5/120*UP
        line_0 = Line(point_0, point_1, color = GREEN)
        line_1 = Line(point_1, point_2, color = BLUE)
        line_2 = Line(point_2, point_3, color = GREEN)
        line_3 = Line(point_3, point_4, color = BLUE)
        line_4 = Line(point_4, point_5, color = GREEN)
        text_0 = MTex(r"\frac{\alpha^0}{0!}", color = BLUE).scale(0.8).next_to(offset + 2*RIGHT, DOWN, buff = 0.1)
        text_1 = MTex(r"\frac{\alpha^1}{1!}", color = GREEN).scale(0.7).next_to(line_0, RIGHT, buff = 0.1)
        text_2 = MTex(r"\frac{\alpha^2}{2!}", color = BLUE).scale(0.6).next_to(line_1, UP, buff = 0.1)
        text_3 = MTex(r"\frac{\alpha^3}{3!}", color = GREEN).scale(0.5).next_to(line_2, LEFT, buff = 0.1)
        text_4 = MTex(r"\frac{\alpha^4}{4!}", color = BLUE).scale(0.4).next_to(line_3, DOWN, buff = 0.1)
        text_5 = MTex(r"\frac{\alpha^5}{5!}", color = GREEN).scale(0.3).next_to(line_4, RIGHT, buff = 0.1)
        involutes = VGroup(arrows, unit_vec, angle_alpha, involute_0, involute_1, involute_2, involute_3, involute_4, line_0, line_1, line_2, line_3, line_4)
        texts = VGroup(text_0, text_1, text_2, text_3, text_4, text_5)
        func_0 = MTex(r"\theta", color = ORANGE).scale(0.8).shift(offset + function_0(5*PI/24) - 0.3*unit(5*PI/24))
        func_1 = MTex(r"\frac{\theta^2}{2!}", color = YELLOW).scale(0.6).shift(offset + function_1(PI/6) - 0.4*unit(PI/6 + PI/2))
        func_2 = MTex(r"\frac{\theta^3}{3!}", color = ORANGE).scale(0.4).shift(offset + function_2(PI/10) - 0.2*unit(PI/10 + PI))
        func_3 = MTex(r"\frac{\theta^4}{4!}", color = YELLOW).scale(0.25).shift(offset + function_3(PI/20) - 0.2*unit(PI/20 + 3*PI/2))
        func_4 = MTex(r"\frac{\theta^5}{5!}", color = ORANGE).scale(0.05).shift(offset + function_4(PI/30) - 0.05*unit(PI/30))
        funcs = VGroup(func_0, func_1, func_2, func_3, func_4)
        left_half = VGroup(involutes, texts, funcs)
        
        mtex_sin = MTex(r"\sin\alpha=\frac{\alpha^1}{1!}-\frac{\alpha^3}{3!}+\frac{\alpha^5}{5!}-\cdots", color = GREEN, tex_to_color_map = {(r"=", r"+", r"-"): WHITE}).scale(0.8).next_to(1.5*UP+0.5*RIGHT)
        mtex_cos = MTex(r"\cos\alpha=\frac{\alpha^0}{0!}-\frac{\alpha^2}{2!}+\frac{\alpha^4}{4!}-\cdots", color = BLUE, tex_to_color_map = {(r"=", r"+", r"-"): WHITE}).scale(0.8).next_to(0.5*DOWN+0.5*RIGHT)
        right_half = VGroup(mtex_sin, mtex_cos)

        self.add(shade, notice4).play(FadeIn(shade))
        self.remove(title, title_line, definition, curve_base, point, direction, involute_point, involute_direction, line, involute, text_involute, text_string
            ).add(left_half, point_limit, right_half, shade, notice4
            ).play(FadeOut(shade), left_half.shift(LEFT).animate.shift(RIGHT), point_limit.shift(LEFT).animate.shift(RIGHT), right_half.shift(RIGHT).animate.shift(LEFT))
        self.waiting(1+2-2, 25+17) #在这个性质的帮助下 我们就能回过头来再看看第一节了
        self.waiting(0, 28) #（空闲）

        self.add(shade, notice4).play(FadeIn(shade), left_half.animating(remover = True).shift(LEFT), point_limit.animating(remover = True).shift(LEFT), right_half.animating(remover = True).shift(RIGHT))
        self.waiting(0, 24) #应该有不少人知道

        taylor = MTex(r"f(x_0+h)=f(x_0)+\frac{h^1}{1!}f'(x_0)+\frac{h^2}{2!}f''(x_0)+\cdots+\frac{h^n}{n!}f^{(n)}(x_0)+\int_0^h\frac{(h-t)^n}{n!}f^{(n+1)}(x_0+t)\,dt", 
                      isolate = r"\int_0^h\frac{(h-t)^n}{n!}f^{(n+1)}(x_0+t)\,dt", tex_to_color_map = {(r"x_0", r"t"): RED, r"h": YELLOW, (r"f", r"h-t"): ORANGE}).scale(0.55).next_to(6.5*LEFT + 3*UP, buff = 0)
        texts = [r"f(x_0+h)", r"&", r"=f(x_0)+\int_{0}^h{1}f'(x_0+t)\,dt", r"\\&", r"=f(x_0)-(h-t)f'(x_0+t)|_{t=0}^h+\int_{0}^h(h-t)f''(x_0+t)\,dt", r"\\&", r"=f(x_0)+hf'(x_0)-\frac{(h-t)^2}{2!}f''(x_0+t)|_{t=0}^h+\int_{0}^h\frac{(h-t)^2}{2!}f^{(3)}(x_0+t)\,dt"]
        texts.extend([r"\\&", r"=f(x_0)+hf'(x_0)+\frac{h^2}{2!}f''(x_0)-\frac{(h-t)^3}{3!}f^{(3)}(x_0+t)|_{t=0}^h+\int_{0}^h\frac{(h-t)^3}{3!}f^{(4)}(x_0+t)\,dt", r"\\&", r"=\cdots", r"\\&", r"=f(x_0)+\frac{h^1}{1!}f'(x_0)+\frac{h^2}{2!}f''(x_0)+\cdots+\frac{h^n}{n!}f^{(n)}(x_0)+\int_0^h\frac{(h-t)^n}{n!}f^{(n+1)}(x_0+t)\,dt"])
        calculation = MTex(r"".join(texts), isolate = texts[::2], tex_to_color_map = {(r"x_0", r"t"): RED, r"h": YELLOW, (r"f", r"{1}", r"h-t"): ORANGE}).scale(0.55).next_to(6.5*LEFT + 2*UP, DR, buff = 0)
        parts_calculation = [calculation.get_part_by_tex(texts[i]) for i in [0, 2, 4, 6, 8, 10, 12]]
        self.play(Write(taylor), ReplacementTransform(notice4, notice5))
        self.waiting(0, 16) #泰勒公式是有积分余项表达式的
        self.waiting(0, 18) #（空闲）

        self.play(FadeIn(parts_calculation[0], 0.2*UP))
        self.waiting(0, 22) #对一个函数而言
        self.play(FadeIn(parts_calculation[1], 0.2*UP, lag_ratio = 0.1, run_time = 2))
        self.waiting(0, 21) #我们可以通过反复对它分部积分
        self.play(FadeIn(parts_calculation[2], 0.2*UP, lag_ratio = 0.07, run_time = 2))
        self.waiting(0, 4) #来得到任意多项的泰勒公式
        self.waiting(0+1-2, 17+21)
        self.play(FadeIn(parts_calculation[3], 0.2*UP, lag_ratio = 0.05, run_time = 2)) #（空闲） 每分部积分一次
        self.play(FadeIn(parts_calculation[4], 0.2*UP, lag_ratio = 0.05, run_time = 2))
        self.waiting(0, 13) #函数的导数就会高一阶
        self.play(FadeIn(parts_calculation[5]), FadeIn(parts_calculation[6], 0.2*UP, lag_ratio = 0.05, run_time = 2))
        self.waiting(0, 12) #而它前面的多项式也会高一次
        self.waiting(0, 17) #（空闲）

        surr = SurroundingRectangle(taylor.get_part_by_tex(r"\int_0^h\frac{(h-t)^n}{n!}f^{(n+1)}(x_0+t)\,dt"))
        self.play(ShowCreationThenDestruction(surr), run_time = 2)
        self.waiting(0, 15) #只要积分余项最后收敛到0
        self.waiting(2, 18) #我们就能得到这个函数的泰勒展开
        self.waiting(0, 18+2) #到此共57秒 + 2帧误差

        self.play(FadeOut(taylor), FadeOut(calculation), ReplacementTransform(notice5, notice6))


        print(self.num_plays, self.time+1)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_4(Scene):
    def construct(self):
        notice6 = Notice("原理展示", "请记笔记")
        notice7 = Notice("所以说", "不要停下来啊")
        notice8 = Notice("讲解完毕", "请　鼓掌")

        self.add(notice6)
        self.waiting(0, 8) #而这个过程

        shade = Shade()
        offset = 2*DOWN+6*LEFT
        arrow_x = Arrow(0.8*LEFT, 4.8*RIGHT, buff = 0, stroke_width = 4).shift(offset)
        arrow_y = Arrow(0.8*DOWN, 5.2*UP, buff = 0, stroke_width = 4).shift(offset)
        arrows = VGroup(arrow_x, arrow_y)
        angle = 5/12*PI
        point = Dot(4*unit(angle), color = r"#EE0000", radius = 0.06).shift(offset)
        unit_vec = DashedLine(ORIGIN, 4*unit(angle), color = "#FFA7D7", stroke_width = 3).shift(offset)
        angle_alpha = MTex(r"\alpha", color = "#FFA7D7").scale(0.7).shift(0.4*unit(angle/2)).shift(offset)
        function_0 = lambda t: 4*unit(angle-t)
        function_1 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2)))
        function_2 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI)))
        function_3 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI))+(t**3/6*unit((angle-t)+PI*3/2)))
        function_4 = lambda t: 4*(unit(angle-t)+(t*unit((angle-t)+PI/2))+(t**2/2*unit((angle-t)+PI))+(t**3/6*unit((angle-t)+PI*3/2))+(t**4/24*unit(angle-t)))
        involute_0 = ParametricCurve(function_0, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_1 = ParametricCurve(function_1, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_2 = ParametricCurve(function_2, [0, angle, DEGREES], color = ORANGE).shift(offset)
        involute_3 = ParametricCurve(function_3, [0, angle, DEGREES], color = YELLOW).shift(offset)
        involute_4 = ParametricCurve(function_4, [0, angle, DEGREES], color = ORANGE).shift(offset)
        point_0 = offset + 4*RIGHT
        point_1 = point_0 + 4*angle*UP
        point_2 = point_1 + 4*(angle)**2/2*LEFT
        point_3 = point_2 + 4*(angle)**3/6*DOWN
        point_4 = point_3 + 4*(angle)**4/24*RIGHT
        point_5 = point_4 + 4*(angle)**5/120*UP
        line_0 = Line(point_0, point_1, color = GREEN)
        line_1 = Line(point_1, point_2, color = BLUE)
        line_2 = Line(point_2, point_3, color = GREEN)
        line_3 = Line(point_3, point_4, color = BLUE)
        line_4 = Line(point_4, point_5, color = GREEN)
        curve_0 = Line(offset, offset + 4*unit(angle), stroke_width = 6).append_points(involute_0.get_points()).add_line_to(offset).insert_n_curves(1000)
        curve_1 = Line(offset, offset + 4*unit(angle), stroke_width = 6).append_points(involute_1.get_points()).add_points_as_corners([point_0, offset]).insert_n_curves(1000)
        curve_2 = Line(offset, offset + 4*unit(angle), stroke_width = 6).append_points(involute_2.get_points()).add_points_as_corners([point_1, point_0, offset]).insert_n_curves(1000)
        curve_3 = Line(offset, offset + 4*unit(angle), stroke_width = 6).append_points(involute_3.get_points()).add_points_as_corners([point_2, point_1, point_0, offset]).insert_n_curves(1000)
        curve_4 = Line(offset, offset + 4*unit(angle), stroke_width = 6).append_points(involute_4.get_points()).add_points_as_corners([point_3, point_2, point_1, point_0, offset]).insert_n_curves(1000)
        curve_limit = Line(offset, offset + 4*unit(angle), stroke_width = 6).add_points_as_corners([point_5, point_4, point_3, point_2, point_1, point_0, offset]).insert_n_curves(1000)
        text_0 = MTex(r"\frac{\alpha^0}{0!}", color = BLUE).scale(0.8).next_to(offset + 2*RIGHT, DOWN, buff = 0.1)
        text_1 = MTex(r"\frac{\alpha^1}{1!}", color = GREEN).scale(0.7).next_to(line_0, RIGHT, buff = 0.1)
        text_2 = MTex(r"\frac{\alpha^2}{2!}", color = BLUE).scale(0.6).next_to(line_1, UP, buff = 0.1)
        text_3 = MTex(r"\frac{\alpha^3}{3!}", color = GREEN).scale(0.5).next_to(line_2, LEFT, buff = 0.1)
        text_4 = MTex(r"\frac{\alpha^4}{4!}", color = BLUE).scale(0.4).next_to(line_3, DOWN, buff = 0.1)
        text_5 = MTex(r"\frac{\alpha^5}{5!}", color = GREEN).scale(0.3).next_to(line_4, RIGHT, buff = 0.1)
        involutes = VGroup(arrows, unit_vec, angle_alpha, involute_0, involute_1, involute_2, involute_3, involute_4, line_0, line_1, line_2, line_3, line_4)
        texts = VGroup(text_0, text_1, text_2, text_3, text_4, text_5)
        func_0 = MTex(r"\theta", color = ORANGE).scale(0.8).shift(offset + function_0(5*PI/24) - 0.3*unit(5*PI/24))
        func_1 = MTex(r"\frac{\theta^2}{2!}", color = YELLOW).scale(0.6).shift(offset + function_1(PI/6) - 0.4*unit(PI/6 + PI/2))
        func_2 = MTex(r"\frac{\theta^3}{3!}", color = ORANGE).scale(0.4).shift(offset + function_2(PI/10) - 0.2*unit(PI/10 + PI))
        func_3 = MTex(r"\frac{\theta^4}{4!}", color = YELLOW).scale(0.25).shift(offset + function_3(PI/20) - 0.2*unit(PI/20 + 3*PI/2))
        func_4 = MTex(r"\frac{\theta^5}{5!}", color = ORANGE).scale(0.05).shift(offset + function_4(PI/30) - 0.05*unit(PI/30))
        funcs = VGroup(func_0, func_1, func_2, func_3, func_4)

        self.add(involutes, point, shade, notice6).play(FadeOut(shade))
        self.waiting(1, 10) #就是第一节那个神奇方法的原理
        self.waiting(0, 19) #（空闲）


        origin = MTex(r"(x, y)=(0, 0)", tex_to_color_map = {r"x": BLUE, r"y": GREEN}, isolate = r"0").scale(0.8).next_to(3*UP, UP)
        origin[7].set_color(BLUE)
        origin[9].set_color(GREEN)
        self.play(Write(origin))
        self.waiting(1, 14) #我们从原点开始出发

        reminder = MTexText(r"*注意$\phi$的旋转方向是顺时针，所以带负号").scale(0.4).next_to(origin, buff = 0.5)
        texts = [r"0 ", r"&", r"=x(\alpha{})" , r"\\&", r"=\int_0^{\alpha{}} {0}\cos({}\alpha-\pi-\theta)\,d\theta", 
                 r"\\&", r"={1}(-\cos({}\alpha-\theta))|_{\theta = 0}^{\alpha{}}+\int_0^{\alpha{}} {1}\cos({}\alpha-\frac{\pi}{2}-\theta)\,d\theta", 
                 r"\\&", r"=\cos(\alpha)-{}1+\frac{\theta}{1}(\sin({}\alpha-\theta))|_{\theta = 0}^{\alpha{}}+\int_0^{\alpha{}} \frac{\theta}{1}\cos({}\alpha-\theta)\,d\theta", 
                 r"\\&", r"=\cos(\alpha)-{}1+\frac{\theta^2}{2!}(\cos({}\alpha-\theta))|_{\theta = 0}^{\alpha{}}+\int_0^{\alpha{}} \frac{\theta^2}{2!}\cos({}\alpha+\frac{\pi}{2}-\theta)\,d\theta", 
                 r"\\&", r"=\cos(\alpha)-{}1+\frac{\alpha^2}{2!}+\frac{\theta^3}{3!}(-\sin({}\alpha-\theta))|_{\theta = 0}^{\alpha{}}+\int_0^{\alpha{}} \frac{\theta^3}{3!}\cos({}\alpha+\pi-\theta)\,d\theta", 
                 r"\\&", r"=\cdots", 
                 r"\\&", r"=\cos(\alpha)-\left({}1-\frac{\alpha^2}{2!}+\frac{\alpha^4}{4!}-\cdots\right)", 
                 ]
        formula = MTex(r"".join(texts), isolate = texts[::2], 
                tex_to_color_map = {r"\alpha{}": "#FFA7D7", r"\theta": RED, (r"{0}", r"{1}", r"\frac{\theta}{1}", r"\frac{\theta^2}{2!}", r"\frac{\theta^3}{3!}"): ORANGE, (r"{}\alpha", r"{0{}}", r"\frac{\pi}{2}", r"\pi"): YELLOW, (r"x", r"\cos(\alpha)", r"{}1", r"\frac{\alpha^2}{2!}", r"\frac{\alpha^4}{4!}"): BLUE}
                ).scale(0.5).next_to(3*UP + 1.2*LEFT, DR)
        parts_formula = [formula.get_part_by_tex(text) for text in texts[::2]]
        self.play(Write(VGroup(*parts_formula[0:3])), FadeIn(reminder))
        self.waiting(1, 16) #原点对应的弧度方程是s(θ)=1
        self.add(curve_0, point).play(Write(parts_formula[3]), ShowPassingFlash(curve_0, run_time = 4))
        self.waiting(0, 1) #我们对它分部积分一次 就能得到圆
        self.add(curve_1, point).play(Write(parts_formula[4]), ShowPassingFlash(curve_1, run_time = 4))
        self.waiting(0, 4) #再分部积分一次 就能得到圆的渐开线
        self.add(curve_2, point).play(Write(parts_formula[5]), ShowPassingFlash(curve_2, run_time = 4), ReplacementTransform(notice6, notice7))
        self.waiting(0, 1) #只要我们一直积分 泰勒展开就会不断添加新的项
        self.add(curve_3, point).play(Write(parts_formula[6]), ShowPassingFlash(curve_3, run_time = 4))
        self.waiting(0, 9) #（空闲）
        self.add(curve_4, point).play(Write(parts_formula[7]), ShowPassingFlash(curve_4, run_time = 4))
        self.waiting(0, 9) #（空闲）

        self.add(curve_limit, point).play(Write(parts_formula[8]), ShowPassingFlash(curve_limit, run_time = 4), ReplacementTransform(notice7, notice8))
        self.waiting(3+3-4, 12+20) #当迭代的渐开线收敛到圆上一点的时候 正弦函数和余弦函数也随之彻底展开了
        self.waiting(0, 26) #（空闲）

        self.waiting(2, 26) #从这种过程中 我们也可以发现
        self.waiting(1, 22) #这种漂亮的图示
        texts = r"\begin{cases}", r"\ x(\theta)=\int_{0}^\theta\cos(\phi+\phi_0)\ {s}'(\phi)\,d\phi", r"\\", r"\ y(\theta)=\int_{0}^\theta\,\sin(\phi+\phi_0)\ {s}'(\phi)\,d\phi", r"\end{cases}"
        definition = MTex(r"".join(texts), 
                          isolate = [r"\cos(\phi+\phi_0)", r"\sin(\phi+\phi_0)", r"{s}'(\phi)\,d\phi", texts[1], texts[3]], 
                          tex_to_color_map = {(r"x", r"y"): GREEN, (r"{0}", r"\theta"): YELLOW, (r"\phi", r"\phi_0"): RED, r"{s}": ORANGE})
        definition.get_part_by_tex(texts[1]).shift(0.3*UP)
        definition.get_part_by_tex(texts[3]).shift(0.3*DOWN)
        surr_unit_vector = SurroundingRectangle(VGroup(definition.get_part_by_tex(r"\cos(\phi+\phi_0)"), definition.get_part_by_tex(r"\sin(\phi+\phi_0)")), buff = 0.05, color = YELLOW_A)
        self.add(shade, notice8).play(FadeIn(shade))
        self.play(FadeIn(definition))
        self.waiting(0, 4) #大概没法推广到别的函数上了
        self.waiting(0, 21) #（空闲）

        self.play(ShowCreationThenDestruction(surr_unit_vector, time_width = 4.0), run_time = 3)
        self.waiting(2+2-3, 9+5) #定义式里面出现的三角函数 限制了弧度方程的发挥
        self.waiting(3, 11) #让它只能够用来解释正弦和余弦的泰勒展开
        self.waiting(0, 20) #（空闲）

        texts = [r"0 ", r"&", r"=y(\alpha{})" , r"\\&", r"=\int_0^{\alpha{}} {0}\sin({}\alpha-\pi-\theta)\,d\theta", 
                 r"\\&", r"={1}(-\sin({}\alpha-\theta))|_{\theta = 0}^{\alpha{}}+\int_0^{\alpha{}} {1}\sin({}\alpha-\frac{\pi}{2}-\theta)\,d\theta", 
                 r"\\&", r"=\sin(\alpha)+\frac{\theta}{1}(-\cos({}\alpha-\theta))|_{\theta = 0}^{\alpha{}}+\int_0^{\alpha{}} \frac{\theta}{1}\sin({}\alpha-\theta)\,d\theta", 
                 r"\\&", r"=\sin(\alpha)-\frac{\alpha}{1}+\frac{\theta^2}{2!}(\sin({}\alpha-\theta))|_{\theta = 0}^{\alpha{}}+\int_0^{\alpha{}} \frac{\theta^2}{2!}\sin({}\alpha+\frac{\pi}{2}-\theta)\,d\theta", 
                 r"\\&", r"=\sin(\alpha)-\frac{\alpha}{1}+\frac{\theta^3}{3!}(\cos({}\alpha-\theta))|_{\theta = 0}^{\alpha{}}+\int_0^{\alpha{}} \frac{\theta^3}{3!}\sin({}\alpha+\pi-\theta)\,d\theta", 
                 r"\\&", r"=\cdots", 
                 r"\\&", r"=\sin(\alpha)-\left(\frac{\alpha}{1}-\frac{\alpha^3}{3!}+\frac{\alpha^5}{5!}-\cdots\right)", 
                 ]
        formula_sin = MTex(r"".join(texts), isolate = texts[::2], 
                tex_to_color_map = {r"\alpha{}": "#FFA7D7", r"\theta": RED, (r"{0}", r"{1}", r"\frac{\theta}{1}", r"\frac{\theta^2}{2!}", r"\frac{\theta^3}{3!}"): ORANGE, (r"{}\alpha", r"{0{}}", r"\frac{\pi}{2}", r"\pi"): YELLOW, (r"y", r"\sin(\alpha)", r"\frac{\alpha}{1}", r"\frac{\alpha^3}{3!}", r"\frac{\alpha^5}{5!}"): GREEN}
                ).scale(0.5).next_to(3*UP + 1.2*LEFT, DR)
        
        self.play(FadeOut(definition))
        self.remove(formula).add(formula_sin, shade, notice8).play(FadeOut(shade))
        self.waiting(1+2-2, 24+23) #不过这也没什么 弧度方程能做的 已经足够多了
        self.waiting(2, 16)
        self.play(FadeIn(shade))
        self.waiting(3, 0) #到此共58+8秒


        
        print(self.num_plays, self.time+1-8)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#################################################################### 

class Summary(Scene):

    def construct(self):
        notice1 = Notice("良心视频", "请　三连")
        notice2 = Notice("下期预告", "敬请期待")
        notice3 = Notice("良心up主", "请　关注")

        self.play(Write(notice1))
        self.waiting(0, 27) #非常感谢大家能看到这里
        self.waiting(0, 16) #（空闲）

        source = ImageMobject("source.png", height = 6).shift(0.6*UP + 3.5*LEFT)
        text_source = MTexText(r"A Problem. Leo S. Gurin. \itshape The American Mathematical Monthly,\upshape \\Oct., 1996, Vol. 103, No. 8 (Oct., 1996), pp. 683-686").scale(0.4).next_to(source, DOWN, buff = 0.1)
        paragraph = MTexText(r"\small \noindent \textbf{TRIBUTE.} I learned about this problem \\and its solution in 1935, when I was in the \\eighth grade, from my teacher of mathe-\\matics, Yakov Stepanovich Chaikovsky, \\a very young man at that time.", tex_to_color_map = {r"Yakov Stepanovich Chaikovsky": YELLOW}, alignment = None).scale(0.8).next_to(0.5*LEFT)
        line_1 = Line(5.3*LEFT + 2.285*UP, 1.7*LEFT + 2.255*UP).insert_n_curves(7)
        line_2 = Line(5.3*LEFT + 2.165*UP, 1.7*LEFT + 2.135*UP).insert_n_curves(7)
        line_3 = Line(5.3*LEFT + 2.045*UP, 3/8*(1.7*LEFT + 2.015*UP)+5/8*(5.3*LEFT + 2.045*UP)).insert_n_curves(2)
        underline = VMobject(color = BLACK, stroke_width = 1).set_points([*line_1.get_all_points(), *line_2.get_all_points(), *line_3.get_all_points()])
        self.waiting(2, 15) #这种解释正余弦的展开式的方法
        self.play(FadeIn(source, 0.25*UP), FadeIn(text_source, 0.25*UP))
        self.waiting(1, 5) #据有文献可查的最早记录
        self.play(ShowCreation(underline), ShowIncreasingSubsets(paragraph), rate_func = linear, run_time = 5)
        self.waiting(2+3-5, 7+12) #是一位中学教师提出的 他名叫雅科夫·斯捷潘诺维奇·柴可夫斯基
        self.waiting(0, 20) #（空闲）

        self.waiting(3, 9) #他的一位学生在1935年的八年级课堂上
        self.waiting(1, 20) #听他讲述了这种方法
        self.waiting(0, 21) #（空闲）

        self.waiting(3, 5) #不幸的是 这位老师后来死于古拉格
        self.waiting(0, 22) #（空闲）

        self.waiting(4, 12) #我无从知晓这位老师是否已经发现了整套弧度方程的理论
        self.waiting(1, 29) #只能以这期视频作为纪念
        self.waiting(0, 20) #（空闲）

        like = Text("", font = 'vanfont')
        coin = Text("", font = 'vanfont')
        star = Text("", font = 'vanfont')
        share = Text("", font = 'vanfont')
        like1 = like.copy()
        coin1 = coin.copy()
        star1 = star.copy()
        like1.shift(3*LEFT)
        star1.shift(3*RIGHT)
        like1.scale(2)
        coin1.scale(2)
        star1.scale(2)
        sanlian1 = VGroup(like1, coin1, star1)
        self.remove(source, text_source, underline, paragraph).play(FadeInFromPoint(like1, 3*LEFT), FadeInFromPoint(coin1, ORIGIN), FadeInFromPoint(star1, 3*RIGHT))
        self.play(ApplyMethod(sanlian1.set_color, "#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian1])
        
        self.waiting(2-2, 21) #如果这期视频能让你感觉到这一点
        self.waiting(2, 0) #不妨一键三连支持一下
        self.waiting(0, 27) #（空闲）

        self.remove(sanlian1).play(ReplacementTransform(notice1, notice2))
        self.waiting(1, 11) #下期视频是第二个转折背后的原理
        self.waiting(0, 13) #（空闲）

        points = []
        points_base = []
        OMEGA = unit(2*PI/3)
        for i in range(-4, 5):
            for j in range(-7+int(i/2), 8+int(i/2)):
                position = j*RIGHT + i*OMEGA
                color_ratio = 6/5/clip(get_norm(position), 1, 6)-1/5
                point_ij = Dot(position, color = WHITE).set_opacity(color_ratio)
                points_base.append(point_ij.copy())
                point_ij.set_opacity(1).set_color(interpolate_color(BACK, TEAL, color_ratio)).generate_target()
                color_ratio = 6/5/clip(get_norm(np.sqrt(7)*position), 1, 6)-1/5
                point_ij.target.rotate(PI/3, about_point = ORIGIN).shift(2*position).scale(2).set_color(interpolate_color(BACK, TEAL, color_ratio))
                points.append(point_ij)
        random.shuffle(points)
        self.play(LaggedStart(*[FadeIn(point) for point in points], lag_ratio = 0.05), run_time = 3)
        self.waiting(2+1-3, 6+14) #我找到了一个挺不错的切入点 应该能让大家满意
        self.waiting(0, 16) #（空闲）

        shade = Shade()
        isomorphism = MTex(r"\mathbb{Z}[\omega]/(3+\omega)\cong \mathbb{Z}/(7)")
        self.bring_to_back(*points_base).play(*[MoveToTarget(point, path_arc = PI/6) for point in points], run_time = 2)
        self.waiting(0, 15) #复数在大多数时候很好用
        self.waiting(3, 10) #但有的时候 它也会影响你的判断
        self.waiting(0, 25)
        self.add(shade, notice2).play(FadeIn(shade)) #懂得什么时候用复数
        self.play(FadeIn(isomorphism))
        self.waiting(1, 11) #什么时候跳出复数看问题
        self.waiting(2, 0) #才能真正入门代数学
        self.waiting(0, 28) #（空闲）

        self.remove(shade, isomorphism, *points_base, *points)

        land = Line(np.array([-8,0,0]), np.array([8,0,0]))
        water = Polygon(np.array([-4,0,0]), np.array([-6,0,0]), np.array([-5,-4,0]), np.array([6,-4,0]), fill_color = BLUE_E, fill_opacity = 0.5, stroke_width = 0)
        band1 = Line(np.array([-6,0,0]), np.array([-5,-4,0]), color = BLUE)
        band2 = Line(np.array([-4,0,0]), np.array([6,-4,0]), color = BLUE)
        river = VGroup(water, band1, band2)
        moon = Circle(radius = 1.2, arc_center = np.array([-5,2,0]), fill_color = WHITE, fill_opacity = 0.9, stroke_width = 0)

        star0 = star.copy().set_color(BLUE).shift(UP)
        star2 = star0.copy().shift(1.3*UP-1.7*RIGHT)
        star3 = star0.copy().shift(2.2*UP+2.6*RIGHT)
        star4 = star0.copy().shift(0.3*UP+2.2*RIGHT)
        star5 = star0.copy().shift(-0.2*UP+6.0*RIGHT)
        star5_1 = coin.copy().set_color(BLUE).shift(2.7*UP+1.6*RIGHT)
        bigstars = VGroup(star2, star3, star4, star5, star5_1)
        star00 = star0.copy().scale(0.7)
        star6 = star00.copy().shift(1.4*UP+4.0*RIGHT)
        star7 = star00.copy().shift(1.7*UP+0.2*RIGHT)
        star8 = star00.copy().shift(0.4*UP+4.3*RIGHT)
        star9 = star00.copy().shift(0.1*UP-3.2*RIGHT)
        star10 = star00.copy().shift(-0.1*UP-2.5*RIGHT)
        star10_1 = like.copy().set_color(BLUE).scale(0.7).shift(2.5*UP-2.7*RIGHT)
        star10_2 = share.copy().set_color(BLUE).scale(0.7).shift(3.2*UP-0.7*RIGHT)
        smallstars = VGroup(star6, star7, star8, star9, star10, star10_1, star10_2)
        star000 = star0.copy().scale(0.4)
        star11 = star000.copy().shift(0.5*UP-1.3*RIGHT)
        star12 = star000.copy().shift(0.8*UP+0.8*RIGHT)
        star13 = star000.copy().shift(-0.2*UP+3.1*RIGHT)
        star14 = star000.copy().shift(1.1*UP+2.7*RIGHT)
        star15 = star000.copy().shift(1.2*UP-0.5*RIGHT)
        star16 = star000.copy().shift(2.2*UP-1.8*RIGHT)
        stardust = VGroup(star11, star12, star13, star14, star15, star16)
        stars = VGroup(bigstars, smallstars, stardust)
        painting = VGroup(river, land, moon, star0, stars)
        painting_others = VGroup(river, land, moon, stars)
        self.play(FadeIn(painting, lag_ratio = 0.01, run_time = 2), ReplacementTransform(notice2, notice3))
        #self.waiting(0, 1) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, 0.5*UP), FadeIn(text_name, 0.5*UP))
        self.waiting(1+2-3, 25+15) #知识的星空浩如烟海 而我 就像我的名字一样

        self.play(FadeOut(painting_others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star0.shift, DOWN))
        self.waiting(1, 7) #想要把天上的星星垂下来

        star_copy = star0.copy()
        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star0, apple))
        self.waiting(1, 5) #变成触手可及的果实

        snowflake = SnowFlake()
        snowflake_2 = snowflake.copy().set_color(RED).set_stroke(width = 1.5)
        snowflake_3 = snowflake.copy().set_color(BLUE).set_stroke(width = 2)
        anims = LaggedStart(SpreadOut(snowflake_2).update_config(rate_func = linear), SpreadOut(snowflake_3).update_config(rate_func = linear), SpreadOut(snowflake).update_config(rate_func = linear), rate_func = rush_into, run_time = 2)
        self.play(Transform(star0, star_copy), anims)
        self.remove(snowflake_2, snowflake_3) 
        #self.waiting(0, 0) #变成指引前路的火光
        self.waiting(1+0-2, 26+22) #变成指引前路的火光 （空闲）
        
        self.remove(star0, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(2, 13) #我是乐正垂星 我们下期视频再见

        self.waiting(5, 20)
        self.play(FadeOut(picture_photo), FadeOut(text_name), FadeOut(notice3))
        self.waiting(6) #到此共83秒
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)


####################################################################  

class Template(Scene):
    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)