from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

def boost(angle: float):
    return np.array([np.cosh(angle), np.sinh(angle), 0])

def iboost(angle: float):
    return np.array([np.sinh(angle), np.cosh(angle), 0]) 

class Toy_1(FrameScene):
    CONFIG = {
        "for_pr": False,
        "camera_config": {
            "frame_config": {"frame_shape": (8.0, 8.0)}, 
            }
    }
    def construct(self):
        unit_angle = np.arcsinh(1)
        hyperbola = ParametricCurve(boost, [-np.arcsinh(4), np.arcsinh(4), np.arcsinh(4)/100])
        colors = [TEAL, PURPLE]
        hyperbolas = VGroup(*[hyperbola.copy().rotate(i*PI/2, about_point = ORIGIN).set_color(colors[i%2]) for i in range(4)])
        
        points_right = [Dot(boost(i*unit_angle), offset = i) for i in [-4, -2, 0, 2, 4]]
        points_up = [Dot(iboost(i*unit_angle), offset = i) for i in [-5, -3, -1, 1, 3, 5]]
        points_left = [Dot(-boost(i*unit_angle), offset = i) for i in [-4, -2, 0, 2, 4]]
        points_down = [Dot(-iboost(i*unit_angle), offset = i) for i in [-5, -3, -1, 1, 3, 5]]
        self.add(hyperbolas, *points_right, *points_up, *points_left, *points_down)
        
        TEAL_G, PURPLE_G = interpolate_color(TEAL, GREY, 0.5), interpolate_color(PURPLE, GREY, 0.5)
        lines_right = []
        for point in points_right:
            offset = point.offset
            color = interpolate_color(TEAL_G, BLACK, abs(offset)/4)
            line = Line(iboost((offset+1)*unit_angle), -iboost((offset-1)*unit_angle), color = color).set_stroke(width = 4-abs(offset))
            line.offset = offset
            lines_right.append(line)
        lines_up = []
        for point in points_up:
            offset = point.offset
            color = interpolate_color(PURPLE_G, BLACK, abs(offset)/4)
            line = Line(boost((offset+1)*unit_angle), -boost((offset-1)*unit_angle), color = color).set_stroke(width = 4-abs(offset))
            line.offset = offset
            lines_up.append(line)
        lines_left = []
        for point in points_left:
            offset = point.offset
            color = interpolate_color(TEAL_G, BLACK, abs(offset)/4)
            line = Line(-iboost((offset+1)*unit_angle), iboost((offset-1)*unit_angle), color = color).set_stroke(width = 4-abs(offset))
            line.offset = offset
            lines_left.append(line)
        lines_down = []
        for point in points_down:
            offset = point.offset
            color = interpolate_color(PURPLE_G, BLACK, abs(offset)/4)
            line = Line(-boost((offset+1)*unit_angle), boost((offset-1)*unit_angle), color = color).set_stroke(width = 4-abs(offset))
            line.offset = offset
            lines_down.append(line)
        all_lines = VGroup(*lines_right, *lines_up, *lines_left, *lines_down)#
        all_lines.submobjects.sort(key = lambda t: -abs(t.offset))
        all_lines.assemble_family()
        self.bring_to_back(all_lines)

        alpha = ValueTracker(0)
        def point_updater_right(mob: Dot):
            offset = alpha.get_value() + mob.offset
            mob.move_to(boost(offset*unit_angle))
        for point in points_right:
            point.add_updater(point_updater_right)
        def point_updater_up(mob: Dot):
            offset = alpha.get_value() + mob.offset
            mob.move_to(iboost(offset*unit_angle))
        for point in points_up:
            point.add_updater(point_updater_up)
        def point_updater_left(mob: Dot):
            offset = alpha.get_value() + mob.offset
            mob.move_to(-boost(offset*unit_angle))
        for point in points_left:
            point.add_updater(point_updater_left)
        def point_updater_down(mob: Dot):
            offset = alpha.get_value() + mob.offset
            mob.move_to(-iboost(offset*unit_angle))
        for point in points_down:
            point.add_updater(point_updater_down)
        
        def line_updater_right(mob: Line):
            offset = alpha.get_value() + mob.offset
            mob.put_start_and_end_on(iboost((offset+1)*unit_angle), -iboost((offset-1)*unit_angle))
            if abs(offset) < 4:
                mob.set_stroke(color = interpolate_color(TEAL_G, BLACK, abs(offset)/4), width = 4-abs(offset), opacity = 1)
            else:
                mob.set_opacity(0)
        for line in lines_right:
            line.add_updater(line_updater_right)
        def line_updater_up(mob: Line):
            offset = alpha.get_value() + mob.offset
            mob.put_start_and_end_on(boost((offset+1)*unit_angle), -boost((offset-1)*unit_angle))
            if abs(offset) < 4:
                mob.set_stroke(color = interpolate_color(PURPLE_G, BLACK, abs(offset)/4), width = 4-abs(offset), opacity = 1)
            else:
                mob.set_opacity(0)
        for line in lines_up:
            line.add_updater(line_updater_up)
        def line_updater_left(mob: Line):
            offset = alpha.get_value() + mob.offset
            mob.put_start_and_end_on(-iboost((offset+1)*unit_angle), iboost((offset-1)*unit_angle))
            if abs(offset) < 4:
                mob.set_stroke(color = interpolate_color(TEAL_G, BLACK, abs(offset)/4), width = 4-abs(offset), opacity = 1)
            else:
                mob.set_opacity(0)
        for line in lines_left:
            line.add_updater(line_updater_left)
        def line_updater_down(mob: Line):
            offset = alpha.get_value() + mob.offset
            mob.put_start_and_end_on(-boost((offset+1)*unit_angle), boost((offset-1)*unit_angle))
            if abs(offset) < 4:
                mob.set_stroke(color = interpolate_color(PURPLE_G, BLACK, abs(offset)/4), width = 4-abs(offset), opacity = 1)
            else:
                mob.set_opacity(0)
        for line in lines_down:
            line.add_updater(line_updater_down)

        def line_updater_all(mob: VGroup):
            for submob in mob.submobjects:
                submob.update()
            mob.submobjects.sort(key = lambda t: -abs(t.offset + alpha.get_value()))
            mob.assemble_family()
        all_lines.add_updater(line_updater_all)
        
        self.play(alpha.animate.set_value(2), run_time = 4, rate_func = linear)
    
    def update_mobjects(self, dt: float) -> None:
        for mobject in self.mobjects:
            mobject.update(dt, recurse = False)

"""
        def line_updater_right(mob: Line):
            offset = alpha.get_value() + mob.offset
            color = interpolate_color(TEAL_G, BLACK, abs(offset)/4)
            line.put_start_and_end_on(iboost((offset+1)*unit_angle), -iboost((offset-1)*unit_angle)).set_stroke(color = color, width = 4-abs(offset))
        for line in lines_right:
            line.the_updater = line_updater_right

        def line_updater_all(mob: VGroup):
            for submob in mob.submobjects:
                if hasattr(submob, "the_updater"):
                    submob.the_updater(submob)
                    print(submob.offset)
            mob.submobjects.sort(key = lambda t: -abs(t.offset))
            mob.assemble_family()
        all_lines.add_updater(line_updater_all)

        def line_updater_right(mob: Line):
            offset = alpha.get_value() + mob.offset
            color = interpolate_color(TEAL_G, BLACK, abs(offset)/4)
            line.put_start_and_end_on(iboost((offset+1)*unit_angle), -iboost((offset-1)*unit_angle)).set_stroke(color = color, width = 4-abs(offset))
        for line in lines_right:
            line.add_updater(line_updater_right)

        def line_updater_all(mob: VGroup):
            for submob in mob.submobjects:
                submob.update()
            mob.submobjects.sort(key = lambda t: -abs(t.offset))
            mob.assemble_family()
        all_lines.add_updater(line_updater_all)
"""

class Trailer(Scene):
    #1728*1080

    def construct(self):
        frac = MTex(r"\mathbf{\sqrt{2}={1}+\cfrac1{2+\cfrac1{2+\cfrac1{\cdots}}}}", tex_to_color_map = {r"{1}": GOLD, r"2": ORANGE, r"\sqrt{2}": YELLOW}).scale(1.25).set_stroke(width = 8, color = BLACK, background = True)
        pell = MTex(r"\mathbf{{m}^2-{2}n^2=1}", tex_to_color_map = {r"{2}": YELLOW, (r"{m}", r"n"): TEAL}).scale(1.5).set_stroke(width = 8, color = BLACK, background = True)
        GREEN_G = interpolate_color(GREEN, BLACK, 0.5)
        ORANGE_G = interpolate_color(ORANGE, BLACK, 0.5)
        TEAL_G = interpolate_color(TEAL, BLACK, 0.5)
        #outer = Circle(radius = 3, color = GREEN_G, fill_opacity = 1, stroke_width = 0)
        radius = 2
        width = 0.5
        angle = 5*PI/6
        outer_l = Arc(angle, PI, radius = radius + width, color = ORANGE_G, fill_opacity = 1, stroke_width = 0, n_components = 24)
        outer_r = Arc(angle, -PI, radius = radius + width, color = TEAL_G, fill_opacity = 1, stroke_width = 0, n_components = 24)
        inner = Circle(radius = radius - width, color = BLACK, fill_opacity = 1, stroke_width = 0)
        triangle = Polyline(2*width*LEFT + 1.5*width*DOWN, 1.5*width*UP, 2*width*RIGHT + 1.5*width*DOWN, fill_color = GREEN_G, fill_opacity = 1, stroke_width = 40, stroke_color = BLACK, draw_stroke_behind_fill = True)
        triangle.shift(radius*RIGHT).insert_n_curves(18).apply_function(lambda t: t[0]*unit(t[1]/3))
        # triangle = Polyline(1.5*unit(-1/6), 2.5*unit(1/6), 3.5*unit(-1/6), fill_color = GREEN_G, fill_opacity = 1, stroke_width = 40, stroke_color = BLACK, draw_stroke_behind_fill = True)
        # triangle#.shift(radius*RIGHT).insert_n_curves(18).apply_function(lambda t: t[0]*unit(t[1]/3))
        # triangle = Polyline(2.5*unit(1/6) + np.sqrt(2)*unit(1/6-PI/4), 2.5*unit(1/6), 2.5*unit(1/6) - np.sqrt(2)*unit(1/6+PI/4), fill_color = GREEN_G, fill_opacity = 1, stroke_width = 40, stroke_color = BLACK, draw_stroke_behind_fill = True)
        # triangle#.shift(radius*RIGHT).insert_n_curves(18).apply_function(lambda t: t[0]*unit(t[1]/3))
        triangle_l = triangle.copy().rotate(angle, about_point = ORIGIN).set_fill(color = TEAL_G)
        triangle_r = triangle_l.copy().rotate(PI, about_point = ORIGIN).set_fill(color = ORANGE_G)

        # text_r = Text(r"连分数", font = "FZDaHei-B02S", color = ORANGE).scale(2).arrange(DOWN).shift(UP + 5.5*RIGHT)
        # text_l = Text(r"佩尔方程", font = "FZDaHei-B02S", color = BLUE).scale(2).arrange(DOWN).shift(0.5*DOWN + 5.5*LEFT)
        # self.add(outer_l, outer_r, inner, triangle_l, triangle_r, frac.shift(UR + 0.5*UP + 0*RIGHT), pell.shift(2*LEFT + 1.5*DOWN), text_l, text_r)# 
        # self.camera.frame.shift(0.5*RIGHT)

        text_r = Text(r"连分数", font = "FZDaHei-B02S", color = ORANGE).scale(2).shift(2.5*DOWN + 4*LEFT)
        text_l = Text(r"佩尔方程", font = "FZDaHei-B02S", color = TEAL).scale(2).shift(3*UP + 3.5*RIGHT)
        self.add(outer_l, outer_r, inner, triangle_l, triangle_r, frac.shift(1*DOWN + 2*LEFT), pell.shift(2*RIGHT + 1*UP), text_l, text_r)# 
        
            
#################################################################### 

class Template(FrameScene):
    def construct(self):
        self.notices = [Notice("示例文本", "请　模仿")]
        self.notice = self.notices[0]