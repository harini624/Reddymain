/* Accessible, mobile-only navigation toggle. */
(() => {
  const toggle = document.querySelector('.mobile-nav-toggle');
  const menu = document.querySelector('#site-navigation-links');
  const navbar = document.querySelector('.main-navbar');
  if (!toggle || !menu || !navbar) return;

  const mobileQuery = window.matchMedia('(max-width: 768px)');
  const setOpen = (open) => {
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
  };

  toggle.addEventListener('click', () => {
    setOpen(toggle.getAttribute('aria-expanded') !== 'true');
  });

  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) setOpen(false);
  });

  document.addEventListener('click', (event) => {
    if (mobileQuery.matches && !navbar.contains(event.target)) setOpen(false);
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      setOpen(false);
      toggle.focus();
    }
  });

  const resetForViewport = () => {
    if (!mobileQuery.matches) setOpen(false);
  };
  if (mobileQuery.addEventListener) mobileQuery.addEventListener('change', resetForViewport);
  else mobileQuery.addListener(resetForViewport);
})();
