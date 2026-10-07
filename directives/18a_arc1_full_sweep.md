# CODEX TASK 18: the full arc-1 sweep

Authorized by Ryan. Register as the next unused DIRECTOR number and write to a new folder `run2/arc1_full_sweep_001/`, with a new suffix if occupied. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results. Copy modules before modifying adapters.

## 0. Why this task exists

TASK_029 swept two arc-1 start points, 2° apart, both centred on C120's 0.5°N. Every flight in the Average Day family — including C120 — inherits essentially that one start. The 36°S clustering that the whole satellite chapter rests on has therefore never been tested against the arc-1 locus as a whole.

The reachable segment of arc 1 is roughly 20° of latitude wide. Two points is not a sample of it.

This task sweeps arc 1 properly. **Arc-1 start position is the primary dimension of this task.** If the budget forces coarsening, every other dimension coarsens first.

The design rule from TASK_029 v2 stands unchanged: **sweep the commanded inputs and record where they land. Never choose a latitude and solve for a flight that reaches it.** Latitude is an output. There is no optimiser anywhere in this task.

Forbidden: any optimiser, solver or search; any target latitude, position, arc distance or endpoint; comparing a result with the 7th arc, a candidate position, a search area or a TASK_022 contact, including as an overlay or a sanity check; changing C120 or any frozen record; adopting any flight as a new reference; carrying anything into the drift work.

## 1. Part A — provenance of the inherited start (do this first, report before running)

Establish and report, with file, hash and line:

1. **Where C120's 19:41 start position came from.** TASK_029 recorded that longitude is "the initial observation-coordinate construction" and that the 19:41 BTO locus is maintained, with a contract in `START_LOCUS_SOURCE.md`. Determine whether the specific point 0.5°N, 93.7541°E on that locus is **derived from an observation** or **inherited by convention**. If it is a convention, say so plainly: it would mean the entire flight family, C120 included, is conditional on an unexamined choice.
2. The arc-1 locus parameterisation the model uses, and how a start point is specified along it.
3. Confirm the 19:41 BTO is not among the four scored BTOs, and state what therefore does and does not constrain the start.

Deliver `start_provenance.md`. Report this section's findings even if the sweep is later blocked on budget.

## 2. Part B — benchmark and tier selection (report before running the grid)

**TASK_029 silently executed about 1% of its specified grid. That must not recur.** Before the sweep:

1. Run one representative flight and record its wall time.
2. Multiply out each tier below and record the forecast.
3. Select the largest complete tier that fits the ceiling, and **report the tier, the benchmark and the forecast**.
4. If even the floor tier does not fit, **stop and report BLOCKED with the numbers**. Do not substitute a smaller grid.

Numerical ceiling: 240 minutes, with 30 reserved for verification and 20 for packaging, reported separately and not mislabelled as CPU time.

| Tier | arc-1 step | bearing step | Mach step | pressure pts | flights |
|---|---|---|---|---|---|
| T1 | 0.5° (41) | 5° (12) | 0.025 (13) | 9 | 57,564 |
| T2 | 0.5° (41) | 10° (6) | 0.05 (7) | 5 | 8,610 |
| T3 | 1.0° (21) | 10° (6) | 0.05 (7) | 5 | 4,410 |
| T4 | 1.0° (21) | 15° (4) | 0.08 (5) | 4 | 1,680 |
| T5 (floor) | 1.0° (21) | 18° (4) | 0.10 (4) | 3 | 1,008 |

**Arc-1 resolution never goes below 1.0° and the span never narrows.** That is the floor for this task.

## 3. Part C — the grid

**Fixed for every flight**, from C120: starting total fuel, the 15 lb APU earmark inside it, constant commanded Mach, no fuel profiling.

**Swept:**

- **Arc-1 start**: −6.0° to +14.0° latitude along the 19:41 BTO locus, at the tier's step. The locus must be maintained exactly at every point; report the maximum 19:41 BTO deviation across the grid. For orientation, the locus longitude runs 93.07°E at 6°S, peaks near 93.75°E at 0.5°N, and falls to 91.64°E at 12°N — the easternmost point of arc 1 sits almost exactly where C120 starts.
- **Initial bearing**: 140° to 195° at the tier's step.
- **Commanded Mach**: 0.55 to 0.86 at the tier's step.
- **Commanded pressure**: at full resolution, 200, 230, 260, 290, 320 hPa, plus 175 and 400 hPa as probes. TASK_029 lost 24 of 36 rows to weather and envelope refusals at 175 and 450 hPa, so the band is concentrated where cruise is actually sustainable and the probes confirm the refusals. **Record every refusal with its named limit.** Coarser tiers drop probe points first, then thin the band.
- **k**: run the whole grid at **k = 1.0 only**. TASK_029 recorded identical χ² for both k passes, so a second full pass buys nothing. Re-run the 50 lowest-χ² grid points at k = 1.024738 as a confirmation subset and report whether the ranking changes.

Record per flight: the 00:11 position; nine-term χ² and all nine squared residuals; fuel at 00:11 and 00:17; exhaustion time if it occurs; envelope or buffet violations with the limit named; aerodynamic and weather domain labels, including whether the track crossed east of the 102.4°E ERA5 clamp; and integration status.

Deliver `sweep_grid.csv`.

## 4. Part D — the incoming leg (reported, never a filter)

Use the EXTERNAL_DERIVED radar position 6.577718°N, 96.340795°E at 18:22:12Z, with its existing qualifications: derived from published MEKAR and NILAM coordinates at 10 nm past MEKAR, decimals describing the calculation not the measurement, DSTG's long-range angular-error caution attached, never a measured fix.

Per flight: great-circle distance to the start, implied minimum mean ground speed over 4,731 s, inbound direct bearing, and turn angle at 19:41. Direct distance is a lower bound on the real track, which included a turn, so implied speeds understate what was actually required.

**Do not filter, reject, weight or rank on these.** They exist so that if viable northern solutions cluster at starts needing implausible inbound speeds, that is visible rather than discovered later.

## 5. Part E — the answer

The question is whether the 36°S clustering survives a proper arc-1 sample.

- `chi2_by_start_and_latitude.csv` and a heat map: arc-1 start latitude on one axis, achieved 00:11 latitude on the other, coloured by best χ² in each bin. This is the deliverable.
- For each arc-1 start, the lowest χ² achieved and the 00:11 latitude where it occurs. If the minimum sits near 36°S for every start, say so. If some starts put it elsewhere, say where and at what χ².
- The same reporting bands as before, declared in advance and unchanged: fuel exhaustion between 00:10 and 00:25, χ² within 2.0 of C120's 8.117071. Reporting bands, not acceptance criteria; report full curves regardless.
- Whether any grid point beats C120's χ², and from which start. A flight scoring better than the frozen reference is a reportable finding, not a replacement — **do not adopt it**.
- The 19:41 BFO squared residual against arc-1 start and bearing. It is the model's largest single misfit at 2.901 and TASK_029 saw it fall to 0.031. Report whether low values coincide with viable full flights or only with later failures.

Then state plainly: does an arc-1 start other than C120's open 00:11 latitudes the family has not reached, and at what cost in χ² and fuel?

## 6. Verification and deliverables

- Reproduce C120's χ² of 8.117071226374 and its 00:11 position exactly through the sweep code path at its own parameters and start. Report the difference; if it does not reproduce, stop.
- Report the maximum 19:41 BTO deviation across all start points, confirming the locus held.
- Hash-confirm no frozen input and no TASK_021, TASK_022, TASK_026 or TASK_029 record changed; report the count.
- List every input actually opened, confirming no arc, candidate, contact or search-area file was read.
- `NOTES.md` with assumptions, the benchmark, the tier chosen and why, failed approaches, hashes, runtime, audit trail. `FINDINGS.md` with the Part E answer first and the Part A provenance second.

## 7. Stop rule

Deliver the map, then stop. No optimiser, no refit, no adopted flight, no arc comparison, no endpoint, no search recommendation, no follow-on. Write "arc-1 full sweep complete" when Parts A to E are done, with the tier achieved stated in that line. If blocked on budget, write "arc-1 sweep BLOCKED" with the benchmark and forecast, and deliver Part A regardless.

## 8. Notes from Claude (not instructions)

- Ryan's point, which I accept: testing one arc-1 point makes the multi-domain structure decorative. Every conclusion in the satellite chapter is conditional on that start until this runs.
- My expectation is that the ring-expansion constraint is largely start-independent, because the four BTO radii are fixed in time whatever the start. But a straight commanded path from a different start traces a different radial profile through those times, and I cannot settle that by argument. I have been wrong four times today on this kind of intuition — bearing, Mach floor, fuel binding, and arc-1 coverage — so treat my expectation as worth nothing against the grid.
- The span bound is mine, from kinematic reachability at or below Mmo. Points beyond it are retained and flagged by the incoming-leg diagnostic rather than excluded.
- A northern endpoint reachable only by a path with turns after 19:41, step climbs or a speed schedule still will not appear here. That remains outside the commanded-flight family as implemented, and the findings must say so.
