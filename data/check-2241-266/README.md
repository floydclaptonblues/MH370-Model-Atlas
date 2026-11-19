# The 22:41 check on the 266 cruise flights: Atlas display data

This directory publishes the comparison of the timing recorded at 22:41:22 UTC with the prediction of each of the 266 accepted cruise flights. The import integrates no flight, forms no prediction and makes no comparison of its own: it copies published tables and formats values from them.

## Source identity

- Repository: `floydclaptonblues/MH370-Ocean-GLORYS-Data`
- Commit: `fccbd9c54941b7cc094d056ba8e202296c12d752`
- Source directories: `reports/diagnostic/CHECK_2241_CRUISE_266/` and, for the ground-station log cross-check, `reports/diagnostic/INMARSAT_LOG_CROSSCHECK_20261118/`
- Calculation revision: `91266581e659`, applied to cruise flights of revision `2a016b1294fa`
- Results date and import date: 18 November 2026
- `sources/` contains 21 published files, copied byte for byte: seven from the log cross-check (its findings, summary and five tables) and fourteen from the check itself: the three output files of the comparison, the predictions and the two records that fix them, the join to the terminal-response flights, the agreement of the two comparison programs, the record of the arithmetic repeated on the computing machine, and five documents. `source_manifest.json` records their source paths, byte lengths, Git blob SHA-1 identities and SHA-256 hashes.

## Who computed what

The predictions were computed on the machine that built the cruise catalogue and fixed before any comparison. The comparison itself was made by the project's independent reviewer (Codex), with the comparison program fixed beforehand and again with a separately written program; the first program was then run again on the computing machine and gave the same files. None of that happens in this repository.

## Displayed values

`scripts/build_check_2241.py` reads the copied tables and writes `display.json`: formatted counts and ranges under short names beginning `q_`, the rows of the group table, and the figure as inline SVG. `gen.py` inserts them wherever a page body contains a name in double braces; an unknown name stops the build, and so does a name compiled by both this script and the terminal-response script. The counts on `check2241.html` and in the 22:41 passages of the overview, flight-histories, terminal and methods pages therefore come from the tables and are not typed by hand.

Typed, not compiled: the limits of 0.1 µs and 0.01 Hz on the agreement of the two integration steps, the times of the commanded second turn, and the additional thresholds of 29 and 129 µs named in the text, all quoted from the method; and the status lamp in `common.js`, which carries no number. The conversion from microseconds of timing to distance between aircraft and satellite uses the speed of light and the two-way path, about 150 m for one microsecond.

`validation.json` lists the 27 reconciliations the compiler performs before writing anything. Among them: each outcome follows from its two residuals and the 43 µs half-width; each residual equals the recorded timing minus the predicted timing in the predictions table; the counts reproduce the published summary and group table; the join to the 90 terminal-response flights, made here from the Atlas's own copy of the terminal tables, reproduces the published join; and the hashes of the predictions and of the record that fixes them are the ones the comparison names.

## The ground-station log

The section of `check2241.html` on the ground-station log is compiled from the log cross-check: the 17 single units of the project's table found in the log with equal values and its two voice-call entries reproduced as means of 51 and 29 units; the 20 µs step in which the log reports timing; descriptive dispersions of selected log records; the residuals at each time divided by one of those dispersions; and the count of flights within the unchanged band when a hypothetical offset is added to the recorded timing. The compiler recomputes that last table from the result rows and requires it to equal the copied one. The log itself is not copied here; the tables hold recorded values and results only.

How these numbers are to be read was corrected on 18 November 2026 after Codex's follow-up review, and the copy of the cross-check findings here is the corrected one. The reporting step is the resolution of a reported estimate and does not bound the true timing or add an allowance to the criterion. The dispersions are descriptive and are not a calibrated error of the measurement in flight. The offsets are hypothetical and are not other readings the log could have given. The 0.03 to 4.20 µs is the excess beyond the 43 µs boundary; the whole residuals of those 51 flights are 43.03 to 47.20 µs in magnitude. No number in the tables changed.

## A description that is not in the source findings

The page states how far from the edge of the band the two outcomes lie: the smallest, median and largest distance outside, and how many flights lie within 1 µs and within 5 µs of the edge. Those two round distances were chosen here to describe the table. They set no outcome and are not criteria of the check.

## Meaning and limits

A withheld-measurement consistency check with disclosed prior exposure. The measurement entered no fit or selection of these flights, but it is public, earlier experiments used it, and the model loads it at start-up. Each flight already matches the timing at 21:41 and 00:11, so the check is an interpolation along a fitted leg. Counts are counts of related model flights, not probabilities. A flight outside the band is not shown to be impossible, and a flight inside it is not confirmed. No position follows from the result.
