from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Title(Text):
    def __init__(self, text):
        super().__init__(text, font = "simsun", color = YELLOW)
        self.next_to(3*UP, UP)

class TitleLine(Line):
    def __init__(self):
        super().__init__(3*UP+6*LEFT, 3*UP+6*RIGHT)

class LabelPicture(Group):
    CONFIG = {
        "picture_config": {"height": 4},
        "text_config": {"font": "simsun"},
        "text_scale": 0.4,
    }
    def __init__(self, picture, text, **kwargs):
        digest_config(self, kwargs)
        image = ImageMobject(picture, **self.picture_config)
        text = Text(text, **self.text_config).scale(self.text_scale).next_to(image, DOWN)
        super().__init__(image, text)

class BVCover(Group):
    def __init__(self, picture, text, **kwargs):
        image = ImageMobject(picture, height = 2)
        text = Text(text, font = "Times New Roman").scale(0.5).next_to(image, UP, buff = 0.1)
        super().__init__(image, text)

class Reuleaux(VMobject):
    CONFIG = {
        "radius": np.sqrt(3),
        "start_angle": PI/2
    }

    def init_points(self) -> None:
        vertices = self.radius*unit(self.start_angle), self.radius*unit(self.start_angle+TAU/3), self.radius*unit(self.start_angle+2*TAU/3)
        points = [*ArcBetweenPoints(vertices[0], vertices[1], PI/3).get_all_points(), *ArcBetweenPoints(vertices[1], vertices[2], PI/3).get_all_points(), *ArcBetweenPoints(vertices[2], vertices[0], PI/3).get_all_points()]
        self.set_points(points)

class HideIn(Animation):
    pass

class ArrowFlow(Animation):
    pass

def angle_of_vector(t: np.ndarray):
    return np.arctan2(t[1], t[0])

#################################################################### 

class Intro0(FrameScene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("我们当然期望题目的天才解答。\n但过于天才的解答，\n可能会把读者和观众带进沟里去。", font = 'simsun', t2c={"天才": GREEN, "解答": BLUE, ("读者", "观众"): YELLOW})
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
                        Notice("趣味几何", "请　尝试"),
                        Notice("离谱答案", "请　挠头"),
                        Notice("混乱构造", "请勿模仿"),
                        Notice("视频前言", "请听介绍"),
                        Notice("传统艺能", "请　三连")]
        self.notice = self.notices[0]
        
        self.play(self.change_notice())
        self.wait(1, 14) #我想请你思考这么一个问题
        line = Line(2*UL, 2*UR, stroke_width = 8)
        line.counter = 0
        self.play(ShowCreation(line))
        self.wait(1, 24) #在平面上画一条单位长度的线段
        base = Line(2*UR, 2*UL, color = GREY)
        alpha = ValueTracker(0.0)
        lines = []
        def line_updater(mob: Line):
            angle = alpha.get_value()
            def start_func(t: float):
                if t <= PI/2:
                    return 2*UL+4*np.cos(t)*RIGHT
                else:
                    return 2*DL+4*np.cos(t-PI/2)*UP
            def end_func(t: float):
                if t <= PI/2:
                    return 2*UL+4*np.sin(t)*DOWN
                else:
                    return 2*DL+4*np.sin(t-PI/2)*RIGHT
            mob.put_start_and_end_on(start_func(angle), end_func(angle))
            critical = mob.counter*TAU/90
            while angle >= critical:
                line = Line(start_func(critical), end_func(critical), color = GREY, stroke_width = 0.6)
                self.bring_to_back(line)
                lines.append(line)
                mob.counter += 1
                critical = mob.counter*TAU/90
        line.add_updater(line_updater)
        self.bring_to_back(base).play(alpha.animate.set_value(PI), run_time = 4, rate_func = lambda t: t**3*(70+t*(-315+t*(546+t*(-420+120*t)))))
        line.clear_updaters()
        self.wait(0, 19) #然后挪动这条线段 使它的朝向调转180度 （空闲）

        boundary = ParametricCurve(lambda t: 2*DL+4*np.array([(np.cos(t))**3, (np.sin(t))**3, 0]), [0, np.arcsin(np.cbrt(1/2)), np.arcsin(np.cbrt(1/2))/100]
                    ).append_points(ParametricCurve(lambda t: 2*UL+4*np.array([(np.cos(t))**3, (np.sin(t))**3, 0]), [-np.arcsin(np.cbrt(1/2)), 0, np.arcsin(np.cbrt(1/2))/100]
                    ).get_all_points()).add_points_as_corners([2*UL, 2*DL]).close_path().insert_n_curves(300).set_color(YELLOW)
        self.add(boundary, line).play(ShowCreation(boundary), run_time = 2)
        self.play(*[FadeOut(mob) for mob in lines], FadeOut(base), boundary.animate.set_fill(opacity = 0.2))
        self.wait(1+2-3, 10+6) #在这个过程中 线段最少需要划过多少面积呢
        self.wait(0, 22) #（空闲）

        self.play(FadeOut(boundary, 2*UP), line.animate.shift(2*UP), self.change_notice())
        self.wait(1, 7) #如果你是第一次遇见这个问题
        offset_l = 3*LEFT
        offset_r = 3*RIGHT + 2/np.sqrt(3)*DOWN
        line_r = line.copy().shift(offset_r)
        self.play(line.animate.shift(offset_l), TransformFromCopy(line, line_r))
        self.wait(1, 16) #那你可能会尝试一些熟悉的图形

        circle = Circle(radius = 2, color = YELLOW, fill_opacity = 0.2, n_components = 24).shift(3*LEFT)
        reuleaux = ArcBetweenPoints(2*RIGHT+offset_r, offset_r+2*np.sqrt(3)*UP, PI/3, color = YELLOW, fill_opacity = 0.2).append_points(
            ArcBetweenPoints(offset_r+2*np.sqrt(3)*UP, 2*LEFT+offset_r, PI/3).get_all_points()).append_points(ArcBetweenPoints(2*LEFT+offset_r, 2*RIGHT+offset_r, PI/3).get_all_points())
        
        alpha = ValueTracker(0.0)
        def line_updater(mob: Line):
            angle = alpha.get_value()
            mob.put_start_and_end_on(3*LEFT+2*unit(angle), 3*LEFT-2*unit(angle))
        def line_copy_updater(mob: Line):
            angle = alpha.get_value()
            def start_func(t: float):
                case = int(t/PI*3)
                if case == 0:
                    return 2*LEFT + offset_r + 4*unit(t)
                elif case == 1:
                    return offset_r + 2*np.sqrt(3)*UP
                else:
                    return 2*RIGHT + offset_r + 4*unit(t)
            def end_func(t: float):
                case = int(t/PI*3)
                if case == 0:
                    return 2*LEFT + offset_r
                elif case == 1:
                    return offset_r + 2*np.sqrt(3)*UP + 4*unit(t+PI)
                else:
                    return 2*RIGHT + offset_r
            mob.put_start_and_end_on(start_func(angle), end_func(angle))
        line.add_updater(line_updater)
        line_r.add_updater(line_copy_updater)
        self.add(circle, reuleaux, line, line_r).play(ShowCreation(circle), ShowCreation(reuleaux), alpha.animating(run_time = 3).set_value(PI))
        line.clear_updaters()
        line_r.clear_updaters()
        self.wait(0, 3) #比如说 圆 或者莱洛三角形
        self.wait(0, 20) #（空闲）

        self.wait(2, 14) #但你如果之前就遇见过这个问题
        self.wait(2, 0) #那大概也听说过它的答案
        self.wait(0, 13) #（空闲）

        self.play(line.animating(remover = True).set_stroke(width = 0), circle.animating(remover = True).scale(np.array([1, 0, 1])).set_stroke(width = 0), reuleaux.animate.shift(DOWN), line_r.animate.shift(DOWN), self.change_notice())
        self.wait(1, 10) #线段可以划过任意小的面积
        self.wait(0, 29) #（空闲）

        #photo_kakeya = ImageMobject("kakeya.jpg", height = 4).shift(3*LEFT)
        #label_kakeya = Text("挂谷宗一（1886.1.18 - 1947.1.9）", font = "simsun").scale(0.4).next_to(photo_kakeya, DOWN)
        #kakeya = Group(photo_kakeya, label_kakeya)
        kakeya = LabelPicture("kakeya.jpg", "挂谷宗一（1886.1.18 - 1947.1.9）").shift(3*LEFT)
        title = Title("挂谷问题")
        title_line = TitleLine()
        kakeya_set = Text("挂谷集", font = "simsun", color = YELLOW).scale(0.8).next_to(3*UP+3*RIGHT, DOWN)
        self.play(FadeIn(kakeya, 0.5*UP), Write(title), GrowFromCenter(title_line), )
        self.wait(1, 14) #这个问题被称作“挂谷问题”
        alpha.set_value(0)
        offset_r += DOWN
        line_r.add_updater(line_copy_updater)
        self.play(alpha.animate.set_value(PI), Write(kakeya_set, rate_func = squish_rate_func(smooth, 1/2, 5/6)), run_time = 3)
        line_r.clear_updaters()
        self.wait(0, 9) #线段扫过的部分 就被称为一个“挂谷集”
        self.wait(0, 17) #（空闲）

        offset_r += UP
        function_r = lambda t: np.array([np.sin(2*t)-2*np.sin(t), np.cos(2*t)+2*np.cos(t), 0]) + offset_r
        deltoid = ParametricCurve(function_r, [-PI/2, PI*3/2, TAU/100], color = YELLOW, fill_opacity = 0.2).save_state()
        self.play(Uncreate(reuleaux.reverse_points()), rate_func = rush_from)
        self.add(deltoid, line_r).play(ShowCreation(deltoid), rate_func = rush_from)
        self.wait(1, 12) #挂谷宗一在1917年提出这个问题的时候
        alpha.set_value(0)
        def line_copy_updater(mob: Line):
            angle = alpha.get_value()
            mob.put_start_and_end_on(function_r(angle - PI/2), function_r(angle + PI/2))
        line_r.add_updater(line_copy_updater)
        self.play(alpha.animate.set_value(PI), run_time = 3)
        line_r.clear_updaters()
        self.wait(0, 7) #猜测面积最小的图形是一条三尖内摆线的内部
        self.wait(0, 18) #（空闲）

        self.wait(1, 19) #但在1928年
        besicovich = LabelPicture("Besicovitch.jpg", "A.S.贝西科维奇（1891.1.23-1970.11.2）").shift(0.5*RIGHT)
        self.play(FadeInFromPoint(besicovich, DOWN), kakeya.animate.shift(LEFT), *[FadeOut(mob, RIGHT, run_time = 0.5, rate_func = rush_into) for mob in [deltoid, line_r, kakeya_set]])
        self.wait(1, 15) #贝西科维奇给出了一种构造
        self.wait(2, 10) #让线段可以划过任意小的面积
        self.wait(0, 17) #（空闲）

        self.play(FadeOut(kakeya, 2*LEFT, rate_func = rush_into), besicovich.animating(run_time = 2).shift(4*LEFT), self.change_notice())
        self.wait(0, 4) #在省略了相当多的细节以后
        picture_1 = ImageMobject("picture_1.png", height = 4).shift(3*RIGHT)
        self.play(FadeIn(picture_1, 0.5*UP))
        self.wait(1, 7) #他的构造大概长这个样子
        self.wait(1, 13) #突出一个乱七八糟
        self.wait(0, 24) #（空闲）
        self.wait(2, 3) #那些细节其实没什么意思
        self.wait(1+0-1, 4+20)
        self.play(*[FadeOut(mob) for mob in [besicovich, picture_1]]) #我也不打算去讲 （空闲）

        sector_1 = Arc(-PI/6, PI/3, radius = 3, stroke_width = 0, fill_opacity = 0.8, fill_color = RED).add_line_to(ORIGIN).close_path().shift(np.sqrt(3)*LEFT + 2*LEFT).insert_n_curves(14)
        sector_2 = sector_1.copy().rotate(TAU/3, about_point = 2*LEFT).set_color(ORANGE)
        sector_3 = sector_1.copy().rotate(2*TAU/3, about_point = 2*LEFT).set_color(PURPLE_A)
        reuleaux = ArcBetweenPoints(2*LEFT+np.sqrt(3)*unit(-PI/3), 2*LEFT+np.sqrt(3)*unit(PI/3), color = BACK, fill_opacity = 1).append_points(
            ArcBetweenPoints(2*LEFT+np.sqrt(3)*unit(PI/3), 2*LEFT+np.sqrt(3)*unit(PI), PI/3).get_all_points()).append_points(ArcBetweenPoints(2*LEFT+np.sqrt(3)*unit(PI), 2*LEFT+np.sqrt(3)*unit(-PI/3), PI/3).get_all_points())
        self.add(sector_3, sector_2, sector_1, reuleaux).play(Uncreate(reuleaux.reverse_points()), self.change_notice())
        self.play(sector_1.animate.shift(2*RIGHT), FadeOut(sector_2, 0.5*LEFT), FadeOut(sector_3, 0.5*LEFT))

        subsector_1 = Arc(-PI/6, PI/9, radius = 3, stroke_width = 0, fill_opacity = 0.8, fill_color = RED).add_line_to(ORIGIN).close_path().shift(np.sqrt(3)*LEFT).insert_n_curves(14)
        subsector_2 = Arc(-PI/18, PI/9, radius = 3, stroke_width = 0, fill_opacity = 0.8, fill_color = RED).add_line_to(ORIGIN).close_path().shift(np.sqrt(3)*LEFT).insert_n_curves(14)
        subsector_3 = Arc(PI/18, PI/9, radius = 3, stroke_width = 0, fill_opacity = 0.8, fill_color = RED).add_line_to(ORIGIN).close_path().shift(np.sqrt(3)*LEFT).insert_n_curves(14)
        self.remove(sector_1).add(subsector_1, subsector_2, subsector_3).remove(reuleaux).play(subsector_1.animate.shift(0.5*DOWN).set_fill(opacity = 0.6, color = RED_B), subsector_2.animate.shift(0.5*RIGHT).set_fill(opacity = 0.6, color = RED_B), subsector_3.animate.shift(0.5*UP).set_fill(opacity = 0.6, color = RED_B))
        self.play(Rotate(subsector_2, PI, about_point = (0.25-np.sqrt(3)+1.5*np.cos(PI/18))*RIGHT))
        self.play(subsector_1.animate.shift((0.5+3*np.sin(PI/18))*UP), subsector_3.animate.shift((0.5+3*np.sin(PI/18))*DOWN))
        subsectors_1 = VGroup(subsector_1, subsector_2, subsector_3)
        subsectors_2 = subsectors_1.copy().rotate(TAU/3, about_point = np.sqrt(3)*np.sin(PI/18)*RIGHT).set_fill(opacity = 0.8, color = ORANGE).shift(2*RIGHT)
        subsectors_3 = subsectors_1.copy().rotate(2*TAU/3, about_point = np.sqrt(3)*np.sin(PI/18)*RIGHT).set_color(opacity = 0.8, color = PURPLE).shift(2*RIGHT)
        group_sectors = VGroup(sector_3, sector_2, sector_1.shift(2*LEFT))
        self.add(subsectors_3, subsectors_2, subsectors_1).play(subsectors_1.animate.shift(2*RIGHT).set_fill(opacity = 0.8, color = RED), FadeIn(subsectors_2, LEFT), FadeIn(subsectors_3, LEFT))
        self.play(FadeIn(group_sectors))
        self.wait(2+1+3+2-7, 8+25+15+14) #这期视频想带给大家的是 在这一个世纪的时间里 数学家们对挂谷问题不同角度的深入思考 以及在思考旅途中遇到的风景
        self.wait(0, 19) #（空闲）

        like = Text("", font = 'vanfont').shift(3*LEFT).scale(2)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT).scale(2)
        sanlian = VGroup(like, coin, star)

        self.clear().add(self.notice).play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, ORIGIN), FadeInFromPoint(star, 3*RIGHT), self.change_notice())
        self.play(Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), sanlian.animate.set_color("#00A1D6"))
        self.wait(2, 7) #长按点赞一键三连 我们开始吧
        self.wait(2, 2)
        self.play(FadeOut(self.notice), FadeOut(sanlian))
        self.wait(2, 0) #到此共82秒
        
#################################################################### 

class Chapter1_0(FrameScene):

    def construct(self):

        text1 = Text("第一节 凸挂谷集", font = 'simsun', t2c={"第一节": YELLOW, "凸": GREEN, "挂谷集": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(FrameScene):
    def construct(self):
        self.notices = [Notice("趣味几何", "请　思考"), 
                        Notice("简单定义", "请　掌握"),
                        Notice("趣味几何", "请　思考"),
                        Notice("简单计算", "请　显然"),
                        Notice("正确答案", "请记笔记"),
                        Notice("相关结论", "请　了解")]
        self.notice = self.notices[0]

        circle = Circle(radius = 2, color = YELLOW, fill_opacity = 0.2, n_components = 24)
        line = Line(2*LEFT, 2*RIGHT, stroke_width = 8)

        self.play(Write(self.notice), GrowFromCenter(line))
        self.wait(0, 7) #我们旅途的第一站......
        self.add(circle, line).play(ShowCreation(circle))
        self.wait(0, 26) #......是去找一些圆润的挂谷集
        self.wait(0, 14) #（空闲）

        title = Title("凸集")
        title_line = TitleLine()
        self.wait(2, 10) #或者用更数学一些的语言来说......
        self.play(Write(title), GrowFromCenter(title_line))
        self.wait(0, 3) #......凸的挂谷集
        self.wait(0, 24) #（空闲）

        point_a = Dot(LEFT+UP)
        point_b = Dot(RIGHT+0.5*UP)
        self.play(self.change_notice(), line.animating(remover = True, rate_func = rush_into, run_time = 0.5).scale(0), GrowFromCenter(point_a, rate_func =lambda t: rush_from(2*t-1)), GrowFromCenter(point_b, rate_func =lambda t: rush_from(2*t-1)))
        self.wait(1, 10) #我们在集合中随便取两个点
        line = Line(LEFT+UP, RIGHT+0.5*UP)
        self.play(ShowCreation(line))
        self.wait(1, 9) #给这两个点连一条线段
        def line_updater(mob: Line):
            mob.put_start_and_end_on(point_a.get_center(), point_b.get_center())
        line.add_updater(line_updater)
        self.play(Rotate(point_b, -PI/2, about_point = ORIGIN))
        self.wait(1, 7) #如果不管这两个点怎么取
        self.play(point_a.animate.shift(2.5*RIGHT), point_b.animate.shift(1.5*LEFT + 0.5*DOWN))
        self.wait(1, 6) #线段总在集合里面
        self.play(point_a.animate.move_to(0.5*DR), point_b.animate.move_to(0.5*UL))
        self.wait(1, 0) #那么这个集合就是凸的
        line.clear_updaters()
        circle.add(point_a, point_b, line)
        self.wait(0, 18) #（空闲）

        self.wait(1, 5) #比如说......
        self.play(circle.animate.shift(4*LEFT).scale(0.75)) #......圆......
        reuleaux_submobject = [Dot(0.5*UR), Dot(0.5*DL), Line(0.5*UR, 0.5*DL)]
        reuleaux = Reuleaux(radius = 4/np.sqrt(3), color = YELLOW, fill_opacity = 0.2).add(*reuleaux_submobject).shift(4/np.sqrt(3)*DOWN+2*UP).scale(0.75)
        self.play(FadeIn(reuleaux, 0.5*UP)) 
        self.wait(2, 2) #......和莱洛三角形 就是两个凸集

        func = lambda t: np.array([np.sin(2*t)-2*np.sin(t), np.cos(2*t)+2*np.cos(t), 0])
        deltoid = ParametricCurve(func, [-PI/2, PI*3/2, TAU/100], color = GREY, fill_opacity = 0.2).add(
            Dot((7*func(PI+PI/8)-func(PI-PI/8))/6), Dot((7*func(PI-PI/8)-func(PI+PI/8))/6), Line((7*func(PI+PI/8)-func(PI-PI/8))/6, func(PI+PI/8)), Line((7*func(PI-PI/8)-func(PI+PI/8))/6, func(PI-PI/8)), Line(func(PI+PI/8), func(PI-PI/8), color = RED)
            ).shift(4*RIGHT+0.75*DOWN).scale(0.75)
        self.play(FadeIn(deltoid, 0.5*UP))
        self.wait(1, 27) #而三尖内摆线 就不是一个凸集
        self.wait(1, 2) #（空闲）
        
        self.play(self.change_notice(), FadeOut(deltoid, 2.5*RIGHT, run_time = 0.75, rate_func = rush_into), reuleaux.animating(run_time = 1.5).shift(3*RIGHT), circle.animating(run_time = 1.5).shift(RIGHT))
        self.wait(0, 10) #在这些凸挂谷集中
        self.wait(1, 26) #面积最小的是哪一个呢
        self.wait(0, 20) #（空闲）

        circle.set_submobjects([])
        reuleaux.set_submobjects([])
        slower_start = bezier([0, 0, 0, 1, 1])
        slower_end = bezier([0, 0, 1, 1, 1])
        diameter_l = Line(4.5*LEFT, 1.5*LEFT, stroke_width = 6).scale(0.5)
        diameter_r = Line(1.5*UP+3*RIGHT+3*unit(-TAU/3), 1.5*UP+3*RIGHT+3*unit(-PI/3), stroke_width = 6).scale(0.5)
        d_l = MTex(r"1").scale(0.8).next_to(diameter_l, UP)
        d_r = MTex(r"1").scale(0.8).next_to(diameter_r, UP)
        self.add(point_a, point_b, line, *reuleaux_submobject).play(
            point_a.animating(rate_func = slower_start).move_to(3*LEFT), point_b.animating(rate_func = slower_start).move_to(3*LEFT), line.animating(remover = True, rate_func = slower_start).scale(0), 
            reuleaux_submobject[0].animating(rate_func = slower_start).move_to(3*RIGHT+np.sqrt(3)*DOWN+1.5*UP), reuleaux_submobject[1].animating(rate_func = slower_start).move_to(3*RIGHT+np.sqrt(3)*DOWN+1.5*UP), reuleaux_submobject[2].animating(rate_func = slower_start, remover = True).scale(0),
            GrowFromCenter(diameter_l, rate_func = rush_into), GrowFromCenter(diameter_r, rate_func = rush_into), run_time = 0.5)
        self.play(*[mob.animating(remover = True, rate_func = slower_end).scale(0) for mob in [point_a, point_b, reuleaux_submobject[0], reuleaux_submobject[1]]], 
                  diameter_l.animating(rate_func = rush_from).scale(2), diameter_r.animating(rate_func = rush_from).scale(2),
                  Write(d_l), Write(d_r), rate_func = slower_end, run_time = 0.5)
        circle.add(diameter_l, d_l)
        reuleaux.add(diameter_r, d_r)
        self.wait(1, 26) #圆和莱洛三角形都是好算面积的
        texts = r"S=\frac{\pi}{4}\approx", r"0.785"
        s_circle = Tex(texts[0]+texts[1], isolate = texts).scale(0.8).shift(3*LEFT)
        s_circle.shift((2.25-s_circle[-1].get_y())*UP)
        parts_l = [s_circle.get_part_by_tex(text) for text in texts]
        texts = r"S=\frac{\pi-\sqrt{3}}{2}\approx", r"0.705"
        s_reuleaux = Tex(texts[0]+texts[1], isolate = texts).scale(0.8).shift(3*RIGHT)
        s_reuleaux.shift((2.25-s_reuleaux[-1].get_y())*UP)
        parts_r = [s_reuleaux.get_part_by_tex(text) for text in texts]
        self.play(Write(s_circle), Write(s_reuleaux), self.change_notice(), run_time = 1)
        self.wait(0, 14) #算出来比一比
        self.wait(2, 11) #可以知道莱洛三角形的面积比较小
        self.wait(0, 23) #（空闲）

        shade_l = BackgroundRectangle(parts_l[0], color = BACK, buff = 0.1, fill_opacity = 1)
        shade_r = BackgroundRectangle(parts_r[0], color = BACK, buff = 0.1, fill_opacity = 1)
        offset_l_1 = (-4 - parts_l[1].get_center()[0])*RIGHT
        shade_l.next_to(parts_l[1].get_left(), RIGHT, buff = -0.1, coor_mask = np.array([1, 0, 0]))
        offset_l_0 = offset_l_1 + shade_l.get_center() - parts_l[0].get_center()
        offset_r_1 = (4 - parts_r[1].get_center()[0])*RIGHT
        shade_r.next_to(parts_r[1].get_left(), RIGHT, buff = -0.1, coor_mask = np.array([1, 0, 0]))
        offset_r_0 = offset_r_1 + shade_r.get_center() - parts_r[0].get_center()
        self.add(shade_l, parts_l[1], shade_r, parts_r[1], self.notice).play(circle.animate.shift(LEFT), reuleaux.animate.shift(RIGHT), 
                parts_l[0].animate.shift(offset_l_0), parts_l[1].animate.shift(offset_l_1), shade_l.animate.shift(offset_l_1), 
                parts_r[0].animate.shift(offset_r_0), parts_r[1].animate.shift(offset_r_1), shade_r.animate.shift(offset_r_1))
        reuleaux.set_submobjects([])
        self.remove(parts_l[0], parts_r[0], shade_l, shade_r)
        self.wait(1, 1) #但面积最小的凸挂谷集

        line = Line(1.5*UP, 1.5*DOWN, stroke_width = 6)
        triangle = Polygon(1.5*UP, 1.5*DOWN+np.sqrt(3)*LEFT, 1.5*DOWN+np.sqrt(3)*RIGHT, color = YELLOW, fill_opacity = 0.2)
        d_m = MTex(r"1").scale(0.8).next_to(line, RIGHT)
        s_triangle = MTex(r"S=\frac{\sqrt3}{3}\approx0.577", isolate = texts).scale(0.8)
        s_triangle.shift((2.25-s_triangle[-1].get_y())*UP)
        self.play(ShowCreation(triangle), self.change_notice())
        self.play(GrowFromCenter(line), Write(s_triangle), Write(d_m))
        self.wait(0, 13) #其实是一个不太圆润的答案
        self.wait(1, 6) #正三角形
        self.wait(0, 28) #（空闲）


        self.play(*[FadeOut(mob, 2.5*LEFT, run_time = 0.75, rate_func = rush_into) for mob in [parts_l[1], circle]], 
                  *[FadeOut(mob, 3*LEFT, run_time = 1.5) for mob in [s_triangle, d_m]], *[mob.animating(run_time = 1.5).shift(3*LEFT) for mob in [line, triangle]], 
                  *[FadeOut(mob, LEFT, run_time = 1.5) for mob in [parts_r[1], d_r]], *[mob.animating(run_time = 1.5).shift(LEFT) for mob in [reuleaux, diameter_r]])
        self.wait(1, 0) #这可能是一个不太符合直觉的答案
        alpha = ValueTracker(0.0)
        def line_updater(mob: VMobject):
            value = alpha.get_value()
            mob.restore().rotate(value, about_point = 3*LEFT + 3*np.sqrt(3)/2*LEFT).shift(value/(PI/3)*(3*DOWN + np.sqrt(3)*RIGHT))
        line.save_state().add_updater(line_updater)
        self.play(alpha.animate.set_value(PI/6))
        line.clear_updaters().save_state()
        self.wait(1, 0)
        self.play(line.animate.shift(0.2*unit(PI/4)), run_time = 0.5)
        self.wait(0, 15)
        self.play(line.animate.shift(0.2*unit(-PI/6)), run_time = 0.5)
        self.wait(2+1-3, 23+12-15) #毕竟在正三角形内 线段还能稍微活动一下
        self.play(line.animate.restore(), Rotate(diameter_r, PI/3, about_point = diameter_r.get_start(), run_time = 1.5))
        self.play(Rotate(diameter_r, PI/3, about_point = diameter_r.get_end(), run_time = 1.5))
        self.wait(1+2-3, 22+16) #而在莱洛三角形内 线段就只能旋转 没法平移
        self.wait(0, 22) #（空闲）

        self.play(FadeOut(line), FadeOut(diameter_r))
        self.wait(1, 25) #但其实这种直觉关系的是另一个问题
        self.wait(0, 18) #（空闲）

        c_orbiform = MTex(r"C=\pi\approx 3.142").scale(0.8).shift(3*RIGHT)
        c_orbiform.shift((2.25-c_orbiform[-1].get_y())*UP)
        c_triangle = MTex(r"C=2\sqrt3\approx 3.464").scale(0.8).shift(4*LEFT)
        c_triangle.shift((2.25-c_triangle[-1].get_y())*UP)
        self.play(self.change_notice())
        self.wait(0, 6) #事实上......
        self.play(Write(c_orbiform), run_time = 1)
        self.wait(2, 0) #......莱洛三角形是周长最小的挂谷集
        circle = Circle(radius = 1.5, color = YELLOW, fill_opacity = 0.2, n_components = 24).shift(4*RIGHT)
        self.play(triangle.animate.shift(LEFT), reuleaux.animate.shift(3*LEFT), c_orbiform.animate.shift(LEFT), FadeIn(circle, 5*LEFT), run_time = 1.5)
        self.wait(1, 10) #并且 圆其实也是
        self.play(Write(c_triangle), run_time = 1)
        self.wait(2, 14) #而等边三角形的周长 比它们都要大
        self.wait(1, 9) #（到此共74秒）
        
class Chapter1_2(FrameScene):
    def construct(self):
        self.notices = [Notice("相关结论", "请　了解"),
                        Notice("证明过程", "请　专注"),
                        Notice("简单情况", "请　显然")]
        self.notice = self.notices[0]

        title = Title("凸集")
        title_line = TitleLine()
        circle = Circle(radius = 1.5, color = YELLOW, fill_opacity = 0.2, n_components = 24).shift(4*RIGHT)
        reuleaux = Reuleaux(radius = np.sqrt(3), color = YELLOW, fill_opacity = 0.2).shift(np.sqrt(3)*DOWN+1.5*UP)
        triangle = Polygon(1.5*UP, 1.5*DOWN+np.sqrt(3)*LEFT, 1.5*DOWN+np.sqrt(3)*RIGHT, color = YELLOW, fill_opacity = 0.2).shift(4*LEFT)
        c_orbiform = MTex(r"C=\pi\approx 3.142").scale(0.8).shift(2*RIGHT)
        c_orbiform.shift((2.25-c_orbiform[-1].get_y())*UP)
        c_triangle = MTex(r"C=2\sqrt3\approx 3.464").scale(0.8).shift(4*LEFT)
        c_triangle.shift((2.25-c_triangle[-1].get_y())*UP)
        self.add(circle, reuleaux, triangle, c_orbiform, c_triangle, title, title_line, self.notice).play(self.change_notice(), *[FadeOut(mob) for mob in [c_orbiform, c_triangle, circle, triangle]], reuleaux.animate.scale(4/3))
        self.wait(0, 15) #让我们说回面积
        self.wait(0, 20) #（空闲）

        self.wait(2, 17) #凸集有一个非常好用的性质
        vertices = [2*UP, 2*LEFT+2*(1-np.sqrt(3))*UP, 2*RIGHT+2*(1-np.sqrt(3))*UP]
        def boundary(angle: float):
            angle = angle%TAU
            if angle <= PI/3:
                return vertices[1] + 4*unit(angle)
            elif angle <= PI*2/3:
                return vertices[0]
            elif angle <= PI:
                return vertices[2] + 4*unit(angle)
            elif angle <= PI*4/3:
                return vertices[1]
            elif angle <= PI*5/3:
                return vertices[0] + 4*unit(angle)
            else:
                return vertices[2]
        point = Dot(boundary(PI/6), color = GREEN)
        self.play(ShowCreation(point))
        self.wait(1, 7) #过凸集边界上的任意一个点
        line = Line(boundary(PI/6) + unit(PI/6+PI/2), boundary(PI/6) + unit(PI/6-PI/2), color = GREEN)
        self.play(GrowFromCenter(line))
        alpha = ValueTracker(PI/6)
        def point_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(boundary(value))
        def line_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(boundary(value) + unit(value+PI/2), boundary(value) + unit(value-PI/2))
        point.add_updater(point_updater)
        line.add_updater(line_updater)
        self.play(alpha.animate.set_value(PI/3))
        self.play(alpha.animate.set_value(2*PI/3), run_time = 2/3, frames = 20, rate_func = bezier([0, 0, 1, 1]))
        self.play(alpha.animate.set_value(PI))
        self.play(alpha.animate.set_value(4*PI/3), run_time = 2/3, frames = 20, rate_func = bezier([0, 0, 1, 1]))
        self.play(alpha.animate.set_value(5*PI/3))
        self.play(alpha.animate.set_value(TAU), run_time = 2/3, frames = 20, rate_func = bezier([0, 0, 1, 1]))
        self.play(alpha.animate.set_value(TAU+PI/6))
        point.clear_updaters()
        line.clear_updaters()
        self.play(line.animating(remover = True, rate_func = bezier([0, 0, 0, 1, 1])).scale(0), run_time = 0.5)
        self.play(point.animating(remover = True, rate_func = bezier([0, 0, 1, 1, 1])).scale(0), run_time = 0.5)
        self.wait(2+2+0+2+0-8, 10+6+18+24+24) #我们总可以作出一条直线 使得凸集在这条直线的一侧 （空闲） 这会为后续的证明带来很大帮助 （空闲）
        
        self.wait(1, 3) #第一步......
        incircle_r = Circle(radius = 4-4/np.sqrt(3), color = BLUE, fill_opacity = 0.2).shift(2*UP+4/np.sqrt(3)*DOWN)
        self.play(FadeIn(incircle_r, scale = np.infty))
        self.wait(1, 18) #......我们需要在凸集内找一个最大的内切圆
        self.wait(0, 19) #（空闲）

        points = VGroup(Dot(boundary(PI/6)), Dot(boundary(5*PI/6)), Dot(boundary(3*PI/2))).set_color(BLUE)
        self.play(ShowCreation(points, lag_ratio = 0.3, remover = True))
        incircle_r.add(points)
        self.wait(2, 7) #大多数凸集的内切圆都会有三个切点

        eye = ArcBetweenPoints(3*LEFT+3*np.cos(PI/6)*unit(-PI/6), 3*LEFT-3*np.cos(PI/6)*unit(-PI/6), TAU/3, color = YELLOW, fill_opacity = 0.2).append_points(
                ArcBetweenPoints(3*LEFT-3*np.cos(PI/6)*unit(-PI/6), 3*LEFT+3*np.cos(PI/6)*unit(-PI/6), TAU/3).get_all_points())
        incircle = Circle(radius = 3/2, color = BLUE, fill_opacity = 0.2).shift(3*LEFT).add(Dot(3*LEFT+3/2*unit(PI/3), color = BLUE, radius = 0.06), Dot(3*LEFT-3/2*unit(PI/3), color = BLUE, radius = 0.06))
        self.play(reuleaux.animate.shift(3*RIGHT).scale(0.75), incircle_r.animate.shift(3*RIGHT).scale(0.75, about_point = 3*RIGHT), FadeIn(eye, 5*RIGHT, scale = 0.75), FadeIn(incircle, 5*RIGHT, scale = 0.75), self.change_notice())
        self.wait(2, 25) #但也有一些凸集 它的内切圆只有两个切点
        self.wait(0, 23) #（空闲）

        smaller_incircle = Circle(radius = 3-np.sqrt(3), color = BLUE).shift(np.cos(PI/6)*unit(5*PI/6) + 3*LEFT)
        tangency_1, tangency_2 = 3*LEFT+3/2*unit(PI/3)-3*unit(PI/6), 3*LEFT-3/2*unit(PI/3)+3*unit(PI/2)
        dot_1, dot_2 = Dot(tangency_1, radius = 0.06, color = BLUE), Dot(tangency_2, radius = 0.06, color = BLUE)
        line = DashedLine(tangency_1, tangency_2, color = BLUE)
        self.play(incircle.animate.set_color(interpolate_color(BLUE, GREY, 0.8)), ShowCreation(smaller_incircle), FadeIn(dot_1, scale = np.infty), FadeIn(dot_2, scale = np.infty))
        self.play(ShowCreation(line))
        self.wait(1, 1) #要是这两个点不是直径的两个端点

        arrow = Arrow(3*LEFT+3/2*unit(5*PI/6)+unit(PI*5/6), 3*LEFT+3/2*unit(5*PI/6)-unit(PI*5/6), color = YELLOW, buff = 0, stroke_width = 8).save_state()
        beta = ValueTracker(0.0)
        def arrow_updater(mob: Arrow):
            ratio = beta.get_value()
            start = 0.6*interpolate(unit(PI*5/6), -unit(PI*5/6), rush_into(ratio)) + 3*LEFT+3/2*unit(5*PI/6)
            end = 0.6*interpolate(unit(PI*5/6), -unit(PI*5/6), rush_from(ratio)) + 3*LEFT+3/2*unit(5*PI/6)
            mob.restore().put_start_and_end_on(start, end)
        arrow.add_updater(arrow_updater)
        self.add(arrow).play(beta.animate.set_value(1.0), rate_func = linear)
        self.remove(arrow.clear_updaters())
        self.play(smaller_incircle.animate.shift(np.cos(PI/6)*unit(-PI/6)), *[FadeOut(mob, np.cos(PI/6)*unit(-PI/6)) for mob in [dot_1, dot_2, line]])
        self.play(smaller_incircle.animating(remover = True).scale((3+np.sqrt(3))/4), incircle.animate.set_color(BLUE))
        self.wait(2+0-3, 17+18) #那么这个内切圆就还可以再变大一点 （空闲）

        self.play(eye.animate.shift(3*RIGHT).scale(4/3), incircle.animate.shift(3*RIGHT).scale(4/3), FadeOut(VGroup(reuleaux, incircle_r), 5*RIGHT, scale = 4/3))
        self.wait(1, 26) #而我们既然已经找了最大的内切圆
        diameter = Line(-2*unit(PI/3), 2*unit(PI/3), color = BLUE)
        center = Dot(color = BLUE)
        self.play(ShowCreation(diameter), FadeIn(center, scale = np.infty, rate_func = rush_into))
        self.wait(1, 13) #这两个点肯定就是它的直径了
        self.wait(0, 27) #（空闲）

        line_1, line_2 = Line(-2*unit(PI/3)-2*unit(-PI/6), -2*unit(PI/3)+2*unit(-PI/6), color = GREEN), Line(2*unit(PI/3)-2*unit(-PI/6), 2*unit(PI/3)+2*unit(-PI/6), color = GREEN)
        dot_1, dot_2 = incircle.submobjects
        incircle.set_submobjects([])
        self.add(line_1, line_2, dot_1, dot_2).play(GrowFromCenter(line_1), GrowFromCenter(line_2))
        self.wait(0, 16) #我们过两个切点
        indicate = eye.copy().set_fill(opacity = 0).set_stroke(color = WHITE, width = 8)
        points = indicate.get_all_points().copy()
        indicate.set_points([*points[12:], *points[0:12]])
        self.add(indicate, dot_1, dot_2).play(ShowPassingFlash(indicate), run_time = 2)
        self.wait(1+0-2, 22+20) #作出之前说过的直线来 （空闲）

        indicate = incircle.copy().set_fill(opacity = 0).set_stroke(color = WHITE, width = 8).rotate(PI/3)
        self.add(indicate, dot_1, dot_2).play(ShowPassingFlash(indicate), run_time = 2)
        self.wait(0, 1) #内切圆作为凸集的一部分
        arrow_1_1 = Arrow(-2.5*unit(PI/3)+2/3*unit(-PI/6), -2*unit(PI/3)+2/3*unit(-PI/6), buff = 0, color = GREEN)
        arrow_1_2 = Arrow(-2.5*unit(PI/3)-2/3*unit(-PI/6), -2*unit(PI/3)-2/3*unit(-PI/6), buff = 0, color = GREEN)
        arrow_2_1 = Arrow(2.5*unit(PI/3)+2/3*unit(-PI/6), 2*unit(PI/3)+2/3*unit(-PI/6), buff = 0, color = GREEN)
        arrow_2_2 = Arrow(2.5*unit(PI/3)-2/3*unit(-PI/6), 2*unit(PI/3)-2/3*unit(-PI/6), buff = 0, color = GREEN)
        self.play(FadeIn(arrow_1_1, 0.5*unit(PI/3)), FadeIn(arrow_1_2, 0.5*unit(PI/3)), FadeIn(arrow_2_1, -0.5*unit(PI/3)), FadeIn(arrow_2_2, -0.5*unit(PI/3)))
        self.wait(0, 27) #当然也被分到了直线的一侧
        self.wait(0, 18) #（空闲）

        elbow_1 = Elbow(angle = 5*PI/6, width = 0.2, color = GREEN).shift(2*unit(PI/3))
        elbow_2 = Elbow(angle = -PI/6, width = 0.2, color = GREEN).shift(-2*unit(PI/3))
        self.add(elbow_1, elbow_2, line_1, line_2, diameter, dot_1, dot_2).play(*[FadeOut(mob) for mob in [arrow_1_1, arrow_1_2, arrow_2_1, arrow_2_2]], ShowCreation(elbow_1), ShowCreation(elbow_2))
        self.wait(1, 14) #那这条直线就必然是圆的切线了
        self.wait(0, 21) #（空闲）
        self.wait(3, 10) #于是 内切圆 和整个凸集
        indicate_1 = line_1.copy().set_stroke(color = WHITE, width = 8)
        indicate_2 = line_2.copy().set_stroke(color = WHITE, width = 8)
        self.add(indicate_1, indicate_2, dot_1, dot_2).play(ShowPassingFlash(indicate_1, time_width = 0.2), ShowPassingFlash(indicate_2, time_width = 0.2), run_time = 1)
        self.add(indicate_1, indicate_2, dot_1, dot_2).play(ShowPassingFlash(indicate_1, time_width = 0.2), ShowPassingFlash(indicate_2, time_width = 0.2), run_time = 1)
        self.wait(0, 11) #就都被夹在了两条平行直线中间
        self.wait(0, 21) #（空闲）

        segment = Line(2*LEFT, 2*RIGHT, stroke_width = 8).shift(unit(-PI/3))
        self.add(segment, dot_1, dot_2, center).play(ShowCreation(segment))
        self.wait(1, 24) #这个时候再看一看凸集中的线段
        self.play(Rotate(segment, PI/3, about_point = unit(-TAU/3)))
        self.wait(1, 13) #它总要旋转到垂直于直线的方向的
        self.wait(0, 18) #（空闲）
        
        text_d = MTex(r"\ge 1").scale(0.8).shift(0.5*unit(5*PI/6))
        text_s = MTex(r"S\ge \frac{\pi}{4}\approx 0.785").scale(0.8).shift(4.5*RIGHT)
        self.play(Write(text_d))
        self.wait(2, 5) #也就是说 内切圆的直径至少是1
        self.wait(0, 19) #（空闲）
        self.play(Write(text_s, run_time = 1))
        self.wait(2, 8) #而直径为1的圆本身面积都不是最小
        self.wait(2, 21) #这个凸集的面积就更不可能最小了
        self.wait(1, 3) #到此共75秒
        
class Chapter1_3(FrameScene):
    def construct(self):
        self.notices = [Notice("简单情况", "请　显然"),
                        Notice("复杂情况", "请　专注"),
                        Notice("证明完毕", "请　鼓掌")]
        self.notice = self.notices[0]

        title = Title("凸集")
        title_line = TitleLine()
        eye = ArcBetweenPoints(4*np.cos(PI/6)*unit(-PI/6), -4*np.cos(PI/6)*unit(-PI/6), TAU/3, color = YELLOW, fill_opacity = 0.2).append_points(
                ArcBetweenPoints(-4*np.cos(PI/6)*unit(-PI/6), 4*np.cos(PI/6)*unit(-PI/6), TAU/3).get_all_points())
        incircle = Circle(radius = 2, color = BLUE, fill_opacity = 0.2)
        elbow_1, elbow_2 = Elbow(angle = 5*PI/6, width = 0.2, color = GREEN).shift(2*unit(PI/3)), Elbow(angle = -PI/6, width = 0.2, color = GREEN).shift(-2*unit(PI/3))
        line_1, line_2 = Line(-2*unit(PI/3)-2*unit(-PI/6), -2*unit(PI/3)+2*unit(-PI/6), color = GREEN), Line(2*unit(PI/3)-2*unit(-PI/6), 2*unit(PI/3)+2*unit(-PI/6), color = GREEN)
        segment = Line(-2*unit(PI/3), 2*unit(PI/3), stroke_width = 8)
        dot_1, dot_2, center = Dot(-2*unit(PI/3), color = BLUE), Dot(2*unit(PI/3), color = BLUE), Dot(color = BLUE)
        text_d = MTex(r"\ge 1").scale(0.8).shift(0.5*unit(5*PI/6))
        text_s = MTex(r"S\ge \frac{\pi}{4}\approx 0.785").scale(0.8).shift(4.5*RIGHT)
        
        self.add(self.notice, title, title_line, eye, incircle, elbow_1, elbow_2, line_1, line_2, segment, dot_1, dot_2, center, text_d, text_s)
        self.fade_out(excepts = [title, title_line], change_notice = True)
        vertices = [0.55*RIGHT+1.5*UP, 1.25*LEFT+0.9*DOWN, 1.25*RIGHT+0.9*DOWN]
        def boundary(angle: float):
            angle = angle%TAU
            if angle <= np.arctan(4/3):
                return vertices[1] + 3.5*unit(angle)
            elif angle <= 2*np.arctan(4/3):
                return vertices[0] + 0.5*unit(angle)
            elif angle <= PI:
                return vertices[2] + 3*unit(angle)
            elif angle <= PI + np.arctan(4/3):
                return vertices[1] + 0.5*unit(angle)
            elif angle <= PI + 2*np.arctan(4/3):
                return vertices[0] + 3.5*unit(angle)
            else:
                return vertices[2] + unit(angle)
        reuleaux = ParametricCurve(boundary, [0, TAU, TAU/100], color = YELLOW, fill_opacity = 0.2)
        # lines = VGroup(Line(boundary(0), boundary(PI)), Line(boundary(np.arctan(4/3)), boundary(PI+np.arctan(4/3))), Line(boundary(2*np.arctan(4/3)), boundary(PI+2*np.arctan(4/3))))
        offset = 0.29*RIGHT+0.18*DOWN
        vector = offset - vertices[1]
        angle = np.arctan2(vector[1], vector[0])
        angle_0, angle_1, angle_2 = 2*np.arctan(4/3)-PI-angle, angle, np.arctan(4/3)+PI/2
        positions = [boundary(angle_0), boundary(angle_1), boundary(angle_2)]
        points = VGroup(Dot(positions[0]), Dot(positions[1]), Dot(positions[2])).set_color(BLUE)
        incircle = Circle(radius = 1.8, color = BLUE, fill_opacity = 0.2).shift(offset)
        self.fade_in(reuleaux, incircle, points, excepts = [title, title_line])
        self.wait(1+1-2, 14+27) #其它的凸集 内切圆至少会有三个切点
        self.wait(0, 24) #（空闲）
        
        left_convex = Polygon(1.5*UP+0.5*RIGHT, 1.5*UP+0.5*LEFT, 1.5*DOWN+3.5*LEFT, 1.5*DOWN+3.5*RIGHT, color = YELLOW, fill_opacity = 0.2).shift(3*LEFT)
        radius_l = (1+np.sqrt(2))/2
        offset_l = 1.5*UP + radius_l*DOWN
        incircle_small = Circle(radius = radius_l, color = BLUE, fill_opacity = 0.2).shift(3*LEFT + offset_l)
        points_l = VGroup(Dot(radius_l*unit(PI/4), radius = 0.06), Dot(radius_l*unit(PI/2), radius = 0.06), Dot(radius_l*unit(3*PI/4), radius = 0.06)).set_color(BLUE).shift(offset_l + 3*LEFT)
        self.play(*[mob.animate.scale(0.75, about_point = ORIGIN).shift(3*RIGHT) for mob in [reuleaux, incircle, points]], FadeIn(VGroup(left_convex, incircle_small, points_l), 5*RIGHT, scale = 0.75))
        self.wait(2, 11) #要是内切圆所有的切点都在同一个半圆上
        radius_l_2 = 7*(np.sqrt(2)-1)/2
        offset_l_2 = 1.5*DOWN + radius_l_2*UP
        points_l_2 = VGroup(Dot(radius_l_2*unit(PI/4), radius = 0.06), Dot(radius_l_2*unit(-PI/2), radius = 0.06), Dot(radius_l_2*unit(3*PI/4), radius = 0.06)).set_color(BLUE).shift(offset_l_2 + 3*LEFT)
        self.play(incircle_small.animate.shift(offset_l_2 - offset_l), FadeOut(points_l, offset_l_2 - offset_l))
        self.play(incircle_small.animate.scale(radius_l_2/radius_l))
        self.play(ShowCreation(points_l_2, lag_ratio = 0.3))
        self.wait(2+0+2-3, 6+17+9) #那么我们也可以把它再变大一点 （空闲） 既然这个内切圆是最大的
        self.play(FadeOut(VGroup(left_convex, incircle_small, points_l_2), 3*LEFT), *[mob.animate.shift(3*LEFT) for mob in [reuleaux, incircle, points]])
        self.wait(2, 11) #我们就肯定能找到三个不在同一个半圆上的点
        self.wait(0, 21) #（空闲）

        offset *= 0.75
        for position in positions:
            position *= 0.75
        midpoints = [(positions[1]+positions[2])/2 - offset, (positions[2]+positions[0])/2 - offset, (positions[0]+positions[1])/2 - offset]
        triangle_vertices = [midpoints[0]*1.35**2/get_norm(midpoints[0])**2 + offset, midpoints[1]*1.35**2/get_norm(midpoints[1])**2 + offset, midpoints[2]*1.35**2/get_norm(midpoints[2])**2 + offset]
        edges = [Line(triangle_vertices[1], triangle_vertices[2], color = GREEN), Line(triangle_vertices[2], triangle_vertices[0], color = GREEN), Line(triangle_vertices[0], triangle_vertices[1], color = GREEN)]
        self.add(*edges, points).play(*[GrowFromPoint(edges[i], positions[i]) for i in range(3)])
        self.wait(1, 9) #过这三个点分别作切线
        labels = VGroup(MTex(r"A", color = GREEN).scale(0.8).next_to(triangle_vertices[0], UP, buff = 0.15), MTex(r"B", color = GREEN).scale(0.8).next_to(triangle_vertices[1], LEFT, buff = 0.15), MTex(r"C", color = GREEN).scale(0.8).next_to(triangle_vertices[2], RIGHT, buff = 0.15))
        self.play(Write(labels))
        self.wait(1, 25) #就可以得到一个有内切圆的三角形
        center = Dot(offset, color = BLUE, radius = 0.06)
        radius = Line(offset, positions[0], color = BLUE, stroke_width = 3)
        label_r = MTex(r"r", color = BLUE).scale(0.8).next_to(radius.get_center(), RIGHT, buff = 0.2)
        self.play(ShowCreation(center), ShowCreation(radius), Write(label_r))
        self.wait(1, 5) #设这个内切圆的半径是r
        self.wait(1, 2) #（空闲）
        
        segment = Line(0.75*boundary(0), 0.75*boundary(PI), stroke_width = 6)
        self.add(segment, radius, points, center).play(ShowCreation(segment))
        self.wait(1, 9) #我们看一看凸集中的线段
        alpha = ValueTracker(0)
        def segment_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(0.75*boundary(value), 0.75*boundary(PI+value))
        segment.add_updater(segment_updater)
        self.play(alpha.animate.set_value(angle_0), run_time = 2)
        segment.clear_updaters()
        self.wait(0, 29) #它总要旋转到和BC垂直的方向
        label_s = MTex(r"1").scale(0.8).next_to(segment.get_center(), RIGHT, buff = 0.2)
        self.play(Write(label_s))
        self.wait(1, 13) #这条线段完全在三角形内
        projection = triangle_vertices[1] + (triangle_vertices[2]-triangle_vertices[1])*np.dot(triangle_vertices[2]-triangle_vertices[1], triangle_vertices[0]-triangle_vertices[1])/(get_norm(triangle_vertices[2]-triangle_vertices[1])**2)
        height = Line(triangle_vertices[0], projection, color = GREEN)
        label_h = MTex(r"H", color = GREEN).scale(0.8).next_to(projection, DOWN, buff = 0.15).shift(0.2*LEFT)
        elbow = Elbow(angle = PI+angle_0, width = 0.2, color = GREEN).shift(projection)
        text_1 = MTex(r"AH\ge 1", tex_to_color_map = {r"AH": GREEN}).scale(0.8)
        text_1.shift(5*LEFT+2*UP-text_1[2].get_center())
        self.play(ShowCreation(height))
        self.play(ShowCreation(elbow), Write(label_h), Write(text_1))
        self.wait(0, 14) #说明BC边上的高大于等于1
        self.wait(0, 18) #（空闲）

        text_2 = MTex(r"S_{\triangle ABC}=\frac{1}{2}BC\cdot AH", tex_to_color_map = {(r"AH", r"BC"): GREEN, r"S_{\triangle ABC}": TEAL}).scale(0.8)
        text_2.shift(5*LEFT+UP-text_2[5].get_center())
        self.play(Write(text_2))
        self.wait(1, 1) #设ABC的面积为S
        text_3 = MTex(r"\Rightarrow BC&=\frac{2S_{\triangle ABC}}{AH}\\&\le 2S_{\triangle ABC}", tex_to_color_map = {(r"AH", r"BC"): GREEN, r"S_{\triangle ABC}": TEAL}).scale(0.8)
        text_3.shift(5*LEFT+0.5*DOWN-text_3[3].get_center())
        self.play(Write(text_3))
        self.wait(1+0-2, 24+19) #我们就能得到这个关系（空闲）

        offset_text = 5*LEFT+0.5*DOWN-text_3[-7].get_center()
        label_o = MTex(r"O", color = BLUE).scale(0.8).next_to(offset, LEFT, buff = 0.15)
        label_d = MTex(r"D", color = BLUE).scale(0.8).next_to(positions[0], DOWN, buff = 0.15)
        label_p = MTex(r"P").scale(0.8).next_to(0.75*boundary(angle_0+PI), UP, buff = 0.15)
        op = Line(offset, 0.75*boundary(angle_0+PI), color = BLUE, stroke_width = 3)
        self.play(FadeOut(text_1, 0.3*UP), FadeOut(text_2, 0.3*UP), FadeOut(text_3[0], offset_text), FadeOut(text_3[3:-7], offset_text), text_3[-7:].animate.shift(offset_text), 
                  *[FadeOut(mob) for mob in [height, label_h, elbow]], Write(label_p), Write(label_d), *[Write(mob, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)) for mob in [label_o, label_d]], ShowCreation(op.reverse_points()))
        self.wait(1+2-2, 14+17) #再连接OP 那么OP和OD的和也不小于1
        self.wait(0, 17) #（空闲）
        condition_bc = VGroup(text_3[1], text_3[2], text_3[-7:])

        label_x = MTex(r"X", color = PURPLE_A).scale(0.8).next_to(label_p, LEFT, buff = 0.1)
        offset_label = label_p.get_center() - label_x.get_center()
        shade_x = BackgroundRectangle(label_x, color = BACK, fill_opacity = 1, buff = 0.1).shift(0.1*LEFT)
        shade_p = BackgroundRectangle(label_p, color = BACK, fill_opacity = 1, buff = 0.1).shift(offset_label+0.1*RIGHT)
        line_ox = Line(0.75*boundary(angle_0+PI), offset, color = PURPLE_A, stroke_width = 3)
        label_ox = MTex(r"1-r", color = PURPLE_A).scale(0.8).next_to(line_ox.get_center(), RIGHT, buff = 0.1).shift(0.1*DOWN)
        self.wait(1, 14) #这也就是说......
        self.bring_to_back(label_x, label_p, shade_x, shade_p).add(line_ox, center).play(label_x.animate.shift(offset_label), label_p.animate.shift(offset_label), Uncreate(op.reverse_points()), ShowCreation(line_ox))
        self.remove(label_p, shade_x, shade_p)
        self.wait(2, 8) #......我们可以在EF外面取一个点X
        self.play(FadeOut(label_s), Write(label_ox))
        self.wait(1, 6) #使得OX长为1-r
        self.wait(0, 18) #（空闲）
        condition_ac = MTex(r"AC&\le 2S_{\triangle ABC}", tex_to_color_map = {r"AC": GREEN, r"S_{\triangle ABC}": TEAL}).scale(0.8)
        condition_ac.shift(5*LEFT+0.25*UP-condition_ac[2].get_center())
        label_y = MTex(r"Y", color = PURPLE_A).scale(0.8).next_to(0.75*boundary(angle_1-PI), LEFT)
        line_oy = Line(0.75*boundary(angle_1-PI), offset, color = PURPLE_A, stroke_width = 3)
        segment.add_updater(segment_updater)
        self.play(alpha.animating(run_time = 2).set_value(angle_1-PI), label_o.animate.shift(0.2*UP))
        self.add(line_oy, center, label_o).play(condition_bc.animate.shift(0.25*DOWN), FadeIn(condition_ac, 0.25*DOWN), Write(label_y), Write(line_oy))
        condition_ab = MTex(r"AB&\le 2S_{\triangle ABC}", tex_to_color_map = {r"AB": GREEN, r"S_{\triangle ABC}": TEAL}).scale(0.8)
        condition_ab.shift(5*LEFT+UP-condition_ab[2].get_center())
        label_z = MTex(r"Z", color = PURPLE_A).scale(0.8).next_to(0.75*boundary(angle_2+PI), RIGHT)
        line_oz = Line(0.75*boundary(angle_2+PI), offset, color = PURPLE_A, stroke_width = 3)
        segment.add_updater(segment_updater)
        self.play(alpha.animating(run_time = 2).set_value(angle_2-TAU))
        self.add(line_oz, center, label_o).play(condition_bc.animate.shift(0.25*DOWN), condition_ac.animate.shift(0.25*DOWN), FadeIn(condition_ab, 0.25*DOWN), Write(label_z), Write(line_oz))
        segment.clear_updaters()
        self.wait(1+2+1-6, 19+17+29) #用同样的方法 我们也可以得到另外两个关系式 并且得到Y点和Z点
        self.wait(0, 28) #（空闲）

        self.play(FadeOut(segment, LEFT), *[mob.animate.shift(LEFT) for mob in [reuleaux, incircle, points, *edges, labels, center, radius, label_r, label_o, label_d, label_x, label_ox, label_y, label_z, line_ox, line_oy, line_oz]], *[mob.animate.shift(0.5*LEFT) for mob in [condition_bc, condition_ac, condition_ab]])
        self.wait(0, 19) #接下来就是最后一步了
        self.wait(0, 20) #（空闲）

        triangle_0 = Polygon(offset, triangle_vertices[1], triangle_vertices[2], fill_opacity = 0.2, stroke_width = 0, color = RED).shift(LEFT)
        triangle_1 = Polygon(offset, triangle_vertices[2], triangle_vertices[0], fill_opacity = 0.2, stroke_width = 0, color = WHITE).shift(LEFT)
        triangle_2 = Polygon(offset, triangle_vertices[0], triangle_vertices[1], fill_opacity = 0.2, stroke_width = 0, color = BLACK).shift(LEFT)
        texts = [r"S_{\triangle ABC}", r"=S_{\triangle BOC}+S_{\triangle COA}+S_{\triangle AOB}", r"=\frac{r}{2}({BC}+{CA}+{AB})", r"\ge \frac{r}{2}(2S_{\triangle ABC}+2S_{\triangle ABC}+2S_{\triangle ABC})"]
        tex = MTex(texts[0] + r"&" + texts[1] + r"\\&" + texts[2] + r"\\&" + texts[3], isolate = texts, tex_to_color_map = {(r"{BC}", r"{CA}", r"{AB}"): GREEN, (r"S_{\triangle ABC}", r"S_{\triangle BOC}", r"S_{\triangle COA}", r"S_{\triangle AOB}"): TEAL, r"\frac{r}{2}": BLUE}).scale(0.6).shift(3.8*RIGHT+UP)
        parts_text = [tex.get_part_by_tex(text) for text in texts]
        self.play(Write(parts_text[0]))
        self.wait(0, 29) #三角形ABC的面积
        self.wait(2, 6) #除了直接计算底乘高以外
        self.bring_to_back(triangle_0, triangle_1, triangle_2).play(LaggedStart(FadeIn(triangle_0, -0.3*unit(angle_0)), FadeIn(triangle_1, -0.3*unit(angle_1)), FadeIn(triangle_2, -0.3*unit(angle_2)), run_time = 1, lag_ratio = 0.3, group = VGroup()), FadeIn(parts_text[1], 0.5*RIGHT))
        self.play(FadeIn(parts_text[2], 0.5*RIGHT))
        self.wait(0, 12) #还可以拆成三个三角形分别计算
        self.wait(0, 19) #（空闲）

        self.play(FadeIn(parts_text[3], 0.5*RIGHT))
        self.wait(1, 15) #把它们面积的表达式加起来
        conclusion = MTex(r"r\ge \frac{1}{3}", tex_to_color_map = {r"r": BLUE, r"\frac{1}{3}": BLUE}).shift(3.5*RIGHT + DOWN)
        indicate = SurroundingRectangle(conclusion)
        self.play(Write(conclusion))
        self.play(ShowCreation(indicate), *[FadeOut(mob) for mob in [tex, condition_bc, condition_ac, condition_ab, triangle_0, triangle_1, triangle_2]])
        self.wait(0, 15) #我们就能得到一个漂亮的结论
        self.play(conclusion.animate.shift(UP), indicate.animate.shift(UP))
        self.wait(1, 8) #内切圆的半径不小于1/3
        self.wait(0, 25) #（空闲）

        self.wait(1, 9) #而我们之前得到了......
        self.play(LaggedStart(Flash(label_x, flash_radius = 0.6), Flash(label_y, flash_radius = 0.6), Flash(label_z, flash_radius = 0.6), lag_ratio = 0.3, run_tme = 1.6), *[FadeOut(mob) for mob in [*edges, labels, label_d, points]], frames = 48)
        self.wait(0, 22) #......XYZ三个点
        indicate = reuleaux.copy().set_fill(opacity = 0).set_stroke(width = 8, color = WHITE).insert_n_curves(700)
        self.play(ShowPassingFlash(indicate), run_time = 2)
        self.wait(0, 26) #既然它们和内切圆都在凸集之内

        angle = np.arccos(1.8/2.2)
        line_x_1 = Line(0.75*boundary(angle_0+PI), 1.8*0.75*unit(angle_0+PI+angle)+offset, color = [PURPLE_A, BLUE]).shift(LEFT)
        line_x_2 = Line(0.75*boundary(angle_0+PI), 1.8*0.75*unit(angle_0+PI-angle)+offset, color = [PURPLE_A, BLUE]).shift(LEFT)
        line_y_1 = Line(0.75*boundary(angle_1+PI), 1.8*0.75*unit(angle_1+PI+angle)+offset, color = [PURPLE_A, BLUE]).shift(LEFT)
        line_y_2 = Line(0.75*boundary(angle_1+PI), 1.8*0.75*unit(angle_1+PI-angle)+offset, color = [PURPLE_A, BLUE]).shift(LEFT)
        line_z_1 = Line(0.75*boundary(angle_2+PI), 1.8*0.75*unit(angle_2+PI+angle)+offset, color = [PURPLE_A, BLUE]).shift(LEFT)
        line_z_2 = Line(0.75*boundary(angle_2+PI), 1.8*0.75*unit(angle_2+PI-angle)+offset, color = [PURPLE_A, BLUE]).shift(LEFT)
        region_x = ArcBetweenPoints(1.8*0.75*unit(angle_0+PI-angle)+offset, 1.8*0.75*unit(angle_0+PI+angle)+offset, 2*angle, fill_color = BLUE, fill_opacity = 0.2, stroke_width = 0).add_line_to(0.75*boundary(angle_0+PI)).close_path().shift(LEFT)
        region_y = ArcBetweenPoints(1.8*0.75*unit(angle_1+PI-angle)+offset, 1.8*0.75*unit(angle_1+PI+angle)+offset, 2*angle, fill_color = BLUE, fill_opacity = 0.2, stroke_width = 0).add_line_to(0.75*boundary(angle_1+PI)).close_path().shift(LEFT)
        region_z = ArcBetweenPoints(1.8*0.75*unit(angle_2+PI-angle)+offset, 1.8*0.75*unit(angle_2+PI+angle)+offset, 2*angle, fill_color = BLUE, fill_opacity = 0.2, stroke_width = 0).add_line_to(0.75*boundary(angle_2+PI)).close_path().shift(LEFT)
        self.bring_to_back(region_x, region_y, region_z).play(ShowCreation(VGroup(line_x_1, line_x_2, line_y_1, line_y_2, line_z_1, line_z_2)), *[FadeIn(mob, rate_func = squish_rate_func(smooth, 0.5, 1)) for mob in [region_x, region_y, region_z]], run_time = 2, lag_ratio = 0.2)
        self.wait(0, 27) #那么过XYZ分别作切线
        self.play(*[FadeOut(mob) for mob in [reuleaux, label_ox, label_r, radius, line_ox, line_oy, line_oz]])
        self.wait(1, 11) #围成的区域自然也在凸集之内
        self.wait(0, 22) #（空闲）

        area = MTex(r"S(r)=\pi r^2+3r\sqrt{1-2r}-3r^2\arccos\frac{r}{1-r}", tex_to_color_map = {r"S": PURPLE_A, r"r": BLUE}).scale(0.8).shift(2.4*UP)
        arrow_x = Arrow(0.5*LEFT, 2*RIGHT, buff = 0, stroke_width = 3)
        arrow_y = Arrow(0.5*DOWN, 3*UP, buff = 0, stroke_width = 3)
        tip_x = MTex(r"r", color = BLUE).scale(0.6).next_to(arrow_x, RIGHT)
        tip_y = MTex(r"S(r)", color = PURPLE_A).scale(0.6).next_to(arrow_y, UP)
        function_area = lambda t: t**2*(PI-3*np.arccos(t/(1-t))) + 3*t*np.sqrt(1-2*t)
        graph_grey = FunctionGraph(function_area, [0, 1/3, 1/300], color = GREY, stroke_width = 3).scale(3, about_point = ORIGIN)
        graph_white = FunctionGraph(function_area, [1/3, 1/2, 1/300]).scale(3, about_point = ORIGIN)
        point = Dot(1.35*RIGHT+3*function_area(0.45)*UP).shift(2*DOWN + 5.5*LEFT)
        coordinate = VGroup(arrow_x, arrow_y, tip_x, tip_y, graph_grey, graph_white).shift(2*DOWN + 5.5*LEFT)
        updating_all = VGroup(label_x, label_y, label_z, incircle, line_x_1, line_x_2, line_y_1, line_y_2, line_z_1, line_z_2, region_x, region_y, region_z, center, label_o)
        self.remove(label_x, label_y, label_z, incircle, line_x_1, line_x_2, line_y_1, line_y_2, line_z_1, line_z_2, region_x, region_y, region_z, center, label_o).add(updating_all)
        self.play(FadeIn(area, RIGHT), updating_all.animate.shift(RIGHT + DOWN - offset), FadeIn(coordinate, 0.5*UP), FadeIn(point))
        self.wait(0, 18) #这个区域的面积
        theta_0 = ValueTracker(angle_0)
        theta_1 = ValueTracker(angle_1)
        theta_2 = ValueTracker(angle_2)
        beta = ValueTracker(1.35)
        def updating(mob: VGroup):
            angle_0 = theta_0.get_value()
            angle_1 = theta_1.get_value()
            angle_2 = theta_2.get_value()
            offset = DOWN
            radius = beta.get_value()
            angle = np.arccos(radius/(3-radius))
            position_x, position_y, position_z = offset - (3-radius)*unit(angle_0), offset - (3-radius)*unit(angle_1), offset - (3-radius)*unit(angle_2)
            tangencies = [offset - radius*unit(angle_0-angle), offset - radius*unit(angle_0+angle), offset - radius*unit(angle_1-angle), offset - radius*unit(angle_1+angle), offset - radius*unit(angle_2-angle), offset - radius*unit(angle_2+angle)]
            mob[0].next_to(position_x, UP, buff = 0.15)
            mob[1].next_to(position_y, LEFT)
            mob[2].next_to(position_z, RIGHT)
            mob[3].set_points(Circle(radius = radius).shift(offset).get_all_points())
            mob[4].put_start_and_end_on(position_x, tangencies[0])
            mob[5].put_start_and_end_on(position_x, tangencies[1])
            mob[6].put_start_and_end_on(position_y, tangencies[2])
            mob[7].put_start_and_end_on(position_y, tangencies[3])
            mob[8].put_start_and_end_on(position_z, tangencies[4])
            mob[9].put_start_and_end_on(position_z, tangencies[5])
            mob[10].set_points(ArcBetweenPoints(tangencies[0], tangencies[1], 2*angle).add_line_to(position_x).close_path().get_all_points())
            mob[11].set_points(ArcBetweenPoints(tangencies[2], tangencies[3], 2*angle).add_line_to(position_y).close_path().get_all_points())
            mob[12].set_points(ArcBetweenPoints(tangencies[4], tangencies[5], 2*angle).add_line_to(position_z).close_path().get_all_points())
        updating_all.add_updater(updating)
        def point_updater(mob: Dot):
            value = beta.get_value()/3
            mob.move_to(3*(value*RIGHT+function_area(value)*UP)).shift(2*DOWN + 5.5*LEFT)
        point.add_updater(point_updater)
        self.play(beta.animate.set_value(1.5), theta_0.animate.set_value(-PI/2), theta_1.animate.set_value(PI/6), theta_2.animate.set_value(5*PI/6), run_time = 2) #是随着半径增加而增加的
        self.wait(0, 18) #（空闲）

        self.play(beta.animating(run_time = 3).set_value(1), self.change_notice())
        updating_all.clear_updaters()
        point.clear_updaters()
        triangle = Polygon(UP, 2*DOWN+np.sqrt(3)*LEFT, 2*DOWN+np.sqrt(3)*RIGHT, stroke_width = 8)
        self.play(ShowPassingFlash(triangle), run_time = 2)
        self.wait(2+2-5, 26+10) #当半径取到最小值1/3的时候 它正好就变成了一个正三角形
        self.wait(0, 14) #（空闲）

        self.wait(1, 8) #也就是说
        self.wait(3, 26) #正三角形的面积 是所有凸挂谷集中最小的
        self.wait(2, 12)
        self.fade_out(end = True)
        self.wait(2, 0) #到此共110秒

#################################################################### 

class Chapter2_0(FrameScene):

    def construct(self):

        text2 = Text("第二节 小转动与累计面积", font = 'simsun', t2c={"第二节": YELLOW, "小转动": GREEN, "累计面积": BLUE})

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(FrameScene):
    def construct(self):
        self.notices = [Notice("趣味几何", "请　思考"),
                        Notice("错误思路", "请勿模仿")]
        self.notice = self.notices[0]

        line = Line(5*LEFT+UP, LEFT+UP, stroke_width = 8)
        rectangle = Polygon(5*LEFT+UP, LEFT+UP, LEFT+DOWN, 5*LEFT+DOWN, color = YELLOW, fill_opacity = 0.2).save_state().set_height(0, stretch = True).shift(UP)
        self.play(ShowCreation(line), Write(self.notice))
        self.bring_to_back(rectangle).play(line.animate.shift(2*DOWN), rectangle.animate.restore())
        self.wait(1, 10) #一条线段如果垂直于它自己的方向平移
        self.wait(2, 0) #那么它会扫过一个长方形
        self.wait(0, 21) #（空闲）

        line_horizontal = Line(5*LEFT+DOWN, LEFT+DOWN, color = YELLOW)
        self.bring_to_back(line_horizontal).play(line.animate.shift(6*RIGHT), line_horizontal.animate.put_start_and_end_on(5*LEFT+DOWN, 5*RIGHT+DOWN), run_time = 2)
        self.wait(0, 24) #但它要是顺着自己的方向平移
        self.wait(3, 9) #就只会在平面上留下一道面积为0的轨迹
        self.wait(0, 24) #（空闲）

        self.play(*[FadeOut(mob, 0.5*(2*UP+3*LEFT), rate_func = rush_into) for mob in [rectangle, line_horizontal]], line.animating(run_time = 2).shift(2*UP+3*LEFT))
        self.wait(0, 17) #这就带来了一个很自然的思路
        angle = np.arctan(8/15) + np.arctan(2/17)
        arc = Arc(radius = 17, start_angle = PI/2-angle, angle = 2*angle, color = YELLOW, n_components = 64).shift(16*DOWN)
        self.bring_to_back(arc).play(ShowCreation(arc))
        line.counter = 0
        alpha = ValueTracker(0.0)
        lines = []
        def line_updater(mob: Line):
            angle = alpha.get_value()
            def start_func(t: float):
                return 16*DOWN + 17*unit(PI/2+t)+2*unit(t)
            def end_func(t: float):
                return 16*DOWN + 17*unit(PI/2+t)-2*unit(t)
            mob.put_start_and_end_on(start_func(angle), end_func(angle))
            critical = mob.counter*TAU/180
            while angle >= critical:
                thinline = Line(start_func(critical), end_func(critical), color = GREY_A, stroke_width = 2)
                self.bring_to_back(thinline)
                lines.append(thinline)
                mob.counter += 1
                critical = mob.counter*TAU/180
        line.add_updater(line_updater)
        self.play(alpha.animate.set_value(angle), rate_func = rush_into)
        line.counter = -line.counter
        left_lines = lines
        lines = []
        alpha.set_value(-angle)
        self.play(alpha.animate.set_value(0), rate_func = rush_from)
        line.clear_updaters()
        group_lines = VGroup(*lines, *left_lines)
        self.wait(0, 21) #如果我们让线段切着一个尽可能大的圆旋转
        outer_arc = Arc(radius = np.sqrt(293), start_angle = PI/2-angle, angle = 2*angle, color = YELLOW, n_components = 64).shift(16*DOWN)
        annulus = outer_arc.copy().set_stroke(width = 0).set_fill(opacity = 0.2).add_line_to(arc.get_points()[-1]).append_points(arc.get_points()[::-1]).close_path().rotate(-2*angle, about_point = 16*DOWN)
        self.bring_to_back(annulus, group_lines).add(outer_arc, line).play(ShowCreation(outer_arc), FadeOut(group_lines, lag_ratio = 1), Rotate(annulus, 2*angle, about_point = 16*DOWN), run_time = 2)
        self.wait(0, 29) #它划过的轨迹宽度就能尽可能小
        group_all = VGroup(annulus, arc, outer_arc, line)
        self.add(group_all).play(group_all.animate.stretch(0.05, 1, about_point = UP), run_time = 2)
        self.wait(0, 6) #这样面积不就可以到0了吗
        self.wait(0, 18) #（空闲）

        self.remove(group_all).add(arc, outer_arc, line).play(Uncreate(arc), Uncreate(outer_arc), self.change_notice())
        self.wait(1, 6) #很可惜 这样到不了0
        self.wait(0, 18) #（空闲）

        inner_circle = Circle(radius = 1.5, stroke_color = YELLOW, fill_color = BACK, fill_opacity = 1)
        outer_circle = Circle(radius = 2.5, color = YELLOW, fill_opacity = 0.2)
        self.bring_to_back(outer_circle, inner_circle, self.shade).play(FadeOut(self.shade, rate_func = rush_into), line.animate.shift(0.5*UP))
        self.wait(1, 17) #线段切着一个圆旋转的时候
        outer_radius = Line(ORIGIN, 2*LEFT+1.5*UP)
        inner_radius = Line(ORIGIN, 1.5*UP)
        label_R = MTex(r"R").scale(0.8).next_to(outer_radius.get_center(), DL, buff = 0.15)
        label_r = MTex(r"r").scale(0.8).next_to(inner_radius.get_center(), RIGHT)
        label_l = MTex(r"1").scale(0.8).next_to(line.get_center(), UP)
        self.play(ShowCreation(outer_radius), ShowCreation(inner_radius), *[Write(mob) for mob in [label_R, label_r, label_l]])
        self.wait(1, 14) #扫过的区域是一个圆环

        updating = VGroup(outer_circle, inner_circle, outer_radius, inner_radius, line, label_R, label_r, label_l)
        alpha = ValueTracker(1.5)
        def all_updater(mob: VGroup):
            r = alpha.get_value()
            R = np.sqrt(r**2 + 4)
            mob[0].set_points(Circle(radius = R).get_points())
            mob[1].set_points(Circle(radius = r).get_points())
            mob[2].put_start_and_end_on(ORIGIN, 2*LEFT + r*UP)
            mob[3].put_start_and_end_on(ORIGIN, r*UP)
            mob[4].put_start_and_end_on(2*LEFT + r*UP, 2*RIGHT + r*UP)
            mob[5].next_to(outer_radius.get_center(), DL, buff = 0.15)
            mob[6].next_to(inner_radius.get_center(), RIGHT)
            mob[7].next_to(line.get_center(), UP)
        updating.add_updater(all_updater)
        self.remove(line, inner_circle, outer_circle, outer_radius, inner_radius, label_R, label_r, label_l).add(updating).play(alpha.animate.set_value(2), run_time = 2)
        updating.clear_points()
        self.remove(updating).add(outer_circle, inner_circle, outer_radius, inner_radius, label_R, label_r, label_l, line).wait(1, 16) #这个圆环内径和外径的差虽然会越来越小

        squares = MTex(r"R^2=r^2+\left(\frac{1}{2}\right)^2", tex_to_color_map = {(r"R", r"r"): YELLOW}).scale(0.8).next_to(6.5*LEFT+1.5*UP)
        self.play(Write(squares))
        self.wait(1, 22) #但它们的平方差却始终是1/4
        self.wait(0, 17) #（空闲）

        area = MTex(r"S=\pi R^2-\pi r^2=\frac{\pi}{4}", tex_to_color_map = {(r"S"): TEAL, (r"R", r"r"): YELLOW}).scale(0.8).next_to(6.5*LEFT, buff = 0)
        self.play(Write(area))
        self.wait(0, 20) #无论圆环有多大
        self.wait(2, 10) #它的面积始终都是π/4
        self.wait(0, 19) #（空闲）

        line.counter = 0
        alpha = ValueTracker(0.0)
        lines = []
        def line_updater(mob: Line):
            angle = alpha.get_value()
            def start_func(t: float):
                return 2*unit(PI/2-t)+2*unit(-t)
            def end_func(t: float):
                return 2*unit(PI/2-t)-2*unit(-t)
            mob.put_start_and_end_on(start_func(angle), end_func(angle))
            critical = mob.counter*TAU/90
            while angle >= critical:
                thinline = Line(start_func(critical), end_func(critical), color = GREY, stroke_width = 1)
                self.bring_to_back(thinline)
                lines.append(thinline)
                mob.counter += 1
                critical = mob.counter*TAU/90
        line.add_updater(line_updater)
        self.play(alpha.animate.set_value(PI), run_time = 2)
        self.wait(0, 3) #而线段转过半圈时

        outer_circle.set_fill(opacity = 0)
        covered_half = Arc(radius = 2, start_angle = -PI/2, angle = PI, stroke_width = 0, color = YELLOW, fill_opacity = 0.2, n_components = 24).add_line_to(2*UP+2*LEFT).append_points(Arc(radius = 2*np.sqrt(2), start_angle = PI*3/4, angle = -PI*3/2, n_components = 24).get_points())
        uncovered_half = Arc(radius = 2, start_angle = PI/2, angle = PI, stroke_width = 0, color = YELLOW, fill_opacity = 0.2, n_components = 24).add_line_to(2*DOWN+2*LEFT).append_points(Arc(radius = 2*np.sqrt(2), start_angle = -PI*3/4, angle = -PI/2, n_components = 24).get_points())
        self.bring_to_back(uncovered_half, covered_half).play(FadeOut(uncovered_half))
        self.wait(1, 12) #至少也要扫过圆环的一半
        self.wait(1, 29) #也就是π/8的面积
        self.wait(0, 27) #（空闲）
        
        self.fade_out()
        self.wait(0, 14) #不只是圆环
        position_back = lambda t: np.array([t, 2*t**3/27+7*t**2/9+14*t/9-11/27, 0])
        position_fore = lambda t: position_back(t) + 3*unit(np.arctan(2*t**2/9+14*t/9+14/9))
        line = Line(position_fore(-9), position_back(-9), stroke_width = 8)
        line.counter = -90
        alpha = ValueTracker(-9.0)
        lines = []
        def line_updater(mob: Line):
            angle = alpha.get_value()
            mob.put_start_and_end_on(position_fore(angle), position_back(angle))
            critical = mob.counter*0.1
            while angle >= critical:
                thinline = Line(position_fore(critical), position_back(critical), color = WHITE, stroke_width = 1)
                self.bring_to_back(thinline)
                lines.append(thinline)
                mob.counter += 1
                critical = mob.counter*0.1
        line.add_updater(line_updater)
        self.add(line).play(alpha.animate.set_value(2.0), run_time = 4)
        self.wait(2+1-4, 27+26) #所有让线段去跑很远的一圈的思路 对应的面积都不是很小
        self.wait(0, 16) #（空闲）
        self.wait(4, 18)
        self.fade_out() #到此共64秒

class Chapter2_2(FrameScene):
    def construct(self):
        self.notices = [Notice("错误思路", "请勿模仿"), 
                        Notice("微元分析", "请　模仿"),
                        Notice("简单函数", "请　显然"),
                        Notice("重要观察", "请记笔记"),
                        Notice("简单例子", "请　熟悉")]
        self.notice = self.notices[0]

        position_a, position_b = 2*LEFT + UP, 2*RIGHT + UP
        position_o = 4*RIGHT+DOWN
        line = Line(position_a, position_b, stroke_width = 8)
        line_copy = line.copy()
        self.play(ShowCreation(line), self.change_notice())
        self.play(Rotate(line_copy, -PI/12, about_point = position_o))
        self.wait(0, 27) #当线段转动了一个小角度的时候
        position_c, position_d = line_copy.get_start(), line_copy.get_end()

        point_o = Dot(position_o, color = YELLOW)
        label_o = MTex(r"O").scale(0.8).next_to(position_o, DOWN)
        label_a = MTex(r"A").scale(0.8).next_to(position_a, DL, buff = 0.15).shift(0.1*RIGHT)
        label_b = MTex(r"B").scale(0.8).next_to(position_b, DL, buff = 0.15).shift(0.1*RIGHT)
        label_c = MTex(r"C").scale(0.8).next_to(position_c, UP)
        label_d = MTex(r"D").scale(0.8).next_to(position_d, UP)
        arc_ac = ArcBetweenPoints(position_a, position_c, -PI/12, color = YELLOW)
        arc_bd = ArcBetweenPoints(position_b, position_d, -PI/12, color = YELLOW)
        self.play(ShowCreation(point_o), ShowCreation(arc_ac), ShowCreation(arc_bd), Write(VGroup(label_o, label_a, label_b, label_c, label_d), run_time = 2, lag_ratio = 0.2))
        self.wait(0, 23) #我们可以认为它近似在绕一个定点转动
        self.wait(0, 22) #（空闲）

        line_ac = Line(position_a, position_c, color = GREY)
        line_bd = Line(position_b, position_d, color = GREY)
        m_ac, m_bd = (position_a+position_c)/2, (position_b+position_d)/2
        direction_ac, direction_bd = (m_ac-position_o)/get_norm(m_ac-position_o), (m_bd-position_o)/get_norm(m_bd-position_o)
        bisector_ac = DashedLine(m_ac+0.5*direction_ac, position_o-0.5*direction_ac, color = GREY)
        bisector_bd = DashedLine(m_bd+0.5*direction_bd, position_o-0.5*direction_bd, color = GREY)
        group_lines = VGroup(*[Line(position_o, position) for position in [position_a, position_b, position_c, position_d]])
        self.bring_to_back(line_ac, line_bd).play(ShowCreation(line_ac), ShowCreation(line_bd))
        self.play(ShowCreation(bisector_ac), ShowCreation(bisector_bd))
        self.add(group_lines, arc_ac, arc_bd, point_o).play(*[FadeOut(mob) for mob in [line_ac, line_bd, bisector_ac, bisector_bd]], ShowCreation(group_lines, lag_ratio = 0.2, run_time = 1.5), frames = 45)
        region = arc_ac.copy().set_stroke(width = 0).set_fill(opacity = 0.2).add_line_to(position_d).append_points(arc_bd.get_points()[::-1]).close_path()
        triangle_oab = Polygon(position_o, position_a, position_b, color = YELLOW, stroke_width = 0, fill_opacity = 0.2)
        small_sector = arc_bd.copy().set_stroke(width = 0).set_fill(opacity = 0.2).add_line_to(position_o).close_path()
        triangle_ocd = Polygon(position_o, position_c, position_d, color = BLUE, stroke_width = 0, fill_opacity = 0.2)
        big_sector = arc_ac.copy().set_stroke(width = 0).set_fill(opacity = 0.2, color = BLUE).add_line_to(position_o).close_path()
        self.bring_to_back(region, triangle_oab, small_sector, triangle_ocd, big_sector).play(*[FadeIn(mob) for mob in [region, triangle_oab, small_sector, triangle_ocd, big_sector]])
        self.wait(2+2-4, 15+17-15) #分别连接AC和BD 点O就在这两条线段的中垂线上
        self.wait(0, 21) #（空闲）

        plus_sign = MTex(r"+").scale(0.8)
        equals_sign = MTex(r"=").scale(0.8)
        minus_sign = MTex(r"-").scale(0.8)
        symbols = VGroup(plus_sign.copy().move_to(3*UP+3*LEFT), plus_sign.copy().move_to(3*UP+LEFT), equals_sign.copy().move_to(3*UP+RIGHT), plus_sign.copy().move_to(3*UP+3*RIGHT))
        self.play(triangle_oab.animate.shift(0.5*DL+0.5*DOWN), small_sector.animate.shift(0.5*DR), *[mob.animate.shift(0.5*DOWN) for mob in [label_a, label_b, label_c, label_d, label_o, point_o, line, line_copy, arc_ac, arc_bd, big_sector, triangle_ocd, group_lines]])
        self.play(region.animate.scale(0.25).move_to(3*UP + 4*LEFT).set_fill(opacity = 1), triangle_oab.animate.scale(0.25).move_to(3*UP + 2*LEFT).set_fill(opacity = 1), small_sector.animate.scale(0.25).move_to(3*UP).set_fill(opacity = 1), big_sector.animate.shift(0.5*DL), triangle_ocd.animate.shift(0.5*DR), *[mob.animate.shift(0.5*DOWN) for mob in [label_a, label_b, label_c, label_d, label_o, point_o, line, line_copy, arc_ac, arc_bd, group_lines]])
        self.play(big_sector.animate.scale(0.25).move_to(3*UP + 2*RIGHT).set_fill(opacity = 1), triangle_ocd.animate.scale(0.25).move_to(3*UP + 4*RIGHT).set_fill(opacity = 1), Write(symbols))

        angle_oa, angle_ob, angle_oc, angle_od = [angle_of_vector(position-position_o) for position in [position_a, position_b, position_c, position_d]]
        angle_arc_ac = Arc(radius = 1, start_angle = angle_oc, angle = angle_oa-angle_oc).shift(position_o + DOWN + 1.5*RIGHT)
        angle_arc_bd = Arc(radius = 1, start_angle = angle_od, angle = angle_ob-angle_od).shift(position_o + DOWN + 1.5*RIGHT)
        dtheta = MTex(r"d\theta").scale(0.5)
        dtheta_ac = dtheta.copy().move_to(position_o + 1.25*unit((angle_oa+angle_oc)/2) + DOWN + 1.5*RIGHT)
        dtheta_bd = dtheta.copy().move_to(position_o + 1.25*unit((angle_ob+angle_od)/2) + DOWN + 1.5*RIGHT)
        equation = VGroup(region.copy(), equals_sign.copy(), big_sector.copy(), minus_sign.copy(), small_sector.copy()).arrange().next_to(1.5*UP + 6.5*LEFT, buff = 0)
        equation_2 = MTex(r"=\frac{d\theta}{2}(|OA|^2-|OB|^2)").scale(0.8)
        equation_2.shift(equation[1].get_center() - equation_2[0].get_center() + DOWN)
        self.play(FadeIn(equation, 0.5*RIGHT), *[FadeIn(mob, 1.5*RIGHT) for mob in [angle_arc_ac, angle_arc_bd, dtheta_ac, dtheta_bd]], *[mob.animate.shift(1.5*RIGHT) for mob in [label_a, label_b, label_c, label_d, label_o, point_o, line, line_copy, arc_ac, arc_bd, group_lines]])
        self.play(Write(equation_2), run_time = 1)
        self.wait(1+1+2-5, 11+28+4) #通过割补法 扫过的这一小段的面积 就等于两个扇形面积的差
        self.wait(0, 19) #（空闲）

        for position in [position_o, position_a, position_b, position_c, position_d]:
            position += DOWN + 1.5*RIGHT
        position_h = 5.5*RIGHT
        line_bh = DashedLine(position_b, position_h)
        line_oh = Line(position_o, position_h)
        label_h = MTex(r"H").scale(0.8).next_to(position_h, UP)
        self.add(line_bh, line_oh, point_o).play(ShowCreation(line_bh), ShowCreation(line_oh), *[FadeOut(mob) for mob in [region, triangle_oab, small_sector, triangle_ocd, big_sector, symbols]])
        self.play(Write(label_h))
        self.wait(0, 13) #再从O点向AB作垂线
        text_ah = MTex(r"AH=a", tex_to_color_map = {r"a": TEAL}).scale(0.8).next_to(3*UP + 5*LEFT)
        formula = MTex(r"\frac{dS}{d\theta}=\frac{a^2-(a-1)^2}{2}", tex_to_color_map = {r"dS": YELLOW, r"a": TEAL}).scale(0.8).next_to(3*UP + LEFT).save_state()
        self.play(Write(text_ah))
        self.play(FadeIn(formula, 0.5*RIGHT))
        lines = group_lines.submobjects
        self.remove(group_lines).add(*lines, arc_ac, arc_bd, point_o
                ).play(label_a.animate.next_to(position_a, UP), label_b.animate.next_to(position_b, UP), 
                       *[FadeOut(mob) for mob in [equation, equation_2, label_c, label_d, line_copy, lines[2], lines[3], arc_ac, arc_bd, angle_arc_ac, angle_arc_bd, dtheta_ac, dtheta_bd]])
        self.wait(1+3-3, 29+5) #设出AH的长度 那么面积就可以进一步写成用a表示的形式
        self.wait(0, 20) #（空闲）

        updating_all = VGroup(point_o, label_o, lines[0], lines[1], line_bh, line_oh, label_h).set_style(stroke_background = True)
        alpha = ValueTracker(5.5)
        def all_updater(mob: VGroup):
            value = alpha.get_value()
            point_o = value*RIGHT + 2*DOWN
            point_h = value*RIGHT
            mob[0].move_to(point_o)
            mob[1].next_to(point_o, DOWN)
            mob[2].put_start_and_end_on(position_a, point_o)
            mob[3].put_start_and_end_on(position_b, point_o)
            mob[4].set_points(DashedLine(position_b, point_h).get_all_points())
            mob[5].put_start_and_end_on(point_o, point_h)
            mob[6].next_to(point_h, UP)
        line_bh.set_submobjects([])
        updating_all.add_updater(all_updater)
        self.remove(point_o, label_o, lines[0], lines[1], line_bh, line_oh, label_h).add(updating_all).play(alpha.animate.set_value(2), formula.animate.set_color(GREY))
        updating_all.clear_updaters()
        self.remove(updating_all).add(label_o, lines[0], lines[1], line_oh, label_h, point_o)
        self.wait(1, 8) #要是H在线段AB内部
        formula_2 = MTex(r"\frac{dS}{d\theta}=\frac{a^2+(a-1)^2}{2}", tex_to_color_map = {r"\frac{dS}{d\theta}": YELLOW, r"a": TEAL}).scale(0.8).next_to(2*UP + LEFT)
        self.play(FadeIn(formula_2, 0.5*RIGHT))
        self.wait(0, 16) #也会有类似的表达
        self.wait(0, 17) #（空闲）

        formula_area = MTex(r"\frac{dS}{d\theta}=\frac{a|a|+(1-a)|1-a|}{2}", tex_to_color_map = {r"\frac{dS}{d\theta}": YELLOW, r"a": TEAL}).scale(0.8).next_to(2.5*UP + LEFT)
        self.play(FadeIn(formula_area), FadeOut(formula, 0.5*DOWN), FadeOut(formula_2, 0.5*UP), self.change_notice())
        self.wait(0, 11) #综合到一起
        arrow_x = Arrow(1.5*LEFT, 2.5*RIGHT, buff = 0, stroke_width = 3)
        arrow_y = Arrow(0.5*DOWN, 2*UP, buff = 0, stroke_width = 3)
        tip_x = MTex(r"a", color = TEAL).scale(0.6).next_to(arrow_x, RIGHT)
        tip_y = MTex(r"\frac{dS}{d\theta}", color = YELLOW).scale(0.6).next_to(arrow_y, UP)
        function_area = lambda t: (t*abs(t) + (1-t)*abs(1-t))/2
        graph = FunctionGraph(function_area, [-1, 2, 0.01], color = WHITE)
        point = Dot(np.array([5/8, function_area(5/8), 0]), color = YELLOW).shift(1.5*DOWN + 4.5*LEFT)
        coordinate = VGroup(arrow_x, arrow_y, tip_x, tip_y, graph).shift(1.5*DOWN + 4.5*LEFT)
        self.play(FadeIn(coordinate, 0.5*UP), FadeIn(point, 0.5*UP), formula_area.animate.next_to(2*UP + 6*LEFT))
        self.wait(1, 21) #我们就能得到面积关于a的表达式
        self.wait(0, 16) #（空闲）

        updating_all = VGroup(point_o, label_o, lines[0], lines[1], line_oh).set_style(stroke_background = True)
        alpha = ValueTracker(2)
        def all_updater(mob: VGroup):
            value = alpha.get_value()
            point_o = 2*RIGHT + value*DOWN
            point_h = 2*RIGHT
            mob[0].move_to(point_o)
            mob[1].next_to(point_o, DOWN)
            mob[2].put_start_and_end_on(position_a, point_o)
            mob[3].put_start_and_end_on(position_b, point_o)
            mob[4].put_start_and_end_on(point_o, point_h)
        updating_all.add_updater(all_updater)
        self.remove(point_o, label_o, lines[0], lines[1], line_oh).add(updating_all).play(alpha.animate.set_value(2.4), run_time = 0.5)
        self.play(alpha.animate.set_value(0), run_time = 1.5)
        updating_all.clear_updaters()
        self.remove(updating_all).add(label_o, point_o)
        self.wait(1, 9) #这个面积只和H在AB上的位置有关
        updating_all = VGroup(point_o, label_o, label_h, point).set_style(stroke_background = True)
        alpha = ValueTracker(2)
        def all_updater(mob: VGroup):
            value = alpha.get_value()
            point = value*RIGHT
            mob[0].move_to(point)
            mob[1].next_to(point, DOWN)
            mob[2].next_to(point, UP)
            ratio = (value+0.5)/4
            mob[3].move_to(np.array([ratio, function_area(ratio), 0]) + 1.5*DOWN + 4.5*LEFT)
        updating_all.add_updater(all_updater)
        self.remove(point_o, label_o, label_h, point).add(updating_all).play(alpha.animating(run_time = 2).set_value(3.5), label_a.animate.next_to(position_a, UL), label_b.animate.next_to(position_b, UR))
        self.wait(0, 7) #H越远离AB的中点
        self.wait(0, 16) #扫过的面积越大
        self.wait(0, 21) #（空闲）
        self.play(alpha.animating(run_time = 2).set_value(1.5))
        updating_all.clear_updaters()
        self.remove(updating_all).add(point_o, label_o, label_h, point)
        self.wait(0, 18) #当H恰好为AB中点时

        dashed_line_y = DashedLine(np.array([1/2, 1/4, 0]), np.array([0, 1/4, 0])).shift(1.5*DOWN + 4.5*LEFT)
        minimal_y = MTex(r"\frac{1}{4}").scale(0.4).next_to(dashed_line_y, LEFT, buff = 0.1)
        dashed_line_x = DashedLine(np.array([1/2, 1/4, 0]), np.array([1/2, 0, 0])).shift(1.5*DOWN + 4.5*LEFT)
        minimal_x = MTex(r"\frac{1}{2}").scale(0.4).next_to(dashed_line_x, DOWN, buff = 0.1)
        self.add(dashed_line_y, dashed_line_x, point).play(ShowCreation(dashed_line_y), ShowCreation(dashed_line_x))
        self.play(Write(minimal_y), Write(minimal_x))
        self.wait(2, 1) #面积取到θ/4的极小值
        
        circle = Circle(radius = 2, stroke_width = 0, color = YELLOW, fill_opacity = 0.2).shift(1.5*RIGHT)
        upper_half = Arc(radius = 2, color = YELLOW, start_angle = 0, angle = PI, n_components = 24).shift(1.5*RIGHT)
        lower_half = Arc(radius = 2, color = YELLOW, start_angle = PI, angle = PI, n_components = 24).shift(1.5*RIGHT)
        self.add(upper_half, lower_half, line, point_o).play(ShowCreation(upper_half), ShowCreation(lower_half), Rotate(line, PI, about_point = 1.5*RIGHT), run_time = 2)
        self.bring_to_back(circle).play(FadeIn(circle))
        self.remove(upper_half, lower_half)
        circle.set_stroke(width = 4)
        self.wait(0, 12) #这样 当AB累计转过180°时
        s_circle = MTex(r"S=\frac{\pi}{4}\approx0.785").scale(0.8).shift(1.5*RIGHT)
        s_circle.shift((3-s_circle[1].get_y())*UP)
        self.play(Write(s_circle))
        self.wait(1, 22) #AB累计扫过的面积就为π/4
        self.wait(0, 17) #（空闲）

        self.play(*[FadeOut(mob) for mob in [label_a, label_b, label_h, label_o, point_o, text_ah, formula_area, coordinate, point, dashed_line_y, dashed_line_x, minimal_y, minimal_x, line]])
        self.wait(1, 13) #这正好就是直径为1的圆的面积
        self.wait(0, 18) #（空闲）

        triangle = Polygon(1.5*UP, 1.5*DOWN+np.sqrt(3)*LEFT, 1.5*DOWN+np.sqrt(3)*RIGHT, color = YELLOW, fill_opacity = 0.2).shift(0.5*DOWN)
        s_triangle = MTex(r"S=\frac{\sqrt3}{3}\approx0.577").scale(0.8)
        s_triangle.shift((1.75-s_triangle[1].get_y())*UP)
        func = lambda t: np.array([np.sin(2*t)-2*np.sin(t), np.cos(2*t)+2*np.cos(t), 0])
        deltoid = ParametricCurve(func, [-PI/2, PI*3/2, TAU/100], color = YELLOW, fill_opacity = 0.2).shift(4*LEFT+1.25*DOWN).scale(0.75)
        s_deltoid = MTex(r"S=\frac{\pi}{8}\approx0.393").scale(0.8).shift(4*LEFT)
        s_deltoid.shift((1.75-s_deltoid[1].get_y())*UP)
        self.play(circle.animating(run_time = 2).scale(0.75).move_to(4*RIGHT+0.5*DOWN), s_circle.animating(run_time = 2).shift(2.5*RIGHT + 1.25*DOWN), 
                  FadeIn(triangle, 3.5*RIGHT, scale = 0.75, run_time = 2), FadeIn(s_triangle, 3.5*RIGHT + DOWN, run_time = 2), 
                  FadeIn(deltoid, 4.5*RIGHT, scale = 0.75, run_time = 2), FadeIn(s_deltoid, 4.5*RIGHT + DOWN, run_time = 2), self.change_notice()) #当然 我们也知道
        self.wait(2, 1) #圆不是面积最小的挂谷集
        self.wait(0, 16) #（空闲）
        self.wait(3, 4) #而其它挂谷集之所以面积能比圆小
        self.wait(2, 21) #原因就在于它们重复扫过了一些区域
        self.wait(0, 17) #（空闲）
        self.wait(1, 20) #在挂谷问题中
        title = Title("面积重叠")
        title_line = TitleLine()
        self.play(FadeIn(title, DOWN), GrowFromPoint(title_line, 4*UP))
        self.wait(2, 8) #“怎么重叠”是比“怎么旋转”更重要的事情
        self.wait(0, 16) #到此共75秒
        self.fade_out(excepts = [title, title_line], change_notice = True)

class Chapter2_3(FrameScene):
    def construct(self):
        self.notices = [Notice("简单例子", "请　熟悉")]
        self.notice = self.notices[0]
        self.frames = 30
        title = Title("面积重叠")
        title_line = TitleLine()
        inner_circle = Circle(radius = 2, stroke_color = YELLOW)
        outer_circle = Circle(radius = 2*np.sqrt(2), color = YELLOW)
        line = Line(2*UP+2*LEFT, 2*UP+2*RIGHT, stroke_width = 8).add(Dot(2*UP, color = TEAL)).set_stroke(background = True)
        text_ah = MTex(r"a=\frac{1}{2}", tex_to_color_map = {r"a": TEAL}).scale(0.8).next_to(2*UP + 5.5*LEFT)
        text_s = MTex(r"S_{\text{累计}}=\frac{\pi}{4}", tex_to_color_map = {r"S_{\text{累计}}": YELLOW}).scale(0.8)
        text_s.shift(text_ah[1].get_center() - text_s[3].get_center() + DOWN)
        self.fade_in(inner_circle, outer_circle, line, excepts = [self.notice, title, title_line]).wait(0, 4) #我们来看几个例子吧
        line.counter = 0
        alpha = ValueTracker(0.0)
        lines = []
        def line_updater(mob: Line):
            angle = alpha.get_value()
            def start_func(t: float):
                return 2*unit(PI/2-t)+2*unit(-t)
            def end_func(t: float):
                return 2*unit(PI/2-t)-2*unit(-t)
            mob.put_start_and_end_on(start_func(angle), end_func(angle))
            critical = mob.counter*TAU/90
            while angle >= critical:
                thinline = Line(start_func(critical), end_func(critical), color = WHITE, stroke_width = 1)
                self.bring_to_back(thinline)
                lines.append(thinline)
                mob.counter += 1
                critical = mob.counter*TAU/90
        line.add_updater(line_updater)
        self.play(alpha.animating(run_time = 2).set_value(PI), Write(text_ah))
        line.clear_updaters()
        self.wait(0, 23) #当线段在圆环中旋转的时候
        self.play(Write(text_s))
        self.wait(1, 8) #它会累计扫过π/4的面积
        self.wait(0, 21) #（空闲）

        union = Arc(radius = 2, start_angle = -PI/2, angle = PI, stroke_width = 0, color = YELLOW, fill_opacity = 0.2, n_components = 24).add_line_to(2*UP+2*LEFT).append_points(Arc(radius = 2*np.sqrt(2), start_angle = PI*3/4, angle = -PI*3/2, n_components = 24).get_points())
        intersection = Arc(radius = 2, start_angle = -PI/2, angle = PI, stroke_width = 0, color = RED, fill_opacity = 0.2, n_components = 24).add_line_to(2*UP+2*RIGHT).append_points(Arc(radius = 2*np.sqrt(2), start_angle = PI/4, angle = -PI/2, n_components = 24).get_points())
        line_1, line_2 = Line(2*UP+2*LEFT, 2*UP+2*RIGHT).save_state().rotate(-PI/3, about_point = ORIGIN), Line(2*UP+2*LEFT, 2*UP+2*RIGHT).save_state().rotate(-2*PI/3, about_point = ORIGIN)
        dot = Dot(4/np.sqrt(3)*RIGHT, color = RED)
        self.bring_to_back(union, intersection).play(FadeIn(union), FadeIn(intersection), GrowFromPoint(line_1, 4/np.sqrt(3)*RIGHT), GrowFromPoint(line_2, 4/np.sqrt(3)*RIGHT), GrowFromCenter(dot))
        alpha_x = ValueTracker(4/np.sqrt(3))
        alpha_y = ValueTracker(0)
        updating = VGroup(line_1, line_2, dot).set_stroke(background = True)
        def all_updater(mob: VGroup):
            position = alpha_x.get_value()*RIGHT + alpha_y.get_value()*UP
            angle = angle_of_vector(position)
            delta = np.arccos(2/get_norm(position))
            mob[0].restore().rotate(angle-PI/2+delta, about_point = ORIGIN)
            mob[1].restore().rotate(angle-PI/2-delta, about_point = ORIGIN)
            mob[2].move_to(position)
        updating.add_updater(all_updater)
        self.remove(line_1, line_2, dot).add(updating).play(alpha_x.animate.set_value(2), alpha_y.animate.set_value(-1), run_time = 1.5)
        updating.clear_updaters()
        self.play(Rotate(updating, PI/2, about_point = ORIGIN), run_time = 2)
        self.wait(1+2-4, 20+29-15) #但在圆环的大部分区域 线段会扫过每个点两次
        self.remove(updating).add(line_1, line_2, dot).play(GrowFromPoint(line_1, RIGHT+2*UP, remover = True, rate_func = lambda t: smooth(1-t)), GrowFromPoint(line_2, RIGHT+2*UP, remover = True, rate_func = lambda t: smooth(1-t)))
        self.play(GrowFromCenter(dot, remover = True, rate_func = lambda t: smooth(1-t)))
        self.wait(0, 9) #于是当圆环足够大的时候
        text_t = MTex(r"S\ge\frac{\pi}{8}", tex_to_color_map = {r"S": YELLOW}).scale(0.8)
        text_t.shift(text_ah[1].get_center() - text_t[1].get_center() + 2*DOWN)
        self.play(FadeIn(text_t, 0.5*RIGHT))
        self.wait(1, 23) #线段扫过的面积大约会是π/8
        self.wait(0, 21) #（空闲）

        self.fade_out(excepts = [title, title_line])
        reuleaux = Reuleaux(radius = 4/np.sqrt(3), color = YELLOW).center()
        vertices = [reuleaux.get_points()[0], reuleaux.get_points()[24], reuleaux.get_points()[48]]
        line = Line(2*UP, 2*DOWN, stroke_width = 8).add(Dot(2*UP, color = TEAL)).set_stroke(background = True)
        self.fade_in(reuleaux, line, excepts = [title, title_line])
        self.wait(0, 17) #而我们之前见过的莱洛三角形
        text_ah = MTex(r"a=1\ \text{或}\ a=0", tex_to_color_map = {r"a": TEAL}).scale(0.8).next_to(2*UP + 6*LEFT)
        text_s = MTex(r"S_{\text{累计}}=\frac{\pi}{2}", tex_to_color_map = {r"S_{\text{累计}}": YELLOW}).scale(0.8)
        text_s.shift(text_ah[3].get_center() - text_s[3].get_center() + DOWN)
        self.play(Write(text_ah))
        self.wait(1, 15) #因为旋转中心是线段的一端
        alpha = ValueTracker(0)
        line.counter = 0
        lines = []
        def line_updater(mob: Line):
            angle = alpha.get_value()
            def start_func(t: float):
                t = (t + PI/6) % PI
                case = int(t/PI*3)%3
                t = t - PI/6
                if case == 0:
                    return vertices[0] + 4*unit(t-PI/2)
                elif case == 1:
                    return vertices[2]
                else:
                    return vertices[1]
            def end_func(t: float):
                t = (t + PI/6) % PI
                case = int(t/PI*3)%3
                t = t - PI/6
                if case == 0:
                    return vertices[0]
                elif case == 1:
                    return vertices[2] + 4*unit(t+PI/2)
                else:
                    return vertices[1] + 4*unit(t-PI/2)
            mob.put_start_and_end_on(start_func(angle), end_func(angle))
            critical = mob.counter*TAU/90
            while angle >= critical:
                thinline = Line(start_func(critical), end_func(critical), color = WHITE, stroke_width = 1)
                self.bring_to_back(thinline)
                lines.append(thinline)
                mob.counter += 1
                critical = mob.counter*TAU/90
            case = int((angle + PI/6)%PI/PI*3)%3
            if case == 0:
                mob[0].move_to(vertices[0])
            elif case == 1:
                mob[0].move_to(vertices[2])
            else:
                mob[0].move_to(vertices[1])
        line.add_updater(line_updater)
        self.play(alpha.animate.set_value(PI), Write(text_s, rate_func = squish_rate_func(smooth, 2/3, 1)), run_time = 3)
        self.wait(2+2-3, 2+20) #当它转过半圈的时候 累计扫过的面积是π/2

        union = reuleaux.copy().set_stroke(width = 0).set_fill(opacity = 0.2)
        intersection = Polygon(*vertices, color = RED, stroke_width = 0, fill_opacity = 0.4)
        text_t = MTex(r"S=\frac{\pi-\sqrt{3}}{2}", tex_to_color_map = {r"S": YELLOW}).scale(0.8)
        text_t.shift(text_ah[3].get_center() - text_t[1].get_center() + 2*DOWN)
        self.bring_to_back(union, intersection).play(FadeIn(union), FadeIn(intersection), Write(text_t))
        self.play(*[FadeOut(mob) for mob in lines])
        self.wait(1, 4) #虽然中间的三角形一共被扫过了三次
        self.wait(2, 17) #但总面积还是比圆环要大一些的
        self.wait(0, 19) #（空闲）

        self.fade_out(excepts = [title, title_line])
        vertices = [2*UP, 2*DOWN+4/np.sqrt(3)*LEFT, 2*DOWN+4/np.sqrt(3)*RIGHT]
        triangle = Polygon(*vertices, color = YELLOW)
        line = Line(2*UP, 2*DOWN, stroke_width = 8).add(Dot(2*UP, color = TEAL)).set_stroke(background = True)
        self.fade_in(triangle, line, excepts = [title, title_line])
        self.wait(0, 8) #而对于正三角形的挂谷集
        alpha = ValueTracker(0)
        line.counter = 0
        lines = []
        def line_updater(mob: Line):
            angle = alpha.get_value()
            def start_func(t: float):
                t = (t + PI/6) % PI
                case = int(t/PI*3)%3
                t = t - PI/6
                if case == 0:
                    return vertices[0] + 4*unit(t-PI/2)
                elif case == 1:
                    return vertices[2]
                else:
                    return vertices[1]
            def end_func(t: float):
                t = (t + PI/6) % PI
                case = int(t/PI*3)%3
                t = t - PI/6
                if case == 0:
                    return vertices[0]
                elif case == 1:
                    return vertices[2] + 4*unit(t+PI/2)
                else:
                    return vertices[1] + 4*unit(t-PI/2)
            mob.put_start_and_end_on(start_func(angle), end_func(angle))
            critical = mob.counter*TAU/90
            while angle >= critical:
                thinline = Line(start_func(critical), end_func(critical), color = WHITE, stroke_width = 1)
                self.bring_to_back(thinline)
                lines.append(thinline)
                mob.counter += 1
                critical = mob.counter*TAU/90
            case = int((angle + PI/6)%PI/PI*3)%3
            if case == 0:
                mob[0].move_to(vertices[0])
            elif case == 1:
                mob[0].move_to(vertices[2])
            else:
                mob[0].move_to(vertices[1])
        line.add_updater(line_updater)
        self.play(alpha.animate.set_value(PI), Write(text_ah, rate_func = squish_rate_func(smooth, 0, 1/3)), Write(text_s, rate_func = squish_rate_func(smooth, 2/3, 1)), run_time = 3)
        self.wait(2+2-3, 7+4) #线段如果也绕顶点旋转 就也会扫过π/2
        angle = np.arccos(1/np.sqrt(3))
        intersection_1 = Arc(radius = 4, angle = angle, stroke_width = 0, fill_color = RED, fill_opacity = 0.2).shift(vertices[1]).append_points(Arc(radius = 4, start_angle = PI, angle = -angle).shift(vertices[2]).get_points()[::-1]).close_path()
        intersection_2 = intersection_1.copy().rotate(TAU/3, about_point = 2/3*DOWN)
        intersection_3 = intersection_1.copy().rotate(-TAU/3, about_point = 2/3*DOWN)
        union = triangle.copy().set_stroke(width = 0).set_fill(opacity = 0.2)
        text_t = MTex(r"S=\frac{\sqrt{3}}{3}", tex_to_color_map = {r"S": YELLOW}).scale(0.8)
        text_t.shift(text_ah[3].get_center() - text_t[1].get_center() + 2*DOWN)
        self.bring_to_back(union, intersection_1, intersection_2, intersection_3).play(Write(text_t), *[FadeIn(mob) for mob in [union, intersection_1, intersection_2, intersection_3]])
        self.play(*[FadeOut(mob) for mob in lines])
        self.wait(1, 29) #但正三角形重叠的部分比莱洛三角形多少要多一点
        self.wait(2, 27) #于是面积会比莱洛三角形稍微小一点
        self.wait(1, 3) #到此共49秒
        self.play(*[FadeOut(mob) for mob in [text_ah, text_s, text_t, union, intersection_1, intersection_2, intersection_3]])
        
class Chapter2_4(FrameScene):
    def construct(self):
        self.notices = [Notice("简单例子", "请　熟悉"),
                        Notice("定长梯子", "墙角滑下"),
                        Notice("简单例子", "请　熟悉")]
        self.notice = self.notices[0]
        self.frames = 30
        title = Title("面积重叠")
        title_line = TitleLine()
        vertices = [2*UP, 2*DOWN+4/np.sqrt(3)*LEFT, 2*DOWN+4/np.sqrt(3)*RIGHT]
        radius = 8/np.sqrt(3)
        triangle = Polygon(*vertices, color = YELLOW)
        line = Line(2*UP, 2*DOWN, stroke_width = 8).add(Dot(2*UP, color = TEAL)).set_stroke(background = True)
        self.add(self.notice, title, title_line, triangle, line)
        self.wait(0, 24) #但我们之前也见过

        line_copy = Line(2*UP, 2*DOWN, color = GREY)
        alpha = ValueTracker(0.0)
        def line_updater(mob: VMobject):
            value = alpha.get_value()
            mob.restore().rotate(value, about_point = 2*np.sqrt(3)*LEFT).shift(value/(PI/3)*(4*DOWN + 4/np.sqrt(3)*RIGHT))
        line_copy.save_state().add_updater(line_updater)
        self.add(line_copy, line).play(alpha.animate.set_value(PI/6))
        line_copy.clear_updaters()
        self.wait(0, 15)
        self.play(line_copy.animate.shift(0.3*unit(PI/4)), run_time = 0.5)
        self.wait(0, 15)
        self.play(line_copy.animate.shift(0.3*unit(-PI/6)), run_time = 0.5)
        self.wait(0, 15)
        self.play(FadeOut(line_copy))
        self.wait(3+2-4, 8+6-15) #正三角形其实是一个比较宽松的挂谷集 线段除了绕着顶点旋转
        alpha = ValueTracker(0.0)
        def line_updater(mob: VMobject):
            value = (alpha.get_value())%PI
            if value <= PI/3:
                mob.restore().rotate(value, about_point = 2*np.sqrt(3)*LEFT).shift(value/(PI/3)*(4*DOWN + 4/np.sqrt(3)*RIGHT))
                mob[0].move_to(vertices[1] + radius*unit(PI/3 - value))
            elif value <= 2*PI/3:
                mob.restore().rotate(value - PI/3, about_point = 2*np.sqrt(3)*LEFT).shift((value/(PI/3)-1)*(4*DOWN + 4/np.sqrt(3)*RIGHT)).rotate(-2*PI/3, about_point = 2/3*DOWN)
                mob[0].move_to(vertices[0] + radius*unit(-value))
            else:
                mob.restore().rotate(value - 2*PI/3, about_point = 2*np.sqrt(3)*LEFT).shift((value/(PI/3)-2)*(4*DOWN + 4/np.sqrt(3)*RIGHT)).rotate(-4*PI/3, about_point = 2/3*DOWN)
                mob[0].move_to(vertices[2] + radius*unit(TAU*5/6 - value))
        line.save_state().add_updater(line_updater)
        self.play(alpha.animating(run_time = 2).set_value(PI/6), self.change_notice())
        self.wait(0, 6) #也可以贴着正三角形的边旋转
        self.wait(0, 19) #（空闲）
        arrow_x = Arrow(0.5*LEFT, 3.5*RIGHT, buff = 0, stroke_width = 3)
        arrow_y = Arrow(0.5*DOWN, UP, buff = 0, stroke_width = 3)
        tip_x = MTex(r"\theta", color = WHITE).scale(0.6).next_to(arrow_x, RIGHT)
        tip_y = MTex(r"a", color = TEAL).scale(0.6).next_to(arrow_y, UP)
        def function_a(t: float):
            if t >= PI*5/6:
                t = PI-t
            elif t >= PI/2:
                t -= TAU/3
            elif t >= PI/6:
                t = PI/3-t
            return np.tan(PI/6+t)/(np.tan(PI/6+t)+np.tan(PI/6-t))
        graph = FunctionGraph(function_a, [0, PI, PI/100], color = WHITE)
        point = Dot(np.array([0, function_a(0), 0]), color = YELLOW).shift(UP + 6*LEFT)
        coordinate = VGroup(arrow_x, arrow_y, tip_x, tip_y, graph).shift(UP + 6*LEFT)
        self.play(alpha.animating(rate_func = lambda t: wiggle(0.5*t)).set_value(PI/4), FadeIn(coordinate))
        self.play(alpha.animate.set_value(PI/12), rate_func = lambda t: -wiggle(0.5*(t+1)))
        line.clear_updaters()
        self.wait(0, 17) #这个时候转动中心就不总在顶点了
        self.wait(0+1+1+0-4, 18+16+25+17)

        arcs = Arc(radius = radius, start_angle = PI/6, angle = PI/6, color = TEAL, stroke_width = 2).shift(vertices[1]).append_points(
              Arc(radius = radius, start_angle = TAU/3, angle = PI/3, n_components = 16).shift(vertices[2]).get_points()).append_points(
              Arc(radius = radius, start_angle = -TAU/3, angle = PI/3, n_components = 16).shift(vertices[0]).get_points()).append_points(
              Arc(radius = radius, start_angle = 0, angle = PI/6, ).shift(vertices[1]).get_points())
        self.add(arcs)
        alpha = ValueTracker(-PI/6)
        line.counter = -7
        lines = []
        def line_updater(mob: VMobject):
            value = alpha.get_value()
            def start_func(t: float):
                if t <= PI/3:
                    return vertices[2] + radius*unit(TAU/3)*np.cos(t)
                elif t <= TAU/3:
                    return vertices[0] + radius*unit(-PI/3)*np.cos(TAU/3-t)
                else:
                    return vertices[1] + radius*unit(0)*np.cos(t-TAU/3)
            def end_func(t: float):
                if t <= PI/3:
                    return vertices[2] + radius*unit(PI)*np.cos(PI/3-t)
                elif t <= TAU/3:
                    return vertices[0] + radius*unit(-TAU/3)*np.cos(t-PI/3)
                else:
                    return vertices[1] + radius*unit(PI/3)*np.cos(PI-t)
            mob.put_start_and_end_on(start_func(value % PI), end_func(value % PI))
            if value % PI <= PI/3:
                mob[0].move_to(vertices[2] + radius*unit(2*PI/3 + value))
            elif value % PI <= 2*PI/3:
                mob[0].move_to(vertices[0] + radius*unit(PI + value))
            else:
                mob[0].move_to(vertices[1] + radius*unit(-2*PI/3 + value % PI))
            critical = mob.counter*TAU/90
            while value >= critical:
                thinline = Line(start_func(critical % PI), end_func(critical % PI), color = WHITE, stroke_width = 1)
                self.bring_to_back(thinline)
                lines.append(thinline)
                mob.counter += 1
                critical = mob.counter*TAU/90
        line.add_updater(line_updater)
        def point_updater(mob: Dot):
            value = alpha.get_value() + PI/6
            mob.move_to(np.array([value, function_a(value), 0]) + UP + 6*LEFT).set_opacity(clip(value/(PI/6), 0, 1))
        point.add_updater(point_updater)
        self.bring_to_back(arcs).add(point).play(alpha.animate.set_value(5*PI/6), ShowCreation(arcs), run_time = 4) #（空闲）随着线段的转动 它会在三段圆弧上移动 （空闲）
        line.clear_updaters()
        point.clear_updaters()

        text_s = MTex(r"S_{\text{累计}}=\frac{5\pi}{24}+\frac{7\sqrt3}{16}\approx 1.412", tex_to_color_map = {r"S_{\text{累计}}": YELLOW}).scale(0.6)
        text_s.shift(5.5*LEFT + 0.2*DOWN - text_s[3].get_center())
        text_t = MTex(r"S=\frac{\sqrt{3}}{3}", tex_to_color_map = {r"S": YELLOW}).scale(0.8)
        text_t.shift(5*LEFT + 1.4*DOWN - text_t[1].get_center())
        def boundary(value: float):
            def start_func(t: float):
                if t <= PI/3:
                    return vertices[2] + radius*unit(TAU/3)*np.cos(t)
                elif t <= TAU/3:
                    return vertices[0] + radius*unit(-PI/3)*np.cos(TAU/3-t)
                else:
                    return vertices[1] + radius*unit(0)*np.cos(t-TAU/3)
            def end_func(t: float):
                if t <= PI/3:
                    return vertices[2] + radius*unit(PI)*np.cos(PI/3-t)
                elif t <= TAU/3:
                    return vertices[0] + radius*unit(-TAU/3)*np.cos(t-PI/3)
                else:
                    return vertices[1] + radius*unit(PI/3)*np.cos(PI-t)
            return interpolate(end_func(value), start_func(value), function_a(value + PI/6))
        intersection = ParametricCurve(boundary, [0, PI, PI/100], fill_opacity = 0.4, color = RED, stroke_width = 0)
        union = triangle.copy().set_stroke(width = 0).set_fill(opacity = 0.2)
        self.bring_to_back(union, intersection).play(FadeIn(text_s, 0.5*RIGHT), FadeIn(text_t, 0.5*RIGHT), FadeIn(union), FadeIn(intersection))
        self.play(*[FadeOut(mob) for mob in lines])
        self.wait(1, 3) #这样旋转的累计面积会比π/2小
        self.wait(2, 16) #但因为重叠的部分也变少了
        self.wait(2, 16) #总面积仍然是正三角形的面积
        self.wait(0, 24) #（空闲）

        self.fade_out(change_notice = True, excepts = [title, title_line])
        boundary_2 = lambda t: np.array([np.sin(2*t)-2*np.sin(t), np.cos(2*t)+2*np.cos(t), 0])
        deltoid = ParametricCurve(boundary_2, [0, TAU, TAU/100], color = YELLOW)
        line = Line(boundary_2(0), boundary_2(PI), stroke_width = 8).add(Dot(3*UP, color = TEAL)).set_stroke(background = True)
        self.play(FadeIn(deltoid), FadeIn(line))
        self.wait(0, 5) #再把这个方案调整一下的话
        arrow_x = Arrow(0.5*LEFT, 3.5*RIGHT, buff = 0, stroke_width = 3)
        arrow_y = Arrow(0.5*DOWN, UP, buff = 0, stroke_width = 3)
        tip_x = MTex(r"\theta", color = WHITE).scale(0.6).next_to(arrow_x.get_right(), UP)
        tip_y = MTex(r"a", color = TEAL).scale(0.6).next_to(arrow_y, UP)
        def function_a(t: float):
            return (np.sin(t*3/2))**2
        graph = FunctionGraph(function_a, [0, PI, PI/100], color = WHITE)
        point = Dot(np.array([0, function_a(0), 0]), color = YELLOW).shift(UP + 6.5*LEFT)
        coordinate = VGroup(arrow_x, arrow_y, tip_x, tip_y, graph).shift(UP + 6.5*LEFT)
        self.play(FadeIn(coordinate, 0.5*UP), FadeIn(point, 0.5*UP))
        self.wait(2, 11) #我们就能得到挂谷宗一当年猜测的答案
        circle = Arc(radius = 3, start_angle = PI/2, angle = -2*PI, color = TEAL, stroke_width = 2)
        alpha = ValueTracker(0)
        line.counter = 0
        lines = []
        def line_updater(mob: VMobject):
            value = alpha.get_value()
            mob.put_start_and_end_on(boundary_2(value), boundary_2(value+PI))
            mob[0].move_to(3*unit(PI/2-2*value))
            critical = mob.counter*TAU/90
            while value >= critical:
                thinline = Line(boundary_2(critical), boundary_2(critical+PI), color = WHITE, stroke_width = 1)
                self.bring_to_back(thinline)
                lines.append(thinline)
                mob.counter += 1
                critical = mob.counter*TAU/90
        line.add_updater(line_updater)
        def point_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(np.array([value, function_a(value), 0]) + UP + 6.5*LEFT)
        point.add_updater(point_updater)
        self.bring_to_back(circle).play(alpha.animate.set_value(PI), ShowCreation(circle), run_time = 4)
        self.wait(1+0+2-4, 19+18+11) #一条三尖内摆线 （空闲） 线段在三尖内摆线内旋转
        text_s = MTex(r"S_{\text{累计}}=\frac{3\pi}{8}\approx 1.178", tex_to_color_map = {r"S_{\text{累计}}": YELLOW}).scale(0.8)
        text_s.shift(5.5*LEFT + 0.2*DOWN - text_s[3].get_center())
        text_t = MTex(r"S=\frac{\pi}{8}\approx 0.393", tex_to_color_map = {r"S": YELLOW}).scale(0.8)
        text_t.shift(5.5*LEFT + 1.4*DOWN - text_t[1].get_center())
        union = deltoid.copy().set_stroke(width = 0).set_fill(color = RED, opacity = 0.4)
        intersection = deltoid.copy().set_stroke(width = 0).set_fill(opacity = 0.2)
        self.bring_to_back(intersection, union).play(FadeIn(text_s, 0.5*RIGHT), FadeIn(text_t, 0.5*RIGHT), FadeIn(union), FadeIn(intersection))
        self.play(*[FadeOut(mob) for mob in lines])
        self.wait(0, 9) #累计会扫过3π/8的面积
        self.wait(0, 16) #（空闲）
        self.wait(1, 6) #而每一个点
        self.wait(2, 2) #都恰好会被扫过三次
        self.wait(2, 20) #于是三尖内摆线的面积是π/8
        self.wait(3, 28)
        self.fade_out(end = True)
        self.wait(2, 0) #到此共52秒
    
#################################################################### 

class Chapter3_0(FrameScene):

    def construct(self):

        text3 = Text("第三节 重叠", font = 'simsun', t2c={"第三节": YELLOW, "重叠": GREEN})

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(FrameScene):
    def construct(self):
        self.notices = [Notice("前情提要", "请　复习"),
                        Notice("本节内容", "请　思考"),
                        Notice("陈旧构造", "请勿模仿"),
                        Notice("上节内容", "请　回顾"),
                        Notice("趣味几何", "请　思考")]
        self.notice = self.notices[0]
        offset_circle = DOWN
        offset_annulus = DOWN + 4.5*RIGHT
        offset_reuleaux = 2*UP + 2*RIGHT
        offset_triangle = 2*UP + 2*LEFT + (np.sqrt(3)-1.5)*UP
        offset_deltoid = 1.5*DOWN + 4.5*LEFT
        circle = Circle(radius = 1.5, color = YELLOW).shift(offset_circle)
        annulus = Arc(radius = 1.5, start_angle = -PI/2, angle = PI, n_components = 24, color = YELLOW).add_line_to(1.5*UP+1.5*LEFT).append_points(Arc(radius = 1.5*np.sqrt(2), start_angle = PI*3/4, angle = -PI*3/2, n_components = 24).get_points()).close_path().shift(offset_annulus)
        reuleaux = Reuleaux(color = YELLOW).shift(offset_reuleaux)
        triangle = Polygon(1.5*UP, 1.5*DOWN+np.sqrt(3)*LEFT, 1.5*DOWN+np.sqrt(3)*RIGHT, color = YELLOW).shift(offset_triangle)
        function_deltoid = lambda t: np.array([np.sin(2*t)-2*np.sin(t), np.cos(2*t)+2*np.cos(t), 0])*0.75
        deltoid = ParametricCurve(function_deltoid, [0, TAU, TAU/100], color = YELLOW).shift(offset_deltoid)
        self.add(circle, annulus, reuleaux, triangle, deltoid).play(Write(self.notice), LaggedStart(FadeIn(circle, 0.5*DOWN), FadeIn(annulus, 0.5*LEFT), FadeIn(reuleaux, 0.5*DL), FadeIn(triangle, 0.5*DR), FadeIn(deltoid, 0.5*RIGHT), group = VGroup(), lag_ratio = 0.25, run_time = 2))
        colors = [interpolate_color(YELLOW, BACK, 0.8), interpolate_color(ORANGE, BACK, 0.6), interpolate_color(RED, BACK, 0.6)]
        union_circle = circle.copy().set_stroke(width = 0).set_fill(opacity = 1, color = colors[0])
        union_annulus = annulus.copy().set_stroke(width = 0).set_fill(opacity = 1, color = colors[0])
        union_reuleaux = reuleaux.copy().set_stroke(width = 0).set_fill(opacity = 1, color = colors[0])
        union_triangle = triangle.copy().set_stroke(width = 0).set_fill(opacity = 1, color = colors[0])
        intersection_annulus = Arc(radius = 1.5, start_angle = -PI/2, angle = PI, n_components = 24, stroke_width = 0, fill_opacity = 1, color = colors[1]).add_line_to(1.5*UP+1.5*RIGHT).append_points(Arc(radius = 1.5*np.sqrt(2), start_angle = PI/4, angle = -PI/2, n_components = 24).get_points()).close_path().shift(offset_annulus)
        intersection_reuleaux = Polygon(np.sqrt(3)*unit(PI/2), np.sqrt(3)*unit(PI*7/6), np.sqrt(3)*unit(-PI/6), stroke_width = 0, fill_opacity = 1, color = colors[2]).shift(offset_reuleaux)
        def function_a(t: float):
            if t >= PI*5/6:
                t = PI-t
            elif t >= PI/2:
                t -= TAU/3
            elif t >= PI/6:
                t = PI/3-t
            return np.tan(PI/6+t)/(np.tan(PI/6+t)+np.tan(PI/6-t))
        def function_triangle(value: float):
            def start_func(t: float):
                if t <= PI/3:
                    return 1.5*DOWN+np.sqrt(3)*RIGHT + 2*np.sqrt(3)*unit(TAU/3)*np.cos(t)
                elif t <= TAU/3:
                    return 1.5*UP + 2*np.sqrt(3)*unit(-PI/3)*np.cos(TAU/3-t)
                else:
                    return 1.5*DOWN+np.sqrt(3)*LEFT + 2*np.sqrt(3)*unit(0)*np.cos(t-TAU/3)
            def end_func(t: float):
                if t <= PI/3:
                    return 1.5*DOWN+np.sqrt(3)*RIGHT + 2*np.sqrt(3)*unit(PI)*np.cos(PI/3-t)
                elif t <= TAU/3:
                    return 1.5*UP + 2*np.sqrt(3)*unit(-TAU/3)*np.cos(t-PI/3)
                else:
                    return 1.5*DOWN+np.sqrt(3)*LEFT + 2*np.sqrt(3)*unit(PI/3)*np.cos(PI-t)
            return interpolate(end_func(value), start_func(value), function_a(value + PI/6))
        intersection_triangle = ParametricCurve(function_triangle, [0, PI, PI/100], stroke_width = 0, fill_opacity = 1, color = colors[2]).shift(offset_triangle)
        intersection_deltoid = deltoid.copy().set_stroke(width = 0).set_fill(opacity = 1, color = colors[2])
        self.bring_to_back(union_circle, union_annulus, union_reuleaux, union_triangle, intersection_annulus, intersection_reuleaux, intersection_triangle, intersection_deltoid, self.shade).play(FadeOut(self.shade))
        self.wait(1+2-3, 28+6) #我们已经见过的这些挂谷集 都有一个统一的问题
        
        squares = [Square(side_length = 0.5, color = [YELLOW, ORANGE, RED][i], fill_opacity = 1, stroke_width = 0).shift(6.25*LEFT + 3*UP + i*0.75*DOWN) for i in range(3)]
        texts = [MTexText("重叠1次").scale(0.8).next_to(squares[0]).add(squares[0]), MTexText("重叠2次").scale(0.8).next_to(squares[1]).add(squares[1]), MTexText("重叠3次").scale(0.8).next_to(squares[2]).add(squares[2])]
        self.play(LaggedStart(*[FadeIn(mob, 0.5*RIGHT) for mob in texts], lag_ratio = 0.2, run_time = 0.7), frames = 21)
        self.wait(1, 18) #它们面积的利用效率太低了
        self.wait(0, 17) #（空闲）
        self.wait(3, 12) #这些方案中 每块面积最多只重叠了三次
        self.wait(0, 21) #（空闲）
        self.play(self.change_notice())
        self.wait(0, 6) #在这一节
        self.wait(2+0-1, 26+17)
        self.fade_out() #我们就来试试看怎么让面积多重叠几次（空闲）

        triangle_0 = Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT, 2.5*DOWN + 2*np.sqrt(3)*RIGHT, color = YELLOW, fill_opacity = 0.5, stroke_width = 0)
        triangles_1 = [Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT + i*2*np.sqrt(3)*RIGHT, 2.5*DOWN + 2*np.sqrt(3)*LEFT + (i+1)*2*np.sqrt(3)*RIGHT, color = YELLOW, fill_opacity = 0.5, stroke_width = 0) for i in range(2)]
        offsets_1 = [2/np.sqrt(3)*RIGHT, 2/np.sqrt(3)*LEFT]
        self.play(FadeIn(triangle_0), self.change_notice())
        self.remove(triangle_0).add(*triangles_1).play(*[triangles_1[i].animate.shift(offsets_1[i]).set_opacity(0.4) for i in range(2)])
        triangles_2 = [Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT + i*np.sqrt(3)*RIGHT, 2.5*DOWN + 2*np.sqrt(3)*LEFT + (i+1)*np.sqrt(3)*RIGHT, color = YELLOW, fill_opacity = 0.4, stroke_width = 0
                               ).save_state().shift(offsets_1[int(i/2)]) for i in range(4)]
        offsets_2 = [np.sqrt(3)*RIGHT, np.sqrt(3)/2*RIGHT, np.sqrt(3)/2*LEFT, np.sqrt(3)*LEFT]
        self.remove(*triangles_1).add(*triangles_2).play(*[triangles_2[i].animate.restore().shift(offsets_2[i]).set_opacity(0.3) for i in range(4)])
        triangles_3 = [Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT + i*np.sqrt(3)/2*RIGHT, 2.5*DOWN + 2*np.sqrt(3)*LEFT + (i+1)*np.sqrt(3)/2*RIGHT, color = YELLOW, fill_opacity = 0.3, stroke_width = 0
                               ).save_state().shift(offsets_2[int(i/2)]) for i in range(8)]
        offsets_3 = [i*np.sqrt(3)/5*RIGHT for i in [6, 5, 3, 2, -2, -3, -5, -6]]
        self.remove(*triangles_2).add(*triangles_3).play(*[triangles_3[i].animate.restore().shift(offsets_3[i]).set_opacity(0.2) for i in range(8)])
        triangles_4 = [Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT + i*np.sqrt(3)/4*RIGHT, 2.5*DOWN + 2*np.sqrt(3)*LEFT + (i+1)*np.sqrt(3)/4*RIGHT, color = YELLOW, fill_opacity = 0.2, stroke_width = 0
                               ).save_state().shift(offsets_3[int(i/2)]) for i in range(16)]
        offsets_4 = [i*np.sqrt(3)/6*RIGHT for i in [8, 7.5, 6.5, 6, 4, 3.5, 2.5, 2, -2, -2.5, -3.5, -4, -6, -6.5, -7.5, -8]]
        self.remove(*triangles_3).add(*triangles_4).play(*[triangles_4[i].animate.restore().shift(offsets_4[i]).set_opacity(0.15) for i in range(16)])
        self.wait(3+2-5, 0+28) #事实上 贝西科维奇给出的构造 就是依靠把三角形不断重叠来缩小面积的
        
        angles = [PI/2 + np.arctan(i/8/np.sqrt(3)) for i in range(-8, 9)]
        line = Line(3.5*UP + offsets_4[0], 3.5*UP + offsets_4[0] - 6*unit(angles[0]), stroke_width = 6).shift(8*unit(angles[0]))
        for i in range(16):
            self.play(line.animate.shift(-8*unit(angles[i])), run_time = 8/30, rate_func = rush_from, frames = 8)
            self.play(Rotate(line, angles[i+1] - angles[i], about_point = 3.5*UP + offsets_4[i]), run_time = 0.3, frames = 9)
            self.play(line.animate.shift(8*unit(angles[i+1])), run_time = 8/30, rate_func = rush_into, frames = 8)
            if i < 15:
                line.shift(offsets_4[i+1] - offsets_4[i])
        self.wait(0+2+1+1+0+3+2+1-13, 17+1+27+10+23+5+16+1-10) #（空闲） 但他的线段的移动方式 以一个世纪后的眼光来看 就有些过于复杂了 （空闲） 在今天 我们可以用非常简单的思路 来构造一个面积任意小的挂谷集

        self.fade_out(change_notice = True)
        line = Line(1.5*LEFT, 1.5*RIGHT)
        dot = Dot(color = TEAL)
        self.fade_in(line, dot)
        self.wait(0, 17) #既然最后总能重叠特别多次
        self.play(dot.animate.shift(LEFT))
        self.play(dot.animate.shift(1.5*RIGHT))
        self.play(dot.animate.shift(LEFT))
        self.play(dot.animate.shift(0.5*RIGHT), line.animate.shift(1.5*LEFT))
        semicircle = Arc(radius = 3, start_angle = PI, angle = -PI, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5)
        alpha = ValueTracker(0.0)
        def sector_updater(mob: Arc):
            angle = alpha.get_value()
            mob.set_points(Arc(radius = 3, start_angle = PI, angle = -angle, n_components = 24).add_line_to(ORIGIN).close_path().get_points())
        semicircle.add_updater(sector_updater)
        self.bring_to_back(semicircle).play(Rotate(line, -PI, about_point = ORIGIN), alpha.animate.set_value(PI), run_time = 2)
        semicircle.clear_updaters()
        self.play(FadeOut(line), FadeOut(dot))
        self.wait(2+0+3+0-7, 19+21+25) #那么旋转中心在哪 就无关紧要了 （空闲） 我们甚至可以把旋转中心 就固定在线段的一端 （空闲）

        sectors_60 = [Arc(radius = 3, start_angle = i*PI/3, angle = PI/3, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path() for i in range(3)]
        self.play(FadeOut(semicircle), FadeIn(sectors_60[1]), self.change_notice())
        self.wait(1, 20) #在这个半圆中取出一个扇形
        self.wait(1, 21) #现在我们需要做的
        sectors_20 = [Arc(radius = 3, start_angle = PI/3 + i*PI/9, angle = PI/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.8).add_line_to(ORIGIN).close_path() for i in range(3)]
        self.remove(sectors_60[1]).add(*sectors_20).play(sectors_20[0].animate.shift(DR).set_fill(color = ORANGE), sectors_20[1].animate.shift(DOWN), sectors_20[2].animate.shift(DL).set_color(LIME))
        self.wait(1, 24) #是把它再切成好几牙小扇形
        r = 3/(1+np.sin(PI/18))
        self.bring_to_back(sectors_20[1]).play(sectors_20[0].animate.shift(LEFT + r*unit(PI/2) - r*unit(7*PI/18)).set_opacity(0.6), sectors_20[1].animate.set_opacity(0.7))
        self.play(sectors_20[2].animate.shift(RIGHT + r*unit(PI/2) - r*unit(11*PI/18)).set_opacity(0.6), sectors_20[1].animate.set_opacity(0.6))
        self.wait(1+2-2, 13+0) #然后拼起来 让这些扇形有一定重叠
        self.wait(0, 17) #（空闲）

        line = Line(DOWN, DOWN+3*unit(PI/3), stroke_width = 8).shift(r*unit(PI/2) - r*unit(7*PI/18))
        start = Line(DOWN, DOWN+3*unit(PI/3), color = GREY).shift(r*unit(PI/2) - r*unit(7*PI/18))
        end = Line(DOWN, DOWN+3*unit(TAU/3), color = GREY).shift(r*unit(PI/2) - r*unit(11*PI/18))
        self.play(ShowCreation(end), ShowCreation(line))
        self.add(start, end, line).wait(0, 7) #但同时
        alpha = ValueTracker(0)
        def line_updater(mob: Line):
            value = alpha.get_value()
            if value <= PI/9:
                mob.put_start_and_end_on(DOWN, DOWN+3*unit(value + PI/3)).shift(r*unit(PI/2) - r*unit(7*PI/18))
            elif value <= TAU/9:
                mob.put_start_and_end_on(DOWN, DOWN+3*unit(value + PI/3))
            else:
                mob.put_start_and_end_on(DOWN, DOWN+3*unit(value + PI/3)).shift(r*unit(PI/2) - r*unit(11*PI/18))
        line.add_updater(line_updater)
        arrow = Arrow(3.5*UP, 2.2*UP, buff = 0.3)
        text = Text(r"不允许像这样跳变", font = "simsun").scale(0.5).shift(3.5*UP).add(arrow)
        self.play(alpha.animating(run_time = 2).set_value(PI/3), FadeIn(text, 0.5*DOWN))
        line.clear_updaters()
        self.wait(0, 17) #我们还得保证线段仍然能在里面旋转
        self.wait(0, 25) #（空闲）

        self.remove(end).play(sectors_20[0].animate.shift(1.5*RIGHT - r*unit(PI/2) + r*unit(7*PI/18)).set_opacity(0.8), sectors_20[2].animate.shift(1.5*LEFT - r*unit(PI/2) + r*unit(11*PI/18)).set_opacity(0.8), sectors_20[1].animate.set_opacity(0.8), FadeOut(line, 1.5*LEFT - r*unit(PI/2) + r*unit(11*PI/18)), FadeOut(start, 1.5*RIGHT - r*unit(PI/2) + r*unit(7*PI/18)), FadeOut(text))
        self.wait(0, 20) #想好怎么做了吗
        self.wait(1, 14) #其实很简单

        self.play(sectors_20[1].animate.shift(1.5*UP))
        self.play(Rotate(sectors_20[1], PI, about_point = 3/2*np.cos(PI/18)*UP + 0.5*UP))
        self.play(sectors_20[1].animate.shift(1.5*DOWN))
        self.play(sectors_20[0].animate.shift(1.5*LEFT + 3*np.sin(PI/18)*LEFT).set_opacity(0.6), sectors_20[1].animate.set_opacity(0.7))
        self.play(sectors_20[2].animate.shift(1.5*RIGHT + 3*np.sin(PI/18)*RIGHT).set_opacity(0.6), sectors_20[1].animate.set_opacity(0.6))
        self.wait(2+3-5, 27+1) #我们只需要把中间的小扇形翻转过来 和两边的小扇形靠在一起 就可以了
        self.wait(0, 26) #（空闲）
        self.wait(2, 19) #如果这三个小扇形是三等分的
        self.wait(2, 26) #那么这足以把中间小扇形的面积省出来
        self.wait(0, 24) #（空闲）

        sectors_60[0].shift(DOWN + 3*np.sin(PI/18)*LEFT)
        sectors_60[2].shift(DOWN + 3*np.sin(PI/18)*RIGHT)
        self.play(FadeIn(sectors_60[0], LEFT), FadeIn(sectors_60[2], RIGHT), *[mob.animate.set_fill(opacity = 0.5, color = YELLOW) for mob in sectors_20])
        sectors = [Arc(radius = 3, start_angle = 0, angle = PI*4/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path().shift(DOWN + 3*np.sin(PI/18)*LEFT), Arc(radius = 3, start_angle = PI*5/9, angle = PI*4/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path().shift(DOWN + 3*np.sin(PI/18)*RIGHT)]
        self.remove(sectors_60[0], sectors_60[2], sectors_20[0], sectors_20[2]).add(*sectors).wait(1, 13) #把这样处理过的扇形拼回去
        self.wait(3, 15) #我们就得到了一个比半圆面积更小的挂谷集
        self.wait(1, 9) #到此共84秒
        
class Chapter3_2(FrameScene):
    def construct(self):
        self.notices = [Notice("趣味几何", "请　思考"),
                        Notice("错误方法", "请勿模仿"), 
                        Notice("优美构造", "请　模仿"),
                        Notice("错误方法", "请勿模仿"), 
                        Notice("正确构造", "请　模仿")]
        self.notice = self.notices[0]
        sectors = [Arc(radius = 3, start_angle = 0, angle = PI*4/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path().shift(DOWN + 3*np.sin(PI/18)*LEFT), 
                   Arc(radius = 3, start_angle = PI+PI*4/9, angle = PI/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path().shift(DOWN + 3*np.cos(PI/18)*UP), 
                   Arc(radius = 3, start_angle = PI*5/9, angle = PI*4/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path().shift(DOWN + 3*np.sin(PI/18)*RIGHT)]
        self.add(self.notice, *sectors)
        alpha = ValueTracker(0.0)
        def sector_updater(mob: Arc):
            value = alpha.get_value()
            mob.restore().rotate(value, about_point = DOWN + 3/2*np.cos(PI/18)*UP).shift(there_and_back(value/PI)*1.5*UP)
        sectors[1].save_state().add_updater(sector_updater)
        def stopper(t: float):
            if t <= 0.5:
                return smooth(2*t)
            else:
                return 1 - (1.5-3*np.sin(PI/18))/1.5*smooth(2*t-1)
        self.play(sectors[0].animating(rate_func = stopper).shift(1.5*RIGHT), sectors[2].animating(rate_func = stopper).shift(1.5*LEFT), alpha.animate.set_value(PI), run_time = 2)
        sectors[1].clear_updaters()
        semicircle = Arc(radius = 3, start_angle = 0, angle = PI, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).shift(DOWN)
        self.remove(*sectors).add(semicircle).wait(1+2-2, 26+5) #半圆也是扇形 所以我们可以直接这么处理半圆
        self.wait(0, 20) #（空闲）

        sectors_60 = [Arc(radius = 3, start_angle = i*PI/3, angle = PI/3, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path().shift(DOWN) for i in range(3)]
        self.add(*sectors_60).remove(semicircle).play(sectors_60[0].animate.shift(2*RIGHT), sectors_60[1].animate.shift(1.5*UP), sectors_60[2].animate.shift(2*LEFT))
        self.wait(0, 14) #把半圆三等分
        self.play(Rotate(sectors_60[1], PI, about_point = 0.5*UP + 3*np.sqrt(3)/4*UP))
        self.wait(0, 12) #把中间一份翻转
        self.play(sectors_60[0].animate.shift(3.5*LEFT), sectors_60[1].animate.shift(1.5*DOWN), sectors_60[2].animate.shift(3.5*RIGHT))
        copy_reuleaux = VGroup(*sectors_60).copy()
        self.wait(0, 13) #再拼起来
        self.wait(2, 0) #我们就能得到莱洛三角形
        self.wait(0, 21) #（空闲）

        r = 7/np.sqrt(3) - 3
        vertices = [r/2*RIGHT + UP, (3*np.sqrt(3)-5)/2*UP, r/2*LEFT + UP]
        self.play(sectors_60[0].animate.shift((1.5+r/2)*RIGHT + 2*UP), sectors_60[1].animate.shift(1.5*DOWN), sectors_60[2].animate.shift((1.5+r/2)*LEFT + 2*UP))
        self.wait(0, 29) #为了进一步缩小面积
        sectors_20 = [[Arc(radius = 3, start_angle = i*PI/9, angle = PI/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path().shift(vertices[0]) for i in range(3)], 
                      [Arc(radius = 3, start_angle = -TAU/3 + i*PI/9, angle = PI/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path().shift(vertices[1]) for i in range(3)], 
                      [Arc(radius = 3, start_angle = TAU/3 + i*PI/9, angle = PI/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.5).add_line_to(ORIGIN).close_path().shift(vertices[2]) for i in range(3)]]
        self.remove(*sectors_60).add(*sectors_20[0], *sectors_20[1], *sectors_20[2]).play(
            sectors_20[0][0].animate.shift(unit(-PI/3)), Rotate(sectors_20[0][1], PI/2, about_point = vertices[0] + 3/2*np.cos(PI/18)*unit(PI/6), rate_func = rush_into), sectors_20[0][2].animate.shift(unit(TAU/3)), 
            sectors_20[1][0].animate.shift(LEFT), Rotate(sectors_20[1][1], PI/2, about_point = vertices[1] + 3/2*np.cos(PI/18)*DOWN, rate_func = rush_into), sectors_20[1][2].animate.shift(RIGHT), 
            sectors_20[2][0].animate.shift(unit(PI/3)), Rotate(sectors_20[2][1], PI/2, about_point = vertices[2] + 3/2*np.cos(PI/18)*unit(5*PI/6), rate_func = rush_into), sectors_20[2][2].animate.shift(unit(-TAU/3)), 
        )
        back = 1+3*np.sin(PI/18)
        self.play(sectors_20[0][0].animate.shift(-back*unit(-PI/3)), Rotate(sectors_20[0][1], PI/2, about_point = vertices[0] + 3/2*np.cos(PI/18)*unit(PI/6), rate_func = rush_from), sectors_20[0][2].animate.shift(-back*unit(TAU/3)), 
            sectors_20[1][0].animate.shift(-back*LEFT), Rotate(sectors_20[1][1], PI/2, about_point = vertices[1] + 3/2*np.cos(PI/18)*DOWN, rate_func = rush_from), sectors_20[1][2].animate.shift(-back*RIGHT), 
            sectors_20[2][0].animate.shift(-back*unit(PI/3)), Rotate(sectors_20[2][1], PI/2, about_point = vertices[2] + 3/2*np.cos(PI/18)*unit(5*PI/6), rate_func = rush_from), sectors_20[2][2].animate.shift(-back*unit(-TAU/3)))
        subsectors_60 = [VGroup(*group) for group in sectors_20]
        copies = [mob.copy() for mob in subsectors_60]
        self.remove(*sectors_20[0], *sectors_20[1], *sectors_20[2]).add(*subsectors_60).play(subsectors_60[0].animate.shift(3*DOWN + 2*RIGHT).set_fill(ORANGE), subsectors_60[2].animate.shift(3*DOWN + 2*LEFT).set_color(LIME))
        self.wait(2+0-3, 20+22) #我们需要再把这三个扇形也分别三等分 （空闲）
        
        self.play(self.change_notice())
        self.wait(1, 7) #但这三个三等分后的图形
        r = 3/(2*np.cos(PI/18))
        copies[0].shift(2*UP + r*np.cos(PI/9)*unit(7*PI/6) - vertices[0]).set_fill(ORANGE)
        copies[1].shift(2*UP + r*np.cos(PI/9)*unit(PI/2) - vertices[1])
        copies[2].shift(2*UP + r*np.cos(PI/9)*unit(-PI/6) - vertices[2]).set_fill(LIME)
        self.add(*copies).play(LaggedStart(FadeIn(copies[0], 0.2*unit(PI/6)), FadeIn(copies[1], 0.2*unit(-PI/2)), FadeIn(copies[2], 0.2*unit(5*PI/6)), group = VGroup(), lag_ratio = 0.5, run_time = 1))
        self.wait(1, 3) #要是边对边直接拼起来
        text_s = MTex(r"S=\frac{\pi-9\tan(10^\circ)}{2}\approx0.777", tex_to_color_map = {r"S": YELLOW}).scale(0.8).next_to(2*UP + 7*LEFT)
        self.play(Write(text_s), run_time = 1)
        self.wait(1, 13) #就只能得到一个莱洛九边形
        self.wait(2, 0) #它的面积比莱洛三角形要大
        self.wait(0, 21) #（空闲）

        s = 3-6*np.sin(PI/18)
        h = subsectors_60[0][0].get_points()[-3][1]
        new_vertices = [h*UP + (s/2)*LEFT, h*UP + s/2*np.sqrt(3)*UP, h*UP + (s/2)*RIGHT]
        r = 3*np.sqrt(3)*np.sin(PI/18)
        self.play(FadeOut(text_s, 1.25*LEFT, run_time = 0.5, rate_func = rush_into), *[mob.animate.shift(2.5*LEFT) for mob in copies], subsectors_60[1].animate.shift(new_vertices[1] - (vertices[1] + r*unit(-PI/2))), self.change_notice())
        self.play(subsectors_60[0].animate.shift(new_vertices[0] - (vertices[0] + 3*DOWN + 2*RIGHT + r*unit(PI/6))))
        self.play(subsectors_60[2].animate.shift(new_vertices[2] - (vertices[2] + 3*DOWN + 2*LEFT + r*unit(5*PI/6))))
        self.play(*[mob.animate.shift(2*DOWN + 0.5*LEFT) for mob in copies], *[mob.animate.shift(h*DOWN + s/(2*np.sqrt(3))*DOWN + 3*RIGHT) for mob in subsectors_60])
        self.wait(1+2-4, 27+11) #但只要稍微挪动一下 重叠的部分就会更多一些

        reuleaux = Reuleaux(radius = s/np.sqrt(3), color = GREY).shift(3*RIGHT)
        reuleaux_verticies = [3*RIGHT + s/np.sqrt(3)*unit(PI/2), 3*RIGHT + s/np.sqrt(3)*unit(7*PI/6), 3*RIGHT + s/np.sqrt(3)*unit(-PI/6)]
        self.play(ShowCreation(reuleaux))
        self.play(reuleaux.animate.set_style(stroke_width = 0, fill_opacity = 0.6))
        self.wait(1+3-2, 17+1) #整个图形看起来 就像是给莱洛三角形的三个角上各缝了一块
        self.wait(0, 24) #（空闲）

        line = Line(reuleaux_verticies[2] + 3*LEFT, reuleaux_verticies[2], stroke_width = 8)
        start = Line(reuleaux_verticies[2] + 3*LEFT, reuleaux_verticies[2], color = GREY)
        end = Line(reuleaux_verticies[1] + 3*RIGHT, reuleaux_verticies[1], color = GREY)
        self.play(ShowCreation(end), ShowCreation(line))
        self.add(start, end, line).wait(1, 15) #线段的旋转也不会受影响
        alpha = ValueTracker(0)
        def line_updater(mob: Line):
            value = alpha.get_value()
            if value <= PI/9:
                mob.restore().rotate(value, about_point = mob.get_start())
            elif value <= TAU/9:
                mob.restore().rotate(PI/9, about_point = mob.get_start()).rotate(value - PI/9, about_point = mob.get_end())
            else:
                mob.restore().rotate(PI/9, about_point = mob.get_start()).rotate(PI/9, about_point = mob.get_end()).rotate(value - TAU/9, about_point = mob.get_start())
        line.save_state().add_updater(line_updater)
        self.play(alpha.animate.set_value(PI/3), run_time = 2) #当它运动到边界的时候
        line.clear_updaters()
        self.play(line.animate.put_start_and_end_on(reuleaux_verticies[1], reuleaux_verticies[1] + 3*unit(PI/3)))
        alpha.set_value(0)
        line.reverse_points().save_state().add_updater(line_updater)
        self.play(alpha.animate.set_value(PI/3), run_time = 1.5)
        line.clear_updaters()
        self.play(line.animate.put_start_and_end_on(reuleaux_verticies[0], reuleaux_verticies[0] + 3*unit(-PI/3)))
        alpha.set_value(0)
        line.reverse_points().save_state().add_updater(line_updater)
        self.play(alpha.animate.set_value(PI/3), run_time = 1.5)
        line.clear_updaters()
        self.remove(end).wait(1+2+0-5, 29+19+29) #只需要沿着边界平移 就能到达下一个图形 继续旋转 （空闲）

        copy_reuleaux[0].set_color(ORANGE), copy_reuleaux[2].set_color(LIME)
        self.play(*[FadeOut(mob) for mob in copies + [start, line]], self.change_notice())
        self.play(FadeIn(copy_reuleaux.shift(3*LEFT)))
        self.wait(1, 14) #看起来 似乎我们只要这么不断地把扇形三等分
        self.play(FadeIn(semicircle.set_opacity(0.8).shift(4*LEFT), 6*RIGHT), copy_reuleaux.animate.shift(4*RIGHT), *[mob.animate.shift(2*RIGHT) for mob in subsectors_60 + [reuleaux]])
        self.wait(0, 26) #重叠的部分就会越来越多
        self.wait(0, 21) #（空闲）
        
        limit = MTex(r"\lim_{n\to\infty}S_n=\frac{\pi}{5}").scale(0.8).shift(3*UP)
        self.play(Write(limit))
        self.wait(0, 16) #但一直这么做
        self.wait(2, 5) #面积最后会趋向一个有限的值
        self.wait(0, 22) #（空闲）

        self.play(FadeOut(limit), *[FadeOut(mob, 2.5*LEFT, rate_func = rush_into) for mob in [semicircle, copy_reuleaux, reuleaux]], *[mob.animating(run_time = 2).shift(5*LEFT) for mob in subsectors_60], self.change_notice())
        self.wait(1+2-2, 26+14) #想要让面积任意小 我们需要对分割方法进行一些调整
        self.wait(0, 22) #（空闲）

        self.remove(*subsectors_60).add(subsectors_60[0], subsectors_60[1][0], subsectors_60[1][1], subsectors_60[1][2], subsectors_60[2]).play(*[FadeOut(mob, 0.5*DOWN) for mob in [subsectors_60[0], subsectors_60[2], subsectors_60[1][0], subsectors_60[1][2]]], subsectors_60[1][1].animate.next_to(DOWN, UP, buff = 0).set_opacity(0.8))
        sector = subsectors_60[1][1]
        false_subsectors = [Arc(radius = 3, start_angle = 4*PI/9 + i*PI/27, angle = PI/27, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.8).add_line_to(ORIGIN).close_path().shift(DOWN) for i in range(3)]
        self.remove(sector).add(*false_subsectors).play(false_subsectors[0].animate.shift(0.5*RIGHT), false_subsectors[2].animate.shift(0.5*LEFT))
        cross = VGroup(Line(UL, DR, color = RED), Line(UR, DL, color = RED), stroke_width = 6).shift(0.5*UP)
        self.play(ShowCreation(cross))
        self.play(FadeOut(cross), false_subsectors[0].animate.shift(0.5*LEFT), false_subsectors[2].animate.shift(0.5*RIGHT))
        self.remove(*false_subsectors).add(sector).wait(1+3-4, 28+11) #第三次处理的时候 我们不再翻转每个扇形中间的1/3
        subsectors = [Arc(radius = 3, start_angle = 4*PI/9, angle = PI/24, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.8).add_line_to(ORIGIN).close_path().shift(DOWN), 
                   Arc(radius = 3, start_angle = 4*PI/9 + PI/24, angle = PI/36, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.8).add_line_to(ORIGIN).close_path().shift(DOWN), 
                   Arc(radius = 3, start_angle = 5*PI/9 - PI/24, angle = PI/24, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 0.8).add_line_to(ORIGIN).close_path().shift(DOWN)]
        alpha = ValueTracker(0.8)
        def opacity_updater(mob: Arc):
            mob.set_opacity(alpha.get_value())
        subsectors[1].add_updater(opacity_updater)
        self.remove(sector).add(*subsectors).play(subsectors[0].animate.shift(RIGHT).set_opacity(0.7), Rotate(subsectors[1], PI/2, about_point = DOWN + 3/2*np.cos(PI/72)*UP, rate_func = rush_into), alpha.animate.set_value(0.7), subsectors[2].animate.shift(LEFT).set_opacity(0.7))
        self.play(subsectors[0].animate.shift(LEFT + 3*np.sin(PI/72)*LEFT).set_opacity(0.6), Rotate(subsectors[1], PI/2, about_point = DOWN + 3/2*np.cos(PI/72)*UP, rate_func = rush_from), alpha.animate.set_value(0.6), subsectors[2].animate.shift(RIGHT + 3*np.sin(PI/72)*RIGHT).set_opacity(0.6))
        subsectors[1].clear_updaters()
        self.wait(0, 17) #而是改为翻转每个扇形中间的1/4
        self.wait(0, 22) #（空闲）

        ratio = 1 - np.sin(PI/72)/np.sin(PI/18)
        verticies_1 = [s/np.sqrt(3)*unit(PI/2), s/np.sqrt(3)*unit(7*PI/6), s/np.sqrt(3)*unit(-PI/6)]
        r = 3*np.cos(PI/18) - np.sqrt(3)*(1+np.sin(PI/18))
        verticies_2 = [verticies_1[2]+3*LEFT, r*unit(PI/6), verticies_1[0]+3*unit(-TAU/3), verticies_1[1]+3*unit(PI/3), r*unit(-PI/2), verticies_1[2]+3*unit(TAU/3), verticies_1[0]+3*unit(-PI/3), r*unit(5*PI/6), verticies_1[1]+3*RIGHT]
        group_0 = VGroup(*subsectors).copy().shift(UP + 3*np.sin(PI/72)/np.tan(PI/18)*DOWN).set_opacity(0.5)
        angles = [-4*PI/9, 2*PI/3, -2*PI/9, 8*PI/9, 0, -8*PI/9, 2*PI/9, -2*PI/3, 4*PI/9]
        colors = [ORANGE, YELLOW, LIME]
        groups = [group_0.copy().rotate(angles[i], about_point = ORIGIN).shift(ratio*verticies_2[i]).set_color(colors[int(i/3)]) for i in range(9)]
        groups[4].save_state().become(VGroup(*subsectors))
        self.add(*groups).remove(*subsectors).play(*[FadeIn(mob, 0.5*UP) for mob in groups[0:4] + groups[5:]], groups[4].animate.restore())
        self.wait(0, 14) #第四次处理
        self.wait(3, 1) #翻转的变成每个扇形中间的1/5
        self.wait(0, 25) #依此类推
        self.wait(0, 22) #（空闲）
        self.fade_out()

class Patch3_2(FrameScene):
    CONFIG = {
        "for_pr": False
    }
    def construct(self):
        self.notices = [Notice("正确构造", "请　模仿")]
        self.notice = self.notices[0]
        shade_2 = self.shade.copy().append_points(Rectangle(height = 6, width = 8).reverse_points().get_points())
        
        self.add(shade_2, self.notice).wait(5)

class Patch3_3(FrameScene):
    CONFIG = {
        "for_pr": False
    }
    def construct(self):
        self.notices = [Notice("正确构造", "请　模仿")]
        self.notice = self.notices[0]
        
        self.add(self.shade, self.notice).wait(5)

class Chapter3_3(FrameScene):
    def construct(self):
        self.notices = [Notice("正确构造", "请　模仿"),
                        Notice("有趣思路", "请　参考")]
        self.notice = self.notices[0]
        self.frames += 2*30+25 + 2*30+25 + 2*30+0 + 0*30+23 + 30

        circle = Circle(radius = 2, color = YELLOW)
        dot = Dot(color = TEAL)
        line = Line(2*LEFT, 2*RIGHT)
        sector_left = Arc(0, 0, color = YELLOW, stroke_width = 0, fill_opacity = 0.2)
        sector_right = Arc(0, 0, color = YELLOW, stroke_width = 0, fill_opacity = 0.2)
        self.fade_in(sector_left, sector_right, circle, line, dot)
        self.wait(0, 2) #而要是观察一下直径为1的圆
        self.wait(1, 10) #就会发现
        alpha = ValueTracker(0)
        lines = []
        line.counter = 0
        def left_updater(mob: Arc):
            value = alpha.get_value()
            mob.set_points(Arc(0, value, radius = 2).add_line_to(ORIGIN).close_path().get_points())
        def right_updater(mob: Arc):
            value = alpha.get_value()
            mob.set_points(Arc(PI, value, radius = 2).add_line_to(ORIGIN).close_path().get_points())
        def line_updater(mob: Line):
            angle = alpha.get_value()
            mob.put_start_and_end_on(2*unit(angle), -2*unit(angle))
            critical = mob.counter*TAU/90
            while angle >= critical:
                thinline = Line(2*unit(critical), -2*unit(critical), color = WHITE, stroke_width = 1)
                self.bring_to_back(thinline)
                lines.append(thinline)
                mob.counter += 1
                critical = mob.counter*TAU/90
        sector_left.add_updater(left_updater)
        sector_right.add_updater(right_updater)
        line.add_updater(line_updater)
        self.play(self.change_notice(), alpha.animating(run_time = 2).set_value(PI))
        for mob in [sector_left, sector_right, line]:
            mob.clear_updaters()
        circle.set_fill(opacity = 0.2)
        self.remove(sector_left, sector_right).play(line.animating(remover = True).scale(0))
        self.play(dot.animating(remover = True).scale(0))
        self.wait(2+1-4, 29+24) #它虽然绝大部分区域只被扫过了一次 但确实有那么一个点
        self.wait(2, 16) #可以被看成扫过了无穷多次
        indicate = Dot(color = RED)
        self.play(GrowFromCenter(indicate)) #它的圆心
        self.wait(0, 21) #（空闲）

        copy_indicate = Circle(radius = 0.3, fill_opacity = 0.5, stroke_width = 0)
        self.add(copy_indicate, indicate).play(TransformFromCopy(indicate, copy_indicate))
        self.wait(2, 21) #要是我们能让圆心从一个点扩大成一个小区域
        flash = Circle(radius = 0.3, stroke_width = 6)
        self.play(ShowPassingFlash(flash))
        self.play(ShowPassingFlash(flash))
        self.wait(0, 24) #让这个小区域被扫过无穷多次
        self.wait(2, 24) #那么挂谷集的面积自然就能缩小到0了
        self.wait(1, 0) #（空闲）

        self.fade_out(run_time = 0.5)
        iter_0 = ArcBetweenPoints(np.sqrt(3)*unit(-PI/6), np.sqrt(3)*unit(7*PI/6), angle = PI, n_components = 24, stroke_width = 0, fill_opacity = 1, color = RED).scale(2, about_point = ORIGIN)
        iter_1 = Reuleaux(color = ORANGE, stroke_width = 0, fill_opacity = 1)
        self.fade_in(iter_0, run_time = 0.5)
        self.wait(1)
        iter_1.save_state().set_color(BACK).scale(2, about_point = ORIGIN)
        self.add(iter_1, iter_0).play(iter_1.animate.restore(), iter_0.animate.scale(0.5, about_point = ORIGIN), run_time = 2)
        triangle_1 = Polygon(np.sqrt(3)*UP, np.sqrt(3)*unit(-PI/6), np.sqrt(3)*unit(7*PI/6), color = GREY_B, stroke_width = 0, fill_opacity = 0.8)
        boundary_1 = triangle_1.copy().set_style(stroke_width = 6, fill_opacity = 0, stroke_color = WHITE)
        def triple_there_and_back(t: float):
            return there_and_back((3*t)%1)
        less_pause = smooth_boot(1/6)
        self.play(FadeIn(triangle_1, remover = True, rate_func = triple_there_and_back), ShowPassingFlash(boundary_1, rate_func = less_pause), run_time = 3)
        self.wait(2)

        ratio_2 = 1 - 2*np.sin(PI/18)
        radius_2 = np.sqrt(3) * ratio_2
        sectors_2 = [Arc(radius = 3, start_angle = -TAU/3 + i*PI/9, angle = PI/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path() for i in range(3)]
        sectors_2[0].shift(3*RIGHT*np.sin(PI/18)), sectors_2[1].rotate(PI, about_point = 3/2*np.cos(PI/18)*DOWN), sectors_2[2].shift(3*LEFT*np.sin(PI/18))
        group_2 = VGroup(*sectors_2).shift((3*np.sqrt(3)*np.sin(PI/18) + radius_2)*UP)
        iter_2 = VGroup(group_2, group_2.copy().rotate(TAU/3, about_point = ORIGIN), group_2.copy().rotate(-TAU/3, about_point = ORIGIN))
        iter_2.save_state().set_color(BACK).scale(1/ratio_2, about_point = ORIGIN)
        self.add(iter_2, iter_1, iter_0).play(iter_2.animate.restore(), iter_1.animate.scale(ratio_2, about_point = ORIGIN), iter_0.animate.scale(ratio_2, about_point = ORIGIN), run_time = 2)
        triangle_2 = Polygon(radius_2*UP, radius_2*unit(-PI/6), radius_2*unit(7*PI/6), color = GREY_B, stroke_width = 0, fill_opacity = 0.8)
        boundary_2 = triangle_2.copy().set_style(stroke_width = 6, fill_opacity = 0, stroke_color = WHITE)
        self.play(FadeIn(triangle_2, remover = True, rate_func = triple_there_and_back), ShowPassingFlash(boundary_2, rate_func = less_pause), run_time = 3)
        self.wait(2)

        ratio_3 = 1 - np.sin(PI/72)/np.sin(PI/18)
        radius_3 = radius_2 * ratio_3
        verticies_1 = [3*ratio_2/np.sqrt(3)*unit(PI/2), 3*ratio_2/np.sqrt(3)*unit(7*PI/6), 3*ratio_2/np.sqrt(3)*unit(-PI/6)]
        r = 3*np.cos(PI/18) - np.sqrt(3)*(1+np.sin(PI/18))
        verticies_2 = [verticies_1[2]+3*LEFT, r*unit(PI/6), verticies_1[0]+3*unit(-TAU/3), verticies_1[1]+3*unit(PI/3), r*unit(-PI/2), verticies_1[2]+3*unit(TAU/3), verticies_1[0]+3*unit(-PI/3), r*unit(5*PI/6), verticies_1[1]+3*RIGHT]
        LIMEGREEN = interpolate_color(LIME, GREEN, 0.75)
        sectors_3 = [Arc(radius = 3, start_angle = 4*PI/9, angle = PI/24, n_components = 24, color = LIMEGREEN, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path(), 
                   Arc(radius = 3, start_angle = 4*PI/9 + PI/24, angle = PI/36, n_components = 24, color = LIMEGREEN, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path(), 
                   Arc(radius = 3, start_angle = 5*PI/9 - PI/24, angle = PI/24, n_components = 24, color = LIMEGREEN, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path()]
        sectors_3[0].shift(3*np.sin(PI/72)*LEFT), sectors_3[1].rotate(PI, about_point = 3/2*np.cos(PI/72)*UP), sectors_3[2].shift(3*np.sin(PI/72)*RIGHT)
        group_3 = VGroup(*sectors_3).shift(3*np.sin(PI/72)/np.tan(PI/18)*DOWN)
        angles = [-4*PI/9, 2*PI/3, -2*PI/9, 8*PI/9, 0, -8*PI/9, 2*PI/9, -2*PI/3, 4*PI/9]
        iter_3 = VGroup(*[group_3.copy().rotate(angles[i], about_point = ORIGIN).shift(ratio_3*verticies_2[i]) for i in range(9)])
        iter_3.save_state().set_color(BACK).scale(1/ratio_3, about_point = ORIGIN)
        self.add(iter_3, iter_2, iter_1, iter_0).play(iter_3.animate.restore(), *[mob.animate.scale(ratio_3, about_point = ORIGIN) for mob in [iter_2, iter_1, iter_0]], run_time = 2)
        triangle_3 = Polygon(radius_3*UP, radius_3*unit(-PI/6), radius_3*unit(7*PI/6), color = GREY_B, stroke_width = 0, fill_opacity = 0.8)
        boundary_3 = triangle_3.copy().set_style(stroke_width = 6, fill_opacity = 0, stroke_color = WHITE)
        self.play(FadeIn(triangle_3, remover = True, rate_func = triple_there_and_back), ShowPassingFlash(boundary_3, rate_func = less_pause), run_time = 3)
        self.wait(2, 26) 
        self.fade_out(end = True)
        self.wait(2, 0) #到此共58秒
        
#################################################################### 

class Summary(FrameScene):

    def construct(self):
        self.notices = [Notice("良心视频", "请　三连"), 
                        Notice("下期预告", "敬请期待"), 
                        Notice("良心up主", "请　关注")]
        self.notice = self.notices[0]

        self.play(Write(self.notice))
        self.wait(0, 24) #非常感谢大家能看到这里
        self.wait(0, 21) #（空闲）

        paper = LabelPicture(r"paper.jpg", "G. Pal. Ein Minimumproblem fur Ovale. \n Math. Ann., 83:311–319, 1921", picture_config = {"height": 5}).shift(0.5*UP + 4*LEFT)
        self.play(FadeIn(paper, 0.5*RIGHT))
        self.wait(3, 3) #这期视频第一节的证明来自1921年保尔的论文
        video = ImageMobject(r"video.png", height = 4).shift(3*RIGHT)
        self.play(FadeIn(video, 0.5*LEFT))
        self.wait(1, 25) #而第三节的构造  我参考了这期视频
        self.wait(0, 21) #（空闲）

        self.fade_out()
        video_1 = BVCover(r"cover_1.jpg", r"BV1Ms411d79m").scale(0.8).shift(5*LEFT + 2.5*UP)
        video_2 = BVCover(r"cover_2.jpg", r"BV1tt411y7V9").scale(0.8).shift(5*LEFT + 0.25*UP)
        video_3 = BVCover(r"cover_3.jpg", r"BV1Rx411p7GN").scale(0.8).shift(5*LEFT + 2*DOWN)
        
        offset = RIGHT
        triangle_0 = Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT, 2.5*DOWN + 2*np.sqrt(3)*RIGHT, color = YELLOW, fill_opacity = 0.5, stroke_width = 0).shift(offset)
        triangles_1 = [Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT + i*2*np.sqrt(3)*RIGHT, 2.5*DOWN + 2*np.sqrt(3)*LEFT + (i+1)*2*np.sqrt(3)*RIGHT, color = YELLOW, fill_opacity = 0.5, stroke_width = 0).shift(offset) for i in range(2)]
        offsets_1 = [2/np.sqrt(3)*RIGHT, 2/np.sqrt(3)*LEFT]
        self.play(LaggedStart(*[FadeIn(video_1, 0.5*RIGHT), FadeIn(video_2, 0.5*RIGHT), FadeIn(video_3, 0.5*RIGHT)], lag_ratio = 0.5, run_time = 2), FadeIn(triangle_0))
        self.wait(0, 6) #挂谷问题一直是一个很热门的科普题材

        self.remove(triangle_0).add(*triangles_1).play(*[triangles_1[i].animate.shift(offsets_1[i]).set_opacity(0.4) for i in range(2)])
        triangles_2 = [Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT + i*np.sqrt(3)*RIGHT, 2.5*DOWN + 2*np.sqrt(3)*LEFT + (i+1)*np.sqrt(3)*RIGHT, color = YELLOW, fill_opacity = 0.4, stroke_width = 0
                               ).shift(offset).save_state().shift(offsets_1[int(i/2)]) for i in range(4)]
        offsets_2 = [np.sqrt(3)*RIGHT, np.sqrt(3)/2*RIGHT, np.sqrt(3)/2*LEFT, np.sqrt(3)*LEFT]
        self.remove(*triangles_1).add(*triangles_2).play(*[triangles_2[i].animate.restore().shift(offsets_2[i]).set_opacity(0.3) for i in range(4)])
        triangles_3 = [Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT + i*np.sqrt(3)/2*RIGHT, 2.5*DOWN + 2*np.sqrt(3)*LEFT + (i+1)*np.sqrt(3)/2*RIGHT, color = YELLOW, fill_opacity = 0.3, stroke_width = 0
                               ).shift(offset).save_state().shift(offsets_2[int(i/2)]) for i in range(8)]
        offsets_3 = [i*np.sqrt(3)/5*RIGHT for i in [6, 5, 3, 2, -2, -3, -5, -6]]
        self.remove(*triangles_2).add(*triangles_3).play(*[triangles_3[i].animate.restore().shift(offsets_3[i]).set_opacity(0.2) for i in range(8)])
        triangles_4 = [Polygon(3.5*UP, 2.5*DOWN + 2*np.sqrt(3)*LEFT + i*np.sqrt(3)/4*RIGHT, 2.5*DOWN + 2*np.sqrt(3)*LEFT + (i+1)*np.sqrt(3)/4*RIGHT, color = YELLOW, fill_opacity = 0.2, stroke_width = 0
                               ).shift(offset).save_state().shift(offsets_3[int(i/2)]) for i in range(16)]
        offsets_4 = [i*np.sqrt(3)/6*RIGHT for i in [8, 7.5, 6.5, 6, 4, 3.5, 2.5, 2, -2, -2.5, -3.5, -4, -6, -6.5, -7.5, -8]]
        self.remove(*triangles_3).add(*triangles_4).play(*[triangles_4[i].animate.restore().shift(offsets_4[i]).set_opacity(0.15) for i in range(16)])
        self.wait(1+2+0-4, 21+14+17) #但这一主题的视频 基本都只介绍了贝西科维奇的构造 （空闲）

        self.fade_out(excepts = [video_1, video_2, video_3])
        self.wait(0, 13) #在他的构造中
        line = Line(UP + 3*LEFT, UP + RIGHT, stroke_width = 8)
        region_1 = Line(UP + 3*LEFT, UP + RIGHT, color = YELLOW)
        self.play(ShowCreation(line))
        self.add(region_1, line).play(line.animate.shift(6*RIGHT), region_1.animate.put_start_and_end_on(UP + 3*LEFT, UP + 7*RIGHT))
        region_2 = Arc(color = YELLOW, fill_opacity = 0.2)
        alpha = ValueTracker(0)
        def region_2_updater(mob: Arc):
            angle = alpha.get_value()
            mob.set_points(Arc(radius = 4, start_angle = PI, angle = angle).add_line_to(ORIGIN).shift(7*RIGHT+UP).get_points())
        region_2.add_updater(region_2_updater)
        self.add(region_2, line).play(Rotate(line, np.arctan(1/5), about_point = 7*RIGHT+UP), alpha.animate.set_value(np.arctan(1/5)))
        region_2.clear_updaters()
        region_3 = Line(7*RIGHT + UP, 7*RIGHT + UP - 4*unit(np.arctan(1/5)), color = YELLOW)
        self.add(region_3, line).play(line.animate.shift(10*LEFT + 2*DOWN + 4*unit(np.arctan(1/5))), region_3.animate.put_start_and_end_on(7*RIGHT + UP - 4*unit(np.arctan(1/5)), DOWN + 3*LEFT))
        region_4 = Arc(color = YELLOW, fill_opacity = 0.2)
        alpha = ValueTracker(0)
        def region_4_updater(mob: Arc):
            angle = alpha.get_value()
            mob.set_points(Arc(radius = 4, start_angle = np.arctan(1/5), angle = -angle).add_line_to(ORIGIN).shift(DOWN+3*LEFT).get_points())
        region_4.add_updater(region_4_updater)
        self.add(region_4, line).play(Rotate(line, -np.arctan(1/5), about_point = DOWN+3*LEFT), alpha.animate.set_value(np.arctan(1/5)))
        region_4.clear_updaters()
        self.wait(2+1+0-5, 24+23+20) #最重要的其实不是挂谷集的形状 而是保尔的平移技巧 （空闲）
        
        self.wait(1, 22) #而一个世纪后的现在

        self.fade_out()
        ratio_2 = 1 - 2*np.sin(PI/18)
        radius_2 = np.sqrt(3) * ratio_2
        ratio_3 = 1 - np.sin(PI/72)/np.sin(PI/18)
        radius_3 = radius_2 * ratio_3
        iter_0 = ArcBetweenPoints(np.sqrt(3)*unit(-PI/6), np.sqrt(3)*unit(7*PI/6), angle = PI, n_components = 24, stroke_width = 0, fill_opacity = 1, color = RED).scale(ratio_2*ratio_3, about_point = ORIGIN)
        iter_1 = Reuleaux(color = ORANGE, stroke_width = 0, fill_opacity = 1).scale(ratio_2*ratio_3, about_point = ORIGIN)
        sectors_2 = [Arc(radius = 3, start_angle = -TAU/3 + i*PI/9, angle = PI/9, n_components = 24, color = YELLOW, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path() for i in range(3)]
        sectors_2[0].shift(3*RIGHT*np.sin(PI/18)), sectors_2[1].rotate(PI, about_point = 3/2*np.cos(PI/18)*DOWN), sectors_2[2].shift(3*LEFT*np.sin(PI/18))
        group_2 = VGroup(*sectors_2).shift((3*np.sqrt(3)*np.sin(PI/18) + radius_2)*UP)
        iter_2 = VGroup(group_2, group_2.copy().rotate(TAU/3, about_point = ORIGIN), group_2.copy().rotate(-TAU/3, about_point = ORIGIN)).scale(ratio_3, about_point = ORIGIN)
        verticies_1 = [3*ratio_2/np.sqrt(3)*unit(PI/2), 3*ratio_2/np.sqrt(3)*unit(7*PI/6), 3*ratio_2/np.sqrt(3)*unit(-PI/6)]
        r = 3*np.cos(PI/18) - np.sqrt(3)*(1+np.sin(PI/18))
        verticies_2 = [verticies_1[2]+3*LEFT, r*unit(PI/6), verticies_1[0]+3*unit(-TAU/3), verticies_1[1]+3*unit(PI/3), r*unit(-PI/2), verticies_1[2]+3*unit(TAU/3), verticies_1[0]+3*unit(-PI/3), r*unit(5*PI/6), verticies_1[1]+3*RIGHT]
        LIMEGREEN = interpolate_color(LIME, GREEN, 0.75)
        sectors_3 = [Arc(radius = 3, start_angle = 4*PI/9, angle = PI/24, n_components = 24, color = LIMEGREEN, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path(), 
                   Arc(radius = 3, start_angle = 4*PI/9 + PI/24, angle = PI/36, n_components = 24, color = LIMEGREEN, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path(), 
                   Arc(radius = 3, start_angle = 5*PI/9 - PI/24, angle = PI/24, n_components = 24, color = LIMEGREEN, stroke_width = 0, fill_opacity = 1).add_line_to(ORIGIN).close_path()]
        sectors_3[0].shift(3*np.sin(PI/72)*LEFT), sectors_3[1].rotate(PI, about_point = 3/2*np.cos(PI/72)*UP), sectors_3[2].shift(3*np.sin(PI/72)*RIGHT)
        group_3 = VGroup(*sectors_3).shift(3*np.sin(PI/72)/np.tan(PI/18)*DOWN)
        angles = [-4*PI/9, 2*PI/3, -2*PI/9, 8*PI/9, 0, -8*PI/9, 2*PI/9, -2*PI/3, 4*PI/9]
        iter_3 = VGroup(*[group_3.copy().rotate(angles[i], about_point = ORIGIN).shift(ratio_3*verticies_2[i]) for i in range(9)])
        self.fade_in(iter_3, iter_2, iter_1, iter_0)
        self.wait(0, 22) #构造一个挂谷集已经不需要平移技巧了
        self.wait(0, 21) #（空闲）

        def triple_there_and_back(t: float):
            return there_and_back((3*t)%1)
        less_pause = smooth_boot(1/6)
        triangle_3 = Polygon(radius_3*UP, radius_3*unit(-PI/6), radius_3*unit(7*PI/6), color = GREY_B, stroke_width = 0, fill_opacity = 0.8)
        boundary_3 = triangle_3.copy().set_style(stroke_width = 6, fill_opacity = 0, stroke_color = WHITE)
        self.play(FadeIn(triangle_3, remover = True, rate_func = triple_there_and_back), ShowPassingFlash(boundary_3, rate_func = less_pause), run_time = 3)
        self.wait(1+2-3, 23+1) #我们唯一需要关注的 只是面积重复利用的方式
        self.wait(0, 24) #（空闲）

        self.clear().add(self.notice)
        like = Text("", font = 'vanfont').scale(2).shift(3*LEFT)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').scale(2).shift(3*RIGHT)
        sanlian = VGroup(like, coin, star)
        self.play(*[GrowFromCenter(mob) for mob in sanlian])
        self.play(ApplyMethod(sanlian.set_color, "#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian])
        self.wait(0, 21) #如果比起别的挂谷猜想的视频
        self.wait(2, 29) #这期视频带给你了一些不一样的收获
        self.wait(2, 0) #不妨一键三连支持一下
        self.wait(0, 28) #（空闲）

        self.play(FadeOut(sanlian), self.change_notice())
        equation = MTex(r"\frac{a}{b+c}+\frac{b}{c+a}+\frac{c}{a+b}=4").shift(2*UP)
        self.play(Write(equation))
        self.wait(2+0-3, 27+22) #下期视频我打算讲一讲一些二元不定方程 （空闲）

        self.wait(2, 17) #你能想象形式这么简单的题目
        x = MTex(r"a=154476802108746166441951315019919837485664325669565431700026634898253202035277999").scale(0.6)
        x.shift(6*LEFT - x[1].get_center())
        y = MTex(r"b=36875131794129999827197811565225474825492979968971970996283137471637224634055579").scale(0.6).add(VMobject())
        y.shift(6*LEFT + 0.5*DOWN - y[1].get_center())
        z = MTex(r"c=4373612677928697257861252602371390152816537558161613618621437993378423467772036").scale(0.6).add(VMobject(), VMobject())
        z.shift(6*LEFT + DOWN - z[1].get_center())
        self.play(FadeIn(x, 0.2*LEFT, lag_ratio = 0.2), FadeIn(y, 0.2*LEFT, lag_ratio = 0.2), FadeIn(z, 0.2*LEFT, lag_ratio = 0.2), run_time = 3) #它的最小正整数解有这么长吗 （空闲）
        
        elliptic = MTex(r"y^2=x^3+109x^2+224x").shift(3*UP)
        self.play(FadeIn(elliptic, 0.5*DOWN), equation.animate.shift(0.5*DOWN))
        self.wait(1, 5) #应该有一部分观众听说过
        self.wait(2, 8) #这道题需要用到椭圆曲线去解
        self.wait(0, 20) #（空闲）

        self.wait(2, 10) #正是因为这些钓鱼题的存在
        self.wait(2, 28) #椭圆曲线作为二元三次不定方程
        self.wait(3, 10) #它的知名度居然会比二元二次不定方程还要高
        self.wait(0, 24) #（空闲）
        self.wait(2, 22) #二元二次方程明显要更简单
        self.wait(2+0-1, 5+24) #
        self.fade_out() #而下期视频将会从它开始 （空闲）

        painting = StarrySky()
        star = painting.star
        self.clear().play(FadeIn(painting, lag_ratio = 0.01, run_time = 2), self.change_notice())
        self.wait(0, 8) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, 0.5*UP), FadeIn(text_name, 0.5*UP))
        self.wait(1, 16) #而我 就像我的名字一样

        self.play(FadeOut(painting.others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star.shift, DOWN))
        self.wait(1, 16) #想要把天上的星星垂下来

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
        self.wait(2+0-2, 0+23) #变成指引前路的火光 （空闲）
        
        self.remove(star, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.wait(2, 6) #我是乐正垂星 我们下期视频再见

        self.wait(4, 27)
        self.fade_out(end = True)
        self.wait(4)


        
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]