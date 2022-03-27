from manimlib import *
import numpy as np

class Toturial(Scene):
    def construct(self):

        triangle = Triangle().scale(3)
        self.add(triangle)

        dot_p = Dot(color = ORANGE).move_to(triangle.get_vertices()[1])
        alpha = ValueTracker(0.)

        def put_p_on_bottom(p: Dot):
            p.move_to(interpolate(*triangle.get_anchors()[2:4], alpha.get_value()))

        dot_p.add_updater(put_p_on_bottom)

        self.add(dot_p)

        line_height = Line()

        def line_updater(l: Line):
            distance = np.dot(l.get_vector(), triangle.get_vertices()[2] - triangle.get_vertices()[1])
            if abs(distance) < 0.05:
                l.set_color(YELLOW)
            else:
                l.set_color(WHITE)
            l.put_start_and_end_on(triangle.get_start(), dot_p.get_center())

        line_height.add_updater(line_updater)
        self.add(line_height)

        self.play(alpha.animate.set_value(0.5))
        self.wait()
        self.play(alpha.animate.set_value(1.0))
        self.wait()

class Exercise1(Scene):
    def construct(self):

        vertice_A = np.array([-4,-3,0])
        vertice_B = np.array([0,3,0])
        vertice_C = np.array([4,1,0])
        curve1 = lambda x: min(-0.5*x + 3, 1.5*x + 3)
        curve2 = lambda x: 0.5*x - 1
        triangle = Polygon(vertice_A, vertice_B, vertice_C)
        self.add(triangle)

        alpha = ValueTracker(-4.0)
        beta = ValueTracker(0.0)

        line_height = Line()

        def line_updater(l: Line):
            a = alpha.get_value()
            #print(a)
            if abs(a) < 0.05:
                l.set_color(YELLOW)
            else:
                l.set_color(WHITE)
            l.put_start_and_end_on(np.array([a, curve1(a),0]), np.array([a, curve2(a),0]))

        def warning_updater(mob):
            b = beta.get_value()
            print(b)
            if b < 0.05:
                mob.set_color(YELLOW)
            elif b < 0.15:
                mob.set_color(RED)
            elif b < 0.25:
                mob.set_color(WHITE)
            elif b < 0.35:
                mob.set_color(RED)
            elif b < 0.45:
                mob.set_color(WHITE)
            elif b < 0.55:
                mob.set_color(RED)
            elif b < 0.6:
                mob.set_color(WHITE)
            else:
                mob.set_color(interpolate_color(WHITE, GREY, smooth(2.5*(b-0.6))))

        self.add(line_height)

        line_height.add_updater(line_updater)
        self.play(alpha.animate.set_value(4.0), run_time = 3)
        self.play(alpha.animate.set_value(0.0), run_time = 2)
        line_height.remove_updater(line_updater)
        line_height.add_updater(warning_updater)
        self.play(beta.animate.set_value(1.0), run_time = 2, rate_func = linear)
        self.wait()