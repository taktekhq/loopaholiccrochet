/* Loopaholic: menu close behaviour + the product page's sticky order bar. No dependencies. */
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

  var inline = document.getElementById('order-cta');
  var bar = document.querySelector('.sticky-cta');
  if (inline && bar && 'IntersectionObserver' in window) {
    document.body.classList.add('has-sticky');
    // the root is stretched far below the viewport, so "not intersecting" means
    // "scrolled above the top", even when a fast scroll jumps straight past it
    new IntersectionObserver(function (entries) {
      var past = !entries[0].isIntersecting;
      bar.classList.toggle('on', past);
      bar.setAttribute('aria-hidden', past ? 'false' : 'true');
      bar.querySelector('a').tabIndex = past ? 0 : -1;
    }, { rootMargin: '0px 0px 100000px 0px' }).observe(inline);
  }
})();
