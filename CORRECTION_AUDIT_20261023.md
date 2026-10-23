# Correction audit, 23 October 2026

**Working document, not published.** It lists what on the Atlas is no longer
supported by the evidence behind it, what the correction is, and where the
evidence sits. No page has been changed yet.

The occasion is a set of findings from 21–23 October. None of them makes the
published measurements wrong. What they change is the **status** those
measurements can claim, and in three places the Atlas claims more than the
evidence now carries.

---

## The three findings that force corrections

### 1. No flight fit in this project has ever passed its own stationarity test

`directives/15a_solver_termination.md` in the ocean repository.

Across the most recent campaign, **twelve qualification assessments returned
zero qualified fits**. The optimizer reports `Optimization terminated
successfully` at points carrying objective gradients of **3.5 to 11.0**, with
empty active-constraint sets, after displacements as small as **2.0 × 10⁻⁹**
scaled units from their starting vectors. Three of nine attempts did not
meaningfully move at all.

This is a defect in the gradient interface, not a statement about the aircraft.
But it means **every χ² quoted on the Atlas describes a point that has not been
shown to be a minimum**, and every comparison between two such points inherits
that.

The Atlas currently says nothing about this. The word "stationarity" appears
twice across all pages and in neither case refers to it.

### 2. No 19:41 fuel state is supported by a connected incoming flight

TASK_051 (`run2/task051_post_radar_feasibility_001`) in the TASK042 repository.

Two reconstructed ancestries were flown forward from a continuously integrated
primary radar handoff toward 19:41. **Neither arrived.** Both reached their
400-trial caps, stopping around **18:27** — some five minutes past the handoff —
against a thrust barrier: 159,460.74 N required against 158,318.61 N available
on one, 158,923.15 N against 158,496.67 N on the other. Shortfalls under 1%,
but shortfalls.

In TASK_051's own words:

> *"No 19:41 fuel exists as a supported output, so its historical-context
> difference from 27856.86569474842 kg remains unassessed."*

So the fuel load at 19:41 is carried from historical context, not derived from
a flight that reaches it. Any statement that a solution is **fuel-limited**, or
that it has a fuel margin of a particular size, is computed against that
unsupported figure.

### 3. The Phase 5A ranking is relative, not absolute

Verified against the recovered archive, 21 October.

Of the **96** Phase 4B/5A candidates, **none passes even the final 00:19:29
timing observation at three sigma**. The smallest final residual anywhere in
the set is **312.8 µs** against a 3σ band of **186 µs**. The top-ranked
candidate's 20:41 residual is **−857.8 µs**, about 29.6σ.

The 12.7× score ratio between tiers reproduces exactly, so the *ranking* stands.
What does not stand is any implication that the winner fits the timing
observations well. The source itself labels that score
`deterministic_dimensionless_compatibility_score_not_posterior`.

---

## Page-by-page corrections

### `closing_body.html` — "What was established"

**(a) "The cruise model fits, under heavy constraint."**
C120's χ² = 8.117071 with nine active constraints and "a fuel allowance margin
of about 0.1 kg."

*Correction:* this return has never passed the project's stationarity test, and
the 0.1 kg margin is measured against a 19:41 fuel load that no connected
incoming flight supports. Both qualifications belong in the claim, not in a
footnote. "Fuel-limited" should become "fuel-limited **under an unverified
19:41 fuel load**."

**(b) "The endpoint latitude is constrained by the handshake sequence."**
"Seven solutions in this family land at 00:11 between 35.85°S and 36.85°S."

*Correction:* this is the spread of seven **unqualified returns from one narrow
search family**, every one propagated forward from an assumed 19:41 state. It
describes where that family's returns landed. It is not a constraint the
handshake sequence imposes. The heading overstates the measurement by a wide
margin and should be rewritten rather than annotated.

**(c) The northern candidate at 32.00°S, χ² = 16.84, "scores worse than the
southern solution."**

*Correction:* a comparison of two unqualified points. The direction is
reportable; "worse" implies a resolved preference that the evidence does not
support. Add that the two become indistinguishable under a common frequency
offset of **+5.692 Hz**, which is **0.81σ** — less than one standard deviation
of a single nuisance parameter.

### `northsouth_body.html` — the whole page

The page compares two candidate fits in detail. Its reasoning is sound and its
measurements are correct; its framing assumes the comparison is between two
resolved solutions.

*Correction:* a standing note at the top — both candidates are unqualified
returns, neither has passed the stationarity test, and the comparison describes
two saved points rather than a resolved preference. The existing section "One
observation carries a quarter of the argument" is the right instinct and should
be strengthened with the 0.81σ figure.

### `canonical_body.html` — Phase 5A reference

*Correction:* where Phase 5A appears, add that no candidate in that set passes
even the final timing observation at three sigma, smallest residual 312.8 µs
against a 186 µs band, and that its score is a deterministic compatibility
measure and not posterior odds.

### Drift pages — no action

`drift2`, `drift3`, `drift4`, `methods`, `reference` carry the drift work,
which was corrected on 15–21 October: the sub-35°S sentence withdrawn, the
four-reanalysis drifter validation added, "negated" in place of the earlier
wording. The candidate-reachability experiment and the withdrawn per-origin
median ordering were never published here, so nothing propagates from them.

The 1.2% transport coefficient appears throughout and is correct as stated — it
is the declared parameter, not a result.

---

## What is *not* proposed

**No measurement is deleted.** Every number above was correctly computed and
correctly reported at the time. What changed is what is known about the
machinery that produced the fits, and that calls for qualification rather than
removal.

**No page is withdrawn.** The reasoning on these pages remains the best account
of what was done. Removing it would destroy the audit trail that makes the
corrections legible.

**No new claim is added.** Nothing here asserts that the southern solutions are
wrong, that the endpoint lies elsewhere, or that the fuel assumption is
mistaken. The corrections reduce certainty; they do not redirect it.

---

## Sources

- `directives/15a_solver_termination.md` — the solver defect and the twelve
  assessments
- `directives/14b_control_folds_operative.md` — the nine returns and their
  status
- `reports/THE_2241_PROBLEM.md` — the physical account
- `reports/WHY_THIS_CASE_IS_HARD.md` — the conditioning analysis
- TASK042 `run2/task051_post_radar_feasibility_001/REPORT.md` — the unclosed
  incoming history
- TASK042 `model/run2/bto_2241_control_folds_001/` — the qualification matrix
