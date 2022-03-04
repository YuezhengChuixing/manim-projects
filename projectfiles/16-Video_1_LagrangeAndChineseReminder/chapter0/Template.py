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

        notice0 = Notice("沃茨基·硕德", "请勿模仿")

        Lagrange = Tex(r"f(x_i) &= y_i, i = 1,2,\cdots, n\\\\ f(x) &= \sum_{i=1}^ny_ip_i(x), \\p_i(x)&=\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}")
        notice1 = Notice("视频前言", "请听介绍")
        Reminder = Tex(r"x&\equiv a_i \ (\bmod\ m_i), i = 1,2,\cdots, n\\\\ x&\equiv \sum_{i=1}^na_iM_i[M_i]_{m_i}^{-1}\ (\bmod\ M)\\M &= \prod_{i=1}^nm_i,\qquad M_i=\frac{M}{m_i}")

        notice2 = Notice("商业互吹", "请　模仿")

        notice3 = Notice("良性竞争", "完全不卷")

        notice4 = Notice("简单验算", "自证不难")
        Lagrange_base = Tex(r"l_2(x)=\frac{(x-x_1)(x-x_3)}{(x_2-x_1)(x_2-x_3)}")

        notice5 = Notice("梦境占卜", "请勿模仿")

        notice6 = Notice("视频前言", "请听介绍")

        ##  Position
        Lagrange_base.shift(np.array([0,3,0]))

        ##  Showing object
        # """
        ##  Making object
        quote = Text("数学是一门形式学科。\n也就是说，数学研究的是表象，不是本质。\n那些表象之间的联系，才是真正的本质。", font = 'simsun', t2c={"表象": GREEN, "联系": BLUE})
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DOWN + RIGHT), DOWN + LEFT)
        ##  Showing object
        self.play(Write(quote), runtime = 2)
        self.play(Write(author), Write(notice0))
        self.wait(2)
        self.play(FadeOut(quote), FadeOut(author))
        self.wait(1)
        # """
        

        # self.add(notice0)
        #"""
        anim1 = prepare_animation(ReplacementTransform(notice0, notice1))
        anim2 = prepare_animation(Write(Lagrange))
        anim2.update_config(run_time = 3)
        self.play(anim1, anim2)
        self.wait(3.40) #本期视频将会带领大家从零开始 自己一步一步推出拉格朗日插值法
        self.play(ReplacementTransform(Lagrange, Reminder), run_time = 2)
        self.wait(1.34) #作为赠品 大家还能顺便熟练掌握中国剩余定理的使用
        self.play(FadeOut(Reminder))
        self.wait(0.79) #（空闲）
        #"""
        
        #self.add(notice1)
        # """
        ##  Making object
        picture_video = ImageMobject("picture_video.jpg", height = 2)
        picture_screenshot1 = ImageMobject("picture_screenshot1.png")
        picture_screenshot2 = ImageMobject("picture_screenshot2.png")
        picture_screenshot3 = ImageMobject("picture_screenshot3.png")
        picture_screenshot4 = ImageMobject("picture_screenshot4.png")
        picture_screenshot5 = ImageMobject("picture_screenshot5.png")
        ##  Position
        picture_screenshot1.shift(np.array([1.5, 0, 0]))
        picture_screenshot2.shift(np.array([1.5, 0, 0]))
        picture_screenshot3.shift(np.array([1.5, 0, 0]))
        picture_screenshot4.shift(np.array([1.5, 0, 0]))
        picture_screenshot5.shift(np.array([1.5, 0, 0]))
        ##  Showing object
        self.wait(1.75) #可能有观众会问
        self.play(FadeIn(picture_video, shift = UP), ReplacementTransform(notice1, notice2))
        self.wait(1.89+2.22-1) #之前不是已经有up主 做过拉格朗日插值法的视频了吗
        self.wait(0.64)#（空闲）
        self.play(ApplyMethod(picture_video.shift, np.array([-5, 0, 0])))
        self.wait(1.10) #嗯 确实如此
        self.play(FadeIn(picture_screenshot3, shift = UP))
        self.wait(2.53) #这是一部非常好的关于拉格朗日插值法的视频
        self.play(FadeOut(picture_screenshot3, shift = UP), FadeIn(picture_screenshot2, shift = UP))
        self.wait(2.03) #不仅详细介绍了拉格朗日插值法的形式
        self.play(FadeOut(picture_screenshot2, shift = UP), FadeIn(picture_screenshot1, shift = UP))
        self.wait(1.42) #还讲述了很多另外的背景知识
        self.play(FadeOut(picture_screenshot1, shift = UP))
        self.wait(0.38) #推荐大家去看
        self.wait(0.97) #（空闲）
        

        self.play(ReplacementTransform(notice2, notice3), WiggleOutThenIn(picture_video))
        self.wait(1.17) #但是这部视频却始终没有解释
        self.play(FadeIn(picture_screenshot4, shift = UP))
        self.wait(3.27) #插值基函数 或者用视频里的话来说 “开关”
        self.play(FadeOut(picture_screenshot4, shift = UP), FadeIn(picture_screenshot5, shift = UP))
        self.wait(1.21) #是如何构造出来的
        
        self.remove(picture_video, picture_screenshot5)
        # """

        # self.add(notice3)
        # """
        ##  Making object
        Lagrange_base_x1_line0 = Tex(r"l_2(x_1)=")
        Lagrange_base_x1_line1_line = Line(np.array([-2,0,0]), np.array([2,0,0]))
        Lagrange_base_x1_line1_numerator = Tex("(x_1-x_1)","(x_1-x_3)")
        Lagrange_base_x1_line1_numerator_colored = Tex("(x_1-x_1)","(x_1-x_3)")
        Lagrange_base_x1_line1_numerator_colored.set_color_by_tex_to_color_map({"(x_1-x_1)": GREEN})
        Lagrange_base_x1_line1_denominator = Tex("(x_2-x_1)","(x_2-x_3)")
        Lagrange_base_x1_line1 = VGroup(Lagrange_base_x1_line1_line, Lagrange_base_x1_line1_numerator, Lagrange_base_x1_line1_denominator)
        Lagrange_base_x1_line2_eq = Tex("=")
        Lagrange_base_x1_line2_RHS = Tex("0", color = GREEN)
        Lagrange_base_x1_line2 = VGroup(Lagrange_base_x1_line2_eq, Lagrange_base_x1_line2_RHS)
        Lagrange_base_x1 = VGroup(Lagrange_base_x1_line0, Lagrange_base_x1_line1, Lagrange_base_x1_line1_numerator_colored, Lagrange_base_x1_line2)
        
        Lagrange_base_x2_line0 = Tex(r"l_2(x_2)=")
        Lagrange_base_x2_line1_line = Line(np.array([-2,0,0]), np.array([2,0,0]))
        Lagrange_base_x2_line1_numerator = Tex("(x_2-x_1)(x_2-x_3)")
        Lagrange_base_x2_line1_denominator = Tex("(x_2-x_1)(x_2-x_3)")
        Lagrange_base_x2_line1 = VGroup(Lagrange_base_x2_line1_line, Lagrange_base_x2_line1_numerator, Lagrange_base_x2_line1_denominator)
        Lagrange_base_x2_line2_eq = Tex("=")
        Lagrange_base_x2_line2_RHS = Tex("1", color = YELLOW)
        Lagrange_base_x2_line2 = VGroup(Lagrange_base_x2_line2_eq, Lagrange_base_x2_line2_RHS)
        Lagrange_base_x2 = VGroup(Lagrange_base_x2_line0, Lagrange_base_x2_line1, Lagrange_base_x2_line2)
        
        Lagrange_base_x3_line0 = Tex(r"l_2(x_3)=")
        Lagrange_base_x3_line1_line = Line(np.array([-2,0,0]), np.array([2,0,0]))
        Lagrange_base_x3_line1_numerator = Tex("(x_3-x_1)","(x_3-x_3)")
        Lagrange_base_x3_line1_numerator_colored = Tex("(x_3-x_1)","(x_3-x_3)")
        Lagrange_base_x3_line1_numerator_colored.set_color_by_tex_to_color_map({"(x_3-x_3)": GREEN})
        Lagrange_base_x3_line1_denominator = Tex("(x_2-x_1)","(x_2-x_3)")
        Lagrange_base_x3_line1 = VGroup(Lagrange_base_x3_line1_line, Lagrange_base_x3_line1_numerator, Lagrange_base_x3_line1_denominator)
        Lagrange_base_x3_line2_eq = Tex("=")
        Lagrange_base_x3_line2_RHS = Tex("0", color = GREEN)
        Lagrange_base_x3_line2 = VGroup(Lagrange_base_x3_line2_eq, Lagrange_base_x3_line2_RHS)
        Lagrange_base_x3 = VGroup(Lagrange_base_x3_line0, Lagrange_base_x3_line1, Lagrange_base_x3_line1_numerator_colored, Lagrange_base_x3_line2)
        
        ##  Position
        Lagrange_base_x1_line0.next_to(np.array([0,1.5,0]), LEFT)
        Lagrange_base_x1_line1_numerator.next_to(Lagrange_base_x1_line1_line.get_corner(UP), UP)
        Lagrange_base_x1_line1_denominator.next_to(Lagrange_base_x1_line1_line.get_corner(DOWN), DOWN)
        Lagrange_base_x1_line1.next_to(np.array([0,1.5,0]), RIGHT)
        Lagrange_base_x1_line1_numerator_colored.next_to(Lagrange_base_x1_line1_line.get_corner(UP), UP)
        Lagrange_base_x1_line2_eq.next_to(np.array([0,0.3,0]), LEFT)
        Lagrange_base_x1_line2_RHS.next_to(np.array([0,0.3,0]), RIGHT)
        Lagrange_base_x1.shift(np.array([-5.5,0,0]))
        Lagrange_base_x1.scale(0.6)

        Lagrange_base_x2_line0.next_to(np.array([0,1.5,0]), LEFT)
        Lagrange_base_x2_line1_numerator.next_to(Lagrange_base_x2_line1_line.get_corner(UP), UP)
        Lagrange_base_x2_line1_denominator.next_to(Lagrange_base_x2_line1_line.get_corner(DOWN), DOWN)
        Lagrange_base_x2_line1.next_to(np.array([0,1.5,0]), RIGHT)
        Lagrange_base_x2_line2_eq.next_to(np.array([0,0.3,0]), LEFT)
        Lagrange_base_x2_line2_RHS.next_to(np.array([0,0.3,0]), RIGHT)
        Lagrange_base_x2.shift(np.array([-1,0,0]))
        Lagrange_base_x2.scale(0.6)

        Lagrange_base_x3_line0.next_to(np.array([0,1.5,0]), LEFT)
        Lagrange_base_x3_line1_numerator.next_to(Lagrange_base_x3_line1_line.get_corner(UP), UP)
        Lagrange_base_x3_line1_denominator.next_to(Lagrange_base_x3_line1_line.get_corner(DOWN), DOWN)
        Lagrange_base_x3_line1.next_to(np.array([0,1.5,0]), RIGHT)
        Lagrange_base_x3_line1_numerator_colored.next_to(Lagrange_base_x3_line1_line.get_corner(UP), UP)
        Lagrange_base_x3_line2_eq.next_to(np.array([0,0.3,0]), LEFT)
        Lagrange_base_x3_line2_RHS.next_to(np.array([0,0.3,0]), RIGHT)
        Lagrange_base_x3.shift(np.array([3.5,0,0]))
        Lagrange_base_x3.scale(0.6)

        ##  Showing object
        self.play(ReplacementTransform(notice3, notice4), Write(Lagrange_base))
        self.wait(0.5)
        self.play(Write(Lagrange_base_x1_line0), Write(Lagrange_base_x2_line0), Write(Lagrange_base_x3_line0))
        self.play(Write(Lagrange_base_x1_line1), Write(Lagrange_base_x2_line1), Write(Lagrange_base_x3_line1))
        anim1 = Transform(Lagrange_base_x1_line1_numerator, Lagrange_base_x1_line1_numerator_colored)
        anim2 = ApplyMethod(Lagrange_base_x2_line1_numerator.set_color, YELLOW)
        anim3 = ApplyMethod(Lagrange_base_x2_line1_denominator.set_color, YELLOW)
        anim4 = Transform(Lagrange_base_x3_line1_numerator, Lagrange_base_x3_line1_numerator_colored)
        self.play(anim1, anim2, anim3, anim4)
        self.play(Write(Lagrange_base_x1_line2), Write(Lagrange_base_x2_line2), Write(Lagrange_base_x3_line2))
        self.wait(2.99+2.18+2.65-7.5) #当然 在看到插值基函数以后 我们可以很通过很简单的验算 看出它确实符合条件
        self.remove(Lagrange_base_x1, Lagrange_base_x2, Lagrange_base_x3)
        # """
        
        # self.add(notice4)
        # self.add(Lagrange_base)
        # """
        ##  Making object
        picture_Lagrange = ImageMobject("picture_Lagrange.jpg")
        picture_blinder = ImageMobject("picture_blinder.png", height = 0.7)
        bubble_1 = Circle(color = WHITE, radius = 0.3)
        bubble_2 = Circle(color = WHITE, radius = 0.5)
        bubble_3 = Circle(color = WHITE, radius = 3, fill_color = BLACK, fill_opacity = 1)
        bubbles = VGroup(bubble_1, bubble_2, bubble_3)
        Zzz = Text("Zzz......")
        Zzz_wakeup = Text("!")
        
        Ramanujan = Tex(r"\frac{1}{\pi}=\frac{2\sqrt2}{99^2}\sum_{k=0}^\infty\frac{(4k)!(1103+26390k)}{(k!)^4396^{4k}}")
        Kekule_hexagon = RegularPolygon(n = 6)
        Kekule_line1 = Line(np.array([-0.45,0.75,0]), np.array([0.45,0.75,0]))
        Kekule_line2 = Line(np.array([-0.45,0.75,0]), np.array([0.45,0.75,0]))
        Kekule_line3 = Line(np.array([-0.45,0.75,0]), np.array([0.45,0.75,0]))
        Kekule = VGroup(Kekule_hexagon, Kekule_line1, Kekule_line2, Kekule_line3)
        
        Lagrange_formula = Tex(r"f(x) &= \sum_{i=1}^ny_i\left(\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}\right)")
        
        ladder1 = Ladder(np.array([0,8,0]), 12, 14, 3/4, 8)
        ladder2 = Ladder(np.array([0,8,0]), 9, 8, 3/4, 12)
        ladders = VGroup(ladder1, ladder2)

        otherstuffs = VGroup(bubble_1,bubble_2,Zzz,Lagrange_base)

        ##  Position
        picture_Lagrange.shift(np.array([4, -1, 0]))
        picture_blinder.shift(np.array([4, -0.2, 0]))
        bubble_1.shift(np.array([2, -0.2, 0]))
        bubble_2.shift(np.array([0.9, -0.5, 0]))
        bubble_3.shift(np.array([-3, -1, 0]))
        Zzz.shift(np.array([4, 1.5, 0]))
        Zzz_wakeup.shift(np.array([4, 1.5, 0]))
        Ramanujan.scale(0.8)
        Ramanujan.shift(np.array([-3, -1, 0]))
        Kekule_line2.rotate_about_origin(TAU/3)
        Kekule_line3.rotate_about_origin(-TAU/3)
        Kekule.shift(np.array([-3, -1, 0]))
        Lagrange_formula.shift(np.array([-3, -1, 0]))

        ##  Showing object
        self.play(ReplacementTransform(notice4, notice5), WiggleOutThenIn(Lagrange_base), run_time = 1)
        self.wait(0.65) #但这个式子本身
        self.play(FadeIn(picture_Lagrange), FadeIn(picture_blinder))
        self.play(FadeIn(bubbles), ShowIncreasingSubsets(Zzz), lag_ratio = 0.5)
        self.wait(0.84) #就像是拉格朗日某天睡觉的时候

        self.remove(Zzz)
        self.play(FadeIn(Ramanujan), ShowIncreasingSubsets(Zzz))
        self.wait(0.21)
        self.remove(Zzz)
        self.play(FadeOut(Ramanujan), ShowIncreasingSubsets(Zzz))
        self.wait(0.21) #突然梦见自己信仰的女神

        self.remove(Zzz)
        self.play(FadeIn(Kekule), ShowIncreasingSubsets(Zzz))
        self.wait(0.41)
        self.remove(Zzz)
        self.play(FadeOut(Kekule), ShowIncreasingSubsets(Zzz))
        self.wait(0.42) #化形成蛇咬住了自己的尾巴

        self.remove(Zzz)
        self.play(FadeIn(Lagrange_formula), ShowIncreasingSubsets(Zzz))
        anim1 = Transform(Zzz, Zzz_wakeup)
        anim1.update_config(run_time = 0.2)
        anim2 = Rotate(picture_blinder, -TAU/6, about_point = np.array([3.2, -0.2, 0]))
        self.play(anim1, anim2)
        anim1 = FadeOut(picture_blinder, shift = 2*DOWN)
        anim2 = ShowCreationThenDestructionAround(Lagrange_formula)
        anim2.update_config(run_time = 2)
        self.play(anim1, anim2)
        self.wait(0.40) #醒来就发现式子已经摆在自己的桌子上了一样
        self.wait(0.26) #（空闲）
        
        self.bring_to_back(bubble_3)
        anim1 = ApplyMethod(Lagrange_formula.move_to, np.array([0,2.5,0]))
        anim2 = ApplyMethod(bubble_3.scale, 4)
        anim3 = FadeOut(otherstuffs)
        anim4 = FadeOut(picture_Lagrange)
        anim3.update_config(run_time = 0.3)
        anim4.update_config(run_time = 0.3)
        self.play(anim1, anim2, anim3, anim4)
        self.play(Write(ladders))
        self.wait(0.93) #但拉格朗日插值法真的就是一个完全的神来之笔吗
        self.play(FadeOut(bubble_3), FadeOut(ladders), FadeOut(Lagrange_formula))
        self.wait(0.68) #其实不然
        # """
        
        # self.add(notice5)
        # """
        ##  Making object
        division = Tex(r"13\divisionsymbol 5 = 2\cdots\cdots3")
        module = Tex(r"13\equiv 3\ (\bmod\ 5)")
        polydivision = Tex(r"(x^2-3x+5)\divisionsymbol (x-2) = (x-1)\cdots\cdots3")
        polymodule = Tex(r"x^2-3x+5\equiv 3\ (\bmod\ x-2)")
        kernel = Tex(r"f(x)\equiv f(a)\ (\bmod\ x-a)")
        conclusion = Tex(r"\sum_{i=1}^ny_i\left(\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}\right) = \sum_{i=1}^na_iM_i[M_i]_{\bmod m_i}^{-1}")

        ##  Position

        ##  Showing object
        anim1 = ReplacementTransform(notice5, notice6)
        anim2 = FadeIn(division)
        anim2.update_config(run_time = 0.5)
        self.play(anim1, anim2)
        self.wait(0.5)
        self.play(ReplacementTransform(division, module), run_time = 0.5)
        self.wait(1)
        self.play(ReplacementTransform(module, polydivision), run_time = 0.5)
        self.wait(1)
        self.play(ReplacementTransform(polydivision, polymodule), run_time = 0.5)
        self.wait(1)
        self.play(ReplacementTransform(polymodule, kernel), run_time = 0.5)
        self.wait(1)
        self.play(ReplacementTransform(kernel, conclusion), run_time = 0.5)
        self.wait(4.28+3.00+4.00+2.51+2.21+4.16-8) #这期视频 我将带领大家从小学二年级的知识说起 一路推导出拉格朗日插值法 可能不少绝顶聪明的观众已经可以从屏幕上展示的公式 明白究竟是怎么一回事了 但是无论大家的水平如何 我相信 这个视频都会带给你崭新的收获
        self.remove(conclusion)

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
        self.wait(1.66+2.56-1) #长按点赞一键三连 我们开始吧
        self.wait(3.68)
        self.play(FadeOut(notice6), FadeOut(sanlian))
        self.wait(3)
        
        # """
        print(self.get_time())
        


        
        ##  Making object

        ##  Position

        ##  Showing object



        ##  Making object

        ##  Position

        ##  Showing object





