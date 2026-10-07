# CODEX TASK 12: B1 exploratory calibration-only bias fit (drift)

Authorized by Ryan. Register as the next unused DIRECTOR number and write to a new folder `task_12_B1_calibration_fit/` beside the Task 11 outputs. Preserve all historical code, inputs and outputs. Frozen B0 physics is the reference and is not edited.

## 0. Status of this fit (label it on every output)

- EXPLORATORY and POST-HOC with respect to the holdout split. The Task 11 holdout results have been seen, so the holdout can confirm non-degradation only. It is not independent evidence that a fix works.
- The original preregistered B1 trigger was false and stays false. This is a new, separately registered exploratory fit.
- No MH370 find, find coordinate, find date, 7th-arc distance or flight path is used anywhere in this task: not as a fit target, a selection criterion, a stopping rule or a plot overlay.
- Use only the existing NOAA GDP drifter corpus, its fixed calibration / validation / holdout split, and C0 undrogued as the primary subset. Drogued drifters are not used to judge slip.

## 1. Step A: diagnose the shape of the error (calibration split only, no model re-run)

Use the saved per-window model and observed displacements from Task 11 Step E. If a needed per-window table was not saved, rebuild it from the existing hindcast code without changing any setting, and report that.

For horizons 30, 60, 90 and 180 d, C0 undrogued, calibration split only:

1. Regress observed displacement on model displacement, zonal and meridional separately: obs = a + b * model. Report a, b and 95% intervals from a block bootstrap by drifter ID (1,000 resamples, seed recorded). Windows from one drifter are one block.
2. Regress the model-minus-observed error on (i) observed displacement, (ii) the model displacement, (iii) the mean daily 10 m wind along the track in the window (zonal and meridional), (iv) mean model current along the track. Report slope, intercept and R^2 with the same bootstrap.
3. Repeat 1 and 2 by starting region (40-55E, 55-80E, 80-100E) and by observed direction (westward, eastward, other). Report sample sizes (windows and distinct drifters). Cells with fewer than 30 distinct drifters are shown and labelled UNDERPOWERED.
4. Interpretation table, written as findings and not as a decision: does the error look like (a) a constant additive offset (intercept nonzero, slope near 1), (b) a speed scale (slope away from 1, intercept near 0), (c) a wind-response error (error tracks along-track wind), or (d) none of these clearly. Say which are not distinguishable.

Stop and report here if Step A shows none of (a), (b) or (c) is supported by the calibration data. Do not run Step B then.

## 2. Step B: registered candidate corrections, calibration fit only

Run only if Step A supports at least one candidate. Registered candidates (no others, no combinations unless Step A supports both):

- M1 current scale: multiply the GLORYS 0.494 m current by s, with s in [0.8, 1.6].
- M2 wind slip: replace the 1.2% floor by a slip fraction f of daily 10 m wind, f in [0.4%, 3.0%].
- M3 additive drift: a constant vector (u0, v0), |u0|, |v0| <= 3 cm/s.

Fitting rules:

- Fit each candidate on the CALIBRATION split only, by minimizing the median absolute zonal plus meridional endpoint error at 90 and 180 d, equal weights. Use a coarse grid of 7 values per parameter, then one local refinement. Record every evaluated value.
- Use blocks by drifter ID for any uncertainty, and report the fitted value, the objective curve and a bootstrap interval.
- Keep every other setting frozen (RK4 1.5 h, K = 10 m^2/s, noon hold, absorbing mask, NCEP wind, no explicit Stokes, ASSUMED_GEOCODE).
- Do not tune any candidate on the validation or holdout split, on region-specific subsets chosen after seeing results, or on drogued drifters.

## 3. Step C: gates, set before any validation run

A candidate passes only if ALL of these hold on the VALIDATION split, evaluated once per candidate:

1. The absolute median zonal error at 90 d and 180 d falls by at least 50% relative to frozen B0, in the 55-100E starting region and overall.
2. Skill versus persistence at 1, 3, 7 and 14 d does not drop by more than 0.02.
3. The absolute median meridional error at 90 and 180 d does not increase by more than 10% (relative to frozen B0).
4. The fitted parameter is not at a bound.

Then run the HOLDOUT once for passing candidates only, label it confirmation-of-non-degradation (seen split), and apply gates 2 and 3 only. Do not use the holdout to choose between candidates or to change a gate.

If no candidate passes, report that as the result. Do not add candidates, relax gates or refit on validation.

## 4. Step D: forward grid, only if a candidate passed Step C

Re-run the box B, W and M forward grids at the unchanged release setup (100 / 25 / 25 particles per cell per class, classes C0 to C3, release 8 Mar 2014 00:19, stage 2 horizon) with the single selected correction. If two candidates pass, run both and report both. Then repeat the Task 11 follow-up diagnostics unchanged: distinct-window common-source counts, the 1,000-shuffle null, delays 0 / 30 / 90 / 180 d and the Reunion before / inside / after table. Report B-versus-W-versus-M differences with the same caveats. Add the sampled-cell and particle-count information next to every maximum. Do not choose a source cell or box, and do not compare any result with the 7th arc as a criterion.

If Step C failed, do not run Step D.

## 5. Deliverables (CSV and PNG; no Excel formats)

- `stepA_regressions.csv`, `stepA_error_shape.csv`, plots of error versus observed displacement and versus along-track wind (PNG).
- `stepB_candidate_fits.csv` with every evaluated parameter value, `stepC_gates.csv` with pass / fail per gate and split.
- If Step D ran: the same file set as the Task 11 follow-up for the corrected model.
- `NOTES.md`: assumptions, failed or unsupported hypotheses and why, audit trail linking each decision to its domain, runtime, seeds, file hashes.

## 6. Stop rule

Deliver the finite experiment and stop. No other correction form, no refits after validation, no holdout tuning, no calibration of the model toward the finds or the arc, no automatic follow-on. Write "bounded B1 experiment complete" when Steps A to C (and D if triggered) are done, whether positive or negative. If Step A stops it, say so plainly.

## 7. Reading notes from Claude (not instructions)

- The Task 11 hindcast shows positive eastward error in all directions and regions at 180 d, which looks more like an offset or wind-response issue than a pure current-speed scale. Step A checks that before any fit.
- The gate numbers in section 3 (50%, 0.02, 10%) are registered now and are not tuned to any outcome.
- A correction that passes does not show that the model is right for the debris. It shows only that the drifter hindcast bias is reduced without damaging the short-horizon skill. Drifters are not flaperon proxies, and class slip stays an assumption.
