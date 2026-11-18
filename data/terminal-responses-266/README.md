# Terminal responses of the accepted cruise flights: Atlas display data

This directory publishes the terminal-response experiment that follows the completed 108-arrival cruise catalogue. The import does not integrate a flight, refit a route, change a scientific result, evaluate a withheld measurement, or interpolate an aircraft state.

## Source identity

- Repository: `floydclaptonblues/MH370-Ocean-GLORYS-Data`
- Results commit: `429c11c4d41d7f26de46aaa71e74cba0cc3b401e`
- Source directory: `reports/diagnostic/CATALOGUE_TERMINAL/` (tables and figures in its `RESULTS/` subdirectory)
- Calculation revision: `c370b2cf70b9`, applied to cruise flights of revision `2a016b1294fa`
- Results dates: 16 and 17 November 2026; imported 18 November 2026
- `sources/` contains 17 original published files, copied byte for byte: four documents, eight tables, one summary and four figures. `source_manifest.json` records their source paths, byte lengths, Git blob SHA-1 identities and SHA-256 hashes.

The source commit is the last one that changed any of these files. It includes the provenance exception and the review record in the findings.

## What the tables hold

Of the 266 accepted cruise flights, 90 have a saved engine-fuel exhaustion before 00:19:29 UTC and were propagated. The other 176 are listed in `FLIGHTS_NOT_PROPAGATED.csv`: 139 whose engine fuel runs out after both final transmissions and 37 with engines running at 00:40. They were not rejected; a fuel event after a transmission cannot have caused a response before it, and no other sequence was examined.

`RESPONSES.csv` has one row for each of the 12,420 sampled responses (138 for each flight: onset times from 60 s before to 8 s after 00:19:29 at 1 s spacing, bank to the left and to the right). `CONTINUATION_ENDINGS.csv` has one row for each of the 5,500 endings of the 1,375 continued responses (two bank laws and two drag formulations after Mach 0.89). The remaining tables are summaries of those two, the numerical checks, and the single provenance exception.

The tables contain predicted timing and frequency at 00:19:29 and 00:19:37 only. They contain no prediction, residual or comparison for 22:41. Prior exposure of that measurement is disclosed by the source project; it is not described as unread or as a sealed holdout.

## Displayed values

`scripts/build_terminal_responses.py` reads the copied tables and writes `display.json`: formatted counts and ranges under short names. `gen.py` inserts them wherever a page body contains `{{name}}`; an unknown name stops the build. Results shown on `terminal.html` and in the terminal-response passages of the overview, flight-histories, methods and archive pages therefore come from the tables and are not typed by hand. Constants of the method (for example the 62 µs band, the 18,400 µs reference value and the warm-up ranges), the recorded measurements, and the reviewed count of 13,925 planned identities are quoted from the method and findings.

`validation.json` lists the reconciliations the compiler performs before writing anything: outcome counts against the published summary, 180 responses at every onset time, per-group counts against the group table, four endings for each continued response, the query counts, the burn rate implied by the table against the fuel and power account, and the identity of the provenance exception.

## Differences from the findings document

The page was compiled independently of the findings' own analysis script. The counts agree. Three displayed values differ in the last digit, and the cause of each is known:

- The eastern bound of the Mach 0.75 group arriving at 25,661 ft at 00:19:29 reads 92.09°E here and 92.10°E in the findings. The stored maximum is 92.09497°E; the findings rounded a three-decimal value a second time.
- The distance from the two Mach 0.75 groups to the Mach 0.67 group reads about 505 km here and about 500 km in the findings. Both are rounded distances between cluster centres.
- The largest difference between drag formulations in the Mach 0.67 group reads "under 0.03 km" here and "under 0.02 km" in the findings. The stored maximum is slightly above 0.02 km.

Heights above the model surface for endings at the lowest weather level are given for each row of the endings table here (for example 219 to 220 m for the Mach 0.67 group); the findings give the overall range, 219 to 232 m, on every row.

## Meaning and limits

Every position is a state of the model under its stated assumptions. The collection is a conditional terminal envelope of the sampled responses. It is not a probability map and not an outer bound, and no path reaches the model surface. Counts are counts of sampled responses. The 90 flights share their fitted cruise measurements, so repeated outcomes are not independent confirmations. A stop at the operating-speed limit is a limit of the model, not a mismatch with a measurement. A joint satellite match does not establish an electrical explanation.

One response, `A052_TO275.F1`, left bank, onset 2 s after 00:19:29, was computed twice because publication erased its first stored result and settlement. The second computation is retained. Equality with the lost first computation cannot be established. It is marked in `RESPONSES.csv` and listed in `PROVENANCE_EXCEPTIONS.csv`.

The rectangle 32 to 33°S, 94 to 96°E appears on the overview map and in the summary as a query on the finished results. It entered no calculation, selection or rule.

## Reproduce the import and validation

From the Atlas repository root:

```sh
python3 scripts/build_terminal_responses.py
python3 scripts/build_terminal_responses.py --check
python3 gen.py
```

The first command writes `source_manifest.json`, `display.json` and `validation.json`. The second verifies that the source files match the manifest and that the committed outputs equal a fresh compilation; it writes nothing. Neither imports a flight solver. This is a display import and a reconciliation of published tables, not a scientific revalidation.
