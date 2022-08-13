from manimlib import *
import numpy as np

def angle_color(angle):

    # colors = ["#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    # colors = [RED, YELLOW, GREEN, TEAL, BLUE, PURPLE]
    # colors = [TEAL, BLUE, BLUE, TEAL, GREEN, GREEN]
    # colors = [TEAL, BLUE, PURPLE, RED, YELLOW, GREEN]

    number_colors = len(colors)
    ratio = number_colors*angle/TAU
    index = int(ratio)
    interpolate = ratio - index

    return interpolate_color(colors[index%number_colors], colors[(index+1)%number_colors], interpolate)


##############################################################

class Orbiting_Grant(VGroup):
    CONFIG = {
        "rate": 7.5,
    }

    def __init__(self, planet, star, ellipse, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.add(planet)
        self.planet = planet
        self.star = star
        self.ellipse = ellipse
        # Proportion of the way around the ellipse
        self.proportion = 0
        planet.move_to(ellipse.point_from_proportion(0))

        self.add_updater(lambda m, dt: m.update(dt))

    def update(self, dt):
        # time = self.internal_time

        planet = self.planet
        star = self.star
        ellipse = self.ellipse

        rate = self.rate
        radius_vector = planet.get_center() - star.get_center()
        rate *= 1.0 / get_norm(radius_vector)

        prop = self.proportion
        d_prop = 0.001
        ds = get_norm(op.add(
            ellipse.point_from_proportion((prop + d_prop) % 1),
            -ellipse.point_from_proportion(prop),
        ))
        
        delta_prop = (d_prop / ds) * rate * dt

        self.proportion = (self.proportion + delta_prop) % 1
        planet.move_to(
            ellipse.point_from_proportion(self.proportion)
        )

class Test1(Scene):
    def construct(self):

        ellipse = Ellipse(width=10, height = 6, color=WHITE, stroke_width=1)
        planet = Dot()
        sun = Dot().shift(4*LEFT)
        orbiting = Orbiting_Grant(planet, sun, ellipse)
        self.add(ellipse, planet, sun, orbiting)
        self.wait(10)

################################################################################

# class ProjectileTrace(Circle):
#     CONFIG = {
#         "GM": 10,
#         "n_components": 24
#     }

#     def __init__(self, planet: np.ndarray, source: np.ndarray, major_axis: float, angle: float, **kwargs):

#         distance = get_norm(source - planet) #r
#         direction = (source - planet) / distance
#         radius = major_axis - distance #2a-r
#         minor_axis = 2 * np.sin(angle) * np.sqrt(distance * radius) #2b
#         focal_length = np.sqrt(major_axis**2 - minor_axis**2) #2c
#         axis_angle = np.arcsin(radius / focal_length * np.sin(2*angle)) #polar angle
        
#         if axis_angle == 0:
#             parameter = np.arccos(2 * distance * np.cos(axis_angle) / major_axis -1)
#         else:
#             parameter = np.arcsin(2 * distance * np.sin(axis_angle) / minor_axis)
#         propotion = PI/2 - parameter

#         super().__init__(**kwargs)
#         self.rotate(propotion)
#         self.set_width(minor_axis, stretch=True)
#         self.set_height(major_axis, stretch=True)
#         self.move_to(planet + focal_length * direction / 2)
#         self.rotate(about_point = planet, angle = axis_angle)
        
#         self.planet = planet
#         self.source = source
#         self.major_axis = major_axis
#         latus_rectum = minor_axis**2 / (2*major_axis)
#         self.angular_momentum = np.sqrt(self.GM * latus_rectum)


def parameter_function(planet: np.ndarray, latus_rectum: float, eccentricity: float, axis_angle: float):

    def util(theta):
        radius = latus_rectum / (1 - eccentricity*np.cos(theta - axis_angle))
        return np.array([-radius * np.sin(theta), radius * np.cos(theta), 0]) + planet
    
    return util

class ParameterTrace(ParametricCurve):
    CONFIG = {
        "GM": 10,
        "n_components": 24
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
        self.axis_angle = np.arcsin(radius / focal_length * np.sin(2*angle)) # initial polar angle
        self.latus_rectum = minor_axis**2 / (2*major_axis) # p = b^2/a
        self.eccentricity = focal_length / major_axis # e = c/a
        
        # if axis_angle == 0:
        #     parameter = np.arccos(2 * distance * np.cos(axis_angle) / major_axis -1)
        # else:
        #     parameter = np.arcsin(2 * distance * np.sin(axis_angle) / minor_axis)
        # propotion = PI/2 - parameter

        # self.rotate(propotion)
        # self.set_width(minor_axis, stretch=True)
        # self.set_height(major_axis, stretch=True)
        # self.move_to(planet + focal_length * direction / 2)
        # self.rotate(about_point = planet, angle = axis_angle)
        
        # self.function = parameter_function(planet, latus_rectum, eccentricity, axis_angle)

        super().__init__(lambda theta: self.parameter_function(theta), np.array([0, TAU, TAU/200]), **kwargs)
        self.angular_momentum = np.sqrt(self.GM * self.latus_rectum)


    def get_radius(self, theta: float):
        if self.angle >= PI:
            return self.latus_rectum / (1 - self.eccentricity*np.cos(- theta - self.axis_angle))
        else:
            return self.latus_rectum / (1 - self.eccentricity*np.cos(theta - self.axis_angle))

    def parameter_function(self, theta):
        if self.angle >= PI:
            radius = self.get_radius(theta)
            return np.array([radius * np.sin(theta), radius * np.cos(theta), 0]) + self.planet
        else:
            radius = self.get_radius(theta)
            return np.array([-radius * np.sin(theta), radius * np.cos(theta), 0]) + self.planet

    


# class Orbiting(VGroup):
#     # 借鉴了在《费曼失传的演讲》一期视频中使用的方法
#     # Acknowledgement to the method in the video Feynman's lost lecture
    
#     def __init__(self, trace: ProjectileTrace, satellite: VMobject, **kwargs):

#         super().__init__(satellite, **kwargs)
#         self.satellite = satellite
#         self.trace = trace

#         # Proportion of the way around the ellipse
#         self.proportion = 0
#         satellite.move_to(trace.point_from_proportion(0))

#         self.add_updater(lambda m, dt: m.orbit_update(dt))

#     def orbit_update(self, dt):

#         satellite = self.satellite
#         trace = self.trace

#         radius_vector = satellite.get_center() - trace.planet
#         velocity = np.sqrt(2*trace.GM * (1.0/get_norm(radius_vector) - 1.0/trace.major_axis))

#         prop = self.proportion
#         d_prop = 0.001
#         ds = get_norm(trace.point_from_proportion((prop + d_prop) % 1) - trace.point_from_proportion(prop))
        
#         delta_prop = (velocity * dt / ds) * d_prop

#         self.proportion = (self.proportion + delta_prop) % 1
#         satellite.move_to(
#             trace.point_from_proportion(self.proportion)
#         )

class DifferentialOrbiting(VGroup):
    CONFIG = {
        "test": False,
    }
    # 在Orbiting类基础上修改
    
    def __init__(self, trace: ParameterTrace, satellite: VMobject, **kwargs):

        super().__init__(satellite, **kwargs)
        self.satellite = satellite
        self.trace = trace

        self.theta = 0
        # self.delay = delay
        satellite.move_to(self.trace.parameter_function(self.theta))

        # # Proportion of the way around the ellipse
        # self.proportion = 0
        # satellite.move_to(trace.point_from_proportion(0))

        self.add_updater(lambda m, dt: m.orbit_update(dt))

    def orbit_update(self, dt):

        satellite = self.satellite
        trace = self.trace

        # radius_vector = satellite.get_center() - trace.planet
        # velocity = np.sqrt(2*trace.GM * (1.0/get_norm(radius_vector) - 1.0/trace.major_axis))
        # if self.test:
        #     print(velocity)

        # def get_new_propotion(delta_t):
        #     prop = self.proportion
        #     d_prop = 0.001
        #     ds = get_norm(trace.point_from_proportion((prop + d_prop) % 1) - trace.point_from_proportion(prop))
            
        #     delta_prop = (velocity * delta_t / ds) * d_prop

        #     self.proportion = (self.proportion + delta_prop) % 1
        #     satellite.move_to(trace.point_from_proportion(self.proportion))

        # sum_of_prop = 0
        # while 1:
        #     radius_vector = satellite.get_center() - trace.planet
        #     velocity = np.sqrt(2*trace.GM * (1.0/get_norm(radius_vector) - 1.0/trace.major_axis))
        #     if self.test:
        #         print(velocity)

        #     prop = min(0.5/velocity, 1-sum_of_prop)
        #     get_new_propotion(dt*prop)
        #     sum_of_prop += prop
        #     if sum_of_prop >= 1:
        #         break

        # if self.delay > 0:
        #     self.delay -= dt
        # el
        if self.theta >= TAU:
            self.theta = TAU
        else:
            sum_of_prop = 0
            while 1:
                radius_vector = trace.get_radius(self.theta)
                angular_velocity = trace.angular_momentum/(radius_vector**2)
                # if self.test:
                #     print(radius_vector, trace.angular_momentum, angular_velocity)

                prop = min(0.5/angular_velocity, 1-sum_of_prop)
                self.theta = min(self.theta + (dt*prop)*angular_velocity, TAU)
                sum_of_prop += prop
                if sum_of_prop >= 1:
                    break
            satellite.move_to(trace.parameter_function(self.theta))


class Test2(Scene):
    def construct(self):

        center = Dot().shift(2*DOWN)
        source = Dot().shift(2*UP)

        # ellipses = VGroup()
        # probes = VGroup()
        # starts = VGroup()
        # orbits = VGroup()
        # for i in range (24):
        #     angle = i*TAU/24 + TAU/48
        #     ellipse_i = ProjectileTrace(2*DOWN, 2*UP, 6, angle, stroke_color = angle_color(2*angle))
        #     ellipses.add(ellipse_i)
        #     start = Dot(color = BLUE).move_to(ellipse_i.point_from_proportion(0))
        #     orbit = Orbiting(ellipse_i, start)
        #     starts.add(start)
        #     orbits.add(orbit)
        # self.add(center, source, ellipses)

        # self.add(starts, orbits)

        # self.wait(10)

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

            # if i == 0:
            #     new_orbit = DifferentialOrbiting(new_ellipse_i, new_start, test = True)
            # else:
            #     new_orbit = DifferentialOrbiting(new_ellipse_i, new_start)
            
            new_orbit = DifferentialOrbiting(new_ellipse_i, new_start)
            new_starts.add(new_start)
            new_orbits.add(new_orbit)
            
            traces_path_i = TracedPath(new_start.get_center).set_color(color)
            # traces_path_i = TracingTail(new_start.get_center, time_traced = 5.0).set_color(color)
            trace_paths.add(traces_path_i)

            # self.add(new_start, new_orbit, traces_path_i)
            # self.wait(0.1)
        
        # self.add(center, source, new_ellipses)

        # probes = VGroup()
        # for i in range (20):
        #     propotion = i/20
        #     probe = Dot(color = GREEN).move_to(new_ellipses[0].point_from_proportion(propotion))
        #     probes.add(probe)
        # self.add(probes)

        self.add(trace_paths, new_starts, new_orbits)

        self.wait(20)

###############################################################################

gravity = 1/9

def quadratic(a,b,c):
    return lambda x: a*x*x + b*x + c

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def projectile(angle):
    return lambda t: t*unit(angle) + gravity*t*t*DOWN

class Trailer(Scene):

    def construct(self):
        
        number_of_sectors = 5
        max_time = 1/(2*gravity*np.sin(PI/number_of_sectors))
        tangent = 1/(2*gravity*np.tan(PI/number_of_sectors))

        points = VGroup()
        traces = VGroup()
        parameter_traces = VGroup()
        density = 10
        number = 2*number_of_sectors*density
        for i in range(density,(number_of_sectors-1)*density):
            angle = TAU * i / number + PI / number
            color = angle_color(angle)

            tangent = 1/(2*gravity*np.tan(angle))
            parameter_trace_i = FunctionGraph(quadratic(-gravity/(np.cos(angle))**2, np.tan(angle), 0), [min(0, tangent), max(0, tangent), 0.05], color = color)
            parameter_traces.add(parameter_trace_i)

            target = max_time*unit(angle) + gravity*max_time*max_time*DOWN
            moving_point_i = Dot(color = color).shift(target)
            traces_path_i = ParametricCurve(projectile(angle), [0, max_time, 0.05], color = color, stroke_width = 2)
            points.add(moving_point_i)
            traces.add(traces_path_i)

        envelope = FunctionGraph(quadratic(-gravity, 0, 1/(4*gravity)), [-tangent, tangent, 0.1], color = [interpolate_color(GREEN, YELLOW, 0.5), YELLOW, ORANGE, interpolate_color(ORANGE, RED, 0.5)])
        self.add(envelope)
        self.add(traces, parameter_traces, points)
        
class Cover(Scene):

    def construct(self):

        max_time = 1/(2*gravity*np.sin(PI/5))
        tangent = 1/(2*gravity*np.tan(PI/5))

        points = VGroup()
        traces = VGroup()
        parameter_traces = VGroup()
        density = 10
        number = 10*density
        for i in range(density,4*density):
            angle = TAU * i / number + PI / number
            color = angle_color(angle)

            tangent = 1/(2*gravity*np.tan(angle))
            parameter_trace_i = FunctionGraph(quadratic(-gravity/(np.cos(angle))**2, np.tan(angle), 0), [min(0, tangent), max(0, tangent), 0.05], color = color).shift(DOWN)
            parameter_traces.add(parameter_trace_i)

            target = max_time*unit(angle) + gravity*max_time*max_time*DOWN
            moving_point_i = Dot(color = color).shift(target).shift(DOWN)
            traces_path_i = ParametricCurve(projectile(angle), [0, max_time, 0.05], color = color, stroke_width = 2).shift(DOWN)
            points.add(moving_point_i)
            traces.add(traces_path_i)

        envelope = FunctionGraph(quadratic(-gravity, 0, 1/(4*gravity)), [-tangent, tangent, 0.1], color = [interpolate_color(GREEN, YELLOW, 0.5), YELLOW, ORANGE, interpolate_color(ORANGE, RED, 0.5)]).shift(DOWN)
        self.add(envelope)
        self.add(traces, parameter_traces, points)

        text1 = Text(r"定 速", color = interpolate_color(GREEN, YELLOW, 0.5), font = "FZDaHei-B02S").scale(3).shift(2.5*UP + 3.5*LEFT)
        text2 = Text(r"抛 体", color = interpolate_color(ORANGE, RED, 0.5), font = "FZDaHei-B02S").scale(3).shift(2.5*UP + 3.5*RIGHT)
        text3 = Text(r"包 络 线", color = interpolate_color(YELLOW, ORANGE, 0.5), font = "FZDaHei-B02S").scale(3).shift(2.5*DOWN)
        texts = VGroup(text1, text2, text3)
        # shadow1 = texts.copy().set_style(fill_opacity = 2/3).shift(0.1/3*DR)
        # shadow2 = texts.copy().set_style(fill_opacity = 1/3).shift(0.1/3*DR*2)
        # self.add(shadow2)
        # self.add(shadow1)
        self.add(texts)
        # self.add(text1, text2, text3)

        # def function(t):
        #     return np.array([-np.sin(t) - t/3, -np.cos(t) + t/3, 0])
        # arrow_line = ParametricCurve(function, t_range = [0, (2.8)*PI]).scale(0.3)
        # arrow_line.shift(DOWN - arrow_line.get_end()).shift(0.3*DL)
        # arrow_tip = ArrowTip(height = 0.2).shift(arrow_line.get_end())
        # arrow_tip.rotate((1/3)*PI, about_point = arrow_tip.get_base()).shift(0.1*DL)
        # text3 = Text(r"一只美丽的", font = "FZYaSong-B-GBK").next_to(arrow_line.get_start(), RIGHT).shift(0.3*RIGHT)
        # text4 = Text(r"包络线孔雀", font = "FZYaSong-B-GBK").next_to(text3, DOWN).shift(0.8*LEFT)
        # self.add(arrow_line, arrow_tip, text3, text4)

##############################################################

class Test3(Scene):
    def construct(self):

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

        #调试用
        # envelope = FunctionGraph(quadratic(-gravity, 0, 1/(4*gravity)), [-16, 16, 0.1]).shift(start_point)
        # self.add(envelope)

        collapse = Triangle(fill_opacity = 1, color = YELLOW, stroke_width = 0).scale(0.1)
        def collapse_updater(collapse: Triangle):
            tan = np.tan(angle.get_value())
            target = tan/((tan**2 + 1)*gravity)*RIGHT + start_point
            collapse.next_to(target, DOWN, buff = 0.1)
        collapse.add_updater(collapse_updater)

        max_target = RIGHT/(2*gravity) + start_point
        max_collapse = Triangle(fill_opacity = 1, color = GREEN, stroke_width = 0).scale(0.1).next_to(max_target, DOWN, buff = 0.1)
        
        group_below = VGroup(background, ground, bow_1, bow_below, knot_below)
        group_string_above = VGroup(bag, string_above)
        group_above = VGroup(bow_above, knot_above)
        self.play(FadeIn(group_below, UP), FadeIn(string_below, UP), FadeIn(bird, DOWN), FadeIn(group_string_above, UP), FadeIn(group_above, UP))
        self.wait(1)
        bird.add_updater(bird_updater)
        bag.add_updater(bag_updater)
        string_above.add_updater(string_above_updater)
        string_below.add_updater(string_below_updater)
        self.play(ApplyMethod(radius.set_value, 1.0), Write(group_dots), run_time = 1)
        self.play(FadeInFromPoint(collapse, 0.1*UP), run_time = 0.5)
        self.bring_to_back(max_collapse)
        self.wait(0.5)
        self.play(ApplyMethod(angle.set_value, PI+PI/12))
        self.wait(1)
        self.play(ApplyMethod(angle.set_value, PI*3/2-PI/12))
        self.wait(1)
        self.play(ApplyMethod(angle.set_value, PI*5/4))
        self.wait(1)
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
        self.wait(1)

        angle1 = ValueTracker(PI/4)
        angle2 = ValueTracker(3*PI/4)
        def tangent_point(angle: float):
            tan = np.tan(angle)
            return np.array([1/(2*gravity*tan), (1-1/(tan**2))/(4*gravity), 0])
        # probe1 = Dot().shift(tangent_point(PI/4))
        # probe2 = Dot().shift(tangent_point(PI/3))
        # probe3 = Dot().shift(tangent_point(PI/2))
        # self.add(probe1, probe2, probe3)
        def background_function(angle1: float, angle2:float):
            tan1 = np.tan(angle1)
            tan2 = np.tan(angle2)
            return lambda x: x*(-gravity*(tan1*tan2+1)*x + (tan1+tan2)/2)
        # probe_function = FunctionGraph(background_function(PI/4, PI/4), [-16, 16, 0.1]).shift(np.array([-5, -1, 0]))
        # self.add(probe_function)

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
        self.wait(1)
        self.play(ApplyMethod(angle1.set_value, PI/3), ApplyMethod(angle2.set_value, 5*PI/6))
        self.wait(1)
        self.play(ApplyMethod(angle1.set_value, 82*PI/360))
        self.wait(1)
        self.play(ApplyMethod(angle1.set_value, PI/3), ApplyMethod(angle2.set_value, 7*PI/12))
        self.wait(1)
        
####################################################################


class Test4(Scene):
    def construct(self):
        
        image_knife = ImageMobject("knife.png", height = 8)
        grid = ComplexPlane(faded_line_ratio = 9)
        # position_0 = np.array([0, -4, 0])
        # position_1 = np.array([0.4, -3.2, 0])
        # position_2 = np.array([0.4, -2.6, 0])
        # position_4 = np.array([0.35, 2.05, 0])
        # position_3 = (position_2 + position_4)/2
        # position_5 = np.array([0.5, 2.15, 0])
        # position_6 = np.array([0.5, 2.25, 0])
        # position_7 = np.array([0.5, 2.4, 0])
        # position_8 = np.array([0.3, 2.5, 0])
        # position_9 = np.array([0.3, 2.6, 0])
        # position_10 = np.array([0.25, 2.6, 0])
        # position_11 = np.array([0.15, 3.2, 0])
        # position_12 = np.array([0.3, 3.5, 0])
        # position_13 = np.array([0.5, 3.7, 0])
        # position_14 = np.array([0.2, 3.8, 0])
        # position_15 = np.array([0.2, 4, 0])
        # position_16 = np.array([0, 4, 0])
        # knife = VMobject()
        # knife.set_points([position_0, position_1, position_2, position_2, position_3, position_4, position_4, position_5, position_6, position_6, position_7, position_8, position_8, position_9, position_10, position_10, position_11, position_12, position_12, position_13, position_14, position_14, position_15, position_16])
        position = np.zeros((33, 3))
        position[0: 17] = np.array([[0, -4, 0], 
        [0.4, -3.2, 0], [0.4, -2.6, 0], [0.375, -0.275, 0], [0.35, 2.05, 0], 
        [0.5, 2.15, 0], [0.5, 2.25, 0], [0.5, 2.4, 0], [0.3, 2.5, 0], 
        [0.3, 2.6, 0], [0.25, 2.6, 0], [0.15, 3.2, 0], [0.3, 3.5, 0], 
        [0.5, 3.7, 0], [0.2, 3.8, 0], [0.2, 4, 0], [0, 4, 0]])
        position[17: 33, 0] = -position[15::-1, 0]
        position[17: 33, 1] = position[15::-1, 1]
        
        points = np.zeros((48, 3))
        points[0::3] = position[0:-1:2]
        points[1::3] = position[1::2]
        points[2::3] = position[2::2]
        knife = VMobject()
        knife.set_points(points)
        self.add(image_knife, grid, knife, )

class Test5(Scene):
    def construct(self):
        
        image_knife = ImageMobject("dagger.png", height = 8).shift(0.06*RIGHT)
        grid = ComplexPlane(faded_line_ratio = 9)

        dagger = VMobject().set_color(RED)
        position_0 = np.array([0, -4, 0])
        position_1 = np.array([0.325, -3.5, 0])
        position_2 = np.array([0.65, -3, 0])
        position_3 = np.array([0.65, -0.45, 0])
        position_4 = np.array([0.65, 2.1, 0])
        position_5 = np.array([0.6, 2.2, 0])
        position_6 = np.array([0.55, 2.3, 0])
        position_7 = np.array([0.55, 2.9, 0])
        position_8 = np.array([0.55, 3.5, 0])
        position_9 = np.array([0.55, 3.85, 0])
        position_10 = np.array([0.35, 4, 0])
        position_11 = np.array([0.175, 4, 0])
        position_12 = np.array([0, 4, 0])
        dagger.set_points([position_0, position_1, position_2, position_2, position_3, position_4, position_4, position_5, position_6, position_6, position_7, position_8, position_8, position_9, position_10, position_10, position_11, position_12])
        self.add(image_knife, grid, dagger, )

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

class Test6(Scene):
    def construct(self):
        # knife = Knife().scale(0.75)
        # dagger = Dagger().scale(0.75)
        # self.add(knife.shift(LEFT), dagger.shift(RIGHT))

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
            number_i = Tex("%d"%i).scale(0.8).shift(3.1*UP).rotate(-angle, about_point = ORIGIN).set_opacity(0)
            outer_text.add(text_i)
            outer_number.add(number_i)

        # outer_radius = 2.6
        # inner_radius = 2.5
        # positions = np.zeros((12 * number_letters, 3))
        # step_angle = TAU/(4*number_letters)
        # outer_samples = np.array([outer_radius * unit(a) for a in np.linspace(PI/2 + step_angle, -3*PI/2 + step_angle, 4*number_letters + 1)])
        # outer_samples[1::2] /= np.cos(step_angle)
        # inner_samples = np.array([inner_radius * unit(a) for a in np.linspace(PI/2 + step_angle, -3*PI/2 + step_angle, 4*number_letters + 1)])
        # inner_samples[1::2] /= np.cos(step_angle)

        # positions = np.zeros((12 * number_letters, 3))
        # positions[0::12] = outer_samples[0:-1:4]
        # positions[1::12] = outer_samples[1::4]
        # positions[2::12] = outer_samples[2::4]
        # positions[3::12] = outer_samples[2::4]
        # positions[4::12] = (outer_samples[2::4] + inner_samples[2::4])/2
        # positions[5::12] = inner_samples[2::4]
        # positions[6::12] = inner_samples[2::4]
        # positions[7::12] = inner_samples[3::4]
        # positions[8::12] = inner_samples[4::4]
        # positions[9::12] = inner_samples[4::4]
        # positions[10::12] = (outer_samples[4::4] + inner_samples[4::4])/2
        # positions[11::12] = outer_samples[4::4]
        # gear_inner = VMobject()
        # gear_inner.set_points(positions)
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
            number_i = Tex("%d"%i, opacity = 0, color = YELLOW_E).scale(0.7).shift(1.9*UP).rotate(-angle, about_point = ORIGIN).set_opacity(0)
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

        self.play(FadeIn(outer_layer), FadeIn(inner_layer), run_time = 0.8)
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

        # alpha = ValueTracker(0.0) #全局相位
        beta = ValueTracker(0.0) #分组偏差
        gamma = ValueTracker(0.0) #个体偏差
        radius_a = ValueTracker(10.0) #半径
        radius_b = ValueTracker(10.0) #半径

        def a_updater(order: int):
            def util(mob: Knife, dt):
                mob.angle -= dt * PI / 6
                # angle_a = alpha.get_value()
                angle_b = beta.get_value()
                angle_c = gamma.get_value()
                r = radius_a.get_value()
                mob.restore().rotate(angle_c).shift(r*UP).rotate(mob.angle + angle_b, about_point = ORIGIN)
            return util
        
        def b_updater(order: int):
            def util(mob: Knife, dt):
                mob.angle -= dt * PI / 6
                # angle_a = alpha.get_value()
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
        

        print(self.num_plays, self.time + 38 + 23/30)
        
    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

####################################################################

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):

        super().__init__()
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

class Intro0_English(Scene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("数学频道有一个基本任务：\n找到物理问题中的美妙结构，\n并阻止学物理的同学直接开始计算。", font = 'simsun', t2c={"物理问题": GREEN, "美妙结构": BLUE, "阻止": YELLOW, "计算": YELLOW})
        quote.shift(2*UP)
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman").next_to(quote.get_corner(DOWN + RIGHT), DOWN + LEFT)
        quote_english = Text(" A main task of a mathematical channel \n is to find elegant structures in physical problems\n and to stop physics students from calculating.", font = "Times New Roman", t2c={"physical problems": GREEN, "elegant structures": BLUE, "stop": YELLOW, "calculating": YELLOW})
        quote_english.scale(0.8).shift(1*DOWN)
        author_english = Text("-Said by myself", color = YELLOW, font = "Times New Roman").next_to(quote_english.get_corner(DOWN + RIGHT), DOWN + LEFT)
        
        ##  Showing object
        self.play(Write(quote), Write(quote_english), runtime = 2)
        self.play(Write(author), Write(author_english), Write(notice0))
        self.wait(2)
        self.play(FadeOut(quote), FadeOut(author), FadeOut(quote_english), FadeOut(author_english))
        self.wait(1)

class Chapter1_0_English(Scene):

    def construct(self):

        ##  Making object
        text1 = Text("第一节 斜抛运动的轨迹", font = 'simsun', t2c={"第一节": YELLOW, "斜抛运动": GREEN, "轨迹": BLUE})
        text1_english = Text("Chapter 1 Traces of Projectiles", font = 'Times New Roman', t2c={"Chapter 1": YELLOW, "Projectiles": GREEN, "Traces": BLUE}).scale(0.8).next_to(text1, DOWN)
        VGroup(text1, text1_english).center()
        self.play(Write(text1), Write(text1_english), run_time = 1)
        self.wait(1)
        self.play(FadeOut(text1), FadeOut(text1_english))

class Chapter2_0_English(Scene):

    def construct(self):

        ##  Making object
        text2 = Text("第二节 抛体轨迹的包络", font = 'simsun', t2c={"第一节": YELLOW, "抛体轨迹": GREEN, "包络": BLUE})
        text2_english = Text("Chapter 2 Envelope of Projectiles", font = 'Times New Roman', t2c={"Chapter 2": YELLOW, "Projectiles": GREEN, "Envelope": BLUE}).scale(0.8).next_to(text2, DOWN)
        VGroup(text2, text2_english).center()
        self.play(Write(text2), Write(text2_english), run_time = 1)
        self.wait(1)
        self.play(FadeOut(text2), FadeOut(text2_english))

class Chapter3_0_English(Scene):

    def construct(self):

        ##  Making object
        text3 = Text("第三节 高速抛体的范围", font = 'simsun', t2c={"第三节": YELLOW, "高速抛体": GREEN, "范围": BLUE})
        text3_english = Text("Chapter 3 Envelope in High Speed Case", font = 'Times New Roman', t2c={"Chapter 3": YELLOW, "High Speed Case": GREEN, "Envelope": BLUE}).scale(0.8).next_to(text3, DOWN)
        VGroup(text3, text3_english).center()
        self.play(Write(text3), Write(text3_english), run_time = 1)
        self.wait(1)
        self.play(FadeOut(text3), FadeOut(text3_english))