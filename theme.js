(() => {
  'use strict';
  const key = 'atz-theme-v1';
  const system = matchMedia('(prefers-color-scheme: light)');
  let preference;
  try { preference = localStorage.getItem(key); } catch (_) {}
  const valid = value => value === 'dark' || value === 'light';
  function apply(theme) {
    document.documentElement.dataset.theme = theme;
    document.documentElement.style.colorScheme = theme;
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', theme === 'light' ? '#f7f8f2' : '#10110f');
    const button = document.getElementById('theme-toggle');
    if (!button) return;
    button.setAttribute('aria-pressed', String(theme === 'light'));
    button.title = theme === 'light' ? 'Switch to dark theme' : 'Switch to light theme';
  }
  apply(valid(preference) ? preference : (system.matches ? 'light' : 'dark'));
  document.addEventListener('DOMContentLoaded', () => {
    apply(document.documentElement.dataset.theme);
    document.getElementById('theme-toggle')?.addEventListener('click', () => {
      preference = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
      apply(preference);
      try { localStorage.setItem(key, preference); } catch (_) {}
    });
  });
  system.addEventListener('change', () => { if (!valid(preference)) apply(system.matches ? 'light' : 'dark'); });
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    preference = event.newValue;
    apply(valid(preference) ? preference : (system.matches ? 'light' : 'dark'));
  });
})();
