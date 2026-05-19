// Reveal on scroll
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Typewriter (Hero subtitle)
const tw = document.getElementById('typewriter');
if (tw) {
  const phrases = [
    window.__profile_title || 'Junior Python Developer',
    'Backend & Telegram Bots',
    'Django Enthusiast',
    'Problem Solver'
  ];
  let p = 0, c = 0, deleting = false;
  function tick() {
    const cur = phrases[p];
    if (!deleting) {
      tw.textContent = cur.slice(0, ++c);
      if (c === cur.length) { deleting = true; setTimeout(tick, 1600); return; }
    } else {
      tw.textContent = cur.slice(0, --c);
      if (c === 0) { deleting = false; p = (p + 1) % phrases.length; }
    }
    setTimeout(tick, deleting ? 40 : 80);
  }
  tick();
}

// Project image galleries (click dots to switch + auto-cycle on hover)
document.querySelectorAll('[data-gallery]').forEach(gal => {
  const slides = gal.querySelectorAll('.gallery-slide');
  const dots = gal.querySelectorAll('.gallery-dot');
  if (slides.length < 2) return;
  let idx = 0, timer = null;
  const show = (i) => {
    idx = (i + slides.length) % slides.length;
    slides.forEach((s, k) => s.style.opacity = k === idx ? '1' : '0');
    dots.forEach((d, k) => d.classList.toggle('bg-white', k === idx) || d.classList.toggle('bg-white/40', k !== idx));
  };
  dots.forEach(d => d.addEventListener('click', (e) => { e.preventDefault(); show(parseInt(d.dataset.idx)); }));
  gal.addEventListener('mouseenter', () => { timer = setInterval(() => show(idx + 1), 1800); });
  gal.addEventListener('mouseleave', () => { clearInterval(timer); show(0); });
});

// Smooth nav highlight
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', (e) => {
    const id = a.getAttribute('href');
    if (id.length > 1) {
      const el = document.querySelector(id);
      if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    }
  });
});

// Theme toggle (initial value is set inline in base.html <head> to avoid flash)
const themeBtn = document.getElementById('theme-toggle');
if (themeBtn) {
  themeBtn.addEventListener('click', () => {
    const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
}

// Follow OS theme changes only if the user hasn't explicitly chosen one.
if (window.matchMedia) {
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('theme')) {
      document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
    }
  });
}
