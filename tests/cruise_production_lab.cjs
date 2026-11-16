// Saved-result UI checks. No model imports or flight computation.
const {JSDOM} = require('jsdom');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
const dom = new JSDOM('<!doctype html><html><body>' + read('src/flight_lab_body.html') + '</body></html>', {
  url:'https://example.test/flight-lab.html', runScripts:'outside-only'
});
const w = dom.window;
w.HTMLElement.prototype.scrollIntoView = () => {};
const events = [];
w.addEventListener('atlas:catalogue', e => events.push(e.detail.catalogue));
w.eval(read('data/cruise-production-108/catalogue.js'));
w.eval(read('flight-lab/assets/data.js'));
const sourceBefore = JSON.stringify(w.CRUISE_PRODUCTION_108);
const oldBefore = JSON.stringify(w.MH370_DATA);
w.eval(read('flight-lab/assets/cruise-production.js'));
const D = w.CRUISE_PRODUCTION_108;
const $ = s => w.document.querySelector(s);
const $$ = s => [...w.document.querySelectorAll(s)];
const input = (s, value) => { assert($(s), s); $(s).value = value; $(s).dispatchEvent(new w.Event('change', {bubbles:true})); };
const click = s => { assert($(s), s); $(s).click(); };
let checks = 0;
function check(name, fn) { fn(); checks++; }
function reset() { click('#cp-reset'); }
function selectFlight(f) {
  reset(); input('#cp-arrival', f.arrival);
  click('[data-cp-config="' + f.configId + '"]');
  input('#cp-flight', f.id);
}
check('opens current catalogue', () => {
  assert.equal(w.CRUISE_LAB.getState().catalogue, 'cruise');
  assert.equal($('#cruise-production-108').hidden, false);
  assert.equal($('#earlier-terminal-catalogue').hidden, true);
  assert.equal(w.document.body.dataset.flightCatalogue, 'cruise');
  assert.equal(events[0], 'cruise');
});
check('all source population is present', () => {
  assert.equal(w.CRUISE_LAB.getState().filteredConfigurations, 424);
  assert.equal(w.CRUISE_LAB.getState().plottedFlights, 266);
  assert.equal($$('#cp-arrival option').length, 109);
  assert.equal($$('#cp-group option').length, 7);
  assert.match($('#cp-filter-count').textContent, /208 with an accepted flight/);
  assert.match($('#cp-filter-count').textContent, /216 without/);
});
check('every configuration reachable by pagination', () => {
  const ids = [];
  for (;;) {
    ids.push(...$$('[data-cp-config]').map(x => x.dataset.cpConfig));
    if ($('#cp-next').disabled) break;
    click('#cp-next');
  }
  assert.equal(ids.length, 424);
  assert.equal(new Set(ids).size, 424);
  assert.deepEqual(ids, Array.from(D.configurations, c => c.id));
  reset();
});
check('marginal group filters to all thirty tests', () => {
  input('#cp-group', '365.113 hPa, Mach 0.75'); input('#cp-level', '31946');
  assert.equal(w.CRUISE_LAB.getState().filteredConfigurations, 30);
  assert.match($('#cp-filter-count').textContent, /26 with an accepted flight/);
  assert.match($('#cp-filter-count').textContent, /4 without/);
});
check('four no-fit outcomes retain their separate directional endings', () => {
  input('#cp-result', 'not-found');
  assert.equal(w.CRUISE_LAB.getState().filteredConfigurations, 4);
  assert.deepEqual($$('[data-cp-config]').map(b => b.dataset.cpConfig), ['A030_TO275','A034_TO275','A038_TO275','A042_TO275']);
  click('[data-cp-config="A030_TO275"]');
  assert.equal($('#cp-flight'), null);
  assert.match($('#cp-detail').textContent, /Starting point found; no trial met all timing/);
  assert.match($('#cp-detail').textContent, /No first-turn starting point found/);
  assert.match($('#cp-detail').textContent, /314\.756 µs/);
  assert.match($('#cp-detail').textContent, /With engine fuel at 00:11: 16/);
});
check('no accepted map markers for unsuccessful selection', () => {
  assert.equal(w.CRUISE_LAB.getState().plottedFlights, 0);
  assert.match($('#cp-map').textContent, /No accepted-flight positions/);
});
check('engine fuel keeps the APU reserve separate and preserves the marginal case', () => {
  const f = D.flights.find(f => f.configId === 'A078_TO275' && f.check.performed);
  assert(f);
  selectFlight(f);
  const text = $('#cp-flight-details').textContent;
  assert.match(text, /0\.101 kg/);
  assert.match(text, /6\.804 kg held for the APU/);
  assert.match(text, /00:11:00\.068 UTC/);
  assert.match(text, /exact flight was repeated/);
  assert.match(text, /fuel difference -0\.061 kg/);
});
check('flight details use the selected checkpoint and source rows', () => {
  const f = D.flights.find(f => f.configId === 'A078_TO275' && f.check.performed);
  assert.equal(w.CRUISE_LAB.getState().flightId, f.id);
  assert.equal($$('.cp-checkpoints tbody tr').length, 3);
  assert.deepEqual($$('.cp-checkpoints tbody th').map(x => x.textContent), ['20:41:05', '21:41:27', '00:11:00']);
  assert($('#cp-flight-details a[href="' + f.sourceRows[0].url + '"]'));
  assert.equal($$('#cp-flight-details td').some(x => /undefined|NaN/.test(x.textContent)), false);
});
check('unrepeated flight does not inherit another flight’s check', () => {
  const f = D.flights.find(f => !f.check.performed);
  selectFlight(f);
  assert.match($('#cp-flight-details').textContent, /not itself selected for a half-step repeat/);
  assert.equal($('#cp-flight-details').textContent.includes('This exact flight was repeated'), false);
});
check('range end remains explicitly identified', () => {
  const f = D.flights.find(f => f.rangeEnd);
  selectFlight(f);
  assert.match($('#cp-flight-details').textContent, /Range-end record/);
  assert.match($('#cp-flight').selectedOptions[0].textContent, /range end/);
});
check('powered-to-horizon stays distinct from a known exhaustion time', () => {
  const f = D.flights.find(f => f.poweredTo0040);
  selectFlight(f);
  assert.match($('#cp-flight-details').textContent, /Still powered at 00:40/);
  assert.match($('#cp-flight-details').textContent, /No exhaustion time was established/);
});
check('control filter does not silently include an unrun climb', () => {
  reset(); input('#cp-group', '300.9 hPa, Mach 0.75'); input('#cp-level', '30053');
  assert.equal(w.CRUISE_LAB.getState().filteredConfigurations, 0);
  assert.match($('#cp-detail').textContent, /No matching configuration/);
  input('#cp-level', 'CONTROL');
  assert.equal(w.CRUISE_LAB.getState().filteredConfigurations, 4);
});
check('overlapping markers offer actual records, not arbitrary substitution', () => {
  reset();
  const f = D.flights[0], svg = $('#cp-map svg');
  svg.getBoundingClientRect = () => ({left:0, top:0, width:640, height:600});
  svg.dispatchEvent(new w.MouseEvent('click', {bubbles:true, clientX:78+(f.position0011.longitude-90)*68.75, clientY:35+(-30-f.position0011.latitude)*82}));
  assert.equal($('#cp-overlap').hidden, false);
  const options = $$('#cp-overlap-flight option').filter(x => x.value);
  assert(options.length > 1);
  const id = options[options.length - 1].value;
  input('#cp-overlap-flight', id);
  assert.equal(w.CRUISE_LAB.getState().flightId, id);
  assert($('#cp-flight-details').textContent.includes(id));
});
check('catalogue switch updates scope without removing historical controls', () => {
  click('#cp-earlier-tab');
  assert.equal($('#earlier-terminal-catalogue').hidden, false);
  assert.equal($('#cruise-production-108').hidden, true);
  assert.equal(w.document.body.dataset.flightCatalogue, 'legacy');
  assert.equal(events[events.length - 1], 'legacy');
  assert($('#guided-example'));
  assert($('#sources-open').closest('#earlier-terminal-catalogue'));
  click('#cp-current-tab');
  assert.equal(w.document.body.dataset.flightCatalogue, 'cruise');
  assert.equal($('#cruise-production-108').hidden, false);
});
check('downloads and original measurements remain attached and unchanged', () => {
  assert($('#cp-downloads a[href="data/cruise-production-108/sources/PROD_SOLUTIONS.csv"]'));
  assert($('#cp-downloads a[href="data/cruise-production-108/catalogue.json"]'));
  const sourceLink = $$('#cp-downloads a').find(x => x.textContent.includes('Pinned findings'));
  assert(sourceLink.href.endsWith('/CRUISE_LEVEL_PRODUCTION_108/FINDINGS.md'));
  assert.equal(sourceLink.href.includes('CRUISE_LEVEL_PRODUCTION_108//'), false);
  assert.equal(JSON.stringify(D), sourceBefore);
  assert.equal(JSON.stringify(w.MH370_DATA), oldBefore);
});
console.log(JSON.stringify({checks, result:'passed', scope:'DOM display, filtering, selection and preservation only; no flight computed'}, null, 2));
dom.window.close();
