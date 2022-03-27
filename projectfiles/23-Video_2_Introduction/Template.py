from pickletools import UP_TO_NEWLINE
from manimlib import *
import numpy as np

OMEGA = np.array([math.sqrt(3)/2, -1/2, 0])

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):

        super().__init__()
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

class ApplyWaveUp1(Homotopy):
    CONFIG = {
        "direction": UP,
        "amplitude": 0.2,
        "run_time": 1,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs, locals())
        left_x = mobject.get_left()[0]
        right_x = mobject.get_right()[0]
        vect = self.amplitude * self.direction

        def homotopy(x, y, z, t):
            alpha = (x - left_x) / (right_x - left_x)
            power = np.exp(2.0 * (alpha - 0.5))
            nudge = there_and_back(t**power)
            return np.array([x, y, z]) + nudge * vect

        super().__init__(homotopy, mobject, **kwargs)

class ApplyWaveUp(Homotopy):
    CONFIG = {
        "direction": LEFT,
        "amplitude": 0.3,
        "run_time": 1,
    }

    def __init__(self, mobject, **kwargs):
        digest_config(self, kwargs, locals())
        bottom_y = mobject.get_bottom()[1]
        top_y = mobject.get_top()[1]
        left_x = mobject.get_left()[0]
        right_x = mobject.get_right()[0]
        
        def homotopy(x, y, z, t):
            alpha = (y - bottom_y) / (top_y - bottom_y)
            beta = (x - left_x) / (right_x - left_x)
            vect = self.amplitude * np.array([beta-0.5, 0, 0])
            factor = 4
            thershold = 1 / (2 * factor)
            scale = factor / (factor-1)
            distance = alpha-scale*(t-thershold)
            if abs(distance) < thershold :
                #nudge = np.cos(factor*2*np.pi*(distance))+1
                nudge = 2 * (0.5+factor*distance)**6.0 * (0.5-factor*distance)**2.0 * (4.0**8.0) / (3.0**6.0)
            else:
                nudge = 0
            #power = 2*np.exp(2.0 * (alpha - 0.5))
            #nudge = there_and_back(t**power)
            return np.array([x, y, z]) + nudge * vect

        super().__init__(homotopy, mobject, **kwargs)

def quadratic(a,b,c,x):
    return a*x*x + b*x + c

class UnderDoubleArrow(Line):
    CONFIG = {
        "buff": MED_SMALL_BUFF,
    }

    def __init__(self, mobject, text = 'w', **kwargs):

        super().__init__(LEFT, RIGHT, **kwargs)
        self.match_width(mobject)
        self.next_to(mobject, DOWN, buff=self.buff)
        self.add_tip(at_start=True, tip_style=1)
        self.add_tip(tip_style=1)

        line_left = Line(self.get_corner(UP+LEFT), self.get_corner(DOWN+LEFT), **kwargs)
        line_right = Line(self.get_corner(UP+RIGHT), self.get_corner(DOWN+RIGHT), **kwargs)

        width = Tex(text, **kwargs)
        width.next_to(self, DOWN, buff = 0)

        self.add(line_left, line_right, width)
        
class ParaHeight(Line):

    def __init__(self, curve = lambda x: -x*x+1, x_range = np.array([-1,1,50]), text = 'h', scale_factor = 1, **kwargs):

        self.curve = curve
        self.range = x_range
        medium = (x_range[0]+x_range[1])/2
        slope = (curve(x_range[0])-curve(x_range[1]))/(x_range[0]-x_range[1])

        super().__init__(scale_factor*np.array([medium, curve(medium), 0]), scale_factor*np.array([medium, (curve(x_range[0])+curve(x_range[1]))/2 , 0]), **kwargs)
        
        height = Tex(text, **kwargs)
        height.move_to(self.get_center())
        height.shift(0.3*(RIGHT+slope*UP))
        self.add(height)
        
class ParaArc(VMobject):
    CONFIG = {
        "color": BLUE,
        "fill_opacity": 0.2,
        "scale_factor": 1,
        "closed": False,
        "height": None,
        "width": None
    }
    def __init__(self, curve = lambda x: -x*x+1, x_range = np.array([-1,1,50]), **kwargs):

        self.curve = curve
        self.range = x_range
        VMobject.__init__(self, **kwargs)
        start = np.array([x_range[0], curve(x_range[0]), 0])
        end = np.array([x_range[1], curve(x_range[1]), 0])
        if self.closed:
            for i in range(int(x_range[2]+0.01)):
                self.add_line_to(end + i*(start-end)/x_range[2])
                self.append_points(end + i*(start-end)/x_range[2])
            self.close_path()
        # self.scale(self.scale_factor)
        self.all = VGroup(self)

        if self.height is None:
            pass
        elif self.height:
            medium = (x_range[0]+x_range[1])/2
            height_value = abs(curve(medium)-(curve(x_range[0])+curve(x_range[1]))/2)
            self.height_line = ParaHeight(curve, x_range, "%d"%height_value, color = YELLOW, scale_factor=self.scale_factor)
            self.all.add(self.height_line)
        else:
            self.height_line = ParaHeight(curve, x_range, color = YELLOW, scale_factor=self.scale_factor)
            self.all.add(self.height_line)

        if self.width is None:
            pass
        elif self.width:
            width_value = abs(x_range[1]-x_range[0])
            self.width_line = UnderDoubleArrow(self, "%d"%width_value, color = YELLOW)
            self.all.add(self.width_line)
        else:
            self.width_line = UnderDoubleArrow(self, color = YELLOW)
            self.all.add(self.width_line)

    def init_points(self):
        samples = np.array([[x, self.curve(x), 0] for x in np.linspace(self.range[0], self.range[1], int(2*self.range[2]+1) )])
        shift = (samples[0]+samples[2])/2 - samples[1]
        samples[1::2] -= shift
        points = np.zeros(( int(3*self.range[2]) , 3))
        points[0::3] = samples[0:-1:2]
        points[1::3] = samples[1::2]
        points[2::3] = samples[2::2]
        points *= self.scale_factor
        self.set_points(points)

    def set_range(self, start, end):
        target = ParaArc(curve = self.curve, x_range = np.array([start,end,self.range[2]]), closed = self.closed)
        self.set_points(target.get_points())
        return self

class ParaTriangle(VGroup):
    CONFIG = {
        "color": (BLUE, GREEN),
        "fill_opacity": 1,
        "scale_factor": 1,
        "stroke_color": WHITE,
        "stroke_width": 0,
        "closed": False,
    }
    def __init__(self, curve, x_range, recurse = 1, **kwargs):

        super().__init__()
        middle = (x_range[0]+x_range[1])/2
        triangle = Polygon(np.array([x_range[0],curve(x_range[0]),0]), np.array([x_range[1],curve(x_range[1]),0]), np.array([middle,curve(middle),0]), fill_opacity = self.fill_opacity)
        self.add(triangle)
        self.group_triangles = [triangle]
        if recurse > 1:
            left = ParaTriangle(curve, np.array([x_range[0],middle]), recurse-1)
            right = ParaTriangle(curve, np.array([middle,x_range[1]]), recurse-1)
            self.add(left, right)
            for i in range (recurse-1):
                group = VGroup(left.group_triangles[i], right.group_triangles[i])
                self.group_triangles.append(group)

        new_colors = color_gradient(self.color, len(self.group_triangles))
        for group, color in zip(self.group_triangles, new_colors):
            group.set_fill(color)
            group.set_stroke(width = self.stroke_width)

class RiemannRectangle(VGroup):
    CONFIG = {
        "color": (BLUE, GREEN),
        "fill_opacity": 1,
        "scale_factor": 1,
        "stroke_color": BLACK,
        "stroke_width": 1,
        "input_sample_type": "center",
        "closed": False,
        "height": None,
        "width": None
    }
    def __init__(self, curve1, curve2, x_range, **kwargs):

        super().__init__()

        rects = []
        xs = np.linspace(x_range[0], x_range[1], x_range[2]+1)
        for x0, x1 in zip(xs, xs[1:]):
            if self.input_sample_type == "left":
                sample = x0
            elif self.input_sample_type == "right":
                sample = x1
            elif self.input_sample_type == "center":
                sample = 0.5 * x0 + 0.5 * x1
            else:
                raise Exception("Invalid input sample type")
            up = curve1(sample)
            down = curve2(sample)
            rect = Polygon(np.array([x0,up,0]), np.array([x1,up,0]), np.array([x1,down,0]), np.array([x0,down,0]), stroke_color = self.stroke_color, stroke_width = self.stroke_width, fill_opacity = self.fill_opacity)
            rects.append(rect)
        self.add(*rects)

        new_colors = color_gradient(self.color, len(rects))
        for rect, color in zip(rects, new_colors):
            rect.set_fill(color)

class Sector(Arc):
    CONFIG = {
        "radius": 1,
        "angle": TAU / 4,
        "start_angle": 0,
        "fill_opacity": 1,
        "color": WHITE,
        "fill_color": BLUE
    }

    def init_points(self):
        arc = Arc(
                start_angle=self.start_angle,
                angle=self.angle,
                radius=self.radius,
                arc_center=self.arc_center,
            )
        self.append_points(self.arc_center)
        self.add_line_to(arc.get_points()[0])
        self.append_points(arc.get_points())
        self.close_path()

class SectorSegment(VGroup):
    CONFIG = {
        "color": (BLUE, GREEN, BLUE),
        "fill_opacity": 1,
        "scale_factor": 1,
        "stroke_color": WHITE,
        "stroke_width": 2,
        "input_sample_type": "center",
        "closed": False,
        "height": None,
        "width": None
    }
    def __init__(self, parts, radius = 1, **kwargs):
        super().__init__()

        sectors = []
        m_angle = TAU/parts
        for i in range (parts):
            sector = Sector(
                    radius = radius,
                    angle=m_angle,
                    start_angle = i * m_angle
                )
            sectors.append(sector)
        self.add(*sectors)

        new_colors = color_gradient(self.color, len(sectors))
        for sector, color in zip(sectors, new_colors):
            sector.set_fill(color)
            sector.set_stroke(width = self.stroke_width)

class SectorRectangle(VGroup):
    CONFIG = {
        "color": (BLUE, GREEN, BLUE),
        "fill_opacity": 1,
        "scale_factor": 1,
        "stroke_color": WHITE,
        "stroke_width": 2,
        "input_sample_type": "center",
        "closed": False,
    }
    def __init__(self, parts, radius = 1, **kwargs):
        super().__init__()

        sectors = []
        m_angle = TAU/parts
        width = 2*radius*np.sin(m_angle/2)
        height = radius*np.cos(m_angle/2)
        for i in range (int(parts/2)):
            sector = Sector(
                    radius = radius,
                    angle=m_angle,
                    start_angle = TAU/4 - m_angle/2
                )
            self.shift(width*RIGHT)
            sectors.append(sector)
            self.add(sector)
        self.shift(0.5*width*LEFT + height*DOWN)

        for i in range (parts-int(parts/2)):
            sector = Sector(
                    radius = radius,
                    angle=m_angle,
                    start_angle = 3*TAU/4 - m_angle/2
                )
            sector.shift(i*width*RIGHT)
            sectors.append(sector)
            self.add(sector)

        self.shift(0.5*height*UP + width * (parts/4-0.75) * LEFT)

        new_colors = color_gradient(self.color, len(sectors))
        for sector, color in zip(sectors, new_colors):
            sector.set_fill(color)
            sector.set_stroke(width = self.stroke_width)

class BipartitedSectorRectangle(VGroup):
    CONFIG = {
        "color": (BLUE, GREEN, BLUE),
        "fill_opacity": 1,
        "scale_factor": 1,
        "stroke_color": WHITE,
        "stroke_width": 2,
        "input_sample_type": "center",
        "closed": False,
        "height": None,
        "width": None
    }
    def __init__(self, parts, radius = 1, **kwargs):
        super().__init__()

        sectors = []
        m_angle = TAU/parts
        width = 2*radius*np.sin(m_angle/2)
        height = radius*np.cos(m_angle/2)
        for i in range (int(parts/2)):
            sector1 = Sector(
                    radius = radius,
                    angle=m_angle/2,
                    start_angle = TAU/4 - m_angle/2
                )
            sector2 = Sector(
                    radius = radius,
                    angle=m_angle/2,
                    start_angle = TAU/4
                )
            self.shift(width*RIGHT)
            sectors.append(sector1)
            sectors.append(sector2)
            self.add(sector1, sector2)
        self.shift(0.5*width*LEFT + height*DOWN)

        for i in range (parts-int(parts/2)):
            sector1 = Sector(
                    radius = radius,
                    angle=m_angle/2,
                    start_angle = 3*TAU/4 - m_angle/2
                )
            sector2 = Sector(
                    radius = radius,
                    angle=m_angle/2,
                    start_angle = 3*TAU/4
                )
            sector1.shift(i*width*RIGHT)
            sector2.shift(i*width*RIGHT)
            sectors.append(sector1)
            sectors.append(sector2)
            self.add(sector1, sector2)

        self.shift(0.5*height*UP + width * (parts/4-0.75) * LEFT)

        new_colors = color_gradient(self.color, len(sectors))
        for sector, color in zip(sectors, new_colors):
            sector.set_fill(color)
            sector.set_stroke(width = self.stroke_width)

class Areafunction(VGroup):
    def __init__(self, mob):

        super().__init__()
        text_left = Tex(r"S(")
        text_right = Tex(")")
        self.figure = mob.copy()
        width = self.figure.get_width()
        self.figure.scale(0.5/width).set_style(stroke_width = 2)
        self.figure.move_to(ORIGIN)
        text_left.next_to(self.figure, LEFT, buff = 0.05)
        text_right.next_to(self.figure, RIGHT, buff = 0.05)
        self.text = VGroup(text_left, text_right)
        self.add(text_left, text_right, self.figure)

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
        edge_radius = (6.7/4)*(3+math.sqrt(3))
        arc1 = Arc(radius = edge_radius, angle = PI, start_angle = -PI/2)
        arc1.shift((-UP-2*OMEGA) * edge_radius)
        arc2 = Arc(radius = edge_radius, angle = PI, start_angle = -5*PI/6)
        arc2.shift((UP-OMEGA) * edge_radius)
        arc3 = Arc(radius = edge_radius, angle = PI, start_angle = 5*PI/6)
        arc3.shift((2*UP+OMEGA) * edge_radius)
        arc4 = Arc(radius = edge_radius, angle = PI, start_angle = PI/2)
        arc4.shift((UP+2*OMEGA)*edge_radius)
        arc5 = Arc(radius = edge_radius, angle = PI, start_angle = PI/6)
        arc5.shift((-UP+OMEGA) * edge_radius)
        arc6 = Arc(radius = edge_radius, angle = PI, start_angle = -PI/6)
        arc6.shift((-2*UP-OMEGA) * edge_radius)

        edge = VGroup(arc1, arc2, arc3, arc4, arc5, arc6)

        self.add(snowring2, snowring3, snowring4, snowring5, snowring6, edge)
        self.scale(0.25)

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

###################################################################################################################################################

class Intro0(Scene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("先用起来，再去搭建严格的基础。\n——数学经常如此。", font = 'simsun', t2c={"用起来": GREEN, "基础": BLUE})
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
        notice2 = Notice("高等数学", "请　选修*")
        notice3 = Notice("小学数学", "请　复习")
        notice4 = Notice("视频前言", "请听介绍")
        

        curve1 = lambda x: quadratic(1,0,-2.25,x)
        curve2 = lambda x: x-0.25
        paraarc1 = ParaArc(curve1, np.array([-2.5,2.5,200]), closed = False)
        self.play(ReplacementTransform(notice0, notice1), ShowCreation(paraarc1))
        self.waiting(1,27) #怎么求一条抛物线围成的面积？
        self.play(ApplyWaveUp(paraarc1), run_time = 3)
        self.waiting(1,7) #抛物线越往上开口越大 围成的面积自然是无限
        self.waiting(0,17) #（空闲）

        line1 = Line(np.array([2,1.75,0]), np.array([-1,-1.25,0]), color = YELLOW)
        paraarc2 = ParaArc(curve1, np.array([-1,2,200]), closed = True, color = YELLOW)
        paraarc3 = ParaArc(curve1, np.array([-1,2,200]), closed = True, color = YELLOW, fill_opacity = 1)
        paraarc3.set_color_by_gradient((BLUE, GREEN))
        paraarc3.set_stroke(color = YELLOW)

        self.play(ShowCreation(line1)) 
        self.waiting(0,26) #但如果加一条弦
        self.play(ShowCreation(paraarc2)) 
        self.waiting(0,18) #形成一个弓形
        self.remove(line1)
        self.play(ApplyMethod(paraarc1.set_fill, BLUE, 0)) 
        self.waiting(1,0) #它的面积就是有限的了
        self.waiting(0,27) #（空闲）

        self.play(FadeOut(paraarc1))
        self.waiting(1,11) #这个面积可以怎么求呢

        riemann = RiemannRectangle(curve1, curve2, np.array([-1,2,7]))
        riemann2 = RiemannRectangle(curve1, curve2, np.array([-1,2,14]))
        riemann3 = RiemannRectangle(curve1, curve2, np.array([-1,2,28]))
        frame1 = Rectangle(height=4, width=6)
        frame2 = Rectangle(height=4, width=6)
        frame1.shift(3.5*LEFT)
        frame2.shift(3.5*RIGHT)
        frame_text1 = Text("BV1HA411n77C", font = "Times New Roman")
        frame_text1.scale(0.5)
        frame_text2 = Text("BV1AY41157Hd", font = "Times New Roman")
        frame_text2.scale(0.5)
        frame_text1.next_to(frame1, UP)
        frame_text2.next_to(frame2, UP)
        frame = VGroup(frame1, frame2, frame_text1, frame_text2)
        self.play(FadeIn(riemann), ReplacementTransform(notice1, notice2))
        self.play(FadeOut(riemann),FadeIn(riemann2))
        self.play(FadeOut(riemann2),FadeIn(riemann3))
        self.play(FadeOut(paraarc2), FadeIn(paraarc3), FadeOut(riemann3))
        self.waiting(2+3-5,25+14) 
        self.remove(paraarc3)
        self.play(ShowCreation(frame1), ShowCreation(frame2), FadeIn(frame_text1), FadeIn(frame_text2)) #可能一些观众会立即想到积分 没错 真正要求抛物线弓形的面积
        

        curve3 = lambda x: quadratic(1/3,0,-1.5,x+5)
        curve4 = lambda x: -1.5
        paraarc4 = ParaArc(curve3, np.array([-5,-2,50]), closed = False, color = YELLOW, fill_opacity = 0)
        paraarc5 = ParaArc(curve3, np.array([-5,-2,50]), closed = False, color = YELLOW, stroke_width = 0, fill_opacity = 1)
        segment = 50
        for i in range(segment):
            paraarc5.add_line_to(np.array([-2,-1.5,0])-i*np.array([3/segment,0,0]))
            paraarc5.append_points(np.array([-2,-1.5,0]-i*np.array([3/segment,0,0])))
        paraarc5.close_path()
        paraarc5.set_color_by_gradient((BLUE, GREEN))
        
        x_axis = Arrow(np.array([-5.5,-1.5,0]), np.array([-1.5,-1.5,0]), buff = 0)
        y_axis = Arrow(np.array([-5,-1.7,0]), np.array([-5,1.7,0]), buff = 0)
        graph_left = VGroup(paraarc4, x_axis, y_axis)
        riemann4 = RiemannRectangle(curve3, curve4, np.array([-5,-2,7]))
        riemann5 = RiemannRectangle(curve3, curve4, np.array([-5,-2,14]))
        riemann6 = RiemannRectangle(curve3, curve4, np.array([-5,-2,28]))

        graph_right = ParaArc(curve1, np.array([-2,1,200]), closed = True, color = YELLOW, fill_opacity = 0)
        paratriangle1 = ParaTriangle(curve1, np.array([-2,1]), recurse = 5)
        paratriangles = VGroup(paratriangle1.group_triangles[3], paratriangle1.group_triangles[4])
        graph_right.rotate_about_origin(-PI/2)
        paratriangle1.rotate_about_origin(-PI/2)
        graph_right.shift(0.5*DOWN+3.75*RIGHT)
        paratriangle1.shift(0.5*DOWN+3.75*RIGHT)

        self.play(ShowCreation(graph_left), ShowCreation(graph_right))
        self.wait(0.5)
        self.play(FadeIn(riemann4), FadeIn(paratriangle1.group_triangles[0]))
        self.play(FadeOut(riemann4),FadeIn(riemann5), FadeIn(paratriangle1.group_triangles[1]))
        self.play(FadeOut(riemann5),FadeIn(riemann6), FadeIn(paratriangle1.group_triangles[2]))
        self.play(FadeIn(paraarc5), FadeOut(riemann6), FadeIn(paratriangles))
        self.waiting(1+2+2-6.5,21+13+7+20) #或者要用到积分 或者要用到等比数列求和 和极限总是脱不了关系 （空闲）
        self.play(FadeOut(frame), FadeOut(graph_left), FadeOut(graph_right), FadeOut(paraarc5), FadeOut(paratriangle1))

        circle = Circle(radius = 2, fill_color = BLUE, fill_opacity = 1, stroke_color = WHITE, stroke_width = 2)

        sectorsegment = SectorSegment(12, radius = 2)
        sectorrectangle = SectorRectangle(12, radius = 2)
        bipartitedsectorrectangle = BipartitedSectorRectangle(12, radius = 2)
        sectorrectangle2 = SectorRectangle(24, radius = 2)
        bipartitedsectorrectangle2 = BipartitedSectorRectangle(24, radius = 2)
        sectorrectangle3 = SectorRectangle(48, radius = 2)

        self.play(ShowCreation(circle), ReplacementTransform(notice2, notice3))
        self.play(ShowCreation(sectorsegment), lag_ratio = 0)
        self.remove(circle)
        self.play(Transform(sectorsegment, sectorrectangle))
        self.play(ShowCreation(bipartitedsectorrectangle), lag_ratio = 0)
        self.remove(sectorsegment)
        self.play(Transform(bipartitedsectorrectangle, sectorrectangle2))
        self.play(ShowCreation(bipartitedsectorrectangle2), lag_ratio = 0)
        self.remove(bipartitedsectorrectangle)
        self.play(Transform(bipartitedsectorrectangle2, sectorrectangle3))
        self.waiting(3+3+0-7, 19+12+20) #但是 求圆的面积也需要用到极限 这并不妨碍我们在小学就学习了圆的面积公式

        self.remove(bipartitedsectorrectangle2)
        paraarc6 = ParaArc(curve1, np.array([-2.5,2.5,200]), closed = False, fill_opacity = 0)
        paraarc7 = ParaArc(curve1, np.array([-1,2,200]), closed = True, color = GREEN, height = False, width = False)
        self.play(ShowCreation(paraarc6), ReplacementTransform(notice3, notice4))
        self.play(ShowCreation(paraarc7))
        self.play(FadeOut(paraarc6))
        self.waiting(0,11) #抛物线也是我们从初中就认识的老朋友了

        text_area = Tex('S=wh?')
        text_area.shift(UP+0.5*LEFT)
        self.play(FadeIn(paraarc7.height_line), FadeIn(paraarc7.width_line))
        self.play(Write(text_area), run_time = 1)
        self.waiting(0,20) #它有没有什么初中水平的面积公式呢
        self.waiting(0,15) #（空闲）

        self.remove(paraarc7.all, text_area)

        like = Text("", font = 'vanfont')
        coin = Text("", font = 'vanfont')
        star = Text("", font = 'vanfont')
        like.shift(3*LEFT)
        star.shift(3*RIGHT)
        like.scale(2)
        coin.scale(2)
        star.scale(2)
        sanlian = VGroup(like, coin, star)
        sanlian.set_color("#00A1D6")
        self.play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, np.array([0,0,0])), FadeInFromPoint(star, 3*RIGHT), Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"))
        self.waiting(0,18) #长按点赞一键三连
        self.waiting(1,0) # 我们开始吧
        self.waiting(2,12)
        self.play(FadeOut(notice4), FadeOut(sanlian))
        self.wait(2)
        print(self.get_time())
        
        
        
    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_0(Scene):
    def construct(self):

        ##  Making object
        text1 = Text("第一节　水平宽与铅垂高", font = 'simsun', t2c={"第一节": YELLOW, "　水平": GREEN, "与铅垂": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(Scene):
    def construct(self):

        notice1 = Notice("小学数学", "请　复习")
        notice2 = Notice("初中数学", "请　复习")
        notice3 = Notice("高中数学", "请　选修*")
        notice4 = Notice("太弱小了", "没有力量")
        notice5 = Notice("探索方法", "请　模仿")
        notice6 = Notice("探索成功", "请　鼓掌")
        notice7 = Notice("数学公式", "请记笔记")
        notice8 = Notice("另一证法", "请　拓展")
        notice9 = Notice("证明完毕", "请　鼓掌")


        vertice1_A = np.array([3.5,1.5,0])
        vertice1_B = np.array([1,-1.5,0])
        vertice1_C = np.array([5,-1.5,0])
        vertice1_H = np.array([3.5,-1.5,0])

        triangle1 = Polygon(vertice1_A, vertice1_B, vertice1_C)
        height_line1 = Line(vertice1_A, vertice1_H)
        line1 = Line(vertice1_H + 0.2*UP, vertice1_H + 0.2*UP + 0.2*RIGHT)
        line2 = Line(vertice1_H + 0.2*UP + 0.2*RIGHT, vertice1_H + 0.2*RIGHT)
        height1 = VGroup(height_line1, line1, line2)

        text_base = Tex("a")
        text_base.next_to([3,-1.5,0], DOWN)
        text_height = Tex("h")
        text_height.next_to([3.5,0,0], LEFT)
        text_area = Tex(r"S=\frac{ah}{2}")
        text_area.shift(2.5*UP+3*RIGHT)

        self.play(ShowCreation(triangle1), Write(notice1))
        self.play(ShowCreation(height1))
        self.waiting(0,7) #我们在小学五年级的时候

        self.waiting(0,28) #就学会了用......
        self.play(self.indicate_line(vertice1_B, vertice1_C), FadeIn(text_base), run_time = 20/30) #......底和......
        self.play(self.indicate_line(vertice1_A, vertice1_H), FadeIn(text_height), run_time = 20/30) #......高......
        self.play(FadeIn(text_area))
        self.waiting(0,7) #......求三角形的面积
        self.waiting(0,20) #（空闲）

        coordinate = NumberPlane([-0.5, 5.5, 1], [-0.5, 4.5, 1], faded_line_ratio = 1)
        coordinate.shift(3.5*LEFT)

        vertice2_A = np.array([-3,2,0])
        vertice2_B = np.array([-5,-1,0])
        vertice2_C = np.array([-1,1,0])
        vertice2_H = np.array([-2.2,0.4,0])
        vertice2_D = np.array([-3,0,0])
        vertice2_E = np.array([-1,-1,0])

        triangle2 = Polygon(vertice2_A, vertice2_B, vertice2_C)
        height_line2 = Line(vertice2_A, vertice2_H)
        small_vector_1 = 0.075*LEFT + 0.15*UP
        small_vector_2 = 0.075*UP + 0.15*RIGHT
        line3 = Line(vertice2_H + small_vector_1, vertice2_H + small_vector_1 + small_vector_2)
        line4 = Line(vertice2_H + small_vector_1 + small_vector_2, vertice2_H + small_vector_2)
        height2 = VGroup(height_line2, line3, line4)

        line_vertical = DashedLine(vertice2_A, vertice2_D)
        right_triangle_1 = Polygon(vertice2_A, vertice2_H, vertice2_D, color = BLUE, fill_opacity = 0.5, stroke_width = 0)
        arc1 = Arc(start_angle=np.arctan(1/2), angle=PI/2 - np.arctan(1/2), radius=0.2, arc_center=vertice2_D)
        line_horizontal_1 = DashedLine(vertice2_B, vertice2_E)
        line_horizontal_2 = DashedLine(vertice2_C, vertice2_E)
        right_triangle_2 = Polygon(vertice2_B, vertice2_E, vertice2_C, color = PURPLE, fill_opacity = 0.5, stroke_width = 0)
        arc2 = Arc(start_angle=PI + np.arctan(1/2), angle=PI/2 - np.arctan(1/2), radius=0.2, arc_center=vertice2_C)


        text_A_1 = Tex("A")
        text_A_2 = Tex("(3,4)")
        text_A_2.next_to(text_A_1, RIGHT, buff = 0.1)
        text_A = VGroup(text_A_1, text_A_2)
        text_B_1 = Tex("B")
        text_B_2 = Tex("(1,1)")
        text_B_2.next_to(text_B_1, RIGHT, buff = 0.1)
        text_B = VGroup(text_B_1, text_B_2)
        text_C_1 = Tex("C")
        text_C_2 = Tex("(5,3)")
        text_C_2.next_to(text_C_1, RIGHT, buff = 0.1)
        text_C = VGroup(text_C_1, text_C_2)
        text_D_1 = Tex("D")
        text_D_2 = Tex("(3,2)")
        text_D_2.next_to(text_D_1, RIGHT, buff = 0.1)
        text_D = VGroup(text_D_1, text_D_2)
        text_E_1 = Tex("E")
        text_E_2 = Tex("(5,1)")
        text_E_2.next_to(text_E_1, RIGHT, buff = 0.1)
        text_E = VGroup(text_E_1, text_E_2)
        text_H = Tex("H")
        text_label = VGroup(text_A_1, text_B_1, text_C_1, text_D_1, text_E_1)
        text_cootdinate = VGroup(text_A_2, text_B_2, text_C_2, text_D_2, text_E_2)
        text_cootdinate.shift(0.03*DOWN)
        text_A.next_to(vertice2_A, UP)
        text_B.next_to(vertice2_B, DOWN)
        text_C.next_to(vertice2_C, UP)
        text_H.next_to(vertice2_H, RIGHT)
        text_D.next_to(vertice2_D, DOWN+RIGHT, buff = 0.1)
        text_E.next_to(vertice2_E, DOWN)
        text_H.shift(0.2*DOWN+0.2*LEFT)
        
        self.play(Write(coordinate), FadeOut(text_height), FadeOut(text_base), FadeOut(height1), ReplacementTransform(notice1, notice2), run_time = 1)
        self.play(ReplacementTransform(triangle1, triangle2))
        self.play(FadeIn(text_A), FadeIn(text_B), FadeIn(text_C))
        self.waiting(0,4) #但当我们把三角形放进坐标系里面
        self.waiting(1,0)
        self.play(self.indicate_line(vertice2_A, vertice2_B), self.indicate_line(vertice2_A, vertice2_C), self.indicate_line(vertice2_B, vertice2_C))
        self.waiting(0,21) #三条边如果都不平行于坐标轴
        self.play(ApplyMethod(text_area.fade, 0.8))
        self.waiting(0,27) #这种方法就失灵了
        self.waiting(0,20) #（空闲）

        function_line = Tex(r"BC:\ x-2y+1=0")
        function_line.shift(1.5*UP+3*RIGHT).scale(0.8)
        function_distance = Tex(r"AH = \frac{|3-2\times 4+1|}{\sqrt{1^2+2^2}}=\frac{4}{5}\sqrt5")
        function_distance.shift(0.5*UP+3*RIGHT).scale(0.8)
        function_base = Tex(r"BC = \sqrt{(5-1)^2+(3-1)^2} = 2\sqrt5")
        function_base.scale(0.8).next_to(1.4*UP, RIGHT)
        function_height = Tex(r"AH=?")
        function_height.scale(0.8).next_to(0.5*UP, RIGHT)
        function_vertical = Tex(r"AD=4-2=2")
        function_vertical.scale(0.8).next_to(0.5*UP, RIGHT)
        function_height2 = Tex(r"AH=AD\cdot\sin\angle ADH")
        function_height2.scale(0.8).next_to(0.4*DOWN, RIGHT)
        function_height2_2 = Tex(r"=\frac{4}{5}\sqrt5", color = YELLOW)
        function_height2_2.scale(0.8).next_to(function_height2, buff = 0.1)
        function_sin_1 = Tex(r"\sin\angle ADH = \sin\angle BCE")
        function_sin_1.scale(0.8).next_to(1.3*DOWN, RIGHT)
        function_sin_2 = Tex(r"=\frac{BE}{BC}=\frac{2}{5}\sqrt5")
        function_sin_2.scale(0.8).next_to(function_sin_1, buff = 0.1)
        function_area = Tex(r"S = \frac{1}{2}BC\cdot AH = 4", color = YELLOW)
        function_area.scale(0.8).next_to(2.2*DOWN, RIGHT)
        functions_exploring = VGroup(function_base, function_vertical, function_height2, function_height2_2, function_sin_1, function_sin_2, function_area)

        self.play(Write(function_line), ShowCreation(height2), FadeIn(text_H), ReplacementTransform(notice2, notice3), run_time = 1)
        self.play(Write(function_distance), run_time = 1)
        self.waiting(1,10) #点到直线的距离公式要到高中才会学到
        self.play(FadeOut(function_line), FadeOut(function_distance), ReplacementTransform(notice3, notice4))
        self.waiting(1,3) #而初中只有勾股定理
        self.waiting(0,18+5)
        self.play(Write(function_base), self.indicate_line(vertice2_B, vertice2_C), run_time = 1)
        self.waiting(0,24-5) #只能帮助我们把底算出来
        self.waiting(0,24+5)
        self.play(Write(function_height), self.indicate_line(vertice2_A, vertice2_H), run_time = 1)
        self.waiting(0,18-5) #没办法直接求出高的数值
        self.waiting(0,23) #（空闲）

        self.play(FadeOut(function_height), self.indicate_line(np.array([-3,2.5,0]), np.array([-3,-2.5,0])), ReplacementTransform(notice4, notice5))
        self.play(ShowCreation(line_vertical), FadeIn(text_D_1))
        self.waiting(0,4) #但我们可以取一点巧
        self.play(ApplyMethod(height2.fade), ApplyMethod(text_H.fade))
        self.waiting(1,3) #虽然AH的长度算不了
        self.play(Write(text_D_2), run_time = 1)
        self.play(Write(function_vertical), run_time = 1)
        self.waiting(0,29) #但是AD的长度是可以算的
        self.bring_to_back(coordinate, right_triangle_1)
        self.play(ShowCreation(right_triangle_1))
        self.waiting(1,9) #在直角三角形AHD中
        self.play(self.indicate_line(vertice2_A, vertice2_D), self.indicate_line(vertice2_D, vertice2_H), run_time = 1.5)
        self.play(ShowCreation(arc1), run_time = 0.5)
        self.waiting(1,5) #如果我们还能得到角ADH的正弦值
        self.play(Write(function_height2), run_time = 1)
        self.waiting(1,0) #那么AH就能求了
        self.waiting(0,25) #（空闲）

        self.play(self.indicate_line(vertice2_B, vertice2_E), self.indicate_line(vertice2_C, vertice2_E))
        self.play(ShowCreation(line_horizontal_1), ShowCreation(line_horizontal_2))
        self.play(FadeIn(text_E))
        self.waiting(1,25) #过B和C分别作x轴和y轴的平行线 交于E
        self.waiting(0,22) #（空闲）
        self.play(self.indicate_line(vertice2_A, vertice2_D), self.indicate_line(vertice2_C, vertice2_E))
        self.waiting(0,8) #根据平行
        self.play(Indicate(arc1))
        self.waiting(0,11) #ADH和...
        self.play(ShowCreation(arc2), run_time = 0.5)
        self.waiting(1,15) #......BCE是等角
        self.play(Write(function_sin_1), run_time = 1)
        self.waiting(1,6) #于是ADH的正弦值
        self.bring_to_back(coordinate, right_triangle_2)
        self.play(Write(function_sin_2), ShowCreation(right_triangle_2), run_time = 1)
        self.waiting(0,28) #就是BE比上BC 
        self.waiting(1,2)#（空闲）
        
        self.play(Write(function_height2_2), run_time = 1)
        self.waiting(0,18) #我们通过这种方法
        self.play(Write(function_area), ReplacementTransform(notice5, notice6))
        self.waiting(1,18) #也可以求出三角形的面积

        calculation_area_0 = Tex(r"S")
        calculation_area_0.scale(0.8).next_to(2*UP+RIGHT, LEFT, buff = 0)
        calculation_area_1 = Tex(r"=\frac{1}{2}AH\cdot BC")
        calculation_area_1.scale(0.8).next_to(2*UP+RIGHT, RIGHT, buff = 0.1)
        calculation_area_first_row = VGroup(calculation_area_0, calculation_area_1)
        calculation_area_2 = Tex(r"=\frac{1}{2}AD\cdot \sin\angle ADH\cdot BC")
        calculation_area_2.scale(0.8).next_to(1.1*UP+RIGHT, RIGHT, buff = 0.1)
        calculation_area_3 = Tex(r"=\frac{1}{2}AD\cdot \frac{BE}{BC}\cdot BC")
        calculation_area_3.scale(0.8).next_to(0.2*UP+RIGHT, RIGHT, buff = 0.1)
        calculation_area_4 = Tex(r"=\frac{1}{2}AD\cdot BE")
        calculation_area_4.scale(0.8).next_to(0.7*DOWN+RIGHT, RIGHT, buff = 0.1)
        calculation_area = VGroup(calculation_area_0, calculation_area_1, calculation_area_2, calculation_area_3, calculation_area_4)
        formula_area = Tex(r"S = \frac{1}{2}AD\cdot BE", color = YELLOW)
        formula_area.move_to(2*DOWN+3*RIGHT)


        self.wait(0.5)
        self.play(FadeOut(functions_exploring), FadeOut(text_area))
        self.wait(0.5)
        self.play(Write(calculation_area_first_row))
        self.wait(0.5)
        self.play(FadeIn(calculation_area_2, DOWN))
        self.wait(0.5)
        self.play(FadeIn(calculation_area_3, DOWN))
        self.wait(0.5)
        self.play(FadeIn(calculation_area_4, DOWN))
        self.waiting(3+1+1+2-7.5,17+9+27+8) #而且 如果把得到的式子稍微化简一下 就会发现 不仅AH不用算 连BC都不用算了
        self.play(FadeIn(formula_area, DOWN))
        self.waiting(0,20) #我们得到了一个更简单的公式
        self.play(FadeOut(calculation_area))
        fading_group = VGroup(height2, text_H, right_triangle_1, right_triangle_2, arc1, arc2, text_cootdinate, coordinate)
        anim_A = ApplyMethod(text_A_1.next_to, vertice2_A, UP)
        anim_B = ApplyMethod(text_B_1.next_to, vertice2_B, DOWN)
        anim_C = ApplyMethod(text_C_1.next_to, vertice2_C, UP)
        anim_D = ApplyMethod(text_D_1.next_to, vertice2_D, DOWN)
        anim_E = ApplyMethod(text_E_1.next_to, vertice2_E, DOWN)
        self.bring_to_back(fading_group)
        self.play(ApplyMethod(formula_area.shift, 3*UP), FadeOut(fading_group), anim_A, anim_B, anim_C, anim_D, anim_E)
        anim1 = ShowCreationThenDestructionAround(formula_area)
        anim1.update_config(run_time = 2)
        anim2 = ReplacementTransform(notice6, notice7)
        anim2.update_config(run_time = 1)
        self.play(anim1, anim2)
        self.waiting(0,26) #S等于1/2AD乘BE
        self.waiting(0,22) #（空闲）

        self.waiting(0,16) #这里的......
        self.play(ApplyMethod(line_horizontal_1.set_color, YELLOW), run_time = 0.5)
        self.waiting(0,5) #......BE......
        self.play(ApplyMethod(line_vertical.set_color, YELLOW), run_time = 0.5)
        self.waiting(0,20) #......和AD

        formula_area_text_1 = Text("面积", font = 'simsun', color = GREEN)
        formula_area_text_2 = Tex(r"=\frac{1}{2}")
        formula_area_text_3 = Text("铅垂高", font = 'simsun', color = YELLOW)
        formula_area_text_4 = Tex(r"\times ")
        formula_area_text_5 = Text("水平宽", font = 'simsun', color = YELLOW)
        formula_area_text_2.next_to(formula_area_text_1, RIGHT, buff = 0.1)
        formula_area_text_3.next_to(formula_area_text_2, RIGHT, buff = 0.1)
        formula_area_text_4.next_to(formula_area_text_3, RIGHT, buff = 0.1)
        formula_area_text_5.next_to(formula_area_text_4, RIGHT, buff = 0.1)
        formula_area_text = VGroup(formula_area_text_1, formula_area_text_2, formula_area_text_3, formula_area_text_4, formula_area_text_5)
        formula_area_text.next_to(formula_area, DOWN)
        formula_area_text_frame = VGroup(formula_area_text_1, formula_area_text_2, formula_area_text_4)
        text_width = Tex(r"w", color = YELLOW)
        text_width.next_to(line_horizontal_1, DOWN)
        text_height = Tex(r"h", color = YELLOW)
        text_height.next_to(line_vertical, LEFT, buff = 0.2)
        text_height.shift(0.1*DOWN)
        self.play(FadeIn(formula_area_text_frame), run_time = 0.8)
        self.waiting(0,3) # 一般被叫做......
        self.play(FadeIn(text_width), Write(formula_area_text_5), run_time = 1)
        self.waiting(0,11) # ......水平宽
        self.play(FadeIn(text_height), Write(formula_area_text_3), run_time = 1)
        self.waiting(0,1) # ......和铅垂高
        self.waiting(1,6) #（空闲）

        self.play(ReplacementTransform(notice7, notice8))
        self.waiting(0,1) #它们虽然被称作......
        self.play(Flash(formula_area_text_5[2], flash_radius=0.6, color = WHITE), run_time = 0.5) #......宽和......
        self.play(Flash(formula_area_text_3[2], flash_radius=0.6, color = WHITE), run_time = 0.5)
        self.waiting(0,12) #......高
        self.waiting(1,4) #但实际上
        self.play(WiggleOutThenIn(line_horizontal_1), run_time = 1)
        self.waiting(1,3) #水平宽更像是高
        self.play(WiggleOutThenIn(line_vertical), run_time = 1)
        self.waiting(1,4) #铅垂高更像是底
        self.waiting(0,27) #（空闲）

        triangle_left = Polygon(vertice2_A, vertice2_D, vertice2_B)
        triangle_right = Polygon(vertice2_A, vertice2_D, vertice2_C)
        vertice_left_H = np.array([-3,-1,0])
        height_line_left = Line(vertice2_B, vertice_left_H)
        extended_base_line_left = DashedLine(vertice_left_H, vertice2_D)
        line_left1 = Line(vertice_left_H + 0.2*UP, vertice_left_H + 0.2*UP + 0.2*LEFT)
        line_left2 = Line(vertice_left_H + 0.2*UP + 0.2*LEFT, vertice_left_H + 0.2*LEFT)
        height_left = VGroup(height_line_left, extended_base_line_left, line_left1, line_left2)
        height_left.shift(0.5*LEFT)
        vertice_right_H = np.array([-3,1,0])
        height_line_right = Line(vertice2_C, vertice_right_H)
        line_right1 = Line(vertice_right_H + 0.2*UP, vertice_right_H + 0.2*UP + 0.2*RIGHT)
        line_right2 = Line(vertice_right_H + 0.2*UP + 0.2*RIGHT, vertice_right_H + 0.2*RIGHT)
        height_right = VGroup(height_line_right, line_right1, line_right2)
        height_right.shift(0.5*RIGHT)
        
        self.play(ShowCreation(triangle_left), ShowCreation(triangle_right))
        self.remove(triangle2, line_vertical)
        anim_left = ApplyMethod(triangle_left.shift, 0.5*LEFT)
        anim_right = ApplyMethod(triangle_right.shift, 0.5*RIGHT)
        below = VGroup(line_horizontal_1, line_horizontal_2, text_width)
        target = below.copy().shift(DOWN).fade()
        anim_below = Transform(below, target)
        anim_height = ApplyMethod(text_height.move_to, vertice2_A + DOWN)
        fading_group = VGroup(text_label, formula_area_text, formula_area)
        self.play(anim_left, anim_right, anim_below, anim_height, FadeOut(fading_group))
        self.play(ShowCreation(height_left), ShowCreation(height_right))
        self.waiting(0,14) #如果沿着铅垂高将三角形裁成两半

        height_left_text = Tex(r"w_1")
        height_right_text = Tex(r"w_2")
        height_left_text.next_to(height_line_left, DOWN)
        height_right_text.next_to(height_line_right, DOWN, buff = 0.1)
        height_right_text.shift(0.3*LEFT)
        text_area_left = Tex(r"S_1 = \frac{1}{2}w_1h")
        text_area_right = Tex(r"S_2 = \frac{1}{2}w_2h")
        text_area_left.scale(0.8).next_to(2*UP, RIGHT)
        text_area_right.scale(0.8).next_to(2*UP+3*RIGHT, RIGHT)
        self.play(FadeIn(height_left_text), FadeIn(height_right_text))
        self.play(Write(text_area_left), Write(text_area_right))
        self.waiting(1,8) #就能分别对它们用底乘以高算面积
        self.waiting(0,23) #（空闲）

        line_base_left = Line(vertice2_A+0.5*LEFT, vertice2_D+0.5*LEFT, color = YELLOW)
        line_base_right = Line(vertice2_A+0.5*RIGHT, vertice2_D+0.5*RIGHT, color = YELLOW)
        text_area_sum = Tex(r"S &= S_1+S_2 \\&= \frac{1}{2}w_1h+\frac{1}{2}w_2h\\&=\frac{1}{2}(w_1+w_2)h\\&=\frac{1}{2}wh")
        text_area_sum.scale(0.8).next_to(0.5*DOWN, RIGHT)
        self.play(self.indicate_line(vertice2_A+0.5*LEFT, vertice2_D+0.5*LEFT), self.indicate_line(vertice2_A+0.5*RIGHT, vertice2_D+0.5*RIGHT), FadeIn(line_base_left), FadeIn(line_base_right))
        self.waiting(0,26) #底自然就是铅垂高
        color_changing_group = VGroup(height_line_left, height_line_right, height_left_text, height_right_text)
        anim = ApplyMethod(color_changing_group.set_color, YELLOW)
        self.play(self.indicate_line(vertice2_B+0.5*LEFT, vertice_left_H+0.5*LEFT), self.indicate_line(vertice2_C+0.5*RIGHT, vertice_right_H+0.5*RIGHT), anim, ReplacementTransform(notice8, notice9))
        self.play(Write(text_area_sum))
        self.waiting(2+0-3,29+26) #而两条高加起来 就是水平宽 （空闲）

        fading_group = VGroup(text_area_left, text_area_right, text_area_sum, below, text_height)
        left_group = VGroup(height_left, height_left_text, line_base_left)
        right_group = VGroup(height_right, height_right_text, line_base_right)
        anim_left = ApplyMethod(triangle_left.shift, 0.5*RIGHT)
        anim_right = ApplyMethod(triangle_right.shift, 0.5*LEFT)
        self.play(FadeOut(fading_group), FadeOut(left_group, 0.5*RIGHT), FadeOut(right_group, 0.5*LEFT), anim_left, anim_right)
        self.waiting(0,23) #准备工作已经做好

        curve = lambda x: quadratic(-1/2,-5/2,-1,x)
        paraarc = ParaArc(curve, np.array([-6,1,200]), closed = False, fill_opacity = 0)
        paraarc.scale(1.007)
        self.play(ShowCreation(paraarc))
        self.waiting(1,3) #是时候让抛物线登场了
        self.waiting(3,5)
        self.play(FadeOut(paraarc), FadeOut(triangle_left), FadeOut(triangle_right), FadeOut(notice9))
        self.waiting(3)
        



        print(self.get_time())



    def indicate_line(self, start, end):
        line = Line(start, end)
        target = line.copy()
        line.set_opacity(0)
        target.scale(1.2)
        target.set_color(YELLOW)
        anim = Transform(line, target)
        anim.update_config(rate_func = there_and_back)

        return anim

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_0(Scene):
    def construct(self):

        ##  Making object
        text1 = Text("第二节　抛物线弓形的面积", font = 'simsun', t2c={"第二节": YELLOW, "　抛物线弓": GREEN, "的面": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter2_1(Scene):
    def construct(self):

        notice1 = Notice("生搬硬套", "干就完了")
        notice2 = Notice("生搬失败", "请勿模仿")
        notice3 = Notice("另辟蹊径", "请　模仿")
        notice4 = Notice("撞破南墙", "请　鼓掌")
        notice5 = Notice("生搬硬套", "干就完了")
        notice6 = Notice("硬撞南墙", "请　模仿")
        notice7 = Notice("撞破南墙", "请　鼓掌")
        curve1 = lambda x: quadratic(-1/2,7/2,-4.5,x)
        paraarc1 = ParaArc(curve1, np.array([0.5,6.5,200]), closed = False, fill_opacity = 0, color = WHITE)
        self.play(Write(notice1), ShowCreation(paraarc1))
        self.waiting(0,28) #虽然没有任何的依据
        self.waiting(0,28) #但是

        vertice1_A = np.array([-4,2,0])
        vertice1_B = np.array([-6,-1,0])
        vertice1_C = np.array([-2,1,0])
        vertice1_D = np.array([-4,0,0])
        vertice1_P = np.array([3.5,1.625,0])
        vertice1_Q = np.array([3.5,-0.25,0])

        triangle_1 = Polygon(vertice1_A, vertice1_B, vertice1_C)
        height_triangle_line = Line(vertice1_A, vertice1_D)
        height_triangle_text = Tex(r"h")
        height_triangle_text.next_to(height_triangle_line, RIGHT)
        height_triangle = VGroup(height_triangle_line, height_triangle_text)
        height_triangle.set_color(YELLOW)
        width_triangle = UnderDoubleArrow(triangle_1)
        width_triangle.set_color(YELLOW)
        text_formula = Tex(r"S = \frac{1}{2}wh")
        text_formula.shift(4*LEFT+3*UP)

        self.play(ShowCreation(triangle_1))
        self.play(ShowCreation(height_triangle), ShowCreation(width_triangle))
        self.play(Write(text_formula), run_time = 1)
        self.waiting(0,6) #让我们试试把水平宽和铅垂高的公式

        arrow = Arrow(2*LEFT, ORIGIN)
        paraarc2 = ParaArc(curve1, np.array([1,5,200]), closed = True, color = YELLOW, fill_opacity = 0)
        coordinate = NumberPlane([-0.5, 5.5, 1], [-0.5, 4.5, 1], faded_line_ratio = 1)
        coordinate.shift(3.5*RIGHT+0.5*DOWN)
        guess_formula = Tex(r"S = ?wh").shift(3.5*RIGHT+3*UP)
        
        self.play(FadeIn(arrow, RIGHT), ShowCreation(paraarc2), Write(guess_formula), run_time = 1)
        self.bring_to_back(coordinate)
        self.play(FadeOut(arrow, RIGHT), Write(coordinate), ApplyMethod(paraarc1.fade), run_time= 1)
        self.waiting(0,10) #生搬硬套到抛物线弓形上
        self.waiting(0,22) #（空闲）

        width_paraarc = UnderDoubleArrow(paraarc2, color = YELLOW)
        line_indication_left = Line([1, 2, 0], [1, -3, 0], color = YELLOW)
        line_indication_right = Line([5, 2, 0], [5, -3, 0], color = YELLOW)

        self.play(ShowCreation(width_paraarc))
        self.waiting(0,18) #水平宽好找
        self.play(ShowCreationThenDestruction(line_indication_left), ShowCreationThenDestruction(line_indication_right), run_time = 2)
        self.waiting(1,10) #弦的两个端点就分别是弓形的左右两端
        self.play(WiggleOutThenIn(height_triangle_line))
        self.waiting(0,2) #那铅垂高呢

        dot_triangle = Dot(vertice1_A, color = ORANGE)
        height_indicate_triangle = Line(vertice1_A, vertice1_D, color = ORANGE)
        dot_parabola = Dot(vertice1_P, color = ORANGE)
        height_indicate_parabola = Line(vertice1_P, vertice1_Q, color = ORANGE)
        
        alpha = ValueTracker(0.0)
        def warning_updater(mob):
            a = alpha.get_value()
            if mob == dot_parabola:
                position = vertice1_P
            if mob == height_indicate_parabola:
                position = (vertice1_P+vertice1_Q)/2
            if a < 0.5:
                if a < 0.1:
                    mob.set_color(RED)
                elif a < 0.2:
                    mob.set_color(WHITE)
                elif a < 0.3:
                    mob.set_color(RED)
                elif a < 0.4:
                    mob.set_color(WHITE)
                else:
                    mob.set_color(RED)
                m,n = 4,5
                Lissajous = np.sin(m*TAU*a/0.5) * 0.05 * UP + np.cos(n*TAU*a/0.5) * 0.05 * RIGHT
                mob.move_to(Lissajous + position)
            else:
                mob.set_color(interpolate_color(WHITE, GREY, smooth(2.5*(a-0.6))))
                mob.move_to(position)

        self.play(FadeInFromPoint(dot_triangle, vertice1_A), FadeInFromPoint(dot_parabola, vertice1_P))
        self.play(ShowCreation(height_indicate_triangle), ShowCreation(height_indicate_parabola))
        self.waiting(0,1) #抛物线不像三角形
        
        self.add(alpha)
        self.waiting(0,15)
        dot_parabola.add_updater(warning_updater)
        height_indicate_parabola.add_updater(warning_updater)
        self.play(alpha.animate.set_value(1.0), rate_func = linear)
        self.waiting(1,13) #没有现成的顶点用来作铅垂线
        dot_parabola.remove_updater(warning_updater)
        height_indicate_parabola.remove_updater(warning_updater)

        group_now = VGroup(paraarc1, paraarc2, triangle_1, height_triangle, width_triangle, text_formula, coordinate, width_paraarc, guess_formula)
        group_indicate = VGroup(dot_triangle, height_indicate_triangle, dot_parabola, height_indicate_parabola)

        self.remove(group_now, group_indicate)

        curve2 = lambda x: quadratic(0.25,0,-2.25,x)
        vertice_top = np.array([0,-2.25,0])
        paraarc3 = ParaArc(curve2, np.array([-5,5,200]), closed = False, fill_opacity = 0, color = WHITE)
        paraarc4 = ParaArc(curve2, np.array([-1,2,200]), closed = True, color = YELLOW, fill_opacity = 0.2)
        dot_parabola_2 = Dot(vertice_top, color = ORANGE)
        dot_surrounding_circle = Circle(color = RED, radius = 0.2).move_to(vertice_top)
        self.play(ReplacementTransform(notice1, notice2), ShowCreation(paraarc3))
        self.play(ShowCreation(paraarc4), FadeInFromPoint(dot_parabola_2, vertice_top), ShowCreation(dot_surrounding_circle))
        self.waiting(0,9)   

        start = ValueTracker(-1.0)
        end = ValueTracker(2.0)
        op = ValueTracker(1.0)

        def moving_updater(mob: ParaArc):
            a = start.get_value()+0.001
            b = end.get_value()
            mob.set_range(a, b)

        def inside_updater(mob: Dot):
            a = start.get_value()
            b = end.get_value()
            if a*b <= 0:
                mob.set_color(ORANGE)
            else:
                mob.set_color(GREY)

        def inside_updater_2(mob: Circle):
            a = start.get_value()
            b = end.get_value()
            if a*b <= 0:
                mob.set_color(RED)
            else:
                mob.set_color(GREY)

        def opacity_updater(mob):
            opacity = op.get_value()
            fill = mob.get_fill_opacity()
            mob.set_style(fill_opacity = fill * opacity, stroke_opacity = opacity)

        paraarc4.add_updater(moving_updater)
        dot_parabola_2.add_updater(inside_updater)
        dot_surrounding_circle.add_updater(inside_updater_2)
        self.play(end.animate.set_value(-4.0))
        self.waiting(0,9)
        self.play(start.animate.set_value(4.0), end.animate.set_value(2.0))
        self.waiting(0,9)
        paraarc4.add_updater(opacity_updater)
        dot_parabola_2.add_updater(opacity_updater)
        dot_surrounding_circle.add_updater(opacity_updater)
        paraarc3.add_updater(opacity_updater)
        self.play(start.animate.set_value(-0.5), end.animate.set_value(-4.5), op.animate.set_value(0.0))
        self.waiting(0,9)
        # 甚至很多时候 抛物线连自己的顶点 都不在弓形的范围内 （空闲）
        self.remove(paraarc4, dot_parabola_2, paraarc3, dot_surrounding_circle)

        self.play(ReplacementTransform(notice2, notice3), ShowCreation(triangle_1), ShowCreation(width_triangle))
        self.waiting(0,25) #而从另一个角度想
        height_triangle_line.set_color(GREY)
        self.play(ShowCreation(height_triangle_line))
        self.waiting(0,21) #三角形的铅垂高

        curve2 = lambda x: min(-0.5*x, 1.5*x + 8)
        curve3 = lambda x: 0.5*x + 2
        line_height = Line()
        line_height_text = Tex(r"h", opacity = 0, color = YELLOW).next_to(np.array([-4,1,0]), RIGHT, buff = 0.15)
        alpha = ValueTracker(-6.0)

        def line_updater(l: Line):
            a = alpha.get_value()
            if abs(a + 4) < 0.2:
                l.set_color(YELLOW)
            else:
                l.set_color(WHITE)
            l.put_start_and_end_on(np.array([a, curve2(a),0]), np.array([a, curve3(a),0]))
        line_height.add_updater(line_updater)
        def text_updater(t: Tex):
            a = alpha.get_value()
            if abs(a + 4) < 0.2:
                t.set_opacity(1)
            else:
                t.set_opacity(0)
        line_height_text.add_updater(text_updater)

        self.add(line_height, line_height_text)
        self.play(alpha.animate.set_value(-2.0), run_time = 2)
        self.play(alpha.animate.set_value(-4.0), run_time = 1.5)
        line_height.remove_updater(line_updater)
        line_height_text.remove_updater(text_updater)
        self.waiting(0,9) #是整个三角形在竖直方向上 最宽的宽度
        self.waiting(0,20) #（空闲）

        curve4 = lambda x: 0.5*x - 2
        line_height_parabola = Line()
        alpha = ValueTracker(1.0)
        line_height_parabola_text = Tex(r"h", opacity = 0, color = YELLOW).next_to(np.array([3,0.5,0]), RIGHT, buff = 0.15)

        def line_updater(l: Line):
            a = alpha.get_value()
            if abs(a - 3) < 0.2:
                l.set_color(YELLOW)
            else:
                l.set_color(WHITE)
            l.put_start_and_end_on(np.array([a, curve1(a),0]), np.array([a, curve4(a),0]))
        line_height_parabola.add_updater(line_updater)
        def text_updater(t: Tex):
            a = alpha.get_value()
            if abs(a - 3) < 0.2:
                t.set_opacity(1)
            else:
                t.set_opacity(0)
        line_height_parabola_text.add_updater(text_updater)

        fading_group = VGroup(triangle_1, width_triangle, line_height, height_triangle_line, line_height_text)
        paraarc1.fade(0)

        function_parabola = Tex(r"y = -\frac{1}{2}x^2 + \frac{5}{2}x + 1").scale(0.8).shift(3*UP+2.5*RIGHT)
        self.play(FadeOut(fading_group), Write(coordinate), ShowCreation(paraarc1), FadeIn(function_parabola), run_time = 1)
        self.play(ShowCreation(paraarc2))
        self.add(line_height_parabola, line_height_parabola_text)
        self.play(alpha.animate.set_value(5.0), run_time = 2) #对于抛物线弓形来说 求竖直方向最宽的宽度

        function_height = Tex(r"h(x) = (-\frac{1}{2}x^2 + \frac{5}{2}x + 1) - (\frac{1}{2}x + 1)").scale(0.8)
        function_height.next_to(np.array([-6.5,2.5,0]), RIGHT)
        maximum_height = Tex(r"h = \max\{h(x)\}").scale(0.8).next_to(np.array([-6.5,1.6,0]), RIGHT)

        self.play(alpha.animate.set_value(1.0), Write(function_height), run_time = 2)
        self.play(alpha.animate.set_value(3.0), FadeIn(maximum_height), run_time = 1)
        line_height_parabola.remove_updater(line_updater)
        line_height_parabola_text.remove_updater(text_updater)
        self.waiting(2+0-3, 23+26) #只是相当于求一个二次函数的极值 （空闲）

        vertice_left = np.array([1, -1.5, 0])
        vertice_right = np.array([5, 0.5, 0])
        dot_left = Dot(vertice_left, color = RED)
        dot_right = Dot(vertice_right, color = RED)
        text_veitices = Tex(r"h(0) = h(4) = 0", color = RED).scale(0.8).next_to(np.array([-6.5,0.7,0]), RIGHT)
        self.play(FadeInFromPoint(dot_left, vertice_left), FadeInFromPoint(dot_right, vertice_right), Flash(vertice_left), Flash(vertice_right), Write(text_veitices), ReplacementTransform(notice3, notice4))
        self.waiting(1,6) #由于我们知道两个端点的值

        formula_roots = Tex(r"h(x) = -\frac{1}{2}(x-0)(x-4)").scale(0.8).next_to(np.array([-6.5,-0.2,0]), RIGHT)
        formula_solution = Tex(r"h = h(2) = 2", color = YELLOW).scale(0.8).next_to(np.array([-6.5,-1.1,0]), RIGHT)
        line_delete = Line(np.array([-7,2.5,0]), np.array([0.3, 2.5, 0]), color = RED)
        line_height_parabola_solution = Tex(r"2", color = YELLOW).next_to(np.array([3,0.5,0]), RIGHT, buff = 0.15)
        self.play(Write(formula_roots), ShowCreation(line_delete), run_time = 1)
        self.wait(0.5)
        self.play(Write(formula_solution), Transform(line_height_parabola_text, line_height_parabola_solution), run_time = 1)
        self.waiting(2+1-2.5, 6+10) #直接用交点式就能求出来 （空闲）

        fading_group = VGroup(function_height, maximum_height, text_veitices, formula_roots, formula_solution,line_delete)
        fading_moving_group_above = VGroup(dot_left, dot_right)
        fading_moving_group = VGroup(coordinate, line_height_parabola, line_height_parabola_text)
        function_generalized = Tex(r"y = ax^2+bx+c").scale(0.8).shift(3*UP+3.5*LEFT)
        moving_group = VGroup(paraarc1, paraarc2)
        self.play(FadeOut(fading_group), FadeOut(fading_moving_group, 7*LEFT), FadeOut(function_parabola, 6*LEFT), FadeIn(function_generalized, 6*LEFT), ApplyMethod(moving_group.shift, 7*LEFT), FadeOut(fading_moving_group_above, 7*LEFT))
        self.waiting(0,5) #实际上

        curve5 = lambda x: quadratic(-1/2,-7/2,-4.5,x)
        curve6 = lambda x: 0.5*x + 1.5
        generalized_height_parabola = Line()
        alpha = ValueTracker(-6.0)
        generalized_height_parabola_text = Tex(r"h", opacity = 0, color = YELLOW).next_to(np.array([-4,0.5,0]), RIGHT, buff = 0.15)
        vertice_left_moved = np.array([-6, -1.5, 0])
        vertice_right_moved = np.array([-2, 0.5, 0])
        dot_left_moved = Dot(vertice_left_moved, color = RED)
        dot_right_moved = Dot(vertice_right_moved, color = RED)
        text_left_moved = Tex(r"(x_1,y_1)").next_to(vertice_left_moved, RIGHT+DOWN, buff = 0.1)
        text_right_moved = Tex(r"(x_2,y_2)").next_to(vertice_right_moved, RIGHT+UP, buff = 0.1)
        text_vertices_moved = Tex(r"h(x_1)=h(x_2)=0", color = RED).scale(0.8).next_to(np.array([0,2.5,0]), RIGHT)
        text_formula_moved = Tex(r"h(x) = -|a|(x-x_1)(x-x_2)").scale(0.8).next_to(np.array([0,1.6,0]), RIGHT)

        def line_updater(l: Line):
            a = alpha.get_value()
            if abs(a + 4) < 0.2:
                l.set_color(YELLOW)
            else:
                l.set_color(WHITE)
            l.put_start_and_end_on(np.array([a, curve5(a),0]), np.array([a, curve6(a),0]))
        generalized_height_parabola.add_updater(line_updater)
        def text_updater(t: Tex):
            a = alpha.get_value()
            if abs(a + 4) < 0.2:
                t.set_opacity(1)
            else:
                t.set_opacity(0)
        generalized_height_parabola_text.add_updater(text_updater)

        self.add(generalized_height_parabola, generalized_height_parabola_text)
        anim1 = ApplyMethod(alpha.set_value, -4.0)
        anim1.update_config(rate_func = rush_into)
        anim2 = AnimationGroup(FadeInFromPoint(dot_left_moved, vertice_left_moved), FadeInFromPoint(dot_right_moved, vertice_right_moved), Flash(vertice_left_moved), Flash(vertice_right_moved), FadeIn(text_left_moved), FadeIn(text_right_moved), Write(text_vertices_moved))
        anim2.update_config(run_time = 1)
        self.play(anim1, anim2)
        anim3 = ApplyMethod(alpha.set_value, -2.0)
        anim3.update_config(rate_func = rush_from)
        anim4 = Write(text_formula_moved)
        anim4.update_config(run_time = 1)
        self.play(anim3, anim4)
        self.waiting(0,6) #每个抛物线弓形的铅垂高

        text_formula_moved_height = Tex(r"h = \max\{h(x)\} = \frac{|a|}{4}(x_2-x_1)^2").scale(0.8).next_to(np.array([0,0.7,0]), RIGHT)
        self.play(ApplyMethod(alpha.set_value, -4.0), Write(text_formula_moved_height), run_time = 1)
        text_formula_moved_width = Tex(r"w = x_2-x_1").scale(0.8).next_to(np.array([0,-0.2,0]), RIGHT)
        width_paraarc_moved = UnderDoubleArrow(paraarc2, color = YELLOW).shift(DOWN)
        self.play(Write(text_formula_moved_width), ShowCreation(width_paraarc_moved), run_time = 1)
        self.waiting(0,14) #都会位于弓形的正中间

        text_formula_simplified_height = Tex(r"h = \frac{|a|w^2}{4}", color = YELLOW).move_to(np.array([3,-1,0]))
        self.play(Write(text_formula_simplified_height), run_time = 1)
        self.waiting(1,22) #长度是a/4倍水平宽的平方
        self.waiting(0,15) #（空闲）

        text_formula_area_0 = Tex(r"S", color = GREEN)
        text_formula_area_1 = Tex(r"=k").next_to(text_formula_area_0, RIGHT, buff = 0.15)
        text_formula_area_2 = Tex(r"wh", color = YELLOW).next_to(text_formula_area_1, RIGHT, buff = 0.05)
        text_formula_area = VGroup(text_formula_area_0, text_formula_area_1, text_formula_area_2).move_to(np.array([3,-1,0]))
        text_formula_area_3 = Tex(r"=\frac{|a|}{4}k").next_to(text_formula_area_0, RIGHT, buff = 0.15).shift(DOWN)
        text_formula_area_4 = Tex(r"w^3", color = YELLOW).next_to(text_formula_area_3, buff = 0.05).shift(0.05*UP)
        text_formula_area_second_row = VGroup(text_formula_area_3, text_formula_area_4)
        fading_group = VGroup(text_vertices_moved, text_formula_moved, text_formula_moved_height, text_formula_moved_width)
        paraarc5 = ParaArc(curve5, np.array([-6,-2,200]), closed = True, stroke_width = 0, color = YELLOW)
        self.bring_to_back(paraarc5)
        self.play(FadeOut(fading_group), ApplyMethod(text_formula_simplified_height.shift, 2*UP), FadeIn(text_formula_area_0), FadeIn(text_formula_area_2), ShowCreation(paraarc5), ReplacementTransform(notice4, notice5))
        self.waiting(0,19) #至于面积公式
        frame = SurroundingRectangle(text_formula_area_1, buff = 0)
        self.play(ShowCreationThenDestruction(frame), run_time = 1)
        self.waiting(1,21) #由于现在还不能确定系数是多少
        self.play(FadeIn(text_formula_area_1))
        self.waiting(0,19) #先随便设一个k吧
        self.waiting(0,24) #（空闲）
        frame = SurroundingRectangle(text_formula_simplified_height, color = WHITE)
        self.play(ShowCreationThenDestruction(frame), run_time = 1)
        self.waiting(1,12) #再把铅垂高的公式代进去
        self.play(Write(text_formula_area_second_row), run_time = 1)
        self.waiting(1,18) #就可以得到一个稍微方便一点的
        self.play(Flash(text_formula_area_4, flash_radius = 0.6))
        self.waiting(0,25) #只包含水平宽的公式
        self.waiting(0,27) #（空闲）

        fading_group = VGroup(paraarc1, paraarc2, paraarc5, function_generalized, generalized_height_parabola, generalized_height_parabola_text, dot_left_moved, dot_right_moved, text_left_moved, text_right_moved, width_paraarc_moved)
        fading_moving_group = VGroup(text_formula_simplified_height, text_formula_area_1, text_formula_area_2)

        self.play(FadeOut(fading_group), FadeOut(fading_moving_group, 6*LEFT + 3.5*UP), ApplyMethod(text_formula_area_0.shift, 6*LEFT + 3.5*UP), ApplyMethod(text_formula_area_second_row.shift, 6*LEFT + 4.5*UP), ReplacementTransform(notice5, notice6))
        self.waiting(1,24) #接下来就是求系数的时候了

        coordinate2 = NumberPlane([-1.5, 1.5, 1], [-0.5, 1.5, 1]).scale(2).shift(3*RIGHT+0.5*DOWN)
        curve7 = lambda x: quadratic(-1/2,3,-4,x)
        vertice2_A = np.array([1,-1.5,0])
        vertice2_B = np.array([5,-1.5,0])
        vertice2_P = np.array([3,0.5,0])
        vertice2_Q = np.array([3,-1.5,0])
        paraarc6 = ParaArc(curve7, np.array([3-np.sqrt(6),3+np.sqrt(6),200]), closed = False, stroke_width = 8, fill_opacity = 0, color = WHITE)
        function_simplified = Tex(r"y = -x^2+1").move_to(2*UP+3*RIGHT)

        paraarc7 = ParaArc(curve7, np.array([1,5,200]), closed = True, stroke_width = 8)
        underline_paraarc7 = UnderDoubleArrow(paraarc7, color = ORANGE, text = '2').shift(0.8*DOWN)
        height_line_simplified = Line(vertice2_P, vertice2_Q, color = ORANGE)
        height_text_simplified = Tex(r"1", color = ORANGE).next_to(height_line_simplified, RIGHT, buff = 0.15)
        height_simplified = VGroup(height_line_simplified, height_text_simplified)

        self.play(Write(coordinate2), ShowCreation(paraarc6), Write(function_simplified), run_time = 1)
        self.play(Write(underline_paraarc7), Write(height_simplified))
        self.waiting(0,18) #我们找一根比较好算的抛物线

        triangle_2 = Polygon(vertice2_P, vertice2_A, vertice2_B, stroke_width = 8, fill_opacity = 0.2, color = GREEN)
        self.play(WiggleOutThenIn(height_line_simplified), run_time = 1)
        self.play(ShowCreation(triangle_2))
        self.waiting(1,29) #首先 依照铅垂高做出一个三角形
        line_left = Line(vertice2_P, vertice2_A, stroke_width = 8)
        line_right = Line(vertice2_P, vertice2_B, stroke_width = 8)
        self.bring_to_back(line_left, line_right)
        self.waiting(1,9) #与此同时
        paraarc_left = ParaArc(curve7, np.array([1,3,200]), closed = True, color = YELLOW, stroke_width = 8)
        paraarc_right = ParaArc(curve7, np.array([5,3,200]), closed = True, color = YELLOW, stroke_width = 8)
        self.play(ShowCreation(paraarc_left), ShowCreation(paraarc_right))
        self.waiting(1,27) #抛物线还被划分为了两个较小的弓形
        self.waiting(0,17) #（空闲）

        area_paraarc7 = Areafunction(paraarc7).next_to(np.array([-6.5, 1.5, 0]), RIGHT, buff = 0)
        equation_symbol = Tex(r"=").next_to(area_paraarc7, RIGHT, buff = 0.1)
        area_paraarc_left = Areafunction(paraarc_left).next_to(equation_symbol, RIGHT, buff = 0.1)
        addition_symbol_1 = Tex(r"+").next_to(area_paraarc_left, RIGHT, buff = 0.1)
        area_triangle2 = Areafunction(triangle_2).next_to(addition_symbol_1, RIGHT, buff = 0.1)
        addition_symbol_2 = Tex(r"+").next_to(area_triangle2, RIGHT, buff = 0.1)
        area_paraarc_right = Areafunction(paraarc_right).next_to(addition_symbol_2, RIGHT, buff = 0.1)
        area_equation = VGroup(area_paraarc7, equation_symbol, area_triangle2, addition_symbol_1, area_paraarc_left, addition_symbol_2, area_paraarc_right)
        area_equation_text = VGroup(equation_symbol, area_triangle2.text, addition_symbol_1, area_paraarc_left.text, addition_symbol_2, area_paraarc_right.text)
        self.play(FadeIn(area_paraarc7.text), ShowCreation(paraarc7))
        self.play(Transform(paraarc7, area_paraarc7.figure), FadeIn(area_equation_text))
        self.play(Transform(triangle_2, area_triangle2.figure), Transform(paraarc_left, area_paraarc_left.figure), Transform(paraarc_right, area_paraarc_right.figure))
        area_equation.add(paraarc7, triangle_2, paraarc_left, paraarc_right)
        self.waiting(1+2-3, 13+0) #大弓形的面积 就是这三部分的面积和
        self.waiting(0,18) #（空闲）

        formula_paraarc7 = Tex(r"\frac{k}{4}2^3", color = BLUE).scale(0.8).next_to(area_paraarc7, ORIGIN).shift(DOWN)
        formula_triangle2 = Tex(r"\frac{1\times 2}{2}", color = GREEN).scale(0.8).next_to(area_triangle2, ORIGIN).shift(DOWN)
        formula_paraarc_left = Tex(r"\frac{k}{4}1^3", color = YELLOW).scale(0.8).next_to(paraarc_left, ORIGIN).shift(DOWN)
        formula_paraarc_right = Tex(r"\frac{k}{4}1^3", color = YELLOW).scale(0.8).next_to(paraarc_right, ORIGIN).shift(DOWN)
        formula_symbols = VGroup(equation_symbol, addition_symbol_1, addition_symbol_2).copy().shift(DOWN)
        formula_equation = VGroup(formula_paraarc7, formula_triangle2, formula_paraarc_left, formula_paraarc_right, formula_symbols)
        self.play(FadeIn(formula_symbols), FadeIn(formula_triangle2, DOWN), FadeIn(formula_paraarc7, DOWN))
        self.waiting(1,11) #三角形的面积是已知的

        underline_paraarc_left = UnderDoubleArrow(line_left, color = YELLOW, text = '1')
        underline_paraarc_right = UnderDoubleArrow(line_right, color = YELLOW, text = '1')
        self.play(Write(underline_paraarc_left), Write(underline_paraarc_right))
        self.waiting(1,3) #这两个较小的弓形的水平宽
        self.play(FadeIn(formula_paraarc_left, DOWN), FadeIn(formula_paraarc_right, DOWN))
        self.waiting(1,0) #都是大弓形水平宽的一半
        self.waiting(0,22) #（空闲）

        formula_equation_symbol = equation_symbol.copy().shift(2*DOWN)
        formula_k = Tex(r"\frac{3}{2}k", color = BLUE).scale(0.8).next_to(formula_equation_symbol, LEFT)
        formula_value = Tex(r"1", color = GREEN) .scale(0.8).next_to(formula_equation_symbol, RIGHT)
        formula_simplified = VGroup(formula_equation_symbol, formula_k, formula_value)
        self.play(FadeIn(formula_simplified, DOWN), ReplacementTransform(notice6, notice7))
        self.waiting(0,18) #把公式代进去

        solution_equation_symbol = equation_symbol.copy().shift(3*DOWN)
        solution_k = Tex(r"k").scale(0.8).next_to(solution_equation_symbol, LEFT)
        solution_value = Tex(r"\frac{2}{3}") .scale(0.8).next_to(solution_equation_symbol, RIGHT)
        solution_simplified = VGroup(solution_equation_symbol, solution_k, solution_value)
        self.play(FadeIn(solution_simplified, DOWN))
        self.wait(0.5)
        self.play(ShowCreationThenDestructionAround(solution_simplified))
        self.waiting(2+0-2.5,12+23) #我们就能解出之前设出的系数 （空闲）

        curve8 = lambda x: quadratic(-0.5,0,2,x)
        paraarc8 = ParaArc(curve8, scale_factor = 1.5, x_range = [-2.5,1.5,50], closed = True, height = False, width = False)
        paraarc8.all.shift(2*LEFT)
        text0 = Tex(r"S", r"=", r"\frac{2}{3}", r"hw", r"=", r"\frac{|a|}{6}", r"w^3")
        text0.set_color_by_tex_to_color_map({"S": GREEN, "hw": YELLOW, "w^3": YELLOW})
        text0.shift(3.5*RIGHT)

        fading_group = VGroup(coordinate2, paraarc6, function_simplified, height_simplified, line_left, line_right, underline_paraarc7, underline_paraarc_left, underline_paraarc_right, text_formula_area_0, text_formula_area_second_row)
        fading_moving_group = VGroup(area_equation, formula_equation, formula_simplified)
        self.play(FadeOut(fading_group), FadeOut(fading_moving_group, 8.5*RIGHT), ApplyMethod(solution_simplified.shift, 8.5*RIGHT+3*UP), run_time = 1.5)
        self.play(ShowCreation(paraarc8), ShowCreation(paraarc8.height_line), ShowCreation(paraarc8.width_line), Write(text0))
        self.waiting(0,21) #这样 我们就得到了抛物线弓形的面积公式
        self.waiting(3,0) 
        fading_group = VGroup(paraarc8.all, text0, solution_simplified, notice7)
        self.play(FadeOut(fading_group))
        self.waiting(3,13)

        print(self.get_time())

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_0(Scene):
    def construct(self):

        ##  Making object
        text1 = Text("第三节　真正的面积公式", font = 'simsun', t2c={"第三节": YELLOW, "的面积公": GREEN})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter3_1(Scene):
    def construct(self):

        notice1 = Notice("小心求证", "请　模仿")
        notice2 = Notice("升华主题", "请　泪目")
        curve1 = lambda x: quadratic(-0.5,0,2,x)
        paraarc1 = ParaArc(curve1, scale_factor = 1.5, x_range = [-2.5,1.5,50], closed = True, height = False, width = False)
        paraarc1.all.shift(2*LEFT)
        text1 = Tex(r"S", r"=", r"\frac{2}{3}", r"hw", r"=", r"\frac{|a|}{6}", r"w^3")
        text1.set_color_by_tex_to_color_map({"S": GREEN, "hw": YELLOW, "w^3": YELLOW})
        text1.shift(3.5*RIGHT)
        self.play(Write(notice1), ShowCreation(paraarc1), ShowCreation(paraarc1.height_line), ShowCreation(paraarc1.width_line), Write(text1))
        self.waiting(1,18) #虽然我们好像找到了抛物线弓形的面积公式

        alpha = ValueTracker(0.0)
        def warning_updater(mob):
            a = alpha.get_value()
            position = 3.5*RIGHT
            if a < 0.5:
                if a < 0.1:
                    mob.set_color(RED)
                elif a < 0.2:
                    mob.set_color(WHITE)
                elif a < 0.3:
                    mob.set_color(RED)
                elif a < 0.4:
                    mob.set_color(WHITE)
                else:
                    mob.set_color(RED)
                m,n = 4,5
                Lissajous = np.sin(m*TAU*a/0.5) * 0.05 * UP + np.cos(n*TAU*a/0.5) * 0.05 * RIGHT
                mob.move_to(Lissajous + position)
            else:
                mob.set_color(interpolate_color(WHITE, GREY, smooth(2.5*(a-0.6))))
                mob.move_to(position)

        text1.add_updater(warning_updater)
        self.play(alpha.animate.set_value(1.0), rate_func = linear)
        text1.remove_updater(warning_updater)
        self.waiting(1,10) #但这毕竟是猜出来的
        removing_group = VGroup(paraarc1.all, text1)
        self.remove(removing_group)
        
        frame1 = Rectangle(height=4, width=6)
        frame2 = Rectangle(height=4, width=6)
        frame1.shift(3.5*LEFT)
        frame2.shift(3.5*RIGHT)
        frame_text1 = Text("BV1HA411n77C", font = "Times New Roman")
        frame_text1.scale(0.5)
        frame_text2 = Text("BV1AY41157Hd", font = "Times New Roman")
        frame_text2.scale(0.5)
        frame_text1.next_to(frame1, UP)
        frame_text2.next_to(frame2, UP)
        frame = VGroup(frame1, frame2, frame_text1, frame_text2)

        curve2 = lambda x: quadratic(1/3,0,-1.5,x+5)
        paraarc2 = ParaArc(curve2, np.array([-5,-2,50]), closed = False, color = YELLOW, fill_opacity = 0)
        paraarc3 = ParaArc(curve2, np.array([-5,-2,50]), closed = False, color = YELLOW, stroke_width = 0, fill_opacity = 1)
        segment = 50
        for i in range(segment):
            paraarc3.add_line_to(np.array([-2,-1.5,0])-i*np.array([3/segment,0,0]))
            paraarc3.append_points(np.array([-2,-1.5,0]-i*np.array([3/segment,0,0])))
        paraarc3.close_path()
        paraarc3.set_color_by_gradient((BLUE, GREEN))
        x_axis = Arrow(np.array([-5.5,-1.5,0]), np.array([-1.5,-1.5,0]), buff = 0)
        y_axis = Arrow(np.array([-5,-1.7,0]), np.array([-5,1.7,0]), buff = 0)
        graph_left = VGroup(paraarc2, x_axis, y_axis)

        curve3 = lambda x: quadratic(1,0,-2.25,x)
        graph_right = ParaArc(curve3, np.array([-2,1,200]), closed = True, color = YELLOW, fill_opacity = 0)
        paratriangle1 = ParaTriangle(curve3, np.array([-2,1]), recurse = 5)
        graph_right.rotate_about_origin(-PI/2)
        paratriangle1.rotate_about_origin(-PI/2)
        graph_right.shift(0.5*DOWN+3.75*RIGHT)
        paratriangle1.shift(0.5*DOWN+3.75*RIGHT)

        self.play(ShowCreation(frame1), ShowCreation(frame2), FadeIn(frame_text1), FadeIn(frame_text2))
        self.play(ShowCreation(graph_left), ShowCreation(graph_right))
        self.bring_to_back(paraarc3, paratriangle1)
        self.play(FadeIn(paraarc3), FadeIn(paratriangle1))
        self.waiting(2+1+0-3, 4+16+17) #想要真正证出来这个公式 还是那两种方法 （空闲）
        removing_group = VGroup(frame, graph_left, graph_right, paraarc3, paratriangle1)
        self.remove(removing_group)

        curve4 = lambda x: quadratic(-1/2,-7/2,-4.5,x)
        paraarc4 = ParaArc(curve4, np.array([-6,-2,200]), closed = True, color = YELLOW)
        vertice_left_integral = np.array([-6, -1.5, 0])
        vertice_right_integral = np.array([-2, 0.5, 0])
        dot_left_integral = Dot(vertice_left_integral, color = RED)
        dot_right_integral = Dot(vertice_right_integral, color = RED)
        text_left_integral = Tex(r"(x_1,y_1)").next_to(vertice_left_integral, DOWN)
        text_right_integral = Tex(r"(x_2,y_2)").next_to(vertice_right_integral, DOWN).shift(0.2*RIGHT)
        
        integral_0 = Tex(r"S", color = YELLOW).scale(0.8).next_to(np.array([0,1.53,0]), LEFT, buff = 0)
        integral_1 = Tex(r"=\int_{x_1}^{x_2}-|a|(x-x_1)(x-x_2)\,dx").scale(0.8).next_to(np.array([0,1.5,0]), RIGHT, buff = 0.15)
        integral_2 = Tex(r"=-|a|\left(\frac{1}{3}x^3-\frac{x_1+x_2}{2}x^2+x_1x_2x\right)_{x_1}^{x_2}").scale(0.8).next_to(np.array([0,0.5,0]), RIGHT, buff = 0.15)
        integral_3 = Tex(r"=\frac{|a|}{6}(x_2-x_1)^3").scale(0.8).next_to(np.array([0,-0.5,0]), RIGHT, buff = 0.15)
        integral = VGroup(integral_0, integral_1, integral_2, integral_3)
        self.play(ShowCreation(paraarc4), FadeIn(text_left_integral), FadeIn(text_right_integral), FadeInFromPoint(dot_left_integral, vertice_left_integral), FadeInFromPoint(dot_right_integral, vertice_right_integral), Write(integral_0), run_time = 1)
        self.wait(0.5)
        self.play(Write(integral_1), run_time = 1)
        self.wait(0.5)
        self.play(Write(integral_2), run_time = 1)
        self.wait(0.5)
        self.play(Write(integral_3), run_time = 1)
        self.wait(0.5)
        self.waiting(1+2+3-6, 18+3+2) #一种是积分 把交点式的表达式代进去 就可以直接得到关于水平宽的面积公式
        self.waiting(0,25) #（空闲）
        removing_group = VGroup(integral, paraarc4, dot_left_integral, dot_right_integral, text_left_integral, text_right_integral)
        self.remove(removing_group)

        curve5 = lambda x: quadratic(-1/2,7/2,-3.5,x)
        paraarc5 = ParaArc(curve5, np.array([1,5,200]), closed = True, color = YELLOW, fill_opacity = 0)
        paratriangle2 = ParaTriangle(curve5, np.array([1,5]), recurse = 5)
        line1 = Line(np.array([1,-0.5,0]), np.array([5, -0.5, 0]))
        width0 = UnderDoubleArrow(line1, color = YELLOW)
        width1 = VGroup()
        distance = 2*RIGHT
        for i in range(2):
            line = Line(np.array([1,-0.5,0])+i*distance, np.array([1,-0.5,0])+(i+1)*distance)
            arrow =UnderDoubleArrow(line, color = YELLOW, text = "w/2") 
            width1.add(arrow)
        width1.shift(0.8*DOWN)
        width2 = VGroup()
        distance = 1*RIGHT
        for i in range(4):
            line = Line(np.array([1,-0.5,0])+i*distance, np.array([1,-0.5,0])+(i+1)*distance)
            arrow =UnderDoubleArrow(line, color = YELLOW, text = "w/4") 
            width2.add(arrow)
        width2.shift(1.6*DOWN)
        width3 = VGroup()
        distance = 0.5*RIGHT
        for i in range(8):
            line = Line(np.array([1,-0.5,0])+i*distance, np.array([1,-0.5,0])+(i+1)*distance)
            arrow =UnderDoubleArrow(line, color = YELLOW, text = "") 
            width3.add(arrow)
        width3.shift(2.4*DOWN)
        widths = VGroup(width0, width1, width2, width3)
        geometry_0 = Tex(r"S", color = YELLOW).scale(0.8).next_to(np.array([-6.5, 3, 0]), LEFT, buff = 0)
        geometry_1_0 = Tex(r"=\frac{|a|}{8}w^3").scale(0.8).next_to(np.array([-6.5, 3, 0]), RIGHT, buff = 0.15)
        geometry_1_1 = Tex(r"+2\cdot\frac{|a|}{8}\left(\frac{w}{2}\right)^3").scale(0.8).next_to(geometry_1_0, RIGHT, buff = 0.15)
        geometry_1_2 = Tex(r"+2^2\cdot\frac{|a|}{8}\left(\frac{w}{2^2}\right)^3").scale(0.8).next_to(geometry_1_1, RIGHT, buff = 0.15)
        geometry_1_3 = Tex(r"+2^3\cdot\frac{|a|}{8}\left(\frac{w}{2^3}\right)^3").scale(0.8).next_to(geometry_1_2, RIGHT, buff = 0.15)
        geometry_1_4 = Tex(r"+\cdots").scale(0.8).next_to(geometry_1_3, RIGHT, buff = 0.15)
        geometry_1 = VGroup(geometry_1_0, geometry_1_1, geometry_1_2, geometry_1_3, geometry_1_4)
        geometry_2 = Tex(r"=\frac{|a|w^3}{8}\sum_{n=0}^{\infty}\left(\frac{1}{4}\right)^n").scale(0.8).next_to(np.array([-6.5, 1.8, 0]), RIGHT, buff = 0.15)
        geometry_3 = Tex(r"=\frac{|a|w^3}{6}").scale(0.8).next_to(np.array([-6.5, 0.6, 0]), RIGHT, buff = 0.15)
        geometry = VGroup(geometry_0, geometry_1, geometry_2, geometry_3)
        self.play(ShowCreation(paraarc5), Write(geometry_0))
        self.wait(0.5)
        anim1 = AnimationGroup(FadeIn(width0), FadeIn(paratriangle2.group_triangles[0]), FadeIn(geometry_1_0))
        anim2 = AnimationGroup(FadeIn(width1), FadeIn(paratriangle2.group_triangles[1]), FadeIn(geometry_1_1))
        anim3 = AnimationGroup(FadeIn(width2), FadeIn(paratriangle2.group_triangles[2]), FadeIn(geometry_1_2))
        anim4 = AnimationGroup(FadeIn(width3), FadeIn(paratriangle2.group_triangles[3]), FadeIn(geometry_1_3))
        anim5 = AnimationGroup(FadeIn(paratriangle2.group_triangles[4]), FadeIn(geometry_1_4))
        self.play(anim1, run_time = 0.4)
        self.play(anim2, run_time = 0.4)
        self.play(anim3, run_time = 0.4)
        self.play(anim4, run_time = 0.4)
        self.play(anim5, run_time = 0.4)
        self.wait(0.5)
        self.play(Write(geometry_2), run_time = 1)
        self.wait(0.5)
        self.play(Write(geometry_3), run_time = 1)
        self.wait(0.5)
        self.waiting(2+1+1+1-7, 10+29+28+23) #另一种就像阿基米德一样 通过不断地取三角形 结合等比数列求和 也能得到最终的结果
        self.waiting(0,28) #（空闲）

        removing_group = VGroup(geometry, widths, paraarc5, paratriangle2)
        self.remove(removing_group)

        text_formula_area = Tex(r"S = \frac{|a|}{4}kw^3").shift(3*LEFT + 2.5*UP)
        coordinate2 = NumberPlane([-1.5, 1.5, 1], [-0.5, 1.5, 1]).scale(2).shift(3*RIGHT+0.5*DOWN)
        curve6 = lambda x: quadratic(-1/2,3,-4,x)
        vertice2_A = np.array([1,-1.5,0])
        vertice2_B = np.array([5,-1.5,0])
        vertice2_P = np.array([3,0.5,0])
        vertice2_Q = np.array([3,-1.5,0])

        function_simplified = Tex(r"y = -x^2+1").move_to(2*UP+3*RIGHT)
        paraarc6 = ParaArc(curve6, np.array([3-np.sqrt(6),3+np.sqrt(6),200]), closed = False, stroke_width = 8, fill_opacity = 0, color = WHITE)
        paraarc7 = ParaArc(curve6, np.array([1,5,200]), closed = True, stroke_width = 8)
        underline_paraarc7 = UnderDoubleArrow(paraarc7, color = ORANGE, text = '2').shift(0.8*DOWN)
        height_line_simplified = Line(vertice2_P, vertice2_Q, color = ORANGE)
        height_text_simplified = Tex(r"1", color = ORANGE).next_to(height_line_simplified, RIGHT, buff = 0.15)
        height_simplified = VGroup(height_line_simplified, height_text_simplified)
        triangle_2 = Polygon(vertice2_P, vertice2_A, vertice2_B, stroke_width = 8, fill_opacity = 0.2, color = GREEN)
        line_left = Line(vertice2_P, vertice2_A, stroke_width = 8)
        line_right = Line(vertice2_P, vertice2_B, stroke_width = 8)
        paraarc_left = ParaArc(curve6, np.array([1,3,200]), closed = True, color = YELLOW, stroke_width = 8)
        paraarc_right = ParaArc(curve6, np.array([5,3,200]), closed = True, color = YELLOW, stroke_width = 8)
        underline_paraarc_left = UnderDoubleArrow(line_left, color = YELLOW, text = '1')
        underline_paraarc_right = UnderDoubleArrow(line_right, color = YELLOW, text = '1')
        graph_simplified = VGroup(coordinate2, paraarc6, function_simplified, height_simplified, line_left, line_right, underline_paraarc7, underline_paraarc_left, underline_paraarc_right)
        
        area_paraarc7 = Areafunction(paraarc7).next_to(np.array([-6.5, 1.5, 0]), RIGHT, buff = 0)
        equation_symbol = Tex(r"=").next_to(area_paraarc7, RIGHT, buff = 0.1)
        area_paraarc_left = Areafunction(paraarc_left).next_to(equation_symbol, RIGHT, buff = 0.1)
        addition_symbol_1 = Tex(r"+").next_to(area_paraarc_left, RIGHT, buff = 0.1)
        area_triangle2 = Areafunction(triangle_2).next_to(addition_symbol_1, RIGHT, buff = 0.1)
        addition_symbol_2 = Tex(r"+").next_to(area_triangle2, RIGHT, buff = 0.1)
        area_paraarc_right = Areafunction(paraarc_right).next_to(addition_symbol_2, RIGHT, buff = 0.1)
        area_equation = VGroup(area_paraarc7, equation_symbol, area_triangle2, addition_symbol_1, area_paraarc_left, addition_symbol_2, area_paraarc_right)
        
        formula_paraarc7 = Tex(r"\frac{k}{4}2^3", color = BLUE).scale(0.8).next_to(area_paraarc7, ORIGIN).shift(DOWN)
        formula_triangle2 = Tex(r"\frac{1\times 2}{2}", color = GREEN).scale(0.8).next_to(area_triangle2, ORIGIN).shift(DOWN)
        formula_paraarc_left = Tex(r"\frac{k}{4}1^3", color = YELLOW).scale(0.8).next_to(area_paraarc_left, ORIGIN).shift(DOWN)
        formula_paraarc_right = Tex(r"\frac{k}{4}1^3", color = YELLOW).scale(0.8).next_to(area_paraarc_right, ORIGIN).shift(DOWN)
        formula_symbols = VGroup(equation_symbol, addition_symbol_1, addition_symbol_2).copy().shift(DOWN)
        formula_equation = VGroup(formula_paraarc7, formula_triangle2, formula_paraarc_left, formula_paraarc_right, formula_symbols)
        
        formula_equation_symbol = equation_symbol.copy().shift(2*DOWN)
        formula_k = Tex(r"\frac{3}{2}k", color = BLUE).scale(0.8).next_to(formula_equation_symbol, LEFT)
        formula_value = Tex(r"1", color = GREEN) .scale(0.8).next_to(formula_equation_symbol, RIGHT)
        formula_simplified = VGroup(formula_equation_symbol, formula_k, formula_value)
        
        solution_equation_symbol = equation_symbol.copy().shift(3*DOWN)
        solution_k = Tex(r"k").scale(0.8).next_to(solution_equation_symbol, LEFT)
        solution_value = Tex(r"\frac{2}{3}") .scale(0.8).next_to(solution_equation_symbol, RIGHT)
        solution_simplified = VGroup(solution_equation_symbol, solution_k, solution_value)
        
        fading_group = VGroup(graph_simplified, text_formula_area, area_equation, formula_equation, formula_simplified, solution_simplified)
        
        self.play(FadeIn(fading_group, UP), ReplacementTransform(notice1, notice2))
        self.waiting(0+2+3-1, 28+6+6) #不过 我们能从这个做法中学到的 可能不止是怎么求抛物线弓形的面积这么简单
        self.waiting(0,27) #（空闲）
        self.play(WiggleOutThenIn(area_paraarc7.figure), WiggleOutThenIn(area_paraarc_left.figure), WiggleOutThenIn(area_paraarc_right.figure), run_time = 1.5)
        self.waiting(1.5,7) #抛物线弓形是一种高度自相似的图形
        self.play(ShowCreationThenDestructionAround(area_equation), run_time = 2)
        self.waiting(1+2-2,18+0) #我们使用过的分割 就是对自相似的一种利用
        self.waiting(0,21) #（空闲）

        self.remove(fading_group)

        seperation = Line(np.array([-0.5,4,0]), np.array([-0.5,-3,0]))
        limit_0 = Tex(r"I").scale(0.7).next_to(np.array([-6, 3, 0]), LEFT, buff = 0)
        limit_1 = Tex(r"=\lim_{x\to 0}\frac{\sin x-x}{x^3}").scale(0.7).next_to(np.array([-6, 3, 0]), RIGHT, buff = 0.15)
        limit_2 = Tex(r"=\lim_{t\to 0}\frac{\sin3t-3t}{(3t)^3}").scale(0.7).next_to(np.array([-6, 2.1, 0]), RIGHT, buff = 0.15)
        limit_3 = Tex(r"=\lim_{t\to 0}\frac{3\sin t-4\sin^3t-3t}{27t^3}").scale(0.7).next_to(np.array([-6, 1.2, 0]), RIGHT, buff = 0.15)
        limit_4 = Tex(r"=\lim_{t\to 0}\frac{3\sin t-3t}{27t^3}-\lim_{t\to 0}\frac{4\sin^3t}{27t^3}").scale(0.7).next_to(np.array([-6, 0.3, 0]), RIGHT, buff = 0.15)
        limit_5 = Tex(r"=\frac{1}{9}I-\frac{4}{27}\left(\lim_{t\to 0}\frac{\sin t}{t}\right)^3").scale(0.7).next_to(np.array([-6, -0.6, 0]), RIGHT, buff = 0.15)
        limit_6_l = Tex(r"\frac{8}{9}I").scale(0.7).next_to(np.array([-6, -1.5, 0]), LEFT, buff = 0)
        limit_6_r = Tex(r"= -\frac{4}{27}").scale(0.7).next_to(np.array([-6, -1.5, 0]), RIGHT, buff = 0.15)
        limit_6 = VGroup(limit_6_l, limit_6_r)
        limit_7_l = Tex(r"I").scale(0.7).next_to(np.array([-6, -2.4, 0]), LEFT, buff = 0)
        limit_7_r = Tex(r"= -\frac{1}{6}").scale(0.7).next_to(np.array([-6, -2.4, 0]), RIGHT, buff = 0.15)
        limit_7 = VGroup(limit_7_l, limit_7_r)
        limit_first_row = VGroup(limit_0, limit_1)
        limit = VGroup(limit_0, limit_1, limit_2, limit_3, limit_4, limit_5, limit_6, limit_7)

        small_triangle = Polygon(np.array([3.75,2.95,0]), np.array([3.5,2.2,0]), np.array([4.5,2.2,0]), color = BLUE, fill_opacity = 0.2)
        v_A = np.array([1,3.7,0])
        v_B = np.array([0.5,2.2,0])
        v_C = np.array([2.5,2.2,0])
        big_triangle = Polygon(v_A, v_B, v_C, fill_opacity = 0.2)
        small_triangle_0 = Polygon((v_B+v_C)/2, (v_A+v_C)/2, (v_B+v_A)/2, color = YELLOW, fill_opacity = 0.2)
        small_triangle_A = Polygon(v_A, (v_A+v_C)/2, (v_B+v_A)/2, color = GREEN, fill_opacity = 0.2)
        small_triangle_B = Polygon((v_B+v_C)/2, v_B, (v_B+v_A)/2, color = GREEN, fill_opacity = 0.2)
        small_triangle_C = Polygon((v_B+v_C)/2, (v_A+v_C)/2, v_C, color = GREEN, fill_opacity = 0.2)
        line_A = Line((4*v_A+v_B+v_C)/6, (v_A+v_B+v_C)/3)
        line_B = Line((v_A+4*v_B+v_C)/6, (v_A+v_B+v_C)/3)
        line_C = Line((v_A+v_B+4*v_C)/6, (v_A+v_B+v_C)/3)
        triangles = VGroup(small_triangle, big_triangle, small_triangle_A, small_triangle_B, small_triangle_C, small_triangle_0, line_A, line_B, line_C)

        inertia_small = Tex(r"I_0").scale(0.7).next_to(small_triangle, DOWN)
        interia_big = Tex(r"16I_0").scale(0.7).next_to(big_triangle, DOWN)
        interia_0 = Tex(r"16I_0").scale(0.7).next_to(np.array([0.5,1.2,0]), LEFT, buff = 0)
        interia_1_1 = Tex(r"=I_0").scale(0.7).next_to(np.array([0.5,1.2,0]), RIGHT, buff = 0.15)
        interia_1_2 = Tex(r"+(I_0+md_a^2)").scale(0.7).next_to(interia_1_1, RIGHT, buff = 0.05)
        interia_1_3 = Tex(r"+(I_0+md_b^2)").scale(0.7).next_to(interia_1_2, RIGHT, buff = 0.05)
        interia_1_4 = Tex(r"+(I_0+md_c^2)").scale(0.7).next_to(interia_1_3, RIGHT, buff = 0.05)
        interia_1 = VGroup(interia_1_1, interia_1_2, interia_1_3, interia_1_4)
        interia_2 = Tex(r"=4I_0+m(d_a^2+d_b^2+d_c^2)").scale(0.7).next_to(np.array([0.5,0.3,0]), RIGHT, buff = 0.15)
        interia_3 = Tex(r"=4I_0+m\cdot\frac{1}{4}(a^2+b^2+c^2)").scale(0.7).next_to(np.array([0.5,-0.6,0]), RIGHT, buff = 0.15)
        interia_4_l = Tex(r"12I_0").scale(0.7).next_to(np.array([0.5,-1.5,0]), LEFT, buff = 0)
        interia_4_r = Tex(r"=\frac{1}{3}m(a^2+b^2+c^2)").scale(0.7).next_to(np.array([0.5,-1.5,0]), RIGHT, buff = 0.15)
        interia_4 = VGroup(interia_4_l, interia_4_r)
        interia_5_l = Tex(r"I_0").scale(0.7).next_to(np.array([0.5,-2.4,0]), LEFT, buff = 0)
        interia_5_r = Tex(r"=\frac{1}{36}m(a^2+b^2+c^2)").scale(0.7).next_to(np.array([0.5,-2.4,0]), RIGHT, buff = 0.15)
        interia_5 = VGroup(interia_5_l, interia_5_r)
        interia = VGroup(inertia_small, interia_big, interia_0, interia_1, interia_2, interia_3, interia_4, interia_5)
        
        self.play(ShowCreation(seperation))
        self.play(Write(limit_first_row), run_time = 1)
        self.play(ShowCreation(small_triangle), ShowCreation(big_triangle), run_time = 1)
        self.play(Write(limit_2), Write(inertia_small), Write(interia_big), run_time = 1)
        self.add(interia_0)
        self.wait(0.2)
        self.add(interia_1_1, small_triangle_0)
        self.wait(0.2)
        self.add(interia_1_2, small_triangle_A, line_A)
        self.bring_to_front(small_triangle_0, line_A)
        self.wait(0.2)
        self.add(interia_1_3, small_triangle_B, line_B)
        self.bring_to_front(small_triangle_0, line_A, line_B)
        self.wait(0.2)
        self.add(interia_1_4, small_triangle_C, line_C)
        self.bring_to_front(small_triangle_0, line_A, line_B, line_C)
        self.wait(0.2)
        self.play(Write(limit_3), run_time = 1)
        self.play(Write(interia_2), run_time = 1)
        self.play(Write(limit_4), run_time = 1)
        self.play(Write(interia_3), run_time = 1)
        self.play(Write(limit_5), run_time = 1)
        self.play(Write(interia_4), run_time = 1)
        self.play(Write(limit_6), run_time = 1)
        self.play(Write(interia_5), run_time = 1)
        self.play(Write(limit_7), run_time = 1)
        self.waiting(2+2+2+2+1+0+2+2-14, 9+13+27+3+19+16+15) #类似的对自相似结构的利用 经常出现在各个领域 这使我们往往可以跳过复杂的计算 只需要通过简单的推演 就能得到正确答案 （空闲） 这可能才是我们从这个例子中 能收获的最大启示吧
        self.waiting(3,4)
        fading_group = VGroup(seperation, limit, triangles, interia, notice2)
        self.play(FadeOut(fading_group))
        self.waiting(3,0)
        print(self.get_time())



    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Summary(Scene):
    def construct(self):

        notice1 = Notice("良心视频", "请　三连")
        notice2 = Notice("良心up主", "请　关注")

        self.play(Write(notice1))
        self.waiting(1,2) #非常感谢大家能看到这里
        self.waiting(0,26) #（空闲）

        picture_former_cover = ImageMobject("picture_former_cover.png")
        self.play(FadeIn(picture_former_cover, UP))
        self.waiting(2,6) #上期视频的成绩远远超过我的预期
        self.waiting(2,12) #这离不开大家对我的大力支持
        self.waiting(0,24) #（空闲）

        picture_cover = ImageMobject("picture_cover.png")
        self.play(FadeOut(picture_former_cover, UP), FadeIn(picture_cover, UP))
        self.waiting(1,20) #本期视频的动画效果很复杂
        self.waiting(1,27) #制作难度也非常高
        self.remove(picture_cover)
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
        self.play(ApplyMethod(sanlian1.set_color, "#00A1D6"), Flash(like1, flash_radius=1, color = "#00A1D6"), Flash(coin1, flash_radius=1, color = "#00A1D6"), Flash(star1, flash_radius=1, color = "#00A1D6"))
        self.waiting(1+1-2, 25+1) #还请大家多多三连 （空闲）

        self.remove(sanlian1)
        text_0_1 = Text(r"Winograd", font = "Times New Roman")
        text_0_2 = Text(r"算法", font = 'simsun').next_to(text_0_1)
        text_0 = VGroup(text_0_1, text_0_2).move_to(2*UP)
        text_1 = Tex(r"x*y = f(x,y,\hat{z})").shift(0.5*UP)
        text_2 = Tex(r"z\cdot f(x,y,\hat{z})=f(x,y,z)=x\cdot f(\hat{x},y,z)").shift(0.5*DOWN)
        text_3 = Tex(r"y*z = f(\hat{x},y,z)").shift(1.5*DOWN)
        text = VGroup(text_0, text_1, text_2, text_3)
        self.play(Write(text), run_time = 2)
        self.waiting(1,3) #Winograd算法的视频已经在制作了
        self.waiting(2,25) #它是对偶性的一次非常精巧的运用
        self.waiting(3,11) #我相信 它会为大家留下深刻的印象
        self.waiting(1,7) #（空闲）
        self.remove(text)

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
        self.play(anim1, ReplacementTransform(notice1, notice2))
        self.waiting(0,12) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(1,22) #而我 就像我的名字一样

        self.play(FadeOut(painting_others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star0.shift, DOWN))
        self.waiting(1,9) #想要把天上的星星垂下来

        star_copy = star0.copy()
        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star0, apple))
        self.waiting(1,8) #变成触手可及的果实

        snowflake = SnowFlake()
        star_copy.scale(0.7)
        anim1 = Transform(star0, star_copy)
        anim1.update_config(run_time = 1)
        anim2 = Write(snowflake)
        anim2.update_config(run_time = 2)
        anim3 = Broadcast(ORIGIN)
        anim3.update_config(run_time = 2)
        self.play(anim1, anim2, anim3)
        self.waiting(0,7) #变成指引前路的火光
        self.waiting(0,23) #（空闲）
        

        self.remove(star0, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(0,17) #我是乐正垂星
        self.waiting(2,2) #我们下期视频再见

        self.waiting(5,11)
        self.play(FadeOut(picture_photo), FadeOut(text_name), FadeOut(notice2))
        self.waiting(5)
        
        print(self.get_time())
        


    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)