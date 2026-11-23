# LRC fixed-recipe satellite assessment

The completed assessment compares the LRC pilot's 42 retained records, representing 41 distinct flight recipes, with the 22:41:22 timing/frequency observation and the 23:14:03 voice-frequency aggregate. It uses the original recipes and includes every retained record. This is a separate assessment of the LRC pilot, not an extension of the 266-flight cruise-catalogue comparison.

`ASSESSMENT_42_ROWS.csv`, `ASSESSMENT_42_ROWS.json` and `SUMMARY.json` are byte-identical copies of the returned Stage B outputs. `REVIEWED_INTERPRETATION.txt` is the reviewed publication text. `source_manifest.json` records their exact identities, the assessment revision, the Stage A seal, the release and the returned/review archive hashes. The full archives are identified by hash rather than duplicated in the site repository.

The 22:41 timing label uses the predeclared inclusive ±43 µs band. Its frequency diagnostic uses the existing centred residual, raw observed-minus-predicted minus −0.18 Hz, against ±7 Hz. The voice diagnostic reports raw observed-minus-predicted frequency against a descriptive ±7 Hz reference band, without transferring the handshake bias or estimating a voice-channel offset. The voice aggregate's standard uncertainty remains unassigned. Its representative instant is not the average time of the contributing units and is not an average of predictions over those units.

The controls and climbing LRC histories give different voice-frequency predictions. A common unknown channel offset preserves their signed difference but can change which family lies closer to the observation. These alternative flight recipes are not independent measurements. No route is selected, ranked or vetoed by the diagnostic. All outside-band labels remain as recorded.

Both observations have disclosed prior exposure. G6 remains advisory and no fuel-event timing screen is applied. The assessment adds no terminal motion, final-transmission compatibility or impact-location result.

## Publication build

From the Atlas repository root, run `python3 scripts/build_lrc_assessment.py` to compile `display.json`, or add `--check` to verify the committed display export. The compiler reads saved CSV/JSON only, checks their source hashes and labels, reconciles record/distinct-recipe counts and formats the page's counts, ranges and tables. It imports no flight model and computes no flight, new prediction, offset estimate or changed scientific criterion.
