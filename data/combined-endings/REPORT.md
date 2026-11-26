# Combined survivors and searched seabed

24 November 2026. Records only: no flight, fuel integration or satellite prediction was run.
Rules were fixed in `METHOD.md` before any area or coverage fraction was computed.

## Summary

- **Where the surviving flights end.** The 91 flights on file that pass every test through
  the final transmissions end along arc 7 between **29.9° S and 34.1° S**, within 21 km of
  the arc at 00:19:37.
- **If the descent continued,** all of them reach the sea inside the 22-nautical-mile band
  that Ocean Infinity is reported to have searched in 2018. That band's geometry is not
  held and was not verified. Only 1.6 % of this area has sonar data documented in the
  files held here.
- **If the descent was arrested and the aircraft glided,** the reachable area is about
  209,000 km², of which about **142,000 km² lies outside both** the documented footprint
  and the reported band, on both sides of the arc.
- **A second group ends further south.** 130 flights that pass the tests to 00:11 and run
  out of fuel in the expected window end between 32.0° S and 37.6° S. They were never
  tested against the final transmissions. Their continued-descent area is 74 % inside
  documented sonar data.
- **So the evidence does not point at one unsearched place.** Under a continued descent,
  essentially all of the area the surviving flights reach is documented or reported as
  searched. An unsearched remainder exists only if the aircraft glided, or if the reported
  2018 coverage has gaps.

## 1  The flights

| Group | What they passed | Flights | End states | Reference latitude |
|---|---|---:|---:|---|
| Tier 1 | 19:41 arrival; timing at 20:41, 21:41, 00:11 within 43 µs; aircraft performance; fuel exhaustion; 00:19:29 and 00:19:37 measurements under at least one treatment | 91 | 1,422 | 29.88–34.06° S |
| Tier 2, cruise-level run | The same through 00:11; fuel exhausted 00:11:00–00:19:37; final transmissions not tested | 90 | 90 | 31.97–36.61° S |
| Tier 2, long-range-cruise pilot | The same | 40 | 40 | 32.24–37.61° S |

Tier 1 by source set: full-population campaign 376 states (24 flights), lower-speed
northern run 239 (15), speed sample 244 (16), climbed branches 185 (12), earlier
candidates 378 (24; 138 at fuel-flow multiplier 1.000 and 240 at 1.005).

Tier 1 states at 00:19:37 are 3.8–8.5 km above the surface, descending at 69–121 m/s.

**Tier 2 flights not carried forward:** 97 cruise-level and 5 long-range-cruise flights run
out of fuel after 00:24:37; 37 cruise-level flights were still powered at the end of their
record (00:40). A further 43 cruise-level flights exhaust fuel within 5 minutes after the
window; they are shown only as a sensitivity. Adding them raises the continued-descent area by 3.5 % and the
others by less than 1 %.

**Frequency, 20:41 to 00:11.** All 90 cruise-level flights have all three centred frequency
residuals within 7 Hz, so that rule removes none. The long-range-cruise table has no such
columns.

## 2  Areas and coverage

End-of-flight scenarios (discs about each reference point, any direction):
S1 continued descent, radius 6.9–26.7 km; S2 recovered glide at lift-to-drag 17, radius
64–144 km; S3 glide from cruise height with the final readings set aside, 185 km.

Coverage layers: **A** documented deep-tow sonar footprint (103,969 km² in total);
**C** the 2018 Ocean Infinity search as reported, modelled as 22 nautical miles either
side of the arc from 25° S to 36° S (not verified, no geometry held).

| Flights | Scenario | Area, km² | In A, km² | In A, % | In C outside A, km² | Outside A and C, km² |
|---|---|---:|---:|---:|---:|---:|
| Tier 1 | S1 continued descent | 26,370 | 425 | 1.6 | 25,945 | 0 |
| Tier 1 | S2 recovered glide | 209,265 | 887 | 0.4 | 66,349 | 142,028 |
| Tier 1 | S3 final readings doubted | 340,363 | 5,343 | 1.6 | 75,597 | 259,422 |
| Tier 2 | S1 | 21,037 | 15,483 | 73.6 | 5,529 | 25 |
| Tier 2 | S2 | 263,756 | 70,153 | 26.6 | 37,686 | 155,916 |
| Tier 2 | S3 | 388,226 | 76,297 | 19.7 | 47,647 | 264,283 |
| Tier 1 + Tier 2 | S1 | 45,036 | 15,908 | 35.3 | 29,103 | 25 |
| Tier 1 + Tier 2 | S2 | 391,183 | 70,501 | 18.0 | 72,892 | 247,790 |
| Tier 1 + Tier 2 | S3 | 554,250 | 76,460 | 13.8 | 77,162 | 400,628 |

Restricting Tier 1 to fuel-flow multiplier 1.000 changes the S1 area to 25,960 km² and
leaves S2 unchanged.

**Tier 1, recovered glide, by latitude** (km²):

| Latitude | Area | In A or C | Outside both |
|---|---:|---:|---:|
| 28–29° S | 4,530 | 658 | 3,872 |
| 29–30° S | 29,706 | 10,492 | 19,214 |
| 30–31° S | 38,112 | 11,480 | 26,632 |
| 31–32° S | 40,524 | 11,781 | 28,743 |
| 32–33° S | 40,219 | 12,125 | 28,094 |
| 33–34° S | 36,545 | 12,523 | 24,022 |
| 34–35° S | 19,629 | 8,177 | 11,451 |

The remainder is spread evenly from 29° S to 34° S, on both sides of the arc. Nothing in
these records favours one stretch of it over another.

Full tables: `areas_by_set_and_scenario.csv`, `areas_by_latitude_band.csv`. Per-flight
rows: `tier1_end_states.csv`, `tier2_flights.csv`, `tier2_flights_with_reference.csv`.
Maps: `map_tier1.png`, `map_all.png`.

## 3  What this does and does not establish

**Established, within the flights flown.** Every flight on file that agrees with the
satellite timing, the aircraft's performance and fuel, and the final transmissions ends
within 21 km of arc 7 between 29.9° S and 34.1° S, descending at 69–121 m/s.

**Depends on an unverified record.** The statement that the continued-descent area was
searched rests almost entirely (98 %) on the reported extent of the 2018 search. The
project holds no geometry for it. Obtaining that coverage, with its data gaps, is the
single most useful missing input.

**Depends on an assumption.** The unsearched remainder exists only under a recovered
glide. The lift-to-drag ratio of 17, still air and the absence of a preferred direction
are assumptions. A glide continuing roughly along track would cover about half of each
disc; that refinement needs the stored tracks, which only two of the five sets carry.

**Not established.**

- That the aircraft is in any of these areas. These are model outputs.
- That Tier 2 flights agree with the final transmissions. They were not tested.
- That other flight types end here. Only the flight types already flown are represented:
  great-circle steering after 19:41, the speeds and levels of the five runs, and the
  starting points of those runs. The deterministic grid now running tests more.
- Detection. "Covered" means sonar data exists. Data gaps, low-quality lines and terrain
  shadows inside the layers were not located.

## 4  Not included

- Ocean Infinity 2025–26 coverage (about 15,000 km² reported between roughly 33° S and
  36° S). No geometry held.
- The Go Phoenix sonar layer (only its bounding rectangle is held) and the Dong Hai Jiu
  101 outline, whose data presence is unresolved. The outline's overlap is reported in the
  table file as "extent only" and is small for Tier 1 (about 1,000 km²).
- Drift evidence. Earlier project runs found the drift timing unable to separate
  positions along this stretch of the arc, so it is not applied as a filter here.
- The 22:41 measurements, which remain withheld.

## 5  Checks

- Deep-tow footprint area: 103,969 km² in the equal-area projection and 103,969 km² by
  geodesic calculation on the source coordinates.
- Disc of 100 km radius: 31,413 km² against 31,416 km² exact (64-segment polygon).
- Arc-7 ring at 90.40° E: 36.889° S, matching the project's stated value.
- Tier 1 row count 1,422, equal to the catalogue's compatible responses at 00:19:37
  (376 + 239 + 244 + 185 + 378).
- An earlier version of the script dropped most of the deep-tow polygons after repair
  (footprint 850 km²) and mis-read the cruise-level fuel-exhaustion times. Both were
  caught by these checks and corrected before any figure here was written.

## 6  Sources

- Flight-state catalogue v1.1, `FLIGHT_STATE_CATALOGUE/flight_state_catalogue.sqlite`.
- `CRUISE_LEVEL_PRODUCTION_108/PROD_SOLUTIONS.csv`.
- `LRC_CRUISE_CLIMB_PILOT/results_pilot_e80252c47000/pilot_accepted_flights.csv`.
- Geoscience Australia GA 120969 deep-tow L0 coverage and Dong Hai Jiu 101 outline, as
  frozen in `TERMINAL_SEARCH_COVERAGE_OVERLAY/SOURCE_MANIFEST.json` (not committed).
- Reported 2018 search extent: V. Iannello, "End-of-Flight Simulations of MH370",
  19 August 2018 (https://mh370.radiantphysics.com/2018/08/19/end-of-flight-simulations-of-mh370/),
  which describes coverage of the arc to 25° S at widths of 22 nautical miles or more.
  The 36° S southern limit is an assumption of this overlay.

## 7  Addendum: recovered glide limited by direction (24 November 2026)

Rule fixed in the `METHOD.md` addendum before computing. Tier 1 only. Track at 00:19:37 is
stored for two sets and derived from the 00:19:29 and 00:19:37 positions for two more
(position step 1.3–1.7 km over 8 s). The climbed-branch set (185 responses, 31.5–33.7° S)
stores neither a track nor a 00:19:29 position and is left out; the any-direction area is
unchanged without it. 1,237 responses are used. Their tracks run from 136° to 206°
(median 166°), that is, roughly south-south-east.

| Glide direction | Area, km² | Documented or reported as searched, km² | Outside both, km² | of which beyond the arc | of which inside the arc |
|---|---:|---:|---:|---:|---:|
| Within 45° of the 00:19:37 track | 115,475 | 54,821 | **60,654** | 57,621 | 3,034 |
| Forward half (within 90°) | 167,802 | 61,801 | 106,002 | 60,578 | 45,424 |
| Any direction | 209,265 | 67,236 | 142,028 | 60,588 | 81,441 |

"Beyond the arc" is the side farther from the satellite (south-east of the arc here).

**Reading.** If the aircraft recovered and kept going roughly the way it was moving, the
remainder outside documented and reported coverage is about 60,700 km², and 95 % of it
lies beyond the arc: a strip from the edge of the reported 22-nautical-mile band out to
about 145 km from the arc, between about 30° S and 35° S. It is spread evenly along that
stretch (10,400–13,900 km² in each one-degree band from 30° S to 35° S;
`glide_direction_by_latitude.csv`).

**Limits.** The 00:19:37 track is a moment in a banked turn, not a settled heading, so
"along track" is an assumption about what a recovery would do. The glide ratio of 17 and
still air are assumptions. The inner edge of the remainder is the reported, unverified
2018 band. Ocean Infinity's 2025–26 search is reported to have reached farther from the
arc between about 33° S and 36° S and may cover part of the southern end; no geometry is
held. Check: a half-disc of 100 km radius comes out at 15,703 km² against 15,708 km² exact.

Files: `glide_direction_areas.csv`, `glide_direction_by_latitude.csv`,
`glide_direction_tracks.csv`, `glide_direction_checks.json`, `map_glide_direction.png`.

## 8  Addendum 2: the second group after its final-transmission test (24 November 2026)

Codex ran the campaign's unchanged end-of-flight response map for all 130 Tier 2 flights
(`tier2_tested/CODEX_REPORT.md`; package SHA-256 `fd1bf657…5567a7`). Checked here: the 130
are the flights listed in section 1; every re-flown flight reproduces its saved timing
and fuel decisions (largest differences 1.2×10⁻¹⁰ µs and 8×10⁻¹¹ s); a saved campaign
flight reproduced all 138 of its compatibility decisions; 16,284 responses were run.

**Result. All 130 flights have at least one response compatible with the final
transmissions** (1,823 compatible responses of 16,284). The second group therefore joins
the fully tested set. It ends in two stretches of arc 7, near 32.3–33° S and from 35° S to
37.9° S, within 20 km of the arc, 3.9–11.1 km above the surface and descending at
70–121 m/s at 00:19:37.

**All flights tested through the final transmissions now end between 29.9° S and
37.9° S** (221 flights, 3,245 compatible end states), with no tested end state between
about 34.1° S and 35° S.

| Flights | Scenario | Area, km² | Documented (A), km² | Reported, not verified (C), km² | Outside both, km² |
|---|---|---:|---:|---:|---:|
| All tested | Continued descent | 43,279 | 17,245 | 25,956 | 78 |
| All tested | Recovered glide within 45° of track | 231,014 | 63,894 | 55,525 | **111,595** |
| All tested | Recovered glide, forward half | 330,961 | 73,963 | 63,498 | 193,500 |
| All tested | Recovered glide, any direction | 414,504 | 80,814 | 71,430 | 262,261 |
| Second group only | Continued descent | 18,846 | 16,820 | 1,947 | 78 |
| Second group only | Recovered glide within 45° of track | 127,886 | 63,245 | 11,467 | 53,174 |

- **Continued descent.** 99.8 % of the area is documented or reported as searched. For
  the southern stretch the coverage is documented sonar data (89 % of the second group's
  area), not the unverified 2018 band.
- **Recovered glide along track.** 111,595 km² lies outside both layers, 107,586 km² of
  it beyond the arc. It forms two strips: 29–35° S (about 61,000 km², close to section 7)
  and 35–40° S (about 50,600 km²), the second lying beyond the outer edge of the
  documented footprint.

The same limits apply as in sections 3 and 7. In addition: the second group's flights
were found by searches over particular levels and schedules, so the gap near 34–35° S is
a gap in what has been flown, not evidence that no flight ends there. The 2025–26 Ocean
Infinity search is reported to lie between about 33° S and 36° S and may cover part of
both strips; no geometry is held.

Files in `tier2_tested/`: `areas_after_tier2_test.csv`,
`areas_after_tier2_test_by_latitude.csv`, `all_tested_end_states.csv`,
`tier2_summary.csv`, `checks.json`, `map_all_tested.png`. The full response table
(15.6 MB) is held with the run record and not committed.
