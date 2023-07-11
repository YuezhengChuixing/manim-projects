from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Intro0(FrameScene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("搞明白计算步骤在干什么，\n有的时候是理解一道题的关键，\n有的时候是理解一道题的最大阻碍。", font = 'simsun', t2c={"计算步骤": GREEN, "关键": BLUE, "最大阻碍": YELLOW})
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DR), DL)
        ##  Showing object
        self.play(Write(quote), runtime = 2)
        self.play(Write(author), Write(notice0))
        self.wait(2)
        self.play(FadeOut(quote), FadeOut(author))
        self.wait(1)

class Intro1(FrameScene):
    def construct(self):
        self.notices = [Notice("沃茨基·硕德", "请勿模仿"), 
                        Notice("视频前言", "请听介绍"),
                        Notice("连 分 数", "请　好奇"),
                        Notice("形式证明", "请勿模仿"),
                        Notice("通用定义", "请　模仿"),
                        Notice("奇妙规律", "请　好奇"),
                        Notice("传统艺能", "请　三连")]
        self.notice = self.notices[0]
        
        root2 = MTex(r"\sqrt{2}").scale(2)
        self.play(self.change_notice(), Write(root2))
        self.wait(2, 21) #这是√2 我们最早接触到的几个无理数之一
        self.wait(0, 19) #（空闲）

        text_0 = r"\sqrt{2}="
        texts = [r"|1+i|", r"\sec\frac{\pi}{4}", r"\sum_{{n}=0}^\infty(-1)^{{n}+1}\frac{(2{n}-3)!!}{(2{n})!!}", r"\prod_{k=0}^\infty\frac{(4k+2)^2}{(4k+1)(4k+3)}", r"{1}+\cfrac1{2+\cfrac1{2+\cfrac1{2+\cfrac1{\cdots}}}}"]
        color_maps = {(r"\sqrt{2}", r"i"): RED}, {(r"\sqrt{2}", r"\sec"): ORANGE}, {(r"\sqrt{2}", r"{n}"): YELLOW}, {(r"\sqrt{2}", r"k"): GREEN}, {r"{1}": GREEN, r"2": TEAL, r"\sqrt{2}": TEAL}
        mtexs = [MTex(text_0+texts[i], isolate = [text_0, texts[i]], tex_to_color_map = color_maps[i]) for i in range(5)]
        roots = [mtex.get_part_by_tex(text_0) for mtex in mtexs]
        formulas = [mtexs[i].get_part_by_tex(texts[i]) for i in range(5)]
        mtexs[0].save_state().scale(2).shift(-mtexs[0][0:3].get_center()).set_color(BACK)
        mtexs[0][0:3].set_color(WHITE)
        self.remove(root2).add(mtexs[0]).play(mtexs[0].animate.restore())
        self.wait()
        for i in range(3):
            self.play(ReplacementTransform(roots[i], roots[i+1]), FadeTransform(formulas[i], formulas[i+1]))
            self.wait()
        self.wait(2+2+0+2-8, 18+0+22+24) # 很多式子都能算出√2来 它们有的简单 有的复杂 （空闲） 但要从中挑选出最有规律的那个的话
        self.play(ReplacementTransform(roots[3], roots[4]), FadeTransform(formulas[3], formulas[4]), self.change_notice())
        self.wait(0, 24) #恐怕会是这个连分数
        self.wait(0, 19) #（空闲）

        self.play(mtexs[4].animate.shift(2*UP))
        self.wait(1, 5) #这个连分数有无穷多项
        self.wait(2, 25) #没法从最底层开始慢慢通分
        equation = MTex(r"x&={1}+\frac1{{1}+x}\\\Rightarrow x&=\pm\sqrt2", tex_to_color_map = {(r"x", r"\sqrt2"): TEAL, r"{1}": GREEN}).shift(1.5*DOWN)
        parts = [equation[0:9], equation[9:]]
        self.play(FadeIn(parts[0]), mtexs[4].save_state().animate.scale(0.5, about_point = 4*UP), self.change_notice())
        self.play(Write(parts[1]))
        self.wait(0, 5) #只能找别的方法来求它的值
        self.wait(0, 22) #（空闲）

        convergents_p = [MTex(r"\sqrt{2}={1}" + i*r"+\cfrac1{2" + r"+\cfrac1{{1}+\sqrt2}" + i*r"}", tex_to_color_map = color_maps[4]).scale(0.8) for i in range(3)]
        cf_p = MTex(r"\sqrt{2}={1}+\cfrac1{2+\cfrac1{2+\cfrac1{2+\cfrac1\cdots}}}", tex_to_color_map = color_maps[4]).scale(0.8)
        for mob in convergents_p + [cf_p]:
            mob.shift(6.5*LEFT + UP - mob[0].get_center())
        convergents_n = [MTex(r"-\sqrt{2}={1}" + i*r"+\cfrac1{2" + r"+\cfrac1{{1}-\sqrt2}" + i*r"}", tex_to_color_map = color_maps[4]).scale(0.8) for i in range(3)]
        cf_n = MTex(r"-\sqrt{2}={1}+\cfrac1{2+\cfrac1{2+\cfrac1{2+\cfrac1\cdots}}}", tex_to_color_map = color_maps[4]).scale(0.8)
        for mob in convergents_n + [cf_n]:
            mob.shift(1.5*RIGHT + UP - mob[0].get_center())
        self.play(Write(convergents_p[0]), Write(convergents_n[0]))
        self.wait()
        self.play(ReplacementTransform(convergents_p[0][:-3], convergents_p[1][:-7]), ReplacementTransform(convergents_p[0][-3:], convergents_p[1][-7:]), ReplacementTransform(convergents_n[0][:-3], convergents_n[1][:-7]), ReplacementTransform(convergents_n[0][-3:], convergents_n[1][-7:]))
        self.wait()
        self.play(ReplacementTransform(convergents_p[1][:-3], convergents_p[2][:-7]), ReplacementTransform(convergents_p[1][-3:], convergents_p[2][-7:]), ReplacementTransform(convergents_n[1][:-3], convergents_n[2][:-7]), ReplacementTransform(convergents_n[1][-3:], convergents_n[2][-7:]))
        self.wait()
        self.play(ReplacementTransform(convergents_p[2][:-3], cf_p[:-5]), ReplacementTransform(convergents_p[2][-3:], cf_p[-5:]), ReplacementTransform(convergents_n[2][:-3], cf_n[:-5]), ReplacementTransform(convergents_n[2][-3:], cf_n[-5:]))
        self.wait(2+3+0+1-7, 5+2+17+21) #这不是一件很容易的事情 有些方法会同时给出±√2两个答案 （空闲） 要想直接得到√2
        self.wait(1+0-1, 13+17)
        self.play(*[FadeOut(mob) for mob in [equation, cf_p, cf_n]], mtexs[4].animate.scale(4/3, about_point = 4*UP)) #还得用其它的手段 （空闲）
        
        convergents = [MTex(r"1", color = GREEN).scale(0.8)] + [MTex(r"{1}" + i*r"+\cfrac1{2" + r"+\cfrac1{2}" + i*r"}", tex_to_color_map = color_maps[4]).scale(0.8) for i in range(4)]
        for i in range(5):
            convergents[i].shift((i-6+0.35*i*i)*RIGHT + 0.5*UP - convergents[i][0].get_center())
        self.play(convergents[4].shift(4*RIGHT).animate.shift(4*LEFT), self.change_notice())
        for i in range(4, 0, -1):
            self.play(TransformFromCopy(convergents[i][:-4], convergents[i-1]))
        self.wait(3+1+0-5, 7+16+20) #比如说 我们可以把这个连分数截断 假装它只有有限项 （空闲）

        texts = [r"\frac{1}{1}", r"\frac{3}{2}", r"\frac{7}{5}", r"\frac{17}{12}", r"\frac{41}{29}"]
        values = [MTex(texts[i], color = BLUE if i%2 else GREEN).scale(0.8).set_y(-2.2).set_x(convergents[i].get_x()) for i in range(5)]
        self.wait(2, 5) #有限项的连分数可以通分
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in values[::-1]], lag_ratio = 0.3, run_time = 2))
        self.wait(1+0-2, 21+22) #也就可以得到准确值 （空闲）
        
        arrow = Arrow(1.5*DOWN + 6.4*LEFT, 1.5*DOWN + 5.6*RIGHT)
        self.play(ShowCreation(arrow, run_time = 2, rate_func = rush_into))
        self.wait(0, 8) #只要这些值能收敛到√2
        self.wait(2, 15) #那这也自然就是无穷连分数的值了
        self.wait(0, 28) #（空闲）

        all_texts = [r"\frac{1}{1}-\sqrt{2}=-0.414213\cdots", r"\frac{3}{2}-\sqrt{2}=0.085786\cdots", r"\frac{7}{5}-\sqrt{2}=-0.014213\cdots", r"\frac{17}{12}-\sqrt{2}=0.002453\cdots", r"\frac{41}{29}-\sqrt{2}=-0.000420\cdots"]
        diffs = [MTex(all_texts[i], isolate = [texts[i], r"="], tex_to_color_map = {texts[i]: BLUE if i%2 else GREEN, r"\sqrt{2}": TEAL}).scale(0.8).set_y((2-i)*1.2 + 0.3) for i in range(5)]
        for i in range(5):
            diffs[i].set_x(-2 - diffs[i].get_part_by_tex(r"=").get_x())
            values[i].generate_target().become(diffs[i].get_part_by_tex(texts[i]))
            diffs[i].remove(*diffs[i].get_part_by_tex(texts[i]))
        self.play(*[FadeOut(mob) for mob in [mtexs[4], arrow] + convergents])
        self.play(LaggedStart(*[MoveToTarget(values[i], path_arc = -10*DEGREES*(4-i)) for i in range(5)], lag_ratio = 0.25, run_time = 2))
        self.wait(0, 15) #所以 这些截断值到底离√2有多接近呢
        self.wait(0, 20) #（空闲）
        for i in range(5):
            values[i].refresh_bounding_box()

        self.play(LaggedStart(*[Write(mob) for mob in diffs], lag_ratio = 0.15, run_time = 2))
        self.wait(1, 0) #它们和√2的差 确实在不断变小
        self.wait(0, 23) #（空闲）
        self.wait(3+0-1, 1+19) 
        self.play(*[FadeOut(mob) for mob in diffs])# 但还有另一种更直观的方法 也能看出这一点 （空闲）

        self.play(self.change_notice())
        self.wait(1, 8) #这些数既然很接近√2
        texts = [r"\frac{1}{1}", r"\frac{9}{4}", r"\frac{49}{25}", r"\frac{289}{144}", r"\frac{1681}{841}"]
        all_texts = [r"\frac{1}{1}={2}-\frac 1{1}", r"\frac{9}{4}={2}+\frac 1{4}", r"\frac{49}{25}={2}-\frac 1{25}", r"\frac{289}{144}={2}+\frac 1{144}", r"\frac{1681}{841}={2}-\frac 1{841}"]
        diffs = [MTex(all_texts[i], isolate = [texts[i], r"=", r" 1"], tex_to_color_map = {texts[i]: BLUE_D if i%2 else GREEN_D, r"{2}": TEAL_D, r"+": BLUE, r"-": GREEN}).scale(0.8).set_y((2-i)*1.2 + 0.3) for i in range(5)]
        squares = [diffs[i].get_part_by_tex(texts[i]) for i in range(5)]
        ones = [diffs[i].get_part_by_tex(r" 1") for i in range(5)]
        for i in range(5):
            diffs[i].set_x(-1-diffs[i].get_part_by_tex(r"=").get_x()).remove(*squares[i])
        self.play(LaggedStart(*[FadeIn(mob, 0.5*RIGHT) for mob in squares], lag_ratio = 0.15, run_time = 1.5))
        self.wait(1+0-1, 21+21-15) #它们的平方就很接近2 （空闲）

        arrow = Arrow(values[2], squares[2])
        arrow.add(Text(r"平方", font = "simsun").scale(0.5).next_to(arrow, UP)).set_color(BACK)
        aim = Arrow(values[2].copy().set_x(0), squares[2].copy().shift(4*RIGHT))
        aim.add(Text(r"平方", font = "simsun").scale(0.5).next_to(aim, UP))

        self.play(LaggedStart(*[Write(mob) for mob in diffs], lag_ratio = 0.15, run_time = 2))
        self.wait(0, 3) #把这些平方和2相减
        self.play(LaggedStart(*[mob.save_state().animate.scale(1.2).set_fill(color = YELLOW) for mob in ones], lag_ratio = 0.15, run_time = 2))
        self.wait(0, 23) #得到的差全都是单位分数 （空闲）

        self.play(LaggedStart(*[mob.animate.restore() for mob in ones], lag_ratio = 0.15, run_time = 2))
        self.wait(0, 21) #等式两边分母相同 于是可以通分
        self.wait(0, 19) #（空闲）

        texts = r"1^{2}-2\times 1^{2}=-1", r"3^{2}-2\times 2^{2}={1}", r"7^{2}-2\times 5^{2}=-1", r"17^{2}-2\times 12^{2}={1}", r"41^{2}-2\times 29^{2}=-1"
        hyperbolas = [MTex(texts[i], color = BLUE if i%2 else GREEN, isolate = [r"="], tex_to_color_map = {r"-2": TEAL, (r"{2}", r"-", r"=", r"\times"): WHITE, r"-1": GREEN}).scale(0.8) for i in range(5)]
        for i in range(5):
            hyperbolas[i].set_x(-3-hyperbolas[i].get_part_by_tex(r"=").get_x()).set_y((2-i)*1.2 + 0.3)
        self.play(LaggedStart(*[mob.animate.shift(4*RIGHT) for mob in squares], lag_ratio = 0.15, run_time = 2), 
                  LaggedStart(*[mob.animate.shift(4*RIGHT) for mob in diffs], lag_ratio = 0.15, run_time = 2),
                  LaggedStart(*[mob.animate.set_x(0) for mob in values], lag_ratio = 0.15, run_time = 2),
                  LaggedStart(*[FadeIn(mob, 2*RIGHT) for mob in hyperbolas], lag_ratio = 0.15, run_time = 2),
                  Transform(arrow, aim, run_time = 2, rate_func = lambda t: smooth(clip(t*1.6-0.3, 0, 1))))
        self.wait(1+4-2, 22+0) #最后得到的结果是 分子的平方 和分母平方的两倍 会相差1
        self.wait(0, 21) #（空闲）

        self.wait(2, 7) #这无疑是个很美妙的规律
        self.wait(1, 14) #它背后的原理是什么呢
        self.wait(0, 20) #（空闲）

        like = Text("", font = 'vanfont').shift(3*LEFT).scale(2)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT).scale(2)
        sanlian = VGroup(like, coin, star)

        self.clear().add(self.notice).play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, ORIGIN), FadeInFromPoint(star, 3*RIGHT), self.change_notice())
        self.play(Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), sanlian.animate.set_color("#00A1D6"))
        self.wait(2, 1) #长按点赞一键三连 我们开始吧
        self.wait(2, 20)
        self.play(FadeOut(self.notice), FadeOut(sanlian))
        self.wait(2, 0) #到此共93秒

#################################################################### 

class Chapter1_0(FrameScene):

    def construct(self):

        text1 = MTexText("第一节 $\sqrt2$的有理逼近", tex_to_color_map={"第一节": YELLOW, "\sqrt2": GREEN, "有理逼近": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(FrameScene):
    def construct(self):
        self.notices = [Notice("奇妙规律", "请　好奇"), 
                        Notice("常规操作", "请　习惯"),
                        Notice("解析几何", "请　熟知"),
                        Notice("关键问题", "请　思考"),
                        Notice("小学数学", "请　显然"),
                        Notice("简单数论", "留作习题"),
                        Notice("线性变换", "请　熟知"),
                        Notice("数学归纳", "请　显然"),
                        Notice("下节预告", "请　好奇"),
                        ]
        self.notice = self.notices[0]

        texts = [r"\frac{1}{1}", r"\frac{3}{2}", r"\frac{7}{5}", r"\frac{17}{12}", r"\frac{41}{29}"]
        values = [MTex(texts[i], color = BLUE if i%2 else GREEN).scale(0.8).set_y((2-i)*1.2 + 0.3).set_x(-2.5) for i in range(5)]
        texts = r"1^{2}-2\times 1^{2}=-1", r"3^{2}-2\times 2^{2}={1}", r"7^{2}-2\times 5^{2}=-1", r"17^{2}-2\times 12^{2}={1}", r"41^{2}-2\times 29^{2}=-1"
        hyperbolas = [MTex(texts[i], color = BLUE if i%2 else GREEN, isolate = [r"=", r"{1}", r"-1"], tex_to_color_map = {r"-2": TEAL, (r"{2}", r"-", r"=", r"\times"): WHITE, r"-1": GREEN}).scale(0.8) for i in range(5)]
        for i in range(5):
            hyperbolas[i].set_x(2.5-hyperbolas[i].get_part_by_tex(r"=").get_x()).set_y((2-i)*1.2 + 0.3)

        self.play(Write(self.notice), *[FadeIn(mob, 0.5*RIGHT) for mob in values], *[FadeIn(mob, 0.5*LEFT) for mob in hyperbolas])
        self.wait(0, 26) #按照我们计算的结果
        self.play(*[values[i].animate.shift(4*RIGHT if i%2 else 2.5*LEFT) for i in range(5)], *[hyperbolas[i].animate.shift(2.5*RIGHT if i%2 else 4*LEFT) for i in range(5)])
        self.play(*[values[i].animate.shift(0.6*(2-i)*DOWN) for i in range(5)], *[hyperbolas[i].animate.shift(0.6*(2-i)*DOWN) for i in range(5)]) #这些截断值可以分为两类
        self.wait(0, 18) #（空闲）

        minus = [hyperbolas[i].get_part_by_tex(r"-1") for i in [0, 2, 4]]
        plus = [hyperbolas[i].get_part_by_tex(r"{1}") for i in [1, 3]]
        flash = [SurroundingRectangle(mob).scale(1.2) for mob in plus]
        self.play(*[mob.save_state().animate.set_color(YELLOW).scale(1.2) for mob in plus], *[ShowPassingFlash(mob, run_time = 2) for mob in flash])
        self.wait(0, 1) #一类是减出来为1的
        flash = [SurroundingRectangle(mob).scale(1.2) for mob in minus]
        self.play(*[mob.save_state().animate.set_color(YELLOW).scale(1.2) for mob in minus], *[ShowPassingFlash(mob, run_time = 2) for mob in flash]) #另一类是减出来为-1的
        self.wait(0, 24) #（空闲）

        group_p = VGroup(values[1], values[3], hyperbolas[1], hyperbolas[3])
        group_n = VGroup(values[0], values[2], values[4], hyperbolas[0], hyperbolas[2], hyperbolas[4])
        offset = 6*LEFT + 2.5*DOWN
        axes = VGroup(Arrow(0.5*LEFT, 7.5*RIGHT), Arrow(0.5*DOWN, 5.5*UP)).shift(offset)
        labels = VGroup(MTex(r"m").scale(0.75).next_to(axes[0], RIGHT), MTex(r"n").scale(0.75).next_to(axes[1], UP))
        self.play(group_p.animating(pah_arc = -PI/6).scale(0.75, about_point = 5*RIGHT).set_y(1.25), 
                  group_n.animating(run_time = 1.5, rate_func = squish_rate_func(smooth, 1/3, 1), path_arc = PI/6).scale(0.75, about_point = 1.5*LEFT).set_y(-1.25).shift(6.5*RIGHT),
                  ShowCreation(axes, lag_ratio = 0, run_time = 2, rate_func = squish_rate_func(smooth, 1/2, 1)), 
                  self.change_notice())
        self.wait(2, 17) #如果将分子和分母 分别当作横坐标和纵坐标
        positions = [np.array([1, 1, 0]), np.array([3, 2, 0]), np.array([7, 5, 0]), np.array([17, 12, 0]), np.array([41, 29, 0])]
        dots = [Dot(positions[i] + offset, radius = 0.05, color = BLUE if i%2 else GREEN) for i in range(5)]
        self.play(FadeIn(labels), 
                  LaggedStart(*[ShowCreation(dot) for dot in dots], lag_ratio = 0.5, run_time = 3.5), 
                  LaggedStart(*[values[i].animating(path_arc = -6*DEGREES*i**2).next_to(dots[i]) for i in range(5)], lag_ratio = 0.5, run_time = 3.5), 
                  hyperbolas[3].animating(run_time = 3, rate_func = squish_rate_func(smooth, 2/3, 1)).fade(),
                  hyperbolas[4].animating(run_time = 3.5, rate_func = squish_rate_func(smooth, 5/7, 1)).fade())
        self.wait(2+0-3, 29+26-15) #我们就可以把这些截断值在平面上标出来 （空闲）

        coordinate = [MTex(r"(1, 1)", color = GREEN).scale(0.6).next_to(dots[0], UL, buff = 0.1), MTex(r"(3, 2)", color = BLUE).scale(0.6).next_to(dots[1], DR, buff = 0.1), MTex(r"(7, 5)", color = GREEN).scale(0.6).next_to(dots[2], UL, buff = 0.1)]
        self.remove(values[3], values[4],dots[3], dots[4]).play(Flash(dots[1]), Uncreate(values[1]), Write(coordinate[1]))
        self.wait(1, 26) #蓝色的点 就是减出来为1的那一类
        self.wait(0, 17) #（空闲）
        self.play(Flash(dots[0]), Uncreate(values[0]), Flash(dots[2]), Uncreate(values[2]), Write(coordinate[0]), Write(coordinate[2]))
        self.wait(2, 5) #而绿色的点 就是减出来为-1的那一类
        self.wait(0, 21) #（空闲）

        self.wait(2, 19) #虽然分子和分母变大得很快
        self.wait(2, 12) #屏幕上其实放不下几个点
        self.wait(2, 21) #但我们还是可以大概看一看它们的位置
        self.wait(0, 21) #（空闲）

        hyperbola_p = ParametricCurve(lambda t: np.array([np.cosh(t), np.sinh(t)/np.sqrt(2), 0]), [np.arcsinh(-0.5), np.arccosh(7.5), 0.01], color = BLUE, stroke_width = 3).shift(offset)
        hyperbola_m = ParametricCurve(lambda t: np.array([np.sinh(t), np.cosh(t)/np.sqrt(2), 0]), [np.arcsinh(-0.5), np.arcsinh(7.5), 0.01], color = GREEN, stroke_width = 3).shift(offset)
        function_p = MTex(r"m^2-{2}n^2=1", tex_to_color_map = {(r"m", r"n", r"1"): BLUE, r"{2}": TEAL}).scale(0.8).next_to(3*UP + 3*np.sqrt(2)*RIGHT + offset, DR).shift(0.1*LEFT)
        function_m = MTex(r"m^2-{2}n^2=-1", tex_to_color_map = {(r"m", r"n", r"-1"): GREEN, r"{2}": TEAL}).scale(0.8).next_to(3*UP + 3*np.sqrt(2)*RIGHT + offset, UL)
        self.play(Write(function_p), Write(function_m), self.change_notice())
        self.wait(2, 14) #m的平方减去二倍n的平方为±1
        self.add(hyperbola_p, hyperbola_m, *dots[0:3]).play(ShowCreation(hyperbola_p), ShowCreation(hyperbola_m))
        self.wait(1, 22) #这个关系在平面上画出了两条双曲线
        self.wait(0, 20) #（空闲）

        self.wait(1, 18) #这些点都在双曲线上
        self.wait(0, 21) #（空闲）
        self.wait(1, 14) #更准确来说
        lines_h = VGroup(*[Line(0.2*LEFT + i*UP, 7.2*RIGHT + i*UP) for i in range(6)]).set_stroke(width = 1, color = RED_A).shift(offset)
        lines_v = VGroup(*[Line(0.2*DOWN + i*RIGHT, 5.2*UP + i*RIGHT) for i in range(8)]).set_stroke(width = 1, color = RED_A).shift(offset)
        self.bring_to_back(lines_h, lines_v).play(Write(lines_h), Write(lines_v), run_time = 2)
        self.wait(1, 23) #它们是双曲线上 横纵坐标都为正整数的点
        self.wait(0, 25) #（空闲）

        asymptote = Line(-0.5*np.array([1, 1/np.sqrt(2), 0]), 7.5*np.array([1, 1/np.sqrt(2), 0]), color = TEAL, stroke_width = 3).shift(offset)
        function_a = MTex(r"m=\sqrt{2}n", tex_to_color_map = {(r"m", r"n", r"\sqrt{2}"): TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).next_to(7.5*np.array([1, 1/np.sqrt(2), 0]) + offset, UR)
        self.add(asymptote, *dots[0:3]).play(ShowCreation(asymptote))
        self.play(Write(function_a))
        self.wait(1, 26) #这两条双曲线有公共的渐近线：m=√2n
        self.wait(0, 20) #（空闲）

        dot_move = Dot(positions[0] + offset, color = YELLOW)
        self.play(GrowFromCenter(dot_move))
        self.play(dot_move.animate.move_to(positions[1] + offset))
        self.play(dot_move.animate.move_to(positions[2] + offset))
        self.play(dot_move.animate.move_to(positions[3] + offset))
        self.remove(dot_move).wait(1+2+0-4, 24+3+23) #越是沿着双曲线走 上面的点离渐近线就越近 （空闲）

        dot_move = Dot(positions[0] + offset, color = YELLOW)
        line_move = Line(positions[0] + offset, positions[0] + offset, color = GREEN)
        origin = Dot(offset, color = YELLOW)
        lines = [Line(position + offset, offset, color = YELLOW, stroke_width = 2) for position in positions]
        slopes = [MTex(r"k=\frac{1}{1}", color = YELLOW).scale(0.6).next_to(coordinate[0], UP), MTex(r"k=\frac{2}{3}", color = YELLOW).scale(0.6).next_to(coordinate[1], DOWN), MTex(r"k=\frac{5}{7}", color = YELLOW).scale(0.6).next_to(coordinate[2], UP)]
        self.play(TransformFromCopy(dots[0], dot_move), line_move.animate.set_color(YELLOW).put_start_and_end_on(positions[0] + offset, + offset), ShowCreation(origin))
        self.bring_to_back(lines_h, lines_v, lines[0]).play(dot_move.animate.move_to(positions[1] + offset), line_move.animate.put_start_and_end_on(positions[1] + offset, + offset))
        self.bring_to_back(lines_h, lines_v, lines[1]).play(dot_move.animate.move_to(positions[2] + offset), line_move.animate.put_start_and_end_on(positions[2] + offset, + offset))
        self.bring_to_back(lines_h, lines_v, lines[2]).add(line_move, function_a).play(dot_move.animate.move_to(positions[3] + offset), line_move.animate.put_start_and_end_on(positions[3] + offset, + offset).set_opacity(0.5))
        self.remove(dot_move).play(line_move.animate.put_start_and_end_on(positions[4] + offset, + offset).set_opacity(0), 
                                   LaggedStart(*[Write(mob) for mob in slopes], run_time = 2, rate_func = squish_rate_func(smooth, 0.25, 1)))
        self.remove(line_move).wait(3+4-6, 2+6) #如果我们连接原点和双曲线上的点 它们离得越远 这条线的斜率就会越接近√2/2
        self.wait(0, 27) #（空闲）

        self.wait(2, 16) #对于两条双曲线上的整点来说
        self.wait(3, 2) #斜率就是它们所对应的截断值的倒数
        self.wait(0, 21) #（空闲）
        copies = [line.copy().set_stroke(width = 6).reverse_points() for line in lines[0:3]]
        self.add(*copies, *dots[0:3]).play(LaggedStart(*[ShowPassingFlashAround(mob) for mob in slopes], run_time = 4, lag_ratio = 0.5), LaggedStart(*[ShowPassingFlash(copies[i], run_time = i/2+1) for i in range(3)], group = VGroup(), run_time = 4, lag_ratio = 0.5))
        self.wait(2+2-4, 17+1) #随着斜率趋近于√2/2 截断值就会趋近于√2
        self.wait(0, 23) #（空闲）

        self.play(self.change_notice())
        self.wait(0, 21) #这看起来挺好的
        self.wait(1, 21) #但唯一的问题是
        self.play(*[WiggleOutThenIn(mob) for mob in coordinate])
        self.wait(0, 18) #为什么所有的点都在这两条双曲线上呢
        self.wait(0, 23) #（空闲）

        self.fade_out(run_time = 0.5)
        color_map = {r"{1}": GREEN, r"{2}": TEAL, r"\sqrt{2}": TEAL}
        mtex = MTex(r"\sqrt{2}={1}+\cfrac1{2+\cfrac1{2+\cfrac1{2+\cfrac1{\cdots}}}}", tex_to_color_map = color_map).shift(2*UP).scale(2/3, about_point = 4*UP)
        convergents = [MTex(r"1", color = GREEN).scale(0.8)] + [MTex(r"{1}" + i*r"+\cfrac1{2" + r"+\cfrac1{2}" + i*r"}", tex_to_color_map = color_map).scale(0.8) for i in range(4)]
        for i in range(5):
            convergents[i].shift((i-6+0.35*i*i)*RIGHT + 0.5*UP - convergents[i][0].get_center())
        self.play(FadeIn(mtex), FadeIn(convergents[4]), run_time = 0.5)
        for i in range(4, 0, -1):
            self.play(TransformFromCopy(convergents[i][:-4], convergents[i-1]), run_time = 0.7, frames = 21)
        self.wait(1+2-3, 21+12-24) #这就需要回过头来 看看在通分的时候发生了什么了
        self.wait(0, 20) #（空闲）

        texts = [r"{1}+\cfrac1{{2}+\cfrac1{2}}", r"=1+\frac2{5}=\frac{7}{5}"]
        mtex_3 = MTex(r"".join(texts), isolate = texts + [r"\frac2{5}", r"\cfrac1{{2}+\cfrac1{2}}", r"="], tex_to_color_map = color_map).scale(0.8).next_to(5*LEFT)
        mtex_3.set_y(2 - mtex_3.get_part_by_tex(r"=").get_y())
        parts_3 = [mtex_3.get_part_by_tex(text) for text in texts] + [mtex_3.get_part_by_tex(r"\frac2{5}"), mtex_3.get_part_by_tex(r"\cfrac1{{2}+\cfrac1{2}}")]
        texts = [r"{1}+\cfrac1{{2}+\cfrac1{{2}+\cfrac1{2}}}", r"=1+\cfrac1{2+\cfrac2{5}}=1+\frac{5}{12}=\frac{17}{12}"]
        mtex_4 = MTex(r"".join(texts), isolate = texts + [r"\cfrac2{5}", r"\cfrac1{{2}+\cfrac1{2}}", r"="], tex_to_color_map = color_map).scale(0.8).next_to(5*LEFT)
        mtex_4.set_y(-0.5 - mtex_4.get_part_by_tex(r"=").get_y())
        parts_4 = [mtex_4.get_part_by_tex(text) for text in texts] + [mtex_4.get_part_by_tex(r"\cfrac2{5}"), mtex_4.get_part_by_tex(r"\cfrac1{{2}+\cfrac1{2}}")]
        value_3 = MTex(r"\frac{7}{5}", color = GREEN).scale(0.8).shift(6*LEFT + 2*UP)
        value_4 = MTex(r"\frac{17}{12}", color = BLUE).scale(0.8).shift(6*LEFT + 0.5*DOWN)

        self.play(*[FadeOut(mob) for mob in [mtex, convergents[0], convergents[1], convergents[4]]], ShowPassingFlashAround(convergents[2]), ShowPassingFlashAround(convergents[3]), self.change_notice())
        self.wait(0, 27) #截断值的第三项和第四项......
        self.play(Write(value_3), ReplacementTransform(convergents[2], parts_3[0]))
        self.wait(0, 9) #......分别是7/5......
        self.play(Write(value_4), ReplacementTransform(convergents[3], parts_4[0]))
        self.wait(0, 29) #......和17/12
        self.play(FadeIn(parts_3[1], 0.5*LEFT), FadeIn(parts_4[1], 0.5*LEFT, run_time = 1.5, rate_func = squish_rate_func(smooth, 1/3, 1)))
        self.wait(0, 21) #它们的计算过程分别是这样的
        self.wait(0, 27) #（空闲）

        self.play(*[mob.save_state().animate.scale(1.1).set_color(YELLOW) for mob in parts_3[2:] + parts_4[2:]])
        self.wait(2, 25) #很明显 它们的运算第一步是一模一样的
        self.play(ShowPassingFlashAround(parts_3[2]), ShowPassingFlashAround(parts_4[2]), run_time = 2)
        self.wait(1+2-3, 29+19) 
        self.play(*[mob.animate.restore() for mob in parts_3[2:] + parts_4[2:]]) #结果都是2/5 算出一个来 另一个就不用算了
        self.wait(0, 23) #（空闲）

        indicates = parts_3[1][1] + parts_4[1][5]
        self.play(*[mob.save_state().animate.scale(1.1).set_color(YELLOW) for mob in indicates])
        self.wait(0, 11) #计算的第二步
        self.wait(3, 9) #它们一个加1 一个加2 才会产生差别
        self.wait(0, 22) #（空闲）

        self.play(*[mob.animate.restore() for mob in indicates])
        self.wait(2, 12) #但我们仍然可以利用一下7/5的运算结果

        texts = [r"=1+\cfrac1{2+\cfrac2{5}}", r"=1+\frac{5}{12}=\frac{17}{12}"]
        replace = MTex(r"".join(texts), isolate = texts, tex_to_color_map = color_map).scale(0.8).next_to(5*LEFT)
        parts_replace = [replace.get_part_by_tex(text) for text in texts]
        replace.shift(parts_4[1][0].get_center() - replace[0].get_center())
        texts = [r"=1+\cfrac1{1+1+\cfrac2{5}}", r"=1+\frac{1}{1+\cfrac7{5}}=\frac{17}{12}"]
        expand = MTex(r"".join(texts), isolate = texts + [r"1+\cfrac2{5}", r"\cfrac7{5}"]).scale(0.8)
        parts_expand = [expand.get_part_by_tex(text) for text in texts] + [expand.get_part_by_tex(r"1+\cfrac2{5}"), expand.get_part_by_tex(r"\cfrac7{5}")]
        expand.shift(parts_4[1][0].get_center() - expand[0].get_center())
        self.add(replace).remove(parts_4[1]).play(
            ReplacementTransform(parts_replace[0][0:5], parts_expand[0][0:5]), ReplacementTransform(parts_replace[0][5], parts_expand[0][5:8]), 
            ReplacementTransform(parts_replace[0][6:], parts_expand[0][8:]), FadeOut(parts_replace[1], 0.5*RIGHT))
        self.wait(0, 18) #只需要把2拆开
        self.play(FadeIn(parts_expand[1], 0.5*LEFT))
        self.play(*[mob.save_state().animate.scale(1.1).set_color(YELLOW) for mob in parts_expand[2:]])
        self.wait(1, 10) #先加一个1 再加另一个1 就可以了
        self.wait(1, 5) #（空闲）

        self.fade_out()
        value_4 = MTex(r"\frac{17}{12}", color = BLUE).scale(0.8).shift(6*LEFT + 2.5*UP)
        value_5 = MTex(r"\frac{41}{29}", color = GREEN).scale(0.8).shift(6*LEFT + 0.5*DOWN)
        texts = [r"{1}+\cfrac1{{2}+\cfrac1{{2}+\cfrac1{2}}}=\cdots=1+\cfrac5{12}=\frac{17}{12}"]
        mtex_4 = MTex(*texts, isolate = [r"\cfrac5{12}", r"\cfrac1{{2}+\cfrac1{{2}+\cfrac1{2}}}", r"="], tex_to_color_map = color_map).scale(0.8).next_to(5*LEFT)
        parts_4 = [mtex_4.get_part_by_tex(r"\cfrac5{12}"), mtex_4.get_part_by_tex(r"\cfrac1{{2}+\cfrac1{{2}+\cfrac1{2}}}")]
        mtex_4.set_y(2.5 - mtex_4.get_part_by_tex(r"=").get_y())
        texts = [r"{1}+\cfrac1{{2}+\cfrac1{{2}+\cfrac1{{2}+\cfrac1{2}}}}=\cdots", r"=1+\cfrac1{2+\cfrac5{12}}", r"=1+\frac{12}{29}=\frac{41}{29}"]
        mtex_5 = MTex(r"".join(texts), isolate = texts + [r"\cfrac5{12}", r"\cfrac1{{2}+\cfrac1{{2}+\cfrac1{2}}}", r"="], tex_to_color_map = color_map).scale(0.8).next_to(5*LEFT)
        mtex_5.set_y(-0.5 - mtex_5.get_part_by_tex(r"=").get_y())
        parts_5 = [mtex_5.get_part_by_tex(text) for text in texts] + [mtex_5.get_part_by_tex(r"\cfrac5{12}"), mtex_5.get_part_by_tex(r"\cfrac1{{2}+\cfrac1{{2}+\cfrac1{2}}}")]
        self.fade_in(value_4, value_5, mtex_4, mtex_5)
        self.wait(0, 9) #其它相邻两项也都一样
        self.play(*[mob.save_state().animate.scale(1.05).set_color(YELLOW) for mob in parts_4 + parts_5[3:]])
        self.wait(2, 11) #算到最后两步之前 所有结果都可以通用
        self.wait(0, 17) #（空闲）
        
        self.play(*[mob.animate.restore() for mob in parts_4 + parts_5[3:]], FadeOut(parts_5[2], 0.5*RIGHT))
        self.wait(0, 25) #后面那项的倒数第二步
        texts = [r"=1+\cfrac1{1+1+\cfrac5{12}}", r"=1+\frac1{1+\cfrac{17}{12}}=\frac{41}{29}"]
        replace = MTex(r"".join(texts), isolate = texts, tex_to_color_map = color_map).scale(0.8).next_to(5*LEFT)
        parts_replace = [replace.get_part_by_tex(text) for text in texts]
        replace.shift(parts_5[1][0].get_center() - replace[0].get_center())
        self.play(ReplacementTransform(parts_5[1][0:5], parts_replace[0][0:5]), ReplacementTransform(parts_5[1][5], parts_replace[0][5:8]), 
                ReplacementTransform(parts_5[1][6:], parts_replace[0][8:]))
        self.wait(1, 1) #把2拆成1+1
        self.play(FadeIn(parts_replace[1], 0.5*LEFT))
        self.wait(1, 2) #就可以利用前面那项的结果
        self.wait(0, 20) #（空闲）

        self.fade_out(excepts = [value_4, value_5])
        terms = [MTex(r"\frac{m_" + str(i+1) + r"}{n_" + str(i+1) + r"}", color = BLUE if i%2 else GREEN).scale(0.8).shift(0.5*DOWN + (i-2.5)*2*RIGHT) for i in range(6)]
        texts = [r"\frac{1}{1}", r"\frac{3}{2}", r"\frac{7}{5}", r"\frac{17}{12}", r"\frac{41}{29}", r"\frac{99}{70}"]
        values = [MTex(texts[i], color = BLUE if i%2 else GREEN).scale(0.8).shift(2*DOWN + (i-2.5)*2*RIGHT) for i in range(6)]
        self.play(Transform(value_4, values[3]), Transform(value_5, values[4]))
        self.play(LaggedStart(*[FadeIn(mob) for mob in terms], lag_ratio = 0.3), LaggedStart(*[FadeIn(mob) for mob in values], lag_ratio = 0.3), run_time = 1)
        self.remove(value_4, value_5).wait(0, 3) #也就是说 相邻的两个截断值
        texts = r"\frac{m_{k+1}}{n_{k+1}}=1+\frac1{1+\cfrac{m_k}{n_k}}", r"=\frac{m_k+2n_k}{m_k+n_k}"
        formula = MTex(texts[0]+texts[1], isolate = texts, tex_to_color_map = {(r"m_{k+1}", r"n_{k+1}", r"m_k", r"n_k", r"2"): TEAL}).scale(0.8).shift(2*UP)
        parts = [formula.get_part_by_tex(text) for text in texts]
        offset_0 = parts[0].get_x()
        offset_1 = parts[1].get_x(RIGHT) - (parts[0].get_x(RIGHT) - offset_0)
        parts[0].shift(-offset_0*RIGHT)
        parts[1].shift(-offset_1*RIGHT)
        shade = BackgroundRectangle(parts[1], buff = 0.1, color = BACK, fill_opacity = 1)
        self.add(parts[1], shade, parts[0]).play(Write(parts[0]), run_time = 1)
        self.wait(1) #有这么一个递推关系
        self.play(parts[0].animate.shift(offset_0*RIGHT), parts[1].animate.shift(offset_1*RIGHT), shade.animate.shift(offset_0*RIGHT))
        self.remove(shade).wait(0, 9) #它可以化简成这样
        self.wait(0, 24) #（空闲）

        gcd = MTex(r"\gcd(m_{k+1}, n_{k+1})=\gcd(m_k+2n_k, m_k+n_k)=\gcd(m_k, n_k)=1", tex_to_color_map = {(r"m_{k+1}", r"n_{k+1}", r"m_k", r"n_k"): TEAL}).scale(0.8).scale(0.8).shift(UP)
        self.play(formula.animate.shift(0.5*UP), FadeIn(gcd, 0.25*UP), self.change_notice())
        self.wait(2, 8) #并且 只要前一项是最简分数
        self.wait(1, 25) #后一项就也不用约分
        self.wait(0, 26) #（空闲）

        formula_short = MTex(r"\frac{m_{k+1}}{n_{k+1}}=\frac{m_k+2n_k}{m_k+n_k}", isolate = [r"="], tex_to_color_map = {(r"m_{k+1}", r"n_{k+1}", r"m_k", r"n_k", r"2"): TEAL}).scale(0.8).shift(UP + 4*RIGHT)
        position = formula_short.get_part_by_tex(r"=").get_center()
        self.play(*[FadeOut(mob) for mob in values + terms + [gcd]], self.change_notice(),
                  ReplacementTransform(parts[0][0:9], formula_short[0:9]), ReplacementTransform(parts[1], formula_short[9:]), 
                  Transform(parts[0][9], formula_short[9], remover = True), parts[0][10:].animating(remover = True).scale(0, about_point = position))
        offset = 6*LEFT + 2.5*DOWN
        axes_below = VGroup(Line(7.5*LEFT, 2*RIGHT), Line(5.5*DOWN, 2*UP)).shift(offset)
        axes_above = VGroup(Arrow(1.5*RIGHT, 7.5*RIGHT), Arrow(1.5*UP, 5.5*UP)).shift(offset)
        labels = VGroup(MTex(r"m").scale(0.75).next_to(axes[0], RIGHT), MTex(r"n").scale(0.75).next_to(axes[1], UP))
        positions = [np.array([1, 1, 0]), np.array([3, 2, 0]), np.array([7, 5, 0])]
        dots = [Dot(positions[i] + offset, radius = 0.05, color = BLUE if i%2 else GREEN) for i in range(3)]
        coordinate = [MTex(r"(1, 1)", color = GREEN).scale(0.6).next_to(dots[0], UL, buff = 0.1), MTex(r"(3, 2)", color = BLUE).scale(0.6).next_to(dots[1], DR, buff = 0.1), MTex(r"(7, 5)", color = GREEN).scale(0.6).next_to(dots[2], UL, buff = 0.1)]
        hyperbola_p = ParametricCurve(lambda t: np.array([np.cosh(t), np.sinh(t)/np.sqrt(2), 0]), [np.arcsinh(-2), np.arccosh(7.5), 0.01], color = BLUE, stroke_width = 3).shift(offset)
        hyperbola_m = ParametricCurve(lambda t: np.array([np.sinh(t), np.cosh(t)/np.sqrt(2), 0]), [np.arcsinh(-2), np.arcsinh(7.5), 0.01], color = GREEN, stroke_width = 3).shift(offset)
        function_p = MTex(r"m^2-{2}n^2=1", tex_to_color_map = {(r"m", r"n", r"1"): BLUE, r"{2}": TEAL}).scale(0.8).next_to(7.5*np.array([1, 1/np.sqrt(2), 0]) + offset, DR).shift(0.1*LEFT)
        function_m = MTex(r"m^2-{2}n^2=-1", tex_to_color_map = {(r"m", r"n", r"-1"): GREEN, r"{2}": TEAL}).scale(0.8).next_to(7.5*np.array([1, 1/np.sqrt(2), 0]) + offset, UL)
        asymptote = Line(-0.5*np.array([1, 1/np.sqrt(2), 0]), 7.5*np.array([1, 1/np.sqrt(2), 0]), color = TEAL, stroke_width = 3).shift(offset)
        function_a = MTex(r"m=\sqrt{2}n", tex_to_color_map = {(r"m", r"n", r"\sqrt{2}"): TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).next_to(7.5*np.array([1, 1/np.sqrt(2), 0]) + offset, UR)
        lines_h = VGroup(*[Line(8*LEFT + i*UP, 16*RIGHT + i*UP) for i in range(-6, 12)]).set_stroke(width = 2, color = RED_A).shift(offset)
        lines_v = VGroup(*[Line(6*DOWN + i*RIGHT, 12*UP + i*RIGHT) for i in range(-8, 16)]).set_stroke(width = 2, color = RED_A).shift(offset)
        shade = VGroup(self.shade.copy().next_to((7+offset[0])*RIGHT, RIGHT), self.shade.copy().next_to(offset[0]*RIGHT, LEFT), self.shade.copy().next_to((5+offset[1])*UP, UP), self.shade.copy().next_to(offset[1]*UP, DOWN))
        self.fade_in(lines_h, lines_v, axes_below, hyperbola_p, hyperbola_m, asymptote, *dots, shade, axes_above, labels, function_p, function_m, function_a, excepts = [formula_short])
        self.wait(0, 8) #让我们回到平面上

        linear = MTex(r"\binom{m}{n}\to\binom{m+2n}{m+n}", tex_to_color_map = {(r"m", r"n", r"2"): TEAL}).scale(0.8).next_to(formula_short, DOWN, buff = 0.5)
        self.play(FadeIn(linear, 0.5*DOWN))
        self.wait(2, 7) #这个递推式确立了平面上的点的一个变换
        arrows = [Arrow(positions[0] + offset, positions[1] + offset, color = YELLOW), Arrow(positions[1] + offset, positions[2] + offset, color = YELLOW), Arrow(positions[2] + offset, np.array([17, 12, 0]) + offset, color = YELLOW, stroke_width = 4)]
        self.play(Grow(arrows[0]))
        self.play(Grow(arrows[1]))
        self.add(arrows[2], function_a).play(Grow(arrows[2]))
        self.wait(0, 10) #让所有截断值对应的点跑到了下一个点的位置上
        self.wait(0, 22) #（空闲）

        surrounding = SurroundingRectangle(linear)
        self.play(*[FadeOut(mob) for mob in arrows], ShowCreation(surrounding))
        self.wait(1, 13) #这个变换并不要求点是整点
        self.wait(2, 12) #也不要求点在双曲线上
        self.wait(2, 0) #而是整个平面都可以作用
        self.wait(0, 19) #（空闲）

        background = VGroup(lines_h.copy(), lines_v.copy(), hyperbola_p.copy(), hyperbola_m.copy()).set_stroke(width = 1, color = GREY).add(*[dot.copy().set_color(GREY) for dot in dots])
        trans = lambda t: np.array([t[0]+2*t[1], t[0]+t[1], 0])
        self.bring_to_back(background).play(lines_h.animating(run_time = 3).apply_function(trans, about_point = offset), lines_v.animating(run_time = 3).apply_function(trans, about_point = offset), 
                                            hyperbola_p.animating(run_time = 3).apply_function(trans, about_point = offset).set_color(GREEN), hyperbola_m.animating(run_time = 3).apply_function(trans, about_point = offset).set_color(BLUE), 
                                            dots[0].save_state().animating(run_time = 3).move_to(positions[1] + offset).set_color(BLUE), dots[1].save_state().animating(run_time = 3).move_to(positions[2] + offset).set_color(GREEN), dots[2].save_state().animating(run_time = 3).move_to(np.array([17, 12, 0]) + offset).set_color(GREEN), 
                                            FadeOut(surrounding))
        self.wait(2+1-3, 21) #这个变换 长这个样子 （空闲）

        self.play(self.change_notice())
        self.wait(1, 4) #两条双曲线互换了位置
        self.add(*arrows, function_a).play(LaggedStart(*[Grow(mob) for mob in arrows], group = VGroup(), run_time = 2, lag_ratio = 0.5))
        self.wait(1+0-2, 28+18) #所有的点都向后挪了一位 （空闲）
        point = Dot(positions[0] + offset, color = YELLOW)
        self.play(Flash(positions[0] + offset), TransformFromCopy(background[4], point))
        self.wait(2, 29) #既然我们的起始点(1, 1)在一条双曲线上
        self.play(Flash(positions[1] + offset), Flash(positions[2] + offset))
        self.wait(1, 13) #所有点就都在这两条双曲线上
        self.wait(0, 28) #（空闲）

        self.play(*[FadeOut(mob) for mob in arrows + [lines_h, lines_v, formula_short]], point.animate.scale(5/8).set_color(GREEN), background.set_submobjects(background.submobjects[0:2].copy()).animate.set_stroke(width = 2, color = RED_A))
        self.wait(2, 8) #至此 关于√2的连分数的秘密
        self.wait(1, 22) #我们已经探索得差不多了
        self.wait(0, 21) #（空闲）

        lines_h = VGroup(*[Line(8*LEFT + i*UP, 20*RIGHT + i*UP) for i in range(-6, 16)]).set_stroke(width = 2, color = RED_A).shift(offset)
        lines_v = VGroup(*[Line(6*DOWN + i*RIGHT, 16*UP + i*RIGHT) for i in range(-8, 20)]).set_stroke(width = 2, color = RED_A).shift(offset)
        self.remove(background).bring_to_back(lines_h, lines_v).play(self.change_notice())
        background = VGroup(lines_h.copy(), lines_v.copy(), hyperbola_p.copy(), hyperbola_m.copy()).set_stroke(width = 1, color = GREY).add(*[dot.copy().set_color(GREY) for dot in dots])
        self.wait(0, 22) #但这两条双曲线上面
        self.wait(1, 25) #还有另一些有趣的东西
        self.wait(0, 19) #（空闲）

        inverse = MTex(r"\binom{-m+2n}{m-n}\gets\binom{m}{n}", tex_to_color_map = {(r"m", r"n", r"2"): TEAL}).scale(0.8).next_to(linear, DOWN, buff = 0.5).shift(UP)
        self.play(FadeIn(inverse, 0.5*DOWN), linear.animate.shift(UP))
        trans = lambda t: np.array([-t[0]+2*t[1], t[0]-t[1], 0])
        self.bring_to_back(background).play(lines_h.animate.apply_function(trans, about_point = offset), lines_v.animate.apply_function(trans, about_point = offset), 
                                            hyperbola_p.animate.apply_function(trans, about_point = offset).set_color(BLUE), hyperbola_m.animate.apply_function(trans, about_point = offset).set_color(GREEN), 
                                            point.animate.move_to(RIGHT + offset).set_color(BLUE), dots[0].animate.restore(), dots[1].animate.restore(), dots[2].animate.restore(), 
                                            run_time = 4)
        self.wait(3+2-5, 6+6) #比如说 之前那个变换的逆变换 同样会把整数点变到整数点
        self.wait(0, 20) #（空闲）
        
        arrows = [Arrow(positions[0] + offset, RIGHT + offset, color = YELLOW), Arrow(positions[1] + offset, positions[0] + offset, color = YELLOW), Arrow(positions[2] + offset, positions[1] + offset, color = YELLOW, stroke_width = 4)]
        self.play(Flash(positions[1] + offset), Flash(positions[2] + offset))
        self.wait(0, 15) #对于其它的点
        self.play(LaggedStart(*[Grow(mob) for mob in [arrows[2], arrows[1]]], run_time = 1.5, lag_ratio = 0.5))
        self.wait(1, 12) #逆变换会把它们往回挪一位
        self.play(Flash(positions[0] + offset))
        self.wait(1, 14) #而对于(1, 1)这个起始点
        self.play(Grow(arrows[0]))
        self.wait(1, 16) #逆变换会把它变到(1, 0)的位置
        self.wait(0, 28) #（空闲）
        
        self.play(*[FadeOut(mob) for mob in arrows + [lines_h, lines_v, function_p, function_m, function_a, asymptote, linear, inverse]], background.set_submobjects(background.submobjects[0:2].copy()).animate.set_stroke(width = 2, color = RED_A))
        self.wait(1, 6) #这看起来还挺合理的
        self.play(Flash(RIGHT+offset))
        self.wait(1, 19) #(1, 0)毫无疑问是双曲线上的整点
        self.wait(0, 19) #（空闲）

        hyperbola_p.set_points(ParametricCurve(lambda t: np.array([np.cosh(t), np.sinh(t)/np.sqrt(2), 0]), [np.arcsinh(-10), np.arcsinh(10), 0.01]).shift(offset).get_points()).add(ParametricCurve(lambda t: -np.array([np.cosh(t), np.sinh(t)/np.sqrt(2), 0]), [np.arcsinh(-10), np.arcsinh(10), 0.01], color = BLUE, stroke_width = 3).shift(offset))
        hyperbola_m.set_points(ParametricCurve(lambda t: np.array([np.sinh(t), np.cosh(t)/np.sqrt(2), 0]), [np.arcsinh(-10), np.arcsinh(10), 0.01]).shift(offset).get_points()).add(ParametricCurve(lambda t: -np.array([np.sinh(t), np.cosh(t)/np.sqrt(2), 0]), [np.arcsinh(-10), np.arcsinh(10), 0.01], color = GREEN, stroke_width = 3).shift(offset))
        lines_h = VGroup(*[Line(16*LEFT + i*UP, 16*RIGHT + i*UP) for i in range(-12, 12)]).set_stroke(width = 2, color = RED_A).shift(offset)
        lines_v = VGroup(*[Line(12*DOWN + i*RIGHT, 12*UP + i*RIGHT) for i in range(-16, 16)]).set_stroke(width = 2, color = RED_A).shift(offset)
        positions_p = [np.array([3, -2, 0]), np.array([1, 0, 0]), np.array([3, 2, 0]), np.array([-3, -2, 0]), np.array([-1, 0, 0]), np.array([-3, 2, 0])]
        positions_m = [np.array([-7, 5, 0]), np.array([-1, 1, 0]), np.array([1, 1, 0]), np.array([7, 5, 0]), np.array([-7, -5, 0]), np.array([-1, -1, 0]), np.array([1, -1, 0]), np.array([7, -5, 0])]
        dots_p = [Dot(position+offset, color = BLUE, radius = 0.05) for position in positions_p]
        dots_m = [Dot(position+offset, color = GREEN, radius = 0.05) for position in positions_m]
        self.remove(point, *dots, background).bring_to_back(lines_h, lines_v).add(*dots_p, *dots_m, *shade, *labels, self.notice).play(*[mob.animate.shift(-offset).scale(1.05, about_point = ORIGIN) for mob in [axes_below, axes_above]], labels[0].animate.next_to(RIGHT_SIDE, UL, buff = 0.1), labels[1].animate.next_to(TOP, DL, buff = 0.1), 
                                                    shade[0].animate.next_to(RIGHT_SIDE, RIGHT, buff = 0), shade[1].animate.next_to(LEFT_SIDE, LEFT, buff = 0), shade[2].animate.next_to(TOP, UP, buff = 0), shade[3].animate.next_to(BOTTOM, DOWN, buff = 0),
                                                    *[dots_p[i].animate.move_to(2/3*positions_p[i]).scale(1.6) for i in range(6)], *[dots_m[i].animate.move_to(2/3*positions_m[i]).scale(1.6) for i in range(8)], 
                                                    *[mob.animate.shift(-offset).scale(2/3, about_point = ORIGIN) for mob in [hyperbola_p, hyperbola_m, lines_h, lines_v]], run_time = 2)
        self.wait(1, 8) #并且 如果我们把双曲线画全
        anims_1 = AnimationGroup(Flash(positions_m[0]*2/3), Flash(positions_m[3]*2/3), Flash(positions_m[4]*2/3), Flash(positions_m[7]*2/3))
        anims_2 = AnimationGroup(Flash(positions_p[0]*2/3), Flash(positions_p[2]*2/3), Flash(positions_p[3]*2/3), Flash(positions_p[5]*2/3))
        anims_3 = AnimationGroup(Flash(positions_m[1]*2/3), Flash(positions_m[2]*2/3), Flash(positions_m[5]*2/3), Flash(positions_m[6]*2/3))
        anims_4 = AnimationGroup(Flash(positions_p[1]*2/3), Flash(positions_p[4]*2/3))
        self.play(LaggedStart(anims_1, anims_2, anims_3, anims_4, run_time = 2, lag_ratio = 0.5))
        self.wait(1+1-2, 27+16) #那么在对称的位置上 会一共有四组整点
        self.wait(0, 22) #（空闲）

        self.wait(2, 16) #于是就有了一个很自然的问题
        self.wait(3, 1) #我们把这两条双曲线上的整点找全了吗
        self.wait(2, 27)
        self.fade_out(end = True)
        self.wait(2, 0) #到此共231秒

#################################################################### 

class Chapter2_0(FrameScene):

    def construct(self):

        text2 = MTexText("第二节 双曲线上的整点", tex_to_color_map={"第二节": YELLOW, "双曲线": GREEN, "整点": BLUE})

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(FrameScene):
    def construct(self):
        self.notices = [Notice("观察可得", "请注意到"),
                        Notice("发现规律", "请　验证"),
                        Notice("探索规律", "请注意到"),
                        Notice("触类旁通", "请　模仿"),
                        Notice("留作习题", "自证不难"),
                        Notice("关键引理", "请　专注"),
                        Notice("这里是一个", "数学频道"), 
                        Notice("证明过程", "请　专注"),
                        Notice("证明完毕", "请　鼓掌")]
        self.notice = self.notices[0]

        lines_h = VGroup(*[Line(64/9*LEFT + i*2/3*UP, 64/9*RIGHT + i*2/3*UP) for i in range(-12, 12)]).set_stroke(width = 1, color = RED_A)
        lines_v = VGroup(*[Line(4*DOWN + i*2/3*RIGHT, 4*UP + i*2/3*RIGHT) for i in range(-16, 16)]).set_stroke(width = 1, color = RED_A)
        axes = VGroup(Line(4*DOWN, 4*UP), Line(64/9*LEFT, 64/9*RIGHT), MTex(r"x").scale(0.75).next_to(RIGHT_SIDE, UL, buff = 0.1), MTex(r"y").scale(0.75).next_to(TOP, DL, buff = 0.1))
        positions_p = [np.array([3, -2, 0])*2/3, np.array([1, 0, 0])*2/3, np.array([3, 2, 0])*2/3, np.array([-3, -2, 0])*2/3, np.array([-1, 0, 0])*2/3, np.array([-3, 2, 0])*2/3]
        positions_m = [np.array([-7, 5, 0])*2/3, np.array([-1, 1, 0])*2/3, np.array([1, 1, 0])*2/3, np.array([7, 5, 0])*2/3, np.array([-7, -5, 0])*2/3, np.array([-1, -1, 0])*2/3, np.array([1, -1, 0])*2/3, np.array([7, -5, 0])*2/3]
        dots_p = [Dot(position, color = BLUE) for position in positions_p]
        dots_m = [Dot(position, color = GREEN) for position in positions_m]
        hyperbola_p = VGroup(ParametricCurve(lambda t: 2/3*np.array([np.cosh(t), np.sinh(t)/np.sqrt(2), 0]), [np.arcsinh(-10), np.arcsinh(10), 0.01]), ParametricCurve(lambda t: -2/3*np.array([np.cosh(t), np.sinh(t)/np.sqrt(2), 0]), [np.arcsinh(-10), np.arcsinh(10), 0.01])).set_stroke(color = BLUE, width = 3)
        hyperbola_m = VGroup(ParametricCurve(lambda t: 2/3*np.array([np.sinh(t), np.cosh(t)/np.sqrt(2), 0]), [np.arcsinh(-10), np.arcsinh(10), 0.01]), ParametricCurve(lambda t: -2/3*np.array([np.sinh(t), np.cosh(t)/np.sqrt(2), 0]), [np.arcsinh(-10), np.arcsinh(10), 0.01])).set_stroke(color = GREEN, width = 3)
        function_p = MTex(r"x^2-{2}y^2=1", tex_to_color_map = {(r"x", r"y", r"1"): BLUE, r"{2}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).next_to(3*RIGHT, UP)
        function_m = MTex(r"x^2-{2}y^2=-1", tex_to_color_map = {(r"x", r"y", r"-1"): GREEN, r"{2}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).shift(1.5*UP)
        linear = MTex(r"\binom{x}{y}\to\binom{x+2y}{x+y}", tex_to_color_map = {(r"x", r"y", r"2"): YELLOW}).scale(0.8).set_stroke(width = 10, color = BACK, background = True).next_to(4*LEFT, UP)
        
        self.fade_in(lines_h, lines_v, axes, hyperbola_p, hyperbola_m, *dots_p, *dots_m, function_p, function_m)
        self.wait(1, 16) #不知道大家有没有一种感觉
        anims_1 = AnimationGroup(Flash(positions_m[0]), Flash(positions_m[3]), Flash(positions_m[4]), Flash(positions_m[7]))
        anims_2 = AnimationGroup(Flash(positions_p[0]), Flash(positions_p[2]), Flash(positions_p[3]), Flash(positions_p[5]))
        anims_3 = AnimationGroup(Flash(positions_m[1]), Flash(positions_m[2]), Flash(positions_m[5]), Flash(positions_m[6]))
        anims_4 = AnimationGroup(Flash(positions_p[1]), Flash(positions_p[4]))
        self.play(LaggedStart(anims_4, anims_3, anims_2, anims_1, run_time = 2, lag_ratio = 0.5))
        self.wait(0, 27) #这些整点在双曲线上分布得还挺均匀的
        self.wait(0, 21) #（空闲）
        self.wait(2, 10) #虽然它们的距离很不均匀
        self.play(Write(linear))
        self.wait(2, 18) #但当我们按连分数的迭代变换这些点的时候

        arrows_1 = [Arrow(positions_m[0], positions_p[0], color = YELLOW, stroke_width = 1), Arrow(positions_p[0], positions_m[1], color = YELLOW, stroke_width = 2), Arrow(positions_m[1], positions_p[1], color = YELLOW, stroke_width = 3), Arrow(positions_p[1], positions_m[2], color = YELLOW, buff = 0.1), Arrow(positions_m[2], positions_p[2], color = YELLOW, stroke_width = 3), Arrow(positions_p[2], positions_m[3], color = YELLOW, stroke_width = 2)]
        arrows_2 = [Arrow(positions_m[7], positions_p[5], color = YELLOW, stroke_width = 1), Arrow(positions_p[5], positions_m[6], color = YELLOW, stroke_width = 2), Arrow(positions_m[6], positions_p[4], color = YELLOW, stroke_width = 3), Arrow(positions_p[4], positions_m[5], color = YELLOW, buff = 0.1), Arrow(positions_m[5], positions_p[3], color = YELLOW, stroke_width = 3), Arrow(positions_p[3], positions_m[4], color = YELLOW, stroke_width = 2), ]
        self.play(LaggedStart(*[ShowCreation(mob) for mob in arrows_1], run_time = 2.5, lag_ratio = 0.3), LaggedStart(*[ShowCreation(mob) for mob in arrows_2], run_time = 2.5, lag_ratio = 0.3))
        self.wait(0, 1) #它们会依次移动到下一个点的位置上
        self.wait(0, 24) #（空闲）
        self.play(self.change_notice())
        self.wait(1, 23) #这种规律其实在别的双曲线上也成立
        self.wait(0, 17) #（空闲）

        self.fade_out()
        ratio = 1/2
        lines_h = VGroup(*[Line(64/9*LEFT + i*ratio*UP, 64/9*RIGHT + i*ratio*UP) for i in range(-12, 12)]).set_stroke(width = 1, color = RED_A)
        lines_v = VGroup(*[Line(4*DOWN + i*ratio*RIGHT, 4*UP + i*ratio*RIGHT) for i in range(-16, 16)]).set_stroke(width = 1, color = RED_A)
        axes = VGroup(Line(4*DOWN, 4*UP), Line(64/9*LEFT, 64/9*RIGHT), MTex(r"x").scale(0.75).next_to(RIGHT_SIDE, UL, buff = 0.1), MTex(r"y").scale(0.75).next_to(TOP, DL, buff = 0.1))
        positions_p = [np.array([9, -4, 0])*ratio, np.array([1, 0, 0])*ratio, np.array([9, 4, 0])*ratio, np.array([-9, -4, 0])*ratio, np.array([-1, 0, 0])*ratio, np.array([-9, 4, 0])*ratio]
        positions_m = [np.array([-2, 1, 0])*ratio, np.array([2, 1, 0])*ratio, np.array([-2, -1, 0])*ratio, np.array([2, -1, 0])*ratio]
        dots_p = [Dot(position, color = BLUE) for position in positions_p]
        dots_m = [Dot(position, color = GREEN) for position in positions_m]
        hyperbola_p = VGroup(ParametricCurve(lambda t: ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(5), 0]), [np.arcsinh(-15), np.arcsinh(15), 0.01]), ParametricCurve(lambda t: -ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(5), 0]), [np.arcsinh(-15), np.arcsinh(15), 0.01])).set_stroke(color = BLUE, width = 3)
        hyperbola_m = VGroup(ParametricCurve(lambda t: ratio*np.array([np.sinh(t), np.cosh(t)/np.sqrt(5), 0]), [np.arcsinh(-15), np.arcsinh(15), 0.01]), ParametricCurve(lambda t: -ratio*np.array([np.sinh(t), np.cosh(t)/np.sqrt(5), 0]), [np.arcsinh(-15), np.arcsinh(15), 0.01])).set_stroke(color = GREEN, width = 3)
        function_p = MTex(r"x^2-{5}y^2=1", tex_to_color_map = {(r"x", r"y", r"1"): BLUE, r"{5}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).next_to(3*RIGHT, UP)
        function_m = MTex(r"x^2-{5}y^2=-1", tex_to_color_map = {(r"x", r"y", r"-1"): GREEN, r"{5}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).shift(1.5*UP)
        linear = MTex(r"\binom{x}{y}\to\binom{2x+5y}{x+2y}", tex_to_color_map = {(r"x", r"y", r"5", r"2"): YELLOW}).scale(0.8).set_stroke(width = 10, color = BACK, background = True).next_to(5*LEFT, UP)
        self.fade_in(lines_h, lines_v, axes, hyperbola_p, hyperbola_m, *dots_p, *dots_m, function_p, function_m)
        self.wait(0, 28) #比如说 我们把2换成5
        self.wait(3, 21) #在x^2-5y^2=±1的两条双曲线上
        self.play(Write(linear), run_time = 1)
        self.wait(0, 23) #同样有一个变换
        arrows_1 = [Arrow(positions_p[0], positions_m[0], color = YELLOW, stroke_width = 2), Arrow(positions_m[0], positions_p[1], color = YELLOW, stroke_width = 2), Arrow(positions_p[1], positions_m[1], color = YELLOW, buff = 0.15), Arrow(positions_m[1], positions_p[2], color = YELLOW, stroke_width = 3)]
        arrows_2 = [Arrow(positions_p[5], positions_m[3], color = YELLOW, stroke_width = 2), Arrow(positions_m[3], positions_p[4], color = YELLOW, stroke_width = 2), Arrow(positions_p[4], positions_m[2], color = YELLOW, buff = 0.15), Arrow(positions_m[2], positions_p[3], color = YELLOW, stroke_width = 3), ]
        self.play(LaggedStart(*[ShowCreation(mob) for mob in arrows_1], run_time = 2, lag_ratio = 0.3), LaggedStart(*[ShowCreation(mob) for mob in arrows_2], run_time = 2, lag_ratio = 0.3))
        self.wait(0, 7) #能让上面的整点依次挪动一位
        self.wait(0, 17) #（空闲）

        self.wait(1, 10).fade_out() #甚至在一些更奇怪的双曲线上
        ratio = 2/3
        lines_h = VGroup(*[Line(30*LEFT + i*ratio*UP, 30*RIGHT + i*ratio*UP) for i in range(-25, 25)]).set_stroke(width = 1, color = RED_A)
        lines_v = VGroup(*[Line(16*DOWN + i*ratio*RIGHT, 16*UP + i*ratio*RIGHT) for i in range(-40, 40)]).set_stroke(width = 1, color = RED_A)
        axes = VGroup(Line(4*DOWN, 4*UP), Line(64/9*LEFT, 64/9*RIGHT), MTex(r"x").scale(0.75).next_to(RIGHT_SIDE, UL, buff = 0.1), MTex(r"y").scale(0.75).next_to(TOP, DL, buff = 0.1))
        positions_p = [np.array([7, -4, 0])*ratio, np.array([2, -1, 0])*ratio, np.array([1, 0, 0])*ratio, np.array([2, 1, 0])*ratio, np.array([7, 4, 0])*ratio, np.array([-7, -4, 0])*ratio, np.array([-2, -1, 0])*ratio, np.array([-1, 0, 0])*ratio, np.array([-2, 1, 0])*ratio, np.array([-7, 4, 0])*ratio]
        dots_p = [Dot(position, color = BLUE) for position in positions_p]
        hyperbola_p = VGroup(ParametricCurve(lambda t: ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-40), np.arcsinh(40), 0.01]), ParametricCurve(lambda t: -ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-40), np.arcsinh(40), 0.01])).set_stroke(color = BLUE, width = 3)
        hyperbola_m = VGroup(ParametricCurve(lambda t: ratio*np.array([np.sinh(t), np.cosh(t)/np.sqrt(3), 0]), [np.arcsinh(-40), np.arcsinh(40), 0.01]), ParametricCurve(lambda t: -ratio*np.array([np.sinh(t), np.cosh(t)/np.sqrt(3), 0]), [np.arcsinh(-40), np.arcsinh(40), 0.01])).set_stroke(color = GREEN, width = 3)
        function_p = MTex(r"x^2-{3}y^2=1", tex_to_color_map = {(r"x", r"y", r"1"): BLUE, r"{3}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).next_to(3*RIGHT, UP)
        function_m = MTex(r"x^2-{3}y^2=-1", tex_to_color_map = {(r"x", r"y", r"-1"): GREEN, r"{3}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).shift(1.5*UP)
        linear = MTex(r"\binom{x}{y}\to\binom{2x+3y}{x+2y}", tex_to_color_map = {(r"x", r"y", r"3", r"2"): YELLOW}).scale(0.8).set_stroke(width = 10, color = BACK, background = True).next_to(4*LEFT, UP)
        self.fade_in(lines_h, lines_v, axes, hyperbola_m, hyperbola_p, *dots_p, function_p, function_m)
        self.wait(0, 29) #这个规律也成立
        
        anims_1 = AnimationGroup(*[Flash(mob) for mob in [positions_p[2], positions_p[7]]])
        anims_2 = AnimationGroup(*[Flash(mob) for mob in [positions_p[1], positions_p[3], positions_p[6], positions_p[8]]])
        anims_3 = AnimationGroup(*[Flash(mob) for mob in [positions_p[0], positions_p[4], positions_p[5], positions_p[9]]])
        self.wait(1) #比如说......
        self.play(LaggedStart(anims_1, anims_2, anims_3, run_time = 2, lag_ratio = 0.5))
        self.wait(1, 6) #......x^2-3y^2=1上有很多整点
        copy_m = hyperbola_m.copy().set_stroke(color = YELLOW, width = 6)
        self.play(ShowPassingFlash(copy_m[0]), ShowPassingFlash(copy_m[1]), run_time = 2)
        self.play(ShowPassingFlash(copy_m[0]), ShowPassingFlash(copy_m[1]), run_time = 2)
        self.wait(3+0-4, 22+19) #而x^2-3y^2=-1上却一个整点都没有 （空闲）
        self.play(Write(linear), run_time = 1)
        self.wait(2, 6) #即便如此 我们仍然能找到一个变换
        arrows_1 = [Arrow(positions_p[i], positions_p[i+1], color = YELLOW, stroke_width = 5-abs(i-1.5)) for i in range(4)]
        arrows_2 = [Arrow(positions_p[9-i], positions_p[8-i], color = YELLOW, stroke_width = 5-abs(i-1.5)) for i in range(4)]
        notice = MTexText(r"*注意这个变换和\\前两个变换的不同", stroke_width = 10, stroke_color = BACK, draw_stroke_behind_fill = True).scale(0.6).shift(2*DOWN)
        self.play(LaggedStart(*[ShowCreation(mob) for mob in arrows_1], run_time = 2, lag_ratio = 0.3), LaggedStart(*[ShowCreation(mob) for mob in arrows_2], run_time = 2, lag_ratio = 0.3), FadeIn(notice, 0.5*UP))
        self.wait(0, 26) #让这一条双曲线上的整点依次挪动一位
        self.wait(0, 23) #（空闲）

        self.play(*[FadeOut(mob) for mob in arrows_1 + arrows_2 + [notice]])
        self.wait(1, 3) #那除了这个变换本身
        self.wait(1, 26) #还有没有什么别的思路
        self.wait(1, 19) #能刻画这种均匀性呢
        self.wait(0, 25) #（空闲）

        self.play(self.change_notice())
        self.wait(0, 25) #最容易看出来的是
        labels = [MTex(r"(2, -1)", color = YELLOW).scale(0.6).next_to(dots_p[1], DL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(1, 0)", color = YELLOW).scale(0.6).next_to(dots_p[2], LEFT, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(2, 1)", color = YELLOW).scale(0.6).next_to(dots_p[3], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)]
        segments = [Line(positions_p[2], positions_p[1], color = YELLOW, stroke_width = 3), Line(positions_p[3], positions_p[2], color = YELLOW, stroke_width = 3)]
        self.add(segments[1], dots_p[2], dots_p[3]).play(*[Write(mob) for mob in labels], ShowCreation(segments[1]))
        self.wait(2, 6) #(2, 1)和(1, 0)之间......
        self.add(segments[0], dots_p[1], dots_p[2]).play(ShowCreation(segments[0]))
        self.wait(3, 7) #......与(1, 0)和(2, -1)之间的距离 是相等的
        self.wait(0, 24) #（空闲）

        self.play(*[Flash(mob) for mob in dots_p[1:4]])
        self.wait(1, 18) #这两对点关于x轴对称
        line = Line(positions_p[1], positions_p[3], color = YELLOW, stroke_width = 3)
        tangent = Line(positions_p[2]+1/3*DOWN, positions_p[2]+1/3*UP, color = YELLOW, stroke_width = 3)
        self.add(line, dots_p[1], dots_p[3]).play(FadeOut(segments[0]), FadeOut(segments[1]), ShowCreation(line))
        self.wait(2, 1) #连接(2, 1)和(2, -1)
        self.add(tangent, dots_p[2], *labels).play(GrowFromCenter(tangent))
        self.wait(2, 14) #那么这条线就和(1, 0)处的切线平行
        self.wait(1, 0) #（空闲）

        background = VGroup(lines_h.copy(), lines_v.copy(), hyperbola_p.copy(), hyperbola_m.copy()).set_stroke(width = 1, color = GREY).add(*[dot.copy().set_color(GREY) for dot in dots_p])
        trans_positions_p = [np.array([26, -15, 0])*ratio, np.array([7, -4, 0])*ratio, np.array([2, -1, 0])*ratio, np.array([1, 0, 0])*ratio, np.array([2, 1, 0])*ratio, np.array([7, 4, 0])*ratio, np.array([26, 15, 0])*ratio]
        trans_dots_1 = [Dot(position, color = BLUE) for position in trans_positions_p[:-1]]
        trans_dots_2 = [Dot(-position, color = BLUE) for position in trans_positions_p[:-1]]
        trans = lambda t: np.array([2*t[0]+3*t[1], t[0]+2*t[1], 0])
        self.bring_to_back(background).remove(*dots_p).add(*trans_dots_1, *trans_dots_2).play(*[mob.animate.apply_function(trans, about_point = ORIGIN) for mob in [lines_h, lines_v, hyperbola_p, hyperbola_m, line, tangent]], 
                                            *[trans_dots_1[i].animate.move_to(trans_positions_p[i+1]) for i in range(6)], *[trans_dots_2[i].animate.move_to(-trans_positions_p[i+1]) for i in range(6)], run_time = 3)
        self.wait(0, 26) #让这条双曲线变换一次 (2, 1)现在跑到了......
        label_3 = MTex(r"(7, 4)", color = YELLOW).scale(0.6).next_to(dots_p[4], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)
        self.play(Write(label_3), background.set_submobjects(background.submobjects[0:2].copy()).animate.set_stroke(width = 1, color = RED_A), FadeOut(lines_h), FadeOut(lines_v))
        self.wait(0, 14) #......(7, 4)的位置
        self.wait(0, 19) #（空闲）

        lines_h = VGroup(*[Line(30*LEFT + i*ratio*UP, 30*RIGHT + i*ratio*UP) for i in range(-25, 25)]).set_stroke(width = 1, color = RED_A)
        lines_v = VGroup(*[Line(16*DOWN + i*ratio*RIGHT, 16*UP + i*ratio*RIGHT) for i in range(-40, 40)]).set_stroke(width = 1, color = RED_A)
        self.remove(background).bring_to_back(lines_h, lines_v).wait(1, 9) #这个时候......
        copy_line = line.copy().set_stroke(color = WHITE, width = 8)
        copy_tangent = tangent.copy().set_stroke(color = WHITE, width = 8)
        self.remove(*trans_dots_1, *trans_dots_2).add(copy_line, *dots_p).play(ShowPassingFlash(copy_line))
        self.add(copy_line, dots_p[2], dots_p[4]).play(ShowPassingFlash(copy_line))
        self.wait(0, 1) #......(1, 0)和它的连线
        self.add(copy_tangent, dots_p[3], labels[1]).play(ShowPassingFlash(copy_tangent))
        self.add(copy_tangent, dots_p[3], labels[1]).play(ShowPassingFlash(copy_tangent))
        self.wait(0, 20) #也是平行于(2, 1)处的切线的
        self.wait(0, 25) #（空闲）

        circle = Circle(radius = 2.5, color = WHITE)
        dots = [Dot(2.5*unit(PI)), Dot(2.5*unit(PI*2/3)), Dot(2.5*unit(PI*4/3))]
        labels_1 = [MTex("A").scale(0.8).shift(3*unit(PI*2/3)), MTex("B").scale(0.8).shift(3*unit(PI)), MTex("C").scale(0.8).shift(3*unit(PI*4/3))]
        self.add(self.shade, self.notice).play(ShowCreation(circle), self.change_notice())
        self.play(*[ShowCreation(dot) for dot in dots], *[Write(mob) for mob in labels_1])
        self.wait(0, 11) #这很像圆上的一个性质

        line_c = Line(2.5*unit(PI*4/3), 2.5*unit(PI*2/3), color = YELLOW)
        tangent_c = Line(2.5*unit(PI) + DOWN, 2.5*unit(PI) + UP, color = YELLOW)
        arc_ba = Arc(PI, -PI/3, radius = 2.5, color = YELLOW, stroke_width = 8)
        arc_bc = Arc(PI, PI/3, radius = 2.5, color = YELLOW, stroke_width = 8)
        self.add(arc_ba, arc_bc, *dots).play(ShowPassingFlash(arc_ba), ShowPassingFlash(arc_bc))
        self.add(arc_ba, arc_bc, *dots).play(ShowPassingFlash(arc_ba), ShowPassingFlash(arc_bc))
        self.wait(1, 3) #如果AB和BC是两段等长的弧
        self.add(line_c, tangent_c, *dots).play(ShowCreation(line_c), ShowCreation(tangent_c))
        self.wait(1, 15) #那么AC和B处的切线平行
        self.wait(0, 29) #（空闲）

        self.play(*[mob.animate.shift(3.5*RIGHT) for mob in [circle, line_c, tangent_c] + dots + labels_1])
        circle_2 = Circle(radius = 2.5, color = WHITE).shift(3.5*LEFT)
        dots_2 = [Dot(2.5*unit(PI)), Dot(2.5*unit(PI*2/3)), Dot(2.5*unit(PI*4/3)), Dot(2.5*unit(PI/3))]
        labels_2 = [MTex("A").scale(0.8).shift(3*unit(PI/3)), MTex("B").scale(0.8).shift(3*unit(PI*2/3)), MTex("C").scale(0.8).shift(3*unit(PI)), MTex("D").scale(0.8).shift(3*unit(PI*4/3))]
        for mob in dots_2 + labels_2:
            mob.shift(3.5*LEFT)
        self.play(ShowCreation(circle_2))
        self.play(*[ShowCreation(dot) for dot in dots_2], *[Write(mob) for mob in labels_2])
        self.wait(0, 13) #在圆上 这只是另一个性质的特殊情况
        self.wait(0, 21) #（空闲）
        
        line_ad = Line(2.5*unit(PI*4/3), 2.5*unit(PI/3), color = YELLOW).shift(3.5*LEFT)
        line_bc = Line(2.5*unit(PI), 2.5*unit(PI*2/3), color = YELLOW).shift(3.5*LEFT)
        arc_ba = Arc(PI*2/3, -PI/3, radius = 2.5, color = YELLOW, stroke_width = 8).shift(3.5*LEFT)
        arc_cd = Arc(PI, PI/3, radius = 2.5, color = YELLOW, stroke_width = 8).shift(3.5*LEFT)
        self.add(arc_ba, arc_cd, *dots_2).play(ShowPassingFlash(arc_ba), ShowPassingFlash(arc_cd))
        self.add(arc_ba, arc_cd, *dots_2).play(ShowPassingFlash(arc_ba), ShowPassingFlash(arc_cd))
        self.wait(0, 29) #如果AB和CD是两段等长的弧
        self.add(line_ad, line_bc, *dots_2).play(ShowCreation(line_ad), ShowCreation(line_bc))
        self.wait(1, 0) #那么AD和BC平行
        self.wait(0, 22) #（空闲）

        self.wait(2, 19) #在双曲线上也会有这种性质吗
        shade = self.shade.copy()
        self.add(shade, self.notice).play(FadeIn(shade))
        function_p.shift(6*LEFT)
        new_labels = [MTex(r"D(2, -1)", color = YELLOW).scale(0.6).next_to(dots_p[1], DL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"C(1, 0)", color = YELLOW).scale(0.6).next_to(dots_p[2], LEFT, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"B(2, 1)", color = YELLOW).scale(0.6).next_to(dots_p[3], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"A(7, 4)", color = YELLOW).scale(0.6).next_to(dots_p[4], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)]
        self.remove(shade, circle, line_c, tangent_c, circle_2, line_ad, line_bc, *dots, *labels_1, *dots_2, *labels_2, line, tangent, linear, *labels, label_3
                    ).add(*new_labels, self.shade, self.notice).play(FadeOut(self.shade)) #我们来试一试 （空闲）
        
        self.play(LaggedStart(*[Flash(position) for position in positions_p[4:0:-1]], run_time = 2.5, lag_ratio = 0.5))
        self.wait(1, 3) #ABCD是双曲线上连续的4个点
        self.wait(0, 19) #（空闲）

        line_ad = Line(positions_p[4], positions_p[1], stroke_width = 3, color = YELLOW)
        line_bc = Line(positions_p[3], positions_p[2], stroke_width = 3, color = YELLOW)
        self.add(line_ad, line_bc, *dots_p).play(ShowCreation(line_ad), ShowCreation(line_bc))
        self.wait(2, 18) #而AD的斜率 和BC的斜率 都是1
        self.wait(1, 1) #（空闲）

        positions_2 = [np.array([26, 15, 0])*ratio, np.array([26, -15, 0])*ratio, np.array([97, 56, 0])*ratio, np.array([97, -56, 0])*ratio, np.array([-26, -15, 0])*ratio, np.array([-26, 15, 0])*ratio, np.array([-97, -56, 0])*ratio, np.array([-97, 56, 0])*ratio]
        dots_2 = [Dot(position, color = BLUE) for position in positions_2]
        hyperbola_p.become(VGroup(ParametricCurve(lambda t: ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-150), np.arcsinh(150), 0.01]), ParametricCurve(lambda t: -ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-150), np.arcsinh(150), 0.01])).set_stroke(color = BLUE, width = 3))
        hyperbola_m.become(VGroup(ParametricCurve(lambda t: ratio*np.array([np.sinh(t), np.cosh(t)/np.sqrt(3), 0]), [np.arcsinh(-150), np.arcsinh(150), 0.01]), ParametricCurve(lambda t: -ratio*np.array([np.sinh(t), np.cosh(t)/np.sqrt(3), 0]), [np.arcsinh(-150), np.arcsinh(150), 0.01])).set_stroke(color = GREEN, width = 3))
        ratio = 2-np.sqrt(3)
        labels_2 = [MTex(r"(7, -4)", color = YELLOW).scale(0.6).next_to(dots_p[0], DL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(26, 15)", color = YELLOW).scale(0.6).next_to(dots_2[0], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(26, -15)", color = YELLOW).scale(0.6).next_to(dots_2[1], DL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(97, 56)", color = YELLOW).scale(0.6).next_to(dots_2[2], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(97, -56)", color = YELLOW).scale(0.6).next_to(dots_2[3], DL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)]
        self.play(self.change_notice(), *[FadeOut(mob[0]) for mob in new_labels], FadeOut(function_p), FadeOut(function_m), FadeIn(labels_2[0]))
        for mob in new_labels:
            mob.remove(mob[0])
        self.wait(1, 9) #这真是相当不错的性质
        self.add(*dots_2).play(*[FadeOut(mob, scale = ratio) for mob in [lines_h, lines_v]], *[FadeOut(mob, -mob.get_x()*(1-ratio)*np.array([1, 1/np.sqrt(3), 0])) for mob in [new_labels[1], new_labels[2]]], 
                               *[mob.animate.scale(ratio, about_point = ORIGIN) for mob in [hyperbola_p, hyperbola_m, line_ad, line_bc]], 
                               *[mob.animate.shift(-mob.get_x(RIGHT)*(1-ratio)*(np.array([1, 1/np.sqrt(3), 0]) if mob.get_y()> 0 else np.array([1, -1/np.sqrt(3), 0]))) for mob in [new_labels[0], new_labels[3]]+labels_2],
                               *[mob.animate.shift(-mob.get_center()*(1-ratio)).set_height(min(mob.get_x()/12.5, 0.16)) for mob in dots_p+dots_2], run_time = 2)#事实上我们可以证明
        line_3 = Line(positions_p[0]*ratio, positions_2[0]*ratio, color = RED_B)
        line_ad_copy = line_ad.copy().reverse_points().set_stroke(color = RED_B, width = 4)
        anims_1 = AnimationGroup(Flash(ratio*positions_p[1]), Flash(ratio*positions_p[0]))
        anims_2 = AnimationGroup(ShowCreation(line_3), ShowCreation(line_ad_copy))
        anims_3 = AnimationGroup(Flash(ratio*positions_p[4]), Flash(ratio*positions_2[0]))
        self.add(line_3, line_ad_copy, *dots_p, *dots_2).play(LaggedStart(anims_1, anims_2, anims_3, group = Group(anims_1.mobject, anims_3.mobject), lag_ratio = 0.5, run_time = 2), line_bc.animate.set_color(RED_B))
        self.remove(line_ad_copy)
        line_ad.set_stroke(color = RED_B, width = 4)
        self.wait(1+2-2, 23+0) #连接相邻的两对点 这两条弦总是平行的
        self.wait(0, 27) #（空闲）

        self.play(*[FadeOut(mob, -mob.get_x()*(1-ratio)*np.array([1, 1/np.sqrt(3), 0])) for mob in [new_labels[0], new_labels[3]]], 
                  *[mob.animate.scale(ratio, about_point = ORIGIN) for mob in [hyperbola_p, hyperbola_m, line_ad, line_bc, line_3]], 
                  *[mob.animate.shift(-mob.get_x(RIGHT)*(1-ratio)*(np.array([1, 1/np.sqrt(3), 0]) if mob.get_y()> 0 else np.array([1, -1/np.sqrt(3), 0]))) for mob in labels_2],
                  *[mob.animate.shift(-mob.get_center()*(1-ratio)).set_height(min(mob.get_x()/12.5, 0.16)) for mob in dots_p+dots_2], run_time = 2)
        self.play(*[Flash(position) for position in [positions_p[1]*ratio**2, positions_2[1]*ratio**2]])
        self.play(*[Flash(position) for position in [positions_p[4]*ratio**2, positions_2[2]*ratio**2]])
        self.wait(0, 1) #更进一步 如果两对点之间隔了同样多的点
        line_4 = Line(positions_2[1]*ratio**2, positions_2[2]*ratio**2, color = YELLOW)
        line_ad_copy = line_ad.copy().reverse_points().set_stroke(color = YELLOW)
        self.add(line_4, line_ad_copy, *dots_p, *dots_2).play(ShowCreation(line_4), ShowCreation(line_ad_copy), line_bc.animate.set_color(YELLOW), line_3.animate.set_color(YELLOW))
        self.wait(2, 2) #那连接它们的两条弦 也总是平行的
        self.wait(1, 3) #（空闲）

        self.fade_out(change_notice = True)
        ratio = 1/6
        hyperbola_p = VGroup(ParametricCurve(lambda t: ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-50), np.arcsinh(50), 0.01]), ParametricCurve(lambda t: -ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-50), np.arcsinh(50), 0.01])).set_stroke(color = BLUE, width = 4)
        function_p = MTex(r"x^2-{3}y^2=1", tex_to_color_map = {(r"x", r"y", r"1"): BLUE, r"{3}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).shift(1.5*UP)
        positions_p = [np.array([26, -15, 0])*ratio, np.array([7, -4, 0])*ratio, np.array([2, -1, 0])*ratio, np.array([1, 0, 0])*ratio, np.array([2, 1, 0])*ratio, np.array([7, 4, 0])*ratio, np.array([26, 15, 0])*ratio, np.array([-26, -15, 0])*ratio, np.array([-7, -4, 0])*ratio, np.array([-2, -1, 0])*ratio, np.array([-1, 0, 0])*ratio, np.array([-2, 1, 0])*ratio, np.array([-7, 4, 0])*ratio, np.array([-26, 15, 0])*ratio]
        dots_p = [Dot(position, color = BLUE) for position in positions_p]
        labels = [MTex(r"A(x_A, y_A)", color = YELLOW).scale(0.6).next_to(dots_p[3], LEFT, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"B(x_B, y_B)", color = YELLOW).scale(0.6).next_to(dots_p[5], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"C(x_C, y_C)", color = YELLOW).scale(0.6).next_to(dots_p[2], DL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"D(x_D, y_D)", color = YELLOW).scale(0.6).next_to(dots_p[6], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)]
        lemma = MTexText(r"$A,\ B,\ C$都是整点，\\则$D$也是整点？", color = YELLOW).scale(0.8).set_stroke(width = 10, color = BACK, background = True).next_to(4*RIGHT, DOWN)

        self.fade_in(axes, hyperbola_p, function_p)
        self.wait(0, 18) #既然如此 那反过来
        line = Line(positions_p[3], positions_p[5], color = YELLOW)
        line_2 = Line(positions_p[2], positions_p[6], color = YELLOW)
        self.play(GrowFromCenter(line), GrowFromCenter(dots_p[3]), GrowFromCenter(dots_p[5]))
        self.wait(1, 7) #如果我们已经有了一条弦
        self.play(Write(labels[0]), Write(labels[1]))
        self.wait(1, 12) #它的两个端点都是整点
        self.play(ShowCreation(line_2), GrowFromCenter(dots_p[2]), Write(labels[2]))
        self.play(GrowFromCenter(dots_p[6]), Write(labels[3]))
        self.wait(0, 13) #过别的整点作它的平行线
        self.play(FadeIn(lemma, 0.3*UP))
        self.wait(1, 29) #这条线和双曲线一定会再交到整点上吗
        self.wait(0, 23) #（空闲）

        self.play(FadeOut(lemma[-1], 0.5*DR))
        lemma.remove(lemma[-1])
        self.wait(0, 22) #答案是一定的
        board = Rectangle(height = 8.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 8.4, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board.add(inner).next_to(LEFT, LEFT, buff = 0.1)
        tex_1 = MTex(r"k=k_{CD}=k_{AB}=\frac{y_B-y_A}{x_B-x_A}").scale(0.5).next_to(6*LEFT + 3*UP)
        tex_2 = MTex(r"\begin{cases}y-y_C = k_{CD}(x-x_C)\\x^2-3y^2=1\end{cases}").scale(0.5).next_to(6*LEFT + 2*UP)
        tex_3 = MTex(r"x^2-\frac{6k(-kx_C+y_C)}{1-3k^2}x-\frac{3(-kx_C+y_C)^2+1}{1-3k^2}=0").scale(0.5).next_to(7*LEFT + UP, buff = 0)
        tex_4 = MTex(r"x_C+x_D = \frac{6k(-kx_C+y_C)}{1-3k^2}", isolate = r"=").scale(0.5).next_to(6*LEFT)
        tex_5 = MTex(r"x_D=\frac{(-1-3k^2)x_C+6ky_C}{1-3k^2}", isolate = r"=").scale(0.5).set_y(-1)
        tex_5.set_x(tex_4.get_part_by_tex(r"=").get_x() - tex_5.get_part_by_tex(r"=").get_x())
        tex_6 = MTex(r"x_D=(x_Ax_B+3y_Ay_B)x_C -3(x_Ay_B+x_By_A)y_C", isolate = r"=").scale(0.5).next_to(7*LEFT + 2*DOWN, buff = 0)
        tex_7 = MTex(r"y_D=(x_Ay_B+x_By_A)x_C -(x_Ax_B+3y_Ay_B)y_C", isolate = r"=").scale(0.5).set_y(-2.5)
        tex_7.set_x(tex_6.get_part_by_tex(r"=").get_x() - tex_7.get_part_by_tex(r"=").get_x())
        board.add(tex_1, tex_2, tex_3, tex_4, tex_5, tex_6, tex_7).shift(6.5*LEFT).remove(inner, tex_1, tex_2, tex_3, tex_4, tex_5, tex_6, tex_7)
        board_all = [board, inner, tex_1, tex_2, tex_3, tex_4, tex_5, tex_6, tex_7]
        shade_copy = self.shade.copy().set_opacity(0.5)
        self.add(shade_copy, self.notice).play(FadeIn(shade_copy), *[mob.animating(rate_func = rush_from).shift(6.5*RIGHT) for mob in board_all], self.change_notice())
        self.wait(1, 3) #可以用一定的计算来说明这一点
        self.wait(0, 24) #（空闲）

        self.wait(3, 4) #虽然这个计算过程多少有些繁琐
        surr = SurroundingRectangle(VGroup(tex_6, tex_7))
        self.play(ShowCreation(surr))
        board_all.append(surr)
        self.wait(1, 15) #但只需要观察最后的计算结果
        self.wait(1, 28) #就足以确认这个点是整点
        self.wait(0, 22) #（空闲）

        self.add(*tex_6.submobjects, *tex_7.submobjects).play(LaggedStart(*[mob.animating(rate_func = there_and_back).shift(0.1*UP).set_color(YELLOW).scale(1.2) for mob in tex_6.submobjects], run_time = 2, lag_ratio = 0.1), LaggedStart(*[mob.animating(rate_func = there_and_back).shift(0.2*UP).set_color(YELLOW).scale(1.2) for mob in tex_7.submobjects], run_time = 2, lag_ratio = 0.1))
        self.wait(2, 18) #它是由整数通过加法 减法 乘法计算出来的
        self.wait(1, 22) #自然自己也是整数
        self.wait(1, 1) #（空闲）

        self.add(self.shade, lemma, shade_copy, self.notice, *board_all).play(*[mob.animating(rate_func = rush_into, remover = True).shift(6.5*LEFT) for mob in board_all], FadeOut(shade_copy), FadeIn(self.shade), lemma.animating(rate_func = rush_into).move_to((3*UP + 3*LEFT+lemma.get_center())/2), self.change_notice())
        self
        ratio = 1/3
        offset = 6*LEFT + 2.25*DOWN
        axes = VGroup(Arrow(1.5*LEFT, 10*RIGHT, buff = 0), Arrow(1.5*DOWN, 6*UP, buff = 0), MTex(r"x").scale(0.75).next_to(10*RIGHT, UP), MTex(r"y").scale(0.75).next_to(6*UP, RIGHT)).shift(offset)
        hyperbola_p = VGroup(ParametricCurve(lambda t: ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-4.5*np.sqrt(3)), np.arcsinh(30), 0.01])).set_stroke(color = BLUE).shift(offset)
        function_p = MTex(r"x^2-{3}y^2=1", tex_to_color_map = {(r"x", r"y", r"1"): BLUE, r"{3}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).shift(1.5*UP + 2*LEFT)
        positions_p = [np.array([7, -4, 0])*ratio, np.array([2, -1, 0])*ratio, np.array([1, 0, 0])*ratio, np.array([2, 1, 0])*ratio, np.array([7, 4, 0])*ratio, np.array([26, 15, 0])*ratio]
        dots_p = [Dot(position + offset, color = BLUE) for position in positions_p]
        labels = [MTex(r"(1, 0)").scale(0.6).next_to(dots_p[2], LEFT, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(2, 1)").scale(0.6).next_to(dots_p[3], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)]
        self.clear().add(axes, hyperbola_p, function_p, self.shade, lemma, self.notice).play(FadeOut(self.shade), lemma.animating(rate_func = rush_from).move_to(3*UP + 3*LEFT))
        self.wait(0, 25) #有了这个性质 我们就可以说明
        self.wait(2, 10) #这条双曲线上的整点是均匀的
        self.wait(0, 19) #（空闲）

        self.wait(1, 15) #更准确来说
        self.play(ShowCreation(dots_p[2]), Write(labels[0]), Flash(positions_p[2] + offset))
        self.wait(0, 27) #从(1, 0)出发
        self.play(ShowCreation(dots_p[3]), Write(labels[1]), Flash(positions_p[3] + offset))
        self.wait(1, 5) #遇到的第一个整点是(2, 1)
        self.wait(0, 19) #（空闲）

        linear = MTex(r"\binom{x}{y}\to\binom{2x+3y}{x+2y}", tex_to_color_map = {(r"2", r"3", r"x", r"y"): TEAL}).scale(0.8).shift(4*RIGHT + UP)
        inverse = MTex(r"\binom{2x-3y}{-x+2y}\gets\binom{x}{y}", tex_to_color_map = {(r"2", r"3", r"x", r"y"): TEAL}).scale(0.8).shift(4*RIGHT + 0.5*DOWN)
        self.play(FadeIn(linear, 0.5*LEFT), ShowCreation(dots_p[4]), Flash(positions_p[4] + offset))
        self.wait(1)
        self.play(ShowCreation(dots_p[5]), Flash(positions_p[5] + offset))
        self.wait(1, 18) #在“保持双曲线不变，把(1, 0)变成(2, 1)”的变换
        self.play(FadeIn(inverse, 0.5*LEFT), ShowCreation(dots_p[1]), Flash(positions_p[1] + offset))
        self.play(ShowCreation(dots_p[0]), Flash(positions_p[0] + offset))
        self.wait(0, 6) #和它的逆变换的作用下
        self.wait(4, 0) #我们就能得到x^2-3y^2=1上的所有整点
        self.wait(1, 1) #（空闲）

        position_extra = ratio*np.array([np.sqrt(170), 13/np.sqrt(3), 0]) + offset
        dot_extra = Dot(position_extra, color = RED)
        label_extra = MTex(r"P", color = RED).scale(0.6).next_to(dot_extra, UL, buff = 0.1)
        self.wait(2, 23) #如果在如果双曲线上还有其它整点
        self.play(ShowCreation(dot_extra), Flash(position_extra), Write(label_extra))
        self.wait(1, 23) #那么不妨假设它的横纵坐标都是正的
        self.wait(0, 20) #（空闲）

        self.wait(2, 17) #既然它不属于我们找到的整点
        self.play(Flash(positions_p[4] + offset), Flash(positions_p[5] + offset), *[mob.animate.set_color(YELLOW) for mob in [dots_p[4], dots_p[5]]])
        self.wait(1, 3) #那它就一定在某两个点之间
        self.wait(0, 22) #（空闲）

        line_bc = Line(positions_p[4], positions_p[3], color = YELLOW).shift(offset)
        line_ad = Line(positions_p[5], positions_p[2], color = YELLOW).shift(offset)
        self.add(line_bc, line_ad, *dots_p, dot_extra).play(ShowCreation(line_bc), ShowCreation(line_ad))
        self.wait(2, 27) #把这两个点和(1, 0) (2, 1)分别连起来
        copy_bc = line_bc.copy().set_stroke(color = WHITE, width = 8)
        copy_ad = line_ad.copy().set_stroke(color = WHITE, width = 8)
        self.add(copy_bc, copy_ad, *dots_p, dot_extra).play(ShowPassingFlash(copy_bc), ShowPassingFlash(copy_ad))
        self.add(copy_bc, copy_ad, *dots_p, dot_extra).play(ShowPassingFlash(copy_bc), ShowPassingFlash(copy_ad)) #那么这两条线是平行的
        self.wait(0, 20) #（空闲）

        position_false = ratio*np.array([26*np.sqrt(170)-45*13/np.sqrt(3), 15*np.sqrt(170)-26*13/np.sqrt(3), 0]) + offset
        dot_false = Dot(position_false, color = RED)
        line_false = Line(position_extra, position_false,  color = RED)
        self.add(line_false, *dots_p, dot_extra).play(ShowCreation(line_false))
        self.play(ShowCreation(dot_false))
        self.wait(1, 4) #再过P也作这两条直线的平行线
        self.play(Flash(position_false))
        self.wait(2, 15) #那么这条平行线会再交双曲线于一个整点
        self.wait(0, 22) #（空闲）

        self.play(*[mob.animate.set_color(GREY) for mob in [line_false, dot_extra, dot_false, label_extra]])
        self.wait(3, 2) #但(1, 0)和(2, 1)之间不可能有其它的整点
        self.play(*[FadeOut(mob) for mob in [line_false, dot_extra, dot_false, label_extra, lemma, line_bc, line_ad]], *[mob.animate.set_color(BLUE) for mob in [dots_p[4], dots_p[5]]], self.change_notice())
        self.wait(1, 0) #所以P也不可能存在
        self.wait(0, 19) #（空闲）

        self.play(ShowCreation(SurroundingRectangle(VGroup(linear, inverse)), run_time = 2))
        self.wait(3, 16) #也就是说 我们已经把x^2-3y^2=1上面的整点找全了
        self.wait(2, 7)
        self.fade_out(end = True)
        self.wait(3, 0) #到此共240秒

#################################################################### 

class Chapter3_0(FrameScene):

    def construct(self):

        text3 = MTexText("第三节 曲线上的有理点", tex_to_color_map={"第三节": YELLOW, "曲线": GREEN, "有理点": BLUE})

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(FrameScene):
    def construct(self):
        self.notices = [Notice("结论推广", "请　模仿"),
                        Notice("尝试推广", "请　思考"),
                        Notice("推广失败", "请勿模仿"),
                        Notice("这里是一个", "数学频道"),
                        Notice("拓宽思路", "请　模仿"), 
                        Notice("这里是一个", "数学频道"),
                        Notice("融会贯通", "请　模仿")]
        self.notice = self.notices[0]

        ratio = 1/5
        axes_3 = VGroup(Line(4*DOWN, 4*UP), Line(64/9*LEFT, 64/9*RIGHT), MTex(r"x").scale(0.75).next_to(RIGHT_SIDE, UL, buff = 0.1), MTex(r"y").scale(0.75).next_to(TOP, DL, buff = 0.1))
        positions_3 = [np.array([7, -4, 0])*ratio, np.array([2, -1, 0])*ratio, np.array([1, 0, 0])*ratio, np.array([2, 1, 0])*ratio, np.array([7, 4, 0])*ratio, np.array([-7, -4, 0])*ratio, np.array([-2, -1, 0])*ratio, np.array([-1, 0, 0])*ratio, np.array([-2, 1, 0])*ratio, np.array([-7, 4, 0])*ratio]
        dots_3 = [Dot(position, color = BLUE) for position in positions_3]
        hyperbola_3 = VGroup(ParametricCurve(lambda t: ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-40), np.arcsinh(40), 0.01]), ParametricCurve(lambda t: -ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-40), np.arcsinh(40), 0.01])).set_stroke(color = BLUE, width = 3)
        function_3 = MTex(r"x^2-{3}y^2=1", tex_to_color_map = {(r"x", r"y", r"1"): BLUE, r"{3}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).next_to(3*RIGHT, UP)
        linear_3 = MTex(r"\binom{x}{y}\to\binom{2x+3y}{x+2y}", tex_to_color_map = {(r"x", r"y", r"3", r"2"): YELLOW}).scale(0.8).set_stroke(width = 10, color = BACK, background = True).next_to(4*LEFT, UP)
        self.fade_in(axes_3, hyperbola_3, *dots_3, function_3, linear_3)
        self.wait(1, 25) #除了x^2-3y^2=1
        self.wait(1, 25) #其它的双曲线上面的整点
        self.wait(1, 9) #也具有这个规律
        self.wait(0, 17) #（空闲）

        board_left = Rectangle(height = 8.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 8.4, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board_left.add(inner).next_to(0.1*RIGHT, LEFT, buff = 0)
        ratio = 1/4
        offset = 7*LEFT + 0.5*UP
        positions_2 = [np.array([3, -2, 0])*ratio, np.array([1, 0, 0])*ratio, np.array([3, 2, 0])*ratio, np.array([17, 12, 0])*ratio]
        dots_2 = [Dot(position + offset, color = BLUE) for position in positions_2]
        labels_2 = [MTex(r"(x_A, y_A)").scale(0.6).next_to(dots_2[3], DR, buff = 0.1).set_stroke(width = 10, color = "#222222", background = True), MTex(r"(x_B, y_B)").scale(0.6).next_to(dots_2[2], UR, buff = 0.1).set_stroke(width = 10, color = "#222222", background = True), MTex(r"(x_C, y_C)").scale(0.6).next_to(dots_2[1], RIGHT, buff = 0.1).set_stroke(width = 10, color = "#222222", background = True), MTex(r"((x_Ax_B+2y_Ay_B)x_C -2(x_Ay_B+x_By_A)y_C, \\(x_Ay_B+x_By_A)x_C -(x_Ax_B+2y_Ay_B)y_C)").scale(0.6).next_to(dots_2[0], DR, buff = 0.1).shift(0*LEFT).set_stroke(width = 10, color = "#222222", background = True)]
        hyperbola_2 = ParametricCurve(lambda t: ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(2), 0]), [np.arcsinh(-40), np.arcsinh(40), 0.01]).set_stroke(color = BLUE, width = 3).shift(offset)
        function_2 = MTex(r"x^2-{2}y^2=1", tex_to_color_map = {(r"x", r"y", r"1"): BLUE, r"{2}": TEAL}).set_stroke(width = 10, color = "#222222", background = True).scale(0.8).next_to(1.5*RIGHT + 2*UP, UP).shift(offset)
        linear_2 = MTex(r"\binom{x}{y}\to\binom{3x+4y}{2x+3y}", tex_to_color_map = {(r"x", r"y", r"3", r"2", r"4"): YELLOW}).scale(0.8).next_to(3*RIGHT + 3.5*DOWN, UP).shift(offset).set_stroke(width = 10, color = "#222222", background = True)
        line_ad = Line(positions_2[0], positions_2[3]).shift(offset).set_color(YELLOW)
        line_bc = Line(positions_2[1], positions_2[2]).shift(offset).set_color(YELLOW)
        all_left = VGroup(hyperbola_2, line_ad, line_bc, *dots_2, function_2, *labels_2).set_stroke(background = True)
        shade = self.shade.copy().set_opacity(0.5)
        self.add(shade, board_left, all_left, self.notice).play(FadeIn(shade), board_left.shift(8*LEFT).animate.shift(8*RIGHT), all_left.shift(8*LEFT).animate.shift(8*RIGHT), rate_func = rush_from, run_time = 2)
        self.wait(1, 26) #比如说 在x^2-2y^2=1上面

        board_right = Rectangle(height = 8.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = YELLOW_E)
        inner = Rectangle(height = 8.4, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = WHITE)
        board_right.add(inner).next_to(0.1*LEFT, RIGHT, buff = 0)
        ratio = 1/25
        offset = 0.5*RIGHT + UP
        positions_5 = [np.array([9, -4, 0])*ratio, np.array([1, 0, 0])*ratio, np.array([9, 4, 0])*ratio, np.array([161, 72, 0])*ratio]
        dots_5 = [Dot(position + offset, color = BLUE) for position in positions_5]
        labels_5 = [MTex(r"(x_A, y_A)").scale(0.6).next_to(dots_5[3], DL, buff = 0.1).set_stroke(width = 10, color = "#222222", background = True), MTex(r"(x_B, y_B)").scale(0.6).next_to(dots_5[2], RIGHT, buff = 0.1).shift(0.1*RIGHT).set_stroke(width = 10, color = "#222222", background = True), MTex(r"(x_C, y_C)").scale(0.6).next_to(dots_5[1], UP).set_stroke(width = 10, color = "#222222", background = True), MTex(r"((x_Ax_B+5y_Ay_B)x_C -5(x_Ay_B+x_By_A)y_C, \\(x_Ay_B+x_By_A)x_C -(x_Ax_B+5y_Ay_B)y_C)").scale(0.6).next_to(dots_5[0], DR, buff = 0.1).shift(0*LEFT).set_stroke(width = 10, color = "#222222", background = True)]
        hyperbola_5 = ParametricCurve(lambda t: ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(5), 0]), [np.arcsinh(-180), np.arcsinh(180), 0.01]).set_stroke(color = BLUE, width = 3).shift(offset)
        function_5 = MTex(r"x^2-{5}y^2=1", tex_to_color_map = {(r"x", r"y", r"1"): BLUE, r"{5}": TEAL}).set_stroke(width = 10, color = "#222222", background = True).scale(0.8).next_to(1.5*RIGHT + 1.5*UP, UP).shift(offset)
        linear_5 = MTex(r"\binom{x}{y}\to\binom{9x+20y}{4x+9y}", tex_to_color_map = {(r"x", r"y", r"9", r"20", r"4"): YELLOW}).scale(0.8).next_to(3*RIGHT + 4*DOWN, UP).shift(offset).set_stroke(width = 10, color = "#222222", background = True)
        line_ad = Line(positions_5[0], positions_5[3]).shift(offset).set_color(YELLOW)
        line_bc = Line(positions_5[1], positions_5[2]).shift(offset).set_color(YELLOW)
        all_right = VGroup(hyperbola_5, line_ad, line_bc, *dots_5, function_5, *labels_5).set_stroke(background = True)
        self.add(board_right, all_right, self.notice.set_stroke(width = 0)).play(shade.animate.set_opacity(1), board_right.shift(8*RIGHT).animate.shift(8*LEFT), all_right.shift(8*RIGHT).animate.shift(8*LEFT), rate_func = rush_from, run_time = 2)
        self.wait(2, 4) #或者是在x^2-5y^2=1上面作平行线
        self.play(ShowCreationThenDestructionAround(labels_2[3]), ShowCreationThenDestructionAround(labels_5[3]), run_time = 2)
        self.wait(1+0-2, 23+17) #得到的点也会是整点 （空闲）

        self.play(Write(linear_2), Write(linear_5)) #我们可以用同样的方法
        self.wait(2, 18) #说明它们上面的整点都是均匀的
        self.wait(0, 22) #（空闲）

        board = Rectangle(height = 8.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 8.4, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        tex_1 = MTex(r"k=k_{CD}=k_{AB}=\frac{y_B-y_A}{x_B-x_A}").scale(0.5).next_to(1.5*LEFT + 3*UP)
        tex_2 = MTex(r"\begin{cases}y-y_C = k_{CD}(x-x_C)\\x^2-dy^2=1\end{cases}", isolate = r"=", tex_to_color_map = {r"d": BLUE}).scale(0.5).next_to(1.5*LEFT + 2*UP)
        tex_3 = MTex(r"x^2-\frac{2dk(-kx_C+y_C)}{1-dk^2}x-\frac{d(-kx_C+y_C)^2+1}{1-dk^2}=0", tex_to_color_map = {r"d": BLUE}).scale(0.5).next_to(2.5*LEFT + UP, buff = 0)
        tex_4 = MTex(r"x_C+x_D = \frac{2dk(-kx_C+y_C)}{1-dk^2}", isolate = r"=", tex_to_color_map = {r"d": BLUE}).scale(0.5).next_to(1.5*LEFT)
        tex_5 = MTex(r"x_D=\frac{(-1-dk^2)x_C+2dky_C}{1-dk^2}", isolate = r"=", tex_to_color_map = {r"d": BLUE}).scale(0.5).set_y(-1)
        tex_5.set_x(tex_4.get_part_by_tex(r"=").get_x() - tex_5.get_part_by_tex(r"=").get_x())
        tex_6 = MTex(r"x_D=(x_Ax_B+dy_Ay_B)x_C -d(x_Ay_B+x_By_A)y_C", isolate = r"=", tex_to_color_map = {r"d": BLUE}).scale(0.5).next_to(2.5*LEFT + 2*DOWN, buff = 0)
        tex_7 = MTex(r"y_D=(x_Ay_B+x_By_A)x_C -(x_Ax_B+dy_Ay_B)y_C", isolate = r"=", tex_to_color_map = {r"d": BLUE}).scale(0.5).set_y(-2.5)
        tex_7.set_x(tex_6.get_part_by_tex(r"=").get_x() - tex_7.get_part_by_tex(r"=").get_x())
        all = VGroup(board, inner, tex_1, tex_2, tex_3, tex_4, tex_5, tex_6, tex_7)
        surr = SurroundingRectangle(VGroup(tex_6, tex_7))
        self.add(shade, self.notice, all).play(FadeIn(shade), all.shift(9*UP).animating(rate_func = rush_from).shift(9*DOWN), run_time = 2)
        self.clear().add(shade, self.notice.set_stroke(width = 8), all).play(ShowCreation(surr))
        self.wait(1, 18) #事实上 这个证明适用于所有等式右端是1的双曲线
        self.wait(0, 18) #（空闲）

        self.play(self.change_notice())
        self.wait(1, 15) #那么自然会有另外一个问题
        self.play(*[FadeOut(mob, 0.3*DOWN) for mob in [tex_3, tex_4, tex_5, tex_6, tex_7, surr, tex_2[-1]]])
        self.wait(1, 0) #如果等式右端不是1......
        tex_8 = MTex(r"x^2-dy^2=m", isolate = r"=", tex_to_color_map = {r"m": RED}).scale(0.5)
        tex_8.shift(tex_2.get_parts_by_tex(r"=")[1].get_center() - tex_8.get_part_by_tex(r"=").get_center())
        self.play(FadeIn(tex_8[-1], 0.3*UP))
        self.wait(0, 9) #......而是别的数
        tex_9 = MTexText(r"$A, B, C$是双曲线$x^2-dy^2=m$上的三个整点，\\过$C$作$AB$的平行线，再次交双曲线于$D$，\\则$D$也是整点吗？", tex_to_color_map = {r"d": BLUE, r"m": RED}).scale(0.6).next_to(UP, DOWN)
        surr_2 = SurroundingRectangle(tex_9, buff = 0.3, fill_color = BLACK, fill_opacity = 1).add(tex_9)
        self.play(FadeIn(surr_2, 0.5*UP))
        all.remove(tex_3, tex_4, tex_5, tex_6, tex_7, surr).add(surr_2)
        tex_2.remove(tex_2[-1]).add(tex_8[-1])
        self.wait(0, 20) #那这个性质还成立吗
        self.wait(0, 23) #（空闲）

        self.play(self.change_notice())
        self.wait(0, 20) #当然不成立

        ratio = 0.8
        axes = VGroup(Line(4*DOWN, 4*UP), Line(64/9*LEFT, 64/9*RIGHT), MTex(r"x").scale(0.75).next_to(RIGHT_SIDE, UL, buff = 0.1), MTex(r"y").scale(0.75).next_to(TOP, DL, buff = 0.1))
        positions = [np.array([5, -3, 0])*ratio, np.array([3, -1, 0])*ratio, np.array([3, 1, 0])*ratio, np.array([5, 3, 0])*ratio, np.array([-5, -3, 0])*ratio, np.array([-3, 1, 0])*ratio, np.array([-3, -1, 0])*ratio, np.array([-5, 3, 0])*ratio, np.array([19/7, 3/7, 0])*ratio]
        dots = [Dot(position, color = BLUE) for position in positions]
        hyperbola = VGroup(ParametricCurve(lambda t: ratio*np.sqrt(7)*np.array([np.cosh(t), np.sinh(t)/np.sqrt(2), 0]), [np.arcsinh(-6), np.arcsinh(6), 0.01]), ParametricCurve(lambda t: -ratio*np.sqrt(7)*np.array([np.cosh(t), np.sinh(t)/np.sqrt(2), 0]), [np.arcsinh(-6), np.arcsinh(6), 0.01])).set_stroke(color = BLUE, width = 3)
        function_7 = MTex(r"x^2-{2}y^2=7", tex_to_color_map = {r"7": RED, r"{2}": BLUE}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).next_to(5*RIGHT + 0.5*UP, UP)
        labels = [MTex(r"(3, 1)", color = BLUE).scale(0.6).next_to(dots[2], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(3, -1)", color = BLUE).scale(0.6).next_to(dots[1], DL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(5, 3)", color = BLUE).scale(0.6).next_to(dots[3], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True), MTex(r"(\frac{19}{7}, \frac{3}{7})", color = BLUE).scale(0.6).next_to(dots[-1], LEFT, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)]
        self.add(axes, hyperbola, function_7, *dots[:-1], shade, all, self.notice).play(all.animating(remover  = True, rate_func = rush_into).shift(9*UP), FadeOut(shade), run_time = 2)
        self.wait(2, 13) #比如说 在x^2-2y^2=7这条双曲线上
        self.wait(0, 26) #我们能找到......
        self.play(Write(labels[0]), Flash(positions[2]))
        self.wait(0, 9) #......(3, 1)......
        self.play(Write(labels[1]), Flash(positions[1]))
        self.wait(0, 13) #......(3, -1)......
        self.play(Write(labels[2]), Flash(positions[3]))
        self.wait(0, 26) #......(5, 3)这三个整数点
        self.wait(0, 21) #（空闲）

        line_ad = Line(positions[1], positions[3], color = YELLOW)
        line_bc = Line(positions[2], positions[-1], color = YELLOW)
        self.add(line_ad, *dots[:-1]).play(ShowCreation(line_ad))
        self.wait(2, 4) #我们连接(3, -1)和(5, 3)
        self.add(line_bc, *dots[:-1]).play(ShowCreation(line_bc))
        self.play(ShowCreation(dots[-1]))
        self.wait(0, 19) #再过(3, 1)作它的平行线
        self.play(Write(labels[3]), Flash(positions[-1]))
        self.wait(2, 23) #会再和双曲线交到(19/7, 3/7)这个点上
        self.wait(0, 23) #（空闲）

        board = Rectangle(height = 8.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 8.4, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board.add(inner).next_to(LEFT, LEFT, buff = 0.1)
        color_map = {(r"{2}", r"4"): BLUE, r"7": RED}
        tex_1 = MTex(r"k=k_{CD}=k_{AB}=\frac{y_B-y_A}{x_B-x_A}").scale(0.5).next_to(6*LEFT + 3.5*UP)
        tex_2 = MTex(r"\begin{cases}y-y_C = k_{CD}(x-x_C)\\x^2-{2}y^2=7\end{cases}", tex_to_color_map = color_map).scale(0.5).next_to(6*LEFT + 2.5*UP)
        tex_3 = MTex(r"x^2-\frac{4k(-kx_C+y_C)}{1-{2}k^2}x-\frac{{2}(-kx_C+y_C)^2+7}{1-{2}k^2}=0", tex_to_color_map = color_map).scale(0.5).next_to(7*LEFT + 1.5*UP, buff = 0)
        tex_4 = MTex(r"x_C+x_D = \frac{4k(-kx_C+y_C)}{1-{2}k^2}", isolate = r"=", tex_to_color_map = color_map).scale(0.5).next_to(6*LEFT + 0.5*UP)
        tex_5 = MTex(r"x_D=\frac{(-1-{2}k^2)x_C+4ky_C}{1-{2}k^2}", isolate = r"=", tex_to_color_map = color_map).scale(0.5).set_y(-0.5)
        tex_5.set_x(tex_4.get_part_by_tex(r"=").get_x() - tex_5.get_part_by_tex(r"=").get_x())
        tex_6 = MTex(r"x_D=\frac{(x_Ax_B+{2}y_Ay_B)x_C -{2}(x_Ay_B+x_By_A)y_C}{7}", isolate = r"=", tex_to_color_map = color_map).scale(0.5).next_to(7*LEFT + 1.5*DOWN)
        tex_7 = MTex(r"y_D=\frac{(x_Ay_B+x_By_A)x_C -(x_Ax_B+{2}y_Ay_B)y_C}{7}", isolate = r"=", tex_to_color_map = color_map).scale(0.5).set_y(-2.5)
        tex_7.set_x(tex_6.get_part_by_tex(r"=").get_x() - tex_7.get_part_by_tex(r"=").get_x())
        board.add(tex_1, tex_2, tex_3, tex_4, tex_5, tex_6, tex_7).shift(6.5*LEFT).remove(inner, tex_1, tex_2, tex_3, tex_4, tex_5, tex_6, tex_7)
        board_all = [board, inner, tex_1, tex_2, tex_3, tex_4, tex_5, tex_6, tex_7]
        shade_copy = self.shade.copy().set_opacity(0.5)
        self.add(shade_copy, self.notice).play(FadeIn(shade_copy), *[mob.animating(rate_func = rush_from).shift(6.5*RIGHT) for mob in board_all])
        self.wait(2, 15) #我们先前的证明 会在这条双曲线上失效
        self.wait(0, 21) #（空闲）

        surr_x = SurroundingRectangle(tex_6[3:])
        surr_y = SurroundingRectangle(tex_7[3:])
        self.play(ShowCreation(surr_x), ShowCreation(surr_y))
        self.wait(3, 11) #根据计算结果 新交出来的点坐标包含了除法
        self.wait(1, 27) #不再一定是整数
        self.wait(1, 7) #我们只能保证
        self.wait(2, 19) #新交出来的点 一定是有理数
        self.wait(1, 0) #（空闲）

        self.play(self.change_notice())
        self.wait(1, 17) #具体的计算过程 我们一样不用管
        self.wait(0, 18) #（空闲）
        self.play(FadeOut(surr_x), FadeOut(surr_y))
        self.wait(1, 12) #我们只需要注意到这么一件事情
        self.wait(2, 27) #整个计算过程 只出现了加减乘除
        self.wait(0, 25) #（空闲）

        surr_1 = SurroundingRectangle(tex_1)
        surr_2 = SurroundingRectangle(tex_2)
        surr_3 = SurroundingRectangle(tex_3)
        surr_4 = SurroundingRectangle(tex_4[0:2])
        surr_5 = SurroundingRectangle(tex_5)
        self.play(ShowCreation(surr_1))
        self.wait(1, 3) #两个整数点之间的连线
        self.wait(2, 11) #斜率是整数除以整数
        self.wait(1, 27) #自然是有理数
        self.play(FadeOut(surr_1), ShowCreation(surr_2))
        self.wait(1, 4) #把直线和双曲线联立
        self.play(ShowCreation(surr_3))
        self.wait(1, 7) #会得到一个一元二次方程
        self.wait(2, 20) #方程的系数也都是有理数
        self.play(FadeOut(surr_2), FadeOut(surr_3), ShowCreation(surr_4))
        self.wait(1, 11) #这个方程的一个根是有理数
        self.play(ShowCreation(surr_5))
        self.wait(0, 11) #根据韦达定理
        self.wait(2, 7) #另外一个根自然也是有理数
        self.wait(0, 21) #（空闲）
        self.play(FadeOut(surr_4), FadeOut(surr_5))
        self.wait(2, 1) #只进行定性分析 不做任何具体计算
        self.wait(1, 16) #就可以得到这个结论了
        self.wait(1, 2) #（空闲）

        self.play(*[mob.animating(rate_func = rush_into, remover = True).shift(6.5*LEFT) for mob in board_all], FadeOut(shade_copy))
        self.wait(0, 20) #对于一般的双曲线
        self.play(Flash(positions[-1]))
        self.wait(1, 8) #做平行线只能保证得到有理点
        self.wait(0, 18) #（空闲）
        self.play(self.change_notice())
        self.wait(1, 21) #而如果我们的目标只能是有理点
        self.play(*[FadeOut(mob) for mob in labels + [function_7]], Uncreate(line_ad))
        function_m = MTex(r"x^2-dy^2=m", tex_to_color_map = {r"d": BLUE, r"m": RED}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).next_to(5*RIGHT + 0.5*UP, UP)
        self.play(*[FadeOut(mob) for mob in dots[0:2] + dots[3:-1]], FadeIn(function_m))
        self.wait(0, 5) #那么平行线就显得有点没必要了
        self.wait(0, 24) #（空闲）

        label_1 = MTex(r"(x_0, y_0)\in \mathbb{Q}^2", color = BLUE).scale(0.6).next_to(dots[2], UL, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)
        self.play(Flash(positions[2]), Write(label_1))
        self.wait(1, 11) #过双曲线上任意一个有理点

        alpha = ValueTracker(np.arccosh(19/7/np.sqrt(7)))
        def dot_updater(mob: Dot):
            angle = alpha.get_value()
            mob.move_to(ratio*np.sqrt(7)*np.array([np.cosh(angle), np.sinh(angle)/np.sqrt(2), 0]))
        def line_updater(mob: Line):
            angle = alpha.get_value()
            mob.put_start_and_end_on(positions[2], ratio*np.sqrt(7)*np.array([np.cosh(angle), np.sinh(angle)/np.sqrt(2), 0]))
        dots[-1].add_updater(dot_updater)
        line_bc.add_updater(line_updater)
        self.play(alpha.animate.set_value(np.arcsinh(-29/7/np.sqrt(7))))
        dots[-1].clear_updaters()
        line_bc.clear_updaters()
        label_2 = MTex(r"(x_1, y_1)", color = BLUE).scale(0.6).next_to(dots[-1], UR, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)
        label_3 = MTex(r"k\in \mathbb{Q}", color = YELLOW).scale(0.6).next_to(line_bc.get_center(), UR, buff = 0.1).set_stroke(width = 10, color = BACK, background = True)
        self.play(Write(label_2), Write(label_3))
        self.wait(0, 24) #作任意一条有理数斜率的直线

        board.add(inner).next_to(LEFT, LEFT, buff = 0.1)
        color_map = {r"d": BLUE, r"m": RED, r"k": YELLOW}
        tex_1 = MTex(r"\begin{cases}y-y_0 = k(x-x_0)\\x^2-dy^2=m\end{cases}", tex_to_color_map = color_map).scale(0.5).next_to(6*LEFT + 3*UP)
        tex_2 = MTex(r"x^2-\frac{2dk(-kx_0+y_0)}{1-dk^2}x-\frac{d(-kx_0+y_0)^2+m}{1-dk^2}=0", tex_to_color_map = color_map).scale(0.5).next_to(7*LEFT + 2*UP, buff = 0)
        tex_3 = MTex(r"x_0+x_1 = \frac{2dk(-kx_0+y_0)}{1-dk^2}", isolate = r"=", tex_to_color_map = color_map).scale(0.5).next_to(6*LEFT + UP)
        tex_4 = MTex(r"x_1=\frac{(-1-dk^2)x_0+2dky_0}{1-dk^2}", isolate = r"=", tex_to_color_map = color_map).scale(0.5).set_y(0)
        tex_4.set_x(tex_3.get_part_by_tex(r"=").get_x() - tex_4.get_part_by_tex(r"=").get_x())
        tex_5 = MTex(r"y_1=\frac{-2kx_0+(1+dk^2)y_0}{1-dk^2}", isolate = r"=", tex_to_color_map = color_map).scale(0.5).set_y(-1)
        tex_5.set_x(tex_4[2].get_x() - tex_5[2].get_x())
        board.add(tex_1, tex_2).shift(6.5*LEFT).remove(inner, tex_1, tex_2)
        surr_2 = SurroundingRectangle(tex_2)
        shade_copy = self.shade.copy().set_opacity(0.5)
        self.add(shade_copy, self.notice).play(FadeIn(shade_copy), *[mob.animating(rate_func = rush_from).shift(6.5*RIGHT) for mob in [board, inner, tex_1, tex_2]], self.change_notice())
        self.play(ShowCreation(surr_2))
        self.wait(0, 16) #我们都能得到一个有理系数的二次方程
        self.wait(0, 19) #（空闲）

        self.play(FadeOut(surr_2), FadeIn(tex_3, 0.5*UP))
        self.wait(0, 20) #进而通过韦达定理
        self.play(FadeIn(tex_4, 0.5*UP), FadeIn(tex_5, 0.5*UP))
        self.wait(0, 7) #得到另一个有理点
        self.wait(0, 21) #（空闲）
        self.wait(2, 16) #虽然说计算过程很复杂
        self.wait(2, 0) #但我们其实完全不用管它
        self.wait(0, 21) #（空闲）
        surr_3 = SurroundingRectangle(tex_3)
        surr = SurroundingRectangle(VGroup(tex_4, tex_5))
        self.play(ShowCreation(surr_3))
        self.wait(1, 26) #只要每一步计算都只有加减乘除
        self.play(FadeOut(surr_3), ShowCreation(surr))
        self.wait(1, 7) #最后的结果就一定是有理的
        self.wait(0, 26) #（空闲）

        self.fade_out(change_notice = True)
        axes = VGroup(Arrow(2.5*LEFT, 2.5*RIGHT, buff = 0), Arrow(2.5*DOWN, 2.5*UP, buff = 0), MTex(r"x").scale(0.8).next_to(2.5*RIGHT, RIGHT), MTex(r"y").scale(0.8).next_to(2.5*UP, UP))
        circle = Circle(radius = 2, color = BLUE)
        label_0 = MTex(r"x^2+y^2=1", color = BLUE).next_to(2*DOWN, DL)
        self.fade_in(axes, circle, label_0)
        self.wait(1+1-2, 20+25) #作为一个有趣的例子 我想请大家看一看单位圆
        self.wait(0, 21) #（空闲）

        positions = [2*LEFT, 2*RIGHT, 2*UP, 2*DOWN]
        dots = [Dot(position, color = BLUE) for position in positions]
        label_1 = MTex(r"A(-1, 0)", tex_to_color_map = {r"A": BLUE}).scale(0.6).next_to(dots[0], UL, buff = 0.15)
        line = Line(2*LEFT, 2*unit(PI/3), color = YELLOW)
        dot_2 = Dot(2*unit(PI/3), color = BLUE)
        label_2 = MTex(r"B\left(\frac{1-k^2}{1+k^2}, \frac{2k}{1+k^2}\right)", tex_to_color_map = {r"B": BLUE, r"k": YELLOW}).scale(0.6).next_to(dot_2, UR, buff = 0.15)
        label_3 = MTex(r"k", color = YELLOW).scale(0.6).next_to(line.get_center(), DR, buff = 0.1)
        self.play(*[GrowFromCenter(dot) for dot in dots], *[Flash(position) for position in positions])
        self.wait(1, 6) #单位圆上有四个整点
        self.play(Write(label_1))
        self.wait(2, 1) #我们过它的左端点(-1, 0)
        self.add(line, dots[0]).play(ShowCreation(line))
        self.play(Write(label_3), ShowCreation(dot_2))
        self.wait(1, 0) #做一条斜率为有理数k的直线
        self.play(Flash(2*unit(PI/3)))
        self.wait(0, 23) #和单位圆再次交于一点
        self.wait(0, 22) #（空闲）

        self.play(Write(label_2))
        self.wait(1+2-2, 22+16) #这一点的横纵坐标 正好就是cos和sin的万能公式
        self.wait(0, 26) #（空闲）

        frac_1 = MTex(r"k=\frac{m}{n}", tex_to_color_map = {(r"k", r"m", r"n"): YELLOW}).scale(0.8).shift(2.5*UP + 3.5*RIGHT)
        frac_2 = MTex(r"B\left(\frac{n^2-m^2}{n^2+m^2}, \frac{2mn}{n^2+m^2}\right)", tex_to_color_map = {r"B": BLUE, (r"m", r"n"): YELLOW}).scale(0.8).shift(UP + 3.5*RIGHT)
        self.play(*[mob.animate.shift(3*LEFT) for mob in [axes, circle, *dots, line, dot_2, label_0, label_1, label_2, label_3]])
        self.play(Write(frac_1))
        self.wait(0, 23) #而如果我们用m/n表示k
        self.play(FadeIn(frac_2, 0.5*UP))
        self.wait(1, 12) #那么这个点的横纵坐标会变成这样
        self.wait(0, 27) #（空闲）

        formula_1 = MTex(r"\left(\frac{n^2-m^2}{n^2+m^2}\right)^2+\left(\frac{2mn}{n^2+m^2}\right)^2=1", tex_to_color_map = {(r"m", r"n"): YELLOW}).scale(0.6).shift(0.5*DOWN + 3.5*RIGHT)
        formula_2 = MTex(r"(n^2-m^2)^2+(2mn)^2=(n^2+m^2)^2", tex_to_color_map = {(r"m", r"n"): YELLOW}).scale(0.8).shift(2*DOWN + 3.5*RIGHT)
        surr = SurroundingRectangle(formula_2)
        self.play(FadeIn(formula_1, 0.5*UP))
        self.wait(2, 11) #把它们带进单位圆的方程 并通分
        self.play(FadeIn(formula_2, 0.5*UP))
        self.play(ShowCreation(surr))
        self.wait(0, 14) #我们就能得到勾股数的参数表示法
        self.wait(0, 22) #（空闲）
        self.wait(1, 28) #每一组互素的m和n
        self.wait(2, 4) #都会对应一组互素的勾股数
        self.wait(2, 11)
        self.fade_out(end = True)
        self.wait(2, 0) #到此共184秒

#################################################################### 

class Summary(FrameScene):

    def construct(self):
        self.notices = [Notice("良心视频", "请　三连"), 
                        Notice("下期预告", "敬请期待"), 
                        Notice("良心up主", "请　关注")]
        self.notice = self.notices[0]

        self.play(Write(self.notice))
        self.wait(0, 26) #非常感谢大家能看到这里
        self.wait(0, 20) #（空闲）

        title = Title(r"（广义）佩尔方程")
        title_line = TitleLine()
        color_map = {r"d": BLUE, r"m": RED}
        function = MTex(r"x^2-dy^2=m", tex_to_color_map = color_map)
        notice = MTexText(r"（$d$为非平方数，$m\ne 0$）", tex_to_color_map = color_map).scale(0.6).next_to(function, DOWN)
        function.add(notice).move_to(1.5*UP)
        self.play(FadeIn(function, 0.5*UP), Write(title), GrowFromCenter(title_line))
        self.wait(1, 23) #这期视频的主题 佩尔方程
        self.wait(1, 27) #是一个很有意思的数学话题
        self.wait(0, 19) #（空闲）
        
        positive = MTex(r"x^2-dy^2=1", tex_to_color_map = {r"d": BLUE, r"1": RED})
        notice = MTexText(r"对所有非平方数$d$均有解", tex_to_color_map = color_map).scale(0.6).next_to(positive, DOWN)
        positive.add(notice).next_to(0.5*UP + 3*LEFT, DOWN)
        negative = MTex(r"x^2-dy^2=-1", tex_to_color_map = {r"d": BLUE, r"-1": RED})
        notice = MTexText(r"$d=p=4k+1$有解\\$d=p=4k+3$无解\\$\cdots$", tex_to_color_map = {r"d": BLUE, r"p": PURPLE_A}).scale(0.6).next_to(negative, DOWN)
        negative.add(notice).next_to(0.5*UP + 3*RIGHT, DOWN)
        self.play(FadeIn(positive))
        self.wait(3, 4) #比如说 所有m=1的佩尔方程都是有解的
        self.play(FadeIn(negative))
        self.wait(1, 20) #而m=-1的佩尔方程则不一定
        self.wait(0, 23) #（空闲）

        ratio = 2/3
        lines_h = VGroup(*[Line(30*LEFT + i*ratio*UP, 30*RIGHT + i*ratio*UP) for i in range(-25, 25)]).set_stroke(width = 1, color = RED_A)
        lines_v = VGroup(*[Line(16*DOWN + i*ratio*RIGHT, 16*UP + i*ratio*RIGHT) for i in range(-40, 40)]).set_stroke(width = 1, color = RED_A)
        axes = VGroup(Line(4*DOWN, 4*UP), Line(64/9*LEFT, 64/9*RIGHT), MTex(r"x").scale(0.75).next_to(RIGHT_SIDE, UL, buff = 0.1), MTex(r"y").scale(0.75).next_to(TOP, DL, buff = 0.1))
        trans_positions_p = [np.array([26, -15, 0])*ratio, np.array([7, -4, 0])*ratio, np.array([2, -1, 0])*ratio, np.array([1, 0, 0])*ratio, np.array([2, 1, 0])*ratio, np.array([7, 4, 0])*ratio, np.array([26, 15, 0])*ratio]
        trans_dots_1 = [Dot(position, color = BLUE) for position in trans_positions_p[:-1]]
        trans_dots_2 = [Dot(-position, color = BLUE) for position in trans_positions_p[:-1]]
        hyperbola_p = VGroup(ParametricCurve(lambda t: ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-40), np.arcsinh(40), 0.01]), ParametricCurve(lambda t: -ratio*np.array([np.cosh(t), np.sinh(t)/np.sqrt(3), 0]), [np.arcsinh(-40), np.arcsinh(40), 0.01])).set_stroke(color = BLUE, width = 3)
        function_p = MTex(r"x^2-{3}y^2=1", tex_to_color_map = {(r"x", r"y", r"1"): BLUE, r"{3}": TEAL}).set_stroke(width = 10, color = BACK, background = True).scale(0.8).next_to(3*RIGHT, UP)
        self.fade_out(run_time = 0.5).fade_in(lines_h, lines_v, axes, hyperbola_p, *trans_dots_1, *trans_dots_2, function_p, run_time = 0.5)
        self.wait(0, 12) #我尽量用图来说明了......
        background = VGroup(lines_h.copy(), lines_v.copy(), hyperbola_p.copy()).set_stroke(width = 1, color = GREY).add(*[dot.copy().set_color(GREY) for dot in trans_dots_1 + trans_dots_2])
        trans = lambda t: np.array([2*t[0]+3*t[1], t[0]+2*t[1], 0])
        self.bring_to_back(background).play(*[mob.animate.apply_function(trans, about_point = ORIGIN) for mob in [lines_h, lines_v, hyperbola_p]], 
                                            *[trans_dots_1[i].animate.move_to(trans_positions_p[i+1]) for i in range(6)], *[trans_dots_2[i].animate.move_to(-trans_positions_p[i+1]) for i in range(6)], run_time = 3)
        self.play(background.set_submobjects(background.submobjects[0:2].copy()).animate.set_stroke(width = 1, color = RED_A), FadeOut(lines_h), FadeOut(lines_v))
        self.wait(2+0+2-5, 28+21+28) #......双曲线上整点的寻找过程（空闲） 这种从已知点生成其它点的方式
        self.wait(1, 20) #在数学中很是常见
        self.wait(0, 17) #（空闲）

        self.fade_out(run_time = 0.5)
        ratio = 1/5
        offset = 0.5*DOWN
        curve = FunctionGraph(lambda x: np.cbrt(1141-x**3), [-30, 30, 0.1], color = BLUE).scale(ratio, about_point = ORIGIN).shift(offset)
        positions = [np.array([-19, 20, 0])*ratio, np.array([-38120/4953, 57893/4953, 0])*ratio, np.array([74451906469/7115358260, -11842954469/7115358260, 0])*ratio]
        dots = [Dot(position, color = BLUE).shift(offset) for position in positions]
        label = MTex(r"x^3+y^3=1141", color = BLUE).scale(0.8).next_to(np.cbrt(1141/2)*ratio*UR, UR).shift(offset)
        labels = [MTex(r"\left(-19, 20\right)").scale(0.6).next_to(dots[0], LEFT), MTex(r"\left(-\frac{38120}{4953}, \frac{57893}{4953}\right)").scale(0.6).next_to(dots[1], UR), MTex(r"\left(\frac{74451906469}{7115358260}, -\frac{11842954469}{7115358260}\right)").scale(0.6).next_to(dots[2], RIGHT)]
        line = Line(positions[0], positions[2], color = YELLOW).shift(offset)
        self.fade_in(curve, label, dots[0], dots[1], labels[0], labels[1], run_time = 0.5)
        self.wait(0, 3) #比如说......
        self.play(Flash(positions[0] + offset))
        self.play(Flash(positions[1] + offset))
        self.wait(1, 4) #......我们如果知道了三次曲线上的两个有理点
        self.add(line, dots[0], dots[1]).play(ShowCreation(line))
        self.play(ShowCreation(dots[2]), Flash(positions[2] + offset), Write(labels[2]))
        self.wait(2+1-3, 7+8) #就能过它们连一条直线 得到第三个有理点
        self.wait(0, 23) #（空闲）

        board = Rectangle(height = 8.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 8.4, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board.add(inner).next_to(ORIGIN, LEFT, buff = 0.1)
        tex_1 = MTex(r"k=\frac{y_2-y_1}{x_2-x_1}").scale(0.5).next_to(5*LEFT + 3*UP)
        tex_2 = MTex(r"\begin{cases}y-y_1 = k(x-x_1)\\x^3+y^3=d\end{cases}").scale(0.5).next_to(5*LEFT + 2*UP)
        tex_3 = MTex(r"(x_2-x_1)^3x^3+((y_2-y_1)x+(x_2y_1-x_1y_2))^3=d(x_2-x_1)^3").scale(0.5).next_to(7*LEFT + UP, buff = 0)
        tex_4 = MTex(r"x_1+x_2+x_3 = \frac{3(y_2-y_1)^2(x_1y_2-x_2y_1)}{(x_2-x_1)^3+(y_2-y_1)^3}").scale(0.5).next_to(6*LEFT)
        tex_5 = MTex(r"x_3=\frac{d(x_2-x_1)+y_1y_2(x_1y_2-x_2y_1)}{x_1x_2(x_2-x_1)+y_1y_2(y_2-y_1)}", isolate = r"=").scale(0.5).next_to(6*LEFT + DOWN, buff = 0)
        tex_6 = MTex(r"y_3=\frac{d(y_2-y_1)+x_1x_2(y_1x_2-y_2x_1)}{x_1x_2(x_2-x_1)+y_1y_2(y_2-y_1)}", isolate = r"=").scale(0.5).set_y(-2)
        tex_6.set_x(tex_5.get_part_by_tex(r"=").get_x() - tex_6.get_part_by_tex(r"=").get_x())
        board.add(tex_1, tex_2, tex_3, tex_4, tex_5, tex_6).shift(6.5*LEFT).remove(inner, tex_1, tex_2, tex_3, tex_4, tex_5, tex_6)
        board_all = [board, inner, tex_1, tex_2, tex_3, tex_4, tex_5, tex_6]
        shade_copy = self.shade.copy().set_opacity(0.5)
        self.add(shade_copy, self.notice).play(FadeIn(shade_copy), *[mob.animating(rate_func = rush_from).shift(6.5*RIGHT) for mob in board_all])
        self.wait(2, 5) #三次曲线的计算过程比二次曲线会更加复杂
        self.wait(0, 19) #（空闲）
        self.wait(2, 2) #但我们不需要去管具体的步骤
        self.wait(0, 20) #（空闲）
        self.wait(2, 17) #每一步计算都只是加减乘除
        self.wait(2, 1) #最后的结果一定是有理的
        self.wait(0, 24) #（空闲）

        self.clear().add(self.notice)
        like = Text("", font = 'vanfont').scale(2).shift(3*LEFT)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').scale(2).shift(3*RIGHT)
        sanlian = VGroup(like, coin, star)
        self.play(*[GrowFromCenter(mob) for mob in sanlian])
        self.play(ApplyMethod(sanlian.set_color, "#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian])
        self.wait(0, 17) #如果这期视频带给你了这样的收获
        self.wait(1, 25) #不妨一键三连支持一下
        self.wait(1, 5) #（空闲）
        
        def curvy_squish(point):
            x, y, z = point
            return (x+np.cos(y))*RIGHT + (y+np.sin(x))*UP
        ratio = 1/2
        lines_h = VGroup(*[Line(10*LEFT + i*ratio*UP, 10*RIGHT + i*ratio*UP).insert_n_curves(79) for i in range(-10, 10)]).set_stroke(width = 2, color = BLUE)
        lines_v = VGroup(*[Line(5*DOWN + i*ratio*RIGHT, 5*UP + i*ratio*RIGHT).insert_n_curves(79) for i in range(-20, 20)]).set_stroke(width = 2, color = BLUE)
        self.add(lines_h, lines_v, self.notice).play(FadeOut(sanlian, run_time = 0.5), FadeIn(lines_h, rate_func = squish_rate_func(smooth, 0.5, 1)), FadeIn(lines_v, rate_func = squish_rate_func(smooth, 0.5, 1)), self.change_notice())
        self.play(lines_h.animate.apply_function(curvy_squish), lines_v.animate.apply_function(curvy_squish), run_time = 1.5)
        self.wait(2+0-2, 9+19-15) #下期视频我打算讲一讲弯曲空间 （空闲）
        self.wait(2, 29) #大家可能会从各个地方接触到这个概念

        board_left = Rectangle(height = 8.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = YELLOW_E)
        inner = Rectangle(height = 8.4, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = WHITE)
        board_left.add(inner).next_to(0.1*RIGHT, LEFT, buff = 0)
        ratio = 0.7
        lines_l = VGroup(*[Line(LEFT_SIDE + 2*DOWN + i*ratio*UP, 2*UP + i*ratio*UP).insert_n_curves(79) for i in range(-10, 10)]).set_stroke(width = 2)
        lines_r = VGroup(*[Line(LEFT_SIDE + 2*UP + i*ratio*UP, 2*DOWN + i*ratio*UP).insert_n_curves(79) for i in range(-10, 10)]).set_stroke(width = 2)
        func = lambda t: t + np.exp(-0.25*get_norm(t-LEFT_SIDE/2)**2)*1.2*DOWN
        lines_l.apply_function(func)
        lines_r.apply_function(func)
        earth = ImageMobject("earth.png", height = 3).shift(LEFT_SIDE/2 + 0.25*DOWN)
        self.add().play(*[mob.shift(8*LEFT).animate.shift(8*RIGHT) for mob in [board_left, lines_l, lines_r, earth]], run_time = 1.5, rate_func = rush_from)
        self.wait(0, 10) #比如说广义相对论

        board_right = Rectangle(height = 8.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 8.4, width = 7.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board_right.add(inner).next_to(0.1*LEFT, RIGHT, buff = 0)
        circle = Circle(radius = 2.5, stroke_width = 8, color = WHITE).shift(RIGHT_SIDE/2)
        poincare = ImageMobject("hyperbolic.png", height = 5).shift(RIGHT_SIDE/2)
        self.add(board_right, poincare, circle, self.notice.set_stroke(width = 0)).play(*[mob.shift(8*RIGHT).animate.shift(8*LEFT) for mob in [board_right, poincare, circle]], run_time = 1.5, rate_func = rush_from)
        self.wait(0, 2) #比如说罗氏几何
        self.wait(0, 18) # （空闲）
        self.wait(2, 11) #虽然这听起来还蛮直观的
        self.wait(3, 0) #但弯曲的空间其实并不怎么好理解
        arrow = Arrow(LEFT_SIDE/2 + 2.5*UP, LEFT_SIDE/2 + 1.5*UP)
        notice = Text(r"比如这个就是错的", font = "simsun").scale(0.6).set_stroke(width = 10, color = "#222222", background = True).next_to(arrow, UP, buff = 0.1).add(arrow)
        self.play(FadeIn(notice, 0.3*DOWN))
        self.wait(1, 11) #一些直观的理解方式很容易出错
        self.wait(0, 24) # （空闲）

        self.wait(2, 22) #在下期视频 我们就来看看
        self.wait(2, 14) #如何恰当地直观理解弯曲空间
        self.wait(0, 3)
        self.fade_out() #（空闲）

        painting = StarrySky()
        star = painting.star
        self.clear().play(FadeIn(painting, lag_ratio = 0.01, run_time = 2), self.change_notice())
        self.wait(0, 4) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, 0.5*UP), FadeIn(text_name, 0.5*UP))
        self.wait(1, 13) #而我 就像我的名字一样

        self.play(FadeOut(painting.others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star.shift, DOWN))
        self.wait(1, 12) #想要把天上的星星垂下来

        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), stroke_color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, stroke_color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star, apple))
        self.wait(1, 9) #变成触手可及的果实

        snowflake = SnowFlake()
        snowflake_2 = snowflake.copy().set_color(RED).set_stroke(width = 1.5)
        snowflake_3 = snowflake.copy().set_color(BLUE).set_stroke(width = 2)
        self.play(star.animate.restore(), 
                  SpreadOut(snowflake_2, rate_func = squish_rate_func(rush_into, 0, 0.9), run_time = 2), 
                  SpreadOut(snowflake_3, rate_func = squish_rate_func(rush_into, 0.05, 0.95), run_time = 2), 
                  SpreadOut(snowflake, rate_func = squish_rate_func(rush_into, 0.1, 1), run_time = 2))
        self.remove(snowflake_2, snowflake_3) 
        self.wait(1+0-2, 29+20) #变成指引前路的火光 （空闲）
        
        self.remove(star, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.wait(2, 1) #我是乐正垂星 我们下期视频再见

        self.wait(4, 22)
        self.fade_out(end = True)
        self.wait(4) #到此共100秒

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]