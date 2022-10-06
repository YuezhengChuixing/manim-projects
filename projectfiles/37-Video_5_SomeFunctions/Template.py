from manimlib import *
from typing import List, Union
import numpy as np

def quadratic(a,b,c):
    return lambda x: a*x*x + b*x + c

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def angle_color(angle):

    # colors = ["#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    # colors = [RED, YELLOW, GREEN, TEAL, BLUE, PURPLE]
    # colors = [TEAL, BLUE, BLUE, TEAL, GREEN, GREEN]
    # colors = [TEAL, BLUE, PURPLE, RED, YELLOW, GREEN]

    number_colors = len(colors)
    ratio = (number_colors * angle / TAU) % number_colors
    index = int(ratio)
    interpolate = ratio - index

    return interpolate_color(colors[index % number_colors], colors[(index+1) % number_colors], interpolate)

#####################################################################

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):

        super().__init__()
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

#####################################################################

class Float(Animation):
    CONFIG = {
        "squishing": None,
        "floating_func": linear,
        "rate_func": there_and_back,
        "scale_difference": 0.2,
        "about_point": None
    }

    def begin(self) -> None:
        if self.squishing is not None:
            self.floating_func = squish_rate_func(self.floating_func, *self.squishing)
            self.rate_func = squish_rate_func(self.rate_func, *self.squishing)
        super().begin()

    def interpolate(self, alpha: float) -> None:
        alpha = clip(alpha, 0, 1)
        self.interpolate_mobject(self.floating_func(alpha), self.rate_func(alpha))
        
    def interpolate_mobject(self, floating_alpha: float, fading_alpha: float) -> None:
        for sm1, sm2 in self.get_all_families_zipped():
            sm1.set_points(sm2.get_points())
        scale_factor = floating_alpha*2*self.scale_difference + (1-self.scale_difference)
        self.mobject.scale(scale_factor, about_point = self.about_point).set_opacity(fading_alpha)

class Test1(Scene):
    def construct(self):
        square = Square().shift(2*RIGHT)
        circle = Circle().shift(2*LEFT)
        text = Text("Template")
        self.play(Float(square), Float(circle, squishing = [0.4, 0.6]), run_time = 3)
        self.play(Float(circle))
        self.play(Float(text))
        print(self.num_plays, self.time)

class Eye(VGroup):
    CONFIG = {
        "color": WHITE,
        "outer_radius": 0.5,
        "medium_radius": 0.25,
        "inner_radius": 0.1,
        "looking_at": PI/4,
        "light_from": PI*3/4
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        outer = Circle(radius = self.outer_radius, fill_color = WHITE, fill_opacity = 1, stroke_width = 0)
        medium = Circle(radius = self.medium_radius, fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        inner = Circle(radius = self.inner_radius, fill_color = WHITE, fill_opacity = 1, stroke_width = 0)
        medium_shift = (self.outer_radius - self.medium_radius) * unit(self.looking_at)
        inner_shift = (self.medium_radius - self.inner_radius) * unit(self.light_from)
        medium.shift(medium_shift)
        inner.shift(medium_shift + inner_shift)
        self.add(outer, medium, inner)
        
class Mouth(ArcBetweenPoints):
    def __init__(self, upper_angle = -PI/3, **kwargs):
        super().__init__(angle=PI/2, start = LEFT, end = RIGHT, fill_color = BLACK, fill_opacity = 1, stroke_width = 0, **kwargs)
        another = ArcBetweenPoints(angle = upper_angle, start = RIGHT, end = LEFT)
        self.append_points(another.get_points())

class Drop(ArcBetweenPoints):
    def __init__(self, **kwargs):
        super().__init__(angle=PI*4/3, start = unit(PI*3/2-PI/12), end = unit(PI*3/2+PI/12), fill_color = WHITE, fill_opacity = 1, stroke_width = 0, **kwargs)
        self.add_line_to(ORIGIN).add_line_to(unit(PI*3/2-PI/12))

class SpringUp(LaggedStart):
    CONFIG = {
        "lag_ratio": None,
        "side_length": None,
        "from_center": True
    }
    def __init__(self, mobject_or_point: Union[Mobject, np.ndarray], texts: List[str], **kwargs):
        digest_config(self, kwargs)
        self.set_default_config_from_length(len(texts))

        if isinstance(mobject_or_point, Mobject):
            base = mobject_or_point.get_corner(DL)
            center = mobject_or_point.get_center()
            height = mobject_or_point.get_height()
            width = mobject_or_point.get_width()
        else:
            if self.side_length is None:
                self.side_length = 1
            center = mobject_or_point
            base = center + self.side_length * DL / 2
            height = self.side_length
            width = self.side_length
        if not self.from_center:
            center = None

        mob_texts = [TexText(text).scale(0.5).shift(base + np.array([random.random()*height, random.random()*width, 0])) for text in texts]
        super().__init__(*[Float(text, about_point = center) for text in mob_texts], **kwargs)

    def set_default_config_from_length(self, length: int) -> None:
        if self.lag_ratio is None:
            self.lag_ratio = min(4.0 / (length + 1.0), 0.2)

class Test2(Scene):
    def construct(self):
        text_sigma = Tex(r"\sigma", color = BLUE).scale(10)
        left_eye = Eye(looking_at = PI*7/6).scale(0.5).shift(1.35*UP+0.1*RIGHT)
        right_eye = Eye(looking_at = PI/3).scale(0.5).shift(1.35*UP+0.8*RIGHT)
        mouth = Mouth().scale(0.3, about_point = ORIGIN).shift(1.05*UP + 0.45*RIGHT)
        drool = Drop().scale(0.2, about_point = ORIGIN).shift(1.05*UP + 0.15*RIGHT)
        sigma_chan = VGroup(left_eye, right_eye, text_sigma, mouth, drool)
        shade = BackgroundRectangle(sigma_chan, fill_color = "#333333", fill_opacity = 1).scale(1.2)
        self.add(sigma_chan, shade)
        
        texts = ["我是谁", "我在哪", "e是什么", "d又是什么", "我可爱的替换加密呢", "为什么是数论", "这和加密有什么关系"]
        texts += texts
        anim1 = SpringUp(sigma_chan, texts, rate_func = squish_rate_func(smooth, 0.2, 1))
        anim2 = FadeOut(shade, rate_func = there_and_back_with_pause(0.6), remover = False)
        sigma_chan.scale(0.8)
        self.play(anim1, anim2, ApplyMethod(sigma_chan.scale, 1.5), run_time = 5)
        self.wait(1)
        self.play(SpringUp(RIGHT, texts, side_length = 2), run_time = 4)
        self.wait(1)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Test6(Scene):
    def construct(self):
        text_sigma = Tex(r"\sigma", color = BLUE).insert_n_curves(100).scale(10)
        left_eye = Eye(looking_at = PI/3).scale(0.5).shift(1.35*UP+0.1*RIGHT)
        right_eye = Eye(looking_at = PI/3).scale(0.5).shift(1.35*UP+0.8*RIGHT)
        mouth = Mouth().scale(0.2, about_point = ORIGIN).shift(1.05*UP + 0.45*RIGHT)
        sigma_chan = VGroup(left_eye, right_eye, text_sigma, mouth)
        def raise_hand(point: np.ndarray):
            if point[0] < 0.8:
                return point
            else:
                return point + (point[0]-0.8)**2 *UP
        copy_sigma = text_sigma.copy()
        copy_sigma.apply_function(raise_hand)
        happy = Mouth(upper_angle = -PI/6).scale(0.2, about_point = ORIGIN).shift(1.05*UP + 0.45*RIGHT)
        sigma_chan_copy = VGroup(left_eye, right_eye, copy_sigma, happy)
        
        self.add(sigma_chan)
        self.wait(1)
        self.play(Transform(sigma_chan, sigma_chan_copy))
        self.wait(1)
        
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#####################################################################

class Test3(Scene):
    def construct(self):
        carrot = SVGMobject("Sleep_Carrot.svg", should_center = False, height = None).move_to(100*UP + 200*LEFT)
        bubble = SVGMobject("Sleep_Bubble.svg", should_center = False, height = None).move_to(85*UP + 195*LEFT)
        bunny = SVGMobject("Sleep_Bunny.svg", should_center = False, height = None).move_to(ORIGIN)
        group = VGroup(carrot, bubble, bunny).scale(0.02, about_point = ORIGIN)
        self.add(group)
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Test4(Scene):
    def construct(self):
        # text_sigma = Tex(r"\sigma", color = BLUE).scale(10)
        # left_eye = Eye(looking_at = PI*7/6).scale(0.5).shift(1.35*UP+0.1*RIGHT)
        # right_eye = Eye(looking_at = PI/3).scale(0.5).shift(1.35*UP+0.8*RIGHT)
        # mouth = Mouth().scale(0.3, about_point = ORIGIN).shift(1.05*UP + 0.45*RIGHT)
        # drool = Drop().scale(0.2, about_point = ORIGIN).shift(1.05*UP + 0.15*RIGHT)
        # sigma_chan = VGroup(left_eye, right_eye, text_sigma, mouth, drool).scale(0.5).move_to(2*UP + 4*LEFT)

        carrot = SVGMobject("Sleep_Carrot.svg", should_center = False, height = None).move_to(100*UP + 200*LEFT)
        bubble = SVGMobject("Sleep_Bubble.svg", should_center = False, height = None).move_to(85*UP + 195*LEFT)
        bunny = SVGMobject("Sleep_Bunny.svg", should_center = False, height = None).move_to(ORIGIN)
        group = VGroup(bubble, bunny).scale(0.02, about_point = ORIGIN)
        # iter1 = group.copy().scale(0.25).move_to(2*UP + 4*LEFT)
        # iter2 = VGroup(group, iter1).copy().scale(0.25).move_to(2*UP + 4*LEFT)
        # iter3 = VGroup(group, iter2).copy().scale(0.25).move_to(2*UP + 4*LEFT)
        self.add(group)
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#####################################################################

class Gear(VMobject):
    CONFIG = {
        "major_radius": 1.0,
        "minor_radius": 0.8,
        "n_teeth": 17,
        "width_ratio": 2/3
    }
    def init_points(self) -> None:
        self.set_points(Gear.create_quadratic_bezier_points(
            major_radius=self.major_radius,
            minor_radius=self.minor_radius,
            n_teeth=self.n_teeth,
            width_ratio=self.width_ratio
        ))

    def create_quadratic_bezier_points(major_radius: float = 1.0, minor_radius: float = 0.8, n_teeth: int = 17, width_ratio: float = 2/3) -> np.ndarray:

        major_width_angle = TAU/(n_teeth)*(width_ratio/2)
        minor_width_angle = TAU/(n_teeth)*((1-width_ratio)/2)
        step_angle = TAU/(4*n_teeth)
        angle_sequence = np.linspace(PI/2, -3*PI/2, n_teeth + 1)

        major_negative = np.array([major_radius * unit(a + major_width_angle) / np.cos(step_angle) for a in angle_sequence])
        major_center = np.array([major_radius * unit(a) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])
        major_positive = np.array([major_radius * unit(a - major_width_angle) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])
        
        minor_negative = np.array([minor_radius * unit(a + minor_width_angle - 2*step_angle) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])
        minor_center = np.array([minor_radius * unit(a - 2*step_angle) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])
        minor_positive = np.array([minor_radius * unit(a - minor_width_angle - 2*step_angle) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])

        positions = np.zeros((12 * n_teeth, 3))
        positions[0::12] = major_negative[0:-1]
        positions[1::12] = major_center
        positions[2::12] = major_positive
        positions[3::12] = major_positive
        positions[4::12] = (major_positive + minor_negative)/2
        positions[5::12] = minor_negative
        positions[6::12] = minor_negative
        positions[7::12] = minor_center
        positions[8::12] = minor_positive
        positions[9::12] = minor_positive
        positions[10::12] = (minor_positive + major_negative[1:])/2
        positions[11::12] = major_negative[1:]
        return positions

class Test5(Scene):
    def construct(self):

        mark_outer = Circle(radius = 3.6, color = WHITE)
        mark_inner = Circle(radius = 3.5, color = WHITE)
        number = 66
        marks = VGroup()
        for i in range (number):
            angle = i * TAU / number
            mark_i = Line(3.5*unit(angle), 3.6*unit(angle))
            marks.add(mark_i)
        marks.add(mark_outer, mark_inner)

        number_letters = 26

        outer_text = VGroup()
        outer_number = VGroup()
        for i in range (number_letters):
            angle = i * TAU / number_letters
            text_i = Text(chr(65 + i), font = 'Times New Roman').scale(0.8).shift(3.1*UP).rotate(-angle, about_point = ORIGIN)
            number_i = Text("%d"%i, font = 'Times New Roman').scale(0.8).shift(3.1*UP).rotate(-angle, about_point = ORIGIN).set_opacity(0)
            outer_text.add(text_i)
            outer_number.add(number_i)

        gear_outer = Circle(radius = 2.7, color = WHITE)
        gear_inner = Gear(major_radius = 2.6, minor_radius = 2.48, n_teeth = number_letters)
        outer_gear = VGroup(gear_outer, gear_inner)
        outer_layer = VGroup(marks, outer_text, outer_gear, outer_number)

        gear_outer = Gear(major_radius = 2.52, minor_radius = 2.4, n_teeth = number_letters, width_ratio = 1/2, fill_opacity = 1, fill_color = "#333333", stroke_color = YELLOW_E)
        gear_inner = Circle(radius = 2.3, color = YELLOW_E)
        inner_gear = VGroup(gear_outer, gear_inner)

        inner_text = VGroup()
        inner_number = VGroup()
        for i in range (number_letters):
            angle = i * TAU / number_letters
            text_i = Text(chr(65 + i), font = 'Times New Roman', color = YELLOW_E).scale(0.7).shift(1.9*UP).rotate(-angle, about_point = ORIGIN)
            number_i = Text("%d"%i, font = 'Times New Roman', opacity = 0, color = YELLOW_E).scale(0.6).shift(1.9*UP).rotate(-angle, about_point = ORIGIN).set_opacity(0)
            inner_text.add(text_i)
            inner_number.add(number_i)

        
        mark_outer = Circle(radius = 1.5, color = YELLOW_E)
        mark_inner = Circle(radius = 1.4, color = YELLOW_E)
        number = 66
        marks = VGroup()
        for i in range (number):
            angle = i * TAU / number
            mark_i = Line(1.5*unit(angle), 1.4*unit(angle), color = YELLOW_E)
            marks.add(mark_i)
        marks.add(mark_outer, mark_inner)
        inner_layer = VGroup(inner_gear, inner_text, marks, inner_number).rotate(3*TAU/26)



        self.add(outer_layer, inner_layer)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#####################################################################

class Cloud(ArcBetweenPoints):
    def __init__(self, **kwargs):
        super().__init__(angle=PI, start = RIGHT, end = RIGHT + 1.2*UP, fill_color = GREY, fill_opacity = 1, stroke_width = 0, **kwargs)
        another = ArcBetweenPoints(angle=PI*5/6, start = RIGHT + 1.2*UP, end = LEFT + 1.5*UP)
        self.append_points(another.get_points())
        another = ArcBetweenPoints(angle=PI, start = LEFT + 1.5*UP, end = LEFT)
        self.append_points(another.get_points()).close_path()
        

class Test7(Scene):
    def construct(self):

        base = Line(2.1*DOWN+3*LEFT, 2.1*DOWN + 3*RIGHT, stroke_width = 6)
        building = Rectangle(height = 4.2, width = 3, stroke_width = 6)
        window = Square(side_length = 0.5)
        for i in range(4):
            for j in range(3):
                if i != 0 or j != 1:
                    building.add(window.copy().shift((i-1.5)*0.9*UP + (j-1)*0.9*RIGHT))
        door = Rectangle(width = 0.5, height = 1.0).shift(1.6*DOWN)
        building.add(door)
        copy_building = building.copy()

        alpha = ValueTracker(0.0)
        def building_update(mob: VMobject):
            a = alpha.get_value()
            unit_vec = unit(a * PI / 2)
            direction = np.array([0.5*unit_vec[0], unit_vec[1], 0])
            def util(point: np.ndarray):
                return np.array([point[0], -2.1, 0]) + (point[1] + 2.1) * direction
            mob.become(copy_building)
            mob.apply_function(util)
        building.add_updater(building_update)
        self.add(base, building)
        self.play(alpha.animate.set_value(1.0))
        building.clear_updaters()
        self.wait(1)

        basement = Rectangle(height = 0.8, width = 3, stroke_width = 6, stroke_color = YELLOW_E).shift(2.5*DOWN)
        baseline = Line(2.1*DOWN+2*LEFT, 2.1*DOWN + 2*RIGHT, stroke_width = 6)
        building.add(basement, baseline)
        hole = basement.copy()
        self.add(hole)
        self.play(Rotate(building, about_point = 2.1*DOWN + 2*LEFT, angle = PI - np.arctan(4.2/0.5)), rate_func = linear, run_time = 0.5)
        self.wait(1)
        building.add(base, hole)
        copy_building.add(base.copy())
        new_building = copy_building.copy().shift(3*RIGHT + 7*UP)
        anim = ApplyMethod(new_building.shift, 7*DOWN, rate_func = squish_rate_func(rush_into, 0.5, 1))
        self.play(building.animate.shift(2*LEFT), anim)
        self.wait(1)

        cloud_quantum = Cloud().add(Text("量子力学", font = "simhei").shift(0.7*UP)).scale(0.7).shift(1.8*RIGHT).save_state()
        cloud_relativity = Cloud().add(Text("相对论", font = "simhei").shift(0.7*UP)).scale(0.7).shift(4.2*RIGHT + UP).save_state()
        building_physics = copy_building.copy().shift(3*RIGHT).save_state()
        velocity = 0.3
        alpha = ValueTracker(0.0)
        def updater_cloud(direction: np.ndarray):
            def util(mob: VMobject, dt):
                scale_factor = alpha.get_value()
                mob.restore().shift(dt * velocity * direction).save_state()
                mob.scale(scale_factor, about_point = 7*RIGHT + 3*DOWN)
            return util
        def updater_building(mob: VMobject):
            scale_factor = alpha.get_value()
            mob.restore().scale(scale_factor, about_point = 7*RIGHT + 3*DOWN)
        building_physics.add_updater(updater_building)
        cloud_quantum.add_updater(updater_cloud(RIGHT))
        cloud_relativity.add_updater(updater_cloud(LEFT))

        self.add(building_physics, cloud_quantum, cloud_relativity)
        self.play(building.animate.scale(0.7, about_point = 7*LEFT + 3*UP), new_building.animate.scale(0.7, about_point = 7*LEFT + 3*UP), alpha.animate.set_value(0.7))
        self.wait(3)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#####################################################################

class Keypad(VGroup):
    def __init__(self):

        number_marks = 66
        number_letters = 26

        outer_radius_2 = 2.9
        outer_radius_1 = outer_radius_2 + 0.1
        outer_radius_4 = 2.2
        outer_radius_3 = (outer_radius_2 + outer_radius_4)/2
        mark_outer_1 = Circle(radius = outer_radius_1)
        mark_outer_2 = Circle(radius = outer_radius_2)
        marks_outer = VGroup(mark_outer_1, mark_outer_2)
        for i in range (number_marks):
            angle = i * TAU / number_marks
            mark_i = Line(outer_radius_2*unit(angle), outer_radius_1*unit(angle))
            marks_outer.add(mark_i)
        text_outer = VGroup()
        fence_outer = VGroup()
        for i in range (number_letters):
            angle = i * TAU / number_letters
            text_i = Text(chr(65 + i), font = 'Times New Roman').scale(0.7).shift(outer_radius_3*UP).rotate(-angle, about_point = ORIGIN)
            text_outer.add(text_i)
            fence_i = Line(outer_radius_2*unit(angle + PI/2 + PI/number_letters), outer_radius_4*unit(angle + PI/2 + PI/number_letters))
            fence_outer.add(fence_i)
        bound_outer = Circle(radius = outer_radius_4)
        outer_layer = VGroup(marks_outer, text_outer, bound_outer, fence_outer).set_color(WHITE)

        inner_radius_4 = 2.1
        inner_radius_2 = 1.6
        inner_radius_3 = (inner_radius_4 + inner_radius_2)/2
        inner_radius_1 = inner_radius_2 - 0.1
        bound_inner = Circle(radius = inner_radius_4, color = YELLOW_E)
        text_inner = VGroup()
        fence_inner = VGroup()
        for i in range (number_letters):
            angle = i * TAU / number_letters
            text_i = Text(chr(65 + i), font = 'Times New Roman').scale(0.5).shift(inner_radius_3*UP).rotate(-angle, about_point = ORIGIN)
            text_inner.add(text_i)
            fence_i = Line(inner_radius_4*unit(angle + PI/2 + PI/number_letters), inner_radius_2*unit(angle + PI/2 + PI/number_letters))
            fence_inner.add(fence_i)
        mark_inner_1 = Circle(radius = inner_radius_2, color = WHITE)
        mark_inner_2 = Circle(radius = inner_radius_1, color = WHITE)
        marks_inner = VGroup(mark_inner_1, mark_inner_2)
        for i in range (number_marks):
            angle = i * TAU / number_marks
            mark_i = Line(inner_radius_2*unit(angle), inner_radius_1*unit(angle))
            marks_inner.add(mark_i)
        inner_layer = VGroup(marks_inner, text_inner, bound_inner, fence_inner).set_color(YELLOW_E)

        super().__init__(outer_layer, inner_layer)
        self.set_stroke(background = True)
        self.outer = outer_layer
        self.inner = inner_layer
        self.message = text_outer
        self.cypher = text_inner
        self.number_letters = number_letters
        self.outer_bound = outer_radius_4
        self.inner_bound = inner_radius_4

        self.tips = VGroup()
        self.add(self.tips)
        self.is_encrypting = False
        self.is_decrypting = False

    def get_highlights(self):

        self.highlight_message = VGroup(*[VHighlight(mob, n_layers=4, max_stroke_width=12.0) for mob in self.message]).set_stroke(opacity = 0)
        self.highlight_cypher = VGroup(*[VHighlight(mob, n_layers=4, max_stroke_width=12.0) for mob in self.cypher]).set_stroke(opacity = 0)
        self.outer.add(self.highlight_message)
        self.inner.add(self.highlight_cypher)

        return self.highlight_message, self.highlight_cypher
        
    def get_handle(self, center = ORIGIN):

        if self.is_decrypting:
            return

        self.handle = ValueTracker(0.0)
        self.standard_inner = self.inner.copy()
        self.rotating_center = center
        def updater_rotating(mob: Keypad):
            angle = TAU/self.number_letters * self.handle.get_value()
            mob.inner.become(self.standard_inner).rotate(angle, about_point = center)
        self.add_updater(updater_rotating)

        return self.handle

    def encrypt(self, *letters):

        if not hasattr(self, "handle"):
            self.get_handle()

        self.orders = [ord(letter) - 65 for letter in letters]
        self.tips.become(VGroup())
        for order in self.orders:
            tip = Triangle(fill_color = RED, fill_opacity = 1, stroke_width = 0).scale(0.1).rotate(PI).next_to(self.outer_bound * UP, DOWN, buff = 0).rotate(- order * TAU / self.number_letters, about_point = ORIGIN).shift(self.rotating_center)
            self.tips.add(tip)
        
        def updater_highlight(mob: Keypad):
            tick = mob.handle.get_value()
            for order in range(mob.number_letters):
                if order in mob.orders:
                    mob.highlight_message[order].set_stroke(opacity = 1)
                else:
                    mob.highlight_message[order].set_stroke(opacity = 0)
                if round(order - tick) % 26 in mob.orders:
                    mob.highlight_cypher[order].set_stroke(opacity = 1)
                else:
                    mob.highlight_cypher[order].set_stroke(opacity = 0)
        if not self.is_encrypting:
            self.add_updater(updater_highlight)
            self.is_encrypting = True
        return self

    def get_outer_handle(self, center = ORIGIN):

        if self.is_encrypting:
            return

        self.handle = ValueTracker(0.0)
        self.standard_outer = self.outer.copy()
        self.rotating_center = center
        def updater_rotating(mob: Keypad):
            angle = TAU/self.number_letters * self.handle.get_value()
            mob.outer.become(self.standard_outer).rotate(angle, about_point = center)
        self.add_updater(updater_rotating)

        return self.handle

    def decrypt(self, *letters):

        if not hasattr(self, "handle"):
            self.get_outer_handle()

        self.orders = [ord(letter) - 65 for letter in letters]
        self.tips.become(VGroup())
        for order in self.orders:
            tip = Triangle(fill_color = RED, fill_opacity = 1, stroke_width = 0).scale(0.1).next_to(self.inner_bound * UP, UP, buff = 0).rotate(- order * TAU / self.number_letters, about_point = ORIGIN).shift(self.rotating_center)
            self.tips.add(tip)
        
        def updater_highlight(mob: Keypad):
            tick = mob.handle.get_value()
            for order in range(mob.number_letters):
                if order in mob.orders:
                    mob.highlight_cypher[order].set_stroke(opacity = 1)
                else:
                    mob.highlight_cypher[order].set_stroke(opacity = 0)
                if round(order - tick) % 26 in mob.orders:
                    mob.highlight_message[order].set_stroke(opacity = 1)
                else:
                    mob.highlight_message[order].set_stroke(opacity = 0)
        if not self.is_decrypting:
            self.add_updater(updater_highlight)
            self.is_decrypting = True
        return self

class Test8(Scene):
    def construct(self):

        keypad = Keypad()
        m,c = keypad.get_highlights()
        # keypad.add_to_back(*m, *c)
        self.add(keypad)
        self.wait(1)
        handle = keypad.get_handle()
        keypad.encrypt("B", "U", "N", "Y")
        self.wait(1)
        self.play(handle.animate.set_value(3.0), run_time = 2)
        self.wait(1)
        self.play(handle.animate.set_value(8.0), run_time = 2)
        self.wait(1)
        self.play(handle.animate.set_value(17.0), run_time = 2)
        self.wait(1)

        keypad.encrypt("S", "T", "R", "O", "N", "G")
        self.wait(1)
        self.play(handle.animate.set_value(12.0), run_time = 2)
        self.wait(1)


        print(self.num_plays, self.time)

class Test9(Scene):
    def construct(self):

        keypad = Keypad()
        m,c = keypad.get_highlights()
        # keypad.add_to_back(*m, *c)
        self.add(keypad)
        self.wait(1)
        handle = keypad.get_outer_handle()
        keypad.decrypt("W", "E", "A", "K")
        self.wait(1)
        self.play(handle.animate.set_value(3.0), run_time = 2)
        self.wait(1)
        self.play(handle.animate.set_value(8.0), run_time = 2)
        self.wait(1)
        self.play(handle.animate.set_value(17.0), run_time = 2)
        self.wait(1)

        keypad.decrypt("S", "T", "R", "O", "N", "G")
        self.wait(1)
        self.play(handle.animate.set_value(12.0), run_time = 2)
        self.wait(1)


        print(self.num_plays, self.time)



    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#####################################################################

def ellipse_unit(angle, a=1, b=1/2):
    return np.array([a*np.cos(angle), b*np.sin(angle), 0])

class RollUp(Homotopy):
    CONFIG = {
        "run_time": 3,
        "remover": True,
        "major": 0.5,
        "minor": 0.25
    }

    def __init__(self, mobject, left_bound = -8, right_bound = 8, **kwargs):
        digest_config(self, kwargs, locals())
        a = self.major
        b = self.minor
        def homotopy(x, y, z, t):
            
            bottom = t * left_bound + (1-t) * right_bound
            if x <= bottom:
                return np.array([x, y, 0])
            else:
                angle = (x - bottom) / a
                return np.array([bottom, y, 0]) + b*UP + ellipse_unit(-PI/2 + angle, a, b)

        super().__init__(homotopy, mobject, **kwargs)

class Testboard(VGroup):
    def __init__(self):
        
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
        line_1 = Line(64/9*LEFT+1.9*UP, 64/9*RIGHT+1.9*UP).insert_n_curves(64)
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
        line_2 = Line(64/9*LEFT+1.15*DOWN, 64/9*RIGHT+1.15*DOWN).insert_n_curves(64)
        text_1 = r"\Rightarrow A=\frac{1}{p}=\frac{c}{b^2},\ h=\sqrt{GM\frac{e}{A}}=\sqrt{GM\frac{b^2}{a}} \qquad\Rightarrow "
        text_2 = r"r^2\dot\theta = \sqrt{GM\frac{b^2}{a}}"
        mtex_8 = MTex(text_1 + text_2, isolate = [text_2]).scale(0.5).next_to(1.6*DOWN + 7*LEFT)
        text_1 = r"\frac{1}{2}hT=S=\pi ab\qquad\Rightarrow T=\frac{2\pi ab}{h}=2\pi ab\sqrt{\frac{a}{GMb^2}}=\sqrt{\frac{4\pi^2 a^3}{GM}}\qquad\Rightarrow "
        text_2 = r"\frac{T^2}{a^3}=\frac{4\pi^2}{GM}"
        mtex_9 = MTex(text_1 + text_2, isolate = [text_2]).scale(0.5).next_to(2.4*DOWN + 7*LEFT)

        super().__init__(mtex_1, mtex_2, mtex_3, line_1, mtex_4, mtex_5, mtex_6, mtex_7, line_2, mtex_8, mtex_9)

class Test10(Scene):
    def construct(self):
        
        group_all = Testboard()
        
        self.add(group_all)
        self.wait(1)
        self.play(RollUp(group_all))
        self.wait(1)
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class UnRolled(Homotopy):
    CONFIG = {
        "run_time": 3,
        "major": 0.5,
        "minor": 0.25
    }

    def __init__(self, mobject, left_bound = -8, right_bound = 8, **kwargs):
        digest_config(self, kwargs, locals())
        a = self.major
        b = self.minor
        def homotopy(x, y, z, t):
            
            bottom = t * left_bound + (1-t) * right_bound
            if x >= bottom:
                return np.array([x, y, 0])
            else:
                angle = (x - bottom) / a
                return np.array([bottom, y, 0]) + b*UP + ellipse_unit(-PI/2 + angle, a, b)

        super().__init__(homotopy, mobject, **kwargs)

class Test13(Scene):
    def construct(self):
        
        group_all = Testboard()
        
        self.play(UnRolled(group_all))
        self.wait(1)
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)
        
#####################################################################

def bounce(t: float):
    return 1- abs(bezier([0, 0, 0, 1.5, 1.5, 1])(t) - 1)

def double_bounce(t: float):
    return 1- abs(bezier([0, 0, 0, 1.6, 1.6, 0.9, 0.9, 1])(t) - 1)


class Test11(Scene):
    def construct(self):

        square = Square(side_length = 1).shift(0.5*UR)
        graph = FunctionGraph(double_bounce, [0, 1, 0.02])
        self.add(square, graph)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Test12(Scene):
    def construct(self):

        ball = Circle().shift(2*UP)
        self.add(ball)
        self.wait(1)
        self.play(ball.animate.shift(4*DOWN), rate_func = bounce)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#####################################################################

class Block(VGroup):
    def __init__(self, shifting):
        
        block = Rectangle(width = 1.1, height = 0.5, stroke_color = BLUE, fill_opacity = 1, fill_color = interpolate_color("#333333", BLUE, 0.2))
        cypher = "{" + chr(ord("a")+shifting) + "}"
        text = MTex("a\leftrightarrow " + cypher, tex_to_color_map = {"\leftrightarrow": GREEN, cypher: YELLOW_E}).scale(0.6)
        text.shift( -(text[1].get_center()) )

        super().__init__(block, text)

class Test14(Scene):
    def construct(self):

        mark_outer = Circle(radius = 3.6, stroke_color = WHITE, fill_color = "#333333", fill_opacity = 1).scale(0.6)
        blocks = []
        block_per_layer = [2, 3, 4, 4, 4, 4, 3, 2]
        order = 0
        for i in range(8):
            number = block_per_layer[i]
            for j in range(number):
                block_i = Block(order).shift(0.6*UP*(i-3.5) + 1.2*RIGHT*(j-(number-1)/2))
                blocks.append(block_i)
                order += 1
        self.add(mark_outer, *blocks)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Test15(Scene):
    def construct(self):
        squares_1 = []
        squares_2 = []
        text_1 = Text("变透明度", font = "simsun").shift(1.5*UP)
        text_2 = Text("颜色插值", font = "simsun").shift(1.5*DOWN)
        for i in range(11):
            square_1 = Square(side_length = 1, fill_opacity = i/10, stroke_width = 0, fill_color = BLUE).shift(0.5*UP+(i-5)*RIGHT)
            squares_1.append(square_1)
            square_2 = Square(side_length = 1, fill_opacity = 1, stroke_width = 0, fill_color = interpolate_color("#333333", BLUE, i/10)).shift(0.5*DOWN+(i-5)*RIGHT)
            squares_2.append(square_2)
        self.add(*squares_1, *squares_2, text_1, text_2)

#####################################################################

class Test16(Scene):
    def construct(self):

        square_1 = Square().shift(2*UL)
        circle_1 = Circle().shift(2*UR)
        square_2 = Square(color = BLUE).shift(2*DL)
        circle_2 = Circle(color = YELLOW).shift(2*DR)

        self.wait(1)
        self.play(ShowCreation(square_1), ShowCreation(circle_1, squish_interval = (0.4, 0.6)), run_time = 2)
        self.wait(1)
        self.play(Transform(square_1, square_2), Transform(circle_1, circle_2, squish_interval = (0.4, 0.6)), run_time = 2)
        self.wait(1)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#####################################################################

class ParallelLink(FunctionGraph):

    def __init__(self, start_point: np.ndarray, end_point: np.ndarray, **kwargs):
        super().__init__(smooth, [0, 1, 0.02], **kwargs)
        self.start_point = start_point
        self.end_point = end_point
        self.scale(end_point - start_point, min_scale_factor = -np.inf, about_point = ORIGIN).shift(start_point)


class ParallelLine(VMobject):

    def __init__(self, start_point: np.ndarray, end_point: np.ndarray, **kwargs):
        self.start_point = start_point
        self.end_point = end_point
        VMobject.__init__(self, **kwargs)

    def init_points(self) -> None:
        
        start_point = self.start_point
        end_point = self.end_point
        middle_point = (start_point + end_point)/2
        horizontal_difference = start_point[0] - end_point[0]
        vertical_difference = start_point[1] - end_point[1]
        if abs(horizontal_difference) >= 10/3*abs(vertical_difference):
            handle_moving = horizontal_difference * abs(vertical_difference) / abs(horizontal_difference)
            handle_moving = (handle_moving + horizontal_difference*0.3) / 2
        else:
            handle_moving = horizontal_difference * 0.3
        
        start_handle = start_point + handle_moving * LEFT
        end_handle = end_point + handle_moving * RIGHT
        self.set_points([start_point, start_handle, middle_point, middle_point, end_handle, end_point])

class Test17(Scene):
    def construct(self):

        line_1 = ParallelLine(3.5*UP + 5*LEFT, 2.5*UP + 5*RIGHT)
        line_2 = ParallelLine(2.5*UP + 4*LEFT, 1.5*UP + 4*RIGHT)
        line_3 = ParallelLine(1.5*UP + 3.5*LEFT, 0.5*UP + 3.5*RIGHT)
        line_4 = ParallelLine(0.5*UP + 3*LEFT, 0.5*DOWN + 3*RIGHT)
        line_5 = ParallelLine(0.5*DOWN + 2.5*LEFT, 1.5*DOWN + 2.5*RIGHT)
        line_6 = ParallelLine(1.5*DOWN + 1.5*LEFT, 2.5*DOWN + 1.5*RIGHT)
        line_7 = ParallelLine(2.5*DOWN + 0.5*LEFT, 3.5*DOWN + 0.5*RIGHT)
        self.add(line_1, line_2, line_3, line_4, line_5, line_6, line_7)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Test18(Scene):
    def construct(self):
        
        lines = []
        for i in range(5):
            for j in range(5):
                position = (i-2)*RIGHT + (j-2)*UP + RIGHT
                lines.append(ParallelLink(3*LEFT, position))
        self.add(*lines)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#####################################################################

class Cover(Scene):
    def construct(self):

        mark_outer = Circle(radius = 3.5, color = WHITE).set_stroke(width = 10)
        mark_inner = Circle(radius = 3.3, color = WHITE).set_stroke(width = 10)
        number = 78
        marks = VGroup()
        for i in range (number):
            angle = i * TAU / number
            mark_i = Line(3.3*unit(angle), 3.5*unit(angle)).set_stroke(width = 10)
            marks.add(mark_i)
        marks.add(mark_outer, mark_inner)

        number_letters = 26

        outer_text = VGroup()
        for i in range (number_letters):
            angle = i * TAU / number_letters
            text_i = Text(chr(65 + i), font = 'Times New Roman').scale(0.8).shift(2.9*UP).rotate(-angle, about_point = ORIGIN)
            outer_text.add(text_i)

        gear_outer = Circle(radius = 2.5, color = WHITE).set_stroke(width = 6)
        gear_inner = Gear(major_radius = 2.4, minor_radius = 2.26, n_teeth = number_letters).set_stroke(width = 6)
        outer_gear = VGroup(gear_outer, gear_inner)
        outer_layer = VGroup(marks, outer_text, outer_gear).scale(1.5, about_point = ORIGIN).shift(64/9*LEFT)

        gear_outer = Gear(major_radius = 2.34, minor_radius = 2.2, n_teeth = number_letters, width_ratio = 2/5, fill_opacity = 1, fill_color = "#000000", stroke_color = YELLOW_E).set_stroke(width = 6)
        gear_inner = Circle(radius = 2.1, color = YELLOW_E).set_stroke(width = 6)
        inner_gear = VGroup(gear_outer, gear_inner)

        inner_text = VGroup()
        for i in range (number_letters):
            angle = i * TAU / number_letters
            text_i = Text(chr(65 + i), font = 'Times New Roman', color = YELLOW_E).scale(0.7).shift(1.7*UP).rotate(-angle, about_point = ORIGIN)
            inner_text.add(text_i)

        
        mark_outer = Circle(radius = 1.3, color = YELLOW_E).set_stroke(width = 10)
        mark_inner = Circle(radius = 1.1, color = YELLOW_E).set_stroke(width = 10)
        number = 39
        marks = VGroup()
        for i in range (number):
            angle = i * TAU / number
            mark_i = Line(1.3*unit(angle), 1.1*unit(angle), color = YELLOW_E).set_stroke(width = 10)
            marks.add(mark_i)
        marks.add(mark_outer, mark_inner)
        inner_layer = VGroup(inner_gear, inner_text, marks).rotate(3*TAU/26).scale(1.5, about_point = ORIGIN).shift(64/9*LEFT)

        text = Text("完美加密", font = "FZYaSong-B-GBK", color = BLUE).scale(3).shift(2.5*RIGHT + 1.5*UP)
        for i in range(4):
            text.submobjects[i].shift(0.15*(i-1.5)*RIGHT)

        pairs = ["sleep-bunny", "sew-cog", "wet-owl", "oui-yes", "all-tee", "haw-pie", "has-exp", "log-two", "paw-tea", "pea-tie", "org-fix", "folk-iron", "rail-envy", "beef-loop", "spit-date", "noon-deed", "loaf-twin", "much-sain", "tear-pawn", "pear-lawn", "damp-road", "semi-cows", "wheel-dolls", "matte-gunny", "latte-funny", "marry-gulls", "melon-cubed", "furry-sheel", "beefs-adder", "dated-spits", "cheer-jolly", "curly-wolfs", "river-arena", "nulls-tarry", "thumbs-manful"]
        random.shuffle(pairs)
        random.random()
        random.random()
        mob_texts = [MTexText(text).scale(0.8 + random.random()*1.2).set_opacity(0 + random.random()*0.6).shift(np.array([-random.random()*12 + 6, (random.random()*7+2)%7 - 3.5, 0])) for text in pairs]
        
        # RED_Y = interpolate_color(RED, YELLOW_E, 0.15)
        # ORANGE_Y = interpolate_color(ORANGE, YELLOW_E, 0.15)
        # letters[0].move_to(1*RIGHT + 1.75*UP).set_color(RED_Y)
        # letters[1].move_to(4.5*RIGHT + 1.75*UP).set_color(RED_Y)
        # letters[2].move_to(1*RIGHT + 1.75*DOWN).set_color(ORANGE_Y)
        # letters[3].move_to(4.5*RIGHT + 1.75*DOWN).set_color(ORANGE_Y)

        self.add(*mob_texts, outer_layer, inner_layer, text)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)


#####################################################################

class Template(Scene):
    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)