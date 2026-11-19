// Validate geometry and interaction state without third-party dependencies.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const {spherePoints, rotate, project} = require('../assets/tool-globe.js');
const points = spherePoints(17);
for (const point of points) {
  assert.ok(Math.abs(Math.hypot(point.x, point.y, point.z) - 1) < 1e-12);
  for (const yaw of [0, .7, 4, 18]) for (const pitch of [-4, 0, .9]) {
    const rotated = rotate(point, yaw, pitch);
    assert.ok(Math.abs(Math.hypot(rotated.x, rotated.y, rotated.z) - 1) < 1e-12);
    for (const size of [240, 300, 540]) {
      const projected = project(rotated, size, 64);
      const half = 32 * projected.scale;
      assert.ok(projected.x - half >= 0 && projected.x + half <= size);
      assert.ok(projected.y - half >= 0 && projected.y + half <= size);
      assert.ok(projected.opacity >= .48 && projected.opacity <= 1);
    }
  }
}

class Element {
  constructor(text = '') {
    this.textContent = text; this.attributes = {}; this.style = {}; this.dataset = {};
    this.children = []; this.listeners = {}; this.selectors = {}; this.offsetWidth = 64;
    this.classes = new Set(); this.captures = new Set();
    this.classList = {add: value => this.classes.add(value), remove: value => this.classes.delete(value)};
  }
  addEventListener(type, fn) { (this.listeners[type] ||= []).push(fn); }
  emit(type, input = {}) {
    const event = {target: this, preventDefault() { this.prevented = true; }, ...input};
    (this.listeners[type] || []).forEach(fn => fn(event)); return event;
  }
  querySelector(selector) { return this.selectors[selector]; }
  querySelectorAll(selector) { return this.selectors[selector] || []; }
  setAttribute(key, value) { this.attributes[key] = String(value); }
  getAttribute(key) { return this.attributes[key]; }
  hasAttribute(key) { return key in this.attributes; }
  removeAttribute(key) { delete this.attributes[key]; }
  append(...elements) { elements.forEach(el => { el.parent = this; this.children.push(el); }); }
  replaceChildren(...elements) { this.children = []; this.textContent = ''; this.append(...elements); }
  contains(el) { return el === this || this.children.some(child => child.contains(el)); }
  closest(selector) { return selector === '.globe-node' && this.className === 'globe-node' ? this : this.parent?.closest(selector) || null; }
  getBoundingClientRect() { return {width: 500}; }
  setPointerCapture(id) { this.captures.add(id); }
  hasPointerCapture(id) { return this.captures.has(id); }
  releasePointerCapture(id) { this.captures.delete(id); }
}
const document = new Element(); document.hidden = false;
document.createElement = () => new Element();
const section = new Element(); document.selectors['#toolkit'] = section;
const selectors = ['.tool-globe', '.tool-globe-nodes', '#globe-tool-name'];
selectors.forEach(selector => { section.selectors[selector] = new Element(); });
const stage = section.querySelector('.tool-globe');
const nodes = section.querySelector('.tool-globe-nodes'); stage.append(nodes);
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const decode = text => text.replace(/&amp;/g, '&').replace(/<[^>]+>/g, '').trim();
for (const [,attrs,content] of html.matchAll(/<button\b([^>]*)>([\s\S]*?)<\/button>/g)) {
  if (!attrs.includes('class="globe-node"')) continue;
  const button = new Element(); button.className = 'globe-node';
  button.setAttribute('aria-label', decode(attrs.match(/aria-label="([^"]+)"/)[1]));
  const image = new Element(); image.setAttribute('src', content.match(/<img[^>]+src="([^"]+)"/)[1]);
  const symbol = new Element(); symbol.append(image); button.append(symbol); nodes.append(button);
}
nodes.selectors['.globe-node'] = nodes.children;
for (const text of ['Browse all tools', 'Pause rotation', 'Reset view', 'About Pejman', 'FROM IDEAS TO WORKING ROBOTS']) assert.ok(!html.includes(text), `Removed copy returned: ${text}`);
const media = new Element(); media.matches = false;
const frames = new Map(); let nextFrame = 0, observer;
class IntersectionObserver { constructor(fn) { observer = fn; } observe() {} }
class ResizeObserver { constructor(fn) { this.fn = fn; } observe() { this.fn(); } }
const window = new Element();
window.matchMedia = () => media;
window.requestAnimationFrame = fn => { frames.set(++nextFrame, fn); return nextFrame; };
window.IntersectionObserver = IntersectionObserver; window.ResizeObserver = ResizeObserver;
function frame(time) { const callbacks = [...frames.values()]; frames.clear(); callbacks.forEach(fn => fn(time)); }
vm.runInNewContext(fs.readFileSync(path.join(root, 'assets/tool-globe.js'), 'utf8'), {document, window, IntersectionObserver, ResizeObserver});
frame(16);
assert.equal(nodes.children.length, 17);
const names = nodes.children.map(button => button.getAttribute('aria-label'));
assert.ok(!names.includes('LiDAR') && !names.includes('IMU integration'));
for (const name of ['C++', 'Git', 'Docker', 'Blender']) assert.equal(names.filter(item => item === name).length, 1);
const iconPaths = nodes.children.map(button => button.children[0].children[0].getAttribute('src'));
assert.equal(new Set(iconPaths).size, 17, 'Each tool has its own icon');
iconPaths.forEach(src => assert.ok(fs.existsSync(path.join(root, src)), `Missing icon: ${src}`));
assert.equal(section.querySelector('#globe-tool-name').textContent, 'ROS 2');
assert.equal(frames.size, 0, 'Offscreen globe must not keep animating');

const python = nodes.children.find(button => button.getAttribute('aria-label') === 'Python');
python.emit('click', {detail: 0});
assert.equal(section.querySelector('#globe-tool-name').textContent, 'Python');
nodes.children[0].emit('click', {detail: 0});
const initial = nodes.children[0].style.transform;
assert.ok(stage.emit('keydown', {key: 'ArrowRight'}).prevented); frame(32);
assert.notEqual(nodes.children[0].style.transform, initial);
stage.emit('keydown', {key: 'Home'}); frame(48);
assert.equal(nodes.children[0].style.transform, initial);

const pointer = {pointerId: 7, isPrimary: true, button: 0, clientX: 100, clientY: 100, timeStamp: 50, target: python};
stage.emit('pointerdown', pointer);
stage.emit('pointermove', {...pointer, clientX: 150, clientY: 130, timeStamp: 80});
frame(80);
stage.emit('pointerup', {...pointer, clientX: 150, clientY: 130, timeStamp: 90});
assert.equal(section.querySelector('#globe-tool-name').textContent, 'ROS', 'Dragging a tool must not select it');
assert.ok(!stage.classes.has('is-dragging'));
stage.emit('pointerdown', {...pointer, timeStamp: 110});
stage.emit('pointerup', {...pointer, timeStamp: 120});
assert.equal(section.querySelector('#globe-tool-name').textContent, 'Python');
stage.emit('pointerdown', {...pointer, timeStamp: 130});
stage.emit('pointercancel', {...pointer, timeStamp: 140});
assert.ok(!stage.hasPointerCapture(7));
assert.ok(!stage.classes.has('is-dragging'));

observer([{isIntersecting: true}]); frame(150);
const beforeAuto = nodes.children[0].style.transform; frame(180);
assert.notEqual(nodes.children[0].style.transform, beforeAuto);
stage.emit('keydown', {key: ' '}); frame(200);
assert.equal(frames.size, 0);
stage.emit('keydown', {key: ' '}); frame(220); assert.ok(frames.size > 0);
media.matches = true; media.emit('change'); frame(240);
assert.equal(frames.size, 0);
const beforeReduced = nodes.children[0].style.transform;
stage.emit('keydown', {key: 'ArrowUp'}); frame(260);
assert.notEqual(nodes.children[0].style.transform, beforeReduced, 'Manual rotation remains available with reduced motion');
assert.equal(frames.size, 0);
stage.emit('keydown', {key: ' '}); frame(280);
document.hidden = true; document.emit('visibilitychange'); frame(300);
assert.equal(frames.size, 0, 'Hidden tabs must stop animating');
console.log('PASS: removed-copy checks; sphere geometry and bounds; tool selection; drag/click separation; pointer cancellation; keyboard/reset; automatic rotation; pause; reduced motion; offscreen/hidden-tab suspension.');
