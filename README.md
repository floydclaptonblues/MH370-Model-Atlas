# MH370 Model Atlas

A static research atlas of the project's satellite-measurement, aircraft-performance and ocean-transport experiments. It distinguishes observations, declared assumptions, calculated states, numerical checks and interpretation. Conditional airborne positions are not crash locations, and record counts are not probabilities.

## Reading the Atlas

- `index.html`: published experiment summaries and links to their source records.
- `mach080-084.html`: the separate 21 November TASK042 starting-Mach experiment, its ten selected samples, numerical checks, fuel-window sensitivity and assumed starting-state scope. These records are not added to the 108-arrival catalogue.
- `methods.html`: current experimental workflow first, with earlier methods and corrections in a dated, collapsed archive.
- `flighthistories.html`: the separately identified six-history dossier and its terminal assumptions, plus links to later work.
- `canonical.html`: measurement and source-data scope.
- `archive.html`: attempts, retirement reasons and provenance.
- `assessment.html`: Ryan's signed interpretation, separate from numerical results.
- `flight-lab.html`: the completed 108-arrival cruise catalogue, with filters, saved airborne positions, directional search outcomes, fuel and numerical-check scope. The earlier terminal catalogue remains a separately labelled view. See `flight-lab/README.md` for both pinned sources.
- `terminal.html`: terminal responses of the accepted cruise flights at the two final transmissions, with their conditional airborne positions, endings, limits and provenance exception.
- `arc7-demo.html`: illustrative satellite geometry and simplified fuel–mass teaching tool. See `src/arc7_demo_NOTES.md`.
- `drift.html`, `drift2.html`, `drift3.html`, `drift4.html`: separate ocean-transport studies and diagnostics, with experiment-specific forcing and limitations.

Older satellite and flight pages remain available as historical records. Their scoring rules, parameter ranges and closed-task statements must not be treated as the current project's universal policy. Each later experiment's frozen method and final accounting govern its own results.

## Sources and presentation

`src/` contains page bodies and selected scripts. `gen.py` combines these with the shared shell and inline historical templates. `data/`, `img/` and `fields/` hold published display assets. The Lab has its own compiled dataset, source manifest and offline download under `flight-lab/`.

The Lab displays saved states, not continuously simulated motion. State, time, cursor and variables must refer to the same selected record. Missing fields stay unavailable. Illustrative wind controls and approximate explanatory quantities remain distinct from retained model outputs. The current cruise catalogue contains no 22:41 prediction or residual. Earlier exposure of that measurement is disclosed in the source project; it is not described as a sealed holdout.

The completed cruise catalogue is compiled from nine byte-verified published files pinned to `24655869cf3fe2452615157cf59c1ed3f28c3677` (including the final findings). Run `python3 scripts/build_cruise_catalogue.py --check` to verify the display export against those saved inputs. This imports results only; it does not integrate, fit or restart a flight. The cruise catalogue itself holds no terminal response; those are a separate import, described next.

The terminal responses of the cruise catalogue (`terminal.html`) are compiled from 17 byte-verified published files pinned to `429c11c4d41d7f26de46aaa71e74cba0cc3b401e`, held in `data/terminal-responses-266/sources/`. `python3 scripts/build_terminal_responses.py` recomputes every displayed count and range from those tables and writes `display.json`; `gen.py` inserts the values into placeholders, each a name in double braces, in the page bodies, and an unknown name stops the build. Run the script with `--check` to verify the source identities and the committed outputs. This imports results only: no flight is computed and nothing is evaluated at 22:41. See `data/terminal-responses-266/README.md`.

## Build

The separate starting-Mach publication uses byte-identical saved report, CSV, audit and figure files in `data/task042-mach080-084/`, plus a labelled compact extraction of the comparison record. `python3 scripts/build_task042_mach.py --check` verifies source hashes, reconciles the selected CSV rows and checks the generated table values. Run without `--check` to regenerate its display export before `gen.py`. This reads saved results only; it imports no model and computes no flight. The full run archive is hash-identified rather than duplicated in the site repository.

From the repository root:

```sh
python3 gen.py
```

Serve the checkout through local HTTP for browser checks; pages that fetch JSON are not adequately tested with `file://`. Check the generated diff before publishing, including source/generated-page consistency, navigation, assets and desktop/mobile controls. No scientific model needs to be run to build this site.

## Preservation

Editorial and interface maintenance must preserve numeric datasets, source identities, scientific acceptance criteria and the signed assessment unless a separate authorized scientific change requires otherwise. Preserve meaningful corrections and superseded results with their dated scope. Do not infer physical exclusion from a model-support stop, a finite search failure or a policy boundary. Distinguish fitted measurements, diagnostics and independent tests, and preserve each experiment's holdout policy.

`directives/` contains historical task briefs and amendments. Those records document their original scope; they are not fresh execution instructions.
