# Handoff — The Magick Hexagon

**Working file:** `Artifact versions/TRIGHEX_002.html`
**Older version preserved:** `Artifact versions/TRIGHEX_001.html` (pre-refactor reference)
**Reference page:** https://www.mathsisfun.com/algebra/trig-magic-hexagon.html
**Mockups (identity overlays):** `media/images/refs/`

---

## What this is

Self-contained HTML widget that renders the trig magic hexagon to a 600×600 canvas and overlays identity relationships on demand. Print-quality PNG export (5400×5400 @ 300 dpi) for an 18″ poster.

---

## Current layout (top to bottom)

- **Title block** — "The Magick Hexagon" (serif italic, dark red `#8b0000`) + ⬡ ornament between thin rules + "trig identities at a glance" small-caps subtitle. Centered.
- **Hexagon canvas** — flat-top orientation. Vertex indices (`i * 60°` clockwise in canvas coords):
  - `0 = cot` (R), `1 = csc` (BR), `2 = sec` (BL), `3 = tan` (L), `4 = sin` (TL), `5 = cos` (TR), center = "1"
  - Co-functions occupy the right column; non-co-functions the left. Cofunction pairs mirror across vertical axis.
- **Floating ƒ button** — bottom-center of canvas, ~8% from bottom edge. Icon is the inlined SVG from `media/hex-gear-icon.svg` (uses `currentColor`).
- **Draggable popup panel** — opens above the button, finger-bumper drag handle at top, shadow deepens while dragging, position resets to default on close/reopen.

---

## ƒ panel — two views

**View 1 · Identity overlay** (default)
Single-select list. Current entries:
None / Reciprocal / Product · diagonal / Product · rim / Quotient / Cofunction / Pythagorean · additive / Pythagorean · subtractive.

The last item, **Appearance**, is separated by a divider and swaps the panel to View 2.

**View 2 · Appearance** (settings)
Accordion: Colors / Stroke / Opacity / Typography / Glow-or-sphere / Show toggles. Back link `← Identities` at top returns to View 1. The `ID highlight` color picker drives the overlay arrow/oval color.

---

## Bottom actions (inside Appearance)

1. **Download PNG · 5400×5400 · 300 dpi** — primary button, brand purple (`#534AB7`).
2. **Save current as default** — writes to `localStorage.trighex_config_v1`, verifies by read-back.
3. **↓ / ↑** — manual export/import of `trighex-config.json`. Bulletproof fallback when file:// localStorage is unavailable.

---

## Identity overlays — current code state

**Status: first-pass implementation landed in session 3. User reviewed and reports extensive mistakes requiring redesign, not just placement tuning. Includes (but not limited to) wrong arrow directions. Specific list of issues per-overlay has not yet been enumerated — next session must walk through each overlay with the user against the mockups.**

The current code is built around two primitives:

- `drawArrow(points[], opts)` — straight (2 points) or multi-segment elbow (3+ points). Arrowhead at end by default; `doubleHeaded` and `headStart` opts available.
- `drawHighlightOval(target, opts)` — red oval around a label. `target` is a vertex index `0..5` or the string `'center'`. Auto-sizes to the label; grows when Pythagorean mode adds a `²` superscript.

Seven overlay functions live in the script, each taking `(fv, lv, hi)` where `fv` is vertex positions, `lv` is label positions, `hi` is the overlay color from `c-hi`:

| ID | Function | What it currently draws |
|---|---|---|
| `recip` | `drawReciprocal` | Circles sin; diagonal arrow from csc; `= 1 / csc` label outside the oval |
| `prod-diag` | `drawProdDiag` | Circles center "1"; arrows along sin↔csc diagonal, terminating at oval edge |
| `prod-rim` | `drawProdRim` | Circles sin; arrows from cos and tan into sin oval |
| `quot` | `drawQuot` | Circles tan; five arrows — top rim sin→cos, connector tan→sin, center path tan→cot through "1", bottom rim sec→csc, connector tan→sec |
| `cofn` | `drawCofn` | Three horizontal pair arrows (sin↔cos, tan↔cot, sec↔csc) + three equation cards at right edge |
| `pyth-add` | `drawPythAdd` | All labels get `²`, center "1" → "1²"; elbow arrow (above-sin² → above-cos² → center 1²); `(+)` marker in top wedge |
| `pyth-sub` | `drawPythSub` | All labels get `²`; circles sin²; V-path (cos² → near-center → sin²); `(−)` marker in top wedge |

All of the above are subject to redesign in the next session — do not treat them as correct.

### Mockup files (`media/images/refs/`)

| File | Currently mapped to |
|---|---|
| `product identity - center-unity.png` | `prod-diag` |
| `product identity - periphery.png` | `prod-rim` |
| `pythagorean identities - additive.png` | `pyth-add` |
| `pythagorean identities - subtractive.png` | `pyth-sub` |
| `quotient identity - periphery.png` | `quot` (without center path) |
| `quotient identity - periphery and center-unity.png` | `quot` (final form, 3 paths) |
| *mathsisfun cofunction screenshot (not in folder; from session 3 chat)* | `cofn` |
| *no mockup; verbal spec only* | `recip` |

### Menu changes this session

- Pythagorean split into two entries (`pyth-add`, `pyth-sub`).
- `half` (Half-angle) and `quad` (Quadrants positive) removed from the dropdown and from the code.
- `applyConfig` migrates legacy saved IDs: `pyth` → `pyth-add`; `half` / `quad` → `none`.

Whether the menu structure (which families exist, which are split, which are dropped) stays as-is depends on the upcoming redesign pass.

---

## Render architecture

- `draw()` is the single source of truth. Reads inputs via `getVal()`/`getChecked()` and renders to `ctx`.
- `ctx` is `let` (not `const`) so PNG export can temporarily swap it to an off-screen 5400×5400 context and call `draw()` unchanged. `targetCtx.scale(S/600)` makes everything scale proportionally — including strokes, fonts, glow radii, arrow widths, oval rings.
- `draw()` builds `fv = flatVerts(hexR)` (vertex positions) and `lv = flatVerts(labelR)` (label positions) once, then passes both to `drawIdentity(id, fv, lv, hi)`.
- `isPyth = currentId === 'pyth-add' || currentId === 'pyth-sub'`. When true:
  - Labels render via `drawSquaredLabel(text, x, y, fs, color)` instead of plain `ctx.fillText` — gives `sin`, `cos`, etc. a small `²` superscript.
  - `drawOne(color, size, true)` adds a `²` next to the center "1".
- Identity dispatch: `drawIdentity(id, fv, lv, hi)` switches on `currentId` and calls one of the seven `draw*` functions.
- **Primitives / helpers added this session** (above the overlay functions in the script):
  - `labelPos(i)` / `radialPt(i, r)` — quick position helpers
  - `offsetToward(from, to, dist)` — point `dist` units along the segment from→to
  - `drawArrowhead(from, to, size, color)` — solid triangle head
  - `drawArrow(points[], opts)` — main arrow primitive
  - `drawHighlightOval(target, opts)` — red oval around a label or the center
  - `drawSquaredLabel(text, x, y, fs, color)` — italic serif text with small `²` to the right
- Helpers still in use from before: `flatVerts(r)`, `bgLabel(text,x,y,size,color)` (translucent white pill behind text), `hexToRgba()`, `lerp()`.
- Key constants: `cx=cy=300`, `hexR=W*0.24` (144), `labelR=hexR*1.3` (187), `outerR=hexR*1.7` (245 — now mostly unused).

---

## Persistence model

- **localStorage** — primary, automatic. Stores: all 9 colors, all 8 ranges, all 6 toggles, `currentId`. Verified on write.
- **JSON file (↓/↑)** — secondary, manual. Same shape. Importing also writes to localStorage and redraws.
- file:// localStorage works in modern Chrome/Edge/Firefox but is fragile. Manual JSON is the reliable fallback.
- `applyConfig` includes the legacy-ID migration (see Identity overlays section).

---

## Session changelog

### Session 3 — identity visual rework (first pass; flagged for redesign)

1. Reviewed user mockups in `media/images/refs/` plus a mathsisfun cofunction screenshot.
2. Discussion-phase decisions (subject to revision in the redesign pass):
   - Reciprocal and Product · diagonal kept as separate menu items.
   - Quotient and Cofunction treated as exceptions to the "one example" rule (Quotient shows 3 paths; Cofunction shows 3 pairs).
   - Pythagorean split into additive and subtractive.
   - Half-angle and Quadrants positive removed from the menu.
3. Added two primitives: `drawArrow` and `drawHighlightOval`. Added `drawSquaredLabel` and a `withSquare` flag on `drawOne`.
4. Replaced the eight old placeholder `draw*` functions with seven new ones.
5. Wired Pythagorean squared-label mode into `draw()` (all six trig labels + center get `²`).
6. Updated dropdown HTML; added legacy-ID migration to `applyConfig`.
7. **User feedback at end of session:** the first-pass overlays have extensive mistakes — including wrong arrow directions — and need redesign, not just tuning. Specific defect list not yet captured.

### Session 2 — pivot from sidebar to floating panel

1. Floated all controls behind a single bottom-centered ƒ button → hexagon gets full canvas width.
2. Replaced the ƒ text glyph with the inlined `media/hex-gear-icon.svg`.
3. Identity overlay dropdown + "Appearance" entry that swaps the panel.
4. Panel made draggable via finger-bumper at top; floating drop shadow.
5. Replaced Manim code export with print-quality PNG export (5400² @ 300 dpi).
6. Primary button styling for Download; localStorage save with verification; manual ↓/↑ JSON import/export.
7. Title block: "The Magick Hexagon" + ⬡ + "trig identities at a glance".

---

## Roadmap

1. **Next session — primary:** identity overlay redesign. User has reported extensive mistakes in the current first-pass; specifics (beyond "wrong arrow directions") to be enumerated at the start of the next session. Walk each overlay with the user against its mockup before changing code.
2. **After identities settle:** push to GitHub.
3. **Future — possibly revisited:** Half-angle and Quadrants positive (currently removed from the menu) as separate widgets or back in the menu — decision deferred.
4. **Future — far:** packaging as an app (Mac / Android / PC) — at which point the persistence model would need rethinking (per-platform native storage).

---

## Misc notes

- `trig_hexagon.py` through `trig_hexagon_005.py` in project root are Manim scripts from the earlier phase. No longer the output target. Useful only as a vertex-arrangement / styling reference if needed.
- `test.py` — unknown purpose, not touched this session.
- `__pycache__/` — Python build artifacts, ignore.
- The `ID highlight` color picker in Appearance drives the overlay color. Default is purple (`#534AB7`); set to red (`#cc0000`) to roughly approximate the mockup style.
