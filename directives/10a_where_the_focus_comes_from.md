# CODEX TASK 10: where does the western focus come from? (no new 90-seed batch)

Author: Claude (direction). Executor: Codex. Requester: Ryan.
Context: Task 9 finished. All 90 runs completed; the broad western focus (about 35 S, 55-58 E) persists in the shuffled-region and random-coast nulls. The observed seeds are more spread and sit about 2.5 deg east of the shuffled mean. The cause is not isolated. This task isolates it. Work in `diagnostics_v2/task_10_focus_origin/`. Do not modify any existing output, config, forcing, mask, class table, coordinate table or code. Reuse them read-only.

## Standing rules
- Frozen physics unchanged: RK4 1.5 h, K = 10 m2/s, noon BOUNDARY_HOLD, GLORYS12V1 0.494 m currents, daily NCEP winds, static NaN land mask, explicit Stokes null, assigned classes, ASSUMED_GEOCODE, N2 offshore rule, absorbing coasts.
- No parameter, seed or filter is chosen by agreement with the 7th arc or any flight path. Arc distance is reported after the fact only.
- **Arc distance must use the full 7th-arc ring, not the arc file.** The file stops at 64.46 E. Its 200 vertices fit a circle about the satellite with centre 0.5327 N, 64.3347 E, angular radius 44.4701 deg (RMS 0.009 deg). Compute great-circle angular distance from the centre and report (radius minus distance) x 111.19 km, positive inside the ring. Recompute every earlier arc-based column the same way (`peak_arc_distance_km`, `score_mass_within300km_arc`) and state that the earlier values used the truncated arc. Task 9 peaks are 726 to 1,059 km inside the ring against 1,003 to 1,433 km reported.
- Fixed seeds from a documented master seed, recorded. Code hash, input hashes and runtime recorded.
- CSV + PNG + Markdown only. Every number in a report traces to a CSV. Each step ends with AUDIT additions: assumptions, what depends on them, failed or rejected hypotheses.
- If a step cannot run as specified, say so and list it. Do not substitute. Do not "restore" lost particles by plotting last positions as endpoints at the target date.

## Step A. Scope of the nulls (read the code, no run)
From `run_null_seeds.py` and the registered plan, write `null_scope.csv` and a short table in the report:
- For each experiment (observed, shuffled_regions, random_coast): exactly what is randomized (coordinates, region labels, dates, classes, weights), what is held fixed, what pool the random coasts are drawn from, and whether the pooled particle mixture can differ from the observed one at all.
- Whether any null preserves the receiving geography (western Indian Ocean coast) that could itself produce a shared upstream region.
- State plainly if the shuffled null cannot change the pooled mixture by construction.

## Step B. Input propagation and zero-motion test
1. For one run of each experiment, dump the resolved launch table actually passed to the integrator: item, class, launch lat/lon after N2 snapping, launch date, particle count, weight, cache identity. Diff observed against each null. Confirm the intended differences are present.
2. Zero-motion test: same launch tables, transport and diffusion disabled (U = 0, K = 0, no wind), 0 steps. Output density must reproduce each launch distribution. Report `zero_motion_check.csv` with max difference per run. This separates input, caching and plotting problems from transport.

## Step C. Attrition and hold ledger (the missing 59%)
Existing baseline ensembles already give the split: of 64,000 particles in `ensemble_summary.csv`, 17,894 survive, 35,958 end on land, 10,120 leave the domain, 28 have invalid forcing. Extend this per particle for the Task 9 configuration (assigned classes), one representative run per experiment plus the original N2 run:
1. Per particle record: item, class, launch site, termination reason (survived, absorbed at coast, left domain, invalid forcing, other), model day of termination, last position, and whether it ever entered a BOUNDARY_HOLD interval (the held windows are 8 Mar 2014 00:19 to noon and 31 Aug 2018 noon to 1 Sep 00:00) and for how many steps.
2. `attrition_ledger.csv` grouped by site, class and termination reason, with counts and shares.
3. Trace the contributors to the western peak (cells within 500 km of each run's peak): split by class, launch region, termination state and hold history. Report whether they are one class, one region or a distinctive retained subset.
4. Denominators. State whether the combined map pools all survivors or normalizes each item first (Codex used "region-balanced density smoothing"; spell out the weights). Recompute the peak location and concentration with (a) survivors only, (b) mass measured against the original 16,000-particle ensemble denominator, (c) each item normalized separately, (d) pooled. Report whether the peak moves.
5. Report that the held-boundary window affects only about the last 12 h of the reverse integration, and quantify the fraction of western-peak contributors that entered it. The earlier boundary test (`boundary_regional_summary.json`) found a mean Eulerian difference of 1.7 km, max 8.3 km, across the main region.

## Step D. When do the groups become similar? (checkpoints)
Re-run one observed, one shuffled and one random-coast replicate (same registered seeds as replicates 1 of each) saving all particle positions at backward-time checkpoints: 0, 30, 60, 90, 120, 180, 240, 360, 480 and the end (about 508 days or each item's own span). Compute the density at each checkpoint on a fixed 0.5 deg grid. Report, per checkpoint: survivor count, peak lat/lon, mass within 500 km of the final peak, and the maximum and mean absolute difference between observed and each null surfaces. Use fixed plotting scales. The question: at what interval does the calculation stop preserving differences between the find patterns? Subtracted surfaces are diagnostic, not calibrated source maps. Plot as PNG.

## Step E. Known-origin synthetic recovery (the resolving-power test)
1. Choose 5 well-separated forward release sites in advance, written to `PROTOCOL.json` before running. Use sites unrelated to the 7th arc and not tuned: for example 40 S 60 E, 35 S 80 E, 30 S 100 E, 25 S 70 E, 20 S 90 E.
2. Forward-release particles from each site at the same date as the event (8 Mar 2014 00:19), same physics, same leeway classes (one run per class), same wind, and record arrivals at the real coast cells within the real find windows (use the existing item windows and coastlines). From each, build a synthetic observation set with the same item count, class assignment, coordinate uncertainty (100 km nominal) and recovery timing assumptions as the real analysis.
3. Feed each synthetic set, without the origin, through the identical reverse procedure and density construction. Report where the combined density peaks, the mass within 500 and 1000 km of the true site, and whether the hotspot differs between sites.
4. If distinct, informative synthetic cases all return the same western hotspot, say plainly that the procedure lacks the resolving power for an origin interpretation. If some sets cannot arrive at all, report the count and do not substitute.
5. Add a forward check on the western region: compare the fraction of releases from the western focus region that reproduce the actual collection of observations (timing and region at the declared assumptions) with releases from other sites. Report as a ranking by site, not as a selection.

## Outputs
`null_scope.csv`, `zero_motion_check.csv`, `attrition_ledger.csv`, `peak_contributors.csv`, `denominator_variants.csv`, `checkpoint_divergence.csv`, `checkpoint_divergence.png`, `synthetic_recovery.csv`, `synthetic_recovery.png`, `ring_distance_recomputed.csv`, `REPORT_10.md` (one page), updated `AUDIT.md`, manifest with seeds, hashes and versions.

## Report back (one page)
What ran. Whether the shuffled null can change the mixture. Whether launch tables differ as intended and the zero-motion check passes. Where the 59% goes and who contributes to the western peak. Whether the peak moves under the denominator variants. The interval at which observed and null densities converge. Whether synthetic origins are distinguishable. Say plainly if the focus appears at initialization (inspect geocoding, snapping, weighting), near a forcing boundary (inspect hold), or gradually as particles disappear (inspect transport and attrition together). Keep the conclusion DIAGNOSTIC / CONDITIONAL. Do not move the aircraft reconstruction to accommodate any result. List what Ryan must still confirm: find coordinates and date intervals, class assignments and measured slip/divergence, wind and Stokes adequacy (ERA5/WAVERYS), beach residence and refloat, detection delays, and the discovery-time versus first-beaching-time assumption.
