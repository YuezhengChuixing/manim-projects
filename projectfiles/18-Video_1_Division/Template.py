from manimlib import *
import numpy as np

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

class ModuleProperty(VGroup):
    def __init__(self, m_text, m_type):

        super().__init__()
        text_1 = Text("如果", font = "simsun")
        text_2 = Text("，那么", font = "simsun")
        text_3 = Text("。", font = "simsun")
        if m_type:
            module_1 = Tex(r"a(x)\equiv b(x)\ (\bmod\ m(x))", color = GREEN)
            module_2 = Tex(r"c(x)\equiv d(x)\ (\bmod\ m(x))", color = BLUE)
        else:
            module_1 = Tex(r"a\equiv b\ (\bmod\ m)", color = GREEN)
            module_2 = Tex(r"c\equiv d\ (\bmod\ m)", color = BLUE)
        module_3 = Tex(m_text, color = YELLOW)

        modules = VGroup(module_1, module_2)
        module_1.shift(0.4*UP)
        module_2.shift(0.4*DOWN)
        modules.scale(0.6)
        text_1.scale(0.6)
        text_2.scale(0.6)
        module_3.scale(0.6)
        text_3.scale(0.6)
        modules.next_to(text_2, LEFT)
        text_1.next_to(modules, LEFT)
        module_3.next_to(text_2, RIGHT)
        text_3.next_to(module_3, RIGHT)
        text_3.shift(0.1*DOWN)
        self.add(text_1, modules, text_2, module_3, text_3)


class Equation(VGroup):
    def __init__(self, m_text1, m_text2, m_text3, m_text4):

        super().__init__()
        self.former = Tex(m_text1, color = GREEN)
        self.symbol = Tex(m_text2)
        self.latter = Tex(m_text3, color = GREEN)
        self.equationsymbol = Tex(r"=")
        self.result = Tex(m_text4, color = YELLOW)
        self.add(self.former, self.symbol, self.latter, self.equationsymbol, self.result)
        
        distance = np.array([0.5,0,0])
        self.former.shift(-6*distance)
        self.symbol.shift(-4*distance)
        self.latter.shift(-2*distance)
        self.result.next_to(0.3*distance,RIGHT)
        self.result_others = VGroup(self.former, self.symbol, self.latter, self.equationsymbol)

class CrossMul(VGroup):
    def __init__(self, m_text1, m_text2, m_text3, m_text4, m_text5):

        super().__init__()
        self.x1 = Tex(m_text1)
        self.x2 = Tex(m_text2)
        self.c1 = Tex(m_text3)
        self.c2 = Tex(m_text4)
        self.xs = VGroup(self.x1, self.x2)
        self.cs = VGroup(self.c1, self.c2)
        self.add(self.x1, self.x2, self.c1, self.c2)
        self.x1.shift(np.array([-1.3,0.5,0]))
        self.x2.shift(np.array([-1.3,-0.5,0]))
        self.c1.shift(np.array([1,0.5,0]))
        self.c2.shift(np.array([1,-0.5,0]))
        
        self.cross1 = Line(self.x1.get_corner(RIGHT)+0.2*RIGHT, self.c2.get_corner(LEFT)+0.2*LEFT, color = GREEN)
        self.cross2 = Line(self.x2.get_corner(RIGHT)+0.2*RIGHT, self.c1.get_corner(LEFT)+0.2*LEFT, color = GREEN)
        self.cross = VGroup(self.cross1, self.cross2)
        self.result = Tex(m_text5)
        self.result.shift(np.array([-0.15,-1,0]))
        self.add(self.cross, self.result)
        self.frame = SurroundingRectangle(self, stroke_color = WHITE, buff = 0.3)
        self.add(self.frame)

class PolynomialLongDivision(VGroup):
    def __init__(self, m_dividend, m_divisor):

        super().__init__()
        length_dividend = m_dividend.shape[0]
        length_divisor = m_divisor.shape[0]
        length_remainder = length_dividend - length_divisor
        spacing = 1.2

        division_line = Line(np.array([-length_dividend * spacing, 0.5, 0]), np.array([0, 0.5, 0]))
        division_arc = Arc(radius = 2, angle = PI/6, start_angle = -PI/6, arc_center = np.array([ -length_dividend*spacing - 2, 0.5, 0]))
        self.division_symbol = VGroup(division_line, division_arc)

        self.poly_dividend = Polynomial(m_dividend, 0)
        self.poly_divisor = Polynomial(m_divisor, 0)
        self.poly_dividend.next_to(np.array([-0.3,0,0]), LEFT)
        self.poly_divisor.next_to(np.array([-length_dividend*spacing-0.3,0,0]), LEFT)
        self.step0 = VGroup(self.poly_dividend, self.poly_divisor, self.division_symbol)
        self.add(self.step0)

        minuend_i = m_dividend
        remainder_i = m_dividend[length_remainder: length_dividend]
        quotient = np.zeros(length_remainder + 1)
        self.poly_subtrahends = []
        self.poly_remainders = []
        self.equation_lines = []
        self.steps = []
        for i in range (length_remainder + 1):
            highest_term = length_dividend - i - 1
            lowest_term = highest_term - length_divisor + 1

            quotient[lowest_term] = remainder_i[length_divisor - 1] / m_divisor[length_divisor - 1]
            subtrahend_i = m_divisor * quotient[lowest_term]
            minuend_i[lowest_term : highest_term+1] = minuend_i[lowest_term : highest_term+1] - subtrahend_i
            
            poly_subtrahend_i = Polynomial(subtrahend_i, lowest_term)
            poly_subtrahend_i.next_to(np.array([-lowest_term*spacing, -2*i-1, 0]), LEFT)
            if lowest_term == 0:
                    poly_subtrahend_i.shift(0.3*LEFT)
            self.poly_subtrahends.append(poly_subtrahend_i)

            if i < length_dividend - length_divisor:
                remainder_i = minuend_i[lowest_term-1:highest_term]
                poly_remainder_i = Polynomial(remainder_i, lowest_term-1)
                poly_remainder_i.next_to(np.array([(-lowest_term+1)*spacing, -2*i-2, 0]), LEFT)
                if lowest_term == 1:
                    poly_remainder_i.shift(0.3*LEFT)
            else:
                remainder_i = minuend_i[lowest_term:highest_term]
                poly_remainder_i = Polynomial(remainder_i, lowest_term)
                poly_remainder_i.next_to(np.array([-lowest_term*spacing-0.3, -2*i-2, 0]), LEFT)
            self.poly_remainders.append(poly_remainder_i)
            
            equation_line_i = Line(np.array([(-highest_term-1)*spacing-0.3, -2*i-1.5, 0]), np.array([-lowest_term*spacing, -2*i-1.5, 0]))
            self.equation_lines.append(equation_line_i)
            step_i = VGroup(poly_subtrahend_i, poly_remainder_i, equation_line_i)
            self.steps.append(step_i)
            self.add(step_i)

        self.poly_quotient = Polynomial(quotient, 0)
        self.poly_quotient.next_to(np.array([-0.3,1,0]), LEFT)
        self.add(self.poly_quotient)
        self.shift((length_remainder+1) * UP + 0.5*spacing*(length_dividend+length_divisor)*RIGHT)


class Polynomial(VGroup):
    def __init__(self, m_coefficients, m_lowest_term):

        super().__init__()
        spacing = 1.2
        length = m_coefficients.shape[0]
        self.term = []
        for i in range (m_lowest_term, length+m_lowest_term):
            j = i - m_lowest_term

            if j == length - 1:
                if m_coefficients[j] == 1:
                    term_i_coefficient = ""
                elif m_coefficients[j] == -1:
                    term_i_coefficient = "-"
                else:
                    term_i_coefficient = "%d"%m_coefficients[j]
            elif i == 0:
                if m_coefficients[j] >= 0:
                    term_i_coefficient = "+%d"%m_coefficients[j]
                else:
                    term_i_coefficient = "%d"%m_coefficients[j]
            else:
                if m_coefficients[j] == 1:
                    term_i_coefficient = "+"
                elif m_coefficients[j] == -1:
                    term_i_coefficient = "-"
                elif m_coefficients[j] >= 0:
                    term_i_coefficient = "+%d"%m_coefficients[j]
                else:
                    term_i_coefficient = "%d"%m_coefficients[j]

            if i == 0:
                term_i = Tex(term_i_coefficient)
                term_i.next_to(np.array([-0.3,-0.4,0]), LEFT+UP)
            elif i == 1:
                term_i = Tex(term_i_coefficient+"x")
                term_i.next_to(np.array([-spacing,-0.4,0]), LEFT+UP)
            else:
                term_i = Tex(term_i_coefficient+"x^%d"%i)
                term_i.next_to(np.array([-i*spacing,-0.4,0]), LEFT+UP)
            self.add(term_i)
            self.term.append(term_i)

class IntegerLongDivision(VGroup):
    def __init__(self, m_dividend, m_divisor):

        super().__init__()
        length_dividend = m_dividend.shape[0]
        length_divisor = m_divisor.shape[0]
        length_remainder = length_dividend - length_divisor
        spacing = 0.6

        division_line = Line(np.array([-length_dividend * spacing, 0.5, 0]), np.array([0, 0.5, 0]))
        division_arc = Arc(radius = 2, angle = PI/6, start_angle = -PI/6, arc_center = np.array([-length_dividend*spacing -2, 0.5, 0]))
        self.division_symbol = VGroup(division_line, division_arc)

        self.poly_dividend = Decimal(m_dividend)
        self.poly_divisor = Decimal(m_divisor)
        self.poly_dividend.next_to(np.array([0,0,0]), LEFT)
        self.poly_divisor.next_to(np.array([-length_dividend*spacing - 0.3,0,0]), LEFT)
        self.step0 = VGroup(self.poly_dividend, self.poly_divisor, self.division_symbol)
        self.add(self.step0)

        minuend_i = m_dividend
        remainder_i = m_dividend[length_remainder: length_dividend]
        quotient = np.zeros(length_remainder + 1)
        self.poly_subtrahends = []
        self.poly_remainders = []
        self.equation_lines = []
        self.steps = []
        for i in range (length_remainder + 1):
            highest_term = length_dividend - i - 1
            lowest_term = highest_term - length_divisor + 1

            quotient[lowest_term] = remainder_i[length_divisor - 1] / m_divisor[length_divisor - 1]
            subtrahend_i = m_divisor * quotient[lowest_term]
            minuend_i[lowest_term : highest_term+1] = minuend_i[lowest_term : highest_term+1] - subtrahend_i
            
            poly_subtrahend_i = Decimal(subtrahend_i)
            poly_subtrahend_i.next_to(np.array([-lowest_term*spacing, -2*i-1, 0]), LEFT)
            self.poly_subtrahends.append(poly_subtrahend_i)

            if i < length_dividend - length_divisor:
                remainder_i = minuend_i[lowest_term-1:highest_term]
                poly_remainder_i = Decimal(remainder_i)
                poly_remainder_i.next_to(np.array([(-lowest_term+1)*spacing, -2*i-2, 0]), LEFT)
            else:
                remainder_i = minuend_i[lowest_term:highest_term]
                poly_remainder_i = Decimal(remainder_i)
                poly_remainder_i.next_to(np.array([-lowest_term*spacing, -2*i-2, 0]), LEFT)
            self.poly_remainders.append(poly_remainder_i)
            
            equation_line_i = Line(np.array([(-highest_term-1)*spacing, -2*i-1.5, 0]), np.array([-lowest_term*spacing, -2*i-1.5, 0]))
            self.equation_lines.append(equation_line_i)
            step_i = VGroup(poly_subtrahend_i, poly_remainder_i, equation_line_i)
            self.steps.append(step_i)
            self.add(step_i)

        self.poly_quotient = Decimal(quotient)
        self.poly_quotient.next_to(np.array([0,1,0]), LEFT)
        self.add(self.poly_quotient)
        self.shift((length_remainder+1) * UP + 0.5*spacing*(length_dividend+length_divisor)*RIGHT)


class Decimal(VGroup):
    def __init__(self, m_coefficients):

        super().__init__()
        spacing = 0.6
        length = m_coefficients.shape[0]
        self.term = []
        for i in range (length):
            term_i = Tex("%d"%m_coefficients[i])
            term_i.next_to(np.array([-i*spacing,-0.4,0]), LEFT+UP)
            self.add(term_i)
            self.term.append(term_i)


class Template(Scene):
    def construct(self):

        #第二节-0
        """
        text2 = Text("第二节　整式的同余", font = 'simsun', t2c={"第二节": YELLOW, "　整": GREEN, "的同": BLUE})
        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))
        """
        
        notice0 = Notice("初中数学", "请　复习")
        notice1 = Notice("初中奥数", "十分简单")
        notice2 = Notice("大胆假设", "小心求证")
        notice3 = Notice("初中奥数", "十分简单")
        notice4 = Notice("啊对对对", "直接开摆")
        notice5 = Notice("初中奥数", "十分简单")
        notice6 = Notice("留作习题", "自证不难")
        notice7 = Notice("除法特性", "请勿模仿")
        notice8 = Notice("初中奥数", "十分简单")
        notice9 = Notice("前情提要", "请　复习")
        notice10 = Notice("初中奥数", "十分简单")
        notice11 = Notice("重要结论", "请记笔记")

        #第二节-1
        """
        formula_poly1 = Tex(r"x+3")
        text_poly1 = Text("整式", font = 'simsun', color = YELLOW)
        text_poly1.shift(UP)
        poly1 = VGroup(formula_poly1, text_poly1)
        poly_addition = Equation(r"(x+3)", r"+", r"(x+2)", r"2x+5")
        poly_addition.shift(3*RIGHT+1.5*UP)
        poly_subtraction = Equation(r"(x+3)", r"-", r"(x+2)", r"1")
        poly_subtraction.shift(3*RIGHT)
        poly_multiplication = Equation(r"(x+3)", r"\times", r"(x+2)", r"x^2+5x+6")
        poly_multiplication.shift(3*RIGHT+1.5*DOWN)
        poly_division_1 = Equation(r"(x+3)", r"\divisionsymbol", r"(x+2)", r"")
        poly_division_2 = Equation(r"(x+3)", r"\divisionsymbol", r"(x+2)", r"1\cdots\cdots1")
        poly_division_3 = Equation(r"(x+3)", r"\divisionsymbol", r"(x+2)", r"\frac{x+3}{x+2}")
        poly_division = VGroup(poly_division_1, poly_division_2, poly_division_3)
        poly_division.shift(3*RIGHT)
        cross_line_1 = Line(np.array([-1,1,0])+4.25*RIGHT, np.array([-1,1,0])+4.25*RIGHT, color = RED)
        cross_line_2 = Line(np.array([1,1,0])+4.25*RIGHT, np.array([1,1,0])+4.25*RIGHT, color = RED)

        self.add(notice0)
        self.wait(2.20) #我们在初中七年级的时候
        self.play(FadeIn(poly1, UP))
        self.wait(1.43) #就学到了整式的概念
        self.play(ApplyMethod(poly1.shift, 3*LEFT))
        self.wait(0.68) #在后续的学习中

        self.wait(1.67) #我们陆续认识了整式的...
        self.play(FadeIn(poly_addition, LEFT), run_time = 0.5)
        self.wait(0.65) #...加法...
        self.play(FadeIn(poly_subtraction, LEFT), run_time = 0.5)
        self.wait(0.67) #...减法...
        self.play(FadeIn(poly_multiplication, LEFT), run_time = 0.5)
        self.wait(1.21) #...和乘法

        self.play(FadeOut(poly_addition, DOWN), FadeOut(poly_subtraction, DOWN), FadeOut(poly_multiplication, DOWN), run_time = 0.75)
        self.wait(0.02) #不过...
        self.play(FadeIn(poly_division_1, LEFT))
        self.wait(0.85) #...当讲到除法的时候

        self.play(Transform(poly_division_1, poly_division_2))
        self.wait(0.90) #课本没有像整数一样...
        self.play(ApplyMethod(cross_line_1.put_start_and_end_on, np.array([-1,1,0])+4.25*RIGHT, np.array([1,-1,0])+4.25*RIGHT) , rate_func=rush_into, run_time = 0.5)
        self.play(ApplyMethod(cross_line_2.put_start_and_end_on, np.array([1,1,0])+4.25*RIGHT, np.array([-1,-1,0])+4.25*RIGHT) , rate_func=rush_from, run_time = 0.5)
        self.wait(0.65) #...引入带余除法

        self.play(FadeOut(poly_division_1.result, UP), FadeOut(cross_line_1, UP), FadeOut(cross_line_2, UP), FadeIn(poly_division_3.result, UP))
        self.wait(0.74) #而是直接介绍了分式

        self.wait(1.03) #（空闲）

        self.remove(poly1, poly_division_1.result_others, poly_division_3)

        poly_division_example_1 = Equation(r"(x^2+5x+6)", r"\divisionsymbol", r"(x+3)", r"")
        poly_division_example_1.former.shift(0.7*LEFT)
        poly_division_example_1.shift(2*UP)
        poly_division_result = Tex(r"x+2", color = YELLOW)
        poly_division_result.next_to(poly_division_example_1, RIGHT)

        poly_cross_mul = Polynomial(np.array([6,5,1]), 0)
        poly_cross_mul.shift(UP+1.5*RIGHT)
        poly_cross_factored = Tex(r"=(x+3)(x+2)")
        poly_cross_factored.shift(0.5*LEFT)

        crossmul1 = CrossMul(r"x", r"x", r"6", r"1", r"7")
        crossmul1.next_to(0.5*DOWN+1.5*RIGHT, LEFT)
        crossmul2 = CrossMul(r"x", r"x", r"3", r"2", r"5")
        crossmul2.next_to(0.5*DOWN+1.5*RIGHT, LEFT)
        crossmul3 = crossmul2.copy()

        self.wait(1.38) #在初中阶段
        self.play(Write(poly_division_example_1))
        self.wait(1.06) #大家肯定会遇到很多这样的式子
        self.play(TransformFromCopy(poly_division_example_1.former, poly_cross_mul))
        self.wait(1.33) #绝大部分会做这一题的观众

        self.play(TransformFromCopy(poly_cross_mul.term[2], crossmul1.xs), TransformFromCopy(poly_cross_mul.term[0], crossmul1.cs), FadeIn(crossmul1.frame, DOWN), run_time = 0.5)
        self.play(FadeIn(crossmul1.cross), run_time = 0.5)
        self.play(FadeIn(crossmul1.result, DOWN), run_time = 0.5)
        self.play(ApplyMethod(crossmul1.result.fade), run_time = 0.5)
        self.play(FadeOut(crossmul1.cross, DOWN), FadeOut(crossmul1.cs, DOWN), FadeOut(crossmul1.result, DOWN), run_time = 0.5)
        self.wait(2.87-2.5) #应该会立即想到十字相乘法

        self.add(crossmul2.xs, crossmul2.frame)
        self.remove(crossmul1.xs, crossmul1.frame)
        self.play(TransformFromCopy(poly_cross_mul.term[0], crossmul2.cs), run_time = 0.5)
        self.play(FadeIn(crossmul2.cross), run_time = 0.5)
        self.play(FadeIn(crossmul2.result, DOWN), run_time = 0.5)
        self.play(Flash(crossmul2.result, flash_radius=0.5), run_time = 0.5)
        self.remove(crossmul2.cs)
        self.play(ReplacementTransform(crossmul2, poly_cross_factored), run_time = 0.5)
        self.wait(3.18-2.5) #通过把二次式分解为两个一次式的乘积

        cross_line_3 = Line(np.array([-0.6,0.6,0])+2*UP+1*LEFT, np.array([-0.6,0.6,0])+2*UP+1*LEFT, color = RED)
        cross_line_4 = Line(np.array([-0.6,0.6,0])+LEFT, np.array([-0.6,0.6,0])+LEFT, color = RED)
        cross_for_vanish = VGroup(cross_line_3, cross_line_4)

        self.play(ApplyMethod(cross_line_3.put_start_and_end_on, np.array([-0.6,0.6,0])+2*UP+1*LEFT, np.array([0.6,-0.6,0])+2*UP+1*LEFT), ApplyMethod(cross_line_4.put_start_and_end_on, np.array([-0.6,0.6,0])+LEFT, np.array([0.6,-0.6,0])+LEFT))
        self.wait(0.08) #顺利约分...
        self.play(Write(poly_division_result))
        self.wait(0.23) #...解决这道题目
        self.wait(0.57) #（空闲）
        
        self.wait(0.50) #但是...
        self.play(FadeOut(cross_for_vanish, DOWN), FadeOut(poly_cross_factored, DOWN), FadeOut(poly_cross_mul, DOWN), FadeIn(crossmul3, DOWN))
        self.wait(1.62) #...十字相乘毕竟是间接的方法
        self.wait(2.32) #我们能不能像整数除法那样
        self.wait(2.88) #直接算出这个除法的答案呢
        self.play(FadeOut(poly_division_example_1, UP), FadeOut(poly_division_result, UP), FadeOut(crossmul3, DOWN), ReplacementTransform(notice0, notice2))
        self.wait(0.27) #让我们来试试吧
        self.wait(0.92) #（空闲）

        longdivision1 = PolynomialLongDivision(np.array([6,5,1]), np.array([3,1]))
        longdivision1.shift(1.5*RIGHT)
        longdivision2 = IntegerLongDivision(np.array([6,5,1]), np.array([3,1]))
        longdivision2.shift(3.5*LEFT)

        longdivision2_copy1 = longdivision2.poly_quotient.term[1].copy()
        longdivision2_copy2 = longdivision2.poly_subtrahends[0].term[1].copy()
        longdivision2_copy3 = longdivision2.poly_subtrahends[0].term[0].copy()
        
        longdivision2_replace1 = Tex(r"2", color = RED)
        longdivision2_replace1.next_to(3*UP+(2+0.6)*LEFT, LEFT)
        longdivision2_replace2 = Tex(r"2", color = RED)
        longdivision2_replace2.next_to(1*UP+(2+1.2)*LEFT, LEFT)
        longdivision2_replace3 = Tex(r"6", color = RED)
        longdivision2_replace3.next_to(1*UP+(2+0.6)*LEFT, LEFT)

        self.wait(0.77) #我们首先把...
        self.play(Write(longdivision1.poly_dividend), run_time = 0.5)
        self.wait(0.45) #...被除式...
        self.play(Write(longdivision1.division_symbol), run_time = 0.5)
        self.wait(0.45) #...除号...
        self.play(Write(longdivision1.poly_divisor), run_time = 0.5)
        self.wait(1.37) #...和除式写好

        self.wait(1.18) #作为参照
        self.play(TransformFromCopy(longdivision1.poly_divisor, longdivision2.poly_divisor))
        self.play(TransformFromCopy(longdivision1.poly_dividend, longdivision2.poly_dividend))
        self.wait(1.15) #我把这个式子每一项的系数单独抄了下来

        self.play(FadeIn(longdivision2.division_symbol))
        self.wait(1.87+1.64-1) #当做一个整数除法 放在了左边

        self.wait(1.59) #应该有理由相信
        self.wait(1.74) #这两个竖式会比较像
        self.wait(0.86) #（空闲）

        self.play(ApplyMethod(longdivision1.step0.set_color, GREY))
        self.wait(0.73) #我们先看左边
        self.play(ShowCreationThenDestructionAround(longdivision2.poly_divisor))
        self.wait(0.79) #因为除数是两位的
        self.play(Indicate(longdivision2.poly_dividend[2]), Indicate(longdivision2.poly_dividend[1]))
        self.wait(1.57) #我们看被除数的最高两位

        self.play(FadeIn(longdivision2_copy1), FadeIn(longdivision2_copy2), FadeIn(longdivision2_copy3))
        self.wait(0.72) #13小于15
        self.play(ReplacementTransform(longdivision2_copy1,longdivision2_replace1), ReplacementTransform(longdivision2_copy2,longdivision2_replace2), ReplacementTransform(longdivision2_copy3,longdivision2_replace3))
        self.wait(0.97) #但是26大于15
        self.play(ReplacementTransform(longdivision2_replace1,longdivision2.poly_quotient.term[1]), FadeOut(longdivision2_replace2), FadeOut(longdivision2_replace3))
        self.wait(1.81) #所以商的十位应该是1

        copyfrom1 = VGroup(longdivision2.poly_quotient.term[1], longdivision2.poly_divisor)
        copy1 = copyfrom1.copy()
        self.play(ReplacementTransform(copy1, longdivision2.poly_subtrahends[0]))
        self.wait(1.00)
        self.play(FadeIn(longdivision2.poly_remainders[0]), FadeIn(longdivision2.equation_lines[0]))
        self.wait(0.21) #我们为被除数的最高两位减去13

        self.play(ApplyMethod(longdivision2.step0.set_color, GREY), ApplyMethod(longdivision2.steps[0].set_color, GREY), ApplyMethod(longdivision2.poly_quotient.term[1].set_color, GREY), ApplyMethod(longdivision1.step0.set_color, WHITE))
        self.wait(0.06) #而右边...
        self.play(ShowCreationThenDestructionAround(longdivision1.poly_divisor))
        self.wait(0.80) #...因为除式有两项
        self.play(Indicate(longdivision1.poly_dividend[2]), Indicate(longdivision1.poly_dividend[1]))
        self.wait(1.52) #我们看被除数的最高两项

        self.wait(1.19) #和左边一样
        self.play(Indicate(longdivision2.poly_quotient.term[1]))
        self.wait(1.43) #商的一次项系数应该是1
        self.play(FadeIn(longdivision1.poly_quotient.term[1], DOWN))
        self.wait(2.42) #所以我们在商的一次项位置写上一倍的x
        copyfrom1 = VGroup(longdivision1.poly_quotient.term[1], longdivision1.poly_divisor)
        copy1 = copyfrom1.copy()
        self.play(Transform(copy1, longdivision1.poly_subtrahends[0]))
        self.wait(1.00)
        self.play(FadeIn(longdivision1.poly_remainders[0]), FadeIn(longdivision1.equation_lines[0]))
        self.wait(1.44) #并且为被除式减去x^2+3x

        self.play(ApplyMethod(longdivision1.step0.set_color, GREY), ApplyMethod(longdivision1.steps[0].set_color, GREY), ApplyMethod(longdivision1.poly_quotient.term[1].set_color, GREY), ApplyMethod(longdivision2.step0.set_color, WHITE), ApplyMethod(longdivision2.steps[0].set_color, WHITE), ApplyMethod(longdivision2.poly_quotient.term[1].set_color, WHITE))
        self.wait(0.64) #我们回到左边
        self.play(ShowCreationThenDestructionAround(longdivision2.poly_remainders[0]))
        self.wait(1.13) #被除数的下两位是26
        self.play(Indicate(longdivision2.poly_divisor[1]), Indicate(longdivision2.poly_divisor[0]))
        self.wait(0.97) #正好是13的2倍

        self.wait(0.78) #所以...
        self.play(FadeIn(longdivision2.poly_quotient.term[0]))
        self.wait(1.02) #...商的个位应该是2
        self.play(FadeIn(longdivision2.steps[1]))
        self.wait(0.65) #余数是0

        self.play(ApplyMethod(longdivision1.step0.set_color, WHITE), ApplyMethod(longdivision1.steps[0].set_color, WHITE), ApplyMethod(longdivision1.poly_quotient.term[1].set_color, WHITE), ApplyMethod(longdivision2.set_color, GREY))
        self.wait(0.11) #而右边
        self.play(ShowCreationThenDestructionAround(longdivision1.poly_remainders[0]))
        self.wait(1.32) #被除式剩下2x+6
        self.play(Indicate(longdivision1.poly_divisor[1]), Indicate(longdivision1.poly_divisor[0]))
        self.wait(0.94) #正好是除式的2倍

        self.wait(0.77) #所以...
        self.play(FadeIn(longdivision1.poly_quotient.term[0], DOWN))
        self.wait(1.51) #...商的常数项系数应该是2
        self.play(FadeIn(longdivision1.steps[1]))
        self.wait(0.24) #余数是0
        self.wait(1.04) #（空闲）

        poly_division = Equation(r"(x^2+5x+6)", r"\divisionsymbol", r"(x+3)", r"x+2")
        poly_division.former.shift(0.7*LEFT)
        poly_division.shift(LEFT+0.5*DOWN)

        self.wait(1.14) #通过对照
        self.play(FadeOut(longdivision2))
        self.play(Indicate(longdivision1.poly_quotient.term[0]), Indicate(longdivision1.poly_quotient.term[1]))
        self.wait(0.36) #我们真的算出了正确答案

        self.play(TransformFromCopy(longdivision1.poly_dividend, poly_division.former))
        self.play(TransformFromCopy(longdivision1.division_symbol, poly_division.symbol))
        self.play(TransformFromCopy(longdivision1.poly_divisor, poly_division.latter))
        self.wait(0.64) #x^2+5x+6除以x+3...
        self.play(FadeIn(poly_division.equationsymbol), TransformFromCopy(longdivision1.poly_quotient, poly_division.result))
        self.wait(1.55) #...答案确实是x+2

        longdivision2.set_color(WHITE)
        self.play(FadeOut(poly_division, DOWN), FadeIn(longdivision2, DOWN))
        self.wait(0.04) #而且...
        self.play(ShowCreationThenDestructionAround(longdivision1))
        self.wait(0.66) #...整式的竖式除法
        self.wait(0.62) #似乎和...
        self.play(ShowCreationThenDestructionAround(longdivision2))
        self.wait(1.63+1.17-1) #...整数的竖式除法 没什么区别
        self.wait(1.68)

        """

        #第二节-2
        """
        self.add(notice2)
        self.play(ReplacementTransform(notice2, notice3))
        self.wait(1.26) #我们再试试其它的例子

        equation_example_2_mul = Equation(r"(x+3)", r"\times", r"(x-2)", r"x^2+x-6")
        equation_example_2_div = Equation(r"(x^2+x-6)", r"\divisionsymbol", r"(x+3)", r"x-2")
        equation_example_2_div.former.shift(0.54*LEFT)
        equation_example_2_mul.shift(1.5*UP)
        equation_example_2_div.shift(0.5*UP)

        self.play(FadeIn(equation_example_2_mul, DOWN))
        self.wait(3.32) #x+3乘以x-2的值是x^2+x-6
        self.play(FadeIn(equation_example_2_div.former, UP), FadeIn(equation_example_2_div.symbol, UP), FadeIn(equation_example_2_div.latter, UP))
        self.wait(2.26) #那么x^2+x-6除以x+3
        self.play(FadeIn(equation_example_2_div.equationsymbol, UP), FadeIn(equation_example_2_div.result, UP))
        self.wait(0.69) #应该就是x-2
        self.wait(0.58) #（空闲）

        longdivision3 = PolynomialLongDivision(np.array([-6,1,1]), np.array([3,1]))
        longdivision3.shift(1.5*RIGHT)

        self.play(FadeOut(equation_example_2_mul, UP), ApplyMethod(equation_example_2_div.shift, 1.5*LEFT+0.5*DOWN), FadeIn(longdivision3.step0))
        self.wait(0.77) #这次我们直接算

        self.play(ShowCreationThenDestructionAround(longdivision3.poly_divisor))
        self.wait(0.39) #除式有两项...
        self.play(Indicate(longdivision3.poly_dividend.term[2]), Indicate(longdivision3.poly_dividend.term[1]))
        self.wait(1.05) #...我们看被除式的最高两项
        self.wait(0.69) #（空闲）

        self.wait(2.31) #由于我们事先已经知道答案了
        self.play(FadeIn(longdivision3.poly_quotient.term[1], DOWN))
        copyfrom1 = VGroup(longdivision3.poly_quotient.term[1], longdivision3.poly_divisor)
        copy1 = copyfrom1.copy()
        self.play(ReplacementTransform(copy1, longdivision3.poly_subtrahends[0]), FadeIn(longdivision3.equation_lines[0]))
        self.wait(0.27) #一次项上应该商x......

        self.wait(0.88) #但是...
        self.play(Indicate(longdivision3.poly_dividend[2]), Indicate(longdivision3.poly_dividend[1]))
        self.wait(0.92) #...x^2+x看上去好像比...
        self.play(Indicate(longdivision3.poly_subtrahends[0][1]), Indicate(longdivision3.poly_subtrahends[0][0]))
        self.wait(1.40) #...x^2+3x小吧

        temp = VGroup(longdivision3.poly_dividend[2], longdivision3.poly_dividend[1], longdivision3.poly_subtrahends[0][1], longdivision3.poly_subtrahends[0][0])
        self.play(ShowCreationThenDestructionAround(temp), run_time = 2)
        self.wait(1.94+0.93-2) #这真的符合除法的规则吗

        inequality_1 = Tex(r"x^2+3x\ >\ x^2+x")
        cross_line_5 = Line(np.array([-0.6,0.6,0])+0.05*RIGHT, np.array([-0.6,0.6,0])+0.05*RIGHT, color = RED)

        self.remove(equation_example_2_div, longdivision3.step0, longdivision3.poly_quotient.term[1], longdivision3.poly_subtrahends[0], longdivision3.equation_lines[0])
        self.wait(4.75) #这就是整式除法和整数除法最大的不同
        self.play(FadeIn(inequality_1))
        self.wait(0.25)
        self.play(ApplyMethod(cross_line_5.put_start_and_end_on, np.array([-0.6,0.6,0])+0.05*RIGHT, np.array([0.6,-0.6,0])+0.05*RIGHT), run_time = 0.5)
        self.wait(0.25)
        self.wait(2.68-2) #整式之间其实不能比大小
        self.play(FadeOut(inequality_1, DOWN), FadeOut(cross_line_5, DOWN), FadeIn(equation_example_2_div, DOWN), FadeIn(longdivision3.step0, DOWN), FadeIn(longdivision3.poly_quotient.term[1], DOWN), FadeIn(longdivision3.poly_subtrahends[0], DOWN), FadeIn(longdivision3.equation_lines[0], DOWN))
        self.play(FadeIn(longdivision3.poly_remainders[0][1]))
        self.wait(0.31) #真正让整式除法能算下去的
        self.play(ShowCreationThenDestructionAround(longdivision3.poly_remainders[0][1]))
        self.wait(0.40) #是余式的次数小于...
        self.play(ShowCreationThenDestructionAround(longdivision3.poly_subtrahends[0]))
        self.wait(0.61) #...除式的次数
        self.play(Indicate(longdivision3.poly_quotient[1]))
        self.wait(0.57) #每次试商的时候
        temp = VGroup(longdivision3.poly_dividend[2], longdivision3.poly_subtrahends[0][1])
        self.play(ShowCreationThenDestructionAround(temp))
        self.wait(1.26) #把最高次项除尽就可以了
        self.play(FadeIn(longdivision3.poly_remainders[0][0]))
        self.wait(0.82) #别的什么也不需要管
        self.wait(1.34) #（空闲）

        self.play(ShowCreationThenDestructionAround(longdivision3.poly_remainders[0][0]), ShowCreationThenDestructionAround(longdivision3.poly_remainders[0][1]), ReplacementTransform(notice3, notice4), run_time = 1.5)
        self.wait(0.63) #出现了负数也没有关系
        self.play(FadeIn(longdivision3.poly_quotient[0], DOWN))
        self.play(Indicate(longdivision3.poly_quotient[0]))
        self.wait(0.55) #整式的系数本来就可以是负数
        self.play(Write(longdivision3.steps[1]))
        self.wait(0.09)
        self.play(FadeOut(longdivision3, DOWN), FadeOut(equation_example_2_div, DOWN), run_time = 0.5) #（空闲）

        equation_example_3 = Equation(r"(5x+5)", r"\divisionsymbol", r"(2x+2)", r"\frac{5}{2}")
        equation_example_3.shift(1.5*LEFT+0.5*DOWN)
        equation_example_3.former.shift(0.25*LEFT)
        equation_example_3.symbol.shift(0.15*LEFT)
        equation_example_3.latter.shift(0.05*LEFT)
        longdivision4 = PolynomialLongDivision(np.array([5,5]), np.array([2,2]))
        longdivision4.shift(1.5*RIGHT)
        longdivision4_replace = Tex(r"\frac{5}{2}")
        longdivision4_replace.next_to(1.5*UP+3.6*RIGHT, UP+LEFT)
        longdivision4.poly_quotient.set_opacity(0)
        longdivision4.poly_quotient = longdivision4_replace
        
        self.play(FadeIn(equation_example_3.result_others, DOWN), FadeIn(longdivision4.step0, DOWN))
        self.play(FadeIn(longdivision4.poly_quotient, DOWN))
        self.wait(0.01) #出现了分数也没有关系
        copyfrom = VGroup(longdivision4.poly_quotient, longdivision4.poly_divisor)
        copy = copyfrom.copy()
        self.play(ReplacementTransform(copy, longdivision4.poly_subtrahends[0]), FadeIn(longdivision4.equation_lines[0]))
        self.play(FadeIn(longdivision4.poly_remainders[0]), FadeIn(equation_example_3.result))
        self.wait(0.76) #整式的系数本来就可以是分数
        
        self.wait(1.56)
        self.play(FadeOut(longdivision4), FadeOut(equation_example_3), FadeOut(longdivision4.poly_quotient))
        self.wait(1)
        """

        #"""
        longdivision5 = PolynomialLongDivision(np.array([0,0,0,1]), np.array([-2,1]))
        longdivision5.shift(0.5*LEFT+0.5*DOWN)
        longdivision5.scale(0.8)
        longdivision5.shift(0.5*UP)

        self.add(notice4)
        self.play(ReplacementTransform(notice4, notice5))
        self.wait(2.34) #接下来 我们来做个小练习吧
        temp = VGroup(longdivision5.poly_divisor, longdivision5.division_symbol, longdivision5.poly_dividend[3])
        self.play(Write(temp), run_time = 2)
        self.wait(2.61) #我们来试着算一算x^3除以x-2
        temp = VGroup(longdivision5.poly_dividend[2], longdivision5.poly_dividend[1], longdivision5.poly_dividend[0])
        self.play(Write(temp), run_time = 2)
        self.wait(0.03) #记得在缺项的地方补0
        self.wait(0.02) #（到此为止共10秒）

        self.play(Indicate(longdivision5.poly_divisor[1]), Indicate(longdivision5.poly_dividend[3]), FadeIn(longdivision5.poly_quotient[2], DOWN))
        self.wait(1)
        copyfrom = VGroup(longdivision5.poly_divisor, longdivision5.poly_quotient[2])
        copy = copyfrom.copy()
        self.play(ReplacementTransform(copy, longdivision5.poly_subtrahends[0]))
        self.play(FadeIn(longdivision5.equation_lines[0]))
        self.play(FadeIn(longdivision5.poly_remainders[0][1], DOWN))
        self.play(TransformFromCopy(longdivision5.poly_dividend[1], longdivision5.poly_remainders[0][0]))
        self.wait(1)
        #（动画演示除法第一步）

        self.play(Indicate(longdivision5.poly_divisor[1]), Indicate(longdivision5.poly_remainders[0][1]), FadeIn(longdivision5.poly_quotient[1], DOWN))
        self.wait(1)
        copyfrom = VGroup(longdivision5.poly_divisor, longdivision5.poly_quotient[1])
        copy = copyfrom.copy()
        self.play(ReplacementTransform(copy, longdivision5.poly_subtrahends[1]))
        self.play(FadeIn(longdivision5.equation_lines[1]))
        self.play(FadeIn(longdivision5.poly_remainders[1][1], DOWN))
        self.play(TransformFromCopy(longdivision5.poly_dividend[0], longdivision5.poly_remainders[1][0]))
        self.wait(1)
        #（动画演示除法第二步）

        self.play(Indicate(longdivision5.poly_divisor[1]), Indicate(longdivision5.poly_remainders[1][1]), FadeIn(longdivision5.poly_quotient[0], DOWN))
        self.wait(1)
        copyfrom = VGroup(longdivision5.poly_divisor, longdivision5.poly_quotient[0])
        copy = copyfrom.copy()
        self.play(ReplacementTransform(copy, longdivision5.poly_subtrahends[2]))
        self.play(FadeIn(longdivision5.equation_lines[2]))
        self.play(FadeIn(longdivision5.poly_remainders[2][0], DOWN))
        self.wait(1)
        #（动画演示除法第三步）
        #（到此为止共30秒）

        equation_example_4_equation = Equation(r"x^3", r"\divisionsymbol", r"(x-2)", r"x^2+2x+4")
        equation_example_4_replace_1 = Tex(r"\cdots\cdots")
        equation_example_4_replace_1.next_to(equation_example_4_equation, RIGHT)
        equation_example_4_replace_2 = Tex(r"2^3", color = YELLOW)
        equation_example_4_replace_2.next_to(equation_example_4_replace_1, RIGHT)
        equation_example_4_replace_2.shift(0.05*UP)
        equation_example_4 = VGroup(equation_example_4_equation, equation_example_4_replace_1, equation_example_4_replace_2)
        equation_example_4.shift(0.5*LEFT)
        longdivision6 = PolynomialLongDivision(np.array([0,0,1]), np.array([-2,1]))
        longdivision6.shift(0.5*LEFT)

        self.play(ShowCreationThenDestructionAround(longdivision5.poly_remainders[2][0]))
        self.wait(0.28) #余数是8...
        copy = longdivision5.copy()
        self.remove(longdivision5)
        self.add(copy)
        self.play(ReplacementTransform(copy, equation_example_4))
        self.wait(1.32) #...正好是2的立方

        self.play(ShowCreationThenDestructionAround(equation_example_4_equation.former), ShowCreationThenDestructionAround(equation_example_4_replace_2))
        self.wait(0.81) #这是巧合吗
        
        self.wait(1)
        self.remove(equation_example_4)
        self.play(FadeIn(longdivision6.poly_divisor, RIGHT), FadeIn(longdivision6.division_symbol, DOWN), FadeIn(longdivision6.poly_dividend[2], UP))
        temp = VGroup(longdivision6.poly_dividend[1], longdivision6.poly_dividend[0])
        self.play(Write(temp), run_time = 1)
        self.wait(0.09) #我们再试试x^2除以x-2吧
        #（到此为止共38.5秒）

        self.play(Indicate(longdivision6.poly_divisor[1]), Indicate(longdivision6.poly_dividend[2]), FadeIn(longdivision6.poly_quotient[1], DOWN))
        self.wait(0.5)
        copyfrom = VGroup(longdivision6.poly_divisor, longdivision6.poly_quotient[1])
        copy = copyfrom.copy()
        self.play(ReplacementTransform(copy, longdivision6.poly_subtrahends[0]))
        self.play(FadeIn(longdivision6.equation_lines[0]))
        self.play(FadeIn(longdivision6.poly_remainders[0][1], DOWN))
        self.play(TransformFromCopy(longdivision6.poly_dividend[0], longdivision6.poly_remainders[0][0]))
        self.wait(0.5)
        #（动画演示除法第一步）

        self.play(Indicate(longdivision6.poly_divisor[1]), Indicate(longdivision6.poly_remainders[0][1]), FadeIn(longdivision6.poly_quotient[0], DOWN))
        self.wait(0.5)
        copyfrom = VGroup(longdivision6.poly_divisor, longdivision6.poly_quotient[0])
        copy = copyfrom.copy()
        self.play(ReplacementTransform(copy, longdivision6.poly_subtrahends[1]))
        self.play(FadeIn(longdivision6.equation_lines[1]))
        self.play(FadeIn(longdivision6.poly_remainders[1][0], DOWN))
        self.wait(1)
        #（动画演示除法第二步）
        #（到此为止共50秒）

        equation_example_5_equation = Equation(r"x^2", r"\divisionsymbol", r"(x-2)", r"x+2")
        equation_example_5_replace_1 = Tex(r"\cdots\cdots")
        equation_example_5_replace_1.next_to(equation_example_5_equation, RIGHT)
        equation_example_5_replace_2 = Tex(r"2^2", color = YELLOW)
        equation_example_5_replace_2.next_to(equation_example_5_replace_1, RIGHT)
        equation_example_5_replace_2.shift(0.05*UP)
        equation_example_5 = VGroup(equation_example_5_equation, equation_example_5_replace_1, equation_example_5_replace_2)
        equation_example_5.shift(0.5*LEFT)

        self.play(ShowCreationThenDestructionAround(longdivision6.poly_remainders[1][0]))
        self.wait(0.51) #余数是4
        copy = longdivision6.copy()
        self.remove(longdivision6)
        self.add(copy)
        self.play(ReplacementTransform(copy, equation_example_5))
        self.wait(1.09) #...正好是2的平方

        equation_example_4.shift(0.5*UP)
        self.play(FadeIn(equation_example_4, 0.5*DOWN), ApplyMethod(equation_example_5.shift, 0.5*DOWN))
        self.wait(1.20) #看起来这不太像是巧合
        
        self.wait(1.87) #是背后有什么规律吗
        self.wait(0.87) #（空闲）

        title = Text("同余理论", font = 'simsun', color = YELLOW)
        title_line = Line(np.array([0,3,0]), np.array([0,3,0]))
        title.next_to(title_line, UP)
        self.play(Write(title), ApplyMethod(title_line.put_start_and_end_on, np.array([-6,3,0]), np.array([6,3,0])), FadeOut(equation_example_4, 1.5*UP), ApplyMethod(equation_example_5.shift, 1.5*UP), run_time = 1 )
        self.wait(2.09) #让我们用同余来研究这个问题

        module_1 = Module(r"x^2", r"4", r"x-2")
        module_1.shift(DOWN)
        name_module = Text("同余式", font = 'simsun')
        name_module.scale(0.8)
        name_division = Text("带余除法", font = 'simsun')
        name_division.scale(0.8)
        name_division.shift(2*UP)
        self.play(FadeIn(module_1.text), FadeIn(name_module), FadeIn(name_division))
        self.wait(0.49) #和整数一样

        self.play(ShowCreationThenDestructionAround(equation_example_5_equation.former), ShowCreationThenDestructionAround(equation_example_5_replace_2), run_time = 1.5)
        self.wait(0.83) #如果两个整式的余数相同

        self.play(TransformFromCopy(equation_example_5_equation.former, module_1.dividend), TransformFromCopy(equation_example_5_equation.latter, module_1.divisor), TransformFromCopy(equation_example_5_replace_2, module_1.remainder))
        self.play(Indicate(module_1))
        self.wait(0.57) #我们也可以把它们放在同余号的两边

        self.wait(0.70) #（空闲）
        self.remove(equation_example_5, module_1, name_module, name_division)

        plus = ModuleProperty(r"a+c\equiv b+d\ (\bmod\ m)", 0)
        plus.shift(1.5*UP)
        minus = ModuleProperty(r"a-c\equiv b-d\ (\bmod\ m)", 0)
        multiply = ModuleProperty(r"ac\equiv bd\ (\bmod\ m)", 0)
        multiply.shift(1.5*DOWN)
        plus_poly = ModuleProperty(r"a(x)+c(x)\equiv b(x)+d(x)\ (\bmod\ m(x))", 1)
        plus_poly.shift(1.5*UP)
        minus_poly = ModuleProperty(r"a(x)-c(x)\equiv b(x)-d(x)\ (\bmod\ m(x))", 1)
        multiply_poly = ModuleProperty(r"a(x)c(x)\equiv b(x)d(x)\ (\bmod\ m(x))", 1)
        multiply_poly.shift(1.5*DOWN)
        
        self.wait(1.14) #对于整数成立的...
        self.play(FadeIn(plus, UP))
        self.wait(0.23) #...加法...
        self.play(FadeIn(minus, UP))
        self.wait(0.31) #...减法...
        self.play(FadeIn(multiply, UP))
        self.wait(0.54) #...乘法

        self.play(Transform(plus, plus_poly), Transform(minus, minus_poly), Transform(multiply, multiply_poly), ReplacementTransform(notice5, notice6))
        self.wait(0.96) #对于整式同样成立
        self.wait(1.16) #（空闲）

        module_inverse_text_1 = Text("如果", font = "simsun")
        module_inverse_1 = Tex(r"a(x)b(x)\equiv 1\ (\bmod\ m(x))", color = GREEN)
        module_inverse_text_2 = Text("，定义", font = "simsun")
        module_inverse_2 = Tex(r"a^{-1}(x)\equiv b(x)\ (\bmod\ m(x))", color = YELLOW)
        module_inverse_text_3 = Text("。", font = "simsun")

        module_inverse_text_1.shift(5*LEFT)
        module_inverse_1.shift(2.5*LEFT)
        module_inverse_text_2.shift(0.2*RIGHT)
        module_inverse_2.shift(3.2*RIGHT)
        module_inverse_text_3.shift(5.3*RIGHT+0.1*DOWN)
        module_inverse_text_1.scale(0.7)
        module_inverse_1.scale(0.7)
        module_inverse_text_2.scale(0.7)
        module_inverse_2.scale(0.7)
        module_inverse_text_3.scale(0.7)

        module_inverse = VGroup(module_inverse_text_1, module_inverse_1, module_inverse_text_2, module_inverse_2, module_inverse_text_3)
        module_inverse.shift(0.5*UP)

        module_division_with_inverse = Tex(r"(x+3)^{-1}\equiv x+4\ (\bmod\ x^2+7x+11)")
        module_division_with_inverse.shift(DOWN)
        module_division_with_inverse.scale(0.7)

        module_inverse_name_1 = Text("数论倒式", font = "simsun")
        module_inverse_name_1.shift(2*UP)
        cross_line_1 = Line(np.array([-0.6,0.6,0])+2*UP, np.array([-0.6,0.6,0])+2*UP, color = RED)
        cross_line_2 = Line(np.array([0.6,0.6,0])+2*UP, np.array([0.6,0.6,0])+2*UP, color = RED)
        cross_lines = VGroup(cross_line_1, cross_line_2)
        
        module_inverse_name_2 = Text("逆元", font = "simsun")
        module_inverse_name_2.shift(2*UP)

        self.remove(plus, minus, multiply)
        self.play(FadeIn(module_inverse, DOWN), ReplacementTransform(notice6, notice7))
        self.wait(0.30) #至于除法...
        self.play(Write(module_division_with_inverse), run_time = 1.5)
        self.wait(1.60) #...嗯......还是那么难算

        self.play(FadeIn(module_inverse_name_1))
        self.play(ApplyMethod(cross_line_1.put_start_and_end_on, np.array([-0.6,0.6,0])+2*UP, np.array([0.6,-0.6,0])+2*UP) , rate_func=rush_into, run_time = 0.5)
        self.play(ApplyMethod(cross_line_2.put_start_and_end_on, np.array([0.6,0.6,0])+2*UP, np.array([-0.6,-0.6,0])+2*UP) , rate_func=rush_from, run_time = 0.5)
        self.wait(1.64) #不过可能是因为“数论倒式”这个名字太怪了

        self.play(FadeIn(module_inverse_name_2, DOWN), FadeOut(cross_lines, DOWN), FadeOut(module_inverse_name_1, DOWN))
        self.wait(1.03) #一般都直接叫“逆元”
        self.wait(1.74) #（空闲）

        title2 = Text("一次式同余", font = 'simsun', color = YELLOW)
        title2.next_to(title_line, UP)
        self.remove(module_inverse_name_2, module_division_with_inverse, module_inverse)
        self.play(ReplacementTransform(notice7, notice8), ReplacementTransform(title, title2))
        self.wait(1.11) #对一个一次式取模的话
        self.wait(2.35) #还会有一些小惊喜

        equation_linear_1 = Equation(r"x",r"\divisionsymbol", r"(x-a)", r"1\ \cdots\cdots\ a")
        equation_linear_1.former.next_to(equation_linear_1.symbol, LEFT)
        module_linear_1 = Module(r"x", r"a", r"x-a")
        self.play(Write(equation_linear_1.result_others), run_time = 1)
        self.wait(1.43) #我们用x除以x-a
        self.play(FadeIn(equation_linear_1.result, RIGHT))
        self.wait(0.68) #余数是a

        self.wait(1.13) #也就是说...
        self.play(ReplacementTransform(equation_linear_1, module_linear_1))
        self.wait(1.00) #...x和a是同余的
        self.wait(0.73) #（空闲）

        module_linear_2 = module_linear_1.copy()
        module_linear_2.shift(UP)
        frame_1 = SurroundingRectangle(module_linear_1, stroke_color = WHITE)
        frame_2 = SurroundingRectangle(module_linear_2, stroke_color = WHITE)
        mult_symbol = Tex(r"\times")
        mult_symbol.next_to(module_linear_1, LEFT)
        equation_line = Line(np.array([-2.5,-0.5,0]), np.array([3.5,-0.5,0]))
        frames = VGroup(frame_1, frame_2, mult_symbol, equation_line)
        self.play(TransformFromCopy(module_linear_1, module_linear_2))
        self.play(FadeIn(frames), run_time = 0.5)
        self.wait(0.51) #把这个式子乘以自身

        module_linear_3 = Module(r"x^2", r"a^2", r"x-a")
        module_linear_3.shift(DOWN)
        module_linear_4 = Module(r"x^n", r"a^n", r"x-a")
        module_linear_4_tex = Tex(r"\forall\ n\in \mathbb{N},")
        module_linear_4_tex.shift(UP)
        self.play(Write(module_linear_3), run_time = 2)
        self.wait(1.72) #我们就能得到x^2和a^2同余
        self.wait(0.81) #（空闲）

        self.play(FadeOut(frames), FadeOut(module_linear_1), FadeOut(module_linear_2))
        self.wait(0.25) #更进一步
        self.play(FadeIn(module_linear_4_tex), ReplacementTransform(module_linear_3, module_linear_4))
        self.wait(1.89) #x和a的任意次方都是同余的
        self.wait(1.20) #（空闲）

        self.remove(module_linear_4_tex, module_linear_4)
        self.wait(2.98) #多项式也只是单项式的加和而已
        poly_linear_formula = Polynomial(np.array([2,-3,5,1]), 0)
        poly_linear_formula.next_to(np.array([-1,1,0]), RIGHT)
        poly_linear_tex = Tex(r"f(x) = ")
        poly_linear_tex.next_to(np.array([-1,1,0]), LEFT)
        poly_linear = VGroup(poly_linear_formula, poly_linear_tex)
        poly_linear_module_1_tex = Tex(r"\equiv")
        poly_linear_module_1_tex.next_to(np.array([-1,0,0]), LEFT)
        poly_linear_module_1_value = Tex(r"a^3+5a^2-3a+2\ (\bmod\ x-a)")
        poly_linear_module_1_value.next_to(np.array([-1,0,0]), RIGHT)
        poly_linear_module_1 = VGroup(poly_linear_module_1_tex, poly_linear_module_1_value)
        poly_linear_module_2_tex = Tex(r"\equiv")
        poly_linear_module_2_tex.next_to(np.array([-1,-1,0]), LEFT)
        poly_linear_module_2_value = Tex(r"f(a)\ (\bmod\ x-a)")
        poly_linear_module_2_value.next_to(np.array([-1,-1,0]), RIGHT)
        poly_linear_module_2 = VGroup(poly_linear_module_2_tex, poly_linear_module_2_value)
        poly_linear_all = VGroup(poly_linear, poly_linear_module_1, poly_linear_module_2)
        poly_linear_module = Module(r"f(x)", r"f(a)", r"x-a")

        self.play(Write(poly_linear), run_time = 2)
        self.wait(0.67) #对于任何一个多项式f（x）
        self.play(TransformFromCopy(poly_linear, poly_linear_module_1))
        self.wait(2.65) #我们都可以把其中的所有x替换成a
        self.play(FadeIn(poly_linear_module_2, RIGHT))
        self.wait(0.28) #也就是说
        self.wait(2.54) #f（x）除以x-a
        self.play(ReplacementTransform(poly_linear_all, poly_linear_module))
        self.play(ShowCreationThenDestructionAround(poly_linear_module))
        self.wait(1.51) #余数是f（x）在x=a处取到的值
        self.wait(0.82) #（空闲）

        self.remove(poly_linear_module)
        module_inverse = Module(r"f^{-1}(x)", r"f^{-1}(a)", r"x-a")
        self.play(FadeIn(module_inverse.text), FadeIn(module_inverse.dividend), FadeIn(module_inverse.divisor))
        self.wait(1.45+1.96-1) #求逆元的时候 还有另一份惊喜
        module_inverse_replace = Module(r"f^{-1}(x)", r"\frac{1}{f(a)}", r"x-a")
        
        self.remove(module_inverse.text, module_inverse.dividend, module_inverse.divisor, title2, title_line)
        equation_example_3 = Equation(r"(5x+5)", r"\divisionsymbol", r"(2x+2)", r"\frac{5}{2}")
        equation_example_3.shift(1.5*LEFT+0.5*DOWN)
        equation_example_3.former.shift(0.25*LEFT)
        equation_example_3.symbol.shift(0.15*LEFT)
        equation_example_3.latter.shift(0.05*LEFT)
        longdivision4 = PolynomialLongDivision(np.array([5,5]), np.array([2,2]))
        longdivision4.shift(1.5*RIGHT)
        longdivision4_replace = Tex(r"\frac{5}{2}")
        longdivision4_replace.next_to(1.5*UP+3.6*RIGHT, UP+LEFT)
        longdivision4.poly_quotient.set_opacity(0)
        
        self.play(FadeIn(equation_example_3), FadeIn(longdivision4), FadeIn(longdivision4_replace), ReplacementTransform(notice8, notice9))
        self.wait(0.62) #之前我们说过
        self.wait(2.76) #整式的系数可以出现分数
        module_inverse_constant = Module(r"\left(\frac{5}{2}\right)^{-1}", r"\frac{2}{5}", r"f(x)")
        self.play(FadeOut(equation_example_3, DOWN), FadeOut(longdivision4, DOWN), FadeOut(longdivision4_replace), FadeIn(module_inverse_constant, DOWN), FadeIn(title2), FadeIn(title_line), ReplacementTransform(notice9, notice10))
        self.wait(2.20) #常数的逆元 就是常数的倒数
        copy = poly_linear_module.copy()
        self.play(FadeOut(module_inverse_constant, DOWN), FadeIn(copy, DOWN))
        self.wait(3.62) #而多项式f（x）同余于在a处的取值f（a）
        self.play(ReplacementTransform(copy, module_inverse))
        self.play(ReplacementTransform(module_inverse, module_inverse_replace))
        self.wait(0.50) #它的逆元就是1/f（a）
        self.wait(1.86) #（空闲）

        poly_linear_module.shift(0.5*UP)
        self.play(FadeIn(poly_linear_module, 0.5*DOWN), ApplyMethod(module_inverse_replace.shift,0.5*DOWN), ReplacementTransform(notice10, notice11))
        self.wait(0.69) #对一次式来说
        self.play(Indicate(poly_linear_module))
        self.wait(0.27) #无论是余数
        self.play(Indicate(module_inverse_replace))
        self.wait(0.24) #还是逆元
        properties = VGroup(poly_linear_module, module_inverse_replace)
        self.play(ShowCreationThenDestructionAround(properties))
        self.wait(2.00) #都没什么难算的
        self.wait(1.76) #而这些优异的性质
        self.wait(3.10) #帮助我们推开了拉格朗日插值法的大门
        self.wait(3.34) #（空闲）
        self.play(FadeOut(properties), FadeOut(notice11), FadeOut(title2), FadeOut(title_line))
        self.wait(2.00) #（空闲）
        #"""


        print(self.get_time())
        
        
        
        
        
        
        
        
        
        
        """
        ##  Making object
        longdivision1 = PolynomialLongDivision(np.array([0,0,0,0,1]), np.array([-2,1]))
        longdivision1.shift(3*RIGHT)
        longdivision1.scale(0.6)
        longdivision2 = IntegerLongDivision(np.array([6,5,1]), np.array([2,1]))
        longdivision2.shift(3*LEFT)

        ##  Position

        ##  Showing object
        self.add(longdivision1, longdivision2)
        """