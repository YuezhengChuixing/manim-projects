from manimlib import *

class Hello_Manim(Scene):
    def construct(self):
        
        ##  Making object
        helloworld = Text("Hello world!", color = RED)

        rectangle = Rectangle(color = BLUE)
        rectangle.surround(helloworld)

        group1 = VGroup(helloworld, rectangle)

        hellomanim = Text(r"Hello Manim", color = BLUE)
        hellomanim.scale(2.5)

        ##  Position

        ##  Showing object
        self.play(Write(helloworld))
        self.wait(1)
        self.play(FadeIn(rectangle))
        self.wait(1)
        self.play(ApplyMethod(group1.scale, 2.5))
        self.wait(1)
        self.play(Transform(helloworld, hellomanim))
        self.wait(1)