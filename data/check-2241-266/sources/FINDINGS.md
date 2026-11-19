# The ground-station log set beside the project's inputs and results

18 November 2026. Workbook `35200217_Logs_for_SITA_08Mar2014p_2.xlsx`, supplied by Ryan Hall as the full unredacted Inmarsat log for 9M-MRO (SHA-256 `61e662fe…2dce38b`; 7,196 signalling units from 00:51 UTC on 7 March to 01:16 UTC on 8 March 2014). The workbook is kept on the computing machine and is not in this repository. It was first opened after the 22:41 comparison was complete.

**Executed:** `crosscheck.py`, which reads recorded values and stored model results and does arithmetic on them. No flight model was imported, no flight was computed and no prediction was formed. **Not executed:** any recalibration, any refit, any change to a label.

## 1. The project's event table equals the log

All 19 events of the project's canonical event table were found in the log on the stated channel, each with the same burst frequency offset and the same raw burst timing offset (`EVENT_CROSSCHECK.csv`). That includes every measurement the cruise catalogue, the 22:41 check and the terminal study were compared with:

| Time, UTC | Log time | Timing offset, µs | Frequency offset, Hz |
|---|---|---:|---:|
| 19:41:03 | 19:41:02.906 | 11,500 | 111 |
| 20:41:05 | 20:41:04.904 | 11,740 | 141 |
| 21:41:27 | 21:41:26.905 | 12,780 | 168 |
| 22:41:22 | 22:41:21.906 | 14,540 | 204 |
| 00:11:00 | 00:10:59.928 | 18,040 | 252 |
| 00:19:29 | 00:19:29.416 | 23,000 (18,400 after the published 4,600 µs correction) | 182 |
| 00:19:37 | 00:19:37.443 | 49,660 (not used) | −2 |

So the 22:41 comparison used the value in the log, with no correction, as the protocol declared.

**One difference, in the times.** The event table carries each time to the whole second, the log to the millisecond. The table's second is the log's time rounded to the nearest second, so the model evaluates each event between 0.46 s before and 0.64 s after the logged time; for the five hourly exchanges it is 0.07 to 0.10 s after. This was not known to me when the protocol was written. Its size at 22:41 is given in section 4. For the two final transmissions the model's times are 0.416 s and 0.443 s before the logged ones. The terminal study samples the onset of the response at 1 s spacing, so a common shift of 0.4 s is inside that sampling; the difference between the two shifts is 0.027 s. I did not compute its effect on the predicted frequencies.

## 2. The grid on which the log reports its measurements

Every one of the 816 timing offsets recorded on the R channel, the channel of all the measurements above, is a whole multiple of 20 µs. Every frequency offset is a whole number of hertz (`REPORTING_GRID.csv`). The log does not say how a measured delay is mapped to that grid (to the nearest step, or downward). Either way a reported 14,540 µs stands for a range of true values 20 µs wide.

Twenty microseconds of two-way timing is 3 km of distance between aircraft and satellite.

## 3. The scatter of a single burst

From 16:00:13 to 16:11:13 UTC the aircraft was at Kuala Lumpur before departure, logged on through the Indian Ocean satellite. **It is assumed to be stationary in those eleven minutes.** The log does not hold the aircraft's position. The assumption rests on three things: the interval lies inside the half hour before take-off that the investigation used to calibrate the timing (Ashton et al., *The Search for MH370*, Journal of Navigation, 2014: seventeen measurements, mean bias −495,679 µs, largest error 17.7 km in the two-way path, which is 59 µs); the timing in the log drifts slowly and steadily there, by 4.9 µs a minute, as the satellite moves; and the frequency offsets stay between 84 and 104 Hz until 16:30 and are between 123 and 160 Hz from 16:41:52, at the take-off. In those eleven minutes the log holds 48 R-channel bursts at 1,200 bit/s:

| Estimate | Bursts or pairs | Standard deviation, µs |
|---|---:|---:|
| The 48 values as they are (14,740 to 14,900 µs) | 48 | 32.9 |
| About a straight line in time, which removes the slow change of range as the satellite moves | 48 | 29.3 |
| From differences of consecutive bursts within 2 s, at the gate | 28 pairs | 40.5 |
| The same, over the whole log | 270 pairs | 29.1 |

**A single burst's timing scatters by about 30 µs (one standard deviation), on these estimates 29 to 40 µs.** The investigation's largest calibration error of 59 µs among seventeen measurements is in keeping with that. The grid of section 2 is part of that scatter. Each hourly exchange during the flight is one burst.

In these units the criterion of the catalogue and of the 22:41 check, ±43 µs, is between about 1.1 and 1.5 standard deviations of one burst (1.5 with the 29.3 µs estimate, which the tables below use). This is the scale of the measurement, read from the log itself. It is not a new criterion and it changes no label.

*Limits of these estimates.* Eleven minutes, two channel units, one evening. Some consecutive signalling units belong to one burst and share a value, which lowers a pair estimate; the estimate from the 600 bit/s channel (26.9 µs from 58 pairs) is mostly of that kind and is not a between-burst scatter, so it is not used. The scatter in flight, at a different signal level, is not measured by this sample.

## 4. The project's results in the units of the log

Residuals are recorded minus predicted timing, over the 266 accepted cruise flights (`RESULTS_AGAINST_LOG.csv`):

| Time, UTC | Role | Residuals, µs | In standard deviations of one burst | Within ±43 µs |
|---|---|---:|---:|---:|
| 20:41:05 | fitted | −42.0 to +20.7 | −1.4 to +0.7 | 266 |
| 21:41:27 | fitted | −16.5 to +34.6 | −0.6 to +1.2 | 266 |
| 22:41:22 | not fitted | −47.2 to +13.3 | −1.6 to +0.5 | 215 |
| 00:11:00 | fitted | −28.4 to +41.4 | −1.0 to +1.4 | 266 |

At the three fitted times the residuals reach the edge of the band on one side or the other (−42.0 at 20:41, +41.4 at 00:11), because the search accepted any flight inside it. At 22:41 the residuals of the same flights run 4.2 µs past the lower edge. The spread of the 266 residuals at 22:41 (60 µs) is about the same as at the fitted times (51 to 70 µs). In the log's own units the flight farthest outside the band at 22:41 is at −1.6 standard deviations of one burst, and the flights at the edge of the band at the fitted times are at 1.4.

**How the 215 and 51 respond to the recorded value** (`LABEL_SENSITIVITY_2241.csv`). Holding every prediction fixed and asking what the count would be had the log reported a slightly different timing:

| Recorded timing changed by | Flights within ±43 µs | Outside |
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

Within half a grid step either way, the count of flights inside the band runs from 172 to 266. All 51 flights outside the band are outside it by less than half a grid step, and by at most about a seventh of the scatter of one burst.

**The time stamp.** The model evaluates the exchange at 22:41:22.000; the log stamps the burst at 22:41:21.906, 0.094 s earlier. Around that time the recorded timing offset was rising by 0.49 to 0.65 µs each second (from the recorded values at 21:41, 22:41 and 00:11), so 0.094 s corresponds to about 0.05 to 0.06 µs. The flight nearest the band is outside it by 0.033 µs. That is one flight; the other 50 are outside by more than the time-stamp effect. I did not recompute any prediction at the logged time, and what instant of the burst the log's stamp marks is not stated in the log.

## 5. What follows, and what does not

- The inputs are right: the measurements the project compared with are the ones in the log.
- **The split of 215 and 51 at 22:41 is not resolved by the measurement.** The 51 lie inside the reporting step of the log and far inside the scatter of one burst. The statement already published stands and is now supported by the log itself: the 51 do not meet the declared criterion, they are not negated, and they remain possible.
- The same holds in the other direction. The 215 are not confirmed by lying inside a band 1.1 to 1.5 standard deviations wide, and the flights at ±42 µs at the fitted times were accepted with the same margin by which the 51 are not.
- The frozen labels are not changed by this note. They are the result of the criterion as declared.
- Nothing here bears on a position.

## 6. Considered and not supported, or not done

| Idea | Status | Reason |
|---|---|---|
| Use the 600 bit/s pair estimate as that channel's burst scatter | Not supported | The pairs are mostly two units of one burst with the same value |
| State how often a flight on the true path would fall outside ±43 µs | Not stated as a result | It needs the distribution of the timing error in flight, which this sample at the gate does not give. For a normal distribution with a 29 to 40 µs standard deviation it would be between about one time in seven and one time in three and a half; that is an illustration of scale and not a property of these flights |
| Re-label the 22:41 outcomes with a band widened by the grid or the scatter | Not done | The criterion was fixed before the predictions; widening it afterwards would be a criterion chosen with the result in view |
| Recompute the predictions at the logged times | Not done | It needs the flight model and a new declared run |
| Check the timing calibration against the 48 bursts at the gate | Not done | It needs the satellite model and the aircraft's gate position; a separate task |
| Effect of the 0.4 s time difference at the final transmissions on the terminal results | Not computed | Stated in section 1 as bounded by the 1 s sampling of onset times; that is an argument, not a calculation |

## Files

`crosscheck.py`; `SUMMARY.json`; `EVENT_CROSSCHECK.csv` (19 events); `REPORTING_GRID.csv`; `BURST_SCATTER.csv`; `RESULTS_AGAINST_LOG.csv`; `LABEL_SENSITIVITY_2241.csv`. The tables hold recorded values from a published log and results already in this repository.
