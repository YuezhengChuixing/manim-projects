from __future__ import annotations

from manimlib import *
import numpy as np

def part_rate(func: Callable[[float], float],
    a: float = 0.4,
    b: float = 0.6):
    start = func(a)
    end = func(b)
    return lambda t: inverse_interpolate(start, end, func((b-a)*t + a))

class SharpImage(VGroup):
    CONFIG = {
        "height": 2,
        "draw_stroke_behind_fill": True,
    }

    def __init__(self, filename, **kwargs):

        self.filename = filename
        super().__init__(*self.get_pixels(), **kwargs)
        self.arrange_in_grid(self.size[0], self.size[1], buff = 0, aligned_edge = UP, fill_rows_first = False).set_height(self.height)

    def get_pixels(self):
        image = Image.open(self.filename)
        self.size = image.size
        pixels = []
        for i in range (self.size[0]):
            for j in range (self.size[1]):
                colorij = image.getpixel((i, j))
                opacity = colorij[3]/255 if len(colorij)>3 else 1
                pixelij = Square(stroke_width = 0, fill_opacity = opacity, color = rgb_to_color(np.array([colorij[0], colorij[1], colorij[2]])/255))
                pixels.append(pixelij)
        return pixels
    
class Flip(Animation):
    # unsafe, not guaranteed to work
    def __init__(self, mobject_1: Mobject, mobject_2: Mobject | None = None, **kwargs):
        super().__init__(Group(mobject_1, mobject_2), **kwargs)
        mobject_1.save_state()
        mobject_2.save_state()

    def interpolate_mobject(self, alpha):
        self.mobject[0].restore().scale(np.array([1, max(np.cos(PI*alpha), 0), 1]))
        self.mobject[1].restore().scale(np.array([1, max(-np.cos(PI*alpha), 0), 1]))
        if alpha > 0.5:
            self.mobject[0].set_opacity(0)

    def clean_up_from_scene(self, scene: Scene) -> None:
        self.mobject[0].restore()
        scene.remove(self.mobject).add(self.mobject[1].restore())

class SquareCross(Polygon):
    def __init__(self, side_length: float = 2, **kwargs):
        self.side_length = side_length
        super().__init__(*self.create_points(), **kwargs)
    pass

    def create_points(self) -> None:
        points = np.zeros((12, 3))
        points[0::3] = np.array([DR, UR, UL, DL])*self.side_length/2
        points[1::3] = np.array([DR+2*RIGHT, UR+2*UP, UL+2*LEFT, DL+2*DOWN])*self.side_length/2
        points[2::3] = np.array([UR+2*RIGHT, UL+2*UP, DL+2*LEFT, DR+2*DOWN])*self.side_length/2
        return points

#################################################################### 

class Intro0(FrameScene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("在实数域中，连接两个真理的\n最短的路径是通过复数域。\n但是，伽罗瓦，代价是什么？", font = 'simsun', t2c={"实数域": GREEN, "复数域": BLUE, "伽罗瓦": YELLOW})
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
        #self.camera.anti_alias_width = 0
        self.notices = [Notice("沃茨基·硕德", "请勿模仿"), 
                        Notice("视频前言", "请听介绍"),
                        Notice("农业技术", "请　参考"),
                        Notice("最优方案", "请　参考"),
                        Notice("数学背景", "请　好奇"),
                        Notice("传统艺能", "请　三连")]
        self.notice = self.notices[0]
        
        size_pixel = 1/9
        cane = SharpImage("sugar_cane.png", height = 32*size_pixel)
        canes = [cane[0:64], cane[64:128], cane[128:192], cane[192:256]]
        water = SharpImage("water.png", height = 16*size_pixel)
        self.play(*[FadeIn(canes[i], 0.5*DOWN, rate_func = squish_rate_func(rush_from, 0.1*i, 0.7+0.1*i)) for i in range(4)], self.change_notice())
        self.wait(1, 28) #不知道大家在minecraft里面种过甘蔗吗？
        self.wait(0, 18) #（空闲）
        self.wait(2, 2) #当我们种下甘蔗的时候
        self.bring_to_back(water).play(FadeIn(water.shift(RIGHT), scale = 0.5, shift = RIGHT), cane.animate.scale(0.5).shift(LEFT))
        self.wait(1, 0) #它必须与一格水相邻
        self.wait(0, 16) #（空闲）

        pixels = 6
        size = pixels*size_pixel
        icons = [ImageMobject("cane_left.png", height = size), ImageMobject("water_enlarged.png", height = size), ImageMobject("cane_right.png", height = size)]
        list_old = []
        list_new = []
        rows, cols = 9, 15
        for i in range(rows):
            for j in range(cols):
                offset = size*(i-(rows-1)/2)*DOWN + size*(j-(cols-1)/2)*RIGHT
                list_new.append(icons[j%3].copy().shift(offset))
                range_i = [clip(int((i-rows/2)*pixels) + 8, 0, 16), clip(int((i-rows/2+1)*pixels) + 8, 0, 16)]
                range_j_left = [clip(int((j-cols/2)*pixels) + 17, 0, 16), clip(int((j-cols/2+1)*pixels) + 17, 0, 16)]
                range_j_right = [clip(int((j-cols/2)*pixels) - 1, 0, 16), clip(int((j-cols/2+1)*pixels) - 1, 0, 16)]
                pixels_left = [x+16*y for x in range(*range_i) for y in range(*range_j_left)]
                pixels_right = [x+16*y for x in range(*range_i) for y in range(*range_j_right)]
                list_old.append(Shade(height = size, width = size).shift(offset).add(*[cane[k] for k in pixels_left], *[water[k] for k in pixels_right]))
        
        self.play(LaggedStart(*[Flip(Group(*list_old[cols*i: cols*(i+1)]), Group(*list_new[cols*i: cols*(i+1)])) for i in range(rows)], lag_ratio = 0.2, run_time = 3), self.change_notice())
        self.wait(2+2-3, 7+21) #对于不追求自动化的玩家 这样的种植方案已经足够日常使用
        self.wait(0, 19) #（空闲）

        alpha = ValueTracker(0.0)
        def fade_updater(mob: Mobject):
            value = alpha.get_value()
            mob.restore().scale(1+smooth(value), about_point = ORIGIN).set_opacity(1-rush_from(value))
        list_keep = []
        list_divide = []
        list_kill = []
        for i in range(rows):
            for j in range(cols):
                if i == 4 and j >= 6 and j <= 8:
                    list_keep.append(list_new[i*15+j])
                elif i >= 3 and i <= 5 and j >= 4 and j <= 10:
                    list_divide.append(list_new[i*15+j])
                else:
                    list_kill.append(list_new[i*15+j].save_state().add_updater(fade_updater))
        
        self.play(alpha.animating(rate_func = linear).set_value(1.0), *[mob.animate.fade().scale(2, about_point = ORIGIN) for mob in list_divide], *[mob.animate.scale(2, about_point = ORIGIN) for mob in list_keep]) 
        self.remove(*list_kill).wait(1, 20) #每一行水两旁各种一行甘蔗
        self.wait(2, 20) #种着也方便 收着也省心
        self.wait(0, 15) #（空闲）

        self.play(*[FadeOut(mob) for mob in list_divide])
        self.wait(1, 18) #但其实就土地利用效率而言
        self.add(list_keep[0], list_keep[2]).play(WiggleOutThenIn(list_keep[0], scale_value = 1.2), WiggleOutThenIn(list_keep[2], scale_value = 1.2))
        self.wait(1, 15) #这种方案的每格水旁边只种了两格甘蔗
        self.play(*[FadeOut(mob) for mob in list_keep])
        self.wait(0, 14) #并不是最优情况
        self.wait(0, 21) #（空闲）

        list_icons = []
        list_center = []
        list_others = []
        anims = []
        rows, cols = 9, 9
        for i in range(rows):
            for j in range(cols):
                offset = size*(i-(rows-1)/2)*DOWN + size*(j-(cols-1)/2)*RIGHT
                if (i + j*2) % 5 == 2:
                    mob = icons[1].copy().shift(offset)
                else:
                    mob = icons[0].copy().shift(offset)
                list_icons.append(mob.save_state().scale(np.array([1, 0, 1])))
                k = i+j
                anims.append(mob.animating(run_time = 2, rate_func = squish_rate_func(smooth, k/19, (k+2)/19)).restore())
                if abs(i-4) + abs(j-4) <= 1:
                    list_center.append(mob)
                else:
                    list_others.append(mob)
        self.play(*anims, self.change_notice())
        self.wait(1, 27) #这是土地利用效率最高的甘蔗种植方案
        self.wait(3, 0) #有效种植面积达到了总面积的80%
        self.wait(0, 21) #（空闲）

        shade = VGroup(Shade(width = 6).shift(6.025*LEFT), Shade(width = 6).shift(6.025*RIGHT), Shade(height = 6).shift(6.025*UP), Shade(height = 6).shift(6.025*DOWN))
        list_crosses = []
        vector_1 = size*(2*RIGHT+DOWN)
        vector_2 = size*(2*UP+RIGHT)
        for i in range(-2, 3):
            for j in range(-2, 3):
                offset = i*vector_1 + j*vector_2
                color = GREEN if (i+j)%2 else BLUE
                list_crosses.append(SquareCross(size, stroke_color = ORANGE, fill_color = color).shift(offset))
                    
        self.play(ShowCreation(list_crosses[12]), *[mob.animate.fade() for mob in list_others])
        self.wait(1, 12) #每四格甘蔗共享一格水
        self.wait(2, 4) #形成一个十字形的基本单元
        self.wait(0, 13) #（空闲）

        self.play(TransformFromCopy(list_crosses[12], list_crosses[11]), TransformFromCopy(list_crosses[12], list_crosses[13]))
        self.add(*list_crosses[10:15], shade, self.notice).play(TransformFromCopy(list_crosses[11], list_crosses[10]), TransformFromCopy(list_crosses[13], list_crosses[14]))
        self.wait(0, 4) #朝着两个相互垂直的方向
        self.add(*list_crosses[5:10], *list_crosses[15:20], shade, self.notice
                 ).play(*[TransformFromCopy(list_crosses[10+i], list_crosses[5+i]) for i in range(5)], 
                        *[TransformFromCopy(list_crosses[10+i], list_crosses[15+i]) for i in range(5)])
        self.add(*list_crosses[0:5], *list_crosses[20:25], shade, self.notice
                 ).play(*[TransformFromCopy(list_crosses[5+i], list_crosses[i]) for i in range(5)], 
                        *[TransformFromCopy(list_crosses[15+i], list_crosses[20+i]) for i in range(5)])
        self.wait(0, 4) #不断复制这个基本单元
        self.wait(2, 5) #我们就能完整地得到这个方案
        self.wait(0, 24) #（空闲）

        self.play(*[FadeOut(mob) for mob in list_icons], *[mob.animate.set_fill(opacity = 1) for mob in list_crosses], self.change_notice())
        self.wait(0, 13) #在数学上
        title = Text("周期性密铺", color = YELLOW, font = "simsun").next_to(3.05*UP, UP)
        title_line = Line(3.1*UP+6*LEFT, 3.1*UP+6*RIGHT)
        self.play(Write(title), PullOpen(title_line))
        self.wait(2, 18) #这个方案一般被称为十字形的“周期性密铺”
        self.wait(0, 21) #（空闲）

        point_0 = Dot(color = BLACK)
        label_0 = MTex("0", color = BLACK).scale(0.6).next_to(point_0, buff = 0.1).add(point_0)
        point_1 = Dot(vector_1, color = BLACK)
        label_1 = MTex("2-i", color = BLACK).scale(0.6).next_to(point_1, buff = 0.1).add(point_1)
        point_2 = Dot(vector_2, color = BLACK)
        label_2 = MTex("1+2i", color = BLACK).scale(0.6).next_to(point_2, buff = 0.1).add(point_2)
        self.play(LaggedStart(FadeIn(label_0), FadeIn(label_1), FadeIn(label_2), lag_ratio = 0.5, run_time = 1))
        self.wait(0, 20) #要是顺着数学的路
        self.wait(1, 18) #走得更远一点
        self.wait(2, 16) #这个密铺就会和复数扯上关系
        self.wait(0, 19) #（空闲）

        self.wait(4, 1) #事实上 它可以被解释为一种特殊的复数乘法
        self.wait(0, 19) #（空闲）

        like = Text("", font = 'vanfont').shift(3*LEFT).scale(2)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT).scale(2)
        sanlian = VGroup(like, coin, star)

        self.clear().add(self.notice).play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, ORIGIN), FadeInFromPoint(star, 3*RIGHT), self.change_notice())
        self.play(Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), sanlian.animate.set_color("#00A1D6"))
        self.wait(1, 12) #长按点赞一键三连 我们开始吧
        self.wait(2, 5)
        self.play(FadeOut(self.notice), FadeOut(sanlian))
        self.wait(3, 0) #到此共74秒
    
#################################################################### 

class Chapter1_0(FrameScene):

    def construct(self):

        text1 = Text("第一节 周期性运算", font = 'simsun', t2c={"第一节": YELLOW, "周期性": GREEN, "运算": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(FrameScene):
    def construct(self):
        self.notices = [Notice("小学数学", "请　熟知"), 
                        Notice("小学奥数", "请　熟知")]
        self.notice = self.notices[0]

        indices = VGroup(*[MTex(str(i), color = ratio_color(i/12, BLUE_B, BLUE_D)).shift(2.5*unit(PI/2-i*PI/6)) for i in range(1, 13)]).shift(3*LEFT)
        circle = Arc(radius = 2.8, start_angle = PI/2, angle = -TAU, fill_opacity = 1, fill_color = BACK, n_components = 32).shift(3*LEFT)
        center = Dot().shift(3*LEFT).save_state().scale(0)
        hand_hour = Arrow(ORIGIN, 1.5*LEFT, buff = 0, stroke_width = 8, color = BLUE_D).shift(3*LEFT)
        hand_minute = Arrow(ORIGIN, 2*UP, buff = 0, stroke_width = 8, color = BLUE_B).shift(3*LEFT).save_state()
        self.play(Write(self.notice), ShowCreation(circle, run_time = 2), ShowIncreasingSubsets(indices, run_time = 2), center.animate.restore())
        self.add(hand_hour, hand_minute, center).play(Grow(hand_hour), Grow(hand_minute)) #在我们生活中 和周期有关的事物

        alpha = ValueTracker(0.0)
        def throw_updater(mob: Arrow):
            value = alpha.get_value()
            mob.restore().rotate(-value*PI*2/3).shift(1.5*value*RIGHT + 0.4*value*value*DOWN)
        hand_minute.add_updater(throw_updater)
        self.play(alpha.animate.set_value(10.0), rate_func = smooth_boot(1/6, -1/6), run_time = 2)
        self.remove(hand_minute).wait(0, 6) #最常见的应该就是钟表了
        self.wait(0, 22) #（空闲）

        for _ in range(12):
            self.play(Rotate(hand_hour, -PI/6, about_point = 3*LEFT, run_time = 1/10), frames = 8)
        self.wait(0, 5) #时针每12小时走过一圈 又回到原位
        self.wait(0, 20) #（空闲）

        shadow_0 = hand_hour.copy().set_color(interpolate_color(BLUE_D, BACK, 0.5))
        self.add(shadow_0, hand_hour, center).wait(2, 10) #如果时针现在指向9点
        for _ in range(4):
            self.play(Rotate(hand_hour, -PI/6, about_point = 3*LEFT, run_time = 1/10), frames = 8)
        self.wait(2, 1) #那么在4个小时以后 它将指向1点
        self.wait(0, 22) #（空闲）

        formula_0 = MTex(r"(9+4)\divisionsymbol 12=1{}\cdots\cdots{}1", 
                       tex_to_color_map = {**{str(i): ratio_color(i/12, BLUE_B, BLUE_D) for i in [4, 9]}, r"12": YELLOW, r"1{}": GREY, r"{}1": ratio_color(1/12, BLUE_B, BLUE_D)}).next_to(UP, buff = 1)
        self.play(Write(formula_0, run_time = 1))
        self.wait(1, 17) #9+4除以12余1
        self.wait(2, 1) 
        self.play(FadeOut(shadow_0)) #这在我们小学二年级的时候 就已经会算了
        shadow_1 = hand_hour.copy().set_color(interpolate_color(BLUE_D, BACK, 0.5))
        self.add(shadow_1, hand_hour, center).wait(0, 24) #（空闲）

        formula_1 = MTex(r"(1+5)\divisionsymbol 12=0\cdots\cdots6", 
                       tex_to_color_map = {**{str(i): ratio_color(i/12, BLUE_B, BLUE_D) for i in [1, 5, 6]}, r"12": YELLOW, r"0": GREY}).next_to(ORIGIN, buff = 1)
        formula_2 = MTex(r"(6+9)\divisionsymbol 12=1{}\cdots\cdots3", 
                       tex_to_color_map = {**{str(i): ratio_color(i/12, BLUE_B, BLUE_D) for i in [6, 9, 3]}, r"12": YELLOW, r"1{}": GREY}).next_to(DOWN, buff = 1)
        for _ in range(5):
            self.play(Rotate(hand_hour, -PI/6, about_point = 3*LEFT, run_time = 1/10), frames = 8)
        self.play(Write(formula_1, run_time = 1), FadeOut(shadow_1))
        shadow_2 = hand_hour.copy().set_color(interpolate_color(BLUE_D, BACK, 0.5))
        self.add(shadow_2, hand_hour, center)
        for _ in range(9):
            self.play(Rotate(hand_hour, -PI/6, about_point = 3*LEFT, run_time = 1/10), frames = 8)
        self.play(Write(formula_2, run_time = 1), FadeOut(shadow_2))
        self.wait(2+3-2, 8+18-112) #所有在钟表盘上的加减法 都可以用先除以12再取余数的方法来计算
        self.wait(0, 17) #（空闲）

        quotient = [formula_0.get_part_by_tex(r"1{}"), formula_1.get_part_by_tex(r"0"), formula_2.get_part_by_tex(r"1{}")]
        deletes = VGroup(*[Line(mob.get_corner(UL), mob.get_corner(DR), color = RED) for mob in quotient])
        title = Text(r"同余运算", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        shade = Shade().next_to(0.5*UP, DR, buff = 0)
        self.play(ShowCreation(deletes), self.change_notice())
        self.wait(2, 8) #这种忽略掉商 只取余数的计算
        self.play(Write(title), PullOpen(title_line), FadeIn(shade), FadeOut(hand_hour))
        self.remove(shade, formula_1, formula_2, *deletes[1:]).add(shadow_0, hand_hour, center).play(FadeIn(hand_hour.rotate(PI/3, about_point = 3*LEFT)), FadeIn(shadow_0))
        self.wait(1+0-2, 15+17) #一般被叫做同余（空闲）

        formula_m = MTex(r"9+4\equiv {}1\ (\bmod\ 12\,)", tex_to_color_map = {**{str(i): ratio_color(i/12, BLUE_B, BLUE_D) for i in [4, 9]}, r"12": YELLOW, r"{}1": ratio_color(1/12, BLUE_B, BLUE_D)}).set_x(formula_0.get_x())
        self.play(Write(formula_m))
        self.wait(0, 18) #钟表上的加减法......
        self.play(ShowPassingFlashAround(formula_m.get_part_by_tex(r"12")))
        self.wait(0, 26) #......就是模12的同余运算
        self.wait(0, 19) #（空闲）

        self.wait(3, 6) #每一个正整数都有它自己的同余运算
        self.wait(1, 25) #我们可以仿照钟表
        
        circle.add(indices, hand_hour)
        tables = []
        for i in range(3, 12):
            indices_i = VGroup(*[MTex(str(j), color = ratio_color(j/i, BLUE_B, BLUE_D)).shift(2.5*unit(PI/2-j*TAU/i)) for j in range(0, i)])
            table = Circle(radius = 2.8, stroke_color = WHITE, fill_opacity = 1, fill_color = BACK).add(*indices_i).shift(3*LEFT + 0.4*(i-5)*RIGHT)
            tables.append(table)
        self.add(*tables, circle, shadow_0, center).play(*[FadeOut(mob, 3*RIGHT)for mob in [formula_0, formula_m, deletes[0]]],
                  LaggedStart(AnimationGroup(ApplyMethod(circle.shift, 2.8*RIGHT), ApplyMethod(center.shift, 2.8*RIGHT), FadeOut(shadow_0, 2.8*RIGHT), group = VGroup()), 
                              *[FadeIn(mob, 2.8*RIGHT) for mob in tables[::-1]], group = VGroup(), run_time = 2))
        self.wait(0, 17) #为每一个同余运算设计一个表盘
        self.wait(1) #到此共47秒

        self.add(Arrow(ORIGIN, 1.8*UP, buff = 0, stroke_width = 8, color = BLUE_D).shift(3*LEFT), Dot().shift(3*LEFT),
                 *tables[3:], circle, center)
        self.play(LaggedStart(*[FadeOut(mob, 2*DOWN) for mob in tables[0:2]], Animation(VMobject()), 
                              *[FadeOut(mob, 2*DOWN) for mob in tables[3:]],
                                AnimationGroup(FadeOut(circle, 2*DOWN), FadeOut(center, 2*DOWN), group = VGroup()), group = VGroup(), run_time = 2))

class Chapter1_2(FrameScene):
    def construct(self):
        self.notices = [Notice("小学奥数", "请　熟知")]
        self.notice = self.notices[0]

        title = Text(r"同余运算", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)

        indices = [MTex(str(i), color = ratio_color(i/5, BLUE_B, BLUE_D)).shift(2.5*unit(PI/2-i*TAU/5) + 3*LEFT) for i in range(0, 5)]
        circle = Arc(radius = 2.8, start_angle = PI/2, angle = TAU).shift(3*LEFT)
        center = Dot().shift(3*LEFT).save_state()
        hand_hour = Arrow(ORIGIN, 1.8*UP, buff = 0, stroke_width = 8, color = BLUE_D).shift(3*LEFT).save_state()

        self.add(*indices, circle, hand_hour, center, title, title_line, self.notice)
        self.frames = 60
        self.wait(0, 19) #这是模5的同余运算的表盘
        self.wait(1, 27) #它上面有5个自然数
        self.wait(0, 14) #（空闲）

        self.wait(1, 21) #其实严格来说
        buff = 0.8
        class_0 = MTex(r"\bar{0}=\{\cdots, -5, 0, 5, 10, 15, \cdots\}", color = ratio_color(0, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.9).next_to(2*buff*UP)
        class_1 = MTex(r"\bar{1}=\{\cdots, -4, 1, 6, 11, 16, \cdots\}", color = ratio_color(0.1, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.9).next_to(buff*UP)
        class_2 = MTex(r"\bar{2}=\{\cdots, -3, 2, 7, 12, 17, \cdots\}", color = ratio_color(0.2, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.9).next_to(ORIGIN)
        class_3 = MTex(r"\bar{3}=\{\cdots, -2, 3, 8, 13, 18, \cdots\}", color = ratio_color(0.3, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.9).next_to(buff*DOWN)
        class_4 = MTex(r"\bar{4}=\{\cdots, -1, 4, 9, 14, 19, \cdots\}", color = ratio_color(0.4, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.9).next_to(2*buff*DOWN)
        classes = [class_0, class_1, class_2, class_3, class_4]
        self.play(Uncreate(circle), *[mob.animate.scale(0, about_point = 3*LEFT) for mob in [hand_hour, center]], LaggedStart(*[ReplacementTransform(indices[i], VGroup(classes[i][1])) for i in range(5)], run_time = 1))
        self.remove(center, hand_hour).wait(1, 3) #它们已经不是自然数了
        self.play(ShowCreation(VGroup(*[classes[i][0] for i in range(5)])), LaggedStart(*[Write(classes[i][2:]) for i in range(5)], run_time = 2))
        self.wait(0, 3) #而是一种名叫“同余类”的概念
        self.wait(0, 18) #（空闲）

        self.wait(2, 17) #但把它们当成自然数来计算
        inside_indices = [MTex(r"\bar" + str(i), color = ratio_color(i/5, BLUE_B, BLUE_D)).scale(0.9).shift(2.1*unit(PI/2-i*TAU/5) + 3*LEFT) for i in range(0, 5)]
        midium_circle = Arc(radius = 2.4, start_angle = PI/2, angle = TAU).shift(3*LEFT)
        outside_indices = [MTex(r"\bar" + str(i), color = ratio_color(i/5, BLUE_B, BLUE_D)).scale(0.9).shift(2.7*unit(PI/2-i*TAU/5) + 3*LEFT) for i in range(0, 5)]
        short_hand = Arrow(ORIGIN, 1.5*UP, buff = 0, stroke_width = 8, color = BLUE_D).shift(3*LEFT)
        self.add(hand_hour, center).play(ShowCreation(midium_circle), center.animate.restore(), ReplacementTransform(hand_hour, short_hand), LaggedStart(*[ReplacementTransform(classes[i][0:2], inside_indices[i]) for i in range(4, -1, -1)]), LaggedStart(*[FadeOut(mob[2:], RIGHT) for mob in classes]), run_time = 1)
        self.add(short_hand, center).wait(1, 0) #其实不会造成什么大的影响
        self.wait(0, 22) #（空闲）

        equation_1 = MTex(r"4+2\equiv 1\ (\bmod\ 5\,)", tex_to_color_map = {**{str(i): ratio_color(i/5, BLUE_B, BLUE_D) for i in [1, 2, 4]}, r"5": YELLOW}).scale(0.8)
        equation_1.shift(UP+4*RIGHT - equation_1[3].get_center())
        equation_2 = MTex(r"4\bmod5+2\bmod5= 1\bmod5", tex_to_color_map = {**{str(i): ratio_color(i/5, BLUE_B, BLUE_D) for i in [1, 2, 4]}, r"5": YELLOW}).scale(0.8)
        equation_2.shift(4*RIGHT - equation_2[11].get_center())
        equation_3 = MTex(r"\bar4+\bar2= \bar1", tex_to_color_map = {r"\bar"+str(i): ratio_color(i/5, BLUE_B, BLUE_D) for i in [1, 2, 4]}).scale(0.8)
        equation_3.shift(DOWN+4*RIGHT - equation_3[5].get_center())
        arrow = Arrow(1.7*DOWN+4*RIGHT, 1.3*DOWN+4*RIGHT, buff = 0, color = YELLOW)
        notice = Text("这三种写法是一个意思", font = "simsun", color = YELLOW).scale(0.4).next_to(1.7*DOWN+4*RIGHT, DOWN, buff = 0.15).add(arrow)
        self.play(LaggedStart(*[FadeIn(mob, 0.5*LEFT) for mob in [equation_1, equation_2, equation_3]], FadeIn(notice, 0.5*UP), run_time = 1.5, lag_ratio = 0.5), Rotate(short_hand, TAU/5, about_point = 3*LEFT, run_time = 1/6))
        self.wait(2, 3) #比如 我们要是想计算4+2

        shadow = short_hand.copy().set_opacity(0.5)
        self.add(shadow, short_hand, center).play(Rotate(short_hand, -TAU/5, about_point = 3*LEFT, run_time = 1/6), frames = 15)
        self.play(Rotate(short_hand, -TAU/5, about_point = 3*LEFT, run_time = 1/6), frames = 15)
        self.wait(2, 2) #就可以将指向4的指针转动两格
        self.wait(1, 10) #让它指向1
        self.wait(0, 20) #（空闲）
        
        self.play(*[mob.animate.scale(0, about_point = 3*LEFT) for mob in [shadow, short_hand, center]], LaggedStart(*[TransformFromCopy(inside_indices[i], outside_indices[i]) for i in range(5)], run_time = 1.5, lag_ratio = 0.5))
        self.wait(0, 24) #但还有另一种计算方法
        alpha = ValueTracker(0.0)
        def revolution_updater(index: int):
            def util(mob: VMobject):
                angle = alpha.get_value()
                mob.move_to(2.1*unit(PI/2  - index*TAU/5 - angle) + 3*LEFT)
            return util
        for i in range(5):
            inside_indices[i].add_updater(revolution_updater(i))
        self.play(alpha.animate.set_value(TAU/5), run_time = 1/6, frames = 15)
        self.play(alpha.animate.set_value(2*TAU/5), run_time = 1/6, frames = 15)
        self.wait(0, 27) #那就是转动整个表盘
        self.wait(0, 16) #（空闲）

        indicate_rectangle = Rectangle(height = 1.2, width = 0.8, color = YELLOW).insert_n_curves(16).shift(2.4*UP + 3*LEFT).rotate(-TAU/5, about_point = 3*LEFT)
        self.play(*[FadeOut(mob) for mob in [equation_1, equation_2, equation_3, notice]])
        self.wait(1, 25) #这样一来 在模5运算中
        self.play(VShowPassingFlash(indicate_rectangle, time_width = 0.5, run_time = 2))
        self.wait(0, 17) #我们不但能得到4+2的结果

        rows = [[MTex(r"+")] + [MTex(r"\bar"+str(i), color = ratio_color(i/8, BLUE_B, BLUE_D)).scale(0.8) for i in range(5)]] + [
            [MTex(r"\bar"+str(i), color = ratio_color(i/8, BLUE_B, BLUE_D)).scale(0.8)] + [MTex(r"\bar"+str((i+j)%5), color = ratio_color((i+j)%5/8, BLUE_B, BLUE_D)).scale(0.8) for j in range(5)] for i in range(5)]
        for i in range(6):
            rows[0][i].shift(UP + RIGHT + 0.8*i*RIGHT)
            rows[1][i].shift(0.8*UP + RIGHT + 0.8*i*RIGHT)
            rows[2][i].shift(0.2*UP + RIGHT + 0.8*i*RIGHT)
            rows[3][i].shift(0.2*DOWN + RIGHT + 0.8*i*RIGHT)
            rows[4][i].shift(DOWN + RIGHT + 0.8*i*RIGHT)
            rows[5][i].shift(1.8*DOWN + RIGHT + 0.8*i*RIGHT)
        row_0 = VGroup(*rows[0])
        row_1 = VGroup(*rows[1])
        row_2 = VGroup(*rows[2])
        row_3 = VGroup(*rows[3])
        row_4 = VGroup(*rows[4])
        row_5 = VGroup(*rows[5])
        line_h = Line(0.6*UP + 0.6*RIGHT, 0.6*UP + 5.4*RIGHT)
        line_v = Line(0.6*UP + 1.4*RIGHT, 0.6*UP + 1.4*RIGHT)
        self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in rows[0]], lag_ratio = 0.5, run_time = 1), LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in rows[3]], lag_ratio = 0.5, run_time = 1), 
                  ShowCreation(line_h), line_v.animating(run_time = 0.5).put_start_and_end_on(1.4*UP + 1.4*RIGHT, 0.6*DOWN + 1.4*RIGHT))
        self.wait(1, 20) #还能知道每个数+2分别是多少
        self.wait(0, 21) #（空闲）

        self.play(alpha.animate.set_value(3*TAU/5), run_time = 1/6, frames = 15)
        self.play(line_v.animate.put_start_and_end_on(1.6*UP + 1.4*RIGHT, 1.4*DOWN + 1.4*RIGHT), *[mob.animate.shift(0.2*UP) for mob in [row_0, line_h]], 
                  Write(rows[4][0]), LaggedStart(*[TransformFromCopy(inside_indices[(i+3)%5], rows[4][i+1]) for i in range(5)], run_time = 1.5, lag_ratio = 0.3))
        self.play(alpha.animate.set_value(4*TAU/5), run_time = 1/6, frames = 15)
        self.play(line_v.animate.put_start_and_end_on(1.8*UP + 1.4*RIGHT, 2.2*DOWN + 1.4*RIGHT), *[mob.animate.shift(0.2*UP) for mob in [row_0, line_h]], 
                  Write(rows[5][0]), LaggedStart(*[TransformFromCopy(inside_indices[(i+4)%5], rows[5][i+1]) for i in range(5)], run_time = 1.5, lag_ratio = 0.3))
        self.play(alpha.animate.set_value(5*TAU/5), run_time = 1/6, frames = 15)
        self.play(line_v.animate.put_start_and_end_on(2*UP + 1.4*RIGHT, 2.4*DOWN + 1.4*RIGHT), *[mob.animate.shift(0.2*UP) for mob in [row_0, line_h]], *[mob.animate.shift(0.2*DOWN) for mob in [row_3, row_4, row_5]], 
                  Write(rows[1][0]), LaggedStart(*[TransformFromCopy(inside_indices[i], rows[1][i+1]) for i in range(5)], run_time = 1.5, lag_ratio = 0.3))
        self.play(alpha.animate.set_value(6*TAU/5), run_time = 1/6, frames = 15)
        self.play(line_v.animate.put_start_and_end_on(2.2*UP + 1.4*RIGHT, 2.6*DOWN + 1.4*RIGHT), *[mob.animate.shift(0.2*UP) for mob in [row_0, row_1, line_h]], *[mob.animate.shift(0.2*DOWN) for mob in [row_3, row_4, row_5]], 
                  Write(rows[2][0]), LaggedStart(*[TransformFromCopy(inside_indices[(i+1)%5], rows[2][i+1]) for i in range(5)], run_time = 1.5, lag_ratio = 0.3))
        self.wait(3+0+2+2-8, 11+20+27+6) #不只是+2 所有加法都可以这么计算 （空闲） 我们还可以写出模5运算的加法表 用来记录每一个加法的结果
        self.wait(0, 21) #（空闲）

        self.play(alpha.animate.set_value(7*TAU/5), run_time = 1/6, frames = 90)
        self.play(alpha.animate.set_value(8*TAU/5), run_time = 1/6, frames = 90)
        self.play(alpha.animate.set_value(9*TAU/5), run_time = 1/6, frames = 90)
        self.play(alpha.animate.set_value(10*TAU/5), run_time = 1/6, frames = 90)
        for mob in inside_indices:
            mob.clear_updaters()
        self.wait(4+0+3+1+1-12, 8+20+22+27+25) #我一直觉得 这种表盘是上手模运算最合适的工具 （空闲） 模运算和常规运算最大的不同点就在于同余 有这样一个表盘在 同余就显得十分自然了
        self.wait(0, 21) #（空闲）

        self.wait(3, 18) #但另一方面 这个表盘只能演示加法运算
        self.wait(0, 15) #（空闲）
        self.play(*[FadeOut(mob, 3*LEFT, rate_func = rush_into) for mob in [*inside_indices, midium_circle, *outside_indices]],
                  *[mob.animating(run_time = 2).shift(6*LEFT) for mob in [row_0, row_1, row_2, row_3, row_4, row_5, line_h, line_v]])
        self.wait(0, 9) #而模运算中除了加法
        self.wait(1, 9) #也是有乘法的
        self.wait(0, 12) #到此共70秒

class Chapter1_3(FrameScene):
    def construct(self):
        self.notices = [Notice("小学奥数", "请　熟知"),
                        Notice("鲁莽操作", "请勿模仿")]
        self.notice = self.notices[0]

        title = Text(r"同余运算", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        
        colors = [interpolate_color(BLUE_B, BLUE_D, i/4) for i in range(5)]
        rows_add = VGroup(VGroup(MTex(r"+").shift(1.8*UP + 5*LEFT), *[MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(1.8*UP + 4.2*LEFT + 0.8*i*RIGHT) for i in range(5)]), *[
            VGroup(MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(UP + 5*LEFT + 0.8*i*DOWN), *[MTex(r"\bar"+str((i+j)%5), color = colors[(i+j)%5]).scale(0.8).shift(UP + 4.2*LEFT + 0.8*i*DOWN + 0.8*j*RIGHT) for j in range(5)]) for i in range(5)])
        line_h_add = Line(1.4*UP + 5.4*LEFT, 1.4*UP + 0.6*LEFT)
        line_v_add = Line(2.2*UP + 4.6*LEFT, 2.6*DOWN + 4.6*LEFT)

        self.add(self.notice, title, title_line, rows_add, line_h_add, line_v_add)
        self.wait(3, 2) #模运算中的乘法 和加法一样
        self.wait(2, 5) #也是先计算 再取余数
        self.wait(0, 17) #（空闲）

        formula_1_0 = MTex(r"(1\times 1)\divisionsymbol5=0\cdots\cdots1", tex_to_color_map = {r"1": colors[0], r"0": GREY, r"5": YELLOW}).scale(0.8)
        formula_1_0.shift(1.4*UP+3*RIGHT-formula_1_0[7].get_center())
        formula_1_1 = MTex(r"1\times 1\equiv 1(\bmod\ 5\,)", tex_to_color_map = {r"1": colors[0], r"5": YELLOW}).scale(0.8)
        formula_1_1.shift(0.6*UP+3*RIGHT-formula_1_1[3].get_center())
        formula_2_0 = MTex(r"(2\times 4)\divisionsymbol5=1\cdots\cdots3", tex_to_color_map = {r"1": GREY, r"2": colors[1], r"3": colors[2], r"4": colors[3], r"5": YELLOW}).scale(0.8)
        formula_2_0.shift(0.6*DOWN+3*RIGHT-formula_2_0[7].get_center())
        formula_2_1 = MTex(r"2\times 4\equiv 3(\bmod\ 5\,)", tex_to_color_map = {r"2": colors[1], r"3": colors[2], r"4": colors[3], r"5": YELLOW}).scale(0.8)
        formula_2_1.shift(1.4*DOWN+3*RIGHT-formula_2_1[3].get_center())
        self.play(FadeIn(formula_1_0, 0.3*RIGHT), FadeIn(formula_1_1, 0.3*RIGHT), run_time = 0.5)
        self.wait(1, 10) #计算1×1的结果
        self.wait(2, 20) #和在自然数中的结果一样 也是1
        self.wait(0, 17) #（空闲）
        self.play(FadeIn(formula_2_0, 0.3*RIGHT), FadeIn(formula_2_1, 0.3*RIGHT), run_time = 0.5)
        self.wait(2, 17) #而计算2×4 结果就不是8了
        self.wait(1, 28) #而是取完余数以后的3
        self.wait(0, 17) #（空闲）

        rows_mul = VGroup(VGroup(MTex(r"\times").shift(1.8*UP + RIGHT), *[MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(1.8*UP + 1.8*RIGHT + 0.8*i*RIGHT) for i in range(5)]), *[
            VGroup(MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(UP + RIGHT + 0.8*i*DOWN), *[MTex(r"\bar"+str((i*j)%5), color = colors[(i*j)%5]).scale(0.8).shift(UP + 1.8*RIGHT + 0.8*i*DOWN + 0.8*j*RIGHT) for j in range(5)]) for i in range(5)])
        line_h_mul = Line(1.4*UP + 1.4*RIGHT, 1.4*UP + 1.4*RIGHT)
        line_v_mul = Line(1.4*UP + 1.4*RIGHT, 1.4*UP + 1.4*RIGHT)
        self.play(*[FadeOut(mob) for mob in [formula_1_0, formula_1_1, formula_2_0, formula_2_1]])
        self.play(line_h_mul.animate.put_start_and_end_on(1.4*UP + 0.6*RIGHT, 1.4*UP + 5.4*RIGHT), line_v_mul.animate.put_start_and_end_on(2.2*UP + 1.4*RIGHT, 2.6*DOWN + 1.4*RIGHT))
        anims = [[] for _ in range(11)]
        for i in range(6):
            for j in range(6):
                anims[i+j].append(ShowCreation(rows_mul[i][j]))
        self.play(LaggedStart(*[AnimationGroup(*anims[k]) for k in range(11)], lag_ratio = 0.5, run_time = 3))
        self.wait(3+2-5, 1+8) #如果把每种可能的乘法都算一遍 我们就也能像加法表那样
        self.wait(1, 7) #列出乘法表来
        self.wait(0, 17) #（空闲）

        inside_indices = [MTex(r"\bar" + str(i), color = ratio_color(i/5, BLUE_B, BLUE_D)).scale(0.9).shift(2.1*unit(PI/2-i*TAU/5) + 3*LEFT) for i in range(0, 5)]
        midium_circle = Arc(radius = 2.4, start_angle = PI/2, angle = TAU).shift(3*LEFT)
        outside_indices = [MTex(r"\bar" + str(i), color = ratio_color(i/5, BLUE_B, BLUE_D)).scale(0.9).shift(2.7*unit(PI/2-i*TAU/5) + 3*LEFT) for i in range(0, 5)]
        self.play(*[FadeOut(mob) for mob in [rows_add, line_h_add, line_v_add]])
        self.play(*[FadeIn(mob) for mob in [*inside_indices, midium_circle, *outside_indices]])
        self.wait(0, 21) #但这个时候要是再看一眼圆盘
        self.wait(1, 9) #那就完全乱套了
        self.wait(0, 23) #（空闲）

        indicate = Rectangle(height = 0.6, width = 4.6, color = YELLOW).shift(3*RIGHT + UP)
        self.play(ShowCreation(indicate))
        self.wait(0, 19) #当我们乘0的时候
        self.play(LaggedStart(*[ApplyMethod(mob.shift, 0.8*(2.1*UP + 3*LEFT - mob.get_center())) for mob in inside_indices], run_time = 1.5, lag_ratio = 0.3), frames = 60) #每个数都会跑到0的位置
        self.wait(0, 16) #（空闲）
        self.play(indicate.animate.shift(0.8*DOWN), LaggedStart(*[ApplyMethod(mob.shift, 4*(mob.get_center() - 2.1*UP - 3*LEFT)) for mob in inside_indices[::-1]], run_time = 1.5, lag_ratio = 0.3), frames = 60)
        self.wait(1+1-2, 22+11) #当我们乘1的时候 每个数都不动
        self.wait(0, 18) #（空闲）
        self.wait(2, 2) #但也就只有这两个数看着还行了
        self.wait(0, 14) #（空闲）

        for i in range(5):
            inside_indices[i].generate_target().move_to(2.1*unit(PI/2-2*i*TAU/5) + 3*LEFT)
        self.play(indicate.animate.shift(0.8*DOWN), LaggedStart(*[MoveToTarget(mob, path_arc = PI/6) for mob in inside_indices], run_time = 1.5, lag_ratio = 0.3))
        self.wait(1, 15) #给圆盘乘2 上面的数就会乱跑
        self.wait(0, 18) #（空闲）
        for i in range(5):
            inside_indices[i].generate_target().move_to(2.1*unit(PI/2-3*i*TAU/5) + 3*LEFT)
        self.play(indicate.animate.shift(0.8*DOWN), LaggedStart(*[MoveToTarget(mob, path_arc = PI/6) for mob in inside_indices], run_time = 1.5, lag_ratio = 0.3))
        self.wait(1, 15) #乘3 也会乱跑
        self.frames -= 30
        self.wait(0, 15) #（空闲）
        for i in range(5):
            inside_indices[i].generate_target().move_to(2.1*unit(PI/2-4*i*TAU/5) + 3*LEFT)
        self.play(indicate.animate.shift(0.8*DOWN), LaggedStart(*[MoveToTarget(mob, path_arc = PI/6) for mob in inside_indices], run_time = 1.5, lag_ratio = 0.3))
        self.wait(1, 19) #乘4 每一对和为5的数会互换
        self.wait(0, 25) #（空闲）

        self.play(*[FadeOut(mob, DOWN) for mob in [*inside_indices, midium_circle, *outside_indices]], Uncreate(indicate))
        self.wait(2, 17) #演示加法的圆盘看起来没法用来演示乘法
        self.wait(2, 0) #那用什么才能演示乘法呢
        self.wait(0, 20) #（空闲）
        self.wait(2, 14) #这个问题一度困扰了我很长时间
        self.wait(0, 16) #（空闲）

        axis = Line(6*LEFT, ORIGIN)
        marks = VGroup(*[Line(0.1*UP, 0.1*DOWN).shift((5.5-i)*LEFT) for i in range(6)])
        numbers = VGroup(*[MTex(str(i-1), color = colors[(i-1)%5]).scale(0.8).shift((5.5-i)*LEFT + 0.4*DOWN) for i in range(6)])
        self.play(ShowCreation(axis), ShowCreation(marks), ShowCreation(numbers), self.change_notice())
        self.wait(0, 28) #直到有一天我想到
        point_1 = Dot(5.5*LEFT, color = BLUE)
        point_4 = Dot(0.5*LEFT, color = BLUE)
        module_1 = MTex(r"-\bar1=\bar4", color = BLUE_D, tex_to_color_map = {r"=": WHITE})
        module_1.shift(0.5*UP+2*RIGHT - module_1[3].get_center())
        module_2 = MTex(r"\bar i=\bar2", color = TEAL, tex_to_color_map = {r"=": WHITE}).next_to(0.5*UP)
        module_2.shift(0.5*DOWN+2*RIGHT - module_2[2].get_center())
        self.play(ShowCreation(point_1), ShowCreation(point_4), *[FadeOut(mob) for mob in [rows_mul, line_h_mul, line_v_mul]])
        self.play(FadeIn(module_1))
        self.wait(0, 13) #既然-1和4是同余的

        point_i = Dot(4.5*LEFT + UP, color = TEAL)
        number_i = MTex(r"i", color = TEAL).scale(0.8).shift(4.5*LEFT + 0.6*UP)
        point_2 = Dot(2.5*LEFT, color = TEAL)
        self.play(TransformFromCopy(point_1, point_i, path_arc = PI/2), TransformFromCopy(numbers[0], number_i, path_arc = PI/2), TransformFromCopy(point_4, point_2))
        self.play(Write(module_2))
        self.wait(1, 28) #那给两边同时开个根号 不就变成了......
        self.wait(0, 21) #到此共67+1秒
        
class Chapter1_4(FrameScene):
    def construct(self):
        camera = self.camera.frame
        self.notices = [Notice("鲁莽操作", "请勿模仿"),
                        Notice("前后呼应", "请　模仿").shift(0.5*DOWN),
                        Notice("下节预告", "请　期待")]
        self.notice = self.notices[0]

        title = Text(r"同余运算", font = "simsun", color = YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        
        colors = [interpolate_color(BLUE_B, BLUE_D, i/4) for i in range(5)]
        axis = Line(6*LEFT, ORIGIN)
        marks = VGroup(*[Line(0.1*UP, 0.1*DOWN).shift((5.5-i)*LEFT) for i in range(6)])
        numbers = VGroup(*[MTex(str(i-1), color = colors[(i-1)%5]).scale(0.8).shift((5.5-i)*LEFT + 0.4*DOWN) for i in range(6)])
        number_i = MTex(r"i", color = TEAL).scale(0.8).shift(4.5*LEFT + 0.6*UP)
        point_1 = Dot(5.5*LEFT, color = BLUE)
        point_4 = Dot(0.5*LEFT, color = BLUE)
        point_i = Dot(4.5*LEFT + UP, color = TEAL)
        point_2 = Dot(2.5*LEFT, color = TEAL)
        module_1 = MTex(r"-\bar1=\bar4", color = BLUE_D, tex_to_color_map = {r"=": WHITE})
        module_1.shift(0.5*UP+2*RIGHT - module_1[3].get_center())
        module_2 = MTex(r"\bar i=\bar2", color = TEAL, tex_to_color_map = {r"=": WHITE}).next_to(0.5*UP)
        module_2.shift(0.5*DOWN+2*RIGHT - module_2[2].get_center())
        self.add(self.notice, title, title_line, axis, marks, numbers, number_i, point_1, point_4, point_i, point_2, module_1, module_2)

        new_marks = VGroup(*[Line(0.1*UP, 0.1*DOWN).shift((6.5+i)*LEFT) for i in range(3)])
        self.play(*[mob.animating(run_time = 2).shift(4.5*LEFT) for mob in [camera, self.notice]], *[FadeOut(mob, 2.25*LEFT, rate_func = rush_into) for mob in [title, title_line]],
                  FadeOut(VGroup(module_1, module_2, *numbers, number_i)), axis.animating(run_time = 2).put_start_and_end_on(9*LEFT, ORIGIN), 
                  ShowCreation(new_marks, run_time = 2))
        for mob in [camera, self.notice, marks, new_marks, axis, point_1, point_4, point_i, point_2]:
            mob.shift(4.5*RIGHT)
        self.wait(1, 9) #既然都能把2和i放进同一个剩余类
        v_lines = VGroup(new_marks[1], new_marks[0], *marks[0:5])
        for i in range(7):
            v_lines[i].generate_target().put_start_and_end_on((i-3)*RIGHT + 3.3*UP, (i-3)*RIGHT + 3.3*DOWN)
            if i != 3:
                v_lines[i].target.set_stroke(width = 1)
        h_lines = [Line((i-3)*DOWN + 3.3*LEFT, (i-3)*DOWN + 3.3*RIGHT, stroke_width = 1) for i in [0, 1, 2, 4, 5, 6]]
        self.add(*v_lines, *h_lines, point_1, point_i, point_2, point_4).play(axis.animate.put_start_and_end_on(3.3*LEFT, 3.3*RIGHT), Uncreate(marks[5]), Uncreate(new_marks[2]), FadeOut(point_4), *[mob.animate.shift(0.5*DOWN) for mob in [camera, self.notice]],
                  LaggedStart(*[MoveToTarget(v_line) for v_line in v_lines], *[PullOpen(h_line) for h_line in h_lines], group = VGroup(), run_time = 2))
        self.wait(1+0-2, 26+22) #我们就不妨再大胆一点 （空闲）
        
        dots = []
        anims = []
        classes = [VGroup() for _ in range(13)]
        for i in range(-3, 4):
            for j in range(-3, 4):
                position = i*RIGHT + j*UP
                if (i, j) == (-1, 0):
                    dots.append(point_1)
                    anims.append(point_1.animate.set_color(colors[4]).scale(2.5))
                elif (i, j) == (2, 0):
                    dots.append(point_2)
                    anims.append(point_2.animate.set_color(colors[2]).scale(2.5))
                elif (i, j) == (0, 1):
                    dots.append(point_i)
                    anims.append(point_i.animate.set_color(colors[2]).scale(2.5))
                else:
                    dot = Dot(position, radius = 0.2).set_color(colors[(i+2*j)%5])
                    dots.append(dot)
                    anims.append(FadeIn(dot, scale = np.infty))
                classes[6-j+i].add(MTex(r"\bar"+str((i+2*j)%5), color = BLACK).scale(0.5).shift(position))
        random.shuffle(anims)
        self.play(LaggedStart(*anims, run_time = 2, lag_ratio = 0.1))
        self.play(ShowIncreasingSubsets(VGroup(*classes)), run_time = 2, rate_func = linear)
        self.wait(1+2+0-4, 28+1+15) #复平面上的所有整点 都可以放进某一个剩余类里面 （空闲）

        shade = Shade()
        points = [dots[24].copy(), dots[25].copy(), dots[17].copy(), dots[23].copy(), dots[31].copy()]
        inside_indices = [classes[6][3].copy(), classes[7][3].copy(), classes[5][3].copy(), classes[5][2].copy(), classes[7][2].copy()]
        circle = Circle(color = WHITE, radius = 1.4)
        rows_mul = VGroup(VGroup(MTex(r"\times").shift(1.8*UP + 0.6*RIGHT), *[MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(1.8*UP + 1.4*RIGHT + 0.8*i*RIGHT) for i in range(5)]), *[
            VGroup(MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(UP + 0.6*RIGHT + 0.8*i*DOWN), *[MTex(r"\bar"+str((i*j)%5), color = colors[(i*j)%5]).scale(0.8).shift(UP + 1.4*RIGHT + 0.8*i*DOWN + 0.8*j*RIGHT) for j in range(5)]) for i in range(5)])
        line_h_mul = Line(1.4*UP + 0.2*RIGHT, 1.4*UP + 5.0*RIGHT)
        line_v_mul = Line(2.2*UP + 1.0*RIGHT, 2.6*DOWN + 1.0*RIGHT)
        tabel_mul = VGroup(rows_mul, line_h_mul, line_v_mul)
        self.add(shade, self.notice, *points, circle).play(FadeIn(shade), ShowCreation(circle), *[mob.animating(rate_func = rush_from).scale(1.5).set_color(BACK) for mob in points], 
                                          inside_indices[0].animate.scale(2).set_color(BLUE_B), inside_indices[1].animate.scale(2).set_color(BLUE_D), 
                                          inside_indices[2].animate.scale(2).set_color(BLUE), inside_indices[3].animate.scale(2).set_color(BLUE_D), 
                                          inside_indices[4].animate.scale(2).set_color(BLUE))
        self.remove(*points).play(*[mob.animate.shift(3*LEFT) for mob in [circle, *inside_indices]])
        self.wait(0, 13) #这样 复平面的原点
        self.wait(2, 5) #以及原点周围的四个单位根
        outside_indices = [inside_indices[i+1].copy().shift(0.8*unit(i*PI/2)) for i in range(4)]
        self.play(*[TransformFromCopy(inside_indices[i+1], outside_indices[i]) for i in range(4)], FadeIn(tabel_mul, 0.5*LEFT))
        self.wait(1, 9) #就天然地构成了一个乘法表盘
        self.wait(0, 20) #（空闲）

        alpha = ValueTracker(0.0)
        def revolution_updater(index: int):
            def util(mob: VMobject):
                angle = alpha.get_value()
                mob.move_to(unit(index*TAU/4 + angle) + 3*LEFT)
            return util
        for i in range(4):
            inside_indices[i+1].add_updater(revolution_updater(i))
        indicate = Rectangle(height = 0.6, width = 4.6, color = YELLOW).shift(2.6*RIGHT + 0.2*UP)
        self.play(ShowCreation(indicate))
        self.wait(0, 19) #无论我们为表盘乘上......
        self.wait(2, 24) #......1......
        self.play(alpha.animating(run_time = 1/5).set_value(PI/2), indicate.animating(run_time = 0.5).shift(0.8*DOWN), frames = 30)
        self.wait(1, 23) #......2......
        self.play(alpha.animating(run_time = 1/5).set_value(0), indicate.animating(run_time = 0.5).shift(0.8*DOWN))
        self.play(alpha.animating(run_time = 1/5).set_value(-PI/2), frames = 15)
        self.wait(1, 24) #......3......
        self.play(alpha.animating(run_time = 1/5).set_value(-PI), indicate.animating(run_time = 0.5).shift(0.8*DOWN), frames = 30)
        self.wait(2, 6) #......还是4
        for i in range(4):
            inside_indices[i+1].clear_updaters()
        self.frames -= 240
        self.wait(3, 14) #对应的操作都只是把表盘旋转到对应的位置上
        self.wait(1, 1) #（空闲）

        self.wait(1, 9) #不止如此......
        self.play(*[FadeOut(mob) for mob in [*inside_indices, *outside_indices, circle, tabel_mul, indicate]], self.change_notice())
        self.play(FadeOut(shade))
        self.wait(0, 13) #......我们要是放眼整个复平面的话
        cross = SquareCross(side_length = 1, color = YELLOW_E)
        self.wait(1, 13) #就会发现......
        self.play(ShowCreation(cross))
        self.wait(0, 22) #......刚刚取出的这5个点
        self.wait(1, 23) #天然地构成了一个十字形
        self.wait(0, 22) #（空闲）
        crosses = [cross.copy().shift(RIGHT+2*UP), cross.copy().shift(UP+2*LEFT), cross.copy().shift(LEFT+2*DOWN), cross.copy().shift(DOWN+2*RIGHT)]
        self.add(*crosses, *dots, *classes).play(LaggedStart(*[TransformFromCopy(cross, mob) for mob in crosses], run_time = 2, lag_ratio = 0.5))
        self.wait(1, 19) #而我们可以用复数的加法来平移这这个十字形

        lines = VGroup(Line(3.5*RIGHT+0.5*DOWN, 3.5*RIGHT+0.5*UP), Line(2.5*UR, 2.5*UR+RIGHT).add_line_to(2.5*UR+DR), Line(2.5*UR, 2.5*UR+UP).add_line_to(3.5*UR), 
                       Line(3.5*UP+0.5*RIGHT, 3.5*UP+0.5*LEFT), Line(2.5*UL, 2.5*UL+UP).add_line_to(2.5*UL+UR), Line(2.5*UL, 2.5*UL+LEFT).add_line_to(3.5*UL), 
                       Line(3.5*LEFT+0.5*UP, 3.5*LEFT+0.5*DOWN), Line(2.5*DL, 2.5*DL+LEFT).add_line_to(2.5*DL+UL), Line(2.5*DL, 2.5*DL+DOWN).add_line_to(3.5*DL), 
                       Line(3.5*DOWN+0.5*LEFT, 3.5*DOWN+0.5*RIGHT), Line(2.5*DR, 2.5*DR+DOWN).add_line_to(2.5*DR+DL), Line(2.5*DR, 2.5*DR+RIGHT).add_line_to(3.5*DR)).set_stroke(color = YELLOW_E)
        self.play(ShowCreation(lines, lag_ratio = 0.5, run_time = 2))
        self.wait(0, 10) #最终可以使它铺满整个复平面
        self.wait(0, 19) #（空闲）

        self.wait(2, 12) #这恰好就是十字形的密铺
        self.wait(2, 6) #也就是种甘蔗的最优方案
        self.wait(0, 22) #（空闲）

        self.add(shade, self.notice).play(FadeIn(shade))
        self.clear().add(self.notice.shift(0.5*UP))
        camera.move_to(ORIGIN)
        inside_indices = [MTex(r"\bar" + str(i), color = ratio_color(i/5, BLUE_B, BLUE_D)).shift(1.6*unit(PI/2-i*TAU/5)) for i in range(0, 5)]
        midium_circle = Arc(radius = 2, start_angle = PI/2, angle = TAU)
        outside_indices = [MTex(r"\bar" + str(i), color = ratio_color(i/5, BLUE_B, BLUE_D)).shift(2.4*unit(PI/2-i*TAU/5)) for i in range(0, 5)]
        add_plate = VGroup(*inside_indices, midium_circle, *outside_indices).shift(3*LEFT)
        inside_indices = [MTex(r"\bar0", color = BLUE_B), MTex(r"\bar1", color = BLUE).shift(1.6*RIGHT), MTex(r"\bar2", color = BLUE_D).shift(1.6*UP), MTex(r"\bar4", color = BLUE).shift(1.6*LEFT), MTex(r"\bar3", color = BLUE_D).shift(1.6*DOWN)]
        midium_circle = Arc(radius = 2, start_angle = PI/2, angle = TAU)
        outside_indices = [MTex(r"\bar0", color = BLUE_B), MTex(r"\bar1", color = BLUE).shift(2.4*RIGHT), MTex(r"\bar2", color = BLUE_D).shift(2.4*UP), MTex(r"\bar4", color = BLUE).shift(2.4*LEFT), MTex(r"\bar3", color = BLUE_D).shift(2.4*DOWN)]
        mul_plate = VGroup(*inside_indices, midium_circle, *outside_indices).shift(3*RIGHT)
        self.play(FadeIn(add_plate), FadeIn(mul_plate), self.change_notice())
        self.wait(1, 1) #5个剩余类如此 那别的模运算呢
        self.wait(0, 18) #（空闲）

        arrow = Arrow(3.2*UP + 3*LEFT, 2.8*UP + 3*LEFT, buff = 0, color = YELLOW)
        add_notation = MTexText("所有正整数都有", color = YELLOW).scale(0.6).next_to(3.1*UP + 3*LEFT, UP).add(arrow)
        arrow = Arrow(3.2*UP + 3*RIGHT, 2.8*UP + 3*RIGHT, buff = 0, color = YELLOW)
        mul_notation = MTexText("只有$m=2, 4, p^k, 2p^k$有", color = YELLOW).scale(0.6).next_to(3.1*UP + 3*RIGHT, UP).add(arrow)
        arrow = Arrow(2.8*UP + 2*RIGHT, 3.2*UP + 2*RIGHT, buff = 0, color = YELLOW)
        notation_notation = MTexText("所有素数都有", color = YELLOW).scale(0.6).next_to(2.9*UP + 1.5*RIGHT, DOWN).add(arrow)
        self.play(FadeIn(add_notation, 0.2*DOWN), run_time = 1/3, frames = 30)
        self.wait(1, 1) #它们当然也有加法表盘
        self.wait(1, 27) #那它们也有乘法表盘吗
        self.wait(0, 20) #（空闲）
        self.wait(1, 7) #答案是不一定
        self.wait(0, 18) #（空闲）
        self.play(FadeIn(mul_notation, 0.2*DOWN), run_time = 1/3, frames = 30)
        self.wait(1, 15) #这和数论中一个叫“原根”的概念有关
        self.wait(0, 17) #（空闲）
        self.wait(3, 4) #只有有原根的数 才会有乘法表盘
        self.wait(0, 20) #（空闲）
        self.play(FadeIn(notation_notation, 0.2*UP), run_time = 1/3, frames = 30)
        self.wait(2, 2) #幸运的是 所有的素数都有原根
        self.wait(0, 19) #（空闲）
        self.wait(3, 14) #下一节 我们就来找几个素数看看吧
        self.wait(2, 28)
        self.play(FadeIn(shade))
        self.wait(2, 0) #到此共79+8秒

#################################################################### 

class Chapter2_0(FrameScene):

    def construct(self):

        text2 = Text("第二节 复平面上的格点", font = 'simsun', t2c={"第二节": YELLOW, "复平面": GREEN, "格点": BLUE})

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(FrameScene):
    def construct(self):
        self.notices = [Notice("平凡情况", "请　显然"),
                        Notice("有趣情况", "请　思考")]
        self.notice = self.notices[0]

        inside_indices = [MTex(r"\bar0", color = BLUE_B), MTex(r"\bar1", color = BLUE).shift(1.6*RIGHT)]
        midium_circle = Arc(radius = 2, start_angle = PI/2, angle = TAU)
        outside_indices = [MTex(r"\bar0", color = BLUE_B), MTex(r"\bar1", color = BLUE).shift(2.4*RIGHT)]
        mul_plate_2 = VGroup(*inside_indices, midium_circle, *outside_indices)

        self.play(FadeIn(mul_plate_2, 0.5*RIGHT), Write(self.notice))
        self.wait(0, 22) #这是2的乘法表盘
        self.wait(2, 0) #唯一的运算是乘1
        self.wait(2+0-1, 3+23)
        self.play(FadeOut(mul_plate_2, 0.5*RIGHT)) #表盘不动 没什么意思 （空闲）

        inside_indices = [MTex(r"\bar0", color = BLUE_B), MTex(r"\bar1", color = BLUE).shift(1.6*RIGHT), MTex(r"\bar2", color = BLUE_D).shift(1.6*LEFT)]
        midium_circle = Arc(radius = 2, start_angle = PI/2, angle = TAU)
        outside_indices = [MTex(r"\bar0", color = BLUE_B), MTex(r"\bar1", color = BLUE).shift(2.4*RIGHT), MTex(r"\bar2", color = BLUE_D).shift(2.4*LEFT)]
        mul_plate_3 = VGroup(*inside_indices, midium_circle, *outside_indices)
        alpha = ValueTracker(0.0)
        def revolution_updater(index: int):
            def util(mob: VMobject):
                angle = alpha.get_value()
                mob.move_to(1.6*unit(index*PI + angle))
            return util
        self.play(FadeIn(mul_plate_3, 0.5*RIGHT))
        self.wait(0, 24) #这是3的乘法表盘
        self.wait(1, 21) #也只有两种运算
        for i in range(2):
            inside_indices[i+1].add_updater(revolution_updater(i))
        self.play(alpha.animate.set_value(PI), run_time = 0.5, frames = 30)
        for i in range(2):
            inside_indices[i+1].clear_updaters()
        self.wait(1, 20) #分别是乘1和旋转半圈
        self.wait(1+0-1, 3+25)
        self.play(FadeOut(mul_plate_3, 0.5*RIGHT)) #也没什么意思（空闲）

        inside_indices = [MTex(r"\bar0", color = BLUE_B), MTex(r"\bar1", color = BLUE).shift(1.6*RIGHT), MTex(r"\bar2", color = BLUE_D).shift(1.6*UP), MTex(r"\bar4", color = BLUE).shift(1.6*LEFT), MTex(r"\bar3", color = BLUE_D).shift(1.6*DOWN)]
        midium_circle = Arc(radius = 2, start_angle = PI/2, angle = TAU)
        outside_indices = [MTex(r"\bar0", color = BLUE_B), MTex(r"\bar1", color = BLUE).shift(2.4*RIGHT), MTex(r"\bar2", color = BLUE_D).shift(2.4*UP), MTex(r"\bar4", color = BLUE).shift(2.4*LEFT), MTex(r"\bar3", color = BLUE_D).shift(2.4*DOWN)]
        mul_plate_5 = VGroup(*inside_indices, midium_circle, *outside_indices)
        self.play(FadeIn(mul_plate_5, 0.5*RIGHT))
        self.wait(1, 17) #5我们在之前已经看过了
        self.wait(2+0-1, 8+29) 
        self.play(FadeOut(mul_plate_5, 0.5*RIGHT), self.change_notice()) #接下来让我们看看7的情况 （空闲）

        h_lines = VGroup(*[Line(3.3*LEFT+(i-3)*DOWN, 3.3*RIGHT+(i-3)*DOWN, stroke_width = 1) for i in range(7)]).shift(0.5*UP)
        v_lines = VGroup(*[Line(3.3*UP+(i-3)*RIGHT, 3.3*DOWN+(i-3)*RIGHT, stroke_width = 1) for i in range(7)]).shift(0.5*UP)
        h_lines[3].set_stroke(width = 4)
        v_lines[3].set_stroke(width = 4)
        point_center = Dot(0.5*UP, radius = 0.2, color = BLUE)
        tex_center = MTex(r"\bar0", color = BLACK).scale(0.5).shift(0.5*UP)
        self.play(Write(VGroup(h_lines, v_lines), lag_ratio = 0.2), ShowCreation(point_center, rate_func = (squish_rate_func(smooth, 0.5, 1))), run_time = 2)
        self.play(Write(tex_center))
        self.wait(2+2-3, 15+10) #想要造出7个剩余类的乘法表 我们就需要在复平面上找6个点
        self.wait(0, 18) #（空闲）

        colors = [interpolate_color(BLUE, color, 0.2) for color in [RED, ORANGE, YELLOW, GREEN, TEAL, PURPLE]] + [BLUE]
        points = [Dot(0.5*UP+unit(i*TAU/6), radius = 0.2, color = colors[i] ) for i in range(6)]
        texes = [Tex(r"\bar"+str((3**i)%7), color = BLACK).scale(0.5).shift(0.5*UP+unit(i*TAU/6)) for i in range(6)]
        self.play(ShowCreation(points[0]), ShowCreation(points[3]))
        self.wait(1, 26) #其中两个点肯定是1和-1
        self.play(Write(texes[0]), Write(texes[3]))
        self.wait(1, 25) #分别对应着剩余类1和剩余类6
        self.wait(0, 16) #（空闲）

        temp_tex = [Tex(r"-\omega^2", color = colors[1]).scale(0.5).shift(0.5*UP+1.5*unit(TAU/6)), Tex(r"\omega", color = colors[2]).scale(0.5).shift(0.5*UP+1.5*unit(TAU/3)), Tex(r"\omega^2", color = colors[4]).scale(0.5).shift(0.5*UP+1.5*unit(-TAU/3)), Tex(r"-\omega", color = colors[5]).scale(0.5).shift(0.5*UP+1.5*unit(-TAU/6))]
        self.play(ShowCreation(VGroup(points[1], points[2], points[4], points[5]), lag_ratio = 0.5, run_time = 1.5), 
                  ShowCreation(VGroup(*temp_tex), lag_ratio = 0.5, run_time = 1.8, rate_func = squish_rate_func(smooth, 1/6, 1)), frames = 60)
        self.wait(1, 12) #还有四个点 它们的立方分别是±1
        self.wait(0, 19) #（空闲）

        self.wait(2, 19) #剩下的剩余类怎么分配呢
        self.wait(1, 26) #其实还是开根号
        self.wait(1, 21) #不过这次开的是立方根
        self.wait(0, 19) #（空闲）

        mtex_1 = MTex(r"\begin{cases}\omega^3=1\\2^3=8\end{cases}", tex_to_color_map = {(r"1", r"8"): colors[0], (r"2", r"\omega"): colors[2]}).next_to(6.5*LEFT)
        self.play(Write(mtex_1))
        self.wait(2, 0) #由于1和8属于同一个剩余类
        self.wait(2, 2) #对它们同时开立方
        self.play(FadeOut(temp_tex[1], -0.5*unit(TAU/3)), Write(texes[2]))
        self.wait(2, 1) #就可以得到ω和2属于同一个等价类
        self.wait(0, 19) #（空闲）

        self.play(LaggedStart(FadeOut(temp_tex[0], -0.5*unit(TAU/6)), FadeOut(temp_tex[2], -0.5*unit(-TAU/3)), FadeOut(temp_tex[3], -0.5*unit(-TAU/6), lag_ratio = 0.3)),
                  LaggedStart(Write(texes[1]), Write(texes[4]), Write(texes[5]), lag_ratio = 0.3), FadeOut(mtex_1), frames = 60)
        self.wait(0, 22) #再配合上复平面上的加法和乘法
        self.wait(2, 22) #我们就可以把剩下的剩余类都分配掉
        self.wait(0, 17) #（空闲）

        circle_stroke = Circle(color = WHITE, radius = 1.4).shift(0.5*UP)
        circle_back = Circle(stroke_width = 0, fill_opacity = 1, fill_color = BACK, radius = 1.4).shift(0.5*UP)
        points.append(point_center)
        texes.append(tex_center)
        points_copy = VGroup(*points).copy()
        texes_copy = VGroup(*texes).copy()
        self.add(points_copy, texes_copy, circle_back, *points, circle_stroke, *texes).play(ShowCreation(circle_stroke), FadeIn(circle_back),
                                                                   *[mob.animate.scale(2).set_color(BACK) for mob in points], 
                                                                   *[texes[i].animate.scale(2).set_color(colors[i]) for i in range(7)])
        self.remove(*points).play(*[mob.animate.shift(5*LEFT) for mob in [circle_back, circle_stroke, *texes]])
        self.wait(0, 10) #这就是7个剩余类的乘法表了
        self.wait(0, 26) #到此共61秒

class Chapter2_2(FrameScene):
    def construct(self):
        self.notices = [Notice("有趣情况", "请　思考"),
                        Notice("总结规律", "请　模仿"),
                        Notice("规律炸了", "请勿模仿"),
                        Notice("正确规律", "请记笔记")]
        self.notice = self.notices[0]

        offset = 0.5*UP
        h_lines = VGroup(*[Line(3.3*LEFT+(i-3)*DOWN, 3.3*RIGHT+(i-3)*DOWN, stroke_width = 1) for i in range(7)]).shift(offset)
        v_lines = VGroup(*[Line(3.3*UP+(i-3)*RIGHT, 3.3*DOWN+(i-3)*RIGHT, stroke_width = 1) for i in range(7)]).shift(offset)
        h_lines[3].set_stroke(width = 4)
        v_lines[3].set_stroke(width = 4)

        mul_colors = [interpolate_color(BLUE, color, 0.2) for color in [RED, ORANGE, YELLOW, GREEN, TEAL, PURPLE]] + [BLUE]
        old_points = [Dot(offset+unit(i*TAU/6), radius = 0.2, color = mul_colors[i] ) for i in range(6)] + [Dot(offset, radius = 0.2, color = BLUE)]
        old_texes = [MTex(r"\bar"+str((3**i)%7), color = BLACK).scale(0.5).shift(offset+unit(i*TAU/6)) for i in range(6)] + [MTex(r"\bar0", color = BLACK).scale(0.5).shift(offset)]
        
        numbers = [MTex(r"\bar"+str((3**i)%7), color = mul_colors[i]).shift(offset+5*LEFT+unit(i*TAU/6)) for i in range(6)] + [MTex(r"\bar0", color = BLUE).shift(offset+5*LEFT)]
        circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*LEFT).add(*numbers)
        
        self.add(self.notice, h_lines, v_lines, *old_points, *old_texes, circle)
        self.play(FadeOut(circle))
        self.wait(0, 27) #我们试着像5那样

        scale = 3
        colors = [BLUE, mul_colors[0], mul_colors[2], mul_colors[1], mul_colors[4], mul_colors[5], mul_colors[3]]
        dots = []
        groups_dot = [[], [], [], []]
        texes = []
        groups_tex = [[], [], [], []]
        hexes = []
        lines = []
        for i in range(-scale, scale+1):
            endpoints = max(i, 0)-scale, min(0, i)+scale
            lines.extend([Line(i*unit(TAU/3) + endpoints[0]*RIGHT + offset, i*unit(TAU/3) + endpoints[1]*RIGHT + offset, stroke_width = 1), 
                          Line(i*unit(2*TAU/3) + endpoints[0]*unit(TAU/3) + offset, i*unit(2*TAU/3) + endpoints[1]*unit(TAU/3) + offset, stroke_width = 1), 
                          Line(i*RIGHT + endpoints[0]*unit(2*TAU/3) + offset, i*RIGHT + endpoints[1]*unit(2*TAU/3) + offset, stroke_width = 1)])
            for j in range(endpoints[0], endpoints[1]+1):
                position = i*unit(TAU/3) + j*RIGHT + offset
                residue = (2*i+j)%7
                group = max(abs(i), abs(j), abs(i-j))
                dot = Dot(position, radius = 0.2, color = colors[residue], n_components = 24).rotate(PI/2)
                hex = RegularPolygon(start_angle = PI/2, stroke_width = 0, fill_opacity = 1, fill_color = colors[residue]).insert_n_curves(18).set_width(0.96).shift(position)
                hex.position = (i, j)
                tex = MTex(r"\bar"+str(residue), color = BLACK).scale(0.5).shift(position)
                dots.append(dot)
                groups_dot[group].append(dot)
                texes.append(tex)
                groups_tex[group].append(tex)
                hexes.append(hex)
        self.add(*groups_dot[2], *groups_dot[3], *groups_tex[2], *groups_tex[3]).play(LaggedStart(ShowCreation(VGroup(*groups_dot[2]), lag_ratio = 0), 
                              AnimationGroup(ShowCreation(VGroup(*groups_dot[3]), lag_ratio = 0), AnimationGroup(*[ShowCreation(mob) for mob in groups_tex[2]])), 
                              AnimationGroup(*[ShowCreation(mob) for mob in groups_tex[3]]), lag_ratio = 0.7, run_time = 2.4, group = VGroup()), 
                FadeOut(h_lines), FadeOut(v_lines), frames = 86) # 把这七个点也向四周延伸 （空闲）

        self.remove(*old_points, *old_texes).add(*lines, *dots, *texes).play(
            LaggedStart(*[AnimationGroup(*[Expand(mob) for mob in group]) for group in [lines[9:12], lines[6:9]+lines[12:15], lines[3:6]+lines[15:18], lines[0:3]+lines[18:21]]],
                              lag_ratio = 0.2, group = VGroup()), run_time = 2)
        self.wait(0, 29) #这会形成一个覆盖复平面的三角形点阵
        self.wait(0, 18) #（空闲）

        self.play(LaggedStart(*[Transform(dots[i], hexes[i]) for i in range(37)], lag_ratio = 0.05, group = VGroup()),
                  LaggedStart(*[tex.animate.scale(1.5) for tex in texes], lag_ratio = 0.05, group = VGroup()), run_time = 3)
        self.play(*[FadeOut(line) for line in lines])
        self.wait(1+2-4, 19+28) #以每个点为中心 可以把平面分隔成一个个六边形区域
        self.wait(0, 17) #（空闲）

        funcs = [lambda t: 2/np.sqrt(3)*unit(t*TAU/6+PI/6) + 1/np.sqrt(3)*unit(t*TAU/6-PI/6), 
                 lambda t: 2/np.sqrt(3)*unit(t*TAU/6+PI/6), 
                 lambda t: 2/np.sqrt(3)*unit(t*TAU/6+PI/6) + 1/np.sqrt(3)*unit(t*TAU/6+PI/2)]
        region = Polygon(*[func(t) for t in range(6) for func in funcs], color = YELLOW_E).shift(offset)
        lines = [Polyline(2/np.sqrt(3)*unit(t*TAU/6+PI/6) + 1/np.sqrt(3)*unit(t*TAU/6-PI/6), 3/np.sqrt(3)*unit(t*TAU/6+PI/6) + 1/np.sqrt(3)*unit(t*TAU/6-PI/6), 
                          3/np.sqrt(3)*unit(t*TAU/6+PI/6) + 2/np.sqrt(3)*unit(t*TAU/6-PI/6), 4/np.sqrt(3)*unit(t*TAU/6+PI/6) + 2/np.sqrt(3)*unit(t*TAU/6-PI/6),
                          color = YELLOW_E).shift(offset) for t in range(6)]
        self.play(ShowCreation(region))
        self.wait(1, 3) #再以七个六边形为一组
        self.play(*[ShowCreation(line) for line in lines])
        self.wait(1, 6) #按复数加法的方式平移
        self.wait(2, 13) #我们就能得到关于它的周期性密铺
        self.wait(0, 18) #（空闲）

        nazca = ImageMobject("nazca.png").set_width(0.75)
        nazcas = []
        groups = []
        anims = []
        for i in [2, 4, 14, 18, 22, 32, 34]:
            hex = dots[i].copy().set_color(BACK)
            mobject = VGroup(dots[i], texes[i])
            target = Group(hex, nazca.copy().move_to(hex.get_center()))
            nazcas.append(target)
            groups.append(mobject)
            anims.append(Flip(mobject, target))
        self.add(*nazcas, *groups).play(LaggedStart(*anims, group = VGroup()), run_time = 2)
        self.wait(1, 15) #如果你玩的游戏不是mc 而是文明
        self.wait(3, 9) #这种密铺的方案应该能为你的城市规划起到帮助
        self.wait(0, 27) #（空闲）

        numbers = [MTex(r"\bar"+str((3**i)%7), color = mul_colors[i]).scale(0.9).shift(offset+5*RIGHT+unit(i*TAU/6)) for i in range(6)] + [MTex(r"\bar0", color = BLUE).scale(0.9).shift(offset+5*RIGHT)]
        mul_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*RIGHT).add(*numbers)
        numbers = [MTex(r"\bar"+str(i), color = ratio_color(i/7, BLUE_B, BLUE_D)).scale(0.9).shift(offset+5*LEFT+unit(PI/2-i*TAU/7)) for i in range(7)]
        add_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*LEFT).add(*numbers)
        title_7 = MTex(r"{p=7}").scale(2).shift(3*UP + 5*LEFT)
        
        self.add(*groups, *nazcas).play(LaggedStart(*[Flip(nazcas[i], groups[i]) for i in range(7)], group = VGroup(), run_time = 2), self.change_notice(), *[FadeIn(mob, rate_func = squish_rate_func(smooth, 1/2, 1)) for mob in [title_7, mul_circle, add_circle]])
        self.wait(1+4-2, 4+14) #这么看来 每一个素数 都对应着一个加法表和一个乘法表
        self.wait(2, 3) #又都对应着一种密铺方案
        self.wait(0, 21) #（空闲）
        
        self.fade_out(run_time = 0.5)
        numbers = [MTex(r"\bar"+str((2**i)%5), color = interpolate_color(BLUE, BLUE_D, i%2)).scale(0.9).shift(offset+5*RIGHT+unit(i*TAU/4)) for i in range(4)] + [MTex(r"\bar0", color = BLUE_B).scale(0.9).shift(offset+5*RIGHT)]
        mul_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*RIGHT).add(*numbers)
        numbers = [MTex(r"\bar"+str(i), color = ratio_color(i/5, BLUE_B, BLUE_D)).scale(0.9).shift(offset+5*LEFT+unit(PI/2-i*TAU/5)) for i in range(5)]
        add_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*LEFT).add(*numbers)
        title_5 = MTex(r"{p=5}").scale(2).shift(3*UP + 5*LEFT)
        squares = []
        for i in range(-3, 4):
            for j in range(-3, 4):
                position = i*RIGHT + j*UP +offset
                residue = i*3-j
                color = int(bool(residue%5)^bool(residue%2))
                square = Square(side_length = 0.9, stroke_width = 0, fill_opacity = 1, fill_color = interpolate_color(BLUE, GREEN, color)).shift(position)
                square.position = (i, j)
                squares.append(square)
        self.fade_in(mul_circle, add_circle, title_5, *squares, run_time = 0.5).wait(2, 5) #像是我们已经见过的5和7

        self.fade_out(run_time = 0.5)
        numbers = [MTex(r"\bar1", color = BLUE_D).scale(0.9).shift(offset+5*RIGHT+unit(0)), MTex(r"\bar0", color = BLUE_B).scale(0.9).shift(offset+5*RIGHT)]
        mul_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*RIGHT).add(*numbers)
        numbers = [MTex(r"\bar"+str(i), color = ratio_color(i/2, BLUE_B, BLUE_D)).scale(0.9).shift(offset+5*LEFT+unit(PI/2-i*PI)) for i in range(2)]
        add_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*LEFT).add(*numbers)
        title_2 = MTex(r"{p=2}").scale(2).shift(3*UP + 5*LEFT)
        colors = [PURPLE_B, BLUE, GREEN]
        for i in range(-3, 4):
            for j in range(-3, 4):
                residue = (i+j*3)%6
                index = int(residue/2)
                square = squares[(i+3)*7+j+3].set_color(colors[index])
        self.fade_in(mul_circle, add_circle, title_2, *squares, run_time = 0.5).wait(1, 25) #还有更小一些的2和3
        self.wait(1, 0) #都是如此
        self.wait(0, 22) #（空闲）

        numbers = [MTex(r"\bar1", color = BLUE_D).scale(0.9).shift(offset+5*RIGHT+unit(0)), MTex(r"\bar2", color = BLUE_D).scale(0.9).shift(offset+5*RIGHT+unit(PI)), MTex(r"\bar0", color = BLUE_B).scale(0.9).shift(offset+5*RIGHT)]
        mul_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*RIGHT).add(*numbers)
        numbers = [MTex(r"\bar"+str(i), color = ratio_color(i/3, BLUE_B, BLUE_D)).scale(0.9).shift(offset+5*LEFT+unit(PI/2-i*TAU/3)) for i in range(3)]
        add_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*LEFT).add(*numbers)
        title_3 = MTex(r"{p=3}").scale(2).shift(3*UP + 5*LEFT)

        self.fade_out(run_time = 0.5)
        scale = 3
        colors = [PURPLE_B, BLUE, GREEN]
        index_row = 0
        for i in range(-scale, scale+1):
            endpoints = max(i, 0)-scale, min(0, i)+scale
            for j in range(endpoints[0], endpoints[1]+1):
                residue = (4*i+j+1)%9
                index = int(residue/3)
                hexes[index_row+j-endpoints[0]].set_color(colors[index])
            index_row += endpoints[1]+1 - endpoints[0]
        self.fade_in(mul_circle, add_circle, title_3, *hexes, run_time = 0.5).wait(1, 4) #这无疑是非常漂亮的结论
        self.play(self.change_notice()).wait(1, 22) #但不幸的是 规律到此结束了
        self.wait(0, 22) #（空闲）

        numbers = [MTex(r"\overline{"+str((2**i)%11)+r"}", color = ratio_color(i/10, BLUE, BLUE_D)).scale(0.6).shift(offset+5*RIGHT+unit(i*TAU/10)) for i in range(10)] + [MTex(r"\bar0", color = BLUE_B).scale(0.9).shift(offset+5*RIGHT)]
        mul_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*RIGHT).add(*numbers)
        numbers = [MTex(r"\overline{"+str(i)+r"}", color = ratio_color(i/11, BLUE_B, BLUE_D)).scale(0.6).shift(offset+5*LEFT+unit(PI/2-i*TAU/11)) for i in range(11)]
        add_circle = Circle(color = WHITE, radius = 1.4).shift(offset+5*LEFT).add(*numbers)
        title_11 = MTex(r"{p=11}").scale(2).shift(3*UP + 5*LEFT)

        self.fade_out(run_time = 0.5).fade_in(title_11, run_time = 0.5).wait(1, 17) #11这个素数并不对应着什么密铺
        self.wait(0, 17) #（空闲）
        self.wait(0, 27) #当然......
        self.play(FadeIn(mul_circle), FadeIn(add_circle))
        self.wait(2, 3) #......11的加法表和乘法表还是有的
        self.wait(1, 23) #只不过问题在于
        
        dot_0 = Dot(offset, radius = 0.1, color = BLUE)
        dots_1 = [Dot(offset+unit(i*TAU/10), color = BLUE) for i in range(10)]
        self.play(FadeOut(add_circle), FadeOut(mul_circle, 5*LEFT, run_time = 2), FadeIn(VGroup(*dots_1, dot_0), 5*LEFT, run_time = 2))
        self.wait(0, 9) #要是把11的乘法表展开
        dots_2 = [dot.copy().scale(0.75).set_opacity(0.75).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_1]
        group_2 = VGroup(*dots_2)
        dots_3 = [dot.copy().scale(2/3).set_opacity(0.5).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_2]
        group_3 = VGroup(*dots_3)
        dots_4 = [dot.copy().scale(0.5).set_opacity(0.25).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_3]
        group_4 = VGroup(*dots_4)
        dots_5 = [dot.copy().scale(0.5).set_opacity(0.15).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_4]
        self.bring_to_back(group_2).play(FadeIn(group_2))
        self.bring_to_back(group_3).play(FadeIn(group_3))
        self.bring_to_back(group_4).play(FadeIn(group_4))
        self.bring_to_back(*dots_5).play(*[FadeIn(dot) for dot in dots_5])
        self.wait(1+2-4, 17+4+26) #它不会形成点阵 而是会弥散到整个复平面上 #到此共66秒
        self.play(self.change_notice())
        self.wait(2+2-2, 25+0) #如果我们把所有的素数都试一遍 那么就会得到一个无奈的结论
        self.fade_out()

class Chapter2_3(FrameScene):
    def construct(self):
        self.notices = [Notice("正确规律", "请记笔记"),
                        Notice("强势安利", "快 去 看"), 
                        Notice("正确规律", "请记笔记")]
        self.notice = self.notices[0]

        self.frames += 145
        self.add(self.notice).wait(0, 17) #（空闲）

        offset_l = 3.5*LEFT + 0.5*UP
        numbers_5 = VGroup(*[MTex(r"\bar"+str((2**i)%5), color = ratio_color(i/2, BLUE_B, BLUE_D)).scale(0.75).shift(offset_l+0.75*unit(i*TAU/4)) for i in range(4)])
        number_0_5 = MTex(r"\bar0", color = BLUE).scale(0.75).shift(offset_l)
        circle_5 = Circle(color = WHITE, radius = 1.1).shift(offset_l)
        offset_r = 3.5*RIGHT + 0.5*UP
        numbers_7 = VGroup(*[MTex(r"\bar"+str((3**i)%7), color = ratio_color(i/3, BLUE_B, BLUE_D)).scale(0.75).shift(offset_r+0.75*unit(i*TAU/6)) for i in range(6)])
        number_0_7 = MTex(r"\bar0", color = BLUE).scale(0.75).shift(offset_r)
        circle_7 = Circle(color = WHITE, radius = 1.1).shift(offset_r)

        self.play(ShowCreation(circle_5), ShowCreation(circle_7), 
                  ShowIncreasingSubsets(numbers_5), ShowIncreasingSubsets(numbers_7), 
                  FadeIn(number_0_5), FadeIn(number_0_7))
        self.wait(1, 21) #把乘法表展开到整个复平面时

        scale_l = 4
        points_l = []
        points_l_center = []
        points_l_others = []
        squares = []
        for i in range(scale_l, -scale_l-1, -1):
            for j in range(-scale_l, scale_l+1):
                position = 0.75*(i*UP + j*RIGHT)
                distance = max(abs(i), abs(j))
                point = Dot(offset_l + position, color = BLUE, fill_opacity = clip((scale_l+1-distance)/scale_l, 0, 1), n_components = 24).rotate(PI/4)
                points_l.append(point)
                if abs(i) + abs(j) <= 1:
                    points_l_center.append(point)
                else:
                    points_l_others.append(point)
                square = Square(side_length = 0.75*0.95, fill_color = BLUE, fill_opacity = clip((scale_l+1-distance)/scale_l, 0, 1), stroke_width = 0).shift(position + offset_l)
                square.position = (i, j)
                squares.append(square)
        random.shuffle(points_l_others)
        others_l = VGroup(*points_l_others)

        scale_r = 6
        points_r = []
        points_r_center = []
        points_r_others = []
        hexes = []
        for i in range(scale_r, -scale_r-1, -1):
            endpoints = max(i, 0)-scale_r, min(0, i)+scale_r
            for j in range(endpoints[0], endpoints[1]+1):
                position = 0.75*(i*unit(TAU/3) + j*RIGHT)
                distance = max(abs(i), abs(j), abs(i-j))
                if abs(position[0]) < 3.3 and abs(position[1]) < 3.5:
                    point = Dot(position + offset_r, color = BLUE, fill_opacity = clip((scale_r+1-distance)/scale_r, 0, 1), n_components = 24).rotate(PI/2)
                    points_r.append(point)
                    if distance <= 1:
                        points_r_center.append(point)
                    else:
                        points_r_others.append(point)
                    hex = RegularPolygon(start_angle = PI/2, stroke_width = 0, fill_color = BLUE, fill_opacity = clip((scale_r+1-distance)/scale_r, 0, 1)).insert_n_curves(18).set_width(0.75*0.95).shift(position + offset_r)
                    hex.position = (i, j)
                    hexes.append(hex)
        random.shuffle(points_r_others)
        others_r = VGroup(*points_r_others)
        line = Line(3.8*UP, 2.8*DOWN)
        self.play(*[FadeOut(mob) for mob in [circle_5, circle_7, numbers_5, numbers_7, number_0_5, number_0_7]], 
                  *[FadeIn(mob) for mob in points_l_center + points_r_center],
                  ShowCreation(line))
        self.wait(0, 21) #只有两种情况下
        self.add(others_l, others_r, self.notice).play(FadeIn(others_l), FadeIn(others_r), lag_ratio = 0.1, run_time = 2)
        self.wait(1+0-2, 20+17) #乘法表会形成点阵 （空闲）
        
        self.wait(1, 8) #这两种点阵
        text_left = MTexText(r"高斯整数$\mathbb{Z}[i]$", tex_to_color_map = {r"\mathbb{Z}[i]": GREEN}).scale(0.8).next_to(3.5*LEFT+3*UP, UP)
        text_right = MTexText(r"艾森斯坦整数$\mathbb{Z}[\omega]$", tex_to_color_map = {r"\mathbb{Z}[\omega]": GREEN}).scale(0.8).next_to(3.5*RIGHT+3*UP, UP)
        self.play(Write(text_left))
        self.wait(1, 4) #分别叫做高斯整数集
        self.play(Write(text_right))
        self.wait(0, 25) #和艾森斯坦整数集
        self.wait(0, 23) #（空闲）

        self.add(*points_l, *points_r, text_left, text_right, self.notice).play(LaggedStart(*[Transform(points_l[i], squares[i]) for i in range(len(points_l))], lag_ratio = 0.02, group = VGroup()), 
                 LaggedStart(*[Transform(points_r[i], hexes[i]) for i in range(len(points_r))], lag_ratio = 0.02, group = VGroup()), run_time = 2)
        self.wait(0, 23) #我们之前分别见过它们的密铺方案
        self.wait(3, 19) #十字形和蜂巢状的密铺图案都是周期性的
        arrow_l = CurvedArrow(offset_l+1.5*unit(0), offset_l+1.5*unit(PI/2), offset = 0, color = GREEN)
        text_l = MTex(r"90^\circ").scale(0.8).shift(offset_l+2*unit(PI/4))
        arrow_r = CurvedArrow(offset_r+1.5*unit(0), offset_r+1.5*unit(PI/3), offset = 0, color = GREEN)
        text_r = MTex(r"60^\circ").scale(0.8).shift(offset_r+2.2*unit(PI/6))
        self.play(ShowCreation(arrow_l), ShowCreation(arrow_r), Write(text_l), Write(text_r))
        self.wait(1, 7) #而且都有不错的旋转对称性
        self.wait(0, 15) #（空闲）

        self.wait(2, 27) #而这样的密铺 其实不是唯一的
        self.wait(0, 22) #（空闲）
        self.play(*[FadeOut(mob, 1.75*RIGHT, rate_func = rush_into) for mob in points_r + [line, arrow_l, text_l, arrow_r, text_r, text_left, text_right]],
                  *[mob.animating(run_time = 2).shift(3.5*RIGHT) for mob in points_l])
        for square in squares:
            position = square.position
            square.shift(3.5*RIGHT).set_opacity(1).set_color(GREEN if (position[0]+position[1])%2 else BLUE)
        self.play(*[Transform(points_l[i], squares[i]) for i in range(len(points_l))])
        self.wait(1+2-3, 27+10) #就拿高斯整数来说 我们既可以一个正方形一组
        self.frames -= 30
        self.wait(1)

        self.fade_out(run_time = 0.5)
        scale = 5
        side_length = 3.5/(scale+0.5)
        offset = 0.5*UP
        squares = []
        for i in range(-scale, scale+1):
            for j in range(-scale, scale+1):
                position = side_length*(i*RIGHT + j*UP) + offset
                residue = i*3-j
                color = int(bool(residue%5)^bool(residue%2))
                square = Square(side_length = 0.95*side_length, stroke_width = 0, fill_opacity = 1, 
                                fill_color = GREEN if color else BLUE).shift(position)
                squares.append(square)
        self.fade_in(*squares, run_time = 0.5)
        self.wait(1, 14) #也可以五个正方形一组
        self.frames -= 60
        self.wait(2)

        self.fade_out(run_time = 0.5)
        scale = 6
        side_length = 3.5/(scale+0.5)
        offset = 0.5*UP
        squares = []
        for i in range(-scale, scale+1):
            for j in range(-scale, scale+1):
                position = side_length*(i*RIGHT + j*UP) + offset
                residue = (i+1)//3 + (j+1)//3
                color = residue%2
                square = Square(side_length = 0.95*side_length, stroke_width = 0, fill_opacity = 1, 
                                fill_color = GREEN if color else BLUE).shift(position)
                squares.append(square)
        self.fade_in(*squares, run_time = 0.5)
        self.wait(1, 14) #还可以九个正方形一组
        self.frames -= 60
        self.wait(2)

        self.fade_out(run_time = 0.5)
        scale = 7
        side_length = 3.5/(scale+0.5)
        offset = 0.5*UP
        list_green = [3, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 19, 23]
        squares = []
        for i in range(-scale, scale+1):
            for j in range(-scale, scale+1):
                position = side_length*(i*RIGHT + j*UP) + offset
                residue = (i-j*5)%26
                color = GREEN if residue in list_green else BLUE
                square = Square(side_length = 0.95*side_length, stroke_width = 0, fill_opacity = 1, 
                                fill_color = color).shift(position)
                square.position = (i, j)
                squares.append(square)
        self.fade_in(*squares, run_time = 0.5)
        self.wait(1, 15) #或者十三个正方形一组
        self.frames -= 60
        self.wait(2)

        self.fade_out(run_time = 0.5)
        scale = 8
        side_length = 3.5/(scale+0.5)
        offset = 0.5*UP
        list_green = [2, 3, 4, 5, 6, 8, 10, 16, 17, 18, 24, 26, 28, 29, 30, 31, 32]
        squares = []
        for i in range(-scale, scale+1):
            for j in range(-scale, scale+1):
                position = side_length*(i*RIGHT + j*UP) + offset
                residue = (i+j*13)%34
                color = GREEN if residue in list_green else BLUE
                square = Square(side_length = 0.95*side_length, stroke_width = 0, fill_opacity = 1, 
                                fill_color = color).shift(position)
                square.position = (i, j)
                squares.append(square)
        self.fade_in(*squares, run_time = 0.5)
        self.wait(1, 4) #乃至十七个正方形一组
        self.frames -= 60
        self.wait(2)
        self.wait(0, 27) #（空闲）

        self.fade_out(run_time = 0.5)
        scale = 9
        side_length = 3.5/(scale+0.5)
        offset = 0.5*UP
        squares = []
        for i in range(-scale, scale+1):
            for j in range(-scale, scale+1):
                position = side_length*(i*RIGHT + j*UP) + offset
                residue = (i+3)//7 + (j+1)//3
                color = residue%2
                square = Square(side_length = 0.95*side_length, stroke_width = 0, fill_opacity = 1, 
                                fill_color = GREEN if color else BLUE).shift(position)
                squares.append(square)
        self.fade_in(*squares, run_time = 0.5)
        self.wait(1, 20) #二十一个正方形虽然也能编组
        self.wait(2, 10) #但它就没有那么好的旋转对称性了
        self.wait(0, 23) #（空闲）

        self.fade_out()

        text_1 = MTex(r"n=1").shift(1.5*UP)
        square_1 = Square(side_length = 0.9, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1)
        group_1 = VGroup(square_1, text_1).shift(5*LEFT + 1.7*UP)
        text_5 = MTex(r"n=5").shift(1.5*UP)
        coordinate_5 = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]
        group_5 = VGroup(text_5)
        for coordinate in coordinate_5:
            position = 0.7*(coordinate[0]*UP + coordinate[1]*RIGHT)
            residue = (coordinate[0] + coordinate[1]*2)%5
            group_5.add(Square(side_length = 0.95*0.7, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1).shift(position))
        group_5.shift(LEFT + 1.7*UP)
        text_9 = MTex(r"n=9").shift(1.5*UP)
        coordinate_9 = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        group_9 = VGroup(text_9)
        for coordinate in coordinate_9:
            position = 0.7*(coordinate[0]*UP + coordinate[1]*RIGHT)
            residue = (coordinate[0] + coordinate[1]*2)%9
            group_9.add(Square(side_length = 0.95*0.7, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1).shift(position))
        group_9.shift(3*RIGHT + 1.7*UP)
        text_13 = MTex(r"n=13").shift(2*UP)
        coordinate_13 = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1), (2, 0), (0, 2), (-2, 0), (0, -2)]
        group_13 = VGroup(text_13)
        for coordinate in coordinate_13:
            position = 0.6*(coordinate[0]*UP + coordinate[1]*RIGHT)
            residue = (coordinate[0] + coordinate[1]*2)%13
            group_13.add(Square(side_length = 0.95*0.6, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1).shift(position))
        group_13.shift(3.25*LEFT + 1.5*DOWN)
        text_17 = MTex(r"n=17").shift(2*UP)
        coordinate_17 = [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        group_17 = VGroup(text_17)
        for coordinate in coordinate_17:
            position = 0.6*(coordinate[0]*UP + coordinate[1]*RIGHT)
            residue = (coordinate[0] + coordinate[1]*2)%17
            group_17.add(Square(side_length = 0.95*0.6, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1).shift(position))
        group_17.shift(0.75*RIGHT + 1.5*DOWN)
        condition = MTex(r"\begin{cases}n\text{为奇数}\\n=a^2+b^2\end{cases}").shift(4.5*RIGHT+1.5*DOWN)

        self.play(LaggedStart(*[FadeIn(mob) for mob in [group_1, group_5, group_9, group_13, group_17]], lag_ratio = 0.5, run_time = 3))
        self.play(Write(condition))
        self.wait(3+0+2-5, 13+16+2) #事实上 这和高斯整数的素因数分解有关 （空闲） 所有4k+1型的素数
        self.wait(1, 8) #都可以用来编组
        self.wait(0, 21) #（空闲）

        self.clear().add(self.notice)
        picture_video = ImageMobject("picture_video.jpg", height = 2)
        text_video = Text("BV1kx411q7kK", font = "Times New Roman").scale(0.5).next_to(picture_video, UP)
        group_cover = Group(picture_video, text_video).shift(5*RIGHT)
        rectangle_video = Rectangle(height = 5.5, width = 5*16/9 + 0.5).shift(2*LEFT)
        self.play(FadeIn(picture_video), Write(text_video), ShowCreation(rectangle_video), self.change_notice())
        self.wait(1, 23) #三蓝一棕曾经做过一期有关的视频
        self.wait(2, 13) #大家如果有兴趣可以去看一看
        self.frames -= 120
        self.wait(4, 16) #到此共65+13秒
        self.play(FadeOut(rectangle_video), FadeOut(group_cover), self.change_notice())

class Chapter2_4(FrameScene):
    def construct(self):
        self.notices = [Notice("正确规律", "请记笔记"),
                        Notice("儿童地垫", "请　玩耍"),
                        Notice("正确规律", "请记笔记"),
                        Notice("下节预告", "请　期待")]
        self.notice = self.notices[0]

        self.frames += 30
        self.wait(0, 10) #而对应地
        offset_r = 0.5*UP
        scale_r = 7
        hexes = []
        for i in range(scale_r, -scale_r-1, -1):
            endpoints = max(i, 0)-scale_r, min(0, i)+scale_r
            for j in range(endpoints[0], endpoints[1]+1):
                position = 0.75*(i*unit(TAU/3) + j*RIGHT)
                distance = max(abs(i), abs(j), abs(i-j))
                if abs(position[0]) < 3.5 and abs(position[1]) < 3.3:
                    hex = RegularPolygon(start_angle = PI/2, stroke_width = 0, fill_color = BLUE, fill_opacity = clip((scale_r+1-distance)/scale_r, 0, 1)).set_width(0.75*0.95).shift(position + offset_r)
                    hex.position = (i, j)
                    hexes.append(hex)
        self.play(*[FadeIn(mob) for mob in hexes])
        self.wait(1, 9) #艾森斯坦整数也可以这么编组
        self.wait(0, 19) #（空闲）

        colors = [BLUE, GREEN, PURPLE_B]
        anims = []
        for hex in hexes:
            index = (hex.position[0]+hex.position[1])%3
            anims.append(hex.animate.set_opacity(1).set_color(colors[index]))
        self.play(*anims, self.change_notice())
        self.wait(1, 13) #我们既可以一个六边形一组
        self.frames -= 30
        self.wait(1)

        self.fade_out(run_time = 0.5)
        offset_r = 0.5*UP
        scale_r = 8
        hexes = []
        for i in range(scale_r, -scale_r-1, -1):
            endpoints = max(i, 0)-scale_r, min(0, i)+scale_r
            for j in range(endpoints[0], endpoints[1]+1):
                position = 0.7*(i*unit(TAU/3) + j*RIGHT)
                if abs(position[0]) < 3.6 and abs(position[1]) < 3.3:
                    if i%2:
                        index = -(j+i-1)%3
                    else:
                        index = ((j+i)%6)//2
                    hex = RegularPolygon(start_angle = PI/2, fill_color = colors[index], stroke_width = 0, fill_opacity = 1
                                         ).set_width(0.7*0.95).shift(position + offset_r)
                    hexes.append(hex)
        self.fade_in(*hexes, run_time = 0.5)
        self.wait(1, 10) #也可以四个六边形一组
        self.frames -= 60
        self.wait(2)

        self.fade_out(run_time = 0.5)
        offset_r = 0.5*UP
        scale_r = 9
        hexes = []
        for i in range(scale_r, -scale_r-1, -1):
            endpoints = max(i, 0)-scale_r, min(0, i)+scale_r
            for j in range(endpoints[0], endpoints[1]+1):
                position = 0.6*(i*unit(TAU/3) + j*RIGHT)
                if abs(position[0]) < 3.5 and abs(position[1]) < 3.3:
                    residue = (j-5*i)%21
                    if residue in [0, 1, 4, 5, 16, 17, 20]:
                        index = 0
                    elif residue in [2, 3, 6, 7, 8, 11, 12]:
                        index = 1
                    else:
                        index = 2
                    hex = RegularPolygon(start_angle = PI/2, fill_color = colors[index], stroke_width = 0, fill_opacity = 1
                                         ).set_width(0.6*0.95).shift(position + offset_r)
                    hexes.append(hex)
        self.fade_in(*hexes, run_time = 0.5)
        self.wait(1, 8) #还可以七个六边形一组
        self.frames -= 60
        self.wait(2)

        self.fade_out(run_time = 0.5)
        offset_r = 0.5*UP
        scale_r = 10
        hexes = []
        for i in range(scale_r, -scale_r-1, -1):
            endpoints = max(i, 0)-scale_r, min(0, i)+scale_r
            for j in range(endpoints[0], endpoints[1]+1):
                position = 0.5*(i*unit(TAU/3) + j*RIGHT)
                if abs(position[0]) < 3.6 and abs(position[1]) < 3.3:
                    residue = (j+16*i)%39
                    if residue in [0, 1, 6, 15, 16, 17, 18, 21, 22, 23, 24, 33, 38]:
                        index = 0
                    elif residue in [2, 3 ,4 ,5 ,8, 9, 10, 11, 20, 25, 26, 27, 32]:
                        index = 1
                    else:
                        index = 2
                    hex = RegularPolygon(start_angle = PI/2, fill_color = colors[index], stroke_width = 0, fill_opacity = 1
                                         ).set_width(0.5*0.95).shift(position + offset_r)
                    hexes.append(hex)
        self.fade_in(*hexes, run_time = 0.5)
        self.wait(1, 11) #或者十三个六边形一组
        self.frames -= 60
        self.wait(2)

        self.fade_out(run_time = 0.5)
        offset_r = 0.5*UP
        scale_r = 13
        hexes = []
        for i in range(scale_r, -scale_r-1, -1):
            endpoints = max(i, 0)-scale_r, min(0, i)+scale_r
            for j in range(endpoints[0], endpoints[1]+1):
                position = 0.4*(i*unit(TAU/3) + j*RIGHT)
                if abs(position[0]) < 3.5 and abs(position[1]) < 3.3:
                    type_i = i%4
                    if type_i == 2:
                        index = ((-j+1)%6//2 + i//4)%3
                    elif type_i == 3:
                        index = ((j+2)%12//4 + i//4 + 1)%3
                    else:
                        index = ((j+1)%12//4 + i//4)%3
                    hex = RegularPolygon(start_angle = PI/2, fill_color = colors[index], stroke_width = 0, fill_opacity = 1
                                         ).set_width(0.4*0.95).shift(position + offset_r)
                    hexes.append(hex)
        self.fade_in(*hexes, run_time = 0.5)
        self.wait(0, 27) #乃至十六个六边形一组
        self.wait(0, 22) #（空闲）
        self.frames -= 60
        self.wait(2)

        self.fade_out(change_notice = True)
        text_1 = MTex(r"n=1").shift(1.5*UP)
        square_1 = RegularPolygon(start_angle = PI/2, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1).set_width(0.9*0.95)
        group_1 = VGroup(square_1, text_1).shift(5*LEFT + 1.7*UP)
        text_4 = MTex(r"n=4").shift(1.5*UP)
        coordinate_4 = [(0, 0), (1, 0), (0, 1), (-1, -1)]
        group_4 = VGroup(text_4)
        for coordinate in coordinate_4:
            position = 0.7*(coordinate[0]*unit(TAU/3) + coordinate[1]*RIGHT)
            residue = (coordinate[0] + coordinate[1]*2)%5
            group_4.add(RegularPolygon(start_angle = PI/2, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1).set_width(0.7*0.95).shift(position))
        group_4.shift(LEFT + 1.7*UP)
        text_7 = MTex(r"n=7").shift(1.5*UP)
        coordinate_7 = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1)]
        group_7 = VGroup(text_7)
        for coordinate in coordinate_7:
            position = 0.7*(coordinate[0]*unit(TAU/3) + coordinate[1]*RIGHT)
            residue = (coordinate[0] + coordinate[1]*2)%9
            group_7.add(RegularPolygon(start_angle = PI/2, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1).set_width(0.7*0.95).shift(position))
        group_7.shift(3*RIGHT + 1.7*UP)
        text_13 = MTex(r"n=13").shift(2*UP)
        coordinate_13 = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1), (2, 1), (1, 2), (-1, 1), (-2, -1), (-1, -2), (1, -1)]
        group_13 = VGroup(text_13)
        for coordinate in coordinate_13:
            position = 0.6*(coordinate[0]*unit(TAU/3) + coordinate[1]*RIGHT)
            residue = (coordinate[0] + coordinate[1]*2)%13
            group_13.add(RegularPolygon(start_angle = PI/2, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1).set_width(0.6*0.95).shift(position))
        group_13.shift(3.25*LEFT + 1.5*DOWN)
        text_16 = MTex(r"n=16").shift(2*UP)
        coordinate_16 = [(0, 0), (1, 0), (1, 1), (0, 1), (-1, 0), (-1, -1), (0, -1), (2, 1), (1, 2), (-1, 1), (-2, -1), (-1, -2), (1, -1), (2, 0), (0, 2), (-2, -2)]
        group_16 = VGroup(text_16)
        for coordinate in coordinate_16:
            position = 0.6*(coordinate[0]*unit(TAU/3) + coordinate[1]*RIGHT)
            residue = (coordinate[0] + coordinate[1]*2)%16
            group_16.add(RegularPolygon(start_angle = PI/2, fill_color = BLUE_D, stroke_width = 0, fill_opacity = 1).set_width(0.6*0.95).shift(position))
        group_16.shift(0.75*RIGHT + 1.5*DOWN)
        condition_r = MTex(r"\begin{cases}n\equiv {}1\ (\bmod\ 3\,)\\n=a^2-ab+b^2\end{cases}").scale(0.9).shift(4.5*RIGHT+1.5*DOWN)
        self.play(LaggedStart(*[FadeIn(mob) for mob in [group_1, group_4, group_7, group_13, group_16]], lag_ratio = 0.5, run_time = 3))
        self.wait(2+2-4, 23+17) #而决定哪些数字可以用来编组的 就和艾森斯坦整数的素因数分解有关
        self.wait(0, 16) #（空闲）
        self.play(Write(condition_r))
        self.wait(1, 14) #比如 所有3k+1型的素数就属于此类
        self.wait(1, 5) #（空闲）

        eisenstein = MTexText(r"在$\mathbb{Z}[\omega]$上：", tex_to_color_map = {r"\mathbb{Z}[\omega]": GREEN}).next_to(3*RIGHT+UP, UP)
        self.play(*[FadeOut(mob, 0.75*UL, run_time = 0.5, rate_func = rush_into) for mob in [group_1, group_4, group_7, group_13, group_16]], 
                  condition_r.animate.shift(1.5*UL), self.change_notice())
        self.play(Write(eisenstein))
        self.wait(0, 23) #不知道大家有没有感到一丝奇怪
        gauss = MTexText(r"在$\mathbb{Z}[i]$上：", tex_to_color_map = {r"\mathbb{Z}[i]": GREEN}).next_to(3*LEFT+UP, UP)
        condition_l = MTex(r"\begin{cases}n\equiv {}1\ (\bmod\ 2\,)\\n=a^2+b^2\end{cases}").scale(0.9).shift(3*LEFT)
        self.play(Write(gauss), Write(condition_l))
        self.wait(0, 25) #为什么在把模运算推广到复数以后
        self.wait(1, 21) #选择反而变少了呢
        self.wait(0, 25) #（空闲）

        self.wait(1, 3) #事实上
        self.wait(4, 13) #高斯整数可不止不能七个正方形一组编组这么简单
        self.wait(2, 6) #它甚至没有七个剩余类的运算
        self.wait(0, 22) #（空闲）

        self.wait(2, 7) #我们到底应该怎么处理这些问题呢
        self.wait(2, 11) 
        self.fade_out(end = True)
        self.wait(2, 0) #到此共51+9秒
        
#################################################################### 

class Chapter3_0(FrameScene):

    def construct(self):

        text3 = Text("第三节 代数数论中的复数", font = 'simsun', t2c={"第三节": YELLOW, "代数数论": GREEN, "复数": BLUE})

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(FrameScene):
    def construct(self):
        self.notices = [Notice("抽象代数", "请　了解"),
                        Notice("代数数论", "请　了解")]
        self.notice = self.notices[0]
        
        texts = r"\mathbb{Z}[{i}]", r"=\{{a}+{b}{i}|{a}, {b}\in \mathbb{Z}\}"
        gauss = MTex(texts[0]+texts[1], 
                     tex_to_color_map = {r"\mathbb{Z}": RED, (r"{a}", r"{b}"): RED_E, r"{i}": BLUE}, 
                     isolate = texts).shift(3*LEFT+1.5*UP)
        part_gauss = [gauss.get_part_by_tex(text) for text in texts]
        offset_l = 3*LEFT+1.5*UP - part_gauss[0].get_center()
        part_gauss[0].save_state().move_to(3*LEFT+1.5*UP)
        part_gauss[1].save_state().align_to(part_gauss[0], RIGHT)
        shade_l = SurroundingRectangle(part_gauss[1], fill_color = BACK, fill_opacity = 1, stroke_width = 0)
        texts = r"\mathbb{Z}[\omega]", r"=\{{a}+{b}\omega|{a}, {b}\in \mathbb{Z}\}"
        eisenstein = MTex(texts[0]+texts[1], 
                     tex_to_color_map = {r"\mathbb{Z}": RED, (r"{a}", r"{b}"): RED_E, r"\omega": BLUE}, 
                     isolate = texts).shift(3*RIGHT+1.5*UP)
        part_eisenstein = [eisenstein.get_part_by_tex(text) for text in texts]
        offset_r = 3*RIGHT+1.5*UP - part_eisenstein[0].get_center()
        part_eisenstein[0].save_state().move_to(3*RIGHT+1.5*UP)
        part_eisenstein[1].save_state().align_to(part_eisenstein[0], RIGHT)
        shade_r = SurroundingRectangle(part_eisenstein[1], fill_color = BACK, fill_opacity = 1, stroke_width = 0)
        
        self.play(Write(self.notice), Write(part_gauss[0]), Write(part_eisenstein[0]))
        self.wait(2, 10) #高斯整数集和艾森斯坦整数集的符号
        self.wait(2, 15) #想必对于学过抽象代数的同学
        self.wait(1, 9) #已经很熟悉了
        self.wait(0, 21) #（空闲）

        polynomial_l = MTex(r"x^2+1=0", tex_to_color_map = {r"x": BLUE}).shift(3*LEFT)
        polynomial_r = MTex(r"x^2+x+1=0", tex_to_color_map = {r"x": BLUE}).shift(3*RIGHT)
        solution_l = MTex(r"i^2+1=0", tex_to_color_map = {r"i": BLUE}).shift(3*LEFT + DOWN)
        solution_r = MTex(r"\omega^2+\omega+1=0", tex_to_color_map = {r"\omega": BLUE}).shift(3*RIGHT + DOWN)
        self.play(Write(polynomial_l))
        self.wait(1, 17) #对于多项式x^2+1=0......
        self.play(Write(polynomial_r))
        self.wait(1, 24) #......和x^2+x+1=0
        self.play(TransformFromCopy(polynomial_l, solution_l), TransformFromCopy(polynomial_r, solution_r))
        self.wait(1, 2) #我们分别取出它们的根
        self.add(part_eisenstein[1], shade_r, part_eisenstein[0], part_gauss[1], shade_l, part_gauss[0]
                 ).play(*[mob.animate.restore() for mob in [part_gauss[0], part_gauss[1], part_eisenstein[0], part_eisenstein[1]]], 
                        shade_l.animate.shift(-offset_l), shade_r.animate.shift(-offset_r))
        self.remove(shade_r, shade_l).wait(0, 24) #和整数一起运算
        self.wait(1, 25) #就能分别得到这两个环
        self.wait(0, 19) #（空闲）

        self.wait(2, 24) #但抽象代数的内容只是浅尝辄止
        self.wait(2, 19) #真正系统研究这些内容的数学分支
        self.play(self.change_notice())
        self.wait(0, 14) #叫做代数数论
        self.wait(0, 24) #（空闲）

        self.wait(2, 7) #在代数数论研究的所有环中

        offset_l = 3.5*LEFT+0.5*UP
        scale_l = 4
        points_l = []
        for i in range(scale_l, -scale_l-1, -1):
            for j in range(-scale_l, scale_l+1):
                position = 0.75*(i*UP + j*RIGHT)
                distance = max(abs(i), abs(j))
                point = Dot(offset_l + position, color = BLUE, fill_opacity = clip((scale_l+1-distance)/scale_l, 0, 1))
                points_l.append(point)
        random.shuffle(points_l)
        group_l = VGroup(*points_l)

        offset_r = 3.5*RIGHT+0.5*UP
        scale_r = 6
        points_r = []
        for i in range(scale_r, -scale_r-1, -1):
            endpoints = max(i, 0)-scale_r, min(0, i)+scale_r
            for j in range(endpoints[0], endpoints[1]+1):
                position = 0.75*(i*unit(TAU/3) + j*RIGHT)
                distance = max(abs(i), abs(j), abs(i-j))
                if abs(position[0]) < 3.3 and abs(position[1]) < 3.5:
                    point = Dot(position + offset_r, color = BLUE, fill_opacity = clip((scale_r+1-distance)/scale_r, 0, 1))
                    points_r.append(point)
        random.shuffle(points_r)
        group_r = VGroup(*points_r)
        line = Line(3.8*UP, 2.8*DOWN)
        self.play(*[FadeOut(mob) for mob in [gauss, eisenstein, polynomial_l, polynomial_r, solution_l, solution_r]], ShowCreation(line))
        self.add(group_l, group_r, self.notice).play(FadeIn(group_l), FadeIn(group_r), lag_ratio = 0.1, run_time = 2)
        self.wait(2+2-3, 17+28) #这两个已经是最漂亮的了 它们在整个复平面上均匀地分布着
        self.wait(1, 20) #形成了有规律的格点
        self.wait(0, 17) #（空闲）

        self.fade_out(run_time = 0.5)
        offset = 0.5*UP
        ring_1 = MTex(r"\mathbb{Z}[\sqrt{-2}]", tex_to_color_map = {r"\mathbb{Z}": RED, r"\sqrt{-2}": BLUE}).next_to(3*UP+6*LEFT)
        points = []
        for i in range(-4, 5):
            for j in range(-7, 8):
                position = 0.75*(i*UP + j/np.sqrt(2)*RIGHT)
                distance = max(abs(position[0]), abs(position[1]))
                point = Dot(position + offset, radius = 0.08*clip(1-distance/3.2, 0, 1)**0.5, color = BLUE)
                points.append(point)
        self.fade_in(*points, ring_1, run_time = 0.5)
        self.wait(0, 10) #而一般的环
        self.wait(2, 7) #要不然分布得不够均匀
        self.frames -= 30
        self.wait(1)

        self.fade_out(run_time = 0.5)
        offset = 0.5*UP
        ring_2 = MTex(r"\mathbb{Z}[\sqrt{2}]", tex_to_color_map = {r"\mathbb{Z}": RED, r"\sqrt{2}": BLUE}).next_to(3*UP+6*LEFT)
        points = []
        for i in range(5):
            points_i = []
            for j in range(-7, 8):
                position = 0.75*(i/np.sqrt(2)*RIGHT + j*RIGHT)
                distance = max(abs(position[0]), abs(position[1]))
                point_0 = Dot(0.75*(i/np.sqrt(2)*RIGHT + j*RIGHT) + offset, radius = 0.08*clip(1-i/5, 0, 1)**0.5, color = BLUE)
                points_i.append(point_0)
                if i > 0:
                    point_1 = Dot(0.75*(-i/np.sqrt(2)*RIGHT + j*RIGHT) + offset, radius = 0.08*clip(1-i/5, 0, 1)**0.5, color = BLUE)
                    points_i.append(point_1)
            random.shuffle(points_i)
            points.extend(points_i)
        self.play(ShowIncreasingSubsets(VGroup(*points), rate_func = linear), FadeIn(ring_2), run_time = 2.5)
        self.wait(0, 17) #要不然全挤在实数轴上
        self.frames -= 60
        self.wait(1)
        self.wait(1, 25) #而最常见的情况

        self.fade_out()
        ring_3 = MTex(r"\mathbb{Z}[\zeta_5]", tex_to_color_map = {r"\mathbb{Z}": RED, r"\zeta_5": BLUE}).next_to(3*UP+6*LEFT)
        dot_0 = Dot(offset, radius = 0.1, color = BLUE)
        dots_1 = [Dot(offset+unit(i*TAU/10), color = BLUE) for i in range(10)]
        dots_2 = [dot.copy().scale(0.75).set_opacity(0.75).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_1]
        group_2 = VGroup(*dots_2)
        dots_3 = [dot.copy().scale(2/3).set_opacity(0.5).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_2]
        group_3 = VGroup(*dots_3)
        dots_4 = [dot.copy().scale(0.5).set_opacity(0.25).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_3]
        group_4 = VGroup(*dots_4)
        dots_5 = [dot.copy().scale(0.5).set_opacity(0.15).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_4]
        self.play(FadeIn(VGroup(*dots_1, dot_0, ring_3)))
        self.bring_to_back(group_2).play(FadeIn(group_2))
        self.bring_to_back(group_3).play(FadeIn(group_3))
        self.bring_to_back(group_4).play(FadeIn(group_4))
        self.bring_to_back(*dots_5).play(*[FadeIn(dot) for dot in dots_5])

class Patch3_2(FrameScene):
    def construct(self):
        self.notices = [Notice("代数数论", "请　了解"),
                        Notice("新手大坑", "请　避开")]
        self.notice = self.notices[0]

        offset = 0.5*UP
        ring_3 = MTex(r"\mathbb{Z}[\zeta_5]", tex_to_color_map = {r"\mathbb{Z}": RED, r"\zeta_5": BLUE}).next_to(3*UP+6*LEFT)
        dot_0 = Dot(offset, radius = 0.1, color = BLUE)
        dots_1 = [Dot(offset+unit(i*TAU/10), color = BLUE) for i in range(10)]
        dots_2 = [dot.copy().scale(0.75).set_opacity(0.75).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_1]
        dots_3 = [dot.copy().scale(2/3).set_opacity(0.5).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_2]
        dots_4 = [dot.copy().scale(0.5).set_opacity(0.25).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_3]
        dots_5 = [dot.copy().scale(0.5).set_opacity(0.15).shift(unit(i*TAU/10)) for i in range(10) for dot in dots_4]
        self.add(*dots_5, *dots_4, *dots_3, *dots_2, *dots_1, dot_0, ring_3, self.notice)
        self.fade_out(change_notice = True)

class Chapter3_2(FrameScene):
    def construct(self):
        self.notices = [Notice("新手大坑", "请　避开")]
        self.notice = self.notices[0]
        self.add(self.notice)
        self.frames += 13*30+24

        colors = [interpolate_color(BLUE_B, BLUE_D, i/4) for i in range(5)]
        rows_add = VGroup(VGroup(MTex(r"+").shift(1.8*UP + 5*LEFT), *[MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(1.8*UP + 4.2*LEFT + 0.8*i*RIGHT) for i in range(5)]), *[
            VGroup(MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(UP + 5*LEFT + 0.8*i*DOWN), *[MTex(r"\bar"+str((i+j)%5), color = colors[(i+j)%5]).scale(0.8).shift(UP + 4.2*LEFT + 0.8*i*DOWN + 0.8*j*RIGHT) for j in range(5)]) for i in range(5)])
        line_h_add = Line(1.4*UP + 5.4*LEFT, 1.4*UP + 0.6*LEFT)
        line_v_add = Line(2.2*UP + 4.6*LEFT, 2.6*DOWN + 4.6*LEFT)
        table_add = VGroup(rows_add, line_h_add, line_v_add).scale(5/8).move_to(4*LEFT+2.2*UP)
        rows_mul = VGroup(VGroup(MTex(r"\times").shift(1.8*UP + RIGHT), *[MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(1.8*UP + 1.8*RIGHT + 0.8*i*RIGHT) for i in range(5)]), *[
            VGroup(MTex(r"\bar"+str(i), color = colors[i]).scale(0.8).shift(UP + RIGHT + 0.8*i*DOWN), *[MTex(r"\bar"+str((i*j)%5), color = colors[(i*j)%5]).scale(0.8).shift(UP + 1.8*RIGHT + 0.8*i*DOWN + 0.8*j*RIGHT) for j in range(5)]) for i in range(5)])
        line_h_mul = Line(1.4*UP + 0.6*RIGHT, 1.4*UP + 5.4*RIGHT)
        line_v_mul = Line(2.2*UP + 1.4*RIGHT, 2.6*DOWN + 1.4*RIGHT)
        table_mul = VGroup(rows_mul, line_h_mul, line_v_mul).scale(5/8).move_to(4*LEFT+1.2*DOWN)
        example = MTex(r"1\equiv 6(\bmod\ 5\,)", tex_to_color_map = {(r"1", r"6"): colors[0], r"5": YELLOW}).scale(0.8).shift(2*UP + 2*RIGHT)
        self.fade_in(table_add, table_mul, example)
        self.wait(0, 19) #我们之前研究过模5的运算

        buff = 0.7
        offset = 0.2*DOWN + 0.8*LEFT
        class_0 = MTex(r"\bar{0}=\{\cdots, -5, 0, 5, 10, 15, \cdots\}", color = ratio_color(0, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.8).next_to(2*buff*UP + offset)
        class_1 = MTex(r"\bar{1}=\{\cdots, -4, 1, 6, 11, 16, \cdots\}", color = ratio_color(0.1, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.8).next_to(buff*UP + offset)
        class_2 = MTex(r"\bar{2}=\{\cdots, -3, 2, 7, 12, 17, \cdots\}", color = ratio_color(0.2, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.8).next_to(offset)
        class_3 = MTex(r"\bar{3}=\{\cdots, -2, 3, 8, 13, 18, \cdots\}", color = ratio_color(0.3, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.8).next_to(buff*DOWN + offset)
        class_4 = MTex(r"\bar{4}=\{\cdots, -1, 4, 9, 14, 19, \cdots\}", color = ratio_color(0.4, BLUE_B, BLUE_D), tex_to_color_map = {(r"=", r"\{", r",", r"\cdots", r"\}"): WHITE}).scale(0.8).next_to(2*buff*DOWN + offset)
        classes = [class_0, class_1, class_2, class_3, class_4]
        self.play(LaggedStart(*[Write(classes[i]) for i in range(5)], run_time = 2))
        self.wait(0, 3) #整数分成了5个剩余类
        self.wait(0, 20) #（空闲）

        extension = MTex(r"\mathbb{Z}\to \mathbb{Z}[i]", tex_to_color_map = {r"\mathbb{Z}": RED, r"i": colors[2]}).shift(3*UP)
        self.play(FadeIn(extension, 0.5*DOWN))
        self.wait(2, 1) #而当我们把整数扩张成高斯整数
        i = MTex(r"{i}\in", tex_to_color_map = {r"i": colors[2]}).scale(0.8).next_to(class_2, LEFT, buff = 0.15)
        self.play(Write(i))
        self.wait(1, 12) #再在上面做模运算的时候
        self.wait(2, 8) #虽然剩余类还是5个

        i_2 = MTex(r"2\equiv i\,(\bmod\ 2-i\,)", tex_to_color_map = {(r"2", r"i"): colors[2], r"2-i": TEAL}).scale(0.8).shift(2*UP + 2*RIGHT)
        example.submobjects = example.submobjects[::-1]
        self.play(Write(i_2, run_time = 2), ShowIncreasingSubsets(example, rate_func = lambda t: smooth(1-t), remover = True, run_time = 1.5))
        self.wait(1, 16) #但此时它已经悄悄变成了模2-i的运算
        self.wait(0, 29) #（空闲）
        self.wait(2, 21) #我们要是想在高斯整数里面模5

        self.fade_out(run_time = 0.5)
        texts = VGroup(*[Circle(radius = 0.3, fill_color = TEAL_B if abs(i)<=2 and abs(j)<=2 or abs(i)>2 and abs(j)>2 else BLUE_B, fill_opacity = 1, stroke_width = 0
                        ).add(MTex(r"\overline{"+str(i%5)+r"+"+str(j%5)+r"i}", color = BLACK).scale(0.4)
                        ).shift(0.75*(i*RIGHT + j*UP) + 0.5*UP) for i in range(-5, 6) for j in range(-4, 5)])
        self.fade_in(texts, run_time = 0.5)
        self.wait(1, 0) #就会得到25个剩余类
        self.wait(0, 24) #（空闲）

        definition = MTex(r"{a}&\equiv {b}\,(\bmod\ 5\,)\\\Leftrightarrow {a}-{b}&=5k,\,k\in \mathbb{Z}[{i}]",
                          tex_to_color_map = {(r"{a}", r"{b}"): BLUE, r"5": YELLOW, r"k": GREY, r"\mathbb{Z}": RED, r"{i}": TEAL}).scale(0.8).shift(4*RIGHT+0.5*UP)
        self.play(texts.animate.shift(2.5*LEFT))
        self.play(Write(definition))
        self.wait(0, 15) #模运算是在任何环上都能定义的运算
        self.wait(2, 18) #但在不同的环上模同一个数
        self.wait(2, 0) #得到的结果会很不一样
        self.wait(1, 0) #到此共46秒

class Chapter3_3(FrameScene):
    def construct(self):
        self.notices = [Notice("新手大坑", "请　避开"),
                        Notice("丑陋形式", "请勿模仿"),
                        Notice("清爽形式", "请　欣赏"),
                        Notice("新手大坑", "请　避开")]
        self.notice = self.notices[0]

        texts = VGroup(*[Circle(radius = 0.3, fill_color = TEAL_B if abs(i)<=2 and abs(j)<=2 or abs(i)>2 and abs(j)>2 else BLUE_B, fill_opacity = 1, stroke_width = 0
                        ).add(MTex(r"\overline{"+str(i%5)+r"+"+str(j%5)+r"i}", color = BLACK).scale(0.4)
                        ).shift(0.75*(i*RIGHT + j*UP) + 0.5*UP) for i in range(-5, 6) for j in range(-4, 5)]).shift(2.5*LEFT)
        definition = MTex(r"{a}&\equiv {b}\,(\bmod\ 5\,)\\\Leftrightarrow {a}-{b}&=5k,\,k\in \mathbb{Z}[{i}]",
                          tex_to_color_map = {(r"{a}", r"{b}"): BLUE, r"5": YELLOW, r"k": GREY, r"\mathbb{Z}": RED, r"{i}": TEAL}).scale(0.8).shift(4*RIGHT+0.5*UP)
        self.add(self.notice, texts, definition)
        self.wait(2, 1) #那要是不管其它元素了

        polynomial = MTex(r"x^5-x-1=0", tex_to_color_map = {r"x": BLUE}).next_to(3*UP + 5*LEFT)
        r_axis = Line(3.4*LEFT+0.5*UP, 3.4*RIGHT+0.5*UP).add(*[Line(i*RIGHT+0.4*UP, i*RIGHT+0.6*UP) for i in [-2, 2]])
        i_axis = Line(3.9*UP, 2.9*DOWN).add(*[Line((i+0.5)*UP+0.1*LEFT, (i+0.5)*UP+0.1*RIGHT) for i in [-2, 2]])
        self.fade_out(run_time = 0.5).fade_in(polynomial, r_axis, i_axis, run_time = 0.5)
        positions = [2*np.array([1.1673, 0, 0]), 2*np.array([0.181232, 1.08395, 0]), 2*np.array([-0.764884, 0.352472, 0]), 2*np.array([-0.764884, -0.352472, 0]), 2*np.array([0.181232, -1.08395, 0])]
        colors = [BLUE, interpolate_color(BLUE, GREEN, 0.2), interpolate_color(BLUE, YELLOW, 0.2), interpolate_color(BLUE, RED, 0.2), interpolate_color(BLUE, PURPLE, 0.2)]
        points = [Dot(positions[i]+0.5*UP, color = colors[i]) for i in range(5)]
        solutions = [MTex(r"1.1673", color = colors[0]).scale(0.6).shift(1.2*positions[0] + 0.5*UP + 0.3*UP), 
                     MTex(r"0.1812 + 1.0840i", color = colors[1]).scale(0.6).shift(1.2*positions[1] + 0.5*UP + 1*RIGHT + 0.1*DOWN), 
                     MTex(r"-0.7649 + 0.3525i", color = colors[2]).scale(0.6).shift(1.2*positions[2] + 0.5*UP + 0.2*UP), 
                     MTex(r"-0.7649 - 0.3525i", color = colors[3]).scale(0.6).shift(1.2*positions[3] + 0.5*UP + 0.2*DOWN), 
                     MTex(r"0.1812 - 1.0840i", color = colors[4]).scale(0.6).shift(1.2*positions[4] + 0.5*UP + 1*RIGHT + 0.1*UP)]
        self.play(*[ShowCreation(point) for point in points], *[Write(solution, run_time = 2) for solution in solutions])
        self.wait(0, 1) #就只研究多项式的根
        self.wait(1, 0) #又怎么样呢
        self.wait(0, 23) #（空闲）

        self.play(*[FadeOut(mob) for mob in [polynomial] + points + solutions], run_time = 0.5)
        polynomial = MTex(r"x^3-x-1=0", tex_to_color_map = {r"x": BLUE}).next_to(3*UP + 5*LEFT)
        component_1 = np.cbrt((1+np.sqrt(23/27))/2)
        component_2 = np.cbrt((1-np.sqrt(23/27))/2)
        positions = [2*(component_1*unit(0)+component_2*unit(0)), 2*(component_1*unit(TAU/3)+component_2*unit(-TAU/3)), 2*(component_1*unit(-TAU/3)+component_2*unit(TAU/3))]
        colors = [BLUE, interpolate_color(BLUE, YELLOW, 0.2), interpolate_color(BLUE, RED, 0.2)]
        points = [Dot(positions[i]+0.5*UP, color = colors[i]) for i in range(3)]
        solutions = [MTex(r"1.3247", color = colors[0]).scale(0.6).shift(1.2*positions[0] + 0.5*UP + 0.3*UP), 
                     MTex(r"-0.6624 + 0.5623 i", color = colors[1]).scale(0.6).shift(1.2*positions[1] + 0.5*UP + 0.2*UP), 
                     MTex(r"-0.6624 - 0.5623 i", color = colors[2]).scale(0.6).shift(1.2*positions[2] + 0.5*UP + 0.2*DOWN)]
        self.play(*[FadeIn(mob) for mob in [polynomial] + points + solutions], run_time = 0.5)
        self.wait(1, 15) #其实大多数情况也不怎么样

        exact_forms = [MTex(r"\sqrt[3]{\frac{1+\sqrt{\frac{23}{27}}}{2}}+\sqrt[3]{\frac{1-\sqrt{\frac{23}{27}}}{2}}", color = colors[0]).scale(0.5).shift(positions[0] + 0.5*UP + 0.7*DOWN), 
                       MTex(r"\omega\sqrt[3]{\frac{1+\sqrt{\frac{23}{27}}}{2}}+\omega^2\sqrt[3]{\frac{1-\sqrt{\frac{23}{27}}}{2}}", color = colors[1]).scale(0.5).shift(1.2*positions[1] + 0.5*UP + 1.7*LEFT + 0.5*DOWN),
                       MTex(r"\omega^2\sqrt[3]{\frac{1+\sqrt{\frac{23}{27}}}{2}}+\omega\sqrt[3]{\frac{1-\sqrt{\frac{23}{27}}}{2}}", color = colors[2]).scale(0.5).shift(1.2*positions[2] + 0.5*UP + 1.7*LEFT + 0.5*UP)]
        self.play(*[Write(mob) for mob in exact_forms], self.change_notice())
        self.wait(2+2-3, 27+27) #高次方程求根还不如求数值解 而数值解除了告诉你这里有个根以外
        self.wait(1, 11) #一般也没什么用
        self.wait(0, 22) #（空闲）

        self.wait(2, 5) #但有一种情况是例外
        self.play(*[FadeOut(mob) for mob in [polynomial] + points + solutions + exact_forms], run_time = 0.5)
        polynomial = MTex(r"x^5-1=0", tex_to_color_map = {r"x": BLUE}).next_to(3*UP + 5*LEFT)
        positions = [2*unit(i*TAU/5) for i in range(5)]
        colors = [BLUE, interpolate_color(BLUE, GREEN, 0.2), interpolate_color(BLUE, YELLOW, 0.2), interpolate_color(BLUE, RED, 0.2), interpolate_color(BLUE, PURPLE, 0.2)]
        points = [Dot(positions[i]+0.5*UP, color = colors[i]) for i in range(5)]
        self.play(*[FadeIn(mob) for mob in [polynomial] + points], run_time = 0.5)
        self.play(self.change_notice())
        self.wait(0, 3) #我们如果要求单位根
        self.wait(2, 5) #那还是可以写出它们的简便形式的
        self.wait(0, 26) #（空闲）

        solutions = [MTex(r"\zeta_0=1", color = colors[0]).scale(0.6).shift(positions[0] + 0.5*UP + 0.3*DOWN), 
                     MTex(r"\zeta_1=e^{\frac{2i\pi}{5}}", color = colors[1]).scale(0.6).shift(positions[1] + 0.5*UP + 0.3*UP + 0.1*RIGHT), 
                     MTex(r"\zeta_2=e^{\frac{4i\pi}{5}}", color = colors[2]).scale(0.6).shift(positions[2] + 0.5*UP + 0.3*UP), 
                     MTex(r"\zeta_3=e^{\frac{6i\pi}{5}}", color = colors[3]).scale(0.6).shift(positions[3] + 0.5*UP + 0.3*DOWN), 
                     MTex(r"\zeta_4=e^{\frac{8i\pi}{5}}", color = colors[4]).scale(0.6).shift(positions[4] + 0.5*UP + 0.3*DOWN + 0.1*RIGHT)]
        self.play(*[Write(mob) for mob in solutions])
        self.wait(1, 28) #一种常见的形式是使用欧拉公式
        self.wait(1, 16) #而更大胆一点
        ambitious = MTex(r"\sqrt[5]{1}", color = BLUE).shift(0.5*UR + 0.5*UP)
        arrows = [Arrow(ambitious, points[i], color = colors[i]) for i in range(5)]
        self.play(Write(ambitious))
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in arrows]), frames = 61) #我们甚至可以直接写成给1开根号的形式
        self.wait(0, 25) #（空闲）

        self.play(self.change_notice())
        self.wait(1, 27) #但有这些表示并不意味着这都是好事
        self.wait(0, 20) #（空闲）
        self.wait(2, 28) #它们在复分析里是完全正确的
        self.wait(3, 28) #但在代数里 可能存在那么一点“小”问题
        self.wait(0, 28) #（空闲）
        self.wait(3, 22) #多项式的次数 是代数数论里十分关键的概念
        self.wait(0, 17) #（空闲）

        self.fade_out(run_time = 0.5)
        axes = VGroup(Line(2*LEFT, 2*RIGHT), Line(1.5*LEFT+0.1*UP, 1.5*LEFT+0.1*DOWN), Line(1.5*RIGHT+0.1*UP, 1.5*RIGHT+0.1*DOWN),
                              Line(2*UP, 2*DOWN), Line(1.5*UP+0.1*LEFT, 1.5*UP+0.1*RIGHT), Line(1.5*DOWN+0.1*LEFT, 1.5*DOWN+0.1*RIGHT))
        axes_l = axes.copy().shift(3*LEFT+0.25*DOWN)
        axes_r = axes.copy().shift(3*RIGHT+0.25*DOWN)
        function_l = MTex(r"i^2+1=0", tex_to_color_map = {r"i": BLUE}).shift(3*LEFT+3.25*UP)
        function_r = MTex(r"\omega^2+\omega+1=0", tex_to_color_map = {r"\omega": BLUE}).shift(3*RIGHT+3.25*UP)
        points_l = [Dot(3*LEFT+1.5*UP+0.25*DOWN, color = BLUE), Dot(3*LEFT+1.5*DOWN+0.25*DOWN, color = BLUE)]
        points_r = [Dot(3*RIGHT+1.5*unit(TAU/3)+0.25*DOWN, color = BLUE), Dot(3*RIGHT+1.5*unit(-TAU/3)+0.25*DOWN, color = BLUE)]
        self.fade_in(axes_l, axes_r, run_time = 0.5)
        self.play(Write(function_l), ShowCreation(points_l[0]), ShowCreation(points_l[1]))
        self.wait(2, 2) #比如 i是方程x^2+1=0的根
        self.play(Write(function_r), ShowCreation(points_r[0]), ShowCreation(points_r[1]))
        self.wait(3, 10) #而ω是方程x^2+x+1=0的根

        reminder = MTexText(r"*于是$i$与$\omega$都是二次代数数").scale(0.4).shift(UP)
        self.play(FadeIn(reminder))
        self.wait(1, 18) #这两个方程都是二次的
        self.wait(1, 29) #但要是去求单位根的话
        unit_l = MTex(r"x^4-1=0", tex_to_color_map = {r"x": TEAL}).shift(3*LEFT+2.5*UP)
        unit_r = MTex(r"x^3-1=0", tex_to_color_map = {r"x": TEAL}).shift(3*RIGHT+2.5*UP)
        root_l = [Dot(3*LEFT+0.25*DOWN+1.5*LEFT, color = TEAL), Dot(3*LEFT+0.25*DOWN+1.5*RIGHT, color = TEAL)]
        root_r = Dot(3*RIGHT+0.25*DOWN+1.5*RIGHT, color = TEAL)
        self.play(Write(unit_l), ShowCreation(root_l[0]), ShowCreation(root_l[1]))
        self.wait(0, 29) #i会是四次单位根
        self.play(Write(unit_r), ShowCreation(root_r))
        self.wait(1, 3) #而ω会是三次单位根
        self.wait(0, 25) #（空闲）
        self.wait(2, 10) #这是非常具有迷惑性的名字
        reminder_2 = MTexText(r"*除了一次单位根$x=1$，\\它真的是一次代数数").scale(0.4).shift(DOWN)
        self.play(FadeIn(reminder_2))
        self.wait(3, 3) #某种意义上 所有的单位根全都名不副实
        self.wait(3, 14) #它们真正的次数一定严格小于名字里写的次数
        self.wait(0, 21) #到此共76秒
        
class Chapter3_4(FrameScene):
    def construct(self):
        self.notices = [Notice("新手大坑", "请　避开")]
        self.notice = self.notices[0]

        axes = VGroup(Line(2*LEFT, 2*RIGHT), Line(1.5*LEFT+0.1*UP, 1.5*LEFT+0.1*DOWN), Line(1.5*RIGHT+0.1*UP, 1.5*RIGHT+0.1*DOWN),
                              Line(2*UP, 2*DOWN), Line(1.5*UP+0.1*LEFT, 1.5*UP+0.1*RIGHT), Line(1.5*DOWN+0.1*LEFT, 1.5*DOWN+0.1*RIGHT))
        axes_l = axes.copy().shift(3*LEFT+0.25*DOWN)
        axes_r = axes.copy().shift(3*RIGHT+0.25*DOWN)
        function_l = MTex(r"i^2+1=0", tex_to_color_map = {r"i": BLUE}).shift(3*LEFT+3.25*UP)
        function_r = MTex(r"\omega^2+\omega+1=0", tex_to_color_map = {r"\omega": BLUE}).shift(3*RIGHT+3.25*UP)
        unit_l = MTex(r"x^4-1=0", tex_to_color_map = {r"x": TEAL}).shift(3*LEFT+2.5*UP)
        unit_r = MTex(r"x^3-1=0", tex_to_color_map = {r"x": TEAL}).shift(3*RIGHT+2.5*UP)
        points_l = [Dot(3*LEFT+0.25*DOWN+1.5*RIGHT, color = TEAL), Dot(3*LEFT+1.5*UP+0.25*DOWN, color = BLUE), Dot(3*LEFT+0.25*DOWN+1.5*LEFT, color = TEAL), Dot(3*LEFT+1.5*DOWN+0.25*DOWN, color = BLUE)]
        points_r = [Dot(3*RIGHT+0.25*DOWN+1.5*RIGHT, color = TEAL), Dot(3*RIGHT+1.5*unit(TAU/3)+0.25*DOWN, color = BLUE), Dot(3*RIGHT+1.5*unit(-TAU/3)+0.25*DOWN, color = BLUE)]
        reminder = MTexText(r"*于是$i$与$\omega$都是二次代数数").scale(0.4).shift(UP)
        reminder_2 = MTexText(r"*除了一次单位根$x=1$，\\它真的是一次代数数").scale(0.4).shift(DOWN)
        self.add(self.notice, axes_l, axes_r, function_l, function_r, unit_l, unit_r, *points_l, *points_r, reminder, reminder_2)
        self.fade_out(run_time = 0.5)

        polynomial = MTex(r"x^5-1=0", tex_to_color_map = {r"x": BLUE}).shift(3*UP + 5*LEFT)
        positions = [1.5*unit(i*TAU/5) + 5*LEFT for i in range(5)]
        colors = [BLUE, interpolate_color(BLUE, GREEN, 0.2), interpolate_color(BLUE, YELLOW, 0.2), interpolate_color(BLUE, RED, 0.2), interpolate_color(BLUE, PURPLE, 0.2)]
        points = [Dot(positions[i], color = colors[i]) for i in range(5)]
        solutions = [MTex(r"\zeta_0=1", color = colors[0]).scale(0.6).shift(positions[0] + 0.3*DOWN), 
                     MTex(r"\zeta_1=e^{\frac{2i\pi}{5}}", color = colors[1]).scale(0.5).shift(positions[1] + 0.3*UP + 0.2*RIGHT), 
                     MTex(r"\zeta_2=e^{\frac{4i\pi}{5}}", color = colors[2]).scale(0.5).shift(positions[2] + 0.3*UP), 
                     MTex(r"\zeta_3=e^{\frac{6i\pi}{5}}", color = colors[3]).scale(0.5).shift(positions[3] + 0.3*DOWN), 
                     MTex(r"\zeta_4=e^{\frac{8i\pi}{5}}", color = colors[4]).scale(0.5).shift(positions[4] + 0.3*DOWN + 0.2*RIGHT)]
        self.fade_in(polynomial, axes.shift(5*LEFT), *points, *solutions, run_time = 0.5)
        self.wait(3, 16) #而且 虽然我们可以把这些单位根在复平面上画出来
        self.wait(1, 23) #但在代数的背景中
        self.wait(2, 8) #它们完全没必要嵌入到复数中
        self.wait(0, 22) #（空闲）

        texts = [r"({1}+\zeta_0)({1}+\zeta_1)({1}+\zeta_2)({1}+\zeta_3)({1}+\zeta_4)", r"({1})+(\zeta_0+\zeta_1+\zeta_2+\zeta_3+\zeta_4)", 
                 r"+(\zeta_0\zeta_1+\zeta_0\zeta_2+\zeta_0\zeta_3+\zeta_0\zeta_4+\zeta_1\zeta_2+\zeta_1\zeta_3+\zeta_1\zeta_4+\zeta_2\zeta_3+\zeta_2\zeta_4+\zeta_3\zeta_4)",
                 r"+(\zeta_0\zeta_1\zeta_2+\zeta_0\zeta_1\zeta_3+\zeta_0\zeta_1\zeta_4+\zeta_0\zeta_2\zeta_3+\zeta_0\zeta_2\zeta_4+\zeta_0\zeta_3\zeta_4+\zeta_1\zeta_2\zeta_3+\zeta_1\zeta_2\zeta_4+\zeta_1\zeta_3\zeta_4+\zeta_2\zeta_3\zeta_4)",
                 r"+(\zeta_0\zeta_1\zeta_2\zeta_3+\zeta_0\zeta_1\zeta_2\zeta_4+\zeta_0\zeta_1\zeta_3\zeta_4+\zeta_0\zeta_2\zeta_3\zeta_4+\zeta_1\zeta_2\zeta_3\zeta_4)+(\zeta_0\zeta_1\zeta_2\zeta_3\zeta_4)",
                 r"{1}+0+0+0+0+{1}",r"{2}"]
        calculate_1 = MTex(r"&"+texts[0]+r"\\=&\,"+texts[1]+r"\\&"+texts[2]+r"\\&"+texts[3]+r"\\&"+texts[4]+r"\\=&"+texts[5]+r"\\=&"+texts[6], isolate = [r"="]+texts, tex_to_color_map = {**{r"\zeta_"+str(i): colors[i] for i in range(5)}, r"{1}": YELLOW}).scale(0.5).next_to(1.5*RIGHT + 3*UP, DOWN, buff = 0)
        texts = [r"({1}+e^0)({1}+e^{\frac{2i\pi}{5}})({1}+e^{\frac{4i\pi}{5}})({1}+e^{\frac{6i\pi}{5}})({1}+e^{\frac{8i\pi}{5}})", r"({1})+(e^0+e^{\frac{2i\pi}{5}}+e^{\frac{4i\pi}{5}}+e^{\frac{6i\pi}{5}}+e^{\frac{8i\pi}{5}})", 
                 r"+(e^{\frac{2i\pi}{5}}+e^{\frac{4i\pi}{5}}+e^{\frac{6i\pi}{5}}+e^{\frac{8i\pi}{5}}+e^{\frac{6i\pi}{5}}+e^{\frac{8i\pi}{5}}+e^0+e^0+e^{\frac{2i\pi}{5}}+e^{\frac{4i\pi}{5}})",
                 r"+(e^{\frac{6i\pi}{5}}+e^{\frac{8i\pi}{5}}+e^0+e^0+e^{\frac{2i\pi}{5}}+e^{\frac{4i\pi}{5}}+e^{\frac{2i\pi}{5}}+e^{\frac{4i\pi}{5}}+e^{\frac{6i\pi}{5}}+e^{\frac{8i\pi}{5}})",
                 r"+(e^{\frac{2i\pi}{5}}+e^{\frac{4i\pi}{5}}+e^{\frac{6i\pi}{5}}+e^{\frac{8i\pi}{5}}+e^0)+(e^0)",
                 r"{1}+0+0+0+0+{1}",r"{2}"]
        calculate_2 = MTex(r"&"+texts[0]+r"\\=&\,"+texts[1]+r"\\&"+texts[2]+r"\\&"+texts[3]+r"\\&"+texts[4]+r"\\=&"+texts[5]+r"\\=&"+texts[6], isolate = [r"="]+texts, tex_to_color_map = {**{r"e^{\frac{"+str(2*i)+r"i\pi}{5}}": colors[i] for i in range(1, 5)}, r"e^0": BLUE, r"{1}": YELLOW}).scale(0.5).next_to(1.5*RIGHT + 0.5*UP, DOWN, buff = 0)
        self.play(Write(calculate_1, run_time = 4))
        self.wait(2+2-4, 7+12) #即使我们想算什么东西 那么凭借这个多项式也就足够了
        self.wait(0, 23) #（空闲）

        self.play(Write(calculate_2, run_time = 4))
        self.wait(0, 3) #当然 我们可以把单位根写成e的复指数的形式
        self.wait(2, 5) #然后再展开求解
        self.wait(3, 17) #但这种过程其实和直接展开也没什么区别
        self.wait(1, 18) #计算过程一模一样
        self.wait(0, 19) #（空闲）
        self.wait(3, 22) #毕竟 应该不会有人想代入三角函数的形式
        self.wait(1, 14) #再把它展开计算吧
        self.wait(2, 1)
        self.fade_out(end = True)
        self.wait(2, 0) #到此共37秒

#################################################################### 

class Summary(FrameScene):

    def construct(self):
        self.notices = [Notice("良心视频", "请　三连"), 
                        Notice("下期预告", "敬请期待"), 
                        Notice("良心up主", "请　关注")]
        self.notice = self.notices[0]

        self.play(Write(self.notice))
        self.wait(1, 1) #非常感谢大家能看到这里
        self.wait(0, 15) #（空闲）

        self.wait(2, 27) #说实话 这期视频的难度很高
        self.wait(0, 14) #（空闲）

        LIME = "#BFFF00"
        Integer = MTex(r"\mathbb{Z}", color = BLUE).shift(5*LEFT)
        Rational = MTex(r"\mathbb{Q}", color = GREEN).shift(2*LEFT + 2*DOWN)
        Real = MTex(r"\mathbb{R}", color = LIME).shift(2*RIGHT + 2*DOWN)
        Complex = MTex(r"\mathbb{C}", color = YELLOW).shift(5*RIGHT)
        arrow_zq = Arrow(Integer, Rational, color = interpolate_color(BLUE, GREEN, 0.5))
        arrow_qr = Arrow(Rational, Real, color = interpolate_color(GREEN, LIME, 0.5))
        arrow_rc = Arrow(Real, Complex, color = interpolate_color(LIME, YELLOW, 0.5))
        self.play(Write(Integer))
        self.wait(0, 16) #从整数开始
        self.wait(0, 15)
        kwargs_1 = {r"run_time": 0.7, r"rate_func": part_rate(smooth, 0, 0.8)}
        kwargs_2 = {r"run_time": 0.3, r"rate_func": rush_from}
        self.play(GrowArrow(arrow_zq), **kwargs_1)
        self.play(GrowFromCenter(Rational), **kwargs_2)
        self.play(GrowArrow(arrow_qr), **kwargs_1)
        self.play(GrowFromCenter(Real), **kwargs_2)
        self.play(GrowArrow(arrow_rc), **kwargs_1)
        self.play(GrowFromCenter(Complex), **kwargs_2)
        self.wait(0, 26) #我们在课堂上逐渐认识了有理数 实数 和复数
        self.wait(0, 21) #（空闲）
        self.wait(2, 9) #这是一条相当自然的学习路径
        self.wait(2, 18) #新的性质总是伴随着新的数出现
        self.wait(0, 23) #（空闲）

        az_1 = MTex(r"\mathbb{Z}[\sqrt{2}]", tex_to_color_map = {r"\mathbb{Z}": BLUE, r"\sqrt{2}": RED}).shift(3*LEFT+0.5*UP)
        az_2 = MTex(r"\mathbb{Z}[\omega]", tex_to_color_map = {r"\mathbb{Z}": BLUE, r"\omega": RED}).shift(3*LEFT+1.5*UP)
        az_3 = MTex(r"\mathbb{Z}[\zeta_5]", tex_to_color_map = {r"\mathbb{Z}": BLUE, r"\zeta_5": RED}).shift(3*LEFT+2.5*UP)
        arrow_z1 = Arrow(Integer, az_1.get_corner(LEFT), color = BLUE)
        arrow_z2 = Arrow(Integer, az_2.get_corner(LEFT), color = BLUE)
        arrow_z3 = Arrow(Integer, az_3.get_corner(LEFT), color = BLUE)
        aq_1 = MTex(r"\mathbb{Q}(\sqrt{2})", tex_to_color_map = {r"\mathbb{Q}": GREEN, r"\sqrt{2}": RED}).shift(0.75*DOWN)
        aq_2 = MTex(r"\mathbb{Q}(\omega)", tex_to_color_map = {r"\mathbb{Q}": GREEN, r"\omega": RED}).shift(0.25*UP)
        aq_3 = MTex(r"\mathbb{Q}(\zeta_5)", tex_to_color_map = {r"\mathbb{Q}": GREEN, r"\zeta_5": RED}).shift(1.25*UP)
        arrow_q1 = Arrow(az_1.get_corner(RIGHT), aq_1.get_corner(LEFT), color = interpolate_color(BLUE, GREEN, 0.5))
        arrow_q2 = Arrow(az_2.get_corner(RIGHT), aq_2.get_corner(LEFT), color = interpolate_color(BLUE, GREEN, 0.5))
        arrow_q3 = Arrow(az_3.get_corner(RIGHT), aq_3.get_corner(LEFT), color = interpolate_color(BLUE, GREEN, 0.5))
        arrow_q4 = Arrow(Rational, aq_1.get_corner(LEFT), color = GREEN)
        arrow_q5 = Arrow(Rational, aq_2.get_corner(LEFT), color = GREEN)
        arrow_q6 = Arrow(Rational, aq_3.get_corner(LEFT), color = GREEN)
        Algebraic = MTex(r"\bar{\mathbb{A}}", color = PURPLE_A).shift(3*UP)
        arrow_a1 = Arrow(az_1.get_corner(RIGHT), Algebraic, color = RED)
        arrow_a2 = Arrow(az_2.get_corner(RIGHT), Algebraic, color = RED)
        arrow_a3 = Arrow(az_3.get_corner(RIGHT), Algebraic, color = RED)
        Algebra = MTex(r"\mathbb{A}", color = RED).shift(1.5*UP + 2.5*RIGHT)
        arrow_aa = Arrow(Algebraic, Algebra, color = interpolate_color(PURPLE, RED, 0.5))
        qrrow_a1 = Arrow(aq_1.get_corner(RIGHT), Algebra, color = RED)
        qrrow_a2 = Arrow(aq_2.get_corner(RIGHT), Algebra, color = RED)
        qrrow_a3 = Arrow(aq_3.get_corner(RIGHT), Algebra, color = RED)
        qrrow_r1 = Arrow(aq_1.get_corner(RIGHT), Real, color = interpolate_color(GREEN, LIME, 0.5))
        arrow_ac = Arrow(Algebra, Complex, color = interpolate_color(RED, YELLOW, 0.5))
        self.play(LaggedStart(AnimationGroup(GrowArrow(arrow_z1, **kwargs_1), GrowFromCenter(az_1, **kwargs_2), lag_ratio = 1), 
                              AnimationGroup(GrowArrow(arrow_z2, **kwargs_1), GrowFromCenter(az_2, **kwargs_2), lag_ratio = 1), 
                               AnimationGroup(GrowArrow(arrow_z3, **kwargs_1), GrowFromCenter(az_3, **kwargs_2), lag_ratio = 1), lag_ratio = 0.25, run_time = 1.5))
        self.play(LaggedStart(GrowArrow(arrow_a1, **kwargs_1), GrowArrow(arrow_a2, **kwargs_1), GrowArrow(arrow_a3, **kwargs_1), lag_ratio = 0.25/0.7, run_time = 1.2))
        self.play(GrowFromCenter(Algebraic, **kwargs_2))
        self.play(LaggedStart(AnimationGroup(AnimationGroup(GrowArrow(arrow_q1, **kwargs_1), GrowArrow(arrow_q4, **kwargs_1)), GrowFromCenter(aq_1, **kwargs_2), lag_ratio = 1), 
                              AnimationGroup(AnimationGroup(GrowArrow(arrow_q2, **kwargs_1), GrowArrow(arrow_q5, **kwargs_1)), GrowFromCenter(aq_2, **kwargs_2), lag_ratio = 1), 
                              AnimationGroup(AnimationGroup(GrowArrow(arrow_q3, **kwargs_1), GrowArrow(arrow_q6, **kwargs_1)), GrowFromCenter(aq_3, **kwargs_2), lag_ratio = 1), lag_ratio = 0.25, run_time = 1.5))
        self.play(GrowArrow(arrow_aa, **kwargs_1))
        self.play(GrowFromCenter(Algebra, **kwargs_2))
        self.play(LaggedStart(GrowArrow(qrrow_a1, **kwargs_1), GrowArrow(qrrow_a2, **kwargs_1), AnimationGroup(GrowArrow(qrrow_a3, **kwargs_1), GrowArrow(qrrow_r1, **kwargs_1)), lag_ratio = 0.25/0.7, run_time = 1.2))
        self.play(GrowArrow(arrow_ac, run_time = 0.8, rate_func = part_rate(smooth, 0.2, 1)))
        self.wait(2+1+0+2+2-7, 16+23+13+13+17-15) #而从整数扩张到代数整数 却是一条完全不同的路 （空闲） 想要研究代数整数的新性质 就必须得把它们从复数中剥离出来
        self.wait(0, 15) #（空闲）
        self.wait(1, 13) #而理解这一切
        self.wait(2, 13) #至少也需要不错的初等数论基础
        self.wait(0, 21) #（空闲）
        self.wait(2, 1) #希望我这期视频里的动画
        self.wait(2, 0) #多少可以为此提供一些帮助
        self.wait(0, 21) #（空闲）

        self.clear().add(self.notice)
        like = Text("", font = 'vanfont').scale(2).shift(3*LEFT)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').scale(2).shift(3*RIGHT)
        sanlian = VGroup(like, coin, star)
        self.play(*[GrowFromCenter(mob) for mob in sanlian])
        self.play(ApplyMethod(sanlian.set_color, "#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian])
        self.wait(1, 17) #如果这期视频成为了你开启代数数论大门的钥匙
        self.wait(1, 29) #不妨一键三连支持一下
        self.wait(0, 26) #（空闲）

        self.play(FadeOut(sanlian), self.change_notice())
        self.wait(1, 26) #下期视频我打算讲一讲挂谷问题

        offset_1 = 4*RIGHT
        offset_3 = 4*LEFT
        scale_factor = 1.8
        line_1 = Line(scale_factor*UP, scale_factor*DOWN, color = RED).shift(offset_1)
        line_2 = Line(scale_factor*UP, scale_factor*DOWN, color = RED)
        line_3 = Line(scale_factor*UP, scale_factor*DOWN, color = RED).shift(offset_3)
        line_1.counter = 0
        line_2.counter = 0
        line_3.counter = 0
        self.play(*[ShowCreation(mob)for mob in [line_1, line_2, line_3]])

        alpha = ValueTracker(0.0)
        def line_1_updater(mob: Line):
            angle = alpha.get_value()
            mob.put_start_and_end_on(scale_factor*unit(angle+PI/2), scale_factor*unit(angle-PI/2)).shift(offset_1)
            critical = mob.counter*TAU/90
            while angle >= critical:
                self.bring_to_back(Line(scale_factor*unit(critical+PI/2), scale_factor*unit(critical-PI/2), color = RED, stroke_width = 0.6).shift(offset_1))
                mob.counter += 1
                critical = mob.counter*TAU/90
        line_1.add_updater(line_1_updater)
        def line_2_updater(mob: Line):
            angle = alpha.get_value()
            def start_func(t: float):
                t = (t + PI/6) % PI
                case = int(t/PI*3)%3
                t = t - PI/6
                if case == 0:
                    return DOWN + 2*unit(t+PI/2)
                elif case == 1:
                    return DOWN + 2*unit(TAU/3)
                else:
                    return DOWN + 2*unit(PI/3)
            def end_func(t: float):
                t = (t + PI/6) % PI
                case = int(t/PI*3)%3
                t = t - PI/6
                if case == 0:
                    return DOWN
                elif case == 1:
                    return DOWN + 2*unit(TAU/3) + 2*unit(t-PI/2)
                else:
                    return DOWN + 2*unit(PI/3) + 2*unit(t+PI/2)
            mob.put_start_and_end_on(scale_factor*start_func(angle), scale_factor*end_func(angle))
            critical = mob.counter*TAU/90
            while angle >= critical:
                self.bring_to_back(Line(scale_factor*start_func(critical), scale_factor*end_func(critical), color = RED, stroke_width = 0.6))
                mob.counter += 1
                critical = mob.counter*TAU/90
        line_2.add_updater(line_2_updater)
        def line_3_updater(mob: Line):
            angle = alpha.get_value()
            start_func = lambda t: (2*unit(t+PI/2)+unit(-2*t-PI/2))/2 + 0.5*UP
            end_func = lambda t: (-2*unit(t+PI/2)+unit(-2*t-PI/2))/2 + 0.5*UP
            mob.put_start_and_end_on(scale_factor*start_func(angle), scale_factor*end_func(angle)).shift(offset_3)
            critical = mob.counter*TAU/90
            while angle >= critical:
                self.bring_to_back(Line(scale_factor*start_func(critical), scale_factor*end_func(critical), color = RED, stroke_width = 0.6).shift(offset_3))
                mob.counter += 1
                critical = mob.counter*TAU/90
        line_3.add_updater(line_3_updater)
        self.play(alpha.animate.set_value(PI), run_time = 4)
        for mob in [line_1, line_2, line_3]:
            mob.clear_updaters()
        self.wait(2+1+1-5, 28+26+21) #想象一个武士在狭小的空间里挥刀 他最少需要多少面积 才能将刀转过一圈呢
        self.wait(0, 21) #（空闲）

        self.fade_out(run_time = 0.5)
        self.wait(1, 9) #比较让人意想不到的是
        self.wait(2, 5) #在一种极其诡异的构造下 #https://www.youtube.com/watch?v=pWk57HpPJmQ
        self.wait(2, 0) #需要的面积可以缩小到0
        self.wait(0, 18) #（空闲）
        self.wait(3, 21) #在下期视频 我们就来好好欣赏一下这个问题的解
        self.wait(1, 0) #（空闲）

        painting = StarrySky()
        star = painting.star
        self.clear().play(FadeIn(painting, lag_ratio = 0.01, run_time = 2), self.change_notice())
        self.wait(0, 1) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, 0.5*UP), FadeIn(text_name, 0.5*UP))
        self.wait(1, 15) #而我 就像我的名字一样

        self.play(FadeOut(painting.others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star.shift, DOWN))
        self.wait(1, 8) #想要把天上的星星垂下来

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
        self.wait(1+0-2, 25+21) #变成指引前路的火光 （空闲）
        
        self.remove(star, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.wait(2, 6) #我是乐正垂星 我们下期视频再见

        self.wait(5)
        self.fade_out(end = True)
        self.wait(5) #到此共91秒

        

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]