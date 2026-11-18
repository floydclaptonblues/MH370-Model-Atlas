# Terminal responses of the accepted cruise flights: findings

16 November 2026. Package revision `c370b2cf70b9` (commit `0aa054d`), approved by Codex for its gate. Method: `METHOD.md`. This note reports what was run, what came out, and what can and cannot be read from it.

**Executed.** The gate; the handoff evaluation of all 90 flights; 12,420 onset responses (552 in the first batch, 11,868 for the other 86 flights); 24 onset checks at half step; 1,375 continuations beyond 00:19:37, each with four last-stage variants (5,500 endings); 8 continuation checks at half step; `analyze_term_cat.py`, which reads the stored records and computes no flight.

**Not executed.** No cruise flight was recomputed. The 139 flights whose engine fuel runs out after both final transmissions and the 37 with engines running at 00:40 were not propagated. No timing residual was formed at 00:19:37. No path was extended analytically to the surface. Nothing was evaluated at 22:41: no prediction, residual or comparison. The checkpoint-restart package was not run.

Every position below is a state of this model under its stated assumptions. The collection is a conditional terminal envelope of the sampled responses. It is not a probability map and not an outer bound. Counts are counts of sampled responses, not probabilities; the 90 flights share their fitted cruise measurements, so repeated outcomes are not independent confirmations.

## 1. Gate

Revision confirmed on the execution machine before the run: `c370b2cf70b9`. The 61 frozen source and data files are compared with their recorded hashes every time the solvers are loaded; no difference was found, and no file outside the frozen list was read.

| Gate item | Result |
|---|---|
| Three published onset controls repeated | Reproduced; no field differs; no failed calculation |
| Published continuation pair repeated | 11 of 11 comparisons for each control; the 4 raw continuations all end in ways the model defines |
| Stage drivers entered without the refusal, on a finished transition | Stages 1 to 3 equal to the published function for both cases |
| Unfinished transition, onset 1 s before 00:19:29, left | All nine obligations met |
| Unfinished transition, onset 3 s after 00:19:29, right | All nine obligations met |
| Handoff of the four first-batch flights | 4 of 4 passed |

**Both unfinished transitions completed.** The transitions ended at 16,715.000 s and 16,719.000 s after 19:41:03 (1 s and 5 s after 00:19:37). The continuations ran on to 16,729.9 s and 16,733.9 s, and both were airborne at the comparison times, 10 s after each transition ended. Against the uninterrupted propagation: no difference at the end of the transition; afterwards 2.4e-9 m and 1.5e-8 m in position. Lift coefficient at half its value within 6e-14; bank 60.000000000° in the commanded direction.

Charged to the gate allowance: 19.6 s of 900 s.

## 2. Completion, checks and cost

| | First batch | Other 86 flights |
|---|---|---|
| Flights | 4 | 86 |
| Handoff evaluations passed | 4 | 86 |
| Onset responses planned / present | 552 / 552 | 11,868 / 11,868 |
| Failed calculations | 0 | 0 |
| Onset checks at half step, owed / met | 8 / 8 | 16 / 16 |
| Responses continued | 61 | 1,314 |
| Continuations present / failed | 61 / 0 | 1,314 / 0 |
| Continuation checks at half step, owed / met | 4 / 4 | 4 / 4 |
| Batch complete under the frozen rule | Yes | Yes |

The other 86 flights were started only after the first batch was complete under the rule in the method.

Largest differences in the half-step checks (`RESULTS/NUMERICAL_CHECKS.csv`), against criteria of 1 m, 0.01 m/s, 0.01 Hz, 0.1 µs and 0.01 s:

| Check | Position | Velocity | Predicted frequency | Predicted timing | Stage event time |
|---|---|---|---|---|---|
| Onset runs (24) | 0.0036 m | 0.00002 m/s | 0.00006 Hz | 0.00001 µs | |
| Continuations (8) | 0.0065 m | 0.00025 m/s | | | 0.00001 s |

| Allowance | Limit (s) | Charged (s) |
|---|---|---|
| Gate | 900 | 19.6 |
| First batch, onset | 2,400 | 902.6 |
| First batch, checks | 2,400 | 26.2 |
| First batch, continuations | 6,000 | 193.9 |
| Other flights, onset | 60,000 | 19,281.1 |
| Other flights, checks | 3,600 | 45.6 |
| Other flights, continuations | 72,000 | 4,163.2 |
| Total | 147,300 | 24,632.2 |

No ceiling was reached, no forbidden prediction was requested, no process was interrupted and the run recorded no stop. The onset responses of the other flights took two sessions per worker, because each process stops admitting work after 6,600 s; that is the frozen arrangement and not an interruption.

### 2.1 A defect in the wrapper's publication step: four stored lines lost, one response computed twice

I found this after the run, while checking the journal against the statements in this note. It was not caught by the reviews or the offline tests, and I did not anticipate it.

**What happened.** When a worker publishes, the wrapper commits its files and then runs `git pull --rebase --autostash`. The autostash step briefly resets tracked files in the working tree and then restores them. The other worker appends to the same journal and record files all the time. Whatever it appends inside that brief window is overwritten when the files are restored. This happened twice, each time while one worker was publishing a block of the onset allowance:

| Time (UTC, 17 Nov) | Lost | Consequence |
|---|---|---|
| 02:32:21 | The stored record and the settlement line of `A052_TO275.F1`, left bank, onset +2 s; the admission line of the next response of that flight (onset +4 s) | The response had been computed normally (about 0.9 s) and its result was gone. The next response was computed and stored normally; only its admission line is missing |
| 03:22:37 | The settlement line of the same response, onset +2 s, after it had been computed again | The stored record survived, in a file not yet tracked |

**How the wrapper dealt with it.** At the start of the next session the journal showed onset +2 s admitted and not settled, which is how an interrupted attempt looks. The wrapper admitted it once more as a repeat, as its rule for interrupted attempts allows, computed it (0.89 s) and stored it. When the checks began, the wrapper found the stored result without a settlement line and settled it from the stored result. The response was therefore **computed twice, and the stored result is the second computation**. The rule that a settled result is never computed again was broken in effect, because the settlement line that enforces it had been lost.

**What I checked afterwards, from stored files only.**

- All 13,925 planned identities are settled (12,420 onset responses, 1,375 continuations, 90 handoff evaluations, 24 and 8 half-step checks, 8 gate items). 13,924 have an admission line; the missing one is onset +4 s above. One identity has two admission lines, onset +2 s. There is no other irregularity in the journal.
- Every one of the 12,420 response records and 1,375 continuation records is present exactly once, and every continuation has its trajectory record.
- The workers' own counts agree: in the first session worker 0 computed 4,386 responses and 4,385 were found stored at the next session; worker 1 lost none.
- The account agrees with the journal once the lost lines are added back: 19,281.1 s charged to the onset allowance against 19,279.4 s in the journal plus the two computations of onset +2 s (0.9 s each). Both computations were charged.
- The stored result for onset +2 s lies between its neighbours: predicted frequency at 00:19:37 of 171.3, 188.4 and 201.7 Hz for onsets +1, +2 and +3 s. Its outcome is "no frequency treatment met", like all 180 responses at that onset time. It is not a continued response and takes part in no owed check.

**What I cannot show.** The first result for onset +2 s no longer exists, so I cannot show that the two computations were identical. The controls reproduce bit for bit on this machine, which makes a difference unlikely; it is not demonstrated.

**What it means for the results.** No planned result is missing from the stored records and none is stored twice. One of the 12,420 stored responses comes from a second computation. Every count in this note is a count of the **surviving records**. The counts have not been compared with the lost first result and cannot be: its values and its classification no longer exist. The journal is not a complete record of what was computed: it is short by three lines, and it records as a repeat after interruption something that was not an interruption.

**Permanent provenance exception** (Codex's wording, adopted; listed in `RESULTS/PROVENANCE_EXCEPTIONS.csv` and marked on the row in `RESULTS/RESPONSES.csv`):

> `A052_TO275.F1`, left bank, onset 2 s after 00:19:29. The response was computed twice because publication erased its first stored result and settlement. The second computation is retained. Equality with the lost first computation cannot be established.

Keeping the response does not make the rule "a settled result is never computed again" satisfied in retrospect. For this identity the rule was broken.

**Status after review** (17 November; this paragraph replaces an earlier one, which said the cruise runner had not been examined and suggested taking the wrapper's file lock around publication).

- The frozen wrapper is unchanged, and nothing was recomputed.
- The final published checkpoint of the cruise catalogue has been audited by Codex, read-only, within the scope given in section 2.2. No unexplained missing or duplicated result and no accounting difference was found.
- Taking the wrapper's existing file lock around publication would not have been enough: the compressed records were written without that lock.
- A replacement publication module is under review in `../PUBLICATION_REPAIR/`. No runner uses it. Adopting it requires every writer of a published file, and the snapshot taken for publication, to use one locking arrangement.

### 2.2 Codex's review of commit `9ae03c4`

Relayed by Ryan on 17 November. Codex ran no flight calculation and changed nothing in the repository.

**Disposition.** Keep the surviving second computation, with the provenance exception above. Do not delete it and do not compute it a third time: a deletion would leave a hole, and a third computation would not recover the missing evidence. Repair the publication mechanism in a new revision before any further production with concurrent workers. Keep the frozen code and the raw records as they are.

**What Codex checked for the terminal run**, independently of my script: the whole published journal, the account, the manifest and the separate gate, handoff and check records.

| Check | Codex's result |
|---|---|
| Planned onset identities | 12,420, each with a settlement, none extra |
| Settled identities in all | 13,925, each settled once |
| Distinct identities with an admission | 13,924 |
| Admitted twice | `A052_TO275.F1`, left bank, onset +2 s |
| Admission missing | The same flight and bank, onset +4 s |
| Replacement settlement | Marked as adopted from a stored result |
| Continuation or check depending on the +2 s identity | None |
| Gate, handoff and check records | 130, unique, matching their settled identities |
| Account against the surviving onset settlements | Account larger by 1.756851704 s, consistent with the two computations whose settlement lines were lost; other allowances agree to floating-point precision |

Codex also read the code: publication holds a Git lock, journal lines are appended under a different lock, and the compressed response records are written under neither. It notes that the account is better protected, because it is updated and published under one lock, so the journal race does not show that the account lost anything.

Codex did not reread every compressed response and trajectory record. That every response and trajectory is present exactly once rests on my verification (`verify_findings.py`), not on a second traversal by Codex.

**A point about method.** The number of admission lines in the journal is the expected 13,925: one extra admission and one missing admission cancel. A check of row totals would have passed. Only a check of each identity's history shows the defect. `verify_findings.py` checks identities.

**Codex's read-only audit of the cruise catalogue's published checkpoint** (revision `2a016b1294fa`). I proposed this audit; Codex carried it out. The figures are Codex's and I have not repeated them.

| Check | Codex's result |
|---|---|
| Archives examined, each checked against its Git blob identity | 110 (108 arrivals, the gate, the numerical checks) |
| Archived file members | 593 |
| Ledger files | 134 |
| Expected search identities; saved search records | 848; 848, each once |
| Attempt admissions; completed results | 24,888; 24,886 |
| Unexplained missing or duplicated completed results | 0 |
| Unexplained accounting difference | 0 |

The two admissions without a result are the attempts of `A013` and `A014` interrupted by the machine restart, already recorded in the cruise findings; each was charged its 120 s reservation, and those 240 s are the whole difference between the charges of completed results and the account. Forty searches were resumed: 37 after ordinary pauses, one after a pause during the continuation, and the two restart cases.

Scope, as Codex states it: this clears the final published checkpoint on the checks performed. It does not recover erased local history or certify every earlier version of the checkpoint, and the original workers' local logs were not inspected. Within that scope Codex found no reason to discard or rerun the cruise catalogue. The two runners store their files differently (the cruise runner publishes compressed snapshots; the terminal wrapper published files that both workers kept changing), so sharing the Git command does not mean both had the same incident. Codex found one remaining weakness in the cruise publication: a checkpoint archive is replaced before the publication lock is taken, and the account identifies the archive by its path, not by a hash of its content.

**The repair** is prepared as a separate package, `../PUBLICATION_REPAIR/`, for review. Nothing in this directory's revision files was changed.

## 3. Computed outcomes

### 3.1 What happens to each response

| Outcome | Kind | Responses |
|---|---|---|
| Operating-speed limit reached before 00:19:29 | Model limit; not compared with either transmission | 6,536 |
| Operating-speed limit reached between the two transmissions | Model limit | 1,423 |
| Supported to 00:19:37; no frequency treatment met | Measurement mismatch | 3,086 |
| Supported to 00:19:37 and a frequency treatment met (continued) | | 1,375 |
| Calculation failed | | 0 |
| Total | | 12,420 |

All 7,959 model-limit stops are the operating Mach or airspeed limit, reached 22.6 to 27.3 s after the onset of the response (by group: 25.7 to 27.3 s; 24.9 to 26.3 s; 22.6 to 23.6 s; 23.7 to 24.6 s). No response stopped at the lift limit, the model surface or the weather record before 00:19:37.

By onset time, both bank directions and all 90 flights together (180 responses per onset time; `RESULTS/BY_GROUP_BANK_ONSET.csv`, `RESULTS/OUTCOME_BY_ONSET_TIME.png`):

| Onset relative to 00:19:29 | Outcome |
|---|---|
| −60 to −19 s | All 180 reach the operating-speed limit before 00:19:37. The earliest sampled onset, −60 s, is in this set |
| −18 to −15 s | Some stop at the limit between the transmissions (144, 112, 88, 55); the rest are supported to 00:19:37 and meet no frequency treatment |
| −14 s | 75 continued; 105 meet no frequency treatment |
| −13 s | 162 continued; 18 meet no frequency treatment |
| −12 to −7 s | All 180 continued |
| −6 s | 58 continued; 122 meet no frequency treatment |
| −5 to +8 s | All 180 supported to 00:19:37; none meets a frequency treatment. The latest sampled onset, +8 s, is in this set |

The continued set lies between −14 and −6 s, in both bank directions (by group: −13 to −6; −14 to −6; −14 to −6; −14 to −7 s). It does not touch either end of the sampled onset times. Every one of the 90 flights has 14, 15 or 16 continued responses (30, 5 and 55 flights). Left and right bank give almost the same counts (687 and 688 continued).

### 3.2 Comparison with the two transmissions

**Timing at 00:19:29.** For the 5,884 responses that reach 00:19:29 the residual against 18,400 µs lies between −18.0 and +24.8 µs. Every one is inside the 62 µs band. By group, continued responses only: −9.0 to +21.0; −4.5 to −1.6; +9.0 to +12.2; +20.8 to +24.8 µs. Within one flight the residual varies by at most 2.3 µs across its continued responses, so it is set by the cruise flight and hardly at all by the response. The cruise flights were fitted to the timing at 20:41:05, 21:41:27 and 00:11:00; the 00:19:29 timing was not fitted.

Against the unverified alternative of 18,440 µs every residual is 40 µs larger. Then 363 of the 403 continued responses of the 365.113 hPa Mach 0.75 group lie between 62 and 65 µs, outside the 62 µs band and inside the 124 µs band; all other continued responses stay inside 62 µs.

**Timing at 00:19:37.** Not evaluated. The predicted values are stored.

**Frequency.** With no response yet begun, the model predicts 214 to 245 Hz at 00:19:29 (recorded: 182 Hz), with the aircraft descending at 4 to 13 m/s. Each second of earlier onset lowers the prediction at either transmission by about 24 Hz. The predicted change over the 8 s between the transmissions is −172 to −194 Hz for the continued responses (recorded: −184 Hz).

| Treatment | Responses meeting it | Flights | Onset times | Vertical speed at 00:19:29 | Vertical speed at 00:19:37 |
|---|---|---|---|---|---|
| Frozen equations, no warm-up | 358 | 90 | −8 to −6 s | −16.9 to −28.5 m/s | −70.0 to −83.8 m/s |
| Historical offset, no warm-up | 357 | 90 | −8 to −6 s | −17.0 to −29.0 m/s | −70.0 to −84.2 m/s |
| Frozen equations, warm-up | 1,196 | 90 | −14 to −6 s | −20.9 to −70.0 m/s | −75.2 to −120.6 m/s |
| Historical offset, warm-up | 1,197 | 90 | −14 to −6 s | −22.0 to −70.1 m/s | −75.6 to −120.8 m/s |
| Any of the four | 1,375 | 90 | −14 to −6 s | −16.9 to −70.1 m/s | −70.0 to −120.8 m/s |

In feet per minute the last row is 3,300 to 13,800 at 00:19:29 and 13,800 to 23,800 at 00:19:37. The two calibration conventions differ by one or two responses.

**Joint satellite match** (00:19:29 timing within the band, plus both frequency measurements under the named treatment, with propagation supported through both transmissions). Because every timing residual is inside 62 µs, the joint counts equal the frequency counts in the table above, for all three bands: 1,375 under any treatment; 358 and 357 without warm-up; 1,196 and 1,197 with it. A joint match does not establish an electrical explanation.

### 3.3 Fuel and the electrical status

| Group | Flights | Fuel event before 00:19:29 | Model APU fuel left at 00:19:29 | At 00:19:37 | Status of the continued responses |
|---|---|---|---|---|---|
| 300.9 hPa, Mach 0.78 (33,985 ft) | 13 | 136 to 158 s | 4.20 to 4.55 kg | 4.07 to 4.42 kg | 182 conditional |
| 331.655 hPa, Mach 0.75 (31,946 ft) | 21 | 176 to 198 s | 3.53 to 3.90 kg | 3.40 to 3.77 kg | 336 conditional |
| 365.113 hPa, Mach 0.67 (25,661 ft) | 30 | 377 to 400 s | 0.21 to 0.58 kg | 0.08 to 0.45 kg | 454 conditional |
| 365.113 hPa, Mach 0.75 (31,946 ft) | 26 | 489 to 509 s | 0 | 0 | 403: model APU fuel exhausted before a final transmission |

The model starts each flight's APU account at its 6.80388555 kg reserve at the fuel event. "Conditional" means only that this reserve, at the model's burn rate, lasts past both transmissions; it depends on every assumption in `FUEL_POWER_ACCOUNT.md` and makes no claim that an APU started. Every interval here is longer than 120 s; that is a reported difference, not an exclusion. At the model's burn rate (0.0165 kg/s) the reserve lasts 412 s from the fuel event. In the Mach 0.67 group that puts its end about 5 to 27 s after 00:19:37 (arithmetic from the fuel left at 00:19:37 and the burn rate).

### 3.4 Where the model puts the aircraft

Positions of the continued responses (`RESULTS/MAP_POSITIONS_AT_0019_29.png`, `RESULTS/MAP_OVERVIEW.png`):

| Group | At 00:19:29, latitude | Longitude | Height | At 00:19:37, height |
|---|---|---|---|---|
| 300.9 hPa, Mach 0.78 | 36.69 to 36.71°S | 90.42 to 90.53°E | 30,000 to 31,500 ft | 27,600 to 30,200 ft |
| 331.655 hPa, Mach 0.75 | 35.50 to 35.76°S | 91.85 to 92.22°E | 27,000 to 28,100 ft | 24,700 to 26,900 ft |
| 365.113 hPa, Mach 0.67 | 32.27 to 32.58°S | 95.66 to 95.99°E | 15,100 to 16,500 ft | 12,600 to 15,400 ft |
| 365.113 hPa, Mach 0.75 | 35.50 to 35.79°S | 91.70 to 92.10°E | 18,500 to 19,800 ft | 16,000 to 18,500 ft |

The largest separation between two positions at 00:19:29 within a group is 12, 45, 47 and 48 km. That spread comes from the different cruise flights of the group; one flight's responses lie within a few kilometres of each other. The two Mach 0.75 groups overlap (centres 11 km apart). The 300.9 hPa group is about 175 km to their south-west. The Mach 0.67 group is about 500 km to their north-east.

### 3.5 How the continued paths end

All 1,375 continuations went through the published four-stage function and reached the last stage: the operating-speed limit, then the onset of drag rise, then Mach 0.89. None ended early. Endings of the last stage (`RESULTS/CONTINUATION_ENDINGS.csv`, `RESULTS/MAP_LAST_PROPAGATED_POSITIONS.png`):

| Group | Lift-support limit of the model, airborne | Lowest level of the weather record |
|---|---|---|
| 300.9 hPa, Mach 0.78 | 728 | 0 |
| 331.655 hPa, Mach 0.75 | 1,334 | 10 |
| 365.113 hPa, Mach 0.67 | 0 | 1,816 |
| 365.113 hPa, Mach 0.75 | 707 | 905 |
| All | 2,769 | 2,731 |

No path reached the model surface inside the weather record, so there is **no propagated surface contact**. No path was still airborne at 00:29:37.

| Ending | Height above the model surface | Time after 00:19:37 | Distance from the position at 00:19:37 | Mach | Vertical speed |
|---|---|---|---|---|---|
| Lift-support limit, 300.9 hPa group | 6.0 to 6.6 km | 13 to 22 s | 2.9 to 4.8 km | 0.97 | −162 to −188 m/s |
| Lift-support limit, 331.655 hPa group | 4.2 to 5.2 km | 15 to 27 s | 3.3 to 5.5 km | 0.97 | −151 to −195 m/s |
| Lift-support limit, 365.113 hPa Mach 0.75 group | 0.8 to 1.7 km | 21 to 31 s | 4.6 to 6.0 km | 0.97 | −122 to −177 m/s |
| Lowest weather level, Mach 0.67 group | 219 to 232 m | 23 to 34 s | 4.6 to 7.0 km | 0.94 to 0.97 | −45 to −172 m/s |
| Lowest weather level, 365.113 hPa Mach 0.75 group, bank held | 219 to 232 m | 28 to 36 s | 5.4 to 7.0 km | 0.96 | −133 to −155 m/s |
| Lowest weather level, 365.113 hPa Mach 0.75 group, roll to wings level | 219 to 232 m | 115 to 199 s | 21 to 39 km | 0.68 to 0.81 | −3 to −80 m/s |
| Lowest weather level, 331.655 hPa group, roll to wings level, pinned drag rise (10 endings of 4 flights, right bank, onsets −9 to −6 s) | 219 to 232 m | 380 to 383 s | 76 km | 0.60 | −35 m/s |

Last propagated times run from 00:19:50 to 00:26:00. Ranges of the last propagated positions by group: 36.72 to 36.76°S, 90.39 to 90.56°E; 35.54 to 35.90°S, 91.35 to 92.25°E; 32.29 to 32.62°S, 95.61 to 96.05°E; 35.48 to 35.83°S, 91.32 to 92.52°E.

Effect of the two choices after Mach 0.89 on the last position of one response:

| Group | Between the two bank laws | Between the two drag formulations |
|---|---|---|
| 300.9 hPa, Mach 0.78 | 0.14 to 0.20 km | 0.19 to 0.23 km |
| 331.655 hPa, Mach 0.75 | 0.13 to 71 km | 0.20 to 72 km |
| 365.113 hPa, Mach 0.67 | 0.11 to 1.0 km | under 0.02 km |
| 365.113 hPa, Mach 0.75 | 16 to 34 km | 1.0 to 34 km |

Where the model ends at the lift-support limit the four variants agree within a few hundred metres, because the path ends before they can diverge. Where a roll to wings level lets the model recover from the dive, the last position moves by tens of kilometres and depends on the drag formulation.

### 3.6 Flights not propagated

`RESULTS/FLIGHTS_NOT_PROPAGATED.csv` lists the 139 flights whose engine fuel runs out after both final transmissions and the 37 with engines running at 00:40:00, with their groups, levels and fuel-event times. A fuel event after a transmission cannot have caused a response before it; that is all these statuses say. The flights are not rejected under another electrical or control sequence, which this method does not examine.

## 4. Interpretation

These are readings of the outcomes above. They hold for this response family and these 90 flights.

1. **In this response family, the two frequency measurements pick out a narrow range of onset times, and the same one for every flight.** A response of this shape (lift coefficient to half and bank to 60° over 10 s) meets a frequency treatment only when it begins 6 to 14 s before 00:19:29; without the warm-up allowance, 6 to 8 s before. This follows from the shape: the frequency depends mainly on vertical speed, the shape fixes how fast the descent steepens, and so the measurements fix when it began. A different response shape would give a different range. The result does not say that a response began then.

2. **The 00:19:29 timing does not separate anything here.** All residuals are within 25 µs, so each joint match is decided by frequency alone. The timing residual is a property of the cruise flight. That all 90 flights meet an unfitted measurement within 25 µs is a consistency of the cruise catalogue with the seventh arc; it is one shared outcome, not 90 confirmations.

3. **More than half of the sampled responses were not compared with the measurements at all.** A response beginning more than 22 to 26 s before 00:19:29, depending on the group, reaches the operating-speed limit first, where this stage of the model stops. Those 6,536 responses are neither supported nor contradicted by the transmissions. Earlier onsets are a limit of the model, not a mathematical exclusion.

4. **The geographic spread is set by the cruise flights, not by the terminal response.** Each group forms one cluster 12 to 48 km long at 00:19:29. With the bank held, the last propagated position is 3 to 7 km from the position at 00:19:37. Only the roll-to-wings-level variants move further, up to 39 km in one group and 76 km for ten endings in another. Nothing is implied between the clusters: cruise levels and speeds between the tested ones have not been computed.

5. **About half of the continued paths end in the air, where the model stops.** 2,769 endings are at the lift-support limit, 0.8 to 6.6 km above the model surface, at Mach 0.97 and descending at 120 to 195 m/s. The model does not say where these reach the surface. The other 2,731 end at the lowest level of the weather record, about 220 to 230 m above the model surface; that is not water contact. Everything after the operating-speed limit rests on an aerodynamic extension outside the performance data, and beyond Mach 0.89 the aerodynamics are unvalidated.

6. **The electrical status differs by group.** For the 26 flights of the 365.113 hPa Mach 0.75 group the model's APU reserve is gone about 76 to 96 s before 00:19:29, so their 403 continued responses carry no conditional electrical account in this model. For the Mach 0.67 group the reserve lasts past both transmissions by seconds to tens of seconds. The grouping is an observed association between cruise level, fuel-event time and reserve; the reserve itself is an assumption of the cruise model.

## 5. Query on the finished results

The rectangle 32 to 33°S, 94 to 96°E was applied to the finished tables. It entered no calculation, selection or rule.

| | Inside | Of |
|---|---|---|
| Responses supported to 00:19:29, position at 00:19:29 | 1,860 | 5,884 |
| Continued responses, position at 00:19:37 | 454 | 1,375 |
| Last propagated positions | 1,672 | 5,500 |

All of these belong to the Mach 0.67 group at 365.113 hPa (25,661 ft): its 30 flights lie inside the rectangle at both transmissions, and 1,672 of its 1,816 last propagated positions are inside; the other 144 are east of 96°E, the furthest at 96.05°E. No position of the other three groups is inside. This is a count on sampled model states. It is not a probability, and it does not rank the groups.

## 6. Limits

- One law before the response, one response shape, one bank magnitude, two directions, onset times from −60 to +8 s at 1 s spacing. "No sampled response" is a statement about this family.
- The onset stage stops at the operating-speed limit, so onsets earlier than about −26 s are not compared with the measurements.
- The frequency test and its warm-up ranges are those of Holland (2017) as implemented in the existing module. Which treatment applies depends on how long the satellite unit had been unpowered, which this model does not determine.
- The 00:19:37 timing is not used.
- The handoff checks are consistency and plausibility checks, not comparisons with recorded powered-flight forces (`HANDOFF.md`).
- No surface position is computed. Last positions are last model states.
- Bit-for-bit reproduction of the controls is established on this machine only.
- The journal of attempts is incomplete by three lines (section 2.1).
- The 22:41 measurement was excluded: no prediction, residual or comparison. It is not described as unread; the flight model loads the event table and a five-epoch array of recorded frequencies, including 22:41, when it is imported (`../HOLDOUT_2241_DISCLOSURE/DISCLOSURE.md`).

## 7. Deviations and corrections

1. **Lost lines in the journal and one response computed twice.** Section 2.1. A defect of the wrapper's publication step, found after the run. The surviving response is kept under a permanent provenance exception (section 2.2).
2. **Analysis script written after the run began.** `analyze_term_cat.py` was written while the onset responses of the other flights were running, after I had seen the first-batch results. It is not part of the revision and changes nothing the run used. The table layout follows the method's "Reporting" section.
3. **Additions to the declared outputs.** Not listed in the method: the outcome-by-onset-time figure; the largest separations within a group and between variants; the query rectangle of section 5; the vertical speeds by treatment.
4. **Correction to my interim report.** I gave the continued onset times of `A006_TO250.F3` as −14 to −7 s. The computed range is −13 to −7 s.
5. **The unfinished-transition entry was not used in production.** No response with an onset from −1 to +8 s met a frequency treatment, so all 1,375 continuations went through the published function. The entry was exercised in the gate only. No continuation carries the flag `rollout_begins_before_transition_end`.
6. **Earlier mistake, before approval.** A refused command run to demonstrate the refusal opened and published an empty account for an intermediate revision. It was removed and the cause repaired before this revision was frozen (`REPAIRS_1.md`).

## Appendix A. Hypotheses not supported, and why

| Hypothesis | Status in this run | Reason |
|---|---|---|
| A response of this shape beginning at or after 5 s before 00:19:29 meets the final frequencies | Not supported for any of 90 flights | The descent has not steepened enough by 00:19:37: predicted 23 to 243 Hz there against −2 Hz recorded. Measurement mismatch under all four treatments |
| A response of this shape beginning 15 to 18 s before 00:19:29 meets the final frequencies | Not supported | Where the response is supported to 00:19:37, the predicted frequency is too low at both transmissions (−96 to +3 Hz at 00:19:29) for every treatment |
| A response beginning 19 s or more before 00:19:29 | Not examined against the measurements | The operating-speed limit is reached before 00:19:37, where this stage of the model stops. Model limit, not a mismatch |
| The 00:19:29 timing narrows the set of responses | Not supported | Every residual is within 25 µs of 18,400 µs |
| A response whose transition is still under way at 00:19:37 can meet the frequencies | Not supported in this family | None of the 1,800 responses with onsets −1 to +8 s met a treatment, as in the earlier published onset map |
| The continued paths give surface positions | Not supported | No path reaches the model surface; half end at the lift-support limit in the air |

## Appendix B. Audit trail

| Item | Where |
|---|---|
| Method, repairs, handoff, fuel and power account | `METHOD.md`, `REPAIRS_1.md` to `REPAIRS_3.md`, `HANDOFF.md`, `FUEL_POWER_ACCOUNT.md` |
| Gate results | `run/c370b2cf70b9/GATE_RESULT.json`, `CONTINUATION_CONTROL_GATE.json` |
| Handoff evaluations | `run/c370b2cf70b9/HANDOFF_CHECKS_first.json`, `HANDOFF_CHECKS_rest.json` |
| Half-step checks | `run/c370b2cf70b9/HALF_STEP_CHECKS_*.json`, `CHAIN_HALF_STEP_CHECKS_*.json` |
| Account, journal of attempts, stored results | `run/c370b2cf70b9/ACCOUNT.json`, `journal.jsonl`, `results.jsonl` |
| Response and continuation records, with trajectories | `run/c370b2cf70b9/records/` |
| Every response, one row each (12,420) | `RESULTS/RESPONSES.csv` |
| Every ending of every continued path (5,500) | `RESULTS/CONTINUATION_ENDINGS.csv` |
| By group, bank direction and onset time | `RESULTS/BY_GROUP_BANK_ONSET.csv` |
| By flight; by group | `RESULTS/SUMMARY_BY_FLIGHT.csv`, `RESULTS/SUMMARY_BY_GROUP.csv` |
| Flights not propagated (176) | `RESULTS/FLIGHTS_NOT_PROPAGATED.csv` |
| Numerical checks | `RESULTS/NUMERICAL_CHECKS.csv` |
| Counts, cost and the query | `RESULTS/RESULTS_SUMMARY.json` |
| Provenance exceptions (1) | `RESULTS/PROVENANCE_EXCEPTIONS.csv` |
| Maps and figure | `RESULTS/MAP_OVERVIEW.png`, `MAP_POSITIONS_AT_0019_29.png`, `MAP_LAST_PROPAGATED_POSITIONS.png`, `OUTCOME_BY_ONSET_TIME.png` |
| Tables and maps produced by | `analyze_term_cat.py` |
| Independent recomputation of this note's main figures from the records and the journal: 26 comparisons, all in agreement | `verify_findings.py`, `VERIFY_FINDINGS.log` |

The analysis script's conversion from Earth-fixed coordinates was checked against the latitude, longitude and height the solver itself recorded: 465 states at the transmissions and 244 endings of the first batch agree to within 1e-13 degrees and under a millimetre.
