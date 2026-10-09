# CODEX TASK 21 — AMENDMENT 3: the exclusions, the budget, and how to read two Gate B verdicts

Pilot continues. Four items, none of which stops it.

---

## 1. Budget: stop the pilot at the first rung that clears

**Stop the ladder as soon as a rung reaches 8 included windows at the median pilot cell.** Do not complete the remaining rungs.

Your 5.1-hour allowance assumes the full ladder, which is only needed if no rung clears. The pilot's purpose is to find the *smallest* sufficient particle count, so the first clearing rung answers it and every rung after that is spend for nothing. If the 6-minute first rung clears at 100 particles per class, the pilot is done in six minutes.

Note the 10-hour ceiling in TASK_21 §7 covers the **whole task**, pilot and full source grid together. If the pilot does consume 5.1 hours — which now means no rung cleared — the grid will not fit behind it and the §2.2 fallback rungs apply rather than a grid at reduced particle counts.

---

## 2. The exclusions: one concern retired, a different one opened

**Retired.** Amendment 2 §3 asked whether survivor conditioning drops items whose trajectories fail to reach a region, which would make the peak's position partly circular. Identification-based exclusion is not that mechanism. **That circularity is retired — say so explicitly in `FINDINGS.md`**, because a concern raised on the record should be closed on the record.

**Opened.** Ten of the eleven are Madagascar items. The mechanism is not geographic but **the effect is**, and sharply: the density rests on a find set from which one entire region has been almost wholly removed, while the collection it is drawn from contains those items. Identification status is also not geographically uniform in its own right — confirmation effort and success differ by jurisdiction — so the included set's geography is partly a map of where items got confirmed.

That is a detection-bias problem, the same family TASK_016 handled with its D0–D3 models and flagged D3 as CIRCULAR. It is not a reason to include unconfirmed identifications in the primary analysis. It is a reason to measure how much the peak depends on excluding them.

**So add one run, real side only:**

Recompute the real reverse-drift density over **all 32 items and 23 windows**, procedure otherwise identical, and report its peak alongside the 21/18 peak. Deliver as `exclusion_sensitivity.json`.

- **Primary remains the 21/18 set.** The all-32 variant is labelled as including unconfirmed identifications and is never presented as the better estimate.
- **Declared in advance: if the peak moves more than 300 km** between the two item sets — the same threshold as Part C — then the published peak is materially a product of confirmation status, and that belongs in the atlas whatever Gate B returns.
- **This variant does not enter Gate B.** It is compared only against the 21/18 real peak: same procedure, same rung, one difference. Feeding it into a synthetic comparison would be the §2.3 cross-rung error. Gate B stays on 21/18 on both sides.

**Also report plainly: how many Madagascar items remain in the included 21.** If the answer is zero, say so — the atlas drift map plots Madagascar find sites beside a density that no Madagascar item informs, and that needs stating on the figure.

---

## 3. Part D gains a required row

Madagascar's near-total absence makes the jackknife more informative than when I wrote it. In Part D, **report the leave-one-out displacement for each remaining Madagascar item individually**, if any remain, rather than only within the distribution. With that region reduced to one or two items, a single item may be carrying a whole region's constraint, and a distribution summary would hide that.

---

## 4. How to read two Gate B verdicts, declared before they exist

Smoothing exceeds 100 km, so both runs are required. State now how they combine, so the rule is not chosen after seeing which way they fall:

- **They agree** → that is the verdict, and the smoothing is not load-bearing. Report it as such.
- **Smoothed says FLOW-DOMINATED, unsmoothed says SOURCE-TRACKING** → **the published peak is source-insensitive because of its own smoothing.** That is a defect in the figure, not a property of the ocean. H1 would be false as physics and true as a description of the published object, and the atlas must say the smoothing, not the circulation, is what makes that peak stable. This is the case I flagged in Amendment 2 §2 as the route by which I could get my predicted answer for the wrong reason, and it is the one to state most carefully.
- **Smoothed says SOURCE-TRACKING, unsmoothed says FLOW-DOMINATED** → the physics is flow-dominated and the smoothing is adding apparent source sensitivity. Unsmoothed carries it.
- **Either returns H4 at a scale the smoothing swamps** → report H4 for that field specifically, not for the task.

The general rule: **the unsmoothed run answers what the peak represents physically; the smoothed run answers what the atlas's published figure represents.** Both are reported, each labelled with which question it answers, and neither is described as the result on its own.

---

## 5. Unchanged

Qualification at 8 of 18 included windows with 23-window counts reported alongside. Amendment 1 §2.2's rungs and §2.3's same-rung constraint. §2.4's domain clip. Parts C, D (plus §3 above), E, F, the scope and the stop rule.
