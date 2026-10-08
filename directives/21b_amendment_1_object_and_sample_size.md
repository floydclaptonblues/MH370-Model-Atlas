# CODEX TASK 21 — AMENDMENT 1: which density field, and the sample-size problem

Two things. The first answers your question. The second is a defect in TASK_21 §2 that your question led me to find, and it matters more.

---

## 1. The density field, identified exactly

**There is only one.** The atlas renders it in two panels, both reading the same file, so the ambiguity in my wording was real but the object is not.

**Canonical file:** `data/density.json` in `floydclaptonblues/MH370-Model-Atlas`, at commit `e59d870`.

```
note      : "probability_mass per 0.5 deg cell, cells >1e-6 only"
cell_deg  : 0.5
cells     : 926 entries, each [lat, lon, probability_mass, hpd_flag]
mass sum  : 0.999797114
extent    : lat -40.25 .. -26.25, lon 48.25 .. 98.25  (retained cells only)
hpd_flag  : 0 = outside, 1 = inside 90%, 2 = inside both 50% and 90%
```

**The two panels, both from that file:**

| page | exact title / label |
|---|---|
| `drift.html` | card headed **"Combined reverse-drift density (baseline, assigned classes)"** |
| `map.html` | switchable layer labelled **"Reverse-drift density"**, with **"Density 90% HPD cells"** as its HPD toggle |

**The peak, and how it is located.** Plain grid maximum of `probability_mass`, **no smoothing of any kind**. The locator is in `common.js`, layer `MH.L.density`:

```js
const pk = D.cells.reduce((a,b) => b[2] > a[2] ? b : a);
```

That returns cell `[-35.25, 55.75, 0.02956, 2]` — centre **35.25°S, 55.75°E**, mass 0.02956, inside both HPD regions. This reproduces the value the atlas text already quotes, and TASK_21 Part A item 4 is therefore answered by "grid maximum, no smoothing".

**But `density.json` is a published view, not the authoritative field.** It is thresholded at `>1e-6`, so 926 cells are what survived the cut, not what the pipeline computed. **Part A must identify the run that produced it and use that run's unthresholded field**, then confirm the unthresholded grid maximum still falls in the `-35.25, 55.75` cell. If it does not, say so — that is a finding about the published figure, and the atlas would need correcting.

**Two further items for Part A's spec, which my original §1 did not ask for and should have:**

5. **Survivor conditioning.** The atlas states the western focus comes partly from "survivor conditioning". Report exactly what conditioning is applied — which particles are retained, on what criterion — because a conditioned density is not the same object as a raw backward density and the distinction bears directly on Ryan's hypothesis.
6. **Site versus window counts.** The atlas says "32 items at 21 sites"; TASK_021 §4 directs the jackknife over **23 distinct date windows**. Those are different quantities — 21 is spatial, 23 is temporal — and both appear in the record. Confirm both, and keep the jackknife on windows as written.

---

## 2. The defect: a previous version of Gate B already returned zero

While locating the field I read this, in the atlas drift diagnostics page, from the earlier synthetic work:

> "All five fixed synthetic sites matched no items under either rule at this sample size, so no synthetic observation set formed and no reverse peak was computed for them."

**That is TASK_21's Gate B, already attempted, returning nothing.** My §2.1 instructs you to harvest synthetic finds "using the identical matching rule the real field uses" and my §2.2 sets a floor of 8 matched windows out of 23. Against a rule that has already produced **zero** matches for five synthetic sites, every cell in the grid fails qualification, Gate B returns H4, and the run burns its budget establishing something the archive already records.

The primary matching rule is strict by design — first land hit within 100 km of an assumed coordinate, inside the exact MOT interval, zero beaching delay. Three simultaneous conditions. That strictness is appropriate for the real finds; as a harvester for synthetic particles it is close to a measure-zero event.

So §2 is amended as follows.

### 2.1 A pilot runs first, and it gates the rest

Before the full source grid, run a pilot on **five source cells only**, drawn from the regular grid (not chosen for promise), at increasing particle counts: a declared ladder, each rung roughly 4× the last. At each rung report, per cell: matched items, matched distinct windows, and wall time.

**GATE B-PILOT.** Report the smallest particle count at which a median pilot cell reaches **≥ 8 matched distinct windows** under the strict rule.

- If that count is affordable across the full source grid within the 10-hour budget: proceed with the strict rule, and §2.2–2.3 stand unchanged.
- If it is not affordable, or the match count does not rise toward 8 at all as particles increase: **the strict rule cannot serve as a harvester**, and you move to the fallback ladder below. Report the pilot numbers either way — a structurally zero match rate is itself a reportable property of the matching rule.

### 2.2 Fallback ladder, declared in advance and in this order only

1. **Strict primary rule** — first land hit within 100 km, exact MOT interval, zero delay.
2. **Kernel-weighted arrival**, using TASK_016's own published values rather than new ones: half-normal spatial kernel at `s ∈ {50, 100, 200}` km and exponential delay at `m ∈ {30, 90, 180}` days. Report every configuration, not a chosen one.
3. **Continuous coastal arrival density** — compare the synthetic arrival distribution along the coast against the observed find distribution as distributions, with no thresholding at all. State the comparison statistic before computing it.

Do not invent a fourth rung. If rung 3 also fails, report H4 with the pilot numbers.

### 2.3 The constraint that makes or breaks this — read it twice

**Whichever rung is used, the identical rung must be applied to the real finds when computing the real density the synthetics are compared against.** Build the comparison from the same rule, the same kernel, the same delay, the same statistic.

A kernel-harvested synthetic peak compared against a strictly-harvested real peak is not a test of anything. That is the same error as comparing a coarse-grid χ² against a refined one in TASK_030, in different clothing, and I have made it once already. Every output row states which rung produced it. **Rows from different rungs are never compared.**

If a rung changes the object under test — and rungs 2 and 3 do — say so explicitly in `FINDINGS.md`: the verdict then applies to the kernel-smoothed or distribution-level field, not to the published `density.json` peak, and the atlas wording must reflect which.

### 2.4 Domain bound

The drift forcing domain is **−55 to 5°N, 20 to 115°E**. The archive records that an eastern control at 100–120°E was not run because it extends past the forcing at 115°E. **Every synthetic source cell must lie inside that domain**, and the grid is clipped to it rather than extending past it. TASK_20 extends the *flight* forcing; it does nothing for the drift forcing, and the two must not be conflated.

---

## 3. Prior art to report rather than rediscover

Two pieces of the archive already bear on Ryan's hypothesis. Report what they show in `FINDINGS.md` **before** the new results, so the new work is visibly incremental rather than presented as the first look.

**TASK_009's nulls.** Shuffled-region and random-coast nulls left the peak essentially in place: every null peak within 500 km of the original, 96.7% of shuffled-region peaks within 250 km, and the atlas's own reading is that "the western focus comes from the frozen dynamics, launch and density method and survivor conditioning, not from the find locations," with "the exact 55.75°E is not stable."

That is already evidence in the FLOW-DOMINATED direction, and it must be credited as such. But it is **not** Gate B. TASK_009 scrambled where the debris was *found*, holding the true source implicit and unknown. Gate B specifies a *known source* and asks whether the peak follows it. Insensitivity to find locations and insensitivity to source location are different properties, and only the second settles Ryan's hypothesis. State that distinction plainly rather than letting TASK_009 stand in for the new test.

**The existing mean-flow divergence figure** (`img/gyre_mean_flow.png` — mean surface speed and divergence of the mean flow, with release boxes and the reverse density peak) is prior art for Part E. Report what it already shows about the peak's position relative to mean-flow divergence.

Then note the limitation that justifies Part E anyway: **mean-flow divergence is not the same diagnostic as FTLE.** A time-averaged flow can look non-divergent while the time-dependent flow stirs strongly, and it is the time-dependent stirring that separates a cluster. Part E stands.

---

## 4. Unchanged

Part C (class stratification, 300 km gate), Part D (jackknife over 23 distinct windows), Part E (FTLE, with §3's prior art added), Part F (outcomes H1–H4), §7's budget ladder, §8's scope and §9's stop rule all stand as written.

§2.4 of the original — the reachability map fenced off as reachability and explicitly not a posterior — stands, and applies to whichever rung produced it.

---

## 5. Note from Claude

Your question was about a file path and it surfaced a dead gate. I wrote §2 specifying a harvester the archive already records as returning zero, which would have spent the budget to rediscover a known null. The pilot in §2.1 exists so that fails in minutes instead of hours.

The thing I would most like preserved through the fallback ladder is §2.3. The rungs are there to make the test runnable, and each one quietly redefines what is being tested; the only protection against that is applying the same rung to both sides and labelling every row with it.
