from __future__ import annotations

from manimlib import *
import numpy as np

#################################################################### 

class Template(Scene):
    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)