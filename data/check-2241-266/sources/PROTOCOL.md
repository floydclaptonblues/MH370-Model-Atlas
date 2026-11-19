# The 22:41 measurement and the 266 accepted cruise flights: protocol

18 November 2026. Amended after Codex's review of the draft at `60d3a4c`, with the seven decisions relayed by Ryan (section 14), and again after Codex's review of the implementation at `524635f` (section 16). The implementation is frozen together with this text; its revision is in `FROZEN.json`.

**Nothing has been run at this repaired revision.** The preceding revision `68895a19a580` passed its real open-epoch gate, recorded at `a283852`. Its records are preserved. This repaired revision's gate, Stage A and Stage B have not been executed, and each needs its own release (`GATE_PLAN.md`). No prediction, residual or comparison at 22:41 has been formed for these flights by this protocol or its executions. The offline tests use invented numbers only.

## 1. What this is, and what it is called

A comparison of the frozen cruise catalogue with the satellite measurement recorded at 22:41:22 UTC, which that catalogue did not use.

It is a **withheld-measurement consistency check with disclosed prior exposure**. That name is used throughout. It is not a blind test, not a sealed holdout and not an independent validation, and it is not described as any of those. Section 3 says what "withheld" covers and what it does not.

The check evaluates the existing frozen cruise flights at 22:41:22. It introduces no descent and no other change of command at that time. Comparing alternatives of that kind would be a separate, separately declared experiment.

## 2. Question and population

For each of the 266 distinct accepted flights of the cruise catalogue (`../CRUISE_LEVEL_PRODUCTION_108/`, runner revision `2a016b1294fa`, frozen at `37199ce`), listed in `../CATALOGUE_TERMINAL/TERMINAL_MANIFEST_266.csv`:

1. What timing and frequency does the frozen model predict at 22:41:22?
2. Does the predicted timing agree with the recorded timing within the tolerance applied at the three fitted times?

**All 266 flights are in the population, whatever their status in the terminal experiment** (90 propagated there, 176 not). No earlier experiment is added. The flights are taken as they are: nothing is fitted, searched, selected or adjusted. `POPULATION_266.json` holds them in manifest order, each with its native accepted record.

## 3. What "withheld" means here

**What is true of these 266 flights.**

- They were fitted to the timing at 20:41:05, 21:41:27 and 00:11:00 only. 22:41 was not a measurement epoch of the run.
- The runner's guard counted no request for a prediction at 22:41 in the gate, in any of the 848 searches or in the numerical checks, and no record of the run holds a 22:41 entry. `build_population.py` refuses any native record that holds one, and found none.
- The terminal experiment on 90 of them made no prediction, residual or comparison at 22:41.

**What is not true, and is disclosed** (`../HOLDOUT_2241_DISCLOSURE/DISCLOSURE.md` and its addendum, which this protocol does not replace):

- The recorded 22:41 values were in the memory of every process that imported the flight model, including the cruise run. The model's setup loads the event table before any guard exists. The same will be true of the gate and of Stage A; each such process is logged in `EXPOSURE_LOG.jsonl`.
- Earlier experiments of this project computed and stored predictions at 22:41 (98 tracked files in 11 directories), and thirteen result tables carry columns named for a 22:41 prediction or residual.
- A separate comparison against the measurement exists for 24 flights of an earlier experiment (`../TWO_TURN_HOLDOUT_2241/`, added 7 November). Five earlier notes concern the measurement by their titles: `directives/14_bto_2241_systematic.md`, `reports/THE_2241_PROBLEM.md`, `reports/RESOLVING_POWER_AND_THE_2241_HELDOUT.md`, `reports/HELDOUT_2241_WHAT_EXCLUDES_IT.md` and `reports/GATE3C_HOLDOUT_SAFETY.md`.
- The people and models who chose this catalogue's speeds, levels, turn ranges, satellite model and calibration worked after those earlier comparisons existed. The runner did not tune the flights to 22:41. That the design and the calibration were uninfluenced by earlier 22:41 results cannot be shown.
- The recorded values are public (the Inmarsat log) and are shown on the Model Atlas. Neither the author nor the reviewer is blind to them. As a language model I may also carry them from general knowledge.
- **Codex's source-equality audit (18 November).** To settle whether the frozen inputs already apply an adjustment to the 22:41 timing, Codex ran a read-only program on the pinned `common.py` and the pinned canonical event table. That program read the observation inputs internally, solely to test source equality and zero correction. It emitted no numerical target observation, and it computed no aircraft prediction and no flight residual. Its findings are recorded in section 5. The observations are therefore not described as never accessed.

**My own exposure.** I have not opened the files of `TWO_TURN_HOLDOUT_2241/`, `PREDICTIONS_2241_SEALED.csv`, the historical case manifest or the five notes above, and I have not read the 22:41 row of the event table or the observation vector in `common.py`. They stay unopened through this check (decision 5). In preparing the implementation I read the frozen evaluator, runner and guard as source text and imported the runner module, which loads no flight model; no process of mine has built the engine for this check. That import recomputes the cruise revision by hashing the bytes of every frozen file, the event table and `common.py` among them; it displays nothing. I know from one title that an earlier note concerns a systematic effect in the 22:41 timing. I do not know its content.

## 4. Why the check has limited power, stated before it is run

22:41:22 lies between two fitted times, 21:41:27 and 00:11:00. The second turn starts between 20:56 and 21:26. After it each flight holds its commanded Mach and its pressure level with no further commanded turn. **Held Mach is not constant ground speed:** temperature and wind change along the leg, so ground speed and course over the ground vary. A flight made to meet the timing at both ends of that leg is already constrained in between, so this is an **interpolation check along a fitted leg**. It tests mainly whether the commanded Mach and level, the weather fields and the satellite model carry a flight correctly across the leg. It shares the satellite model and the timing calibration with the three fitted times.

Fixed now:

- Agreement at 22:41 is weaker evidence than agreement at a time outside the fitted span would be. It is not a confirmation of position.
- The 266 flights share their fitted measurements and many share an arrival. Their outcomes are not 266 independent results.
- The tolerance is ±43 µs: a **43 µs half-width and an 86 µs full width**. Stage A reports, from the predictions alone, the spread of predicted timing within each speed-and-level group and between groups, beside those two widths. A small spread is reported as **limited expected discrimination relative to the tolerance**. It is not said that flights "cannot be distinguished": predictions that lie close together have overlapping but unequal acceptance intervals, and a recorded value near a boundary can place one inside and another outside.

## 5. Fixed inputs, the recorded measurement and the residuals

| Item | Fixed as |
|---|---|
| Flights | The 266 of `POPULATION_266.json`, each defined by its arrival, level, commanded Mach, climb and three turn commands with the stored 20:41 turn-anchor position |
| Flight model, weather, performance data, fuel-flow multiplier 1.000 | Those of runner revision `2a016b1294fa`, unchanged. The revision is recomputed from the 70 files it covers at the start of every process that builds the engine, and the frozen dependency list must be unchanged |
| Satellite positions and velocities, satellite-plus-EAFC term, timing bias, frequency calibration | The frozen ones used at the three fitted times. No alternative orbit, ephemeris or two-line element set is introduced under this protocol (decision 7) |

**The recorded measurement**, fixed before Stage A:

| | |
|---|---|
| Event | `T6_224122` |
| Timestamp | `2014-03-07T22:41:22Z` |
| Channel | `IOR-R1200-0-36ED` |
| Message type | `Log-on/Log-off Acknowledge` |
| Timing used | field `canonical_bto_us` (raw field `raw_bto_us`, correction field `bto_correction_us`) |
| Frequency used | field `observed_bfo_hz` |
| Runtime counterpart | the entry of `V.OBS` at epoch index 3, which is the value the frozen evaluator would use |
| Canonical event table | SHA-256 `06f2684f9ff77c02d2ac13cfa9ed20e28a3ed800cb221f1b5107f5db76927642` |
| `common.py` (holds `V.OBS`) | SHA-256 `f1a374d15a5e9e898b77d7f83c60214aff33310db51055df230df60fc76931cd` |

**Established by Codex's audit, not by me:** the runtime timing entry equals both the canonical and the raw field; the correction is zero; the timestamps agree; the same equalities hold at the other four runtime epochs; and the prediction equation that was inspected uses one common geometry bias with no separate 22:41 term. So no adjustment specific to 22:41 exists in the checked path from raw value to canonical value to runtime value, and none is introduced here. Stage B reads the timing and frequency from the pinned canonical table and refuses to run unless the table has that hash, the event appears once with that timestamp, channel and message type, the correction is zero and the canonical value equals the raw one. Both hashes are on the frozen dependency list of the cruise revision; the offline tests check that.

**Residual conventions**, as in the frozen evaluator:

```text
Timing residual            = observed timing − predicted timing
Raw frequency residual     = observed BFO − predicted BFO
Centred frequency residual = observed BFO − predicted BFO − MU_BFO
MU_BFO = −0.18 Hz
```

## 6. Criteria, fixed before any prediction exists

**Timing (the check).** A flight **meets the 22:41 timing** if the absolute timing residual is at most **43 µs** (the bound is included), using the existing calibration. This is the frozen project threshold, `ACCEPT_US = 43`, applied at 20:41:05, 21:41:27 and 00:11:00.

*Where 43 µs comes from.* Codex's review records that the ATSB factsheet on BTO characteristics (https://www.atsb.gov.au/publications/educational-fact-sheet/2022/aviation/mh370-burst-timing-offset-bto-characteristics) reports 43 µs as the 95% error statistic of its stated experiment with a static aircraft terminal on the R1200 channel, and that DSTG (Davey et al., 2016, chapter 5) uses 29 µs as a standard deviation for ordinary R1200 messages. These are different statistics. I could not open the factsheet from this session, so that description is Codex's. The threshold is a tolerance on a measurement. It is not a probability that a flight or a location is correct, and it is not replaced here by another statistical model.

**Additional thresholds.** The counts of flights within **29 µs**, **86 µs** and **129 µs** are also reported, by those names. They set no label. They are not described as one, two and three standard deviations.

**Frequency (diagnostic).** The **centred** frequency residual is reported against **±7 Hz** (bound included). It does not determine the timing label. Keeping frequency as a diagnostic is a scope choice made in advance; the shared calibration and the prior exposure limit its independence. If the raw frequency residual is shown, it is named separately.

**Numerical agreement.** Each prediction is made at the catalogue's integration step (15 s) and at half that step (7.5 s). The two must agree within **0.1 µs** in timing and **0.01 Hz** in frequency. Both predictions are kept at stored precision, with their differences.

**Boundary sensitivity.** If the two steps agree within those limits but their timing residuals fall on opposite sides of the 43 µs threshold, the flight is reported as **boundary-sensitive** and has no definitive timing label under this protocol. The same rule is applied separately to the frequency diagnostic and to each additional threshold, and shown separately. No refinement is made after the seal.

No other criterion is added after Stage A or Stage B.

## 7. Reproduction: what "the flight reproduces its record" means

Before any prediction at 22:41:22 is formed for a flight, the flight is repeated at the unchanged step and compared with its **native accepted record**: the result the cruise run stored in its ledger for the flight to 00:11:00, copied into `POPULATION_266.json` at stored precision. Rounded summary tables are not used.

**Identity and recipe**, checked before the flight is computed: the arrival; the search cell; the target pressure; the commanded Mach; the climb start (19:41:03 where there is a climb); the first turn, the second-turn start and angle and the stored 20:41 turn-anchor position; the end time 16,197 s and the default step; the policy label. Together these must give the flight's ledger key through the frozen runner's own key function. The cruise revision and its dependency hashes must be unchanged.

**Compared fields:** every field of the native record except the two listed below.

| Group | Fields |
|---|---|
| Fitted timing residuals | `r20`, `r21`, `r00` |
| Physical support and ending | `sup`, `label`, `native_status`, `geometry_status`, `geometry_last_s`, `last_s`, `exh`, `stop_bracket`, and `rej`, `event` or `cls` if present (none is present in the 266 records) |
| Endpoint and margins | `last_fuel`, `min_margins` (buffet, thrust, Mach support), `min_realised_Mach`, `min_floor_margin`, `min_bank_margin`, `min_crab_margin`, `stages`, `p_target` |
| Open-epoch tuples at 19:41:03, 20:41:05, 21:41:27 and 00:11:00 | all ten entries of each: latitude, longitude, height, predicted timing, predicted frequency, fuel, ground speed, course, vertical speed, centred frequency residual |

**Excluded, and only these:** `wall_s` (measured computation time) and `final` (ledger bookkeeping); and `cached`, which only a reused ledger entry carries.

**Equality rule.** On the same frozen numerical runtime every compared value must be **equal**: numbers as parsed values with no tolerance, strings, truth values and absent values exactly, and the same set of fields on both sides. This is equality of recorded values, not byte identity of a whole record. A flight with any difference is recorded as **not reproduced**: no prediction is formed for it and the stage stops for review.

**Another runtime.** No tolerance for a different numerical runtime is declared. If equality fails in the gate, Stage A does not start. A tolerance could only be introduced by an amendment before any target prediction, justified on the open control flights.

**The continuation to 00:40 is not repeated.** The reference is the record of the flight to 00:11:00, whose endpoint fuel and ending are compared. The fuel-exhaustion event of a flight belongs to its separate continuation record, later than the target time, and is not compared here. That is a declared limit, set by the allowance.

**Half step.** The half-step repeat is a separate numerical check and is not expected to equal the record. It must be the same kind of flight (supported to 00:11:00, same label and statuses, measured at the same four epochs). If it is not, the flight is numerically unresolved.

## 8. The prediction-only adapter

The frozen evaluator's `measure()` forms, at each listed epoch, the aircraft state, the predicted timing and frequency, and then the residuals against the recorded values. In the cruise runs 22:41:22 is removed from the list, so `measure()` is never entered for it. That stays so. **No helper that forms a 22:41 residual is called and nothing is deleted afterwards.**

`adapter_2241.py` forms the state and the two predictions by the statements of `measure()` that do so, and nothing else. It selects no recorded value and forms no residual. The offline tests compare its statements with those of the frozen source, one by one. It preserves:

- **Material height:** the height of the commanded pressure level at the state, with the same pressure wrapper the frozen `evaluate()` installs for a climbing flight.
- **Kinematics:** the frozen routine on the flight's command and geometry spline, **one-sided at a non-initial epoch (`side = −1`) with `eps = 0.125·dt/15`**; the velocity rotated into local east, north and up.
- **Timing:** the frozen routine with the same position, height and epoch index, which selects the satellite position. The cruise guard wraps this routine and stays installed; the adapter takes the routine from the guard's own closure, in one place.
- **Frequency:** the frozen Doppler routine with position, height, ground speed, course and vertical speed, and the frozen satellite position, satellite velocity and satellite-plus-EAFC entry of the epoch.

The command and spline are those of the flight just evaluated, taken from `measure()`'s own last kinematics call by a pass-through recorder that changes no argument and no result.

**Qualified at the open epochs before it is used at the target.** For every flight and at both steps, the adapter is first applied at 21:41:27 and 00:11:00. Its latitude, longitude, height, predicted timing, predicted frequency, ground speed, course and vertical speed must **equal** what `measure()` stored for the same flight. Any difference stops the stage before the target evaluation. The gate does this for eleven control flights and makes no evaluation at 22:41 (`GATE_PLAN.md`).

Fuel at 22:41:22 is not exported: the frozen evaluator exposes fuel only at its listed epochs, and the two predictions do not use it.

## 9. Stage A: predictions only

One process. All 266 flights in manifest order at the full step, then the half step for those with a full-step prediction. For each attempt:

1. The flight is repeated by the frozen functions with its stored commands. No search is made.
2. Full step: the flight must reproduce its native record (section 7). Half step: it must be the same kind of flight.
3. The adapter must equal the stored predictions at the two open epochs.
4. The cruise guard's count of requests at 22:41 must be zero, and the frozen dependency check must report no changed frozen file and no file or module outside the frozen lists.
5. A record that the target evaluation is about to begin is written.
6. The target evaluation is made: one predicted timing and one predicted frequency at 22:41:22. The guard's count and the dependency check are read again.
7. The prediction is written to its own file, with those two readings, and the attempt is settled.

Stage A forms no residual and makes no comparison. Its code contains none, and it does not read the recorded 22:41 values (they are in memory, as section 3 says).

**Every one of the 266 identities has a status in the output**, one of:

| Stage A status | Meaning |
|---|---|
| `PREDICTED` | Both steps predicted and in numerical agreement: a usable pair |
| `NUMERICALLY_UNRESOLVED` | Both steps predicted; they differ by more than 0.1 µs or 0.01 Hz |
| `HALF_STEP_NOT_USABLE` | The half-step flight was not the same kind of flight |
| `NOT_REPRODUCED`, `ADAPTER_MISMATCH` | Failed reproduction, of the record or of the adapter at an open epoch |
| `LOST_AFTER_TARGET`, `ERROR_BEFORE_TARGET`, `GUARD_REQUEST`, `DEPENDENCY_PROBLEM`, `RETRIES_EXHAUSTED`, `NOT_COMPUTED` | Not computed, with the reason: execution stopped, a ceiling was reached, or an attempt was lost |

**The seal** (`STAGE_A_SEAL.json`) binds: the population file and the order of identities; the hashes of every file of this package, of the manifest and of the pinned inputs, and the cruise revision; the two step settings and the target settings; the bytes of the predictions file; the coverage and numerical status of all 266; and the actual attempts, target evaluations, charges and stops, with the journal of phase records. The predictions file holds the full-step and half-step timing and frequency predictions at stored precision and their differences.

**Sealing is three durable steps.**

1. One record, `seal_begin`. It fixes the state that is sealed, as the number of phase records before it, and the SHA-256 and length of each of the four files: `PREDICTIONS_2241_266.csv`, `JOURNAL.jsonl`, `STAGE_A_REPORT.json`, `STAGE_A_SEAL.json`.
2. The four files, in that order. The seal file is the last.
3. One record, `sealed`.

**Computation is closed from step 1.** After the `seal_begin` record no attempt is admitted and no record is written except the completion. A Stage A invocation returns `CLOSED` without building the engine, flying a flight or evaluating a target. A seal file, or any of the other three export files, closes computation in the same way even if no record of sealing is found beside it.

**An interrupted seal is finished, not redone.** The four files are a function of the fixed state and of nothing else: no time and no process identity enters them. A process that finds step 1 without step 3 forms the files again from the fixed state and requires them to equal the recorded hashes. It writes the files that are missing. A file that exists must be the recorded one, and it is left as it is. If the fixed state no longer gives the recorded files, or an existing file differs, sealing stops with a refusal that names the file; nothing is replaced, and computation stays closed. A seal begun with a statement of partial coverage is finished with that statement.

**After the seal is confirmed, no flight and no prediction is computed again.** Independent Stage B arithmetic remains allowed.

## 10. Allowance, interruption and counts

| Ceiling | Seconds |
|---|---:|
| Gate | 1,200 |
| Stage A, full step | 8,000 |
| Stage A, half step | 12,000 |
| Total, not raised | 21,200 |

In the cruise run the 266 full-step flights to 00:11:00 took 11.6 to 21.1 s each (median 14.1 s), 3,801 s together. A half-step flight should take about twice as long.

**Reservation, settlement, refund.** One process; a second process on the same records is refused. An attempt is admitted only if the charges of its stage plus its reservation fit the stage ceiling: 120 s at the full step and 240 s at the half step, the frozen runner's values, which are also the attempt's deadline. When the attempt ends it is charged the time it used, and the rest of the reservation returns to the allowance. An attempt that never reaches settlement is charged its whole reservation when the next process starts. The account is computed from the phase records; the account file is a copy that must agree with them.

**Counter units.** An *attempt* is one admitted try at one identity and step. A *target evaluation* is one use of the adapter at 22:41:22, returning one predicted timing and one predicted frequency; it makes exactly one call of the timing routine and one call of the frequency routine at that epoch, and the adapter refuses any other number. A complete clean run has one full-step and one half-step target evaluation for each flight: **266 + 266 = 532** target evaluations, 532 timing calls and 532 frequency calls. Every actual attempt and every target evaluation that was begun is counted from the records, including interrupted ones. Counters are never reset. The gate makes none. The cruise guard's own count of requests at 22:41 must stay at zero; anything else stops the stage.

**Interruption, fixed rule.**

| What happened | What is done |
|---|---|
| The attempt ended before its target evaluation began (process stopped, or deadline reached) | Charged as above. **One retry**, by a fresh process. A second such ending for the same identity and step stops the stage for review |
| An error in the calculation before the target evaluation; a flight that did not reproduce; an adapter difference at an open epoch; a request through the guard; a dependency problem | Not retried. The stage stops for review |
| The prediction was stored | It is kept and reused. It is never computed again |
| The target evaluation began and the prediction file is present and whole, but the process stopped before recording it | The file is adopted, kept and reused |
| The target evaluation began and no prediction is left | **Ambiguous loss.** Not retried. The stage stops for review |
| A prediction was stored and the guard's count or the dependency check, read after its target evaluation, was not clean | The prediction is kept and is not computed again. The stage stops for review |

**Review requirements.** Each "stops for review" above is a *review requirement*, and it is not a record of its own. It is what the attempt's closing record means: the settlement or interruption record that carries the outcome, or the record of the stored prediction that carries the integrity reading. For exhausted retries it is the closing record of the last permitted attempt. That record is one file, written whole or not at all, so there is no moment at which the outcome is recorded and its requirement is not. A process that stops at any point leaves either no closing record, and the attempt is then settled by the table above when the next process starts, or the closing record with its requirement.

While a requirement is unresolved, a session ends `STOPPED` before the engine is built, and no attempt is admitted. A requirement has an identifier (`attempt:<attempt id>`, or `stop:<record number>` for a finding recorded between attempts). It is lifted only by a recorded decision that names that identifier; a decision lifts the one requirement it names. Lifting a requirement computes nothing: the identity keeps its status and is not attempted again.

Phase records and prediction files are each written whole or not at all, and never overwritten. Two predictions for one identity, a missing or incomplete record, a changed prediction file, a file that no attempt accounts for, and an account that disagrees with the records are all refused. A resolution that names no recorded, unresolved requirement is refused.

**A ceiling** stops admission for that step. The identities not reached keep the status `NOT_COMPUTED`. A seal of an incomplete stage is possible only with its reason stated, and it carries the true coverage.

## 11. Stage B: the comparison

A separate arithmetic program, `stage_b.py`, frozen and tested on invented inputs before Stage A. It imports no flight module. It verifies the seal and the pinned event table, forms the residuals of section 5 and applies section 6.

- It runs only after Codex has confirmed the Stage A commit and the hash of the seal; the release file must name that hash.
- **Codex recomputes the Stage B arithmetic and labels independently** from the same sealed predictions and the same pinned observation and calibration definitions (decision 6).

**Primary label, for a flight with a usable pair of predictions:** *meets the 22:41 timing*; *outside the band*; or *boundary-sensitive*, with no definitive label. The frequency diagnostic is shown beside it. A flight that was not reproduced, not computed or numerically unresolved has **no label, with its reason. It is not a measurement failure.**

## 12. What each outcome will be taken to mean

Written now, so that the reading cannot follow the result. **Every "all", "some" or "none" names its denominator.**

| Outcome | What will be said |
|---|---|
| All 266 of the catalogue meet the timing | The catalogue is consistent with the 22:41 timing along its fitted leg, at the tolerance used for the fitted times. An interpolation check with disclosed prior exposure; not a confirmation of position |
| Some meet it and some do not, all 266 having a definitive label | Reported flight by flight and by group. Under the frozen model the 22:41 timing separates the sampled flights |
| None of the 266 meets it | The catalogue as computed is inconsistent with the 22:41 timing at this tolerance under the frozen satellite model and calibration. Reported as plainly as agreement would be |
| Incomplete or indeterminate: one or more of the 266 without a definitive label | The counts with a label, the counts without and why, and a statement about the labelled subset that names that subset as its denominator |

In every case:

- **The original catalogue and its acceptance at the three fitted epochs are preserved.** A separate 22:41 timing status is appended. No flight is removed, refitted or re-searched under this protocol, and no parameter is changed in response to the result (decision 3).
- **A flight found inconsistent at 22:41 is identified clearly whenever agreement with all checked measurements is discussed.** The terminal results of such a flight stay published, with that status.
- Residual size inside the band does not rank flights. Counts are counts, not probabilities.
- A flight outside the band is inconsistent **under this model**. The cause may be the flight, the commanded speed and level, the weather fields, the satellite input (the separate audit's sensitivity is still open) or the timing calibration. The check does not separate these.
- **This check cannot establish a unique impact location or a calibrated probability of a location.** It can change the consistency of particular sampled flights.
- After Stage B the measurement is no longer withheld for this catalogue. A later experiment that uses it as a fitted time is a new experiment and must say so.

## 13. Reporting

Stage A report: reproduction, adapter agreement at the open epochs, numerical agreement, expected discrimination, coverage, attempts, target evaluations and cost. No residual. Stage B: one row for each of the 266 flights, one table by group, and a summary with the outcome sentence. The findings will state what was executed and what was not, list deviations, and repeat section 3. Atlas wording will carry the name in section 1 and the limits in section 4, and will not use "holdout", "blind" or "sealed".

## 14. The seven decisions (Codex's review of `60d3a4c`, relayed by Ryan on 18 November)

1. **Population.** All 266 frozen cruise histories, whatever their terminal-propagation status. No earlier experiment is added.
2. **Timing criterion.** An absolute timing residual of at most 43 µs, with the existing calibration.
3. **Consequences.** The original catalogue and its acceptance at the fitted epochs are preserved; a separate 22:41 timing status is appended; a newly inconsistent history is identified clearly whenever agreement with all checked measurements is discussed.
4. **Frequency.** A separate diagnostic against ±7 Hz, on the centred residual. It does not determine the timing label.
5. **Historical material.** The earlier 24-flight comparison, the sealed predictions file and the five historical notes stay unopened through this check. Any later historical comparison is a separately declared task.
6. **Independent comparison.** Codex recomputes the Stage B arithmetic and labels from the same sealed predictions and pinned definitions.
7. **Satellite inputs.** The frozen satellite and EAFC inputs are kept. No alternative orbit or two-line element set is introduced under this protocol.

## 15. Changes from the draft at `60d3a4c`

- Sections 5 to 11 are new or rewritten: the exact event and fields, the residual conventions, the reproduction rule, the adapter, the statuses, the accounting and interruption rules, and the seal.
- "Cannot distinguish the groups" is withdrawn (section 4). "Holds its Mach and course law" is replaced by an accurate description of the commands.
- "Nothing follows about a location" is replaced by the limitation in section 12.
- The statement that selection on frequency at 19:41 makes the later frequency "not an independent test" is replaced by the scope statement in section 6.
- The 29, 86 and 129 µs thresholds are named as additional thresholds and are no longer tied to a standard deviation.
- An incomplete or indeterminate outcome is added, and every outcome names its denominator.
- "One flight repeated once" is replaced by the fixed interruption rule of section 10.

## 16. Changes from revision `7cddf8710d7a` (Codex's review of `524635f`)

Implementation repairs. The population, the event mapping, the residual conventions, the thresholds, the satellite inputs, the flight recipes and the frozen cruise engine are unchanged, and so are sections 1 to 8 and 11 to 14.

1. **Review requirements survive interruptions** (section 10). In the reviewed revision a failed attempt was closed by one record and its stop was written as a second record. A process that died between the two left a closed failure with no stop, and the next process went on. The requirement is now read from the closing record itself. Resolutions name the requirement they answer.
2. **Sealing is recoverable and closes computation from its first record** (section 9). In the reviewed revision the four files were written before the one record that closed computation. A process that died among them left exports that a later process could compute past, and a seal that could not be finished.
3. **The gate is started once for a revision** (`GATE_PLAN.md`). In the reviewed revision an interrupted gate could be started again under the same release, and its interrupted control flight was then computed again.
4. **Found while making these repairs, same kind of fault.** The dependency check was made once, at the end of a session, and its finding was written as a separate record. A session that died early left no finding for the flights it had computed. The check is now made in every attempt, before its target evaluation and after it, and the finding is part of the attempt's closing record (section 9, steps 4 and 6; the new status `DEPENDENCY_PROBLEM`). The check takes about 0.24 s; two for each of 532 attempts is about 250 s, charged to the attempts within the existing ceilings.
5. **Found while making these repairs.** The settlement of a failed attempt was written inside the attempt's deadline. A deadline arriving during that write could have produced two settlements for one attempt, which the records refuse. Every closing record is now written after the deadline has been cancelled.

## 17. Narrow dependency repair after the real gate of revision `68895a19a580`

Codex reviewed the real gate recorded at `a283852`, which passed the twelve declared checks. That gate qualifies its original revision only; its records and charges remain unchanged. No target prediction or comparison was made by that gate.

Before Stage A, the nonfatal `HALF_STEP_NOT_USABLE` branch now asks the existing dependency checker for its findings before it returns. With clean dependencies it retains exactly the same numerical status and proceeds by the existing rule. With a dependency finding it instead closes as `DEPENDENCY_PROBLEM`, preserves both the unusable-half reason and the complete dependency findings in its detail, and creates the existing durable review requirement. A fresh process must stop before further calculation, even if the preceding process died immediately after the closing record was written. The half-step forms no target prediction in either case.

This change affects the previously unchecked nonfatal branch only. Full-step reproduction, usable-half calculations, the adapter, population, flight commands, observation mapping, residual conventions, thresholds, satellite inputs, integration settings and computation allowances are unchanged. The new regression file is part of the frozen identity. The previous gate is retained as evidence; the repaired revision needs its own gate. Report the earlier gate's cost with the new run rather than discarding it.

## Not executed for this repaired revision

The gate, Stage A and Stage B of this repaired revision. Its preparation used source inspection and offline tests only. The earlier gate of revision `68895a19a580` is recorded separately at `a283852`. Historical preparation evidence is identified by its revision in `IMPLEMENTATION.md`; it is not represented as a new run of those tests or computations.
