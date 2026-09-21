document.querySelectorAll('.fft-media-guide').forEach(viewer => {
  if (viewer.dataset.ready) return;
  viewer.dataset.ready = 'true';
  const slides = [...viewer.querySelectorAll('[data-fft-slide]')];
  const dots = [...viewer.querySelectorAll('[data-fft-dot]')];
  const video = viewer.querySelector('video');
  const controls = viewer.querySelector('nav');
  const back = viewer.querySelector('[data-fft-back]');
  const next = viewer.querySelector('[data-fft-next]');
  let active = 0;

  function show(index) {
    if (index < 0 || index >= slides.length) return;
    if (index !== active) video.pause();
    active = index;
    slides.forEach((slide, i) => {
      slide.setAttribute('aria-hidden', String(i !== index));
      slide.inert = i !== index;
    });
    dots.forEach((dot, i) => {
      if (i === index) dot.setAttribute('aria-current', 'step');
      else dot.removeAttribute('aria-current');
    });
    viewer.querySelector('[data-fft-count]').textContent = `${index + 1} / ${slides.length}`;
    viewer.querySelector('[data-fft-title]').textContent = slides[index].dataset.title;
    viewer.querySelector('[data-fft-caption]').textContent = slides[index].dataset.caption;
    back.disabled = index === 0;
    next.disabled = index === slides.length - 1;
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
  window.addEventListener('beforeprint', () => slides.forEach(slide => {
    slide.setAttribute('aria-hidden', 'false');
    slide.inert = false;
  }));
  window.addEventListener('afterprint', () => show(active));
  controls.hidden = false;
  show(0);
});
