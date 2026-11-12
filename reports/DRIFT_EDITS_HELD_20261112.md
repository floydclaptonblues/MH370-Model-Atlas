# Drift-page edits held for review, 12 November 2026

The recovered editorial commit `158fb35` proposed wording changes to `drift2.html`, `drift3.html` and `drift4.html`. They are **not published**. The three pages are byte-identical to the published baseline `e79b34e`.

Reason: the drift pages are to stay as they are until Ryan Hall has reviewed them. Several of the proposed changes are not tone edits; they alter what the pages claim (the one-year 13-versus-11 comparison described as a domain comparison rather than a timestep test; the convergence statements; "latitude outweighs along-arc position" restated as fixed-latitude east–west offsets; the scope of the G0 statement). Those are decisions for the author of the pages.

The proposed changes are kept in `DRIFT_EDITS_HELD_20261112.patch` (source bodies only; apply to `src/`, then run `python3 gen.py`). `tests/check_editorial_preservation.py` now asserts that the drift pages equal the baseline.
