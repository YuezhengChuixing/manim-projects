from manimlib import *
import numpy as np


class Picture(VGroup):

    def __init__(self, address):

        super().__init__()
        ##  Picture reading
        self.image = Image.open(address)
        self.size = self.image.size
        Colors = []
        for i in range (self.size[0]):
            Colors.append([])
            for j in range (self.size[1]):
                pixel = self.image.getpixel((i,j))
                Colors[i].append(rgb_to_color( np.array([pixel[0], pixel[1], pixel[2]])/255 ))
        ##  VGroup Constructing
        self.pixel = []
        self.row = []
        self.pixel_position = []
        for j in range (self.size[1]):
            self.pixel.append([])
            self.pixel_position.append([])
            self.row.append(VGroup())
            for i in range (self.size[0]):
                pixelij = Square(stroke_width = 0, fill_color = Colors[i][j], fill_opacity = 1)
                pixelij.scale(FRAME_HEIGHT /(2*self.size[0]))
                self.pixel_position[j].append(FRAME_HEIGHT*np.array([i+0.5,-j-0.5,0])/self.size[0] + np.array([-FRAME_HEIGHT,FRAME_HEIGHT,0])/2)
                pixelij.shift(self.pixel_position[j][i])
                self.add(pixelij)
                self.row[j].add(pixelij)
                self.pixel[j].append(pixelij)

class Template(Scene):
    def construct(self):

        ##  Making object
        picture = Picture("test9.png")

        group_list = []
        for w in range (int(picture.size[1]/4)):
            groupw = VGroup()
            for j in range(4):
                groupw.add(picture.row[4*w+j])
            group_list.append(groupw)

        #size = np.array([16,16])
        vector1 = np.array([0.5,3,0])
        offset1 = np.array([2,0,0])
        offset2 = np.array([0,-0.5,0])

        ##  Position
        picture.scale(picture.size[0]/64)
        picture.shift(np.array([-4.5,0,0]))

        ##  Showing object
        self.play(FadeIn(picture), lag_ratio = 2/(picture.size[0]*picture.size[1]), run_time = 3)
        self.wait(1)
        if (picture.size[0] == 16):
            for w in range (int(picture.size[1]/4)):
                self.play(WiggleOutThenIn(group_list[w]), lag_ratio = 1/(picture.size[0]*picture.size[1]), run_time = 2)
                self.play(ApplyMethod( group_list[w].move_to, vector1+w*offset1 ), lag_ratio = 1/(picture.size[0]*picture.size[1]), run_time = 0.5)
                self.wait(1)
        if (picture.size[0] == 32):
            for w in range (int(picture.size[1]/4)):
                self.play(WiggleOutThenIn(group_list[w]), lag_ratio = 1/(picture.size[0]*picture.size[1]), run_time = 2)
                self.play(ApplyMethod( group_list[w].move_to, vector1+(w%2)*2*offset1+(w-w%2)*offset2/2 ), lag_ratio = 1/(picture.size[0]*picture.size[1]), run_time = 0.5)
        