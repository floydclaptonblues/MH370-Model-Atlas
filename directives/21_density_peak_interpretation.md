# CODEX TASK 21: what the reverse-drift density peak actually is

Authorized by Ryan. Register as the next unused DIRECTOR number. Write to `run2/density_peak_interpretation_001/`, new suffix if occupied. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results.

Standing rules, in force throughout:

- **No parameter is ever tuned toward any source region, any arc, or any flight path.** This task tests an interpretation; it does not search for a source.
- Every gate below is declared before the run. A failed gate is reported as failed, not widened or reinterpreted.
- Label uncertainty and assumptions. Keep the appendix of failed hypotheses and the audit trail.
- Use only real data from the project's files. Where something is missing or unverified, say so in those words.
- **B0 stays frozen.** No refit, no new forcing, no changed matching rule, no new wind-slip value. This task runs the existing configuration and asks what its output means.
- **Nothing from the satellite branch enters.** No arc, ring, candidate, endpoint or contact coordinate is read — the twelve TASK_022 contacts above all. The branches were deliberately separated and stay separated.
- Nothing large leaves the Windows machine. Summary CSVs, small gridded text and PNGs only.

---

## 0. The hypothesis under test

**This hypothesis is Ryan's and should be attributed to him in `FINDINGS.md`.** His words: the density peak may be *"better representative of where the debris cluster separated on its paths to other places"* than of where it originated.

Why it is dynamically serious rather than loose. Reverse drift integrates backward in time, and backward trajectories accumulate on sets that attract in backward time. A set that attracts in backward time repels in forward time, and a forward-repelling set is precisely one where initially co-located particles diverge and go to different destinations. So a reverse-drift density peak is, by construction, a candidate location for where a tight cluster split up — and a flow feature sits where the flow puts it, independent of where the debris actually started.

If that is what the peak is, it carries **less** source information than has been assumed, not more, and it supplies a mechanism for TASK_016's null: estimating a source means integrating backward *through* a divergence zone, where separation grows rather than shrinks. A mode spread of 675 to 1,914 km is what that looks like.

This task determines which it is. **It does not nominate a source region**, and no part of it may be read as doing so.

---

## 1. Part A — state the object precisely

Before testing anything, pin down exactly which density field is under examination. Report in `object_spec.md`:

1. The file and function that produce the reverse-drift density field shown in the atlas, and the exact B0 configuration used (RK4 step, K, boundary handling, currents product, wind product, Stokes treatment, wind-slip rule, class set, land mask).
2. Which items contribute: the item count, the distinct date-window count, and whether the field uses the primary matching rule (first land hit within 100 km of the assumed coordinate inside the exact MOT interval, zero beaching delay) or something else.
3. The beaching-delay assumption baked into that field, stated explicitly. Every test below runs under the **same** delay assumption as the field it is testing; say which that is.
4. The peak location as currently computed, with the method used to locate it (grid maximum, kernel-smoothed maximum, contour centroid — say which, and the smoothing length if any).
5. How many of the contributing coordinates are `ASSUMED_GEOCODE`, and confirm whether the Saint-André coordinate — which did not verify under TASK_014 — contributes to this field.

**The peak location from item 4 is recorded and then set aside.** It must not influence the synthetic source grid in Part B. Biasing that grid toward the existing peak would make the invariance test meaningless.

---

## 2. Part B — source invariance (GATE B, the decisive test)

### 2.1 Construction

Choose synthetic source cells on a **regular grid spanning the model domain**, at fixed spacing, **independent of the observed peak's location**. State the spacing and the cell list before running. Include cells deliberately far from any previously discussed region — the test needs widely separated truths to have any power.

For each synthetic source cell `S_i`:

1. Release particles at `S_i` at the crash epoch, with the same class mix (C0–C3) and the same per-class slip rule as B0.
2. Forward-integrate under B0 across the full period.
3. **Harvest synthetic finds using the identical matching rule the real field uses.** For each real find — its assumed coordinate and its exact MOT interval — record whether any synthetic particle from `S_i` satisfies that match, and which class it was.
4. Feed the resulting synthetic arrival set into the **identical** reverse-drift density procedure, unchanged, and locate its peak by the same method Part A item 4 reports.

### 2.2 What is reported per source cell

`source_invariance.csv`, one row per `S_i`: cell coordinates; number and fraction of the 23 distinct date windows matched; number of items matched; class breakdown of matches; the reverse-drift peak location; distance from that peak to `S_i`; and whether the row qualifies for the comparison set.

**Qualification: a source cell enters the comparison only if it matches at least 8 of the 23 distinct date windows.** Declared now. Cells below that are reported but excluded, with their match counts shown, because a peak built from three arrivals is not comparable to one built from twenty.

### 2.3 The gate

Over the qualifying set, compute:

- `peak_spread` — the maximum pairwise great-circle distance between reverse-drift peaks.
- `source_spread` — the maximum pairwise great-circle distance between the true source cells.
- `ratio = peak_spread / source_spread`.
- `median_peak_to_truth` — median distance from each peak to its own source cell.

**GATE B, declared in advance:**

| outcome | criterion | meaning |
|---|---|---|
| **FLOW-DOMINATED** | `ratio < 0.25` | The peak barely moves when the truth moves a long way. It is a circulation feature. Ryan's reading is confirmed, and the peak carries no usable source information. |
| **SOURCE-TRACKING** | `ratio > 0.75` **and** `median_peak_to_truth < 800 km` | The peak follows the truth. Ryan's reading is retired for this object. |
| **PARTIAL** | anything between, or a split verdict | Report the numbers and say plainly that the peak is a mixture. |

The 800 km figure is TASK_016's own recovery threshold, reused deliberately rather than chosen fresh. The 0.25 and 0.75 ratio bounds are declared thresholds fixed before the run; **report the raw distances alongside them** so a reader can apply different ones.

### 2.4 A separate quantity, reported but not used to select anything

Part B produces, as a by-product, a map of **which source cells can reproduce the observed find pattern at all** — the match-fraction field from §2.2. Report it as `reachability_map.csv` and as a PNG.

**Label it reachability. It is not a likelihood, not a posterior, and not a source estimate.** It must not be converted into one, normalised into one, or described as one. TASK_016 already ran the source-estimation question under a preregistered recovery gate and returned no determinable region; re-reading a reachability map as a source map would be that question again without its gates. If the reachability field turns out to be informative, that is a finding to report and to task separately, not to act on here.

---

## 3. Part C — is the peak a windage mixture? (GATE C)

Items span classes C0–C3 with different wind slip, floored at 1.2%. Differential windage separates a cluster even in a flow with no divergence at all, purely by giving items different effective velocities — a competing explanation for the western Indian Ocean spread that needs no separation node.

Recompute the real reverse-drift density **separately for each class**, holding everything else fixed, and report each class's peak and particle count in `class_peaks.csv`.

**GATE C:** if the maximum pairwise distance between class peaks exceeds **300 km**, windage is doing material separating, and the single all-class peak is a mixture of class-specific peaks rather than a location. Report the distances whatever the verdict. 300 km is a declared threshold; the raw matrix is published.

Note in `FINDINGS.md` that the 1.2% floor was fitted to ERA-Interim winds, BRAN2015 currents and a CAWCR wave hindcast — products B0 does not use — with no transfer validation. Any class-dependence found here inherits that.

---

## 4. Part D — how stubborn is the peak? (reported, no gate)

Jackknife over the **23 distinct date windows**, not the 32 items. Items sharing a window are not independent, and resampling items would be pseudo-replication.

1. Leave-one-window-out: 23 runs, report each peak's displacement from the full-set peak.
2. Leave-half-out: a declared number of random half-partitions of the windows, report the displacement distribution.
3. Drop the unverified Saint-André coordinate alone, if Part A found it contributes, and report the displacement.

Report whether displacement is structured — concentrated on particular windows, classes or regions — rather than scattered. A peak dominated by a flow attractor should be stubborn under this; one carrying real source information should degrade in a way tied to which windows were removed. **This is read as corroboration alongside Gate B, never on its own** — both a flow feature and a well-constrained source signal can be stubborn, so it discriminates only in combination.

---

## 5. Part E — is the peak sitting on a separation surface?

Compute the **finite-time Lyapunov exponent field** over the model domain under B0, at integration times `T ∈ {30, 90, 180}` days, both backward and forward in time from the crash epoch.

Report, in `ftle_summary.csv` plus one PNG per `T`:

- the FTLE field on a stated grid (coarsen if needed, and say by how much);
- ridge locations by a stated extraction method;
- the distance from the observed density peak to the nearest backward-time FTLE ridge, at each `T`;
- whether that distance is small compared with the ridge spacing in the region.

A backward-time FTLE ridge *is* an attracting structure in backward time and a separation surface in forward time, so this tests Ryan's sentence directly rather than by inference. If the peak sits on a ridge, the interpretation has a named dynamical object behind it.

**Caveat to carry into `FINDINGS.md`:** this is B0's FTLE field, not the ocean's. B0 sets Stokes drift explicitly null and floors wind slip at 1.2% from mismatched products, and both affect divergence structure. The field describes the model that produced the density map — which is the right object for this test, and is not a claim about the real circulation.

If FTLE over the full domain is unaffordable, coarsen the grid before dropping an integration time, and report the grid actually used.

---

## 6. Part F — outcomes, declared in advance

In `FINDINGS.md`, state which of these the run produced. More than one may apply.

**H1 — the peak is a circulation feature.** Gate B returns FLOW-DOMINATED, and preferably the peak sits on a backward FTLE ridge. Then Ryan's reading is confirmed: the peak marks where a cluster would separate, not where it began, and the atlas must stop presenting it as source-adjacent. TASK_016's null gains a mechanism rather than remaining a bare negative.

**H2 — the peak carries source information.** Gate B returns SOURCE-TRACKING. Then Ryan's reading is retired for this object and should be recorded as retired, with the peak's source content stated together with its spread. Note that the flow could still have a separation node; H2 only says the peak is not purely it.

**H3 — the peak is a windage mixture.** Gate C exceeds 300 km. The single all-class peak is then not a place, independent of H1 and H2, and every figure showing one peak needs re-captioning.

**H4 — inconclusive.** Too few source cells qualified under §2.2, or FTLE could not be computed at a usable resolution. State exactly what was insufficient and what would fix it. Do not substitute a weaker test and report it as this one.

---

## 7. Budget

Part B is the expensive part: one forward integration per synthetic source cell across the full period, plus one reverse-drift density per qualifying cell. Estimate and report wall time before running, with the cell count and particle count stated.

If the estimate exceeds 10 hours, cut in this declared order and no other:

1. Particles per class per source cell, to a declared floor.
2. FTLE grid resolution in Part E.
3. FTLE integration times, dropping 30 days first.
4. Synthetic source grid spacing — **coarsened uniformly, never trimmed toward or away from any region.**
5. Stop and ask.

The jackknife in Part D and the class split in Part C are cheap and are not on the ladder.

---

## 8. Scope

- No refit of B0, no new calibration, no B1 revival.
- No new forcing product and no change to the existing drift forcing.
- No satellite-branch file is read at any point.
- No source region is nominated, ranked, or recommended, by this task or in its outputs.
- If a part is blocked, report the block and stop at that part.

---

## 9. Stop rule

Deliver Parts A through F and stop. Final line, one of:

- `"Density peak interpretation complete"` — with the Gate B verdict, the ratio, the Gate C maximum class distance, and the H-class outcome in that line.
- `"Density peak interpretation BLOCKED at Part <X>"` — with the reason.

No follow-on source estimation without a separate directive, whatever the reachability map looks like.

---

## 10. Note from Claude (not an instruction)

Gate B is the one that matters, and the construction detail that makes or breaks it is in Part A item 4 and Part B §2.1: the synthetic source grid must be laid out without reference to where the observed peak is. If the grid is centred on the peak, every synthetic peak lands near every synthetic truth for trivial reasons and the test returns SOURCE-TRACKING by construction. I would rather the grid be awkwardly placed than conveniently placed.

The outcome I expect is H1, possibly with H3 alongside. I am recording that expectation here so that it is on the record before the numbers exist, and so that if the run returns H2 it is visible that I was wrong rather than quietly reconciled. My prediction has no weight in how the gates are evaluated.
