/* Display only: saved cruise results. No propagation, interpolation or refitting. */
(function () {
  'use strict';
  var D = window.CRUISE_PRODUCTION_108;
  var $ = function (s) { return document.querySelector(s); };
  if (!$('#cruise-production-108')) return;
  var catalogue = 'cruise';
  function switchCatalogue(next) {
    catalogue = next === 'legacy' ? 'legacy' : 'cruise';
    $('#cruise-production-108').hidden = catalogue !== 'cruise';
    $('#earlier-terminal-catalogue').hidden = catalogue !== 'legacy';
    [['#cp-current-tab', 'cruise'], ['#cp-earlier-tab', 'legacy']].forEach(function (p) {
      $(p[0]).classList.toggle('active', p[1] === catalogue);
      $(p[0]).setAttribute('aria-pressed', String(p[1] === catalogue));
    });
    document.body.dataset.flightCatalogue = catalogue;
    window.dispatchEvent(new CustomEvent('atlas:catalogue', {detail: {catalogue: catalogue}}));
    if (catalogue === 'legacy') window.dispatchEvent(new Event('resize'));
  }
  $('#cp-current-tab').addEventListener('click', function () { switchCatalogue('cruise'); });
  $('#cp-earlier-tab').addEventListener('click', function () { switchCatalogue('legacy'); });
  var legacyHashes = ['#earlier-terminal-catalogue', '#lab'];
  switchCatalogue(legacyHashes.indexOf(location.hash) >= 0 ? 'legacy' : 'cruise');
  window.addEventListener('hashchange', function () {
    if (legacyHashes.indexOf(location.hash) >= 0) switchCatalogue('legacy');
    if (location.hash === '#cruise-production-108') switchCatalogue('cruise');
  });
  if (!D || !Array.isArray(D.configurations) || !Array.isArray(D.flights)) {
    $('#cp-filter-count').textContent = 'The catalogue could not load. The source CSV downloads below remain available.';
    return;
  }
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return {'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]; }); };
  var finite = function (n) { return typeof n === 'number' && Number.isFinite(n); };
  var number = function (n, places) { return finite(n) ? n.toLocaleString('en-US', {minimumFractionDigits: places, maximumFractionDigits: places}) : 'not recorded'; };
  var signed = function (n, places) { return finite(n) ? (n > 0 ? '+' : '') + number(n, places) : 'not recorded'; };
  var position = function (p) { return p && finite(p.latitude) && finite(p.longitude) ? number(Math.abs(p.latitude), 4) + '°' + (p.latitude < 0 ? 'S' : 'N') + ', ' + number(Math.abs(p.longitude), 4) + '°' + (p.longitude < 0 ? 'W' : 'E') : 'not recorded'; };
  var clock = function (seconds) {
    if (!finite(seconds)) return 'not recorded';
    var ms = Math.round((19 * 3600 + 41 * 60 + 3 + seconds) * 1000);
    var day = 86400000; ms = ((ms % day) + day) % day;
    return String(Math.floor(ms / 3600000)).padStart(2, '0') + ':' +
      String(Math.floor(ms / 60000) % 60).padStart(2, '0') + ':' +
      String(Math.floor(ms / 1000) % 60).padStart(2, '0') + '.' + String(ms % 1000).padStart(3, '0');
  };
  var turn = function (n) { return finite(n) ? (Math.abs(n) < 1e-12 ? 'no course change' : number(Math.abs(n), 2) + '° ' + (n < 0 ? 'left' : 'right')) : 'not recorded'; };
  var byConfig = new Map(D.configurations.map(function (c) { return [c.id, c]; }));
  var byFlight = new Map(D.flights.map(function (f) { return [f.id, f]; }));
  var byArrival = new Map((D.arrivals || []).map(function (a) { return [a.id, a]; }));
  var state = {group: '', level: '', result: '', arrival: '', page: 0, configId: D.configurations[0].id, flightId: null};
  var pageSize = 12;
  var endings = {
    ACCEPTED_FLIGHT_FOUND: 'Accepted flight found',
    ACCEPTED_FLIGHT_ONLY_ON_AN_END_OF_THE_SEARCHED_RANGE: 'Accepted flights only at a searched-range end',
    NO_STARTING_POINT: 'No first-turn starting point found in the sampled search',
    STOPPED_AT_AN_AIRCRAFT_LIMIT_OF_THE_PERFORMANCE_MODEL: 'Stopped at the model’s lift-margin limit',
    FUEL_EXHAUSTED_BEFORE_THE_FIT_TIME_ON_EVERY_TRIAL_FLIGHT: 'Every trial exhausted engine fuel before 00:11',
    STARTING_POINT_FOUND_BUT_NO_ACCEPTED_FLIGHT: 'Starting point found; no trial met all timing and fuel requirements'
  };
  function filtered() {
    return D.configurations.filter(function (c) {
      return (!state.group || c.group === state.group) &&
        (!state.level || (state.level === 'CONTROL' ? c.kind === 'UNCHANGED_LEVEL_CONTROL' : c.kind !== 'UNCHANGED_LEVEL_CONTROL' && c.levelFt === +state.level)) &&
        (!state.result || c.accepted === (state.result === 'accepted')) &&
        (!state.arrival || c.arrival === state.arrival);
    });
  }
  D.groups.forEach(function (g) {
    $('#cp-group').insertAdjacentHTML('beforeend', '<option value="' + esc(g.id) + '">' + esc(g.label) + '</option>');
  });
  (D.arrivals || []).forEach(function (a) {
    $('#cp-arrival').insertAdjacentHTML('beforeend', '<option value="' + esc(a.id) + '">' + esc(a.id) + ' · Mach ' + number(a.mach, 2) + '</option>');
  });
  function groupTable() {
    var columns = ['CONTROL', 30053, 31946, 33985];
    var html = '<table><thead><tr><th scope="col">Starting group</th><th scope="col">Incoming level</th><th scope="col">30,053 ft</th><th scope="col">31,946 ft</th><th scope="col">33,985 ft</th></tr></thead><tbody>';
    D.groups.forEach(function (g) {
      html += '<tr><th scope="row">' + esc(g.label) + '</th>';
      columns.forEach(function (col) {
        var c = D.configurations.filter(function (x) { return x.group === g.id && (col === 'CONTROL' ? x.kind === 'UNCHANGED_LEVEL_CONTROL' : x.kind !== 'UNCHANGED_LEVEL_CONTROL' && x.levelFt === col); });
        var accepted = c.filter(function (x) { return x.accepted; }).length;
        html += '<td>' + (c.length ? '<span class="' + (accepted ? 'cp-cell-found' : 'cp-cell-none') + '">' + accepted + ' / ' + c.length + '</span> accepted' : 'Not a separate test') + '</td>';
      });
      html += '</tr>';
    });
    $('#cp-group-table').innerHTML = html + '</tbody></table>';
  }
  function direction(d, name) {
    return '<div class="cp-direction"><strong>' + name + ' first-turn search</strong><span>' + esc(endings[d.ending] || d.ending) + '</span><small>Coverage: ' + esc(d.coverage.toLowerCase()) + ' · Check: ' + esc(d.check) + '</small><a href="' + esc(d.sourceUrl) + '" target="_blank" rel="noopener">Directional source row ↗</a></div>';
  }
  function trialDetails(c) {
    var t = c.trialCounts || {};
    return '<details><summary>What the full trial flights established</summary><p>Distinct trials: <b>' + number(t.total, 0) + '</b>. With engine fuel at 00:11: <b>' + number(t.withEngineFuel, 0) + '</b>; of those, matching all three timing bands: <b>' + number(t.withEngineFuelAndAllTiming, 0) + '</b>.</p><p>Exhausted before 00:11: <b>' + number(t.outOfFuel, 0) + '</b>; of those, matching the two earlier timing bands: <b>' + number(t.outOfFuelAndEarlyTiming, 0) + '</b>. An exhausted flight has no supported timing residual at 00:11.</p>' +
      (finite(t.closest0011ResidualAmongPoweredEarlyFitsUs) && !c.accepted ? '<p>Among trials that kept fuel and met both earlier bands, the closest absolute 00:11 timing residual was <b>' + number(t.closest0011ResidualAmongPoweredEarlyFitsUs, 3) + ' µs</b>, against a 43 µs band.</p>' : '') + '</details>';
  }
  function flightDetails(f) {
    var event = f.exhaustion;
    var checked = f.check && f.check.performed;
    var check = checked ? 'This exact flight was repeated at half step; ' + (f.check.resolved ? 'its check resolved.' : 'its check is unresolved.') : 'This flight was not itself selected for a half-step repeat. A check on another flight does not validate this record.';
    var eventText = event ? clock(event.secondsAfter1941) + ' UTC' : f.poweredTo0040 ? 'Still powered at 00:40' : 'Not recorded';
    var html = '<h4>Saved flight <code>' + esc(f.id) + '</code></h4><p class="cp-description">At 00:11 this flight is airborne at <b>' + position(f.position0011) + '</b>, with <b>' + number(f.engineFuel0011Kg, 3) + ' kg of engine fuel</b> above the separate APU reserve.</p>' +
      '<div class="cp-flight-metrics"><div><span>Engine fuel at 00:11</span><strong>' + number(f.engineFuel0011Kg, 3) + ' kg</strong><small>Above the model’s APU reserve</small></div><div><span>Total fuel at 00:11</span><strong>' + number(f.fuel0011Kg, 3) + ' kg</strong><small>Includes ' + number(f.reserveKg, 3) + ' kg held for the APU</small></div><div class="cp-wide"><span>Recorded engine-fuel ending</span><strong>' + esc(eventText) + '</strong>' +
      (event ? '<small>' + number(event.secondsAfter0011, 3) + ' s after 00:11 · Numerical time, not physical timing accuracy</small>' : '<small>No exhaustion time was established before the continuation horizon.</small>') + '</div></div>' +
      '<p>Mach <b>' + number(f.mach, 2) + '</b> held; cruise level <b>' + number(f.levelFt, 0) + ' ft pressure altitude</b>. At 00:11 the recorded geometric height is ' + number(f.position0011.heightM, 1) + ' m above the reference ellipsoid.</p>' +
      '<p class="cp-check' + (checked ? '' : ' cp-unchecked') + '">' + esc(check) + '</p>';
    if (checked) {
      html += '<p>Half-step comparison: ' + f.check.rows.map(function (r) { return esc(r.side === 'L' ? 'left' : 'right') + ' search — position difference ' + number(r.positionDifference0011M, 3) + ' m, fuel difference ' + signed(r.fuelDifference0011Kg, 3) + ' kg' + (finite(r.eventDifferenceS) ? ', exhaustion-time difference ' + signed(r.eventDifferenceS, 3) + ' s' : '') + ' (<a href="' + esc(r.sourceUrl) + '" target="_blank" rel="noopener">check record ↗</a>)'; }).join('; ') + '.</p>';
    }
    html += f.rangeEnd ? '<p class="cp-range">Range-end record: ' + esc(f.rangeEndFlags.join(', ') || 'at an end of the searched command range') + '. Its acceptance does not establish coverage beyond that range.</p>' : '<p>Returned commands are not flagged at a searched-range end.</p>';
    html += '<details><summary>Saved checkpoints and commands</summary><p>First course change: <b>' + turn(f.firstTurnDeg) + '</b>. Second course change: <b>' + turn(f.secondTurnDeg) + '</b>, starting at <b>' + clock(f.secondTurnStartS) + ' UTC</b>. These are course changes, not bank angles.</p><div class="cp-table-scroll"><table class="cp-checkpoints"><thead><tr><th scope="col">UTC</th><th scope="col">Saved position</th><th scope="col">Height (m)</th><th scope="col">BTO residual (µs)</th><th scope="col">BFO residual (Hz)</th></tr></thead><tbody>' +
      f.checkpoints.map(function (p) { return '<tr><th scope="row">' + esc(p.utc) + '</th><td>' + position(p) + '</td><td>' + number(p.heightM, 1) + '</td><td>' + signed(p.timingResidualUs, 3) + '</td><td>' + signed(p.frequencyResidualHz, 3) + '</td></tr>'; }).join('') +
      '</tbody></table></div><p>The BTO timing residuals were fitted. BFO frequency residuals were recorded as diagnostics under the frozen calibration and did not select these later flights. Values between these checkpoints are not reconstructed by this viewer.</p>' +
      (event && event.position ? '<p>Saved engine-fuel exhaustion position: <b>' + position(event.position) + '</b>, geometric height ' + number(event.position.heightM, 1) + ' m. This is another airborne state, not an impact point.</p>' : '') +
      '<p>Returned by ' + f.sides.map(function (s) { return s === 'L' ? 'the left search' : 'the right search'; }).join(' and ') + '. ' + f.sourceRows.map(function (r) { return '<a href="' + esc(r.url) + '" target="_blank" rel="noopener">' + esc(r.side) + ' source record ↗</a>'; }).join(' · ') + '</p></details>';
    return html;
  }
  function renderDetail() {
    var c = byConfig.get(state.configId);
    if (!c) {
      $('#cp-detail').innerHTML = '<h3>No matching configuration</h3><p>Change or clear the filters to inspect a saved result.</p>';
      return;
    }
    var a = byArrival.get(c.arrival);
    var flights = c.flightIds.map(function (id) { return byFlight.get(id); });
    if (!c.flightIds.includes(state.flightId)) state.flightId = c.flightIds[0] || null;
    var html = '<p class="eyebrow">SELECTED TEST</p><h3>' + esc(c.id) + '</h3><p class="cp-description">' + esc(c.arrival) + ' holds Mach <b>' + number(c.mach, 2) + '</b> ' + (c.kind === 'UNCHANGED_LEVEL_CONTROL' ? 'at its incoming level of ' : 'after a climb started at 19:41 to ') + '<b>' + number(c.levelFt, 0) + ' ft pressure altitude</b>.</p>' +
      '<span class="cp-result-tag' + (c.accepted ? '' : ' cp-none') + '">' + (c.accepted ? 'Accepted flight found' : 'No accepted flight in the completed search') + '</span>' +
      '<div class="cp-direction-list">' + direction(c.left, 'Left') + direction(c.right, 'Right') + '</div>';
    if (flights.length) html += '<label class="cp-flight-select">Choose a distinct returned flight (' + flights.length + ')<select id="cp-flight">' + flights.map(function (f) { return '<option value="' + esc(f.id) + '"' + (f.id === state.flightId ? ' selected' : '') + '>' + esc(f.id) + (f.rangeEnd ? ' · range end' : '') + (f.check.performed ? ' · repeated at half step' : '') + '</option>'; }).join('') + '</select></label><div id="cp-flight-details">' + flightDetails(byFlight.get(state.flightId)) + '</div>';
    else html += '<p>No returned flight meets all three timing bands with engine fuel at 00:11. The separate left and right endings above explain what each bounded search found; they are not a proof about every pair of turns.</p>';
    html += trialDetails(c);
    if (a) html += '<details><summary>The starting state at 19:41:03</summary><p>Position: ' + position({latitude:a.latitude1941, longitude:a.longitude1941}) + '. Incoming pressure altitude: ' + number(a.incomingAltitudeFt, 0) + ' ft. Fuel: ' + number(a.fuel1941Kg, 3) + ' kg; mass: ' + number(a.mass1941Kg, 1) + ' kg; course: ' + number(a.course1941, 3) + '°.</p><p><a href="' + esc(a.sourceUrl) + '" target="_blank" rel="noopener">Starting-state source row ↗</a></p></details>';
    html += '<p><a href="' + esc(c.sourceUrl) + '" target="_blank" rel="noopener">Configuration source row ↗</a></p>';
    $('#cp-detail').innerHTML = html;
    if ($('#cp-flight')) $('#cp-flight').addEventListener('change', function () {
      state.flightId = this.value;
      $('#cp-flight-details').innerHTML = flightDetails(byFlight.get(state.flightId));
      drawMap();
    });
  }
  function renderRows() {
    var list = filtered();
    var pages = Math.max(1, Math.ceil(list.length / pageSize));
    state.page = Math.min(state.page, pages - 1);
    $('#cp-filter-count').textContent = list.length + ' configurations shown · ' + list.filter(function (c) { return c.accepted; }).length + ' with an accepted flight · ' + list.filter(function (c) { return !c.accepted; }).length + ' without an accepted flight in the completed search';
    var rows = list.slice(state.page * pageSize, (state.page + 1) * pageSize);
    $('#cp-config-rows').innerHTML = rows.length ? rows.map(function (c) {
      return '<tr' + (c.id === state.configId ? ' class="cp-selected"' : '') + '><td><button type="button" data-cp-config="' + esc(c.id) + '" aria-label="Inspect ' + esc(c.id) + '">' + esc(c.arrival) + '</button><small>Mach ' + number(c.mach, 2) + '</small></td><td>' + number(c.levelFt, 0) + ' ft<small>' + (c.kind === 'UNCHANGED_LEVEL_CONTROL' ? 'Incoming level' : 'Climb at 19:41') + '</small></td><td><span class="cp-result-tag' + (c.accepted ? '' : ' cp-none') + '">' + (c.accepted ? 'Accepted' : 'None found') + '</span></td><td>' + c.flightIds.length + '</td></tr>';
    }).join('') : '<tr><td colspan="4" class="cp-empty">No configurations match these filters. No untested case is being counted as a failed search.</td></tr>';
    $('#cp-page').textContent = 'Page ' + (state.page + 1) + ' of ' + pages + (list.length ? ' · ' + (state.page * pageSize + 1) + '–' + Math.min((state.page + 1) * pageSize, list.length) + ' of ' + list.length : '');
    $('#cp-prev').disabled = state.page === 0;
    $('#cp-next').disabled = state.page >= pages - 1;
  }
  function selectConfig(id, flightId, scroll) {
    var list = filtered(), index = list.findIndex(function (c) { return c.id === id; });
    if (index < 0) return;
    state.configId = id; state.flightId = flightId || null; state.page = Math.floor(index / pageSize);
    renderRows(); renderDetail(); drawMap();
    if (scroll) $('#cp-detail').scrollIntoView({block:'nearest', behavior:'smooth'});
  }
  $('#cp-config-rows').addEventListener('click', function (event) {
    var button = event.target.closest('[data-cp-config]');
    if (button) selectConfig(button.dataset.cpConfig, null, false);
  });
  function filterChange() {
    state.page = 0;
    ['group', 'level', 'result', 'arrival'].forEach(function (key) { state[key] = $('#cp-' + key).value; });
    var list = filtered();
    if (!list.some(function (c) { return c.id === state.configId; })) { state.configId = list.length ? list[0].id : null; state.flightId = null; }
    $('#cp-overlap').hidden = true;
    renderRows(); renderDetail(); drawMap();
  }
  ['group', 'level', 'result', 'arrival'].forEach(function (key) { $('#cp-' + key).addEventListener('change', filterChange); });
  $('#cp-reset').addEventListener('click', function () { ['group', 'level', 'result', 'arrival'].forEach(function (key) { $('#cp-' + key).value = ''; }); filterChange(); });
  $('#cp-prev').addEventListener('click', function () { state.page--; renderRows(); });
  $('#cp-next').addEventListener('click', function () { state.page++; renderRows(); });
  var mapFlights = [];
  var mapX = function (lon) { return 78 + (lon - 90) * 68.75; };
  var mapY = function (lat) { return 35 + (-30 - lat) * 82; };
  function drawMap() {
    var ids = new Set(filtered().flatMap(function (c) { return c.flightIds; }));
    mapFlights = D.flights.filter(function (f) { return ids.has(f.id); });
    $('#cp-map-count').textContent = mapFlights.length + ' distinct flights';
    var h = '<svg viewBox="0 0 640 600" role="img" aria-labelledby="cp-plot-title cp-plot-desc"><title id="cp-plot-title">Recorded aircraft positions at 00:11 UTC</title><desc id="cp-plot-desc">All points are airborne saved model states. Blue circles mark Mach 0.67, orange squares Mach 0.75 and purple diamonds Mach 0.78. Use the configuration table and flight selector for every exact record.</desc><rect x="78" y="35" width="481.25" height="492" fill="#f8fbfb"/>';
    for (var lon = 90; lon <= 97; lon++) h += '<line class="cp-plot-grid" x1="' + mapX(lon) + '" y1="35" x2="' + mapX(lon) + '" y2="527"/><text x="' + mapX(lon) + '" y="549" text-anchor="middle">' + lon + '°E</text>';
    for (var lat = -30; lat >= -36; lat--) h += '<line class="cp-plot-grid" x1="78" y1="' + mapY(lat) + '" x2="559.25" y2="' + mapY(lat) + '"/><text x="66" y="' + (mapY(lat) + 4) + '" text-anchor="end">' + Math.abs(lat) + '°S</text>';
    h += '<text x="320" y="582" text-anchor="middle">Longitude · latitude positions at 00:11</text>';
    mapFlights.forEach(function (f) {
      var x = mapX(f.position0011.longitude), y = mapY(f.position0011.latitude), title = '<title>' + esc(f.id) + ' · ' + position(f.position0011) + '</title>';
      if (f.mach === .67) h += '<circle cx="' + x + '" cy="' + y + '" r="4" fill="#165d91" stroke="#fff" stroke-width=".6">' + title + '</circle>';
      else if (f.mach === .75) h += '<rect class="cp-marker" x="' + (x - 3.7) + '" y="' + (y - 3.7) + '" width="7.4" height="7.4" fill="#a36516" stroke="#fff" stroke-width=".6">' + title + '</rect>';
      else h += '<path class="cp-marker" d="M' + x + ' ' + (y - 5) + 'L' + (x + 5) + ' ' + y + 'L' + x + ' ' + (y + 5) + 'L' + (x - 5) + ' ' + y + 'Z" fill="#735696" stroke="#fff" stroke-width=".6">' + title + '</path>';
    });
    var selected = byFlight.get(state.flightId);
    if (selected && ids.has(selected.id)) h += '<circle class="cp-highlight" cx="' + mapX(selected.position0011.longitude) + '" cy="' + mapY(selected.position0011.latitude) + '" r="10"/>';
    if (!mapFlights.length) h += '<text x="320" y="284" text-anchor="middle">No accepted-flight positions in this filtered selection.</text>';
    $('#cp-map').innerHTML = h + '</svg>';
  }
  $('#cp-map').addEventListener('click', function (event) {
    var svg = $('#cp-map svg'), r = svg.getBoundingClientRect();
    if (!r.width || !r.height) return;
    var x = (event.clientX - r.left) * 640 / r.width, y = (event.clientY - r.top) * 600 / r.height;
    var near = mapFlights.map(function (f) { return {flight:f, distance:Math.hypot(mapX(f.position0011.longitude) - x, mapY(f.position0011.latitude) - y)}; }).filter(function (p) { return p.distance <= 12; }).sort(function (a, b) { return a.distance - b.distance || a.flight.id.localeCompare(b.flight.id); });
    if (!near.length) { $('#cp-overlap').hidden = true; return; }
    if (near.length === 1) { $('#cp-overlap').hidden = true; selectConfig(near[0].flight.configId, near[0].flight.id, true); return; }
    $('#cp-overlap').hidden = false;
    $('#cp-overlap').innerHTML = '<label>' + near.length + ' saved flights overlap near this point. Choose a record:<select id="cp-overlap-flight"><option value="">Select a flight…</option>' + near.map(function (p) { return '<option value="' + esc(p.flight.id) + '">' + esc(p.flight.id) + ' · ' + number(p.flight.levelFt, 0) + ' ft · ' + position(p.flight.position0011) + '</option>'; }).join('') + '</select></label>';
    $('#cp-overlap-flight').addEventListener('change', function () { var f = byFlight.get(this.value); if (f) selectConfig(f.configId, f.id, true); });
  });
  var sourceNames = [
    ['PROD_CONFIGURATIONS.csv', 'All 424 configurations · CSV'],
    ['PROD_DIRECTIONS.csv', 'All 848 directional searches · CSV'],
    ['PROD_SOLUTIONS.csv', 'All returned records · CSV'],
    ['PROD_NUMERICAL_CHECKS.csv', 'Numerical checks · CSV'],
    ['ARRIVALS_108.csv', 'All starting states · CSV'],
    ['FINDINGS.md', 'Final findings · text']
  ];
  $('#cp-downloads').innerHTML = '<div class="cp-downloads"><a href="data/cruise-production-108/catalogue.json" download>266-flight viewer catalogue · JSON ↓</a>' +
    sourceNames.map(function (p) { return '<a href="data/cruise-production-108/sources/' + p[0] + '" download>' + esc(p[1]) + ' ↓</a>'; }).join('') +
    '<a href="data/cruise-production-108/source_manifest.json" download>Source hashes · JSON ↓</a></div><p class="cp-source-id">Source commit <code>' + esc(D.provenance.commit) + '</code> · Runner revision <code>' + esc(D.provenance.runnerRevision) + '</code>. <a href="' + esc(D.provenance.sourceBaseUrl.replace(/\/$/, '') + '/FINDINGS.md') + '" target="_blank" rel="noopener">Pinned findings ↗</a>. One flight returned by both directions is counted once here: 266 distinct flights, 267 directional solution records. The source CSV also retains duplicate return entries.</p>';
  groupTable(); filterChange();
  window.CRUISE_LAB = {version:'1.0', getState:function () { return Object.assign({}, state, {catalogue:catalogue, filteredConfigurations:filtered().length, plottedFlights:mapFlights.length}); }, counts:D.summary};
})();
