/* MH370 Flight Dynamics Lab — dependency-free perspective canvas renderer.
   x is horizontal, y is up, z is depth. Geometry uses scene units;
   glyph radii, line widths and label sizes use CSS pixels. */
(function (global) {
  'use strict';

  const clamp = (n, a, b) => Math.max(a, Math.min(b, n));
  const validPoint = p => Array.isArray(p) && p.length >= 3 && p.slice(0, 3).every(Number.isFinite);
  const emptyScene = () => ({ points: [], lines: [], polygons: [], labels: [] });

  class Scene3D {
    constructor(canvas, options = {}) {
      if (!canvas || !canvas.getContext) throw new TypeError('Scene3D requires a canvas.');
      this.canvas = canvas;
      this.ctx = canvas.getContext('2d', { alpha: true });
      this.options = options;
      this.view = {
        radius: options.radius || 10,
        center: (options.center || [0, 0, 0]).slice(),
        yaw: options.yaw ?? -0.65,
        pitch: options.pitch ?? 0.48,
        zoom: options.zoom ?? 1
      };
      this.initialView = { ...this.view, center: this.view.center.slice() };
      this.scene = emptyScene();
      this.onPick = options.onPick || null;
      this.onPickCandidates = options.onPickCandidates || null;
      this.onHover = options.onHover || null;
      this.onViewChange = options.onViewChange || null;
      this.width = 1;
      this.height = 1;
      this.hitRegions = [];
      this._pointers = new Map();
      this._drag = null;
      this._frame = 0;
      this._destroyed = false;
      this._events = [];
      this._hoverId = undefined;
      canvas.style.touchAction = 'none';
      if (!canvas.hasAttribute('tabindex')) canvas.tabIndex = 0;
      this._bind();
      this._observer = typeof ResizeObserver === 'function' ? new ResizeObserver(() => this.resize()) : null;
      this._observer?.observe(canvas);
      this.resize();
    }

    _listen(target, type, fn, opts) {
      target.addEventListener(type, fn, opts);
      this._events.push([target, type, fn, opts]);
    }

    _bind() {
      const c = this.canvas;
      this._listen(c, 'pointerdown', e => {
        if (e.button !== 0 && e.pointerType !== 'touch') return;
        c.focus({ preventScroll: true });
        c.setPointerCapture?.(e.pointerId);
        this._pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
        if (this._pointers.size === 1) {
          this._drag = { x: e.clientX, y: e.clientY, startX: e.clientX, startY: e.clientY, moved: false, multi: false };
        } else if (this._pointers.size === 2) {
          this._drag.multi = true;
          this._pinch = this._pointerDistance();
        }
        c.style.cursor = 'grabbing';
      });
      this._listen(c, 'pointermove', e => {
        if (this._pointers.has(e.pointerId) && this._drag) {
          const last = this._pointers.get(e.pointerId);
          this._pointers.set(e.pointerId, { x: e.clientX, y: e.clientY });
          if (this._pointers.size === 2) {
            const distance = this._pointerDistance();
            if (this._pinch > 1) this.view.zoom = clamp(this.view.zoom * distance / this._pinch, 0.35, 4);
            this._pinch = distance;
            this._drag.moved = true;
          } else {
            this.view.yaw -= (e.clientX - last.x) * 0.007;
            this.view.pitch = clamp(this.view.pitch + (e.clientY - last.y) * 0.007, -1.45, 1.45);
            if (Math.hypot(e.clientX - this._drag.startX, e.clientY - this._drag.startY) > 4) this._drag.moved = true;
          }
          this._changed();
        } else if (!this._pointers.size) {
          const hit = this._hitAtEvent(e);
          c.style.cursor = hit ? 'pointer' : 'grab';
          const id = hit?.item.id;
          if (id !== this._hoverId) {
            this._hoverId = id;
            this.onHover?.(id ?? null, hit?.item ?? null, e);
          }
        }
      });
      const endPointer = e => {
        if (!this._pointers.has(e.pointerId)) return;
        const didClick = this._pointers.size === 1 && this._drag && !this._drag.moved && !this._drag.multi && e.type === 'pointerup';
        this._pointers.delete(e.pointerId);
        if (didClick) {
          const hits = this._hitCandidatesAtEvent(e);
          if (hits.length > 1 && this.onPickCandidates) {
            this.onPickCandidates(hits.map(hit => hit.item.id), hits, e);
          } else {
            const hit = hits[0];
            this.onPick?.(hit?.item.id ?? null, hit?.item ?? null, e);
          }
        }
        if (!this._pointers.size) {
          this._drag = null;
          c.style.cursor = 'grab';
        }
        if (c.hasPointerCapture?.(e.pointerId)) c.releasePointerCapture(e.pointerId);
      };
      this._listen(c, 'pointerup', endPointer);
      this._listen(c, 'pointercancel', endPointer);
      this._listen(c, 'pointerleave', e => {
        if (!this._pointers.size) {
          this._hoverId = undefined;
          this.onHover?.(null, null, e);
        }
      });
      this._listen(c, 'wheel', e => {
        // A focused scene consumes the wheel; an unfocused one leaves page scrolling alone.
        if (global.document?.activeElement !== c) return;
        e.preventDefault();
        this.view.zoom = clamp(this.view.zoom * Math.exp(-e.deltaY * 0.0012), 0.35, 4);
        this._changed();
      }, { passive: false });
      this._listen(c, 'keydown', e => {
        let handled = true;
        switch (e.key) {
          case 'ArrowLeft': this.view.yaw += 0.10; break;
          case 'ArrowRight': this.view.yaw -= 0.10; break;
          case 'ArrowUp': this.view.pitch = clamp(this.view.pitch + 0.10, -1.45, 1.45); break;
          case 'ArrowDown': this.view.pitch = clamp(this.view.pitch - 0.10, -1.45, 1.45); break;
          case '+': case '=': this.view.zoom = clamp(this.view.zoom * 1.12, 0.35, 4); break;
          case '-': case '_': this.view.zoom = clamp(this.view.zoom / 1.12, 0.35, 4); break;
          case 'Home': case 'r': case 'R': this.reset(); break;
          default: handled = false;
        }
        if (handled) { e.preventDefault(); this._changed(); }
      });
      if (!this._observer && global.addEventListener) this._listen(global, 'resize', () => this.resize());
    }

    _pointerDistance() {
      const a = Array.from(this._pointers.values());
      return a.length > 1 ? Math.hypot(a[0].x - a[1].x, a[0].y - a[1].y) : 0;
    }

    _changed() { this.render(); this.onViewChange?.({ ...this.view }); }

    setScene(scene = {}) {
      this.scene = { ...emptyScene(), ...scene };
      if (scene.center) this.view.center = scene.center.slice();
      if (Number.isFinite(scene.radius) && scene.radius > 0) this.view.radius = scene.radius;
      if (this.options.autoFit) this.fit();
      this.render();
      return this;
    }

    setView(view = {}) {
      for (const k of ['yaw', 'pitch', 'zoom', 'radius']) if (Number.isFinite(view[k])) this.view[k] = view[k];
      this.view.pitch = clamp(this.view.pitch, -1.45, 1.45);
      this.view.zoom = clamp(this.view.zoom, 0.35, 4);
      this.view.radius = Math.max(0.001, this.view.radius);
      if (validPoint(view.center)) this.view.center = view.center.slice();
      this._changed();
      return this;
    }

    reset() {
      this.view = { ...this.initialView, center: this.initialView.center.slice() };
      this._changed();
      return this;
    }

    fit(padding = 1.12) {
      const pts = [];
      for (const p of this.scene.points) if (validPoint(p.p)) pts.push(p.p);
      for (const l of this.scene.lines) { if (validPoint(l.a)) pts.push(l.a); if (validPoint(l.b)) pts.push(l.b); }
      for (const poly of this.scene.polygons) for (const p of poly.vertices || []) if (validPoint(p)) pts.push(p);
      if (!pts.length) return this;
      const min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
      for (const p of pts) for (let k = 0; k < 3; k++) { min[k] = Math.min(min[k], p[k]); max[k] = Math.max(max[k], p[k]); }
      this.view.center = min.map((v, k) => (v + max[k]) / 2);
      this.view.radius = Math.max(0.01, ...pts.map(p => Math.hypot(...p.map((v, k) => v - this.view.center[k])))) * padding;
      this.render();
      return this;
    }

    resize() {
      if (this._destroyed) return;
      const rect = this.canvas.getBoundingClientRect();
      this.width = Math.max(1, rect.width);
      this.height = Math.max(1, rect.height);
      this.dpr = Math.min(2, global.devicePixelRatio || 1);
      const w = Math.round(this.width * this.dpr), h = Math.round(this.height * this.dpr);
      if (this.canvas.width !== w) this.canvas.width = w;
      if (this.canvas.height !== h) this.canvas.height = h;
      this.render();
    }

    _camera() {
      const v = this.view, sy = Math.sin(v.yaw), cy = Math.cos(v.yaw), sp = Math.sin(v.pitch), cp = Math.cos(v.pitch);
      return {
        right: [cy, 0, -sy], up: [-sy * sp, cp, -cy * sp], normal: [sy * cp, sp, cy * cp],
        distance: v.radius * 3.25 / v.zoom,
        focal: Math.min(this.width, this.height) / (2 * Math.tan((this.options.fov || 40) * Math.PI / 360)),
        near: Math.max(0.005, v.radius * 0.025)
      };
    }

    project(p, camera) {
      if (!validPoint(p)) return { x: NaN, y: NaN, depth: NaN, visible: false, scale: 0 };
      const c = camera || this._camera(), q = p.map((v, k) => v - this.view.center[k]);
      const dot = a => q[0] * a[0] + q[1] * a[1] + q[2] * a[2];
      const depth = c.distance - dot(c.normal), scale = c.focal / depth;
      return {
        x: this.width / 2 + dot(c.right) * scale,
        y: this.height / 2 - dot(c.up) * scale,
        depth, scale, visible: depth > c.near
      };
    }

    render() {
      if (this._destroyed || this._frame) return;
      this._frame = global.requestAnimationFrame(() => { this._frame = 0; this._draw(); });
    }

    _draw() {
      const ctx = this.ctx, camera = this._camera(), list = [];
      ctx.setTransform(this.dpr, 0, 0, this.dpr, 0, 0);
      ctx.clearRect(0, 0, this.width, this.height);
      this.hitRegions = [];
      for (const p of this.scene.points || []) {
        const s = this.project(p.p, camera);
        if (s.visible && s.x > -30 && s.y > -30 && s.x < this.width + 30 && s.y < this.height + 30) list.push({ type: 'point', item: p, s, depth: s.depth });
      }
      for (const l of this.scene.lines || []) {
        const a = this.project(l.a, camera), b = this.project(l.b, camera);
        if (a.visible && b.visible) list.push({ type: 'line', item: l, a, b, depth: (a.depth + b.depth) / 2 });
      }
      for (const p of this.scene.polygons || []) {
        const vertices = (p.vertices || []).map(v => this.project(v, camera));
        if (vertices.length > 2 && vertices.every(v => v.visible)) list.push({ type: 'polygon', item: p, vertices, depth: vertices.reduce((s, v) => s + v.depth, 0) / vertices.length });
      }
      list.sort((a, b) => b.depth - a.depth);
      for (const prim of list) {
        const p = prim.item;
        ctx.globalAlpha = p.opacity ?? 1;
        if (prim.type === 'point') this._drawPoint(prim);
        else if (prim.type === 'line') this._drawLine(prim);
        else {
          ctx.beginPath();
          prim.vertices.forEach((v, k) => k ? ctx.lineTo(v.x, v.y) : ctx.moveTo(v.x, v.y));
          ctx.closePath();
          ctx.fillStyle = p.color || '#a9bac5';
          ctx.fill();
          if (p.stroke) { ctx.strokeStyle = p.stroke; ctx.lineWidth = p.width || 1; ctx.stroke(); }
        }
      }
      ctx.globalAlpha = 1;
      for (const label of this.scene.labels || []) {
        const s = this.project(label.p, camera);
        if (!s.visible) continue;
        ctx.save();
        ctx.globalAlpha = label.opacity ?? 1;
        ctx.font = `${label.weight || 500} ${label.size || 12}px ${label.font || 'system-ui, sans-serif'}`;
        ctx.textAlign = label.align || 'center';
        ctx.textBaseline = label.baseline || 'middle';
        ctx.lineJoin = 'round';
        if (label.halo !== false) { ctx.strokeStyle = label.halo || '#142432'; ctx.lineWidth = 4; ctx.strokeText(label.text, s.x + (label.dx || 0), s.y + (label.dy || 0)); }
        ctx.fillStyle = label.color || '#d2dde1';
        ctx.fillText(label.text, s.x + (label.dx || 0), s.y + (label.dy || 0));
        ctx.restore();
      }
      ctx.setLineDash([]);
      ctx.globalAlpha = 1;
    }

    _drawPoint(prim) {
      const { item: p, s } = prim, ctx = this.ctx, r = p.size ?? 3;
      ctx.beginPath();
      switch (p.shape) {
        case 'square': ctx.rect(s.x - r, s.y - r, r * 2, r * 2); break;
        case 'diamond': ctx.moveTo(s.x, s.y - r * 1.4); ctx.lineTo(s.x + r, s.y); ctx.lineTo(s.x, s.y + r * 1.4); ctx.lineTo(s.x - r, s.y); ctx.closePath(); break;
        case 'triangle': ctx.moveTo(s.x, s.y - r * 1.4); ctx.lineTo(s.x + r * 1.2, s.y + r); ctx.lineTo(s.x - r * 1.2, s.y + r); ctx.closePath(); break;
        case 'cross': ctx.moveTo(s.x - r, s.y - r); ctx.lineTo(s.x + r, s.y + r); ctx.moveTo(s.x + r, s.y - r); ctx.lineTo(s.x - r, s.y + r); break;
        default: ctx.arc(s.x, s.y, r, 0, Math.PI * 2);
      }
      if (p.shape !== 'cross') { ctx.fillStyle = p.color || '#a5c7db'; ctx.fill(); }
      if (p.stroke || p.shape === 'cross') { ctx.strokeStyle = p.stroke || p.color || '#a5c7db'; ctx.lineWidth = p.strokeWidth || 1.3; ctx.stroke(); }
      if (p.id != null) this.hitRegions.push({ x: s.x, y: s.y, radius: Math.max(r + 3, 6), depth: s.depth, item: p });
    }

    _drawLine(prim) {
      const { item: l, a, b } = prim, ctx = this.ctx;
      ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
      ctx.strokeStyle = l.color || '#506171';
      ctx.lineWidth = l.width || 1;
      ctx.setLineDash(l.dash || []);
      ctx.stroke(); ctx.setLineDash([]);
      if (l.arrow) {
        const angle = Math.atan2(b.y - a.y, b.x - a.x), length = l.arrowSize || Math.max(7, (l.width || 1) * 3.5);
        ctx.beginPath(); ctx.moveTo(b.x, b.y);
        ctx.lineTo(b.x - length * Math.cos(angle - 0.40), b.y - length * Math.sin(angle - 0.40));
        ctx.lineTo(b.x - length * Math.cos(angle + 0.40), b.y - length * Math.sin(angle + 0.40));
        ctx.closePath(); ctx.fillStyle = l.color || '#506171'; ctx.fill();
      }
    }

    // Pure lookup: one result per record, ordered by screen distance. A selected
    // overlay can repeat an ID, so it must not create a false ambiguity.
    static hitCandidates(hitRegions, x, y) {
      const byId = new Map();
      for (const hit of hitRegions) {
        if (hit.item?.id == null) continue;
        const distance = Math.hypot(x - hit.x, y - hit.y);
        if (!(distance <= hit.radius)) continue;
        const previous = byId.get(hit.item.id);
        if (!previous || distance < previous.distance ||
            (distance === previous.distance && hit.depth < previous.depth)) {
          byId.set(hit.item.id, { ...hit, distance });
        }
      }
      return [...byId.values()].sort((a, b) => a.distance - b.distance || a.depth - b.depth);
    }

    _hitCandidatesAtEvent(e) {
      const r = this.canvas.getBoundingClientRect();
      return Scene3D.hitCandidates(this.hitRegions, e.clientX - r.left, e.clientY - r.top);
    }

    _hitAtEvent(e) {
      const r = this.canvas.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
      let best = null, score = Infinity;
      for (const hit of this.hitRegions) {
        const distance = Math.hypot(x - hit.x, y - hit.y);
        if (distance <= hit.radius && (distance < score || (distance === score && hit.depth < (best?.depth ?? Infinity)))) { best = hit; score = distance; }
      }
      return best;
    }

    destroy() {
      this._destroyed = true;
      if (this._frame) global.cancelAnimationFrame(this._frame);
      this._observer?.disconnect();
      for (const [target, type, fn, opts] of this._events) target.removeEventListener(type, fn, opts);
      this._events = []; this.hitRegions = []; this._pointers.clear();
    }
  }

  global.Scene3D = Scene3D;
})(typeof window !== 'undefined' ? window : globalThis);
