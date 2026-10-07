# CODEX TASK 9 RERUN: independent-seed null tests, 90 runs

Author: Claude (direction). Executor: Codex. Requester: Ryan ("send this to Codex, 90 runs").
This replaces the blocked attempt in `diagnostics_v2/task_9_null_seeds/`. The science, seeds, registration and physics are unchanged. Only the runtime is repaired.

## 0. What blocked it
`runtime_failure.json`: `ImportError: cannot import name 'njit' from 'numba' (unknown location)` from `outputs/fast_interpolation.py`. "Unknown location" means Python found an empty or inaccessible `numba` folder (a namespace package), not a working install. `work/compiled_runtime/` holds `numba-0.68.0` and `llvmlite-0.50.0` dist-info, which is the version the original ensembles used.

Claude checked that `pip install numba` resolves to exactly `numba 0.68.0` with `llvmlite 0.50.0` on a clean Python, so the same-version wheels exist on PyPI.

## 1. Repair the runtime (do not change any model code)
Ryan's machine has network access; the Codex sandbox does not. If the sandbox still blocks sockets, stop and ask Ryan to run this in his own terminal, then continue:

```
python -m venv C:\Users\ihall\Documents\Codex\numba_venv
C:\Users\ihall\Documents\Codex\numba_venv\Scripts\pip install numba==0.68.0 llvmlite==0.50.0 numpy scipy netCDF4 matplotlib
```

Use the Python version that built `work/compiled_runtime` if that is knowable, and record it. Record the versions of numba, llvmlite, numpy, scipy and netCDF4 in the manifest. If Windows still denies access to the venv, report the exact error and stop. Do not write a replacement solver, a NumPy fallback, or any synthetic or bootstrapped result.

## 2. Qualify the runtime before any null run (fail closed)
1. Import `engine`, `common` and `fast_interpolation` without error.
2. Closure gate: 256 particles, 30 days forward then backward, 1.5 h step, K = 0, 0.001 degree tolerance in latitude and longitude. Must pass 256 of 256, as in the original.
3. Reproduction check: rerun at least one saved baseline group (item with assigned class, N2 offshore, 500 particles) from `ensembles/initial.npz` using the original seeds and compare against `ensembles/final.npz`. Report max absolute difference in final latitude, longitude, status and end time. Exact match is expected. If differences appear, report their size and stop. Do not proceed to the null runs until this is reported to Ryan and accepted.
4. Time one full 16,000-particle run before launching all 90 and report the projected total. The original took 2,756 s for 304 ensembles of 500 particles, so expect about 5 minutes per run on 8 threads, about 7.5 hours for 90.

## 3. Run the registered plan
- `run_null_seeds.py` is already written (resumable; refuses to resume if the wrapper hash changes). Use it unchanged. If `set_num_threads(8)` fails because the machine has fewer threads, change only that number and record the edit and the new code hash.
- 30 runs each of `shuffled_regions`, `random_coast` and `observed`, 32 items x 500 particles, with the seeds in `task_7_recovery_delay/registration.json` (`task9_seeds`). Do not reuse the original single-realization seeds. Do not add, drop or reorder seeds.
- All physics frozen: RK4 1.5 h, K = 10 m2/s, noon BOUNDARY_HOLD, GLORYS12V1 0.494 m currents, daily NCEP winds, static NaN land mask, explicit Stokes null, assigned classes, `ASSUMED_GEOCODE` coordinates, N2 offshore rule, absorbing coasts.
- Run in resumable checkpoints and keep logs. Report progress if the run exceeds an hour.
- No parameter, seed or filter may be chosen by agreement with the 7th arc. The arc is used only for distance reporting after every integration is complete.

## 4. Outputs (CSV + PNG + Markdown, no Excel formats)
In `diagnostics_v2/task_9_null_seeds/`:
- `null_seed_results.csv`: per run, combined-density peak lat/lon, peak density, mass fraction within 500 km and 1000 km of the peak, distance of the peak to the original observed peak (35.25 S, 55.75 E), distance of the peak to the arc, survivor share at 31 to 34 S, survival fraction.
- `observed_seed_results.csv`: the same columns for the 30 observed-find replicates.
- `null_focus_summary.csv`: per experiment, mean, SD, 5 to 95%, min and max of peak latitude, longitude and peak density; fraction of runs whose peak lies within 250, 500 and 1000 km of the original observed peak; position of the observed-run result in the null distribution (percentile) for peak density and for mass fraction.
- PNG: peak locations for all runs (three experiments, distinct markers, original peak and arc overlaid); PNG of the percentile position.
- `REPORT_9.md` (one page, replaces the blocked report), `RUN_STATUS.csv` updated per run, `unrun_items.csv` and `unavailable_outputs.csv` emptied or updated truthfully, manifest with package versions, code hashes and seed list, and `AUDIT.md` additions (assumptions, which outputs depend on them, appendix of failed or rejected hypotheses, including the blocked first attempt).

## 5. Report back
One page: what ran, runtime qualification results (closure, reproduction), how many of the 90 runs completed, where the combined density peaks across seeds and how widely, what fraction of null runs reproduce the 55.75 E focus within 250, 500 and 1000 km, where the observed result sits in the null distribution, and whether the earlier conclusion is stronger, weaker or unchanged. Say plainly if the focus does not persist, or if it persists equally in the nulls (meaning it is a property of the method and survivor conditioning, not of the finds). List what Ryan must still confirm: find coordinates and date intervals, class assignments and measured slip/divergence, wind and Stokes adequacy, beach residence and refloat, and detection delays.
