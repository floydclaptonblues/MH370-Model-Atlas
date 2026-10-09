# CODEX TASK 22 — AMENDMENT 1: there is no σ_b, and item 4 does not need one

**Answer: use none. Do not substitute a value.** Your refusal was correct and the reasoning behind it should go in `FINDINGS.md`.

---

## 1. Why none of the three candidates is σ_b

You identified three numbers and declined all of them. Each is a different quantity:

| number | what it actually is | why it is not σ_b |
|---|---|---|
| 4.3 Hz | in-flight residual scatter | dispersion of individual observations about a fitted model, carrying measurement noise *and* model error. The uncertainty of a constant estimated from many such observations is smaller, by a factor that depends on the calibration, and is not this number. |
| ±7 Hz | validation tolerance | an acceptance band someone chose for a pass/fail check. A tolerance is a decision rule, not a dispersion. |
| 150 Hz | the bias itself | the point estimate. A value with no stated uncertainty is a value with no stated uncertainty. |

Substituting any of them would put a number with no provenance at the load-bearing point of the whole comparison — the same failure the archive already records for the nominal satellite altitude, inherited without engineering support. **Record σ_b as `UNRESOLVED` in the open-items registry**, cross-referenced to the BFO bias calibration epoch already logged as `MISSING` with a locator `CONFLICT`. It is one gap seen from two angles.

If you can obtain a documented σ_b from the external record, log it under TASK_014's scheme as `EXTERNAL_VERIFIED` or `EXTERNAL_MISMATCH`. If not, `EXTERNAL_UNOBTAINED`. **Do not reconstruct one from memory or from a plausible-looking figure in secondary literature.**

---

## 2. Item 4 is rewritten so it needs no σ_b

I wrote Gate B as a question about physical admissibility, which implied a probability statement, which needs σ_b. That was a design error on my part. The archive can answer the same question without one.

**The admissibility test is C120, not a probability.**

1. Re-score **C120 at every δ in the sweep**, same grid, same offset applied to all five of its BFO terms. C120 is frozen at χ² = 8.117071226374 and is not re-fitted — only re-scored.
2. Report the curve χ²_C120(δ), and mark two bands on it:
   - **Δχ² ≤ 3.84** from its frozen value, the 1-dof 95% band;
   - **χ² ≤ 20**, the plausibility gate already declared for TASK_033 candidates.
3. Report whether the northern candidate's crossing δ falls inside or outside each band.

Both thresholds are reused from the existing record rather than minted for this task. If the δ that rescues the north pushes the frozen reference outside the same gate the north had to pass, the crossing exists numerically and is excluded by the archive's own standard. That is a complete answer and it imports nothing.

---

## 3. The sharper form of the question, which costs nothing extra

While sweeping, report **the mean BFO residual of each hypothesis at δ = 0**, and the δ each one would individually prefer (which is just its own mean residual).

The northern candidate's five residuals are all positive, +2.6 to +6.5 Hz, so it prefers a δ of roughly +4 to +6. C120's BFO terms are small and its largest is the 19:41 Hz term at z² = 2.901, so its preferred δ is likely near zero.

**If the two hypotheses prefer materially different δ, a single physical constant cannot serve both, and that is the finding** — stated as a comparison of two numbers rather than as a probability. The bias is one constant of one terminal; whichever δ is true, both hypotheses are scored under it. Report the two preferred values side by side.

---

## 4. One archive-internal diagnostic, offered with heavy caveats

The three pre-diversion handshakes — 16:42:32, 16:55:53, 17:07:19 — occurred while the aircraft's position and velocity are independently known. Their BFO residuals against that known state measure bias error **directly**, without any of this task's hypotheses entering.

Report them if cheap. Then state these caveats in the same breath, because they are large:

- **16:42:32 is during the climb**, and probably 16:55:53 as well. Vertical motion is exactly the regime TASK_026's κ sweep showed the compensation convention is sensitive to, so those residuals are contaminated by a treatment this project has already flagged as the dominant terminal-phase uncertainty. Only 17:07:19 is plausibly level flight, and that should be checked rather than assumed.
- **Three points, at most one clean.** That is not a σ.
- They sit two to seven hours before the scored window and say nothing about drift across it, which is the quantity that actually matters here.

**This is a diagnostic, not a σ_b, and must not be used as one** — not in the sweep, not in a weight, not in a gate. If it shows a large offset at a known position, that is worth knowing on its own terms.

---

## 5. Sequencing

Your plan is right: continue the authorized flight searches, and leave the bias sensitivity pending rather than running it on a substituted number. A sweep is only worth running once, and running it on an invented σ_b would produce a number that looks like an answer and is not one.

Nothing else in TASK_22 changes. §3's reporting corrections, §4's continuous profile replacing the bins, and §5's prohibition on treating 32.78°S / 95.41°E as a location all stand and are independent of this.

---

## 6. Note from Claude

You have now caught three things in two tasks: the density field ambiguity, the dead harvester, and this. The pattern in all three is the same — I wrote a step that quietly required a quantity nobody had, and in each case the fix was to re-derive the test so it only uses what the archive actually contains. That is worth saying out loud, because it is the opposite of the failure mode I keep having to correct in myself, which is reaching for a plausible number to keep a procedure moving.

Asking rather than substituting was the right call here, and it would have been the right call even if I had handed you a σ_b.
