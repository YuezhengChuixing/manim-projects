from base64 import b16decode
from contextlib import redirect_stdout
from manimlib import *
import numpy as np
import re

OMEGA = np.array([math.sqrt(3)/2, -1/2, 0])
colors = ["#0080FF", "#9999FF", "#00FFCC", "#66CCFF", "#EE82EE", "#006666", "#FFFF00"]
BLUE_P = interpolate_color(BLUE, PURPLE, 0.5)
BLUE_G = interpolate_color(BLUE, GREEN, 0.5)
RED_P = interpolate_color(RED, PURPLE, 0.5)
YELLOW_O = interpolate_color(ORANGE, YELLOW, 2/3)
YELLOW_G = interpolate_color(GREEN, YELLOW, 2/3)

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def scale_center(position, target, ratio):
    return position - (position - target) / (1 - ratio)

def dark(color, fade = 0.5):
    return interpolate_color(color, "#333333", fade)

def angle_color(angle):
    colors = [TEAL, BLUE, BLUE, TEAL, GREEN, GREEN]

    number_colors = len(colors)
    ratio = number_colors*angle/TAU
    index = int(ratio)
    interpolate = ratio - index

    return interpolate_color(colors[index%number_colors], colors[(index+1)%number_colors], interpolate)

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):

        super().__init__()
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

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

class Year(VGroup):
    def __init__(self, decimal):

        super().__init__()
        distance = 0.12
        self.one = Digit(decimal % 10).shift(3*distance*RIGHT)
        decimal = int(decimal / 10)
        self.ten = Digit(decimal % 10).shift(distance*RIGHT)
        decimal = int(decimal / 10)
        self.hundred = Digit(decimal % 10).shift(distance*LEFT)
        decimal = int(decimal / 10)
        self.thousand = Digit(decimal % 10).shift(3*distance*LEFT)
        self.add(self.one, self.ten, self.hundred, self.thousand)

    def set_year(self, year, opacity):
        self.one.set_number(year % 10, opacity)
        year = int(year / 10)
        self.ten.set_number(year % 10, opacity)
        year = int(year / 10)
        self.hundred.set_number(year % 10, opacity)
        year = int(year / 10)
        self.thousand.set_number(year % 10, opacity)

class Chip(VGroup):
    def __init__(self):

        super().__init__()
        lines = VGroup()
        for i in range (9):
            linei = Line(np.array([0, 0.15, 0]), np.array([0, -0.15, 0])).shift(0.5*(i-4)*UP)
            lines.add(linei)
        pins = VGroup()
        for i in range (8):
            pini = Rectangle(height = 0.2, width = 0.4).shift(0.5*(i-3.5)*UP)
            pins.add(pini)
        left_lines = lines.copy().shift(2.15*LEFT)
        right_lines = lines.copy().shift(2.15*RIGHT)
        left_pins = pins.copy().shift(2.3*LEFT)
        right_pins = pins.copy().shift(2.3*RIGHT)
        upper = Line(np.array([-2.15, 2.15, 0]), np.array([2.15, 2.15, 0]))
        lower = Line(np.array([-2.15, -2.15, 0]), np.array([2.15, -2.15, 0]))
        self.add(left_lines, right_lines, left_pins, right_pins, upper, lower)

class FullChip(Chip):
    def __init__(self):

        super().__init__()
        
        block1 = Block(True, 3, 4, "", colors[0], 0, 0)
        block2 = Block(True, 4, 2, "", colors[1], 3, 0)
        block3 = Block(True, 4, 3, "", colors[1], 3, 2)
        block4 = Block(True, 7, 14, "", colors[2], 9, 0)
        block5 = Block(True, 9, 11, "", colors[3], 0, 5)
        block6 = Block(True, 3, 1, "", colors[4], 0, 4)
        block7 = Block(True, 2, 1, "", colors[5], 7, 0)
        block8 = Block(True, 2, 1, "", colors[5], 7, 1)
        block9 = Block(True, 2, 1, "", colors[5], 7, 2)
        block10 = Block(True, 2, 1, "", colors[5], 7, 3)
        block11 = Block(True, 2, 1, "", colors[5], 7, 4)
        block12 = Block(True, 1, 2, "", colors[6], 9, 14)
        block13 = Block(True, 2, 2, "", colors[6], 10, 14)
        block14 = Block(True, 1, 2, "", colors[6], 12, 14)
        block15 = Block(True, 2, 2, "", colors[6], 13, 14)
        block16 = Block(True, 1, 2, "", colors[6], 15, 14)
        blocks = VGroup(block1, block6, block2, block3, block7, block8, block9, block10, block11, block5, block4, block12, block13, block14, block15, block16).shift(4*RIGHT)
        self.add(blocks)     

class SwallowIn(Homotopy):
    CONFIG = {
        "run_time": 2,
    }

    def __init__(self, mobject, target, **kwargs):
        digest_config(self, kwargs, locals())

        distance = max(np.linalg.norm(mobject.get_corner(UL)-target), np.linalg.norm(mobject.get_corner(UR)-target), np.linalg.norm(mobject.get_corner(DL)-target), np.linalg.norm(mobject.get_corner(DR)-target))
        
        def homotopy(x, y, z, t):
            position = np.array([x, y, z])
            vect = position - target
            length = np.linalg.norm(vect)
            move = t * distance
            if move >= length:
                return target
            else:
                ratio = 1 - move/length
                return target + np.array([ratio * vect[0], np.sqrt(ratio) * vect[1], ratio * vect[2]])

        super().__init__(homotopy, mobject, **kwargs)

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

class Grid(VGroup):
    def __init__(self, size, buff):

        super().__init__()
        height = size[0] * buff
        width = size[1] * buff

        line_x = VGroup()
        for i in range (size[0]+1):
            linei = Line(width/2 * LEFT, width/2 * RIGHT, stroke_width = 2).shift((i - size[0]/2) * buff * UP).insert_n_curves(17)
            line_x.add(linei)
        line_y = VGroup()
        for i in range (size[1]+1):
            linei = Line(height/2 * UP, height/2 * DOWN, stroke_width = 2).shift((i - size[0]/2) * buff * RIGHT).insert_n_curves(17)
            line_y.add(linei)
        self.add(line_x, line_y)

class Block(VGroup):
    def __init__(self, m_relative, m_width, m_height, m_name, m_color, m_coor_x = 0, m_coor_y = 0):

        super().__init__()
        if m_relative:
            height = m_height * 0.25 - 0.1
            width = m_width * 0.25 - 0.1
            position = 6*LEFT + 2*DOWN + (m_coor_x+m_width/2)*0.25*RIGHT + (m_coor_y+m_height/2)*0.25*UP
            text_scale = min(0.8, height)*1.25
        else:
            height = m_height
            width = m_width
            position = 3*RIGHT
            text_scale = 1

        self.block = Rectangle(height = height, width = width, color = m_color, fill_color = interpolate_color(m_color, "#333333", 0.5), fill_opacity = 0.8)
        self.name  = Tex(m_name, color = m_color).scale(text_scale)
        self.add(self.block, self.name)
        self.move_to(position)

class Series(VGroup):
    def __init__(self, m_symbol, m_start, m_length, m_step = 1):

        super().__init__()
        self.symbol = m_symbol
        self.start = m_start
        self.length = m_length
        self.term = []
        for i in range (self.length):
            termi = MTex(self.symbol + r"_{" + f"{i*m_step + self.start}" + r"}").scale(0.8).shift((i - (self.length-1)/2) * LEFT)
            self.term.append(termi)
            self.add(termi)

class LongMultiplication(VGroup):
    def __init__(self, m_mul_1 : Series, m_mul_2 : Series, m_target, m_bounded = False, h_space = 1.4, v_space = 0.7, m_colors = [BLUE, RED, YELLOW], result_offset = 0):

        if m_mul_1.length < m_mul_2.length:
            self.mul_1, self.mul_2 = m_mul_2, m_mul_1
        else:
            self.mul_1, self.mul_2 = m_mul_1, m_mul_2
        self.h_space = h_space
        self.v_space = v_space
        

        super().__init__(self.mul_1, self.mul_2)
        self.mul_1.set_color(m_colors[0])
        self.mul_2.set_color(m_colors[1])

        for i in range (self.mul_1.length):
            self.mul_1.term[i].next_to(self.h_space*i*LEFT + self.v_space*1*UP, UP+LEFT, buff = 0.2)
        for j in range (self.mul_2.length):
            self.mul_2.term[j].next_to(self.h_space*j*LEFT + self.v_space*0*UP, UP+LEFT, buff = 0.2)
        self.mul = MTex(r"\times").next_to(self.h_space*self.mul_1.length*LEFT + self.v_space*0*UP, UP+LEFT)
        self.add(self.mul)

        self.upper_line = Line(self.h_space*(self.mul_1.length+0.5)*LEFT, self.h_space*0.1*RIGHT)
        self.add(self.upper_line)

        self.input = VGroup(self.mul_1, self.mul_2, self.mul, self.upper_line)

        self.bounded = m_bounded
        if self.bounded:
            self.result = Series(m_target, self.mul_1.start + self.mul_2.start + self.mul_2.length - 1 + result_offset, self.mul_1.length - self.mul_2.length + 1).set_color(m_colors[2])    

            self.terms_mul_1 = []
            self.terms_mul_2 = []
            group_mul_1 = VGroup()
            group_mul_2 = VGroup()
            for j in range(self.mul_2.length):
                self.terms_mul_1.append([])
                self.terms_mul_2.append([])
                for i in range (self.result.length):
                    term2 = self.mul_2.term[j].copy().next_to(self.h_space*(i+self.mul_2.length-1)*LEFT + self.v_space*(j+1)*DOWN, UP+LEFT, buff = 0.2)
                    term1 = self.mul_1.term[i+self.mul_2.length-j-1].copy().next_to(term2.get_corner(DOWN+LEFT), UP+LEFT, buff = 0).shift(0.08*LEFT)
                    self.terms_mul_1[j].append(term1)
                    self.terms_mul_2[j].append(term2)
                    group_mul_1.add(term1)
                    group_mul_2.add(term2)
            self.add(group_mul_1, group_mul_2)

            self.lower_line = Line(self.h_space*(self.result.length+self.mul_2.length-0.8)*LEFT + self.v_space*self.mul_2.length*DOWN, self.h_space*(self.mul_2.length-1.1)*LEFT + self.v_space*self.mul_2.length*DOWN)
            self.add(self.lower_line)

            for k in range (self.result.length):
                self.result.term[k].next_to(self.h_space*(k+self.mul_2.length-1)*LEFT +self.v_space*(self.mul_2.length+1)*DOWN, UP+LEFT, buff = 0.2)
            self.add(self.result)

        else:
            self.result = Series(m_target, self.mul_1.start + self.mul_2.start + result_offset, self.mul_1.length + self.mul_2.length - 1).set_color(m_colors[2]) 

            self.terms_mul_1 = []
            self.terms_mul_2 = []
            group_mul_1 = VGroup()
            group_mul_2 = VGroup()
            for j in range(self.mul_2.length):
                self.terms_mul_1.append([])
                self.terms_mul_2.append([])
                for i in range (self.mul_1.length):
                    term2 = self.mul_2.term[j].copy().next_to(self.h_space*(i+j)*LEFT + self.v_space*(j+1)*DOWN, UP+LEFT, buff = 0.2)
                    term1 = self.mul_1.term[i].copy().next_to(term2.get_corner(DOWN+LEFT), UP+LEFT, buff = 0).shift(0.08*LEFT)
                    self.terms_mul_1[j].append(term1)
                    self.terms_mul_2[j].append(term2)
                    group_mul_1.add(term1)
                    group_mul_2.add(term2)
            self.add(group_mul_1, group_mul_2)
            self.calculation = VGroup(group_mul_1, group_mul_2)

            self.lower_line = Line(self.h_space*(self.result.length)*LEFT + self.v_space*self.mul_2.length*DOWN, self.h_space*0.1*RIGHT + self.v_space*self.mul_2.length*DOWN)
            self.add(self.lower_line)

            for k in range (self.result.length):
                self.result.term[k].next_to(self.h_space*k*LEFT +self.v_space*(self.mul_2.length+1)*DOWN, UP+LEFT, buff = 0.2)
            self.add(self.result)

        self.center()
    
    def get_duality(self):
        if self.bounded:
            self.terms_result = []
            group_result = VGroup()
            for j in range(self.mul_2.length):
                self.terms_result.append([])
                for i in range (self.result.length):
                    term = self.result.term[i].copy().next_to(self.terms_mul_2[j][i].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.08*RIGHT)
                    self.terms_result[j].append(term)
                    group_result.add(term)
        else:
            self.terms_result = []
            group_result = VGroup()
            for j in range(self.mul_2.length):
                self.terms_result.append([])
                for i in range (self.mul_1.length):
                    term = self.result.term[i+j].copy().next_to(self.terms_mul_2[j][i].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.08*RIGHT)
                    self.terms_result[j].append(term)
                    group_result.add(term)
        self.calculation.add(group_result)
        return group_result

    def get_polynomial(self):
        if self.bounded:
            return []
        else:
            poly_mul_1 = []
            for i in range (self.mul_1.length):
                if i == 0:
                    term = MTex(f"", color = PURPLE_A)
                elif i == 1:
                    term = MTex(f"x\ \ +", tex_to_color_map = {r"x": PURPLE_A})
                else:
                    term = MTex(f"x^{i}\ +", tex_to_color_map = {f"x^{i}": PURPLE_A})
                term.scale(0.8).next_to(self.mul_1.term[i].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0.03).shift(0.05*RIGHT)
                poly_mul_1.append(term)
            
            poly_mul_2 = []
            for j in range (self.mul_2.length):
                if j == 0:
                    term = MTex(f"", color = PURPLE_A)
                elif j == 1:
                    term = MTex(f"x\ \ +", tex_to_color_map = {r"x": PURPLE_A})
                else:
                    term = MTex(f"x^{j}\ +", tex_to_color_map = {f"x^{j}": PURPLE_A})
                term.scale(0.8).next_to(self.mul_2.term[j].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0.03).shift(0.05*RIGHT)
                poly_mul_2.append(term)

            poly_result = []
            for k in range (self.result.length):
                if k == 0:
                    term = MTex(f"", color = PURPLE_A)
                elif k == 1:
                    term = MTex(f"x\ \ +", tex_to_color_map = {r"x": PURPLE_A})
                else:
                    term = MTex(f"x^{k}\ +", tex_to_color_map = {f"x^{k}": PURPLE_A})
                term.scale(0.8).next_to(self.result.term[k].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0.03).shift(0.05*RIGHT)
                poly_result.append(term)

            polynomial_f = MTex(r"=\ f(x)", tex_to_color_map = {r"f(x)": interpolate_color(BLUE, PURPLE, 0.5)}).scale(0.8).next_to(self.mul_1.term[0].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.3*RIGHT+0.05*DOWN)
            polynomial_g = MTex(r"=\ g(x)", tex_to_color_map = {r"g(x)": interpolate_color(RED, PURPLE, 0.5)}).scale(0.8).next_to(self.mul_2.term[0].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.3*RIGHT+0.05*DOWN)
            polynomial_h = MTex(r"=\ h(x)", tex_to_color_map = {r"h(x)": ORANGE}).scale(0.8).next_to(self.result.term[0].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.3*RIGHT+0.05*DOWN)
            poly = [polynomial_f, polynomial_g, polynomial_h]

            self.add(*poly_mul_1, *poly_mul_2, *poly_result, *poly)
            
            return [poly_mul_1, poly_mul_2, poly_result, poly]

class DrawBorderWhileFill(AnimationGroup):
    # 本部分代码来自不愿意透露姓名的群友（群内ID：嘤）
    def __init__(self, vmob: VMobject, **kwargs):
        self.mainmob = vmob
        self.fill = vmob.copy().set_stroke(width=0)
        self.stroke = vmob.copy().set_fill(opacity=0)
        super().__init__(FadeIn(self.fill, rate_func = rush_into, **kwargs), ShowCreation(self.stroke, **kwargs))

    def clean_up_from_scene(self, scene: Scene) -> None:
        scene.remove(self.fill, self.stroke)
        scene.add(self.mainmob)

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

###############################################################################################

class Intro0(Scene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("数学家们喜欢给相同的东西起不同的名字，\n这样，一些好用的性质就会自己长出来。", font = 'simsun', t2c={"相同的东西": GREEN, "不同的名字": GREEN, "好用的性质": BLUE})
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
        notice1 = Notice("历史故事", "请听介绍")
        notice2 = Notice("最妙算法", "请　瞻仰")
        notice3 = Notice("历史故事", "请听介绍")
        notice4 = Notice("有 蜘 蛛", "啊啊啊啊")
        notice5 = Notice("硬件知识", "请记结论*")
        notice6 = Notice("历史故事", "请听介绍")
        notice7 = Notice("视频前言", "请听介绍")


        picture_winograd = ImageMobject("picture_winograd.jpg", height = 4).shift(2*LEFT + 0.5*UP)
        picture_cover_book = ImageMobject("picture_cover_book.jpg", height = 5).shift(2*RIGHT)
        text_winograd = Text("Shmuel Winograd", font = "Times New Roman").scale(0.5).next_to(picture_winograd, DOWN)
        life_winograd = Tex("1936.1.4 - 2019.3.25").scale(0.5).next_to(text_winograd, DOWN)
        group_winograd = VGroup(text_winograd, life_winograd)
        copy_winograd = group_winograd.copy().scale(0.5, about_point = scale_center(np.array([-2, 0.5, 0]), np.array([-2.7, -0.1, 0]), 0.5)).set_opacity(0)

        self.play(ReplacementTransform(notice0, notice1))
        self.waiting(0, 10) #1980年

        self.play(FadeIn(picture_winograd, UP), FadeIn(group_winograd, UP))
        self.waiting(0, 28) #Shmuel Winograd 在他编写的......
        self.play(FadeIn(picture_cover_book, UP))
        self.waiting(1, 8) #......《计算的算术复杂度》一书中
        self.waiting(2, 16) #提出了一种计算卷积的快速方法
        self.waiting(0, 24) #（空闲）

        time_axis = NumberLine(color = WHITE, x_range = [1950, 2030, 1], unit_size = 0.2, tick_size = 0.02, longer_tick_multiple = 5, tick_frequency = 0.2, numbers_with_elongated_ticks = np.linspace(1950, 2030, 17, endpoint = True))
        time_axis.shift(DOWN*1.7)
        group_axis = VGroup(time_axis)
        tip = Polygon(np.array([0.1, 0, 0]), np.array([-0.1, 0, 0]), np.array([0, -0.1, 0]), color = GREEN, fill_opacity = 1).shift(1.3*DOWN)

        tip1 = tip.copy().shift(2*LEFT)
        time1 = Year(1980).shift(2*LEFT+2.2*DOWN)
        group_axis.add(tip1, time1)
        anim1 = ApplyMethod(picture_winograd.scale, 0.5, 1e-8, scale_center(np.array([-2, 0.5, 0]), np.array([-2.7, -0.1, 0]), 0.5))
        anim2 = ApplyMethod(picture_cover_book.scale, 0.4, 1e-8, scale_center(np.array([2, 0, 0]), np.array([-1.3, -0.1, 0]), 0.4))
        self.play(anim1, anim2, Transform(group_winograd, copy_winograd), Write(time_axis), FadeIn(tip1, DOWN), FadeIn(time1, UP), run_time = 1)
        self.waiting(0, 13) #但在那时

        picture_cooley = ImageMobject("picture_cooley.jpg", height = 1.5).shift(5.7*LEFT)
        picture_tukey = ImageMobject("picture_tukey.jpg", height = 1.5).shift(4.3*LEFT)
        group_picture = Group(picture_winograd, picture_cover_book, picture_cooley, picture_tukey)
        text_cooley = Text("J.Cooley", font = "Times New Roman", stroke_width = 0.1).scale(0.5).next_to(picture_cooley, DOWN, buff = 0.1)
        text_tukey = Text("J.Tukey", font = "Times New Roman").scale(0.5).next_to(picture_tukey, DOWN, buff = 0.1)
        text_FFT = Text("快速傅立叶算法", font = 'Source Han Sans HW SC').scale(0.6).next_to(np.array([-5, 0.85, 0]), UP)
        word_FFT = Text("FFT", font = "Times New Roman").scale(0.6).next_to(text_FFT, UP)
        beams = VGroup()
        for i in range (11):
            beam_i = Line(np.array([-3.3, 0.5, 0]), np.array([-3, 0.5, 0])).rotate(((1+0.4*i)/6)*PI, about_point = np.array([-5, 0.5, 0]))
            beams.add(beam_i)
        group_name = Group(text_cooley, text_tukey, picture_cooley, picture_tukey)
        group_FFT = VGroup(text_FFT, word_FFT, beams).set_color("#FFD700")
        tip2 = tip.copy().shift(5*LEFT)
        time2 = Year(1965).shift(5*LEFT+2.2*DOWN)
        group_axis.add(tip2, time2)
        self.play(FadeIn(group_name, DOWN), FadeIn(tip2, DOWN), FadeIn(time2, UP))
        self.waiting(0, 9) #1965年提出的......
        self.play(FadeIn(group_FFT, UP), ReplacementTransform(notice1, notice2))
        self.waiting(0, 15)#......快速傅立叶算法

        slash_l = Line(np.array([-3.7, 0.5, 0]), np.array([-3.2, 0.5, 0])).rotate(2*PI/3, about_point = np.array([-5, 0.5, 0])).shift(UP)
        slash_r = Line(np.array([-3.7, 0.5, 0]), np.array([-3.2, 0.5, 0])).rotate(PI/3, about_point = np.array([-5, 0.5, 0])).shift(UP)
        text_1 = Text("卷积算法", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_1 = VGroup(text_1, slash_l.copy(), slash_r.copy()).set_color("#FFFF00").rotate(PI/24, about_point = np.array([-5, 0.5, 0]))
        text_2 = Text("智慧结晶", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_2 = VGroup(text_2, slash_l.copy(), slash_r.copy()).set_color("#66CCFF").rotate(-PI/12, about_point = np.array([-5, 0.5, 0]))
        text_3 = Text("美的化身", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_3 = VGroup(text_3, slash_l.copy(), slash_r.copy()).set_color("#00FFCC").rotate(-PI/3, about_point = np.array([-5, 0.5, 0]))
        text_4 = Text("人类之光", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_4 = VGroup(text_4, slash_l.copy(), slash_r.copy()).set_color("#9999FF").rotate(PI/6, about_point = np.array([-5, 0.5, 0]))
        text_5 = Text("最终答案", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_5 = VGroup(text_5, slash_l.copy(), slash_r.copy()).set_color("#0080FF").rotate(-5*PI/24, about_point = np.array([-5, 0.5, 0]))
        text_6 = Text("唯一真神", font = 'Source Han Sans HW SC').scale(0.5).shift(5*LEFT+2.9*UP)
        praise_6 = VGroup(text_6, slash_l.copy(), slash_r.copy()).set_color("#EE82EE").rotate(PI/24, about_point = np.array([-5, 0.5, 0]))

        self.play(FadeIn(praise_1, 0.5*unit(13*PI/24)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_1, 0.5*unit(13*PI/24)), FadeIn(praise_2, 0.5*unit(5*PI/12)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_2, 0.5*unit(5*PI/12)), FadeIn(praise_3, 0.5*unit(PI/6)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_3, 0.5*unit(PI/6)), FadeIn(praise_4, 0.5*unit(2*PI/3)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_4, 0.5*unit(2*PI/3)), FadeIn(praise_5, 0.5*unit(7*PI/24)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_5, 0.5*unit(7*PI/24)), FadeIn(praise_6, 0.5*unit(13*PI/24)), run_time = 0.6)
        self.waiting(0, 6)
        self.play(FadeOut(praise_6, 0.5*unit(13*PI/24)), run_time = 0.6)
        self.waiting(1+3+0-4.2, 25+2+23-36) #已经广为人知 Winograd提出的算法并没有受到广泛的关注 （空闲）

        tip3 = tip.copy().shift(0.6*LEFT)
        time3 = Year(1987).shift(4.4*RIGHT+2.2*DOWN)
        tip4 = tip.copy().shift(4.4*RIGHT)
        time4 = Year(2012).shift(4.4*RIGHT+2.2*DOWN)
        group_axis.add(tip4, time4)
        text_alex = Text("AlexNet", font = "Times New Roman").scale(0.6).next_to(tip4, UP)
        config_alex = Tex("\mathscr{A}").scale(3).move_to(np.array([4.4, 0, 0]))
        group_alex = VGroup(text_alex, config_alex)
        
        alpha = ValueTracker(0.0)
        def tip_updater(tip):
            a = alpha.get_value()
            ratio = smooth(min(a/2, 1))
            tip.set_opacity(ratio)
            tip.move_to(0.6*LEFT + 1.35*DOWN + 5*ratio*RIGHT)
        self.add(tip3)
        tip3.add_updater(tip_updater)
        def time_updater(time):
            a = alpha.get_value()
            ratio = smooth(min(a/2, 1))
            time.move_to(0.6*LEFT + 2.2*DOWN + 5*ratio*RIGHT)
            year = int(1987 + 25*ratio + 0.5)
            time.set_year(year, ratio)
        self.add(time3)
        time3.add_updater(time_updater)
        def text_updater(text):
            a = alpha.get_value() - 1.5
            ratio = smooth(max(a, 0))
            text.next_to(tip4, UP).shift((1-ratio) * UP)
            text.set_opacity(ratio)
        self.add(group_alex)
        group_alex.add_updater(text_updater)

        self.play(ReplacementTransform(notice2, notice3))
        self.play(alpha.animate.set_value(2.5), run_time = 2.5, rate_func = linear)
        tip3.remove_updater(tip_updater)
        time3.remove_updater(time_updater)
        group_alex.remove_updater(text_updater)
        self.add(tip4, time4)
        self.waiting(1+2-3.5, 15+6) #直到近些年 随着卷积神经网络的发展

        self.waiting(0, 9)
        alpha.set_value(0.0)
        def tip_updater2(tip):
            a = alpha.get_value()
            tip.set_opacity(1-a)
            tip.move_to(4.4*RIGHT + 1.35*DOWN + 5*a*RIGHT)
        tip3.add_updater(tip_updater2)
        def time_updater2(time):
            a = alpha.get_value()
            time.move_to(4.4*RIGHT + 2.2*DOWN + 5*a*RIGHT)
            year = int(2012 + 25*a + 0.5)
            time.set_year(year, 1-a)
        time3.add_updater(time_updater2)
        self.play(alpha.animate.set_value(1.0), run_time = 2)
        self.waiting(1+1-2, 11+4-9) #人们发现 快速傅立叶算法......
        self.play(ApplyMethod(group_FFT.set_color, WHITE))
        self.waiting(0, 13) #......并不总是那么好用
        self.waiting(0, 18) #（空闲）

        group_text = VGroup(group_FFT, text_cooley, text_tukey, text_alex)
        chip = Chip().shift(4*LEFT + 7*UP)
        string = Line(np.array([-4, 6, 0]), np.array([-4, 2.15, 0]), stroke_width = 1.5).shift(7*UP)

        self.add(chip, string)
        self.play(FadeOut(group_picture, DOWN), FadeOut(group_axis, DOWN), FadeOut(group_text, DOWN), ApplyMethod(chip.shift, DOWN*7), ApplyMethod(string.shift, DOWN*7), ReplacementTransform(notice3, notice4))
        self.play(ApplyMethod(string.put_start_and_end_on, np.array([-4, 2.15, 0]), np.array([-4, 2.15, 0])))
        self.waiting(0, 9) #尤其是在一些硬件工程师

        self.play(SwallowIn(config_alex, 4*LEFT))
        self.remove(config_alex)
        grid = Grid(np.array([16, 16]), 0.25).shift(4*LEFT).set_color(YELLOW).set_stroke(width = 1.5)
        grid2 = Grid(np.array([16, 16]), 0.25).shift(4*LEFT).set_color(GREY)
        self.add(grid)
        anims = LaggedStart(SpreadOut(grid).update_config(rate_func = linear), SpreadOut(grid2).update_config(rate_func = linear))
        self.play(anims, run_time = 2.5)
        self.remove(grid) 
        self.waiting(2+1-4.5, 26+21) #准备把神经网络放进芯片里的时候 （空闲）

        self.play(ReplacementTransform(notice4, notice5))
        self.waiting(1, 2) #专用于某一功能的芯片
        self.waiting(2, 12) #运算速度要比CPU快得多
        self.waiting(0, 20) #（空闲）
        
        block1 = Block(True, 3, 4, "", colors[0], 0, 0)
        block2 = Block(True, 4, 2, "", colors[1], 3, 0)
        block3 = Block(True, 4, 3, "", colors[1], 3, 2)
        block4 = Block(True, 7, 14, "", colors[2], 9, 0)
        block5 = Block(True, 9, 11, "", colors[3], 0, 5)
        block6 = Block(True, 3, 1, "", colors[4], 0, 4)
        block7 = Block(True, 2, 1, "", colors[5], 7, 0)
        block8 = Block(True, 2, 1, "", colors[5], 7, 1)
        block9 = Block(True, 2, 1, "", colors[5], 7, 2)
        block10 = Block(True, 2, 1, "", colors[5], 7, 3)
        block11 = Block(True, 2, 1, "", colors[5], 7, 4)
        block12 = Block(True, 1, 2, "", colors[6], 9, 14)
        block13 = Block(True, 2, 2, "", colors[6], 10, 14)
        block14 = Block(True, 1, 2, "", colors[6], 12, 14)
        block15 = Block(True, 2, 2, "", colors[6], 13, 14)
        block16 = Block(True, 1, 2, "", colors[6], 15, 14)
        blocks = VGroup(block1, block6, block2, block3, block7, block8, block9, block10, block11, block5, block4, block12, block13, block14, block15, block16)

        self.waiting(0, 22) #但是......
        self.play(FadeIn(blocks), lag_ratio = 0.02, run_time = 2)
        self.waiting(0, 12) #......在芯片上的每一种不同的运算
        self.play(FadeOut(blocks), lag_ratio = 0.02, run_time = 2)
        self.waiting(1+0-2, 28+27) # 都会占用一定的资源 （空闲）
        
        module1 = Block(True, 3, 4, "+", colors[0], 0, 0)
        module2 = Block(True, 4, 2, r"\times 0.5", colors[1], 3, 0)
        module3 = Block(True, 4, 3, r"\times 3", colors[1], 3, 2)
        module4 = Block(True, 7, 14, r"\times", colors[2], 9, 0)
        module5 = Block(True, 9, 11, r"\tilde{+}", colors[3], 0, 5)

        module6 = Block(False, 2.25, 3, "+", colors[0])
        input1 = Line(np.array([1.5, 1, 0]), np.array([1.875, 1, 0]), stroke_color = colors[0])
        input2 = Line(np.array([1.5, -1, 0]), np.array([1.875, -1, 0]), stroke_color = colors[0])
        output = Line(np.array([4.125, 0, 0]), np.array([4.5, 0, 0]), stroke_color = colors[0])
        in_text1 = Tex("x").next_to(input1, LEFT)
        in_text2 = Tex("y").next_to(input2, LEFT)
        out_text = Tex("x+y").next_to(output, RIGHT)
        module6_others = VGroup(input1, input2, output, in_text1, in_text2, out_text)
        self.play(FadeIn(module6, UP), FadeIn(module6_others, UP))
        self.waiting(0, 15)
        target = module6_others.copy().scale(1/3, about_point = scale_center(module6.get_center(), module1.get_center(), 1/3)).set_opacity(0)
        self.play(Transform(module6, module1), Transform(module6_others, target))
        self.waiting(0, 6) #加法是一种很简单的运算

        module7 = Block(False, 3, 1.5, r"\times 0.5", colors[1]).shift(1.5*DOWN)
        input = Line(np.array([1.125, -1.5, 0]), np.array([1.5, -1.5, 0]), stroke_color = colors[1])
        output = Line(np.array([4.5, -1.5, 0]), np.array([4.875, -1.5, 0]), stroke_color = colors[1])
        in_text = Tex("x").next_to(input, LEFT)
        out_text = Tex(r"\frac{x}{2}").next_to(output, RIGHT)
        module7_others = VGroup(input, output, in_text, out_text)

        module8 = Block(False, 3, 2.25, r"\times 3", colors[1]).shift(1*UP)
        input = Line(np.array([1.125, 1, 0]), np.array([1.5, 1, 0]), stroke_color = colors[1])
        output = Line(np.array([4.5, 1, 0]), np.array([4.875, 1, 0]), stroke_color = colors[1])
        in_text = Tex("x").next_to(input, LEFT)
        out_text = Tex("3x").next_to(output, RIGHT)
        module8_others = VGroup(input, output, in_text, out_text)

        self.play(FadeIn(module7, UP), FadeIn(module7_others, UP), FadeIn(module8, UP), FadeIn(module8_others, UP))
        self.waiting(0, 15)
        target = module7_others.copy().scale(1/3, about_point = scale_center(module7.get_center(), module2.get_center(), 1/3)).set_opacity(0)
        self.play(Transform(module7, module2), Transform(module7_others, target))
        target = module8_others.copy().scale(1/3, about_point = scale_center(module8.get_center(), module3.get_center(), 1/3)).set_opacity(0)
        self.play(Transform(module8, module3), Transform(module8_others, target))
        self.waiting(2+1+0-3.5, 12+1+23) #给一个输入乘以固定的倍数 也很简单 （空闲）

        module9 = Block(False, 1.75, 3.5, r"\times", colors[2])
        input1 = Line(np.array([1.75, 1, 0]), np.array([2.125, 1, 0]), stroke_color = colors[2])
        input2 = Line(np.array([1.75, -1, 0]), np.array([2.125, -1, 0]), stroke_color = colors[2])
        output = Line(np.array([3.875, 0, 0]), np.array([4.25, 0, 0]), stroke_color = colors[2])
        in_text1 = Tex("x").next_to(input1, LEFT)
        in_text2 = Tex("y").next_to(input2, LEFT)
        out_text = Tex("xy").next_to(output, RIGHT)
        module9_others = VGroup(input1, input2, output, in_text1, in_text2, out_text)
        self.play(FadeIn(module9, UP), FadeIn(module9_others, UP))
        self.waiting(0, 15)
        target = module9_others.copy().shift(module4.get_center() - module9.get_center()).set_opacity(0)
        self.play(Transform(module9, module4), Transform(module9_others, target))
        self.waiting(3-2.5, 10) #但是 把两个输入乘起来很困难
        self.waiting(0, 18) #（空闲）

        module10 = Block(False, 2.25, 2.75, r"\tilde{+}", colors[3])
        input1 = Line(np.array([1.5, 1, 0]), np.array([1.875, 1, 0]), stroke_color = colors[3])
        input2 = Line(np.array([1.5, -1, 0]), np.array([1.875, -1, 0]), stroke_color = colors[3])
        output = Line(np.array([4.125, 0, 0]), np.array([4.5, 0, 0]), stroke_color = colors[3])
        in_text1 = Tex(r"\tilde{x}").next_to(input1, LEFT)
        in_text2 = Tex(r"\tilde{y}").next_to(input2, LEFT)
        out_text = Tex(r"\tilde{x}+\tilde{y}").next_to(output, RIGHT)
        module10_others = VGroup(input1, input2, output, in_text1, in_text2, out_text)
        self.play(FadeIn(module10, UP), FadeIn(module10_others, UP))
        self.waiting(0, 15)
        target = module10_others.copy().shift(module5.get_center() - module10.get_center()).set_opacity(0)
        self.play(Transform(module10, module5), Transform(module10_others, target))
        self.waiting(2+1-2.5, 12+1) #浮点数的运算 也很困难 （空闲）
        
        modules = VGroup(module6, module7, module8, module9, module10)
        copy_FFT = group_FFT.copy().shift(8*RIGHT + 1.5*DOWN).set_color("#FFD700")
        self.play(FadeIn(copy_FFT, UP))
        self.waiting(1, 23) #快速傅立叶算法没有多少乘法
        self.play(ApplyMethod(copy_FFT.set_color, WHITE))
        self.waiting(2, 5) #但是它的所有运算都是浮点运算
        self.play(ApplyMethod(string.put_start_and_end_on, np.array([-4, 6, 0]), np.array([-4, 2.15, 0])), FadeOut(copy_FFT, DOWN))
        self.play(ApplyMethod(chip.shift, 7*UP), ApplyMethod(string.shift, 7*UP), ApplyMethod(modules.shift, 7*UP), ApplyMethod(grid2.shift, 7*UP), run_time = 2)
        self.waiting(2+1-3, 7+12) #基本和芯片缘分已尽了（空闲）

        group_refade = VGroup(tip1, tip2, time1, time2, time_axis, group_FFT, text_cooley, text_tukey)
        tip5 = tip.copy().shift(5.2*RIGHT)
        time5 = Year(2016).shift(5.2*RIGHT+2.2*DOWN)
        self.play(FadeIn(group_picture), FadeIn(group_refade), FadeIn(tip5, DOWN), FadeIn(time5, UP), ReplacementTransform(notice5, notice6))
        self.waiting(0, 15) #2016年

        picture_paper = ImageMobject("picture_paper.jpg", height = 3).shift(5.2*RIGHT + 0.4*UP)
        self.play(FadeIn(picture_paper, DOWN))
        self.waiting(2, 9) #一篇论文重新发现了Winograd算法
        self.waiting(3, 3) #并用它加速了卷积神经网络
        self.waiting(2, 24) #这一行为引起了广泛的效仿

        self.remove(group_picture, group_refade, tip5, time5, picture_paper)

        tex1 = Tex(r"c = a*b = S(P(a)\odot P(b))")
        tex2 = Tex(r"a*b = T(a, b, \hat{c})")
        tex3 = Tex(r"b\ \dot{*}\ c = T(\hat{a}, b, c)")
        tex4 = Tex(r"a = b\ \dot{*}\ c = P^{*}(P(b)\odot S^{*}(c))")
        self.play(Write(tex1), ReplacementTransform(notice6, notice7), run_time = 2)
        self.waiting(1, 0)
        self.play(Transform(tex1, tex2), run_time = 1)
        self.waiting(1, 0)
        self.play(Transform(tex1, tex3), run_time = 1)
        self.waiting(1, 0)
        self.play(Transform(tex1, tex4), run_time = 1)
        self.waiting(2+2+0+1+1-8, 11+3+28+21+9) #而这一算法背后的数学洞见 也逐渐回到人们的视野 （空闲） 我今天要带给大家的 就是这份洞见 
        self.waiting(0, 21) #（空闲）

        self.remove(tex1)

        like = Text("", font = 'vanfont')
        coin = Text("", font = 'vanfont')
        star = Text("", font = 'vanfont')
        like.shift(3*LEFT)
        star.shift(3*RIGHT)
        like.scale(2)
        coin.scale(2)
        star.scale(2)
        sanlian = VGroup(like, coin, star)
        sanlian.set_color("#00A1D6")
        self.play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, np.array([0,0,0])), FadeInFromPoint(star, 3*RIGHT), Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"))
        self.waiting(1+1-2,20+24) #长按点赞一键三连 我们开始吧
        self.waiting(3, 28)
        self.play(FadeOut(notice7), FadeOut(sanlian))
        self.waiting(4, 0)

        print(self.get_time())

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)
        
class Chapter1_0(Scene):

    def construct(self):

        ##  Making object
        text1 = Text("第一节　卷积与多项式乘法", font = 'simsun', t2c={"第一节": YELLOW, "卷积": GREEN, "多项式乘法": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(Scene):
    def construct(self):

        notice1 = Notice("基础知识", "请记笔记")
        notice2 = Notice("前情提要", "请　复习")
        notice3 = Notice("数学魔法", "请　验算")
        notice4 = Notice("奇思妙想", "请　模仿")

        text_convolution = Text("卷积", font = 'simsun', color = GREEN).shift(3.5*UP)
        title_line = Line(np.array([0,3,0]), np.array([0,3,0]))

        self.play(Write(notice1), FadeIn(text_convolution, DOWN), ApplyMethod(title_line.put_start_and_end_on, np.array([-6,3,0]), np.array([6,3,0]) ))
        self.waiting(0, 25) #我们这里说的卷积

        tex_continuous = MTex(r"(f*g)(x)=\int_{-\infty}^{\infty}f(t)g(x-t)\,dt")
        cross_line_1 = Line(np.array([-1,1,0]), np.array([-1,1,0]), color = RED)
        cross_line_2 = Line(np.array([1,1,0]), np.array([1,1,0]), color = RED)
        self.play(FadeIn(tex_continuous, DOWN))
        self.play(ApplyMethod(cross_line_1.put_start_and_end_on, np.array([-1,1,0]), np.array([1,-1,0])) , rate_func=rush_into, run_time = 0.5)
        self.play(ApplyMethod(cross_line_2.put_start_and_end_on, np.array([1,1,0]), np.array([-1,-1,0])) , rate_func=rush_from, run_time = 0.5)
        self.waiting(0, 2) #不是对两个函数的运算

        background = BackgroundRectangle(text_convolution, color = "#333333", fill_opacity = 1)
        text_discrete = Text("离散", font = 'simsun', color = GREEN).shift(3.5*UP)
        tex_discrete = MTex(r"(a*b)[n]=\sum_{t=-\infty}^{\infty}a[t]b[n-t]")
        group_title = VGroup(text_discrete, background, text_convolution, title_line)
        group_continuous = VGroup(tex_continuous, cross_line_1, cross_line_2)

        self.add(text_discrete, background)
        self.bring_to_back(text_discrete, background)
        anim1 = ApplyMethod(background.next_to, 3.5*UP, RIGHT, {"buff" : 0.02})
        anim2 = ApplyMethod(text_convolution.next_to, 3.5*UP, RIGHT, {"buff" : 0.02})
        anim3 = ApplyMethod(text_discrete.next_to, 3.5*UP, LEFT, {"buff" : 0.02})
        anim4 = FadeIn(tex_discrete, DOWN)
        anim5 = FadeOut(group_continuous, DOWN)
        self.play(anim1, anim2, anim3, anim4, anim5)
        self.waiting(1, 0)
        self.play(FadeOut(tex_discrete, DOWN))
        self.waiting(2+1-3, 20+0) #而是对两个向量的“离散卷积” （空闲）
        
        mtex_a = MTex(r"\vec{a} = \begin{bmatrix}a_0\\a_1\\a_2\end{bmatrix}", isolate = [r"="], tex_to_color_map={r"\vec{a}": BLUE, r"a_0": BLUE, r"a_1": BLUE, r"a_2": BLUE}).shift(1.5*UP+4.5*LEFT)
        mtex_b = MTex(r"\vec{b} = \begin{bmatrix}b_0\\b_1\end{bmatrix}", isolate = [r"="], tex_to_color_map={r"\vec{b}": RED, r"b_0": RED, r"b_1": RED}).shift(1.5*UP+1*LEFT)
        mtex_conv = MTex(r"\vec{a}*\vec{b}=\vec{c}=\begin{bmatrix}c_0\\c_1\\c_2\\c_3\end{bmatrix}", isolate = [r"="], tex_to_color_map={r"\vec{a}":BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW, r"c_0": YELLOW, r"c_1": YELLOW, r"c_2": YELLOW, r"c_3": YELLOW}).shift(1.5*UP+2.5*RIGHT)
        self.play(FadeIn(mtex_a, UP), FadeIn(mtex_b, UP), FadeIn(mtex_conv, UP))
        self.waiting(1, 24) #两个向量卷积成一个向量

        mtex_c0 = MTex(r"c_0=a_0b_0", tex_to_color_map={r"c_0": YELLOW, r"a_0": BLUE, r"b_0": RED}).next_to(2*LEFT, RIGHT)
        mtex_c1 = MTex(r"c_1=a_1b_0+a_0b_1", tex_to_color_map={r"c_1": YELLOW, r"a_1": BLUE, r"a_0": BLUE, r"b_1": RED, r"b_0": RED}).next_to(0.6*DOWN + 2*LEFT, RIGHT)
        mtex_c2 = MTex(r"c_2=a_2b_0+a_1b_1", tex_to_color_map={r"c_2": YELLOW, r"a_2": BLUE, r"a_1": BLUE, r"b_1": RED, r"b_0": RED}).next_to(1.2*DOWN + 2*LEFT, RIGHT)
        mtex_c3 = MTex(r"c_3=a_2b_1", tex_to_color_map={r"c_3": YELLOW, r"a_2": BLUE, r"b_1": RED}).next_to(1.8*DOWN + 2*LEFT, RIGHT)
        mtex_c = VGroup(mtex_c0, mtex_c1, mtex_c2, mtex_c3)
        self.play(Write(mtex_c), run_time = 4, lag_ratio = 1, rate_func = linear)
        self.waiting(1+4-4, 18+7) #新向量的每一项 是原来向量所有下标和相同的数 乘积的和
        self.waiting(1, 3) #（空闲）

        anims = [ShowCreationThenDestructionAround(mtex_a.get_part_by_tex(f"a_{i}")) for i in range(3)]
        self.play(LaggedStart(*anims), run_time = 1.5)
        self.waiting(0, 14) #a的长度是3
        anims = [ShowCreationThenDestructionAround(mtex_b.get_part_by_tex(f"b_{i}")) for i in range(2)]
        self.play(LaggedStart(*anims), run_time = 1.5)
        self.waiting(0, 13) #b的长度是2
        anims = [ShowCreationThenDestructionAround(mtex_conv.get_part_by_tex(f"c_{i}")) for i in range(4)]
        self.play(LaggedStart(*anims), run_time = 1.5)
        self.waiting(0, 3) #我们要计算c
        anim1 = ShowCreationThenDestructionAround(mtex_c0.get_part_by_tex(r"a_0b_0"))
        anim2 = ShowCreationThenDestructionAround(mtex_c1.get_part_by_tex(r"a_1b_0"))
        anim3 = ShowCreationThenDestructionAround(mtex_c1.get_part_by_tex(r"a_0b_1"))
        anim4 = ShowCreationThenDestructionAround(mtex_c2.get_part_by_tex(r"a_2b_0"))
        anim5 = ShowCreationThenDestructionAround(mtex_c2.get_part_by_tex(r"a_1b_1"))
        anim6 = ShowCreationThenDestructionAround(mtex_c3.get_part_by_tex(r"a_2b_1"))
        self.play(LaggedStart(anim1, anim2, anim3, anim4, anim5, anim6, lag_ratio = 0.02), run_time = 2)
        self.waiting(1+0-2, 29+26) #就一共要用6次乘法 （空闲）

        mtex_a_2 = MTex(r"\vec{a} = \begin{bmatrix}a_0\\a_1\\\vdots\\a_{m-1}\end{bmatrix}", isolate = [r"="], tex_to_color_map={r"\vec{a}": BLUE, r"a_0": BLUE, r"a_1": BLUE, r"\vdots": BLUE, r"a_{m-1}": BLUE}).shift(1.5*UP+4.5*LEFT).scale(0.8)
        mtex_b_2 = MTex(r"\vec{b} = \begin{bmatrix}b_0\\b_1\\\vdots\\b_{n-1}\end{bmatrix}", isolate = [r"="], tex_to_color_map={r"\vec{b}": RED, r"b_0": RED, r"b_1": RED, r"\vdots": RED, r"b_{n-1}": RED}).shift(1.5*UP+1*LEFT).scale(0.8)
        mtex_conv_2 = MTex(r"\vec{a}*\vec{b}=\vec{c}=\begin{bmatrix}c_0\\c_1\\\vdots\\c_{m+n-2}\end{bmatrix}", isolate = [r"="], tex_to_color_map={r"\vec{a}":BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW, r"c_0": YELLOW, r"c_1": YELLOW, r"\vdots": YELLOW, r"c_{m+n-2}": YELLOW}).shift(1.5*UP+2.5*RIGHT).scale(0.8)
        
        self.play(TransformMatchingStrings(mtex_a, mtex_a_2, key_map = {r"a_2": r"\vdots\\a_{m-1}"}), TransformMatchingStrings(mtex_b, mtex_b_2, key_map = {r"b_0": r"b_0\\b_1", r"b_1": r"\vdots\\b_{n-1}"}), TransformMatchingStrings(mtex_conv, mtex_conv_2, key_map = {r"c_2": r"\vdots", r"c_3": r"c_{m+n-2}"}), FadeOut(mtex_c, DOWN))
        self.waiting(0, 13) #一般地

        mtex_c0_2 = MTex(r"c_0=a_0b_0", tex_to_color_map={r"c_0": YELLOW, r"a_0": BLUE, r"b_0": RED}).scale(0.8).next_to(0.1*UP + 2*LEFT, RIGHT)
        mtex_c1_2 = MTex(r"c_1=a_1b_0+a_0b_1", tex_to_color_map={r"c_1": YELLOW, r"a_1": BLUE, r"a_0": BLUE, r"b_1": RED, r"b_0": RED}).scale(0.8).next_to(0.4*DOWN + 2*LEFT, RIGHT)
        mtex_c2_2 = MTex(r"c_2=a_2b_0+a_1b_1+a_0b_2", isolate = [r"="], tex_to_color_map={r"c_2": YELLOW, r"a_2": BLUE, r"a_1": BLUE, r"a_0": BLUE, r"b_2": RED, r"b_1": RED, r"b_0": RED}).scale(0.8).next_to(0.9*DOWN + 2*LEFT, RIGHT)
        mtex_c2_3 = mtex_c2_2.copy().shift(0.5*DOWN)
        mtex_c3_2 = MTex(r"\cdots = \cdots", isolate = [r"="]).scale(0.8)
        direction = mtex_c2_2.get_part_by_tex(r"=").get_center() - mtex_c3_2.get_part_by_tex(r"=").get_center()
        mtex_c3_2.shift(direction + 0.5*DOWN)
        mtex_c4_2 = MTex(r"c_{m+n-3}=a_{m-1}b_{n-2}+a_{m-2}b_{n-1}", isolate = [r"="], tex_to_color_map={r"c_{m+n-3}": YELLOW, r"a_{m-1}": BLUE, r"a_{m-2}": BLUE, r"b_{n-1}": RED, r"b_{n-2}": RED}).scale(0.8)
        direction = mtex_c3_2.get_part_by_tex(r"=").get_center() - mtex_c4_2.get_part_by_tex(r"=").get_center()
        mtex_c4_2.shift(direction + 0.5*DOWN)
        mtex_c5_2 = MTex(r"c_{m+n-2}=a_{m-1}b_{n-1}", isolate = [r"="], tex_to_color_map={r"c_{m+n-2}": YELLOW, r"a_{m-1}": BLUE, r"b_{n-1}": RED}).scale(0.8)
        direction = mtex_c4_2.get_part_by_tex(r"=").get_center() - mtex_c5_2.get_part_by_tex(r"=").get_center()
        mtex_c5_2.shift(direction + 0.5*DOWN)
        mtex_c_2 = VGroup(mtex_c0_2, mtex_c1_2, mtex_c2_2, mtex_c3_2, mtex_c4_2, mtex_c5_2)

        a_slices = [r"a_0", r"a_1", r"\vdots", r"a_{m-1}"]
        anims1 = LaggedStart(*[ShowCreationThenDestructionAround(mtex_a_2.get_part_by_tex(i)) for i in a_slices])
        b_slices = [r"b_0", r"b_1", r"\vdots", r"b_{n-1}"]
        anims2 = LaggedStart(*[ShowCreationThenDestructionAround(mtex_b_2.get_part_by_tex(i)) for i in b_slices])
        self.play(LaggedStart(anims1, anims2, run_time = 3, lag_ratio = 1), Write(mtex_c_2).update_config(run_time = 3, lag_ratio = 1, rate_func = linear))
        self.waiting(0, 14) #计算长为m和n的向量的卷积

        c_slices_0 = [mtex_c0_2.get_part_by_tex(r"a_0b_0")]
        c_slices_1 = [mtex_c1_2.get_part_by_tex(r"a_1b_0"), mtex_c1_2.get_part_by_tex(r"a_0b_1")]
        c_slices_2 = [mtex_c2_2.get_part_by_tex(r"a_2b_0"), mtex_c2_2.get_part_by_tex(r"a_1b_1"), mtex_c2_2.get_part_by_tex(r"a_0b_2")]
        c_slices_3 = [mtex_c2_3.get_part_by_tex(r"a_2b_0"), mtex_c2_3.get_part_by_tex(r"a_1b_1"), mtex_c2_3.get_part_by_tex(r"a_0b_2")]
        c_slices_4 = [mtex_c4_2.get_part_by_tex(r"a_{m-1}b_{n-2}"), mtex_c4_2.get_part_by_tex(r"a_{m-2}b_{n-1}")]
        c_slices_5 = [mtex_c5_2.get_part_by_tex(r"a_{m-1}b_{n-1}")]
        c_slices = [*c_slices_0, *c_slices_1, *c_slices_2, *c_slices_3, *c_slices_4, *c_slices_5]
        anims = [ShowCreationThenDestructionAround(mob) for mob in c_slices]
        self.play(LaggedStart(*anims, lag_ratio = 0.02), run_time = 2)
        self.waiting(0, 11) #就一共要用mn次乘法 
        self.waiting(1, 8) #（空闲）

        remove_group = VGroup(group_title, mtex_a_2, mtex_b_2, mtex_conv_2, mtex_c_2)
        self.remove(remove_group)

        chip = Chip().shift(4*LEFT)
        string = Line(np.array([-4, 6, 0]), np.array([-4, 2.15, 0]), stroke_width = 1.5)
        grid = Grid(np.array([16, 16]), 0.25).shift(4*LEFT).set_color(GREY)
        module1 = Block(True, 3, 4, "+", colors[0], 0, 0)
        module2 = Block(True, 4, 2, r"\times 0.5", colors[1], 3, 0)
        module3 = Block(True, 4, 3, r"\times 3", colors[1], 3, 2)
        module4 = Block(True, 7, 14, r"\times", colors[2], 9, 0)
        module5 = Block(True, 9, 11, r"\tilde{+}", colors[3], 0, 5)
        group_chip = VGroup(chip, string, grid, module1, module2, module3, module5).shift(7*UP)

        anim1 = ApplyMethod(group_chip.shift, DOWN*7)
        anim1.update_config(run_time = 1.5)
        self.play(anim1, ReplacementTransform(notice1, notice2))
        self.waiting(0, 10)#我们之前说过

        module9 = Block(False, 1.75, 3.5, r"\times", colors[2])
        input1 = Line(np.array([1.75, 1, 0]), np.array([2.125, 1, 0]), stroke_color = colors[2])
        input2 = Line(np.array([1.75, -1, 0]), np.array([2.125, -1, 0]), stroke_color = colors[2])
        output = Line(np.array([3.875, 0, 0]), np.array([4.25, 0, 0]), stroke_color = colors[2])
        in_text1 = Tex("x").next_to(input1, LEFT)
        in_text2 = Tex("y").next_to(input2, LEFT)
        out_text = Tex("xy").next_to(output, RIGHT)
        module9_others = VGroup(input1, input2, output, in_text1, in_text2, out_text)
        self.play(ApplyMethod(string.put_start_and_end_on, np.array([-4, 2.15, 0]), np.array([-4, 2.15, 0])), FadeIn(module9, UP), FadeIn(module9_others, UP))
        self.waiting(1, 1) #为两个输入做乘法
        target = module9_others.copy().shift(module4.get_center() - module9.get_center()).set_opacity(0)
        self.play(Transform(module9, module4), Transform(module9_others, target))
        self.waiting(0, 17) # 是很困难的事情
        self.waiting(0, 26) #（空闲）

        picture_winograd = ImageMobject("picture_winograd.jpg", height = 5).shift(2*RIGHT)
        self.play(FadeIn(picture_winograd, UP))
        self.waiting(2, 19) #Winograd想到了一个方法 来降低乘法的次数
        self.waiting(0, 29) #（空闲）

        self.remove(picture_winograd, module9, module9_others, group_chip)

        tex_string1 = r"\vec{f} = \begin{bmatrix}f_0\\f_1\\f_2\\f_3\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}a_0\\a_0+a_1+a_2\\a_0-a_1+a_2\\a_2\end{bmatrix}="
        tex_string3 = r"\begin{bmatrix}{1}&{0}&{0}\\{1}&{1}&{1}\\{1}&{-1}&{1}\\{0}&{0}&{1}\end{bmatrix}"
        tex_string4 = r"\begin{bmatrix}a_0\\a_1\\a_2\end{bmatrix}"

        mtex_f = MTex(
        tex_string1 + tex_string2 + tex_string3 + tex_string4, 
        tex_to_color_map = {r"\vec{f}": BLUE_P, re.compile(r"f_."): BLUE_P, (r"{1}", r"{0}", r"{-1}", r"+", r"-"): PURPLE, re.compile(r"a_."): BLUE}, 
        isolate = [tex_string1, tex_string2, tex_string3, tex_string4],
        ).scale(0.8).next_to(2*UP + 7*LEFT, RIGHT)
        
        mtex_f_short = MTex(
        tex_string1 + tex_string3 + tex_string4,
        tex_to_color_map = {r"\vec{f}": BLUE_P, re.compile(r"f_."): BLUE_P, (r"{1}", r"{0}", r"{-1}"): PURPLE, re.compile(r"a_."): BLUE},
        isolate = [tex_string1, tex_string3, tex_string4],
        ).scale(0.8).next_to(2*UP + 7*LEFT, RIGHT)
        
        mtex_f_a = mtex_f.get_part_by_tex(tex_string4)
        mtex_f_cal = mtex_f.get_part_by_tex(tex_string2 + tex_string3)
        mtex_f_others = mtex_f.get_part_by_tex(tex_string1)
        mtex_f_short_cal = mtex_f_short.get_part_by_tex(tex_string3)
        
        tex_string1 = r"\vec{g} = \begin{bmatrix}g_0\\g_1\\g_2\\g_3\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}b_0\\b_0+b_1\\b_0-b_1\\b_1\end{bmatrix}="
        tex_string3 = r"\begin{bmatrix}{1}&{0}\\{1}&{1}\\{1}&{-1}\\{0}&{1}\end{bmatrix}"
        tex_string4 = r"\begin{bmatrix}b_0\\b_1\end{bmatrix}"

        mtex_g = MTex(
        tex_string1 + tex_string2 + tex_string3 + tex_string4, 
        tex_to_color_map = {r"\vec{g}": RED_P, re.compile(r"g_."): RED_P, (r"{1}", r"{0}", r"{-1}", r"+", r"-"): PURPLE, re.compile(r"b_."): RED},
        isolate = [tex_string1, tex_string2, tex_string3, tex_string4],
        ).scale(0.8).next_to(1*DOWN + 7*LEFT, RIGHT)
        mtex_g_short = MTex(
        tex_string1 + tex_string3 + tex_string4,
        tex_to_color_map = {r"\vec{g}": RED_P, re.compile(r"g_."): RED_P, (r"{1}", r"{0}", r"{-1}"): PURPLE, re.compile(r"b_."): RED},
        isolate = [tex_string1, tex_string3, tex_string4],
        ).scale(0.8).next_to(1*DOWN + 7*LEFT, RIGHT)
        
        mtex_g_b = mtex_g.get_part_by_tex(tex_string4)
        mtex_g_cal = mtex_g.get_part_by_tex(tex_string2 + tex_string3)
        mtex_g_others = mtex_g.get_part_by_tex(tex_string1)
        mtex_g_short_cal = mtex_g_short.get_part_by_tex(tex_string3)
        
        tex_string1 = r"\vec{h} = \begin{bmatrix}h_0\\h_1\\h_2\\h_3\end{bmatrix} = "
        tex_string2 = r"\begin{bmatrix}f_0g_0\\f_1g_1\\f_2g_2\\f_3g_3\end{bmatrix} = \vec{f}\odot\vec{g}"
        mtex_h = MTex(
        tex_string1 + tex_string2,
        tex_to_color_map = {r"\vec{f}": BLUE_P, re.compile(r"f_."): BLUE_P, r"\vec{g}": RED_P, re.compile(r"g_."): RED_P, r"\vec{h}": ORANGE, re.compile(r"h_."): ORANGE},
        isolate = [tex_string1, tex_string2],
        ).scale(0.8).next_to(2*UP + LEFT, RIGHT)
        mtex_h_fg = mtex_h.get_part_by_tex(tex_string2)
        mtex_h_others = mtex_h.get_part_by_tex(tex_string1)

        tex_string1 = r"\vec{c} = \begin{bmatrix}c_0\\c_1\\c_2\\c_3\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}{1}&{0}&{0}&{0}\\{0}&{0.5}&{-0.5}&{-1}\\{-1}&{0.5}&{0.5}&{0}\\{0}&{0}&{0}&{1}\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}h_0\\h_1\\h_2\\h_3\end{bmatrix}"
        mtex_c = MTex(
        tex_string1 + tex_string2 + tex_string3,
        tex_to_color_map = {r"\vec{c}": YELLOW, re.compile(r"c_."): YELLOW, r"\vec{h}": ORANGE, re.compile(r"h_."): ORANGE, (r"{1}", r"{0}", r"{-1}", r"{0.5}", r"{-0.5}"): GREEN},
        isolate = [tex_string1, tex_string2, tex_string3],
        ).scale(0.8).next_to(1*DOWN + LEFT, RIGHT)
        mtex_c_h = mtex_c.get_part_by_tex(tex_string3)
        mtex_c_cal = mtex_c.get_part_by_tex(tex_string2)
        mtex_c_others = mtex_c.get_part_by_tex(tex_string1)

        self.play(ReplacementTransform(notice2, notice3))
        self.waiting(0, 4) #首先......
        self.play(FadeIn(mtex_f_a, LEFT))
        self.play(FadeIn(mtex_g_b, LEFT))
        self.waiting(0, 5) #通过a和b

        self.play(FadeIn(mtex_f_cal, RIGHT), FadeIn(mtex_g_cal, RIGHT))
        self.waiting(0, 19) #计算出两个新的向量
        self.play(FadeIn(mtex_f_others, RIGHT))
        self.play(FadeIn(mtex_g_others, RIGHT))
        self.waiting(0, 7) #f和g
        self.waiting(0, 27) #（空闲）
        
        self.play(TransformMatchingStrings(mtex_f, mtex_f_short), TransformMatchingStrings(mtex_g, mtex_g_short))
        self.waiting(0, 4) #接着......
        self.play(FadeIn(mtex_h_fg, LEFT))
        self.waiting(1, 22) #把f和g乘起来
        self.play(FadeIn(mtex_h_others, RIGHT))
        self.waiting(0, 1) #得到h
        self.waiting(0, 26) #（空闲）

        self.waiting(1, 3) #最后
        self.play(FadeIn(mtex_c_h, LEFT))
        self.waiting(0, 4) #通过h
        self.play(FadeIn(mtex_c_cal, RIGHT), FadeIn(mtex_c_others, RIGHT))
        self.waiting(0, 5) #计算出c
        self.waiting(1, 10) #（空闲）

        mtexs = [mtex_f_short_cal, mtex_g_short_cal, mtex_c_cal]
        anims = [ShowCreationThenDestructionAround(mtex) for mtex in mtexs]
        self.play(LaggedStart(*anims), run_time = 2)
        self.waiting(0, 17) #虽然加法和倍增增多了

        self.waiting(1, 0)
        anims = [ShowCreationThenDestructionAround(mtex_h.get_part_by_tex(f"f_{i}g_{i}")) for i in range(4)]
        self.play(LaggedStart(*anims), run_time = 2)
        self.waiting(0, 3) #但6次的乘法运算减少到了4次
        self.waiting(0, 25) #（空闲）

        self.waiting(2, 17) #Winograd是怎么给出这个式子的呢
        self.waiting(0, 21) #（空闲）

        self.remove(mtex_f_short, mtex_g_short, mtex_h, mtex_c)
        mtex_a = MTex(r"\vec{a} = \begin{bmatrix}a_0\\a_1\\a_2\end{bmatrix}", tex_to_color_map={(r"\vec{a}", re.compile(r"a_.")): BLUE}).scale(0.8).next_to(1*UP+6*LEFT, RIGHT)
        mtex_b = MTex(r"\vec{b} = \begin{bmatrix}b_0\\b_1\end{bmatrix}", tex_to_color_map={(r"\vec{b}", re.compile(r"b_.")): RED}).scale(0.8).next_to(1*DOWN+6*LEFT, RIGHT)
        mtex_conv = MTex(r"\vec{a}*\vec{b}=\vec{c}=\begin{bmatrix}c_0\\c_1\\c_2\\c_3\end{bmatrix} = \begin{bmatrix}a_0b_0\\a_1b_0+a_0b_1\\a_2b_0+a_1b_1\\a_2b_1\end{bmatrix}", tex_to_color_map={(r"\vec{a}", re.compile(r"a_.")): BLUE, (r"\vec{b}", re.compile(r"b_.")): RED, (r"\vec{c}", re.compile(r"c_.")): YELLOW}).scale(0.8).next_to(2.5*UP+3*LEFT, RIGHT)
        
        self.play(FadeIn(mtex_a, DOWN), FadeIn(mtex_b, DOWN), ReplacementTransform(notice3, notice4))
        self.play(Write(mtex_conv), lag_ratio = 1, run_time = 2)
        self.waiting(2+0-3, 18+26) #让我们先把目光转回到卷积上 （空闲）

        self.play(ApplyWave(mtex_conv), run_time = 1.5)
        self.waiting(0, 12) #除了直接套公式
        self.waiting(1, 22) #我们计算卷积时
        
        series_a = Series(r"a", 0, 3)
        series_b = Series(r"b", 0, 2)
        long_mul = LongMultiplication(series_a, series_b, r"c", False).shift(0*RIGHT + 0.5*DOWN)
        anims1 = [TransformFromCopy(mtex_a.get_part_by_tex(f"a_{i}"), long_mul.mul_1.term[i]) for i in range (3)]
        anims2 = [TransformFromCopy(mtex_b.get_part_by_tex(f"b_{i}"), long_mul.mul_2.term[i]) for i in range (2)]
        self.play(*anims1, *anims2)
        self.play(FadeIn(long_mul.upper_line, UP), FadeIn(long_mul.mul, UP))
        self.waiting(0, 5) #也可以列一个大竖式

        anims = []
        for j in range (2):
            for i in range (3):
                anim1 = TransformFromCopy(long_mul.mul_1.term[i], long_mul.terms_mul_1[j][i])
                anim2 = TransformFromCopy(long_mul.mul_2.term[j], long_mul.terms_mul_2[j][i])
                anim_group = AnimationGroup(anim1, anim2)
                anims.append(anim_group)
        self.play(LaggedStart(*anims, lag_ratio = 1), run_time = 6) #把对应的项写在对应的位置
        self.waiting(0, 10)
        self.play(ShowCreation(long_mul.lower_line))

        print(self.get_time())

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_2(Scene):
    def construct(self):

        notice4 = Notice("奇思妙想", "请　模仿")
        notice5 = Notice("常用结论", "请记笔记")
        notice6 = Notice("前情提要", "请看上期")
        notice7 = Notice("奇思妙想", "请　模仿")
        notice8 = Notice("地狱绘图", "请　验算")
        notice9 = Notice("推导完毕", "请　鼓掌")
    
        mtex_a = MTex(r"\vec{a} = \begin{bmatrix}a_0\\a_1\\a_2\end{bmatrix}", isolate = [r"="], tex_to_color_map={(r"\vec{a}", re.compile(r"a_.")): BLUE}).scale(0.8).next_to(1*UP+6*LEFT, RIGHT)
        mtex_b = MTex(r"\vec{b} = \begin{bmatrix}b_0\\b_1\end{bmatrix}", isolate = [r"="], tex_to_color_map={(r"\vec{b}", re.compile(r"b_.")): RED}).scale(0.8).next_to(1*DOWN+6*LEFT, RIGHT)
        tex_string_1 = r"\vec{a}*\vec{b}=\vec{c}"
        tex_string_2 = r"=\begin{bmatrix}c_0\\c_1\\c_2\\c_3\end{bmatrix} = \begin{bmatrix}a_0b_0\\a_1b_0+a_0b_1\\a_2b_0+a_1b_1\\a_2b_1\end{bmatrix}"
        mtex_conv = MTex(tex_string_1 + tex_string_2, isolate = [tex_string_1, tex_string_2, r"="], tex_to_color_map={(r"\vec{a}", re.compile(r"a_.")): BLUE, (r"\vec{b}", re.compile(r"b_.")): RED, (r"\vec{c}", re.compile(r"c_.")): YELLOW}).scale(0.8).next_to(2.5*UP+3*LEFT, RIGHT)
        series_a = Series(r"a", 0, 3)
        series_b = Series(r"b", 0, 2)
        long_mul = LongMultiplication(series_a, series_b, r"c", False).shift(0*RIGHT + 0.5*DOWN)
        
        self.add(notice4, mtex_a, mtex_b, mtex_conv, long_mul)
        self.remove(long_mul.result)
        self.play(FadeIn(long_mul.result, UP))
        self.waiting(0, 15) #这样也可以算出c
        self.waiting(0, 20) #（空闲）

        self.waiting(3, 12) #而且 这个看上去像乘法的竖式
        anims1 = [ShowCreationThenDestructionAround(long_mul.mul_1.term[i])  for i in range(3)]
        anims2 = [ShowCreationThenDestructionAround(long_mul.mul_2.term[j])  for j in range(2)]
        anims3 = [ShowCreationThenDestructionAround(long_mul.result.term[k]) for k in range(4)]
        self.play(LaggedStart(*anims1, *anims2, *anims3, lag_ratio = 0.02), run_time = 2)
        self.waiting(0, 23) #只要我们把向量看成系数

        long_mul_poly = long_mul.get_polynomial()
        poly_mul_1 = VGroup(long_mul.mul_1, *long_mul_poly[0], long_mul_poly[3][0])
        poly_mul_2 = VGroup(long_mul.mul_2, *long_mul_poly[1], long_mul_poly[3][1])
        poly_result = VGroup(long_mul.result, *long_mul_poly[2], long_mul_poly[3][2])

        anims1 = [FadeIn(mtex, 0.3*LEFT)  for mtex in long_mul_poly[0]]
        anims2 = [FadeIn(mtex, 0.3*LEFT)  for mtex in long_mul_poly[1]]
        anims3 = [FadeIn(mtex, 0.3*LEFT)  for mtex in long_mul_poly[2]]
        self.play(LaggedStart(*anims1, *anims2, *anims3, lag_ratio = 0.2), run_time = 2)
        self.waiting(0, 8) #为它们添加对应的项
        anims = [FadeIn(mtex, 0.3*LEFT) for mtex in long_mul_poly[3]]
        self.play(LaggedStart(*anims, lag_ratio = 0.5), run_time = 2)
        self.waiting(0, 3) #就真的是多项式的乘法
        self.waiting(1, 0) #（空闲）

        text_generating_function = Text("生成函数", font = 'simhei')
        text_generating_function.rotate(-PI/2).shift(5.3*RIGHT + 0.3*DOWN).set_color(GREEN)
        for i in range (4):
            text_generating_function[i].rotate(PI/2).shift(0.1*i*DOWN)
        width = text_generating_function.get_width()
        right_line = Line(text_generating_function.get_corner(UR) + 0.1*UR, text_generating_function.get_corner(DR) + 0.1*DR)
        text_generating_function.shift(width * RIGHT)
        background = BackgroundRectangle(text_generating_function, color = "#333333", fill_opacity = 1)

        self.waiting(1, 28) #向量对应的多项式
        self.waiting(1, 0)
        self.play(ShowCreation(right_line)) #称为这个向量的“母函数”......
        self.add(text_generating_function, background)
        self.bring_to_back(text_generating_function, background)
        self.play(ApplyMethod(text_generating_function.shift, width*LEFT), rate_func = rush_from, lag_ratio = 0.5, run_time = 1.6)
        self.waiting(0, 16) #......或者“生成函数”
        self.waiting(0, 22) #（空闲）

        mtex_conv_short = mtex_conv.get_part_by_tex(tex_string_1)
        copy_mtex_conv_short = mtex_conv_short.copy()
        mtex_conv_others = mtex_conv.get_part_by_tex(tex_string_2)
        text_vector = Text("向量", font = 'simhei', color = GREEN).scale(0.8).move_to(mtex_conv_short.get_center() + 2*LEFT + 0.8*UP)
        self.add(copy_mtex_conv_short)
        self.remove(mtex_conv_short)
        self.play(ApplyMethod(copy_mtex_conv_short.shift, 2*LEFT), FadeOut(VGroup(mtex_a, mtex_b, mtex_conv_others), 2*LEFT), FadeIn(text_vector, 2*LEFT), ReplacementTransform(notice4, notice5))
        self.waiting(1, 8) #对两个向量作卷积

        mtex_multi = MTex(r"f(x)g(x)=h(x)", tex_to_color_map = {r"f(x)": BLUE_P, r"g(x)": RED_P, r"h(x)": ORANGE}).scale(0.8).shift(2.5*UP)
        mtex_equiv = MTex(r"\Leftrightarrow").move_to( (copy_mtex_conv_short.get_corner(RIGHT) + mtex_multi.get_corner(LEFT))/2 )
        text_generating_function_2 = Text("生成函数", font = 'simhei', color = GREEN).scale(0.8).shift(3.4*UP)
        height = text_generating_function_2.get_height()
        under_line_2 = Line(text_generating_function_2.get_corner(DL) + 0.1*DL, text_generating_function_2.get_corner(DR) + 0.1*DR)
        text_generating_function_2.shift(height * DOWN)
        background_2 = BackgroundRectangle(text_generating_function_2, color = "#333333", fill_opacity = 1)

        self.waiting(0, 12)
        self.play(ShowCreation(under_line_2), rate_func = rush_from, run_time = 0.6)
        self.waiting(0, 3) #对应地......
        self.add(text_generating_function_2, background_2)
        self.bring_to_back(text_generating_function_2, background_2)
        self.play(ApplyMethod(long_mul.shift, 3.5*LEFT), FadeIn(VGroup(mtex_multi, mtex_equiv), LEFT), ApplyMethod(text_generating_function.shift, width*RIGHT), ApplyMethod(text_generating_function_2.shift, height*UP))
        self.remove(text_generating_function, background, background_2)
        self.play(Uncreate(right_line), Uncreate(under_line_2), rate_func = lambda t: rush_into(1-t), run_time = 0.6)
        self.waiting(0, 12) #它们的生成函数相乘
        self.waiting(0, 20) #（空闲）

        self.waiting(1, 8) #也就是说......
        self.play(Flash(mtex_conv.get_part_by_tex(r"\vec{c}").get_center() + 2*LEFT, flash_radius = 0.4), *[Flash(long_mul.result.term[i], flash_radius = 0.4) for i in range (4)])
        self.waiting(0, 18) #我们要计算c
        self.play(ShowCreationThenDestructionAround(mtex_multi.get_part_by_tex(r"h(x)")), ShowCreationThenDestructionAround(poly_result, run_time = 2))
        self.waiting(0, 27) #只需要知道c的生成函数就可以了
        self.waiting(1, 2) #（空闲）

        
        self.waiting(2, 23) #这听上去只是好记一点而已
        self.waiting(2, 20) #对计算似乎没什么帮助

        line_divide = Line(RIGHT+2*UP, RIGHT+2.5*DOWN)
        mtex_h_coefficient = MTex(r"h(x)=c_3x^3+c_2x^2+c_1{x}+c_0", tex_to_color_map = {r"h(x)": ORANGE, re.compile(r"c_."): YELLOW, (r"{x}", re.compile(r"x\^.")): PURPLE_A}).scale(0.8).shift(4*RIGHT+1.5*UP)
        mtex_h_interpolate = MTex(r"h(x)=\sum_{i=0}^{3}h(x_i)\prod_{j\ne i}\frac{{x}-{x_i}}{{x_j}-{x_i}}", tex_to_color_map = {(r"h(x)", r"h(x_i)"): ORANGE, r"{x}": PURPLE_A, (r"{x_i}", r"{x_j}"): GREEN}).scale(0.8).next_to(mtex_h_coefficient.get_corner(DL), DR, buff = 0).shift(0.4*DOWN)
        self.play(ReplacementTransform(notice5, notice6), ShowCreation(line_divide))
        self.waiting(0, 3) #但是......
        self.play(Write(mtex_h_coefficient), run_time = 1.5, lag_ratio = 1)
        self.waiting(0, 21+15) #多项式除了可以用系数表示
        self.play(Write(mtex_h_interpolate), run_time = 1.5, lag_ratio = 1)
        self.waiting(2.5, 0) #还可以通过一些点处的取值 插值得出
        self.waiting(0, 25) #（空闲）


        tex_string0 = r"\vec{f} ="
        tex_string1 = r"\begin{bmatrix}f(0)\\f(1)\\f(-1)\\\frac{f(\infty)}{\infty^2}\end{bmatrix}"
        tex_string2 = r"=\begin{bmatrix}{1}&{0}&{0}\\{1}&{1}&{1}\\{1}&{-1}&{1}\\{0}&{0}&{1}\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}a_0\\a_1\\a_2\end{bmatrix}"
        mtex_f = MTex(
        tex_string0 + tex_string1 + tex_string2 + tex_string3,
        tex_to_color_map = {(r"\vec{f}", r"f(0)", r"f(1)", r"f(-1)", r"\frac{f(\infty)}{\infty^2}"): BLUE_P, (r"{1}", r"{0}", r"{-1}"): PURPLE, re.compile(r"a_."): BLUE},
        isolate = [tex_string0, tex_string1, tex_string2, tex_string3],
        ).scale(0.8).next_to(1*UP + 7*LEFT, RIGHT)
        mtex_f_f = mtex_f.get_part_by_tex(tex_string0)
        mtex_f_vec = mtex_f.get_part_by_tex(tex_string1)
        mtex_f_cal = mtex_f.get_part_by_tex(tex_string2)
        mtex_f_a = mtex_f.get_part_by_tex(tex_string3)

        tex_string0 = r"\vec{g} ="
        tex_string1 = r"\begin{bmatrix}g(0)\\g(1)\\g(-1)\\\frac{g(\infty)}{\infty}\end{bmatrix}"
        tex_string2 = r"=\begin{bmatrix}{1}&{0}\\{1}&{1}\\{1}&{-1}\\{0}&{1}\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}b_0\\b_1\end{bmatrix}"
        mtex_g = MTex(
        tex_string0 + tex_string1 + tex_string2 + tex_string3,
        tex_to_color_map = {(r"\vec{g}", r"g(0)", r"g(1)", r"g(-1)", r"\frac{g(\infty)}{\infty}"): RED_P, (r"{1}", r"{0}", r"{-1}"): PURPLE, re.compile(r"b_."): RED},
        isolate = [tex_string0, tex_string1, tex_string2, tex_string3],
        ).scale(0.8).next_to(1.5*DOWN + 7*LEFT, RIGHT)
        mtex_g_g = mtex_g.get_part_by_tex(tex_string0)
        mtex_g_vec = mtex_g.get_part_by_tex(tex_string1)
        mtex_g_cal = mtex_g.get_part_by_tex(tex_string2)
        mtex_g_b = mtex_g.get_part_by_tex(tex_string3)

        tex_string0 = r"\vec{h} ="
        tex_string1 = r"\begin{bmatrix}h(0)\\h(1)\\h(-1)\\\frac{h(\infty)}{\infty^3}\end{bmatrix} = "
        tex_string2 = r"\begin{bmatrix}f(0)g(0)\\f(1)g(1)\\f(-1)g(-1)\\\frac{f(\infty)}{\infty^2}\frac{g(\infty)}{\infty}\end{bmatrix} = "
        tex_string3 = r"\vec{f}\odot\vec{g}"
        mtex_h = MTex(
        tex_string0 + tex_string1 + tex_string2 + tex_string3,
        tex_to_color_map = {(r"\vec{f}", r"f(0)", r"f(1)", r"f(-1)", r"\frac{f(\infty)}{\infty^2}"): BLUE_P, (r"\vec{g}", r"g(0)", r"g(1)", r"g(-1)", r"\frac{g(\infty)}{\infty}"): RED_P, (r"\vec{h}", r"h(0)", r"h(1)", r"h(-1)", r"\frac{h(\infty)}{\infty^3}"): ORANGE},
        isolate = [tex_string0, tex_string1, tex_string2, tex_string3],
        ).scale(0.8).next_to(1*UP + 0.5*LEFT, RIGHT)
        mtex_h_h = mtex_h.get_part_by_tex(tex_string0)
        mtex_h_vec = mtex_h.get_part_by_tex(tex_string1)
        mtex_h_cal = mtex_h.get_part_by_tex(tex_string2)
        mtex_h_fg = mtex_h.get_part_by_tex(tex_string3)

        tex_string0 = r"\vec{c} ="
        tex_string1 = r"\begin{bmatrix}c_0\\c_1\\c_2\\c_3\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}{1}&{0}&{0}&{0}\\{0}&{0.5}&{-0.5}&{-1}\\{-1}&{0.5}&{0.5}&{0}\\{0}&{0}&{0}&{1}\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}h(0)\\h(1)\\h(-1)\\\frac{h(\infty)}{\infty^3}\end{bmatrix}"
        mtex_c = MTex(
        tex_string0 + tex_string1 + tex_string2 + tex_string3,
        tex_to_color_map = {(r"\vec{c}", re.compile(r"c_.")): YELLOW, (r"\vec{h}", r"h(0)", r"h(1)", r"h(-1)", r"\frac{h(\infty)}{\infty^3}"): ORANGE, (r"{1}", r"{0}", r"{-1}", r"{0.5}", r"{-0.5}"): GREEN},
        isolate = [tex_string0, tex_string1, tex_string2, tex_string3],
        ).scale(0.8).next_to(1.5*DOWN + LEFT, RIGHT)
        mtex_c_c = mtex_c.get_part_by_tex(tex_string0)
        mtex_c_vec = mtex_c.get_part_by_tex(tex_string1)
        mtex_c_cal = mtex_c.get_part_by_tex(tex_string2)
        mtex_c_h = mtex_c.get_part_by_tex(tex_string3)
        mtex_c_others = VGroup(mtex_c_c, mtex_c_vec, mtex_c_cal)
        width = mtex_c_others.get_width()
        background = BackgroundRectangle(mtex_c_others, color = "#333333", fill_opacity = 1)


        self.play(ApplyWave(poly_mul_1))
        self.waiting(1, 18) #a的生成函数是二次的
        self.play(ApplyWave(poly_mul_2))
        self.waiting(1, 14) #b的生成函数是一次的
        self.waiting(0, 12)
        self.play(ApplyWave(poly_result))
        self.waiting(1, 7) #于是c的生成函数是三次的
        self.waiting(0, 23) #（空闲）

        self.play(FadeIn(mtex_c_h, LEFT))
        text_notice = Text("最高次项系数", font = 'simsun', color = YELLOW).scale(0.4).move_to(mtex_c_h.get_corner(DOWN) + 0.5*DOWN)
        arrow_notice = Arrow(text_notice.get_corner(UP), mtex_c_h.get_corner(DOWN), buff = 0.1, color = YELLOW)
        self.play(FadeIn(VGroup(text_notice, arrow_notice), 0.5*UP))
        self.waiting(1, 25) #我们只需要知道h在4个点处的取值
        self.add(mtex_c_others, background)
        self.bring_to_back(mtex_c_others, background)
        self.play(FadeOut(VGroup(long_mul, line_divide), 2*LEFT), ApplyMethod(background.shift, (width+0.1)*LEFT))
        self.remove(background)
        self.waiting(0, 15) #就可以解出c来
        self.waiting(0, 21) #（空闲）

        anims = [Indicate(mtex) for mtex in mtex_multi]
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2), FadeOut(mtex_h_coefficient), FadeOut(mtex_h_interpolate), ReplacementTransform(notice6, notice7))
        self.waiting(1, 9) #而h是f和g的乘积

        mtex_f_infty = mtex_f.get_part_by_tex(r"\frac{f(\infty)}{\infty^2}")
        text_notice_f = Text("最高次项系数", font = 'simsun', color = YELLOW).rotate(-PI/2).scale(0.4)
        for text in text_notice_f:
            text.rotate(PI/2)
        text_notice_f.next_to(mtex_f_infty.get_corner(UL), DL, buff = 0).shift(0.8*LEFT)
        arrow_notice_f = Arrow(mtex_f_infty.get_corner(LEFT) + 0.7*LEFT, mtex_f_infty.get_corner(LEFT) + 0.4*LEFT, buff = 0.0, color = YELLOW)
        mtex_g_infty = mtex_g.get_part_by_tex(r"\frac{g(\infty)}{\infty}")
        text_notice_g = Text("最高次项系数", font = 'simsun', color = YELLOW).rotate(-PI/2).scale(0.4)
        for text in text_notice_g:
            text.rotate(PI/2)
        text_notice_g.next_to(mtex_g_infty.get_corner(UL), DL, buff = 0).shift(0.8*LEFT)
        arrow_notice_g = Arrow(mtex_g_infty.get_corner(LEFT) + 0.7*LEFT, mtex_g_infty.get_corner(LEFT) + 0.4*LEFT, buff = 0.0, color = YELLOW)
        
        self.play(FadeIn(VGroup(mtex_f_f, mtex_f_vec), RIGHT), FadeIn(VGroup(mtex_g_g, mtex_g_vec), RIGHT))
        self.play(FadeIn(VGroup(text_notice_f, arrow_notice_f), 0.5*RIGHT), FadeIn(VGroup(text_notice_g, arrow_notice_g), 0.5*RIGHT))
        self.play(FadeIn(VGroup(mtex_f_cal, mtex_f_a), LEFT), FadeIn(VGroup(mtex_g_cal, mtex_g_b), LEFT))
        self.waiting(1, 10) #所以在算出f和g在4个点处的取值后

        self.play(FadeIn(VGroup(mtex_h_h, mtex_h_vec), RIGHT), FadeIn(VGroup(mtex_h_cal, mtex_h_fg), LEFT), ReplacementTransform(notice7, notice8))
        self.waiting(1, 16) #我们只需要把它们乘起来就可以了
        self.waiting(1, 4) #（空闲）

        mtex_f_cover = SurroundingRectangle(VGroup(mtex_f_vec, mtex_f_cal), fill_opacity = 1, stroke_color = PURPLE_A, fill_color = dark(PURPLE_A))
        mtex_a_cover = SurroundingRectangle(mtex_f_a, fill_opacity = 1,stroke_color = BLUE, fill_color = dark(BLUE))
        mtex_g_cover = SurroundingRectangle(VGroup(mtex_g_vec, mtex_g_cal), fill_opacity = 1,stroke_color = PURPLE_A, fill_color = dark(PURPLE_A))
        mtex_b_cover = SurroundingRectangle(mtex_g_b, fill_opacity = 1,stroke_color = RED, fill_color = dark(RED))
        mtex_c_cover = SurroundingRectangle(VGroup(mtex_c_vec, mtex_c_cal), fill_opacity = 1,stroke_color = GREEN, fill_color = dark(GREEN))
        mtex_h_cover = SurroundingRectangle(mtex_c_h, fill_opacity = 1,stroke_color = ORANGE, fill_color = dark(ORANGE))
        

        mtex_f_trans = MTex(r"\vec{f}=P(\vec{a})", isolate = ["=", "(", ")"], tex_to_color_map = {r"\vec{f}":BLUE_P, r"P":PURPLE_A, r"\vec{a}":BLUE}).scale(0.8)
        mtex_f_trans_f = mtex_f_trans.get_part_by_tex(r"\vec{f}=")
        mtex_f_trans_p = VGroup(mtex_f_trans.get_part_by_tex(r"P("), mtex_f_trans.get_part_by_tex(r")"))
        mtex_f_trans_a = mtex_f_trans.get_part_by_tex(r"\vec{a}")
        mtex_f_trans.shift(mtex_f_f.get_center() - mtex_f_trans_f.get_center())

        mtex_g_trans = MTex(r"\vec{g}=P(\vec{b})", isolate = ["=", "(", ")"], tex_to_color_map = {r"\vec{g}":RED_P, r"P":PURPLE_A, r"\vec{b}":RED}).scale(0.8)
        mtex_g_trans_g = mtex_g_trans.get_part_by_tex(r"\vec{g}=")
        mtex_g_trans_p = VGroup(mtex_g_trans.get_part_by_tex(r"P("), mtex_g_trans.get_part_by_tex(r")"))
        mtex_g_trans_b = mtex_g_trans.get_part_by_tex(r"\vec{b}")
        mtex_g_trans.shift(mtex_g_g.get_center() - mtex_g_trans_g.get_center())

        mtex_h_trans = MTex(r"\vec{h}=\vec{f}\odot\vec{g}", isolate = [r"\vec{h}=", r"\vec{f}\odot\vec{g}"], tex_to_color_map={r"\vec{f}":BLUE_P, r"\vec{g}":RED_P, r"\vec{h}":ORANGE}).scale(0.8)
        mtex_h_trans_h = mtex_h_trans.get_part_by_tex(r"\vec{h}=")
        mtex_h_trans.shift(mtex_h_h.get_center() - mtex_h_trans_h.get_center())

        mtex_c_trans = MTex(r"\vec{c}=S(\vec{h})", isolate = ["=", "(", ")"], tex_to_color_map = {r"\vec{c}":YELLOW, r"S":GREEN, r"\vec{h}": ORANGE}).scale(0.8)
        mtex_c_trans_c = mtex_c_trans.get_part_by_tex(r"\vec{c}=")
        mtex_c_trans_s = VGroup(mtex_c_trans.get_part_by_tex(r"S("), mtex_c_trans.get_part_by_tex(r")"))
        mtex_c_trans_h = mtex_c_trans.get_part_by_tex(r"\vec{h}")
        mtex_c_trans.shift(mtex_c_c.get_center() - mtex_c_trans_c.get_center())
        
        self.play(DrawBorderWhileFill(mtex_f_cover), DrawBorderWhileFill(mtex_a_cover), DrawBorderWhileFill(mtex_g_cover), DrawBorderWhileFill(mtex_b_cover), FadeOut(VGroup(text_notice, arrow_notice, text_notice_f, arrow_notice_f, text_notice_g, arrow_notice_g)))
        copy_f = mtex_f_trans_p.copy().move_to(mtex_f_cover.get_center()).set_color(WHITE)
        copy_a = mtex_f_trans_a.copy().move_to(mtex_a_cover.get_center()).set_color(WHITE)
        copy_g = mtex_g_trans_p.copy().move_to(mtex_g_cover.get_center()).set_color(WHITE)
        copy_b = mtex_g_trans_b.copy().move_to(mtex_b_cover.get_center()).set_color(WHITE)
        self.play(Write(copy_f), Write(copy_a), Write(copy_g), Write(copy_b))
        self.remove(mtex_f, mtex_g)
        self.add(mtex_f_trans_f, mtex_g_trans_g)
        self.waiting(0, 15)
        self.play(ReplacementTransform(copy_f, mtex_f_trans_p), ReplacementTransform(copy_a, mtex_f_trans_a), ReplacementTransform(copy_g, mtex_g_trans_p), ReplacementTransform(copy_b, mtex_g_trans_b), FadeOutToPoint(mtex_f_cover, mtex_f_trans_p.get_center()), FadeOutToPoint(mtex_a_cover, mtex_f_trans_a.get_center()), FadeOutToPoint(mtex_g_cover, mtex_g_trans_p.get_center()), FadeOutToPoint(mtex_b_cover, mtex_g_trans_b.get_center()))
        self.waiting(0, 16) #如果我们用P表示从系数到取值的变换

        self.play(DrawBorderWhileFill(mtex_c_cover), DrawBorderWhileFill(mtex_h_cover), ApplyMethod(mtex_h_vec.fade), ApplyMethod(mtex_h_cal.fade))
        copy_c = mtex_c_trans_s.copy().move_to(mtex_c_cover.get_center()).set_color(WHITE)
        copy_h = mtex_c_trans_h.copy().move_to(mtex_h_cover.get_center()).set_color(WHITE)
        self.play(Write(copy_c), Write(copy_h))
        self.remove(mtex_c)
        self.add(mtex_c_trans_c)
        self.waiting(0, 15)
        self.play(ReplacementTransform(copy_c, mtex_c_trans_s), ReplacementTransform(copy_h, mtex_c_trans_h), FadeOutToPoint(mtex_c_cover, mtex_c_trans_s.get_center()), FadeOutToPoint(mtex_h_cover, mtex_c_trans_h.get_center()), TransformMatchingStrings(mtex_h, mtex_h_trans))
        self.waiting(0, 6) #用S表示从取值到系数的变换

        mtex_result = MTex(r"\vec{c}=S\left(P(\vec{a})\odot P(\vec{b})\right)", isolate = [r"\odot"], tex_to_color_map = {r"\vec{c}":YELLOW, r"S": GREEN, r"P": PURPLE_A, r"\vec{a}": BLUE, r"\vec{b}": RED}).scale(0.8).shift(0.25*DOWN)
        surrounding = SurroundingRectangle(mtex_result, buff = 0.2)
        self.play(Write(mtex_result).update_config(run_time = 1, lag_ratio = 1), ShowCreation(surrounding), ReplacementTransform(notice8, notice9))
        self.waiting(1, 27) #那么c的表达式是这个样子的
        self.waiting(1, 4) #（空闲）

        
        position_f_p = mtex_result.select_part(r"P", index = 0).get_center()
        position_g_p = mtex_result.select_part(r"P", index = 1).get_center()
        arrow_notice_f_p = Arrow(position_f_p + 0.7*DOWN, position_f_p + 0.3*DOWN, buff=0, color = PURPLE_A)
        arrow_notice_g_p = Arrow(position_g_p + 0.7*DOWN, position_g_p + 0.3*DOWN, buff=0, color = PURPLE_A)
        text_notice_p = Text("系数到取值的变换", font = 'simsun', color = PURPLE_A).scale(0.4).next_to((position_f_p + position_g_p)/2 + 0.8*DOWN, DOWN, buff = 0)
        position_s = mtex_result.get_part_by_tex(r"S").get_center()
        arrow_notice_s = Arrow(position_s + 0.7*UP, position_s + 0.3*UP, buff=0, color = GREEN)
        text_notice_s = Text("取值到系数的变换", font = 'simsun', color = GREEN).scale(0.4).next_to(position_s + 0.8*UP, UP, buff = 0)
        notices = VGroup(arrow_notice_f_p, arrow_notice_g_p, text_notice_p, arrow_notice_s, text_notice_s).shift(3*RIGHT)
        
        mtex_a.next_to(UP + 6*LEFT, RIGHT)
        mtex_b.next_to(UP + 3*LEFT, RIGHT)
        mtex_conv.next_to(1.5*DOWN + 6.5*LEFT, RIGHT)
        self.play(ApplyMethod(VGroup(mtex_result, surrounding).shift, 3*RIGHT), FadeOut(VGroup(mtex_f_trans, mtex_g_trans, mtex_h_trans, mtex_c_trans), 3*RIGHT), FadeIn(VGroup(mtex_a, mtex_b, mtex_conv, notices), 3*RIGHT))
        self.waiting(1, 11) #Winograd就是按照这样的思路

        mtexes = [r"a_0b_0", r"a_1b_0", r"a_0b_1", r"a_2b_0", r"a_1b_1", r"a_2b_1"]
        anims = [Indicate(mtex_conv.get_part_by_tex(mtex)) for mtex in mtexes]
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2))
        self.waiting(1, 2) #把对a和b做的6次乘法

        odot = mtex_result.get_part_by_tex(r"\odot")
        self.play(Indicate(odot))
        self.waiting(2, 13) #变成了对f和g做的4次乘法

        self.waiting(2, 6) #（空闲）

        mtex_a_2 = MTex(r"\vec{a} = \begin{bmatrix}a_0\\a_1\\\vdots\\a_{m-1}\end{bmatrix}", isolate = [r"="], tex_to_color_map={(r"\vec{a}", r"a_0", r"a_1", r"\vdots", r"a_{m-1}"): BLUE}).scale(0.8).next_to(UP + 6*LEFT, RIGHT)
        mtex_b_2 = MTex(r"\vec{b} = \begin{bmatrix}b_0\\b_1\\\vdots\\b_{n-1}\end{bmatrix}", isolate = [r"="], tex_to_color_map={(r"\vec{b}", r"b_0", r"b_1", r"\vdots", r"b_{n-1}"): RED}).shift(1.5*UP+1*LEFT).scale(0.8).next_to(UP + 3*LEFT, RIGHT)
        tex_string1 = r"\vec{a}*\vec{b}=\vec{c}"
        tex_string2 = r"=\begin{bmatrix}c_0\\c_1\\\vdots\\c_{m+n-2}\end{bmatrix}=\begin{bmatrix}a_0b_0\\a_1b_0+a_0b_1\\{\vdots}\\a_{m-1}b_{n-1}\end{bmatrix}"
        mtex_conv_2 = MTex(tex_string1 + tex_string2, isolate = [tex_string_1, tex_string_2, r"="], tex_to_color_map={(r"\vec{a}", r"a_0", r"a_1", r"a_{m-1}"): BLUE, (r"\vec{b}", r"b_0", r"b_1", r"b_{n-1}"): RED, (r"\vec{c}", r"c_0", r"c_1", r"\vdots", r"c_{m+n-2}"): YELLOW, r"{\vdots}": WHITE}).scale(0.8).next_to(1.5*DOWN + 6.5*LEFT, RIGHT)
        self.play(TransformMatchingStrings(mtex_a, mtex_a_2), TransformMatchingStrings(mtex_b, mtex_b_2), TransformMatchingStrings(mtex_conv, mtex_conv_2))
        self.waiting(0, 12) #更一般地......
        mtexes = [r"a_0", r"a_1", r"\vdots", r"a_{m-1}"]
        anims = [Indicate(mtex_a_2.get_part_by_tex(mtex)) for mtex in mtexes]
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 1.2))
        self.waiting(0, 1)
        mtexes = [r"b_0", r"b_1", r"\vdots", r"b_{n-1}"]
        anims = [Indicate(mtex_b_2.get_part_by_tex(mtex)) for mtex in mtexes]
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 1.2))
        self.waiting(1, 6) #对长度为m和n的向量做卷积

        anims = [Indicate(mtex) for mtex in mtex_multi]
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2))
        self.waiting(0, 12) #通过考虑它们的生成函数

        mtexes = [r"a_0b_0", r"a_1b_0", r"a_0b_1", r"{\vdots}", r"a_{m-1}b_{n-1}"]
        anims = [Indicate(mtex_conv_2.get_part_by_tex(mtex)) for mtex in mtexes]
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2))
        self.waiting(0, 2) #可以把mn次乘法......
        self.play(Indicate(odot))
        self.waiting(0, 21) #降低到m+n-1次

        self.waiting(1, 22) #至此共109秒

        print(self.get_time())

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_3(Scene):

    def construct(self):

        notice9 = Notice("推导完毕", "请　鼓掌")
        notice10 = Notice("经典论断", "请　借鉴")
        notice11 = Notice("一朵乌云", "出大问题")
        notice12 = Notice("数学魔法", "请　验算")
        notice13 = Notice("数学魔法", "请　挠头")
        notice13 = Notice("下节预告", "请　继续")

        tex_string_1 = r"\vec{a}*\vec{b}=\vec{c}"
        tex_string_2 = r"=\begin{bmatrix}c_0\\c_1\\c_2\\c_3\end{bmatrix} = \begin{bmatrix}a_0b_0\\a_1b_0+a_0b_1\\a_2b_0+a_1b_1\\a_2b_1\end{bmatrix}"
        mtex_conv = MTex(tex_string_1 + tex_string_2, isolate = [tex_string_1, tex_string_2, r"="], tex_to_color_map={(r"\vec{a}", re.compile(r"a_.")): BLUE, (r"\vec{b}", re.compile(r"b_.")): RED, (r"\vec{c}", re.compile(r"c_.")): YELLOW}).scale(0.8).next_to(2.5*UP+5*LEFT, RIGHT)
        mtex_conv_short = mtex_conv.get_part_by_tex(tex_string_1)
        copy_mtex_conv_short = mtex_conv_short.copy()
        text_vector = Text("向量", font = 'simhei', color = GREEN).scale(0.8).move_to(copy_mtex_conv_short.get_center() + 0.8*UP)
        mtex_multi = MTex(r"f(x)g(x)=h(x)", tex_to_color_map = {r"f(x)": BLUE_P, r"g(x)": RED_P, r"h(x)": ORANGE}).scale(0.8).shift(2.5*UP)
        mtex_equiv = MTex(r"\Leftrightarrow").move_to( (copy_mtex_conv_short.get_corner(RIGHT) + mtex_multi.get_corner(LEFT))/2 )
        text_generating_function_2 = Text("生成函数", font = 'simhei', color = GREEN).scale(0.8).shift(3.4*UP)
        group_duality = VGroup(copy_mtex_conv_short, text_vector, mtex_multi, mtex_equiv, text_generating_function_2)
        
        mtex_result = MTex(r"\vec{c}=S\left(P(\vec{a})\odot P(\vec{b})\right)", isolate = [r"\odot"], tex_to_color_map = {r"\vec{c}":YELLOW, r"S": GREEN, r"P": PURPLE_A, r"\vec{a}": BLUE, r"\vec{b}": RED}).scale(0.8).shift(0.25*DOWN + 3*RIGHT)
        surrounding = SurroundingRectangle(mtex_result, buff = 0.2)
        position_f_p = mtex_result.select_part(r"P", index = 0).get_center()
        position_g_p = mtex_result.select_part(r"P", index = 1).get_center()
        arrow_notice_f_p = Arrow(position_f_p + 0.7*DOWN, position_f_p + 0.3*DOWN, buff=0, color = PURPLE_A)
        arrow_notice_g_p = Arrow(position_g_p + 0.7*DOWN, position_g_p + 0.3*DOWN, buff=0, color = PURPLE_A)
        text_notice_p = Text("系数到取值的变换", font = 'simsun', color = PURPLE_A).scale(0.4).next_to((position_f_p + position_g_p)/2 + 0.8*DOWN, DOWN, buff = 0)
        position_s = mtex_result.get_part_by_tex(r"S").get_center()
        arrow_notice_s = Arrow(position_s + 0.7*UP, position_s + 0.3*UP, buff=0, color = GREEN)
        text_notice_s = Text("取值到系数的变换", font = 'simsun', color = GREEN).scale(0.4).next_to(position_s + 0.8*UP, UP, buff = 0)
        group_result = VGroup(arrow_notice_f_p, arrow_notice_g_p, text_notice_p, arrow_notice_s, text_notice_s, surrounding, mtex_result)

        mtex_a_2 = MTex(r"\vec{a} = \begin{bmatrix}a_0\\a_1\\\vdots\\a_{m-1}\end{bmatrix}", isolate = [r"="], tex_to_color_map={(r"\vec{a}", r"a_0", r"a_1", r"\vdots", r"a_{m-1}"): BLUE}).scale(0.8).next_to(UP + 6*LEFT, RIGHT)
        mtex_b_2 = MTex(r"\vec{b} = \begin{bmatrix}b_0\\b_1\\\vdots\\b_{n-1}\end{bmatrix}", isolate = [r"="], tex_to_color_map={(r"\vec{b}", r"b_0", r"b_1", r"\vdots", r"b_{n-1}"): RED}).shift(1.5*UP+1*LEFT).scale(0.8).next_to(UP + 3*LEFT, RIGHT)
        tex_string1 = r"\vec{a}*\vec{b}=\vec{c}"
        tex_string2 = r"=\begin{bmatrix}c_0\\c_1\\\vdots\\c_{m+n-2}\end{bmatrix}=\begin{bmatrix}a_0b_0\\a_1b_0+a_0b_1\\{\vdots}\\a_{m-1}b_{n-1}\end{bmatrix}"
        mtex_conv_2 = MTex(tex_string1 + tex_string2, isolate = [tex_string_1, tex_string_2, r"="], tex_to_color_map={(r"\vec{a}", r"a_0", r"a_1", r"a_{m-1}"): BLUE, (r"\vec{b}", r"b_0", r"b_1", r"b_{n-1}"): RED, (r"\vec{c}", r"c_0", r"c_1", r"\vdots", r"c_{m+n-2}"): YELLOW, r"{\vdots}": WHITE}).scale(0.8).next_to(1.5*DOWN + 6.5*LEFT, RIGHT)
        group_origin = VGroup(mtex_a_2, mtex_b_2, mtex_conv_2)

        self.add(notice9, group_duality, group_result, group_origin)
        self.waiting(5, 13) #呼 各位 我向你们保证
        self.waiting(3, 17) #本视频最繁琐的部分已经结束
        self.waiting(2, 17) #我们刚刚完成了全部的推导
        self.waiting(2, 15) #现在是庆祝的时候了
        self.waiting(1, 13) #（空闲）

        self.play(ReplacementTransform(notice9, notice10))
        self.waiting(2, 3) #Winograd算法的大厦已经落成
        self.waiting(3, 15) #这个视频后面的部分 只是一些修饰工作而已
        self.waiting(0, 29) #（空闲）

        self.waiting(3, 28) #晴朗的天空下只剩下一朵小小的乌云
        self.play(FadeOut(VGroup(group_duality, group_origin, group_result),0.5*DOWN), run_time = 2, lag_ratio = 0.01)
        self.waiting(0, 6) #在卷积神经网络里面

        series_a = Series(r"a", 0, 32)
        series_b = Series(r"b", 0, 3)
        long_mul = LongMultiplication(series_a, series_b, r"c", False, h_space = 1.1).scale(0.3).shift(2.5*UP + LEFT)
        long_mul.upper_line.set_stroke(width = 2)
        long_mul.lower_line.set_stroke(width = 2)

        initial = 11.0
        ratio = 2
        alpha = ValueTracker(initial)
        width = 20
        speed = width/(4*ratio)
        initial_position = 10*LEFT + DOWN + initial*speed*LEFT
        amplitude = 0.1
        time_window = 1/6

        def lissajous(time):
            return amplitude * (np.sin(time*PI*5)*UP + np.cos(time*PI*7)*RIGHT)

        def hit(step):
            return (step + max(0, step-(1-time_window)) + min(time_window, step))/(1 + 2*time_window)

        chip_shell = Chip().rotate(PI/2)
        chip_grid = Grid(np.array([16, 16]), 0.25).set_color(GREY)
        chip_text1 = Text("有乘法器", font = 'simsun').scale(0.3)
        chip_text2 = Text("啊啊啊啊", font = 'simsun').scale(0.3)
        for i in range (4):
            chip_text1[i].move_to(2.3*UP+0.5*(i-1.5)*RIGHT)
            chip_text2[i].move_to(2.3*DOWN+0.5*(i-1.5)*RIGHT)
        chip = VGroup(chip_shell, chip_grid, chip_text1, chip_text2).shift(initial_position).save_state()
        def chip_updater(chip):
            a = alpha.get_value()
            tick = int(a)
            step = max(0, a - tick)
            chip.restore().shift((tick+hit(step)) * speed * RIGHT)
            if step >= 1-time_window or step <= time_window:
                chip.set_color(RED).shift(lissajous(a))
        self.add(chip)
        chip.add_updater(chip_updater)

        string = Line(chip.get_corner(RIGHT), 10*RIGHT+DOWN, stroke_width = 1.5)
        def string_updater(string):
            string.put_start_and_end_on(chip.get_corner(RIGHT), 10*RIGHT+DOWN)
        string.add_updater(string_updater)

        def module_updater(index):

            def util(module, index):
                a = alpha.get_value()
                tick = int(a)
                step = max(0, a - tick)

                if tick < index:
                    module.restore()
                elif tick == index:
                    module.restore().shift(tick*speed*RIGHT + step*width*RIGHT)
                    if step >= 1-time_window:
                        module.set_style(stroke_color = RED, fill_color = dark(RED)).shift(lissajous(a))
                else:
                    module.restore().shift((width-speed)*RIGHT + (tick+hit(step))*speed*RIGHT)
                    if step >= 1-time_window or step <= time_window:
                        module.set_style(stroke_color = RED, fill_color = dark(RED)).shift(lissajous(a))
            
            return lambda x : util(x, index)

        module_0 = Block(True, 7, 14, r"\times", colors[2], 9, 2).shift(initial_position + (-4*LEFT) + (width-speed)*LEFT)
        modules = []
        group_modules = VGroup()
        for i in range (3):
            for j in range (10):
                index = i*10+j
                module_ij = module_0.copy().shift(i*DOWN*0.25 + j*LEFT*0.25).save_state()
                self.add(module_ij)
                modules.append(module_ij)
                group_modules.add(module_ij)
                module_ij.add_updater(module_updater(index))

        anims = []
        for i in range (32):
            anim = FadeIn(long_mul.mul_1.term[i], 0.5*DOWN+3*LEFT)
            anim.update_config(rate_func = rush_from)
            anims.append(anim)
        self.play(LaggedStart(*anims, lag_ratio = 0.05, run_time = 3), ReplacementTransform(notice10, notice11))
        self.play(FadeIn(VGroup(long_mul.mul_2, long_mul.mul, long_mul.upper_line), 0.5*UP))
        self.waiting(0, 14) #a 有点......长？

        self.waiting(0, 13)
        self.play(ShowCreation(string)) #（空闲）

        anims = []
        for i in range(32):
            term_group = VGroup(*[long_mul.terms_mul_1[j][31-i] for j in range (3)], *[long_mul.terms_mul_2[j][31-i] for j in range (3)])
            anim = FadeIn(term_group, 0.5*UP+2*RIGHT)
            anim.update_config(rate_func = rush_from)
            anims.append(anim)
        anim = ApplyMethod(alpha.set_value, initial + 3*ratio)
        anim.update_config(run_time = 3, rate_func = linear)
        self.play(LaggedStart(*anims, lag_ratio = 0.05, run_time = 3), anim)
        anim = ApplyMethod(alpha.set_value, initial + 4*ratio)
        anim.update_config(rate_func = linear)
        self.play(anim, FadeIn(VGroup(long_mul.lower_line, long_mul.result), UP), run_time = 1)
        self.waiting(1+3-4, 25+1) #即使用Winograd算法 芯片也没办法一次性把c算出来

        chip.remove_updater(chip_updater)
        string.remove_updater(string_updater)
        for i in range (30):
            modules[i].remove_updater(module_updater(i))
        self.remove(chip, string, group_modules)

        split_lines = []
        for i in range (16):
            linei = Line((long_mul.result.term[2*i+1].get_corner(UR)+long_mul.result.term[2*i+2].get_corner(UL))/2 + 0.05*UP, (long_mul.result.term[2*i+1].get_corner(DR)+long_mul.result.term[2*i+2].get_corner(DL))/2 + 0.05*DOWN, color = ORANGE, width = 1)
            split_lines.append(linei)
        group_lines = VGroup(*split_lines)
        self.play(FadeIn(group_lines, 0.3*UP), run_time = 1.5, lag_ratio = 0.05)
        self.waiting(0, 9) #只能分段

        series_a = Series(r"a", 2, 4)
        series_b = Series(r"b", 0, 3)
        bounded_mul = LongMultiplication(series_a, series_b, r"c", True).shift(DOWN + 3*RIGHT)
        surrounding_mul = SurroundingRectangle(bounded_mul, color = ORANGE, buff = 0.3, width = 1)
        
        copy_width = surrounding_mul.get_width()
        corner_UR = split_lines[1].get_corner(DOWN)
        corner_UL = split_lines[2].get_corner(DOWN)
        target_width = corner_UR[0]-corner_UL[0]
        copy_surrounding = surrounding_mul.copy().scale(target_width/copy_width).next_to(corner_UR, DL, buff = 0).set_style(stroke_opacity = 0)
        line_UR = Line(corner_UR, corner_UR, stroke_opacity = 0, color = ORANGE, width = 1)
        line_UL = Line(corner_UL, corner_UL, stroke_opacity = 0, color = ORANGE, width = 1)
        target_UR = Line(corner_UR, surrounding_mul.get_corner(UR), color = ORANGE, width = 1)
        target_UL = Line(corner_UL, surrounding_mul.get_corner(UL), color = ORANGE, width = 1)
        self.add(copy_surrounding, line_UR, line_UL)
        self.play(TransformFromCopy(long_mul.result.term[4], bounded_mul.result.term[0]), TransformFromCopy(long_mul.result.term[5], bounded_mul.result.term[1]), ReplacementTransform(copy_surrounding, surrounding_mul), Transform(line_UR, target_UR), Transform(line_UL, target_UL))
        anims = []
        for j in range (2, -1, -1):
            for i in range(1, -1, -1):
                terms1 = VGroup(long_mul.terms_mul_1[j][i-j+4], long_mul.terms_mul_2[j][i-j+4])
                terms2 = VGroup(bounded_mul.terms_mul_1[j][i], bounded_mul.terms_mul_2[j][i])
                anim = TransformFromCopy(terms1, terms2)
                anims.append(anim)
        self.play(LaggedStart(*anims, run_time = 1.5), ShowCreation(bounded_mul.lower_line))
        self.waiting(0, 8) #这样 为了算出每一段的c

        anims1 = [FadeIn(bounded_mul.upper_line, 0.5*DOWN), FadeIn(bounded_mul.mul, 0.5*DOWN)]
        anims2 = [FadeIn(mtex, 0.5*DOWN) for mtex in bounded_mul.mul_2.term]
        anims3 = [FadeIn(mtex, 0.5*DOWN) for mtex in bounded_mul.mul_1.term]
        self.play(LaggedStart(*anims1, *anims2, *anims3, lag_ratio = 0.1, run_time = 1.5))
        self.waiting(0, 11) #就要用到更长的a
        self.waiting(0, 20) #（空闲）

        self.play(ApplyWave(bounded_mul.mul_1))
        self.waiting(0, 19) #这种通过更长的a......
        self.play(ApplyWave(bounded_mul.result))
        self.waiting(1, 9) #......算出更短的c的运算

        text_convolution = Text("卷积", font = 'simsun', color = GREEN).shift(3*UP + 4*LEFT)
        text_gossip = Text("计算机科学家：懒得起名了爱咋叫咋叫吧", font = 'simsun', color = GREY).scale(0.3).next_to(text_convolution, DOWN, buff = 0.1)
        mtex_convolution_abc = MTex(r"\vec{a}\ \dot{*}\ \vec{b}=\vec{c}", tex_to_color_map = {r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW}).scale(0.8).shift(1.5*UP + 4*LEFT)
        mtex_convolution_vec = MTex(r"\begin{bmatrix}a_2\\a_3\\a_4\\a_5\end{bmatrix}\dot{*}\begin{bmatrix}b_0\\b_1\\b_2\end{bmatrix}=\begin{bmatrix}c_4\\c_5\end{bmatrix}", tex_to_color_map = {re.compile(r"a_."): BLUE, re.compile(r"b_."): RED, re.compile(r"c_."): YELLOW}).scale(0.8).shift(0.5*DOWN + 4*LEFT)
        mtex_convolution = VGroup(mtex_convolution_abc, mtex_convolution_vec)
        self.play(FadeOut(VGroup(long_mul, group_lines, line_UR, line_UL, surrounding_mul), 0.5*UP), ApplyMethod(bounded_mul.shift, 0.5*UP), FadeIn(VGroup(text_convolution, text_gossip), 0.5*UP))
        self.waiting(1, 5) #一般也被叫做卷积
        self.play(FadeIn(mtex_convolution, 0.5*UP))
        self.waiting(1, 24) # 在本视频里将会用这个符号来表示
        self.waiting(1, 9)

        unbounded_mul = LongMultiplication(series_a, series_b, r"c", False).next_to(bounded_mul.get_corner(DR), UL, buff = 0)
        hidden_left = VGroup(unbounded_mul.result.term[4], unbounded_mul.result.term[5], unbounded_mul.terms_mul_1[2][3], unbounded_mul.terms_mul_1[2][2], unbounded_mul.terms_mul_1[1][3], unbounded_mul.terms_mul_2[2][3], unbounded_mul.terms_mul_2[2][2], unbounded_mul.terms_mul_2[1][3])
        shade_left = BackgroundRectangle(hidden_left, color = "#333333", fill_opacity = 1)
        target_left = Rectangle(height = shade_left.get_height(), width = 0, color = "#333333", fill_opacity = 1, stroke_width = 0).next_to(shade_left, LEFT, buff = 0)
        hidden_right = VGroup(unbounded_mul.result.term[1], unbounded_mul.result.term[0], unbounded_mul.terms_mul_1[0][0], unbounded_mul.terms_mul_1[0][1], unbounded_mul.terms_mul_1[1][0], unbounded_mul.terms_mul_2[0][0], unbounded_mul.terms_mul_2[0][1], unbounded_mul.terms_mul_2[1][0])
        shade_right = BackgroundRectangle(hidden_right, color = "#333333", fill_opacity = 1)
        target_right = Rectangle(height = shade_right.get_height(), width = 0, color = "#333333", fill_opacity = 1, stroke_width = 0).next_to(shade_right, RIGHT, buff = 0)
        self.add(hidden_left, hidden_right, shade_left, shade_right)
        self.bring_to_back(hidden_left, hidden_right, shade_left, shade_right, target_left, target_right)
        self.waiting(1, 15)
        self.play(Transform(shade_left, target_left), Transform(shade_right, target_right), Transform(bounded_mul.lower_line, unbounded_mul.lower_line))
        self.remove(shade_left, shade_right, target_left, target_right)
        self.waiting(1, 1) #我们确实可以用之前的思路把c全部算出来
        self.play(ApplyMethod(hidden_left.set_color, GREY), ApplyMethod(hidden_right.set_color, GREY))
        self.waiting(1, 12) #然后只取中间
        self.waiting(3, 13) #但这太浪费了 有没有更简单的方法呢
        self.waiting(1, 0) #（空闲）

        self.play(FadeOut(VGroup(text_convolution, text_gossip, mtex_convolution, bounded_mul, hidden_left, hidden_right), DOWN), ReplacementTransform(notice11, notice12))
        self.waiting(0, 27) #还真有

        tex_string1 = r"\vec{f} = \begin{bmatrix}f_0\\f_1\\f_2\\f_3\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}a_5-a_3\\(a_4+a_3){/2}\\(-a_4+a_3){/2}\\-a_4+a_2\end{bmatrix}="
        tex_string3 = r"\begin{bmatrix}{1}&{0}&{-1}&{0}\\{0}&{0.5}&{0.5}&{0}\\{0}&{-0.5}&{0.5}&{0}\\{0}&{-1}&{0}&{1}\end{bmatrix}"
        tex_string4 = r"\begin{bmatrix}a_5\\a_4\\a_3\\a_2\end{bmatrix}"

        mtex_f = MTex(
        tex_string1 + tex_string2 + tex_string3 + tex_string4, 
        tex_to_color_map = {(r"\vec{f}", re.compile(r"f_.")): TEAL, (r"{/2}", r"{1}", r"{0}", r"{-1}", r"{0.5}", r"{-0.5}", r"+", r"-", r"(", r")"): GREEN, re.compile(r"a_."): BLUE}, 
        isolate = [tex_string1, tex_string2, tex_string3, tex_string4],
        ).scale(0.8).next_to(1.5*UP + 7*LEFT, RIGHT)
        
        mtex_f_short = MTex(
        tex_string1 + tex_string3 + tex_string4,
        tex_to_color_map = {(r"\vec{f}", re.compile(r"f_.")): TEAL, (r"{1}", r"{0}", r"{-1}", r"{0.5}", r"{-0.5}"): GREEN, re.compile(r"a_."): BLUE},
        isolate = [tex_string1, tex_string3, tex_string4],
        ).scale(0.8).next_to(1.5*UP + 7*LEFT, RIGHT)
        
        mtex_f_a = mtex_f.get_part_by_tex(tex_string4)
        mtex_f_cal = mtex_f.get_part_by_tex(tex_string2 + tex_string3)
        mtex_f_others = mtex_f.get_part_by_tex(tex_string1)
        mtex_f_short_f = mtex_f_short.get_part_by_tex(tex_string1)
        mtex_f_short_cal = mtex_f_short.get_part_by_tex(tex_string3)
        mtex_f_short_a = mtex_f_short.get_part_by_tex(tex_string4)
        
        tex_string1 = r"\vec{g} = \begin{bmatrix}g_0\\g_1\\g_2\\g_3\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}b_0\\b_0+b_1+b_2\\b_0-b_1+b_2\\b_2\end{bmatrix}="
        tex_string3 = r"\begin{bmatrix}{1}&{0}&{0}\\{1}&{1}&{1}\\{1}&{-1}&{1}\\{0}&{0}&{1}\end{bmatrix}"
        tex_string4 = r"\begin{bmatrix}b_0\\b_1\\b_2\end{bmatrix}"

        mtex_g = MTex(
        tex_string1 + tex_string2 + tex_string3 + tex_string4, 
        tex_to_color_map = {(r"\vec{g}", re.compile(r"g_.")): RED_P, (r"{1}", r"{0}", r"{-1}", r"+", r"-"): PURPLE, re.compile(r"b_."): RED},
        isolate = [tex_string1, tex_string2, tex_string3, tex_string4],
        ).scale(0.8).next_to(1.5*DOWN + 7*LEFT, RIGHT)
        mtex_g_short = MTex(
        tex_string1 + tex_string3 + tex_string4,
        tex_to_color_map = {(r"\vec{g}", re.compile(r"g_.")): RED_P, (r"{1}", r"{0}", r"{-1}"): PURPLE, re.compile(r"b_."): RED},
        isolate = [tex_string1, tex_string3, tex_string4],
        ).scale(0.8).next_to(1.5*DOWN + 7*LEFT, RIGHT)
        
        mtex_g_b = mtex_g.get_part_by_tex(tex_string4)
        mtex_g_cal = mtex_g.get_part_by_tex(tex_string2 + tex_string3)
        mtex_g_others = mtex_g.get_part_by_tex(tex_string1)
        mtex_g_short_g = mtex_g_short.get_part_by_tex(tex_string1)
        mtex_g_short_cal = mtex_g_short.get_part_by_tex(tex_string3)
        mtex_g_short_b = mtex_g_short.get_part_by_tex(tex_string4)
        
        tex_string1 = r"\vec{h} = \begin{bmatrix}h_0\\h_1\\h_2\\h_3\end{bmatrix} = "
        tex_string2 = r"\begin{bmatrix}f_0g_0\\f_1g_1\\f_2g_2\\f_3g_3\end{bmatrix} = \vec{f}\odot\vec{g}"
        mtex_h = MTex(
        tex_string1 + tex_string2,
        tex_to_color_map = {(r"\vec{f}", re.compile(r"f_.")): TEAL, (r"\vec{g}", re.compile(r"g_.")): RED_P, (r"\vec{h}", re.compile(r"h_.")): ORANGE},
        isolate = [tex_string1, tex_string2],
        ).scale(0.8).next_to(1.5*UP + 0*LEFT, RIGHT)
        mtex_h_fg = mtex_h.get_part_by_tex(tex_string2)
        mtex_h_others = mtex_h.get_part_by_tex(tex_string1)

        tex_string1 = r"\vec{c} = \begin{bmatrix}c_5\\c_4\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}{1}&{1}&{1}&{0}\\{0}&{1}&{-1}&{1}\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}h_0\\h_1\\h_2\\h_3\end{bmatrix}"
        mtex_c = MTex(
        tex_string1 + tex_string2 + tex_string3,
        tex_to_color_map = {(r"\vec{c}", re.compile(r"c_.")): YELLOW, (r"\vec{h}", re.compile(r"h_.")): ORANGE, (r"{1}", r"{0}", r"{-1}"): PURPLE},
        isolate = [tex_string1, tex_string2, tex_string3],
        ).scale(0.8).next_to(1.5*DOWN + 0*LEFT, RIGHT)
        mtex_c_h = mtex_c.get_part_by_tex(tex_string3)
        mtex_c_cal = mtex_c.get_part_by_tex(tex_string2)
        mtex_c_others = mtex_c.get_part_by_tex(tex_string1)

        self.waiting(0, 11) #首先......
        self.play(FadeIn(mtex_f_a, LEFT))
        self.play(FadeIn(mtex_g_b, LEFT))
        self.waiting(1, 3) #通过a和b

        self.play(FadeIn(mtex_f_cal, RIGHT), FadeIn(mtex_g_cal, RIGHT))
        self.waiting(1, 5) #计算出两个新的向量
        self.play(FadeIn(mtex_f_others, RIGHT))
        self.play(FadeIn(mtex_g_others, RIGHT))
        self.waiting(3+1-4, 19+4-5) #f和g （空闲）
        
        self.play(TransformMatchingStrings(mtex_f, mtex_f_short), TransformMatchingStrings(mtex_g, mtex_g_short))
        self.waiting(0, 9) #接着......
        self.play(FadeIn(mtex_h_fg, LEFT))
        self.waiting(1, 19) #把f和g乘起来
        self.play(FadeIn(mtex_h_others, RIGHT))
        self.waiting(5-4, 2-9-19) #得到h
        self.waiting(0, 24) #（空闲）

        self.waiting(1, 7) #最后
        self.play(FadeIn(mtex_c_h, LEFT))
        self.waiting(0, 3) #通过h
        self.play(FadeIn(mtex_c_cal, RIGHT), FadeIn(mtex_c_others, RIGHT))
        self.waiting(0, 5) #计算出c
        self.waiting(1, 10) #（空闲）

        group_others = VGroup(mtex_f_short_f, mtex_f_short_a, mtex_g_short_g, mtex_g_short_b, mtex_h, mtex_c_h, mtex_c_others)
        copy_others = group_others.copy()
        surr_f_cal = SurroundingRectangle(mtex_f_short_cal, color = GREEN)
        surr_g_cal = SurroundingRectangle(mtex_g_short_cal, color = PURPLE)
        surr_c_cal = SurroundingRectangle(mtex_c_cal, color = PURPLE)
        group_surrs = VGroup(surr_f_cal, surr_g_cal, surr_c_cal)
        
        arrow_f = CurvedArrow(surr_c_cal.get_corner(UL)+0.1*UL, surr_f_cal.get_corner(DR)+0.1*DR, angle = PI/6, color = ["#333333", GREEN], tip_length = 0.20)
        arrow_f.get_tip().set_color(GREEN)
        arrow_f_text = Text("转置", font = "simsun", color = GREEN).scale(0.5).move_to(arrow_f.get_center()+0.1*DL)
        arrow_g = CurvedArrow(surr_f_cal.get_corner(DL)+0.1*DL, surr_g_cal.get_corner(UL)+0.1*UL, angle = 4*PI/6, color = ["#333333", PURPLE], tip_length = 0.20)
        tip_g = arrow_g.get_tip()
        tip_g.set_color(PURPLE).rotate(-PI/12, about_point = tip_g.get_base())
        arrow_g_text = Text("不转置", font = "simsun", color = PURPLE).scale(0.5).next_to(arrow_g.get_corner(RIGHT), RIGHT, buff = 0)
        arrow_c = CurvedArrow(surr_g_cal.get_corner(DR)+0.1*DR, surr_c_cal.get_corner(DL)+0.1*DL, angle = PI/6, color = ["#333333", PURPLE], tip_length = 0.20)
        arrow_c.get_tip().set_color(PURPLE)
        arrow_c_text = Text("转置", font = "simsun", color = PURPLE).scale(0.5).move_to(arrow_c.get_center())
        group_arrows = VGroup(arrow_f, arrow_g, arrow_c)
        group_texts = VGroup(arrow_f_text, arrow_g_text, arrow_c_text)

        self.play(ApplyMethod(group_others.set_color, GREY), ShowCreation(surr_f_cal), ShowCreation(surr_g_cal), ShowCreation(surr_c_cal), ReplacementTransform(notice12, notice13))
        self.play(ShowCreation(arrow_f), ShowCreation(arrow_g), ShowCreation(arrow_c), FadeIn(group_texts))
        self.waiting(2, 28) #这看起来不过是取了矩阵转置 又重新排列了一下
        self.waiting(2, 15) #怎么看都像是在胡闹
        self.play(FadeOut(group_surrs), FadeOut(arrow_f), FadeOut(arrow_g), FadeOut(arrow_c), FadeOut(group_texts), Transform(group_others, copy_others))
        self.waiting(1, 3) #但它确实能算出正确的结果
        self.waiting(0, 24) #（空闲）

        self.waiting(1, 22) #这是为什么呢
        self.waiting(1, 28) #想要理解这个方法
        self.remove(mtex_f_short, mtex_g_short, mtex_h, mtex_c)

        text_duality = Text("对偶性", font = "simhei").shift(UP)
        mtex_duality = MTex(r"\langle\vec{u}, \vec{v}\rangle=L(\vec{v})").shift(0.5*DOWN)
        self.play(FadeIn(text_duality, UP), FadeIn(mtex_duality, UP))
        self.waiting(1, 22) #需要先理解一个叫“对偶性”的概念

        self.waiting(2, 24)
        self.play(FadeOut(VGroup(text_duality, mtex_duality), DOWN), FadeOut(notice13))
        self.waiting(3, 0) #到此共112秒
        print(self.get_time())
        print(self.num_plays)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_0(Scene):
    
    def construct(self):

        ##  Making object
        text2 = Text("第二节　对偶性与叉积", font = 'simsun', t2c={"第二节": YELLOW, "对偶性": GREEN, "叉积": BLUE})

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(Scene):
    
    def construct(self):
        notice1 = Notice("线性代数", "请　复习")
        notice2 = Notice("重要定理", "请记笔记")
        notice3 = Text("真的吗？", font = 'simsun').scale(0.5).shift(np.array([5.8,2.9,0]))

        distance = 1.8
        text_inner_product = Text("内积", font = 'simhei', color = ORANGE).shift(3*distance*LEFT + 1.7*UP).scale(0.8)
        mtex_inner_product = MTex(r"\langle \vec{u}, \vec{v}\rangle", tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": RED}).shift(3*distance*LEFT + 1*UP)
        group_inner_product = VGroup(text_inner_product, mtex_inner_product)
        text_dot_product = Text("点乘", font = 'simhei', color = YELLOW_O).shift(distance*LEFT + 1.7*UP).scale(0.8)
        mtex_dot_product = MTex(r"\vec{u}\cdot \vec{v}", tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": RED}).shift(distance*LEFT + 1*UP)
        group_dot_product = VGroup(text_dot_product, mtex_dot_product)
        text_multiplication = Text("矩阵乘法", font = 'simhei', color = YELLOW_G).shift(distance*RIGHT + 1.7*UP).scale(0.8)
        mtex_multiplication = MTex(r"\vec{u}^\mathrm{T}\vec{v}", tex_to_color_map = {(r"\vec{u}", r"\mathrm{T}"): BLUE, r"\vec{v}": RED}).shift(distance*RIGHT + 1*UP)
        group_multiplication = VGroup(text_multiplication, mtex_multiplication)
        text_linear_function = Text("线性函数", font = 'simhei', color = GREEN).shift(3*distance*RIGHT + 1.7*UP).scale(0.8)
        mtex_linear_function = MTex(r"L(\vec{v})", tex_to_color_map = {r"L": BLUE, r"\vec{v}": RED}).shift(3*distance*RIGHT + 1*UP)
        group_linear_function = VGroup(text_linear_function, mtex_linear_function)
        group_concepts = VGroup(group_inner_product, group_dot_product, group_multiplication, group_linear_function)

        mtex_inner_dot = MTex(r"\langle \vec{u}, \vec{v}\rangle &= \vec{u}^\mathrm{T}A\vec{v}\\ &=\vec{u}^\mathrm{T}D^\mathrm{T}D\vec{v}\\ &=(D\vec{u})^\mathrm{T}(D\vec{v})\\ &=(D\vec{u})\cdot(D\vec{v})", tex_to_color_map = {(r"\vec{u}", r"\mathrm{T}"): BLUE, r"\vec{v}": RED, (r"A", r"D"): GREEN}).scale(0.8).next_to(2*distance*LEFT + 0.5*UP, DOWN)
        mtex_dot_mul = MTex(r"\vec{u}\cdot \vec{v} = \vec{u}^\mathrm{T}\vec{v}", tex_to_color_map = {(r"\vec{u}", r"\mathrm{T}"): BLUE, r"\vec{v}": RED}).scale(0.8).next_to(0.5*UP, DOWN)
        tex_string1 = r"\begin{bmatrix}1\\0 \end{bmatrix}" 
        tex_string2 = r"\begin{bmatrix}0\\1 \end{bmatrix}"
        mtex_linear_mul = MTex(r"L \left(" + tex_string1 + r"\right) &= {a} \\ L \left(" + tex_string2 + r"\right) &= {b}", isolate = [tex_string1, tex_string2], tex_to_color_map = {(r"L", r"{a}", r"{b}"): BLUE, (tex_string1, tex_string2): RED}).scale(0.8).next_to(3*distance*RIGHT + 0.5*UP, DOWN)
        mtex_mul_linear = MTex(r"\vec{u}^\mathrm{T}\vec{v} = \begin{bmatrix}{a}&{b} \end{bmatrix}\vec{v}", tex_to_color_map = {(r"\vec{u}", r"\mathrm{T}", r"{a}", r"{b}"): BLUE, r"\vec{v}": RED}).scale(0.8).move_to(mtex_linear_mul.get_center() + 2*distance*LEFT)
        
        self.play(Write(notice1))
        self.waiting(1, 10) #大家如果学过线性代数
        self.waiting(3, 2) #一定会很熟悉这四个概念
        self.play(FadeIn(group_inner_product, UP))
        self.waiting(0, 27) #两个向量的内积
        self.play(FadeIn(group_dot_product, UP))
        self.waiting(1, 0) #两个向量的点乘
        self.play(FadeIn(group_multiplication, UP))
        self.waiting(1, 18) #行向量与列向量的乘法
        self.waiting(0, 16) #以及......
        self.play(FadeIn(group_linear_function, UP))
        self.waiting(1, 9) #从向量到标量的线性函数
        self.waiting(1, 0) #（空闲）

        self.waiting(3, 11) #它们之间有着很紧密的联系
        self.play(Write(mtex_inner_dot), run_time = 3, lag_ratio = 1)
        self.waiting(2+3+0-4, 9+2+28) #点乘是内积的一种 而任何内积都是基变换后的点乘
        self.play(FadeOut(mtex_inner_dot, DOWN)) #（空闲）
        self.play(Write(mtex_dot_mul), run_time = 1, lag_ratio = 1)
        self.waiting(3, 0) #点乘一般直接用行向量和列向量的乘法来定义
        self.play(FadeOut(mtex_dot_mul, DOWN)) #（空闲）
        self.play(Write(mtex_linear_mul), run_time = 2)
        self.waiting(1, 13) #任何线性函数都有对应的矩阵表达
        self.waiting(2, 0) #映射到标量的线性函数对应的......
        self.play(FadeIn(mtex_mul_linear, UP))
        self.waiting(0, 3) #......矩阵
        self.waiting(1, 17) #就正好是行向量
        self.waiting(0, 4) 
        self.play(FadeOut(VGroup(mtex_linear_mul, mtex_mul_linear))) #（空闲）

        arrow_linear_mul = ArcBetweenPoints(text_linear_function.get_corner(UL)+0.2*UL, text_multiplication.get_corner(UR)+0.2*UR, angle = PI/3, color = [GREEN, YELLOW_G], tip_config = {"width" : 0.2, "length" : 0.2})
        tip_linear_mul = arrow_linear_mul.create_tip(fill_color = YELLOW_G)
        tip_linear_mul.rotate(-6*DEGREES, about_point = tip_linear_mul.get_tip_point()).save_state()
        arrow_mul_dot = ArcBetweenPoints(text_multiplication.get_corner(UL)+0.2*UL, text_dot_product.get_corner(UR)+0.2*UR, angle = PI/3, color = [YELLOW_G, YELLOW, YELLOW_O], tip_config = {"width" : 0.2, "length" : 0.2})
        tip_mul_dot = arrow_mul_dot.create_tip(fill_color = YELLOW_O)
        tip_mul_dot.rotate(-6*DEGREES, about_point = tip_mul_dot.get_tip_point()).save_state()
        arrow_dot_inner = ArcBetweenPoints(text_dot_product.get_corner(UL)+0.2*UL, text_inner_product.get_corner(UR)+0.2*UR, angle = PI/3, color = [YELLOW_O, ORANGE], tip_config = {"width" : 0.2, "length" : 0.2})
        tip_dot_inner = arrow_dot_inner.create_tip(fill_color = ORANGE)
        tip_dot_inner.rotate(-6*DEGREES, about_point = tip_dot_inner.get_tip_point()).save_state()

        arrow_inner_dot = ArcBetweenPoints(text_inner_product.get_corner(DR)+0.2*DR, text_dot_product.get_corner(DL)+0.2*DL, angle = PI/3, color = [ORANGE, YELLOW_O], tip_config = {"width" : 0.2, "length" : 0.2})
        tip_inner_dot = arrow_inner_dot.create_tip(fill_color = YELLOW_O)
        tip_inner_dot.rotate(-6*DEGREES, about_point = tip_inner_dot.get_tip_point()).save_state()
        arrow_dot_mul = ArcBetweenPoints(text_dot_product.get_corner(DR)+0.2*DR, text_multiplication.get_corner(DL)+0.2*DL, angle = PI/3, color = [YELLOW_O, YELLOW, YELLOW_G], tip_config = {"width" : 0.2, "length" : 0.2})
        tip_dot_mul = arrow_dot_mul.create_tip(fill_color = YELLOW_G)
        tip_dot_mul.rotate(-6*DEGREES, about_point = tip_dot_mul.get_tip_point()).save_state()
        arrow_mul_linear = ArcBetweenPoints(text_multiplication.get_corner(DR)+0.2*DR, text_linear_function.get_corner(DL)+0.2*DL, angle = PI/3, color = [YELLOW_G, GREEN], tip_config = {"width" : 0.2, "length" : 0.2})
        tip_mul_linear = arrow_mul_linear.create_tip(fill_color = GREEN)
        tip_mul_linear.rotate(-6*DEGREES, about_point = tip_mul_linear.get_tip_point()).save_state()
        group_arrows = VGroup(arrow_linear_mul, tip_linear_mul, arrow_mul_dot, tip_mul_dot, arrow_dot_inner, tip_dot_inner, arrow_inner_dot, tip_inner_dot, arrow_dot_mul, tip_dot_mul, arrow_mul_linear, tip_mul_linear)

        alpha = ValueTracker(0.0)
        def tip_updater(arrow):
            def util(tip, arrow):
                a = alpha.get_value()
                tip.restore()
                tip.scale(a, about_point = tip.get_tip_point()).rotate((a-1) * PI/3 + a*5*DEGREES, about_point = arrow.get_arc_center())
            return lambda x : util(x, arrow)

        self.waiting(1, 4) #于是......
        self.add(tip_linear_mul, tip_inner_dot)
        func1 = tip_updater(arrow_linear_mul)
        func2 = tip_updater(arrow_inner_dot)
        tip_linear_mul.add_updater(func1)
        tip_inner_dot.add_updater(func2)
        self.play(ShowCreation(arrow_linear_mul), ShowCreation(arrow_inner_dot), ApplyMethod(alpha.set_value, 1.0), rate_func = smooth, run_time = 0.5)
        tip_linear_mul.remove_updater(func1)
        tip_inner_dot.remove_updater(func2)

        alpha.set_value(0.0)
        self.add(tip_mul_dot, tip_dot_mul)
        func1 = tip_updater(arrow_mul_dot)
        func2 = tip_updater(arrow_dot_mul)
        tip_mul_dot.add_updater(func1)
        tip_dot_mul.add_updater(func2)
        self.play(ShowCreation(arrow_mul_dot), ShowCreation(arrow_dot_mul), ApplyMethod(alpha.set_value, 1.0), rate_func = smooth, run_time = 0.5)
        tip_mul_dot.remove_updater(func1)
        tip_dot_mul.remove_updater(func2)

        alpha.set_value(0.0)
        self.add(tip_dot_inner, tip_mul_linear)
        func1 = tip_updater(arrow_dot_inner)
        func2 = tip_updater(arrow_mul_linear)
        tip_dot_inner.add_updater(func1)
        tip_mul_linear.add_updater(func2)
        self.play(ShowCreation(arrow_dot_inner), ShowCreation(arrow_mul_linear), ApplyMethod(alpha.set_value, 1.0), rate_func = smooth, run_time = 0.5)
        tip_dot_inner.remove_updater(func1)
        tip_mul_linear.remove_updater(func2)
        self.waiting(2, 4) #......一个线性函数就可以很自然地对应一个内积
        self.waiting(0, 23) #（空闲）

        background = Rectangle(width = FRAME_WIDTH, height = FRAME_HEIGHT, color = WHITE, stroke_width = 1, fill_opacity = 0.5)
        board = Rectangle(width = 8.6,  height = 6.5, color = BLACK, stroke_width = 0, fill_opacity = 1).shift(0.25*LEFT)
        tex_string1 = r"在域$\mathrm{F}$上的线性空间$\mathrm{V}$中，\\"
        tex_string2 = r"对于任意一个线性函数$L: \mathrm{V}\to \mathrm{F}$，\\"
        tex_string3 = r"若$\mathrm{V}$上定义了内积$\langle\cdot, \cdot\rangle: \mathrm{V}\times \mathrm{V}\to \mathrm{F}$，则\\"
        tex_string4 = r"存在一个向量$\vec{u}=\vec{u}(L)\in \mathrm{V}$，\\"
        tex_string5 = r"使得对于任意向量$\vec{v}\in \mathrm{V}$，有"
        tex_string6 = r"$$\langle\vec{u}, \vec{v}\rangle=L(\vec{v}),$$"
        tex_string7 = r"其中$\vec{u}$被称为$L$的对偶向量。"
        mtex_theorem = MTexText(
            tex_string1 + tex_string2 + tex_string3 + tex_string4 + tex_string5 + tex_string6 + tex_string7, 
        alignment="", isolate = [tex_string1, tex_string2, tex_string3, tex_string4, tex_string5, tex_string6, tex_string7], 
        tex_to_color_map = {(r"\vec{u}", r"L"): BLUE, r"\vec{v}": RED, r"\mathrm{F}": BLUE_P, r"\mathrm{V}": RED_P}
        ).scale(0.8).shift(0.25*LEFT)
        theorem_basic = mtex_theorem.get_part_by_tex(tex_string1)
        theorem_linear = mtex_theorem.get_part_by_tex(tex_string2)
        theorem_inner = mtex_theorem.get_part_by_tex(tex_string3)
        theorem_dual = mtex_theorem.get_part_by_tex(tex_string4)
        theorem_vec = mtex_theorem.get_part_by_tex(tex_string5)
        theorem_formula = mtex_theorem.get_part_by_tex(tex_string6)
        theorem_name = mtex_theorem.get_part_by_tex(tex_string7)
        theorem_formula.shift((theorem_formula.get_center()[0])*LEFT + 0.25*LEFT)
        
        self.play(FadeIn(background), FadeIn(board, 8*UP), ReplacementTransform(notice1, notice2))
        self.waiting(0, 22) #具体来说

        self.play(Write(theorem_basic), run_time = 1.5, lag_ratio = 1)
        self.waiting(0, 15)
        self.play(Write(theorem_linear), run_time = 1.5, lag_ratio = 1)
        self.waiting(0, 25) #对于任意一个从向量到标量的线性函数L
        self.play(Write(theorem_inner), run_time = 1.5, lag_ratio = 1)
        self.waiting(0, 6) #与一个内积<·,·>
        self.play(Write(theorem_dual), run_time = 1.5, lag_ratio = 1)
        self.waiting(0, 11) #存在一个向量u
        self.play(Write(theorem_vec), run_time = 1.5, lag_ratio = 1)
        self.waiting(0, 25) #使得对于任何向量v
        self.play(Write(theorem_formula), run_time = 1.5, lag_ratio = 1)
        self.waiting(1, 17) #使得对于任何向量v
        self.waiting(0, 22) #（空闲）
        self.play(Write(theorem_name), run_time = 2, lag_ratio = 1)
        self.waiting(2, 10) #这个向量u 就被称作线性函数L的对偶向量
        self.waiting(0, 29) #（空闲）

        title_duality = Text("对偶性原理", font = "simhei", color = YELLOW).shift(3.3*UP)
        self.play(FadeOut(background), ApplyMethod(board.shift, 0.75*DOWN), ApplyMethod(mtex_theorem.shift, 0.5*DOWN), FadeIn(title_duality, 0.5*DOWN))
        self.waiting(1, 2) #这就是对偶性原理

        fullchip = FullChip().scale(0.5).rotate(PI/6).shift(4.15*UP + 6.5*LEFT).shift(2*unit(2*PI/3))
        bubble = Union(Ellipse(width = 1.8, height = 0.9), Triangle().scale(0.5).rotate(PI/4).shift(0.6*LEFT + 0.15*UP))
        text = Text("可爱！", font = "lolita").scale(0.6)
        cute = VGroup(bubble, text).shift(3.1*UP + 4*LEFT)
        
        self.play(ApplyMethod(fullchip.shift, -2*unit(2*PI/3)))
        self.waiting(0, 17)
        self.play(FadeInFromPoint(cute, cute.get_corner(UL) + 0.3*LEFT), run_time = 0.5)
        self.waiting(1, 1) #看上去又和善 又可爱

        self.waiting(0, 21)
        self.play(ApplyMethod(VGroup(fullchip, cute).shift, 2*unit(2*PI/3)))
        self.waiting(0, 20) #唯一的缺点就是太平凡了
        self.waiting(1, 8) #似乎没什么用
        self.waiting(0, 29) #（空闲）

        all_text = VGroup(mtex_theorem, group_concepts, group_arrows, title_duality)
        all_text.set_color(WHITE)
        self.remove(notice2)
        self.add(notice3)
        self.waiting(1, 0) #真的吗
        self.waiting(3, 0) #到此共80秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_2(Scene):
    
    def construct(self):
        notice3 = Text("真的吗？", font = 'simsun').scale(0.5).shift(np.array([5.8,2.9,0]))
        notice4 = Notice("醒了吧？", "我们继续")
        notice5 = Notice("线性代数", "请　复习")
        notice6 = Notice("奇思妙想", "请　模仿")
        notice7 = Notice("前情提要", "请　参考")
        notice8 = Notice("张量代数", "请　选修*")
        notice9 = Notice("神奇结论", "请　模仿")
        notice10 = Notice("经典例子", "请　参考")
        notice11 = Notice("下节预告", "请　继续")

        determinant = MTex(r"\det(A)=\begin{vmatrix}{{3}}&{{2}}&{{-6}}\\{{8}}&{{-1}}&{{-5}}\\{{-4}}&{{7}}&{{-9}}\end{vmatrix}=4",  tex_to_color_map = {(r"\det", r"A"): WHITE}).scale(0.8)
        symbol = determinant.get_part_by_tex(r"\det")
        matrix = determinant.get_part_by_tex(r"A")
        column_a = determinant.get_parts_by_tex((r"3", r"8", r"-4"))
        column_b = determinant.get_parts_by_tex((r"2", r"-1", r"7"))
        column_c = determinant.get_parts_by_tex((r"-6", r"-5", r"-9"))
        
        self.play(ReplacementTransform(notice3, notice4), FadeIn(determinant, 0.5*UP))
        self.waiting(1, 2) #我们学过行列式
        self.waiting(2, 22) #它是矩阵到标量的映射

        split_line_1 = DashedLine((column_a.get_corner(UR)+column_b.get_corner(UL))/2 + 0.2*UP, (column_a.get_corner(DR)+column_b.get_corner(DL))/2 + 0.2*DOWN)
        split_line_2 = DashedLine((column_b.get_corner(UR)+column_c.get_corner(UL))/2 + 0.2*UP, (column_b.get_corner(DR)+column_c.get_corner(DL))/2 + 0.2*DOWN)
        
        bottom_a = column_a.get_corner(DOWN)
        vec_a = MTex(r"\vec{a}", color = RED).next_to(bottom_a+1.2*DOWN, UP, buff = 0).scale(0.8)
        arrow_a = Arrow(bottom_a+0.8*DOWN, bottom_a+0.2*DOWN, buff = 0.1, color = RED)
        bottom_b = column_b.get_corner(DOWN)
        vec_b = MTex(r"\vec{b}", color = YELLOW).next_to(bottom_b+1.2*DOWN, UP, buff = 0).scale(0.8)
        arrow_b = Arrow(bottom_b+0.8*DOWN, bottom_b+0.2*DOWN, buff = 0.1, color = YELLOW)
        bottom_c = column_c.get_corner(DOWN)
        vec_c = MTex(r"\vec{c}", color = GREEN).next_to(bottom_c+1.2*DOWN, UP, buff = 0).scale(0.8)
        arrow_c = Arrow(bottom_c+0.8*DOWN, bottom_c+0.2*DOWN, buff = 0.1, color = GREEN)
        splits = VGroup(split_line_1, split_line_2, vec_a, arrow_a, vec_b, arrow_b, vec_c, arrow_c)

        anims1 = AnimationGroup(ApplyMethod(column_a.set_color, RED), FadeIn(VGroup(vec_a, arrow_a), 0.5*UP))
        anims2 = AnimationGroup(ApplyMethod(column_b.set_color, YELLOW), FadeIn(VGroup(vec_b, arrow_b), 0.5*UP))
        anims3 = AnimationGroup(ApplyMethod(column_c.set_color, GREEN), FadeIn(VGroup(vec_c, arrow_c), 0.5*UP))
        self.play(ShowCreation(split_line_1), ShowCreation(split_line_2))
        self.play(LaggedStart(anims1, anims2, anims3, run_time = 1.4, lag_ratio = 0.2), ApplyMethod(symbol.set_color, BLUE), ApplyMethod(matrix.set_color, TEAL)) #而矩阵可以看成多个向量
        self.waiting(0, 24) #（空闲）

        basic_color_map = {r"\det": BLUE, r"\vec{a}": RED, r"\vec{b}": YELLOW, r"\vec{c}": GREEN}
        det_multilinear = MTex(r"\det(\vec{a}, \vec{b}, \vec{c}) = \det(A)", tex_to_color_map = {**basic_color_map, r"A": TEAL}).scale(0.8).shift(3.5*LEFT)
        self.play(ReplacementTransform(notice4, notice5), ApplyMethod(VGroup(determinant, splits).shift, 1.5*RIGHT))
        self.waiting(0, 3) #于是......
        self.play(Write(det_multilinear), lag_ratio = 1, run_time = 1.5)
        self.waiting(2, 13) #行列式就可以看成多个向量到标量的多元函数
        self.waiting(1, 0) #（空闲）
        
        tex_string1_1 = r"\det(k\vec{a}_1+\vec{a}_2, \vec{b}, \vec{c})"
        tex_string1_2 = r"=k\det(\vec{a}_1, \vec{b}, \vec{c})+\det(\vec{a}_2, \vec{b}, \vec{c})"
        tex_string2_1 = r"\det(\vec{a}, k\vec{b}_1+\vec{b}_2, \vec{c})"
        tex_string2_2 = r"=k\det(\vec{a}, \vec{b}_1, \vec{c})+\det(\vec{a}, \vec{b}_2, \vec{c})"
        tex_string3_1 = r"\det(\vec{a}, \vec{b}, k\vec{c}_1+\vec{c}_2)"
        tex_string3_2 = r"=k\det(\vec{a}, \vec{b}, \vec{c}_1)+\det(\vec{a}, \vec{b}, \vec{c}_2)"
        det_linearity = MTex(
        r"\begin{aligned}" + tex_string1_1 + r"&" + tex_string1_2 + r"\\" + tex_string2_1 + r"&" + tex_string2_2 + r"\\" + tex_string3_1 + r"&" + tex_string3_2 + r"\end{aligned}",
        isolate = [r"\det"]).scale(0.8).next_to(det_multilinear.get_corner(LEFT), RIGHT, buff = 0).shift(1.25*DOWN)

        def get_difference(mtex1: MTex, mtex2: MTex, index1: int = 0, index2: int = 0, tex: str = r"\det"):
            return mtex1.select_part(tex, index1).get_center() - mtex2.select_part(tex, index2).get_center()
        
        det_origin_0 = MTex(r"\det(\vec{a}, \vec{b}, \vec{c})", tex_to_color_map = basic_color_map).scale(0.8)
        det_origin_0.shift(get_difference(det_multilinear, det_origin_0))
        def opacity_updater(mob: Mobject):
            height = mob.get_center() - det_origin_0.get_center()
            if height[1] >= 0:
                mob.set_opacity(1)
        det_origin_1 = det_origin_0.copy().shift(get_difference(det_linearity, det_origin_0)).set_opacity(0).add_updater(opacity_updater)
        det_origin_2 = det_origin_0.copy().shift(get_difference(det_linearity, det_origin_0, 3)).set_opacity(0).add_updater(opacity_updater)
        det_origin_3 = det_origin_0.copy().shift(get_difference(det_linearity, det_origin_0, 6)).set_opacity(0).add_updater(opacity_updater)
        
        self.add(det_origin_1, det_origin_2, det_origin_3)
        distance = det_origin_3.get_center() - det_origin_0.get_center()
        self.play(ApplyMethod(VGroup(determinant, splits, det_multilinear).shift, 2.5*UP), ApplyMethod(det_origin_0.shift, distance))
        det_origin_1.clear_updaters()
        det_origin_2.clear_updaters()
        det_origin_3.clear_updaters()
        self.remove(det_origin_0)
        
        self.waiting(1, 9-26) #行列式有很好的性质......
        
        det_multilinear1_1 = MTex(tex_string1_1, tex_to_color_map = {**basic_color_map, (r"\vec{a}_1", r"\vec{a}_2", r"+", r"k"): RED}).scale(0.8)
        det_multilinear1_1.shift(get_difference(det_linearity, det_multilinear1_1, 0))
        det_multilinear1_2 = MTex(tex_string1_2, tex_to_color_map = {**basic_color_map, (r"\vec{a}_1", r"\vec{a}_2", r"+", r"k"): RED}).scale(0.8)
        det_multilinear1_2.shift(get_difference(det_linearity, det_multilinear1_2, 1))
        det_multilinear2_1 = MTex(tex_string2_1, tex_to_color_map = {**basic_color_map, (r"\vec{b}_1", r"\vec{b}_2", r"+", r"k"): YELLOW}).scale(0.8)
        det_multilinear2_1.shift(get_difference(det_linearity, det_multilinear2_1, 3))
        det_multilinear2_2 = MTex(tex_string2_2, tex_to_color_map = {**basic_color_map, (r"\vec{b}_1", r"\vec{b}_2", r"+", r"k"): YELLOW}).scale(0.8)
        det_multilinear2_2.shift(get_difference(det_linearity, det_multilinear2_2, 4))
        det_multilinear3_1 = MTex(tex_string3_1, tex_to_color_map = {**basic_color_map, (r"\vec{c}_1", r"\vec{c}_2", r"+", r"k"): GREEN}).scale(0.8)
        det_multilinear3_1.shift(get_difference(det_linearity, det_multilinear3_1, 6))
        det_multilinear3_2 = MTex(tex_string3_2, tex_to_color_map = {**basic_color_map, (r"\vec{c}_1", r"\vec{c}_2", r"+", r"k"): GREEN}).scale(0.8)
        det_multilinear3_2.shift(get_difference(det_linearity, det_multilinear3_2, 7))
        det_multilinear_first_variable = VGroup(det_multilinear1_1, det_multilinear1_2)
        det_multilinear_others = VGroup(det_multilinear2_1, det_multilinear2_2, det_multilinear3_1, det_multilinear3_2)
        
        anims1 = LaggedStart(ShowCreationThenDestructionAround(det_origin_1.get_part_by_tex(r"\vec{a}")), ShowCreationThenDestructionAround(det_origin_2.get_part_by_tex(r"\vec{b}")), ShowCreationThenDestructionAround(det_origin_3.get_part_by_tex(r"\vec{c}")), lag_ratio = 0.25)
        anims2 = LaggedStart(TransformMatchingStrings(det_origin_1, det_multilinear1_1), TransformMatchingStrings(det_origin_2, det_multilinear2_1), TransformMatchingStrings(det_origin_3, det_multilinear3_1), lag_ratio = 0.25)
        anims3 = LaggedStart(TransformMatchingStrings(det_multilinear1_1.copy(), det_multilinear1_2), TransformMatchingStrings(det_multilinear2_1.copy(), det_multilinear2_2), TransformMatchingStrings(det_multilinear3_1.copy(), det_multilinear3_2), lag_ratio = 1/6)
        self.play(anims1, run_time = 1.5)
        self.play(anims2, run_time = 1.5) #它对于这些向量中的每一个
        self.play(anims3, run_time = 2)
        self.waiting(0, 1) # 都是线性的 （空闲）

        text_multilinear_function = Text("多重线性函数", font = 'simhei')
        text_multilinear_function.rotate(-PI/2).shift(4.9*RIGHT + 0.7*DOWN).set_color(BLUE)
        for i in range (6):
            text_multilinear_function[i].rotate(PI/2, about_point = text_multilinear_function[i].get_corner(LEFT))
        width = text_multilinear_function.get_width()
        right_line = Line(text_multilinear_function.get_corner(UR) + 0.1*UR, text_multilinear_function.get_corner(DR) + 0.1*DR)
        text_multilinear_function.shift(width * RIGHT)
        background = BackgroundRectangle(text_multilinear_function, color = "#333333", fill_opacity = 1)
        
        self.play(ShowCreation(right_line))
        self.waiting(0, 9) #这样的函数
        self.add(text_multilinear_function, background)
        self.bring_to_back(text_multilinear_function, background)
        self.play(ApplyMethod(text_multilinear_function.shift, width*LEFT), rate_func = rush_from, lag_ratio = 0.5, run_time = 1.6)
        self.remove(background)
        self.waiting(2-1.6, 5) #名为多重线性函数
        self.waiting(0, 27) #（空闲）

        
        position = matrix.get_corner(DOWN)
        text_notice_matrix = Text("三维方阵", font = 'simsun', color = YELLOW).scale(0.4).move_to(position + 0.5*DOWN)
        arrow_notice_matrix = Arrow(text_notice_matrix.get_corner(UP), position, buff = 0.1, color = YELLOW)
        notice_matrix = VGroup(text_notice_matrix, arrow_notice_matrix)
        text_notice_multilinear = Text("三重线性函数", font = 'simsun', color = YELLOW).rotate(-PI/2)
        for i in range (6):
            text_notice_multilinear[i].rotate(PI/2, about_point = text_notice_multilinear[i].get_corner(LEFT))
        text_notice_multilinear.scale(0.4).next_to(det_multilinear2_2, RIGHT, buff = 0.4)
        arrow_notice_multilinear_1 = Arrow(det_multilinear1_2.get_corner(RIGHT), text_notice_multilinear.get_corner(UL), buff = 0.11, color = YELLOW)
        arrow_notice_multilinear_2 = Arrow(det_multilinear2_2.get_corner(RIGHT), text_notice_multilinear.get_corner(LEFT), buff = 0.1, color = YELLOW)
        arrow_notice_multilinear_3 = Arrow(det_multilinear3_2.get_corner(RIGHT), text_notice_multilinear.get_corner(DL), buff = 0.11, color = YELLOW)
        notice_multilinear = VGroup(text_notice_multilinear, arrow_notice_multilinear_1, arrow_notice_multilinear_2, arrow_notice_multilinear_3)
        self.waiting(1, 20) #对于行列式而言
        self.play(FadeIn(notice_matrix, 0.5*UP))
        self.waiting(0, 24) #矩阵是几维的
        self.play(FadeIn(notice_multilinear, 0.5*RIGHT))
        self.waiting(1, 10) #它就是几重线性函数
        self.waiting(1, 19) #（空闲）

        partial = MTex(r"{{L_{\vec{b}, \vec{c}}(\vec{a})=}}\det(\vec{a}, {\vec{b}}, {\vec{c}})", tex_to_color_map = {(r"\det", r"L_{\vec{b}, \vec{c}}"): BLUE, r"\vec{a}": RED, r"{\vec{b}}": YELLOW, r"{\vec{c}}": GREEN}, isolate = [r"\vec{b}, \vec{c}"]).scale(0.8)
        partial.shift(get_difference(det_multilinear, partial, 0))
        partial_linear = partial.get_part_by_tex(r"L_{\vec{b}, \vec{c}}(\vec{a})=")
        partial_footnote = partial.get_part_by_tex((r"\vec{b}, \vec{c}"))
        partial_linearity = MTex(
        r"L_{\vec{b}, \vec{c}}(k\vec{a}_1 + \vec{a}_2)=kL_{\vec{b}, \vec{c}}(\vec{a}_1)+L_{\vec{b}, \vec{c}}(\vec{a}_2)", 
        tex_to_color_map = {(r"\det", r"L_{\vec{b}, \vec{c}}"): BLUE, (r"\vec{a}_1", r"\vec{a}_2", r"+", r"k"): RED}
        ).scale(0.8).shift(3*LEFT)

        self.play(FadeIn(partial_linear, 0.5*UP), ApplyMethod(det_multilinear_others.set_color, WHITE), ReplacementTransform(notice5, notice6))
        self.waiting(1, 12) #如果我们只看第一个向量
        self.play(FadeIn(partial_linearity, DOWN), FadeOut(VGroup(det_multilinear_others, notice_multilinear, text_multilinear_function, right_line), DOWN), ApplyMethod(det_multilinear_first_variable.shift, DOWN))
        self.waiting(0, 23) #不看别的向量
        self.waiting(0, 28) #那么......
        self.play(ShowCreationThenDestructionAround(partial_linearity), run_time = 2)
        self.waiting(1, 1) #......这就是一个向量到标量的线性函数
        self.waiting(0, 27) #（空闲）

        distance = 1.8
        text_multiplication = Text("矩阵乘法", font = 'simhei', color = YELLOW_G).shift(distance*RIGHT + 1.7*UP).scale(0.8)
        mtex_multiplication = MTex(r"\vec{u}^\mathrm{T}\vec{v}", tex_to_color_map = {(r"\vec{u}", r"\mathrm{T}"): BLUE, r"\vec{v}": RED}).shift(distance*RIGHT + 1*UP)
        text_linear_function = Text("线性函数", font = 'simhei', color = GREEN).shift(3*distance*RIGHT + 1.7*UP).scale(0.8)
        mtex_linear_function = MTex(r"L(\vec{v})", tex_to_color_map = {r"L": BLUE, r"\vec{v}": RED}).shift(3*distance*RIGHT + 1*UP)
        arrow_linear_mul = ArcBetweenPoints(text_linear_function.get_corner(UL)+0.2*UL, text_multiplication.get_corner(UR)+0.2*UR, angle = PI/3, color = [GREEN, YELLOW_G], tip_config = {"width" : 0.2, "length" : 0.2})
        tip_linear_mul = arrow_linear_mul.create_tip(fill_color = YELLOW_G)
        tip_linear_mul.rotate(-6*DEGREES, about_point = tip_linear_mul.get_tip_point()).rotate(5*DEGREES, about_point = arrow_linear_mul.get_arc_center())
        arrow_mul_linear = ArcBetweenPoints(text_multiplication.get_corner(DR)+0.2*DR, text_linear_function.get_corner(DL)+0.2*DL, angle = PI/3, color = [YELLOW_G, GREEN], tip_config = {"width" : 0.2, "length" : 0.2})
        tip_mul_linear = arrow_mul_linear.create_tip(fill_color = GREEN)
        tip_mul_linear.rotate(-6*DEGREES, about_point = tip_mul_linear.get_tip_point()).rotate(5*DEGREES, about_point = arrow_mul_linear.get_arc_center())
        group_former = VGroup(text_multiplication, mtex_multiplication, text_linear_function, mtex_linear_function, arrow_linear_mul, tip_linear_mul, arrow_mul_linear, tip_mul_linear).shift(7*RIGHT)
        group_former_groupable = VGroup(text_multiplication, mtex_multiplication, text_linear_function, mtex_linear_function, tip_linear_mul, tip_mul_linear)
        background = Rectangle(width = FRAME_WIDTH, height = FRAME_HEIGHT, color = WHITE, stroke_width = 1, fill_opacity = 0)
        board = Rectangle(width = 8.6,  height = 6.5, color = BLACK, stroke_width = 0, fill_opacity = 1).shift(4.8*RIGHT).shift(7*RIGHT)

        self.play(ShowCreationThenDestructionAround(partial_footnote), run_time = 2)
        self.waiting(0, 24) #这个函数和别的向量有关
        self.remove(notice6)
        self.add(background, board, group_former, notice6)
        self.play(ApplyMethod(background.set_opacity, 0.5), ApplyMethod(board.shift, 7*LEFT), ApplyMethod(group_former_groupable.shift, 7*LEFT), ApplyMethod(arrow_linear_mul.shift, 7*LEFT), ApplyMethod(arrow_mul_linear.shift, 7*LEFT), ReplacementTransform(notice6, notice7))
        self.waiting(0, 4) #所以......

        center_position = arrow_linear_mul.get_corner(UP)
        cross_line_1 = Line(0.5*UL, 0.5*DR, color = RED).shift(center_position)
        cross_line_2 = Line(0.5*UR, 0.5*DL, color = RED).shift(center_position)
        cross = VGroup(cross_line_1, cross_line_2)
        self.play(ShowCreation(cross_line_1), rate_func=rush_into, run_time = 0.5)
        self.play(ShowCreation(cross_line_2), rate_func=rush_from, run_time = 0.5)
        self.waiting(1, 21) #我们没法具体写出它对应的矩阵
        self.waiting(1, 4) #（空闲）

        underbase = VGroup(partial, partial_linearity, det_multilinear_first_variable, notice_matrix, determinant, splits, det_multilinear)
        self.remove(background, board, group_former, cross, underbase)
        levi_civita = MTex(r"\text{Levi-Civita符号：}\epsilon_{{i}jk}=\frac{({i}-j)(j-k)(k-{i})}{2}=\begin{cases}1, &{i}jk\text{是偶排列}\\-1, &{i}jk\text{是奇排列}\\0, &\text{其它情况}\end{cases}", tex_to_color_map = {(r"\epsilon", r"{i}", r"j", r"k"): BLUE_P, (r"2", r"1", r"-1", r"0"): RED_P}).scale(0.8).shift(0.5*UP)
        tensor_determinant = MTex(r"\det(\vec{a}, \vec{b}, \vec{c}) = \epsilon_{ijk}a^ib^jc^k", tex_to_color_map = {**basic_color_map, r"a^i": RED, r"b^j":YELLOW, r"c^k":GREEN, r"\epsilon_{ijk}": BLUE_P}).scale(0.8).shift(1*DOWN)
        tensor_partial = MTex(r"L_{\vec{b}, \vec{c}}(\vec{a})=\langle \epsilon^{ijk}b_jc_k, a^i\rangle", tex_to_color_map = {(r"L_{\vec{b}, \vec{c}}", r"\epsilon^{ijk}b_jc_k"): BLUE, (r"\vec{a}", r"a^i"): RED}).scale(0.8).shift(2*DOWN)
        mtexes_tensor = VGroup(levi_civita, tensor_determinant, tensor_partial)

        partial_linearity.shift(3*UP + 4.5*RIGHT)
        partial.shift(get_difference(partial_linearity, partial, tex = r"L_{\vec{b}, \vec{c}}") + 4.5*LEFT)
        anim = Write(levi_civita).update_config(run_time = 3, lag_ratio = 1)
        self.play(ReplacementTransform(notice7, notice8), anim)
        self.play(Write(tensor_determinant), run_time = 1, lag_ratio = 1)
        self.play(Write(tensor_partial), run_time = 1, lag_ratio = 1)
        self.waiting(2+2-5, 23+28) #额......实际上可以 不过要用到张量的语言来描述
        self.waiting(0, 21) #在这里......
        self.play(FadeOut(mtexes_tensor, DOWN), FadeIn(partial), FadeIn(partial_linearity))
        self.waiting(0, 9) #......就不展开了
        self.waiting(1, 9) #（空闲）

        board = Rectangle(width = 10,  height = 6.5, color = BLACK, stroke_width = 0, fill_opacity = 1).next_to(FRAME_HEIGHT/2*DOWN, UP, buff = 0)
        tex_string1 = r"在域$\mathrm{F}$上的线性空间$\mathrm{V}$中，\\"
        tex_string2_0 = r"对于"
        tex_string2 = r"任意一个线性函数$L: \mathrm{V}\to \mathrm{F}$，\\"
        tex_string3 = r"若$\mathrm{V}$上定义了内积$\langle\cdot, \cdot\rangle: \mathrm{V}\times \mathrm{V}\to \mathrm{F}$，则\\"
        tex_string4_0 = r"存在一个"
        tex_string4 = r"向量$\vec{u}=\vec{u}(L)\in \mathrm{V}$，\\"
        tex_string5_0 = r"使得对于任意向量"
        tex_string5 = r"$\vec{v}\in \mathrm{V}$，有"
        tex_string6 = r"$$\langle\vec{u}, \vec{v}\rangle=L(\vec{v}),$$"
        tex_string7_0 = r"其中"
        tex_string7 = r"$\vec{u}$被称为$L$的对偶向量。"
        mtex_theorem = MTexText(
            tex_string1 + tex_string2_0 + tex_string2 + tex_string3 + tex_string4_0 + tex_string4 + tex_string5_0 + tex_string5 + tex_string6 + tex_string7_0 + tex_string7, 
        alignment="", isolate = [tex_string2, r"任意", tex_string4, tex_string5, tex_string6, r"对偶向量", tex_string7_0, tex_string7], 
        tex_to_color_map = {(r"\vec{u}", r"L"): BLUE, r"\vec{v}": RED, r"\mathrm{F}": BLUE_P, r"\mathrm{V}": RED_P}
        ).scale(0.8).move_to(board.get_center() + 0.4*UP + 0.75*LEFT)
        theorem_linear = mtex_theorem.get_part_by_tex(tex_string2)
        theorem_any = mtex_theorem.get_part_by_tex(r"任意")
        theorem_dual = mtex_theorem.get_part_by_tex(tex_string4)
        theorem_vec = mtex_theorem.get_part_by_tex(tex_string5)
        theorem_formula = mtex_theorem.get_part_by_tex(tex_string6)
        theorem_formula.shift((theorem_formula.get_center()[0] + board.get_center()[0])*LEFT + 0.1*UP)
        _ = mtex_theorem.get_part_by_tex(tex_string7_0).shift(0.2*UP)
        theorem_name = mtex_theorem.get_part_by_tex(tex_string7).shift(0.2*UP)
        anim1 = FadeIn(VGroup(board, mtex_theorem), 6.5*UP)
        anim1.update_config(run_time = 2)
        self.play(anim1, ReplacementTransform(notice8, notice9))
        self.waiting(2, 14) #但对偶性原理并不依赖于矩阵写不写得出来
        self.play(ShowCreationThenDestructionAround(theorem_any), run_time = 2)
        self.waiting(1, 10) #它对任意线性函数都成立

        replace_linear = MTexText(r"线性函数$L(\cdot, \cdot, \cdot)=L_{\cdot,\cdot}(\cdot): (\mathrm{V}\times \mathrm{V})\times \mathrm{V}\to \mathrm{F}$，",tex_to_color_map = {(r"L", r"L_{\cdot,\cdot}"): BLUE, r"\vec{v}": RED, r"\mathrm{F}": BLUE_P, r"\mathrm{V}": RED_P}, isolate= [r"L(\cdot, \cdot, \cdot)"]).scale(0.8)
        replace_linear.next_to(theorem_linear.get_corner(UL), DR, buff = 0)
        shade_1 = BackgroundRectangle(replace_linear, color = "#666666", fill_opacity = 1, buff = 0.05).shift(0.05*RIGHT)
        under_shade_1 = shade_1.copy().set_width(0, stretch=True).next_to(shade_1.get_corner(LEFT), RIGHT, buff = 0)
        shade_target_1 = shade_1.copy().set_width(0, stretch=True).next_to(shade_1.get_corner(RIGHT), LEFT, buff = 0)
        self.add(under_shade_1)
        self.play(Transform(under_shade_1, shade_1))
        self.waiting(1, 0)
        self.add(replace_linear, shade_1)
        under_shade_1.set_color("#333333")
        self.play(Transform(shade_1, shade_target_1))
        self.remove(shade_1)
        self.waiting(1, 3) #既然这个函数和b与c有关

        replace_dual = MTexText(r"向量函数$\vec{u}(\cdot, \cdot) : \mathrm{V}\times \mathrm{V}\to \mathrm{V}$，",tex_to_color_map = {r"\vec{u}": BLUE, r"\vec{v}": RED, r"\mathrm{F}": BLUE_P, r"\mathrm{V}": RED_P}, isolate = [r"\vec{u}(\cdot, \cdot)"]).scale(0.8)
        replace_dual.next_to(theorem_dual.get_corner(UL), DR, buff = 0)
        shade_2 = BackgroundRectangle(replace_dual, color = "#666666", fill_opacity = 1, buff = 0.05).shift(0.05*RIGHT)
        under_shade_2 = shade_2.copy().set_width(0, stretch=True).next_to(shade_2.get_corner(LEFT), RIGHT, buff = 0)
        shade_target_2 = shade_2.copy().set_width(0, stretch=True).next_to(shade_2.get_corner(RIGHT), LEFT, buff = 0)
        replace_vec = MTexText(r"$\vec{v},\,\vec{b},\,\vec{c} \in \mathrm{V}$，有",tex_to_color_map = {r"\vec{v}": RED, r"\vec{b}": YELLOW, r"\vec{c}": GREEN, r"\mathrm{V}": RED_P}).scale(0.8)
        replace_vec.next_to(theorem_vec.get_corner(UL), DR, buff = 0)
        shade_3 = BackgroundRectangle(replace_vec, color = "#666666", fill_opacity = 1, buff = 0.05)
        under_shade_3 = shade_3.copy().set_width(0, stretch=True).next_to(shade_3.get_corner(LEFT), RIGHT, buff = 0)
        shade_target_3 = shade_3.copy().set_width(0, stretch=True).next_to(shade_3.get_corner(RIGHT), LEFT, buff = 0)
        replace_formula = MTex(r"\langle\,\vec{u}(\vec{b}, \vec{c}),\,\vec{v}\,\rangle=L_{\vec{b},\,\vec{c}}(\vec{v})",tex_to_color_map = {(r"\vec{u}", r"L"): BLUE, r"\vec{v}": RED, r"\vec{b}": YELLOW, r"\vec{c}": GREEN}, isolate = [r"\vec{u}(\vec{b}, \vec{c})"]).scale(0.8)
        replace_formula.next_to(theorem_formula.get_corner(DOWN), UP, buff = 0)
        shade_4 = BackgroundRectangle(replace_formula, color = "#666666", fill_opacity = 1, buff = 0.05)
        under_shade_4 = shade_4.copy().set_width(0, stretch=True).next_to(shade_4.get_corner(LEFT), RIGHT, buff = 0)
        shade_target_4 = shade_4.copy().set_width(0, stretch=True).next_to(shade_4.get_corner(RIGHT), LEFT, buff = 0)

        def less_smooth(t):
            return t**2 * (3-2*t)

        self.play(Transform(under_shade_2, shade_2), run_time = 2/3, rate_func = less_smooth)
        self.play(Transform(under_shade_3, shade_3), run_time = 2/3, rate_func = less_smooth)
        self.play(Transform(under_shade_4, shade_4), run_time = 2/3, rate_func = less_smooth)
        self.waiting(1, 0)
        self.add(replace_dual, shade_2, replace_vec, shade_3, replace_formula, shade_4)
        under_shade_2.set_color("#333333")
        under_shade_3.set_color("#333333")
        under_shade_4.set_color("#333333")
        self.play(Transform(shade_2, shade_target_2), run_time = 2/3, rate_func = less_smooth)
        self.play(Transform(shade_3, shade_target_3), run_time = 2/3, rate_func = less_smooth)
        self.play(Transform(shade_4, shade_target_4), run_time = 2/3, rate_func = less_smooth)
        self.remove(shade_2, shade_3, shade_4)

        self.waiting(1, 3) #那么现在的u就变成了一个关于b与c的函数

        self.play(ShowCreationThenDestructionAround(replace_vec.get_part_by_tex(r"\vec{b}")), ShowCreationThenDestructionAround(replace_vec.get_part_by_tex(r"\vec{c}")), run_time = 1)
        self.waiting(0, 9)
        self.play(ShowCreationThenDestructionAround(replace_formula.get_part_by_tex(r"\vec{u}(\vec{b}, \vec{c})")))
        self.waiting(2, 7) #从两个向量到一个向量的二重线性函数
        self.waiting(1, 9) #（空闲）

        self.waiting(2, 29) #这就是对偶性的不平凡之处
        self.waiting(0, 9) #它将......
        self.play(ShowCreationThenDestructionAround(replace_linear.get_part_by_tex(r"L(\cdot, \cdot, \cdot)")))
        self.waiting(0, 24) #......多重线性函数变成一种......
        self.play(ShowCreationThenDestructionAround(replace_dual.get_part_by_tex(r"\vec{u}(\cdot, \cdot)")))
        self.waiting(0, 16) #......新的向量运算
        self.waiting(0, 26) #（空闲）

        self.waiting(1, 19) #这个新的运算
        self.play(ShowCreationThenDestructionAround(mtex_theorem.get_part_by_tex(r"对偶向量")), run_time = 2)
        self.waiting(1, 9) #依然被称作多重线性函数的“对偶向量”......

        replace_name = MTexText(r"$L(\hat{v}, \vec{b}, \vec{c}) = \vec{u}(\vec{b}, \vec{c})$被称为$L$关于$\vec{v}$的对偶向量。",tex_to_color_map = {(r"L", r"\vec{u}"): BLUE, (r"\vec{v}", r"\hat{v}"): RED, r"\vec{b}": YELLOW, r"\vec{c}": GREEN}).scale(0.8)
        replace_name.next_to(theorem_name.get_corner(LEFT), RIGHT, buff = 0)
        shade_5 = BackgroundRectangle(replace_name, color = "#666666", fill_opacity = 1, buff = 0.05).shift(0.05*RIGHT)
        under_shade_5 = shade_5.copy().set_width(0, stretch=True).next_to(shade_5.get_corner(LEFT), RIGHT, buff = 0)
        shade_target_5 = shade_5.copy().set_width(0, stretch=True).next_to(shade_5.get_corner(RIGHT), LEFT, buff = 0)
        self.add(under_shade_5)
        self.play(Transform(under_shade_5, shade_5))
        self.add(replace_name, shade_5)
        under_shade_5.set_color("#333333")
        self.play(Transform(shade_5, shade_target_5))
        self.remove(shade_5)
        self.play(ShowCreationThenDestructionAround(replace_name.get_part_by_tex(r"\hat{v}")), run_time = 1)
        self.waiting(0, 33) #......（空闲） 有的时候会用^这个记号来表示

        self.waiting(0, 19)
        grafted_mtex_theorem = VGroup(board, mtex_theorem, under_shade_1, under_shade_2, under_shade_3, under_shade_4, under_shade_5, replace_linear, replace_dual, replace_vec, replace_formula, replace_name)
        self.play(FadeOut(grafted_mtex_theorem, DOWN), FadeOut(partial_linearity, UP), FadeOut(partial, UP)) #（空闲）

        tex_string1 = r"\det(\hat{a}, \vec{b}, \vec{c}) = \vec{u}(\vec{b}, \vec{c})"
        tex_string2 = r"= \vec{b}\times \vec{c}"
        det_dual_3 = MTex(tex_string1 + tex_string2, tex_to_color_map = {(r"\det", r"\vec{u}"): BLUE, r"\hat{a}": RED, r"\vec{b}": YELLOW, r"\vec{c}": GREEN}, isolate = [tex_string1, tex_string2, r")"]).scale(0.8).shift(1*UP)
        det_dual_3_left = det_dual_3.get_part_by_tex(tex_string1)
        det_dual_3_right = det_dual_3.get_part_by_tex(tex_string2)
        tex_string1 = r"\det(\hat{a}, \vec{b}) = \vec{u}(\vec{b})"
        tex_string2 = r"= \begin{bmatrix}0&1\\-1&0\end{bmatrix}\vec{b}"
        det_dual_2 = MTex(tex_string1 + tex_string2, tex_to_color_map = {(r"\det", r"\vec{u}", r"0", r"1", r"-1"): BLUE, r"\hat{a}": RED, r"\vec{b}": YELLOW}, isolate = [tex_string1, tex_string2, r")"]).scale(0.8)
        det_dual_2.shift(get_difference(det_dual_3, det_dual_2, 1, 1, r")") + 1.5*UP)
        det_dual_2_left = det_dual_2.get_part_by_tex(tex_string1)
        det_dual_2_right = det_dual_2.get_part_by_tex(tex_string2)
        det_dual_4 = MTex(r"\det(\hat{a}, \vec{b}, \vec{c}, \vec{d}) = \vec{u}(\vec{b}, \vec{c}, \vec{d})", tex_to_color_map = {(r"\det", r"\vec{u}"): BLUE, r"\hat{a}": RED, r"\vec{b}": YELLOW, r"\vec{c}": GREEN, r"\vec{d}": TEAL}, isolate = [r")"]).scale(0.8)
        det_dual_4.shift(get_difference(det_dual_3, det_dual_4, 1, 1, r")") + 1.5*DOWN)
        det_dual_5 = MTex(r"\det(\hat{v}_1, \vec{v}_2, \vec{v}_3, \cdots, \vec{v}_n) = \vec{u}(\vec{v}_2, \vec{v}_3, \cdots, \vec{v}_n)", tex_to_color_map = {(r"\det", r"\vec{u}"): BLUE, r"\hat{v}_1": RED, r"\vec{v}_2": YELLOW, r"\vec{v}_3": GREEN, r"\vec{v}_n": TEAL}, isolate = [r")"]).scale(0.8)
        det_dual_5.shift(get_difference(det_dual_3, det_dual_5, 1, 1, r")") + 3*DOWN)
        group_det_dual = VGroup(det_dual_2, det_dual_3, det_dual_4, det_dual_5)

        self.play(ReplacementTransform(notice9, notice10), FadeIn(det_dual_3_left, RIGHT))
        self.waiting(1, 10) #三阶行列式的对偶向量
        self.play(FadeIn(det_dual_3_right, LEFT))
        self.waiting(0, 26) #一般被称作叉积
        self.waiting(1, 3) #（空闲）

        self.play(FadeIn(det_dual_2_left, RIGHT))
        self.waiting(2, 28) #二阶行列式的对偶向量是一个一元运算
        self.play(FadeIn(det_dual_2_right, LEFT))
        self.waiting(3, 8) #这个一元运算 等价于将向量旋转90度
        self.waiting(1, 9) #（空闲）

        self.play(FadeIn(det_dual_4, RIGHT))
        self.waiting(2, 7) #四阶行列式的对偶向量是一个三元运算
        self.waiting(0, 26) #（空闲）

        self.waiting(1, 12) #一般地......
        self.play(FadeIn(det_dual_5, RIGHT))
        self.waiting(2, 16) #n阶行列式的对偶向量是一个n-1元运算
        self.waiting(0, 27) #（空闲）

        mtex_checkmark_3 = MTex(r"\checkmark", color = GREEN).scale(0.8).next_to(det_dual_3, LEFT)
        mtex_checkmark_2 = mtex_checkmark_3.copy().next_to(det_dual_2, LEFT)
        mtex_checkmark_4 = mtex_checkmark_3.copy().next_to(det_dual_4, LEFT)
        mtex_checkmark_5 = mtex_checkmark_3.copy().next_to(det_dual_5, LEFT)
        mtex_chechmarks = VGroup(mtex_checkmark_2, mtex_checkmark_3, mtex_checkmark_4, mtex_checkmark_5)
        text_judge_3 = mtex_checkmark_3.copy().next_to(det_dual_3, RIGHT)
        text_judge_2 = Text(r"✗", font = "simsun", color = RED).scale(0.8).next_to(det_dual_2, RIGHT)
        text_judge_4 = text_judge_2.copy().next_to(det_dual_4, RIGHT)
        text_judge_5 = text_judge_2.copy().next_to(det_dual_5, RIGHT)
        text_judges = VGroup(text_judge_2, text_judge_3, text_judge_4, text_judge_5)
        cross_product = VGroup(det_dual_3, mtex_checkmark_3, text_judge_3)

        self.waiting(1, 18) #如果我们将叉积 定义为......
        self.play(Write(mtex_chechmarks), run_time = 1.5)
        self.waiting(1, 10) #......定义为行列式的对偶向量
        self.play(Write(text_judges), run_time = 1.5)
        self.waiting(1, 15) #并且要求叉积是二元运算

        self.waiting(1, 1) #那么......
        self.play(ShowCreationThenDestructionAround(cross_product), run_time = 2)
        self.waiting(0, 16) #......只有三维空间存在叉积

        self.waiting(0, 27)
        self.play(FadeOut(VGroup(group_det_dual, mtex_chechmarks, text_judges), DOWN)) #（空闲）

        mtex_winograd = MTex(r"\vec{a}*\vec{b}=\vec{u}_1(\vec{a}, \vec{b}) &= T(\vec{a}, \vec{b}, \hat{c})\\\vec{c}\ \dot{*}\ \vec{b} = \vec{u}_2(\vec{c}, \vec{b})&= T(\hat{a}, \vec{b}, \vec{c})")
        self.play(ReplacementTransform(notice10, notice11), Write(mtex_winograd))
        self.waiting(0, 4) #在了解了对偶性以后
        self.waiting(3, 6) #我们就有能力理解Winograd算法了

        self.waiting(2, 29)
        self.play(FadeOut(mtex_winograd, 0.5*DOWN), FadeOut(notice11))
        self.waiting(3, 0) #到此共150秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_0(Scene):
    
    def construct(self):

        ##  Making object
        text3 = Text("第三节　Winograd算法", font = 'simsun', t2c={"第三节": YELLOW, "Winograd": GREEN, "算法": BLUE})

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(Scene):
    
    def construct(self):
        notice1 = Notice("前情提要", "请　复习")
        notice2 = Notice("奇妙思路", "请　模仿")
        notice3 = Notice("繁冗计算", "请　选做*")
        notice4 = Notice("奇妙思路", "请　模仿")
        notice5 = Notice("推导完毕", "请　鼓掌")

        mtex_convolution = MTex(r"\vec{a}*\vec{b} = \vec{c}", isolate = [r"="], tex_to_color_map = {r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW}).scale(0.8).shift(2*UP + 2*RIGHT)
        tex_string1 = r"\begin{bmatrix}a_0\\a_1\\a_2\\a_3\end{bmatrix}"
        tex_string2 = r"\begin{bmatrix}b_0\\b_1\\b_2\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}c_0\\c_1\\c_2\\c_3\\c_4\\c_5\end{bmatrix}"
        mtex_convolution_vec = MTex(tex_string1 + r"*" + tex_string2+ r"=" + tex_string3, tex_to_color_map = {re.compile(r"a_."): BLUE, re.compile(r"b_."): RED, re.compile(r"c_."): YELLOW}).scale(0.8).shift(2*UP + 3*LEFT)
        vec_a = mtex_convolution_vec.get_part_by_tex(tex_string1)
        vec_b = mtex_convolution_vec.get_part_by_tex(tex_string2)
        vec_c = mtex_convolution_vec.get_part_by_tex(tex_string3)
        self.play(FadeIn(mtex_convolution, 0.5*DOWN), FadeIn(mtex_convolution_vec, 0.5*DOWN), Write(notice1))
        self.waiting(2, 1) #我们来重新审视一下离散卷积

        mtex_multilinear_1 = MTex(r"(k\vec{a}_1+\vec{a}_2)*\vec{b} = k\vec{a}_1*\vec{b}+\vec{a}_2*\vec{b}", tex_to_color_map = {(r"\vec{a}_1", r"\vec{a}_2"): BLUE, (r"k", r"+"): TEAL, r"\vec{b}": RED}).scale(0.8).shift(0.5*DOWN + 3*LEFT)
        mtex_multilinear_2 = MTex(r"\vec{a}*(k\vec{b}_1+\vec{b}_2) = k\vec{a}*\vec{b}_1+\vec{a}*\vec{b}_2", tex_to_color_map = {r"\vec{a}": BLUE, (r"k", r"+"): ORANGE, (r"\vec{b}_1", r"\vec{b}_2"): RED}).scale(0.8).shift(1.3*DOWN + 3*LEFT)
        group_multilinear = VGroup(mtex_multilinear_1, mtex_multilinear_2)
        self.play(FadeIn(group_multilinear, 0.5*RIGHT))
        self.waiting(1, 2) #它是一个二重线性函数

        anims1 = [Indicate(mtex) for mtex in vec_a]
        anims2 = [Indicate(mtex) for mtex in vec_b]
        anims3 = [Indicate(mtex) for mtex in vec_c]
        self.play(LaggedStart(*anims1, lag_ratio = 0.1, run_time = 1.5), LaggedStart(*anims2, lag_ratio = 0.1, run_time = 1.5))
        self.play(LaggedStart(*anims3, lag_ratio = 0.1, run_time = 1.5))
        self.waiting(2+0-3, 14+25) #把两个向量映射成一个向量 （空闲）

        picture_winograd = ImageMobject("picture_winograd.jpg", height = 4).shift(5*RIGHT + 0.5*DOWN)
        self.play(FadeIn(picture_winograd, UP), ReplacementTransform(notice1, notice2))
        self.waiting(1, 27) #Winograd考虑了这么一个问题

        def get_difference(mtex1: MTex, mtex2: MTex, index1: int = 0, index2: int = 0, tex: str = r"="):
            return mtex1.select_part(tex, index1).get_center() - mtex2.select_part(tex, index2).get_center()

        mtex_dual = MTex(r"\vec{a}*\vec{b} = L(\vec{a}, \vec{b}, \hat{c})", isolate = [r"="], tex_to_color_map = {r"\vec{a}": BLUE, r"\vec{b}": RED, r"\hat{c}": YELLOW, r"L": PURPLE}).scale(0.8)
        mtex_dual.shift(get_difference(mtex_convolution, mtex_dual)+0.8*UP)
        mtex_multilinear = MTex(r"L(\vec{a}, \vec{b}, \vec{c}) =\ ?", isolate = [r"L(\vec{a}, \vec{b}, \vec{c}) =", r"=", r"?"], tex_to_color_map = {r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW, r"L": PURPLE}).scale(0.8)
        mtex_multilinear.shift(get_difference(mtex_convolution, mtex_multilinear)+0.8*DOWN)
        multilinear_function = mtex_multilinear.get_part_by_tex(r"L(\vec{a}, \vec{b}, \vec{c}) =")
        multilinear_others = mtex_multilinear.get_part_by_tex(r"?")

        self.play(Write(mtex_dual), run_time = 1.5, lag_ratio = 1)
        self.waiting(2, 3) #如果卷积是一个三重线性函数的对偶向量
        self.play(FadeIn(mtex_multilinear, 0.5*DOWN))
        self.waiting(2, 12) #那么这个三重线性函数应该是什么

        self.waiting(0, 8)
        self.play(FadeOut(group_multilinear, DOWN), FadeOut(picture_winograd, DOWN)) #（空闲）

        mtex_winograd_function = MTex(r"\vec{c}=S\left({{}P}{(}\vec{a}{)}\odot P{(}\vec{b}{)}\right)", isolate = [r"=", r"{(}", r"{)}"], tex_to_color_map = {r"\vec{c}":YELLOW, r"S": GREEN, (r"{{}P}", r"P"): PURPLE_A, r"\vec{a}": BLUE, r"\vec{b}": RED}).scale(0.8).shift(0.5*DOWN + 3*LEFT)
        function_p_1 = mtex_winograd_function.select_part(r"P", 0)
        function_p_2 = mtex_winograd_function.select_part(r"P", 1)
        function_s = mtex_winograd_function.select_part(r"S")
        mtex_winograd_matrix = MTex(r"\vec{c}=S_c\left(P_a\vec{a}\odot P_b\vec{b}\right)", isolate = [r"="], tex_to_color_map = {r"\vec{c}":YELLOW, r"S_c": GREEN, (r"P_a", r"P_b"): PURPLE_A, r"\vec{a}": BLUE, r"\vec{b}": RED}).scale(0.8).shift(0.5*DOWN + 3*LEFT)
        mtex_winograd_matrix.shift(get_difference(mtex_winograd_function, mtex_winograd_matrix))
        self.play(Write(mtex_winograd_function), lag_ratio = 1, run_time = 1.5)
        self.waiting(3, 1) #我们在第一节里面把Winograd算法写成过变换的形式
        self.play(ShowCreationThenDestructionAround(function_p_1), ShowCreationThenDestructionAround(function_p_2), run_time = 2)
        self.waiting(0, 15) #从系数到取值的变换P
        self.waiting(0, 10) #和......
        self.play(ShowCreationThenDestructionAround(function_s), run_time = 2)
        self.waiting(0, 22) #和从取值到系数的变换S
        self.waiting(1, 25) #都是线性函数
        self.waiting(0, 17) #于是......
        self.play(TransformMatchingStrings(mtex_winograd_function, mtex_winograd_matrix, key_map = {r"S": r"S_c", r"{{}P}": r"P_a", r"P":r"P_b"}))
        self.waiting(0, 21) #它们都可以写成矩阵
        self.waiting(0, 26) #（空闲）

        PURPLES = [interpolate_color(BLUE, PURPLE, 2/7), interpolate_color(BLUE, PURPLE, 4/7), interpolate_color(BLUE, PURPLE, 6/7), interpolate_color(RED, PURPLE, 6/7), interpolate_color(RED, PURPLE, 4/7), interpolate_color(RED, PURPLE, 2/7)]
        mtex_matrix_p_1 = MTex(
        r"P_a=\begin{bmatrix}{{1}}&x_1&x_1^2&x_1^3\\{{1}}&x_2&x_2^2&x_2^3\\{{1}}&x_3&x_3^2&x_3^3\\{{1}}&x_4&x_4^2&x_4^3\\{{1}}&x_5&x_5^2&x_5^3\\{{1}}&x_6&x_6^2&x_6^3\end{bmatrix}",
        tex_to_color_map = {r"P_a": PURPLE_A, (r"x_1", r"x_1^2", r"x_1^3"): PURPLES[0], (r"x_2", r"x_2^2", r"x_2^3"): PURPLES[1], (r"x_3", r"x_3^2", r"x_3^3"): PURPLES[2], (r"x_4", r"x_4^2", r"x_4^3"): PURPLES[3], (r"x_5", r"x_5^2", r"x_5^3"): PURPLES[4], (r"x_6", r"x_6^2", r"x_6^3"): PURPLES[5]},
        ).scale(0.8).shift(DOWN + 2*RIGHT)
        for i in range (6):
            mtex_matrix_p_1.select_part(r"1", i).set_color(PURPLES[i])

        self.play(FadeIn(mtex_matrix_p_1, RIGHT))
        self.waiting(1, 18) #矩阵P的每一项都是方幂
        self.waiting(2, 15) #这样的矩阵被称作范德蒙矩阵
        self.waiting(0, 22) #（空闲）

        mtex_matrix_s = MTex(r"S_c = P_c^{-1}", isolate = [r"="], tex_to_color_map = {r"S_c": GREEN, r"P_c": PURPLE_A}).scale(0.8).shift(0.5*DOWN)
        mtex_term_s = MTex(
        r"{S_c}_{(i, j)}=\frac{(-1)^{n-i}\sigma_{{n-i}}^{(j)}}{\prod_{k\ne j}(x_k-x_j)}", 
        isolate = [r"="], tex_to_color_map = {r"S_c": GREEN, (r"\sigma", r"{{n-i}}"): ORANGE, (r"x_k", r"x_j"): GREEN_E}
        ).scale(0.8)
        mtex_term_s.next_to(mtex_matrix_s.get_corner(RIGHT), LEFT, buff = 0).shift(1.2*DOWN)

        tex_string1 = r"h(x)=&\sum_jh(x_j)\prod_{k\ne j}\frac{x-x_j}{x_k-x_j}\\"
        tex_string2 = r"=&\sum_jh(x_j)\frac{\sum_i(-1)^{n-i}\sigma_{n-i}x^i}{\prod_{k\ne j}(x_k-x_j)}\\"
        tex_string3 = r"=&\sum_i\sum_jx^i\frac{(-1)^{n-i}\sigma_{n-i}^{(j)}}{\prod_{k\ne j}(x_k-x_j)}h(x_j)"
        tex_string3_0 = r"\frac{(-1)^{n-i}\sigma_{n-i}^{(j)}}{\prod_{k\ne j}(x_k-x_j)}"
        mtex_interpolation = MTex(
        tex_string1 + tex_string2 + tex_string3, 
        tex_to_color_map = {tex_string3_0: GREEN}
        ).scale(0.6).shift(DOWN + 4*RIGHT)
        surrounding = SurroundingRectangle(mtex_interpolation, buff = 0.3)

        self.play(FadeOut(mtex_matrix_p_1, RIGHT), FadeIn(mtex_matrix_s, RIGHT))
        self.waiting(2, 3) #矩阵S是范德蒙矩阵的逆矩阵
        self.play(FadeIn(mtex_term_s, RIGHT))
        self.waiting(1, 7) #展开形式比较复杂
        self.play(ShowCreation(surrounding), ReplacementTransform(notice2, notice3))
        self.play(Write(mtex_interpolation), lag_ratio = 1, run_time = 3)
        self.waiting(1+2-4, 18+24) #大家如果有兴趣 可以拿拉格朗日插值法算一算
        self.play(FadeOut(VGroup(mtex_interpolation, surrounding, mtex_term_s), DOWN), ReplacementTransform(notice3, notice4))
        self.waiting(1, 9) #这里为了方便就不展开了
        self.play(FadeOut(mtex_matrix_s, LEFT))
        self.waiting(0, 21) #还是用S来表示
        self.waiting(1, 3) #（空闲）

        tex_string0 = r"L(\vec{a}, \vec{b}, \vec{c})"
        tex_string1 = r"\vec{c}\cdot\left(S_c\left(P_a\vec{a}\odot P_b\vec{b}\right)\right)"
        tex_string2 = r"=\vec{c}^\mathrm{T}S_c\left(P_a\vec{a}\odot P_b\vec{b}\right)"
        tex_string3 = r"=(S_c^\mathrm{T}\vec{c})\cdot\left(P_a\vec{a}\odot P_b\vec{b}\right)"
        tex_string4 = r"=\langle\,P_a\vec{a},\,P_b\vec{b},\,S_c^\mathrm{T}\vec{c}\,\rangle"
        mtex_calculate = MTex(
        tex_string0 + r"&=" + tex_string1 + r"\\&" + tex_string2 + r"\\&" + tex_string3 + r"\\&" + tex_string4, 
        isolate = [tex_string0, r"=", tex_string1, tex_string2, tex_string3, tex_string4, r"\odot"], 
        tex_to_color_map = {r"L": PURPLE, r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW, r"S_c": GREEN, (r"P_a", r"P_b"): PURPLE_A}, 
        ).scale(0.8)
        mtex_calculate.shift(get_difference(mtex_multilinear, mtex_calculate) + LEFT)
        calculate_function = VGroup(mtex_calculate.get_part_by_tex(tex_string0), mtex_calculate.select_part(r"=", 0))
        calculate_dot = mtex_calculate.get_part_by_tex(tex_string1)
        calculate_multiply = mtex_calculate.get_part_by_tex(tex_string2)
        calculate_transpose = mtex_calculate.get_part_by_tex(tex_string3)
        calculate_result = mtex_calculate.get_part_by_tex(tex_string4)
        calculate_p_a = mtex_calculate.select_part(r"P_a\vec{a}", 2)
        calculate_p_b = mtex_calculate.select_part(r"P_b\vec{b}", 2)
        calculate_odot = mtex_calculate.select_part(r"\odot", 2)
        
        self.play(ShowCreationThenDestructionAround(mtex_dual), run_time = 2)
        self.waiting(0, 23) #把卷积视为一个对偶向量的话
        self.play(ApplyMethod(multilinear_function.shift, LEFT), FadeOut(multilinear_others, LEFT))
        self.remove(multilinear_function)
        self.add(calculate_function)
        self.waiting(1, 1) #它对应的三重线性函数
        self.play(Write(calculate_dot), run_time = 2, lag_ratio = 1)
        self.waiting(1, 16) #就应该是卷积和第三个向量c的点乘
        self.waiting(0, 19) #（空闲）
        self.play(Write(calculate_multiply), run_time = 2, lag_ratio = 1)
        self.waiting(1, 15) #这个时候使用矩阵的优势就体现出来了
        self.play(Write(calculate_transpose), run_time = 2, lag_ratio = 1)
        self.waiting(1, 3) #S可以通过取转置与c结合
        self.waiting(0, 17) #（空闲）


        hint_odot = MTex(r"(\vec{u}\odot\vec{v}=\begin{bmatrix}u_1v_1\\u_2v_2\\\vdots\\u_nv_n\end{bmatrix})", tex_to_color_map = {(r"\vec{u}", re.compile(r"u_.")): BLUE_P, (r"\vec{v}", re.compile(r"v_.")): RED_P}).scale(0.8).shift(1.5*DOWN + LEFT)
        hint_triple = MTex(r"(\langle\,\vec{u},\,\vec{v},\,\vec{w}\,\rangle = \sum_{i=1}^nu_iv_iw_i)", tex_to_color_map = {(r"\vec{u}", r"u_i"): BLUE_E, (r"\vec{v}", r"v_i"): RED_E, (r"\vec{w}", r"w_i"): YELLOW_E}).scale(0.8).shift(1.5*DOWN + 1.5*LEFT)
        
        self.play(ShowCreationThenDestructionAround(calculate_p_a), ShowCreationThenDestructionAround(calculate_p_b), run_time = 2)
        self.waiting(0, 18) #而a和b变换成的两个向量
        anim = ShowCreationThenDestructionAround(calculate_odot)
        anim.update_config(run_time = 2)
        self.play(anim, FadeIn(hint_odot, UP))
        self.waiting(0, 24) #它们的分量分别乘了起来

        self.waiting(1, 0) #于是......
        anim = Write(calculate_result)
        anim.update_config(lag_ratio = 1, run_time = 2)
        self.play(anim, FadeIn(hint_triple, UP), FadeOut(hint_odot, DOWN))
        self.waiting(1, 6) #最后的结果就相当于把三个向量
        self.play(ReplacementTransform(notice4, notice5))
        self.waiting(1, 7) #按点乘的方式乘起来
        self.waiting(0, 22) #（空闲）

        fullchip = FullChip().scale(0.5).rotate(PI/6).shift(4.15*UP + 6.5*LEFT).shift(2*unit(2*PI/3))
        bubble = Union(Ellipse(width = 1.8, height = 0.9), Triangle().scale(0.5).rotate(PI/6).shift(0.6*LEFT + 0.15*UP))
        text = Text("漂亮！", font = "lolita").scale(0.6)
        cute = VGroup(bubble, text).shift(1.8*UP + 6*LEFT)
        
        anim = ShowCreationThenDestructionAround(calculate_result)
        anim.update_config(run_time = 2)
        self.play(ApplyMethod(fullchip.shift, -2*unit(2*PI/3)), FadeOut(hint_triple), anim)
        self.waiting(0, 14) #这个结果有着很不错的对称性
        self.play(FadeInFromPoint(cute, cute.get_corner(UL) + 0.3*UP), run_time = 0.5)
        self.waiting(1, 0) #又漂亮 又好记
        self.play(ApplyMethod(VGroup(fullchip, cute).shift, 3*unit(5*PI/6)))
        self.waiting(3, 1) #到此共92秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_2(Scene):

    def construct(self):

        notice5 = Notice("推导完毕", "请　鼓掌")
        notice6 = Notice("另一角度", "请注意到")
        notice7 = Notice("注意力集中", "请")
        notice8 = Notice("神奇结论", "请　欣赏")
        notice9 = Notice("前情回顾", "请　参考")
        notice10 = Notice("神奇结论", "请　欣赏")

        tex_string1 = r"\begin{bmatrix}a_0\\a_1\\a_2\\a_3\end{bmatrix}"
        tex_string2 = r"\begin{bmatrix}b_0\\b_1\\b_2\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}c_0\\c_1\\c_2\\c_3\\c_4\\c_5\end{bmatrix}"
        mtex_convolution_vec = MTex(tex_string1 + r"*" + tex_string2+ r"=" + tex_string3, tex_to_color_map = {re.compile(r"a_."): BLUE, re.compile(r"b_."): RED, re.compile(r"c_."): YELLOW}).scale(0.8).shift(2*UP + 3*LEFT)
        
        def get_difference(mtex1: MTex, mtex2: MTex, index1: int = 0, index2: int = 0, tex: str = r"="):
            return mtex1.select_part(tex, index1).get_center() - mtex2.select_part(tex, index2).get_center()

        mtex_winograd_function = MTex(r"\vec{c}=S\left({{}P}{(}\vec{a}{)}\odot P{(}\vec{b}{)}\right)", isolate = [r"=", r"{(}", r"{)}"], tex_to_color_map = {r"\vec{c}":YELLOW, r"S": GREEN, (r"{{}P}", r"P"): PURPLE_A, r"\vec{a}": BLUE, r"\vec{b}": RED}).scale(0.8).shift(0.5*DOWN + 3*LEFT)
        mtex_winograd_matrix = MTex(r"\vec{c}=S_c\left(P_a\vec{a}\odot P_b\vec{b}\right)", isolate = [r"="], tex_to_color_map = {r"\vec{c}":YELLOW, r"S_c": GREEN, (r"P_a", r"P_b"): PURPLE_A, r"\vec{a}": BLUE, r"\vec{b}": RED}).scale(0.8).shift(0.5*DOWN + 3*LEFT)
        mtex_winograd_matrix.shift(get_difference(mtex_winograd_function, mtex_winograd_matrix))
        
        mtex_convolution = MTex(r"\vec{a}*\vec{b} = \vec{c}", isolate = [r"="], tex_to_color_map = {r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW}).scale(0.8).shift(2*UP + 2*RIGHT)
        mtex_dual = MTex(r"\vec{a}*\vec{b} = L(\vec{a}, \vec{b}, \hat{c})", isolate = [r"="], tex_to_color_map = {r"\vec{a}": BLUE, r"\vec{b}": RED, r"\hat{c}": YELLOW, r"L": PURPLE}).scale(0.8)
        mtex_dual.shift(get_difference(mtex_convolution, mtex_dual)+0.8*UP)
        tex_string0 = r"L(\vec{a}, \vec{b}, \vec{c})"
        tex_string1 = r"\vec{c}\cdot\left(S_c\left(P_a\vec{a}\odot P_b\vec{b}\right)\right)"
        tex_string2 = r"=\vec{c}^\mathrm{T}S_c\left(P_a\vec{a}\odot P_b\vec{b}\right)"
        tex_string3 = r"=(S_c^\mathrm{T}\vec{c})\cdot\left(P_a\vec{a}\odot P_b\vec{b}\right)"
        tex_string4 = r"=\langle\,P_a\vec{a},\,P_b\vec{b},\,S_c^\mathrm{T}\vec{c}\,\rangle"
        mtex_calculate = MTex(
        tex_string0 + r"&=" + tex_string1 + r"\\&" + tex_string2 + r"\\&" + tex_string3 + r"\\&" + tex_string4, 
        isolate = [tex_string0, r"=", tex_string1, tex_string2, tex_string3, tex_string4, r"\odot"], 
        tex_to_color_map = {r"L": PURPLE, r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW, r"S_c": GREEN, (r"P_a", r"P_b"): PURPLE_A}, 
        ).scale(0.8)
        calculate_function = VGroup(mtex_calculate.get_part_by_tex(tex_string0), mtex_calculate.select_part(r"=", 0))
        calculate_others = mtex_calculate.get_parts_by_tex((tex_string1, tex_string2, tex_string3, tex_string4))
        mtex_calculate.shift(get_difference(mtex_convolution, mtex_calculate) + 0.8*DOWN + LEFT)
        
        self.add(notice5, mtex_convolution_vec, mtex_convolution, mtex_dual, mtex_calculate, mtex_winograd_matrix)

        convolution_c = MTex(r"c_i = \sum_{j}a_jb_{i-j}", tex_to_color_map = {r"c_i": YELLOW, r"a_j": BLUE, r"b_{i-j}": RED}).scale(0.8).shift(0.5*DOWN + 3*LEFT)
        surrounding_c = SurroundingRectangle(convolution_c)
        formula_c = VGroup(convolution_c, surrounding_c)
        tex_string0 = r"L(\vec{a}, \vec{b}, \vec{c})="
        tex_string1 = r"\sum_{i=0}^3\sum_{j=0}^2a_ib_jc_{i+j}"
        mtex_multilinear_direct = MTex(r"L(\vec{a}, \vec{b}, \vec{c})=\sum_{i=0}^3\sum_{j=0}^2a_ib_jc_{i+j}", isolate = [r"=", tex_string0, tex_string1], tex_to_color_map = {r"L": PURPLE, (r"\vec{a}", r"a_i"): BLUE, (r"\vec{b}", r"b_j"): RED, (r"\vec{c}", r"c_{i+j}"): YELLOW}).scale(0.8)
        mtex_multilinear_direct.shift(get_difference(mtex_convolution, mtex_multilinear_direct)+0.8*DOWN)
        direct_function = mtex_multilinear_direct.get_part_by_tex(tex_string0)
        direct_others = mtex_multilinear_direct.get_parts_by_tex(tex_string1)

        self.play(ReplacementTransform(notice5, notice6), FadeOut(mtex_winograd_matrix, RIGHT), FadeOut(calculate_others, RIGHT), ApplyMethod(calculate_function.shift, RIGHT), FadeIn(formula_c, RIGHT))
        self.waiting(2, 17) #但是卷积还可以直接表示为分量相乘
        self.remove(calculate_function)
        self.add(direct_function)

        self.play(Write(direct_others), run_time = 2)
        self.waiting(0, 29) #于是我们可以得到函数L的一个不同表示
        self.waiting(1, 1) #（空闲）

        self.waiting(2, 17) #光是式子可能有些不好理解
        
        series_a = Series(r"a", 0, 4)
        series_b = Series(r"b", 0, 3)
        long_mul = LongMultiplication(series_a, series_b, r"c", False).shift(0.5*DOWN + 0.5*RIGHT)
        self.play(FadeOut(VGroup(mtex_multilinear_direct, formula_c), LEFT), ApplyMethod(VGroup(mtex_convolution_vec, mtex_convolution, mtex_dual).shift, LEFT), FadeIn(long_mul, LEFT))
        self.waiting(1, 22) #结合竖式乘法来看会简单一些
        self.waiting(0, 23) #（空闲）

        anims = []
        for i in range (6):
            anim = ApplyMethod(long_mul.result.term[i].next_to, long_mul.result.term[i].get_corner(DR) + 0.08*RIGHT, UR, 0)
            anims.append(anim)
        self.play(*anims)
        self.waiting(1, 18) #只需要把原来作为结果的c

        alpha = ValueTracker(0.0)
        self.add(long_mul.get_duality())
        for i in range (6):
            long_mul.result.term[i].save_state()

        def moving_updater(layer: int):
            def util(layer:int, mob: Mobject):
                a = alpha.get_value()
                distance = a * 2.1
                mob.restore().shift(distance * UP)
                if distance >= layer*0.7:
                    mob.set_opacity(0)
            return lambda x: util(layer, x)
        long_mul.result.term[5].add_updater(moving_updater(1))
        long_mul.result.term[4].add_updater(moving_updater(2))
        for i in range (4):
            long_mul.result.term[i].add_updater(moving_updater(3))
        def opacity_updater(layer: int):
            def util(layer: int, mob:Mobject):
                a = alpha.get_value()
                if 3*a >= 3-layer:
                    mob.set_opacity(1)
                else:
                    mob.set_opacity(0)
            return lambda x: util(layer, x)
        for j in range (3):
            for i in range (4):
                long_mul.terms_result[j][i].add_updater(opacity_updater(j))
        self.play(ApplyMethod(alpha.set_value, 1.0))
        for j in range (3):
            for i in range (4):
                long_mul.terms_result[j][i].clear_updaters()
        for i in range (6):
            long_mul.result.term[i].clear_updaters()
        self.remove(long_mul.result)
        self.waiting(1, 13) #反过来乘上去

        surrounding = SurroundingRectangle(long_mul.calculation)
        sum = MTex(r"L(\vec{a}, \vec{b}, \vec{c})=\sum", isolate = [r"L(\vec{a}, \vec{b}, \vec{c})=", r"\sum"], tex_to_color_map = {r"L": PURPLE, r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW}).scale(0.8).next_to(surrounding, LEFT)
        sum_function = sum.get_part_by_tex(r"L(\vec{a}, \vec{b}, \vec{c})=")
        sum_symbol = sum.get_part_by_tex(r"\sum")
        self.play(ShowCreation(surrounding))
        self.play(Write(sum_symbol))
        self.waiting(0, 16) #再把这些东西都加起来
        self.play(FadeIn(sum_function, 0.5*RIGHT))
        self.waiting(1, 14) #就能找到我们需要的函数L
        self.waiting(4, 6)
        self.play(FadeOut(VGroup(surrounding, sum_symbol, sum_function))) #（空闲）

        self.play(ReplacementTransform(notice6, notice7))
        self.waiting(2, 16) #可能一些富有洞察力的观众已经注意到了
        self.waiting(3, 12) #现在这个样子看上去很眼熟

        series_c_2 = Series(r"c", 0, 6)
        series_b_2 = Series(r"b", 2, 3, -1)
        long_mul_bounded = LongMultiplication(series_c_2, series_b_2, r"a", True, m_colors = [YELLOW, RED, BLUE], result_offset = -4)
        long_mul_bounded.shift(long_mul.mul_2.term[0].get_center() - long_mul_bounded.mul_2.term[0].get_center())
        conlolution_bounded = MTex(r"\begin{bmatrix}c_0\\c_1\\c_2\\c_3\\c_4\\c_5\end{bmatrix}\dot{*}\begin{bmatrix}b_2\\b_1\\b_0\end{bmatrix}{=}\begin{bmatrix}a_0\\a_1\\a_2\\a_3\end{bmatrix}", tex_to_color_map = {re.compile(r"a_."): BLUE, re.compile(r"b_."): RED, re.compile(r"c_."): YELLOW}).scale(0.8).shift(2*UP + 5*LEFT)
        anims = []
        all_terms = VGroup()
        for j in range (3):
            for i in range (4):
                termsji = VGroup(long_mul.terms_mul_1[j][i], long_mul.terms_mul_2[j][i], long_mul.terms_result[j][i])
                all_terms.add(termsji)
                direction = long_mul.terms_mul_2[j][i].get_corner(DR)-long_mul.terms_result[j][i].get_corner(DR)+(2-j)*1.4*LEFT
                anim = ApplyMethod(termsji.shift, direction)
                anims.append(anim)
        self.play(*anims)
        self.waiting(2, 10) #我们如果把这些项重新排列一下位置

        copy = []
        for i in range (4):
            copy.append(long_mul_bounded.result.term[i].copy())
            long_mul_bounded.result.term[i].move_to(long_mul.terms_mul_1[0][i])
        self.add(long_mul_bounded.result)
        def opacity_updater(layer: int):
            def util(layer: int, mob:Mobject):
                a = alpha.get_value()
                if 3*a >= 3-layer:
                    mob.set_color(BLUE)
                else:
                    mob.set_color(dark(BLUE))
            return lambda x: util(layer, x)
        for j in range (3):
            for i in range (4):
                long_mul.terms_mul_1[j][i].add_updater(opacity_updater(j))
        self.play(ApplyMethod(alpha.set_value, 0.0), ApplyMethod(long_mul_bounded.result.shift, 2.1*DOWN))
        for j in range (3):
            for i in range (4):
                long_mul.terms_mul_1[j][i].clear_updaters()
        self.play(*[Transform(long_mul_bounded.result.term[i], copy[i]) for i in range (4)])
        self.play(FadeOut(VGroup(mtex_convolution_vec, long_mul.mul_1, long_mul.mul_2)))
        self.play(FadeIn(VGroup(long_mul_bounded.mul_1, long_mul_bounded.mul_2, conlolution_bounded)))
        self.waiting(2+7-4, 20) #就能得到另一个表达式 （空闲）

        mtex_convolution_bounded = MTex(r"\vec{c}\ \dot{*}\ \vec{b} = \vec{a}", isolate = [r"="], tex_to_color_map = {r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW}).scale(0.8).shift(2*UP + 2*LEFT)
        mtex_dual_bounded = MTex(r"\vec{c}\ \dot{*}\ \vec{b} = L(\hat{a}, \vec{b}, \vec{c})", isolate = [r"="], tex_to_color_map = {r"\hat{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW, r"L": PURPLE}).scale(0.8)
        mtex_dual_bounded.shift(get_difference(mtex_convolution_bounded, mtex_dual_bounded)+0.8*UP)
        mtex_bounded = VGroup(mtex_convolution_bounded, mtex_dual_bounded)
        mtex_unbounded = VGroup(mtex_convolution, mtex_dual)
        dividing_line = Line(series_c_2.get_corner(UL) + 0.2*UL, series_c_2.get_corner(UR) + 0.2*UR).set_color("#666666")
        
        surrounding = SurroundingRectangle(all_terms)
        sum_bounded = MTex(r"L(\vec{a}, \vec{b}, \vec{c})=\sum", isolate = [r"L(\vec{a}, \vec{b}, \vec{c})=", r"\sum"], tex_to_color_map = {r"L": PURPLE, r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW}).scale(0.8).next_to(surrounding, LEFT)
        
        self.play(FadeIn(mtex_convolution_bounded, DOWN), ApplyMethod(mtex_unbounded.shift, RIGHT), ShowCreation(dividing_line), ShowCreation(surrounding))
        self.waiting(1, 18) #这正好是只取中间的卷积
        self.play(FadeIn(sum_bounded, 0.5*RIGHT), FadeIn(mtex_dual_bounded, DOWN))
        self.waiting(1, 9) #所对应的的三重线性函数
        self.waiting(0, 26) #（空闲）
        
        copy_multilinear = MTex(r"L(\vec{a}, \vec{b}, \vec{c})=\sum_{i=0}^m\sum_{j=0}^na_ib_jc_{i+j}", tex_to_color_map = {r"L": PURPLE, (r"\vec{a}", r"a_i"): BLUE, (r"\vec{b}", r"b_j"): RED, (r"\vec{c}", r"c_{i+j}"): YELLOW}).scale(0.8).move_to(0.5*UP)
        copy_unbound_matrix = mtex_winograd_matrix.copy().move_to(0.5*DOWN + 3*RIGHT)
        copy_winograd_matrix = MTex(r"L(\vec{a}, \vec{b}, \vec{c}) = \langle\,P_a\vec{a},\,P_b\vec{b},\,S_c^\mathrm{T}\vec{c}\,\rangle", tex_to_color_map = {r"L": PURPLE, r"\vec{a}": BLUE, r"\vec{b}": RED, r"\vec{c}": YELLOW, r"S_c": GREEN, (r"P_a", r"P_b"): PURPLE_A}).scale(0.8).move_to(1.5*DOWN)
        copy_bounded_matrix = MTex(r"\vec{a}=P_a^\mathrm{T}\left(P_b\vec{b}\odot S_c^\mathrm{T}\vec{c}\right)", tex_to_color_map = {r"\vec{c}":YELLOW, r"S_c": GREEN, (r"P_a", r"P_b"): PURPLE_A, r"\vec{a}": BLUE, r"\vec{b}": RED}).scale(0.8).move_to(0.5*DOWN + 3*LEFT)
        copy_mtexes = VGroup(copy_multilinear, copy_unbound_matrix, copy_winograd_matrix, copy_bounded_matrix)
        self.play(FadeOut(VGroup(surrounding, sum_bounded, conlolution_bounded, long_mul_bounded.mul_1, long_mul_bounded.mul_2, long_mul_bounded.mul_1, long_mul_bounded.result, long_mul.upper_line, long_mul.lower_line, long_mul.mul, all_terms, dividing_line), 0.5*LEFT), ApplyMethod(VGroup(mtex_bounded, mtex_unbounded).shift, 0.5*LEFT), ReplacementTransform(notice7, notice8))
        self.waiting(0, 10) #也就是说......
        self.play(ShowCreationThenDestructionAround(mtex_convolution), ShowCreationThenDestructionAround(mtex_convolution_bounded), run_time = 2)
        self.waiting(0, 0) #两种不同的卷积
        self.play(ShowCreationThenDestructionAround(mtex_dual), ShowCreationThenDestructionAround(mtex_dual_bounded), Write(copy_multilinear), run_time = 2)
        self.waiting(1, 12) #对应的是同一个三重线性函数
        self.waiting(1, 21) #区别仅仅在于
        self.play(ShowCreationThenDestructionAround(mtex_dual.get_part_by_tex(r"\hat{c}")), run_time = 2)
        self.waiting(1, 0) #一种取的是关于c的对偶向量
        self.play(ShowCreationThenDestructionAround(mtex_dual_bounded.get_part_by_tex(r"\hat{a}")), run_time = 2)
        self.waiting(0, 24) #另一种取的是关于a的对偶向量
        self.waiting(0, 20) #（空闲）

        self.waiting(1, 2) #于是......
        self.play(FadeIn(copy_unbound_matrix, LEFT), FadeIn(copy_winograd_matrix, LEFT))
        self.waiting(2, 9) #......根据一种对偶向量所提供的计算方法
        self.play(FadeIn(copy_bounded_matrix, RIGHT))
        self.waiting(2, 3) #我们就能得到另一种对偶向量的计算方法
        self.waiting(0, 26) #（空闲）

        tex_string1 = r"\vec{f} = \begin{bmatrix}f_0\\f_1\\f_2\\f_3\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}{1}&{0}&{-1}&{0}\\{0}&{0.5}&{0.5}&{0}\\{0}&{-0.5}&{0.5}&{0}\\{0}&{-1}&{0}&{1}\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}a_5\\a_4\\a_3\\a_2\end{bmatrix}"
        mtex_f = MTex(
        tex_string1 + tex_string2 + tex_string3,
        tex_to_color_map = {(r"\vec{f}", re.compile(r"f_.")): TEAL, (r"{1}", r"{0}", r"{-1}", r"{0.5}", r"{-0.5}"): GREEN, re.compile(r"a_."): BLUE},
        ).scale(0.8).next_to(1.5*UP + 7*LEFT, RIGHT)
        
        tex_string1 = r"\vec{g} = \begin{bmatrix}g_0\\g_1\\g_2\\g_3\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}{1}&{0}&{0}\\{1}&{1}&{1}\\{1}&{-1}&{1}\\{0}&{0}&{1}\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}b_0\\b_1\\b_2\end{bmatrix}"
        mtex_g = MTex(
        tex_string1 + tex_string2 + tex_string3,
        tex_to_color_map = {(r"\vec{g}", re.compile(r"g_.")): RED_P, (r"{1}", r"{0}", r"{-1}"): PURPLE, re.compile(r"b_."): RED},
        ).scale(0.8).next_to(1.5*DOWN + 7*LEFT, RIGHT)
        
        tex_string1 = r"\vec{h} = \begin{bmatrix}h_0\\h_1\\h_2\\h_3\end{bmatrix} = "
        tex_string2 = r"\begin{bmatrix}f_0g_0\\f_1g_1\\f_2g_2\\f_3g_3\end{bmatrix} = \vec{f}\odot\vec{g}"
        mtex_h = MTex(
        tex_string1 + tex_string2,
        tex_to_color_map = {(r"\vec{f}", re.compile(r"f_.")): TEAL, (r"\vec{g}", re.compile(r"g_.")): RED_P, (r"\vec{h}", re.compile(r"h_.")): ORANGE},
        ).scale(0.8).next_to(1.5*UP + 0*LEFT, RIGHT)

        tex_string1 = r"\vec{c} = \begin{bmatrix}c_5\\c_4\end{bmatrix}="
        tex_string2 = r"\begin{bmatrix}{1}&{1}&{1}&{0}\\{0}&{1}&{-1}&{1}\end{bmatrix}"
        tex_string3 = r"\begin{bmatrix}h_0\\h_1\\h_2\\h_3\end{bmatrix}"
        mtex_c = MTex(
        tex_string1 + tex_string2 + tex_string3,
        tex_to_color_map = {(r"\vec{c}", re.compile(r"c_.")): YELLOW, (r"\vec{h}", re.compile(r"h_.")): ORANGE, (r"{1}", r"{0}", r"{-1}"): PURPLE},
        ).scale(0.8).next_to(1.5*DOWN + 0*LEFT, RIGHT)
        
        on_screen = VGroup(mtex_bounded, mtex_unbounded, copy_mtexes)
        concrete_formula = VGroup(mtex_f, mtex_g, mtex_h, mtex_c)

        self.waiting(2, 7) #具体写成表达式的形式
        self.play(FadeOut(on_screen, DOWN), FadeIn(concrete_formula, DOWN), ReplacementTransform(notice8, notice9))
        self.waiting(2, 0) #就是第一节最后出现的样子
        self.waiting(6, 14) #（空闲）

        self.play(FadeIn(on_screen, UP), FadeOut(concrete_formula, UP), ReplacementTransform(notice9, notice10))
        self.waiting(1, 23) #这就是完整的Winograd算法
        self.waiting(2, 25) #不仅是从系数到取值的转换
        self.waiting(3, 20) #更是一次无比精妙的对偶性的应用

        self.waiting(2, 7)
        self.play(FadeOut(on_screen), FadeOut(notice10))
        self.waiting(3, 0) #到此共105秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Summary(Scene):

    def construct(self):
        notice1 = Notice("良心视频", "请　三连")
        notice2 = Notice("下期预告", "敬请期待")
        notice3 = Notice("良心up主", "请　关注")

        picture_cover = ImageMobject("picture_cover.png", height = 2.5)
        self.play(Write(notice1), FadeIn(picture_cover, UP))
        self.waiting(2, 7) #预告了两期的Winograd算法的视频终于出了
        self.waiting(2, 8) #希望还符合大家的期待
        self.waiting(0, 29) #（空闲）

        self.waiting(2, 17) #本期视频的难度确实比较高
        self.waiting(3, 5) #所以 非常感谢大家能看到这里
        self.waiting(0, 24) #（空闲）

        picture_code_1 = ImageMobject("picture_code_1.png", height = 5).shift(3*LEFT)
        picture_code_2 = ImageMobject("picture_code_2.png", height = 5).shift(3*LEFT + 0.5*DL)
        self.play(ApplyMethod(picture_cover.shift, 3.5*RIGHT))
        self.play(FadeIn(picture_code_1, 0.5*UR))
        self.waiting(0, 24) #为了能尽量将这个算法讲清楚
        self.play(FadeIn(picture_code_2, 0.5*UR))
        self.waiting(2, 2) #这期视频耗费了我相当多的精力
        self.remove(picture_cover, picture_code_1, picture_code_2)
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
        self.play(ApplyMethod(sanlian1.set_color, "#00A1D6"), Flash(like1, flash_radius=1, color = "#00A1D6"), Flash(coin1, flash_radius=1, color = "#00A1D6"), Flash(star1, flash_radius=1, color = "#00A1D6"))
        self.waiting(0, 17) #希望大家多多三连支持
        self.waiting(0, 27) #（空闲）

        self.remove(sanlian1)

        gravity = 1/9
        alpha = ValueTracker(0.0)

        def moving_updater(angle):
            def util(angle: float, mob: Mobject):
                a = alpha.get_value()
                mob.move_to(DOWN).shift(a*unit(angle) + gravity*a*a*DOWN)
            return lambda x: util(angle, x)

        point_0 = Dot(color = TEAL).shift(DOWN)
        self.play(ShowCreation(point_0), ReplacementTransform(notice1, notice2))
        points = []
        traces = []
        number = 30
        for i in range (number):
            angle = TAU * i / number
            color = angle_color(angle)
            moving_point_i = Dot(color = color).shift(DOWN)
            traces_path_i = TracedPath(moving_point_i.get_center).set_color(color)
            points.append(moving_point_i)
            traces.append(traces_path_i)
            moving_point_i.add_updater(moving_updater(angle))
            self.add(moving_point_i, traces_path_i)
        self.remove(point_0)

        self.waiting(1, 0)
        self.play(ApplyMethod(alpha.set_value, 12.0), rate_func = linear, run_time = 2)
        for trace in traces:
            trace.clear_updaters()
        for point in points:
            point.clear_updaters()
        self.waiting(2+2-4, 20+29) #下期视频可能跨度会比较大 我想应该很难有人猜到是什么
        self.waiting(2, 10) #容我在这里先卖个关子
        self.play(FadeOut(VGroup(*points, *traces), DOWN))
        self.waiting(0, 6) #（空闲）

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
        self.waiting(0,7) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(1,21) #而我 就像我的名字一样

        self.play(FadeOut(painting_others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star0.shift, DOWN))
        self.waiting(1,12) #想要把天上的星星垂下来

        star_copy = star0.copy()
        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star0, apple))
        self.waiting(1,13) #变成触手可及的果实

        snowflake = SnowFlake()
        snowflake_2 = snowflake.copy().set_color(RED).set_stroke(width = 1.5)
        snowflake_3 = snowflake.copy().set_color(BLUE).set_stroke(width = 2)
        anims = LaggedStart(SpreadOut(snowflake_2).update_config(rate_func = linear), SpreadOut(snowflake_3).update_config(rate_func = linear), SpreadOut(snowflake).update_config(rate_func = linear), rate_func = rush_into, run_time = 2)
        self.play(Transform(star0, star_copy), anims)
        self.remove(snowflake_2, snowflake_3)
        self.waiting(2+1-2, 10+0) #变成指引前路的火光 （空闲）
        
        self.remove(star0, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(0,18) #我是乐正垂星
        self.waiting(2,8) #我们下期视频再见

        self.waiting(5,16)
        self.play(FadeOut(picture_photo), FadeOut(text_name), FadeOut(notice3))
        self.waiting(5)
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)