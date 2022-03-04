from manimlib import *
import numpy as np

class Template(Scene):
    def construct(self):

        ##  Making object
        UP = np.array([0,1,0])
        DOWN = np.array([0,-1,0])
        LEFT = np.array([-1,0,0])
        RIGHT = np.array([1,0,0])

        circle01 = Circle(color = BLUE)
        circle02 = Circle(color = RED, fill_color = RED, fill_opacity = 1)
        circle02.scale(0.1)

        line01 = Line(LEFT, RIGHT, color = GREEN)
        line02 = Line(UP, DOWN, color = GREEN)

        aim_scope = VGroup(circle01, circle02, line01, line02)

        target_list = []
        for i in range (3):
            for j in range(5):
                target_ij = Circle(color = YELLOW, fill_color = YELLOW, fill_opacity = 0.4)
                target_ij.scale(0.4)
                target_ij.shift(2*(j-2)*RIGHT + 2*(i-1)*UP)
                self.play(FadeIn(target_ij))
                target_list.append(target_ij)

        def shoot_ij(i,j):
            target_ij = target_list[j+i*5]
            self.play(ApplyMethod( aim_scope.next_to, target_ij, 0))
            self.play(ApplyMethod( target_ij.set_fill, GREY), ApplyMethod(target_ij.set_color, GREY))
            self.wait(0.5)
            ij = Text("(%d,%d)" %(i,j), color = GREY)
            ij.next_to(target_ij, DOWN)
            self.play(Write(ij))
            self.wait(1)
            return 0

        ##  Position

        ##  Showing object
        self.wait(1)
        self.add(aim_scope)
        self.play(ApplyMethod(aim_scope.shift, DOWN*3+LEFT*6))
        shoot_ij(0,1)
        shoot_ij(2,0)
        shoot_ij(1,3)
        shoot_ij(0,0)
        shoot_ij(2,4)