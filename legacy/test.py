from manim import *

class UnitCircle(Scene):
    def construct(self):
        self.camera.background_color = "#1a1a2e"
        self.camera.frame_width = 8
        self.camera.frame_height = 8

        # Axes as manual lines, stopping at exactly ±2
        x_axis = Line(LEFT * 2, RIGHT * 2, color=BLUE_D, stroke_width=1.5)
        y_axis = Line(DOWN * 2, UP * 2, color=BLUE_D, stroke_width=1.5)

        # Tick marks at ±1 and ±2 on each axis
        ticks = VGroup()
        tick_size = 0.08
        for pos in [-2, -1, 1, 2]:
            ticks.add(Line(
                [pos, -tick_size, 0], [pos, tick_size, 0],
                color=BLUE_D, stroke_width=1.5
            ))
            ticks.add(Line(
                [-tick_size, pos, 0], [tick_size, pos, 0],
                color=BLUE_D, stroke_width=1.5
            ))

        circle = Circle(radius=1, color=WHITE, stroke_width=3)

        self.add(x_axis, y_axis, ticks, circle)