# Cruise level after 19:41 for all 108 accepted arrivals: findings

16 November 2026. Runner revision `2a016b1294fa` (frozen at `37199ce`). Method: `METHOD.md`, with Amendments 1 to 4. Every number below is taken from the tables in this directory; `verify_findings.py` recomputes them from those tables.

## Result

All 108 arrivals, 424 configurations and 848 one-sided searches finished. Nothing was lost, no stop rule was triggered, and every required comparison with the pilot passed.

- **An accepted flight was found for 208 configurations; the completed bounded search returned none for 216.** An accepted flight meets the three timing measurements (20:41:05, 21:41:27, 00:11:00) within 43 microseconds, is supported throughout by the performance model, and still has engine fuel at 00:11:00.
- **At each speed, accepted flights were found at only some of the tested levels.** Mach 0.67: the arrival level and 30,053 ft. Mach 0.75: 31,946 ft and 33,985 ft. Mach 0.78: 33,985 ft only. These are the tested levels with accepted flights. Levels between them, and climbs later than 19:41, were not tested, so no continuous range of altitude is established.
- **In 21 of the 22 combinations of group and level, every arrival has the same outcome as the group's pilot arrival.** In the remaining one (arrivals at 25,661 ft and Mach 0.75, climbing to 31,946 ft) 26 arrivals have an accepted flight and 4 do not. That level is marginal for that group under the tested model and search.
- **All 218 numerical checks were performed and resolved.**

A completed search that returns no flight describes that search. It does not establish that no flight exists. Counts of arrivals are counts of saved starting states; they are not probabilities, and arrivals of one group are closely related, not independent.

## What was computed

| Item | Value |
|---|---|
| Starting states | 108 accepted arrivals at 19:41:03, each with its own position, course, fuel and mass |
| Groups (arrival pressure level, speed) | 6: 365.113 hPa (25,661 ft) at Mach 0.67 and 0.75, 30 arrivals each; 331.655 hPa (27,830 ft) at Mach 0.67 and 0.75, 20 each; 300.9 hPa (29,987 ft) at Mach 0.75 and 0.78, 4 each |
| Levels | The arrival's own level (control) and climbs to 300 hPa (30,053 ft), 275 hPa (31,946 ft) and 250 hPa (33,985 ft); the 300 hPa climb is not run for the 8 arrivals already at 300.9 hPa |
| Configurations | 424 |
| Searches | 848: for each configuration, first turn 0 to 20 degrees left and, separately, 0 to 20 degrees right |
| Fuel-flow multiplier | 1.000 |
| Flights computed | 24,886 completed: 438 in the gate, 24,012 in the searches and continuations, 436 in the numerical checks. Two more were interrupted by a machine restart and repeated |
| Distinct trial flights to 00:11:00 | 16,039 |
| Measurement at 22:41 | Not evaluated. The guard counted 0 requests in all 848 search records; no stop was recorded in the checks |

Altitudes are pressure altitudes. Positions are airborne model states at the stated time, conditional on the starting state; they are not impact positions.

## Outcomes by group and level

Number of arrivals with an accepted flight, out of the arrivals in the group. Where there is none, the way the searches ended is given (left side; right side).

| Group | Control level | 30,053 ft | 31,946 ft | 33,985 ft |
|---|---|---|---|---|
| 25,661 ft, Mach 0.67 (30) | 30 | 30 | 0: lift-margin limit; lift-margin limit | 0: lift-margin limit; lift-margin limit |
| 25,661 ft, Mach 0.75 (30) | 0: fuel out before 00:11; no starting point | 0: fuel out before 00:11; no starting point | **26** (4 without) | 30 |
| 27,830 ft, Mach 0.67 (20) | 20 | 20 | 0: lift-margin limit; lift-margin limit | 0: lift-margin limit; lift-margin limit |
| 27,830 ft, Mach 0.75 (20) | 0: fuel out before 00:11; no starting point | 0: fuel out before 00:11; no starting point | 20 | 20 |
| 29,987 ft, Mach 0.75 (4) | 0: fuel out before 00:11; fuel out before 00:11 | not run | 4 | 4 |
| 29,987 ft, Mach 0.78 (4) | 0: no starting point; fuel out before 00:11 | not run | 0: no starting point; fuel out before 00:11 | 4 |

What the endings mean:

- **Lift-margin limit.** Every flight stopped where the performance model's margin to buffet onset is exhausted. This concerns the tested case only: a climb started at 19:41, at Mach 0.67 and the weight at that time, to 31,946 ft or to 33,985 ft. 200 searches ended this way (50 arrivals, two levels, two sides).
- **Fuel out before 00:11.** A first turn that meets the 20:41 timing was found, but every trial flight from it exhausted engine fuel before 00:11:00. 117 searches.
- **No starting point.** The bounded search found no first turn on that side that meets the 20:41 timing, so no full flight was attempted. The search flies five sampled first turns (0, 5, 10, 15 and 20 degrees), refines wherever neighbouring samples have 20:41 residuals of opposite sign, and otherwise accepts only a sample already inside the band; it would not see a qualifying turn lying wholly between two samples. 309 searches, 300 of them on the right side.

The accepted flights turn left at 19:41 in the four larger groups (first turn between 2.0 and 9.5 degrees left). In the two groups at 29,987 ft the first turn is small (0.4 degrees left to 1.0 degree right) and 12 right-side searches returned accepted flights.

Source: `PROD_SUMMARY_BY_GROUP_AND_LEVEL.csv`, `PROD_CONFIGURATIONS.csv`, `PROD_DIRECTIONS.csv`.

## Differences from the pilot arrivals

The pilot ran one arrival of each group (A001 to A006). Six of the 424 configurations differ from their group's pilot arrival in outcome or in how a side ended.

| Configuration | Group | Level | Difference |
|---|---|---|---|
| A030, A034, A038, A042 at 275 hPa | 25,661 ft, Mach 0.75 | 31,946 ft | No accepted flight in the completed bounded search. All four have accepted flights at 33,985 ft |
| A012 at 250 hPa | 29,987 ft, Mach 0.78 | 33,985 ft | Accepted on both sides, but the left side only with the second turn starting at an end of its searched range |
| A024 at 250 hPa | 29,987 ft, Mach 0.78 | 33,985 ft | Accepted on the right side; no starting point on the left |

Every other configuration has the pilot arrival's outcome and the same ending on each side.

## The group at 25,661 ft and Mach 0.75, climbing to 31,946 ft

### Computed outcomes

26 arrivals have an accepted flight. 4 have none in the completed bounded search. All 30 right-side searches found no starting point, so the outcome is that of the left side.

| Fuel at 19:41 (kg) | Arrivals | Outcome | Returned flights: engine fuel above the reserve at 00:11 (kg) | Returned flights: engine fuel exhausted after 00:11 (s) |
|---|---|---|---|---|
| 26,003.3 to 26,006.6 | 12 | Accepted | 23.087 to 30.001 | 15.732 to 20.422 |
| 25,983.4 to 25,984.3 | 11 | Accepted | 1.821 to 5.473 | 1.233 to 3.729 |
| 25,980.3 | 3 (A070, A074, A078) | Accepted | 1.154, 0.508, 0.101 | 0.781, 0.344, 0.068 |
| 25,976.3 to 25,976.8 | 4 (A030, A034, A038, A042) | No accepted flight | none | none |

The fuel figures are those of the returned flights. The model holds back 6.80388555 kg for the auxiliary power unit; the modelled event is engine-fuel exhaustion with that reserve still on board. Per-arrival rows: `PROD_GROUPS_WITH_MIXED_OUTCOMES.csv`.

### What the trial flights established

Counts per arrival, of distinct trial flights to 00:11:00, from the detailed flight ledger.

| Arrivals | Trial flights | With engine fuel at 00:11 | Of those, meeting all three timing bands | Out of fuel before 00:11 | Of those, meeting the 20:41 and 21:41 bands |
|---|---|---|---|---|---|
| The 26 accepted | 46 to 52 | 28 to 44 | 14 to 19 | 8 to 20 | 0 to 3 |
| A030 | 58 | 16 | 0 | 42 | 18 |
| A034 | 55 | 14 | 0 | 41 | 14 |
| A038 | 47 | 9 | 0 | 38 | 14 |
| A042 | 25 | 0 | 0 | 25 | 4 |

For the four arrivals without an accepted flight, the trial flights that meet both earlier bands are of two kinds, and neither yields an accepted flight:

- **Those that keep engine fuel to 00:11 miss the 00:11 timing by a wide margin.** There are 5, 5 and 4 of them (A030, A034, A038); their closest residuals at 00:11 are 314.756, 417.400 and 621.416 microseconds, against a 43 microsecond band. A042 has no trial flight with engine fuel at 00:11.
- **Those that run out of engine fuel before 00:11 have no timing residual at 00:11.** There are 18, 14, 14 and 4 of them (A030, A034, A038, A042), so none is established as meeting all three bands. Within this fuel-exhausted subset, the latest stops 0.0496, 0.1155, 0.0181 and 0.3597 s before 00:11:00. These times describe that subset only, not every trial flight that meets the two earlier bands.
- **The latest fuel exhaustion of any trial flight** is 0.0496, 0.0461, 0.0124 and 0.0207 s before 00:11:00. For A034, A038 and A042 that flight is a different one, which does not meet both earlier bands.

For A078, the closest accepted case, the two statements concern different flights: the returned flight exhausts engine fuel 0.068 s after 00:11:00; another trial flight, meeting only the two earlier bands, exhausts it 0.0018 s before. The 15 trial flights of A078 that meet all three bands hold between 0.034 and 0.329 kg above the reserve at 00:11.

### Numerical step

The numerical check repeated one returned flight of each of the 26 accepted arrivals at half the integration step. All 26 remained supported to 00:11:00 and were resolved. Fuel at 00:11 changed by between -0.074 and +0.152 kg (14 of the 26 decreased).

- **A078** (the repeated flight is its returned solution, index 0): at half step it has 0.061 kg less fuel at 00:11, leaving 0.040 kg above the reserve, and exhausts engine fuel 0.027 s after 00:11:00 instead of 0.068 s. Position at 00:11 differs by 0.014 m. Resolved.
- **The four arrivals without an accepted flight were not repeated at half step.** The check repeats returned flights only. Their fuel-exhausted trial flights that meet the two earlier bands run out 0.02 to 0.36 s before 00:11:00 at the latest. At the fuel flow of these flights (about 1.5 kg per second: in the returned flights 30.0 kg lasts 20.4 s) that is about 0.03 to 0.5 kg, a range that overlaps the changes the half step produced in this group (up to 0.15 kg).

### Interpretation

The computed outcomes above stand as computed. Separately:

- **31,946 ft is marginal for this group under the tested model and search.** Accepted and unsuccessful searches occur among closely related arrivals, separated by a few kilograms of fuel at 19:41 and by less than a second of engine endurance at 00:11.
- **The pattern against starting fuel is an observed association, not a fuel-only threshold.** The arrivals also differ in position, course and fitted turns. Within the second row of the table the returned fuel is not ordered by starting fuel (A104 starts with 25,983.7 kg and has 5.473 kg above the reserve; A102 starts with 25,983.8 kg and has 1.821 kg).
- **The margins are outputs of the calculation.** The run does not establish that the real aircraft's fuel at 19:41 or its consumption is known to a few kilograms. That uncertainty limits how strongly an unsuccessful search can be read; it does not supply an accepted flight.

## Accepted flights: where they are at 00:11 and when their fuel runs out

266 distinct accepted flights, each counted once per configuration (one flight, in `A023_TO275`, was returned by both directions; 7 lie on an end of the searched second-turn time, in three configurations of the Mach 0.78 group). Fuel exhaustion times are reported outcomes of the continuation. They were not used to select or reject any flight.

| Group | Level | Flights | Latitude at 00:11 (deg) | Longitude at 00:11 (deg) | Engine fuel above reserve at 00:11 (kg) | Engine fuel exhausted, relative to 00:11:00 (s) | Relative to 00:19:29 (s) |
|---|---|---|---|---|---|---|---|
| 25,661 ft, Mach 0.67 | 25,661 ft | 30 | -31.69 to -31.39 | 95.51 to 95.82 | 170 to 204 | +109 to +132 | -400 to -377 |
| 25,661 ft, Mach 0.67 | 30,053 ft | 37 | -30.89 to -30.56 | 96.34 to 96.65 | 2,268 to 2,304 | +1,625 to +1,651 | +1,116 to +1,142 |
| 25,661 ft, Mach 0.75 | 31,946 ft | 26 | -34.90 to -34.62 | 91.72 to 92.09 | 0.1 to 30.0 | +0.07 to +20.42 | -509 to -489 |
| 25,661 ft, Mach 0.75 | 33,985 ft | 34 | -34.53 to -34.25 | 92.22 to 92.58 | 844 to 877 | +601 to +626 | +92 to +117 |
| 27,830 ft, Mach 0.67 | 27,830 ft | 20 | -31.24 to -30.95 | 95.97 to 96.27 | 1,606 to 1,638 | +1,094 to +1,116 | +585 to +607 |
| 27,830 ft, Mach 0.67 | 30,053 ft | 37 | -30.78 to -30.47 | 96.39 to 96.73 | 2,572 to 2,605 | engines running at 00:40:00 | |
| 27,830 ft, Mach 0.75 | 31,946 ft | 21 | -34.78 to -34.52 | 91.87 to 92.22 | 456 to 488 | +311 to +333 | -198 to -176 |
| 27,830 ft, Mach 0.75 | 33,985 ft | 28 | -34.40 to -34.14 | 92.38 to 92.72 | 1,329 to 1,360 | +946 to +969 | +437 to +460 |
| 29,987 ft, Mach 0.75 | 31,946 ft | 8 | -34.65 to -34.63 | 92.05 to 92.08 | 854 to 884 | +582 to +603 | +73 to +94 |
| 29,987 ft, Mach 0.75 | 33,985 ft | 12 | -34.26 to -34.23 | 92.57 to 92.65 | 1,749 to 1,779 | +1,244 to +1,265 | +735 to +756 |
| 29,987 ft, Mach 0.78 | 33,985 ft | 13 | -35.71 to -35.68 | 90.50 to 90.60 | 513 to 544 | +351 to +373 | -158 to -136 |

- **Across the catalogue:** at 00:11 the accepted flights lie between 30.47 and 35.71 degrees south and between 90.50 and 96.73 degrees east: the Mach 0.67 flights near 31 degrees south, 96 degrees east; the Mach 0.75 flights near 34.5 degrees south, 92 degrees east; the Mach 0.78 flights near 35.7 degrees south, 90.5 degrees east.
- **Fuel exhaustion:** 229 flights exhaust engine fuel before 00:40:00 and 37 still have engines running then. Of the 229, 90 exhaust it before 00:19:29 and 139 after. None is within 60 s of 00:19:29; the nearest are 73 s after (`A005_TO275`) and 136 s before (`A018_TO250`).
- **Within a group, the higher level always exhausts fuel later.** In three groups (25,661 ft at Mach 0.67 and at Mach 0.75; 27,830 ft at Mach 0.75) the two levels with accepted flights fall on either side of 00:19:29. That is a description of these outcomes, and the question it raises (intermediate levels) is a separately declared experiment.
- **Optional query, not used in any choice:** none of the 266 accepted flights is inside 32 to 33 degrees south, 94 to 96 degrees east at 00:11:00, and none of the 229 is inside it at engine-fuel exhaustion. Both are airborne positions.

Source: `PROD_SOLUTIONS.csv`.

## Frequency at the fitted times (reported, not used)

The frequency residual at 20:41, 21:41 and 00:11 was recorded for every accepted flight and played no part in acceptance. For all 267 accepted-flight records (one per direction that returned the flight) it is within 7 Hz at all three times: -5.83 to -1.94 Hz at 20:41, -4.68 to -2.24 Hz at 21:41, and -1.72 to +4.16 Hz at 00:11. These are the three fitted times only; nothing here concerns the final transmissions.

## Numerical checks

One returned flight per direction with an accepted flight, repeated at half the integration step (7.5 s) to 00:11:00 and to 00:40:00. 218 were owed (206 left, 12 right). The one direction whose accepted flights all lie on a range end owed none.

| Quantity | Result | Criterion |
|---|---|---|
| Performed | 218 of 218 | |
| Resolved | 218 | |
| Supported to 00:11:00 at half step | 218 | required |
| Position difference at 00:11 | median 0.049 m, largest 0.267 m | 1 m |
| Timing difference at 00:11 | largest 0.001 microseconds | reported |
| Fuel difference at 00:11 | median 0.005 kg, largest 0.298 kg | reported |
| Same computed ending | 218: fuel exhaustion in both runs for 198, engines running at 00:40:00 in both for 20 | required |
| Fuel-exhaustion time difference | median 0.005 s, largest 0.213 s (198 checks) | 1 s |

A check speaks for the flight that was repeated. It does not validate the other trial flights of the search, and it does not repeat searches that returned no flight. `PROD_NUMERICAL_CHECKS.csv` names the repeated flight in each row.

## Computation

| Stage | Used (s) | Allowance (s) |
|---|---|---|
| Gate | 1,523 | 3,000 |
| Searches and continuations | 270,803 | 372,000 |
| Numerical checks | 10,148 | 25,000 |
| Lost | 0 | |

The search total includes the full reservations (120 s each) of the two flights interrupted by the restart.

Cost per arrival, searches and continuations:

| Group | Mean (s) | Range (s) | Total (s) |
|---|---|---|---|
| 25,661 ft, Mach 0.67 | 2,084 | 1,846 to 2,370 | 62,513 |
| 25,661 ft, Mach 0.75 | 2,675 | 1,993 to 3,092 | 80,252 |
| 27,830 ft, Mach 0.67 | 2,022 | 1,793 to 2,334 | 40,436 |
| 27,830 ft, Mach 0.75 | 2,987 | 2,510 to 4,042 | 59,744 |
| 29,987 ft, Mach 0.75 | 4,319 | 3,862 to 4,783 | 17,277 |
| 29,987 ft, Mach 0.78 | 2,645 | 1,697 to 3,250 | 10,581 |

Timeline (UTC): gate 14 November 16:14 to 16:40; searches 14 November 16:40 to 16 November 06:59, in 21 sessions on two processors; numerical checks 16 November 06:59 to 09:49, in 2 sessions on one processor. Regression: all 27 searches with a pilot reference gave every compared value equal (`REGRESSION.json`); tranche 1 passed before the other 102 arrivals were released.

## Deviations and corrections, in order

1. **Machine restart, 14 November 22:08 UTC.** The machine restarted while two flights were being computed (`A013_TO300#L` and `A014_TO275#L`, grid stage). Each was charged its full 120 s reservation and repeated, as the method requires. No record was lost and the run resumed from the published account.
2. **Reporting changes after the run (Amendment 4).** The analysis script took trial fuel-exhaustion counts and times from compact summaries that omit the time for one stage of the search. They are now taken from the detailed ledger, and the trial flights are split by the timing bands they meet. The effect is confined to four configurations (57 flights; `A030_TO275`, `A034_TO275`, `A038_TO275`, `A078_TO275`). No flight was recomputed and the runner revision is unchanged.
3. **Interim reports corrected.** Reports given during the run (in the working conversation, not committed) contained three statements that Codex's reviews corrected and that this document does not repeat: that trial flights "matching the timing" ran out 0.0 to 0.5 s before 00:11 (the figure was the latest exhaustion of any trial flight, and small negative margins had been rounded to zero); that some records carried no exhaustion time (they are in the ledger); and that 5 to 8 trial flights per accepted arrival meet all three bands (14 to 19, from the ledger).
4. **Count of accepted flights.** An interim report gave 267 distinct accepted flights. That counts a flight once per direction; counted once per configuration there are 266.

5. **Wording corrected after Codex's review of `43a46b2`.** Three statements were narrowed without any change to the tables: "no starting point" is described as what the bounded search found; the fuel-exhaustion times of trial flights meeting the two earlier bands are stated for the fuel-exhausted subset only; and the levels with accepted flights are described as tested levels, not as continuous ranges of altitude.

No arrival, level, speed, range or rule was added or changed after results were seen.

## What this does not show

- That a configuration with no accepted flight has none outside the searched turns, or under a different climb time.
- Anything about intermediate levels, later climbs or changes of speed.
- Where a flight ends: positions are airborne model states, not impact positions.
- Compatibility with the final transmissions, an auxiliary-power-unit restart, or the 22:41 measurement.
- A probability for any flight or region. The number of accepted flights in a part of the catalogue is not a probability.
- That the real aircraft's fuel state is known to the precision of the calculation.
- Robustness to the satellite ephemeris and its calibration: the separate audit in `../SATELLITE_EPHEMERIS_AUDIT/` found the admission of the earlier histories sensitive to those inputs; this run uses the frozen Table 4 model throughout.

## Appendix A: readings that were withdrawn or negated

| Reading | Status | Why |
|---|---|---|
| The outcome of a group's pilot arrival holds for every arrival of the group at every level | Negated for one of 22 group and level combinations | 4 of 30 arrivals at 25,661 ft and Mach 0.75 have no accepted flight at 31,946 ft |
| A fuel threshold between 25,976.8 and 25,983.5 kg at 19:41 separates accepted from unsuccessful arrivals | Withdrawn | Three later arrivals at 25,980.3 kg were accepted; the arrivals differ in more than fuel; returned fuel is not ordered by starting fuel within a cluster |
| The trial flights that match the timing run out 0.0 to 0.5 s before 00:11 | Withdrawn | The figure was the latest exhaustion of any trial flight; exhausted flights have no 00:11 residual |
| Some fuel-exhausted trial flights have no recorded exhaustion time | Withdrawn | All are in the detailed ledger; a compact summary omitted them |
| "The fuel model cannot resolve the difference, so the level stays possible for the whole group" as a statement of the result | Withdrawn as a result; kept as interpretation | Computed outcomes and physical uncertainty are separate statements |
| Fuel exhaustion near 00:19:29 as a property of the accepted flights | Not found in this catalogue | No accepted flight exhausts engine fuel within 60 s of 00:19:29. This was a reported outcome and not a selection criterion; the run was not designed to find or exclude it |

## Appendix B: audit trail

| Item | Where |
|---|---|
| Method and amendments | `METHOD.md` |
| Frozen runner and rules | `prod.py`, `prod_rules.py`, `durable.py`, `build_manifest.py`, `engine_deps.py`, `PINNED.json`, `ENGINE_DEPENDENCIES.json` (revision `2a016b1294fa`, commit `37199ce`) |
| Manifest and starting states | `PRODUCTION_MANIFEST.csv`, `ARRIVALS_108.csv`, `HANDOFF_REFERENCE_108.json` |
| Gate | `GATE_RESULT.json` (passed, 12 of 12 checks, published `c4732d6`) |
| Account | `checkpoint/2a016b1294fa/ACCOUNT.json`: every reservation and settlement, each published as its own commit (281 commits, the last `2dfe846`) |
| Search records and flight ledgers | `checkpoint/2a016b1294fa/arrivals/A001.tar.gz` to `A108.tar.gz` |
| Numerical checks | `HALF_STEP_CHECKS.json`, `checkpoint/2a016b1294fa/checks/checks.tar.gz`, `PROD_NUMERICAL_CHECKS.csv` |
| Tables | `PROD_CONFIGURATIONS.csv`, `PROD_DIRECTIONS.csv`, `PROD_SOLUTIONS.csv`, `PROD_SUMMARY_BY_GROUP_AND_LEVEL.csv`, `PROD_GROUPS_WITH_MIXED_OUTCOMES.csv`, `PROD_SUMMARY.json`, `REGRESSION.json` |
| Analysis and its tests | `analyze_prod.py`, `test_prod.py`, `TEST_PROD.log` (68 tests) |
| Check of the figures in this document | `verify_findings.py` |

Four historical input files used by the frozen runner are held on the computing machine and are not in the repository, as accepted at review; their hashes are in `ENGINE_DEPENDENCIES.json`.

## For the next stages

These are separately declared experiments and none has been started.

- **Intermediate levels** between the tested ones: in three groups the two levels with accepted flights fall on either side of 00:19:29, and 31,946 ft is marginal for one group.
- **Later climbs** for the Mach 0.67 arrivals, whose climbs at 19:41 to 31,946 ft and to 33,985 ft stop at the lift-margin limit at that weight.
- **The four arrivals without an accepted flight at 31,946 ft**, repeated at half the integration step, if their classification is to be relied on.
- **Sensitivity to the satellite inputs**, which waits on the decisions recorded in the ephemeris audit.
