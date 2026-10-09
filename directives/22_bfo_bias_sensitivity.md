# CODEX TASK 22: does the north–south preference survive the BFO bias?

Authorized by Ryan. Register as the next unused DIRECTOR number. Write to `run2/bfo_bias_sensitivity_001/`. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results.

Standing rules, in force: **no parameter is ever tuned toward the 7th arc or toward any flight path**; gates declared before the run and reported as failed rather than adjusted; uncertainty and assumptions labelled; only real data from the archive; nothing crosses into the drift branch.

---

## 0. Why this task exists

TASK_033 produced the project's first clean northern candidate: χ² 18.27 at 31.87°S, 95.36°E, against 7.92 for the 34–36°S control, at equal free parameters. Δχ² = 10.35, a likelihood ratio of 177:1 for the south **if the error model holds**.

All five of the northern fit's BFO residuals are positive, +2.6 to +6.5 Hz against σ_BFO = 4.3. A common offset in the BFO bias produces exactly that signature.

The amount a single free common offset removes from χ² is exact and depends **only on the mean residual**, not its spread:

> absorbed = n·r̄² / σ² = 5·r̄² / 18.49

| mean BFO residual | absorbed | Δχ² becomes |
|---|---|---|
| 2.6 Hz | 1.83 | +8.52 |
| 4.55 Hz | 5.60 | +4.75 |
| 6.00 Hz | 9.73 | +0.62 |
| **6.19 Hz** | **10.35** | **0.00** |
| 6.5 Hz | 11.43 | −1.08 |

The observed residuals span the range across which this verdict flips from *south wins comfortably* to *tie*. **The bias is not a footnote on this result; it is the result.** And the closing report already lists the BFO bias calibration epoch as **MISSING, with a CONFLICT on its locator** — this is that unresolved item arriving at the one place it decides something.

---

## 1. The design constraint that makes or breaks this

**The BFO bias is one physical constant of one terminal. It is not a per-hypothesis free parameter.**

Fitting δ separately for each candidate — letting the northern fit choose 4.5 Hz while the control keeps 0 — would manufacture a northern result out of a nuisance parameter. That is the TASK_030 error in a new costume: giving one side a freedom the other does not have.

So the test is a **sweep, not a fit**, following the TASK_026 κ methodology:

1. Choose a grid of δ across a stated range, **δ = −8 to +8 Hz in 0.25 Hz steps**, symmetric about zero so the grid itself carries no preference.
2. At **each** δ, apply the same δ to **every** BFO term of **both** hypotheses.
3. Re-minimise both, each over its own command parameters, at that δ.
4. Report χ²_north(δ), χ²_south(δ) and Δχ²(δ) = north − south.

**Do not nominate a preferred δ.** The deliverable is the curve, not a value.

---

## 2. Gates, declared now

**G-A. Crossing.** Report whether Δχ²(δ) reaches zero anywhere in the swept range, and at what δ. If it does, report that δ and state plainly that the north–south preference is conditional on the bias being wrong by that amount in that direction.

**G-B. Defensibility of the crossing.** A crossing only matters if that δ is physically admissible. Report, from the archive and from the external record:
- any documented value or uncertainty for this terminal's BFO bias;
- the warm-up offset envelope already adopted elsewhere in the project (17 to 136 Hz) and whether it bears on cruise BFO at all;
- whether a δ of the crossing magnitude would break any other fit in the archive — above all **C120, whose χ² = 8.117071226374 is frozen**. Re-score C120 at the crossing δ and report the change.

If a crossing requires a δ that visibly breaks C120 or contradicts a documented bound, say so: the crossing exists numerically and is excluded physically.

**G-C. Sign structure.** At δ = 0, report the sign pattern of all five BFO residuals for **both** hypotheses. A southern fit with mixed signs and a northern fit with five positives is itself evidence; five-of-five one-signed has probability 1/16 under a correct model. Report the equivalent count for the control.

---

## 3. Things to fix in the TASK_033 reporting

**3.1 The 30–32°S bin minimum is 16.85, not 18.27.** If the search found 16.85 at 32.0°S within the 30–32°S bin, then that bin's best known value is 16.85 and the 18.27 point is **the best non-edge point found**, not the bin optimum. Report both, with 18.27 labelled as the clean interior candidate and 16.85 as the bin's actual best-known. Ryan is right that the 16.85 should not be read as a better northern result — it is 23 µs inside the engine-loss window, below your own numerical error — but that argues the bin is unconverged, not that 18.27 is its minimum.

**3.2 The 30–32°S bin is barely interior.** 31.87°S sits 0.13° — about 14 km — from its 32.0°S edge. Combined with 3.1, the honest reading is that this bin also leans south and is being held, not that it found a free interior optimum. Say so rather than describing it as unpinned without qualification.

**3.3 The 20:41 miss is not unusual.** −51 µs is 1.76σ against σ_BTO = 29.0. For the worst of four BTO residuals, **P(worst > 1.76σ) ≈ 28%**. That is an ordinary draw, not evidence against the northern fit. Remove it from the list of reasons the ring timings favour the south; the control's 1.21σ worst is likewise unremarkable. The BTO case against the north has to be made on the total, not on its largest single term.

**3.4 Report the full nine-term z² breakdown for both fits.** Δχ² of 10.35 cannot be interpreted without knowing which terms carry it. From what is known, the northern fit's 20:41 term is ≈3.09 and its five BFO terms ≈6.1 if the mean residual is near 4.55, leaving roughly 9 across the other three BTO terms — which would be the real story and is currently invisible. One table, nine rows, two columns.

**3.5 Convergence, both sides.** The control is pinned on its 36°S edge, so its true optimum lies outside its bin — and the known southern family (C120 at 35.85°S, 8.117) is almost certainly what it is leaking toward. The northern search stopped on an optimizer error after 35 evaluations. These fail in **opposite directions**: fixing the control widens the gap, fixing the north narrows it. Converge both before any ratio is quoted. Where the control and C120 are the same solution, compare against C120's frozen 8.117 on the identical nine terms and say so.

---

## 4. The bins are mine and they are an artifact

Every bin's best fit presses on its **southern** edge. On a monotone surface that is close to a tautology: binning a decreasing function and reporting that each bin pins low is a property of the binning, not a finding about the data.

**Replace the bins with a continuous profile.** Scan endpoint latitude from 24°S to 40°S in 0.25° steps, minimising at each fixed latitude over the remaining command parameters, and report χ²(endpoint latitude) as a curve. That object has no edges to press on, shows whether 31.87°S is a genuine local minimum or a shoulder on a slope to the south, and is the thing that should have been produced instead of bins. The bin table stays in the record as superseded.

---

## 5. What must not be said about 32.78°S, 95.41°E

The arc-7 projection is a geometric label on a model state. **It is not a location and must not be reported as one**, in the atlas or anywhere else.

Report the coverage overlap as Ryan found it — inside Go Phoenix SAS coverage, about 13 km north of the Deep Tow northern limit — as a fact about where a projection falls, with the caveat that reaching a real endpoint from a 00:11 state needs the full terminal-phase treatment, and that every terminal continuation TASK_022 found from C120 arrived supersonic inside an aerodynamic proxy the model flags as unsupported. Two inferential steps separate this projection from seabed.

Also record the gap Ryan identified: Ocean Infinity's 2018 coverage north along the arc is **not in the layers held**, so "outside all three layers" for the 24–26°S projection means outside the layers available, not unsearched.

---

## 6. Scope

- C120 stays frozen. It is re-scored at swept δ for diagnosis and never re-fitted.
- No new forcing, no drift work, no terminal search.
- The nine-term score definition does not change. δ enters as an offset applied identically to both hypotheses, never as a tenth fitted term.
- If a part is blocked, report and stop at that part.

## 7. Stop rule

`"BFO bias sensitivity complete"` with the crossing δ (or "no crossing in ±8 Hz"), the C120 re-score at that δ, and the continuous profile's minimum, in that line. Or `"BLOCKED at Part <X>"` with the reason.

---

## 8. Note from Claude

The gate I set was χ² ≤ 20 and the candidate passes it at 18.27. That stands — I am not moving it after the fact. But passing a plausibility gate and being the better hypothesis are different claims, and only the first is established. Both belong in the writeup, in that order.

What I would most like to avoid is this result being quoted at 177:1 before §1 runs. The gap is 10.35 and a common BFO offset of 6.19 Hz erases it exactly. That number sits inside the residual range already observed. Until the sweep exists, the honest statement is that the south is preferred **conditional on a bias the project has formally recorded as missing**.
