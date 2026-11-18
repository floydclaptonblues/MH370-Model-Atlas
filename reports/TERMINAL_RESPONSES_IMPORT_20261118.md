# Terminal responses of the cruise catalogue: Atlas import, 18 November 2026

Base: `cce1e038` (Atlas `main`). Source: `floydclaptonblues/MH370-Ocean-GLORYS-Data` at `429c11c4d41d7f26de46aaa71e74cba0cc3b401e`, `reports/diagnostic/CATALOGUE_TERMINAL/`, calculation revision `c370b2cf70b9`.

Ryan Hall asked for the Atlas to be updated with the accepted terminal-response results and their provenance exception.

## Changes

- New page `terminal.html` (body `src/terminal_body.html`), reached from the overview, the flight-histories page, the methods and archive pages and the Flight Lab note. It is not added to the navigation bar; it highlights "Flight histories".
- New data package `data/terminal-responses-266/`: 17 source files copied byte for byte, a source manifest with hashes, the compiled display values, the reconciliation record and a README.
- New compiler `scripts/build_terminal_responses.py`. `gen.py` gained a `fill()` step that inserts compiled values into `{{name}}` placeholders in the terminal, overview, flight-histories, methods and archive bodies.
- Overview: a results section, a chapter card, two list items under "Where the evidence stands" and a population-label paragraph. The sentence saying the final-transmission tests had not run is replaced.
- Methods: a section stating what the terminal experiment tested and the role of each measurement. Archive: a campaign entry with hypotheses not supported and the provenance exception. Flight histories: one paragraph. Flight Lab: one sentence, outside the earlier-catalogue section; the viewer itself is unchanged and does not display terminal responses.
- `common.js`: the status lamp "Terminal follow-up: not run" now reads "Terminal responses: 90 flights". The Flight Lab's cache-refresh string for that script was updated.
- `README.md`, `tests/README.md`: build and check instructions.

## Not changed

- `assessment.html` and `src/assessment_body.html`. Ryan Hall's signed assessment contains a dated calculation update of 16 November stating that the terminal calculations for the cruise catalogue have not run. That statement is now out of date. It was left as written and reported to him; it is his to revise.
- `drift.html` to `drift4.html`, `currents.html` and their sources.
- The historical AI assessment, the cruise-catalogue data package, the Flight Lab data, assets and offline download.
- The source repository. No flight was computed, and nothing was evaluated at 22:41.

## Verification performed

- Each copied file was written from the pinned commit with `git show`; its Git blob identity equals the one at the head of the source branch on 18 November.
- `python3 scripts/build_terminal_responses.py --check`: 17 source files match the manifest; 217 displayed values and 341 reconciliations reproduce the committed outputs.
- The compiled values were compared with the reviewed findings document. Counts agree. Three values differ in the last digit for known reasons, listed in `data/terminal-responses-266/README.md`.
- `python3 scripts/build_cruise_catalogue.py --check`: passed.
- `python3 gen.py` rewrote only `terminal.html`, `index.html`, `flighthistories.html`, `methods.html`, `archive.html` and `flight-lab.html`. No `{{` remains in any generated page.
- Against the base commit, no numerical token was removed from any existing page.
- `python3 tests/check_local_links.py`: 261 local file links checked, none missing.
- Node display suites: `flight_lab_dom` (46 passed), `flight_lab_renderer` (8), `flight_lab_readouts` (21), `cruise_production_lab` (15 checks, passed), `cruise_grid` (13).
- Browser check with Chromium (Playwright) on a local server at 1280 px and 400 px widths for the six changed pages: no horizontal overflow, no image failing to load, no script error, no placeholder text left. The new page and the new overview section were inspected as screenshots.

## Not verified

- The optional Playwright suite `flight_lab_regression.cjs` was not run.
- `check_preservation.py` and `check_editorial_preservation.py` compare with a pre-recovery baseline and already reported differences before this update; they were not used as evidence here.
- Rendering in browsers other than Chromium, and on the published site after deployment.
