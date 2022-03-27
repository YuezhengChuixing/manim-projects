from manimlib import *
import numpy as np

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
        if self.closed:
            self.close_path()

        if self.height is None:
            pass
        elif self.height:
            medium = (x_range[0]+x_range[1])/2
            height_value = abs(curve(medium)-(curve(x_range[0])+curve(x_range[1]))/2)
            height_line = ParaHeight(curve, x_range, "%d"%height_value, color = YELLOW, scale_factor=self.scale_factor)
            self.add(height_line)
        else:
            height_line = ParaHeight(curve, x_range, color = YELLOW, scale_factor=self.scale_factor)
            self.add(height_line)

        if self.width is None:
            pass
        elif self.width:
            width_value = abs(x_range[1]-x_range[0])
            width_line = UnderDoubleArrow(self, "%d"%width_value, color = YELLOW)
            self.add(width_line)
        else:
            width_line = UnderDoubleArrow(self, color = YELLOW)
            self.add(width_line)


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
        

def quadratic(a,b,c,x):
    return a*x*x + b*x + c

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
        colors = color_gradient(self.color, x_range[2])
        for x0, x1,color in zip(xs, xs[1:], colors):
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
            rect = Polygon(np.array([x0,up,0]), np.array([x1,up,0]), np.array([x1,down,0]), np.array([x0,down,0]), fill_color = color,  stroke_color = self.stroke_color, stroke_width = self.stroke_width, fill_opacity = self.fill_opacity)
            rects.append(rect)
        self.add(*rects)

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
        # 和上面黎曼和的实现方法不同，但都规避了边缘线条被遮盖的问题

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
        # 和上面黎曼和的实现方法不同，但都规避了边缘线条被遮盖的问题

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


class Template0(Scene):
    def construct(self):

        ##  Making object
        curve1 = lambda x: quadratic(1,0,-2.25,x)
        curve2 = lambda x: x-0.25
        riemann = RiemannRectangle(curve1, curve2, np.array([-1,2,10]))
        riemann2 = RiemannRectangle(curve1, curve2, np.array([-1,2,20]))
        paraarc1 = ParaArc(curve1, np.array([-1,2,200]), closed = True, color = YELLOW)

        ##  Position

        ##  Showing object
        self.add(paraarc1)
        self.add(riemann)
        self.wait(1)
        self.play(Transform(riemann, riemann2))
        self.wait(1)

class Template1(Scene):
    def construct(self):

        ##  Making object
        #sector = Sector()
        #self.add(sector)
        circle = Circle(radius = 2, fill_color = BLUE, fill_opacity = 1, stroke_color = WHITE, stroke_width = 2)

        sectorsegment = SectorSegment(12, radius = 2)
        sectorrectangle = SectorRectangle(12, radius = 2)
        bipartitedsectorrectangle = BipartitedSectorRectangle(12, radius = 2)
        sectorrectangle2 = SectorRectangle(24, radius = 2)
        bipartitedsectorrectangle2 = BipartitedSectorRectangle(24, radius = 2)
        sectorrectangle3 = SectorRectangle(48, radius = 2)
        self.add(circle)
        self.wait(1)
        self.play(ShowCreation(sectorsegment), lag_ratio = 0, run_time = 2)
        self.remove(circle)
        self.wait(1)
        self.play(Transform(sectorsegment, sectorrectangle), run_time = 2)
        self.play(ShowCreation(bipartitedsectorrectangle), lag_ratio = 0)
        self.remove(sectorsegment)
        self.play(Transform(bipartitedsectorrectangle, sectorrectangle2))
        self.play(ShowCreation(bipartitedsectorrectangle2), lag_ratio = 0)
        self.remove(bipartitedsectorrectangle)
        self.play(Transform(bipartitedsectorrectangle2, sectorrectangle3))
        self.wait(1)

class Template2(Scene):
    def construct(self):

        ##  Making object
        curve1 = lambda x: quadratic(1,0,-2.25,x)
        paraarc = ParaArc(curve1, np.array([-1,2,200]), closed = True, color = YELLOW, fill_opacity = 0)
        paratriangle1 = ParaTriangle(curve1, np.array([-1,2]), recurse = 5)

        self.add(paraarc, paratriangle1)

class Template3(Scene):
    def construct(self):

        ##  Making object
        curve1 = lambda x: quadratic(1,0,-2.25,x)
        paraarc1 = ParaArc(curve1, np.array([-3,3,200]), closed = False, fill_opacity = 0)
        paraarc2 = ParaArc(curve1, np.array([-1,2,200]), closed = True, color = YELLOW, fill_opacity = 0.2)

        start = ValueTracker(-1.0)
        end = ValueTracker(2.0)

        def paraarc2_updater(p: ParaArc):
            a = start.get_value()
            b = end.get_value()
            p.set_range(a, b)

        paraarc2.add_updater(paraarc2_updater)
        self.add(paraarc1, paraarc2)

        self.play(start.animate.set_value(-2.0), run_time = 2)
        self.wait()
        self.play(end.animate.set_value(-1.0), run_time = 2)
        self.wait()

