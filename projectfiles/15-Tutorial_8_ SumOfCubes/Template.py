from manimlib import *
import numpy as np

class Template(Scene):
    def construct(self):

        ##  Making object
        equal = Tex("=", color = RED)
        eq_left01 = Tex(r"1^3+2^3+\cdots+n^3", color = GREEN)
        eq_right01 = Tex(r"(1+2+\cdots+n)^2", color = YELLOW)

        eq_left02 = Tex(r"\sum_{i=1}^n i^3", color = GREEN)
        eq_right02 = Tex(r"\left(\sum_{i=1}^n i\right)^2", color = YELLOW)
        equation02 = VGroup(equal, eq_left02, eq_right02)

        ##  Position
        eq_left01.next_to(equal, LEFT)
        eq_right01.next_to(equal, RIGHT)
        eq_left02.next_to(equal, LEFT)
        eq_right02.next_to(equal, RIGHT)

        ##  Showing object
        self.play(FadeIn(eq_left01), FadeIn(equal), FadeIn(eq_right01))
        self.wait(1)
        self.play(ReplacementTransform(eq_left01, eq_left02))
        self.play(ReplacementTransform(eq_right01, eq_right02))
        self.wait(1)
        self.play(ApplyMethod(equation02.scale, 2.4))
        self.wait(1)