# LRC cruise-climb pilot publication, 22 November 2026

Adds `lrc-cruise-climb.html` and links it from the overview, Flight Lab, Methods, Archive and navigation.

## Sources

- **Files.** `data/lrc-cruise-climb-pilot/` holds byte-identical copies of the pilot's results report, four CSV tables and outcome figure. They come from the private source repository `MH370-Ocean-GLORYS-Data`, branch `claude/post1941-full-population-campaign`, report commit `be1c59fa1530b446afe42e60c934fb27062f03aa`.
- **Identities.** `source_manifest.json` records the SHA-256 of every file, the run, release and review commits, and the recorded time account.
- **Review.** The report includes Codex's report-only corrections from `LRC_Pilot_Results_Review_2026-11-22_e80252c47000.zip` (SHA-256 `8c7787f7…7750`).

## Build and checks

- `python3 scripts/build_lrc_pilot.py --check` verifies the file hashes against the manifest. It also recomputes every displayed count from the CSVs: 48 sides, 10 accepted, 7 converged, 18 fuel exhausted before 00:11, 20 without a starting point, 42 retained records, 37 unavailable at 00:19 and 10 resolved repeats.
- `python3 gen.py` inserts these values into the page bodies.
- The generated pages were checked over local HTTP at 1366 px and 400 px width. Neither width scrolls sideways, and no placeholder is left unfilled.

## Scope

This is a saved-record publication only. No model was imported and no flight was computed. Nothing was evaluated at 22:41: that assessment is a later stage and is labelled as not yet run. The 90–180 s fuel-event screen is a separate conditional assumption and is not published here. Existing datasets, catalogues and the signed assessment are unchanged.
