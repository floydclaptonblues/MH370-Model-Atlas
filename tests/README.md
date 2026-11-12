# Display and preservation checks

Run from the repository root:

```sh
python3 gen.py
python3 tests/check_preservation.py
python3 tests/check_editorial_preservation.py
python3 tests/check_local_links.py
npm install --prefix tests
node tests/flight_lab_dom.cjs
```

The DOM suite uses jsdom from `tests/package.json`, stubs the canvas renderer and controls timers. It does not validate pixels or real browser behavior.

`flight_lab_regression.cjs` is a separate Playwright browser test. It requires Playwright, Chromium at `/usr/bin/chromium`, and a served preview at `http://127.0.0.1:8765` (or `ATLAS_URL`). It was blocked at browser startup during this recovery; it is not a passed test. Use it in an environment with supported browser execution before claiming browser QA.

Preservation checks compare with the exact pre-recovery commit. The two table checks count different things: numeric-containing cells and numerical tokens. Neither is a scientific validation of the original numbers.

Note, 12 November (later): the lower-speed results added one row to the results table on `index.html`, so the two table-preservation checks, which compare with `e79b34e`, now report that page as changed (4 cells added, none removed or altered). All other pages still pass.
