from re import A
from manimlib import *
import numpy as np
import random

ORANGE_A = interpolate_color(ORANGE, WHITE, 0.5)
OMEGA = np.array([math.sqrt(3)/2, -1/2, 0])

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def ellipse_unit(angle, a=1, b=1/2):
    return np.array([a*np.cos(angle), b*np.sin(angle), 0])

def bounce(t: float):
    return 1- abs(bezier([0, 0, 0, 1.5, 1.5, 1])(t) - 1)

def double_bounce(t: float):
    return 1- abs(bezier([0, 0, 0, 1.6, 1.6, 0.9, 0.9, 1])(t) - 1)

def breath(t: float):
    return bezier([0, 0, 0, 1.5, 1.5, 1])(t)

def rate_color(rate):

    # colors = ["#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]
    # colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    # colors = [RED, YELLOW, GREEN, TEAL, BLUE, PURPLE]
    # colors = [TEAL, BLUE, BLUE, TEAL, GREEN, GREEN]
    # colors = [TEAL, BLUE, PURPLE, RED, YELLOW, GREEN]
    colors = [YELLOW_A, GREEN_A, BLUE_A, PURPLE_A, RED_A, ORANGE_A]
    #colors = [YELLOW_A, interpolate_color(ORANGE, WHITE, 0.5), RED_A, PURPLE_A, BLUE_A, GREEN_A]

    number_colors = len(colors)
    ratio = (number_colors * rate) % number_colors
    index = int(ratio)
    interpolate = ratio - index

    return interpolate_color(colors[index % number_colors], colors[(index+1) % number_colors], interpolate)

def caeser(text, offset):
            text_cypher = ""
            counter = np.zeros(26)
            for c in text:
                if "a" <= c <= "z":
                    order = (ord(c) - ord("a") + offset) % 26
                    text_cypher += chr(ord("a") + order)
                    counter[order] += 1
                elif "A" <= c <= "Z":
                    order = (ord(c) - ord("A")+ offset) % 26
                    text_cypher += chr(ord("A") + order)
                    counter[order] += 1
                else:
                    text_cypher += c
            return text_cypher, counter

def inverse_rush_from(t: float):
    return rush_into(1-t)

def inverse_rush_into(t: float):
    return rush_from(1-t)

######################################################################################################

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):

        super().__init__()
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

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
        "from_center": True,
        "scale_factor": None
    }
    from typing import List, Union
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
        if self.scale_factor is None:
            self.scale_factor = 0.5
        mob_texts = [TexText(text).scale(self.scale_factor).shift(base + np.array([random.random()*height, random.random()*width, 0])) for text in texts]
        super().__init__(*[Float(text, about_point = center) for text in mob_texts], **kwargs)

    def set_default_config_from_length(self, length: int) -> None:
        if self.lag_ratio is None:
            self.lag_ratio = min(4.0 / (length + 1.0), 0.2)

class Cloud(ArcBetweenPoints):
    def __init__(self, **kwargs):
        super().__init__(angle=PI, start = RIGHT, end = RIGHT + 1.2*UP, fill_color = GREY, fill_opacity = 1, stroke_width = 0, **kwargs)
        another = ArcBetweenPoints(angle=PI*5/6, start = RIGHT + 1.2*UP, end = LEFT + 1.5*UP)
        self.append_points(another.get_points())
        another = ArcBetweenPoints(angle=PI, start = LEFT + 1.5*UP, end = LEFT)
        self.append_points(another.get_points()).close_path()

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

class Knife(VMobject):
    CONFIG = {
        "fill_color": WHITE,
        "fill_opacity": 1.0,
        "stroke_color": WHITE,
        "stroke_opacity": 0.0,
        "stroke_width": 0.0,
    }
    def init_points(self) -> None:
        position = np.zeros((33, 3))
        position[0: 17] = np.array([[0, -4, 0], 
        [0.4, -3.2, 0], [0.4, -2.6, 0], [0.375, -0.275, 0], [0.35, 2.05, 0], 
        [0.5, 2.15, 0], [0.5, 2.25, 0], [0.5, 2.4, 0], [0.3, 2.5, 0], 
        [0.3, 2.6, 0], [0.25, 2.6, 0], [0.15, 3.2, 0], [0.3, 3.5, 0], 
        [0.5, 3.7, 0], [0.2, 3.8, 0], [0.2, 4, 0], [0, 4, 0]])
        position[17: 33, 0] = -position[15::-1, 0]
        position[17: 33, 1] = position[15::-1, 1]
        position /= 2
        
        points = np.zeros((48, 3))
        points[0::3] = position[0:-1:2]
        points[1::3] = position[1::2]
        points[2::3] = position[2::2]
        self.set_points(points)

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

class Block(VGroup):
    def __init__(self, shifting):
        
        block = Rectangle(width = 1.05, height = 0.45, stroke_color = BLUE, fill_opacity = 1, fill_color = interpolate_color("#333333", BLUE, 0.2))
        background = Rectangle(width = 1.15, height = 0.55, stroke_width = 0, fill_opacity = 1, fill_color = "#333333")
        cypher = "{" + chr(ord("a")+shifting) + "}"
        text = MTex("a\leftrightarrow " + cypher, tex_to_color_map = {"\leftrightarrow": GREEN, cypher: YELLOW_E}).scale(0.5)
        text.shift( -(text[1].get_center()) )

        super().__init__(background, block, text)

class HorizontalLink(FunctionGraph):

    def __init__(self, start_point: np.ndarray, end_point: np.ndarray, **kwargs):
        super().__init__(smooth, [0, 1, 0.02], **kwargs)
        self.start_point = start_point
        self.end_point = end_point
        self.scale(end_point - start_point, min_scale_factor = -np.inf, about_point = ORIGIN).shift(start_point)

class DoubleArrow(VMobject):
    CONFIG = {
        "fill_color": interpolate_color("#333333", BLUE, 0.2),
        "fill_opacity": 1.0,
        "stroke_color": BLUE,
    }
    def init_points(self) -> None:
        
        corners = np.array([[-0.3, 0.15, 0], [0.3, 0.15, 0], [0.3, 0.25, 0], [0.55, 0, 0], 
        [0.3, -0.25, 0], [0.3, -0.15, 0], [-0.3, -0.15, 0], [-0.3, -0.25, 0], 
        [-0.55, 0, 0], [-0.3, 0.25, 0], [-0.3, 0.15, 0]])

        self.set_points_as_corners(corners)

class RightArrow(VMobject):
    CONFIG = {
        "fill_color": interpolate_color("#333333", BLUE, 0.2),
        "fill_opacity": 1.0,
        "stroke_color": BLUE,
    }
    def init_points(self) -> None:
        
        corners = np.array([[-0.3, 0.15, 0], [0.3, 0.15, 0], [0.3, 0.25, 0], [0.55, 0, 0], 
        [0.3, -0.25, 0], [0.3, -0.15, 0], [-0.3, -0.15, 0], [-0.3, 0.15, 0]])

        self.set_points_as_corners(corners)

class LeftTip(VMobject):
    CONFIG = {
        "fill_color": interpolate_color("#333333", GREEN, 0.2),
        "fill_opacity": 1.0,
        "stroke_color": GREEN,
    }
    def init_points(self) -> None:
        
        corners = np.array([[-0.3, 0.15, 0], [-0.3, -0.15, 0], [-0.3, -0.25, 0], 
        [-0.55, 0, 0], [-0.3, 0.25, 0], [-0.3, 0.15, 0]])

        self.set_points_as_corners(corners)


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

######################################################################################################

class Intro0(Scene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("字符本身没有任何“意义”。\n字符的意义完全取决于解码方式，\n或者说，创造、习得、或者研究出的解读方式。", font = 'simsun', t2c={"字符": GREEN, "意义": YELLOW, "解码方式": BLUE, "解读方式": BLUE})
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DOWN + RIGHT), DOWN + LEFT)
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
        notice2 = Notice("没错", "又是香农")
        notice3 = Notice("视频前言", "请听介绍")
        notice4 = Notice("解谜游戏", "请迫击炮")
        notice5 = Notice("大段定义", "请　忽略")
        notice6 = Notice("常见疑问", "请　困惑")
        notice7 = Notice("经典论断", "请　借鉴")
        notice8 = Notice("视频前言", "请听介绍")
        notice9 = Notice("传统艺能", "请　三连")

        title = Text("密码学", font = 'simsun', color = YELLOW).shift(0.5*UP)
        self.play(Write(title), ReplacementTransform(notice0, notice1))
        self.waiting(2, 14) #大家应该都或多或少看过一些密码学的科普

        line_title = Line(3*UP, 3*UP)
        self.play(title.animate.next_to(3*UP, UP))
        self.play(line_title.animate.put_start_and_end_on(3*UP + 6*LEFT, 3*UP + 6*RIGHT))
        self.waiting(0, 14) #大概知道一些密码学的发展脉络
        self.waiting(0, 21) #（空闲）

        picture_shannon = ImageMobject("picture_Shannon.jpg", height = 4).shift(2*LEFT + 0.5*UP)
        picture_paper = ImageMobject("picture_paper.jpg", height = 5).shift(2*RIGHT)
        text_shannon = Text("Claude Elwood Shannon", font = "Times New Roman").scale(0.5).next_to(picture_shannon, DOWN)
        life_shannon = Tex("1916.4.30 — 2001.2.24").scale(0.5).next_to(text_shannon, DOWN)
        group_shannon = Group(picture_shannon, text_shannon, life_shannon, picture_paper)
        self.play(FadeIn(group_shannon, UP), ReplacementTransform(notice1, notice2))
        self.waiting(0, 13) #大体上来说
        self.waiting(3, 24) #以克劳德·香农在1949年发表的一篇论文为界

        subline_left = Line(3*UP + 5*LEFT, 3*UP + 1*LEFT, stroke_color = GREY)
        subline_right = Line(3*UP + 1*RIGHT, 3*UP + 5*RIGHT, stroke_color = GREY)
        copy_line = line_title.copy()
        self.add(subline_left, subline_right, copy_line)
        self.play(subline_left.animate.shift(DOWN), subline_right.animate.shift(DOWN), FadeOut(group_shannon, DOWN), FadeOut(copy_line, DOWN), ReplacementTransform(notice2, notice3))
        self.waiting(1, 14) #密码学可以分为两个阶段

        classic = Text("古典密码学", font = 'simsun', color = YELLOW).scale(0.8).next_to(2*UP + 3*LEFT, UP)
        modern = Text("现代密码学", font = 'simsun', color = YELLOW).scale(0.8).next_to(2*UP + 3*RIGHT, UP)
        title_left = VGroup(classic, subline_left)
        title_right = VGroup(modern, subline_right)
        self.play(Write(classic))
        self.waiting(0, 3) #古典密码学......
        self.play(Write(modern))
        self.waiting(0, 5) #......和现代密码学
        self.waiting(0, 23) #（空闲）
        self.remove(classic, subline_left, modern, subline_right).add(title_left, title_right)

        mark_outer = Circle(radius = 3.6, color = WHITE)
        mark_inner = Circle(radius = 3.5, color = WHITE)
        number = 78
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
        gear_outer = Gear(major_radius = 2.52, minor_radius = 2.4, n_teeth = number_letters, width_ratio = 1/2, fill_opacity = 0, stroke_color = YELLOW_E)
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
        number = 78
        marks = VGroup()
        for i in range (number):
            angle = i * TAU / number
            mark_i = Line(1.5*unit(angle), 1.4*unit(angle), color = YELLOW_E)
            marks.add(mark_i)
        marks.add(mark_outer, mark_inner)
        inner_layer = VGroup(inner_gear, inner_text, marks, inner_number).rotate(3*TAU/26)
        keypad = VGroup(outer_layer, inner_layer).scale(0.6).shift(3*RIGHT + 0.5*DOWN)
        
        shade = SurroundingRectangle(title_right, stroke_width = 0, fill_color = "#333333", fill_opacity = 1).shift(4.2*RIGHT)
        text_sigma = Tex(r"\sigma", color = BLUE).insert_n_curves(100).scale(10)
        left_eye = Eye(looking_at = PI/3).scale(0.5).shift(1.35*UP+0.1*RIGHT)
        right_eye = Eye(looking_at = PI/3).scale(0.5).shift(1.35*UP+0.8*RIGHT)
        mouth = Mouth().scale(0.2, about_point = ORIGIN).shift(1.00*UP + 0.45*RIGHT)
        def raise_hand(point: np.ndarray):
            if point[0] < 0.8:
                return point
            else:
                return point + (point[0]-0.8)**2 *UP
        copy_sigma = text_sigma.copy()
        copy_sigma.apply_function(raise_hand)
        copy_left = left_eye.copy()
        copy_right = right_eye.copy()
        happy = Mouth(upper_angle = -PI/6).scale(0.2, about_point = ORIGIN).shift(1.00*UP + 0.45*RIGHT)
        sigma_chan = VGroup(left_eye, right_eye, text_sigma, mouth).shift(1.5*LEFT + 1.5*DOWN)
        sigma_chan_copy = VGroup(copy_left, copy_right, copy_sigma, happy).shift(1.5*LEFT + 1.5*DOWN) 

        texts = ["隐藏法", "恺撒密码", "猪圈密码", "栅栏密码", "替换密码", "玛丽女王密码", "同音替代法", "维吉尼亚密码", "比尔密码", "莫斯电码", "俚语加密", "恩尼格码"]
        anim = SpringUp(4*LEFT + 0.5*UP, texts, side_length = 2)
        anim.update_config(run_time = 7)

        self.add(shade, notice3)
        self.play(title_left.animate.shift(3*RIGHT), title_right.animate.shift(6*RIGHT), FadeIn(sigma_chan, 3*RIGHT), ReplacementTransform(notice3, notice4))
        self.waiting(1, 15) #古典密码学以替换密码为主
        self.play(FadeIn(keypad), Transform(sigma_chan, sigma_chan_copy), anim)
        self.waiting(3+2+2-7, 4+14+18) #从两千年前的恺撒密码一路发展而来 充满了大家喜闻乐见的内容 至今还是各类解谜游戏中的常客
        self.waiting(0, 23) #（空闲）

        shade = Rectangle(height = 5.8, weight = 2, stroke_width = 0, fill_color = "#333333", fill_opacity = 1).shift(7.5*LEFT)
        self.add(shade)

        self.play(FadeOut(sigma_chan, 9*LEFT), keypad.animate.shift(12*LEFT), title_left.animate.shift(9*LEFT), title_right.animate.shift(9*LEFT), ReplacementTransform(notice4, notice5))
        self.waiting(0, 28) #而一提起现代密码学
        rsa = MTexText(r"随机抽取素数$p, q$, 记$N=pq$\\ 随机抽取与$\phi(N)$互素的$e$\\ 记$d\equiv e^{-1}\pmod{\phi(N)}$\\ 则有对应的加密方案：\\私钥：$p, q, d$\\ 公钥：$N, e$\\ 加密：$c\equiv m^e \pmod N$\\ 解密：$m\equiv c^d \pmod N$", alignment="").scale(0.8).shift(0.2*DOWN + 3*LEFT)
        self.play(Write(rsa), run_time = 4)
        self.waiting(1+3-4, 23+11) #恐怕大家的第一反应 是RSA算法这样充满了数学气息的加密方案
        self.waiting(0, 19) #（空闲）

        text_sigma = Tex(r"\sigma", color = BLUE).scale(10)
        left_eye = Eye(looking_at = PI*7/6).scale(0.5).shift(1.35*UP+0.1*RIGHT)
        right_eye = Eye(looking_at = PI/3).scale(0.5).shift(1.35*UP+0.8*RIGHT)
        mouth = Mouth().scale(0.3, about_point = ORIGIN).shift(1.05*UP + 0.45*RIGHT)
        drool = Drop().scale(0.2, about_point = ORIGIN).shift(1.05*UP + 0.15*RIGHT)
        sigma_chan = VGroup(left_eye, right_eye, text_sigma, mouth, drool).shift(3*RIGHT + 0.5*DOWN)
        shade = BackgroundRectangle(sigma_chan, fill_color = "#333333", fill_opacity = 1).scale(1.2)
        self.add(sigma_chan, shade)
        
        texts = ["我是谁", "我在哪", "为什么要取素数", "为什么是数论", "那个-1次方是什么意思", "数论倒数？", "我是不是在哪见过", "e是什么", "d是什么", "φ又是什么", "我可爱的替换加密呢", "这和加密有什么关系"]
        anim1 = SpringUp(sigma_chan, texts, rate_func = squish_rate_func(smooth, 0.2, 1))
        anim2 = FadeOut(shade, rate_func = there_and_back_with_pause(0.6), remover = False)
        sigma_chan.scale(0.8)
        self.play(anim1, anim2, ApplyMethod(sigma_chan.scale, 1.5), run_time = 6)
        self.remove(sigma_chan, shade)
        self.waiting(2+2+2-6, 14+18+4) #这些方案又充斥着复杂的运算 又不像恺撒密码那么好理解 而且 更重要的是
        self.play(title_right.animate.shift(3*RIGHT), rsa.animate.shift(6*RIGHT), keypad.animate.shift(6*RIGHT), title_left.animate.shift(6*RIGHT), ReplacementTransform(notice5, notice6))
        self.waiting(2, 21) #现代密码学到底和古典密码学有什么关系啊？
        self.waiting(0, 24) #（空闲）

        self.remove(title_right, rsa, keypad, title_left, title, line_title)

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
            mob.become(copy_building).apply_function(util)
        building.add_updater(building_update)
        self.add(base, building)
        self.play(alpha.animate.set_value(1.0))
        building.clear_updaters()
        self.waiting(1, 1) #从古典到现代的革命

        basement = Rectangle(height = 0.8, width = 3, stroke_width = 6, stroke_color = YELLOW_E).shift(2.5*DOWN)
        baseline = Line(2.1*DOWN+2*LEFT, 2.1*DOWN + 2*RIGHT, stroke_width = 6)
        building.add(basement, baseline)
        hole = basement.copy()
        self.add(hole)
        self.play(Rotate(building, about_point = 2.1*DOWN + 2*LEFT, angle = PI - np.arctan(4.2/0.5)), rate_func = lambda t: 2*t**3 - 3*t**2 + 2*t)
        self.waiting(2, 22) #似乎是把密码学这栋大厦的地基整个掀起来

        self.remove(base, hole)
        building.add(base, hole)
        copy_building.add(base.copy())
        new_building = copy_building.copy().shift(3*RIGHT + 7*UP)
        anim = ApplyMethod(new_building.shift, 7*DOWN, rate_func = squish_rate_func(rush_into, 0.5, 1))
        self.play(building.animate.shift(2*LEFT), anim)
        self.waiting(2, 10) #然后在旁边重新盖了一栋新的一样
        self.waiting(2, 4) #从加密对象到加密手法
        self.waiting(1, 14) #全部刷新了一遍
        self.waiting(0, 16) #（空闲）

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
        beta = ValueTracker(1.0)
        def updater_stroke_opacity(mob: VMobject):
            mob.set_stroke(opacity = beta.get_value())
        def updater_fill_opacity(mob: VMobject):
            mob.set_fill(opacity = beta.get_value())

        self.add(building_physics, cloud_quantum, cloud_relativity)
        self.play(building.animate.scale(0.7, about_point = 7*LEFT + 3*UP), new_building.animate.scale(0.7, about_point = 7*LEFT + 3*UP), alpha.animate.set_value(0.7), ReplacementTransform(notice6, notice7))
        self.waiting(2, 11) #和它一比 量子力学和相对论的革命
        self.waiting(2+0-1, 0+26) #都只能算是小修小补的 （空闲）
        fading_group = [building, new_building, building_physics, cloud_quantum, cloud_relativity]
        for mob in [building, new_building, building_physics]:
            mob.add_updater(updater_stroke_opacity)
        for mob in [cloud_quantum, cloud_relativity]:
            mob.add_updater(updater_fill_opacity)
        self.play(beta.animate.set_value(0.0))
        self.remove(*fading_group)

        showing_group = VGroup(title_right, rsa, keypad, title_left, title, line_title)
        self.play(FadeIn(showing_group, UP), ReplacementTransform(notice7, notice8))
        self.waiting(1, 14) #但其实大家看到的这些加密方案
        self.play(showing_group.animate.set_color(GREY))
        self.waiting(1, 16) #都不是密码学真正的地基
        self.remove(showing_group)

        shannon_secrecy = MTexText("香农私密性（香农定义的）：\\ $\mbox{Pr}[k\leftarrow \mathbf{Gen}; m\leftarrow D: m=m'|\mathbf{Enc}_k(m)=c]=\mbox{Pr}[m\leftarrow D: m=m']$\\\\\\ 完美私密性（也是香农定义的）：\\ $\mbox{Pr}[k\leftarrow \mathbf{Gen}: \mathbf{Enc}_k(m_1)=c]=\mbox{Pr}[k\leftarrow \mathbf{Gen}: \mathbf{Enc}_k(m_2)=c]$").scale(0.8)
        self.play(FadeIn(shannon_secrecy, UP))
        self.waiting(0, 21) #密码学真正的地基
        self.waiting(1, 20) #是一件非常简单
        self.waiting(2+0-1, 24+21)
        self.play(FadeOut(shannon_secrecy)) #却被所有人忽略了快两千年的小事 （空闲）

        like = Text("", font = 'vanfont').shift(3*LEFT).scale(2)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT).scale(2)
        sanlian = VGroup(like, coin, star)

        self.play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, np.array([0,0,0])), FadeInFromPoint(star, 3*RIGHT), ReplacementTransform(notice8, notice9))
        self.play(Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), ApplyMethod(sanlian.set_color, "#00A1D6"))
        self.waiting(3-2,7) #长按点赞一键三连 我们开始吧
        self.waiting(3, 6)
        self.play(FadeOut(notice9), FadeOut(sanlian))
        self.waiting(3, 0) #到此共90秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

######################################################################################################

class Chapter1_0(Scene):

    def construct(self):

        ##  Making object
        text1 = Text("第一节 恺撒密码什么时候是安全的？", font = 'simsun', t2c={"第一节": YELLOW, "恺撒密码": GREEN, "安全": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(Scene):
    def construct(self):

        notice1 = Notice("经典方案", "请　复习")
        notice2 = Notice("还有你吗", "布鲁图斯")
        notice3 = Notice("经典解法", "请　复习")
        notice4 = Notice("经典缺陷", "请　复习")
        notice5 = Notice("太弱小了", "没有力量")

        keypad = Keypad()
        copy_keypad = keypad.copy()

        alpha = ValueTracker(0.0)
        def updater_wheel(mob: VMobject):
            distance = 10.5 * (1- bezier([0, 0, 0, 1.5, 1.5, 1, 1, 1])(alpha.get_value()))
            mob.become(keypad).rotate(distance/3).shift(distance * LEFT)
        
        self.add(copy_keypad)
        copy_keypad.add_updater(updater_wheel)
        self.play(Write(notice1), ApplyMethod(alpha.set_value, 1.0).update_config(rate_func = linear, run_time = 2))
        copy_keypad.clear_updaters()
        self.remove(copy_keypad).add(keypad)
        self.waiting(0, 4) #大家应该都见过恺撒密码
        self.waiting(0, 15) #（空闲）

        self.waiting(2, 5) #它的加密十分简单

        message = MTexText("simple").shift(4.2*LEFT)
        copy_message = message.copy()

        alpha = ValueTracker(0.0)
        def updater_car(mob: VMobject):
            value = alpha.get_value()
            if value < 0.6:
                shift = ((0.6 - value)/0.6)**2
                distance = shift * 4
                angle = -PI/6*(1 - shift)
            else:
                distance = 0
                angle = -PI/6*(1 - ((value - 0.6)/0.4)**2)
            mob.become(message).rotate(angle, about_point = message.get_corner(DR)).shift(distance * LEFT)

        self.add(copy_message)
        copy_message.add_updater(updater_car)
        self.play(ApplyMethod(alpha.set_value, 1.0).update_config(rate_func = linear, run_time = 1))
        copy_message.clear_updaters()
        self.remove(copy_message).add(message) 
        self.waiting(1, 0) #对于一段英文文本

        keypad.get_highlights()
        handle = keypad.get_handle()
        keypad.encrypt("S", "I", "M", "P", "L", "E")
        cypher_0 = MTexText("simple", color = YELLOW_E)
        self.play(Write(cypher_0))
        self.waiting(1, 5) #我们按照字母表的顺序

        cypher_1 = MTexText("tjnqmf", color = YELLOW_E)
        cypher_2 = MTexText("ukorng", color = YELLOW_E)
        cypher_3 = MTexText("vlpsoh", color = YELLOW_E)

        self.play(ApplyMethod(handle.set_value, 1.0), FadeOut(cypher_0).update_config(rate_func = squish_rate_func(smooth, 0, 0.5)), FadeIn(cypher_1).update_config(rate_func = squish_rate_func(smooth, 0, 0.5)), run_time = 0.2)
        self.waiting(0, 24)
        self.play(ApplyMethod(handle.set_value, 2.0), FadeOut(cypher_1).update_config(rate_func = squish_rate_func(smooth, 0, 0.5)), FadeIn(cypher_2).update_config(rate_func = squish_rate_func(smooth, 0, 0.5)), run_time = 0.2)
        self.waiting(0, 24)
        self.play(ApplyMethod(handle.set_value, 3.0), FadeOut(cypher_2).update_config(rate_func = squish_rate_func(smooth, 0, 0.5)), FadeIn(cypher_3).update_config(rate_func = squish_rate_func(smooth, 0, 0.5)), run_time = 0.2)
        self.waiting(0, 24)
        keypad.clear_updaters()
        self.waiting(0, 17) #把每一个字母往前或者往后推一定的位置
        self.waiting(0, 17) #（空闲）

        self.waiting(1, 18) #经过这样的操作
        anims = [Indicate(text) for text in message]
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 1))
        self.waiting(1, 3) #原本很有规律的单词
        anims = [Indicate(text) for text in cypher_3]
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 1))
        self.waiting(1, 8) #就变成了看不出规律的乱码
        self.waiting(0, 19) #（空闲）

        picture_ceasar = ImageMobject("picture_Caesar.png", height = 8).shift(5*RIGHT + 11*DOWN)
        self.add(picture_ceasar)
        self.play(picture_ceasar.animate.shift(8*UP))
        bubble = Union(Ellipse(width = 2.2, height = 1.1), Triangle().scale(0.5).rotate(-PI/12).shift(0.5*RIGHT + 0.4*DOWN)).shift(4*RIGHT + 2*UP)
        perfect = Text("完美。", font = "simsun").scale(0.8).shift(4*RIGHT + 2*UP)
        talk = VGroup(bubble, perfect)
        self.play(FadeInFromPoint(talk, talk.get_corner(DR) + 0.3*DOWN), run_time = 0.5)
        self.waiting(0.5, 7) #对于在两千年前的人来说
        self.waiting(2, 2)
        self.play(FadeOut(talk)) #恺撒使用的这种方法十分难以破解

        brutus = Knife(stroke_width = 0, fill = "#c0c0c0").rotate(PI/2).shift(3.2*DOWN)
        brutus.save_state()
        showing = Rectangle(height = 1, width = 12).shift(3.2*DOWN + 10/9*LEFT)
        alpha = ValueTracker(9.5)
        def brutus_updater(brutus: Knife):
            distance = alpha.get_value()
            brutus.restore().shift(distance * LEFT)
            outside = Intersection(brutus, showing)
            brutus.set_points(outside.get_all_points())
        brutus.add_updater(brutus_updater)
        bubble = Union(Ellipse(width = 2.4, height = 0.9), Triangle().scale(0.4).rotate(-PI/12).shift(0.5*RIGHT + 0.4*DOWN)).shift(4*RIGHT + 1.6*UP)
        et_tu = Text("Et tu, Brute?", font = "Trajan Pro").scale(0.4).shift(4*RIGHT + 1.6*UP)
        brute = VGroup(bubble, et_tu)

        self.add(brutus)
        self.play(ApplyMethod(alpha.set_value, -5.0).update_config(run_time = 0.5), ReplacementTransform(notice1, notice2))
        brutus.clear_updaters()
        self.play(FadeInFromPoint(brute, brute.get_corner(DR) + 0.3*DOWN))
        self.waiting(1, 0)
        falling = Group(picture_ceasar, brutus, brute)
        falling.save_state()
        self.remove(picture_ceasar, brutus, brute).add(falling)
        alpha = ValueTracker(0.0)
        def falling_updater(mob: Mobject):
            distance = alpha.get_value()
            mob.restore().rotate(-distance*0.5, about_point = mob.get_corner(DL)).shift(distance**2 * DOWN)
        falling.add_updater(falling_updater)
        self.play(alpha.animate.set_value(3.0))
        falling.clear_updaters()
        self.remove(falling)
        self.waiting(2+4-4, 6+9) #但对于两千年后的我们来说 恺撒密码实在是最有规律 最好破解的一种加密方式了
        self.waiting(0, 18) #（空闲）

        self.play(ReplacementTransform(notice2, notice3))
        self.waiting(0, 26) #说到破解恺撒密码
        self.waiting(1, 14) #大家听到最多的
        title = Text("频率分析法", font = 'simsun', color = YELLOW).next_to(4*UP, UP)
        line_title = Line(4*UP, 4*UP).insert_n_curves(64)
        self.play(FadeOut(message, DOWN), FadeOut(cypher_3, DOWN), FadeOut(keypad, DOWN), title.animate.next_to(3*UP, UP), line_title.animate.put_start_and_end_on(3*UP + 6*LEFT, 3*UP + 6*RIGHT))
        self.waiting(1, 2) #应该是频率分析法

        # text_message = "Shannon secrecy:\nGiven some a priori information,\nthe adversary cannot learn any\nadditional information about\nthe plaintext by observing the ciphertext."
        # text_message = "The notion of perfect secrecy requires\nthat the distribution of ciphertexts\nfor any two messages are identical.\nThis formalizes our intuition that\nthe ciphertexts carry\nno information about the plaintext."
        text_message = "At first glance, messages encrypted using\nthe Ceasar Cipher look “scrambled”\n(unless key is known). However, to break\nthe scheme we just need to try\nall possible keys (which is easily done)\nand see if the resulting plaintext is “readable”." # If the message is relatively long, the scheme is easily broken.
        offset = 5
        text_cypher, counter = caeser(text_message, offset)
        cypher = Text(text_cypher, font = "Times New Roman", color = YELLOW_E).scale(0.6).shift(1.5*UP + 3*LEFT)
        message = Text(text_message, font = "Times New Roman").scale(0.6).shift(1.5*DOWN + 3*RIGHT)
        line = Line(2.1*DOWN + 6.6*LEFT, 2.1*DOWN + 0.9*LEFT)
        letters = Text("a b c d e f g h i j k l m n o p q r s t u v w x y z", font = "Times New Roman", color = YELLOW_E).scale(0.5).next_to(2.1*DOWN + 3.75*LEFT, DOWN, buff = 0.1).shift(0.4*UP)
        positions = [np.array([letter.get_center()[0], -2.1, 0]) for letter in letters]
        starts = [position + 0.1*DOWN for position in positions]
        ends = [positions[i] + counter[i]*0.06*UP for i in range(26)]
        dots = [Dot(color = YELLOW).shift(start) for start in starts]
        anim_dots = LaggedStart(*[ApplyMethod(dots[i].move_to, ends[i]) for i in range(26)], group = VGroup(), lag_ratio = 0.03)
        lines = [Line(start, start) for start in starts]
        anim_lines = LaggedStart(*[ApplyMethod(lines[i].put_start_and_end_on, positions[i], ends[i]) for i in range(26)], group = VGroup(), lag_ratio = 0.03)
        shade = Rectangle(height = 0.4, width = 6, stroke_width = 0, fill_opacity = 1, fill_color = "#333333").shift(1.95*DOWN + 3.75*LEFT)
        self.play(FadeIn(cypher, 0.5*RIGHT))
        self.add(letters, shade)
        self.play(ShowCreation(line))
        self.play(letters.animate.shift(0.4*DOWN), lag_ratio = 0.03, run_time = 1.5)
        self.bring_to_back(*lines, *dots, shade.shift(0.35*DOWN))
        self.play(anim_dots, anim_lines, run_time = 1.5)

        arrow_notice = Arrow(dots[9].get_center()+0.6*RIGHT, dots[9].get_center()+0.2*RIGHT, buff = 0)
        text_notice = MTexText("应该是e").scale(0.6).next_to(arrow_notice, buff = 0.1)
        group_notice = VGroup(arrow_notice, text_notice)
        arrow_decrypt = CurvedArrow(cypher.get_corner(RIGHT)+0.1*RIGHT, message.get_corner(UP)+0.3*UP, angle = -PI/2, color = ["#333333", GREEN], tip_length = 0.20)
        arrow_decrypt.get_tip().set_color(GREEN)
        arrow_f_text = MTex("-5", color = GREEN).move_to(arrow_decrypt.get_center()+0.8*UR)

        self.play(FadeIn(group_notice, 0.5*LEFT))
        self.play(ShowCreation(arrow_decrypt), FadeIn(arrow_f_text))
        self.play(ShowIncreasingSubsets(message), run_time = 5, rate_func = linear)
        self.waiting(2+2+2+0 + 2+2 - 12, 2+22+16+15 + 27+15) #只要有一段足够长的密文 通过统计不同符号出现的频率 我们就可以反推出加密前的明文 （空闲） 实际上 频率分析法的用途 不止有破解恺撒密码这一个 
        self.waiting(2, 23) #它是所有替换加密法的通用破解法
        self.waiting(0, 21) #（空闲）
        
        self.play(ReplacementTransform(notice3, notice4))
        self.waiting(2, 11) #当然 频率分析法不是万能的
        self.waiting(2, 10) #想要用它去破解替换加密
        self.play(WiggleOutThenIn(cypher), run_time = 1.5)
        anim_dots = [ApplyMethod(dots[i].move_to, starts[i]) for i in range(26)]
        anim_lines = [ApplyMethod(lines[i].put_start_and_end_on, starts[i], starts[i]) for i in range(26)]
        self.waiting(2+0-2.5, 15+18) # 首先得拿到足够长的密文才行 （空闲）
        self.play(*anim_dots, *anim_lines, *[FadeOut(mob) for mob in [cypher, message, arrow_decrypt, arrow_f_text, group_notice]])
        
        # text_message = "Caesar Cipher is a\nprivate-key encryption scheme."
        text_message = "It is only key that\nshould be assumed private."
        offset = 7
        text_cypher, counter = caeser(text_message, offset)
        cypher = Text(text_cypher, font = "Times New Roman", color = YELLOW_E).shift(1.5*UP + 3*LEFT)
        ends = [positions[i] + counter[i]*0.2*UP for i in range(26)]
        self.play(FadeIn(cypher, 0.5*RIGHT))
        anim_dots = [ApplyMethod(dots[i].move_to, ends[i]) for i in range(26)]
        anim_lines = [ApplyMethod(lines[i].put_start_and_end_on, positions[i], ends[i]) for i in range(26)]
        self.play(*anim_dots, *anim_lines)
        self.waiting(0, 1) #如果得到的密文非常短
        arrow_1 = Arrow(dots[11].get_center()+0.6*UP, dots[11].get_center()+0.2*UP, buff = 0)
        arrow_2 = Arrow(dots[25].get_center()+0.6*UP, dots[25].get_center()+0.2*UP, buff = 0)
        arrow_3 = Arrow(dots[0].get_center()+0.6*UP, dots[0].get_center()+0.2*UP, buff = 0)
        text = Text("???", font = "Times New Roman").scale(0.6).shift(3.75*LEFT + 0.4*DOWN)
        group_notice = VGroup(arrow_1, arrow_2, arrow_3, text)
        self.play(FadeIn(group_notice, 0.2*DOWN))
        self.waiting(2+0-2, 3+18) #频率分析法就无计可施了 （空闲）
        self.play(*[FadeOut(mob) for mob in [*dots, *lines, group_notice, line, letters, cypher]])
        self.remove(shade)
        
        keypad = Keypad().shift(3.5*LEFT)
        copy_inner = keypad.inner.copy()
        copy_outer = keypad.outer.copy()
        alpha = ValueTracker(PI/4)
        def updater_outer(mob: VMobject):
            angle = alpha.get_value()
            mob.become(keypad.outer).rotate(angle)
        copy_outer.add_updater(updater_outer)
        def updater_inner(mob: VMobject):
            angle = alpha.get_value()
            mob.become(keypad.inner).rotate(-angle)
        copy_inner.add_updater(updater_inner)
        shade = SurroundingRectangle(keypad, fill_color = "#333333", fill_opacity = 1, stroke_width = 0)

        self.bring_to_back(copy_outer, copy_inner, shade)
        self.play(alpha.animate.set_value(0.0), FadeOut(shade), ReplacementTransform(notice4, notice5))
        copy_outer.clear_updaters()
        copy_inner.clear_updaters()
        self.remove(copy_outer, copy_inner).add(keypad)
        self.waiting(1, 15) # 但恺撒密码实在是太弱了
        self.play(RollUp(title), RollUp(line_title), rate_func = linear) #弱到我们甚至不需要动用频率分析法

        keypad.get_highlights()
        handle = keypad.get_outer_handle(center = 3.5*LEFT)
        keypad.decrypt("E", "M", "I", "S")
        cypher_weak = MTexText("emis", color = YELLOW_E).shift(3.5*LEFT)
        self.play(Write(cypher_weak))
        self.waiting(1, 6) #弱到即使只有一个单词
        self.waiting(1, 25) #我们也能着手破解它
        self.waiting(0, 23) #（空闲）
        
        def align_all(string: str, buff: float = 1.5):
            all_texts = []
            for i in range(26):
                text, _ = caeser(string, i)
                all_texts.append(text)
            mob_texts = MTexText("".join(all_texts), isolate = all_texts)
            part_texts = [mob_texts.get_part_by_tex(text).set_x(2.5) for text in all_texts]
            for i in range(26):
                row = i // 3
                col = i % 3
                part_texts[i].shift(0.6*DOWN*(row-4) + buff*RIGHT*(col-1))
            return mob_texts, part_texts

        _, part_texts = align_all("emis")
        
        base = np.array([4, 12, 8, 18])
        self.play(TransformFromCopy(VGroup(*[keypad.message[i] for i in base + 0]), part_texts[0]), run_time = 0.8)
        self.play(handle.animate.set_value(1.0), run_time = 0.2)
        self.play(TransformFromCopy(VGroup(*[keypad.message[i] for i in base + 1]), part_texts[1]), run_time = 0.6)
        self.play(handle.animate.set_value(2.0), run_time = 0.2)
        self.play(TransformFromCopy(VGroup(*[keypad.message[i] for i in base + 2]), part_texts[2]), run_time = 0.4)
        self.play(handle.animate.set_value(3.0), run_time = 0.2)
        self.play(TransformFromCopy(VGroup(*[keypad.message[i] for i in base + 3]), part_texts[3]), run_time = 0.2)
        for i in range(4, 22):
            self.play(handle.animate.set_value(i), ShowIncreasingSubsets(part_texts[i]), run_time = 0.2)
        self.play(handle.animate.set_value(22.0), run_time = 0.2)    
        self.play(TransformFromCopy(VGroup(*[keypad.message[i%26] for i in base + 22]), part_texts[22]), run_time = 0.2)
        self.play(handle.animate.set_value(23.0), run_time = 0.2)
        self.play(TransformFromCopy(VGroup(*[keypad.message[i%26] for i in base + 23]), part_texts[23]), run_time = 0.4)
        self.play(handle.animate.set_value(24.0), run_time = 0.2)
        self.play(TransformFromCopy(VGroup(*[keypad.message[i%26] for i in base + 24]), part_texts[24]), run_time = 0.6)
        self.play(handle.animate.set_value(25.0), run_time = 0.2)
        self.play(TransformFromCopy(VGroup(*[keypad.message[i%26] for i in base + 25]), part_texts[25]), run_time = 0.8)
        self.play(handle.animate.set_value(26.0), run_time = 0.2)
        handle.set_value(0.0)
        self.waiting(2+3+2+1-9.2, 22+4+21+19) # 这个破解方法就是暴力穷举 即使我们不知道加密的时候移动了几位 但反正英文字母只有26个 挨个试过去就可以了
        self.waiting(0, 19) #（空闲）

        self.waiting(1, 18) #26种可能中
        anims = []
        for i in range (26):
            if i == 18:
                highlight = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight)
                anims.append(ApplyMethod(highlight.set_stroke, {"opacity": 1}))
            else:
                anims.append(ApplyMethod(part_texts[i].fade))
        self.play(LaggedStart(*anims, group = VGroup(), lag_ratio = 0.3, run_time = 2))
        self.waiting(0, 2) #绝大部分都是乱码

        indicate = SurroundingRectangle(part_texts[18])
        self.play(ShowCreation(indicate))
        self.waiting(2, 19) #我们可以轻松地从里面挑出没加密的原文

        cypher_ceaser = MTexText("vxtlxk", color = YELLOW_E).shift(3.5*LEFT)
        keypad.decrypt()
        self.play(*[FadeOut(mob) for mob in part_texts], FadeOut(highlight), FadeOut(indicate), FadeOut(cypher_weak, rate_func = squish_rate_func(smooth, 0, 0.5)), FadeIn(cypher_ceaser, rate_func = squish_rate_func(smooth, 0.5, 1)))
        keypad.decrypt("V", "X", "T", "L", "K")
        self.waiting(0, 25) #到此共98秒

        _, part_texts = align_all("vxtlxk", buff = 1.8)
        all_texts = VGroup(*part_texts)
        self.play(handle.animate.set_value(25.0), ShowIncreasingSubsets(all_texts, int_func = lambda t: np.round(t*25/26 + 1)), run_time = 4)
        self.remove(all_texts).add(*part_texts)
        self.waiting(1, 0)

        anims = []
        for i in range (26):
            if i == 7:
                highlight = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight)
                anims.append(ApplyMethod(highlight.set_stroke, {"opacity": 1}))
            else:
                anims.append(ApplyMethod(part_texts[i].fade))
        self.play(LaggedStart(*anims, group = VGroup(), lag_ratio = 0.3, run_time = 2))
        indicate = SurroundingRectangle(part_texts[7])
        self.play(ShowCreation(indicate))
        self.waiting(1, 0)

        cypher_coin = MTexText("pbva", color = YELLOW_E).shift(3.5*LEFT)
        keypad.decrypt()
        self.play(*[FadeOut(mob) for mob in part_texts], FadeOut(highlight), FadeOut(indicate), FadeOut(cypher_ceaser, rate_func = squish_rate_func(smooth, 0, 0.5)), FadeIn(cypher_coin, rate_func = squish_rate_func(smooth, 0.5, 1)), handle.animate.set_value(26))
        handle.set_value(0.0)
        keypad.decrypt("P", "B", "V", "A")
        self.waiting(1, 0)

        _, part_texts = align_all("pbva", buff = 1.8)
        all_texts = VGroup(*part_texts)
        self.play(handle.animate.set_value(25.0), ShowIncreasingSubsets(all_texts, int_func = lambda t: np.round(t*25/26 + 1)), run_time = 4)
        self.remove(all_texts).add(*part_texts)
        self.waiting(1, 0)

        anims = []
        for i in range (26):
            if i == 13:
                highlight = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight)
                anims.append(ApplyMethod(highlight.set_stroke, {"opacity": 1}))
            else:
                anims.append(ApplyMethod(part_texts[i].fade))
        self.play(LaggedStart(*anims, group = VGroup(), lag_ratio = 0.3, run_time = 2))
        indicate = SurroundingRectangle(part_texts[13])
        self.play(ShowCreation(indicate))
        self.waiting(1, 0)

        cypher_sleep = MTexText("hatte", color = YELLOW_E).shift(3.5*LEFT)
        keypad.decrypt()
        self.play(*[FadeOut(mob) for mob in part_texts], FadeOut(highlight), FadeOut(indicate), FadeOut(cypher_coin, rate_func = squish_rate_func(smooth, 0, 0.5)), FadeIn(cypher_sleep, rate_func = squish_rate_func(smooth, 0.5, 1)), handle.animate.set_value(26))
        handle.set_value(0.0)
        keypad.decrypt("H", "A", "T", "E")
        self.waiting(1, 0)

        _, part_texts = align_all("hatte", buff = 1.8)
        all_texts = VGroup(*part_texts)
        self.play(handle.animate.set_value(25.0), ShowIncreasingSubsets(all_texts, int_func = lambda t: np.round(t*25/26 + 1)), run_time = 4)
        self.remove(all_texts).add(*part_texts)
        self.waiting(1, 0)

        anims = []
        for i in range (26):
            if i == 11 or i == 20:
                highlight = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight)
                anims.append(ApplyMethod(highlight.set_stroke, {"opacity": 1}))
            else:
                anims.append(ApplyMethod(part_texts[i].fade))
        self.play(LaggedStart(*anims, group = VGroup(), lag_ratio = 0.3, run_time = 2))
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_2(Scene):
    def construct(self):
        notice5 = Notice("太弱小了", "没有力量")
        notice6 = Notice("大意了", "没有闪")
        notice7 = Notice("趣味字谜", "请　积累")
        notice8 = Notice("技术调整", "请勿惊慌")
        notice9 = Notice("重要问题", "请　思考")

        def align_all(string: str, buff: float = 1.5):
            all_texts = []
            for i in range(26):
                text, _ = caeser(string, i)
                all_texts.append(text)
            mob_texts = MTexText("".join(all_texts), isolate = all_texts)
            part_texts = [mob_texts.get_part_by_tex(text).set_x(2.5) for text in all_texts]
            for i in range(26):
                row = i // 3
                col = i % 3
                part_texts[i].shift(0.6*DOWN*(row-4) + buff*RIGHT*(col-1))
            return mob_texts, part_texts

        keypad = Keypad().shift(3.5*LEFT)
        keypad.get_highlights()
        handle = keypad.get_outer_handle(center = 3.5*LEFT).set_value(25.0)
        cypher_sleep = MTexText("hatte", color = YELLOW_E).shift(3.5*LEFT)
        keypad.decrypt("H", "A", "T", "E")
        _, part_texts = align_all("hatte", buff = 1.8)

        for i in range (26):
            if i == 11: 
                highlight_1 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5)
                self.add(highlight_1)
            elif i == 20:
                highlight_2 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5)
                self.add(highlight_2)
            else:
                part_texts[i].fade()

        self.add(notice5, keypad, cypher_sleep, *part_texts)

        indicate_1 = SurroundingRectangle(part_texts[11], color = BLUE)
        indicate_2 = SurroundingRectangle(part_texts[20], color = BLUE)
        confuse = Text("???", font = "Times New Roman").shift(6*RIGHT + 0.2*DOWN)
        self.play(ShowCreation(indicate_1), ShowCreation(indicate_2), ReplacementTransform(notice5, notice6))
        self.play(Write(confuse))
        self.waiting(1+0-2, 28+18) #额......也没那么灵 （空闲）

        self.waiting(2, 20) #这方法有时候也会出一点小问题
        self.waiting(0, 17) #（空闲）
        self.waiting(2, 0) #经过恺撒密码的加密
        self.play(*[WiggleOutThenIn(mob) for mob in [part_texts[11], part_texts[20], indicate_1, indicate_2, cypher_sleep, highlight_1, highlight_2]])
        self.waiting(0, 14) #有些词恰巧能对应相同的密文
        self.waiting(0, 14) #（空闲）

        rectangle_left = Rectangle(height = 6.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        rectangle_inner = Rectangle(height = 6, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        rectangle_left.add(rectangle_inner).shift(11.5*LEFT + 0.1*UP)
        rectangle_right = Rectangle(height = 6.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        rectangle_inner = Rectangle(height = 6, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        rectangle_right.add(rectangle_inner).shift(11.5*RIGHT + 0.1*UP)
        self.add(rectangle_left).play(rectangle_left.animate.shift(7.2*RIGHT), run_time = 1.9, rate_func = double_bounce)

        pairs = ["sew-cog", "wet-owl", "oui-yes", "all-tee", "haw-pie", "has-exp", "log-two", "paw-tea", "pea-tie", "org-fix", "mew-cum", "folk-iron", "rail-envy", "beef-loop", "spit-date", "noon-deed", "loaf-twin", "much-sain", "tear-pawn", "pear-lawn", "damp-road", "semi-cows", "wheel-dolls", "matte-gunny", "latte-funny", "marry-gulls", "melon-cubed", "furry-sheel", "beefs-adder", "dated-spits", "cheer-jolly", "curly-wolfs", "river-arena", "nulls-tarry", "thumbs-manful"]
        random.shuffle(pairs)
        pairs = ["sleep-bunny"] + pairs
        anim = SpringUp(4*LEFT, pairs, from_center = False, side_length = 4, scale_factor = 1.0)
        mobject = anim.mobject
        self.add(mobject)
        anim.begin()
        beta = ValueTracker(0.0)
        def alter_updater(m):
            alpha = beta.get_value() / 480
            if alpha >= 1:
                anim.finish()
                m.remove_updater(alter_updater)
                self.remove(m)
            anim.interpolate(alpha)
        mobject.add_updater(alter_updater)
        self.play(ReplacementTransform(notice6, notice7), ApplyMethod(beta.set_value, 30, rate_func = linear))
        self.play(ApplyMethod(beta.set_value, 205, rate_func = linear), run_time = 29/6) # 除了我们刚才发现的sleep和bunny之外 这样的词对还有一些 但确实是十分稀有的情况 （空闲）
        
        cute_bunny = MTexText("iazk hatte", isolate = ["iazk", "hatte"], color = YELLOW_E).shift(3*RIGHT + 2*UP)
        text_cute = cute_bunny.get_part_by_tex("iazk")
        text_bunny = cute_bunny.get_part_by_tex("hatte")
        infer_cute = MTexText("只能是cute").scale(0.6).move_to(text_cute).shift(1.2*DOWN)
        arrow_1 = Arrow(text_cute.get_corner(DOWN), infer_cute.get_corner(UP), buff = 0.2, color = GREEN)
        infer_cute.add(arrow_1)
        infer_key = MTexText("前移6位解码").scale(0.6).move_to(infer_cute).shift(1.8*DOWN)
        arrow_2 = Arrow(infer_cute.get_corner(DOWN), infer_key.get_corner(UP), buff = 0.2, color = GREEN)
        infer_key.add(arrow_2)
        infer_bunny = MTexText("是bunny而不是sleep").scale(0.6).move_to(text_bunny).shift(4*DOWN)
        arrow_3 = Arrow(text_bunny.get_corner(DOWN), infer_bunny.get_corner(UP), buff = 0.2, color = GREEN)
        decrypt = MTex("-6", color = GREEN).scale(0.6).move_to(arrow_3).shift(0.3*RIGHT)
        infer_bunny.add(arrow_3, decrypt)

        self.add(rectangle_right, notice7).play(ApplyMethod(rectangle_right.shift, 7.8*LEFT, run_time = 1.9, rate_func = double_bounce), ApplyMethod(beta.set_value, 262, run_time = 1.9, rate_func = linear), ReplacementTransform(notice7, notice8)) 
        self.play(ApplyMethod(beta.set_value, 292, rate_func = linear), Write(cute_bunny), run_time = 1)
        self.play(ApplyMethod(beta.set_value, 322, rate_func = linear), ShowCreationThenDestructionAround(text_bunny), run_time = 1) #再说了 我们即使分辨不出来sleep和bunny
        self.play(FadeIn(infer_cute, 0.5*DOWN), ApplyMethod(beta.set_value, 352, rate_func = linear))
        self.play(FadeIn(infer_key, 0.5*DOWN), ApplyMethod(beta.set_value, 382, rate_func = linear))
        self.play(ApplyMethod(beta.set_value, 407, rate_func = linear), run_time = 5/6) # 还是可以先破译文本中其它的内容
        self.play(FadeIn(infer_bunny, 0.5*DOWN), ApplyMethod(beta.set_value, 437, rate_func = linear))
        self.play(ApplyMethod(beta.set_value, 456, rate_func = linear), run_time = 19/30) #再回过头来反推
        self.play(ApplyMethod(beta.set_value, 480, rate_func = linear), run_time = 0.8) #（空闲）

        self.remove(confuse)
        handle.set_value(0.0)
        self.play(rectangle_left.animate.shift(7.2*LEFT), *[mob.animate.shift(7.8*RIGHT) for mob in [cute_bunny, rectangle_right, infer_cute, infer_key, infer_bunny]], ReplacementTransform(notice8, notice9))
        self.waiting(1, 14) #但是 话说回来
        self.play(ShowCreationThenDestructionAround(cypher_sleep), run_time = 2)
        self.waiting(0, 26) #如果我们只有这一个被加密的单词
        self.waiting(3, 7) #而没有其它的文本这些额外的信息

        confuse_1 = MTex("?").move_to(indicate_1.get_corner(RIGHT)).shift(RIGHT)
        arrow_1 = Arrow(confuse_1.get_corner(LEFT), indicate_1.get_corner(RIGHT), buff = 0.1)
        confuse_1.add(arrow_1)
        confuse_2 = MTex("?").move_to(indicate_2.get_corner(RIGHT)).shift(RIGHT)
        arrow_2 = Arrow(confuse_2.get_corner(LEFT), indicate_2.get_corner(RIGHT), buff = 0.1)
        confuse_2.add(arrow_2)
        self.play(FadeIn(confuse_1, 0.5*LEFT))
        self.waiting(2, 7) #我们还能分辨出它是是由sleep加密而来的
        self.play(FadeIn(confuse_2, 0.5*LEFT))
        self.waiting(1, 0) #还是从bunny加密而来的吗
        self.waiting(4, 26) #到此共46秒
 
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_3(Scene):
    def construct(self):

        notice9 = Notice("重要问题", "请　思考")
        notice10 = Notice("重要结论", "请　验证")
        notice11 = Notice("可爱睡兔", "awsl")
        notice12 = Notice("重要结论", "请　验证")
        notice13 = Notice("核心区别", "请记笔记")

        def align_all(string: str, buff: float = 1.5):
            all_texts = []
            for i in range(26):
                text, _ = caeser(string, i)
                all_texts.append(text)
            mob_texts = MTexText("".join(all_texts), isolate = all_texts)
            part_texts = [mob_texts.get_part_by_tex(text).set_x(2.5) for text in all_texts]
            for i in range(26):
                row = i // 3
                col = i % 3
                part_texts[i].shift(0.6*DOWN*(row-4) + buff*RIGHT*(col-1))
            return mob_texts, part_texts

        keypad = Keypad().shift(3.5*LEFT)
        keypad.get_highlights()
        handle = keypad.get_outer_handle(center = 3.5*LEFT)
        cypher_sleep = MTexText("hatte", color = YELLOW_E).shift(3.5*LEFT)
        keypad.decrypt("H", "A", "T", "E")
        _, part_texts = align_all("hatte", buff = 1.8)

        for i in range (26):
            if i == 11: 
                highlight_1 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5)
                self.add(highlight_1)
            elif i == 20:
                highlight_2 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5)
                self.add(highlight_2)
            else:
                part_texts[i].fade()

        indicate_1 = SurroundingRectangle(part_texts[11], color = BLUE)
        indicate_2 = SurroundingRectangle(part_texts[20], color = BLUE)
        confuse_1 = MTex("?").move_to(indicate_1.get_corner(RIGHT)).shift(RIGHT)
        arrow_1 = Arrow(confuse_1.get_corner(LEFT), indicate_1.get_corner(RIGHT), buff = 0.1)
        confuse_2 = MTex("?").move_to(indicate_2.get_corner(RIGHT)).shift(RIGHT)
        arrow_2 = Arrow(confuse_2.get_corner(LEFT), indicate_2.get_corner(RIGHT), buff = 0.1)
        self.add(notice9, keypad, cypher_sleep, *part_texts, indicate_1, indicate_2, confuse_1, confuse_2, arrow_1, arrow_2)

        confuse_3 = MTex("?").move_to(confuse_2).shift(0.9*UP).scale(5.0, about_edge=LEFT)
        self.play(ReplacementTransform(notice9, notice10), Transform(confuse_1, confuse_3, remover = True), ReplacementTransform(confuse_2, confuse_3))
        self.waiting(2, 22) #很遗憾的是 我们没有任何方法能知道
        self.play(ShowPassingFlashAround(part_texts[11], time_width = 0.2), ShowPassingFlashAround(part_texts[20], time_width = 0.2))
        self.waiting(1, 21) #这个单词到底是从谁加密来的
        self.waiting(0, 13) #（空闲）

        example_cypher_1 = part_texts[5]
        keypad.decrypt()
        self.play(example_cypher_1.animate.move_to(3.5*LEFT).set_fill(color = YELLOW_E, opacity = 1), *[FadeOut(mob) for mob in [cypher_sleep, *part_texts[0:5], *part_texts[6:26], indicate_1, indicate_2, highlight_1, highlight_2, arrow_1, arrow_2, confuse_3]])
        keypad.decrypt("M", "F", "Y", "J")

        _, part_texts = align_all("mfyyj", buff = 1.8)
        all_texts = VGroup(*part_texts)
        self.play(handle.animate.set_value(26.0), ShowIncreasingSubsets(all_texts, int_func = lambda t: np.round(t + 1)), run_time = 2)
        handle.set_value(0.0)
        self.remove(all_texts).add(*part_texts)

        anims = []
        for i in range (26):
            if i == 6: 
                highlight_1 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight_1)
                anims.append(ApplyMethod(highlight_1.set_stroke, {"opacity": 1}))
            elif i == 15:
                highlight_2 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight_2)
                anims.append(ApplyMethod(highlight_2.set_stroke, {"opacity": 1}))
            else:
                anims.append(ApplyMethod(part_texts[i].fade))
        self.play(AnimationGroup(*anims, group = VGroup()))
        indicate_1 = SurroundingRectangle(part_texts[6], color = BLUE)
        indicate_2 = SurroundingRectangle(part_texts[15], color = BLUE)
        self.play(ShowCreation(indicate_1), ShowCreation(indicate_2))
        self.waiting(1, 0)

        example_cypher_2 = part_texts[10]
        keypad.decrypt()
        self.play(example_cypher_2.animate.move_to(3.5*LEFT).set_fill(color = YELLOW_E, opacity = 1), *[FadeOut(mob) for mob in [example_cypher_1, *part_texts[0:10], *part_texts[11:26], indicate_1, indicate_2, highlight_1, highlight_2]])
        keypad.decrypt("W", "P", "I", "T")

        _, part_texts = align_all("wpiit", buff = 1.8)
        all_texts = VGroup(*part_texts)
        self.play(handle.animate.set_value(26.0), ShowIncreasingSubsets(all_texts, int_func = lambda t: np.round(t + 1)), run_time = 2)
        handle.set_value(0.0)
        self.remove(all_texts).add(*part_texts)

        anims = []
        for i in range (26):
            if i == 22: 
                highlight_1 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight_1)
                anims.append(ApplyMethod(highlight_1.set_stroke, {"opacity": 1}))
            elif i == 5:
                highlight_2 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight_2)
                anims.append(ApplyMethod(highlight_2.set_stroke, {"opacity": 1}))
            else:
                anims.append(ApplyMethod(part_texts[i].fade))
        self.play(AnimationGroup(*anims, group = VGroup()))
        indicate_1 = SurroundingRectangle(part_texts[22], color = BLUE)
        indicate_2 = SurroundingRectangle(part_texts[5], color = BLUE)
        self.play(ShowCreation(indicate_1), ShowCreation(indicate_2))
        self.waiting(1, 0)

        example_cypher_3 = part_texts[22]
        keypad.decrypt()
        self.play(example_cypher_3.animate.move_to(3.5*LEFT).set_fill(color = YELLOW_E, opacity = 1), *[FadeOut(mob) for mob in [example_cypher_2, *part_texts[0:22], *part_texts[23:26], indicate_1, indicate_2, highlight_1, highlight_2]])
        keypad.decrypt("S", "L", "E", "P")

        _, part_texts = align_all("sleep", buff = 1.8)
        all_texts = VGroup(*part_texts)
        self.play(handle.animate.set_value(26.0), ShowIncreasingSubsets(all_texts, int_func = lambda t: np.round(t + 1)), run_time = 2)
        handle.set_value(0.0)
        keypad.clear_updaters()
        self.remove(all_texts).add(*part_texts)

        anims = []
        for i in range (26):
            if i == 0: 
                highlight_1 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight_1)
                anims.append(ApplyMethod(highlight_1.set_stroke, {"opacity": 1}))
            elif i == 9:
                highlight_2 = VHighlight(part_texts[i], max_stroke_width = 5, color_bounds = [GREY_C, "#333333"], n_layers = 5).set_stroke(opacity = 0)
                self.bring_to_back(highlight_2)
                anims.append(ApplyMethod(highlight_2.set_stroke, {"opacity": 1}))
            else:
                anims.append(ApplyMethod(part_texts[i].fade))
        self.play(AnimationGroup(*anims, group = VGroup()))
        indicate_1 = SurroundingRectangle(part_texts[0], color = BLUE)
        indicate_2 = SurroundingRectangle(part_texts[9], color = BLUE)
        self.play(ShowCreation(indicate_1), ShowCreation(indicate_2))
        self.waiting(2+3+2 + 2+2+3 + 0 - 17, 24+1+16 + 25+13+0 +24) # 而且 不止这一种情况 无论密文是26种情况中的哪一种 我们都不能知道明文是谁 即使一个用恺撒密码加密的sleep 就在眼前明晃晃地摆着 我们仍然没法判断明文到底是不是bunny （空闲）

        svg_carrot = SVGMobject("Sleep_Carrot.svg", should_center = False, height = None).move_to(100*UP + 200*LEFT)
        svg_bubble = SVGMobject("Sleep_Bubble.svg", should_center = False, height = None).move_to(85*UP + 195*LEFT)
        svg_bunny = SVGMobject("Sleep_Bunny.svg", should_center = False, height = None).move_to(ORIGIN)
        svg_sleep = VGroup(svg_bubble, svg_carrot)
        group_svg = VGroup(svg_bunny, svg_bubble, svg_carrot).scale(0.015, about_point = ORIGIN).shift(2.5*LEFT + 0.5*DOWN)

        text_sleep = part_texts[0]
        text_bunny = part_texts[9]
        keypad.decrypt()
        self.play(FadeOut(keypad), FadeOut(example_cypher_3), text_sleep.animate.shift(1.5*DOWN + 1*RIGHT), text_bunny.animate.shift(1.5*DOWN + 1*RIGHT), *[FadeOut(mob, 1.5*DOWN + 1*RIGHT) for mob in [*part_texts[1:9], *part_texts[10:26], indicate_1, indicate_2, highlight_1, highlight_2]], ReplacementTransform(notice10, notice11))
        self.play(ShowCreation(svg_bunny), ShowCreation(svg_sleep), run_time = 2) #如果我们只需要加密sleep和bunny
        
        picture_ceasar = ImageMobject("picture_Caesar.png", height = 8).shift(5*RIGHT + 3*DOWN)
        bubble = Union(Ellipse(width = 2.2, height = 1.1), Triangle().scale(0.5).rotate(-PI/12).shift(0.5*RIGHT + 0.4*DOWN)).shift(4*RIGHT + 2*UP)
        perfect = Text("完美。", font = "simsun").scale(0.8).shift(4*RIGHT + 2*UP)
        talk = VGroup(bubble, perfect)
        brutus = Intersection(Knife().rotate(PI/2).shift(3.2*DOWN+5*RIGHT), Rectangle(height = 1, width = 6).shift(3.2*DOWN + 17/9*RIGHT)).set_fill(opacity = 1).set_stroke(width = 0)
        raising = Group(picture_ceasar, brutus)
        raising.save_state()
        alpha = ValueTracker(3.0)
        def raising_updater(mob: Mobject):
            distance = alpha.get_value()
            mob.restore().rotate(-distance*0.5, about_point = mob.get_corner(DL)).shift(distance**2 * DOWN)
        raising.add_updater(raising_updater)
        self.add(raising)
        self.play(alpha.animate.set_value(0.0))
        raising.clear_updaters()
        self.play(FadeInFromPoint(talk, talk.get_corner(DR) + 0.3*DOWN), run_time = 0.5)
        self.waiting(0.5, 21) #那么恺撒密码完美地完成了任务
        self.play(raising.animate.shift(8*DOWN), talk.animate.shift(8*DOWN))
        self.remove(raising, talk)
        self.waiting(0, 13) #它就是安全的
        self.waiting(0, 20) #（空闲）
        
        COLOR_S = rate_color(11/26)
        COLOR_B = rate_color(20/26)
        anim1 = Transform(text_sleep, text_sleep.copy().move_to(2.5*UP + 5.5*LEFT).set_color(COLOR_S), path_arc = PI/4)
        anim2 = Transform(text_bunny, text_bunny.copy().move_to(2.5*DOWN + 2.5*LEFT).set_color(COLOR_B), path_arc = -PI/4)
        self.play(anim1, anim2, svg_sleep.animate.set_color(COLOR_S), svg_bunny.animate.set_color(COLOR_B), ReplacementTransform(notice11, notice12))
        self.waiting(1, 2) #sleep和bunny这一对词

        line_title = Line(3*UP + 6*LEFT, 3*UP + 6*RIGHT).insert_n_curves(64)
        title = Text("完美加密", font = "simsun", color = YELLOW).next_to(3*UP, UP).add(line_title)
        
        keypad = Keypad().scale(0.6).shift(2.5*RIGHT)
        keypad.save_state()
        alpha = ValueTracker(0.0)
        def updater_wheel(mob: VMobject):
            ratio = (clip(alpha.get_value(), 0.5, 2)-0.5) / 1.5
            distance = 6.5 * (1-rush_from(ratio))
            mob.restore().rotate(-distance/1.8).shift(distance * RIGHT)
        keypad.add_updater(updater_wheel)
        self.add(keypad)
        self.play(UnRolled(title), alpha.animate.set_value(3.0), rate_func = linear, run_time = 3)
        keypad.clear_updaters()
        self.waiting(2+1-3, 27+19) #能用恺撒密码这种最弱的加密方法 做到完美加密
        self.waiting(1, 21) #特殊就特殊在

        def small_align(string: str, buff: float = 1):
            all_texts = []
            for i in range(26):
                text, _ = caeser(string, i)
                all_texts.append(text)
            mob_texts = MTexText("".join(all_texts), isolate = all_texts).scale(0.6)
            part_texts = [mob_texts.get_part_by_tex(text).set_x(2.5) for text in all_texts]
            for i in range(26):
                row = i // 5
                col = i % 5
                part_texts[i].shift(0.4*DOWN*(row-2.5) + buff*RIGHT*(col-2))
            return mob_texts, part_texts

        mob_texts_sleep, part_texts_sleep = small_align("sleep")
        mob_texts_sleep.shift(1.5*UP).set_color(COLOR_S).save_state()
        mob_texts_bunny, part_texts_bunny = small_align("bunny")
        mob_texts_bunny.shift(1.5*DOWN).set_color(COLOR_B).save_state()

        alpha = ValueTracker(0.0)
        def keypad_updater(mob: Keypad):
            angle = alpha.get_value()
            mob.restore().scale(np.array([np.cos(angle), 1, 1]))
            if angle >= PI/2:
                mob.clear_updaters()
                self.remove(mob).add(mob_texts_sleep, mob_texts_bunny)
                mob_texts_sleep.add_updater(texts_updater)
                mob_texts_bunny.add_updater(texts_updater)
        keypad.add_updater(keypad_updater)
        def texts_updater(mob: MTexText):
            angle = alpha.get_value()
            mob.restore().scale(np.array([-np.cos(angle), 1, 1]))
        self.play(alpha.animate.set_value(PI))
        self.remove(mob_texts_sleep, mob_texts_bunny).add(*part_texts_sleep, *part_texts_bunny)
        self.waiting(0, 26) # 用恺撒密码加密后

        anim_1 = LaggedStart(*[ApplyMethod(part_texts_sleep[(i+15)%26].set_color, rate_color(i/26)) for i in range(26)], lag_ratio = 0.3, run_time = 2)
        anim_2 = LaggedStart(*[ApplyMethod(part_texts_bunny[(i+6)%26].set_color, rate_color(i/26)) for i in range(26)], lag_ratio = 0.3, run_time = 2)
        surrounding_sleep = Rectangle(height = 2.5, width = 5.1, color = COLOR_S).shift(1.5*UP + 2.5*RIGHT).scale(np.array([1, -1, 1]), min_scale_factor = -1)
        surrounding_bunny = Rectangle(height = 2.5, width = 5.1, color = COLOR_B).shift(1.5*DOWN + 2.5*RIGHT)
        equal = MTex("=").rotate(PI/2).shift(2.5*RIGHT)
        self.play(anim_1, anim_2)
        self.play(ShowCreation(surrounding_sleep), ShowCreation(surrounding_bunny), Write(equal))
        self.waiting(0, 13) #这两个单词所有可能的密文是相同的
        self.waiting(0, 19) #（空闲）

        hatte = MTexText("hatte", color = YELLOW_A).shift(2.5*LEFT + 2*UP)
        arrow_sleep = Arrow(2.5*UP + 5*LEFT, 2*UP + 3*LEFT, color = COLOR_S)
        arrow_bunny = Arrow(0.1*DR + 1.5*LEFT, 0.1*DR + 2*UP + 2*LEFT, color = COLOR_B)
        self.play(TransformFromCopy(part_texts_sleep[15], hatte.copy(), remover = True), TransformFromCopy(part_texts_bunny[6], hatte.copy(), remover = True), ShowCreation(arrow_sleep), ShowCreation(arrow_bunny), *[mob.animate.fade(0.8) for mob in [*part_texts_sleep[0:15], *part_texts_sleep[16:26], *part_texts_bunny[0:6], *part_texts_bunny[7:26]]])
        self.add(hatte)
        self.waiting(0, 28) #如果我们只得到了密文
        self.waiting(2, 6) #而不知道之前加密的时候

        arrow_sleep.save_state()
        arrow_bunny.save_state()
        alpha = ValueTracker(0.0)
        def rotating_updater(mob: Arrow):
            ratio = alpha.get_value()
            mob.restore().rotate(ratio*PI).set_color(interpolate_color(mob.get_color(), YELLOW_A, ratio))
        arrow_sleep.add_updater(rotating_updater)
        arrow_bunny.add_updater(rotating_updater)
        self.play(part_texts_sleep[15].animate.fade(0.8), part_texts_bunny[6].animate.fade(0.8), alpha.animate.set_value(1.0))
        arrow_sleep.clear_updaters()
        arrow_bunny.clear_updaters()
        self.waiting(1, 2) #字母到底移动了几位

        confuse_sleep = MTex("?", color = YELLOW_A).move_to(arrow_sleep.get_center()+0.3*(UP+0.25*RIGHT))
        confuse_bunny = MTex("?", color = YELLOW_A).move_to(arrow_bunny.get_center()+0.3*(RIGHT+0.25*UP))
        self.play(Write(confuse_sleep, remover = True), Write(confuse_bunny, remover = True))
        arrow_sleep.add(confuse_sleep)
        arrow_bunny.add(confuse_bunny)
        self.waiting(1, 20) #那么 我们就会无计可施
        self.waiting(1, 21) #最好的破解方法
        indicate_sleep = SurroundingRectangle(text_sleep, color = BLUE)
        indicate_bunny = SurroundingRectangle(text_bunny, color = BLUE)
        self.play(ShowCreation(indicate_sleep), arrow_bunny.animate.fade(0.8))
        self.play(ShowCreation(indicate_bunny), Uncreate(indicate_sleep), arrow_bunny.animate.set_opacity(1), arrow_sleep.animate.fade(0.8))
        self.play(Uncreate(indicate_bunny), arrow_sleep.animate.set_opacity(1))
        self.waiting(2+0-3, 23+19) #也只能是闭着眼睛随便挑一个罢了 （空闲）

        self.remove(indicate_sleep, indicate_bunny, arrow_sleep, arrow_bunny, text_sleep, text_bunny, svg_sleep, svg_bunny, surrounding_sleep, surrounding_bunny, equal, title, *part_texts_sleep, *part_texts_bunny, hatte)
        
        text_message = "At first glance, messages encrypted\nusing the Ceasar Cipher look\n“scrambled” (unless key is known).\nHowever, to break the scheme\nwe just need to try all possible keys\n(which is easily done) and see\nif the resulting plaintext is “readable”." # If the message is relatively long, the scheme is easily broken.
        text_cypher, _ = caeser(text_message, 5)
        message = Text(text_message, font = "Times New Roman").scale(0.6).next_to(2*UP + 6.7*LEFT)
        cypher = Text(text_cypher, font = "Times New Roman", color = YELLOW_E).scale(0.6).next_to(1.5*DOWN + 6.7*LEFT)
        orderless = Text("（看上去）没有规律", font = "simsun", color = YELLOW_E).scale(0.6).shift(0.25*UP + 4*LEFT)
        self.play(Write(message), ReplacementTransform(notice12, notice13))
        self.play(TransformFromCopy(message, cypher))
        self.waiting(0, 12) #这听起来和古典密码学的思路有一些不一样
        self.waiting(1, 25) #古典密码学的加密目标
        self.play(Write(orderless))
        self.waiting(1, 11) #是力争让密文没有“规律”

        _, part_texts_hatte = small_align("hatte")
        for i in range(26):
            part_texts_hatte[i].set_color(rate_color(i/26)).shift(2*UP)
        self.play(*[FadeIn(mob) for mob in part_texts_hatte])
        self.waiting(1, 16) #但实际上sleep和bunny的密文

        line_sleep = Line(0.5*LEFT, 0.5*RIGHT, color = RED).move_to(part_texts_hatte[11])
        line_bunny = Line(0.5*LEFT, 0.5*RIGHT, color = RED).move_to(part_texts_hatte[20])
        self.play(ShowCreation(line_sleep), ShowCreation(line_bunny))
        self.waiting(1, 14) #只有24个没有规律的组合

        _, part_texts_ceaser = small_align("vxtlxk", buff = 1.1)
        for i in range(26):
            part_texts_ceaser[i].set_color(rate_color(i/26)).shift(1*DOWN+0.2*RIGHT)
        self.play(*[FadeIn(mob) for mob in part_texts_ceaser])
        self.waiting(0, 13) #而一般的单词

        line_ceaser = Line(0.5*LEFT, 0.5*RIGHT, color = RED).move_to(part_texts_ceaser[7])
        self.play(ShowCreation(line_ceaser))
        self.waiting(2, 2) #密文却有25种没有规律的组合
        self.waiting(1, 8) #某种意义上
        self.waiting(3, 10) #sleep和bunny的密文甚至更有规律一点

        self.waiting(1, 0) #到此共83秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_4(Scene):
    def construct(self):

        notice13 = Notice("核心区别", "请记笔记")
        notice14 = Notice("首尾呼应", "请　模仿")

        def small_align(string: str, buff: float = 1):
            all_texts = []
            for i in range(26):
                text, _ = caeser(string, i)
                all_texts.append(text)
            mob_texts = MTexText("".join(all_texts), isolate = all_texts).scale(0.6)
            part_texts = [mob_texts.get_part_by_tex(text).set_x(2.5) for text in all_texts]
            for i in range(26):
                row = i // 5
                col = i % 5
                part_texts[i].shift(0.4*DOWN*(row-2.5) + buff*RIGHT*(col-2))
            return mob_texts, part_texts

        text_message = "At first glance, messages encrypted\nusing the Ceasar Cipher look\n“scrambled” (unless key is known).\nHowever, to break the scheme\nwe just need to try all possible keys\n(which is easily done) and see\nif the resulting plaintext is “readable”." # If the message is relatively long, the scheme is easily broken.
        text_cypher, _ = caeser(text_message, 5)
        message = Text(text_message, font = "Times New Roman").scale(0.6).next_to(2*UP + 6.7*LEFT)
        cypher = Text(text_cypher, font = "Times New Roman", color = YELLOW_E).scale(0.6).next_to(1.5*DOWN + 6.7*LEFT)
        orderless = Text("（看上去）没有规律", font = "simsun", color = YELLOW_E).scale(0.6).shift(0.25*UP + 4*LEFT)
        
        _, part_texts_hatte = small_align("hatte")
        for i in range(26):
            part_texts_hatte[i].set_color(rate_color(i/26)).shift(2*UP)
        _, part_texts_ceaser = small_align("vxtlxk", buff = 1.1)
        line_sleep = Line(0.5*LEFT, 0.5*RIGHT, color = RED).move_to(part_texts_hatte[11])
        line_bunny = Line(0.5*LEFT, 0.5*RIGHT, color = RED).move_to(part_texts_hatte[20])
        
        for i in range(26):
            part_texts_ceaser[i].set_color(rate_color(i/26)).shift(1*DOWN+0.2*RIGHT)
        line_ceaser = Line(0.5*LEFT, 0.5*RIGHT, color = RED).move_to(part_texts_ceaser[7])
        
        self.add(notice13, message, cypher, orderless, *part_texts_hatte, *part_texts_ceaser, line_sleep, line_bunny, line_ceaser)

        rectangle_right = Rectangle(height = 6.4, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        rectangle_inner = Rectangle(height = 6.2, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        rectangle_right.add(rectangle_inner).shift(11.5*RIGHT + 0.25*UP)
        
        self.add(rectangle_right, notice13).play(ApplyMethod(rectangle_right.shift, 7.5*LEFT, run_time = 2, rate_func = double_bounce))
        self.remove(*part_texts_hatte, *part_texts_ceaser, line_sleep, line_bunny, line_ceaser)
        self.waiting(1, 3) # 这就是现代密码学最重要的观点
        
        line = Line(orderless.get_corner(LEFT)+0.5*LEFT, orderless.get_corner(RIGHT)+0.5*RIGHT, color = RED)
        self.play(ShowCreation(line))
        self.waiting(2, 2) # 完美的加密不依赖密文没有“规律”

        COLOR_S = rate_color(11/26)
        COLOR_B = rate_color(20/26)
        mob_texts_sleep, part_texts_sleep = small_align("sleep")
        mob_texts_sleep.shift(2*UP).scale(0.9, about_point = 5*RIGHT).set_color(COLOR_S)
        mob_texts_bunny, part_texts_bunny = small_align("bunny")
        mob_texts_bunny.shift(1.5*DOWN).scale(0.9, about_point = 5*RIGHT).set_color(COLOR_B)
        surrounding_sleep = Rectangle(height = 2.5, width = 5.1, color = COLOR_S).shift(2*UP + 2.5*RIGHT).scale(0.9, about_point = 5*RIGHT).scale(np.array([1, -1, 1]), min_scale_factor = -1)
        surrounding_bunny = Rectangle(height = 2.5, width = 5.1, color = COLOR_B).shift(1.5*DOWN + 2.5*RIGHT).scale(0.9, about_point = 5*RIGHT)
        equal = Text("（实际上）没有区别", font = "simsun", color = BLUE).scale(0.6).shift(0.25*UP + 2.75*RIGHT)

        self.play(FadeIn(mob_texts_sleep, 0.5*DOWN), FadeIn(mob_texts_bunny, 0.5*UP))
        anim_1 = LaggedStart(*[ApplyMethod(part_texts_sleep[(i+15)%26].set_color, rate_color(i/26)) for i in range(26)], lag_ratio = 0.3, run_time = 2)
        anim_2 = LaggedStart(*[ApplyMethod(part_texts_bunny[(i+6)%26].set_color, rate_color(i/26)) for i in range(26)], lag_ratio = 0.3, run_time = 2)
        self.play(anim_1, anim_2)
        self.play(ShowCreation(surrounding_sleep), ShowCreation(surrounding_bunny), Write(equal))
        self.waiting(3+1-4, 14+20) # 它所依赖的 是不同的明文能得到的密文之间，没有“区别”
        self.waiting(0, 24) #（空闲）

        self.waiting(3, 11) # 只要sleep和bunny能移位出相同的结果
        self.waiting(2, 6) # 那么在只看密文的时候
        self.waiting(2, 17) # 它们就永远也不可能被区分出来
        self.waiting(0, 25) #（空闲）

        left_group = [message, cypher, orderless, line]
        right_group = [rectangle_right, mob_texts_sleep, mob_texts_bunny, surrounding_sleep, surrounding_bunny, equal]
        self.play(*[mob.animate.shift(7.5*LEFT) for mob in left_group], *[mob.animate.shift(7.5*RIGHT) for mob in right_group], ReplacementTransform(notice13, notice14))
        self.remove(*left_group, *right_group)
        self.waiting(2, 1) # 所以 恺撒密码什么时候是安全的呢？
        self.waiting(0, 18) #（空闲）
        
        keypad = Keypad().shift(3.5*LEFT)
        copy_inner = keypad.inner.copy()
        copy_outer = keypad.outer.copy()
        alpha = ValueTracker(PI/4)
        def updater_outer(mob: VMobject):
            angle = alpha.get_value()
            mob.become(keypad.outer).rotate(angle)
        copy_outer.add_updater(updater_outer)
        def updater_inner(mob: VMobject):
            angle = alpha.get_value()
            mob.become(keypad.inner).rotate(-angle)
        copy_inner.add_updater(updater_inner)
        shade = SurroundingRectangle(keypad, fill_color = "#333333", fill_opacity = 1, stroke_width = 0)

        self.bring_to_back(copy_outer, copy_inner, shade)
        self.play(alpha.animate.set_value(0.0), FadeOut(shade))
        copy_outer.clear_updaters()
        copy_inner.clear_updaters()
        self.remove(copy_outer, copy_inner).add(keypad)
        self.waiting(2, 0) #这个问题的答案应该已经很明显了

        c = MTexText("c").shift(2*UP + 2.5*RIGHT)

        all_texts = []
        for i in range(26):
            text, _ = caeser("c", i)
            all_texts.append(text)
        mob_texts = MTexText("".join(all_texts), isolate = all_texts, color = YELLOW_E)
        part_texts = [mob_texts.get_part_by_tex(text).set_x(2.5) for text in all_texts]
        for i in range(26):
            row = i // 7
            col = i % 7
            part_texts[i].shift(0.6*DOWN*(row-1.5) + 0.4*RIGHT*(col-3))

        self.play(Write(c))
        keypad.get_highlights()
        handle = keypad.get_handle(center = 3.5*LEFT)
        keypad.encrypt("C")
        self.play(handle.animate.set_value(26.0), ShowIncreasingSubsets(mob_texts, int_func = lambda t: np.round(t + 1)), run_time = 4)   
        keypad.clear_updaters()
        self.waiting(3+2-5, 6+28) # 如果我们用恺撒密码加密单个的字符 那么密文可能是任何一个字母
        self.waiting(3, 20) # 这样的恺撒密码是绝对安全的完美加密方案
        self.waiting(1, 21) # 绝对不可能被破解
        self.waiting(0, 15) #（空闲）

        text_message = "perfect secrecy"
        text_letter = "perfectsecrecy"
        cypher_letter = ""
        shifting = []
        example = Text(text_message, font = "Times New Roman").scale(0.8).shift(9*UP)
        example_letter = Text(text_message, font = "Times New Roman").scale(0.8).shift(1.5*UP)
        for i in range(14):
            example_letter[i].set_x(0.9*(i-6.5))
            shift = random.randint(0, 25)
            shifting.append(shift)
            cypher, _ = caeser(text_letter[i], shift)
            cypher_letter += cypher
        example_cypher = Text(cypher_letter, font = "Times New Roman", color = YELLOW_E).scale(0.8).shift(1.5*DOWN)
        arrows = VGroup()
        texts = VGroup()
        for i in range(14):
            example_cypher[i].set_x(0.9*(i-6.5))
            arrow = Arrow(1*UP, 1*DOWN, buff = 0).shift(0.9*(i-6.5)*RIGHT)
            text = MTex("+" + str(shifting[i])).scale(0.5).shift((0.9*(i-6.5) + 0.3)*RIGHT)
            arrows.add(arrow)
            texts.add(text)
        arrows.set_color(BLUE)
        texts.set_color(BLUE)
            
        removing = [keypad, keypad.tips, c, mob_texts]
        self.play(*[mob.animate.shift(7.5*DOWN) for mob in removing], example.animate.shift(7.5*DOWN))
        self.remove(*removing)
        self.play(Transform(example, example_letter))
        self.play(FadeIn(arrows, 0.5*DOWN), FadeIn(texts, 0.5*DOWN), lag_ratio = 0.05)
        self.play(ShowIncreasingSubsets(example_cypher))
        self.waiting(1+3-4, 19+14) #如果一段文本中 我们把每个字母都独立使用恺撒密码加密
        self.waiting(2, 28) #那么 这段密文就绝对安全了

        self.waiting(3, 8)
        self.play(*[FadeOut(mob) for mob in [example, arrows, texts, example_cypher, notice14]])
        self.waiting(3, 0) #到此共55秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

######################################################################################################

class Chapter2_0(Scene):

    def construct(self):

        ##  Making object
        text2 = Text("第二节 加密方案", font = 'simsun', t2c={"第二节": YELLOW, "加密": GREEN, "方案": BLUE})

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(Scene):
    def construct(self):

        notice1 = Notice("前情提要", "请　复习")
        notice2 = Notice("正式名词", "请记笔记")
        notice3 = Notice("前情提要", "请　复习")
        notice4 = Notice("核心区别", "请　牢记")
        notice5 = Notice("前情提要", "请　复习")


        def small_align(string: str, buff: float = 1):
            all_texts = []
            for i in range(26):
                text, _ = caeser(string, i)
                all_texts.append(text)
            mob_texts = MTexText("".join(all_texts), isolate = all_texts).scale(0.6)
            part_texts = [mob_texts.get_part_by_tex(text).set_x(2.5) for text in all_texts]
            for i in range(26):
                row = i // 5
                col = i % 5
                part_texts[i].shift(0.4*DOWN*(row-2.5) + buff*RIGHT*(col-2))
            return mob_texts, part_texts

        def align_all(string: str, buff: float = 1.5):
            all_texts = []
            for i in range(26):
                text, _ = caeser(string, i)
                all_texts.append(text)
            mob_texts = MTexText("".join(all_texts), isolate = all_texts)
            part_texts = [mob_texts.get_part_by_tex(text).set_x(2.5) for text in all_texts]
            for i in range(26):
                row = i // 3
                col = i % 3
                part_texts[i].shift(0.6*DOWN*(row-4) + buff*RIGHT*(col-1))
            return mob_texts, part_texts

        self.play(Write(notice1))
        self.waiting(2, 5) #我们先来复习一下刚才的内容吧

        mark_outer = Circle(radius = 3.6, stroke_color = WHITE, fill_color = "#333333", fill_opacity = 1)
        mark_inner = Circle(radius = 3.5, color = WHITE)
        number = 78
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
        outer_layer = VGroup(marks, outer_text, outer_gear, outer_number).scale(0.6, about_point = ORIGIN)
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
        number = 78
        marks = VGroup()
        for i in range (number):
            angle = i * TAU / number
            mark_i = Line(1.5*unit(angle), 1.4*unit(angle), color = YELLOW_E)
            marks.add(mark_i)
        marks.add(mark_outer, mark_inner)
        inner_layer = VGroup(inner_gear, inner_text, marks, inner_number).scale(0.6, about_point = ORIGIN)

        copy_inner = inner_layer.copy()
        copy_outer = outer_layer.copy()
        alpha = ValueTracker(PI/4)
        def updater_outer(mob: VMobject):
            angle = alpha.get_value()
            mob.become(outer_layer).rotate(angle)
        copy_outer.add_updater(updater_outer)
        def updater_inner(mob: VMobject):
            angle = alpha.get_value()
            mob.become(inner_layer).rotate(-angle)
        copy_inner.add_updater(updater_inner)
        shade = SurroundingRectangle(outer_layer, fill_color = "#333333", fill_opacity = 1, stroke_width = 0)
        
        self.add(copy_outer, copy_inner, shade)
        self.play(alpha.animate.set_value(0.0), FadeOut(shade))
        copy_outer.clear_updaters()
        copy_inner.clear_updaters()
        self.remove(copy_outer, copy_inner).add(outer_layer, inner_layer)
        self.waiting(0, 21) #对于一套加密方案
        self.waiting(2, 2) #比如恺撒密码来说

        text_sleep = MTexText("sleep").shift(4.5*LEFT + UP)
        text_bunny = MTexText("bunny").shift(4.5*LEFT + DOWN)
        arrow = Arrow(3.5*LEFT, 3.5*RIGHT, color = BLUE)
        text_hatte = MTexText("hatte", color = YELLOW_E).shift(4.5*RIGHT)
        self.play(Write(text_sleep), Write(text_bunny))
        self.bring_to_back(arrow).play(ShowCreation(arrow))
        self.play(Write(text_hatte))
        self.waiting(0, 11) #如果它能把不同的明文加密成相同的密文

        alpha = ValueTracker(0.0)
        def color_updater(mob: VMobject):
            ratio = alpha.get_value()
            mob.set_color(interpolate_color(BLUE, GREEN, ratio))
        arrow.add_updater(color_updater)
        self.play(Rotate(arrow, PI, about_point = ORIGIN), Rotate(outer_layer, PI, about_point = ORIGIN), Rotate(inner_layer, -PI, about_point = ORIGIN), alpha.animate.set_value(1.0))
        self.waiting(0, 26) #那么没有任何方法

        surrounding_sleep = SurroundingRectangle(text_sleep, color = BLUE)
        surrounding_bunny = SurroundingRectangle(text_bunny, color = BLUE)
        confusing = MTexText("???").shift(4.5*LEFT)
        self.play(ShowCreation(surrounding_sleep), ShowCreation(surrounding_bunny))
        self.play(Write(confusing))
        self.waiting(0, 23) #能从密文中反向还原出明文来
        self.waiting(0, 19) #（空闲）

        self.play(*[FadeOut(mob) for mob in [surrounding_sleep, surrounding_bunny, confusing, text_sleep, text_bunny, arrow, text_hatte]], ReplacementTransform(notice1, notice2))
        self.waiting(0, 13) #更具体地说

        title_scheme = Text("加密方案", font = "simsun", color = BLUE).shift(2.8*UP)
        blocks = []
        block_per_layer = [2, 3, 4, 4, 4, 4, 3, 2]
        order = 0
        numbers = []
        for i in range(8):
            number = block_per_layer[i]
            for j in range(number):
                position = 0.6*UP*(i-3.5) + 1.2*RIGHT*(j-(number-1)/2)
                block_i = Block(order).shift(position)
                blocks.append(block_i)
                number_i = MTex(str(order), color = BLUE_D).scale(0.9).shift(position)
                numbers.append(number_i)
                order += 1
        spreading = blocks + [title_scheme]
        spreading = spreading[::-1]
        background_scheme = Square(side_length = 4.8, stroke_width = 0, fill_opacity = 1, fill_color = "#333333")
        self.bring_to_back(background_scheme)
        
        self.play(Write(title_scheme))
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in blocks], lag_ratio = 0.1), run_time = 3)
        self.waiting(1, 5) #一套加密方案 是由很多对加密算法和解密算法组成的
        self.waiting(1, 19) #在恺撒密码中

        self.play(LaggedStart(*[mob.animate.shift(0.25*mob.get_center()) for mob in spreading]), run_time = 2)
        self.waiting(1, 0) #加密和解密的算法一共有26对
        alpha = ValueTracker(0.0)
        def shrinking(mob: VMobject):
            position = mob.get_center()
            norm = get_norm(position)
            def util(mob: VMobject):
                value = clip(alpha.get_value(), 0.55*norm, 1.25*norm)
                ratio = (value/norm - 0.55) / 3.5
                mob.restore().shift(-ratio * position)
            mob.add_updater(util)
        for mob in spreading:
            mob.save_state()
            shrinking(mob)
        self.play(alpha.animate.set_value(5.0), run_time = 2)
        for mob in spreading:
            mob.clear_updaters()
        self.waiting(0, 12) # 每一种都是一种位移字母的方式
        self.waiting(0, 21) #（空闲）
            
        text_sleep = MTexText("sleep").shift(4*LEFT)
        arrow = Arrow(3*LEFT, 3*RIGHT, color = BLUE, buff = 0, stroke_width = 10)
        text_hatte = MTexText("hatte", color = YELLOW_E).shift(4*RIGHT)
        chosen = SurroundingRectangle(blocks[15], buff = 0)
        self.play(Write(text_sleep))
        self.waiting(2, 20) #每当我们使用恺撒密码加密一段字符的时候
        self.play(ShowCreation(chosen))
        self.bring_to_back(arrow).play(ShowCreation(arrow))
        self.play(Write(text_hatte))
        self.waiting(2+1-3, 1+27) #我们就要从这些方法中 随机挑选一对

        notation = Text("*密钥的读音一直是争论的重灾区，\n我按照我习惯的读法读作yào。\n大家不要打架，打架没有金坷垃。", font = "simsun").scale(0.4).shift(4*RIGHT + 2*DOWN)
        self.play(FadeIn(notation, 0.5*UP))
        self.waiting(2, 15) #这个挑选的过程就叫密钥生成
        self.play(FadeOut(notation))
        self.waiting(0, 18) #在恺撒密码中

        self.play(LaggedStart(*[FadeIn(mob, scale = 0.6) for mob in numbers], lag_ratio = 0.1), run_time = 3)
        self.waiting(0, 16) #我们可以用1 2 3这些偏移量
        self.waiting(1, 17) #来表示这些密钥
        self.waiting(0, 23) #（空闲）

        text_message = "At first glance, messages\nencrypted using the Ceasar\nCipher look “scrambled”\n(unless key is known).\nHowever, to break the scheme\nwe just need to try all possible\nkeys (which is easily done)\nand see if the resulting\nplaintext is “readable”." # If the message is relatively long, the scheme is easily broken.
        text_cypher, _ = caeser(text_message, 5)
        message_long = Text(text_message, font = "Times New Roman").scale(0.5).move_to(5*LEFT)
        cypher_long = Text(text_cypher, font = "Times New Roman", color = YELLOW_E).scale(0.5).move_to(5*RIGHT)
        title_message = Text("明文", font = "simsun", color = WHITE).shift(2.8*UP + 4*LEFT)
        title_cypher = Text("密文", font = "simsun", color = YELLOW_E).shift(2.8*UP + 4*RIGHT)
        shade_title = SurroundingRectangle(title_scheme, stroke_width = 0, fill_opacity = 1, fill_color = "#333333")
        arrow_title = Arrow(2.5*LEFT + 2.8*UP, 2.5*RIGHT + 2.8*UP, stroke_width = 10, buff = 0, color = BLUE)
        
        self.play(FadeIn(message_long, 0.5*DOWN), Write(title_message), *[FadeOut(mob, 0.5*DOWN) for mob in [text_sleep, arrow, text_hatte]], FadeOut(chosen))
        self.waiting(1, 7) #原本的字符叫做明文
        chosen = SurroundingRectangle(blocks[5], buff = 0)
        self.play(ShowCreation(chosen))
        self.bring_to_back(arrow).play(ShowCreation(arrow, rate_func = squish_rate_func(smooth, 0, 2/3)), FadeIn(cypher_long, 0.5*RIGHT, rate_func = squish_rate_func(smooth, 1/3, 1)), run_time = 1.5)
        self.waiting(0, 9) #在经过随机挑选的算法的加密后
        self.bring_to_back(arrow_title, shade_title).play(ShowCreation(arrow_title, rate_func = squish_rate_func(smooth, 0, 2/3)), Write(title_cypher, rate_func = squish_rate_func(smooth, 1/3, 1)), run_time = 1.5)
        self.waiting(1.5, 0) #这段字符就会变成相应的密文

        self.play(ShowCreationThenDestructionAround(cypher_long, run_time = 2), ReplacementTransform(notice2, notice3))
        self.waiting(0, 6) #这些密文看起来毫无规律
        self.waiting(2, 15) #古典密码学基本就满足于此了
        self.waiting(0, 16) #（空闲）

        self.play(FadeOut(message_long), FadeOut(cypher_long), FadeOut(chosen))
        self.waiting(1, 28) #但我们知道 这是不够的

        message_bunny = MTexText("bunny", color = RED_A).shift(UP + 4.5*LEFT)
        mob_texts_bunny, _ = small_align("bunny")
        mob_texts_bunny.scale(0.7, about_point = 2.5*RIGHT).shift(1.0*UP + 2.5*RIGHT).set_color(interpolate_color(YELLOW_E, RED, 0.2))
        background_bunny = Rectangle(width = 3.5, height = 1.68, color = RED_A, fill_opacity = 0.2).shift(5*RIGHT+UP)
        message_wheel = MTexText("wheel", color = GREEN_A).shift(DOWN + 4.5*LEFT)
        mob_texts_wheel, _ = small_align("wheel")
        mob_texts_wheel.scale(0.7, about_point = 2.5*RIGHT).shift(1.0*DOWN + 2.5*RIGHT).set_color(interpolate_color(YELLOW_E, GREEN, 0.2))
        background_wheel = Rectangle(width = 3.5, height = 1.68, color = GREEN_A, fill_opacity = 0.2).shift(5*RIGHT+DOWN)
        not_equal = MTex(r"\ne", color = GREEN).scale(0.7).rotate(PI/2).shift(5*RIGHT)

        self.play(Write(message_bunny), Write(message_wheel))
        self.play(FadeIn(mob_texts_bunny, 0.5*RIGHT), FadeIn(mob_texts_wheel, 0.5*RIGHT))
        self.bring_to_back(background_bunny, background_wheel).play(ShowCreation(background_bunny), ShowCreation(background_wheel))
        self.play(Write(not_equal))
        self.waiting(0, 5) #只要不同的明文生成的密文可以被找到区别

        title_encrypt = Text("加密方案", font = "simsun", color = BLUE).shift(2.8*UP)
        title_attack = Text("强行解密", font = "simsun", color = GREEN).shift(2.8*UP)
        alpha = ValueTracker(0.0)
        arrow_upper = Arrow(3*LEFT + DOWN, 3*RIGHT + DOWN, buff = 0, color = GREEN)
        arrow_lower = Arrow(3*LEFT + UP, 3*RIGHT + UP, buff = 0, color = GREEN)
        def fading_out_updater(mob: VMobject):
            ratio = alpha.get_value()
            mob.set_opacity(1 - ratio)
        def fading_in_updater(mob: VMobject):
            ratio = alpha.get_value()
            mob.set_opacity(ratio)
        def color_updater(mob: VMobject):
            ratio = alpha.get_value()
            mob.set_color(interpolate_color(BLUE, GREEN, ratio))
        arrow.add_updater(fading_out_updater)
        arrow_upper.add_updater(fading_in_updater)
        arrow_lower.add_updater(fading_in_updater)
        arrow_title.add_updater(color_updater)
        self.remove(title_scheme).add(title_encrypt, background_scheme.set_fill(opacity = 0))
        self.play(alpha.animate.set_value(1.0), Rotate(arrow, PI, about_point = ORIGIN), Rotate(arrow_title, PI, about_point = 2.8*UP), Rotate(arrow_upper, PI, about_point = ORIGIN), Rotate(arrow_lower, PI, about_point = ORIGIN), Transform(title_encrypt, title_attack), background_scheme.animate.set_fill(opacity = 0.5))
        for mob in [arrow, arrow_upper, arrow_lower, arrow_title]:
            mob.clear_updaters()
        self.remove(arrow).waiting(2, 20) #那么这套加密方案就有可能被破解
        
        self.play(FadeIn(title_scheme, rate_func = squish_rate_func(smooth, 0.5, 1)), FadeOut(title_encrypt, rate_func = squish_rate_func(smooth, 0, 0.5)), *[FadeOut(mob) for mob in [arrow_title, background_scheme]], *[FadeOut(mob, 0.5*DOWN) for mob in [message_bunny, mob_texts_bunny, background_bunny, message_wheel, mob_texts_wheel, background_wheel, not_equal, arrow_upper, arrow_lower]])
        self.waiting(0, 17) #正确的思路是

        COLOR_S = rate_color(11/26)
        COLOR_B = rate_color(20/26)
        message_bunny = MTexText("bunny", color = COLOR_B).shift(UP + 4.5*LEFT)
        message_sleep = MTexText("sleep", color = COLOR_S).shift(DOWN + 4.5*LEFT)
        mob_texts_hatte, part_texts_hatte = align_all("hatte", buff = 1.7)
        mob_texts_hatte.scale(0.6, about_point = 2.5*RIGHT).shift(2.2*RIGHT)
        for i in range(26):
            part_texts_hatte[i].set_color(rate_color(i/26))
        arrow.set_opacity(1).rotate(PI, about_point = ORIGIN)
        arrow_title.set_color(BLUE).rotate(PI, about_point = 2.8*UP)
        background_scheme.set_opacity(1)

        self.play(Write(message_bunny), Write(message_sleep))
        self.bring_to_back(arrow, arrow_title, background_scheme).play(ShowCreation(arrow), ShowCreation(arrow_title))
        self.play(FadeIn(mob_texts_hatte, 0.5*RIGHT))
        self.waiting(0, 13) #让不同的明文生成找不到任何区别的密文
        self.waiting(0, 17) #（空闲）

        self.play(ReplacementTransform(notice3, notice4))
        self.waiting(1, 6) #把找规律变成找不同
        self.waiting(4, 17) #就是现代密码学 相比于古典密码学 最大的区别
        self.waiting(0, 23) #（空闲）

        self.play(ReplacementTransform(notice4, notice5))
        self.waiting(0, 18) #基于这种思路
        self.waiting(2, 12) #我们可以从恺撒密码出发
        self.waiting(4, 8) #设计出一套绝对安全 完全无法破解的加密方案
        self.waiting(0, 16) #（空闲）

        self.remove(title_scheme, outer_layer, inner_layer, *blocks, *numbers, title_message, title_cypher, shade_title, arrow_title, message_bunny, message_sleep, mob_texts_hatte, arrow, background_scheme)
        
        text_message = "perfect secrecy"
        text_letter = "perfectsecrecy"
        cypher_letter = ""
        shifting = []
        example = Text(text_message, font = "Times New Roman").scale(0.8).shift(1.5*UP)
        example_letter = Text(text_message, font = "Times New Roman").scale(0.8).shift(1.5*UP)
        for i in range(14):
            example_letter[i].set_x(0.9*(i-6.5))
            shift = random.randint(0, 25)
            shifting.append(shift)
            cypher, _ = caeser(text_letter[i], shift)
            cypher_letter += cypher
        example_cypher = Text(cypher_letter, font = "Times New Roman", color = YELLOW_E).scale(0.8).shift(1.5*DOWN)
        arrows = VGroup()
        keys = VGroup()
        for i in range(14):
            example_cypher[i].set_x(0.9*(i-6.5))
            arrow = Arrow(1*UP, 1*DOWN, buff = 0).shift(0.9*(i-6.5)*RIGHT)
            key = MTex("+" + str(shifting[i])).scale(0.5).shift((0.9*(i-6.5))*RIGHT)
            arrows.add(arrow)
            keys.add(key)
        arrows.set_color(BLUE)
        keys.set_color(BLUE)
            
        self.play(Write(example))
        self.waiting(0, 12) #对于一段文本
        self.play(FadeIn(keys, 0.5*DOWN), lag_ratio = 0.05, run_time = 2)
        self.play(Transform(example, example_letter))
        self.waiting(0, 20) #我们首先随机一串从0到25的偏移量
        self.play(FadeIn(arrows, 0.5*DOWN), keys.animate.shift(0.3*RIGHT), lag_ratio = 0.05, run_time = 2)
        self.play(ShowIncreasingSubsets(example_cypher), run_time = 2, rate_func = linear)
        self.waiting(0, 7) #然后让每一个字母独立地通过恺撒密码来加密
        self.waiting(0, 29) #这样
        self.play(ApplyWave(example))
        self.waiting(0, 16) #一段文本就可以变成......
        self.play(ApplyWave(example_cypher))
        self.waiting(2, 1) #......任何一段和它长度相同的字符串

        def get_key(message, cypher):
            return (ord(cypher) - ord(message))%26

        text_all_1 = "congratulation"
        message_all_1 = Text(text_all_1, font = "Times New Roman").scale(0.8).shift(1.5*UP)
        for i in range(14):
            message_all_1[i].set_x(0.9*(i-6.5))
        key_all_1 = VGroup(*[MTex("+" + str(get_key(text_all_1[i], cypher_letter[i])), color = BLUE).scale(0.5).shift((0.9*(i-6.5) + 0.3)*RIGHT) for i in range(14)])
        self.play(FadeOut(example), FadeOut(keys), run_time = 0.5)
        self.play(FadeIn(message_all_1), FadeIn(key_all_1), run_time = 0.5)
        self.waiting(1, 0)
        
        text_all_2 = "manimcommunity"
        message_all_2 = Text(text_all_2, font = "Times New Roman").scale(0.8).shift(1.5*UP)
        for i in range(14):
            message_all_2[i].set_x(0.9*(i-6.5))
        key_all_2 = VGroup(*[MTex("+" + str(get_key(text_all_2[i], cypher_letter[i])), color = BLUE).scale(0.5).shift((0.9*(i-6.5) + 0.3)*RIGHT) for i in range(14)])
        self.play(FadeOut(message_all_1), FadeOut(key_all_1), run_time = 0.5)
        self.play(FadeIn(message_all_2), FadeIn(key_all_2), run_time = 0.5)
        self.waiting(1, 0)

        surrounding = SurroundingRectangle(example_cypher).insert_n_curves(64)
        anim = ShowCreationThenDestruction(surrounding)
        mobject = anim.mobject
        self.add(mobject)
        anim.begin()
        beta = ValueTracker(0.0)
        def alter_updater(m):
            alpha = beta.get_value()
            if alpha >= 1:
                anim.finish()
                m.remove_updater(alter_updater)
                self.remove(m)
            anim.interpolate(alpha)
        mobject.add_updater(alter_updater)

        text_all_3 = "hypermeanshigh"
        message_all_3 = Text(text_all_3, font = "Times New Roman").scale(0.8).shift(1.5*UP)
        for i in range(14):
            message_all_3[i].set_x(0.9*(i-6.5))
        key_all_3 = VGroup(*[MTex("+" + str(get_key(text_all_3[i], cypher_letter[i])), color = BLUE).scale(0.5).shift((0.9*(i-6.5) + 0.3)*RIGHT) for i in range(14)])
        self.play(FadeOut(message_all_2), FadeOut(key_all_2), run_time = 0.5)
        self.play(FadeIn(message_all_3), FadeIn(key_all_3), ApplyMethod(beta.set_value, 13/60, rate_func = squish_rate_func(smooth, 2/15, 1)), run_time = 0.5)
        self.play(ApplyMethod(beta.set_value, 43/60))

        text_all_4 = "gankuaisanlian"
        message_all_4 = Text(text_all_4, font = "Times New Roman").scale(0.8).shift(1.5*UP)
        for i in range(14):
            message_all_4[i].set_x(0.9*(i-6.5))
        key_all_4 = VGroup(*[MTex("+" + str(get_key(text_all_4[i], cypher_letter[i])), color = BLUE).scale(0.5).shift((0.9*(i-6.5) + 0.3)*RIGHT) for i in range(14)])
        self.play(FadeOut(message_all_3), FadeOut(key_all_3), ApplyMethod(beta.set_value, 58/60), run_time = 0.5)
        self.play(FadeIn(message_all_4), FadeIn(key_all_4), ApplyMethod(beta.set_value, 1, rate_func = squish_rate_func(smooth, 0, 2/15)), run_time = 0.5)
        self.waiting(1, 0)
        
        self.play(FadeOut(message_all_4), FadeOut(key_all_4), run_time = 0.5)
        self.play(FadeIn(example), FadeIn(keys), run_time = 0.5)
        self.waiting(2+2+4+0-9, 17+0+10+18) #所有文本都能得到同样的密文 在不知道密钥的情况下 只拿着一段密文 是绝对没办法反向推理出明文的 （空闲）

        title = Text("单次密码簿", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP, 3*UP)
        shade = SurroundingRectangle(title, stroke_width = 0, fill_opacity = 1, fill_color = "#333333").next_to(title, DOWN, buff = 0.1)
        title.next_to(shade.get_corner(UP), DOWN, buff = 0)
        self.add(title, shade).play(title.animate.next_to(3*UP, UP), title_line.animate.put_start_and_end_on(3*UP+6*LEFT, 3*UP+6*RIGHT))
        self.remove(shade)
        self.waiting(1, 28) #这套加密方案被称作“单次密码簿”方案
        self.waiting(1, 10) #到此共123秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_2(Scene):
    def construct(self):

        notice5 = Notice("前情提要", "请　复习")
        notice6 = Notice("经典缺陷", "请勿应用")
        notice7 = Notice("下节内容", "请往后看")
        notice8 = Notice("重要问题", "请　思考")

        text_message = "perfect secrecy"
        text_letter = "perfectsecrecy"
        cypher_letter = ""
        shifting = []
        example = Text(text_message, font = "Times New Roman").scale(0.8).shift(1.5*UP)
        for i in range(14):
            example[i].set_x(0.9*(i-6.5))
            shift = random.randint(0, 25)
            shifting.append(shift)
            cypher, _ = caeser(text_letter[i], shift)
            cypher_letter += cypher
        example_cypher = Text(cypher_letter, font = "Times New Roman", color = YELLOW_E).scale(0.8).shift(1.5*DOWN)
        arrows = VGroup()
        keys = VGroup()
        for i in range(14):
            example_cypher[i].set_x(0.9*(i-6.5))
            arrow = Arrow(1*UP, 1*DOWN, buff = 0).shift(0.9*(i-6.5)*RIGHT)
            key = MTex("+" + str(shifting[i])).scale(0.5).shift((0.9*(i-6.5) + 0.3)*RIGHT)
            arrows.add(arrow)
            keys.add(key)
        arrows.set_color(BLUE)
        keys.set_color(BLUE)
        title = Text("单次密码簿", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)

        self.add(notice5, example, example_cypher, arrows, keys, title, title_line)
        self.waiting(2, 2) #这套方案安全归安全
        self.play(ReplacementTransform(notice5, notice6))
        self.waiting(0, 29) #但也有一定的问题

        self.waiting(1, 4) #比如说......
        self.play(ApplyWave(keys))
        self.waiting(1, 9) #......它需要的密钥太长了

        center = VMobject(stroke_color = YELLOW)
        center.set_points([0.15*LEFT, ORIGIN, 0.15*RIGHT, 0.15*UP, ORIGIN, 0.15*DOWN])
        corner = VMobject(stroke_color = YELLOW)
        corner.set_points_as_corners([0.2*DOWN, 0.2*DOWN+0.2*LEFT, 0.2*LEFT])
        corners = [corner.copy().rotate(i*PI/2, about_point=ORIGIN) for i in range(4)]
        initial = VGroup(center, *corners)
        aim = initial.copy().shift(1.5*UP).set_opacity(0)
        opened_aim = VGroup(center.copy(), corners[0].copy().shift(6.1*LEFT + 0.1*DOWN), corners[1].copy().shift(6.1*RIGHT + 0.1*DOWN), corners[2].copy().shift(6.1*RIGHT + 0.1*UP), corners[3].copy().shift(6.1*LEFT + 0.1*UP))
        to_message = opened_aim.copy().shift(1.5*UP)
        to_keys = opened_aim.copy().shift(0.3*RIGHT)
        initial.shift(1.5*UP)
        
        self.play(LaggedStart(*[ApplyMethod(example[i].set_color, [WHITE, GREY_B, GREY_E][i%3]) for i in range(14)]), run_time = 1.5)
        self.waiting(0, 11) #想要发送多长的消息
        self.play(LaggedStart(*[ApplyMethod(keys[i].set_color, [BLUE_A, BLUE, BLUE_E][i%3]) for i in range(14)]), run_time = 1.5)
        self.waiting(0.5, 6) #就要准备多长的密钥
        self.add(aim).play(Transform(aim, to_message))
        self.waiting(0, 19) #在发送消息之前
        self.play(Transform(aim, to_keys))
        self.waiting(0, 23) #需要先把密钥发出去
        self.waiting(0, 16) #（空闲）

        self.waiting(2, 22) #可是如果能安全地把密钥发出去
        self.play(Transform(aim, to_message))
        self.waiting(1, 12) #那为什么不直接把信息发过去呢
        self.waiting(0, 19) #（空闲）

        self.play(Transform(aim, initial))
        alpha = ValueTracker(0.0)
        def rotating_updater(mob: VMobject):
            ratio = alpha.get_value()
            rotate_factor = smooth(ratio)
            scale_factor = breath(1 - ratio)
            mob.become(initial).scale(scale_factor).rotate(rotate_factor * TAU)
        aim.add_updater(rotating_updater)
        self.play(alpha.animate.set_value(1.0), rate_func = linear)
        aim.clear_updaters()
        self.remove(alpha, aim)
        self.waiting(1+1-2, 17+26) #如果偶尔用一下 还可以在发消息之前
        self.waiting(2, 5) #先碰面交换密码
        self.waiting(2, 24) #但这根本不适用于大规模通讯的场合
        self.waiting(0, 23) #（空闲）

        self.remove(example, example_cypher, arrows, keys)
        
        all_scheme = Ellipse(height = 5, width = 12, stroke_width = 0, fill_color = GREY_C, fill_opacity = 1)
        simple_scheme = Circle(radius = 2, stroke_width = 0, fill_color = GREEN_E, fill_opacity = 1).shift(2.5*LEFT)
        secure_scheme = Circle(radius = 2, stroke_width = 0, fill_color = BLUE_E, fill_opacity = 1).shift(2.5*RIGHT)
        text_all = Text("加密方案", font = "simsun").shift(2*UP)
        text_simple = Text("能传递密钥的", font = "simsun", color = GREEN_A).scale(0.8).shift(1*UP + 2.5*LEFT)
        text_secure = Text("能完美加密的", font = "simsun", color = BLUE_A).scale(0.8).shift(1*UP + 2.5*RIGHT)
        text_ceaser = Text("恺撒加密法", font = "simhei", color = YELLOW_E).scale(0.6).shift(2.5*LEFT)
        text_one_time_pad = Text("单次密码簿", font = "simhei", color = YELLOW_E).scale(0.6).shift(2.5*RIGHT)
        arrow_left = Arrow(1.9*DOWN+0.8*LEFT, 1.2*DOWN+1.5*LEFT, buff = 0)
        arrow_right = Arrow(1.9*DOWN+0.8*RIGHT, 1.2*DOWN+1.5*RIGHT, buff = 0)
        text_disjoint = Text("交集为空", font = "simsun").scale(0.6).shift(2*DOWN).add(arrow_left, arrow_right)
        self.play(ShowCreation(all_scheme))
        self.play(Write(text_all), ShowCreation(simple_scheme), ShowCreation(secure_scheme))
        self.play(Write(text_simple), Write(text_secure))
        self.play(FadeIn(text_ceaser, scale = 0.6), FadeIn(text_one_time_pad, scale = 0.6))
        self.play(FadeIn(text_disjoint, 0.5*UP))
        self.waiting(2+2+2-5, 17+6+4) #这就造成了一个很尴尬的局面 能用的加密方案不安全 而安全的加密方案不能用
        self.waiting(0, 21) #（空闲）
        self.waiting(2, 11) #这个两难问题有什么解决方案吗
        self.waiting(0, 19) #（空闲）

        public_shceme = Text("公钥加密", font = "simhei", color = YELLOW_E).scale(0.6)
        background = Ellipse(height = 1, width = 2, stroke_width = 0, fill_color = TEAL_E, fill_opacity = 1)
        self.play(ShowCreation(background), ReplacementTransform(notice6, notice7))
        self.play(Write(public_shceme))
        self.waiting(0, 23) #有的观众可能会想到公钥加密
        self.waiting(2, 4) #但其实只要是公钥加密
        self.play(public_shceme.animate.shift(DOWN + 2.5*LEFT), FadeOut(background))
        self.waiting(1, 3) #就不可能做到完美加密
        self.waiting(2, 10) #理论上还是可以破解的
        self.waiting(2, 8) #只不过破解需要的时间太长
        self.waiting(1, 4) #太不划算了
        self.waiting(0, 22) #（空闲）

        self.play(FadeOut(public_shceme), ReplacementTransform(notice7, notice8))
        self.waiting(1, 20) #那么 除了公钥加密之外
        self.waiting(3, 3) #还有别的可以简化单次密码簿的方法吗
        self.waiting(0, 23) #到此共61秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_3(Scene):
    def construct(self):

        notice8 = Notice("重要问题", "请　思考")
        notice9 = Notice("常用性质", "请记笔记")
        notice10 = Notice("一一映射", "请　取逆")
        notice11 = Notice("常见误区", "请勿模仿")
        notice12 = Notice("重要思路", "请　借鉴")
        notice13 = Notice("通辽史料", "请　催更")
        notice14 = Notice("重要思路", "请　借鉴")

        title = Text("单次密码簿", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        all_scheme = Ellipse(height = 5, width = 12, stroke_width = 0, fill_color = GREY_C, fill_opacity = 1)
        simple_scheme = Circle(radius = 2, stroke_width = 0, fill_color = GREEN_E, fill_opacity = 1).shift(2.5*LEFT)
        secure_scheme = Circle(radius = 2, stroke_width = 0, fill_color = BLUE_E, fill_opacity = 1).shift(2.5*RIGHT)
        text_all = Text("加密方案", font = "simsun").shift(2*UP)
        text_simple = Text("能传递密钥的", font = "simsun", color = GREEN_A).scale(0.8).shift(1*UP + 2.5*LEFT)
        text_secure = Text("能完美加密的", font = "simsun", color = BLUE_A).scale(0.8).shift(1*UP + 2.5*RIGHT)
        text_ceaser = Text("恺撒加密法", font = "simhei", color = YELLOW_E).scale(0.6).shift(2.5*LEFT)
        text_one_time_pad = Text("单次密码簿", font = "simhei", color = YELLOW_E).scale(0.6).shift(2.5*RIGHT)
        arrow_left = Arrow(1.9*DOWN+0.8*LEFT, 1.2*DOWN+1.5*LEFT, buff = 0)
        arrow_right = Arrow(1.9*DOWN+0.8*RIGHT, 1.2*DOWN+1.5*RIGHT, buff = 0)
        text_disjoint = Text("交集为空", font = "simsun").scale(0.6).shift(2*DOWN).add(arrow_left, arrow_right)

        title_scheme = Text("加密方案", font = "simsun", color = BLUE).shift(2.8*UP)
        title_message = Text("明文", font = "simsun", color = WHITE).shift(2.8*UP + 4*LEFT)
        title_cypher = Text("密文", font = "simsun", color = YELLOW_E).shift(2.8*UP + 4*RIGHT)
        blocks = []
        block_per_layer = [2, 3, 4, 4, 4, 4, 3, 2]
        order = 0
        for i in range(8):
            number = block_per_layer[i]
            for j in range(number):
                position = 0.6*UP*(i-3.5) + 1.2*RIGHT*(j-(number-1)/2)
                number_i = MTex(str(order), color = BLUE_D).scale(0.9)
                block_i = Block(order).add(number_i).shift(position)
                blocks.append(block_i)
                order += 1
        
        mob_letters = MTexText("abcdefghijklmnopqrstuvwxyz").scale(0.9)
        for i in range(26):
            row = i // 4
            col = i % 4
            mob_letters[i].set_x(0).shift(0.6*DOWN*(row-3) + 0.6*RIGHT*(col-1.5))
        mob_message = mob_letters.copy().shift(4*LEFT)
        part_message = mob_message.submobjects
        mob_cypher = mob_letters.copy().set_color(YELLOW_E).shift(4*RIGHT)
        part_cypher = mob_cypher.submobjects

        removings = [title, title_line, all_scheme, simple_scheme, secure_scheme, text_all, text_simple, text_secure, text_ceaser, text_one_time_pad, text_disjoint]
        addings = [title_scheme, title_message, title_cypher, *blocks, *part_message, *part_cypher]
        self.add(notice8, *removings).bring_to_back(*addings)
        removings = removings[::-1]
        number = len(removings)
        anim_fadings = [FadeOut(removings[i], 0.5*DOWN, squish_interval = (i/(number+4), (i+5)/(number+4)), run_time = 1.5) for i in range(number)]
        number = len(addings)
        random.shuffle(addings)
        anim_addings = [FadeIn(addings[i], 0.5*UP, squish_interval = (i/(number+15), (i+16)/(number+15)), run_time = 3) for i in range(number)]
        self.play(*anim_fadings, *anim_addings)
        self.waiting(0, 8) #乍一听 似乎找不到什么简化的方法
        self.waiting(0, 19) #（空闲）

        self.play(ReplacementTransform(notice8, notice9))
        self.waiting(0, 16) #一套加密系统

        shade = Rectangle(height = 8, width = 5, fill_opacity = 0.7, stroke_width = 0, fill_color = "#333333")
        arrow = CurvedArrow(title_cypher.get_corner(UL)+0.1*UL, title_message.get_corner(UR+0.5*UR), angle = PI/6, stroke_width = 10, color = GREEN)
        title_attack = Text("强行解密", font = "simsun", color = GREEN).shift(3.5*UP)
        shade_attack = BackgroundRectangle(title_attack, fill_color = "#333333", fill_opacity = 1)
        cross = VMobject(color = RED).set_points([0.5*UR, ORIGIN, 0.5*DL, 0.5*UL, ORIGIN, 0.5*DR]).shift(3.5*UP)
        self.play(FadeIn(shade))
        self.add(arrow, shade_attack).play(ShowCreation(arrow), Write(title_attack))
        self.play(ShowCreation(cross))
        self.waiting(2+2-3, 12+12) #虽然在拿不到密钥的时候 应该做到完全无法破译

        chosen_blocks = [block.copy() for block in blocks]
        chosen_block = chosen_blocks[18]
        copy_scheme = title_scheme.copy()
        chosen = SurroundingRectangle(chosen_block, buff = 0)
        self.play(*[FadeOut(mob) for mob in [cross, title_attack, arrow]], FadeIn(chosen_block), ShowCreation(chosen), ReplacementTransform(notice9, notice10))
        self.remove(shade_attack)
        self.waiting(0, 23) #但在拿到密钥以后

        def message_get_need(message: VMobject, algorithm: VMobject, line_color, reversed: bool = False):
            link = HorizontalLink(message.get_center() + 0.2*RIGHT, algorithm.get_center(), color = line_color)
            shade = link.copy().set_stroke(width = 10, color = "#333333")
            if reversed:
                link.reverse_points()
                shade.reverse_points()
                show_func = rush_from
                tear_func = inverse_rush_from
            else:
                show_func = rush_into
                tear_func = inverse_rush_into
            anim_1 = ShowCreation(shade, rate_func = show_func, run_time = 0.5)
            anim_2 = ShowCreation(link, rate_func = show_func, run_time = 0.5)
            anim_3 = ApplyMethod(message.set_opacity, 1, run_time = 0.5)
            anim_4 = Uncreate(shade, rate_func = tear_func, run_time = 0.5)
            anim_5 = Uncreate(link, rate_func = tear_func, run_time = 0.5)
            anim_6 = ApplyMethod(message.fade, run_time = 0.5)
            return [shade, link], [anim_1, anim_2], anim_3, [anim_4, anim_5], anim_6

        def cypher_get_need(cypher: VMobject, algorithm: VMobject, line_color, reversed: bool = False):
            link = HorizontalLink(algorithm.get_center(), cypher.get_center() + 0.2*LEFT, color = line_color)
            shade = link.copy().set_stroke(width = 10, color = "#333333")
            if reversed:
                link.reverse_points()
                shade.reverse_points()
                show_func = rush_into
                tear_func = inverse_rush_into
            else:
                show_func = rush_from
                tear_func = inverse_rush_from
            anim_1 = ShowCreation(shade, rate_func = show_func, run_time = 0.5)
            anim_2 = ShowCreation(link, rate_func = show_func, run_time = 0.5)
            anim_3 = ApplyMethod(cypher.set_opacity, 1, run_time = 0.5)
            anim_4 = Uncreate(shade, rate_func = tear_func, run_time = 0.5)
            anim_5 = Uncreate(link, rate_func = tear_func, run_time = 0.5)
            anim_6 = ApplyMethod(cypher.fade, run_time = 0.5)
            return [shade, link], [anim_1, anim_2], anim_3, [anim_4, anim_5], anim_6

        def get_color(index: int):
            colors = [MAROON_A, RED_A, ORANGE_A, YELLOW_A, GREEN_A, TEAL_A, BLUE_A, PURPLE_A, ]
            length = len(colors)
            return colors[index % length]

        links_1_1, anims_1_1, _, tearing_1_1, fading_1_1 = cypher_get_need(part_cypher[18], chosen_block, get_color(1), True)
        links_1_2, anims_1_2, _, tearing_1_2, fading_1_2 = message_get_need(part_message[0], chosen_block, get_color(1), True)
        self.add(*links_1_1, chosen_block, chosen).play(*anims_1_1, *[mob.animate.fade() for mob in [*part_cypher[0:18], *part_cypher[19:26], *part_message[1:26]]], run_time = 0.5)
        self.add(*links_1_2, chosen_block, chosen).play(*anims_1_2)
        self.waiting(0, 15)

        for mob in [*links_1_1, *links_1_2]:
            mob.reverse_points()
        links_2_1, anims_2_1, lightening_2_1, tearing_2_1, fading_2_1 = cypher_get_need(part_cypher[8], chosen_block, get_color(2), True)
        links_2_2, anims_2_2, lightening_2_2, tearing_2_2, fading_2_2 = message_get_need(part_message[16], chosen_block, get_color(2), True)
        self.add(*links_2_1, chosen_block, chosen).play(*tearing_1_1, *anims_2_1, lightening_2_1, lightening_2_2)
        self.add(*links_2_2, chosen_block, chosen).play(*tearing_1_2, *anims_2_2, fading_1_1, fading_1_2)
        self.waiting(0, 15)

        for mob in [*links_2_1, *links_2_2]:
            mob.reverse_points()
        links_3_1, anims_3_1, lightening_3_1, tearing_3_1, fading_3_1 = message_get_need(part_message[12], chosen_block, get_color(3))
        links_3_2, anims_3_2, lightening_3_2, tearing_3_2, fading_3_2 = cypher_get_need(part_cypher[4], chosen_block, get_color(3))
        self.add(*links_3_1, chosen_block, chosen).play(*tearing_2_1, *anims_3_1, lightening_3_1, lightening_3_2)
        self.add(*links_3_2, chosen_block, chosen).play(*tearing_2_2, *anims_3_2, fading_2_1, fading_2_2)
        self.waiting(0, 15)

        for mob in [*links_3_1, *links_3_2]:
            mob.reverse_points()
        links_4_1, anims_4_1, lightening_4_1, tearing_4_1, fading_4_1 = message_get_need(part_message[7], chosen_block, get_color(4))
        links_4_2, anims_4_2, lightening_4_2, tearing_4_2, fading_4_2 = cypher_get_need(part_cypher[25], chosen_block, get_color(4))
        self.add(*links_4_1, chosen_block, chosen).play(*tearing_3_1, *anims_4_1, lightening_4_1, lightening_4_2)
        self.add(*links_4_2, chosen_block, chosen).play(*tearing_3_2, *anims_4_2, fading_3_1, fading_3_2)
        self.waiting(0, 15)

        for mob in [*links_4_1, *links_4_2]:
            mob.reverse_points()
        links_5_1, anims_5_1, lightening_5_1, tearing_5_1, fading_5_1 = message_get_need(part_message[19], chosen_block, get_color(5))
        links_5_2, anims_5_2, lightening_5_2, tearing_5_2, fading_5_2 = cypher_get_need(part_cypher[11], chosen_block, get_color(5))
        self.add(*links_5_1, chosen_block, chosen).play(*tearing_4_1, *anims_5_1, lightening_5_1, lightening_5_2)
        self.add(*links_5_2, chosen_block, chosen).play(*tearing_4_2, *anims_5_2, fading_4_1, fading_4_2)
        self.waiting(0, 15)

        for mob in [*links_5_1, *links_5_2]:
            mob.reverse_points()
        links_6_1, anims_6_1, lightening_6_1, tearing_6_1, fading_6_1 = message_get_need(part_message[15], chosen_block, get_color(6))
        links_6_2, anims_6_2, lightening_6_2, tearing_6_2, fading_6_2 = cypher_get_need(part_cypher[7], chosen_block, get_color(6))
        self.add(*links_6_1, chosen_block, chosen).play(*tearing_5_1, *anims_6_1, lightening_6_1, lightening_6_2)
        self.add(*links_6_2, chosen_block, chosen).play(*tearing_5_2, *anims_6_2, fading_5_1, fading_5_2)
        self.waiting(0, 15)

        count_messages = MTex("m").shift(4*LEFT + 3.4*UP)
        count_cyphers = MTex("c", color = YELLOW_E).shift(4*RIGHT + 3.4*UP)
        more_cyphers = MTex("m\le c", tex_to_color_map = {"c": YELLOW_E}).shift(2.2*LEFT + 3.4*UP)
        write_1 = Write(count_messages)
        write_2 = Write(count_cyphers)
        write_3 = Write(more_cyphers)
        count_keys = MTex("k", color = BLUE).shift(3.4*UP)
        more_keys = MTex("k\ge c", tex_to_color_map = {"k": BLUE, "c": YELLOW_E}).shift(2.2*RIGHT + 3.4*UP)
        write_4 = Write(count_keys)
        write_5 = Write(more_keys)
        for mob in [*links_6_1, *links_6_2]:
            mob.reverse_points()
        links_7_1, anims_7_1, lightening_7_1, tearing_7_1, fading_7_1 = message_get_need(part_message[4], chosen_block, get_color(7))
        links_7_2, anims_7_2, lightening_7_2, tearing_7_2, fading_7_2 = cypher_get_need(part_cypher[22], chosen_block, get_color(7))
        self.add(*links_7_1, chosen_block, chosen).play(*tearing_6_1, *anims_7_1, lightening_7_1, lightening_7_2)
        self.add(*links_7_2, chosen_block, chosen).play(*tearing_6_2, *anims_7_2, fading_6_1, fading_6_2, write_1, write_2)

        for mob in [*links_7_1, *links_7_2]:
            mob.reverse_points()
        links_8_1, anims_8_1, lightening_8_1, tearing_8_1, fading_8_1 = message_get_need(part_message[21], chosen_block, get_color(8))
        links_8_2, anims_8_2, lightening_8_2, tearing_8_2, fading_8_2 = cypher_get_need(part_cypher[13], chosen_block, get_color(8))
        self.add(*links_8_1, chosen_block, chosen).play(*tearing_7_1, *anims_8_1, lightening_8_1, lightening_8_2)
        self.add(*links_8_2, chosen_block, chosen).play(*tearing_7_2, *anims_8_2, fading_7_1, fading_7_2)
        self.waiting(0, 15)

        for mob in [*links_8_1, *links_8_2]:
            mob.reverse_points()
        links_9_1, anims_9_1, lightening_9_1, tearing_9_1, fading_9_1 = message_get_need(part_message[14], chosen_block, get_color(9))
        links_9_2, anims_9_2, lightening_9_2, tearing_9_2, fading_9_2 = cypher_get_need(part_cypher[6], chosen_block, get_color(9))
        self.add(*links_9_1, chosen_block, chosen).play(*tearing_8_1, *anims_9_1, lightening_9_1, lightening_9_2)
        self.add(*links_9_2, chosen_block, chosen).play(*tearing_8_2, *anims_9_2, fading_8_1, fading_8_2, write_3)

        for mob in [*links_9_1, *links_9_2]:
            mob.reverse_points()
        links_10_1, anims_10_1, lightening_10_1, tearing_10_1, fading_10_1 = message_get_need(part_message[2], chosen_block, get_color(10))
        links_10_2, anims_10_2, lightening_10_2, tearing_10_2, fading_10_2 = cypher_get_need(part_cypher[20], chosen_block, get_color(10))
        self.add(*links_10_1, chosen_block, chosen).play(*tearing_9_1, *anims_10_1, lightening_10_1, lightening_10_2)
        self.add(*links_10_2, chosen_block, chosen).play(*tearing_9_2, *anims_10_2, fading_9_1, fading_9_2)
        self.waiting(0, 15)

        for mob in [*links_10_1, *links_10_2]:
            mob.reverse_points()
        links_11_1, anims_11_1, lightening_11_1, _, _ = message_get_need(part_message[25], chosen_block, get_color(11))
        links_11_2, anims_11_2, lightening_11_2, _, fading_11_2 = cypher_get_need(part_cypher[17], chosen_block, get_color(11))
        self.add(*links_11_1, chosen_block, chosen).play(*tearing_10_1, *anims_11_1, lightening_11_1, lightening_11_2)
        self.add(*links_11_2, chosen_block, chosen).play(*tearing_10_2, *anims_11_2, fading_10_1, fading_10_2)
        self.waiting(0, 15)

        for mob in [*links_11_1, *links_11_2]:
            mob.reverse_points()
        links_12_1, anims_12_1, lightening_12_1, _, fading_12_1 = message_get_need(part_message[3], chosen_blocks[14], get_color(12))
        links_12_2, anims_12_2, lightening_12_2, _, _ = cypher_get_need(part_cypher[17], chosen_blocks[14], get_color(12))
        self.play(FadeIn(chosen_blocks[14]), FadeIn(copy_scheme))
        self.add(*links_12_1, chosen_block, chosen_blocks[14], chosen).play(*anims_12_1, lightening_12_1, lightening_12_2)
        self.add(*links_12_2, chosen_block, chosen_blocks[14], chosen).play(*anims_12_2)
        self.waiting(0, 15)

        links_13_1, anims_13_1, lightening_13_1, _, fading_13_1 = message_get_need(part_message[11], chosen_blocks[6], get_color(13))
        links_13_2, anims_13_2, lightening_13_2, _, _ = cypher_get_need(part_cypher[17], chosen_blocks[6], get_color(13))
        self.play(FadeIn(chosen_blocks[6]), *[FadeOut(mob) for mob in [*links_12_1, *links_12_2, chosen_blocks[14]]], fading_12_1)
        self.add(*links_13_1, chosen_block, chosen_blocks[6], chosen).play(*anims_13_1, lightening_13_1, lightening_13_2)
        self.add(*links_13_2, chosen_block, chosen_blocks[6], chosen).play(*anims_13_2)
        self.waiting(0, 15)

        links_14_1, anims_14_1, lightening_14_1, _, fading_14_1 = message_get_need(part_message[18], chosen_blocks[25], get_color(14))
        links_14_2, anims_14_2, lightening_14_2, _, _ = cypher_get_need(part_cypher[17], chosen_blocks[25], get_color(14))
        self.play(FadeIn(chosen_blocks[25]), *[FadeOut(mob) for mob in [*links_13_1, *links_13_2, chosen_blocks[6]]], fading_13_1)
        self.add(*links_14_1, chosen_block, chosen_blocks[25], chosen).play(*anims_14_1, lightening_14_1, lightening_14_2)
        self.add(*links_14_2, chosen_block, chosen_blocks[25], chosen).play(*anims_14_2)
        self.waiting(0, 15)

        links_15_1, anims_15_1, lightening_15_1, _, fading_15_1 = message_get_need(part_message[13], chosen_blocks[4], get_color(15))
        links_15_2, anims_15_2, lightening_15_2, _, _ = cypher_get_need(part_cypher[17], chosen_blocks[4], get_color(15))
        self.play(FadeIn(chosen_blocks[4]), *[FadeOut(mob) for mob in [*links_14_1, *links_14_2, chosen_blocks[25]]], fading_14_1)
        self.add(*links_15_1, chosen_block, chosen_blocks[4], chosen).play(*anims_15_1, lightening_15_1, lightening_15_2)
        self.add(*links_15_2, chosen_block, chosen_blocks[4], chosen).play(*anims_15_2)
        self.waiting(0, 15)

        indicate = SurroundingRectangle(part_message[25])
        links_16_1, anims_16_1, lightening_16_1, _, fading_16_1 = message_get_need(part_message[5], chosen_blocks[18], get_color(16))
        links_16_2, anims_16_2, lightening_16_2, _, fading_16_2 = cypher_get_need(part_cypher[23], chosen_blocks[18], get_color(16))
        self.play(*[FadeOut(mob) for mob in [*links_15_1, *links_15_2, chosen_blocks[4], *links_11_1, *links_11_2]], fading_11_2, ShowCreation(indicate))
        self.add(*links_16_1, chosen_block, chosen).play(*anims_16_1, lightening_16_1, lightening_16_2)
        self.add(*links_16_2, chosen_block, chosen).play(*anims_16_2, fading_15_1)
        links_17_1, anims_17_1, lightening_17_1, _, _ = message_get_need(part_message[25], chosen_blocks[24], get_color(17))
        links_17_2, anims_17_2, lightening_17_2, _, _ = cypher_get_need(part_cypher[23], chosen_blocks[24], get_color(17))
        self.play(FadeIn(chosen_blocks[24]))
        self.add(*links_17_1, chosen_block, chosen_blocks[24], chosen).play(*anims_17_1, lightening_17_1, lightening_17_2)
        self.add(*links_17_2, chosen_block, chosen_blocks[24], chosen).play(*anims_17_2)
        self.waiting(0, 15)

        links_18_1, anims_18_1, lightening_18_1, tearing_18_1, fading_18_1 = message_get_need(part_message[10], chosen_blocks[18], get_color(18))
        links_18_2, anims_18_2, lightening_18_2, tearing_18_2, fading_18_2 = cypher_get_need(part_cypher[2], chosen_blocks[18], get_color(18))
        self.play(*[FadeOut(mob) for mob in [*links_16_1, *links_16_2, *links_17_1, *links_17_2, chosen_blocks[24]]], fading_16_1, fading_16_2, write_4)
        self.add(*links_18_1, chosen_block, chosen).play(*anims_18_1, lightening_18_1, lightening_18_2)
        self.add(*links_18_2, chosen_block, chosen).play(*anims_18_2)
        links_19_1, anims_19_1, lightening_19_1, _, _ = message_get_need(part_message[25], chosen_blocks[3], get_color(19))
        links_19_2, anims_19_2, lightening_19_2, _, _ = cypher_get_need(part_cypher[2], chosen_blocks[3], get_color(19))
        self.play(FadeIn(chosen_blocks[3]), write_5)
        self.add(*links_19_1, chosen_block, chosen_blocks[3], chosen).play(*anims_19_1, lightening_19_1, lightening_19_2)
        self.add(*links_19_2, chosen_block, chosen_blocks[3], chosen).play(*anims_19_2)
        self.waiting(0, 15)

        links_20_1, anims_20_1, lightening_20_1, tearing_20_1, fading_20_1 = message_get_need(part_message[17], chosen_blocks[18], get_color(20))
        links_20_2, anims_20_2, lightening_20_2, tearing_20_2, fading_20_2 = cypher_get_need(part_cypher[9], chosen_blocks[18], get_color(20))
        self.play(*[FadeOut(mob) for mob in [*links_18_1, *links_18_2, *links_19_1, *links_19_2, chosen_blocks[3]]], fading_18_1, fading_18_2)
        self.add(*links_20_1, chosen_block, chosen).play(*anims_20_1, lightening_20_1, lightening_20_2)
        self.add(*links_20_2, chosen_block, chosen).play(*anims_20_2)
        links_21_1, anims_21_1, lightening_21_1, _, _ = message_get_need(part_message[25], chosen_blocks[10], get_color(21))
        links_21_2, anims_21_2, lightening_21_2, _, _ = cypher_get_need(part_cypher[9], chosen_blocks[10], get_color(21))
        self.play(FadeIn(chosen_blocks[10]))
        self.add(*links_21_1, chosen_block, chosen_blocks[10], chosen).play(*anims_21_1, lightening_21_1, lightening_21_2)
        self.add(*links_21_2, chosen_block, chosen_blocks[10], chosen).play(*anims_21_2)
        self.waiting(0, 15)

        links_22_1, anims_22_1, lightening_22_1, tearing_22_1, fading_22_1 = message_get_need(part_message[1], chosen_blocks[18], get_color(22))
        links_22_2, anims_22_2, lightening_22_2, tearing_22_2, fading_22_2 = cypher_get_need(part_cypher[19], chosen_blocks[18], get_color(22))
        self.play(*[FadeOut(mob) for mob in [*links_20_1, *links_20_2, *links_21_1, *links_21_2, chosen_blocks[10]]], fading_20_1, fading_20_2)
        self.add(*links_22_1, chosen_block, chosen).play(*anims_22_1, lightening_22_1, lightening_22_2)
        self.add(*links_22_2, chosen_block, chosen).play(*anims_22_2)
        links_23_1, anims_23_1, lightening_23_1, _, _ = message_get_need(part_message[25], chosen_blocks[20], get_color(23))
        links_23_2, anims_23_2, lightening_23_2, _, _ = cypher_get_need(part_cypher[19], chosen_blocks[20], get_color(23))
        self.play(FadeIn(chosen_blocks[20]))
        self.add(*links_23_1, chosen_block, chosen_blocks[20], chosen).play(*anims_23_1, lightening_23_1, lightening_23_2)
        self.add(*links_23_2, chosen_block, chosen_blocks[20], chosen).play(*anims_23_2)
        self.waiting(0, 15)

        shade_all = Rectangle(width = 10.4, height = 5, fill_opacity = 1, fill_color = "#333333", stroke_width = 0)
        self.play(*[FadeOut(mob) for mob in [*links_22_1, *links_22_2, *links_23_1, *links_23_2, chosen_blocks[20]]], fading_22_1, fading_22_2, FadeIn(shade_all))
        self.waiting(0, 15) # 都应该把不同的明文 变成不同的密文 （空闲） 于是 所有可能的密文的总数 应该不小于所有可能的明文的总数 （空闲） 如果这套加密方案能完美加密 那么对于任何一个密文来说 既然一个明文能加密出它来 所有明文就应该都能加密出它来才对 （空闲） 也就是说 一个明文要有可能加密出所有的密文 于是 每条密文至少要对应一种加密方法 （空闲）那么 一个完美加密的加密方案 所拥有的加密方法的数量 也就是密钥的数量 至少不能比明文少 （空闲）
        title_all = VGroup(title_scheme, title_message, title_cypher, count_messages, count_cyphers, more_cyphers, count_keys, more_keys)
        self.clear().add(notice10, title_all)
        
        text_letter = "perfectsecrecy"
        cypher_letter = ""
        shifting = [12, 24, 13, 1, 8, 16, 15, 12, 25, 9, 15, 11, 18, 6]
        example = Text(text_letter, font = "Times New Roman").scale(0.8).shift(1.5*UP)
        for i in range(14):
            example[i].set_x(0.9*(i-6.5))
            cypher, _ = caeser(text_letter[i], shifting[i])
            cypher_letter += cypher
        example_cypher = Text(cypher_letter, font = "Times New Roman", color = YELLOW_E).scale(0.8).shift(1.5*DOWN)
        arrows = VGroup()
        keys = VGroup()
        for i in range(14):
            example_cypher[i].set_x(0.9*(i-6.5))
            arrow = Arrow(1*UP, 1*DOWN, buff = 0).shift(0.9*(i-6.5)*RIGHT)
            key = MTex("+" + str(shifting[i])).scale(0.5).shift((0.9*(i-6.5) + 0.3)*RIGHT)
            arrows.add(arrow)
            keys.add(key)
        arrows.set_color(BLUE)
        keys.set_color(BLUE)

        center = VMobject(stroke_color = YELLOW)
        center.set_points([0.15*LEFT, ORIGIN, 0.15*RIGHT, 0.15*UP, ORIGIN, 0.15*DOWN])
        corner = VMobject(stroke_color = YELLOW)
        corner.set_points_as_corners([0.2*DOWN, 0.2*DOWN+0.2*LEFT, 0.2*LEFT])
        corners = [corner.copy().rotate(i*PI/2, about_point=ORIGIN) for i in range(4)]
        initial = VGroup(center, *corners)
        initial_message = initial.copy().shift(1.5*UP)
        initial_keys = initial.copy().shift(0.3*RIGHT)
        aim_message = initial.copy().shift(1.5*UP).set_opacity(0)
        aim_keys = initial.copy().shift(0.3*RIGHT).set_opacity(0)
        aim_cypher = initial.copy().shift(1.5*DOWN).set_opacity(0)
        indicate_message = SurroundingRectangle(example)
        opened_aim = VGroup(center.copy(), corners[0].copy().shift(6.1*LEFT + 0.1*DOWN), corners[1].copy().shift(6.1*RIGHT + 0.1*DOWN), corners[2].copy().shift(6.1*RIGHT + 0.1*UP), corners[3].copy().shift(6.1*LEFT + 0.1*UP))
        to_message = opened_aim.copy().shift(1.5*UP)
        to_keys = opened_aim.copy().shift(0.3*RIGHT)
        to_cypher = opened_aim.copy().shift(1.5*DOWN)

        self.play(*[FadeIn(mob, 0.5*UP) for mob in [example, example_cypher, arrows, keys]], ReplacementTransform(notice10, notice11))
        self.waiting(1, 27) #这似乎正好对应了单次密码簿中
        self.add(aim_message, aim_keys).play(Transform(aim_message, to_message), Transform(aim_keys, to_keys))
        self.waiting(1, 23) #密钥长度要等于明文长度的情况
        self.waiting(0, 16) #（空闲）

        self.waiting(1, 3)
        self.play(Transform(aim_message, initial_message), Transform(aim_keys, initial_keys)) #但如果我们仔细想一想
        alpha = ValueTracker(0.0)
        def message_updater(mob: VMobject):
            ratio = alpha.get_value()
            rotate_factor = smooth(ratio)
            scale_factor = breath(1 - ratio)
            mob.become(initial_message).scale(scale_factor).rotate(rotate_factor * TAU)
        def cypher_updater(mob: VMobject):
            ratio = alpha.get_value()
            rotate_factor = smooth(ratio)
            scale_factor = breath(1 - ratio)
            mob.become(initial_keys).scale(scale_factor).rotate(rotate_factor * TAU)
        aim_message.add_updater(message_updater)
        aim_keys.add_updater(cypher_updater)
        self.play(alpha.animate.set_value(1.0), rate_func = linear)
        aim_message.clear_updaters()
        aim_keys.clear_updaters()
        self.remove(alpha, aim_message, aim_keys)
        self.waiting(0, 27) #就会发现并非如此
        self.waiting(0, 21) #（空闲）

        self.add(aim_cypher).play(Transform(aim_cypher, to_cypher))
        self.waiting(1, 27) #虽然密文可以是所有可能的字符串
        self.play(ShowCreation(indicate_message))
        self.waiting(2, 1) #但是明文显然有很明显的拼写规律在
        self.waiting(0, 17) #（空闲）

        rectangle_up = Rectangle(height = 8, width = 16, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        rectangle_inner = Rectangle(height = 7.8, width = 16, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        rectangle_up.add(rectangle_inner).shift(9*DOWN)

        template = MTex("abcdefghijklmnopqrstuvwxyz")
        template_letters = template.submobjects
        for mob in template.submobjects:
            mob.set_x(0)
        letters = [VMobject(stroke_width = 0) for _ in range(5)]
        alpha = ValueTracker(0.0)
        beta = ValueTracker(-7.0)
        arrow = Arrow(DOWN, 0.1*DOWN, color = GREEN)
        choice = Text("26种", font = "simsun", color = GREEN).scale(0.3).shift(DOWN).add(arrow)
        choices = VGroup(*[choice.copy().shift((i-2)*0.5 * RIGHT) for i in range(5)])
        all_choices = MTex("26^5 = 11881376", color = GREEN).shift(UP)
        def opacity_updater(mob: VMobject):
            mob.set_opacity(alpha.get_value())
        def changing_updater(mob: VMobject):
            if mob.counter % 3 == 0:
                mob.random = random.randint(0, 25)
            mob.set_points(template_letters[mob.random].get_points()).shift(np.array([mob.position_x, beta.get_value(), 0]))
            mob.counter += 1
        for i in range(5):
            letters[i].position_x = (i-2)*0.5
            letters[i].counter = random.randint(0, 2)
            letters[i].random = random.randint(0, 25)
            letters[i].add_updater(changing_updater).add_updater(opacity_updater)
        self.add(rectangle_up, *letters).play(rectangle_up.animate.shift(7*UP), alpha.animate.set_value(1.0), beta.animate.set_value(0.0))
        self.remove(aim_cypher, indicate_message, example, example_cypher, arrows, keys)
        self.play(FadeIn(choices, 0.5*UP, lag_atio = 0.3), Write(all_choices))
        self.waiting(0, 26) #五个字母的字符串总共有一千多万种
        self.waiting(2, 22) #而所有的英语单词加起来都没那么多
        self.waiting(0, 17) #（空闲）

        text_1 = MTexText("perfect").shift(1.5*UP + 2*LEFT)
        text_2 = MTexText("secrecy").shift(1.5*UP + 2*RIGHT)
        arrow_1 = Arrow(1*UP + 2*LEFT, 1*DOWN + 2*LEFT, buff = 0, color = BLUE)
        arrow_2 = Arrow(1*UP + 2*RIGHT, 1*DOWN + 2*RIGHT, buff = 0, color = BLUE)
        key_1 = Text("密钥1", font = "simsun", color = BLUE).scale(0.4).next_to(2*LEFT)
        key_2 = Text("密钥2", font = "simsun", color = BLUE).scale(0.4).next_to(2*RIGHT)
        cypher_1 = MTexText("carrot", color = YELLOW_E).shift(1.5*DOWN + 2*LEFT)
        cypher_2 = MTexText("rabbit", color = YELLOW_E).shift(1.5*DOWN + 2*RIGHT)
        self.bring_to_back(text_1, text_2, arrow_1, arrow_2, cypher_1, cypher_2, key_1, key_2).play(beta.animate.set_value(-7.0), *[mob.animate.shift(7*DOWN) for mob in [rectangle_up, choices, all_choices]], ReplacementTransform(notice11, notice12))
        self.remove(rectangle_up, choices, all_choices, *letters)
        self.waiting(1, 1) #如果我们换一套加密方案
        self.waiting(2, 15) #根本没必要准备那么长的密钥
        self.waiting(0, 19) #（空闲）

        self.waiting(1, 7) #更进一步
        coin_1 = Circle(radius = 0.3, stroke_width = 0, fill_opacity = 1, fill_color = RED).add(Text("T", font = "Times New Roman").scale(0.7)).shift(1.5*UP + 2*LEFT)
        coin_2 = Circle(radius = 0.3, stroke_width = 0, fill_opacity = 1, fill_color = GOLD_D).add(Text("H", font = "Times New Roman").scale(0.7)).shift(1.5*UP + 2*RIGHT)
        self.play(FadeOut(text_1), FadeOut(text_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(coin_1), FadeIn(coin_2), run_time = 0.5, rate_func = rush_from)
        self.waiting(1, 0)
        sanlian_1 = Text("", font = 'vanfont', color = "#F25D8E").shift(1.5*UP + 2*LEFT)
        sanlian_2 = Text("", font = 'vanfont', color = "#F25D8E").shift(1.5*UP + 2*RIGHT)
        self.play(FadeOut(coin_1), FadeOut(coin_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(sanlian_1), FadeIn(sanlian_2), run_time = 0.5, rate_func = rush_from)
        self.waiting(1, 0)
        emoji_1 = Text("_(:зゝ∠)_", font = 'simsun').scale(0.9).shift(1.5*UP + 2*LEFT)
        emoji_2 = Text("(|||ﾟДﾟ)", font = 'simsun').scale(0.9).shift(1.5*UP + 2*RIGHT)
        self.play(FadeOut(sanlian_1), FadeOut(sanlian_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(emoji_1), FadeIn(emoji_2), run_time = 0.5, rate_func = rush_from)
        self.waiting(1, 0)
        bin_1 = MTex("01011001", font = 'simsun', color = YELLOW_E).shift(1.5*DOWN + 2*LEFT)
        bin_2 = MTex("01000011", font = 'simsun', color = YELLOW_E).shift(1.5*DOWN + 2*RIGHT)
        self.play(FadeOut(cypher_1), FadeOut(cypher_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(bin_1), FadeIn(bin_2), run_time = 0.5, rate_func = rush_from)
        self.waiting(1, 0)
        svg_1 = SVGMobject("Sleep_Carrot.svg", color = YELLOW_E, height = None).scale(0.01).shift(1.5*DOWN + 2*LEFT)
        svg_2 = SVGMobject("Sleep_Bunny.svg", color = YELLOW_E, height = None).scale(0.005).shift(1.5*DOWN + 2*RIGHT)
        self.play(FadeOut(bin_1), FadeOut(bin_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(svg_1), FadeIn(svg_2), run_time = 0.5, rate_func = rush_from)
        self.waiting(1, 0)
        number_1 = MTex("367458", font = 'simsun', color = YELLOW_E).shift(1.5*DOWN + 2*LEFT)
        number_2 = MTex("109826", font = 'simsun', color = YELLOW_E).shift(1.5*DOWN + 2*RIGHT)
        self.play(FadeOut(svg_1), FadeOut(svg_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(number_1), FadeIn(number_2), run_time = 0.5, rate_func = rush_from)
        self.waiting(2+1+2+1+3-11, 16+29+25+12+5) #明文甚至不需要是语言 无论什么种类的信息 我们都能设置一套相应的加密方案 而相对应的 密文也可以是任意种类的信息
        self.clear().add(notice12)
        latour = ImageMobject("picture_Latour.jpg", height = 4)
        bv_id = Text("BV1aa411r7aQ", font = "Times New Roman").next_to(2*UP, UP)
        self.play(FadeIn(latour, 0.5*UP), FadeIn(bv_id, 0.5*UP), ReplacementTransform(notice12, notice13))
        self.waiting(0, 9) #二战时期
        self.waiting(4, 26) #菲利斯·皮帕·拉图尔就曾经运用针织图案来传递情报
        self.waiting(2, 17) #而这 即使在现在看来
        self.waiting(1+0-1, 27+12) #也仍然是一种完美的加密 （空闲）
        self.play(FadeOut(latour, 0.5*DOWN), FadeOut(bv_id, 0.5*DOWN))

        text_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        text_codes = ['\cdot -', '-\cdot \cdot \cdot ', '-\cdot -\cdot ', '-\cdot \cdot ', '\cdot ', '\cdot \cdot -\cdot ', '--\cdot ', '\cdot \cdot \cdot \cdot ', '\cdot \cdot ', '\cdot ---', '-\cdot -', '\cdot -\cdot \cdot ', '--', '-\cdot ', '---', '\cdot --\cdot ', '--\cdot -', '\cdot -\cdot ', '\cdot \cdot \cdot ', '-', '\cdot \cdot -', '\cdot \cdot \cdot -', '\cdot --', '-\cdot \cdot -', '-\cdot --', '--\cdot \cdot ']
        letters = []
        codes = []
        for i in range(2):
            for j in range(13):
                order = i*13 + j
                letter_i = Text(text_letters[order], font = "simsun").scale(0.9).shift((i-0.5)*4*RIGHT + (j-6)*0.5*DOWN + 0.4*UP + 1*LEFT)
                code_i = MTex(text_codes[order], color = YELLOW_E).next_to((i-0.5)*4*RIGHT + (j-6)*0.5*DOWN + 0.4*UP, RIGHT)
                letters.append(letter_i)
                codes.append(code_i)
        table = VGroup(*letters, *codes)
        self.play(FadeIn(table, 0.5*DOWN), ReplacementTransform(notice13, notice14))
        self.waiting(2, 2) #甚至 我们熟悉的任何一种编码
        self.waiting(2, 17) #其实都可以看作是一种加密系统
        self.waiting(3, 14) #只不过 它们大多数只有一套编码方案
        self.waiting(2, 4) #根本没有任何的安全性可言

        self.waiting(3, 13)
        self.play(*[FadeOut(mob) for mob in [table, notice14]])
        self.waiting(3, 13) #到此共130秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

######################################################################################################

class Chapter3_0(Scene):

    def construct(self):

        ##  Making object
        text3 = Text("第三节 单向函数与公钥加密", font = 'simsun', t2c={"第三节": YELLOW, "单向函数": GREEN, "公钥加密": BLUE})

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(Scene):

    def construct(self):

        notice1 = Notice("前情提要", "请　复习")

        title_scheme = Text("加密方案", font = "simsun", color = BLUE).shift(2.8*UP)
        title_message = Text("明文", font = "simsun", color = WHITE).shift(2.8*UP + 4*LEFT)
        title_cypher = Text("密文", font = "simsun", color = YELLOW_E).shift(2.8*UP + 4*RIGHT)
        blocks = []
        block_per_layer = [2, 3, 4, 4, 4, 4, 3, 2]
        order = 0
        for i in range(8):
            number = block_per_layer[i]
            for j in range(number):
                position = 0.6*UP*(i-3.5) + 1.2*RIGHT*(j-(number-1)/2)
                number_i = MTex(str(order), color = BLUE_D).scale(0.7)
                block_i =  DoubleArrow().add(number_i).shift(position).save_state()
                blocks.append(block_i)
                order += 1
        addings = [*blocks]
        random.shuffle(addings)
        addings = [title_scheme, title_message, title_cypher] + addings
        number = len(addings)
        shade = Square(side_length = 4.8, fill_opacity = 1, stroke_width = 0, fill_color = "#333333")
        anim_addings = [FadeIn(addings[i], 0.5*UP, squish_interval = (i/(number+8), (i+9)/(number+8)), run_time = 2) for i in range(number)]
        self.bring_to_back(shade).play(Write(notice1), *anim_addings)
        self.waiting(1+3-2, 16+13) #到现在为止 我们已经搭好了现代密码学最重要的框架
        self.waiting(0, 20) #（空闲）

        self.waiting(1, 21) #比起古典密码学
        position_lu = 4.5*LEFT + 0.5*UP
        position_ld = 4.5*LEFT + 0.5*DOWN
        position_ru = 4.5*RIGHT + 0.5*UP
        position_rd = 4.5*RIGHT + 0.5*DOWN
        text_sleep = MTexText("sleep").shift(position_lu)
        text_bunny = MTexText("bunny").shift(position_ld)
        arrow = Arrow(3.5*LEFT, 3.5*RIGHT, color = BLUE, stroke_width = 10, buff = 0)
        text_hatte = MTexText("hatte", color = YELLOW_E).shift(position_ru)
        text_cvooz = MTexText("cvooz", color = YELLOW_E).shift(position_rd)
        self.play(Write(text_sleep), Write(text_bunny))
        self.bring_to_back(arrow).play(ShowCreation(arrow))
        self.play(Write(text_hatte), Write(text_cvooz))
        self.waiting(0, 14) #香农发现了保密的核心在于掩盖不同

        perfect_secrecy = Text("完美加密：任意两个明文可能被加密成的密文的概率分布相同", font = "simsun", color = YELLOW).scale(0.6).shift(3.5*UP)
        self.play(FadeIn(perfect_secrecy, 0.5*RIGHT))
        self.waiting(1, 19) #并由此确定了完美加密的要求
        self.waiting(0, 17) #（空闲）

        coin_1 = Circle(radius = 0.3, stroke_width = 0, fill_opacity = 1, fill_color = RED).add(Text("T", font = "Times New Roman").scale(0.7)).shift(position_lu)
        coin_2 = Circle(radius = 0.3, stroke_width = 0, fill_opacity = 1, fill_color = GOLD_D).add(Text("H", font = "Times New Roman").scale(0.7)).shift(position_ld)
        self.play(FadeOut(text_sleep), FadeOut(text_bunny), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(coin_1), FadeIn(coin_2), run_time = 0.5, rate_func = rush_from)
        sanlian_1 = Text("", font = 'vanfont', color = "#F25D8E").shift(position_ru)
        sanlian_2 = Text("", font = 'vanfont', color = "#F25D8E").shift(position_rd)
        self.play(FadeOut(text_hatte), FadeOut(text_cvooz), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(sanlian_1), FadeIn(sanlian_2), run_time = 0.5, rate_func = rush_from)
        emoji_1 = Text("_(:зゝ∠)_", font = 'simsun').scale(0.6).shift(position_lu)
        emoji_2 = Text("(|||ﾟДﾟ)", font = 'simsun').scale(0.6).shift(position_ld)
        self.play(FadeOut(coin_1), FadeOut(coin_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(emoji_1), FadeIn(emoji_2), run_time = 0.5, rate_func = rush_from)
        svg_1 = SVGMobject("Sleep_Carrot.svg", color = YELLOW_E, height = None).scale(0.01).shift(position_ru)
        svg_2 = SVGMobject("Sleep_Bunny.svg", color = YELLOW_E, height = None).scale(0.005).shift(position_rd)
        self.play(FadeOut(sanlian_1), FadeOut(sanlian_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(svg_1), FadeIn(svg_2), run_time = 0.5, rate_func = rush_from)
        bin_1 = MTex("01011001", font = 'simsun').shift(position_lu)
        bin_2 = MTex("01000011", font = 'simsun').shift(position_ld)
        self.play(FadeOut(emoji_1), FadeOut(emoji_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(bin_1), FadeIn(bin_2), run_time = 0.5, rate_func = rush_from)
        number_1 = MTex("367458", font = 'simsun', color = YELLOW_E).shift(position_ru)
        number_2 = MTex("109826", font = 'simsun', color = YELLOW_E).shift(position_rd)
        self.play(FadeOut(svg_1), FadeOut(svg_2), run_time = 0.5, rate_func = rush_into)
        self.play(FadeIn(number_1), FadeIn(number_2), run_time = 0.5, rate_func = rush_from)
        self.waiting(1+3+1+0-6, 9+3+25+16) #相应的 明文和密文不再需要是一段文本 而是任何格式都可以 （空闲）
        
        indicate = SurroundingRectangle(blocks[18])
        self.play(ShowCreation(indicate), FadeOut(perfect_secrecy), *[mob.animate.fade() for mob in [*blocks[0:18], *blocks[19:26], title_scheme]])
        self.waiting(0, 6) #一对加密和解密的算法......
        
        def message_get_need(message: VMobject, algorithm: VMobject, line_color, reversed: bool = False):
            link = HorizontalLink(message.get_corner(RIGHT) + 0.1*RIGHT, algorithm.get_center(), color = line_color)
            shade = link.copy().set_stroke(width = 10, color = "#333333")
            if reversed:
                link.reverse_points()
                shade.reverse_points()
                show_func = rush_from
                tear_func = inverse_rush_from
            else:
                show_func = rush_into
                tear_func = inverse_rush_into
            anim_1 = ShowCreation(shade, rate_func = show_func, run_time = 0.5)
            anim_2 = ShowCreation(link, rate_func = show_func, run_time = 0.5)
            anim_4 = Uncreate(shade, rate_func = tear_func, run_time = 0.5)
            anim_5 = Uncreate(link, rate_func = tear_func, run_time = 0.5)
            return [shade, link], [anim_1, anim_2], [anim_4, anim_5]

        def cypher_get_need(cypher: VMobject, algorithm: VMobject, line_color, reversed: bool = False):
            link = HorizontalLink(algorithm.get_center(), cypher.get_corner(LEFT) + 0.1*LEFT, color = line_color)
            shade = link.copy().set_stroke(width = 10, color = "#333333")
            if reversed:
                link.reverse_points()
                shade.reverse_points()
                show_func = rush_into
                tear_func = inverse_rush_into
            else:
                show_func = rush_from
                tear_func = inverse_rush_from
            anim_1 = ShowCreation(shade, rate_func = show_func, run_time = 0.5)
            anim_2 = ShowCreation(link, rate_func = show_func, run_time = 0.5)
            anim_4 = Uncreate(shade, rate_func = tear_func, run_time = 0.5)
            anim_5 = Uncreate(link, rate_func = tear_func, run_time = 0.5)
            return [shade, link], [anim_1, anim_2], [anim_4, anim_5]

        links_1_1, anims_1_1, tearing_1_1 = message_get_need(bin_1, blocks[18], RED_A)
        links_1_2, anims_1_2, tearing_1_2 = cypher_get_need(number_2, blocks[18], RED_A)
        self.add(*links_1_1, blocks[18], indicate).play(*anims_1_1)
        self.add(*links_1_2, blocks[18], indicate).play(*anims_1_2)
        self.waiting(0, 15)

        for mob in [*links_1_1, *links_1_2]:
            mob.reverse_points()
        links_2_1, anims_2_1, tearing_2_1 = cypher_get_need(number_1, blocks[18], ORANGE_A, True)
        links_2_2, anims_2_2, tearing_2_2 = message_get_need(bin_2, blocks[18], ORANGE_A, True)
        self.add(*links_2_1, blocks[18], indicate).play(*tearing_1_1, *anims_2_1)
        self.add(*links_2_2, blocks[18], indicate).play(*tearing_1_2, *anims_2_2)
        self.waiting(0, 15)

        for mob in [*links_2_1, *links_2_2]:
            mob.reverse_points()
        self.play(*tearing_2_1)
        self.play(*tearing_2_2)
        self.waiting(0, 6) #是一种明文和密文之间的一一映射

        indicate_all = Square(side_length = 4.8, color = YELLOW)
        self.play(Transform(indicate, indicate_all), *[mob.animate.restore() for mob in blocks], title_scheme.animate.set_opacity(1))
        self.waiting(2, 22) #一套加密方案由许多这样的一一映射组成
        self.waiting(1, 19) #需要加密的时候
        chosen = SurroundingRectangle(blocks[11])
        self.play(ShowCreation(chosen), *[mob.animate.fade() for mob in [*blocks[0:11], *blocks[12:26], title_scheme, indicate]])
        self.waiting(1, 1) #就从里面随机挑一个
        self.waiting(0, 17) #（空闲）

        self.waiting(2, 10) #这就是之前所有的重点
        self.waiting(1, 18) #能够理清的话
        self.play(*[mob.animate.restore() for mob in blocks], title_scheme.animate.set_opacity(1), FadeOut(indicate), FadeOut(chosen))
        self.waiting(2, 15) #剩下的时间 我们可以来看一看公钥加密
        self.waiting(1, 13) #到此共43秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_2(Scene):

    def construct(self):

        notice1 = Notice("前情提要", "请　复习")
        notice2 = Notice("转换思路", "请　模仿")
        notice3 = Notice("异想天开", "请勿模仿")
        notice4 = Notice("转换思路", "请　模仿")
        notice5 = Notice("前沿猜想", "请　了解")
        notice6 = Notice("两难问题", "请　思考")
        notice7 = Notice("转换思路", "请　模仿")

        def message_get_need(message: VMobject, algorithm: VMobject, line_color, reversed: bool = False):
            link = HorizontalLink(message.get_corner(RIGHT) + 0.2*RIGHT, algorithm.get_center(), color = line_color)
            shade = link.copy().set_stroke(width = 10, color = "#333333")
            if reversed:
                link.reverse_points()
                shade.reverse_points()
                show_func = rush_from
                tear_func = inverse_rush_from
            else:
                show_func = rush_into
                tear_func = inverse_rush_into
            anim_1 = ShowCreation(shade, rate_func = show_func, run_time = 0.5)
            anim_2 = ShowCreation(link, rate_func = show_func, run_time = 0.5)
            anim_4 = Uncreate(shade, rate_func = tear_func, run_time = 0.5)
            anim_5 = Uncreate(link, rate_func = tear_func, run_time = 0.5)
            return [shade, link], [anim_1, anim_2], [anim_4, anim_5]

        def cypher_get_need(cypher: VMobject, algorithm: VMobject, line_color, reversed: bool = False):
            link = HorizontalLink(algorithm.get_center(), cypher.get_corner(LEFT) + 0.2*LEFT, color = line_color)
            shade = link.copy().set_stroke(width = 10, color = "#333333")
            if reversed:
                link.reverse_points()
                shade.reverse_points()
                show_func = rush_into
                tear_func = inverse_rush_into
            else:
                show_func = rush_from
                tear_func = inverse_rush_from
            anim_1 = ShowCreation(shade, rate_func = show_func, run_time = 0.5)
            anim_2 = ShowCreation(link, rate_func = show_func, run_time = 0.5)
            anim_4 = Uncreate(shade, rate_func = tear_func, run_time = 0.5)
            anim_5 = Uncreate(link, rate_func = tear_func, run_time = 0.5)
            return [shade, link], [anim_1, anim_2], [anim_4, anim_5]

        title_scheme = Text("加密方案", font = "simsun", color = BLUE).shift(2.8*UP)
        title_message = Text("明文", font = "simsun", color = WHITE).shift(2.8*UP + 4*LEFT)
        title_cypher = Text("密文", font = "simsun", color = YELLOW_E).shift(2.8*UP + 4*RIGHT)
        blocks = []
        block_per_layer = [2, 3, 4, 4, 4, 4, 3, 2]
        order = 0
        for i in range(8):
            number = block_per_layer[i]
            for j in range(number):
                position = 0.6*UP*(i-3.5) + 1.2*RIGHT*(j-(number-1)/2)
                number_i = MTex(str(order), color = BLUE_D).scale(0.7)
                block_i =  DoubleArrow().add(number_i).shift(position)
                blocks.append(block_i)
                order += 1
        shade = Square(side_length = 4.8, fill_opacity = 1, stroke_width = 0, fill_color = "#333333")
        indicate_all = Square(side_length = 4.8, color = YELLOW)
        
        bin_1 = MTex("01011001", font = 'simsun').shift(4.5*LEFT + 0.5*UP)
        bin_2 = MTex("01000011", font = 'simsun').shift(4.5*LEFT + 0.5*DOWN)
        number_1 = MTex("367458", font = 'simsun', color = YELLOW_E).shift(4.5*RIGHT + 0.5*UP)
        number_2 = MTex("109826", font = 'simsun', color = YELLOW_E).shift(4.5*RIGHT + 0.5*DOWN)
        arrow = Arrow(3.5*LEFT, 3.5*RIGHT, color = BLUE, stroke_width = 10, buff = 0)
        
        self.add(notice1, arrow, shade, title_scheme, title_message, title_cypher, *blocks, bin_1, bin_2, number_1, number_2)
        
        perfect_secrecy = MTexText("完美加密：$m\le c\le k$", tex_to_color_map = {"完美加密": YELLOW, 'c': YELLOW_E, 'k': BLUE}).scale(0.8).shift(3.5*UP)
        key = perfect_secrecy.get_part_by_tex("k")
        self.play(FadeIn(perfect_secrecy, 0.5*RIGHT), ReplacementTransform(notice1, notice2))
        self.waiting(1, 18) #完美加密可以做到完全保密
        self.play(ShowCreationThenDestructionAround(key), run_time = 2)
        self.waiting(0, 2) #但它需要很长的密钥
        self.play(*[FadeOut(mob) for mob in [bin_1, bin_2, number_1, number_2]])
        self.waiting(0, 19) #实际上用途不大
        self.waiting(0, 18) #（空闲）

        self.play(RollUp(perfect_secrecy, left_bound = -10, right_bound = 2))
        self.waiting(1+1-3, 20+23) #为了能有实际应用 我们需要换一种思路
        self.waiting(0, 19) #（空闲）

        text_messages = ["01010011", "01001000", "01001111", "01010101", "01000011", "01000001", "01001110", "01000111"]
        messages = [MTex(text_messages[i]).scale(0.8).shift(4.5*LEFT + (i-3.5)*0.5*DOWN) for i in range(8)]
        cyphers = [MTex(str(random.randint(100000, 999999)), color = YELLOW_E).scale(0.8).shift(4.5*RIGHT + (i-3.5)*0.5*DOWN) for i in range(8)]
        self.play(*[FadeIn(messages[7-i], 0.5*DOWN, squish_interval = (i/10, (i+3)/10), run_time = 2) for i in range(8)], *[FadeIn(cyphers[7-i], 0.5*DOWN, squish_interval = (i/10, (i+3)/10), run_time = 2) for i in range(8)])
        self.waiting(0, 12) #保密的核心在于掩盖不同
        self.play(ShowCreationThenDestruction(indicate_all, run_time = 2), ReplacementTransform(notice2 ,notice3))
        self.waiting(0, 7) #而要是一套加密方案里面

        indicate = SurroundingRectangle(blocks[11])
        self.play(ShowCreation(indicate), *[mob.animate.fade(0.8) for mob in [*blocks[0:11], *blocks[12:26]]])
        links_1_1, anims_1_1, tearing_1_1 = message_get_need(messages[0], blocks[11], RED_A)
        links_1_2, anims_1_2, tearing_1_2 = cypher_get_need(cyphers[5], blocks[11], RED_A)
        self.add(*links_1_1, blocks[11], indicate).play(*anims_1_1)
        self.add(*links_1_2, blocks[11], indicate).play(*anims_1_2)
        self.waiting(0, 15)

        for mob in [*links_1_1, *links_1_2]:
            mob.reverse_points()
        links_2_1, anims_2_1, _ = cypher_get_need(cyphers[3], blocks[11], ORANGE_A, True)
        cross = VMobject(color = RED, stroke_width = 10).set_points([0.3*UR, ORIGIN, 0.3*DL, 0.3*UL, ORIGIN, 0.3*DR]).move_to(blocks[11].get_corner(LEFT)).save_state()
        alpha = ValueTracker(0.0)
        def warning_updater(mob: VMobject):
            a = alpha.get_value()
            if a < 0.1:
                color = RED
            elif a < 0.2:
                color = WHITE
            elif a < 0.3:
                color = RED
            elif a < 0.4:
                color = WHITE
            elif a < 0.5:
                color = RED
            else:
                color = GREY
            m,n = 4,5
            Lissajous = np.sin(m*TAU*a/0.5) * 0.05 * UP + np.cos(n*TAU*a/0.5) * 0.05 * RIGHT
            mob.restore().set_color(color).shift(Lissajous)
        cross.add_updater(warning_updater)
        self.add(*links_2_1, blocks[11], indicate).play(*tearing_1_1, *anims_2_1)
        self.add(cross).play(*tearing_1_2, ApplyMethod(alpha.set_value, 0.5, rate_func = linear), run_time = 0.5)
        cross.clear_updaters()
        self.play(*[FadeOut(mob) for mob in [cross, *links_2_1]], run_time = 0.5)
        self.waiting(1+2+2-4, 19+22+17) #每一种加密算法 都无法根据输出反推输入 那么 明文即使有不同
        self.waiting(1, 11) #也没法被发现
        self.waiting(0, 22) #（空闲）

        indicate_cypher = SurroundingRectangle(cyphers[3])
        self.play(ShowCreation(indicate_cypher))
        self.waiting(1, 5) #这严格来说不可能
        links_1_1, anims_1_1, tearing_1_1 = message_get_need(messages[0], blocks[11], RED_A)
        links_1_2, anims_1_2, tearing_1_2 = cypher_get_need(cyphers[5], blocks[11], RED_A)
        self.add(*links_1_1, blocks[11], indicate).play(*anims_1_1)
        self.add(*links_1_2, blocks[11], indicate).play(*anims_1_2)
        for mob in [*links_1_1, *links_1_2]:
            mob.reverse_points()
        links_2_1, anims_2_1, tearing_2_1 = message_get_need(messages[1], blocks[11], ORANGE_A)
        links_2_2, anims_2_2, tearing_2_2 = cypher_get_need(cyphers[1], blocks[11], ORANGE_A)
        self.add(*links_2_1, blocks[11], indicate).play(*tearing_1_1, *anims_2_1)
        self.add(*links_2_2, blocks[11], indicate).play(*tearing_1_2, *anims_2_2)
        for mob in [*links_2_1, *links_2_2]:
            mob.reverse_points()
        links_3_1, anims_3_1, tearing_3_1 = message_get_need(messages[2], blocks[11], YELLOW_A)
        links_3_2, anims_3_2, tearing_3_2 = cypher_get_need(cyphers[6], blocks[11], YELLOW_A)
        self.add(*links_3_1, blocks[11], indicate).play(*tearing_2_1, *anims_3_1)
        self.add(*links_3_2, blocks[11], indicate).play(*tearing_2_2, *anims_3_2)
        for mob in [*links_3_1, *links_3_2]:
            mob.reverse_points()
        links_4_1, anims_4_1, tearing_4_1 = message_get_need(messages[3], blocks[11], GREEN_A)
        links_4_2, anims_4_2, tearing_4_2 = cypher_get_need(cyphers[2], blocks[11], GREEN_A)
        self.add(*links_4_1, blocks[11], indicate).play(*tearing_3_1, *anims_4_1)
        self.add(*links_4_2, blocks[11], indicate).play(*tearing_3_2, *anims_4_2)
        for mob in [*links_4_1, *links_4_2]:
            mob.reverse_points()
        links_5_1, anims_5_1, tearing_5_1 = message_get_need(messages[4], blocks[11], TEAL_A)
        links_5_2, anims_5_2, tearing_5_2 = cypher_get_need(cyphers[7], blocks[11], TEAL_A)
        self.add(*links_5_1, blocks[11], indicate).play(*tearing_4_1, *anims_5_1)
        self.add(*links_5_2, blocks[11], indicate).play(*tearing_4_2, *anims_5_2)
        for mob in [*links_5_1, *links_5_2]:
            mob.reverse_points()
        links_6_1, anims_6_1, tearing_6_1 = message_get_need(messages[5], blocks[11], BLUE_A)
        links_6_2, anims_6_2, tearing_6_2 = cypher_get_need(cyphers[3], blocks[11], BLUE_A)
        self.add(*links_6_1, blocks[11], indicate).play(*tearing_5_1, *anims_6_1)
        self.add(*links_6_2, blocks[11], indicate).play(*tearing_5_2, *anims_6_2)
        indicate_message = SurroundingRectangle(messages[5])
        self.play(ShowCreation(indicate_message))
        self.waiting(3+2+2-7, 4+1+12) # #对于一一映射的加密和解密算法来说 只要知道了确定的输出 至少也可以穷举出对应的输入
        self.waiting(0, 15) #（空闲）

        self.play(ReplacementTransform(notice3, notice4)) 
        self.waiting(1, 28) #但没关系 我们可以退一步
        self.waiting(3 ,13) #有没有只能通过穷举的方法反推输入的函数呢
        self.waiting(0, 20) #（空闲）

        rectangle_up = Rectangle(height = 8, width = 16, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        rectangle_inner = Rectangle(height = 7.8, width = 16, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        rectangle_up.add(rectangle_inner).shift(9*DOWN)

        self.add(rectangle_up, notice4).play(ApplyMethod(rectangle_up.shift, 8.2*UP, run_time = 2, rate_func = double_bounce), ReplacementTransform(notice4, notice5))
        self.waiting(1+2-2, 15+12) # 嗯...... 很遗憾 人类到目前为止还不知道

        text_NP = MTex("\mathbf{NP}", color = PURPLE).scale(2).shift(5.5*LEFT)
        text_BPP = MTex("\mathbf{BPP}", color = PINK).scale(2).shift(5.5*RIGHT)
        label_NP = MTex("\mathbf{NP}", color = PURPLE).scale(0.6)
        label_BPP = MTex("\mathbf{BPP}", color = PINK).scale(0.6)
        text_unsolved = MTexText('?', color = YELLOW).scale(3).shift(2*UP)
        label_NP_1 = label_NP.copy().shift(UP + 3.9*LEFT)
        label_NP_2 = label_NP.copy().shift(DOWN + 1.3*LEFT)
        label_NP_3 = label_NP.copy().shift(UP + 2.7*RIGHT)
        label_BPP_1 = label_BPP.copy().shift(UP + 2.7*LEFT)
        label_BPP_2 = label_BPP.copy().shift(DOWN + 1.3*RIGHT)
        label_BPP_3 = label_BPP.copy().shift(UP + 3.9*RIGHT)
        circle_NP_1 = Circle(radius = 1.3, color = PURPLE, fill_opacity = 0.2).shift(UP + 3*LEFT)
        circle_NP_2 = Circle(radius = 1.3, color = PURPLE, fill_opacity = 0.2).shift(DOWN + 0.5*LEFT)
        circle_NP_3 = Circle(radius = 0.8, color = PURPLE, fill_opacity = 0.2).shift(UP + 2.7*RIGHT)
        circle_BPP_1 = Circle(radius = 0.8, color = PINK, fill_opacity = 0.2).shift(UP + 2.7*LEFT)
        circle_BPP_2 = Circle(radius = 1.3, color = PINK, fill_opacity = 0.2).shift(DOWN + 0.5*RIGHT)
        circle_BPP_3 = Circle(radius = 1.3, color = PINK, fill_opacity = 0.2).shift(UP + 3*RIGHT)
        self.play(FadeInFromPoint(text_NP, ORIGIN), FadeInFromPoint(text_BPP, ORIGIN))
        self.waiting(2, 21) #这涉及到一个和“P=NP？”相似的问题
        circles = [circle_NP_1, circle_BPP_1, circle_NP_2, circle_BPP_2, circle_NP_3, circle_BPP_3]
        labels = [label_NP_1, label_NP_2, label_NP_3, label_BPP_1, label_BPP_2, label_BPP_3]
        self.play(*[ShowCreation(mob) for mob in circles], *[FadeIn(mob) for mob in labels], Write(text_unsolved))
        self.waiting(1, 0) #NP包含于BPP吗？
        self.waiting(0, 17) #（空闲）

        indicate_1 = SurroundingRectangle(circle_NP_1)
        indicate_2 = SurroundingRectangle(VGroup(circle_NP_2, circle_BPP_2))
        config_oneway = RightArrow().scale(2, about_point = ORIGIN).add(MTex("m").shift(1.6*LEFT), MTex("c", color = YELLOW_E).shift(1.6*RIGHT)).shift(4*LEFT)
        self.play(ShowCreation(indicate_1), ShowCreation(indicate_2))
        self.waiting(0, 28) #如果答案是否定的
        self.play(*[FadeOut(mob, 6*RIGHT) for mob in [text_NP, text_BPP, *circles, *labels, indicate_1, indicate_2, text_unsolved]], FadeIn(config_oneway, 6*RIGHT))
        self.waiting(1, 21) #我们就肯定能找到这样的函数
        self.waiting(3, 16) #当然 这样的函数看起来很可能存在

        title_oneway_1 = Text("单向函数", font = "simsun", color = YELLOW).shift(2*UP)
        self.play(Write(title_oneway_1))
        self.waiting(2, 16) #人们为这种函数 起了一个叫“单向函数”的名字
        self.waiting(0, 19) #（空闲）
        rsa = MTexText(r"随机抽取素数$p, q$, 记$N=pq$\\ 随机抽取与$\phi(N)$互素的$e$\\ 记$d\equiv e^{-1}\pmod{\phi(N)}$\\ 则有对应的加密方案：\\私钥：$p, q, d$\\ 公钥：$N, e$\\ 加密：$c\equiv m^e \pmod N$\\ 解密：$m\equiv c^d \pmod N$", alignment="", isolate = [r"加密：$c\equiv m^e \pmod N$"]).scale(0.8).shift(0.5*DOWN + 3*RIGHT)
        indicate_1 = SurroundingRectangle(rsa.get_part_by_tex(r"加密：$c\equiv m^e \pmod N$"))
        self.play(FadeIn(rsa, 0.5*UP))
        self.play(ShowCreation(indicate_1))
        self.waiting(0, 10) #RSA算法中加密的步骤
        self.waiting(2, 6) #就很可能是一种单向函数
        self.waiting(0, 25) #（空闲）

        oneway_blocks = []
        block_per_layer = [2, 3, 4, 4, 4, 4, 3, 2]
        order = 0
        for i in range(8):
            number = block_per_layer[i]
            for j in range(number):
                position = 0.6*UP*(i-3.5) + 1.2*RIGHT*(j-(number-1)/2)
                number_i = MTex(str(order), color = BLUE_D).scale(0.7)
                block_i =  RightArrow().add(number_i).shift(position)
                oneway_blocks.append(block_i)
                order += 1
        self.remove(indicate_cypher, indicate_message, *links_6_1, *links_6_2, *blocks, indicate)
        self.bring_to_back(arrow, shade, *oneway_blocks)
        title_trapdoor = MTexText("暗门单向函数", isolate = ["暗门", "单向函数"], tex_to_color_map = {"暗门": GREEN, "单向函数": BLUE}).scale(0.8).shift(3.5*UP)
        trapdoor_1 = title_trapdoor.get_part_by_tex("暗门")
        trapdoor_2 = title_trapdoor.get_part_by_tex("单向函数")
        title_oneway = trapdoor_2.copy().set_color(YELLOW).set_x(0)
        self.bring_to_back(title_oneway).play(*[mob.animate.shift(8.2*DOWN) for mob in [rectangle_up, title_oneway_1, config_oneway, rsa, indicate_1]], ReplacementTransform(notice5, notice6), FadeIn(title_oneway))
        self.waiting(2, 14) #但一般的单向函数还不能满足我们的需求
        self.play(ShowCreation(indicate), *[mob.animate.fade(0.8) for mob in [*oneway_blocks[0:11], *oneway_blocks[12:26]]])
        self.waiting(2, 12) #如果我们选择了一个单向函数当加密算法
        
        links_1_1, anims_1_1, tearing_1_1 = message_get_need(messages[0], oneway_blocks[11], RED_A)
        links_1_2, anims_1_2, tearing_1_2 = cypher_get_need(cyphers[5], oneway_blocks[11], RED_A)
        self.add(*links_1_1, oneway_blocks[11], indicate).play(*anims_1_1)
        self.add(*links_1_2, oneway_blocks[11], indicate).play(*anims_1_2)
        self.waiting(0, 15)

        for mob in [*links_1_1, *links_1_2]:
            mob.reverse_points()
        links_2_1, anims_2_1, _ = cypher_get_need(cyphers[3], oneway_blocks[11], ORANGE_A, True)
        cross = VMobject(color = RED, stroke_width = 10).set_points([0.3*UR, ORIGIN, 0.3*DL, 0.3*UL, ORIGIN, 0.3*DR]).move_to(oneway_blocks[11].get_corner(LEFT)).save_state()
        alpha = ValueTracker(0.0)
        cross.add_updater(warning_updater)
        self.add(*links_2_1, oneway_blocks[11], indicate).play(*tearing_1_1, *anims_2_1)
        self.add(cross).play(*tearing_1_2, ApplyMethod(alpha.set_value, 0.5, rate_func = linear, run_time = 0.5))
        cross.clear_updaters()
        self.play(*[FadeOut(mob) for mob in [cross, *links_2_1]], run_time = 0.5)
        self.waiting(0, 8) #想解密 就只能靠穷举了

        position = 0.3*DOWN + 0.6*RIGHT
        tip = LeftTip().shift(position)
        self.play(ShowCreation(tip))
        self.waiting(1, 8) #而如果有方便的解密算法
        links_2_1, anims_2_1, _ = cypher_get_need(cyphers[3], blocks[11], ORANGE_A, True)
        links_2_2, anims_2_2, _ = message_get_need(messages[5], blocks[11], ORANGE_A, True)
        self.add(*links_2_1, oneway_blocks[11], indicate, tip).play(*anims_2_1)
        self.add(*links_2_2, oneway_blocks[11], indicate, tip).play(*anims_2_2)
        self.waiting(1, 8) #能不靠穷举反推输入
        line = Line(title_oneway.get_corner(LEFT)+0.2*LEFT, title_oneway.get_corner(RIGHT)+0.2*RIGHT, color = RED)
        self.play(ShowCreation(line))
        self.waiting(1, 8) #那这又不可能是单向函数了
        self.waiting(0, 17) #（空闲）

        self.play(ReplacementTransform(notice6, notice7), *[FadeOut(mob) for mob in [*links_2_1, *links_2_2, line]])
        self.waiting(2, 11) #但没关系 我们可以再退一步
        
        tips = []
        all_colors = [RED, ORANGE, YELLOW, TEAL, BLUE, PURPLE, GREY, MAROON]
        random.shuffle(all_colors)
        all_colors = [*all_colors[0:4], GREEN, *all_colors[4:8]]
        for i in range(9):
            if i == 4:
                tips.append(tip.save_state())
            else:
                color = all_colors[i]
                fill = interpolate_color("#333333", color, 0.2)
                tip_i = LeftTip(fill_color = fill, stroke_color = color).shift(position + 0.6*(i-4)*DOWN).save_state()
                tips.append(tip_i)
        alpha = ValueTracker(0.0)
        beta = ValueTracker(0.1)
        def rolling_updater(mob: VMobject):
            offset = alpha.get_value()
            interval = beta.get_value()
            mob.restore().shift(offset * UP)
            distance = abs(mob.get_center()[1] - position[1])
            opacity = clip(distance/interval, 0, 1)
            mob.fade(smooth(opacity))
        for mob in tips:
            mob.add_updater(rolling_updater)
        self.add(*tips).play(alpha.animate.set_value(-0.6), beta.animate.set_value(0.7), run_time = 1)
        self.wait(0.5)
        self.play(alpha.animate.set_value(1.2), beta.animate.set_value(1.3), run_time = 1.5)
        self.wait(0.5)
        self.play(alpha.animate.set_value(-1.2), run_time = 2.5)
        self.wait(0.5)
        self.play(alpha.animate.set_value(0), run_time = 1.5)
        for mob in tips:
            mob.clear_updaters()
        self.waiting(2+2+2+2-8, 15+17+12+1) #有方便的解密算法没问题 只要它足够不好找就行了 找解密方法也要穷举的话 那还不如直接穷举输入
        self.play(*[FadeOut(mob) for mob in tips[0:4]+tips[5:8]])
        self.waiting(0, 20) #可能还能更快一些
        self.waiting(0, 14) #（空闲）

        self.waiting(2, 9) #这样不容易发现的解密算法
        copy_trapdoor_1 = trapdoor_1.copy().set_x(0)
        shade_copy = BackgroundRectangle(title_oneway, fill_opacity = 1)
        shade = BackgroundRectangle(trapdoor_2, fill_opacity = 1)
        self.bring_to_back(copy_trapdoor_1, shade_copy).play(Transform(title_oneway, trapdoor_2), Transform(shade_copy, shade), Transform(copy_trapdoor_1, trapdoor_1))
        self.waiting(1, 0) #就叫做单向函数的暗门
        self.waiting(1, 13) #到此共108秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_3(Scene):

    def construct(self):

        notice7 = Notice("转换思路", "请　模仿")
        notice8 = Notice("完善思路", "请　模仿")
        notice9 = Notice("对比学习", "请　模仿")

        oneway_blocks = []
        block_per_layer = [2, 3, 4, 4, 4, 4, 3, 2]
        order = 0
        for i in range(8):
            number = block_per_layer[i]
            for j in range(number):
                position = 0.6*UP*(i-3.5) + 1.2*RIGHT*(j-(number-1)/2)
                number_i = MTex(str(order), color = BLUE_D).scale(0.7)
                block_i =  RightArrow().add(number_i).shift(position)
                if order == 11:
                    block_i.fade(0.2)
                else:
                    block_i.fade(0.8)
                oneway_blocks.append(block_i)
                order += 1

        title_public_scheme = Text("公钥加密方案", font = "simsun").shift(2.8*UP)
        public_1 = VGroup(*title_public_scheme.submobjects[0:2]).set_color(GREEN)
        public_2 = VGroup(*title_public_scheme.submobjects[2:6]).set_color(BLUE)
        shade_1 = BackgroundRectangle(public_2).set_opacity(1)
        title_public = public_1.copy().set_x(0)
        title_scheme = public_2.copy().set_x(0)
        shade_2 = BackgroundRectangle(title_scheme).set_opacity(1)
        title_message = Text("明文", font = "simsun", color = WHITE).shift(2.8*UP + 4*LEFT)
        title_cypher = Text("密文", font = "simsun", color = YELLOW_E).shift(2.8*UP + 4*RIGHT)
        title_trapdoor = MTexText("暗门单向函数", isolate = ["暗门", "单向函数"], tex_to_color_map = {"暗门": GREEN, "单向函数": BLUE}).scale(0.8).shift(3.5*UP)
        shade = Square(side_length = 4.8, fill_opacity = 1, stroke_width = 0, fill_color = "#333333")
        arrow = Arrow(3.5*LEFT, 3.5*RIGHT, color = BLUE, stroke_width = 10, buff = 0)
        
        text_messages = ["01010011", "01001000", "01001111", "01010101", "01000011", "01000001", "01001110", "01000111"]
        messages = [MTex(text_messages[i]).scale(0.8).shift(4.5*LEFT + (i-3.5)*0.5*DOWN) for i in range(8)]
        cyphers = [MTex(str(random.randint(100000, 999999)), color = YELLOW_E).scale(0.8).shift(4.5*RIGHT + (i-3.5)*0.5*DOWN) for i in range(8)]

        tip = LeftTip().shift(0.3*DOWN + 0.6*RIGHT).fade(0.2)
        copy_block = oneway_blocks[11].copy().set_opacity(1)
        copy_tip = tip.copy().set_opacity(1)
        indicate = SurroundingRectangle(VGroup(copy_tip, copy_block))
        self.add(notice7, arrow, shade, *oneway_blocks, title_scheme, title_message, title_cypher, title_trapdoor, *messages, *cyphers, indicate, copy_block, tip, copy_tip)
        self.play(copy_tip.animate.move_to(3*LEFT), FadeOut(arrow), ReplacementTransform(notice7, notice8))
        self.waiting(1, 4) #将暗门留在自己手里
        self.play(copy_block.animate.move_to(3*RIGHT))
        self.waiting(1, 7) #把单向函数公开出去
        self.bring_to_back(title_public, shade_2).play(Transform(title_public, public_1), Transform(title_scheme, public_2), Transform(shade_2, shade_1))
        self.remove(title_public, title_scheme, shade, shade_2).add(title_public_scheme)
        self.waiting(1, 15) #这样就形成了一个公钥加密方案
        self.waiting(0, 17) #（空闲）

        public_key = Text("公钥", font = "simsun", color = BLUE).scale(0.7).shift(3*RIGHT + 0.6*UP)
        private_key = Text("私钥", font = "simsun", color = GREEN).scale(0.7).shift(3*LEFT + 0.6*UP)
        self.waiting(1, 21) #单向函数和暗门
        self.play(Write(public_key), Write(private_key))
        self.waiting(1, 6) #分别就是公钥和私钥
        self.waiting(0, 15) #（空闲）

        public_mobs = [*oneway_blocks, title_public_scheme, title_message, title_cypher, title_trapdoor, *messages, *cyphers, indicate, copy_block, tip, copy_tip, public_key, private_key]
        public_all = VGroup(*public_mobs)
        

        title_scheme = Text("加密方案", font = "simsun", color = BLUE).shift(2.8*UP)
        title_message = Text("明文", font = "simsun", color = WHITE).shift(2.8*UP + 4*LEFT)
        title_cypher = Text("密文", font = "simsun", color = YELLOW_E).shift(2.8*UP + 4*RIGHT)
        blocks = []
        block_per_layer = [2, 3, 4, 4, 4, 4, 3, 2]
        order = 0
        for i in range(8):
            number = block_per_layer[i]
            for j in range(number):
                position = 0.6*UP*(i-3.5) + 1.2*RIGHT*(j-(number-1)/2)
                number_i = MTex(str(order), color = BLUE_D).scale(0.7)
                block_i =  DoubleArrow().add(number_i).shift(position).save_state()
                blocks.append(block_i)
                order += 1
        mob_letters = MTexText("abcdefghijklmnopqrstuvwxyz").scale(0.9)
        for i in range(26):
            row = i // 4
            col = i % 4
            mob_letters[i].set_x(0).shift(0.6*DOWN*(row-3) + 0.6*RIGHT*(col-1.5))
        mob_message = mob_letters.copy().shift(4*LEFT)
        mob_cypher = mob_letters.copy().set_color(YELLOW_E).shift(4*RIGHT)
        private_mobs = [title_scheme, title_message, title_cypher, *blocks, mob_message, mob_cypher]
        private_all = VGroup(*private_mobs).shift(128/9*LEFT)
        dividing_line = Line(64/9*LEFT+3*UP, 64/9*LEFT+3*DOWN)
        self.remove(*public_mobs).add(public_all, private_all)

        self.play(ReplacementTransform(notice8, notice9))
        self.waiting(1, 7) #可能在看这期视频之前
        self.play(public_all.animate.scale(0.5, about_point = 64/9*RIGHT), private_all.animate.scale(0.5, about_point = 64/9*RIGHT), dividing_line.animate.shift(64/9*RIGHT))
        self.waiting(2, 3) #大家对于公钥加密和私钥加密的看法

        feature_1 = Text("公钥可以传递？", color = GREEN, font = "simsun").scale(0.8).shift(32/9*RIGHT + 3.2*UP)
        feature_2 = Text("不对称？", color = GREEN, font = "simsun").scale(0.8).shift(32/9*RIGHT + 2.5*UP)
        self.play(Write(feature_2))
        self.waiting(1, 12) #主要在于公钥加密不对称
        self.play(Write(feature_1))
        self.waiting(1, 10) #可以胜任大规模通讯的场合
        self.waiting(0, 18) #（空闲）

        self.waiting(2, 21) #但在分别了解了它们的原理之后
        self.play(*[mob.animate.scale(2, about_point = 64/9*LEFT) for mob in [public_all, private_all, feature_1, feature_2]], dividing_line.animate.shift(64/9*RIGHT))
        self.remove(feature_1, feature_2, dividing_line)
        self.waiting(2, 1) #大家对这个问题或许会有一些新的认识
        self.waiting(0, 18) #（空闲）

        indicate = Square(side_length = 4.8, color = YELLOW)
        indicate_1 = SurroundingRectangle(blocks[18])
        indicate_2 = SurroundingRectangle(blocks[11])
        indicate_3 = SurroundingRectangle(blocks[23])
        self.play(ShowCreation(indicate), run_time = 1)
        self.waiting(1, 0)
        self.play(TransformFromCopy(indicate, indicate_1), *[mob.animate.fade() for mob in blocks[0:18]+blocks[19:26]])
        self.waiting(1, 0)
        self.play(Transform(indicate_1, indicate_2), blocks[18].animate.fade(), blocks[11].animate.set_opacity(1))
        self.waiting(1, 0)
        self.play(Transform(indicate_1, indicate_3), blocks[11].animate.fade(), blocks[23].animate.set_opacity(1))
        self.waiting(3+4-7, 7+13) #私钥加密最重要的保密手段就是密钥 绝对的安全 建立在每次加密时 对密钥的随机抽取上
        self.waiting(0, 13) #（空闲）

        self.play(*[mob.animate.shift(128/9*LEFT) for mob in [public_all, private_all, indicate, indicate_1, dividing_line]])
        self.remove(private_all, indicate, indicate_1, dividing_line)
        self.waiting(0, 9) #而公钥加密
        self.play(ShowCreationThenDestructionAround(VGroup(copy_tip, private_key)), ShowCreationThenDestructionAround(VGroup(copy_block, public_key)), run_time = 2)
        self.waiting(0, 6) #却可以一对钥匙一直用
        self.waiting(1, 25) #它最重要的保密手段
        self.waiting(3, 2) #是人类还没有那么发达的算力和智力
        self.waiting(3, 10)
        self.play(*[FadeOut(mob) for mob in [public_all, notice9]])
        self.waiting(3, 10) #到此共53秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

######################################################################################################

class Summary(Scene):

    def construct(self):
        notice1 = Notice("良心视频", "请　三连")
        notice2 = Notice("下期预告", "敬请期待")
        notice3 = Notice("良心up主", "请　关注")

        self.play(Write(notice1))
        self.waiting(1, 11) #非常感谢大家能看到这里
        self.waiting(0, 10) #（空闲）

        cryptography = Text(" 现代\n密码学", font = "simhei").scale(0.8).shift(0.2*UP)
        hex_crypto = RegularPolygon(color = YELLOW_E, stroke_width = 10).scale(1.2).shift(0.2*UP)
        fields = ["加密系统", "伪随机性", "零知识\n 证明", "不可取分\n  混淆", "全同态\n 加密", "......"]
        modules = []
        for i in range(6):
            text_i = Text(fields[i], font = "simhei").scale(0.8).shift(0.2*UP)
            hex_i = hex_crypto.copy()
            module_i = VGroup(text_i, hex_i).shift(1.2*np.sqrt(3)*unit((i+0.5)*PI/3))
            modules.append(module_i)
        self.play(ShowCreation(hex_crypto))
        self.play(Write(cryptography))
        self.waiting(2, 10) #这一期我带领大家大体领略了一下现代密码学的风景
        self.waiting(4, 1) #现代密码学是一门内容丰富 发展迅速的学科
        self.waiting(1, 21) #除了视频中提到的
        self.play(LaggedStart(*[FadeIn(modules[i], -unit((i+0.5)*PI/3)) for i in range(6)]), lag_ratio = 0.5, run_time = 2)
        self.waiting(3, 13) #还有伪随机性 零知识证明 哈希函数等等很多有趣的话题
        self.waiting(0, 12) #（空闲）

        self.waiting(1, 28) #它们拥有共同的核心
        cover = Text("掩盖", font = "simhei", color = YELLOW_E).shift(3.6*unit(PI/3))
        obscure = Text("混淆", font = "simhei", color = YELLOW_E).shift(3.6*unit(2*PI/3))
        self.play(Write(cover), Write(obscure))
        self.waiting(1, 4) #如何在达成目标的时候
        self.waiting(1, 25) #不泄露任何额外信息
        self.waiting(0, 16) #（空闲）

        self.waiting(3, 0) #现在到处都能看到RSA算法的科普
        self.waiting(2, 17) #但这些有趣的内容却没有人讲
        self.waiting(1, 19) #不得不说有些遗憾
        self.waiting(0, 16) #（空闲）

        self.waiting(3, 19) #这期视频 就算是对这份遗憾的小小弥补
        self.waiting(0, 13) #（空闲）

        self.remove(*modules, cover, obscure, cryptography, hex_crypto)
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
        self.play(FadeInFromPoint(like1, 3*LEFT), FadeInFromPoint(coin1, np.array([0,0,0])), FadeInFromPoint(star1, 3*RIGHT))
        self.play(ApplyMethod(sanlian1.set_color, "#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian1])
        self.waiting(0, 4) #如果大家看了这期视频
        self.waiting(2, 16) #能有一些与别处不一样的收获
        self.waiting(2, 7) #那不妨一键三连支持一下
        self.waiting(0, 17) #（空闲）

        self.remove(sanlian1)

        len = ArcBetweenPoints(DOWN*2, UP*2, PI/6, color = GREEN, fill_opacity = 1, fill_color = average_color(GREEN, "#333333")).append_points(ArcBetweenPoints(UP*2, DOWN*2, PI/6).get_points())
        bench = Rectangle(width = 12, height = 0.2, fill_opacity = 1, fill_color = average_color(BLUE, "#333333")).add(*[Line(0.1*UP, 0.1*DOWN).shift((i-2)*2*RIGHT) for i in range(5)])
        shade_left = Rectangle(width = 8, height = 1, fill_opacity = 1, stroke_width = 0, fill_color = "#333333").shift(4*LEFT)
        shade_right = Rectangle(width = 8, height = 1, fill_opacity = 1, stroke_width = 0, fill_color = "#333333").shift(4*RIGHT)
        label_left_1 = MTex("f").scale(0.5).shift(2*LEFT+0.5*DOWN)
        label_right_1 = MTex("f").scale(0.5).shift(2*RIGHT+0.5*DOWN)
        label_left_2 = MTex("2f").scale(0.5).shift(4*LEFT+0.5*DOWN)
        label_right_2 = MTex("2f").scale(0.5).shift(4*RIGHT+0.5*DOWN)
        dot_center = Dot(color = YELLOW)
        dot_any = Dot(color = YELLOW).shift(3*LEFT + UP)
        line_1_1 = Line(3*LEFT + UP, UP, color = YELLOW)
        line_1_2 = Line(3*LEFT + UP, ORIGIN, color = YELLOW)
        line_1_3 = Line(3*LEFT + UP, 2*DOWN, color = YELLOW)
        intersection_1 = Dot(color = YELLOW).shift(UP)
        intersection_2 = Dot(color = YELLOW).shift(2*DOWN)
        line_2_1 = Line(UP, 6*RIGHT + 2*DOWN, color = YELLOW)
        line_2_2 = Line(ORIGIN, 6*RIGHT + 2*DOWN, color = YELLOW)
        line_2_3 = Line(2*DOWN, 6*RIGHT + 2*DOWN, color = YELLOW)
        image = Dot(color = YELLOW).shift(6*RIGHT + 2*DOWN)
        def line_1_1_updater(mob: Line):
            position = dot_any.get_center()
            other_end = np.array([0, position[1], 0])
            mob.put_start_and_end_on(position, other_end)
        def line_1_2_updater(mob: Line):
            position = dot_any.get_center()
            mob.put_start_and_end_on(position, ORIGIN)
        def line_1_3_updater(mob: Line):
            position = dot_any.get_center()
            other_end = np.array([0, 2*position[1]/(position[0]+2), 0])
            mob.put_start_and_end_on(position, other_end)
        def intersection_1_updater(mob: Dot):
            position = dot_any.get_center()
            mob_position = np.array([0, position[1], 0])
            mob.move_to(mob_position)
        def intersection_2_updater(mob: Dot):
            position = dot_any.get_center()
            mob_position = np.array([0, 2*position[1]/(position[0]+2), 0])
            mob.move_to(mob_position)
        def line_2_1_updater(mob: Line):
            position = dot_any.get_center()
            start = np.array([0, position[1], 0])
            end = 2/(position[0]+2)*position
            mob.put_start_and_end_on(start, end)
        def line_2_2_updater(mob: Line):
            position = dot_any.get_center()
            start = ORIGIN
            end = 2/(position[0]+2)*position
            mob.put_start_and_end_on(start, end)
        def line_2_3_updater(mob: Line):
            position = dot_any.get_center()
            start = np.array([0, 2*position[1]/(position[0]+2), 0])
            end = 2/(position[0]+2)*position
            mob.put_start_and_end_on(start, end)
        def image_updater(mob: Dot):
            position = dot_any.get_center()
            mob_position = 2/(position[0]+2)*position
            mob.move_to(mob_position)
        self.add(len).play(ReplacementTransform(notice1, notice2), ShowCreation(len))
        self.bring_to_back(bench, shade_left, shade_right).play(shade_left.animate.shift(8*LEFT), shade_right.animate.shift(8*RIGHT))
        self.remove(shade_left, shade_right)
        self.play(*[FadeIn(mob, 0.5*UP) for mob in [label_left_1, label_right_1, label_left_2, label_right_2]])
        self.play(ShowCreation(dot_center), ShowCreation(dot_any))
        self.play(ShowCreation(line_1_1), ShowCreation(line_1_2), ShowCreation(line_1_3), rate_func = rush_into)
        self.play(ShowCreation(intersection_1), ShowCreation(intersection_2), ShowCreation(line_2_1, rate_func = rush_from), ShowCreation(line_2_2, rate_func = rush_from), ShowCreation(line_2_3, rate_func = rush_from))
        self.play(ShowCreation(image))
        line_1_1.add_updater(line_1_1_updater)
        line_1_2.add_updater(line_1_2_updater)
        line_1_3.add_updater(line_1_3_updater)
        intersection_1.add_updater(intersection_1_updater)
        intersection_2.add_updater(intersection_2_updater)
        line_2_1.add_updater(line_2_1_updater)
        line_2_2.add_updater(line_2_2_updater)
        line_2_3.add_updater(line_2_3_updater)
        image.add_updater(image_updater)
        self.play(dot_any.animate.shift(LEFT))
        self.wait(1)
        self.play(dot_any.animate.move_to(3.2*LEFT))
        self.wait(1)
        trace_left = TracedPath(dot_any.get_center)
        trace_right = TracedPath(image.get_center)
        self.add(trace_left, trace_right).play(Rotate(dot_any, TAU, about_point = 4*LEFT), run_time = 2)
        trace_left.clear_updaters()
        trace_right.clear_updaters()
        self.wait(1)
        self.play(dot_any.animate.move_to(3*LEFT + UP))
        with_updater = [line_1_1, line_1_2, line_1_3, intersection_1, intersection_2, line_2_1, line_2_2, line_2_3, image]
        for mob in with_updater:
            mob.clear_updaters()
        self.bring_to_back(bench, shade_left, shade_right).play(shade_left.animate.shift(8*LEFT), shade_right.animate.shift(8*RIGHT))
        self.play(*[FadeOut(mob) for mob in [trace_left, trace_right, dot_any, dot_center, *with_updater, len, bench, label_left_1, label_right_1, label_left_2, label_right_2]])
        self.waiting(2+3+1+3+0 +1+2+1+0 -17, 20+16+21+7+13 +12+20+20+19) #下期视频是关于光学的话题 凸透镜的成像蕴藏着一幅相当美观的图像 但似乎这半年来 关注这一问题的人基本给出的都是计算方法 （空闲） 在下期视频 欢迎大家和我一起揭开计算的面纱  一睹美妙的真容
        
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
        anim1 = FadeIn(painting)
        anim1.update_config(lag_ratio = 0.01, run_time = 2)
        self.play(anim1, ReplacementTransform(notice2, notice3))
        self.waiting(0, 4) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(1, 13) #而我 就像我的名字一样

        self.play(FadeOut(painting_others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star0.shift, DOWN))
        self.waiting(1, 12) #想要把天上的星星垂下来

        star_copy = star0.copy()
        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star0, apple))
        self.waiting(1, 3) #变成触手可及的果实

        snowflake = SnowFlake()
        snowflake_2 = snowflake.copy().set_color(RED).set_stroke(width = 1.5)
        snowflake_3 = snowflake.copy().set_color(BLUE).set_stroke(width = 2)
        anims = LaggedStart(SpreadOut(snowflake_2).update_config(rate_func = linear), SpreadOut(snowflake_3).update_config(rate_func = linear), SpreadOut(snowflake).update_config(rate_func = linear), rate_func = rush_into, run_time = 2)
        self.play(Transform(star0, star_copy), anims)
        self.remove(snowflake_2, snowflake_3)
        self.waiting(2+0-2, 0+19) #变成指引前路的火光 （空闲）
        
        self.remove(star0, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(2, 9) #我是乐正垂星 我们下期视频再见

        self.waiting(5, 23)
        self.play(FadeOut(picture_photo), FadeOut(text_name), FadeOut(notice3))
        self.waiting(6) #到此共90秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

######################################################################################################

class Template(Scene):
    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)