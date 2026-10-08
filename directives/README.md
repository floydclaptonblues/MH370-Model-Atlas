# Directives

The task briefs written for the execution agent, in the order they were issued. They are here so that the thresholds in the atlas can be checked against the record rather than taken on trust.

**Why this matters.** A negative result is easy to produce by accident — stop early, pick a convenient cutoff, test one configuration. The only thing separating a real null from a failed search is a record of what was declared before the data came back. These files are that record. Several carry numbers that were fixed in advance and then failed, and the failures were reported rather than adjusted.

Each brief was written against standing rules that appear in most of them verbatim: never tune a parameter toward the 7th arc or any flight path; label uncertainty and assumptions; keep an appendix of failed hypotheses and an audit trail; use only real data from the project's files and say where something is missing or unverified.

## What to check

| Claim in the atlas | Where it was declared, before the result |
|---|---|
| The B1 bias fit stopped at Step A with no supported correction | `12` §1, §3 — the support rule and the gates (50% error reduction at 90 and 180 d, skill drop no worse than 0.02, meridional error up no more than 10%, fitted value not at a bound) |
| No drift source region is determinable | `16` §2 — the recovery gate (true cell inside the 50% mass region in ≥60% of trials, median mode-to-truth under 800 km) stated against a box whose width is given, with "if no configuration passes, stop" written in |
| The detection weights are judgement, not data | `16` §1 — `D1` declared as an ordinal ranking set by Claude, `D3` labelled CIRCULAR by construction and required to be flagged on every output row |
| The terminal result survives or fails a convention sweep | `15` §2, §5 — κ defined as a diagnostic coordinate, "do not nominate a preferred κ", and a requirement to report a result that reverses the previous task |
| Northern latitudes are excluded by the signals, not fuel | `17b` §4 — χ² and fuel reported separately as functions of latitude, with reporting bands declared in advance |
| The arc-1 sweep tier was not chosen for convenience | `18f` §4 — the fallback ladder pre-authorised, arc-1 resolution never cut on any rung |
| The ERA5 extension will not silently splice two reanalysis vintages | `19` §3 — the overlap gate (agreement to 1×10⁻³) with "if the gate fails, do not splice" written in before any download |
| Whatever the arc-1 sweep concludes, the grid that produced it could find a known answer | `20` §5 — Gate E: the grid must contain C120's own command vector as an explicit node and must reach χ² ≤ 8.2 at C120's own arc-1 start, declared with "if it does not, no comparison between starts is interpretable — stop" |
| The sweep's northern result is not read off a coarse grid | `20` §6.2 — two stages with Stage-1 and Stage-2 χ² required in separate columns, and "never compare a Stage-1 value against a Stage-2 value" |
| A northern arc-1 start is not a northern endpoint | `20` §6.3 — the 00:11 position required on every row, for that reason, before any row existed |
| The northern indication can be retired by its own test | `20` §7 — outcomes G1 to G4 written out before the numbers existed, G1 being "the northern indication is retired … it was my reading and it was wrong" |
| The 18:22 radar position never selected anything | `20` §9 — declared a zero-weight diagnostic: "not a term, not a prior, not a filter" |
| The reverse-drift density peak was tested against the possibility that it is only a flow feature | `21` §2 — Gate B: synthetic sources on a grid laid out "independent of the observed peak's location", with FLOW-DOMINATED, SOURCE-TRACKING and PARTIAL criteria fixed before the run |
| The reachability map was not quietly turned into a source estimate | `21` §2.4 — "Label it reachability. It is not a likelihood, not a posterior, and not a source estimate," with the reason given before the map existed |
| Claude's expectation did not shape the drift verdict | `21` §10 — the expected outcome (H1) recorded in the brief before the numbers existed, with "my prediction has no weight in how the gates are evaluated" |

## Corrections in the record

The briefs were revised when they were found to be wrong. Those revisions are kept rather than tidied away.

- **`17a` is superseded in full by `17b`.** The first version fixed the initial bearing and set a Mach floor of 0.70. Either alone would have made a northern endpoint unreachable by construction rather than by physics. `17b` §8 names both as errors.
- **`18b` is withdrawn**, by `18c` §1. It prepared a terminal handoff that was not wanted.
- **`18e` §4 set a branch threshold at "more than half", which was wrong**, and `18f` §2 corrects it: 25.4% of per-flight time was worth 224 minutes across the grid and should not have been discarded for missing an arbitrary line.
- **`18f` §6 records an inference drawn from two benchmarks that turned out to use the same timestep**, so the difference between them measured nothing. The execution agent's diagnostic contradicted it and was right.
- **`16` §F** (answered in conversation, not in the file) corrected a half-normal kernel asserted to converge to a 100 km indicator. It converges to a point mass. The verification step built on it was replaced.
- **`21` §2 specified a synthetic harvester the archive already records as returning zero**, and `21b` §2 corrects it. The earlier synthetic work found that "all five fixed synthetic sites matched no items under either rule at this sample size" — so Gate B's qualification floor would have failed on every cell and spent the budget rediscovering a known null. `21b` adds a five-cell pilot that fails in minutes, a declared fallback ladder, and the requirement that whichever rung is used be applied to both the synthetic and the real side. The execution agent's question about which density field to read is what surfaced it.
- **`18a`–`18f` built a grid that did not contain the reference flight**, and `20` §5 is the correction. The grid's bearing resolution was 18° against C120's 184.6°, its Mach ceiling 0.86 against C120's 0.8406, and its pressure nodes bracketed 214.198 hPa without landing on it. Absolute χ² was then compared across starts as though that meant something. `20` requires the grid to recover C120's score at C120's own start before any other start is read, and stops the run if it cannot.

## Files

| File | Subject |
|---|---|
| `00`, `01` | Initial debris-drift simulation and follow-ups |
| `09` | Task 9 rerun |
| `10a`, `10b` | Where the western focus comes from; revised forward grid |
| `11` | Drifter hindcast and forward release grid |
| `12` | B1 exploratory calibration-only bias fit |
| `13` | Open-items registry and confirmation sheet |
| `14` | External source verification |
| `15` | BFO convention sensitivity, provenance and warm-up evidence |
| `16` | Graded source-region likelihood with a recovery gate |
| `17a`, `17b` | Latitude reachability (v1 superseded, v2 current) |
| `18a`–`18f` | The full arc-1 sweep and its amendments |
| `19`, `19b` | Extending the ERA5 forcing domain east and north; amendment once the files were supplied rather than downloaded |
| `20` | Activating the extended domain, then sweeping arc 1 on a grid that must first prove itself |
| `21`, `21b` | Whether the reverse-drift density peak is a source signal, a circulation feature, or a windage mixture — Ryan's hypothesis, tested; amendment identifying the field and fixing a dead gate |
| `_slides_prompt…` | The brief for a walkthrough deck, kept because it fixes what a public presentation of this work may and may not claim |

Results packages are not in this repository. The atlas pages report their contents, and the briefs state what was asked for.
