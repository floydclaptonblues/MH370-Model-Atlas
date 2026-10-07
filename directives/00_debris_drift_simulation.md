# CODEX TASK: Standalone MH370 debris reverse-drift simulation (no flight scenarios)

Author: Claude (direction). Executor: Codex. Requester: Ryan.
Status of prior work: Claude drafted `drift_core.py`, `debris_items.py`, `run_reverse.py` in
`MH370-External-Data/claude_drift_runs/2026-10-03_debris_reverse/`. Syntax-checked, NOT yet run end to end.
Treat them as a draft spec; rewrite freely, keep the model definition below.

## 1. Goal
Reverse-drift every debris find from its find place/date back to ONE terminal-event time
(8 Mar 2014 00:19 UTC, day 19/1440 since 2014-03-08 00:00). No flight path, no arc, no BTO/BFO input anywhere
in the drift run. Arcs appear only as an overlay in plots.
Test each item ALONE and in ENSEMBLE, under each leeway class, and report how class changes dispersal
and where the combined backward clouds focus.

## 2. Inputs (read only)
- Currents: `Documents/MH370-External-Data/copernicus_ocean_forcing_v1/`
  - `cmems_2014_2015/monthly/*_wind_envelope_roi_v0_8_20.nc` (8 Mar 2014 .. mid 2015)
  - `glorys12v1_2015_2018/glorys12v1_uo_vo_surface_*.nc` (after that, to 31 Aug 2018)
  - daily, 0.49 m, 1/12 deg, uo/vo only. Land = NaN cells.
- Winds: `Documents/Codex/2026-08-02/files-mentioned-by-the-user-mh370/raw/drift/winds/phase7b/ncep_ncar_reanalysis1/{uwnd,vwnd}.10m.gauss.{2014..2018}.nc` (T62, daily mean, ~1.875 deg)
- Debris table: MOT "Summary of Possible Debris Recovered, updated 30 Dec 2018" (32 items) and pack file
  `MH370_Drift_Science_Pack_v0.1/.../phase7b_debris_forcing_windows.csv` (dates + classification, no coordinates).
- Optional coastline: GSHHG in `raw/drift/coastline/phase7b/gshhg-shp-2.3.7/`.

## 3. Hard rules (fail-closed, per the pack)
- Stokes: WAVERYS explicit Stokes was NOT acquired. Keep explicit Stokes = null. The 1.2% wind-proxy is a
  mutually exclusive mode: it is the FLOOR of total wind slip, never added on top.
- Find coordinates are `FAIL_CLOSED_UNDEFINED` in the pack. Claude's coordinates in `debris_items.py` are approximate
  geocodes of place names (+/- 20-100 km, some uncertain: Daghatane, Anvil Bay, Macenta/Macaneta). Put every
  coordinate in ONE editable CSV (`debris_find_coords.csv`) with columns id, lat, lon, coord_source, coord_uncertainty_km,
  and flag each as `ASSUMED_GEOCODE` until Ryan confirms. Do not silently rely on them.
- Leeway class numbers below are ASSUMPTIONS from NOAA/Trinanes (flaperon ~0.8%, tested 0-4%) and Fu et al. 2018
  (3.29%, angles 0/18/32 left). Put them in `leeway_classes.csv`, editable, labeled ASSUMPTION.
- All forcing daily fields treated as valid at 12:00 UTC. Say so in the report.
- Do not tune any parameter to hit a target region. No forward-fit to the 7th arc.

## 4. Model
Particle velocity = surface current + total_slip * wind10 rotated by signed divergence angle + random walk.
- Integrator: RK4, dt 6 h. Random walk K = 10 m2/s (sensitivity 0, 10, 50).
- Currents bilinear (NaN-aware), time-linear between daily fields. Winds bilinear + time-linear.
- Backward run: start at each particle's find time, integrate to T_EVENT on a time grid anchored at the event.
- Land: static mask from NaN current cells. A reverse particle that enters land is status 1 (invalid); outside domain is status 2.
  No refloat in baseline. Optional run: beach residence delay U(0,60 d) added before the reverse start.
- Particles per item per class: N=500. Initial position jitter +/-0.04 deg over ocean cells only; find time sampled across the MOT date window.
- Domain: lat -55..5, lon 20..115 (or tighter, document it).

## 5. Leeway classes (total downwind slip incl. 1.2% Stokes floor; angle = |left/right| divergence, sign random)
| class | meaning | slip range | angle |
|---|---|---|---|
| C0 | water-following control | 1.2% fixed | 0 |
| C1 | flaperon-like (low freeboard, thin) | 0.8%..3.3% (floor 1.2%) | up to 25 deg |
| C2 | mid-freeboard panel/fairing/flap | 1.5..3.5% | up to 30 deg |
| C3 | high-freeboard buoyant fragment | 2.5..5.0% | up to 35 deg |
Assigned class per item (`debris_items.py`): flaperon and outboard flap = C1; cowls, closet, cabin/IFE panels = C3; fairings/panels = C2.
Run EVERY item under ALL four classes as well, so assignment error is visible.

## 6. Runs
A. Per item x class (32 x 4 = 128 ensembles, N=500, 64,000 particles).
B. Assigned-class ensemble per item; all-class ensembles (everything as C0, as C1, as C2, as C3).
C. Sensitivities on the flaperon (item 1) and one beach-found item: K = 0/10/50, delay = 0/60 d, wind scale 0.5/1/1.5, no-wind (currents only).
D. Closure test: forward-then-backward of a test set must return within 0.001 deg x tolerance, else halt.
E. Optional forward validation: from candidate origins (e.g. 7th-arc points -26..-42 S), assigned classes, with beaching on land. Report which coasts and what timing (flaperon: day 508) they hit. Report only, not a fit.

## 7. Combined origin density
- Identifiable items only (MOT class not "not identifiable" gets weight; "not identifiable" weight 0).
- Per-item density: KDE of surviving backward particles on 0.5 deg grid, ~1 deg Gaussian smoothing, plus an outlier floor eps by classification
  (confirmed 0.02, almost certain 0.05, highly likely 0.10, likely 0.15, possible 0.30).
- Combine region-balanced: mixture within a region, product across regions (Reunion, Mauritius/Rodrigues, Mozambique, South Africa, Tanzania, Madagascar). Avoids overcounting correlated finds.
- Report the highest-density zone, its mass fraction, and the distance to the 7th arc. Repeat for each class set and for the sensitivities.
- Also report survival fraction (alive vs land vs left domain) per ensemble. Low survival is itself a result.

## 8. Outputs (CSV + PNG, no Excel formats; Ryan uses LibreOffice)
- `ensemble_summary.csv`: item, class, N, survival, median end lat/lon, 68% and 90% spread radii (km), mean displacement.
- `class_shift.csv`: per item, centroid shift between classes (km, bearing).
- `combined_density_*.csv` + PNG maps with 7th arc overlay.
- Per-item PNG: all four classes' clouds, find point marked.
- `RUN_MANIFEST.json`: input file hashes, parameters, seeds, code hash, git/commit if any.
- `AUDIT.md`: every assumption, which output depends on it, and an appendix of failed or rejected hypotheses.
- Run to completion with logs; if long, write resumable chunk files.

## 9. Performance note (why Claude stalled)
Reading daily 1/12 deg NetCDF slices costs ~0.16 s/day, forcing load ~33 s, and a flaperon reverse run needs ~500+ days,
so a cold run is minutes. Build a one-time compact local cache (float16 or 1/6 deg, memmap, resumable) of the daily fields,
or keep a persistent process. Use 2 cores if available. Disk on the Codex side is tight: keep the cache in
`MH370-External-Data/claude_drift_runs/` which has room, and do not duplicate the raw files.

## 10. Report back
One page: what ran, survival, where the combined density focuses (lat/lon, spread, distance to 7th arc), how much each class moves the answer,
which results depend on assumed coordinates/classes/daily-mean winds, and what Ryan must confirm.
Say plainly if the clouds do NOT focus anywhere.
