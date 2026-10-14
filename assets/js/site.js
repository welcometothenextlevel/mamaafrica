/* Mama Africa Beauty — interactions */
(function () {
  'use strict';
  var d = document, html = d.documentElement, body = d.body;
  var REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var MOBILE = function () { return innerWidth <= 760; };
  var WA = '41782597738';
  var hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);

  /* ---------- smooth scroll ---------- */
  var lenis = null;
  var TOUCH = matchMedia('(pointer: coarse)').matches;
  // phones keep native momentum scrolling: smoothing it fights iOS and adds lag
  if (!REDUCE && !TOUCH && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ duration: 1.15, smoothWheel: true, wheelMultiplier: 0.95 });
    if (hasGsap) {
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
      gsap.ticker.lagSmoothing(0);
    } else {
      (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })();
    }
  }
  d.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var id = a.getAttribute('href');
      if (id.length < 2) return;
      var el = d.querySelector(id);
      if (!el) return;
      e.preventDefault();
      if (lenis) lenis.scrollTo(el, { offset: -90 }); else el.scrollIntoView({ behavior: 'smooth' });
    });
  });

  /* ---------- header ---------- */
  var hdr = d.getElementById('hdr'), mbar = d.getElementById('mbar');
  var lastY = 0;
  function onScroll() {
    var y = scrollY;
    hdr.classList.toggle('is-solid', y > 30);
    var down = y > lastY && y > 500;
    if (!body.classList.contains('menu-open')) hdr.classList.toggle('is-hidden', down);
    lastY = y;
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  var burger = d.querySelector('.burger');
  function setMenu(open) {
    body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open);
    hdr.classList.remove('is-hidden');
    if (mbar) mbar.classList.toggle('is-hidden', open);
    if (lenis) open ? lenis.stop() : lenis.start();
    body.style.overflow = open ? 'hidden' : '';
  }
  if (burger) burger.addEventListener('click', function () { setMenu(!body.classList.contains('menu-open')); });
  d.querySelectorAll('.mnav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  /* ---------- booking sheet ---------- */
  var sheet = d.getElementById('sheet'), lastFocus = null;
  function openSheet() {
    if (body.classList.contains('menu-open')) setMenu(false);
    lastFocus = d.activeElement;
    sheet.classList.add('is-open');
    sheet.setAttribute('aria-hidden', 'false');
    if (lenis) lenis.stop();
    setTimeout(function () { var f = sheet.querySelector('.way'); if (f) f.focus(); }, 60);
  }
  function closeSheet() {
    sheet.classList.remove('is-open');
    sheet.setAttribute('aria-hidden', 'true');
    if (lenis) lenis.start();
    if (lastFocus) lastFocus.focus();
  }
  d.querySelectorAll('[data-book]').forEach(function (b) { b.addEventListener('click', openSheet); });
  sheet.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', closeSheet); });
  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (sheet.classList.contains('is-open')) closeSheet();
      if (body.classList.contains('menu-open')) setMenu(false);
      closeLb();
    }
    if (e.key === 'Tab' && sheet.classList.contains('is-open')) {
      var f = sheet.querySelectorAll('a,button');
      if (e.shiftKey && d.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && d.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });

  /* ---------- split headings ---------- */
  function split(el) {
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var parts = n.textContent.split(/(\s+)/);
          var frag = d.createDocumentFragment();
          parts.forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(d.createTextNode(' ')); return; }
            var w = d.createElement('span'); w.className = 'split-w';
            var i = d.createElement('span'); i.textContent = p;
            w.appendChild(i); frag.appendChild(w);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== 'BR') {
          walk(n);
        }
      });
    };
    walk(el);
  }

  if (hasGsap && !REDUCE) {
    d.querySelectorAll('[data-split]').forEach(function (el) {
      split(el);
      var words = el.querySelectorAll('.split-w>span');
      gsap.set(words, { yPercent: 115 });
      el.style.visibility = 'visible';
      ScrollTrigger.create({
        trigger: el, start: 'top 97%', once: true,
        onEnter: function () { gsap.to(words, { yPercent: 0, duration: 1.15, ease: 'expo.out', stagger: 0.055 }); }
      });
    });

    /* reveals */
    d.querySelectorAll('[data-reveal]').forEach(function (el) {
      ScrollTrigger.create({ trigger: el, start: 'top 98%', once: true, onEnter: function () { el.classList.add('is-in'); } });
    });

    /* image veils */
    d.querySelectorAll('.veil').forEach(function (el) {
      var c = el.querySelector('.veil-c'), m = el.querySelector('img,video');
      if (!c) return;
      gsap.set(c, { scaleY: 1 });
      if (m) gsap.set(m, { scale: 1.18 });
      ScrollTrigger.create({
        trigger: el, start: 'top 85%', once: true,
        onEnter: function () {
          gsap.to(c, { scaleY: 0, duration: 1.3, ease: 'expo.inOut' });
          if (m) gsap.to(m, { scale: 1, duration: 1.8, ease: 'expo.out' });
        }
      });
    });

    /* soft parallax on arch frames */
    if (!MOBILE()) d.querySelectorAll('.arch video, .phero-media img, .phero-media video').forEach(function (m) {
      gsap.to(m, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: m.parentNode, start: 'top top', end: 'bottom top', scrub: true } });
    });
  } else {
    d.querySelectorAll('[data-reveal]').forEach(function (el) { el.classList.add('is-in'); });
    d.querySelectorAll('[data-split]').forEach(function (el) { el.style.visibility = 'visible'; });
    d.querySelectorAll('.veil-c').forEach(function (c) { c.remove(); });
  }

  /* ---------- tilt cards ---------- */
  if (!REDUCE && matchMedia('(hover:hover)').matches) {
    d.querySelectorAll('[data-tilt]').forEach(function (el) {
      el.addEventListener('pointermove', function (e) {
        var r = el.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = 'rotateY(' + x * 8 + 'deg) rotateX(' + -y * 8 + 'deg) translateZ(0)';
      });
      el.addEventListener('pointerleave', function () { el.style.transform = ''; });
    });
  }

  /* ---------- weave story ---------- */
  var weave = d.querySelector('.weave');
  var steps = weave ? weave.querySelectorAll('.weave-step') : [];
  var bars = weave ? weave.querySelectorAll('.weave-bar i') : [];
  var weaveKey = -1;
  function weaveTick() {
    if (!weave) return;
    var r = weave.getBoundingClientRect();
    var span = r.height - innerHeight;
    var p = Math.min(1, Math.max(0, -r.top / span));
    var q = Math.min(1, Math.max(0, (p - 0.12) / 0.76));
    var idx = Math.min(3, Math.floor(q * 4));
    if (r.bottom < -50 || r.top > innerHeight + 50) return;
    var key = Math.round(q * 200);
    if (key === weaveKey) return;
    weaveKey = key;
    steps.forEach(function (s, i) { s.classList.toggle('is-on', i === idx); });
    bars.forEach(function (b, i) { b.style.setProperty('--p', Math.min(1, Math.max(0, q * 4 - i)).toFixed(3)); });
  }

  /* ---------- horizontal catalogue ---------- */
  var hcat = d.querySelector('.hcat'), track = hcat && hcat.querySelector('.hcat-track'), hbar = hcat && hcat.querySelector('.hcat-progress i');
  var hDist = 0;
  function hcatSize() {
    if (!hcat) return;
    if (MOBILE()) { hcat.style.height = ''; track.style.transform = ''; return; }
    hDist = Math.max(0, track.scrollWidth - innerWidth);
    hcat.style.height = (innerHeight + hDist) + 'px';
  }
  function hcatTick() {
    if (!hcat || MOBILE()) return;
    var r = hcat.getBoundingClientRect();
    var span = r.height - innerHeight;
    var p = span > 0 ? Math.min(1, Math.max(0, -r.top / span)) : 0;
    track.style.transform = 'translate3d(' + (-p * hDist) + 'px,0,0)';
    if (hbar) hbar.style.transform = 'scaleX(' + p + ')';
  }
  hcatSize();
  addEventListener('resize', function () { hcatSize(); if (hasGsap) ScrollTrigger.refresh(); });
  addEventListener('load', function () { hcatSize(); if (hasGsap) ScrollTrigger.refresh(); });

  function frame() { weaveTick(); hcatTick(); requestAnimationFrame(frame); }
  requestAnimationFrame(frame);

  /* ---------- before / after ---------- */
  d.querySelectorAll('[data-ba]').forEach(function (ba) {
    var range = ba.querySelector('input[type=range]'), drag = false;
    function set(pct) { pct = Math.max(2, Math.min(98, pct)); ba.style.setProperty('--x', pct + '%'); if (range) range.value = pct; }
    function fromEvent(e) { var r = ba.getBoundingClientRect(); set(((e.clientX - r.left) / r.width) * 100); }
    ba.addEventListener('pointerdown', function (e) { drag = true; ba.setPointerCapture(e.pointerId); fromEvent(e); });
    ba.addEventListener('pointermove', function (e) { if (drag) fromEvent(e); });
    ba.addEventListener('pointerup', function () { drag = false; });
    ba.addEventListener('pointercancel', function () { drag = false; });
    if (range) range.addEventListener('input', function () { set(+range.value); });
    if (hasGsap && !REDUCE) {
      var o = { v: 50 };
      ScrollTrigger.create({
        trigger: ba, start: 'top 70%', once: true,
        onEnter: function () {
          gsap.timeline().to(o, { v: 22, duration: 0.9, ease: 'power3.inOut', onUpdate: function () { set(o.v); } })
            .to(o, { v: 76, duration: 1.1, ease: 'power3.inOut', onUpdate: function () { set(o.v); } })
            .to(o, { v: 50, duration: 0.8, ease: 'power3.inOut', onUpdate: function () { set(o.v); } });
        }
      });
    }
  });

  /* ---------- hours: today + open now (Payerne time) ---------- */
  (function () {
    var now;
    try {
      var parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Zurich', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
      var get = function (t) { return (parts.find(function (p) { return p.type === t; }) || {}).value; };
      var wd = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday'));
      now = { day: wd, min: (+get('hour') % 24) * 60 + (+get('minute')) };
    } catch (e) { var t = new Date(); now = { day: t.getDay(), min: t.getHours() * 60 + t.getMinutes() }; }
    d.querySelectorAll('.hours li').forEach(function (li) { if (+li.dataset.day === now.day) li.classList.add('is-today'); });
    var open = now.day >= 1 && now.day <= 6 && now.min >= 540 && now.min < 1110;
    d.querySelectorAll('#open-now').forEach(function (b) {
      b.classList.toggle('is-open', open);
      b.querySelector('span').textContent = open ? 'Ouvert maintenant · jusqu’à 18h30' : (now.day === 0 || (now.day === 6 && now.min >= 1110) ? 'Fermé · ouvre lundi à 9h00' : (now.min < 540 ? 'Fermé · ouvre à 9h00' : 'Fermé · ouvre demain à 9h00'));
    });
  })();

  /* ---------- gallery filter + lightbox ---------- */
  var lb = d.getElementById('lb'), lbList = [], lbI = 0;
  function showLb(i) {
    lbI = (i + lbList.length) % lbList.length;
    var f = lbList[lbI], im = f.querySelector('img');
    lb.querySelector('img').src = im.currentSrc || im.src;
    lb.querySelector('img').alt = im.alt;
    lb.querySelector('p').textContent = (f.querySelector('figcaption') || {}).textContent || '';
  }
  function closeLb() { if (lb && lb.classList.contains('is-open')) { lb.classList.remove('is-open'); lb.setAttribute('aria-hidden', 'true'); if (lenis) lenis.start(); } }
  var mas = d.getElementById('masonry');
  if (mas) {
    var figs = Array.prototype.slice.call(mas.querySelectorAll('figure'));
    d.querySelectorAll('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        d.querySelectorAll('[data-filter]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
        var k = b.dataset.filter;
        figs.forEach(function (f) { f.classList.toggle('is-hidden', k !== 'all' && f.dataset.cat !== k); f.classList.add('is-in'); });
        if (hasGsap) ScrollTrigger.refresh();
      });
    });
    figs.forEach(function (f) {
      f.tabIndex = 0;
      var open = function () {
        lbList = figs.filter(function (x) { return !x.classList.contains('is-hidden'); });
        showLb(lbList.indexOf(f));
        lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false');
        if (lenis) lenis.stop();
        lb.querySelector('.x').focus();
      };
      f.addEventListener('click', open);
      f.addEventListener('keydown', function (e) { if (e.key === 'Enter') open(); });
    });
    lb.querySelector('.x').addEventListener('click', closeLb);
    lb.querySelector('.pv').addEventListener('click', function () { showLb(lbI - 1); });
    lb.querySelector('.nx').addEventListener('click', function () { showLb(lbI + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
    d.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'ArrowLeft') showLb(lbI - 1);
      if (e.key === 'ArrowRight') showLb(lbI + 1);
    });
  }

  /* ---------- forms → WhatsApp ---------- */
  function openWa(text) { window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(text), '_blank', 'noopener'); }
  var bf = d.getElementById('book-form');
  if (bf) {
    var total = d.getElementById('bf-total');
    var date = d.getElementById('bf-date');
    var today = new Date(); date.min = today.toISOString().slice(0, 10);
    var upd = function () {
      var sum = 0, demand = false;
      bf.querySelectorAll('input[name=svc]:checked').forEach(function (c) { var p = +c.dataset.price; if (p) sum += p; else demand = true; });
      total.textContent = (sum ? sum + ' CHF' : '0 CHF') + (demand ? ' + sur demande' : '');
    };
    bf.addEventListener('change', upd);
    bf.addEventListener('submit', function (e) {
      e.preventDefault();
      var name = bf.name.value.trim();
      if (!name) { bf.name.focus(); bf.name.setCustomValidity('Merci d’indiquer votre nom'); bf.name.reportValidity(); return; }
      bf.name.setCustomValidity('');
      var svc = Array.prototype.map.call(bf.querySelectorAll('input[name=svc]:checked'), function (c) { return '• ' + c.value; });
      var dt = bf.date.value ? new Date(bf.date.value + 'T12:00').toLocaleDateString('fr-CH', { weekday: 'long', day: 'numeric', month: 'long' }) : 'à convenir';
      var msg = 'Bonjour Mama Africa, je souhaite prendre rendez-vous.\n\n' +
        (svc.length ? 'Prestation(s) :\n' + svc.join('\n') + '\n\n' : '') +
        'Date souhaitée : ' + dt + '\nMoment : ' + bf.time.value + '\n' +
        'Nom : ' + name + (bf.tel.value ? '\nTéléphone : ' + bf.tel.value : '') +
        (bf.msg.value.trim() ? '\n\n' + bf.msg.value.trim() : '');
      openWa(msg);
    });
  }
  var cf = d.getElementById('contact-form');
  if (cf) {
    cf.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!cf.name.value.trim()) { cf.name.reportValidity(); return; }
      if (!cf.msg.value.trim()) { cf.msg.reportValidity(); return; }
      openWa('Bonjour Mama Africa,\n\n' + cf.msg.value.trim() + '\n\n— ' + cf.name.value.trim() + ' (' + cf.subj.value + ')');
    });
  }

  /* ---------- pause off-screen videos ---------- */
  if ('IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting) { var p = v.play(); if (p && p.catch) p.catch(function () {}); } else v.pause();
      });
    }, { rootMargin: '200px' });
    d.querySelectorAll('video').forEach(function (v) { vio.observe(v); });
  }

  window.__ma = true;
})();
