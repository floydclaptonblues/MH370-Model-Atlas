# Inmarsat 3-F1 comparison at the published Table 4 epochs

Published with the Atlas Canonical Data page on 14 November 2026. This package compares two descriptions of the same satellite: the published Table 4 states and a historical TLE propagated with SGP4. Table 4 remains the reference for the existing Atlas satellite display. Publishing this comparison does not replace a flight-model ephemeris, recalibrate measurements or change the running production experiment.

## Reproduction

Unzip, enter the directory containing this README, and run the commands below. The executed environment used CPython 3.12.14 on Linux. Package installation requires access to PyPI or a local wheel mirror. The calculation itself runs offline. Leave Python assertions enabled.

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python compare.py
```

The run regenerates comparison.csv with signed Cartesian residuals and both original and propagated vectors. RMS is the unweighted root mean square of the 11 vector norms. Times are UTC on the dates in the JSON, zero seconds within each listed minute, including March 8 after midnight. No interpolation to handshake times or adjustment of clock or position is applied.

## Source identity

All three files under inputs are verbatim blobs at https://github.com/floydclaptonblues/MH370-Model-Atlas/tree/1bc68965efd2ec4c8e30cf059c71799f41b3a3b4/data . The TLE and provenance live in its satellite subdirectory. Checksums in compare.py guard the two scientific inputs. The provenance SHA-256 is 8098fa88a4c072c60ac436aa840557d015b9b8768b13e99b622f1c130a9a1393. The study reporting Table 4 is https://doi.org/10.1017/S037346331400068X . All 11 Cartesian states and times match the printed table at its precision. The latitude and longitude are additional Atlas fields. Geocentric latitude and east longitude from the tabulated XYZ reproduce them within 0.0005 degree.

## Method

The three sets pass their six checksums and yield identical SGP4 states at every evaluated time. They describe a single GP fit. Use WGS-72 SGP4, with the deep-space branch selected by the orbital period, and a split UTC Julian date. Epoch 2014-03-07T23:13:15.867264 UTC. Positions and velocities leave SGP4 in TEME in km and km/s. Transform to ITRS as the terrestrial realization of Table 4 ECEF, with X at Greenwich, Y at 90 degrees east and Z north. The paper specifies ECEF axes but no particular terrestrial frame realization.

Astropy applies the Vallado TEME convention, GMST82 evaluated in UT1, and IERS B pole coordinates with the TIO locator set to zero. The offline historical IERS B file in the pinned package has SHA-256 ceff866eb69d1e3ff454fa21a7d74c661088d47b267cc3289715d6879195359a. The CSV records interpolated UT1-UTC and pole coordinates for each row. For rotation R from TEME to ITRS, position is R r and velocity is R v + (dR/dt) r. A separate ERFA matrix/product-rule calculation agrees with Astropy to within 0.00000003 m/s, checking implementation of the same convention. A different diagnostic differentiates successive SGP4 positions using a centered 10-second span. That differs from transformed SGP4 velocity by 0.066 to 0.068 m/s. The reported velocity residual always uses SGP4's supplied velocity. Transformation reference: https://docs.astropy.org/en/stable/coordinates/satellites.html .

## Findings and scope

The TLE minus Table 4 discrepancies have 3D RMS 3.003 km and 0.240 m/s. Position norms range from 2.194 to 4.193 km, velocity norms from 0.147 to 0.286 m/s. The TLE radius is 1.275 to 1.850 km smaller throughout. At 19:40 the Z difference is only +0.006 km while the 3D difference is 2.508 km. At 00:20 the position difference is (-3.690, +0.360, -1.958) km and the velocity difference is (-0.118, +0.058, -0.067) m/s. Smooth offsets exceed Table 4 nearest-digit rounding bounds of 0.087 km and 0.0087 m/s in 3D. Those bounds concern printed precision only.

These results corroborate the broad geometry and motion. They provide no absolute reference or covariance for either solution. The proximity of the epoch limits propagation time, but the underlying fit can already differ at epoch. Source precision, orbit determination and model conventions can contribute. There is no maneuver diagnosis or fitted correction here. For background on object-specific TLE performance see https://celestrak.org/columns/v04n05/ . Effects on handshake BTO or BFO require evaluating both links and the model calibration at the actual event times. No aircraft, terminal descent or search-location calculation was run.

## File integrity

The comparison CSV and the three source files are byte-for-byte copies of the reviewed package. The script and pinned requirements are also unchanged. The source commit predates this page publication.

| File | SHA-256 |
| --- | --- |
| `comparison.csv` | `6de7828c34a74840afd641a2b66e4cb1c558fd48bb2162b407f486f9862afed3` |
| `compare.py` | `edd3d721177f7c678ba10d59e050ea8d8e69a000f0117807a9f275d7e5f83c23` |
| `requirements.txt` | `52bc3b8616086a39316fdc365ff966dbcc5b0ee4e938b3d54fce944759ef7d1d` |
| `inputs/satstate.json` | `0ba0f9ebe2e6258722f98c7726cd11cd732e5f38d559e940f810f560d2209a2d` |
| `inputs/inmarsat_3f1_celestrak_20140307.tle` | `0223860d5a37631b25234350e0d603d55912a36811b816312a5b8ee771210826` |
| `inputs/inmarsat_3f1_celestrak_20140307.provenance.json` | `8098fa88a4c072c60ac436aa840557d015b9b8768b13e99b622f1c130a9a1393` |

The page rounds state values for display; the CSV retains the calculated values and signed component differences. Table 4 velocities and propagated state velocities are in km/s; velocity differences in the CSV are in m/s.
