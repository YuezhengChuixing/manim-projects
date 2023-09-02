from __future__ import annotations

from manimlib import *
from manimlib.once_useful_constructs.fractals import *
import numpy as np

#################################################################### 

class MySierpinski(VGroup):
    def __init__(self, iters: int = 1, **kwargs):
        points = [unit(PI/2), unit(PI*7/6), unit(PI/6)/2]
        triangles = [Triangle()]
        if iters <= 0:
            super().__init__(*triangles)
        else:
            for _ in range(iters):
                triangles_0 = [triangle.copy().scale(np.array([-1/2, 1/2, 0]), about_point = points[0], min_scale_factor = -1) for triangle in triangles]
                triangles_1 = [triangle.copy().scale(1/2, about_point = points[1], min_scale_factor = -1) for triangle in triangles]
                triangles_2 = [triangle.copy().rotate(TAU/3, about_point = points[2]) for triangle in triangles_0]
                triangles = triangles_0 + triangles_1 + triangles_2
            super().__init__(*triangles, **kwargs)
        self.childs = [VGroup(*triangles_0), VGroup(*triangles_1), VGroup(*triangles_2)]

#################################################################### 

class Trailer(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8, 8)}, 
            }
    }
    def construct(self):
        self.camera.anti_alias_width = 0
        rectangle_0 = Rectangle(height = 1.5, width = 6, color = BLUE, stroke_width = 0, fill_opacity = 1).shift(1.5*UP)
        self.add(rectangle_0)
        corner_left = 2*DOWN + 3*LEFT
        corner_right = 2*DOWN + 3*RIGHT
        centers_1 = [corner_left, corner_right]
        rectangles_1 = [rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[0]).set_color(interpolate_color(GREEN, BLUE, 0.5)), rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[1]).set_color(interpolate_color(BLUE, GREEN, 0.5))]
        self.play(TransformFromCopy(rectangle_0, rectangles_1[0]), TransformFromCopy(rectangle_0, rectangles_1[1]))
        last_centers = centers_1
        last_rectangles = rectangles_1
        for i in range(2, 10):
            centers = [*(last_centers-corner_left)/3+corner_left, *(last_centers-corner_right)/3+corner_right]
            rectangles = [last_rectangles[j//2].copy().scale(np.array([1/3, 1/2, 0]), about_point = centers[j]).set_color(interpolate_color(GREEN, BLUE, 1/2**i)) for j in range(2**i)]
            self.add(*rectangles)
            last_centers = centers
            last_rectangles = rectangles

class Cover(CoverScene):
    def construct(self):
        self.camera.anti_alias_width = 0
        points_cross = np.array([UP, 3*UP + 2*RIGHT, 2*UP + 3*RIGHT, RIGHT, 2*DOWN + 3*RIGHT, 3*DOWN + 2*RIGHT, DOWN, 3*DOWN + 2*LEFT, 2*DOWN + 3*LEFT, LEFT, 2*UP + 3*LEFT, 3*UP + 2*LEFT])
        cross = Polygon(*points_cross, fill_color = RED, fill_opacity = 0.5, stroke_width = 0).shift(10/3*LEFT)
        points_check = np.array([2.5*DOWN + LEFT, 0.5*DOWN + 3*LEFT, 0.5*UP + 2*LEFT, 0.5*DOWN + LEFT, 2.5*UP + 2*RIGHT, 1.5*UP + 3*RIGHT])
        checkmark = Polygon(*points_check, fill_color = GREEN, fill_opacity = 0.5, stroke_width = 0).shift(10/3*RIGHT)
        line = Line(4*UP, 4*DOWN)
        self.add(cross, checkmark, line)

        sier = MySierpinski(iters = 6).set_color_by_gradient(TEAL, WHITE).set_style(stroke_color = BLACK, stroke_background = True, fill_opacity = 1).shift(0.5*UP + 10/3*LEFT).scale(2.5, about_point = 10/3*LEFT)
        koch = KochCurve(radius = 5, order = 5, colors = [BLUE, WHITE]).set_stroke(width = 1.5).shift(2*DOWN + 10/3*LEFT)
        koch_stroke = KochCurve(radius = 5, order = 5, colors = [BLACK]).set_stroke(width = 3).shift(2*DOWN + 10/3*LEFT)
        questionmark = Text(r"？", font = "FZDaHei-B02S", color = YELLOW).make_smooth().make_smooth().make_smooth().set_stroke(background = True, color = BLACK, width = 8).set_height(5).shift(10/3*RIGHT + 0.25*UP)
        self.add(sier, koch_stroke, koch, questionmark)

#################################################################### 

class Video(FrameScene):
    def construct(self):
        rectangle_0 = Rectangle(height = 1.5, width = 8, color = BLUE, stroke_width = 0, fill_opacity = 1).shift(1.5*UP)
        anim_rectangle_0 = rectangle_0.copy()
        corner_left = 2*DOWN + 4*LEFT
        corner_right = 2*DOWN + 4*RIGHT
        centers_1 = [corner_left, corner_right]
        rectangles_1 = [rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[0]).set_color(interpolate_color(GREEN, BLUE, 0.5)), rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[1]).set_color(interpolate_color(BLUE, GREEN, 0.5))]
        anim_rectangles_1 = [rect.copy() for rect in rectangles_1]
        anims = [FadeIn(anim_rectangle_0, 3*DOWN, rate_func = linear, run_time = 0.25), AnimationGroup(TransformFromCopy(rectangle_0.set_color(BACK), anim_rectangles_1[0], rate_func = linear), TransformFromCopy(rectangle_0.set_color(BACK), anim_rectangles_1[1], rate_func = linear), rate_func = linear, run_time = 0.25, group = VGroup())]
        self.bring_to_back(*anim_rectangles_1, anim_rectangle_0)
        last_centers = centers_1
        last_rectangles = rectangles_1
        for i in range(2, 10):
            centers = [*(last_centers-corner_left)/3+corner_left, *(last_centers-corner_right)/3+corner_right]
            rectangles = [last_rectangles[j//2].copy().scale(np.array([1/3, 1/2, 0]), about_point = centers[j]).set_color(interpolate_color(GREEN, BLUE, 1/2**i)) for j in range(2**i)]
            anim_rectangles = [rect.copy() for rect in rectangles]
            anims.append(AnimationGroup(*[TransformFromCopy(last_rectangles[j//2].set_color(BACK), anim_rectangles[j], rate_func = linear) for j in range(2**i)], rate_func = linear, run_time = 1/2**i, group = VGroup()))
            self.bring_to_back(*anim_rectangles)
            last_centers = centers
            last_rectangles = rectangles
        self.play(LaggedStart(*anims, lag_ratio = 1, run_time = 2, group = VGroup()))
        self.wait(2+0-2, 17+22) #为什么说康托集是最简单的分形？ （空闲）

        title = Title("分形").shift(UP)
        title_line = TitleLine().save_state().scale(0, about_point = 4*UP)
        self.play(title.animate.shift(DOWN), title_line.animate.restore())
        self.wait(2+0-2, 24+18)
        self.add(self.shade, title, title_line).play(FadeIn(self.shade))
        self.clear().add(title, title_line) #想搞懂这个问题 就要知道分形是什么 （空闲）

        circle = Circle(radius = 1.5, color = YELLOW).shift(2*LEFT)
        focus = Square(side_length = 0.3).shift(2*LEFT + 1.5*unit(TAU/3))
        back = focus.copy().set_style(stroke_width = 0, fill_opacity = 1, fill_color = BACK)
        focus_back = back.copy()
        focus_frame = focus.copy()
        line = Line(-0.15*(RIGHT + UP/np.sqrt(3)), 0.15*(RIGHT + UP/np.sqrt(3)), color = YELLOW).shift(2*LEFT + 1.5*unit(TAU/3))
        line_conn = Line(2*LEFT + 1.5*unit(TAU/3), 2*LEFT + 1.5*unit(TAU/3), stroke_width = 2)
        self.play(ShowCreation(circle))
        self.play(ShowCreation(focus))
        self.add(line_conn, back, circle, focus, focus_back, line, focus_frame).play(*[mob.animate.scale(10/3).move_to(5*LEFT + UP) for mob in [focus_back, line, focus_frame]], line_conn.animate.put_start_and_end_on(2*LEFT + 1.5*unit(TAU/3), 5*LEFT + UP))
        self.wait(1+1-3, 18+13) #我们要是画一个圆 将它放得足够大
        indicate = line.copy().set_stroke(color = WHITE, width = 8)
        self.play(ShowPassingFlash(indicate))
        self.play(ShowPassingFlash(indicate))
        self.wait(0, 14) #那这一小段就几乎变成了光滑的直线
        self.wait(0, 16) #（空闲）

        text_l = Text(r"不是分形", font = "simsun", color = YELLOW).scale(0.8).next_to(3*UP + 32/9*LEFT, DOWN)
        text_r = Text(r"是分形", font = "simsun", color = YELLOW).scale(0.8).next_to(3*UP + 32/9*RIGHT, DOWN)
        mandelbrot = Text("曼德博集", font = "simsun", color = YELLOW).scale(0.5).next_to(2*DOWN + 32/9*RIGHT, DOWN)
        self.play(Write(text_l), Write(text_r), FadeIn(mandelbrot))
        self.wait(0, 16) #但是分形不一样
        self.wait(0, 16) #（空闲）
        self.wait(2, 0) #无论我们把它放大多少倍
        self.wait(2, 11) #分形始终都有无穷多的细节
        self.wait(0, 27) #（空闲）

        title_2 = Title(r"自相似")
        self.add(self.shade, title, title_line).play(FadeIn(self.shade), title.animating(remover = True).scale(0, about_point = 3*UP), title_2.shift(UP).animate.shift(DOWN))
        self.clear().add(title_2, title_line).wait(0, 20) #想要制作一个分形
        self.wait(2, 0) #最好的方法是利用自相似
        self.wait(0, 16) #（空闲）

        sier_0 = Sierpinski(order = 0).set_color(RED)[0]
        triangle_1 = sier_0.copy().scale(0.5).shift(UP + 3*LEFT)
        triangle_2 = sier_0.copy().scale(0.5).shift(UP).set_color(interpolate_color(RED, WHITE, 0.5))
        triangle_3 = sier_0.copy().scale(0.5).shift(UP + 3*RIGHT).set_color(WHITE)
        sier_1 = Sierpinski(order = 1)
        self.play(ShowCreation(sier_0))
        self.wait(1, 27) #比如说 我们取一个正三角形
        self.remove(sier_0).add(triangle_2, triangle_1, triangle_3).play(LaggedStart(TransformFromCopy(sier_0, triangle_3), TransformFromCopy(sier_0, triangle_1), TransformFromCopy(sier_0, triangle_2), lag_ratio = 0.5, run_time = 2, group = VGroup()))
        self.play(ReplacementTransform(triangle_1, sier_1[0]), ReplacementTransform(triangle_2, sier_1[1]), ReplacementTransform(triangle_3, sier_1[2]))
        sier_2 = Sierpinski(order = 2)
        self.play(FadeTransform(sier_1, sier_2))
        sier_3 = Sierpinski(order = 3)
        self.play(FadeTransform(sier_2, sier_3))
        sier_4 = Sierpinski(order = 4)
        self.play(FadeTransform(sier_3, sier_4))
        sier_5 = Sierpinski(order = 5)
        self.play(FadeTransform(sier_4, sier_5))
        sier_8 = Sierpinski(order = 8, stroke_width = 0)
        copy_sier_8 = sier_8.copy()
        self.play(FadeTransform(sier_5, sier_8))
        self.wait(2+0+1+2+1+0-7, 2+19+14+9+18+20) #将它复制三份 拼起来 （空闲） 重复这个过程 就会得到一个很著名的分形 谢尔宾斯基三角形 （空闲）

        self.play(FadeTransform(sier_8[1], copy_sier_8), sier_8[0].animating(remover = True).scale(2, about_point = 2*UP).set_opacity(0), sier_8[2].animating(remover = True).scale(2, about_point = 2*UP).set_opacity(0), run_time = 2)

class Video_2(FrameScene):
    def construct(self):
        self.frames += 42*30+22
        
        title = Title(r"自相似")
        title_line = TitleLine()
        self.add(title, title_line).wait(1)
        koch_0 = KochCurve(order = 0, radius = 8, num_submobjects = 101).shift(DOWN)
        koch_1 = KochCurve(order = 1, radius = 8, num_submobjects = 401).next_to(1.5*DOWN, UP, buff = 0)
        self.play(ShowCreation(koch_0))
        self.wait(0, 13) #另一个很出名的分形是科赫雪花
        self.wait(0, 16) #（空闲）

        lines = [koch_0.copy().scale(1/3).move_to(3*LEFT + 1.5*DOWN), koch_0.copy().scale(1/3).move_to(2*LEFT + UP), koch_0.copy().scale(1/3).move_to(2*RIGHT + UP), koch_0.copy().scale(1/3).move_to(3*RIGHT + 1.5*DOWN)]
        self.remove(koch_0).add(*lines).play(LaggedStart(*[TransformFromCopy(koch_0, line) for line in lines], lag_ratio = 0.5, run_time = 2, group = VGroup()))
        self.wait(0, 6) #我们把一条线段复制四份
        self.play(*[ReplacementTransform(lines[i], koch_1[100*i:100*(i+1)]) for i in range(4)])
        self.wait(0, 15) #然后拼起来
        self.remove(koch_1)
        koch_1 = KochCurve(order = 1, radius = 8, num_submobjects = 256).next_to(1.5*DOWN, UP, buff = 0)
        koch_2 = KochCurve(order = 2, radius = 8, num_submobjects = 256).next_to(1.5*DOWN, UP, buff = 0)
        self.play(ReplacementTransform(koch_1, koch_2))
        koch_3 = KochCurve(order = 3, radius = 8, num_submobjects = 256).next_to(1.5*DOWN, UP, buff = 0)
        self.play(ReplacementTransform(koch_2, koch_3))
        koch_4 = KochCurve(order = 4, radius = 8, num_submobjects = 256).next_to(1.5*DOWN, UP, buff = 0)
        self.play(ReplacementTransform(koch_3, koch_4))
        koch_6 = KochCurve(order = 6, radius = 8, num_submobjects = 256).next_to(1.5*DOWN, UP, buff = 0)
        self.play(ReplacementTransform(koch_4, koch_6))
        self.wait(1+1+0-4, 20+27+21) #这么不断重复下去 最后就能得到这样一条曲线 （空闲）

class Video_3(FrameScene):
    def construct(self):
        self.frames += 53*30+20
        title = Title(r"自相似")
        title_line = TitleLine()
        koch_0 = KochCurve(order = 6, radius = 8).next_to(1.5*DOWN, UP, buff = 0)
        koch_1 = KochCurve(order = 6, radius = 8).next_to(1.5*DOWN, UP, buff = 0)
        koch_2 = KochCurve(order = 6, radius = 8).next_to(1.5*DOWN, UP, buff = 0).save_state()
        self.add(title, title_line, koch_0, koch_1, koch_2).wait(1, 12) #不过严格来说
        self.wait(2, 10) #它现在还不是一片雪花
        alpha = ValueTracker(0)
        def left_updater(mob: VMobject):
            value = alpha.get_value()
            if value <= 0.75:
                offset = smooth(1.25*value)*1.1*(2/np.sqrt(3)*unit(PI*7/6) - 1.5*DOWN)
            else:
                offset = 1.1*(2/np.sqrt(3)*unit(PI*7/6) - 1.5*DOWN) - smooth(4*value-3)*0.1*(2/np.sqrt(3)*unit(PI*7/6) - 1.5*DOWN)
            mob.restore().scale(interpolate(1, 0.5, smooth(value)), about_point = 1.5*DOWN).rotate(smooth(value)*TAU/3, about_point = 1.5*DOWN).shift(offset)
        def right_updater(mob: VMobject):
            value = alpha.get_value()
            if value <= 0.75:
                offset = smooth(1.25*value)*1.1*(2/np.sqrt(3)*unit(-PI/6) - 1.5*DOWN)
            else:
                offset = 1.1*(2/np.sqrt(3)*unit(-PI/6) - 1.5*DOWN) - smooth(4*value-3)*0.1*(2/np.sqrt(3)*unit(-PI/6) - 1.5*DOWN)
            mob.restore().scale(interpolate(1, 0.5, smooth(value)), about_point = 1.5*DOWN).rotate(-smooth(value)*TAU/3, about_point = 1.5*DOWN).shift(offset)
        def up_updater(mob: VMobject):
            value = alpha.get_value()
            if value <= 0.75:
                offset = smooth(1.25*value)*1.1*(1.5*UP + 2/np.sqrt(3)*UP)
            else:
                offset = 1.1*(1.5*UP + 2/np.sqrt(3)*UP) - smooth(4*value-3)*0.1*(1.5*UP + 2/np.sqrt(3)*UP)
            mob.restore().scale(interpolate(1, 0.5, value), about_point = 1.5*DOWN).shift(offset)
        koch_0.save_state().add_updater(up_updater)
        koch_1.save_state().add_updater(left_updater)
        koch_2.save_state().add_updater(right_updater)
        self.play(alpha.animating(run_time = 2, rate_func = linear).set_value(1))
        self.wait(0, 24) #我们把它再复制两份 拼到一起
        koch = KochSnowFlake(order = 6, colors = [BLUE_D, WHITE, BLUE_D, WHITE, BLUE_D, WHITE, BLUE_D])
        self.add(koch).remove(koch_0, koch_1, koch_2)
        self.wait(1, 9) #就能得到雪花了
        self.wait(1, 1) #（空闲）

        sier = Sierpinski(order = 7).shift(3*LEFT)
        self.play(koch.animate.shift(3*RIGHT), FadeIn(sier, 4*RIGHT), run_time = 2)
        self.wait(0, 4) #但无论是谢尔宾斯基三角形
        self.wait(1, 13) #还是科赫雪花
        self.wait(1, 28) #都称不上是最简单的分形
        self.wait(0, 21) #（空闲）

        surr_1 = Square(color = YELLOW, side_length = 5).shift(3*LEFT)
        surr_2 = Square(color = YELLOW, side_length = 5).shift(3*RIGHT)
        line = Line(3*LEFT, 3*RIGHT, color = GREEN)
        self.play(ShowCreation(surr_1), ShowCreation(surr_2))
        self.wait(0, 24) #它们都是平面图形
        title_3 = Title("康托集")
        self.play(FadeOut(surr_1, 1.5*LEFT, rate_func = rush_into), FadeOut(sier, 1.5*LEFT, rate_func = rush_into), 
                  FadeOut(surr_2, 1.5*RIGHT, rate_func = rush_into), FadeOut(koch, 1.5*RIGHT, rate_func = rush_into), 
                  GrowFromCenter(line, run_time = 2), title.animating(remover = True).scale(0, about_point = 3*UP), title_3.shift(UP).animate.shift(DOWN))
        self.camera.anti_alias_width = 0
        self.wait(0, 17) #而康托集在一条线段上就能摆得下
        self.wait(0, 22) #（空闲）
        self.wait(0, 27) #并且......

        line_1 = line.copy().set_stroke(width = 6)
        line_2 = line.copy().set_stroke(width = 6)
        self.remove(line).add(line_1, line_2).play(LaggedStart(line_1.animate.scale(4/9).shift(8/3*LEFT + UP), line_2.animate.scale(4/9).shift(8/3*RIGHT + UP), lag_ratio = 0.5, run_time = 1.5))
        self.wait(1, 2) #康托集每次迭代只用复制两份
        self.wait(0, 22) #（空闲）
        
        self.play(line_1.animate.shift(DOWN), line_2.animate.shift(DOWN))
        self.wait(1, 26) #把这两条线段摆在左右三分之一的地方
        old_lines = [line_1, line_2]
        old_group = VGroup(line_1, line_2)
        for i in range(1, 6):
            lines = [line.copy().scale(1/3, about_point = 4*LEFT) for line in old_lines] + [line.copy().scale(1/3, about_point = 4*RIGHT) for line in old_lines]
            group_lines = VGroup(*lines).set_stroke(width = 4+2*i)
            self.play(FadeTransform(old_group, group_lines))
            old_lines = lines
            old_group = group_lines
        self.wait(2+1+0-5, 24+23+25) #然后对每条线段都重复这个操作 最终就能得到康托集了 （空闲）

        indicate = VMobject(stroke_width = 30, color = YELLOW).set_points(group_lines.get_all_points())
        self.play(ShowPassingFlash(indicate, run_time = 4, lag_ratio = 1), rate_func = linear)
        self.wait(2+1-4, 16+21) #它不像之前的那两个例子那么好看 我们甚至不太能看得见它
        self.wait(0, 20) #（空闲）

        koch = KochCurve(order = 6, radius = 8).set_stroke(width = 2).next_to(0.5*DOWN, UP, buff = 0)
        self.play(FadeIn(koch, 0.7*DOWN), group_lines.animate.shift(0.7*DOWN))
        self.wait(1, 1) #但它却藏身在科赫雪花之中
        self.wait(0, 21) #（空闲）

        line = Line(4.5*LEFT, 4.5*RIGHT, color = YELLOW_E).shift(0.5*DOWN)
        self.bring_to_back(line).play(ShowCreation(line))
        self.wait(1, 7) #科赫雪花最底端的这一条线
        indicate_2 = group_lines.copy().set_stroke(width = 40, color = YELLOW)
        self.play(ShowIncreasingSubsets(indicate_2, rate_func = linear, run_time = 2))
        self.remove(group_lines, indicate_2).add(indicate.shift(0.7*DOWN).set_stroke(width = 40)).wait(1+0-2, 9+27) #就是一个康托集 （空闲）

        self.wait(2, 27) #既然不好看 那要康托集有什么用呢
        self.wait(0, 15) #（空闲）
        self.wait(1, 1) #用途还真不小
        self.wait(0, 18) #（空闲）

        contor = LabelPicture("Cantor.jpg", "格奥尔格·康托（1845.3.3 - 1918.1.6）", text_config = {r"font": "simhei"}).shift(4*LEFT)
        self.play(FadeIn(contor, 3*RIGHT), *[mob.animate.shift(2.25*RIGHT) for mob in [koch, line, indicate]])
        self.wait(1, 23) #康托是19世纪的一位伟大的数学家
        self.wait(1, 19) #集合论就是他创立的
        self.wait(0, 16) #（空闲）
        self.play(FadeOut(koch, 0.5*UP), line.animate.scale(8/9).shift(0.5*UP), indicate.animate.set_color(GREEN))
        self.wait(1, 25) #他发现 康托集虽然简单
        self.wait(3, 2) #但能很好地帮助我们理解实数和无穷是什么
        self.wait(0, 26) #（空闲）

        arrow_up = Arrow(line.get_start() + UP, line.get_start(), color = YELLOW, buff = 0.2).shift(0.1*UP)
        arrow_down = Arrow(line.get_start() + DOWN, line.get_start(), color = YELLOW, buff = 0.2).shift(1*DOWN)
        self.play(FadeIn(arrow_up, 0.3*DOWN), FadeIn(arrow_down, 0.3*UP))
        self.wait(2, 1) #比如说 康托集虽然长度是0
        alpha = ValueTracker(0.0)
        def arrow_updater(mob: Arrow):
            value = alpha.get_value()
            mob.set_x(indicate.quick_point_from_proportion(value)[0])
        arrow_down.add_updater(arrow_updater)
        self.play(arrow_up.animate.shift(8*RIGHT), alpha.animate.set_value(1), run_time = 4, rate_func = there_and_back)
        arrow_down.clear_updaters()
        self.wait(1+2-4, 19+26) #但它里面的所有点 和一条线段里面的所有点是一样多的
        self.wait(0, 22) #（空闲）

        self.play(FadeOut(arrow_up), FadeOut(arrow_down))
        self.wait(1, 13) #康托集还有很多很神奇的性质
        self.wait(2, 0) #如果你对这个话题感兴趣
        self.wait(1, 14) #可以看我的下一期视频
        self.wait(0, 18)

        self.camera.anti_alias_width = 1.5
        alpha = ValueTracker(0.0)
        def photo_updater(mob: ImageMobject):
            value = alpha.get_value()
            mob.restore().scale(value).rotate(PI*(1-value))
        picture_photo = ImageMobject("picture_photo.png", height = 2).save_state().add_updater(photo_updater)
        text_name = Text("乐正垂星", font = "simhei")
        shade = BackgroundRectangle(text_name, color = BACK, fill_opacity = 1)
        self.clear().add(picture_photo).play(alpha.animate.set_value(1.0))
        picture_photo.clear_updaters()
        shade.next_to(picture_photo.get_edge_center(RIGHT), LEFT, buff = 0)
        text_name.move_to(shade)
        self.add(text_name, shade, picture_photo).play(picture_photo.animate.shift(1.5*LEFT), shade.animate.shift(1.5*LEFT), text_name.animate.shift(1.2*RIGHT))
        self.wait(2, 1) #我是乐正垂星 把远在天边的知识送到你的面前
        self.wait(2, 24) #关注我 带你深入地理解这个世界
        self.wait(1, 9) #到此共138秒

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]