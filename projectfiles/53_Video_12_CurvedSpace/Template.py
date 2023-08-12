from __future__ import annotations

from manimlib import *
import numpy as np

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

#################################################################### 

class Intro0(FrameScene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("亲眼看一看肯定有助于理解，\n但弯曲的空间是什么样，\n和它看上去什么样没多大关系。", font = 'simsun', t2c={"是": GREEN, "看上去": BLUE, ("看一看", "没多大关系"): YELLOW})
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DR), DL)
        ##  Showing object
        self.play(Write(quote), runtime = 2)
        self.play(Write(author), Write(notice0))
        self.wait(2)
        self.play(FadeOut(quote), FadeOut(author))
        self.wait(1)


class Intro_Patch1(Scene):
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        camera.shift(2*OUT+DOWN).set_orientation(Rotation(quadternion))
        # plane = Square(side_length = 8, fill_opacity = 1, stroke_width = 0, color = BLUE, reflectiveness = 0, gloss = 0.3, shadow = 0.6).rotate(PI/6)
        plane = Surface(u_range = (-4, 4), v_range = (-4, 4), color = BLUE).rotate(PI/6)
        self.play(Rotating(plane, angle = PI/2, run_time = 30))

class Intro_Patch2(Scene):
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        camera.shift(OUT+DOWN).set_orientation(Rotation(quadternion))
        # plane = Square(side_length = 8, fill_opacity = 1, stroke_width = 0, color = BLUE, reflectiveness = 0, gloss = 0.3, shadow = 0.6).rotate(PI/6)
        sphere = Sphere(radius = 3, color = BLUE).rotate(PI/6)
        sphere.add(SurfaceMesh(sphere, stroke_color = BLUE_A, stroke_width = 1))
        self.play(Rotating(sphere, angle = PI/2, run_time = 30))

class Intro_Patch3(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 16.0)}, 
            }
    }
    def construct(self):
        camera = self.camera.frame
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        camera.shift(6*OUT).set_orientation(Rotation(quadternion))
        paraboloid = ParametricSurface(lambda u, v: np.array(u*unit(v) + u**2*OUT), u_range = (0, 2), v_range = (0, TAU), color = BLUE).rotate(PI/6)
        z_axis = Arrow(DOWN, 5*UP, buff = 0, depth_test = True).rotate(PI/2, about_point = ORIGIN, axis = RIGHT)
        axes = VGroup(Arrow(2.5*DOWN, 2.5*UP, buff = 0), Arrow(2.5*LEFT, 2.5*RIGHT, buff = 0), depth_test = True)
        self.add(axes, z_axis, paraboloid).play(Rotating(paraboloid, angle = PI/2, run_time = 30), Rotating(axes, angle = PI/2, run_time = 30))

class Intro1(FrameScene):
    def construct(self):
        self.notices = [FixedNotice("沃茨基·硕德", "请勿模仿"), 
                        FixedNotice("视频前言", "请听介绍"),
                        FixedNotice("高维球面", "请　脑补"),
                        FixedNotice("常见科普", "请　熟知"),
                        FixedNotice("深入科普", "请　跳过"),
                        FixedNotice("视频前言", "请听介绍"),
                        FixedNotice("传统艺能", "请　三连")]
        self.notice = self.notices[0]
        
        self.play(self.change_notice())
        self.wait(1, 16) #相信大家都对弯曲的空间不算陌生
        self.wait(0, 18) #（空闲）

        self.wait(2, 5) #相比于平面这种平直空间
        self.wait(3, 2) #像是球面 或者一个二维函数的图像
        self.wait(2, 22) #我们用肉眼就能看出它们确实是弯曲的
        self.wait(0, 20) #（空闲）

        camera = self.camera.frame
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        camera.shift(0.3*OUT).set_orientation(Rotation(quadternion))
        mesh = SurfaceMesh(Sphere(radius = 2.5), stroke_width = 2).rotate(PI/6)
        meshes_left = VGroup(*[mesh.copy().scale((i+1)/5).set_stroke(opacity = (i+1)/5, color = ratio_color((i+1)/10), width = 2*np.sqrt((i+1)/5)) for i in range(5)]).shift(3*LEFT)
        meshes_right = VGroup(*[mesh.copy().scale((i+1)/5).set_stroke(opacity = (i+1)/5, color = ratio_color((9-i)/10), width = 2*np.sqrt((i+1)/5)) for i in range(5)]).shift(3*RIGHT)
        notice = FixedText(r"总共表示一个“三维球面”，即“四维球的表面”", font = "simsun").set_color(YELLOW).scale(0.7).shift(3.5*UP)
        arrow_1 = Arrow(notice, 2.2*UP, is_fixed_in_frame = True, color = YELLOW).shift(3*LEFT)
        arrow_2 = Arrow(notice, 2.2*UP, is_fixed_in_frame = True, color = YELLOW).shift(3*RIGHT)
        notice.add(arrow_1, arrow_2)
        def rotate_updater(mob: Mobject, dt):
            mob.rotate(0.1*dt)
        meshes_left.add_updater(rotate_updater)
        meshes_right.add_updater(rotate_updater)
        self.fade_in(meshes_left, meshes_right, notice, change_notice = True, rate_func = squish_rate_func(smooth, 0.5, 1))
        self.wait(1, 19) #但是这就已经是肉眼的极限了
        self.wait(2, 16) #维度再高 连想象都会变得很困难
        self.wait(0, 18) #（空闲）

        self.clear().add(self.notice)
        camera.set_orientation(Rotation.identity())
        rectangle_video = Rectangle(height = 6, width = 5.5*16/9 + 0.5)
        self.play(ShowCreation(rectangle_video), self.change_notice())
        self.wait(2, 16) #所以 我们见到的关于广义相对论的科普
        self.wait(2, 13) #大多都只是讲了低维类比
        self.play(self.change_notice())
        self.wait(1, 10) #更深入的科普也不能说没有
        self.wait(3, 4) #但它们上来就会引入一大堆数学概念
        self.wait(2, 6) #直观图像就基本被抛弃掉了
        self.clear().wait(0, 26) #（空闲）
        
        self.wait(4, 5) #确实 这么做能精确地规定出弯曲空间的样子
        
        ratio = 0.2
        lines_l = [Line(LEFT_SIDE + 3*DOWN + i*ratio*UP, RIGHT_SIDE + 3*UP + i*ratio*UP, stroke_width = 1 if i%4 else 2).insert_n_curves(79) for i in range(-40, 40)]
        lines_r = [Line(LEFT_SIDE + 3*UP + i*ratio*UP, RIGHT_SIDE + 3*DOWN + i*ratio*UP, stroke_width = 1 if i%4 else 2).insert_n_curves(79) for i in range(-40, 40)]
        lines = VGroup(*lines_l, *lines_r).save_state()
        def skew_norm(x: np.ndarray):
            return x[0]**2 + x[1]**2*64/27
        def normal(mu: np.ndarray, sigma: float):
            def util(position: np.ndarray):
                return np.exp(-skew_norm(position-mu)**2/(2*sigma**2))*0.3*DOWN
            return util
        numbers = 16
        mus = (np.random.rand(numbers, 3)-np.array([0.5, 0.5, 0.5]))*np.array([FRAME_WIDTH, FRAME_HEIGHT, 6])
        sigmas = np.random.rand(numbers)*2
        normals = [normal(mus[i], sigmas[i]) for i in range(numbers)]
        now_time = self.get_time()
        vectors = (np.random.rand(numbers, 3)-np.array([0.5, 0.5, 0.5]))*np.array([FRAME_WIDTH, FRAME_HEIGHT, 0])
        nudges = np.random.rand(numbers)
        def lines_updater(mob: VMobject):
            t = (self.get_time() - now_time)/10
            phases = [(nudge + t)%1 - 0.5 for nudge in nudges]
            def util(position: np.ndarray):
                result = position
                for i in range(numbers):
                    result += np.cos(phases[i]*PI)**2*normals[i](position - phases[i]*vectors[i])
                return result
            mob.restore().apply_function(util)
        lines.add_updater(lines_updater)
        
        self.add(lines).play(self.change_notice())
        self.wait(1, 3) #但直观也不用放弃得这么彻底
        self.wait(0, 18) #（空闲）
        self.wait(2, 5) #我们仍然能在高维的弯曲空间中
        self.wait(1, 28) #找到一些合适的几何图像
        self.wait(1, 9) #来辅助我们理解
        self.wait(0, 24) #（空闲）

        like = Text("", font = 'vanfont').shift(3*LEFT).scale(2)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT).scale(2)
        sanlian = VGroup(like, coin, star)

        self.clear().add(self.notices[0]).play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, ORIGIN), FadeInFromPoint(star, 3*RIGHT), self.change_notice())
        self.play(Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), sanlian.animate.set_color("#00A1D6"))
        self.wait(1, 29) #长按点赞一键三连 我们开始吧
        self.wait(1, 28)
        self.fade_out(end = True)
        self.wait(2, 0) #到此共54秒
        
class Intro_Patch4(FrameScene):
    def construct(self):
        notice_1 = Notice("常见科普", "请　熟知").set_stroke(width = 0)
        notice_2 = Notice("深入科普", "请　跳过").set_stroke(width = 0)
        notice_3 = Notice("视频前言", "请听介绍").set_stroke(width = 0)

        self.add(notice_1)
        ends = [1.5*UP + 3.5*LEFT, 3.5*LEFT, 1.5*DOWN + 3.5*LEFT, 1.5*UP + 3.5*RIGHT, 3.5*RIGHT, 1.5*DOWN + 3.5*RIGHT]
        formula_1 = MTex(r"\mathrm{d}s^2=g_{\alpha\beta}\mathrm{d}x^\alpha\mathrm{d}x^\beta").next_to(7.5*RIGHT + 1.5*UP)
        formula_2 = MTex(r"\Gamma^i_{jk}=\frac{1}{2}g^{i\alpha}\left(\frac{\partial g_{\alpha j}}{\partial x^k} + \frac{\partial g_{\alpha k}}{\partial x^j}-\frac{\partial g_{jk}}{\partial x^\alpha}\right)").scale(0.8).next_to(7.5*RIGHT)
        formula_3 = MTex(r"R^i_{jkl}=\frac{\partial \Gamma^i_{jl}}{\partial x^k}-\frac{\partial \Gamma^i_{jk}}{\partial x^l}+\Gamma^\alpha_{jl}\Gamma^i_{\alpha k}-\Gamma^\alpha_{jk}\Gamma^i_{\alpha l}").scale(0.75).next_to(7.5*RIGHT + 1.5*DOWN)
        formula_4 = MTex(r"\frac{\mathrm{d}^2x^i}{\mathrm{d}t^2}+\Gamma^i_{\alpha\beta}\frac{\mathrm{d}x^\alpha}{\mathrm{d}t}\frac{\mathrm{d}x^\beta}{\mathrm{d}t}=0").scale(0.8).next_to(14.5*RIGHT + 1.5*UP)
        formula_5 = MTex(r"L=\int\sqrt{g_{\alpha\beta}\frac{\mathrm{d}x^\alpha}{\mathrm{d}t}\frac{\mathrm{d}x^\beta}{\mathrm{d}t}}\mathrm{d}t").scale(0.75).next_to(14.5*RIGHT)
        formula_6 = MTex(r"R_{\mu\nu}-\frac{1}{2}Rg_{\mu\nu}=\frac{8\pi G}{c^4}T_{\mu\nu}").scale(0.8).next_to(14.5*RIGHT + 1.5*DOWN)
        formulas = [formula_1, formula_2, formula_3, formula_4, formula_5, formula_6]
        starts = [mob.get_center().copy() for mob in formulas]
        self.add(*formulas)
        def position(index: int, step: int):
            return interpolate(starts[index], ends[index], step/6)
        def click(index: int, step: int):
            return formulas[index].animating(rate_func = rush_from).move_to(position(index, step))
        board_start = Rectangle(height = 8.4, width = 15.2, fill_opacity = 1, fill_color = BLACK, stroke_color = YELLOW_E).shift(15*RIGHT)
        inner_start = Rectangle(height = 8.2, width = 15, fill_opacity = 1, fill_color = "#222222", stroke_color = WHITE).shift(15*RIGHT)
        board_end = Rectangle(height = 8.4, width = 15.2, fill_opacity = 1, fill_color = BLACK, stroke_color = YELLOW_E)
        inner_end = Rectangle(height = 8.2, width = 15, fill_opacity = 1, fill_color = "#222222", stroke_color = WHITE)
        board = board_start.copy(deep = True)
        inner = inner_start.copy(deep = True)
        def drag(step: int):
            return board.animating(rate_func = rush_from).interpolate(board_start, board_end, step/6), inner.animating(rate_func = rush_from).interpolate(inner_start, inner_end, step/6)
        alpha = ValueTracker(0.0)
        def halve_updater(mob: Text):
            value = alpha.get_value()
            mob.restore().shift(smooth(value)*UP).set_opacity(there_and_back(value))
        halve = Text(r"观众减半", font = "simsun", color = RED_E).next_to(formulas[0], LEFT).save_state().add_updater(halve_updater)
        shade = Shade().set_opacity(0)
        
        self.add(shade, board, inner, notice_1, formulas[0], halve).play(click(0, 1), *drag(1), Transform(notice_1, notice_2), alpha.set_value(0).animating(rate_func = linear).set_value(1), shade.animate.set_opacity(1/12))
        self.wait(0, 3)
        self.add(formulas[1].move_to(position(1, 1))).play(formulas[1].save_state().shift(8*RIGHT).animate.restore(), run_time = 0.4, rate_func = linear, frames = 12)
        self.add(halve.next_to(formulas[1], LEFT).save_state()).play(click(0, 2), click(1, 2), *drag(2), alpha.set_value(0).animating(rate_func = linear).set_value(1), shade.animate.set_opacity(2/12))
        self.wait(0, 3)
        self.add(formulas[2].move_to(position(2, 2))).play(formulas[2].save_state().shift(8*RIGHT).animate.restore(), run_time = 0.4, rate_func = linear, frames = 12)
        self.add(halve.next_to(formulas[2], LEFT).save_state()).play(click(0, 3), click(1, 3), click(2, 3), *drag(3), alpha.set_value(0).animating(rate_func = linear).set_value(1), shade.animate.set_opacity(3/12))
        self.wait(0, 3)
        self.add(formulas[3].move_to(position(3, 3))).play(formulas[3].save_state().shift(8*RIGHT).animate.restore(), run_time = 0.4, rate_func = linear, frames = 12)
        self.add(halve.next_to(formulas[3], LEFT).save_state()).play(click(0, 4), click(1, 4), click(2, 4), click(3, 4), *drag(4), alpha.set_value(0).animating(rate_func = linear).set_value(1), shade.animate.set_opacity(4/12))
        self.wait(0, 3)
        self.add(formulas[4].move_to(position(4, 4))).play(formulas[4].save_state().shift(8*RIGHT).animate.restore(), run_time = 0.4, rate_func = linear, frames = 12)
        self.add(halve.next_to(formulas[4], LEFT).save_state()).play(click(0, 5), click(1, 5), click(2, 5), click(3, 5), click(4, 5), *drag(5), alpha.set_value(0).animating(rate_func = linear).set_value(1), shade.animate.set_opacity(5/12))
        self.wait(0, 3)
        self.add(formulas[5].move_to(position(5, 5))).play(formulas[5].save_state().shift(8*RIGHT).animate.restore(), run_time = 0.4, rate_func = linear, frames = 12)
        self.add(halve.next_to(formulas[5], LEFT).save_state()).play(click(0, 6), click(1, 6), click(2, 6), click(3, 6), click(4, 6), click(5, 6), *drag(6), alpha.set_value(0).animating(rate_func = linear).set_value(1), shade.animate.set_opacity(6/12))
        self.wait(2+3+2+0-8, 10+4+6+26-15) #更深入的科普也不能说没有 但它们上来就会引入一大堆数学概念 直观图像就基本被抛弃掉了 （空闲）
        self.wait(4, 5) #确实 这么做能精确地规定出弯曲空间的样子
        self.play(FadeOut(shade), *[mob.animate.shift(9*DOWN) for mob in [board, inner, formula_1, formula_2, formula_3, formula_4, formula_5, formula_6]], Transform(notice_1, notice_3))
        

####################################################################

class Chapter1_0(FrameScene):

    def construct(self):

        text1 = Text("第一节 坐标系", font = 'simsun', t2c={"第一节": YELLOW, "坐标系": GREEN})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(FrameScene):
    def construct(self):
        self.notices = [Notice("初中数学", "请　复习"), 
                        Notice("温故知新", "请　掌握"), 
                        Notice("双极坐标", "请　观赏"), 
                        Notice("罕见操作", "请　好奇"), 
                        Notice("易错思路", "请勿模仿"), 
                        Notice("罕见画法", "请　好奇"), 
                        Notice("关键问题", "请　思考"), 
                        ]
        self.notice = self.notices[0]

        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v, lines_h[10])
        
        self.bring_to_back(lines).play(Write(self.notice), Write(lines)) #我们先从大家最熟悉的例子出发
        self.wait(0, 21) #（空闲）
        self.wait(1, 17) #这是一张平面
        self.wait(2, 3) #上面铺满了均匀的坐标网格
        self.wait(0, 20) #（空闲）
        self.wait(2, 2) #我们在初中一年级就知道
        self.wait(2, 24) #这种坐标网格 叫作平面直角坐标系
        self.wait(0, 24) #（空闲）

        position = 2.4*UP + 3.2*RIGHT
        origin = Dot()
        dot = Dot(position, color = RED)
        line = Line(ORIGIN, position)
        self.play(GrowFromCenter(origin), ShowCreation(dot))
        self.add(line, origin, dot).play(ShowCreation(line))
        self.wait(0, 17) #同时我们还学习了另一种方法
        length = MTex(r"5").set_stroke(width = 8, color = BACK, background = True).scale(0.8).next_to(line.get_center(), UL, buff = 0.15)
        angle = MTex(r"36.9^\circ").set_stroke(width = 8, color = BACK, background = True).scale(0.8).next_to(0.6*RIGHT, UR, buff = 0.15)
        self.play(Write(length), Write(angle))
        self.wait(2, 11) #用方位角和距离来表示平面上的点

        circles = [Circle(radius = i*ratio, stroke_width = 1 if i%2 else 2, color = GREEN, n_components = 24) for i in range(1, 25)]
        rays = [Line(ORIGIN, 8.5*unit(i*TAU/24), stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(24)]
        radar = VGroup(*circles, *rays)
        self.wait(1, 12) #后来我们知道
        self.bring_to_back(radar).play(FadeOut(lines), FadeIn(radar))
        self.wait(0, 14) #这叫作极坐标
        self.wait(0, 23) #（空闲）

        offset = 7.6*RIGHT
        board = Rectangle(height = 8.4, width = 15.2, fill_opacity = 1, fill_color = BACK, stroke_width = 0).next_to(0.05*RIGHT, LEFT, buff = 0)
        inner = Rectangle(height = 8.4, width = 0.1, fill_opacity = 1, fill_color = BLACK, stroke_width = 0).next_to(0.05*RIGHT, LEFT, buff = 0)
        line_1 = Line(4.2*UP + 0.05*LEFT, 4.2*DOWN + 0.05*LEFT)
        line_2 = Line(4.2*UP + 0.05*RIGHT, 4.2*DOWN + 0.05*RIGHT, color = YELLOW_E)
        ratio = 0.4
        lines_h = [Line(32/9*LEFT + i*ratio*UP, 32/9*RIGHT + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-12, 12)]
        lines_v = [Line(5*UP + i*ratio*RIGHT, 5*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*LEFT)
        self.play(radar.animate.shift(32/9*RIGHT), origin.animate.shift(32/9*RIGHT), *[FadeOut(mob, 32/9*RIGHT) for mob in [dot, line, length, angle]], *[mob.shift(-offset).animate.shift(offset) for mob in [board, lines, inner, line_1, line_2]], run_time = 2)
        self.wait(0, 8) #直角坐标系和极坐标系
        self.wait(2, 25) #就是用来表示平面最常用的两个坐标系
        self.wait(0, 19) #（空闲）

        self.play(self.change_notice())
        self.wait(0, 27) #它们各有各的好处
        self.wait(2, 12) #我们可以对平面做很多操作
        self.wait(2, 11) #其中两大类是平移和旋转
        self.wait(0, 16) #（空闲）

        self.play(lines.animating(run_time = 2, rate_func = there_and_back).shift(UP))
        self.wait(0, 17) #直角坐标系就适合平移
        self.play(Rotate(radar, PI/6, about_point = 32/9*RIGHT, run_time = 2, rate_func = there_and_back))
        self.wait(0, 12) #而极坐标系就适合旋转
        self.wait(0, 26) #（空闲）

        self.wait(3, 23) #有没有既适合平移 又适合旋转的坐标系呢
        self.wait(1, 6) #答案是没有
        self.wait(0, 18) #（空闲）
        self.wait(3, 29) #那有没有既不适合平移 又不适合旋转的坐标系呢
        self.wait(1+0-1, 5+24)
        self.fade_out() #那可就太多了（空闲）

        point_a = Dot(2*LEFT)
        point_b = Dot(2*RIGHT)
        point = Dot(4*RIGHT + 2*UP, color = RED)
        line_left = Line(2*LEFT, 2*LEFT)
        line_right = Line(2*RIGHT, 2*RIGHT)
        self.bring_to_back(line_left, line_right).play(ShowCreation(point_a), ShowCreation(point_b), FadeInFromPoint(point, 4*RIGHT + 2*UP), self.change_notice(), line_left.animate.put_start_and_end_on(LEFT_SIDE, ORIGIN), line_right.animate.put_start_and_end_on(RIGHT_SIDE, ORIGIN))
        self.wait(2, 16) #比如说 我们在平面上找两个基准点

        handle_1 = Line(2*LEFT, 4*RIGHT + 2*UP)
        handle_2 = Line(2*RIGHT, 4*RIGHT + 2*UP)
        angle_1 = MTex(r"18.4^\circ").set_stroke(width = 8, color = BACK, background = True).scale(0.6).next_to(1*LEFT, UR, buff = 0.1)
        angle_2 = MTex(r"45^\circ").set_stroke(width = 8, color = BACK, background = True).scale(0.6).next_to(2.3*RIGHT, UR, buff = 0.1)
        self.add(handle_1, handle_2, point_a, point_b, point).play(ShowCreation(handle_1), ShowCreation(handle_2))
        self.play(Write(angle_1), Write(angle_2))
        self.wait(1, 15) #把坐标设定为关于这两个点的方向角
        rays_l = [Line(ORIGIN, 10*unit(i*TAU/48), stroke_width = 1 if i%4 else 3, color = PURPLE).shift(2*LEFT) for i in range(48)]
        rays_r = [Line(ORIGIN, 10*unit(i*TAU/48), stroke_width = 1 if i%4 else 3, color = PURPLE).shift(2*RIGHT) for i in range(48)]
        eyes = VGroup(*rays_l, *rays_r)
        self.bring_to_back(eyes).play(FadeIn(eyes))
        self.wait(2, 9) #就能得到一个平移和旋转都不适合的坐标系
        self.wait(1, 2) #（空闲）
        self.wait(2, 8) #当然 除了这么干以外
        self.wait(2, 18) #我们还有另一种截然不同的思路
        self.wait(2, 4) #那就是不把坐标系画标准
        self.wait(0, 4)
        self.fade_out(run_time = 0.5) #（空闲）

        number = 12
        ratio = 0.5
        rays_length = 2*number*ratio
        circles = [Circle(start_angle = -PI, radius = i*ratio, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE, n_components = 24) for i in range(2*number+1)]
        rays = [Line(ORIGIN, rays_length*unit(i*TAU/24 - PI), stroke_width = 1 if i%2 else 2, color = GREEN if i - 12 else WHITE).insert_n_curves(23) for i in range(2*number+1)]
        self.add(*circles, *rays, self.notice).play(*[FadeIn(mob, run_time = 0.5) for mob in circles + rays], self.change_notice()) #比如说......

        offset = 2.75*DOWN
        breadth = ratio*number
        alpha = ValueTracker(0.0)
        def start_line(t: float):
            return Line(ORIGIN, rays_length*unit(interpolate(-PI, PI/2, t))).shift(t**2*breadth*unit(-PI/2*(1-t)) + t*offset)
        def middle_line(t: float):
            return Line(ORIGIN, rays_length*unit(interpolate(0, PI/2, t))).shift(t**2*breadth*(np.tan((1-t)*PI/2))*unit(PI/2-PI/2*(1-t)) + t*offset)
        def end_line(t: float):
            return Line(ORIGIN, rays_length*unit(interpolate(PI, PI/2, t))).shift(t**2*breadth*unit(PI-PI/2*(1-t)) + t*offset)
        def circle_updater(index: int):
            def util(mob: Circle):
                value = alpha.get_value()
                ratio = index/(2*number)
                start, middle, end = start_line(value), middle_line(value), end_line(value)
                mob.set_points(ArcBetweenPoints(interpolate(start.get_start(), start.get_end(), ratio), interpolate(middle.get_start(), middle.get_end(), ratio), angle = PI*(1-value)).get_points()
                    ).append_points(ArcBetweenPoints(interpolate(middle.get_start(), middle.get_end(), ratio), interpolate(end.get_start(), end.get_end(), ratio), angle = PI*(1-value)).get_points())
            return util
        def ray_updater(index: int):
            def util(mob: Line):
                value = alpha.get_value()
                ratio = index/(2*number)
                if ratio <= 1/2:
                    mob.set_points(path_along_arc(PI*(1-value))(start_line(value).get_points(), middle_line(value).get_points(), 2*ratio))
                else:
                    mob.set_points(path_along_arc(PI*(1-value))(middle_line(value).get_points(), end_line(value).get_points(), 2*ratio-1))
            return util
        for i in range(2*number+1):
            circles[i].add_updater(circle_updater(i))
            rays[i].add_updater(ray_updater(i))
        self.add(circles[0]).play(alpha.animate.set_value(1), run_time = 3)
        for mob in circles + rays:
            mob.clear_updaters()
        new_coordinate = VGroup(*circles[1:], *rays, circles[0])
        label_r = MTex(r"r").scale(0.8).next_to(4*UP, DL, buff = 0.1).set_stroke(width = 8, color = BACK, background = True)
        label_theta = MTex(r"\theta").scale(0.8).next_to(breadth*RIGHT + offset, UL, buff = 0.1).set_stroke(width = 8, color = BACK, background = True)
        self.add(new_coordinate, self.notice).play(Write(label_r), Write(label_theta))
        self.wait(3+1-4, 25+12) #我们可以把极坐标系按照直角坐标系的样子 横平竖直地画出来
        self.wait(0, 20) #（空闲）

        self.wait(2, 12) #这种画法虽然很令人发指
        self.wait(2, 26) #但至少已经没人能看得出来它适合旋转了
        self.wait(1, 1) #（空闲）
        self.play(self.change_notice())
        self.wait(1, 22) #但既然坐标线已经变得横平竖直了
        self.wait(1, 18) #难道它不适合平移吗
        self.wait(0, 16) #（空闲）

        offset_l = 32/9*LEFT
        offset_r = 32/9*RIGHT + offset
        number = 12
        ratio = 0.5
        rays_length = 2*number*ratio
        circles = [Circle(start_angle = -PI, radius = i*ratio, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE, n_components = 72) for i in range(2*number+1)]
        rays = [Line(ORIGIN, rays_length*unit(i*TAU/24), stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE).insert_n_curves(71) for i in range(2*number)]
        radar = VGroup(*circles, *rays).apply_function(lambda t: np.array([min(t[0], 32/9), t[1], t[2]])).shift(32/9*LEFT)
        board = Rectangle(height = 8.4, width = 15.2, fill_opacity = 1, fill_color = BACK, stroke_width = 0).next_to(0.05*RIGHT, LEFT, buff = 0)
        line_1 = Line(4.2*UP + 0.05*LEFT, 4.2*DOWN + 0.05*LEFT)
        line_2 = Line(4.2*UP + 0.05*RIGHT, 4.2*DOWN + 0.05*RIGHT, color = YELLOW_E)
        inner = Rectangle(height = 8.4, width = 0.1, fill_opacity = 1, fill_color = BLACK, stroke_width = 0).next_to(0.05*RIGHT, LEFT, buff = 0).add(line_1, line_2)
        def edge_updater(mob):
            value = alpha.get_value()
            position = min(breadth + value*32/9, 64/9)
            mob.next_to(position*RIGHT + offset, UL, buff = 0.1)
        label_theta.add_updater(edge_updater)
        self.play(new_coordinate.animate.shift(32/9*RIGHT), label_r.animate.shift(32/9*RIGHT), alpha.set_value(0).animate.set_value(1.0), *[mob.shift(7.5*LEFT).animate.shift(7.5*RIGHT) for mob in [board, radar, inner]], run_time = 2)
        label_theta.clear_updaters()
        self.wait(1+2-2, 20+2) #当然不适合 坐标系画成这个样子时
        self.wait(2, 0) #图像就已经被严重扭曲了
        self.wait(0, 19) #（空闲）

        self.play(self.change_notice())
        self.wait(1, 24) #比如说 在正常的坐标系下
        line_left = Line(2*UP, DOWN + np.sqrt(3)*RIGHT, color = YELLOW).shift(offset_l)
        self.play(ShowCreation(line_left))
        self.wait(1, 0) #我们要是画一条直线
        point_left = Dot(2*UP, color = YELLOW).shift(offset_l)
        point_right = Dot(2*UP + 3*LEFT, color = YELLOW).shift(offset_r)
        theta = ValueTracker(PI/2)
        def func_left(t: float):
            return 1/np.cos(t - PI/6)*unit(t) + offset_l
        def point_left_updater(mob: Dot):
            value = theta.get_value()
            mob.move_to(func_left(value))
        def func_right(t: float):
            return np.array([-t/(PI/6), 1/np.cos(t - PI/6), 0]) + offset_r
        def point_right_updater(mob: Dot):
            value = theta.get_value()
            mob.move_to(func_right(value))
        self.play(ShowCreation(point_left), ShowCreation(point_right))
        point_left.add_updater(point_left_updater)
        point_right.add_updater(point_right_updater)
        line_right = ParametricCurve(func_right, [-PI/6, PI/2, PI/144], color = YELLOW).reverse_points()
        self.play(theta.animate.set_value(-PI/6), ShowCreation(line_right))
        point_left.clear_updaters()
        point_right.clear_updaters()
        self.play(point_left.animating(remover = True).scale(0), point_right.animating(remover = True).scale(0))
        self.wait(2+1-3, 3+18) #那在扭曲的坐标系下 它就会严重弯曲
        self.wait(0, 22) #（空闲）

        line_left_start = ParametricCurve(func_left, [PI/2, TAU/3-PI/24, PI/144], color = YELLOW)
        line_left_end = ParametricCurve(func_left, [-PI/6, -PI/3+PI/24, PI/144], color = YELLOW).reverse_points()
        line_right_start = ParametricCurve(func_right, [PI/2, TAU/3-PI/24, PI/144], color = YELLOW)
        line_right_end = ParametricCurve(func_right, [-PI/6, -PI/3+PI/24, PI/144], color = YELLOW).reverse_points()
        self.add(line_right_start, line_right_end, self.notice, board, radar, inner, line_left, line_left_start, line_left_end).play(*[ShowCreation(mob) for mob in [line_right_start, line_right_end, line_left_start, line_left_end]])
        self.remove(line_left, line_right, line_right_start, line_right_end, line_left_start, line_left_end)
        line_left = ParametricCurve(func_left, [-PI/3+PI/144, TAU/3-PI/144, PI/144], color = YELLOW)
        line_right = ParametricCurve(func_right, [-PI/3+PI/144, TAU/3-PI/144, PI/144], color = YELLOW)
        self.add(line_right, self.notice, board, radar, inner, line_left)
        self.wait(0, 23) #有些观众可能知道

        indicate = line_right.copy().set_stroke(color = WHITE, width = 6)
        self.add(indicate, self.notice, board, radar, inner, line_left).play(ShowPassingFlash(indicate, run_time = 2))
        self.add(indicate, self.notice, board, radar, inner, line_left).play(ShowPassingFlash(indicate, run_time = 2))
        self.wait(2+1-4, 27+27) #这时候 右边的这条“直线” 已经应该叫“测地线”了
        self.wait(0, 19) #（空闲）

        self.play(line_left.animate.shift(-0.5*unit(PI/6)), line_right.animate.scale(np.array([1, 0.5, 1]), about_point = offset_r))
        self.wait(1)
        self.play(line_left.animate.shift(0.5*unit(PI/6)), line_right.animate.scale(np.array([1, 2, 1]), about_point = offset_r))
        self.wait(1)
        fore = lambda t: t*(3-t**2)/2
        back = lambda t: t**2*(3-t)/2
        arrow_fore = Arrow(5*UP, UP, color = YELLOW, buff = 0).shift(offset_r)
        arrow_back = Arrow(UP, 5*UP, color = YELLOW, buff = 0).shift(offset_r)
        positions = [5*UP + offset_r + LEFT, UP + offset_r + LEFT]
        alpha = ValueTracker(0.0)
        def arrow_updater(index: int):
            def util(mob: Arrow):
                ratio = alpha.get_value()
                start = interpolate(positions[index], positions[1-index], back(ratio))
                end = interpolate(positions[index], positions[1-index], fore(ratio))
                mob.restore().put_start_and_end_on(start, end)
            return util
        arrow_fore.save_state().add_updater(arrow_updater(0))
        arrow_back.save_state().add_updater(arrow_updater(1))
        self.add(arrow_fore).play(alpha.animate.set_value(1), line_left.animate.shift(-0.8*unit(PI/6)), line_right.animate.scale(np.array([1, 0.2, 1]), about_point = offset_r), run_time = 1.5)
        alpha.set_value(0)
        self.remove(arrow_fore).wait(1)
        self.add(arrow_back).play(alpha.animate.set_value(1), line_left.animate.shift(0.8*unit(PI/6)), line_right.animate.scale(np.array([1, 5, 1]), about_point = offset_r), run_time = 1.5)
        self.remove(arrow_back).wait(2+2+0+1+1+0-8, 28+4+16+17+22+29) #而当我们平移左边这条直线的时候 它在右边就不是简单的平移 （空闲） 从结果上来说 这更像是一个拉伸变换 （空闲）
        
        self.play(FadeOut(line_left), FadeOut(line_right), new_coordinate.animate.set_color("#666666"), radar.animate.set_color("#666666"))
        self.wait(1, 2) #作为一个更直观的展示
        lines_h = [Line(32/9*LEFT + i*ratio*UP, 32/9*RIGHT + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE).shift(32/9*LEFT) for i in range(-13, 14)]
        lines_v = [Line(5*DOWN + i*ratio*RIGHT, 5*UP + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = PURPLE_A).shift(32/9*LEFT) if i<= 7 else VMobject() for i in range(-13, 14)]
        coordinate_left = VGroup(*lines_h, *lines_v)
        def func_h_positive(index: int):
            def util(t: float):
                return np.array([-t/(PI/6), index/(2*np.cos(t - PI/2)), 0]) + offset_r
            return util
        def func_h_negative(index: int):
            def util(t: float):
                return np.array([-t/(PI/6), index/(2*np.cos(t + PI/2)), 0]) + offset_r
            return util
        def func_v_positive(index: int):
            def util(t: float):
                return np.array([-t/(PI/6), index/(2*np.cos(t)), 0]) + offset_r
            return util
        def func_v_negative_1(index: int):
            def util(t: float):
                return np.array([-t/(PI/6), index/(2*np.cos(t - PI)), 0]) + offset_r
            return util
        def func_v_negative_2(index: int):
            def util(t: float):
                return np.array([-t/(PI/6), index/(2*np.cos(t + PI)), 0]) + offset_r
            return util
        lines_h = [ParametricCurve(func_h_negative(i), [-PI+PI/48, -PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = BLUE) for i in range(13, 0, -1)
                   ] + [Polyline(6*LEFT + 7*UP, 6*LEFT, stroke_width = 2).append_points(Line(6*LEFT, ORIGIN).insert_n_curves(48).get_points()).add_line_to(7*UP).add_line_to(ORIGIN).append_points(Line(ORIGIN, 6*RIGHT).insert_n_curves(48).get_points()).add_line_to(6*RIGHT + 7*UP).shift(offset_r)] + [
                   ParametricCurve(func_h_positive(i), [PI/48, PI-PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = BLUE).reverse_points() for i in range(1, 14)]
        lines_v = [ParametricCurve(func_v_negative_2(i), [PI/2+PI/48, PI, PI/144], stroke_width = 1 if i%2 else 2, color = PURPLE_A).append_points(
                    ParametricCurve(func_v_negative_1(i), [-PI, -PI/2-PI/48, PI/144]).get_points()).reverse_points() for i in range(13, 0, -1)
                   ] + [Line(9*LEFT, 3*LEFT, stroke_width = 2).insert_n_curves(48).add_line_to(3*LEFT + 7*UP).add_line_to(3*LEFT).append_points(Line(3*LEFT, 3*RIGHT).insert_n_curves(48).get_points()).add_line_to(7*UP + 3*RIGHT).add_line_to(3*RIGHT).append_points(Line(3*RIGHT, 9*RIGHT).insert_n_curves(48).get_points()).shift(offset_r)] + [
                   ParametricCurve(func_v_positive(i), [-PI/2+PI/48, PI/2-PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = PURPLE_A) for i in range(1, 14)]
        coordinate_right = VGroup(*lines_h, *lines_v)
        self.add(coordinate_right, label_r, label_theta, self.notice, board, radar, coordinate_left, inner).play(Write(coordinate_left), Write(coordinate_right), run_time = 4)
        self.wait(2+1-4, 29+2) #我们可以把直角坐标系的网格也画出来 也铺到右边
        self.wait(0, 18) #（空闲）
        self.wait(3, 2) #这些网格变换成了间隔均匀的曲线
        self.wait(2, 0) #网格交点也不再是直角了
        self.wait(0, 22) #（空闲）
        self.wait(1, 17) #从某种意义上来说
        self.wait(2, 27) #这确实也是平面的一种坐标系
        self.wait(2, 24) #不过这种看上去毫无优点的坐标系
        self.wait(1, 26) #应该不会有人真的拿着用吧
        self.wait(1, 0) #（空闲）
        self.fade_out(change_notice = True)
        self.wait(0, 12) #到目前为止

        picture_1 = ImageMobject("Patch1_1.png", height = 8)
        picture_2 = ImageMobject("Patch1_2.png", height = 8)
        picture_3 = ImageMobject("Patch1_3.png", height = 8)
        picture_4 = ImageMobject("Patch1_4.png", height = 8)
        self.play(FadeIn(picture_1, 8/9*RIGHT + 0.5*DOWN))
        self.wait(1, 15) #我们画过了正常的直角坐标系
        self.play(FadeIn(picture_2, 8/9*RIGHT + 0.5*UP))
        self.wait(0, 26) #正常的极坐标系
        self.add(picture_3, self.notice).play(FadeIn(picture_3, 8/9*LEFT + 0.5*DOWN), self.notice.animate.set_stroke(color = BLACK))
        self.wait(1, 12) #硬画得横平竖直的极坐标系
        self.play(FadeIn(picture_4, 8/9*LEFT + 0.5*UP))
        self.wait(1, 24) #以及这种极坐标对应的xy坐标系
        self.wait(0, 16) #（空闲）
        self.wait(3, 2) #那么 哪幅图代表的空间是弯曲的呢
        self.wait(0, 15) #到此共160秒

        text2 = Text("第二节 空间与标准图像", font = 'simsun', t2c={"第二节": YELLOW, "空间": GREEN, "标准图像": BLUE})

        self.bring_to_back(text2).play(Write(text2), self.notice.animating(remover = True).set_opacity(0).set_stroke(color = interpolate_color(BACK, BLACK, 0.5)), picture_1.save_state().animate.set_opacity(0.5).shift(1.5*(8/9*LEFT + 0.5*UP)), picture_2.save_state().animate.set_opacity(0.5).shift(1.5*(8/9*LEFT + 0.5*DOWN)), picture_3.save_state().animate.set_opacity(0.5).shift(1.5*(8/9*RIGHT + 0.5*UP)), picture_4.save_state().animate.set_opacity(0.5).shift(1.5*(8/9*RIGHT + 0.5*DOWN)))
        self.wait(3)
        self.play(FadeOut(text2), *[mob.animate.restore() for mob in [picture_1, picture_2, picture_3, picture_4]])

class Patch1_1(Scene):
    def construct(self):
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = PURPLE_A if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*LEFT + 2*UP)
        shade = Polygon(7.5*RIGHT + 4.5*UP, 7.5*RIGHT + 4.5*DOWN, 7.5*LEFT + 4.5*DOWN, 7.5*LEFT + 0.05*UP, 0.05*LEFT + 0.05*UP, 0.05*LEFT + 4.5*UP, stroke_color = YELLOW_E, fill_color = BACK, fill_opacity = 1)
        self.add(lines, lines_h[10], shade)

class Patch1_2(Scene):
    def construct(self):
        ratio = 0.4
        circles = [Circle(radius = i*ratio, stroke_width = 1 if i%2 else 2, color = GREEN, n_components = 24) for i in range(1, 25)]
        rays = [Line(ORIGIN, 8.5*unit(i*TAU/24), stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(24)]
        radar = VGroup(*circles, *rays).shift(32/9*LEFT + 2*DOWN)
        shade = Polygon(7.5*RIGHT + 4.5*DOWN, 7.5*RIGHT + 4.5*UP, 7.5*LEFT + 4.5*UP, 7.5*LEFT + 0.05*DOWN, 0.05*LEFT + 0.05*DOWN, 0.05*LEFT + 4.5*DOWN, stroke_color = WHITE, fill_color = BACK, fill_opacity = 1)
        self.add(radar, shade)
        
class Patch1_3(Scene):
    def construct(self):
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*RIGHT + 2*UP + 1.5*DOWN)
        shade = Polygon(7.5*LEFT + 4.5*UP, 7.5*LEFT + 4.5*DOWN, 7.5*RIGHT + 4.5*DOWN, 7.5*RIGHT + 0.05*UP, 0.05*RIGHT + 0.05*UP, 0.05*RIGHT + 4.5*UP, stroke_color = WHITE, fill_color = BACK, fill_opacity = 1)
        self.add(lines, lines_h[0], shade)

class Patch1_4(Scene):
    def construct(self):
        ratio = 0.4
        offset_r = 32/9*RIGHT + 2*DOWN + 1.5*DOWN
        def func_h_positive(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t - PI/2), 0]) + offset_r
            return util
        def func_h_negative(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t + PI/2), 0]) + offset_r
            return util
        def func_v_positive(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t), 0]) + offset_r
            return util
        def func_v_negative_1(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t - PI), 0]) + offset_r
            return util
        def func_v_negative_2(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t + PI), 0]) + offset_r
            return util
        lines_h = [ParametricCurve(func_h_negative(i), [-PI+PI/48, -PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = BLUE) for i in range(13, 0, -1)] + [ParametricCurve(func_h_positive(i), [PI/48, PI-PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = BLUE).reverse_points() for i in range(1, 14)]
        lines_v = [ParametricCurve(func_v_negative_2(i), [PI/2+PI/48, PI, PI/144], stroke_width = 1 if i%2 else 2, color = PURPLE_A).append_points(
                    ParametricCurve(func_v_negative_1(i), [-PI, -PI/2-PI/48, PI/144]).get_points()) for i in range(13, 0, -1)] + [ParametricCurve(func_v_positive(i), [-PI/2+PI/48, PI/2-PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = PURPLE_A).reverse_points() for i in range(1, 14)]
        coordinate_right = VGroup(*lines_h, *lines_v, Line(4*LEFT, 4*RIGHT, stroke_width = 2).shift(offset_r), Line(ORIGIN, 4*UP, stroke_width = 2).shift(offset_r), Line(ORIGIN, 4*UP, stroke_width = 2).shift(2.4*LEFT + offset_r), Line(ORIGIN, 4*UP, stroke_width = 2).shift(2.4*RIGHT + offset_r))
        shade = Polygon(7.5*LEFT + 4.5*DOWN, 7.5*LEFT + 4.5*UP, 7.5*RIGHT + 4.5*UP, 7.5*RIGHT + 0.05*DOWN, 0.05*RIGHT + 0.05*DOWN, 0.05*RIGHT + 4.5*DOWN, stroke_color = YELLOW_E, fill_color = BACK, fill_opacity = 1)
        self.add(coordinate_right, shade)

#################################################################### 

class Chapter2_1(FrameScene):
    def construct(self):
        self.notices = [Notice("正确答案", "请勿惊讶").set_stroke(color = BLACK), 
                        Notice("关键问题", "请　认真").set_stroke(color = BLACK), 
                        Notice("具体应用", "请　掌握"), 
                        Notice("温故知新", "请　对照"), 
                        Notice("具体例子", "请　掌握"), 
                        Notice("关键问题", "请　思考"), 
                        ]
        self.notice = self.notices[0]

        picture_1 = ImageMobject("Patch1_1.png", height = 8).save_state()
        picture_2 = ImageMobject("Patch1_2.png", height = 8).save_state()
        picture_3 = ImageMobject("Patch1_3.png", height = 8).save_state()
        picture_4 = ImageMobject("Patch1_4.png", height = 8).save_state()
        position_1 = 8/9*LEFT + 0.5*UP
        position_2 = 8/9*LEFT + 0.5*DOWN
        position_3 = 8/9*RIGHT + 0.5*UP
        position_4 = 8/9*RIGHT + 0.5*DOWN
        self.add(picture_1, picture_2, picture_3, picture_4).play(Write(self.notice))
        self.wait(2, 15) #答案是 哪幅图代表的空间都不是弯曲的
        self.wait(0, 22) #（空闲）

        self.play(self.notice.animate.set_stroke(color = interpolate_color(BLACK, BACK, 0.5)), picture_3.animate.set_opacity(0.5).shift(RIGHT), picture_4.animate.set_opacity(0.5).shift(RIGHT))
        self.wait(1, 4) #左边两幅图自然不必说
        self.wait(2, 6) #它们都是平面最正常的表示
        self.wait(0, 21) #（空闲）
        self.play(self.notice.animate.set_stroke(color = BLACK), picture_3.animate.restore().shift(0.5*RIGHT), picture_4.animate.restore().shift(0.5*RIGHT), picture_1.animate.set_opacity(0.5).shift(0.5*LEFT), picture_2.animate.set_opacity(0.5).shift(0.5*LEFT))
        self.wait(1, 4) #但右边两幅图所表示的
        self.wait(1, 5) #其实也是平面
        self.wait(0, 18) #（空闲）

        ratio = 0.5
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = PURPLE_A if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v)
        circles = [Circle(radius = i*ratio, stroke_width = 1 if i%2 else 2, color = GREY, n_components = 24) for i in range(1, 25)]
        rays = [Line(ORIGIN, 8.5*unit(i*TAU/24), stroke_width = 1 if i%2 else 2, color = GREY) for i in range(24)]
        radar = VGroup(*circles, *rays)
        self.bring_to_back(radar, lines, self.shade).play(self.notice.animate.set_stroke(color = BACK), FadeOut(picture_1, 0.5*position_1), FadeOut(picture_2, 0.5*position_2), FadeOut(picture_3, 0.5*position_3), FadeOut(picture_4, 0.5*position_4), FadeOut(self.shade))
        self.wait(1, 12) #虽然我们在画右边的图的时候
        offset = 2.75*DOWN
        lines_h = [Line(6*LEFT + i*ratio*UP, 6*RIGHT + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = GREY).insert_n_curves(71) for i in range(20)]
        lines_v = [Line(10*UP + i*ratio*RIGHT, i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREY).insert_n_curves(71) for i in range(-12, 13)]
        new_coordinate = VGroup(*lines_h, *lines_v).shift(offset)
        def func_h_positive(index: int):
            def util(t: float):
                return np.array([-2*ratio*t/(PI/6), ratio*index/np.cos(t - PI/2), 0]) + offset
            return util
        def func_h_negative(index: int):
            def util(t: float):
                return np.array([-2*ratio*t/(PI/6), ratio*index/np.cos(t + PI/2), 0]) + offset
            return util
        def func_v_positive(index: int):
            def util(t: float):
                return np.array([-2*ratio*t/(PI/6), ratio*index/np.cos(t), 0]) + offset
            return util
        def func_v_negative_1(index: int):
            def util(t: float):
                return np.array([-2*ratio*t/(PI/6), ratio*index/np.cos(t - PI), 0]) + offset
            return util
        def func_v_negative_2(index: int):
            def util(t: float):
                return np.array([-2*ratio*t/(PI/6), ratio*index/np.cos(t + PI), 0]) + offset
            return util
        lines_h = [ParametricCurve(func_h_negative(i), [-PI+PI/48, -PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = BLUE) for i in range(13, 0, -1)
                   ] + [ParametricCurve(func_h_positive(i), [PI/48, PI-PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = BLUE).reverse_points() for i in range(1, 14)]
        lines_v = [ParametricCurve(func_v_negative_2(i), [PI/2+PI/48, PI, PI/144], stroke_width = 1 if i%2 else 2, color = PURPLE_A).append_points(
                    ParametricCurve(func_v_negative_1(i), [-PI, -PI/2-PI/48, PI/144]).get_points()).reverse_points() for i in range(13, 0, -1)
                   ] + [ ParametricCurve(func_v_positive(i), [-PI/2+PI/48, PI/2-PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = PURPLE_A) for i in range(1, 14)]
        specials = [Line(6*LEFT, 6*RIGHT, stroke_width = 2).shift(offset).insert_n_curves(71), Line(6*LEFT + 7*UP, 6*LEFT, stroke_width = 2).shift(offset).insert_n_curves(71), Line(ORIGIN, 7*UP, stroke_width = 2).shift(offset).insert_n_curves(71), Line(6*RIGHT + 7*UP, 6*RIGHT, stroke_width = 2).shift(offset).insert_n_curves(71), Line(3*LEFT + 7*UP, 3*LEFT, stroke_width = 2).shift(offset).insert_n_curves(71), Line(3*RIGHT + 7*UP, 3*RIGHT, stroke_width = 2).shift(offset).insert_n_curves(71)]
        coordinate_right = VGroup(*lines_h, *lines_v, *specials)
        self.wait(3)
        label_r = MTex(r"r").scale(0.8).next_to(4*UP, DL, buff = 0.1).set_stroke(width = 8, color = BACK, background = True)
        label_theta = MTex(r"\theta").scale(0.8).next_to(6*RIGHT + offset, UL, buff = 0.1).set_stroke(width = 8, color = BACK, background = True)
        self.remove(radar, lines).add(new_coordinate, coordinate_right, self.notice).play(Write(label_r), Write(label_theta))
        self.wait(3+1-4, 28+24) #和左边相比 可以看到明显的扭曲形变的过程 但这只是我们画得不标准
        self.wait(0, 21) #（空闲）
        self.add(self.shade, picture_1.restore(), picture_2.restore(), picture_3.restore(), picture_4.restore(), self.notice).play(self.notice.animate.set_stroke(color = BLACK), FadeIn(picture_1, -position_1), FadeIn(picture_2, -position_2), FadeIn(picture_3, -position_3), FadeIn(picture_4, -position_4), FadeIn(self.shade))
        self.remove(new_coordinate, coordinate_right, label_r, label_theta).wait(1, 26) #四幅图代表的 毕竟都是平面
        self.wait(0, 26) #（空闲）
        self.play(self.change_notice())
        self.wait(1, 16) #不过话说回来 什么叫“标准”呢？
        self.wait(0, 21) #（空闲）

        ratio = 0.5
        offset_l = 32/9*LEFT
        lines_h = [Line(LEFT_SIDE + i*ratio*(1/2)*UP, RIGHT_SIDE + i*ratio*(1/2)*UP, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-20, 20)]
        lines_v = [Line(4*UP + i*ratio*(1/2)*RIGHT, 4*DOWN + i*ratio*(1/2)*RIGHT, stroke_width = 1 if i%4 else 2, color = BLUE if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h[:20], *lines_h[21:], *lines_v, lines_h[20]).shift(offset_l)
        label_x = MTex(r"x").scale(0.8).next_to(0.1*LEFT, DL, buff = 0.1).set_stroke(width = 8, color = BACK, background = True)
        label_y = MTex(r"y").scale(0.8).next_to(4*UP + 32/9*LEFT, UL, buff = 0.1).set_stroke(width = 8, color = BACK, background = True)
        circles = [Circle(radius = i*ratio/2, stroke_width = 1 if i%4 else 2, color = GREEN, n_components = 24) for i in range(1, 49)]
        rays = [Line(ORIGIN, 8.5*unit(i*TAU/24), stroke_width = 1 if i%4 else 2, color = GREEN if i else WHITE) for i in range(24)]
        radar = VGroup(*circles, *rays).shift(offset_l)
        offset_r = 32/9*RIGHT + 2.75*DOWN
        board = Rectangle(height = 8.2, width = 8, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        inner = Rectangle(height = 8.4, width = 7.8, fill_opacity = 1, fill_color = BACK, stroke_color = YELLOW_E)
        board.add(inner).next_to(0.05*LEFT, RIGHT, buff = 0)
        lines_h = [Line(6*(PI/6)*LEFT + i*ratio*(1/2)*UP, 6*(PI/6)*RIGHT + i*ratio*(1/2)*UP, stroke_width = 1 if i%4 else 2, color = GREEN if i else WHITE).insert_n_curves(71) for i in range(40)]
        lines_v = [Line(10*UP + i*ratio*(PI/6)*RIGHT, i*ratio*(PI/6)*RIGHT, stroke_width = 1 if i%4 else 2, color = GREEN if i else WHITE).insert_n_curves(71) for i in range(-12, 13)]
        new_coordinate = VGroup(*lines_h[1:], *lines_v, lines_h[0]).shift(offset_r)
        label_r = MTex(r"r").scale(0.8).next_to(4*UP + 32/9*RIGHT, DL, buff = 0.1).set_stroke(width = 8, color = BACK, background = True)
        label_theta = MTex(r"\theta").scale(0.8).next_to(PI*RIGHT + offset_r, UL, buff = 0.1).set_stroke(width = 8, color = BACK, background = True)
        self.add(lines, label_x, label_y, board, new_coordinate, label_r, label_theta, self.shade, picture_1, picture_2, picture_3, picture_4, self.notice
            ).play(self.notice.animate.set_stroke(color = BACK), FadeOut(picture_1, 0.5*position_1), FadeOut(picture_2, 0.5*position_2), FadeOut(picture_3, 0.5*position_3), FadeOut(picture_4, 0.5*position_4), FadeOut(self.shade))
        self.wait(1, 2) #最简单的一个想法就是
        line = Line(UP, 2*UR, color = YELLOW).center()
        self.play(ShowCreation(line))
        positions = [4*LEFT + 2*UP, 3.5*RIGHT + 1.5*UP, 2.5*RIGHT + DOWN, 3*LEFT + 1.5*DOWN]
        for i in range(4):
            self.wait(0, 27)
            self.play(line.animate.move_to(positions[i]))
        self.wait(2+2+2+1+0-5, 12+14+3+25+20-108) #如果我们随便画上一条线 要是这条线在画面上有多长 实际上就有多长 那这种画法就是标准的 （空闲）
        
        self.play(line.animate.move_to(offset_l + RIGHT + 1.5*UP))
        self.wait(3, 8) #比如说 在正常的直角坐标系里画这么一条线段
        length_l = MTex(r"l=\sqrt{5}", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BACK, background = True).next_to(offset_l + RIGHT + 1.5*UP, UL, buff = 0.1)
        self.play(Write(length_l))
        self.wait(0, 22) #它的长度就是√5
        self.wait(0, 18) #（空闲）

        YELLOW_G = interpolate_color(YELLOW, BACK, 0.5)
        line_copy = line.copy()
        self.add(line_copy, line).play(line.animate.move_to(offset_r + RIGHT + 1.5*UP), line_copy.animate.set_color(YELLOW_G), length_l.animate.set_fill(color = YELLOW_G))
        self.wait(1, 15) #而在横平竖直的极坐标系里面
        self.wait(2, 11) #同样画上这么一条“线段”
        length_r = MTex(r"l\approx 3.1678", color = YELLOW).scale(0.8).set_stroke(width = 8, color = BACK, background = True).next_to(offset_r + RIGHT + 1.5*UP, UL, buff = 0.1)
        self.play(Write(length_r))
        self.wait(1, 6) #它的实际长度就不是√5
        self.wait(0, 18) #（空闲）

        point_r = Dot(offset_r + UP, color = YELLOW)
        point_l = Dot(offset_l + RIGHT, color = YELLOW)
        def func_left(t: float):
            return (1+t/2)*unit(-t) + offset_l
        line_left = ParametricCurve(func_left, [0, 2, 0.01], color = YELLOW)
        self.play(ShowCreation(point_l), ShowCreation(point_r))
        alpha = ValueTracker(0.0)
        def point_l_updater(mob: Dot):
            value = alpha.get_value()
            mob.move_to(func_left(value))
        point_l.add_updater(point_l_updater)
        self.play(point_r.animate.shift(2*RIGHT + UP), alpha.animate.set_value(2), ShowCreation(line_left))
        point_l.clear_updaters()
        self.play(point_l.animate.scale(0), point_r.animate.scale(0), remover = True)
        self.wait(0, 6) #而且 它在平面中其实也不是直线
        self.wait(0, 28) #（空闲）

        self.play(self.change_notice())
        self.wait(1, 15) #标准的图像具有直观的优点
        self.wait(2, 15) #但不标准的图像也有另外的优点
        self.wait(1, 1) #那就是方便
        self.wait(0, 20) #（空闲）

        self.clear().add(self.notice).wait(2, 7) #大家都知道球面是弯曲的
        self.wait(1, 7) #和平面不一样
        self.wait(0, 18) #（空闲）
        self.wait(2, 0) #我们要是想画一个球面
        self.wait(2, 19) #那么标准的图像就必须在三维空间中
        self.wait(0, 21) #（空闲）
        
        self.wait(1, 21) #地球是个球体
        self.wait(1, 28) #标准的图像只有地球仪
        self.wait(0, 17) #（空闲）

        ratio_h = 3.5/12
        lines_h = [Line(3.5*LEFT + i*ratio_h*UP, 3.5*RIGHT + i*ratio_h*UP, stroke_width = 1 if i%2 else 2).shift(3*RIGHT) for i in range(-6, 7)]
        ratio_v = 3.5/12
        lines_v = [Line(1.75*UP + i*ratio_v*RIGHT, 1.75*DOWN + i*ratio_v*RIGHT, stroke_width = 1 if i%2 else 2).shift(3*RIGHT) for i in range(-12, 13)]
        grid = VGroup(*lines_h, *lines_v)
        world_map = ImageMobject("earth_day.jpg", height = 3.5).shift(3*RIGHT)
        self.add(world_map, self.shade, self.notice).play(FadeOut(self.shade), world_map.shift(3.5*RIGHT).animate.shift(3.5*LEFT), run_time = 2)
        self.wait(0, 11) #如果我们想画一张世界地图
        self.wait(1, 27) #那么它必然是不标准的
        self.wait(0, 18) #（空闲）

        self.play(Write(grid))
        copies_h = [mob.copy().set_stroke(width = 2*mob.get_stroke_width(), color = YELLOW) for mob in lines_h]
        copies_v = [mob.copy().set_stroke(width = 2*mob.get_stroke_width(), color = YELLOW) for mob in lines_v]
        self.play(LaggedStart(*[ShowPassingFlash(mob) for mob in copies_h], lag_ratio = 0.05, run_time = 2), LaggedStart(*[ShowPassingFlash(mob) for mob in copies_v], lag_ratio = 0.05, run_time = 2))
        self.wait(1+3-4, 29+8) #最常见的那些世界地图 它们的经线和纬线都取成了横平竖直的样子
        self.wait(0, 16) #（空闲）

        hole = Rectangle(height = 1.5, width = 8, stroke_color = YELLOW).shift(3*RIGHT + 1.25*UP)
        shade = Shade(fill_opacity = 0.5).append_points(hole.get_points()[::-1])
        self.play(ShowCreation(hole), self.change_notice())
        self.add(shade, hole, self.notice).play(FadeIn(shade))
        self.wait(0, 14) #这些地图在南北极处的处理
        self.wait(2, 10) #几乎就是我们之前见过的
        self.wait(1, 28) #硬画得横平竖直的极坐标
        self.wait(0, 20) #（空闲）

        self.wait(1, 12) #和平面一样
        self.wait(1, 29) #球面画在了平面上
        self.wait(2, 4) #是图像产生了扭曲
        self.wait(3, 16) #并不意味着球面这个二维空间也变得平直了
        self.wait(0, 28) #（空闲）

        self.fade_out(change_notice = True)
        self.wait(0, 9) #再比如......
        tex = MTex(r"z=x^2+y^2").shift(3*UP)
        self.play(Write(tex))
        self.wait(0, 24) #一个二元函数的图像
        self.wait(2, 8) #也可以是一个二维空间
        self.wait(1, 29) #想要画出它的标准图像
        self.wait(1, 16) #也得在三维空间中
        self.wait(0, 19) #（空闲）
        self.wait(3, 28) #但同时 这个图像也可以很自然地画在平面上
        self.wait(0, 19) #（空闲）
        self.wait(2, 20) #每个图像都天然带有一个坐标系
        self.wait(1, 24) #就是这个函数的两个自变量
        self.wait(0, 20) #（空闲）
        self.fade_out(change_notice = True)
        self.wait(1, 6) #那么现在问题就来了

        picture_1 = ImageMobject("Patch2_4.png", height = 8)
        picture_2 = ImageMobject("Patch2_5.png", height = 8)
        picture_3 = ImageMobject("Patch2_6.png", height = 8)
        picture_4 = ImageMobject("Patch2_7.png", height = 8)
        self.add(picture_1, picture_2, picture_3, picture_4, self.notice).play(LaggedStart(FadeIn(picture_1, 8/9*RIGHT + 0.5*DOWN), FadeIn(picture_2, 8/9*LEFT + 0.5*DOWN), FadeIn(picture_3, 8/9*RIGHT + 0.5*UP), FadeIn(picture_4, 8/9*LEFT + 0.5*UP), lag_ratio = 0.5, run_time = 2.5, group = VGroup()), self.notice.animating(run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)).set_stroke(color = BLACK))
        self.wait(1, 2) #如果所有二维空间都能画成横平竖直的样子
        self.wait(2, 18) #我们还怎么区分哪个是哪个呢
        self.wait(1, 7) #到此共136秒

        text3 = Text("第三节 弯曲空间与线元", font = 'simsun', t2c={"第三节": YELLOW, "弯曲空间": GREEN, "线元": BLUE})

        self.bring_to_back(text3).play(Write(text3), self.notice.animating(remover = True).set_opacity(0).set_stroke(color = interpolate_color(BACK, BLACK, 0.5)), picture_1.save_state().animate.set_opacity(0.5).shift(1.5*(8/9*LEFT + 0.5*UP)), picture_2.save_state().animate.set_opacity(0.5).shift(1.5*(8/9*RIGHT + 0.5*UP)), picture_3.save_state().animate.set_opacity(0.5).shift(1.5*(8/9*LEFT + 0.5*DOWN)), picture_4.save_state().animate.set_opacity(0.5).shift(1.5*(8/9*RIGHT + 0.5*DOWN)))
        self.wait(2)
        self.play(picture_1.animate.restore(), *[FadeOut(mob) for mob in [text3, picture_2, picture_3, picture_4]])

class Patch2_2(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        sphere = Sphere(radius=3).rotate(PI, axis = RIGHT)
        ball = TexturedSurface(sphere, "Grid_2.png")
        texture = TexturedSurface(sphere, "earth_day_grid.jpg").rotate(PI, axis = RIGHT)
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        camera = self.camera.frame
        camera.set_orientation(Rotation(quadternion))
        camera.add_updater(lambda m, dt: m.increment_theta(-0.05 * dt))

        self.play(ShowCreation(ball), run_time = 2)
        self.wait(0, 7) #大家都知道球面是弯曲的
        self.wait(1, 7) #和平面不一样
        self.wait(0, 18) #（空闲）
        self.wait(2, 0) #我们要是想画一个球面
        self.wait(2, 19) #那么标准的图像就必须在三维空间中
        self.wait(0, 21) #（空闲）
        self.play(ShowCreation(texture), Uncreate(ball), run_time = 3)
        self.wait(1+1-3, 21+28) #地球是个球体 标准的图像只有地球仪
        self.wait(0, 17) #（空闲）
        alpha = ValueTracker()
        def camera_updater(mob: CameraFrame):
            value = alpha.get_value()
            mob.set_width(interpolate(8, FRAME_WIDTH, value))
        camera.add_updater(camera_updater)
        self.play(alpha.animate.set_value(1), run_time = 2)
        camera.remove_updater(camera_updater)
        self.wait(0, 11) #如果我们想画一张世界地图
        self.wait(1, 27) #那么它必然是不标准的
        self.wait(0, 18) #（空闲）
        self.wait(1, 29) #最常见的那些世界地图
        self.wait(3, 8) #它们的经线和纬线都取成了横平竖直的样子
        self.wait(0, 16) #（空闲）
        self.play(camera.clear_updaters().animate.set_orientation(Rotation.identity()), run_time = 2)
        self.wait(0, 14) #这些地图在南北极处的处理
        self.wait(2, 10) #几乎就是我们之前见过的
        self.wait(1, 28) #硬画得横平竖直的极坐标
        self.wait(0, 20) #（空闲）
        self.wait(1, 12) #和平面一样
        self.wait(1, 29) #球面画在了平面上
        self.wait(2, 4) #是图像产生了扭曲
        self.wait(3, 16) #并不意味着球面这个二维空间也变得平直了
        self.wait(0, 28) #（空闲）

class Patch2_3(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 16.0)}, 
            }
    }
    def construct(self):
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        camera = self.camera.frame
        camera.shift(5.5*OUT).set_orientation(Rotation(quadternion))
        camera.add_updater(lambda m, dt: m.increment_theta(-0.05 * dt))

        lines_x = [ParametricCurve(lambda t: np.array([t, i/2, t**2 + (i/2)**2]), [-np.sqrt(4.5-(i/2)**2), np.sqrt(4.5-(i/2)**2), 0.01], depth_test = True) for i in range(-4, 5)]
        lines_y = [ParametricCurve(lambda t: np.array([i/2, t, t**2 + (i/2)**2]), [-np.sqrt(4.5-(i/2)**2), np.sqrt(4.5-(i/2)**2), 0.01], depth_test = True) for i in range(-4, 5)]
        mesh = VGroup(*lines_x, *lines_y).set_color(YELLOW)
        paraboloid = ParametricSurface(lambda u, v: np.array(u*unit(v) + u**2*OUT), u_range = (0, np.sqrt(4.5)), v_range = (0, TAU), color = BLUE).rotate(PI/6)
        z_axis = Arrow(DOWN, 5*UP, buff = 0, depth_test = True).rotate(PI/2, about_point = ORIGIN, axis = RIGHT)
        axes = VGroup(Arrow(2.5*DOWN, 2.5*UP, buff = 0), Arrow(2.5*LEFT, 2.5*RIGHT, buff = 0), depth_test = True)
        self.add(axes, paraboloid, z_axis).wait(3, 3) #一个二元函数的图像
        self.wait(2, 8) #也可以是一个二维空间
        self.wait(1, 29) #想要画出它的标准图像
        self.wait(1, 16) #也得在三维空间中
        self.wait(0, 19) #（空闲）

        self.play(ShowCreation(mesh), run_time = 2)
        self.wait(1, 28) #但同时 这个图像也可以很自然地画在平面上
        self.wait(0, 19) #（空闲）

        self.play(camera.clear_updaters().animate.set_orientation(Rotation.identity()), FadeOut(z_axis), run_time = 2)
        self.play(camera.animating(run_time = 2).shift(5.5*IN), paraboloid.animate.scale(np.array([1, 1, 0]), min_scale_factor = 0), mesh.animate.scale(np.array([1, 1, 0]), min_scale_factor = 0))
        self.wait(2+1-4, 20+24) #每个图像都天然带有一个坐标系 就是这个函数的两个自变量
        self.wait(0, 20) #（空闲）
        self.play(FadeIn(self.shade))
        self.wait(1, 6) #那么现在问题就来了

class Patch2_4(Scene):
    def construct(self):
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*LEFT + 2*UP)
        shade = Polygon(7.5*RIGHT + 4.5*UP, 7.5*RIGHT + 4.5*DOWN, 7.5*LEFT + 4.5*DOWN, 7.5*LEFT + 0.05*UP, 0.05*LEFT + 0.05*UP, 0.05*LEFT + 4.5*UP, stroke_color = WHITE, fill_color = BACK, fill_opacity = 1)
        notice = Rectangle(height = 0.7, width = 3, stroke_color = WHITE, fill_color = BLACK, fill_opacity = 1).next_to(0.05*UL, UL, buff = 0)
        text = MTexText(r"平面", color = YELLOW).scale(0.8).move_to(notice)
        self.add(lines, lines_h[10], shade, notice, text)

class Patch2_5(Scene):
    def construct(self):
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*RIGHT + 2*UP + 1.5*DOWN)
        shade = Polygon(7.5*LEFT + 4.5*UP, 7.5*LEFT + 4.5*DOWN, 7.5*RIGHT + 4.5*DOWN, 7.5*RIGHT + 0.05*UP, 0.05*RIGHT + 0.05*UP, 0.05*RIGHT + 4.5*UP, stroke_color = YELLOW_E, fill_color = BACK, fill_opacity = 1)
        notice = Rectangle(height = 0.7, width = 3, stroke_color = YELLOW_E, fill_color = BLACK, fill_opacity = 1).next_to(0.05*UR, UR, buff = 0)
        text = MTexText(r"平面（极坐标）", color = YELLOW).scale(0.8).move_to(notice)
        self.add(lines, lines_h[0], shade, notice, text)

class Patch2_6(Scene):
    def construct(self):
        ratio_h = 3.5/12
        lines_h = [Line(3.5*LEFT + i*ratio_h*UP, 3.5*RIGHT + i*ratio_h*UP, stroke_width = 1 if i%2 else 2) for i in range(-6, 7)]
        ratio_v = 3.5/12
        lines_v = [Line(1.75*UP + i*ratio_v*RIGHT, 1.75*DOWN + i*ratio_v*RIGHT, stroke_width = 1 if i%2 else 2) for i in range(-12, 13)]
        grid = VGroup(*lines_h, *lines_v).shift(32/9*LEFT + 2*DOWN)
        shade = Polygon(7.5*RIGHT + 4.5*DOWN, 7.5*RIGHT + 4.5*UP, 7.5*LEFT + 4.5*UP, 7.5*LEFT + 0.05*DOWN, 0.05*LEFT + 0.05*DOWN, 0.05*LEFT + 4.5*DOWN, stroke_color = YELLOW_E, fill_color = BACK, fill_opacity = 1)
        notice = Rectangle(height = 0.7, width = 3, stroke_color = YELLOW_E, fill_color = BLACK, fill_opacity = 1).next_to(0.05*DL, DL, buff = 0)
        text = MTexText(r"球面", color = YELLOW).scale(0.8).move_to(notice)
        self.add(grid, shade, notice, text)
        
class Patch2_7(Scene):
    def construct(self):
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = YELLOW if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = YELLOW if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*RIGHT + 2*DOWN)
        shade = Polygon(7.5*LEFT + 4.5*DOWN, 7.5*LEFT + 4.5*UP, 7.5*RIGHT + 4.5*UP, 7.5*RIGHT + 0.05*DOWN, 0.05*RIGHT + 0.05*DOWN, 0.05*RIGHT + 4.5*DOWN, stroke_color = WHITE, fill_color = BACK, fill_opacity = 1)
        notice = Rectangle(height = 0.7, width = 3, stroke_color = WHITE, fill_color = BLACK, fill_opacity = 1).next_to(0.05*DR, DR, buff = 0)
        text = MTexText(r"抛物面", color = YELLOW).scale(0.8).move_to(notice)
        self.add(lines, shade, notice, text)

#################################################################### 

class Chapter3_1(FrameScene):
    def construct(self):
        self.notices = [Notice("正确答案", "请　理解"), 
                        Notice("高等数学", "请取微元"), 
                        Notice("思路转换", "请　接受").set_stroke(color = BLACK), 
                        Notice("重要概念", "请记笔记").set_stroke(color = BLACK), 
                        Notice("具体例子", "请　掌握").set_stroke(color = BLACK), 
                        Notice("具体例子", "请　掌握"), 
                        ]
        self.notice = self.notices[0]

        picture_1 = ImageMobject("Patch2_4.png", height = 8).save_state()
        self.add(picture_1).play(Write(self.notice))
        self.wait(3, 6) #答案是 我们只要规定好这个空间的长度怎么算
        self.wait(2, 17) #那么这个空间很多其它性质
        self.wait(2, 17) #像是面积 或者是曲率
        self.wait(1, 12) #也都会被确定下来
        self.wait(0, 18) #（空闲）

        riemann = LabelPicture("Riemann.jpeg", "伯恩哈德·黎曼（1826.9.17 - 1866.7.20）").shift(3*RIGHT)
        self.play(FadeIn(riemann, 0.5*UP))
        self.wait(0, 25) #这是黎曼告诉我们的方法
        self.wait(0, 25) #（空闲）

        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(5*UP + i*ratio*RIGHT, 5*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h[:10], *lines_h[11:], *lines_v, lines_h[10]).shift(32/9*LEFT + 2*UP)
        shade = Polygon(7.5*RIGHT + 10*UP, 7.5*RIGHT + 4.5*DOWN, 7.5*LEFT + 4.5*DOWN, 7.5*LEFT + 0.05*UP, 0.05*LEFT + 0.05*UP, 0.05*LEFT + 10*UP, stroke_color = WHITE, fill_color = BACK, fill_opacity = 1)
        board = Shade(fill_color = BLACK)
        notice = Rectangle(height = 0.7, width = 3, stroke_color = WHITE, fill_color = BLACK, fill_opacity = 1).next_to(0.05*UL, UL, buff = 0)
        text = MTexText(r"平面", color = YELLOW).scale(0.8).move_to(notice)
        def func(t: float):
            return 0.8*np.array([1-np.cos(t), (t-PI)-np.sin(t), 0])
        cycloid = ParametricCurve(func, [0, TAU, TAU/100], color = YELLOW).shift(32/9*LEFT)
        alpha = ValueTracker(0.0)
        def cycloid_updater(mob: ParametricCurve):
            value = alpha.get_value()
            mob.set_points(ParametricCurve(func, [(1-value)*PI, (1+value)*PI, TAU/100], color = YELLOW).shift(32/9*LEFT + (1-value)*2*UP).get_points())
        cycloid.add_updater(cycloid_updater)
        self.remove(picture_1).bring_to_back(board, lines, shade, notice, text).add(cycloid).play(alpha.animating(run_time = 2).set_value(1.0), FadeOut(riemann, 0.5*DOWN, rate_func = rush_into), *[mob.animating(run_time = 2).shift(5*DOWN) for mob in [shade, notice, text]], lines.animating(run_time = 2).shift(2*DOWN), self.change_notice())
        cycloid.clear_updaters()
        self.wait(1+1-2, 23+20) #求一条曲线的长度 如果是在平面上
        self.wait(1, 28) #想必大家都很熟悉怎么办了
        self.wait(0, 22) #（空闲）

        def marks(t: float):
            return Line(0.05*unit(t/2 + PI/2), -0.05*unit(t/2 + PI/2), color = YELLOW).shift(func(t) + 32/9*LEFT)
        tips = VGroup(*[marks(i*TAU/20) for i in range(21)])
        ds = MTex(r"\mathrm{d}s", color = YELLOW).set_stroke(width = 8, color = BLACK, background = True).scale(0.6).shift(func(6.25*TAU/10) - 0.3*unit(6.25*TAU/20 + PI/2) + 32/9*LEFT)
        step_1 = MTex(r"1.").next_to(1.25*RIGHT + 1.5*UP)
        line_1 = Line(step_1, ds, stroke_width = 2, buff = 0.2, color = YELLOW)
        step_2 = MTex(r"2.\ \mathrm{d}s^2=\mathrm{d}x^2+\mathrm{d}y^2", tex_to_color_map = {r"mathrm{d}s": YELLOW, (r"\mathrm{d}x", r"\mathrm{d}y"): BLUE}).next_to(1.25*RIGHT)
        step_3 = MTex(r"3.\ L=\int\sqrt{\mathrm{d}s^2}", tex_to_color_map = {r"mathrm{d}s": YELLOW, r"L": ORANGE}).next_to(1.25*RIGHT + 1.5*DOWN)
        self.play(ShowCreation(tips, run_time = 2), Write(step_1, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)), Write(ds, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)), ShowCreation(line_1, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)))
        self.wait(0, 3) #把曲线截成很多小段
        self.play(Write(step_2, run_time = 1))
        self.wait(1, 20) #把每一段小段当作是直的
        self.wait(2, 9) #按照勾股定理求出长度
        self.play(Write(step_3, run_time = 1))
        self.wait(0, 26) #再对整条曲线积分
        self.wait(2, 5) #我们就能得到曲线的总长度
        self.wait(0, 20) #（空闲）

        surr_1 = SurroundingRectangle(step_1)
        surr_3 = SurroundingRectangle(step_3[0:2])
        self.play(ShowCreation(surr_1))
        self.wait(0, 8) #截成小段......
        self.play(ShowCreation(surr_3))
        self.wait(0, 20) #......和对整条曲线积分
        self.play(*[mob.animate.set_color(GREY) for mob in [step_1, step_3, surr_1, surr_3]])
        self.wait(1, 9) #实际上和求长度没什么关系
        self.wait(0, 21) #（空闲）

        gauge = step_2[2:]
        dl = ParametricCurve(func, [12*TAU/20, 13*TAU/20, TAU/100], color = YELLOW).shift(32/9*LEFT)
        surr_2 = SurroundingRectangle(gauge)
        self.play(ShowCreation(surr_2))
        self.wait(1, 22) #真正会因为空间的不同而受影响的
        self.add(dl).play(*[FadeOut(mob) for mob in [step_1, step_3, surr_1, surr_3, line_1, step_2[0:2]]], Uncreate(tips, run_time = 2), Uncreate(cycloid, run_time = 2))
        self.wait(0, 9) #只有中间求小段长度这一步
        self.wait(0, 24) #（空闲）

        ratio = 0.4
        lines_h = [Line(LEFT_SIDE/2 + 0.05*RIGHT + i*ratio*UP, RIGHT_SIDE/2 + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(20)]
        lines_v = [Line(7*UP + i*ratio*RIGHT, i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(-8, 9)]
        radar = VGroup(*lines_h[1:], *lines_v, lines_h[0]).shift(32/9*RIGHT + 2.75*DOWN)
        label_r = MTex(r"r").scale(0.8).next_to(4*UP + 32/9*RIGHT, DL, buff = 0.1).set_stroke(width = 8, color = BLACK, background = True)
        label_theta = MTex(r"\theta").scale(0.8).next_to(RIGHT_SIDE + 2.75*DOWN, UL, buff = 0.1).set_stroke(width = 8, color = BLACK, background = True)
        dl_2 = Line(1.6*LEFT + 2*UP, 0.8*LEFT + 1.6*UP, color = YELLOW).shift(32/9*RIGHT + 2.75*DOWN)
        ds_2 = MTex(r"\mathrm{d}s", color = YELLOW).set_stroke(width = 8, color = BLACK, background = True).scale(0.8).move_to(dl_2).shift(0.3*UR)
        self.bring_to_back(board, radar, label_r, label_theta, dl_2, ds_2).play(self.change_notice(run_time = 1.5, rate_func = squish_rate_func(smooth, 1/3, 1)), *[mob.animating(run_time = 2).shift(7.45*LEFT) for mob in [lines, ds, dl, shade, gauge, surr_2]], *[mob.shift(7.45*RIGHT).animating(run_time = 2).shift(7.45*LEFT) for mob in [radar, label_r, label_theta, dl_2, ds_2]])
        self.remove(lines, ds, dl).wait(0, 26) #可想而知 当空间不同了
        surr_2.set_fill(opacity = 1, color = BACK)
        gauge_2 = MTex(r"\mathrm{d}s^2\ne \mathrm{d}r^2+\mathrm{d}\theta^2", tex_to_color_map = {r"\ne": RED, r"\mathrm{d}s": YELLOW, (r"\mathrm{d}r", r"\mathrm{d}\theta"): GREEN})
        gauge_2.shift(gauge[0].get_center() - gauge_2[0].get_center())
        self.add(gauge_2, surr_2, gauge).play(*[mob.animating(remover = True).shift(UP).set_color(BACK) for mob in [surr_2, gauge]])
        self.wait(2, 11) #我们求长度 自然也没法再用勾股定理了
        self.wait(0, 18) #（空闲）

        self.play(gauge_2.animate.set_color(GREY))
        self.wait(1, 2) #或者可以用另一种说法
        self.wait(2, 13) #每个空间都有它自己的勾股定理
        self.wait(0, 20) #（空闲）

        gauge = MTex(r"\mathrm{d}s^2= \mathrm{d}r^2+{r^2}\mathrm{d}\theta^2", tex_to_color_map = {r"\mathrm{d}s": YELLOW, r"{r^2}": TEAL, (r"\mathrm{d}r", r"\mathrm{d}\theta"): GREEN}).move_to(gauge_2)
        gauge_2.submobjects = gauge_2.submobjects[::-1]
        surr = SurroundingRectangle(gauge, fill_opacity = 1, fill_color = BACK)
        self.play(ShowIncreasingSubsets(gauge_2, rate_func = lambda t: smooth(1-t), remover = True), ShowIncreasingSubsets(gauge))
        self.add(surr, gauge).play(ShowCreation(surr))
        self.wait(0, 22) #比如说 在极坐标系上面
        self.wait(2, 14) #一小段线段的长度 应该这么求
        self.wait(0, 23) #（空闲）

        line_shade = Line(4*UP, 4*DOWN).shift(0.05*RIGHT)
        self.remove(shade).add(line_shade, surr, gauge)
        board.next_to(0.05*RIGHT, buff = 0)
        shade = Shade(height = 9, width = 15, stroke_width = 4, stroke_color = YELLOW_E).shift(7.45*RIGHT)
        ratio = 0.5
        circles = [Circle(radius = i*ratio, stroke_width = 1 if i%2 else 2, color = GREY, n_components = 24) for i in range(1, 25)]
        rays = [Line(ORIGIN, 8.5*unit(i*TAU/24), stroke_width = 1 if i%2 else 2, color = GREY if i else WHITE) for i in range(24)]
        radar = VGroup(*circles, *rays).shift(32/9*LEFT)
        dl_left = Line(2*unit(1.6*PI/6), 1.6*unit(0.8*PI/6), color = YELLOW).shift(32/9*LEFT)
        ds_left = MTex(r"\mathrm{d}s", color = YELLOW).set_stroke(width = 8, color = BLACK, background = True).scale(0.8).move_to(dl_left).shift(0.3*RIGHT + 0.1*UP)
        line_1 = Line(ORIGIN, 2*unit(1.6*PI/6), color = WHITE, stroke_width = 2).shift(32/9*LEFT)
        line_2 = Line(ORIGIN, 1.6*unit(0.8*PI/6), color = WHITE, stroke_width = 2).shift(32/9*LEFT)
        angle_dthrta = Arc(0.8*PI/6, 0.8*PI/6, radius = 0.3, color = GREEN).shift(32/9*LEFT)
        dtheta = MTex(r"\mathrm{d}\theta", color = GREEN).scale(0.6).set_stroke(width = 8, color = BLACK, background = True).shift(0.6*unit(1.2*PI/6) + 32/9*LEFT)
        line_dr = Line(2*unit(1.6*PI/6), 1.6*unit(1.6*PI/6), color = GREEN).shift(32/9*LEFT)
        dr = MTex(r"\mathrm{d}r", color = GREEN).scale(0.6).set_stroke(width = 8, color = BLACK, background = True).shift(1.8*unit(1.6*PI/6) + 0.2*unit(1.6*PI/6 + PI/2) + 32/9*LEFT)
        line_rdtheta = Line(1.6*unit(1.6*PI/6), 1.6*unit(0.8*PI/6), color = TEAL).shift(32/9*LEFT)
        rdtheta = MTex(r"r\mathrm{d}\theta", color = TEAL).scale(0.6).set_stroke(width = 8, color = BLACK, background = True).shift(32/9*LEFT + 1.2*unit(1.2*PI/6))
        geo_mobs = [angle_dthrta, line_1, line_2, line_dr, line_rdtheta, rdtheta, dtheta, dr, dl_left, ds_left]
        board_copy = board.copy().center()
        self.bring_to_back(board_copy, radar, *geo_mobs, shade).play(*[mob.shift(7.45*LEFT).animate.shift(7.45*RIGHT) for mob in [radar, *geo_mobs, shade]], *[mob.animating(path_arc = PI/2).move_to(2.5*UP) for mob in [gauge, surr]], run_time = 2)
        self.wait(1, 7) #这个时候我们或许应该切回正常的极坐标
        self.wait(2, 24) #这样就可以接着使用普通的勾股定理
        self.wait(2, 0) #这个式子也会更直观一些
        self.wait(0, 21) #（空闲）

        shade_2 = Shade().next_to(4*UP, UP, buff = 0)
        title = Title("线元").shift(UP)
        title_line = TitleLine().save_state().put_start_and_end_on(4*UP, 4*UP)
        self.play(self.change_notice(), shade_2.animate.shift(DOWN), title.animate.shift(DOWN), title_line.animate.restore(), label_r.animate.shift(DOWN))
        self.wait(0, 24) #写成这种样子的式子
        self.wait(1, 16) #一般被称作“线元”
        self.wait(0, 16) #（空闲）
        self.wait(3, 18) #它展示了各个空间自己的勾股定理应该是什么样的
        self.wait(0, 26) #（空闲）
        self.play(self.change_notice())
        self.wait(1, 8) #之前提到的那些别的例子
        self.wait(1+0-1, 10+19) #也有自己的线元
        self.fade_out(change_notice = True, excepts = [title, title_line])

        ratio_h = 3.5/12
        lines_h = [Line(3.5*LEFT + i*ratio_h*UP, 3.5*RIGHT + i*ratio_h*UP, stroke_width = 1 if i%2 else 2).shift(3*RIGHT + 0.5*DOWN) for i in range(-6, 7)]
        ratio_v = 3.5/12
        lines_v = [Line(1.75*UP + i*ratio_v*RIGHT, 1.75*DOWN + i*ratio_v*RIGHT, stroke_width = 1 if i%2 else 2).shift(3*RIGHT + 0.5*DOWN) for i in range(-12, 13)]
        grid = VGroup(*lines_h, *lines_v)
        label_theta = MTex(r"\theta").scale(0.6).next_to(grid.get_corner(UL), UP, buff = 0.15)
        label_phi = MTex(r"\phi").scale(0.6).next_to(grid.get_corner(DR), RIGHT, buff = 0.15)
        gauge = MTex(r"\mathrm{d}s^2=\mathrm{d}\theta^2 + \sin^2\theta\mathrm{d}\phi^2", tex_to_color_map = {r"\mathrm{d}s": YELLOW}).move_to(2.5*UP)
        surr = SurroundingRectangle(gauge)
        self.play(Write(grid), *[Write(mob, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)) for mob in [label_phi, label_theta, gauge]], ShowCreation(surr))
        self.wait(1, 10) #比如说 一个单位球的线元是这个样子的
        self.wait(0, 21) #（空闲）
        self.wait(2, 20) #这个线元和极坐标的形式很像
        self.wait(1+0-1, 9+19) #但也不完全一样 （空闲）
        self.fade_out(excepts = [title, title_line])

        ratio = 0.5
        lines_h = [Line(3.25*LEFT + i*ratio*UP, 3.25*RIGHT + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = YELLOW if i else WHITE) for i in range(-3, 4)]
        lines_v = [Line(1.75*UP + i*ratio*RIGHT, 1.75*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = YELLOW if i else WHITE) for i in range(-6, 7)]
        lines = VGroup(*lines_h[:3], *lines_h[4:], *lines_v, lines_h[3]).shift(3*RIGHT + 0.5*DOWN)
        label_x = MTex(r"x").scale(0.6).next_to(1.75*UP, UP, buff = 0.15).shift(3*RIGHT + 0.5*DOWN)
        label_y = MTex(r"y").scale(0.6).next_to(3.25*RIGHT, RIGHT, buff = 0.15).shift(3*RIGHT + 0.5*DOWN)
        gauge = MTex(r"\mathrm{d}s^2=(4x^2+1)\mathrm{d}x^2 + (4y^2+1)\mathrm{d}y^2 + 8xy\mathrm{d}x\mathrm{d}y", tex_to_color_map = {r"\mathrm{d}s": YELLOW, (r"\mathrm{d}x", r"\mathrm{d}y"): YELLOW}).scale(0.8).move_to(2.5*UP)
        surr = SurroundingRectangle(gauge)
        indicate = SurroundingRectangle(gauge[-7:], color = YELLOW_E)
        self.fade_in(lines, label_x, label_y, gauge, surr, excepts = [title, title_line]).wait(1, 10) #而抛物面上的线元 是这样的
        self.wait(0, 28) #（空闲）
        self.wait(1, 27) #和之前那些线元不同
        self.play(ShowCreationThenDestruction(indicate), run_time = 2)
        self.wait(0, 27) #这个线元的表达式里出现了交叉项
        self.wait(2, 10) #这表明两条坐标线并不正交
        self.wait(0, 14) #（空闲）
        self.wait(1, 20) #在标准图像里面
        self.wait(2, 16) #其实是在用余弦定理计算线元
        self.wait(0, 24) #（空闲）
        self.remove(self.notice).wait(1)
        
class Patch3_1(FrameScene):
    CONFIG = {
        "for_pr": False,
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        sphere = Sphere(radius=2).rotate(PI, axis = RIGHT)
        ball = TexturedSurface(sphere, "Grid_2.png")
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        camera = self.camera.frame
        camera.set_orientation(Rotation(quadternion))
        camera.add_updater(lambda m, dt: m.increment_theta(-0.05 * dt))

        self.play(ShowCreation(ball), run_time = 2)
        self.wait(1, 10) #比如说 一个单位球的线元是这个样子的
        self.wait(0, 21) #（空闲）
        self.wait(2, 20) #这个线元和极坐标的形式很像
        self.wait(1, 9) #但也不完全一样
        self.wait(0, 19) #（空闲）
        
class Patch3_2(FrameScene):
    CONFIG = {
        "for_pr": False,
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 16.0)}, 
            }
    }
    def construct(self):
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        camera = self.camera.frame
        camera.shift(5.5*OUT).set_orientation(Rotation(quadternion))
        camera.add_updater(lambda m, dt: m.increment_theta(-0.05 * dt))

        lines_x = [ParametricCurve(lambda t: np.array([t, i/2, t**2 + (i/2)**2]), [-np.sqrt(4.5-(i/2)**2), np.sqrt(4.5-(i/2)**2), 0.01], depth_test = True) for i in range(-4, 5)]
        lines_y = [ParametricCurve(lambda t: np.array([i/2, t, t**2 + (i/2)**2]), [-np.sqrt(4.5-(i/2)**2), np.sqrt(4.5-(i/2)**2), 0.01], depth_test = True) for i in range(-4, 5)]
        mesh = VGroup(*lines_x, *lines_y).set_color(YELLOW)
        paraboloid = ParametricSurface(lambda u, v: np.array(u*unit(v) + u**2*OUT), u_range = (0, np.sqrt(4.5)), v_range = (0, TAU), color = BLUE).rotate(PI/6)
        z_axis = Arrow(DOWN, 5*UP, buff = 0, depth_test = True).rotate(PI/2, about_point = ORIGIN, axis = RIGHT)
        axes = VGroup(Arrow(2.5*DOWN, 2.5*UP, buff = 0), Arrow(2.5*LEFT, 2.5*RIGHT, buff = 0), depth_test = True)
        self.add(axes, paraboloid, z_axis, mesh).wait(2, 10) #而抛物面上的线元 是这样的
        self.wait(0, 28) #（空闲）
        self.wait(1, 27) #和之前那些线元不同
        self.wait(2, 27) #这个线元的表达式里出现了交叉项
        self.wait(2, 10) #这表明两条坐标线并不正交
        self.wait(0, 14) #（空闲）
        self.wait(1, 20) #在标准图像里面
        self.wait(2, 16) #其实是在用余弦定理计算线元
        self.wait(0, 24) #（空闲）
        self.wait(1)

class Patch3_3(Scene):
    def construct(self):
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = BLUE if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*LEFT + 2*UP)
        shade = Polygon(7.5*RIGHT + 4.5*UP, 7.5*RIGHT + 4.5*DOWN, 7.5*LEFT + 4.5*DOWN, 7.5*LEFT + 0.05*UP, 0.05*LEFT + 0.05*UP, 0.05*LEFT + 4.5*UP, stroke_color = WHITE, fill_color = BACK, fill_opacity = 1)
        notice = Rectangle(height = 0.7, width = 4, stroke_color = WHITE, fill_color = BLACK, fill_opacity = 1).next_to(0.05*UL, UL, buff = 0)
        gauge = MTex(r"\mathrm{d}s^2=\mathrm{d}x^2+\mathrm{d}y^2", tex_to_color_map = {r"mathrm{d}s": YELLOW, (r"\mathrm{d}x", r"\mathrm{d}y"): BLUE}).scale(0.8).move_to(notice)
        self.add(lines, lines_h[10], shade, notice, gauge)

class Patch3_4(Scene):
    def construct(self):
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*RIGHT + 2*UP + 1.5*DOWN)
        shade = Polygon(7.5*LEFT + 4.5*UP, 7.5*LEFT + 4.5*DOWN, 7.5*RIGHT + 4.5*DOWN, 7.5*RIGHT + 0.05*UP, 0.05*RIGHT + 0.05*UP, 0.05*RIGHT + 4.5*UP, stroke_color = YELLOW_E, fill_color = BACK, fill_opacity = 1)
        notice = Rectangle(height = 0.7, width = 4, stroke_color = YELLOW_E, fill_color = BLACK, fill_opacity = 1).next_to(0.05*UR, UR, buff = 0)
        gauge = MTex(r"\mathrm{d}s^2= \mathrm{d}r^2+{r^2}\mathrm{d}\theta^2", tex_to_color_map = {r"\mathrm{d}s": YELLOW, r"{r^2}": TEAL, (r"\mathrm{d}r", r"\mathrm{d}\theta"): GREEN}).scale(0.8).move_to(notice)
        self.add(lines, lines_h[0], shade, notice, gauge)

class Patch3_5(Scene):
    def construct(self):
        ratio_h = 3.5/12
        lines_h = [Line(3.5*LEFT + i*ratio_h*UP, 3.5*RIGHT + i*ratio_h*UP, stroke_width = 1 if i%2 else 2) for i in range(-6, 7)]
        ratio_v = 3.5/12
        lines_v = [Line(1.75*UP + i*ratio_v*RIGHT, 1.75*DOWN + i*ratio_v*RIGHT, stroke_width = 1 if i%2 else 2) for i in range(-12, 13)]
        grid = VGroup(*lines_h, *lines_v).shift(32/9*LEFT + 2*DOWN)
        shade = Polygon(7.5*RIGHT + 4.5*DOWN, 7.5*RIGHT + 4.5*UP, 7.5*LEFT + 4.5*UP, 7.5*LEFT + 0.05*DOWN, 0.05*LEFT + 0.05*DOWN, 0.05*LEFT + 4.5*DOWN, stroke_color = YELLOW_E, fill_color = BACK, fill_opacity = 1)
        notice = Rectangle(height = 0.7, width = 4, stroke_color = YELLOW_E, fill_color = BLACK, fill_opacity = 1).next_to(0.05*DL, DL, buff = 0)
        gauge = MTex(r"\mathrm{d}s^2=\mathrm{d}\theta^2 + \sin^2\theta\mathrm{d}\phi^2", tex_to_color_map = {r"\mathrm{d}s": YELLOW}).scale(0.8).move_to(notice)
        self.add(grid, shade, notice, gauge)

class Patch3_6(FrameScene):
    def construct(self):
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = YELLOW if i else WHITE) for i in range(-10, 10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, 4*DOWN + i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = YELLOW if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*RIGHT + 2*DOWN)
        shade = Polygon(7.5*LEFT + 4.5*DOWN, 7.5*LEFT + 4.5*UP, 7.5*RIGHT + 4.5*UP, 7.5*RIGHT + 0.05*DOWN, 0.05*RIGHT + 0.05*DOWN, 0.05*RIGHT + 4.5*DOWN, stroke_color = WHITE, fill_color = BACK, fill_opacity = 1)
        notice = Rectangle(height = 0.7, width = 5.5, stroke_color = WHITE, fill_color = BLACK, fill_opacity = 1).next_to(0.05*DR, DR, buff = 0)
        gauge = MTex(r"\mathrm{d}s^2=(4x^2+1)\mathrm{d}x^2 + (4y^2+1)\mathrm{d}y^2 + 8xy\mathrm{d}x\mathrm{d}y", tex_to_color_map = {r"\mathrm{d}s": YELLOW, (r"\mathrm{d}x", r"\mathrm{d}y"): YELLOW}).scale(0.52).move_to(notice)
        self.add(lines, shade, notice, gauge)

class Patch3_7(FrameScene):
    CONFIG = {
        "for_pr": False,
    }
    def construct(self):
        self.frames += 107*30 + 12
        self.notices = [Notice("具体例子", "请　掌握"), 
                        Notice("重要区别", "请　牢记"),
                        Notice("具体例子", "请　掌握").set_stroke(width = 0)]
        self.notice = self.notices[0]
        picture_1 = ImageMobject("Patch3_3.png", height = 8)
        picture_2 = ImageMobject("Patch3_4.png", height = 8)
        picture_3 = ImageMobject("Patch3_5.png", height = 8)
        picture_4 = ImageMobject("Patch3_6.png", height = 8)
        self.play(FadeIn(self.shade), FadeIn(picture_1, 8/9*RIGHT + 0.5*DOWN), self.change_notice())
        self.add(picture_2, self.notice).play(FadeIn(picture_2, 8/9*LEFT + 0.5*DOWN), self.notice.animate.set_stroke(color = BLACK))
        self.play(FadeIn(picture_3, 8/9*RIGHT + 0.5*UP))
        self.play(FadeIn(picture_4, 8/9*LEFT + 0.5*UP))
        self.wait(2+2-4, 1+9) #我们现在看到的这些例子 它们的线元其实都是推导出来的
        self.wait(0, 22) #（空闲）
        self.wait(2, 7) #我们先画出它们的标准图像
        self.wait(1, 28) #再通过标准的勾股定理
        self.wait(1, 17) #推导出线元的形式
        self.wait(0, 18) #（空闲）
        self.wait(1, 27) #但在更一般的空间里面
        self.wait(1, 19) #线元是直接指定的
        self.wait(0, 17) #（空闲）
        self.wait(1, 15) #道理也很简单
        self.wait(1, 23) #一般空间的标准图像
        self.wait(1+0-1, 15+20) #我们不一定画得出来 （空闲）
        position_1 = 8/9*LEFT + 0.5*UP
        position_2 = 8/9*RIGHT + 0.5*UP
        position_3 = 8/9*LEFT + 0.5*DOWN
        position_4 = 8/9*RIGHT + 0.5*DOWN
        self.play(FadeOut(picture_1, position_1), FadeOut(picture_2, position_2), FadeOut(picture_3, position_3), FadeOut(picture_4, position_4), self.change_notice())
        self.remove(self.shade)

class Patch3_8(FrameScene):
    CONFIG = {
        "for_pr": False,
    }
    def construct(self):
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        camera = self.camera.frame
        camera.set_orientation(Rotation(quadternion))
        camera.add_updater(lambda m, dt: m.increment_theta(-0.2 * dt))
        square = ParametricSurface(uv_func = lambda u, v: np.array([u, 0, -v]), u_range = (-2, 2), v_range = (-2, 2), color = [BLUE, GREEN, BLUE]).save_state()
        self.play(ShowCreation(square), run_time = 2)
        self.wait(1)
        def velocity(t: float):
            return 30*(t**2)*(1-t)**2
        def camera_updater(mob: CameraFrame, dt):
            residue = (self.time - 3)/2
            mob.increment_theta(-(PI - 0.8) * dt * velocity(residue))
        def camera_updater_2(mob: CameraFrame, dt):
            residue = abs(self.time - 4)
            mob.increment_theta(-0.3 * residue * dt)
        camera.add_updater(camera_updater).add_updater(camera_updater_2)
        def square_updater(mob: ParametricSurface):
            ratio = smooth((self.time - 3)/2)
            def util(point: np.ndarray):
                base = interpolate(-2, 0, ratio)
                offset = interpolate(0, -2, ratio)
                if point[0] < interpolate(-2, 2, ratio):
                    angle = (interpolate(-2, 2, ratio) - point[0])/4*TAU
                    return np.array([base - 4/TAU*np.sin(angle), 4/TAU*(1 - np.cos(angle)), point[2]])
                else:
                    return point + offset*RIGHT
            mob.restore().apply_function(util).center()
        square.add_updater(square_updater)
        self.wait(2)
        camera.remove_updater(camera_updater).remove_updater(camera_updater_2)
        square.clear_updaters()
        self.wait(1+1+1-5, 29+14+29) #要只是一个方向连在一起 那相当好处理 直接把它粘成圆柱面就可以了
        self.wait(0, 20) #（空闲）

        circle_up = Circle(radius = 4/TAU, color = YELLOW, depth_test = True, stroke_width = 8).shift(2*OUT)
        circle_down = Circle(radius = 4/TAU, color = YELLOW, depth_test = True, stroke_width = 8).shift(2*IN)
        self.play(ShowPassingFlash(circle_up), ShowPassingFlash(circle_down), rate_func = rush_into)
        self.play(ShowPassingFlash(circle_up), ShowPassingFlash(circle_down), rate_func = rush_from)
        self.wait(2+1-2, 12+25) #但要想再把圆柱面的上下粘起来 就只能在四维空间里做了
        self.wait(0, 23) #（空闲）
        self.wait(1, 19) #大家如果不相信的话
        self.wait(2, 9) #可以自己拿一张纸试一试
        self.wait(2, 0) #看看能不能不留下折痕
        self.wait(2, 0) #把它的两组对边都拼在一起
        self.wait(0, 22) #（空闲）
        self.wait(2, 17) #三维空间中最接近这个空间的
        self.wait(1, 23) #是甜甜圈的表面
        self.wait(2, 9) #但它内外的长度也是不一样的
        self.wait(0, 19) #（空闲）
        self.wait(2, 6) #使用甜甜圈来代表这个空间
        self.wait(3, 21) #就如同使用这个扭曲的xy坐标来代表平面一样
        self.wait(2, 0) #应该没有人会真的拿来用吧
        self.wait(2, 9) #到此共177秒

class Patch3_9(FrameScene):
    CONFIG = {
        "for_pr": False,
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 16.0)}, 
            }
    }
    def construct(self):
        quadternion = quaternion_mult(quad(RIGHT, PI/3))
        camera = self.camera.frame
        camera.shift(2*OUT).set_orientation(Rotation(quadternion))
        camera.add_updater(lambda m, dt: m.increment_theta(-0.2 * dt))
        torus = Torus(r1=2, r2=4/TAU, color = [BLUE, GREEN, BLUE])
        self.play(ShowCreation(torus), run_time = 2)
        ring_out = Circle(radius = 2+4/TAU, color = WHITE, depth_test = True, stroke_width = 10)
        ring_in = Circle(radius = 2-4/TAU, color = YELLOW_E, depth_test = True, stroke_width = 10)
        self.wait(0, 17) #三维空间中最接近这个空间的
        self.wait(1, 23) #是甜甜圈的表面
        self.play(ShowCreation(ring_out), ShowCreation(ring_in))
        self.wait(1, 9) #但它内外的长度也是不一样的
        self.wait(0, 19) #（空闲）
        self.wait(2, 6) #使用甜甜圈来代表这个空间
        self.wait(3, 21) #就如同使用这个扭曲的xy坐标来代表平面一样
        self.wait(2, 0) #应该没有人会真的拿来用吧
        self.wait(2, 9) #到此共177秒

class Patch3_10(FrameScene):
    def construct(self):
        ratio = 0.4
        offset_r = 32/9*LEFT + 2*DOWN + 1.5*DOWN
        def func_h_positive(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t - PI/2), 0]) + offset_r
            return util
        def func_h_negative(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t + PI/2), 0]) + offset_r
            return util
        def func_v_positive(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t), 0]) + offset_r
            return util
        def func_v_negative_1(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t - PI), 0]) + offset_r
            return util
        def func_v_negative_2(index: int):
            def util(t: float):
                return np.array([-0.8*t/(PI/6), ratio*index/np.cos(t + PI), 0]) + offset_r
            return util
        lines_h = [ParametricCurve(func_h_negative(i), [-PI+PI/48, -PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = BLUE) for i in range(13, 0, -1)] + [ParametricCurve(func_h_positive(i), [PI/48, PI-PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = BLUE).reverse_points() for i in range(1, 14)]
        lines_v = [ParametricCurve(func_v_negative_2(i), [PI/2+PI/48, PI, PI/144], stroke_width = 1 if i%2 else 2, color = PURPLE_A).append_points(
                    ParametricCurve(func_v_negative_1(i), [-PI, -PI/2-PI/48, PI/144]).get_points()) for i in range(13, 0, -1)] + [ParametricCurve(func_v_positive(i), [-PI/2+PI/48, PI/2-PI/48, PI/144], stroke_width = 1 if i%2 else 2, color = PURPLE_A).reverse_points() for i in range(1, 14)]
        coordinate_right = VGroup(*lines_h, *lines_v, Line(4*LEFT, 4*RIGHT, stroke_width = 2).shift(offset_r), Line(ORIGIN, 4*UP, stroke_width = 2).shift(offset_r), Line(ORIGIN, 4*UP, stroke_width = 2).shift(2.4*RIGHT + offset_r), Line(ORIGIN, 4*UP, stroke_width = 2).shift(2.4*LEFT + offset_r))
        shade = Polygon(7.5*RIGHT + 4.5*DOWN, 7.5*RIGHT + 4.5*UP, 7.5*LEFT + 4.5*UP, 7.5*LEFT + 0.05*DOWN, 0.05*LEFT + 0.05*DOWN, 0.05*LEFT + 4.5*DOWN, stroke_color = YELLOW_E, fill_color = BACK, fill_opacity = 1)
        self.add(coordinate_right, shade)

class Patch3_11(FrameScene):
    CONFIG = {
        "for_pr": False,
    }
    def construct(self):
        picture_4 = ImageMobject("Patch3_10.png", height = 8)
        self.play(FadeIn(picture_4, 8/9*RIGHT + 0.5*UP))
        self.wait(2, 21) #就如同使用这个扭曲的xy坐标来代表平面一样
        self.wait(2, 0) #应该没有人会真的拿来用吧
        self.wait(2, 9) #到此共177秒
        
#################################################################### 

class Summary(FrameScene):

    def construct(self):
        self.notices = [Notice("良心视频", "请　三连"), 
                        Notice("下期预告", "敬请期待"), 
                        Notice("良心up主", "请　关注")]
        self.notice = self.notices[0]

        self.play(Write(self.notice))
        self.wait(0, 25) #非常感谢大家能看到这里
        self.wait(0, 16) #（空闲）

        inner = Rectangle(height = 8, width = 0.1, stroke_width = 0, fill_color = BLACK, fill_opacity = 1)
        line_left = Line(4*UP, 4*DOWN).shift(0.05*LEFT)
        line_right = Line(4*UP, 4*DOWN, color = YELLOW_E).shift(0.05*RIGHT)
        shade = Shade().next_to(3*UP, UP, buff = 0)
        title_left = Title("空间").shift(32/9*LEFT)
        title_right = Title("图像").shift(32/9*RIGHT)
        title_line_left = Line(3*LEFT, 3*RIGHT).shift(32/9*LEFT + 3*UP).save_state().scale(0, min_scale_factor = 0).shift(UP)
        title_line_right = Line(3*LEFT, 3*RIGHT).shift(32/9*RIGHT + 3*UP).save_state().scale(0, min_scale_factor = 0).shift(UP)
        inner.add(line_left, line_right)
        self.play(title_left.shift(UP).animate.shift(DOWN), title_right.shift(UP).animate.shift(DOWN), title_line_left.animate.restore(), title_line_right.animate.restore(), inner.shift(8*UP).animate.shift(8*DOWN))
        picture_1 = ImageMobject(r"Patch4_1.png", height = 8)
        picture_2 = ImageMobject(r"Patch4_2.png", height = 8)
        notice_1 = Text("（爱长成啥样就啥样）", font = "simsun", color = YELLOW).scale(0.4).next_to(title_left.get_corner(DR), UR, buff = 0).shift(0.2*RIGHT)
        notice_2 = Text("（爱画成啥样就啥样）", font = "simsun", color = YELLOW).scale(0.4).next_to(title_right.get_corner(DR), UR, buff = 0).shift(0.2*RIGHT)
        plane = Text(r"[平面]", font = "simsun", color = YELLOW).shift(32/9*LEFT)
        plane.add(SurroundingRectangle(plane))
        self.bring_to_back(picture_1, shade).play(FadeIn(plane, 0.5*DOWN), picture_1.shift(3*UP).animate.shift(3*DOWN), self.notice.animate.set_stroke(color = BLACK), FadeIn(notice_1), FadeIn(notice_2))
        self.bring_to_back(picture_2).play(picture_2.shift(3*UP).animate.shift(3*DOWN))
        self.wait(0, 17) #这期视频我尝试讲了一些理解弯曲空间的基本功
        self.wait(3, 3) #也就是分清“空间”和“空间的图像”
        self.wait(1, 15) #不知道有没有讲清楚
        self.wait(0, 23) #（空闲）

        titleline = TitleLine().save_state().put_start_and_end_on(3*UP, 3*UP)
        self.add(inner, self.notice).play(inner.animate.scale(np.array([150, 1, 1])), titleline.animate.restore(), run_time = 2)
        self.clear().add(inner, self.notice, titleline)
        topics = MTexText(r"·切向量\\·对偶向量\\·度规\\·协变导数\\·李导数\\·微分形式\\·...", alignment = "")
        topics[0:4].shift((topics[4].get_x() - topics[0].get_x())*RIGHT)
        self.play(Write(topics))
        self.wait(1+2+1-4, 15+10+29) #弯曲空间这一话题 还有相当多可以展开的部分 这期视频只是它的冰山一角
        self.wait(0, 18) #（空闲）

        title = Title(r"微分几何")
        self.play(Write(title))
        self.wait(2, 13) #这条路最终会通向一门叫“微分几何”的学科
        self.wait(1, 22) #但在路上的最大收获
        self.wait(1, 28) #可能是完全掌握多元微积分
        self.wait(0, 24) #（空闲）
        self.wait(2, 25) #我想知道大家对这个话题是否感兴趣
        self.wait(2, 3) #我是否应该继续做下去
        self.wait(2, 11) #请大家在评论区留下宝贵的意见
        self.wait(0, 19) #（空闲）

        self.clear().add(self.notice.set_stroke(color = BACK))
        like = Text("", font = 'vanfont').scale(2).shift(3*LEFT)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').scale(2).shift(3*RIGHT)
        sanlian = VGroup(like, coin, star)
        self.play(*[GrowFromCenter(mob) for mob in sanlian])
        self.play(ApplyMethod(sanlian.set_color, "#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian])
        self.wait(0, 15) #如果你看了这期视频觉得有所收获
        self.wait(1, 23) #不妨一键三连支持一下
        self.wait(0, 25) #（空闲）

        rectangle_0 = Rectangle(height = 1, width = 8, color = BLUE, stroke_width = 0, fill_opacity = 1).shift(UP)
        self.play(FadeOut(sanlian), self.change_notice(), FadeIn(rectangle_0, 0.5*DOWN))
        centers_1 = [2*DOWN + 4*LEFT, 2*DOWN + 4*RIGHT]
        rectangles_1 = [rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[0]).set_color(interpolate_color(GREEN, BLUE, 0.5)), rectangle_0.copy().scale(np.array([1/3, 1/2, 0]), about_point = centers_1[1]).set_color(interpolate_color(BLUE, GREEN, 0.5))]
        self.play(TransformFromCopy(rectangle_0, rectangles_1[0]), TransformFromCopy(rectangle_0, rectangles_1[1]))
        last_centers = centers_1
        last_rectangles = rectangles_1
        for i in range(2, 10):
            centers = [*(last_centers-(2*DOWN + 4*LEFT))/3+(2*DOWN + 4*LEFT), *(last_centers-(2*DOWN + 4*RIGHT))/3+(2*DOWN + 4*RIGHT)]
            rectangles = [last_rectangles[j//2].copy().scale(np.array([1/3, 1/2, 0]), about_point = centers[j]).set_color(interpolate_color(GREEN, BLUE, 1/2**i)) for j in range(2**i)]
            self.play(*[TransformFromCopy(last_rectangles[j//2], rectangles[j]) for j in range(2**i)])
            last_centers = centers
            last_rectangles = rectangles
        self.wait(2+1+2+0+4-10, 16+20+2+17+16) #下期视频我打算讲一讲康托集 它是最简单的分形 也是性质非常丰富的数学对象 （空闲）某种意义上 康托集甚至要比实数更加符合我们的直观
        self.wait(3, 0) #至少比十进制小数更加符合我们的直观
        self.wait(0, 17) #（空闲）
        self.wait(4+0+1-3, 2+26+29) #下期视频 我们就从0.99999......和1的关系开始 （空闲）
        self.fade_out()
        
        painting = StarrySky()
        star = painting.star
        self.clear().play(FadeIn(painting, lag_ratio = 0.01, run_time = 2), self.change_notice())
        # self.wait(0, 0) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, 0.5*UP), FadeIn(text_name, 0.5*UP))
        self.wait(1, 6) #而我 就像我的名字一样

        self.play(FadeOut(painting.others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star.shift, DOWN))
        self.wait(1, 2) #想要把天上的星星垂下来

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
        self.wait(1+0-2, 25+18) #变成指引前路的火光 （空闲）
        
        self.remove(star, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.wait(2, 2) #我是乐正垂星 我们下期视频再见

        self.wait(3, 22)
        self.fade_out(end = True)
        self.wait(3) #到此共80秒
        
class Patch4_1(FrameScene):
    def construct(self):
        ratio = 0.4
        lines_h = [Line(LEFT_SIDE + i*ratio*UP, RIGHT_SIDE + i*ratio*UP, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(10)]
        lines_v = [Line(4*UP + i*ratio*RIGHT, i*ratio*RIGHT, stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(-20, 20)]
        lines = VGroup(*lines_h, *lines_v).shift(32/9*RIGHT + 1.5*UP + 1.25*DOWN)
        shade = Polygon(7.5*LEFT + 4.5*UP, 7.5*LEFT + 4.5*DOWN, 7.5*RIGHT + 4.5*DOWN, 7.5*RIGHT, ORIGIN, 4.5*UP, stroke_color = YELLOW_E, fill_color = BACK, fill_opacity = 1)
        self.add(lines, lines_h[0], shade)

class Patch4_2(FrameScene):
    def construct(self):
        ratio = 0.4
        circles = [Circle(radius = i*ratio, stroke_width = 1 if i%2 else 2, color = GREEN, n_components = 24) for i in range(1, 25)]
        rays = [Line(ORIGIN, 8.5*unit(i*TAU/24), stroke_width = 1 if i%2 else 2, color = GREEN if i else WHITE) for i in range(24)]
        radar = VGroup(*circles, *rays).shift(32/9*RIGHT + 1.5*DOWN)
        shade = Polygon(7.5*LEFT + 4.5*UP, 7.5*LEFT + 4.5*DOWN, 7.5*RIGHT + 4.5*DOWN, 7.5*RIGHT + 3*DOWN, 3*DOWN, 4.5*UP, stroke_color = YELLOW_E, fill_color = BACK, fill_opacity = 1)
        self.add(radar, shade)

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]