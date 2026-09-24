(() => {
  'use strict';
  const art = document.getElementById('hero-art');
  const toggle = document.getElementById('motion-toggle');
  if (!art || !toggle) return;
  const media = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = media.matches;
  let visible = true;
  function update() {
    document.body.classList.toggle('paused', paused);
    document.body.classList.toggle('motion-idle', document.hidden);
    art.classList.toggle('offstage', !visible);
    toggle.setAttribute('aria-pressed', String(paused));
    toggle.setAttribute('aria-label', paused ? 'Play logo animation' : 'Pause logo animation');
    toggle.textContent = paused ? '▷' : 'Ⅱ';
    if (paused) resetTilt();
  }
  function resetTilt() { art.style.setProperty('--rx', '0deg'); art.style.setProperty('--ry', '0deg'); }
  toggle.addEventListener('click', () => { paused = !paused; update(); });
  media.addEventListener('change', event => { paused = event.matches; update(); });
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; update(); }, {threshold: .05}).observe(art);
  const secondary = document.querySelector('.finder-brand');
  if (secondary) new IntersectionObserver(entries => secondary.classList.toggle('motion-offstage', !entries[0].isIntersecting)).observe(secondary);
  document.addEventListener('visibilitychange', update);
  art.addEventListener('pointermove', event => {
    if (paused || media.matches || event.pointerType !== 'mouse') return;
    const r = art.getBoundingClientRect();
    art.style.setProperty('--rx', (-(event.clientY-r.top-r.height/2)/r.height*8)+'deg');
    art.style.setProperty('--ry', ((event.clientX-r.left-r.width/2)/r.width*12)+'deg');
  });
  art.addEventListener('pointerleave', resetTilt);
  update();
})();
