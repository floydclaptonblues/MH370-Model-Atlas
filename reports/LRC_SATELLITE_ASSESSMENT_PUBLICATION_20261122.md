# LRC satellite assessment publication — 22 November 2026

This update publishes the completed fixed-recipe assessment of the LRC pilot at 22:41:22 and the 23:14:03 voice-frequency diagnostic. Stage A and Stage B had already completed before this publication. No flight, replay, prediction, observation comparison or new scientific test was run to make this site update.

## Publication scope

The LRC page now includes the completed assessment, its record and distinct-recipe counts, the three distinct recipes outside the timing band, frequency ranges by arrival and schedule, numerical agreement and the reviewed interpretation. The Overview, Flight Lab, Methods, Archive and existing 22:41 page link to that section. Stale statements that this LRC assessment had not run are removed, including the LRC-specific status in the shared sidebar. Its script version is refreshed on the LRC page so browsers receive the updated status.

The assessment covers all 42 retained pilot records, representing 41 distinct recipes. It does not add records to the separate 266-flight cruise-catalogue comparison. The pilot report, tables, figure and original publication record remain unchanged.

The fuel-event definition on the LRC page is clarified: total remaining fuel reaches the model's 6.80 kg APU reserve, leaving zero engine-usable fuel. This is a wording clarification, with no changed event or result.

## Results and interpretation preserved

- 22:41 timing: 38 of 42 records, or 38 of 41 distinct recipes, meet the inclusive ±43 µs criterion. Four records represent three distinct outside-band recipes. All original labels remain intact.
- 22:41 centred frequency: all 42 records, or 41 recipes, are within the ±7 Hz diagnostic band.
- 23:14 raw frequency: the 10 own-Mach controls are inside the descriptive ±7 Hz reference band. The 32 climbing-LRC records, representing 31 recipes, are outside it.
- There are no full-step/half-step band-edge straddles. Numerical repeatability is not a physical-model uncertainty budget.
- The voice-channel offset is unknown and is not estimated. Its aggregate standard uncertainty is unassigned. The controls are closer under the frozen raw convention; an unknown common offset can change which family is closer to the calibrated observation. The signed prediction separation does not establish a preferred or more likely family.
- Records are alternative histories, not independent measurements. Both observations had prior exposure. No route is fitted, selected, ranked or vetoed by this assessment. No fuel-event timing screen is applied. G6 stays advisory.
- No terminal-motion, final-transmission compatibility or impact-location result is added.

## Exact records

Assessment revision: `5a05740c69d6c81f0562b76c30d4de5fe8503767070893fb3cd34a5609eccc7a`.

Stage A seal SHA-256: `c13672ac972d8abaf89332f95b8e049cc592a3b94e75499c6962a2514d84457c`.

Stage B release SHA-256: `b9e81d35caa3b4c17579ad0034896265029d5c00b3eb19d00e78aa91ba0de7a3`.

The new `data/lrc-cruise-climb-assessment/` directory contains byte-identical copies of the returned CSV, JSON and summary, plus the reviewed publication text. Its `source_manifest.json` records exact copied-file identities and the return/review archive hashes. Private execution paths and approval files are not published.

## Verification before publication

- `python3 scripts/build_lrc_pilot.py --check` passes; original pilot sources and display values still verify.
- `python3 scripts/build_lrc_assessment.py --check` passes. It verifies source hashes, CSV/JSON correspondence, all 42 records, the 41-recipe mapping, the original labels and summary, and the generated display values. It reads saved records using the standard library only.
- `python3 gen.py` completes with no unresolved placeholders. Exactly the six intended generated pages change: Overview, LRC, 22:41, Methods, Archive and Flight Lab. Other generated pages match the pinned repository tree.
- A bounded link check resolves 194 local references in those six pages against the pinned repository tree plus new files, including 54 available-page anchors, with none missing. Changed Markdown contains no Liquid template delimiters.
- A separate editorial review found the count denominators, unchanged bands, prior-exposure statement and unknown-offset interpretation consistent with the reviewed publication text.
- Local desktop/mobile screenshot checks could not run: the Playwright-managed browser was absent, and the installed Chromium could not open a required process socket in this environment. No local visual-test pass is claimed. The existing site stylesheet and table scroll containers are reused.

The source snapshot used for this update is Atlas commit `d0da9c835b10a82d8611bfc3953944e29559bfc8`. Publication uses a new commit and an expected-head check so concurrent repository changes cannot be overwritten.
