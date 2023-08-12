from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

def curve_interpolate(start: np.ndarray, end: np.ndarray, alpha: float, angle: float):
    diff = 0.5*(end - start)
    center = start + diff
    if not np.isclose(angle%TAU, np.pi):
        center += np.cross(OUT, diff) / math.tan(angle / 2)
    rot_matrix_T = rotation_matrix_transpose(alpha * angle, OUT)
    return center + np.dot(start - center, rot_matrix_T)

# class Comb(Homotopy):
#     CONFIG = {
#         "run_time": 3,
#     }

#     def __init__(self, mobject, **kwargs):
#         digest_config(self, kwargs, locals())
#         def homotopy(x, y, z, t):
            
#             alpha = x/6
#             beta = (y + 2.75)/10
#             number = 12
#             ratio = 0.5
#             rays_length = 10
#             offset = 2.75*DOWN
#             breadth = ratio*number
#             if alpha < 0:
#                 start_line = Line(ORIGIN, rays_length*unit(interpolate(PI/2, -PI, t))).shift((1-t)**2*breadth*unit(-PI/2*t) + (1-t)*offset)
#                 middle_line = Line(ORIGIN, rays_length*unit(interpolate(PI/2, 0, t))).shift((1-t)**2*breadth*(np.tan(t*PI/2))*unit(PI/2-PI/2*t) + (1-t)*offset)
#                 line = VMobject().set_points(path_along_arc(PI*t)(start_line.get_points(), middle_line.get_points(), (alpha + 1)))
#                 return interpolate(line.get_start(), line.get_end(), beta)
#             else:
#                 middle_line = Line(ORIGIN, rays_length*unit(interpolate(PI/2, 0, t))).shift((1-t)**2*breadth*(np.tan(t*PI/2))*unit(PI/2-PI/2*t) + (1-t)*offset)
#                 end_line = Line(ORIGIN, rays_length*unit(interpolate(PI/2, PI, t))).shift((1-t)**2*breadth*unit(PI-PI/2*t) + (1-t)*offset)
#                 line = VMobject().set_points(path_along_arc(PI*t)(middle_line.get_points(), end_line.get_points(), alpha))
#                 return interpolate(line.get_start(), line.get_end(), beta)
                
#         super().__init__(homotopy, mobject, **kwargs)

class Comb(Homotopy):
    CONFIG = {
        "run_time": 3,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs, locals())
        def homotopy(x, y, z, t):
            
            alpha = x/6
            beta = (y + 2.75)/10
            number = 12
            ratio = 0.5
            rays_length = 10
            offset = 2.75*DOWN
            breadth = ratio*number
            if alpha < 0:
                start_point = interpolate(ORIGIN, rays_length*unit(interpolate(PI/2, -PI, t)), beta) + (1-t)**2*breadth*unit(-PI/2*t) + (1-t)*offset
                middle_point = interpolate(ORIGIN, rays_length*unit(interpolate(PI/2, 0, t)), beta) + (1-t)**2*breadth*(np.tan(t*PI/2))*unit(PI/2-PI/2*t) + (1-t)*offset
                return curve_interpolate(start_point, middle_point, (alpha + 1), PI*t)
            else:
                middle_point = interpolate(ORIGIN, rays_length*unit(interpolate(PI/2, 0, t)), beta) + (1-t)**2*breadth*(np.tan(t*PI/2))*unit(PI/2-PI/2*t) + (1-t)*offset
                end_point = interpolate(ORIGIN, rays_length*unit(interpolate(PI/2, PI, t)), beta) + (1-t)**2*breadth*unit(PI-PI/2*t) + (1-t)*offset
                return curve_interpolate(middle_point, end_point, alpha, PI*t)
                
        super().__init__(homotopy, mobject, **kwargs)

class Test1(Scene):
    def construct(self):
        notice = Notice("正确答案", "请勿惊讶")
        offset = 2.75*DOWN
        ratio = 0.5
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
        self.add(new_coordinate, coordinate_right, notice).play(Comb(new_coordinate), Comb(coordinate_right))
        
class Patch2_1(FrameScene):
    def construct(self):
        notice = Notice("正确答案", "请勿惊讶")
        offset = 2.75*DOWN
        ratio = 0.5
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
        self.add(new_coordinate, coordinate_right, notice).play(Comb(new_coordinate), Comb(coordinate_right))

#################################################################### 
        
class SurfaceExample(ThreeDScene):
    def construct(self):
        surface_text = Text("For 3d scenes, try using surfaces")
        surface_text.fix_in_frame()
        surface_text.to_edge(UP)
        self.add(surface_text)
        self.wait(0.1)

        torus1 = Torus(r1=1, r2=1)
        torus2 = Torus(r1=3, r2=1)
        sphere = Sphere(radius=3, resolution=torus1.resolution)
        # You can texture a surface with up to two images, which will
        # be interpreted as the side towards the light, and away from
        # the light.  These can be either urls, or paths to a local file
        # in whatever you've set as the image directory in
        # the custom_config.yml file

        # day_texture = "EarthTextureMap"
        # night_texture = "NightEarthTextureMap"
        # day_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Whole_world_-_land_and_oceans.jpg/1280px-Whole_world_-_land_and_oceans.jpg"
        # night_texture = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/The_earth_at_night.jpg/1280px-The_earth_at_night.jpg"
        day_texture = "earth_day.jpg"
        night_texture = "earth_night.jpg"

        surfaces = [
            TexturedSurface(surface, day_texture, night_texture)
            for surface in [sphere, torus1, torus2]
        ]

        for mob in surfaces:
            mob.shift(IN)
            mob.mesh = SurfaceMesh(mob)
            mob.mesh.set_stroke(BLUE, 1, opacity=0.5)

        surface = surfaces[0]

        self.play(
            FadeIn(surface),
            ShowCreation(surface.mesh, lag_ratio=0.01, run_time=3),
        )
        for mob in surfaces:
            mob.add(mob.mesh)
        surface.save_state()
        self.play(Rotate(surface, PI / 2), run_time=2)
        for mob in surfaces[1:]:
            mob.rotate(PI / 2)

        self.play(
            Transform(surface, surfaces[1]),
            run_time=3
        )

        self.play(
            Transform(surface, surfaces[2]),
            # Move camera frame during the transition
            # self.frame.animate.increment_phi(-10 * DEGREES),
            self.camera.frame.animate.increment_phi(-10 * DEGREES),
            # self.frame.animate.increment_theta(-20 * DEGREES),
            self.camera.frame.animate.increment_theta(-20 * DEGREES),
            run_time=3
        )
        # Add ambient rotation
        # self.frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))
        self.camera.frame.add_updater(lambda m, dt: m.increment_theta(-0.1 * dt))

        # Play around with where the light is
        light_text = Text("You can move around the light source")
        light_text.move_to(surface_text)
        light_text.fix_in_frame()

        self.play(FadeTransform(surface_text, light_text))
        light = self.camera.light_source
        self.add(light)
        light.save_state()
        self.play(light.animate.move_to(3 * IN), run_time=5)
        self.play(light.animate.shift(10 * OUT), run_time=5)

        drag_text = Text("Try moving the mouse while pressing d or f")
        drag_text.move_to(light_text)
        drag_text.fix_in_frame()

        self.play(FadeTransform(light_text, drag_text))
        self.wait()

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

class Test2(FrameScene):
    def construct(self):
        sphere = Sphere(radius=3).rotate(PI, axis = RIGHT)
        # sphere.submobjects = sphere.submobjects[::-1]
        day_texture = "earth_day_grid.jpg"
        night_texture = "earth_night.jpg"
        ball = TexturedSurface(sphere, "grid_2.png")
        texture = TexturedSurface(sphere, day_texture).rotate(PI, axis = RIGHT)
        mesh = SurfaceMesh(sphere, resolution = (25, 13))
        quadternion = quaternion_mult(quad(RIGHT, PI/2))
        quadternion_2 = quaternion_mult(quad(RIGHT, -PI/12), quad(RIGHT, PI/2))
        camera = self.camera.frame
        camera.set_orientation(Rotation(quadternion))

        self.play(ShowCreation(ball), run_time = 3)
        self.wait()
        self.play(camera.animate.set_orientation(Rotation(quadternion_2)))
        self.play(ShowCreation(texture), Uncreate(ball), run_time = 3)
        self.wait()
        # self.play(ShowCreation(mesh), run_time = 3)
        # self.wait()

class Grid_1(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (16.0, 8.0)}, 
            }
    }
    def construct(self):
        ratio_h = 2/3
        lines_h = [Line(8*LEFT + i*ratio_h*UP, 8*RIGHT + i*ratio_h*UP, stroke_width = 2 if i%2 else 4) for i in range(-6, 7)]
        ratio_v = 2/3
        n = 600
        def width(t: float):
            return [100] + [t/np.sin(i/n*PI) for i in range(1, n)] + [100]
        lines_v = [Line(4*UP + i*ratio_v*RIGHT, 4*DOWN + i*ratio_v*RIGHT, stroke_width = width(2) if i%2 else width(4)).insert_n_curves(n-1) for i in range(-12, 13)]
        grid = VGroup(*lines_h, *lines_v)
        self.add(grid)

class Grid_2(FrameScene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (16.0, 8.0)}, 
            }
    }
    def construct(self):
        ratio_h = 2/3
        lines_h = [Line(8*LEFT + i*ratio_h*UP, 8*RIGHT + i*ratio_h*UP, stroke_width = 2 if i%2 else 4) for i in range(-6, 7)]
        ratio_v = 2/3
        n = 600
        def width(t: float):
            return [100] + [t/np.sin(i/n*PI) for i in range(1, n)] + [100]
        lines_v = [Line(4*UP + i*ratio_v*RIGHT, 4*DOWN + i*ratio_v*RIGHT, stroke_width = width(2) if i%2 else width(4)).insert_n_curves(n-1) for i in range(-12, 13)]
        grid = VGroup(*lines_h, *lines_v)
        self.add(grid)

class Trailer(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (2*FRAME_WIDTH, 2*FRAME_HEIGHT)}, 
            }
    }
    def construct(self):
        ratio = 2
        lines_h = [Line(np.sqrt(max(10000-(i*ratio)**2, 0))*LEFT + i*ratio*UP, np.sqrt(max(10000-(i*ratio)**2, 0))*RIGHT + i*ratio*UP, stroke_width = 5*np.exp(-i**2/100) if i%4 else 10*np.exp(-i**2/100), color = WHITE).insert_n_curves(199) for i in range(-100, 101)]
        lines_v = [Line(np.sqrt(max(10000-(i*ratio)**2, 0))*UP + i*ratio*RIGHT, 15*DOWN + i*ratio*RIGHT, stroke_width = 5*np.exp(-i**2/100) if i%4 else 10*np.exp(-i**2/100), color = WHITE).insert_n_curves(199) for i in range(-100, 101)]
        lines = VGroup(*lines_h, *lines_v)
        earth = TexturedSurface(Sphere(radius=3), "earth_day.jpg").shift(2*OUT)
        lines.apply_function(lambda t: t + 3*np.exp(-get_norm(t)**2/20)*IN)
        quadternion = quaternion_mult(quad(RIGHT, PI/2 - PI/12))
        camera = self.camera.frame
        camera.shift(2*OUT).set_orientation(Rotation(quadternion))
        text = Text(r"弯曲空间", font = "FZDaHei-B02S", stroke_width = 10, stroke_color = BLACK, fill_color = WHITE).set_style(stroke_background = True).fix_in_frame().scale(3)
        text[0].move_to(4*LEFT + UL)
        text[1].move_to(4*LEFT + UR)
        text[2].move_to(4*LEFT + DL)
        text[3].move_to(4*LEFT + DR)
        self.add(lines, earth, text)
        
class Cover(Scene):
    CONFIG = {
        "camera_config": {
            "frame_config": {"frame_shape": (2*FRAME_WIDTH, 2*FRAME_HEIGHT)}, 
            }
    }
    def construct(self):
        ratio = 2
        lines_h = [Line(np.sqrt(max(10000-(i*ratio)**2, 0))*LEFT + i*ratio*UP, np.sqrt(max(10000-(i*ratio)**2, 0))*RIGHT + i*ratio*UP, stroke_width = 5*np.exp(-i**2/100) if i%4 else 10*np.exp(-i**2/100), color = WHITE).insert_n_curves(199) for i in range(-100, 101)]
        lines_v = [Line(np.sqrt(max(10000-(i*ratio)**2, 0))*UP + i*ratio*RIGHT, 15*DOWN + i*ratio*RIGHT, stroke_width = 5*np.exp(-i**2/100) if i%4 else 10*np.exp(-i**2/100), color = WHITE).insert_n_curves(199) for i in range(-100, 101)]
        lines = VGroup(*lines_h, *lines_v)
        earth = TexturedSurface(Sphere(radius=3), "earth_day.jpg").shift(2*OUT)
        lines.apply_function(lambda t: t + 3*np.exp(-get_norm(t)**2/20)*IN)
        quadternion = quaternion_mult(quad(RIGHT, PI/2 - PI/12))
        camera = self.camera.frame
        camera.shift(2*OUT).set_orientation(Rotation(quadternion))
        text = Text(r"弯曲空间", font = "FZDaHei-B02S", stroke_width = 10, stroke_color = BLACK, fill_color = WHITE).set_style(stroke_background = True).fix_in_frame().scale(3)
        text[0].move_to(4*LEFT + UL)
        text[1].move_to(4*LEFT + UR)
        text[2].move_to(4*LEFT + DL)
        text[3].move_to(4*LEFT + DR)
        self.add(lines, earth, text)

#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]