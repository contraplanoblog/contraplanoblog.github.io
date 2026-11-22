// Busca e filtro por tags na lista de textos da página inicial.
{
  const norm = s => String(s ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const q = document.getElementById('q');
  const chips = document.getElementById('chips');
  const empty = document.getElementById('empty');
  const count = document.getElementById('count');
  const rows = [...document.querySelectorAll('#index .row')];
  const total = rows.length;
  let tag = '';

  rows.forEach(r => {
    r._q = norm(r.dataset.q);
    r._t = (r.dataset.tags || '').split('|').map(t => norm(t.trim())).filter(Boolean);
  });

  if (chips) {
    const seen = new Map();
    rows.forEach(r => (r.dataset.tags || '').split('|').forEach(t => {
      const k = norm(t.trim());
      if (k && !seen.has(k)) seen.set(k, t.trim());
    }));
    if (seen.size === 0) chips.remove();
    [...seen.entries()].sort((a, b) => a[0].localeCompare(b[0])).forEach(([k, t]) => {
      const b = document.createElement('button');
      b.type = 'button'; b.className = 'chip'; b.dataset.tag = k;
      b.setAttribute('aria-pressed', 'false'); b.textContent = t;
      chips.appendChild(b);
    });
  }

  const filter = () => {
    const t = norm(q ? q.value : '').trim();
    let n = 0;
    rows.forEach(r => {
      const ok = (!t || r._q.includes(t)) && (!tag || r._t.includes(tag));
      r.hidden = !ok;
      if (ok) n++;
    });
    if (empty) empty.hidden = n > 0;
    if (count) count.textContent = n === total ? `(${total})` : `(${n} de ${total})`;
  };

  if (q) q.addEventListener('input', filter);
  if (chips) chips.addEventListener('click', e => {
    const b = e.target.closest('.chip');
    if (!b) return;
    tag = b.dataset.tag;
    chips.querySelectorAll('.chip').forEach(c => c.setAttribute('aria-pressed', String(c === b)));
    filter();
  });
}
