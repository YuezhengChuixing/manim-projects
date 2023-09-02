from __future__ import annotations

from manimlib import *
import numpy as np

class Cut(Animation):
    def __init__(self, position: np.ndarray = ORIGIN, length: float = 4, **kwargs):
        width = [length*4/2500*i*(100-i) for i in range(50)]
        mobject = Line(position + length/2*UP, position + length/2*DOWN, stroke_width = width + width[::-1]).insert_n_curves(99)
        super().__init__(mobject, **kwargs)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        start, end = starting_submobject.get_start(), starting_submobject.get_end()
        head, tail = interpolate(start, end, alpha*(3-alpha**2)/2), interpolate(start, end, alpha**2*(3-alpha)/2)
        submobject.become(starting_submobject).put_start_and_end_on(head, tail)

class Interval(Polyline):
    def __init__(self, left: np.ndarray, right: np.ndarray, height: float = 0.25, **kwargs):
        super().__init__(left + height * UP, left, right, right + height * UP, **kwargs)

def halve(mob: Interval):
    height = mob.get_height()
    left = mob.get_corner(DL)
    right = mob.get_corner(DR)
    stroke_width = mob.get_stroke_width()
    middle = (left + right)/2
    return Line(middle, middle + height*UP).set_stroke(width = stroke_width), Interval(left, middle, height).set_stroke(width = stroke_width), Interval(middle, right, height).set_stroke(width = stroke_width)

def trisect(mob: Interval):
    height = mob.get_height()
    left = mob.get_corner(DL)
    right = mob.get_corner(DR)
    stroke_width = mob.get_stroke_width()
    m_l = (2*left + right)/3
    m_r = (left + 2*right)/3
    return Line(m_l, m_l + height*UP, stroke_width = stroke_width), Line(m_r, m_r + height*UP, stroke_width = stroke_width), Interval(left, m_l, height, stroke_width = stroke_width), Line(m_l, m_r, stroke_width = stroke_width), Interval(m_r, right, height, stroke_width = stroke_width)

#################################################################### 

class Intro0(FrameScene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("支付自己关于数字的直觉，\n换取自己关于数学的直觉，\n是一笔稳赚不赔的买卖。", font = 'simsun', t2c={"数字": GREEN, "数学": BLUE, "稳赚不赔": YELLOW})
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DR), DOWN)
        ##  Showing object
        self.play(Write(quote), runtime = 2)
        self.play(Write(author), Write(notice0))
        self.wait(2)
        self.play(FadeOut(quote), FadeOut(author))
        self.wait(1)

class Intro1(FrameScene):
    def construct(self):
        self.notices = [Notice("沃茨基·硕德", "请勿模仿"), 
                        Notice("气人操作", "请勿模仿"),
                        Notice("相似操作", "请　思考"),
                        Notice("重要事实", "请　接受"),
                        Notice("关键问题", "请　好奇"),
                        Notice("传统艺能", "请　三连")]
        self.notice = self.notices[0]
        
        wrong = MTex(r"0.\dot9 < 1").scale(2)
        wrong.shift(-wrong[-2].get_y()*UP)
        self.play(self.change_notice(), Write(wrong))
        self.wait(1, 26) #大家应该都知道0.9的循环小于1吧
        self.wait(0, 18) #（空闲）

        induce_1 = MTex(r"0.9<1").scale(1.2).next_to(LEFT + 1.8*UP, LEFT)
        induce_2 = MTex(r"0.99<1").scale(1.2).next_to(LEFT + 0.6*UP, LEFT)
        induce_3 = MTex(r"0.999<1").scale(1.2).next_to(LEFT + 0.6*DOWN, LEFT)
        induce_4 = MTex(r"\vdots").scale(1.2).shift(induce_3[-2].get_center() + 1.2*DOWN)
        infer = MTex(r"\Rightarrow").scale(3)
        self.play(wrong.animate.shift(3*RIGHT), Write(induce_1))
        self.wait(0, 26) #毕竟0.9小于1
        self.play(Write(induce_2))
        self.wait(0, 22) #0.99小于1
        self.play(Write(induce_3))
        self.wait(0, 26) #0.999小于1
        self.play(Write(induce_4), Write(infer))
        self.wait(0, 18) #这样无限递推下去
        self.wait(2, 8) #0.9的循环肯定也小于1
        self.wait(0, 17) #（空闲）

        lie = MTex(r"0<1").scale(1.5).shift(2*UP)
        self.play(*[FadeOut(mob, 1.5*LEFT, rate_func = rush_into)for mob in [induce_1, induce_2, induce_3, induce_4, infer]], wrong.animating(run_time = 2).shift(3*LEFT))
        self.wait(0, 1) #甚至我们都不需要这么干
        self.play(wrong[0].animate.set_color(YELLOW), wrong[-1].animate.set_color(YELLOW), rate_func = there_and_back, run_time = 2/3, frames = 20)
        self.play(wrong[0].animate.set_color(YELLOW), wrong[-1].animate.set_color(YELLOW), run_time = 1/3, frames = 10)
        self.wait(0, 10) #直接看首位
        self.play(Write(lie))
        self.wait(0, 21) #1比0大
        self.play(ShowCreationThenDestructionAround(wrong[-2], run_time = 2))
        self.wait(0, 9) #所以0.9的循环比1小
        self.wait(0, 23) #（空闲）

        crossmark = MTex(r"\times", color = RED).scale(3).move_to(wrong[-2])
        self.wait(1) #是这样吗？
        self.play(wrong[0].animate.set_color(WHITE), wrong[-1].animate.set_color(WHITE), Write(crossmark), FadeOut(lie), self.change_notice())
        self.wait(0+0-1, 25+23) #当然不是 （空闲）

        target = wrong.generate_target().shift(3*UP)
        target[0:4].set_color(BLUE)
        target[5].set_color(GREEN)
        self.add(wrong, crossmark).play(MoveToTarget(wrong), crossmark.animate.shift(3*UP))
        self.wait(1, 8) #用另一种方式可能会更好说明一点
        self.wait(0, 18) #（空闲）

        close_ket = MTex(r"\mathbf]").next_to(ORIGIN, LEFT, buff = 0).set_stroke(width = 4)
        open_ket = MTex(r"\mathbf)").next_to(ORIGIN, LEFT, buff = 0).set_stroke(width = 4)
        interval_1 = MTex(r"(-\infty, 0.9]", tex_to_color_map = {r"0.9": BLUE}).next_to(1.5*UP + LEFT)
        line_1 = Line(6*LEFT, 2.1*LEFT).add(close_ket.copy().shift(2.1*LEFT)).shift(1.5*UP)
        interval_2 = MTex(r"(-\infty, 0.99]", tex_to_color_map = {r"0.99": BLUE}).next_to(0.7*UP + LEFT)
        line_2 = Line(6*LEFT, 2.01*LEFT).add(close_ket.copy().shift(2.01*LEFT)).shift(0.7*UP)
        interval_3 = MTex(r"(-\infty, 0.999]", tex_to_color_map = {r"0.999": BLUE}).next_to(0.1*DOWN + LEFT)
        line_3 = Line(6*LEFT, 2.001*LEFT).add(close_ket.copy().shift(2.001*LEFT)).shift(0.1*DOWN)
        interval_inf = MTex(r"(-\infty, 1) = (-\infty, 0.9]\cup(-\infty, 0.99]\cup(-\infty, 0.999]\cup\cdots", tex_to_color_map = {r"1": GREEN, (r"0.9", r"0.99", r"0.999"): BLUE}).next_to(2*DOWN + LEFT)
        ellipsis = MTex(r"\vdots").shift(4*LEFT + DOWN)
        infer = MTex(r"\to").rotate(-PI/2).shift(interval_1[3].get_x()*RIGHT + DOWN)
        interval_inf[6:].scale(0.6, about_point = interval_inf[5].get_edge_center(RIGHT))
        line_inf = Line(6*LEFT, 2*LEFT).add(open_ket.copy().shift(2*LEFT)).shift(2*DOWN)
        self.play(*[FadeIn(mob, 0.5*DOWN) for mob in [interval_1, line_1]])
        self.wait(2, 2) #我们首先取出不大于0.9的所有实数
        self.play(*[FadeIn(mob, 0.5*DOWN) for mob in [interval_2, line_2]])
        self.wait(1, 3)
        self.play(*[FadeIn(mob, 0.5*DOWN) for mob in [interval_3, line_3]]) #然后取出不大于0.99的所有实数
        self.wait(0, 22)
        self.play(*[FadeIn(mob, 0.5*DOWN) for mob in [ellipsis, infer]]) #再这么一直取下去
        self.wait(0, 27)
        self.play(*[FadeIn(mob, 0.5*DOWN) for mob in [interval_inf[0:6], line_inf]])
        self.play(Write(interval_inf[6:]), run_time = 1) #我们就能取到不大于0.9的循环的实数了
        self.wait(0, 20) #（空闲）
        
        set_compare = MTex(r"(-\infty, 1)\subsetneqq (-\infty, 1]", tex_to_color_map = {r"1": GREEN}).scale(1.5).shift(2*RIGHT + 0.5*UP)
        self.play(*[FadeOut(mob, 2*LEFT, rate_func = rush_into) for mob in [line_1, line_2, line_3, ellipsis, line_inf]], 
                  *[mob.animating(run_time = 2).shift(4*LEFT).fade() for mob in [interval_1, interval_2, interval_3, infer, interval_inf]], 
                  FadeIn(set_compare, 2*LEFT, rate_func = squish_rate_func(rush_from, 0.5, 1), run_time = 2))
        self.wait(1, 14) #这个集合和不大于1的所有实数组成的集合相比
        self.play(Indicate(set_compare[6]))
        self.play(Indicate(set_compare[6]))
        self.wait(1+0-2, 16+16) #确实小了那么一点 （空闲）

        arrow_l = Arrow(0.5*UP, ORIGIN, buff = 0, color = YELLOW).next_to(set_compare[5], UP)
        arrow_r = Arrow(0.5*UP, ORIGIN, buff = 0, color = YELLOW).next_to(set_compare[-1], UP)
        cross_l = VGroup(Line(UL, DR), Line(UR, DL)).set_color(RED).scale(0.25).move_to(arrow_l)
        cross_r = VGroup(Line(UL, DR), Line(UR, DL)).set_color(RED).scale(0.25).move_to(arrow_r)
        kets = MTex(r")<]", tex_to_color_map = {r")": BLUE, r"]": GREEN}).scale(1.5)
        kets[0].move_to(set_compare[5]).shift(DOWN)
        kets[2].move_to(set_compare[-1]).shift(DOWN)
        kets[1].move_to((kets[0].get_center() + kets[2].get_center())/2)
        numbers = MTex(r"1=1", tex_to_color_map = {r"1": GREEN}).scale(1.5)
        numbers[0].move_to(set_compare[4]).shift(DOWN)
        numbers[2].move_to(set_compare[-2]).shift(DOWN)
        numbers[1].move_to((numbers[0].get_center() + numbers[2].get_center())/2)
        offset = numbers[1].get_center() - kets[1].get_center()
        self.play(FadeIn(arrow_l, 0.3*DOWN), FadeIn(arrow_r, 0.3*DOWN), self.change_notice(), FadeIn(kets[1], DOWN), TransformFromCopy(set_compare[5], kets[0]), TransformFromCopy(set_compare[-1], kets[2]))
        self.play(Write(cross_l), Write(cross_r))
        alpha = ValueTracker(1.0)
        cross_l.add_updater(lambda mob: mob.move_to(arrow_l).set_opacity(alpha.get_value()))
        cross_r.add_updater(lambda mob: mob.move_to(arrow_r).set_opacity(alpha.get_value()))
        self.wait(1+2-2, 25+26) #但我们用来比大小的 可不是集合右端是开的还是闭的
        self.play(FadeOut(kets, offset), FadeIn(numbers, offset), arrow_l.animate.next_to(set_compare[4], UP), arrow_r.animate.next_to(set_compare[-2], UP), alpha.animate.set_value(0))
        self.remove(cross_l, cross_r).wait(0, 11) #而是这两个1
        self.wait(0, 24) #（空闲）

        self.play(*[mob.animating(remover = True, rate_func = rush_into, run_time = 0.5).set_opacity(0).shift(LEFT + 0.25*DOWN) for mob in [interval_1, interval_2, interval_3, infer, interval_inf]], 
                  *[mob.animate.shift(2*LEFT + 0.5*DOWN) for mob in [set_compare, arrow_l, arrow_r, numbers]])
        self.wait(0, 20) #这背后的原因是

        line_l = Underline(wrong[0:4], color = YELLOW)
        line_r = Underline(wrong[5], color = YELLOW)
        notice_1 = Simsun(r"只是小数，不是实数", color = YELLOW).scale(0.5).next_to(line_l, DOWN).set_x(line_l.get_x())
        notice_2 = Simsun(r"更像是实数，虽然也不是实数", color = YELLOW).scale(0.5).next_to(arrow_l, UP).set_x(numbers[1].get_x())
        self.play(Write(notice_1), ShowCreation(line_l))
        self.wait(2, 3) #0.9的循环 其实并不是一个实数
        self.wait(0, 16) #（空闲）
        self.play(notice_1.animate.set_x(0), ShowCreation(line_r), Write(notice_2))
        self.wait(1, 3) #甚至1都不是一个实数
        self.wait(0, 19) #（空闲）

        self.wait(2, 3) #它们是两个不同的小数
        self.wait(2, 15) #只是恰好表示了同一个实数而已
        self.wait(0, 19) #（空闲）

        indicate = SurroundingRectangle(numbers).save_state()
        self.play(FadeIn(indicate, remover = True, rate_func = there_and_back))
        self.play(FadeIn(indicate.restore(), remover = True, rate_func = there_and_back))
        self.wait(1, 0) #而等号比较的 是两个实数
        self.wait(0, 22) #（空闲）

        bra = MTex(r"\begin{cases}\\\\\\\\\\\\\end{cases}").set_color(interpolate_color(WHITE, BACK, 0.5))
        ket = bra.copy().scale(np.array([-1, 1, 0]), min_scale_factor = -1)
        bra_l = bra.copy().shift(5*LEFT)
        ket_l = ket.copy().shift(1*LEFT)
        bra_r = bra.copy().shift(1*RIGHT)
        ket_r = ket.copy().shift(5*RIGHT)
        decimal = MTex(r"\mathbb{D}").next_to(3*LEFT + 3*UP, DOWN)
        real = MTex(r"\mathbb{R}").next_to(3*RIGHT + 3*UP, DOWN)
        frame = VGroup(bra_l, ket_l, bra_r, ket_r, decimal, real)
        self.fade_out(run_time = 0.5)
        self.fade_in(frame, run_time = 0.5)

        dec_1 = MTex(r"0.6180339887\cdots").shift(3*LEFT + 1.6*UP)
        dec_2 = MTex(r"0.9999999999\cdots").shift(3*LEFT + 0.8*UP)
        dec_3 = MTex(r"1.0000000000\cdots").shift(3*LEFT)
        dec_4 = MTex(r"2.7182818284\cdots").shift(3*LEFT + 0.8*DOWN)
        dec_5 = MTex(r"3.1415926535\cdots").shift(3*LEFT + 1.6*DOWN)
        decs = [dec_1, dec_2, dec_3, dec_4, dec_5]
        real_1 = MTex(r"\mathrm{\phi}").shift(3*RIGHT + 1.5*UP)
        real_2 = MTex(r"1").shift(3*RIGHT + 0.5*UP)
        real_3 = MTex(r"\mathrm{e}").shift(3*RIGHT + 0.5*DOWN)
        real_4 = MTex(r"\mathrm{\pi}").shift(3*RIGHT + 1.5*DOWN)
        reals = [real_1, real_2, real_3, real_4]
        self.play(LaggedStart(*[FadeIn(mob) for mob in decs], run_time = 2, lag_ratio = 0.3), LaggedStart(*[FadeIn(mob) for mob in reals], run_time = 2, lag_ratio = 0.3))
        self.wait(0, 1) #事实上 所有的小数组成的集合
        tip = Simsun(r"*这里的“大”是指赋了序拓扑以后，实数集同胚于无限小数集的一个真子集").scale(0.4).next_to(3*DOWN, UP)
        self.play(FadeIn(tip))
        self.wait(2, 8) #要比所有的实数组成的集合 稍微大那么一点
        self.wait(0, 21) #（空闲）

        line_1 = Line(dec_1, real_1, buff = 0.2)
        line_2 = Line(dec_2, real_2, buff = 0.2)
        line_3 = Line(dec_3, real_2, buff = 0.2)
        line_4 = Line(dec_4, real_3, buff = 0.2)
        line_5 = Line(dec_5, real_4, buff = 0.2)
        lines = [line_1, line_2, line_3, line_4, line_5]
        self.play(FadeOut(tip), LaggedStart(*[ShowCreation(mob) for mob in lines], run_time = 2, lag_ratio = 0.3))
        self.wait(1+3-2, 26+6) #正是因为大了这么一点 0.9的循环和1这两个不同的小数
        interval_1 = MTex(r"(-\infty, 1)").shift(6*LEFT + 0.8*UP)
        interval_2 = MTex(r"(-\infty, 1]").shift(6*LEFT)
        self.play(FadeIn(interval_1, 0.5*RIGHT), FadeIn(interval_2, 0.5*RIGHT))
        self.wait(0, 26) #可以表示不同的集合
        indicate = SurroundingRectangle(real_2).save_state()
        self.play(FadeIn(indicate, remover = True, rate_func = there_and_back))
        self.play(FadeIn(indicate.restore(), remover = True, rate_func = there_and_back))
        self.wait(0, 11) #但它们表示的实数是同一个
        self.wait(0, 27) #（空闲）

        self.play(self.change_notice())
        self.wait(1, 28) #话说回来 有没有这样一种集合
        self.wait(2, 17) #它和所有小数组成的集合一样大呢
        self.wait(0, 15) #（空闲）
        rectangle_0 = Rectangle(height = 2, width = 12, color = BLUE, stroke_width = 0, fill_opacity = 0.2).shift(2*UP)
        corner_left = 3*DOWN + 6*LEFT
        corner_right = 3*DOWN + 6*RIGHT
        centers_1 = [corner_left, corner_right]
        rectangles_1 = [rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[0]).set_color(interpolate_color(GREEN, BLUE, 0.5)), rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[1]).set_color(interpolate_color(BLUE, GREEN, 0.5))]
        cantor = VGroup(*rectangles_1, rectangle_0)
        last_centers = centers_1
        last_rectangles = rectangles_1
        for i in range(2, 10):
            centers = [*(last_centers-corner_left)/3+corner_left, *(last_centers-corner_right)/3+corner_right]
            rectangles = [last_rectangles[j//2].copy().scale(np.array([1/3, 1/2, 0]), about_point = centers[j]).set_color(interpolate_color(GREEN, BLUE, 1/2**i)) for j in range(2**i)]
            cantor.add(*rectangles)
            last_centers = centers
            last_rectangles = rectangles
        self.bring_to_back(cantor).play(FadeIn(cantor, rate_func = there_and_back))
        self.wait(0+0-1, 25+17) #还真有 （空闲）

        alpha = ValueTracker(0.0)
        def photo_updater(mob: ImageMobject):
            value = alpha.get_value()
            mob.restore().scale(value).rotate(PI*(1-value))
        picture_photo = ImageMobject("photo.png", height = 2).shift(1.5*UP).save_state().add_updater(photo_updater)
        text_name = Text("乐正垂星", font = "simhei").shift(1.5*UP)
        shade = BackgroundRectangle(text_name, color = BACK, fill_opacity = 1)
        like = Text("", font = 'vanfont').shift(3*LEFT + 1.5*DOWN).scale(2)
        coin = Text("", font = 'vanfont').shift(1.5*DOWN).scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT + 1.5*DOWN).scale(2)
        sanlian = VGroup(like, coin, star)
        self.clear().add(picture_photo).play(self.change_notice(), FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, ORIGIN), FadeInFromPoint(star, 3*RIGHT), alpha.animate.set_value(1.0))
        picture_photo.clear_updaters()
        shade.next_to(picture_photo.get_edge_center(RIGHT), LEFT, buff = 0)
        text_name.move_to(shade)
        self.add(text_name, shade, picture_photo).play(picture_photo.animate.shift(1.5*LEFT), shade.animate.shift(1.5*LEFT), text_name.animate.shift(1.2*RIGHT), Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), sanlian.animate.set_color("#00A1D6"))
        self.wait(1+3-2, 7+0) #我是乐正垂星 长按点赞一键三连 我们开始吧
        self.wait(2, 10)
        self.fade_out(end = True)
        self.wait(2, 0) #到此共102秒

#################################################################### 

class Chapter1_0(FrameScene):

    def construct(self):

        text1 = MTexText("第一节\ 二进制下的$0.\dot1$", tex_to_color_map = {"第一节": YELLOW, "二进制": BLUE, "0.\dot1": GREEN})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Patch1_1(FrameScene):
    def construct(self):

        rectangle_0 = Rectangle(height = 2, width = 10, color = BLUE, stroke_width = 0, fill_opacity = 1).shift(1.5*UP)
        anim_rectangle_0 = rectangle_0.copy()
        corner_left = 2*DOWN + 5*LEFT
        corner_right = 2*DOWN + 5*RIGHT
        corners = [interpolate(corner_left, corner_right, i/9) for i in range(10)]
        rectangles_1 = [rectangle_0.copy().scale(np.array([1/19, 1/3, 0]), about_point = corner).set_color(interpolate_color(GREEN, BLUE, 1/3)) for corner in corners]
        anim_rectangles_1 = [rect.copy() for rect in rectangles_1]
        anims = [FadeIn(anim_rectangle_0, 3*DOWN), LaggedStart(*[TransformFromCopy(rectangle_0.set_color(BACK), rect, rate_func = linear) for rect in anim_rectangles_1], lag_ratop = 0.2, group = VGroup())]
        self.bring_to_back(*anim_rectangles_1, anim_rectangle_0)
        last_centers = corners
        last_rectangles = rectangles_1
        for i in range(2, 5):
            centers = [(center-corner)/19+corner for corner in corners for center in last_centers]
            rectangles = [last_rectangles[j//10].copy().scale(np.array([1/19, 1/3, 0]), about_point = centers[j]).set_color(interpolate_color(GREEN, BLUE, 1/3**i)) for j in range(10**i)]
            anim_rectangles = [rect.copy() for rect in rectangles]
            anims.append(AnimationGroup(*[LaggedStart(*[TransformFromCopy(last_rectangles[j].set_color(BACK), anim_rectangles[j*10+k], rate_func = linear) for k in range(10)], lag_ratio = 0.2, group = VGroup()) for j in range(10**(i-1))], rate_func = linear, run_time = 1, group = VGroup()))
            self.bring_to_back(*anim_rectangles)
            last_centers = centers
            last_rectangles = rectangles
        text = Simhei(r"十进制小数对应的集合").scale(0.8).next_to(3*UP, UP)
        self.play(LaggedStart(*anims, lag_ratio = 1, run_time = 5, group = VGroup()), Write(text, run_time = 5, rate_func = squish_rate_func(smooth, 3.9/5, 4.9/5)))
        self.wait(1+1+0+3-5, 5+29+20+8) #在开始之前 我们还有一点准备工作要做 （空闲） 十进制对于这个集合来说还是有些过于复杂了
        self.wait(0, 19) #（空闲）
        self.play(text.animate.shift(3.75*LEFT), run_time = 2)
        self.wait(1+2-2, 5+13) #相比之下 它的二进制版本要更容易理解一些
        self.wait(0, 23) #（空闲）
        self.wait(0, 15) #淡出

class Patch1_2(FrameScene):
    CONFIG = {
        "for_pr": False,
    }
    def construct(self):
        self.notices = [Notice("话题引入", "请听介绍")]
        self.notice = self.notices[0]
        self.play(Write(self.notice))
        self.wait(0, 5) #在开始之前
        self.wait(1, 29) #我们还有一点准备工作要做
        self.wait(0, 20) #（空闲）
        self.wait(3, 8) #十进制对于这个集合来说还是有些过于复杂了
        self.wait(0, 19) #（空闲）
        rectangle_0 = Rectangle(height = 2, width = 10, color = BLUE, stroke_width = 0, fill_opacity = 1).shift(1.5*UP)
        corner_left = 2*DOWN + 5*LEFT
        corner_right = 2*DOWN + 5*RIGHT
        centers_1 = [corner_left, corner_right]
        rectangles_1 = [rectangle_0.copy().scale(np.array([1/3, 1/3, 0]), about_point = centers_1[0]).set_color(interpolate_color(GREEN, BLUE, 0.5)), rectangle_0.copy().scale(np.array([1/3, 1/3, 0]), about_point = centers_1[1]).set_color(interpolate_color(BLUE, GREEN, 0.5))]
        cantor = VGroup(*rectangles_1, rectangle_0)
        last_centers = centers_1
        last_rectangles = rectangles_1
        for i in range(2, 10):
            centers = [*(last_centers-corner_left)/3+corner_left, *(last_centers-corner_right)/3+corner_right]
            rectangles = [last_rectangles[j//2].copy().scale(np.array([1/3, 1/3, 0]), about_point = centers[j]).set_color(interpolate_color(GREEN, BLUE, 1/2**i)) for j in range(2**i)]
            cantor.add(*rectangles)
            last_centers = centers
            last_rectangles = rectangles
        board = Rectangle(height = 8.4, width = 15.2, fill_opacity = 1, fill_color = BACK, stroke_width = 0).shift(15.1*RIGHT)
        inner = Rectangle(height = 8.4, width = 0.1, fill_opacity = 1, fill_color = BLACK, stroke_width = 0).shift(7.5*RIGHT)
        line_1 = Line(4.2*UP, 4.2*DOWN).shift(0.05*LEFT + 7.5*RIGHT)
        line_2 = Line(4.2*UP, 4.2*DOWN, color = YELLOW_E).shift(0.05*RIGHT + 7.5*RIGHT)
        inner.add(line_1, line_2)
        alpha = ValueTracker(0.0)
        rectangles = cantor.submobjects
        func = lambda mob: mob.restore().shift(15*alpha.get_value()*LEFT).set_points(Intersection(mob, board).get_points())
        for rect in rectangles:
            rect.shift(15*RIGHT).save_state().add_updater(func)
        text = Simhei(r"二进制小数对应的集合").scale(0.8).next_to(3*UP + 15*RIGHT, UP)
        self.add(board, *rectangles, inner, self.notice).play(text.animate.shift(11.25*LEFT), alpha.animate.set_value(1), board.animate.shift(7.6*LEFT), inner.animate.shift(7.6*LEFT), run_time = 2)
        self.wait(1+2-2, 5+13) #相比之下 它的二进制版本要更容易理解一些
        self.wait(0, 23) #（空闲）
        self.wait(0, 15)

class Chapter1_1(FrameScene):
    def construct(self):
        self.notices = [Notice("话题引入", "请听介绍"), 
                        Notice("小学奥数", "请　掌握"), 
                        Notice("等价形式", "请　模仿"), 
                        Notice("违规操作", "请换规范"), 
                        ]
        self.notice = self.notices[0]
        self.frames += 12*30+2
        self.add(self.notice).wait(2, 6) #想必在这个信息化的时代
        title = Title(r"二进制")
        title_line = TitleLine()
        self.play(Write(title), GrowFromCenter(title_line), self.change_notice())
        self.wait(1, 6) #大家对于二进制都已经不陌生了
        self.wait(0, 19) #（空闲）

        decimal = Simhei(r"十进制").scale(0.75).shift(UP + 6*0.8*LEFT)
        binary = Simhei(r"二进制").scale(0.75).shift(DOWN + 6*0.8*LEFT)
        decimals = [MTex(f"{i:d}", color = GREEN_B if i%2 else BLUE_B).scale(0.8).shift(UP + (i-3.5)*RIGHT) for i in range(10)]
        binaries = [MTex(f"{i:b}", color = GREEN_B if i%2 else BLUE_B).scale(0.8).shift(DOWN + (i-3.5)*RIGHT) for i in range(10)]
        self.play(Write(decimal), FadeIn(VGroup(*decimals), 0.3*RIGHT, lag_ratio = 0.2, run_time = 2))
        self.wait(0, 8) #不同于逢十进一的十进制
        self.play(Write(binary), FadeIn(binaries[0], 0.3*RIGHT), FadeIn(binaries[1], 0.3*RIGHT))
        self.wait(1, 21) #二进制只有0和1两种数码
        self.wait(1, 1) #逢二进一
        self.wait(0, 20) #（空闲）
        
        indicate = SurroundingRectangle(decimals[2])
        self.play(FadeIn(indicate, run_time = 2, rate_func = double_there_and_back, remover = True))
        self.wait(0, 7) #在十进制中写作2的数
        self.play(FadeIn(binaries[2], 0.3*DOWN))
        self.wait(1, 3) #在二进制中会被写成10
        self.wait(0, 21) #（空闲）

        indicate = SurroundingRectangle(decimals[3])
        self.play(IndicateAround(decimals[3]))
        self.wait(0, 13) #再往后 十进制中的3......
        self.play(FadeIn(binaries[3], 0.3*DOWN))
        self.wait(1, 11) #......在二进制中会被写成11
        self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in binaries[4:]], lag_ratio = 0.2, run_time = 1.5))
        self.wait(1+0-1, 1+22-15) #依此类推 （空闲）

        decimal_all = VGroup(decimal, *decimals)
        binary_all = VGroup(binary, *binaries)
        self.play(decimal_all.animate.scale(0.6).next_to(6*LEFT + 3*UP, DR), binary_all.animate.scale(0.6).next_to(6*LEFT + 2.5*UP, DR))
        self.wait(0, 12) #不仅是自然数
        self.wait(2, 13) #小数也可以表示成二进制的形式
        self.wait(0, 19) #（空闲）

        frac_1 = MTex(r"\frac{1}{2}=(0.1)_2")
        self.play(Write(frac_1))
        self.wait(2, 20)
        self.play(frac_1.animate.scale(0.6).next_to(5*LEFT + UP)) #比如说 二进制中的0.1 表示的就是1/2
        frac_2 = MTex(r"\frac{1}{4}=(0.01)_2")
        self.play(Write(frac_2))
        self.wait(1, 9)
        self.play(frac_2.animate.scale(0.6).next_to(5*LEFT)) #而0.01表示的就是1/4
        frac_3 = MTex(r"\frac{1}{8}=(0.001)_2")
        self.play(Write(frac_3))
        self.wait(1, 0)
        ellipsis = MTex(r"\vdots").set_color(BACK).set_x(frac_3[3].get_x()).set_y(-1)
        self.play(frac_3.animate.scale(0.6).next_to(5*LEFT + DOWN), ellipsis.animate.set_color(WHITE).scale(0.6).set_x(frac_2[3].get_x()).set_y(-2)) #每往小数点后一位 数值就会缩小一半
        self.wait(0, 18) #（空闲）

        frac_4 = MTex(r"(0.101)_2=\frac{5}{8}")
        frac_4_1 = MTex(r"\frac{1}{2}", color = BLUE).scale(0.8).move_to(frac_4[3]).shift(UP)
        frac_4_2 = MTex(r"\frac{1}{8}", color = GREEN).scale(0.8).move_to(frac_4[5]).shift(DOWN)
        self.play(Write(frac_4[0:8]))
        self.play(LaggedStart(AnimationGroup(FadeIn(frac_4_1), frac_4[3].animate.set_color(BLUE)), AnimationGroup(FadeIn(frac_4_2), frac_4[5].animate.set_color(GREEN)), run_time = 1.5, lag_ratio = 0.5))
        self.play(Write(frac_4[8:]))
        self.wait(0, 11) #而像是0.101这样的小数 表示的就是5/8
        self.wait(0, 25) #（空闲）

        self.wait(1, 25) #既然有了小数的概念
        self.wait(3, 5) #我们就能看一看二进制中的除法是怎么算的了
        self.wait(0, 18) #（空闲）

        self.play(*[FadeOut(mob) for mob in [frac_4, frac_4_1, frac_4_2]])
        division_d = MTex(r"9\divisionsymbol6=1.5", tex_to_color_map = {r"9": BLUE, r"6": GREEN, r"1.5": TEAL})
        parts_d = [division_d[0], division_d[1], division_d[2], division_d[3], division_d[4:]]
        division_b = MTex(r"1001\divisionsymbol110=1.1", tex_to_color_map = {r"1001": BLUE, r"110": GREEN, r"1.1": TEAL}).scale(0.7).next_to(binary_all, buff = 0.8)
        parts_b = [division_b[0:4], division_b[4], division_b[5:8], division_b[8], division_b[9:]]
        self.play(Write(division_d))
        self.wait(1, 11) #比如说 我们来看看9÷6应该怎么算
        self.wait(0, 19) #（空闲）

        division_d.save_state().scale(0.7)
        for i in range(5):
            parts_d[i].move_to(parts_b[i]).shift(0.5*UP)
        division_d.generate_target()
        division_d.restore()
        self.play(MoveToTarget(division_d, path_arc = PI/6))
        self.wait(1, 29) #这个式子在十进制中的结果是1.5
        self.play(LaggedStart(*[FadeIn(parts_b[i], parts_b[i].get_center() - parts_d[i].get_center()) for i in range(5)], run_time = 2, lag_ratio = 0.3))
        self.wait(1, 26) #而这三个数字在二进制中的表示 分别是这样的
        self.wait(0, 22) #（空闲）

        self.wait(2, 16) #我们怎么不借助十进制的桥梁
        self.wait(2, 4) #直接在二进制中得到结果呢
        self.wait(0, 21) #（空闲）

        offset = 3*RIGHT + 0.5*UP
        def pos(x: float, y:float):
            return offset + 0.6*RIGHT*x + 0.8*UP*y
        def put_to(mob: VGroup, x: float, y: float):
            terms = len(mob.submobjects)
            for i in range(terms):
                mob[i].move_to(pos(x-(terms-1-i), y))
            return mob
        dividend = put_to(MTex(r"1001", color = BLUE), 0, 0)
        divisor = put_to(MTex(r"110", color = GREEN), -4.5, 0)
        division_symbol = VGroup(Line(pos(-3.5, 0.5), pos(0.5, 0.5)), Arc(radius = 1.6, angle = -PI/6, start_angle = 0, arc_center = pos(-3.5, 0.5)+2*0.8*LEFT))
        quotient = put_to(MTex(r"11", color = TEAL), 1, 1)
        quotient.add(MTex(r".", color = TEAL).move_to(quotient[0].get_corner(DR) + 0.1*RIGHT))
        dividend.add(MTex(r".", color = GREY).move_to(dividend[-1].get_corner(DR) + 0.1*RIGHT), MTex(r"0", color = GREY).move_to(pos(1, 0)))
        self.play(LaggedStart(TransformFromCopy(parts_b[2], divisor, path_arc = -PI/6), TransformFromCopy(parts_b[0], dividend[0:4], path_arc = -PI/6), run_time = 1.5, lag_ratio = 0.5))
        self.wait(0, 5) #和在十进制中一样
        self.play(ShowCreation(division_symbol))
        self.wait(0, 26) #这也需要列出竖式来计算
        self.wait(0, 20) #（空闲）

        surr_1 = SurroundingRectangle(dividend[0:3])
        surr_2 = SurroundingRectangle(quotient[0]).move_to(pos(-1, 1))
        self.play(ShowCreation(surr_1), FadeIn(surr_2), *[mob.save_state().animate.scale(1.2).set_color(YELLOW) for mob in [decimals[4], decimals[6], binaries[4], binaries[6]]])
        self.wait(1, 24) #首三位的100要比110小
        temp = MTex(r"0", color = GREY).move_to(pos(-1, 1))
        self.play(Write(temp))
        self.wait(0, 26) #所以第二位商0
        self.play(FadeOut(temp), surr_2.animate.move_to(pos(0, 1)), Transform(surr_1, SurroundingRectangle(dividend[0:4])), *[mob.animate.restore() for mob in [decimals[4], binaries[4]]], *[mob.save_state().animate.scale(1.2).set_color(YELLOW) for mob in [decimals[9], binaries[9]]])
        self.wait(0, 15) #我们直接来看第一位
        self.wait(0, 19) #（空闲）

        m_1 = put_to(MTex(r"110", color = GREEN), 0, -1)
        line_1 = Line(pos(-3.5, -1.5), pos(0.5, -1.5))
        d_1 = put_to(MTex(r"110", color = BLUE), 1, -2)
        self.play(Write(quotient[0]))
        self.wait(0, 15) #第一位商1
        self.play(Write(m_1), FadeOut(surr_1))
        self.play(ShowCreation(line_1))
        self.wait(0, 6) #用1001减去110
        self.play(Write(d_1[0:2]), *[mob.save_state().animate.scale(1.2).set_color(YELLOW) for mob in [decimals[3], binaries[3]]])
        self.wait(0, 3) #会得到11
        self.wait(0, 20) #（空闲）

        self.wait(3, 6) #竖式减法和十进制的过程没什么两样
        self.wait(2, 27) #只是在退位的时候不再是借一当十
        self.wait(1, 5) #而是借一当二
        self.wait(0, 22) #（空闲）

        self.play(surr_2.animate.move_to(pos(1, 1)), FadeIn(quotient[-1]), FadeIn(dividend[-2]), *[mob.animate.restore() for mob in [decimals[3], binaries[3], decimals[9], binaries[9]]], division_symbol[0].animate.put_start_and_end_on(pos(-3.5, 0.5), pos(1.5, 0.5)))
        self.wait(0, 25) #接下来是小数部分
        self.play(Write(dividend[-1]), Write(d_1[-1]))
        self.wait(0, 19) #需要给11补0
        self.wait(0, 16) #（空闲）

        m_2 = put_to(MTex(r"110", color = GREEN), 1, -3)
        line_2 = Line(pos(-1.5, -3.5), pos(1.5, -3.5))
        d_2 = put_to(MTex(r"0", color = BLUE), 1, -4)
        self.play(Write(quotient[1]))
        self.play(Write(m_2))
        self.play(ShowCreation(line_2))
        self.play(Write(d_2))
        self.wait(1+2-4, 16+19) #二分位商1 110减110正好除尽
        self.play(Transform(surr_2, SurroundingRectangle(quotient)))
        self.wait(0, 20) #商是1.1
        self.wait(2, 13) #正好是1.5在二进制下的表示
        self.wait(0, 29) #（空闲）

        self.play(*[FadeOut(mob) for mob in [division_d, division_b, dividend, divisor, division_symbol, quotient, surr_2, m_1, line_1, d_1, m_2, line_2, d_2]], *[mob.animate.restore() for mob in [decimals[6], binaries[6]]])
        division_d = MTex(r"1\divisionsymbol3=0.\dot3", tex_to_color_map = {r"1": BLUE, r"3": GREEN, r"0.\dot3": TEAL}).scale(0.7).next_to(decimal_all, buff = 0.8)
        parts_d = [division_d[0], division_d[1], division_d[2], division_d[3], division_d[4:]]
        for i in range(5):
            parts_d[i].set_x(parts_b[i].get_x())
        division_b = MTex(r"1\divisionsymbol11=0.\dot0\dot1", tex_to_color_map = {r"1": BLUE, r"11": GREEN, r"0.\dot0\dot1": TEAL}).scale(0.7).next_to(binary_all, buff = 0.8)
        parts_b = [division_b[0], division_b[1], division_b[2:4], division_b[4], division_b[5:]]
        for i in range(5):
            parts_b[i].set_x(parts_d[i].get_x())
        offset = 2*RIGHT + 0.5*UP
        dividend = put_to(MTex(r"100", color = BLUE), 2, 0)
        dividend[1:].set_color(GREY)
        divisor = put_to(MTex(r"11", color = GREEN), -1.5, 0)
        division_symbol = VGroup(Line(pos(-0.5, 0.5), pos(0.5, 0.5)), Arc(radius = 1.6, angle = -PI/6, start_angle = 0, arc_center = pos(-0.5, 0.5)+2*0.8*LEFT))
        quotient = put_to(MTex(r"001", color = TEAL), 2, 1)
        dot_1 = MTex(r".", color = TEAL).move_to(quotient[0].get_corner(DR) + 0.1*RIGHT)
        dot_2 = MTex(r".", color = GREY).move_to(dividend[0].get_corner(DR) + 0.1*RIGHT)
        self.play(*[FadeIn(mob) for mob in [division_d, division_b[0:5], dividend[0], divisor, division_symbol]], *[mob.save_state().animate.scale(1.2).set_color(YELLOW) for mob in [decimals[3], binaries[3]]])
        self.wait(1+0-2, 23+16) #我们再来试试1÷3 （空闲）

        surr_1 = SurroundingRectangle(quotient[0])
        surr_2 = SurroundingRectangle(dividend[0])
        self.play(FadeIn(surr_1), Write(surr_2), *[mob.save_state().animate.scale(1.2).set_color(YELLOW) for mob in [decimals[1], binaries[1]]])
        self.play(Write(quotient[0]))
        self.wait(0, 27) #1小于11 于是个位是0
        self.wait(0, 16) #（空闲）
        self.play(division_symbol[0].animate.put_start_and_end_on(pos(-0.5, 0.5), pos(1.5, 0.5)), surr_1.animate.shift(0.6*RIGHT), Transform(surr_2, SurroundingRectangle(dividend[:2])), FadeIn(dividend[1]), FadeIn(dot_1), FadeIn(dot_2), *[mob.save_state().animate.scale(1.2).set_color(YELLOW) for mob in [decimals[2], binaries[2]]], *[mob.animate.restore() for mob in [decimals[1], binaries[1]]])
        self.play(Write(quotient[1]))
        self.wait(1, 2) #10小于11 于是二分位也是0
        self.wait(0, 20) #（空闲）

        m_1 = put_to(MTex(r"11", color = GREEN), 2, -1)
        line_1 = Line(pos(-0.5, -1.5), pos(2.5, -1.5))
        d_1 = put_to(MTex(r"1", color = BLUE), 2, -2)
        self.play(division_symbol[0].animate.put_start_and_end_on(pos(-0.5, 0.5), pos(2.5, 0.5)), surr_1.animate.shift(0.6*RIGHT), Transform(surr_2, SurroundingRectangle(dividend)), FadeIn(dividend[2]), *[mob.save_state().animate.scale(1.2).set_color(YELLOW) for mob in [decimals[4], binaries[4]]], *[mob.animate.restore() for mob in [decimals[2], binaries[2]]])
        self.wait(0, 16) #补了两次0之后
        self.play(Write(quotient[2]))
        self.play(Write(m_1), FadeOut(surr_2))
        self.play(ShowCreation(line_1))
        self.wait(0, 9) #100大于11 于是四分位是1
        self.wait(0, 17) #（空闲）
        self.play(Write(d_1), *[mob.animate.restore() for mob in [decimals[4], binaries[4]]], FadeOut(surr_1))
        self.wait(1, 20) #余下1 和最开始的形式一模一样
        self.wait(0, 21) #（空闲）
        
        step_dr = 2*0.6*RIGHT + 2*0.8*DOWN
        copy_dr = VGroup(dividend[1:].copy().set_color(BLUE), m_1, line_1, d_1).copy().shift(step_dr)
        step_r = 2*0.6*RIGHT
        copy_r = VGroup(dividend[1:].copy(), quotient[1:].copy()).shift(step_r)
        self.play(FadeIn(copy_r, step_r, path_arc = -PI/2), division_symbol[0].animate.put_start_and_end_on(pos(-0.5, 0.5), pos(4.5, 0.5)))
        self.play(FadeIn(copy_dr, step_dr, path_arc = -PI/2))
        copy_dr_2 = copy_dr.copy().shift(step_dr)
        copy_r_2 = copy_r.copy().shift(step_r)
        self.play(FadeIn(copy_r_2, step_r, path_arc = -PI/2), division_symbol[0].animate.put_start_and_end_on(pos(-0.5, 0.5), pos(6.5, 0.5)))
        self.play(FadeIn(copy_dr_2, step_dr, path_arc = -PI/2))
        copy_r_3 = copy_r_2.copy().shift(step_r)
        self.play(FadeIn(copy_r_3, step_r, path_arc = -PI/2), division_symbol[0].animate.put_start_and_end_on(pos(-0.5, 0.5), pos(8.5, 0.5)))
        self.wait(2+2-5, 16+24) #接下来就是反复重复这个过程 最终我们会得到一个无限循环小数
        parts_b[4].shift(parts_d[4][0].get_center() - parts_b[4][0].get_center() + 0.5*DOWN)
        surr = SurroundingRectangle(parts_b[4])
        self.play(Write(parts_b[4]))
        self.play(ShowCreation(surr))
        self.wait(0, 10) #它就是二进制表示下的1/3
        self.wait(1, 0) #（空闲）

        self.play(*[FadeOut(mob) for mob in [dividend, divisor, division_symbol, quotient, dot_1, dot_2, m_1, line_1, d_1, copy_dr, copy_dr_2, copy_r, copy_r_2, copy_r_3]], *[mob.animate.restore() for mob in [decimals[3], binaries[3]]])
        self.wait(2, 1) #这说明无限小数在二进制中也是存在的
        self.wait(0, 18) #（空闲）

        dec_1 = MTex(r"(1)_{10}", color = GREEN).shift(0.6*UP + 0.5*LEFT)
        dec_0 = MTex(r"(0.\dot9)_{10}", color = BLUE).shift(0.6*UP + 1.5*RIGHT)
        equal_1 = MTex(r"\Leftrightarrow").rotate(PI/2).shift(0.5*LEFT)
        equal_0 = MTex(r"\Leftrightarrow").rotate(PI/2).shift(1.5*RIGHT)
        bin_1 = MTex(r"(1)_2", color = GREEN).shift(0.6*DOWN + 0.5*LEFT)
        bin_0 = MTex(r"(0.\dot1)_2", color = BLUE).shift(0.6*DOWN + 1.5*RIGHT)
        self.play(FadeIn(dec_1, 0.3*DOWN), FadeIn(dec_0, 0.3*DOWN))
        self.play(Write(equal_1), Write(equal_0), self.change_notice())
        self.wait(2, 20) #于是 我们可以放心地把1和0.9的循环换到二进制来表示了
        self.wait(0, 23) #（空闲）
        self.play(FadeIn(bin_1, 0.3*DOWN))
        self.wait(0, 29) #1当然还会变成1
        self.play(FadeIn(bin_0, 0.3*DOWN))
        self.wait(1, 23) #而0.9的循环则会变成0.1的循环
        self.wait(0, 21) #（空闲）

        expand = MTex(r"=0.1111111111111111", color = WHITE)
        expand.next_to(bin_0).shift((bin_0[1].get_y()-expand[1].get_y())*UP)
        self.play(Write(expand))
        self.wait(0, 12) #如果我们把每一项都写出来
        fracs = [MTex(r"\frac{1}{" + str(2**i) + r"}", color = BLUE if i%2 else GREEN).scale(0.8*i**(np.log(2/3))).next_to(expand[i+2], UP if i%2 else DOWN) for i in range(1, 17)]
        self.play(LaggedStart(*[FadeIn(frac, 0.1*RIGHT) for frac in fracs], run_time = 2, lag_ratio = 0.1), LaggedStart(*[expand[i+2].animate.set_color(BLUE if i%2 else GREEN) for i in range(1, 17)], run_time = 2, lag_ratio = 0.1))
        self.wait(1, 4) #那就是从1/2开始的无穷等比数列求和
        self.wait(0, 16) #（空闲）

        self.wait(1, 24) #它自然应该等于1
        dec_wrong = MTex(r"-=(0.\dot01)_{10}")
        offset_d = (dec_0.get_x(LEFT) - dec_1.get_x(RIGHT) - dec_wrong[0].get_width())/2
        parts_d = [dec_wrong[0].next_to(dec_1, buff = offset_d), dec_wrong[1].next_to(dec_0, buff = offset_d), dec_wrong[2:].next_to(dec_wrong[1], buff = offset_d)]
        bin_wrong = MTex(r"-=(0.\dot01)_{2}")
        offset_b = (bin_0.get_x(LEFT) - bin_1.get_x(RIGHT) - bin_wrong[0].get_width())/2
        parts_b = [bin_wrong[0].next_to(bin_1, buff = offset_b), bin_wrong[1].next_to(bin_0, buff = offset_b), bin_wrong[2:].next_to(bin_wrong[1], buff = offset_b)]
        self.play(FadeOut(expand), FadeOut(VGroup(*fracs)), Write(dec_wrong), self.change_notice())
        self.wait(0, 28) #但你如果认为在十进制中
        self.wait(2, 27) #0.9的循环和1差了一个无穷小
        self.play(Write(bin_wrong))
        self.wait(0, 20) #那么在二进制中
        self.wait(3, 8) #0.1的循环和1之间 也应该差一个无穷小
        self.wait(0, 23) #（空闲）
        self.wait(2, 29) #既然实数里面容不下这个无穷小的存在
        self.wait(2, 18) #我们为什么不自己新造一套数字系统呢
        self.wait(2, 0)
        self.fade_out(end = True)
        self.wait(2, 9) #到此共187秒

#################################################################### 

class Chapter2_0(FrameScene):

    def construct(self):

        text2 = Text("第二节 切分数轴", font = 'simsun', t2c={"第二节": YELLOW, "切分": BLUE, "数轴": GREEN})

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(FrameScene):
    def construct(self):
        self.notices = [Notice("危险操作", "简高禁"), 
                        Notice("安全操作", "请　模仿"), 
                        Notice("微妙细节", "请　思考"), 
                        Notice("奇妙数集", "请　掌握"), 
                        Notice("等价交换", "请　思考"), 
                        ]
        self.notice = self.notices[0]

        self.tip = Simsun(r"*所有小数均为二进制小数").scale(0.4).next_to(self.notice, LEFT).set_x(-5)
        self.play(Write(self.notice), Write(self.tip))
        self.wait(0+0-1, 26+18) #说干就干（空闲）

        intervals = [Interval(ORIGIN, 2*RIGHT).shift(2*i*RIGHT) for i in range(-5, 5)]
        self.add(*intervals, self.shade, self.tip, self.notice).play(self.shade.save_state().animate.shift(128/9*RIGHT), run_time = 2)
        self.remove(self.shade.restore()).wait(1+2-2, 16+6) #这是一条数轴 上面的每个点对应了一个实数
        self.wait(0, 18) #（空闲）

        bin_1 = MTex(r"1", color = GREEN).next_to(2*RIGHT, UR)
        bin_0 = MTex(r"0.\dot1", color = BLUE).next_to(2*RIGHT, UL)
        self.play(LaggedStart(Write(bin_1), Write(bin_0), run_time = 1.5, lag_ratio = 0.5))
        self.wait(1, 27) #1和0.1的循环这两个二进制小数
        self.play(Transform(Line(2*RIGHT, 2*RIGHT + 0.25*UP), Line(2*RIGHT, 2*RIGHT + 0.25*UP, color = YELLOW, stroke_width = 8), run_time = 2, remover = True, rate_func = double_there_and_back))
        self.wait(0, 2) #在这条数轴上对应了同一个点
        self.wait(0, 19) #（空闲）

        self.wait(2, 7) #如果我们想让它们有所区别
        paras = {"run_time": 1.5, "rate_func": squish_rate_func(rush_from, 1/3, 1)}
        self.play(Cut(2*RIGHT), *[mob.animating(**paras).shift(0.5*LEFT) for mob in intervals[:6]], *[mob.animating(**paras).shift(0.5*RIGHT) for mob in intervals[6:]], bin_1.animating(**paras).next_to(2.5*RIGHT + 0.25*UP, UP), bin_0.animating(**paras).next_to(1.5*RIGHT + 0.25*UP, UP))
        self.wait(1+0-1, 23+17-15) #那就需要把数轴一分为二 （空闲）

        self.play(Transform(Line(1.5*RIGHT, 1.5*RIGHT + 0.25*UP), Line(1.5*RIGHT, 1.5*RIGHT + 0.25*UP, color = YELLOW, stroke_width = 8), run_time = 2, remover = True, rate_func = double_there_and_back))
        self.wait(1, 25) #左半边的数轴多了一个右端点 0.1的循环
        self.play(Transform(Line(2.5*RIGHT, 2.5*RIGHT + 0.25*UP), Line(2.5*RIGHT, 2.5*RIGHT + 0.25*UP, color = YELLOW, stroke_width = 8), run_time = 2, remover = True, rate_func = double_there_and_back))
        self.wait(1, 0) #而右半边的数轴多了一个左端点 1
        self.wait(0, 23) # （空闲）

        bin_2_1 = MTex(r"10", color = GREEN).next_to(4.5*RIGHT, UR)
        bin_2_0 = MTex(r"1.\dot1", color = BLUE).next_to(4.5*RIGHT, UL)
        alpha = ValueTracker(0.0)
        def bin_updater(offset: np.ndarray):
            def util(mob: MTex):
                value = alpha.get_value()
                if value <= 0.5:
                    mob.restore().set_opacity(smooth(value*2))
                else:
                    mob.restore().set_opacity(smooth(2 - value*2)).shift(offset*rush_from(value - 0.5))
            return util
        bin_2_1.save_state().add_updater(bin_updater(RIGHT))
        self.add(bin_2_1).play(FadeIn(bin_2_0, rate_func = there_and_back, remover = True), alpha.animating(rate_func = linear).set_value(1.0), FadeOut(bin_1), FadeOut(bin_0),
                  Cut(4.5*RIGHT), *[mob.animating(**paras).shift(RIGHT) for mob in intervals[7:]])
        self.remove(bin_2_1, alpha)
        tip = Simsun(r"* 0只对应一种小数表示，但为了后续叙述方便，仍然在0处切开").scale(0.4).next_to(3*DOWN, UP)
        self.play(LaggedStart(*[Cut((0.5 + 2*i)*LEFT) for i in range(0, 4)], run_time = 1.5, lag_ratio = 1/6), FadeIn(tip))
        self.play(*[intervals[i].animate.shift((5-i)*LEFT) for i in range(5)])
        self.wait(1+3+0-4, 5+12+17) #不仅如此 在每个整数处 我们都需要把数轴一分为二 （空闲）

        self.wait(3, 21) #于是 数轴被切成了一段段长度为1的区间
        self.wait(0, 21) #（空闲）

        self.play(FadeOut(tip))
        self.wait(1, 1) #但这就是我们想要的吗
        self.wait(0, 23) #当然不是
        self.wait(0, 21) #（空闲）

        bin_0.next_to(1.5*RIGHT + DOWN, UP)
        bin_1.next_to(2.5*RIGHT + DOWN, UP)
        self.play(FadeIn(bin_0, 0.3*UP), FadeIn(bin_1, 0.3*UP))
        self.wait(0, 29) #小数点后无限循环的1
        self.wait(1, 15) #可不止在整数处有
        self.wait(0, 19) #（空闲）

        line = Line(0.5*RIGHT, 0.5*RIGHT + 0.25*UP)
        frac = MTex(r"\frac12", color = TEAL).scale(0.8).next_to(0.5*RIGHT, DOWN)
        interval_1 = Interval(0.5*LEFT, 0.5*RIGHT)
        interval_2 = Interval(0.5*RIGHT, 1.5*RIGHT)
        self.play(ShowCreation(line), Write(frac), FadeOut(bin_0), FadeOut(bin_1))
        now_intervals = intervals[3:5] + intervals[6:8]
        self.remove(line, *intervals).add(*now_intervals, interval_1, interval_2)
        self.wait(1, 24) #比如说 1/2这个实数
        bin_1 = MTex(r"0.1", color = GREEN).scale(0.8).next_to(0.5*RIGHT + 0.25*UP, UR, buff = 0.1)
        bin_0 = MTex(r"0.0\dot1", color = BLUE).scale(0.8).next_to(0.5*RIGHT + 0.25*UP, UL, buff = 0.1)
        self.wait(0, 24) #可以同时用......
        self.play(Write(bin_1)) #......0.1......
        self.play(Write(bin_0)) 
        self.wait(0, 23) #......和0.01的循环来表示
        self.wait(0, 21) #（空闲）

        self.play(Cut(0.5*RIGHT), FadeOut(frac), interval_1.animating(**paras).shift(0.1*LEFT), interval_2.animating(**paras).shift(0.1*RIGHT), bin_1.animating(**paras).next_to(0.6*RIGHT + 0.25*UP, UR, buff = 0.1), bin_0.animating(**paras).next_to(0.4*RIGHT + 0.25*UP, UL, buff = 0.1))
        self.wait(1, 18) #所以 1/2的位置也得切上一刀
        self.wait(0, 21) #（空闲）
        
        halves = [halve(interval) for interval in now_intervals]
        lines, lefts, rights = [triple[0] for triple in halves], [triple[1] for triple in halves], [triple[2] for triple in halves]
        positions = [line.get_start() for line in lines]
        texs = [r"-\frac32", r"-\frac12", r"\frac32", r"\frac52"]
        fracs = [MTex(texs[i], color = TEAL).scale(0.8).next_to(positions[i], DOWN) for i in range(4)]
        alpha = ValueTracker(0.0)
        texs = [r"-1.0\dot1", r"-0.0\dot1", r"1.1", r"10.1"]
        bins_1 = [MTex(texs[i], color = GREEN).scale(0.8).next_to(positions[i] + 0.25*UP, UR, buff = 0.1).save_state().add_updater(bin_updater(0.1*RIGHT)) for i in range(4)]
        texs = [r"-1.1", r"-0.1", r"1.0\dot1", r"10.0\dot1"]
        bins_0 = [MTex(texs[i], color = BLUE).scale(0.8).next_to(positions[i] + 0.25*UP, UL, buff = 0.1).save_state().add_updater(bin_updater(0.1*LEFT)) for i in range(4)]
        self.play(FadeOut(bin_1), FadeOut(bin_0), LaggedStart(*[ShowCreation(line) for line in lines], lag_ratio = 1/3, run_time = 2), LaggedStart(*[Write(frac) for frac in fracs], lag_ratio = 1/3, run_time = 2))
        self.remove(*now_intervals, *lines).add(*lefts, *rights).wait(0, 16) #每个区间上都有这么一个位置
        self.add(*bins_1, *bins_0).play(alpha.animating(rate_func = linear).set_value(1), *[FadeOut(mob) for mob in fracs], *[Cut(position) for position in positions], *[mob.animating(**paras).shift(0.1*LEFT) for mob in lefts], *[mob.animating(**paras).shift(0.1*RIGHT) for mob in rights])
        self.remove(*bins_1, *bins_0, alpha).wait(0, 11) #都得在正中间切上一刀
        self.wait(0, 18) #（空闲）

        self.play(FadeOut(VGroup(*lefts), run_time = 2, lag_ratio = 1/3), FadeOut(VGroup(*rights), run_time = 2, lag_ratio = 1/3))
        self.wait(0, 7) #不过这些区间没什么不同

        ratio = 2/3
        ratio_o = 4/5
        ratio_s = 4/5
        marks_0 = [MTex(r"0", color = TEAL).shift(0.5*DOWN + 6*LEFT), MTex(r"\frac12", color = TEAL).set_opacity(ratio_o).shift(0.5*DOWN).scale(ratio), MTex(r"1", color = TEAL).shift(0.5*DOWN + 6*RIGHT)]
        self.play(Transform(interval_1, Interval(4*LEFT + 3/4*LEFT, 4*LEFT + 3/4*RIGHT, 0.5), run_time = 2), Transform(interval_2, Interval(4*RIGHT + 3/4*LEFT, 4*RIGHT + 3/4*RIGHT, 0.5), run_time = 2), *[Write(mob, rate_func = squish_rate_func(smooth, 0.5, 1)) for mob in marks_0])
        self.wait(1, 2) #我们只看整数部分为0的这一段就足够了
        self.wait(0, 27) #（空闲）

        self.play(Transform(Line(13/4*LEFT, 13/4*LEFT + 0.5*UP), Line(13/4*LEFT, 13/4*LEFT + 0.5*UP, color = YELLOW, stroke_width = 8), run_time = 2, remover = True, rate_func = double_there_and_back), Transform(Line(13/4*RIGHT, 13/4*RIGHT + 0.5*UP), Line(13/4*RIGHT, 13/4*RIGHT + 0.5*UP, color = YELLOW, stroke_width = 8), run_time = 2, remover = True, rate_func = double_there_and_back))
        self.wait(0, 8) #在1/2处切完就结束了吗
        self.wait(0, 23) #当然没有
        self.wait(0, 15) #（空闲）

        line, left, right = halve(interval_1)
        position = line.get_start()
        frac = MTex(r"\frac14", color = TEAL).set_opacity(ratio_o**2).scale(ratio**2).next_to(line, DOWN)
        self.play(ShowCreation(line), Write(frac))
        self.remove(line, interval_1).add(left, right).wait(0, 23) #1/4这个实数
        bin_1 = MTex(r"0.01", color = GREEN).scale(0.8).next_to(line, UR, buff = 0.1)
        bin_0 = MTex(r"0.00\dot1", color = BLUE).scale(0.8).next_to(line, UL, buff = 0.1)
        self.wait(0, 19) #可以同时用......
        self.play(Write(bin_1)) #......0.01......
        self.play(Write(bin_0)) 
        self.wait(0, 27) #......和0.001的循环来表示
        self.wait(0, 17) #（空闲）

        self.play(FadeOut(bin_1, run_time = 0.5), FadeOut(bin_0, run_time = 0.5), Cut(position), frac.animating(**paras).move_to(position + 0.5*DOWN), left.animating(**paras).set_x(-16/3).set_stroke(width = 4*ratio_s), right.animating(**paras).set_x(-8/3).set_stroke(width = 4*ratio_s))
        self.wait(0, 15) #于是我们也得在这再切一刀
        self.wait(0, 18) #（空闲）

        intervals_2 = [left, right]
        line, left, right = halve(interval_2)
        intervals_2 = intervals_2 + [left.set_stroke(width = 4*ratio_s**2), right.set_stroke(width = 4*ratio_s**2)]
        position = line.get_start()
        alpha = ValueTracker(0.0)
        t = 4/3 - 3/8
        bin_1 = MTex(r"0.11", color = GREEN).scale(0.8).next_to(line, UR, buff = 0.1).save_state().add_updater(bin_updater(t*RIGHT))
        bin_0 = MTex(r"0.10\dot1", color = BLUE).scale(0.8).next_to(line, UL, buff = 0.1).save_state().add_updater(bin_updater(t*LEFT))
        frac = MTex(r"\frac34", color = TEAL).set_opacity(ratio_o**2).scale(ratio**2).next_to(line, DOWN)
        self.play(ShowCreation(line), Write(frac))
        self.remove(line, interval_2).add(left, right, bin_1, bin_0).play(alpha.animating(rate_func = linear).set_value(1), Cut(position), frac.animating(**paras).move_to(position + 0.5*DOWN), left.animating(**paras).shift(t*LEFT).set_stroke(width = 4*ratio_s), right.animating(**paras).shift(t*RIGHT).set_stroke(width = 4*ratio_s))
        self.remove(bin_1, bin_0).wait(0, 10) #同样地 3/4的位置也有一刀
        self.wait(0, 19) #（空闲）
        
        halves = [halve(interval) for interval in intervals_2]
        lines, lefts, rights = [triple[0] for triple in halves], [triple[1] for triple in halves], [triple[2] for triple in halves]
        positions = [line.get_start() for line in lines]
        texs = [r"\frac18", r"\frac38", r"\frac58", r"\frac78"]
        fracs = [MTex(texs[i], color = TEAL).set_opacity(ratio_o**3).scale(ratio**3).next_to(positions[i], DOWN) for i in range(4)]
        alpha = ValueTracker(0.0)
        t = 4/9 - 3/16
        texs = [r"0.001", r"0.011", r"0.101", r"0.111"]
        bins_1 = [MTex(texs[i], color = GREEN).scale(ratio**3).next_to(positions[i] + 0.5*UP, UR, buff = 0.1).save_state().add_updater(bin_updater(t*RIGHT)) for i in range(4)]
        texs = [r"0.000\dot1", r"0.010\dot1", r"0.100\dot1", r"0.110\dot1"]
        bins_0 = [MTex(texs[i], color = BLUE).scale(ratio**3).next_to(positions[i] + 0.5*UP, UL, buff = 0.1).save_state().add_updater(bin_updater(t*LEFT)) for i in range(4)]
        self.wait(1, 19) #然而这还没完
        self.play(LaggedStart(*[ShowCreation(line) for line in lines], lag_ratio = 1/3, run_time = 2), LaggedStart(*[Write(frac) for frac in fracs], lag_ratio = 1/3, run_time = 2))
        self.remove(*intervals_2, *lines).add(*lefts, *rights).wait(0, 23) #这四条线段的中点也有两种表示
        self.add(*bins_1, *bins_0).play(alpha.animating(rate_func = linear).set_value(1), *[fracs[i].animating(**paras).move_to(positions[i] + 0.5*DOWN) for i in range(4)], *[Cut(position) for position in positions], *[mob.animating(**paras).shift(t*LEFT).set_stroke(width = 4*ratio_s**2) for mob in lefts], *[mob.animating(**paras).shift(t*RIGHT).set_stroke(width = 4*ratio_s**2) for mob in rights])
        self.remove(*bins_1, *bins_0, alpha).wait(1+0-1, 4+16-15) #也都得来一刀 （空闲）

        intervals_3 = [line for triple in halves for line in triple[1:]]
        halves = [halve(interval) for interval in intervals_3]
        lines, lefts, rights = [triple[0] for triple in halves], [triple[1] for triple in halves], [triple[2] for triple in halves]
        positions = [line.get_start() for line in lines]
        texs = [r"\frac{"+str(2*i+1)+r"}{16}"  for i in range(8)]
        fracs = [MTex(texs[i], color = TEAL).set_opacity(ratio_o**4).scale(ratio**4).next_to(positions[i], DOWN) for i in range(8)]
        t = 4/27 - 3/32
        self.play(LaggedStart(*[ShowCreation(line) for line in lines], lag_ratio = 1/7, run_time = 2), LaggedStart(*[Write(frac) for frac in fracs], lag_ratio = 1/7, run_time = 2))
        self.remove(*intervals_3, *lines).add(*lefts, *rights).play(*[fracs[i].animating(**paras).move_to(positions[i] + 0.5*DOWN) for i in range(8)], *[Cut(position) for position in positions], *[mob.animating(**paras).shift(t*LEFT).scale(np.array([2/3, 1, 1])).set_stroke(width = 4*ratio_s**3) for mob in lefts], *[mob.animating(**paras).shift(t*RIGHT).scale(np.array([2/3, 1, 1])).set_stroke(width = 4*ratio_s**3) for mob in rights])
        self.wait(1+1+0-3, 23+19+18-15) #而切出来的八条线段 它们的中点也一样 （空闲）
        intervals = [line for triple in halves for line in triple[1:]]
        
        for index in range(4, 7):
            numbers = 2**index
            halves = [halve(interval) for interval in intervals]
            lines, lefts, rights = [triple[0] for triple in halves], [triple[1] for triple in halves], [triple[2] for triple in halves]
            positions = [line.get_start() for line in lines]
            texs = [r"\frac{"+str(2*i+1)+r"}{"+str(2*numbers)+"}"  for i in range(numbers)]
            fracs = [MTex(texs[i], color = TEAL).set_opacity(ratio_o**(index+1)).scale(ratio**(2*index-3)).next_to(positions[i], DOWN) for i in range(numbers)]
            t /= 3
            self.play(LaggedStart(*[ShowCreation(line) for line in lines], lag_ratio = 1/(numbers-1), run_time = 2), LaggedStart(*[Write(frac) for frac in fracs], lag_ratio = 1/(numbers-1), run_time = 2))
            self.remove(*intervals, *lines).add(*lefts, *rights).play(*[fracs[i].animating(**paras).move_to(positions[i] + 0.5*DOWN) for i in range(numbers)], *[Cut(position) for position in positions], *[mob.animating(**paras).shift(t*LEFT).scale(np.array([2/3, 1, 1])).set_stroke(width = 4*ratio_s**index) for mob in lefts], *[mob.animating(**paras).shift(t*RIGHT).scale(np.array([2/3, 1, 1])).set_stroke(width = 4*ratio_s**index) for mob in rights])
            self.wait(0, 15)
            intervals = [line for triple in halves for line in triple[1:]]
        self.wait(1+2+2+0+2+2-12, 11+25+22+29+6+11) #就这样下去 每条线段都会被我们不断地切成两半 最终我们得到的 是这样的一堆散点 （空闲） 但毕竟断点有无数个 我们怎么能把这无穷刀全部切完呢
        self.wait(0, 19) #（空闲）
        
        self.play(self.change_notice())
        self.wait(0, 26) #其实不用担心这个
        self.wait(2, 17) #有另一种方法可以直接获得这一堆散点
        self.wait(0, 22) #（空闲）
        self.fade_out(run_time = 0.5)

        interval = Interval(6*LEFT, 6*RIGHT, height = 0.5)
        marks_1 = [marks_0[0], marks_0[2]]
        self.fade_in(interval, *marks_1, run_time = 0.5)
        self.wait(1, 0) #我们还是从[0,1]出发
        self.wait(0, 18) #（空闲）

        line_l, line_r, left, middle, right = trisect(interval)
        self.wait(1, 0) #第一步......
        self.play(ShowCreation(line_l), ShowCreation(line_r))
        self.remove(line_l, line_r, interval).add(left, middle, right).wait(0, 19) #......三等分这个区间
        self.play(FadeOut(middle, 0.5*UP))
        self.wait(0, 26) #然后取走中间那份
        self.play(Indicate(left), Indicate(right))
        self.wait(0, 11) #留下两端的闭区间
        self.wait(0, 21) #（空闲）

        intervals = [left, right]
        parts = [trisect(interval) for interval in intervals]
        lines_l, lines_r, lefts, middles, rights = [quintuple[0] for quintuple in parts], [quintuple[1] for quintuple in parts],[quintuple[2] for quintuple in parts], [quintuple[3] for quintuple in parts], [quintuple[4] for quintuple in parts]
        self.wait(1, 0) #第二步......
        self.play(*[ShowCreation(mob) for mob in lines_l + lines_r])
        self.remove(*lines_l, *lines_r, *intervals).add(*lefts, *middles, *rights).wait(1, 13) #......再三等分两端的这两个区间
        self.play(*[FadeOut(mob, 0.5*UP) for mob in middles])
        self.wait(1, 5) #并且也取走各自的中间那份
        self.wait(0, 22) #（空闲）
        intervals = lefts + rights

        for i in range(1, 6):
            parts = [trisect(interval) for interval in intervals]
            lines_l, lines_r, lefts, middles, rights = [quintuple[0] for quintuple in parts], [quintuple[1] for quintuple in parts],[quintuple[2] for quintuple in parts], [quintuple[3] for quintuple in parts], [quintuple[4] for quintuple in parts]
            self.play(*[ShowCreation(mob) for mob in lines_l + lines_r])
            self.remove(*lines_l, *lines_r, *intervals).add(*lefts, *middles, *rights)
            intervals = lefts + rights
            self.play(*[FadeOut(mob, 0.5*UP) for mob in middles], *[mob.animate.set_stroke(width = 4*ratio**i) for mob in intervals])
        self.wait(3+2+0+3+0-10, 11+7+19+17+28) #这种操作和我们之前的切分操作如出一辙 最终也能得到同样的一堆散点 （空闲） 不过这次 我们有其它的办法来刻画这个操作 （空闲）

        self.fade_out(run_time = 0.5, excepts = marks_1)
        self.tip = Simsun(r"*所有小数均为三进制小数").scale(0.4).next_to(self.notice, LEFT).set_x(-5)
        self.fade_in(interval, self.tip, excepts = marks_1, run_time = 0.5)
        self.wait(1, 6) #这个办法就是使用三进制小数
        self.wait(0, 20) #（空闲）

        positions = [interpolate(6*LEFT, 6*RIGHT, i/7) for i in range(1, 7)]
        points = [Dot(position) for position in positions]
        fracs = [MTex(r"\frac"+str(i+1)+r"7", color = TEAL).scale(0.8).next_to(positions[i], UP) for i in range(6)]
        texs = [r"0.\dot01021\dot2", r"0.\dot02120\dot1", r"0.\dot10212\dot0", r"0.\dot12010\dot2", r"0.\dot20102\dot1", r"0.\dot21201\dot0"]
        ters = [MTex(texs[i], color = YELLOW).scale(0.6).next_to(positions[i], DOWN) for i in range(6)]
        self.play(*[LaggedStart(*[FadeIn(mob) for mob in mobs], run_time = 2, lag_ratio = 0.2) for mobs in [points, fracs, ters]])
        self.wait(0, 17) #我们可以在数轴上取一些点作为例子
        self.wait(0, 18) #（空闲）

        self.play(ShowCreation(line_l), ShowCreation(line_r))
        digits_1 = [MTex(r"0."+str(i)+r"\cdots", color = YELLOW).shift((i-1)*4*RIGHT + 2*UP) for i in range(3)]
        self.wait(0, 28) #在第一次三等分的时候
        self.remove(line_l, line_r, interval).add(middle, left, right).play(*[mob.animate.set_color(interpolate_color(WHITE, BACK, 0.5)) for mob in [middle, points[2], points[3]]], *[mob.animate.fade() for mob in fracs[2:4] + ters[2:4]])
        self.play(Write(digits_1[1], rate_func = squish_rate_func(smooth, 0.5, 1)), *[Transform(mob, mob.copy().scale(1.2).set_fill(color = WHITE, opacity = 1), rate_func = double_there_and_back) for mob in [ters[2][3], ters[3][3]]], run_time = 2)
        self.wait(0, 5) #去掉的所有数 小数点后第一位都是1
        self.wait(0, 17) #（空闲）

        self.play(Write(digits_1[0]), Write(digits_1[2]), *[Transform(ters[i][3], ters[i][3].copy().scale(1.2).set_fill(color = WHITE, opacity = 1), rate_func = double_there_and_back) for i in [0, 1, 4, 5]], run_time = 2)
        self.wait(0, 17) #而小数点后第一位是0或2的
        self.wait(1, 4) #都保留了下来
        self.wait(0, 18) #（空闲）

        self.play(*[FadeOut(mob) for mob in points + fracs + ters], self.change_notice())
        marks_1 = marks_1 + [MTex(r"\frac13", color = TEAL).scale(0.8).next_to(2*LEFT, DOWN), MTex(r"\frac23", color = TEAL).scale(0.8).next_to(2*RIGHT, DOWN)]
        self.play(Write(marks_1[2]), Write(marks_1[3]))
        self.wait(0, 23) #这里我想请大家关注一下两个端点的位置
        self.wait(0, 17) #（空闲）

        ter_0 = MTex(r"0.0\dot2", color = BLUE).next_to(2*LEFT + 0.25*UP, UL)
        ter_1 = MTex(r"0.1", color = GREEN).next_to(2*LEFT + 0.25*UP, UR)
        self.play(Write(ter_0), Transform(Line(2*LEFT, 2*LEFT + 0.5*UP), Line(2*LEFT, 2*LEFT + 0.5*UP, color = YELLOW, stroke_width = 8), run_time = 2, remover = True, rate_func = double_there_and_back))
        self.wait(0, 29) #这个端点因为能表示成0.02的循环
        self.wait(2, 0) #所以它被保留了下来
        self.play(Write(ter_1))
        self.wait(1, 15) #而它另一种表示 0.1
        self.play(ter_1.animate.fade())
        self.wait(0, 18) #实际上已经被删掉了
        self.wait(0, 21) #（空闲）

        ter_2 = MTex(r"0.1\dot2", color = BLUE).next_to(2*RIGHT + 0.25*UP, UL)
        ter_3 = MTex(r"0.2", color = GREEN).next_to(2*RIGHT + 0.25*UP, UR)
        self.play(Transform(Line(2*RIGHT, 2*RIGHT + 0.5*UP), Line(2*RIGHT, 2*RIGHT + 0.5*UP, color = YELLOW, stroke_width = 8), run_time = 2, remover = True, rate_func = double_there_and_back))
        self.play(Write(ter_3))
        self.wait(1, 12) #是因为它可以表示成0.2
        self.play(Write(ter_2))
        self.wait(0, 20) #它也有另一种表示......
        self.play(ter_2.animate.fade())
        self.wait(0, 5) #......但也被删掉了
        self.wait(0, 17) #（空闲）

        intervals = [left, right]
        parts = [trisect(interval) for interval in intervals]
        lines_l, lines_r, lefts, middles, rights = [quintuple[0] for quintuple in parts], [quintuple[1] for quintuple in parts],[quintuple[2] for quintuple in parts], [quintuple[3] for quintuple in parts], [quintuple[4] for quintuple in parts]
        digits_2 = [MTex(r"0."+str(i_1)+str(i_2)+r"\cdots", color = YELLOW).scale(0.5).shift(((i_1-1)*4+(i_2-1)*4/3)*RIGHT + 4/3*UP) for i_1 in (0, 2) for i_2 in range(0, 3)]
        self.play(*[FadeOut(mob) for mob in [ter_0, ter_1, ter_2, ter_3, digits_1[1], middle]], *[ShowCreation(mob) for mob in lines_l + lines_r])
        del digits_1[1]
        self.remove(*intervals, *lines_l, *lines_r).add(*middles, *lefts, *rights).play(*[Write(mob) for mob in digits_2], *[mob.animate.fade() for mob in middles])
        self.wait(0, 28) #接下来 第二步取走的两个区间
        self.play(*[FadeOut(mob) for mob in middles + digits_2[1::3]])
        del digits_2[1::3]
        self.wait(2, 17) #实际上就是取走了所有小数点后第二位是1的小数
        self.wait(0, 17) #（空闲）

        ratio = 0.5
        ratio_o = 0.8
        ratio_s = 0.8
        intervals = lefts + rights
        parts = [trisect(interval) for interval in intervals]
        lines_l, lines_r, lefts, middles, rights = [quintuple[0] for quintuple in parts], [quintuple[1] for quintuple in parts],[quintuple[2] for quintuple in parts], [quintuple[3] for quintuple in parts], [quintuple[4] for quintuple in parts]
        digits_3 = [MTex(r"0."+str(i_1)+str(i_2)+str(i_3)+r"\cdots", color = YELLOW).set_opacity(ratio_o).scale(1/3*ratio).shift(((i_1-1)*4+(i_2-1)*4/3+(i_3-1)*4/9)*RIGHT + (2/3 + (4/3)/4)*UP) for i_1 in (0, 2) for i_2 in (0, 2) for i_3 in range(0, 3)]
        self.play(*[Write(mob) for mob in digits_3], *[ShowCreation(mob) for mob in lines_l + lines_r])
        self.remove(*intervals, *lines_l, *lines_r).add(*middles, *lefts, *rights).play(*[FadeOut(mob) for mob in middles + digits_3[1::3]], *[mob.animate.set_stroke(width = 4*ratio_s) for mob in lefts + rights])
        del digits_3[1::3]

        intervals = lefts + rights
        parts = [trisect(interval) for interval in intervals]
        lines_l, lines_r, lefts, middles, rights = [quintuple[0] for quintuple in parts], [quintuple[1] for quintuple in parts],[quintuple[2] for quintuple in parts], [quintuple[3] for quintuple in parts], [quintuple[4] for quintuple in parts]
        digits_4 = [MTex(r"0."+str(i_1)+str(i_2)+str(i_3)+str(i_4)+r"\cdots", color = YELLOW).set_opacity(ratio_o**2).scale(1/3*ratio**2).shift(((i_1-1)*4+(i_2-1)*4/3+(i_3-1)*4/9+(i_4-1)*4/27)*RIGHT + (2/3 + (4/3)/8)*UP) for i_1 in (0, 2) for i_2 in (0, 2) for i_3 in (0, 2) for i_4 in range(0, 3)]
        self.play(*[Write(mob) for mob in digits_4], *[ShowCreation(mob) for mob in lines_l + lines_r])
        self.remove(*intervals, *lines_l, *lines_r).add(*middles, *lefts, *rights).play(*[FadeOut(mob) for mob in middles + digits_4[1::3]], *[mob.animate.set_stroke(width = 4*ratio_s**2) for mob in lefts + rights])
        del digits_4[1::3]

        intervals = lefts + rights
        parts = [trisect(interval) for interval in intervals]
        lines_l, lines_r, lefts, middles, rights = [quintuple[0] for quintuple in parts], [quintuple[1] for quintuple in parts],[quintuple[2] for quintuple in parts], [quintuple[3] for quintuple in parts], [quintuple[4] for quintuple in parts]
        digits_5 = [MTex(r"0."+str(i_1)+str(i_2)+str(i_3)+str(i_4)+str(i_5)+r"\cdots", color = YELLOW).set_opacity(ratio_o**3).scale(1/3*ratio**3).shift(((i_1-1)*4+(i_2-1)*4/3+(i_3-1)*4/9+(i_4-1)*4/27+(i_5-1)*4/81)*RIGHT + (2/3 + (4/3)/16)*UP) for i_1 in (0, 2) for i_2 in (0, 2) for i_3 in (0, 2) for i_4 in (0, 2) for i_5 in range(0, 3)]
        self.play(*[Write(mob) for mob in digits_5], *[ShowCreation(mob) for mob in lines_l + lines_r])
        self.remove(*intervals, *lines_l, *lines_r).add(*middles, *lefts, *rights).play(*[FadeOut(mob) for mob in middles + digits_5[1::3]], *[mob.animate.set_stroke(width = 4*ratio_s**3) for mob in lefts + rights])
        del digits_5[1::3]

        intervals = lefts + rights
        parts = [trisect(interval) for interval in intervals]
        lines_l, lines_r, lefts, middles, rights = [quintuple[0] for quintuple in parts], [quintuple[1] for quintuple in parts],[quintuple[2] for quintuple in parts], [quintuple[3] for quintuple in parts], [quintuple[4] for quintuple in parts]
        digits_6 = [MTex(r"0."+str(i_1)+str(i_2)+str(i_3)+str(i_4)+str(i_5)+str(i_6)+r"\cdots", color = YELLOW).set_opacity(ratio_o**4).scale(1/3*ratio**4).shift(((i_1-1)*4+(i_2-1)*4/3+(i_3-1)*4/9+(i_4-1)*4/27+(i_5-1)*4/81+(i_6-1)*4/243)*RIGHT + (2/3 + (4/3)/32)*UP) for i_1 in (0, 2) for i_2 in (0, 2) for i_3 in (0, 2) for i_4 in (0, 2) for i_5 in (0, 2) for i_6 in range(0, 3)]
        self.play(*[Write(mob) for mob in digits_6], *[ShowCreation(mob) for mob in lines_l + lines_r])
        self.remove(*intervals, *lines_l, *lines_r).add(*middles, *lefts, *rights).play(*[FadeOut(mob) for mob in middles + digits_6[1::3]], *[mob.animate.set_stroke(width = 4*ratio_s**4) for mob in lefts + rights])
        del digits_6[1::3]
        self.wait(1+2+0+1+3-8, 16+20+16+14+1) #接下来的每一步 都会取走相应位数上是1的所有小数 （空闲） 而最后剩下的数 小数点后面的所有数 不是0 就是2
        self.wait(0, 23) #（空闲）

        title = Title(r"康托集")
        title_line = TitleLine()
        self.play(Write(title), GrowFromCenter(title_line), self.change_notice())
        self.wait(1, 8) #这个集合被称作康托集
        self.play(*[FadeOut(mob) for mob in marks_1])
        self.wait(1, 7) #它和我们之前切出来的集合
        self.wait(1, 18) #有一个奇妙的一一对应
        self.wait(0, 16) #（空闲）

        self.tip_2 = Simsun(r"*所有小数均为二进制小数").scale(0.4).set_y(-self.notice.get_y() + 0.5).set_x(-5)
        digits_1_2 = [MTex(r"0."+str(i//2)+r"\cdots", color = TEAL).shift((i-1)*4*RIGHT + 1.5*DOWN) for i in (0, 2)]
        digits_2_2 = [MTex(r"0."+str(i_1//2)+str(i_2//2)+r"\cdots", color = TEAL).scale(0.5).shift(((i_1-1)*4+(i_2-1)*4/3)*RIGHT + 5/6*DOWN) for i_1 in (0, 2) for i_2 in (0, 2)]
        digits_3_2 = [MTex(r"0."+str(i_1//2)+str(i_2//2)+str(i_3//2)+r"\cdots", color = TEAL).set_opacity(ratio_o).scale(1/3*ratio).shift(((i_1-1)*4+(i_2-1)*4/3+(i_3-1)*4/9)*RIGHT + (1/6 + (4/3)/4)*DOWN) for i_1 in (0, 2) for i_2 in (0, 2) for i_3 in (0, 2)]
        digits_4_2 = [MTex(r"0."+str(i_1//2)+str(i_2//2)+str(i_3//2)+str(i_4//2)+r"\cdots", color = TEAL).set_opacity(ratio_o**2).scale(1/3*ratio**2).shift(((i_1-1)*4+(i_2-1)*4/3+(i_3-1)*4/9+(i_4-1)*4/27)*RIGHT + (1/6 + (4/3)/8)*DOWN) for i_1 in (0, 2) for i_2 in (0, 2) for i_3 in (0, 2) for i_4 in (0, 2)]
        digits_5_2 = [MTex(r"0."+str(i_1//2)+str(i_2//2)+str(i_3//2)+str(i_4//2)+str(i_5//2)+r"\cdots", color = TEAL).set_opacity(ratio_o**3).scale(1/3*ratio**3).shift(((i_1-1)*4+(i_2-1)*4/3+(i_3-1)*4/9+(i_4-1)*4/27+(i_5-1)*4/81)*RIGHT + (1/6 + (4/3)/16)*DOWN) for i_1 in (0, 2) for i_2 in (0, 2) for i_3 in (0, 2) for i_4 in (0, 2) for i_5 in (0, 2)]
        digits_6_2 = [MTex(r"0."+str(i_1//2)+str(i_2//2)+str(i_3//2)+str(i_4//2)+str(i_5//2)+str(i_6//2)+r"\cdots", color = TEAL).set_opacity(ratio_o**4).scale(1/3*ratio**4).shift(((i_1-1)*4+(i_2-1)*4/3+(i_3-1)*4/9+(i_4-1)*4/27+(i_5-1)*4/81+(i_6-1)*4/243)*RIGHT + (1/6 + (4/3)/32)*DOWN) for i_1 in (0, 2) for i_2 in (0, 2) for i_3 in (0, 2) for i_4 in (0, 2) for i_5 in (0, 2) for i_6 in (0, 2)]
        self.play(FadeIn(self.tip_2), *[Write(mob) for mob in digits_1_2])
        self.play(*[Write(mob) for mob in digits_2_2])
        self.play(*[Write(mob) for mob in digits_3_2])
        self.play(*[Write(mob) for mob in digits_4_2])
        self.play(*[Write(mob) for mob in digits_5_2])
        self.play(*[Write(mob) for mob in digits_6_2])
        self.wait(3+1+0+2-6, 5+24+24+22) #只需要把康托集中的所有2都换成1 我们就可以得到对应的数了 （空闲） 就这样 我们创造了一个集合
        self.wait(2, 27) #它能完美符合我们对小数比大小的直观
        self.wait(0, 18) #（空闲）
        self.wait(2, 28) #但问题是 这么做的代价是什么
        self.wait(3, 0)
        self.fade_out(end = True)
        self.wait(2, 5) #到此共215秒

#################################################################### 

class Chapter3_0(FrameScene):

    def construct(self):

        text3 = Simsun("第三节 康托集的大小", t2c={"第三节": YELLOW, "康托集": BLUE, "大小": GREEN})

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(FrameScene):
    CONFIG = {
        "camera_class": AACamera
    }
    def construct(self):
        self.notices = [Notice("困惑问题", "请　思考", anti_alias_width = 1.5), 
                        Notice("违规计算", "请勿模仿", anti_alias_width = 1.5).set_stroke(color = "#222222"), 
                        Notice("困惑问题", "请　思考", anti_alias_width = 1.5).set_stroke(color = "#222222"), 
                        Notice("重要性质", "请　接受", anti_alias_width = 1.5).set_stroke(color = "#222222"), 
                        Notice("重要性质", "请　接受", anti_alias_width = 1.5), 
                        ]
        self.notice = self.notices[0]

        offset = 0.5*UP
        old_lines = [Line(5*LEFT, 5*RIGHT)]
        for _ in range(6):
            lines = [line.copy().scale(1/3, about_point = 5*LEFT) for line in old_lines] + [line.copy().scale(1/3, about_point = 5*RIGHT) for line in old_lines]
            old_lines = lines
        cantor = VMobject(color = TEAL, stroke_width = 50, anti_alias_width = 0).set_points(VGroup(*old_lines).get_all_points()).shift(0.5*UP + offset)
        interval = Interval(5*LEFT, 5*RIGHT, 0.5, color = YELLOW).shift(0.75*DOWN + offset)
        shade = Shade(width = 12.2, height = 1).shift(0.25*DOWN)
        notice_cantor = MTex(r"\mathbb{B}", color = BLUE, anti_alias_width = 1.5).shift(5.5*LEFT + 0.5*UP + offset)
        notice_interval = MTex(r"\mathbb{I}", color = LIME, anti_alias_width = 1.5).shift(5.5*LEFT + 0.5*DOWN + offset)
        self.add(interval, shade, cantor, self.notice).play(Write(self.notice), ShowCreation(cantor, run_time = 2), shade.animating(run_time = 2, remover = True).shift(12.2*RIGHT))
        self.play(Write(notice_cantor), Write(notice_interval))
        self.wait(1+1-3, 24+28) #一个比较明显的问题是 康托集作为一个集合
        symbol = MTex(r"<").rotate(PI/2).shift(5.5*LEFT + offset)
        self.play(Write(symbol))
        self.wait(1, 7) #好像既大于[0, 1]
        self.play(Rotate(symbol))
        self.wait(0, 19) #又小于[0, 1]
        self.wait(0, 18) #（空闲）

        board_up = Rectangle(height = 4.1, width = 15.2, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 3.9, width = 15, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board_up.add(inner).shift(6.5*UP)
        interval_up = Interval(1.5*LEFT + 2*UP + offset, 1.5*RIGHT + 2*UP + offset, 0.5)
        tex_paras = {r"tex_to_color_map": {r"\mathbb{I}": LIME, r"\mathbb{B}": BLUE}, r"anti_alias_width": 1.5}
        texts = [r"\mathbb{I}", r"<\mathbb{I}+1", r"+2", r"+4", r"+8", r"+\cdots", r"= \mathbb{B}"]
        inequality_up = MTex("".join(texts), isolate = texts, **tex_paras).shift(3.15*UP + offset)
        parts_inequality = [inequality_up.get_part_by_tex(tex).save_state() for tex in texts]
        parts_copy = [part.copy().save_state() for part in parts_inequality]
        shades = [BackgroundRectangle(part, fill_opacity = 1, buff = 0.1).set_color("#222222") for part in parts_inequality]
        self.add(board_up, self.notice).play(self.notice.animate.set_stroke(color = "#222222"), FadeOut(symbol), board_up.animate.shift((3*DOWN + offset)), interval_up.shift(-(3*DOWN + offset)).animate.shift((3*DOWN + offset)), parts_inequality[0].set_x(0).shift(-(3*DOWN + offset)).animate.shift(3*DOWN + offset))
        
        ratio_s = 4/5
        line, left, right = halve(interval_up)
        position = line.get_start() + 0.25*UP
        d = 10/3
        l = 3/4
        t = d - l
        self.play(ShowCreation(line), rate_func = rush_into, run_time = 0.5)
        paras = {"rate_func": squish_rate_func(rush_from, 1/3, 1)}
        parts_inequality[1].set_x(parts_inequality[0].get_x(RIGHT), RIGHT)
        shades[1].move_to(parts_inequality[1])
        VGroup(*parts_copy[0:2]).set_x(0)
        self.remove(line, interval_up).add(left, right, parts_inequality[1], shades[1], parts_inequality[0]).play(self.change_notice(), Cut(position + 0.25*UP, 1.5, run_time = 2/3, rate_func = rush_from), left.animating(**paras).shift(t*LEFT).set_stroke(width = 4*ratio_s), right.animating(**paras).shift(t*RIGHT).set_stroke(width = 4*ratio_s), 
                                                          *[parts_inequality[i].animate.move_to(parts_copy[i]) for i in range(2)], shades[1].animating(remover = True).set_x(parts_copy[0].get_x(RIGHT) + 0.1, RIGHT))
        for i in range(2):
            parts_copy[i].restore()

        intervals_up = [left, right]
        for j in range(2, 7):
            halves = [halve(interval) for interval in intervals_up]
            lines, lefts, rights = [triple[0] for triple in halves], [triple[1] for triple in halves], [triple[2] for triple in halves]
            positions = [line.get_start() + 0.25*UP for line in lines]
            d = d/3
            l = l/2 if j <= 3 else l/3
            t = d-l
            self.play(*[ShowCreation(line) for line in lines], rate_func = rush_into, run_time = 0.5)
            parts_inequality[j].set_x(parts_inequality[j-1].get_x(RIGHT), RIGHT)
            shades[j].move_to(parts_inequality[j])
            VGroup(*parts_copy[0:j+1]).set_x(0)
            scale_factor = 1 if j == 2 else np.array([2/3, 1, 1])
            self.remove(*intervals_up, *lines).add(*lefts, *rights, parts_inequality[j], shades[j], *parts_inequality[0:j]).play(*[Cut(position + 0.25*UP, 1.5, run_time = 2/3, rate_func = rush_from) for position in positions], *[mob.animating(**paras).shift(t*LEFT).set_stroke(width = 4*ratio_s**j).scale(scale_factor) for mob in lefts], *[mob.animating(**paras).shift(t*RIGHT).set_stroke(width = 4*ratio_s**j).scale(scale_factor) for mob in rights], 
                                                            *[parts_inequality[i].animate.move_to(parts_copy[i]) for i in range(j+1)], shades[j].animating(remover = True).set_x(parts_copy[j-1].get_x(RIGHT) + 0.1, RIGHT))
            for i in range(j+1):
                parts_copy[i].restore()
            intervals_up = lefts + rights

        self.wait(2+3+1+3+0-10, 14+12+6+10+18) #在使用切分得到康托集的时候 每切一次 端点处就会多一个数 这样算下来 所有的切分一共向区间里面增加了无穷多个数 （空闲）

        board_down = Rectangle(height = 4.1, width = 15.2, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 3.9, width = 15, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board_down.add(inner).shift(6.5*DOWN)
        interval_down = Interval(5*LEFT + 3.25*DOWN + offset, 5*RIGHT + 3.25*DOWN + offset, 0.5)
        texts = [r"\mathbb{I}", r">\mathbb{I}-\infty", r"-{}\infty", r"-\infty{}", r"-{\infty}", r"-\cdots", r"= \mathbb{B}"]
        inequality_down = MTex("".join(texts), isolate = texts, **tex_paras).shift(2*DOWN + offset)
        parts_inequality = [inequality_down.get_part_by_tex(tex).save_state() for tex in texts]
        parts_copy = [part.copy().save_state() for part in parts_inequality]
        shades = [BackgroundRectangle(part, fill_opacity = 1, buff = 0.1).set_color("#222222") for part in parts_inequality]
        self.play(board_down.animate.shift(3*UP + offset), interval_down.shift(-(3*UP + offset)).animate.shift(3*UP + offset), parts_inequality[0].set_x(0).shift(-(3*UP + offset)).animate.shift(3*UP + offset))
        
        line_l, line_r, left, middle, right = trisect(interval_down)
        parts_inequality[1].set_x(parts_inequality[0].get_x(RIGHT), RIGHT)
        shades[1].move_to(parts_inequality[1])
        VGroup(*parts_copy[0:2]).set_x(0)
        self.play(ShowCreation(line_l), ShowCreation(line_r), run_time = 0.5, rate_func = rush_into)
        self.remove(line_l, line_r, interval_down).add(left, middle, right, parts_inequality[1], shades[1], parts_inequality[0]).play(FadeOut(middle, 0.5*UP, run_time = 0.5, rate_func = rush_from), *[parts_inequality[i].animate.move_to(parts_copy[i]) for i in range(2)], shades[1].animating(remover = True).set_x(parts_copy[0].get_x(RIGHT) + 0.1, RIGHT))
        for i in range(2):
            parts_copy[i].restore()

        intervals_down = [left, right]
        for j in range(2, 7):
            parts = [trisect(interval) for interval in intervals_down]
            lines_l, lines_r, lefts, middles, rights = [quintuple[0] for quintuple in parts], [quintuple[1] for quintuple in parts],[quintuple[2] for quintuple in parts], [quintuple[3] for quintuple in parts], [quintuple[4] for quintuple in parts]
            parts_inequality[j].set_x(parts_inequality[j-1].get_x(RIGHT), RIGHT)
            shades[j].move_to(parts_inequality[j])
            VGroup(*parts_copy[0:j+1]).set_x(0)
            self.play(*[ShowCreation(mob) for mob in lines_l + lines_r], run_time = 0.5, rate_func = rush_into)
            self.remove(*lines_l, *lines_r, *intervals_down).add(*lefts, *middles, *rights, parts_inequality[j], shades[j], *parts_inequality[0:j]).play(*[FadeOut(mob, 0.5*UP, run_time = 0.5, rate_func = rush_from) for mob in middles], *[mob.animate.set_stroke(width = 4*ratio_s**j) for mob in lefts + rights], 
                                                                                            *[parts_inequality[i].animate.move_to(parts_copy[i]) for i in range(j+1)], shades[j].animating(remover = True).set_x(parts_copy[j-1].get_x(RIGHT) + 0.1, RIGHT))
            for i in range(j+1):
                parts_copy[i].restore()
            intervals_down = lefts + rights
        self.wait(2+3+1+2+0-10, 18+6+8+16+18) #而在使用三进制得到康托集的时候 每取出一位 就删去了很多个数 这样算下来 一共向从区间里面删去了无穷多个数 （空闲）

        surr_1 = SurroundingRectangle(inequality_up.get_part_by_tex(r"\mathbb{B}")).save_state()
        surr_2 = SurroundingRectangle(inequality_down.get_part_by_tex(r"\mathbb{B}")).save_state()
        self.play(self.change_notice(), FadeIn(surr_1, run_time = 2, rate_func = double_there_and_back), FadeIn(surr_2, run_time = 2, rate_func = double_there_and_back))
        self.play(FadeIn(surr_1.restore()), FadeIn(surr_2.restore()), run_time = 0.5)
        self.wait(1+2-2, 14+22-15) #而这两种方法 最终居然能得到同样多的一堆散点
        self.wait(1, 10) #这是怎么一回事呢
        self.wait(0, 26) #（空闲）

        self.play(self.change_notice()) #答案是
        self.play(IndicateAround(inequality_up[1]), IndicateAround(inequality_down[1]))
        self.wait(1, 12) #我们直觉上认为的 “包含”意味着“更多”
        cross_1 = VGroup(Line(UR, DL), Line(DR, UL)).set_color(RED).scale(0.2).move_to(inequality_up[1])
        cross_2 = VGroup(Line(UR, DL), Line(DR, UL)).set_color(RED).scale(0.2).move_to(inequality_down[1])
        self.play(ShowCreation(cross_1), ShowCreation(cross_2))
        self.wait(1, 16) #在遇到无穷以后 就变得不适用了
        self.wait(0, 21) #（空闲）

        self.fade_out(change_notice = True)
        self.wait(0, 25) #举一个最简单的例子

        buff_h = 1
        buff_v = 0.8
        flint_blue = ImageMobject("flint_teal_enlarged.png", height = 0.8)
        flint_lime = ImageMobject("flint_yellow_enlarged.png", height = 0.8)
        flints_up = [flint_blue.copy().move_to((i-3.5)*buff_h*RIGHT + buff_v*UP) for i in range(8)]
        flints_down = [flint_lime.copy().move_to((i-3.5)*buff_h*RIGHT + buff_v*DOWN) for i in range(6)]
        line = DashedLine(2*UP + 2*buff_h*RIGHT, 2*DOWN + 2*buff_h*RIGHT)
        tex_up = MTex(r"8", color = BLUE, anti_alias_width = 1.5).scale(1.5).shift(5.5*LEFT + buff_v*UP)
        tex_down = MTex(r"6", color = LIME, anti_alias_width = 1.5).scale(1.5).shift(5.5*LEFT + buff_v*DOWN)
        tex_mid = MTex(r"<", anti_alias_width = 1.5).rotate(PI/2).scale(1.5).shift(5.5*LEFT)
        tex = VGroup(tex_up, tex_mid, tex_down)
        self.add(*flints_up, *flints_down).play(LaggedStart(*[FadeIn(mob, 0.5*RIGHT) for mob in flints_up], lag_ratio = 0.1, group = Group(), run_time = 1), LaggedStart(*[FadeIn(mob, 0.5*RIGHT) for mob in flints_down + [VMobject(), VMobject()]], lag_ratio = 0.1, group = Group(), run_time = 1))
        self.wait(0, 13) #对于两排石子
        self.play(ShowCreation(line))
        self.wait(1, 17) #如果上面这排要比下面这排长
        self.play(Write(tex))
        self.wait(0, 28) #那么上面的石子就更多一些
        self.wait(0, 18) #（空闲）

        shade = Shade(width = 8*buff_h)
        alpha = ValueTracker(0.0)
        def line_down_updater(mob: Interval):
            value = alpha.get_value()
            scale_factor = np.array([min(value*4/3, 1), 1, 1])
            mob.restore().scale(scale_factor, min_scale_factor = 0, about_point = 4*buff_h*LEFT)
        line_up = Interval(4*buff_h*LEFT, 4*buff_h*RIGHT, 0.5, color = TEAL, stroke_width = 8).shift((-0.25 + buff_v)*UP).save_state()
        line_down = Interval(4*buff_h*LEFT, 2*buff_h*RIGHT, 0.5, color = YELLOW, stroke_width = 8).shift((0.25 + buff_v)*DOWN).save_state().add_updater(line_down_updater)
        tip = Simsun("  只是线段的长度，\n不是线段里点的数量", color = YELLOW).scale(0.4).shift(5.5*LEFT + (buff_v + 1.5)*UP)
        arrow = Arrow(tip, tex, color = YELLOW)
        tip.add(arrow)
        self.add(shade, line_up, line_down, tex).play(alpha.animating(run_time = 2, rate_func = rush_from).set_value(1), shade.shift(8*buff_h*LEFT).animating(run_time = 2, rate_func = rush_from).shift(8*buff_h*RIGHT), tex.animate.set_color(GREY), line_up.scale(np.array([0, 1, 1]), min_scale_factor = 0, about_point = 4*buff_h*LEFT).animating(run_time = 2, rate_func = rush_from).restore())
        line_down.clear_updaters().restore()
        self.remove(shade, *flints_up, *flints_down, line).play(FadeIn(tip, 0.3*DOWN))
        self.wait(2+0-3, 15+17) #但要是我们换成两条线段就不一样了 （空闲）
        
        base = line_down.copy().set_color(interpolate_color(YELLOW, BACK, 0.5))
        self.bring_to_back(base).play(line_down.animate.shift(2*buff_v*UP))
        self.wait(3, 1) #虽然我们可以把底下这条线段平移进上面这条线段里面
        self.play(line_down.animate.restore())
        self.wait(0, 12) #但这样的包含
        self.wait(2, 12) #并不意味着上面的线段有更多的点
        self.wait(0, 18) #（空闲）

        alpha = ValueTracker(0.0)
        beta = ValueTracker(8.0)
        def dashed_line_updater(ratio: float):
            def util(mob: DashedLine):
                value_a, value_b = alpha.get_value(), beta.get_value()
                start, end = 4*buff_h*LEFT + 6*ratio*RIGHT + (0.25 + buff_v)*DOWN, 4*buff_h*LEFT + value_b*ratio*RIGHT + (-0.25 + buff_v)*UP
                mob.set_points(DashedLine(start, interpolate(start, end, value_a)).get_all_points())
            return util
        dashed_lines = [VMobject(color = [interpolate_color(YELLOW, BACK, 0.5), YELLOW]).add_updater(dashed_line_updater(i/10)) for i in range(11)]
        self.bring_to_back(*dashed_lines).play(alpha.animate.set_value(1), line_down.animate.scale(np.array([4/3, 1, 1])).move_to(line_up))
        self.wait(1, 11) #底下这条线段同样可以缩放
        self.wait(2, 5) #然后和上面的线段重合
        self.play(beta.animate.set_value(10), line_down.animate.scale(np.array([5/4, 1, 1]), about_point = 4*buff_h*LEFT))
        self.wait(1, 3) #甚至能把上面的线段包进来
        self.wait(0, 25) #（空闲）

        self.fade_out()
        self.fade_in(notice_cantor, notice_interval, cantor, interval)
        self.wait(1, 0) #而康托集和[0, 1]之间的关系
        self.wait(1, 4) #也和这个类似
        self.wait(0, 21) #（空闲）

        board_down = Rectangle(height = 4.1, width = 15.2, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 3.9, width = 15, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board_down.add(inner).shift(6.5*DOWN)
        cantor_down = cantor.copy().set_color(WHITE).shift(3.5*DOWN)
        equation_down = MTex(r"\mathbb{B}=\mathbb{I}-\infty-\infty-\infty-\infty-\cdots", **tex_paras).shift(2*DOWN + offset)
        self.play(board_down.animate.shift(3*UP + offset), *[mob.shift(-(3*UP + offset)).animate.shift(3*UP + offset) for mob in [cantor_down, equation_down]])
        self.wait(2, 15) #既有把康托集包含到[0, 1]里的映射

        board_up = Rectangle(height = 4.1, width = 15.2, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 3.9, width = 15, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board_up.add(inner).shift(6.5*UP)
        cantor_up = cantor.copy().set_color(WHITE).shift(1.75*UP)
        equation_up = MTex(r"\mathbb{B} = \mathbb{I}+1+2+4+8+\cdots", **tex_paras).shift(3.15*UP + offset)
        self.add(board_up, self.notice).play(self.notice.animate.set_stroke(color = "#222222"), board_up.animate.shift((3*DOWN + offset)), *[mob.shift(-(3*DOWN + offset)).animate.shift((3*DOWN + offset)) for mob in [cantor_up, equation_up]])
        self.wait(2, 0) #也有把[0, 1]包含到康托集里的映射
        self.wait(0, 20) #（空闲）

        inequality_up = MTex(r"\mathbb{B} \not< \mathbb{I}", **tex_paras)
        inequality_up.shift(equation_up[0].get_center() - inequality_up[0].get_center()).set_x(-6, LEFT)
        inequality_down = MTex(r"\mathbb{B} \not> \mathbb{I}", **tex_paras)
        inequality_down.shift(equation_down[0].get_center() - inequality_down[0].get_center()).set_x(-6, LEFT)
        inequality_up = VGroup(inequality_up[0], inequality_up[2], inequality_up[1].set_color(RED), inequality_up[3])
        inequality_down = VGroup(inequality_down[0], inequality_down[2], inequality_down[1].set_color(RED), inequality_down[3])
        self.wait(2, 5) #这两个映射既然都存在
        self.play(Write(inequality_up), Write(inequality_down))
        self.wait(3, 8) #那肯定就都不能说明康托集和[0, 1]哪个包含了更多的点
        self.wait(0, 21) #（空闲）

        equal = MTex(r"=").rotate(PI/2).shift(5.5*LEFT + offset)
        self.wait(2, 4) #如果我们非得给它们比个大小
        self.play(Write(equal))
        self.wait(1, 12) #那就称它们俩所含的点一样多吧
        self.wait(1, 1) #（空闲）

        self.play(self.notice.animate.set_stroke(color = BACK), *[mob.animating(remover = True).shift(-(3*DOWN + offset)) for mob in [board_up, cantor_up, equation_up, inequality_up]], *[mob.animating(remover = True).shift(-(3*UP + offset)) for mob in [board_down, cantor_down, equation_down, inequality_down]])
        self.wait(2, 5) #当然 两个集合所含的点一样多
        pos_left, pos_right, pos_down = 1*UP + 5/3*LEFT, 1*UP + 5/3*RIGHT, 0.25*DOWN
        bins = [MTex(r"(0.0\dot1)_2", color = TEAL).next_to(pos_left + 0.25*UP, UP), MTex(r"(0.1)_2", color = TEAL).next_to(pos_right + 0.25*UP, UP)]
        lines = [Line(pos_left + 0.3*UP, pos_left + 0.3*DOWN, stroke_width = 2), Line(pos_right + 0.3*UP, pos_right + 0.3*DOWN, stroke_width = 2)]
        frac = MTex(r"\frac{1}{2}", color = YELLOW).next_to(pos_down, DOWN)
        point = Dot(pos_down)
        arrow_1, arrow_2 = Arrow(pos_left + 0.25*DOWN, pos_down, color = [TEAL, YELLOW]), Arrow(pos_right + 0.25*DOWN, pos_down, color = [TEAL, YELLOW])
        self.play(*[Write(mob) for mob in bins + [frac]], *[ShowCreation(mob) for mob in lines + [point]])
        self.play(ShowCreation(arrow_1), ShowCreation(arrow_2))
        self.wait(1, 18) #并不影响我们可以把好几个小数对应到同一个实数上
        self.wait(0, 18) #（空闲）

        self.wait(2, 5) #就像是最通用的对应方法
        self.wait(3, 10) #我们会把1和0.9的循环对应到同一个实数上
        self.wait(0, 20) #（空闲）
        self.wait(3, 18) #甚至 再给小数多加一些位数也是可行的
        self.wait(0, 16) #（空闲）

        hyperreal = MTex(r"(0.\dot01)_2\notin \mathbb{B}", tex_to_color_map = {r"(0.\dot01)_2": PURPLE_A, r"\mathbb{B}": BLUE})
        hyperreal_1 = hyperreal[0:8]
        center_old = hyperreal_1.get_center().copy()
        offset = hyperreal_1.next_to(2*UP + 5*LEFT, UP).get_center() - center_old
        hyperreal_2 = hyperreal[8:].shift(offset)
        self.play(Write(hyperreal_1))
        self.wait(1, 25) #比如说 我们大可以定义一个小数
        self.wait(1, 29) #它在无穷多个0以后有一个1
        self.wait(0, 19) #（空闲）

        arrow_3 = Arrow(hyperreal_1, 1.25*UP + 5*LEFT, buff = 0.1, color = [PURPLE_A, TEAL])
        self.play(Write(hyperreal_2))
        self.wait(1, 12) #这样的小数当然不在康托集里
        self.play(ShowCreation(arrow_3))
        self.wait(2, 5) #但要是把康托集挤一挤 还是能放得下的
        self.wait(0, 20) #（空闲）

        arrow_4 = Arrow(0.75*UP + 5*LEFT, 0.25*UP + 5*LEFT, buff = 0.05, color = [TEAL, YELLOW])
        self.play(ShowCreation(arrow_4))
        self.wait(1, 4) #不过它对应什么实数呢
        zero = MTex(r"0", color = YELLOW).shift(np.array([-5, frac.get_y(), 0]))
        self.play(Write(zero))
        self.wait(0, 24) #只不过是一个简单的0而已
        self.wait(2, 8)
        self.fade_out(end = True)
        self.wait(2, 0) #到此共134秒
        
#################################################################### 

class Summary(FrameScene):

    def construct(self):
        self.notices = [Notice("良心视频", "请　三连"), 
                        Notice("下期预告", "敬请期待"), 
                        Notice("良心up主", "请　关注")]
        self.notice = self.notices[0]

        self.play(Write(self.notice))
        self.wait(0, 26) #非常感谢大家能看到这里
        self.wait(0, 18) #（空闲）

        decs_text = MTexText(r"作为小数：$0.\dot9\ne 1$", tex_to_color_map = {r"0.\dot9": BLUE, r"1": GREEN, r"小": TEAL}).shift(0.5*UP)
        reals_text = MTexText(r"作为实数：$0.\dot9 = 1$", tex_to_color_map = {r"0.\dot9": BLUE, r"1": GREEN, r"实": YELLOW}).shift(0.5*DOWN)

        self.play(FadeIn(decs_text, 0.5*DOWN), FadeIn(reals_text, 0.5*UP))
        self.wait(2, 28) #1和0.9的循环的关系 也算是一个经久不衰的话题了
        self.wait(0, 18) #（空闲）

        self.play(IndicateAround(decs_text))
        self.wait(0, 20) #它们作为两个小数自然是不同的
        self.play(IndicateAround(reals_text))
        self.wait(0, 10) #但这不妨碍它们表示同一个实数
        self.wait(0, 21) #（空闲）

        discuss_dec = MTexText(r"\small“因为$0.\dot9$(小数)和$1$(小数)之间插不进别的(小)数，所以它们是同一个(小)数”", tex_to_color_map = {r"0.\dot9": BLUE, r"1": GREEN, (r"小", r"小数"): TEAL}).scale(0.75).shift(1.5*UP)
        discuss_real = MTexText(r"\small“因为$0.\dot9$(实数)和$1$(实数)之间插不进别的(实)数，所以它们是同一个(实)数”", tex_to_color_map = {r"0.\dot9": BLUE, r"1": GREEN, (r"实", r"实数"): YELLOW}).scale(0.75).shift(1.5*DOWN)
        wrong = Text(r"✗", font = "simsun", color = RED).scale(0.8).next_to(discuss_dec, LEFT)
        right = MTex(r"\checkmark", color = GREEN).scale(0.8).next_to(discuss_real, LEFT)
        self.play(Write(discuss_dec), Write(discuss_real))
        self.play(Write(wrong), Write(right))
        self.wait(2+2-3, 26+24) #不过可能是因为我们对小数比较熟悉 大家很容易从小数出发来理解它们
        self.wait(1, 23) #而这会造成一定的误解
        self.wait(0, 22) #（空闲）

        self.wait(2, 15) #我特意选用了这个视角来解释问题
        self.wait(1, 24) #希望能有助于大家的理解
        self.wait(0, 17) #（空闲）

        self.clear().add(self.notice)
        like = Text("", font = 'vanfont').scale(2).shift(3*LEFT)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').scale(2).shift(3*RIGHT)
        sanlian = VGroup(like, coin, star)
        self.play(*[GrowFromCenter(mob) for mob in sanlian])
        self.play(sanlian.animate.set_color("#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian])
        self.wait(1+2-2, 19+22) #如果你看了这期视频 理解了小数和实数之间微妙的差别
        self.wait(1, 24) #不妨一键三连支持一下
        self.wait(0, 20) #（空闲）

        self.fade_out(run_time = 0.5)
        self.fade_in(decs_text, reals_text, discuss_dec, discuss_real, wrong, right, run_time = 0.5)
        self.wait(1, 17) #不知道大家还有没有像这个话题一样
        self.wait(3, 1) #感觉哪里不对 又说不太清楚的问题呢
        self.wait(1, 22) #欢迎在评论区下方留言
        self.wait(0, 22) #（空闲）

        image_1 = ImageMobject("Patch1_1.png", height = 8)
        image_2 = ImageMobject("Patch1_2.png", height = 8)
        self.fade_out(change_notice = True)
        self.fade_in(image_1, image_2)
        self.wait(0, 26) #下期视频我打算讲一讲坐标和坐标系是什么
        self.wait(0, 18) #（空闲）
        self.wait(2, 12) #这也是理解弯曲空间的基本功之一
        self.wait(0, 13) #（空闲）
        self.wait(3, 5) #虽然我们在日常生活中见到的坐标系还挺少的
        self.wait(0, 12) #（空闲）

        line = Line(LEFT_SIDE, RIGHT_SIDE)
        self.play(FadeOut(image_1, 0.5*np.array([-16/9, 1, 0])), FadeOut(image_2, 0.5*np.array([-16/9, -1, 0])), ShowCreation(line))
        self.wait(1)
        coordinates_1 = [MTex(str(i)).scale(0.6).next_to(i*RIGHT, DOWN) for i in range(-7, 8)]
        self.play(LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in coordinates_1], lag_ratio = 0.1, run_time = 1))
        self.wait(1)
        coordinates_2 = [MTex(f"{i**3/6:.2f}").scale(0.6).next_to(i*RIGHT, UP) for i in range(-7, 8)]
        self.play(LaggedStart(*[FadeOut(mob, 0.3*DOWN) for mob in coordinates_1], lag_ratio = 0.1, run_time = 1), LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in coordinates_2], lag_ratio = 0.1, run_time = 1))
        self.wait(1)
        coordinates_3 = [MTex(f"{5*np.tanh(i/2):.2f}").scale(0.6).next_to(i*RIGHT, DOWN) for i in range(-7, 8)]
        self.play(LaggedStart(*[FadeOut(mob, 0.3*UP) for mob in coordinates_2], lag_ratio = 0.1, run_time = 1), LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in coordinates_3], lag_ratio = 0.1, run_time = 1))
        self.wait(1)
        coordinates_4 = [MTex(f"{np.exp(i):.2f}").scale(0.6).next_to(i*RIGHT, UP) for i in range(-7, 8)]
        self.play(LaggedStart(*[FadeOut(mob, 0.3*DOWN) for mob in coordinates_3], lag_ratio = 0.1, run_time = 1), LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in coordinates_4], lag_ratio = 0.1, run_time = 1))
        self.wait(3+0+4+1-9, 15+21+10+0) #但事实上 坐标和坐标系的选择相当随意 （空闲） 在下期视频 我打算详细讲讲这种随意的优势和劣势 （空闲）

        painting = StarrySky()
        star = painting.star
        self.clear().play(FadeIn(painting, lag_ratio = 0.01, run_time = 2), self.change_notice())
        # self.wait(0, 0) #知识的星空浩如烟海

        picture_photo = ImageMobject("photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, 0.5*UP), FadeIn(text_name, 0.5*UP))
        self.wait(1+2-3, 28+10) #而我 就像我的名字一样

        self.play(FadeOut(painting.others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star.shift, DOWN))
        self.wait(1, 1) #想要把天上的星星垂下来

        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), stroke_color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, stroke_color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star, apple))
        self.wait(1, 1) #变成触手可及的果实

        snowflake = SnowFlake()
        snowflake_2 = snowflake.copy().set_color(RED).set_stroke(width = 1.5)
        snowflake_3 = snowflake.copy().set_color(BLUE).set_stroke(width = 2)
        self.play(star.animate.restore(), 
                  SpreadOut(snowflake_2, rate_func = squish_rate_func(rush_into, 0, 0.9), run_time = 2), 
                  SpreadOut(snowflake_3, rate_func = squish_rate_func(rush_into, 0.05, 0.95), run_time = 2), 
                  SpreadOut(snowflake, rate_func = squish_rate_func(rush_into, 0.1, 1), run_time = 2))
        self.remove(snowflake_2, snowflake_3) 
        self.wait(1+0-2, 24+18) #变成指引前路的火光 （空闲）
        
        self.remove(star, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.wait(1, 28) #我是乐正垂星 我们下期视频再见

        self.wait(3, 9)
        self.fade_out(end = True)
        self.wait(2) #到此共80秒

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]