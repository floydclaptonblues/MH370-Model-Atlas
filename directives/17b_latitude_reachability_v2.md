# CODEX TASK 17 (v2, supersedes v1): which 00:11 latitudes are reachable, and what each one costs

Authorized by Ryan. This replaces the earlier Task 17 directive in full; do not execute the earlier version. Register as the next unused DIRECTOR number and write to a new folder `run2/latitude_reachability_001/`, with a new suffix if occupied. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results. Copy modules before modifying adapters.

## 0. The question, and the one design rule that keeps it honest

Every flight in the Average Day family so far arrives at 00:11 between 35.85°S and 36.85°S — seven solutions inside about 110 km. That is one commanded-flight shape, not a search outcome. The question is whether a more northerly 00:11 position is reachable at all, and if so what it costs.

**The design rule: sweep the commanded inputs and record where they land. Never choose a latitude and solve for a flight that reaches it.** Latitude is an output of this task, never a target, a constraint or a stopping condition. There is no optimiser anywhere in this task.

That rule is what keeps this consistent with the standing prohibition on tuning toward the 7th arc or any flight path. Scoring a flight against the real BTO and BFO observations is using the data and is required. Adjusting a parameter because it moves the aircraft toward a desired position is not, and does not happen here.

Explicitly forbidden: any optimiser, solver or search; any target latitude, position, arc distance or endpoint; comparing a result with the 7th arc, a candidate position, a search area or a TASK_022 contact, including as a plot overlay or a sanity check; changing C120 or any frozen record; adopting any flight from this task as a new reference; carrying anything from this task into the drift work.

C120 stays frozen and remains the reference. This task does not refit it, replace it, or rank anything against it. A finding that northern latitudes are unreachable, and a finding that they are reachable at modest cost, are equally acceptable results.

## 1. Part A — what the model can actually be told to do

Before sweeping, document the existing commanded-flight interface: which parameters a commanded flight takes, what the lateral mode is (constant track, constant heading, great circle, or whatever is implemented), and what the vertical mode is. Use only modes the model already implements. Do not invent a new path family, and do not add turns, step climbs or speed schedules that are not already supported.

**Establish how the 19:41:03 start position is constrained.** The four scored BTOs are at 20:41, 21:41, 22:41 and 00:11; the 19:41 BTO is not among them. Determine whether the start is placed on the 19:41 arc by construction, and how the model parameterises it. This decides the sweep in section 2:

- If the start is arc-constrained, sweep **position along that arc**, not latitude at fixed longitude. Moving north-south at a fixed longitude would walk the start off the arc while the score stays silent, because that BTO is unscored.
- If the start is genuinely free in range, sweep latitude at fixed longitude as a fallback and say so explicitly in the findings.

Report which case holds, with the file and line that establishes it.

Record the full vertical extent over which ERA5 provides real data. The package README notes that temperatures above the 300 hPa level are held at their 300 hPa values, and that ERA5 is clamped east of 102.4°E. An altitude sweep depends directly on both, and a northern arc crossing lies east of that clamp. Report which parts of the intended pressure range and which longitudes are supported by real data and which are extrapolated, and label every grid point accordingly. If a large part of the range is extrapolated, say so before presenting any result built on it.

Deliver `model_interface.md` and `forcing_support.csv`.

## 2. Part B — the sweep

Run the frozen model forward over a declared grid. One flight per grid point, no iteration.

**Fixed for every flight, in both k passes**, taken from C120: the 19:41 start longitude (or the arc parameterisation origin, per Part A), starting total fuel, the 15 lb APU earmark inside that total, constant commanded Mach, and no fuel profiling.

**Swept:**

- **Initial bearing**: 140° to 195° in 5° steps (12 values).
- **Commanded Mach**: 0.55 to 0.86 in 0.025 steps (13 values). Let the model's own buffet and envelope checks reject what is infeasible, and record every rejection with its reason. Do not narrow this range because low Mach looks implausible at altitude — that exclusion is a finding, not a grid choice.
- **Commanded pressure level**: 175, 220, 265, 310, 355, 400, 450 hPa (7 values). The low-altitude levels matter because slow flight is only sustainable lower down.
- **Start position**: three points spanning roughly ±1° of latitude equivalent, moved along arc 1 if Part A says the start is arc-constrained, otherwise at −1.0°, 0.0°, +1.0° latitude at fixed longitude.

That is 12 × 13 × 7 × 3 = 3,276 flights per k pass. Run **k = 1.0** as the first pass and **k = 1.024738** (C120's value) as the second. Do not vary k within a pass and do not fit it.

Benchmark one flight before committing and record the forecast. If both passes will not fit the ceiling, complete the k = 1.0 pass and report the second as not run. If one pass will not fit, coarsen uniformly across all four dimensions and state the tier. **Never drop a dimension, never narrow a range, and never coarsen or refine selectively toward any region.**

For every grid point record: the 00:11 position; the nine-term PHYSICAL χ² and all nine individual squared residuals; fuel remaining at 00:11 and at 00:17; fuel exhaustion time if it occurs; whether the point violates buffet or any implemented envelope limit, with the limit named; the aerodynamic and weather domain labels, including whether the track crossed east of the 102.4°E ERA5 clamp; and the integration status.

Deliver `sweep_grid.csv`, one row per flight.

## 3. Part C — the incoming-leg diagnostic (reported, never a filter)

Register the last military-radar position as a **derived approximate position**: 6.577718°N, 96.340795°E at 2014-03-07T18:22:12Z, computed from the published MEKAR and NILAM coordinates as the along-N571 point 10 nm past MEKAR. The Malaysian report gives the location in words, not as a latitude and longitude. The decimals describe the calculation, not the measurement. Record DSTG's caution that the final return was at long range where angular errors could produce substantial position errors, and that DSTG did not use this position quantitatively. Status EXTERNAL_DERIVED, never SOURCED, never a measured fix.

For every grid point, record: the great-circle distance from that position to the flight's 19:41 start; the implied minimum mean ground speed over the 4,731 s leg; the inbound direct bearing; and the turn angle required at 19:41 between that inbound bearing and the flight's commanded initial bearing.

For reference, from the 0.5°N 93.754°E start the leg is 734 km at 302 kt direct, inbound bearing 203.1°, against a heading of about 296° along N571 at 18:22. C120's 184.6° implies about 18° of left turn at the handshake; a 140° bearing implies about 63°.

**Do not filter, reject, weight or rank any grid point using these numbers.** Filtering on them would be tuning toward a route. They exist so that if the reachable northern region depends on large turns or implausible inbound speeds, that is visible in the findings rather than discovered later.

Deliver `incoming_leg.csv`.

## 4. Part D — the decomposition that answers the question

This is the point of the task. Report χ² and fuel feasibility **separately** as functions of the resulting 00:11 latitude, because they are different constraints and may not bind together.

- `chi2_vs_latitude.csv` and a figure: achieved 00:11 latitude against nine-term χ², every grid point plotted, with C120's 8.117071 marked as a horizontal reference line only. State the lowest χ² achieved in each one-degree latitude band.
- `fuel_vs_latitude.csv` and a figure: achieved 00:11 latitude against fuel exhaustion time, marking which points exhaust before, during and after the 00:17 window, and which still hold fuel at 00:19:37.
- A joint map: for each latitude band, whether any grid point is simultaneously inside the performance envelope, exhausting fuel in a declared window, and within a declared χ² of C120. Declare those windows now, before any run: **fuel exhaustion between 00:10 and 00:25, and χ² within 2.0 of C120's value.** These are my thresholds, fixed in advance, and they are reporting bands rather than acceptance criteria. Report the full curves regardless so a reader can apply different bands.
- Report the 19:41 BFO squared residual separately against bearing. That term is currently the model's largest single misfit at about 2.90 of C120's 8.117, and bearing drives it directly, so the sweep may improve it. Say whether it does.

Then state plainly which constraint binds in the north: the signals, the fuel, the performance envelope, the ERA5 support, or none of them. If northern latitudes are excluded, say which term excludes them and by how much. If they are not excluded, say that too, and do not soften it.

## 5. Part E — the fuel-model sensitivity

The README flags that one-engine fuel burn may be too generous at altitude, roughly FL370 at M0.60 against FL290 in the ATSB figure. Too generous means excess range, and excess range pushes the endpoint south.

As a declared sensitivity only, rerun a reduced grid with the single-engine burn rate scaled by 1.1 and 1.25, and report how far the reachable latitude band moves. These scalings are arbitrary probes, not corrections, and must be labelled as such on every row. Do not adopt either, and do not change the frozen fuel model.

Report separately the duration of the single-engine phase in a representative flight, so the size of the effect is visible rather than assumed.

## 6. Verification, budget, deliverables

- Reproduce C120's nine-term χ² of 8.117071226374 and its 00:11 position exactly through the sweep code path at its own commanded parameters, and report the difference. If it does not reproduce, stop and report that rather than proceeding.
- Confirm by hash that no frozen input and no TASK_021, TASK_022 or TASK_026 record changed, and report the count.
- Confirm no arc, candidate, contact or search-area file was opened, by listing every input actually read.
- A 120-minute numerical ceiling, with 20 minutes reserved for verification and 15 for packaging, reported separately and not mislabelled as CPU time.
- `NOTES.md` with assumptions, every declared parameter, failed approaches, hashes, runtime and an audit trail. `FINDINGS.md` with the Part D answer first.

## 7. Stop rule

Deliver the map, then stop. No optimiser, no refit of C120, no adopted flight, no arc comparison, no endpoint, no search recommendation, no automatic follow-on. Write "latitude reachability map complete" when Parts A to E are done, whatever they show. Name precisely anything not assessed.

A reachable northern latitude in this map is **not** a candidate endpoint. It is a statement that a commanded flight of this family exists with that 00:11 position, at a stated cost in χ² and fuel, under a stated incoming-leg requirement.

## 8. Notes from Claude (not instructions)

- My expectation is that fuel binds before the signals do, because C120's fuel allowance is active with a margin near 0.1 kg. But the handshake BTOs at 20:41, 21:41 and 22:41 pin ring radii over time and therefore constrain average speed, so the signals may bind first. Which one binds is the finding, and I do not know it in advance.
- The 00:11 BTO fixes a ring, not a latitude. Position along that ring is set by the speed and track history, which is why a sweep is the right instrument and a single-point solve is not.
- Grid bounds are mine. Mach 0.70 would have capped the answer near 30°S, which is why the floor is 0.55. The bearing range matters because the arc crossing moves east as it moves north; a fixed bearing would have made the question unanswerable by construction. Both were errors in the first version of this directive.
- Geometry I computed, for orientation only and not as targets: from a 0.5°N 93.754°E start the arc crossing is near 30°S at bearing 172°, near 25°S at 163°, near 20°S at 153°. Mean ground speeds over the 4h30m to 00:11 are about 211, 183 and 159 m/s respectively. No grid point may be chosen or scored by reference to these.
- Paths with turns after 19:41, step climbs or speed schedules are outside this task and outside the commanded-flight family as implemented. A northern endpoint reachable only by such a path will not appear here, and the findings must say so.
