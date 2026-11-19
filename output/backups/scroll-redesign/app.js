(() => {
  'use strict';
  document.documentElement.classList.add('js-enabled');
  const header = document.querySelector('.site-header');
  const menu = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  const navLinks = [...navigation.querySelectorAll('a[href^="#"]')];
  const dots = [...document.querySelectorAll('.chapter-dots a')];
  const chapters = [...document.querySelectorAll('[data-chapter]')];
  const frames = [...document.querySelectorAll('[data-visual]')];
  let activeChapter = '';
  let pendingFrame = false;

  function closeMenu() {
    menu.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('open');
    header.classList.remove('menu-open');
  }
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('open', open);
    header.classList.toggle('menu-open', open);
  });
  navLinks.forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menu.focus();
    }
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  window.matchMedia('(min-width: 801px)').addEventListener('change', closeMenu);

  function setActiveChapter(id) {
    if (id === activeChapter) return;
    activeChapter = id;
    navLinks.forEach(link => {
      if (link.getAttribute('href') === '#' + id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    // Keep the first image ready while the introductory portrait is visible.
    const visualId = id === 'home' ? 'research' : id;
    frames.forEach(frame => {
      const active = frame.dataset.visual === visualId;
      frame.classList.toggle('is-active', active);
      frame.setAttribute('aria-hidden', String(!active));
      frame.querySelectorAll('a').forEach(link => { link.tabIndex = active ? 0 : -1; });
    });
    dots.forEach(link => {
      if (link.getAttribute('href') === '#' + visualId) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
    document.body.dataset.section = id;
  }

  function updateScrollState() {
    pendingFrame = false;
    const y = window.scrollY || 0;
    const headerHeight = header.getBoundingClientRect().height;
    // Change chapters as their heading reaches the upper third of the viewport.
    const activationLine = headerHeight + (window.innerHeight - headerHeight) * .3;
    let current = 'home';
    for (const chapter of chapters) {
      if (chapter.getBoundingClientRect().top <= activationLine) current = chapter.dataset.chapter;
      else break;
    }
    const maximum = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    if (maximum > 0 && y >= maximum - 3) current = chapters[chapters.length - 1].dataset.chapter;
    setActiveChapter(current);
    header.classList.toggle('is-scrolled', y > 24);
    const progress = maximum > 0 ? Math.max(0, Math.min(1, y / maximum)) : 0;
    header.style.setProperty('--reading-progress', String(progress));
  }
  function scheduleScrollUpdate() {
    if (!pendingFrame) {
      pendingFrame = true;
      window.requestAnimationFrame(updateScrollState);
    }
  }
  window.addEventListener('scroll', scheduleScrollUpdate, {passive: true});
  window.addEventListener('resize', scheduleScrollUpdate, {passive: true});
  window.addEventListener('hashchange', scheduleScrollUpdate);
  window.addEventListener('pageshow', scheduleScrollUpdate);
  window.addEventListener('load', scheduleScrollUpdate);
  document.querySelectorAll('details').forEach(detail => detail.addEventListener('toggle', scheduleScrollUpdate));
  if ('ResizeObserver' in window) new ResizeObserver(scheduleScrollUpdate).observe(document.querySelector('.story-flow'));

  const publications = [...document.querySelectorAll('.publication')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  filters.forEach(button => button.addEventListener('click', () => {
    const filter = button.dataset.filter;
    filters.forEach(item => {
      item.classList.toggle('active', item === button);
      item.setAttribute('aria-pressed', String(item === button));
    });
    publications.forEach(item => { item.hidden = filter !== 'all' && item.dataset.type !== filter; });
    const count = publications.filter(item => !item.hidden).length;
    const labels = {all: 'selected publication', journal: 'journal article', conference: 'conference paper', preprint: 'preprint'};
    document.querySelector('#publication-count').textContent = `${count} ${labels[filter]}${count === 1 ? '' : 's'}`;
    scheduleScrollUpdate();
  }));

  document.querySelector('#year').textContent = new Date().getFullYear();
  updateScrollState();
})();
