# Flight Dynamics Lab — Atlas section

Public route: `flight-lab.html`. Navigation and the homepage's Scientific tools section link to it.

This is the Atlas presentation of the standalone Flight Dynamics Lab, originally frozen at `33a90b300657bf0a11005bab885fec055ed56df6`. The Atlas edition uses the shared scientific-console shell and a scoped Windows 98 stylesheet. It carries the same safe compiled dataset without changing a scientific value.

## Sources and scope

- Catalogue commit: `de50a5206e940fcb34acf587f98e849f9f4e98b5`.
- Scientific export baseline: `31b6b16ef4ddcc8cad153b56ae2e380f838046dd`.
- `assets/data.js` SHA-256: `652729047a556b5bee46363f5aa6bc296466c5eaffcd20d5f7c1f1fb3ef28b7e`.
- Counts: 5,750 declared configurations, 22 arrival histories, 278 returned-flight summaries, 3,171 retained final-transmission states, and one seven-checkpoint worked example.
- The source manifest and original dataset validation report are retained beside this note. Sources are pinned public exports, not raw mixed records.
- The 22:41 observation and withheld numerical predictions are absent. The lower-speed experiment is not imported into this frozen snapshot.

No propagation, fitting, performance-model change, impact calculation, breakup calculation or debris-drift calculation is performed by the viewer. Uncomputed cells remain uncomputed. Recorded values, schematic connectors, reference-gravity weight and illustrative wind controls are labelled separately. Record counts are not probabilities.

## Maintenance

The page body lives in `src/flight_lab_body.html`. `gen.py` declares `FLIGHT_LAB_HEAD` and the corresponding `pages["flight-lab.html"]` route. It loads `common.css`, the scoped `assets/win98.css`, `common.js`, and the three local data/scene/controller scripts. Do not load the standalone viewer's global stylesheet into the Atlas.

The download is explicitly labelled **Standalone offline viewer**. It contains the original standalone layout, safe source exports, compiler, provenance and validation; it does not require the Atlas navigation to function offline.

The viewer's internal state controls operate only on the retained data or the separate vector-addition teaching example. They do not create accepted flights.

## Playback repair, 12 November 2026

The controller keeps configuration, parent flight and terminal response identities separate. Opening a different response on the worked example's parent shows only the exported parent summary; it does not substitute the example's seven-checkpoint terminal trajectory. A selection without a returned flight displays an explicit unavailable state.

Manual checkpoint selection stops the slideshow. Slider input preserves its DOM control, while the scene marker, UTC, fuel cursor and variables update together. The 1.7-second slideshow interval is presentation time, not model time. Actual elapsed time between checkpoints is displayed separately. Missing measurements remain missing; algebraically derived summary mass is labelled.

`playback_repair_validation.json` records fresh DOM/controller checks, including source-value and force-vector checks. These are not flight simulations or scientific revalidation. Chromium launch was blocked in the recovery environment and the separate browser could not reach the local preview, so this record does not claim renewed desktop/mobile pixel QA.

Reproduce controller checks with `npm install --prefix tests` then `node tests/flight_lab_dom.cjs` from the repository root. For actual browser checks, serve the repository locally on port 8765 and run `node tests/flight_lab_regression.cjs` with Playwright and Chromium installed.
