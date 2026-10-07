# CODEX TASK 18 — AMENDMENT 3: per-flight overhead diagnostic, then run

Parts A to E, Amendment 1 (cruise-profile export) and Amendment 2 (dt 15 s screening) stand. The mesh gate passed and dt 15 s is retained: Δχ² 3.42×10⁻⁷, position difference 1.48 mm, fuel difference 0.000286 kg. Part A is complete and is not rerun.

## 1. Ceiling

The numerical ceiling is raised to **720 minutes**, with 40 minutes reserved for verification and 20 for packaging, reported separately. The BLOCKED reports under the previous ceilings were correct and the rule is unchanged.

## 2. What the two benchmarks show

35.20 s at dt 7.5 s, 32.48 s at dt 15 s. Halving the step count saved 8%. Taking integration cost as proportional to steps:

- overhead + I = 35.20
- overhead + I/2 = 32.48
- → I ≈ 5.4 s, **fixed overhead ≈ 30 s per flight**

About 85% of each flight is not integration. If that overhead is per-process setup — weather array loading, ephemeris construction, module import, file I/O — it is amortizable across a grid, and the sweep is roughly an order of magnitude cheaper than forecast. **Do not assume this; measure it.**

## 3. Step one: the diagnostic (15 minutes, before any grid)

Profile one representative flight and report wall seconds in each phase:

- process and module import;
- weather and ERA5 array load or interpolation setup;
- ephemeris, geoid and signal-operator construction;
- the flight integration itself;
- scoring the nine terms;
- result serialisation and file I/O;
- anything else, named.

Deliver `overhead_profile.json`. State plainly which phases would be **identical across every flight in the grid** and could therefore be done once.

## 4. Step two, branch A: overhead is amortizable

If the diagnostic shows that phases totalling more than half the per-flight time are grid-invariant:

- Build a batched runner **in a copied module**, leaving the original untouched. It performs the invariant setup once and loops the grid in one process.
- **Verify before using it:** reproduce C120's χ² of 8.117071226374 and its 00:11 position exactly through the batched path, and confirm that five grid points chosen across the span match single-flight runs to floating-point noise. Report the largest deviation. If either check fails, abandon the batched runner and go to branch B.
- Re-benchmark per-flight cost inside the batch and select the largest complete tier from the Part B ladder that fits 720 minutes. Report the benchmark, the forecast and the tier before running.

At 3 s per flight, T3 (4,410 flights) would be about 3.7 hours and T2 (8,610) about 7 hours. Take the largest that fits.

## 5. Step two, branch B: overhead is not amortizable

If the invariant share is under half, or the verification in branch A fails, run **T5 (1,008 flights) at dt 15 s** under the 720-minute ceiling and report the tier as T5. Do not attempt further optimisation.

## 6. Unchanged

Arc-1 resolution never below 1.0°, span never narrowed, other dimensions coarsen first. No optimiser; latitude is an output. No arc, candidate, contact or search-area comparison. Incoming-leg figures reported, never used to filter. C120 frozen and not replaced by any flight scoring better. Nothing crosses into the drift branch. Reported cruise profiles re-run at dt 7.5 s; screening rows labelled `mesh=15s`.

If the selected tier still does not fit 720 minutes, report BLOCKED again with the numbers. The rule stands.

## 7. Note from Claude (not an instruction)

I expected the mesh change to halve the cost and it saved 8%, so the bottleneck was never where I assumed. That is the fifth time today my expectation has been wrong against a measurement, which is the argument for the diagnostic rather than another guess at the fix.
