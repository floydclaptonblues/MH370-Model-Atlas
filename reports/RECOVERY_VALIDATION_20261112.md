# Atlas recovery validation, 12 November 2026

Baseline: `e79b34ea61f207ab8eb86101bdc314a5788579c9`.

The original conversation stopped during preparation of an upload. Remote `main` still contained the initial Lab integration. The interrupted workspace's patches were unavailable, so these repairs were reconstructed from the owner's supplied handoff and checked anew. No claim is made that the prior workspace's sixteen reported checks were recovered.

## Integrated checks

- `python3 gen.py`: completed. A second build produced identical bytes for every generated root HTML page.
- `python3 tests/check_preservation.py`: passed. All 1,845 numeric-containing table cells retained the same numerical token sequence. The signed assessment, Lab dataset and protected Arc 7 source assets remained byte-identical to the baseline.
- `python3 tests/check_editorial_preservation.py`: passed. All 3,039 numerical tokens in root-page tables stayed in their original page/order; editorial scope assertions passed.
- `python3 tests/check_local_links.py`: passed. All 184 static local file references in root HTML resolved. This checks file existence, not external URLs or fragment behavior.
- `node tests/flight_lab_dom.cjs`: 25 DOM/controller checks passed with jsdom 31.0.0, a stubbed canvas renderer and controlled timers. These exercise checkpoint/state synchronization, slider identity, timer interruption, response identity, missing data and the force display's generated scene geometry.
- JavaScript syntax checks passed for the shared shell, Lab controller/scene scripts and all twenty inline script blocks in generated root pages. Added disclosure-wrapper tags are balanced. Python source compilation and `git diff --check` passed.
- The rebuilt offline ZIP passed CRC integrity checking; its controller and dataset match the corrected online controller and preserved dataset.

## Verification limit

Desktop/mobile browser rendering and real canvas interactions remain unverified in this recovery. Chromium startup failed because the execution environment disallowed its required process socket; the browser test did not reach the page. The DOM checks are not a substitute for pixel or real-browser validation. No old screenshot is presented as a view of these repairs.

## Scientific boundary

No model was run. No observations, trajectories, catalogue dataset, numeric result tables, scientific acceptance thresholds or signed assessment were changed. The independent 22:41 holdout was not evaluated. Current-method wording was checked against the pinned campaign directive, observation-role contract and catalogue definition linked on the Methods page. Old methods remain explicitly dated archival material, not newly validated scientific claims.

Publication is a separate step. This report documents local validation, not a successful deployment.
