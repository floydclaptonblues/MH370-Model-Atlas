# CODEX TASK 18 — ADDENDUM: Part F, the survivor set and terminal handoff

Add this as Part F of Task 18. It does not change Parts A to E. **Nothing in this addendum runs a terminal experiment.** It defines, before any result is seen, which cruise solutions would be eligible for one and freezes their states so a separate authorized task could run it.

## F.1 Why this is preregistered now

The terminal experiment costs roughly 10 s per history: TASK_022 used 6,062.658 s of measured numerical time for 582 histories on a single parent. It cannot be run across the sweep. Selecting survivors after seeing the map would be choosing the answer, so the rule is fixed here instead.

## F.2 The survivor rule

A grid point is a SURVIVOR if **all** of:

1. Integration completed, with no envelope or buffet violation, and no weather-domain exit.
2. Nine-term χ² ≤ 10.117071 (C120's value plus the declared band of 2.0).
3. Fuel exhaustion between 00:10 and 00:25 UTC.
4. The aircraft is powered through 00:11.

These are the same reporting bands declared in Task 17 v2 and used in TASK_029, unchanged. Report the survivor count in `FINDINGS.md`. **Zero survivors is a complete and reportable result**, and it would mean the arc-1 locus contains no commanded flight meeting the conditions C120 meets.

## F.3 Selection for handoff, capped and diversity-preserving

From the survivors, select at most **12** for the handoff, by this rule and no other:

- Bin survivors by achieved 00:11 latitude in 1° bands.
- From each occupied band take the single lowest χ².
- If more than 12 bands are occupied, take the 12 bands whose lowest-χ² entries are most widely separated in 00:11 position, so the handoff spans the reachable latitude range rather than clustering at the minimum.
- If fewer than 12 bands are occupied, take all of them and say so.

**Do not select the twelve lowest χ² overall.** That would collapse the handoff onto one latitude and discard exactly the spread this task exists to measure. If C120's own band is occupied by a different flight, keep both and label them.

## F.4 What to freeze and deliver

For each selected survivor, export the complete state a terminal experiment would need, in the same form TASK_022 consumed for C120:

- commanded parameters, arc-1 start, bearing, Mach, pressure, k;
- the full 00:11 state: ECEF position and ground velocity, air velocity and wind, mass and resources, thermodynamics, CL and lift direction;
- the engine-loss event time and state, where one occurs;
- the nine individual squared residuals;
- fuel chronology through 00:25;
- the incoming-leg diagnostics from Part D.

Deliver `survivor_handoff/` with one record per selected flight, plus `survivor_summary.csv` listing all survivors with their selection status and the band they represent.

## F.5 Scope limits

- **No terminal search, no frequency evaluation at 00:19:29 or 00:19:37, no contact propagation, no adopted flight.** This addendum produces frozen states and nothing else.
- A survivor is not a candidate aircraft history. It is a commanded flight meeting the same declared bands C120 meets, which is a statement about the model's feasible set.
- C120 remains the frozen reference and is not replaced by any survivor, including one scoring better.
- Nothing here crosses into the drift branch. Task 16 established that no source region is determinable from the drift data, so a terminal contact would have nothing to connect to regardless of what this produces.

## F.6 Cost note for whoever authorizes stage 2

At TASK_022's measured rate, a reduced terminal search of 96 histories per parent is roughly 1,000 s of numerical time, so twelve parents is about 3.5 hours plus contact propagation, refinement and verification. A full 582-history search per parent would be closer to 20 hours for twelve. That decision belongs to a separate directive, not to this one.

## F.7 Note from Claude (not an instruction)

TASK_029 found zero of 36 grid points meeting all three conditions. If that holds across the full arc-1 locus, the survivor set is empty, the handoff is empty, and the satellite chapter closes on a stronger statement than it currently carries: that C120 sits in a feasible set the sweep cannot otherwise populate. If instead survivors appear at starts we never tested, the 36°S clustering was an artifact of the inherited start and the chapter reopens. Both outcomes are worth the run.
