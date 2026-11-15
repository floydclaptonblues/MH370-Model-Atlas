// Plain-language readouts must describe the selected saved record, never fill
// missing motion with a different response, and keep the wind example separate.
// Display/controller checks only: no flight integration or scientific validation.
const assert = require('node:assert/strict');
const { createHarness } = require('./flight_lab_harness.cjs');

const h = createHarness(), { $, click, input, tick, state, w } = h;
const D = w.MH370_DATA, passed = [];
const check = (name, fn) => { fn(); passed.push(name); };
const text = selector => {
  const element = $(selector);
  assert(element, 'readout element exists: ' + selector);
  return element.textContent.replace(/\s+/g, ' ').trim();
};
const card = key => text('#plain-readout [data-readout="' + key + '"]');
const formatted = (value, decimals) => value.toLocaleString('en-US', {
  minimumFractionDigits: decimals, maximumFractionDigits: decimals
});
const includesNumber = (body, value, decimals) => {
  const expected = formatted(value, decimals);
  assert(body.includes(expected), 'readout contains source-derived value ' + expected);
};
const identity = () => ({
  flight: state().flight,
  response: state().routeResponseId,
  checkpoint: state().checkpoint
});
const currentClock = () => D.witness.states[state().checkpoint].epoch.slice(11, 19);
const assertWitnessTime = index => {
  assert.equal(state().checkpoint, index);
  assert.equal(state().flight, D.witness.flightId);
  assert.equal(state().routeResponseId, D.witness.responseId);
  assert(text('#readout-title').includes(D.witness.states[index].epoch.slice(11, 19)));
  assert.equal($('[data-checkpoint-utc]').dataset.checkpointUtc, D.witness.states[index].epoch);
};
const assertCoordinates = st => {
  const location = card('location');
  includesNumber(location, Math.abs(st.lat), 4);
  includesNumber(location, Math.abs(st.lon), 4);
  assert(location.includes('°' + (st.lat < 0 ? 'S' : 'N')));
  assert(location.includes('°' + (st.lon < 0 ? 'W' : 'E')));
};
const assertMissingMotion = () => {
  assert(/not (?:recorded|included)|unavailable|not available/i.test(card('motion')));
  assert(!/\d[\d,.]*\s*(?:km\/h|knots)/i.test(card('motion')),
    'a position-only record does not acquire a numeric speed');
  assert(!/travell?ing|moving (?:north|south|east|west)/i.test(text('#readout-summary')),
    'a position-only record does not acquire a travel direction');
};

try {
  check('Landing view describes the first saved example checkpoint', () => {
    assert.equal(state().view, 'flight');
    assert.equal($('#plain-readout').dataset.kind, 'flight');
    assertWitnessTime(0);
    assertCoordinates(D.witness.states[0]);
    assert($('#readout-checkpoint'));
  });

  check('Ground-motion readout converts the first checkpoint and names its travel direction', () => {
    const motion = card('motion');
    assert(/south/i.test(motion));
    assert(/781\s*km\/h/.test(motion));
    assert(/422\s*knots/.test(motion));
    includesNumber(motion, D.witness.states[0].trackDeg, 1);
    assert(/ground|Earth/.test(motion));
  });

  check('Near-level motion and ellipsoid-reference height remain distinct from ocean clearance', () => {
    const height = card('height');
    assert(/nearly steady|nearly level/i.test(height));
    assert(/reference/i.test(height));
    includesNumber(height, D.witness.states[0].heightM, 0);
    includesNumber(height, D.witness.states[0].heightM / .3048, 0);
    assert(!/above the model surface/i.test(height));
  });

  input('#readout-checkpoint', 3, 'change');
  check('Plain checkpoint control updates the source state, inspector and scene together', () => {
    assertWitnessTime(3);
    assertCoordinates(D.witness.states[3]);
    assert.equal(+$('#time-slider').value, 3);
    assert.equal(h.scene.scene.points.find(p => p.size === 6).id, 'checkpoint:3');
    includesNumber(card('fuel'), D.witness.states[3].fuelKg, 0);
    assert(/powered flight/i.test(card('fuel')));
  });

  input('#readout-checkpoint', 4, 'change');
  check('Nonzero auxiliary fuel is not mistaken for usable engine fuel at exhaustion', () => {
    assertWitnessTime(4);
    const fuel = card('fuel');
    assert(/engine fuel.*(?:runs out|exhaust)|fuel.*exhaust/i.test(fuel));
    assert(/auxiliary|APU/i.test(fuel));
    includesNumber(fuel, D.witness.states[4].fuelKg, 1);
  });

  input('#readout-checkpoint', 6, 'change');
  check('Final readout separates ground motion, instantaneous descent and model-surface height', () => {
    assertWitnessTime(6);
    assertCoordinates(D.witness.states[6]);
    assert(/south-southeast/.test(card('motion')));
    assert(/762\s*km\/h/.test(card('motion')));
    assert(/85\.3\s*m\/s/.test(card('height')));
    assert(/descending/i.test(card('height')));
    includesNumber(card('height'), D.witness.states[6].heightAboveSurfaceM, 0);
    assert(/above the model surface/.test(card('height')));
    assert(/without engine power/i.test(card('fuel')));
    assert(/auxiliary/i.test(card('fuel')));
  });

  check('Endpoint changes retain the eight-second interval and do not become a continuous trajectory', () => {
    const change = card('change');
    assert(/8(?:\.0+)?\s*s(?:econds?)?\b/.test(change));
    includesNumber(change, D.witness.states[5].heightM - D.witness.states[6].heightM, 1);
    assert(/endpoint|between.*saved|between.*record/i.test(change));
    assert(/not displayed|not.*continuous|no.*continuous/.test(change));
  });

  input('#readout-checkpoint', 5, 'change');
  const firstTransmission = identity();
  click('[data-view="forces"]');
  check('Force view keeps the first-transmission readout and its recorded bank', () => {
    assert.deepEqual(identity(), firstTransmission);
    assertWitnessTime(5);
    assertCoordinates(D.witness.states[5]);
    includesNumber(text('#readout-summary'), Math.abs(D.witness.states[5].bankDeg), 1);
    assert(!/60\.0°/.test(text('#readout-summary')),
      'the commanded bank is not substituted for the first-transmission recorded bank');
  });
  input('#terminal-time', 6, 'change');
  check('Force time control updates the plain readout to the same final checkpoint', () => {
    assertWitnessTime(6);
    assert(/85\.3\s*m\/s/.test(card('height')));
  });
  click('#force-back');
  input('#readout-checkpoint', 2, 'change');
  click('#step-play'); tick();
  check('Slideshow advances the plain summary and source readout together', () => {
    assertWitnessTime(3);
    assert(text('#readout-title').includes(currentClock()));
    assert.equal(+$('#readout-checkpoint').value, 3);
  });
  input('#readout-checkpoint', 1, 'change'); tick();
  check('Manual plain-readout selection stops playback and prevents stale time updates', () => {
    assertWitnessTime(1);
    assert.equal(state().playing, false);
    assert.equal(h.timers.size, 0);
  });

  const alternate = D.flights.find(f => f.id !== D.witness.flightId);
  input('#flight-select', alternate.id, 'change');
  check('Another flight shows its own one-state record with missing motion', () => {
    assert.equal(state().flight, alternate.id);
    assert.equal($('#plain-readout').dataset.kind, 'flight');
    assertCoordinates(alternate.states[0]);
    assertMissingMotion();
    assert(/not recorded|unavailable/i.test(card('height')));
    assert(!$('#readout-checkpoint'), 'one-state record has no phantom checkpoint selection');
  });
  const alternateIdentity = identity();
  click('[data-view="forces"]');
  check('Unavailable forces preserve the alternative flight and its missing-motion readout', () => {
    assert.deepEqual(identity(), alternateIdentity);
    assertCoordinates(alternate.states[0]);
    assertMissingMotion();
  });

  click('#guided-example'); click('#cloud-mode');
  check('Cloud position readout does not invent direction, speed or descent from command fields', () => {
    assert.equal($('#plain-readout').dataset.kind, 'final');
    assertCoordinates(D.points.find(p => p.id === state().point));
    assertMissingMotion();
    assert(/airborne|not.*impact/i.test(card('location')));
    assert(/not.*likely|not.*probab/i.test(card('meaning')));
  });
  const otherResponse = D.points.find(p => p.flightId === D.witness.flightId && p.id !== D.witness.responseId && p.compatible);
  input('#point-select', otherResponse.id, 'change'); click('#point-flight');
  check('A different response on the example parent never acquires example motion or checkpoints', () => {
    assert.equal(state().routeResponseId, otherResponse.id);
    assert(text('#readout-title').includes('00:11:00'));
    assertMissingMotion();
    assert(!$('#readout-checkpoint'));
    assert(!$('#time-slider'));
  });

  click('[data-view="grid"]');
  const uncomputed = D.configurations.find(c => c.evidence === 'none');
  input('#cell-select', uncomputed.id, 'change');
  check('Uncomputed scenario readout reports an absent result rather than a rejected aircraft', () => {
    assert.equal($('#plain-readout').dataset.kind, 'scenario');
    assert(/no.*(?:computed|flight).*result|no.*result.*available/i.test(text('#readout-summary')));
    assert(/not.*geographical|experiment settings/i.test(text('#plain-readout')));
  });
  click('[data-view="flight"]');
  check('An empty selection clears previous position, fuel and movement readouts', () => {
    assert.equal(state().flight, null);
    assert(/no.*(?:saved|imported).*flight|no.*aircraft state/i.test(text('#plain-readout')));
    for (const key of ['location', 'motion', 'height', 'fuel']) {
      assert(!$('#plain-readout [data-readout="' + key + '"]'), 'no stale ' + key + ' card');
    }
  });

  click('#guided-example'); input('#readout-checkpoint', 6, 'change');
  click('[data-view="forces"]');
  const selectedBeforeWind = identity(), recordBeforeWind = JSON.stringify(D.witness.states[6]);
  click('#wind-lab');
  check('Wind illustration is labelled separately without changing the selected flight identity', () => {
    assert.equal($('#plain-readout').dataset.kind, 'illustration');
    assert.deepEqual(identity(), selectedBeforeWind);
    assert(/illustration|example/i.test(text('#plain-readout')));
  });
  input('#wind-east', 0); input('#wind-north', 0); input('#wind-up', 0); input('#lab-heading', 180);
  const zeroWindText = text('#plain-readout');
  check('Zero-wind illustration gives due-south travel with the selected illustrative airspeed', () => {
    assert(/south/i.test(zeroWindText));
    const tas = state().labMach * Math.sqrt(1.4 * 287.05 * state().labTemp);
    includesNumber(zeroWindText, tas * 3.6, 0);
  });
  input('#wind-east', 60);
  check('Changing illustrative wind updates its readout but preserves the saved aircraft record', () => {
    assert.equal($('#plain-readout').dataset.kind, 'illustration');
    assert.notEqual(text('#plain-readout'), zeroWindText);
    assert(/east|south-southeast/i.test(text('#plain-readout')));
    assert.deepEqual(identity(), selectedBeforeWind);
    assert.equal(JSON.stringify(D.witness.states[6]), recordBeforeWind);
    assert(h.dataUnchanged());
  });
  click('#recorded-forces');
  check('Returning from the wind example restores the unchanged selected flight readout', () => {
    assert.equal($('#plain-readout').dataset.kind, 'flight');
    assert.deepEqual(identity(), selectedBeforeWind);
    assertWitnessTime(6);
    assert(/762\s*km\/h/.test(card('motion')));
    assert(h.dataUnchanged());
  });

  console.log(JSON.stringify({
    scope: 'Plain-language display/controller checks against frozen exported states; no browser raster QA, flight integration or scientific revalidation',
    passed: passed.length,
    tests: passed
  }, null, 2));
} finally { h.close(); }
