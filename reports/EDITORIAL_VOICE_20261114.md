# Public wording revision, 14 November 2026

Base: `68a10274afa352e9cd1b517efabaea8204c8fb04`.

Ryan Hall requested a wording pass across the website to remove assistant self-reference and chat-thread narration, especially when describing predictions.

## Changes

- Replaced first-person assistant narration with descriptions of the experiment, assumption, calculation, review or correction.
- Retained expectations recorded before experiments, including predictions contradicted by the results, in neutral language.
- Revised conversational headings, figure captions and map labels in the canonical data, methods, drift and historical flight pages.
- Restated the historical AI assessment in the third person, retaining its attribution, dated scope, superseded conclusions and subjective-estimate qualifications. Added a pinned link to the original attributed text.
- Preserved Ryan Hall's signed assessment without alteration. References identifying the origin of AI-generated data remain where they explain provenance.
- Updated the source bodies and generator alongside the published HTML.

The scientific reinterpretations in `DRIFT_EDITS_HELD_20261112.patch` were not applied. This author-requested wording pass does not resolve or replace that separate held proposal. Historical directives and original downloadable evidence were not rewritten.

## Verification

- The generator reproduced all 19 generated pages at the base commit exactly before the edit.
- After the edit, all 20 public HTML pages were compared with the base. Fifteen changed; all 7,148 displayed numerical tokens, including 3,584 within table cells, remained identical and in the same order.
- Every existing link, page ID and embedded asset reference was preserved. The historical AI assessment has one additional source link to its original text.
- The 114 checked protected files were byte-identical to the base: the signed assessment, scientific datasets, figures, forcing fields, Flight Lab files, shared styles and scripts, and the standalone display scripts.
- The existing local-link check passed: 197 local file links checked, none missing.
- `git diff --check` passed.

These are editorial and preservation checks. No scientific calculation, flight integration, fit, catalogue import or production-run modification was performed.
