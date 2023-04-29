from __future__ import annotations

from manimlib import *
import numpy as np

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

#######################################################

class Toy_1(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    # shell: manimgl Template.py Toy_1 -osr 480x480
    
    def construct(self):
        circle_out = Circle(radius = 3, stroke_color = WHITE, stroke_width = 3)
        circle_in = Circle(radius = 1, stroke_color = GREY, stroke_width = 3)
        center = Dot(color = GREY, radius = 0.05)
        circle_up = Circle(radius = 1, stroke_color = GREY, stroke_width = 3).shift(2*UP)
        center_up = Dot(color = YELLOW, radius = 0.05).shift(2*UP)
        circle_down = Circle(radius = 1, stroke_color = GREY, stroke_width = 3).shift(2*DOWN)
        center_down = Dot(color = YELLOW, radius = 0.05).shift(2*DOWN)
        
        alpha = ValueTracker(0.0)
        function = lambda t: [-np.cos(2*t)-2*np.cos(t), -np.sin(2*t)+2*np.sin(t), 0]
        deltoid = ParametricCurve(function, [0, TAU, TAU/100], color = GREEN, stroke_width = 6).save_state()
        def delta_updater(mob: ParametricCurve):
            value = alpha.get_value()
            mob.restore().rotate(value/3, about_point = ORIGIN)
        deltoid.add_updater(delta_updater)
        point = Dot(color = BLUE, radius = 0.05)
        point_up = Dot(color = RED, radius = 0.05)
        point_down = Dot(color = RED, radius = 0.05)
        def point_updater(position: np.ndarray):
            def util(mob: Dot):
                value = alpha.get_value()
                mob.move_to(unit(value) + position)
            return util
        point.add_updater(point_updater(ORIGIN))
        point_up.add_updater(point_updater(2*UP))
        point_down.add_updater(point_updater(2*DOWN))
        radius = Line(ORIGIN, RIGHT, color = GREY)
        radius_up = Line(ORIGIN, RIGHT, color = [YELLOW, RED])
        radius_down = Line(ORIGIN, RIGHT, color = [YELLOW, RED])
        def radius_updater(position: np.ndarray):
            def util(mob: Dot):
                value = alpha.get_value()
                mob.put_start_and_end_on(position, unit(value) + position)
            return util
        radius.add_updater(radius_updater(ORIGIN))
        radius_up.add_updater(radius_updater(2*UP))
        radius_down.add_updater(radius_updater(2*DOWN))
        
        circle_moving = Circle(radius = 1, stroke_color = BLUE, stroke_width = 3)
        def circle_updater(mob: Circle):
            value = alpha.get_value()
            mob.move_to(2*unit(value))
        circle_moving.add_updater(circle_updater)
        center_moving = Dot(color = BLUE, radius = 0.05)
        center_moving.add_updater(circle_updater)
        outside_moving = Dot(color = BLUE, radius = 0.05)
        def center_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(3*unit(value))
        outside_moving.add_updater(center_updater)
        radius = Line(ORIGIN, 3*RIGHT, color = [GREY, BLUE, BLUE, BLUE]).insert_n_curves(2)
        def outside_radius_updater(mob: Dot):
            value = alpha.get_value()
            mob.put_start_and_end_on(ORIGIN, 3*unit(value))
        radius.add_updater(outside_radius_updater)
        perp = Line(3*RIGHT, RIGHT, color = [BLUE, PURPLE])
        def perp_updater(mob: Dot):
            value = alpha.get_value()
            mob.put_start_and_end_on(3*unit(value), 2*unit(value) - unit(-value))
        perp.add_updater(perp_updater) 

        tangency = Dot(color = PURPLE, radius = 0.05)
        def tangency_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(2*unit(value) - unit(-value))
        tangency.add_updater(tangency_updater)
        line_moving = Line(2*UP, 2*DOWN, color = RED, stroke_width = 6)
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(2*UP + unit(value), 2*DOWN + unit(value))
        line_moving.add_updater(line_updater)
        lines = [radius, radius_up, radius_down, circle_moving, perp]
        dots = [center, center_up, center_down, point, point_up, point_down, tangency, center_moving, outside_moving]

        self.add(alpha, circle_out, circle_in, circle_up, circle_down, *lines, deltoid, line_moving, *dots)
        def alpha_updater(alpha: ValueTracker, dt):
            alpha.set_value(alpha.get_value() + dt*PI/4)
        alpha.add_updater(alpha_updater)
        self.waiting(8)
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#######################################################

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

    def get_t_func(self):
        return self.t_func

    def get_function(self):
        if hasattr(self, "underlying_function"):
            return self.underlying_function
        if hasattr(self, "function"):
            return self.function

    def get_x_range(self):
        if hasattr(self, "x_range"):
            return self.x_range

class Test_1(Scene):
    def construct(self):
        """
        test_1 = RadCurve(np.sin, [0, TAU, TAU/1000])
        test_2 = RadCurve(lambda t: 2*np.sin(t), [0, TAU, TAU/1000])
        test_3 = RadCurve(lambda t: 2*np.sin(2*t), [0, TAU, TAU/1000])
        test_4 = RadCurve(lambda t: 2*np.sin(3*t), [0, TAU, TAU/1000])
        test_5 = RadCurve(lambda t: 2*np.sin(t/2), [0, TAU*2, TAU/1000])
        test_6 = RadCurve(lambda t: 2*np.sin(t/3), [0, TAU*3/2, TAU/1000])
        self.add(test_2, test_3, test_4, test_5, test_6)
        test_7 = RadCurve(lambda t: 3*np.log(1+t), [0, 5*TAU, TAU/1000])
        self.add(test_7)
        """

        test_8 = RadCurve(lambda t: np.tan(t), [0, PI/2-PI/20, TAU/1000])
        test_8.add(test_8.copy().apply_function(lambda t: np.array([-t[0], t[1], 0])))
        cosh = FunctionGraph(lambda t: (np.exp(t)+np.exp(-t))/2, [0, 3, 0.01]).shift(DOWN)

        test_9 = RadCurve(lambda t: np.log((1+np.sin(t))/np.cos(t)), [0, PI/2-PI/20, TAU/1000], color = RED)
        int_tan = FunctionGraph(lambda t: -np.log(np.cos(t)), [0, 1, 0.01])

        self.add(test_8, test_9, cosh, int_tan)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

def ratio_color(colors: list, ratio: float):

    # colors = ["#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]
    # colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    # colors = [RED, YELLOW, GREEN, TEAL, BLUE, PURPLE]
    # colors = [TEAL, BLUE, BLUE, TEAL, GREEN, GREEN]
    # colors = [TEAL, BLUE, PURPLE, RED, YELLOW, GREEN]

    number_colors = len(colors) - 1
    # colors.append(colors[-1])
    if ratio >= 1:
        index = number_colors - 1
        interpolate = 1
    else:
        ratio = number_colors * ratio
        index = int(ratio)
        interpolate = ratio - index

    return interpolate_color(colors[index], colors[index+1], interpolate)

class Test_2(Scene):
    def construct(self):
        test_1 = RadCurve(np.sin, [0, TAU, TAU/1000])
        test_2 = RadCurve(lambda t: 2*np.sin(t), [0, TAU, TAU/1000])
        test_3 = RadCurve(lambda t: 2*np.sin(2*t), [0, TAU, TAU/1000])
        test_4 = RadCurve(lambda t: 2*np.sin(3*t), [0, TAU, TAU/1000])
        test_5 = RadCurve(lambda t: 2*np.sin(t/2), [0, TAU*2, TAU/1000])
        test_6 = RadCurve(lambda t: 2*np.sin(t/3), [0, TAU*3/2, TAU/1000])

        test_out = RadCurve(lambda t: 2*np.sin(t), [-TAU, TAU, DEGREES])
        list_out = [YELLOW, ORANGE, RED, PURPLE]
        mu_out = ValueTracker(0.0)
        def out_updater(mob: RadCurve):
            value = mu_out.get_value()
            k = 1 + 1/(2*max(value, 0.2))
            alpha = 1/(1+2*value)
            curve = RadCurve(lambda t: 1.5*np.sin(alpha*t), [0, k*PI, k*TAU/1000])
            curve_left = curve.copy().apply_function(lambda t: np.array([-t[0], t[1], 0])).reverse_points().append_points(curve.get_points())
            mob.set_points(curve_left.get_points()).set_color(ratio_color(list_out, value))
        test_out.add_updater(out_updater)

        test_in = RadCurve(lambda t: 2*np.sin(t), [-TAU, TAU, DEGREES])
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
        test_in.add_updater(in_updater)

        self.add(test_out, test_in)
        self.wait()
        # self.play(mu_out.animate.set_value(1.0), mu_in.animate.set_value(-0.5), run_time = 3)
        self.play(mu_out.animate.set_value(1.0), mu_in.animate.set_value(-1/3), run_time = 3)
        self.wait()
        

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

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

    def get_t_func(self):
        return self.t_func

    def get_function(self):
        if hasattr(self, "underlying_function"):
            return self.underlying_function
        if hasattr(self, "function"):
            return self.function

    def get_x_range(self):
        if hasattr(self, "x_range"):
            return self.x_range
        
class Test_3(Scene):
    def construct(self):
        """
        test_1 = RadCurve(np.sin, [0, TAU, TAU/1000])
        test_2 = RadCurve(lambda t: 2*np.sin(t), [0, TAU, TAU/1000])
        test_3 = RadCurve(lambda t: 2*np.sin(2*t), [0, TAU, TAU/1000])
        test_4 = RadCurve(lambda t: 2*np.sin(3*t), [0, TAU, TAU/1000])
        test_5 = RadCurve(lambda t: 2*np.sin(t/2), [0, TAU*2, TAU/1000])
        test_6 = RadCurve(lambda t: 2*np.sin(t/3), [0, TAU*3/2, TAU/1000])
        test_7 = RadCurve(lambda t: 3*np.log(1+t), [0, 5*TAU, TAU/1000])
        self.add(test_2, test_3, test_4, test_5, test_6)
        """
        """
        test_2 = RadParameterCurve(lambda t: np.array([2*np.sin(t), t]), [0, TAU, TAU/1000])
        test_3 = RadParameterCurve(lambda t: np.array([2*np.sin(2*t), t]), [0, TAU, TAU/1000])
        test_4 = RadParameterCurve(lambda t: np.array([2*np.sin(3*t), t]), [0, TAU, TAU/1000])
        test_5 = RadParameterCurve(lambda t: np.array([2*np.sin(t/2), t]), [0, TAU*2, TAU/1000])
        test_6 = RadParameterCurve(lambda t: np.array([2*np.sin(t/3), t]), [0, TAU*3/2, TAU/1000])
        """

        test_8 = RadParameterCurve(lambda t: np.array([np.sin(t), PI/2*np.cos(t)]), [PI/2, PI*3/2, TAU/1000])
        offset = test_8.get_end()
        test_9 = RadParameterCurve(lambda t: np.array([np.sin(t), PI/2*np.cos(t)]), [-PI/2, PI*3/2, TAU/1000]).shift(-offset)
        print(offset)
        
        
        self.add(test_9)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#######################################################

class Trailer(Scene):
    def construct(self):
        # title = Text("母函数", font = "simhei", color = YELLOW).scale(3)
        # title[0].move_to(5*LEFT + 2*UP)
        # title[1].move_to(5*LEFT)
        # title[2].move_to(5*LEFT + 2*DOWN)
        # function = MTex(r"{1}x^0+{1}x^1+{2}x^2+{3}x^3+{5}x^4+{8}x^5+{13}x^6+\cdots", tex_to_color_map = {(r"{1}", r"{2}", r"{3}", r"{5}", r"{8}", r"{13}"): BLUE, r"x": RED}).set_stroke(width = 8, color = BLACK, background = True).shift(1*RIGHT).rotate(-PI/6)
        # frac = MTex(r"\frac{1}{1-x-x^2}", tex_to_color_map = {r"x": RED}).scale(2).shift(1.8*DOWN + 1*LEFT)
        # # Fibonacci = Text("斐波那契数列", font = "simhei").scale(1.5).shift(2*UP + 3*RIGHT)
        # Fibonacci = MTex(r"f_{n+1} = f_{n}+f_{n-1}", tex_to_color_map = {(r"f_{n+1}", r"f_{n}", r"f_{n-1}"): BLUE}).scale(1.5).shift(2*UP + 3*RIGHT)
        # equal = MTex(r"\Leftrightarrow").scale(6).shift(1*RIGHT).rotate(PI/3)
        # self.add(title, equal, function, frac, Fibonacci)

        offset = 1.5*PI*LEFT
        lime = interpolate_color(BLUE, PURPLE_A, 0.5)
        color_1 = TEAL
        color_2 = TEAL
        color_3 = BLUE # "#5eb588"
        function_1 = lambda t: 1.5*np.array([2*t + np.sin(2*t), 1 - np.cos(2*t), 0])
        function_2 = lambda t: 1.5*np.array([2*t - np.sin(2*t), np.cos(2*t) - 1, 0])
        cycloid = ParametricCurve(function_1, [0, PI, PI/100], color = color_1, stroke_width = [0, 4, 7, 9, 10, 9, 7, 4, 0]).shift(offset)
        involute = ParametricCurve(function_2, [0, PI, PI/100], color = color_2, stroke_width = [0, 4, 7, 9, 10, 9, 7, 4, 0]).shift(offset)

        n = 18
        angle = PI/n
        lines = []
        for i in range(n-1):
            phase = (i+1)*angle
            ratio = abs((i+1)*2/n-1)
            line_i = Line(function_1(phase), function_2(phase), color = [color_1, color_2, color_2], stroke_width = 10*(1-ratio**2), stroke_opacity = (1-ratio**2)).shift(offset)
            lines.append(line_i)

        # text = Text("渐开线与摆线", font = "AaYuanHeiTi").scale(4/3).set_color(color_3)
        # text = Text("渐开线与摆线", font = "LXGW WenKai").scale(4/3).set_color(color_3)
        text = Text("渐开线与摆线", font = "FZDaHei-B02S").scale(4/3).set_color(color_3)
        place_l = 2.3*UP + 3.5*LEFT
        place_r = 2.3*UP + 3.5*RIGHT
        offset_l = 0.7*DOWN + 1.6*LEFT
        offset_r = 0.7*DOWN + 1.6*RIGHT
        text[1].scale(3).move_to(place_l)
        text[4].scale(3).move_to(place_r)
        text[0].move_to(place_l + offset_l)
        text[2].move_to(place_l + offset_r + 0.2*LEFT)
        text[3].move_to(place_r + offset_l)
        text[5].move_to(place_r + offset_r)
        self.add(*lines, cycloid, involute, text)
        

#######################################################
'''
class SwallowIn(Homotopy):
    CONFIG = {
        "run_time": 2,
        "remover": True, 
        "stretch": True, 
        "target": None,
        "norm_func": get_norm,
        "apply_function_kwargs": {}
    }

    def __init__(self, mobject: VMobject, **kwargs):
        digest_config(self, kwargs, locals())
        if self.target is None:
            self.target = mobject.get_center()
            self.apply_function_kwargs["about_point"] = self.target
        if self.stretch:
            self.scales = np.array([mobject.get_width() if mobject.get_width() else 1, 
                               mobject.get_height() if mobject.get_height() else 1, 
                               mobject.get_depth() if mobject.get_depth() else 1])
        else:
            self.scales = np.array([1, 1, 1])
        self.squishs = np.array([1/self.scales[0], 1/self.scales[1], 1/self.scales[2]])
        mobject.scale(self.squishs, about_point = self.target)
        max_distance = max(*[self.norm_func((mobject.get_corner(position)-self.target)) for position in [UL, UR, DL, DR]])
        
        def homotopy(x, y, z, t):
            position = np.array([x, y, z])
            distance_ratio = self.norm_func(position) / max_distance
            if t >= distance_ratio:
                return ORIGIN
            else:
                length = 1 - t/distance_ratio
                angle = np.log(length)
                rotation_matrix = np.array([unit(angle), unit(angle+PI/2), np.zeros(3)])
                moved = length * np.dot(position, rotation_matrix)
                return moved

        super().__init__(homotopy, mobject, **kwargs)

    def interpolate_submobject(
        self,
        submob: Mobject,
        start: Mobject,
        alpha: float
    ) -> None:
        super().interpolate_submobject(submob, start, alpha)
        submob.scale(self.scales, about_point = self.target)
'''

'''      
class SwallowIn(Homotopy):
    CONFIG = {
        "run_time": 2,
        "remover": True, 
        "target": None,
        "stretch": True, 
        "norm_func": get_norm,
        "speed": 1,
        "apply_function_kwargs": {}
    }

    def __init__(self, mobject: VMobject, **kwargs):
        digest_config(self, kwargs, locals())
        if self.target is None:
            self.target = mobject.get_center()
            self.apply_function_kwargs["about_point"] = self.target
        if self.stretch:
            scales = np.array([mobject.get_width() if mobject.get_width()>1e-8 else 1, 
                               mobject.get_height() if mobject.get_height()>1e-8 else 1, 
                               mobject.get_depth() if mobject.get_depth()>1e-8 else 1])
            def make_fn(fn, scales):
                return lambda t: fn(t / scales)
            self.norm_func = make_fn(self.norm_func, scales)
        else:
            scales = np.ones([3])
        
        max_distance = max(*[self.norm_func((mobject.get_corner(position)-self.target)) for position in [UL, UR, DL, DR]])
        
        def homotopy(x, y, z, t):
            position = np.array([x, y, z])
            distance_ratio = self.norm_func(position) / max_distance
            if t >= distance_ratio:
                return ORIGIN
            else:
                length = 1 - t/distance_ratio
                angle = np.log(length)*self.speed
                rotation_matrix = np.array([unit(angle), unit(angle+PI/2), np.zeros(3)])
                moved = length * np.dot(position/scales, rotation_matrix)*scales
                return moved

        super().__init__(homotopy, mobject, **kwargs)
'''

class Test_4(Scene):
    def construct(self):

        text_1 = r"\begin{pmatrix}\hat{r} \\ \hat{\theta}\end{pmatrix}"
        text_2 = r"=\begin{pmatrix}\cos\theta & \sin\theta \\ -\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}\hat\imath\\\hat\jmath\end{pmatrix}"
        text_3 = r"\Rightarrow\begin{pmatrix}\dot{\hat{r}}\\\dot{\hat{\theta}}\end{pmatrix}"
        text_4 = r"=\frac{d}{dt}\begin{pmatrix}\cos\theta & \sin\theta \\ -\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}\hat\imath\\\hat\jmath\end{pmatrix}"
        text_5 = r"=\begin{pmatrix}-\dot\theta\sin\theta & \dot\theta\cos\theta \\ -\dot\theta\cos\theta & -\dot\theta\sin\theta\end{pmatrix}\begin{pmatrix}\hat\imath\\\hat\jmath\end{pmatrix}"
        text_6 = r"=\dot\theta\begin{pmatrix}\hat{\theta} \\ -\hat{r}\end{pmatrix}"
        mtex_1 = MTex(text_1 + text_2 + text_3 + text_4 + text_5 + text_6).scale(0.5).next_to(3.6*UP + 7*LEFT)
        text_1 = r"\Rightarrow\vec{v}=\frac{d}{dt}\vec{r}=\frac{d}{dt}(r\hat{r})=\dot{r}\hat{r}+r\dot{\hat{r}}=\dot{r}\hat{r}+r\dot\theta\hat\theta"
        mtex_2 = MTex(text_1).scale(0.5).next_to(2.96*UP + 7*LEFT)
        text_1 = r"\Rightarrow\vec{a}=\frac{d}{dt}\vec{v}=\frac{d}{dt}(\dot{r}\hat{r}+r\dot\theta\hat\theta)"
        text_2 = r"=(\ddot{r}\hat{r}+\dot{r}\dot{\hat{r}})+(\dot{r}\dot{\theta}\hat{\theta}+r\ddot\theta\hat\theta+r\dot\theta(-\dot\theta\hat{r}))"
        text_3 = r"=(\ddot{r}-r\dot\theta^2)\hat{r}+(2\dot{r}\dot\theta+r\ddot\theta)\hat\theta=:a_r\hat{r}+a_\theta\hat\theta"
        mtex_3 = MTex(text_1 + text_2 + text_3).scale(0.5).next_to(2.32*UP + 7*LEFT)
        line_1 = Line(64/9*LEFT+1.9*UP, 64/9*RIGHT+1.9*UP).insert_n_curves(99)
        text_1 = r"\vec{F}=-\frac{GMm}{r^2}\hat{r}\Rightarrow\begin{cases}a_r=-\frac{GM}{r^2}\\a_\theta=0\end{cases}"
        text_2 = r"\Rightarrow 0=a_\theta=2\dot{r}\dot\theta+r\ddot\theta=\frac{1}{r}\frac{d}{dt}(r^2\dot\theta)\qquad\Rightarrow r^2\dot\theta = h"
        text_3 = r"\qquad\Rightarrow \frac{d}{dt}=\frac{d\theta}{dt}\frac{d}{d\theta}=\frac{h}{r^2}\frac{d}{d\theta}"
        mtex_4 = MTex(text_1 + text_2 + text_3).scale(0.5).next_to(1.4*UP + 7*LEFT)
        text_1 = r"u:=\frac{1}{r}\qquad \Rightarrow \dot{r}=\frac{d}{dt}\left(\frac{1}{u}\right)=-\frac{1}{u^2}\frac{d}{dt}u=-r^2\left(\frac{h}{r^2}\frac{du}{d\theta}\right)=-h\frac{du}{d\theta}"
        text_2 = r"\qquad \Rightarrow \ddot{r}=\frac{d}{dt}\dot{r}=\left(\frac{h}{r^2}\frac{d}{d\theta}\right)\left(-h\frac{du}{d\theta}\right)=-\frac{h^2}{r^2}\frac{d^2u}{d\theta^2}"
        mtex_5 = MTex(text_1 + text_2).scale(0.5).next_to(0.7*UP + 7*LEFT)
        text_1 = r"\Rightarrow -\frac{GM}{r^2}=a_r=\ddot{r}-r\dot\theta^2 = -\frac{h^2}{r^2}\frac{d^2u}{d\theta^2}-r\left(\frac{h}{r^2}\right)^2=-\frac{h^2}{r^2}\left(\frac{d^2u}{d\theta^2} + u\right)"
        text_2 = r"\qquad\Rightarrow \frac{d^2u}{d\theta^2}+u = \frac{GM}{h^2}"
        mtex_6 = MTex(text_1 + text_2).scale(0.5).next_to(7*LEFT)
        text_1 = r"\Rightarrow u=\frac{GM}{h^2}-A\cos(\theta + \phi)\qquad\Rightarrow "
        text_2 = r"r=\frac{ep}{1-e\cos(\theta + \phi)}"
        text_3 = r",\ (e, p):=\left(\frac{h^2}{GM}A,\ \frac{1}{A}\right)"
        mtex_7 = MTex(text_1 + text_2 + text_3, isolate = [text_2]).scale(0.5).next_to(0.7*DOWN + 7*LEFT)
        indicate_1 = SurroundingRectangle(mtex_7.get_part_by_tex(text_2))
        line_2 = Line(64/9*LEFT+1.15*DOWN, 64/9*RIGHT+1.15*DOWN).insert_n_curves(99)
        text_1 = r"\Rightarrow A=\frac{1}{p}=\frac{c}{b^2},\ h=\sqrt{GM\frac{e}{A}}=\sqrt{GM\frac{b^2}{a}} \qquad\Rightarrow "
        text_2 = r"r^2\dot\theta = \sqrt{GM\frac{b^2}{a}}"
        mtex_8 = MTex(text_1 + text_2, isolate = [text_2]).scale(0.5).next_to(1.6*DOWN + 7*LEFT)
        indicate_2 = SurroundingRectangle(mtex_8.get_part_by_tex(text_2))
        text_1 = r"\frac{1}{2}hT=S=\pi ab\qquad\Rightarrow T=\frac{2\pi ab}{h}=2\pi ab\sqrt{\frac{a}{GMb^2}}=\sqrt{\frac{4\pi^2 a^3}{GM}}\qquad\Rightarrow "
        text_2 = r"\frac{T^2}{a^3}=\frac{4\pi^2}{GM}"
        mtex_9 = MTex(text_1 + text_2, isolate = [text_2]).scale(0.5).next_to(2.4*DOWN + 7*LEFT)
        indicate_3 = SurroundingRectangle(mtex_9.get_part_by_tex(text_2))

        group_1 = VGroup(mtex_1, mtex_2, mtex_3)
        group_2 = VGroup(mtex_4, mtex_5, mtex_6, mtex_7)
        group_3 = VGroup(mtex_8, mtex_9)
        group_all = VGroup(mtex_1, mtex_2, mtex_3, line_1, mtex_4, mtex_5, mtex_6, mtex_7, indicate_1, line_2, mtex_8, indicate_2, mtex_9, indicate_3)
        # group_all.set_width(group_all.get_height(), stretch = True)

        self.add(group_all)
        self.wait()
        func_1 = lambda t: abs(t[0]) + abs(t[1]) + abs(t[2])
        func_2 = get_norm
        func_infty = lambda t: max(abs(t[0]), abs(t[1]), abs(t[2]))
        scales = np.array([group_all.get_width()/group_all.get_height(), 1, 1])
        # func_rectangle = lambda t: sum(((t[i]/scales[i])**2 for i in range(3)))**0.5
        # self.play(SwallowIn(group_all, norm_func = func_rectangle, speed = 1/np.sqrt(3)))
        self.play(SwallowIn(group_all, stretch = True))
        self.wait()

class Test_5(Scene):
    def construct(self):
        rectangle = Rectangle(width = 14, height = 6).insert_n_curves(76)
        rectangle.add(*[Rectangle(width = 13-i, height = 5-i).insert_n_curves(68-8*i) for i in range(5)])
        squares = VGroup(*[Square(side_length = 7-i).insert_n_curves((6-i)*4) for i in range(7)])
        self.add(squares)
        self.wait()
        func_1 = lambda t: abs(t[0]) + abs(t[1]) + abs(t[2])
        func_2 = get_norm
        func_infty = lambda t: max(abs(t[0]), abs(t[1]), abs(t[2]))
        self.play(SwallowIn(squares, norm_func = func_infty, speed = 1))
        self.wait()

class Test_6(Scene):
    def construct(self):

        group_all = Testboard()
        # group_all.set_width(group_all.get_height(), stretch = True)

        self.add(group_all)
        self.wait()
        func_1 = lambda t: abs(t[0]) + abs(t[1]) + abs(t[2])
        func_2 = get_norm
        func_infty = lambda t: max(abs(t[0]), abs(t[1]), abs(t[2]))
        scales = np.array([group_all.get_width()/group_all.get_height(), 1, 1])
        # func_rectangle = lambda t: sum(((t[i]/scales[i])**2 for i in range(3)))**0.5
        # self.play(SwallowIn(group_all, norm_func = func_rectangle, speed = 1/np.sqrt(3)))
        self.play(SwallowIn(group_all, stretch = True))
        self.wait()

#######################################################

class Toy_2(FrameScene):
    CONFIG = {
        "for_pr": False,
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }   

    def construct(self):
        radius = 0.8
        circle_out = Circle(radius = 4*radius, stroke_color = WHITE, stroke_width = 3)
        x_axis = Line(4*radius*LEFT, 4*radius*RIGHT)
        y_axis = Line(4*radius*UP, 4*radius*DOWN)
        function = lambda t: 4*radius*np.array([(np.cos(t))**3, (np.sin(t))**3, 0])
        astroid = ParametricCurve(function, [0, TAU, TAU/100], color = GREEN, stroke_width = 6).save_state()
        critical_angle = np.arccos(np.sqrt(2)/6) /2

        alpha = ValueTracker(0.0)
        circle_moving = Circle(radius = radius, stroke_color = BLUE, stroke_width = 3).shift(3*radius*RIGHT)
        point_moving = Dot(color = BLUE, radius = 0.05).shift(4*radius*RIGHT)
        line_moving = Line(4*radius*RIGHT, ORIGIN)
        
        self.play(ShowCreation(circle_out), PullOpen(x_axis), PullOpen(y_axis, along_axis = 1), ShowCreation(circle_moving), FadeIn(point_moving))

        def astroid_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function, [0, value, TAU/100])
            mob.set_points(curve.get_all_points())
            if value > TAU:
                mob.clear_updaters()
        astroid.add_updater(astroid_updater)
        def circle_updater(mob: Circle):
            value = alpha.get_value()
            mob.move_to(3*radius*unit(value))
            ratio = clip((value-critical_angle)/PI*2-2.5, 0, 1)
            mob.set_stroke(opacity = 1-ratio)
        circle_moving.add_updater(circle_updater)
        def point_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(function(value))
        point_moving.add_updater(point_updater)
        def line_updater(mob: Line):
            value = alpha.get_value()
            unit_vector = 4*radius*unit(value)
            mob.put_start_and_end_on(unit_vector[0]*RIGHT, unit_vector[1]*UP)
            ratio = clip((value-critical_angle)/PI*2-1.5, 0, 1)
            mob.set_stroke(opacity = ratio)
        line_moving.add_updater(line_updater)
        self.add(astroid, line_moving, point_moving).play(alpha.animate.set_value(TAU + critical_angle), rate_func = smooth_boot(1/6, 1/6), run_time = 4)
        self.remove(circle_moving)

        for mob in [astroid, circle_moving, point_moving, line_moving]:
            mob.clear_updaters()

        start_point = function(critical_angle)
        self.play(line_moving.animate.scale(0, about_point = start_point), rate_func = rush_into)

        function_1 = lambda t: radius*np.array([(3+np.sqrt(0.5))*np.cos(t)-2*(np.cos(t))**3, (3-np.sqrt(0.5))*np.sin(t)-2*(np.sin(t))**3, 0])
        astroid_base = astroid.copy().set_stroke(color = GREY, width = 4)
        semi_astroid = ParametricCurve(function, [critical_angle, PI-critical_angle, TAU/100], color = BLUE, stroke_width = 6).save_state()
        line_involute = Line(start_point, start_point, color = [BLUE, GREEN], stroke_width = 6)
        alpha.set_value(critical_angle)
        def astroid_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(lambda t: function(critical_angle + TAU - t), [0, critical_angle + TAU - value, PI/100])
            mob.set_points(curve.get_all_points())
        def involute_updater(mob: ParametricCurve):
            value = alpha.get_value()
            curve = ParametricCurve(function_1, [critical_angle, value, PI/100])
            mob.set_points(curve.get_all_points())
        def point_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(function_1(value))
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(function_1(value), function(value))
        astroid.add_updater(astroid_updater)
        semi_astroid.add_updater(involute_updater)
        point_moving.add_updater(point_updater)
        line_involute.add_updater(line_updater)
        self.bring_to_back(astroid_base).add(line_involute, semi_astroid, point_moving).play(alpha.animate.set_value(critical_angle + TAU), rate_func = smooth_boot(1/6), run_time = 4.5)
        
        for mob in [astroid, semi_astroid, point_moving, line_involute]:
            mob.clear_updaters()
        axes_copy = VGroup(x_axis, y_axis).copy()
        self.remove(astroid, line_involute).bring_to_back(axes_copy).play(semi_astroid.animate.scale(2), *[FadeOut(mob, scale = 2, shift = mob.get_center()) for mob in [axes_copy, circle_out, astroid_base, point_moving]])

        radius = 2*radius
        function_1 = lambda t: radius*np.array([(3+np.sqrt(0.5))*np.cos(t)-2*(np.cos(t))**3, (3-np.sqrt(0.5))*np.sin(t)-2*(np.sin(t))**3, 0])
        line_left = x_axis.copy().save_state()
        line_right = x_axis.copy().save_state()
        points = [Dot(function_1(angle), color = YELLOW) for angle in [PI*3/8, PI*5/8, -PI*3/8, -PI*5/8]]
        alpha = ValueTracker(0.0)
        def line_updater(multiple: float):
            def util(mob: Line):
                value = alpha.get_value()
                mob.restore().rotate(multiple*value).set_opacity(clip(value/PI, 0, 1))
            return util
        line_left.add_updater(line_updater(1))
        line_right.add_updater(line_updater(-1))
        self.add(line_left, line_right, semi_astroid).play(alpha.animate.set_value(PI - PI/8), rate_func = smooth_boot(1/6, -1/6), run_time = 1.4, frames = 42)
        for mob in [line_left, line_right]:
            mob.clear_updaters().set_color(YELLOW)
        self.add(*points)
        self.wait(0, 3)
        for mob in [line_left, line_right, *points]:
            mob.set_color(WHITE)

        point = Dot(function_1(0), color = YELLOW)
        line = Line(2*radius*unit(PI/8)*np.cos(PI/8), 2*radius*unit(-PI/8)*np.cos(PI/8), stroke_width = 6, color = YELLOW)
        line_extra = Line(radius*unit(PI/8)*np.cos(PI/8)+radius*unit(-PI/8)*np.cos(PI/8), function_1(0), stroke_width = 3, color = YELLOW)
        self.play(*[FadeOut(mob) for mob in [*points, x_axis, y_axis]], PullOpen(line, along_axis = 1), FadeIn(point))
        alpha = ValueTracker(0)
        def point_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(function_1(value))
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(2*radius*unit(PI/8)*np.cos(value-PI/8), 2*radius*unit(-PI/8)*np.cos(value+PI/8))
        def line_extra_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(radius*unit(PI/8)*np.cos(value-PI/8)+radius*unit(-PI/8)*np.cos(value+PI/8), function_1(value))
        point.add_updater(point_updater)
        line.add_updater(line_updater)
        line_extra.add_updater(line_extra_updater)
        self.play(alpha.animate.set_value(-PI/8))
        self.add(line_extra, line, point).play(alpha.animate.set_value(TAU), rate_func = smooth_boot(1/6, 0), run_time = 4)
        for mob in [line_extra, line, point]:
            mob.clear_updaters()
        shade = Shade(height = 8, width = 8, fill_color = BLACK)
        self.play(FadeIn(shade))
        self.clear()


#######################################################

class Template(Scene):
    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)