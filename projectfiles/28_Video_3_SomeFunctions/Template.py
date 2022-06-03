from manimlib import *
import numpy as np

class Chip(VGroup):
    def __init__(self):

        super().__init__()
        lines = VGroup()
        for i in range (9):
            linei = Line(np.array([0, 0.15, 0]), np.array([0, -0.15, 0])).shift(0.5*(i-4)*UP)
            lines.add(linei)
        pins = VGroup()
        for i in range (8):
            pini = Rectangle(height = 0.2, width = 0.4).shift(0.5*(i-3.5)*UP)
            pins.add(pini)
        left_lines = lines.copy().shift(2.15*LEFT)
        right_lines = lines.copy().shift(2.15*RIGHT)
        left_pins = pins.copy().shift(2.3*LEFT)
        right_pins = pins.copy().shift(2.3*RIGHT)
        upper = Line(np.array([-2.15, 2.15, 0]), np.array([2.15, 2.15, 0]))
        lower = Line(np.array([-2.15, -2.15, 0]), np.array([2.15, -2.15, 0]))
        self.add(left_lines, right_lines, left_pins, right_pins, upper, lower)

class Test1(Scene):
    def construct(self):

        chip = Chip()
        self.add(chip)

#############################################################

class SwallowIn(Homotopy):
    CONFIG = {
        "run_time": 2,
    }

    def __init__(self, mobject, target, **kwargs):
        digest_config(self, kwargs, locals())

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

class Unfold(Homotopy):
    CONFIG = {
        "run_time": 2,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs, locals())

        center = mobject.get_center()

        size = get_norm(center - mobject.get_corner(UL))

        def homotopy(x, y, z, t):
            vect = np.array([x, y, z]) - center
            length = get_norm(vect)
            move = t * size
            if move >= length:
                return vect + center
            else:
                ratio = move / length
                return ratio * vect + center

        super().__init__(homotopy, mobject, **kwargs)

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


class Grid(VGroup):
    def __init__(self, size, buff):

        super().__init__()
        # stroke = 0.005
        height = size[0] * buff
        width = size[1] * buff
        line_x = VGroup()
        for i in range (size[0]+1):
            # linei = Rectangle(width = width + stroke, height = stroke, fill_opacity = 1, stroke_width = 0).shift((i - size[0]/2) * buff * UP)
            linei = Line(width/2 * LEFT, width/2 * RIGHT, stroke_width = 2).shift((i - size[0]/2) * buff * UP).insert_n_curves(17)
            line_x.add(linei)
        line_y = VGroup()
        for i in range (size[1]+1):
            # linei = Rectangle(width = stroke, height = height + stroke, fill_opacity = 1, stroke_width = 0).shift((i - size[1]/2) * buff * RIGHT)
            linei = Line(height/2 * UP, height/2 * DOWN, stroke_width = 2).shift((i - size[0]/2) * buff * RIGHT).insert_n_curves(17)
            line_y.add(linei)
        self.add(line_x, line_y)


class Test2(Scene):
    def construct(self):
        chip = Chip().shift(4*LEFT)
        config_alex = Tex("\mathscr{A}").scale(3).move_to(np.array([4.4, 0, 0]))
        self.add(chip, config_alex)
        self.wait(1)
        self.play(SwallowIn(config_alex, 4*LEFT), run_time = 2)
        
        grid = Grid(np.array([16, 16]), 0.25).shift(4*LEFT).set_color(YELLOW).set_stroke(width = 1.5)
        grid2 = Grid(np.array([16, 16]), 0.25).shift(4*LEFT).set_color(GREY)
        self.add(grid)
        anims = LaggedStart(SpreadOut(grid).update_config(rate_func = linear), SpreadOut(grid2).update_config(rate_func = linear))
        self.play(anims, run_time = 2.5)
        self.remove(grid)
        
        self.wait(1)

###############################################################

class Series(VGroup):
    def __init__(self, m_symbol, m_start, m_length):

        super().__init__()
        self.symbol = m_symbol
        self.start = m_start
        self.length = m_length
        self.term = []
        for i in range (self.length):
            termi = MTex(self.symbol + f"_{i + self.start}").scale(0.8).shift((i - (self.length-1)/2) * LEFT)
            self.term.append(termi)
            self.add(termi)

class LongMultiplication(VGroup):
    h_space = 1.4
    v_space = 0.7
    def __init__(self, m_mul_1 : Series, m_mul_2 : Series, m_target, m_bounded = False):

        if m_mul_1.length < m_mul_2.length:
            self.mul_1, self.mul_2 = m_mul_2, m_mul_1
        else:
            self.mul_1, self.mul_2 = m_mul_1, m_mul_2
        

        super().__init__(self.mul_1, self.mul_2)
        self.mul_1.set_color(BLUE)
        self.mul_2.set_color(RED)

        for i in range (self.mul_1.length):
            self.mul_1.term[i].next_to(self.h_space*i*LEFT + self.v_space*1*UP, UP+LEFT, buff = 0.2)
        for j in range (self.mul_2.length):
            self.mul_2.term[j].next_to(self.h_space*j*LEFT + self.v_space*0*UP, UP+LEFT, buff = 0.2)
        self.mul = MTex(r"\times").next_to(self.h_space*self.mul_1.length*LEFT + self.v_space*0*UP, UP+LEFT)
        self.add(self.mul)

        self.upper_line = Line(self.h_space*0.1*RIGHT, self.h_space*(self.mul_1.length+0.5)*LEFT)
        self.add(self.upper_line)

        self.bounded = m_bounded
        if self.bounded:
            self.result = Series(m_target, self.mul_1.start + self.mul_2.start + self.mul_2.length - 1, self.mul_1.length - self.mul_2.length + 1).set_color(YELLOW)    

            self.terms_mul_1 = []
            self.terms_mul_2 = []
            group_mul_1 = VGroup()
            group_mul_2 = VGroup()
            for i in range (self.result.length):
                self.terms_mul_1.append([])
                self.terms_mul_2.append([])
                for j in range(self.mul_2.length):
                    term2 = self.mul_2.term[j].copy().next_to(self.h_space*(i+self.mul_2.length-1)*LEFT + self.v_space*(j+1)*DOWN, UP+LEFT, buff = 0.2)
                    term1 = self.mul_1.term[i+self.mul_2.length-j-1].copy().next_to(term2.get_corner(DOWN+LEFT), UP+LEFT, buff = 0).shift(0.08*LEFT)
                    self.terms_mul_1[i].append(term1)
                    self.terms_mul_2[i].append(term2)
                    group_mul_1.add(term1)
                    group_mul_2.add(term2)
            self.add(group_mul_1, group_mul_2)

            self.lower_line = Line(self.h_space*(self.mul_2.length-1.1)*LEFT + self.v_space*self.mul_2.length*DOWN, self.h_space*(self.result.length+self.mul_2.length-0.8)*LEFT + self.v_space*self.mul_2.length*DOWN)
            self.add(self.lower_line)

            for k in range (self.result.length):
                self.result.term[k].next_to(self.h_space*(k+self.mul_2.length-1)*LEFT +self.v_space*(self.mul_2.length+1)*DOWN, UP+LEFT, buff = 0.2)
            self.add(self.result)

        else:
            self.result = Series(m_target, self.mul_1.start + self.mul_2.start, self.mul_1.length + self.mul_2.length - 1).set_color(YELLOW) 

            self.terms_mul_1 = []
            self.terms_mul_2 = []
            group_mul_1 = VGroup()
            group_mul_2 = VGroup()
            for i in range (self.mul_1.length):
                self.terms_mul_1.append([])
                self.terms_mul_2.append([])
                for j in range(self.mul_2.length):
                    term2 = self.mul_2.term[j].copy().next_to(self.h_space*(i+j)*LEFT + self.v_space*(j+1)*DOWN, UP+LEFT, buff = 0.2)
                    term1 = self.mul_1.term[i].copy().next_to(term2.get_corner(DOWN+LEFT), UP+LEFT, buff = 0).shift(0.08*LEFT)
                    self.terms_mul_1[i].append(term1)
                    self.terms_mul_2[i].append(term2)
                    group_mul_1.add(term1)
                    group_mul_2.add(term2)
            self.add(group_mul_1, group_mul_2)

            self.lower_line = Line(self.h_space*0.1*RIGHT + self.v_space*self.mul_2.length*DOWN, self.h_space*(self.result.length)*LEFT + self.v_space*self.mul_2.length*DOWN)
            self.add(self.lower_line)

            for k in range (self.result.length):
                self.result.term[k].next_to(self.h_space*k*LEFT +self.v_space*(self.mul_2.length+1)*DOWN, UP+LEFT, buff = 0.2)
            self.add(self.result)

        self.center()
    
    def get_duality(self):
        if self.bounded:
            self.terms_result = []
            group_result = VGroup()
            for i in range (self.result.length):
                self.terms_result.append([])
                for j in range(self.mul_2.length):
                    term = self.result.term[i].copy().next_to(self.terms_mul_2[i][j].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.08*RIGHT)
                    self.terms_result[i].append(term)
                    group_result.add(term)
        else:
            self.terms_result = []
            group_result = VGroup()
            for i in range (self.mul_1.length):
                self.terms_result.append([])
                for j in range(self.mul_2.length):
                    term = self.result.term[i+j].copy().next_to(self.terms_mul_2[i][j].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.08*RIGHT)
                    self.terms_result[i].append(term)
                    group_result.add(term)
        return group_result

    def get_polynomial(self):
        if self.bounded:
            return VGroup()
        else:
            group_poly_mul_1 = VGroup()
            for i in range (self.mul_1.length):
                if i == 0:
                    term = MTex(f"", color = PURPLE_A)
                elif i == 1:
                    term = MTex(f"x\ \ +", tex_to_color_map = {r"x": PURPLE_A})
                else:
                    term = MTex(f"x^{i}\ +", tex_to_color_map = {f"x^{i}": PURPLE_A})
                term.scale(0.8).next_to(self.mul_1.term[i].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0.03).shift(0.05*RIGHT)
                group_poly_mul_1.add(term)
            polynomial = MTex(r"=\ f(x)", tex_to_color_map = {r"f(x)": interpolate_color(BLUE, PURPLE, 0.5)}).scale(0.8).next_to(self.mul_1.term[0].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.3*RIGHT+0.05*DOWN)
            group_poly_mul_1.add(polynomial)
            
            group_poly_mul_2 = VGroup()
            for j in range (self.mul_2.length):
                if j == 0:
                    term = MTex(f"", color = PURPLE_A)
                elif j == 1:
                    term = MTex(f"x\ \ +", tex_to_color_map = {r"x": PURPLE_A})
                else:
                    term = MTex(f"x^{j}\ +", tex_to_color_map = {f"x^{j}": PURPLE_A})
                term.scale(0.8).next_to(self.mul_2.term[j].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0.03).shift(0.05*RIGHT)
                group_poly_mul_2.add(term)
            polynomial = MTex(r"=\ g(x)", tex_to_color_map = {r"g(x)": interpolate_color(RED, PURPLE, 0.5)}).scale(0.8).next_to(self.mul_2.term[0].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.3*RIGHT+0.05*DOWN)
            group_poly_mul_2.add(polynomial)

            group_poly_result = VGroup()
            for k in range (self.result.length):
                if k == 0:
                    term = MTex(f"", color = PURPLE_A)
                elif k == 1:
                    term = MTex(f"x\ \ +", tex_to_color_map = {r"x": PURPLE_A})
                else:
                    term = MTex(f"x^{k}\ +", tex_to_color_map = {f"x^{k}": PURPLE_A})
                term.scale(0.8).next_to(self.result.term[k].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0.03).shift(0.05*RIGHT)
                group_poly_result.add(term)
            polynomial = MTex(r"=\ h(x)", tex_to_color_map = {r"h(x)": ORANGE}).scale(0.8).next_to(self.result.term[0].get_corner(DOWN+RIGHT), UP+RIGHT, buff = 0).shift(0.3*RIGHT+0.05*DOWN)
            group_poly_result.add(polynomial)
            
            return [group_poly_mul_1, group_poly_mul_2, group_poly_result]

class Test3(Scene):
    def construct(self):
        series_a = Series(r"a", 0, 3)
        series_b = Series(r"b", 0, 2)
        # series_c = Series("c", 3, 5).shift(DOWN)
        # self.add(series_a, series_b, series_c)
        long_multiplication = LongMultiplication(series_a, series_b, r"c", False)
        self.add(long_multiplication)
        self.add(*long_multiplication.get_polynomial())
        self.add(long_multiplication.get_duality())
        
##################################################################

class Test4(Scene):

    def construct(self):
        moving_point = Dot()
        moving_point.save_state()
        traces_path = TracedPath(moving_point.get_center)
        alpha = ValueTracker(0.0)

        def moving_updater(mob: Mobject):
            a = alpha.get_value()
            mob.restore().shift(np.array([a, a**2, 0]))

        self.add(moving_point, traces_path)
        moving_point.add_updater(moving_updater)
        self.wait(1)
        self.play(ApplyMethod(alpha.set_value, 3.0), rate_func = linear, run_time = 3)
        self.wait(1)

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def angle_color(angle):

    # colors = ["#FF0000", "#FFFF00", "#00FF00", "#00FFFF", "#0000FF", "#FF00FF"]
    # colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    # colors = [RED, YELLOW, GREEN, TEAL, BLUE, PURPLE]
    colors = [TEAL, BLUE, BLUE, TEAL, GREEN, GREEN]

    number_colors = len(colors)
    ratio = number_colors*angle/TAU
    index = int(ratio)
    interpolate = ratio - index

    return interpolate_color(colors[index%number_colors], colors[(index+1)%number_colors], interpolate)

class Test5(Scene):

    def construct(self):
        gravity = 1/3
        alpha = ValueTracker(0.0)

        def moving_updater(angle):
            def util(angle: float, mob: Mobject):
                a = alpha.get_value()
                mob.restore().shift(a*unit(angle) + gravity*a*a*DOWN)
            return lambda x: util(angle, x)

        points = []
        traces = []
        number = 30
        for i in range (number):
            angle = TAU * i / number
            color = angle_color(angle)
            moving_point_i = Dot().shift(DOWN).set_color(color).save_state()
            traces_path_i = TracedPath(moving_point_i.get_center).set_color(color)
            points.append(moving_point_i)
            traces.append(traces_path_i)
            moving_point_i.add_updater(moving_updater(angle))
            self.add(moving_point_i, traces_path_i)

        self.wait(1)
        self.play(ApplyMethod(alpha.set_value, 2.0), rate_func = linear, run_time = 2)
        self.wait(1)

###############################################################################################

colors = ["#0080FF", "#9999FF", "#00FFCC", "#66CCFF", "#EE82EE", "#006666", "#FFFF00"]

class Block(VGroup):
    def __init__(self, m_relative, m_width, m_height, m_name, m_color, m_coor_x = 0, m_coor_y = 0):

        super().__init__()
        if m_relative:
            height = m_height * 0.25 - 0.1
            width = m_width * 0.25 - 0.1
            position = 6*LEFT + 2*DOWN + (m_coor_x+m_width/2)*0.25*RIGHT + (m_coor_y+m_height/2)*0.25*UP
            text_scale = min(0.8, height)*1.25
        else:
            height = m_height
            width = m_width
            position = 3*RIGHT
            text_scale = 1

        self.block = Rectangle(height = height, width = width, color = m_color, fill_color = interpolate_color(m_color, "#333333", 0.5), fill_opacity = 0.8)
        self.name  = Tex(m_name, color = m_color).scale(text_scale)
        self.add(self.block, self.name)
        self.move_to(position)
        
class FullChip(Chip):
    def __init__(self):

        super().__init__()
        
        block1 = Block(True, 3, 4, "", colors[0], 0, 0)
        block2 = Block(True, 4, 2, "", colors[1], 3, 0)
        block3 = Block(True, 4, 3, "", colors[1], 3, 2)
        block4 = Block(True, 7, 14, "", colors[2], 9, 0)
        block5 = Block(True, 9, 11, "", colors[3], 0, 5)
        block6 = Block(True, 3, 1, "", colors[4], 0, 4)
        block7 = Block(True, 2, 1, "", colors[5], 7, 0)
        block8 = Block(True, 2, 1, "", colors[5], 7, 1)
        block9 = Block(True, 2, 1, "", colors[5], 7, 2)
        block10 = Block(True, 2, 1, "", colors[5], 7, 3)
        block11 = Block(True, 2, 1, "", colors[5], 7, 4)
        block12 = Block(True, 1, 2, "", colors[6], 9, 14)
        block13 = Block(True, 2, 2, "", colors[6], 10, 14)
        block14 = Block(True, 1, 2, "", colors[6], 12, 14)
        block15 = Block(True, 2, 2, "", colors[6], 13, 14)
        block16 = Block(True, 1, 2, "", colors[6], 15, 14)
        blocks = VGroup(block1, block6, block2, block3, block7, block8, block9, block10, block11, block5, block4, block12, block13, block14, block15, block16).shift(4*RIGHT)
        self.add(blocks)     

class Cover(Scene):

    def construct(self):

        text1 = Text(r"AI", color = BLUE, font = "Times New Roman", font_size = 55, weight = BOLD).scale(4).shift(2.2*UP + 4.5*LEFT)
        text2 = Text(r"与芯片", t2c = {"芯片": GREEN}, font = "FZDaHei-B02S").scale(4).shift(2.2*UP + 2.5*RIGHT)
        for i in range (3):
            text2[i].shift(0.1*i*RIGHT)
        position = (text1.get_corner(RIGHT) + text2.get_corner(LEFT)) /2

        fullchip = FullChip().scale(0.75).shift(position + 3.5*DOWN)
        string = Line(position + 2*UP, position + (3.5-2.15*0.75)*DOWN, stroke_width = 1.5)
        def function(t):
            return np.array([np.cos(t) - t/3, np.sin(t) + t/3, 0])
        arrow_line = ParametricCurve(function, t_range = [0, (2.8)*PI]).scale(0.3).next_to(fullchip.get_corner(UR), DR, buff = 0).shift(0.4*RIGHT + 0.1*UP)
        arrow_tip = ArrowTip(height = 0.2).shift(arrow_line.get_end())
        arrow_tip.rotate((7/6)*PI, about_point = arrow_tip.get_base())
        text3 = Text(r"一只可爱的", font = "FZYaSong-B-GBK").next_to(arrow_line.get_start(), DOWN).shift(0.3*RIGHT)
        text4 = Text(r"芯片小蜘蛛", font = "FZYaSong-B-GBK").next_to(text3, DOWN).shift(0.8*RIGHT)

        self.add(fullchip, text1, text2, string, arrow_line, arrow_tip, text3, text4)

class Trailer(Scene):

    def construct(self):

        fullchip = FullChip().shift(0.5*DOWN)
        string = Line(4*UP, (0.5-2.15)*DOWN, stroke_width = 1.5)
        self.add(fullchip, string)

########################################################################

OMEGA = np.array([math.sqrt(3)/2, -1/2, 0])

class SnowFlake(VGroup):
    def __init__(self):

        super().__init__()
        snowhex1 = SnowHex(2, 1)
        snowhex2 = SnowHex(6,2)
        snowhex3 = SnowHex(6,3)
        snowhex4 = SnowHex(6,4)
        snowring2 = VGroup(snowhex1)
        snowring3 = SnowRing(3)
        snowring4 = SnowRing(4)
        snowring5 = SnowRing(5)
        snowring6 = VGroup(snowhex2, snowhex3, snowhex4)
        # edge_radius = (6.7/4)*(3+math.sqrt(3))
        # arc1 = Arc(radius = edge_radius, angle = PI, start_angle = -PI/2)
        # arc1.shift((-UP-2*OMEGA) * edge_radius)
        # arc2 = Arc(radius = edge_radius, angle = PI, start_angle = -5*PI/6)
        # arc2.shift((UP-OMEGA) * edge_radius)
        # arc3 = Arc(radius = edge_radius, angle = PI, start_angle = 5*PI/6)
        # arc3.shift((2*UP+OMEGA) * edge_radius)
        # arc4 = Arc(radius = edge_radius, angle = PI, start_angle = PI/2)
        # arc4.shift((UP+2*OMEGA)*edge_radius)
        # arc5 = Arc(radius = edge_radius, angle = PI, start_angle = PI/6)
        # arc5.shift((-UP+OMEGA) * edge_radius)
        # arc6 = Arc(radius = edge_radius, angle = PI, start_angle = -PI/6)
        # arc6.shift((-2*UP-OMEGA) * edge_radius)
        # edge = VGroup(arc1, arc2, arc3, arc4, arc5, arc6)
        
        # outer_radius = 12
        # cycloids = VGroup()
        # for i in range (6):
        #     cycloid_i = Cycloid(outer_radius * unit(i*TAU/6 + TAU/12), outer_radius * unit((i+1)*TAU/6 + TAU/12))
        #     cycloids.add(cycloid_i)

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

class Cycloid(ParametricCurve):

    def __init__(self, start_point, end_point):

        super().__init__(lambda t: np.array([t - np.sin(t), 1 - np.cos(t), 0]), t_range = [0, TAU])
        self.put_start_and_end_on(start_point, end_point)

class Test6(Scene):
    def construct(self):

        # def function(t):
        #     return np.array([t - np.sin(t), 1 - np.cos(t), 0])
        # cycloid = ParametricCurve(function, t_range = [0, TAU]).put_start_and_end_on(LEFT, RIGHT)
        # cycloid = Cycloid(4*LEFT, 4*RIGHT)
        # cycloid2 = Cycloid(4*RIGHT, 4*LEFT)
        # self.add(cycloid, cycloid2)

        snowflake = SnowFlake()
        snowflake_2 = snowflake.copy().set_color(RED).set_stroke(width = 1.5)
        snowflake_3 = snowflake.copy().set_color(BLUE).set_stroke(width = 2)

        #self.add(snowflake)
        self.wait(1)
        anims = LaggedStart(SpreadOut(snowflake_2).update_config(rate_func = linear), SpreadOut(snowflake_3).update_config(rate_func = linear), SpreadOut(snowflake).update_config(rate_func = linear))
        self.play(anims, run_time = 3)
        self.remove(snowflake_2, snowflake_3)
        self.wait(1)