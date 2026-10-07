# CODEX TASK 17: which 00:11 latitudes are reachable, and what each one costs

Authorized by Ryan. Register as the next unused DIRECTOR number and write to a new folder `run2/latitude_reachability_001/`, with a new suffix if occupied. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results. Copy modules before modifying adapters.

## 0. The question, and the one design rule that keeps it honest

Every flight in the Average Day family so far arrives at 00:11 between 35.85°S and 36.85°S — seven solutions inside about 110 km. That is one commanded-flight shape, not a search outcome. The question is whether a more northerly 00:11 position is reachable at all, and if so what it costs.

**The design rule: sweep the commanded inputs and record where they land. Never choose a latitude and solve for a flight that reaches it.** Latitude is an output of this task, never a target, a constraint or a stopping condition. There is no optimiser in this task.

That rule is what keeps this consistent with the standing prohibition on tuning toward the 7th arc or any flight path. Scoring a flight against the real BTO and BFO observations is using the data and is required. Adjusting a parameter because it moves the aircraft toward a desired position is not, and does not happen here.

Explicitly forbidden: any optimiser, solver or search; any target latitude, position, arc distance or endpoint; comparing a result with the 7th arc, a candidate position, a search area or a TASK_022 contact, including as a plot overlay; changing C120 or any frozen record; adopting any flight from this task as a new reference; carrying anything from this task into the drift work.

C120 stays frozen and remains the reference. This task does not refit it, replace it, or rank anything against it. A finding that northern latitudes are unreachable, or that they are reachable at modest cost, are equally acceptable results.

## 1. Part A — what the model can actually be told to do

Before sweeping, document the existing commanded-flight interface: which parameters a commanded flight takes, what the lateral mode is (constant track, constant heading, great circle, or whatever is implemented), and what the vertical mode is. Use only modes the model already implements. Do not invent a new path family, and do not add turns, step climbs or speed schedules that are not already supported.

Record the full vertical extent over which ERA5 provides real data. The package README notes that temperatures above the 300 hPa level are held at their 300 hPa values and that ERA5 is clamped east of 102.4°E. An altitude sweep depends directly on both. Report which parts of the intended pressure range are supported by real data and which are extrapolated, and label every grid point accordingly. If a large part of the range is extrapolated, say so before presenting any result from it.

Deliver `model_interface.md` and `forcing_support.csv`.

## 2. Part B — the sweep

Run the frozen model forward over a declared grid. One flight per grid point, no iteration.

- **Commanded Mach**: 0.70 to 0.86 in steps of 0.01.
- **Commanded pressure level**: 175 to 375 hPa in steps of 25 hPa, which spans roughly FL250 to FL430.
- **Start latitude at 19:41:03**: −2.0° to +2.0° in steps of 0.5°, at the existing start longitude.
- **k**: fixed at 1.0 for the whole sweep, and separately at C120's 1.024738, as two declared passes. Do not vary k within a pass and do not fit it.

That is 17 × 9 × 9 = 1,377 flights per k pass. If the budget cannot complete both passes, complete the k = 1.0 pass first and report the second as not run. Coarsen the grid uniformly if needed; never coarsen selectively or refine toward any region.

For every grid point record: the 00:11 position; the nine-term PHYSICAL χ² and all nine individual squared residuals; fuel remaining at 00:11 and at 00:17; the fuel exhaustion time if it occurs; whether the point violates buffet or any other implemented envelope limit; the aerodynamic and weather domain labels; and the integration status.

Deliver `sweep_grid.csv`, one row per flight.

## 3. Part C — the decomposition that answers the question

This is the point of the task. Report χ² and fuel feasibility **separately** as functions of the resulting 00:11 latitude, because they are different constraints and may not bind together.

- `chi2_vs_latitude.csv` and a figure: the achieved 00:11 latitude against the nine-term χ², every grid point plotted, with C120's 8.117071 marked as a horizontal reference line only. State the lowest χ² achieved in each one-degree latitude band.
- `fuel_vs_latitude.csv` and a figure: achieved 00:11 latitude against fuel exhaustion time, marking which points exhaust before, during and after the 00:17 window, and which still hold fuel at 00:19:37.
- A joint map: for each latitude band, whether any grid point is simultaneously inside the performance envelope, exhausting fuel in a declared window, and within a declared χ² of C120. Declare those two windows now, before any run: fuel exhaustion between 00:10 and 00:25, and χ² within 2.0 of C120's value. **These are my thresholds, fixed in advance, and they are reporting bands, not acceptance criteria.** Report the full curves regardless, so a reader can apply different bands.

Then state plainly which constraint binds in the north: the signals, the fuel, the performance envelope, or none of them. If northern latitudes are excluded, say which term excludes them and by how much. If they are not excluded, say that too, and do not soften it.

## 4. Part D — the fuel-model sensitivity

The README flags that one-engine fuel burn may be too generous at altitude, roughly FL370 at M0.60 against FL290 in the ATSB figure. Too generous means excess range, and excess range pushes the endpoint south.

As a declared sensitivity only, rerun a reduced grid with the single-engine burn rate scaled by 1.1 and 1.25, and report how far the reachable latitude band moves. These scalings are arbitrary probes, not corrections, and must be labelled as such on every row. Do not adopt either, and do not change the frozen fuel model.

Report separately the duration of the single-engine phase in a representative flight, so the size of the effect is visible rather than assumed.

## 5. Verification, budget, deliverables

- Reproduce C120's nine-term χ² of 8.117071226374 and its 00:11 position exactly through the sweep code path at its own commanded parameters, and report the difference. If it does not reproduce, stop and report that rather than proceeding.
- Confirm by hash that no frozen input, TASK_021, TASK_022 or TASK_026 record changed, and report the count.
- Confirm no arc, candidate, contact or search-area file was opened, by listing every input actually read.
- A 120-minute numerical ceiling, with 20 minutes reserved for verification and 15 for packaging, reported separately and not mislabelled as CPU time. Benchmark one flight before committing to the grid and record the forecast.
- `NOTES.md` with assumptions, every declared parameter, failed approaches, hashes, runtime and an audit trail. `FINDINGS.md` with the answer to Part C first.

## 6. Stop rule

Deliver the map, then stop. No optimiser, no refit of C120, no adopted flight, no arc comparison, no endpoint, no search recommendation, no automatic follow-on. Write "latitude reachability map complete" when Parts A to D are done, whatever they show. Name precisely anything not assessed.

A reachable northern latitude in this map is **not** a candidate endpoint. It is a statement that a commanded flight of this family exists with that 00:11 position at a stated cost in χ² and fuel.

## 7. Notes from Claude (not instructions)

- My expectation is that fuel binds before the signals do, because C120's fuel allowance is active with a margin near 0.1 kg. But the earlier handshake BTOs at 20:41, 21:41 and 22:41 pin the ring radii over time and therefore constrain the average speed, so the signals may bind first. Which one binds is the finding, and I do not know it in advance.
- The 00:11 BTO fixes a ring, not a latitude. Position along that ring is set by the speed and track history. That is exactly why this sweep is the right instrument and a single-point solve is not.
- The grid bounds are mine. Mach 0.70 is near the low end of sensible cruise, 0.86 is past Mmo, and the pressure range deliberately extends well below and above the 214 hPa the family has used. If the model refuses parts of that range, report the refusals rather than narrowing the grid quietly.
- Paths with turns, step climbs or speed schedules are outside this task and outside the commanded-flight family as implemented. A northern endpoint reachable only by such a path would not appear here, and the findings must say so.
