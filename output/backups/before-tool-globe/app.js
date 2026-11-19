(() => {
  'use strict';
  document.documentElement.classList.add('js-enabled');
  const header = document.querySelector('.site-header');
  const menu = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  const navLinks = [...navigation.querySelectorAll('a[href^="#"]')];
  const chapters = [...document.querySelectorAll('[data-chapter]')];
  const covers = [...document.querySelectorAll('.chapter-cover')];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
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
  window.matchMedia('(min-width: 1201px)').addEventListener('change', closeMenu);

  function setActiveChapter(id) {
    if (id === activeChapter) return;
    activeChapter = id;
    navLinks.forEach(link => {
      if (link.getAttribute('href') === '#' + id) link.setAttribute('aria-current', 'location');
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
    covers.forEach(cover => {
      const bounds = cover.getBoundingClientRect();
      if (bounds.bottom > 0 && bounds.top < window.innerHeight) {
        const shift = reducedMotion.matches || window.innerWidth <= 800 ? 0 : Math.max(-18, Math.min(18, -bounds.top * .035));
        cover.style.setProperty('--image-shift', shift + 'px');
      }
    });
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
  function revealAnchor() {
    const id = window.location.hash.slice(1);
    const target = id ? document.getElementById(id) : null;
    if (!target) return;
    let parent = target.parentElement;
    let opened = false;
    while (parent) {
      if (parent.tagName === 'DETAILS' && !parent.open) { parent.open = true; opened = true; }
      parent = parent.parentElement;
    }
    if (opened) window.requestAnimationFrame(() => target.scrollIntoView());
    scheduleScrollUpdate();
  }
  window.addEventListener('hashchange', revealAnchor);
  reducedMotion.addEventListener('change', scheduleScrollUpdate);
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
  revealAnchor();
  updateScrollState();

  // Fade sections on entry in either scroll direction without changing layout.
  if ('IntersectionObserver' in window) {
    const sections = document.querySelectorAll('.hero, .affiliations, .chapter-cover, .chapter-content, .contact-section');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.target.classList.toggle('is-visible', entry.isIntersecting));
    }, {rootMargin: '0px 0px -6% 0px', threshold: 0});
    sections.forEach(section => {
      const bounds = section.getBoundingClientRect();
      section.classList.toggle('is-visible', bounds.bottom > 0 && bounds.top < window.innerHeight * .94);
      section.classList.add('section-fade');
      observer.observe(section);
    });
  }
})();
