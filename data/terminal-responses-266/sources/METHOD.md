# Terminal responses of the accepted cruise flights: method

16 November 2026, revised the same day after Codex's reviews of `2fc9d0e` (five repairs, `REPAIRS_1.md`) of `b742742` (three repairs, `REPAIRS_2.md`) and of `d1335b4` (one repair, `REPAIRS_3.md`). The manifest, the physical assumptions, the flight-selection rules and the allowances are unchanged by the second and third sets. Prepared for review. The gate and the calculations that follow it are declared here as one method, so that one approval can cover both.

**No terminal calculation has been run and no cruise flight was recomputed.** Executed so far: `build_manifest.py` and `bookkeeping.py` (they read committed files and do arithmetic), `deps.py` and `term_cat.py --phase bind` (they import the existing solvers, load the reference results the gate will compare with, and hash files; they evaluate nothing), and the offline tests. One command that was refused, run to demonstrate the refusal, opened and published an empty account for an intermediate revision; that account is removed and the cause repaired (`REPAIRS_1.md`).

## Questions

For the accepted flights of the cruise-level catalogue (`../CRUISE_LEVEL_PRODUCTION_108/`, revision `2a016b1294fa`):

1. After the modelled engine fuel runs out, which declared responses can the model carry to each of the two final transmissions, 00:19:29 and 00:19:37 UTC?
2. How does each response compare with the timing and the frequency recorded at those transmissions, taken separately and together?
3. Where does the model put the aircraft at the two transmissions, and where does each continued path end, and for what reason?

Every position produced is a state of this model under its stated assumptions. The collection of positions is a conditional terminal envelope of the sampled responses. It is not a probability map and not an outer bound.

## Population

All 266 distinct accepted flights are listed in `TERMINAL_MANIFEST_266.csv` with their command identities, ledger keys, numerical-check status and range-end flags. Each has one status, set by its saved fuel-event time alone.

| Status | Flights | What is done here |
|---|---|---|
| Engine fuel runs out before 00:19:29 | 90 | Terminal responses computed |
| Engine fuel runs out after both final transmissions | 139 | Kept in the manifest; not propagated |
| Engines still running at 00:40:00 | 37 | Kept in the manifest; no fuel-exhaustion state exists |

A fuel event later than a transmission cannot have caused a response before it. That is all the second and third statuses say. They do not reject those flights under another electrical or control sequence, which this method does not examine.

The 90 flights by incoming group and cruise level, with the time from the fuel event to 00:19:29 (`ELECTRICAL_BOOKKEEPING_BY_GROUP.csv`):

| Incoming level and speed | Cruise level | Flights | Fuel event before 00:19:29 |
|---|---|---|---|
| 300.9 hPa, Mach 0.78 | 33,985 ft | 13 | 136 to 158 s |
| 331.655 hPa, Mach 0.75 | 31,946 ft | 21 | 176 to 198 s |
| 365.113 hPa, Mach 0.67 | 25,661 ft | 30 | 377 to 400 s |
| 365.113 hPa, Mach 0.75 | 31,946 ft | 26 | 489 to 509 s |

No window is placed on that time. It is reported, and all 90 flights are computed whatever its value.

Not changed anywhere: the fuel-flow multiplier (1.000), the fuel on board, the event time, and every command upstream of the event.

## First batch

Four flights, one from each group, chosen as engineering and scientific cases. They are not a sample and carry no weighting. Where a configuration has several accepted flights, the one taken is the flight of the stated side that the numerical check repeated and that is not on an end of the searched range.

| Flight | Group | Ledger key (continuation to 00:40) | Fuel event | Hash of the saved state |
|---|---|---|---|---|
| `A001_CONTROL.F1` | Mach 0.67 at its incoming level | `PF\|1\|CONTROL\|17937.0\|None\|-5.3662109375\|5532.457036342286\|-11.381762563356205` | 00:13:09.44 | `5fc1f731…3789` |
| `A002_TO275.F1` | Lower arrival, Mach 0.75 at 275 hPa | `PF\|2\|275.0\|17937.0\|None\|-2.3974609375\|5509.584292432174\|-6.241439400012644` | 00:11:18.20 | `caed5986…b914` |
| `A004_TO275.F1` | Middle arrival, Mach 0.75 at 275 hPa | `PF\|4\|275.0\|17937.0\|None\|-5.28564453125\|5594.224642981841\|-5.8750577347354165` | 00:16:13.18 | `59c1f8c7…f4a0` |
| `A006_TO250.F3` | Mach 0.78 at 250 hPa, right side, interior | `PF\|6\|250.0\|17937.0\|None\|0.771484375\|5276.451131896138\|-4.945008631393586` | 00:16:51.40 | `e82acd7e…c8df` |

Full hashes are in `MANIFEST_SUMMARY.json` and are asserted by the tests.

## The calculation

The existing solvers are used unchanged (`HANDOFF.md`, "Source and data that are reused"). `term_cat.py` supplies the new event states, the gate, the batches, the record of each requirement and the accounting.

**Before the response.** From the fuel event: no thrust, lift coefficient and bank held at their values at the event.

**The response.** At the onset time the lift coefficient goes to half its value and the bank to 60°, both over 10 s. Onset times: every second from 60 s before to 8 s after 00:19:29 (69 values). Bank to the left and to the right. That is 138 responses per flight: 552 in the first batch, 11,868 for the other 86 flights.

**To the transmissions.** Each response is propagated to 00:19:37 or to the first stop. The model state and the predicted timing and frequency are recorded at 00:19:29 and 00:19:37 where the response reaches them.

**Beyond 00:19:37.** Each continued response (defined below) goes through the four published stages: to the operating-speed limit; to the onset of drag rise; to Mach 0.89; then, for two bank laws (60° held; roll to wings level over 10 s) and two drag-rise formulations, to the first event or 00:29:37.

### A transition still under way at 00:19:37

For the ten latest onsets (1 s before to 8 s after 00:19:29) the 10 s transition has not finished at 00:19:37. The published continuation function refuses such a response. The three stage drivers behind it do not need that restriction: each builds its dynamics from the fuel-event time and the saved delay and duration of the transition, and each places an integration boundary at the end of the transition. So the transition continues with its original time origin and its remaining duration.

`term_cat.py` therefore sends such a response through the same three stage drivers, entered without the refusal (`Solvers.stages_1_to_3`, a statement-for-statement copy of stages 1 to 3 of the published function), and then through the published function's last stage. A response whose transition has finished goes through the published function as before. Every continuation records which entry was used and which stages began before the transition had ended.

One consequence is flagged and not hidden: if Mach 0.89 is reached before the transition has ended, the roll-out law of the last stage starts from a lift coefficient and bank part-way through the transition. Such results carry `rollout_begins_before_transition_end`.

In the earlier published onset map, none of the 600 responses with these ten onsets met a frequency treatment. Whether any does here is an outcome of the run.

### Limits of what is sampled

- One law before the response (fixed lift coefficient and bank), one response shape, one bank magnitude, two directions.
- Onset times within a 68 s span around the log-on, at 1 s spacing.
- Two bank laws and two drag formulations after Mach 0.89.
- A response outside these is not examined. A result that "no sampled response" meets a requirement is a statement about this family only.

## What is recorded for each response

Each requirement is recorded on its own. The earlier label "compatible" is not used.

| Requirement | Definition | Recorded |
|---|---|---|
| Physical support to 00:19:29 | The propagation reaches 16,706 s without a stop | Yes or no; if no, the stop, its time, state and reason |
| Physical support to 00:19:37 | The same for 16,714 s | As above |
| Timing at 00:19:29 | Recorded 23,000 µs less the 4,600 µs correction for that message type, 18,400 µs (project lineage table), minus the predicted value | Residual in µs. Also against 18,440 µs, the unverified alternative of provenance item P-1 |
| Timing at 00:19:37 | Not evaluated: the project lineage assigns no usable correction to the recorded 49,660 µs | The predicted value is stored |
| Frequency at 00:19:29 and 00:19:37 | Recorded 182 Hz and −2 Hz minus the predicted values, under each of two calibration conventions (the frozen equations; the same with the earlier common offset of 0.554 Hz) | Four residuals, and the predicted change over the 8 s |
| Frequency requirement, four treatments | The existing test (`envelopes.py`), for each calibration convention, with and without an oscillator warm-up offset | Met or not, and the margin in Hz, for each of the four |
| Joint satellite match | Defined below | Met or not, for each timing band and each treatment |
| Electrical sequence | See below | A status and the quantities behind it |

**Joint satellite match.** The 00:19:29 timing within a stated band, plus both final frequency measurements under one named treatment, with propagation supported through both transmissions. The 00:19:37 timing is not part of it. A joint match does not establish an electrical explanation.

Meeting a frequency treatment is never reported as a joint match. The 43 µs and 7 Hz bands of the cruise fit are not used at the final transmissions.

### Timing bands

The project lineage assigns no noise figure to the 00:19:29 timing. For reporting, the residual is compared with 62, 124 and 186 µs: one, two and three times the standard deviation of the timing of that message type (R600). Davey et al., *Bayesian Methods in the Search for MH370* (2016), §5.2 "Burst Timing Offset", gives empirically derived standard deviations of 62 µs for R600 messages, 29 µs for ordinary R1200 messages and 43 µs for anomalous R1200 messages. Codex checked the figure against the book in its review of `2fc9d0e`; I have not opened the book from this session.

The bands are comparisons with a measurement. They are not probabilities assigned to a flight or a location, and they select nothing.

Forming a timing residual at 00:19:37 later would need a declared, sourced correction and an explicit amendment. The stored prediction makes that possible without recomputation.

### Frequency treatments

The warm-up treatment allows a common offset of 17 to 136 Hz at the log-on, falling by 0 to 6 Hz by the acknowledgement, on top of the error bounds; the treatment without warm-up allows the error bounds only. The ranges are those of Holland (2017), as implemented in the existing module. Which treatment applies depends on how long the satellite unit had been without power, which this model does not determine.

### Electrical sequence

The model has one aggregate fuel event and no electrical system. For each response the record holds the time from the fuel event to 00:19:29 and the APU fuel remaining in the model at each transmission, and one of three statuses:

| Status | Meaning |
|---|---|
| `CONDITIONAL` | The model's APU fuel lasts past both transmissions. An electrical explanation would still depend on every assumption listed in `FUEL_POWER_ACCOUNT.md` |
| `MODEL_APU_FUEL_EXHAUSTED_BEFORE_A_FINAL_TRANSMISSION` | Under the model's 15 lb reserve and its burn rate, the APU fuel is gone before a transmission it would have to power |
| `NOT_EVALUATED` | The response does not reach the transmissions |

No status says an electrical explanation is established, and none can: the 6.80 kg reserve is imposed by the cruise model and is not evidence that an APU started.

### Which responses are continued

A response is continued beyond 00:19:37 if it is supported to 00:19:37 and meets the frequency requirement under at least one of the four treatments. Timing does not enter this rule. Every response that could satisfy a joint satellite match is therefore among those continued. Timing and electrical status are kept beside each continuation, so that a map can show what each path satisfies.

### Outcome of a response

| Outcome | Kind |
|---|---|
| Stopped before 00:19:29, or between the transmissions, with the limit named | Model limit |
| Supported to 00:19:37, no frequency treatment met | Measurement mismatch |
| Continued | |
| Calculation failed | Recorded with the reason; not retried |

A model-limit stop is an ending the model defines and locates: the lift coefficient reaching the supported maximum, the operating Mach or airspeed limit, the model surface, or the top or lowest level of the weather record. It says where this model can no longer follow the aircraft, and is kept apart from a mismatch with a measurement.

### Failed calculations

A calculation has failed when it did not end in one of the ways the model defines. The wrapper holds the list of defined endings, for an onset run and for each stage of a continuation, and treats every other status as a failure. That includes the reused solvers' own `NUMERICAL_FAILURE`; their two exceptions raised when the model leaves its domain inside a step without the place being located (`AERODYNAMIC_MODEL_DOMAIN_EXCEPTION`, `WEATHER_HORIZONTAL_OR_TIME_DOMAIN`); an exception in the adapter; a deadline; and any status not on the list.

The test is applied to an onset result, to every stage of a continuation and to every ending of its last stage, and inside every gate comparison. A failed calculation

- is recorded with its native status and is never reported as a model-limit stop;
- makes any numerical check it takes part in `FAILED`, whether or not the other calculation failed in the same way;
- is not the basis of a negative result: where onset calculations of a flight or group failed, "none continued" is not claimed for it;
- keeps its batch incomplete (below).

Every published onset and continuation record of the earlier terminal experiments (5,118 and 467) ends in a way on the list. The list errs on the side of failure: an ending the solvers define but the list omits would be reported as failed and would stop the sequence.

### Endings of continued paths

Each stage ends at its own event and is recorded with its state. A path that ends early is kept with that event and is not forced onward.

| Ending | Reported as |
|---|---|
| Lift coefficient at the supported maximum | Last supported airborne state; model limit |
| Lowest level of the weather record | Last supported airborne state, with its height above the model surface. Not water contact |
| Model surface reached inside the weather record | Propagated surface contact |
| 00:29:37 | Airborne at the horizon |

Everything beyond the operating-speed limit depends on an aerodynamic extension outside the range the performance data cover, and beyond Mach 0.89 the aerodynamics are unvalidated. Results from those stages are labelled with that dependence, and the two drag formulations are kept separate.

No analytic tail to the surface is computed. If one is added it will be declared separately and shown apart from the propagated path.

## Gate

Nothing after the gate runs unless every item of it has passed at the current revision of this package. Each item is computed once; an item that did not pass is not repeated at that revision.

| Part | Content | Requirement |
|---|---|---|
| 1a | The three published onset controls recomputed | Every compared field equal to the published record |
| 1b | The published pair of continuations recomputed through all four stages, by the published control routine | Every stage end equal bit for bit, and equal in time, to the published records: all eleven comparisons of the published gate present and true for each of the two. **And** every stage and every ending of the last stage, in each of the four continuations the routine computes, ended in a way the model defines |
| 1c | The new entry (`stages_1_to_3`) on the same published pair, whose transitions had finished | All three stages present, none failed, each with the published status, end time and end state, bit for bit |
| 1d | Two published onset responses whose transition ends 1 s and 5 s after 00:19:37 | See below |
| 2 | The handoff checks of `HANDOFF.md` on the four first-batch flights. No propagation | All met |

**Part 1d, an unfinished transition.** Two published responses are used: left bank with onset 1 s before 00:19:29, and right bank with onset 3 s after. For each, three calculations are made: the onset run; the continuation from its 00:19:37 state through the new entry; and one uninterrupted propagation with the published driver from the fuel event to at least 10 s past the end of the transition. The case passes only if every one of these obligations is met:

| Obligation | Requirement |
|---|---|
| Onset reproduces the published record | Field for field, and the calculation did not fail |
| The case is what it is meant to be | Supported to 00:19:37 with the transition still under way |
| Same configuration | The uninterrupted propagation uses the response configuration of the onset record |
| No failed calculation | Neither the continuation's first stage nor the uninterrupted propagation failed |
| State at 00:19:37 | The uninterrupted propagation's state equals the onset record's, bit for bit |
| **Transition completed in both** | Both calculations reach the end of the transition |
| Agreement at the end of the transition | Position within 1 m, velocity within 0.01 m/s, lift coefficient within 1e-8, lift reference direction within 1e-7, APU fuel within 1e-5 kg (the published continuation-control criteria) |
| Commanded law reached | Lift coefficient within 1e-6 of half the inherited value; bank within 1e-6° of 60° |
| Agreement after the transition | The same criteria 10 s or more after it; or, if the model stops first, the same limit within 0.01 s and the same criteria at the stop |

If either calculation ends before the end of the transition, by a model limit or by a failure, the last four obligations are `UNEXERCISED` and the case does not pass. Two calculations that stop early in the same way agree with each other; that shows nothing about how the transition completes. The gate then does not pass, and other cases would have to be declared in a new revision.

**Part 1b, the raw results.** The published control routine compares state and time. For the three stage ends, and for the endings at the later horizon that have no later published record, it does not compare the ending status, and it hands back only a table of true and false. A calculation that failed while keeping the reference state and time would be true in that table. The wrapper therefore examines each continuation as the routine's calculation returns it, before the routine sees it: for each of the two controls, the continuation through all four stages to 00:21:37 and the one from the Mach 0.89 state to 00:29:37. A failed or unknown ending in any stage or last-stage ending fails the gate whatever the table says, and is recorded with its native status, its control and its horizon. The result is passed to the routine unchanged.

Parts 1a to 1c show the reused solver still reproduces its known results on this machine. Part 1d shows an unfinished transition is carried on correctly. Part 2 shows the new states enter the solver as intended.

## Sequence

| Step | Work | Begins only if |
|---|---|---|
| 1. Gate | 3 onset controls, 1 pair of continuations, 2 equivalence runs, 2 unfinished-transition cases, 4 handoff evaluations | |
| 2. First batch, onset | 552 | Gate passed |
| 3. First batch, onset half-step checks | 8 owed: each flight and bank direction | All 552 present |
| 4. First batch, continuation | Every continued response | Step 3: all 8 met |
| 5. First batch, continuation half-step checks | 4 owed: one per flight | Step 4 |
| 6. Handoff checks on the other 86 flights | 86 evaluations, no propagation | Controls passed |
| 7. Other 86 flights, onset | 11,868 | **The first batch complete** (steps 2 to 5: every run present, every owed check passed, no failed calculation) and step 6 passed |
| 8. Onset half-step checks | 16 owed: per group and bank direction, the flights with the earliest and the latest fuel event | All 11,868 present |
| 9. Continuation | Every continued response | Step 8: all 16 met |
| 10. Continuation half-step checks | 4 owed: one per group | Step 9 |

If every check is met, the sequence runs to the end without a further decision. Otherwise the steps that depend on it do not start, and what is missing is reported.

### Owed checks

The checks that are owed are fixed by the manifest before anything is computed, and each has an explicit result:

| Result | Meaning | Counts as passed |
|---|---|---|
| `MET` | Compared and within the criteria | Yes |
| `NOT_MET` | Compared and outside the criteria | No |
| `FAILED` | A calculation in the comparison failed or ran past its deadline, at either step | No |
| `INCOMPLETE` | The runs the check needs are not all present | No |
| `NOT_ATTEMPTED` | Not yet computed, or refused by an allowance | No |
| `NONE_CONTINUED` | Continuation check only: with every onset run of the batch present and none of that flight's or group's onset calculations failed, no response of it is continued | Yes |
| `UNDETERMINED` | Continuation check only: no response is continued, but onset calculations of that flight or group failed | No |
| `MISSING` | Gate or handoff item with no stored result | No |

A batch is complete only when every planned onset run and every continuation of a continued response is present, every owed check has passed, and no onset calculation or continuation of the batch failed. Two calculations that both failed are never a pass; nor is a comparison in which nothing was compared.

The remaining flights start only after the first batch is complete in that sense. Within the remaining flights, continuations start when their onset runs are all present and the owed onset checks are met; failed calculations there are counted and reported, and leave that batch incomplete.

**Onset half-step check.** The run is repeated with half the step and tighter tolerances. Required: the same outcome and the same requirements met; position within 1 m, velocity within 0.01 m/s, predicted frequency within 0.01 Hz and predicted timing within 0.1 µs at each transmission reached; for a stopped run, the same limit within 0.01 s. The response checked is the continued one with the earliest onset; where a flight has none in that direction, the earliest supported to 00:19:37; where it has none of those, the latest onset.

**Continuation half-step check.** As the published check: the same ending event, within 0.01 s, 1 m and 0.01 m/s. The response checked is the continued one with the earliest onset, right bank if there is one; for a group, that of the flight with the earliest fuel event that has a continued response.

Each check is tied to the particular response repeated. It is not a statement about the other responses.

## Enforcement

These rules are in the code and are exercised by the offline tests through the same paths the run uses.

**One path for every calculation.** Gate items, handoff evaluations, onset runs, continuations and numerical checks all go through one function. It records the attempt in a journal before computing, runs it under a deadline, stores the result, and records the settlement. A settled attempt is never computed again, by any command, worker or arrangement. Results of gate items and checks are stored once; a report is compiled from the stored results and is not itself evidence.

**Allowances.** Computing time is drawn from a durable account, the production run's with one function changed (`account.py`). A reservation is published before the work it covers is computed. An attempt is admitted only if the reservation covers what has been used, what is in progress, and the attempt's own reservation.

| Allowance | Seconds | For scale |
|---|---|---|
| Gate, with the first-batch handoff | 900 | |
| First batch, onset | 2,400 | Earlier run: 1.64 s per response, 3.2 s at most |
| First batch, checks | 2,400 | |
| First batch, continuation | 6,000 | Earlier run: 9.6 s per continued response, 16.6 s at most |
| Other 86 flights, onset | 60,000 | |
| Other 86 flights, handoff and checks | 3,600 | |
| Other 86 flights, continuation | 72,000 | |

The earlier figures come from flights with about four minutes between fuel event and log-on; here it is up to eight and a half. The allowances are limits and not forecasts. Time is measured around each attempt by the wrapper.

**Reservation and deadline of one attempt.** Onset run 60 s; continuation 300 s; onset half-step 120 s; continuation half-step 900 s; gate items 60 to 300 s; handoff evaluation 30 s. An attempt that reaches its deadline is stopped, recorded as such, charged its full reservation and not retried.

**Interruption.** An attempt that is admitted and does not reach its settlement is charged its full reservation, exactly once, and is left unsettled in the journal; it is not recorded as computed. This holds when the calculation is interrupted, when storing its result fails, and when the process is killed outright. In the first two cases the charge is made at once, before the command's cleanup settles and removes its local account file; in the third the open attempt stays in that file and is charged when it is next opened. If the result had already been stored, it is kept and the attempt is not repeated. It may be admitted once more, marked as a repeat after interruption; after a second interruption it is not attempted again and its run counts as missing. If the local files of the run are lost, every outstanding reservation is charged in full.

**Arrangement.** Onset runs and continuations are divided between two workers by their position in the plan. No other arrangement is accepted. One process computes for at most 6,600 s and then stops admitting; the next process continues with what is unsettled.

**Stop.** A satellite prediction may be requested at 00:19:29 and 00:19:37 only. A request at any other time is recorded as a stop before it is raised, and is raised as an exception that the solvers' ordinary error handling cannot catch. The stop is written locally and into the published account. Every worker meets it at its next attempt and every later command at its start. Only an explicit, recorded resolution lifts it. A file read during the run that is on no frozen list causes the same stop.

**Refusal.** Whether a command may start is decided from stored results before any account is opened or solver imported. A refused command publishes nothing.

**Records.** A stored response is accepted only if it is the planned response of this revision: its identity, its event-state hash, its clock and its revision are checked when it is read.

## Frozen inputs

`DEPENDENCIES.json` lists every source file and every data file read while the solvers are imported and the gate's references are loaded: 36 source files and 25 data files (260 MB), each with its hash. The data include the aircraft performance table, the weather arrays and their configuration, the geoid grid, the satellite ephemeris, the ground station, the frequency model, the event table, and the published records and manifests the gate compares with. The list is part of the revision.

- Before any computing entry point, every listed file must still have its frozen hash.
- The 26 files this calculation shares with the cruise catalogue must have the hashes the catalogue was computed with (`../CRUISE_LEVEL_PRODUCTION_108/ENGINE_DEPENDENCIES.json`). They do.
- During a run, every file the process reads is recorded. One that is on no list stops the run.

The list was collected without evaluating anything. A file first opened only during a calculation would not be on it; the run would then stop at the gate naming the file, and a new revision would be needed.

## 22:41

No satellite prediction, residual or comparison is made at 22:41, and no 22:41 value is printed, stored or used by this package.

The values are, however, in the memory of every process that imports the flight model. Its shared setup loads the project's event table (19 events with their recorded timing and frequency) and an array of recorded frequencies at five times, one of which is 22:41, before any guard of this package exists. The same holds for every earlier run of this flight model. This package therefore does not claim that the measurement is "not read". The addendum of 16 November to `../HOLDOUT_2241_DISCLOSURE/DISCLOSURE.md` records this, with the accesses made while preparing and reviewing this package.

## Reporting

After the run, tables and maps will give:

- model states at the two transmissions, for every response that reaches them;
- responses meeting each requirement, and each joint satellite match, by flight, group, bank direction and onset time, with the limits of the sampled onset times marked where a set touches them;
- for every continued path: last propagated position, time, height, speed and ending reason, by bank law and drag formulation, with timing and electrical status beside it;
- propagated surface contacts, if any, apart from last airborne states;
- responses stopped by a model limit, with the limit; failed calculations and missing runs, by reason;
- the 139 and 37 flights not propagated, with their statuses.

Counts will be given per flight and per group. They are not probabilities, and repeated outcomes within a group are not independent confirmations. Maps will show computed points only, with nothing drawn between clusters.

Outputs not listed here will be declared as additions when they are made. They will be written outside the files that make up the revision.

## Offline tests

`test_term_cat.py`, 91 tests. They import no solver and propagate nothing. The solvers are replaced by stand-ins that return synthetic records, and the remote branch by a directory, so the gate, the batches, the checks, the accounting and the stop are driven through the real dispatch code with the real manifest and plan.

Seventy-two defects were inserted into the wrapper one at a time, each removing or weakening one rule: 36 after the first review and 28 after the second, both sets run against the revision of the second review, and 8 after the third. Seventy-one are caught. The other removes a rule that the failure test now implies (a comparison with nothing in it can no longer arise from results that are not failed), so it changes no behaviour. The stand-in records have the shapes of the reused solvers' own records, and several tests use published records directly.

Not reachable offline, and first exercised in the gate: the handoff evaluation and every call into the existing solvers. The judgements applied to what the gate's calls return are separate functions and are tested offline.

## Known limits of this package

1. **The published force checks** that need the recorded thrust and drag of the last powered stage are replaced, not repeated (`HANDOFF.md`). The replacement checks are consistency and plausibility checks. They are not comparisons against independently recorded powered-flight forces.
2. **Publication during the run.** The wrapper commits and pushes its account, journal, reports and record files as it goes, as the production run did. Responses are stored in files of at most one process each.
3. **Same machine.** Bit-for-bit reproduction of the controls is established on this machine only.
4. **The two unfinished-transition gate cases** are expected to reach the end of their transitions (`REPAIRS_2.md`); that is not known until the gate runs. If one does not, the gate does not pass.
5. **Checkpoint-restart package.** Not run. Its three required repairs are recorded in `../CHECKPOINT_RESTART/REQUIRED_REPAIRS.md`.

## Files

| File | Content |
|---|---|
| `TERMINAL_MANIFEST_266.csv`, `EVENT_STATES_229.json`, `MANIFEST_SUMMARY.json` | The population, the saved states and their hashes |
| `build_manifest.py` | Builds them from the committed catalogue; computes no flight |
| `HANDOFF.md` | Mapping of a saved state into the terminal model |
| `term_cat.py` | The wrapper: gate, batches, checks, records, enforcement |
| `account.py` | The durable account (the production run's, one function changed) |
| `deps.py`, `DEPENDENCIES.json` | The frozen list of source and data files, and how it is collected and verified |
| `test_term_cat.py`, `TEST_TERM_CAT.log` | Offline tests |
| `REPAIRS_1.md`, `REPAIRS_2.md`, `REPAIRS_3.md` | Codex's reviews of `2fc9d0e`, `b742742` and `d1335b4`: each issue, the repair and its test |
| `FUEL_POWER_ACCOUNT.md`, `bookkeeping.py`, `ELECTRICAL_BOOKKEEPING_BY_GROUP.csv` | Sourced account of fuel, power, APU and satellite unit, and the arithmetic by group |
| `run/<revision>/` | Created by the run: account, journal, results, reports, records |

The revision of this package is the hash of `term_cat.py`, `account.py`, `deps.py`, `test_term_cat.py`, `build_manifest.py`, `DEPENDENCIES.json`, the manifest, its summary, the event states, `HANDOFF.md` and this document. It is printed by `python3 -I term_cat.py --phase status`. Everything a run produces is kept under that revision and is not read by another.

## Sources

- Holland, I. D. (2017). *MH370 Burst Frequency Offset Analysis and Implications on Descent Rate at End-of-Flight.* https://arxiv.org/abs/1702.02432
- Davey, S., Gordon, N., Holland, I., Rutten, M., Williams, J. (2016). *Bayesian Methods in the Search for MH370.* Springer. §5.2, "Burst Timing Offset". https://library.oapen.org/handle/20.500.12657/27976
- Project lineage of the measurements: `reports/MEASUREMENT_LINEAGE_TABLE.csv`.
