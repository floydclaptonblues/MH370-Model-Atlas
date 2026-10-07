# CODEX TASK: Three follow-ups to the debris drift diagnostics (v2)

Author: Claude (direction). Executor: Codex. Requester: Ryan ("OPTIONS 1, 2 & 3").
Work inside `diagnostics_v2/` as new task folders `task_7_recovery_delay/`, `task_8_leeway_audit/`, `task_9_null_seeds/`. Do not overwrite or modify any existing output, config, forcing, mask, class table, coordinate table or code. Reuse them read-only. Append to `RUN_MANIFEST.json` / `PROTOCOL.json` as new entries only.

## Standing rules (all three tasks)
- No parameter is chosen, tuned, ranked or filtered by agreement with the 7th arc or any flight path. Arc agreement may be REPORTED after the fact, never used as a selector.
- All physical parameters stay as frozen: RK4 1.5 h, K = 10 m2/s, 12:00 UTC convention with BOUNDARY_HOLD, GLORYS12V1 0.494 m currents, NCEP/NCAR daily winds, static NaN land mask, 1.2% Stokes proxy as floor (never additive), offshore launch rule N = 2 unless stated, absorbing coasts, existing class table and item-to-class assignments, existing coordinates (`ASSUMED_GEOCODE`).
- Fixed seeds recorded in the manifest. Code hash, input hashes, and runtime recorded.
- Outputs: CSV + PNG + short Markdown. No Excel formats. Every number in a report must trace to a CSV.
- Every task ends with `AUDIT.md` additions: assumptions, which outputs depend on them, and an appendix of failed or rejected hypotheses.
- If any item cannot be run as specified, say so and list it; do not substitute.

## Task 7. Beaching-to-discovery delay scenarios (reuse completed forward trajectories)
Question: do stated recovery delays reconcile forward arrival timing at Reunion, Mauritius, Madagascar, Mozambique, South Africa and Tanzania with the actual find dates, without changing any drift physics?
1. Use the existing forward trajectories and per-particle landing times (`arrival_particles.csv`, task 5/6 outputs). Do not rerun physics. If landing time per particle is not stored, report that and rerun forward launches with identical seeds and parameters only to record it, flagging the rerun.
2. Define delay scenarios as stated, fixed in advance and listed in `PROTOCOL.json` before computing: D0 = 0 d; fixed 30, 90, 180, 365 d; U(0, 60 d); U(0, 365 d); exponential mean 90 d and 180 d. Define the discovery time = landing time + delay. No refloat, no coastal re-drift (state this as a limitation: retention and refloat are NOT modeled here).
3. For every arc point x setting (existing 25 points, existing leeway settings), compute for each region: fraction of arrivals whose discovery time falls within the item's observed find-date window (use the MOT date interval per item, plus +/- 30 d and +/- 90 d tolerance bands), median and 5-95% range of (discovery time minus observed find date), and the share of arrivals EARLIER than the find (for which a delay can help) versus LATER (for which no delay can help).
4. Report the key structural result separately: for each setting and region, the fraction of arrivals that are already later than the find date at zero delay. A delay can only shift arrivals later, so this fraction is a hard ceiling that no delay scenario can fix.
5. Re-score the existing arc-point ranking under each delay scenario, same Jeffreys pseudocounts and normalization, and report rank changes and score spread. Report only. Do not select a scenario.
6. Outputs: `delay_scenarios.csv`, `delay_region_timing.csv`, `delay_ceiling.csv`, `delay_rescored_rankings.csv`, PNG of timing distributions per region (zero delay vs scenarios, find window shaded), `REPORT_7.md` (one page).

## Task 8. Measured-leeway evidence audit (literature, no fitting)
Question: what measured leeway or windage evidence exists for debris like MH370 parts, and is the assumed class table consistent with it?
1. Use WebSearch/WebFetch only on publicly reachable sources. Catalogue, with full citation and URL, every source you can find on: flaperon windage/leeway (Trinanes/NOAA, Fu et al. 2018, Durgadoo et al., Lee/Griffin/CSIRO/ATSB drift reports, Wang et al.), laboratory or field leeway for comparable flat or low-freeboard panels, and any measured Stokes or wave-drift contribution. Include aircraft-debris and generic marine-debris leeway tables (for example Allen and Plourde, Breivik et al., Nesterov, Duran et al., Ocean Surface Drift of Debris).
2. For each source record: object type, freeboard/draft, measured or modeled, slip percentage and uncertainty, divergence angle and sign convention, wind height reference (10 m vs other), whether Stokes is included, and the quality of evidence (direct measurement, model fit, assumption). Mark each field `NOT_STATED` rather than guessing.
3. Convert every value to the model convention (total slip as % of 10 m wind, including Stokes) ONLY where the source supports the conversion; list any conversion assumption explicitly. Do not convert silently.
4. Compare the assumed classes C0 to C3 to the catalogue: for each class, which sources support, contradict, or say nothing. State whether windage plus a plausible Stokes component is consistent with a roughly 2% total, and what range the evidence allows.
5. Hard rule: do not recommend, select or update any class parameter for improved arc agreement. If the evidence suggests a class is unsupported, say that and give the evidence-based range; leave the table unchanged.
6. Outputs: `leeway_evidence.csv` (one row per source value), `leeway_class_support.csv`, `REPORT_8.md` with a short "what Ryan must confirm" list, and a `sources.md` list.

## Task 9. Repeat the location null tests with independent seeds
Question: is the western focus of the combined reverse density (near 35.25 S, 55.75 E) a property of the finds, or of the method plus survivor conditioning?
1. Re-run the two null tests (shuffled-region assignment and random-coast) with at least 30 independent seeds each (use 100 if runtime allows, document the choice). Seeds are drawn from a documented master seed, all listed in the manifest, none reused from the original single realizations.
2. Preserve every physical parameter, class assignment and offshore rule exactly. Only the null randomization changes.
3. For each seed record: combined-density peak lat/lon, peak density, mass fraction within 500 km and 1000 km of the peak, distance of the peak to the original observed peak (35.25 S, 55.75 E), distance of the peak to the arc, and survivors share at 31-34 S.
4. Summarize focus persistence: distribution (mean, SD, 5-95%, min, max) of peak location and the fraction of seeds whose peak lies within 250, 500 and 1000 km of the original observed peak. Compare to the observed-find run. Report where the observed run sits in the null distribution (rank/percentile) for peak density and mass fraction.
5. Repeat the observed-find run's own stochastic variability with independent particle seeds (same 30+ count) so the observed result has its own spread; report it beside the nulls.
6. Outputs: `null_seed_results.csv`, `null_focus_summary.csv`, `observed_seed_results.csv`, PNG of peak locations (all seeds, both nulls, observed) with the arc overlaid, PNG of the percentile position, `REPORT_9.md`.

## Final one-page report (`REPORT_FOLLOWUPS.md`)
1. What ran, and anything that did not.
2. Task 7: which regions can and cannot be reconciled by delay, with the hard ceiling table headline.
3. Task 8: evidence-supported leeway range and whether the class table is supported, unsupported, or untestable per class.
4. Task 9: how much of the western focus persists under independent seeds, with the percentile of the observed result.
5. How much the answer moved relative to the diagnostics_v2 conclusions (plainly: unchanged / weaker / stronger).
6. What Ryan must still confirm: exact find coordinates and date intervals, class assignments and measured slip/divergence, wind adequacy (ERA5 10 m winds and WAVERYS Stokes for 2014-2015), beach residence and refloat, and detection delays.
Say plainly if nothing focuses, or if the evidence cannot constrain the question.
