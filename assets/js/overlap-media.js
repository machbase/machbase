document.querySelectorAll('.overlap-media').forEach((viewer) => {
  if (viewer.dataset.ready) return;
  viewer.dataset.ready = 'true';
  const dots = [...viewer.querySelectorAll('[data-media-slide]')];
  const video = viewer.querySelector('.tag-analyzer-player');
  const link = viewer.querySelector('[data-media-link]');
  const caption = viewer.querySelector('figcaption');
  const controls = viewer.querySelector('nav');
  const back = viewer.querySelector('[data-media-back]');
  const next = viewer.querySelector('[data-media-next]');
  let active = 0;

  function show(index) {
    if (index < 0 || index >= dots.length || index === active) return;
    active = index;
    video.pause();
    video.hidden = index !== 0;
    link.hidden = index === 0;
    caption.textContent = dots[index].dataset.caption;
    dots.forEach((dot, i) => {
      if (i === index) dot.setAttribute('aria-current', 'step');
      else dot.removeAttribute('aria-current');
    });
    back.disabled = index === 0;
    next.disabled = index === dots.length - 1;
  }

  dots.forEach((dot, index) => dot.addEventListener('click', () => show(index)));
  back.addEventListener('click', () => show(active - 1));
  next.addEventListener('click', () => show(active + 1));
  controls.addEventListener('keydown', (event) => {
    const destinations = { ArrowLeft: active - 1, ArrowRight: active + 1, Home: 0, End: dots.length - 1 };
    if (!(event.key in destinations)) return;
    event.preventDefault();
    show(destinations[event.key]);
    dots[active].focus({ preventScroll: true });
  });
  controls.hidden = false;
});
