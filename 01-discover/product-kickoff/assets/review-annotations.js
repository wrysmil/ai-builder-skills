(() => {
  const left = document.querySelector('#prototype-pane');
  const right = document.querySelector('#requirements-pane');
  const content = document.querySelector('#requirement-content');
  const overlay = document.querySelector('.review-overlay');
  const toggle = document.querySelector('.review-annotations-toggle');
  if (!left || !right || !content || !overlay || !toggle) return;

  const ink = getComputedStyle(overlay.parentElement).getPropertyValue('--review-line').trim();
  const narrow = matchMedia('(max-width: 900px)');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let pairs = [];
  let hovered = null;
  let focused = null;
  let pinned = null;
  let visible = true;
  let frame = 0;

  function svg(name, attributes) {
    const element = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (const [key, value] of Object.entries(attributes)) element.setAttribute(key, value);
    return element;
  }

  function visibleBox(element) {
    if (!element.getClientRects().length) return null;
    const box = element.getBoundingClientRect();
    let x1 = Math.max(0, box.left), y1 = Math.max(0, box.top);
    let x2 = Math.min(innerWidth, box.right), y2 = Math.min(innerHeight, box.bottom);
    for (let parent = element.parentElement; parent && parent !== document.body; parent = parent.parentElement) {
      const bounds = parent.getBoundingClientRect();
      const style = getComputedStyle(parent);
      if (style.overflowX !== 'visible') { x1 = Math.max(x1, bounds.left); x2 = Math.min(x2, bounds.right); }
      if (style.overflowY !== 'visible') { y1 = Math.max(y1, bounds.top); y2 = Math.min(y2, bounds.bottom); }
    }
    return x1 < x2 && y1 < y2 ? { left: x1, right: x2, mid: (y1 + y2) / 2 } : null;
  }

  function paint() {
    frame = 0;
    overlay.replaceChildren();
    const active = hovered || focused || pinned;
    const dialog = document.querySelector('[aria-modal="true"]:not(.is-hidden):not([hidden])');
    const modalOpen = dialog && dialog.getClientRects().length > 0;
    for (const pair of pairs) {
      const selected = pair.key === active;
      pair.target.toggleAttribute('data-review-active', selected);
      pair.card.toggleAttribute('data-review-active', selected);
      if (!visible || narrow.matches || modalOpen) continue;
      const from = visibleBox(pair.target), to = visibleBox(pair.card);
      if (!from || !to || from.right >= to.left) continue;
      const x = (from.right + to.left) / 2, y = (from.mid + to.mid) / 2;
      const group = svg('g', { opacity: selected ? 1 : active ? 0.35 : 0.75 });
      group.append(
        svg('path', { d: `M${from.right} ${from.mid} C${x} ${from.mid} ${x} ${to.mid} ${to.left} ${to.mid}`, fill: 'none', stroke: ink, 'stroke-width': selected ? 2.4 : 1.5 }),
        svg('circle', { cx: x, cy: y, r: 9, fill: ink, stroke: 'white', 'stroke-width': 1 }),
      );
      const label = svg('text', { x, y, 'text-anchor': 'middle', 'dominant-baseline': 'central', fill: 'white', 'font-size': 10, 'font-weight': 700 });
      label.textContent = pair.number;
      group.append(label);
      overlay.append(group);
    }
  }

  function schedule() {
    if (!frame) frame = requestAnimationFrame(paint);
  }

  const geometry = new ResizeObserver(schedule);
  geometry.observe(left);
  geometry.observe(right);

  function refresh() {
    for (const pair of pairs) {
      pair.target.removeAttribute('data-review-active');
      geometry.unobserve(pair.target);
      geometry.unobserve(pair.card);
    }
    hovered = focused = pinned = null;
    pairs = Array.from(content.querySelectorAll('.review-card[data-review-note]')).flatMap((card, index) => {
      const key = card.dataset.reviewNote;
      const target = Array.from(left.querySelectorAll('[data-review-target]')).find((element) => element.dataset.reviewTarget === key);
      if (!target) return [];
      const number = index + 1;
      const badge = card.querySelector('.review-number');
      if (badge) badge.textContent = number;
      geometry.observe(target);
      geometry.observe(card);
      return [{ key, number, target, card }];
    });
    schedule();
  }

  function keyFor(element) {
    if (!(element instanceof Element)) return null;
    const region = element.closest('[data-review-target], [data-review-note]');
    return region?.dataset.reviewTarget || region?.dataset.reviewNote || null;
  }

  document.addEventListener('pointerover', (event) => { hovered = keyFor(event.target); schedule(); });
  document.addEventListener('pointerout', (event) => { hovered = keyFor(event.relatedTarget); schedule(); });
  document.addEventListener('focusin', (event) => { focused = keyFor(event.target); schedule(); });
  document.addEventListener('focusout', (event) => { focused = keyFor(event.relatedTarget); schedule(); });
  content.addEventListener('click', (event) => {
    const button = event.target.closest('.review-jump');
    if (!button) return;
    const pair = pairs.find(({ key }) => key === keyFor(button));
    if (!pair) return;
    pinned = pair.key;
    pair.target.scrollIntoView({ behavior: motion.matches ? 'instant' : 'smooth', block: 'nearest', inline: 'nearest' });
    schedule();
  });
  function updateToggle() {
    toggle.textContent = visible ? '隐藏连线' : '显示连线';
    toggle.setAttribute('aria-pressed', String(visible));
    overlay.toggleAttribute('hidden', !visible);
  }
  toggle.addEventListener('click', () => { visible = !visible; updateToggle(); schedule(); });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') { pinned = null; schedule(); }
  });
  document.addEventListener('scroll', schedule, { capture: true, passive: true });
  window.addEventListener('resize', schedule);
  narrow.addEventListener('change', schedule);
  new MutationObserver(refresh).observe(content, { childList: true });
  new MutationObserver(schedule).observe(left, { subtree: true, childList: true, attributes: true, attributeFilter: ['class', 'hidden'] });
  const dialog = document.querySelector('[aria-modal="true"]');
  if (dialog) new MutationObserver(schedule).observe(dialog, { attributes: true, attributeFilter: ['class', 'hidden'] });
  updateToggle();
  refresh();
})();
