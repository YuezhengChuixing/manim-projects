from manimlib import *
import numpy as np

class Template(Scene):

    def construct(self):

        background = Rectangle(height = 8, width = 16, stroke_width = 0, fill_color = BLACK, fill_opacity = 1)
        grid = Axes([-1, 4.5, 1], [-1, 3.5, 1], height = 4.5, width = 5.5, stroke_color = WHITE, opacity = 1)
        grid.set_color(WHITE)
        grid.set_opacity(1)
        func_graph = FunctionGraph(self.func_to_graph, color = YELLOW)
        grid.scale(2, about_point = np.array([6,3.5,0]))
        func_graph.scale(2, about_point = np.array([6,3.5,0]))
        dot1 = Dot(np.array([-4,-1.5,0]), radius = 0.15, color = YELLOW)
        dot2 = Dot(np.array([-2,0.5,0]), radius = 0.15, color = YELLOW)
        dot3 = Dot(np.array([0,-1.5,0]), radius = 0.15, color = YELLOW)
        dot4 = Dot(np.array([2,0.5,0]), radius = 0.15, color = YELLOW)
        dots = VGroup(dot1, dot2, dot3, dot4)
        text1 = Text("拉格朗日插值法", font = "simsun", color = BLUE)
        text2 = Text("的", font = "Source Han Sans HW SC")
        text3 = Text("本", font = "Source Han Sans HW SC", color = GREEN)
        text4 = Text("质", font = "Source Han Sans HW SC", color = GREEN)
        text1.shift(2*LEFT+3*UP)
        text1.scale(1.5)
        text2.next_to(text1,RIGHT)
        text2.scale(1.5)
        text3.shift(4.5*RIGHT+1*UP)
        text3.scale(3)
        text4.shift(4.5*RIGHT-1*UP)
        text4.scale(3)
        text = VGroup(text1, text2, text3, text4)
        self.add(background, grid, func_graph, dots, text)
        
        

    def func_to_graph(self,x):
        return 2*x*x*x/3 - 5*x*x + 34*x/3 - 6