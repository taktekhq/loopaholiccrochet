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
    new IntersectionObserver(function (entries) {
      var e = entries[0];
      var past = !e.isIntersecting && e.boundingClientRect.top < 0;
      bar.classList.toggle('on', past);
      bar.setAttribute('aria-hidden', past ? 'false' : 'true');
      bar.querySelector('a').tabIndex = past ? 0 : -1;
    }).observe(inline);
  }
})();
