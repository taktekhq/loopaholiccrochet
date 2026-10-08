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
      chips.forEach(function (c) { c.removeAttribute('aria-current'); });
      if (current && byId[current.id]) {
        var chip = byId[current.id];
        chip.setAttribute('aria-current', 'true');
        var row = chip.closest('.chips');
        var r = chip.getBoundingClientRect(), rr = row.getBoundingClientRect();
        if (r.left < rr.left || r.right > rr.right) chip.scrollIntoView({ block: 'nearest', inline: 'nearest' });
      }
    }, { rootMargin: '-30% 0px -60% 0px' });
    cats.forEach(function (s) { cio.observe(s); });
  }
})();
