# MH370 Model Atlas

A static site collecting the satellite, flight-model and debris-drift work on MH370, built entirely from the project's own files. Where a source is missing, assumed or unverified, the page says so.

**No part of this work locates the aircraft.** Every position in the atlas is a conditional model state. The drift analysis found no determinable source region. The satellite and flight chapter closed on 6 October 2026; the drift branch remains open.

## Pages

| Page | Contents |
|---|---|
| `index.html` | Overview, status of each model, sources used, sources set aside |
| `satcom.html` | 5,029 BTO/BFO rows from the Inmarsat log, the 19-row canonical event table, published satellite states |
| `flight.html` | Average Day reference flights, the TASK_021 solver, the TASK_022 terminal experiment, the TASK_026 convention sweep, TASK_029 reachability, Phase 5A candidates |
| `map.html` | Arc, candidates, search areas and reverse-drift density on one switchable map |
| `drift.html` | 17-month currents map, reverse-drift density, currents-only forward test, Tasks 7 to 9 |
| `drift2.html` | Drifter hindcast, forward release grid, permutation null, the B1 stop, provenance audit, and why no source region is determinable |
| `closing.html` | Closing report for the satellite and flight chapter, including an appendix of readings that turned out to be wrong |

## Headline findings

- **The cruise model fits.** C120 scores χ² = 8.117 on nine terms (4 BTO, 5 BFO) with no residual worse than 1.7σ — close to the expected value for nine degrees of freedom. It sits under nine active constraints, with k pinned at its lower bound and about 0.1 kg of fuel margin.
- **That fit is sharp, not permissive.** Moving the endpoint to 24–26°S raises χ² to 2,507.
- **The endpoint latitude is constrained by the handshake sequence, within the region the model can see.** Northern commands reach 23.9–26.4°S with fuel to spare but miss every ring by 108–127 km, at 24.8–29.2σ.
- **Northern endpoints were never testable.** ERA5 ends at 10°N and 100°E; the 7th arc crosses 100°E at 27.5°S. No flight in this model can reach the arc north of that, because there is no forcing there. About 1,460 km of arc, from 27°S to 15°S, lies outside both the forcing domain and every seabed search box in the manifest, whose northern limit is 27°S. The subset was evidently clipped to the region the search already assumed, so the model could never challenge the assumption that defined its inputs.
- **The terminal continuations that match the final frequency pair are not locations.** All twelve arrive supersonic at 2.1–2.7 × Vmo inside an aerodynamic proxy the model flags as unsupported.
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
