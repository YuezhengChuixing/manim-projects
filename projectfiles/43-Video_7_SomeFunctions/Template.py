from manimlib import *
import numpy as np
import __future__

class Template(Scene):
    def construct(self):

        print(self.num_plays, self.time)

    def waiting(self, second, frame = 0):
        self.wait(second + frame/30)

#######################################################################

# This part of code is copied from 3b1b's 

def get_set_tex(values, max_shown=7, **kwargs):
    if len(values) > max_shown:
        value_mobs = [
            *map(Integer, values[:max_shown - 2]),
            MTex("\\dots"),
            Integer(values[-1], group_with_commas=False),
        ]
    else:
        value_mobs = list(map(Integer, values))

    commas = MTex(",").replicate(len(value_mobs) - 1)
    result = VGroup()
    result.add(MTex("\\{"))
    result.add(*it.chain(*zip(value_mobs, commas)))
    if len(value_mobs) > 0:
        result.add(value_mobs[-1].align_to(value_mobs[0], UP))
    result.add(MTex("\\}"))
    result.arrange(RIGHT, buff=SMALL_BUFF)
    if len(values) > 0:
        commas.set_y(value_mobs[0].get_y(DOWN))
    if len(values) > max_shown:
        result[-4].match_y(commas)
    result.values = values
    return result

def get_brackets(set_tex):
    return VGroup(set_tex[0], set_tex[-1])

def set_tex_transform(set_tex1, set_tex2):
    bracket_anim = TransformFromCopy(
        get_brackets(set_tex1),
        get_brackets(set_tex2),
    )
    matching_anims = [
        TransformFromCopy(
            get_part_by_value(set_tex1, value),
            get_part_by_value(set_tex2, value),
        )
        for value in filter(
            lambda v: v in set_tex2.values,
            set_tex1.values,
        )
    ]
    mismatch_animations = [
        FadeInFromPoint(
            get_part_by_value(set_tex2, value),
            set_tex1.get_center()
        )
        for value in set(set_tex2.values).difference(set_tex1.values)
    ]
    anims = [bracket_anim, *matching_anims, *mismatch_animations]
    if len(set_tex2.values) > 1:
        commas = []
        for st in set_tex1, set_tex2:
            if len(st.values) > 1:
                commas.append(st[2:-1:2])
            else:
                commas.append(MTex(",").set_opacity(0).move_to(st, DOWN))
        comma_animations = TransformFromCopy(*commas)
        anims.append(comma_animations)
    for part in set_tex2:
        if isinstance(part, MTex) and part.get_tex() == "\\dots":
            anims.append(FadeInFromPoint(part, set_tex1.get_bottom()))
    return AnimationGroup(*anims)

def get_sum_animation(set_tex, sum_group, path_arc=-10 * DEGREES):
    arrow, sum_value = sum_group

    return AnimationGroup(
        GrowArrow(arrow),
        FadeTransform(
            get_integer_parts(set_tex).copy(),
            sum_value,
            path_arc=path_arc,
        ),
    )

def get_part_by_value(set_tex, value):
    try:
        return next(sm for sm in set_tex if isinstance(sm, Integer) and sm.get_value() == value)
    except StopIteration:
        return VMobject().move_to(set_tex)

def get_integer_parts(set_tex):
    result = VGroup(*(
        sm for sm in set_tex
        if isinstance(sm, Integer)
    ))
    if len(result) == 0:
        result.move_to(set_tex)
    return result

def get_subsets(full_set):
    return list(it.chain(*(
        it.combinations(full_set, k)
        for k in range(len(full_set) + 1)
    )))

def get_sum_group(set_tex, sum_color=YELLOW):
    height = set_tex.get_height()
    buff = 0.75 * height
    arrow = Vector(height * RIGHT)
    arrow.next_to(set_tex, RIGHT, buff=buff)
    sum_value = MTex(str(int(sum(set_tex.values))))
    sum_value.set_color(sum_color)
    sum_value.set_height(0.66 * height)
    sum_value.next_to(arrow, RIGHT, buff=buff)

    return VGroup(arrow, sum_value)

class ExampleWith5(InteractiveScene):
    elem_colors = color_gradient([BLUE_B, BLUE_D], 5)

    def construct(self):
        # Show all subsets
        N = 5
        full_set = list(range(1, N + 1))
        set_tex = get_set_tex(full_set)
        set_tex.to_edge(UP)
        self.add(set_tex)
        self.wait()

        # Show n choose k stacks
        stacks = self.get_subset_stacks(full_set)

        anims = []
        for stack in stacks:
            for new_subset in stack:
                anims.append(set_tex_transform(set_tex, new_subset))

        self.play(LaggedStart(*anims, lag_ratio=0.05))
        self.wait()

        # Show their sums
        sum_stacks = self.get_subset_sums(stacks)
        covered_sums = []
        n_selections = 6
        for n in range(n_selections):
            self.wait(note=f"Example sum {n + 1} / {n_selections}")
            # Show sum based on what's in self.selection
            anims = []
            for stack, sum_stack in zip(stacks, sum_stacks):
                for subset, sum_mob in zip(stack, sum_stack):
                    if set(subset.get_family()).intersection(self.selection.get_family()):
                        if sum_mob not in covered_sums:
                            covered_sums.append(sum_mob)
                            anims.append(get_sum_animation(subset, sum_mob))
            self.clear_selection()
            self.play(LaggedStart(*anims))
        self.add(sum_stacks)

        # Isolate counts we care about
        self.highlight_multiple_of_5(stacks, sum_stacks)

        # Count total
        stack_group = VGroup(stacks, sum_stacks, self.highlight_rects)
        stack_group.save_state()
        stack_group.generate_target()
        stack_group.target[:2].set_opacity(1)
        stack_group.target.set_height(4)
        stack_group.target.center().to_edge(DOWN, buff=LARGE_BUFF)

        stack_group_rect = SurroundingRectangle(stack_group.target, buff=MED_LARGE_BUFF)
        stack_group_rect.round_corners(radius=0.5)
        stack_group_rect.set_stroke(BLUE, 2)

        count = TexText(
            "Total subsets:", " $2^5 = 32$"
        )
        count.set_color_by_tex("32", BLUE)
        count.next_to(stack_group_rect, UP)
        counter = Integer(32)
        counter.add_updater(lambda c: c.set_color(BLUE))
        counter.next_to(count[0], RIGHT)

        self.play(
            MoveToTarget(stack_group),
            FadeIn(stack_group_rect, scale=0.8),
        )

        highlights = VGroup()
        for stack in stacks:
            for subset in stack:
                highlights.add(VHighlight(subset))

        self.add(highlights, stack_group)
        self.play(
            Write(count[0]),
            ShowIncreasingSubsets(highlights, run_time=5),
            CountInFrom(counter, 0, run_time=5),
        )
        self.play(
            Transform(counter, count[1][-2:]),
            Write(count[1][:-2]),
            FadeOut(highlights)
        )
        self.remove(counter)
        self.add(count)
        self.wait()

        # Ask about construction
        questions = VGroup(
            Text("How do you\ncount these?", font_size=36),
            Text(
                "How do you\nconstruct these?",
                t2c={"construct": YELLOW},
                t2s={"construct": ITALIC},
                font_size=36,
            )
        )

        for question in questions:
            question.to_corner(UL)

        count_word = questions[0].get_part_by_text("count")
        construct_word = questions[1].get_part_by_text("construct")
        cross = Cross(count_word)
        cross.scale(1.5)

        arrow = Arrow(questions[0], count.get_left())

        self.play(
            Write(questions[0]),
            ShowCreation(arrow),
        )
        self.wait()
        self.play(ShowCreation(cross))
        self.play(
            VGroup(count_word, cross).animate.shift(0.75 * DOWN),
            Write(construct_word),
            questions[0][-len("these?"):].animate.move_to(questions[1][-1], RIGHT),
        )
        self.wait()
        to_fade = VGroup(
            questions[0], construct_word, cross, arrow,
            stack_group_rect, count, *stack_group, self.counter,
        )
        self.play(LaggedStartMap(FadeOut, to_fade, run_time=1.5, lag_ratio=0.25))

        # Construct all subsets
        subsets = self.construct_all_subsets(set_tex)

        # Show reorganizations
        stack_group.restore()
        stack_group[:2].set_opacity(2)
        anims = []
        for stack in stacks:
            for new_subset in stack:
                for subset in subsets:
                    if set(subset.values) == set(new_subset.values):
                        anims.append(FadeTransform(subset, new_subset))

        self.play(LaggedStart(*anims, lag_ratio=0.05))
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, sum_stacks, run_time=1),
            LaggedStartMap(FadeIn, self.highlight_rects, run_time=1),
        )
        self.wait()
        self.group_by_sum(stacks, sum_stacks)

        # Show generating function
        self.show_generating_function(set_tex)
        self.transition_to_full_generating_function(set_tex)

    def construct_all_subsets(self, set_tex):
        # Preview binary choices
        value_parts = VGroup(*(
            get_part_by_value(set_tex, v) for v in range(1, 6)
        ))
        rects = VGroup(*(
            SurroundingRectangle(vp, buff=0.1).round_corners()
            for vp in value_parts
        ))
        rects.set_stroke(BLUE, 2)

        words = Text("5 binary choices")
        words.next_to(set_tex, DOWN, buff=1.5)
        lines = VGroup(*(
            Line(words.get_top(), rect.get_bottom(), buff=0.15)
            for rect in rects
        ))
        lines.match_style(rects)

        def match_n(rects, n):
            bits = it.chain(
                str(bin(n)[-1:1:-1]),
                it.repeat("0")
            )
            for rect, bit in zip(rects, bits):
                rect.set_stroke(opacity=float(bit == "1"))

        self.add(rects)
        self.play(
            Write(words),
            Write(lines),
            UpdateFromAlphaFunc(
                rects, lambda r, a: match_n(r, int(31 * a)),
                run_time=4,
                rate_func=linear,
            )
        )
        self.wait()
        self.play(
            FadeOut(rects),
            LaggedStartMap(Uncreate, lines),
            FadeOut(words, 0.1 * DOWN),
        )

        # Show construction
        subsets = VGroup(get_set_tex([]))
        for value in range(1, 6):
            value_mob = get_part_by_value(set_tex, value)
            marks = VGroup(Text(r"✗"), MTex(r"\checkmark"))
            marks.match_height(value_mob)
            marks.next_to(value_mob, DOWN)

            subsets.generate_target()
            added_subsets = VGroup(*(
                get_set_tex([*ss.values, value]).move_to(ss)
                for ss in subsets
            ))
            for ss in added_subsets:
                self.color_set_tex(ss)
                get_integer_parts(ss)[-1].set_opacity(0)

            vect = [RIGHT, DOWN, RIGHT, DOWN, RIGHT][value - 1]
            buff = [2.25, 0.75, 2.0, 0.75, 1.0][value - 1]
            added_subsets.next_to(subsets, vect, buff=buff)
            new_subsets = VGroup(*subsets.target, *added_subsets)
            new_subsets.set_max_width(FRAME_WIDTH - 1)
            new_subsets.center()
            subsets_copy = subsets.copy()
            for ssc, nss in zip(subsets_copy, added_subsets):
                ssc.match_height(nss)
                ssc.move_to(nss)

            self.wait()
            elem = get_part_by_value(set_tex, value)
            self.play(
                elem.animate.set_color(self.elem_colors[value - 1]),
                FlashAround(elem, color=self.elem_colors[value - 1]),
            )
            if value == 1:
                self.play(set_tex_transform(set_tex, subsets[0]))
                self.add(subsets)
                self.wait()
            self.play(
                MoveToTarget(subsets, path_arc=30 * DEGREES),
                ReplacementTransform(
                    subsets.copy(),
                    subsets_copy,
                    path_arc=30 * DEGREES,
                )
            )
            self.remove(subsets_copy)
            self.play(
                LaggedStart(*(
                    Transform(
                        elem.copy(),
                        get_integer_parts(st)[-1].copy().set_opacity(1),
                        remover=True,
                    )
                    for st in added_subsets
                ), lag_ratio=0.1),
                *(
                    set_tex_transform(st1, st2)
                    for st1, st2 in zip(subsets_copy, added_subsets)
                )
            )
            self.remove(subsets_copy, new_subsets)
            subsets.set_submobjects(list(new_subsets))
            self.add(subsets)
            subsets.set_opacity(1)
            self.wait()
        self.wait()

        # Equation
        equation = MTex("2 \\cdot 2 \\cdot 2 \\cdot 2 \\cdot 2 = 2^5 = 32")
        equation.set_width(4)
        equation.to_corner(UL)
        equation.set_color(YELLOW)
        self.play(Write(equation))
        self.wait()
        self.play(FadeOut(equation))

        return subsets

    def highlight_multiple_of_5(self, stacks, sum_stacks):
        # Blah
        rects = VGroup()
        anims = []
        for stack, sum_stack in zip(stacks, sum_stacks):
            for set_tex, sum_group in zip(stack, sum_stack):
                if sum(set_tex.values) % 5 == 0:
                    rect = SurroundingRectangle(VGroup(set_tex, sum_group))
                    rect.value = sum(set_tex.values)
                    rects.add(rect)
                else:
                    anims.append(set_tex.animate.set_opacity(0.25))
                    anims.append(sum_group.animate.set_opacity(0.25))
        rects.set_stroke(TEAL, 2)
        for rect in rects:
            rect.round_corners()

        counter = Integer(0, font_size=72)
        counter.to_corner(UR)
        counter.set_color(TEAL)

        self.play(*anims, run_time=1)
        self.wait()
        self.play(
            FadeIn(rects, lag_ratio=0.9),
            ChangeDecimalToValue(counter, len(rects)),
            run_time=1.5
        )
        self.wait()

        self.highlight_rects = rects
        self.counter = counter

    def group_by_sum(self, stacks, sum_stacks):
        # Lock sums to subsets
        subset_groups = VGroup()
        for stack, sum_stack in zip(stacks, sum_stacks):
            for set_tex, sum_group in zip(stack, sum_stack):
                set_tex.sum_group = sum_group
                sum_group.set_tex = set_tex
                subset_groups.add(VGroup(set_tex, sum_group))

        # Reorganize
        common_sum_stacks = VGroup()
        max_sum = max(sum(ssg[0].values) for ssg in subset_groups)
        for n in range(max_sum + 1):
            stack = VGroup(*filter(
                lambda ssg: sum(ssg[0].values) == n,
                subset_groups
            ))
            common_sum_stacks.add(stack)

        common_sum_stacks.generate_target()
        csst = common_sum_stacks.target
        for stack in common_sum_stacks.target:
            stack.arrange(DOWN, aligned_edge=RIGHT, buff=SMALL_BUFF)

        csst.arrange_in_grid(4, 5, buff=MED_LARGE_BUFF, aligned_edge=RIGHT)
        csst[10:15].set_y(np.mean([csst[5].get_y(DOWN), csst[15].get_y(UP)]))
        csst.refresh_bounding_box()
        csst.set_width(FRAME_WIDTH - 1)
        csst.to_corner(DL)
        csst.set_opacity(1)

        # Create new rectangles
        common_sum_rects = VGroup()
        for stack in common_sum_stacks.target:
            rect = SurroundingRectangle(stack, buff=SMALL_BUFF)
            rect.round_corners(radius=0.05)
            rect.value = sum(stack[0][0].values)
            color = TEAL if rect.value % 5 == 0 else GREY_B
            rect.set_stroke(color, 1)
            common_sum_rects.add(rect)

        rect_anims = []
        for highlight_rect in self.highlight_rects:
            for rect in common_sum_rects:
                if rect.value == highlight_rect.value:
                    rect_anims.append(Transform(highlight_rect, rect))

        # Transition to common sum
        self.play(
            MoveToTarget(common_sum_stacks),
            *rect_anims,
            run_time=2
        )
        self.play(
            FadeOut(self.highlight_rects),
            FadeIn(common_sum_rects),
        )
        self.wait()

        self.subset_groups = subset_groups
        self.common_sum_stacks = common_sum_stacks
        self.common_sum_rects = common_sum_rects

    def show_generating_function(self, set_tex):
        # Setup expressions
        css = self.common_sum_stacks
        csr = self.common_sum_rects
        lower_group = self.lower_group = VGroup(csr, css)

        factored_terms = "(1 + x^1)", "(1 + x^2)", "(1 + x^3)", "(1 + x^4)", "(1 + x^5)"
        factored = MTex("".join(factored_terms), isolate=factored_terms)
        expanded_terms = ["1"]
        for n in range(1, 16):
            k = len(css[n])
            expanded_terms.append((str(k) if k > 1 else "") + f"x^{{{n}}}")
        expanded = MTex("+".join(expanded_terms), isolate=["+", *expanded_terms])
        expanded.set_width(FRAME_WIDTH - 1)
        factored.next_to(set_tex, DOWN, MED_LARGE_BUFF)
        expanded.next_to(factored, DOWN, MED_LARGE_BUFF)

        self.play(Write(factored))
        self.wait()
        self.play(lower_group.animate.set_height(3.0, about_edge=DOWN))

        # Emphasize 5 binary choices
        parts = VGroup(*(
            factored.get_part_by_tex(term)
            for term in factored_terms
        ))
        rects = VGroup(*(
            SurroundingRectangle(part, buff=0.05).round_corners()
            for part in parts
        ))
        rects.set_stroke(BLUE, 2)
        words = Text("5 binary choices", color=BLUE)
        words.next_to(rects, DOWN, MED_LARGE_BUFF)

        self.play(
            LaggedStartMap(
                VFadeInThenOut, rects,
                lag_ratio=0.25,
                run_time=4,
            ),
            Write(words),
        )
        self.play(FadeOut(words))

        # Animate expansion
        fac_term_parts = [factored.get_part_by_tex(term) for term in factored_terms]
        expanded_parts = [expanded.get_part_by_tex(term) for term in expanded_terms]
        super_expanded = VGroup()
        super_expanded.next_to(factored, DOWN, MED_LARGE_BUFF)
        collection_anims = []

        subset_groups = self.subset_groups
        subset_groups.submobjects.sort(
            key=lambda ssg: sum(ssg[0].values)
        )

        for subset_group in subset_groups:
            bits = [i + 1 in subset_group[0].values for i in range(5)]
            top_terms = [
                part[3:-1] if bit else part[1]
                for bit, part in zip(bits, fac_term_parts)
            ]
            top_rects = VGroup(*(
                SurroundingRectangle(part).set_stroke(BLUE, 2).round_corners()
                for part in top_terms
            ))
            n = sum(b * k for k, b in zip(range(1, 6), bits))
            if n == 0:
                new_term = MTex("1", font_size=36)
                super_expanded.add(new_term)
            else:
                new_plus = MTex("+", font_size=36)
                new_term = MTex(f"x^{{{n}}}", font_size=36)
                super_expanded.add(new_plus, new_term)
                collection_anims.append(FadeOut(new_plus))
            super_expanded.arrange(RIGHT, aligned_edge=DOWN, buff=SMALL_BUFF)
            super_expanded.next_to(factored, DOWN, MED_LARGE_BUFF)
            super_expanded.to_edge(LEFT)
            if len(super_expanded) > 33:
                super_expanded[33:].next_to(
                    super_expanded[0], DOWN, MED_LARGE_BUFF, aligned_edge=LEFT
                )
            low_rect = SurroundingRectangle(new_term, buff=0.5 * SMALL_BUFF)
            low_rect.set_stroke(BLUE, 2).round_corners()
            collection_anims.append(
                FadeTransform(new_term, expanded_parts[n], path_arc=10 * DEGREES)
            )

            self.add(top_rects)
            self.add(super_expanded, low_rect)
            subset_groups.set_opacity(0.25)
            subset_group.set_opacity(1)
            self.wait()
            self.remove(top_rects, low_rect)
        self.wait()

        # Reorganize to expanded
        lower_group.generate_target()
        lower_group.target.set_height(4, about_edge=DOWN)
        lower_group.target[1].set_opacity(1)
        self.play(
            LaggedStart(*collection_anims),
            LaggedStartMap(FadeIn, expanded.get_parts_by_tex("+")),
            MoveToTarget(
                lower_group,
                rate_func=squish_rate_func(smooth, 0.5, 1.0)
            ),
            run_time=3,
        )
        self.add(expanded)
        self.wait(note="Highlight multiples of 5")

        self.factored_func = factored
        self.expanded_func = expanded

    def transition_to_full_generating_function(self, set_tex):
        # Expressions
        factored = MTex(
            "f(x) = (1 + x^1)(1 + x^2)(1 + x^3) \\cdots \\left(1 + x^{1{,}999}\\right)\\left(1 + x^{2{,}000}\\right)",
        )
        expanded = MTex(
            "f(x) = 1+x+x^{2}+2 x^{3}+2 x^{4}+ 3x^{5} +\\cdots + x^{2{,}001{,}000}",
            isolate="+",
        )
        new_set_tex = get_set_tex(range(1, 2001))
        new_set_tex.move_to(set_tex)
        self.color_set_tex(new_set_tex)
        get_integer_parts(new_set_tex)[-1].set_color(
            interpolate_color(BLUE_E, BLUE_D, 0.5)
        )

        h_line = Line(LEFT, RIGHT).set_width(FRAME_WIDTH)
        h_line.set_stroke(GREY_C, 1)
        h_line.set_y(0.5)

        factored_word = Text("Factored", font_size=60, color=BLUE_B)
        factored_word.next_to(set_tex, DOWN, MED_LARGE_BUFF)
        factored.next_to(factored_word, DOWN, MED_LARGE_BUFF)
        expanded_word = Text("Expanded", font_size=60, color=TEAL)
        expanded_word.next_to(h_line, DOWN, LARGE_BUFF)
        expanded.next_to(expanded_word, DOWN, MED_LARGE_BUFF)
        for mob in [factored, factored_word, expanded, expanded_word]:
            mob.to_edge(LEFT)

        self.play(
            TransformMatchingShapes(set_tex, new_set_tex),
            FadeTransform(self.factored_func, factored),
            FadeIn(factored_word, scale=2.0),
            FadeOut(self.expanded_func, 2 * DOWN),
            FadeOut(self.lower_group, DOWN),
        )
        self.wait()
        self.play(
            ShowCreation(h_line),
            FadeIn(expanded_word),
            Write(expanded)
        )
        self.wait()

        # Show example term
        n = 25
        subsets = list(filter(
            lambda s: sum(s) == n,
            get_subsets(range(1, n))
        ))
        coef = len(subsets)
        term = Tex(str(coef), f"x^{{{n}}}", "+", "\\cdots")
        term[:2].set_color(TEAL)
        term[2:].set_color(WHITE)
        tail = expanded[-11:]
        term.move_to(tail, DL)
        tail.generate_target()
        tail.target.next_to(term, RIGHT, buff=0.15, aligned_edge=DOWN)

        self.play(
            Write(term),
            MoveToTarget(tail),
        )
        self.wait()

        subset_mobs = VGroup(*map(get_set_tex, subsets))
        subset_mobs.arrange_in_grid(n_cols=10)
        subset_mobs.set_width(FRAME_WIDTH - 1)
        subset_mobs.to_edge(UP)
        subset_mobs.set_color(TEAL)
        top_rect = FullScreenFadeRectangle()
        top_rect.set_fill(BLACK, opacity=0.9)
        top_rect.set_height(4, about_edge=UP, stretch=True)

        term_rect = SurroundingRectangle(term[:2])
        term_rect.round_corners()
        term_rect.set_stroke(YELLOW, 2)
        term_words = Text("Is there a snazzy\nway to deduce this?", font_size=36)
        term_words.next_to(term_rect, DOWN)
        term_words.set_color(YELLOW)

        self.play(
            FadeIn(top_rect),
            ShowIncreasingSubsets(subset_mobs, run_time=5)
        )
        self.wait()
        self.play(
            ShowCreation(term_rect),
            Write(term_words),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, subset_mobs, shift=0.2 * UP),
            FadeOut(top_rect, rate_func=squish_rate_func(smooth, 0.6, 1)),
            run_time=3
        )
        self.wait()

    ##

    def color_set_tex(self, set_tex):
        for value in set_tex.values:
            elem = get_part_by_value(set_tex, value)
            if value - 1 < len(self.elem_colors):
                elem.set_color(self.elem_colors[value - 1])

    def get_subset_stacks(self, full_set, buff=3.5):
        stacks = VGroup(*(
            VGroup(*(
                get_set_tex(subset)
                for subset in it.combinations(full_set, k)
            ))
            for k in range(len(full_set) + 1)
        ))
        for stack in stacks:
            stack.arrange(DOWN)
            for ss in stack:
                self.color_set_tex(ss)
        stacks.arrange(RIGHT, buff=buff, aligned_edge=DOWN)

        stacks[0].move_to(stacks[1]).align_to(stacks[2], UP)
        stacks[4].align_to(stacks[3], UP)
        stacks[5].match_x(stacks[4])

        stacks.set_max_height(FRAME_HEIGHT - 3)
        stacks.set_max_width(FRAME_WIDTH - 2)
        stacks.center().to_edge(DOWN)
        return stacks

    def get_subset_sums(self, stacks):
        return VGroup(*(
            VGroup(*(
                get_sum_group(set_tex)
                for set_tex in stack
            ))
            for stack in stacks
        ))

#######################################################################
# This part of code acknowledges the above part

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

class CopyFrom5(InteractiveScene):
    def construct(self):
        # Show all subsets
        N = 5
        full_set = list(range(1, N + 1))
        set_tex = get_set_tex(full_set).shift(3*UP)
        self.add(set_tex)
        self.wait()

        # Show n choose k stacks
        subsets = get_subsets(full_set)
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
        stacks.set_height(3.5).next_to(3*DOWN, UP, buff = 0).set_opacity(1)

        # Create new rectangles
        rects = VGroup(*[SurroundingRectangle(stack, buff = 0.1, stroke_width = 1, stroke_color = GREY_B).round_corners(radius=0.05) for stack in stacks])

        # Transition to common sum
        self.play(FadeIn(stacks), run_time=2)
        self.play(Write(rects))
        self.wait()

        # Show generating function
        factored_terms = "(1 + x^1)", "(1 + x^2)", "(1 + x^3)", "(1 + x^4)", "(1 + x^5)"
        factored = MTex("".join(factored_terms), isolate=factored_terms).scale(0.8).next_to(set_tex, DOWN)
        expanded_terms = ["1"]
        for n in range(1, 16):
            k = len(stacks[n])
            expanded_terms.append((str(k) if k > 1 else "") + f"x^{{{n}}}")
        expanded = MTex("+".join(expanded_terms), isolate=["+", *expanded_terms]).set_width(FRAME_WIDTH - 1).next_to(factored, DOWN)

        self.play(Write(factored))
        self.play(Write(expanded))
        self.wait()

        # Animate expansion
        fac_term_parts = [factored.get_part_by_tex(term) for term in factored_terms]
        expanded_parts = [expanded.get_part_by_tex(term) for term in expanded_terms]
        
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
        self.add(super_expanded)
        self.remove(expanded)
        
        for i in range(32):
            top_terms = [
                part[3:-1] if bit else part[1]
                for bit, part in zip(subsets[i][0].bits, fac_term_parts)
            ]
            top_rects = VGroup(*[SurroundingRectangle(part).set_stroke(BLUE, 2).round_corners() for part in top_terms])
            low_rect = SurroundingRectangle(super_expanded[2*i], buff=0.5 * SMALL_BUFF).set_stroke(BLUE, 2).round_corners()
            
            self.add(top_rects, low_rect)
            subsets.set_opacity(0.25)
            subsets[i].set_opacity(1)
            self.wait(0.5)
            self.remove(top_rects, low_rect)
        subsets.set_opacity(0.25)
        self.wait()

#######################################################################

class Trailer(Scene):
    def construct(self):
        title = Text("母函数", font = "simhei", color = YELLOW).scale(3)
        title[0].move_to(5*LEFT + 2*UP)
        title[1].move_to(5*LEFT)
        title[2].move_to(5*LEFT + 2*DOWN)
        function = MTex(r"{1}x^0+{1}x^1+{2}x^2+{3}x^3+{5}x^4+{8}x^5+{13}x^6+\cdots", tex_to_color_map = {(r"{1}", r"{2}", r"{3}", r"{5}", r"{8}", r"{13}"): BLUE, r"x": RED}).set_stroke(width = 8, color = BLACK, background = True).shift(1*RIGHT).rotate(-PI/6)
        frac = MTex(r"\frac{1}{1-x-x^2}", tex_to_color_map = {r"x": RED}).scale(2).shift(1.8*DOWN + 1*LEFT)
        # Fibonacci = Text("斐波那契数列", font = "simhei").scale(1.5).shift(2*UP + 3*RIGHT)
        Fibonacci = MTex(r"f_{n+1} = f_{n}+f_{n-1}", tex_to_color_map = {(r"f_{n+1}", r"f_{n}", r"f_{n-1}"): BLUE}).scale(1.5).shift(2*UP + 3*RIGHT)
        equal = MTex(r"\Leftrightarrow").scale(6).shift(1*RIGHT).rotate(PI/3)
        self.add(title, equal, function, frac, Fibonacci)

#######################################################################

BACK = "#333333"

class Test1(Scene):
    def construct(self):
        rectangle = Rectangle(height = 1, width = 4/3, fill_opacity = 1, stroke_width = 0)
        rectangles = []
        alpha = ValueTracker(0.0)
        def rect_updater(start_angle: float):
            def util(mob: VMobject):
                value = alpha.get_value()
                mob.restore().shift(np.sin((value + start_angle)*PI)*0.02*UP)
            return util
        for _ in range(100):
            rect_i = rectangle.copy().shift(np.array([(2*random.random()-1)*5, (2*random.random()-1)*3, 0])).scale(random.random()**2+0.25).set_opacity(0.5+0.5*random.random()).set_color(interpolate_color(BLUE_A, BLUE_E, random.random()))
            rect_i.save_state().add_updater(rect_updater(2*random.random()))
            rectangles.append(rect_i)
        def alpha_updater(mob: ValueTracker, dt):
            value = mob.get_value()
            mob.set_value(value + dt)
        alpha.add_updater(alpha_updater)
        self.add(alpha, *rectangles)
        self.wait(10)

#######################################################################