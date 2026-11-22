# TASK042 starting Mach 0.80–0.84: publication evidence

This directory publishes the separate completed experiment
`TASK042_Mach080_084_20261121_001`. Ten selected histories—five starting Mach
values from each of two historical origins—are eligible under the experiment's
model and fuel-window rules and pass the declared numerical refinement checks.
This is a finite local search, not a global optimum or branch-connectivity proof.

## Provenance

`RESULTS.csv`, `RESULTS.md`, `CLOSING_AUDIT.json`, `design.json`, and the PNG/PDF
figure are byte-identical copies of the saved experiment files. Their original
paths and SHA-256 hashes are in `source_manifest.json`. The completed record ZIP
has SHA-256:

```text
a55a217300bf29f67b3631690cc0cc175a4577da58b59bc2164175d8e4d48c92
```

The source repository commit identifies the starting source snapshot. It does
not imply that these new results were committed to that repository. The original
report and audit retain their historical scope and workspace paths as evidence.

`comparisons.json` is a compact, explicitly labelled extraction of the original
`analysis/retained_comparisons.json`; its original hash is recorded. It preserves
all ten CSV-equivalent rows, twenty mesh-comparison summaries, per-mesh fuel
eligibility and edge margins, five comparisons between origins, accounting and
source identities. Full trajectories and resource traces are omitted. No model
input, geometry, integration, fitting or prediction was performed to produce it.

## Interpretation

- **Starting Mach:** the inherited command reduces Mach by 0.01 over 23:30–23:32
  UTC and then holds. These are not constant-Mach holds throughout the flight.
  Pressure is constant per recipe; geometric altitude can change.
- **Score:** modified J is the retained observation χ² plus the original MID
  prior. It scores three BTO terms (20:41, 21:41, 00:11) and all five BFO terms.
  Starting longitude is closed with 19:41 BTO. No new 22:41 BTO prediction or use
  in selection occurred; 22:41 BFO remains fitted. Historical anchor selection
  and setup have prior exposure, so this is not a blind holdout.
- **Verification:** all ten selections are eligible on 15, 7.5 and 3.75-second
  meshes and pass both adjacent comparisons. Numerical agreement is not a
  satellite-fit acceptance threshold, an absolute error bound, or a certification
  of the real aircraft. Seven searches hit their per-target/restoration caps;
  none has independently certified stationarity.
- **Fuel window:** engine loss must be within 00:16:29–00:17:59 UTC. Some retained
  cases lie extremely close to its edges. At the finest mesh both Mach 0.840
  selections are less than 0.2 milliseconds inside the late limit. Eligibility
  is as recorded and is not a demonstrated robust fuel reserve.
- **Positions:** map/table locations are supported 00:11 UTC powered states,
  not engine-loss or impact locations. No terminal calculation was performed.

## Starting assumptions and historical ancestry

The experiment starts at 19:41:03 UTC with TASK042's assumed total fuel of
27,856.86569474842 kg, including 6.80388555 kg assigned to the APU, and nonfuel
mass 174,369 kg (initial total mass 202,225.86569474842 kg). Latitude, bearing and
pressure are adjusted, and starting longitude is solved on the BTO locus.
These are prescribed starting assumptions, not quantities established here from
a connected incoming flight.

The saved TASK042 instruction explicitly excludes early-route reconstruction;
the experiment does not establish radar-to-19:41 ancestry or reinstate the
withdrawn connected ancestry of the historical TASK042 starts. The source-text
paths and hashes supporting these assumptions are recorded in
`comparisons.json`. This qualification accompanies, rather than edits, the
original report. This experiment is separate from the LRC pilot and the proposed
high-altitude Mach 0.84 climb experiment.

## Rebuild and check

From the Atlas repository root:

```sh
python3 scripts/build_task042_mach.py
python3 scripts/build_task042_mach.py --check
```

The standard-library-only compiler verifies copied source hashes, compares every
CSV field with the compact extraction, reconciles selected identities and
eligibility across meshes, and formats display strings. It reads only committed
files in this directory; no model installation or original workspace is needed.
`--check` writes nothing. `display.json` and `validation.json` are generated
publication products, not new flight evidence.
