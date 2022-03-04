from manimlib import *
import numpy as np
import math

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):

        super().__init__()
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

class Module(VGroup):
    def __init__(self, m_text1, m_text2, m_text3):

        super().__init__()
        self.dividend = Tex(m_text1, color = GREEN)
        self.modulesymbol = Tex(r"\equiv")
        self.remainder = Tex(m_text2, color = BLUE)
        self.bra = Tex(r"(")
        self.moduletext = Tex(r"\bmod")
        self.divisor = Tex(m_text3, color = YELLOW)
        self.ket = Tex(r")")
        self.add(self.dividend, self.modulesymbol, self.remainder, self.bra, self.moduletext, self.divisor, self.ket)
        self.dividend_others = VGroup(self.modulesymbol, self.remainder, self.bra, self.moduletext, self.divisor, self.ket)
        
        #distance = np.array([0.5,0,0])
        self.remainder.next_to(self.bra.get_corner(LEFT), LEFT)
        self.modulesymbol.next_to(self.remainder.get_corner(LEFT), LEFT)
        self.dividend.next_to(self.modulesymbol.get_corner(LEFT), LEFT)
        self.moduletext.next_to(self.bra.get_corner(RIGHT), RIGHT)
        self.divisor.next_to(self.moduletext.get_corner(RIGHT), RIGHT)
        self.ket.next_to(self.divisor.get_corner(RIGHT), RIGHT)

        self.text = VGroup(self.modulesymbol, self.bra, self.moduletext, self.ket)

class Pixel(Square):

    def __init__(self, x_position, y_position, m_fill_opacity):

        super().__init__(stroke_width = 0, color = BLUE_E, fill_opacity = m_fill_opacity, side_length=1)
        self.shift(np.array([x_position, y_position, 0]))
        
class FiniteNumberPlane(VGroup):

    def __init__(self, x_range, y_range):
        super().__init__()
        self.coordinate = NumberPlane([-0.5, x_range-0.5, 1], [-0.5, y_range-0.5, 1])
        position_of_origin = self.coordinate.get_origin()

        label_x = VGroup()
        for i in range (x_range):
            labeli = Tex(r"%d" %i)
            labeli.next_to(np.array([i, -0.5, 0]), DOWN)
            label_x.add(labeli)
        label_x_mod = Tex(r"\bmod %d" %x_range)
        label_x_mod.next_to(np.array([0.5*(x_range-1), -1, 0]), DOWN)
        label_x.add(label_x_mod)
        label_x.set_color(GREEN)

        label_y = VGroup()
        for i in range (y_range):
            labeli = Tex(r"%d" %i)
            labeli.next_to(np.array([-0.5, i, 0]), LEFT)
            label_y.add(labeli)
        label_y_mod = Tex(r"\bmod %d" %y_range)
        label_y_mod.next_to(np.array([-1, 0.5*(y_range-1), 0]), LEFT)
        label_y.add(label_y_mod)
        label_y.set_color(YELLOW)

        self.dots = []
        self.remainders = []
        self.group_dots = VGroup()
        self.group_remainders = VGroup()
        for i in range (x_range):
            self.dots.append([])
            self.remainders.append([])
            for j in range (y_range):
                dot_ij = Dot(np.array([i,j,0]))
                self.dots[i].append(dot_ij)
                self.group_dots.add(dot_ij)
                self.remainders[i].append( Tex("0") )

        self.downarrows = []
        self.uparrows = []
        self.group_arrows = VGroup()
        self.remainders_ordered = []
        self.group_remainders_ordered = VGroup()
        for k in range (x_range * y_range):
            i = k % x_range
            j = k % y_range
            reminder_ij = Tex("%d" %k)
            reminder_ij.scale(0.6)
            reminder_ij.next_to(np.array([i,j,0]), 0.8*(RIGHT+UP))
            reminder_ij.scale(1.2)
            self.remainders[i][j] = reminder_ij
            self.group_remainders.add(reminder_ij)

            reminder_ordered_ij = Tex("%d" %k,color = YELLOW)
            reminder_ordered_ij.scale(0.6)
            reminder_ordered_ij.next_to(np.array([i,j,0]), 0.8*(LEFT+UP))
            reminder_ordered_ij.scale(1.2)
            self.remainders_ordered.append(reminder_ordered_ij)
            self.group_remainders_ordered.add(reminder_ordered_ij)

            downarrow_k = Line(np.array([i,j,0]), np.array([i+0.5,j+0.5,0]), stroke_color = ORANGE)
            uparrow_k = Arrow(np.array([i-0.5,j-0.5,0]), np.array([i,j,0]), stroke_color = ORANGE, buff = 0)
            self.downarrows.append(downarrow_k)
            self.uparrows.append(uparrow_k)
            self.group_arrows.add(downarrow_k, uparrow_k)

            if i == 1 and j == 0:
                x_base = k
            if i == 0 and j == 1:
                y_base = k

        sum_max = (x_range-1)*x_base + (y_range-1)*y_base
        number_of_colors = math.ceil( sum_max/(x_range * y_range) )
        self.colors = []
        group_colors = VGroup()
        for i in range(number_of_colors):
            groupi = VGroup()
            self.colors.append(groupi)
            group_colors.add(groupi)

        self.pixels = []
        self.sumofbasis = []
        self.group_pixels = VGroup()
        group_sumofbasis = VGroup()
        for i in range (x_range):
            self.pixels.append([])
            self.sumofbasis.append([])
            for j in range (y_range):
                k = i*x_base + j*y_base
                sumofbasis_ij = Tex(r"%d" %k)
                sumofbasis_ij.scale(0.6)
                sumofbasis_ij.next_to(np.array([i,j,0]), 0.8*(RIGHT+UP))
                sumofbasis_ij.scale(1.2)
                self.sumofbasis[i].append(sumofbasis_ij)
                group_sumofbasis.add(sumofbasis_ij)

                color_ij = math.floor(k/(x_range * y_range))
                pixel_ij = Pixel(i,j, color_ij/(number_of_colors - 1) )
                self.pixels[i].append(pixel_ij)
                self.group_pixels.add(pixel_ij)
                self.colors[color_ij].add(pixel_ij)
                
        self.labels = VGroup(label_x, label_y, self.group_dots)
        self.calculation = VGroup(self.group_remainders, self.group_remainders_ordered, group_sumofbasis, self.group_arrows, self.group_pixels)
        self.others = VGroup(self.labels, self.calculation)
        self.others.shift(position_of_origin)
        self.add(self.coordinate, self.others)
        self.remainder_type = VGroup(self.coordinate, self.labels, self.group_remainders)
        self.remainder_others = VGroup(self.group_remainders_ordered, group_sumofbasis, self.group_arrows, self.group_pixels)
        self.remainder_ordered_type = VGroup(self.coordinate, self.labels, self.group_remainders_ordered)
        self.remainder_ordered_others = VGroup(self.group_remainders, group_sumofbasis, self.group_arrows, self.group_pixels)
        self.sumofbasis_type = VGroup(self.coordinate, self.labels, group_sumofbasis)
        self.sumofbasis_others = VGroup(self.group_remainders, self.group_remainders_ordered, self.group_arrows, self.group_pixels)
        self.sumofbasis_changed = VGroup(label_x, label_y, self.group_pixels, group_sumofbasis)

class Template(Scene):
    def construct(self):

        notice0 = Notice("良心视频", "请　三连")
        notice1 = Notice("小学奥数", "非常简单")
        notice2 = Notice("精致动画", "请　欣赏")
        notice3 = Notice("探索规律", "请　模仿")
        notice4 = Notice("总结规律", "请　模仿")
        notice5 = Notice("一般结论", "请记笔记")
        notice6 = Notice("著名口诀", "请勿遗忘")
        notice7 = Notice("观察易知", "请　模仿")
        notice8 = Notice("前情提要", "请　复习")
        notice9 = Notice("观察易知", "请　模仿")
        notice10 = Notice("数学定理", "请记笔记")
        notice11 = Notice("探究内容", "请　选修*")

        # 第一节-2
        """ 
        ##  Making object
        module0_1 = Module(r"x", r"0", r"2")
        module0_1_others = VGroup(module0_1.modulesymbol, module0_1.remainder, module0_1.bra, module0_1.moduletext, module0_1.divisor, module0_1.ket)
        module0_2 = Module(r"x", r"0", r"3")
        equation_1 = Tex(r"(2,3) = 1,\ 2\times 3 = 6")

        module0_aligned_1 = Module(r"0", r"0", r"2")
        module0_aligned_2 = Module(r"0", r"0", r"3")
        module0_aligned = VGroup(module0_aligned_1, module0_aligned_2)
        module1_aligned_1 = Module(r"3", r"1", r"2")
        module1_aligned_2 = Module(r"3", r"0", r"3")
        module1_aligned = VGroup(module1_aligned_1, module1_aligned_2)
        module2_aligned_1 = Module(r"4", r"0", r"2")
        module2_aligned_2 = Module(r"4", r"1", r"3")
        module2_aligned = VGroup(module2_aligned_1, module2_aligned_2)
        module3_aligned_1 = Module(r"1", r"1", r"2")
        module3_aligned_2 = Module(r"1", r"1", r"3")
        module3_aligned = VGroup(module3_aligned_1, module3_aligned_2)
        module4_aligned_1 = Module(r"2", r"0", r"2")
        module4_aligned_2 = Module(r"2", r"2", r"3")
        module4_aligned = VGroup(module4_aligned_1, module4_aligned_2)
        module5_aligned_1 = Module(r"5", r"1", r"2")
        module5_aligned_2 = Module(r"5", r"2", r"3")
        module5_aligned = VGroup(module5_aligned_1, module5_aligned_2)
        module_aligned = VGroup(module0_aligned, module1_aligned, module2_aligned, module3_aligned, module4_aligned, module5_aligned)

        module0_1_instead_1 = Tex(r"0", color = GREEN)
        module0_2_instead_1 = Tex(r"0", color = GREEN)
        module0_1_instead_2 = Tex(r"6", color = GREEN)
        module0_2_instead_2 = Tex(r"6", color = GREEN)
        module0_1_instead_3 = Tex(r"12", color = GREEN)
        module0_2_instead_3 = Tex(r"12", color = GREEN)
        module0_1_instead_4 = Tex(r"18", color = GREEN)
        module0_2_instead_4 = Tex(r"18", color = GREEN)
        module0_1_instead = VGroup(module0_1_instead_1, module0_1_instead_2, module0_1_instead_3, module0_1_instead_4)
        module0_2_instead = VGroup(module0_2_instead_1, module0_2_instead_2, module0_2_instead_3, module0_2_instead_4)
        

        ##  Position
        module0_1.shift(UP)
        module0_2.shift(DOWN)
        module0_1_instead.shift(np.array([-1.5,1,0]))
        module0_2_instead.shift(np.array([-1.5,-1,0]))

        module0_aligned_1.scale(0.5)
        module0_aligned_2.scale(0.5)
        module0_aligned_1.shift(np.array([-5, -1, 0]))
        module0_aligned_2.shift(np.array([-5, -1.5, 0]))

        module1_aligned_1.scale(0.5)
        module1_aligned_2.scale(0.5)
        module1_aligned_1.shift(np.array([-2, -1, 0]))
        module1_aligned_2.shift(np.array([-2, -1.5, 0]))

        module2_aligned_1.scale(0.5)
        module2_aligned_2.scale(0.5)
        module2_aligned_1.shift(np.array([-5, 0.25, 0]))
        module2_aligned_2.shift(np.array([-5, -0.25, 0]))

        module3_aligned_1.scale(0.5)
        module3_aligned_2.scale(0.5)
        module3_aligned_1.shift(np.array([-2, 0.25, 0]))
        module3_aligned_2.shift(np.array([-2, -0.25, 0]))

        module4_aligned_1.scale(0.5)
        module4_aligned_2.scale(0.5)
        module4_aligned_1.shift(np.array([-5, 1.5, 0]))
        module4_aligned_2.shift(np.array([-5, 1, 0]))

        module5_aligned_1.scale(0.5)
        module5_aligned_2.scale(0.5)
        module5_aligned_1.shift(np.array([-2, 1.5, 0]))
        module5_aligned_2.shift(np.array([-2, 1, 0]))

        frame_0 = SurroundingRectangle(module0_aligned, stroke_color = YELLOW, fill_opacity = 0, )
        frame_1 = SurroundingRectangle(module1_aligned, stroke_color = YELLOW, fill_opacity = 0, )
        frame_2 = SurroundingRectangle(module2_aligned, stroke_color = YELLOW, fill_opacity = 0, )
        frame_3 = SurroundingRectangle(module3_aligned, stroke_color = YELLOW, fill_opacity = 0, )
        frame_4 = SurroundingRectangle(module4_aligned, stroke_color = YELLOW, fill_opacity = 0, )
        frame_5 = SurroundingRectangle(module5_aligned, stroke_color = YELLOW, fill_opacity = 0, )
        
        ##  Showing object
        self.add(notice0)
        self.play(ReplacementTransform(notice0, notice1))
        self.wait(0.79) #学会了同余式以后
        self.wait(1.89) #我们来做一点小练习吧
        self.wait(0.72) #（空闲）
        self.play(FadeIn(module0_1.dividend, DOWN))
        self.wait(0.55) #如果一个自然数
        self.play(FadeIn(module0_1_others, DOWN))
        self.wait(0.51) #除以2余0...
        self.play(FadeIn(module0_2, UP))
        self.wait(0.96) #...除以3也余0
        self.play(Indicate(module0_1.dividend), Indicate(module0_2.dividend))
        self.wait(0.65) #那么这个数是多少
        self.wait(0.84) #（空闲）
        self.play(Indicate(notice1))
        self.wait(1.89) #这是一道简单到不能再简单的题了
        self.wait(1.96) #任何一个人都能看出来
        self.play(Transform(module0_1.dividend, module0_1_instead_1), Transform(module0_2.dividend, module0_2_instead_1))
        self.wait(0.88) #0就满足条件
        self.wait(1.14) #当然 由于...
        self.play(FadeIn(equation_1, RIGHT))
        self.wait(0.33)
        self.play(FadeOut(equation_1, RIGHT)) #当然 由于6是2和3的最小公倍数
        self.wait(0.30) #所以...
        self.play(Transform(module0_1.dividend, module0_1_instead_2), Transform(module0_2.dividend, module0_2_instead_2), run_time = 0.5)
        self.wait(0.20) #...6...
        self.play(Transform(module0_1.dividend, module0_1_instead_3), Transform(module0_2.dividend, module0_2_instead_3), run_time = 0.5)
        self.wait(0.35) #...12...
        self.play(Transform(module0_1.dividend, module0_1_instead_4), Transform(module0_2.dividend, module0_2_instead_4), run_time = 0.5)
        self.wait(1.70) #...18这些6的倍数
        self.wait(1.76) #也都满足
        self.wait(0.00) #（空闲）
        self.wait(1.84) #不过为了简便考虑
        self.play(Transform(module0_1.dividend, module0_1_instead_1), Transform(module0_2.dividend, module0_2_instead_1))
        self.wait(1.05)#我们只关心最小的那个
        self.wait(1.20)#（空闲）
        

        module1_1 = Module(r"x", r"1", r"2")
        module1_1_others = VGroup(module1_1.modulesymbol, module1_1.remainder, module1_1.bra, module1_1.moduletext, module1_1.divisor, module1_1.ket)
        module1_2 = Module(r"x", r"0", r"3")

        module1_1_instead = Tex(r"3", color = GREEN)
        module1_2_instead = Tex(r"3", color = GREEN)

        module1_1.shift(UP+RIGHT)
        module1_2.shift(DOWN+RIGHT)
        module1_1_instead.shift(np.array([-0.5,1,0]))
        module1_2_instead.shift(np.array([-0.5,-1,0]))

        self.play(ReplacementTransform(module0_1, module0_aligned_1), ReplacementTransform(module0_2, module0_aligned_2))
        self.wait(1.44)  #接下来稍微增加一点难度
        self.play(FadeIn(module1_1.dividend, DOWN))
        self.wait(0.19) #如果一个数
        self.play(FadeIn(module1_1_others, DOWN))
        self.wait(0.70) #除以2余1
        self.play(FadeIn(module1_2, UP))
        self.wait(0.80) #除以3余0
        self.play(Indicate(module1_1.dividend), Indicate(module1_2.dividend))
        self.wait(0.67) #那么这个数是多少
        self.wait(0.79) #（空闲）
        self.wait(1.42) #这也很简单
        self.play(Transform(module1_1.dividend, module1_1_instead), Transform(module1_2.dividend, module1_2_instead))
        self.wait(0.66) #3本身就是奇数
        self.play(Indicate(module1_1.dividend), Indicate(module1_2.dividend))
        self.play(ReplacementTransform(module1_1, module1_aligned_1), ReplacementTransform(module1_2, module1_aligned_2))
        self.wait(1.91+0.89-2) #所以3就满足条件 + （空闲）
        
        module2_1 = Module(r"x", r"0", r"2")
        module2_1_others = VGroup(module2_1.modulesymbol, module2_1.remainder, module2_1.bra, module2_1.moduletext, module2_1.divisor, module2_1.ket)
        module2_2 = Module(r"x", r"1", r"3")

        module2_1_not = Line(np.array([-0.3, 0.3, 0]), np.array([0.3, -0.3, 0]), color = RED)
        module2_2_not = Line(np.array([-0.3, 0.3, 0]), np.array([0.3, -0.3, 0]), color = RED)

        module2_1_instead_0 = Tex(r"0", color = GREEN)
        module2_2_instead_0 = Tex(r"0", color = GREEN)
        module2_1_instead_1 = Tex(r"1", color = GREEN)
        module2_2_instead_1 = Tex(r"1", color = GREEN)
        module2_1_instead_2 = Tex(r"2", color = GREEN)
        module2_2_instead_2 = Tex(r"2", color = GREEN)
        module2_1_instead_3 = Tex(r"3", color = GREEN)
        module2_2_instead_3 = Tex(r"3", color = GREEN)
        module2_1_instead_4 = Tex(r"4", color = GREEN)
        module2_2_instead_4 = Tex(r"4", color = GREEN)
        module2_1_instead = VGroup(module2_1_instead_0, module2_1_instead_1, module2_1_instead_2, module2_1_instead_3, module2_1_instead_4)
        module2_2_instead = VGroup(module2_2_instead_0, module2_2_instead_1, module2_2_instead_2, module2_2_instead_3, module2_2_instead_4)
        
        module2_1.shift(UP+2*RIGHT)
        module2_2.shift(DOWN+2*RIGHT)
        module2_1_instead.shift(np.array([0.5,1,0]))
        module2_2_instead.shift(np.array([0.5,-1,0]))
        module2_1_not.shift(np.array([1,1,0]))
        module2_2_not.shift(np.array([1,-1,0]))
        
        self.play(FadeIn(module2_1.dividend, DOWN))
        self.wait(0.24) #那如果一个数
        self.play(FadeIn(module2_1_others, DOWN))
        self.wait(0.38) #除以2余0
        self.play(FadeIn(module2_2, UP))
        self.wait(0.65) #除以3余1呢
        self.wait(0.61) #（空闲）
        self.wait(2.29) #这就不太好一眼看出来了
        self.wait(1.29) #但没关系
        self.play(Transform(module2_1.dividend, module2_1_instead_0), Transform(module2_2.dividend, module2_2_instead_0), FadeIn(module2_2_not), run_time = 0.4)
        self.wait(0.4)
        self.play(Transform(module2_1.dividend, module2_1_instead_1), Transform(module2_2.dividend, module2_2_instead_1), FadeIn(module2_1_not), FadeOut(module2_2_not), run_time = 0.4)
        self.wait(0.4)
        self.play(Transform(module2_1.dividend, module2_1_instead_2), Transform(module2_2.dividend, module2_2_instead_2), FadeOut(module2_1_not), FadeIn(module2_2_not), run_time = 0.4)
        self.wait(0.4)
        self.play(Transform(module2_1.dividend, module2_1_instead_3), Transform(module2_2.dividend, module2_2_instead_3), FadeIn(module2_1_not), run_time = 0.4)
        self.wait(0.4)
        self.play(Transform(module2_1.dividend, module2_1_instead_4), Transform(module2_2.dividend, module2_2_instead_4), FadeOut(module2_1_not), FadeOut(module2_2_not), run_time = 0.4)
        self.wait(0.4)
        self.wait(1.86+0.72+2.28-4) #我们可以一个一个试过去 最后就能找到答案了
        self.play(Indicate(module2_1.dividend), Indicate(module2_2.dividend), run_time = 0.8)
        self.wait(0.08) #是4

        self.play(ReplacementTransform(module2_1, module2_aligned_1), ReplacementTransform(module2_2, module2_aligned_2))
        self.wait(0.16) #（空闲）
        

        module3_1 = Module(r"x", r"1", r"2")
        module3_2 = Module(r"x", r"1", r"3")
        module3_1_instead = Tex(r"1", color = GREEN)
        module3_2_instead = Tex(r"1", color = GREEN)
        module3_1.shift(0.5*UP+2*RIGHT)
        module3_2.shift(0.5*DOWN+2*RIGHT)
        module3_1_instead.shift(np.array([0.5,0.5,0]))
        module3_2_instead.shift(np.array([0.5,-0.5,0]))

        module4_1 = Module(r"x", r"0", r"2")
        module4_2 = Module(r"x", r"2", r"3")
        module4_1_instead = Tex(r"2", color = GREEN)
        module4_2_instead = Tex(r"2", color = GREEN)
        module4_1.shift(0.5*UP+2*RIGHT)
        module4_2.shift(0.5*DOWN+2*RIGHT)
        module4_1_instead.shift(np.array([0.5,0.5,0]))
        module4_2_instead.shift(np.array([0.5,-0.5,0]))

        module5_1 = Module(r"x", r"1", r"2")
        module5_2 = Module(r"x", r"2", r"3")
        module5_1_instead = Tex(r"5", color = GREEN)
        module5_2_instead = Tex(r"5", color = GREEN)
        module5_1.shift(0.5*UP+2*RIGHT)
        module5_2.shift(0.5*DOWN+2*RIGHT)
        module5_1_instead.shift(np.array([0.5,0.5,0]))
        module5_2_instead.shift(np.array([0.5,-0.5,0]))

        self.wait(1)
        self.play(FadeIn(module3_1, DOWN), FadeIn(module3_2, UP), run_time = 0.5)
        self.wait(0.25)
        self.play(Transform(module3_1.dividend, module3_1_instead), Transform(module3_2.dividend, module3_2_instead), run_time = 0.5)
        self.wait(0.25)
        self.play(ReplacementTransform(module3_1, module3_aligned_1), ReplacementTransform(module3_2, module3_aligned_2), run_time = 0.5)
        

        self.play(FadeIn(module4_1, DOWN), FadeIn(module4_2, UP), run_time = 0.5)
        self.wait(0.25)
        self.play(Transform(module4_1.dividend, module4_1_instead), Transform(module4_2.dividend, module4_2_instead), run_time = 0.5)
        self.wait(0.25)
        self.play(ReplacementTransform(module4_1, module4_aligned_1), ReplacementTransform(module4_2, module4_aligned_2), run_time = 0.5)
        

        self.play(FadeIn(module5_1, DOWN), FadeIn(module5_2, UP), run_time = 0.5)
        self.wait(0.25)
        self.play(Transform(module5_1.dividend, module5_1_instead), Transform(module5_2.dividend, module5_2_instead), run_time = 0.5)
        self.wait(0.25)
        self.play(ReplacementTransform(module5_1, module5_aligned_1), ReplacementTransform(module5_2, module5_aligned_2), run_time = 0.5)
        self.wait(1.18+3.67+1.47+1.57-7) #就这样 我们可以列举出除以2和除以3的全部6种情况 为了方便起见

        self.remove(module_aligned)
        grid = NumberPlane()
        self.play(Write(grid), run_time = 1.87) #我们打个表吧
        
        grid1 = FiniteNumberPlane(2,3)
        grid1.shift(np.array([0.5, 1, 0]))

        grid2 = FiniteNumberPlane(7,3)
        grid3 = FiniteNumberPlane(7,5)
        grid4 = FiniteNumberPlane(3,5)

        self.play(FadeIn(grid1.coordinate))
        self.wait(1.24) #诶 等一下
        self.remove(grid)
        self.wait(0.2)
        self.add(grid)
        self.wait(0.2)
        self.remove(grid)
        self.wait(0.2)
        self.add(grid)
        self.wait(0.2)
        self.remove(grid)
        self.wait(0.2)
        self.add(grid)
        self.wait(0.27) #不需要这么大

        self.play(ShowCreationThenDestructionAround(grid1.coordinate), FadeOut(grid), run_time = 2)
        grid1.others.shift(np.array([2.5, -1, 0]))
        self.play(ApplyMethod(grid1.coordinate.shift, np.array([2.5, -1, 0])), FadeIn(module_aligned), FadeIn(grid1.labels, np.array([2.5, -1, 0])))
        self.wait(2.17+0.88-3) #只需要2乘3的一块就够了

        grid1.remainders[0][0].set_color(YELLOW)
        self.add(frame_0, grid1.remainders[0][0])
        self.wait(0.5)
        grid1.remainders[0][0].set_color(WHITE)
        self.remove(frame_0)

        grid1.remainders[1][0].set_color(YELLOW)
        self.add(frame_1, grid1.remainders[1][0])
        self.wait(0.5)
        grid1.remainders[1][0].set_color(WHITE)
        self.remove(frame_1)

        grid1.remainders[0][1].set_color(YELLOW)
        self.add(frame_2, grid1.remainders[0][1])
        self.wait(0.5)
        grid1.remainders[0][1].set_color(WHITE)
        self.remove(frame_2)

        grid1.remainders[1][1].set_color(YELLOW)
        self.add(frame_3, grid1.remainders[1][1])
        self.wait(0.5)
        grid1.remainders[1][1].set_color(WHITE)
        self.remove(frame_3)

        grid1.remainders[0][2].set_color(YELLOW)
        self.add(frame_4, grid1.remainders[0][2])
        self.wait(0.5)
        grid1.remainders[0][2].set_color(WHITE)
        self.remove(frame_4)

        grid1.remainders[1][2].set_color(YELLOW)
        self.add(frame_5, grid1.remainders[1][2])
        self.wait(0.5)
        grid1.remainders[1][2].set_color(WHITE)
        self.remove(frame_5)
        self.wait(3.03-3) # 我们再把之前求出来的数都标上去

        self.play(FadeOut(module_aligned))
        self.play(ApplyMethod( grid1.remainder_type.shift, np.array([-3, 0, 0]) ))
        self.wait(0.04) # 这张表就打好了
        self.wait(0.86) # （空闲）

        self.play(ReplacementTransform(grid1.remainder_type, grid2.remainder_type), ReplacementTransform(notice1, notice2))
        self.wait(5)
        self.play(ReplacementTransform(grid2.remainder_type, grid3.remainder_type))
        self.wait(5)
        self.play(ReplacementTransform(grid3.remainder_type, grid4.remainder_type))
        self.wait(5)
        self.wait(0.91)
        #对任何两个互素的数 我们都可以这样打表
        """

        # 第一节-3
        """
        grid4 = FiniteNumberPlane(3,5)
        self.add(grid4.remainder_type)

        self.play(ApplyMethod(grid4.remainder_type.shift, UP), ReplacementTransform(notice2, notice1))
        grid4.remainder_others.shift(UP)
        self.wait(1.37) #既然这是一张3乘5的表
        self.wait(3.84) #那么我们应该就能在上面找到15的所有余数
        self.wait(2.17) #我们来试试看吧


        current_runtime = [1.09, 0.98, 0.89, 1.05, 1.09, 0.94, 1.02, 1.08, 1.03, 0.93, 1.15, 1.07, 1.09, 1.09, 0.94]
        for order in range (15):
            animations = []
            ratio = 15
            for i in range (order):
                ratio = ratio - 1
                anim_i = ApplyMethod(grid4.remainders_ordered[order - i - 1].set_color, interpolate_color(WHITE, YELLOW, ratio/15))
                animations.append(anim_i)
            self.play(*animations, ReplacementTransform(grid4.remainders[order % 3][order % 5], grid4.remainders_ordered[order]), run_time = current_runtime[order])
        self.wait(0.98) #0,1,2,3,4,5,6,7,8,9,10,11,12,13,14

        self.wait(2.07) #和我们之前猜测的一样
        self.play(ApplyMethod(grid4.group_remainders_ordered.set_color, YELLOW))
        self.play(ApplyMethod(grid4.group_remainders_ordered.set_color, WHITE))
        self.wait(1.81+0.64-2) #所有的余数都找到了

        self.wait(2.40) #可能有细心的观众已经发现了

        self.play(FadeIn(grid4.downarrows[0]), FadeIn(grid4.uparrows[1]), run_time = 0.5)
        self.wait(0.5)
        self.play(FadeOut(grid4.downarrows[0]), FadeOut(grid4.uparrows[1]), run_time = 0.5)
        self.play(FadeIn(grid4.downarrows[1]), FadeIn(grid4.uparrows[2]), run_time = 0.5)
        self.wait(0.5)
        self.play(FadeOut(grid4.downarrows[1]), FadeOut(grid4.uparrows[2]), run_time = 0.5)
        self.wait(3.29-3) #下一个数总会出现在上一个数的右上角
        self.play(FadeIn(grid4.downarrows[2]))
        self.wait(1.56-1) # 如果碰到了边界
        self.play(FadeIn(grid4.uparrows[3]), run_time = 0.5)
        self.wait(0.93)
        for i in range (2,13):
            self.play(FadeOut(grid4.downarrows[i]), FadeOut(grid4.uparrows[i+1]), FadeIn(grid4.downarrows[i+1]), FadeIn(grid4.uparrows[i+2]), run_time = 0.5)
            self.wait(0.5)
        self.play(FadeOut(grid4.downarrows[13]), FadeOut(grid4.uparrows[14]))
        #就像贪吃蛇一样穿过去 这是为什么呢 想出来的观众 可以把答案留在评论区里
        """

        # 第一节-4-1
        """
        grid4 = FiniteNumberPlane(3,5)
        grid4.shift(UP)
        grid4.group_remainders_ordered.set_color(WHITE)
        self.add(notice1, grid4.remainder_ordered_type)
        animations = []
        for i in range (15):
            anim_i = ReplacementTransform(grid4.remainders_ordered[i], grid4.remainders[i % 3][i % 5])
            animations.append(anim_i)
        self.play(*animations, ReplacementTransform(notice1, notice3))
        self.wait(1.56) #这张表还有一个有趣的地方

        self.wait(0.4)
        animations = []
        for i in range (5):
            anim_i = Indicate(grid4.remainders[0][i])
            animations.append(anim_i)
            anim_i = Indicate(grid4.dots[0][i])
            animations.append(anim_i)
        self.play(ApplyMethod(grid4.coordinate.fade), ApplyMethod(grid4.group_remainders.fade), ApplyMethod(grid4.group_dots.fade), Indicate(grid4.coordinate.y_axis), *animations)
        self.wait(0.52) #大家看最左边一列

        self.play(Flash(grid4.remainders[0][2], flash_radius=0.5), ApplyMethod(grid4.remainders[0][2].set_color, YELLOW), run_time = 0.56)
        self.wait(0.42) #12正好是...
        self.play(Flash(grid4.remainders[0][1], flash_radius=0.5), ApplyMethod(grid4.remainders[0][1].set_color, YELLOW), run_time = 0.56)
        self.wait(0.34) #...6的两倍
        self.wait(0.44) #（空闲）

        self.wait(1.71) #这是一个巧合吗
        self.play(ApplyMethod(grid4.remainder_type.shift, 3*LEFT))
        grid4.remainder_others.shift(3*LEFT)
        self.wait(0.47) #其实不是
        
        module_base_1_1 = Module(r"6", r"0", r"3")
        module_base_1_2 = Module(r"6", r"1", r"5")
        module_base_1_1.shift(0.4*UP)
        module_base_1_2.shift(0.4*DOWN)
        module_base_1 = VGroup(module_base_1_1, module_base_1_2)
        module_base_1.shift(np.array([3, 2, 0]))
        frame_base_1 = SurroundingRectangle(module_base_1, stroke_color = WHITE)

        equation_line_1 = Line(np.array([3, 1, 0]), np.array([3, 1, 0]))

        factor_1_1 = Tex(r"2\times")
        factor_1_1.shift(np.array([0.8, 2, 0]))
        module_result_1_1 = Module(r"12", r"0", r"3")
        module_result_1_2 = Module(r"12", r"2", r"5")
        module_result_1_1.shift(0.4*UP)
        module_result_1_2.shift(0.4*DOWN)
        module_result_1 = VGroup(module_result_1_1, module_result_1_2)
        module_result_1.shift(np.array([3, 0, 0]))
        module_with_factor_1_1 = VGroup(factor_1_1, module_base_1_1)
        module_with_factor_1_2 = VGroup(factor_1_1, module_base_1_2)

        factor_1_2 = Tex(r"3\times")
        factor_1_2.shift(np.array([0.8, 2, 0]))
        module_result_2_1 = Module(r"18", r"0", r"3")
        module_result_2_2 = Module(r"18", r"3", r"5")
        module_result_2_1.shift(0.4*UP)
        module_result_2_2.shift(0.4*DOWN)
        module_result_2 = VGroup(module_result_2_1, module_result_2_2)
        module_result_2.shift(np.array([3, 0, 0]))
        module_calculate_2 = Module(r"18", r"3", r"15")
        module_calculate_2.shift(np.array([3, -2, 0]))

        factor_1_3 = Tex(r"4\times")
        factor_1_3.shift(np.array([0.8, 2, 0]))
        module_result_3_1 = Module(r"24", r"0", r"3")
        module_result_3_2 = Module(r"24", r"4", r"5")
        module_result_3_1.shift(0.4*UP)
        module_result_3_2.shift(0.4*DOWN)
        module_result_3 = VGroup(module_result_3_1, module_result_3_2)
        module_result_3.shift(np.array([3, 0, 0]))
        module_calculate_3 = Module(r"24", r"9", r"15")
        module_calculate_3.shift(np.array([3, -2, 0]))
        
        self.play(FadeIn(module_base_1_1, DOWN))
        self.wait(0.62) #6是3的倍数
        self.play(FadeIn(module_base_1_2, UP))
        self.wait(0.80) #而且除以5余1
        self.wait(0.42) #（空闲）
        self.play(FadeIn(frame_base_1), FadeIn(factor_1_1))
        self.wait(1.01) #那么如果把6乘以2
        self.add(equation_line_1)
        self.play(TransformFromCopy(module_with_factor_1_1, module_result_1_1), ApplyMethod(equation_line_1.put_start_and_end_on, np.array([0,1,0]), np.array([6,1,0]) ))
        self.wait(1.46) #12就应该也是3的倍数
        self.play(TransformFromCopy(module_with_factor_1_2, module_result_1_2))
        self.wait(0.76) #而且除以5余2
        self.wait(0.71) #（空闲）

        self.wait(1.32) #按照这个思路
        self.play(ReplacementTransform(factor_1_1, factor_1_2), ReplacementTransform(module_result_1, module_result_2))
        self.wait(1.58) #再上面一格应该是18

        self.play(FadeIn(module_calculate_2, UP))
        self.wait(1.78) #18除以15 余数是3
        self.play(Flash(grid4.remainders[0][3], flash_radius=0.5), ApplyMethod(grid4.remainders[0][3].set_color, YELLOW))
        self.wait(0.03) #正好满足
        self.wait(0.59) #（空闲）
        self.play(FadeOut(module_calculate_2, DOWN), ReplacementTransform(factor_1_2, factor_1_3), ReplacementTransform(module_result_2, module_result_3))
        self.wait(0.43) #再上面一格
        self.play(FadeIn(module_calculate_3, UP))
        self.wait(1.79) #24除以15 余数是9
        self.play(Flash(grid4.remainders[0][4], flash_radius=0.5), ApplyMethod(grid4.remainders[0][4].set_color, YELLOW))
        self.wait(0.33) #正好也满足
        self.wait(0.87) #（空闲）
        
        module_base_2_1 = Module(r"10", r"1", r"3")
        module_base_2_2 = Module(r"10", r"0", r"5")
        module_base_2_1.shift(0.4*UP)
        module_base_2_2.shift(0.4*DOWN)
        module_base_2 = VGroup(module_base_2_1, module_base_2_2)
        module_base_2.shift(np.array([3, 0, 0]))
        frame_base_2 = SurroundingRectangle(module_base_2, stroke_color = WHITE)
        equation_line_2 = Line(np.array([3, -1, 0]), np.array([3, -1, 0]))
        module_basis = VGroup(module_base_1, module_base_2)

        factor_2_4 = Tex(r"2\times")
        factor_2_4.shift(np.array([0.8, 0, 0]))
        module_result_4_1 = Module(r"20", r"2", r"3")
        module_result_4_2 = Module(r"20", r"0", r"5")
        module_result_4_1.shift(0.4*UP)
        module_result_4_2.shift(0.4*DOWN)
        module_result_4 = VGroup(module_result_4_1, module_result_4_2)
        module_result_4.shift(np.array([3, -2, 0]))
        module_calculate_4 = Module(r"20", r"5", r"15")
        module_calculate_4.shift(np.array([3, -3, 0]))
        module_with_factor_4_1 = VGroup(factor_2_4, module_base_2_1)
        module_with_factor_4_2 = VGroup(factor_2_4, module_base_2_2)

        
        mobs = [grid4.coordinate.x_axis, grid4.dots[1][0], grid4.dots[2][0], grid4.remainders[1][0], grid4.remainders[2][0]]
        targets_1 = []
        targets_2 = []
        for i in range(5):
            target = mobs[i].copy()
            target.scale(1.2)
            target.set_color(YELLOW)
            target.set_opacity(1)
            targets_1.append(target)
            target = mobs[i].copy()
            target.set_opacity(1)
            targets_2.append(target)
        animations = []
        for i in range (5):
            anim_a = Transform(mobs[i], targets_1[i])
            anim_b = Transform(mobs[i], targets_2[i])
            anims = Succession(anim_a, anim_b)
            animations.append(anims)
        self.play(*animations, FadeOut(module_calculate_3, DOWN), FadeOut(module_result_3, DOWN), FadeOut(equation_line_1, RIGHT), FadeOut(frame_base_1, UP), FadeOut(factor_1_3, UP), ApplyMethod(module_base_1.fade), run_time = 1)
        self.play(FadeIn(module_base_2_1, DOWN), FadeIn(module_base_2_2, UP), ApplyMethod(grid4.remainders[1][0].set_color, YELLOW), Flash(grid4.remainders[1][0], flash_radius=0.5))
        self.wait(0.24) #最下面一行也是一样

        
        self.play(FadeIn(frame_base_2), FadeIn(factor_2_4), run_time = 0.5)
        self.add(equation_line_2)
        self.play(TransformFromCopy(module_with_factor_4_1, module_result_4_1), TransformFromCopy(module_with_factor_4_2, module_result_4_2), ApplyMethod(equation_line_2.put_start_and_end_on, np.array([0,-1,0]), np.array([6,-1,0]) ))
        self.wait(0.40) #20是10的两倍
        self.wait(1.86) #除以15余5
        self.wait(1.50)
        self.play(Flash(grid4.remainders[2][0], flash_radius=0.5), ApplyMethod(grid4.remainders[2][0].set_color, YELLOW))
        self.wait(0.10) #所以10的右边一个位置就是5
        self.wait(0.87) #（空闲）

        plus_symbol = Tex(r"+")
        plus_symbol.shift(np.array([3, 1, 0]))

        self.play(FadeOut(module_result_4, DOWN), FadeOut(factor_2_4, LEFT), FadeIn(frame_base_1, DOWN), FadeIn(plus_symbol), ApplyMethod(module_base_1.set_opacity, 1))
        self.wait(0.61) #让我们更大胆一点吧
        self.wait(0.61) #（空闲）

        factor_1_5 = Tex(r"1\times")
        factor_1_5.shift(np.array([0.8, 2, 0]))
        factor_2_5 = Tex(r"1\times")
        factor_2_5.shift(np.array([0.8, 0, 0]))
        module_result_5_1 = Module(r"16", r"1", r"3")
        module_result_5_2 = Module(r"16", r"1", r"5")
        module_result_5_1.shift(0.4*UP)
        module_result_5_2.shift(0.4*DOWN)
        module_result_5 = VGroup(module_result_5_1, module_result_5_2)
        module_result_5.shift(np.array([3, -2, 0]))
        module_with_factor_5 = VGroup(module_basis, factor_1_5, factor_2_5)

        self.play(FadeIn(factor_1_5, RIGHT))
        self.wait(0.70) #一个除以5余1
        self.play(FadeIn(factor_2_5, RIGHT))
        self.wait(0.75) #除以3余1的数
        
        self.wait(0.50)
        self.play(TransformFromCopy(module_with_factor_5, module_result_5))
        self.wait(1.47) #应该是10加6 16

        target = grid4.remainders[1][1].copy()
        target.set_color(YELLOW)
        target.set_opacity(1)
        self.play(Flash(grid4.remainders[1][1], flash_radius=0.5), Transform(grid4.remainders[1][1], target), ApplyMethod(grid4.dots[1][1].set_opacity, 1))
        self.wait(1.85+0.56-2) #除以15正好余1
        self.play(FadeOut(module_result_5), FadeOut(factor_1_5), FadeOut(factor_2_5))

        factor_1_6 = Tex(r"3\times")
        factor_1_6.shift(np.array([0.8, 2, 0]))
        factor_2_6 = Tex(r"2\times")
        factor_2_6.shift(np.array([0.8, 0, 0]))
        module_result_6_1 = Module(r"38", r"2", r"3")
        module_result_6_2 = Module(r"38", r"3", r"5")
        module_result_6_1.shift(0.4*UP)
        module_result_6_2.shift(0.4*DOWN)
        module_result_6 = VGroup(module_result_6_1, module_result_6_2)
        module_result_6.shift(np.array([3, -2, 0]))
        module_with_factor_6 = VGroup(module_basis, factor_1_6, factor_2_6)

        self.play(FadeIn(factor_1_6, RIGHT))
        self.wait(0.66) #一个除以5余3
        self.play(FadeIn(factor_2_6, RIGHT))
        self.wait(0.70) #除以3余2的数
        
        self.wait(0.50)
        self.play(TransformFromCopy(module_with_factor_6, module_result_6))
        self.wait(1.66) #应该是18加20 38

        target = grid4.remainders[2][3].copy()
        target.set_color(YELLOW)
        target.set_opacity(1)
        self.play(Flash(grid4.remainders[2][3], flash_radius=0.5), Transform(grid4.remainders[2][3], target), ApplyMethod(grid4.dots[2][3].set_opacity, 1))
        self.wait(1.92+0.68-2) #除以15正好余8
        self.play(FadeOut(module_result_6), FadeOut(factor_1_6), FadeOut(factor_2_6))

        factor_1_7 = Tex(r"a\times")
        factor_1_7.shift(np.array([0.8, 2, 0]))
        factor_2_7 = Tex(r"b\times")
        factor_2_7.shift(np.array([0.8, 0, 0]))
        module_result_7_1 = Module(r"a\times 6+b\times 10", r"b", r"3")
        module_result_7_1.dividend.next_to(module_result_7_1.modulesymbol.get_corner(LEFT), LEFT)
        module_result_7_2 = Module(r"a\times 6+b\times 10", r"a", r"5")
        module_result_7_2.dividend.next_to(module_result_7_2.modulesymbol.get_corner(LEFT), LEFT)
        module_result_7_1.shift(0.4*UP)
        module_result_7_2.shift(0.4*DOWN)
        module_result_7 = VGroup(module_result_7_1, module_result_7_2)
        module_result_7.shift(np.array([3, -2, 0]))
        module_with_factor_7 = VGroup(module_basis, factor_1_7, factor_2_7)

        self.play(FadeIn(factor_1_7, RIGHT), FadeIn(factor_2_7, RIGHT))
        self.wait(0.72) #我们想要的任何答案
        
        self.wait(0.50)
        self.play(TransformFromCopy(module_with_factor_7, module_result_7))
        self.wait(0.37) #只要分别乘以10和6

        target = grid4.group_remainders.copy()
        target.set_color(YELLOW)
        target.set_opacity(1)
        self.play(Transform(grid4.group_remainders, target), ApplyMethod(grid4.group_dots.set_opacity, 1))
        self.wait(0.12) #都可以算出
        self.wait(1.08) #（空闲）

        self.remove(module_with_factor_7, plus_symbol, frame_base_1, frame_base_2, module_result_7, equation_line_2)

        base_vector_1 = Tex(r"10 = \binom{1}{0}", color = GREEN)
        base_vector_2 = Tex(r"6 = \binom{0}{1}", color = YELLOW)
        base_vector_1.shift(np.array([1,1,0]))
        base_vector_2.shift(np.array([4,1,0]))
        vector_arrow_1 = Arrow(np.array([-4, -1, 0]), np.array([-3, -1, 0]), buff = 0, stroke_color = GREEN)
        vector_arrow_2 = Arrow(np.array([-4, -1, 0]), np.array([-4, 0, 0]), buff = 0, stroke_color = YELLOW)
        vector = Tex(r"\binom{a}{b} &= a\times \binom{1}{0}+b\times \binom{0}{1}\\ &= a\times 10+b\times 6")
        vector.shift(np.array([2.5,-1,0]))

        self.play(ReplacementTransform(notice3, notice4))
        self.wait(0.82) #用线性代数的话来说
        self.play(FadeIn(base_vector_1), FadeIn(base_vector_2), FadeIn(vector_arrow_1), FadeIn(vector_arrow_2))
        self.wait(1.81) #10 和6 就是一组基向量
        self.wait(0.66) #（空闲）
        
        self.play(WiggleOutThenIn(vector_arrow_1), WiggleOutThenIn(vector_arrow_2), run_time = 1.5)
        self.wait(0.10) #用这组基向量
        self.play(Write(vector))
        self.wait(0.58) #我们就可以很简单地通过余数
        self.wait(1.31) #直接求出解来
        self.wait(0.87) #（空闲）

        self.remove(vector_arrow_1, vector_arrow_2, vector, grid4, base_vector_1, base_vector_2)
        """

        # 第一节4-2
        """
        self.add(notice4)
        self.play(ReplacementTransform(notice4, notice5))
        self.wait(1.39) #这不仅对于两个数是有效的

        module_equation_1 = Module(r"x", r"a_1", r"m_1")
        module_equation_2 = Module(r"x", r"a_2", r"m_2")
        module_equation_3 = Module(r"x", r"a_3", r"m_3")
        module_equation_4 = Tex(r"\cdots")
        module_equation_5 = Module(r"x", r"a_n", r"m_n")
        module_equation_1.shift(2*UP)
        module_equation_2.shift(1*UP)
        module_equation_4.shift(1*DOWN)
        module_equation_5.shift(2*DOWN)
        module_equations = VGroup(module_equation_1, module_equation_2, module_equation_3, module_equation_4, module_equation_5)
        module_equations.shift(3*LEFT)
        module_equations_divisors = VGroup(module_equation_1.divisor, module_equation_2.divisor, module_equation_3.divisor, module_equation_5.divisor)

        self.play(Write(module_equations))
        self.wait(2.17) #更一般地 它可以用来解任何的同余方程组

        module_equation_base1_1 = Module(r"\vec{e}_1", r"1", r"m_1")
        module_equation_base1_2 = Module(r"\vec{e}_1", r"0", r"m_2")
        module_equation_base1_3 = Module(r"\vec{e}_1", r"0", r"m_3")
        module_equation_base1_4 = Tex(r"\cdots")
        module_equation_base1_5 = Module(r"\vec{e}_1", r"0", r"m_n")
        module_equation_base1_1.shift(2*UP)
        module_equation_base1_2.shift(1*UP)
        module_equation_base1_4.shift(1*DOWN)
        module_equation_base1_5.shift(2*DOWN)
        module_equations_base1 = VGroup(module_equation_base1_1, module_equation_base1_2, module_equation_base1_3, module_equation_base1_4, module_equation_base1_5)
        module_equations_base1.shift(2.8*RIGHT)

        module_equation_base2_1 = Module(r"\vec{e}_2", r"0", r"m_1")
        module_equation_base2_2 = Module(r"\vec{e}_2", r"1", r"m_2")
        module_equation_base2_3 = Module(r"\vec{e}_2", r"0", r"m_3")
        module_equation_base2_4 = Tex(r"\cdots")
        module_equation_base2_5 = Module(r"\vec{e}_2", r"0", r"m_n")
        module_equation_base2_1.shift(2*UP)
        module_equation_base2_2.shift(1*UP)
        module_equation_base2_4.shift(1*DOWN)
        module_equation_base2_5.shift(2*DOWN)
        module_equations_base2 = VGroup(module_equation_base2_1, module_equation_base2_2, module_equation_base2_3, module_equation_base2_4, module_equation_base2_5)
        module_equations_base2.shift(2.8*RIGHT)

        module_equation_base3_1 = Module(r"\vec{e}_n", r"0", r"m_1")
        module_equation_base3_2 = Module(r"\vec{e}_n", r"0", r"m_2")
        module_equation_base3_3 = Module(r"\vec{e}_n", r"0", r"m_3")
        module_equation_base3_4 = Tex(r"\cdots")
        module_equation_base3_5 = Module(r"\vec{e}_n", r"1", r"m_n")
        module_equation_base3_1.shift(2*UP)
        module_equation_base3_2.shift(1*UP)
        module_equation_base3_4.shift(1*DOWN)
        module_equation_base3_5.shift(2*DOWN)
        module_equations_base3 = VGroup(module_equation_base3_1, module_equation_base3_2, module_equation_base3_3, module_equation_base3_4, module_equation_base3_5)
        module_equations_base3.shift(2.8*RIGHT)

        module_equations_basis = Module(r"\vec{e}_i", r"\delta_{ij}", r"m_j")
        module_equations_basis.shift(2.8*RIGHT+2*UP)

        self.play(FadeIn(module_equations_base1), run_time = 3.44/4)
        self.play(Transform(module_equations_base1, module_equations_base2), run_time = 3.44/4)
        self.play(Transform(module_equations_base1, module_equations_base3), run_time = 3.44/4)
        self.play(Transform(module_equations_base1, module_equations_basis), run_time = 3.44/4) #只要我们知道了每个数所对应的基向量的值

        module_equations_solution = Module(r"x", r"\sum_{i=1}^na_i\vec{e}_i", r"\prod_{i=1}^nm_i")
        module_equations_solution.shift(2.5*RIGHT)

        self.play(Write(module_equations_solution))
        self.wait(0.98) #我们就可以把同余方程组解出来

        self.play(Indicate(module_equations_divisors), run_time = 2)
        self.wait(0.01) #当这些数互质的时候
        self.wait(1.90) #基向量总是存在的
        self.wait(0.65) #（空闲）

        self.remove(module_equations_solution, module_equations_base1, module_equations)
        self.play(ReplacementTransform(notice5, notice6))
        self.wait(0.64) #那句知名口诀

        quote_1 = Text("三人同行七十稀，五树梅花廿一支。\n七子团圆正月半，除百零五便得知。", font = 'simsun')
        quote_2 = Text("三人同行七十稀，五树梅花廿一支。\n七子团圆正月半，除百零五便得知。", font = 'simsun', t2c={"七十": GREEN})
        quote_3 = Text("三人同行七十稀，五树梅花廿一支。\n七子团圆正月半，除百零五便得知。", font = 'simsun', t2c={"廿一": GREEN, "七十": GREEN})
        quote_4 = Text("三人同行七十稀，五树梅花廿一支。\n七子团圆正月半，除百零五便得知。", font = 'simsun', t2c={"月半": GREEN, "廿一": GREEN, "七十": GREEN})
        quotes = VGroup(quote_1, quote_2, quote_3, quote_4)
        author = Text("——程大位《算法统宗》", color = YELLOW, font = 'simsun')
        quotes.shift(2*UP)
        author.next_to(quote_1.get_corner(DOWN + RIGHT), 1.1*DOWN+0.3*LEFT)

        module_example_base1_1 = Module(r"70", r"1", r"3")
        module_example_base1_2 = Module(r"70", r"0", r"5")
        module_example_base1_3 = Module(r"70", r"0", r"7")
        module_example_base1_1.shift(UP)
        module_example_base1_3.shift(DOWN)
        module_example_base1 = VGroup(module_example_base1_1, module_example_base1_2, module_example_base1_3)
        module_example_base1.scale(0.6)
        module_example_base1.shift(DOWN+3*LEFT)
        frame_example_1 = SurroundingRectangle(module_example_base1_1, stroke_color = YELLOW)

        module_example_base2_1 = Module(r"21", r"0", r"3")
        module_example_base2_2 = Module(r"21", r"1", r"5")
        module_example_base2_3 = Module(r"21", r"0", r"7")
        module_example_base2_1.shift(UP)
        module_example_base2_3.shift(DOWN)
        module_example_base2 = VGroup(module_example_base2_1, module_example_base2_2, module_example_base2_3)
        module_example_base2.scale(0.6)
        module_example_base2.shift(DOWN)
        frame_example_2 = SurroundingRectangle(module_example_base2_2, stroke_color = YELLOW)

        module_example_base3_1 = Module(r"15", r"0", r"3")
        module_example_base3_2 = Module(r"15", r"0", r"5")
        module_example_base3_3 = Module(r"15", r"1", r"7")
        module_example_base3_1.shift(UP)
        module_example_base3_3.shift(DOWN)
        module_example_base3 = VGroup(module_example_base3_1, module_example_base3_2, module_example_base3_3)
        module_example_base3.scale(0.6)
        module_example_base3.shift(DOWN+3*RIGHT)
        frame_example_3 = SurroundingRectangle(module_example_base3_3, stroke_color = YELLOW)
        

        self.play(Write(quote_1))
        self.play(Write(author))
        self.wait(2.12-3+2.17) #三人同行七十稀 五树梅花廿一支
        self.wait(2.09) #七子团圆正月半
        self.wait(2.26) #除百零五便得知

        self.wait(0.77)
        self.play(FadeIn(module_example_base1), Transform(quote_1, quote_2), run_time = 0.5)
        self.wait(0.66)
        self.play(FadeIn(module_example_base2), Transform(quote_1, quote_3), run_time = 0.5)
        self.wait(0.47)
        self.play(FadeIn(module_example_base3), Transform(quote_1, quote_4), run_time = 0.5)
        self.wait(0.77) #其中的70 21 和15

        self.wait(0.48)
        self.play(FadeIn(frame_example_1), run_time = 0.5)
        self.wait(0.39)
        self.play(FadeIn(frame_example_2), run_time = 0.5)
        self.wait(0.15)
        self.play(FadeIn(frame_example_3), run_time = 0.5)
        self.wait(2.11) #就是3 5 7对应的基向量
        self.wait(0.82)
        #到此为止共120秒
        """

        # 第一节-5
        """
        self.add(notice6)
        self.play(ReplacementTransform(notice6, notice7))
        self.wait(2.26) #这些好用的基向量是怎么算出来的呢

        grid4 = FiniteNumberPlane(3,5)
        grid4.shift(3*LEFT + UP)
        self.play(Write(grid4.remainder_type))
        self.wait(0.13) #让我们回到3乘5的表格上来
        self.wait(0.69) #（空闲）

        module_base_5_1 = Module(r"\binom{0}{1}", r"0", r"3")
        module_base_5_1.dividend.set_color(YELLOW)
        module_base_5_1.shift(2.5*RIGHT+2.4*UP)
        vector_arrow_1 = Arrow(np.array([-4, -1, 0]), np.array([-3, -1, 0]), buff = 0, stroke_color = GREEN)
        vector_arrow_2 = Arrow(np.array([-4, -1, 0]), np.array([-4, 0, 0]), buff = 0, stroke_color = YELLOW)
        self.play(FadeIn(module_base_5_1.dividend), FadeIn(vector_arrow_2)) 
        self.wait(1.04) #想要成为5的基向量
        self.play(FadeIn(module_base_5_1.dividend_others))
        self.wait(1.68) #那么这个数就得是3的倍数

        module_base_5_1_instead_1 = Tex(r"3", color = GREEN)
        module_base_5_1_instead_1.next_to(module_base_5_1.modulesymbol.get_corner(LEFT), LEFT)
        self.play(Transform(module_base_5_1.dividend, module_base_5_1_instead_1))
        self.wait(0.66) #3行不行呢

        module_base_5_2 = Module(r"3", r"3", r"5")
        module_base_5_2.shift(2.5*RIGHT+1.6*UP)
        self.wait(1.00)
        self.play(FadeIn(module_base_5_2, UP), Flash(grid4.remainders[0][3], flash_radius=0.5))
        self.wait(1.67) #很可惜 3除以5余3 不余1
        self.wait(0.66) #（空闲）

        module_inverse_text_1 = Text("如果", font = "simsun")
        module_inverse_1 = Tex(r"ab\equiv 1\ (\bmod\ m)", color = GREEN)
        module_inverse_text_2 = Text("，定义", font = "simsun")
        module_inverse_2 = Tex(r"a^{-1}\equiv b\ (\bmod\ m)", color = YELLOW)
        module_inverse_text_3 = Text("。", font = "simsun")
        module_inverse_text_1.shift(5*LEFT)
        module_inverse_1.shift(2.5*LEFT)
        module_inverse_text_2.shift(0.2*RIGHT)
        module_inverse_2.shift(3.2*RIGHT)
        module_inverse_text_3.shift(5.3*RIGHT+0.2*DOWN)
        module_inverse = VGroup(module_inverse_text_1, module_inverse_1, module_inverse_text_2, module_inverse_2, module_inverse_text_3)
        module_inverse.shift(1*UP)
        module_division_with_inverse = Tex(r"14\divisionsymbol 3\equiv 4\times 3^{-1}\equiv 4\times 2\equiv 3\ (\bmod\ 5)")
        module_division_with_inverse.shift(DOWN)

        self.remove(grid4.remainder_type, module_base_5_1, module_base_5_2, vector_arrow_2)
        self.play(Write(module_inverse), Write(module_division_with_inverse), ReplacementTransform(notice7, notice8))
        self.wait(1.98) #但是 我们之前刚刚见过“数论倒数”

        module_base_5_3 = Module(r"2", r"3^{-1}", r"5")
        module_base_5_3.shift(2.5*RIGHT+0.5*UP)
        self.remove(module_inverse, module_division_with_inverse)
        self.add(grid4.remainder_type, module_base_5_1, module_base_5_2, vector_arrow_2)
        self.play(ReplacementTransform(notice8, notice9), FadeIn(module_base_5_3, UP))
        self.wait(1.67) #3关于5的数论倒数是2

        module_base_5 = VGroup(module_base_5_1, module_base_5_2)
        frame_base_5 = SurroundingRectangle(module_base_5, stroke_color = WHITE)
        factor_base_5 = Tex(r"2\times")
        factor_base_5.next_to(frame_base_5.get_corner(LEFT), LEFT)
        self.play(FadeIn(frame_base_5), ReplacementTransform(module_base_5_3.dividend, factor_base_5), FadeOut(module_base_5_3.dividend_others), run_time = 1)
        self.wait(1.39) #那么只要我们给3乘上2

        module_base_5_1_instead_2 = Module(r"6", r"0", r"3")
        module_base_5_1_instead_2.shift(2.5*RIGHT+2.4*UP)
        module_base_5_2_instead_2 = Module(r"6", r"1", r"5")
        module_base_5_2_instead_2.shift(2.5*RIGHT+1.6*UP)
        module_basis_5_instead_2 = VGroup(module_base_5_1_instead_2.dividend, module_base_5_2_instead_2.dividend, module_base_5_1_instead_2.remainder, module_base_5_2_instead_2.remainder)
        self.play(Transform(module_base_5_1, module_base_5_1_instead_2), Transform(module_base_5_2, module_base_5_2_instead_2), Transform(factor_base_5, module_basis_5_instead_2))
        self.remove(factor_base_5)
        self.wait(1.28) #就能得到5的基向量

        
        module_base_3_1 = Module(r"5", r"2", r"3")
        module_base_3_1.shift(2.5*RIGHT+0.4*UP)
        module_base_3_2 = Module(r"5", r"0", r"5")
        module_base_3_2.shift(2.5*RIGHT+0.4*DOWN)
        module_base_3_3 = Module(r"2", r"5^{-1}", r"3")
        module_base_3_3.shift(2.5*RIGHT+1.5*DOWN)
        self.wait(0.85)
        self.play(FadeIn(module_base_3_1, UP), FadeIn(module_base_3_2, UP), FadeIn(module_base_3_3, UP), FadeIn(vector_arrow_1))
        self.wait(1.46) #同样 5关于3的数论倒数是2

        module_base_3 = VGroup(module_base_3_1, module_base_3_2)
        frame_base_3 = SurroundingRectangle(module_base_3, stroke_color = WHITE)
        factor_base_3 = Tex(r"2\times")
        factor_base_3.next_to(frame_base_3.get_corner(LEFT), LEFT)
        self.play(FadeIn(frame_base_3), ReplacementTransform(module_base_3_3.dividend, factor_base_3), FadeOut(module_base_3_3.dividend_others), run_time = 1)
        self.wait(1.22) #那么只要我们给5乘上2

        module_base_3_1_instead_2 = Module(r"10", r"1", r"3")
        module_base_3_1_instead_2.shift(2.5*RIGHT+0.4*UP)
        module_base_3_2_instead_2 = Module(r"10", r"0", r"5")
        module_base_3_2_instead_2.shift(2.5*RIGHT+0.4*DOWN)
        module_basis_3_instead_2 = VGroup(module_base_3_1_instead_2.dividend, module_base_3_2_instead_2.dividend, module_base_3_1_instead_2.remainder, module_base_3_2_instead_2.remainder)
        self.play(Transform(module_base_3_1, module_base_3_1_instead_2), Transform(module_base_3_2, module_base_3_2_instead_2), Transform(factor_base_3, module_basis_3_instead_2), ApplyMethod(frame_base_3.scale, 1.1), run_time = 1)
        self.remove(factor_base_3)
        self.wait(1.83) #就能得到5的基向量

        self.remove(grid4.remainder_type, module_base_5_1, module_base_5_2, vector_arrow_2, frame_base_5, module_base_3_1, module_base_3_2, vector_arrow_1, frame_base_3)

        example_3_5_7 = Tex(r"m_1=3\qquad m_2=5\qquad m_3=7", color = YELLOW)
        example_3_5_7.shift(3*UP)

        example_base_vector_1 = Tex(r"\vec{e}_1", color = ORANGE)
        example_base_vector_1.shift(2.25*UP+1.7*LEFT)
        example_base_vector_1_calculating = Tex(r"&=M_1\times[M_1]^{-1}_{\bmod\ 3}\\&=35\times2\\&=70")
        example_base_vector_1_calculating.shift(1.6*UP+0.8*RIGHT)
        multiply_1 = Tex(r"M_1=5\times 7=35")
        multiply_1.shift(0.1*UP)
        example_base_1_module_1 = Module(r"M_1", r"2", r"3")
        example_base_1_module_2 = Module(r"M_1", r"0", r"5")
        example_base_1_module_3 = Module(r"M_1", r"0", r"7")
        example_base_1_module_1.shift(0.7*DOWN)
        example_base_1_module_2.shift(1.5*DOWN)
        example_base_1_module_3.shift(2.3*DOWN)
        example_base_1_modules = VGroup(example_base_1_module_1, example_base_1_module_2, example_base_1_module_3)
        example_inverse_1 = Module(r"M_1^{-1}", r"2", r"3")
        example_inverse_1.shift(3.1*DOWN)
        example_frame_1 = SurroundingRectangle(example_base_1_modules, stroke_color = WHITE)
        example_factor_1 = Tex(r"2\times")
        example_factor_1.next_to(example_frame_1, LEFT)

        calculation_1 = VGroup(example_base_vector_1, example_base_vector_1_calculating, multiply_1, example_base_1_modules, example_inverse_1, example_frame_1, example_factor_1)
        calculation_1.scale(0.8)
        calculation_1.shift(4.5*LEFT)

        example_base_vector_2 = Tex(r"\vec{e}_2", color = ORANGE)
        example_base_vector_2.shift(2.25*UP+1.7*LEFT)
        example_base_vector_2_calculating = Tex(r"&=M_2\times[M_2]^{-1}_{\bmod\ 5}\\&=21\times1\\&=21")
        example_base_vector_2_calculating.shift(1.6*UP+0.8*RIGHT)
        multiply_2 = Tex(r"M_2=3\times 7=21")
        multiply_2.shift(0.1*UP)
        example_base_2_module_1 = Module(r"M_2", r"0", r"3")
        example_base_2_module_2 = Module(r"M_2", r"1", r"5")
        example_base_2_module_3 = Module(r"M_2", r"0", r"7")
        example_base_2_module_1.shift(0.7*DOWN)
        example_base_2_module_2.shift(1.5*DOWN)
        example_base_2_module_3.shift(2.3*DOWN)
        example_base_2_modules = VGroup(example_base_2_module_1, example_base_2_module_2, example_base_2_module_3)
        example_inverse_2 = Module(r"M_2^{-1}", r"1", r"5")
        example_inverse_2.shift(3.1*DOWN)
        example_frame_2 = SurroundingRectangle(example_base_2_modules, stroke_color = WHITE)
        example_factor_2 = Tex(r"1\times")
        example_factor_2.next_to(example_frame_2, LEFT)

        calculation_2 = VGroup(example_base_vector_2, example_base_vector_2_calculating, multiply_2, example_base_2_modules, example_inverse_2, example_frame_2, example_factor_2)
        calculation_2.scale(0.8)

        example_base_vector_3 = Tex(r"\vec{e}_3", color = ORANGE)
        example_base_vector_3.shift(2.25*UP+1.7*LEFT)
        example_base_vector_3_calculating = Tex(r"&=M_3\times[M_3]^{-1}_{\bmod\ 7}\\&=15\times1\\&=15")
        example_base_vector_3_calculating.shift(1.6*UP+0.8*RIGHT)
        multiply_3 = Tex(r"M_3=3\times 5=15")
        multiply_3.shift(0.1*UP)
        example_base_3_module_1 = Module(r"M_3", r"0", r"3")
        example_base_3_module_2 = Module(r"M_3", r"0", r"5")
        example_base_3_module_3 = Module(r"M_3", r"1", r"7")
        example_base_3_module_1.shift(0.7*DOWN)
        example_base_3_module_2.shift(1.5*DOWN)
        example_base_3_module_3.shift(2.3*DOWN)
        example_base_3_modules = VGroup(example_base_3_module_1, example_base_3_module_2, example_base_3_module_3)
        example_inverse_3 = Module(r"M_3^{-1}", r"1", r"7")
        example_inverse_3.shift(3.1*DOWN)
        example_frame_3 = SurroundingRectangle(example_base_3_modules, stroke_color = WHITE)
        example_factor_3 = Tex(r"1\times")
        example_factor_3.next_to(example_frame_3, LEFT)

        calculation_3 = VGroup(example_base_vector_3, example_base_vector_3_calculating, multiply_3, example_base_3_modules, example_inverse_3, example_frame_3, example_factor_3)
        calculation_3.scale(0.8)
        calculation_3.shift(4.5*RIGHT)

        self.play(Write(example_3_5_7))
        self.wait(0.31) #对于n个数的情况而言呢
        
        self.play(Write(example_base_vector_1), run_time = 1)
        self.wait(1.24) #想要成为m1的基向量
        self.play(FadeIn(example_base_1_module_2.dividend_others), FadeIn(example_base_1_module_3.dividend_others))
        self.wait(1.83) #就必须要是其它所有数的公倍数
        self.wait(1.26) #最简单的
        self.play(Write(multiply_1), run_time = 1)
        self.play(FadeIn(example_base_1_module_2.dividend), FadeIn(example_base_1_module_3.dividend), FadeIn(example_base_1_module_1))
        self.wait(0.77) #就是先把剩下的数全部乘起来
        self.wait(0.85)
        self.play(Write(example_inverse_1), run_time = 1)
        self.play(FadeIn(example_frame_1), FadeIn(example_factor_1))
        self.wait(0.88) #之后 再为它乘上自己的数论倒数
        self.play(Write(example_base_vector_1_calculating), run_time = 2)
        self.wait(1.33) #这样我们就求出了m1的基向量的值

        self.play(Write(example_base_vector_2), Write(example_base_vector_3), run_time = 1)
        self.wait(1)
        self.play(FadeIn(example_base_2_module_1.dividend_others), FadeIn(example_base_2_module_3.dividend_others), FadeIn(example_base_3_module_1.dividend_others), FadeIn(example_base_3_module_2.dividend_others))
        self.wait(1)
        self.play(Write(multiply_2), Write(multiply_3), run_time = 1)
        self.play(FadeIn(example_base_2_module_1.dividend), FadeIn(example_base_2_module_3.dividend), FadeIn(example_base_2_module_2), FadeIn(example_base_3_module_1.dividend), FadeIn(example_base_3_module_2.dividend), FadeIn(example_base_3_module_3))
        self.wait(1)
        self.play(Write(example_inverse_2), Write(example_inverse_3), run_time = 1)
        self.play(FadeIn(example_frame_2), FadeIn(example_factor_2), FadeIn(example_frame_3), FadeIn(example_factor_3))
        self.wait(1)
        self.play(Write(example_base_vector_2_calculating), Write(example_base_vector_3_calculating), run_time = 2)
        self.wait(4.06) #其它基向量的求法也是这样

        print(self.get_time())
        self.remove(example_3_5_7, calculation_1, calculation_2, calculation_3)
        
        title2 = Text("中国剩余定理", font = 'simsun', color = YELLOW)
        title2.shift(3.5*UP)
        title2_line = Line(np.array([0,3,0]), np.array([0,3,0]))

        text_1 = Text("对于同余方程组", font = 'simsun')
        module_equation_1 = Module(r"x", r"a_1", r"m_1")
        module_equation_2 = Module(r"x", r"a_2", r"m_2")
        module_equation_3 = Module(r"x", r"a_3", r"m_3")
        module_equation_4 = Tex(r"\cdots")
        module_equation_5 = Module(r"x", r"a_n", r"m_n")
        module_equation_1.shift(1.6*UP)
        module_equation_2.shift(0.8*UP)
        module_equation_4.shift(0.8*DOWN)
        module_equation_5.shift(1.6*DOWN)
        module_equations = VGroup(module_equation_1, module_equation_2, module_equation_3, module_equation_4, module_equation_5)
        text_2 = Text("，其中", font = 'simsun')
        tex_1 = Tex("m_1,\ m_2,\ \cdots,\ m_n", color = YELLOW)
        text_3 = Text("两两互质，", font = 'simsun')

        text_1.shift(1.5*UP+6.5*LEFT)
        module_equations.shift(1.45*UP+2.45*LEFT)
        text_2.shift(1.5*UP+1*RIGHT)
        tex_1.shift(1.45*UP+4*RIGHT)
        text_3.shift(1.5*UP+7.5*RIGHT)

        text_4 = Text("其解为", font = 'simsun')
        module_solution = Module(r"x", r"\sum_{i=1}^na_i\vec{e}_i", r"M")
        text_5 = Text("，", font = 'simsun')
        tex_2 = Tex("M=\prod_{i=1}^nm_i", color = YELLOW)
        text_6 = Text("，", font = 'simsun')

        text_4.shift(1.5*DOWN + 6.5 * LEFT)
        module_solution.next_to(text_4, RIGHT)
        text_5.next_to(module_solution, RIGHT)
        tex_2.next_to(text_5, RIGHT)
        text_6.next_to(tex_2, RIGHT)
        text_5.shift(0.15*DOWN)
        tex_2.shift(0.05*DOWN)
        text_6.shift(0.15*DOWN)

        text_7 = Text("其中", font = 'simsun')
        tex_3 = Tex(r"\vec{e}_i = M_i[M_i]^{-1}_{\bmod m_i}", color = ORANGE)
        text_8 = Tex(",", color = ORANGE)
        tex_4 = Tex(r"M_i = \frac{M}{m_i},\ i=1,2,\cdots, n",color = GOLD)
        text_9 = Text("。", font = 'simsun')

        text_7.shift(3*DOWN + 6.8 * LEFT)
        tex_3.next_to(text_7, RIGHT)
        text_8.next_to(tex_3, RIGHT)
        tex_4.next_to(text_8, RIGHT)
        text_9.next_to(tex_4, RIGHT)
        text_8.shift(0.15*DOWN)
        text_9.shift(0.15*DOWN)

        group_text = VGroup(text_1, module_equations, text_2, tex_1, text_3, text_4, module_solution, text_5, tex_2, text_6, text_7, tex_3, text_8, tex_4, text_9)
        group_text.scale(0.7)

        anim1 = ReplacementTransform(notice9, notice10)
        anim1.update_config(run_time = 1)
        anim2 = Write(title2)
        anim2.update_config(run_time = 2)
        anim3 = ApplyMethod(title2_line.put_start_and_end_on, np.array([-6,3,0]), np.array([6,3,0]) )
        anim3.update_config(run_time = 1)
        self.play(anim1, anim2, anim3)
        self.wait(1)
        self.play(Write(group_text), run_time = 5)
        self.wait(5)
        self.play(FadeOut(group_text))
        self.wait(1)
        """


        # 第一节-6
        #"""
        title2 = Text("中国剩余定理", font = 'simsun', color = YELLOW)
        title2.shift(3.5*UP)
        title2_line = Line(np.array([-6,3,0]), np.array([6,3,0]))

        self.add(notice10, title2, title2_line)
        self.play(ReplacementTransform(notice10, notice11))
        self.wait(1.12) #可能有喜欢探索的观众
        self.wait(1.92) #对中国剩余定理有些不满
        self.wait(0.50) #（空闲）

        quote_5 = Text("今有物，不知其数。\n三三数之剩二，五五数之剩三，七七数之剩二。\n问：物几何？", font = 'simsun')
        author_2 = Text("——《孙子算经》", color = YELLOW, font = 'simsun')
        quote_5.shift(1.5*UP)
        author_2.next_to(quote_5.get_corner(DOWN + RIGHT), 1.1*DOWN+0.3*LEFT)
        quote_and_author = VGroup(quote_5, author_2)
        quote_and_author.scale(0.8)

        self.play(Write(quote_and_author))
        self.wait(0.90) #比如 这道《孙子算经》上的题目

        module_sunzi_1 = Module(r"23", r"2", r"3")
        module_sunzi_2 = Module(r"23", r"3", r"5")
        module_sunzi_3 = Module(r"23", r"2", r"7")

        module_sunzi_1.shift(0.8*UP)
        module_sunzi_3.shift(0.8*DOWN)
        module_sunzi = VGroup(module_sunzi_1, module_sunzi_2, module_sunzi_3)
        module_sunzi.shift(1.5*DOWN+4*LEFT)

        self.play(FadeIn(module_sunzi, LEFT))
        self.wait(1.01) #最小的解是23

        module_solution = Tex(r"2\times 70+3\times 21+2\times 15 = 233", color = ORANGE)
        module_solution.shift(1.5*DOWN+2.5*RIGHT)

        self.play(FadeIn(module_solution, RIGHT))
        self.wait(1.29) #但是用中国剩余定理算出来

        self.wait(1.56)
        self.play(Indicate(module_sunzi_1.dividend), Indicate(module_sunzi_2.dividend), Indicate(module_sunzi_3.dividend))
        self.wait(0.10) #却是233 大了10倍
        self.wait(0.80) #（空闲）

        self.play(FadeOut(quote_and_author), FadeOut(module_sunzi), FadeOut(module_solution), FadeOut(title2), FadeOut(title2_line))
        self.wait(1.95) #很可惜 这是不可避免的

        grid4 = FiniteNumberPlane(3,5)
        grid4.shift(UP)
        self.play(Write(grid4.remainder_type))
        self.wait(0.63) #让我们回到3乘5的表格上来

        vector_arrow_1 = Arrow(np.array([-1, -1, 0]), np.array([0, -1, 0]), buff = 0, stroke_color = GREEN)
        vector_arrow_2 = Arrow(np.array([-1, -1, 0]), np.array([-1, 0, 0]), buff = 0, stroke_color = YELLOW)
        grid_line1 = Line(np.array([0,-1.5,0]), np.array([0,3.5,0]), color = BLUE)
        grid_line1.set_opacity(0)
        target1 = grid_line1.copy()
        target1.scale(1.2)
        target1.set_color(YELLOW)
        target1.set_opacity(1)
        grid_line2 = Line(np.array([-1.5,0,0]), np.array([1.5,0,0]), color = BLUE)
        grid_line2.set_opacity(0)
        target2 = grid_line2.copy()
        target2.scale(1.2)
        target2.set_color(YELLOW)
        target2.set_opacity(1)

        self.wait(1.45) #如果用中国剩余定理算...
        self.add(grid_line1)
        anim1 = Transform(grid_line1, target1)
        anim1.update_config(rate_func = there_and_back)
        anim2 = FadeIn(vector_arrow_1)
        anim2.update_config(rate_func = smooth)
        self.play(anim1, anim2)
        self.wait(0.28) #...除以3余1...
        self.remove(grid_line1)
        self.add(grid_line2)
        anim1 = Transform(grid_line2, target2)
        anim1.update_config(rate_func = there_and_back)
        anim2 = FadeIn(vector_arrow_2)
        anim2.update_config(rate_func = smooth)
        self.play(anim1, anim2)
        self.remove(grid_line2)
        self.wait(0.74) #除以5余1的数

        self.wait(0.78) #会得到一个...
        self.play(Flash(grid4.remainders[1][1], flash_radius=0.5))
        self.wait(1.41) #...除以15余1的数

        self.play(WiggleOutThenIn(vector_arrow_1, rotation_angle=0.02*TAU), WiggleOutThenIn(vector_arrow_2, rotation_angle=0.02*TAU), run_time = 1)
        self.wait(0.56) #但这两个基向量

        self.play(Flash(grid4.remainders[1][0], flash_radius=0.5))
        self.wait(0.68) #一个是5的倍数
        self.play(Flash(grid4.remainders[0][1], flash_radius=0.5))
        self.wait(0.76) #一个是3的倍数

        self.wait(1.98) #加起来不可能是1
        self.wait(1.68+0.79-1)
        self.play(FadeOut(grid4.remainder_type), FadeOut(vector_arrow_1), FadeOut(vector_arrow_2)) #那就只能大于15了

        self.wait(1.00) #一般地
        tex_5 = Module(r"\vec{e}_1+\vec{e}_2+\cdots+\vec{e}_n", r"1", r"M")
        tex_6 = Tex(r"\vec{e}_1+\vec{e}_2+\cdots+\vec{e}_n>1", color = ORANGE)
        tex_7 = Tex(r"\vec{e}_1+\vec{e}_2+\cdots+\vec{e}_n\ge M+1", color = GOLD)
        tex_8 = Tex(r"\Rightarrow")
        tex_5.shift(1.5*UP+1*RIGHT)
        tex_6.shift(0.5*UP)
        tex_7.shift(0.5*DOWN)
        tex_8.next_to(tex_7,LEFT)
        texes = VGroup(tex_5, tex_6, tex_7, tex_8)

        self.play(Write(texes))
        self.wait(1.59+2.25-2) #这些基向量的和 一定会大于所有数的乘积
        self.wait(1.40) #（空闲）

        self.remove(texes)
        grid5 = FiniteNumberPlane(3,5)
        grid5.shift(UP)
        self.play(Write(grid5.sumofbasis_type), run_time = 1.8)
        self.play(ApplyMethod(grid5.sumofbasis_type.shift, 3.5*LEFT))
        grid5.sumofbasis_others.shift(3.5*LEFT)
        self.wait(0.00) #如果用中国剩余定理打一个表格

        grid4.shift(2.5*RIGHT)
        self.play(Write(grid4.remainder_type))
        self.wait(0.80) #再把它和正常的表格放在一起

        frame_gird_1 = SurroundingRectangle(grid4, stroke_color = WHITE)
        frame_gird_2 = SurroundingRectangle(grid5, stroke_color = WHITE)
        tex9 = Tex(r"\equiv")
        tex10 = Tex(r"(\bmod\ 15)")
        tex9.shift(1.5*LEFT+UP)
        tex10.shift(5.5*RIGHT+UP)
        frame_grid = VGroup(frame_gird_1,frame_gird_2,tex9,tex10)
        self.play(FadeIn(frame_grid))
        self.wait(0.77) #看起来会是这个样子
        self.wait(0.97) #（空闲）

        self.bring_to_back(grid5.group_pixels)
        animations = []
        for i in range (3):
            for j in range (5):
                anim_i = ApplyMethod(grid5.sumofbasis[i][j].move_to, np.array([-4.5,-1,0]) + i*RIGHT + j*UP)
                animations.append(anim_i)
        self.play(FadeOut(grid5.coordinate), FadeIn(grid5.group_pixels), FadeOut(grid5.group_dots), *animations, run_time = 2)
        self.wait(1.08) #我用色块标出来了两边的值差几个15
        self.wait(0.54) #（空闲）

        self.wait(2.13) #在整数的中国剩余定理中
        self.wait(2.21) #这可能就是最大的遗憾吧
        self.wait(0.74) #（空闲）
        self.wait(2.95) #就让我用这幅图作为第一节的结束
        self.wait(2.65-0.77) #接下来 整式要出场了
        print(self.get_time())


        self.play(FadeOut(frame_grid), FadeOut(grid4.remainder_type), FadeOut(grid5.sumofbasis_changed), FadeOut(notice11), run_time = 2)
        self.wait(2)
        #"""

        print(self.get_time())




        # print(self.get_time())
        """
        grid1 = FiniteNumberPlane(3,5)
        grid2 = FiniteNumberPlane(3,5)

        text1 = Tex(r"\equiv")
        text2 = Tex(r"(\bmod\ 15)")
        
        ##  Position
        grid1.shift(3.5*LEFT)
        grid2.shift(2.5*RIGHT)
        text1.shift(1.5*LEFT)
        text2.shift(5.5*RIGHT)

        ##  Showing object
        self.play(Write(grid1.sumofbasi_type))
        self.play(Write(grid2.remainder_type))
        self.wait(1)
        self.play(Write(text1), Write(text2))
        # self.bring_to_back(grid1.group_pixels)
        # self.play(FadeIn(grid1.group_pixels), FadeOut(grid1.coordinate))
        self.bring_to_back(grid1.group_pixels)
        self.play(FadeOut(grid1.coordinate), FadeIn(grid1.group_pixels), FadeOut(grid2.coordinate))
        self.wait(1)
        """