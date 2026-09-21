document.querySelectorAll('.range-controls').forEach(viewer => {
  if (viewer.dataset.ready) return;
  viewer.dataset.ready = 'true';
  const slides = [...viewer.querySelectorAll('[data-range-slide]')];
  const dots = [...viewer.querySelectorAll('[data-range-dot]')];
  const controls = viewer.querySelector('nav');
  const back = viewer.querySelector('[data-range-back]');
  const next = viewer.querySelector('[data-range-next]');
  let active = 0;

  function show(index) {
    if (index < 0 || index >= slides.length) return;
    active = index;
    slides.forEach((slide, i) => {
      slide.setAttribute('aria-hidden', String(i !== index));
      slide.inert = i !== index;
    });
    dots.forEach((dot, i) => {
      if (i === index) dot.setAttribute('aria-current', 'step');
      else dot.removeAttribute('aria-current');
    });
    viewer.querySelector('[data-range-count]').textContent = `${index + 1} / ${slides.length}`;
    viewer.querySelector('[data-range-title]').textContent = slides[index].dataset.title;
    viewer.querySelector('[data-range-caption]').textContent = slides[index].dataset.caption;
    back.disabled = index === 0;
    next.disabled = index === slides.length - 1;
  }

  function showLinkedSlide() {
    const index = slides.findIndex(slide => `#${slide.id}` === location.hash);
    if (index !== -1) show(index);
  }

  dots.forEach((dot, i) => dot.addEventListener('click', () => show(i)));
  back.addEventListener('click', () => show(active - 1));
  next.addEventListener('click', () => show(active + 1));
  controls.addEventListener('keydown', event => {
    const targets = { ArrowLeft: active - 1, ArrowRight: active + 1, Home: 0, End: slides.length - 1 };
    if (!(event.key in targets)) return;
    event.preventDefault();
    show(targets[event.key]);
    dots[active].focus({ preventScroll: true });
  });
  window.addEventListener('hashchange', showLinkedSlide);
  window.addEventListener('beforeprint', () => slides.forEach(slide => {
    slide.setAttribute('aria-hidden', 'false');
    slide.inert = false;
  }));
  window.addEventListener('afterprint', () => show(active));
  controls.hidden = false;
  show(0);
  showLinkedSlide();
});
