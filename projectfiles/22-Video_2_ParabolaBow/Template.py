from manimlib import *
import numpy as np
import manimpango
        
def quadratic(a,b,c,x):
    return a*x*x + b*x + c

class Underline(Line):
    CONFIG = {
        "buff": MED_SMALL_BUFF,
    }

    def __init__(self, mobject, **kwargs):
        super().__init__(LEFT, RIGHT, **kwargs)
        self.match_width(mobject)
        self.next_to(mobject, DOWN, buff=self.buff)
        #self.add_tip()
        #self.add_tip(at_start=True)

class UnderArrow(Line):
    CONFIG = {
        "buff": MED_SMALL_BUFF,
    }

    def __init__(self, mobject, **kwargs):
        super().__init__(LEFT, RIGHT, **kwargs)
        self.match_width(mobject)
        self.next_to(mobject, DOWN, buff=self.buff)
        self.add_tip()
        #self.add_tip(at_start=True)

class UnderArrow2(Line):
    CONFIG = {
        "buff": MED_SMALL_BUFF,
    }

    def __init__(self, mobject, **kwargs):
        super().__init__(LEFT, RIGHT, **kwargs)
        self.match_width(mobject)
        self.next_to(mobject, DOWN, buff=self.buff)
        #self.add_tip()
        self.add_tip(at_start=True)

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
        # self.scale(self.scale_factor)

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
        samples = np.array([[x, self.curve(x), 0] for x in np.linspace(self.range[0], self.range[1], 2*int(self.range[2])+1)])
        shift = (samples[0]+samples[2])/2 - samples[1]
        samples[1::2] -= shift
        points = np.zeros((3 * int(self.range[2]), 3))
        points[0::3] = samples[0:-1:2]
        points[1::3] = samples[1::2]
        points[2::3] = samples[2::2]
        points *= self.scale_factor
        self.set_points(points)



class Template(Scene):
    def construct(self):

        ##  Making object
        #axes = NumberPlane()

        curve1 = lambda x: quadratic(-0.5,0,2,x)
        curve2 = lambda x: quadratic(1,11,29,x)
        curve3 = lambda x: quadratic(1,5,7,x)
        curve4 = lambda x: quadratic(0.5,-5,10,x)

        paraarc1 = ParaArc(height = True, width = True)
        paraarc2 = ParaArc(curve1, np.array([-3,1,50]), closed = True, height = False, width = False)
        paraarc3 = ParaArc(curve2, np.array([-6,-5,50]), closed = True)
        paraarc4 = ParaArc(curve3, np.array([-4,-2,50]), closed = True, height = True, width = False)
        paraarc5 = ParaArc(curve4, np.array([3,6,50]), closed = False, height = False)
        paraarcs = VGroup(paraarc1, paraarc2, paraarc3, paraarc4, paraarc5)
        
        paraarc1.shift(3*RIGHT+UP)
        paraarc3.shift(RIGHT+DOWN)
        #underline = UnderDoubleArrow(paraarc2)
        #height = ParaHeight(curve1, np.array([-3,1,50]), color = YELLOW)

        '''
        underline1 = Underline(paraarc2)
        underline2 = UnderArrow(underline1)
        underline3 = UnderArrow2(underline2)
        underline4 = UnderDoubleArrow(underline3)
        underlines = VGroup(underline1, underline2, underline3, underline4)

        curved1 = ArcBetweenPoints(np.array([3,-3,0]), np.array([2,-2,0]))
        curved2 = CurvedArrow(np.array([4,-2,0]), np.array([3,-1,0]))
        curved3 = ArcBetweenPoints(np.array([5,-1,0]), np.array([4,0,0]))
        curved3.add_tip(at_start=True)
        curved4 = ArcBetweenPoints(np.array([6,0,0]), np.array([5,1,0]))
        curved4.add_tip(at_start=True).add_tip()
        curves = VGroup(curved1, curved2, curved3, curved4)
        '''

        self.add(paraarcs)
        self.remove(paraarcs)

        curve5 = lambda x: quadratic(1,0,-2.25,x)
        paraarc6 = ParaArc(curve5, np.array([-2.5,2.5,50]), closed = False)
        paraarc7 = ParaArc(curve5, np.array([-1,2,50]), closed = True, color = YELLOW)
        paraarc8 = ParaArc(curve5, np.array([-2,1,50]), closed = True, color = YELLOW)
        self.play(ShowCreation(paraarc6), ShowCreation(paraarc7))
        self.wait(1)
        self.play(Transform(paraarc7, paraarc8))
        self.wait(1)

class Cover(Scene):

    def construct(self):
        background = Rectangle(height = 8, width = 16, stroke_width = 0, fill_color = BLACK, fill_opacity = 1)
        
        curve1 = lambda x: quadratic(-0.5,0,2,x)
        paraarc = ParaArc(curve1, scale_factor = 1.5, x_range = [-2.5,1.5,50], closed = True, height = False, width = False)
        paraarc.shift(2*LEFT+DOWN)
        text0 = Tex(r"S", r"=", r"\frac{2}{3}", r"hw")
        text0.set_color_by_tex_to_color_map({"S": GREEN, "hw": YELLOW})
        text0.scale(2)
        text0.shift(3.5*RIGHT+DOWN)
        text1 = Text("抛物线弓形", font = "simsun", color = BLUE)
        text2 = Text("的", font = "simsun")
        # text3 = Text("面", font = "FZYaSong-B-GBK", color = GREEN)
        # text4 = Text("积", font = "FZYaSong-B-GBK", color = GREEN)
        # text3 = Text("面", font = "FZXiaoBiaoSong-B05S", color = GREEN)
        # text4 = Text("积", font = "FZXiaoBiaoSong-B05S", color = GREEN)
        text3 = Text("面", font = "Source Han Sans HW SC", color = GREEN)
        text4 = Text("积", font = "Source Han Sans HW SC", color = GREEN)
        # text2.insert_n_curves(1000)
        # text3.insert_n_curves(1000)
        # text4.insert_n_curves(1000)
        text1.shift(3*LEFT+3*UP)
        text1.scale(1.5)
        text2.next_to(text1,RIGHT)
        text2.scale(1.5)
        text3.shift(2.5*RIGHT+2*UP)
        text3.scale(3)
        text4.shift(4.5*RIGHT+2*UP)
        text4.scale(3)
        texts = VGroup(text1, text2, text3, text4)

        self.add(background, paraarc, text0, texts)

