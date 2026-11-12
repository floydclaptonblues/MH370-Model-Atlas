# Atlas editorial recovery, 12 November 2026

Recovered baseline: `e79b34ea61f207ab8eb86101bdc314a5788579c9`.
The interrupted workspace was unavailable. These are newly reconstructed edits from the supplied handoff, not recovered copies of its uncommitted patches.

## Scope

- Replaced thread-addressed narration on public explanatory pages with project/experiment descriptions.
- Retained Ryan Hall's signed assessment byte-for-byte. Kept the AI assessment as an attributed historical statement and added a separate status notice.
- Labelled the shared population summary as the published six-history branch, rather than the full catalogue. Removed the generic fuel-exhaustion and floor-exit times, which vary by case. Separated rejected scenarios from unavailable/uncomputed data in the label key.
- Corrected the canonical page's scope: its display contains derived timing rings, approximate debris geocodes and search boxes as well as primary observations and reanalyses.
- Put old flight experiments, the north–south comparison and the closed chapter's correction narrative behind labelled archive controls. Their recorded numerical results remain available.
- Distinguished rejection of the specified G0 response from exclusion of its geographic region.
- Corrected the one-year 13-versus-11 crossing comparison: it compares domains and is not a timestep-convergence test. Limited claims from the actual two-step sensitivity test; chaotic advection alone does not prove numerical convergence is unattainable.
- Distinguished fixed-latitude east–west offsets from distance along the satellite arc, preserving reported crossing values and boundary-censoring qualifications.

No new model runs, scoring, catalogue imports, or updates from later lower-speed experiments were performed in this editorial recovery. A dated historical extent is not a current physical limit.

## Verification

`python3 gen.py`, `python3 -m py_compile gen.py`, `node --check common.js`, and `git diff --check` passed at this stage.

`python3 tests/check_editorial_preservation.py` checks all generated root-page tables against the recovered baseline. All 3,039 numeric tokens remain in the same page/order. Some glossary prose cells contain numbers; their wording changed but their numeric tokens did not. This is a new explicit check, not a repetition of the interrupted thread's claimed 1,211-cell test.

The signed assessment source and generated page, and the Flight Lab dataset, are byte-identical to the baseline.

Local Chromium rendering could not start because the execution environment blocked its process socket. The attempted Playwright pass therefore produced no visual or interaction validation. Browser validation, the Lab regression suite, final integrated checks and deployment status are separate from this editorial record.
