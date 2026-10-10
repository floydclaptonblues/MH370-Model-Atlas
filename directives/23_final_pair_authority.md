# CODEX TASK 23: can the 00:19:37 observation carry what rests on it?

Authorized by Ryan. Register as the next unused DIRECTOR number. Write to `run2/final_pair_authority_001/`. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results.

---

## 0. Read this part before anything else

This task was prompted by a line of reasoning that, if it succeeds, rescues a long-glide endpoint in unsearched water. **That is exactly the condition under which a project talks itself into an answer.** The standing rule is in force and matters more here than anywhere else it has been applied:

> **No parameter is ever tuned toward the 7th arc, toward any flight path, or toward any terminal case.** No oscillator model is chosen, shaped or bounded because of what it does to G0, to R0, to the twelve matching cases, or to C120. A model comes from documentation or from a fit to data that is blind to the terminal outcome, or it does not exist.

**The result cuts in every direction, not one.** If the 00:19:37 observation is downgraded, the chapter does not gain a glide — it loses the basis for one of its headline findings, that all twelve matching continuations arrive supersonic. That finding rests on the same eight seconds. A result that weakens the final pair weakens the southern conclusion and the glide's rejection together, and the report must say so in that order.

C120 stays frozen. No refit, no new flights, no optimiser.

---

## 1. Why this is being asked

The last two observations are 8 seconds apart: **182 Hz at 00:19:29 and −2 Hz at 00:19:37.** The information is in the difference, not either value. 184 Hz is 34.5 m/s of line-of-sight velocity, which is **0.44 g sustained** along the line to the satellite. A bias or a warm-up offset is constant over 8 seconds and cannot produce a difference between two readings 8 seconds apart; only a real acceleration or a **drift rate** can.

G0's residuals are +34.204 Hz and −121.425 Hz — opposite signs, spread 155.629 Hz, which is **19.5 Hz per second** sustained for 8 seconds. That is the bar any instrument explanation has to clear.

Two facts make that bar worth measuring rather than assuming:

**The other log-on did nearly the same thing.** 18:25:27 reads 142 Hz and 18:25:34 reads 273 Hz — **+131 Hz over 7 s, 18.7 Hz/s** — across the equivalent interval after the only other log-on in the record. That is confounded by aircraft motion and is not a clean measurement, but it removes the argument that 19.5 Hz/s is implausible on its face.

**The size is already inside the project's own envelope.** 19.5 Hz/s for 8 s is 97.5 parts per billion of total excursion at L-band. The adopted warm-up envelope of 17 to 136 Hz is 11 to 85 ppb. **The project already admits excursions of this magnitude. What it has never examined is whether they can occur this fast.**

---

## 2. Part A — the inclusion asymmetry (answer this first; it is cheap)

The canonical events table flags `included_for_bfo` as **False** for 18:25:27 and 18:25:34, and **True** for 00:19:29 and 00:19:37. These are the same two message types in the same order — *Log-on Request / Log-on Flight Information* followed by *Log-on/Log-off Acknowledge* — one pair excluded from scoring, the other carrying the entire terminal analysis.

**Find the reason in the record.** Trace the flags to whatever decision set them: a cited source, an inherited convention, a judgement made in this project, or nothing at all. Quote it with its file and line.

**GATE A.** If no documented basis exists, record in `FINDINGS.md` and in the open-items registry that **the authority of the final frequency pair rests on an undocumented inclusion flag**, and that the same pair at the other log-on was excluded. That is a finding about provenance and it stands whatever Parts B to D return.

Also report the meaning of the parenthetical in the 00:19:37 message type, **`Final Log-on/Log-off Acknowledge (partial)`**. A message recorded as partial raises a question about its measurement quality that this project has never put. Say what "partial" denotes in the source, or that it is unexplained.

---

## 3. Part B — what the oscillator can actually do (documentary)

Establish, from sources rather than from reasoning: the reference oscillator in this terminal, its type, and any published warm-up characteristic — settling time, drift magnitude, and above all **drift rate as a function of time since power-up**.

The quantity that matters is whether **12.2 ppb per second at 8 seconds after a cold start** is inside or outside that device's behaviour.

Log every claim under TASK_014's scheme: `EXTERNAL_VERIFIED`, `EXTERNAL_MISMATCH` or `EXTERNAL_UNOBTAINED`. **Do not reconstruct a figure from memory or infer one from a general class of oscillator.** `EXTERNAL_UNOBTAINED` is an acceptable and likely outcome; a plausible-looking number with no source is not.

---

## 4. Part C — the 18:25 sequence, with its confound stated first

Seven observations follow the 18:25 log-on: 18:25:27, 18:25:34, 18:27:04 (×2), 18:27:08, 18:28:06, 18:28:15, with BFO values 142, 273, 176, 175, 172, 144, 143.

**Declare the confound before computing.** The aircraft was manoeuvring, and its state through that window is unproved — the 18:22 radar report has no published coordinates at all. Any residual series from this sequence mixes oscillator behaviour with assumed motion.

So the test is a **sensitivity**, not a measurement:

1. Choose a spread of plausible aircraft states across the interval, stated in advance and spanning the range the record permits rather than one preferred reconstruction.
2. For each, compute predicted BFO at all seven times and report the residual series.
3. **Report whether a decaying transient appears in the residuals that is common to every assumed state.** A feature that survives the whole spread is an instrument signature. A feature that moves with the assumed state is not.

**GATE C, declared now.** If the residual shape depends materially on which state is assumed, **the 18:25 sequence cannot calibrate the oscillator and must be reported as unusable.** Do not select the state that produces the most transient-looking residual. That selection is the failure mode this gate exists to prevent, and it would be indistinguishable from a result.

---

## 5. Part D — what rests on the term, mapped in both directions

Diagnostic rescoring only. **Drop the 00:19:37 term** and recompute, reporting in a separate column and never mixing with nine-term values:

| Case | What to report |
|---|---|
| G0 / S14 | residual at 00:19:29 alone; does it still fail, and by how much |
| R0 | the same |
| The twelve matching continuations | **do they still require supersonic arrival once that term is removed, or was the requirement carried by it** |
| C120 | change in χ², for reference |

**State plainly that removing a term changes the score definition**, so these values are not comparable with anything else in the archive and are diagnostics, not fits.

**The third row is the one that matters most.** If the twelve no longer require a supersonic arrival without that term, then the chapter's finding that no matching continuation can leave debris at its own coordinate was carried by a single eight-second observation whose authority is what Part A is examining.

---

## 6. Part E — what would and would not follow

Declared before the run, so it is not chosen afterwards:

- **If Part B returns a documented rate well below 12.2 ppb/s**, the instrument explanation fails, G0's rejection stands on firmer ground than before, and the final pair is strengthened rather than weakened. Report it that way.
- **If Part B returns `EXTERNAL_UNOBTAINED` and Part C returns unusable**, then the authority of the final pair is **undetermined** — not refuted. G0 stays rejected on the record as it stands, with the rejection labelled as resting on an observation whose instrument behaviour has never been characterised. **Undetermined is not permission to revive a glide.**
- **If a documented rate reaches 12.2 ppb/s**, that does not make G0 correct either. It makes the final pair unable to discriminate, which removes evidence from both sides, and the supersonic finding goes with it.

No outcome of this task nominates an endpoint, and none licenses a new terminal search. If one looks warranted, it needs its own directive.

---

## 7. Scope and stop rule

No new flights, no refits, no optimiser, no drift work, no change to the nine-term score definition outside Part D's labelled diagnostic column. The canonical events table is not edited; if an inclusion flag is judged wrong, that is reported, not applied.

Deliver Parts A to E and stop. Final line, one of:

- `"Final pair authority: characterised"` with the Part A basis, the Part B status, the Part C verdict and the Part D consequences in that line.
- `"Final pair authority: undetermined"` with which parts returned nothing.
- `"BLOCKED at Part <X>"` with the reason.

---

## 8. Note from Claude

Ryan asked whether the −2 Hz could be an aircraft losing power rather than an aircraft accelerating. The chronology in that question does not hold: the 22:41 and 00:11 residuals are both about 0.3σ, so nothing is degrading before 00:11, and the 00:19 log-on is itself what a power interruption looks like, which dates the interruption to just before it rather than an hour earlier.

What survives is narrower and better. The last observation sits eight seconds into a cold start, in the regime this project elsewhere treats as unusable, and it is carrying more weight than any other number in the chapter. I have been calling its authority settled while the matching pair at the other log-on sits excluded a few rows above it in the same table. I did not notice that until it was pointed out, and Part A exists because of it.
