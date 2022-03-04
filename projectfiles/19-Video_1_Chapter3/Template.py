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
        
        self.remainder.next_to(self.bra.get_corner(LEFT), LEFT)
        self.modulesymbol.next_to(self.remainder.get_corner(LEFT), LEFT)
        self.dividend.next_to(self.modulesymbol.get_corner(LEFT), LEFT)
        self.moduletext.next_to(self.bra.get_corner(RIGHT), RIGHT)
        self.divisor.next_to(self.moduletext.get_corner(RIGHT), RIGHT)
        self.ket.next_to(self.divisor.get_corner(RIGHT), RIGHT)

        self.text = VGroup(self.modulesymbol, self.bra, self.moduletext, self.ket)

class Template(Scene):
    def construct(self):

        notice0 = Notice("最后一步", "请　专注")
        notice1 = Notice("前情提要", "请　复习")
        notice2 = Notice("数学定理", "请记笔记")
        notice3 = Notice("前情提要", "请　复习")
        notice4 = Notice("合情推理", "谨慎验证")
        notice5 = Notice("证明完毕", "请　鼓掌")

        #第三节-0
        """
        text3 = Text("第三节　整式的中国剩余定理", font = 'simsun', t2c={"第三节": YELLOW, "　整": GREEN, "的中国剩余定": BLUE})
        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))
        """

        title = Text("整式的中国剩余定理", font = 'simsun', color = YELLOW)
        title_line = Line(np.array([0,3,0]), np.array([0,3,0]))
        title.next_to(title_line, UP)

        self.add(notice0)
        self.wait(3.41) #我们现在离拉格朗日插值法只有最后一步了
        self.wait(1.37) #而这最后一步
        self.play(Write(title), ApplyMethod(title_line.put_start_and_end_on, np.array([-6,3,0]), np.array([6,3,0])), run_time = 1)
        self.wait(0.76) #就是整式的中国剩余定理
        self.wait(0.79) #（空闲）

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
        title2 = Text("中国剩余定理", font = 'simsun', color = YELLOW)
        title2.next_to(title_line, UP)

        self.remove(title)
        self.play(FadeIn(group_text, DOWN), FadeIn(title2, DOWN), ReplacementTransform(notice0, notice1))
        self.wait(1.90) #还记得之前说到过的中国剩余定理吗

        self.play(ShowCreationThenDestructionAround(module_equations), run_time = 2)
        self.wait(0.15) #如果要解一个同余方程
        self.play(WiggleOutThenIn(tex_3), run_time = 2)
        self.wait(0.45) #我们只需要找到每个数的基向量
        self.play(ShowCreationThenDestructionAround(module_solution), run_time = 2)
        self.wait(0.44) #然后相乘 再加起来
        self.wait(1.40) #而找基向量
        self.play(WiggleOutThenIn(tex_2), WiggleOutThenIn(tex_4), run_time = 2)
        self.wait(0.12) #就是先把其它数都乘起来
        self.play(ShowCreationThenDestructionAround(tex_3), run_time = 2)
        self.wait(1.98+0.81-2) #再乘上相应的数论倒数

        text_1 = Text("对于同余方程组", font = 'simsun')
        module_equation_1 = Module(r"f(x)", r"a_1(x)", r"m_1(x)")
        module_equation_2 = Module(r"f(x)", r"a_2(x)", r"m_2(x)")
        module_equation_3 = Module(r"f(x)", r"a_3(x)", r"m_3(x)")
        module_equation_4 = Tex(r"\cdots")
        module_equation_5 = Module(r"f(x)", r"a_n(x)", r"m_n(x)")
        module_equation_1.shift(1.6*UP)
        module_equation_2.shift(0.8*UP)
        module_equation_4.shift(0.8*DOWN)
        module_equation_5.shift(1.6*DOWN)
        module_equations = VGroup(module_equation_1, module_equation_2, module_equation_3, module_equation_4, module_equation_5)
        copy_equations = module_equations.copy()
        text_2 = Text("，其中", font = 'simsun')
        text_2_replace = Text("，", font = 'simsun')
        tex_1 = Tex("m_i(x)", color = YELLOW)
        text_3 = Text("两两互质，", font = 'simsun')

        text_1.shift(1.5*UP+6.5*LEFT)
        module_equations.shift(1.45*UP+0.95*LEFT)
        text_2.shift(1.5*UP+3.5*RIGHT)
        text_2_replace.shift(0.7*(1.3*UP+2.5*RIGHT))
        text_2_replace.scale(0.7)
        tex_1.shift(1.45*UP+5.25*RIGHT)
        text_3.shift(1.5*UP+7.5*RIGHT)

        text_4 = Text("其解为", font = 'simsun')
        module_solution = Module(r"f(x)", r"\sum_{i=1}^na_i(x)\vec{e}_i(x)", r"M(x)")
        module_solution_replace = Module(r"f(x)", r"\sum_{i=1}^nf(x_i)\vec{e}_i(x)", r"M(x)")
        module_solution_replace.scale(0.7)
        module_solution_replace_2 = Module(r"f(x)", r"\sum_{i=1}^nf(x_i)\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}", r"M(x)")
        module_solution_replace_2.scale(0.7)
        text_5 = Text("，", font = 'simsun')
        tex_2 = Tex("M(x)=\prod_{i=1}^nm_i(x)", color = YELLOW)
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
        tex_3 = Tex(r"\vec{e}_i(x) = M_i(x)[M_i(x)]^{-1}_{\bmod m_i(x)}", color = ORANGE)
        text_8 = Tex(",", color = ORANGE)
        text_8_replace = Text("。", font = 'simsun')
        tex_4 = Tex(r"M_i(x) = \frac{M(x)}{m_i(x)},\ i=1,2,\cdots, n",color = GOLD)
        text_9 = Text("。", font = 'simsun')

        text_7.shift(3*DOWN + 6.8 * LEFT)
        tex_3.next_to(text_7, RIGHT)
        text_8.next_to(tex_3, RIGHT)
        tex_4.next_to(text_8, RIGHT)
        text_9.next_to(tex_4, RIGHT)
        text_8.shift(0.15*DOWN)
        text_9.shift(0.15*DOWN)

        group_text_2 = VGroup(text_1, module_equations, text_2, tex_1, text_3, text_4, module_solution, text_5, tex_2, text_6, text_7, tex_3, text_8, tex_4, text_9)
        group_text_2.scale(0.7)
        text_8_replace.scale(0.7)
        text_8_replace.next_to(tex_3, RIGHT)
        text_8_replace.shift(0.15*DOWN+0.4*RIGHT)
        group_text_replace_1 = VGroup(text_1, text_2_replace, text_4, module_solution, text_5, tex_2, text_6, text_7, tex_3, text_8, tex_4, text_9)
        group_text_replace_2 = VGroup(text_1, copy_equations, text_2_replace, text_4, module_solution, text_5, text_6, text_7, text_8, text_9)
        group_text_replace_3 = VGroup(text_1, copy_equations, text_2_replace, text_4, module_solution, text_5, tex_2, text_6, text_7, text_8_replace)
        group_text_replace_4 = VGroup(text_1, copy_equations, text_2_replace, text_4, text_5, tex_2, text_6, text_7, text_8_replace)
        module_solution_replace.next_to(text_4, RIGHT)
        module_solution_replace_2.next_to(text_5, LEFT)
        module_solution_replace_2.shift(0.12*UP)

        self.play(ReplacementTransform(group_text, group_text_2), ReplacementTransform(title2, title), ReplacementTransform(notice1, notice2))
        self.wait(1.56) #对于整式来说 也一样
        self.play(ShowCreationThenDestructionAround(module_equations), run_time = 2)
        self.wait(0.48) #如果要解一个整式的同余方程组
        self.play(WiggleOutThenIn(tex_3), run_time = 2)
        self.wait(0.53) #我们只需要找到每个整式的基向量
        self.play(ShowCreationThenDestructionAround(module_solution), run_time = 2)
        self.wait(0.29) #然后相乘 加起来
        self.wait(1.28) #而找基向量
        self.play(WiggleOutThenIn(tex_2), WiggleOutThenIn(tex_4), run_time = 2)
        self.wait(0.19) #也是先把其它整式都乘起来
        self.play(ShowCreationThenDestructionAround(tex_3), run_time = 2)
        self.wait(1.71+0.81-2) #再乘上相应的逆元

        linear_module = Module(r"f(x)", r"f(a)", r"x-a")
        linear_module.shift(0.5*UP)
        linear_reverse = Module(r"f^{-1}(x)", r"\frac{1}{f(a)}", r"x-a")
        linear_reverse.shift(0.5*DOWN)
        linear = VGroup(linear_module, linear_reverse)
        self.remove(group_text_2, title, title_line)
        self.play(FadeIn(linear, UP), ReplacementTransform(notice2, notice3))
        self.wait(0.94) #我们在第二节已经见过
        self.wait(1.46) #对一次式取模
        self.wait(2.82) #往往会得到一些很漂亮的结果

        copy_equations.shift(3*RIGHT)
        copy_equations.scale(0.7)
        copy_linear = linear.copy()
        copy_linear.shift(3*LEFT)
        copy_linear.scale(0.7)
        self.play(Transform(linear, copy_linear), FadeIn(copy_equations, UP), ReplacementTransform(notice3, notice4))
        self.wait(1.74) #如果在解整式的同余方程组的时候

        module_linear_1 = Module(r"f(x)", r"a_1(x)", r"x-x_1")
        module_linear_2 = Module(r"f(x)", r"a_2(x)", r"x-x_2")
        module_linear_3 = Module(r"f(x)", r"a_3(x)", r"x-x_3")
        module_linear_4 = Tex(r"\cdots")
        module_linear_5 = Module(r"f(x)", r"a_n(x)", r"x-x_n")
        module_linear_1.shift(1.6*UP)
        module_linear_2.shift(0.8*UP)
        module_linear_4.shift(0.8*DOWN)
        module_linear_5.shift(1.6*DOWN)
        module_linears = VGroup(module_linear_1, module_linear_2, module_linear_3, module_linear_4, module_linear_5)
        module_linears.scale(0.7)
        module_linears.shift(3*RIGHT)

        module_value_1 = Module(r"f(x)", r"f(x_1)", r"x-x_1")
        module_value_2 = Module(r"f(x)", r"f(x_2)", r"x-x_2")
        module_value_3 = Module(r"f(x)", r"f(x_3)", r"x-x_3")
        module_value_4 = Tex(r"\cdots")
        module_value_5 = Module(r"f(x)", r"f(x_n)", r"x-x_n")
        module_value_1.shift(1.6*UP)
        module_value_2.shift(0.8*UP)
        module_value_4.shift(0.8*DOWN)
        module_value_5.shift(1.6*DOWN)
        module_values = VGroup(module_value_1, module_value_2, module_value_3, module_value_4, module_value_5)
        module_values.scale(0.7)

        self.play(Transform(copy_equations, module_linears))
        self.wait(1.37) #这些整式全部是一次式
        self.wait(1.77+1.45) #中国剩余定理的样子 会不会好看一些呢
        self.wait(0.86) #（空闲）

        property_line = Line(np.array([0,2.35,0]), np.array([0,2.35,0]))
        self.play(ApplyMethod(linear.move_to, 3.1*UP), ApplyMethod(copy_equations.move_to, np.array([0,0,0])), ApplyMethod(property_line.put_start_and_end_on, np.array([-5,2.35,0]), np.array([5,2.35,0])))
        self.wait(0.18) #我们来试试吧
        self.wait(0.69) #（空闲）

        self.play(ShowCreationThenDestructionAround(copy_equations))
        self.wait(1.10) #我们首先来看条件
        self.wait(1)
        self.play(Indicate(linear_module), run_time = 2)
        self.wait(2.41) #由于f（x）和f（x1）关于x-x1是同余的
        self.play(ShowCreationThenDestructionAround(module_value_1.remainder))
        self.play(Transform(copy_equations[0], module_value_1))
        self.wait(2.00) #我们可以得到f（x1）同余于a1
        self.wait(1.78) #其它的式子也是一样
        self.play(Transform(copy_equations[1], module_value_2))
        self.wait(1)
        self.play(Transform(copy_equations[2], module_value_3))
        self.play(ApplyWave(copy_equations[3]))
        self.play(ApplyWave(copy_equations[3]))
        self.play(ApplyWave(copy_equations[3]))
        self.play(Transform(copy_equations[4], module_value_5))
        self.wait(3)
        # 到此为止共80秒
        
        self.play(FadeIn(group_text_replace_1), ApplyMethod(copy_equations.shift, 0.7*(1.35*UP+0.95*LEFT)))
        self.wait(2)
        self.play(Transform(module_solution, module_solution_replace))
        self.wait(3.26+1.99-4) #于是 我们可以把解里面所有的ai 全部替换成f（xi）
        self.wait(0.67) #（空闲）
        
        self.play(ShowCreationThenDestructionAround(tex_2), ShowCreationThenDestructionAround(tex_4))
        self.wait(0.97) #式子里还有一个乘积
        copy_1 = tex_2.copy()
        copy_2 = tex_4.copy()
        copy_3 = tex_3.copy()
        copies = VGroup(copy_1, copy_2, copy_3)
        self.add(copies)
        self.remove(tex_2, tex_3, tex_4)
        self.play(FadeOut(group_text_replace_2), ApplyMethod(copy_1.move_to, np.array([-5,1.5,0])), ApplyMethod(copy_2.move_to, np.array([-1,1.5,0])), ApplyMethod(copy_3.move_to, np.array([4,1.5,0])))
        self.wait(0.94) #它有没有好一点的表达式呢
        self.wait(0.62) #（空闲）
        
        multiply_1 = Tex(r"M_1(x) = \frac{(x-x_1)(x-x_2)\cdots(x-x_n)}{x-x_1}")
        multiply_1.scale(0.7)
        multiply_1.next_to(np.array([-3.55, 0.5, 0]), RIGHT)
        multiply_2 = Tex(r"M_1(x) = (x-x_2)\cdots(x-x_n)")
        multiply_2.scale(0.7)
        multiply_2.next_to(np.array([-3.55, 0.5, 0]), RIGHT)
        multiply_inverse = Module(r"[M_1(x)]^{-1}_{\bmod x-x_1}", r"M^{-1}_1(x)", r"x-x_1")
        multiply_inverse.scale(0.7)
        multiply_inverse.next_to(np.array([-3.55, -0.5, 0]), RIGHT)
        multiply_inverse_replace = Tex(r"\frac{1}{M_1(x_1)}", color = BLUE)
        multiply_inverse_replace.scale(0.7)
        multiply_inverse_replace.next_to(multiply_inverse.modulesymbol, RIGHT)
        self.play(TransformFromCopy(copy_2, multiply_1))
        self.wait(0.5)
        self.play(Transform(multiply_1, multiply_2))
        self.wait(0.13) #虽然乘积本身没有涉及取模
        anim1 = ShowCreationThenDestructionAround(copy_3)
        anim1.update_config(run_time = 2)
        anim2 = FadeIn(multiply_inverse, UP)
        anim2.update_config(run_time = 1)
        self.play(anim1, anim2)
        self.wait(0.98) #但是它的逆元却涉及到了取模
        
        self.wait(1)
        self.play(Indicate(linear_reverse), run_time = 2)
        self.wait(2.58) #f（x）关于x-x1的逆元是1/f（x1）
        self.play(ShowCreationThenDestructionAround(multiply_inverse.remainder), run_time = 2)
        self.wait(1.68) #那么M1（x）关于x-x1的逆元
        self.play(Transform(multiply_inverse.remainder, multiply_inverse_replace))
        self.wait(1.67) #就是1/M1（x）

        base_1 = Tex(r"\vec{e}_1(x) = M_1(x)[M_1(x)]^{-1}_{\bmod x-x_1}", color = ORANGE)
        base_1.scale(0.7)
        base_1.next_to(np.array([-5, -1.5, 0]), RIGHT)
        base_2 = Tex(r"=\frac{M_1(x)}{M_1(x_1)}")
        base_2.scale(0.7)
        base_2.next_to(base_1)
        base_3 = Tex(r"=\frac{(x-x_2)\cdots(x-x_n)}{(x_1-x_2)\cdots(x_1-x_n)}", color = BLUE)
        base_3.scale(0.7)
        base_3.next_to(base_2)
        base_4 = Tex(r"=\prod_{j\ne 1}\frac{x-x_j}{x_1-x_j}")
        base_4.scale(0.7)
        base_4.next_to(np.array([-4.15, -2.5, 0]), RIGHT)
        
        self.play(TransformFromCopy(copy_3, base_1))
        self.wait(1)
        self.play(TransformFromCopy(multiply_inverse, base_2))
        self.play(TransformFromCopy(multiply_1, base_3))
        self.wait(1.29+3.04-4) #也就是说 x-x1的基向量 e1
        self.play(FadeIn(base_4, UP))
        temp = VGroup(base_1, base_4)
        self.wait(0.26) #展开以后是这个样子的
        self.play(ShowCreationThenDestructionAround(temp))
        self.wait(4.06) #（空闲）

        
        base_0 = Tex(r"\vec{e}_i(x)=\prod_{j\ne i}\frac{x-x_j}{x_i-x_j},\ i = 1,2 \cdots, n", color = GOLD)
        self.wait(1.60) #其它的基向量 
        self.play(FadeOut(linear), FadeOut(property_line), FadeOut(copies), FadeOut(multiply_1), FadeOut(multiply_1), FadeOut(multiply_inverse), FadeOut(base_2), FadeOut(base_3), Transform(temp, base_0), run_time = 2)
        self.wait(0.63) #展开以后也都是这个样子的
        self.play(ShowCreationThenDestructionAround(temp), run_time = 2)
        self.wait(4.78) #（空闲）
        print(self.get_time())

        copy = temp.copy()
        copy.scale(0.7)
        copy.next_to(text_7, RIGHT)
        copy.shift(0.15*DOWN)
        self.play(FadeIn(group_text_replace_3), ReplacementTransform(temp, copy))
        self.play(Transform(module_solution, module_solution_replace_2), ApplyMethod(text_4.next_to, module_solution_replace_2, LEFT))
        self.wait(1.00) #把基向量的表达式带回到解里面去
        temp = VGroup(module_solution[0], module_solution[1], module_solution[2])
        self.play(ShowCreationThenDestructionAround(temp))
        self.wait(0.27) #我们得到的
        
        tex_result_1 = Tex(r"f(x)", color = GREEN)
        tex_result_2 = Tex(r"=")
        tex_result_3 = Tex(r"\sum_{i=1}^nf(x_i)\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}", color = BLUE)
        tex_result_2.shift(2*LEFT)
        tex_result_1.next_to(tex_result_2, LEFT)
        tex_result_3.next_to(tex_result_2, RIGHT)
        module_solution_others = VGroup(module_solution[3], module_solution[4], module_solution[5], module_solution[6])
        self.play(FadeOut(group_text_replace_4), FadeOut(module_solution_others), FadeOut(copy), Transform(module_solution[0], tex_result_1), Transform(module_solution[1], tex_result_2), Transform(module_solution[2], tex_result_3), ReplacementTransform(notice4, notice5), run_time = 2)
        self.wait(1.58) #就正好是拉格朗日插值法的表达式
        self.wait(4)
        self.play(FadeOut(temp), FadeOut(notice5))
        self.wait(2.5)

        
         
        print(self.get_time())

        ##  Making object

        ##  Position

        ##  Showing object
        pass