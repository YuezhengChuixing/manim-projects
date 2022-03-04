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
        all_pixels = Picture("test7.png")

        ##  Position
        all_pixels.scale(0.5)

        #def blow(mob):
        #    new_mob = VGroup()
        #    for j in range(mob.size[1]):
        #        for i in range(mob.size[0]):
        #            new_mob.add(mob.pixel[j][i].move_to(0.75*mob.pixel_position[j][i]))
        #    return new_mob

        ##  Showing object
        self.play(FadeIn(all_pixels), lag_ratio = 2/(all_pixels.size[0]*all_pixels.size[1]), run_time = 3)
        #self.play(ApplyMethod(all_pixels.pixel[3][5].shift, UP+LEFT*2))
        #self.play(ApplyMethod(all_pixels.pixel[3][5].move_to, 0.75*all_pixels.pixel_position[3][5]))
        self.wait(1)

        #play 的内部实现.begin
        animations = []
        for j in range (all_pixels.size[1]):
            for i in range (all_pixels.size[0]):
                anim = prepare_animation( ApplyMethod(all_pixels.pixel[i][j].move_to, 0.75*all_pixels.pixel_position[i][j]) )
                anim.update_config(rate_func=rush_into, run_time = 0.5)
                animations.append(anim)

        # for animation in animations:
        #     animation.update_config()

        self.lock_static_mobject_data(*animations)
        self.begin_animations(animations)
        self.progress_through_animations(animations)
        self.finish_animations(animations)
        self.unlock_mobject_data()
        #play 的内部实现.end

        self.play(WiggleOutThenIn(all_pixels), lag_ratio = 5/(all_pixels.size[0]*all_pixels.size[1]), run_time = 3)
        
        #多动画组合可用AnimationGroup实现.begin
        animations2 = []
        for j in range (all_pixels.size[1]):
            for i in range (all_pixels.size[0]):
                anim = ApplyMethod(all_pixels.pixel[i][j].move_to, 0.5*all_pixels.pixel_position[i][j])
                animations2.append(anim)
        anims = AnimationGroup(*animations2, rate_func=rush_from, run_time = 0.5)
        self.play(anims)
        #多动画组合可用AnimationGroup实现.end
        
        self.wait(1)















        