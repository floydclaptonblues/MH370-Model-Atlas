# CODEX TASK 13: open-items registry and confirmation ingest (no drift runs)

Authorized by Ryan. Register as the next unused DIRECTOR number and write to a new folder `task_13_open_items/` beside the Task 12 outputs. Preserve all historical code, inputs and outputs. Frozen B0 physics, the Task 11 and Task 12 results and every existing input table are not edited.

## 0. Purpose and limits

Five inputs to the drift analysis are still assumed or unconfirmed. This task finds what the project files actually say about each, records provenance, and builds a confirmation sheet that Ryan fills in. It then provides a loader that validates his confirmed values into a NEW versioned input table.

This task does NOT:
- run any drift, hindcast, forward or reverse job, or re-score anything;
- invent, estimate, interpolate or "reasonably assume" a value that no file states;
- download data or use the web. Use only the project files, the Drift Science Pack reports, and files Ryan supplies;
- use any MH370 arc, flight path, candidate position or search area to choose among values;
- change the frozen B0 inputs. Confirmed values go into a new table with a new version tag; B0 keeps its assumed values.

Every value is labelled one of: SOURCED (a file states it, with path, hash and location), ASSUMED (the project chose it, with where), CONFLICT (two files disagree), MISSING (no file states it).

## 1. Items to registry (one section each)

### 1.1 Find coordinates and date intervals (32 items)
For each of the 32 items, read the existing MOT/find table and the ASSUMED_GEOCODE table. Record: item id, object description, region, the coordinate used by B0, how that coordinate was derived (named beach, town centroid, administrative centroid, other), the date interval opens/closes and whether each bound is a discovery date, a report date, an observation date or an inferred window. Flag items whose coordinate is a centroid larger than the 100 km primary matching radius, and items whose interval is longer than 30 days. List the 23 distinct windows with their item ids. Do not search for better coordinates; list what is missing.

### 1.2 Measured class slip and divergence
Locate any file that states measured or published leeway / windage / slip for a flaperon, a floating aircraft part, or a comparable object, and any file that gives the basis for the C0 to C3 assignments (1.2%, and the C1, C2, C3 values). For each class record the slip value, how it was set (measured, literature, proxy, assumed), and which items it is assigned to. Record where divergence angle or downwind/crosswind decomposition is stated or absent. If the class values come only from the project's own assumptions, say so.

### 1.3 CSIRO wind source
Find where the "CSIRO 1.2% wind proxy" is cited. Record the file, the wording, and whether it names a paper, a report, a dataset or only a label. State plainly if the source cannot be resolved from the files. Also record which wind product B0 uses (daily NCEP/NCAR Reanalysis 1, T62) and whether any file records a comparison with ERA5 winds. Do not add ERA5 or any new wind product.

### 1.4 Beach residence and refloat
Find any file that states how long a particle stays at the coast after landing, whether refloat is allowed, and what the beaching algorithm is (static land mask versus GSHHG L1 with 5 km segments). Record B0's rule (absorbing, no refloat) and the Phase 7B alternative, with the measured difference from `beaching_variant_check.csv` for reference only.

### 1.5 Detection delay and discovery versus first-beaching
Find any file that states how long between landing and discovery for any item, or any assumption about it. Record the delay values used in the Task 11 follow-up (0, 30, 90, 180 days) and state that they are sensitivity values, not measurements. List, for each item whose find report gives a discovery date, whether any file says when it was likely to have landed.

## 2. Deliverables (CSV, Markdown and PNG only)

- `open_items_registry.csv`: one row per item/field with columns `section, item_id, field, b0_value, status, source_path, source_sha256, source_location, note`.
- `ryan_confirmation_sheet.csv`: one row per ITEM x FIELD that is not SOURCED, with columns `section, item_id, field, b0_value, status, what_is_needed, ryan_value, ryan_source, ryan_date_confirmed`. The last three columns are blank. Ryan fills them.
- `window_summary.csv`: the 23 distinct windows with width in days, region, item ids.
- `registry_summary.md`: counts by section and status, the conflicts, and the five most consequential gaps ranked by how many items they touch (a count, not an opinion about the source location).
- `load_confirmations.py`: reads `ryan_confirmation_sheet.csv`, validates each filled row (numeric ranges, coordinate within the forcing domain or the coast region, date order, units), rejects any row with a blank source, writes `confirmed_inputs_v1.csv` plus `confirmation_report.csv` listing accepted and rejected rows with reasons. It must not edit any B0 table. Include a test with a small synthetic sheet that is clearly labelled as a test and never written to the real outputs.
- `NOTES.md`: assumptions, failed or unavailable searches, file hashes, runtime, audit trail linking each registry row to its source file.

## 3. Verification

- Every SOURCED row must resolve: the cited file exists, the hash matches, and the cited text or table location exists. Report the count that passed and any that failed.
- The item count must equal 32 and the distinct-window count must equal 23, or the discrepancy is reported.
- Counts in `registry_summary.md` must match the CSV.
- Confirm no historical file hash changed (compare against the Task 11 and Task 12 manifests).

## 4. Stop rule

Deliver the registry, the sheet and the loader, then stop. No drift run, no re-matching, no corrected grid, no use of confirmed values until Ryan has filled the sheet and asked for a separate run. Write "registry complete; awaiting Ryan's confirmations" when done. If a section cannot be answered from the files, state that plainly and mark the rows MISSING; do not fill them.

## 5. Notes from Claude (not instructions)

- The 100 km primary radius and one-day windows make the coordinates and date intervals the most consequential items. Items with long windows (for example items 28, 29, 31 and 32, which share a 15-month window) are easy to match by chance, and a coordinate that is a centroid does not support a 100 km rule.
- Measured slip for a flaperon may not exist in the files. If it does not, 1.2% and the C1 to C3 values stay assumptions, and the sheet should say so rather than ask Ryan for a number he may not have.
- Detection delay may be unknowable for most items. A blank, labelled UNKNOWN, is a valid confirmation.
