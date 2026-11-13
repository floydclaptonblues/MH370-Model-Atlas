# Flight Lab playback selection and terminal scale repair

**Date:** 12 November 2026, America/Chicago.  
**Atlas base:** `8f22c4912d2367acec37bc2b3ac28cfe125e69dd`.  
**Scope:** display, selection, navigation and offline packaging; no scientific calculation or data import.

## Problems addressed

The main Forces tab previously maintained a separate terminal index and could display 00:19:37 while the route inspector showed 00:19:29. It could also replace an unrelated selected flight with the worked example. Grid entry and guided entry did not consistently load the same supplement. On the regional overview, the final saved points occupied nearly the same pixels, while the old hit-test tie tolerance could choose the wrong timestamp.

The presentation also gave widely unequal saved intervals the same slideshow duration without a sufficiently clear separation between presentation time and model time. Long straight spatial connectors implied a path through unrecorded intervals. The terminal bank command could be read as the recorded bank at the first final transmission.

## Resulting behavior

- Route and recorded Forces share flight, response and checkpoint selection. Unsupported force records remain explicitly unavailable, with deliberate load buttons for the two available example records.
- Return navigation keeps the selected flight, response, time and route extent.
- Grid, dropdown and guided entry select the same exact seven-checkpoint example. Another terminal response on that parent cannot inherit the example's trajectory.
- Full route shows numbered saved positions without spatial path connectors. It preserves the visible height-exaggeration control.
- Terminal close-up displays three retained records in a fixed local tangent frame. All axes use 250 m per scene unit and 1× height. The floor is labelled as an 8,000 m ellipsoid-height reference plane.
- The terminal height chart uses real elapsed-time spacing, fixed axes, unjoined points and a cursor tied to the selected checkpoint. The saved final pair is 8,773.955 m at 00:19:29 and 8,314.906 m at 00:19:37: a 459.049 m decrease over eight seconds. This is an endpoint difference, not a new integrated descent.
- Numbered checkpoint cards show actual gaps. The slideshow states its 1.7-second presentation duration per record. Manual selection and view/scope changes stop playback.
- Ambiguous marker clicks open a timestamp chooser instead of silently resolving by depth. Duplicate overlays for one record are not counted as distinct candidates.
- Commanded bank and recorded bank are separate. At 00:19:29 they display −60.0° and −58.32°, respectively.
- Cache versions are updated for the changed controller, renderer and scoped stylesheet. The standalone ZIP receives matching application and renderer code, plus supplemental styles for the new controls.

## Verification

### Automated controller and display geometry

The two focused Node suites passed **54 checks**: 46 in `tests/flight_lab_dom.cjs` and eight in `tests/flight_lab_renderer.cjs`. The harness executes the production scene renderer's projection, traversal, hit-region generation and pointer handling. Only Canvas2D rasterization, interval delivery and animation-frame scheduling are substituted.

Coverage includes all seven source-record selections; main-tab and inspector-button force entry; 00:19:29 identity and force values; unavailable force states; faithful return navigation; consistent example entry; another response on the same parent; missing data; derived mass; orphan and uncomputed selections; stable slider controls; timer cancellation; actual overview overlap selection; terminal framing; height-chart spacing and cursor; and removal of spatial path connectors.

At the reviewed 768 × 480 CSS-pixel canvas, the terminal close-up's final-transmission markers are **41.099 pixels apart**. All three saved terminal markers are inside the frame. These are display-geometry measurements, not scientific-model validation.

### Direct browser checks

Chromium was operated through the browser interface against the generated Atlas page in the managed local preview. The following were observed directly:

- The guided example exposes seven numbered checkpoints and their unequal intervals.
- Selecting 00:19:29 and then the main Forces tab preserves that UTC and exact response; the inspector shows the recorded bank separately from the command.
- Returning preserves 00:19:29. Terminal close-up presents the three records and the fixed-axis height plot with the endpoint-derived decrease.
- Selecting the A00 one-state summary and opening Forces displays unavailable data without substituting the worked example. Return navigation preserves A00.
- At a 390 px iframe width (375 px content width after the scrollbar), terminal cards, the chart and the Forces view fit without horizontal document overflow. The cards and force-return controls work at that width.

The extracted standalone ZIP was also loaded in Chromium through the preview server: its new controls and chart are styled, and its main Forces tab preserves 00:19:29. This checks the packaged files as served, not a separate `file:` protocol run.

The phone-width check is a responsive-layout check in desktop Chromium. It does not claim physical-device, touch or cross-browser testing. The optional shell Playwright suite was updated and syntax checked but was not executed in this environment.

### Preservation and packaging

The compiled scientific data retains SHA-256 `652729047a556b5bee46363f5aa6bc296466c5eaffcd20d5f7c1f1fb3ef28b7e`. The original source manifest and scientific validation files remain unchanged. The offline builder verifies data, safe-export, compiler and provenance byte identity against the existing archive, and verifies the packaged controller and renderer against the worktree.

ZIP integrity passed, all 14 protected package members remained byte-identical, and the packaged application and renderer matched the worktree. The repository link check found 189 local file links and no missing targets. JavaScript syntax and whitespace checks passed.

Only Flight Lab presentation, its generated asset URLs, tests, packaging and maintenance records are in this repair. Homepage, signed assessment, scientific records and drift pages are outside its edits. Existing lower-speed results remain outside the Lab's frozen `de50a52` catalogue. No 22:41 record, raw mixed record, withheld prediction, aircraft integration, fitting, impact or drift calculation was used.

## Practical limit

This remains a saved-checkpoint viewer. It now presents selection and terminal motion evidence faithfully, but it cannot provide continuous replay from an export containing only seven example checkpoints. The full-duration fuel chart retains its real time scale, so final-second cursor movements there remain small; the terminal height chart provides the separate detailed view.
