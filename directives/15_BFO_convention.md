# CODEX TASK 15: BFO convention — provenance, sensitivity sweep, and warm-up evidence

Authorized by Ryan. Register as the next unused DIRECTOR number and write to a new folder `run2/bfo_convention_001/`, with a new suffix if occupied. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results. Copy modules before modifying adapters.

## 0. Why this task exists, and what it must not become

TASK_022 concluded that the final frequency pair requires a steep accelerating descent and excludes a long controlled glide. That conclusion rests on one unvalidated choice: how the model treats vertical motion in the SDU pre-compensation, recorded as K-mode OPEN and as a zero-vertical-speed compensation convention. The physical term now includes local up; the compensation term uses horizontal ground velocity only, with nominal satellite and surface position.

If the real SDU compensated vertical motion as well, a descent would produce little or no BFO signature, and the dive-versus-glide conclusion would invert. Nobody has shown which it is.

This task measures **how much of the conclusion depends on that choice**. It does not try to establish the correct convention, and it does not fit one.

Explicitly forbidden: fitting, tuning or selecting any convention parameter to make any history compatible; adopting any convention as the new default; changing C120, its nine-term cruise score, k, fuel, engine-loss timing, or any frozen input; running a new terminal search or any new trajectory optimisation; changing the warm-up envelope, the measurement envelopes, or the retained TASK_022 records; using the 7th arc, any flight path, candidate position or search area anywhere; producing an endpoint, crash coordinate or search recommendation.

Deliver the sensitivity map and the evidence, whatever they show, and stop.

## 1. Part A — what the project files actually state (no computation)

Identify, in the existing code and documents, exactly what the following are and where each is defined. Quote the defining line or passage with file path, hash and location.

1. The SDU / AES Doppler pre-compensation term: which velocity components enter it, which satellite position (nominal or ephemeris), which aircraft position (surface-projected or actual altitude), and what the existing K-mode flag actually controls. **Determine this by reading the implementation, not by assuming it matches my description above.** If my description is wrong, say so and correct it.
2. The physical Doppler term and which velocity components enter it.
3. The oscillator / warm-up model: where the offsets (a, a−d) with 17 ≤ a ≤ 136 Hz, 0 ≤ d ≤ 6 Hz and residual bounds −18 to +28 Hz come from, and whether any file sources them to a document or declares them as chosen.
4. The BFO bias constant and its calibration epoch.
5. σ_BFO and σ_BTO as used, and where they are stated.

Label every row SOURCED, ASSUMED, CONFLICT or MISSING, using the Task 13 vocabulary. Deliver `bfo_convention_provenance.csv`. If the compensation convention turns out to be sourced to a document, that changes this task's weight and must be reported prominently.

## 2. Part B — the sensitivity sweep (the main deliverable)

Re-evaluate the **existing, frozen** TASK_022 message states. Do not re-integrate any trajectory and do not search. Use all sixteen retained histories: the twelve fitted frequency-compatible ones, R0, G0, and the two bank-release comparisons.

Define a one-parameter family that spans the two endpoints, with κ the fraction of the aircraft's vertical velocity that the compensation term removes:

- κ = 0 is the current convention (no vertical compensation).
- κ = 1 is full vertical compensation, where BFO is insensitive to vertical speed.

Implement κ in a **copied** module, leaving the original operator untouched. Confirm by exact comparison that κ = 0 reproduces every TASK_022 BFO residual to within floating-point noise, and report the largest difference. If it does not reproduce them, stop and report the discrepancy rather than proceeding.

Sweep κ over {0, 0.1, 0.2, … , 1.0}. At each value, for each of the sixteen histories, compute BFO29 and BFO37 predicted values and residuals, and evaluate warm-up and no-warm-up compatibility under the existing unchanged envelopes and feasible-set solver.

Also evaluate, as separate declared switches at κ = 0 and κ = 1 only:

- nominal satellite position versus the actual ephemeris position in the compensation term;
- surface-projected aircraft position versus actual altitude in the compensation term.

Deliver `kappa_sweep.csv` (one row per history, κ, switch combination, with both residuals, both compatibility verdicts, and the feasible offset interval where one exists) and `convention_switches.csv`.

### What to report from the sweep

- For each history, the **interval of κ over which it is compatible**, under warm-up and under no-warm-up separately.
- The **crossover**: the κ at which the twelve dive histories stop being compatible, and the κ at which R0 or G0 start being compatible, if either ever does.
- Whether any κ exists at which **no** history is compatible, and whether any κ exists at which **both** a dive history and a glide control are compatible.
- A figure: BFO37 residual against κ, one line per history, dive cases and controls distinguished, with the compatibility band marked.

Do not nominate a preferred κ. Do not describe any κ as better. The output is a map.

## 3. Part C — confirm the cruise score cannot settle this

C120's vertical speed in cruise is of order 0.04 m/s, so κ should have almost no effect on the nine cruise terms. Verify this rather than assuming it: recompute the nine-term cruise χ² at each κ in the same sweep and report the full curve.

If the curve is flat, state the consequence plainly: **the cruise data carry no information about κ**, so the convention cannot be calibrated from the part of the record that is well fitted, and the only data that constrain it are the two final messages — which is precisely the inference the convention is being used to make. Report that circularity as a finding.

If the curve is not flat, report the variation and stop before drawing any conclusion from it; that would be a more interesting result than expected and needs separate scrutiny.

## 4. Part D — empirical warm-up evidence from the 18:25 log-on

The warm-up envelope (a up to 136 Hz) is permissive enough to absorb raw residuals of 10 to 67 Hz, so nine of the twelve fitted histories depend on it. There is a second log-on in the record that can constrain it.

From the existing burst log, extract the **18:25 UTC log-on sequence** and any other log-on or post-power-interruption sequence present. For each, tabulate the BFO values against time since the first burst of the sequence. Compare the shape and magnitude of that behaviour with the offsets the 00:19 feasible sets require.

Report:

- the observed BFO excursion at 18:25 and its decay with time, as measured values;
- whether the 00:19 feasible offset intervals are consistent with it, inconsistent with it, or not comparable (and if not comparable, why);
- the 18:25 aircraft state as recorded in the project files, with the caveat that it is itself a model product, not an observation.

This is a comparison, not a calibration. **Do not narrow the warm-up envelope, refit anything, or add a term to any score.** If the 18:25 sequence turns out to be unusable for this, say so.

## 5. Part E — what survives

Write, in `FINDINGS.md`, which TASK_022 conclusions hold across the entire swept domain and which do not. In particular, state whether "the final BFO pair requires a steep descent and excludes a long controlled glide" is:

- robust across the whole κ range,
- robust only for κ below some value, which you state, or
- not robust.

State the answer that the evidence gives, including an answer that weakens or reverses the TASK_022 reading. A result that undermines the previous task is a valid and useful outcome and must not be softened.

## 6. Budget, verification, deliverables

This is re-evaluation of saved states, not integration, so it should be cheap. A 60-minute numerical ceiling applies, with 15 minutes reserved for verification and 15 for packaging, reported separately and not mislabelled as CPU time. If the sweep cannot complete, reduce the κ grid to {0, 0.25, 0.5, 0.75, 1.0} and say so; a coarser complete sweep is an authorized result.

Verification: the κ = 0 reproduction check above; a hash comparison confirming no TASK_021, TASK_022 or frozen input file changed, with the count reported; and a check that the copied operator differs from the original only in the κ term, with the diff included.

Deliverables, in simple existing formats: `bfo_convention_provenance.csv`, `kappa_sweep.csv`, `convention_switches.csv`, `cruise_chi2_vs_kappa.csv`, `logon_warmup_comparison.csv`, the κ figure and the cruise-χ² figure as PNG, the operator diff, `NOTES.md` (assumptions, failed approaches, hashes, runtime, audit trail) and `FINDINGS.md`.

## 7. Stop rule

Deliver the map and the evidence, then stop. No adopted convention, no refit, no new terminal search, no endpoint, no automatic follow-on. Write "BFO convention sensitivity complete" when Parts A to E are done, whatever they show. Name precisely anything that could not be assessed. Completing this task does not resolve the convention; it measures what rests on it.

## 8. Notes from Claude (not instructions)

- My description of the convention in section 0 is my reading of `signal_contract.json` and the TASK_022 caveats. Part A exists to check it. Correct me in the output if the implementation says otherwise.
- κ is a diagnostic coordinate I invented for this sweep. It is not a physical parameter of any SDU and must never be described as one, or fitted.
- The expected result is that κ near 0 keeps the TASK_022 reading and κ near 1 destroys it, with a crossover somewhere between. The value of the task is locating that crossover and seeing whether anything else constrains it. If the crossover sits at a κ that no plausible hardware would produce, that strengthens the TASK_022 reading; if it sits in the middle of a plausible range, the reading is weak and should be labelled so on every downstream use.
- Part D is the only strand in this task with a chance of supplying independent evidence rather than sensitivity. It is worth doing carefully even if it ends in "not comparable".
