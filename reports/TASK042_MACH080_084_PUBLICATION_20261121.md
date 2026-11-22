# Starting Mach 0.80–0.84: Atlas publication record

Ryan requested publication of the completed separate experiment on 21 November
2026. This update imports saved results and creates a dedicated results page,
linked from the overview, Flight Lab, methods, archive and navigation.

## Source and interpretation

- Experiment: `TASK042_Mach080_084_20261121_001`.
- Frozen scientific revision:
  `11f3ec951da4ac4d05bccbc5a8cf620063aff97b815ab5703cf2254687efad25`.
- Atlas publication base: `5221c2b78416b0a4caede67cee09d1bb9590bb86`.
- File identities: `data/task042-mach080-084/source_manifest.json`.

The report, CSV, closing audit, frozen design and two figure formats are copied
byte for byte. The compact comparison JSON is a labelled extraction; it omits
full trajectories and resource traces, while retaining selected identities,
all twenty numerical comparisons and per-mesh fuel-window margins. The full
run archive is hash-identified and is not stored in this website repository.

The publication distinguishes starting Mach from constant Mach, model support
and numerical verification from statistical fit acceptance, sampled bests from
certified minima, and supported 00:11 states from terminal or impact positions.
It preserves the assumed historical starting fuel/mass and the lack of an
established incoming radar-connected history. The 22:41 BTO exclusion, fitted
22:41 BFO and prior exposure are stated explicitly. Fuel-window edge sensitivity
and all seven capped searches remain visible.

## Publication checks

- Saved-source compiler and `--check`: passed. Every CSV field agrees with the
  compact record; ten selected rows and twenty comparisons reconcile.
- Isolated compiler check using only committed publication inputs: passed.
- `gen.py`: repeated generation produces identical HTML.
- Local file-link check: 324 links checked, none missing.
- Shared navigation and new-page DOM check: passed for the new page, overview,
  methods, archive and Flight Lab. The new page has its own ten-sample context;
  the existing catalogue retains its 266-flight context.
- Existing Flight Lab suites: controller 46, renderer 8, readouts 21,
  cruise-production 15 and cruise-grid 13 checks passed (103 total).
- 109 existing scientific assets, signed/held pages and shared stylesheet
  compared byte for byte with the publication base: unchanged.

The DOM suites omit browser rasterization. The local Chromium screenshot
attempt could not start because the environment refused its socket; the cloud
browser could not reach the local preview. Those attempts are not passed visual
checks. Deployment and live-page verification are reported separately.

This publication performs no model import, integration, fit, new prediction or
G6 execution. The other scientific repositories and their campaign records are
not modified. The Atlas is the publication repository only.
