# From a saved fuel-exhaustion state to the terminal model: what is carried, derived and assumed

16 November 2026, revised the same day after Codex's review of `2fc9d0e`. Part of the package in this directory, prepared for review with `METHOD.md`. **No terminal calculation has been run.** The statements below come from reading the source that will be reused; each is turned into a numerical check in the gate (`term_cat.py --phase handoff`), and the checks are listed with their limits.

## The saved record

For each of the 229 accepted flights whose engines run out of fuel before 00:40:00, the cruise catalogue (`../CRUISE_LEVEL_PRODUCTION_108/`, revision `2a016b1294fa`) saved one record at the instant the modelled engine fuel reaches the reserve. It was written by `../ALT_STARTS_CRUISE_LEVEL_PILOT/camp_engine.py` (function `_evaluate`), using the engine's own motion routine at the event time with central differencing. `build_manifest.py` copied each record unchanged into `EVENT_STATES_229.json`, added the flight's identity beside it, and hashed it.

The earlier terminal experiment on other flights (`../NEW_BRANCH_TERMINAL/`) took records with the same fields, written by the same lines of code, into the same solver.

## Mapping

"Carried" means the number enters the terminal model exactly as saved. "Derived" means the terminal model computes it from carried numbers. "Assumed" means the terminal model imposes it; nothing in the cruise flight supplies it.

| Quantity | In the saved record | In the terminal model | Class | Check in the gate |
|---|---|---|---|---|
| Time | `t_s`, seconds after 7 March 2014 19:41:03 UTC | Start time of the propagation. Same origin: 00:19:29 is 16,706 s and 00:19:37 is 16,714 s in both | Carried | Identical to the time inside the state; inside the event bracket; before 16,706 s. No clock is reset |
| Position | Earth-fixed Cartesian, metres | State components 1 to 3 | Carried | Identical, bit for bit |
| Velocity | Earth-fixed Cartesian, m/s, relative to the rotating Earth | State components 4 to 6 | Carried | Identical, bit for bit |
| Acceleration | Earth-fixed Cartesian, m/s² | Used once, at the event, to obtain the force the wing was supplying. Not a state | Carried | Enters the force check below |
| Latitude, longitude, height | Degrees; height above the ellipsoid, metres | Recomputed from the position | Derived | Within 1e-9 degrees and 1e-6 m of the saved values |
| East, north, up velocity | m/s | Recomputed from position and velocity | Derived | Within 1e-9 m/s |
| Mass | 174,369 kg without fuel plus the 6.804 kg reserve | The same sum | Carried | Within 1e-9 kg |
| Fuel | Total fuel equal to the reserve, 6.80388555 kg: no engine fuel | Engine fuel zero; the reserve becomes the APU fuel (state component 11) | Carried | Identical |
| Air temperature, pressure, density, wind | Not saved | Read from the same weather object at the saved time and position, interpolated in height | Derived | Reported per flight |
| Speed through the air, Mach number | Mach number saved | Recomputed from velocity, wind and temperature | Derived | Mach within 1e-9 of the saved value |
| Bank angle | Saved | Recomputed from the acceleration; held until the response starts | Derived | Within 1e-9 degrees |
| Lift coefficient | Not saved | From the lift needed to produce the saved acceleration at the saved mass and airspeed; held until the response starts | Derived | Finite, positive, inside the range the aerodynamic model supports; the solver's value at the event equals it |
| Lift reference direction | Not saved | Unit vector perpendicular to the direction of flight in the vertical plane (state components 7 to 9) | Derived | Covered by the force check |
| Thrust after the event | | Zero, from the event instant | **Assumed** | |
| Lift and bank before the response | | Lift coefficient and bank held at their values at the event | **Assumed** | |
| The response | | At a chosen onset time: lift coefficient to half its value and bank to 60° left or right, both over 10 s | **Assumed** | |
| Airframe | | Clean and intact; no change of drag from windmilling engines, a ram-air turbine or flight controls | **Assumed** | |
| APU fuel | | Drawn at 2 lb per 55 s from the event instant until the 15 lb are gone; feed uninterrupted | **Assumed** | |
| Vertical wind | | None | **Assumed** | |

**Units and frames.** SI units throughout, in both models. Position and velocity are in Earth-fixed axes in both; the terminal equations contain the Earth-rotation terms that go with that choice. No conversion is applied.

**Height.** The weather object is the one the cruise flight used, in the same configuration (the solver refuses any other): geopotential heights converted to height above the ellipsoid with the geoid correction. The saved height and the height recomputed from the saved position must agree to a micrometre, which ties the two conventions together.

**Weather.** The cruise flight read the weather on its commanded pressure surface. The terminal model reads the same data as a column in height at the aircraft's position. At the event the two readings give slightly different temperature and wind for the same point, and the terminal model's is used from then on. In the first-batch flight of `A001_CONTROL` the saved air-relative Mach number is 0.6699997 against a commanded 0.67.

## The force check

At the event the terminal equations give an acceleration with no thrust. The saved acceleration belongs to the powered flight. If position, velocity, mass, weather and the lift reconstruction are all handed over correctly, the two can differ only along the direction of flight through the air, by the thrust that has been removed. The gate requires:

| Check | Requirement |
|---|---|
| Difference between saved and zero-thrust acceleration, measured across the direction of flight | At most 1e-6 m/s² |
| Thrust implied by the difference along the direction of flight, divided by the terminal model's drag | Between 0.95 and 1.05 |
| Lift divided by weight | Between 0.98 and 1.02 |
| The solver's acceleration at the event, for the left and the right response, against the zero-thrust value | Within 1e-9 m/s² |
| Lift coefficient and Mach number at the event | Inside the range the aerodynamic model supports |

The first and fourth rows test the reconstruction and the solver against each other. The second and third are plausibility checks on the saved numbers themselves: an acceleration in the wrong frame or unit, or a wrong mass, would move them far from one. Their bands are set here, before any evaluation.

These are consistency and plausibility checks. They do not repeat the earlier comparisons against the thrust and drag recorded by the powered flight, and the findings will not describe them as such.

## Quantities the saved record does not hold

| Not saved | Was it an input of the terminal solver? | Consequence |
|---|---|---|
| Thrust, drag, lift and lift coefficient of the last powered stage | No | The two published force checks that used the recorded thrust cannot be repeated from the records. The checks above replace them. What they do not establish: that the terminal model's drag at the event equals the drag the cruise stage computed. Both come from the same pinned force routine, and on the 24 earlier flights where it could be tested the two drags were identical (`../TWO_TURN_TERMINAL_DYNAMICS_PILOT/HANDOFF_CHECKS.json`); recorded thrust was 0.986 to 0.992 of drag there |
| Air data on the commanded pressure surface (true airspeed, pressure) | No | The size of the difference between the two weather readings at the event is not reported per flight |
| Lift, bank, Mach number at any time other than the event | No | Not needed |

Every input the solver reads (`pilot_runner.initial_state`: time, the three vectors, latitude, longitude, height, total fuel) is in the saved record. **No cruise flight has to be recomputed to run the terminal calculation**, and none is in this method.

Codex's review accepted the replacement checks without a replay of the four first-batch flights. No replay is part of this method.

## Differences from the precedent

| Item | Precedent (`NEW_BRANCH_TERMINAL`) | Here |
|---|---|---|
| Source of the event states | Twelve flights recomputed to 00:40 for the purpose, behind a three-flight gate | Saved by the production run; copied, not recomputed |
| Fuel-integration boundaries past 00:11 | Published list, including 16,706 s | The same published list (`terminal_runner.OBS_BOUNDARIES`); every event used here precedes 16,706 s |
| Time from fuel event to 00:19:29 | About 4 minutes | 136 to 509 s (`ELECTRICAL_BOOKKEEPING_BY_GROUP.csv`) |
| Handoff checks | None beyond the control reproduction | This document |
| Continuation controls | Earlier gate cited | Repeated in the gate |
| A transition unfinished at 00:19:37 | Could not be continued | Continued through the same stage drivers; two gate cases (`METHOD.md`) |
| Frozen inputs | Source files pinned by the solvers' own lists | Every source and data file read, including the performance table, the weather arrays and the satellite inputs |
| What a response is tested against | One label, "compatible", from the frequency tests | Each requirement separately (`METHOD.md`) |

The longer unpowered interval matters. Before the response starts, the model flies with no thrust at a fixed lift coefficient for between 76 and 517 s, longer than in any earlier use of this solver. Whether the model stays inside its supported range for that long is an outcome of the run.

## Source and data that are reused

`DEPENDENCIES.json` lists the 36 source files and 25 data files (260 MB) read while the existing solvers are imported and the gate's reference results are loaded, each with its hash. It is written by `deps.py`, which records every file the process opens from its first line, and evaluates nothing. `METHOD.md`, "Frozen inputs", says how the list is enforced.

| Role | File |
|---|---|
| Onset calculation | `../TERMINAL_ALL_CANDIDATES_ONSET/tac_runner.py` (function `one`) |
| Event state to solver state, propagation with explicit stops, frequency tests | `../TWO_TURN_TERMINAL_DYNAMICS_PILOT/pilot_runner.py` |
| The response law | `../TWO_TURN_TERMINAL_ONSET_REQUIREMENTS/or_common.py` |
| Satellite prediction at a given time | `../TWO_TURN_TERMINAL_POWERED_CONTINUATION/terminal_runner.py` (function `exact_epoch_prediction`) |
| Continuation in four stages | `../TERMINAL_ALL_CANDIDATES_CONTINUATION/tcc_common.py` (function `chain`) and the stage drivers it imports |
| Continuation controls | `../TERMINAL_ALL_CANDIDATES_CONTINUATION/tcc_runner.py` (function `controls`) |
| Terminal equations and frequency tests | `descent.py`, `envelopes.py` in the read-only flight-model directory |

| Physical input | File (in the flight-model directory) |
|---|---|
| Aircraft performance table | `ps.csv` |
| Weather arrays and their configuration | `extended_validated.npz`, `forcing_config.json` |
| Geoid grid | `WW15MGH.GRD` |
| Satellite ephemeris, ground station | `…satellite_ephemeris.parquet`, `…ground_stations.parquet` |
| Frequency model and calibration | `…bfo_model.json` |
| Event table | `…mh370_satcom_canonical_events_v1_0.csv` |

All of these are among the 26 files shared with the cruise catalogue's frozen list, and each has the hash the catalogue was computed with. That comparison is against the catalogue's list and not against a value computed from the file being checked.

The remaining data files are the published records and manifests the gate compares with.

## 22:41

No satellite prediction, residual or comparison is made at 22:41. `term_cat.py` wraps the prediction routine so that a request at any time other than 16,706 s or 16,714 s is recorded as a stop and raised as an exception that ordinary error handling cannot catch (`METHOD.md`, "Enforcement").

The 22:41 values are nevertheless loaded into memory. The event table above holds the recorded timing and frequency of 19 events, one of them at 22:41, and the flight model's shared setup reads it and builds an array of recorded frequencies at five times when it is imported, before any guard exists. This package uses neither at 22:41 and prints neither. It does not claim the measurement is unread. See the addendum to `../HOLDOUT_2241_DISCLOSURE/DISCLOSURE.md`.

Two of the reused files (`pilot_runner.py`, `terminal_runner.py`) define a path to the directory of the withheld comparison. In `pilot_runner.py` the path is never used. In `terminal_runner.py` it is used only inside the function that built an earlier report's manifest, which nothing here calls. No file of that directory is on the frozen list, and a read of one during the run would stop it.
