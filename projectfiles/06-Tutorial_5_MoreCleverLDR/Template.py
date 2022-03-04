from manimlib import *
import numpy as np

class Template(Scene):
    def construct(self):

        ##  Making object
        circle01 = Circle(fill_color=RED, color=RED,fill_opacity=0.5)
        center01 = np.array([-np.sqrt(1/2),np.sqrt(1/2),0])
        circle02 = Circle(fill_color=RED, color=RED,fill_opacity=0.5)
        center02 = np.array([np.sqrt(1/2),np.sqrt(1/2),0])
        square01 = Square(fill_color=RED, color=RED,fill_opacity=0.5)
        love = VGroup(circle01, circle02, square01)
        center_love = np.array([-4,4,0])

        rect01 = Rectangle(height=0.8, width=4,fill_color=RED, color=RED, fill_opacity=0.5)
        rect02 = Rectangle(height=0.8, width=4,fill_color=RED, color=RED, fill_opacity=0.5)
        death = VGroup(rect01, rect02)
        center_death = np.array([0,4,0])

        square02 = Square(fill_color = RED, color = RED, fill_opacity=0.5)
        square02.scale(1.6)
        circle03 = Circle(fill_color = BLACK, color = RED, fill_opacity=0.5)
        circle03.scale(0.45)
        center03 = np.array([-0.72,0.6,0])
        circle04 = Circle(fill_color = BLACK, color = RED, fill_opacity=0.5)
        circle04.scale(0.45)
        center04 = np.array([0.72,0.6,0])

        robots = VGroup(square02,circle03,circle04)
        center_robot = np.array([4,4,0])

        line01 = Line( np.array([-6,-2.4,0]), np.array([6,-2.4,0]), color = RED)
        line01.set_height(0.2)

        text01 = Text("LOVE, DEATH, & ROBOTS", color = RED)
        text01.scale(1.8)
        center_text = np.array([0,-2.5,0])

        graphs = VGroup(love, death, robots)
        center_graphs = np.array([0,-2,0])
        group_all = VGroup(graphs, line01, text01)
        center_all = np.array([0,0.5,0])

        ##  Position
        circle01.shift(center01)
        circle02.shift(center02)
        square01.rotate(np.pi / 4)

        rect01.rotate(np.pi / 4)
        rect02.rotate(-np.pi / 4)

        circle03.shift(center03)
        circle04.shift(center04)

        graphs.shift(center_graphs)

        text01.shift(center_text)
        text01.shift(center_all)

        def function(mob):
            return (mob.shift(center_graphs)).set_opacity(1)


        ##  Showing object
        self.play(ShowCreation(circle01), ShowCreation(circle02), ShowCreation(square01))
        self.wait(0.5)
        self.play(ApplyMethod(love.shift, center_love))
        self.wait(1)

        self.play(ShowCreation(rect01), ShowCreation(rect02))
        self.wait(0.5)
        self.play(ApplyMethod(death.shift, center_death))
        self.wait(1)

        self.play(ShowCreation(square02))
        self.play(ShowCreation(circle03), ShowCreation(circle04))
        self.wait(0.5)
        self.play(ApplyMethod(robots.shift, center_robot))
        self.wait(1)

        self.play(ApplyFunction(function, graphs),ShowCreation(line01))
        self.wait(1)

        self.play(Transform(line01, text01),ApplyMethod(graphs.shift, center_all))
        self.wait(1)
