(() => {
  // Older source documents can keep their hidden appearance hook without reviving dark mode.
  document.documentElement.dataset.ihdTheme = 'light';
  document.querySelectorAll('[data-ihd-theme-toggle]').forEach(button => { button.hidden = true; });

  document.querySelectorAll('[data-ihd-steps]').forEach(root => {
    const panels = [...root.children].filter(child => child.matches('[data-ihd-step]'));
    const own = selector => [...root.querySelectorAll(selector)].find(node => node.closest('[data-ihd-steps]') === root);
    const controls = own('[data-ihd-step-controls]');
    const toggle = own('[data-ihd-step-toggle]');
    const navigation = own('[data-ihd-step-nav]');
    const previous = own('[data-ihd-previous]');
    const next = own('[data-ihd-next]');
    const status = own('[data-ihd-step-status]');
    if (!panels.length || !controls || !toggle || !navigation || !previous || !next || !status) return;
    let guided = false;
    let index = 0;
    function render(focus = false) {
      panels.forEach((panel, i) => { panel.hidden = guided && i !== index; });
      navigation.hidden = !guided;
      toggle.setAttribute('aria-pressed', String(guided));
      toggle.textContent = guided ? 'Read all steps' : 'Guide me';
      previous.disabled = index === 0;
      next.disabled = index === panels.length - 1;
      status.textContent = `Step ${index + 1} of ${panels.length}`;
      if (focus) {
        const heading = panels[index].querySelector('h2, h3, h4') || panels[index];
        heading.tabIndex = -1;
        heading.focus({ preventScroll: true });
      }
    }
    toggle.addEventListener('click', () => { guided = !guided; render(); });
    previous.addEventListener('click', () => { index = Math.max(0, index - 1); render(true); });
    next.addEventListener('click', () => { index = Math.min(panels.length - 1, index + 1); render(true); });
    render();
    controls.hidden = false;
  });

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const printing = matchMedia('print');
  document.querySelectorAll('[data-ihd-motion]').forEach(root => {
    const button = root.querySelector('[data-ihd-motion-toggle]');
    root.dataset.ihdRunning = 'false';
    if (!button || !('IntersectionObserver' in window)) return;
    let paused = false;
    let visible = false;
    function render() {
      const running = !paused && visible && !document.hidden && !reduced.matches && !printing.matches;
      const changed = root.dataset.ihdRunning !== String(running);
      root.dataset.ihdRunning = String(running);
      button.disabled = reduced.matches;
      button.setAttribute('aria-pressed', String(paused));
      button.textContent = reduced.matches ? 'Motion reduced' : paused ? 'Play motion' : 'Pause motion';
      button.setAttribute('aria-label', button.textContent);
      if (changed) root.dispatchEvent(new CustomEvent('ihd:motionchange', { bubbles: true, detail: { running } }));
    }
    const observer = new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting;
      render();
    });
    observer.observe(root);
    button.addEventListener('click', () => { paused = !paused; render(); });
    document.addEventListener('visibilitychange', render);
    reduced.addEventListener('change', render);
    printing.addEventListener('change', render);
    render();
    button.hidden = false;
  });

  const headers = [...document.querySelectorAll('[data-ihd-masthead]')];
  const landings = [...document.querySelectorAll('[data-ihd-landing]')].filter(root => root.querySelector('[data-ihd-wordmark]'));
  if (headers.length || landings.length) {
    let frame = 0;
    let lastY = window.scrollY;
    let geometry = [];
    let headerHeight = 0;
    function update() {
      frame = 0;
      const y = Math.max(0, window.scrollY);
      if (Math.abs(y - lastY) > 4 || y < headerHeight) {
        headers.forEach(header => { header.dataset.ihdAway = String(y > headerHeight * 2 && y > lastY); });
        lastY = y;
      }
      geometry.forEach(({ root, top, range }) => {
        const progress = Math.max(0, Math.min(1, (y - top) / range));
        root.style.setProperty('--ihd-intro-progress', reduced.matches ? '0' : String(progress));
        root.dataset.ihdScrolled = String(progress > 0);
      });
    }
    function schedule() { if (!frame) frame = requestAnimationFrame(update); }
    function measure() {
      headerHeight = Math.max(0, ...headers.map(header => header.offsetHeight));
      geometry = landings.map(root => ({ root, top: root.getBoundingClientRect().top + window.scrollY, range: Math.max(1, window.innerHeight * .65) }));
      schedule();
    }
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', measure, { passive: true });
    window.addEventListener('pageshow', measure);
    reduced.addEventListener('change', schedule);
    if ('ResizeObserver' in window) new ResizeObserver(measure).observe(document.body);
    document.fonts.ready.then(measure);
    measure();
  }

  // Contents rail: a plain <details> below 80rem, a sticky column above it. Links work without this script.
  document.querySelectorAll('.ihd-doc > .ihd-toc').forEach(toc => {
    const wide = matchMedia('(min-width: 80rem)');
    const entries = [...toc.querySelectorAll('a[href^="#"]')]
      .map(link => ({ link, target: document.getElementById(decodeURIComponent(link.hash.slice(1))) }))
      .filter(entry => entry.target);
    const breakouts = [...document.querySelectorAll('.ihd-doc .ihd-wide, .ihd-doc [data-ihd-breakout]')];
    let chosen = toc.open;
    let frame = 0;
    toc.addEventListener('toggle', () => { if (!wide.matches) chosen = toc.open; });
    function update() {
      frame = 0;
      let current = null;
      let best = -Infinity;
      for (const entry of entries) {
        const top = entry.target.getBoundingClientRect().top;
        if (top <= 140 && top > best) { best = top; current = entry; }
      }
      if (entries.length && innerHeight + scrollY >= document.documentElement.scrollHeight - 2) current = entries[entries.length - 1];
      entries.forEach(entry => {
        if (entry === current) entry.link.setAttribute('aria-current', 'location');
        else entry.link.removeAttribute('aria-current');
      });
      const rail = toc.getBoundingClientRect();
      if (current && wide.matches) {
        const link = current.link.getBoundingClientRect();
        if (link.top < rail.top || link.bottom > rail.bottom) toc.scrollTop += link.top - rail.top - rail.height / 2;
      }
      // A wide figure that crosses the rail takes the space; the rail stays reachable by keyboard.
      const covered = wide.matches && breakouts.some(el => {
        const r = el.getBoundingClientRect();
        return r.height > 0 && r.bottom > rail.top && r.top < rail.bottom && r.left < rail.right && r.right > rail.left;
      });
      toc.dataset.ihdFaded = String(covered);
    }
    function schedule() { if (!frame) frame = requestAnimationFrame(update); }
    function layout() { toc.open = wide.matches || chosen; schedule(); }
    window.addEventListener('scroll', schedule, { passive: true });
    window.addEventListener('resize', schedule, { passive: true });
    wide.addEventListener('change', layout);
    document.fonts.ready.then(schedule);
    layout();
  });
})();
