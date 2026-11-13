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

Browser checks were subsequently run in Chromium on desktop and phone-size viewports before publication; see `reports/CLAUDE_VERIFICATION_20261112.md`. The mass label distinguishes recorded from algebraically derived values.

## Playback selection and terminal scale update, 12 November 2026

The route and recorded Forces views now share the selected flight, exact response and checkpoint. The main Forces tab preserves 00:19:29 when that record is selected. If force fields were not exported for the current record, the viewer keeps its identity visible and offers explicitly labelled buttons to load either available worked-example force record. Returning to the saved flight preserves the original selection and route scale.

The worked example is the same seven-checkpoint supplement whether opened from the grid, dropdown or guided example. A different response on its parent stays a parent-only summary. The bank command and instantaneous recorded bank have separate labels.

Full route displays numbered saved positions without joining unknown intervals. Terminal close-up displays the fuel event and both final transmissions at a fixed local scale, with 1× height and a labelled 8,000 m ellipsoid-height reference plane. A separate height plot uses the actual elapsed times, fixed axes and unjoined saved points. Its 459.049 m decrease over eight seconds is derived only from the two retained transmission endpoints.

Numbered cards expose the unequal time gaps. The control is explicitly a checkpoint slideshow at 1.7 presentation seconds per record; it does not synthesize continuous motion. Overlapping canvas markers offer a timestamp chooser. Manual selection stops the timer.

`playback_context_validation.json` and `../reports/FLIGHT_LAB_PLAYBACK_REPAIR_20261112.md` record this update's checks separately from the earlier reports: 46 controller/production-renderer geometry checks, eight pointer checks, and direct Chromium checks of desktop and phone-width layouts. The optional shell Playwright suite was not executed for this update.

Run the focused checks using the commands in `../tests/README.md`. To rebuild the existing standalone download after editing the viewer, run `python3 flight-lab/build_offline.py`; it copies the controller and renderer, adds styles for the new controls, and verifies that the packaged data, safe exports, compiler and scientific provenance remain byte-identical.
