# Completed 108-arrival cruise run — Atlas display data

This directory publishes the completed cruise-level study in the Flight Dynamics Lab. It is a separate catalogue from the earlier terminal-response snapshot. The import does not integrate a flight, refit a route, change a scientific result, evaluate a withheld measurement, or interpolate an aircraft state.

## Source identity

- Repository: `floydclaptonblues/MH370-Ocean-GLORYS-Data`
- Results commit: `24655869cf3fe2452615157cf59c1ed3f28c3677`
- Source directory: `reports/diagnostic/CRUISE_LEVEL_PRODUCTION_108/`
- Frozen flight runner: `2a016b1294fa`
- Results date: 16 November 2026
- `sources/` contains nine original published files, copied byte for byte. `source_manifest.json` records their byte lengths, Git blob SHA-1 identities and SHA-256 hashes.

The source commit includes the final wording corrections following review. The results tables are unchanged by those corrections.

## Displayed records

The dataset contains 108 arrivals, 424 configurations, 848 completed directional searches, and 266 distinct returned-flight representatives. There are 208 configurations with an accepted flight and 216 for which the completed bounded search found none. All 108 arrivals have an accepted flight at at least one tested level.

`PROD_SOLUTIONS.csv` contains 1,129 returned rows. The source marks 267 as distinct directional representatives and the remaining 862 as aliases. This compiler retains those source decisions. It merges two distinct directional representatives only when their configuration and three turn-command values are identical, giving 266 flights. It does not independently reclassify the source aliases. The full unchanged CSV remains available for inspection.

Flight identifiers such as `A006_TO250.F3` follow the sorted-command numbering used in the terminal manifest. No terminal result is implied by the shared identifier.

Each accepted flight has three saved position checkpoints: 20:41:05, 21:41:27 and 00:11:00 UTC. The arrival table also supplies the input position at 19:41:03. Fuel at the two earlier saved checkpoints was not exported in the solutions table and stays unavailable. The viewer must not infer a continuously saved track from those points. The fuel-exhaustion position is a separate saved airborne model state, not a contact or impact position.

Each flight keeps its directional source references, range-end flags, reported timing and frequency residuals, total fuel at 00:11, engine fuel above the imposed 6.80388555 kg APU reserve, and its continuation ending. An exhausted flight keeps its published UTC time and the more precise elapsed-time fields. The 37 flights still powered at 00:40 have no exhaustion time or exhaustion position.

The 218 numerical checks are attached to the specific repeated flights and source rows. A flight without its own repeat is not labelled numerically checked because another flight in the same configuration passed. Seven returned flights lie at a searched range end. The source method does not require a repeat for a direction returning only range-end flights.

## Meaning and limits

Acceptance means support under the chosen performance model, engine fuel remaining at 00:11, and timing residuals within 43 microseconds at the three fitted epochs. Later frequency residuals are reported diagnostics under the frozen calibration; they were not used for acceptance. Final-transmission compatibility, the electrical sequence and a terminal envelope for these flights were not calculated by this cruise study.

The result establishes outcomes at the tested levels. It does not establish continuous altitude bands, a global optimum, probabilities, or physical exclusion after an unsuccessful bounded search. Closely related arrivals are not independent confirmations. Model-support stops and numerical uncertainty remain distinct from a satellite-measurement mismatch.

The satellite setup's prior exposure to the withheld observation is documented by the project separately. This importer reads the final published tables, which contain no prediction or residual column for that epoch.

## Reproduce the import and validation

From the Atlas repository root:

```sh
python3 scripts/build_cruise_catalogue.py
python3 scripts/build_cruise_catalogue.py --check
```

The first command writes `catalogue.json`, `catalogue.js` and `validation.json`. The second verifies source identities and checks that the generated files are exact matches for a fresh compilation; it writes nothing. Neither command imports a flight solver.

The validation reconciles all 22 group-and-level rows, every configuration's accepted-flight count, all directional coverage, all check identities, command-identical source values, reserve arithmetic, 16,039 distinct trial flights, 229 exhaustion events and 37 powered horizons. It also verifies the 90 events before the first final transmission and the 139 after both final transmissions, without predicting either transmission.

`catalogue.js` exposes `window.CRUISE_PRODUCTION_108`. The JSON file has the same data. The generated values preserve the source's numerical precision for inspection; that precision is not a statement of accuracy for the real aircraft.
