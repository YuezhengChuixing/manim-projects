from manimlib import *
import numpy as np

class Template(Scene):
    def construct(self):

        ##  Making object
        quote = Text("使用manim制作数学动画很有意思", font='simsun')
        quote.set_color(RED)
        quote2 = Text("Making animation by manim is funny.")
        quote2.set_color(BLUE)
        author = Text("-鲁迅", color = PINK, font='Source Han Sans')

        ##  Position
        quote.to_edge(UP)
        author.next_to(quote.get_corner(DOWN + RIGHT), DOWN)

        ##  Showing object
        self.add(quote)
        self.add(author)
        self.wait(2)
        self.play(Transform(quote, quote2), 
                  ApplyMethod(author.move_to, quote2.get_corner(DOWN + RIGHT) + DOWN + 2*LEFT))
        
        self.play(ApplyMethod(author.scale, 1.6))
        author.match_color(quote2)
        self.play(FadeOut(quote), FadeOut(author))
        self.wait()