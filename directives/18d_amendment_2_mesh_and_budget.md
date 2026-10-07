# CODEX TASK 18 — AMENDMENT 2: screening mesh and revised budget

This unblocks TASK_030. Parts A to E of Task 18 and Amendment 1 (Part F replaced by the cruise-profile export) are otherwise unchanged. Part A is complete and its finding stands; do not rerun it.

## 1. Budget

The 240-minute ceiling is replaced by a **600-minute (10 hour) numerical ceiling**, with 40 minutes reserved for verification and 20 for packaging, reported separately and not mislabelled as CPU time. The BLOCKED report was correct behaviour under the old rule and the rule itself is unchanged — if the selected tier does not fit the new ceiling, report BLOCKED again with the numbers rather than shrinking the grid.

## 2. Screening mesh

Run the sweep at **dt = 15 s** instead of 7.5 s. TASK_021 verified records on 15, 7.5 and 3.75 s meshes and all passed.

**Before committing to the grid**, confirm the mesh is adequate for screening:

- Re-run C120 at its own commanded parameters at dt 15 s and dt 7.5 s.
- Report Δχ², the 00:11 position difference, and the fuel difference between them.
- **Gate: proceed at 15 s only if Δχ² < 0.05 and the 00:11 position differs by less than 2 km.** These are mine, declared now. If the gate fails, report the measured differences and fall back to dt 7.5 s with the tier reduced to whatever fits the 600-minute ceiling.

Record the gate result in `mesh_gate.json` either way.

## 3. Tier

With the gate passed, re-benchmark one flight at dt 15 s and select the largest complete tier that fits, from the same ladder in Part B. The expectation is roughly 17 s per flight, which would put **T4 (1,680 flights)** inside the ceiling at about 8 hours and leave T3 (4,410) out of reach. Report the benchmark, the forecast and the tier chosen before running.

Arc-1 resolution still never goes below 1.0° and the span never narrows. Other dimensions coarsen first.

## 4. Final-mesh re-run of the reported profiles

Everything reported as a cruise profile must be re-run at **dt 7.5 s**:

- every row of `cruise_profiles.csv` and `cruise_profile_summary.csv`;
- any grid point quoted by value in `FINDINGS.md`.

That is one re-run per arc-1 start, about 21 flights, roughly 12 minutes. Report the 15-to-7.5 s Δχ² for each, and flag any whose χ² ordering changes between meshes.

The screening grid itself stays at 15 s and must be labelled `mesh=15s` on every row, so no reader mistakes a screening value for a verified one.

## 5. Unchanged

Everything else holds: no optimiser, latitude is an output, no arc or candidate or contact comparison, incoming-leg figures reported but never used to filter, C120 frozen and not replaced by any flight scoring better, nothing crossing into the drift branch.

## 6. Note on Part A

The Part A result — that C120's 0.5°N start is a fitted latitude-box boundary rather than an observed latitude — is retained as delivered and needs no rerun. Carry it into `FINDINGS.md` alongside the sweep result, since it is the reason the sweep matters.
