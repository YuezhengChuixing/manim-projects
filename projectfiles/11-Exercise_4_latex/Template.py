from manimlib import *
import numpy as np

class Template(Scene):
    def construct(self):

        ##  Making object
        helloworld = Tex(r"Hello world!", color = RED)
        hellomanim = Tex(r"Hello Manim", color = BLUE)
        basel = Tex(r"\sum_{i=1}^{\infty}\frac{1}{i^2}=\frac{\pi^2}{6}", color = GREEN)
        swap_text = ""
        swap_text += r"&\sum_{b=0}^{d-1}\sum_{c=0}^{d-1}(X_2^bZ_2^c)(Z_3^{-c}X_3^{-b})\\"
        swap_text += r"=&\sum_{b=0}^{d-1}\sum_{c=0}^{d-1}\left(\left(\sum_{k=0}^{d-1}|k+b\rangle_2\langle k|\right)\left(\sum_{l=0}^{d-1}\omega^{cl}|l\rangle_2\langle l|\right)\right)"
        swap_text += r"\left(\left(\sum_{l=0}^{d-1}\omega^{-cl}|l\rangle_3\langle l|\right)\left(\sum_{k=0}^{d-1}|k\rangle_3\langle k+b|\right)\right)\\"
        swap_text += r"=&\sum_{b=0}^{d-1}\sum_{c=0}^{d-1}\left(\sum_{k=0}^{d-1}\omega^{ck}|k+b\rangle_2\langle k|\right)\left(\sum_{l=0}^{d-1}\omega^{-cl}|l\rangle_3\langle l+b|\right)\\"
        swap_text += r"=&\sum_{b=0}^{d-1}\sum_{k=0}^{d-1}\sum_{l=0}^{d-1}|k+b\rangle_2\langle k||l\rangle_3\langle l+b|\left(\sum_{c=0}^{d-1}\omega^{c(k-l)}\right)\\"
        swap_text += r"=&\sum_{b=0}^{d-1}\sum_{k=0}^{d-1}\sum_{l=0}^{d-1}|k+b,l\rangle_{23}\langle k,l+b|d\delta_{kl}\\"
        swap_text += r"=&d\sum_{b=0}^{d-1}\sum_{k=0}^{d-1}|k+b,k\rangle_{23}\langle k,k+b|\\"
        swap_text += r"=&d\sum_{k=0}^{d-1}\sum_{l=0}^{d-1}|k,l\rangle_{23}\langle l,k|\\"
        swap_text += r"=&dSWAP_{23}"
        swap = Tex(swap_text, color = YELLOW)
        swap.scale(0.5)

        ##  Position

        ##  Showing object
        self.play(Write(hellomanim))
        self.wait(1)
        self.play(Transform(hellomanim, helloworld))
        self.wait(1)
        self.play(FadeOut(hellomanim))#注意这里Transform的变换不改变名称，所以还是需要对hellomanim作变换
        self.wait(1)
        self.play(Write(basel))
        self.wait(1)
        self.play(Transform(basel, swap))
        self.wait(1)
        # self.play(FadeOut(basel))
