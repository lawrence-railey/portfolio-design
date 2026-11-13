// Local hover experiment. Add ?fx=off to compare without the overlay.
(() => {
  if (new URLSearchParams(location.search).get('fx') === 'off') return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const mouse = matchMedia('(hover: hover) and (pointer: fine)');
  const selector = '.menu-toggle, .button, .project-card > a, .world-link, .artwork > a, .gallery > figure > a, .architecture-links > a, .filter-bar button, .carousel-controls button, .carousel-thumbnails button, .text-link, .back-link, .section-nav a, .case-section-nav a';
  const cooldowns = new WeakMap();
  const surfaces = new WeakMap();

  function prepare(target) {
    if (surfaces.has(target)) return surfaces.get(target);
    target.classList.add('fx-target');
    // Keep linked card captions outside the animated image surface.
    const surface = target.matches('.project-card > a')
      ? target.querySelector('.project-brand-image, .project-image') || target
      : target;
    surfaces.set(target, surface);
    surface.classList.add('fx-surface');
    if (getComputedStyle(surface).position === 'static') surface.classList.add('fx-position');
    if (target.matches('.project-card > a, .world-link, .artwork > a, .gallery > figure > a, .architecture-links > a')) surface.classList.add('fx-card');
    const scanOnly = target.matches('.text-link, .back-link, .section-nav a, .case-section-nav a, .filter-bar button');
    const flickerOnly = target.matches('.section-nav a');
    const galleryItem = target.matches('.project-card > a, .artwork > a, .gallery > figure > a, .carousel-thumbnails button');
    const noScan = galleryItem || target.matches('.world-link');
    const overlay = document.createElement('span');
    overlay.className = 'fx-overlay';
    overlay.setAttribute('aria-hidden', 'true');
    const parts = flickerOnly ? ['pulse'] : scanOnly ? ['scan'] : galleryItem ? ['corners', 'scan'] : ['corners', 'scan', 'ticks'];
    for (const name of parts.filter(name => !noScan || name !== 'scan')) {
      const part = document.createElement('span');
      part.className = `fx-${name}`;
      overlay.append(part);
    }
    surface.append(overlay);
    return surface;
  }

  function enter(target) {
    if (!target || target.matches(':disabled, [aria-disabled="true"]') || reduced.matches) return;
    const surface = prepare(target);
    surface.classList.add('fx-active');
    const now = performance.now();
    if (now - (cooldowns.get(target) ?? -Infinity) < 850) return;
    cooldowns.set(target, now);
    surface.classList.remove('fx-burst');
    void surface.offsetWidth;
    surface.classList.add('fx-burst');
  }

  document.addEventListener('pointerover', event => {
    if (!mouse.matches || event.pointerType === 'touch') return;
    const target = event.target.closest(selector);
    if (target && !target.contains(event.relatedTarget)) enter(target);
  });
  document.addEventListener('pointerout', event => {
    const target = event.target.closest('.fx-target');
    if (target && !target.contains(event.relatedTarget) && !target.matches(':focus-visible')) surfaces.get(target)?.classList.remove('fx-active');
  });
  document.addEventListener('focusin', event => {
    const target = event.target.closest(selector);
    if (target?.matches(':focus-visible')) enter(target);
  });
  document.addEventListener('focusout', event => {
    const target = event.target.closest('.fx-target');
    if (target && !target.matches(':hover')) surfaces.get(target)?.classList.remove('fx-active');
  });
})();
