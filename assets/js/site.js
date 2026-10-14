/* Mama Africa Beauty — interactions (v2) */
(function () {
  'use strict';
  var d = document, body = d.body;
  var REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var TOUCH = matchMedia('(pointer: coarse)').matches;
  var MOBILE = function () { return innerWidth <= 760; };
  var WA = window.MA_WA || '41782597738';
  var OFFERS = window.MA_OFFERS || {};
  var hasGsap = typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined';
  if (hasGsap) gsap.registerPlugin(ScrollTrigger);
  var waLink = function (t) { return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(t); };

  /* ---------- smooth scroll (desktop only: phones keep native momentum) ---------- */
  var lenis = null;
  if (!REDUCE && !TOUCH && typeof Lenis !== 'undefined') {
    lenis = new Lenis({ duration: 1.1, smoothWheel: true });
    if (hasGsap) { lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(function (t) { lenis.raf(t * 1000); }); gsap.ticker.lagSmoothing(0); }
    else (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })();
  }
  var lockScroll = function (on) { if (lenis) on ? lenis.stop() : lenis.start(); body.style.overflow = on ? 'hidden' : ''; };
  d.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var el = a.getAttribute('href').length > 1 && d.querySelector(a.getAttribute('href'));
      if (!el) return;
      e.preventDefault();
      if (lenis) lenis.scrollTo(el, { offset: -80 }); else el.scrollIntoView({ behavior: REDUCE ? 'auto' : 'smooth' });
    });
  });

  /* ---------- header ---------- */
  var hdr = d.getElementById('hdr'), lastY = 0;
  function onScroll() {
    var y = scrollY;
    hdr.classList.toggle('is-solid', y > 24);
    if (!body.classList.contains('menu-open')) hdr.classList.toggle('is-hidden', y > lastY && y > 600);
    lastY = y;
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- menu ---------- */
  var burger = d.querySelector('.burger');
  function setMenu(open) {
    body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open);
    hdr.classList.remove('is-hidden');
    lockScroll(open);
  }
  if (burger) burger.addEventListener('click', function () { setMenu(!body.classList.contains('menu-open')); });
  d.querySelectorAll('.mnav a').forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });

  /* ---------- sheets (booking, offer) ---------- */
  var openSheetEl = null, lastFocus = null;
  function openSheet(el) {
    if (body.classList.contains('menu-open')) setMenu(false);
    lastFocus = d.activeElement; openSheetEl = el;
    el.classList.add('is-open'); el.setAttribute('aria-hidden', 'false');
    body.classList.add('sheet-open'); lockScroll(true);
    setTimeout(function () { var f = el.querySelector('.x'); if (f) f.focus(); }, 50);
  }
  function closeSheet() {
    if (!openSheetEl) return;
    openSheetEl.classList.remove('is-open'); openSheetEl.setAttribute('aria-hidden', 'true');
    openSheetEl = null; body.classList.remove('sheet-open'); lockScroll(false);
    if (lastFocus) lastFocus.focus();
  }
  var sheet = d.getElementById('sheet'), offer = d.getElementById('offer');
  d.querySelectorAll('[data-book]').forEach(function (b) { b.addEventListener('click', function () { openSheet(sheet); }); });
  d.querySelectorAll('.sheet [data-close]').forEach(function (b) { b.addEventListener('click', closeSheet); });

  function showOffer(id) {
    var o = OFFERS[id]; if (!o) return;
    var q = function (k) { return offer.querySelector('[data-o="' + k + '"]'); };
    q('img').src = 'assets/img/' + o.img + '.webp'; q('img').alt = o.title;
    q('badge').textContent = o.badge; q('title').textContent = o.title;
    q('price').innerHTML = '<span class="price">' + (o.pre ? '<em>' + o.pre + '</em>' : '') + o.price + '<small>CHF</small></span>';
    q('lead').textContent = o.lead;
    q('incl').innerHTML = o.incl.map(function (x) { return '<li>' + x + '</li>'; }).join('');
    q('wa').href = waLink('Bonjour Mama Africa, je souhaite réserver l’offre « ' + o.title + ' » (' + o.price + ' CHF).');
    var fb = q('flyer');
    fb.hidden = !o.flyer;
    fb.onclick = function () { openLb([{ src: 'assets/img/' + o.flyer + '.webp', cap: 'Affiche : ' + o.title }], 0); };
    openSheet(offer);
  }

  /* ---------- lightbox ---------- */
  var lb = d.getElementById('lb'), lbList = [], lbI = 0;
  function lbShow(i) {
    lbI = (i + lbList.length) % lbList.length;
    lb.querySelector('img').src = lbList[lbI].src;
    lb.querySelector('img').alt = lbList[lbI].cap || '';
    lb.querySelector('p').textContent = lbList[lbI].cap || '';
    lb.querySelector('.pv').hidden = lb.querySelector('.nx').hidden = lbList.length < 2;
  }
  function openLb(list, i) { lbList = list; lbShow(i); lb.classList.add('is-open'); lb.setAttribute('aria-hidden', 'false'); lockScroll(true); lb.querySelector('.x').focus(); }
  function closeLb() { if (!lb.classList.contains('is-open')) return; lb.classList.remove('is-open'); lb.setAttribute('aria-hidden', 'true'); lockScroll(!!openSheetEl); }
  lb.querySelector('.x').addEventListener('click', closeLb);
  lb.querySelector('.pv').addEventListener('click', function () { lbShow(lbI - 1); });
  lb.querySelector('.nx').addEventListener('click', function () { lbShow(lbI + 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) closeLb(); });
  d.querySelectorAll('[data-flyer]').forEach(function (b) {
    b.addEventListener('click', function () { openLb([{ src: 'assets/img/' + b.dataset.flyer + '.webp', cap: 'Affiche Mama Africa' }], 0); });
  });

  d.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { if (lb.classList.contains('is-open')) closeLb(); else if (openSheetEl) closeSheet(); else if (body.classList.contains('menu-open')) setMenu(false); }
    if (lb.classList.contains('is-open')) { if (e.key === 'ArrowLeft') lbShow(lbI - 1); if (e.key === 'ArrowRight') lbShow(lbI + 1); }
    if (e.key === 'Tab' && openSheetEl) {
      var f = Array.prototype.filter.call(openSheetEl.querySelectorAll('a,button'), function (x) { return !x.hidden; });
      if (!f.length) return;
      if (e.shiftKey && d.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && d.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });

  /* ---------- reveals ---------- */
  function split(el) {
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = d.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (p) {
            if (!p) return;
            if (/^\s+$/.test(p)) { frag.appendChild(d.createTextNode(' ')); return; }
            var w = d.createElement('span'); w.className = 'split-w';
            var i = d.createElement('span'); i.textContent = p; w.appendChild(i); frag.appendChild(w);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== 'BR' && n.tagName !== 'svg') walk(n);
      });
    })(el);
  }
  if (hasGsap && !REDUCE) {
    d.querySelectorAll('[data-split]').forEach(function (el) {
      split(el);
      var w = el.querySelectorAll('.split-w>span');
      gsap.set(w, { yPercent: 110 });
      el.style.visibility = 'visible';
      ScrollTrigger.create({ trigger: el, start: 'top 96%', once: true, onEnter: function () { gsap.to(w, { yPercent: 0, duration: 1.05, ease: 'expo.out', stagger: 0.05 }); } });
    });
    d.querySelectorAll('[data-reveal]').forEach(function (el) {
      ScrollTrigger.create({ trigger: el, start: 'top 98%', once: true, onEnter: function () { el.classList.add('is-in'); } });
    });
  } else {
    d.querySelectorAll('[data-reveal]').forEach(function (el) { el.classList.add('is-in'); });
    d.querySelectorAll('[data-split]').forEach(function (el) { el.style.visibility = 'visible'; });
  }

  /* ---------- hero progress (labels only; the braid reads scroll itself) ---------- */
  var hero = d.querySelector('[data-braid-hero]'), heroStep = d.getElementById('hero-step'), heroHint = d.querySelector('.hero-hint');
  var STEPS = ['Trois mèches', 'Croiser, serrer', 'Tresser', 'La signature'], lastStep = -1, lastHp = -1;
  function heroTick() {
    if (!hero) return;
    var r = hero.getBoundingClientRect();
    if (r.bottom < 0) return;
    var hp = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - innerHeight)));
    if (Math.abs(hp - lastHp) < 0.004) return;
    lastHp = hp;
    if (heroHint) heroHint.style.setProperty('--hp', hp.toFixed(3));
    var s = Math.min(3, Math.floor((hp / 0.66) * 4));
    if (s !== lastStep && heroStep) { heroStep.textContent = STEPS[s]; lastStep = s; }
  }

  /* ---------- 3D offer ring ---------- */
  var stage = d.getElementById('ring');
  var ringState = null;
  if (stage) {
    var ringEl = stage.querySelector('.ring'), cards = Array.prototype.slice.call(ringEl.children);
    var n = cards.length, step = 360 / n, rot = 0, vel = 0, drag = false, moved = 0, startX = 0, startRot = 0, lastX = 0, lastT = 0, target = null;
    var layoutRing = function () {
      var cw = MOBILE() ? Math.min(250, innerWidth * 0.62) : 300;
      var R = Math.round((cw / 2) / Math.tan(Math.PI / n) + (MOBILE() ? 26 : 60));
      stage.style.setProperty('--cw', cw + 'px');
      cards.forEach(function (c, i) { c.style.transform = 'rotateY(' + (i * step) + 'deg) translateZ(' + R + 'px)'; });
      ringEl.style.setProperty('--R', R);
      ringState = { R: R };
    };
    layoutRing(); addEventListener('resize', layoutRing);
    var inView = true;
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { inView = es[0].isIntersecting; }).observe(stage);
    var paint = function () {
      ringEl.style.transform = 'translateZ(' + (-ringState.R) + 'px) rotateY(' + rot + 'deg)';
      cards.forEach(function (c, i) {
        var a = ((i * step + rot) % 360 + 360) % 360;
        var f = Math.cos(a * Math.PI / 180);
        c.style.filter = 'brightness(' + (0.55 + 0.45 * Math.max(0, f)).toFixed(3) + ')';
      });
    };
    var tick = function () {
      requestAnimationFrame(tick);
      if (!inView) return;
      if (!drag) {
        if (target !== null) { rot += (target - rot) * 0.12; if (Math.abs(target - rot) < 0.05) { rot = target; target = null; } }
        else { vel *= 0.95; rot += vel + (REDUCE ? 0 : (Math.abs(vel) < 0.05 ? -0.06 : 0)); }
      }
      paint();
    };
    tick();
    stage.addEventListener('pointerdown', function (e) {
      drag = true; moved = 0; startX = lastX = e.clientX; startRot = rot; lastT = performance.now(); vel = 0; target = null;
      stage.classList.add('is-drag');
    });
    addEventListener('pointermove', function (e) {
      if (!drag) return;
      var dx = e.clientX - startX; moved = Math.max(moved, Math.abs(dx));
      rot = startRot + dx * (MOBILE() ? 0.35 : 0.22);
      var now = performance.now(); vel = ((e.clientX - lastX) * (MOBILE() ? 0.35 : 0.22)) / Math.max(1, (now - lastT) / 16); lastX = e.clientX; lastT = now;
    });
    addEventListener('pointerup', function () { if (!drag) return; drag = false; stage.classList.remove('is-drag'); vel = Math.max(-8, Math.min(8, vel)); });
    cards.forEach(function (c) {
      c.addEventListener('click', function (e) { if (moved > 8) { e.preventDefault(); return; } showOffer(c.dataset.offer); });
    });
    d.querySelectorAll('[data-ring]').forEach(function (b) {
      b.addEventListener('click', function () { var k = Math.round(rot / step) - (+b.dataset.ring); target = k * step; vel = 0; });
    });
  }

  /* ---------- offer cards outside the ring ---------- */
  d.querySelectorAll('[data-offer]:not(.ring-card)').forEach(function (b) { b.addEventListener('click', function () { showOffer(b.dataset.offer); }); });

  /* ---------- model codes ---------- */
  d.querySelectorAll('.codes').forEach(function (grid) {
    var wrap = grid.parentNode, sel = wrap.querySelector('#code-sel'), link = wrap.querySelector('#code-wa');
    grid.querySelectorAll('.code').forEach(function (b) {
      b.addEventListener('click', function () {
        grid.querySelectorAll('.code').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
        if (sel) sel.innerHTML = 'Votre choix : <b>Code ' + b.dataset.code + '</b> · ' + b.dataset.price + ' CHF';
        if (link) link.href = waLink('Bonjour Mama Africa, je souhaite réserver le modèle code ' + b.dataset.code + ' (' + b.dataset.price + ' CHF). Quelles sont vos disponibilités ?');
      });
    });
  });

  /* ---------- tabs ---------- */
  d.querySelectorAll('[role="tablist"]').forEach(function (tl) {
    var tabs = tl.querySelectorAll('[role="tab"]');
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () {
        tabs.forEach(function (x) { x.setAttribute('aria-selected', x === t); d.getElementById(x.getAttribute('aria-controls')).hidden = x !== t; });
        if (hasGsap) ScrollTrigger.refresh();
      });
      t.addEventListener('keydown', function (e) {
        var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (k) { var nx = tabs[(i + k + tabs.length) % tabs.length]; nx.focus(); nx.click(); }
      });
    });
  });

  /* ---------- hair colour swatches → 3D braid ---------- */
  var NAMES = {};
  d.querySelectorAll('.sw').forEach(function (b) { NAMES[b.dataset.shade] = { name: b.querySelector('small').textContent, c: b.style.getPropertyValue('--c') }; });
  function markShade(code) {
    d.querySelectorAll('.sw').forEach(function (b) { b.setAttribute('aria-pressed', b.dataset.shade === code); });
    var info = NAMES[code]; if (!info) return;
    d.querySelectorAll('#shade-now').forEach(function (p) { p.style.setProperty('--c', info.c); p.querySelector('span').innerHTML = 'Couleur choisie : <b>' + code + ' · ' + info.name + '</b>'; });
    d.querySelectorAll('.shade-visual').forEach(function (v) { v.style.setProperty('--c', info.c); });
    d.querySelectorAll('#shade-tag').forEach(function (t) { t.textContent = 'Mèches ' + code + ' · ' + info.name + ', en boutique'; });
  }
  d.querySelectorAll('.sw').forEach(function (b) {
    b.addEventListener('click', function () { d.dispatchEvent(new CustomEvent('ma:color', { detail: b.dataset.shade })); markShade(b.dataset.shade); });
  });
  var savedShade = null; try { savedShade = sessionStorage.getItem('ma-color'); } catch (e) {}
  markShade(savedShade && NAMES[savedShade] ? savedShade : '4');

  /* ---------- hours ---------- */
  (function () {
    var now;
    try {
      var parts = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Zurich', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
      var get = function (t) { return (parts.find(function (p) { return p.type === t; }) || {}).value; };
      now = { day: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(get('weekday')), min: (+get('hour') % 24) * 60 + (+get('minute')) };
    } catch (e) { var t = new Date(); now = { day: t.getDay(), min: t.getHours() * 60 + t.getMinutes() }; }
    d.querySelectorAll('.hours li').forEach(function (li) { if (+li.dataset.day === now.day) li.classList.add('is-today'); });
    var open = now.day >= 1 && now.day <= 6 && now.min >= 540 && now.min < 1110;
    d.querySelectorAll('#open-now').forEach(function (b) {
      b.classList.toggle('is-open', open);
      b.querySelector('span').textContent = open ? 'Ouvert maintenant · jusqu’à 18h30' : (now.day === 0 || (now.day === 6 && now.min >= 1110) ? 'Fermé · ouvre lundi à 9h00' : (now.min < 540 ? 'Fermé · ouvre à 9h00' : 'Fermé · ouvre demain à 9h00'));
    });
  })();

  /* ---------- gallery ---------- */
  var mas = d.getElementById('masonry');
  if (mas) {
    var figs = Array.prototype.slice.call(mas.querySelectorAll('figure'));
    d.querySelectorAll('[data-filter]').forEach(function (b) {
      b.addEventListener('click', function () {
        d.querySelectorAll('[data-filter]').forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
        figs.forEach(function (f) { f.classList.toggle('is-hidden', b.dataset.filter !== 'all' && f.dataset.cat !== b.dataset.filter); f.classList.add('is-in'); });
        if (hasGsap) ScrollTrigger.refresh();
      });
    });
    figs.forEach(function (f) {
      f.tabIndex = 0;
      var open = function () {
        var vis = figs.filter(function (x) { return !x.classList.contains('is-hidden'); });
        openLb(vis.map(function (x) { var im = x.querySelector('img'); return { src: im.currentSrc || im.src, cap: im.alt }; }), vis.indexOf(f));
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
      var shade = null; try { shade = sessionStorage.getItem('ma-color'); } catch (er) {}
      window.open(waLink('Bonjour Mama Africa, je souhaite prendre rendez-vous.\n\n' +
        (svc.length ? 'Prestation(s) :\n' + svc.join('\n') + '\n' : '') +
        (code ? 'Modèle : code ' + code.value + '\n' : '') +
        (shade ? 'Couleur de mèches envisagée : ' + shade + '\n' : '') +
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

  /* ---------- pause off-screen videos ---------- */
  if ('IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { var p = e.target.play(); if (p && p.catch) p.catch(function () {}); } else e.target.pause(); });
    }, { rootMargin: '200px' });
    d.querySelectorAll('video').forEach(function (v) { vio.observe(v); });
  }

  (function loop() { heroTick(); requestAnimationFrame(loop); })();
  window.__ma = true;
})();
