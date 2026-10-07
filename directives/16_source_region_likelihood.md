# CODEX TASK 16: graded source-region likelihood, with a recovery gate

Authorized by Ryan. Register as the next unused DIRECTOR number and write to a new folder `task_16_source_likelihood/` beside the Task 12 outputs. Preserve all historical code, inputs and outputs. Frozen B0 physics, the existing particle data and every Task 10 to 14 record are read-only and are not edited.

## 0. What this task is for, and the one rule that governs it

The binary matching rule (first land hit within 100 km of an assumed coordinate, inside an exact MOT interval, zero delay) has produced no source region, and the permutation null says its best cells are indistinguishable from a shuffle. This task replaces hit-counting with a likelihood over release cells, using an explicit observation model, and asks whether a source region can be resolved at all.

**The governing rule: the method must be shown to work on synthetic collections with known sources before it is applied to the real finds.** Part B is a gate. If it fails, Part C does not run, and "this data cannot localise a source" is the result.

Forbidden throughout: tuning any observation-model parameter to the real 32 items, or to any result computed from them; using the 7th arc, any flight path, candidate position, search area or TASK_022 contact anywhere, including as a plot overlay, a prior, a sanity check or a validation step; changing B0 physics, the particle data, or any frozen input; re-running any drift integration; selecting a preferred detection model after seeing its answer; reporting a posterior without its recovery-gate result attached.

No contact coordinate, endpoint or arc distance from the satellite branch enters this task. The two branches stay separate.

## 1. Part A — the observation model, declared before any run

Build the likelihood from the existing stage-2 particle data for boxes B, W and M. For a release cell `c` and item `i`, the per-item likelihood is the fraction of that cell's particles whose landing satisfies a graded version of the match, replacing the three hard cuts:

**Spatial term.** Replace the 100 km hard radius with a kernel on great-circle distance from the item's assumed coordinate to the landing position. Use a half-normal kernel with scale `s`. Run the whole task at `s` in {50, 100, 200} km and report all three. These stand in for both the find-coordinate uncertainty and the model's own position error; they are not a measurement.

**Temporal term.** Replace the exact interval and zero delay with a landing-to-discovery delay distribution. The item is discovered in its stated interval; the landing may precede it by a delay drawn from an exponential with mean `m`. Run at `m` in {30, 90, 180} days and report all three. For items whose interval is itself long (25, 23, 28, 29, 31, 32, 30), integrate over the interval as stated; do not narrow it.

**Detection term.** Weight each landing by the probability that a landing there would have been found. Run under **four declared variants**, all reported, none selected:

- `D0` uniform: every coast segment equally likely to yield a find. This is the current implicit assumption and is almost certainly wrong.
- `D1` region-coarse: a weight per coastal region (Réunion, Mauritius/Rodrigues, Madagascar, Mozambique, Tanzania, Kenya, Somalia, South Africa, Australian west coast, other), set from a declared accessibility proxy, not from where finds occurred.
- `D2` population-proxy: a weight from a coastal population or night-lights proxy if one is already present in the project files. If none is, mark `D2` UNAVAILABLE and do not acquire data.
- `D3` found-coast-only: weight one on coastal regions where any item was found, zero elsewhere. This variant is deliberately circular and is included as an upper bound on how much the detection term can do; label it CIRCULAR on every output row.

Document every weight and its basis in `detection_models.csv`. Weights must not be derived from the number of items found in a region.

**Combination.** Per-cell log-likelihood is the sum over the 32 items of log of the per-item probability, with a floor for zero-probability items that you declare and record. Report the per-item contributions, not just the total, so a cell carried by one item is visible. Compute for each class C0 to C3 separately and for the assigned mixture. Normalise across cells within each box to a posterior under a uniform prior over cells, and state that the prior is uniform and that the three boxes are not a complete partition of the ocean.

The full grid is 3 spatial scales x 3 delay means x 4 detection variants = up to 36 configurations per class per box. Record the grid. If that exceeds budget, reduce to the three scales x {90 d} x all four detection variants and say so.

## 2. Part B — the recovery gate (runs before Part C)

Using the same particle data and the same machinery, generate synthetic collections from known source cells and test whether the posterior recovers them.

Procedure, per trial: choose a true cell at random from box B; draw 32 synthetic items from that cell's own landed particles; assign each synthetic item a discovery region and a discovery interval generated through the **same** observation model being tested, including the detection weights; then run the full Part A likelihood on that synthetic collection, with the true cell unknown to the scoring code.

Run at least 200 trials per configuration, or the largest complete number the budget allows. Use C0 as the primary class, as pre-declared elsewhere.

**Preregistered gate, fixed now, before any result is seen.** A configuration passes if both hold:

1. The true cell falls inside the smallest region containing 50% of posterior mass in **at least 60%** of trials.
2. The **median** great-circle distance from the posterior mode to the true cell is **under 800 km**.

These thresholds are Claude's, chosen before any output exists, against a box about 1,830 by 1,760 km. They are not derived from any result. Do not change them. Report the achieved values whatever they are.

Also report, for context and not as part of the gate: the distribution of mode-to-truth distance, the posterior entropy, and how often the posterior is effectively flat.

**If no configuration passes, stop.** Deliver Part B, write `recovery_gate.csv` and the finding that the method cannot resolve a source from this data under these assumptions, and do not compute any posterior over the real 32 items. Do not relax the gate, add configurations, or substitute an easier synthetic design.

## 3. Part C — the real collection (only if a configuration passed)

For each configuration that passed the gate, and only those, compute the posterior over release cells for the real 32 items. Deliver:

- `source_posterior_by_cell.csv`: box, class, configuration, cell, latitude, longitude, log-likelihood, posterior mass, the per-item contributions, and the gate result for that configuration carried on every row.
- Maps of the posterior for each passing configuration, with the 50% and 90% mass regions drawn. No arc, no candidate, no search area, no contact on any map.
- `configuration_spread.csv`: how far the posterior mode moves across spatial scale, delay mean and detection variant. If the mode moves further between configurations than the width of any single posterior, say so plainly: that means the answer is set by the assumptions rather than by the data.
- A separate statement of how much of the result is carried by the `D3` circular variant versus the others.

Report a flat or multi-modal posterior as flat or multi-modal. Do not report a single best cell. Do not compare any result with the arc, and do not characterise any region as consistent or inconsistent with any flight model.

## 4. Part D — what the answer depends on

For the passing configurations, report:

- the number of items contributing non-negligible likelihood, and which items contribute nothing under every configuration;
- the posterior recomputed with the seven long-window items removed, and with the five items sharing one window counted once;
- the posterior recomputed with item 4's window treated as "ashore by 23 December 2015" instead of its stated one-day window, as a declared sensitivity only, with the original retained;
- the effect of the known eastward transport bias: shift every landing position west by 150 km and by 300 km as two crude declared sensitivities, and report how far the posterior mode moves. This is not a bias correction and must not be described as one.

## 5. Verification and deliverables

- Confirm the particle data and all Task 10 to 14 outputs are unchanged, by hash comparison, and report the count.
- Confirm the Part A code reproduces the existing binary match exactly in the limiting case (`s` small, delay zero, detection uniform, hard interval). Report the largest discrepancy. If it does not reproduce, stop and report that.
- Confirm no arc, flight-path, candidate or contact file was read, by listing every input actually opened.
- `NOTES.md`: assumptions, every declared parameter and its basis, failed approaches, seeds, hashes, runtime, and an audit trail from each number to its source.
- `FINDINGS.md`: the gate result first, then the posterior if one exists, then what it rests on.

## 6. Stop rule

Deliver the gate and, if it passed, the posterior. Then stop. No further configurations, no relaxed thresholds, no arc comparison, no search recommendation, no automatic follow-on. Write "source-region likelihood complete" when Parts A, B and, if reached, C and D are done — including when the gate failed. A failed gate is a complete result, not a partial one.

## 7. Notes from Claude (not instructions)

- The detection term is the largest new assumption in this task and possibly the largest unmodelled effect in the whole drift analysis. Every item was found on populated, accessible coast and none on uninhabited shoreline. Until that is in the model, landing counts and find counts are not the same quantity. `D3` is included to bound how much it can do, and it is circular by construction, which is why it is labelled on every row.
- I expect the gate to be the hard part. If the method cannot recover a known source from its own synthetic data, that is a real and publishable result about this dataset, and it is more valuable than a posterior nobody should trust.
- If the posterior mode moves further between configurations than any single posterior is wide, there is no source region here, only a map of our assumptions. Say so in those words.
- Nothing in this task can locate the aircraft. A posterior over release cells is conditional on B0 transport, assumed find coordinates, assumed slip classes and a declared detection model, every one of which is unvalidated.
