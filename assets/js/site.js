/* Mama Africa — interactions (v3, editorial: quiet motion, no 3D) */
(function () {
  'use strict';
  var d = document, body = d.body;
  var REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var TOUCH = matchMedia('(pointer: coarse)').matches;
  var HOVER = matchMedia('(hover: hover) and (min-width: 961px)').matches;
  var WA = window.MA_WA || '41782597738';
  var hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);
  var waLink = function (t) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(t); };

  /* ---------- smooth scroll on desktop only ---------- */
  var lenis = null;
  if (!REDUCE && !TOUCH && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ duration: 1.15, smoothWheel: true });
    if (hasGsap) { lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(function (t) { lenis.raf(t * 1000); }); gsap.ticker.lagSmoothing(0); }
    else (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })();
  }
  var lock = function (on) { if (lenis) on ? lenis.stop() : lenis.start(); body.style.overflow = on ? 'hidden' : ''; };
  d.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href'); var el = id.length > 1 && d.querySelector(id);
      if (!el) return; e.preventDefault();
      if (lenis) lenis.scrollTo(el, { offset: -70 }); else el.scrollIntoView({ behavior: REDUCE ? 'auto' : 'smooth' });
    });
  });

  /* ---------- header & action bar ---------- */
  var hdr = d.getElementById('hdr'), abar = d.getElementById('abar');
  var darkTop = null;
  var lastY = 0;
  function onScroll() {
    var y = scrollY, h = darkTop ? darkTop.offsetHeight : 0;
    var solid = y > Math.max(40, h - 90);
    hdr.classList.toggle('is-solid', solid);
    if (!body.classList.contains('menu-open')) hdr.classList.toggle('is-hidden', y > lastY && y > h + 200);
    if (abar) abar.classList.toggle('is-away', y < 420);
    lastY = y;
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- menu ---------- */
  var burger = d.querySelector('.burger');
  function setMenu(open) {
    body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open);
    hdr.classList.remove('is-hidden'); lock(open);
  }
  if (burger) burger.addEventListener('click', function () { setMenu(!body.classList.contains('menu-open')); });
  d.querySelectorAll('.mnav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  /* ---------- booking sheet ---------- */
  var sheet = d.getElementById('sheet'), lastFocus = null;
  function openSheet() {
    if (body.classList.contains('menu-open')) setMenu(false);
    lastFocus = d.activeElement; sheet.classList.add('is-open'); sheet.setAttribute('aria-hidden', 'false');
    body.classList.add('sheet-open'); lock(true);
    setTimeout(function () { sheet.querySelector('.x').focus(); }, 60);
  }
  function closeSheet() {
    if (!sheet.classList.contains('is-open')) return;
    sheet.classList.remove('is-open'); sheet.setAttribute('aria-hidden', 'true'); body.classList.remove('sheet-open'); lock(false);
    if (lastFocus) lastFocus.focus();
  }
  d.querySelectorAll('[data-book]').forEach(function (b) { b.addEventListener('click', openSheet); });
  sheet.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', closeSheet); });

  /* ---------- lightbox ---------- */
  var lb = d.getElementById('lb'), list = [], li = 0;
  function show(i) {
    li = (i + list.length) % list.length;
    var im = lb.querySelector('img'); im.src = list[li].src; im.alt = list[li].cap || '';
    lb.querySelector('p').textContent = list[li].cap || '';
    lb.querySelector('.pv').hidden = lb.querySelector('.nx').hidden = list.length < 2;
  }
  function openLb(l, i) { list = l; show(i); lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false'); lock(true); lb.querySelector('.x').focus(); }
  function closeLb() { if (!lb.classList.contains('is-open')) return; lb.classList.remove('is-open'); lb.setAttribute('aria-hidden', 'true'); lock(false); }
  lb.querySelector('.x').addEventListener('click', closeLb);
  lb.querySelector('.pv').addEventListener('click', function () { show(li - 1); });
  lb.querySelector('.nx').addEventListener('click', function () { show(li + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
  d.querySelectorAll('[data-flyer]').forEach(function (b) {
    b.addEventListener('click', function () { openLb([{ src: 'assets/img/' + b.dataset.flyer + '.webp', cap: 'Affiche Mama Africa' }], 0); });
  });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (lb.classList.contains('is-open')) closeLb(); else if (sheet.classList.contains('is-open')) closeSheet(); else if (body.classList.contains('menu-open')) setMenu(false); }
    if (lb.classList.contains('is-open')) { if (e.key === 'ArrowLeft') show(li - 1); if (e.key === 'ArrowRight') show(li + 1); }
    if (e.key === 'Tab' && sheet.classList.contains('is-open')) {
      var f = sheet.querySelectorAll('a,button'); if (!f.length) return;
      if (e.shiftKey && d.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && d.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });

  /* ---------- hero entrance ---------- */
  var hero = d.getElementById('hero');
  if (hero) requestAnimationFrame(function () { requestAnimationFrame(function () { hero.classList.add('is-ready'); }); });

  /* ---------- quiet reveals ---------- */
  if (hasGsap && !REDUCE) {
    d.querySelectorAll('[data-reveal]').forEach(function (el) {
      ScrollTrigger.create({ trigger: el, start: 'top 94%', once: true, onEnter: function () { el.classList.add('is-in'); } });
    });
    d.querySelectorAll('.veil').forEach(function (v) {
      var c = v.querySelector('.veil-c'), m = v.querySelector('img');
      if (!c) return;
      gsap.set(c, { scaleY: 1 }); if (m) gsap.set(m, { scale: 1.12 });
      ScrollTrigger.create({ trigger: v, start: 'top 90%', once: true, onEnter: function () {
        gsap.to(c, { scaleY: 0, duration: 1.4, ease: 'expo.inOut' });
        if (m) gsap.to(m, { scale: 1, duration: 2, ease: 'expo.out' });
      } });
    });
    if (!TOUCH) {
      d.querySelectorAll('.phero .bg img, .phero .bg video').forEach(function (m) {
        gsap.to(m, { yPercent: 12, ease: 'none', scrollTrigger: { trigger: m.closest('.phero'), start: 'top top', end: 'bottom top', scrub: true } });
      });
      var hv = d.querySelector('.hero-media');
      if (hv) gsap.to(hv, { yPercent: 14, ease: 'none', scrollTrigger: { trigger: hero, start: 'top top', end: 'bottom top', scrub: true } });
    }
  } else {
    d.querySelectorAll('[data-reveal]').forEach(function (el) { el.classList.add('is-in'); });
    d.querySelectorAll('.veil-c').forEach(function (c) { c.remove(); });
  }

  /* ---------- signatures rail ---------- */
  var rail = d.getElementById('rail');
  if (rail) {
    var bar = d.querySelector('.rail-bar i');
    var upd = function () {
      var max = rail.scrollWidth - rail.clientWidth;
      var p = max > 0 ? rail.scrollLeft / max : 0;
      var w = Math.max(12, (rail.clientWidth / rail.scrollWidth) * 100);
      if (bar) { bar.style.width = w + '%'; bar.style.left = (p * (100 - w)) + '%'; }
    };
    rail.addEventListener('scroll', upd, { passive: true }); addEventListener('resize', upd); upd();
    d.querySelectorAll('[data-rail]').forEach(function (b) {
      b.addEventListener('click', function () {
        var card = rail.querySelector('.sig'); var step = card ? card.getBoundingClientRect().width + 24 : 400;
        rail.scrollBy({ left: step * (+b.dataset.rail), behavior: REDUCE ? 'auto' : 'smooth' });
      });
    });
    if (!TOUCH) { // drag to scroll with the mouse
      var down = false, sx = 0, sl = 0, moved = 0;
      rail.addEventListener('pointerdown', function (e) { if (e.pointerType !== 'mouse') return; down = true; moved = 0; sx = e.clientX; sl = rail.scrollLeft; rail.classList.add('is-drag'); });
      addEventListener('pointermove', function (e) { if (!down) return; var dx = e.clientX - sx; moved = Math.max(moved, Math.abs(dx)); rail.scrollLeft = sl - dx; });
      addEventListener('pointerup', function () { if (!down) return; down = false; rail.classList.remove('is-drag'); });
      rail.addEventListener('click', function (e) { if (moved > 6) { e.preventDefault(); e.stopPropagation(); } }, true);
      rail.addEventListener('dragstart', function (e) { e.preventDefault(); });
    }
  }

  /* ---------- la carte: a photo follows the cursor ---------- */
  var hov = d.getElementById('hover-img');
  if (hov && HOVER && !REDUCE) {
    var hImg = hov.querySelector('img'), tx = 0, ty = 0, x = 0, y = 0, on = false;
    d.querySelectorAll('.carte li[data-hover]').forEach(function (row) {
      row.addEventListener('mouseenter', function () { hImg.src = row.dataset.hover; on = true; hov.classList.add('is-on'); });
      row.addEventListener('mouseleave', function () { on = false; hov.classList.remove('is-on'); });
    });
    addEventListener('mousemove', function (e) { tx = e.clientX + 150; ty = e.clientY; });
    (function loop() { x += (tx - x) * 0.14; y += (ty - y) * 0.14; if (on) hov.style.left = x + 'px', hov.style.top = y + 'px'; requestAnimationFrame(loop); })();
  }

  /* ---------- services: the photo follows the hovered row ---------- */
  var svcPics = d.querySelectorAll('.svc-pic img');
  if (svcPics.length) d.querySelectorAll('.svc-row').forEach(function (row) {
    row.addEventListener('mouseenter', function () {
      d.querySelectorAll('.svc-row').forEach(function (r) { r.classList.toggle('is-on', r === row); });
      svcPics.forEach(function (p, i) { p.classList.toggle('is-on', i === +row.dataset.pic); });
    });
  });

  /* ---------- sound toggle on her videos ---------- */
  d.querySelectorAll('.snd').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.parentNode.querySelector('video'); if (!v) return;
      var on = v.muted;
      d.querySelectorAll('.vcard video').forEach(function (o) { o.muted = true; });
      d.querySelectorAll('.snd').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); o.setAttribute('aria-label', 'Activer le son'); });
      v.muted = !on;
      if (on) { v.currentTime = 0; var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      b.setAttribute('aria-pressed', on); b.setAttribute('aria-label', on ? 'Couper le son' : 'Activer le son');
    });
  });

  /* ---------- model codes ---------- */
  d.querySelectorAll('.codes').forEach(function (grid) {
    var box = grid.parentNode, sel = box.querySelector('#code-sel'), link = box.querySelector('#code-wa');
    grid.querySelectorAll('.code').forEach(function (b) {
      b.addEventListener('click', function () {
        grid.querySelectorAll('.code').forEach(function (z) { z.setAttribute('aria-pressed', z === b); });
        if (sel) sel.innerHTML = 'Votre choix : <em>code ' + b.dataset.code + '</em>, ' + b.dataset.price + ' CHF';
        if (link) link.href = waLink('Bonjour Mama Africa, je souhaite réserver le modèle code ' + b.dataset.code + ' (' + b.dataset.price + ' CHF). Quelles sont vos disponibilités ?');
      });
    });
  });

  /* ---------- hours ---------- */
  (function () {
    var now;
    try {
      var parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Zurich', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
      var get = function (t) { return (parts.find(function (p) { return p.type === t; }) || {}).value; };
      now = { day: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday')), min: (+get('hour') % 24) * 60 + (+get('minute')) };
    } catch (e) { var t = new Date(); now = { day: t.getDay(), min: t.getHours() * 60 + t.getMinutes() }; }
    d.querySelectorAll('.hours li').forEach(function (l) { if (+l.dataset.day === now.day) l.classList.add('is-today'); });
    var open = now.day >= 1 && now.day <= 6 && now.min >= 540 && now.min < 1110;
    d.querySelectorAll('#open-now').forEach(function (b) {
      b.classList.toggle('is-open', open);
      b.querySelector('span').textContent = open ? 'Ouvert · jusqu’à 18h30' : (now.day === 0 || (now.day === 6 && now.min >= 1110) ? 'Fermé · ouvre lundi à 9h00' : (now.min < 540 ? 'Fermé · ouvre à 9h00' : 'Fermé · ouvre demain à 9h00'));
    });
  })();

  /* ---------- gallery ---------- */
  var mas = d.getElementById('masonry');
  if (mas) {
    var figs = Array.prototype.slice.call(mas.querySelectorAll('figure'));
    d.querySelectorAll('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        d.querySelectorAll('[data-filter]').forEach(function (z) { z.setAttribute('aria-pressed', z === b); });
        figs.forEach(function (f) { f.classList.toggle('is-hidden', b.dataset.filter !== 'all' && f.dataset.cat !== b.dataset.filter); f.classList.add('is-in'); });
        if (hasGsap) ScrollTrigger.refresh();
      });
    });
    figs.forEach(function (f) {
      f.tabIndex = 0;
      var open = function () {
        var vis = figs.filter(function (z) { return !z.classList.contains('is-hidden'); });
        openLb(vis.map(function (z) { var im = z.querySelector('img'); return { src: im.currentSrc || im.src, cap: im.alt }; }), vis.indexOf(f));
      };
      f.addEventListener('click', open);
      f.addEventListener('keydown', function (e) { if (e.key === 'Enter') open(); });
    });
  }

  /* ---------- forms → WhatsApp ---------- */
  var bf = d.getElementById('book-form');
  if (bf) {
    var total = d.getElementById('bf-total');
    bf.date.min = new Date().toISOString().slice(0, 10);
    bf.addEventListener('change', function () {
      var sum = 0, ask = false;
      bf.querySelectorAll('input[name=svc]:checked').forEach(function (c) { if (+c.dataset.price) sum += +c.dataset.price; else ask = true; });
      total.textContent = sum + ' CHF' + (ask ? ' + sur demande' : '');
    });
    bf.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = bf.name.value.trim();
      if (!name) { bf.name.setCustomValidity('Merci d’indiquer votre nom'); bf.name.reportValidity(); bf.name.setCustomValidity(''); return; }
      var svc = Array.prototype.map.call(bf.querySelectorAll('input[name=svc]:checked'), function (c) { return '• ' + c.value; });
      var code = bf.querySelector('input[name=code]:checked');
      var dt = bf.date.value ? new Date(bf.date.value + 'T12:00').toLocaleDateString('fr-CH', { weekday: 'long', day: 'numeric', month: 'long' }) : 'à convenir';
      window.open(waLink('Bonjour Mama Africa, je souhaite prendre rendez-vous.\n\n' +
        (svc.length ? 'Prestation(s) :\n' + svc.join('\n') + '\n' : '') + (code ? 'Modèle : code ' + code.value + '\n' : '') +
        '\nDate souhaitée : ' + dt + '\nMoment : ' + bf.time.value + '\nNom : ' + name + (bf.tel.value ? '\nTéléphone : ' + bf.tel.value : '') +
        (bf.msg.value.trim() ? '\n\n' + bf.msg.value.trim() : '')), '_blank', 'noopener');
    });
  }
  var cf = d.getElementById('contact-form');
  if (cf) cf.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!cf.name.value.trim()) { cf.name.reportValidity(); return; }
    if (!cf.msg.value.trim()) { cf.msg.reportValidity(); return; }
    window.open(waLink('Bonjour Mama Africa,\n\n' + cf.msg.value.trim() + '\n\n— ' + cf.name.value.trim() + ' (' + cf.subj.value + ')'), '_blank', 'noopener');
  });

  /* ---------- pause off-screen videos (and only load the hero film that is shown) ---------- */
  d.querySelectorAll('.hero-media video').forEach(function (v) {
    if (getComputedStyle(v).display === 'none') { v.removeAttribute('autoplay'); v.preload = 'none'; v.pause(); v.removeAttribute('src'); v.load(); }
  });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { var v = e.target; if (!v.getAttribute('src')) return; if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause(); });
    }, { rootMargin: '200px' });
    d.querySelectorAll('video').forEach(function (v) { io.observe(v); });
  }

  window.__ma = true;
})();
