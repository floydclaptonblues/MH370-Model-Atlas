# Archive of Attempts — inventory draft (for review)

Draft for the Atlas restructure, 10 November 2026. **Nothing here is published yet.** Each entry records what the
work was, where its final record sits, its disposition, the reason in ordinary language, and what replaced it.
Dispositions follow four outcomes, plus a review flag where the evidence does not settle it:

- **Negated under stated conditions** — a validly executed test rejected the tested scenario under its stated
  assumptions. The test and result are identified. (Negation is a result, not a failure.)
- **Operationally abandoned** — work stopped for a practical reason (compute, data access, architecture). Its
  scientific question may remain open.
- **Superseded** — a later method, dataset or run replaced it. Supersession alone does not make the earlier
  result wrong.
- **Invalidated / withdrawn** — an identified defect made particular outputs unreliable. The defect and the
  affected conclusions are stated.
- **UNDER REVIEW** — disposition not yet settled by the record, or the record sits outside these repositories
  and its identifier still needs to be supplied.

Per the investigator's instruction: the drift pages (`drift.html`–`drift4.html`, `currents.html`) are **not**
consolidated or edited by this restructure. Their entries below are listed for completeness only, pending his
own review.

---

## A. Satellite and flight chapter (closed 6 Oct 2026; corrections recorded 23 Oct 2026)

### A1. The assumed 19:41 start state — the chapter's foundation
- **Record:** TASK_051, `run2/task051_post_radar_feasibility_001` (TASK042 repository); `CORRECTION_AUDIT_20261023.md` §2.
- **Disposition:** Invalidated as a supported quantity; superseded as a foundation.
- **Reason:** two reconstructed ancestries flown forward from the continuously integrated radar handoff both
  stopped near 18:27 against a thrust barrier (shortfalls under 1%); neither reached 19:41. The 19:41 fuel load
  was therefore carried from historical context, not derived from a connected flight, and every "fuel-limited"
  statement measured against it inherits that qualification.
- **Replaced by:** the connected six-history chain starting at the retained 18:22:12 handoff (flight-histories
  dossier, archive SHA-256 `3d3e5c3e…eb8fe0ed`; audit at `MH370-Ocean-GLORYS-Data` commit `f7939be`), in which
  fuel, mass and clock are integrated continuously from the handoff to the terminal branches.

### A2. Cruise-fit χ² results, including C120 (χ² = 8.117, "0.1 kg fuel margin")
- **Record:** `CORRECTION_AUDIT_20261023.md` §1 and page-correction (a); `directives/15a_solver_termination.md`
  (ocean repository).
- **Disposition:** Invalidated / withdrawn as fit claims.
- **Reason:** twelve qualification assessments returned zero qualified fits; the optimiser reported success at
  points with objective gradients 3.5–11.0 and empty active-constraint sets. No χ² on the Atlas describes a
  verified minimum, and the 0.1 kg margin is measured against the unsupported 19:41 fuel load (A1).
- **Replaced by:** the enumerated response-family approach of the terminal campaign (populations, not point
  fits), and the documented resolution limit of the frozen satellite model.

### A3. "Endpoint latitude is constrained by the handshake sequence" (35.85–36.85°S)
- **Record:** `CORRECTION_AUDIT_20261023.md` page-correction (b); `closing.html` (already struck through).
- **Disposition:** Withdrawn as a constraint claim.
- **Reason:** the spread of seven unqualified returns from one narrow search family, each propagated from the
  assumed 19:41 state, was presented as a constraint imposed by the handshake sequence. It is a description of
  where one family's returns landed.

### A4. North-vs-south χ² margin 16.84 against 7.92
- **Record:** `CORRECTION_AUDIT_20261023.md` page-correction (c); `README.md` "Where the evidence stands";
  `northsouth.html`.
- **Disposition:** Withdrawn (the margin). The north–south question itself remains **open and presented as open**.
- **Reason:** an optimiser gradient defect (corrected 22–24 Oct) collapsed the scores to 4.840 against 4.821,
  and the two candidates become indistinguishable under a common frequency offset of +5.692 Hz — 0.81σ of a
  single nuisance parameter. Neither point passed the stationarity test.

### A5. Northern commanded flights reaching 23.9–26.4°S
- **Record:** `README.md` / `closing.html` (standing result).
- **Disposition:** Negated under stated conditions. **Stays a result** (moves to the archive's "negated" shelf
  only if the chapter page is retired; the negation itself remains current).
- **Reason:** they miss every handshake ring by 108–127 km (24.8–29.2σ) and are still under power at 00:25,
  incompatible with the 00:19 log-on.

### A6. The long glide G0/S14
- **Record:** `closing.html` (standing result).
- **Disposition:** Negated under stated conditions; stays a result.
- **Reason:** reaches the water 168 km beyond the published 7th arc, wings level at 196 kt, and misses the final
  frequency pair by +34.2 Hz and −121.4 Hz; no vertical-compensation fraction in [0, 1] makes a glide compatible.

### A7. Phase 4B / Phase 5A candidate set (96 candidates)
- **Record:** `CORRECTION_AUDIT_20261023.md` §3 (verified against the recovered archive, 21 Oct).
- **Disposition:** Superseded; the absolute-fit implication withdrawn.
- **Reason:** the 12.7× tier ranking reproduces, but no candidate passes even the final 00:19:29 timing
  observation at 3σ (smallest residual 312.8 µs against a 186 µs band). The score is a deterministic
  compatibility index, not a posterior; any reading of the winner as "fitting the data" was an overstatement.
- **Replaced by:** the terminal campaign's compatible-response populations.

### A8. mbce_mh370_v06/v07 engine and the pre-repair northern basins
- **Record:** outside these repositories — **identifier to be supplied** (UNDER REVIEW).
- **Disposition:** outputs before the path-epoch repair: Invalidated. The engine line: Superseded.
- **Reason:** the scorer evaluated pre-anchor BTO observations (16:42, 16:55, 17:07) by back-propagating the
  post-anchor first-leg azimuth, forcing one parameter to span two flight epochs; this manufactured
  high-scoring northern-hemisphere basins. After the repair (and its twin in the BFO channel) the instrument
  independently converged near 34.54°S / 93.23°E with no mask, drift term or route prior — treated as validation
  of the instrument, not a located aircraft, since that area has been searched.

### A9. Domain Algorithm V1 (S00–S110 gated pipeline), stopped at S50
- **Record:** outside these repositories — identifier to be supplied (UNDER REVIEW).
- **Disposition:** Operationally abandoned.
- **Reason:** the architecture demanded source checks for derived quantities and hashed whole records, locking
  the machine for days before hanging on a source-connection detail. Its blocker and eligibility lists are a
  dead branch's record, not live constraints. The scientific questions moved to later work; none were settled
  by the abandonment.

### A10. The Average Day Model (commanded-flight RK4 reference)
- **Record:** frozen Sep–Oct 2026 as read-only input; presented on `flight.html`.
- **Disposition:** Superseded as a live model; **retained** as the reference flight and as the documented
  resolution-limit result. Not an archive-only item.

### A11. Early task line on `flight.html` (TASK_021 / TASK_022 / TASK_026 / TASK_029)
- TASK_021 solver fits: carry the A2 qualification (no verified minima). UNDER REVIEW whether the page keeps
  them as history or they move wholly to the archive.
- TASK_022 terminal experiment (72 continuations; arrival Mach 0.35–1.34; no supersonic arrival required):
  standing result, kept with its conditions.
- TASK_026 convention sweep: produced the retained BFO convention (zero vertical speed) — **current convention**,
  belongs in Methods, not the archive.
- TASK_029 / directive `17a_latitude_reachability_v1`: Superseded by `17b` (so labelled in the record).
- Directive `18b_addendum_survivor_handoff`: Withdrawn (so labelled in the record).

## B. Terminal campaign and dossier (current — the Atlas's new lead; not archive)

Six connected incoming histories from 18:22:12; 98 baseline response identities; 128 displayed Mach-0.89
records (98 baseline + 24 exploratory command alternatives + 6 reproduction controls); 424 registered
continuation candidates; 68 floor-ending branches reported at the **terminal reporting endpoint** convention
(last propagated state at the lowest weather level, original event labels and heights attached); 332 stops at
the model-support boundary — which does **not** by itself negate the underlying flight hypothesis; 24
alternatives not continued by design. Records: `MH370-Ocean-GLORYS-Data` terminal directories (catalogue at
`95d1b5a`), the dossier archive (SHA-256 above) and its independent audit (`f7939be`). The published envelope
covers exactly these histories, response families and tests — it is not a claim that every mathematically
possible BTO/BFO-compatible flight has been enumerated.

## C. Drift chapter — pages kept as-is pending the investigator's review

Entries listed for completeness; **no disposition assigned by this draft**: Tasks 7–9 (`drift.html`), drifter
hindcast / forward release grid / permutation null / B1 stop / provenance audit (`drift2.html`), forward
transport (`drift3.html`), four-year transport (`drift4.html`), currents reference (`currents.html`). The
standing conclusion — no determinable source region; the answer moves 1,000–1,900 km under an unmeasured
assumption — is a current result, not an archive item. **Open work item:** the Canonical Data page must name
the same ocean-forcing product and version as the drift pages (Copernicus/GLORYS12V1 archive, 2014–2018, plus
NCEP/NCAR 10 m winds); any mismatch gets flagged, not silently edited.

## D. Proposed locations (neither catalogue results nor archive)

- **32.355°S, 97.4°E** — *Proposed location; originating run and evaluation status awaiting verification.*
  Point marker only; no footprint drawn (the "±100 km diameter" phrase does not establish a radius). Two
  frozen-method experiments (target-conditioned feasibility; location-unconstrained reconstruction) are planned
  on the execution machine; the Atlas does not change until their results are reviewed.
- **31.4°S, 90.4°E** (early multi-domain convergence proposal) and the **28–30°S / 97–100°E** fuel-burn/drift
  hypothesis and the **Java hotspot**: UNDER REVIEW — list with provenance or leave off; records to be supplied.

---

*Prepared from the committed records named above. Entries marked UNDER REVIEW need either an identifier or a
decision from the investigator before publication.*
