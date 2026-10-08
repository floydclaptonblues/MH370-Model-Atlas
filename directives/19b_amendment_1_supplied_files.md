# CODEX TASK 19 — AMENDMENT 1: the ERA5 files are already downloaded

Ryan has fetched the data himself. **Part B's download step is withdrawn.** Parts A, C and D stand unchanged.

## 1. The supplied files

```
C:\Users\ihall\Downloads\5abd7a88ca5dbe8413c7393c50d6ba46.zip
C:\Users\ihall\Downloads\f050b20afa9b5b576a66de30d740e104.zip
C:\Users\ihall\Downloads\6a3911269dc3ac3a79295743f1fe85a8.nc
C:\Users\ihall\Downloads\71ac16a7d43ddbe6854b90f48fee942b.nc
```

Copy them into the task folder before touching them. Do not work in `Downloads`, do not modify the originals, and record the SHA-256 of each as received.

## 2. Part B replacement — inventory, not download

**Determine each file's real format from its magic bytes, not its extension.** CDS delivers GRIB and NetCDF under both, and a `.zip` commonly contains one or more `.nc` inside. Unpack the archives and inventory every dataset found, including those nested in the zips.

For each dataset report: format; variables with stored names and units; pressure levels; horizontal grid spacing, latitude ordering and longitude convention; exact domain bounds; time steps; and any CDS request metadata or provenance attributes embedded in the file.

Then produce `supplied_vs_required.csv`, one row per required item from Part A's `existing_forcing_spec.md`, marked PRESENT, MISSING or MISMATCHED:

- every variable the existing subset carries;
- every pressure level it uses, plus any between 100 and 550 hPa;
- hourly steps from 2014-03-07 15:00 UTC to 2014-03-08 03:00 UTC;
- coverage to at least 20°N, 50°S, 55°E, 120°E.

**Report gaps before ingesting anything.** If a variable, level or hour is absent, say so plainly and state what a follow-up request would need. Do not interpolate, extrapolate or substitute to fill a gap, and do not quietly proceed on a partial field.

Also state whether the four files are complementary (different variables, levels or times) or overlapping, and if they overlap, whether they agree.

## 3. Unchanged

- **Part A** still runs first and still reports before anything else, including whether the loader hard-codes domain bounds or array shapes.
- **Part C's overlap gate still applies in full.** These were downloaded in 2026; the existing subset may be a different ERA5 vintage. Agreement to 1×10⁻³ in the overlap region, or do not splice — re-derive the whole domain from the new files alone and record that earlier results used a different vintage.
- **Part D** still re-runs C120 and still requires Δχ² < 0.01 and within 1 km at 00:11.
- No sweep, no grid, no optimiser. C120 frozen. The existing subset unmodified. Nothing crosses into the drift branch.

## 4. Stop rule

Unchanged: "ERA5 domain extension complete" with the new bounds and the C120 regression in that line, or "ERA5 extension BLOCKED" with the reason. No follow-on sweep without a separate directive.
