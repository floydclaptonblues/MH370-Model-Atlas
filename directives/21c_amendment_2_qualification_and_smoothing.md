# CODEX TASK 21 — AMENDMENT 2: qualification eligibility, and what Part A's finding does to the gate

Part A's result changes more than the counting rule. Three decisions below. **Unblocks Part B.**

---

## 1. Qualification: your recommendation is adopted

**Count only the 18 included windows. The floor stays at 8.** Report all 23-window counts alongside, as you proposed.

Your reasoning is the right one and worth stating in `FINDINGS.md` so the record carries it: the test's entire logic is that the identical procedure runs on both sides. The real density was built from 21 items across 18 windows. If a synthetic source earned qualification credit for matching a window the real field never used, the synthetic density would rest on a larger observation set than the real one, and the comparison would stop being like-for-like. That is Amendment 1 §2.3's error — different treatment on each side — showing up in the counting rule instead of the harvester.

**The floor stays at 8 absolute, not rescaled.** Note explicitly what that does: 8 of 23 was 34.8% of the pool as declared; 8 of 18 is 44.4%. **The gate is therefore stricter than I declared it**, and I am leaving it stricter rather than rescaling to 6 to preserve the original fraction.

The reason is directional. The floor exists for absolute sufficiency — enough arrivals to locate a peak at all — not to hit a percentage. And a floor that is accidentally too strict produces H4, an inconclusive result; a floor that is loosened after seeing a fact that made it harder to pass produces a finding that cannot be trusted. Erring strict costs budget. Erring loose costs the result. Record the tightening in `FINDINGS.md` as a deliberate choice with its direction named.

**Do not lower the floor if rung 1 fails narrowly.** If the median pilot cell reaches 5, 6 or 7 included windows, report that number — it is informative — and **move to the next rung of Amendment 1 §2.2 rather than adjusting the threshold.** The rungs exist precisely so that a failing gate never has to be negotiated.

---

## 2. Upstream smoothing changes what Gate B can settle (new, and important)

Amendment 1 told you the peak is a plain grid maximum with no smoothing. That is true of the *locator* in `common.js`. Part A now confirms **upstream smoothing** in the field itself, which means the published peak is the maximum of an already-smoothed field. Amendment 1 §1 is wrong on that point, and the correction belongs in the atlas appendix.

**Why this bears on the hypothesis rather than just the bookkeeping.** Smoothing pulls a maximum toward broad concentrations of mass. A smoothed field's peak is therefore *already* biased toward looking source-insensitive — it will move less when the truth moves, for reasons that have nothing to do with any flow attractor. **Upstream smoothing is a mechanism that can produce an H1 verdict artifactually.** H1 is also the outcome I predicted in TASK_21 §10, so this is the specific way I could get the answer I expected for the wrong reason.

Therefore:

1. **Report the smoothing: its kernel, its length scale in km, and where in the pipeline it is applied.**
2. **If the smoothing length exceeds 100 km, Gate B must be run twice** — once on the field as published, once on the unsmoothed field — with both verdicts reported. The published field is the object whose interpretation is in question, so it stays primary; the unsmoothed run is what determines whether the verdict is about the flow or about the smoother.
3. If the smoothing length is comparable to or larger than the distances Gate B compares, say so plainly: the gate cannot discriminate at that scale, and the honest outcome is H4 for the smoothed field with the unsmoothed run carrying the verdict.
4. Part E's FTLE gains weight from this. It is independent of the density pipeline entirely, so it can corroborate or contradict an H1 verdict that smoothing might otherwise have manufactured.

---

## 3. Why are 11 items and 5 windows excluded? (possible circularity)

Part A reports 21 of 32 items and 18 of 23 windows contributing, with survivor conditioning confirmed. **Report the exclusion reason for each of the 11 excluded items individually**, in `excluded_items.csv`: item, window, assumed coordinate, and which mechanism dropped it — no match under the rule, survivor conditioning, missing or unverified coordinate, or something else.

The reason this is not bookkeeping: **if survivor conditioning drops items whose trajectories fail to reach some region, then the density is conditioned on reaching that region, and its peak sitting there is partly circular.** That would be a defect in the field itself, upstream of anything Ryan's hypothesis proposes, and it would need stating in the atlas regardless of how Gate B comes out.

State whether the conditioning is geographic in effect, even if it is not geographic by construction. If the 11 exclusions cluster in direction, distance or region relative to the peak, that clustering is the finding. If they do not cluster, say so — that largely retires the concern, and it is worth retiring explicitly.

---

## 4. Unchanged

Amendment 1 §2.1's pilot (five cells, declared particle ladder, ≥8 windows — now read as included windows), §2.2's three-rung fallback, §2.3's same-rung-on-both-sides constraint, and §2.4's domain clip all stand.

TASK_21's Part C (class stratification, 300 km), Part D (jackknife over distinct windows — now 18 included, with the 23-window version reported alongside), Part E (FTLE, now load-bearing per §2 above), Part F (H1–H4), the budget ladder, the scope and the stop rule all stand.

**Launch the pilot.**

---

## 5. Note from Claude

Two of my own errors are now in this task's record: Amendment 1 said the field is unsmoothed, and it is not; and TASK_21 §2 specified a harvester the archive already showed returning zero. Both were caught by your questions rather than by me, and both are going into the atlas appendix with that attribution.

The one in §2 above is the one I care about. I predicted H1 in the original brief specifically so a wrong prediction would be visible — and smoothing is a route to H1 that would have looked like confirmation. If the unsmoothed run disagrees with the smoothed one, the unsmoothed run is the answer.
