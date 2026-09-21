(() => {
  const players = [...document.querySelectorAll('.tag-analyzer-player')];
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(({ target, isIntersecting }) => {
      if (!isIntersecting) target.pause();
    });
  });

  players.forEach((video) => {
    video.addEventListener('play', () => {
      players.forEach((other) => {
        if (other !== video) other.pause();
      });
    });
    observer.observe(video);
  });
})();
