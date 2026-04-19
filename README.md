# trig_hexagon

Print-quality visualizations of the Magic Trig Hexagon — built with Manim.

![Python 3.12](https://img.shields.io/badge/Python-3.12-blue) ![Manim CE](https://img.shields.io/badge/Manim_CE-v0.20-red)

This repository renders the **Magic Trig Hexagon** — a mnemonic diagram encoding six fundamental trig identities as geometric relationships between vertices of a regular hexagon.

## What the hexagon encodes

Vertices are labeled `sin`, `cos`, `tan`, `cot`, `sec`, `csc` at fixed positions on a flat-top hexagon. The geometry is structural, not decorative:

- Any three consecutive vertices satisfy a **product identity** (e.g. sin · csc = 1)
- Opposite vertices are **reciprocal pairs**
- The central **1** anchors all six relationships
- The three long diagonals connect each function to its reciprocal through unity

## Implementation

All geometry is computed from first principles using vertex angles — no GUI, no dragging handles. Coordinates are derived mathematically and passed directly to Manim primitives. Labels render via `MathTex` with LaTeX.

## Outputs

- 4096×4096 PNG exports for print
- Color variants and labeled/unlabeled versions in progress

## Usage

```bash
# Preview
manim -pql --resolution 480,480 trig_hexagon.py TrigHexagon

# Print
manim -pqh --resolution 4096,4096 trig_hexagon.py TrigHexagon
```
