# Flight Dynamics Lab — Atlas section

Public route: `flight-lab.html`. Navigation and the homepage's Scientific tools section link to it.

The opening view is the completed **108-arrival cruise-level run**, published 16 November 2026. A catalogue switch retains the earlier terminal viewer as a separate dated snapshot. The Atlas edition uses the shared scientific-console shell and scoped Windows 98 stylesheets. Neither view computes a flight.

## Completed cruise catalogue, 16 November 2026

The current explorer reads `../data/cruise-production-108/catalogue.js`, compiled from the committed source tables at `24655869cf3fe2452615157cf59c1ed3f28c3677`, runner revision `2a016b1294fa`. The source files, exact hashes, JSON export and display-validation record are kept beside that asset.

The explorer covers all 108 arrivals, 424 configurations and 848 completed one-sided searches. It exposes 266 distinct accepted flights, their 267 directional solution records, the separate endings of both searches, the three recorded measurement-time checkpoints, total fuel and engine fuel above the model's 6.80388555 kg APU reserve, and the recorded fuel-exhaustion event or powered-at-00:40 status. Exact-command duplicates are linked; nearby flights remain separate. Numerical-check labels refer to the particular flight repeated, and range-end flags remain attached.

Filters select the starting group, incoming-level control or climbed level, search outcome and individual arrival. The configuration list and returned-flight selector provide access to every record. The latitude/longitude plot shows saved 00:11 airborne positions only, with different shapes as well as colours for the three Mach values. Overlapping markers offer a record chooser. No trajectory joins or probability contours are drawn.

Acceptance in this run concerns the three later timing bands, performance support and engine fuel at 00:11. Its terminal package has not yet run; earlier terminal results are not transferred to these flights. The page states the bounded-search scope, diagnostic role of later frequency residuals, numerical-check limits and satellite-input sensitivity.

`assets/cruise-production.js` and `assets/cruise-production.css` provide the new display. `src/flight_lab_body.html` holds its markup. The historical `assets/data.js`, `assets/app.js` and `assets/scene3d.js` remain unchanged. The shared shell receives `atlas:catalogue` when the user switches between current and earlier catalogues, so its displayed counts have the same scope.

Source CSVs and the compiled JSON can be downloaded from the current view. The existing standalone ZIP remains the **earlier 12 November viewer**; it does not include this new cruise catalogue. Future offline rebuilds extract only the body between `LEGACY_CATALOGUE_START` and `LEGACY_CATALOGUE_END`.

Focused new display checks: `node tests/cruise_production_lab.cjs`. They exercise real filtering and selection against the imported catalogue, fuel/reserve and check identity, range-end labels, the overlap chooser, the catalogue switch and source preservation. These are interface checks, not scientific revalidation.

## Earlier terminal catalogue: sources and scope

The retained historical view is the Atlas presentation of the standalone Flight Dynamics Lab, originally frozen at `33a90b300657bf0a11005bab885fec055ed56df6`.

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

## Plain-language readouts, 15 November 2026

The opening view now follows the existing seven-checkpoint example. A readout above the diagram explains the selected position, compass direction, ground speed, vertical motion, fuel and engine phase. A saved-time selector changes the same record as the slider, map and detailed inspector. Height uses the exported height above the model surface when available, otherwise the labelled ellipsoid reference. Familiar units are display conversions; “height nearly steady” means the saved vertical speed has magnitude below 0.1 m/s, without changing any model classification.

Changes since the previous checkpoint compare saved endpoints only. The readout does not interpolate motion or estimate remaining flight time. Ordinary one-position summaries and final-position cloud records retain their missing-motion labels; another response cannot inherit the example's fields.

Force descriptions explain lift, drag, approximate weight and the separate velocity arrow. Recorded bank remains distinct from commanded bank; no unverified left/right convention or nose attitude is inferred. The wind illustration has its own dynamic readout and changes no saved flight. Technical values and source records remain available, while the general model tutorial is collapsed initially. The frozen catalogue is explicitly separate from the 108-arrival cruise-level study and current working-area assessment.

The focused display regression is `node tests/flight_lab_readouts.cjs`, in addition to the controller and renderer checks below. None of these checks performs a flight calculation. `build_offline.py` also copies the shared page sections into the standalone download and verifies preservation of its scientific data and provenance.

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
