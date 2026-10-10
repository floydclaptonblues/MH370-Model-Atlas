# MH370 Model Atlas

A static site collecting the satellite, flight-model and debris-drift work on MH370, built entirely from the project's own files. Where a source is missing, assumed or unverified, the page says so.

**No part of this work locates the aircraft.** Every position in the atlas is a conditional model state. The drift analysis found no determinable source region. The satellite and flight chapter closed on 6 October 2026; the drift branch remains open.

## Pages

| Page | Contents |
|---|---|
| `index.html` | Overview, status of each model, sources used, sources set aside |
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

## Headline findings

- **The cruise model fits.** C120 scores χ² = 8.117 on nine terms (4 BTO, 5 BFO) with no residual worse than 1.7σ — close to the expected value for nine degrees of freedom. It sits under nine active constraints, with k pinned at its lower bound and about 0.1 kg of fuel margin.
- **That fit is sharp, not permissive.** Moving the endpoint to 24–26°S raises χ² to 2,507.
- **The endpoint latitude is constrained by the handshake sequence, within the region the model can see.** Northern commands reach 23.9–26.4°S with fuel to spare but miss every ring by 108–127 km, at 24.8–29.2σ.
- **There is now a real northern candidate, and it loses.** A solution at 32.00°S, 95.26°E scores χ² = 16.84, found from two bins converging on the same point from opposite sides — not a coarse-grid artifact. The southern solution scores 7.92. The difference is exactly linear in the frequency bias at 1.568 per hertz, so a common offset of +5.69 Hz would make them indistinguishable.
- **The bias was measured, and it points the wrong way for the north.** Calibrated against the published communication logs with the aircraft stationary at the gate: −1.39 Hz pooled, −0.36 Hz on the channel the scored events use. Applying it *widens* the gap to 9.50–11.10, and at the pooled value the northern candidate fails the χ² ≤ 20 gate it was admitted under. How far the bias drifts in the four hours to the scored window is still unmeasured, and that is the whole remaining question.
- **Northern endpoints were never testable.** ERA5 ends at 10°N and 100°E; the 7th arc crosses 100°E at 27.5°S. No flight in this model can reach the arc north of that, because there is no forcing there. About 1,460 km of arc, from 27°S to 15°S, lies outside both the forcing domain and every seabed search box in the manifest, whose northern limit is 27°S. The subset was evidently clipped to the region the search already assumed, so the model could never challenge the assumption that defined its inputs.
- **The terminal family is not uniformly supersonic, and the frequency pair never said it was.** TASK_022's twelve all arrived at 2.1–2.7× Vmo under C120. Under a different parent, arrivals range Mach 0.35–1.34, and the best-fitting case of all arrives at 1.1× Vmo while matching the final frequency pair to +0.82 and −0.42 Hz. What separates a survivable arrival from a supersonic one happens after the last transmission, so the observations cannot see it. None of these coordinates is a location.
- **No drift source region is determinable.** The method recovers known synthetic sources, but on the real finds the posterior mode moves 1,000–1,900 km when an unmeasured assumption changes — further than any single posterior is wide.
- **The 1.2% wind-slip floor was fitted to forcing products this model does not use** (ERA-Interim winds, BRAN2015 currents, a CAWCR wave hindcast), with no transfer validation.

## Directives

`directives/` holds the task briefs written for the execution agent, in the order issued, with superseded and withdrawn versions kept. They are there so the thresholds quoted in the atlas can be checked against the record: several were fixed in advance, then failed, and the failures were reported rather than adjusted. `directives/README.md` maps each claim to the brief that declared its threshold, and lists the briefs that were wrong and how they were corrected.

## Building

`gen.py` writes every `.html` page from inline templates plus the two bodies in `src/`. Run it from the repository root:

```
python3 gen.py
```

`data/` holds the JSON the pages fetch at runtime. `img/` holds generated figures. `fields/` holds monthly current and wind field text files.

## Standing rules this work was produced under

- No parameter is ever tuned toward the 7th arc or toward any flight path.
- Uncertainty and assumptions are labelled rather than smoothed over.
- Failed and superseded hypotheses are kept, including the author's own — see the appendix in `closing.html`.
- The satellite and drift branches are kept separate: no contact coordinate crosses into the drift analysis.
