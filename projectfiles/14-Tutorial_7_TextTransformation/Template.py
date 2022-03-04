from manimlib import *
import numpy as np

class Template(Scene):
    def construct(self):

        ##  Making object
        square = Square(side_length = 5, fill_color = BLUE, fill_opacity = 0.5)

        label = Text("扭一下身体", font = 'simsun', color = WHITE)
        label.bg = BackgroundRectangle(label, fill_opacity = 1)
        label_group = VGroup(label.bg, label)

        label2 = Text("加个边框", font = 'simsun', color = BLACK)
        label2.bg = SurroundingRectangle(label2, color = BLUE, fill_color = RED, fill_opacity = 0.5)
        label2_group = VGroup(label2.bg, label2)

        label3 = Text("变成彩虹", font = 'simsun')
        label3.set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)

        ##  Position
        label_group.rotate(TAU/8)
        label2_group.next_to(label_group, DOWN)
        label3.scale(1.8)
        label3.to_edge(DOWN)

        ##  Showing object
        self.add(square)
        self.play(FadeIn(label2_group))
        self.play(FadeIn(label_group))
        self.play(FadeIn(label3))
        self.wait()

        
