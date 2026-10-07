# CODEX TASK 18 — AMENDMENT: Part F withdrawn, replaced by cruise-profile export

**Part F (survivor set and terminal handoff) is withdrawn in full. Do not execute it.** No survivor selection, no frozen state export, no terminal handoff, no stage-2 preparation. Parts A to E of Task 18 are unchanged.

Replace Part F with the following.

## Part F (replacement) — cruise profiles

For **every arc-1 start point in the grid**, export the cruise profile of that start's lowest-χ² flight. One profile per start, whether or not it meets any reporting band. A start whose every flight failed integration gets a row saying so with the reason.

`cruise_profiles.csv`, one row per start per timestamp, at the five scored epochs:

- 19:41:03, 20:41:05, 21:41:27, 22:41:22, 00:11:00 UTC

Columns per row: arc-1 start latitude and locus longitude, commanded bearing, commanded Mach, commanded pressure, k, timestamp, latitude, longitude, ground speed (m/s and kt), track (deg), geopotential height (m and ft), pressure (hPa), Mach, temperature (K), vertical speed (m/s), total fuel remaining (kg).

`cruise_profile_summary.csv`, one row per arc-1 start: the start coordinates, the commanded parameters of its best flight, nine-term χ² and all nine squared residuals, 00:11 position, fuel at 00:11 and 00:17, fuel exhaustion time if any, envelope and weather status, path length 19:41 to 00:11, maximum turn rate, and the Part D incoming-leg figures.

That is the deliverable Ryan asked for. Keep the Part E map and tables as specified; this adds the profiles themselves.

## Scope

- No terminal search, no frequency evaluation at 00:19:29 or 00:19:37, no contact propagation.
- No flight is adopted. C120 remains the frozen reference, including against any flight scoring better.
- Nothing crosses into the drift branch.
- A cruise profile here is a commanded model flight, not a reconstructed aircraft history.
