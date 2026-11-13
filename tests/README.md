# Flight Lab display and preservation checks

## Focused controller and renderer regressions

Run these from the repository root (Node 24 was used during development):

```sh
npm ci --prefix tests --ignore-scripts --no-audit --no-fund
node tests/flight_lab_dom.cjs
node tests/flight_lab_renderer.cjs
```

Both suites use jsdom from `tests/package.json`. The shared `flight_lab_harness.cjs` loads the published data asset, the production `scene3d.js`, and the production application. It controls interval timers and animation-frame delivery. Canvas2D rasterization is replaced with no-op drawing calls, while the renderer's projection, draw traversal, hit regions, candidate lookup, and pointer handlers run unchanged.

The controller suite checks the reviewed user flows: the main Forces tab and the dedicated inspector button preserve the first transmission's flight, response, and epoch; records without force data stay selected and report the absence; returning preserves the original selection; grid, dropdown, and guided entry identify the same worked-example supplement; another response on that parent cannot inherit the witness states. It retains the prior missing-value, recorded/derived-mass, slider-identity, timer-cancellation, and stale-selection regressions.

The same suite checks the terminal close-up using the actual projection at a 768×480 CSS-pixel canvas. It asserts that all three terminal checkpoints are inside the frame and that the final-transmission markers are more than 24 pixels apart. It checks the explicit checkpoint list, recorded height loss and eight-second interval, absence of spatial path connectors, and the actual overview pointer-event → overlap chooser → exact checkpoint flow. The JSON output reports measured projection coordinates and final-transmission marker separation.

The renderer suite separately checks the reviewed near-overlap geometry, duplicate selected-marker IDs, and real pointer dispatch for overlapping, single, and empty hits. These are display-geometry and controller checks. They do not establish browser raster appearance, text layout, touch behavior, or scientific-model validity. Neither suite runs a flight integration or reads protected scientific records.

## Optional browser suite

`flight_lab_regression.cjs` is a separate Playwright browser test. It requires Playwright, Chromium at `/usr/bin/chromium`, and a served preview at `http://127.0.0.1:8765` (or `ATLAS_URL`). It has been updated for the main Forces-tab, alternative-flight, consistent-entry, and terminal-list regressions. Updating this script is not a passed browser run. Execute it only in an environment that permits browser automation, and report browser/CUA verification separately from the Node results.

## Historical preservation checks

Run from the repository root:

```sh
python3 gen.py
python3 tests/check_preservation.py
python3 tests/check_editorial_preservation.py
python3 tests/check_local_links.py
```

Preservation checks compare with the exact pre-recovery commit. The two table checks count different things: numeric-containing cells and numerical tokens. Neither is a scientific validation of the original numbers.

Historical note, 12 November: adding the lower-speed results row to `index.html` changed that earlier preservation comparison by four added cells, with none removed or altered; the other pages were then reported unchanged. Those counts describe that earlier update, not a fresh check of the present tree.

Those historical baselines are not a claim that later authorized Atlas edits are unchanged. For a new display repair, compare the scientific data, source manifest, signed assessment, and held drift files directly against that repair's actual base commit as well.

Historical note, 13 November: the northern closing-run row and the two new list items in `index.html` were rewritten for the completed run, so `check_preservation.py` and `check_editorial_preservation.py` report `index.html` as changed against the pre-recovery baseline. No other file is reported changed. The signed assessment, the drift pages and the Flight Lab data are byte-identical to the previous commit.
