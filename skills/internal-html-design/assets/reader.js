(() => {
  const key = 'internal-html-design:theme';
  const toggles = [...document.querySelectorAll('[data-ihd-theme-toggle]')];
  let theme = 'light';
  try { if (localStorage.getItem(key) === 'dark') theme = 'dark'; } catch {}

  function applyTheme() {
    document.documentElement.dataset.ihdTheme = theme;
    toggles.forEach(button => button.setAttribute('aria-pressed', String(theme === 'dark')));
  }
  applyTheme();
  toggles.forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => {
      theme = theme === 'light' ? 'dark' : 'light';
      applyTheme();
      try { localStorage.setItem(key, theme); } catch {}
    });
  });

  document.querySelectorAll('[data-ihd-steps]').forEach(root => {
    const panels = [...root.children].filter(child => child.matches('[data-ihd-step]'));
    const controls = root.querySelector('[data-ihd-step-controls]');
    const toggle = root.querySelector('[data-ihd-step-toggle]');
    const navigation = root.querySelector('[data-ihd-step-nav]');
    const previous = root.querySelector('[data-ihd-previous]');
    const next = root.querySelector('[data-ihd-next]');
    const status = root.querySelector('[data-ihd-step-status]');
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
        const heading = panels[index].querySelector('h2, h3, h4');
        if (heading) { heading.tabIndex = -1; heading.focus({ preventScroll: true }); }
      }
    }
    toggle.addEventListener('click', () => { guided = !guided; render(); });
    previous.addEventListener('click', () => { index = Math.max(0, index - 1); render(true); });
    next.addEventListener('click', () => { index = Math.min(panels.length - 1, index + 1); render(true); });
    render();
    controls.hidden = false;
  });
})();
