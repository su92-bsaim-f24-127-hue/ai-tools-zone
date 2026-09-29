/* Optional local integration events. No network requests, cookies or persistent tracking. */
(() => {
  const section = location.pathname.split('/').filter(Boolean)[0] || 'home';
  const allowed = new Set(['home', 'products', 'categories', 'compare', 'alternatives', 'use-cases', 'guides', 'pricing', 'about', 'privacy', 'terms']);
  const emit = (name, extra = {}) => document.dispatchEvent(new CustomEvent('aitz:measure', {
    detail: { name, page: location.pathname, section: allowed.has(section) ? section : 'other', ...extra }
  }));
  emit('page_view');
  document.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (link) {
      const url = new URL(link.href, location.href);
      if (url.hostname === 'wa.me' && url.pathname === '/923430173923') emit('whatsapp_click');
    }
    if (event.target.closest('[data-open-compare]')) emit('comparison_open');
    if (event.target.closest('[data-finder]')) emit('finder_open');
  });
})();
