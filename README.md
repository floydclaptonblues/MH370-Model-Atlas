# MH370 Model Atlas

A static site collecting the satellite, flight-model and debris-drift work on MH370, built entirely from the project's own files. Where a source is missing, assumed or unverified, the page says so.

**No part of this work locates the aircraft.** Every position in the atlas is a conditional model state. The drift analysis found no determinable source region. The satellite and flight chapter closed on 6 October 2026; the drift branch remains open.

## Pages

| Page | Contents |
|---|---|
| `index.html` | What is measured and modelled (with the governing equations), where the evidence stands, how the work is checked, chapters, data sources |
| `flight-lab.html` | Windows 98 scientific viewer of the frozen 5,750-configuration catalogue: saved flight states, satellite tests and explanatory forces/wind instruments. No new flight fits; 22:41 stays sealed. Body: `src/flight_lab_body.html`; assets: `flight-lab/assets/`. |
| `arc7-demo.html` | Win98 scientific teaching tool: supplied illustrative arc positions, satellite geometry, a simplified interactive fuel–mass loop, and a clearly dated historical snapshot. Source and adaptation notes: `src/arc7_demo_NOTES.md`. |
| `methods.html` | **What each model computes.** BTO and BFO explained from first principles, the flight model's inputs and integration, what a drift particle is, every tolerance converted to physical units, and a worked example of why an error in the known signal leg transfers into the unknown one |
| `satcom.html` | 5,029 BTO/BFO rows from the Inmarsat log, the 19-row canonical event table, published satellite states |
| `flight.html` | Average Day reference flights, the TASK_021 solver, the TASK_022 terminal experiment, the TASK_026 convention sweep, TASK_029 reachability, Phase 5A candidates |
| `map.html` | Arc, candidates, search areas and reverse-drift density on one switchable map |
| `reference.html` | **All canonical data on one map** — ocean currents and winds by month, the published 7th arc and the ten derived rings, the satellite track, the last radar fix, debris finds and search areas, plus where to obtain each dataset at source and how the files are formatted |
| `canonical.html` | **Observations only.** The measurement record, published satellite states, the published 7th arc in full (both arms, to 45&deg;N), the debris find record and the seabed search boxes &mdash; with every model output deliberately excluded and listed as excluded |
| `drift.html` | 17-month currents map, reverse-drift density, currents-only forward test, Tasks 7 to 9 |
| `drift2.html` | Drifter hindcast, forward release grid, permutation null, the B1 stop, provenance audit, and why no source region is determinable |
| `northsouth.html` | **The live question.** A northern candidate at 32.00°S scoring χ² 16.84 against 7.92 in the south, why the comparison is exactly linear in the frequency bias, what the bias measures and which way it points |
| `closing.html` | Closing report for the satellite and flight chapter, including an appendix of readings that turned out to be wrong |

## Where the evidence stands

The landing page (`index.html`) carries the same summary. Findings later shown to be wrong are withdrawn in place on the pages where they were published, dated and struck through; see `closing.html` and `CORRECTION_AUDIT_20261023.md`.

- **Northern commanded flights reaching 23.9–26.4°S are rejected.** They miss every handshake ring by 108–127 km (24.8–29.2σ) and are still under power at 00:25, so they cannot produce the 00:19 log-on.
- **North (≈32°S) against south (≈36°S) is unresolved.** With the optimiser gradient defect corrected (22–24 October), the two score 4.840 and 4.821. The earlier 16.84 against 7.92 margin is withdrawn. An enumeration of the 19:41 state surface finds two basins, and which is deeper depends on whether the common frequency offset is held fixed or estimated.
- **The long glide G0/S14 is rejected.** It reaches the water 168 km beyond the 7th arc, wings level at 196 kt, and misses the final frequency pair by +34.2 Hz and −121.4 Hz. No vertical-compensation fraction in [0, 1] makes a glide compatible.
- **The final frequency pair does not require a supersonic arrival.** Across 72 terminal continuations, arrival speed ranges from Mach 0.35 to 1.34; a continuation arriving at 1.1× Vmo fits the pair to +0.82 and −0.42 Hz.
- **One engine could not hold the commanded cruise.** Mach 0.831 cannot be sustained; the best single-engine Mach is 0.688–0.698. Whether a descent was also required depends on which certified thrust rating applies.
- **The cruise fit has three nominal degrees of freedom** (nine scored values, six parameters). A close fit does not show that the aircraft flew a single course, and no fit has been shown to be the minimum of its family.
- **The 19:41 state is assumed.** No published connected flight from the primary-radar handoff reaches 19:41.
- **Four and a half years of debris transport executed.** 233–256 of 481 objects cross 80°E westward in year two and 168 reach 50°E in year three; year one is eastward.
- **No drift source region is determinable.** On the real finds the answer moves 1,000–1,900 km when an unmeasured assumption changes.

## Directives

`directives/` holds the task briefs written for the execution agent, in the order issued, with superseded and withdrawn versions kept. They are there so the thresholds quoted in the atlas can be checked against the record: several were fixed in advance, then failed, and the failures were reported rather than adjusted. `directives/README.md` maps each claim to the brief that declared its threshold, and lists the briefs that were wrong and how they were corrected.

## Building

`gen.py` writes every `.html` page from inline templates plus the page bodies in `src/`. Run it from the repository root:

```
python3 gen.py
```

`data/` holds the JSON the pages fetch at runtime. `img/` holds generated figures. `fields/` holds monthly current and wind field text files.

## Standing rules this work was produced under

- No parameter is ever tuned toward the 7th arc or toward any flight path.
- Uncertainty and assumptions are labelled rather than smoothed over.
- Failed and superseded hypotheses are kept, including the author's own — see the appendix in `closing.html`.
- The satellite and drift branches are kept separate: no contact coordinate crosses into the drift analysis.

