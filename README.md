# The Magick Trig Hexagon

The six trig functions, along with key identity families including reciprocal, product, quotient, cofunction, and Pythagorean, encoded in the geometry of a single hexagon. Toggle identity overlays, customize the appearance, export a print-quality poster.

### [Try the interactive hexagon →](https://fourier18.github.io/trig_hexagon/)

Free, no install, no login. Runs in any browser.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

## What the hexagon encodes

The Magic Trig Hexagon arranges the six trig functions (`sin`, `cos`, `tan`, `cot`, `sec`, `csc`) at the vertices of a regular flat-top hexagon, with **`1`** at the center. The geometry isn't decorative; every trig identity falls out of the structure:

- **Reciprocal pairs** sit at opposite vertices (sin↔csc, cos↔sec, tan↔cot)
- **Diagonal products** through the center equal `1` (sin · csc = 1)
- **Rim products** make each vertex the product of its two neighbors (sin = cos · tan)
- **Quotients** give each vertex as a ratio of its neighbors along three independent paths (tan = sin/cos = 1/cot = sec/csc)
- **Pythagorean wedges** in the three central triangles encode sin² + cos² = 1, 1 + tan² = sec², 1 + cot² = csc²
- **Cofunction pairs** mirror across the vertical axis (sin↔cos, tan↔cot, sec↔csc)

The widget surfaces each identity family as a togglable overlay so the structural meaning is visible without losing the underlying diagram.

Reference page: [Magic Hexagon for Trig Identities (Math is Fun)](https://www.mathsisfun.com/algebra/trig-magic-hexagon.html)

---

## Features

- **Identity overlays**: single-select dropdown with seven families:
  - Product · diagonal: `sin · csc = 1`
  - Product · rim: `sin = cos · tan`
  - Quotient: `tan = sin/cos = 1/cot = sec/csc`
  - Reciprocal: `sin = 1 / csc`
  - Cofunction: `sin = cos(90° − x)`
  - Pythagorean · additive: `sin² + cos² = 1²`
  - Pythagorean · subtractive: `sin² = 1² − cos²`
  - Overlays render on top of whatever hex configuration is active; Pythagorean modes also re-render all trig labels with `²` superscripts
- **Floating ƒ panel**: a single bottom-centered button opens a draggable popup with two views (Identity overlay / Appearance), keeping the full canvas width for the hexagon
- **Appearance customization**: 10 colors (background, hex outline, hex fill, internals, labels, center, sphere fill, sphere edge, ID highlight, ƒ button), strokes, opacities (hex fill, tri fill, internal lines), font sizes, sphere radius, five visibility toggles (labels, diagonals, center 1, triangles, sphere). Overlay arrows and ovals are drawn with a contrasting halo so they stay readable against any background or fill.
- **Print-quality PNG export**: exports a 5400×5400 px PNG at 300 dpi (sized for an 18″ poster), scaled losslessly from the 600×600 canvas. On iOS Safari/Edge the export is capped at 3000×3000 and shows a modal preview for saving via the share sheet.
- **Persistence**: settings save automatically to `localStorage` with read-back verification; manual JSON export/import (`↓` / `↑`) as a fallback for `file://` contexts

---

## Run it locally

```bash
git clone https://github.com/Fourier18/trig_hexagon.git
cd trig_hexagon
# Open index.html in any modern browser, or serve it:
python -m http.server  # then visit http://localhost:8000
```

No build step. Single self-contained HTML file.

---

## Project layout

```
trig_hexagon/
├── index.html                 # The widget, single-file, self-contained
├── oldindex_001.html          # Historical v0 layout (preserved)
├── README.md                  # This file
├── HANDOFF.md                 # State-of-the-widget for picking up cold
├── media/
│   ├── hex-gear-icon.svg      # ƒ-button glyph
│   └── images/
│       ├── refs/               # Mockups for the identity overlays
│       ├── trig-hexagon.png    # Preview/social image
│       └── blank hex - *.png   # Blank hex reference renders
└── legacy/
    ├── TRIGHEX_001.html       # Pre-refactor reference (sidebar layout)
    ├── trig_hexagon_005_html_001.html  # Interim html snapshot
    ├── test.py                # Early scratch
    └── trig_hexagon_00*.py    # 5 historical Manim scripts (project was
                               # Manim-targeted before the print-PNG pivot)
```

`HANDOFF.md` is the canonical state document; read it first if you're picking up where the last session left off.

---

## Status

Functional end-to-end: render, customize, save, export. Seven identity overlays implemented against the mockups in `media/images/refs/` using a unified design language: red arrows, circled "this equals" label, floating equation in trig-label style.

## Roadmap

1. **Testing**: cross-browser (Firefox / Safari), per-overlay PNG export verification, mobile touch panel behavior.
2. **Native-app packaging** (future): Mac / Windows / Android via Electron, Capacitor, or PWA.

---

## Contributors

- **[Fourier18](https://github.com/Fourier18)**: owner, design, mathematics
- **Claude (Anthropic)**: code

---

## License

**CC BY-NC 4.0**: free to use, share, remix, and print (including for classroom handouts and posters) with attribution, non-commercial. See [LICENSE](LICENSE) for details.
