// Projection and pointer-selection regressions using the production Scene3D class.
// Canvas drawing calls are no-ops: these are display-geometry checks, not pixel QA.
const assert = require('node:assert/strict');
const { createHarness } = require('./flight_lab_harness.cjs');
const h = createHarness(), tests = [];
const check = (name, fn) => { fn(); tests.push(name); };

try {
  check('Near-overlapping hit candidates retain the exact closest timestamp', () => {
    // Rounded display positions from the reviewed 768×480 overview. A nearer
    // camera depth must not make the fuel event beat a pointer on 00:19:29.
    const hits = [
      { x: 258.531, y: 145.860, radius: 7, depth: 10, item: { id: 'checkpoint:4' } },
      { x: 258.513, y: 146.048, radius: 9, depth: 11, item: { id: 'checkpoint:5' } },
      { x: 258.857, y: 147.401, radius: 7, depth: 11.1, item: { id: 'checkpoint:6' } }
    ];
    const candidates = h.Renderer.hitCandidates(hits, 258.513, 146.048);
    assert.equal(candidates[0].item.id, 'checkpoint:5');
    assert.deepEqual([...candidates].map(hit => hit.item.id).sort(), ['checkpoint:4', 'checkpoint:5', 'checkpoint:6']);
    assert.equal(candidates[0].distance, 0);
  });

  check('Selected-marker overlays do not create duplicate chooser entries', () => {
    const candidates = h.Renderer.hitCandidates([
      { x: 10, y: 10, radius: 7, depth: 12, item: { id: 'same' } },
      { x: 10, y: 10, radius: 9, depth: 12, item: { id: 'same' } },
      { x: 11, y: 10, radius: 7, depth: 11, item: { id: 'other' } }
    ], 10, 10);
    assert.deepEqual([...candidates].map(hit => hit.item.id), ['same', 'other']);
  });

  const scene = h.scene;
  scene.setView({ radius: 10, center: [0, 0, 0], yaw: 0, pitch: 0, zoom: 1 });
  scene.setScene({ points: [
    { p: [0, 0, 0], id: 'first', size: 6 },
    { p: [0.003, 0, 0.02], id: 'second', size: 4 }
  ], lines: [], labels: [] });
  h.flush();
  const first = scene.hitRegions.find(hit => hit.item.id === 'first');
  let singlePicks = [], candidatePicks = [];
  scene.onPick = id => singlePicks.push(id);
  scene.onPickCandidates = (ids, hits) => candidatePicks.push({ ids: [...ids], hits });

  check('Actual renderer draw traversal creates both overlapping hit regions', () => {
    assert.equal(scene.hitRegions.length, 2);
    assert(first && first.x === 384 && first.y === 240);
  });

  check('Pointer event dispatch delegates overlapping IDs to the chooser callback', () => {
    h.pointerClick(first.x, first.y);
    assert.equal(singlePicks.length, 0);
    assert.equal(candidatePicks.length, 1);
    assert.deepEqual(candidatePicks[0].ids, ['first', 'second']);
    assert.equal(candidatePicks[0].hits[0].distance, 0);
  });

  check('Without a chooser callback an exact nearest point wins', () => {
    scene.onPickCandidates = null;
    h.pointerClick(first.x, first.y);
    assert.deepEqual(singlePicks, ['first']);
  });

  check('A non-overlapping pointer click still selects its only point', () => {
    scene.setScene({ points: [{ p: [0, 0, 0], id: 'alone', size: 4 }], lines: [], labels: [] });
    scene.onPickCandidates = (ids, hits) => candidatePicks.push({ ids: [...ids], hits });
    h.flush(); h.pointerClick(384, 240);
    assert.equal(singlePicks.at(-1), 'alone');
    assert.equal(candidatePicks.length, 1);
  });

  check('An empty pointer click does not choose a stale record', () => {
    h.pointerClick(50, 50);
    assert.equal(singlePicks.at(-1), null);
  });

  check('Display-geometry checks leave the scientific export untouched', () => assert(h.dataUnchanged()));
  console.log(JSON.stringify({ scope: 'Production renderer geometry and pointer handlers with no-op Canvas2D rasterization; no browser or scientific-model validation', passed: tests.length, tests }, null, 2));
} finally { h.close(); }
