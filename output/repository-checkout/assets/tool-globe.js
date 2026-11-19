(() => {
  'use strict';
  const TAU = Math.PI * 2;
  function spherePoints(count) {
    return Array.from({length: count}, (_, i) => {
      const y = 1 - (2 * i + 1) / count;
      const r = Math.sqrt(1 - y * y);
      const angle = i * Math.PI * (3 - Math.sqrt(5));
      return {x: Math.cos(angle) * r, y, z: Math.sin(angle) * r};
    });
  }
  function rotate(point, yaw, pitch) {
    const x = point.x * Math.cos(yaw) + point.z * Math.sin(yaw);
    const z = point.z * Math.cos(yaw) - point.x * Math.sin(yaw);
    return {x, y: point.y * Math.cos(pitch) - z * Math.sin(pitch), z: point.y * Math.sin(pitch) + z * Math.cos(pitch)};
  }
  function project(point, size, tokenSize) {
    const radius = Math.max(0, (size - tokenSize * 1.4) / 2);
    return {x: size / 2 + point.x * radius, y: size / 2 + point.y * radius,
      scale: .82 + (point.z + 1) * .14, opacity: .48 + (point.z + 1) * .26, depth: Math.round((point.z + 1) * 100)};
  }
  // Pure geometry is also used by the small dependency-free validation script.
  if (typeof module !== 'undefined' && module.exports) module.exports = {spherePoints, rotate, project};
  if (typeof document === 'undefined') return;
  const section = document.querySelector('#toolkit');
  if (!section) return;
  const stage = section.querySelector('.tool-globe');
  const nodes = section.querySelector('.tool-globe-nodes');
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  const tools = [...nodes.querySelectorAll('.globe-node')].map(button => ({
    name: button.getAttribute('aria-label'), button
  }));
  if (!tools.length) return;
  const points = spherePoints(tools.length);
  let yaw = .35, pitch = -.15, size = 500, tokenSize = 64;
  let paused = media.matches, visible = !('IntersectionObserver' in window);
  let hovered = false, focused = false, drag = null, velocityX = 0, velocityY = 0;
  let frame = 0, lastTime = 0;
  function select(index) {
    section.querySelector('#globe-tool-name').textContent = tools[index].name;
    tools.forEach((tool, i) => tool.button.setAttribute('aria-pressed', String(i === index)));
  }
  tools.forEach((tool, index) => {
    tool.button.dataset.index = String(index);
    tool.button.addEventListener('click', event => {
      // Pointer selection is resolved after the drag threshold.
      if (event.detail === 0) select(index);
    });
  });
  function draw() {
    tools.forEach((tool, index) => {
      const p = project(rotate(points[index], yaw, pitch), size, tokenSize);
      tool.button.style.transform = `translate(-50%, -50%) translate(${p.x}px, ${p.y}px) scale(${p.scale})`;
      tool.button.style.opacity = p.opacity;
      tool.button.style.zIndex = p.depth;
    });
  }
  function queue() { if (!frame) frame = window.requestAnimationFrame(tick); }
  function tick(now) {
    frame = 0;
    const dt = lastTime ? Math.min((now - lastTime) / 1000, .05) : 0;
    lastTime = now;
    const active = visible && !document.hidden;
    const automatic = active && !paused && !hovered && !focused && !drag;
    const inertia = active && !media.matches && !drag && (Math.abs(velocityX) + Math.abs(velocityY) > .005);
    if (inertia) {
      yaw += velocityX * dt; pitch += velocityY * dt;
      velocityX *= Math.exp(-6 * dt); velocityY *= Math.exp(-6 * dt);
    } else if (automatic) yaw += dt * .13;
    yaw %= TAU; pitch %= TAU;
    draw();
    if (inertia || automatic) queue(); else lastTime = 0;
  }
  function setPaused(value) {
    paused = value;
    velocityX = velocityY = 0;
    queue();
  }
  function resetView() { yaw = .35; pitch = -.15; velocityX = velocityY = 0; queue(); }
  stage.addEventListener('pointerenter', event => { if (event.pointerType === 'mouse') { hovered = true; queue(); } });
  stage.addEventListener('pointerleave', () => { hovered = false; queue(); });
  stage.addEventListener('focusin', () => { focused = true; velocityX = velocityY = 0; queue(); });
  stage.addEventListener('focusout', event => { focused = stage.contains(event.relatedTarget); queue(); });
  stage.addEventListener('pointerdown', event => {
    if (!event.isPrimary || event.button !== 0 || drag) return;
    const button = event.target.closest('.globe-node');
    drag = {id: event.pointerId, x: event.clientX, y: event.clientY, travel: 0, time: event.timeStamp,
      selected: button ? Number(button.dataset.index) : null};
    velocityX = velocityY = 0;
    stage.setPointerCapture(event.pointerId);
    stage.classList.add('is-dragging');
  });
  stage.addEventListener('pointermove', event => {
    if (!drag || drag.id !== event.pointerId) return;
    const dx = event.clientX - drag.x, dy = event.clientY - drag.y;
    drag.travel += Math.abs(dx) + Math.abs(dy);
    const dt = Math.max((event.timeStamp - drag.time) / 1000, .016);
    yaw += dx * .007; pitch -= dy * .007;
    velocityX = Math.max(-2, Math.min(2, dx * .007 / dt));
    velocityY = Math.max(-2, Math.min(2, -dy * .007 / dt));
    drag.x = event.clientX; drag.y = event.clientY; drag.time = event.timeStamp;
    queue();
  });
  function endDrag(event, cancel = false) {
    if (!drag || drag.id !== event.pointerId) return;
    if (!cancel && drag.travel < 6 && drag.selected !== null) select(drag.selected);
    if (cancel || drag.travel < 6 || paused || media.matches) velocityX = velocityY = 0;
    drag = null;
    stage.classList.remove('is-dragging');
    if (stage.hasPointerCapture(event.pointerId)) stage.releasePointerCapture(event.pointerId);
    queue();
  }
  stage.addEventListener('pointerup', event => endDrag(event));
  stage.addEventListener('pointercancel', event => endDrag(event, true));
  stage.addEventListener('lostpointercapture', event => endDrag(event, true));
  stage.addEventListener('keydown', event => {
    if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', ' '].includes(event.key)) return;
    if (event.key === ' ' && event.target !== stage) return;
    event.preventDefault();
    velocityX = velocityY = 0;
    if (event.key === 'Home') resetView();
    else if (event.key === ' ') setPaused(!paused);
    else {
      yaw += event.key === 'ArrowRight' ? .2 : event.key === 'ArrowLeft' ? -.2 : 0;
      pitch += event.key === 'ArrowUp' ? .2 : event.key === 'ArrowDown' ? -.2 : 0;
      queue();
    }
  });
  function resize() {
    size = stage.getBoundingClientRect().width;
    tokenSize = tools[0].button.offsetWidth || 64;
    queue();
  }
  media.addEventListener('change', () => { if (media.matches) setPaused(true); });
  document.addEventListener('visibilitychange', () => { lastTime = 0; queue(); });
  section.classList.add('has-tool-globe');
  select(Math.max(0, tools.findIndex(tool => tool.name === 'ROS 2')));
  setPaused(paused);
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(stage);
  else window.addEventListener('resize', resize, {passive: true});
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    lastTime = 0;
    queue();
  }, {threshold: .05}).observe(stage);
  resize();
})();
