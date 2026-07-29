---
name: trig-hex-image-export
description: Generate real PNG image files (color/palette variations, identity-overlay states, marketing assets, poster exports) from this project's widget (index.html) and write them straight to disk. Use this whenever asked to produce, export, capture, download, or generate images, screenshots, variations, or renders of the trig hexagon — for Pinterest, social media, marketing, printing, or any other purpose — even if the request doesn't use the word "export" (e.g. "make some versions with different colors", "give me images of each identity", "I need pictures of the hexagon for X"). Do NOT use browser automation (sandboxed preview pane or a real-browser extension) for this — that path was tried and failed repeatedly. Always use the headless Puppeteer approach below.
---

# Trig Hex image export

## Why this exists

Generating real image files from this widget went through three failed
approaches before landing on the one that works — worth knowing so you don't
repeat them:

1. **A sandboxed preview-browser pane** — its downloads don't land anywhere
   on the local filesystem. No way to retrieve the output.
2. **Pulling canvas pixels via `toDataURL()` and manually retyping the
   base64 string into a file-write call** — silently truncates at that
   length (40,000+ characters) and produces a corrupted image that still
   *looks* superficially valid (right file extension, plausible-ish size)
   until you actually try to open it.
3. **Automating a real browser's UI** (clicking the real Download PNG
   button through a browser extension) — works in principle, but the
   button's own download hits native OS/browser-level "where do you want
   to save this" dialogs that page-content-only browser tools can't see or
   click, and each UI action needed a fresh permission click, burning a lot
   of time for zero output.

**What actually works:** the widget is a single self-contained HTML file
with no server dependency. Its `draw()` function and all the overlay
drawing functions are plain Canvas 2D calls — nothing browser-UI-specific.
Load the real `index.html` in headless Puppeteer, drive its real functions
directly (same code, same math, zero reinterpretation), and write PNG
bytes straight to disk from inside the same Node process. No browser UI,
no downloads folder, no permission prompts, no manual base64 handling.

## How to do it

1. Confirm Node is available (`node --version`) and `puppeteer` is
   installed in the project (`npm install puppeteer --no-save` if not —
   it's a prebuilt-Chromium download, no native compilation, installs in
   seconds).
2. Use `scripts/generate-variations.js` in this skill as the starting
   template — copy it into the project (e.g. into a working folder like
   `pinterest-variations/` or wherever the output should live) and edit
   the `PALETTES` array and `OUT_DIR` for the specific request. The
   script already discovers the current identity-overlay list dynamically
   from the live page, so it doesn't need updating if the widget's overlay
   menu changes later.
3. Run it with `node <script>`. It launches headless Chromium, loads the
   real `index.html`, and for each palette × identity-state combination:
   sets the real color `<input>` values and dispatches a real `input`
   event (exactly what the app's own `bind()` listens for — this is
   genuinely driving the real UI state, not a shortcut), sets the real
   `currentId` and calls the real `draw()`, then reads
   `canvas.toDataURL()` and writes the decoded bytes directly to disk via
   `fs.writeFileSync` — all inside the same Node process, so no large
   base64 string ever needs to pass through your own output.
4. **Verify every output file before reporting success** — this is not
   optional, it's what catches problem #2 above before it reaches the
   user. Check PNG magic bytes and IEND chunk are present, sanity-check
   file sizes are consistent with each other (a wildly smaller file than
   its siblings is a red flag), and actually view at least one sample per
   distinct palette/state combination with the Read tool to confirm it
   shows the correct content — not just that it decodes as *a* valid PNG.

## When NOT to use this

If the request is about the widget's live, interactive behavior itself
(testing that a button works, checking layout at different viewport
sizes, verifying an in-browser bug) — that genuinely needs a browser, use
the browser tools normally. This skill is specifically for "produce a
real static image file on disk," where the headless/local path is always
better than driving a browser's UI.

## Extending this skill

Add more example palettes, resolution presets, or output-naming
conventions to `scripts/generate-variations.js` as they come up, and note
any new gotchas discovered in the "Why this exists" section above so the
next invocation doesn't rediscover them the hard way.
