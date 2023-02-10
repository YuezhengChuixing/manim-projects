from manimlib import *
import numpy as np

def unit(angle):
    return np.array([np.cos(angle), np.sin(angle), 0])

def quad(axis: np.ndarray, angle: float):
    vec = unit(angle/2)
    return np.array([axis[0]*vec[1], axis[1]*vec[1], axis[2]*vec[1], vec[0]])

def less_smooth(t: float) -> float:
    # Zero and first derivatives at t=0 and t=1.
    # Equivalent to bezier([0, 0, 1, 1])
    return (t**2) * (3 - 2 * t)

def double_bounce(t: float):
    return 1- abs(bezier([0, 0, 0, 1.6, 1.6, 0.9, 0.9, 1])(t) - 1)

OMEGA = unit(-PI/6)

BACK = "#333333"

###############################################################################

class Notice(VGroup):
    def __init__(self, m_text1, m_text2, **kwargs):

        super().__init__(**kwargs)
        self.line1 = Text(m_text1, font = 'simsun')
        self.line2 = Text(m_text2, font = 'simsun')
        if self.line1.get_height() < 0.5:
            self.line1.scale(1.25)
        if self.line2.get_height() < 0.5:
            self.line2.scale(1.25)
        self.line2.next_to(self.line1, DOWN)
        self.add(self.line1, self.line2)
        self.scale(0.5)
        self.shift(np.array([5.8,2.9,0]))

class SwallowIn(Homotopy):
    CONFIG = {
        "run_time": 2,
        "remover": True
    }

    def __init__(self, mobject, target = None, **kwargs):
        digest_config(self, kwargs, locals())
        if target is None:
            target = mobject.get_center()
        distance = max(
            get_norm(mobject.get_corner(UL)-target), 
            get_norm(mobject.get_corner(UR)-target), 
            get_norm(mobject.get_corner(DL)-target), 
            get_norm(mobject.get_corner(DR)-target),
            )
        
        def homotopy(x, y, z, t):
            position = np.array([x, y, z])
            vect = position - target
            length = get_norm(vect)
            move = t * distance
            if move >= length:
                return target
            else:
                ratio = 1 - move/length
                return target + np.array([ratio * vect[0], np.sqrt(ratio) * vect[1], 0])

        super().__init__(homotopy, mobject, **kwargs)

# This part of code is reformed from 3b1b's

elem_colors = color_gradient([BLUE_B, BLUE_D], 5)
number_color_map = {str(i+1): elem_colors[i] for i in range(5)}

def get_sum_group(set_tex, sum_color=YELLOW):
    height = set_tex.get_height()
    buff = 0.75 * height
    arrow = Vector(height * RIGHT).next_to(set_tex, RIGHT, buff=buff)
    sum_value = MTex(str(set_tex.sum)).set_height(height*2/3).set_color(sum_color).next_to(arrow, RIGHT, buff=buff)

    return VGroup(arrow, sum_value)

def get_subsets(full_set):
    all_subsets = []
    for k in range(len(full_set) + 1):
        all_subsets.extend([get_set_tex(subset) for subset in it.combinations(full_set, k)])
    return VGroup(*[VGroup(set_tex, get_sum_group(set_tex)) for set_tex in all_subsets])

def get_set_tex(values, max_shown=7, **kwargs):
    
    all_length = len(values)
    if all_length > max_shown:
        value_mobs = [
            *[MTex(str(int(value)), tex_to_color_map = number_color_map) for value in values[:max_shown - 2]],
            MTex("\\dots"),
            MTex(str(int(values[-1])), tex_to_color_map = number_color_map),
        ]
    else:
        value_mobs = [MTex(str(int(value)), tex_to_color_map = number_color_map) for value in values]
    shown_length = len(value_mobs)

    commas = MTex(",").replicate(shown_length - 1)
    result = VGroup()
    result.add(MTex("\\{"))
    result.add(*it.chain(*zip(value_mobs, commas)))
    if shown_length > 0:
        result.add(value_mobs[-1].align_to(value_mobs[0], UP))
    result.add(MTex("\\}"))
    result.arrange(RIGHT, buff=SMALL_BUFF)
    if all_length > 0:
        commas.set_y(value_mobs[0].get_y(DOWN))
    if all_length > max_shown:
        result[-4].match_y(commas)
    result.values = values
    result.sum = sum(values)
    result.bits = [i + 1 in values for i in range(5)]
    return result.scale(0.8)
        
# till here

def term_surrounding(mob, buff = 0.05, radius = None):
    return SurroundingRectangle(mob, buff = buff, stroke_width = 2, stroke_color = BLUE).round_corners(radius=radius)

def breath(t: float):
    return bezier([1, 1.5, 1.5, 1.5, 0, 0, 0])(t)

class Swirl(Animation):
    CONFIG = {
        "rotate_func": smooth,
        "rate_func": breath,
        "scale_factor": 0.2,
        "about_point": None,
        "run_time": 2,
        "remover": True
    }

    def interpolate(self, alpha: float) -> None:
        alpha = clip(alpha, 0, 1)
        self.interpolate_mobject(self.rotate_func(alpha), self.rate_func(alpha))
        
    def interpolate_mobject(self, rotate_alpha: float, scale_alpha: float) -> None:
        for sm1, sm2 in self.get_all_families_zipped():
            sm1.set_points(sm2.get_points())
        self.mobject.scale(scale_alpha).rotate(rotate_alpha * TAU)
        
class SnowFlake(VGroup):
    def __init__(self):

        super().__init__()
        snowhex1 = SnowHex(2,1)
        snowhex2 = SnowHex(6,2)
        snowhex3 = SnowHex(6,3)
        snowhex4 = SnowHex(6,4)
        snowring2 = VGroup(snowhex1)
        snowring3 = SnowRing(3)
        snowring4 = SnowRing(4)
        snowring5 = SnowRing(5)
        snowring6 = VGroup(snowhex2, snowhex3, snowhex4)

        outer_radius = 12
        arcs = VGroup()
        arc = ArcBetweenPoints(outer_radius * unit(TAU/12), outer_radius * unit(-TAU/12), angle = PI + PI/12).insert_n_curves(16)
        width = arc.get_width()
        ratio = 2/3
        arc.set_width(width*ratio, stretch = True).shift(width*RIGHT*(1-ratio)/2)
        for i in range (6):
            arc_i = arc.copy().rotate(i*TAU/6, about_point = ORIGIN)
            arcs.add(arc_i)
        
        self.add(snowring2, snowring3, snowring4, snowring5, snowring6, arcs)
        self.scale(0.3)

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

class SpreadOut(Animation):
    # 本部分代码来自一碗星空汤（b站ID：一碗星空咕）
    # 另外感谢不愿意透露姓名的群友（群内ID：嘤）的帮助，虽然他的代码最后没用上（）
    def __init__(self, mobject, **kwargs):
        super().__init__(mobject, **kwargs)

        self.center = mobject.get_center()
        self.radius = get_norm(mobject.get_corner(UL) - self.center)

    def interpolate_submobject(self, submobject, starting_submobject, alpha):
        points = starting_submobject.data["points"] - self.center
        dr = self.radius * alpha

        to_delete = np.where(np.linalg.norm(points[::3], axis = 1) > dr)
        deleted = np.delete(points.reshape((int(points.shape[0]/3), 3, 3)), to_delete, axis = 0) + self.center
        submobject.data["points"] = deleted.reshape(deleted.shape[0]*3, 3)

###############################################################################

class Intro0(Scene):
    def construct(self):

        ##  Making object
        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        quote = Text("就像每次看到π的时候，\n总能找到一条通往圆的路一样，\n有母函数的地方，一定有分配律。", font = 'simsun', t2c={("看到π", "通往圆的路"): GREEN, ("母函数", "分配律"): BLUE})
        author = Text("-Walski Schölder", color = YELLOW, font = "Times New Roman")
        author.next_to(quote.get_corner(DR), DL)
        ##  Showing object
        self.play(Write(quote), runtime = 2)
        self.play(Write(author), Write(notice0))
        self.wait(2)
        self.play(FadeOut(quote), FadeOut(author))
        self.wait(1)

class Intro1(Scene):
    def construct(self):

        notice0 = Notice("沃茨基·硕德", "请勿模仿")
        notice1 = Notice("视频前言", "请听介绍")
        notice2 = Notice("奇妙操作", "请　疑惑")
        notice3 = Notice("照猫画虎", "请　模仿")
        notice4 = Notice("视频前言", "请听介绍")
        notice5 = Notice("传统艺能", "请　三连")

        texts = "求集合", "$\{1, 2, 3, 4, 5\}$", "元素和为8的子集的个数"
        problem = MTexText("".join(texts), isolate = texts, tex_to_color_map = number_color_map).scale(0.8).shift(UP)
        theset = problem.get_part_by_tex(texts[1])
        others = VGroup(*(problem.get_part_by_tex(texts[0]).split()), *(problem.get_part_by_tex(texts[2]).split()))
        numbers = [problem.get_part_by_tex(str(i+1)) for i in range (5)]
        self.play(ReplacementTransform(notice0, notice1), Write(theset))
        self.waiting(0, 4) #给你一个集合
        for i in range (5):
            self.play(Indicate(numbers[i]), run_time = 0.5)
            self.waiting(0, 5)
        self.waiting(0, 23) #{1, 2, 3, 4, 5}
        self.play(Write(others), run_time = 2)
        self.waiting(1, 28) #它有多少个子集 里面所有的元素和为8？
        self.waiting(0, 15) #（空闲）

        self.play(problem.animate.shift(2*UP))
        self.waiting(1, 7) #这道题再简单不过了
        
        first = Text("最大元素", color = YELLOW, font = "simhei").scale(0.8).shift(2*UP + 3*LEFT)
        first_numbers = [MTex(str(5-i)).scale(0.8).shift(3*LEFT + (i*0.8 - 1.2)*DOWN).save_state() for i in range(5)]

        self.play(Write(first), FadeIn(VGroup(*first_numbers), 0.5*DOWN, lag_ratio = 0.3), rate_func = less_smooth)

        deny = Text("（不可能）", color = RED, font = "simhei").scale(0.7)
        deny_3 = deny.copy().next_to(first_numbers[2]).save_state()
        deny_2 = deny.copy().next_to(first_numbers[3]).save_state()
        deny_1 = deny.copy().next_to(first_numbers[4]).save_state()
        alpha = ValueTracker(0.0)
        def deny_updater(delay: float):
            def util(mob: VMobject):
                value = alpha.get_value()
                if value <= 0.4 + delay:
                    ratio = inverse_interpolate(delay, 0.4 + delay, clip(value, delay, 0.4 + delay))
                    mob.restore().shift((1-ratio)*0.5*RIGHT).set_opacity(ratio)
                else:
                    ratio = inverse_interpolate(0.4 + delay, 0.8 + delay, clip(value, 0.4 + delay, 0.8 + delay))
                    mob.restore().set_color(GREY).shift(ratio*0.5*LEFT).set_opacity(1-ratio)
            return util
        def number_updater(delay: float):
            def util(mob: VMobject):
                value = alpha.get_value()
                if value >= 0.4 + delay:
                    ratio = inverse_interpolate(0.4 + delay, 0.8 + delay, clip(value, 0.4 + delay, 0.8 + delay))
                    mob.restore().set_color(GREY).shift(ratio*0.5*LEFT).set_opacity(1-ratio)
            return util
        deny_3.add_updater(deny_updater(0))
        deny_2.add_updater(deny_updater(0.1))
        deny_1.add_updater(deny_updater(0.2))
        first_numbers[2].add_updater(number_updater(0))
        first_numbers[3].add_updater(number_updater(0.1))
        first_numbers[4].add_updater(number_updater(0.2))
        self.add(deny_3, deny_2, deny_1).play(alpha.animate.set_value(1.0), rate_func = less_smooth)
        self.remove(first_numbers[2], first_numbers[3], first_numbers[4], deny_3, deny_2, deny_1)

        alpha = ValueTracker(0.0)
        def line_updater(mob: VMobject):
            value = alpha.get_value()
            start = value * (4*LEFT + 0.9*DOWN) + (1-value) * (3*LEFT + 0.8*UP)
            end = value * (RIGHT + 0.9*DOWN) + (1-value) * (3*LEFT + 0.8*UP)
            dash = DashedLine(start, end)
            mob.set_submobjects(dash.submobjects).set_opacity(value)
        line = Line(3*LEFT + 0.8*UP, 3*LEFT + 0.8*UP)
        line.add_updater(line_updater)
        self.add(line).play(first_numbers[0].animate.move_to(0.5*UP + 3*LEFT), first_numbers[1].animate.move_to(1.95*DOWN + 3*LEFT), alpha.animate.set_value(1.0))
        line.clear_updaters()

        second = Text("次大元素", color = YELLOW, font = "simhei").scale(0.8).shift(2*UP)
        second_numbers_5 = [MTex(str(4-i)).scale(0.7).shift((i*0.6 - 1.4)*DOWN).save_state() for i in range(4)]
        second_numbers_4 = [MTex(str(3-i)).scale(0.7).shift((i*0.6 + 1.35)*DOWN).save_state() for i in range(3)]
        self.add(second, *second_numbers_5, *second_numbers_4)
        self.play(Write(second), FadeIn(VGroup(*second_numbers_5), 0.4*DOWN, lag_ratio = 0.3), FadeIn(VGroup(*second_numbers_4), 0.4*DOWN, lag_ratio = 0.3), rate_func = less_smooth)
        
        deny.scale(0.75)
        alpha = ValueTracker(0.0)
        deny_5_4 = deny.copy().next_to(second_numbers_5[0], buff = 0.2).save_state().add_updater(deny_updater(0))
        deny_5_1 = deny.copy().next_to(second_numbers_5[3], buff = 0.2).save_state().add_updater(deny_updater(1/15))
        deny_4_2 = deny.copy().next_to(second_numbers_4[1], buff = 0.2).save_state().add_updater(deny_updater(2/15))
        deny_4_1 = deny.copy().next_to(second_numbers_4[2], buff = 0.2).save_state().add_updater(deny_updater(0.2))
        second_numbers_5[0].add_updater(number_updater(0))
        second_numbers_5[3].add_updater(number_updater(1/15))
        second_numbers_4[1].add_updater(number_updater(2/15))
        second_numbers_4[2].add_updater(number_updater(0.2))
        self.add(deny_5_4, deny_5_1, deny_4_2, deny_4_1).play(alpha.animate.set_value(1), rate_func = less_smooth)

        subset_1 = MTex("\{5, 3\}").scale(0.8).next_to(0.8*UP + 2*RIGHT)
        subset_2 = MTex("\{5, 2, 1\}").scale(0.8).next_to(0.2*UP + 2*RIGHT)
        subset_3 = MTex("\{4, 3, 1\}").scale(0.8).next_to(1.35*DOWN + 2*RIGHT)
        self.play(Write(subset_1), Write(subset_2), Write(subset_3))
        self.waiting(3+4-6, 2+7) #通过从大到小枚举子集中的元素 我们可以轻松地找到全部3个元素和为8的子集
        self.waiting(0, 19) #（空闲）

        self.play(ReplacementTransform(notice1, notice2), *[FadeOut(mob) for mob in [first, second, first_numbers[0], first_numbers[1], line, second_numbers_5[1], second_numbers_5[2], second_numbers_4[0], subset_1, subset_2, subset_3]])
        self.waiting(1, 18) #但这道题还有另一种解法

        subsets = get_subsets(list(range(1, 6)))
        subsets.submobjects.sort(key = lambda subset: subset[0].sum)

        max_sum = max(subset[0].sum for subset in subsets)
        stacks = VGroup()
        for n in range(max_sum + 1):
            stack = VGroup(*filter(
                lambda ssg: ssg[0].sum == n,
                subsets
            )).arrange(DOWN, aligned_edge = RIGHT, buff = 0.1)
            stacks.add(stack)

        stacks.arrange_in_grid(4, 5, buff = 0.5, aligned_edge = RIGHT)
        stacks[10:15].set_y(np.mean([stacks[5].get_y(DOWN), stacks[15].get_y(UP)]))
        stacks.set_height(3.5).next_to(3*DOWN, UP, buff = 0.1).set_opacity(1)

        rects = VGroup(*[SurroundingRectangle(stack, buff = 0.1, stroke_width = 1, stroke_color = GREY_B).round_corners(radius=0.05) for stack in stacks])

        factored_terms = "(1 + x^{1})", "(1 + x^{2})", "(1 + x^{3})", "(1 + x^{4})", "(1 + x^{5})"
        factored = MTex("".join(factored_terms), isolate=factored_terms, tex_to_color_map = {"{" + str(i+1) + "}": elem_colors[i] for i in range(5)}).scale(0.8).next_to(theset, DOWN)
        expanded_terms = ["1"]
        for n in range(1, 16):
            k = len(stacks[n])
            expanded_terms.append((str(k) if k > 1 else "") + f"x^{{{n}}}")
        expanded = MTex("+".join(expanded_terms), isolate=["+", "x", *expanded_terms]).set_width(FRAME_WIDTH - 1).next_to(factored, DOWN).set_x(0)
        fac_term_parts = [factored.get_part_by_tex(term) for term in factored_terms]
        expanded_parts = [expanded.get_part_by_tex(term) for term in expanded_terms]
        expanded_adds = expanded.get_parts_by_tex("+")
        expanded_xs = expanded.get_parts_by_tex("x")
        x_power_8 = term_surrounding(expanded_parts[8], buff=0.05)
        subsets_8 = stacks[8].copy().scale(2).move_to(0.5*DOWN)
        subsets_8[0].shift(0.2*UP)
        subsets_8[2].shift(0.2*DOWN)
        
        self.play(Write(factored), run_time = 1)
        self.waiting(1, 0) #写出这样一个多项式
        self.play(Write(expanded))
        self.play(ShowCreation(x_power_8))
        self.waiting(1+2-3, 22+7) #然后把它乘开 x的8次方对应的系数
        self.play(*[FadeIn(subsets_8[i], 0.5*DOWN, rate_func = squish_rate_func(smooth, 0.25*i, 0.5+0.25*i)) for i in range(3)])
        self.waiting(0, 19) #就是要求的子集数
        self.waiting(0, 17) #（空闲）

        self.play(FadeOut(x_power_8), Transform(subsets_8, stacks[8]))
        self.waiting(0, 6) #不止如此......
        self.play(Write(stacks, lag_ratio = 0.01)) #......每个不同次项的系数
        self.remove(subsets_8)
        self.play(Write(rects))
        self.waiting(0, 25) #都正好是对应的元素和的子集数
        self.waiting(0, 23) #（空闲）

        polymonial_surroundings = VGroup(*[term_surrounding(factored.get_part_by_tex("{" + str(i+1) + "}")) for i in range(5)]).set_fill(color = BACK, opacity = 1)
        problem_surroundings = VGroup(*[term_surrounding(problem.get_part_by_tex(str(i+1)))  for i in range(5)]).set_fill(color = BACK, opacity = 1)
        lines = VGroup(*[Line(problem_surroundings[i].get_corner(DOWN), polymonial_surroundings[i].get_corner(UP), color = BLUE, stroke_width = 2) for i in range(5)])
        shade = BackgroundRectangle(VGroup(polymonial_surroundings, problem_surroundings, lines), fill_opacity = 1, fill_color = BACK)
        self.waiting(2, 24) #这是一个初看特别离谱的操作
        self.bring_to_back(polymonial_surroundings, problem_surroundings).play(ShowCreation(polymonial_surroundings), ShowCreation(problem_surroundings))
        self.bring_to_back(lines).play(ShowCreation(lines), run_time = 2)
        self.waiting(0, 2) #凭什么把每个元素照着抄到系数上
        self.waiting(1, 28) #再把这个多项式乘起来
        self.waiting(1, 25) #就能得到正确的结果了？
        self.waiting(0, 23) #（空闲）

        self.bring_to_back(lines, polymonial_surroundings, problem_surroundings, shade).play(FadeIn(shade), ReplacementTransform(notice2, notice3))
        self.remove(lines, polymonial_surroundings, problem_surroundings, shade).waiting(1, 23) #但离谱中似乎又透着点合理
        super_expanded = VGroup()
        collection_anims = []
        for subset in subsets:
            n = subset[0].sum
            if n == 0:
                new_term = MTex("1", font_size=36)
                super_expanded.add(new_term)
            else:
                new_plus = MTex("+", font_size=36)
                new_term = MTex(f"x^{{{n}}}", font_size=36)
                super_expanded.add(new_plus, new_term)
                collection_anims.append(FadeOut(new_plus))
        super_expanded.arrange(RIGHT, aligned_edge=DOWN, buff=0.1).next_to(factored, DOWN).to_edge(LEFT)
        super_expanded[33:].next_to(super_expanded[0], DOWN, aligned_edge=LEFT)
        collection_anims = [TransformFromCopy(expanded_parts[subsets[i][0].sum], super_expanded[2*i], path_arc=10 * DEGREES) for i in range(32)]
        self.play(
            LaggedStart(*collection_anims),
            LaggedStartMap(FadeOut, expanded),
            LaggedStartMap(FadeIn, super_expanded[1::2]),
            ApplyMethod(stacks.set_opacity, 0.25, rate_func=squish_rate_func(smooth, 0, 0.5)),
            run_time=3)
        self.remove(expanded).add(super_expanded)
        
        for i in range(32):
            top_terms = [
                part[3:-1] if bit else part[1]
                for bit, part in zip(subsets[i][0].bits, fac_term_parts)
            ]
            top_rects = VGroup(*[term_surrounding(part, buff = 0.1) for part in top_terms])
            low_rect = term_surrounding(super_expanded[2*i])
            
            self.add(top_rects, low_rect)
            subsets.set_opacity(0.25)
            subsets[i].set_opacity(1)
            self.wait(0.5)
            self.remove(top_rects, low_rect)
        subsets.set_opacity(0.25)
        self.waiting(2+2+2+2+0+2+3+1+2+0-19, 12+15+0+24+16+14+4+29+11+24) #如果对着多项式多看两眼 就有可能发现这么一件事 展开这个多项式的过程 似乎就是在求每一个子集的过程 （空闲） 但再一细想又不对了 整个多项式就像天上掉下来的一样 如果不是之前见过 根本不可能有人想到这么干

        for anim in collection_anims:
            anim.update_config(rate_func = lambda t: smooth(1-t))
        expanded.shift(0.6*DOWN)
        expanded_reverse = VGroup(*expanded.submobjects[::-1])
        super_expanded_reverse = VGroup(*super_expanded.submobjects[::-1])
        title = Text("母函数", color = YELLOW, font = "simsun").next_to(3*UP, UP)
        line_title = Line(3.5*UP, 3.5*UP)
        self.play(
            LaggedStart(*collection_anims[::-1]), 
            LaggedStartMap(FadeIn, expanded_reverse),
            LaggedStartMap(FadeOut, super_expanded_reverse[1::2]), 
            ApplyMethod(factored.move_to, (factored.get_y()-0.5)*UP, rate_func = squish_rate_func(smooth, 0.5, 1)),
            ApplyMethod(problem.shift, 0.5*DOWN, rate_func = squish_rate_func(smooth, 0.5, 1)),
            FadeIn(title, 0.5*DOWN, rate_func = squish_rate_func(smooth, 0.5, 1)), 
            ApplyMethod(line_title.put_start_and_end_on, 3*UP+6*LEFT, 3*UP+6*RIGHT, rate_func = squish_rate_func(smooth, 0.5, 1)), 
            ReplacementTransform(notice3, notice4, rate_func = squish_rate_func(smooth, 0, 1/3)), 
            FadeOut(stacks), FadeOut(rects), run_time = 3,
        )
        self.remove(super_expanded).add(expanded).waiting(1+4-3, 18+8) #依照翻译的不同 这个多项式一般被称作“母函数”或者“生成函数”
        self.waiting(0, 16) #（空闲）

        expanded.set_opacity(0.25)
        expanded_xs.set_opacity(1)
        x_expanded = expanded.copy().shift(1.5*DOWN)
        expanded.set_opacity(1)

        center_1 = expanded_xs[2].get_center()
        center_2 = expanded_xs[5].get_center()
        center_3 = expanded_xs[8].get_center()
        center_4 = expanded_xs[11].get_center()
        text_1 = Text("不是变量", font="simsun").scale(0.5).shift(center_1+0.5*DOWN).add(Arrow(center_1+0.8*DOWN, center_1+1.2*DOWN, buff = 0))
        text_2 = Text("没法代值", font="simsun").scale(0.5).shift(center_2+0.5*DOWN).add(Arrow(center_2+0.8*DOWN, center_2+1.2*DOWN, buff = 0))
        text_3 = Text("只是记号", font="simsun").scale(0.5).shift(center_3+0.5*DOWN).add(Arrow(center_3+0.8*DOWN, center_3+1.2*DOWN, buff = 0))
        text_4 = Text("没有意义", font="simsun").scale(0.5).shift(center_4+0.5*DOWN).add(Arrow(center_4+0.8*DOWN, center_4+1.2*DOWN, buff = 0))

        self.waiting(2, 4) #大家如果之前学过母函数
        self.play(expanded.animate.set_opacity(0.25), TransformFromCopy(expanded, x_expanded))
        self.waiting(1, 10) #可能会听到这么一个说法
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in [text_1, text_2, text_3, text_4]], lag_ratio = 0.3), run_time = 1.5)
        self.waiting(1.5, 28) #母函数里面的x只是一个抽象的形式记号
        self.waiting(1, 25) #不需要赋予具体数值
        self.waiting(0, 17) #（空闲）
        
        expanded_group = VGroup(x_expanded, text_1, text_2, text_3, text_4)
        self.play(FadeOut(expanded, DOWN), expanded_group.animate.shift(DOWN))
        self.waiting(0, 21) #但实际情况是

        center_5 = factored[8].get_center()
        center_6 = (factored[23].get_center() + factored[24].get_center()) / 2
        text_5 = Text("不是加法", font="simsun").scale(0.5).shift(center_5+DOWN).add(Arrow(center_5+0.7*DOWN, center_5+0.3*DOWN, buff = 0))
        text_6 = Text("不是乘法", font="simsun").scale(0.5).shift(center_6+DOWN).add(Arrow(center_6+0.7*DOWN, center_6+0.3*DOWN, buff = 0))
        line_3 = Line(center_3+1.5*DOWN+0.6*LEFT, center_3+1.5*DOWN+0.6*RIGHT, color = RED)
        line_4 = Line(center_4+1.5*DOWN+0.6*LEFT, center_4+1.5*DOWN+0.6*RIGHT, color = RED)
        self.play(ShowCreation(line_3), ShowCreation(line_4))
        self.play(LaggedStart(*[FadeIn(mob, 0.5*UP) for mob in [text_5, text_6]], lag_ratio = 0.3), run_time = 1)
        self.waiting(0, 25) #x虽然确实不是一个具体的数
        self.waiting(1, 18) #但并不抽象
        self.waiting(1, 10) #相较之下
        self.waiting(2, 17) #这个多项式里面的加法和乘法
        self.waiting(2, 7) #才更应该被叫做形式记号
        self.waiting(0, 21) #（空闲）

        like = Text("", font = 'vanfont').shift(3*LEFT).scale(2)
        coin = Text("", font = 'vanfont').scale(2)
        star = Text("", font = 'vanfont').shift(3*RIGHT).scale(2)
        sanlian = VGroup(like, coin, star)

        self.clear().add(notice4)
        self.play(FadeInFromPoint(like, 3*LEFT), FadeInFromPoint(coin, np.array([0,0,0])), FadeInFromPoint(star, 3*RIGHT), ReplacementTransform(notice4, notice5))
        self.play(Flash(like, flash_radius=1, color = "#00A1D6"), Flash(coin, flash_radius=1, color = "#00A1D6"), Flash(star, flash_radius=1, color = "#00A1D6"), ApplyMethod(sanlian.set_color, "#00A1D6"))
        self.waiting(3-2,17) #长按点赞一键三连 我们开始吧
        
        self.waiting(3, 22)
        self.play(FadeOut(notice5), FadeOut(sanlian))
        self.waiting(4, 0) #到此共114秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

###############################################################################

class Chapter1_0(Scene):

    def construct(self):

        text1 = Text("第一节 加法原理和乘法原理", font = 'simsun', t2c={"第一节": YELLOW, "加法原理": GREEN, "乘法原理": BLUE})

        self.play(Write(text1))
        self.wait(1)
        self.play(FadeOut(text1))

class Chapter1_1(Scene):
    def construct(self):
        notice1 = Notice("本节内容", "请　期待")
        notice2 = Notice("高中数学", "请　复习")
        notice3 = Notice("直接改题", "请勿模仿")
        notice4 = Notice("高中数学", "请　复习")
        notice5 = Notice("触类旁通", "请　模仿")
        notice6 = Notice("见微知著", "请　模仿")

        texts = "求集合$\{1, 2, 3, 4, 5\}$", "元素和为8的", "子集", "的个数"
        problem = MTexText("".join(texts), isolate = [*texts, "元素和为8的子集"], tex_to_color_map = number_color_map).scale(0.8).shift(3*UP)
        delete = problem.get_part_by_tex("元素和为8的")
        delete_line = Line(delete.get_corner(LEFT)+0.05*LEFT, delete.get_corner(RIGHT)+0.05*RIGHT, color = RED)
        indicate = problem.get_part_by_tex("元素和为8的子集")
        problem_numbers = [problem.get_part_by_tex(str(i+1)) for i in range(5)]
        line = Underline(indicate, color = YELLOW)
        factored_terms = "(1 + x^{1})", "(1 + x^{2})", "(1 + x^{3})", "(1 + x^{4})", "(1 + x^{5})"
        factored = MTex("".join(factored_terms), isolate=factored_terms, tex_to_color_map = {"{" + str(i+1) + "}": elem_colors[i] for i in range(5)}).scale(0.8).move_to(2.3*UP).save_state()
        fac_term_parts = [factored.get_part_by_tex(term) for term in factored_terms]
        
        self.play(FadeIn(problem, 0.5*DOWN), FadeIn(factored, 0.5*DOWN), Write(notice1))
        self.waiting(0, 13) #我们先来试试看
        self.waiting(2, 23) #能不能离谱里面看出点合理来
        self.waiting(0, 17) #（空闲）

        principle_add = ImageMobject("add.jpg", height = 2).shift(3*LEFT + 0.5*DOWN)
        principle_mul = ImageMobject("mul.jpg", height = 2).shift(3*RIGHT + 0.5*DOWN)
        label_addmul = Text("加法原理与乘法原理，人教版《数学》选修(B版)2-3，第3页", font = "simsun").scale(0.4).next_to(1.5*DOWN, DOWN)
        self.play(ReplacementTransform(notice1, notice2))
        self.waiting(0, 14) #除了穷举以外
        self.play(FadeIn(principle_add, 0.5*UP), FadeIn(principle_mul, 0.5*UP), FadeIn(label_addmul, 0.5*UP))
        self.waiting(2, 1) #我们学到过的第一种数个数的便捷方法
        self.waiting(2, 7) #是加法原理和乘法原理
        self.waiting(0, 14) #（空闲）

        bubble = Union(Ellipse(width = 2.2, height = 1.1), Triangle().scale(0.5).rotate(-PI/12).shift(0.5*RIGHT + 0.4*DOWN)).set_fill(opacity = 1, color = BACK)
        bubble_1 = bubble.copy().add(Text("太难了", font = "simsun").scale(0.75)).scale(0.8).shift(5.5*LEFT + 1.2*UP)
        bubble_2 = bubble.copy().add(Text("做不来", font = "simsun").scale(0.75)).scale(0.8).shift(0.5*RIGHT + 1.2*UP)
        bubble_3 = bubble.copy().add(Text("这个简单", font = "simsun").scale(0.75)).scale(0.8).shift(5.3*LEFT + 1.2*UP)
        bubble_4 = bubble.copy().add(Text("好耶", font = "simsun").scale(0.75)).scale(0.8).shift(0.7*RIGHT + 1.2*UP)

        shade = Rectangle(height = 3, width = 8.5, fill_opacity = 1, stroke_width = 0, fill_color = BACK).shift(2.5*LEFT + 0.5*UP)
        
        self.play(ShowCreation(line))
        line.reverse_points()
        self.play(Uncreate(line))
        self.waiting(1, 14) #虽然对于数元素和为8的子集数量的任务
        self.play(LaggedStart(FadeInFromPoint(bubble_1, bubble_1.get_corner(DR) + 0.3*DOWN), FadeInFromPoint(bubble_2, bubble_2.get_corner(DR) + 0.3*DOWN), lag_ratio = 0.3, run_time = 1))
        self.waiting(2, 2) #加法原理和乘法原理明显力不从心
        self.play(ShowCreation(delete_line), ReplacementTransform(notice2, notice3), factored.animate.fade())
        self.play(LaggedStart(FadeInFromPoint(bubble_3, bubble_3.get_corner(DR) + 0.3*DOWN), FadeInFromPoint(bubble_4, bubble_4.get_corner(DR) + 0.3*DOWN), lag_ratio = 0.3, run_time = 1))
        self.waiting(1, 4) #但它们至少能帮我们数一数子集的数量
        self.waiting(0, 22) #（空闲）

        arrow = Arrow(problem_numbers[0].get_center()+0.7*UP, problem_numbers[0].get_center()+0.3*UP, buff = 0, color = YELLOW_E)
        self.bring_to_back(bubble_1, bubble_2, bubble_3, bubble_4, shade).play(FadeIn(shade), FadeIn(arrow, 0.5*DOWN), *[mob.animate.shift(0.5*DOWN) for mob in [principle_add, principle_mul, label_addmul, bubble_1, bubble_2, bubble_3, bubble_4]])
        self.remove(bubble_1, bubble_2, bubble_3, bubble_4, shade).play(arrow.animate.set_x(problem_numbers[3].get_x()), run_time = 0.5)
        self.wait(1)
        self.play(arrow.animate.set_x(problem_numbers[1].get_x()), run_time = 0.5)
        self.wait(1)
        self.play(arrow.animate.set_x(problem_numbers[2].get_x()), run_time = 0.5)
        self.wait(1)
        self.play(arrow.animate.set_x(problem_numbers[4].get_x()), run_time = 0.5)
        self.wait(1)
        self.play(arrow.animate.set_x(problem_numbers[0].get_x()))
        self.waiting(6+3-8, 5+8) #在我们从\{1, 2, 3, 4, 5\}这个集合中挑选子集的时候 我们需要决定每一个元素在不在子集里面
        self.waiting(0, 15) #（空闲）

        case_1_1 = MTexText("包含1：1种情况").scale(0.8).next_to(2*LEFT + 1.7*UP, LEFT)
        case_1_2 = MTexText("不包含1：1种情况").scale(0.8).next_to(2*LEFT + 1.1*UP, LEFT)
        case_2_1 = MTexText("包含2：1种情况").scale(0.8).next_to(1.7*UP, LEFT)
        case_2_2 = MTexText("不包含2：1种情况").scale(0.8).next_to(1.1*UP, LEFT)
        case_3_1 = MTexText("包含3：1种情况").scale(0.8).next_to(2*RIGHT + 1.7*UP, LEFT)
        case_3_2 = MTexText("不包含3：1种情况").scale(0.8).next_to(2*RIGHT + 1.1*UP, LEFT)
        case_4_1 = MTexText("包含4：1种情况").scale(0.8).next_to(4*RIGHT + 1.7*UP, LEFT)
        case_4_2 = MTexText("不包含4：1种情况").scale(0.8).next_to(4*RIGHT + 1.1*UP, LEFT)
        case_5_1 = MTexText("包含5：1种情况").scale(0.8).next_to(6*RIGHT + 1.7*UP, LEFT)
        case_5_2 = MTexText("不包含5：1种情况").scale(0.8).next_to(6*RIGHT + 1.1*UP, LEFT)
        formula = MTex("(1+1)(1+1)(1+1)(1+1)(1+1)", isolate = ["(1+1)"]).scale(0.8).shift(0.5*UP).save_state()
        parts_formula = formula.get_parts_by_tex("(1+1)")
        for i in range(5):
            parts_formula[i].set_color(elem_colors[i]).set_x(2*(i-2))
        self.play(LaggedStart(FadeIn(case_1_1, 0.5*RIGHT), FadeIn(case_1_2, 0.5*RIGHT), lag_ratio = 0.3, run_time = 1), ReplacementTransform(notice3, notice4))
        self.waiting(2, 4) #子集可以包含1或者不包含1
        self.waiting(1, 26) #那么根据加法原理
        self.play(Write(parts_formula[0]))
        self.waiting(2, 0) #我们就需要把这两种可能的选择加起来
        self.waiting(0, 15) #（空闲）

        self.play(arrow.animate.set_x(problem_numbers[1].get_x()), Transform(case_1_1, case_2_1), Transform(case_1_2, case_2_2), run_time = 0.5)
        self.play(Write(parts_formula[1]))
        self.play(arrow.animate.set_x(problem_numbers[2].get_x()), Transform(case_1_1, case_3_1), Transform(case_1_2, case_3_2), run_time = 0.5)
        self.play(Write(parts_formula[2]))
        self.play(arrow.animate.set_x(problem_numbers[3].get_x()), Transform(case_1_1, case_4_1), Transform(case_1_2, case_4_2), run_time = 0.5)
        self.play(Write(parts_formula[3]))
        self.play(arrow.animate.set_x(problem_numbers[4].get_x()), Transform(case_1_1, case_5_1), Transform(case_1_2, case_5_2), run_time = 0.5)
        self.play(Write(parts_formula[4]))
        self.waiting(3+2-6, 8+27) #对于2 3 4和5 每个数字也都各有两种选择

        self.play(FadeOut(arrow), FadeOut(case_1_1), FadeOut(case_1_2))
        self.waiting(1, 14) #最后 根据乘法原理
        self.play(formula.animate.restore())
        self.waiting(1, 7) #我们把这5个部分乘起来
        self.waiting(1, 23) #就能得到最终的结果
        self.waiting(0, 18) #（空闲）

        result = MTex("=32").scale(0.8).next_to(formula, buff = 0.15)
        self.waiting(2, 15) #这不过是小学二年级程度的计算
        self.play(Write(result))
        self.waiting(1, 15) #很容易就能算出来结果是32
        self.waiting(0, 15) #（空闲）

        texts = [r"(\text{不选}"+str(i+1)+r"\ \text{或}\ \text{选}"+str(i+1)+r")" for i in range(5)]
        operation = MTex(r"\text{和}".join(texts), isolate = [*texts, r"\text{和}"], 
        tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r"\text{或}", r")"): WHITE}).scale(0.65).shift(0.5*UP)
        operation_terms = [operation.get_part_by_tex(texts[i]).set_x(2.5*(i-2)) for i in range(5)]
        operation_muls = operation.get_parts_by_tex(r"\text{和}")
        for i in range(4):
            operation_muls[i].set_x(2.5*(i-1.5))
            
        self.play(FadeOut(result, 0.5*RIGHT), ReplacementTransform(notice4, notice5))
        self.waiting(1, 13) #但这个式子的重点不在结果
        anims = [Indicate(mtex) for mtex in formula]
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2))
        self.waiting(0, 14) #而在它刚写下来的样子
        self.play(fac_term_parts[0].animate.move_to(1.7*UP + 5*LEFT).set_opacity(1), parts_formula[0].animate.move_to(1.1*UP + 5*LEFT).set_color(elem_colors[0]))
        self.play(fac_term_parts[4].animate.move_to(1.7*UP + 5*RIGHT).set_opacity(1), parts_formula[4].animate.move_to(1.1*UP + 5*RIGHT).set_color(elem_colors[4]))
        self.play(fac_term_parts[1].animate.move_to(1.7*UP + 2.5*LEFT).set_opacity(1), parts_formula[1].animate.move_to(1.1*UP + 2.5*LEFT).set_color(elem_colors[1]))
        self.play(fac_term_parts[3].animate.move_to(1.7*UP + 2.5*RIGHT).set_opacity(1), parts_formula[3].animate.move_to(1.1*UP + 2.5*RIGHT).set_color(elem_colors[3]))
        self.play(fac_term_parts[2].animate.move_to(1.7*UP).set_opacity(1), parts_formula[2].animate.move_to(1.1*UP).set_color(elem_colors[2]))
        self.waiting(2+1+1+1-5, 4+18+14+25) #它和之前写出的母函数 用了同样多的加法 同样多的乘法 同样多的括号
        
        rect_factored_2 = [term_surrounding(fac_term_parts[i][3:-1]) for i in range(5)]
        rect_formula_2 = [term_surrounding(parts_formula[i][3]) for i in range(5)]
        self.waiting(1, 10) #唯一的区别......
        self.play(LaggedStart(*[ShowCreation(mob) for mob in rect_factored_2], lag_ratio = 0.3, run_time = 1.2))
        self.play(LaggedStart(*[ShowCreation(mob) for mob in rect_formula_2], lag_ratio = 0.3, run_time = 1.2))
        self.waiting(1, 13) #......是所有的x 全部变成了另一个1
        self.waiting(0, 18) #（空闲）

        self.play(*[FadeOut(mob) for mob in [*rect_factored_2, *rect_formula_2]], LaggedStart(*anims, lag_ratio = 0.1, run_time = 2))
        self.waiting(0, 29) #但这个式子是我们一步一步造出来的
        self.play(factored.animate.fade())
        self.waiting(0, 23) #比起母函数来 可要好理解多了
        self.waiting(0, 18) #（空闲）

        self.play(LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in operation_terms], lag_ratio = 0.3, run_time = 1), ReplacementTransform(notice5, notice6))
        self.waiting(2, 11) #每一个1+1代表了是否选取某个元素
        self.play(LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in operation_muls], lag_ratio = 0.3, run_time = 1))
        self.waiting(2, 14) #而五个1+1相乘代表了五次选取
        self.waiting(0, 15) #（空闲）

        operation_terms_1 = [term_surrounding(operation_terms[i][1:4]).set_fill(opacity = 1, color = BACK) for i in range(5)]
        operation_terms_2 = [term_surrounding(operation_terms[i][5:7]).set_fill(opacity = 1, color = BACK) for i in range(5)]
        operation_terms = list(it.chain(*zip(operation_terms_1, operation_terms_2)))
        rect_formula_1 = [term_surrounding(parts_formula[i][1]).set_fill(opacity = 1, color = BACK) for i in range(5)]
        rect_formula_2 = [term_surrounding(parts_formula[i][3]).set_fill(opacity = 1, color = BACK) for i in range(5)]
        rect_formula = list(it.chain(*zip(rect_formula_1, rect_formula_2)))
        lines_formula = [Line(operation_terms[i].get_center(), rect_formula[i].get_center(), stroke_width = 2, color = BLUE) for i in range(10)]
        rect_factored_1 = [term_surrounding(fac_term_parts[i][1]).set_fill(opacity = 1, color = BACK) for i in range(5)]
        rect_factored_2 = [term_surrounding(fac_term_parts[i][3:-1]).set_fill(opacity = 1, color = BACK) for i in range(5)]
        rect_factored = list(it.chain(*zip(rect_factored_1, rect_factored_2)))
        lines_factored = [Line(operation_terms[i].get_center(), rect_factored[i].get_center(), stroke_width = 2, color = BLUE) for i in range(10)]
        self.waiting(1, 12) #这个式子整体......
        self.bring_to_back(*operation_terms).play(LaggedStart(*[ShowCreation(mob) for mob in operation_terms], group = VGroup(), lag_ratio = 0.3, run_time = 1.5))
        self.waiting(0.5, 15) #......就是把所有的操作都写下来以后
        self.bring_to_back(*lines_formula, *operation_terms, *rect_formula).play(LaggedStart(*[ShowCreation(mob) for mob in rect_formula], group = VGroup()), LaggedStart(*[ShowCreation(mob) for mob in lines_formula], group = VGroup()), lag_ratio = 0.3, run_time = 1.5)
        self.waiting(0.5, 21) #把它们依次替换成需要算的值
        self.waiting(0, 17) #（空闲）

        arrow_1 = Arrow(1.7*UP + 6.6*LEFT, 1.7*UP + 5.9*LEFT, path_arc = DEGREES, buff = 0)
        arrow_2 = Arrow(1.1*UP + 6.6*LEFT, 1.1*UP + 5.9*LEFT, path_arc = DEGREES, buff = 0)
        arrow_3 = Arrow(0.5*UP + 6.2*LEFT, 1.7*UP + 5.9*LEFT, path_arc = -PI*5/6, buff = 0)
        arrow_4 = Arrow(0.5*UP + 6.2*LEFT, 1.1*UP + 5.9*LEFT, path_arc = -PI*11/12, buff = 0)
        self.play(factored.animate.set_opacity(1), FadeIn(arrow_1, 0.3*RIGHT), FadeIn(arrow_2, 0.3*RIGHT))
        self.waiting(2, 1) #这样一来 这两个式子长得很像
        self.waiting(1, 24) #就是一件非常自然的事了
        self.waiting(0, 17) #（空闲）

        self.play(Transform(arrow_1, arrow_3), Transform(arrow_2, arrow_4), FadeOut(delete_line))
        self.waiting(1, 20) #它们就是一个模子里刻出来的
        self.bring_to_back(*lines_factored, *lines_formula, *operation_terms, *rect_factored).play(LaggedStart(*[ShowCreation(mob) for mob in rect_factored], group = VGroup()), LaggedStart(*[ShowCreation(mob) for mob in lines_factored], group = VGroup()), lag_ratio = 0.3, run_time = 1.5)
        self.waiting(1, 5) #都是将所有可能的操作
        self.waiting(2, 15) #依次替换成了需要算的值
        self.waiting(0, 21) #到此共111秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_2(Scene):
    def construct(self):
        notice6 = Notice("见微知著", "请　模仿")
        notice7 = Notice("符号约定", "请　模仿")
        notice8 = Notice("暗箱操作", "请勿模仿")
        notice9 = Notice("这里是一个", "数学频道")

        texts = "求集合$\{1, 2, 3, 4, 5\}$", "元素和为8的", "子集", "的个数"
        problem = MTexText("".join(texts), isolate = [*texts, "元素和为8的子集"], tex_to_color_map = number_color_map).scale(0.8).shift(3*UP)
        factored_terms = "(1 + x^{1})", "(1 + x^{2})", "(1 + x^{3})", "(1 + x^{4})", "(1 + x^{5})"
        factored = MTex("".join(factored_terms), isolate=factored_terms, tex_to_color_map = {"{" + str(i+1) + "}": elem_colors[i] for i in range(5)}).scale(0.8)
        fac_term_parts = [factored.get_part_by_tex(factored_terms[i]).move_to(1.7*UP + 2.5*(i-2)*RIGHT) for i in range(5)]
        formula = MTex("(1+1)(1+1)(1+1)(1+1)(1+1)", isolate = ["(1+1)"]).scale(0.8)
        parts_formula = formula.get_parts_by_tex("(1+1)")
        for i in range(5):
            parts_formula[i].set_color(elem_colors[i]).move_to(2.5*(i-2)*RIGHT + 1.1*UP)
        texts = [r"(\text{不选}"+str(i+1)+r"\ \text{或}\ \text{选}"+str(i+1)+r")" for i in range(5)]
        operation = MTex(r"\text{和}".join(texts), isolate = [*texts, r"\text{和}"], 
            tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r"\text{或}", r")"): WHITE}).scale(0.65).shift(0.5*UP)
        operation_terms = [operation.get_part_by_tex(texts[i]).set_x(2.5*(i-2)) for i in range(5)]
        operation_muls = operation.get_parts_by_tex(r"\text{和}")
        operation_adds = operation.get_parts_by_tex(r"\text{或}")
        for i in range(4):
            operation_muls[i].set_x(2.5*(i-1.5))
        operation.refresh_bounding_box()

        arrow_3 = Arrow(0.5*UP + 6.2*LEFT, 1.7*UP + 5.9*LEFT, path_arc = -PI*5/6, buff = 0)
        arrow_4 = Arrow(0.5*UP + 6.2*LEFT, 1.1*UP + 5.9*LEFT, path_arc = -PI*11/12, buff = 0)
        
        rect_operation_1 = [term_surrounding(term[1:4]).set_fill(opacity = 1, color = BACK) for term in operation_terms]
        rect_operation_2 = [term_surrounding(term[5:7]).set_fill(opacity = 1, color = BACK) for term in operation_terms]
        rect_operation = list(it.chain(*zip(rect_operation_1, rect_operation_2)))
        rect_formula_1 = [term_surrounding(term[1]).set_fill(opacity = 1, color = BACK) for term in parts_formula]
        rect_formula_2 = [term_surrounding(term[3]).set_fill(opacity = 1, color = BACK) for term in parts_formula]
        rect_formula = list(it.chain(*zip(rect_formula_1, rect_formula_2)))
        lines_formula = [Line(rect_operation[i].get_center(), rect_formula[i].get_center(), stroke_width = 2, color = BLUE) for i in range(10)]
        rect_factored_1 = [term_surrounding(term[1]).set_fill(opacity = 1, color = BACK) for term in fac_term_parts]
        rect_factored_2 = [term_surrounding(term[3:-1]).set_fill(opacity = 1, color = BACK) for term in fac_term_parts]
        rect_factored = list(it.chain(*zip(rect_factored_1, rect_factored_2)))
        lines_factored = [Line(rect_operation[i].get_center(), rect_factored[i].get_center(), stroke_width = 2, color = BLUE) for i in range(10)]
        
        principle_add = ImageMobject("add.jpg", height = 2).shift(3*LEFT + 1*DOWN)
        principle_mul = ImageMobject("mul.jpg", height = 2).shift(3*RIGHT + 1*DOWN)
        label_addmul = Text("加法原理与乘法原理，人教版《数学》选修(B版)2-3，第3页", font = "simsun").scale(0.4).next_to(2*DOWN, DOWN)
        
        self.add(notice6, *lines_factored, *lines_formula, *rect_operation, *rect_formula, *rect_factored, arrow_3, arrow_4, problem, factored, formula, operation, principle_add, principle_mul, label_addmul)
        
        shade = Rectangle(width = 16, height = 1.8, fill_opacity = 1, fill_color = BACK, stroke_width = 0).shift(1.1*UP)
        self.waiting(2, 12) #但我们为什么可以替换呢？
        self.add(shade, operation).play(FadeIn(shade), *[FadeOut(mob) for mob in [arrow_3, arrow_4, principle_add, principle_mul, label_addmul]])
        self.remove(shade, *lines_factored, *lines_formula, *rect_operation, *rect_formula, *rect_factored, factored, formula)
        self.waiting(2, 0) #这就需要仔细观察一下所有可能的操作了
        self.waiting(0, 20) #（空闲）

        rect_add = [term_surrounding(term).set_fill(opacity = 1, color = BACK) for term in operation_adds]
        arrow_add = [Arrow(0.7*DOWN + term.get_center(), 0.3*DOWN + term.get_center(), buff = 0, color = YELLOW) for term in operation_adds]
        rect_mul = [term_surrounding(term).set_fill(opacity = 1, color = BACK) for term in operation_muls]
        arrow_mul = [Arrow(0.7*UP + term.get_center(), 0.3*UP + term.get_center(), buff = 0, color = GREEN) for term in operation_muls]
        self.play(*[mob.animate.set_color(YELLOW) for mob in operation_adds], *[mob.animate.set_color(GREEN) for mob in operation_muls])
        self.waiting(2, 22) #操作式里面有两种运算 “或”与“和”
        self.waiting(0, 18) #（空闲）

        self.bring_to_back(*rect_add).play(LaggedStart(*[ShowCreation(mob) for mob in rect_add], group = VGroup(), lag_ratio = 0.3, run_time = 1.5), LaggedStart(*[FadeIn(mob, 0.3*UP) for mob in arrow_add], lag_ratio = 0.3, run_time = 1.5))
        self.waiting(1.5, 10) #“或”运算连接了同一步选择中的不同选项
        self.bring_to_back(*rect_mul).play(LaggedStart(*[ShowCreation(mob) for mob in rect_mul], group = VGroup(), lag_ratio = 0.3, run_time = 1.5), LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in arrow_mul], lag_ratio = 0.3, run_time = 1.5))
        self.waiting(0.5, 16) #“和”运算连接了不同步的选择
        self.waiting(0, 15) #（空闲）

        text_1 = r"(\text{不选}1\ \text{或}\ \text{选}1)\ \text{和}\ (\text{不选}2\ \text{或}\ \text{选}2)"
        text_2 = r"=\text{不选}1\text{和}\text{不选}2\ \text{或}\ \text{选}1\text{和}\text{不选}2\ \text{或}\ \text{不选}1\text{和}\text{选}2\ \text{或}\ \text{选}1\text{和}\text{选}2"
        example = MTex(text_1+text_2, isolate = [text_1, text_2], tex_to_color_map = {r"\text{或}": YELLOW, r"\text{和}": GREEN, (r"\text{不选}1", r"\text{选}1"): elem_colors[0], (r"\text{不选}2", r"\text{选}2"): elem_colors[1]}).scale(0.6).shift(DOWN)
        example_1 = example.get_part_by_tex(text_1)
        example_2 = example.get_part_by_tex(text_2)
        self.play(TransformFromCopy(operation[0:17], example_1))
        self.play(Write(example_2))
        self.waiting(0, 11) #很自然地 “和”对“或”有着分配律
        self.waiting(0, 22) #（空闲）

        offset = 2.4*UP + 6.9*LEFT - operation.get_corner(LEFT)
        self.play(*[FadeOut(mob, offset, path_arc=-PI/6) for mob in [*rect_add, *arrow_add, *rect_mul, *arrow_mul]], ApplyMethod(operation.shift, offset, path_arc=-PI/6), FadeOut(example))
        self.waiting(1, 14) #有了分配律就可以开始算了
        self.play(ReplacementTransform(notice6, notice7))
        self.waiting(0, 22) #但在我们开始之前
        self.waiting(2, 1) #还有几件需要注意的事情
        self.waiting(0, 19) #（空闲）

        self.remove(operation).add(*operation_terms, *operation_muls).play(LaggedStart(*[Swirl(term) for term in operation_muls], lag_ratio = 0.3, run_time = 2))
        self.play(*[operation_terms[i].animate.shift((0.4*i - 0.9)*LEFT) for i in range(5)])
        self.waiting(0, 24) #就像乘法那样 “和”也经常被省略不写

        choices = [[r"\text{不选}"+str(i+1), r"\text{选}"+str(i+1)] for i in range(5)]
        subsets = [text_1+text_2+text_3+text_4+text_5 for text_1 in choices[0] for text_2 in choices[1] for text_3 in choices[2] for text_4 in choices[3] for text_5 in choices[4]]
        expanded = MTex(r"\ \text{或}\ ".join(subsets), isolate = subsets, tex_to_color_map = {**{(choices[i][0], choices[i][1]): elem_colors[i] for i in range(5)}, r"\text{或}": YELLOW}).scale(0.45)
        expanded_subsets = [expanded.get_part_by_tex(text) for text in subsets]
        expanded_adds = expanded.get_parts_by_tex(r"\text{或}")
        element_1, element_2, element_3, element_4, element_5 = [[], [1]], [[], [2]], [[], [3]], [[], [4]], [[], [5]]
        tex_subsets = [get_set_tex(bool_1+bool_2+bool_3+bool_4+bool_5).scale(0.45) for bool_1 in element_1 for bool_2 in element_2 for bool_3 in element_3 for bool_4 in element_4 for bool_5 in element_5]
        for i in range(8):
            for j in range(4):
                k = i*4+j
                expanded_subsets[k].next_to((3*j-3)*RIGHT + (0.65*i-1.75)*DOWN, LEFT, buff = 0.2)
                tex_subsets[k].move_to((3*j-4.5)*RIGHT + (0.65*i-2.075)*DOWN)
                if k > 0:
                    expanded_adds[k-1].move_to((3*j-6)*RIGHT + (0.65*i-1.75)*DOWN)
        equality = MTex("=").scale(0.65).next_to(6*LEFT + 1.75*UP, LEFT, buff = 0.3).add(*expanded.submobjects)

        board = Rectangle(height = 6.2, width = 9, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        board_inner = Rectangle(height = 6, width = 8.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        board.add(board_inner).shift(0.1*UP + 7.5*UP)
        shade_all = Rectangle(height = FRAME_HEIGHT, width = FRAME_WIDTH, stroke_width = 0, fill_opacity = 0, fill_color = BACK)
        title_operation = Text("操作运算", color = YELLOW, font = "simhei").shift(2.1*UP + 2*LEFT)
        title_bool = Text("布尔运算", color = YELLOW, font = "simhei").shift(2.1*UP + 2*RIGHT)
        adds = MTex(r"\text{或}\ne \text{或}", tex_to_color_map = {r"\text{或}": RED}).scale(2).shift(0.6*UP)
        muls = MTex(r"\text{和}\ne \text{与}", tex_to_color_map = {r"\text{和}": RED, r"\text{与}": RED}).scale(2).shift(0.9*DOWN)
        adds[0].set_x(-1.5)
        adds[-1].set_x(1.5)
        muls[0].set_x(-1.5)
        muls[-1].set_x(1.5)
        arrow_1_1 = Arrow(2.4*LEFT+0.6*UP, 2*LEFT+0.6*UP, buff = 0)
        text_1_1 = Text("多种选择能且仅能选一个", font = "simsun").arrange_in_grid(3, 4, buff = 0.05).scale(0.5).next_to(2.5*LEFT+0.6*UP, LEFT, buff = 0).add(arrow_1_1)
        arrow_1_2 = Arrow(2.4*RIGHT+0.6*UP, 2*RIGHT+0.6*UP, buff = 0)
        text_1_2 = Text("多个条件一个为真即为真", font = "simsun").arrange_in_grid(3, 4, buff = 0.05).scale(0.5).next_to(2.5*RIGHT+0.6*UP, RIGHT, buff = 0).add(arrow_1_2)
        arrow_3 = Arrow(2.15*DOWN + 1.5*LEFT, 1.15*DOWN + 1.5*LEFT)
        arrow_4 = Arrow(2.15*DOWN + 1.5*RIGHT, 1.15*DOWN + 1.5*RIGHT)
        text_2 = Text("一点关系也没有，只是恰巧名字差不多", font = "simsun").scale(0.5).shift(2.15*DOWN).add(arrow_3, arrow_4)
        
        self.add(shade_all, notice7, board).play(board.animate.shift(7.5*DOWN), shade_all.animate.set_opacity(0.8))
        self.bring_to_back(equality).play(Write(equality, lag_ratio = 0.1), 
            ReplacementTransform(notice7, notice8, rate_func = squish_rate_func(smooth, 0, 1/15)), 
            Write(title_operation, rate_func = squish_rate_func(smooth, 0, 1/10)), Write(title_bool, rate_func = squish_rate_func(smooth, 0, 1/10)), 
            FadeIn(adds[0], 0.5*DOWN, rate_func = squish_rate_func(smooth, 0, 1/15)), FadeIn(adds[-1], 0.5*DOWN, rate_func = squish_rate_func(smooth, 0, 1/15)), 
            FadeIn(muls[0], 0.5*DOWN, rate_func = squish_rate_func(smooth, 1/30, 1/10)), FadeIn(muls[-1], 0.5*DOWN, rate_func = squish_rate_func(smooth, 1/30, 1/10)), 
            Write(adds[1:-1], rate_func = squish_rate_func(smooth, (1+17/30)/15, (2+17/30)/15)), Write(muls[1:-1], rate_func = squish_rate_func(smooth, (1+17/30)/15, (2+17/30)/15)),
            FadeIn(text_1_1, 0.5*RIGHT, rate_func = squish_rate_func(smooth, (7+3/30)/15, (8+3/30)/15)), FadeIn(text_1_2, 0.5*LEFT, rate_func = squish_rate_func(smooth, (8+3/30)/15, (9+3/30)/15)), 
            FadeIn(text_2, 0.5*UP, rate_func = squish_rate_func(smooth, (11+20/30)/15, (12+20/30)/15)), 
            run_time = 15)
        self.waiting(2+4+0+4+4-16, 17+24+22+17+12) #而且 虽然名字差不多 但这两种二元运算和布尔运算里面的“或”和“与”没什么关系 （空闲） 即使能硬说操作之间的“或”比较像布尔运算中的“异或” 操作之间的“和”与布尔运算中的“与”也是完全没关系的
        self.waiting(0, 12) #到此共49秒
        
        self.play(*[mob.animate.shift(7.5*UP) for mob in [board, title_operation, title_bool, adds, muls, text_1_1, text_1_2, text_2]], FadeOut(shade_all), ReplacementTransform(notice8, notice9))
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter1_3(Scene):
    def construct(self):
        notice9 = Notice("这里是一个", "数学频道")
        notice10 = Notice("简单情况", "请　显然")
        notice11 = Notice("问题不大", "请勿惊慌")
        notice12 = Notice("小修小补", "请　模仿")
        notice13 = Notice("构造完毕", "请　鼓掌")
        notice14 = Notice("彼岸行为", "请勿模仿")
        notice15 = Notice("下节预告", "请　期待")

        texts = "求集合$\{1, 2, 3, 4, 5\}$", "元素和为8的", "子集", "的个数"
        problem = MTexText("".join(texts), isolate = [*texts, "元素和为8的子集"], tex_to_color_map = number_color_map).scale(0.8).shift(3*UP)
        texts = [r"(\text{不选}"+str(i+1)+r"\ \text{或}\ \text{选}"+str(i+1)+r")" for i in range(5)]
        operation = MTex("".join(texts), isolate = texts, 
            tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"\text{或}": YELLOW}).scale(0.65).shift(0.5*UP)
        operation_terms = [operation.get_part_by_tex(texts[i]).next_to(6*LEFT + 2.4*UP + 2.1*i*RIGHT, buff = 0) for i in range(5)]
        operation.refresh_bounding_box()
        
        choices = [[r"\text{不选}"+str(i+1), r"\text{选}"+str(i+1)] for i in range(5)]
        subsets = [text_1+text_2+text_3+text_4+text_5 for text_1 in choices[0] for text_2 in choices[1] for text_3 in choices[2] for text_4 in choices[3] for text_5 in choices[4]]
        expanded = MTex(r"\ \text{或}\ ".join(subsets), isolate = subsets, tex_to_color_map = {**{(choices[i][0], choices[i][1]): elem_colors[i] for i in range(5)}, r"\text{或}": YELLOW}).scale(0.45)
        expanded_subsets = [expanded.get_part_by_tex(text) for text in subsets]
        expanded_adds = expanded.get_parts_by_tex(r"\text{或}")
        element_1, element_2, element_3, element_4, element_5 = [[], [1]], [[], [2]], [[], [3]], [[], [4]], [[], [5]]
        tex_subsets = [get_set_tex(bool_1+bool_2+bool_3+bool_4+bool_5).scale(0.45) for bool_1 in element_1 for bool_2 in element_2 for bool_3 in element_3 for bool_4 in element_4 for bool_5 in element_5]
        for i in range(8):
            for j in range(4):
                k = i*4+j
                expanded_subsets[k].next_to((3*j-3)*RIGHT + (0.65*i-1.75)*DOWN, LEFT, buff = 0.2)
                tex_subsets[k].next_to((3*j-4.4)*RIGHT + (0.65*i-2.075)*DOWN, LEFT, buff = 0.05)
                if k > 0:
                    expanded_adds[k-1].move_to((3*j-6)*RIGHT + (0.65*i-1.75)*DOWN)
        sum_subsets = [get_sum_group(set_tex) for set_tex in tex_subsets]
        equality = MTex("=").scale(0.65).next_to(6*LEFT + 1.75*UP, LEFT, buff = 0.3)
        all_mtex = VGroup(expanded, *tex_subsets, *sum_subsets, equality)

        self.add(notice9, problem, operation, equality, expanded)
        self.waiting(2, 6) #把这些括号依次展开
        self.waiting(2, 2) #把每一项都乘出来
        self.waiting(2, 12) #会得到一个有32项的式子
        self.waiting(0, 18) #（空闲）
        self.play(LaggedStart(*[FadeIn(mob, 0.2*RIGHT) for mob in tex_subsets], lag_ratio = 0.2, run_time = 3))
        self.waiting(0, 22) #这些项正好对应着所有的32个子集
        self.waiting(0, 18) #（空闲）
        self.waiting(2, 7) #如果我们用穷举法解题
        self.play(LaggedStart(*[FadeIn(mob, 0.2*RIGHT) for mob in sum_subsets], lag_ratio = 0.2, run_time = 3))
        self.waiting(1, 21) #那么下一步就是把这32个子集全部变成我们想算的值
        self.waiting(2, 16) #但既然计算步骤是一样的
        self.play(SwallowIn(all_mtex))
        self.waiting(0, 4) #我们就可以换一下顺序
        self.waiting(2, 2) #先替换 再计算
        self.waiting(0, 26) #（空闲）

        sum_subsets = MTex(r"(1+1)(1+1)(1+1)(1+1)(1+1)", isolate = {r"(1+1)"}).move_to(operation.get_center() + 1.2*DOWN)
        terms_subsets = sum_subsets.get_parts_by_tex(r"(1+1)")
        mul_subsets = MTex("=32").next_to(sum_subsets)
        anims = []
        for i in range(5):
            anims.append(TransformFromCopy(operation_terms[i][0], terms_subsets[i][0]))
            anims.append(TransformFromCopy(operation_terms[i][1:4], terms_subsets[i][1].set_color(elem_colors[i])))
            anims.append(TransformFromCopy(operation_terms[i][4], terms_subsets[i][2].set_color(YELLOW)))
            anims.append(TransformFromCopy(operation_terms[i][5:7], terms_subsets[i][3].set_color(elem_colors[i])))
            anims.append(TransformFromCopy(operation_terms[i][7], terms_subsets[i][4]))
        self.play(LaggedStart(*anims,lag_ratio = 0.05, run_time = 2), ReplacementTransform(notice9, notice10))
        self.play(Write(mul_subsets))
        self.waiting(2+1-3, 24+29) #我们如果把每种操作都替换成1 就能算出子集的总数
        self.waiting(0, 16) #（空闲）

        texts = r"(1+1)", r"(1+2)", r"(1+3)", r"(1+4)", r"(1+5)"
        sum_sums = MTex("".join(texts), isolate = texts).move_to(operation.get_center() + 1.2*DOWN)
        mul_sums = MTex("=720").next_to(sum_sums)
        arrow = Arrow(ORIGIN, 0.6*UP, buff = 0).next_to(mul_sums[2], DOWN)
        question = MTexText("???").next_to(arrow, DOWN).add(arrow)
        terms_sums = [sum_sums.get_part_by_tex(text) for text in texts]
        anims = []
        for i in range(5):
            anims.append(TransformFromCopy(operation_terms[i][0], terms_sums[i][0]))
            anims.append(TransformFromCopy(operation_terms[i][1:4], terms_sums[i][1].set_color(elem_colors[i])))
            anims.append(TransformFromCopy(operation_terms[i][4], terms_sums[i][2].set_color(YELLOW)))
            anims.append(TransformFromCopy(operation_terms[i][5:7], terms_sums[i][3].set_color(elem_colors[i])))
            anims.append(TransformFromCopy(operation_terms[i][7], terms_sums[i][4]))
        self.play(LaggedStart(*anims,lag_ratio = 0.05, run_time = 2), FadeOut(sum_subsets, 1.2*DOWN), FadeOut(mul_subsets, 1.2*DOWN), ReplacementTransform(notice10, notice11))
        self.play(Write(mul_sums))
        self.waiting(0, 1) #但如果把每种操作替换成对应的数
        self.play(FadeIn(question, 0.5*UP))
        self.waiting(1, 28) #却没法算出元素和为8的子集总数
        self.waiting(0, 17) #（空闲）

        operation_add = MTex(r"\text{或}", color = YELLOW).shift(0.25*DOWN + 4.5*LEFT)
        operation_mul = MTex(r"\text{和}", color = GREEN).shift(0.25*DOWN + 3*LEFT)
        arrow_add = Arrow(0.75*DOWN + 4.5*LEFT, 1.25*DOWN + 4.5*LEFT, buff = 0, color = YELLOW)
        arrow_mul = Arrow(0.75*DOWN + 3*LEFT, 1.25*DOWN + 3*LEFT, buff = 0, color = GREEN)
        symbol_add = MTex(r"+", color = YELLOW).scale(1.5).shift(1.75*DOWN + 4.5*LEFT).add(arrow_add)
        symbol_mul = MTex(r"\times", color = GREEN).scale(1.5).shift(1.75*DOWN + 3*LEFT).add(arrow_mul)
        example_operations = MTex(r"\text{选}3\ \text{和}\ \text{选}5", tex_to_color_map = {r"\text{选}3": elem_colors[2], r"\text{和}": GREEN, r"\text{选}5": elem_colors[4]}).shift(0.25*DOWN)
        arrow_example = Arrow(0.75*DOWN, 1.25*DOWN, buff = 0, color = BLUE)
        example_sum = MTex(r"3+5", tex_to_color_map = {r"3": elem_colors[2], r"+": YELLOW, r"5": elem_colors[4]}).shift(1.75*DOWN)
        self.play(FadeOut(question), FadeOut(mul_sums))
        self.waiting(1, 5) #这是因为在替换的时候
        self.play(LaggedStart(ShowCreation(operation_add), ShowCreation(operation_mul), run_time = 1, lag_ratio = 0.5))
        self.waiting(1, 6) #“或”运算 与“和”运算
        self.play(LaggedStart(FadeIn(symbol_add, 0.5*DOWN), FadeIn(symbol_mul, 0.5*DOWN), run_time = 1, lag_ratio = 0.5))
        self.waiting(2, 11) #分别被我们替换成了加法和乘法
        self.play(Write(example_operations), run_time = 1)
        self.waiting(1, 15) #但如果要计算一个子集的(元素)和
        self.play(FadeIn(arrow_example, 0.5*DOWN), FadeIn(example_sum, 0.5*DOWN))
        self.waiting(2, 12) #“和”运算所对应的选择应该被加起来才对
        self.waiting(0, 18) #（空闲）

        require_mul = MTex(r"\times", color = GREEN).scale(1.5).move_to(0.25*DOWN + 2*RIGHT)
        require_add = MTex(r"+", color = YELLOW).scale(1.5).move_to(1.75*DOWN + 2*RIGHT)
        require_arrow = Arrow(0.75*DOWN + 2*RIGHT, 1.25*DOWN + 2*RIGHT, buff = 0, color = BLUE)
        require_question = MTex("?", color = BLUE).scale(0.8).shift(DOWN + 2.25*RIGHT)
        require = VGroup(require_mul, require_arrow, require_add, require_question)
        self.waiting(2, 0) #想要算出正确的答案
        self.play(FadeIn(require, 0.5*RIGHT))
        self.waiting(2, 5) #就需要另一种能把乘法变回加法的运算
        self.waiting(0, 16) #（空闲）

        sloution_mul = MTex(r"x^3\times x^5", tex_to_color_map = {r"3": elem_colors[2], r"\times": GREEN, r"5": elem_colors[4]}).shift(0.2*DOWN + 3*RIGHT)
        solution_add = MTex(r"x^{3+5}", tex_to_color_map = {r"3": elem_colors[2], r"+": YELLOW, r"5": elem_colors[4]}).shift(1.7*DOWN + 3*RIGHT)
        solution_arrow = Arrow(0.75*DOWN + 3*RIGHT, 1.25*DOWN + 3*RIGHT, buff = 0, color = BLUE)
        solution = VGroup(sloution_mul, solution_add, solution_arrow)
        arrow_fixed_mul = Arrow(1.5*RIGHT + 0.25*DOWN, 2*RIGHT + 0.25*DOWN, buff = 0, color = GREEN)
        arrow_fixed_add = Arrow(2*RIGHT + 1.75*DOWN, 1.5*RIGHT + 1.75*DOWN, buff = 0, color = YELLOW)
        self.play(FadeOut(require, 3*RIGHT), FadeIn(solution), ReplacementTransform(notice11, notice12))
        self.waiting(2, 20) #正巧 指数运算就有这种性质
        self.play(Uncreate(arrow_example), LaggedStart(ShowCreation(arrow_fixed_mul), ShowCreation(arrow_fixed_add), run_time = 1, lag_ratio = 1))
        self.waiting(1, 10) #因为我们只需要利用这种性质
        self.waiting(2, 19) #所以底数是谁无关紧要
        self.waiting(1, 22) #随便写一个x就行
        self.waiting(0, 18) #（空闲）

        texts = r"(1+x^{1})", r"(1+x^{2})", r"(1+x^{3})", r"(1+x^{4})", r"(1+x^{5})"
        sum_func = MTex("".join(texts), isolate = texts, tex_to_color_map = {r"{"+str(i+1)+r"}": elem_colors[i] for i in range(5)}).move_to(operation.get_center() + 1.2*DOWN + 0.5*RIGHT)
        symbol_func = MTex(r"P(x)=").next_to(sum_func, LEFT)
        terms_func = [sum_func.get_part_by_tex(text) for text in texts]
        anims = []
        for i in range(5):
            anims.append(ReplacementTransform(terms_sums[i][0], terms_func[i][0]))
            anims.append(ReplacementTransform(terms_sums[i][1], terms_func[i][1]))
            anims.append(ReplacementTransform(terms_sums[i][2], terms_func[i][2].set_color(YELLOW)))
            anims.append(ReplacementTransform(terms_sums[i][3], terms_func[i][3:-1]))
            anims.append(ReplacementTransform(terms_sums[i][4], terms_func[i][-1]))
        self.play(LaggedStart(*anims,lag_ratio = 0.05, run_time = 2), ReplacementTransform(notice12, notice13))
        self.remove(sum_sums).waiting(0, 21) #再把对应的数写到指数的位置上
        self.play(Write(symbol_func))
        self.waiting(1, 1) #母函数就这么出现了
        self.waiting(1, 1) #（空闲）

        surrounding = SurroundingRectangle(solution)
        gossip_1 = MTexText(r"—$P(\pi)$表示什么？").scale(0.5).next_to(4*RIGHT + 0.25*UP)
        gossip_2 = MTexText(r"—什么也不表示。").scale(0.5).next_to(4*RIGHT + 0.25*DOWN)
        gossip_3 = MTexText(r"—$P(x)$的图像什么样？").scale(0.5).next_to(4*RIGHT + 0.75*DOWN)
        gossip_4 = MTexText(r"—不用管，反正没性质。").scale(0.5).next_to(4*RIGHT + 1.25*DOWN)
        gossip_5 = MTexText(r"$\uparrow$但这些都是对的", color = YELLOW).scale(0.5).next_to(4.3*RIGHT + 1.75*DOWN)
        self.play(ShowCreation(surrounding))
        self.waiting(3, 9) #这就是大家会经常听到“x是一个形式记号”的原因
        self.play(Indicate(sloution_mul[0]), Indicate(sloution_mul[3]), Indicate(solution_add[0]), Write(gossip_1), run_time = 1)
        self.play(Write(gossip_2), run_time = 1)
        self.play(Write(gossip_3), run_time = 1)
        self.play(Write(gossip_4), run_time = 1)
        self.waiting(2+1-4, 29+25) #它只是一个为了利用指数运算的性质 而凑出来的标记
        self.waiting(1, 29) #本身没有任何意义
        self.waiting(1, 17) #也不能代值进去
        self.waiting(0, 16) #（空闲）
        
        self.play(ReplacementTransform(notice13, notice14), FadeIn(gossip_5, 0.3*UP))
        self.waiting(1, 18) #但这种说法多少有些颠因为果了
        self.waiting(0, 19) #（空闲）

        self.play(ReplacementTransform(notice14, notice15))
        self.waiting(1, 23) #x不只是一个被凑出来的记号
        self.waiting(2, 3) #它有自己明确的含义
        self.waiting(2, 27) #并且 正是因为它有明确的含义
        self.waiting(2, 6) #我们才能通过一些别的手段
        self.waiting(1, 28) #把母函数硬凑出来

        self.waiting(3, 2)
        self.play(*[FadeOut(mob) for mob in [problem, operation, sum_func, symbol_func, operation_add, operation_mul, symbol_add, symbol_mul, example_operations, example_sum, solution, arrow_fixed_mul, arrow_fixed_add, surrounding, gossip_1, gossip_2, gossip_3, gossip_4, gossip_5, notice15]])
        self.waiting(3, 0) #到此共110秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

###############################################################################

class Chapter2_0(Scene):

    def construct(self):

        text2 = Text("第二节 不同的母函数", font = 'simsun', t2c={"第二节": YELLOW, "不同": GREEN, "母函数": BLUE})

        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))

class Chapter2_1(Scene):
    def construct(self):
        notice1 = Notice("前情提要", "请　复习")
        notice2 = Notice("问题引入", "请　好奇")

        texts = "求集合$\{1, 2, 3, 4, 5\}$", "元素和为8的", "子集", "的个数"
        problem = MTexText("".join(texts), isolate = [*texts, "元素和为8的子集"], tex_to_color_map = number_color_map).scale(0.8).shift(3*UP)
        texts = [r"(\text{不选}"+str(i+1)+r"\ \text{或}\ \text{选}"+str(i+1)+r")" for i in range(5)]
        operation = MTex("".join(texts), isolate = texts, 
            tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"\text{或}": YELLOW}).scale(0.65).next_to(6*LEFT + 2.1*UP)
        operation_terms = [operation.get_part_by_tex(text) for text in texts]
        operation_operations = []
        operation_symbols = []
        for i in range(5):
            operation_operations.append(operation_terms[i][1:4].save_state())
            operation_operations.append(operation_terms[i][5:7].save_state())
            operation_symbols.append(operation_terms[i][0].save_state())
            operation_symbols.append(operation_terms[i][4].save_state())
            operation_symbols.append(operation_terms[i][7].save_state())
        self.play(Write(notice1), FadeIn(problem, 0.5*DOWN))
        self.waiting(1, 21) #先来看看我们在第一节都做了什么吧
        self.waiting(0, 17) #（空闲）

        self.play(Write(operation))
        self.waiting(1, 27) #我们把取出所有子集的操作写成了一个式子

        self.play(LaggedStart(*[ApplyMethod(mob.shift, 0.2*UP, rate_func = there_and_back) for mob in operation_operations], run_time = 2, lag_ratio = 0.2))
        self.waiting(0, 7) #这个式子里面有一些操作
        self.play(LaggedStart(*[ApplyMethod(mob.shift, 0.2*UP, rate_func = there_and_back) for mob in operation_symbols], run_time = 2, lag_ratio = 0.2))
        self.waiting(2, 0) #以及“或”与“和”这两种满足分配率的运算
        self.waiting(0, 21) #（空闲）

        sum_subsets = MTex(r"(1+1)(1+1)(1+1)(1+1)(1+1)", isolate = {r"(1+1)"}).move_to(operation.get_center() + 1.2*DOWN)
        terms_subsets = sum_subsets.get_parts_by_tex(r"(1+1)")
        anims_1 = []
        anims_2 = []
        for i in range(5):
            anims_1.append(TransformFromCopy(operation_terms[i][0], terms_subsets[i][0]))
            anims_2.append(TransformFromCopy(operation_terms[i][1:4], terms_subsets[i][1].set_color(elem_colors[i])))
            anims_1.append(TransformFromCopy(operation_terms[i][4], terms_subsets[i][2].set_color(YELLOW)))
            anims_2.append(TransformFromCopy(operation_terms[i][5:7], terms_subsets[i][3].set_color(elem_colors[i])))
            anims_1.append(TransformFromCopy(operation_terms[i][7], terms_subsets[i][4]))
        copy_sub_sets = sum_subsets.copy() ############这里这么写是因为直接用save_state和restore会出现插值bug，加号不是平移过去的，可能是曲线分段出了问题
        for i in range(5):
            terms_subsets[i].set_x(operation_terms[i].get_x())
        sum_subsets.save_state()
        self.waiting(2, 2) #如果我们想求什么值
        self.play(LaggedStart(*anims_2,lag_ratio = 0.1, run_time = 2))
        self.waiting(0, 20) #就可以把操作替换成对应的量
        self.play(LaggedStart(*anims_1,lag_ratio = 0.1, run_time = 2))
        self.waiting(1, 11) #并且把两种运算替换成加法和乘法
        self.waiting(0, 20) #（空闲）
        sum_subsets.restore() 
        self.play(Transform(sum_subsets, copy_sub_sets))
        self.waiting(2, 10) #两种运算之间的分配律保证了这种替换的成立
        self.waiting(0, 17) #（空闲）

        texts = r"(1+x^{1})", r"(1+x^{2})", r"(1+x^{3})", r"(1+x^{4})", r"(1+x^{5})"
        sum_func = MTex("".join(texts), isolate = texts, tex_to_color_map = {**{r"{"+str(i+1)+r"}": elem_colors[i] for i in range(5)}, r"+": YELLOW}).move_to(operation.get_center() + 1.2*DOWN + 0.5*RIGHT).save_state()
        symbol_func = MTex(r"P(x)=").next_to(sum_func, LEFT)
        terms_func = [sum_func.get_part_by_tex(text) for text in texts]
        anims = []
        for i in range(5):
            anims.append(TransformFromCopy(operation_terms[i][0], terms_func[i][0]))
            anims.append(TransformFromCopy(operation_terms[i][1:4], terms_func[i][1]))
            anims.append(TransformFromCopy(operation_terms[i][4], terms_func[i][2]))
            anims.append(TransformFromCopy(operation_terms[i][5:7], terms_func[i][3:-1]))
            anims.append(TransformFromCopy(operation_terms[i][7], terms_func[i][-1]))
        rectangles = [term_surrounding(term[3:-1]) for term in terms_func]
        self.play(LaggedStart(*anims, lag_ratio = 0.05, run_time = 2), FadeOut(sum_subsets, 1.2*DOWN))
        sum_func.restore()
        self.waiting(0, 5) #如果在用于替换的值中
        self.play(LaggedStart(*[ShowCreation(rect) for rect in rectangles], lag_ratio = 0.3, run_time = 2))
        self.waiting(0, 11) #有一个形式记号x
        self.play(FadeIn(symbol_func, 0.5*RIGHT))
        self.waiting(2, 13) #那么替换完的式子就被称为母函数
        self.waiting(0, 23) #（空闲）

        example_func = MTex(r"(1+x^3)(1+x^5)=1+x^3+x^5+x^{3+5}", isolate = [r"(1+x^3)", r"(1+x^5)", r"+", r"=1+x^3+x^5+x^{3+5}"], tex_to_color_map = {r"+": YELLOW, r"3": elem_colors[2], r"5": elem_colors[4]}).move_to(operation.get_center() + 3*DOWN)
        example_1 = example_func.get_part_by_tex(r"(1+x^3)")
        example_2 = example_func.get_part_by_tex(r"(1+x^5)")
        example_rest = example_func.get_part_by_tex(r"=1+x^3+x^5+x^{3+5}")
        example_adds = example_func.get_parts_by_tex(r"+")
        example_adds[5].set_color(WHITE)
        self.play(TransformFromCopy(terms_func[2], example_1), TransformFromCopy(terms_func[4], example_2), ReplacementTransform(notice1, notice2))
        self.play(Write(example_rest), run_time = 2)
        self.waiting(1, 2) #这个形式记号的作用是把乘法变回加法

        arrow_1 = Arrow(example_adds[2].get_center() + 0.8*DOWN, example_adds[2].get_center() + 0.4*DOWN, buff = 0, color = YELLOW)
        arrow_2 = Arrow(example_adds[3].get_center() + 0.8*DOWN, example_adds[3].get_center() + 0.4*DOWN, buff = 0, color = YELLOW)
        arrow_3 = Arrow(example_adds[4].get_center() + 0.8*DOWN, example_adds[4].get_center() + 0.4*DOWN, buff = 0, color = YELLOW)
        formal_add = Text("满足分配律的形式记号", font = "simsun", color = YELLOW).scale(0.4).shift(example_adds[3].get_center() + 1.1*DOWN).add(arrow_1, arrow_2, arrow_3)
        arrow_4 = Arrow(example_adds[5].get_center() + 0.7*UP, example_adds[5].get_center() + 0.3*UP, buff = 0)
        real_add = Text("确实是加法，把两个元素加起来", font = "simsun").scale(0.4).shift(example_adds[5].get_center() + 1.0*UP).add(arrow_4)
        self.play(FadeIn(formal_add, 0.3*UP, rate_func = squish_rate_func(smooth, 0, 2/3)), FadeIn(real_add, 0.3*DOWN, rate_func = squish_rate_func(smooth, 1/3, 1)))
        self.waiting(3, 5) #但这样一来 式子中就有两个名为加法的东西了
        self.waiting(0, 17) #（空闲）

        self.waiting(2, 11) #有什么办法解决这个问题吗
        self.waiting(0, 21) #（空闲）

        text_operation = Text("操作：", font = "simsun").scale(0.6).next_to(6*LEFT + 2.1*UP, LEFT, buff = 0.1)
        text_operator = Text("影响：", font = "simsun").scale(0.6).next_to(6*LEFT + 0.9*UP, LEFT, buff = 0.1)
        self.play(Write(text_operation), Write(text_operator), *[FadeOut(mob, 0.5*DOWN) for mob in [sum_func, symbol_func, *rectangles, example_func, formal_add, real_add]])
        self.waiting(2, 29) #这就要看看每一步选择对于元素和的影响了
        
        texts = [r"(\text{加}0\ \text{或}\ \text{加}"+str(i+1)+r")" for i in range(5)]
        operator = MTex("".join(texts), isolate = texts, 
            tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"\text{或}": YELLOW}).scale(0.65).next_to(6*LEFT + 0.9*UP).save_state()
        operator_terms = [operator.get_part_by_tex(texts[i]).next_to(operation_terms[i].get_corner(RIGHT) + 1.2*DOWN, LEFT, buff = 0) for i in range(5)]
        rect_1 = term_surrounding(operation_operations[1])
        rect_2 = term_surrounding(operation_operations[0])
        operator_remain = VGroup(operator_terms[0][0], operator_terms[0][3], operator_terms[0][6])
        self.play(ShowCreation(rect_1))
        self.waiting(1, 8) #如果这个子集包含1
        self.play(FadeTransform(rect_1, operator_terms[0][4:6], stretch = False))
        self.waiting(1, 23) #它所有元素的和就会增加1
        self.play(ShowCreation(rect_2))
        self.waiting(1, 1) #而它如果不包含1
        self.play(FadeTransform(rect_2, operator_terms[0][1:3], stretch = False))
        self.waiting(1, 21) #所有元素的和就会增加0
        self.waiting(3, 18) #这两种影响是两个对于元素和的不同操作
        self.play(Write(operator_remain))
        self.waiting(1, 29) #仍然应该用“或”运算连接起来
        anims = []
        for i in range(1, 5):
            anims.append(FadeTransform(operation_terms[i][0].copy(), operator_terms[i][0]))
            anims.append(FadeTransform(operation_terms[i][1:4].copy(), operator_terms[i][1:3]))
            anims.append(FadeTransform(operation_terms[i][4].copy(), operator_terms[i][3]))
            anims.append(FadeTransform(operation_terms[i][5:7].copy(), operator_terms[i][4:6]))
            anims.append(FadeTransform(operation_terms[i][7].copy(), operator_terms[i][6]))
        self.play(LaggedStart(*anims, lag_ratio = 0.05, run_time = 2))
        self.waiting(1, 1) #别的四个元素也是一样的处理方法
        self.play(operator.animate.restore())
        self.waiting(2, 11) #不同括号之间仍然是用“和”运算连接起来
        self.waiting(0, 28) #到此共75秒


        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_2(Scene):
    def construct(self):
        notice2 = Notice("问题引入", "请　好奇")
        notice3 = Notice("良好性质", "请　利用")
        notice4 = Notice("十分相似", "请注意到")
        notice5 = Notice("细节处理", "请　模仿")
        notice6 = Notice("我只想当", "县长夫人")

        texts = "求集合$\{1, 2, 3, 4, 5\}$", "元素和为8的", "子集", "的个数"
        problem = MTexText("".join(texts), isolate = [*texts, "元素和为8的子集"], tex_to_color_map = number_color_map).scale(0.8).shift(3*UP)
        texts = [r"(\text{不选}"+str(i+1)+r"\ \text{或}\ \text{选}"+str(i+1)+r")" for i in range(5)]
        operation = MTex("".join(texts), isolate = texts, 
            tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"\text{或}": YELLOW}).scale(0.65).next_to(6*LEFT + 2.1*UP)
        operation_terms = [operation.get_part_by_tex(text) for text in texts]
        texts = [r"(\text{加}0\ \text{或}\ \text{加}"+str(i+1)+r")" for i in range(5)]
        operator = MTex("".join(texts), isolate = texts, 
            tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"\text{或}": YELLOW}).scale(0.65).next_to(6*LEFT + 0.9*UP)
        operator_terms = [operator.get_part_by_tex(texts[i]) for i in range(5)]
        text_operation = Text("操作：", font = "simsun").scale(0.6).next_to(6*LEFT + 2.1*UP, LEFT, buff = 0.1)
        text_operator = Text("影响：", font = "simsun").scale(0.6).next_to(6*LEFT + 0.9*UP, LEFT, buff = 0.1)
        
        self.add(notice2, problem, operation, operator, text_operation, text_operator)
        self.play(ReplacementTransform(notice2, notice3))
        self.waiting(2, 5) #虽然这个新式子也是由操作构成的

        example_add = MTex(r"\text{加}1\text{加}2=\text{加}3", isolate = [r"\text{加}1", r"\text{加}2", r"=\text{加}3"], tex_to_color_map = {r"\text{加}1": elem_colors[0], r"\text{加}2": elem_colors[1], r"\text{加}3": interpolate_color(BLUE_B, BLUE_D, 1/8)}).scale(0.8).shift(0.3*DOWN + 3*LEFT)
        term_1 = example_add.get_part_by_tex(r"\text{加}1")
        term_2 = example_add.get_part_by_tex(r"\text{加}2")
        term_3 = example_add.get_part_by_tex(r"=\text{加}3")
        self.play(TransformFromCopy(operator_terms[0][4:6], term_1), TransformFromCopy(operator_terms[1][4:6], term_2))
        self.play(Write(term_3))
        self.waiting(0, 13) #但它和原来的操作式不一样
        self.waiting(0, 18) #（空闲）
        
        texts = r"(\text{加}0\ \text{或}\ \text{加}1\ \text{或}\ \text{加}2\ \text{或}\ \text{加}3)", r"(\text{加}0\ \text{或}\ \text{加}3)", r"(\text{加}0\ \text{或}\ \text{加}4)", r"(\text{加}0\ \text{或}\ \text{加}5)"
        first_row = MTex("".join(texts), isolate = texts, tex_to_color_map = {texts[0]: interpolate_color(BLUE_B, BLUE_D, 1/8), texts[1]: elem_colors[2], texts[2]: elem_colors[3], texts[3]: elem_colors[4], (r"(", r")"): WHITE, r"\text{或}": YELLOW}).scale(0.65).next_to(6.1*LEFT + 0.3*UP)
        first_equal = MTex("=").scale(0.65).next_to(6*LEFT + 0.3*UP, LEFT, buff = 0).add(*first_row.submobjects)
        texts = r"(\text{加}0\ \text{或}\ \text{加}1\ \text{或}\ \text{加}2\ \text{或}\ {2}\text{加}3\ \text{或}\ \text{加}4\ \text{或}\ \text{加}5\ \text{或}\ \text{加}6)", r"(\text{加}0\ \text{或}\ \text{加}4)", r"(\text{加}0\ \text{或}\ \text{加}5)"
        second_row = MTex("".join(texts), isolate = texts, tex_to_color_map = {texts[0]: elem_colors[1], texts[1]: elem_colors[3], texts[2]: elem_colors[4], (r"(", r")", r"{2}"): WHITE, r"\text{或}": YELLOW}).scale(0.65).next_to(6.3*LEFT + 0.3*DOWN)
        second_equal = MTex("=").scale(0.65).next_to(6.2*LEFT + 0.3*DOWN, LEFT, buff = 0).add(*second_row.submobjects)
        texts = r"(\text{加}0\ \text{或}\ \text{加}1\ \text{或}\ \text{加}2\ \text{或}\ {2}\text{加}3\ \text{或}\ {2}\text{加}4\ \text{或}\ {2}\text{加}5\ \text{或}\ {2}\text{加}6\ \text{或}\ {2}\text{加}7\ \text{或}\ \text{加}8\ \text{或}\ \text{加}9\ \text{或}\ \text{加}10)", r"(\text{加}0\ \text{或}\ \text{加}5)"
        third_row = MTex("".join(texts), isolate = texts, tex_to_color_map = {texts[0]: interpolate_color(BLUE_B, BLUE_D, 3/8), texts[1]: elem_colors[4], (r"(", r")", r"{2}"): WHITE, r"\text{或}": YELLOW}).scale(0.6).next_to(6.5*LEFT + 0.9*DOWN)
        third_equal = MTex("=").scale(0.65).next_to(6.4*LEFT + 0.9*DOWN, LEFT, buff = 0).add(*third_row.submobjects)
        texts = r"\text{加}0", r"\text{加}1", r"\text{加}2", r"{2}\text{加}3", r"{2}\text{加}4", r"{3}\text{加}5", r"{3}\text{加}6", r"{3}\text{加}7", r"{3}\text{加}8", r"{3}\text{加}9", r"{3}\text{加}10", r"{2}\text{加}11", r"{2}\text{加}12", r"\text{加}13", r"\text{加}14", r"\text{加}15"
        without_coefficients = [r"\text{加}"+str(i) for i in range(16)]
        final_row = MTex(r"\ \text{或}\ ".join(texts), color = elem_colors[2], isolate = without_coefficients, tex_to_color_map = {(r"{2}", r"{3}"): WHITE, r"\text{或}": YELLOW}).scale(0.45).next_to(6.7*LEFT + 1.5*DOWN)
        final_terms = [final_row.get_part_by_tex(text) for text in without_coefficients]
        final_2s = final_row.get_parts_by_tex(r"{2}")
        final_3s = final_row.get_parts_by_tex(r"{3}")
        final_adds = final_row.get_parts_by_tex(r"\text{或}")
        final_equal = MTex("=").scale(0.65).next_to(6.6*LEFT + 1.5*DOWN, LEFT, buff = 0).add(*final_row.submobjects)
        self.play(Write(first_equal), example_add.animate.shift(0.45*DOWN).set_opacity(0.75))
        self.wait(1.5)
        self.play(Write(second_equal), example_add.animate.shift(0.45*DOWN).set_opacity(0.5))
        self.wait(1.5)
        self.play(Write(third_equal), example_add.animate.shift(0.45*DOWN).set_opacity(0.25))
        self.wait(1.5)
        self.play(Write(final_equal), FadeOut(example_add, 0.45*DOWN))
        self.waiting(3+2+2+0+5-12.5, 2+14+23+15) #两个加操作可以合成成一个加操作 于是新式子在展开以后 还可以接着化简 再合并同类项 （空闲）
        
        self.play(ReplacementTransform(notice3, notice4), FadeOut(third_equal, rate_func = squish_rate_func(smooth, 0, 0.3)), FadeOut(second_equal, rate_func = squish_rate_func(smooth, 0, 0.6)), FadeOut(first_equal, rate_func = squish_rate_func(smooth, 0, 0.9)), ApplyMethod(final_equal.shift, 1.8*UP, rate_func = squish_rate_func(smooth, 0.1, 1)), run_time = 1)
        self.waiting(2, 12) #最后 我们会得到一个眼熟的结果

        generating_func = MTex(r"x^0+x^1+x^2+{2}x^3+{2}x^4+{3}x^5+{3}x^6+{3}x^7+{3}x^8+{3}x^9+{3}x^{10}+{2}x^{11}+{2}x^{12}+x^{13}+x^{14}+x^{15}", isolate = [r"+"], tex_to_color_map = {r"x": elem_colors[2], r"+": YELLOW}).scale(0.63).next_to(6.7*LEFT + 1.2*DOWN)
        function_adds = generating_func.get_parts_by_tex(r"+")
        texts = [r"(1+x^"+str(i+1)+r")" for i in range(5)]
        factored_func = MTex(r"".join(texts), tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"+": YELLOW}).scale(0.8).shift(1.95*DOWN)
        terms_func = [factored_func.get_part_by_tex(text) for text in texts]
        self.play(FadeIn(generating_func, 0.3*UP, lag_ratio = 0.1, run_time = 3), Write(factored_func, rate_func = squish_rate_func(smooth, 1/6, 5/6)))
        self.waiting(0, 6) #它和母函数的展开式几乎一模一样

        texts = r"\text{加}1^0", r"\text{加}1^1", r"\text{加}1^2", r"{2}\text{加}1^3", r"{2}\text{加}1^4", r"{3}\text{加}1^5", r"{3}\text{加}1^6", r"{3}\text{加}1^7", r"{3}\text{加}1^8", r"{3}\text{加}1^9", r"{3}\text{加}1^{10}", r"{2}\text{加}1^{11}", r"{2}\text{加}1^{12}", r"\text{加}1^{13}", r"\text{加}1^{14}", r"\text{加}1^{15}"
        without_coefficients = [r"\text{加}1^"+str(i) for i in range(10)] + [r"\text{加}1^{"+str(i)+r"}" for i in range(10, 16)]
        generate_ver = MTex(r"\ \text{或}\ ".join(texts), isolate = [*texts, r"{2}", r"{3}", *without_coefficients], tex_to_color_map = {r"\text{加}1": elem_colors[2], r"\text{或}": YELLOW}).scale(0.42).shift(0.45*DOWN)
        generate_terms = [generate_ver.get_part_by_tex(text) for text in without_coefficients]
        generate_2s = generate_ver.get_parts_by_tex(r"{2}")
        generate_3s = generate_ver.get_parts_by_tex(r"{3}")
        generate_adds = generate_ver.get_parts_by_tex(r"\text{或}")
        generate_equal = MTex(r"=").scale(0.65).next_to(generate_ver, LEFT, buff = 0.1)
        anims = [ReplacementTransform(MTex("=").scale(0.65).next_to(6.6*LEFT + 0.3*UP, LEFT, buff = 0), generate_equal)]
        j, k = 0, 0
        for i in range(16):
            if i == 3 or i == 4 or i == 11 or i == 12:
                anims.append(TransformFromCopy(final_2s[j], generate_2s[j]))
                j += 1
            elif 5 <= i and 10 >= i:
                anims.append(TransformFromCopy(final_3s[k], generate_3s[k]))
                k += 1
            anims.append(TransformFromCopy(final_terms[i], generate_terms[i]))
            if i < 15:
                anims.append(TransformFromCopy(final_adds[i], generate_adds[i]))
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2))
        self.waiting(1, 6) #这是因为 加操作既然可以合成
        self.waiting(3, 27) #自然就可以反过来分解成一个个加一
        
        isomorphism_x = MTex(r"x \Leftrightarrow \text{加}1", tex_to_color_map = {(r"x", r"\text{加}1"): elem_colors[2]}).scale(0.8).shift(1.2*UP)
        surrounding_x = SurroundingRectangle(isomorphism_x)
        equal = MTex(r"\Leftrightarrow").scale(0.63).next_to(generating_func[0], LEFT)
        self.play(FadeOut(final_equal, 0.3*DOWN), operator.animate.shift(0.6*DOWN), text_operator.animate.shift(0.6*DOWN))
        self.waiting(0, 19) #这些加一的操作
        self.play(ShowCreation(surrounding_x), Write(isomorphism_x), Write(equal))
        self.waiting(1, 14) #就是形式记号x的本来面目
        self.waiting(0, 23) #（空闲）

        isomorphism_add = MTex(r"+ \Leftrightarrow \text{或}", tex_to_color_map = {(r"+", r"\text{或}"): elem_colors[2]}).scale(0.8).shift(1.2*UP + 3*LEFT)
        surrounding_add = SurroundingRectangle(isomorphism_add)
        isomorphism_mul = MTex(r"\times \Leftrightarrow \text{和}", tex_to_color_map = {(r"\times", r"\text{和}"): elem_colors[2]}).scale(0.8).shift(1.2*UP + 3*RIGHT)
        surrounding_mul = SurroundingRectangle(isomorphism_mul)
        symbols_operator = []
        symbols_function = []
        for i in range(5):
            symbols_operator.append(operator_terms[i][0])
            symbols_operator.append(operator_terms[i][3])
            symbols_operator.append(operator_terms[i][6])
            symbols_function.append(terms_func[i][0])
            symbols_function.append(terms_func[i][2])
            symbols_function.append(terms_func[i][-1])
        self.play(ReplacementTransform(notice4, notice5))
        self.waiting(1, 27) #当然 细心的观众可能会发现
        self.play(FadeIn(isomorphism_add, LEFT), FadeIn(isomorphism_mul, RIGHT))
        self.waiting(1, 23) #两个式子中的运算是不一样的
        self.play(LaggedStart(*[ApplyMethod(mob.shift, 0.2*UP, rate_func = there_and_back) for mob in symbols_function], run_time = 2, lag_ratio = 0.2), 
            LaggedStart(*[ApplyMethod(mob.shift, 0.2*UP, rate_func = there_and_back) for mob in function_adds], run_time = 2, lag_ratio = 0.2))
        self.waiting(0, 5) #一边是加法与乘法
        self.play(LaggedStart(*[ApplyMethod(mob.shift, 0.2*UP, rate_func = there_and_back) for mob in symbols_operator], run_time = 2, lag_ratio = 0.2), 
            LaggedStart(*[ApplyMethod(mob.shift, 0.2*UP, rate_func = there_and_back) for mob in generate_adds], run_time = 2, lag_ratio = 0.2))
        self.waiting(1, 12) #而另一边是“或”运算与“和”运算

        self.play(ReplacementTransform(notice5, notice6))
        self.waiting(2, 1) #但名称的不同不会带来什么影响
        self.waiting(1, 16) #在计算过程中
        self.waiting(3, 14) #我们只需要一种运算对另一种运算的分配律
        self.waiting(3, 6) #以及它们分别的交换律 结合律而已
        self.waiting(0, 15) #（空闲）
        self.waiting(2, 28) #至于运算具体是什么 那不重要
        self.waiting(0, 18) #（空闲）
        self.play(ShowCreation(surrounding_add), ShowCreation(surrounding_mul))
        self.waiting(1, 13) #两个式子中出现的这两对运算
        self.waiting(3, 22) #除了名字有区别 完全是同构的
        self.waiting(1, 24) #只要再把记号改一改
        self.waiting(2, 7) #（空闲）
        self.waiting(0, 22) #到此共(71+5)=76秒

        print(self.num_plays, self.time-5)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter2_3(Scene):
    def construct(self):
        notice6 = Notice("我只想当", "县长夫人")
        notice7 = Notice("本节总结", "请　复习")
        notice8 = Notice("拓展内容", "请　加餐")

        texts = "求集合$\{1, 2, 3, 4, 5\}$", "元素和为8", "的子集的个数"
        problem = MTexText("".join(texts), isolate = texts, tex_to_color_map = number_color_map).scale(0.8).shift(3*UP)
        texts = [r"(\text{不选}"+str(i+1)+r"\ \text{或}\ \text{选}"+str(i+1)+r")" for i in range(5)]
        operation = MTex("".join(texts), isolate = texts, 
            tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"\text{或}": YELLOW}).scale(0.65).next_to(6*LEFT + 2.1*UP)
        operation_terms = [operation.get_part_by_tex(text) for text in texts]
        texts = [r"(\text{加}0\ \text{或}\ \text{加}"+str(i+1)+r")" for i in range(5)]
        operator = MTex("".join(texts), isolate = texts, 
            tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"\text{或}": YELLOW}).scale(0.65).next_to(6*LEFT + 0.3*UP)
        operator_terms = [operator.get_part_by_tex(texts[i]) for i in range(5)]
        text_operation = Text("操作：", font = "simsun").scale(0.6).next_to(6*LEFT + 2.1*UP, LEFT, buff = 0.1)
        text_operator = Text("影响：", font = "simsun").scale(0.6).next_to(6*LEFT + 0.3*UP, LEFT, buff = 0.1)
        text_number = Text("（元素数）", font = "simsun").scale(0.3).next_to(text_operator, UP, buff = 0.1)

        isomorphism_x = MTex(r"x \Leftrightarrow \text{加}1", tex_to_color_map = {(r"x", r"\text{加}1"): elem_colors[2]}).scale(0.8).shift(1.2*UP)
        surrounding_x = SurroundingRectangle(isomorphism_x)
        isomorphism_add = MTex(r"+ \Leftrightarrow \text{或}", tex_to_color_map = {(r"+", r"\text{或}"): elem_colors[2]}).scale(0.8).shift(1.2*UP + 3*LEFT)
        surrounding_add = SurroundingRectangle(isomorphism_add)
        isomorphism_mul = MTex(r"\times \Leftrightarrow \text{和}", tex_to_color_map = {(r"\times", r"\text{和}"): elem_colors[2]}).scale(0.8).shift(1.2*UP + 3*RIGHT)
        surrounding_mul = SurroundingRectangle(isomorphism_mul)
        isomorphism = VGroup(isomorphism_x, surrounding_x, isomorphism_add, surrounding_add, isomorphism_mul, surrounding_mul)
        
        texts = r"\text{加}1^0", r"\text{加}1^1", r"\text{加}1^2", r"{2}\text{加}1^3", r"{2}\text{加}1^4", r"{3}\text{加}1^5", r"{3}\text{加}1^6", r"{3}\text{加}1^7", r"{3}\text{加}1^8", r"{3}\text{加}1^9", r"{3}\text{加}1^{10}", r"{2}\text{加}1^{11}", r"{2}\text{加}1^{12}", r"\text{加}1^{13}", r"\text{加}1^{14}", r"\text{加}1^{15}"
        generate_ver = MTex(r"\ \text{或}\ ".join(texts), isolate = texts, tex_to_color_map = {r"\text{加}1": elem_colors[2], r"\text{或}": YELLOW}).scale(0.42).shift(0.45*DOWN)
        generate_equal = MTex(r"=").scale(0.65).next_to(generate_ver, LEFT, buff = 0.1)
        
        generating_func = MTex(r"x^0+x^1+x^2+{2}x^3+{2}x^4+{3}x^5+{3}x^6+{3}x^7+{3}x^8+{3}x^9+{3}x^{10}+{2}x^{11}+{2}x^{12}+x^{13}+x^{14}+x^{15}", isolate = [r"+"], tex_to_color_map = {r"x": elem_colors[2], r"+": YELLOW}).scale(0.63).next_to(6.7*LEFT + 1.2*DOWN)
        equal = MTex(r"\Leftrightarrow").scale(0.63).next_to(generating_func[0], LEFT)
        texts = [r"(1+x^"+str(i+1)+r")" for i in range(5)]
        factored_func = MTex(r"".join(texts), tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"+": YELLOW}).scale(0.8).shift(1.95*DOWN)
        facotred_terms = [factored_func.get_part_by_tex(text) for text in texts]

        self.add(notice6, problem, operation, operator, text_operation, text_operator, isomorphism, generate_ver, generate_equal, generating_func, equal, factored_func)
        self.play(FadeOut(isomorphism), FadeOut(generate_ver, 0.15*UP), FadeOut(generate_equal, 0.15*UP), FadeOut(generating_func, 0.3*UP), FadeOut(equal, 0.3*UP), factored_func.animate.shift(0.45*UP), ReplacementTransform(notice6, notice7))
        self.waiting(0, 25) #这就是母函数的由来
        self.waiting(0, 17) #（空闲）

        self.play(LaggedStart(*[ApplyMethod(mob.shift, 0.2*UP, rate_func = there_and_back) for mob in problem], lag_ratio = 0.1, run_time = 2))
        self.waiting(1+2-2, 24+4) #对于一个计数问题 我们在操作式的基础上

        operators_copy = []
        anims = []
        for i in range(5):
            operator_1 = operator_terms[i][1:3].copy().move_to(operation_terms[i][1:4].get_center() + 0.6*DOWN)
            operator_2 = operator_terms[i][4:6].copy().move_to(operation_terms[i][5:7].get_center() + 0.6*DOWN)
            anim_1 = TransformFromCopy(operation_terms[i][1:4], operator_1)
            anim_2 = TransformFromCopy(operation_terms[i][5:7], operator_2)
            operators_copy.append(operator_1)
            operators_copy.append(operator_2)
            anims.append(anim_1)
            anims.append(anim_2)
        self.play(LaggedStart(*anims, lag_ratio = 0.2, run_time = 2))
        self.waiting(1, 17) #找到每一个操作对我们关心的东西的影响
        anims = []
        for i in range(5):
            anims.append(Transform(operators_copy[2*i], operator_terms[i][1:3], remover = True))
            anims.append(Transform(operators_copy[2*i+1], operator_terms[i][4:6], remover = True))
        self.waiting(0, 28) #接着......
        self.play(LaggedStart(*anims, lag_ratio = 0.3, run_time = 2))
        self.waiting(2+2-2, 17+17-28) #......把式子中的操作 依次替换成对应的影响

        texts = [r"(\text{加}1^0\ \text{或}\ \text{加}1^"+str(i+1)+r")" for i in range(5)]
        operator_function = MTex(r"".join(texts), isolate = texts, tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"\text{或}": YELLOW}).scale(0.65).next_to(6*LEFT + 0.6*DOWN)
        operator_function_terms = [operator_function.get_part_by_tex(text) for text in texts]
        anims_1 = []
        anims_2 = []
        for i in range(5):
            position_1 = operator_function_terms[i][1:4].get_x()
            position_2 = operator_function_terms[i][5:8].get_x()
            anims_1.append(TransformFromCopy(operator_terms[i][0], operator_function_terms[i][0]))
            anims_2.append(TransformFromCopy(operator_terms[i][1:3], operator_function_terms[i][1:4].set_x(operator_terms[i][1:3].get_x())))
            anims_1.append(ApplyMethod(operator_function_terms[i][1:4].set_x, position_1))
            anims_1.append(TransformFromCopy(operator_terms[i][3], operator_function_terms[i][4]))
            anims_2.append(TransformFromCopy(operator_terms[i][4:6], operator_function_terms[i][5:8].set_x(operator_terms[i][4:6].get_x())))
            anims_1.append(ApplyMethod(operator_function_terms[i][5:8].set_x, position_2))
            anims_1.append(TransformFromCopy(operator_terms[i][6], operator_function_terms[i][8]))
        self.play(LaggedStart(*anims_2, lag_ratio = 0.2, run_time = 2))
        self.waiting(1, 24) #如果这些影响都可以化简成某一个小步骤的复合
        self.play(LaggedStart(*anims_1, lag_ratio = 0.03, run_time = 2))
        self.waiting(1, 21) #那么整个式子 就也可以写成这个小步骤的复合
        self.waiting(0, 20) #（空闲）
        anims = []
        for i in range(5):
            anims.append(TransformFromCopy(operator_function_terms[i][0], facotred_terms[i][0].copy(), remover = True))
            anims.append(TransformFromCopy(operator_function_terms[i][1:4], facotred_terms[i][1].copy(), remover = True))
            anims.append(TransformFromCopy(operator_function_terms[i][4], facotred_terms[i][2].copy(), remover = True))
            anims.append(TransformFromCopy(operator_function_terms[i][5:8], facotred_terms[i][3:5].copy(), remover = True))
            anims.append(TransformFromCopy(operator_function_terms[i][8], facotred_terms[i][5].copy(), remover = True))
        self.play(LaggedStart(*anims, lag_ratio = 0.05, run_time = 2))
        self.waiting(1+2-2, 22+5) #再改变一下记号 我们就得到了需要的母函数
        self.waiting(0, 20) #（空闲）

        self.waiting(1, 25) #这个方法的正确性
        self.play(ShowCreation(surrounding_x), ShowCreation(surrounding_add), ShowCreation(surrounding_mul), Write(isomorphism_x), Write(isomorphism_add), Write(isomorphism_mul))
        self.waiting(2, 3) #是因为“或”与“和”这两种运算
        self.waiting(3, 4) #和“加法”与“乘法”这两种运算同构
        self.waiting(0, 26) #（空闲）

        self.play(ReplacementTransform(notice7, notice8))
        self.waiting(1, 4) #随着我们关心的问题不同
        self.waiting(2, 17) #母函数自然也会产生改变
        self.waiting(5, 8) #比如 现在这个函数可以告诉我们元素和为8的子集的个数
        texts = "求集合$\{1, 2, 3, 4, 5\}$", "有3个元素", "的子集的个数"
        problem_replace = MTexText("".join(texts), isolate = texts, tex_to_color_map = {**number_color_map, r"有3个元素": WHITE}).scale(0.8).shift(3*UP)
        self.play(ReplacementTransform(problem, problem_replace), *[FadeOut(mob) for mob in [operator, isomorphism, operator_function, factored_func]])
        self.waiting(2, 11) #但它没办法告诉我们有3个元素的子集的个数
        self.waiting(0, 17) #（空闲）

        self.play(Write(text_number))
        self.waiting(2, 1) #计算这个值需要一个新的母函数
        self.waiting(2, 8) #我们仍然从操作式出发

        operator_raplace = MTex(r"(\text{加}0\ \text{或}\ \text{加}1)(\text{加}0\ \text{或}\ \text{加}1)(\text{加}0\ \text{或}\ \text{加}1)(\text{加}0\ \text{或}\ \text{加}1)(\text{加}0\ \text{或}\ \text{加}1)", isolate = r"(\text{加}0\ \text{或}\ \text{加}1)").scale(0.65).next_to(6*LEFT + 0.3*UP)
        operator_raplace_terms = operator_raplace.get_parts_by_tex(r"(\text{加}0\ \text{或}\ \text{加}1)")
        anims = []
        remain = VGroup()
        for i in range(5):
            operator_raplace_terms[i][1:3].set_color(elem_colors[i])
            operator_raplace_terms[i][3].set_color(YELLOW)
            operator_raplace_terms[i][4:6].set_color(elem_colors[i])
            if i >= 1:
                anims.append(TransformFromCopy(operation_terms[i][1:4], operator_raplace_terms[i][1:3]))
                anims.append(TransformFromCopy(operation_terms[i][5:7], operator_raplace_terms[i][4:6]))
            remain.add(operator_raplace_terms[i][0], operator_raplace_terms[i][3], operator_raplace_terms[i][6])
        offset = operator_raplace_terms[0][4:6].get_center() - (operation_terms[0][5:7].get_center() + 0.9*DOWN)
        self.play(TransformFromCopy(operation_terms[0][5:7], operator_raplace_terms[0][4:6].shift(-offset)))
        self.waiting(1, 16) #这次 把1加入子集
        self.play(operator_raplace_terms[0][4:6].animate.shift(offset))
        self.waiting(1, 8) #会让最终的结果加1
        self.play(TransformFromCopy(operation_terms[0][1:4], operator_raplace_terms[0][1:3]))
        self.waiting(2, 6) #不加入子集则会让最终的结果加0
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2), Write(remain, lag_ratio = 0.1, run_time = 2))
        self.waiting(0, 2) #其它四个式子也是一样的
        self.waiting(0, 19) #（空闲）

        operator_function_raplace = MTex(r"(\text{加}1^0\ \text{或}\ \text{加}1^1)(\text{加}1^0\ \text{或}\ \text{加}1^1)(\text{加}1^0\ \text{或}\ \text{加}1^1)(\text{加}1^0\ \text{或}\ \text{加}1^1)(\text{加}1^0\ \text{或}\ \text{加}1^1)", isolate = r"(\text{加}1^0\ \text{或}\ \text{加}1^1)").scale(0.65).next_to(6*LEFT + 0.6*DOWN)
        operator_function_raplace_terms = operator_function_raplace.get_parts_by_tex(r"(\text{加}1^0\ \text{或}\ \text{加}1^1)")
        anims = []
        for i in range(5):
            anims.append(TransformFromCopy(operator_raplace_terms[i][0], operator_function_raplace_terms[i][0]))
            anims.append(TransformFromCopy(operator_raplace_terms[i][1:3], operator_function_raplace_terms[i][1:4].set_color(elem_colors[i])))
            anims.append(TransformFromCopy(operator_raplace_terms[i][3], operator_function_raplace_terms[i][4].set_color(YELLOW)))
            anims.append(TransformFromCopy(operator_raplace_terms[i][4:6], operator_function_raplace_terms[i][5:8].set_color(elem_colors[i])))
            anims.append(TransformFromCopy(operator_raplace_terms[i][6], operator_function_raplace_terms[i][8]))
        self.play(LaggedStart(*anims, lag_ratio = 0.05, run_time = 2))
        self.waiting(0, 29) #再把写出来的式子的记号替换一下

        function_raplace = MTex(r"({1}+x)^{12345}", tex_to_color_map = {(r"{1}", r"x"): elem_colors[2], r"+": YELLOW}).scale(0.8)
        height = function_raplace[5].get_height()
        position = function_raplace[5].get_center()
        for i in range(6, 10):
            function_raplace[i].set_height(height).move_to(position)
        function_raplace.refresh_bounding_box().move_to(1.8*DOWN)
        alpha = ValueTracker(0.0)
        def power_updater(mob: VMobject):
            value = alpha.get_value()
            if value < 0.5:
                mob.set_opacity(0)
            elif value < 5/8:
                mob.set_opacity(1)
            elif value < 3/4:
                mob.become(function_raplace[6])
            elif value < 7/8:
                mob.become(function_raplace[7])
            elif value <1:
                mob.become(function_raplace[8])
            else:
                mob.become(function_raplace[9])
        function_raplace[5].add_updater(power_updater)
        anims = []
        for i in range(5):
            anim_i = []
            anim_i.append(TransformFromCopy(operator_function_raplace_terms[i][0], function_raplace[0].copy(), remover = True))
            anim_i.append(TransformFromCopy(operator_function_raplace_terms[i][1:4], function_raplace[1].copy(), remover = True))
            anim_i.append(TransformFromCopy(operator_function_raplace_terms[i][4], function_raplace[2].copy(), remover = True))
            anim_i.append(TransformFromCopy(operator_function_raplace_terms[i][5:8], function_raplace[3].copy(), remover = True))
            anim_i.append(TransformFromCopy(operator_function_raplace_terms[i][8], function_raplace[4].copy(), remover = True))
            anims.append(AnimationGroup(*anim_i))
        self.add(function_raplace[5]).play(LaggedStart(*anims, lag_ratio = 0.25), alpha.animate.set_value(1), run_time = 2)
        function_raplace.clear_updaters()
        self.add(function_raplace[0:5])
        self.waiting(0, 18) #我们就能得到一个很眼熟的结果
        self.waiting(1, 20) #一个二项式

        expanded = MTex(r"={1}+5x+10x^2+{10}x^3+5x^4+x^5", isolate = [r"{10}"], tex_to_color_map = {(r"{1}", r"x"): elem_colors[2], r"+":YELLOW}).scale(0.8).move_to(2.4*DOWN)
        needed = expanded.get_part_by_tex(r"{10}")
        surrounding = term_surrounding(needed)
        self.play(Write(expanded))
        self.play(ShowCreation(surrounding))
        self.waiting(1, 3) #也就是说 这个母函数告诉了我们这么一件事
        self.waiting(3, 12) #每一个组合数 都是二项式的对应系数
        self.waiting(3, 20)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.waiting(3, 0) #到此共89秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

###############################################################################

class Chapter3_0(Scene):

    def construct(self):

        text3 = Text("第三节 数列", font = 'simsun', t2c={"第三节": YELLOW, "数列": GREEN})

        self.play(Write(text3))
        self.wait(1)
        self.play(FadeOut(text3))

class Chapter3_1(Scene):
    def construct(self):
        notice1 = Notice("前情提要", "请　复习")
        notice2 = Notice("现象引入", "请　好奇")
        notice3 = Notice("简单计算", "请　显然")

        problem = MTexText("求集合$\{1, 2, 3, 4, 5\}$元素和为8的子集的个数", tex_to_color_map = number_color_map).scale(0.8).shift(3*UP)
        texts = [r"(1+x^"+str(i+1)+r")" for i in range(5)]
        factored_func = MTex(r"".join(texts), tex_to_color_map = {**{texts[i]: elem_colors[i] for i in range(5)}, (r"(", r")"): WHITE, r"+": YELLOW}).scale(0.8).shift(2.1*UP)
        shade = Rectangle(height = FRAME_HEIGHT, width = FRAME_WIDTH, fill_opacity = 1, fill_color = BACK, stroke_width = 0)
        shade_in_proportion = Rectangle(height = FRAME_WIDTH/4*3, width = FRAME_WIDTH, fill_opacity = 1, fill_color = BACK, stroke_width = 0)
        self.play(Write(notice1), Write(problem), Write(factored_func))
        self.waiting(1, 19) #至此 组合计数问题中母函数的由来
        self.waiting(1, 23) #我们已经十分清楚了
        self.waiting(0, 14) #（空闲）

        rect_shade = shade_in_proportion.copy().add(problem, factored_func)

        rectangle = Rectangle(height = 1, width = 4/3, fill_opacity = 1, stroke_width = 0)
        rectangles = []
        alpha = ValueTracker(0.0)
        def alpha_updater(mob: ValueTracker, dt):
            value = mob.get_value()
            mob.set_value(value + dt)
        alpha.add_updater(alpha_updater)
        def rect_updater(start_angle: float):
            def util(mob: VMobject):
                value = alpha.get_value()
                mob.restore().shift(np.sin((value + start_angle)*PI)*0.02*UP)
            return util
        for _ in range(100):
            rect_i = rectangle.copy().shift(np.array([(2*random.random()-1)*5, (2*random.random()-1)*3, 0])).scale(random.random()**2+0.25).set_opacity(0.5+0.5*random.random()).set_color(interpolate_color(BLUE_A, BLUE_E, random.random()))
            rect_i.save_state().add_updater(rect_updater(2*random.random()))
            rectangles.append(rect_i)
        
        rect_combinatoric = rectangle.copy().scale(2).set_color(BLUE_B).add(Text("组合计数", font = "LXGW WenKai", color = BLACK).scale(0.8)).shift(3*LEFT)
        rect_array = rectangle.copy().scale(2).set_color(BLUE).add(Text("数列", font = "LXGW WenKai", color = BLACK).scale(0.8)).shift(1.6*DOWN).save_state().add_updater(rect_updater(2*random.random()))
        rect_number_theory = rectangle.copy().scale(2).set_color(BLUE_D).add(Text("解析数论", font = "LXGW WenKai", color = BLACK).scale(0.8)).shift(1.6*UP + 3*RIGHT).save_state().add_updater(rect_updater(2*random.random()))

        anim = FadeTransform(rect_shade, rect_combinatoric)
        self.remove(problem, factored_func).add(alpha, *rectangles, rect_array, rect_number_theory, shade, anim.mobject, notice1) #因为FadeTransform会干扰图层，所以用这种方法强制notice在最上层
        self.play(anim, FadeOut(shade), ReplacementTransform(notice1, notice2))
        rect_combinatoric.save_state().add_updater(rect_updater(-alpha.get_value()))
        self.waiting(0, 21) #但会用到母函数的
        self.waiting(3, 4) #除了组合计数 还有很多其它的领域
        rect_array.clear_updaters()
        anim = FadeTransform(rect_array, shade_in_proportion)
        self.waiting(0, 22) #比如说......
        self.add(shade, anim.mobject, notice2).play(anim, FadeIn(shade))
        self.remove(*self.mobjects).add(notice2)
        self.waiting(0+0-1, 28+18) #......数列 （空闲）
        
        texts = [r"a_"+str(i)+r"x^"+str(i) for i in range(7)] + [r"\cdots"]
        series = MTex(r"+".join(texts), isolate = [r"+", *texts]).scale(0.8).shift(0.45*DOWN + 0.5*RIGHT)
        series_terms = [series.get_part_by_tex(text) for text in texts]
        series_adds = series.get_parts_by_tex(r"+")
        power_series = MTex(r"P(x)=", tex_to_color_map = {r"x": RED, r"P": BLUE_D}).scale(0.8).next_to(series, LEFT).shift(0.05*DOWN)
        array_terms = VGroup()
        anims = []
        for i in range(7):
            series_terms[i][0:2].set_color(BLUE)
            series_terms[i][2:4].set_color(RED)
            term = series_terms[i][0:2].copy()
            array_terms.add(term)
            anims.append(TransformFromCopy(term, series_terms[i][0:2]))
            anims.append(Write(series_terms[i][2:4]))
            anims.append(Write(series_adds[i]))
        anims.append(Write(series_terms[7]))
        array_terms.shift(UP)
        array = MTex(r"\{a_n\}_{n=0}^{\infty}:", tex_to_color_map = {r"a_n": BLUE}).scale(0.8).next_to(array_terms, LEFT)
        self.play(Write(array), LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in array_terms], lag_ratio = 0.5, run_time = 1.5))
        self.waiting(0, 9) #把一个数列的所有项
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2))
        self.waiting(0, 11) #当作一个幂级数的所有系数
        self.play(Write(power_series))
        self.waiting(0, 26) #这样写出来的幂级数
        self.waiting(2, 10) #就被称作这个数列的母函数
        self.waiting(0, 23) #（空闲）

        self.play(*[FadeOut(mob, 0.5*UP) for mob in [series, power_series, array_terms, array]])
        self.waiting(0, 27) #我们试试用这样的思路
        array_Fibonacci = MTex(r"\{f_n\}_{n=0}^{\infty}:\ f_0=f_1=1;\ f_n=f_{n-1}+f_{n-2}(n\ge 2)", tex_to_color_map = {(r"f_n", r"f_0", r"f_1", r"f_{n-1}", r"f_{n-2}"): BLUE}).scale(0.8).shift(2.4*UP)
        self.play(Write(array_Fibonacci))
        self.waiting(1, 4) #来求一下斐波那契数列的通项公式

        Fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        texts = [str(Fibonacci[i]) + r"x^" + str(i) for i in range(8)] + [r"\cdots"]
        series_Fibonacci = MTex(r"+".join(texts), isolate = [r"+", *texts]).scale(0.8).next_to(5*LEFT+1.25*UP, buff = 0)
        terms_Fibonacci = [series_Fibonacci.get_part_by_tex(text) for text in texts]
        adds_Fibonacci = series_Fibonacci.get_parts_by_tex(r"+")
        symbol_Fibonacci = MTex(r"F(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT+1.2*UP, LEFT)
        symbol_Fibonacci_1 = MTex(r"xF(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT+0.4*UP, LEFT)
        symbol_Fibonacci_2 = MTex(r"x^2F(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT+0.4*DOWN, LEFT)
        terms_array = []
        terms_power = []
        for i in range(8):
            terms_array.append(terms_Fibonacci[i][0:-2].set_color(BLUE))
            terms_power.append(terms_Fibonacci[i][-2:].set_color(RED))
        terms_array_1 = []
        terms_remain_1 = VGroup()
        terms_array_2 = []
        terms_remain_2 = VGroup(terms_power[1].copy().shift(10*DOWN), adds_Fibonacci[1].copy().shift(10*DOWN)) #这两个物品不会出现在屏幕里，它们的作用是让两个Write动画同步
        ellipsis_1 = terms_Fibonacci[8].copy().shift(0.8*DOWN)
        ellipsis_2 = terms_Fibonacci[8].copy().shift(1.6*DOWN)
        for i in range(7):
            terms_array_1.append(terms_array[i].copy().next_to(terms_array[i+1].get_corner(RIGHT), LEFT, buff = 0).shift(0.8*DOWN))
            terms_remain_1.add(terms_power[i+1].copy().shift(0.8*DOWN), adds_Fibonacci[i+1].copy().shift(0.8*DOWN))
        anims = [TransformFromCopy(terms_array[1], terms_array_1[0])]
        for i in range(6):
            terms_array_2.append(terms_array_1[i].copy().next_to(terms_array_1[i+1].get_corner(RIGHT), LEFT, buff = 0).shift(0.8*DOWN))
            terms_remain_2.add(terms_power[i+2].copy().shift(1.6*DOWN), adds_Fibonacci[i+2].copy().shift(1.6*DOWN))
            anims.append(TransformFromCopy(terms_array[i+2], terms_array_2[i]))
            anims.append(TransformFromCopy(terms_array[i+2], terms_array_1[i+1]))
        anims.append(TransformFromCopy(terms_Fibonacci[8], ellipsis_2))
        anims.append(TransformFromCopy(terms_Fibonacci[8], ellipsis_1))
        
        self.play(Write(VGroup(symbol_Fibonacci, series_Fibonacci)))
        self.waiting(2, 3) #首先 写出斐波那契数列的母函数F(x)
        self.waiting(2, 16) #根据斐波那契数列的递推公式
        self.play(LaggedStart(*anims, lag_ratio = 0.1, run_time = 2))
        self.waiting(1+2-2, 28+7) #F(x)的每一项系数 都可以拆成两项的和
        self.waiting(1, 9) #根据这一点
        self.play(Write(terms_remain_1), Write(terms_remain_2))
        self.waiting(1, 7) #F(x)就可以拆成两个幂级数的和
        self.play(Write(symbol_Fibonacci_1), Write(symbol_Fibonacci_2))
        self.waiting(2, 6) #而这两个幂级数都可以用F(x)来表示

        equation_1 = MTex(r"\Rightarrow F(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT + 1.2*DOWN, LEFT)
        equation_2 = MTex(r"1+xF(x)+x^2F(x)", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT + 1.2*DOWN, buff = 0)
        self.play(Write(VGroup(equation_1, equation_2)))
        self.waiting(1, 6) #于是 我们得到了一个关于它的等式
        self.waiting(0, 15) #（空闲）

        solution_1 = MTex(r"\Rightarrow F(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT + 2.2*DOWN, LEFT)
        texts = r"\frac{1}{1-x-x^2}", r"=\frac{1}{\sqrt5}\left(\frac{\phi}{1-\phi x}+\frac{1/\phi}{1+x/\phi}\right)", r"=\sum_{n=0}^{\infty}\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}x^n"
        solution_2 = MTex("".join(texts), isolate = [*texts, r"\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}"], tex_to_color_map = {r"x": RED, r"\phi": YELLOW}).scale(0.8).next_to(5*LEFT + 2.2*DOWN, buff = 0)
        solution_terms = [solution_2.get_part_by_tex(text) for text in texts]
        solution_terms[2][-2:].shift(0.1*RIGHT)
        indicate = SurroundingRectangle(solution_2.get_part_by_tex(r"\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}"))
        formula = MTex(r"f_n", color = BLUE).scale(0.8).next_to(indicate, UP)
        self.play(ReplacementTransform(notice2, notice3), FadeIn(solution_1, 0.3*RIGHT), FadeIn(solution_terms[0], 0.3*RIGHT))
        self.waiting(1, 8) #通过这个等式解出F(x)
        self.play(FadeIn(solution_terms[1], 0.3*RIGHT))
        self.waiting(1, 16) #再做一点简单的几何级数展开
        self.play(FadeIn(solution_terms[2], 0.3*RIGHT))
        self.waiting(0, 29) #就可以通过对比系数
        self.play(ShowCreation(indicate), Write(formula))
        self.waiting(1, 11) #得到斐波那契数列的通项公式
        self.waiting(0, 15) #到此共59秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_2(Scene):
    def construct(self):
        notice3 = Notice("简单计算", "请　显然")
        notice4 = Notice("神奇操作", "请　好奇")
        notice5 = Notice("记号引入", "请记笔记")
        notice6 = Notice("理直气壮", "请勿模仿")

        array_Fibonacci = MTex(r"\{f_n\}_{n=0}^{\infty}:\ f_0=f_1=1;\ f_n=f_{n-1}+f_{n-2}(n\ge 2)", tex_to_color_map = {(r"f_n", r"f_0", r"f_1", r"f_{n-1}", r"f_{n-2}"): BLUE}).scale(0.8).shift(2.4*UP)
        symbol_Fibonacci = MTex(r"F(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT+1.2*UP, LEFT)
        symbol_Fibonacci_1 = MTex(r"xF(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT+0.4*UP, LEFT)
        symbol_Fibonacci_2 = MTex(r"x^2F(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT+0.4*DOWN, LEFT)
        symbols_Fibonacci = VGroup(symbol_Fibonacci, symbol_Fibonacci_1, symbol_Fibonacci_2)
        
        Fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        texts = [str(Fibonacci[i]) + r"x^" + str(i) for i in range(8)] + [r"\cdots"]
        series_Fibonacci = MTex(r"+".join(texts), isolate = [r"+", *texts]).scale(0.8).next_to(5*LEFT+1.25*UP, buff = 0)
        terms_Fibonacci = [series_Fibonacci.get_part_by_tex(text) for text in texts]
        adds_Fibonacci = series_Fibonacci.get_parts_by_tex(r"+")
        terms_array = []
        terms_power = []
        for i in range(8):
            terms_array.append(terms_Fibonacci[i][0:-2].set_color(BLUE))
            terms_power.append(terms_Fibonacci[i][-2:].set_color(RED))
        function_Fibonacci_1 = VGroup()
        function_Fibonacci_2 = VGroup()
        for i in range(7):
            function_Fibonacci_1.add(terms_array[i].copy().next_to(terms_array[i+1].get_corner(RIGHT), LEFT, buff = 0).shift(0.8*DOWN), terms_power[i+1].copy().shift(0.8*DOWN), adds_Fibonacci[i+1].copy().shift(0.8*DOWN))
        function_Fibonacci_1.add(terms_Fibonacci[8].copy().shift(0.8*DOWN))
        for i in range(6):
            function_Fibonacci_2.add(terms_array[i].copy().next_to(terms_array[i+2].get_corner(RIGHT), LEFT, buff = 0).shift(1.6*DOWN), terms_power[i+2].copy().shift(1.6*DOWN), adds_Fibonacci[i+2].copy().shift(1.6*DOWN))
        function_Fibonacci_2.add(terms_Fibonacci[8].copy().shift(1.6*DOWN))
        functions_Fibonacci = VGroup(series_Fibonacci, function_Fibonacci_1, function_Fibonacci_2)

        equation_1 = MTex(r"\Rightarrow F(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT + 1.2*DOWN, LEFT)
        equation_2 = MTex(r"1+xF(x)+x^2F(x)", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT + 1.2*DOWN, buff = 0)
        equation = VGroup(equation_1, equation_2)
        
        solution_1 = MTex(r"\Rightarrow F(x)=", tex_to_color_map = {r"x": RED, r"F": BLUE_D}).scale(0.8).next_to(5*LEFT + 2.2*DOWN, LEFT)
        texts = r"\frac{1}{1-x-x^2}=\frac{1}{\sqrt5}\left(\frac{\phi}{1-\phi x}+\frac{1/\phi}{1+x/\phi}\right)=\sum_{n=0}^{\infty}\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}x^n"
        solution_2 = MTex("".join(texts), isolate = r"\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}", tex_to_color_map = {r"x": RED, r"\phi": YELLOW}).scale(0.8).next_to(5*LEFT + 2.2*DOWN, buff = 0)
        solution_2[-2:].shift(0.1*RIGHT)
        indicate = SurroundingRectangle(solution_2.get_part_by_tex(r"\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}"))
        formula = MTex(r"f_n", color = BLUE).scale(0.8).next_to(indicate, UP)
        solution = VGroup(solution_1, solution_2, indicate, formula)

        self.add(notice3, array_Fibonacci, symbols_Fibonacci, functions_Fibonacci, equation, solution)
        self.waiting(2, 28) #这一通操作猛如虎 可谓相当神奇
        self.waiting(0, 14) #（空闲）
        self.play(ReplacementTransform(notice3, notice4))
        self.waiting(0, 28) #想必大家已经跃跃欲试
        self.play(LaggedStart(*[ApplyMethod(mob.shift, 0.2*UP, rate_func = there_and_back) for mob in terms_power], run_time = 2, lag_ratio = 0.2))
        self.waiting(1, 18) #要尝试着去搞清楚这里的x代表什么意思
        self.play(LaggedStart(*[ApplyMethod(mob.shift, 0.2*UP, rate_func = there_and_back) for mob in adds_Fibonacci], run_time = 2, lag_ratio = 0.2))
        self.waiting(0, 26) #加法和乘法又代表了哪两种运算了
        self.waiting(0, 22) #（空闲）

        self.play(*[FadeOut(mob) for mob in [array_Fibonacci, symbols_Fibonacci, functions_Fibonacci, equation, solution]], ReplacementTransform(notice4, notice5))
        self.waiting(1, 22) #有一种非常常见的数列的定义方式

        array = MTex(r"\{a_n\}_{n=0}^{\infty}:", tex_to_color_map = {r"a_n": BLUE}).scale(0.8).next_to(4.5*LEFT + 1.5*UP, LEFT)
        array_terms = [MTex(r"a_"+str(i), color = BLUE).scale(0.8).shift((i*1.5-4)*RIGHT + 1.5*UP) for i in range(7)] + [MTex(r"\cdots", color = BLUE).scale(0.8).shift(6.5*RIGHT + 1.5*UP)]
        brray = MTex(r"\{b_n\}_{n=0}^{\infty}:", tex_to_color_map = {r"b_n": GREEN}).scale(0.8).next_to(4.5*LEFT + 0.5*UP, LEFT)
        brray_terms = [MTex(r"b_0=0").scale(0.8).shift(4*LEFT + 0.5*UP)] + [MTex(r"b_"+str(i) + r"=a_"+str(i-1)).scale(0.8).shift((i*1.5-4)*RIGHT + 0.5*UP) for i in range(1, 8)] + [MTex(r"\cdots", color = GREEN).scale(0.8).shift(6.5*RIGHT + 0.5*UP)]
        terms_b = []
        terms_a = []
        remain = VGroup()
        for i in range(7):
            term_b = brray_terms[i][0:2].set_color(GREEN)
            term_b.position = term_b.get_center()
            term_b.refresh_bounding_box()
            terms_b.append(term_b)
            remain.add(brray_terms[i][2])
            if i == 0:
                remain.add(brray_terms[i][3].set_color(BLUE))
            else:
                terms_a.append(brray_terms[i][3:].set_color(BLUE))
        self.play(Write(array), LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in array_terms], lag_ratio = 0.5, run_time = 1.5))
        self.waiting(0, 9) #根据一个数列\{a_n\}
        self.play(Write(brray), LaggedStart(*[FadeIn(terms_b[i].move_to((i*1.5-4)*RIGHT+0.5*UP), 0.3*RIGHT) for i in range(7)], FadeIn(brray_terms[8], 0.3*RIGHT), lag_ratio = 0.5, run_time = 1.5))
        self.waiting(0, 15) #定义另一个数列\{b_n\}
        self.play(Write(remain, lag_ratio = 0.5, run_time = 2), 
                LaggedStart(*[ApplyMethod(term.move_to, term.position) for term in terms_b], lag_ratio = 0.1, run_time = 2), 
                LaggedStart(*[TransformFromCopy(array_terms[i], terms_a[i]) for i in range(6)], lag_ratio = 0.1, run_time = 2))
        self.waiting(1, 21) #使得对于每个n 都有b_n等于a_\{n-1\}
        self.waiting(0, 16) #（空闲）
        
        terms_b.append(brray_terms[7][0:2])
        arrows = [Arrow(array_terms[i].get_corner(DR), terms_b[i+1].get_corner(UL), color = [BLUE, GREEN]) for i in range(7)]
        self.play(LaggedStart(*[ShowCreation(mob) for mob in arrows], lag_ratio = 0.5, run_time = 2))
        self.waiting(1, 2) #这种方式把\{a_n\}整体向右移动了一位

        wrong_notation = MTex(r"\{b_n\}=\{a_{n-1}\}", tex_to_color_map = {r"b_n": GREEN, r"a_{n-1}": BLUE}).scale(0.8).shift(2.4*UP)
        line = Line(wrong_notation.get_corner(LEFT)+0.1*LEFT, wrong_notation.get_corner(RIGHT)+0.1*RIGHT, color = RED)
        self.play(Write(wrong_notation))
        self.waiting(3, 22) #所以很多书上会选择把\{b_n\}这个数列直接记作\{a_\{n-1\}\}的样子
        self.waiting(0, 19) #（空闲）
        self.play(ShowCreation(line), wrong_notation.animate.fade())
        self.waiting(2, 5) #但这样会引发记号的混乱 我不是很推荐
        self.waiting(0, 17) #（空闲）

        recommended_notation = MTex(r"\{b_n\}=\{S(a)_{n}\}", tex_to_color_map = {r"b_n": GREEN, (r"a", r"{n}"): BLUE, r"S": RED}).scale(0.8).shift(2.4*UP)
        self.waiting(1, 10) #在这个视频里
        self.play(Write(recommended_notation), FadeOut(wrong_notation, 0.3*DOWN), FadeOut(line, 0.3*DOWN))
        self.waiting(2, 12) #我们会用S这个记号来表示这种方式
        title = Text(r"移位算子", color = YELLOW, font = "simsun").next_to(3*UP, UP)
        line_title = Line(3*UP, 3*UP)
        self.play(Write(title), line_title.animate.put_start_and_end_on(3*UP+6*LEFT, 3*UP+6*RIGHT))
        self.waiting(1, 0) #S被称作移位算子
        self.waiting(1, 16) #它有两种运算
        
        operator_add = MTexText(r"$\bullet$定义$S_1+S_2$为：对任意数列$\{a_n\}_{n=0}^{\infty}$，$(S_1+S_2)(a)_n=S_1(a)_n+S_2(a)_n$", tex_to_color_map = {(r"S_1", r"S_2"): RED, (r"a_n", r"a"): BLUE}).scale(0.6).next_to(6*LEFT + 0.4*DOWN)
        operator_mul = MTexText(r"$\bullet$定义$S_1\circ S_2$为：对任意数列$\{a_n\}_{n=0}^{\infty}$，$(S_1\circ S_2)(a)_n=S_1(S_2(a))_n$", tex_to_color_map = {(r"S_1", r"S_2"): RED, (r"a_n", r"a"): BLUE}).scale(0.6).next_to(6*LEFT + 1.1*DOWN)
        self.play(FadeIn(operator_add, 0.5*RIGHT), lag_ratio = 0.1, run_time = 1.5) #一种是加法......
        self.play(FadeIn(operator_mul, 0.5*RIGHT), lag_ratio = 0.1, run_time = 1.5)
        self.waiting(2+0-3, 29+14) #另一种是复合（空闲）

        abelian_add = MTex(r"S_1+S_2 = S_2+S_1", tex_to_color_map = {(r"S_1", r"S_2"): RED}).scale(0.6).next_to(4*LEFT + 1.8*DOWN)
        abelian_mul = MTex(r"S_1\circ S_2 = S_2\circ S_1", tex_to_color_map = {(r"S_1", r"S_2"): RED}).scale(0.6).next_to(RIGHT + 1.8*DOWN)
        distribution = MTex(r"(S_1+S_2)(S_3+S_4)=S_1S_3 + S_1S_4 + S_2S_3 + S_2S_4", tex_to_color_map = {re.compile(r"S_."): RED}).scale(0.6).shift(2.5*DOWN)
        self.play(FadeIn(abelian_add, 0.5*RIGHT), FadeIn(abelian_mul, 0.5*RIGHT), lag_ratio = 0.1)
        self.waiting(1, 7) #这两种运算都满足交换律
        self.play(FadeIn(distribution, 0.5*RIGHT), lag_ratio = 0.1, run_time = 1.5)
        self.waiting(0.5, 12) #而且它们之间满足分配律
        self.play(ReplacementTransform(notice5, notice6))
        self.waiting(0, 16) #具体我就不证了
        self.waiting(3, 1) #感兴趣的同学可以在评论区写出证明
        self.waiting(0, 19) #到此共57秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_3(Scene):
    def construct(self):
        notice6 = Notice("理直气壮", "请勿模仿")
        notice7 = Notice("推导过程", "请　专心")
        notice8 = Notice("前置结论", "请还记得")
        notice9 = Notice("推导过程", "请　专心")

        title = Text(r"移位算子", color = YELLOW, font = "simsun").next_to(3*UP, UP)
        line_title = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        notation = MTex(r"\{b_n\}=\{S(a)_{n}\}", tex_to_color_map = {r"b_n": GREEN, (r"a", r"{n}"): BLUE, r"S": RED}).scale(0.8).shift(2.4*UP)
        shade = BackgroundRectangle(notation, fill_opacity = 1, fill_color = BACK).scale(np.array([3, 1, 0])).next_to(notation.get_corner(RIGHT), LEFT, buff = 0)
        
        array = MTex(r"\{a_n\}_{n=0}^{\infty}:", tex_to_color_map = {r"a_n": BLUE}).scale(0.8).next_to(4.5*LEFT + 1.5*UP, LEFT)
        array_terms = [MTex(r"a_"+str(i), color = BLUE).scale(0.8).shift((i*1.5-4)*RIGHT + 1.5*UP) for i in range(7)] + [MTex(r"\cdots", color = BLUE).scale(0.8).shift(6.5*RIGHT + 1.5*UP)]
        brray = MTex(r"\{b_n\}_{n=0}^{\infty}:", tex_to_color_map = {r"b_n": GREEN}).scale(0.8).next_to(4.5*LEFT + 0.5*UP, LEFT)
        brray_terms = [MTex(r"b_0=0").scale(0.8).shift(4*LEFT + 0.5*UP)] + [MTex(r"b_"+str(i) + r"=a_"+str(i-1)).scale(0.8).shift((i*1.5-4)*RIGHT + 0.5*UP) for i in range(1, 8)] + [MTex(r"\cdots", color = GREEN).scale(0.8).shift(6.5*RIGHT + 0.5*UP)]
        for i in range(7):
            brray_terms[i][0:2].set_color(GREEN)
            brray_terms[i][3:].set_color(BLUE)
        arrows = [Arrow(array_terms[i].get_corner(DR), brray_terms[i+1][0:2].get_corner(UL), color = [BLUE, GREEN]) for i in range(7)]
        
        operator_add = MTexText(r"$\bullet$定义$S_1+S_2$为：对任意数列$\{a_n\}_{n=0}^{\infty}$，$(S_1+S_2)(a)_n=S_1(a)_n+S_2(a)_n$", tex_to_color_map = {(r"S_1", r"S_2"): RED, (r"a_n", r"a"): BLUE}).scale(0.6).next_to(6*LEFT + 0.4*DOWN)
        operator_mul = MTexText(r"$\bullet$定义$S_1\circ S_2$为：对任意数列$\{a_n\}_{n=0}^{\infty}$，$(S_1\circ S_2)(a)_n=S_1(S_2(a))_n$", tex_to_color_map = {(r"S_1", r"S_2"): RED, (r"a_n", r"a"): BLUE}).scale(0.6).next_to(6*LEFT + 1.1*DOWN)
        abelian_add = MTex(r"S_1+S_2 = S_2+S_1", tex_to_color_map = {(r"S_1", r"S_2"): RED}).scale(0.6).next_to(4*LEFT + 1.8*DOWN)
        abelian_mul = MTex(r"S_1\circ S_2 = S_2\circ S_1", tex_to_color_map = {(r"S_1", r"S_2"): RED}).scale(0.6).next_to(RIGHT + 1.8*DOWN)
        distribution = MTex(r"(S_1+S_2)(S_3+S_4)=S_1S_3 + S_1S_4 + S_2S_3 + S_2S_4", tex_to_color_map = {re.compile(r"S_."): RED}).scale(0.6).shift(2.5*DOWN)
        laws = VGroup(operator_add, operator_mul, abelian_add, abelian_mul, distribution)

        array_Fibonacci = MTex(r"\{f_n\}_{n=0}^{\infty}:\ f_0=f_1=1;\ f_n=f_{n-1}+f_{n-2}(n\ge 2)", isolate = [r"(n\ge 2)"], tex_to_color_map = {(r"f_n", r"f_0", r"f_1", r"f_{n-1}", r"f_{n-2}"): BLUE}).scale(0.8).shift(1.8*UP)
        indicate = SurroundingRectangle(array_Fibonacci.get_part_by_tex(r"(n\ge 2)").shift(0.1*RIGHT))
        notice_operator = MTex(r":\ b_n=a_{n-1},\ b_0={0}", tex_to_color_map = {(r"b_n", r"b_0"): GREEN, (r"a_{n-1}", r"{0}"): BLUE}).scale(0.8).next_to(notation, buff = 0.1)
        self.add(notice6, title, line_title, notation, array, *array_terms, brray, *brray_terms[0:7], brray_terms[8], *arrows, laws)
        self.waiting(1, 21) #有了移位算子以后
        self.add(notice_operator, shade, notation).play(ReplacementTransform(notice6, notice7), *[FadeOut(mob) for mob in [array, *array_terms, brray, *brray_terms[0:7], brray_terms[8], *arrows, laws]], notation.animate.shift(2*LEFT), shade.animate.shift(2*LEFT), FadeIn(notice_operator.shift(2*LEFT), (notice_operator.get_width()+0.1)*RIGHT))
        self.play(FadeIn(array_Fibonacci))
        self.waiting(1, 24) #之前的递推公式就有了一种不同的表达方式

        position = MTex(r"f_0 = f_0+f_0+f_0", isolate = [r"f_0", r"+"]).scale(0.8).next_to(6*LEFT + 1.2*UP)
        position_terms = position.get_parts_by_tex(r"f_0")
        position_adds = position.get_parts_by_tex(r"+")
        recurses = [MTex(r"f_0=0+0+1", tex_to_color_map = {(r"f", r"0"): BLUE, r"1": PURPLE}).scale(0.8).next_to(6*LEFT + 0.9*UP), 
                MTex(r"f_1=f_0+{0}", tex_to_color_map = {(r"f_0", f"f_1", r"{0}"): BLUE}).scale(0.8).next_to(6*LEFT + 0.3*UP)] + [
                MTex(r"f_"+str(i)+r"=f_"+str(i-1)+r"+f_"+str(i-2), tex_to_color_map = {re.compile(r"f_."): BLUE}).scale(0.8).next_to(6*LEFT + (i*0.6-0.9)*DOWN) for i in range(2, 6)] + [
                MTex(r"\vdots").scale(0.8).set_x(position[2].get_x()).set_y(-2.7)]
        recurses[0][3].set_x(position_terms[1].get_x())
        recurses[0][4].set_x(position_adds[0].get_x())
        recurses[0][5].set_x(position_terms[2].get_x())
        recurses[0][6].set_x(position_adds[1].get_x())
        recurses[0][7].set_x(position_terms[3].get_x())
        recurses[1][6].set_x(position_terms[2].get_x())
        self.play(ShowCreation(indicate), LaggedStart(*[FadeIn(mob, 0.3*DOWN) for mob in recurses], lag_ratio = 0.5, run_time = 2))
        self.waiting(1, 11) #递推式是对所有大于等于2的数都成立的
        
        texts = r"\{f_{n}\}=\{S(f)_{n}\}+\{S^2(f)_{n}\}", r"+\{\delta_n\}"
        equality = MTex(r"".join(texts), isolate = [*texts, r"="], tex_to_color_map = {(r"f", r"{n}"): BLUE, (r"S", r"2"): RED, r"\delta_n": PURPLE}).scale(0.8).next_to(0.6*DOWN + 2*LEFT)
        terms = [equality.get_part_by_tex(text) for text in texts]
        sign_equal = equality.get_part_by_tex(r"=")
        approx = Text("几乎成立", font = "simsun", color = YELLOW).scale(0.6).shift(sign_equal.get_center()).shift(DOWN)
        arrow = Arrow(approx, sign_equal, buff = 0.15, color = YELLOW)
        approx.add(arrow)
        delta = Text("单位采样序列", font = "simsun", color = YELLOW).scale(0.6).shift(terms[1][2].get_center()).shift(UP)
        arrow = Arrow(delta, terms[1][2], buff = 0.15, color = YELLOW)
        delta.add(arrow)
        self.play(Write(terms[0]))
        self.play(FadeIn(approx, 0.3*UP))
        self.waiting(2+2-3, 20+22) #所以我们几乎有这么一个式子 它在n不等于零的时候都成立
        self.waiting(2, 14) #当然 这也不是什么大事
        self.play(Write(terms[1]), FadeOut(approx, 0.3*DOWN), FadeIn(delta, 0.3*DOWN), FadeOut(indicate))
        self.waiting(1, 17) #补一个只在n=0时取1
        self.waiting(2, 12) #其它时候都取0的数列就好了
        self.waiting(0, 16) #（空闲）
        
        texts = r"\Rightarrow", r"\{\delta_n\}=\{(1-S-S^2)(f)_{n}\}"
        simplified = MTex(r"".join(texts), isolate = [*texts, r"="], tex_to_color_map = {(r"f", r"{n}"): BLUE, (r"1", r"S", r"2"): RED, r"\delta_n": PURPLE}).scale(0.8)
        offset = sign_equal.get_center() + 1.2*DOWN - simplified.get_part_by_tex(r"=").get_center()
        simplified.shift(offset)
        terms = [simplified.get_part_by_tex(text) for text in texts]
        indicate = SurroundingRectangle(terms[1])
        self.waiting(1, 19) #再经过一些化简
        self.play(Write(simplified))
        self.waiting(0, 13) #我们就不出意外地得到了......

        offset = 0.6*DOWN - terms[1].get_center()
        start = indicate.get_corner(UR)
        alpha = ValueTracker(0.0)
        def indicate_updater(mob: SurroundingRectangle):
            value = alpha.get_value()
            mob.next_to(start + value*offset, DL, buff = 0)
        indicate.add_updater(indicate_updater)
        self.play(*[FadeOut(mob) for mob in recurses], *[FadeOut(mob, offset) for mob in [equality, terms[0], delta]], terms[1].animate.shift(offset), alpha.animate.set_value(1), ShowCreation(indicate))
        indicate.clear_updaters()
        array_delta = Text("单位采样序列", font = "simsun", color = YELLOW).scale(0.6).shift(0.9*UP + 5*LEFT)
        formula_delta = MTex(r"\delta_n=\begin{cases}{1}, n=0\\{0}, n>0\end{cases}", tex_to_color_map = {(r"\delta_n", r"{1}", r"{0}"): PURPLE}).scale(0.8).next_to(array_delta, DOWN)
        delta = VGroup(array_delta, formula_delta)
        self.play(FadeIn(delta))
        self.waiting(2, 5) #把斐波那契数列变为单位采样序列的方法 嗯？
        self.waiting(1, 5) #（空闲）

        operator = MTex(r"\{\delta_n\}=\{(1-S-S^2)(f)_{n}\}", isolate = [r"(1-S-S^2)", r"="], tex_to_color_map = {(r"f", r"{n}"): BLUE, (r"1", r"S", r"2"): RED, r"\delta_n": PURPLE}).scale(0.8).shift(0.6*DOWN)
        position_equal = operator.get_part_by_tex(r"=").get_center()
        self.add(operator).remove(terms[0])
        indicate_inverse = SurroundingRectangle(operator.get_part_by_tex(r"(1-S-S^2)"))
        series = MTex(r"1=({1}-x-x^2)F(x)", isolate = [r"({1}-x-x^2)", r"="], tex_to_color_map = {(r"{1}", r"x", r"2"): RED, r"F": BLUE_D}).scale(0.8).shift(0.6*UP)
        offset = position_equal + 1.2*UP - series.get_part_by_tex(r"=").get_center()
        series.shift(offset)
        indicate_same = SurroundingRectangle(series.get_part_by_tex(r"({1}-x-x^2)"))
        self.play(Transform(indicate, indicate_inverse), ReplacementTransform(notice7, notice8))
        self.waiting(2, 1) #现在 斐波那契数列前面的式子
        self.play(Write(series))
        self.waiting(1, 6) #和我们之前解母函数的时候
        self.play(ShowCreation(indicate_same))
        self.waiting(1, 0) #F(x)前面的系数
        self.waiting(1, 16) #表达式一模一样
        self.waiting(0, 15) #（空闲）
        
        texts = r"F(x)=", r"\frac{1}{1-x-x^2}=\frac{1}{\sqrt5}\left(\frac{\phi}{1-\phi x}+\frac{1/\phi}{1+x/\phi}\right)=", r"\sum_{n=0}^{\infty}\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}x^n"
        solution = MTex(r"".join(texts), isolate = texts, tex_to_color_map = {r"x": RED, r"\phi": YELLOW, r"F": BLUE_D}).scale(0.6).shift(2.4*DOWN)
        terms = [solution.get_part_by_tex(text) for text in texts]
        solution_short = MTex(texts[0]+texts[2], isolate = [texts[0], texts[2]], tex_to_color_map = {r"x": RED, r"\phi": YELLOW, r"F": BLUE_D}).scale(0.6).next_to(2.4*DOWN + 7*RIGHT, LEFT)
        terms_short = [solution_short.get_part_by_tex(text) for text in [texts[0], texts[2]]]
        point = (terms_short[0].get_corner(RIGHT) + terms_short[1].get_corner(LEFT))/2
        self.play(Write(solution), FadeOut(indicate), FadeOut(indicate_same), ReplacementTransform(notice8, notice9))
        self.waiting(2, 10) #不同的是 当时我们可以把带x的式子除过去
        self.waiting(3, 12) #但现在我们不知道带S的式子能不能除
        self.waiting(0, 14) #（空闲）
        self.play(ReplacementTransform(terms[0], terms_short[0]), terms[2].animate.next_to(2.4*DOWN + 7*RIGHT, LEFT), FadeOutToPoint(terms[1], point)) #TransformMatchingStrings用不了
        self.remove(solution).add(solution_short).waiting(2, 6) #好在F(x)的表达式我们已经知道了
        
        operator_inverse = MTex(r"\Rightarrow \{F(S)(\delta)_n\}=\{F(S)(1-S-S^2)(f)_n\}", isolate = [r"F(S)(1-S-S^2)", r"="], tex_to_color_map = {r"(f)_n": BLUE, (r"1", r"S", r"2"): RED, r"(\delta)_n": PURPLE, r"F": BLUE_D, (r"(", r")"): WHITE}).scale(0.8)
        offset = position_equal + 0.9*DOWN - operator_inverse.get_part_by_tex(r"=").get_center()
        operator_inverse.shift(offset)
        term_canceled = operator_inverse.get_part_by_tex(r"F(S)(1-S-S^2)")
        line = Line(term_canceled.get_corner(LEFT) + 0.1*LEFT, term_canceled.get_corner(RIGHT) + 0.1*RIGHT, color = RED)
        operator_solution = MTex(r"\Rightarrow \{F(S)(\delta)_{n}\}=\{f_n\}", isolate = [r"="], tex_to_color_map = {(r"f_n"): BLUE, r"S": RED, (r"\delta", r"{n}"): PURPLE, r"F": BLUE_D}).scale(0.8)
        offset = position_equal + 1.8*DOWN - operator_solution.get_part_by_tex(r"=").get_center()
        operator_solution.shift(offset)
        self.play(Write(operator_inverse))
        self.waiting(0, 27) #只要我们把S代进这个表达式里面
        self.waiting(2, 1) #给两边同时乘上去
        self.play(ShowCreation(line))
        self.waiting(2, 2) #斐波那契数列前面的式子就会被消掉
        self.play(Write(operator_solution))
        self.waiting(1+3-2, 12+1) #而最后剩下的 就只有单位采样序列前面的F(S)
        self.waiting(1, 8) #到此共66秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Chapter3_4(Scene):
    def construct(self):
        notice9 = Notice("推导过程", "请　专心")
        notice10 = Notice("重要结论", "请记笔记")
        notice11 = Notice("常见误区", "请勿模仿")
        notice12 = Notice("理论框架", "请记笔记")

        title = Text(r"移位算子", color = YELLOW, font = "simsun").next_to(3*UP, UP)
        line_title = Line(3*UP+6*LEFT, 3*UP+6*RIGHT)
        
        notation = MTex(r"\{b_n\}=\{S(a)_{n}\}", tex_to_color_map = {r"b_n": GREEN, (r"a", r"{n}"): BLUE, r"S": RED}).scale(0.8).shift(2.4*UP + 2*LEFT)
        notice_operator = MTex(r":\ b_n=a_{n-1},\ b_0={0}", tex_to_color_map = {(r"b_n", r"b_0"): GREEN, (r"a_{n-1}", r"{0}"): BLUE}).scale(0.8).next_to(notation, buff = 0.1)
        notation.add(notice_operator)
        array_Fibonacci = MTex(r"\{f_n\}_{n=0}^{\infty}:\ f_0=f_1=1;\ f_n=f_{n-1}+f_{n-2}(n\ge 2)", isolate = [r"(n\ge 2)"], tex_to_color_map = {(r"f_n", r"f_0", r"f_1", r"f_{n-1}", r"f_{n-2}"): BLUE}).scale(0.8).shift(1.8*UP)
        array_Fibonacci[-5:].shift(0.1*RIGHT)
        
        array_delta = Text("单位采样序列", font = "simsun", color = YELLOW).scale(0.6).shift(0.9*UP + 5*LEFT)
        formula_delta = MTex(r"\delta_n=\begin{cases}{1}, n=0\\{0}, n>0\end{cases}", tex_to_color_map = {(r"\delta_n", r"{1}", r"{0}"): PURPLE}).scale(0.8).next_to(array_delta, DOWN)
        delta = VGroup(array_delta, formula_delta)

        operator = MTex(r"\{\delta_n\}=\{(1-S-S^2)(f)_{n}\}", isolate = [r"(1-S-S^2)", r"="], tex_to_color_map = {(r"f", r"{n}"): BLUE, (r"1", r"S", r"2"): RED, r"\delta_n": PURPLE}).scale(0.8).shift(0.6*DOWN)
        operator_anchor = operator.get_part_by_tex(r"=").get_center()
        series = MTex(r"1=({1}-x-x^2)F(x)", isolate = [r"({1}-x-x^2)", r"="], tex_to_color_map = {(r"{1}", r"x", r"2"): RED, r"F": BLUE_D}).scale(0.8).shift(0.6*UP)
        series_anchor = series.get_part_by_tex(r"=").get_center()
        series.shift(operator_anchor + 1.2*UP - series_anchor)
        series_anchor = operator_anchor + 1.2*UP
        operator_inverse = MTex(r"\Rightarrow \{F(S)(\delta)_n\}=\{F(S)(1-S-S^2)(f)_n\}", isolate = [r"F(S)(1-S-S^2)", r"="], tex_to_color_map = {r"(f)_n": BLUE, (r"1", r"S", r"2"): RED, r"(\delta)_n": PURPLE, r"F": BLUE_D, (r"(", r")"): WHITE}).scale(0.8)
        inverse_anchor = operator_inverse.get_part_by_tex(r"=").get_center()
        operator_inverse.shift(operator_anchor + 0.9*DOWN - inverse_anchor)
        term_canceled = operator_inverse.get_part_by_tex(r"F(S)(1-S-S^2)")
        line_cancel = Line(term_canceled.get_corner(LEFT) + 0.1*LEFT, term_canceled.get_corner(RIGHT) + 0.1*RIGHT, color = RED)
        texts = r"\Rightarrow", r"\{F(S)(\delta)_{n}\}=\{f_n\}"
        operator_solution = MTex(r" ".join(texts), isolate = [r"=", *texts], tex_to_color_map = {(r"f_n"): BLUE, r"S": RED, (r"\delta", r"{n}"): PURPLE, r"F": BLUE_D}).scale(0.8)
        operator_solution_terms = [operator_solution.get_part_by_tex(text) for text in texts]
        offset = operator_anchor + 1.8*DOWN - operator_solution.get_part_by_tex(r"=").get_center()
        operator_solution.shift(offset)
        
        solution_short = MTex(r"F(x)=\sum_{n=0}^{\infty}\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}x^n", tex_to_color_map = {r"x": RED, r"\phi": YELLOW, r"F": BLUE_D}).scale(0.6).next_to(2.4*DOWN + 7*RIGHT, LEFT)
        
        self.add(notice9, title, line_title, notation, array_Fibonacci, delta, operator, series, operator_inverse, line_cancel, operator_solution, solution_short)
        position_equal = solution_short[4].get_center()
        offset_series = position_equal + 3.3*UP - series_anchor
        offset_operator = position_equal + 2.7*UP - operator_anchor
        offset_solution = 0*UP - operator_solution_terms[1].get_center()
        
        self.play(operator_solution_terms[1].animate.shift(offset_solution), FadeOut(operator_solution_terms[0], offset_solution), 
            FadeOutToPoint(operator_inverse, operator_anchor + 1.2*UP), FadeOutToPoint(line_cancel, operator_anchor + 1.2*UP), 
            series.animate.scale(0.75, about_point = series_anchor).shift(offset_series), operator.animate.scale(0.75, about_point = operator_anchor).shift(offset_operator), 
            solution_short.animate.next_to(0.6*DOWN + 7*RIGHT, LEFT), ReplacementTransform(notice9, notice10))
        self.waiting(3, 19) #数列的母函数 表示了把单位采样序列变成它的过程
        self.waiting(3, 12) #母函数里面的x 就是移位算子S
        self.waiting(0, 16) #（空闲）

        Fibonacci = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        drray = MTex(r"\{\delta_n\}_{n=0}^{\infty}:", tex_to_color_map = {r"\delta_n": PURPLE}).scale(0.8).next_to(4.5*LEFT + 1.5*DOWN, LEFT)
        drray_terms = [MTex(str(int(i==0)), color = PURPLE).scale(0.8).shift((i*1.5-4)*RIGHT + 1.5*DOWN) for i in range(7)] + [MTex(r"\cdots", color = PURPLE).scale(0.8).shift(6.5*RIGHT + 1.5*DOWN)]
        frray = MTex(r"\{f_n\}_{n=0}^{\infty}:", tex_to_color_map = {r"f_n": BLUE}).scale(0.8).next_to(4.5*LEFT + 2.5*DOWN, LEFT)
        frray_terms = [MTex(str(Fibonacci[i]), color = BLUE).scale(0.8).shift((i*1.5-4)*RIGHT + 2.5*DOWN) for i in range(7)] + [MTex(r"\cdots", color = BLUE).scale(0.8).shift(6.5*RIGHT + 2.5*DOWN)]
        
        operator_terms = [MTex(str(Fibonacci[i]) + r"S^" + str(i), tex_to_color_map = {str(Fibonacci[i]): BLUE, r"S^" + str(i): RED}).scale(0.5).next_to(4*LEFT + 2.15*DOWN + 1.5*i*RIGHT) for i in range(7)]
        arrow = ArcBetweenPoints(ORIGIN, 0.55*DR, angle = -PI/2, color = [PURPLE, BLUE]).set_width(1.5, stretch = True).next_to(4*LEFT + 1.5*DOWN, DR, buff = 0)
        tip = Triangle(stroke_width = 0, fill_opacity = 1, fill_color = BLUE).rotate(PI).set_height(0.2).next_to(4*LEFT + 2.25*DOWN, UP, buff = 0)
        shade = BackgroundRectangle(drray_terms[0], fill_opacity = 1, fill_color = BACK, buff = 0.1)
        arrows = [arrow.copy().scale(np.array([0, 1, 0]), about_point = 4*LEFT + 1.5*DOWN)] + [arrow.copy().shift(i*1.5*RIGHT) for i in range(7)] #
        tips = [tip.copy().shift(1.5*i*RIGHT) for i in range(8)]
        line = Line(4*LEFT + 1.5*DOWN, 5*RIGHT + 1.5*DOWN, color = PURPLE)
        line_tail = Line(5*RIGHT + 1.5*DOWN, 6*RIGHT + 1.5*DOWN, color = [PURPLE, PURPLE, BACK])

        self.play(Write(drray), LaggedStart(*[FadeIn(mob, 0.3*RIGHT) for mob in drray_terms], lag_ratio = 0.5, run_time = 1.5))
        self.waiting(0.5, 18) #这件事情琢磨琢磨还挺合理的
        self.add(line_tail, line, *arrows, shade, drray_terms[0]).play(Write(frray), 
        *[ShowCreation(arrows[i], run_time = 4, rate_func = squish_rate_func(linear, i/10, (i+1)/10)) for i in range(8)], 
        *[ShowCreation(operator_terms[i], run_time = 4, rate_func = squish_rate_func(smooth, (i+1)/10, (i+2)/10)) for i in range(7)],
        *[ShowCreation(tips[i], run_time = 4, rate_func = squish_rate_func(smooth, (i+1)/10, (i+2)/10)) for i in range(8)],
        *[FadeOut(drray_terms[i+1], run_time = 4, rate_func = squish_rate_func(smooth, i/10, (i+2)/10)) for i in range(6)], 
        *[Write(frray_terms[i], run_time = 4, rate_func = squish_rate_func(smooth, (i+2)/10, (i+3)/10)) for i in range(8)], 
        ShowCreation(line, run_time = 4, rate_func = squish_rate_func(linear, 1/10, 7/10)), ShowCreation(line_tail, run_time = 4, rate_func = squish_rate_func(linear, 7/10, 7.5/10)))
        self.waiting(2+1-4, 22+21) #毕竟数列的每一项都在系数上摆着 我们只需要挪就完事了
        self.waiting(0, 21) #（空闲）

        texts = r"F(S)=", r"\frac{1}{1-S-S^2}=\frac{1}{\sqrt5}\left(\frac{\phi}{1-\phi S}+\frac{1/\phi}{1+S/\phi}\right)=", r"\sum_{n=0}^{\infty}\frac{\phi^{n+1}-(-\phi)^{-n-1}}{\sqrt5}S^n"
        solution = MTex(r"".join(texts), isolate = texts, tex_to_color_map = {r"S": RED, r"\phi": YELLOW, r"F": BLUE_D}).scale(0.6).shift(2*DOWN)
        solution_terms = [solution.get_part_by_tex(text) for text in texts]
        solution_s = MTex(texts[0]+texts[2], isolate = [texts[0], texts[2]], tex_to_color_map = {r"S": RED, r"\phi": YELLOW, r"F": BLUE_D}).scale(0.6).next_to(2.4*DOWN + 7*RIGHT, LEFT)
        solution_s.shift(position_equal - solution_s[4].get_center())
        solution_s_terms = [solution_s.get_part_by_tex(text) for text in [texts[0], texts[2]]]
        point = (solution_s_terms[0].get_corner(RIGHT) + solution_s_terms[1].get_corner(LEFT))/2
        [solution_short[i].become(solution_s[i]) for i in range(5, 10)] #不这么做的话，求和符号插值会出问题
        self.play(ReplacementTransform(solution_short, solution_s), ReplacementTransform(notice10, notice11))
        self.waiting(1, 15) #但我们把x换成S之后
        shade_all = Rectangle(stroke_width = 0, fill_color = BACK, fill_opacity = 1, width = FRAME_WIDTH, height = 1.8).shift(2*DOWN)

        self.add(shade_all, *solution_s_terms).play(ReplacementTransform(solution_s_terms[0], solution_terms[0]), ReplacementTransform(solution_s_terms[1], solution_terms[2]), 
            FadeIn(shade_all), FadeInFromPoint(solution_terms[1], point))
        self.remove(shade_all, drray, *drray_terms, frray, *frray_terms, *arrows, *tips, *operator_terms, line, line_tail)
        self.waiting(0, 18) #就多出来了很多问题
        self.waiting(0, 19) #（空闲）

        line_1 = Underline(solution_terms[1][0:8], color = YELLOW)
        confusion_1 = MTex("???", color = YELLOW).scale(0.5).next_to(line_1, DOWN, buff = 0.1)
        line_1.add(confusion_1)
        confusion_2 = confusion_1.copy().next_to(solution_terms[1][-1], DOWN).set_y(confusion_1.get_y())
        arrow = Arrow(confusion_2, solution_terms[1][-1], buff = 0.1, color = YELLOW)
        confusion_2.add(arrow)
        self.play(Write(line_1))
        self.waiting(2, 1) #S的多项式的除法应该怎么定义呢
        self.play(FadeIn(confusion_2, 0.3*UP))
        self.waiting(2, 12) #另外 麦克劳林展开是有收敛域的
        self.waiting(2, 4) #但S根本不是一个数
        self.waiting(2, 9) #我们还能放心地展开几何级数吗
        self.waiting(0, 21) #（空闲）

        back = SurroundingRectangle(series, buff = 0.2, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        back_inner = SurroundingRectangle(series, buff = 0.1, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        back.add(back_inner)
        self.bring_to_back(back).play(ShowCreation(back), ReplacementTransform(notice11, notice12))
        self.waiting(0, 27) #但其实这都不是问题
        self.waiting(0, 15) #（空闲）

        shade_all = Rectangle(height = FRAME_HEIGHT, width = FRAME_WIDTH, stroke_width = 0, fill_opacity = 0, fill_color = BACK)
        board = Rectangle(height = 6, width = 10, fill_opacity = 1, fill_color = BLACK, stroke_color = WHITE)
        board_inner = Rectangle(height = 5.8, width = 9.8, fill_opacity = 1, fill_color = "#222222", stroke_color = YELLOW_E)
        title_2 = Text(r"形式幂级数", color = YELLOW, font = "simsun").next_to(3*UP, UP)
        series_s = MTex(r"1=({1}-S-S^2)F(S)", tex_to_color_map = {(r"{1}", r"S", r"2"): RED, r"F": BLUE_D}).scale(0.8).shift(2.4*UP)
        board.add(board_inner)
        self.add(shade_all, line_title, back, series, notice12).play(shade_all.animate.set_opacity(0.8), Transform(back, board), Transform(series, series_s), FadeOut(title), FadeIn(title_2))
        self.waiting(1, 7) #形式幂级数的理论告诉我们

        series_1 = MTex(r"P(S)=1-S-S^2", isolate = r"=", tex_to_color_map = {(r"1", r"S", r"2"): RED, r"P": BLUE_D}).scale(0.8).next_to(1.5*UP + 4*LEFT)
        series_2 = MTex(r"F(S)={1}+{1}S+{2}S^2+{3}S^3+{5}S^4+{8}S^5+\cdots", tex_to_color_map = {(r"{1}", r"{2}", r"{3}", r"{5}", r"{8}"): BLUE, (r"S", re.compile(r"S^.")): RED, r"F": BLUE_D}).scale(0.8).next_to(0.75*UP + 4*LEFT)
        series_3 = MTex(r"P(S)F(S)={1}+{0}S+{0}S^2+{0}S^3+{0}S^4+{0}S^5+\cdots", isolate = r"=", tex_to_color_map = {r"{1}": BLUE, r"{0}": GREY, (r"S", re.compile(r"S^.")): RED, (r"F", r"P"): BLUE_D}).scale(0.8)
        offset = series_1.get_part_by_tex(r"=").get_center() + 1.5*DOWN - series_3.get_part_by_tex(r"=").get_center()
        series_3.shift(offset)
        self.play(FadeIn(series_1, 0.3*RIGHT), lag_ratio = 0.2)
        self.waiting(1, 24) #几乎每一个由S组成的幂级数
        self.play(FadeIn(series_2, 0.3*RIGHT), lag_ratio = 0.2, run_time = 1.5)
        self.waiting(0.5, 21) #都有另一个由S组成的幂级数
        self.play(FadeIn(series_3, 0.3*RIGHT), lag_ratio = 0.2, run_time = 1.5)
        self.waiting(1.5, 4) #这两个幂级数的复合 等于什么都没做
        self.waiting(0, 16) #（空闲）

        inverse_1 = MTex(r"P(x)=\left(F(x)\right)^{-1}", tex_to_color_map = {(r"P", r"F"): BLUE_D, r"x": RED}).scale(0.8).shift(DOWN + 2*LEFT)
        inverse_2 = MTex(r"F(x)=\left(P(x)\right)^{-1}", tex_to_color_map = {(r"P", r"F"): BLUE_D, r"x": RED}).scale(0.8).shift(DOWN + 2*RIGHT)
        self.play(Write(inverse_1), Write(inverse_2))
        self.waiting(2, 19) #这两个式子 互相被称作对方的逆
        self.waiting(1, 26) #我们要除以一个式子
        self.waiting(2, 5) #只需要乘上它的逆就好了
        self.waiting(0, 14) #（空闲）
        self.waiting(2, 22) #并且 这样的逆如果存在
        self.waiting(1, 15) #就一定是唯一的
        self.waiting(0, 19) #（空闲）

        operator_solution = MTex(r"\{F(S)(\delta)_{n}\}=\{f_n\}", tex_to_color_map = {(r"f_n"): BLUE, r"S": RED, (r"\delta", r"{n}"): PURPLE, r"F": BLUE_D}).scale(0.8).move_to(2.4*UP)
        self.remove(operator_solution_terms[1], notation, array_Fibonacci, line_1, confusion_2).bring_to_back(operator_solution).play(*[mob.animate.shift(13*LEFT) for mob in [back, series, series_1, series_2, series_3, inverse_1, inverse_2]], 
            *[FadeOut(mob) for mob in [delta, operator, shade_all]])
        self.waiting(2, 15) #所以 形式幂级数之间的互逆关系
        self.waiting(2, 16) #不是因为麦克劳林展开才成立的
        self.waiting(0, 16) #（空闲）

        linear_1 = MTex(r"P_1(S)=1-\phi S", isolate = r"=", tex_to_color_map = {r"P_1": BLUE_D, r"S": RED, r"\phi": YELLOW}).scale(0.6).next_to(1.5*UP + 6.5*LEFT)
        geometry_1 = MTex(r"P_1^{-1}(S)=1+\phi S+\phi^2S^2+\phi^3S^3+\cdots", isolate = r"=", tex_to_color_map = {r"P_1^{-1}": BLUE_D, (r"S", re.compile(r"S^.")): RED, (r"\phi"): YELLOW}).scale(0.6)
        linear_2 = MTex(r"P_2(S)=1+\frac{S}{\phi}", isolate = r"=", tex_to_color_map = {r"P_2": BLUE_D, r"S": RED, r"\phi": YELLOW}).scale(0.6).next_to(1.5*UP + 0.5*LEFT)
        geometry_2 = MTex(r"P_2^{-1}(S)=1+(-\phi)^{-1} S+(-\phi)^{-2}S^2+(-\phi)^{-3}S^3+\cdots", isolate = r"=", tex_to_color_map = {r"P_2^{-1}": BLUE_D, (r"S", re.compile(r"S^.")): RED, r"\phi": YELLOW}).scale(0.6)
        linear_1_anchor = linear_1.get_part_by_tex(r"=").get_center()
        geometry_1_anchor = geometry_1.get_part_by_tex(r"=").get_center()
        linear_2_anchor = linear_2.get_part_by_tex(r"=").get_center()
        geometry_2_anchor = geometry_2.get_part_by_tex(r"=").get_center()
        geometry_1.shift(linear_1_anchor + 0.75*DOWN - geometry_1_anchor)
        geometry_2.shift(linear_2_anchor + 0.75*DOWN - geometry_2_anchor)
        cancel = MTex(r"P_1(S)P_1^{-1}(S)=P_2(S)P_2^{-1}(S)=1+0S+0S^2+0S^3+\cdots", tex_to_color_map = {(r"P_1", r"P_2", r"-1"): BLUE_D, (r"S", re.compile(r"S^.")): RED, r"0": GREY}).scale(0.6)
        result = MTex(r"F(S)=\frac{\phi}{\sqrt5}P_1^{-1}(S)+\frac{1}{\sqrt5\phi}P_2^{-1}(S)", tex_to_color_map = {(r"P_1^{-1}", r"P_2^{-1}", r"F"): BLUE_D, r"S": RED, r"\phi": YELLOW}).scale(0.6).shift(0.9*DOWN)
        indicate_result = SurroundingRectangle(result)
        self.play(LaggedStart(*[FadeIn(mob) for mob in [linear_1, geometry_1, linear_2, geometry_2]], lag_ratio = 0.5, run_time = 2))
        self.waiting(0, 8) #只要我们找到了某个幂级数
        self.play(Write(cancel))
        self.waiting(0, 8) #乘以一次多项式等于1
        self.play(Write(result))
        self.play(ShowCreation(indicate_result))
        self.waiting(2+2-3, 15+4) #那么它就是这个一次多项式的逆 就可以被用来展开几何级数
        self.waiting(0, 17) #（空闲）

        self.waiting(2, 11) #并且 在一定程度上
        self.waiting(2, 22) #正是因为形式幂级数有唯一的逆
        self.waiting(2, 2) #在麦克劳林展开的时候
        self.waiting(2, 29) #一次分式才会得到几何级数的结果
        self.waiting(4, 5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.waiting(4, 0) #到此共95秒
        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

###############################################################################

class Summary_1(Scene):

    def construct(self):
        notice1 = Notice("良心视频", "请　三连")

        self.play(Write(notice1))
        self.waiting(1, 16) #非常感谢大家能看到这里

        cover = ImageMobject("Cover.png", height = 2)
        self.play(FadeIn(cover, 0.5*UP))
        self.waiting(2, 11) #这应该是我做过的体量最大的一期视频了
        self.waiting(2, 25) #把母函数这个话题完整地呈现出来
        self.play(FadeOut(cover))
        self.waiting(0, 21) #要考虑相当多的事情
        self.waiting(0, 14) #（空闲）

        function = MTex(r"F(x)=a_0x^0+a_1x^1+a_2x^2+a_3x^3+a_4x^4+a_5x^5+a_6x^6+\cdots", tex_to_color_map = {r"F": BLUE_D, re.compile(r"a_."): BLUE, r"x": RED}).scale(0.6)
        self.play(Write(function))
        self.waiting(0, 20) #会用母函数其实要求不是太高
        self.waiting(2, 5) #学会了集合就能上手

        self.play(function.animate.move_to(2.5*UP))
        self.waiting(0, 7) 
        ring = MTexText(r"一个集合$R$与其上的两种二元运算$+, \times$的组合$(R, +, \times)$被称为环，\\当且仅当其满足:", alignment = None).scale(0.8).next_to(1.5*UP + 6*LEFT, buff = 0)
        self.play(Write(ring)) #但要严格地从零开始构造母函数的理论
        
        axiom_1 = MTexText(r"(1)对$a,b\in R$，有$a+b\in R$；").scale(0.7).next_to(0.5*UP + 6*LEFT)
        axiom_2 = MTexText(r"(2)对$a,b,c\in R$，有$(a+b)+c=a+(b+c)$；").scale(0.7).next_to(6*LEFT)
        axiom_3 = MTexText(r"(3)存在$0\in R$，对任意$a\in R$，有$a+0=a$；").scale(0.7).next_to(0.5*DOWN + 6*LEFT)
        axiom_4 = MTexText(r"(4)对任意$a\in R$， 存在$b\in R$，使得$a+b=0$").scale(0.7).next_to(1*DOWN + 6*LEFT)
        axiom_5 = MTexText(r"(5)对$a,b\in R$，有$a\times b\in R$；").scale(0.7).next_to(1.5*DOWN + 6*LEFT)
        axiom_6 = MTexText(r"(6)对$a,b,c\in R$，有$(a\times b)\times c=a\times (b\times c)$；").scale(0.7).next_to(2*DOWN + 6*LEFT)
        axiom_7 = MTexText(r"(7)对$a,b,c\in R$，有$(a+b)\times c=a\times c + b\times c$与$a\times (b+c)=a\times b + a\times c$.").scale(0.7).next_to(2.5*DOWN + 6*LEFT)
        axioms = [axiom_1, axiom_2, axiom_3, axiom_4, axiom_5, axiom_6, axiom_7]
        self.play(LaggedStart(*[FadeIn(mob, 0.5*RIGHT) for mob in axioms], lag_ratio = 0.3, run_time = 2))
        self.waiting(0, 8) #就需要用到抽象代数的底子了
        self.waiting(0, 18) #（空闲）

        self.waiting(4, 19)
        self.play(*[FadeOut(mob) for mob in [ring, *axioms]]) #其实 这期视频的内容还挺适合作为年轻人的第一节抽象代数课的

        texts = r"\mathbb C", r"\mathbb R", r"\mathbb Q", r"\mathbb Z"
        rings = [MTex(texts[i]).scale(1.2).shift((i-1)*DOWN) for i in range(4)]
        special = [MTex(r"R[x]").scale(1.2).shift(5*LEFT), MTex(r"R[[x]]").scale(1.2).shift(5*RIGHT)]
        random_texts = [r"\mathbb Z[\sqrt5]", r"\mathbb Z[i]", r"\mathbb Z[\omega]", r"\mathbb Z(\frac{1+\sqrt{-19}}{2})", r"\mathbb Q(\sqrt2+\sqrt3)", r"\mathbb Q[x]/(x^3+x+1)", r"\mathbb Q[\sqrt2]", r"\mathbb Q(\pi)"]
        random_rings = [MTex(text).shift((random.randint(0, 1)-0.5)*4*RIGHT + (random.random()-0.5)*2*RIGHT + (random.random()-0.6)*5*UP).set_opacity((random.random()+1)/2).scale(0.6+random.random()*0.2) for text in random_texts]
        all_rings = random_rings + special
        random.shuffle(all_rings)
        self.play(LaggedStart(*[FadeIn(mob, 0.5*DOWN) for mob in rings], lag_ratio = 0.5, run_time = 1))
        self.play(LaggedStart(*[FadeInFromPoint(mob, mob.get_center()) for mob in all_rings], lag_ratio = 0.3, run_time = 2))
        self.waiting(0, 24) #可以让人认识到 数学中还有别的代数系统
        self.waiting(2, 11) #和我们熟悉的数截然不同
        self.waiting(0, 17) #（空闲）

        self.play(*[FadeOut(mob) for mob in [*rings, *all_rings]], function.animate.move_to(ORIGIN).scale(4/3))
        self.waiting(3, 12) #总之 母函数就是这么一种巧妙而自然的东西
        self.waiting(4, 21) #它的出现 就代表着附近一定有两种满足分配律的运算
        self.waiting(1, 24) #至少能构成一个环
        self.waiting(0, 20) #（空闲）

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
        self.remove(function).play(FadeInFromPoint(like1, 3*LEFT), FadeInFromPoint(coin1, ORIGIN), FadeInFromPoint(star1, 3*RIGHT))
        self.play(ApplyMethod(sanlian1.set_color, "#00A1D6"), *[Flash(mob, flash_radius=1, color = "#00A1D6") for mob in sanlian1])
        
        self.waiting(2-2, 18) #如果这期视频能让你感觉到这一点
        self.waiting(2, 4) #不妨一键三连支持一下
        self.waiting(0, 15) #到此共51秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

class Summary_2(Scene):

    def construct(self):
        notice1 = Notice("良心视频", "请　三连")
        notice2 = Notice("下期预告", "敬请期待")
        notice3 = Notice("良心up主", "请　关注")

        self.play(ReplacementTransform(notice1, notice2))
        self.waiting(2, 29) #下期视频我暂时不打算做第二个转折背后的原理

        texts = r"\mathbb C", r"\mathbb R", r"\mathbb Q", r"\mathbb Z"
        rings = [MTex(texts[i]).scale(1.2).shift((i-1)*DOWN) for i in range(4)]
        special = [MTex(r"R[x]").scale(1.2).shift(5*LEFT), MTex(r"R[[x]]").scale(1.2).shift(5*RIGHT)]
        random_texts = [r"\mathbb Z[\sqrt5]", r"\mathbb Z[i]", r"\mathbb Z[\omega]", r"\mathbb Z(\frac{1+\sqrt{-19}}{2})", r"\mathbb Q(\sqrt2+\sqrt3)", r"\mathbb Q[x]/(x^3+x+1)", r"\mathbb Q[\sqrt2]", r"\mathbb Q(\pi)"]
        random_rings = [MTex(text).shift((random.randint(0, 1)-0.5)*4*RIGHT + (random.random()-0.5)*2*RIGHT + (random.random()-0.5)*5*UP).set_opacity((random.random()+1)/2).scale(0.6+random.random()*0.2) for text in random_texts]
        all_rings = random_rings + special
        random.shuffle(all_rings)
        all_rings = rings + all_rings
        self.play(LaggedStart(*[FadeInFromPoint(mob, mob.get_center()) for mob in all_rings], lag_ratio = 0.3, run_time = 2))
        self.waiting(0, 20) #正如这期视频我想带给大家的那样
        self.waiting(2, 6) #数学中可以做加减乘除的
        self.waiting(3, 9) #除了复数 还有很多别的代数系统
        complex_field = Rectangle(stroke_color = ORANGE, stroke_width = 10, height = 5, width = 8.4)
        self.play(rings[0].animate.move_to(3*UP).set_color(ORANGE))
        self.play(ShowCreation(complex_field))
        self.waiting(1+2-2, 26+27) #但复数太好用了 所有的多项式都可以在里面找到根
        self.waiting(3, 8) #这就使得大家在第一次接触别的系统的时候
        self.waiting(1, 29) #会经常受到复数的影响
        self.waiting(0, 15) #（空闲）
        self.waiting(2, 13) #为了更加自然地呈现第二个转折
        self.play(*[FadeOut(mob) for mob in [*all_rings, complex_field]])
        self.waiting(0, 14) #我得再想想办法
        self.waiting(0, 22) #（空闲）

        radius = 0.5
        circle = Circle(radius = radius, color = YELLOW).shift(0.5*UP)
        point = Dot(color = RED).shift(radius*RIGHT).shift(0.5*UP)
        line = Line(radius * RIGHT, radius * RIGHT, color = [YELLOW, RED]).shift(0.5*UP)
        self.play(ShowCreation(circle))
        self.play(FadeIn(point, scale = np.infty))
        
        alpha = ValueTracker(0.0)
        def line_updater(mob: Line):
            value = alpha.get_value()
            start = radius * unit(value) + 0.5*UP
            end = start + radius * value * unit(value - PI/2)
            mob.put_start_and_end_on(start, end)
        def point_updater(mob: Dot):
            value = alpha.get_value()
            position = radius * (unit(value) + value * unit(value - PI/2)) + 0.5*UP
            mob.move_to(position)
        point.add_updater(point_updater)
        line.add_updater(line_updater)
        trace = TracedPath(point.get_center)
        self.add(trace, line, point).play(alpha.animate.set_value(PI/2), rate_func = rush_into)
        self.play(alpha.animate.set_value(3*PI/2), rate_func = linear)
        self.play(alpha.animate.set_value(TAU), rate_func = rush_from)
        point.clear_updaters()
        line.clear_updaters()
        trace.clear_updaters()
        circle.add(trace, line, point)
        self.play(circle.animate.scale(0.5, about_point = 0.5*UP).shift(4*LEFT + 2*UP))

        function_1 = lambda t: np.array([2*t + np.sin(2*t), 1 - np.cos(2*t), 0])
        function_2 = lambda t: np.array([2*t - np.sin(2*t), np.cos(2*t) - 1, 0])
        cycloid = ParametricCurve(function_1, [0, PI, PI/100], color = YELLOW).shift(PI/2*LEFT)
        point = Dot(color = RED).shift(PI/2*LEFT)
        line = Line(PI/2*LEFT, PI/2*LEFT, color = [YELLOW, RED]).shift(0.5*UP)
        self.play(ShowCreation(cycloid))
        self.play(FadeIn(point, scale = np.infty))

        alpha = ValueTracker(0.0)
        def line_updater(mob: Line):
            value = alpha.get_value()
            start = function_1(value) + PI/2*LEFT
            end = function_2(value) + PI/2*LEFT
            mob.put_start_and_end_on(start, end)
        def point_updater(mob: Dot):
            value = alpha.get_value()
            position = function_2(value) + PI/2*LEFT
            mob.move_to(position)
        point.add_updater(point_updater)
        line.add_updater(line_updater)
        trace = TracedPath(point.get_center)
        self.add(trace, line, point).play(alpha.animate.set_value(PI/4), rate_func = rush_into)
        self.play(alpha.animate.set_value(3*PI/4), rate_func = linear)
        self.play(alpha.animate.set_value(PI), rate_func = rush_from)
        point.clear_updaters()
        line.clear_updaters()
        trace.clear_updaters()
        cycloid.add(trace, line, point)
        self.play(cycloid.animate.scale(0.5).shift((4+PI/2)*LEFT + 1*DOWN))

        function_1 = lambda t: 2*np.exp(-t)*(np.sin(t) - np.cos(t))
        function_2 = lambda t: 2*np.exp(-t)*(-np.sin(t) - np.cos(t))
        function_3 = lambda t: 2*np.exp(-t)*(-np.sin(t) + np.cos(t))
        function_4 = lambda t: 2*np.exp(-t)*(np.sin(t) + np.cos(t))
        point_1 = Dot(color = RED).shift(2*DOWN)
        point_2 = Dot(color = RED).shift(2*DOWN + 4* RIGHT)
        point_3 = Dot(color = RED).shift(2*UP + 4* RIGHT)
        point_4 = Dot(color = RED).shift(2*UP)
        square = Square(side_length = 4, color = YELLOW).shift(2*RIGHT)
        self.play(ShowCreation(square))
        self.play(*[FadeIn(mob) for mob in [point_1, point_2, point_3, point_4]])

        alpha = ValueTracker(1.0)
        def point_updater_1(mob: Dot):
            value = alpha.get_value()
            if value == 0:
                position = 2*RIGHT
            else:
                value = -np.log(value)
                position = np.array([function_1(value) + 2, function_2(value), 0])
            mob.move_to(position)
        def point_updater_2(mob: Dot):
            value = alpha.get_value()
            if value == 0:
                position = 2*RIGHT
            else:
                value = -np.log(value)
                position = np.array([function_2(value) + 2, function_3(value), 0])
            mob.move_to(position)
        def point_updater_3(mob: Dot):
            value = alpha.get_value()
            if value == 0:
                position = 2*RIGHT
            else:
                value = -np.log(value)
                position = np.array([function_3(value) + 2, function_4(value), 0])
            mob.move_to(position)
        def point_updater_4(mob: Dot):
            value = alpha.get_value()
            if value == 0:
                position = 2*RIGHT
            else:
                value = -np.log(value)
                position = np.array([function_4(value) + 2, function_1(value), 0])
            mob.move_to(position)
        point_1.add_updater(point_updater_1)
        point_2.add_updater(point_updater_2)
        point_3.add_updater(point_updater_3)
        point_4.add_updater(point_updater_4)
        trace_1 = TracedPath(point_1.get_center)
        trace_2 = TracedPath(point_2.get_center)
        trace_3 = TracedPath(point_3.get_center)
        trace_4 = TracedPath(point_4.get_center)

        self.add(trace_1, trace_2, trace_3, trace_4, point_1, point_2, point_3, point_4).play(alpha.animate.set_value(0.0), run_time = 2, rate_func = linear)
        for mob in [trace_1, trace_2, trace_3, trace_4, point_1, point_2, point_3, point_4]:
            mob.clear_updaters()
        self.waiting(3+1+2+3+0+4+2+0 - 17, 3+28+6+22+16+1+13+20) #下期视频的内容是渐屈线与渐伸线 这是一对非常常见的概念 但出现的地方非常散碎 也没有人从这些散碎中总结出什么漂亮的东西来 （空闲） 在下期视频 我们就一起来看看这些散碎背后 有什么样统一而精妙的规律 （空闲）
        self.play(*[FadeOut(mob) for mob in [circle, cycloid, square, trace_1, trace_2, trace_3, trace_4, point_1, point_2, point_3, point_4]])

        like = Text("", font = 'vanfont')
        coin = Text("", font = 'vanfont')
        star = Text("", font = 'vanfont')
        share = Text("", font = 'vanfont')

        land = Line(np.array([-8,0,0]), np.array([8,0,0]))
        water = Polygon(np.array([-4,0,0]), np.array([-6,0,0]), np.array([-5,-4,0]), np.array([6,-4,0]), fill_color = BLUE_E, fill_opacity = 0.5, stroke_width = 0)
        band1 = Line(np.array([-6,0,0]), np.array([-5,-4,0]), color = BLUE)
        band2 = Line(np.array([-4,0,0]), np.array([6,-4,0]), color = BLUE)
        river = VGroup(water, band1, band2)
        moon = Circle(radius = 1.2, arc_center = np.array([-5,2,0]), fill_color = WHITE, fill_opacity = 0.9, stroke_width = 0)

        star0 = star.copy().set_color(BLUE).shift(UP)
        star2 = star0.copy().shift(1.3*UP-1.7*RIGHT)
        star3 = star0.copy().shift(2.2*UP+2.6*RIGHT)
        star4 = star0.copy().shift(0.3*UP+2.2*RIGHT)
        star5 = star0.copy().shift(-0.2*UP+6.0*RIGHT)
        star5_1 = coin.copy().set_color(BLUE).shift(2.7*UP+1.6*RIGHT)
        bigstars = VGroup(star2, star3, star4, star5, star5_1)
        star00 = star0.copy().scale(0.7)
        star6 = star00.copy().shift(1.4*UP+4.0*RIGHT)
        star7 = star00.copy().shift(1.7*UP+0.2*RIGHT)
        star8 = star00.copy().shift(0.4*UP+4.3*RIGHT)
        star9 = star00.copy().shift(0.1*UP-3.2*RIGHT)
        star10 = star00.copy().shift(-0.1*UP-2.5*RIGHT)
        star10_1 = like.copy().set_color(BLUE).scale(0.7).shift(2.5*UP-2.7*RIGHT)
        star10_2 = share.copy().set_color(BLUE).scale(0.7).shift(3.2*UP-0.7*RIGHT)
        smallstars = VGroup(star6, star7, star8, star9, star10, star10_1, star10_2)
        star000 = star0.copy().scale(0.4)
        star11 = star000.copy().shift(0.5*UP-1.3*RIGHT)
        star12 = star000.copy().shift(0.8*UP+0.8*RIGHT)
        star13 = star000.copy().shift(-0.2*UP+3.1*RIGHT)
        star14 = star000.copy().shift(1.1*UP+2.7*RIGHT)
        star15 = star000.copy().shift(1.2*UP-0.5*RIGHT)
        star16 = star000.copy().shift(2.2*UP-1.8*RIGHT)
        stardust = VGroup(star11, star12, star13, star14, star15, star16)
        stars = VGroup(bigstars, smallstars, stardust)
        painting = VGroup(river, land, moon, star0, stars)
        painting_others = VGroup(river, land, moon, stars)
        self.play(FadeIn(painting, lag_ratio = 0.01, run_time = 2), ReplacementTransform(notice2, notice3))
        self.waiting(0, 1) #知识的星空浩如烟海

        picture_photo = ImageMobject("picture_photo.png", height = 2).move_to(5*RIGHT+1.3*DOWN)
        text_name = Text("乐正垂星", font = "simhei").move_to(2.5*RIGHT+1.3*DOWN)
        self.play(FadeIn(picture_photo, 0.5*UP), FadeIn(text_name, 0.5*UP))
        self.waiting(1, 16) #而我 就像我的名字一样

        self.play(FadeOut(painting_others), FadeOut(picture_photo), FadeOut(text_name), ApplyMethod(star0.shift, DOWN))
        self.waiting(1, 8) #想要把天上的星星垂下来

        star_copy = star0.copy()
        apple1 = Circle(radius = 0.5, arc_center = np.array([0,0,0]), color = BLACK, fill_color = RED, fill_opacity = 1, stroke_width = 8)
        apple2 = Circle(radius = 0.1, arc_center = np.array([0,0.3,0]), fill_color = BLACK, fill_opacity = 1, stroke_width = 0)
        apple3 = Arc(radius = 2, angle = PI/12, start_angle = PI-PI/12, color = BLACK, arc_center = np.array([2,0.3,0]), stroke_width = 8)
        apple = VGroup(apple1, apple2, apple3)
        apple.scale(0.8)
        self.play(Transform(star0, apple))
        self.waiting(1, 2) #变成触手可及的果实

        snowflake = SnowFlake()
        snowflake_2 = snowflake.copy().set_color(RED).set_stroke(width = 1.5)
        snowflake_3 = snowflake.copy().set_color(BLUE).set_stroke(width = 2)
        anims = LaggedStart(SpreadOut(snowflake_2).update_config(rate_func = linear), SpreadOut(snowflake_3).update_config(rate_func = linear), SpreadOut(snowflake).update_config(rate_func = linear), rate_func = rush_into, run_time = 2)
        self.play(Transform(star0, star_copy), anims)
        self.remove(snowflake_2, snowflake_3) 
        #self.waiting(0, 0) #变成指引前路的火光
        self.waiting(0, 18) #（空闲）
        
        self.remove(star0, snowflake)
        picture_photo.move_to(1.5*LEFT)
        text_name.move_to(RIGHT)
        self.play(FadeIn(picture_photo, UP), FadeIn(text_name, UP))
        self.waiting(2, 13) #我是乐正垂星 我们下期视频再见

        self.waiting(6, 5)
        self.play(FadeOut(picture_photo), FadeOut(text_name), FadeOut(notice3))
        self.waiting(6) #到此共74秒

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

###############################################################################

class Template(Scene):
    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)