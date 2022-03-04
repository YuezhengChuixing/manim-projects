from decimal import DivisionUndefined
from manimlib import *
import numpy as np
import math

SCALER_OF_LADDER = math.pow(0.5,1/24)

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):

        super().__init__()
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

class Division(VGroup):
    def __init__(self, m_text1, m_text2, m_text3, m_text4, m_type):

        super().__init__()
        self.dividend = Tex(m_text1, color = GREEN)
        self.divisionsymbol = Tex(r"\divisionsymbol")
        self.divisor = Tex(m_text2, color = YELLOW)
        self.equationsymbol = Tex(r"=")
        self.quotient = Tex(m_text3)
        self.add(self.dividend, self.divisionsymbol, self.divisor, self.equationsymbol)
        
        distance = np.array([0.5,0,0])
        self.dividend.shift(-3*distance)
        self.divisionsymbol.shift(-2*distance)
        self.divisor.shift(-1*distance)
        self.quotient.next_to(self.equationsymbol.get_corner(RIGHT), RIGHT)

        if (m_type):
            self.remindline = Tex(r"\cdots\cdots")
            self.remainder = Tex(m_text4, color = BLUE)
            self.quot_and_rem = VGroup(self.quotient, self.remindline, self.remainder)

            self.remindline.shift(3*distance)
            self.remainder.shift(4.5*distance)
        else:
            self.quotient.set_color(BLUE_B)
            self.quot_and_rem = VGroup(self.quotient)

        self.add(self.quot_and_rem)

class Noted_Division(VGroup):
    def __init__(self, m_text1, m_text2, m_text3, m_text4, m_type):

        super().__init__()
        self.equation = Division(m_text1, m_text2, m_text3, m_text4, m_type)

        distance = np.array([0.5,0,0])
        self.dividend_line = Tex(r"\cdots")
        self.dividend_text = Text(r"被除数", font = 'simsun', color = GREEN)
        self.dividend = VGroup(self.dividend_line, self.dividend_text)

        self.divisor_line = Tex(r"\cdots")
        self.divisor_text = Text(r"除数", font = 'simsun', color = YELLOW)
        self.divisor = VGroup(self.divisor_line, self.divisor_text)
        

        if (m_type):
            self.quotient_line = Tex(r"\cdots")
            self.quotient_text = Text(r"商", font = 'simsun')
            self.quotient = VGroup(self.quotient_line, self.quotient_text)

            self.remainder_line = Tex(r"\cdots")
            self.remainder_text = Text(r"余数", font = 'simsun', color = BLUE)
            self.remainder = VGroup(self.remainder_line, self.remainder_text)
            self.quot_and_rem = VGroup(self.quotient, self.remainder)

            self.remainder_line.rotate(PI/2)
            self.remainder_text.shift(0.75*DOWN)
            self.remainder_text.scale(0.5)
            self.remainder.shift(4.5*distance + DOWN)
        else:
            self.quotient_line = Tex(r"\cdots")
            self.quotient_text = Text(r"商数", font = 'simsun', color = BLUE_B)
            self.quotient = VGroup(self.quotient_line, self.quotient_text)
            self.quot_and_rem = VGroup(self.quotient)
        
        self.add(self.dividend, self.divisor, self.quot_and_rem, self.equation)
        self.note = VGroup(self.dividend, self.divisor, self.quot_and_rem)
        
        self.dividend_line.rotate(PI/2)
        self.dividend_text.shift(0.75*DOWN)
        self.dividend_text.scale(0.5)
        self.divisor_line.rotate(PI/2)
        self.divisor_text.shift(0.75*DOWN)
        self.divisor_text.scale(0.5)
        self.quotient_line.rotate(PI/2)
        self.quotient_text.shift(0.75*DOWN)
        self.quotient_text.scale(0.5)

        self.dividend.shift(-3*distance + DOWN)
        self.divisor.shift(-1*distance + DOWN)
        self.quotient.shift(1*distance + DOWN)

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
        
        distance = np.array([0.5,0,0])
        self.dividend.shift(-3*distance)
        self.modulesymbol.shift(-2*distance)
        self.remainder.shift(-1*distance)
        self.moduletext.shift(1.3*distance)
        self.divisor.shift(3*distance)
        self.ket.shift(3.5*distance)

        self.text = VGroup(self.modulesymbol, self.bra, self.moduletext, self.ket)

class Step(VGroup):
    def __init__(self, m_peak, m_height, m_width, m_ratio):

        super().__init__()
        ratio = m_ratio * 0.5
        self.line1 = Line(m_peak+np.array([-ratio*m_width, -m_ratio*m_height, 0]), m_peak+np.array([-ratio*m_width, -m_height, 0]))
        self.line2 = Line(m_peak+np.array([ratio*m_width, -m_ratio*m_height, 0]), m_peak+np.array([ratio*m_width, -m_height, 0]))
        self.line3 = Line(m_peak+np.array([-ratio*m_width, -m_ratio*m_height, 0]), m_peak+np.array([ratio*m_width, -m_ratio*m_height, 0]))
        self.add(self.line1, self.line2, self.line3)

class Ladder(VGroup):
    def __init__(self, m_peak, m_height, m_width, m_ratio, m_number):
        super().__init__()
        height = m_height
        width = m_width
        ratio = math.pow(m_ratio, 1/m_number)
        for i in range (m_number):
            self.stepi = Step(m_peak, height, width, ratio)
            self.add(self.stepi)
            height = height * ratio
            width = width * ratio

class Template(Scene):
    def construct(self):

        ##  Making object
        text1 = Text("第一节　整数的中国剩余定理", font = 'simsun', t2c={"第一节": YELLOW, "　整": GREEN, "的中国剩余定": BLUE})

        notice1 = Notice("小学数学", "请　复习")
        notice2 = Notice("小学奥数", "非常简单")
        notice3 = Notice("除法特性", "请勿模仿")
        notice4 = Notice("良心视频", "请　三连")
        ##  Position

        ##  Showing object
        """
        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))
        """

        ##  Making object
        division0 = Noted_Division(r"13", r"3", r"4", r"1", 1)
        division1 = Noted_Division(r"13", r"3", r"4", r"1", 1)
        division2 = Noted_Division(r"13", r"3", r"4.333\dots", r"1", 0)

        division3 = Division(r"13", r"3", r"4", r"1", 1)
        division3.set_color(WHITE)
        module1 = Module(r"13", r"1", r"3")

        division4 = Division(r"17", r"5", r"3", r"2", 1)
        module2 = Module(r"17", r"2", r"5")

        division5 = Division(r"21", r"7", r"3", r"0", 0)
        module3 = Module(r"21", r"0", r"7")

        division6 = Division(r"65", r"4", r"16", r"1", 1)
        module4 = Module(r"65", r"1", r"4")

        division7_1 = Division(r"65", r"4", r"16", r"1", 1)
        division7_2 = Division(r"1", r"4", r"0", r"1", 1)
        division7 = VGroup(division7_1, division7_2)

        division8_1 = Division(r"25", r"4", r"6", r"1", 1)
        module5 = Module(r"25", r"1", r"4")

        division9_2 = Division(r"9", r"4", r"2", r"1", 1)
        module6 = Module(r"25", r"9", r"4")

        division10_1 = Division(r"-3", r"4", r"-1", r"1", 1)
        module7 = Module(r"-3", r"9", r"4")
        
        title = Text("同余理论", font = 'simsun', color = YELLOW)

        title_line = Line(np.array([0,3,0]), np.array([0,3,0]))

        arrow = Arrow(LEFT, RIGHT)

        name_module = Text("同余式", font = 'simsun')
        name_module.scale(0.8)
        name_division = Text("带余除法", font = 'simsun')
        name_division.scale(0.8)
        
        ##  Position
        division0.shift(UP)
        division1.shift(UP)
        division2.shift(UP)
        division3.shift(UP)
        division4.shift(UP)
        division5.shift(UP)
        division6.shift(UP)
        division7_1.shift(3*LEFT)
        division7_2.shift(3*RIGHT)
        division7.shift(UP)
        division8_1.shift(3*LEFT+UP)
        division9_2.shift(3*RIGHT+UP)
        division10_1.shift(3*LEFT+UP)

        title.shift(UP)
        name_division.shift(2*UP)
        module1.shift(DOWN)
        module2.shift(DOWN)
        module3.shift(DOWN)
        module4.shift(DOWN)
        module5.shift(DOWN)
        module6.shift(DOWN)
        module7.shift(DOWN)


        ##  Showing object
        self.add(notice1)
        self.wait(2.08) #我们在上小学二年级的时候
        self.play(Write(division0.equation))
        self.wait(0.79) #就学过带余除法
        self.wait(0.47) #认识了...
        self.play(Write(division0.dividend), run_time = 0.5)
        self.wait(0.50) #...被除数...
        self.play(Write(division0.divisor), run_time = 0.5)
        self.wait(0.45) #...除数...
        self.play(Write(division0.quotient), run_time = 0.5)
        self.wait(0.17) #...商...
        self.play(Write(division0.remainder), run_time = 0.5)
        self.wait(1.05) #...和余数
        self.wait(2.32) #但当我们上了小学五年级
        self.play(ReplacementTransform(division0, division2))
        self.wait(1.00) #学会了小数除法以后
        self.play(ApplyWave(division2.equation.quotient))
        self.wait(1.00) #商可以不是整数
        division1.equation.remainder.shift(1.5*RIGHT)
        division1.equation.remindline.shift(1.5*RIGHT)
        self.wait(0.8)
        self.add(division1.equation.remainder, division1.equation.remindline)
        self.wait(0.2)
        self.remove(division1.equation.remainder, division1.equation.remindline)
        self.wait(0.2)
        self.add(division1.equation.remainder, division1.equation.remindline)
        self.wait(0.2)
        self.remove(division1.equation.remainder, division1.equation.remindline)
        self.wait(0.2)
        self.add(division1.equation.remainder, division1.equation.remindline)
        self.wait(0.2)
        self.remove(division1.equation.remainder, division1.equation.remindline)
        self.wait(1.30) #余数就从除法的世界中消失了
        self.wait(0.00) #（空闲）
        division1.equation.remainder.shift(1.5*LEFT)
        division1.equation.remindline.shift(1.5*LEFT)
        self.play(ApplyMethod(division2.equation.shift, 3*RIGHT + DOWN), FadeOut(division2.note, 3*RIGHT + DOWN))
        division1.equation.shift(3.5*LEFT + DOWN)
        self.wait(0.53) #很多人就认为
        self.play(FadeIn(division1.equation))
        self.wait(0.87) #带余除法没什么用
        self.play(FadeIn(arrow, 0.5*RIGHT))
        self.wait(0.50) #只是学习真正的除法之前...
        self.play(FadeOut(arrow, 0.5*RIGHT), ApplyMethod(division1.equation.set_color, WHITE))
        self.wait(0.58) #的一个过渡而已
        self.wait(0.83) #（空闲）
        self.wait(1.80) #但数学家们却发现
        self.play(ApplyMethod(division1.equation.shift, 3.5*RIGHT + UP), FadeOut(division2.equation))
        self.wait(0.47) #在带余除法中
        self.play(ApplyMethod(division1.equation.quotient.set_color, GREY))
        self.wait(1.13) #虽然商确实没什么用
        self.play(ApplyMethod(division1.equation.remainder.set_color, BLUE))
        self.wait(0.87) #但是余数的水...
        self.play(Indicate(division1.equation.remainder)) #...比想象中的要深很多
        self.wait(0.62) #（空闲）
        self.wait(3.63) #为此 数学家们专门搭建了一个领域
        self.play(ReplacementTransform(division1.equation, title))
        self.wait(0.56) #同余理论
        self.add(title_line)
        self.play(ApplyMethod(title_line.put_start_and_end_on, np.array([-6,3,0]), np.array([6,3,0]) ), ApplyMethod(title.next_to, title_line.get_corner(UP), UP), ReplacementTransform(notice1, notice2))
        self.wait(1.16) #来研究关于余数的问题
        self.wait(1.20) #（空闲）
        
        self.play(Write(division3))
        self.wait(2.01) #我们回到最开始展示的这个除法式
        self.play(Indicate(division3.dividend), run_time = 0.5)
        self.wait(0.14) #13...
        self.play(Indicate(division3.divisor), run_time = 0.5)
        self.wait(0.71) #...除以3...
        self.play(Indicate(division3.quotient), run_time = 0.5)
        self.wait(0.52) #...商4...
        self.play(Indicate(division3.remainder), run_time = 0.5)
        self.wait(0.97) #...余1
        self.wait(0.59) #我们可以把...
        self.play(FadeIn(module1.text), ApplyMethod(division3.dividend.set_color, GREEN))
        self.wait(0.18) #...被除数13...
        self.play(ApplyMethod(division3.remainder.set_color, BLUE))
        self.wait(0.30) #...和余数1
        self.play(TransformFromCopy(division3.dividend, module1.dividend), TransformFromCopy(division3.remainder, module1.remainder), run_time = 1.5)
        self.wait(1.48) #分别放在这个三条线的等号的两边
        self.wait(0.82) #之后...
        self.play(ApplyMethod(division3.divisor.set_color, YELLOW), run_time = 0.5)
        self.wait(0.28) #...再把除数3...
        self.play(TransformFromCopy(division3.divisor, module1.divisor), run_time = 1.5)
        self.wait(0.17) #标在最后面
        self.play(ShowCreationThenDestructionAround(module1), run_time = 2)
        self.wait(1.10) #现在 这个式子已经完整了
        self.play(FadeIn(name_module))
        self.wait(1.18) #它的名字叫做“同余式”
        self.wait(0.78) #读作...
        self.play(Indicate(module1.dividend), run_time = 0.5)
        self.wait(0.33) #...13...
        self.play(Indicate(module1.remainder), run_time = 0.5)
        self.wait(0.70) #...同余于1...
        self.play(Indicate(module1.divisor), run_time = 0.5)
        self.wait(0.41) #...模3
        self.wait(0.82)
        self.play(FadeIn(name_division))
        self.wait(1) #每一个除法式 都有它对应的同余式
        self.play(Transform(module1, module2), Transform(division3, division4))
        self.wait(2)
        self.play(Transform(module1, module3), Transform(division3, division5))
        self.wait(2)
        self.play(Transform(module1, module4), Transform(division3, division6))
        self.wait(1.83)
        # 到此为止共80秒
        
        self.wait(1.64) #在实际应用中
        self.play(ReplacementTransform(division3, division7))
        self.wait(1.92) #同余式的形式会更自由一点
        self.play(ShowCreationThenDestructionAround(division7_2), ShowCreationThenDestructionAround(module1.remainder), run_time = 2)
        self.wait(0.36) #右边不一定要放余数
        self.play(Transform(division7_1, division8_1), Transform(module1, module5))
        self.wait(3) # 只要同余号两边的余数相同 这个式子就是正确的
        self.play(Transform(division7_2, division9_2), Transform(module1, module6))
        self.wait(3)
        self.play(Transform(division7_1, division10_1), Transform(module1, module7))
        self.wait(3)
        self.wait(1.08)
        #到此为止共100秒
        

        ################################################
        module_plus_text_1 = Text("如果", font = "simsun")
        module_plus_1 = Tex(r"a\equiv b\ (\bmod\ m)", color = GREEN)
        module_plus_text_2 = Text("，且", font = "simsun")
        module_plus_2 = Tex(r"c\equiv d\ (\bmod\ m)", color = BLUE)
        module_plus_text_3 = Text("，那么", font = "simsun")
        module_plus_3 = Tex(r"a+c\equiv b+d\ (\bmod\ m)", color = YELLOW)
        module_plus_text_4 = Text("。", font = "simsun")

        module_plus_text_1.shift(4.8*LEFT)
        module_plus_text_1.scale(0.6)
        module_plus_1.shift(3.3*LEFT)
        module_plus_1.scale(0.6)
        module_plus_text_2.shift(2*LEFT)
        module_plus_text_2.scale(0.6)
        module_plus_2.shift(0.5*LEFT)
        module_plus_2.scale(0.6)
        module_plus_text_3.shift(1*RIGHT)
        module_plus_text_3.scale(0.6)
        module_plus_3.shift(3.2*RIGHT)
        module_plus_3.scale(0.6)
        module_plus_text_4.shift(4.7*RIGHT+0.1*DOWN)
        module_plus_text_4.scale(0.6)

        module_plus = VGroup(module_plus_text_1, module_plus_1, module_plus_text_2, module_plus_2, module_plus_text_3, module_plus_3, module_plus_text_4)
        module_plus.shift(2*UP)

        module_minus_text_1 = Text("如果", font = "simsun")
        module_minus_1 = Tex(r"a\equiv b\ (\bmod\ m)", color = GREEN)
        module_minus_text_2 = Text("，且", font = "simsun")
        module_minus_2 = Tex(r"c\equiv d\ (\bmod\ m)", color = BLUE)
        module_minus_text_3 = Text("，那么", font = "simsun")
        module_minus_3 = Tex(r"a-c\equiv b-d\ (\bmod\ m)", color = YELLOW)
        module_minus_text_4 = Text("。", font = "simsun")

        module_minus_text_1.shift(4.8*LEFT)
        module_minus_text_1.scale(0.6)
        module_minus_1.shift(3.3*LEFT)
        module_minus_1.scale(0.6)
        module_minus_text_2.shift(2*LEFT)
        module_minus_text_2.scale(0.6)
        module_minus_2.shift(0.5*LEFT)
        module_minus_2.scale(0.6)
        module_minus_text_3.shift(1*RIGHT)
        module_minus_text_3.scale(0.6)
        module_minus_3.shift(3.2*RIGHT)
        module_minus_3.scale(0.6)
        module_minus_text_4.shift(4.7*RIGHT+0.1*DOWN)
        module_minus_text_4.scale(0.6)

        module_minus = VGroup(module_minus_text_1, module_minus_1, module_minus_text_2, module_minus_2, module_minus_text_3, module_minus_3, module_minus_text_4)
        module_minus.shift(0.5*UP)

        module_multiply_text_1 = Text("如果", font = "simsun")
        module_multiply_1 = Tex(r"a\equiv b\ (\bmod\ m)", color = GREEN)
        module_multiply_text_2 = Text("，且", font = "simsun")
        module_multiply_2 = Tex(r"c\equiv d\ (\bmod\ m)", color = BLUE)
        module_multiply_text_3 = Text("，那么", font = "simsun")
        module_multiply_3 = Tex(r"ac\equiv bd\ (\bmod\ m)", color = YELLOW)
        module_multiply_text_4 = Text("。", font = "simsun")

        module_multiply_text_1.shift(4.8*LEFT)
        module_multiply_text_1.scale(0.6)
        module_multiply_1.shift(3.3*LEFT)
        module_multiply_1.scale(0.6)
        module_multiply_text_2.shift(2*LEFT)
        module_multiply_text_2.scale(0.6)
        module_multiply_2.shift(0.5*LEFT)
        module_multiply_2.scale(0.6)
        module_multiply_text_3.shift(1*RIGHT)
        module_multiply_text_3.scale(0.6)
        module_multiply_3.shift(3.2*RIGHT)
        module_multiply_3.scale(0.6)
        module_multiply_text_4.shift(4.7*RIGHT+0.1*DOWN)
        module_multiply_text_4.scale(0.6)

        module_multiply = VGroup(module_multiply_text_1, module_multiply_1, module_multiply_text_2, module_multiply_2, module_multiply_text_3, module_multiply_3, module_multiply_text_4)
        module_multiply.shift(1*DOWN)

        self.wait(3.31) #同余式有着和等式几乎一样的性质
        self.play(FadeOut(module1), FadeOut(division7), FadeOut(name_division), FadeOut(name_module))
        self.wait(0.85) #可以同时在式子两边做...
        self.play(FadeIn(module_plus, UP))
        self.wait(0.12) #...加法...
        self.play(FadeIn(module_minus, UP))
        self.wait(0.30) #...减法...
        self.play(FadeIn(module_multiply, UP))
        self.wait(1.06) #...或者乘法
        self.wait(1.96) #证明都十分简单
        self.wait(1.54) #留给大家作为习题...
        self.play(FadeOut(module_plus, DOWN), FadeOut(module_minus, DOWN), FadeOut(module_multiply, DOWN)) #...
        

        #################################
        module_division_1 = Tex(r"14\divisionsymbol 3\equiv")
        module_division_2 = Tex(r"(\bmod\ 5)")
        module_division_attempt1 = Tex(r"4\cdots\cdots 2")
        module_division_attempt2 = Tex(r"\frac{14}{3}")
        cross_line_1 = Line(np.array([-1,1,0]), np.array([-1,1,0]), color = RED)
        cross_line_2 = Line(np.array([1,1,0]), np.array([1,1,0]), color = RED)

        module_division_1.shift(2*LEFT)
        module_division_2.shift(2*RIGHT)

        self.play(FadeIn(module_division_1), FadeIn(module_division_2), ReplacementTransform(notice2, notice3))
        self.wait(1.89) #至于除法 嗯
        self.wait(1.64) #在同余理论里面
        self.play(FadeIn(module_division_attempt1, UP))
        self.play(ApplyMethod(cross_line_1.put_start_and_end_on, np.array([-1,1,0]), np.array([1,-1,0])) , rate_func=rush_into, run_time = 0.5)
        self.play(ApplyMethod(cross_line_2.put_start_and_end_on, np.array([1,1,0]), np.array([-1,-1,0])) , rate_func=rush_from, run_time = 0.5)
        self.wait(0.23) #我们不能再写一个余数
        self.play(FadeOut(module_division_attempt1, DOWN), FadeOut(cross_line_1, DOWN), FadeOut(cross_line_2, DOWN), FadeIn(module_division_attempt2, UP))
        cross_line_1.put_start_and_end_on(np.array([-1,1,0]), np.array([-1,1,0]))
        cross_line_2.put_start_and_end_on(np.array([1,1,0]), np.array([1,1,0]))
        self.play(ApplyMethod(cross_line_1.put_start_and_end_on, np.array([-1,1,0]), np.array([1,-1,0])) , rate_func=rush_into, run_time = 0.5)
        self.play(ApplyMethod(cross_line_2.put_start_and_end_on, np.array([1,1,0]), np.array([-1,-1,0])) , rate_func=rush_from, run_time = 0.5)
        self.wait(0.24) #也不能直接写分数
        self.play(FadeOut(module_division_attempt2, DOWN), FadeOut(cross_line_1, DOWN), FadeOut(cross_line_2, DOWN))
        self.play(FadeOut(module_division_1, DOWN), FadeOut(module_division_2, DOWN))
        self.wait(0.83) #不好直接套用原来的除法
        

        ##################################
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

        self.play(Write(module_inverse), run_time = 1.5)
        self.wait(1.60) #但是我们可以定义数论倒数
        self.play(FadeIn(module_division_with_inverse, UP))
        self.wait(1.41) #把除法转换为乘法计算
        self.wait(0.93) #（空闲）
        

        self.remove(title, title_line, module_inverse, module_division_with_inverse)

        equation_0 = Tex(r"1")
        equation_0.shift(6*LEFT+3*UP)

        equation_1_0 = Tex(r"=")
        equation_1_0.shift(5*LEFT+3*UP)
        equation_1_1 = Tex(r"+")
        equation_1_1.shift(2*LEFT+3*UP)
        equation_1_2 = Tex(r"13a", color = BLUE)
        equation_1_2.shift(3.5*LEFT+3*UP)
        equation_1_3 = Tex(r"47b", color = YELLOW)
        equation_1_3.shift(0.5*LEFT+3*UP)
        equation_1 = VGroup(equation_1_0, equation_1_1, equation_1_2, equation_1_3)

        equation_2_0 = Tex(r"=")
        equation_2_0.shift(5*LEFT+2*UP)
        equation_2_1 = Tex(r"+")
        equation_2_1.shift(2*LEFT+2*UP)
        equation_2_2 = Tex(r"13a", color = BLUE)
        equation_2_2.shift(3.5*LEFT+2*UP)
        equation_2_3 = Tex(r"(3\times13+8)b", color = YELLOW)
        equation_2_3.shift(0.5*LEFT+2*UP)
        equation_2 = VGroup(equation_2_0, equation_2_1, equation_2_2, equation_2_3)

        equation_3_0 = Tex(r"=")
        equation_3_0.shift(5*LEFT+2*UP)
        equation_3_1 = Tex(r"+")
        equation_3_1.shift(2*LEFT+2*UP)
        equation_3_2 = Tex(r"13(a+3b)", color = BLUE)
        equation_3_2.shift(3.5*LEFT+2*UP)
        equation_3_3_1 = Tex(r"13(3b)+", color = GREEN)
        equation_3_3_2 = Tex(r"8b", color = YELLOW)
        equation_3_3_1.shift(0.25*LEFT)
        equation_3_3_2.shift(1*RIGHT)
        equation_3_3 = VGroup(equation_3_3_1, equation_3_3_2)
        equation_3_3.shift(0.5*LEFT+2*UP)
        equation_3_2_0 = VGroup(equation_3_3_1, equation_2_2)
        equation_3 = VGroup(equation_2_0, equation_3_2_0, equation_2_2, equation_3_3_2)

        equation_4_0 = Tex(r"=")
        equation_4_0.shift(5*LEFT+1*UP)
        equation_4_1 = Tex(r"+")
        equation_4_1.shift(2*LEFT+1*UP)
        equation_4_2 = Tex(r"5(a+3b)", color = BLUE)
        equation_4_2.shift(3.5*LEFT+1*UP)
        equation_4_3 = Tex(r"8(a+4b)", color = YELLOW)
        equation_4_3.shift(0.5*LEFT+1*UP)
        equation_4 = VGroup(equation_4_0, equation_4_1, equation_4_2, equation_4_3)

        equation_5_0 = Tex(r"=")
        equation_5_0.shift(5*LEFT)
        equation_5_1 = Tex(r"+")
        equation_5_1.shift(2*LEFT)
        equation_5_2 = Tex(r"5(2a+7b)", color = BLUE)
        equation_5_2.shift(3.5*LEFT)
        equation_5_3 = Tex(r"3(a+4b)", color = YELLOW)
        equation_5_3.shift(0.5*LEFT)
        equation_5 = VGroup(equation_5_0, equation_5_1, equation_5_2, equation_5_3)

        equation_6_0 = Tex(r"=")
        equation_6_0.shift(5*LEFT+1*DOWN)
        equation_6_1 = Tex(r"+")
        equation_6_1.shift(2*LEFT+1*DOWN)
        equation_6_2 = Tex(r"2(2a+7b)", color = BLUE)
        equation_6_2.shift(3.5*LEFT+1*DOWN)
        equation_6_3 = Tex(r"3(3a+11b)", color = YELLOW)
        equation_6_3.shift(0.5*LEFT+1*DOWN)
        equation_6 = VGroup(equation_6_0, equation_6_1, equation_6_2, equation_6_3)

        equation_7_0 = Tex(r"=")
        equation_7_0.shift(5*LEFT+2*DOWN)
        equation_7_1 = Tex(r"+")
        equation_7_1.shift(2*LEFT+2*DOWN)
        equation_7_2 = Tex(r"2(5a+18b)", color = BLUE)
        equation_7_2.shift(3.5*LEFT+2*DOWN)
        equation_7_3 = Tex(r"1(3a+11b)", color = YELLOW)
        equation_7_3.shift(0.5*LEFT+2*DOWN)
        equation_7 = VGroup(equation_7_0, equation_7_1, equation_7_2, equation_7_3)
        equation_7_4 = VGroup(equation_7_2, equation_7_3)

        equation_of_ab = Tex(r"5a+18b&=0 \\3a+11b&=1")
        equation_of_ab.shift(np.array([3,2,0]))

        solution_of_ab = Tex(r"\Rightarrow a=-18,\ b=5")
        solution_of_ab.shift(np.array([3,0,0]))

        solution_of_inverse = Tex(r"13^{-1}\equiv -18\equiv 29\ (\bmod\ 47)", color = GREEN)
        solution_of_inverse.shift(np.array([0,-3,0]))

        equation = VGroup(equation_0, equation_1)
        self.play(Write(equation), ReplacementTransform(notice3, notice4))
        self.play(TransformFromCopy(equation_1, equation_2))
        self.play(ReplacementTransform(equation_2_3, equation_3_3))
        self.play(Transform(equation_3_2_0, equation_3_2), ApplyMethod(equation_3_3_2.shift, LEFT))
        self.play(TransformFromCopy(equation_3, equation_4))
        self.play(TransformFromCopy(equation_4, equation_5))
        self.play(TransformFromCopy(equation_5, equation_6))
        self.play(TransformFromCopy(equation_6, equation_7))
        self.play(TransformFromCopy(equation_7_4, equation_of_ab))
        self.play(FadeIn(solution_of_ab, RIGHT))
        self.play(FadeIn(solution_of_inverse, RIGHT))
        self.wait(1)
        #具体的计算过程比较繁琐 需要反复用到辗转相除法 这里就不详细展开了 大家如果感兴趣 可以验证一下方法的正确性
        self.wait(2.59)
        print(self.get_time())






        










