'use strict';
const csrf = document.querySelector('meta[name="csrf-token"]').content;
// 浏览位置记忆：从首页进入详情后，返回时恢复筛选条件与滚动位置。
const LIST_KEY = 'listState';
if (document.getElementById('searchForm')) {
  document.querySelectorAll('.card').forEach(link => link.addEventListener('click', () => {
    sessionStorage.setItem(LIST_KEY, JSON.stringify({scrollY: window.scrollY, search: location.search}));
  }));
  const raw = sessionStorage.getItem(LIST_KEY);
  if (raw) {
    sessionStorage.removeItem(LIST_KEY);
    try {
      const saved = JSON.parse(raw);
      if ((saved.search || '') === location.search) window.scrollTo(0, saved.scrollY || 0);
    } catch { /* 损坏的记录直接丢弃 */ }
  }
} else {
  // 详情等子页面：返回链接带上原筛选条件，首页才会恢复位置。
  const raw = sessionStorage.getItem(LIST_KEY);
  if (raw) {
    try {
      const saved = JSON.parse(raw);
      document.querySelectorAll('.back, a[href="/"]').forEach(link =>
        link.setAttribute('href', '/' + (saved.search || '')));
    } catch { /* 损坏的记录直接丢弃 */ }
  }
}
function toast(message) {
  const element = document.getElementById('toast');
  element.textContent = message; element.hidden = false;
  clearTimeout(window.toastTimer);
  window.toastTimer = setTimeout(() => element.hidden = true, 3500);
}
async function api(url, options = {}) {
  const response = await fetch(url, {...options, headers: {...options.headers, 'X-CSRF-Token': csrf}});
  let data;
  try { data = await response.json(); } catch { throw new Error('服务器响应异常，请稍后重试'); }
  if (!response.ok) throw new Error(data.error || '操作失败，请重试');
  return data;
}
document.getElementById('publishForm')?.addEventListener('submit', async event => {
  event.preventDefault();
  const form = event.currentTarget, button = form.querySelector('[type="submit"]');
  const error = document.getElementById('formError');
  error.hidden = true; button.disabled = true;
  try {
    const data = await api('/api/posts', {method:'POST', body:new FormData(form)});
    location.href = data.redirect;
  } catch (e) { error.textContent = e.message; error.hidden = false; }
  finally { button.disabled = false; }
});
document.querySelectorAll('[data-finish], [data-delete]').forEach(button => {
  button.addEventListener('click', async () => {
    const deleting = button.hasAttribute('data-delete');
    if (!confirm(deleting ? '确定删除这条信息？删除后无法恢复。' : '确认物品已经找回或归还？')) return;
    button.disabled = true;
    try {
      const id = deleting ? button.dataset.delete : button.dataset.finish;
      await api(`/api/posts/${id}${deleting ? '' : '/finish'}`, {method: deleting ? 'DELETE' : 'PATCH'});
      location.reload();
    } catch (e) { toast(e.message); button.disabled = false; }
  });
});
document.getElementById('copyContact')?.addEventListener('click', async () => {
  const element = document.getElementById('contactText');
  try { await navigator.clipboard.writeText(element.textContent); toast('联系方式已复制'); }
  catch {
    const selection = window.getSelection(), range = document.createRange();
    range.selectNodeContents(element); selection.removeAllRanges(); selection.addRange(range);
    toast('自动复制不可用，已选中联系方式，请按 Ctrl+C 复制');
  }
});
