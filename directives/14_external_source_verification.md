# CODEX TASK 14: verify external sources and record them as candidates (no drift runs)

Authorized by Ryan. Register as the next unused DIRECTOR number and write to a new folder `task_14_external_sources/` beside the Task 13 outputs. Preserve all historical code, inputs and outputs. Frozen B0, the Task 13 registry and every existing input table are not edited.

## 0. Purpose and standing

A third-party assistant produced an index of external documents claiming to resolve several Task 13 gaps. Those claims are **unverified** and the index is explicitly not a hash manifest. This task obtains the documents, checks each claim against the actual document, and records what survives as **EXTERNAL_CANDIDATE** rows. It does not promote anything to SOURCED and does not change any model input.

Status vocabulary, used on every output row:

- `EXTERNAL_VERIFIED` — the cited document was obtained, its hash recorded, and the claimed text or value found at or near the cited location.
- `EXTERNAL_MISMATCH` — the document was obtained but the claim is not supported there, or differs. Record what the document actually says.
- `EXTERNAL_UNOBTAINED` — the document could not be obtained. Record why. Do not substitute a mirror, a summary, a news article or recollection.

`SOURCED` remains reserved for the local project files, exactly as in Task 13. No external row may be written into any B0 table, any frozen input, or `confirmed_inputs_v*.csv` by this task.

This task does NOT: run any drift, hindcast, forward or reverse job; re-match anything; fit or tune a parameter; use any MH370 arc, flight path, candidate position or search area to choose among values; or alter the Task 13 registry files.

## 1. Obtaining the documents

For each document in section 2, attempt retrieval in this order and record which was used:

1. A copy Ryan supplies locally.
2. A direct download from the publisher's own domain.
3. An archive copy, recorded as such.

For every obtained file record: URL or local path, retrieval timestamp, byte size, SHA-256, publisher domain, and whether it is publisher-hosted or a third-party or archive copy. If a document cannot be obtained, mark every claim that depends on it `EXTERNAL_UNOBTAINED` and continue. Obtaining nothing is an acceptable outcome.

Do not acquire any other data, and do not start a general literature search.

## 2. Claims to check, one row each

For each, locate the cited page and record the document's actual wording alongside the claim.

### 2.1 Flaperon starting coordinate (item 1)
Claim: Pierre Daniel, Météo-France, *Dérive à rebours de flaperon*, 8 February 2016, page 3 gives a starting location on the shore of Saint-André, Réunion, at 20°56.20′S, 55°40.87′E, with a model start of 29 July 2015 04:00 UTC.
Check: the place name, the degrees-and-minutes values, the date and time, and whether the report presents this as a recovery position or as the starting point of its own reverse-drift model. Record the decimal conversion as a derived value, computed here, not as published precision. Record whether the document states any positional uncertainty. Note the existing conflict with the Malaysian summary's Saint-Denis label; do not resolve it, average it, or discard either.

### 2.2 Item 6 recovery description
Claim: Malaysian Appendix 1.12D, report DB/01/17, records discovery south of Chidenguele, Mozambique on 24 April 2016, and no numerical coordinate.
Check: the location wording, the date, and whether any coordinate or extent appears anywhere in the report. If none appears, record that explicitly: it means a town-centre coordinate stays an assumption.

### 2.3 CSIRO forcing products and the meaning of 1.2%
Claim: Griffin, Oke and Jones, *The search for MH370 and ocean surface drift*, 8 December 2016, section 2.4, printed pages 9 to 11, identifies ERA-Interim 10 m winds, BRAN2015 currents and Stokes drift from a CAWCR Wave Hindcast extension, and defines 1.2% as the value minimising unexplained drifter velocities.
Claude has already checked this one against the ATSB-hosted PDF and found section 2.4 to state those three products, and the 1.2% defined through its equation 2.4.2 as the value minimising the unexplained drifter velocities. **Verify independently and record the exact sentence and equation number.** Record whether the report characterises the coefficient as predominantly wave-driven Stokes drift carried through a wind proxy, or only as a fitted effective windage; this distinction matters and must not be filled in from the third-party summary.
Then record, as a separate derived row: B0 applies a 1.2% floor with daily NCEP/NCAR R1 T62 winds and GLORYS12V1 currents, which are not the products the coefficient was fitted with, and no transfer validation exists in the project files.

### 2.4 Earlier observation of item 4 ("Roy")
Claim: the same CSIRO report records Roy as first seen at Mossel Bay on 23 December 2015, while the Malaysian catalogue gives a discovery date of 22 March 2016.
Claude found a figure caption stating the 23 December 2015 first sighting. **Verify independently**, record the figure number and page, and record the Malaysian date from the catalogue.
Then record, as a separate derived row, what this does and does not support: a first sighting establishes presence by that date. It does not establish a landing date, continuous residence, or any general detection-delay distribution. Compute and record the interval between the two dates. Record B0's current window for item 4 and flag it `WINDOW_MAY_BE_MISDATED`. **Do not change the window.** Any rerun with an altered window is a separate task requiring Ryan's decision.

### 2.5 French DGA coefficients
Claim: B. Pengam, DGA Techniques hydrodynamiques, report 16-500560, 1 April 2016, embedded in the flaperon appendices PDF, gives 3.29% with 18° left deflection for trailing-edge-to-wind and 2.76% with 32° left for leading-edge-to-wind, as numerical-model results.
Check: the values, the angles, the orientation each belongs to, and above all whether the report presents them as computed or as measured. Record the evidence type the original document states. If the document is in French, record the original wording with a translation marked as such.

### 2.6 Nesterov provenance disagreement
Claim: Nesterov, *Ocean Science* 2018, section 2.2, describes the French parameters as experimentally established, while the original DGA report identifies them as numerical; Nesterov's own forcing is HYCOM GLBa0.08 currents and NOAA ARL GDAS1 winds at 1° and three-hourly.
Check: the characterisation, the forcing products and their stated resolution. Record the disagreement with the original report as a `CONFLICT` row, with both source locations, and leave it unresolved.

### 2.7 CSIRO Part II directional evidence
Claim: *Part II*, 13 April 2017, section 2.3 and Figure 2.3.1, printed pages 10 to 11, reports a mean flaperon deflection near 16° left relative to an undrogued-buoy reference, evaluates 10° and 20° modelling angles, and adds roughly 0.1 m/s above the 1.2% reference relationship.
Check: the values and what object each applies to (genuine cut-down flaperon, replica, or drifter). Record explicitly that a mean deflection is not a divergence width, and that nothing here supplies parameters for fragments other than the object tested.

### 2.8 Items 28 to 32 window provenance
Claim: Debris Examination Report DB/01/18, 30 December 2018, states the pieces were handed over on 30 November 2018 but found between late 2016 and late 2017, except item 30 in August 2018.
Check: the wording and whether any more specific recovery date exists for any of the five. Record that the handover date is not a discovery or landing date. Do not narrow any window.

### 2.9 Item 1 locality corroboration
Claim: contemporary Reuters photograph captions dated 29 July 2015 credit the recovery to Saint-André.
Check only whether the captions say that. Record it as press corroboration of locality, never as a coordinate or as positional accuracy.

## 3. Deliverables (CSV, Markdown, JSON; no Excel formats)

- `external_documents.csv`: one row per document — id, title, publisher, date, retrieval route, URL or path, retrieval timestamp, bytes, SHA-256, publisher-hosted or archive, obtained yes/no, failure reason.
- `external_claims.csv`: one row per claim in section 2 — claim id, section, item ids affected, claim as stated, document id, cited locator, locator confirmed yes/no, document's actual wording, extracted value, units, evidence type (measured / computed / reported / descriptive), status from section 0, note.
- `external_candidates.csv`: only `EXTERNAL_VERIFIED` rows that correspond to a field on the Task 13 confirmation sheet, in the sheet's own column shape, with `ryan_value` **left blank** and the proposed value in a separate `external_proposed_value` column. Ryan fills `ryan_value` himself or does not. This file is an input to his decision, not a confirmation.
- `conflicts.csv`: Saint-André versus Saint-Denis, the Nesterov versus DGA evidence type, item 4's two dates, and any new disagreement found. Both sides, both locators, unresolved.
- `derived_notes.md`: the separate derived rows called for in 2.3 and 2.4, plus the coefficient-transfer note, each labelled as Codex's or Claude's inference rather than a document statement.
- `NOTES.md`: assumptions, what could not be obtained and why, file hashes, runtime, and an audit trail linking every row to a document and locator.

## 4. Verification

- Every `EXTERNAL_VERIFIED` row must carry a document id whose hash is in `external_documents.csv`, and a locator that was actually opened.
- Confirm no Task 13 file, B0 table or frozen input changed, by hash comparison against the Task 13 manifest. Report the count checked.
- Confirm `external_candidates.csv` has `ryan_value` blank in every row.
- Report counts by status, and the count of claims that could not be checked.

## 5. Stop rule

Deliver the three CSVs, the conflicts file and the notes, then stop. No drift run, no rematching, no window change for item 4 or any other item, no change to the 1.2% floor or any class value, no automatic follow-on. Write "external verification complete; nothing promoted" when done. If most documents could not be obtained, say so plainly rather than filling the gap from the third-party summary.

## 6. Notes from Claude (not instructions)

- The third-party index is a navigation aid. Its own text says it does not certify publisher authenticity of mirrors, so a claim is only as good as the document you actually open.
- The two claims that could change the analysis are 2.3 and 2.4. The first says the 1.2% was fitted to a different forcing set than B0 uses, which bears on the documented eastward hindcast bias. The second says item 4's matching window may be about 90 days late.
- Saint-André versus Saint-Denis is roughly 20 to 25 km. Both sit inside the 100 km primary matching radius, so recording the conflict is enough; it does not change matching.
- A verified external value is still not a measurement of what B0 needs. The DGA coefficients are for a flaperon, computed numerically, and say nothing about the other 31 items.
