# TASK042_Mach080_084_20261121_001: results

Generated from the closed record at 2026-11-21T21:16:54.795368+00:00.

**10 of 10 origin–Mach pairs were attempted; 10 retained a physically eligible sampled best; 10 passed both mesh comparisons. 0 pairs were not assessed.** The recorded final status is `BOUNDED_EXPERIMENT_COMPLETE`.

“Verified” here means the selected model-supported flight passed the declared numerical checks. It does not certify an optimum, a statistical fit, a real flight history, or a location. No additional satellite-compatibility threshold has been imposed.

## Experiment definition

- Revision: `11f3ec951da4ac4d05bccbc5a8cf620063aff97b815ab5703cf2254687efad25`.
- Source repository snapshot: `64e090a167dd402043ddff6b8fa6fc16ac919ade`.
- Two exact historical origins, five starting Mach targets from 0.800 through 0.840; the commanded Mach decreases by 0.01 over 23:30–23:32 UTC.
- Starting latitude, initial bearing and constant pressure are optimized. Constant pressure is not constant geometric height.
- The modified objective contains three BTO terms (20:41, 21:41, 00:11), all five BFO terms, and the original MID prior. The 19:41 BTO supplies starting-longitude closure.
- No new 22:41 BTO prediction was made. Its BFO remains fitted. Historical anchor selection and setup have prior exposure; this is not a blind holdout.
- The inherited fuel-loss window is 00:16:29–00:17:59 UTC. No LRC pilot, climb experiment or terminal calculation is included.

## All requested origin–Mach pairs

| Origin | Starting Mach | Pressure hPa | Modified J | Max \|BTO z\| | Max \|BFO z\| | Outcome |
| --- | --- | --- | --- | --- | --- | --- |
| north | 0.800 | 264.500 | 15.179740 | 2.6064 | 0.8743 | VERIFIED |
| north | 0.810 | 257.277 | 6.463590 | 1.3171 | 0.8647 | VERIFIED |
| north | 0.820 | 248.738 | 4.884322 | 0.9395 | 0.9535 | VERIFIED |
| north | 0.830 | 239.920 | 4.272901 | 0.7446 | 1.3141 | VERIFIED |
| north | 0.840 | 227.559 | 3.821366 | 0.5714 | 1.4185 | VERIFIED |
| south | 0.800 | 264.501 | 15.169851 | 2.6068 | 0.8732 | VERIFIED |
| south | 0.810 | 257.279 | 6.463199 | 1.3177 | 0.8638 | VERIFIED |
| south | 0.820 | 248.751 | 4.884449 | 0.9526 | 0.9623 | VERIFIED |
| south | 0.830 | 237.720 | 5.740477 | 1.2977 | 1.4348 | VERIFIED |
| south | 0.840 | 227.556 | 3.821919 | 0.5680 | 1.4177 | VERIFIED |

The residual maxima are descriptive statistics, not newly introduced pass/fail tests. The BFO maxima use the selected fitted offset and include the 22:41 BFO.

## Retained starting parameters

| Origin | Starting Mach | Latitude ° | Longitude ° | Bearing ° | Pressure hPa |
| --- | --- | --- | --- | --- | --- |
| north | 0.800 | 5.352851741 | 93.576776429 | 175.182641292 | 264.499789 |
| north | 0.810 | 5.465135848 | 93.566929169 | 175.562977742 | 257.276565 |
| north | 0.820 | 4.260481458 | 93.682358269 | 177.967361813 | 248.737720 |
| north | 0.830 | 2.734285806 | 93.762219809 | 180.854663799 | 239.920082 |
| north | 0.840 | 1.525770651 | 93.776295948 | 183.119251267 | 227.558634 |
| south | 0.800 | 5.347247730 | 93.577385397 | 175.192681964 | 264.501335 |
| south | 0.810 | 5.459465609 | 93.567565344 | 175.573048156 | 257.278808 |
| south | 0.820 | 4.226455361 | 93.684858467 | 178.024197425 | 248.750704 |
| south | 0.830 | 1.561853432 | 93.772797717 | 182.716160329 | 237.720079 |
| south | 0.840 | 1.534580506 | 93.776392145 | 183.104692848 | 227.555944 |

Longitude is solved from the 19:41 timing locus. Blank entries have no retained eligible flight; the search status and reason are preserved in RESULTS.csv.

## Supported 00:11 states of production selections

| Origin | Starting Mach | Latitude ° | Longitude ° | Geometric height m | Total fuel kg | Fuel above APU kg | Engine loss UTC |
| --- | --- | --- | --- | --- | --- | --- | --- |
| north | 0.800 | -30.4101805 | 96.8320610 | 10421.15 | 605.414 | 598.611 | 00:17:21.054 |
| north | 0.810 | -30.6159209 | 96.5934957 | 10604.36 | 526.262 | 519.458 | 00:16:29.029 |
| north | 0.820 | -32.1058378 | 95.0981304 | 10797.10 | 520.195 | 513.391 | 00:16:29.000 |
| north | 0.830 | -33.7976807 | 93.1532629 | 11012.24 | 519.259 | 512.455 | 00:16:29.000 |
| north | 0.840 | -35.0524841 | 91.5150835 | 11348.28 | 652.968 | 646.164 | 00:17:58.999 |
| south | 0.800 | -30.4160973 | 96.8260715 | 10420.96 | 605.418 | 598.614 | 00:17:21.058 |
| south | 0.810 | -30.6218728 | 96.5874385 | 10604.14 | 526.202 | 519.398 | 00:16:29.000 |
| south | 0.820 | -32.1391218 | 95.0614853 | 10796.10 | 520.334 | 513.530 | 00:16:29.000 |
| south | 0.830 | -34.7969513 | 91.8206777 | 11066.72 | 644.547 | 637.743 | 00:17:54.740 |
| south | 0.840 | -35.0448287 | 91.5259097 | 11348.39 | 652.976 | 646.172 | 00:17:58.999 |

These are the selected 15-second production records at 00:11. They are reported only when the resource history supports powered flight at that epoch. They are not terminal or impact positions. The full finer-mesh records are included in the detailed JSON.

## Qualification and baseline evidence

| Anchor | Qualification | Saved score exact | Δ kept χ² | Position shift m | Fuel shift kg | Loss shift s |
| --- | --- | --- | --- | --- | --- | --- |
| north | PASS | True | -1.20703447e-12 | 0 | 1.12777343e-10 | 7.27595761e-11 |
| south | PASS | True | -7.44826423e-12 | 0 | 4.43378667e-12 | 2.54658516e-11 |

The saved original scores were reproduced from stored residuals before the new score was applied. Real anchor qualification compared retained score terms, physical states, resource outcomes and the saved mesh; it did not calculate a new 22:41 BTO.

| Origin | Exact anchor starting Mach | Pressure hPa | 15 s modified J | Engine loss UTC | Eligible |
| --- | --- | --- | --- | --- | --- |
| north | 0.81348351851586675 | 254.532207 | 8.494318599 | 00:16:32.091 | yes |
| south | 0.84342729182503895 | 224.783193 | 5.385695402 | 00:17:47.044 | yes |

The southern anchor remains at its exact Mach above 0.840. The new target at 0.840 is a separate flight.

## Mesh verification

| Selection | Comparison | Result | Δ kept χ² | Position m | Fuel kg | Loss s |
| --- | --- | --- | --- | --- | --- | --- |
| north_down_M0.810 | 15 → 7.5 s | PASS | -0.0000112 | 0.08251 | 0.000525 | 0.000080 |
| north_down_M0.810 | 7.5 → 3.75 s | PASS | 0.0000041 | 0.03027 | -0.000011 | -0.000075 |
| north_down_M0.800 | 15 → 7.5 s | PASS | -0.0000063 | 0.01989 | 0.000514 | 0.000196 |
| north_down_M0.800 | 7.5 → 3.75 s | PASS | -0.0000026 | 0.00724 | -0.000009 | -0.000019 |
| north_up_M0.820 | 15 → 7.5 s | PASS | -0.0000026 | 0.10111 | 0.000380 | 0.000074 |
| north_up_M0.820 | 7.5 → 3.75 s | PASS | 0.0000006 | 0.01997 | -0.000016 | -0.000079 |
| north_up_M0.830 | 15 → 7.5 s | PASS | -0.0000020 | 0.08585 | 0.000237 | 0.000156 |
| north_up_M0.830 | 7.5 → 3.75 s | PASS | 0.0000001 | 0.00356 | -0.000016 | -0.000015 |
| north_up_M0.840 | 15 → 7.5 s | PASS | 0.0000005 | 0.00241 | 0.000266 | 0.000210 |
| north_up_M0.840 | 7.5 → 3.75 s | PASS | -0.0000001 | 0.00739 | -0.000021 | -0.000014 |
| south_down_M0.840 | 15 → 7.5 s | PASS | -0.0000009 | 0.00881 | 0.000272 | 0.000214 |
| south_down_M0.840 | 7.5 → 3.75 s | PASS | -0.0000001 | 0.00376 | -0.000020 | -0.000013 |
| south_down_M0.830 | 15 → 7.5 s | PASS | -0.0000028 | 0.00916 | 0.000231 | 0.000116 |
| south_down_M0.830 | 7.5 → 3.75 s | PASS | 0.0000007 | 0.00133 | -0.000016 | -0.000034 |
| south_down_M0.820 | 15 → 7.5 s | PASS | -0.0000021 | 0.07009 | 0.000372 | 0.000100 |
| south_down_M0.820 | 7.5 → 3.75 s | PASS | 0.0000002 | 0.00620 | -0.000011 | -0.000063 |
| south_down_M0.810 | 15 → 7.5 s | PASS | 0.0000070 | 0.04456 | 0.000502 | 0.000044 |
| south_down_M0.810 | 7.5 → 3.75 s | PASS | -0.0000022 | 0.02029 | -0.000014 | -0.000057 |
| south_down_M0.800 | 15 → 7.5 s | PASS | 0.0000206 | 0.07048 | 0.000524 | 0.000388 |
| south_down_M0.800 | 7.5 → 3.75 s | PASS | -0.0000053 | 0.02156 | -0.000010 | -0.000077 |

The production fitted offset is fixed on both repeats. Both comparisons must retain physical eligibility and satisfy |Δ observation χ²| < 0.01, position shift < 10 m, |Δ fuel| < 1 kg, and |Δ engine-loss time| < 5 s. A retained point with failed or unfinished verification remains a production sample.

### Hard physical eligibility at each mesh

| Selection | Mesh s | Eligible | Loss seconds after 19:41:03 | Early margin s | Late margin s | Recorded reasons |
| --- | --- | --- | --- | --- | --- | --- |
| north_down_M0.800 | 15 | yes | 16578.054554134585 | 52.0545541346 | 37.9454458654 | none |
| north_down_M0.800 | 7.5 | yes | 16578.054750420848 | 52.0547504208 | 37.9452495792 | none |
| north_down_M0.800 | 3.75 | yes | 16578.054731756543 | 52.0547317565 | 37.9452682435 | none |
| north_down_M0.810 | 15 | yes | 16526.029707875525 | 0.0297078755248 | 89.9702921245 | none |
| north_down_M0.810 | 7.5 | yes | 16526.029787913663 | 0.0297879136633 | 89.9702120863 | none |
| north_down_M0.810 | 3.75 | yes | 16526.029712879292 | 0.0297128792918 | 89.9702871207 | none |
| north_up_M0.820 | 15 | yes | 16526.00046159904 | 0.000461599040136 | 89.999538401 | none |
| north_up_M0.820 | 7.5 | yes | 16526.000535875497 | 0.000535875497008 | 89.9994641245 | none |
| north_up_M0.820 | 3.75 | yes | 16526.000456832528 | 0.000456832527561 | 89.9995431675 | none |
| north_up_M0.830 | 15 | yes | 16526.000011184435 | 1.11844346975e-05 | 89.9999888156 | none |
| north_up_M0.830 | 7.5 | yes | 16526.000166908565 | 0.000166908565006 | 89.9998330914 | none |
| north_up_M0.830 | 3.75 | yes | 16526.000151669912 | 0.000151669912157 | 89.9998483301 | none |
| north_up_M0.840 | 15 | yes | 16615.999675225845 | 89.9996752258 | 0.00032477415516 | none |
| north_up_M0.840 | 7.5 | yes | 16615.999885184552 | 89.9998851846 | 0.000114815447887 | none |
| north_up_M0.840 | 3.75 | yes | 16615.99987155505 | 89.9998715551 | 0.000128444949951 | none |
| south_down_M0.800 | 15 | yes | 16578.058026659714 | 52.0580266597 | 37.9419733403 | none |
| south_down_M0.800 | 7.5 | yes | 16578.058414226733 | 52.0584142267 | 37.9415857733 | none |
| south_down_M0.800 | 3.75 | yes | 16578.058337065675 | 52.0583370657 | 37.9416629343 | none |
| south_down_M0.810 | 15 | yes | 16526.000782144543 | 0.000782144543336 | 89.9992178555 | none |
| south_down_M0.810 | 7.5 | yes | 16526.000825904986 | 0.000825904986414 | 89.999174095 | none |
| south_down_M0.810 | 3.75 | yes | 16526.00076935075 | 0.000769350750488 | 89.9992306492 | none |
| south_down_M0.820 | 15 | yes | 16526.000041779615 | 4.17796145484e-05 | 89.9999582204 | none |
| south_down_M0.820 | 7.5 | yes | 16526.000141716162 | 0.000141716162034 | 89.9998582838 | none |
| south_down_M0.820 | 3.75 | yes | 16526.00007894696 | 7.89469595475e-05 | 89.999921053 | none |
| south_down_M0.830 | 15 | yes | 16611.740869665427 | 85.7408696654 | 4.25913033457 | none |
| south_down_M0.830 | 7.5 | yes | 16611.740985301203 | 85.7409853012 | 4.2590146988 | none |
| south_down_M0.830 | 3.75 | yes | 16611.740951041582 | 85.7409510416 | 4.25904895842 | none |
| south_down_M0.840 | 15 | yes | 16615.999640757887 | 89.9996407579 | 0.000359242112609 | none |
| south_down_M0.840 | 7.5 | yes | 16615.999854952104 | 89.9998549521 | 0.000145047895785 | none |
| south_down_M0.840 | 3.75 | yes | 16615.999841938949 | 89.9998419389 | 0.000158061051479 | none |

The early margin is loss time minus 16,526 s; the late margin is 16,616 s minus loss time. Both must be nonnegative. The table retains enough digits to expose sub-millisecond boundary crossings. A small mesh difference does not excuse a negative margin. Coarse eligibility is never inherited by a finer mesh.

| Selection | Comparison | Failed numerical thresholds | Both physically eligible | Failure classification |
| --- | --- | --- | --- | --- |
| north_down_M0.800 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| north_down_M0.800 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |
| north_down_M0.810 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| north_down_M0.810 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |
| north_up_M0.820 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| north_up_M0.820 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |
| north_up_M0.830 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| north_up_M0.830 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |
| north_up_M0.840 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| north_up_M0.840 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.800 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.800 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.810 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.810 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.820 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.820 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.830 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.830 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.840 | 15 → 7.5 s | none | yes | PASSED_RECORDED_CHECK |
| south_down_M0.840 | 7.5 → 3.75 s | none | yes | PASSED_RECORDED_CHECK |

`HARD_FUEL_WINDOW_BOUNDARY_ONLY` means all four numerical-difference checks passed, but a saved flight crossed the hard fuel-loss-window boundary. It remains a verification failure. The report neither relaxes the window nor selects a replacement flight.

## Search stops and accounting

| Unique search-trial outcome | Count |
| --- | --- |
| EARLY_FUEL_EXHAUSTION | 198 |
| MODEL_SUPPORT_LIMIT | 3 |
| PHYSICALLY_ELIGIBLE | 238 |
| POWERED_AT_WINDOW_END_RIGHT_CENSORED | 75 |
| WEATHER_OR_GUIDANCE_STOP | 9 |

Counts above deduplicate saved trial records referenced by the continuation nodes. Qualification, baselines and mesh repeats are separate from these search counts. Early exhaustion, a model-support stop and remaining powered at the window end are different outcomes. None by itself is a measured satellite mismatch.

| Origin | Mach | Optimizer success | New flights | Termination or non-assessment reason |
| --- | --- | --- | --- | --- |
| north | 0.800 | no | 54 | PER_TARGET_OR_RESTORATION_CAP |
| north | 0.810 | yes | 42 | Optimization terminated successfully |
| north | 0.820 | no | 54 | PER_TARGET_OR_RESTORATION_CAP |
| north | 0.830 | no | 54 | PER_TARGET_OR_RESTORATION_CAP |
| north | 0.840 | no | 54 | PER_TARGET_OR_RESTORATION_CAP |
| south | 0.800 | no | 54 | PER_TARGET_OR_RESTORATION_CAP |
| south | 0.810 | yes | 51 | Optimization terminated successfully |
| south | 0.820 | yes | 52 | Optimization terminated successfully |
| south | 0.830 | no | 54 | PER_TARGET_OR_RESTORATION_CAP |
| south | 0.840 | no | 54 | PER_TARGET_OR_RESTORATION_CAP |

Total flights started/completed: **547/547**; software failures: **0**. Charged execution: **4406.128 s** of **7200 s**, with a **600-flight** cap. Recorded 22:41 BTO requests: **0**.

## Relation between origins

| Starting Mach | Saved comparison | 00:11 separation m | Both verified |
| --- | --- | --- | --- |
| 0.800 | DISTINCT_RETAINED_SAMPLES | 873.355 | yes |
| 0.810 | DISTINCT_RETAINED_SAMPLES | 879.761 | yes |
| 0.820 | DISTINCT_RETAINED_SAMPLES | 5060.305 | yes |
| 0.830 | DISTINCT_RETAINED_SAMPLES | 165317.991 | yes |
| 0.840 | DISTINCT_RETAINED_SAMPLES | 1302.255 | yes |

Identical selected parameters indicate that the two searches recovered the same retained recipe. Different retained samples establish only that the sampled recipes differ. Five Mach cuts and finite local searches cannot certify global connection, disconnection, or a global minimum. A stopped direction means no continuation was established within its method and budget.

## Files

- `RESULTS.csv`: all ten requested origin–Mach pairs with parameters, scores, resource outcomes, solver status and verification status.
- `retained_comparisons.json`: selected and finer-mesh saved records, qualification, same-Mach comparisons, accounting and source-file hashes.
- The original `record/` directory contains the immutable experiment journal, design, trial files and verification comparisons.

This report performs saved-record analysis only. No aircraft model, observation predictor or integrator is imported or run.
