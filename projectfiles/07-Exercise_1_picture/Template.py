from manimlib import *
import numpy as np

class Template(Scene):
    def construct(self):
        screen_height = 8

        ##  Making object
        image = Image.open("test3.jpg")
        size = image.size
        Colors = []
        for i in range (size[0]):
            Colors.append([])
            for j in range (size[1]):
                pixel = image.getpixel((i,j))
                Colors[i].append(rgb_to_color( np.array([pixel[0], pixel[1], pixel[2]])/255 ))
        ##  Position

        ##  Showing object
        pixels = []
        all_pixels = VGroup()
        for i in range (size[0]):
            pixels.append([])
            for j in range (size[1]):
                pixelij = Square(stroke_width = 0, fill_color = Colors[j][size[0]-i-1], fill_opacity = 1)
                pixelij.scale(screen_height /(2*size[0]))
                pixelij.shift(screen_height*(np.array([j+0.5,i+0.5,0])/size[0]) - np.array([screen_height,screen_height,0])/2 )
                all_pixels.add(pixelij)
                pixels[i].append(pixelij)

        self.play(FadeIn(all_pixels),lag_ratio = 2/(size[0]*size[1]), run_time = 3)














        