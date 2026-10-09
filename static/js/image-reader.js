'use strict';
(() => {
  const input = document.getElementById('image');
  if (!input) return;
  const preview = document.getElementById('imagePreview');
  const clear = document.getElementById('clearImage');
  let url = null;
  function reset() {
    if (url) URL.revokeObjectURL(url);
    url = null; preview.removeAttribute('src'); preview.hidden = clear.hidden = true;
  }
  input.addEventListener('change', () => {
    reset();
    const file = input.files[0];
    if (!file) return;
    if (file.size > 5 * 1024 * 1024 || !['image/jpeg','image/png','image/webp'].includes(file.type)) {
      input.value = ''; toast('请选择不超过 5MB 的 JPG、PNG、WebP 图片'); return;
    }
    url = URL.createObjectURL(file); preview.src = url; preview.hidden = clear.hidden = false;
  });
  preview.addEventListener('error', () => { reset(); input.value = ''; toast('图片无法预览，请重新选择'); });
  clear.addEventListener('click', () => { reset(); input.value = ''; });
  window.addEventListener('pagehide', reset);
})();
