# The 22:41 check: result of the replacement gate, revision `91266581e659`

18 November 2026. Not part of the revision. The first gate, of revision `68895a19a580`, is reported in `GATE_FINDINGS.md` and its records are unchanged.

**The replacement gate passed: twelve of twelve checks.** It was started once, under the release in Codex's repair packet (SHA-256 `7d728bf2…04264991`), at commit `bfa2915`, and ran to its end in one process without interruption.

**Why there is a second gate.** Revision `91266581e659` is the first revision with one change, written by Codex and applied here unchanged: an attempt whose half-step flight is not usable now has its dependencies checked before it closes. A gate qualifies the code it ran, so the changed revision needed its own. The eleven control flights, the two integration steps, the twelve checks, the numerical limits and the 1,200 s allowance are the same.

**What it is, and is not.** As before: eleven of the 266 accepted cruise flights were flown again from their stored commands at 15 s and at 7.5 s to 00:11:00 UTC, and the adapter was applied at 21:41:27 and 00:11:00 only. Nothing was evaluated at 22:41:22. No recorded 22:41 value was read, no residual was formed and no comparison was made.

## Result

| # | Check | Result |
|---|---|---|
| 1 | First start of the gate for this revision; no earlier record in its run directory | Pass |
| 2 | Every file of the revision present | Pass |
| 3 | Population file equal to a fresh build | Pass |
| 4 | Eleven control flights by the fixed rule | Pass |
| 5 | Cruise revision `2a016b1294fa` unchanged; engine carries the declared epochs, boundary, guard and constants | Pass |
| 6 | Every compared field of each native record equal at the unchanged step | Pass, 11 of 11 |
| 7 | Adapter equal to the stored values at 21:41:27 and 00:11:00, both steps | Pass, 22 of 22 |
| 8 | Half step against full step at those epochs within 0.1 µs and 0.01 Hz | Pass: largest 0.00096 µs and 0.0000031 Hz |
| 9 | No evaluation at 22:41 | Pass: adapter calls at index 3: timing 0, frequency 0; guard requests 0; target evaluations in the records 0 |
| 10 | No frozen file changed; nothing loaded or read outside the frozen lists | Pass: nothing listed |
| 11 | Charges within 1,200 s | Pass: 355.8 s |
| 12 | No review requirement and no gate attempt open at the end | Pass |

## Comparison with the first gate

For all eleven control flights, the recorded differences from the native record at the three open epochs, at both steps, are identical in every digit to those of the first gate. That is what a deterministic replay on the same machine and numerical runtime should give, and it is the only sense in which the two gates agree: the second is a repetition by the same code path, not an independent confirmation. The largest half-step differences are therefore the same: 0.00096 µs in timing and 0.0000031 Hz in frequency, at 00:11:00, flight `A003_TO300.F1`; the largest in fuel, +0.172 kg at 20:41:05, flight `A004_TO275.F1`, with no declared limit and no established origin. `GATE_CONTROLS_91266581e659.csv` has every flight.

No control flight closed as not usable at the half step, so the changed branch was not exercised by this gate. Its behaviour rests on the seven focused offline tests.

## Runtime and charges

| Quantity | This gate | First gate |
|---|---:|---:|
| Process wall time, engine build included | 360 s | 386 s |
| Attempts admitted / settled / interrupted / open | 22 / 22 / 0 / 0 | 22 / 22 / 0 / 0 |
| Charged to the gate allowance of its revision | 355.8 s of 1,200 s | 377.3 s of 1,200 s |
| Full-step flights (11) | 12.7 to 17.1 s; 150.7 s together | 13.2 to 18.4 s; 157.8 s |
| Half-step flights (11) | 17.5 to 20.3 s; 205.1 s together | 18.6 to 20.8 s; 219.6 s |
| Charged to Stage A | 0 s | 0 s |

Gate computation over both revisions: 733.1 s. Each revision has its own allowance; the first revision's charge stays in its own records and is reported here beside the second.

From the two gates, the 266 full-step flights would take about 3,640 to 3,820 s and the 266 half-step flights about 4,960 to 5,310 s, against ceilings of 8,000 s and 12,000 s. These are extrapolations from eleven flights. They leave out the target evaluations, which no gate makes, and Stage A's two dependency checks for each attempt where the gate makes one.

## Final state of the records

`run/91266581e659/`: 45 records (one gate start, 22 admissions, 22 settlements, all `GATE_FLIGHT_COMPLETED`). No review requirement, no stored prediction, sealing not begun. `require_gate` accepts the result as that of the one gate start in the records. The gate cannot be started again for this revision. `run/68895a19a580/` is unchanged.

`EXPOSURE_LOG.jsonl` now has two entries, one for each gate process: each imported the flight model, whose setup loads the recorded frequencies, 22:41 included. Neither printed, selected or compared such a value. As Codex's review says, this does not make 22:41 a blind or unexposed measurement; the check's name and its disclosure (PROTOCOL.md, section 3) stand.

## Deviations and limits

- None in the run: one start, one process, no interruption, no retry, no frozen file changed. The package hashes to `91266581e659`.
- The repair was not written or altered here; it was applied from Codex's packet and verified against the packet's identities.
- The inserted-defect campaign was not repeated for this revision, by Codex's decision. The 99-defect log is the first revision's.
- In the package itself, the offline tests that require no release file and no run record do not hold. The suites pass in a clean copy of the revision's files (`gate_review_and_fix_91266581e659/RECEIVED.md`).
- Stage A and Stage B are not released and were not run.
