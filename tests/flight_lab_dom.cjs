// User-flow regressions against the real app and Scene3D projection/hit-testing.
// This is a jsdom harness, not browser pixel QA or aircraft-model validation.
const assert = require('node:assert/strict');
const { createHarness } = require('./flight_lab_harness.cjs');
const h = createHarness(), { $, $$, click, input, tick, state, w } = h;
const D = w.MH370_DATA, tests = [], measurements = {};
const check = (name, fn) => { fn(); tests.push(name); };
const short = id => id.replace(/^FPC\|/, '');
const formatted = (n, dp) => n.toLocaleString('en-US', { minimumFractionDigits: dp, maximumFractionDigits: dp });
const selection = () => ({ flight: state().flight, response: state().routeResponseId, checkpoint: state().checkpoint });
const missingForces = () => /not (?:available|retained|exported)|unavailable|no (?:recorded )?force/i.test($('#inspector').textContent);
const checkpointMarker = index => h.scene.scene.points.find(p => p.id === 'checkpoint:' + index);
const checkpointHit = index => h.scene.hitRegions.find(p => p.item.id === 'checkpoint:' + index);
const noSpatialConnections = () => {
  const points = h.scene.scene.points.filter(p => /^checkpoint:/.test(p.id || '')).map(p => p.p);
  const equals = (a, b) => a.length === b.length && a.every((v, i) => v === b[i]);
  assert(!h.scene.scene.lines.some(l => points.some(p => equals(p, l.a)) && points.some(p => equals(p, l.b))));
};
const firstTransmission = D.witness.states[5], finalTransmission = D.witness.states[6];
const alternate = D.flights.find(f => short(f.id) === 'A00_M0.6550_CS00000.000#R0');
assert(alternate, 'the reviewed alternative flight exists in the frozen export');

try {
  click('#guided-example');
  check('Worked example explicitly selects its exact response and seven checkpoints', () => {
    assert.equal(state().routeResponseId, D.witness.responseId);
    assert.equal(+$('#time-slider').max, 6);
    assert($('#inspector').textContent.includes(short(D.witness.responseId)));
  });

  for (let i = 0; i < 7; i++) {
    input('#time-slider', i);
    const st = D.witness.states[i], text = $('#inspector').textContent;
    check('Source record, UTC, fuel cursor and actual scene agree at checkpoint ' + i, () => {
      assert.equal(state().checkpoint, i);
      assert.equal($('[data-checkpoint-utc]').dataset.checkpointUtc, st.epoch);
      assert.equal(+$('[data-fuel-cursor]').dataset.fuelCursor, i);
      assert.equal(h.scene.scene.points.find(p => p.size === 6).id, 'checkpoint:' + i);
      [st.massKg / 1000, st.fuelKg, Math.abs(st.lat), Math.abs(st.lon)].forEach((value, k) => {
        assert(text.includes(formatted(value, [2, 1, 4, 4][k])));
      });
    });
  }

  input('#time-slider', 5);
  check('Commanded bank and instantaneous recorded bank are labelled separately', () => {
    const text = $('#inspector').textContent.replace(/−/g, '-');
    assert(/Commanded bank/.test(text));
    assert(/Recorded bank/.test(text));
    assert(text.includes('-60'));
    assert(/-58\.3/.test(text));
    assert(/00:19:29/.test(text) && /onset/i.test(text));
  });
  const selectedFirst = selection();
  click('[data-view="forces"]');
  check('Main Forces tab preserves the first-transmission flight, response and epoch', () => {
    assert.deepEqual(selection(), selectedFirst);
    assert.equal(state().terminalIndex, 5);
    assert($('#scene-count').textContent.startsWith('00:19:29'));
    assert($('#inspector').textContent.includes(short(D.witness.responseId)));
    assert($('#inspector').textContent.includes(formatted(firstTransmission.trueAirspeedMps, 1)));
  });
  check('Force magnitudes use the first-transmission record', () => {
    for (const [color, value] of [['#83c5f2', firstTransmission.liftN], ['#ecc17b', firstTransmission.dragN]]) {
      const line = h.scene.scene.lines.find(l => l.color === color && l.width === 3 && l.arrow);
      assert(line);
      assert(Math.abs(Math.hypot(...line.b.map((v, k) => v - line.a[k])) - value / 350000) < 1e-10);
    }
  });
  click('#force-back');
  check('Return from Forces restores the exact first-transmission selection', () => assert.deepEqual(selection(), selectedFirst));
  click('#inspect-forces');
  check('Dedicated force-inspection button uses the same first-transmission state', () => {
    assert.deepEqual(selection(), selectedFirst);
    assert($('#scene-count').textContent.startsWith('00:19:29'));
  });
  input('#terminal-time', 6, 'change');
  click('#force-back');
  check('Explicit force-epoch selection also updates the saved-state selection', () => {
    assert.equal(state().checkpoint, 6);
    assert.equal($('[data-checkpoint-utc]').dataset.checkpointUtc, finalTransmission.epoch);
    assert($('#checkpoint-interval').textContent.includes('8.000 seconds'));
  });

  input('#time-slider', 3);
  const selectedPowered = selection(); click('[data-view="forces"]');
  check('A powered checkpoint with no exported forces stays selected and reports absence', () => {
    assert.deepEqual(selection(), selectedPowered);
    assert(missingForces());
    assert(!h.scene.scene.lines.some(l => l.width === 3 && l.arrow));
  });
  click('#force-back');
  input('#flight-select', alternate.id, 'change');
  const selectedAlternate = selection(); click('[data-view="forces"]');
  check('Forces on another flight never substitutes the worked example', () => {
    assert.deepEqual(selection(), selectedAlternate);
    assert(missingForces());
    assert($('#inspector').textContent.includes(short(alternate.id)));
    assert(!h.scene.scene.lines.some(l => l.width === 3 && l.arrow));
  });
  click('#force-back');
  check('Return from unavailable forces preserves the alternative flight', () => {
    assert.deepEqual(selection(), selectedAlternate);
    assert($('#inspector').textContent.includes('00:11:00'));
  });

  click('[data-view="grid"]'); input('#cell-select', D.witness.configId, 'change'); click('#open-config-flight');
  const gridEntry = selection();
  check('Grid entry loads the clearly identified seven-checkpoint worked example', () => {
    assert.equal(gridEntry.response, D.witness.responseId);
    assert.equal(+$('#time-slider').max, 6);
    assert($('#inspector').textContent.includes(short(D.witness.responseId)));
  });
  input('#flight-select', alternate.id, 'change'); input('#flight-select', D.witness.flightId, 'change');
  check('Dropdown and grid entry select the same worked-example dataset', () => assert.deepEqual(selection(), gridEntry));
  click('#guided-example');
  check('Guided entry selects the same worked-example dataset', () => assert.deepEqual(selection(), gridEntry));

  const slider = $('#time-slider'); input('#time-slider', 2);
  check('Checkpoint slider retains its DOM node during input', () => assert.equal($('#time-slider'), slider));
  click('#step-play'); tick();
  check('Slideshow advances one saved checkpoint', () => assert.equal(state().checkpoint, 3));
  input('#time-slider', 1); tick();
  check('Manual slider selection cancels the timer', () => assert(state().checkpoint === 1 && !state().playing && h.timers.size === 0));
  click('#step-play'); click('#step-next'); tick();
  check('Manual Next cancels the timer', () => assert(state().checkpoint === 2 && !state().playing));
  click('#step-play'); click('#jump-terminal'); tick();
  check('Jump to final transmission cancels the timer', () => assert(state().checkpoint === 6 && !state().playing));
  // Check the full-history restart independently of the terminal-only scope.
  click('#route-overview'); click('#step-play'); tick();
  check('Full-history slideshow restart advances from the first saved checkpoint', () => assert(state().checkpoint === 1 && state().playing));
  click('[data-view="forces"]'); tick();
  check('View switch cancels the slideshow', () => assert(!state().playing && state().view === 'forces' && h.timers.size === 0));

  click('#guided-example'); click('#cloud-mode');
  const otherResponse = D.points.find(p => p.flightId === D.witness.flightId && p.id !== D.witness.responseId && p.compatible);
  input('#point-select', otherResponse.id, 'change'); click('#point-flight');
  check('Another response on the witness parent has no substituted witness checkpoints', () => {
    assert(!$('#time-slider'));
    assert.equal(state().routeResponseId, otherResponse.id);
    assert($('#inspector').textContent.includes('00:11:00'));
  });
  check('Missing ground speed stays missing and derived summary mass is labelled', () => {
    assert(/Ground speed\s*—/.test($('#inspector').textContent));
    assert($('#inspector').textContent.includes('Mass · derived'));
  });
  const selectedOtherResponse = selection(); click('[data-view="forces"]');
  check('Forces also protects another response on the witness parent', () => {
    assert.deepEqual(selection(), selectedOtherResponse);
    assert(missingForces());
    assert(!h.scene.scene.lines.some(l => l.width === 3 && l.arrow));
  });
  click('#force-back'); click('#cloud-mode');
  const orphan = D.points.find(p => !D.flights.some(f => f.id === p.flightId) && p.compatible);
  input('#point-select', orphan.id, 'change'); click('#route-mode');
  check('A response without an exported parent does not show the previous flight', () => assert($('#inspector').textContent.includes('No saved flight available')));
  click('[data-view="grid"]');
  const empty = D.configurations.find(c => !D.flights.some(f => f.configId === c.id));
  input('#cell-select', empty.id, 'change'); click('[data-view="flight"]');
  check('An uncomputed configuration clears the previous flight', () => assert($('#inspector').textContent.includes('No saved flight available')));

  click('#guided-example'); input('#time-slider', 5); click('#route-terminal');
  check('Terminal close-up preserves the selected state and exposes three explicit checkpoints', () => {
    assert.equal(state().checkpoint, 5);
    assert.equal(state().routeExtent, 'terminal');
    assert.equal(+$('#time-slider').min, 4);
    assert.equal(+$('#time-slider').max, 6);
    assert.deepEqual($$('#checkpoint-sequence [data-checkpoint-index]').map(b => +b.dataset.checkpointIndex), [4, 5, 6]);
  });
  const terminalPositions = [4, 5, 6].map(i => ({ index: i, ...h.scene.project(checkpointMarker(i).p) }));
  measurements.terminalProjection768x480 = terminalPositions.map(p => ({ index: p.index, x: p.x, y: p.y }));
  measurements.finalTransmissionSeparationPx = Math.hypot(terminalPositions[2].x - terminalPositions[1].x, terminalPositions[2].y - terminalPositions[1].y);
  check('Terminal points are in frame and final transmissions have useful screen separation', () => {
    terminalPositions.forEach(p => assert(p.visible && p.x > 20 && p.x < 748 && p.y > 20 && p.y < 460));
    assert(measurements.finalTransmissionSeparationPx > 24, 'recorded descent is legible at desktop size');
  });
  check('Terminal height panel contains the recorded descent and elapsed-time evidence', () => {
    assert($('#terminal-height-plot'));
    const text = $('.terminal-detail').textContent;
    assert(text.includes('459.049'));
    assert(/8(?:\.000)?\s*s(?:econds)?/.test(text));
  });
  const heightPositions = () => $$('[data-terminal-checkpoint] circle').map(circle => [Number(circle.getAttribute('cx')), Number(circle.getAttribute('cy'))]);
  const fixedHeights = heightPositions();
  check('Height chart uses actual unequal elapsed-time gaps, with separate saved dots', () => {
    const [[x4], [x5, y5], [x6, y6]] = fixedHeights;
    const firstGap = firstTransmission.elapsedSeconds - D.witness.states[4].elapsedSeconds;
    const secondGap = finalTransmission.elapsedSeconds - firstTransmission.elapsedSeconds;
    assert(Math.abs((x6 - x5) / (x5 - x4) - secondGap / firstGap) < 1e-12);
    assert(y6 > y5, 'the lower final height is below the first-transmission height on the chart');
    assert(!$('#terminal-height-plot polyline'));
  });
  check('Terminal scene does not connect saved positions into an inferred path', noSpatialConnections);
  for (const i of [4, 5, 6]) {
    click($('#checkpoint-sequence [data-checkpoint-index="' + i + '"]'));
    check('Terminal list unambiguously selects saved checkpoint ' + i, () => {
      assert.equal(state().checkpoint, i);
      assert.equal($('[data-checkpoint-utc]').dataset.checkpointUtc, D.witness.states[i].epoch);
      assert.equal(+$('[data-terminal-time-cursor]').dataset.terminalTimeCursor, i);
      assert.deepEqual(heightPositions(), fixedHeights, 'height/time axes stay fixed across selected checkpoints');
    });
  }

  click('#route-overview'); input('#time-slider', 5);
  check('Full-route view has no long spatial chords through unrecorded intervals', noSpatialConnections);
  const overlapHit = checkpointHit(5);
  const overlapCandidates = h.scene._hitCandidatesAtEvent({ clientX: overlapHit.x, clientY: overlapHit.y });
  check('Actual overview projection exposes all overlapping terminal candidates', () => {
    for (const i of [4, 5, 6]) assert(overlapCandidates.some(hit => hit.item.id === 'checkpoint:' + i));
  });
  h.pointerClick(overlapHit.x, overlapHit.y);
  check('Clicking an overlapping terminal marker opens a chooser without changing selection', () => {
    assert.equal(state().checkpoint, 5);
    assert($('#checkpoint-choice') && !$('#checkpoint-choice').hidden);
    const text = $('#checkpoint-choice').textContent;
    for (const time of ['00:19:19', '00:19:29', '00:19:37']) assert(text.includes(time));
  });
  const chooseFirst = $$('#checkpoint-choice button').find(b => b.textContent.includes('00:19:29'));
  click(chooseFirst);
  check('Choosing the first transmission never selects fuel exhaustion', () => {
    assert.equal(state().checkpoint, 5);
    assert.equal($('[data-checkpoint-utc]').dataset.checkpointUtc, firstTransmission.epoch);
  });
  click('#route-terminal'); input('#time-slider', 5);
  const terminalSelection = selection(); click('[data-view="forces"]'); click('#force-back');
  check('Force round-trip preserves terminal framing and selected epoch', () => {
    assert.deepEqual(selection(), terminalSelection);
    assert.equal(state().routeExtent, 'terminal');
  });
  check('Display interactions leave the scientific export unchanged', () => assert(h.dataUnchanged()));

  console.log(JSON.stringify({ scope: 'Controller and production renderer geometry in jsdom; Canvas2D rasterization omitted; no browser, model rerun or scientific validation', passed: tests.length, tests, measurements }, null, 2));
} finally { h.close(); }
