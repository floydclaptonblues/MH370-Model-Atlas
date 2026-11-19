# Stage A acceptance and the completed Stage B comparison, as received and published

Received from Ryan Hall on 18 November 2026 (22:22 America/Chicago) as `MH370_2241_Stage_B_Results_9a67641.zip`, SHA-256 `6271fbfaf94c8487d0847d833e1cb6edfbfd9aaa6862ccf1c9c9e8df1bb00c97`. Every file listed in the packet's `SHA256SUMS` verified. Codex's result message had arrived at 21:49 without the packet. Not part of the package revision.

**Authorship.** Codex accepted Stage A, issued the Stage B release and ran the comparison, in its own environment, before any of this was in the repository. The reports, tables and programs in this directory are Codex's, unchanged. I did not perform the original comparison. What I did is listed below.

**This directory** is the packet as received, without eleven files whose identical bytes the repository already holds (`OMITTED_DUPLICATES.json` names each, with its hash and where it is), plus this note.

## Decisions in the packet

- Stage A is accepted at `9a67641173e878d04a07cb2da4c104095110fb91`: the 532 original prediction files, the journal, the account and the four fixed exports.
- Stage B is released for package revision `91266581e659` and seal `76b296438732738fd330b510ab2d27a9df98ebb48a78bca1df815201d871de1c`, and is complete.

## Result (Codex's; `STAGE_B_FINDINGS.md`)

Recorded at 22:41:22 UTC: burst timing offset 14,540 µs, burst frequency offset 204 Hz (event `T6_224122` of the pinned table).

| | Histories |
|---|---:|
| Meet the ±43 µs timing band | 215 of 266 |
| Outside the band | 51 of 266 |
| Label depends on the integration step | 0 |
| Without a label | 0 |
| Within the separate ±7 Hz centred-frequency diagnostic | 266 of 266 |
| Parent flights of the terminal-response catalogue that meet the timing | 90 of 90 |

All 51 are among the 74 sampled histories that enter at Mach 0.67 and climb to about 30,053 ft pressure altitude; 23 of those 74 meet the band. The other nine combinations hold 192 histories, and all meet it.

## What was done here

1. The package reports revision `91266581e659`. The seal and predictions have the hashes in `FINAL_DECISION.json`. The packet's copies of `stage_b.py`, the population, the protocol and the four fixed exports equal this repository's files byte for byte, and its event table equals the pinned table in this container.
2. `RELEASE_STAGE_B.json` (SHA-256 `5910113de0335cd263711b9ec84b7a8364b0102f40b7df15468e45917d3ffea2`) was placed beside `stage_b.py`. None existed before.
3. The three result files were copied, byte for byte, to `../STAGE_B_OUTPUT_91266581e659/`.
4. The arithmetic was repeated in this container: the frozen program on this repository's own files, then the packet's independent program, reconciliation and terminal-parent join. Every output equals the packet's (`../STAGE_B_OUTPUT_91266581e659/LOCAL_REPRODUCTION.json`). This is a repetition of arithmetic on stored predictions, not an independent confirmation, and no flight or prediction was computed. `check_2241.py` was not run; Stage A stays closed.
5. Two entries were added to `../EXPOSURE_LOG.jsonl`: Codex's comparison, and the repetition here. The five earlier entries are unchanged.

## How far the two labels lie apart

These numbers are read from Codex's result table. They add no criterion and change no label.

- Every one of the 51 histories outside the band is outside it on the same side and by little: by 0.03 to 4.20 µs, with a median of 1.87 µs. The predicted timing is higher than the recorded one in all 51.
- Of the 215 that meet the band, 15 lie within 4.2 µs of that same edge, 8 of them within 1 µs.
- All 266 are within ±86 µs.

So the edge of the band passes through one cluster of 66 histories, and what separates the two labels within that cluster is a few microseconds. The labels are numerically firm: the two integration steps differ by at most 0.00033 µs, and no label depends on the step. That firmness is a property of the arithmetic. The recorded timing is quantised and noisy at the level of tens of microseconds, and the model's inputs (satellite ephemeris, calibration, winds, the stored commands) are not known to a few microseconds either.

**What follows for wording.** "Outside the band" is the result of applying, consistently and as fixed beforehand, the same 43 µs criterion that accepted these histories at the earlier times. It is correct to say that 51 histories do not meet that criterion at 22:41 and to identify them whenever agreement with all checked measurements is discussed. It is not correct to say that the check shows those 51 histories to be impossible, or the 215 to be confirmed. A history 0.03 µs outside the band and one 0.1 µs inside it are not distinguished by this measurement in any physical sense.

## Limits that stay attached to the result

- A withheld-measurement consistency check with disclosed prior exposure, along a leg already fitted at 21:41 and 00:11. It is not a blind test.
- Counts are counts of related model histories, not probabilities and not independent confirmations. Histories of one group and level have nearly the same predicted timing.
- All 90 terminal parents meeting the 22:41 timing says nothing new about the 12,420 terminal responses, whose classifications against the final transmissions stand as they were, with the one permanent provenance exception.
- A model state in the air at 22:41 or at 00:19 is not an impact location.
- No flight was computed for Stage B, and none was recomputed.
