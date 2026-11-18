# Fuel exhaustion, electrical power, APU and the satellite unit: what the source says and what the model holds

16 November 2026, revised the same day after Codex's review of `2fc9d0e`. Prepared alongside `METHOD.md`. It uses no terminal calculation. The numbers in the tables are arithmetic on the saved fuel-event times (`bookkeeping.py`, `ELECTRICAL_BOOKKEEPING_BY_GROUP.csv`).

**Summary.** The model has one fuel event and no electrical system. The published sequence that leads to the 00:19:29 log-on takes about two minutes from the loss of both engines' generators. In the 90 flights whose fuel event precedes the log-on, the model's interval is 136 to 509 s, grouped by cruise level and speed. Nothing here establishes an electrical explanation for any flight. The 6.80 kg reserve is a modelling choice and is not evidence that an APU started.

## What the source says

Australian Transport Safety Bureau, *MH370 – Definition of Underwater Search Areas*, 3 December 2015, pages 8 to 10. The quotations were extracted on 7 November 2026 and are held in `../TWO_TURN_TERMINAL_ELECTRICAL_TIMELINE/TIMING_CONTRACT.json`; the item numbers below are those of `TIMING_CONTRACT.md` in that directory.

| Item | Statement | Duration given |
|---|---|---|
| S1 | An engine that flames out spools down and its generator drops off-line | None |
| S2 | The satellite unit is powered from the left AC bus | |
| S3, S4 | If one generator is lost, the other powers both buses automatically; the satellite unit is designed to stay on through that switch | "Brief" |
| S5 | An interruption long enough to cause a log-on needs the loss of both AC buses, or disabled automatic switching | |
| S6 | Loss of both AC buses starts the APU automatically; its generator comes on-line | About 60 s |
| S7 | From power being applied, the satellite unit sends its log-on request | About 60 s |
| S8 | The APU draws from the left main tank: about 30 lb available after the left engine runs out; 2 lb per 55 s under electrical load; enough for "around 2 minutes" assuming small pitch changes and positive acceleration | Up to 13 min 45 s |
| S9 | After loss of both AC buses the ram-air turbine deploys and batteries are available. The source does not say either powers the satellite unit | |
| S10 | The right engine likely flamed out first; the left could have run up to 15 minutes longer | Estimate |

The source's own table puts the APU start at about 00:17:30 and power restoration at about 00:18:30, both counted back from the observed 00:19:29. It gives no flame-out time. Its durations are approximate and carry no stated tolerance.

Holland (2017) treats the same sequence for the frequency analysis: under a loss and restoration of power the outage before the log-on "would have lasted about one minute", and the oscillator warm-up offset applies; under a momentary interruption it does not.

## What the model holds

| Item | In the model | Origin |
|---|---|---|
| Fuel event | One instant at which total fuel equals the reserve; both engines lose thrust together | Aggregate fuel bookkeeping of the cruise model |
| Reserve | 15 lb (6.80388555 kg) set aside from usable fuel | Project choice. The source's figure is about 30 lb (S8) |
| APU fuel use | 2 lb per 55 s from the fuel event until the reserve is gone, 412.5 s later; feed uninterrupted | Rate from S8; start time and uninterrupted feed are project assumptions |
| APU start, satellite-unit start | Times 60 s and 120 s after the event exist only as step boundaries of the integration | S6, S7 |
| Generators, buses, switching, ram-air turbine, batteries | Not represented | |
| Sequential flame-outs, flight on one engine | Not represented | |

## Mapping the fuel event onto the sequence

If the aggregate fuel event is read as the loss of the second engine, the source's sequence follows from it directly:

| Step | Source | Model counterpart | Standing |
|---|---|---|---|
| Both AC buses lose power | S5, S6 | The fuel event | Assumed equal; the source describes two flame-outs at different times |
| APU starts and its generator comes on-line | S6, about 60 s | None | Not evaluated |
| Satellite unit powers up and requests log-on | S7, about 60 s | None | Not evaluated |
| Log-on request received 00:19:29 | Observed | Prediction compared | Reported per response |
| APU still fuelled through 00:19:37 | S8 | Reserve and burn rate | Arithmetic below |

## Arithmetic by group

The 90 flights whose fuel event precedes 00:19:29:

| Incoming level and speed | Cruise level | Flights | Fuel event to 00:19:29 | Longer than the source's 120 s by | Model APU fuel left at 00:19:29 (15 lb reserve) | Same arithmetic with 30 lb |
|---|---|---|---|---|---|---|
| 300.9 hPa, Mach 0.78 | 33,985 ft | 13 | 136.4 to 157.6 s | 16 to 38 s | 4.20 to 4.56 kg | 11.0 to 11.4 kg |
| 331.655 hPa, Mach 0.75 | 31,946 ft | 21 | 175.8 to 198.2 s | 56 to 78 s | 3.53 to 3.91 kg | 10.3 to 10.7 kg |
| 365.113 hPa, Mach 0.67 | 25,661 ft | 30 | 377.3 to 399.8 s | 257 to 280 s | 0.21 to 0.58 kg | 7.0 to 7.4 kg |
| 365.113 hPa, Mach 0.75 | 31,946 ft | 26 | 488.6 to 508.9 s | 369 to 389 s | None: gone 76 to 96 s before 00:19:29 | 5.2 to 5.5 kg |

Computed outcomes:

- In all 90 flights the interval is longer than the source's approximate 120 s. The source states no tolerance for its two durations, so this is a reported difference. It excludes no flight.
- Under the model's own reserve and burn rate, 64 flights have APU fuel left at both final transmissions and 26 do not.
- With 30 lb in place of 15 lb in the same arithmetic, all 90 have APU fuel left at both.
- The intervals fall into four separate ranges, one per group. This is an observed association with cruise level and speed in this catalogue. It is not a selection criterion and no flight is removed on it.

**What the 30 lb column is.** It is arithmetic on the saved event times: the time from each event to the transmission, multiplied by the burn rate, subtracted from 30 lb. It is not a flight computed with a different reserve. A cruise flight that set 30 lb aside would reach its fuel event earlier, by the time the engines take to burn the other 15 lb, and no such flight has been computed.

The other flights:

| Status | Flights | Fuel event relative to 00:19:29 |
|---|---|---|
| Fuel event after both final transmissions | 139 | 73 to 1,143 s after |
| of which, within two minutes after | 42 | 73 to 94 s after (8 flights: 300.9 hPa, Mach 0.75 at 31,946 ft); 92 to 117 s after (34 flights: 365.113 hPa, Mach 0.75 at 33,985 ft) |
| Engines running at 00:40:00 | 37 | No fuel event |

## Interpretation, kept apart from the numbers

**A longer interval than about two minutes.** The source's sequence does not contain the extra time. Two readings are possible and neither is evaluated here.

- *A delay the source does not describe* between loss of thrust and the log-on.
- *Two flame-outs at different times*, as the source describes (S10). This is a scenario and not a result. The aggregate model burns all remaining fuel with both engines. If instead one tank emptied first, the fuel left would be burned by one engine and could last longer, so the loss of both AC buses could come later than the aggregate event and nearer to the log-on. Whether the aggregate event falls between two real flame-outs, and by how much, cannot be said without a model of tank feed and of flight on one engine. This work has neither. The zero-thrust propagation of this method starts at the aggregate event and does not establish the scenario. If it held, the aircraft would be under power on one engine for part of the interval, which the terminal paths computed here do not represent; that mismatch would be largest for the groups with intervals of six to eight minutes.

**The 42 flights with the fuel event shortly after the log-on.** In the same scenario the first flame-out would precede the aggregate event. The source says a single flame-out does not interrupt the satellite unit unless automatic switching was disabled (S3 to S5). This is not examined; the flights keep their status.

**Warm-up.** Which frequency treatment applies depends on how long the satellite unit was unpowered. The model does not determine it, so all four treatments are reported side by side.

## Standing of each element

| Element | Standing |
|---|---|
| Time of the aggregate fuel event in each flight | Computed by the cruise model at fuel-flow multiplier 1.000, conditional on that model and on each flight's commands |
| That the event is the loss of both AC buses | Assumed |
| That the APU started, came on-line, and fed the satellite unit | Not evaluated. Not established by anything in this work |
| APU fuel sufficiency | Arithmetic only: conditional on the reserve chosen (15 lb or 30 lb), on the burn rate, and on uninterrupted feed, which the source makes conditional on small pitch changes and positive acceleration; the declared responses include a 60° bank and a halving of lift |
| About 60 s + about 60 s | Source values, approximate, no tolerance |
| Sequential flame-outs, one-engine flight, bus switching, ram-air turbine, batteries | Not represented |
| The 6.80 kg reserve | Imposed by the model. Not evidence of an APU start |

## Sources

- Australian Transport Safety Bureau (2015). *MH370 – Definition of Underwater Search Areas.* AE-2014-054, 3 December 2015. https://www.atsb.gov.au/sites/default/files/2022-12/AE-2014-054_MH370-Definition%20of%20Underwater%20Search%20Areas_3Dec2015.pdf
- Holland, I. D. (2017). *MH370 Burst Frequency Offset Analysis and Implications on Descent Rate at End-of-Flight.* https://arxiv.org/abs/1702.02432
