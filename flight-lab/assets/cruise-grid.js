/* Saved configurations only. No flight calculation or interpolation. */
(function (global) {
  'use strict';
  var D = global.CRUISE_PRODUCTION_108, lab = global.CRUISE_LAB;
  var $ = function (selector) { return document.querySelector(selector); };
  var canvas = $('#cp-grid-canvas');
  if (!canvas || !D || !lab || typeof global.Scene3D !== 'function') return;

  var levels = [25661, 27830, 29987, 30053, 31946, 33985];
  var machs = [.67, .75, .78];
  var arrivals = D.arrivals.map(function (a) { return a.id; });
  var byId = new Map(D.configurations.map(function (c) { return [c.id, c]; }));
  var categories = {
    accepted: {label: 'Accepted flight found', symbol: '●', shape: 'circle', color: '#175d91'},
    'lift-stop': {label: 'No accepted flight · model lift-margin stop', symbol: '×', shape: 'cross', color: '#755391'},
    'fuel-exhausted': {label: 'No accepted flight · fuel-exhaustion ending', symbol: '■', shape: 'square', color: '#aa6a18'},
    'no-joint-match': {label: 'No accepted flight · timing and fuel not met together', symbol: '◆', shape: 'diamond', color: '#4e6974'}
  };
  var order = ['accepted', 'lift-stop', 'fuel-exhausted', 'no-joint-match'];
  var visibleIds = new Set(), counts = {}, selectedId = null;
  var esc = function (s) { return String(s).replace(/[&<>"']/g, function (c) { return {'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[c]; }); };
  var number = function (n) { return n.toLocaleString('en-US'); };
  var category = function (c) {
    if (c.accepted) return 'accepted';
    var endings = [c.left.ending, c.right.ending];
    if (endings.every(function (e) { return e === 'STOPPED_AT_AN_AIRCRAFT_LIMIT_OF_THE_PERFORMANCE_MODEL'; })) return 'lift-stop';
    if (endings.some(function (e) { return e === 'FUEL_EXHAUSTED_BEFORE_THE_FIT_TIME_ON_EVERY_TRIAL_FLIGHT'; }) &&
        endings.every(function (e) { return e === 'FUEL_EXHAUSTED_BEFORE_THE_FIT_TIME_ON_EVERY_TRIAL_FLIGHT' || e === 'NO_STARTING_POINT'; })) return 'fuel-exhausted';
    return 'no-joint-match';
  };
  var point = function (c) {
    return [(c.mach - .67) / .11 * 12, levels.indexOf(c.levelFt) * 2, arrivals.indexOf(c.arrival) / (arrivals.length - 1) * 14];
  };
  var defaultZoom = function () { return (canvas.getBoundingClientRect().width || 500) < 420 ? .88 : 1.10; };
  var defaults = {center: [6, 5, 7], radius: 11.5, yaw: -.71, pitch: .45, zoom: defaultZoom()};
  var renderer = new global.Scene3D(canvas, Object.assign({}, defaults, {
    onPick: function (id) { hideChooser(); if (id && visibleIds.has(id)) lab.selectConfiguration(id); },
    onPickCandidates: function (ids) { showChooser(ids); },
    onHover: function (id, item, event) { showTooltip(id, event); }
  }));

  function hideChooser() {
    var node = $('#cp-grid-overlap');
    if (node) { node.hidden = true; node.innerHTML = ''; }
  }
  function showChooser(ids) {
    var unique = Array.from(new Set(ids)).filter(function (id) { return visibleIds.has(id); });
    if (unique.length < 2) {
      hideChooser();
      if (unique.length) lab.selectConfiguration(unique[0]);
      return;
    }
    var node = $('#cp-grid-overlap');
    node.hidden = false;
    node.innerHTML = '<label for="cp-grid-overlap-select">' + unique.length + ' configurations overlap in this view. Choose the exact test:</label><select id="cp-grid-overlap-select"><option value="">Choose a configuration…</option>' + unique.map(function (id) {
      var c = byId.get(id);
      return '<option value="' + esc(id) + '">' + esc(id) + ' · Mach ' + c.mach.toFixed(2) + ' · ' + number(c.levelFt) + ' ft · ' + esc(categories[category(c)].label) + '</option>';
    }).join('') + '</select><p>Rotate the grid to separate the markers, or use the results table.</p>';
    $('#cp-grid-overlap-select').addEventListener('change', function () {
      var id = this.value;
      if (visibleIds.has(id)) { hideChooser(); lab.selectConfiguration(id); }
    });
  }
  function showTooltip(id, event) {
    var node = $('#cp-grid-tooltip'), c = byId.get(id);
    if (!node) return;
    if (!c || !visibleIds.has(id) || !event) { node.hidden = true; return; }
    node.textContent = c.id + ' · Mach ' + c.mach.toFixed(2) + ' · ' + number(c.levelFt) + ' ft\n' + categories[category(c)].label;
    var rect = canvas.getBoundingClientRect();
    node.style.left = Math.max(8, Math.min(event.clientX - rect.left + 12, rect.width - 248)) + 'px';
    node.style.top = Math.max(8, Math.min(event.clientY - rect.top + 12, rect.height - 78)) + 'px';
    node.hidden = false;
  }
  function axes() {
    var scene = {points: [], lines: [], polygons: [], labels: []};
    var label = function (p, text, options) {
      scene.labels.push(Object.assign({p:p, text:text, color:'#294652', halo:'#f7f4e9', font:'Tahoma, Arial, sans-serif', size:11, weight:500}, options || {}));
    };
    var line = function (a, b, major) {
      scene.lines.push({a:a, b:b, color:major ? '#4d6a76' : '#c9d2cf', width:major ? 1.5 : .8});
    };
    // Grid lines describe display axes, never paths between aircraft states.
    levels.forEach(function (ft, index) {
      var y = index * 2;
      line([0,y,0], [12,y,0]); line([0,y,0], [0,y,14]);
      label([0,y,0], number(ft), {align:'right', dx:-11});
    });
    machs.forEach(function (mach) {
      var x = (mach - .67) / .11 * 12;
      line([x,0,0], [x,0,14]);
      line([x,0,14], [x,10,14]);
      label([x,0,0], mach.toFixed(2), {dy:19});
    });
    [0,27,54,81,107].forEach(function (index) {
      var z = index / 107 * 14;
      line([0,0,z], [12,0,z]);
      label([12,0,z], arrivals[index], {align:'left', dx:9, dy:8});
    });
    line([0,0,0], [12,0,0], true);
    line([0,0,0], [0,10,0], true);
    line([12,0,0], [12,0,14], true);
    label([5,0,0], 'Cruise Mach', {dy:38, weight:700});
    label([0,10,0], 'Tested level (ft)', {dy:-21, align:'left', weight:700});
    label([12,0,8], 'Starting arrival', {dx:16, dy:32, align:'center', weight:700});
    return scene;
  }
  function refresh() {
    var filtered = lab.getFilteredConfigurations(), state = lab.getState();
    visibleIds = new Set(filtered.map(function (c) { return c.id; }));
    selectedId = visibleIds.has(state.configId) ? state.configId : null;
    counts = Object.fromEntries(order.map(function (key) { return [key, 0]; }));
    var scene = axes();
    filtered.forEach(function (c) {
      var key = category(c), style = categories[key];
      counts[key]++;
      scene.points.push({id:c.id, p:point(c), size:3.9, shape:style.shape, color:style.color, stroke:style.shape === 'cross' ? style.color : '#fffdf4', strokeWidth:style.shape === 'cross' ? 1.8 : .7, category:key});
    });
    if (selectedId) {
      var chosen = byId.get(selectedId), style = categories[category(chosen)];
      scene.points.push({id:selectedId, p:point(chosen), size:8, shape:style.shape, color:'rgba(255,253,244,0.22)', stroke:'#172d37', strokeWidth:2.1, selected:true});
    }
    renderer.setScene(scene);
    $('#cp-grid-count').textContent = filtered.length + ' tested configurations · ' + counts.accepted + ' with an accepted flight';
    $('#cp-grid-legend').innerHTML = order.map(function (key) {
      var style = categories[key];
      return '<span><b class="cp-grid-key cp-grid-key-' + key + '" aria-hidden="true">' + style.symbol + '</b>' + esc(style.label) + ' <strong>(' + counts[key] + ')</strong></span>';
    }).join('');
    $('#cp-grid-caption').textContent = (selectedId ? 'Selected: ' + selectedId + '. ' : '') + 'Each marker is one tested arrival-and-level configuration; click it for the two search endings and its returned flights. The level axis shows the incoming or target pressure level, with six equally spaced display rows. A stopped climb may not have reached that target. Arrival IDs label starting states, not time or distance. Blank combinations are not counted as failed tests.';
    canvas.setAttribute('aria-label', '3D tested-scenario grid. ' + filtered.length + ' configurations, ' + counts.accepted + ' with an accepted flight. Axes: cruise Mach, six equally spaced tested pressure levels, and starting arrival ID. Drag or use arrow keys to rotate, plus and minus to zoom. Use the results table to select records without the plot.');
    hideChooser();
    showTooltip(null);
    if (state.catalogue === 'cruise' && state.view === 'grid') renderer.resize();
  }
  function bind(id, action) { var node = $('#' + id); if (node) node.addEventListener('click', action); }
  bind('cp-grid-reset', function () { renderer.setView(Object.assign({}, defaults, {zoom:defaultZoom()})); hideChooser(); });
  bind('cp-grid-top', function () { renderer.setView({yaw:0, pitch:1.42, zoom:1.12}); hideChooser(); });
  bind('cp-grid-front', function () { renderer.setView({yaw:0, pitch:.015, zoom:1.18}); hideChooser(); });
  bind('cp-grid-zoom-in', function () { renderer.setView({zoom:renderer.view.zoom * 1.15}); });
  bind('cp-grid-zoom-out', function () { renderer.setView({zoom:renderer.view.zoom / 1.15}); });
  global.addEventListener('atlas:cruise-state', refresh);
  global.addEventListener('atlas:catalogue', function () {
    var state = lab.getState();
    if (state.catalogue === 'cruise' && state.view === 'grid') renderer.resize();
  });
  global.CRUISE_GRID = {
    version:'1.0', renderer:renderer,
    configPoint:function (id) { var c = byId.get(id); return c ? point(c) : null; },
    getState:function () {
      return {
        ids:Array.from(visibleIds), selectedId:selectedId, counts:Object.assign({}, counts),
        categories:Object.fromEntries(Array.from(visibleIds).map(function (id) { return [id, category(byId.get(id))]; })),
        axes:{mach:machs.slice(), levels:levels.slice(), levelSpacing:'equally spaced categorical rows', arrivals:arrivals.slice()},
        view:Object.assign({}, renderer.view, {center:renderer.view.center.slice()})
      };
    }
  };
  refresh();
})(window);
