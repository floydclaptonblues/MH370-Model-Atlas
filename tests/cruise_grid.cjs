// Integration checks for the completed-run 3D comparison. The real controller,
// projection, draw traversal and pointer handlers run; Canvas2D pixels are stubbed.
// No aircraft model is loaded and no flight is computed.
const {JSDOM} = require('jsdom');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const dom = new JSDOM('<!doctype html><html><body>' + read('src/flight_lab_body.html') + '</body></html>', {
  url:'https://example.test/flight-lab.html', runScripts:'outside-only'
});
const w = dom.window, frames = new Map(), errors = [], tests = [];
let nextFrame = 0;
const bounds = {left:0, top:0, width:900, height:590};
const noop = () => {};
const context = Object.fromEntries([
  'setTransform','clearRect','fillRect','beginPath','moveTo','lineTo','closePath',
  'fill','stroke','rect','arc','save','restore','strokeText','fillText','setLineDash','drawImage'
].map(name => [name, noop]));
context.measureText = text => ({width:String(text).length * 6});
w.HTMLCanvasElement.prototype.getContext = () => context;
w.HTMLCanvasElement.prototype.getBoundingClientRect = () => ({...bounds, right:bounds.width, bottom:bounds.height});
w.HTMLElement.prototype.scrollIntoView = noop;
w.requestAnimationFrame = fn => { const id = ++nextFrame; frames.set(id, fn); return id; };
w.cancelAnimationFrame = id => frames.delete(id);
w.addEventListener('error', e => { errors.push(e.error || e.message); e.preventDefault(); });
w.eval(read('data/cruise-production-108/catalogue.js'));
w.eval(read('flight-lab/assets/data.js'));
const D = w.CRUISE_PRODUCTION_108;
const sourceBefore = JSON.stringify(D), legacyBefore = JSON.stringify(w.MH370_DATA);
w.eval(read('flight-lab/assets/scene3d.js'));
w.eval(read('flight-lab/assets/cruise-production.js'));
w.eval(read('flight-lab/assets/cruise-grid.js'));
const $ = s => w.document.querySelector(s);
const $$ = s => [...w.document.querySelectorAll(s)];
function flush() {
  for (let n = 0; frames.size; n++) {
    assert(n < 20, 'display animation frames settle');
    const work = [...frames.values()]; frames.clear(); work.forEach(fn => fn(0));
  }
  if (errors.length) throw errors.shift();
}
function click(s) { assert($(s), s); $(s).click(); flush(); }
function input(s, value) { assert($(s), s); $(s).value = value; $(s).dispatchEvent(new w.Event('change', {bubbles:true})); flush(); }
function check(name, fn) { fn(); tests.push(name); }
const reset = () => click('#cp-reset');
const grid = () => w.CRUISE_GRID.renderer;
const gridIds = () => [...new Set(grid().scene.points.map(p => p.id).filter(Boolean))].sort();
const sourceIds = list => Array.from(list, c => c.id).sort();
const filteredIds = () => sourceIds(w.CRUISE_LAB.getFilteredConfigurations());
function pointerClick(x, y) {
  for (const type of ['pointerdown','pointerup']) {
    const e = new w.MouseEvent(type, {bubbles:true, button:0, clientX:x, clientY:y});
    Object.defineProperties(e, {pointerId:{value:1}, pointerType:{value:'mouse'}});
    $('#cp-grid-canvas').dispatchEvent(e);
  }
  flush();
}

try {
  flush();
  check('Completed run opens on its own 3D comparison with all source configurations', () => {
    assert.equal(w.CRUISE_LAB.getState().view, 'grid');
    assert.equal($('#cp-grid-panel').hidden, false);
    assert.equal($('#cp-table-panel').hidden, true);
    assert.equal(w.CRUISE_LAB.getState().catalogue, 'cruise');
    assert.deepEqual(gridIds(), sourceIds(D.configurations));
    assert.equal(gridIds().length, 424);
    assert.equal(D.configurations.filter(c => c.accepted).length, 208);
    assert.match($('#cp-grid-count').textContent, /424/);
  });

  check('The three parameter axes and sampled-level spacing are explained', () => {
    const labels = grid().scene.labels.map(x => x.text).join(' ');
    assert.match(labels, /Mach/i);
    assert.match(labels, /level|altitude/i);
    assert.match(labels, /arrival/i);
    assert.match($('#cp-grid-caption').textContent, /categorical|equally spaced|evenly spaced/i);
    assert.match($('#cp-grid-caption').textContent, /starting states, not time or distance/i);
    assert.match($('#cp-grid-caption').textContent, /stopped climb may not have reached that target/i);
    assert.deepEqual(Array.from(w.CRUISE_GRID.getState().axes.mach), [.67,.75,.78]);
    assert.deepEqual(Array.from(w.CRUISE_GRID.getState().axes.levels), [25661,27830,29987,30053,31946,33985]);
  });

  check('Outcome glyphs distinguish model stops, exhausted searches and mixed timing/fuel failures', () => {
    const state = w.CRUISE_GRID.getState();
    assert.deepEqual(JSON.parse(JSON.stringify(state.counts)), {
      accepted:208, 'lift-stop':100, 'fuel-exhausted':113, 'no-joint-match':3
    });
    assert.equal(state.categories.A001_TO275, 'lift-stop');
    assert.equal(state.categories.A078_TO275, 'accepted');
    for (const id of ['A030_TO275','A034_TO275','A038_TO275']) {
      assert.equal(state.categories[id], 'no-joint-match');
      assert(D.configurations.find(c => c.id === id).trialCounts.withEngineFuel > 0);
    }
    assert.equal(state.categories.A042_TO275, 'fuel-exhausted');
    const markers = grid().scene.points.filter(p => p.id && !p.selected);
    const distinctShapes = new Set(markers.map(p => p.shape));
    assert.equal(distinctShapes.size, 4, 'outcomes remain distinct without colour perception');
    assert.equal(markers.length, 424, 'one scientific marker per configuration');
  });

  check('Default projection keeps every configuration in frame at desktop and narrow widths', () => {
    for (const [width,height] of [[900,590],[500,570],[360,480],[300,390]]) {
      Object.assign(bounds,{width,height}); grid().resize(); click('#cp-grid-reset');
      const rendered = [...new Set(grid().hitRegions.map(h => h.item.id))].sort();
      assert.deepEqual(rendered, sourceIds(D.configurations), 'all markers rendered at '+width+'×'+height);
      assert(grid().hitRegions.every(h => h.x >= 0 && h.y >= 0 && h.x <= width && h.y <= height), 'markers within viewport');
    }
    Object.assign(bounds,{width:900,height:590}); grid().resize(); click('#cp-grid-reset');
  });

  check('Each Mach filter draws exactly the corresponding saved configurations', () => {
    for (const mach of ['0.67','0.75','0.78']) {
      reset(); input('#cp-mach', mach);
      assert.deepEqual(gridIds(), sourceIds(D.configurations.filter(c => c.mach === +mach)));
      assert.deepEqual(gridIds(), filteredIds());
    }
  });

  check('Group, level and result filters expose the four marginal unsuccessful cases', () => {
    reset(); input('#cp-group','365.113 hPa, Mach 0.75'); input('#cp-level','31946');
    assert.equal(gridIds().length, 30);
    assert.match($('#cp-filter-count').textContent, /26 with an accepted flight/);
    input('#cp-result','not-found');
    assert.deepEqual(gridIds(), ['A030_TO275','A034_TO275','A038_TO275','A042_TO275']);
    assert.deepEqual(gridIds(), filteredIds());
    assert.equal($('#cp-flight'), null);
  });

  check('An actual marker click selects its exact configuration in the shared inspector', () => {
    reset(); input('#cp-arrival','A005');
    const expected = 'A005_TO250';
    const hit = grid().hitRegions.find(h => h.item.id === expected);
    assert(hit, 'selected source record has a production hit region');
    const hits = w.Scene3D.hitCandidates(grid().hitRegions, hit.x, hit.y);
    assert.equal(hits.length, 1, 'this sparse view supplies an unambiguous pointer target');
    pointerClick(hit.x, hit.y);
    assert.equal(w.CRUISE_LAB.getState().configId, expected);
    assert.match($('#cp-detail').textContent, /A005_TO250/);
    assert.equal($('[data-cp-config="'+expected+'"]').closest('tr').classList.contains('cp-selected'), true);
  });

  check('Real projected overlaps offer an exact-record chooser before changing selection', () => {
    reset();
    const overlap = grid().hitRegions.map(h => ({h, hits:w.Scene3D.hitCandidates(grid().hitRegions,h.x,h.y)})).find(x => x.hits.length > 1);
    assert(overlap, 'dense source population has a real projected overlap');
    const before = w.CRUISE_LAB.getState().configId;
    pointerClick(overlap.h.x, overlap.h.y);
    assert.equal(w.CRUISE_LAB.getState().configId, before);
    assert.equal($('#cp-grid-overlap').hidden, false);
    const choices = $$('#cp-grid-overlap-select option').map(x => x.value).filter(Boolean);
    assert(choices.length > 1);
    assert.deepEqual([...new Set(choices)].sort(), Array.from(overlap.hits, h => h.item.id).sort());
    const id = choices.find(id => id !== before) || choices[0];
    input('#cp-grid-overlap-select', id);
    assert.equal(w.CRUISE_LAB.getState().configId, id);
    assert($('#cp-detail').textContent.includes(id));
    assert($('[data-cp-config="'+id+'"]').closest('tr').classList.contains('cp-selected'));
  });

  check('The table and grid retain the same selected flight and inspection state', () => {
    reset(); input('#cp-arrival','A078'); input('#cp-level','31946');
    const flight = D.flights.find(f => f.configId === 'A078_TO275');
    input('#cp-flight', flight.id);
    const before = w.CRUISE_LAB.getState();
    click('#cp-table-view');
    assert.equal($('#cp-table-panel').hidden, false);
    assert.equal($('#cp-grid-panel').hidden, true);
    assert.equal(w.CRUISE_LAB.getState().configId, before.configId);
    assert.equal(w.CRUISE_LAB.getState().flightId, before.flightId);
    click('#cp-grid-view');
    assert.equal($('#cp-grid-panel').hidden, false);
    assert.equal(w.CRUISE_LAB.getState().flightId, before.flightId);
    assert.match($('#cp-flight-details').textContent, /0\.101 kg/);
    assert.match($('#cp-flight-details').textContent, /00:11:00\.068 UTC/);
  });

  check('Untested group/level combinations produce no markers or inherited result', () => {
    reset(); input('#cp-group','300.9 hPa, Mach 0.75'); input('#cp-level','30053');
    assert.deepEqual(gridIds(), []);
    assert.equal(w.CRUISE_LAB.getState().configId, null);
    assert.equal(w.CRUISE_LAB.getState().flightId, null);
    assert.match($('#cp-detail').textContent, /No matching configuration/);
    assert.equal($('#cp-flight'), null);
    assert.equal($('#cp-grid-overlap').hidden, true);
  });

  check('The earlier catalogue links to the new comparison without replacing its own controls', () => {
    reset(); input('#cp-arrival','A006');
    const before = w.CRUISE_LAB.getState();
    click('#cp-earlier-tab');
    assert.equal($('#earlier-terminal-catalogue').hidden, false);
    assert.equal($('#cruise-production-108').hidden, true);
    assert($('[data-view="grid"]'), 'historical grid control retained');
    click('#cp-open-current-grid');
    assert.equal(w.CRUISE_LAB.getState().catalogue, 'cruise');
    assert.equal(w.CRUISE_LAB.getState().view, 'grid');
    assert.equal(w.CRUISE_LAB.getState().configId, before.configId);
    assert.equal(w.CRUISE_LAB.getState().flightId, before.flightId);
    assert.equal($('#earlier-terminal-catalogue').hidden, true);
  });

  check('Camera actions change the view without changing the scientific selection', () => {
    const before = w.CRUISE_LAB.getState(), initial = {...grid().view};
    click('#cp-grid-zoom-in'); assert(grid().view.zoom > initial.zoom);
    click('#cp-grid-zoom-out');
    click('#cp-grid-top'); assert.notEqual(grid().view.pitch, initial.pitch);
    click('#cp-grid-front');
    click('#cp-grid-reset');
    assert.equal(w.CRUISE_LAB.getState().configId, before.configId);
    assert.equal(w.CRUISE_LAB.getState().flightId, before.flightId);
    assert.deepEqual(gridIds(), filteredIds());
  });

  check('Display and filtering leave both scientific exports unchanged', () => {
    assert.equal(JSON.stringify(D), sourceBefore);
    assert.equal(JSON.stringify(w.MH370_DATA), legacyBefore);
  });
  console.log(JSON.stringify({scope:'Cruise grid controller, production projection and pointer interactions; no browser pixel QA or flight computation', passed:tests.length, tests},null,2));
} finally {
  w.CRUISE_GRID?.renderer?.destroy();
  dom.window.close();
}
