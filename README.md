# MH370 Model Atlas

A static research atlas of the project's satellite-measurement, aircraft-performance and ocean-transport experiments. It distinguishes observations, declared assumptions, calculated states, numerical checks and interpretation. Conditional airborne positions are not crash locations, and record counts are not probabilities.

## Reading the Atlas

- `index.html`: published experiment summaries and links to their source records.
- `methods.html`: current experimental workflow first, with earlier methods and corrections in a dated, collapsed archive.
- `flighthistories.html`: the separately identified six-history dossier and its terminal assumptions, plus links to later work.
- `canonical.html`: measurement and source-data scope.
- `archive.html`: attempts, retirement reasons and provenance.
- `assessment.html`: Ryan's signed interpretation, separate from numerical results.
- `flight-lab.html`: Windows 98 scientific viewer of a frozen catalogue snapshot. See `flight-lab/README.md` for the pinned source and coverage; later experiments are not imported automatically.
- `arc7-demo.html`: illustrative satellite geometry and simplified fuel–mass teaching tool. See `src/arc7_demo_NOTES.md`.
- `drift.html`, `drift2.html`, `drift3.html`, `drift4.html`: separate ocean-transport studies and diagnostics, with experiment-specific forcing and limitations.

Older satellite and flight pages remain available as historical records. Their scoring rules, parameter ranges and closed-task statements must not be treated as the current project's universal policy. Each later experiment's frozen method and final accounting govern its own results.

## Sources and presentation

`src/` contains page bodies and selected scripts. `gen.py` combines these with the shared shell and inline historical templates. `data/`, `img/` and `fields/` hold published display assets. The Lab has its own compiled dataset, source manifest and offline download under `flight-lab/`.

The Lab displays saved checkpoints, not continuously simulated motion. State, time, cursor and variables must refer to the same selected record. Missing fields stay unavailable. Illustrative wind controls and approximate explanatory quantities remain distinct from retained model outputs. The viewer excludes the sealed 22:41 observation and its withheld numerical predictions.

## Build

From the repository root:

```sh
python3 gen.py
```

Serve the checkout through local HTTP for browser checks; pages that fetch JSON are not adequately tested with `file://`. Check the generated diff before publishing, including source/generated-page consistency, navigation, assets and desktop/mobile controls. No scientific model needs to be run to build this site.

## Preservation

Editorial and interface maintenance must preserve numeric datasets, source identities, scientific acceptance criteria and the signed assessment unless a separate authorized scientific change requires otherwise. Preserve meaningful corrections and superseded results with their dated scope. Do not infer physical exclusion from a model-support stop, a finite search failure or a policy boundary. Distinguish fitted measurements, diagnostics and independent tests, and preserve each experiment's holdout policy.

`directives/` contains historical task briefs and amendments. Those records document their original scope; they are not fresh execution instructions.
