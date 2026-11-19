# The 22:41 check: Stage A (predictions only), revision `91266581e659`

18 November 2026 (America/Chicago; the run ended at 02:13 UTC on 19 November). Not part of the revision.

**Stage A is complete and sealed.** All 266 accepted cruise flights have a usable pair of predictions at 22:41:22 UTC: one at the catalogue's 15 s integration step and one at 7.5 s, agreeing within the declared numerical limits. No flight was left without a status, none failed reproduction, and nothing stopped for review.

**What Stage A is, and is not.** Each flight was flown again from its stored commands by the frozen cruise functions and had to reproduce its native record exactly. The prediction-only adapter was then checked at 21:41:27 and 00:11:00 against the frozen measurement and applied once at 22:41:22. The result for each flight is a model state and a *predicted* burst timing offset and burst frequency offset at that time. Stage A read no recorded 22:41 value, formed no residual, made no comparison and assigned no consistency label. Whether any flight is consistent with the 22:41 measurement is not known from Stage A. That is Stage B, which is not released.

This remains a withheld-measurement consistency check with disclosed prior exposure. The three Stage A processes each imported the flight model, whose setup loads the recorded frequencies, 22:41 included (`EXPOSURE_LOG.jsonl`, five entries with the two gates). The package printed, selected and compared none of them.

## The seal

| File in `run/91266581e659/` | SHA-256 |
|---|---|
| `STAGE_A_SEAL.json` | `76b296438732738fd330b510ab2d27a9df98ebb48a78bca1df815201d871de1c` |
| `PREDICTIONS_2241_266.csv` | `2cd38ef3034d83621467146656eca711abaa89371ff052108587aaca70f572dd` |
| `JOURNAL.jsonl` | `8c158f59e12e7662c52d7323fa5749e64f6f48d48a3d2c1db31c51f1fd8b05ed` |
| `STAGE_A_REPORT.json` | `d8902891c9b6be7aa092917b4066da687b879818843cb1b80ffb93f820aa0604` |

The seal is complete, not partial. It fixes the state after 2,176 phase records. The record that sealing began (number 2,177) carries these four hashes, and the four files equal them; the completion record is number 2,178. Sealing ran in one process without interruption. Computation is closed for this revision.

## Coverage and counts

| Quantity | Value |
|---|---:|
| Identities | 266 |
| Status `PREDICTED` (both steps stored and in numerical agreement) | 266 |
| Any other status | 0 |
| Attempts: full step / half step | 266 / 266 |
| Attempts interrupted, retried, or closed without a prediction | 0 |
| Target evaluations begun / predictions stored | 532 / 532 |
| Timing calls / frequency calls at 22:41:22 | 532 / 532 |
| Requests through the cruise guard | 0 |
| Dependency findings, before or after a target evaluation | 0 |
| Review requirements | 0 |

This is the clean count the protocol states for a complete run: one full-step and one half-step target evaluation for each flight, and no more.

## Reproduction and the adapter

For all 266 flights the full-step replay equalled the native record in every compared field, with no tolerance. For all 532 flight calculations the adapter equalled the frozen measurement's stored values at 21:41:27 and 00:11:00. A flight that failed either would have closed without a target evaluation and stopped the stage; none did.

## Agreement between the two integration steps at 22:41:22

| Quantity | Largest over 266 flights | Median | Limit |
|---|---:|---:|---:|
| Predicted timing, half step minus full step | 0.00033 µs (`A084_TO250.F1`) | 0.000077 µs | 0.1 µs |
| Predicted frequency, half step minus full step | 0.0000042 Hz (`A008_TO250.F1`) | 0.00000028 Hz | 0.01 Hz |

The predictions do not depend on the integration step at any level that matters for a 43 µs criterion. This is a statement about numerical convergence of the model, not about its physical accuracy.

## The predictions, and how much they can discriminate

From the predictions alone (`STAGE_A_REPORT.json`, `expected_discrimination`):

| Quantity | Value |
|---|---:|
| Predicted timing, lowest to highest over 266 flights | 14,526.7 to 14,587.2 µs |
| Spread of predicted timing over all flights | 60.5 µs |
| Spread between the means of the eleven group-and-level combinations | 44.4 µs |
| Spread within one combination | 0.2 to 24.3 µs |
| Acceptance band of the declared criterion | half-width 43 µs, full width 86 µs |
| Predicted frequency, lowest to highest | 203.42 to 205.23 Hz (spread 1.82 Hz) |

Two things follow from these numbers and nothing else:

- The whole population spans 60.5 µs, less than the 86 µs full width of the band. A single recorded timing could therefore place all 266 flights inside the band. It could also place some inside and some outside, since the span is more than the 43 µs half-width. Stage A does not say which.
- Most of the spread is between combinations of incoming group and cruise level, not within them. Flights of one combination have nearly the same predicted timing (within 0.2 to 24.3 µs), so they will tend to share one outcome. Counts of flights in Stage B will not be counts of independent tests.

The predicted frequencies span 1.8 Hz against a ±7 Hz diagnostic band, so the frequency diagnostic is expected to discriminate little among these flights.

The model states at 22:41:22 lie between 20.5°S and 24.6°S and between 91.3°E and 94.7°E. These are conditional airborne states of the 266 model flights at that time. They are not an estimate of where the aircraft was and not a search area.

## Sessions, runtime and charges

| Session | Ended | Process time | What it did |
|---|---|---:|---|
| 1 | `PAUSED` (clean, one-hour limit) | 3,611 s | Full-step pass: 266 flights |
| 2 | `PAUSED` (clean, one-hour limit) | 3,610 s | Half-step pass: 190 flights |
| 3 | `COMPLETE` | 1,388 s | Half-step pass: the remaining 76 flights |

One process at a time; the records were committed at each pause with no process running. No container restart occurred during Stage A.

| Allowance | Charged | Limit |
|---|---:|---:|
| Stage A, full step (12.5 to 17.1 s a flight, median 13.5 s) | 3,606.5 s | 8,000 s |
| Stage A, half step (16.7 to 22.2 s a flight, median 18.7 s) | 4,991.5 s | 12,000 s |
| Gate of this revision | 355.8 s | 1,200 s |
| This revision in all | 8,953.7 s | 21,200 s |
| Gate of the earlier revision `68895a19a580`, in its own records | 377.3 s | 1,200 s |

## Deviations and limits

- None in the run: no interruption, no retry, no review requirement, no ceiling reached, no frozen file changed. The package hashes to `91266581e659`.
- Exact reproduction holds on this machine's numerical runtime (Python 3.13.18, NumPy 2.5.3, SciPy 1.18.1, x86-64). It is not a claim about another runtime.
- The adapter at 22:41:22 cannot be checked against the frozen measurement, which refuses that epoch by design. Its correctness there rests on the same statements producing the stored values at the two open epochs for every flight, and on the offline source comparison.
- The branch repaired by Codex (an unusable half-step flight with a dependency finding) was never reached: every half-step flight was usable.
- The predictions come from one model with fixed inputs: the frozen satellite ephemeris and frequency-compensation tables, one wind and temperature field, the stored commands. They carry no uncertainty of their own. The spread across flights is a spread across accepted histories, not an error bar.
- Stage B is not released. No Stage B release file exists, `stage_b.py` was not run, and no recorded 22:41 value was read.
