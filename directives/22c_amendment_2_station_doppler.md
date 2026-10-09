# CODEX TASK 22 — AMENDMENT 2: order the BFO residuals by time before sweeping anything

**This supersedes the priority of Amendment 1. Do this first; it is one table and it may make the sweep unnecessary or invalid.**

---

## 1. What the 86 km is

A displacement of the **satellite relative to the ground station**. Not the aircraft, not the arc, not the terminal event. Between 19:41:03 and 00:19:29 the satellite's range to the station falls by 82.3 km as it drifts south, which moves the BTO term by −549 µs against the −573 µs discrepancy — 95.8%, with 24 µs left over.

That part is settled. What follows is what the same displacement does in the frequency domain.

## 2. The same term, differentiated, lands exactly on the scored BFO set

The range rate of that displacement is a Doppler shift. Computed from the published state table:

| scored BFO epoch | station range rate | station Doppler, L-band | C120 z² | C120 \|residual\| |
|---|---|---|---|---|
| 19:41:03 | −0.006 m/s | 0.03 Hz | 2.901 | 7.32 Hz |
| 20:41:05 | −2.432 m/s | 12.98 Hz | 0.096 | 1.33 Hz |
| 21:41:27 | −4.648 m/s | 24.81 Hz | 0.041 | 0.87 Hz |
| 22:41:22 | −6.505 m/s | 34.72 Hz | 0.068 | 1.12 Hz |
| 00:11:00 | −8.383 m/s | 44.74 Hz | 0.052 | 0.98 Hz |

**The term spans 44.7 Hz at L-band, 102 Hz at C-band, monotonically, across exactly the five scored BFO observations**, against σ_BFO = 4.3. The window opens at the stationary point of the satellite's motion — the range rate at 19:41:03 is −0.006 m/s — and climbs steadily from there.

The BTO version of this term is the one I dropped, and dropping it cost 86 km. **Its frequency-domain twin is the quantity the project records as MISSING.** They are the same geometry seen in range and in range rate.

## 3. The test, which is one table

**Report the five BFO residuals of the northern candidate in time order. Same for C120. Nothing else is needed to decide this.**

| if the residuals are… | the explanation is | consequence |
|---|---|---|
| **unordered** — scattered within +2.6 to +6.5 with no trend against the rate column | a constant bias offset | Amendment 1's sweep is the right test; a mean of 4.55 Hz absorbs 5.60 of χ² |
| **ascending with the rate** — near 2.6 at 19:41 rising to near 6.5 at 00:11 | an error in the station-leg Doppler, **not** a bias | a scale error of 8.7% on a 44.7 Hz term plus a 2.6 Hz offset. The sweep as designed is invalid |

Five points against a regressor computed from published ephemeris, with no free parameters in the regressor, is enough to separate these.

## 4. Why this invalidates the sweep if the second case holds

**A single constant δ can absorb only the mean of a residual set. It cannot absorb structure.** If the residuals carry a monotone trend, a δ sweep will partially absorb it, report a crossing, and attribute to the bias something that belongs to the station term. Amendment 1's test would then produce a confident number about the wrong quantity.

That is the same failure as treating the station leg as a constant K in the BTO. I made it once in this task's own neighbourhood and it is worth not making twice.

## 5. The asymmetry that makes this informative either way

A scale error in the station term is **hypothesis-independent**: it contaminates every candidate's residuals identically, because the station geometry does not care where the aircraft is. So if this is the explanation, **C120's residuals must show it too.**

They appear not to. C120's four later BFO residuals sit at 0.87 to 1.33 Hz while the station term climbs 13 → 45 Hz, which is flat, not ascending. So:

- If the northern residuals ascend and C120's stay flat, no shared instrument error explains the difference, and the northern misfit is a property of that trajectory. **That strengthens the southern case rather than weakening it.**
- If both ascend, the model has a shared defect and both χ² values are structurally inflated.
- If neither ascends, it is a bias question and Amendment 1 stands unchanged.

Report which, explicitly. Do not report a crossing before this is settled.

## 6. Two honest limits

**This almost certainly is not a missing term.** The station-leg Doppler is standard, the ground station's AFC removes most of it, and C120 could not fit at all if 45 Hz were unmodelled. What §3 tests is a **second-order** error — a scale factor, an AFC assumption, a station coordinate — not an absent term. Say so in `FINDINGS.md` rather than letting the 44.7 Hz read as discovered.

**The station coordinate is mine, not the archive's.** Perth at 31.80°S, 115.887°E, supplied from general knowledge. The rate column above inherits it. A 2° error in station latitude moves the computed rate by a few per cent — small against the 8.7% scale error the second case implies, but not negligible, and it is the same unverified number the ring derivation already depends on. **The archive should carry the real coordinate**, and that is now load-bearing twice over.

## 7. One hypothesis I checked and am dropping

C120's largest BFO residual, 7.32 Hz, sits at 19:41 — precisely where the station term vanishes. An AFC tracking lag proportional to range **acceleration** would peak there and would explain it. It does not survive: acceleration varies only 2.97× across the scored set while C120's residuals vary 8.4×. Recorded here as tested and rejected so nobody re-runs it.

C120's 19:41 residual stays unexplained. It is the first handshake after the 18:25 log-on, so residual warm-up drift is a candidate — **a hypothesis, not a finding**, and not one to pursue inside this task.

## 8. Everything else holds

Amendment 1's σ_b answer (use none), the C120-based admissibility bands, the archive-internal pre-diversion diagnostic, and TASK_22 §3–§5 are unchanged. Continue the authorized flight searches. **Send the two ordered residual tables when convenient; they are cheap and they decide what the sweep is for.**
