from manimlib import *
import numpy as np

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

OMEGA = unit(-PI/6)

####################################################################    

class Notice(VGroup):
    def __init__(self, m_text1, m_text2, **kwargs):

        super().__init__(**kwargs)
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        if self.line1.get_height() < 0.5:
            self.line1.scale(1.25)
        if self.line2.get_height() < 0.5:
            self.line2.scale(1.25)
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

class FixedNotice(VMobject):
    def __init__(self, m_text1, m_text2):
        super().__init__(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True)
        notice = Notice(m_text1, m_text2)
        self.set_points(notice.get_all_points())

class FixedText(VMobject):
    def __init__(self, text, **kwargs):
        super().__init__(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True)
        notice = Text(text, **kwargs)
        #self.set_points(notice.get_all_points())
        for mob in notice.submobjects:
            new_submob = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(mob.get_all_points())
            self.add(new_submob)


class FixedTex(VMobject):
    def __init__(self, text, **kwargs):
        super().__init__(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True)
        notice = MTex(text, **kwargs)
        self.set_points(notice.get_all_points())

BACK = "#333333"

class FocusInterpolate(Homotopy):
    CONFIG = {
        "run_time": 2,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs, locals())
        
        def homotopy(x, y, z, t):
            position = np.array([x, y, z])
            inverse_focus = t/2
            result = 1/(position[0]*inverse_focus+1)*position
            return result

        super().__init__(homotopy, mobject, **kwargs)

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


#########################################################################

class Intro0(Scene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("遇到了什么问题，\n在引发自己的思考之前，\n至少应该看清楚它的样子。", font = 'simsun', t2c={"问题": GREEN, ("引发", "思考"): BLUE, "看清楚": YELLOW})
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DOWN + RIGHT), DOWN)
        ##  Showing object
        self.play(Write(quote), runtime = 2)
        self.play(Write(author), Write(notice0))
        self.wait(2)
        self.play(FadeOut(quote), FadeOut(author))
        self.wait(1)

class Intro1(Scene):
    def construct(self):

        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        notice1 = Notice("视频前言", "请听介绍")
        notice2 = Notice("文献综述", "请　模仿")
        notice3 = Notice("频道特色", "不能不品尝")
        notice4 = Notice("观前叠甲", "不要打架")
        notice5 = Notice("传统艺能", "请　三连")

        thelen = ArcBetweenPoints(DOWN*2, UP*2, PI/6, color = GREEN, fill_opacity = 1, fill_color = average_color(GREEN, BACK)).append_points(ArcBetweenPoints(UP*2, DOWN*2, PI/6).get_points())
        label_left_1 = MTex("f").scale(0.5).shift(2*LEFT+0.5*DOWN)
        label_right_1 = MTex("f").scale(0.5).shift(2*RIGHT+0.5*DOWN)
        label_left_2 = MTex("2f").scale(0.5).shift(4*LEFT+0.5*DOWN)
        label_right_2 = MTex("2f").scale(0.5).shift(4*RIGHT+0.5*DOWN)
        bench = Rectangle(width = 12, height = 0.2, fill_opacity = 1, fill_color = average_color(BLUE, BACK)).add(*[Line(0.1*UP, 0.1*DOWN).shift((i-2)*2*RIGHT) for i in (0, 1, 3, 4)], label_left_1, label_left_2, label_right_1, label_right_2)
        shade_left = Rectangle(width = 8, height = 2, fill_opacity = 1, stroke_width = 0, fill_color = BACK).shift(4*LEFT)
        shade_right = Rectangle(width = 8, height = 2, fill_opacity = 1, stroke_width = 0, fill_color = BACK).shift(4*RIGHT)
        circle = Circle(radius = 0.8, color = PURPLE).shift(4*LEFT)
        dot_center = Dot(color = YELLOW)
        dot_any = Dot(color = YELLOW).shift(4*LEFT + 0.8*UP)
        line_1_1 = Line(4*LEFT + 0.8*UP, 0.8*UP, color = YELLOW)
        line_1_2 = Line(4*LEFT + 0.8*UP, ORIGIN, color = YELLOW)
        line_1_3 = Line(4*LEFT + 0.8*UP, 0.8*DOWN, color = YELLOW)
        intersection_1 = Dot(color = YELLOW).shift(0.8*UP)
        intersection_2 = Dot(color = YELLOW).shift(0.8*DOWN)
        line_2_1 = Line(0.8*UP, 4*RIGHT + 0.8*DOWN, color = YELLOW)
        line_2_2 = Line(ORIGIN, 4*RIGHT + 0.8*DOWN, color = YELLOW)
        line_2_3 = Line(0.8*DOWN, 4*RIGHT + 0.8*DOWN, color = YELLOW)
        image = Dot(color = YELLOW).shift(4*RIGHT + 0.8*DOWN)

        def len_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[0]+focus)*point

        def line_1_1_updater(mob: Line):
            position = dot_any.get_center()
            other_end = np.array([0, position[1], 0])
            mob.put_start_and_end_on(position, other_end)
        def line_1_2_updater(mob: Line):
            position = dot_any.get_center()
            mob.put_start_and_end_on(position, ORIGIN)
        def line_1_3_updater(mob: Line):
            position = dot_any.get_center()
            other_end = np.array([0, 2*position[1]/(position[0]+2), 0])
            mob.put_start_and_end_on(position, other_end)
        def intersection_1_updater(mob: Dot):
            position = dot_any.get_center()
            mob_position = np.array([0, position[1], 0])
            mob.move_to(mob_position)
        def intersection_2_updater(mob: Dot):
            position = dot_any.get_center()
            mob_position = np.array([0, 2*position[1]/(position[0]+2), 0])
            mob.move_to(mob_position)
        def line_2_1_updater(mob: Line):
            position = dot_any.get_center()
            start = np.array([0, position[1], 0])
            end = len_trans(position)
            mob.put_start_and_end_on(start, end)
        def line_2_2_updater(mob: Line):
            position = dot_any.get_center()
            start = ORIGIN
            end = len_trans(position)
            mob.put_start_and_end_on(start, end)
        def line_2_3_updater(mob: Line):
            position = dot_any.get_center()
            end = len_trans(position)
            start = np.array([0, end[1], 0])
            mob.put_start_and_end_on(start, end)
        def image_updater(mob: Dot):
            position = len_trans(dot_any.get_center())
            mob.move_to(position)
        self.add(bench, shade_left, shade_right).play(ReplacementTransform(notice0, notice1), shade_left.animate.shift(8*LEFT), shade_right.animate.shift(8*RIGHT), ShowCreation(thelen), FadeIn(dot_center))
        self.remove(shade_left, shade_right)
        self.play(ShowCreation(circle))
        self.waiting(0, 29) #如果我们在凸透镜的一侧放一个圆
        self.play(ShowCreation(line_1_1, rate_func = rush_into), ShowCreation(line_1_2, rate_func = rush_into), ShowCreation(line_1_3, rate_func = rush_into), FadeIn(dot_any), run_time = 0.5)
        self.play(FadeIn(intersection_1), FadeIn(intersection_2), ShowCreation(line_2_1, rate_func = rush_from), ShowCreation(line_2_2, rate_func = rush_from), ShowCreation(line_2_3, rate_func = rush_from), run_time = 0.5)
        self.play(ShowCreation(image))
        self.waiting(0, 10) #另一侧的成像会是什么样的？
        self.waiting(0, 21) #（空闲）

        cover_0 = ImageMobject("cover_0.jpg", height = 2).shift(2.5*RIGHT+2.5*UP)
        bv_0 = Text("BV1S34y1Y7Tb", font = "Times New Roman").scale(0.5).next_to(cover_0, UP, buff = 0.1)
        self.play(FadeIn(cover_0, 0.5*UP), FadeIn(bv_0, 0.5*UP))
        self.waiting(2, 15) #这是八个月前的一期视频中提到的一道题目

        line_1_1.add_updater(line_1_1_updater)
        line_1_2.add_updater(line_1_2_updater)
        line_1_3.add_updater(line_1_3_updater)
        intersection_1.add_updater(intersection_1_updater)
        intersection_2.add_updater(intersection_2_updater)
        line_2_1.add_updater(line_2_1_updater)
        line_2_2.add_updater(line_2_2_updater)
        line_2_3.add_updater(line_2_3_updater)
        image.add_updater(image_updater)
        trace_right = TracedPath(image.get_center, stroke_color = BLUE, stroke_width = 4)
        self.add(trace_right, line_2_1, line_2_2, line_2_3, image).play(Rotate(dot_any, TAU, about_point = 4*LEFT), run_time = 2)
        trace_right.clear_updaters()
        self.waiting(1+0-2, 21+21) # 答案是一个椭圆 （空闲）

        axis = DashedLine(2*UP, 2*DOWN).shift((1.6/0.6+2.4/1.4)*RIGHT)
        self.play(FadeOut(cover_0), FadeOut(bv_0), ShowCreation(axis))
        self.waiting(0, 27) # 它居然是左右对称的
        self.waiting(3, 6) # 看起来完全不像凸透镜能成像出来的东西
        self.waiting(0, 18) #（空闲）


        with_updater = [line_1_1, line_1_2, line_1_3, intersection_1, intersection_2, line_2_1, line_2_2, line_2_3, image]
        for mob in with_updater:
            mob.clear_updaters()
        self.remove(trace_right, dot_any, dot_center, *with_updater, thelen, bench, circle, axis)

        cover_0 = ImageMobject("cover_0.jpg", height = 2).shift(4.5*RIGHT)
        bv_0 = Text("BV1S34y1Y7Tb", font = "Times New Roman").scale(0.5).next_to(cover_0, UP, buff = 0.1)
        calculate_0 = ImageMobject("calculate_0.png", height = 5).shift(2*LEFT)
        surrounding = SurroundingRectangle(calculate_0)
        cover_1 = ImageMobject("cover_2.jpg", height = 2).shift(4.5*RIGHT)
        bv_1 = Text("BV1Da411Z7oy", font = "Times New Roman").scale(0.5).next_to(cover_0, UP, buff = 0.1)
        calculate_1 = ImageMobject("calculate_2.png", height = 5).shift(2*LEFT)
        cover_2 = ImageMobject("cover_1.jpg", height = 2).shift(4.5*RIGHT)
        bv_2 = Text("BV1JU4y1X7WP", font = "Times New Roman").scale(0.5).next_to(cover_0, UP, buff = 0.1)
        calculate_2 = ImageMobject("calculate_1.png", height = 5).shift(2*LEFT)
        self.play(ReplacementTransform(notice1, notice2), ShowCreation(surrounding), FadeIn(calculate_0), FadeIn(cover_0, 0.5*UP), FadeIn(bv_0, 0.5*UP))
        self.waiting(4, 0)
        self.play(FadeTransform(calculate_0, calculate_1, stretch = False) , FadeIn(cover_1, 0.5*UP), FadeIn(bv_1, 0.5*UP), FadeOut(cover_0, 0.5*UP), FadeOut(bv_0, 0.5*UP))
        self.waiting(4, 0)
        self.play(FadeTransform(calculate_1, calculate_2, stretch = False) , FadeIn(cover_2, 0.5*UP), FadeIn(bv_2, 0.5*UP), FadeOut(cover_1, 0.5*UP), FadeOut(bv_1, 0.5*UP))
        self.waiting(2+1+2+0+2+2+1+0-11, 16+28+9+16+7+17+7+20) #这道题引起了广泛的讨论 包括视频的原作者在内 很多人都给出了自己的证法 （空闲） 当然 不出意外的是 这些证法全都带有大量的计算 十分地不友好 （空闲）
        
        self.play(ReplacementTransform(notice2, notice3))
        self.waiting(1, 0) #这里是一个数学频道
        colors = [GREY_A, GREY_B, GREY_C, GREY_D, BACK]
        n_layers = len(colors)
        shade = Rectangle(height = 8, width = 16, fill_opacity = 1, stroke_width = 0)
        shades = shade.replicate(n_layers)
        alpha = ValueTracker(0.0)
        lag_ratio = 0.2
        def sub_updater(index: int):
            def util(mob: Rectangle):
                value = alpha.get_value()
                subvalue = clip(value*(1+(n_layers-1)*lag_ratio)-index*lag_ratio, 0, 1)
                if subvalue > 0:
                    mob.restore().scale(np.array([1, subvalue, 1]))
            return util
        for i in range(n_layers):
            shades[i].set_color(colors[i]).save_state()
            shades[i].set_opacity(0).add_updater(sub_updater(i))
        shade_left = Rectangle(height = 8, width = 8, fill_opacity = 1, stroke_width = 0).shift(4*LEFT)
        shades_left = shade_left.replicate(n_layers)
        shade_right = Rectangle(height = 8, width = 8, fill_opacity = 1, stroke_width = 0).shift(4*RIGHT)
        shades_right = shade_right.replicate(n_layers)
        for i in range(n_layers):
            shades_left[i].set_color(colors[i])
            shades_right[i].set_color(colors[i])
        self.add(*shades, notice3).play(alpha.animate.set_value(1), run_time = 1.3)
        self.remove(*shades, cover_2, bv_2, calculate_2, surrounding).add(bench, thelen, dot_center, *shades_left, *shades_right, notice3)
        self.play(LaggedStart(*[ApplyMethod(mob.shift, 8*LEFT) for mob in shades_left[::-1]], group = VGroup(), lag_ratio = 0.1, run_time = 1.2), LaggedStart(*[ApplyMethod(mob.shift, 8*RIGHT) for mob in shades_right[::-1]], group = VGroup(), lag_ratio = 0.1, run_time = 1.2))
        self.waiting(0, 9) #肯定不会像他们那样暴力计算

        grids = 8
        grid_group = 5
        major_lines = VGroup()
        minor_lines = VGroup()
        lines_h = VGroup()
        alpha = ValueTracker(0.0)
        def horizontal_updater(height: float):
            def util(mob: Line):
                value = alpha.get_value()
                left_end = np.array([-8, height*(1+value*8), 0])
                right_end = np.array([8, height*(1-value*8), 0])
                mob.put_start_and_end_on(left_end, right_end)
            return util
        for i in range(grids*grid_group + 1):
            height = -(i/grid_group-grids/2)
            line_i = Line(8*LEFT, 8*RIGHT, color = BLUE).shift(height*UP)
            if i % 5 != 0:
                line_i.set_stroke(width = 2, color = BLUE)
                minor_lines.add(line_i.copy())
            else:
                major_lines.add(line_i.copy())
            line_i.add_updater(horizontal_updater(height))
            lines_h.add(line_i)
        
        grids = 100
        grid_group = 5
        lines_v = VGroup()
        center_v = VGroup()
        for i in range(grids*grid_group + 1):
            position = i/grid_group-50
            line_i = Line(4*UP, 4*DOWN, color = BLUE).shift((i/grid_group-50)*RIGHT)
            if i % 5 != 0:
                line_i.set_stroke(width = 2, color = BLUE)
                minor_lines.add(line_i.copy())
            else:
                major_lines.add(line_i.copy())
            lines_v.add(line_i)
            if abs(position) < 8:
                center_v.add(line_i)
        grid = VGroup(minor_lines, major_lines).set_color(GREY).set_opacity(0.5)
        self.bring_to_back(center_v, lines_h).play(Write(lines_h), Write(center_v), run_time = 2)
        self.waiting(0, 16) #只要我们能找得到几何结构
        self.remove(center_v).bring_to_back(grid, lines_v).play(FocusInterpolate(lines_v), alpha.animate.set_value(1/2), run_time = 2)
        for mob in lines_h:
            mob.clear_updaters()
        self.waiting(0, 6) #计算部分自然能少就少
        self.waiting(0, 24) #（空闲）

        former_smooth = squish_rate_func(smooth, 0, 0.5)
        latter_smooth = squish_rate_func(smooth, 0.5, 1)
        former_half = squish_rate_func(rush_into, 0, 0.5)
        latter_half = squish_rate_func(rush_from, 0.5, 1)
        dot_any.set_color(GREY)
        image.set_color(BLUE)
        anims = [FadeIn(dot_any, rate_func = former_smooth), ShowCreation(line_1_1, rate_func = former_half), ShowCreation(line_1_2, rate_func = former_half), ShowCreation(line_1_3, rate_func = former_half), FadeIn(intersection_1, rate_func = latter_smooth), FadeIn(intersection_2, rate_func = latter_smooth), ShowCreation(line_2_1, rate_func = latter_half), ShowCreation(line_2_2, rate_func = latter_half), ShowCreation(line_2_3, rate_func = latter_half)]
        self.add(*with_updater, dot_any).play(lines_h.animate.fade(), lines_v.animate.fade(), *anims, ReplacementTransform(notice3, notice4))
        self.play(ShowCreation(image))
        line_1_1.add_updater(line_1_1_updater)
        line_1_2.add_updater(line_1_2_updater)
        line_1_3.add_updater(line_1_3_updater)
        intersection_1.add_updater(intersection_1_updater)
        intersection_2.add_updater(intersection_2_updater)
        line_2_1.add_updater(line_2_1_updater)
        line_2_2.add_updater(line_2_2_updater)
        line_2_3.add_updater(line_2_3_updater)
        image.add_updater(image_updater)
        self.waiting(1.5, 0)
        self.play(dot_any.animate.shift(2*LEFT + UP), run_time = 1.5)
        self.waiting(1.5, 0)
        self.play(dot_any.animate.shift(4.8*RIGHT + DOWN), run_time = 1.5)
        self.waiting(1+3+2+2-8, 17+11+16+14) #为了方便起见 这期视频不会考虑成像会被遮挡的问题 也不区分实像和虚像 我们只研究这么一件事情
        for mob in with_updater:
            mob.clear_updaters()
        self.play(*[FadeOut(mob) for mob in with_updater], FadeOut(dot_any), lines_h.animate.set_opacity(1), lines_v.animate.set_opacity(1))
        self.waiting(1, 25) #平面上的每一个点通过凸透镜以后
        self.waiting(1+0-1, 21+15) #像会跑到哪里 （空闲）
        self.play(*[FadeOut(mob) for mob in [lines_h, grid, bench, thelen, dot_center]], lines_v.animate.set_opacity(0.0)) #奇怪的问题：FadeOut(lines_v)不工作，可能是无穷的原因
        self.remove(lines_v)

        like = Text("", font = 'vanfont').shift(3*LEFT).scale(2)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT).scale(2)
        sanlian = VGroup(like, coin, star)

        self.play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, np.array([0,0,0])), FadeInFromPoint(star, 3*RIGHT), ReplacementTransform(notice4, notice5))
        self.play(Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), ApplyMethod(sanlian.set_color, "#00A1D6"))
        self.waiting(3-2,3) #长按点赞一键三连 我们开始吧
        
        self.waiting(3, 0)
        self.play(FadeOut(notice5), FadeOut(sanlian))
        self.waiting(3, 0) #到此共67秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#########################################################################

class Chapter1_0(Scene):

    def construct(self):

        text1 = Text("第一节 凸透镜成像", font = 'simsun', t2c={"第一节": YELLOW, "凸透镜": GREEN, "成像": BLUE}).scale(1.25)

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(Scene):
    def construct(self):
        notice1 = Notice("初中物理", "请　复习")
        notice2 = Notice("非近轴光学", "请别找高斯")
        notice3 = Notice("近轴光学", "请找高斯")

        thelen = ArcBetweenPoints(DOWN*3, UP*3, PI/6, color = GREEN, fill_opacity = 1, fill_color = average_color(GREEN, BACK)).append_points(ArcBetweenPoints(UP*3, DOWN*3, PI/6).get_points())
        label_left_1 = MTex("f").scale(0.5).shift(2*LEFT+0.5*DOWN)
        label_right_1 = MTex("f").scale(0.5).shift(2*RIGHT+0.5*DOWN)
        label_left_2 = MTex("2f").scale(0.5).shift(4*LEFT+0.5*DOWN)
        label_right_2 = MTex("2f").scale(0.5).shift(4*RIGHT+0.5*DOWN)
        labels = VGroup(label_left_1, label_right_1, label_left_2, label_right_2)
        bench = Rectangle(width = 12, height = 0.2, fill_opacity = 1, fill_color = average_color(BLUE, BACK)).add(*[Line(0.1*UP, 0.1*DOWN).shift((i-2)*2*RIGHT) for i in (0, 1, 3, 4)], labels)
        shade_left = Rectangle(width = 8, height = 2, fill_opacity = 1, stroke_width = 0, fill_color = BACK).shift(4*LEFT)
        shade_right = Rectangle(width = 8, height = 2, fill_opacity = 1, stroke_width = 0, fill_color = BACK).shift(4*RIGHT)
        dot_center = Dot(color = YELLOW)
        
        self.add(bench, shade_left, shade_right).play(Write(notice1), shade_left.animate.shift(8*LEFT), shade_right.animate.shift(8*RIGHT), ShowCreation(thelen), FadeIn(dot_center))
        self.remove(shade_left, shade_right)
        self.waiting(2, 29) #凸透镜的基本性质 想必大家都已经十分熟悉了
        self.waiting(0, 23) #（空闲）
        self.waiting(2, 2) #我们在初二就学过

        lines_1 = []
        for i in range(9):
            height = (i-4)*0.4*UP
            line_i = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([height+5*LEFT, height, -1.5*height+5*RIGHT])
            lines_1.append(line_i)
        self.play(*[ShowCreation(mob) for mob in lines_1], run_time = 1.5)
        self.waiting(2.5, 29) #平行于主光轴的光线 经过凸透镜后会汇聚于焦点
        lines_2 = []
        for i in range(9):
            height = (i-4)*0.4*UP
            line_i = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([-1.5*height+5*LEFT, height, height+5*RIGHT])
            lines_2.append(line_i)
            lines_1[i].reverse_points()
        self.play(*[ShowCreation(mob) for mob in lines_2], *[Uncreate(mob) for mob in lines_1], run_time = 1.5)
        self.waiting(2.5, 16) #穿过焦点的光线 经过凸透镜后会平行于主光轴
        lines_3 = []
        for i in range(9):
            height = (i-4)*0.4*UP
            line_i = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([-1.25*height+5*LEFT, ORIGIN, -1.25*height+5*RIGHT])
            lines_3.append(line_i)
            lines_2[i].reverse_points()
        self.play(*[ShowCreation(mob) for mob in lines_3], *[Uncreate(mob) for mob in lines_2], run_time = 1.5)
        self.waiting(2.5, 1) #而穿过凸透镜光心的光线 则不会发生偏折
        self.waiting(0, 20) #（空闲）
        for i in range(9):
            lines_3[i].reverse_points()
        self.play(*[Uncreate(mob) for mob in lines_3], run_time = 1.5)
        self.waiting(1.5, 29) #借此 我们可以确定凸透镜成像的规律

        def len_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[0]+focus)*point

        start = 10/3*LEFT + 1.2*UP
        end = len_trans(start)
        point_any = Dot(color = YELLOW).shift(start)
        point_image = Dot(color = YELLOW).shift(end)
        lines_2 = []
        lines_3 = []
        for i in range(9):
            height = (i-4)*0.6*UP
            line_i = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, height, end])
            line_j = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, height, end+0.2*RIGHT+0.02*(i-4)*abs(i-4)*DOWN])
            lines_2.append(line_i)
            lines_3.append(line_j)
        self.play(ShowCreation(point_any))
        self.waiting(0, 5) #从一点出发的所有光线......
        self.play(*[ShowCreation(mob) for mob in lines_2], run_time = 2)
        self.waiting(2, 6) #......经过凸透镜折射后 会经过同一个点
        self.waiting(0, 14) #（空闲）

        self.play(ShowCreation(point_image))
        self.waiting(1, 5) #这一点就是我们要求的像
        self.waiting(1, 1) #（空闲）

        self.play(ReplacementTransform(notice1, notice2))
        self.waiting(3, 3) #但是 不知道大家有没有想过这么一个问题
        self.play(FadeOut(point_image), *[Transform(lines_2[i], lines_3[i]) for i in range(9)])
        self.waiting(1, 26) #这些折射光线真的会经过同一个点吗
        self.waiting(0, 25) #（空闲）

        self.play(*[FadeOut(mob) for mob in [point_any, *lines_2]])
        self.waiting(0, 21) #应该有不少人知道
        self.waiting(2, 28) #满足三条基本性质的凸透镜是不存在的
        self.waiting(0, 15) #（空闲）

        lines = []
        for i in range(9):
            height = (i-4)*0.4
            start = height*UP + 5*LEFT
            left = np.array([2*(height**2/45-1/5), height, 0])
            left_1 = (start*3+left)/4
            left_2 = (start*2+left*2)/4
            left_3 = (start+left*3)/4
            right = np.array([2*(1/5-(height*0.95)**2/45), height*0.95, 0])
            end = 1.5*height*DOWN + 5*RIGHT + 0.12*(i-4)*abs(i-4)*DOWN
            right_1 = (right*3+end)/4
            right_2 = (right*2+end*2)/4
            right_3 = (right+end*3)/4
            line_i = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, left_1, left_2, left_3, left, right, right_1, right_2, right_3, end])
            lines.append(line_i)
        surrounding = Rectangle(height = 1, width = 1, color = RED).shift(1.6*RIGHT)

        self.play(*[ShowCreation(mob) for mob in lines], run_time = 2)
        self.play(ShowCreation(surrounding))
        self.waiting(0, 13) #现实中的凸透镜都会不可避免地带有像差
        self.waiting(3, 8) #这三条基本性质都只是近似成立

        ideal_len = Line(3*UP, 3*DOWN).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN)
        ideal_bench = NumberLine([-6, 6, 2], stroke_width = 8, color = BLUE)
        lines_1 = []
        for i in range(9):
            height = (i-4)*0.4*UP
            line_i = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([height+5*LEFT, height, -1.5*height+5*RIGHT])
            lines_1.append(line_i)
        former_half = squish_rate_func(rush_into, 0, 0.5)
        latter_half = squish_rate_func(rush_from, 0.5, 1)
        self.add(bench, ideal_bench, thelen, ideal_len, labels, dot_center, *lines, *lines_1, surrounding).play(*[FadeOut(mob, rate_func = former_half) for mob in [thelen, bench, *lines, surrounding]], *[FadeOut(mob, rate_func = there_and_back, remover = False) for mob in [labels, dot_center]], *[FadeIn(mob, rate_func = latter_half) for mob in [ideal_len, ideal_bench, *lines_1]], ReplacementTransform(notice2, notice3))
        self.add(labels).waiting(0, 29) #符合这三条基本性质的
        self.waiting(2, 3) #只能是一片理想凸透镜
        self.waiting(0, 17) #（空闲）

        start = 10/3*LEFT + 1.2*UP
        end = len_trans(start)
        lines_2 = []
        for i in range(9):
            height = (i-4)*0.6*UP
            line_i = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, height, end])
            lines_2.append(line_i)
        self.play(ShowCreation(point_any), *[FadeOut(mob) for mob in lines_1])
        self.play(*[ShowCreation(mob) for mob in lines_2], run_time = 2)
        self.waiting(2+3-3, 2+10) #那在这片理想的凸透镜上 所有折射光线就会经过同一个点吗
        self.waiting(2, 2) #这是不是另一种近似呢
        self.waiting(0, 18) #（空闲）

        self.play(*[FadeOut(mob) for mob in lines_2])
        self.waiting(1, 5) #即使是最简单的情况
        self.waiting(1, 25) #我们从一点出发
        line_1 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, 1.2*UP, 2.4*DOWN+6*RIGHT])
        line_2 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, ORIGIN, 2.16*DOWN+6*RIGHT])
        line_3 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, 1.8*DOWN, 1.8*DOWN+6*RIGHT])
        self.waiting(0, 14) #发出......
        self.play(ShowCreation(line_1))
        self.waiting(0, 10) #......平行于主光轴......
        self.play(ShowCreation(line_2)) #......过光心......
        self.play(ShowCreation(line_3))
        self.waiting(0, 29) #.......过焦点的三条光线

        point_image.set_fill(opacity = 0).set_stroke(width = 4).scale(4)
        self.play(ShowCreation(point_image))
        self.play(point_image.animate.scale(0.25))
        self.waiting(0, 27) #这三条光线就一定会交于一点吗

        self.waiting(4, 0) #到此共82秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30) 

class Chapter1_2(Scene):
    def construct(self):
        notice3 = Notice("近轴光学", "请找高斯")
        notice4 = Notice("中考几何", "请　显然")
        notice5 = Notice("村规私设", "请勿模仿")

        ideal_len = Line(3*UP, 3*DOWN).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN)
        ideal_bench = NumberLine([-6, 6, 2], stroke_width = 8, color = BLUE)
        label_left_1 = MTex("f").scale(0.5).shift(2*LEFT+0.5*DOWN)
        label_right_1 = MTex("f").scale(0.5).shift(2*RIGHT+0.5*DOWN)
        label_left_2 = MTex("2f").scale(0.5).shift(4*LEFT+0.5*DOWN)
        label_right_2 = MTex("2f").scale(0.5).shift(4*RIGHT+0.5*DOWN)
        labels_old = VGroup(label_left_1, label_right_1, label_left_2, label_right_2)
        dot_center = Dot(color = YELLOW)

        def len_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[0]+focus)*point
        start = 10/3*LEFT + 1.2*UP
        end = len_trans(start)

        point_any = Dot(color = YELLOW).shift(start)
        circle_image = Dot(color = YELLOW, stroke_width = 4, fill_opacity = 0).shift(end)
        point_image = Dot(color = YELLOW).shift(end)
        line_1 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([2.4*DOWN+6*RIGHT, 1.2*UP, start])
        line_2 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([2.16*DOWN+6*RIGHT, ORIGIN, start])
        line_3 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([1.8*DOWN+6*RIGHT, 1.8*DOWN, start])
        
        line_4 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, 1.2*UP, end])
        line_5_0 = DashedLine(end, start, color = YELLOW, stroke_width = 2)
        line_5 = Line(start, end, color = YELLOW, stroke_width = 2)
        line_6 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, 1.8*DOWN, end])
        
        self.add(notice3, ideal_bench, labels_old, ideal_len, dot_center, point_any, line_1, line_2, line_3, circle_image)
        self.play(FadeOut(circle_image), FadeIn(point_image))
        self.waiting(2, 12) #令人安心的是 这不是另一种近似
        self.waiting(1, 22) #而是可以证明的结论
        self.waiting(0, 21) #（空闲）

        point_f1 = Dot(color = YELLOW).shift(2*LEFT)
        point_f2 = Dot(color = YELLOW).shift(2*RIGHT)
        point_p = Dot(color = YELLOW).shift(1.2*UP)
        point_q = Dot(color = YELLOW).shift(1.8*DOWN)
        label_a = MTex("A").scale(0.7).next_to(start, UP)
        label_b = MTex("B").scale(0.7).next_to(end, DOWN)
        label_f1 = MTex("F_{1}").scale(0.7).next_to(2*LEFT, DOWN)
        label_f2 = MTex("F_{2}").scale(0.7).next_to(2*RIGHT, DOWN)
        label_o = MTex("O").scale(0.7).next_to(ORIGIN, DL).shift(0.05*RIGHT)
        label_p = MTex("P").scale(0.7).next_to(1.2*UP, UR, buff = 0.15)
        label_q = MTex("Q").scale(0.7).next_to(1.8*DOWN, DL, buff = 0.15)
        labels = VGroup(point_p, point_q, point_f1, point_f2, label_a, label_b, label_p, label_q, label_o, label_f1, label_f2)
        self.add(line_4, line_5_0, line_6).play(ReplacementTransform(notice3, notice4), *[FadeOut(mob) for mob in [line_1, line_2, line_3, labels_old]], Write(labels, run_time = 2))
        self.waiting(1+2-2, 25+18) #验证这组三线共点 只是一道简单的平面几何习题而已
        self.waiting(0, 16) #（空闲）

        text_1 = r"F_1O\parallel AP"
        text_2 = r"\Delta F_1QO\sim \Delta AQP"
        text_3 = r"\frac{F_1O}{AP}=\frac{OQ}{PQ}"
        text_left = MTex(r"&" + text_1 + r"\\\Rightarrow &"+ text_2 +r"\\\Rightarrow &"+ text_3, isolate = [text_1, text_2, text_3, r"AP", r"F_1O", r"OQ", r"PQ", r"\Rightarrow"]).scale(0.7).next_to(7*LEFT + 2*UP, RIGHT)
        includes = text_left.get_parts_by_tex(r"\Rightarrow")
        text_left_1 = text_left.get_part_by_tex(text_1)
        text_left_2 = includes[0].add(text_left.get_part_by_tex(text_2))
        text_left_3 = includes[1].add(text_left.get_part_by_tex(text_3))
        text_1 = r"F_2O\parallel BQ"
        text_2 = r"\Delta F_2PO\sim \Delta BPQ"
        text_3 = r"\frac{F_2O}{BQ}=\frac{OP}{QP}"
        text_right = MTex(r"&" + text_1 + r"\\\Rightarrow &"+ text_2 +r"\\\Rightarrow &"+ text_3, isolate = [text_1, text_2, text_3, r"BQ", r"F_2O", r"OP", r"QP", r"\Rightarrow"]).scale(0.7).next_to(RIGHT + 2*UP, RIGHT)
        includes = text_right.get_parts_by_tex(r"\Rightarrow")
        text_right_1 = text_right.get_part_by_tex(text_1)
        text_right_2 = includes[0].add(text_right.get_part_by_tex(text_2))
        text_right_3 = includes[1].add(text_right.get_part_by_tex(text_3))
        self.play(WiggleOutThenIn(line_4), WiggleOutThenIn(line_6))
        self.waiting(1, 15) #我们设B是AP和AQ的折射光线的交点
        line_indicate_u = Line(start, 1.2*UP, stroke_width = 8)
        line_indicate_v = Line(end, 1.8*DOWN, stroke_width = 8)
        self.add(line_indicate_u, line_indicate_v, point_any, point_image, point_p, point_q).play(Write(text_left_1), Write(text_right_1), ShowPassingFlash(line_indicate_u), ShowPassingFlash(line_indicate_v))
        self.waiting(2, 25) #就可以根据AP BQ与主光轴分别平行
        self.play(Write(text_left_2), Write(text_right_2))
        self.waiting(1, 8) #得到对应的相似三角形
        self.play(Write(text_left_3), Write(text_right_3))
        self.waiting(0, 25) #以及这些线段的比例
        self.waiting(0, 20) #（空闲）

        text_down = MTex(r"\Rightarrow \frac{AP}{BQ}=\frac{OP}{OQ}", isolate = [r"AP", r"BQ", r"OP", r"OQ"]).scale(0.7).next_to(7*LEFT + DOWN, RIGHT)
        text_1 = r"\frac{f}{u}+\frac{f}{v}=\frac{OQ+OP}{PQ}=1"
        text_2 = r"\frac{1}{u}+\frac{1}{v}=\frac{1}{f}"
        text_end = MTex(
            text_1 + r"\Rightarrow " + text_2, 
            isolate = [text_1, r"\Rightarrow", text_2],
            tex_to_color_map = {(r"u", r"\frac{1}{u}"): PURPLE, (r"v", r"\frac{1}{v}"): ORANGE, (r"f", r"\frac{1}{f}"): BLUE, (r"OP", r"OQ", r"PQ"): GREEN},
            ).scale(0.7).next_to(7*LEFT + 2.2*DOWN, RIGHT)
        text_end_others = text_end.get_parts_by_tex([text_1, r"\Rightarrow"])
        formula = text_end.get_part_by_tex(text_2)
        surrounding = SurroundingRectangle(formula)
        line_indicate_op = Line(ORIGIN, 1.2*UP, stroke_width = 8)
        line_indicate_oq = Line(ORIGIN, 1.8*DOWN, stroke_width = 8)
        self.play(Write(text_down))
        self.play(ShowPassingFlash(line_indicate_u), ShowPassingFlash(line_indicate_v))
        self.waiting(1, 0)
        self.add(line_indicate_op, line_indicate_oq, point_p, point_q, dot_center).play(ShowPassingFlash(line_indicate_op), ShowPassingFlash(line_indicate_oq))
        self.waiting(1, 0) #于是 AP和BQ的比例就等于OP和OQ的比例
        self.play(Uncreate(line_5_0), ShowCreation(line_5))
        self.waiting(2, 0) #就有A O B三点共线的结论
        self.waiting(0, 16) #（空闲）

        line_u = Line(start, 1.2*UP, stroke_width = 8, color = PURPLE)
        line_v = Line(end, 1.8*DOWN, stroke_width = 8, color = ORANGE)
        label_u = MTex(r"u", color = PURPLE).scale(0.9).next_to(line_u, UP)
        label_v = MTex(r"v", color = ORANGE).scale(0.9).next_to(line_v, UP)
        label_f_l = MTex(r"f", color = BLUE).scale(0.6).next_to(LEFT, DOWN, buff = 0.11)
        label_f_r = MTex(r"f", color = BLUE).scale(0.6).next_to(RIGHT, UP, buff = 0.11)
        text_left_u = text_left.get_parts_by_tex(r"AP")
        text_left_f = text_left.get_parts_by_tex(r"F_1O")
        text_left_h = text_left.get_parts_by_tex([r"PQ", r"OQ"])
        text_right_v = text_right.get_parts_by_tex(r"BQ")
        text_right_f = text_right.get_parts_by_tex(r"F_2O")
        text_right_h = text_right.get_parts_by_tex([r"QP", r"OP"])
        text_down_u = text_down.get_parts_by_tex(r"AP")
        text_down_v = text_down.get_parts_by_tex(r"BQ")
        text_down_h = text_down.get_parts_by_tex([r"OP", r"OQ"])
        all_u = VGroup(text_left_u, text_down_u)
        all_v = VGroup(text_right_v, text_down_v)
        all_f = VGroup(text_left_f, text_right_f)
        all_h = VGroup(text_left_h, text_right_h, text_down_h)
        self.add(line_u, point_any, point_p).play(ShowCreation(line_u), ShowCreation(label_u), all_u.animate.set_color(PURPLE))
        self.waiting(1, 27) #而如果我们记AP为物距u
        self.add(line_v, point_image, point_q).play(ShowCreation(line_v), ShowCreation(label_v), all_v.animate.set_color(ORANGE))
        self.waiting(0, 29) #BQ为像距v
        self.play(ShowCreation(label_f_l), ShowCreation(label_f_r), all_f.animate.set_color(BLUE), all_h.animate.set_color(GREEN))
        self.waiting(1, 11) #并且将焦距记为f
        self.play(Write(text_end))
        self.play(ShowCreation(surrounding))
        self.waiting(2+0-3, 25+28) #还可以顺手得到凸透镜的成像公式 （空闲）

        offset = 5*LEFT + 1.5*DOWN - formula.get_corner(LEFT)
        self.play(formula.animate.shift(offset), surrounding.animate.shift(offset), *[FadeOut(mob, offset) for mob in [text_down, text_end_others]], FadeOut(text_left, offset/3), FadeOut(text_right, offset/3))
        self.waiting(1, 9) #我们可以把这个取像的过程
        self.waiting(1, 29) #看成是一个映射
        self.waiting(2, 15) #既然是通过凸透镜定义出来的
        title = Text("凸透镜变换", font = "simsun", color = YELLOW).scale(1.25).next_to(3.05*UP, UP)
        line_title = Line(3.1*UP, 3.1*UP)
        self.play(Write(title), line_title.animate.put_start_and_end_on(3.1*UP+6*LEFT, 3.1*UP+6*RIGHT), ReplacementTransform(notice4, notice5))
        self.waiting(1, 6) #那就叫它凸透镜变换好了
        self.waiting(0, 17) #（空闲）

        line_af = DashedLine(start, 2*LEFT, stroke_width = 1, color = YELLOW)
        line_bf = DashedLine(end, 2*RIGHT, stroke_width = 1, color = YELLOW)
        line_ao = Line(start, ORIGIN, stroke_width = 2, color = YELLOW)
        line_bo = Line(ORIGIN, end, stroke_width = 2, color = YELLOW)
        line_aq = Line(start, 1.8*DOWN, stroke_width = 2, color = YELLOW)
        line_bp = Line(1.2*UP, end, stroke_width = 2, color = YELLOW)
        self.remove(line_4, line_5, line_6).add(line_af, line_bf, line_ao, line_bo, line_aq, line_bp, line_u, line_v, point_any, point_image, point_p, point_q, point_f1, point_f2, dot_center, label_u, label_v, label_a, )
        circle_start = Circle(radius = 0.6, color = YELLOW).shift(start).save_state()
        circle_end = Circle(radius = 0.6, color = YELLOW).shift(end).save_state()

        alpha = ValueTracker(0.0)
        def circle_start_updater(mob: Circle):
            value = alpha.get_value()
            mob.restore().scale(value).pointwise_become_partial(mob, 0, value)
        circle_start.add_updater(circle_start_updater)
        self.add(circle_start).play(alpha.animate.set_value(1.0), rate_func = rush_from)
        circle_start.clear_updaters()
        self.play(circle_start.animate.scale(0), rate_func = rush_into)
        self.remove(circle_start)

        for mob in [line_4, line_5, line_6]:
            mob.set_stroke(width = 8)
        self.play(*[ShowPassingFlash(mob) for mob in [line_4, line_5, line_6]], rate_func = linear)
        self.play(*[ShowPassingFlash(mob) for mob in [line_4, line_5, line_6]], rate_func = linear)

        def circle_end_updater(mob: Circle):
            value = alpha.get_value()
            mob.restore().scale(value).pointwise_become_partial(mob, 0, value)
        self.play(circle_end.animate.scale(0), rate_func = lambda t: rush_into(1-t))
        circle_end.add_updater(circle_end_updater)
        self.play(alpha.animate.set_value(0.0))
        self.remove(circle_end)

        self.waiting(2+2+1-6, 14+2+19) # 这个映射将平面上的一个点 通过凸透镜的基本性质 变成另一个点

        x = ValueTracker(-10/3)
        y = ValueTracker(1.2)
        def a_updater(mob: Dot):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.move_to(position)
        def label_a_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            if position[0] < 0 and position[0] > -2:
                direction = DOWN
            else:
                direction = UP
            mob.next_to(position, direction)
        def b_updater(mob: Dot):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.move_to(destination)
        def label_b_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            if position[0] < 0 and position[0] > -2:
                direction = UP
            else:
                direction = DOWN
            mob.next_to(destination, direction)
        def p_updater(mob: Dot):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.move_to(np.array([0, position[1], 0]))
        def label_p_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            if position[0] > 0:
                direction = UL
            else:
                direction = UR
            mob.next_to(np.array([0, position[1], 0]), direction, buff = 0.15)
        def q_updater(mob: Dot):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.move_to(np.array([0, destination[1], 0]))
        def label_q_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            if position[0] > 0:
                direction = UL
            elif position[0] > -2:
                direction = UR
            else:
                direction = DL
            mob.next_to(np.array([0, destination[1], 0]), direction, buff = 0.15)
        def line_u_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.put_start_and_end_on(position, np.array([0, position[1], 0]))
        def label_u_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.next_to(np.array([position[0]/2, position[1], 0]), UP)
        def line_v_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.put_start_and_end_on(destination, np.array([0, destination[1], 0]))
        def label_v_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.next_to(np.array([destination[0]/2, destination[1], 0]), UP)
        def line_aq_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.put_start_and_end_on(position, np.array([0, destination[1], 0]))
        def line_bp_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.put_start_and_end_on(np.array([0, position[1], 0]), destination)
        def line_ao_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.put_start_and_end_on(position, ORIGIN)
        def line_bo_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.put_start_and_end_on(ORIGIN, destination)
        def line_af_updater(mob: DashedLine):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.become(DashedLine(position, 2*LEFT, color = YELLOW, stroke_width = 1))
        def line_bf_updater(mob: DashedLine):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.become(DashedLine(destination, 2*RIGHT, color = YELLOW, stroke_width = 1))
        def label_f_r_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            if position[0] > 0:
                direction = DOWN
            else:
                direction = UP
            mob.next_to(RIGHT, direction, buff = 0.11)

        point_any.add_updater(a_updater)
        label_a.add_updater(label_a_updater)
        point_image.add_updater(b_updater)
        label_b.add_updater(label_b_updater)
        point_p.add_updater(p_updater)
        label_p.add_updater(label_p_updater)
        point_q.add_updater(q_updater)
        label_q.add_updater(label_q_updater)
        line_u.add_updater(line_u_updater)
        label_u.add_updater(label_u_updater)
        line_v.add_updater(line_v_updater)
        label_v.add_updater(label_v_updater)
        line_aq.add_updater(line_aq_updater)
        line_bp.add_updater(line_bp_updater)
        line_ao.add_updater(line_ao_updater)
        line_bo.add_updater(line_bo_updater)
        line_af.add_updater(line_af_updater)
        line_bf.add_updater(line_bf_updater)
        label_f_r.add_updater(label_f_r_updater)
        self.play(x.animate.set_value(-4), y.animate.set_value(2))
        self.waiting(1, 14) #无论这一点是在一倍焦距以外......
        self.play(x.animate.set_value(-1), y.animate.set_value(1), run_time = 2)
        line_7 = VMobject(color = YELLOW, stroke_width = 8).set_points_as_corners([LEFT+UP, UP, 2*LEFT+2*UP])
        line_8 = VMobject(color = YELLOW, stroke_width = 8).set_points_as_corners([LEFT+UP, ORIGIN, 2*LEFT+2*UP])
        line_9 = VMobject(color = YELLOW, stroke_width = 8).set_points_as_corners([LEFT+UP, 2*UP, 2*LEFT+2*UP])
        self.play(*[ShowPassingFlash(mob) for mob in [line_7, line_8, line_9]], rate_func = linear)
        self.play(*[ShowPassingFlash(mob) for mob in [line_7, line_8, line_9]], rate_func = linear)
        self.waiting(1+3-4, 28+9) #......还是一倍焦距以内 我们都能用同样的步骤来取出它的像
        self.play(x.animate.set_value(4), y.animate.set_value(2), run_time = 2)
        self.waiting(1, 2) #这个映射甚至可以定义在右半平面上

        self.waiting(3, 3) #只不过这时候并不对应着什么光学现象
        self.waiting(1, 0) #到此共73秒
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30) 

class Chapter1_3(Scene):
    def construct(self):
        notice5 = Notice("村规私设", "请勿模仿")
        notice6 = Notice("中考几何", "请　显然")
        notice7 = Notice("重要结论", "请记笔记")
        notice8 = Notice("下节预告", "请　好奇")

        ideal_len = Line(3*UP, 3*DOWN).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN)
        ideal_bench = NumberLine([-6, 6, 2], stroke_width = 8, color = BLUE)
        dot_center = Dot(color = YELLOW)

        def len_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[0]+focus)*point
        start = 4*RIGHT + 2*UP
        end = len_trans(start)

        point_any = Dot(color = YELLOW).shift(start)
        point_image = Dot(color = YELLOW).shift(end)
        point_f1 = Dot(color = YELLOW).shift(2*LEFT)
        point_f2 = Dot(color = YELLOW).shift(2*RIGHT)
        point_p = Dot(color = YELLOW).shift(2*UP)
        point_q = Dot(color = YELLOW).shift(2*UP/3)
        line_u = Line(start, 2*UP, stroke_width = 8, color = PURPLE)
        line_v = Line(end, 2*UP/3, stroke_width = 8, color = ORANGE)
        line_af = DashedLine(start, 2*LEFT, stroke_width = 1, color = YELLOW)
        line_bf = DashedLine(end, 2*RIGHT, stroke_width = 1, color = YELLOW)
        line_ao = Line(start, ORIGIN, stroke_width = 2, color = YELLOW)
        line_bo = Line(ORIGIN, end, stroke_width = 2, color = YELLOW)
        line_aq = Line(start, 2*UP/3, stroke_width = 2, color = YELLOW)
        line_bp = Line(2*UP, end, stroke_width = 2, color = YELLOW)
        label_a = MTex("A").scale(0.7).next_to(start, UP)
        label_b = MTex("B").scale(0.7).next_to(end, DOWN)
        label_f1 = MTex("F_{1}").scale(0.7).next_to(2*LEFT, DOWN)
        label_f2 = MTex("F_{2}").scale(0.7).next_to(2*RIGHT, DOWN)
        label_o = MTex("O").scale(0.7).next_to(ORIGIN, DL).shift(0.05*RIGHT)
        label_p = MTex("P").scale(0.7).next_to(2*UP, UL, buff = 0.15)
        label_q = MTex("Q").scale(0.7).next_to(2*UP/3, UL, buff = 0.15)
        label_u = MTex(r"u", color = PURPLE).scale(0.9).next_to(line_u, UP)
        label_v = MTex(r"v", color = ORANGE).scale(0.9).next_to(line_v, UP)
        label_f_l = MTex(r"f", color = BLUE).scale(0.6).next_to(LEFT, DOWN, buff = 0.11)
        label_f_r = MTex(r"f", color = BLUE).scale(0.6).next_to(RIGHT, DOWN, buff = 0.11)

        title = Text("凸透镜变换", font = "simsun", color = YELLOW).scale(1.25).next_to(3.05*UP, UP)
        line_title = Line(3.1*UP+6*LEFT, 3.1*UP+6*RIGHT)
        formula = MTex(r"\frac{1}{u}+\frac{1}{v}=\frac{1}{f}", tex_to_color_map = {r"\frac{1}{u}": PURPLE, r"\frac{1}{v}": ORANGE, r"\frac{1}{f}": BLUE}).scale(0.7).next_to(5*LEFT + 1.5*DOWN, RIGHT, buff = 0)
        surrounding = SurroundingRectangle(formula)
        
        self.add(notice5, title, line_title, formula, surrounding, ideal_len, ideal_bench, dot_center, line_af, line_bf, line_ao, line_bo, line_aq, line_bp, line_u, line_v, point_any, point_image, point_f1, point_f2, point_p, point_q, label_a, label_b, label_f1, label_f2, label_o, label_p, label_q, label_u, label_v, label_f_l, label_f_r)
        
        x = ValueTracker(4.0)
        y = ValueTracker(2.0)
        def a_updater(mob: Dot):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.move_to(position)
        def label_a_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            if position[0] < 0 and position[0] > -2:
                direction = DOWN
            else:
                direction = UP
            mob.next_to(position, direction)
        def b_updater(mob: Dot):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.move_to(destination)
        def label_b_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            if position[0] < 0 and position[0] > -2:
                direction = UP
            else:
                direction = DOWN
            mob.next_to(destination, direction)
        def p_updater(mob: Dot):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.move_to(np.array([0, position[1], 0]))
        def label_p_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            if position[0] > 0:
                direction = UL
            else:
                direction = UR
            mob.next_to(np.array([0, position[1], 0]), direction, buff = 0.15)
        def q_updater(mob: Dot):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.move_to(np.array([0, destination[1], 0]))
        def label_q_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            if position[0] > 0:
                direction = UL
            elif position[0] > -2:
                direction = UR
            else:
                direction = DL
            mob.next_to(np.array([0, destination[1], 0]), direction, buff = 0.15)
        def line_u_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.put_start_and_end_on(position, np.array([0, position[1], 0]))
        def label_u_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.next_to(np.array([position[0]/2, position[1], 0]), UP)
        def line_v_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.put_start_and_end_on(destination, np.array([0, destination[1], 0]))
        def line_bq_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.put_start_and_end_on(np.array([0, destination[1], 0]), destination)
        def label_v_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.next_to(np.array([destination[0]/2, destination[1], 0]), UP)
        def line_aq_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.put_start_and_end_on(position, np.array([0, destination[1], 0]))
        def line_bp_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.put_start_and_end_on(np.array([0, position[1], 0]), destination)
        def line_ao_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.put_start_and_end_on(position, ORIGIN)
        def line_bo_updater(mob: Line):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.put_start_and_end_on(ORIGIN, destination)
        def line_af_updater(mob: DashedLine):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.become(DashedLine(position, 2*LEFT, color = YELLOW, stroke_width = 1))
        def line_bf_updater(mob: DashedLine):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.become(DashedLine(destination, 2*RIGHT, color = YELLOW, stroke_width = 1))
        def label_f_r_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            if position[0] > 0:
                direction = DOWN
            else:
                direction = UP
            mob.next_to(RIGHT, direction, buff = 0.11)

        point_any.add_updater(a_updater)
        label_a.add_updater(label_a_updater)
        point_image.add_updater(b_updater)
        label_b.add_updater(label_b_updater)
        point_p.add_updater(p_updater)
        label_p.add_updater(label_p_updater)
        point_q.add_updater(q_updater)
        label_q.add_updater(label_q_updater)
        line_u.add_updater(line_u_updater)
        label_u.add_updater(label_u_updater)
        line_v.add_updater(line_v_updater)
        label_v.add_updater(label_v_updater)
        line_aq.add_updater(line_aq_updater)
        line_bp.add_updater(line_bp_updater)
        line_ao.add_updater(line_ao_updater)
        line_bo.add_updater(line_bo_updater)
        line_af.add_updater(line_af_updater)
        line_bf.add_updater(line_bf_updater)
        label_f_r.add_updater(label_f_r_updater)
        
        start = 10/3*LEFT + 1.2*UP
        end = len_trans(start)
        line_1 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, 1.2*UP, end])
        line_2 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, ORIGIN, end])
        line_3 = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, 1.8*DOWN, end])

        self.play(x.animate.set_value(-10/3), y.animate.set_value(1.2), run_time = 2)
        self.waiting(0, 16) #特殊的三条光线确实共点
        with_updater = [point_any, label_a, point_image, label_b, point_p, label_p, point_q, label_q, line_u, label_u, line_v, label_v, line_aq, line_bp, line_ao, line_bo, line_af, line_bf, label_f_r]
        for mob in with_updater:
            mob.clear_updaters()
        labels = [label_a, label_b, label_f1, label_f2, label_o, label_p, label_q, label_u, label_v, label_f_l, label_f_r]
        self.remove(line_af, line_bf, line_ao, line_bo, line_aq, line_bp).bring_to_back(ideal_len, ideal_bench, line_1, line_2, line_3).play(LaggedStart(*[Uncreate(mob) for mob in [point_p, point_q, *labels]], group = VGroup(), run_time = 2), *[Uncreate(mob) for mob in [line_u, line_v, surrounding]], FadeOut(formula))
        self.waiting(0, 2) #这算是开了个好头

        lines = []
        for i in range(9):
            height = (i-4)*0.6*UP
            line_i = VMobject(color = YELLOW, stroke_width = 2).set_points_as_corners([start, height, end])
            lines.append(line_i)

        points = [point_any, point_image, point_f1, point_f2, dot_center]
        self.add(*lines, *points).play(*[ShowCreation(mob) for mob in lines], run_time = 2)
        self.remove(line_1, line_2, line_3)
        self.waiting(1, 8) #但要验证每一条折射光线都经过点B
        self.waiting(1, 12) #还是比较麻烦的
        self.waiting(0, 23) #（空闲）

        self.play(*[mob.animate.fade(0.8) for mob in lines])
        self.waiting(2, 1) #三条基本性质的哪一条都没有说过

        line_any = VMobject(color = YELLOW).set_points_as_corners([np.array([-20/3, 3, 0]), np.array([-10/3, 1.2, 0]), 0.6*DOWN, np.array([2.5, -1.2, 0])])
        self.play(ShowCreation(line_any))
        line_left = Line(np.array([-20/3, 3, 0]), 0.6*DOWN, color = YELLOW)
        line_right = Line(0.6*DOWN, np.array([2.5, -1.2, 0]), color = YELLOW)
        self.remove(line_any).add(line_left, line_right)
        vector = np.array([2.5, -1.2, 0]) - 0.6*DOWN
        norm = get_norm(vector)
        angle = np.arctan2(vector[1], vector[0])

        alpha = ValueTracker(angle)
        def line_right_updater(mob: Line):
            value = alpha.get_value()
            mob.put_start_and_end_on(0.6*DOWN, 0.6*DOWN + norm*unit(value))
        line_right.add_updater(line_right_updater)
        q_mark = MTexText("?").shift(0.6*DOWN + 1.1*norm*unit(angle))
        beta = ValueTracker(0.0)
        def q_mark_updater(mob: MTexText):
            mob.move_to(0.6*DOWN + 1.1*norm*unit(alpha.get_value())).set_opacity(beta.get_value())
        q_mark.add_updater(q_mark_updater)

        self.add(q_mark).play(alpha.animate.set_value(angle*2), beta.animate.set_value(1.0))
        self.play(alpha.animate.set_value(-angle/2))
        line_right.clear_updaters()
        q_mark.clear_updaters()
        self.waiting(0, 4) #一般位置的光线应该满足什么样的折射规律
        self.waiting(0, 21) #（空闲）
        
        self.play(Uncreate(line_right), Uncreate(q_mark), *[FadeOut(mob) for mob in lines])
        self.waiting(1, 26) #这个时候就需要用到一点技巧了

        line_ap = Line(start, 1.2*UP, stroke_width = 2, color = YELLOW)
        line_bq = Line(1.8*DOWN, end, stroke_width = 2, color = YELLOW)
        for mob in [line_ap, line_ao, line_aq, line_bp, line_bo, line_bq]:
            mob.set_color(YELLOW_E)
        
        self.add(line_ap, line_ao, line_aq, *points).play(*[ShowCreation(mob) for mob in [line_ap, line_ao, line_aq]], rate_func = rush_into)
        self.add(line_bp, line_bo, line_bq, *points).play(*[ShowCreation(mob) for mob in [line_bp, line_bo, line_bq]], rate_func = rush_from)
        self.waiting(0, 3) #既然这条光路上的每一点

        point_any.add_updater(a_updater)
        point_image.add_updater(b_updater)
        line_ap.add_updater(line_u_updater)
        line_bq.add_updater(line_bq_updater)
        line_aq.add_updater(line_aq_updater)
        line_bp.add_updater(line_bp_updater)
        line_ao.add_updater(line_ao_updater)
        line_bo.add_updater(line_bo_updater)
        
        def l(x: float):
            return -0.6-0.54*x
        self.play(x.animate.set_value(-4), y.animate.set_value(l(-4)))
        self.play(x.animate.set_value(-8/3), y.animate.set_value(l(-8/3)), run_time = 1+5/6) #都可以用基本性质取出对应的像
        trace = TracedPath(point_image.get_center, stroke_color = ORANGE, stroke_width = 2)
        line_right = Line(8*RIGHT+2.52*DOWN, 0.6*DOWN, color = ORANGE)
        self.bring_to_back(trace).play(x.animate.set_value(-14/3), y.animate.set_value(l(-14/3)), run_time = 2+7/10) #我们就可以把所有像形成的轨迹
        trace.clear_updaters()
        self.play(Transform(trace, line_right))
        self.remove(trace).bring_to_back(ideal_len, ideal_bench, line_right).waiting(1, 21) #反过来定义成这条光线的折射
        self.waiting(0, 15) #（空闲）

        copy_right = line_right.copy().reverse_points().set_color(YELLOW)
        self.play(ShowPassingFlash(copy_right))
        self.play(ShowPassingFlash(copy_right))
        self.play(ShowPassingFlash(copy_right))
        self.waiting(0, 9) #那么 这条轨迹是不是一条直线呢
        self.waiting(0, 22) #（空闲）

        label_a = MTex("A").scale(0.7).next_to(start, UR, buff = 0.15)
        label_b = MTex("B").scale(0.7).next_to(end, DR, buff = 0.15)
        label_f1 = MTex("F_{1}").scale(0.7).next_to(2*LEFT, DOWN)
        label_f2 = MTex("F_{2}").scale(0.7).next_to(2*RIGHT, UP)
        label_o = MTex("O").scale(0.7).next_to(ORIGIN, UR, buff = 0.15)

        for mob in [point_any, point_image, line_ap, line_bq, line_aq, line_bp, line_ao, line_bo]:
            mob.clear_updaters()
        
        line_bp.reverse_points()
        line_bo.reverse_points()
        line_bq.reverse_points()
        
        self.play(*[ShowCreation(mob) for mob in [label_f1, label_f2, label_o]], *[Uncreate(mob) for mob in [point_any, point_image, line_ap, line_ao, line_aq, line_bp, line_bo, line_bq]])
        self.waiting(2, 7) #这同样是一道简单的平面几何习题

        direction = 0.6*DOWN - start
        angle = np.arctan2(direction[1], direction[0])
        direction_1 = 3*DOWN - start
        angle_1 = np.arctan2(direction_1[1], direction_1[0])
        direction_2 = DOWN + 8/3*LEFT - start
        angle_2 = np.arctan2(direction_2[1], direction_2[0])

        alpha = ValueTracker(angle)
        def line_left_updater(mob: Line):
            value = alpha.get_value()
            k = np.tan(value)
            upper = (1.8/k - 10/3)*RIGHT +3*UP
            if value >= angle_1:
                lower = (10/3*k+1.2)*UP
            else:
                lower = (-4.2/k - 10/3)*RIGHT +3*DOWN
            mob.put_start_and_end_on(upper, lower)
        line_left.add_updater(line_left_updater)
        def line_right_updater(mob: Line):
            value = alpha.get_value()
            k = np.tan(value)
            if value >= angle_1:
                upper = 8*RIGHT + (2*k+18/5) * DOWN
                lower = (10/3*k+1.2)*UP
            elif value >= angle_2:
                upper = 8*RIGHT + (2*k+18/5) * DOWN
                lower = 3*DOWN + (5+18/(10*k+9))*RIGHT
            else:
                upper = 3*UP + (5-72/(10*k+9))*RIGHT
                lower = 3*DOWN + (5+18/(10*k+9))*RIGHT
            mob.put_start_and_end_on(upper, lower)
        line_right.add_updater(line_right_updater)
        self.add(notice5).play(alpha.animate.set_value(-PI/2))
        self.waiting(1, 20) #如果这条光线垂直于主光轴

        self.waiting(3, 1) #虽然它实际上并不会被凸透镜折射
        shade_up = Rectangle(width = 16, height = 0.95, fill_color = BACK, stroke_width = 0, fill_opacity = 1).next_to(4*UP, DOWN, buff = 0)
        shade_down = Rectangle(width = 16, height = 0.95, fill_color = BACK, stroke_width = 0, fill_opacity = 1).next_to(4*DOWN, UP, buff = 0)
        line_u = Line(start, 1.2*UP, stroke_width = 8, color = PURPLE)
        line_v = Line(end, 1.8*DOWN, stroke_width = 8, color = ORANGE)
        label_u = MTex(r"u", color = PURPLE).scale(0.9).next_to(line_u, UP)
        label_v = MTex(r"v", color = ORANGE).scale(0.9).next_to(line_v, UP)
        formula.shift(LEFT)
        self.add(line_u, line_v, label_u, label_v, point_f1, point_f2, dot_center, label_f1, label_f2, label_o, shade_up, shade_down, title, line_title).play(*[ShowCreation(mob) for mob in [line_u, line_v, label_u, label_v]], Write(formula))
        self.play(line_u.animate.shift(5*DOWN), label_u.animate.shift(5*DOWN), line_v.animate.shift(7.5*UP), label_v.animate.shift(7.5*UP), run_time = 1.5, rate_func = rush_into)
        self.waiting(0, 7) #但根据之前得到的成像公式

        self.remove(line_u, line_v, label_u, label_v).play(Uncreate(formula))
        self.waiting(1, 2) #对应的轨迹确实是直线
        self.waiting(0, 18) #（空闲）

        self.play(alpha.animate.set_value(angle))
        line_left.clear_updaters()
        line_right.clear_updaters()
        self.waiting(1, 21) #如果这条光线不垂直于主光轴
        point_q = Dot(color = YELLOW).shift(1.8*DOWN)
        label_q = MTex("Q").scale(0.7).next_to(1.8*DOWN, DL, buff = 0.15)
        point_c = Dot(color = YELLOW).shift(0.6*DOWN)
        label_c = MTex("C").scale(0.7).next_to(0.6*DOWN, DL, buff = 0.15)
        point_d = Dot(color = YELLOW).shift(2*LEFT + 0.48*UP)
        label_d = MTex("D").scale(0.7).next_to(2*LEFT + 0.48*UP, UR, buff = 0.2)
        line_fd = DashedLine(2*LEFT, 2*LEFT + 0.48*UP, stroke_width = 2, stroke_color = YELLOW)
        self.play(ReplacementTransform(notice5, notice6))
        self.waiting(2, 15) #我们可以在上面取两个辅助点来帮助证明
        self.play(ShowCreation(line_fd), rate_func = rush_into)
        self.play(ShowCreation(point_d), DrawBorderThenFill(label_d), rate_func = rush_from, run_time = 1)
        self.waiting(0, 10) #它们分别是一倍焦距处的点
        self.play(ShowCreation(point_c), DrawBorderThenFill(label_c), run_time = 1)
        self.waiting(0, 24) #和在凸透镜上的点
        self.waiting(0, 19) #（空闲）

        point_any.add_updater(a_updater)
        point_image.add_updater(b_updater)
        point_q.add_updater(q_updater)
        label_q.add_updater(label_q_updater)
        line_ap.add_updater(line_u_updater)
        line_bq.add_updater(line_bq_updater)
        line_aq.add_updater(line_aq_updater)
        line_bp.add_updater(line_bp_updater)
        line_ao.add_updater(line_ao_updater)
        line_bo.add_updater(line_bo_updater)
        x.set_value(-10/3), y.set_value(1.2)
        
        self.play(ShowCreation(point_any), DrawBorderThenFill(label_a), run_time = 1)
        self.waiting(1, 3) #对于这条直线上的一点A
        for mob in [line_bp, line_bo, line_bq]:
            mob.reverse_points()
        self.add(line_ap, line_ao, line_aq, point_any, point_f1, dot_center).play(*[ShowCreation(mob) for mob in [line_ap, line_aq, line_ao]], rate_func = rush_into, run_time = 0.5)
        tail = squish_rate_func(rush_from, 0, 1/3)
        former = squish_rate_func(smooth, 0, 2/3)
        latter = squish_rate_func(smooth, 1/3, 1)
        self.add(line_bp, line_bo, line_bq, point_q, label_q, point_image, label_b, point_f2, dot_center).play(*[ShowCreation(mob, rate_func = tail) for mob in [line_bp, line_bo, line_bq]], ShowCreation(point_q, rate_func = former) , DrawBorderThenFill(label_q, rate_func = former), ShowCreation(point_image, rate_func = latter), DrawBorderThenFill(label_b, rate_func = former), run_time = 1.5)
        self.waiting(1+0-2, 25+18) #我们做出它的像B （空闲）

        indicate_1 = Line(2*LEFT, ORIGIN, stroke_color = YELLOW, stroke_width = 8)
        indicate_2 = Line(1.8*DOWN, 1.8*DOWN+5*RIGHT, stroke_color = YELLOW, stroke_width = 8)
        self.play(ShowPassingFlash(indicate_1), ShowPassingFlash(indicate_2))
        indicate_3 = Line(2*LEFT, 2*LEFT + 0.48*UP, stroke_color = YELLOW, stroke_width = 8)
        indicate_4 = Line(1.8*DOWN, 0.6*DOWN, stroke_color = YELLOW, stroke_width = 8)
        self.play(ShowPassingFlash(indicate_3), ShowPassingFlash(indicate_4))
        self.waiting(0, 7) #根据平行和垂直
        triangle_1 = Polygon(2*LEFT, 2*LEFT + 0.48*UP, ORIGIN, stroke_width = 0, fill_opacity = 0.2, fill_color = ORANGE)
        triangle_2 = Polygon(1.8*DOWN, 0.6*DOWN, 1.8*DOWN+5*RIGHT, stroke_width = 0, fill_opacity = 0.2, fill_color = RED)
        self.bring_to_back(triangle_1, triangle_2).play(ShowCreation(triangle_1), ShowCreation(triangle_2))
        self.waiting(1, 12) #我们能得到两组平行线段

        text_1 = MTex(r"\frac{AD}{AC}=\frac{AF_1}{AQ}=\frac{AO}{AB}").scale(0.7).next_to(6*LEFT+1.5*DOWN)
        self.play(Write(text_1))
        self.waiting(0, 15) #它们提供了比例关系的转换
        line_do = Line(ORIGIN, 2*LEFT + 0.48*UP, stroke_color = ORANGE)
        text_2 = MTex(r"\Rightarrow OD\parallel CB").scale(0.7).next_to(6*LEFT+2.5*DOWN)
        self.add(line_do, line_left, point_any, point_c, point_d, dot_center).play(ShowCreation(line_do), Write(text_2))
        self.waiting(1, 15) #于是OD和CB也是平行的
        self.waiting(0, 24) #（空闲）

        def label_a_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            mob.next_to(position, UR, buff = 0.15)
        def label_b_updater(mob: MTex):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.next_to(destination, DR, buff = 0.15)
        def triangle_updater(mob: Polygon):
            position = np.array([x.get_value(), y.get_value(), 0])
            destination = len_trans(position)
            mob.set_points_as_corners([np.array([0, destination[1], 0]), 0.6*DOWN, destination])
        label_a.add_updater(label_a_updater)
        label_b.add_updater(label_b_updater)
        triangle_2.add_updater(triangle_updater)

        self.play(x.animate.set_value(-4), y.animate.set_value(l(-4)), run_time = 1.5)
        self.play(x.animate.set_value(-8/3), y.animate.set_value(l(-8/3)), run_time = 2)
        self.play(x.animate.set_value(-14/3), y.animate.set_value(l(-14/3)), run_time = 2)
        self.play(x.animate.set_value(-10/3), y.animate.set_value(l(-10/3)), run_time = 1.5)
        self.waiting(2+2+2-7, 24+14+7) #那么 当A运动的时候 CB始终和OD平行 B的轨迹就是一条直线 
        self.waiting(0, 22) #（空闲）

        with_updaters = [point_any, label_a, point_image, label_b, point_q, label_q, triangle_2, line_ap, line_bq, line_aq, line_bp, line_ao, line_bo]
        for mob in with_updaters:
            mob.clear_updaters()
        for mob in [line_bp, line_bo, line_bq, line_do, line_fd]:
            mob.reverse_points()
        self.play(FadeOut(text_1), FadeOut(text_2), ReplacementTransform(notice6, notice7), *[Uncreate(mob) for mob in [*with_updaters, triangle_1, point_d, label_d, point_c, label_c, line_do, line_fd, label_f1, label_f2, point_f1, point_f2, label_o, dot_center]])
        self.waiting(2, 20) #这样 我们获得了一个很漂亮的结论

        copy_left = line_left.copy().set_stroke(width = 8, color = WHITE)
        copy_right.set_stroke(width = 8, color = WHITE)
        self.play(ShowPassingFlash(copy_left), run_time = 0.5, rate_func = rush_into)
        self.play(ShowPassingFlash(copy_right), run_time = 0.5, rate_func = rush_from)
        self.play(ShowPassingFlash(copy_left), run_time = 0.5, rate_func = rush_into)
        self.play(ShowPassingFlash(copy_right), run_time = 0.5, rate_func = rush_from)
        self.play(ShowPassingFlash(copy_left), run_time = 0.5, rate_func = rush_into)
        self.play(ShowPassingFlash(copy_right), run_time = 0.5, rate_func = rush_from)
        self.waiting(0, 5) #凸透镜变换会将直线映射到直线
        self.waiting(0, 16) #（空闲）

        self.remove(shade_down, shade_up)

        def tan_color(x: float):
            a = np.arctan(x/4)/(PI/2)+1
            if a > 1:
                return interpolate_color(RED_E, YELLOW_E, a-1)
            else:
                return interpolate_color(YELLOW_E, GREEN_E, a)

        grids = 8
        grid_group = 5
        major_lines = VGroup()
        minor_lines = VGroup()
        lines_h = VGroup()
        alpha = ValueTracker(0.0)
        def horizontal_updater(height: float):
            def util(mob: Line):
                value = alpha.get_value()
                left_end = np.array([-8, height*(1+value*8), 0])
                right_end = np.array([8, height*(1-value*8), 0])
                mob.put_start_and_end_on(left_end, right_end)
            return util
        for i in range(grids*grid_group + 1):
            height = -(i/grid_group-grids/2)
            line_i = Line(8*LEFT, 8*RIGHT, color = YELLOW_E, stroke_width = 4).shift(height*UP)
            if i % 5 != 0:
                line_i.set_stroke(width = 1)
                minor_lines.add(line_i.copy())
            else:
                major_lines.add(line_i.copy())
            line_i.add_updater(horizontal_updater(height))
            lines_h.add(line_i)
        grids = 100
        grid_group = 5
        lines_v = VGroup()
        center_v = VGroup()
        for i in range(grids*grid_group + 1):
            position = i/grid_group-50
            line_i = Line(4*UP, 4*DOWN, stroke_width = 4).shift(position*RIGHT)
            if i % 5 != 0:
                line_i.set_stroke(width = 2)
                minor_lines.add(line_i.copy())
            else:
                major_lines.add(line_i.copy())
            line_i.set_color(tan_color(position))
            lines_v.add(line_i)
            if abs(position) < 8:
                center_v.add(line_i)
        grid = VGroup(minor_lines, major_lines).set_color(GREY).set_opacity(0.5)
        self.bring_to_back(center_v, lines_h).play(ideal_len.animate.set_color(WHITE), *[FadeOut(mob) for mob in [title, line_title, line_left, line_right]], Write(lines_h), Write(center_v), run_time = 2)
        self.waiting(0, 18) #如果我们给平面打上网格
        self.remove(center_v).bring_to_back(grid, lines_h, lines_v).play(FocusInterpolate(lines_v), alpha.animate.set_value(1/2), run_time = 3)
        for mob in lines_h:
            mob.clear_updaters()
        self.waiting(0, 9) #就可以比较直观地看到每个点都跑到哪里去了
        self.waiting(2, 4) #（空闲）

        coordinate_1 = np.array([-5, 2, 0])
        coordinate_2 = np.array([-3, -1, 0])
        line_any = Line(coordinate_1, coordinate_2, stroke_width = 8, stroke_color = PURPLE)
        line_image = Line(len_trans(coordinate_1), len_trans(coordinate_2), stroke_width = 8, stroke_color = ORANGE)
        self.play(ShowCreation(line_any))
        self.waiting(0, 26) #左边的任何一条直线
        self.play(ShowCreation(line_image))
        self.waiting(1, 6) #都会变成右边的一条直线
        self.waiting(0, 27) #（空闲）

        self.waiting(3, 27) #这看起来和视频开始的那道题还有一定距离

        point = Dot(fill_opacity = 0).shift(3.2*LEFT)
        trace_left = TracedPath(point.get_center, stroke_color = PURPLE, stroke_width = 8)
        trace_right = TracedPath(lambda: len_trans(point.get_center()), stroke_color = ORANGE, stroke_width = 8)

        self.add(trace_left, trace_right).play(ReplacementTransform(notice7, notice8), Uncreate(line_any), Uncreate(line_image), Rotate(point, TAU, about_point = 4*LEFT, ))
        trace_left.clear_updaters()
        trace_right.clear_updaters()
        self.waiting(1, 25) #毕竟那道题要求我们找到圆的像
        self.waiting(0, 23) #（空闲）

        self.waiting(3, 0) #但大概有一部分观众已经意识到
        self.waiting(2, 12) #在证明了保直线性的那一刻
        self.play(FadeOut(lines_h), lines_v.animate.set_opacity(0.0), FadeOut(grid), ideal_len.animate.set_color(GREEN))
        self.remove(lines_v).waiting(1, 2) #整道题就已经做完了
        self.waiting(0, 22) #（空闲）

        self.waiting(3, 14) #而我们 也只需要一点更多的知识
        self.waiting(2, 0) #就能跟上他们的脚步

        self.waiting(3, 10)
        self.play(*[FadeOut(mob) for mob in [trace_left, trace_right, ideal_bench, ideal_len, notice8]])
        self.waiting(3, 0) #到此共132秒
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30) 

#########################################################################

class Chapter2_0(Scene):

    def construct(self):

        text2 = Text("第二节 透视", font = 'simsun', t2c={"第二节": YELLOW, "透视": GREEN}).scale(1.25)

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(Scene):
    def construct(self):
        notice1 = Notice("简单情况", "请　重视")
        notice2 = Notice("奇妙结论", "请　惊叹")

        ideal_len = Line(3*UP, 3*DOWN).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN)
        ideal_bench = NumberLine([-6, 6, 2], stroke_width = 8, color = BLUE)
        dot_center = Dot(color = YELLOW)

        point_any = Dot(color = YELLOW).shift(10/3*LEFT)
        point_image = Dot(color = YELLOW).shift(5*RIGHT)
        line_u = Line(10/3*LEFT, ORIGIN, stroke_color = PURPLE, stroke_width = 8)
        line_v = Line(5*RIGHT, ORIGIN, stroke_color = ORANGE, stroke_width = 8)
        label_u = MTex("u", color = PURPLE).next_to(5/3*LEFT, UP)
        label_v = MTex("v", color = ORANGE).next_to(5/2*RIGHT, UP)

        def tan_color(x: float):
            a = np.arctan(x/4)/(PI/2)+1
            if a > 1:
                return interpolate_color(RED_E, YELLOW_E, a-1)
            else:
                return interpolate_color(YELLOW_E, GREEN_E, a)

        grids = 8
        grid_group = 5
        grey_lines = VGroup()
        lines = VGroup()
        for i in range(grids*grid_group + 1):
            height = -(i/grid_group-grids/2)
            line_i = Line(8*LEFT, 8*RIGHT, color = YELLOW_E, stroke_width = 4).shift(height*UP)
            if i % 5 != 0:
                line_i.set_stroke(width = 1)
            grey_lines.add(line_i.copy())
            line_i.put_start_and_end_on(np.array([-8, height*5, 0]), np.array([8, -height*3, 0]))
            lines.add(line_i)
        grids = 100
        grid_group = 5
        def len_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[0]+focus)*point
        for i in range(grids*grid_group + 1):
            position = i/grid_group-50
            up = 4*UP + position*RIGHT
            down = 4*DOWN + position*RIGHT
            line_i = Line(up, down, stroke_width = 4)
            if i % 5 != 0:
                line_i.set_stroke(width = 2)
            grey_lines.add(line_i.copy())
            if position != -2:
                line_i.set_color(tan_color(position)).put_start_and_end_on(len_trans(up), len_trans(down))
                lines.add(line_i)
        grey_lines.set_color(GREY).set_opacity(0.5).fade()
        lines.fade()
        
        self.play(Write(notice1), *[ShowCreation(mob) for mob in [ideal_len, ideal_bench, dot_center]])
        self.waiting(3, 0) #我们暂时只关注主光轴上的点在凸透镜变换下的像
        self.add(line_u, line_v, point_any, point_image, dot_center).play(*[ShowCreation(mob) for mob in [point_any, point_image, line_u, line_v]], *[Write(mob) for mob in [label_u, label_v]])
        self.waiting(1, 26) #设物距和像距分别是u和v
        self.bring_to_back(grey_lines, lines).play(FadeIn(grey_lines), FadeIn(lines), rate_func = there_and_back, run_time = 2)
        self.remove(grey_lines, lines).waiting(1+2-2, 20+24) #在没有网格了以后 这个变换看起来不是很容易理解
        
        self.waiting(2, 2) #但既然主光轴是一维的

        axis_u = Arrow(3*LEFT+2*DOWN, 3*RIGHT+2*DOWN, buff = 0)
        axis_v = Arrow(3*DOWN+2*LEFT, 3*UP+2*LEFT, buff = 0)
        tip_u = MTex("u", color = PURPLE).next_to(axis_u, RIGHT)
        tip_v = MTex("v", color = ORANGE).next_to(axis_v, UP)
        graph_left = FunctionGraph(lambda t: t/(t-1), [-1, 0.5, 0.01]).shift(2*DL)
        graph_right = FunctionGraph(lambda t: t/(t-1), [5/4, 5, 0.01]).shift(2*DL)
        graph = VGroup(graph_left, graph_right)

        self.remove(ideal_len, ideal_bench, dot_center, line_u, line_v, point_any, point_image, label_u, label_v).play(ShowCreation(axis_u), ShowCreation(axis_v))
        self.play(Write(tip_u), Write(tip_v), ShowCreation(graph))
        self.waiting(0, 26) #我们就可以画出v关于u的函数图像了
        self.waiting(0, 15) #（空闲）

        text_1 = r"\frac{1}{u}+\frac{1}{v}=\frac{1}{f}"
        text_2 = r"v=\frac{uf}{u-f}"
        text_3 = r"v=\frac{f^2}{u-f}+f"
        formula = MTex(r"&" + text_1 + r"\\\Rightarrow\ &" + text_2 + r"\\\Rightarrow\ &" + text_3, 
            isolate = [text_1, text_2, text_3, r"\Rightarrow"], 
            tex_to_color_map = {(r"u", r"\frac{1}{u}"): PURPLE, (r"v", r"\frac{1}{v}"): ORANGE, (r"f", r"f^2", r"\frac{1}{f}"): BLUE}
            ).scale(0.7).shift(5*LEFT)
        formula_1 = formula.get_part_by_tex(text_1)
        formula_2 = formula.get_parts_by_tex(r"\Rightarrow")[0].add(formula.get_part_by_tex(text_2))
        formula_3 = formula.get_parts_by_tex(r"\Rightarrow")[1].add(formula.get_part_by_tex(text_3))
        self.play(Write(formula_1))
        self.waiting(1, 23) #之前我们推过凸透镜的成像公式
        self.play(Write(formula_2))
        self.waiting(0, 19) #将它稍微变形一下
        self.waiting(2, 6) #就变成了v的表达式

        shade = Square(side_length = 8.5, fill_color = BACK, stroke_width = 0, fill_opacity = 1).append_points(Square(side_length = 6).reverse_points().get_all_points())
        shift_graph_left = FunctionGraph(lambda t: t/(t-1), [-1, 0.5, 0.01], color = YELLOW_E).shift(3*DL)
        shift_graph_right = FunctionGraph(lambda t: t/(t-1), [6/5, 6, 0.01], color = YELLOW_E).shift(3*DL)
        dash_h = DashedLine(3*LEFT+2*DOWN, 3*RIGHT+2*DOWN, stroke_width = 2)
        dash_v = DashedLine(3*DOWN+2*LEFT, 3*UP+2*LEFT, stroke_width = 2)
        label_f_h = MTex("f", color = BLUE).scale(0.6).next_to(LEFT+2*DOWN, DR, buff = 0.15)
        label_f_v = MTex("f", color = BLUE).scale(0.6).next_to(2*LEFT+DOWN, DL, buff = 0.15)
        self.add(shift_graph_left, shift_graph_right, shade, axis_u, axis_v, tip_u, tip_v, graph_left, graph_right).play(ShowCreation(shift_graph_right))
        self.waiting(0, 10) #这是一个反比例函数......
        self.add(dash_h, dash_v).play(Write(formula_3), *[mob.animate.shift(UR) for mob in [shift_graph_left, shift_graph_right]], dash_h.animate.shift(UP), dash_v.animate.shift(RIGHT))
        self.remove(shade, shift_graph_left, shift_graph_right)
        self.play(Write(label_f_h), Write(label_f_v))
        self.waiting(1, 0) #......向上和向右分别平移了一倍焦距以后
        self.waiting(1, 6) #得到的图像
        self.waiting(0, 22) #（空闲）

        point = Dot(radius = 0.05, color = RED)
        perp_h = Line(ORIGIN, 2*LEFT, stroke_width = 2, color = RED)
        perp_v = Line(ORIGIN, 2*DOWN, stroke_width = 2, color = RED)
        self.play(*[ShowCreation(mob) for mob in [perp_h, perp_v, point]])
        self.waiting(1, 2) #这看起来挺没意思的

        alpha = ValueTracker(PI/4)
        func_v = lambda u: -u/(u+1)
        def point_updater(mob: Dot):
            angle = alpha.get_value()
            u = np.tan(angle)-1
            v = func_v(u)
            mob.move_to(np.array([u, v, 0]))
        def perp_h_updater(mob: Line):
            angle = alpha.get_value()
            u = np.tan(angle)-1
            v = func_v(u)
            mob.put_start_and_end_on(np.array([u, v, 0]), np.array([-2, v, 0]))
        def perp_v_updater(mob: Line):
            angle = alpha.get_value()
            u = np.tan(angle)-1
            v = func_v(u)
            mob.put_start_and_end_on(np.array([u, v, 0]), np.array([u, -2, 0]))
        point.add_updater(point_updater)
        perp_h.add_updater(perp_h_updater)
        perp_v.add_updater(perp_v_updater)

        self.play(ShowPassingFlashAround(formula_1), ApplyMethod(alpha.set_value, PI/3, run_time = 1.5, rate_func = rush_into))
        self.play(alpha.animate.set_value(5*PI/12), run_time = 1.5, rate_func = rush_from)
        self.play(alpha.animate.set_value(PI/12), run_time = 4)

        line_fixed = DashedLine(2*LEFT, 2*DOWN, stroke_width = 2, color = RED)
        point_fixed = Dot(radius = 0.05, color = YELLOW).shift(DL)
        beta = ValueTracker(0.0)
        def line_fixed_updater(mob: Line):
            angle = alpha.get_value()
            u = np.tan(angle)-1
            v = func_v(u)
            mob.become(DashedLine(np.array([-2, v, 0]), np.array([u, -2, 0]), stroke_width = 2, color = RED)).set_opacity(beta.get_value())
        line_fixed.add_updater(line_fixed_updater)
        text_right = MTex(r"y=&kx+b \\=& -\frac{v}{u}x+v\\=&-\frac{f}{u-f}x+\frac{uf}{u-f}\\{{f}}=&-\frac{f}{u-f}{{f}}+\frac{uf}{u-f}", tex_to_color_map = {r"{{f}}": BLUE}).scale(0.7).shift(4*RIGHT+UP)
        shade = Rectangle(height = 8, width = 16, fill_opacity = 1, stroke_width = 0, fill_color = BACK)
        self.add(line_fixed).play(alpha.animate.set_value(5*PI/12), ApplyMethod(beta.set_value, 1, rate_func = squish_rate_func(smooth, 5/10, 7/10)), run_time = 5)
        self.play(alpha.animate.set_value(PI/12), run_time = 5)
        self.play(alpha.animate.set_value(5*PI/12), ShowCreation(point_fixed, rate_func = squish_rate_func(smooth, 0, 1/5)), run_time = 5)
        self.play(alpha.animate.set_value(PI/12), 
        Write(text_right, rate_func = squish_rate_func(smooth, 0.8/5, 2.8/5)), 
        FadeIn(shade, rate_func = squish_rate_func(smooth, 3/5, 4/5)), 
        *[FadeIn(mob, rate_func = squish_rate_func(smooth, 4/5, 1)) for mob in [ideal_len, ideal_bench, dot_center, point_any, point_image]], 
        run_time = 5)
        for mob in [point, perp_h, perp_v, line_fixed]:
            mob.clear_updaters()
        self.remove(shade, axis_u, axis_v, tip_u, tip_v, graph, dash_h, dash_v, label_f_h, label_f_v, formula_1, formula_2, formula_3, text_right, point_fixed, point, perp_h, perp_v, line_fixed).waiting(2+3+2+0+2+1+2+3+0+2+2+2-27, 26+11+20+18+26+29+11+5+23+5+4+6) #有关u和v的表达式我们早就知道了 图像看起来就得是个反比例函数之类的样子 真画出来也似乎不会有什么别的收获 （空闲） 但是如果我们连接每个对应的u和v 就会发现一件事情 无论u和v取什么值 它们的连线总过一个定点 (f，f) （空闲） 
        
        BLUE_G = interpolate_color(BLUE, BACK, 0.5)
        YELLOW_G = interpolate_color(YELLOW, BACK, 0.5)
        ideal_piece = NumberLine([0, 6, 2], stroke_width = 8, color = BLUE)
        h_left = ideal_piece.copy().shift(3*LEFT).set_color(BLUE_G)
        h_right = ideal_piece.copy().shift(3*RIGHT)
        v_left = ideal_piece.copy().shift(3*LEFT)
        v_right = ideal_piece.copy().shift(3*RIGHT).set_color(BLUE_G)
        h_any = point_any.copy().set_color(YELLOW_G)
        h_image = point_image
        v_any = point_any
        v_image = point_image.copy().set_color(YELLOW_G)
        self.add(h_left, v_right, h_right, v_left, ideal_len, dot_center, h_any, v_image, h_image, v_any).remove(ideal_bench)
        self.play(*[Rotate(mob, -PI/2, about_point = ORIGIN) for mob in [v_right, v_left, v_image, v_any]], Rotate(ideal_len, -PI/4), ReplacementTransform(notice1, notice2))
        self.waiting(1, 3) #如果我们把光具座立起来

        dash_h = DashedLine(2*UP, 2*UR, stroke_color = BLUE, stroke_width = 2)
        dash_v = DashedLine(2*RIGHT, 2*UR, stroke_color = BLUE, stroke_width = 2)
        focus = Dot(color = BLUE).shift(2*UR)
        self.play(ShowCreation(dash_h), ShowCreation(dash_v), rate_func = rush_into)
        self.play(ShowCreation(focus), rate_func = rush_from)
        self.waiting(1, 19) #并且过两个焦点做平行线 交于一点

        circle_start = Circle(radius = 0.6, color = YELLOW).shift(10/3*UP).save_state()
        dash_line = DashedLine(10/3*UP, 5*RIGHT)
        circle_end = Circle(radius = 0.6, color = YELLOW).shift(5*RIGHT).save_state()
        alpha = ValueTracker(0.0)
        def circle_start_updater(mob: Circle):
            value = alpha.get_value()
            mob.restore().scale(value).pointwise_become_partial(mob, 0, value)
        circle_start.add_updater(circle_start_updater)
        self.add(circle_start).play(alpha.animate.set_value(1.0), rate_func = rush_from, run_time = 1.5)
        circle_start.clear_updaters()
        self.play(circle_start.animate.scale(0), rate_func = rush_into, run_time = 1.5)
        self.remove(circle_start)

        self.add(dash_line, v_any, h_image, focus).play(ShowCreation(dash_line), run_time = 2)

        def circle_end_updater(mob: Circle):
            value = alpha.get_value()
            mob.restore().scale(value).pointwise_become_partial(mob, 0, value)
        self.play(circle_end.animate.scale(0), rate_func = lambda t: rush_into(1-t), run_time = 1.5)
        circle_end.add_updater(circle_end_updater)
        self.play(alpha.animate.set_value(0.0), run_time = 1.5)
        self.remove(circle_end)

        self.waiting(3+2+4-8, 3+2+14) #那么对于竖着的主光轴上的任意一点 只要做过这两点的直线 就一定会交到横着的主光轴上 它的像应该在的位置上

        self.waiting(0, 24) #（到此共75秒）


        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30) 

class Chapter2_2(Scene):
    def construct(self):
        notice2 = Notice("奇妙结论", "请　惊叹")
        notice3 = Notice("易错考点", "请　辨析")
        notice4_material = Notice("典型傲娇", "请　模仿")
        notice4 = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(notice4_material.get_all_points())
        notice5_material = Notice("奇妙结论", "请　惊叹")
        notice5 = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(notice5_material.get_all_points())
        notice6_material = Notice("准备齐全", "请　速通")
        notice6 = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(notice6_material.get_all_points())
        notice7_material = Notice("强势安利", "快 去 看")
        notice7 = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(notice7_material.get_all_points())
        notice8_material = Notice("证明完毕", "请　鼓掌")
        notice8 = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(notice8_material.get_all_points())
        notice9_material = Notice("下节预告", "敬请期待")
        notice9 = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(notice9_material.get_all_points())

        BLUE_G = interpolate_color(BLUE, BACK, 0.5)
        YELLOW_G = interpolate_color(YELLOW, BACK, 0.5)
        ideal_len = Line(3*UP, 3*DOWN).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN).rotate(-PI/4)
        dot_center = Dot(color = YELLOW)
        v_any = Dot(color = YELLOW).shift(10/3*LEFT)
        h_image = Dot(color = YELLOW).shift(5*RIGHT)
        ideal_piece = NumberLine([0, 6, 2], stroke_width = 8, color = BLUE)
        h_left = ideal_piece.copy().shift(3*LEFT).set_color(BLUE_G)
        h_right = ideal_piece.copy().shift(3*RIGHT)
        v_left = ideal_piece.copy().shift(3*LEFT)
        v_right = ideal_piece.copy().shift(3*RIGHT).set_color(BLUE_G)
        h_any = v_any.copy().set_color(YELLOW_G)
        v_image = h_image.copy().set_color(YELLOW_G)
        dash_h = DashedLine(2*UP, 2*UR, stroke_color = BLUE, stroke_width = 2)
        dash_v = DashedLine(2*RIGHT, 2*UR, stroke_color = BLUE, stroke_width = 2)
        dash_line = DashedLine(10/3*UP, 5*RIGHT)
        focus = Dot(color = BLUE).shift(2*UR)
        v_bench = VGroup(v_left, v_right, v_any, v_image).rotate(-PI/2)
        bench = [h_left, v_right, h_right, v_left, ideal_len, dot_center, dash_h, dash_v, dash_line, h_any, v_image, h_image, v_any, focus]
        self.add(notice2, *bench)

        self.play(*[mob.animate.shift(6.5*LEFT + 2.5*DOWN) for mob in bench], ReplacementTransform(notice2, notice3))
        self.waiting(0, 16) #我要特别强调一点

        line_seperate = Line(3*UP, 3*DOWN)
        hole = Line(2*UP, 0.1*UP).append_points(Line(0.1*DOWN, 2*DOWN).get_points()).shift(3*RIGHT)
        arrow = Arrow(DOWN+RIGHT, UP+RIGHT, buff = 0, color = GREEN)
        dash_up = DashedLine(RIGHT+UP, 5*RIGHT+DOWN, stroke_width = 2)
        dash_down = DashedLine(RIGHT+DOWN, 5*RIGHT+UP, stroke_width = 2)
        arrow_image = Arrow(UP+5*RIGHT, DOWN+5*RIGHT, buff = 0, color = GREEN)
        pinhole = VGroup(hole, arrow, dash_up, dash_down, arrow_image)
        neq = MTex(r"\neq", color = RED)
        self.play(ShowCreation(line_seperate))
        self.play(FadeIn(pinhole, DOWN))
        self.play(Write(neq))
        self.waiting(0, 19) #这并不意味着小孔成像和凸透镜成像是一回事
        self.waiting(0, 13) #（空闲）

        self.waiting(1, 28) #把光具座竖起来作图
        self.waiting(2, 6) #并不意味着光真的会走这条路
        self.waiting(0, 18) #（空闲）

        back_left = Rectangle(height = 8, width = 8, fill_color = BLACK, fill_opacity = 1, stroke_width = 0).shift(4*LEFT)
        back_right = Rectangle(height = 8, width = 8, fill_color = BLACK, fill_opacity = 1, stroke_width = 0).shift(4*RIGHT)
        len = Line(3*UP, 3*DOWN).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN)
        ideal_piece.set_stroke(width = 4).scale(np.array([1, 2, 1]))
        x_bench = ideal_piece.copy().shift(3*RIGHT)
        z_bench = ideal_piece.copy().shift(3*LEFT)
        dot = Dot(color = YELLOW)
        former_half = squish_rate_func(rush_into, 0, 0.5)
        latter_half = squish_rate_func(rush_from, 0.5, 1)
        self.add(back_left, back_right, notice3).play(*[FadeIn(mob, rate_func = former_half) for mob in [back_left, back_right]], *[FadeIn(mob, rate_func = latter_half) for mob in [len, x_bench, z_bench, dot]], ReplacementTransform(notice3, notice4))
        self.remove(*bench, line_seperate, pinhole, neq).waiting(1, 18) #但无论如何 它们真的很像

        camera = self.camera.frame
        quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, PI/6))
        self.play(camera.animate.shift(2*OUT+2*RIGHT+2*DOWN).set_orientation(Rotation(quadternion)).set_focal_distance(8.0), run_time = 4)
        self.play(*[Rotate(mob, PI/2, UP, about_point = ORIGIN) for mob in [back_left, z_bench]], *[Rotate(mob, PI/4, UP, about_point = ORIGIN) for mob in [len, dot]], run_time = 3)
        self.waiting(1, 29) #不只是主光轴 我们甚至可以把整张平面竖起来

        line_z = DashedLine(2*OUT, 2*OUT+2*RIGHT, color = BLUE, stroke_width = 2)
        line_x = DashedLine(2*RIGHT, 2*OUT+2*RIGHT, color = BLUE, stroke_width = 2)
        focus = Sphere(radius = 0.08, color = BLUE).shift(2*RIGHT+2*OUT)
        self.play(ShowCreation(line_z), ShowCreation(line_x))
        self.waiting(1, 4) #再过两个焦点做平行线......
        self.play(ShowCreation(focus))
        self.waiting(0, 25) #......交于一个定点

        point_any = Dot(color = YELLOW).shift(10/3*LEFT + 1.2*UP).rotate(PI/2, UP, about_point = ORIGIN)
        line_f = Line(10/3*OUT+1.2*UP, 5*RIGHT + 1.8*DOWN, color = YELLOW)
        point_image = Dot(color = YELLOW).shift(5*RIGHT + 1.8*DOWN)
        self.play(ShowCreation(point_any), ReplacementTransform(notice4, notice5))
        self.waiting(1, 5) #对于竖着的平面上的任意一点
        self.add(line_f, focus).play(ShowCreation(line_f))
        self.waiting(0, 25) #做过这两点的直线
        self.play(ShowCreation(point_image))
        self.waiting(0, 23) #它就会和横着的平面
        self.waiting(1, 27) #相交在这一点的像上
        self.waiting(0, 20) #（空闲）

        self.waiting(2, 2) #这是一条很方便的性质
        self.waiting(4, 4) #在这个视角下 很多结论的证明会变得方便许多
        line_z = Line(8*OUT+3.72*UP, 0.6*DOWN, color = YELLOW)
        line_x = Line(0.6*DOWN, 8*RIGHT+2.52*DOWN, color = ORANGE) 
        line = VGroup(line_z, line_x)
        self.add(line, point_any, point_image, line_f, focus).play(ShowCreation(line))
        self.remove(line).add(line_z, line_x, point_any, point_image, line_f, focus).waiting(2, 15) #比如说 如果我们想要求一条直线的像
        self.waiting(2, 2) #就没必要导比例了

        indicate_z = line_z.copy().set_stroke(width = 8, color = WHITE)
        self.play(ShowPassingFlash(indicate_z), run_time = 1)
        self.play(ShowPassingFlash(indicate_z), run_time = 1)
        self.waiting(0, 7) #竖直平面里面的一条直线
        plane = VMobject(stroke_width = 0, fill_opacity = 0.2, fill_color = BLUE).set_points_as_corners([np.array([0, 3.72, 8]), np.array([0, -0.6, 0]), np.array([8, -2.52, 0]), np.array([8, 1.8, 8])])
        self.add(plane, line, point_any, point_image, line_f, focus, notice5).play(ShowCreation(plane))
        self.waiting(1, 13) #和这个定点会组成一个平面
        indicate_x = line_x.copy().set_stroke(width = 8, color = WHITE)
        self.play(ShowPassingFlash(indicate_x), run_time = 1)
        self.play(ShowPassingFlash(indicate_x), run_time = 1)
        self.waiting(0, 29) #这个平面交水平平面于一条直线

        alpha = ValueTracker(10/3)
        def l(z: float):
            return np.array([0, -0.6+0.54*z, z])
        def focus_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[2]-focus)*np.array([point[2], -point[1], 0])
        def a_updater(mob: Dot):
            z = alpha.get_value()
            position = l(z)
            mob.move_to(position)
        def b_updater(mob: Dot):
            z = alpha.get_value()
            position = focus_trans(l(z))
            mob.move_to(position)
        def line_updater(mob: Line):
            z = alpha.get_value()
            position = l(z)
            destination = focus_trans(position)
            mob.put_start_and_end_on(position, destination)
        point_any.add_updater(a_updater)
        point_image.add_updater(b_updater)
        line_f.add_updater(line_updater)
        self.play(alpha.animate.set_value(5), run_time = 1.5)
        self.play(alpha.animate.set_value(3), run_time = 2)
        self.play(alpha.animate.set_value(4), run_time = 1.5)
        for mob in [point_any, point_image, line_f]:
            mob.clear_updaters()
        self.waiting(3+2-5, 0+23) #而原来直线上的任意一点与定点的连线 一定会和水平平面交于这条直线上
        self.waiting(0, 15) #（空闲）

        alpha = ValueTracker(-0.6)
        def line_z_updater(mob: Line):
            value = alpha.get_value()
            position_1 = value*UP
            position_2 = 2*np.array([0, 1.56, 4]) - position_1
            mob.put_start_and_end_on(position_2, position_1)
        def line_x_updater(mob: Line):
            value = alpha.get_value()
            position_1 = value*UP
            position_2 = 2*np.array([4, -1.56, 0]) - position_1
            mob.put_start_and_end_on(position_1, position_2)
        def plane_updater(mob: VMobject):
            value = alpha.get_value()
            position_1 = value*UP
            position_2 = 2*np.array([0, 1.56, 4]) - position_1
            position_3 = 2*np.array([4, -1.56, 0]) - position_1
            position_4 = position_2 + position_3 - position_1
            mob.set_points_as_corners([position_2, position_1, position_3, position_4])
        line_z.add_updater(line_z_updater)
        line_x.add_updater(line_x_updater)
        plane.add_updater(plane_updater)
        self.play(alpha.animate.set_value(0.0))
        line_indicate = VMobject(stroke_width = 8).set_points([*line_z.get_points(), *line_x.get_points()])
        self.play(ShowPassingFlash(line_indicate), run_time = 1)
        self.play(alpha.animate.set_value(0.6))
        line_indicate = VMobject(stroke_width = 8).set_points([*line_z.get_points(), *line_x.get_points()])
        self.play(ShowPassingFlash(line_indicate), run_time = 1)
        self.play(alpha.animate.set_value(1.2))
        line_indicate = VMobject(stroke_width = 8).set_points([*line_z.get_points(), *line_x.get_points()])
        self.play(ShowPassingFlash(line_indicate), run_time = 1)
        for mob in [line_z, line_x, plane]:
            mob.clear_updaters()

        circle = Circle(radius = 0.8, color = PURPLE).shift(4*LEFT).rotate(PI/2, UP, about_point = ORIGIN)
        self.remove(line_x, line_z).add(line).play(*[Uncreate(mob, rate_func = lambda t: rush_into(1-t)) for mob in [point_any, point_image, line_f, line, plane]], ReplacementTransform(notice5, notice6))
        self.play(ShowCreation(circle), rate_func = rush_from)
        self.waiting(2+2+0+3-8, 22+14+23+7) #也就是说 每一条可能的光路 都会对应一个过这个定点的平面 （空闲） 在这个视角下 视频开头的那个性质
        self.waiting(1, 21) #也只是几句话的事情
        self.waiting(0, 13) #（空闲）

        circle_indicate = circle.copy().set_stroke(color = WHITE, width = 8)
        self.play(ShowPassingFlash(circle_indicate))
        self.waiting(1, 1) #对于竖直平面上的一个圆

        lines = []
        for i in range(8):
            start = 4*OUT + 0.8*np.array([0, np.sin(TAU*i/8), np.cos(TAU*i/8)])
            end = focus_trans(start)
            line_i = Line(start, end, color = YELLOW)
            lines.append(line_i)
        def parameter(u: float, v: float):
            start = 4*OUT + 0.8*np.array([0, np.sin(u), np.cos(u)])
            end = focus_trans(start)
            ratio = (np.cos(v)*end[0], np.sin(v)*start[2])
            ratio /= (ratio[0] + ratio[1])
            return ratio[0]*start + ratio[1]*end
        cone = ParametricSurface(parameter, u_range = (0, TAU), v_range = (0, PI/2), opacity = 0.2, color = YELLOW)
        self.add(*lines, focus).play(*[ShowCreation(mob) for mob in lines])
        self.waiting(1, 22) #我们连接定点和它上面的每一点
        self.add(cone, *lines, focus).play(ShowCreation(cone))
        self.waiting(1, 22) #这些直线构成了一个斜圆锥

        ellipse = circle.copy().apply_function(focus_trans).set_color(ORANGE)
        ellipse_indicate = ellipse.copy().set_stroke(color = WHITE, width = 8)
        self.play(ShowPassingFlash(ellipse_indicate))
        self.play(ShowPassingFlash(ellipse_indicate))
        self.waiting(0, 24) #而如果我们拿平面去截一个斜圆锥
        self.add(ellipse, cone, *lines, focus).play(ShowCreation(ellipse))
        self.waiting(1, 15) #我们总会得到一条圆锥曲线

        shade = Rectangle(width = 16, height = 8, fill_opacity = 1, stroke_width = 0, fill_color = BACK, is_fixed_in_frame = True)
        picture_video = ImageMobject("cover_3.jpg", is_fixed_in_frame = True, height = 2).shift(5*RIGHT)
        text_video = Text("BV1Ks411G7kN", font = "Times New Roman").scale(0.5).next_to(picture_video, UP)
        text_fixed = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(text_video.get_all_points())
        rectangle_video = Rectangle(height = 5.5, width = 5*16/9 + 0.5, is_fixed_in_frame = True).shift(2*LEFT)
        
        self.add(shade, notice6).play(FadeIn(shade), ReplacementTransform(notice6, notice7))
        self.play(FadeIn(picture_video, UP), FadeIn(text_fixed, UP), ShowCreation(rectangle_video))
        self.waiting(0, 13) #如果大家还不熟悉这个结论的话
        self.waiting(2, 2) #三蓝一棕做过一期视频
        self.waiting(2, 12) #介绍了一种绝妙的证法
        self.play(FadeOut(picture_video, DOWN), FadeOut(text_fixed, DOWN), Uncreate(rectangle_video), ReplacementTransform(notice7, notice8)) #就这样 我们证完了

        quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, PI/8))
        self.camera.frame.shift(2*UP)
        self.camera.frame.quadternion = quadternion
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(mob.quadternion, quad(UP, PI/90*dt))
            mob.set_orientation(Rotation(mob.quadternion))
        self.camera.frame.add_updater(camera_updater)
        self.play(FadeOut(shade))

        self.waiting(9, 3) # 到此共102秒
        self.waiting(10, 0) 
        
        self.play(ReplacementTransform(notice8, notice9))
        self.waiting(1, 16) #虽然我们已经解决了开头的问题
        self.waiting(2, 5) #但还剩一点别的事情
        self.add(shade, notice9).play(FadeIn(shade))
        self.camera.frame.suspend_updating()

        last_len = Line(3*UP, 3*DOWN, is_fixed_in_frame = True).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN)
        last_bench = NumberLine([-6, 6, 2], stroke_width = 8, color = BLUE, is_fixed_in_frame = True)
        last_center = Dot(color = YELLOW, is_fixed_in_frame = True)
        
        def tan_color(x: float):
            a = np.arctan(x/4)/(PI/2)+1
            if a > 1:
                return interpolate_color(RED_E, YELLOW_E, a-1)
            else:
                return interpolate_color(YELLOW_E, GREEN_E, a)
        grids = 8
        grid_group = 5
        grey_lines = VGroup(is_fixed_in_frame = True)
        lines = VGroup(is_fixed_in_frame = True)
        for i in range(grids*grid_group + 1):
            height = -(i/grid_group-grids/2)
            line_i = Line(8*LEFT, 8*RIGHT, color = YELLOW_E, stroke_width = 4, is_fixed_in_frame = True).shift(height*UP)
            if i % 5 != 0:
                line_i.set_stroke(width = 1)
            grey_lines.add(line_i.copy())
            line_i.put_start_and_end_on(np.array([-8, height*5, 0]), np.array([8, -height*3, 0]))
            lines.add(line_i)
        grids = 100
        grid_group = 5
        def len_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[0]+focus)*point
        for i in range(grids*grid_group + 1):
            position = i/grid_group-50
            up = 4*UP + position*RIGHT
            down = 4*DOWN + position*RIGHT
            line_i = Line(up, down, stroke_width = 4, is_fixed_in_frame = True)
            if i % 5 != 0:
                line_i.set_stroke(width = 2)
            grey_lines.add(line_i.copy())
            if position != -2:
                line_i.set_color(tan_color(position)).put_start_and_end_on(len_trans(up), len_trans(down))
                lines.add(line_i)
        grey_lines.set_color(GREY).set_opacity(0.5).fade()
        lines.fade()

        shade_2 = shade.copy()
        self.add(grey_lines, lines, last_len, last_bench, last_center, shade_2, notice9).play(FadeOut(shade_2))
        self.waiting(1+2-2, 27+18) #我在第一节的末尾说过 只要凸透镜映射是保直线的
        self.waiting(1, 25) #证明就已经可以结束了
        self.waiting(0, 13) #（空闲）
        self.add(shade_2, notice9).play(FadeIn(shade_2))
        self.remove(grey_lines, lines, last_len, last_bench, last_center, shade_2)
        self.camera.frame.resume_updating()
        self.play(FadeOut(shade))
        self.waiting(0, 13) #但我们把平面竖起来的时候
        self.waiting(2, 7) #似乎没有用到这件事
        self.waiting(2, 6) #保直线性到底代表了什么呢
        
        self.waiting(3, 20)
        self.play(FadeIn(shade))
        self.waiting(4, 0) #到此共102+10+27秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30) 

#########################################################################

class Chapter3_0(Scene):

    def construct(self):

        text3 = Text("第三节 射影变换", font = 'simsun', t2c={"第三节": YELLOW, "射影变换": BLUE}).scale(1.25)

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(Scene):
    def construct(self):
        notice1 = FixedNotice("前情提要", "请　复习")
        notice2 = FixedNotice("问题不大", "请勿惊慌")
        notice3 = FixedNotice("射影几何", "请　听经")
        notice4 = FixedNotice("两点透视", "请　绘图")

        camera = self.camera.frame
        quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, PI/8))
        camera.set_orientation(Rotation(quadternion)).set_focal_distance(12.0)
        offset = np.array([-3, 3, -3])
        plane_z = Rectangle(height = 8, width = 10, stroke_width = 0, fill_opacity = 0.2, fill_color = GREEN).shift(3*LEFT).rotate(PI/2, UP, about_point = ORIGIN).shift(offset)
        plane_x = Rectangle(height = 8, width = 10, stroke_width = 0, fill_opacity = 0.2, fill_color = BLUE).shift(3*RIGHT).shift(offset)
        line_y = Line(4*UP, 4*DOWN, color = TEAL, stroke_opacity = 0.2).shift(offset)

        self.play(Write(notice1))
        self.waiting(1, 24) #先来回顾一下我们在第二节做了什么吧
        self.waiting(0, 15) #（空闲）
        self.play(FadeIn(plane_z, 2*IN), FadeIn(plane_x, 2*LEFT), FadeIn(line_y))
        self.waiting(0, 26) #对于空间中的两张平面

        focus = Sphere(radius = 0.08, color = BLUE).shift(offset + 2*RIGHT+2*OUT)
        self.play(ShowCreation(focus))
        self.waiting(1, 8) #和不在这两张平面上的一点

        point_any = Dot(color = YELLOW).shift(10/3*LEFT + 1.2*UP).rotate(PI/2, UP, about_point = ORIGIN).shift(offset)
        line_f = Line(offset + 2*RIGHT+2*OUT, offset + 2*RIGHT+2*OUT, color = YELLOW)
        point_image = Dot(color = YELLOW).shift(5*RIGHT + 1.8*DOWN).shift(offset)
        self.add(line_f, focus).play(line_f.animate.put_start_and_end_on(offset + 10/3*OUT+1.2*UP, offset + 5*RIGHT + 1.8*DOWN))
        self.play(FadeIn(point_any), FadeIn(point_image))
        self.waiting(0, 20) #我们可以借助过这一点的所有直线

        z = ValueTracker(10/3)
        y = ValueTracker(1.2)
        def point_trans(point: np.ndarray, focus: float = 2):
            point = point - offset
            if point[2] > 2.5:
                result = focus/(point[2]-focus)*np.array([point[2], -point[1], 0])
            else:
                result = 6*np.array([2, 0, 2]) - 5*point
            return result + offset
        def line_trans(point: np.ndarray, focus: float = 2):
            point = point - offset
            if point[2] > 2.5:
                result = focus/(point[2]-focus)*np.array([point[2], -point[1], 0])
            else:
                result = 4*np.array([2, 0, 2]) - 3*point
            return result + offset
        def a_updater(mob: Dot):
            position = np.array([0, y.get_value(), z.get_value()]) + offset
            mob.move_to(position)
        def b_updater(mob: Dot):
            position = np.array([0, y.get_value(), z.get_value()]) + offset
            destination = point_trans(position)
            mob.move_to(destination)
        def line_updater(mob: Line):
            position = np.array([0, y.get_value(), z.get_value()]) + offset
            destination = line_trans(position)
            mob.put_start_and_end_on(position, destination)
        point_any.add_updater(a_updater)
        point_image.add_updater(b_updater)
        line_f.add_updater(line_updater)

        self.play(z.animate.set_value(4), y.animate.set_value(2), run_time = 0.5)
        self.wait(0.5)
        self.play(z.animate.set_value(5), y.animate.set_value(-1), run_time = 0.5)
        self.wait(0.5)
        self.play(z.animate.set_value(3), y.animate.set_value(-1), run_time = 0.5)
        self.waiting(0, 3) #建立两张平面上的一一映射 （空闲）

        infinity_z = plane_x.copy().shift(2*OUT).set_fill(color = YELLOW, opacity = 0.1)
        line_infinity_z = Line(2*OUT+4*DOWN, 2*OUT+4*DOWN, color = YELLOW).shift(offset)
        self.play(ReplacementTransform(notice1, notice2), ApplyMethod(z.set_value, 2, rate_func = squish_rate_func(smooth, 0.4, 0.9)), ApplyMethod(y.set_value, -4, rate_func = squish_rate_func(smooth, 0.4, 0.9)))
        self.waiting(0, 12)
        self.add(infinity_z, focus).play(y.animate.set_value(1), FadeIn(infinity_z), line_infinity_z.animate.put_start_and_end_on(2*OUT+4*DOWN+offset, 2*OUT+4*UP+offset), run_time = 1.5)
        self.wait(0.5)
        for mob in [point_any, point_image, line_f]:
            mob.clear_updaters()
        self.play(FadeOut(point_any, scale = 0), line_f.animate.put_start_and_end_on(offset + 2*RIGHT+2*OUT, offset + 2*RIGHT+2*OUT), run_time = 0.5, rate_func = rush_into)
        self.remove(point_image, line_f)
        point_any = Dot(color = YELLOW).shift(2*RIGHT + 4*DOWN).shift(offset)
        line_f = Line(offset + 2*RIGHT+2*OUT, offset + 2*RIGHT+2*OUT, color = YELLOW)
        self.add(line_f, focus).play(FadeIn(point_any, scale = np.inf), line_f.animate.put_start_and_end_on(offset + 2*RIGHT + 4*DOWN, offset + 4*(2*RIGHT+2*OUT) - 3*(2*RIGHT+4*DOWN)), run_time = 0.5, rate_func = rush_from)
        self.waiting(0.5)

        y = ValueTracker(-4)
        def a_updater(mob: Dot):
            position = np.array([2, y.get_value(), 0]) + offset
            mob.move_to(position)
        def line_updater(mob: Line):
            position = np.array([2, y.get_value(), 0]) + offset
            destination = 4*(2*RIGHT+2*OUT+offset) - 3*position
            mob.put_start_and_end_on(position, destination)
        point_any.add_updater(a_updater)
        line_f.add_updater(line_updater)
        infinity_x = plane_z.copy().shift(2*RIGHT).set_fill(color = YELLOW, opacity = 0.1)
        line_infinity_x = Line(2*RIGHT + 4*DOWN, 2*RIGHT + 4*DOWN, color = YELLOW).shift(offset)
        line_infinite_focus = Line(2*RIGHT + 2*OUT + 4*DOWN, 2*RIGHT + 2*OUT + 4*UP, color = YELLOW, stroke_opacity = 0.2).shift(offset)
        self.add(infinity_x, line_infinite_focus, focus).play(y.animate.set_value(1), FadeIn(infinity_x), FadeIn(line_infinite_focus), line_infinity_x.animate.put_start_and_end_on(2*RIGHT + 4*DOWN + offset, 2*RIGHT + 4*UP + offset), run_time = 1.5)
        self.wait(0.5)
        point_any.clear_updaters()
        line_f.clear_updaters()
        self.play(FadeOut(point_any, scale = 0), line_f.animate.put_start_and_end_on(offset + 2*RIGHT+2*OUT, offset + 2*RIGHT+2*OUT), run_time = 0.5, rate_func = rush_into)
        self.remove(line_f).waiting(2+0+3+2+2-10, 3+15+1+17+3) #当然 这不是一个严格的一一映射 那些平行于两张平面之一的直线 不会和这张平面有交点

        indicate_x = line_infinity_x.copy().set_stroke(color = WHITE, width = 8)
        indicate_z = line_infinity_z.copy().set_stroke(color = WHITE, width = 8)
        self.play(ShowPassingFlash(indicate_x), ShowPassingFlash(indicate_z))
        self.waiting(1, 0)
        self.play(ShowPassingFlash(indicate_x), ShowPassingFlash(indicate_z))
        self.waiting(1, 0)
        self.play(ShowPassingFlash(indicate_x), ShowPassingFlash(indicate_z))
        self.waiting(2+1+0-5, 23+22+20) #从而每张平面上都会有一条直线 上面的点找不到对象 （空闲）

        self.play(ReplacementTransform(notice2, notice3))
        self.waiting(0, 20) #为了避免这种情况
        self.waiting(1, 19) #一种解决方法是
        infinity_plane = Rectangle(width =16, height = 8, color = PURPLE, stroke_width = 0, fill_opacity = 0, is_fixed_in_frame = True)
        self.bring_to_back(infinity_plane).play(infinity_plane.animate.set_fill(opacity = 0.2), rate_func = there_and_back)
        self.play(infinity_plane.animate.set_fill(opacity = 0.2), rate_func = there_and_back)
        self.play(infinity_plane.animate.set_fill(opacity = 0.2), rate_func = there_and_back)
        self.waiting(2+2-3, 12+16) #在空间中加入一些无穷远点 把这个空间变成射影空间

        line_long = VMobject(stroke_width = [1, 2, 3, 4, 4, 3, 2, 1]).set_points_as_corners(
            [64*DOWN, 32*DOWN, 16*DOWN, 8*DOWN, 4*DOWN, 2*DOWN, DOWN, ORIGIN, UP, 2*UP, 4*UP, 8*UP, 16*UP, 32*UP, 64*UP]
            ).shift(offset).insert_n_curves(45)
        line_long_1 = line_long.copy().set_stroke(color = TEAL, opacity = 0.2)
        line_long_2 = line_long.copy().shift(2*OUT).set_stroke(color = YELLOW)
        line_long_3 = line_long.copy().shift(2*RIGHT).set_stroke(color = YELLOW)
        line_long_4 = line_long.copy().shift(2*RIGHT+2*OUT).set_stroke(color = YELLOW, opacity = 0.2)
        line_long_5 = line_long.copy().shift(8*RIGHT).set_stroke(color = BLUE, opacity = 0.2)
        line_long_6 = line_long.copy().shift(8*RIGHT+2*OUT).set_stroke(color = YELLOW, opacity = 0.2)
        line_long_7 = line_long.copy().shift(8*OUT).set_stroke(color = GREEN, opacity = 0.2)
        line_long_8 = line_long.copy().shift(8*OUT+2*RIGHT).set_stroke(color = YELLOW, opacity = 0.2)
        lines_long = [line_long_1, line_long_2, line_long_3, line_long_4, line_long_5, line_long_6, line_long_7, line_long_8]
        
        line_5 = line_y.copy().shift(8*RIGHT).set_stroke(color = BLUE, opacity = 0)
        line_6 = line_y.copy().shift(8*RIGHT+2*OUT).set_stroke(color = YELLOW, opacity = 0)
        line_7 = line_y.copy().shift(8*OUT).set_stroke(color = GREEN, opacity = 0)
        line_8 = line_y.copy().shift(8*OUT+2*RIGHT).set_stroke(color = YELLOW, opacity = 0)
        lines = [line_y, line_infinity_z, line_infinity_x, line_infinite_focus, line_5, line_6, line_7, line_8]
        for line in lines:
            line.set_stroke(width = [4, 4, 4, 4, 4, 4, 4, 4]).insert_n_curves(59)
        self.add(*lines, focus).play(*[Transform(lines[i], lines_long[i]) for i in range(8)])
        self.waiting(0, 13) #在射影空间里

        infinity = np.array([12*np.tan(PI/8), 0, 0])
        infinity_point_x = Dot(radius = 0.05, color = PURPLE, is_fixed_in_frame = True).shift(infinity)
        self.play(FadeIn(infinity_point_x, scale = 0.3))
        self.waiting(1, 28) #每条射影直线恰巧会经过一个无穷远点
        self.waiting(0, 12) #（空闲）

        def projection(point: np.ndarray, view: np.ndarray = 12*unit(-3/8*PI)):
            x_hat = unit(PI/8)
            y_hat = OUT
            difference = point - view
            t = - np.dot(view, view) / np.dot(view, difference)
            position = view + t*difference
            return np.array([np.dot(position, x_hat), np.dot(position, y_hat), 0])
        centers = [ORIGIN, 2*OUT, 2*RIGHT, 2*RIGHT+2*OUT, 8*RIGHT, 8*RIGHT+2*OUT, 8*OUT, 8*OUT+2*RIGHT]
        lines_indicate = [Line(projection(center + offset), infinity, is_fixed_in_frame = True, stroke_width = 2, color = PURPLE) for center in centers]
        self.add(*lines_indicate, focus).play(*[ShowPassingFlash(mob) for mob in lines_indicate])
        self.play(*[ShowPassingFlash(mob) for mob in lines_indicate])
        self.remove(*lines_indicate)
        lines_indicate = [Line(center + offset, center + 12*DOWN + offset, stroke_width = 2, color = PURPLE) for center in centers]
        self.add(*lines_indicate, focus).play(*[ShowPassingFlash(mob) for mob in lines_indicate])
        self.play(*[ShowPassingFlash(mob) for mob in lines_indicate])
        self.remove(*lines_indicate)
        self.waiting(2+2-4, 20+16) #如果我们沿着射影直线走向无穷远 无论是走向左边还是走向右边

        circle_start = Circle(radius = 0.3, color = PURPLE, is_fixed_in_frame = True).shift(infinity).save_state()
        alpha = ValueTracker(0.0)
        def circle_start_updater(mob: Circle):
            value = alpha.get_value()
            mob.restore().scale(value).pointwise_become_partial(mob, 0, value)
        circle_start.add_updater(circle_start_updater)
        self.add(circle_start).play(alpha.animate.set_value(1.0), rate_func = rush_from)
        circle_start.clear_updaters()
        self.play(circle_start.animate.scale(0), rate_func = rush_into)
        self.remove(circle_start)
        self.waiting(0, 21) #我们都会到达同一个无穷远点

        angle = ValueTracker(PI/8)
        focal_distance = ValueTracker(12.0)
        def camera_updater(mob: CameraFrame):
            quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, angle.get_value()))
            mob.set_orientation(Rotation(quadternion)).set_focal_distance(focal_distance.get_value())
        def infinity_updater(mob: Dot):
            mob.move_to(focal_distance.get_value()*np.tan(angle.get_value())*RIGHT)
        camera.add_updater(camera_updater)
        infinity_point_x.add_updater(infinity_updater)
        self.play(ApplyMethod(angle.set_value,-PI/4, run_time = 3), ApplyMethod(focal_distance.set_value, 6.0, run_time = 3), ReplacementTransform(notice3, notice4))
        camera.clear_updaters()
        infinity_point_x.clear_updaters()
        self.waiting(1+2-3, 25+2) #所有的平行的射影直线 都会交于同一个无穷远点

        line_y = Line(2*LEFT, 8*RIGHT).shift(offset)
        line_y_1 = line_y.copy().shift(4*UP).set_stroke(color = BLUE, opacity = 0)
        line_y_2 = line_y.copy().shift(4*DOWN).set_stroke(color = BLUE, opacity = 0)
        line_y_3 = line_y.copy().shift(4*UP + 2*OUT).set_stroke(color = YELLOW, opacity = 0)
        line_y_4 = line_y.copy().shift(4*DOWN + 2*OUT).set_stroke(color = YELLOW, opacity = 0)
        line_y_5 = line_y.copy().shift(4*UP + 4*OUT).set_stroke(color = RED, opacity = 0)
        line_y_6 = line_y.copy().shift(4*DOWN + 4*OUT).set_stroke(color = RED, opacity = 0)
        line_y_7 = line_y.copy().shift(4*UP + 8*OUT).set_stroke(color = GREEN, opacity = 0)
        line_y_8 = line_y.copy().shift(4*DOWN + 8*OUT).set_stroke(color = GREEN, opacity = 0)
        lines_y = [line_y_1, line_y_2, line_y_3, line_y_4, line_y_5, line_y_6, line_y_7, line_y_8]
        for line in lines_y:
            line.set_stroke(width = [4, 4, 4, 4, 4, 4, 4, 4]).insert_n_curves(59)
        line_long_y = VMobject(stroke_width = [1, 2, 3, 4, 4, 3, 2, 1]).set_points_as_corners(
            [64*LEFT, 32*LEFT, 16*LEFT, 8*LEFT, 4*LEFT, 2*LEFT, LEFT, ORIGIN, RIGHT, 2*RIGHT, 4*RIGHT, 8*RIGHT, 16*RIGHT, 32*RIGHT, 64*RIGHT]
            ).shift(offset).insert_n_curves(45)
        line_long_1 = line_long_y.copy().shift(4*UP).set_stroke(color = BLUE, opacity = 0.2)
        line_long_2 = line_long_y.copy().shift(4*DOWN).set_stroke(color = BLUE, opacity = 0.2)
        line_long_3 = line_long_y.copy().shift(4*UP + 2*OUT).set_stroke(color = YELLOW, opacity = 0.2)
        line_long_4 = line_long_y.copy().shift(4*DOWN + 2*OUT).set_stroke(color = YELLOW, opacity = 0.2)
        line_long_5 = line_long_y.copy().shift(4*UP + 4*OUT).set_stroke(color = RED, opacity = 0.2)
        line_long_6 = line_long_y.copy().shift(4*DOWN + 4*OUT).set_stroke(color = RED, opacity = 0.2)
        line_long_7 = line_long_y.copy().shift(4*UP + 8*OUT).set_stroke(color = GREEN, opacity = 0.2)
        line_long_8 = line_long_y.copy().shift(4*DOWN + 8*OUT).set_stroke(color = GREEN, opacity = 0.2)
        lines_long = [line_long_1, line_long_2, line_long_3, line_long_4, line_long_5, line_long_6, line_long_7, line_long_8]
        
        self.add(*lines_y, *lines, focus).play(*[Transform(lines_y[i], lines_long[i]) for i in range(8)])
        self.waiting(0, 21) #而不平行的射影直线

        infinity_point_y = Dot(radius = 0.05, color = PURPLE, is_fixed_in_frame = True).shift(6*RIGHT)
        self.play(FadeIn(infinity_point_y, scale = 0.3))
        self.waiting(1, 2) #会经过不同的无穷远点

        self.waiting(3 ,12) #射影直线的方向决定了它会过哪个无穷远点
        self.waiting(3, 20) #所以无穷远点有时候也被叫做这条射影直线的线向
        self.waiting(0, 24) #到此共62秒
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_2(Scene):
    def construct(self):
        notice4 = FixedNotice("两点透视", "请　绘图")
        notice5 = FixedNotice("照本宣科", "请　听经")
        notice6 = FixedNotice("基本定理", "请　当真")
        notice7 = FixedNotice("温故知新", "请　鼓掌")
        notice8 = FixedNotice("拓展内容", "请　欣赏")

        camera = self.camera.frame
        quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, -PI/4))
        camera.set_orientation(Rotation(quadternion)).set_focal_distance(6.0)
        offset = np.array([-3, 3, -3])
        plane_z = Rectangle(height = 8, width = 10, stroke_width = 0, fill_opacity = 0.2, fill_color = GREEN).shift(3*LEFT).rotate(PI/2, UP, about_point = ORIGIN).shift(offset)
        plane_x = Rectangle(height = 8, width = 10, stroke_width = 0, fill_opacity = 0.2, fill_color = BLUE).shift(3*RIGHT).shift(offset)
        infinity_z = plane_x.copy().shift(2*OUT).set_fill(color = YELLOW, opacity = 0.1)
        infinity_x = plane_z.copy().shift(2*RIGHT).set_fill(color = YELLOW, opacity = 0.1)
        focus = Sphere(radius = 0.08, color = BLUE).shift(offset + 2*RIGHT+2*OUT)

        line_y = VMobject(stroke_width = [1, 2, 3, 4, 4, 3, 2, 1]).set_points_as_corners(
            [64*DOWN, 32*DOWN, 16*DOWN, 8*DOWN, 4*DOWN, 2*DOWN, DOWN, ORIGIN, UP, 2*UP, 4*UP, 8*UP, 16*UP, 32*UP, 64*UP]
            ).shift(offset).insert_n_curves(45)
        line_y_1 = line_y.copy().set_stroke(color = TEAL, opacity = 0.2)
        line_y_2 = line_y.copy().shift(2*OUT).set_stroke(color = YELLOW)
        line_y_3 = line_y.copy().shift(2*RIGHT).set_stroke(color = YELLOW)
        line_y_4 = line_y.copy().shift(2*RIGHT+2*OUT).set_stroke(color = YELLOW, opacity = 0.2)
        line_y_5 = line_y.copy().shift(8*RIGHT).set_stroke(color = BLUE, opacity = 0.2)
        line_y_6 = line_y.copy().shift(8*RIGHT+2*OUT).set_stroke(color = YELLOW, opacity = 0.2)
        line_y_7 = line_y.copy().shift(8*OUT).set_stroke(color = GREEN, opacity = 0.2)
        line_y_8 = line_y.copy().shift(8*OUT+2*RIGHT).set_stroke(color = YELLOW, opacity = 0.2)
        lines_y = [line_y_1, line_y_2, line_y_3, line_y_4, line_y_5, line_y_6, line_y_7, line_y_8]
        
        line_x = VMobject(stroke_width = [1, 2, 3, 4, 4, 3, 2, 1]).set_points_as_corners(
            [64*LEFT, 32*LEFT, 16*LEFT, 8*LEFT, 4*LEFT, 2*LEFT, LEFT, ORIGIN, RIGHT, 2*RIGHT, 4*RIGHT, 8*RIGHT, 16*RIGHT, 32*RIGHT, 64*RIGHT]
            ).shift(offset).insert_n_curves(45)
        line_x_1 = line_x.copy().shift(4*UP).set_stroke(color = BLUE, opacity = 0.2)
        line_x_2 = line_x.copy().shift(4*DOWN).set_stroke(color = BLUE, opacity = 0.2)
        line_x_3 = line_x.copy().shift(4*UP + 2*OUT).set_stroke(color = YELLOW, opacity = 0.2)
        line_x_4 = line_x.copy().shift(4*DOWN + 2*OUT).set_stroke(color = YELLOW, opacity = 0.2)
        line_x_5 = line_x.copy().shift(4*UP + 4*OUT).set_stroke(color = RED, opacity = 0.2)
        line_x_6 = line_x.copy().shift(4*DOWN + 4*OUT).set_stroke(color = RED, opacity = 0.2)
        line_x_7 = line_x.copy().shift(4*UP + 8*OUT).set_stroke(color = GREEN, opacity = 0.2)
        line_x_8 = line_x.copy().shift(4*DOWN + 8*OUT).set_stroke(color = GREEN, opacity = 0.2)
        lines_x = [line_x_1, line_x_2, line_x_3, line_x_4, line_x_5, line_x_6, line_x_7, line_x_8]

        infinity_point_x = Dot(radius = 0.05, color = PURPLE, is_fixed_in_frame = True).shift(6*LEFT)
        infinity_point_y = Dot(radius = 0.05, color = PURPLE, is_fixed_in_frame = True).shift(6*RIGHT)
        infinity_line_xy = Line(8*LEFT, 8*RIGHT, color = PURPLE, is_fixed_in_frame = True)
        
        self.add(plane_z, plane_x, infinity_z, infinity_x, *lines_x, *lines_y, focus, infinity_point_x, infinity_point_y, notice4)
        
        infinity_plane = Rectangle(width =16, height = 8, color = PURPLE, stroke_width = 0, fill_opacity = 0, is_fixed_in_frame = True)
        self.bring_to_back(infinity_plane).play(infinity_plane.animate.set_fill(opacity = 0.2), rate_func = there_and_back)
        self.play(infinity_plane.animate.set_fill(opacity = 0.2), rate_func = there_and_back)
        self.play(infinity_plane.animate.set_fill(opacity = 0.2), rate_func = there_and_back)
        self.waiting(1+2-3, 12+20) #所有的无穷远点 构成了这个射影空间的无穷远平面

        def projection(point: np.ndarray, view: np.ndarray = 6*unit(-3/4*PI)):
            x_hat = unit(-PI/4)
            y_hat = OUT
            difference = point - view
            t = - np.dot(view, view) / np.dot(view, difference)
            position = view + t*difference
            return np.array([np.dot(position, x_hat), np.dot(position, y_hat), 0])
        
        plane_x_projected = VMobject(stroke_width = 0, fill_opacity = 0.2, fill_color = BLUE, is_fixed_in_frame = True).set_points_as_corners([projection(2*LEFT+4*UP+offset), projection(2*LEFT+4*DOWN+offset), projection(8*RIGHT+4*DOWN+offset), projection(8*RIGHT+4*UP+offset)])

        alpha = ValueTracker(0.0)
        def plane_x_updater(mob: Rectangle):
            scale = np.power(2, (alpha.get_value()))
            corners = [projection(scale*(8*RIGHT+4*DOWN)+offset), projection(scale*(8*RIGHT+4*UP)+offset), projection(scale*(2*LEFT+4*UP)+offset)]
            problem = scale*(2*LEFT+4*DOWN)+offset
            cut_1 = np.array([problem[0], -3/np.sqrt(2)-problem[0], problem[2]])
            cut_2 = np.array([-3/np.sqrt(2)-problem[1], problem[1], problem[2]])
            corners.extend([projection(cut_1), projection(cut_2)])
            mob.set_points_as_corners(corners)
        plane_x_projected.add_updater(plane_x_updater)
        plane_x.set_opacity(0)
        self.bring_to_back(plane_x_projected).play(plane_x_projected.animate.set_opacity(0.05), plane_x.animate.set_opacity(0.2), alpha.animate.set_value(8.0), run_time = 2)
        plane_x_projected.clear_updaters()
        self.bring_to_back(infinity_line_xy).play(ShowCreation(infinity_line_xy))
        self.waiting(1+2-3, 25+15) #而任意一张射影平面 会和它交于一条无穷远直线

        point_any = Dot(color = YELLOW).shift(2*LEFT+3.5*DOWN).rotate(PI/2, UP, about_point = ORIGIN).shift(offset)
        projection_any = projection((2*OUT+3.5*DOWN) + offset)
        projection_image = projection(6*unit(-3/4*PI) + (2*OUT+3.5*DOWN) - (2*RIGHT+2*OUT))
        line_f = Line(projection_any, projection_image, color = [YELLOW, YELLOW, YELLOW, YELLOW, PURPLE], is_fixed_in_frame = True).insert_n_curves(4)
        point_image = Dot(radius = 0.05, color = PURPLE, is_fixed_in_frame = True).shift(projection_image)

        circle_start = Circle(radius = 0.24, color = YELLOW).shift(2*LEFT+3.5*DOWN).rotate(PI/2, UP, about_point = ORIGIN).shift(offset).save_state()
        alpha = ValueTracker(0.0)
        def circle_start_updater(mob: Circle):
            value = alpha.get_value()
            mob.restore().scale(value).pointwise_become_partial(mob, 0, value)
        circle_start.add_updater(circle_start_updater)
        self.add(circle_start).play(alpha.animate.set_value(1.0), rate_func = rush_from)
        circle_start.clear_updaters()
        self.play(circle_start.animate.scale(1/3).set_stroke(width = 0), FadeIn(point_any, scale = 1/3), rate_func = rush_into)
        self.remove(circle_start)
        self.add(line_f, focus).play(ShowCreation(line_f))
        self.play(ShowCreation(point_image))
        self.waiting(2+3-5, 27+7)

        alpha = ValueTracker(-3.5)
        def a_updater(mob: Dot):
            position = np.array([0, alpha.get_value(), 2]) + offset
            mob.move_to(position)
        def b_updater(mob: Dot):
            position = np.array([0, alpha.get_value(), 2]) + offset
            destination = projection(6*unit(-3/4*PI) + position - (2*RIGHT+2*OUT) - offset)
            mob.move_to(destination)
        def line_updater(mob: Line):
            position = np.array([0, alpha.get_value(), 2]) + offset
            destination = projection(6*unit(-3/4*PI) + position - (2*RIGHT+2*OUT) - offset)
            mob.put_start_and_end_on(projection(position), destination)
        point_any.add_updater(a_updater)
        point_image.add_updater(b_updater)
        line_f.add_updater(line_updater)
        self.play(alpha.animate.set_value(-1.5), run_time = 0.5) 
        self.wait(0.5) #这样 原本找不到对象的那条直线 就会被对应到另一张平面的无穷远直线上
        self.play(alpha.animate.set_value(-2.5), run_time = 0.5)
        self.wait(0.5)
        self.play(alpha.animate.set_value(-0.5), run_time = 0.5)
        self.wait(0.5)
        for mob in [point_any, point_image, line_f]:
            mob.clear_updaters()
        self.play(Uncreate(point_any), Uncreate(point_image), line_f.animate.put_start_and_end_on(projection((2*RIGHT+2*OUT) + offset), projection((2*RIGHT+2*OUT) + offset)), FadeOut(plane_x_projected))
        self.waiting(0, 7) #两张射影平面间的一一映射就能被建立起来了
        self.waiting(0, 15) #（空闲）

        angle = ValueTracker(-PI/4)
        focal_distance = ValueTracker(6.0)
        camera_x = ValueTracker(0.0)
        def camera_updater(mob: CameraFrame):
            quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, angle.get_value()))
            mob.move_to(np.array([camera_x.get_value(), 0, 0])).set_orientation(Rotation(quadternion)).set_focal_distance(focal_distance.get_value())
        def infinity_y_updater(mob: Dot):
            mob.move_to(focal_distance.get_value()*np.tan(angle.get_value())*RIGHT)
        def infinity_x_updater(mob: Dot):
            mob.move_to(focal_distance.get_value()*np.tan(angle.get_value()-PI/2)*RIGHT)
        camera.add_updater(camera_updater)
        infinity_point_x.add_updater(infinity_x_updater)
        infinity_point_y.add_updater(infinity_y_updater)

        def focus_trans(point: np.ndarray, focus: float = 2):
            point = point - offset
            result = focus/(point[2]-focus)*np.array([point[2], -point[1], 0])
            return result + offset

        circle = Circle(radius = 1.2, color = PURPLE, n_components = 24).shift(4.1*LEFT+0.1*UP).rotate(PI/2, UP, about_point = ORIGIN).shift(offset)
        starts = [4.1*OUT + 0.1*UP + 1.2*np.array([0, np.sin(TAU*i/8 + TAU/16), np.cos(TAU*i/8 + TAU/16)]) + offset for i in range(8)]
        ends = [focus_trans(start) for start in starts]
        lines = [Line(starts[i], ends[i], color = YELLOW, stroke_width = 2) for i in range(8)]

        ellipse = circle.copy().apply_function(focus_trans).set_color(ORANGE)
        perspective = FixedTex(r"\text{透视变换}").set_color(YELLOW).shift(3*UP + 4.4*LEFT).scale(0.8, about_point = 7*LEFT)
        line_y = Line(4*UP, 4*DOWN, color = TEAL, stroke_opacity = 0.2).shift(offset)

        self.add(*lines, focus).play(
            Write(perspective, run_time = 3, rate_func = squish_rate_func(smooth, 2/3, 1)), 
            *[ShowCreation(mob, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)) for mob in lines], 
            *[FadeOut(mob) for mob in [*lines_x, *lines_y, infinity_x, infinity_z, infinity_point_x, infinity_point_y, infinity_line_xy]], 
            FadeIn(line_y), 
            ApplyMethod(angle.set_value, PI/8, run_time = 3), ApplyMethod(focal_distance.set_value, 12.0, run_time = 3), 
            ApplyMethod(camera_x.set_value, -1, run_time = 3), 
            ReplacementTransform(notice4, notice5))
        camera.clear_updaters()
        infinity_point_x.clear_updaters()
        infinity_point_y.clear_updaters()
        self.waiting(0, 16) #这样的一一映射 一般被叫做透视变换

        plane_y = Square(side_length = 8, stroke_width = 0, fill_opacity = 0.2, fill_color = RED).shift(4*RIGHT).rotate(-PI/2, RIGHT, about_point = 4*UP).shift(offset)
        self.bring_to_back(plane_y).play(FadeIn(plane_y, RIGHT+OUT))
        self.waiting(0, 24) #而如果对不同的平面

        focus_2 = Sphere(radius = 0.08, color = RED).shift(offset + 4*RIGHT+2*OUT+2*UP)

        def focus_trans_2(point: np.ndarray, focus: float = 2):
            point = point - offset - 4*RIGHT - 4*UP
            result = focus/(point[1]+focus)*np.array([point[0], 0, point[1]])
            return result + offset + 4*RIGHT + 4*UP
        ends_2 = [focus_trans_2(end) for end in ends]
        lines_2 = [Line(ends[i], ends_2[i], color = ORANGE, stroke_width = 2) for i in range(8)]
        ellipse_2 = ellipse.copy().apply_function(focus_trans_2).set_color(RED)

        self.add(*lines_2, focus_2, *lines, focus).play(*[ShowCreation(mob) for mob in [*lines_2, focus_2]])
        self.waiting(1, 7) #连续做好几次透视变换

        project = FixedTex(r"\text{射影变换}=\text{透视变换}^n").set_color(YELLOW).next_to(0*DOWN + 7*LEFT).scale(0.8, about_point = 7*LEFT)

        self.play(Write(project))
        self.waiting(2, 0) #那么总体的映射 就被称为射影变换
        self.waiting(0, 19) #（空闲）

        line_conserve = FixedTex(r"\text{保直线}").set_color(ORANGE).shift(2*UP + 3*LEFT).scale(0.8, about_point = 7*LEFT)
        conic_conserve = FixedTex(r"\text{保圆锥曲线}").set_color(ORANGE).shift(2*DOWN + 3*LEFT).scale(0.8, about_point = 7*LEFT)

        arrow_1_1 = Arrow(0.5*UP+3*LEFT, 1.5*UP+3*LEFT, buff = 0, color = [YELLOW, ORANGE], is_fixed_in_frame = True).scale(0.8, about_point = 7*LEFT)
        arrow_1_2 = Arrow(0.5*DOWN+3*LEFT, 1.5*DOWN+3*LEFT, buff = 0, color = [YELLOW, ORANGE], is_fixed_in_frame = True).scale(0.8, about_point = 7*LEFT)
        arrow_2_1 = Arrow(0.5*UP+4.8*LEFT, 1.5*UP+3.6*LEFT, buff = 0, color = [YELLOW, ORANGE], is_fixed_in_frame = True).scale(0.8, about_point = 7*LEFT)
        arrow_2_2 = Arrow(0.5*DOWN+4.8*LEFT, 1.5*DOWN+3.6*LEFT, buff = 0, color = [YELLOW, ORANGE], is_fixed_in_frame = True).scale(0.8, about_point = 7*LEFT)
        concepts = [perspective, project, line_conserve, conic_conserve, arrow_1_1, arrow_1_2, arrow_2_1, arrow_2_2]
        self.play(ShowCreation(arrow_1_1))
        self.play(Write(line_conserve))
        self.waiting(1, 0) #由于透视变换会把直线映射成直线
        self.add(circle, *lines_2, focus_2, *lines, focus).play(ShowCreation(arrow_1_2), ShowCreation(circle))
        self.add(ellipse, *lines_2, focus_2, *lines, focus).play(Write(conic_conserve), ShowCreation(ellipse))
        self.waiting(0, 17) #把圆锥曲线映射成圆锥曲线
        self.waiting(1, 23) #作为透视变换的复合
        self.play(ShowCreation(arrow_2_1))
        self.waiting(1, 27) #射影变换也会把直线映射成直线
        self.add(ellipse_2, *lines_2, focus_2, *lines, focus).play(ShowCreation(arrow_2_2), ShowCreation(ellipse_2))
        self.waiting(1, 11) #把圆锥曲线映射成圆锥曲线
        self.waiting(0, 14) #（空闲）


        shade = Rectangle(width = 0, height = 1, fill_opacity = 1, fill_color = BACK, stroke_width = 0, is_fixed_in_frame = True).shift(3.5*UP)
        shade_1 = Rectangle(width = 16, height = 1.2, fill_opacity = 1, fill_color = BACK, stroke_width = 0, is_fixed_in_frame = True).shift(3.5*UP)
        shade_2 = Rectangle(width = 16, height = 8, fill_opacity = 1, fill_color = BACK, stroke_width = 0, is_fixed_in_frame = True)
        title = FixedText("射影几何", font = "simsun").set_color(YELLOW).next_to(3*UP, UP)
        title_line = Line(3*UP, 3*UP, is_fixed_in_frame = True)
        self.play(Transform(shade, shade_1), Write(title), title_line.animate.put_start_and_end_on(3*UP+6*LEFT, 3*UP+6*RIGHT))
        self.waiting(3, 26) #射影几何就是建立在射影平面 或者更一般的射影空间上的几何体系
        self.waiting(0, 14) #（空闲）

        self.add(shade, title, title_line, notice5).play(Transform(shade, shade_2), ReplacementTransform(notice5, notice6))
        self.waiting(0, 22) #和其它很多领域一样

        fundamental = ImageMobject("fundamental.jpg", height = 700/1080*8, is_fixed_in_frame = True).shift(0.2*UP + 2*RIGHT)
        fundamental_text = FixedText("射影几何基本定理, Geometric Algebra, E. Artin, p.88", font = "simsun").scale(0.5).shift(2.6*DOWN + 2*RIGHT)
        self.play(FadeIn(fundamental, 0.5*UP), FadeIn(fundamental_text, 0.5*UP))
        self.waiting(1, 9) #射影几何中也有一个基本定理
        self.waiting(2, 2) #射影几何基本定理

        cover_fundamental = ImageMobject("cover_4.jpg", height = 2, is_fixed_in_frame = True).shift(UP + 4*LEFT)
        bv_fundamental = FixedText("BV19f4y137mJ", font = "Times New Roman").scale(0.5).next_to(cover_fundamental, UP, buff = 0.1)
        gossip_fundamental = FixedText("关于“对称多项式基本定理”的视频，\n视频长33分钟，大半篇幅都在讲证明。\n这个基本定理属于基本定理中很好证的一类。\n视频中也介绍了别的一些基本定理。\n\n以及，这期视频的up主，@凡人忆拾，\n已经一年多没更新了。", font = "simsun").scale(0.4).next_to(cover_fundamental, DOWN)
        #gossip_fundamental = FixedText("关于“对称多项式基本定理”的视频", font = "simsun").scale(0.4).next_to(cover_fundamental, DOWN)
        self.play(FadeIn(cover_fundamental, 0.5*UP), FadeIn(bv_fundamental, 0.5*UP))
        self.play(ShowIncreasingSubsets(gossip_fundamental), run_time = 3)
        self.waiting(1+2-4, 18+20) #它和别的基本定理一样 证明十分冗长 难度颇高
        self.waiting(2, 7) #但是结论简单而漂亮

        self.play(*[FadeOut(mob) for mob in [cover_fundamental, bv_fundamental, gossip_fundamental]])
        shade_temp = Rectangle(height = 5.6, width = 5, stroke_width = 0, fill_opacity = 1, fill_color = BACK, is_fixed_in_frame = True).next_to(7*LEFT, buff = 0)
        self.add(*concepts, shade_temp).play(FadeOut(shade_temp))
        self.waiting(1, 16) #把它应用到射影平面上 就会得到这样的结论

        arrow_3 = Arrow(1.5*UP+4.0*LEFT, 0.5*UP+5.2*LEFT, buff = 0, color = [ORANGE, YELLOW], is_fixed_in_frame = True).scale(0.8, about_point = 7*LEFT)
        surrounding = SurroundingRectangle(line_conserve, is_fixed_in_frame = True, buff = 0.2).rotate(PI)
        self.play(ShowCreation(surrounding))
        self.waiting(2, 0) #如果一个映射将直线映射成直线
        self.play(Uncreate(surrounding), ShowCreation(arrow_3))
        self.waiting(0, 29) #它就是一个射影变换

        shade_upper = shade.copy()
        self.add(shade_upper, notice6).play(FadeIn(shade_upper), ReplacementTransform(notice6, notice7))
        last_len = Line(3*UP, 3*DOWN, is_fixed_in_frame = True).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN)
        last_bench = NumberLine([-6, 6, 2], stroke_width = 8, color = BLUE, is_fixed_in_frame = True)
        last_center = Dot(color = YELLOW, is_fixed_in_frame = True)
        
        def tan_color(x: float):
            a = np.arctan(x/4)/(PI/2)+1
            if a > 1:
                return interpolate_color(RED_E, YELLOW_E, a-1)
            else:
                return interpolate_color(YELLOW_E, GREEN_E, a)
        grids = 8
        grid_group = 5
        grey_lines = VGroup(is_fixed_in_frame = True)
        lines = VGroup(is_fixed_in_frame = True)
        for i in range(grids*grid_group + 1):
            height = -(i/grid_group-grids/2)
            line_i = Line(8*LEFT, 8*RIGHT, color = YELLOW_E, stroke_width = 4, is_fixed_in_frame = True).shift(height*UP)
            if i % 5 != 0:
                line_i.set_stroke(width = 1)
            grey_lines.add(line_i.copy())
            line_i.put_start_and_end_on(np.array([-8, height*5, 0]), np.array([8, -height*3, 0]))
            lines.add(line_i)
        grids = 100
        grid_group = 5
        def len_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[0]+focus)*point
        for i in range(grids*grid_group + 1):
            position = i/grid_group-50
            up = 4*UP + position*RIGHT
            down = 4*DOWN + position*RIGHT
            line_i = Line(up, down, stroke_width = 4, is_fixed_in_frame = True)
            if i % 5 != 0:
                line_i.set_stroke(width = 2)
            grey_lines.add(line_i.copy())
            if position != -2:
                line_i.set_color(tan_color(position)).put_start_and_end_on(len_trans(up), len_trans(down))
                lines.add(line_i)
        grey_lines.set_color(GREY).set_opacity(0.5).fade()
        lines.fade()

        shade_upper_2 = shade.copy()
        self.add(grey_lines, lines, last_len, last_bench, last_center, shade_2, notice7).play(FadeOut(shade_2))
        self.waiting(1, 13) #既然凸透镜变换会把直线映射到直线
        self.play(FadeOut(grey_lines), FadeOut(lines))
        self.waiting(1, 6) #那么它就是一个射影变换
        circle_flat = Circle(radius = 0.8, color = PURPLE, n_components = 24, is_fixed_in_frame = True).shift(4*LEFT)
        def len_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[0]+focus)*point
        ellipse_flat = circle_flat.copy().apply_function(len_trans).set_color(ORANGE)
        self.play(ShowCreation(circle_flat), ShowCreation(ellipse_flat))
        self.waiting(1, 20) #就会把圆锥曲线映射到圆锥曲线
        self.waiting(0, 13) #（空闲）

        self.waiting(3, 7) #当然 实际情况会更舒服一些
        self.waiting(2, 26) #凸透镜变换不止是个射影变换
        self.add(shade_upper_2, notice7).play(FadeIn(shade_upper_2))
        self.clear()

        back_left = Rectangle(height = 8, width = 8, fill_color = BLACK, fill_opacity = 1, stroke_width = 0).shift(4*LEFT).rotate(PI/2, UP, about_point = ORIGIN)
        back_right = Rectangle(height = 8, width = 8, fill_color = BLACK, fill_opacity = 1, stroke_width = 0).shift(4*RIGHT)
        len = Line(3*UP, 3*DOWN).add(Line(3*UP, 3*UP+0.25*DL), Line(3*UP, 3*UP+0.25*DR), Line(3*DOWN, 3*DOWN+0.25*UL), Line(3*DOWN, 3*DOWN+0.25*UR)).set_color(GREEN).rotate(PI/4, UP, about_point = ORIGIN)
        ideal_piece = NumberLine([0, 6, 2], stroke_width = 8, color = BLUE)
        ideal_piece.set_stroke(width = 4).scale(np.array([1, 2, 1]))
        x_bench = ideal_piece.copy().shift(3*RIGHT)
        z_bench = ideal_piece.copy().shift(3*LEFT).rotate(PI/2, UP, about_point = ORIGIN)
        dot = Dot(color = YELLOW).rotate(PI/4, UP, about_point = ORIGIN)
        line_z = DashedLine(2*OUT, 2*OUT+2*RIGHT, color = BLUE, stroke_width = 2)
        line_x = DashedLine(2*RIGHT, 2*OUT+2*RIGHT, color = BLUE, stroke_width = 2)
        focus = Sphere(radius = 0.08, color = BLUE).shift(2*RIGHT+2*OUT)
        circle = Circle(radius = 0.8, color = PURPLE).shift(4*LEFT).rotate(PI/2, UP, about_point = ORIGIN)
        def focus_trans(point: np.ndarray, focus: float = 2):
            return focus/(point[2]-focus)*np.array([point[2], -point[1], 0])
        lines = []
        for i in range(8):
            start = 4*OUT + 0.8*np.array([0, np.sin(TAU*i/8), np.cos(TAU*i/8)])
            end = focus_trans(start)
            line_i = Line(start, end, color = YELLOW)
            lines.append(line_i)
        def parameter(u: float, v: float):
            start = 4*OUT + 0.8*np.array([0, np.sin(u), np.cos(u)])
            end = focus_trans(start)
            ratio = (np.cos(v)*end[0], np.sin(v)*start[2])
            ratio /= (ratio[0] + ratio[1])
            return ratio[0]*start + ratio[1]*end
        cone = ParametricSurface(parameter, u_range = (0, TAU), v_range = (0, PI/2), opacity = 0.2, color = YELLOW)
        ellipse = circle.copy().apply_function(focus_trans).set_color(ORANGE)
        
        quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, PI/8))
        camera.move_to(2*OUT+2*RIGHT).set_orientation(Rotation(quadternion)).set_focal_distance(8.0)
        camera.quadternion = quadternion
        def camera_updater(mob, dt):
            mob.quadternion = quaternion_mult(mob.quadternion, quad(UP, PI/30*dt))
            mob.set_orientation(Rotation(mob.quadternion))
        camera.add_updater(camera_updater)

        self.add(camera, back_left, back_right, len, x_bench, z_bench, dot, line_z, line_x, circle, ellipse, cone, *lines, focus, shade, notice7)
        self.play(FadeOut(shade))
        self.waiting(2 ,3) #当我们把物平面和像平面摆在恰当的位置的时候
        self.waiting(2, 16) #它甚至是一个透视变换
        self.waiting(3, 24) #这也解释了为什么凸透镜变换和小孔成像很像
        self.waiting(2, 28) #毕竟所有的小孔成像都是透视变换
        self.waiting(0, 25) #到此共98秒

        self.play(ReplacementTransform(notice7, notice8))
        self.waiting(2, 4) #总之 我们证明了一个平面上的结论
        self.waiting(2, 17) #但实际上借助了三维空间
        self.add(shade, notice8).play(FadeIn(shade))
        


        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)


class Chapter3_3(Scene):
    def construct(self):
        notice8 = FixedNotice("拓展内容", "请　欣赏")

        self.add(notice8)
        self.waiting(3, 4) #总之 我们证明了一个平面上的结论
        self.waiting(2, 17) #但实际上借助了三维空间
        self.waiting(2, 25) #这样的例子在几何中其实很常见

        background = Rectangle(width = 16, height = 8, fill_opacity = 1, stroke_width = 0, fill_color = BLACK)
        ex_1 = 2.5*DOWN + 4*LEFT
        ex_2 = 2.5*DOWN
        ex_3 = 2.5*DOWN + 4*RIGHT
        center_1 = LEFT+2.5*UP
        center_2 = 0.5*center_1 + 0.5*ex_1
        center_3 = 1/3*center_1 + 2/3*ex_2
        point_e1 = Dot(radius = 0.05, color = ORANGE).shift(ex_1)
        point_e2 = Dot(radius = 0.05, color = ORANGE).shift(ex_2)
        point_e3 = Dot(radius = 0.05, color = ORANGE).shift(ex_3)
        ball_e1 = Sphere(radius = 0.05, color = ORANGE).shift(ex_1)
        ball_e2 = Sphere(radius = 0.05, color = ORANGE).shift(ex_2)
        ball_e3 = Sphere(radius = 0.05, color = ORANGE).shift(ex_3)
        circle_o1 = Circle(radius = 1.2, color = YELLOW).shift(center_1)
        circle_o2 = Circle(radius = 0.6, color = YELLOW).shift(center_2)
        circle_o3 = Circle(radius = 0.4, color = YELLOW).shift(center_3)
        plane_exsimilicenters = [point_e1, point_e2, point_e3]
        circles = [circle_o1, circle_o2, circle_o3]
        exsimilicenters = [ball_e1, ball_e2, ball_e3]
        collinear = Line(8*LEFT+2.5*DOWN, 8*RIGHT+2.5*DOWN, color = RED)

        def tangent(point: np.ndarray, center: np.ndarray, radius: float):
            vector = point - center
            slope = np.arctan2(vector[1], vector[0])
            norm = get_norm(vector)
            angle = np.arccos(radius / norm)
            tangent_1 = center + radius*unit(slope + angle)
            tangent_2 = center + radius*unit(slope - angle)
            return [DashedLine(tangent_1, point), DashedLine(tangent_2, point)]
        tangent_1 = tangent(ex_1, center_1, 1.2)
        tangent_2 = tangent(ex_2, center_1, 1.2)
        tangent_3 = tangent(ex_3, center_2, 0.6)
        tangents = [*tangent_1, *tangent_2, *tangent_3]
        for mob in tangents:
            mob.set_stroke(width = 2, color = ORANGE)

        self.bring_to_back(background).play(FadeIn(background), LaggedStart(*[ShowCreation(mob) for mob in circles], run_time = 1.5))
        self.add(*circles).waiting(0.5, 26) #比如 对于平面上的任意三个圆
        self.play(LaggedStart(*[ShowCreation(mob) for mob in tangents]), run_time = 1.5)
        self.waiting(0, 14) #分别作它们两两的外公切线......
        self.play(LaggedStart(*[ShowCreation(mob) for mob in plane_exsimilicenters]), run_time = 1.5) #交于三个点
        self.add(collinear, *plane_exsimilicenters).play(ShowCreation(collinear))
        self.remove(*plane_exsimilicenters).add(*exsimilicenters)
        self.waiting(0, 29) #那么这三点共线

        camera = self.camera.frame
        quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, -5*PI/12))
        target = camera.copy().shift(1.2*OUT+2*LEFT+0*DOWN).set_orientation(Rotation(quadternion))
        
        sphere_1_lower = Sphere(radius = 1.2, color = BLUE, v_range = (0, PI/2), fill_opacity = 1).shift(center_1)
        sphere_1_upper = Sphere(radius = 1.2, color = BLUE, v_range = (PI/2, PI)).shift(center_1)
        sphere_2_lower = Sphere(radius = 0.6, color = BLUE, v_range = (0, PI/2), fill_opacity = 1).shift(center_2)
        sphere_2_upper = Sphere(radius = 0.6, color = BLUE, v_range = (PI/2, PI)).shift(center_2)
        sphere_3_lower = Sphere(radius = 0.4, color = BLUE, v_range = (0, PI/2), fill_opacity = 1).shift(center_3)
        sphere_3_upper = Sphere(radius = 0.4, color = BLUE, v_range = (PI/2, PI)).shift(center_3)
        spheres_lower = [sphere_1_lower, sphere_2_lower, sphere_3_lower]
        spheres_upper = [sphere_1_upper, sphere_2_upper, sphere_3_upper]
        self.add(*spheres_upper).bring_to_back(*spheres_lower).play(
            ApplyMethod(background.set_opacity, 0.2, run_time = 2), 
            Transform(camera, target, run_time = 4, rate_func = squish_rate_func(smooth, 0, 0.75)),
            *[ShowCreation(mob, run_time = 4, rate_func = squish_rate_func(rush_into, 0.5, 0.75)) for mob in spheres_lower], 
            *[ShowCreation(mob, run_time = 4, rate_func = squish_rate_func(rush_from, 0.75, 1)) for mob in spheres_upper], 
            )
        self.waiting(2+1-4, 13+18) #如果我们把视角放到空间中 把圆变成球

        theta = np.arcsin(1.2/5)
        tangent_plane_1 = background.copy().set_fill(color = ORANGE, opacity = 0.1).rotate(theta, RIGHT, about_point = 2.5*DOWN)
        tangent_plane_2 = background.copy().set_fill(color = ORANGE, opacity = 0.1).rotate(-theta, RIGHT, about_point = 2.5*DOWN)
        self.add(tangent_plane_1).bring_to_back(tangent_plane_2).play(
            FadeIn(tangent_plane_1, np.array([0, np.cos(theta), np.sin(theta)])), FadeIn(tangent_plane_2, np.array([0, np.cos(theta), -np.sin(theta)])), 
            run_time = 1.5)
        self.waiting(0.5, 19) #那么这三个球会有两个外公切面
        indicate = collinear.copy().set_stroke(width = 8, color = WHITE)
        self.add(indicate, *exsimilicenters).play(ShowPassingFlash(indicate))
        self.waiting(0, 21) #它们交于一条直线
        self.waiting(1+0-1, 23+28)
        shade = Rectangle(width = 16, height = 8, color = BACK, stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True)
        self.play(FadeIn(shade))
        self.remove(shade, *circles, *exsimilicenters, collinear, *tangents, *spheres_lower, *spheres_upper, background, tangent_plane_1, tangent_plane_2)
        camera.move_to(ORIGIN).set_orientation(Rotation(quad(RIGHT, PI/4)))

        point_1_1 = np.array([-2, -1, 0])
        point_1_2 = np.array([-1, -3, 0])
        point_1_3 = np.array([1, -2, 0])
        def point_trans(point: np.ndarray):
            return 2/(point[1]-2)*np.array([-point[0], 0, point[1]])
        point_2_1 = point_trans(point_1_1)
        point_2_2 = point_trans(point_1_2)
        point_2_3 = point_trans(point_1_3)
        triangle_1 = Polygon(point_1_1, point_1_2, point_1_3)
        triangle_2 = Polygon(point_2_1, point_2_2, point_2_3)
        perspective = 2*OUT + 2*UP
        intersect_1 = np.array([5, 0, 0])
        intersect_2 = np.array([-5, 0, 0])
        intersect_3 = np.array([-2.5, 0, 0])
        line_1 = DashedLine(point_1_1, perspective, color = YELLOW)
        line_2 = DashedLine(point_1_2, perspective, color = YELLOW)
        line_3 = DashedLine(point_1_3, perspective, color = YELLOW)
        line_1_1 = DashedLine(point_1_3, intersect_1)
        line_2_1 = DashedLine(point_2_3, intersect_1)
        line_1_2 = DashedLine(point_1_1, intersect_2)
        line_2_2 = DashedLine(point_2_1, intersect_2)
        line_1_3 = DashedLine(point_1_1, intersect_3)
        line_2_3 = DashedLine(point_2_1, intersect_3)
        collinear = Line(8*LEFT, 8*RIGHT, color = RED)
        self.play(ShowCreation(triangle_1), ShowCreation(triangle_2))
        self.waiting(2, 7) #再比如 对于平面上的两个三角形
        self.play(ShowCreation(line_1), ShowCreation(line_2), ShowCreation(line_3))
        self.waiting(1, 17) #如果它们的三对顶点连线共点
        self.play(*[ShowCreation(mob) for mob in [line_1_1, line_1_2, line_1_3, line_2_1, line_2_2, line_2_3]])
        self.bring_to_back(collinear).play(ShowCreation(collinear))
        self.waiting(0, 13) #那么它们的三组对边交点共线
        self.waiting(0, 16) #（空闲）
        lines = VGroup()
        line = Line(8*LEFT, 8*RIGHT, color = GREY, stroke_width = 1)
        for i in range(4):
            line_i = line.copy().shift((i+1)*DOWN)
            line_j = line.copy().shift((i+1)*OUT)
            lines.add(line_i, line_j)
        line = VMobject(color = GREY, stroke_width = 1).set_points_as_corners([4*DOWN, ORIGIN, 4*OUT])
        for i in range(17):
            line_i = line.copy().shift((i-8)*RIGHT)
            lines.add(line_i)

        surface_1 = Polygon(perspective, point_1_1, point_1_3, color = YELLOW, stroke_width = 0, fill_opacity = 0.2)
        surface_2 = Polygon(perspective, point_1_3, point_1_2, color = YELLOW, stroke_width = 0, fill_opacity = 0.2)
        surface_3 = Polygon(perspective, point_1_2, point_1_1, color = YELLOW, stroke_width = 0, fill_opacity = 0.2)
        quadternion = quaternion_mult(quad(OUT, -PI/4), quad(RIGHT, PI/3))
        self.bring_to_back(lines).play(FadeIn(lines), 
        ApplyMethod(camera.set_orientation, Rotation(quadternion), run_time = 4, rate_func = squish_rate_func(smooth, 0, 0.75)), 
        ShowCreation(surface_1, run_time = 4, rate_func = squish_rate_func(smooth, 0.5, 0.75)), 
        ShowCreation(surface_2, run_time = 4, rate_func = squish_rate_func(smooth, 0.75, 1)), 
        ShowCreation(surface_3, run_time = 4, rate_func = squish_rate_func(smooth, 0.25, 0.5)))
        self.waiting(1+3-4, 23+3) #我们将它拿到空间中 三对共线的顶点就会组成一个三棱锥
        indicate = collinear.copy().set_stroke(width = 8, color = WHITE)
        self.play(ShowPassingFlash(indicate))
        self.play(ShowPassingFlash(indicate))
        self.waiting(1, 0) #而两个不共面的三角形会交于一条线
        surface_1_1 = Polygon(point_1_3, point_2_3, intersect_1, color = YELLOW, stroke_width = 0, fill_opacity = 0.2)
        surface_2_1 = Polygon(point_1_1, point_2_1, intersect_2, color = YELLOW, stroke_width = 0, fill_opacity = 0.2)
        surface_3_1 = Polygon(point_1_1, point_2_1, intersect_3, color = YELLOW, stroke_width = 0, fill_opacity = 0.2)
        self.waiting(1, 14) #三组对边的交点
        self.play(ShowCreation(surface_3_1))
        self.play(ShowCreation(surface_1_1))
        self.play(ShowCreation(surface_2_1))
        self.waiting(0, 13) #就分别是这个三棱锥的三个面与这条线的交点

        self.waiting(3, 17)
        self.play(FadeIn(shade))
        self.waiting(3, 0) #
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#########################################################################

class Summary_1(Scene):

    def construct(self):
        notice1 = Notice("良心视频", "请　三连")

        self.play(Write(notice1))
        self.waiting(1, 14) #非常感谢大家能看到这里
        
        back = Rectangle(height = 2.1, width = 2*16/9+0.1, color = BACK, fill_opacity = 1, stroke_width = 0)
        cover_1 = ImageMobject("my_cover_6.png", height = 2).shift(1.5*UP)
        cover_2 = ImageMobject("my_cover_5.png", height = 2)
        cover_3 = ImageMobject("my_cover_4.png", height = 2)
        cover_4 = ImageMobject("my_cover_3.png", height = 2)
        group_2 = Group(back.copy(), cover_2).shift(0.5*UP + 1.3*LEFT)
        group_3 = Group(back.copy(), cover_3).shift(0.5*DOWN + 1.3*RIGHT)
        group_4 = Group(back.copy(), cover_4).shift(1.5*DOWN + 3.9*RIGHT)

        self.play(FadeIn(cover_1, 0.5*UP))
        self.waiting(2, 21) #这期视频的内容其实很早就出现在了我的计划单上
        anims = [ApplyMethod(cover_1.shift, 3.9*LEFT), 
        FadeIn(group_2, 2.9*LEFT), 
        FadeIn(group_3, 1.9*LEFT), 
        FadeIn(group_4, 0.9*LEFT)]
        self.add(group_2, group_3, group_4).play(LaggedStart(*anims, lag_ratio = 0.2, group = Group()), run_time = 2)
        self.waiting(1, 5) #但在这之前还有三个我也想做的话题
        self.waiting(0, 24) 
        self.play(*[FadeOut(mob) for mob in [cover_1, group_2, group_3, group_4]]) #所以就只能按顺序来了
        self.waiting(0, 16) #（空闲）

        offset = 1*UP + 8/3*LEFT
        back_1 = Rectangle(height = 4+0.2, width = 4*16/9+0.2, fill_color = BACK, fill_opacity = 1).shift(0.3*UP)
        back_2 = back_1.copy()
        back_3 = back_1.copy()
        bv_1 = Text("BV1S34y1Y7Tb", font = "Times New Roman").scale(0.4).next_to(back_1.get_corner(UR), UL, buff = 0.1)
        bv_2 = Text("BV1JU4y1X7WP", font = "Times New Roman").scale(0.5).next_to(back_2.get_corner(UR), UL, buff = 0.1)
        bv_3 = Text("BV1hB4y1a7P8", font = "Times New Roman").scale(0.5).next_to(back_3.get_corner(UR), UL, buff = 0.1).shift(-offset)
        self.play(ShowCreation(back_1), Write(bv_1))
        self.waiting(1, 21) #原视频在结尾处升华了一下主题
        self.bring_to_back(bv_3, bv_2, bv_1, back_3, back_2).play(back_1.animate.shift(offset), bv_1.animate.shift(offset), back_3.animate.shift(-offset), FadeIn(bv_2), FadeIn(bv_3, -offset))
        self.waiting(1, 15) #这也引起了很多其它视频的效仿


        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Summary_2(Scene):

    def construct(self):
        notice1 = Notice("良心视频", "请　三连")

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
        self.add(notice1).play(FadeInFromPoint(like1, 3*LEFT), FadeInFromPoint(coin1, np.array([0,0,0])), FadeInFromPoint(star1, 3*RIGHT))
        self.play(ApplyMethod(sanlian1.set_color, "#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian1])
        
        self.waiting(1+2-2, 21+2) #大家看了这期视频 如果能觉得有所收获的话
        self.waiting(2, 5) #不如一键三连支持一下
        self.waiting(0, 18) #（空闲）


        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Summary_3(Scene):
    def construct(self):

        notice1 = Notice("良心视频", "请　三连")
        notice2 = Notice("下期预告", "敬请期待")

        self.play(ReplacementTransform(notice1, notice2))
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Summary_3_1(Scene):
    def construct(self):
        notice2 = Notice("下期预告", "敬请期待")
        
        left_side = ImageMobject("left_side.png", height = 8)
        right_side = ImageMobject("right_side.png", height = 8).shift(128/9*RIGHT)
        self.add(left_side, right_side, notice2).play(left_side.animate.shift(128/9*LEFT), right_side.animate.shift(128/9*LEFT), run_time = 4)
        self.waiting(2+2-4, 28+16) #但这两次转折都是有背后的原理的 它们很巧妙 但它们也很自然

        print(self.num_plays, self.time + 82 + 26/30)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Summary_4(Scene):
    def construct(self):
        notice2 = Notice("下期预告", "敬请期待")
        notice3 = Notice("良心up主", "请　关注")

        like = Text("", font = 'vanfont')
        coin = Text("", font = 'vanfont')
        star = Text("", font = 'vanfont')
        share = Text("", font = 'vanfont')

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
        # self.waiting(0, 0) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, 0.5*UP), FadeIn(text_name, 0.5*UP))
        self.waiting(1+2-3, 23+9) #而我 就像我的名字一样

        self.play(FadeOut(painting_others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star0.shift, DOWN))
        self.waiting(1, 4) #想要把天上的星星垂下来

        star_copy = star0.copy()
        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star0, apple))
        self.waiting(0, 26) #变成触手可及的果实

        snowflake = SnowFlake()
        snowflake_2 = snowflake.copy().set_color(RED).set_stroke(width = 1.5)
        snowflake_3 = snowflake.copy().set_color(BLUE).set_stroke(width = 2)
        anims = LaggedStart(SpreadOut(snowflake_2).update_config(rate_func = linear), SpreadOut(snowflake_3).update_config(rate_func = linear), SpreadOut(snowflake).update_config(rate_func = linear), rate_func = rush_into, run_time = 2)
        self.play(Transform(star0, star_copy), anims)
        self.remove(snowflake_2, snowflake_3)
        self.waiting(1+0-2, 29+14) #变成指引前路的火光 （空闲）
        
        self.remove(star0, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(2, 6) #我是乐正垂星 我们下期视频再见

        self.waiting(6, 13)
        self.play(FadeOut(picture_photo), FadeOut(text_name), FadeOut(notice3))
        self.waiting(6) #到此共110秒

        print(self.num_plays, self.time + 82 + 26/30)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)


#########################################################################


class Template(Scene):
    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)
