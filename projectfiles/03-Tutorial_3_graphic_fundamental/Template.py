from manimlib import *
import numpy as np

class Template(Scene):
    def construct(self):

        ##  Making object
        ring = Annulus(inner_radius = .4, outer_radius = 1, color = BLUE)
        center1 = np.array([0, 2, 0])
        square = Square(color = ORANGE, fill_color = RED, fill_opacity = .5)
        center2 = np.array([-1, -2, 0])
        rectangle = Rectangle(height = 3.2, width = 1.2, color = PINK, fill_color = PURPLE, fill_opacity = 0.5)
        center3 = np.array([1, -1.1, 0])
        
        line01 = Line(np.array([0, 3.6, 0]),np.array([0, 2, 0]), color = GREEN)
        line02 = Line(np.array([-1, 2, 0]),np.array([-1, -1, 0]), color = GREEN)
        line03 = Line(np.array([1, 2, 0]),np.array([1, 0.5, 0]), color = GREEN)

        ##  Position
        ring.shift(center1)
        square.shift(center2)
        rectangle.shift(center3)

        ##  Showing object
        self.add(line01)
        self.play(GrowFromCenter(ring))
        self.wait(0.5)
        self.play(FadeIn(line02), FadeIn(line03))
        self.wait(0.5)
        self.play(FadeInFromPoint(square,center2 + np.array([0, -1, 0])))
        self.play(FadeInFromPoint(rectangle,center3 + np.array([0, -1, 0])))
        self.wait(1)