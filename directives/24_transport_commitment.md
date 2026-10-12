# CODEX TASK 24: transport commitment — which arc releases can reach the corridor the debris actually used

Authorized by Ryan. Register as the next unused DIRECTOR number. Write to `run2/transport_commitment_001/`. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results.

Standing rules, in force throughout:

- **No parameter is ever tuned toward any arc latitude, any endpoint, or any corridor outcome.** Corridors are defined in Part A before a single particle is released, from circulation alone, and are not revised afterwards.
- Gates declared here are evaluated as written. A failed gate is reported as failed.
- B0 stays frozen. No refit, no new calibration, no change to the wind-slip rule or the class table.
- Nothing crosses into the satellite branch. No arc-7 candidate's score, no BFO, no terminal case enters as a weight or a prior. Part E uses endpoint *coordinates* only, as release points, and never their scores.
- Nothing large leaves the Windows machine.

---

## 0. The idea, and why it is worth running

Reverse drift asks the ocean where the aircraft was. TASK_016 answered that it cannot say: the posterior mode moved 675 to 1,914 km when an unmeasured assumption changed. This task asks a different question, one that is robust to exactly that failure.

**Not "where did the debris come from" but "which release regions can reach the transport corridor the debris demonstrably used, and which cannot".** A set-valued question tolerates trajectory-level noise that destroys a posterior mode. If a broad span of arc can reach the western corridor, the finds constrain nothing about latitude and we will have established that cleanly. If only a narrow span can, that is a geographic constraint obtained without reconstructing any fragment's journey.

The structure this depends on is present in the project's own fields. Mean zonal velocity across 80&ndash;100&deg;E, by latitude, over the 17 archived months:

| latitude | 17-month mean | months flowing west |
|---|---|---|
| 41&deg;S | +8.6 cm/s | **0 of 17** |
| 39&deg;S | +4.6 | 0 of 17 |
| 37&deg;S | +3.6 | 1 of 17 |
| 35&deg;S | +1.2 | 5 of 17 |
| 33&deg;S | +1.4 | 10 of 17 |
| 31&deg;S | +0.1 | 8 of 17 |
| 29&deg;S | +3.8 | 5 of 17 |
| 27&deg;S | &minus;3.7 | **14 of 17** |

Two regimes with an undetermined band between them. **Verify this table independently before relying on it** &mdash; it was computed by Claude from the atlas monthly means and is a first-order diagnostic, not a Lagrangian measure.

---

## 1. The methodological constraint that governs everything below

The 6-hour versus 12-hour experiment produced a **median 850 km difference** between corresponding particle endpoints at 508 days. That is not a resolution deficiency to be fixed by a finer step. It is the signature of chaotic advection &mdash; neighbouring trajectories separating exponentially &mdash; and refining the step in a stretching flow does not converge an individual path, it produces a different realisation of it.

**Therefore: no claim in this task may depend on an individual trajectory.** Every reported quantity is a property of an ensemble or of a region. Individual paths may be integrated; they may not be quoted, mapped as findings, or used to assert that any particular object went anywhere.

The corollary is good news and should be stated in `FINDINGS.md`: **the trajectory-convergence problem is not a prerequisite for this analysis.** It would be fatal to a trajectory-level claim and is tolerable for a set-level one, provided the set-level discipline holds.

---

## 2. Part A — define the corridors from circulation, before any release

Define two transport corridors as regions of the ocean, using **only** the velocity fields. No find location, no coastline of interest, no arc latitude may enter the definition.

Suggested construction, to be stated exactly and fixed before Part B: integrate the time-mean zonal transport over the available period and partition the domain by its sign and persistence, producing a **western corridor**, an **eastern/southern corridor**, and an explicitly labelled **undetermined band** between them. Report the boundary's position and how it moves through the year.

**GATE A.** If no persistent partition exists &mdash; if the sign structure is not stable enough to define corridors without choosing a threshold that determines the answer &mdash; report that and stop. A corridor definition that has to be tuned to produce two corridors is not a corridor definition.

Record that the corridors were fixed before any release, with a hash, so the ordering is auditable.

---

## 3. Part B — forward ensembles from the arc

Release ensembles forward from arc-7 cells. **Forward, not backward** &mdash; this is the direction that avoids the backward-attractor pathology under test in TASK_021, and the two tasks must stay independent.

- Release cells along the arc at a stated spacing, spanning at minimum 20&deg;S to 42&deg;S.
- Each cell gets an ensemble over the B0 class set C0&ndash;C3 and the existing diffusivity, at a stated particle count, released at the crash epoch.
- Integrate forward under B0, unchanged.

For each release cell `c` and deadline `T`, report the **ensemble fractions**: `f_W(c,T)` in the western corridor, `f_E(c,T)` in the eastern, `f_U(c,T)` undetermined, plus the fraction beached and the fraction outside the domain. These fractions are the deliverable. No individual endpoint is reported.

---

## 4. Part C — sweep the deadline, do not choose it

Commitment at 240 days is a different classification from commitment at 508 or 900 days, and selecting one deadline selects an answer. **Report the full `f_W(c,T)` surface over `T` from 90 days to the end of the available period, at a stated interval.**

The first-commitment quantity Codex proposed is then read off the surface rather than fitted: for each cell, the earliest `T` at which the competing corridor's fraction falls below a declared threshold and stays below it for the remainder of the period. Declare that threshold now, before the surface exists.

---

## 5. Part D — the shuffled-find null (GATE)

TASK_009's lesson applies directly: scrambling the find locations left the reverse-drift peak where it was, because the structure belonged to the circulation rather than to the debris.

**The equivalent null here is mandatory.** Repeat the full analysis against shuffled find locations &mdash; the same number of coastal arrivals, relocated by the TASK_009 scheme &mdash; and compare the arc-latitude span that reaches the corridor containing them.

**GATE D.** If the span of arc that can reach the shuffled corridor is the same as for the real one, **the commitment structure is a property of the Indian Ocean and carries no information about MH370.** Report that as the result. A positive finding is only meaningful as a difference from this null.

---

## 6. Part E — the southern candidates, including the long glide

Using **coordinates only**, release the same ensembles from the project's own candidate endpoints and report their corridor fractions on the same basis as Part B:

| release | coordinate |
|---|---|
| C120 00:11 state | 35.848&deg;S, 90.393&deg;E |
| southern bin optimum | 36.000&deg;S, 90.176&deg;E |
| northern candidate | 32.003&deg;S, 95.258&deg;E |
| **G0 / S14 water contact** | **38.706&deg;S, 90.415&deg;E** |
| R0 control | 38.509&deg;S, 90.266&deg;E |

G0 is the one to watch. Its contact sits where the archived monthly means run eastward in 17 months of 17, which would be a difficulty for any debris-delivery story from that endpoint **entirely independent of the frequency data that rejects it**. That is worth knowing either way, and it is the only test in this project that reaches the glide from a direction the BFO cannot.

**No score, no &chi;&sup2; and no terminal diagnostic enters this part.** These are coordinates being used as release points. Nothing here re-ranks any candidate, and the output is corridor fractions, not a likelihood.

---

## 7. What cannot be established with the inputs on hand — declare this before running

**The strongest of Codex's three categories is unavailable and must not be claimed.** "Robustly committed &mdash; competing corridors unreachable under explicitly bounded forcing assumptions" requires sampling the uncertainty of the current field itself. **Only one current realisation exists here.** Perturbing wind slip and diffusivity samples the debris response, not the ocean. Every result from this task is therefore at most **conditionally committed under the tested variations**, and `FINDINGS.md` must say so in those words.

Two further limits, stated rather than buried:

- **Stokes drift is explicitly zero in B0.** A wave-driven transport term is absent, not small. A boundary in the water is not necessarily a boundary for a flaperon riding the surface, and this is the term that would decide it.
- The wind-slip floor of 1.2% was fitted to ERA-Interim winds, BRAN2015 currents and a CAWCR wave hindcast &mdash; products B0 does not use &mdash; with no transfer validation. Every corridor fraction inherits that.

**Input check, to report in Part A:** the project record states no wave product was obtained, while Ryan's own notes describe holding four years of Copernicus ocean data including Stokes drift. Establish which is true. If a Stokes field is actually available and simply never ingested, say so plainly &mdash; that changes what this task could eventually become, though it does not change this run, which uses B0 unchanged.

Daily GLORYS in place of monthly means is likewise worth having and is **not** required for this task, per &sect;1. If it is available, report that; do not block on it.

---

## 8. Scope and stop rule

No reverse drift. No source-region estimate. No refit of B0. No change to the matching rule, the class table or the slip floor. No candidate is ranked, nominated or excluded by this task.

Deliver Parts A to E and stop. Final line, one of:

- `"Transport commitment: informative"` &mdash; with the arc span that reaches the western corridor, the deadline at which it stabilises, and the Gate D null comparison in that line.
- `"Transport commitment: uninformative"` &mdash; the span is broad, or Gate D shows the null behaves the same.
- `"BLOCKED at Part <X>"` with the reason.

---

## 9. Note from Claude

The attractive outcome here is a narrow span of arc. That is also the outcome most likely to be manufactured, by a corridor boundary placed where it separates the latitudes someone already prefers. Part A exists to make that impossible: the corridors are fixed from circulation, hashed, before any release, and Gate D checks the whole thing against scrambled finds.

I would rather this return "uninformative" honestly than "informative" by construction. A clean negative here is worth real money &mdash; it would mean the debris record constrains the ocean and not the latitude, which is a sharper statement of what TASK_016 found than TASK_016 managed.
