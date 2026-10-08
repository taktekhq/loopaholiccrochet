/* Loopaholic: menu close behaviour, the sticky order bar, and the shop's current-category chip.
   No dependencies. */
(function () {
  var menu = document.querySelector('.menu');
  if (menu) {
    var summary = menu.querySelector('summary');
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.open) { menu.open = false; summary.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (menu.open && !menu.contains(e.target)) menu.open = false;
    });
    menu.addEventListener('toggle', function () {
      summary.setAttribute('aria-expanded', menu.open ? 'true' : 'false');
    });
  }

  if (!('IntersectionObserver' in window)) return;

  // Sticky order bar: shown whenever no inline order button is on screen
  // (above or below the viewport), hidden as soon as one is visible.
  var ctas = document.querySelectorAll('[data-order-cta]');
  var bar = document.querySelector('.sticky-cta');
  if (ctas.length && bar) {
    document.body.classList.add('has-sticky');
    var link = bar.querySelector('a');
    var seen = new Map();
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { seen.set(e.target, e.isIntersecting); });
      var show = true;
      seen.forEach(function (v) { if (v) show = false; });
      bar.classList.toggle('on', show);
      bar.setAttribute('aria-hidden', show ? 'false' : 'true');
      link.tabIndex = show ? 0 : -1;
    });
    ctas.forEach(function (c) { io.observe(c); });
  }

  // Shop: mark the chip of the section being read.
  var chips = document.querySelectorAll('.chip');
  var cats = document.querySelectorAll('.cat');
  if (chips.length && cats.length) {
    var byId = {};
    chips.forEach(function (c) { byId[c.getAttribute('href').slice(1)] = c; });
    var visible = new Map();
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { visible.set(e.target, e.isIntersecting); });
      var current = null;
      cats.forEach(function (s) { if (!current && visible.get(s)) current = s; });
      // at the very bottom the last short sections never reach the band: mark the last one
      if (innerHeight + scrollY >= document.documentElement.scrollHeight - 2) current = cats[cats.length - 1];
      // above the first section: nothing is current, and the row goes back to its start
      if (!current && cats[0].getBoundingClientRect().top > innerHeight * 0.3) {
        chips.forEach(function (c) { c.removeAttribute('aria-current'); });
        var row0 = chips[0].closest('.chips'), c0 = chips[0].getBoundingClientRect(), r0 = row0.getBoundingClientRect();
        if (c0.left < r0.left || c0.right > r0.right) row0.scrollBy({ left: c0.left - r0.left - (document.dir === 'rtl' ? r0.width - c0.width - 16 : 16) });
        return;
      }
      if (!current) return;   // between sections: keep the last one marked
      chips.forEach(function (c) { c.removeAttribute('aria-current'); });
      if (current && byId[current.id]) {
        var chip = byId[current.id];
        chip.setAttribute('aria-current', 'true');
        // scroll only the chip row (physical delta, so it works in RTL); never the window
        var row = chip.closest('.chips');
        var r = chip.getBoundingClientRect(), rr = row.getBoundingClientRect();
        if (r.left < rr.left || r.right > rr.right) {
          row.scrollBy({ left: r.left - rr.left - (rr.width - r.width) / 2, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
        }
      }
    }, { rootMargin: '-30% 0px -60% 0px' });
    cats.forEach(function (s) { cio.observe(s); });
    addEventListener('scroll', function () {
      if (innerHeight + scrollY >= document.documentElement.scrollHeight - 2) {
        chips.forEach(function (c) { c.removeAttribute('aria-current'); });
        var last = byId[cats[cats.length - 1].id];
        if (last) last.setAttribute('aria-current', 'true');
      }
    }, { passive: true });
  }
  // Product page: the loupe becomes a magnifier over Rana's full photo (1 photo pixel per
  // CSS pixel). Mouse: follows the pointer. Touch: tap the photo, or drag the ring.
  // Keyboard: the ring is focusable, arrow keys move it, Escape puts it back.
  // Without JS (or before first use) it stays the static close-up crop.
  var gal = document.querySelector('.pdp .gallery');
  var lp = gal && gal.querySelector('.loupe[data-full]');
  if (lp) {
    var tile = gal.querySelector('.tile');
    var photo = tile.querySelector('img');
    var lens = null, live = false, pos = { x: 0.5, y: 0.5 }, base = null, dragging = false;
    var SRC = 1200;  // the full photo is 1200 px square
    lp.tabIndex = 0;
    lp.setAttribute('role', 'application');
    lp.setAttribute('aria-roledescription', lp.dataset.role);
    lp.setAttribute('aria-label', lp.dataset.label);

    var full = function () {
      var u = photo.currentSrc || photo.src;
      return /\.avif/.test(u) ? lp.dataset.full + '.avif' : lp.dataset.full + '.jpg';
    };
    var ensure = function () {
      if (lens) return;
      lens = document.createElement('span');
      lens.className = 'loupe-lens';
      lens.setAttribute('aria-hidden', 'true');
      lens.style.backgroundImage = 'url("' + (photo.currentSrc || photo.src) + '")';
      lp.appendChild(lens);
      var hi = new Image();
      hi.onload = function () { lens.style.backgroundImage = 'url("' + hi.src + '")'; };
      hi.src = full();
    };
    var measure = function () {
      lp.style.transform = '';
      var t = tile.getBoundingClientRect(), l = lp.getBoundingClientRect();
      base = { left: l.left - t.left, top: l.top - t.top, size: l.width, w: t.width, h: t.height };
    };
    var render = function () {
      var cx = pos.x * base.w, cy = pos.y * base.h;
      lp.style.transform = 'translate(' + (cx - base.size / 2 - base.left) + 'px,' + (cy - base.size / 2 - base.top) + 'px)';
      var inner = lp.clientWidth;
      lens.style.backgroundSize = SRC + 'px ' + SRC + 'px';
      lens.style.backgroundPosition = (inner / 2 - pos.x * SRC) + 'px ' + (inner / 2 - pos.y * SRC) + 'px';
    };
    var start = function () {
      if (live) return;
      ensure(); measure(); live = true; lp.classList.add('is-live');
    };
    var stop = function () {
      live = false; dragging = false; lp.classList.remove('is-live'); lp.style.transform = '';
    };
    var at = function (e) {
      var t = tile.getBoundingClientRect();
      pos.x = Math.min(1, Math.max(0, (e.clientX - t.left) / t.width));
      pos.y = Math.min(1, Math.max(0, (e.clientY - t.top) / t.height));
    };

    gal.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'mouse' || dragging) { start(); at(e); render(); }
    });
    gal.addEventListener('pointerleave', function (e) { if (e.pointerType === 'mouse') stop(); });
    tile.addEventListener('click', function (e) { start(); at(e); render(); });
    var fromRing = function () {  // go live where the ring already sits
      var l = lp.getBoundingClientRect(), t = tile.getBoundingClientRect();
      start();
      pos.x = Math.min(1, Math.max(0, (l.left + l.width / 2 - t.left) / t.width));
      pos.y = Math.min(1, Math.max(0, (l.top + l.height / 2 - t.top) / t.height));
      render();
    };
    lp.addEventListener('pointerdown', function (e) {
      if (e.pointerType === 'mouse') return;
      if (!live) fromRing();
      dragging = true; lp.setPointerCapture(e.pointerId); e.preventDefault();
    });
    lp.addEventListener('pointerup', function () { dragging = false; });
    lp.addEventListener('pointercancel', function () { dragging = false; });
    lp.addEventListener('focus', function () { if (!live) fromRing(); });
    lp.addEventListener('blur', function () { if (!dragging) stop(); });
    document.addEventListener('pointerdown', function (e) { if (live && !gal.contains(e.target)) stop(); });
    lp.addEventListener('keydown', function (e) {
      var step = e.shiftKey ? 0.12 : 0.04;
      var k = { ArrowLeft: [-step, 0], ArrowRight: [step, 0], ArrowUp: [0, -step], ArrowDown: [0, step] }[e.key];
      if (e.key === 'Escape') { stop(); return; }
      if (!k) return;
      e.preventDefault();
      if (!live) start();
      pos.x = Math.min(1, Math.max(0, pos.x + k[0]));
      pos.y = Math.min(1, Math.max(0, pos.y + k[1]));
      render();
    });
    addEventListener('resize', function () { if (live) { measure(); render(); } });
  }
})();
