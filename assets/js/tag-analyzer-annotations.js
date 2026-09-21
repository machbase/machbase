document.querySelectorAll('[data-annotated-image]').forEach(image => {
  image.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    const dialog = document.createElement('dialog');
    dialog.className = 'ta-image-dialog';
    dialog.setAttribute('aria-label', image.getAttribute('aria-label'));
    const close = document.createElement('button');
    close.type = 'button';
    const lang = document.documentElement.lang;
    close.textContent = lang.startsWith('ko') ? '닫기 ×' : lang.startsWith('ja') ? '閉じる ×' : 'Close ×';
    close.addEventListener('click', () => dialog.close());
    const enlarged = document.createElement('div');
    enlarged.className = image.className;
    enlarged.style.cssText = image.style.cssText;
    enlarged.innerHTML = image.innerHTML;
    dialog.append(close, enlarged);
    dialog.addEventListener('close', () => { dialog.remove(); image.focus({ preventScroll: true }); }, { once: true });
    document.body.append(dialog);
    dialog.showModal();
  });
});
