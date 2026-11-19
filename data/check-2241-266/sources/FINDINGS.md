# The ground-station log set beside the project's inputs and results

18 November 2026. Workbook `35200217_Logs_for_SITA_08Mar2014p_2.xlsx`, supplied by Ryan Hall as the full unredacted Inmarsat log for 9M-MRO (SHA-256 `61e662fe…2dce38b`; 7,196 signalling units from 00:51 UTC on 7 March to 01:16 UTC on 8 March 2014). The workbook is kept on the computing machine and is not in this repository. It was first opened after the 22:41 comparison was complete.

**Corrected the same evening, after Codex's audit of the same workbook.** The first version of this note said that all 19 entries of the project's event table were found in the log "with the same frequency and timing". That was wrong for two of them. Seventeen entries are single received units, and those are equal. The other two are voice calls, and each is the rounded mean frequency of many units; my script had matched one unit to each and called it equal. Codex's audit found the true make-up of those two entries, and I have checked each of its statements against the workbook here. Section 1 is rewritten, section 1a and section 1b are new, and the largest time difference in section 1 is corrected from 0.64 s to 0.10 s. No number in sections 2 to 4 changed.

**Interpretation corrected on 18 November 2026 (America/Chicago), after review.** The earlier wording treated the 20 µs reporting grid as a bound on the true timing, treated descriptive log dispersion as a calibrated error scale for the 22:41 burst, and confused the excess beyond the 43 µs criterion with the full residual. It also overstated what could be inferred about timestamp effects. Those interpretations are withdrawn below. The recorded numbers, numerical table entries, source code, frozen inputs, predictions and labels are unchanged: 215 histories meet the fixed criterion and 51 do not. This documentation correction requires no new flight calculation.

**Executed:** `crosscheck.py`, which reads recorded values and stored model results and does arithmetic on them. No flight model was imported, no flight was computed and no prediction was formed. **Not executed:** any recalibration, any refit, any change to a label.

## 1. The project's event table against the log

The table has 19 entries (`EVENT_CROSSCHECK.csv`, with the worksheet row of each).

**Seventeen are single received units.** Each was found exactly once in the log on the stated channel, with the same burst frequency offset and the same raw burst timing offset. They include every timing measurement the cruise catalogue, the 22:41 check and the terminal study were compared with:

| Time, UTC | Log time | Worksheet row | Timing offset, µs | Frequency offset, Hz |
|---|---|---:|---:|---:|
| 18:25:27 | 18:25:27.421 | 7007 | 17,120 (12,520 after the published 4,600 µs correction) | 142 |
| 19:41:03 | 19:41:02.906 | 7126 | 11,500 | 111 |
| 20:41:05 | 20:41:04.904 | 7128 | 11,740 | 141 |
| 21:41:27 | 21:41:26.905 | 7130 | 12,780 | 168 |
| 22:41:22 | 22:41:21.906 | 7132 | 14,540 | 204 |
| 00:11:00 | 00:10:59.928 | 7187 | 18,040 | 252 |
| 00:19:29 | 00:19:29.416 | 7188 | 23,000 (18,400 after the same correction) | 182 |
| 00:19:37 | 00:19:37.443 | 7194 | 49,660 (not used for timing) | −2 |

So the 22:41 comparison used the value in the log, with no correction, as the protocol declared. The 4,600 µs correction of the two log-on requests is the investigation's published one; nothing in this workbook was used to derive it.

**One difference, in the times.** The event table carries each time to the whole second, the log to the millisecond. The table's second is the log's time rounded to the nearest second, so the model evaluates each single unit between 0.46 s before and 0.10 s after the logged time; for the five hourly exchanges it is 0.07 to 0.10 s after. This was not known to me when the protocol was written. Section 4 gives a rough scale comparison at 22:41, not a calculation of its effect on any flight. For the two final transmissions the model's times are 0.416 s and 0.443 s before the logged ones; the difference between those shifts is 0.027 s. The terminal study samples response onset at 1 s spacing, but that spacing does not bound the change in a predicted timing or frequency caused by shifting a measurement epoch by about 0.4 s. Those effects remain uncomputed.

## 1a. The two voice-call entries: the values are right, their description is incomplete

Found by Codex's audit; each line below was checked here against the workbook.

| Entry | Units averaged | Channels | Mean frequency offset | Table value | Span of the units, UTC |
|---|---:|---|---:|---:|---|
| 18:39:58 | 51 | IOR-3730 (29) and IOR-373E (22) | 87.8235 Hz | 88 Hz | 18:39:55.354 to 18:40:56.354 |
| 23:14:03 | 29 | IOR-3737 (29) | 217.2759 Hz | 217 Hz | 23:14:00.904 to 23:15:02.032 |

The rounded means reproduce the table's values. Three things about them are not said by the table:

- The 18:39 entry names one channel, IOR-373E. Its mean is taken over both channels of the call.
- Both means include call-progress messages as well as telephony acknowledgements (at 18:39: 17 acknowledgements and 34 call-progress units; at 23:14: 9 and 20).
- Each mean spans about a minute. The table's times, 18:39:58 and 23:14:03, are representative instants and not the time of each unit. Single units in those minutes range from 86 to 90 Hz and from 216 to 222 Hz.

None of these units carries a timing offset. **This is a clarification of provenance. The frozen values and times are not changed by it.** Whether using the individual units at their own times would alter any fitted flight is a separate calculation and was not made. The 266 cruise flights were accepted on timing at 20:41, 21:41 and 00:11, where neither voice call enters.

## 1b. No later response from the aircraft

The last unit received from the aircraft in the log is the acknowledgement at 00:19:37.443 (worksheet row 7194). The log continues to 01:16:15 with four more units. All four are transmissions from the ground station (three log-on interrogations and one acknowledgement), and none carries a timing or frequency offset. The workbook holds no response from the aircraft after 00:19:37.443.

## 2. The grid on which the log reports its measurements

Every one of the 816 timing offsets recorded on the R channel, the channel of all the timing measurements above, is a whole multiple of 20 µs. Every frequency offset is a whole number of hertz (`REPORTING_GRID.csv`). This is the resolution of the reported timing estimate. The log does not specify the quantiser's rounding rule, and the estimate also contains measurement error. A reported 14,540 µs therefore does not confine the true physical BTO to a 20 µs interval.

The [ATSB's BTO characteristics factsheet](https://www.atsb.gov.au/publications/educational-fact-sheet/2022/aviation/mh370-burst-timing-offset-bto-characteristics) identifies the 20 µs GES measurement quantisation as one of several error components. The 43 µs statistic used in the project's tolerance comes from the factsheet's measured error distribution, which already includes the quantisation. The reporting step is not an additional allowance to add to the fixed ±43 µs criterion.

Twenty microseconds of two-way timing corresponds to about 3 km in satellite slant range. This conversion is not a bound on the timing error or on horizontal position.

## 3. Dispersion in the selected log samples

From 16:00:13 to 16:11:13 UTC the aircraft was at Kuala Lumpur before departure, logged on through the Indian Ocean satellite. **It is assumed to be stationary in those eleven minutes.** The log does not hold its position. This interval lies within the half hour before take-off used in the investigation's timing calibration. [Ashton et al., *The Search for MH370*](https://www.cambridge.org/core/journals/journal-of-navigation/article/search-for-mh370/D2D1C4C99E7BFDE35841CFD70081114A), report seventeen calibration measurements, a mean bias of −495,679 µs, and a largest error of 17.7 km in the two-way path, equivalent to about 59 µs. That is a peak error, not a standard deviation, and does not validate a standard deviation for the present sample or the later flight.

The recorded timing has a fitted trend of 4.9 µs a minute in the selected interval. The recorded frequencies stay between 84 and 104 Hz until 16:30 and are between 123 and 160 Hz from 16:41:52, around take-off. These observations provide context but do not themselves establish stationarity or separate satellite motion from measurement error. The interval contains 48 R-channel records at 1,200 bit/s:

| Descriptive statistic | Records or pairs | Dispersion, µs |
|---|---:|---:|
| The 48 values as they are (14,740 to 14,900 µs) | 48 | 32.9 |
| Residuals about a straight line fitted in time | 48 | 29.3 |
| From differences of consecutive records within 2 s, at the gate | 28 pairs | 40.5 |
| The same, over the whole log | 270 pairs | 29.1 |

These are descriptive calculations on the selected records. The script divides the sum of squared deviations by the number of values, including after the straight-line fit; it does not make a degrees-of-freedom adjustment. The pair figures divide the dispersion of the differences by the square root of two. Interpreting them as the error of an individual measurement would require assumptions about equal error distributions, independence and negligible physical change between the paired records. Some records occur in more than one pair.

The first three rows concern the selected interval; the fourth uses the whole log, including other times and channels. Within the 48-record interval, 39 records are on IOR-R1200-0-36D3 (channel unit 8) and nine on IOR-R1200-0-36E3 (unit 11), across several message types. The 22:41 measurement is on IOR-R1200-0-36ED (unit 4). These differences, the selected interval and the unverified error assumptions limit transfer of the 29 to 40 µs figures to that measurement. They are not a calibrated in-flight error distribution.

The fixed ±43 µs criterion is numerically about 1.1 to 1.5 times these dispersion figures, or 1.5 times the 29.3 µs value used below. Those ratios are descriptive, not normal-distribution significance levels or probabilities. Reporting quantisation is already present in the logged samples and in the ATSB provenance of the criterion; it supplies no separate allowance.

The 600 bit/s calculation gives 26.9 µs from 58 pairs. The pairing and repeated values alone do not establish that the pairs are mostly units of a single burst or that they measure independent errors. This note does not adopt that figure as the channel's error standard deviation. Each hourly timing comparison uses one recorded unit; the dispersion of its in-flight error has not been calibrated by this exercise.

## 4. The project's results in the units of the log

Residuals are recorded minus predicted timing, over the 266 accepted cruise flights (`RESULTS_AGAINST_LOG.csv`):

| Time, UTC | Role | Residuals, µs | Residual divided by 29.3 µs | Within ±43 µs |
|---|---|---:|---:|---:|
| 20:41:05 | fitted | −42.0 to +20.7 | −1.4 to +0.7 | 266 |
| 21:41:27 | fitted | −16.5 to +34.6 | −0.6 to +1.2 | 266 |
| 22:41:22 | not fitted | −47.2 to +13.3 | −1.6 to +0.5 | 215 |
| 00:11:00 | fitted | −28.4 to +41.4 | −1.0 to +1.4 | 266 |

At the fitted times the residuals approach the edge of the band on one side or the other (−42.0 at 20:41, +41.4 at 00:11). At 22:41 the residuals of the same flights run 4.2 µs past the lower edge. The spread of the 266 residuals at 22:41 (60 µs) is about the same as at the fitted times (51 to 70 µs). The fourth column retains the arithmetic division by 29.3 µs: −1.6 at the most negative 22:41 residual and about 1.4 in magnitude at the fitted-time edges. It does not express calibrated standard deviations of those in-flight measurements.

**Sensitivity of the fixed rule to an illustrative offset** (`LABEL_SENSITIVITY_2241.csv`). This arithmetic holds every prediction fixed and adds the listed offset to the comparison's reference value. The rows are not alternative observations or a probability distribution for the measurement:

| Illustrative offset to the reference value | Flights within ±43 µs | Outside |
|---:|---:|---:|
| −20 µs (one grid step) | 89 | 177 |
| −10 µs (half a step) | 172 | 94 |
| −5 µs | 199 | 67 |
| −1 µs | 207 | 59 |
| 0 (as recorded) | 215 | 51 |
| +1 µs | 229 | 37 |
| +2 µs | 241 | 25 |
| +5 µs | 266 | 0 |
| +10 µs (half a step) | 266 | 0 |

Across the illustrative offsets from −10 to +10 µs, the count inside the band runs from 172 to 266. The non-grid offsets, including ±1 µs and half a step, do not produce readings on the log's observed 20 µs grid. They describe sensitivity of the classification rule and are not possible quantised log readings or probabilities. The actual recorded value still gives 215 within the criterion and 51 outside.

For those 51 histories, about 0.03 to 4.20 µs is the **excess beyond the 43 µs boundary**. Their full residuals are about 43 to 47 µs in magnitude. It is incorrect to describe those residuals as inside one 20 µs reporting step or far inside the selected sample's dispersion. A small excess beyond a chosen criterion does not itself establish that a history is physically possible.

**The time stamp.** The model evaluates the exchange at 22:41:22.000; the log stamps the burst at 22:41:21.906, 0.094 s earlier. Differences between the recorded values at 21:41, 22:41 and 00:11 give average slopes of 0.49 to 0.65 µs per second over those long intervals. Multiplying them by 0.094 s gives about 0.05 to 0.06 µs as a rough scale comparison. These are neither the local derivative of any flight's prediction nor a bound on its change when evaluated at the logged time. The nearest excess is 0.033 µs, but this arithmetic does not determine whether its label, or any other label, would change. No prediction was recomputed at the logged time, and the log does not state which instant of the burst its stamp marks.

## 5. What follows, and what does not

- The seventeen individual measurements match the supplied log, and the two voice-call means are reproduced. This supports their transcription and aggregation; the description of the two means requires section 1a's qualifications.
- **The fixed 22:41 result remains 215 histories within the criterion and 51 outside.** The log's reporting resolution and this descriptive dispersion analysis do not cancel the 51 failures or establish those histories' physical feasibility. Failure of this criterion also does not, by itself, prove physical impossibility.
- Meeting the criterion does not confirm the 215 histories, their probabilities or their locations. The ratios to 29.3 µs and the illustrative offset counts are not calibrated likelihoods.
- Quantisation is already included in the ATSB error-statistic provenance of the fixed criterion. No extra grid or scatter allowance is added, and no frozen label changes.
- The effects of using the logged millisecond epochs remain uncomputed. Neither the hourly finite differences nor the terminal onset grid supplies a bound on those effects.
- Nothing in this note establishes an aircraft position or an impact location.

## 6. Considered and not supported, or not done

| Idea | Status | Reason |
|---|---|---|
| Use the 600 bit/s pair estimate as that channel's calibrated error | Not supported | Nearby records and repeated values do not establish independent errors, equal distributions or negligible physical timing changes |
| State how often a flight on the true path would fall outside ±43 µs | Not established | It requires a justified in-flight error distribution. The selected log dispersion and the overlapping pairs do not provide one; no normal-distribution failure probability is inferred |
| Re-label the 22:41 outcomes with a band widened by the grid or the scatter | Not done | Quantisation is already part of the criterion's stated error provenance. An additional allowance is not justified here; the criterion was fixed before the predictions |
| Recompute the predictions at the logged times | Not done | It needs the flight model and a new declared run |
| Check the timing calibration against the 48 records at the gate | Not done | It needs the satellite model and the aircraft's gate position; a separate task |
| Effect of the 0.4 s time difference at the final transmissions on the terminal results | Unknown; not computed | The 1 s onset spacing does not bound the change in a prediction with measurement time. A calculation or a justified local bound would be needed to quantify it; correcting this note requires no new flight |

## Files

`crosscheck.py`; `SUMMARY.json`; `EVENT_CROSSCHECK.csv` (19 entries: 17 single units and 2 means); `REPORTING_GRID.csv`; `BURST_SCATTER.csv`; `RESULTS_AGAINST_LOG.csv`; `LABEL_SENSITIVITY_2241.csv`. The tables hold recorded values from the supplied log and results already in this repository.
