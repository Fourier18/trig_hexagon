// Template script for generating real PNG variations of the trig hexagon
// widget, directly from its own real rendering code via headless Chromium.
// No browser UI, no downloads folder, no manual base64 handling.
//
// Usage: copy this file into a working output folder, edit the CONFIG
// section below, then run `node generate-variations.js`.
//
// See ../SKILL.md for why this approach exists and what it replaces.

const path = require('path');
const fs = require('fs');
const puppeteer = require('puppeteer');

// ============================== CONFIG ==============================

// Path to the real widget. Adjust the relative path if this script isn't
// sitting one level below the project root.
const INDEX = 'file://' + path.resolve(__dirname, '..', '..', '..', '..', 'index.html');

// Where to write the output PNGs.
const OUT_DIR = __dirname;

// Each entry: { tag: 'shows-up-in-filename', colors: { 'input-id': '#hex', ... } }
// An empty colors object means "use whatever is currently live/default" —
// useful as a baseline palette. Find input ids by reading the Colors
// accordion in index.html (c-bg, c-hex, c-hex-fill, c-diag, c-label,
// c-center, c-sphere, c-sphere2, c-hi, c-fbtn as of this writing — but
// don't trust that list blindly, read the actual current HTML).
const PALETTES = [
  { tag: 'default', colors: {} },
  // { tag: 'example-variant', colors: { 'c-label': '#000000', 'c-center': '#000000' } },
];

// Canvas render size. The on-screen canvas is 600x600 natively; this just
// controls the Puppeteer viewport, not the actual image resolution (that's
// whatever hex-canvas's width/height attributes are, read from the DOM).
const VIEWPORT = { width: 800, height: 800 };

// ============================ END CONFIG =============================

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);
  await page.goto(INDEX, { waitUntil: 'load' });

  // Discover the current identity-overlay states directly from the live
  // page rather than hardcoding them, so this keeps working if the menu
  // changes later.
  const states = await page.evaluate(() =>
    Array.from(document.querySelectorAll('.id-item[data-id]')).map(el => el.dataset.id)
  );
  console.log('Discovered states:', states.join(', '));

  const written = [];
  for (const palette of PALETTES) {
    // Set real color inputs and dispatch a real 'input' event — this is
    // what the app's own bind() listens for, so it's genuinely driving
    // the real UI state, not a shortcut around it.
    await page.evaluate((colors) => {
      for (const [id, val] of Object.entries(colors)) {
        const el = document.getElementById(id);
        if (!el) throw new Error(`No element #${id} — check the id is correct`);
        el.value = val;
        el.dispatchEvent(new Event('input', { bubbles: true }));
      }
    }, palette.colors);

    for (const state of states) {
      const dataUrl = await page.evaluate((id) => {
        currentId = id;
        document.querySelectorAll('.id-item[data-id]').forEach(i => i.classList.toggle('sel', i.dataset.id === id));
        draw();
        return document.getElementById('hex-canvas').toDataURL('image/png');
      }, state);

      const base64 = dataUrl.split(',')[1];
      const outPath = path.join(OUT_DIR, `${palette.tag}_${state}.png`);
      fs.writeFileSync(outPath, Buffer.from(base64, 'base64'));
      written.push(outPath);
      console.log('wrote', outPath);
    }
  }

  await browser.close();

  // Basic integrity check on every file written — catches truncation/
  // corruption before it's reported as done. Not a substitute for
  // actually viewing a sample of the outputs, but a fast first pass.
  console.log('\nVerifying', written.length, 'files...');
  for (const p of written) {
    const buf = fs.readFileSync(p);
    const hasHeader = buf.slice(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]));
    const hasIEND = buf.slice(-8, -4).toString('ascii') === 'IEND';
    if (!hasHeader || !hasIEND) {
      console.error('INTEGRITY CHECK FAILED:', p, { hasHeader, hasIEND, size: buf.length });
      process.exitCode = 1;
    }
  }
  console.log('All files structurally valid. Still view a sample manually to confirm correct content.');
})();
