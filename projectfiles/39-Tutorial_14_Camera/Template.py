from manimlib import *
import numpy as np

class MoveCameraExample(Scene):
    def setup(self):
        # 初始化坐标系
        self.plane = NumberPlane()
        self.plane.add_coordinate_labels()
        self.add(self.plane)

    

    def construct(self):
        def t_func(t):
        # 螺线参数方程
            a, b = 3, 3
            return np.array([
                a * np.cos(t) / t,
                b * np.sin(t) / t,
                0
            ])

        # 获取相机帧的引用
        frame = self.camera.frame
        # 创建螺线
        curve = ParametricCurve(t_func, t_range=[0.1, 200, 0.05], color=YELLOW)
        self.add(curve)
        self.play(
            curve.animate.set_stroke(width=0.3),       # 设置螺线粗细
            frame.animate.set_width(2).rotate(PI / 2), # 旋转缩放相机帧
            run_time=3
        )
        self.wait(0.5)

class ReorientCameraExample(Scene):
    def setup(self):
        # 初始化场景
        axes = ThreeDAxes()
        self.add(axes)
        sphere = Sphere().move_to(axes.coords_to_point(3, 2, 2))
        self.add(sphere)

    def construct(self) -> None:
        # 获取相机帧的引用
        camera = self.camera.frame
        self.wait()
        # 使用四元数旋转（欧拉旋转经常会检测到万向节锁死）
        self.play(camera.animate.set_orientation(Rotation([0.8, 0.2, 0.1, 0.9])))
        self.wait()

class Test1(Scene):
    def setup(self):
        # 初始化场景
        axes = ThreeDAxes(z_range = np.array([-20.0, 20.0, 1.0]))
        self.add(axes)
        sphere = Sphere().move_to(axes.coords_to_point(3, 2, 2))
        self.add(sphere)

    def construct(self) -> None:
        # 获取相机帧的引用
        camera = self.camera.frame
        self.wait()
        # 使用四元数旋转（欧拉旋转经常会检测到万向节锁死）
        self.play(camera.animate.shift(UP))
        self.wait()
        self.play(camera.animate.shift(16*IN))
        self.wait()

class Test2(Scene):
    CONFIG = {
        "camera_config": {"frame_config": {"focal_dist_to_height": 1}}
    }
    def setup(self):
        # 初始化场景
        axes = ThreeDAxes(z_range = np.array([-20.0, 20.0, 1.0]))
        self.add(axes)
        sphere = Sphere().move_to(axes.coords_to_point(3, 2, 2))
        self.add(sphere)

    def construct(self) -> None:
        # 获取相机帧的引用
        camera = self.camera.frame
        self.wait()
        # 使用四元数旋转（欧拉旋转经常会检测到万向节锁死）
        self.play(camera.animate.shift(UP))
        self.wait()
        self.play(camera.animate.shift(8*IN))
        self.wait()

def unit(angle: float):
    return np.array([np.cos(angle), np.sin(angle), 0])

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

class Test3(Scene):
    def setup(self):
        # 初始化场景
        axes = ThreeDAxes(z_range = np.array([-20.0, 20.0, 1.0]))
        # self.add(axes)
        

    def construct(self) -> None:
        # 获取相机帧的引用
        rec_left = Rectangle(height = 8, width = 8, fill_color = GREEN, fill_opacity = 1, stroke_width = 0).shift(4*LEFT)
        rec_right = Rectangle(height = 8, width = 8, fill_color = BLUE, fill_opacity = 1, stroke_width = 0).shift(4*RIGHT)
        line_before = Line(2*UP+RIGHT, 2*DOWN+RIGHT)
        self.add(rec_left, rec_right, line_before)
        camera = self.camera.frame
        self.wait()
        # 使用四元数旋转（欧拉旋转经常会检测到万向节锁死）
        quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, PI/8))
        self.play(camera.animate.shift(3*OUT+2*RIGHT+2*DOWN).set_orientation(Rotation(quadternion)), run_time = 3)
        # self.play(camera.animate.set_orientation(Rotation(quad(IN, 0))), run_time = 3)
        # rec_behind = Rectangle(height = 2, width = 2, fill_color = RED, fill_opacity = 1, stroke_width = 0).shift(2*LEFT+IN)
        # self.add(rec_behind).wait() #manim的遮挡关系按图层算，不按景深算
        self.play(Rotate(rec_left, PI/2, UP, about_point = ORIGIN), run_time = 2)
        self.wait()
        point = Sphere(radius = 0.08, color = RED).shift(2*RIGHT+2*OUT)
        self.play(ShowCreation(point))
        self.wait()
        line = Line(3*OUT+1*UP, 6*RIGHT+2*DOWN)
        self.add(line, point).play(ShowCreation(line))
        self.wait()

class Test4(Scene):

    def construct(self) -> None:
        # 获取相机帧的引用
        rec_left = Rectangle(height = 8, width = 8, fill_color = GREEN, fill_opacity = 1, stroke_width = 0).shift(4*LEFT)
        rec_right = Rectangle(height = 8, width = 8, fill_color = BLUE, fill_opacity = 1, stroke_width = 0).shift(4*RIGHT)
        notice = VGroup(Text("示例", font = "simsun", is_fixed_in_frame = True).shift(2.9*UP + 5.8*RIGHT))
        notice_phony = VMobject(stroke_width = 0, fill_opacity = 1, is_fixed_in_frame = True).set_points(notice.get_all_points())
        self.add(rec_left, rec_right, notice_phony)
        camera = self.camera.frame
        self.wait()
        quadternion = quaternion_mult(quad(RIGHT, PI/2), quad(UP, PI/6))
        self.play(camera.animate.shift(2*OUT+2*RIGHT+2*DOWN).set_orientation(Rotation(quadternion)).set_focal_distance(8), run_time = 3)
        self.play(Rotate(rec_left, PI/2, UP, about_point = ORIGIN), run_time = 2)
        self.wait()
        point = Sphere(radius = 0.08, color = RED).shift(2*RIGHT+2*OUT)
        self.play(ShowCreation(point))
        self.wait()
        line = Line(3*OUT+1*UP, 6*RIGHT+2*DOWN)
        self.add(line, point).play(ShowCreation(line))
        self.wait()

class Template(Scene):
    def construct(self):

        camera = self.camera
        frame = camera.frame

        print(camera.get_frame_center())

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)