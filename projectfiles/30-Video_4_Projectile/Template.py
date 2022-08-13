from manimlib import *
import numpy as np

OMEGA = np.array([math.sqrt(3)/2, -1/2, 0])

def quadratic(a,b,c):
    return lambda x: a*x*x + b*x + c

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def angle_color(angle):

    # colors = ["#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    # colors = [RED, YELLOW, GREEN, TEAL, BLUE, PURPLE]
    # colors = [TEAL, BLUE, BLUE, TEAL, GREEN, GREEN]
    # colors = [TEAL, BLUE, PURPLE, RED, YELLOW, GREEN]

    number_colors = len(colors)
    ratio = (number_colors * angle / TAU) % number_colors
    index = int(ratio)
    interpolate = ratio - index

    return interpolate_color(colors[index % number_colors], colors[(index+1) % number_colors], interpolate)

#########################################################################

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):

        super().__init__()
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

class Indicating(Transform):
    CONFIG = {
        "rate_func": there_and_back,
        "stroke_width": 6,
        "color": YELLOW,
    }

    def create_target(self):
        target = self.mobject.copy()
        target.set_style(stroke_width = self.stroke_width)
        target.set_color(self.color)
        return target

class SwallowIn(Homotopy):
    CONFIG = {
        "run_time": 2,
        "remover": True
    }

    def __init__(self, mobject, target = None, **kwargs):
        digest_config(self, kwargs, locals())
        if target is None:
            target = mobject.get_center()
        distance = max(
            get_norm(mobject.get_corner(UL)-target), 
            get_norm(mobject.get_corner(UR)-target), 
            get_norm(mobject.get_corner(DL)-target), 
            get_norm(mobject.get_corner(DR)-target),
            )
        
        def homotopy(x, y, z, t):
            position = np.array([x, y, z])
            vect = position - target
            length = get_norm(vect)
            move = t * distance
            if move >= length:
                return target
            else:
                ratio = 1 - move/length
                return target + np.array([ratio * vect[0], np.sqrt(ratio) * vect[1], 0])

        super().__init__(homotopy, mobject, **kwargs)

#########################################################################

class ParameterTrace(ParametricCurve):
    CONFIG = {
        "GM": 10,
    }

    def __init__(self, planet: np.ndarray, source: np.ndarray, major_axis: float, angle: float, **kwargs):

        distance = get_norm(source - planet) # r
        direction = (source - planet) / distance
        radius = major_axis - distance # 2a-r
        minor_axis = 2 * np.sin(angle) * np.sqrt(distance * radius) # 2b
        focal_length = np.sqrt(major_axis**2 - minor_axis**2) # 2c

        self.planet = planet
        self.source = source
        self.major_axis = major_axis
        self.angle = angle
        self.focal_length = focal_length
        self.radius = radius
        if focal_length == 0:
            self.axis_angle = self.angle
        else:
            self.axis_angle = np.arcsin(radius / focal_length * np.sin(2*angle)) # initial polar angle
        self.latus_rectum = minor_axis**2 / (2*major_axis) # p = b^2/a
        self.eccentricity = focal_length / major_axis # e = c/a

        super().__init__(lambda theta: self.parameter_function(theta), np.array([0, TAU, TAU/400]), **kwargs)
        self.angular_momentum = np.sqrt(self.GM * self.latus_rectum)


    def get_radius(self, theta: float):
        if self.angle >= PI:
            return self.latus_rectum / (1 - self.eccentricity*np.cos(- theta - self.axis_angle))
        else:
            return self.latus_rectum / (1 - self.eccentricity*np.cos(theta - self.axis_angle))

    def get_directrix(self):
        a = self.major_axis/2
        c = self.focal_length/2
        angle = self.axis_angle
        distance = (a**2 + c**2)/c
        focus_position = self.planet
        pedal = focus_position + distance*unit(angle + PI/2)
        self.directrix = Line(pedal + 8*unit(angle), pedal - 8*unit(angle))
        return self.directrix
    
    def get_focus(self):
        angle = self.angle
        source_position = self.source
        radius = self.radius
        focus_position = source_position + radius*unit(2*angle + PI/2)
        self.focus = Dot().shift(focus_position)
        return self.focus

    def parameter_function(self, theta):
        if self.angle >= PI:
            radius = self.get_radius(theta)
            return np.array([radius * np.sin(theta), radius * np.cos(theta), 0]) + self.planet
        else:
            radius = self.get_radius(theta)
            return np.array([-radius * np.sin(theta), radius * np.cos(theta), 0]) + self.planet

    def get_major_axis(self):
        if self.angle >= PI:
            self.major_axis = Line(self.parameter_function(-self.axis_angle), self.parameter_function(-self.axis_angle + PI))
        else:
            self.major_axis = Line(self.parameter_function(self.axis_angle), self.parameter_function(self.axis_angle + PI))
        return self.major_axis

class DifferentialOrbiting(Group):
    CONFIG = {
        "stop": True,
    }
    # 在Orbiting类基础上修改
    
    def __init__(self, trace: ParameterTrace, satellite: Mobject, **kwargs):

        super().__init__(satellite, **kwargs)
        self.satellite = satellite
        self.trace = trace

        self.theta = 0
        satellite.move_to(self.trace.parameter_function(self.theta))

        self.add_updater(lambda m, dt: m.orbit_update(dt))

    def orbit_update(self, dt):

        satellite = self.satellite
        trace = self.trace

        if self.theta >= TAU and self.stop:
                self.theta = TAU
        else:
            sum_of_prop = 0
            while 1:
                radius_vector = trace.get_radius(self.theta)
                angular_velocity = trace.angular_momentum/(radius_vector**2)

                prop = min(0.5/angular_velocity, 1-sum_of_prop)
                self.theta += (dt*prop)*angular_velocity
                if self.stop:
                    self.theta = min(self.theta, TAU)
                sum_of_prop += prop
                if sum_of_prop >= 1:
                    break
            satellite.move_to(trace.parameter_function(self.theta))

#########################################################################

class Knife(VMobject):
    CONFIG = {
        "fill_color": WHITE,
        "fill_opacity": 1.0,
        "stroke_color": WHITE,
        "stroke_opacity": 0.0,
        "stroke_width": 0.0,
    }
    def init_points(self) -> None:
        position = np.zeros((33, 3))
        position[0: 17] = np.array([[0, -4, 0], 
        [0.4, -3.2, 0], [0.4, -2.6, 0], [0.375, -0.275, 0], [0.35, 2.05, 0], 
        [0.5, 2.15, 0], [0.5, 2.25, 0], [0.5, 2.4, 0], [0.3, 2.5, 0], 
        [0.3, 2.6, 0], [0.25, 2.6, 0], [0.15, 3.2, 0], [0.3, 3.5, 0], 
        [0.5, 3.7, 0], [0.2, 3.8, 0], [0.2, 4, 0], [0, 4, 0]])
        position[17: 33, 0] = -position[15::-1, 0]
        position[17: 33, 1] = position[15::-1, 1]
        position /= 4
        
        points = np.zeros((48, 3))
        points[0::3] = position[0:-1:2]
        points[1::3] = position[1::2]
        points[2::3] = position[2::2]
        self.set_points(points)

class Dagger(VMobject):
    CONFIG = {
        "fill_color": WHITE,
        "fill_opacity": 1.0,
        "stroke_color": "#333333",
        "stroke_opacity": 1.0,
        "stroke_width": 4,
        "draw_stroke_behind_fill": True,
    }
    def init_points(self) -> None:
        position = np.zeros((25, 3))
        position[0: 13] = np.array([[0, -4, 0], 
        [0.325, -3.5, 0], [0.65, -3, 0], [0.65, -0.45, 0], [0.65, 2.1, 0], 
        [0.6, 2.2, 0], [0.55, 2.3, 0], [0.55, 2.9, 0], [0.55, 3.5, 0], 
        [0.55, 3.85, 0], [0.35, 4, 0], [0.175, 4, 0], [0, 4, 0]])
        position[13: 25, 0] = -position[11::-1, 0]
        position[13: 25, 1] = position[11::-1, 1]
        position /= 4
        
        points = np.zeros((36, 3))
        points[0::3] = position[0:-1:2]
        points[1::3] = position[1::2]
        points[2::3] = position[2::2]
        self.set_points(points)

class Gear(VMobject):
    CONFIG = {
        "major_radius": 1.0,
        "minor_radius": 0.8,
        "n_teeth": 17,
        "width_ratio": 2/3
    }
    def init_points(self) -> None:
        self.set_points(Gear.create_quadratic_bezier_points(
            major_radius=self.major_radius,
            minor_radius=self.minor_radius,
            n_teeth=self.n_teeth,
            width_ratio=self.width_ratio
        ))

    @staticmethod
    def create_quadratic_bezier_points(major_radius: float = 1.0, minor_radius: float = 0.8, n_teeth: int = 17, width_ratio: float = 2/3) -> np.ndarray:

        major_width_angle = TAU/(n_teeth)*(width_ratio/2)
        minor_width_angle = TAU/(n_teeth)*((1-width_ratio)/2)
        step_angle = TAU/(4*n_teeth)
        angle_sequence = np.linspace(PI/2, -3*PI/2, n_teeth + 1)

        major_negative = np.array([major_radius * unit(a + major_width_angle) / np.cos(step_angle) for a in angle_sequence])
        major_center = np.array([major_radius * unit(a) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])
        major_positive = np.array([major_radius * unit(a - major_width_angle) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])
        
        minor_negative = np.array([minor_radius * unit(a + minor_width_angle - 2*step_angle) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])
        minor_center = np.array([minor_radius * unit(a - 2*step_angle) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])
        minor_positive = np.array([minor_radius * unit(a - minor_width_angle - 2*step_angle) / np.cos(step_angle) for a in angle_sequence[0: n_teeth]])

        positions = np.zeros((12 * n_teeth, 3))
        positions[0::12] = major_negative[0:-1]
        positions[1::12] = major_center
        positions[2::12] = major_positive
        positions[3::12] = major_positive
        positions[4::12] = (major_positive + minor_negative)/2
        positions[5::12] = minor_negative
        positions[6::12] = minor_negative
        positions[7::12] = minor_center
        positions[8::12] = minor_positive
        positions[9::12] = minor_positive
        positions[10::12] = (minor_positive + major_negative[1:])/2
        positions[11::12] = major_negative[1:]
        return positions

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
        quote = Text("数学频道有一个基本任务：\n找到物理问题中的美妙结构，\n并阻止学物理的同学直接开始计算。", font = 'simsun', t2c={"物理问题": GREEN, "美妙结构": BLUE, "阻止": YELLOW, "计算": YELLOW})
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DOWN + RIGHT), DOWN + LEFT)
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
        notice2 = Notice("小学科学", "请　复习")
        notice3 = Notice("赛 尔 号", "请爷青回")
        notice4 = Notice("经典结论", "请　熟知")
        notice5 = Notice("问题引入", "请　思考")
        notice6 = Notice("优美结论", "请　欣赏")
        notice7 = Notice("暴力计算", "请　阻止")
        notice8 = Notice("优美结论", "请　欣赏")
        notice9 = Notice("催更良药", "请　三连")
        self.add(notice0)

        ground = Line(np.array([-FRAME_WIDTH/2, -3, 0]), np.array([FRAME_WIDTH/2, -3, 0]))
        background = Rectangle(height = 2, width = FRAME_WIDTH, color = BLUE_E, stroke_width = 0, fill_opacity = 0.5).shift(2*DOWN)
        bow_1 = Rectangle(height = 1, width = 0.2, fill_opacity = 1, color = LIGHT_BROWN).next_to(np.array([-5, -3, 0]), UP, buff = 0)
        bow_above = AnnularSector(inner_radius = 0.9, outer_radius = 1.2, angle = PI/2+PI/12, start_angle = PI-PI/12, color = LIGHT_BROWN)
        bow_below = AnnularSector(inner_radius = 0.9, outer_radius = 1.2, angle = PI/2+PI/12, start_angle = PI*3/2, color = LIGHT_BROWN)
        VGroup(bow_above, bow_below).set_width(1, stretch=True).next_to(np.array([-5, -2.2, 0]), UP, buff = 0)
        knot_above = Rectangle(height = 0.35, width = 0.25, fill_opacity = 1, color = DARK_BROWN).move_to(np.array([-5.4, -1.1, 0]))
        knot_below = Rectangle(height = 0.35, width = 0.25, fill_opacity = 1, color = DARK_BROWN).move_to(np.array([-4.6, -1.1, 0]))

        angle = ValueTracker(PI*5/4)
        radius = ValueTracker(0.0)

        start_point = np.array([-5, -1, 0])
        bird = Circle(radius = 0.15, fill_opacity = 1, color = RED).move_to(start_point)
        def bird_updater(bird: VMobject):
            target = radius.get_value() * unit(angle.get_value())
            bird.move_to(start_point + target)
        bag = Rectangle(height = 0.15, width = 0.28, fill_opacity = 1, color = DARK_BROWN).move_to(np.array([-5, -1.1, 0]))
        def bag_updater(bag: VMobject):
            bag.move_to(bird.get_center() + 0.1*DOWN)
        string_above = Line(np.array([-5.4, -1.1, 0]), np.array([-5, -1.1, 0]), stroke_width = 20, color = DARK_BROWN)
        def string_above_updater(string: Line):
            start = bag.get_center()
            ratio = 0.4 / get_norm(start - np.array([-5, -1.1, 0.4]))
            string.put_start_and_end_on(start, np.array([-5.4, -1.1, 0])).set_style(stroke_width = 20 * ratio)
        string_below = Line(np.array([-4.6, -1.1, 0]), np.array([-5, -1.1, 0]), stroke_width = 20, color = DARK_BROWN)
        def string_below_updater(string: Line):
            start = bag.get_center()
            ratio = 0.4 / get_norm(start - np.array([-5, -1.1, 0.4]))
            string.put_start_and_end_on(start, np.array([-4.6, -1.1, 0])).set_style(stroke_width = 20 * ratio)
        
        gravity = 1/20
        def dot_updater(order: int):
            def util(dot: Dot):
                length = 0.4 * order
                target = - length * unit(angle.get_value()) + gravity * length * length * DOWN
                dot.move_to(start_point + target)
                if dot.get_corner(UP)[1] < -1:
                    dot.set_opacity(0)
                else:
                    dot.set_opacity(1)
            return util
        group_dots = VGroup()
        dots = []
        for i in range (60):
            dot_i = Dot(radius = 0.04).add_updater(dot_updater(i))
            dots.append(dot_i)
            group_dots.add(dot_i)

        collapse = Triangle(fill_opacity = 1, color = YELLOW, stroke_width = 0).scale(0.1)
        def collapse_updater(collapse: Triangle):
            tan = np.tan(angle.get_value())
            target = tan/((tan**2 + 1)*gravity)*RIGHT + start_point
            collapse.next_to(target, DOWN, buff = 0.1)
        collapse.add_updater(collapse_updater)

        max_target = RIGHT/(2*gravity) + start_point
        max_collapse = Triangle(fill_opacity = 1, color = GREEN, stroke_width = 0).scale(0.1).next_to(max_target, DOWN, buff = 0.1)
        
        group_below = VGroup(ground, bow_1, bow_below, knot_below)
        group_string_above = VGroup(bag, string_above)
        group_above = VGroup(bow_above, knot_above)
        group_bow = VGroup(group_below, string_below, bird, group_string_above, group_above)
        self.play(FadeIn(background, UP), FadeIn(group_below, UP), FadeIn(string_below, UP), FadeIn(bird, DOWN), FadeIn(group_string_above, UP), FadeIn(group_above, UP), ReplacementTransform(notice0, notice1))
        self.waiting(1, 12) #如何把一个球扔得尽量远？
        self.waiting(0, 28) #（空闲）

        bird.add_updater(bird_updater)
        bag.add_updater(bag_updater)
        string_above.add_updater(string_above_updater)
        string_below.add_updater(string_below_updater)
        self.play(ApplyMethod(radius.set_value, 1.0), Write(group_dots), run_time = 1)
        self.play(FadeInFromPoint(collapse, 0.1*UP), run_time = 0.5)
        self.bring_to_back(max_collapse)
        self.waiting(0, 17) #大概从小学开始
        self.waiting(2, 10) #我们就会从各种地方
        self.play(ApplyMethod(angle.set_value, PI+PI/12), ReplacementTransform(notice1, notice2))
        self.waiting(0, 25) #或者是学校里
        self.play(ApplyMethod(angle.set_value, PI*3/2-PI/12), ReplacementTransform(notice2, notice3))
        self.waiting(1, 0) #或者是游戏里
        self.play(ApplyMethod(angle.set_value, PI*5/4), ReplacementTransform(notice3, notice4))
        self.waiting(0, 14) #学到这么一个结论
        self.waiting(1, 1) #（空闲）

        self.play(ApplyMethod(radius.set_value, 0.0), rate_func = rush_into, run_time = 0.3)
        bird.clear_updaters()
        bag.clear_updaters()
        distance = ValueTracker(0.0)
        def bird_updater_2(bird: VMobject):
            length = distance.get_value()
            target = - length * unit(angle.get_value()) + gravity * length * length * DOWN
            target[1] = max(-1.85, target[1])
            bird.move_to(start_point + target)
        bird.add_updater(bird_updater_2)
        self.play(ApplyMethod(distance.set_value, 24), rate_func = linear, run_time = 3)
        string_above.clear_updaters()
        string_below.clear_updaters()
        self.waiting(0, 7) #当扔出方向与地面成45度的时候
        self.waiting(1, 24) #球可以扔得最远
        self.waiting(1, 7) #（空闲）

        angle1 = ValueTracker(PI/4)
        angle2 = ValueTracker(3*PI/4)
        def tangent_point(angle: float):
            tan = np.tan(angle)
            return np.array([1/(2*gravity*tan), (1-1/(tan**2))/(4*gravity), 0])
        def background_function(angle1: float, angle2:float):
            tan1 = np.tan(angle1)
            tan2 = np.tan(angle2)
            return lambda x: x*(-gravity*(tan1*tan2+1)*x + (tan1+tan2)/2)

        def dot_updater_2(order: int):
            def util(dot: Dot):
                position = dot.get_center() - start_point
                theta1 = angle1.get_value()
                theta2 = angle2.get_value()
                if position[1] < background_function(theta1, theta2)(position[0]):
                    dot.set_opacity(0)
                else:
                    dot.set_opacity(1)
            return util
        for i in range(60):
            dots[i].clear_updaters()
            dots[i].add_updater(dot_updater_2(i))
        def collapse_updater_2(collapse: Triangle):
            tan1 = np.tan(angle1.get_value())
            tan2 = np.tan(angle2.get_value())
            x = (tan1+tan2-2)/(2*gravity*(tan1*tan2-1))
            collapse.next_to(np.array([x, x*(1-2*gravity*x), 0]) + start_point, DOWN, buff = 0.1)
        collapse.clear_updaters()
        collapse.add_updater(collapse_updater_2)
        
        background_curve = VMobject(color = BLUE_E, stroke_width = 0, fill_opacity = 0.5)
        def background_updater(background: VMobject):
            curve = FunctionGraph(background_function(angle1.get_value(), angle2.get_value()), [-19/9, 109/9, 1/9]).shift(start_point)
            background.set_points(curve.get_all_points())
            background.add_line_to(np.array([FRAME_WIDTH/2, -3, 0])).add_line_to(np.array([-FRAME_WIDTH/2, -3, 0])).close_path()
        background_curve.add_updater(background_updater)

        def max_dot_updater(order: int):
            def util(dot: Dot):
                theta = angle1.get_value()
                length = 0.4 * order
                target = length * unit(theta) + gravity * length * length * DOWN
                dot.move_to(start_point + target)
                if target[0] > tangent_point(theta)[0]:
                    dot.set_opacity(0)
                else:
                    dot.set_opacity(1)
            return util
        max_dots = VGroup()
        for i in range (60):
            max_dot_i = Dot(radius = 0.04, color = GREY).add_updater(max_dot_updater(i))
            max_dots.add(max_dot_i)

        def max_collapse_updater(collapse: Triangle):
            collapse.next_to(tangent_point(angle1.get_value()) + start_point, DOWN, buff = 0.1)
        max_collapse.add_updater(max_collapse_updater)

        self.bring_to_back(background_curve, max_dots)
        self.remove(background)
        self.play(ApplyMethod(angle1.set_value, PI/3), ApplyMethod(angle2.set_value, 5*PI/6), ReplacementTransform(notice4, notice5))
        self.waiting(1, 10) #但如果是在斜坡上扔球呢
        self.waiting(0, 29) #（空闲）
        self.play(ApplyMethod(angle1.set_value, 82*PI/360))
        self.waiting(2, 14) #再进一步 如果地面不是平的呢
        self.waiting(1, 4) #（空闲）
        self.play(ApplyMethod(angle1.set_value, PI/3), ApplyMethod(angle2.set_value, 7*PI/12))
        self.waiting(2, 9) #45度的情况就一般不是最优解了
        self.waiting(0, 29) #（空闲）
        fading_group = VGroup(group_dots, collapse, max_dots, max_collapse, background_curve, group_bow)
        bird.clear_updaters()
        background_curve.clear_updaters()
        for i in range (60):
            dots[i].clear_updaters()
            max_dots[i].clear_updaters()
        collapse.clear_updaters()
        max_collapse.clear_updaters()

        #######################################################################################################

        gravity = 1/9
        alpha = ValueTracker(0.0)

        def moving_updater(angle):
            def util(angle: float, mob: Mobject):
                a = alpha.get_value()
                mob.move_to(a*unit(angle) + gravity*a*a*DOWN + DOWN)
            return lambda x: util(angle, x)

        point_0 = Dot(color = RED).shift(DOWN)
        points = []
        traces = []
        number = 100
        for i in range(number):
            if i % 2:
                angle_i = PI * i / number - PI/2
            else:
                angle_i = - PI * (i+1) / number - PI/2
            color = angle_color(angle_i)
            moving_point_i = Dot(color = RED)
            traces_path_i = TracedPath(moving_point_i.get_center).set_color(color)
            points.append(moving_point_i)
            traces.append(traces_path_i)
            moving_point_i.add_updater(moving_updater(angle_i))

        self.play(FadeOut(fading_group, DOWN), FadeIn(point_0, DOWN))
        self.add(*points, *traces)
        self.remove(point_0)
        self.waiting(1, 14) #那么 最一般地
        self.play(ApplyMethod(alpha.set_value, 12.0), rate_func = linear, run_time = 3)
        for trace in traces:
            trace.clear_updaters()
        for point in points:
            point.clear_updaters()
        self.remove(*points)
        self.waiting(1, 3) #如果向四面八方 以固定速度扔球

        envelope = FunctionGraph(quadratic(-gravity, 0, 1/(4*gravity)-1), [-64/9, 64/9, 0.1], color = BLUE)
        guided_point = Dot(color = BLUE)
        alpha = ValueTracker(-64/9)
        def guide_updater(point: Dot):
            value = alpha.get_value()
            point.move_to(np.array([value, -gravity * value * value + 1/(4*gravity) - 1, 0]))
        guided_point.add_updater(guide_updater)

        self.add(envelope, guided_point)
        self.play(ShowCreation(envelope), ApplyMethod(alpha.set_value, 64/9), run_time = 2)
        self.waiting(0, 15) #能扔到的范围有多大呢
        self.waiting(1, 10) #（空闲）
        guided_point.clear_updaters()
        self.remove(guided_point)
        background = envelope.copy()
        background.close_path()
        background.set_style(stroke_width = 0, fill_opacity = 0, fill_color = BLUE)
        
        self.play(ReplacementTransform(notice5, notice6))
        self.waiting(0, 25) #从图上来看
        self.bring_to_back(background)
        self.play(ApplyMethod(background.set_opacity, 0.2), run_time = 0.4)
        self.play(ApplyMethod(background.set_opacity, 0), run_time = 0.4)
        self.play(ApplyMethod(background.set_opacity, 0.2), run_time = 0.4)
        self.play(ApplyMethod(background.set_opacity, 0), run_time = 0.4)
        self.play(ApplyMethod(background.set_opacity, 0.2), run_time = 0.4)
        self.waiting(1, 26) #能扔到的区域 似乎是一条抛物线的内部
        self.waiting(0, 25) #（空闲）

        coordinate = Axes(axis_config = {"include_tip": True}, x_range = np.array([-5, 5, 1]), y_range = np.array([-3, 3, 1]), height = 6, width = 10).shift(2*DOWN).set_style(stroke_color = WHITE, stroke_opacity = 1)
        group_traces = VGroup(*traces, envelope, background)
        
        #######################################################################################################

        def projectile_para(angle: float):
            return lambda t: t*unit(angle) + gravity*t*t*DOWN + 2*DOWN
        def projectile_xy(angle: float):
            tan = np.tan(angle)
            return lambda x: - gravity * (tan**2 + 1) * x**2 + tan*x -2
        def tangent_point(angle: float):
            tan = np.tan(angle)
            return np.array([1/(2*gravity*tan), (1-1/(tan**2))/(4*gravity), 0]) + 2*DOWN
        
        start_angle = PI * 81 / number - PI/2
        angle_tracker = ValueTracker(start_angle)
        def example_updater(example: VMobject):
            angle_example = angle_tracker.get_value()
            curve = ParametricCurve(projectile_para(angle_example), [0, 12, 0.05])
            example.set_color(angle_color(angle_example)).set_points(curve.get_all_points())
        example = ParametricCurve(projectile_para(start_angle), [0, 12, 0.05], color = angle_color(start_angle))
        def tangent_updater(tangent: Line):
            tangent.put_start_and_end_on(2*DOWN, 2*DOWN + 1.5*unit(angle_tracker.get_value()))
        tangent = Arrow(2*DOWN, 2*DOWN + 1.5*unit(angle_tracker.get_value()), buff = 0)

        def v0_updater(text: MTex):
            text.next_to(tangent.get_end(), UP)
        text_v0 = MTex(r"\vec{v}_0").scale(0.7).add_updater(v0_updater)
        def theta_updater(text: MTex):
            angle_example = angle_tracker.get_value()
            text.move_to(0.5*unit(angle_example/2) + 2*DOWN)
        text_theta = MTex(r"\theta").scale(0.7).add_updater(theta_updater)
        def arc_updater(arc: Arc):
            angle_example = angle_tracker.get_value()
            curve = Arc(radius = 0.3, angle = angle_example).shift(2*DOWN)
            arc.set_points(curve.get_all_points())
        arc = Arc(radius = 0.3, angle = start_angle).shift(2*DOWN)

        text_1 = MTex(r"\begin{cases}&x=v_0t\cos\theta\\&y=v_0t\sin\theta - \frac{1}{2}gt^2\end{cases}").scale(0.5).next_to(7*LEFT+3.3*UP)
        text_2 = MTex(r"\Rightarrow y=v_0\sin\theta\left(\frac{x}{v_0\cos\theta}\right)-\frac{1}{2}g\left(\frac{x}{v_0\cos\theta}\right)^2=-\frac{g}{2v_0^2}x^2\sec^2\theta +x\tan\theta=-\frac{gx^2}{2v_0^2}(\tan\theta)^2+x(\tan\theta)-\frac{gx^2}{2v_0^2}").scale(0.5).next_to(7*LEFT+2.4*UP)
        text_3 = MTex(r"\max_{\theta}(y)|_{x}=\max_{\tan\theta}(y)|_{x}=c-\frac{b^2}{4a}=-\frac{gx^2}{2v_0^2}-\frac{(x)^2}{4(-gx^2/2v_0^2)}=-\frac{g}{2v_0^2}x^2+\frac{v_0^2}{2g}", isolate = [r"-\frac{g}{2v_0^2}x^2+\frac{v_0^2}{2g}"]).scale(0.5).next_to(7*LEFT+1.6*UP)
        formula = text_3.get_part_by_tex(r"-\frac{g}{2v_0^2}x^2+\frac{v_0^2}{2g}")
        
        self.play(ApplyMethod(group_traces.shift, DOWN), FadeIn(coordinate, DOWN))
        self.play(ApplyMethod(group_traces.fade), ShowCreation(tangent), ReplacementTransform(notice6, notice7))
        example.add_updater(example_updater)
        tangent.add_updater(tangent_updater)
        self.play(ShowCreation(example), FadeIn(text_v0), FadeIn(text_theta), ShowCreation(arc), Write(VGroup(text_1, text_2)))
        arc.add_updater(arc_updater)
        self.waiting(3+0-4, 15+20) #有些训练有素的同学可能已经准备开始计算了 （空闲）

        target_tracker = ValueTracker(2*PI/5)
        start_tangent = tangent_point(2*PI/5)
        def base_line_updater(line: Line):
            target_angle = target_tracker.get_value()
            target = tangent_point(target_angle)
            line.put_start_and_end_on(np.array([target[0], -5, 0]), target)
            ratio = target_angle / TAU
            line.set_opacity(ratio % 1 < 0.5)
        base_line = Line(np.array([start_tangent[0], -5, 0]), start_tangent)
        def intersect_updater(dot: Dot):
            target = tangent_point(target_tracker.get_value())
            angle_example = angle_tracker.get_value()
            position = np.array([target[0], projectile_xy(angle_example)(target[0]), 0])
            dot.move_to(position)
            if target[1] - position[1] < 0.1:
                dot.set_color(YELLOW)
                formula.set_color(YELLOW)
            else:
                dot.set_color(WHITE)
                formula.set_color(WHITE)
            ratio = angle_example / TAU
            dot.set_opacity(ratio % 1 < 0.5)
        intersect = Dot().move_to(np.array([start_tangent[0], projectile_xy(start_angle)(start_tangent[0]), 0]))

        self.play(ShowCreation(base_line))
        self.play(ShowCreation(intersect), Write(text_3))
        base_line.add_updater(base_line_updater)
        intersect.add_updater(intersect_updater)
        self.waiting(0, 8) #确实 证明这是一条抛物线......
        self.play(ApplyMethod(angle_tracker.set_value, 4*PI/9))
        self.play(ApplyMethod(angle_tracker.set_value, PI/3)) #......计算量不算大

        self.play(ApplyMethod(angle_tracker.set_value, 2*PI/5))
        self.waiting(0, 15)
        self.play(ApplyMethod(angle_tracker.set_value, 2*PI/3), ApplyMethod(target_tracker.set_value, 2*PI/3), run_time = 1.5)
        self.play(ApplyMethod(angle_tracker.set_value, -4*PI/3), ApplyMethod(target_tracker.set_value, -4*PI/3), run_time = 3)
        self.waiting(4+2-6, 8+5) #而且能在网上找到的 关于这个结论的证明 基本也都是算出来的
        self.waiting(0, 26) #（空闲）

        example.clear_updaters()
        tangent.clear_updaters()
        text_v0.clear_updaters()
        text_theta.clear_updaters()
        arc.clear_updaters()
        base_line.clear_updaters()
        intersect.clear_updaters()
        fading_group = VGroup(coordinate, tangent, text_v0, text_theta, arc, base_line, intersect)
        shifting_group = VGroup(example, group_traces)
        self.play(SwallowIn(VGroup(text_1, text_2, text_3), 2.5*UP), ApplyMethod(shifting_group.shift, UP), FadeOut(fading_group, UP), ReplacementTransform(notice7, notice8))
        self.waiting(0, 12) #但这里是一个数学频道
        
        start_point = 2*PI/3
        angle_tracker.set_value(2*PI/3)
        opacity_tracker = ValueTracker(0.0)
        def tangent_dot_updater(dot: Dot):
            angle_example = angle_tracker.get_value()
            position = tangent_point(angle_example)+UP
            if abs(position[0]) > 10 or abs(position[1]) > 5:
                position = np.array([0, -5, 0])
            dot.move_to(position).set_opacity(opacity_tracker.get_value())
        tangent_dot = Dot(opacity = 0).move_to(tangent_point(start_point)+UP).add_updater(tangent_dot_updater)
        def focus_updater(dot: Dot):
            angle_example = angle_tracker.get_value()
            dot.move_to(unit(2*angle_example-PI/2)/(4*gravity)+DOWN).set_opacity(opacity_tracker.get_value()).set_color(angle_color(angle_example))
        focus = Dot(color = angle_color(start_point), opacity = 0).move_to(unit(2*start_point-PI/2)/(4*gravity)+DOWN).add_updater(focus_updater)
        def example_updater_2(example: VMobject):
            angle_example = angle_tracker.get_value()
            curve = ParametricCurve(projectile_para(angle_example), [0, 12, 0.05]).shift(UP)
            example.set_color(angle_color(angle_example)).set_points(curve.get_all_points())
        example.add_updater(example_updater_2)
        def full_curve_updater(full_curve: VMobject):
            angle_example = angle_tracker.get_value()
            curve = ParametricCurve(projectile_para(angle_example), [-12, 12, 0.05]).shift(UP)
            full_curve.set_color(angle_color(angle_example)).set_points(curve.get_all_points())
            full_curve.set_style(stroke_opacity = 0.5*opacity_tracker.get_value())
        full_curve = ParametricCurve(projectile_para(start_angle), [-12, 12, 0.05], color = angle_color(start_angle), fill_opacity = 0).shift(UP).add_updater(full_curve_updater)

        self.add(full_curve, tangent_dot, focus)
        self.play(ApplyMethod(angle_tracker.set_value, PI/3), run_time = 2)
        self.play(ApplyMethod(angle_tracker.set_value, 3*PI/2), ApplyMethod(opacity_tracker.set_value, 1.0), run_time = 4)
        focus_trace = TracedPath(focus.get_center, opacity = 0.5)
        self.bring_to_back(focus_trace)
        self.play(ApplyMethod(angle_tracker.set_value, PI/2), run_time = 4)
        self.waiting(1+3+0+3+0-10, 22+17+24+18+26) #这么优美的结论 怎么能没有相对应的 优美的几何结构呢 （空闲） 越优美的几何结构 往往计算量越少 （空闲）
        
        tangent_dot.clear_updaters()
        focus.clear_updaters()
        example.clear_updaters()
        full_curve.clear_updaters()
        focus_trace.clear_updaters()

        fading_group = VGroup(shifting_group, full_curve, tangent_dot, focus_trace, focus)
        self.waiting(1, 8) 
        self.play(FadeOut(fading_group)) #这个结论也不例外
        self.waiting(0, 21) #（空闲）
        
        like = Text("", font = 'vanfont').shift(3*LEFT).scale(2)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT).scale(2)
        sanlian = VGroup(like, coin, star)

        self.play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, np.array([0,0,0])), FadeInFromPoint(star, 3*RIGHT), ReplacementTransform(notice8, notice9), )
        self.play(Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), ApplyMethod(sanlian.set_color, "#00A1D6"))
        self.waiting(4-2,3) #长按点赞一键三连 我们开始吧
        self.waiting(3, 0)
        self.play(FadeOut(notice9), FadeOut(sanlian))
        self.waiting(3, 15) #到此共94秒
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#########################################################################

class Chapter1_0(Scene):

    def construct(self):

        ##  Making object
        text1 = Text("第一节 斜抛运动的轨迹", font = 'simsun', t2c={"第一节": YELLOW, "斜抛运动": GREEN, "轨迹": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(Scene):
    def construct(self):

        notice1 = Notice("磨刀不误", "砍柴工")
        notice2 = Notice("中学数学", "请　复习")
        notice3 = Notice("二周目内容", "请　全收集")
        notice4 = Notice("简单实验", "请　尝试")
        notice5 = Notice("优美动画", "请　欣赏")

        gravity = 1/9
        alpha = ValueTracker(0.0)

        def moving_updater(angle):
            def util(angle: float, mob: Mobject):
                a = alpha.get_value()
                mob.move_to(a*unit(angle) + gravity*a*a*DOWN + DOWN)
            return lambda x: util(angle, x)

        point_0 = Dot(color = RED).shift(DOWN)
        points = []
        traces = []
        paired_traces_0 = []
        paired_traces_1 = []
        number = 100
        for i in range(number):
            if i % 2:
                angle_i = PI * i / number - PI/2
            else:
                angle_i = - PI * (i+1) / number - PI/2
            color = angle_color(angle_i)
            moving_point_i = Dot(color = RED)
            traces_path_i = TracedPath(moving_point_i.get_center).set_color(color)
            points.append(moving_point_i)
            traces.append(traces_path_i)
            if i % 2:
                paired_traces_1.append(traces_path_i)
            else:
                paired_traces_0.append(traces_path_i)
            moving_point_i.add_updater(moving_updater(angle_i))
        
        self.play(ShowCreation(point_0), Write(notice1))
        self.add(*points, *traces)
        self.remove(point_0)
        self.waiting(0, 3)
        self.play(ApplyMethod(alpha.set_value, 12.0), rate_func = linear, run_time = 3)
        for trace in traces:
            trace.clear_updaters()
        for point in points:
            point.clear_updaters()
        self.remove(*points)

        envelope = FunctionGraph(quadratic(-gravity, 0, 1/(4*gravity)-1), [-64/9, 64/9, 0.1], color = BLUE)
        guided_point = Dot(color = BLUE)
        alpha = ValueTracker(-64/9)
        def guide_updater(point: Dot):
            value = alpha.get_value()
            point.move_to(np.array([value, -gravity * value * value + 1/(4*gravity) - 1, 0]))
        guided_point.add_updater(guide_updater)

        self.add(envelope, guided_point)
        self.play(ShowCreation(envelope), ApplyMethod(alpha.set_value, 64/9), run_time = 2)
        
        self.waiting(2+1+1+0-6, 6+20+20+20-3) #上来就直接证明结论 对于一些观众来说 可能有一些难度 （空闲）
        self.waiting(1, 24) #我们先从简单的开始
        self.waiting(0, 29) #（空闲）

        anims_0 = LaggedStart(*[Indicating(trace) for trace in paired_traces_0], lag_ratio = 0.2)
        anims_1 = LaggedStart(*[Indicating(trace) for trace in paired_traces_1[::-1]], lag_ratio = 0.2)
        self.play(anims_0, anims_1, run_time = 4)
        self.waiting(2+2-4, 4+13) #既然这里全都是抛物线 那么我们就先来看看抛物线
        self.waiting(0, 7)
        self.play(FadeOut(VGroup(*traces, envelope))) #（空闲）

        ###########################################################################

        center_0 = 1.5*RIGHT + 0.25*UP
        origin_0 = center_0 + 2*LEFT
        center_1 = 4.5*LEFT + 2.15*UP
        center_2 = 4.5*LEFT + 1.65*DOWN
        coordinate = Axes(axis_config = {"include_tip": True}, x_range = np.array([-1, 5, 1]), y_range = np.array([-3, 3, 1]), height = 6, width = 6).shift(center_0).set_style(stroke_color = WHITE, stroke_opacity = 1)
        surrounding_0 = Square(side_length = 6.5).shift(center_0)
        surrounding_1 = Square(side_length = 3.5).shift(center_1)
        surrounding_2 = Square(side_length = 3.5).shift(center_2)

        quadratic_function = FunctionGraph(quadratic(1, -4, 2), [-0.2, 4.2, 0.1], color = RED).shift(center_0 + 2*LEFT)
        text_quadratic_function = MTex(r"y=ax^2+bx+c").scale(0.8).move_to(center_0 + 2.75*UP)
        text_peak_function = MTex(r"y=a(x-h)^2+k").scale(0.8).move_to(center_0 + 2*UP)
        line_peak_function_x = DashedLine(2*RIGHT, 2*RIGHT+2*DOWN).shift(origin_0)
        line_peak_function_y = DashedLine(2*DOWN, 2*RIGHT+2*DOWN).shift(origin_0)
        focus_quadratic_function = Dot(color = YELLOW).shift(center_0 + 1.75*DOWN)
        directrix_quadratic_function = Line(center_0 + 2.25*DOWN + 3*LEFT, center_0 + 2.25*DOWN + 3*RIGHT, color = YELLOW)
        group_hidden = VGroup(text_peak_function, line_peak_function_x, line_peak_function_y, focus_quadratic_function, directrix_quadratic_function).set_opacity(0)
        coordinate_quadratic_function = coordinate.copy()
        group_quadratic_function = VGroup(coordinate_quadratic_function, quadratic_function, text_quadratic_function, group_hidden)
        surrounding_quadratic_function = surrounding_0.copy()
        group_quadratic_function_0 = group_quadratic_function.copy().add(surrounding_0.copy())
        group_quadratic_function_1 = group_quadratic_function.copy().scale(0.5).move_to(center_1).add(surrounding_1.copy())
        group_quadratic_function_2 = group_quadratic_function.copy().scale(0.5).move_to(center_2).add(surrounding_2.copy())
        group_quadratic_function.add(surrounding_quadratic_function)

        def projectile_xy(angle: float):
            tan = np.tan(angle)
            return lambda x: - gravity * (tan**2 + 1) * x**2 + tan*x
        start_angle = PI/3
        function_projectile = projectile_xy(start_angle)
        projectile = FunctionGraph(function_projectile, [0, 4.5, 0.1], color = GREEN).shift(origin_0)
        velocity_projectile = Arrow(origin_0, origin_0 + 1.5*unit(start_angle), buff = 0)
        text_projectile = MTex(r"\vec{v}_0").scale(0.8).shift(origin_0 + 1.8*unit(start_angle))
        x_axis = Arrow(origin_0, origin_0 + RIGHT, buff = 0)
        label_x_axis = MTex(r"x").scale(0.8).next_to(origin_0 + RIGHT, RIGHT, buff = 0.15)
        y_axis = Arrow(origin_0, origin_0 + UP, buff = 0)
        label_y_axis = MTex(r"y").scale(0.8).next_to(origin_0 + UP, UP, buff = 0.15)
        decomposition_projectile = VGroup(x_axis, label_x_axis, y_axis, label_y_axis)
        group_projectile = VGroup(projectile, velocity_projectile, text_projectile, decomposition_projectile)
        surrounding_projectile = surrounding_0.copy()
        group_projectile_0 = group_projectile.copy().add(surrounding_0.copy())
        group_projectile_1 = group_projectile.copy().scale(0.5).move_to(center_1).add(surrounding_1.copy())
        group_projectile_2 = group_projectile.copy().scale(0.5).move_to(center_2).add(surrounding_2.copy())
        group_projectile.add(surrounding_projectile)
        decomposition_projectile.set_opacity(0)

        def parabola_to_right(p: float):
            return lambda y: np.array([y**2/(2*p), y, 0])
        function_conic = parabola_to_right(1)
        conic = ParametricCurve(function_conic, [-3, 3, 0.1], color = BLUE).shift(center_0 + 2*LEFT)
        text_conic = MTex(r"y^2=2px").scale(0.8).move_to(center_0 + 2.5*UP + 0.75*LEFT)
        coordinate_conic = coordinate
        focus = Dot(color = YELLOW).shift(origin_0 + 0.5*RIGHT)
        directrix = Line(origin_0 + 0.5*LEFT + 3*UP, origin_0 + 0.5*LEFT + 3*DOWN, color = YELLOW)
        group_conic = VGroup(coordinate_conic, conic, text_conic, focus, directrix)
        surrounding_conic = surrounding_0.copy()
        group_conic_0 = group_conic.copy().add(surrounding_0.copy())
        group_conic_1 = group_conic.copy().scale(0.5).move_to(center_1).add(surrounding_1.copy())
        group_conic_2 = group_conic.copy().scale(0.5).move_to(center_2).add(surrounding_2.copy())
        group_conic.add(surrounding_conic)

        
        self.play(ReplacementTransform(notice1, notice2))
        self.waiting(1, 7) #我们在中学的学习过程中
        self.play(Write(coordinate))
        self.waiting(1, 16) #一般会有三次相对独立的接触抛物线的经历
        self.waiting(0, 20) #（空闲）

        self.play(ShowCreation(quadratic_function), Write(text_quadratic_function))
        self.add(coordinate_quadratic_function)
        self.play(ShowCreation(surrounding_quadratic_function))
        self.waiting(1, 5) #初三接触二次函数是第一次

        self.waiting(1, 0)
        self.play(Transform(group_quadratic_function, group_quadratic_function_1))
        self.waiting(0, 11) #二次函数的图像是一条抛物线
        self.waiting(0, 26) #（空闲）

        self.play(ShowCreation(velocity_projectile))
        self.play(ShowCreation(projectile), FadeIn(text_projectile))
        self.add(decomposition_projectile)
        self.play(ShowCreation(surrounding_projectile))
        self.waiting(0, 5) #高一接触斜抛运动是第二次

        self.waiting(1, 0)
        self.play(Transform(group_projectile, group_projectile_2))
        self.waiting(1, 4) #斜抛运动的运动轨迹 是抛物线的一部分
        self.waiting(0, 26) #（空闲）

        self.play(ShowCreation(conic))
        self.add(coordinate_conic)
        self.play(Write(text_conic))
        self.waiting(1, 6) #高二学习圆锥曲线是第三次

        self.play(ShowCreation(surrounding_conic))
        self.waiting(1, 9) #抛物线是圆锥曲线的一种
        self.waiting(1, 7) #（空闲）

        start_point = function_conic(1.5)
        start_pedal = np.array([-0.5, start_point[1], 0])
        point_example = Dot().shift(start_point)
        line_example = Line(start_point, 0.5*RIGHT)
        pedal_example = Dot().shift(start_pedal)
        ortho_example = Line(start_point, start_pedal)
        group_example = VGroup(point_example, line_example, pedal_example, ortho_example).shift(origin_0)
        self.play(ShowCreation(focus), ShowCreation(directrix))
        self.waiting(2, 14) #我们直到开始系统地学习圆锥曲线的时候
        self.play(ShowCreation(point_example))
        self.bring_to_back(line_example, ortho_example)
        self.play(ShowCreation(line_example), ShowCreation(ortho_example))
        self.play(ShowCreation(pedal_example))
        self.waiting(2+0-3, 11+20) #才会接触到抛物线的几何性质 （空闲）

        self.play(ReplacementTransform(notice2, notice3))
        self.play(Indicate(surrounding_quadratic_function, scale_factor = 1.1))
        self.waiting(1, 14) #而之前 无论是二次函数的图像
        self.play(Indicate(surrounding_projectile, scale_factor = 1.1))
        self.waiting(1, 11) #还是斜抛运动的轨迹

        y_value = ValueTracker(1.5)
        def point_updater(point: Dot):
            value = y_value.get_value()
            position = function_conic(value)
            point.move_to(position + origin_0)
            if value < -1.5:
                point.set_opacity(value + 2.5)
        def line_updater(line: Line):
            value = y_value.get_value()
            position = function_conic(value)
            line.put_start_and_end_on(position + origin_0, 0.5*RIGHT + origin_0)
            if value < -1.5:
                line.set_opacity(value + 2.5)
        def pedal_updater(point :Dot):
            value = y_value.get_value()
            point.move_to(np.array([-0.5, value, 0]) + origin_0)
            if value < -1.5:
                point.set_opacity(value + 2.5)
        def ortho_updater(line: Line):
            value = y_value.get_value()
            position = function_conic(value)
            line.put_start_and_end_on(position + origin_0, np.array([-0.5, position[1], 0]) + origin_0)
            if value < -1.5:
                line.set_opacity(value + 2.5)
        point_example.add_updater(point_updater)
        line_example.add_updater(line_updater)
        pedal_example.add_updater(pedal_updater)
        ortho_example.add_updater(ortho_updater)

        self.play(ApplyMethod(y_value.set_value, -1.5))
        self.waiting(0, 21) #像是焦点和准线......

        end_position = function_conic(-1.5)
        half_angle = np.arctan(end_position[1]/(end_position[0]*2))
        tangent_line = Line(end_position, np.array([0, end_position[1]/2, 0])).shift(origin_0)
        arc_angle_1 = Arc(radius = 0.3, start_angle = PI + half_angle,  angle = - half_angle).shift(end_position + origin_0)
        arc_angle_2 = Arc(radius = 0.35, start_angle = PI + half_angle,  angle = half_angle).shift(end_position + origin_0)
        text_angle_1 = MTex(r"\theta").scale(0.6).shift(end_position + origin_0 + 0.6*unit(PI + 0.5*half_angle))
        text_angle_2 = MTex(r"\theta").scale(0.6).shift(end_position + origin_0 + 0.6*unit(PI + 1.5*half_angle))
        group_optical = VGroup(tangent_line, arc_angle_1, arc_angle_2, text_angle_1, text_angle_2)
        
        self.play(ShowCreation(tangent_line))
        self.play(ShowCreation(arc_angle_1), ShowCreation(arc_angle_2), Write(text_angle_1), Write(text_angle_2))
        self.waiting(0, 25) #......这样的的几何性质
        self.waiting(3, 19) #因为还没学到 自然不在教学范围之内
        self.waiting(1, 3) #（空闲）

        self.waiting(1, 2) #于是......
        self.play(Indicate(surrounding_quadratic_function, scale_factor = 1.1), Indicate(surrounding_projectile, scale_factor = 1.1))
        self.waiting(1, 5) #......这两个视角的几何性质
        def tangent_line_updater(line: Line):
            value = y_value.get_value()
            position = function_conic(value)
            line.put_start_and_end_on(position, np.array([0, position[1]/2, 0])).shift(origin_0)
            if value < -1.5:
                line.set_opacity(value + 2.5)
        def arc_angle_updater(number: int):
            def util(arc: Arc):
                value = y_value.get_value()
                position = function_conic(value)
                half_angle = np.arctan(position[1]/(position[0]*2))
                curve = Arc(radius = 0.25 + number*0.05, start_angle = PI + half_angle,  angle = (-1)**number*half_angle).shift(position + origin_0)
                arc.set_points(curve.get_all_points())
                if value < -1.5:
                    arc.set_opacity(value + 2.5)
            return util
        def text_angle_updater(number: int):
            def util(text: MTex):
                value = y_value.get_value()
                position = function_conic(value)
                half_angle = np.arctan(position[1]/(position[0]*2))
                text.move_to(position + origin_0 + 0.6*unit(PI + (number-0.5)*half_angle))
                if value < -1.5:
                    text.set_opacity(value + 2.5)
            return util
        tangent_line.add_updater(tangent_line_updater)
        arc_angle_1.add_updater(arc_angle_updater(1))
        arc_angle_2.add_updater(arc_angle_updater(2))
        text_angle_1.add_updater(text_angle_updater(1))
        text_angle_2.add_updater(text_angle_updater(2))

        self.play(ApplyMethod(y_value.set_value, -2.5))
        self.remove(group_example, group_optical)
        self.waiting(0, 10) #就被空过去了
        self.waiting(0, 24) #（空闲）

        self.play(Transform(group_quadratic_function, group_quadratic_function_0), Transform(group_projectile, group_projectile_1), Transform(group_conic, group_conic_2))
        self.waiting(1, 10) #二次函数的图像还好说
        text_peak_function.set_opacity(1)
        self.play(Write(text_peak_function))
        line_peak_function_x.set_opacity(1)
        line_peak_function_y.set_opacity(1)
        self.play(ShowCreation(line_peak_function_x), ShowCreation(line_peak_function_y))
        focus_quadratic_function.set_opacity(1)
        directrix_quadratic_function.set_opacity(1)
        self.play(ShowCreation(focus_quadratic_function), ShowCreation(directrix_quadratic_function))
        self.waiting(1+2-3, 25+19) #经过一个坐标变换 就能化归回标准抛物线

        group_quadratic_function_0[3].set_opacity(1)
        group_quadratic_function_1[3].set_opacity(1)
        group_quadratic_function_2[3].set_opacity(1)
        self.play(Transform(group_quadratic_function, group_quadratic_function_2), Transform(group_projectile, group_projectile_0), Transform(group_conic, group_conic_1))
        self.waiting(1, 4) #但斜抛运动的轨迹

        coordinate_function = lambda x: np.array([x, projectile_xy(start_angle)(x), 0])
        start_coordinate = coordinate_function(0)
        coordinate_tracker = ValueTracker(0.0)
        point_example = Dot().shift(start_coordinate + origin_0)
        def point_updater(point: Dot):
            position = coordinate_function(coordinate_tracker.get_value())
            point.move_to(position + origin_0)
        self.play(ShowCreation(point_example))
        point_example.add_updater(point_updater)
        self.play(ApplyMethod(coordinate_tracker.set_value, 1.5))
        self.waiting(0, 23) #可不止和坐标平面有关

        middle_coordinate = coordinate_function(1.5)
        text_example = MTex(r"(x, y)").scale(0.8).next_to(middle_coordinate + origin_0, UP).shift(0.3*RIGHT)
        def text_updater(text: MTex):
            position = coordinate_function(coordinate_tracker.get_value())
            text_example.next_to(position + origin_0, UP).shift(0.3*RIGHT)
        self.play(Write(text_example))
        text_example.add_updater(text_updater)
        self.play(ApplyMethod(coordinate_tracker.set_value, 4), run_time = 1.8)
        self.waiting(0, 1) #坐标平面只记录了空间的信息
        self.play(ApplyMethod(coordinate_tracker.set_value, 3), run_time = 1.2)
        point_example.clear_updaters()
        text_example.clear_updaters()
        self.waiting(0, 26) #而斜抛运动的轨迹

        text_time = MTex(r"\begin{cases}x=v_0t\cos\theta\\y=v_0t\sin\theta - \frac{1}{2}gt^2\end{cases}").scale(0.8).next_to(origin_0 + DOWN + LEFT)
        text_energy = MTex(r"E=E_k+E_p=\frac{1}{2}mv_0^2+mgh").scale(0.8).next_to(origin_0 + 2.2*DOWN + LEFT)
        self.play(Write(text_time))
        self.play(Write(text_energy))
        self.waiting(3+1-4, 15+29) #和时间啊 机械能啊 这些物理量 不能说是毫无关系吧
        self.waiting(2, 0) #起码也是浑然一体
        self.waiting(0, 24) #（空闲）

        radius = 1/(4*gravity)
        directrix_projectile = Line(center_0 + radius*UP + 3*LEFT, center_0 + radius*UP + 3*RIGHT, color = YELLOW)
        focus_projectile = Dot(color = YELLOW).shift(origin_0 + radius*unit(2*start_angle-PI/2))
        self.waiting(1, 9) #这些物理量......
        self.play(ShowCreation(focus_projectile), ShowCreation(directrix_projectile))
        self.waiting(1, 24) #......和焦点准线 有什么联系呢
        self.waiting(1, 0) #（空闲）

        fading_group = VGroup(group_quadratic_function, group_conic, point_example, text_example, text_time, text_energy, surrounding_projectile, focus_projectile, directrix_projectile)
        moving_group = VGroup(decomposition_projectile, projectile, velocity_projectile, text_projectile)
        new_focus_projectile = Dot(color = YELLOW).shift(radius * unit(2*start_angle - PI/2))
        new_directrix_projectile = Line(radius*UP + 5*LEFT, radius*UP + 5*RIGHT, color = YELLOW)
        self.play(FadeOut(fading_group, -origin_0), ApplyMethod(moving_group.shift, -origin_0))
        
        def projectile_para(angle: float):
            return lambda t: t*unit(angle) + gravity*t*t*DOWN
        new_projectile = ParametricCurve(projectile_para(start_angle), [0, 12, 0.05]).set_color(angle_color(start_angle + 2*PI/3))
        new_projectile_adjoint = ParametricCurve(projectile_para(start_angle + PI), [0, 12, 0.05], width = 2, stroke_opacity = 0.5).set_color(angle_color(start_angle + 2*PI/3))
        self.play(ShowCreation(new_projectile), ShowCreation(new_projectile_adjoint), ReplacementTransform(notice3, notice4))
        self.remove(projectile)
        self.waiting(0, 22) #我们不妨先来画图看看

        start_point = Dot()
        text_energy = MTex(r"E=E_k+E_p=\frac{1}{2}mv_0^2+mgh").scale(0.8).next_to(3.23*UP + 5*LEFT)
        text_velocity = MTex(r"v_0=\sqrt{\frac{2E}{m}-2gh}").scale(0.8).next_to(3.3*UP + RIGHT)
        self.play(ShowCreation(start_point), Flash(ORIGIN))
        self.waiting(1, 7) #对于同一位置抛出的物体
        self.play(Write(text_energy))
        self.waiting(0, 6) #如果机械能保持不变
        self.play(Write(text_velocity), run_time = 2)
        self.play(Flash(text_projectile, flash_radius = 0.6))
        self.waiting(0, 13) #那么抛出的初速度大小相同

        arc_angle = Arc(radius = 0.3, start_angle = PI/2, angle = start_angle - PI/2, color = YELLOW)
        label_angle = MTex(r"\theta", color = YELLOW).scale(0.8).shift(0.6*unit((start_angle + PI/2)/2))
        self.waiting(1, 0) #于是 ......
        self.play(ShowCreation(arc_angle))
        self.play(Write(label_angle))
        self.waiting(0, 18) #可以改变的量只有抛出角度了
        self.waiting(0, 21) #（空闲）

        self.play(ShowCreation(new_focus_projectile), ShowCreation(new_directrix_projectile))
        self.waiting(1, 15) #我们把焦点和准线画上去
        self.play(ApplyMethod(decomposition_projectile.fade), ReplacementTransform(notice4, notice5))
        self.waiting(2, 5) #然后改变角度试试看

        angle_value = ValueTracker(start_angle)
        def velocity_updater(vector: Arrow):
            angle = angle_value.get_value()
            vector.put_start_and_end_on(ORIGIN, 1.5*unit(angle))
        velocity_projectile.add_updater(velocity_updater)
        def text_updater(text: MTex):
            angle = angle_value.get_value()
            text.move_to(1.8*unit(angle))
        text_projectile.add_updater(text_updater)
        def arc_updater(arc: Arc):
            angle = angle_value.get_value()
            labeled_angle = (((angle - PI/2)/TAU +1) % 2 -1)*TAU
            curve = Arc(radius = 0.3, start_angle = PI/2, angle = labeled_angle)
            arc.set_points(curve.get_all_points())
        arc_angle.add_updater(arc_updater)
        def label_updater(text: MTex):
            angle = angle_value.get_value()
            text.move_to(0.6*unit((angle + PI/2)/2))
        label_angle.add_updater(label_updater)
        def projectile_updater(trace: Mobject):
            angle = angle_value.get_value()
            curve = ParametricCurve(projectile_para(angle), [0, 12, 0.05])
            trace.set_color(angle_color(angle + 2*PI/3)).set_points(curve.get_all_points())
        new_projectile.add_updater(projectile_updater)
        def projectile_adjoint_updater(trace: Mobject):
            angle = angle_value.get_value()
            curve = ParametricCurve(projectile_para(angle + PI), [0, 12, 0.05])
            trace.set_color(angle_color(angle + 2*PI/3)).set_points(curve.get_all_points())
        new_projectile_adjoint.add_updater(projectile_adjoint_updater)
        def focus_updater(point: Dot):
            angle = angle_value.get_value()
            point.move_to(radius * unit(2*angle - PI/2))
        new_focus_projectile.add_updater(focus_updater)
        self.play(angle_value.animate.set_value(0.0), rate_func = rush_into, run_time = 4/3)
        self.play(angle_value.animate.set_value(-3*PI/2), rate_func = linear, run_time = 3)
        focus_trace = TracedPath(new_focus_projectile.get_center, opacity = 0.5)
        self.bring_to_back(focus_trace)
        self.play(angle_value.animate.set_value(-10*PI/3), rate_func = linear, run_time = 11/3)
        self.play(angle_value.animate.set_value(-11*PI/3), rate_func = rush_from, run_time = 4/3)
        self.waiting(1, 20) # 到此共130秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_2(Scene):
    def construct(self):

        notice5 = Notice("优美动画", "请　欣赏")
        notice6 = Notice("现象总结", "请注意到")
        notice7 = Notice("暴力计算", "请　阻止")
        notice8 = Notice("优美证法", "请　欣赏")
        notice9 = Notice("证明完毕", "请　鼓掌")
        notice10 = Notice("美妙性质", "请　欣赏")

        gravity = 1/9
        radius = 1/(4*gravity)
        start_angle = PI/3
        def projectile_para(angle: float):
            return lambda t: t*unit(angle) + gravity*t*t*DOWN
        text_energy = MTex(r"E=E_k+E_p=\frac{1}{2}mv_0^2+mgh").scale(0.8).next_to(3.23*UP + 5*LEFT)
        text_velocity = MTex(r"v_0=\sqrt{\frac{2E}{m}-2gh}").scale(0.8).next_to(3.3*UP + RIGHT)
        focus_projectile = Dot(color = YELLOW).shift(radius * unit(2*start_angle - PI/2))
        directrix_projectile = Line(radius*UP + 5*LEFT, radius*UP + 5*RIGHT, color = YELLOW)
        projectile = ParametricCurve(projectile_para(start_angle), [0, 12, 0.05]).set_color(angle_color(start_angle + 2*PI/3))
        projectile_adjoint = ParametricCurve(projectile_para(start_angle + PI), [0, 12, 0.05], width = 2, stroke_opacity = 0.5).set_color(angle_color(start_angle + 2*PI/3))
        x_axis = Arrow(ORIGIN, RIGHT, buff = 0)
        label_x_axis = MTex(r"x").scale(0.8).next_to(RIGHT, RIGHT, buff = 0.15)
        y_axis = Arrow(ORIGIN, UP, buff = 0)
        label_y_axis = MTex(r"y").scale(0.8).next_to(UP, UP, buff = 0.15)
        decomposition_projectile = VGroup(x_axis, label_x_axis, y_axis, label_y_axis).fade()
        velocity_projectile = Arrow(ORIGIN, 1.5*unit(start_angle), buff = 0)
        text_projectile = MTex(r"\vec{v}_0").scale(0.8).shift(1.8*unit(start_angle))
        start_point = Dot()
        arc_angle = Arc(radius = 0.3, start_angle = PI/2, angle = start_angle - PI/2, color = YELLOW)
        label_angle = MTex(r"\theta", color = YELLOW).scale(0.8).shift(0.6*unit((start_angle + PI/2)/2))
        trace = Circle(radius = radius, stroke_width = 2, stroke_color = WHITE)

        angle_value = ValueTracker(start_angle)
        def velocity_updater(vector: Arrow):
            angle = angle_value.get_value()
            vector.put_start_and_end_on(ORIGIN, 1.5*unit(angle))
        velocity_projectile.add_updater(velocity_updater)
        def text_updater(text: MTex):
            angle = angle_value.get_value()
            text.move_to(1.8*unit(angle))
        text_projectile.add_updater(text_updater)
        def arc_updater(arc: Arc):
            angle = angle_value.get_value()
            labeled_angle = (((angle - PI/2)/TAU +1) % 2 -1)*TAU
            curve = Arc(radius = 0.3, start_angle = PI/2, angle = labeled_angle)
            arc.set_points(curve.get_all_points())
        arc_angle.add_updater(arc_updater)
        def label_updater(text: MTex):
            angle = angle_value.get_value()
            text.move_to(0.6*unit((angle + PI/2)/2))
        label_angle.add_updater(label_updater)
        def projectile_updater(trace: Mobject):
            angle = angle_value.get_value()
            curve = ParametricCurve(projectile_para(angle), [0, 12, 0.05])
            trace.set_color(angle_color(angle + 2*PI/3)).set_points(curve.get_all_points())
        projectile.add_updater(projectile_updater)
        def projectile_adjoint_updater(trace: Mobject):
            angle = angle_value.get_value()
            curve = ParametricCurve(projectile_para(angle + PI), [0, 12, 0.05])
            trace.set_color(angle_color(angle + 2*PI/3)).set_points(curve.get_all_points())
        projectile_adjoint.add_updater(projectile_adjoint_updater)
        def focus_updater(point: Dot):
            angle = angle_value.get_value()
            point.move_to(radius * unit(2*angle - PI/2))
        focus_projectile.add_updater(focus_updater)
        with_updater = [velocity_projectile, text_projectile, arc_angle, label_angle, projectile, projectile_adjoint, focus_projectile]
        
        self.add(notice5, trace, decomposition_projectile, velocity_projectile, text_projectile, text_energy, text_velocity, focus_projectile, directrix_projectile, projectile, projectile_adjoint, start_point, arc_angle, label_angle)

        self.play(ReplacementTransform(notice5, notice6))
        self.waiting(1, 11) #一些观众可能会注意到
        self.play(Indicate(trace, scale_factor = 1.1))
        self.waiting(1, 28) #焦点的轨迹形成了一个圆
        self.waiting(2+1-3, 24+27)
        self.play(angle_value.animate.set_value(PI/4))
        self.play(angle_value.animate.set_value(2*PI/5))
        self.play(angle_value.animate.set_value(PI/3)) #不过 更值得注意的是 在角度变化的时候
        for mob in with_updater:
            mob.clear_updaters()
        self.play(WiggleOutThenIn(directrix_projectile))
        self.waiting(0, 8) #准线似乎是完全不动的
        self.waiting(0, 28) #（空闲）
        
        height_arrow = Line(ORIGIN, radius*UP).add_tip(at_start=True, tip_style=1).add_tip(tip_style=1)
        line_left = Line(height_arrow.get_corner(UR), height_arrow.get_corner(UL))
        line_right = Line(height_arrow.get_corner(DR), height_arrow.get_corner(DL))
        group_arrow = VGroup(height_arrow, line_left, line_right).next_to(radius*UP/2, LEFT, buff = 0.1)
        copy_projectile = projectile.copy().set_style(stroke_opacity = 0.5).add_updater(projectile_updater)
        copy_projectile_adjoint = projectile_adjoint.copy().set_style(stroke_opacity = 0.5).add_updater(projectile_adjoint_updater)
        copy_focus_projectile = focus_projectile.copy().set_opacity(0.5).add_updater(focus_updater)
        copy_velocity_projectile = velocity_projectile.copy().set_opacity(0.5).add_updater(velocity_updater)
        copy_text_projectile = MTex(r"\vec{v}'_0").scale(0.8).shift(1.8*unit(start_angle)).set_opacity(0.5).add_updater(text_updater)
        copy_with_updater = [copy_projectile, copy_projectile_adjoint, copy_focus_projectile, copy_velocity_projectile, copy_text_projectile]
        text_max_energy = MTex(r"mg\Delta h=\frac{1}{2}mv_0^2 \Rightarrow").scale(0.8).next_to(radius*UP/2 + 6*LEFT, RIGHT)
        text_max_height = MTex(r"\Delta h=\frac{v_0^2}{2g}").scale(0.7).next_to(radius*UP/2, LEFT, buff = 0.4)

        self.bring_to_back(*copy_with_updater)
        self.play(angle_value.animate.set_value(PI/2), FadeOut(decomposition_projectile))
        for mob in copy_with_updater:
            mob.clear_updaters()
        self.waiting(0, 9)
        self.play(ShowCreation(line_left), ShowCreation(line_right)) #从竖直上抛的情况推断
        self.play(FadeInFromPoint(height_arrow, height_arrow.get_center()))
        self.play(Write(text_max_energy))
        self.play(FadeIn(text_max_height, 0.5*RIGHT))
        self.waiting(1, 15) #准线 是在全部机械能都转化成重力势能时
        self.waiting(2, 4) #这个抛体所在的等势面
        self.waiting(0, 25) #（空闲）

        self.waiting(1, 0) #那么......
        velocity_decomposition_y = Arrow(5*LEFT, np.array([-5, 1.5*unit(start_angle)[1], 0]), buff = 0, color = BLUE)
        velocity_decomposition_x = Arrow(5*LEFT, np.array([-5 + 1.5*unit(start_angle)[0], 0]), buff = 0, color = RED)
        text_decomposition_y = MTex(r"v_0\cos \theta", color = BLUE).scale(0.7).next_to(velocity_decomposition_y, LEFT)
        text_decomposition_x = MTex(r"v_0\sin \theta", color = RED).scale(0.7).next_to(velocity_decomposition_x, DOWN, buff = 0.1)
        fading_group = VGroup(text_energy, text_velocity, text_max_energy, text_max_height, *with_updater[0:2], *copy_with_updater, group_arrow, trace, with_updater[5])
        shifting_group = VGroup(*with_updater[2:5], with_updater[6], start_point)
        self.play(FadeOut(fading_group, 5*LEFT), shifting_group.animate.shift(5*LEFT), directrix_projectile.animate.put_start_and_end_on(radius*UP + 6*LEFT, radius*UP + RIGHT), TransformFromCopy(velocity_projectile, velocity_decomposition_y), TransformFromCopy(text_projectile, text_decomposition_y), TransformFromCopy(velocity_projectile, velocity_decomposition_x), TransformFromCopy(text_projectile, text_decomposition_x))
        self.waiting(0, 22) #......在一般的情况下
        self.waiting(2, 9) #我们应该怎么说明这一点呢
        self.waiting(1, 4) #（空闲）

        label_focus = MTex(r"F").scale(0.7).move_to((radius + 0.3) * unit(2*start_angle-PI/2) + 5*LEFT)
        coordinate_focus = radius * unit(2*start_angle - PI/2)
        position_apex = np.array([coordinate_focus[0] - 5, (coordinate_focus[1]+radius)/2, 0])
        point_apex = Dot().shift(position_apex)
        label_apex = MTex(r"A").scale(0.7).next_to(point_apex, UP, buff = 0.1)
        label_start = MTex(r"P").scale(0.7).next_to(start_point, LEFT, buff = 0.1)
        label_directrix = MTex(r"l").next_to(directrix_projectile, LEFT)
        text_1 = MTex(r"\begin{cases}x=v_0t\sin\theta\\y=v_0t\cos\theta - \frac{1}{2}gt^2\end{cases}").scale(0.5).next_to(RIGHT + 2*UP)
        text_2 = MTex(r"\Rightarrow y&=-\frac{g}{2v_0^2\sin^2\theta}x^2+(\cot\theta)x\\&=-\frac{g}{2v_0^2\sin^2\theta}\left(x-\frac{v_0^2\sin\theta\cos\theta}{g}\right)^2 + \frac{v_0^2}{2g}\cos^2\theta").scale(0.5).next_to(RIGHT + 0.7*UP)
        text_3 = MTex(r"\Rightarrow A = \left(\frac{v_0^2\sin\theta\cos\theta}{g},\ \frac{v_0^2}{2g}\cos^2\theta\right),\ p = \frac{v_0^2\sin^2\theta}{g}").scale(0.5).next_to(RIGHT + 0.7*DOWN)
        text_4 = MTex(r"\Rightarrow l: y = A[y] + \frac{p}{2}=\frac{v_0^2}{2g}").scale(0.5).next_to(RIGHT + 1.5*DOWN)
        self.play(ShowCreation(label_focus), ShowCreation(point_apex), ShowCreation(label_apex), ShowCreation(label_directrix), Write(text_1), ReplacementTransform(notice6, notice7))
        self.waiting(1, 7) #有些久经考验的同学可能已经准备开始计算了
        self.waiting(0, 19) #（空闲）
        self.play(Write(text_2))
        self.waiting(1, 25) #确实 抛物线的轨迹方程可以算
        self.play(Write(text_3))
        self.waiting(0, 15) #焦准距同样可以算
        self.play(Write(text_4))
        self.waiting(1, 8) #计算量加起来也不如一道圆锥曲线的大题
        self.waiting(0, 20) #（空闲）

        self.waiting(2, 14) #但这里是一个数学频道
        self.play(SwallowIn(VGroup(text_1, text_2, text_3, text_4)), ReplacementTransform(notice7, notice8))
        self.waiting(0, 20) #能用几何手段就要用几何手段
        self.waiting(1, 3) #（空闲）

        self.waiting(1, 10) #首先......
        self.play(ShowCreation(label_start))
        self.waiting(1, 22) #......我们从起始点作出最常见的辅助线
        self.waiting(0, 18) #（空闲）

        position_start = start_point.get_center()
        position_focus = focus_projectile.get_center()
        position_pedal = position_start + radius * UP
        position_middle = (position_focus + position_pedal)/2
        line_to_focus = Line(position_start, position_focus)
        pedal = Dot().shift(position_pedal)
        label_pedal = MTex(r"H").scale(0.7).next_to(pedal, UP, buff = 0.1)
        line_to_pedal = Line(position_start, position_pedal)
        line_focus_pedel = Line(position_focus, position_pedal)
        middle_point = Dot().shift(position_middle)
        label_middle = MTex(r"M").scale(0.7).next_to(middle_point, UR, buff = 0.1)
        line_tangent = DashedLine(position_start, position_middle)
        arc_angle_2 = Arc(radius = 0.3, start_angle = start_angle, angle = start_angle - PI/2, color = interpolate_color(YELLOW, "#333333", 0.5)).shift(position_start)
        label_angle_2 = MTex(r"\theta", color = interpolate_color(YELLOW, "#333333", 0.5)).scale(0.8).shift(0.6*unit((3*start_angle - PI/2)/2) + position_start)
        tex_1 = r"PF=PH"
        tex_2 = r"MF=MH"
        tex_3 = r"\Rightarrow \angle FPM=\angle MPH=\theta"
        mtex_1 = MTex(r"\begin{cases}"+tex_1+r"\\"+tex_2+r"\end{cases}", isolate = [tex_1, tex_2]).scale(0.8).next_to(RIGHT+2.5*UP)
        mtex_1_1 = mtex_1.get_part_by_tex(tex_1)
        mtex_1_2 = mtex_1.get_part_by_tex(tex_2)
        mtex_2 = MTex(tex_3).scale(0.8).next_to(RIGHT+1.5*UP)
        self.bring_to_back(line_to_focus)
        self.play(ShowCreation(line_to_focus))
        self.waiting(0, 28) #到焦点的连线
        self.bring_to_back(line_to_pedal)
        self.play(ShowCreation(line_to_pedal))
        self.play(ShowCreation(pedal), ShowCreation(label_pedal), Write(mtex_1_1)) #到准线的垂线......
        self.waiting(1+0-2, 28+25) #......以及......
        self.play(ShowCreation(line_tangent))
        self.play(ShowCreation(arc_angle_2), Write(label_angle_2))
        self.waiting(0+1-1, 18+1) #过这一点处的切线 （空闲）

        self.bring_to_back(projectile, line_focus_pedel)
        self.play(ShowCreation(line_focus_pedel))
        self.play(ShowCreation(middle_point), Write(label_middle), Write(mtex_1_2))
        self.waiting(0, 29) #再取出垂足和焦点的中点
        self.waiting(0, 18) #（空闲）
        self.play(ShowCreation(mtex_1[0]))
        self.waiting(1, 12) #那么 根据光学性质
        self.play(FadeIn(mtex_2, 0.5*RIGHT))
        self.waiting(1, 6) #这个中点就在切线上
        self.waiting(0, 28) #（空闲）

        elbow_1 = Elbow(width = 0.15, angle = start_angle + PI, stroke_width = 3).shift(position_middle)
        position_b = 2*position_middle - position_apex
        point_b = Dot().shift(position_b)
        label_b = MTex(r"B").scale(0.7).next_to(point_b, UL, buff = 0.1)
        line_to_b = Line(position_middle, position_b)
        elbow_2 = Elbow(width = 0.15, angle = -PI/2, stroke_width = 3).shift(position_b)
        mtex_3 = MTex(r"PB=PM\cos\theta=PH\cos^2\theta").scale(0.8).next_to(RIGHT+0.8*UP)
        self.bring_to_back(line_to_b)
        self.play(ShowCreation(line_to_b))
        self.play(ShowCreation(point_b), Write(label_b))
        self.play(ShowCreation(elbow_1), ShowCreation(elbow_2), Write(mtex_3))
        self.waiting(3+1-4, 5+4) #这样 我们获得了一些直角三角形 （空闲）

        apex_tangent_left = DashedLine(position_apex, position_b + LEFT)
        apex_tangent_right = DashedLine(position_apex, position_b + 5*RIGHT)
        self.bring_to_back(apex_tangent_left, apex_tangent_right)
        self.play(ShowCreation(apex_tangent_left), ShowCreation(apex_tangent_right))
        self.waiting(1, 7) # 我们再作出顶点处的切线
        self.waiting(0, 19) #（空闲）
        self.waiting(1, 1) #那么......
        self.play(Indicate(middle_point), Indicate(label_middle), Indicate(point_b), Indicate(label_b))
        self.waiting(2, 7) #我们刚才取的中点 也在这条切线上
        self.waiting(0, 22) #（空闲）

        self.play(Indicate(VGroup(apex_tangent_left, apex_tangent_right), scale_factor = 1.1), Indicate(directrix_projectile, scale_factor = 1.1))
        self.waiting(1, 26) #并且这条切线是水平方向的
        tex_0 = r"PB"
        tex_1 = r"=\frac{v_P^2-v_A^2}{2g}"
        tex_2 = r"=\frac{v_0^2-v_0^2\sin^2\theta}{2g}"
        tex_3 = r"=\frac{v_0^2}{2g}\cos^2\theta"
        mtex_4 = MTex(tex_0 + r"&" + tex_1 + tex_2 + r"\\&" + tex_3, isolate = [tex_0, tex_1, tex_2, tex_3]).scale(0.8).next_to(RIGHT+0.6*DOWN)
        mtex_4_1 = mtex_4.get_parts_by_tex([tex_0, tex_1])
        mtex_4_2 = mtex_4.get_part_by_tex(tex_2)
        mtex_4_3 = mtex_4.get_part_by_tex(tex_3)
        self.play(Write(mtex_4_1))
        self.waiting(0, 28) #于是它是一个等势面
        self.waiting(0, 27) #（空闲）
        

        velocity_apex = velocity_decomposition_x.copy().shift(position_apex - position_start)
        text_velocity_apex = text_decomposition_x.copy().next_to(velocity_apex.get_corner(UR), UP, buff = 0.15)
        self.play(TransformFromCopy(velocity_decomposition_x, velocity_apex), TransformFromCopy(text_decomposition_x, text_velocity_apex))
        self.play(Write(mtex_4_2))
        self.waiting(0, 4) #而我们能知道顶点处的能量情况
        self.play(Write(mtex_4_3))
        self.waiting(1, 3) #于是就可以得到高度差

        tex_1 = r"\Rightarrow "
        tex_2 = r"PH=\frac{v_0^2}{2g}"
        mtex_5 = MTex(tex_1 + tex_2, isolate = [tex_1, tex_2]).scale(0.8).next_to(RIGHT+2.2*DOWN)
        mtex_5_1 = mtex_5.get_part_by_tex(tex_1)
        mtex_5_2 = mtex_5.get_part_by_tex(tex_2)
        self.waiting(1, 10) #再进一步
        self.play(Write(mtex_5), ReplacementTransform(notice8, notice9))
        self.waiting(2, 2) #就能得到准线和起始点的距离了
        self.waiting(1, 0) #（空闲）

        surrounding = SurroundingRectangle(mtex_5_2)
        self.play(ShowCreation(surrounding))
        self.waiting(1, 26) #这是一个只与初速度大小有关的量
        fading_group = VGroup(velocity_decomposition_y, velocity_decomposition_x, text_decomposition_y, text_decomposition_x, point_apex, label_apex, label_directrix, line_focus_pedel, middle_point, label_middle, line_tangent, arc_angle_2, label_angle_2, point_b, label_b, line_to_b, elbow_1, elbow_2, apex_tangent_left, apex_tangent_right, velocity_apex, text_velocity_apex)
        fading_moving_group = VGroup(mtex_1, mtex_2, mtex_3, mtex_4, mtex_5_1)
        self.play(FadeOut(fading_group), FadeOut(fading_moving_group, 5.4*UP), VGroup(mtex_5_2, surrounding).animate.shift(5.4*UP))
        self.waiting(2, 18) #数值上 等于竖直上抛所能上升的最大高度
        self.waiting(0, 13) #（空闲）

        fading_group = VGroup(*with_updater[0:2], with_updater[5])
        vanishing_group = VGroup(*with_updater[2:4])
        shifting_group = VGroup(with_updater[4], with_updater[6], start_point, label_start, label_pedal, label_focus, line_to_focus, line_to_pedal, pedal)
        mtex_6 = MTex(r"PF = \frac{v_0^2}{2g}").scale(0.8).next_to(3.2*UP + 5*LEFT)
        surrounding_2 = SurroundingRectangle(mtex_6)
        self.bring_to_back(projectile_adjoint, line_to_focus, line_to_pedal)
        self.play(FadeIn(fading_group, 5*RIGHT), FadeOut(vanishing_group, 5*RIGHT), shifting_group.animate.shift(5*RIGHT), directrix_projectile.animate.put_start_and_end_on(radius*UP + 5*LEFT, radius*UP + 5*RIGHT), ReplacementTransform(notice9, notice10))
        self.waiting(1, 19) #而起始点到准线的距离
        self.waiting(3, 4) #正好等于起始点到焦点的距离
        self.waiting(0, 20) #（空闲）
        self.play(WiggleOutThenIn(directrix_projectile))
        self.play(Write(mtex_6))
        self.play(ShowCreation(surrounding_2))
        self.waiting(1+3-4, 21+2) #如果准线不变 那么起始点到焦点的距离就是定值
        self.waiting(0, 25) #（空闲）

        angle_value = ValueTracker(start_angle)
        velocity_projectile.add_updater(velocity_updater)
        text_projectile.add_updater(text_updater)
        projectile.add_updater(projectile_updater)
        projectile_adjoint.add_updater(projectile_adjoint_updater)
        focus_projectile.add_updater(focus_updater)
        def line_updater(line: Line):
            angle = angle_value.get_value()
            line.put_start_and_end_on(ORIGIN, radius * unit(2*angle - PI/2))
        line_to_focus.add_updater(line_updater)
        def label_focus_updater(text: MTex):
            angle = angle_value.get_value()
            text.move_to((radius + 0.3) * unit(2*angle - PI/2))
        label_focus.add_updater(label_focus_updater)
        focus_trace = TracedPath(focus_projectile.get_center, opacity = 0.5)
        with_updater = [velocity_projectile, text_projectile, projectile, projectile_adjoint, focus_projectile, line_to_focus, label_focus, focus_trace]
        self.bring_to_back(focus_trace)
        self.play(angle_value.animate.set_value(0.0), rate_func = rush_into, run_time = 4/3)
        self.play(angle_value.animate.set_value(-4*PI/3), rate_func = linear, run_time = 8/3)
        self.play(angle_value.animate.set_value(-5*PI/3), rate_func = rush_from, run_time = 4/3)
        for mob in with_updater:
            mob.clear_updaters()
        self.waiting(2+2+1-5, 8+17+14-10) #随着抛出角度的变化 焦点的轨迹就会形成一个圆 （空闲）

        self.waiting(1, 17) #这么好的性质
        self.waiting(2, 17) #足够我们解决一开始的问题了

        self.waiting(3, 16)
        fading_group = VGroup(*with_updater, directrix_projectile, start_point, label_start, label_pedal, pedal, line_to_pedal, mtex_5_2, surrounding, mtex_6, surrounding_2, notice10)
        self.play(FadeOut(fading_group))
        self.waiting(4, 0) #到此共137秒
        
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#########################################################################

class Chapter2_0(Scene):

    def construct(self):

        ##  Making object
        text2 = Text("第二节 抛体轨迹的包络", font = 'simsun', t2c={"第一节": YELLOW, "抛体轨迹": GREEN, "包络": BLUE})

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(Scene):
    def construct(self):

        notice1 = Notice("问题再现", "请　复习")
        notice2 = Notice("概念引入", "请记笔记")
        notice3 = Notice("优美性质", "请　思考")
        notice4 = Notice("丢三落四", "请勿模仿")
        notice5 = Notice("常用定义", "请　参考")
        notice6 = Notice("简单引理", "请　验证")
        notice7 = Notice("最后一步", "请　专注")

        gravity = 1/9
        radius = 1/(4*gravity)
        alpha = ValueTracker(0.0)

        def moving_updater(angle):
            def util(angle: float, mob: Mobject):
                a = alpha.get_value()
                mob.move_to(a*unit(angle) + gravity*a*a*DOWN + DOWN)
            return lambda x: util(angle, x)

        point_0 = Dot(color = RED).shift(DOWN)
        points = []
        traces = []
        number = 100
        for i in range(number):
            if i % 2:
                angle_i = PI * i / number - PI/2
            else:
                angle_i = - PI * (i+1) / number - PI/2
            color = angle_color(angle_i)
            moving_point_i = Dot(color = RED)
            traces_path_i = TracedPath(moving_point_i.get_center).set_color(color)
            points.append(moving_point_i)
            traces.append(traces_path_i)
            moving_point_i.add_updater(moving_updater(angle_i))

        self.play(ShowCreation(point_0), Write(notice1))
        self.add(*points, *traces)
        self.remove(point_0)
        self.waiting(0, 3)
        self.play(alpha.animate.set_value(12.0), rate_func = linear, run_time = 3)
        for trace in traces:
            trace.clear_updaters()
        for point in points:
            point.clear_updaters()
        self.remove(*points)

        envelope = FunctionGraph(quadratic(-gravity, 0, radius), [-64/9, 64/9, 0.1], color = BLUE).shift(DOWN)
        background = envelope.copy()
        background.close_path()
        background.set_style(stroke_width = 0, fill_opacity = 0.2, fill_color = BLUE)
        guided_point = Dot(color = BLUE)
        base = VGroup(background, *traces)

        self.play(FadeIn(background), ReplacementTransform(notice1, notice2))
        self.waiting(3+3-5, 17+13-3) #按照恒定速度向所有方向抛出物体 抛体运动的所有轨迹围成了一个区域

        alpha = ValueTracker(-64/9)
        def guide_updater(point: Dot):
            value = alpha.get_value()
            point.move_to(np.array([value, -gravity * value * value + 1/(4*gravity) - 1, 0]))
        guided_point.add_updater(guide_updater)
        text_envelope = Text(r"包络线", font = 'simsun', color = YELLOW).next_to(3*UP, UP)
        line_envelope = Line(3*UP, 3*UP)

        self.add(envelope, guided_point)
        self.play(ShowCreation(envelope), alpha.animate.set_value(64/9), run_time = 2)
        guided_point.clear_updaters()
        self.remove(guided_point)
        self.play(FadeIn(text_envelope, 0.5*DOWN), line_envelope.animate.put_start_and_end_on(3*UP + 6*LEFT, 3*UP + 6*RIGHT))
        self.waiting(1+2-3, 18+22) #这个区域的边界 被称作所有抛体轨迹的包络线
        self.waiting(0, 22) #（空闲）
        
        start_point = Dot(color = BLUE).shift(DOWN)
        envelope_directrix = Line(DOWN + 2*radius*UP + 0*LEFT, DOWN + 2*radius*UP + 0*RIGHT, color = BLUE)
        apex = Dot(color = BLUE).shift(DOWN + radius*UP)
        self.bring_to_back(base)
        self.play(FadeOut(VGroup(text_envelope, line_envelope)), base.animate.fade())
        self.waiting(0, 28) #按照我们所猜测的
        self.waiting(1, 11) #这条包络线......
        self.play(ShowCreation(start_point), envelope_directrix.animate.put_start_and_end_on(DOWN + 2*radius*UP + 5*LEFT, DOWN + 2*radius*UP + 5*RIGHT))
        self.waiting(1, 0) #......应该是一条抛物线
        self.waiting(0, 18) #（空闲）

        example_angle = PI/3
        def projectile_para(angle: float):
            return lambda t: t*unit(angle) + gravity*t*t*DOWN + DOWN
        example_function = projectile_para(example_angle)
        example_projectile = ParametricCurve(example_function, [0, 12, 0.05]).set_color(angle_color(example_angle))
        copy_projectile = example_projectile.copy()
        example_focus = Dot(color = YELLOW).shift(radius * unit(2*example_angle - PI/2) + DOWN)
        copy_focus = example_focus.copy()
        example_directrix = Line(DOWN + radius*UP + 0*LEFT, DOWN + radius*UP + 0*RIGHT, color = YELLOW)
        self.bring_to_back(example_projectile)
        self.play(ShowCreation(example_projectile), ShowCreation(example_focus), example_directrix.animate.put_start_and_end_on(DOWN + radius*UP + 5*LEFT, DOWN + radius*UP + 5*RIGHT), ReplacementTransform(notice2, notice3))
        self.bring_to_back(copy_projectile, copy_focus)
        self.waiting(0, 22) #所有轨迹上的点

        example_point = start_point.copy()
        alpha = ValueTracker(0.0)
        target = 2*radius/np.sin(example_angle)
        def point_updater(point: Dot):
            t = alpha.get_value()
            point.move_to(example_function(t))
            if abs(t - target) < 0.2:
                point.set_color(YELLOW)
            else:
                point.set_color(BLUE)
        example_point.add_updater(point_updater)
        self.add(example_point)
        self.play(alpha.animate.set_value(target))
        self.waiting(0, 29) #要不然在包络线上
        self.play(alpha.animate.set_value(3.0))
        self.play(alpha.animate.set_value(7.0))
        example_point.clear_updaters()
        self.waiting(0, 5) #要不然在包络线内部
        self.waiting(1, 1) #（空闲）

        self.waiting(1, 17) #从图上来看
        self.play(Indicate(start_point))
        self.waiting(0, 19) #这条包络线的焦点
        self.waiting(1, 22) #就是起始点
        self.play(ShowCreation(apex))
        self.waiting(0, 10) #而它的顶点
        alpha = ValueTracker(example_angle)
        def projectile_updater(trace: VMobject):
            angle = alpha.get_value()
            curve = ParametricCurve(projectile_para(angle), [0, 12, 0.05])
            trace.set_color(angle_color(angle)).set_points(curve.get_all_points())
        copy_projectile.add_updater(projectile_updater)
        def focus_updater(point: Dot):
            angle = alpha.get_value()
            point.move_to(radius * unit(2*angle - PI/2) + DOWN)
        copy_focus.add_updater(focus_updater)
        self.play(alpha.animate.set_value(PI/2))
        copy_projectile.clear_updaters()
        copy_focus.clear_updaters()
        self.remove(copy_focus)
        self.waiting(1, 8) #是竖直上抛的最高点

        line_to_apex = Line(DOWN + radius * UP, DOWN, color = RED)
        alpha = ValueTracker(3*PI/2)
        self.play(WiggleOutThenIn(envelope_directrix))
        self.bring_to_back(line_to_apex)
        self.play(WiggleOutThenIn(example_directrix), FadeOut(copy_projectile), ShowCreation(line_to_apex))
        self.waiting(1+2-4, 23+20) #那么它的准线 就应该比所有轨迹的公共准线
        copy_directrix = example_directrix.copy().save_state()
        copy_apex = apex.copy().save_state()
        copy_to_apex = line_to_apex.copy().save_state()
        def moving_updater(mob: VMobject):
            angle = alpha.get_value()
            mob.restore().shift(radius/2*UP + radius/2*unit(angle))
        def directrix_updater(line: Line):
            rate = (3*PI/2 - alpha.get_value())/PI
            line.set_color(interpolate_color(YELLOW, BLUE, rate))
        copy_directrix.add_updater(moving_updater).add_updater(directrix_updater)
        copy_apex.add_updater(moving_updater)
        copy_to_apex.add_updater(moving_updater)
        self.bring_to_back(copy_directrix, copy_to_apex)
        self.add(copy_apex)
        self.play(alpha.animate.set_value(PI/2), run_time = 1.5)
        copy_directrix.clear_updaters()
        copy_apex.clear_updaters()
        copy_to_apex.clear_updaters()
        self.remove(copy_directrix)
        self.waiting(0, 10) #再高出一倍
        self.waiting(1, 23) #这应该怎么证呢
        self.waiting(1, 2) #（空闲）

        fading_lines = VGroup(example_directrix, envelope, envelope_directrix, line_to_apex, copy_to_apex, example_projectile)
        fading_points = VGroup(start_point, apex, example_point, example_focus, copy_apex)
        self.play(FadeOut(fading_lines, 0.5*DOWN), FadeOut(fading_points, 0.5*DOWN), FadeOut(base, 0.5*DOWN), ReplacementTransform(notice3, notice4))
        self.waiting(0, 24) #我们首先应该做的

        lemma_projectile = FunctionGraph(lambda x: -x**2/4 + 1, [-5, 5, 0.1], color = BLUE)
        lemma_focus = Dot(color = WHITE)
        lemma_label_focus = MTex(r"F").scale(0.8).next_to(ORIGIN, LEFT, buff = 0.2)
        lemma_directrix = Line(2*UP + 0* LEFT, 2*UP + 0*RIGHT)
        self.play(ShowCreation(lemma_projectile))
        lemma_projectile.close_path()
        self.play(lemma_projectile.animate.set_style(fill_opacity = 0.2), run_time = 0.4)
        self.play(lemma_projectile.animate.set_style(fill_opacity = 0), run_time = 0.4)
        self.play(lemma_projectile.animate.set_style(fill_opacity = 0.2), run_time = 0.4)
        self.play(lemma_projectile.animate.set_style(fill_opacity = 0), run_time = 0.4)
        self.play(lemma_projectile.animate.set_style(fill_opacity = 0.2), run_time = 0.4)
        self.waiting(0, 4) #是搞清楚什么是“一条抛物线的内部”
        self.waiting(0, 22) #（空闲）

        position_a = np.array([-2, 0, 0])
        position_b = np.array([3, -5/4, 0])
        point_a = Dot().shift(position_a)
        label_a = MTex(r"A").scale(0.8).next_to(position_a, UL, buff = 0.15)
        point_b = Dot().shift(position_b)
        label_b = MTex(r"B").scale(0.8).next_to(position_b, UR, buff = 0.15)
        line_a_b = Line(position_a, position_b)
        self.play(ShowCreation(point_a), Write(label_a), ShowCreation(point_b), Write(label_b), ReplacementTransform(notice4, notice5))
        self.play(ShowCreation(line_a_b))

        point_p = Dot().shift(position_a)
        label_p = MTex(r"P").scale(0.8).next_to(position_a, DOWN, buff = 0.2)
        text_p = MTex(r"\overrightarrow{AP}=t\cdot\overrightarrow{AB},\ t\in(0, 1)").scale(0.8).shift(2*UP)
        alpha = ValueTracker(0.6)
        beta = ValueTracker(0.0)
        def point_updater(point: Dot):
            rate = alpha.get_value()
            opacity = beta.get_value()
            point.move_to(rate * position_b + (1-rate) * position_a).set_opacity(opacity)
        point_p.add_updater(point_updater)
        def label_updater(text: MTex):
            rate = alpha.get_value()
            opacity = beta.get_value()
            text.next_to(rate * position_b + (1-rate) * position_a, DOWN, buff = 0.2).set_opacity(opacity)
        label_p.add_updater(label_updater)
        self.add(point_p, label_p)
        self.play(alpha.animate.set_value(0.0), beta.animate.set_value(1.0), Write(text_p), run_time = 1)
        self.play(alpha.animate.set_value(1.0))
        self.play(alpha.animate.set_value(0.4), beta.animate.set_value(0.0), FadeOut(VGroup(point_a, label_a, point_b, label_b, line_a_b, text_p)))
        self.waiting(2+2+1-5, 1+4+15) #这有不少刻画方式 而对于这个结论来说 最方便的方式
        self.add(lemma_directrix)
        self.play(ReplacementTransform(notice5, notice6), ShowCreation(lemma_focus), ShowCreation(lemma_label_focus), lemma_directrix.animate.put_start_and_end_on(2*UP + 5* LEFT, 2*UP + 5*RIGHT))
        self.waiting(1, 22) #是利用一个几何不等式

        mtex_1 = MTex(r"\Rightarrow AF<AC", isolate = [r"\Rightarrow", r"AF<AC"]).scale(0.8).shift(2.7*UP)
        mtex_1_1 = mtex_1.get_part_by_tex(r"\Rightarrow")
        mtex_1_2 = mtex_1.get_part_by_tex(r"AF<AC")
        mtex_2 = MTex(r"BA+AF=BF=BD<BA+AC").scale(0.8).shift(3.4*UP)
        position_a = np.array([2, -5/6, 0])
        position_c = np.array([2, 2, 0])
        position_d = np.array([3, 2, 0])
        point_a = Dot().shift(position_a)
        label_a = MTex(r"A").scale(0.8).next_to(position_a, DOWN, buff = 0.2)
        line_a_f = Line(position_a, ORIGIN)
        line_a_b = Line(position_a, position_b)
        point_c = Dot().shift(position_c)
        label_c = MTex(r"C").scale(0.8).next_to(position_c, UP, buff = 0.2)
        line_a_c = Line(position_a, position_c)
        elbow_c = Elbow(width = 0.25, angle = -PI/2, stroke_width = 3).shift(position_c)
        point_d = Dot().shift(position_d)
        label_d = MTex(r"D").scale(0.8).next_to(position_d, UP, buff = 0.2)
        line_b_d = Line(position_b, position_d)
        elbow_d = Elbow(width = 0.25, angle = -PI/2, stroke_width = 3).shift(position_d)
        self.play(ShowCreation(point_a), Write(label_a))
        self.waiting(0, 25) #一个抛物线内部的点
        self.play(ShowCreation(line_a_f))
        self.waiting(0, 6) #到焦点的距离......
        self.play(ShowCreation(line_a_c))
        self.play(ShowCreation(point_c), Write(label_c), ShowCreation(elbow_c), Write(mtex_1_2))
        self.waiting(0, 3) #要小于到准线的距离
        self.waiting(0, 19) #（空闲）
        
        self.waiting(2, 7) #证明起来也很简单
        self.play(ShowCreation(line_a_b))
        self.play(ShowCreation(point_b), Write(label_b), ShowCreation(line_b_d))
        self.play(ShowCreation(point_d), Write(label_d), ShowCreation(elbow_d))
        self.waiting(0, 21) #首先把FA延长至与抛物线相交
        self.play(Write(mtex_2))
        self.waiting(0, 9) #然后根据垂线段最短
        self.play(FadeIn(mtex_1_1, 0.5*RIGHT))
        self.waiting(0, 12) #就可以得到结论
        self.waiting(0, 28) #（空闲）

        self.waiting(1, 9) #知道了这一点
        traces = VGroup()
        for i in range(number):
            if i % 2:
                angle_i = PI * i / number - PI/2
            else:
                angle_i = - PI * (i+1) / number - PI/2
            color = angle_color(angle_i)
            trace_i = ParametricCurve(projectile_para(angle_i), [0, 12, 0.05], stroke_width = 2, stroke_opacity = 0.3, stroke_color = color)
            traces.add(trace_i)

        background.set_opacity(0.05)
        fading_group = VGroup(lemma_projectile, lemma_focus, lemma_label_focus, lemma_directrix, mtex_1, mtex_2, point_a, label_a, line_a_f, line_a_b, point_b, label_b, point_c, label_c, line_a_c, elbow_c, point_d, label_d, line_b_d, elbow_d)
        fading_lines = VGroup(example_directrix, envelope, envelope_directrix, line_to_apex, copy_to_apex)
        fading_points = VGroup(start_point, apex, copy_apex)
        self.play(FadeIn(traces, 0.5*UP), FadeIn(background, 0.5*UP), FadeIn(fading_lines, 0.5*UP), FadeIn(fading_points, 0.5*UP), FadeOut(fading_group, 0.5*UP), ReplacementTransform(notice6, notice7))
        self.waiting(1, 3) #就可以回来处理包络线了
        self.waiting(0, 21) #到此共77秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_2(Scene):
    def construct(self):

        notice7 = Notice("最后一步", "请　专注")
        notice8 = Notice("证明完毕", "请　鼓掌")
        notice9 = Notice("美妙性质", "请　欣赏")
        notice10 = Notice("图穷匕见", "请勿模仿")

        gravity = 1/9
        radius = 1/(4*gravity)
        def projectile_para(angle: float):
            return lambda t: t*unit(angle) + gravity*t*t*DOWN + DOWN

        start_point = Dot(color = BLUE).shift(DOWN)
        traces = VGroup()
        number = 100
        for i in range(number):
            if i % 2:
                angle_i = PI * i / number - PI/2
            else:
                angle_i = - PI * (i+1) / number - PI/2
            color = angle_color(angle_i)
            trace_i = ParametricCurve(projectile_para(angle_i), [0, 12, 0.05], stroke_width = 2, stroke_opacity = 0.3, stroke_color = color)
            traces.add(trace_i)
        
        envelope = FunctionGraph(quadratic(-gravity, 0, radius), [-64/9, 64/9, 0.1], color = BLUE).shift(DOWN)
        background = envelope.copy()
        background.close_path()
        background.set_style(stroke_width = 0, fill_opacity = 0.05, fill_color = BLUE)
        envelope_directrix = Line(DOWN + 2*radius*UP + 5*LEFT, DOWN + 2*radius*UP + 5*RIGHT, color = BLUE)
        example_directrix = Line(DOWN + radius*UP + 5*LEFT, DOWN + radius*UP + 5*RIGHT, color = YELLOW)
        apex = Dot(color = BLUE).shift(DOWN + radius*UP)
        line_to_apex = Line(DOWN + radius * UP, DOWN, color = RED)
        copy_apex = Dot(color = BLUE).shift(DOWN + 2*radius*UP)
        copy_to_apex = Line(DOWN + radius * UP, DOWN + 2 * radius * UP, color = RED)
        self.add(notice7, traces, background, line_to_apex, copy_to_apex, envelope, envelope_directrix, example_directrix, start_point, apex, copy_apex)
        
        example_angle = PI/3
        example_function = projectile_para(example_angle)
        start_focus_position = radius * unit(2*example_angle - PI/2) + DOWN
        start_position = example_function(7.0)
        start_pedal_position = np.array([start_position[0], radius - 1, 0])
        start_envelope_position = np.array([start_position[0], 2*radius - 1, 0])
        point_focus_distance = start_pedal_position[1] - start_position[1]

        example_projectile = ParametricCurve(example_function, [0, 12, 0.05]).set_color(angle_color(example_angle))
        example_focus = Dot(color = YELLOW).shift(start_focus_position)
        example_point = Dot(color = BLUE).move_to(start_position)
        example_focus_point = Line(start_position, start_focus_position, color = GREEN)
        example_pedal = Dot(color = BLUE).move_to(start_pedal_position)
        example_pedal_point = Line(start_position, start_pedal_position, color = GREEN)
        example_envelope_pedal = Dot(color = BLUE).move_to(start_envelope_position)
        example_pedals = Line(start_pedal_position, start_envelope_position, color = RED)
        
        self.add(example_projectile)
        self.bring_to_front(start_point)
        self.play(ShowCreation(example_projectile), ShowCreation(example_focus))
        self.waiting(0, 23) #对于任意一条轨迹上的......
        self.play(ShowCreation(example_point))
        self.waiting(0, 10) #......任意一点
        self.waiting(2, 3) #我们还是老样子
        self.waiting(3, 13) #首先 作出最常见的辅助线
        self.add(example_focus_point).bring_to_front(example_focus, example_point)
        self.play(ShowCreation(example_focus_point))
        self.waiting(0, 21) #和焦点的连线
        self.add(example_pedal_point).bring_to_front(example_point)
        self.play(ShowCreation(example_pedal_point))
        self.play(ShowCreation(example_pedal))
        self.waiting(0, 15) #到公共准线的垂线
        self.play(WiggleOutThenIn(example_focus_point), WiggleOutThenIn(example_pedal_point))
        self.waiting(0, 28) #这两条绿色线段是相等的
        self.add(example_pedals).bring_to_front(example_pedal)
        self.play(ShowCreation(example_pedals))
        self.play(ShowCreation(example_envelope_pedal))
        self.waiting(0, 13) #我们再把这条垂线延长
        self.play(WiggleOutThenIn(example_pedals))
        self.waiting(0, 1) #得到的这条红色线段
        target = copy_to_apex.copy()
        self.bring_to_back(target).play(TransformFromCopy(example_pedals, target))
        self.remove(target)
        self.waiting(1, 11) #就是两条准线之间的距离
        self.waiting(0, 20) #（空闲）

        focus_circle = Circle(radius = radius, stroke_width = 2, color = WHITE).rotate(PI/2).shift(DOWN)
        line_focus_start = Line(DOWN, start_focus_position, color = RED)
        self.add(focus_circle).bring_to_front(example_focus, apex)
        self.play(ShowCreation(focus_circle))
        self.add(line_focus_start).bring_to_front(start_point, example_focus)
        self.play(ShowCreation(line_focus_start))
        self.waiting(0, 21) #还记得我们之前得到的结论吗
        beta = ValueTracker(PI/3)
        def radius_updater(line: Line):
            angle = beta.get_value()
            line.put_start_and_end_on(DOWN, radius * unit(2*angle - PI/2) + DOWN)
        line_radius = line_focus_start.copy().add_updater(radius_updater)
        self.add(line_radius).bring_to_front(start_point, example_focus, apex, copy_apex)
        self.play(beta.animate.set_value(PI/2))
        line_radius.clear_updaters().save_state()
        self.waiting(2, 2) #起始点到焦点的距离是恒定的
        self.waiting(1, 11) #而这个距离
        beta = ValueTracker(3*PI/2)
        def radius_updater_2(line: Line):
            angle = beta.get_value()
            line.restore().shift(radius/2*UP + radius/2*unit(angle))
        line_radius.add_updater(radius_updater_2)
        self.play(beta.animate.set_value(PI/2))
        line_radius.clear_updaters()
        self.remove(line_radius)
        self.waiting(1, 18) #恰好就是两条准线之间的距离
        self.waiting(0, 22) #（空闲）

        line_point_start = Line(start_position, DOWN, color = YELLOW)
        self.waiting(3, 12) #那么 根据两点之间线段最短
        self.add(line_point_start).bring_to_front(start_point, example_point)
        self.play(ShowCreation(line_point_start))
        self.waiting(1, 5) #这一点到起始点的距离
        self.play(WiggleOutThenIn(line_focus_start), WiggleOutThenIn(example_focus_point))
        self.waiting(1, 14) #不大于红线段和绿线段长度的和
        
        vector_point_focus = start_focus_position - start_position
        beta = ValueTracker(np.arctan2(vector_point_focus[1], vector_point_focus[0]))
        gamma = ValueTracker(7*PI/6)
        def distance_1_updater(line: Line):
            angle = beta.get_value()
            line.put_start_and_end_on(start_position, start_position + point_focus_distance*unit(angle))
        distance_1 = example_focus_point.copy().add_updater(distance_1_updater)
        def distance_2_updater(line: Line):
            angle_0 = beta.get_value()
            angle_1 = gamma.get_value()
            position = start_position + point_focus_distance*unit(angle_0)
            line.put_start_and_end_on(position, position + radius*unit(angle_1))
        self.waiting(2, 1) #而红绿线段长度的和
        distance_2 = line_focus_start.copy().add_updater(distance_2_updater)
        self.add(distance_1, distance_2).bring_to_front(apex, start_point, example_focus, example_point, example_pedal, example_envelope_pedal)
        self.play(beta.animate.set_value(PI/2), gamma.animate.set_value(PI/2))
        distance_1.clear_updaters()
        distance_2.clear_updaters()
        self.remove(distance_1,distance_2)
        self.waiting(1, 21) #就是这一点到包络线准线的距离
        self.waiting(0, 21) #（空闲）

        self.waiting(1, 9) #也就是说
        self.play(WiggleOutThenIn(line_point_start), run_time = 1.5)
        self.waiting(0, 1) #这一点到焦点的距离......
        line_point_envelope = VGroup(example_pedal_point, example_pedals)
        self.add(line_point_envelope).bring_to_front(example_point, example_pedal, example_envelope_pedal)
        self.play(WiggleOutThenIn(line_point_envelope), run_time = 1.5)
        self.waiting(0, 17) #......不大于到准线的距离

        alpha = ValueTracker(7.0)
        target = 2*radius/np.sin(example_angle)
        def point_updater(point: Dot):
            t = alpha.get_value()
            point.move_to(example_function(t))
            if abs(t - target) < 0.2:
                point.set_color(YELLOW)
            else:
                point.set_color(BLUE)
        example_point.add_updater(point_updater)
        def to_focus_updater(line: Line):
            t = alpha.get_value()
            line.put_start_and_end_on(start_focus_position, example_function(t))
        example_focus_point.add_updater(to_focus_updater)
        def to_start_updater(line: Line):
            t = alpha.get_value()
            line.put_start_and_end_on(DOWN, example_function(t))
        line_point_start.add_updater(to_start_updater)
        def pedal_updater(point: Dot):
            t = alpha.get_value()
            point.move_to(np.array([example_function(t)[0], radius-1, 0]))
        example_pedal.add_updater(pedal_updater)
        def to_pedal_updater(line: Line):
            position = example_function(alpha.get_value())
            line.put_start_and_end_on(position, np.array([position[0], radius-1, 0]))
        example_pedal_point.add_updater(to_pedal_updater)
        def envelope_updater(point: Dot):
            t = alpha.get_value()
            point.move_to(np.array([example_function(t)[0], 2*radius-1, 0]))
        example_envelope_pedal.add_updater(envelope_updater)
        def to_envelope_updater(line: Line):
            position = example_function(alpha.get_value())
            line.put_start_and_end_on(np.array([position[0], radius-1, 0]), np.array([position[0], 2*radius-1, 0]))
        example_pedals.add_updater(to_envelope_updater)
        with_updater = [example_point, example_focus_point, line_point_start, example_pedal, example_pedal_point, example_envelope_pedal, example_pedals]
        self.play(alpha.animate.set_value(target), ReplacementTransform(notice7, notice8))
        self.waiting(1, 0) #它要不然在抛物线上
        self.play(alpha.animate.set_value(3.0), run_time = 1.0)
        self.play(alpha.animate.set_value(7.0), run_time = 1.4)
        for mob in with_updater:
            mob.suspend_updating()
        self.waiting(0, 2) #要不然在抛物线内部
        
        surrounding_1 = SurroundingRectangle(example_point)
        surrounding_2 = SurroundingRectangle(example_focus)
        surrounding_3 = SurroundingRectangle(start_point)
        self.waiting(1, 9) #并且 对于......
        self.play(ShowCreation(surrounding_1))
        self.waiting(0, 13) #......轨迹上的一点......
        self.play(ShowCreation(surrounding_2))
        self.waiting(0, 12) #......轨迹的焦点......
        self.play(ShowCreation(surrounding_3))
        self.waiting(0, 18)
        self.play(FadeOut(VGroup(surrounding_1, surrounding_2, surrounding_3))) #......和起始点这三个点来说
        self.play(WiggleOutThenIn(line_focus_start), WiggleOutThenIn(example_focus_point), WiggleOutThenIn(line_point_start))
        self.play(ShowCreationThenDestructionAround(example_point))
        self.waiting(1+3-3, 28+8) #如果它们不共线 那么轨迹上的点就在这条包络线内部
        for mob in with_updater:
            mob.resume_updating()

        example_projectile_adjoint = ParametricCurve(projectile_para(example_angle + PI), [0, 12, 0.05], stroke_color = angle_color(example_angle), stroke_opacity = 0.5)
        self.play(alpha.animate.set_value(target))
        self.add(example_projectile_adjoint).bring_to_front(apex, start_point, example_focus, example_point, example_pedal, example_envelope_pedal, copy_apex)
        self.play(ShowCreation(example_projectile_adjoint), example_directrix.animate.put_start_and_end_on(DOWN + radius*UP + 64/9*LEFT, DOWN + radius*UP + 64/9*RIGHT), envelope_directrix.animate.put_start_and_end_on(DOWN + 2*radius*UP + 64/9*LEFT, DOWN + 2*radius*UP + 64/9*RIGHT))
        self.waiting(0, 1) #如果它们三点共线
        for mob in with_updater:
            mob.clear_updaters()
        
        alpha = ValueTracker(PI/3)
        def tangent_point(angle: float):
            if angle % PI == PI/2:
                cot = 0
            elif angle % PI == 0:
                cot = 10000
            else:
                cot = 1/np.tan(angle)
            return np.array([cot/(2*gravity), (1-cot**2)/(4*gravity), 0]) + DOWN
        def point_updater(point: Dot):
            position = tangent_point(alpha.get_value())
            point.move_to(position)
        example_point.add_updater(point_updater)
        def to_focus_updater(line: Line):
            angle = alpha.get_value()
            position = tangent_point(angle)
            focus_position = radius * unit(2*angle - PI/2) + DOWN
            line.put_start_and_end_on(position, focus_position)
        example_focus_point.add_updater(to_focus_updater)
        def to_start_updater(line: Line):
            position = tangent_point(alpha.get_value())
            line.put_start_and_end_on(DOWN, position)
        line_point_start.add_updater(to_start_updater)
        def pedal_updater(point: Dot):
            position = tangent_point(alpha.get_value())
            point.move_to(np.array([position[0], radius-1, 0]))
        example_pedal.add_updater(pedal_updater)
        def to_pedal_updater(line: Line):
            position = tangent_point(alpha.get_value())
            line.put_start_and_end_on(position, np.array([position[0], radius-1, 0]))
        example_pedal_point.add_updater(to_pedal_updater)
        def envelope_updater(point: Dot):
            position = tangent_point(alpha.get_value())
            point.move_to(np.array([position[0], 2*radius-1, 0]))
        example_envelope_pedal.add_updater(envelope_updater)
        def to_envelope_updater(line: Line):
            position = tangent_point(alpha.get_value())
            line.put_start_and_end_on(np.array([position[0], radius-1, 0]), np.array([position[0], 2*radius-1, 0]))
        example_pedals.add_updater(to_envelope_updater)
        def focus_updater(point: Dot):
            position = radius * unit(2*alpha.get_value() - PI/2) + DOWN
            point.move_to(position)
        example_focus.add_updater(focus_updater)
        def to_focus_updater(line: Line):
            position = radius * unit(2*alpha.get_value() - PI/2) + DOWN
            line.put_start_and_end_on(DOWN, position)
        line_focus_start.add_updater(to_focus_updater)
        def projectile_updater(trace: Mobject):
            angle = alpha.get_value()
            curve = ParametricCurve(projectile_para(angle), [0, 12, 0.05])
            trace.set_color(angle_color(angle)).set_points(curve.get_all_points())
        example_projectile.add_updater(projectile_updater)
        def projectile_adjoint_updater(trace: Mobject):
            angle = alpha.get_value()
            curve = ParametricCurve(projectile_para(angle + PI), [0, 12, 0.05])
            trace.set_color(angle_color(angle)).set_points(curve.get_all_points())
        example_projectile_adjoint.add_updater(projectile_adjoint_updater)
        with_updater_points = [example_point, example_pedal, example_envelope_pedal, example_focus]
        with_updater_lines = [line_focus_start, example_focus_point, line_point_start, example_pedal_point, example_pedals, example_projectile, example_projectile_adjoint]
        animate = ApplyMethod(alpha.set_value, PI/6, run_time = 2, rate_func = rush_into)
        self.play(animate, ReplacementTransform(notice8, notice9))
        self.play(alpha.animate.set_value(-3*PI/2), rate_func = linear, run_time = 10)
        self.play(alpha.animate.set_value(-5*PI/3), rate_func = rush_from, run_time = 2)
        for mob in with_updater_points:
            mob.clear_updaters()
        for mob in with_updater_lines:
            mob.clear_updaters()
        self.waiting(2+2+0+3+2+2-14, 11+7+26+16+5+29) #那么这一点就在包络线上 是包络线和轨迹的切点 （空闲） 至此 我们完全解决了这个问题 通过焦点和准线来推导 可比直接计算要漂亮多了 对吧
        self.waiting(1, 5) #（空闲）

        fading_group = VGroup(traces, envelope, envelope_directrix, line_to_apex, copy_to_apex, *with_updater_lines, *with_updater_points, apex, copy_apex, start_point, focus_circle, example_directrix, background)
        self.play(ReplacementTransform(notice9, notice10))
        self.waiting(2, 2) #但这只是这一类问题中最简单的一个而已
        self.waiting(0, 17) #（空闲）
        self.play(FadeOut(fading_group))
        self.waiting(1, 20) #如果我们不在地面上抛出物体

        picture_earth = ImageMobject("earth.png", height = 0.5).shift(2*DOWN)
        picture_moon = ImageMobject("moon.png", height = 0.2).shift(1.3*DOWN)
        source = Dot(color = BLUE).shift(2*UP)
        trace = Circle(radius = 0.7, stroke_width = 2, color = WHITE).shift(2*DOWN)
        picture_moon.angle = 0
        beta = ValueTracker(0.0)
        def moon_updater(moon: ImageMobject, dt):
            moon.angle += dt
            moon.move_to(2*DOWN + 0.7*unit(moon.angle))
        def opacity_updater(mob: Mobject):
            mob.set_opacity(beta.get_value())
        def Vopacity_updater(mob: VMobject):
            mob.set_style(stroke_opacity = beta.get_value())
        picture_moon.add_updater(moon_updater).add_updater(opacity_updater)
        picture_earth.add_updater(opacity_updater)
        trace.add_updater(Vopacity_updater)
        self.add(trace, picture_earth, picture_moon)
        self.play(beta.animate.set_value(1.0), ShowCreation(source))
        self.waiting(0, 19) #而改到天空中

        ellipses = VGroup()
        starts = VGroup()
        orbits = VGroup()
        trace_paths = VGroup()
        number = 24
        for i in range (number):
            angle = i*TAU/number + PI/number
            color = angle_color(2*angle)
            ellipse_i = ParameterTrace(2*DOWN, 2*UP, 6, angle, stroke_color = color, GM = 18.5)
            ellipses.add(ellipse_i)
            start = Dot(color = BLUE).move_to(ellipse_i.point_from_proportion(0)).add_updater(opacity_updater)
            
            orbit = DifferentialOrbiting(ellipse_i, start, stop = False)
            starts.add(start)
            orbits.add(orbit)
            
            traces_path_i = TracedPath(start.get_center).set_color(color).add_updater(Vopacity_updater)
            trace_paths.add(traces_path_i)
        self.remove(source).add(trace_paths, starts, orbits).bring_to_front(picture_earth, picture_moon)
        self.waiting(2, 29) #能覆盖到的范围 又会是什么样的呢
        self.waiting(8, 8)
        self.play(beta.animate.set_value(0.0), FadeOut(notice10))
        self.waiting(3, 0) #到此共110秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)
        
#########################################################################

class Chapter3_0(Scene):

    def construct(self):

        ##  Making object
        text3 = Text("第三节 高速抛体的范围", font = 'simsun', t2c={"第三节": YELLOW, "高速抛体": GREEN, "范围": BLUE})

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(Scene):

    def construct(self):
        notice1 = Notice("前置知识", "请点科技")
        notice2 = Notice("强势安利", "快 去 看")
        notice3 = Notice("暴力计算", "请　阻止")
        
        ellipse_ellipse = ParameterTrace(0.5*DOWN + 3.5*LEFT, 3.5*UP + 3.5*LEFT, 6, PI/2, stroke_color = WHITE, GM = 18.5)
        trace_ellipse = ParametricCurve(ellipse_ellipse.parameter_function, [0, TAU, TAU/100])
        earth_ellipse = ImageMobject("earth.png", height = 0.5).shift(0.5*DOWN + 3.5*LEFT)
        moon_ellipse = ImageMobject("moon.png", height = 0.2).shift(3.5*UP + 3.5*LEFT)
        orbit_ellipse = DifferentialOrbiting(ellipse_ellipse, moon_ellipse, stop = False)

        circle_circle = ParameterTrace(0.5*UP + 3.5*LEFT, 3.5*UP + 3.5*LEFT, 6, PI/2, stroke_color = WHITE, GM = 18.5)
        trace_circle = ParametricCurve(circle_circle.parameter_function, [0, TAU, TAU/100])
        earth_circle = ImageMobject("earth.png", height = 0.5).shift(0.5*UP + 3.5*LEFT)
        moon_circle = ImageMobject("moon.png", height = 0.2).shift(3.5*UP + 3.5*LEFT)
        orbit_circle = DifferentialOrbiting(circle_circle, moon_circle, stop = False)

        alpha = ValueTracker(0.0)
        def stroke_updater_a(mob: VMobject):
            mob.set_style(stroke_opacity = alpha.get_value())
        def opacity_updater_a(mob: Mobject):
            mob.set_opacity(alpha.get_value())
        earth_ellipse.add_updater(opacity_updater_a)
        moon_ellipse.add_updater(opacity_updater_a)
        trace_ellipse.add_updater(stroke_updater_a)

        beta = ValueTracker(0.0)
        def stroke_updater_b(mob: VMobject):
            mob.set_style(stroke_opacity = beta.get_value())
        def opacity_updater_b(mob: Mobject):
            mob.set_opacity(beta.get_value())
        earth_circle.add_updater(opacity_updater_b)
        moon_circle.add_updater(opacity_updater_b)
        trace_circle.add_updater(stroke_updater_b)
        
        self.add(earth_ellipse, trace_ellipse, moon_ellipse, orbit_ellipse, earth_circle, trace_circle, moon_circle, orbit_circle)
        self.play(alpha.animate.set_value(1.0), Write(notice1))
        self.waiting(1, 20) #这一节就要涉及到天体运动了

        kepler_1_ellipse = MTex(r"1.\ r(\theta)=\frac{ep}{1-e\cos\theta}").scale(0.8).next_to(2*UP + 0.5*RIGHT)
        kepler_2_ellipse = MTex(r"2.\ r^2\dot\theta=\sqrt{GM\frac{b^2}{a}}").scale(0.8).next_to(0.5*UP + 0.5*RIGHT)
        kepler_3_ellipse = MTex(r"3.\ \frac{T^2}{a^3}=\frac{4\pi^2}{GM}").scale(0.8).next_to(DOWN + 0.5*RIGHT)
        kepler_ellipse = VGroup(kepler_1_ellipse, kepler_2_ellipse, kepler_3_ellipse)

        kepler_1_circle = MTex(r"1.\ r(\theta)=r_0").scale(0.8).next_to(2*UP + 0.5*RIGHT)
        kepler_2_circle = MTex(r"2.\ \omega=\sqrt{\frac{GM}{r_0^3}}").scale(0.8).next_to(0.5*UP + 0.5*RIGHT)
        kepler_3_circle = MTex(r"3.\ \frac{T^2}{r_0^3}=\frac{4\pi^2}{GM}").scale(0.8).next_to(DOWN + 0.5*RIGHT)
        kepler_circle = VGroup(kepler_1_circle, kepler_2_circle, kepler_3_circle)

        self.play(Write(kepler_ellipse))
        self.waiting(1, 10) #主要的推导将依赖开普勒三定律进行
        self.waiting(2, 27) #虽然开普勒三定律是高中课内内容
        self.waiting(2, 20) #但对于没有参加物理竞赛的同学
        self.waiting(1, 13) #在高中阶段
        self.play(alpha.animate.set_value(0.0), beta.animate.set_value(1.0), FadeOut(kepler_ellipse), FadeIn(kepler_circle))
        self.remove(earth_ellipse, trace_ellipse, moon_ellipse, orbit_ellipse)
        self.waiting(2, 4) #可能只接触了圆轨道下的开普勒三定律
        self.waiting(1, 0)
        self.play(beta.animate.set_value(0.0), FadeOut(kepler_circle)) #不太熟悉一般的情况
        self.remove(earth_circle, trace_circle, moon_circle, orbit_circle)
        self.waiting(0, 27) #（空闲）

        picture_video = ImageMobject("picture_video.jpg", height = 2)
        text_video = Text("BV1Zs411A7KJ", font = "Times New Roman").scale(0.5).next_to(picture_video, UP)
        group_cover = Group(picture_video, text_video)
        rectangle_video = Rectangle(height = 5.5, width = 5*16/9 + 0.5).shift(2*LEFT)
        self.play(FadeIn(picture_video), Write(text_video), ReplacementTransform(notice1, notice2))
        self.waiting(2, 2) #3蓝1棕做过一期珠玉在前的视频
        self.play(group_cover.animate.shift(5*RIGHT), ShowCreation(rectangle_video))
        self.waiting(2, 29) #详细讲述了从万有引力定律和开普勒第二定律
        self.waiting(2, 22) #推导开普勒第一定律的方法
        self.waiting(3, 8) #如果大家好奇行星的轨道为什么是椭圆
        self.waiting(1+0-1, 20+27)
        self.play(FadeOut(rectangle_video), FadeOut(group_cover)) #可以去那里看一看 （空闲）

        text_1 = r"\begin{pmatrix}\hat{r} \\ \hat{\theta}\end{pmatrix}"
        text_2 = r"=\begin{pmatrix}\cos\theta & \sin\theta \\ -\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}\hat\imath\\\hat\jmath\end{pmatrix}"
        text_3 = r"\Rightarrow\begin{pmatrix}\dot{\hat{r}}\\\dot{\hat{\theta}}\end{pmatrix}"
        text_4 = r"=\frac{d}{dt}\begin{pmatrix}\cos\theta & \sin\theta \\ -\sin\theta & \cos\theta\end{pmatrix}\begin{pmatrix}\hat\imath\\\hat\jmath\end{pmatrix}"
        text_5 = r"=\begin{pmatrix}-\dot\theta\sin\theta & \dot\theta\cos\theta \\ -\dot\theta\cos\theta & -\dot\theta\sin\theta\end{pmatrix}\begin{pmatrix}\hat\imath\\\hat\jmath\end{pmatrix}"
        text_6 = r"=\dot\theta\begin{pmatrix}\hat{\theta} \\ -\hat{r}\end{pmatrix}"
        mtex_1 = MTex(text_1 + text_2 + text_3 + text_4 + text_5 + text_6).scale(0.5).next_to(3.6*UP + 7*LEFT)
        text_1 = r"\Rightarrow\vec{v}=\frac{d}{dt}\vec{r}=\frac{d}{dt}(r\hat{r})=\dot{r}\hat{r}+r\dot{\hat{r}}=\dot{r}\hat{r}+r\dot\theta\hat\theta"
        mtex_2 = MTex(text_1).scale(0.5).next_to(2.96*UP + 7*LEFT)
        text_1 = r"\Rightarrow\vec{a}=\frac{d}{dt}\vec{v}=\frac{d}{dt}(\dot{r}\hat{r}+r\dot\theta\hat\theta)"
        text_2 = r"=(\ddot{r}\hat{r}+\dot{r}\dot{\hat{r}})+(\dot{r}\dot{\theta}\hat{\theta}+r\ddot\theta\hat\theta+r\dot\theta(-\dot\theta\hat{r}))"
        text_3 = r"=(\ddot{r}-r\dot\theta^2)\hat{r}+(2\dot{r}\dot\theta+r\ddot\theta)\hat\theta=:a_r\hat{r}+a_\theta\hat\theta"
        mtex_3 = MTex(text_1 + text_2 + text_3).scale(0.5).next_to(2.32*UP + 7*LEFT)
        line_1 = Line(64/9*LEFT+1.9*UP, 64/9*RIGHT+1.9*UP)
        text_1 = r"\vec{F}=-\frac{GMm}{r^2}\hat{r}\Rightarrow\begin{cases}a_r=-\frac{GM}{r^2}\\a_\theta=0\end{cases}"
        text_2 = r"\Rightarrow 0=a_\theta=2\dot{r}\dot\theta+r\ddot\theta=\frac{1}{r}\frac{d}{dt}(r^2\dot\theta)\qquad\Rightarrow r^2\dot\theta = h"
        text_3 = r"\qquad\Rightarrow \frac{d}{dt}=\frac{d\theta}{dt}\frac{d}{d\theta}=\frac{h}{r^2}\frac{d}{d\theta}"
        mtex_4 = MTex(text_1 + text_2 + text_3).scale(0.5).next_to(1.4*UP + 7*LEFT)
        text_1 = r"u:=\frac{1}{r}\qquad \Rightarrow \dot{r}=\frac{d}{dt}\left(\frac{1}{u}\right)=-\frac{1}{u^2}\frac{d}{dt}u=-r^2\left(\frac{h}{r^2}\frac{du}{d\theta}\right)=-h\frac{du}{d\theta}"
        text_2 = r"\qquad \Rightarrow \ddot{r}=\frac{d}{dt}\dot{r}=\left(\frac{h}{r^2}\frac{d}{d\theta}\right)\left(-h\frac{du}{d\theta}\right)=-\frac{h^2}{r^2}\frac{d^2u}{d\theta^2}"
        mtex_5 = MTex(text_1 + text_2).scale(0.5).next_to(0.7*UP + 7*LEFT)
        text_1 = r"\Rightarrow -\frac{GM}{r^2}=a_r=\ddot{r}-r\dot\theta^2 = -\frac{h^2}{r^2}\frac{d^2u}{d\theta^2}-r\left(\frac{h}{r^2}\right)^2=-\frac{h^2}{r^2}\left(\frac{d^2u}{d\theta^2} + u\right)"
        text_2 = r"\qquad\Rightarrow \frac{d^2u}{d\theta^2}+u = \frac{GM}{h^2}"
        mtex_6 = MTex(text_1 + text_2).scale(0.5).next_to(7*LEFT)
        text_1 = r"\Rightarrow u=\frac{GM}{h^2}-A\cos(\theta + \phi)\qquad\Rightarrow "
        text_2 = r"r=\frac{ep}{1-e\cos(\theta + \phi)}"
        text_3 = r",\ (e, p):=\left(\frac{h^2}{GM}A,\ \frac{1}{A}\right)"
        mtex_7 = MTex(text_1 + text_2 + text_3, isolate = [text_2]).scale(0.5).next_to(0.7*DOWN + 7*LEFT)
        indicate_1 = SurroundingRectangle(mtex_7.get_part_by_tex(text_2))
        line_2 = Line(64/9*LEFT+1.15*DOWN, 64/9*RIGHT+1.15*DOWN)
        text_1 = r"\Rightarrow A=\frac{1}{p}=\frac{c}{b^2},\ h=\sqrt{GM\frac{e}{A}}=\sqrt{GM\frac{b^2}{a}} \qquad\Rightarrow "
        text_2 = r"r^2\dot\theta = \sqrt{GM\frac{b^2}{a}}"
        mtex_8 = MTex(text_1 + text_2, isolate = [text_2]).scale(0.5).next_to(1.6*DOWN + 7*LEFT)
        indicate_2 = SurroundingRectangle(mtex_8.get_part_by_tex(text_2))
        text_1 = r"\frac{1}{2}hT=S=\pi ab\qquad\Rightarrow T=\frac{2\pi ab}{h}=2\pi ab\sqrt{\frac{a}{GMb^2}}=\sqrt{\frac{4\pi^2 a^3}{GM}}\qquad\Rightarrow "
        text_2 = r"\frac{T^2}{a^3}=\frac{4\pi^2}{GM}"
        mtex_9 = MTex(text_1 + text_2, isolate = [text_2]).scale(0.5).next_to(2.4*DOWN + 7*LEFT)
        indicate_3 = SurroundingRectangle(mtex_9.get_part_by_tex(text_2))

        group_1 = VGroup(mtex_1, mtex_2, mtex_3)
        group_2 = VGroup(mtex_4, mtex_5, mtex_6, mtex_7)
        group_3 = VGroup(mtex_8, mtex_9)
        group_all = VGroup(mtex_1, mtex_2, mtex_3, line_1, mtex_4, mtex_5, mtex_6, mtex_7, indicate_1, line_2, mtex_8, indicate_2, mtex_9, indicate_3)
        self.play(ReplacementTransform(notice2, notice3), Write(group_1))
        self.play(ShowCreation(line_1))
        self.play(Write(group_2))
        self.play(ShowCreation(line_2), ShowCreation(indicate_1))
        self.play(Write(group_3))
        self.play(ShowCreation(indicate_2), ShowCreation(indicate_3))
        self.waiting(3+1+2+3-9, 8+25+2+0) #当然 即使不熟悉开普勒三定律  也不用太紧张 这里是一个数学频道 不会涉及什么大篇幅的物理推导
        self.waiting(1, 25) #我们这一节所要用到的
        self.play(SwallowIn(group_all, ORIGIN))
        self.waiting(0, 13) #仅仅是非常基础的运算而已
        self.waiting(0, 28) #到此共50秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)


class Chapter3_2(Scene):

    def construct(self):
        notice3 = Notice("暴力计算", "请　阻止")
        notice4 = Notice("问题引入", "请　思考")
        notice5 = Notice("前情提要", "请　复习")
        notice6 = Notice("射影几何", "请　选修*")
        notice7 = Notice("照猫画虎", "请　模仿")
        self.add(notice3)

        earth = ImageMobject("earth.png", height = 0.5).shift(2*DOWN)
        source = Dot(color = BLUE).shift(2*UP)
        vector_velocity = Arrow(2*UP, 3*UP, buff = 0)
        text_velocity = MTex(r"\vec{v}_0").next_to(vector_velocity, UP)
        velocity = VGroup(vector_velocity, text_velocity)

        self.play(ReplacementTransform(notice3, notice4), FadeInFromPoint(earth, 2*DOWN))
        self.waiting(1, 23) #在一个中心天体的引力作用下
        self.play(ShowCreation(source), rate_func = rush_into)
        self.waiting(2+1-3, 19+29)
        self.add(velocity).bring_to_front(source)
        self.play(FadeInFromPoint(velocity, 2*UP))
        self.play(Rotate(velocity, TAU, about_point = 2*UP)) #我们从高空中的一个起始点 保持速度大小不变

        alpha = ValueTracker(1.0)
        def opacity_updater(mob: VMobject):
            opacity = alpha.get_value()
            mob.set_opacity(opacity)
        ellipses = VGroup()
        starts = VGroup()
        orbits = VGroup()
        trace_paths = VGroup()
        number = 24
        for i in range (number):
            angle = i*TAU/number + PI/number
            color = angle_color(2*angle)
            ellipse_i = ParameterTrace(2*DOWN, 2*UP, 6, angle, stroke_color = color, GM = 18.5)
            ellipses.add(ellipse_i)
            start = Dot(color = RED).move_to(ellipse_i.point_from_proportion(0))
            
            orbit = DifferentialOrbiting(ellipse_i, start, stop = False).add_updater(opacity_updater)
            starts.add(start)
            orbits.add(orbit)
            
            traces_path_i = TracedPath(start.get_center).set_color(color)
            trace_paths.add(traces_path_i)
        self.add(trace_paths, orbits).bring_to_front(earth, source)
        self.play(FadeOut(velocity), run_time = 0.5) 
        self.waiting(1.5, 22) #向四面八方抛出物体
        self.waiting(2, 3) #这样的所有抛体的轨道

        def ellipse_envelope(t: float):
            return np.array([2*np.sqrt(3)*np.cos(t), 4*np.sin(t), 0])
        envelope = ParametricCurve(ellipse_envelope, [PI/2, TAU+PI/2, TAU/100], color = BLUE)
        self.add(envelope).bring_to_front(orbits)
        self.play(ShowCreation(envelope))
        self.waiting(1, 6) #包络线似乎是一个椭圆
        self.waiting(0, 16) #（空闲）
        for mob in trace_paths:
            mob.clear_updaters()

        surrounding_1 = SurroundingRectangle(source)
        surrounding_2 = SurroundingRectangle(earth)
        position_point = np.array([3*np.sqrt(5)/2, 1, 0])
        line_to_source = Line(position_point, 2*UP)
        line_to_earth = Line(position_point, 2*DOWN)
        point = Dot(color = BLUE).shift(position_point)
        self.play(trace_paths.animate.fade(), alpha.animate.set_value(0.5))
        self.waiting(0, 2) #并且......
        self.play(ShowCreation(surrounding_1))
        self.waiting(0, 2) #......起始点......
        self.play(ShowCreation(surrounding_2))
        self.waiting(0, 16) #......和中心天体
        self.add(line_to_source, line_to_earth).bring_to_front(source, earth, point)
        self.play(ShowCreation(point), ShowCreation(line_to_source), ShowCreation(line_to_earth))
        self.waiting(2+0-2, 9+28) 
        fading_group = Group(line_to_source, line_to_earth, envelope, trace_paths, surrounding_1, surrounding_2, source, point, earth)
        self.play(FadeOut(fading_group), alpha.animate.set_value(0.0))#似乎是这个椭圆的两个焦点 （空闲）
        for mob in orbits:
            mob.clear_updaters()
        self.remove(orbits)

        gravity = 1/2
        radius = 1/(4*gravity)
        def projectile_para(angle: float):
            return lambda t: t*unit(angle) + gravity*t*t*DOWN

        start_point = Dot(color = BLUE)
        traces = []
        number = 48
        for i in range(number):
            if i % 2:
                angle_i = PI * i / number - PI/2
            else:
                angle_i = - PI * (i+1) / number - PI/2
            color = angle_color(angle_i)
            trace_i = ParametricCurve(projectile_para(angle_i), [0, 4, 0.05], stroke_width = 2, stroke_color = color)
            traces.append(trace_i)
        self.play(ShowCreation(start_point), ReplacementTransform(notice4, notice5))
        self.bring_to_back(*traces)
        self.play(*[ShowCreation(trace) for trace in traces])
        self.waiting(0, 11) #想一想我们之前研究过的

        def limit_para(eccentricity: float):
            def util(theta: float):
                r = 2*radius/(1-eccentricity*np.sin(theta))
                return r*unit(-theta)
            return util
        envelope_para = ParametricCurve(limit_para(1), [-3*PI/2 + PI/6, PI/2 -PI/6, PI/100], color = BLUE)
        envelope_copy = ParametricCurve(limit_para(0.99), [-3*PI/2 + PI/6, PI/2 -PI/6, PI/100], color = BLUE).shift(32/9*LEFT)
        focus_copy = Dot(color = YELLOW).shift(32/9*LEFT)
        spliting_line = Line(4*UP, 4*DOWN)
        envelope_limit = ParametricCurve(limit_para(0.99), [-3*PI/2, PI/2, PI/100], color = BLUE).shift(32/9*LEFT)

        self.play(ShowCreation(envelope_para))
        self.waiting(1, 24) #在地面附近的抛体的包络线
        self.play(envelope_para.animate.shift(32/9*RIGHT), *[trace.animate.shift(32/9*RIGHT) for trace in traces], start_point.animate.shift(32/9*RIGHT), TransformFromCopy(envelope_para, envelope_copy), TransformFromCopy(start_point, focus_copy))
        self.play(*[trace.animate.set_style(stroke_opacity = 0.5) for trace in traces], ShowCreation(spliting_line))
        self.waiting(0, 18) #这条包络线是抛物线
        self.play(ShowCreationThenFadeAround(start_point), ShowCreationThenFadeAround(focus_copy), run_time = 2.0)
        self.waiting(1+0-2, 25+25) #起始点是它的焦点 （空闲）
        
        self.add(envelope_limit).remove(envelope_copy).bring_to_front(focus_copy)
        self.play(ReplacementTransform(notice5, notice6))
        self.waiting(2, 16) #大家可能或多或少听说过这么一个观点
        line_infinity = Line(3*DOWN + 64/9*LEFT, 3*DOWN)
        focus_infinity = Dot(color = YELLOW).shift(32/9*LEFT + 3*DOWN)
        text_infinity = Text("无穷远", font = "simsun").scale(0.5).next_to(line_infinity, DOWN, buff = 0.1).shift(2*LEFT)
        text_infinity_2 = Text("Infinity", font = "Times New Roman").scale(0.5).next_to(line_infinity, UP, buff = 0.1).shift(2*LEFT)
        self.play(envelope_limit.animate.scale((1-0.99**2)*0.99*3, about_point = UP + 32/9*LEFT).shift(2*UP), focus_copy.animate.scale((1-0.99**2)*0.99*3, about_point = UP + 32/9*LEFT).scale(50/3).shift(2*UP), run_time = 2, rate_func = rush_into)
        self.waiting(0, 11) #抛物线也有两个焦点
        self.bring_to_back(line_infinity)
        self.play(ShowCreation(line_infinity))
        self.play(ShowCreation(focus_infinity), Write(text_infinity), Write(text_infinity_2))
        self.waiting(1, 0) #它的另一个焦点是无穷远点

        def norm_color(norm):
            colors = [RED, ORANGE, YELLOW, GREEN]
            ratio = 3*(norm - 1)/(np.sqrt(45)-1)
            index = int(ratio)
            interpolate = ratio - index
            return interpolate_color(colors[index], colors[(index+1)%4], interpolate)

        vectors_near = []
        for y in range(-3, 3):
            for x in range(-3, 4):
                position = np.array([x+32/9, y, 0])
                vector = Arrow(position, position+0.4*DOWN, buff = 0, color = norm_color(6))
                vectors_near.append(vector)
        vectorvield_near = VGroup(*vectors_near)

        def function_gravity(position):
            vector = position - np.array([-32/9, -3, 0])
            norm = get_norm(vector)
            return -0.4*vector/norm, norm
        vectors_far = []
        for y in range(-2, 4):
            for x in range(-3, 4):
                position = np.array([x-32/9, y, 0])
                gravity, norm = function_gravity(position)
                vector = Arrow(position, position + gravity, buff = 0, color = norm_color(norm))
                vectors_far.append(vector)
        vectorvield_far = VGroup(*vectors_far)

        self.waiting(1, 9) #同时......
        self.bring_to_back(vectorvield_near)
        self.play(FadeIn(vectorvield_near), lag_ratio = 0.02)
        self.waiting(0, 25) #......地面附近的重力场
        self.bring_to_back(vectorvield_far)
        self.play(FadeIn(vectorvield_far), lag_ratio = 0.02)
        self.waiting(0, 28) #就指向这个无穷远点
        self.waiting(0, 20) #（空闲）


        envelope_para_copy = envelope_para.copy().set_color(YELLOW)
        self.waiting(1, 2) #同时......
        self.play(ShowCreation(envelope_para_copy))
        self.waiting(1, 1) #......这个包络线的两个焦点
        self.play(ShowCreationThenFadeAround(focus_copy), ShowCreationThenFadeAround(focus_infinity))
        self.waiting(0, 17) #也是起始点和中心天体
        self.waiting(0, 28) #（空闲）

        fading_group = VGroup(vectorvield_far, line_infinity, envelope_limit, focus_copy, focus_infinity, text_infinity, text_infinity_2, envelope_para_copy)
        position_earth = 2*DOWN
        position_source = 2*UP
        length_major_axis = 6
        earth = ImageMobject("earth.png", height = 0.5).shift(position_earth + 32/9*LEFT)
        source = Dot(color = BLUE).shift(position_source + 32/9*LEFT)
        envelope = ParametricCurve(ellipse_envelope, [PI/2, TAU+PI/2, TAU/100], color = BLUE).shift(32/9*LEFT)
        envelope_copy = envelope.copy().set_color(YELLOW)
        ellipses = VGroup()
        number = 48
        for i in range (number):
            angle = i*TAU/number + PI/number
            color = angle_color(2*angle)
            ellipse_i = ParameterTrace(position_earth, position_source, length_major_axis, angle, stroke_color = color, stroke_width = 2, stroke_opacity = 0.5, GM = 20)
            ellipses.add(ellipse_i)
        ellipses.shift(32/9*LEFT).set_style(stroke_opacity = 0.5)
        self.play(FadeOut(fading_group), FadeOut(vectorvield_near), FadeIn(ellipses), FadeIn(earth), FadeIn(source), FadeIn(envelope), ReplacementTransform(notice6, notice7))
        self.waiting(0, 11) #这么一看
        self.play(ShowCreationThenDestruction(envelope_copy), run_time = 2)
        self.waiting(1, 10) #在宇宙中 向四面八方抛出物体
        self.play(ShowCreationThenDestruction(envelope_para_copy), run_time = 2)
        self.waiting(1, 22) #和在地面附近 向四面八方抛出物体
        self.waiting(2, 2) #实在是很像

        moving_group = Group(ellipses, earth, source, envelope)
        fading_group = VGroup(envelope_para, start_point, spliting_line)
        start_angle = PI/2
        alpha = ValueTracker(start_angle)
        beta = ValueTracker(0.0)
        gamma = ValueTracker(0.0)
        trace_example = ParameterTrace(position_earth, position_source, length_major_axis, start_angle, stroke_color = angle_color(2*start_angle), GM = 20)
        directrix_example = trace_example.get_directrix().set_color(YELLOW)
        focus_example = trace_example.get_focus().set_color(YELLOW)
        def trace_updater(trace: ParameterTrace):
            angle = alpha.get_value()
            curve = ParameterTrace(position_earth, position_source, length_major_axis, angle, GM = 20)
            trace.set_style(stroke_color = angle_color(2*angle)).set_points(curve.get_all_points())
        def directrix_updater(line: Line):
            angle = alpha.get_value()
            opacity = beta.get_value()
            curve = ParameterTrace(position_earth, position_source, length_major_axis, angle, GM = 20)
            line.set_opacity(opacity).set_points(curve.get_directrix().get_all_points())
        def focus_updater(point: Dot):
            angle = alpha.get_value()
            opacity = gamma.get_value()
            curve = ParameterTrace(position_earth, position_source, length_major_axis, angle, GM = 20)
            point.set_opacity(opacity).set_points(curve.get_focus().get_all_points())
            
        self.play(*[FadeOut(trace, 32/9*RIGHT) for trace in traces], FadeOut(fading_group, 32/9*RIGHT), moving_group.animate.shift(32/9*RIGHT))
        self.add(trace_example).bring_to_front(earth, source)
        self.play(ShowCreation(trace_example), ellipses.animate.set_style(stroke_opacity = 0.3), envelope.animate.set_style(fill_opacity = 0.1))
        trace_example.add_updater(trace_updater)
        self.add(directrix_example, focus_example)
        directrix_example.add_updater(directrix_updater)
        focus_example.add_updater(focus_updater)

        self.play(alpha.animate.set_value(PI*2/3), rate_func = rush_into)
        self.play(alpha.animate.set_value(PI), rate_func = linear)
        self.play(alpha.animate.set_value(PI*4/3), rate_func = linear) #既然像 那就可能能用同样的方法来解决问题 （空闲）......
        self.play(alpha.animate.set_value(PI*5/3), beta.animate.set_value(1.0), rate_func = linear)
        self.play(alpha.animate.set_value(TAU), rate_func = linear)
        self.play(alpha.animate.set_value(PI*7/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*8/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*3), beta.animate.set_value(0.0), rate_func = linear) #轨道的主轴有角度变化 准线估计是利用不上了......
        self.play(alpha.animate.set_value(PI*10/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*11/3), gamma.animate.set_value(1.0), rate_func = linear)
        self.play(alpha.animate.set_value(PI*4), rate_func = linear) #但是焦点呢 我们画出另一个焦点来试试看
        self.play(alpha.animate.set_value(PI*13/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*14/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*5), rate_func = linear)
        focus_trace = TracedPath(focus_example.get_center, opacity = 0.5)
        self.add(focus_trace).bring_to_front(trace_example, focus_example, earth, source)
        self.play(alpha.animate.set_value(PI*16/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*17/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*6), rate_func = linear)
        self.play(alpha.animate.set_value(PI*19/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*20/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*7), rate_func = linear)
        self.play(alpha.animate.set_value(PI*22/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*15/2), rate_func = rush_from) #别问我为什么不合成一个，问就是调参调出来的
        self.waiting(2, 0) #到此共90秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_3(Scene):

    def construct(self):
        notice7 = Notice("照猫画虎", "请　模仿")
        notice8 = Notice("现象总结", "请注意到")
        notice9 = Notice("基础知识", "请记笔记")
        notice10 = Notice("现象总结", "请注意到")
        notice11 = Notice("暴力计算", "请　阻止")
        notice12 = Notice("优美证法", "请　欣赏")
        notice13 = Notice("暴力计算", "请　阻止")
        notice14 = Notice("优美证法", "请　欣赏")
        self.add(notice7)

        def ellipse_envelope(t: float):
            return np.array([2*np.sqrt(3)*np.cos(t), 4*np.sin(t), 0])
        position_earth = 2*DOWN
        position_source = 2*UP
        length_major_axis = 6
        focus_radius = length_major_axis - get_norm(position_earth - position_source)
        start_angle = PI/2
        earth = ImageMobject("earth.png", height = 0.5).shift(position_earth)
        source = Dot(color = BLUE).shift(position_source)
        envelope = ParametricCurve(ellipse_envelope, [PI/2, TAU+PI/2, TAU/100], color = BLUE, fill_opacity = 0.1)
        ellipses = VGroup()
        number = 48
        for i in range (number):
            angle = i*TAU/number + PI/number
            color = angle_color(2*angle)
            ellipse_i = ParameterTrace(position_earth, position_source, length_major_axis, angle, stroke_color = color, stroke_width = 2, stroke_opacity = 0.3, GM = 20)
            ellipses.add(ellipse_i)
        trace_example = ParameterTrace(position_earth, position_source, length_major_axis, start_angle, stroke_color = angle_color(2*start_angle), GM = 20)
        focus_example = trace_example.get_focus().set_color(YELLOW)
        focus_trace = Circle(radius = focus_radius, opacity = 0.5, stroke_width = 2, color = WHITE).shift(position_source)
        background = VGroup(ellipses, envelope, focus_trace)
        self.add(background, trace_example, focus_example, earth, source)
        self.play(ReplacementTransform(notice7, notice8))
        self.waiting(1, 22) #看起来焦点的轨迹仍然是一个圆
        self.waiting(0, 16) #（空闲）

        line_to_earth = Line(position_earth, position_source, color = RED)
        line_to_focus = Line(focus_example.get_center(), position_source, color = RED)
        major_axis = trace_example.get_major_axis().set_opacity(0.0).set_color(YELLOW)
        alpha = ValueTracker(start_angle)
        beta = ValueTracker(0.0)
        gamma = ValueTracker(1.0)
        def trace_updater(trace: ParameterTrace):
            angle = alpha.get_value()
            opacity = gamma.get_value()
            curve = ParameterTrace(position_earth, position_source, length_major_axis, angle, GM = 20)
            trace.set_style(stroke_color = angle_color(2*angle), stroke_opacity = opacity).set_points(curve.get_all_points())
        def focus_updater(point: Dot):
            angle = alpha.get_value()
            opacity = gamma.get_value()
            curve = ParameterTrace(position_earth, position_source, length_major_axis, angle, GM = 20)
            point.set_opacity(opacity).set_points(curve.get_focus().get_all_points())
        def to_focus_updater(line: Line):
            angle = alpha.get_value()
            opacity = gamma.get_value()
            curve = ParameterTrace(position_earth, position_source, length_major_axis, angle, GM = 20)
            line.set_opacity(opacity).put_start_and_end_on(curve.get_focus().get_center(), position_source)
        def major_axis_updater(line: Line):
            angle = alpha.get_value()
            opacity = beta.get_value()
            curve = ParameterTrace(position_earth, position_source, length_major_axis, angle, GM = 20)
            line.set_opacity(opacity).set_points(curve.get_major_axis().get_all_points())
            
        self.waiting(0, 26) #于是......
        self.add(line_to_earth, line_to_focus, major_axis).bring_to_front(focus_example, earth, source)
        self.play(ShowCreation(line_to_earth), ShowCreation(line_to_focus))
        trace_example.add_updater(trace_updater)
        focus_example.add_updater(focus_updater)
        line_to_focus.add_updater(to_focus_updater)
        major_axis.add_updater(major_axis_updater)
        self.play(alpha.animate.set_value(PI*2/3), rate_func = rush_into)
        self.play(alpha.animate.set_value(PI), rate_func = linear)
        self.play(alpha.animate.set_value(PI*4/3), rate_func = linear)
        self.play(alpha.animate.set_value(PI*5/3), beta.animate.set_value(1.0), rate_func = linear)
        self.play(alpha.animate.set_value(PI*2), rate_func = linear)
        self.play(alpha.animate.set_value(PI*7/3), rate_func = linear)
        self.play(FadeOut(background), FadeOut(line_to_earth), alpha.animate.set_value(PI*5/2), beta.animate.set_value(0.0), gamma.animate.set_value(0.0), FadeOut(earth), FadeOut(source), rate_func = rush_from) 
        self.remove(trace_example, focus_example, line_to_focus, major_axis)

        position_earth = np.array([3.5, -1.7, 0])
        position_moon = np.array([3.5, 2.3, 0])
        length_major_axis = 5
        ellipse_ellipse = ParameterTrace(position_earth, position_moon, length_major_axis, PI/2, stroke_color = WHITE, GM = 18.5)
        trace_ellipse = ParametricCurve(ellipse_ellipse.parameter_function, [0, TAU, TAU/100])
        earth_ellipse = ImageMobject("earth.png", height = 0.5).shift(position_earth)
        moon_ellipse = ImageMobject("moon.png", height = 0.2).shift(position_moon)
        orbit_ellipse = DifferentialOrbiting(ellipse_ellipse, moon_ellipse, stop = False)

        alpha = ValueTracker(0.0)
        def stroke_updater_a(mob: VMobject):
            mob.set_style(stroke_opacity = alpha.get_value())
        def opacity_updater_a(mob: Mobject):
            mob.set_opacity(alpha.get_value())
        earth_ellipse.add_updater(opacity_updater_a)
        moon_ellipse.add_updater(opacity_updater_a)
        trace_ellipse.add_updater(stroke_updater_a)

        self.add(earth_ellipse, trace_ellipse, orbit_ellipse)
        self.play(alpha.animate.set_value(1.0), ReplacementTransform(notice8, notice9))
        self.waiting(0, 21) #类似于重力势能

        mtex_1 = MTex(r"E_p=-\frac{GMm}{r}", color = YELLOW).scale(0.8).next_to(0.8*UP + 5.5*LEFT)
        mtex_2 = MTex(r"E=E_k+E_p=\frac{1}{2}mv^2-\frac{GMm}{r}", color = YELLOW).scale(0.8).next_to(0.8*DOWN + 5.5*LEFT)
        line_above = Line(2.5*UP + 0.5*LEFT, 2.5*UP + -0.5*RIGHT)
        self.play(Write(mtex_1))
        self.waiting(1, 24) # 天体运动可以定义引力势能
        self.play(Write(mtex_2))
        self.waiting(0, 1) #一样有机械能守恒定律
        self.waiting(0, 19) #（空闲）

        self.play(FadeOut(mtex_1, 4.1*UP), mtex_2.animate.shift(4.1*UP), ReplacementTransform(notice9, notice10))
        self.play(line_above.animate.put_start_and_end_on(2.5*UP + 6*LEFT, 2.5*UP + 5*RIGHT))
        self.waiting(0, 12) #我们的实验似乎告诉我们
        text_1 = r"E_1 = E_2\quad"
        text_2 = r"\Rightarrow"
        text_3 = r"\quad a_1 = a_2"
        mtex_3 = MTex(text_1 + text_2 + text_3, isolate = [text_1, text_2, text_3], tex_to_color_map = {(r"E_1", r"a_1"): GREEN, (r"E_2", r"a_2"): RED}).scale(0.8).next_to(5.5*LEFT)
        mtex_3_1 = mtex_3.get_part_by_tex(text_1)
        mtex_3_2 = mtex_3.get_part_by_tex(text_2)
        mtex_3_3 = mtex_3.get_part_by_tex(text_3)
        mtex_4 = mtex_3.copy().shift(2.7*UP)
        mtex_4_1 = mtex_4.get_part_by_tex(text_1)
        mtex_4_2 = mtex_4.get_part_by_tex(text_2)
        mtex_4_3 = mtex_4.get_part_by_tex(text_3)
        shade = Rectangle(width = 5, height = 2.7, stroke_width = 0, fill_color = "#333333", fill_opacity = 1).shift(np.array([-3, 1.65, 0]))
        self.play(Write(mtex_3_1))
        self.waiting(0, 28) #如果机械能相同
        self.play(FadeIn(mtex_3_2, 0.5*RIGHT), FadeIn(mtex_3_3, 0.5*RIGHT))
        self.waiting(1, 10) #那么长轴相同
        self.waiting(2, 0) #这个结论该怎么证呢
        self.waiting(0, 28) #（空闲）

        self.bring_to_back(mtex_3, mtex_4, shade)
        self.play(mtex_3.animate.shift(0.6*UP), mtex_4.animate.shift(0.6*UP), mtex_2.animate.shift(5*RIGHT), ReplacementTransform(notice10, notice11))
        self.remove(mtex_3, shade)
        mtex_5 = MTex(r"u=\frac{1}{r}=\frac{GM}{h^2}+A\cos\theta=\frac{GM}{h^2}(1-e\cos\theta),\ e^2=1-\frac{b^2}{a^2}=1-\frac{h^2}{GMa}").scale(0.5).next_to(2*UP + 6.5*LEFT)
        mtex_6 = MTex(r"\vec{v}=\dot{r}\hat{r}+r\dot\theta\hat\theta=\left(-h\frac{du}{d\theta}\right)\hat{r}+\left(hu\right)\hat{\theta}").scale(0.5).next_to(1.3*UP + 6.5*LEFT)
        text_1 = r"\Rightarrow E_k &=\frac{1}{2}mv^2=\frac{m}{2}\left(\left(-h\frac{du}{d\theta}\right)^2+\left(hu\right)^2\right)\\"
        text_2 = r"&=\frac{m}{2}\left(\left(-\frac{GM}{h}e\sin\theta\right)^2+\left(\frac{GM}{h}(1-e\cos\theta)\right)^2\right)\\"
        text_3 = r"&=\frac{m}{2}\left(\frac{GM}{h}\right)^2\left(1-2e\cos\theta+e^2\right)\\"
        text_4 = r"&=\frac{m}{2}\left(\frac{GM}{h}\right)^2\left(2(1-e\cos\theta)-\frac{h^2}{GMa}\right)\\"
        text_5 = r"&=\frac{GMm}{r}-\frac{GMm}{2a}=:-E_p+E"
        mtex_7 = MTex(text_1 + text_2 + text_3 + text_4 + text_5, isolate = [r"-\frac{GMm}{2a}"]).scale(0.5).next_to(DOWN + 6.5*LEFT)
        indicate_1 = SurroundingRectangle(mtex_7.get_part_by_tex(r"-\frac{GMm}{2a}"))
        self.play(Write(mtex_5))
        self.play(Write(mtex_6))
        self.play(Write(mtex_7), run_time = 4)
        self.waiting(3+4+1-9, 18+4+20) #有些学习竞赛的同学可能已经准备开始计算了 确实 如果熟练掌握了天体运动的相关公式 借助一些微分运算
        self.play(ShowCreation(indicate_1))
        self.waiting(0, 26) #确实可以证明这个结论
        self.waiting(0, 19) #（空闲）
        
        self.waiting(2, 6) #但这里是一个数学频道
        group_text = VGroup(mtex_5, mtex_6, mtex_7, indicate_1)
        self.play(SwallowIn(group_text))
        self.waiting(1+2-2, 28+8) #只要有好的几何结构 那么能少算就尽量少算
        self.waiting(0, 23) #（空闲）

        cross_1 = Line(UL, DR, color = RED)
        cross_2 = Line(UR, DL, color = RED)
        cross = VGroup(cross_1, cross_2).scale(0.5).shift(mtex_4_2.get_center())
        self.play(ReplacementTransform(notice11, notice12))
        self.waiting(1, 22) #少算的方法是反过来思考
        self.waiting(1, 9) #也就是说
        self.play(mtex_4_1.animate.scale(1.25), ShowCreation(cross), mtex_4_3.animate.scale(0.8))
        self.waiting(1, 12) #不根据机械能来算长轴
        self.play(mtex_4_1.animate.scale(0.8), FadeOut(cross), Rotate(mtex_4_2, PI), mtex_4_3.animate.scale(1.25))
        self.waiting(1, 10) #而是根据轨道来算机械能
        self.waiting(0, 23) #（空闲）

        parabola = FunctionGraph(quadratic(-0.5, 0, 2), [-4, 4, 0.1]).shift(32/9*LEFT)
        position_focus = np.array([-32/9, 1.5, 0])
        position_point = np.array([-32/9-1.5, 0.875, 0])
        position_pedal = np.array([-32/9-1.5, 2.5, 0])
        position_apex = np.array([-32/9, 2.0, 0])
        position_middle = (position_focus + position_pedal)/2
        position_intersect = 2*position_middle - position_apex
        focus = Dot().shift(position_focus)
        point = Dot().shift(position_point)
        pedal = Dot().shift(position_pedal)
        apex = Dot().shift(position_apex)
        middle = Dot().shift(position_middle)
        intersect = Dot().shift(position_intersect)
        line_to_focus = Line(position_point, position_focus)
        line_to_pedal = Line(position_point, position_pedal)
        line_focus_pedal = Line(position_focus, position_pedal)
        line_tangent = Line(position_point, position_middle)
        line_tangent_apex = Line(position_apex, position_intersect)
        
        list_parabola = [parabola, line_to_focus, line_to_pedal, line_focus_pedal, line_tangent, line_tangent_apex, focus, point, pedal, apex, middle, intersect]
        self.play(*[ShowCreation(mob) for mob in list_parabola])
        self.waiting(0, 25) #在处理抛物线的时候
        self.play(ShowCreationThenFadeAround(apex), run_time = 2)
        self.waiting(0, 5) #我们取了它的顶点
        for mob in list_parabola:
            mob.reverse_points()
        self.play(*[Uncreate(mob) for mob in list_parabola])
        self.waiting(1, 3) #而椭圆比起抛物线

        position_above = np.array([3.5, 2.3, 0])
        position_below = np.array([3.5, -2.7, 0])
        apex_above = Dot(color = YELLOW).shift(position_above)
        apex_below = Dot(color = YELLOW).shift(position_below)
        arrow_above = Arrow(position_above, position_above + 0.4*LEFT, color = BLUE, buff = 0)
        text_above = MTex(r"\vec{v}_1", color = BLUE).scale(0.8).next_to(arrow_above.get_corner(LEFT), DOWN, buff = 0.1)
        velocity_above = VGroup(arrow_above, text_above)
        arrow_below = Arrow(position_below, position_below + 1.6*RIGHT, color = BLUE, buff = 0)
        text_below = MTex(r"\vec{v}_2", color = BLUE).scale(0.8).next_to(arrow_below.get_corner(RIGHT), UP, buff = 0.1)
        velocity_below = VGroup(arrow_below, text_below)
        line_to_above = Line(position_earth, position_above, color = BLUE)
        text_above = MTex(r"a+c", color = GREEN).scale(0.8).next_to(line_to_above, RIGHT, buff = 0.1)
        line_to_below = Line(position_earth, position_below, color = BLUE)
        text_below = MTex(r"a-c", color = GREEN).scale(0.8).next_to(line_to_below, LEFT, buff = 0.1)
        self.add(apex_above, apex_below).bring_to_front(orbit_ellipse)
        self.play(ShowCreation(apex_above), ShowCreation(apex_below))
        self.add(velocity_above, velocity_below).bring_to_front(apex_above, apex_below, orbit_ellipse).bring_to_back(line_to_above, line_to_below)
        self.play(FadeInFromPoint(velocity_above, position_above), FadeInFromPoint(velocity_below, position_below), ShowCreation(line_to_above), ShowCreation(line_to_below), FadeIn(text_above), FadeIn(text_below))
        self.waiting(0, 6) #好就好在它有两个顶点
        self.waiting(0, 12) #（空闲）

        text_energy = MTex(r"E=\frac{1}{2}mv_1^2-\frac{GMm}{a+c}\\E=\frac{1}{2}mv_2^2-\frac{GMm}{a-c}", tex_to_color_map = {r"E": YELLOW, (r"v_1", r"v_2"): BLUE, (r"a", r"c"): GREEN, (r"GM", r"m"): ORANGE}).scale(0.8).next_to(1.4*UP + 6*LEFT)
        surround_energy = SurroundingRectangle(text_energy)
        group_energy = VGroup(text_energy, surround_energy)
        text_angular_momentum = MTex(r"L=mv_1(a+c)\\\\L=mv_2(a-c)", tex_to_color_map = {r"L": PURPLE, (r"v_1", r"v_2"): BLUE, (r"a", r"c"): GREEN, r"m": ORANGE}, isolate = [r"(a+c)", r"(a-c)"]).scale(0.8).next_to(1.4*UP + 2*LEFT)
        surround_angular_momentum = surround_energy.copy().set_width(surround_energy.get_width()-0.8, stretch=True).shift(3.6*RIGHT)
        group_angular_momentum = VGroup(text_angular_momentum, surround_angular_momentum)
        indicate = SurroundingRectangle(text_angular_momentum.get_parts_by_tex([r"(a+c)", r"(a-c)"]), color = ORANGE)
        self.play(FadeIn(group_energy, 0.5*UP))
        self.waiting(0, 17) #根据机械能守恒......
        self.play(FadeIn(group_angular_momentum, 0.5*UP))
        self.waiting(0, 24) #......和角动量守恒
        
        text_function = MTex(r"\begin{cases}\dfrac{1}{2}v_1^2-\dfrac{GM}{a+c}=\dfrac{1}{2}v_2^2-\dfrac{GM}{a-c}\\v_1(a+c)=v_2(a-c)\end{cases}").scale(0.5).next_to(0.5*DOWN + 6*LEFT)
        text_solution = MTex(r"\Rightarrow\begin{cases}v_1=\sqrt{\dfrac{GM}{a}\cdot\dfrac{a-c}{a+c}}\\v_2=\sqrt{\dfrac{GM}{a}\cdot\dfrac{a+c}{a-c}}\end{cases}").scale(0.5).next_to(0.5*DOWN + 2*LEFT)
        text_mechanical = MTex(r"\Rightarrow E=\frac{1}{2}mv_1^2-\frac{GMm}{a+c}=\frac{GMm}{a+c}\left(\frac{a-c}{2a}-1\right)=-\frac{GMm}{2a}").scale(0.5).next_to(1.5*DOWN + 6*LEFT)
        self.play(ReplacementTransform(notice12, notice13), Write(text_function))
        self.waiting(1, 2) #我们可以列出两个顶点处速度的关系
        self.waiting(0, 29) #（空闲）

        self.waiting(2, 24) #这是一个关于速度的二元二次方程组......
        self.play(FadeIn(text_solution, 0.3*RIGHT))
        self.waiting(0, 11) #......不难解
        self.play(Write(text_mechanical))
        self.waiting(2, 1) #解出来以后再根据速度确定机械能 确实可以
        self.waiting(0, 18) #（空闲）

        self.waiting(2, 6) #但这里是一个数学频道
        self.waiting(3, 8) #既然我们要的是机械能 不是速度
        self.play(SwallowIn(VGroup(text_function, text_solution, text_mechanical)))
        self.waiting(1+0-2, 20+28) #那么就把速度消掉 （空闲）

        text_1 = r"(a+c)^2E-(a-c)^2E"
        text_2 = r"-(a+c)GMm+(a-c)GMm"
        text_3 = r"-2cGMm"
        mtex_7 = MTex(r"&" + text_1 + r"\\{=}&" + text_2 + r"\\{={}}&" + text_3, isolate = [r"(a+c)^2", r"-(a-c)^2", r"E", r"{=}", r"{={}}", text_2, text_3], tex_to_color_map = {r"E": YELLOW, (r"a", r"c"): GREEN, (r"GM", r"m"): ORANGE}).scale(0.8).next_to(0.6*DOWN+6*LEFT)
        mtex_7_1 = mtex_7.get_parts_by_tex([r"(a+c)^2", r"-(a-c)^2"])
        mtex_7_2 = mtex_7.get_parts_by_tex([r"E"])
        mtex_7_3 = mtex_7.get_parts_by_tex([r"{=}", text_2, r"{={}}", text_3])
        text_1 = r"-\frac{GMm}{2a}"
        mtex_8 = MTex(r"\Rightarrow E=\frac{-2cGMm}{4ac}=" + text_1, isolate = [text_1], tex_to_color_map = {r"E": YELLOW, (r"a", r"c"): GREEN, (r"GM", r"m"): ORANGE}).scale(0.8).next_to(2*DOWN + 6*LEFT)
        indicate_1 = SurroundingRectangle(mtex_8.get_part_by_tex(text_1))
        self.play(ReplacementTransform(notice13, notice14))
        self.waiting(0, 18) #设而不求的方法
        self.waiting(4, 2) #相信会做圆锥曲线大题的观众们 都已经很熟悉了
        self.waiting(0, 24) #（空闲）

        self.play(ShowCreationThenDestruction(indicate), run_time = 2)
        self.waiting(1, 14) #角动量守恒提供了两个速度的比例关系
        self.play(FadeIn(mtex_7_1, 0.5*DOWN), FadeIn(mtex_7_2, 0.5*UP))
        self.waiting(0, 18) #配到机械能上
        self.play(Write(mtex_7_3))
        self.waiting(0, 9) #我们就可以消去速度
        self.play(Write(mtex_8))
        self.waiting(0, 1) #再经过一些简单的化简
        self.play(ShowCreation(indicate_1))
        self.waiting(1, 16) #我们就能得到机械能的表达式
        self.waiting(2, 4) #它确实只与长轴有关

        fading_list = [mtex_2, mtex_4, line_above, group_energy, group_angular_momentum, indicate_1, mtex_7, mtex_8, apex_above, apex_below, velocity_above, velocity_below, line_to_above, line_to_below, text_above, text_below]
        self.play(alpha.animate.set_value(0.0), *[FadeOut(mob) for mob in fading_list]) #到此共112秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_4(Scene):

    def construct(self):
        notice14 = Notice("优美证法", "请　欣赏")
        notice15 = Notice("照猫画虎", "请　模仿")
        notice16 = Notice("希望之花", "连接着羁绊")
        notice17 = Notice("最后一步", "请　专注")
        notice18 = Notice("证明完毕", "请　鼓掌")
        notice19 = Notice("美妙性质", "请　欣赏")
        self.add(notice14)

        def ellipse_envelope(t: float):
            return np.array([2*np.sqrt(3)*np.cos(t), 4*np.sin(t), 0])
        position_earth = 2*DOWN
        position_source = 2*UP
        length_major_axis = 6
        focus_radius = length_major_axis - get_norm(position_earth - position_source)
        angle_example = -PI/3
        earth = ImageMobject("earth.png", height = 0.5).shift(position_earth)
        source = Dot(color = BLUE).shift(position_source)
        envelope = ParametricCurve(ellipse_envelope, [PI/2, TAU+PI/2, TAU/100], color = BLUE, fill_opacity = 0.1)
        ellipses = VGroup()
        number = 48
        for i in range (number):
            angle = i*TAU/number + PI/number
            color = angle_color(2*angle-PI)
            ellipse_i = ParameterTrace(position_earth, position_source, length_major_axis, angle, stroke_color = color, stroke_width = 2, stroke_opacity = 0.3, GM = 20)
            ellipses.add(ellipse_i)
        trace_example = ParameterTrace(position_earth, position_source, length_major_axis, angle_example, stroke_color = angle_color(2*angle_example-PI), GM = 20)
        focus_example = trace_example.get_focus().set_color(YELLOW)
        focus_trace = Circle(radius = focus_radius, opacity = 0.5, stroke_width = 2, color = WHITE).shift(position_source).rotate(-PI/6)
        self.play(FadeIn(ellipses), ShowCreation(envelope), FadeIn(earth), FadeIn(source), ReplacementTransform(notice14, notice15))
        self.add(trace_example, focus_example).bring_to_front(earth, source)
        self.play(ShowCreation(trace_example), ShowCreation(focus_example))
        self.add(focus_trace).bring_to_front(trace_example, focus_example, earth, source)
        self.play(ShowCreation(focus_trace))
        self.waiting(0, 3) #我们成功说明了所有的焦点组成一个圆
        self.waiting(0, 13) #（空闲）

        function_example = trace_example.parameter_function
        axis_angle_example = trace_example.axis_angle
        start_angle = axis_angle_example + PI
        position_focus_example = focus_example.get_center()
        target = PI+2*angle_example
        point_example = Dot(color = BLUE).shift(position_earth + position_focus_example - function_example(target))
        alpha = ValueTracker(TAU + 2*angle_example)
        def point_updater(point: Dot):
            t = alpha.get_value()
            point.move_to(position_earth + position_focus_example - function_example(t))
            if abs(t - target) < 0.2:
                point.set_color(YELLOW)
            else:
                point.set_color(BLUE)
        point_example.add_updater(point_updater)
        
        self.waiting(1, 10) #按照经验
        self.add(point_example)
        self.play(alpha.animate.set_value(start_angle))
        self.waiting(1, 26) #接下来就是说明轨迹上的任何一点
        self.play(alpha.animate.set_value(1.5*target - 0.5*start_angle))
        self.waiting(0, 23) #要不然在椭圆内......
        self.play(alpha.animate.set_value(target))
        point_example.clear_updaters()
        self.waiting(0+0-1, 19+23)
        fading_list = [ellipses, envelope, focus_trace, trace_example, focus_example, earth, source, point_example]
        self.play(*[FadeOut(mob) for mob in fading_list]) #......要不然在椭圆上了 （空闲）

        ellipse_example = ParametricCurve(lambda t: np.array([4*np.cos(t), 2*np.sqrt(2)*np.sin(t), 0]), [0, TAU, TAU/100], color = BLUE)
        position_l = 2*np.sqrt(2)*LEFT
        position_r = 2*np.sqrt(2)*RIGHT
        focus_left = Dot().shift(position_l)
        focus_right = Dot().shift(position_r)
        label_left = MTex(r"F_1").scale(0.8).next_to(focus_left, DOWN, buff = 0.13)
        label_right = MTex(r"F_2").scale(0.8).next_to(focus_right, DOWN, buff = 0.13)
        self.play(ShowCreation(ellipse_example), ShowCreation(focus_left), ShowCreation(focus_right), Write(label_left), Write(label_right))
        self.play(ellipse_example.animate.set_style(fill_opacity = 0.2))
        self.waiting(0, 24) #椭圆的内部也有比较方便的刻画

        position_b = np.array([4*np.cos(PI/3), 2*np.sqrt(2)*np.sin(PI/3), 0])
        position_a = 0.75*position_b + 0.25*position_l
        point_a = Dot().shift(position_a)
        label_a = MTex(r"A").scale(0.8).next_to(point_a, UL, buff = 0.1)
        point_b = Dot().shift(position_b)
        label_b = MTex(r"B").scale(0.8).next_to(point_b, UR, buff = 0.1)
        line_a_l = Line(position_a, position_l)
        line_a_r = Line(position_a, position_r)
        line_a_b = Line(position_a, position_b)
        line_b_r = Line(position_b, position_r)
        text_1 = r"AF_1+AF_2<"
        text_2 = r"AF_1+AB+BF_2=BF_1+BF_2="
        text_3 = r"2a"
        mtex_1 = MTex(text_1 + text_3, isolate = [text_1, text_3]).scale(0.8).shift(3.4*UP)
        mtex_1_1 = mtex_1.get_part_by_tex(text_1)
        mtex_1_3 = mtex_1.get_part_by_tex(text_3)
        mtex_2 = MTex(text_1 + text_2 + text_3, isolate = [text_1, text_2, text_3]).scale(0.8).shift(3.4*UP)
        mtex_2_1 = mtex_2.get_part_by_tex(text_1)
        mtex_2_2 = mtex_2.get_part_by_tex(text_2)
        mtex_2_3 = mtex_2.get_part_by_tex(text_3)
        self.play(ShowCreation(point_a), ShowCreation(label_a))
        self.waiting(0, 18) #一个椭圆内部的点
        self.play(ShowCreation(line_a_l), ShowCreation(line_a_r))
        self.waiting(0, 28) #到两个焦点的距离和
        self.play(Write(mtex_1))
        self.waiting(0, 19) #小于长轴的长度
        self.waiting(0, 17) #（空闲）

        self.play(ShowCreation(line_a_b))
        self.play(ShowCreation(point_b), ShowCreation(label_b), ReplacementTransform(mtex_1_1, mtex_2_1), ReplacementTransform(mtex_1_3, mtex_2_3))
        self.play(ShowCreation(line_b_r), Write(mtex_2_2))
        self.waiting(2+2-4, 17+12) #这比抛物线的情况还要好证 只需利用两点之间线段最短

        self.waiting(1+0-1, 15+25)
        fading_group = VGroup(ellipse_example, focus_left, focus_right, label_left, label_right, point_a, label_a, point_b, label_b, line_a_l, line_a_r, line_a_b, line_b_r, mtex_2)
        self.play(FadeOut(fading_group)) #就可以得到结论 （空闲）

        self.play(FadeIn(ellipses), ShowCreation(envelope), FadeIn(earth), FadeIn(source), ReplacementTransform(notice15, notice16))
        self.add(trace_example, focus_example).bring_to_front(earth, source)
        self.play(ShowCreation(trace_example), ShowCreation(focus_example))
        self.add(focus_trace).bring_to_front(trace_example, focus_example, earth, source)
        self.play(ShowCreation(focus_trace))
        self.waiting(0, 8) #路已经打开了 接着只要前进就好
        self.waiting(0, 25) #（空闲）

        alpha.set_value(TAU + 2*angle_example)
        self.add(point_example)
        point_example.add_updater(point_updater)
        start_angle = 0.6*start_angle + 0.4*target
        self.play(alpha.animate.set_value(start_angle), ReplacementTransform(notice16, notice17))
        self.waiting(1, 23) #对于任意一条轨迹上的任意一点

        position_start = position_earth + position_focus_example - function_example(start_angle)
        line_to_focus = Line(position_start, position_focus_example, color = GREEN)
        line_to_earth = Line(position_start, position_earth, color = GREEN)
        line_source_focus = Line(position_source, position_focus_example, color = RED)
        line_to_source = Line(position_start, position_source, color = YELLOW)
        indicate = SurroundingRectangle(focus_example)
        self.add(line_to_focus, line_to_earth).bring_to_front(point_example, focus_example, earth, source)
        self.play(ShowCreation(line_to_focus), ShowCreation(line_to_earth))
        self.waiting(1, 18) #作出它和两个焦点的连线
        self.play(ShowCreationThenFadeAround(earth), run_time = 2)
        self.waiting(0, 15) #其中一个焦点是中心天体
        self.add(line_source_focus).bring_to_front(trace_example, source, focus_example, point_example)
        self.play(ShowCreation(indicate), ShowCreation(line_source_focus))
        self.play(FadeOut(indicate), Rotate(line_source_focus, TAU, about_point = position_source))
        self.waiting(0, 3) #另外一个焦点在一个定圆上
        self.waiting(0, 20) #（空闲）

        self.add(line_to_source).bring_to_front(source, focus_example, point_example, earth)
        self.play(ShowCreation(line_to_source))
        self.play(WiggleOutThenIn(line_to_source), WiggleOutThenIn(line_to_earth))
        self.waiting(1, 10) #于是 这一点到起始点和中心天体的距离之和
        self.play(WiggleOutThenIn(line_source_focus), WiggleOutThenIn(line_to_focus), WiggleOutThenIn(line_to_earth))
        self.waiting(0, 10) #不大于这三段线段的长度和
        self.waiting(0, 21) #（空闲）

        def to_focus_updater(line: Line):
            t = alpha.get_value()
            position_p = position_earth + position_focus_example - function_example(t)
            line.put_start_and_end_on(position_p, position_focus_example)
        line_to_focus.add_updater(to_focus_updater)
        def to_earth_updater(line: Line):
            t = alpha.get_value()
            position_p = position_earth + position_focus_example - function_example(t)
            line.put_start_and_end_on(position_p, position_earth)
        line_to_earth.add_updater(to_earth_updater)
        def to_source_updater(line: Line):
            t = alpha.get_value()
            position_p = position_earth + position_focus_example - function_example(t)
            line.put_start_and_end_on(position_p, position_source)
        line_to_source.add_updater(to_source_updater)
        self.play(alpha.animate.set_value(target))
        point_example.clear_updaters()
        line_to_focus.clear_updaters()
        line_to_earth.clear_updaters()
        line_to_source.clear_updaters()
        self.remove(line_to_focus, line_source_focus)
        self.waiting(1+3+0-5, 26+3+25) #这一点在包络线上......
        
        alpha = ValueTracker(-PI/3)
        def trace_updater(trace: ParameterTrace):
            angle = alpha.get_value()
            curve = ParameterTrace(position_earth, position_source, length_major_axis, angle, GM = 20)
            trace.set_style(stroke_color = angle_color(2*angle-PI)).set_points(curve.get_all_points())
        trace_example.add_updater(trace_updater)
        def focus_updater(point: Dot):
            angle = alpha.get_value()
            curve = ParameterTrace(position_earth, position_source, length_major_axis, angle, GM = 20)
            point.set_points(curve.get_focus().get_all_points())
        focus_example.add_updater(focus_updater)
        def point_updater(point: Dot):
            angle = 2 * alpha.get_value()
            radius = 6/(2+np.cos(angle))
            point.move_to(position_source + radius * unit(angle + PI/2))
        point_example.add_updater(point_updater)
        def to_source_updater(line: Line):
            angle = 2 * alpha.get_value()
            position_p = position_source + 6/(2+np.cos(angle)) * unit(angle + PI/2)
            line.put_start_and_end_on(position_p, position_source)
        line_to_source.add_updater(to_source_updater)
        def to_earth_updater(line: Line):
            angle = 2 * alpha.get_value()
            position_p = position_source + 6/(2+np.cos(angle)) * unit(angle + PI/2)
            line.put_start_and_end_on(position_p, position_earth)
        line_to_earth.add_updater(to_earth_updater)
        self.play(alpha.animate.set_value(-PI/2), rate_func = rush_into)
        self.play(alpha.animate.set_value(-PI*5/6), rate_func = linear)
        self.play(alpha.animate.set_value(-PI*7/6), rate_func = linear)
        self.play(alpha.animate.set_value(-PI*4/3), rate_func = rush_from) #......当且仅当它与焦点 起始点共线 （空闲）
        trace_example.clear_updaters()
        focus_example.clear_updaters()
        point_example.clear_updaters()
        line_to_source.clear_updaters()
        line_to_earth.clear_updaters()

        self.play(ReplacementTransform(notice17, notice18))
        self.waiting(1, 10) #就这样 我们完成了证明
        self.waiting(0, 6)
        fading_list = [ellipses, envelope, focus_trace, trace_example, focus_example, point_example, line_to_earth, line_to_source]
        self.play(*[FadeOut(mob) for mob in fading_list]) #（空闲）
        
        alpha = ValueTracker(1.0)
        def opacity_updater(mob: VMobject):
            opacity = alpha.get_value()
            mob.set_opacity(opacity)
        ellipses = VGroup()
        starts = VGroup()
        orbits = VGroup()
        trace_paths = VGroup()
        number = 24
        for i in range (number):
            angle = i*TAU/number + PI/number
            color = angle_color(2*angle)
            ellipse_i = ParameterTrace(2*DOWN, 2*UP, 6, angle, stroke_color = color, GM = 20)
            ellipses.add(ellipse_i)
            start = Dot(color = RED).move_to(ellipse_i.point_from_proportion(0))
            
            orbit = DifferentialOrbiting(ellipse_i, start, stop = False).add_updater(opacity_updater)
            starts.add(start)
            orbits.add(orbit)
            
            traces_path_i = TracedPath(start.get_center).set_color(color)
            trace_paths.add(traces_path_i)

        self.play(ReplacementTransform(notice18, notice19))
        self.add(trace_paths, orbits).bring_to_front(earth, source)
        self.waiting(2, 25) #其实椭圆的情况比起抛物线来说 还要更有趣一些
        self.waiting(0, 19) #（空闲）
        self.waiting(1, 23) #可能有观众注意到了
        self.waiting(2, 0) #在这一节一开始的实验中
        for mob in trace_paths:
            mob.suspend_updating()
        for mob in orbits:
            mob.suspend_updating()
        indicate = SurroundingRectangle(orbits)
        self.play(ShowCreation(indicate), trace_paths.animate.set_style(stroke_opacity = 0.5))
        self.waiting(1, 6) #这些物体同时回到了起始点
        self.waiting(0, 15) #（空闲）
        self.play(FadeOut(indicate), trace_paths.animate.set_style(stroke_opacity = 1.0))

        for mob in trace_paths:
            mob.resume_updating()
        for mob in orbits:
            mob.resume_updating()
        self.waiting(1, 0) #这其实不是巧合
        for mob in trace_paths:
            mob.clear_updaters()
        mtex_1 = MTex(r"E=-\frac{GMm}{2a}").scale(0.8).next_to(2*UP + 7*LEFT)
        mtex_2 = MTex(r"T=\sqrt{\frac{4\pi^2a^3}{GM}}").scale(0.8).next_to(7*LEFT)
        mtex_3 = MTex(r"T=\pi GM\sqrt{\frac{-m^3}{2E^3}}").scale(0.8).next_to(2*DOWN + 7*LEFT)
        self.play(Write(mtex_1), run_time = 1)
        self.waiting(2, 23) #我们知道 机械能只和主轴长度有关
        self.waiting(2, 2) #而根据开普勒第三定律
        self.play(Write(mtex_2), run_time = 1)
        self.waiting(1, 23) #周期也只和主轴长度有关
        self.play(Write(mtex_3), run_time = 1)
        self.waiting(1, 21) #所以 对于同一个天体来说
        self.waiting(2, 7)
        self.play(FadeOut(VGroup(mtex_1, mtex_2, mtex_3)), FadeOut(trace_paths), alpha.animate.set_value(0.0)) #相同机械能的轨道 周期相同
        for mob in orbits:
            mob.clear_updaters()
        
        alpha.set_value(1.0)
        new_ellipses = VGroup()
        new_starts = VGroup()
        new_orbits = VGroup()
        trace_paths = VGroup()
        number = 180
        for i in range (number):
            angle = i*TAU/number + PI/number
            color = angle_color(2*angle)
            new_ellipse_i = ParameterTrace(2*DOWN, 2*UP, 6, angle, stroke_color = color)
            new_ellipses.add(new_ellipse_i)
            new_start = Dot(color = BLUE).move_to(new_ellipse_i.point_from_proportion(0))
            
            new_orbit = DifferentialOrbiting(new_ellipse_i, new_start).add_updater(opacity_updater)
            new_starts.add(new_start)
            new_orbits.add(new_orbit)
            
            traces_path_i = TracingTail(new_start.get_center, time_traced = 5.0).set_color(color)
            trace_paths.add(traces_path_i)

        self.add(trace_paths, new_orbits).bring_to_front(source, earth)
        self.waiting(3, 13) #如果我们同时向四面八方抛出物体
        self.waiting(3, 16) #那么它们会在分别绕中心天体一周以后
        self.waiting(2, 6) #在同一时间回到原位
        self.waiting(5, 6) 
        alpha.set_value(0.0)
        self.play(FadeOut(source), FadeOut(earth), FadeOut(notice19))
        self.waiting(3, 0) #到此共105秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Summary(Scene):

    def construct(self):
        notice1 = Notice("良心视频", "请　三连")
        notice2 = Notice("下期预告", "敬请期待")
        notice3 = Notice("良心up主", "请　关注")

        self.play(Write(notice1))
        self.waiting(1, 3) #非常感谢大家能看到这里
        self.waiting(0, 13) #（空闲）

        gravity = 1/9
        radius = 1/(4*gravity)
        start_radius = ValueTracker(0.0)
        def projectile_para(angle: float):
            return lambda t: t*unit(angle) + gravity*t*t*DOWN
        def trace_mover(angle: float):
            def util(trace: ParametricCurve):
                radius = start_radius.get_value()
                trace.set_points(trace.save.get_all_points())
                trace.shift(radius * unit(angle + PI/2))
            return util


        self.waiting(2, 3) #其实定速抛体问题
        self.waiting(2 ,10) #还有很多相关的变体
        
        start_point = Dot(color = BLUE)
        circle_radius = 2
        start_circle = Circle(color = BLUE, stroke_width = 10, radius = circle_radius)
        envelope = FunctionGraph(quadratic(-gravity, 0, radius + gravity*circle_radius**2), [-8, 8, 0.05], stroke_color = BLUE)
        focus = Dot(color = YELLOW).shift(gravity*circle_radius**2*UP)
        traces = []
        number = 48
        for i in range(number):
            if i % 2:
                angle_i = PI * i / number - PI/2
            else:
                angle_i = - PI * (i+1) / number - PI/2
            color = angle_color(angle_i)
            trace_i = ParametricCurve(projectile_para(angle_i), [0, 12, 0.05], stroke_width = 2, stroke_color = color)
            trace_i.save = trace_i.copy()
            trace_i.add_updater(trace_mover(angle_i))
            traces.append(trace_i)
        self.play(ShowCreation(start_point))
        self.waiting(0, 3) #比如说
        self.bring_to_back(*traces)
        self.play(*[ShowCreation(trace) for trace in traces])
        self.waiting(0, 28) #在地面上抛出时
        self.bring_to_back(start_circle)
        self.play(start_radius.animate.set_value(circle_radius), TransformFromCopy(start_point, start_circle))
        for mob in traces:
            mob.clear_updaters()
        self.waiting(1, 16) #如果是沿着圆的切线抛出
        self.play(ShowCreation(envelope), ShowCreation(focus), start_point.animate.fade())
        self.waiting(1, 17) #那么包络线仍然会形成抛物线
        self.waiting(0, 11) #（空闲）
        self.play(*[FadeOut(mob) for mob in traces], FadeOut(envelope), FadeOut(focus), FadeOut(start_circle), start_point.animate.set_opacity(1.0))
        self.waiting(0, 7) # 再比如

        dot_positive = Dot(radius = 0.5, fill_color = YELLOW)
        text_positive = MTex(r"+", color = RED).scale(1.5)
        self.play(Transform(start_point, dot_positive), FadeIn(text_positive))
        self.waiting(1, 15) #如果把引力改变为斥力

        radius = 0.5
        def trace_hyper(distance: float):
            a = radius
            b = distance
            c = np.sqrt(a ** 2 + b ** 2)
            angle = np.arcsin(b/c)
            return lambda theta: b**2/(a-c*np.cos(theta + angle)) * unit(theta)
        traces = []
        number = 48
        for i in range(number):
            distance = -4 + 8 * (i+1/2) / number
            a = radius
            b = distance
            c = np.sqrt(a ** 2 + b ** 2)
            angle = np.arcsin(b/c)
            color = angle_color(2*angle + PI)
            if angle >= 0:
                t_range = [-2*angle + TAU/1000, -TAU/1000, TAU/1000]
                trace_i = ParametricCurve(trace_hyper(distance), t_range, stroke_width = 2, stroke_color = color).reverse_points()
            else:
                t_range = [-2*angle - TAU/1000, +TAU/1000, TAU/1000]
                trace_i = ParametricCurve(trace_hyper(distance), t_range, stroke_width = 2, stroke_color = color)
            traces.append(trace_i)
        envelope = ParametricCurve(lambda theta: radius*4/(1-np.cos(theta))*unit(theta), [TAU/100, TAU - TAU/100, TAU/100], stroke_color = BLUE)
        
        self.play(*[ShowCreation(mob) for mob in traces])
        self.waiting(1, 18) #那么从无穷远处射来的物体
        self.play(ShowCreation(envelope))
        self.waiting(1, 22) #会覆盖一个抛物线外部的全部区域
        self.waiting(0, 17) #（空闲）

        self.waiting(1, 26) #如果有感兴趣的观众
        self.waiting(2+0-1, 25+25) 
        self.play(*[FadeOut(mob) for mob in traces], FadeOut(envelope), FadeOut(start_point), FadeOut(text_positive)) #欢迎在评论区给出这些结论的证明 （空闲）

        cover = ImageMobject("cover.png", height = 3)
        self.play(FadeIn(cover, UP))
        self.waiting(1, 27) #这期视频涉及的动画效果非常复杂
        self.waiting(2, 9) #着实花费了我不少心血
        self.remove(cover)
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
        self.play(FadeInFromPoint(like1, 3*LEFT), FadeInFromPoint(coin1, np.array([0,0,0])), FadeInFromPoint(star1, 3*RIGHT))
        self.play(ApplyMethod(sanlian1.set_color, "#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian1]) #希望大家多多三连
        self.waiting(0, 0) 
        self.waiting(0, 28) #（空闲）

        self.remove(sanlian1)
        
        mark_outer = Circle(radius = 3.6, color = WHITE)
        mark_inner = Circle(radius = 3.5, color = WHITE)
        number = 66
        marks = VGroup()
        for i in range (number):
            angle = i * TAU / number
            mark_i = Line(3.5*unit(angle), 3.6*unit(angle))
            marks.add(mark_i)
        marks.add(mark_outer, mark_inner)

        texts_letter = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'V', 'X', 'Y', 'Z'] #23个拉丁字母
        number_letters = 23

        outer_text = VGroup()
        outer_number = VGroup()
        for i in range (number_letters):
            angle = i * TAU / number_letters
            text_i = Text(texts_letter[i], font = 'Trajan Pro').scale(0.8).shift(3.1*UP).rotate(-angle, about_point = ORIGIN)
            number_i = Text("%d"%i, font = 'Trajan Pro').scale(0.8).shift(3.1*UP).rotate(-angle, about_point = ORIGIN).set_opacity(0)
            outer_text.add(text_i)
            outer_number.add(number_i)

        gear_outer = Circle(radius = 2.7, color = WHITE)
        gear_inner = Gear(major_radius = 2.6, minor_radius = 2.48, n_teeth = number_letters)
        outer_gear = VGroup(gear_outer, gear_inner)
        outer_layer = VGroup(marks, outer_text, outer_gear, outer_number)

        gear_outer = Gear(major_radius = 2.52, minor_radius = 2.4, n_teeth = number_letters, width_ratio = 1/2, fill_opacity = 1, fill_color = "#333333", stroke_color = YELLOW_E)
        gear_inner = Circle(radius = 2.3, color = YELLOW_E)
        inner_gear = VGroup(gear_outer, gear_inner)

        inner_text = VGroup()
        inner_number = VGroup()
        for i in range (number_letters):
            angle = i * TAU / number_letters
            text_i = Text(texts_letter[i], font = 'Trajan Pro', color = YELLOW_E).scale(0.7).shift(1.9*UP).rotate(-angle, about_point = ORIGIN)
            number_i = Text("%d"%i, font = 'Trajan Pro', opacity = 0, color = YELLOW_E).scale(0.6).shift(1.9*UP).rotate(-angle, about_point = ORIGIN).set_opacity(0)
            inner_text.add(text_i)
            inner_number.add(number_i)

        alpha = ValueTracker(1.0)
        def text_updater(mob: VMobject):
            opacity = alpha.get_value()
            mob.set_opacity(opacity)
        def number_updater(mob: VMobject):
            opacity = 1 - alpha.get_value()
            mob.set_opacity(opacity)
        def stroke_layer(mob: VMobject):
            opacity = alpha.get_value()

            mob.set_style(stroke_opacity = opacity)
        
        mark_outer = Circle(radius = 1.5, color = YELLOW_E)
        mark_inner = Circle(radius = 1.4, color = YELLOW_E)
        number = 66
        marks = VGroup()
        for i in range (number):
            angle = i * TAU / number
            mark_i = Line(1.5*unit(angle), 1.4*unit(angle), color = YELLOW_E)
            marks.add(mark_i)
        marks.add(mark_outer, mark_inner)
        inner_layer = VGroup(inner_gear, inner_text, marks, inner_number)

        self.play(FadeIn(outer_layer), FadeIn(inner_layer), ReplacementTransform(notice1, notice2), run_time = 0.8)
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6)
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6) #下期视频是关于密码学的话题......
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6)
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6)
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6)
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6) #我发现 现在关于密码学的科普......
        outer_text.add_updater(text_updater)
        inner_text.add_updater(text_updater)
        outer_number.add_updater(number_updater)
        inner_number.add_updater(number_updater)
        self.play(Rotate(inner_layer, -TAU/23), alpha.animate.set_value(0.0), run_time = 0.2)
        outer_text.clear_updaters()
        inner_text.clear_updaters()
        outer_number.clear_updaters()
        inner_number.clear_updaters()
        self.remove(outer_text, inner_text)
        self.waiting(0.6)
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6)
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6)
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6)
        self.play(Rotate(inner_layer, -TAU/23), run_time = 0.2)
        self.waiting(0.6) #基本都没有提及现代密码学的一次重要的观点转换......
        alpha.set_value(0.5)
        inner_layer.add_updater(stroke_layer)
        inner_number.add_updater(text_updater)
        self.play(Rotate(inner_layer, -TAU/23), alpha.animate.set_value(0.0), FadeOut(outer_layer), run_time = 0.2)
        self.remove(inner_layer)
        self.waiting(0.6) #（空闲）......

        beta = ValueTracker(0.0) #分组偏差
        gamma = ValueTracker(0.0) #个体偏差
        radius_a = ValueTracker(10.0) #半径
        radius_b = ValueTracker(10.0) #半径

        def a_updater(order: int):
            def util(mob: Knife, dt):
                mob.angle -= dt * PI / 6
                angle_b = beta.get_value()
                angle_c = gamma.get_value()
                r = radius_a.get_value()
                mob.restore().rotate(angle_c).shift(r*UP).rotate(mob.angle + angle_b, about_point = ORIGIN)
            return util
        
        def b_updater(order: int):
            def util(mob: Knife, dt):
                mob.angle -= dt * PI / 6
                angle_b = beta.get_value()
                angle_c = gamma.get_value()
                r = radius_b.get_value()
                mob.restore().rotate(-angle_c).shift(r*UP).rotate(mob.angle - angle_b, about_point = ORIGIN)
            return util

        number = 11
        knives_a = VGroup()
        knives_b = VGroup()
        for i in range (number):
            knife_a_i = Knife()
            knife_b_i = Knife()
            knife_a_i.angle = i * TAU / 11
            knife_b_i.angle = i * TAU / 11 + PI / 11
            knife_a_i.save_state().add_updater(a_updater(i))
            knife_b_i.save_state().add_updater(b_updater(i))
            knives_a.add(knife_a_i)
            knives_b.add(knife_b_i)

        text_Juluis = Text(r"IVLIVS", font = 'Trajan Pro').shift(0.6*UP)
        text_Caesar = Text(r"CAESAR", font = 'Trajan Pro')
        text_d_time = Text(r"440315", font = 'Trajan Pro').shift(0.6*DOWN)
        caesar = VGroup(text_Juluis, text_Caesar, text_d_time)
        caesar.save_state()

        delta = ValueTracker(1.0)
        epsilon = ValueTracker(0.0)

        def caesar_updater(caesar: VGroup):
            scale_factor = delta.get_value()
            opacity = epsilon.get_value()
            caesar.restore().scale(scale_factor).set_opacity(opacity)
        caesar.add_updater(caesar_updater)

        brutus = Dagger(stroke_width = 10, stroke_color = "#333333")
        brutus.save_state()
        upper_half = Square(side_length = 4).shift(2*UP)
        zeta = ValueTracker(5.0)
        def brutus_updater(brutus: Dagger):
            height = zeta.get_value()
            brutus.restore().shift(height * UP)
            outside = Intersection(brutus, upper_half)
            brutus.set_points(outside.get_all_points())
        brutus.add_updater(brutus_updater)

        self.add(knives_a, knives_b, caesar, brutus)
        beat = ApplyMethod(delta.set_value, 1.2)
        beat.update_config(rate_func = there_and_back)
        self.play(radius_a.animate.set_value(6.0), epsilon.animate.set_value(0.25), beat, run_time = 0.2)
        self.waiting(0.6)
        self.play(radius_a.animate.set_value(7.0), epsilon.animate.set_value(0.5), beat, radius_b.animate.set_value(5.0), run_time = 0.2)
        self.waiting(0.6)
        self.play(radius_a.animate.set_value(4.0), epsilon.animate.set_value(0.75), beat, radius_b.animate.set_value(6.0), run_time = 0.2)
        self.waiting(0.6)
        self.play(radius_a.animate.set_value(5.0), epsilon.animate.set_value(1.0), beat, radius_b.animate.set_value(3.0), run_time = 0.2)
        self.waiting(0.6)
        self.play(radius_a.animate.set_value(2.5), radius_b.animate.set_value(2.5), beat, run_time = 0.2)
        self.waiting(0.6)
        self.play(radius_a.animate.set_value(3.5), radius_b.animate.set_value(3.5), beta.animate.set_value(PI/22), gamma.animate.set_value(PI/6), beat, run_time = 0.2)
        self.waiting(0.6)
        self.play(beta.animate.set_value(-PI/22), gamma.animate.set_value(PI*5/6), beat, run_time = 0.2)
        self.waiting(0.6)
        self.play(radius_a.animate.set_value(2.5), radius_b.animate.set_value(2.5), beta.animate.set_value(0), gamma.animate.set_value(PI), beat, run_time = 0.2)
        self.waiting(0.6)
        self.play(radius_a.animate.set_value(3.5), radius_b.animate.set_value(3.5), beta.animate.set_value(PI/22), gamma.animate.set_value(PI*7/6), beat, run_time = 0.2)
        self.waiting(0.6)
        self.play(beta.animate.set_value(-PI/22), gamma.animate.set_value(PI*11/6), beat, run_time = 0.2)
        self.waiting(0.6)
        self.play(radius_a.animate.set_value(2.5), radius_b.animate.set_value(2.5), beta.animate.set_value(0), gamma.animate.set_value(TAU), beat, run_time = 0.2)
        self.waiting(0.6)
        caesar.clear_updaters()
        self.play(radius_a.animate.set_value(-2.5), radius_b.animate.set_value(-2.5), zeta.animate.set_value(2.0), caesar.animate.set_color(RED), run_time = 0.2)
        self.waiting(0.6)
        self.play(radius_a.animate.set_value(-10), radius_b.animate.set_value(-10), zeta.animate.set_value(0.0), caesar.animate.set_color(MAROON_E), run_time = 0.2)
        self.waiting(0.6)
        for mob in knives_a:
            mob.clear_updaters()
        for mob in knives_b:
            mob.clear_updaters()
        self.remove(knives_a, knives_b)
        brutus.clear_updaters()
        self.play(FadeOut(caesar), FadeOut(brutus), run_time = 0.2)

        self.waiting(2+3+3+0+4+4+2+1 - 21, 25+4+26+15+0+3+4+0) # 下期视频是关于密码学的话题 我发现 现在关于密码学的科普 基本都没有提及现代密码学的一次重要的观点转换 在下期视频 密码学这条穿越过两千多年 从罗马人的王后 到数学中的女王的精彩旅程 欢迎大家和我一起走入 （空闲）
        
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
        self.waiting(0, 6) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(1, 22) #而我 就像我的名字一样

        self.play(FadeOut(painting_others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star0.shift, DOWN))
        self.waiting(1, 16) #想要把天上的星星垂下来

        star_copy = star0.copy()
        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star0, apple))
        self.waiting(1, 10) #变成触手可及的果实

        snowflake = SnowFlake()
        snowflake_2 = snowflake.copy().set_color(RED).set_stroke(width = 1.5)
        snowflake_3 = snowflake.copy().set_color(BLUE).set_stroke(width = 2)
        anims = LaggedStart(SpreadOut(snowflake_2).update_config(rate_func = linear), SpreadOut(snowflake_3).update_config(rate_func = linear), SpreadOut(snowflake).update_config(rate_func = linear), rate_func = rush_into, run_time = 2)
        self.play(Transform(star0, star_copy), anims)
        self.remove(snowflake_2, snowflake_3)
        self.waiting(2+0-2, 5+23) #变成指引前路的火光 （空闲）
        
        self.remove(star0, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(2, 12) #我是乐正垂星 我们下期视频再见

        self.waiting(5,16)
        self.play(FadeOut(picture_photo), FadeOut(text_name), FadeOut(notice3))
        self.waiting(5)

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)
    
class Template(Scene):

    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)