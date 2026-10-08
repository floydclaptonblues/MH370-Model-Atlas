# CODEX TASK 20: activate the extended domain, then sweep arc 1 properly

Authorized by Ryan. Register as the next unused DIRECTOR number. Write to `run2/domain_activation_001/`, new suffix if occupied. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results. **Do not modify the existing ERA5 subset, the original partial files, the pressure files, the provenance records, or any frozen input.** New data and new caches go alongside, never over.

Standing rules, unchanged and in force for every part of this task:

- **No parameter is ever tuned toward the 7th arc or toward any flight path.** Not the grid bounds, not a tolerance, not a stopping rule.
- Every gate in this file is declared before the run. A failed gate is reported as failed. It is not widened, moved or reinterpreted after the fact.
- Label uncertainty and assumptions. Keep the appendix of failed hypotheses and the audit trail.
- Use only real data from the project's files. Where something is missing or unverified, say so in those words.
- Nothing crosses into the drift branch. No contact, candidate or endpoint coordinate is read by, or written toward, any drift artifact.
- **Nothing from the forcing cache is staged out of the Windows machine.** Summary CSVs and JSON only, kilobytes not gigabytes.

---

## 0. Where this stands

Offline intake reports complete: seven-variable extended surface files for 2014-03-07 and 2014-03-08, all package hashes passed, dynamic fields unchanged, `z` and `lsm` matching the supplements exactly, and the earlier overlap matching exactly. Not yet done: loader changes, cache rebuild, C120 replay, Parts C and D of TASK 19, and any refit.

Exact overlap agreement is a stronger pass than TASK 19 Part C required (1×10⁻³). **Record it as a pass with the measured numbers and move on** — there is no vintage splice to worry about, and that should be stated in `FINDINGS.md` so the atlas can retire the concern rather than carry it.

What this task is for: the northern arc has never been evaluable in this model, because the forcing stopped at 100°E and the arc crosses 100°E at 27.5°S. If the extended domain now covers it, the question can finally be asked. **This task asks it. It does not assume the answer.**

---

## 1. Part A — domain audit, by field family (GATE A)

The intake note says the *surface* files are new and that the *pressure* files are preserved. A 777 at 214 hPa does not fly on surface fields. **Before anything else, establish which fields the flight loader actually reads at cruise, and what each one's domain bounds now are.**

Report, as `domain_audit.csv`, one row per field the flight model consumes:

| column | content |
|---|---|
| `field` | name as the loader asks for it |
| `stored_name` | name as stored in the file |
| `family` | `surface` or `pressure_level` |
| `source_file` | which file family supplies it |
| `lat_min`, `lat_max`, `lon_min`, `lon_max` | exact bounds as the loader now sees them |
| `levels` | pressure levels present, in order, or `n/a` |
| `t_first`, `t_last`, `t_step` | time coverage |
| `required_at_cruise` | yes / no, with the reason |

Then state, in one explicit sentence, the answer to this:

> **At what most-northerly and most-easterly point are *all* fields required for a cruise-altitude flight simultaneously available?**

**GATE A.** If the pressure-level fields do not cover the full target domain — 20°N to 50°S, 55°E to 120°E — then the northern arc is still not modellable, whatever the surface files cover. In that case:

- report exactly which fields, levels, times and regions are missing;
- state what a follow-up request would need, in CDS terms, to close it;
- **stop at the end of Part D.** Do not run Parts E, F or G on partial vertical coverage.
- **Do not extrapolate vertically from surface fields, do not substitute a nearby level, do not persist a last-good value across a domain edge, and do not fill a gap by interpolation.** If a flight would need forcing that does not exist, that flight fails and is reported as failing on domain, exactly as the 765 rows in TASK_030 did.

Also report, as part of Part A: whether the loader hard-codes domain bounds, array shapes, level counts or longitude conventions anywhere, quoting file and line numbers. That is the code that has to change, and it is identified before it is touched.

---

## 2. Part B — loader change and cache rebuild (GATE B)

Make the loader bounds data-driven rather than hard-coded, so the domain comes from the files. Keep the old behaviour reachable: the old subset must still load and still produce the old numbers.

Before building the new cache, **estimate its size and build time and report both.** The current cache is about 5.4 GB for the old domain. The new domain is substantially larger in both dimensions.

**GATE B.** If the estimated cache exceeds 60% of free disk on the target volume, report the estimate and the free space and stop for Ryan's decision. Do not build a cache that fills his disk, and do not silently fall back to a coarser cache to fit — if a coarser cache is the right answer, that is a decision to be taken explicitly and recorded, not a workaround.

Report actual cache size and build wall time once built.

---

## 3. Part C — record the overlap result

Produce `overlap_check.csv` and `overlap_gate.json` from the comparison already performed: maximum absolute difference per variable with units, the fraction of cells differing by more than floating-point noise, and whether any differences are structured by level, time or region. Record the gate as PASSED and note that agreement was exact rather than merely within tolerance.

---

## 4. Part D — C120 must not move (GATE D)

Re-run C120 against the extended forcing at dt 7.5 s. Report against the frozen values:

| quantity | frozen value |
|---|---|
| χ² | 8.117071226374 |
| 00:11 latitude | −35.84787668666737 |
| 00:11 longitude | 90.39256120382451 |
| fuel at 00:11 | 585.0195324362951 kg |
| engine loss | 2014-03-08T00:17:14.058422Z |
| k | 1.024738 |

Report all nine individual residuals and z² terms, not just the total.

**GATE D. C120 must reproduce to Δχ² < 0.01 and within 1 km at 00:11.** C120's entire track lies inside the old domain. Extending a domain outward cannot change a flight that never leaves the interior. If C120 moves, the ingest is wrong — **report and stop.** Do not proceed to the sweep on a forcing field that changed a flight it should not have touched.

Then confirm the loader returns real values, not an edge hold, at test points 105°E, 115°E, 10°N and 18°N. Report the most northerly latitude at which the 7th arc is now inside the domain, and the same for arc 1. Deliver `c120_regression.json` and `domain_after.json`.

---

## 5. Part E — prove the grid can find a known answer (GATE E)

**This part exists because of a specific error in the record, and it is the most important instruction in this file.**

TASK_030's grid reached χ² ≈ 1,174 at C120's own arc-1 start — a start that demonstrably supports 8.117. The grid was 145× off where the right answer was already known, because it did not contain C120: bearing resolution was 18° against C120's 184.6°, the Mach ceiling was 0.86 against C120's 0.8406, and the pressure nodes bracketed 214.198 hPa without landing on it. Absolute χ² was then compared across starts as though those comparisons meant something. They did not.

So, before sweeping anything:

**E1. State C120's command parameterisation exactly as the solver represents it.** Quote the file and the fields. C120's reported bearing drifts 184.6° → 185.8° and its Mach drifts 0.8406 → 0.8306, so a constant-bearing, constant-Mach command cannot be what C120 is — a constant true course produces a drifting great-circle bearing, and a constant TAS produces a drifting Mach as temperature changes. **Determine which it actually is. Do not assume.** The grid must be built in the solver's own command coordinates, not in a reparameterisation that cannot express C120.

**E2. Build the grid so that C120's own command vector is an explicit node**, at its exact values, not a nearby one.

**E3. Run the grid at C120's own arc-1 start and report the best χ² it achieves there.**

**GATE E. The grid must reach χ² ≤ 8.2 at C120's own arc-1 start.** It contains C120 as a node, so it must. If it does not, the grid is not representative of the solver and **no comparison between starts made on that grid is interpretable** — report the failure, state the discrepancy, and stop. Do not sweep.

Deliver `grid_fidelity.json` with the command parameterisation, the node list, the achieved χ² at C120's start, and the gate result.

---

## 6. Part F — the arc-1 sweep (only after Gates A–E pass)

### 6.1 Starts move along the arc-1 locus, not through a box

Arc 1 is a ring: centre 0.5327°N, 64.3347°E, angular radius 29.4182°. **Every start lies on that ring.** Establish the locus first and step the start along it, parameterised by latitude. A start that drifts off the ring would walk away from the 19:41 BTO while that term stays silent — the 19:41 BTO is unscored precisely because the ring constraint satisfies it geometrically. State that in `FINDINGS.md`, and report each start's residual distance from the ring as a plumbing check (it should be ~0).

**Latitude range: 20°N to 10°S, at 0.5° steps.** TASK_030's finding that no start north of 9°N produced a finite history was a domain artifact, not physics, and that ceiling is now gone. Report, per start, the ring longitude the locus puts it at.

**Arc-1 start resolution is never cut**, on any budget rung. That rule carried over from `18f` and still holds.

### 6.2 Two stages, not one flat grid

A single flat grid is what produced the uninterpretable 145× comparison. Replace it:

**Stage 1, coarse scan per start.** Bearing 140° to 205° at 5°. Mach from 0.55 to **0.87 (Mmo)** — the TASK_030 optima pinned at the old 0.86 ceiling from 6°N northward, and a pinned bound means the optimum may lie beyond it, so the ceiling moves to the aircraft limit and not past it. Pressure levels spanning the supported cruise band, including 214.198 hPa as a node.

**Stage 2, local refinement per start.** For every start whose Stage-1 best falls within two decades of the global Stage-1 best, refine locally at the resolution C120 itself enjoyed: bearing to ≤0.5°, Mach to ≤0.005, pressure to the solver's own continuous treatment if it has one.

**Report Stage-1 and Stage-2 χ² in separate columns, always.** Never compare a Stage-1 value against a Stage-2 value, and never quote a Stage-1 value as a start's χ². That conflation is the error this design exists to prevent.

### 6.3 What every row reports

`sweep_results.csv`, one row per start, with at minimum: start latitude, ring longitude, ring residual, Stage-1 best χ² and its command, Stage-2 best χ² and its command, whether any parameter sits at a bound and which, the nine individual z² terms at the Stage-2 optimum, **the 00:11 position**, fuel remaining at 00:11, engine-loss time, the k value and whether k is pinned, active constraint count, and the failure mode if the flight did not complete.

**The 00:11 position is not optional.** A northern arc-1 start flown on a southerly bearing still ends in the southern Indian Ocean; "the sweep points north" is a statement about where the aircraft was at 19:41, not about where it ended. Every row must make its own endpoint explicit so that distinction cannot be lost again.

### 6.4 Fuel is reported separately, never folded into the score

As in `17b`: report χ² and fuel as independent functions of start latitude. A northern start has further to fly to reach the arc, and C120 had about 0.1 kg of margin. If northern starts are fuel-infeasible, that is a finding about fuel, and it must not be able to masquerade as a finding about the signals. Report, per start: fuel required, fuel available, margin, and whether the fuel constraint is active.

---

## 7. Part G — what the result means, declared in advance

Write the interpretation rule now, before the numbers exist. In `FINDINGS.md`, report which of these the sweep produced:

**G1 — the northern indication is retired.** C120's start refines to ≈8.1 and every start north of it refines to χ² far worse (order 100 or more). The TASK_030 northern signal was a coarse-grid artifact. Say so plainly; it was my reading and it was wrong.

**G2 — the northern indication survives.** One or more northern starts refine to χ² comparable to or better than 8.117, with no parameter pinned at a bound, fuel feasible, and residuals no worse than about 2σ. That is a real second solution family and must be reported as one — with its endpoint, which is a separate question from its start.

**G3 — the northern starts are bound-limited.** Northern starts refine well but pin at Mmo, at a pressure limit, or at fuel exhaustion. Report the binding constraint as the finding. A solution that exists only beyond the aircraft's certified envelope is not a solution, and a solution pinned at a bound is a constrained optimum, not a free one — state which.

**G4 — still not evaluable.** Coverage, fuel or convergence prevents the comparison. State what is missing.

More than one may apply across different latitude bands. Report by band.

---

## 8. Budget

Measured: setup 13.34 s, per flight 39.28 s of which 34.93 s is command-dependent force calculation. The extended domain is larger and may change both — **take a fresh benchmark on the new cache before estimating, and report it.** Do not reuse an old timing figure on new forcing.

The mesh gate already passed at dt 15 s (Δχ² 3.42×10⁻⁷, position difference 1.48 mm), so Stage 1 runs at dt 15 s. Stage 2 and the Part D regression run at dt 7.5 s.

Estimate total wall time for Stage 1 and Stage 2 separately and report before running. If the estimate exceeds 10 hours, cut in this declared order and no other:

1. Pressure nodes in Stage 1 (keeping 214.198 hPa).
2. Mach nodes in Stage 1 (keeping the 0.87 ceiling and the 0.55 floor).
3. Stage-1 bearing step from 5° to 7.5°, never coarser.
4. Stop and ask for a ceiling extension.

**Arc-1 start resolution is not on that ladder.** Testing one arc-1 point was the original defect; the sweep does not get cheaper by reintroducing it.

---

## 9. Diagnostics that are computed and never scored

Report these, clearly labelled as diagnostics with zero weight in any score or selection:

1. **The 18:22 leg.** The last Malaysian military radar position is a derived-approximate 6.58°N, 96.34°E — derived, not a raw fix, and DSTG cautioned on long-range angular error and did not use it quantitatively. For each start, report the great-circle distance and bearing from that position to the arc-1 start, and the mean ground speed the 18:22→19:41 interval would require. **This is context for a reader, not evidence.** It is not a term, not a prior, not a filter. Do not let it select anything.
2. **Search-box overlap.** For each start's 00:11 position, whether it falls inside any seabed search box in the project manifest. The manifest's northern limit is 27°S and its boxes are flagged approximate, so this is coverage bookkeeping, not a likelihood.

---

## 10. Scope

- No drift work. No reverse drift, no debris, no beaching, no coastline comparison.
- No new terminal-scenario search. TASK_022's twelve contacts stay where they are and are not propagated as locations.
- C120 stays frozen as the primary reference throughout. The sweep does not replace it, re-fit it, or adjust it.
- The old ERA5 subset, the partial files, the pressure files and the provenance records stay on disk unmodified.
- If a part is blocked, report the block and stop at that part. Do not substitute a different reanalysis product, a coarser dataset, or an extrapolation.

---

## 11. Stop rule

Deliver Parts A through G and stop. Final line, one of:

- `"Domain activation complete"` — with the new bounds, the Part D regression result, the Gate E figure, and the G-class outcome by latitude band, all in that line.
- `"Domain activation BLOCKED at Part <X>"` — with the reason.

No follow-on sweep, refit or terminal search without a separate directive.

---

## 12. Note from Claude (not an instruction)

Gate E is the one I would most like to see fail loudly if it is going to fail. Everything northern in this chapter now rests on a comparison between starts, and I have already made that comparison once on a grid that could not reproduce a known answer at a known start. If the grid cannot recover 8.117 where 8.117 is achievable, I would rather the run stop than produce another table of numbers that look like evidence.

The second thing worth saying: a northern arc-1 start and a northern 7th-arc endpoint are different claims, and only the first is what TASK_030 gestured at. Part F's endpoint column exists so that the next person reading this — including me — cannot slide from one to the other.
