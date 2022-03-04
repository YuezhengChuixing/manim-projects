from manimlib import *
import numpy as np
import math

UP = np.array([0, 1, 0])
OMEGA = np.array([math.sqrt(3)/2, -1/2, 0])

class Notice(VGroup):
    def __init__(self, m_text1, m_text2):

        super().__init__()
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

class SnowFlake(VGroup):
    def __init__(self):

        super().__init__()
        snowhex1 = SnowHex(2, 1)
        snowhex2 = SnowHex(6,2)
        snowhex3 = SnowHex(6,3)
        snowhex4 = SnowHex(6,4)
        snowring2 = VGroup(snowhex1)
        snowring3 = SnowRing(3)
        snowring4 = SnowRing(4)
        snowring5 = SnowRing(5)
        snowring6 = VGroup(snowhex2, snowhex3, snowhex4)
        edge_radius = (6.7/4)*(3+math.sqrt(3))
        arc1 = Arc(radius = edge_radius, angle = PI, start_angle = -PI/2)
        arc1.shift((-UP-2*OMEGA) * edge_radius)
        arc2 = Arc(radius = edge_radius, angle = PI, start_angle = -5*PI/6)
        arc2.shift((UP-OMEGA) * edge_radius)
        arc3 = Arc(radius = edge_radius, angle = PI, start_angle = 5*PI/6)
        arc3.shift((2*UP+OMEGA) * edge_radius)
        arc4 = Arc(radius = edge_radius, angle = PI, start_angle = PI/2)
        arc4.shift((UP+2*OMEGA)*edge_radius)
        arc5 = Arc(radius = edge_radius, angle = PI, start_angle = PI/6)
        arc5.shift((-UP+OMEGA) * edge_radius)
        arc6 = Arc(radius = edge_radius, angle = PI, start_angle = -PI/6)
        arc6.shift((-2*UP-OMEGA) * edge_radius)

        edge = VGroup(arc1, arc2, arc3, arc4, arc5, arc6)

        self.add(snowring2, snowring3, snowring4, snowring5, snowring6, edge)
        self.scale(0.25)

class SnowRing(VGroup):
    def __init__(self, radius):

        super().__init__()
        for i in range(radius):
            snowhexi = SnowHex(radius, i)
            self.add(snowhexi)

class SnowHex(VGroup):
    def __init__(self, x_position, omega_position):

        super().__init__()
        x = x_position
        omega = omega_position
        for i in range(6):
            snowi = Snow(x, omega)
            self.add(snowi)
            (x, omega) = (x-omega, x)

class Snow(RegularPolygon):
    def __init__(self, x_position, omega_position):

        super().__init__(n = 6, stroke_width = 2)
        self.scale(0.5)
        self.shift( x_position*UP + omega_position*OMEGA)

class Template(Scene):
    def construct(self):

        notice0 = Notice("良心视频", "请　三连")
        notice1 = Notice("良心up主", "请　关注")
        formula1 = Tex(r"\sum_{i=1}^ny_i\left(\prod_{j\ne i}\frac{x-x_j}{x_i-x_j}\right)", color = BLUE)
        formula2 = Tex(r"=")
        formula3 = Tex(r"\sum_{i=1}^na_iM_i[M_i]_{\bmod m_i}^{-1}", color = GREEN)
        formula1.next_to(formula2, LEFT)
        formula3.next_to(formula2, RIGHT)
        formula = VGroup(formula1, formula2, formula3) 
        
        self.play(Write(notice0))
        self.wait(1.70) #非常感谢大家能看到这里
        self.play(Write(formula), run_time = 1)
        self.wait(2.33) #拉格朗日插值法与中国剩余定理的这种联系

        winograd1_1 = Text("Winograd", font = "Times New Roman")
        winograd1_2 = Text("算法", font = 'simsun')
        winograd1_2.next_to(winograd1_1, RIGHT)
        winograd1 = VGroup(winograd1_1, winograd1_2)
        winograd2 = Tex(r"h = A^T[Gp\odot B^Ts]")
        winograd2.shift(0.5*DOWN)
        winograd1.next_to(winograd2, UP)
        winograd1.shift(1*UP)
        winograd = VGroup(winograd1, winograd2)
        winograd3 = Tex(r"s &= B[Gp\odot Ah]\\ \Leftrightarrow h &= A^T[Gp\odot B^Ts]")
        winograd3.shift(0.5*DOWN)
        winograd4 = Tex(r"\hat{z}\cdot(x*y)\Leftrightarrow \hat{x}\cdot(z*y)")
        winograd4.shift(0.5*DOWN)

        self.play(ReplacementTransform(formula, winograd))
        self.wait(2.48) #是我在学习Winograd算法时注意到的

        frame =  Rectangle(height = 4.5, width = 8, color = WHITE)

        self.play(ShowCreation(frame))
        self.wait(2.98) #Winograd算法是一个可以加速多项式乘法的算法
        self.wait(3.84) #拉格朗日插值法是它得以实现的重要一步

        self.play(Transform(winograd2, winograd3))
        self.wait(1.72) #Winograd算法本身的思路也十分巧妙
        self.play(Transform(winograd2, winograd4))
        self.wait(1.73) #非常能体现形式化思维的特点
        self.wait(2.35) #值得再做一期视频

        self.remove(winograd, frame)
        like = Text("", font = 'vanfont')
        coin = Text("", font = 'vanfont')
        star = Text("", font = 'vanfont')
        share = Text("", font = 'vanfont')
        like1 = like.copy()
        coin1 = coin.copy()
        star1 = star.copy()
        like1.shift(3*LEFT)
        star1.shift(3*RIGHT)
        like1.scale(2)
        coin1.scale(2)
        star1.scale(2)
        sanlian1 = VGroup(like1, coin1, star1)
        self.play(FadeInFromPoint(like1, 3*LEFT), FadeInFromPoint(coin1, np.array([0,0,0])), FadeInFromPoint(star1, 3*RIGHT))
        self.play(ApplyMethod(sanlian1.set_color, "#00A1D6"), Flash(like1, flash_radius=1, color = "#00A1D6"), Flash(coin1, flash_radius=1, color = "#00A1D6"), Flash(star1, flash_radius=1, color = "#00A1D6"))
        self.wait(0.81) #如果这期视频收获了足够多的三连

        self.wait(2.68) #可能下期视频就是Winograd算法
        self.wait(1.77) #（空闲）

        self.remove(sanlian1)
        picture_cover = ImageMobject("picture_cover.png")
        picture_cover.shift(3*LEFT)
        picture_photo = ImageMobject("picture_photo.png", height = 2)
        picture_photo.shift(3*RIGHT+0.5*UP)
        text_name = Text("乐正垂星", font = "simhei")
        text_name.shift(3*RIGHT+DOWN)

        self.play(FadeIn(picture_cover, UP), ReplacementTransform(notice0, notice1))
        self.wait(1.47) #这期视频是我的第一个视频
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.wait(1.82) #这也是我第一次和大家见面

        self.remove(picture_cover, picture_photo, text_name)

        land = Line(np.array([-8,0,0]), np.array([8,0,0]))
        water = Polygon(np.array([-4,0,0]), np.array([-6,0,0]), np.array([-5,-4,0]), np.array([6,-4,0]), fill_color = BLUE_E, fill_opacity = 0.5, stroke_width = 0)
        band1 = Line(np.array([-6,0,0]), np.array([-5,-4,0]), color = BLUE)
        band2 = Line(np.array([-4,0,0]), np.array([6,-4,0]), color = BLUE)
        river = VGroup(water, band1, band2)
        moon = Circle(radius = 1.2, arc_center = np.array([-5,2,0]), fill_color = WHITE, fill_opacity = 0.9, stroke_width = 0)

        star0 = star.copy()
        star0.set_color(BLUE)
        star0.shift(UP)
        star2 = star0.copy()
        star2.shift(1.3*UP-1.7*RIGHT)
        star3 = star0.copy()
        star3.shift(2.2*UP+2.6*RIGHT)
        star4 = star0.copy()
        star4.shift(0.3*UP+2.2*RIGHT)
        star5 = star0.copy()
        star5.shift(-0.2*UP+6.0*RIGHT)
        star5_1 = coin.copy()
        star5_1.set_color(BLUE)
        star5_1.shift(2.7*UP+1.6*RIGHT)
        bigstars = VGroup(star2, star3, star4, star5, star5_1)
        star00 = star0.copy()
        star00.scale(0.7)
        star6 = star00.copy()
        star6.shift(1.4*UP+4.0*RIGHT)
        star7 = star00.copy()
        star7.shift(1.7*UP+0.2*RIGHT)
        star8 = star00.copy()
        star8.shift(0.4*UP+4.3*RIGHT)
        star9 = star00.copy()
        star9.shift(0.1*UP-3.2*RIGHT)
        star10 = star00.copy()
        star10.shift(-0.1*UP-2.5*RIGHT)
        star10_1 = like.copy()
        star10_1.set_color(BLUE)
        star10_1.scale(0.7)
        star10_1.shift(2.5*UP-2.7*RIGHT)
        star10_2 = share.copy()
        star10_2.set_color(BLUE)
        star10_2.scale(0.7)
        star10_2.shift(3.2*UP-0.7*RIGHT)
        smallstars = VGroup(star6, star7, star8, star9, star10, star10_1, star10_2)
        star000 = star0.copy()
        star000.scale(0.4)
        star11 = star000.copy()
        star11.shift(0.5*UP-1.3*RIGHT)
        star12 = star000.copy()
        star12.shift(0.8*UP+0.8*RIGHT)
        star13 = star000.copy()
        star13.shift(-0.2*UP+3.1*RIGHT)
        star14 = star000.copy()
        star14.shift(1.1*UP+2.7*RIGHT)
        star15 = star000.copy()
        star15.shift(1.2*UP-0.5*RIGHT)
        star16 = star000.copy()
        star16.shift(2.2*UP-1.8*RIGHT)
        stardust = VGroup(star11, star12, star13, star14, star15, star16)
        stars = VGroup(bigstars, smallstars, stardust)
        painting = VGroup(river, land, moon, star0, stars)
        painting_others = VGroup(river, land, moon, stars)
        self.play(FadeIn(painting), lag_ratio = 0.01, run_time = 2)
        self.wait(0.17) #知识的星空浩如烟海

        picture_photo.move_to(5*RIGHT+1.3*DOWN)
        text_name.move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.wait(1.63) #而我 就像我的名字一样

        self.play(FadeOut(painting_others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star0.shift, DOWN))
        self.wait(1.44) #想要把天上的星星垂下来

        star_copy = star0.copy()
        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star0, apple))
        self.wait(1.16) #变成触手可及的果实

        snowflake = SnowFlake()
        star_copy.scale(0.7)
        anim1 = Transform(star0, star_copy)
        anim1.update_config(run_time = 1)
        anim2 = Write(snowflake)
        anim2.update_config(run_time = 2)
        anim3 = Broadcast(ORIGIN)
        anim3.update_config(run_time = 2)
        self.play(anim1, anim2, anim3)
        self.wait(0.07) #变成指引前路的火光
        self.wait(0.63) #（空闲）
        

        self.remove(star0, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.wait(0.44) #我是乐正垂星
        self.wait(1.76) #我们下期视频再见
        self.wait(5)
        self.play(FadeOut(picture_photo), FadeOut(text_name), FadeOut(notice1))
        self.wait(1.02)

        print(self.get_time())
        
        """
        ## Making object
        snowflake = SnowFlake()
        circle = Circle(radius = math.sqrt(3)/6, stroke_width = 0, fill_color = BLUE, fill_opacity = 1)
        ##  Position

        ##  Showing object
        self.add(snowflake, circle)
        """