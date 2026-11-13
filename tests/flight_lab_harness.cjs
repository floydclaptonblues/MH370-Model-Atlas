// Non-browser DOM harness. The production projection, drawing traversal, hit regions,
// pointer handlers and controller all run; only Canvas2D rasterization and time are stubbed.
const { JSDOM } = require('jsdom');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');

const root = path.resolve(__dirname, '..');
const read = name => fs.readFileSync(path.join(root, name), 'utf8');

function createHarness({ width = 768, height = 480 } = {}) {
  const dom = new JSDOM(read('flight-lab.html'), {
    url: 'https://example.test/flight-lab.html',
    runScripts: 'outside-only'
  });
  const w = dom.window, timers = new Map(), frames = new Map(), errors = [];
  let next = 0, scene;
  const bounds = { width, height, left: 0, top: 0, right: width, bottom: height, x: 0, y: 0 };
  const noOp = () => {};
  const drawingContext = Object.fromEntries([
    'setTransform', 'clearRect', 'fillRect', 'beginPath', 'moveTo', 'lineTo',
    'closePath', 'fill', 'stroke', 'rect', 'arc', 'save', 'restore',
    'strokeText', 'fillText', 'setLineDash', 'drawImage'
  ].map(name => [name, noOp]));
  drawingContext.measureText = text => ({ width: String(text).length * 6 });
  w.HTMLCanvasElement.prototype.getContext = () => drawingContext;
  w.HTMLCanvasElement.prototype.getBoundingClientRect = () => ({ ...bounds });
  Object.defineProperties(w.HTMLCanvasElement.prototype, {
    clientWidth: { get: () => bounds.width },
    clientHeight: { get: () => bounds.height }
  });
  w.HTMLElement.prototype.scrollIntoView = noOp;
  w.setInterval = fn => { const id = ++next; timers.set(id, fn); return id; };
  w.clearInterval = id => timers.delete(id);
  w.requestAnimationFrame = fn => { const id = ++next; frames.set(id, fn); return id; };
  w.cancelAnimationFrame = id => frames.delete(id);
  w.addEventListener('error', e => { errors.push(e.error || e.message); e.preventDefault(); });
  w.eval(read('flight-lab/assets/data.js'));
  const dataBefore = JSON.stringify(w.MH370_DATA);
  w.eval(read('flight-lab/assets/scene3d.js'));
  const Renderer = w.Scene3D;
  // Capture the real instance without replacing any renderer method.
  w.Scene3D = class extends Renderer {
    constructor(...args) { super(...args); scene = this; }
  };
  w.eval(read('flight-lab/assets/app.js'));

  function flush() {
    for (let count = 0; frames.size; count++) {
      assert(count < 20, 'renderer animation frames settle');
      const pending = [...frames.values()]; frames.clear();
      pending.forEach(fn => fn(0));
    }
    if (errors.length) throw errors.shift();
  }
  const $ = selector => w.document.querySelector(selector);
  const $$ = selector => [...w.document.querySelectorAll(selector)];
  function required(selector) {
    const el = typeof selector === 'string' ? $(selector) : selector;
    assert(el, 'control exists: ' + selector);
    return el;
  }
  function click(selector) { required(selector).click(); flush(); }
  function input(selector, value, type = 'input') {
    const el = required(selector); el.value = value;
    el.dispatchEvent(new w.Event(type, { bubbles: true })); flush();
  }
  function tick() { [...timers.values()].forEach(fn => fn()); flush(); }
  function pointerClick(x, y) {
    const canvas = required('#scene');
    for (const type of ['pointerdown', 'pointerup']) {
      const event = new w.MouseEvent(type, { bubbles: true, clientX: x, clientY: y, button: 0 });
      Object.defineProperties(event, { pointerId: { value: 1 }, pointerType: { value: 'mouse' } });
      canvas.dispatchEvent(event);
    }
    flush();
  }
  function resize(newWidth, newHeight) {
    Object.assign(bounds, { width: newWidth, height: newHeight, right: newWidth, bottom: newHeight });
    scene.resize(); flush();
  }
  flush();
  return {
    w, dom, Renderer, $, $$, click, input, tick, pointerClick, resize, flush, timers,
    get scene() { return scene; },
    state: () => w.FLIGHT_LAB.getState(),
    dataUnchanged: () => JSON.stringify(w.MH370_DATA) === dataBefore,
    close: () => { scene.destroy(); dom.window.close(); }
  };
}

module.exports = { createHarness };
