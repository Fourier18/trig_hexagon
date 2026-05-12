from manim import *
import numpy as np

class TrigHexagon(Scene):
    def construct(self):
        self.camera.background_color = "#ffffff"
        self.camera.frame_width = 10
        self.camera.frame_height = 10

        hex_color     = "#cc0000"
        diag_color    = "#cc0000"
        label_color   = "#8b0000"
        sphere_color  = "#ffb3b3"
        glow_color    = "#ffb3b3"
        hex_stroke    = 5.5
        diag_stroke   = 4
        hex_opacity   = 0.30
        glow_radius   = 0.40   # in Manim units (16/40 scaled)
        font_size     = 39

        # flat-top hex: vertices at angles 0,60,120,180,240,300 degrees
        # screen y is flipped in Manim vs canvas, so:
        # i=0: 0°   right      → cot
        # i=1: 60°  upper-right → cos   (Manim y-up, so 60° is upper-right)
        # i=2: 120° upper-left  → sin
        # i=3: 180° left        → tan
        # i=4: 240° lower-left  → sec
        # i=5: 300° lower-right → csc
        R = 2.8  # hex radius in Manim units
        label_R = R * 1.32

        angles_deg = [0, 60, 120, 180, 240, 300]
        labels_at  = ['cot', 'cos', 'sin', 'tan', 'sec', 'csc']

        vertices = [
            np.array([R * np.cos(np.radians(a)), R * np.sin(np.radians(a)), 0])
            for a in angles_deg
        ]

        # --- Hexagon outline ---
        hex_poly = Polygon(*vertices,
            stroke_color=hex_color,
            stroke_width=hex_stroke,
            fill_color=hex_color,
            fill_opacity=hex_opacity
        )

        # --- Internal lines (3 long diagonals + 6 spokes to center) ---
        internals = VGroup()
        diagonal_pairs = [(0,3),(1,4),(2,5)]
        for a, b in diagonal_pairs:
            internals.add(Line(vertices[a], vertices[b],
                stroke_color=diag_color, stroke_width=diag_stroke))
        for v in vertices:
            internals.add(Line(ORIGIN, v,
                stroke_color=diag_color, stroke_width=diag_stroke))

        # --- Sphere / glow at center ---
        sphere = Circle(
            radius=glow_radius,
            fill_color=sphere_color,
            fill_opacity=1,
            stroke_color="#000000",
            stroke_width=1.5
        )

        # --- Center "1" drawn as geometry ---
        one_height = 0.28
        one_width  = 0.035
        stem = Line(
            np.array([0, -one_height/2, 0]),
            np.array([0,  one_height/2, 0]),
            stroke_color=BLACK,
            stroke_width=one_width * 40
        )
        serif = Line(
            np.array([-0.06,  one_height/2 - 0.07, 0]),
            np.array([0,      one_height/2,         0]),
            stroke_color=BLACK,
            stroke_width=one_width * 35
        )
        one = VGroup(stem, serif)

        # --- Labels ---
        label_group = VGroup()
        for i, (angle_deg, name) in enumerate(zip(angles_deg, labels_at)):
            angle_rad = np.radians(angle_deg)
            pos = np.array([
                label_R * np.cos(angle_rad),
                label_R * np.sin(angle_rad),
                0
            ])
            lbl = MathTex(r"\it{" + name + r"}",
                font_size=font_size,
                color=label_color
            )
            lbl.move_to(pos)
            label_group.add(lbl)

        # --- Copyright notice ---
        copyright = Text(
            "© 2026 Folio Artlabs",
            font_size=11,
            color="#aaaaaa"
        )
        copyright.to_corner(DR, buff=0.15)

        # --- Assemble ---
        self.add(hex_poly, internals, sphere, one, label_group, copyright)
