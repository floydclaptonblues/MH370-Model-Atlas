# Combined survivors and searched seabed: method

Written 24 November 2026, before the areas and coverage fractions were computed.
Records only: no flight, fuel integration or satellite prediction is run here.

## Purpose

To put the project's separate results into one statement: which of the flights already on
file satisfy every constraint the project has tested, where those flights end, how much of
that ending area has documented sonar coverage, and what remains.

## Disclosure

The latitude ranges of the stored end states were seen while taking stock of the files,
before these rules were written. No coverage fraction or area had been computed. The rules
below use only quantities and thresholds that earlier project runs had already fixed, plus
three end-of-flight scenarios stated here.

## Flights used

**Tier 1, tested through the final transmissions.** Every end-of-flight response in the
flight-state catalogue (`FLIGHT_STATE_CATALOGUE/flight_state_catalogue.sqlite`) marked
compatible with the 00:19:29 and 00:19:37 measurements under at least one of the
catalogue's measurement treatments, taken at its 00:19:37 state. Five sets: the
full-population campaign (FPC), the lower-speed northern run (LSN), the 11 November speed
sample (SCE), the climbed branches (NBT) and the 24 earlier candidates (TACO, fuel-flow
multipliers 1.000 and 1.005 kept apart). Each of these flights had already passed, in its
own run: accepted arrival at 19:41:03; timing residuals within 43 microseconds at
20:41:05, 21:41:27 and 00:11:00; support by the aircraft performance model throughout;
and a fuel-exhaustion event from which the end-of-flight response was computed.

**Tier 2, tested to 00:11 and fuel exhaustion only.** Accepted flights of the cruise-level
run (`CRUISE_LEVEL_PRODUCTION_108`, distinct flights) and of the long-range-cruise pilot
(`LRC_CRUISE_CLIMB_PILOT`, pilot e80252c47000). They passed the same 19:41 to 00:11 tests.
No end-of-flight response was computed for them, so their agreement with the final
transmissions is **not tested**.

The 22:41 measurements remain withheld: they are not used here.

## Rules (fixed now)

1. **Timing and performance.** As accepted by the source run. Nothing is re-fitted.
2. **Fuel.**
   - Tier 1: as required by the source run's end-of-flight mapping.
   - Tier 2 primary: fuel exhaustion between 00:11:00 and 00:19:37 UTC, the window used by
     the project's end-of-flight mapping.
   - Tier 2 sensitivity: the same window widened by 5 minutes at each end. Five minutes is
     about 1 % of the flight's endurance, a rough allowance for fuel-flow uncertainty.
3. **Frequency, 20:41 to 00:11 (reported, and applied as a second count).** Where the
   source run reports centred frequency residuals, a flight is also counted under the
   stricter rule that all three are within 7 Hz. The long-range-cruise table carries no
   such columns; those flights are marked "not available".
4. **Reference end point.**
   - Tier 1: the stored 00:19:37 position.
   - Tier 2: the point on the project's arc-7 ring nearest the fuel-exhaustion position
     (ring: half-angle 44.4701 degrees about 0.5345 N, 64.4641 E). The distance moved is
     recorded.
5. **End-of-flight scenarios.** Each is a disc about the reference point; direction after
   00:19:37 is not assumed.
   - **S1, continued descent.** The aircraft keeps its 00:19:37 descent rate to the
     surface. Radius = 221 m/s x height / descent rate. 221 m/s is the largest ground
     speed among the stored compatible states. Where a set stores no descent rate, the
     slowest compatible descent in the catalogue (68.7 m/s) is used.
   - **S2, recovered glide.** The descent is arrested and the aircraft glides from its
     00:19:37 height at a lift-to-drag ratio of 17 in still air. Radius = 17 x height.
     The ratio is an assumption (clean 777 near best glide is usually quoted in the high
     teens); wind is ignored.
   - **S3, final descent readings doubted.** If the 00:19:29 and 00:19:37 frequency
     readings are set aside, a glide from cruise height is possible. Radius 185 km
     (100 nautical miles), a conventional upper figure. This scenario abandons the
     evidence that defines Tier 1 and is shown for scale only.
   - Tier 2 points take the largest Tier 1 radius of each scenario.
6. **Coverage layers.**
   - **A, documented.** The Geoscience Australia deep-tow valid-data footprint (GA 120969,
     Fugro deep tow, L0 coverage), repaired for invalid rings. "Covered" means sonar data
     is present; it does not mean a target would have been detected.
   - **B, extent only.** The Dong Hai Jiu 101 outline and the Go Phoenix mosaic rectangle.
     Presence of data inside them is unresolved, so they are reported separately and not
     added to A.
   - **C, reported but not verified.** Ocean Infinity's 2018 search is generally described
     as covering the arc from about 36 S to 25 S to about 22 nautical miles either side.
     No geometry is held. The description is from an independent analyst's published
     account (source in REPORT.md), not from a primary record; the 36 S southern limit is
     assumed here.
     It is modelled as that band and labelled as an unverified scenario, never as a
     coverage record.
   - **Not modelled.** Ocean Infinity 2025-26 (about 15,000 km2 between roughly 33 S and
     36 S, reported up to about 45-50 nautical miles from the arc): no geometry held.
     Data gaps, low-quality lines and terrain shadows inside any layer: not located.
7. **Areas.** Lambert azimuthal equal-area projection centred at 33 S, 94 E. Areas are of
   the union of discs, per tier and scenario, split by coverage layer and by one-degree
   bands of latitude.

## What the result is and is not

It is the set of endings of the flights flown so far that pass the stated tests. It covers
only the flight types those runs flew. It is not a probability map; an area being large or
small says nothing about likelihood. A flight type not yet flown could end elsewhere.

## Addendum, 24 November 2026: glide direction (fixed before computing)

The recovered-glide scenario S2 above assumes no direction. This addendum narrows it by
direction for Tier 1 only.

- **Track at 00:19:37.** Where the catalogue stores a ground track at 00:19:37 (the
  full-population campaign and the lower-speed northern run) it is used. For the other
  three sets it is taken as the geodesic bearing from the stored 00:19:29 position to the
  stored 00:19:37 position of the same response.
- **S2a, along track:** the glide ends within 45 degrees either side of that track.
- **S2b, forward half:** within 90 degrees either side.
- Radius as S2 (17 x height at 00:19:37). Sectors are built geodesically.
- Areas are split as before, and also by side of the arc: beyond the arc (farther from
  the satellite) or inside it.

Caution fixed in advance: the compatible end-of-flight responses are banked, so the
00:19:37 track is a moment in a turn, not a settled heading. A recovery could roll out
on another heading. The sectors describe "continues roughly as it was moving", nothing
stronger.

## Addendum 2, 24 November 2026: second group after its final-transmission test

Codex ran the campaign's unchanged end-of-flight response map for the 130 Tier 2
flights (package SHA-256 fd1bf657735ff5c6a51852dd293b008e60e4411832b715f083e3b6288b5567a7).
Rule fixed before recomputing areas: every response it marks compatible, at its stored
00:19:37 state, is treated exactly as a Tier 1 end state (same S1, S2, S2a, S2b radii and
sectors, stored descent rate and track). The result is reported for the original Tier 1,
for the newly tested group, and for both together. No rule above is changed.
