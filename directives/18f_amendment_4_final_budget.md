# CODEX TASK 18 — AMENDMENT 4: final budget, and a fallback so this does not block again

Parts A to E and Amendments 1 to 3 stand, except where changed below. Part A, the mesh gate and the overhead diagnostic are complete and are not rerun. dt 15 s is retained for screening.

My branch threshold in Amendment 3 was badly set and sent you to branch B over a 25.4% figure that is worth 224 minutes across the grid. That is corrected here.

## 1. Ceiling

**840 minutes** numerical, with 40 reserved for verification and 20 for packaging, reported separately.

## 2. Amortise the setup (this supersedes the branch B instruction)

Setup is 13.34 s per flight and grid-invariant. Over 1,008 flights that is about 224 minutes of repeated identical work. Build a batched runner **in a copied module**, leaving the original untouched, performing setup once and looping the grid in one process.

Verification before it is used for anything:

- reproduce C120's χ² of 8.117071226374 and its 00:11 position exactly through the batched path;
- confirm five grid points spread across the arc-1 span match single-flight runs to floating-point noise.

Report the largest deviation. **If either check fails, abandon the batch and go to the fallback ladder in section 4.**

Do not attempt to optimise the 34.93 s of command-dependent force calculation. That is genuine physics, it differs per flight, and it is not to be approximated, cached or interpolated.

## 3. Drop the k-confirmation subset

The 50-flight re-run at k = 1.024738 is withdrawn. TASK_029 recorded identical χ² across both k passes, so it buys nothing for about 33 minutes. Run the grid at **k = 1.0 only** and state in `FINDINGS.md` that the k invariance is carried from TASK_029 rather than re-measured here.

## 4. Fallback ladder — pre-authorised, no further approval needed

Select the first rung that fits 840 minutes and report which one you ran:

| Rung | Grid | Flights |
|---|---|---|
| R1 | T5 as specified: arc-1 21 × bearing 4 × Mach 4 × pressure 3 | 1,008 |
| R2 | pressure cut to 2 points: arc-1 21 × bearing 4 × Mach 4 × pressure 2 | 672 |
| R3 | Mach cut to 3: arc-1 21 × bearing 4 × Mach 3 × pressure 2 | 504 |

**Arc-1 stays at 21 points across the full −6° to +14° span on every rung.** That is the dimension this task exists to sample and it is never cut. If a rung below R1 is used, say in `FINDINGS.md` which coverage was sacrificed and why.

If even R3 does not fit, report BLOCKED with the numbers — but at 39.28 s batched, R3 is about 330 minutes, so it should not come to that.

## 5. Unchanged

No optimiser; latitude is an output. No arc, candidate, contact or search-area comparison. Incoming-leg figures reported, never used to filter. C120 frozen and not replaced by any flight scoring better. Nothing crosses into the drift branch. Reported cruise profiles re-run at dt 7.5 s; screening rows labelled `mesh=15s`. Every refusal recorded with its named limit.

## 6. Note from Claude (not an instruction)

Correcting the record: I inferred a 30 s fixed overhead from two benchmarks that were both at dt 15 s, so the difference between them measured nothing. The diagnostic was right to contradict it. That is the sixth wrong expectation of mine today against a measurement, and the reason this amendment carries a pre-authorised ladder instead of another threshold for me to set wrongly.
