# Verification before publication, 12 November 2026 (Claude)

Starting point: remote `main` at `e79b34e` (Flight Dynamics Lab added). The recovered commit `158fb35` was imported from the supplied bundle (verified; it descends directly from `e79b34e`). No earlier edits of this kind existed in this workspace, so nothing else was recovered or merged.

Changes made on top of the recovered commit:

1. Drift pages restored to the published baseline (see `DRIFT_EDITS_HELD_20261112.md`).
2. Lab state inspector: the mass label read "derived" for every state that carried any origin text, including the three states whose mass is recorded. It now reads "Mass · derived" for algebraically derived mass and "Mass · recorded" for recorded mass.
3. Offline package rebuilt so its controller equals the corrected online controller.

Checks run here (all on the final tree):

- `python3 gen.py`: generated pages equal the committed pages.
- `tests/check_preservation.py`, `tests/check_editorial_preservation.py` (3,039 numeric table tokens in the same page and order; signed assessment, Lab dataset and drift pages byte-identical to the baseline), `tests/check_local_links.py` (183 local references resolve).
- `node tests/flight_lab_dom.cjs`: 25 controller checks pass.
- Real Chromium (Playwright), desktop 1440x1000: `tests/flight_lab_regression.cjs` logic, 20 checks pass, no script errors.
- Additional real-browser checks, desktop and iPhone 13 emulation: an uncomputed configuration shows "No saved flight available" with flight cleared, and the toolbar remains usable afterwards; all 278 returned flights selected in turn show the identity, configuration, latitude and longitude of their own saved record, with no missing value displayed as zero; the slideshow run on its real timer ends at checkpoint 7 of 7 with slider, UTC label, fuel cursor and button state in agreement; no horizontal overflow; canvas drawn.
- All 20 root pages loaded on desktop and mobile with every collapsed section opened: no script errors, no horizontal overflow, no zero-size map or canvas.
- Offline package: archive integrity passes; `app.js`, `data.js`, `scene3d.js` equal the online files; opened from disk in Chromium, worked example and checkpoint selection work without errors.
- Dataset SHA-256 `652729047a556b5bee46363f5aa6bc296466c5eaffcd20d5f7c1f1fb3ef28b7e`, unchanged.

Not verified: external resources (web fonts, map tiles and other third-party hosts) could not be reached from the test machine, so pages that draw on them were checked for layout and script errors only; browsers other than Chromium; real touch input on a physical phone; pixel-level comparison against earlier screenshots. No model was run, the lower-speed experiment is not included, and the 22:41 observation was not read.
