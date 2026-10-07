# CODEX TASK 19: extend the ERA5 forcing domain

Authorized by Ryan. Register as the next unused DIRECTOR number and write to a new folder `run2/era5_domain_extension_001/`, with a new suffix if occupied. Read AGENTS.md and the working rules. Preserve all historical code, inputs and results. **Do not modify the existing ERA5 subset or any frozen input.** New data goes alongside it, not over it.

## 0. Why

TASK_030 established that the existing ERA5 subset ends at 10°N and 100°E. The 7th arc crosses 100°E at about 27.5°S, so **the model cannot place an aircraft on the arc anywhere north of that** — there is no forcing there to fly through. 765 of 1,008 sweep rows failed on `WEATHER_HORIZONTAL_OR_TIME_DOMAIN`, the per-start minima piled up at 29.2–31.6°S against that edge, and starts north of 10°N produced no finite history at all.

The northern endpoint question has therefore never been evaluable. This task acquires the data that would make it evaluable. It does not answer it.

## 1. Part A — characterise what exists (report before downloading anything)

Inspect the existing ERA5 subset and report exactly:

1. File format and layout (GRIB, NetCDF, derived binary, per-time or per-variable files), naming convention, and directory structure.
2. Every variable present, with its name as stored, its units as stored, and any scaling or offset applied on load.
3. Pressure levels present, in order.
4. Horizontal grid: spacing, whether latitudes run north-to-south or south-to-north, longitude convention (0–360 or −180–180), and the exact domain bounds.
5. Time steps: first, last, interval, and whether times are instantaneous or accumulated.
6. The ERA5 vintage if recorded anywhere — download date, CDS request JSON, dataset version, any provenance file.
7. What the model's loader expects: the exact function that reads this data, what shape and units it assumes, how it interpolates in space, time and pressure, and what it does at a domain edge. Quote the file and lines.

Deliver `existing_forcing_spec.md`. **If the loader hard-codes the domain bounds or array shapes anywhere, say so explicitly** — that is the code that has to change, and it must be identified before any data is fetched.

## 2. Part B — the request specification

From Part A, construct the CDS request that extends the domain while matching the existing data exactly in format, variables, levels and time steps.

Target domain, generous enough that this is not repeated:

- **Latitude: 20°N to 50°S**
- **Longitude: 55°E to 120°E**
- **Time: 2014-03-07 15:00 UTC through 2014-03-08 03:00 UTC**, hourly
- **Pressure levels:** every level the existing subset uses, plus any between 100 and 550 hPa that it omits. State which are new.
- **Variables:** exactly those the existing subset carries, named identically.

Deliver `cds_request.json` and `cds_request.py` — a runnable script, not a fragment. Estimate and report the download size before running it.

Ryan supplies the credentials. He needs a Copernicus CDS account, the ERA5 pressure-level licence accepted on the dataset page, and an API key in the location the client expects. **Verify the current API endpoint and key format from the CDS documentation rather than assuming** — Copernicus migrated its API and the old endpoint and key format are not valid. Report what the current client requires. Never write a key into any file in the repository, any log, or any output.

## 3. Part C — the overlap check, before anything downstream uses the new data

**This is the gate.** ERA5 has been reprocessed since 2014, so a fresh download may not be the same vintage as the existing subset. Splicing two vintages would contaminate every result downstream silently.

In the region where old and new overlap, compare them cell by cell for every variable, level and time step. Report:

- maximum absolute difference per variable, with units;
- the fraction of cells differing by more than floating-point noise;
- whether differences are structured — concentrated at particular levels, times or regions — rather than scattered.

**Gate: the overlap must agree to within 1×10⁻³ of each variable's units**, or the data are not the same vintage.

If the gate fails: **do not splice.** Re-download the entire target domain fresh, so the whole field is internally consistent from one vintage, and treat the existing subset as superseded for any new run. Say clearly in `FINDINGS.md` that previous results used a different vintage, and quantify how different.

Deliver `overlap_check.csv` and `overlap_gate.json`.

## 4. Part D — ingest and confirm nothing moved

Install the extended field alongside the existing one. Then:

1. **Re-run C120 against the extended forcing at dt 7.5 s.** Report χ², the 00:11 position, fuel and the nine individual residuals against the frozen values (χ² 8.117071226374). Report every difference.
2. **Gate: C120 must reproduce to Δχ² < 0.01 and within 1 km at 00:11.** C120's whole track lies inside the old domain, so extending the domain outward must not change it. If it does, something in the ingest is wrong — report and stop rather than proceeding.
3. Report the new domain bounds as the loader now sees them, and confirm a test point at 105°E and at 15°N returns real values rather than an edge hold.
4. Report where the 7th arc now sits relative to the domain, and the most northerly arc latitude that is now inside it.

Deliver `c120_regression.json` and `domain_after.json`.

## 5. Scope

- No sweep, no grid, no optimiser, no flight search. This task acquires and validates data.
- No arc, candidate, contact or search-area file is read. Part D item 4 uses only the arc's geometry to state a coverage bound, never to score or select anything.
- C120 stays frozen. The existing ERA5 subset stays on disk unmodified.
- Nothing crosses into the drift branch. The drift forcing is separate and is not touched.
- If the download cannot be completed — credentials, licence, quota, size — report exactly what blocked it and stop. Do not substitute a different reanalysis product, a coarser dataset, or an extrapolation of the existing field.

## 6. Stop rule

Deliver Parts A to D and stop. Write "ERA5 domain extension complete" with the new bounds and the C120 regression result in that line, or "ERA5 extension BLOCKED" with the reason. No follow-on sweep without a separate directive.

## 7. Note from Claude (not an instruction)

The overlap check in Part C matters more than it looks. If a 2026 download of 2014 ERA5 differs from the subset this project has used since the beginning, then every flight result in the archive rests on a specific vintage, and that needs recording in the atlas rather than discovering later. A clean pass is the good outcome; a fail is worth knowing about immediately.
