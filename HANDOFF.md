# Handoff — The Magick Trig Hexagon

**Working file:** `index.html` at repo root — single source of truth, full HTML5 doc, hosted via GitHub Pages
**Live URL:** https://fourier18.github.io/trig_hexagon/
**Historical references:** `legacy/TRIGHEX_001.html` (pre-refactor), `oldindex_001.html` (v0 layout)
**Reference page:** https://www.mathsisfun.com/algebra/trig-magic-hexagon.html
**Mockups (identity overlays):** `media/images/refs/`

---

## What this is

Self-contained HTML widget that renders the trig magic hexagon to a 600×600 canvas and overlays identity relationships on demand. Print-quality PNG export (5400×5400 @ 300 dpi) for an 18″ poster.

---

## Current layout (top to bottom)

- **Title block** — "The Magick Trig Hexagon" (serif italic, dark red `#8b0000`) + ⬡ ornament between thin rules + "Identities at a Glance" small-caps subtitle. Centered.
- **Hexagon canvas** — flat-top orientation. Vertex indices (`i * 60°` clockwise in canvas coords):
  - `0 = cot` (R), `1 = csc` (BR), `2 = sec` (BL), `3 = tan` (L), `4 = sin` (TL), `5 = cos` (TR), center = "1"
  - Co-functions occupy the right column; non-co-functions the left. Cofunction pairs mirror across the vertical axis.
- **Floating ƒ button** — bottom-center of canvas, ~8% from bottom edge. Icon is the inlined SVG from `media/hex-gear-icon.svg` (uses `currentColor`).
- **Draggable popup panel** — opens above the button, finger-bumper drag handle at top, shadow deepens while dragging, position resets to default on close/reopen.

---

## ƒ panel — two views

**View 1 · Identity overlay** (default). Single-select list:

1. None
2. Product · diagonal — *sin · csc = 1*
3. Product · rim — *sin = cos · tan*
4. Quotient — *tan = sin/cos = 1/cot = sec/csc*
5. **Reciprocal** — *sin = 1 / csc* (subspecies of Quotient: simplifies the center path)
6. Cofunction — *sin = cos(90° − x)*
7. Pythagorean · additive — *sin² + cos² = 1²*
8. Pythagorean · subtractive — *sin² = 1² − cos²*

Below a divider: **Appearance** entry that swaps the panel to View 2.

**View 2 · Appearance** (settings).
Accordion: Colors / Stroke / Opacity / Typography / Sphere / Show. Back link `← Identities` at top returns to View 1. The `ID highlight` color picker drives the overlay arrow/oval color — default is red `#cc0000`, matching the mockup style.

---

## Bottom actions (inside Appearance)

1. **Download PNG · 5400×5400 · 300 dpi** — primary button, brand purple.
2. **Save current as default** — writes to `localStorage.trighex_config_v1`, verifies by read-back.
3. **↓ / ↑** — manual export/import of `trighex-config.json`. Reliable fallback when `file://` localStorage is unavailable.

---

## Identity overlays — current state (settled, session 4)

All seven overlays now match the user-supplied mockups in `media/images/refs/` (plus the mathsisfun screenshot for cofunction). Design language is unified across all overlays.

### Design language

- **`drawArrow(points[], opts)`** — straight (2 points) or multi-segment elbow (3+ points). Arrowhead at end by default. Opts: `color`, `lineWidth`, `arrowSize`, `headStart`, `doubleHeaded`.
- **`drawHighlightOval(target, opts)`** — red oval around a label (vertex index `0..5`) or `'center'` for the "1". Auto-sizes to label width; grows for `²` superscript in Pyth mode.
- **Arrows do not bisect labels** — start/end offsets keep arrows from cutting through label text. Standard offsets: ~28–34 px from label center toward target.
- **Floating equation in trig-label style** — italic serif, `c-label` color, no background pill, sized to match labels (or scaled down for multi-line). Most overlays place it at upper-left at `(cx + labelR×1.45 × cos 240°, cy + labelR×1.45 × sin 240°)` ≈ upper-left corner of canvas.
- **Operator markers** for Pythagorean wedges (`+`, `−`) rendered at the wedge centroid in trig-label style (no pill background).

### Per-overlay treatment

| ID | Function | Visual |
|---|---|---|
| `prod-diag` | `drawProdDiag` | Center "1" circled. Two arrows from outside sin and csc into center oval edge. `sin · csc = 1` at upper-left. |
| `prod-rim` | `drawProdRim` | sin circled. Dashed quadratic Bezier *associator* from tan to cos arcing **outside** the hex (says "these two multiplied"). Solid arrows from cos and tan into sin oval. `sin = cos · tan` at upper-left. |
| `quot` | `drawQuot` | tan circled. **6 arrows in 3 two-arrow paths:** top rim (tan→sin→cos), center via "1" (tan→1→cot — terminates at glow radius), bottom rim (tan→sec→csc). Multi-line equation upper-left:<br>`tan = sin / cos`<br>` = 1 / cot`<br>` = sec / csc` |
| `recip` | `drawReciprocal` | sin circled. Two-arrow flow: sin→1 (numerator) then 1→csc (denominator). `sin = 1 / csc` at upper-left. |
| `cofn` | `drawCofn` | Three horizontal pair arrows: sin→cos, tan→cot, sec→csc. Multi-line equation block upper-left:<br>`sin(x) = cos(90° − x)`<br>`tan(x) = cot(90° − x)`<br>`sec(x) = csc(90° − x)` |
| `pyth-add` | `drawPythAdd` | All labels squared (`sin²`, `cos²`, …, center `1²`). 1² circled. **L-shape arrow:** horizontal bar between sin² and cos² labels (just below them), bend just before cos² label, diagonal **through the top wedge interior**, terminating at top center of 1² oval. Stylized `+` at wedge centroid. `sin² + cos² = 1²` upper-left. |
| `pyth-sub` | `drawPythSub` | All labels squared. sin² circled. **Mirror of additive arrow geometry, reversed direction**: starts at top of 1² oval, up through top wedge, bend before cos² label, horizontal left to sin² oval (arrowhead here). Stylized `−` at wedge centroid. `sin² = 1² − cos²` upper-left. |

### Dropped (code removed, not in menu)

- **Half-angle** (`half`) — doesn't live on the hex geometrically.
- **Quadrants positive / ASTC** (`quad`) — same.
- `applyConfig` migrates legacy saved IDs: `pyth` → `pyth-add`, `half` / `quad` → `none`.

---

## Render architecture

- `draw()` is the single source of truth. Reads inputs via `getVal()`/`getChecked()` and renders to `ctx`.
- `ctx` is `let` (not `const`) so PNG export can temporarily swap it to an off-screen 5400×5400 context and call `draw()` unchanged. `targetCtx.scale(S/600)` makes everything scale proportionally — strokes, fonts, glow radii, arrow widths, oval rings.
- `draw()` builds `fv = flatVerts(hexR)` (hex vertex positions) and `lv = flatVerts(labelR)` (label positions) once, then passes both to `drawIdentity(id, fv, lv, hi)`.
- `isPyth = currentId === 'pyth-add' || currentId === 'pyth-sub'`. When true:
  - Labels render via `drawSquaredLabel(text, x, y, fs, color)` instead of plain `ctx.fillText` — gives `sin`, `cos`, etc. a small `²` superscript.
  - `drawOne(color, size, true)` adds a `²` next to the center "1".
- Identity dispatch: `drawIdentity(id, fv, lv, hi)` switches on `currentId` and calls one of the seven `draw*` functions.

### Primitives / helpers (above the overlay functions in the script)

- `labelPos(i)` / `radialPt(i, r)` — position helpers
- `offsetToward(from, to, dist)` — point `dist` units along the segment from→to
- `drawArrowhead(from, to, size, color)` — solid triangle head
- `drawArrow(points[], opts)` — main arrow primitive (straight / elbow / multi-segment)
- `drawHighlightOval(target, opts)` — red oval around a label or center
- `drawSquaredLabel(text, x, y, fs, color)` — italic serif text with small `²` to the right

### Still-used legacy helpers

- `flatVerts(r)`, `hexToRgba()`
- (Cleaned up session 5: `bgLabel`, `lerp`, `drawGlow` removed as dead code.)

### Key constants

- `cx = cy = 300`, `hexR = W*0.24` (144), `labelR = hexR*1.3` (187)
- (Cleaned up session 5: `outerR` removed.)

---

## Persistence model

- **localStorage** — primary, automatic. Stores: all 9 colors, all 8 ranges, all 6 toggles, `currentId`. Verified on write.
- **JSON file (↓/↑)** — secondary, manual. Same shape. Importing also writes to localStorage and redraws.
- file:// localStorage works in modern Chrome/Edge/Firefox but is fragile. Manual JSON is the reliable fallback.
- `applyConfig` includes the legacy-ID migration (see Identity overlays section).

---

## Session changelog

### Session 9 — Rename, license, marketing plan

1. Renamed the project everywhere: "The Magick Hexagon" → "The Magick Trig Hexagon" (adds "Trig" for SEO). Subtitle changed from "trig identities at a glance" to "Identities at a Glance" (drops the now-redundant "trig"). Updated `index.html` (`<title>`, `<h1>`, subtitle, meta description) and this file's living-state sections. Session 2's changelog entry below intentionally still reads the old name — that's an accurate historical record, not a bug.
2. Added Open Graph + Twitter Card meta tags to `index.html` (`og:title`, `og:description`, `og:image`, `twitter:card`, etc.) pointing at `media/images/trig-hexagon.png` so links shared on social platforms get a real preview card instead of a blank one. That image is from an old blue/purple palette — swap in a fresh screenshot in the current red/pink branding before real launch.
3. **Added a license.** Was "all rights reserved" with no formal terms — incompatible with "free distribution to students and teachers." Added `LICENSE` (CC BY-NC 4.0: free to use/share/print/remix with attribution, non-commercial) and a matching README badge + License section.
4. Wrote `MARKETING.md` — the campaign plan for free distribution to students/teachers plus a social media presence across Twitter/X, Pinterest, Reddit, Instagram, TikTok, Facebook, and BlueSky. See that file for channel strategy, asset checklist, and rollout steps. **Deliberately gitignored, local-only** — no practical reason for a growth/strategy doc to be world-readable in a public code repo. It still exists in the project folder; it just won't show up if you clone from GitHub.

### Session 8 — Bug-fix / QA pass (subagent-driven)

1. Ran two review subagents in parallel: one code-correctness audit of `index.html`, one docs-accuracy audit of README/HANDOFF against the actual code. Findings below were confirmed real, not false positives, before fixing.
2. **Critical fixes:** `exportPNG()`'s offscreen-canvas `ctx` swap only restored `ctx` on the happy path — if `draw()` threw mid-export, `ctx` stayed pointed at the detached canvas for the rest of the session, silently breaking all future renders. Wrapped in `try/finally`. Also wrapped the async `toBlob` callback in its own `try/catch` — an unhandled throw there left the Download button stuck on "Generating…" forever.
3. **iPadOS detection gap:** UA sniffing (`/iPad|iPhone|iPod/`) misses modern iPadOS Safari, which reports a desktop-Mac UA by default. Added the standard `navigator.platform==='MacIntel' && navigator.maxTouchPoints>1` fallback so iPads correctly get the 3000×3000 export cap instead of hitting the same canvas-limit bug iPhone was patched for.
4. **Halo gap:** `drawProdRim`'s dashed "associator" curve was the one overlay element drawing raw `ctx.stroke()` instead of going through `drawArrow`/`drawHighlightOval` — the one path that could become invisible if the highlight color matched the fill/background. Gave it the same halo-pass treatment.
5. Removed dead code (`radialPt`, never called) and fixed two CSS custom-property fallbacks that still referenced the old purple default.
6. **Doc fixes:** HANDOFF had two self-contradicting mentions of the ID-highlight default (said purple, actually red, HANDOFF's own changelog already said red). Fixed. Also fixed a stale "Glow-or-sphere" accordion name (renamed to "Sphere" back in Session 5) and added the iOS export cap + a missing legacy file to README.
7. **Opacity defaults were still washed out.** `hex-opacity` (30%) and `diag-opacity` (15%) were leftover from the old translucent-wash design, never bumped when the color model moved to solid scarlet fill — raised both to 100%.
8. **Real draw-order bug**, caught by the user after the opacity fix: the hex body's full-area fill was drawn *after* the internal divider lines, so at 100% fill opacity it painted directly over them and hid them completely, regardless of `int-opacity`. Reordered the pipeline — fills first (body, then wedges), divider lines on top of the fill, outline stroke last for a crisp border.
9. `onSave()` now auto-downloads the config JSON when `localStorage` is blocked (sandboxed iframes, private browsing) instead of just telling the user to click ↓ themselves.

### Session 7 — Appearance polish

1. **Drag handle truly sticky.** Previously `top: -10px` placed the handle 10px above the panel viewport when stuck, so it scrolled away. Now `top: 0`, panel restructured with `padding: 0 10px 10px` so the handle owns the top of the scroll area. Handle bar made more prominent (64×6 with 6px radius, opacity hover effect) and tinted via `--fbtn-color`.
2. **New `c-fbtn` color picker** in the Appearance Colors accordion. Drives a CSS custom property `--fbtn-color` that themes the ƒ button (icon inactive / bg active) and the drag-handle bar. Wired via `applyFbtnColor()` called on init and on picker `input`.
3. **New `int-opacity` slider** (Opacity accordion → "Internal", default 100%). Controls the alpha of the internal divider lines independently of hex fill and triangle fill, so dropping hex opacity no longer fades the dividers.
4. **Halo around overlay arrows and highlight ovals.** Added `contrastColor(hex)` helper (returns `#000` for light arrows, `#fff` for dark, based on relative luminance). `drawArrow` and `drawHighlightOval` now make a halo pass at `lw + 2.5` before the main stroke, guaranteeing overlays stay visible against any background, fill, or label color the user picks.
5. **New defaults:** background and sphere fill are now just-off-white pink (`#fff5f5`); center "1" matches label color (`#cc0000`); center-size reduced from 18 → 14 so the "1" doesn't crowd the sphere edge.

### Session 6 — Consolidation + color model fix

1. Killed the dual-file pattern. `Artifact versions/TRIGHEX_002.html` deleted; `index.html` at root is now the single source of truth. `TRIGHEX_001.html` moved to `legacy/`. No more "edit both files" overhead.
2. **Color model fix:** previously the `Hexagon` color picker controlled both stroke and fill, AND wedge triangles used hardcoded alternating reds (`#e08080`/`#c06060`) plus a buggy `* 1.5` opacity multiplier — meaning no UI setting could fully clear the "haze" on the interior. Now: hex outline (`c-hex`) and hex fill (`c-hex-fill`) are separate pickers; wedge triangles share `c-hex-fill` so a single setting controls all interior fill uniformly; the `* 1.5` is removed so the opacity slider is true 0–100%.
3. New defaults: rose pink bg (`#ffd6dd`), black hex outline + internals + center + sphere edge, scarlet hex fill + labels + ID highlight (`#cc0000`), rose pink sphere fill matching bg.

### Session 5 — Cleanup pass

1. Removed dead code: `bgLabel`, `lerp`, `drawGlow` functions; `outerR` constant.
2. Collapsed sphere/glow rendering to sphere-only (`drawSphere` is the sole center decoration).
3. Appearance UI: removed `Glow` color, `Intensity` slider, `Sphere mode` toggle. `Glow / sphere` accordion → `Sphere`; `Show: Glow` toggle → `Show: Sphere`.
4. Internal IDs `show-glow` and `glow-radius` kept so old saved configs continue loading cleanly; only UI labels changed.

### Session 4 — Identity overlay redesign (all 7 settled)

1. Walked through each overlay one-by-one with the user; rebuilt against the mockups in `media/images/refs/`.
2. Reciprocal: two-arrow flow (sin→1, 1→csc), removed pasted-on red text, added trig-label-style floating equation.
3. Product · diagonal: arrows no longer bisect labels (start just past each label), added side equation.
4. Product · rim: added dashed Bezier associator (tan↔cos arcing outside hex) saying "these two multiplied"; bumped arrow offsets; fixed dropdown caption (`cos = sin · cot` → `sin = cos · tan`).
5. Quotient: split center path into two arrows (tan→1, 1→cot) to match Reciprocal flow scheme; added multi-line equation block with three quotient forms; **menu reorder**: Reciprocal moved from position 1 → 5 (after Quotient) since it's the subspecies.
6. Cofunction: dropped right-side pill cards (were clipping), replaced with multi-line equation block in upper-left, kept three pair arrows.
7. Pythagorean · additive: rebuilt geometry to L-shape with diagonal entering the top wedge interior and terminating at top center of 1² oval; replaced pill `(+)` with clean italic `+` at wedge centroid.
8. Pythagorean · subtractive: mirror of additive geometry, reversed direction (arrowhead lands at sin²); clean italic `−` at wedge centroid.

### Session 3 — First pass + GitHub publication

1. Built first-pass overlay code (later fully redesigned in session 4).
2. Initialized git in the project; created README, HANDOFF, `.gitignore`; restructured root with `legacy/` for old Manim scripts; wrapped TRIGHEX_002 as a published `index.html` with full HTML5 doc.
3. Committed and pushed to https://github.com/Fourier18/trig_hexagon. GitHub Pages enabled, live at https://fourier18.github.io/trig_hexagon/.

### Session 2 — Pivot from sidebar to floating panel

1. Floated all controls behind a single bottom-centered ƒ button → hexagon gets full canvas width.
2. Replaced the ƒ text glyph with the inlined `media/hex-gear-icon.svg`.
3. Identity overlay dropdown + "Appearance" entry that swaps the panel.
4. Panel made draggable via finger-bumper at top; floating drop shadow.
5. Replaced Manim code export with print-quality PNG export (5400² @ 300 dpi).
6. Primary button styling for Download; localStorage save with verification; manual ↓/↑ JSON import/export.
7. Title block: "The Magick Hexagon" + ⬡ + "trig identities at a glance".

---

## Roadmap — next session focus

### 1. Cleanup / inspection
- `Show: Triangles` and `Show: Diagonals` are NOT redundant — triangles control the cell fills, diagonals control the dividing line work. Both kept.
- (Other cleanup items resolved in sessions 5 and 6; see changelog.)

### 2. Testing
- **Cross-browser:** verify PNG export, drag, and localStorage persistence on Firefox and Safari (currently developed on Edge/Chrome).
- **Per-overlay PNG export:** render each overlay at 5400×5400 and confirm arrows/text scale cleanly (the canvas ctx-swap should handle this but worth verifying).
- **Mobile/tablet:** check whether the draggable panel works on touch (uses pointer events — should be OK in modern mobile browsers).
- **Verify legacy-ID migration** — if a user with an old saved config (e.g., `currentId: 'pyth'`) loads the new version, does it cleanly migrate to `pyth-add`?

### 3. App speculations (future)
- **Electron wrapper** is the lowest-effort path to a desktop app (Mac/Windows/Linux). Persistence would need to switch from `localStorage` to filesystem (e.g., per-platform AppData / Application Support).
- **Mobile (Android/iOS):** Capacitor or PWA wrapping around the existing HTML. PWA route is interesting because it works with no app store and respects the existing localStorage model.
- **Single-file constraint:** keep the widget as one HTML file as long as it's the published artifact — splitting into multiple files breaks the "open it in a browser, done" workflow.

### 4. Future identities (deferred)
- **Half-angle**, **Derivatives**, **Quadrants positive (ASTC)** — these don't live on the hex geometrically. Could be sibling widgets (separate canvases) or modal overlays that don't try to map onto the hex.

### 5. Marketing rollout (active — see MARKETING.md)
- License and social meta tags are in place; the plan is written. What's NOT done and requires the user directly (Claude can't create accounts): actually creating the social media accounts on each chosen platform, and swapping the OG/Twitter-card preview image for a fresh screenshot in the current red/pink branding (current one is the old blue/purple palette).
- Full channel strategy, asset checklist, and rollout steps live in `MARKETING.md`, not duplicated here.

---

## Misc notes

- `trig_hexagon.py` through `trig_hexagon_005.py` in `legacy/` are Manim scripts from the earlier phase. No longer the output target. Useful only as a vertex-arrangement / styling reference if needed.
- `legacy/test.py` — unknown purpose, kept for reference.
- `media/Tex/`, `media/texts/`, `media/videos/`, `media/images/trig_hexagon*/` are Manim build artifacts, gitignored.
- The `ID highlight` color picker in Appearance drives the overlay color. Default is red (`#cc0000`), matching the mockup style.
