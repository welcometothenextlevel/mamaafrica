/* Mama Africa — procedural 3D: braids, gold cuffs, cowrie shells, afro pick.
   Every canvas[data-scene] gets its own small renderer that only runs while on screen. */
import * as THREE from 'three';
import { RoomEnvironment } from './vendor/addons/RoomEnvironment.js';

const MOBILE = matchMedia('(max-width: 760px)').matches;
const REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
const TAU = Math.PI * 2;

const HAIR = {
  espresso: { root: 0x140b07, tip: 0x3a2213, sheen: 0xb98552 },
  ombre:    { root: 0x120a06, tip: 0x9a5a26, sheen: 0xe0a35c },
  bordeaux: { root: 0x1a0a0a, tip: 0x6d1622, sheen: 0xd06a6a },
  miel:     { root: 0x1b100a, tip: 0xb07a3a, sheen: 0xf0c27a },
};

/* ---------- shared textures & materials ---------- */
let hairBump = null;
function getHairBump() {
  if (hairBump) return hairBump;
  const c = document.createElement('canvas');
  c.width = 256; c.height = 512;
  const g = c.getContext('2d');
  g.fillStyle = '#808080'; g.fillRect(0, 0, 256, 512);
  for (let i = 0; i < 1400; i++) {
    const y = Math.random() * 512;
    const a = Math.random();
    g.strokeStyle = a > 0.5 ? `rgba(255,255,255,${0.08 + Math.random() * 0.25})` : `rgba(0,0,0,${0.1 + Math.random() * 0.3})`;
    g.lineWidth = 0.6 + Math.random() * 1.6;
    g.beginPath(); g.moveTo(0, y);
    g.bezierCurveTo(85, y + (Math.random() - 0.5) * 6, 170, y + (Math.random() - 0.5) * 6, 256, y);
    g.stroke();
  }
  hairBump = new THREE.CanvasTexture(c);
  hairBump.wrapS = hairBump.wrapT = THREE.RepeatWrapping;
  hairBump.repeat.set(10, 3);
  return hairBump;
}

function hairMaterial(tone) {
  const h = HAIR[tone] || HAIR.espresso;
  return new THREE.MeshPhysicalMaterial({
    color: 0xffffff, vertexColors: true,
    roughness: 0.42, metalness: 0.0,
    sheen: 1, sheenColor: new THREE.Color(h.sheen), sheenRoughness: 0.35,
    clearcoat: 0.35, clearcoatRoughness: 0.5,
    bumpMap: getHairBump(), bumpScale: 1.6,
  });
}
const gold = () => new THREE.MeshStandardMaterial({ color: 0xd8a24a, metalness: 1, roughness: 0.22 });

/* ---------- geometry builders ---------- */
function frames(spine, n) {
  const f = spine.computeFrenetFrames(n, false);
  return f;
}

// three interlaced strands following a spine curve
function strandPoints(spine, fr, k, { turns, A, B, from = 0, to = 1, n, taper = 0.22 }) {
  const pts = [];
  for (let i = 0; i <= n; i++) {
    const s = from + (to - from) * (i / n);
    const idx = Math.min(fr.normals.length - 1, Math.round(s * (fr.normals.length - 1)));
    const ph = s * turns * TAU + (k * TAU) / 3;
    const sc = 1 - taper * s;
    const p = spine.getPointAt(s);
    // three's frames put the normal along the view axis for planar spines, so the wide sway goes on the binormal
    p.addScaledVector(fr.binormals[idx], Math.sin(ph) * A * sc);
    p.addScaledVector(fr.normals[idx], Math.sin(2 * ph) * B * sc);
    pts.push(p);
  }
  return pts;
}

function colorTube(geo, tone, tubular, radial, sFrom = 0, sTo = 1) {
  const h = HAIR[tone] || HAIR.espresso;
  const a = new THREE.Color(h.root), b = new THREE.Color(h.tip), c = new THREE.Color();
  const n = geo.attributes.position.count;
  const col = new Float32Array(n * 3);
  for (let v = 0; v < n; v++) {
    const i = Math.floor(v / (radial + 1));
    const s = sFrom + (sTo - sFrom) * (i / tubular);
    const t = THREE.MathUtils.smoothstep(s, 0.35, 1.0);
    c.copy(a).lerp(b, t);
    const j = v % (radial + 1);
    const shade = 0.82 + 0.18 * Math.sin((j / radial) * TAU * 2 + i * 0.02);
    col[v * 3] = c.r * shade; col[v * 3 + 1] = c.g * shade; col[v * 3 + 2] = c.b * shade;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
}

function buildBraid(spine, opt) {
  const { tone = 'espresso', turns = 7, A = 0.6, B = 0.36, r = 0.37, radial = MOBILE ? 10 : 16 } = opt;
  const n = Math.round(turns * (MOBILE ? 34 : 52));
  const fr = frames(spine, 400);
  const group = new THREE.Group();
  const mat = hairMaterial(tone);
  const meshes = [];
  for (let k = 0; k < 3; k++) {
    const pts = strandPoints(spine, fr, k, { turns, A, B, n, taper: opt.taper ?? 0.22 });
    const curve = new THREE.CatmullRomCurve3(pts);
    const geo = new THREE.TubeGeometry(curve, n, r, radial, false);
    colorTube(geo, tone, n, radial);
    const m = new THREE.Mesh(geo, mat);
    m.userData = { n, radial };
    group.add(m); meshes.push(m);
  }
  group.userData = { meshes, fr, spine, mat, opt: { turns, A, B, r, radial, tone } };
  return group;
}

function cuffGeometry(R = 1.05, h = 0.46, ridges = 5) {
  const pts = [];
  const N = 60;
  for (let i = 0; i <= N; i++) {
    const t = i / N;
    const y = -h / 2 + h * t;
    const ridge = Math.pow(Math.abs(Math.sin(t * Math.PI * ridges)), 0.6) * 0.06;
    const edge = Math.sin(t * Math.PI) * 0.05;
    pts.push(new THREE.Vector2(R + ridge + edge, y));
  }
  for (let i = N; i >= 0; i--) pts.push(new THREE.Vector2(R - 0.035, -h / 2 + h * (i / N)));
  return new THREE.LatheGeometry(pts, MOBILE ? 36 : 64);
}

function placeOnSpine(obj, spine, s) {
  obj.position.copy(spine.getPointAt(s));
  const tan = spine.getTangentAt(s);
  obj.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), tan);
}

let _cowrie = null;
function cowrieGeometry() {
  if (_cowrie) return _cowrie;
  const g = new THREE.SphereGeometry(1, MOBILE ? 36 : 64, MOBILE ? 24 : 40);
  const p = g.attributes.position;
  const col = new Float32Array(p.count * 3);
  const ivory = new THREE.Color(0xf2e7d2), cream = new THREE.Color(0xd9c3a0), dark = new THREE.Color(0x3a2416), c = new THREE.Color();
  for (let i = 0; i < p.count; i++) {
    let x = p.getX(i), y = p.getY(i), z = p.getZ(i);
    const pinch = 1 - 0.28 * Math.pow(Math.abs(x), 3);
    y *= 0.64 * pinch; z *= 0.52 * pinch;
    if (z < 0) z *= 0.38;
    const d = Math.abs(y) / 0.64;
    let groove = 0;
    if (z <= 0 && d < 0.2) {
      groove = 1 - d / 0.2;
      z += 0.07 * groove;
      y *= 1 - 0.25 * groove;
    }
    // slight dorsal hump
    if (z > 0) z *= 1 + 0.12 * (1 - Math.abs(x));
    p.setXYZ(i, x, y, z);
    c.copy(ivory).lerp(cream, THREE.MathUtils.clamp(0.5 - z * 0.9 + Math.abs(x) * 0.25, 0, 1));
    if (z <= 0.02 && d < 0.16) {
      const teeth = Math.cos(x * 34) > 0.15 && d > 0.05;
      if (!teeth) c.copy(dark);
    }
    col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b;
  }
  g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  g.computeVertexNormals();
  _cowrie = g;
  return g;
}
const cowrieMat = () => new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.28, clearcoat: 0.8, clearcoatRoughness: 0.2, sheen: 0.4, sheenColor: new THREE.Color(0xffe2b5) });

function afroPick() {
  const grp = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({ color: 0xd8a24a, metalness: 1, roughness: 0.2 });
  const lacquer = new THREE.MeshPhysicalMaterial({ color: 0x1a110b, roughness: 0.18, clearcoat: 1, clearcoatRoughness: 0.08 });
  // handle with a round window
  const s = new THREE.Shape();
  const w = 0.95, top = 2.0, bot = 0.0, rr = 0.42;
  s.moveTo(-w, bot);
  s.lineTo(w, bot);
  s.lineTo(w, top - rr);
  s.quadraticCurveTo(w, top, w - rr, top);
  s.lineTo(-w + rr, top);
  s.quadraticCurveTo(-w, top, -w, top - rr);
  s.lineTo(-w, bot);
  const hole = new THREE.Path();
  hole.absarc(0, 1.15, 0.42, 0, TAU, true);
  s.holes.push(hole);
  const hg = new THREE.ExtrudeGeometry(s, { depth: 0.22, bevelEnabled: true, bevelThickness: 0.08, bevelSize: 0.07, bevelSegments: 4, curveSegments: 40 });
  hg.translate(0, 0, -0.11);
  grp.add(new THREE.Mesh(hg, lacquer));
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.42, 0.06, 16, 64), mat);
  ring.position.set(0, 1.15, 0);
  grp.add(ring);
  const band = new THREE.Mesh(new THREE.BoxGeometry(2.06, 0.16, 0.42), mat);
  band.position.set(0, 0.08, 0);
  grp.add(band);
  const teeth = 7;
  for (let i = 0; i < teeth; i++) {
    const x = -0.82 + (1.64 * i) / (teeth - 1);
    const tg = new THREE.CylinderGeometry(0.075, 0.03, 3.1, 14);
    const t = new THREE.Mesh(tg, mat);
    t.position.set(x, -1.55, 0);
    grp.add(t);
  }
  grp.position.y = 0.4;
  return grp;
}

/* ---------- scene factory ---------- */
function makeRenderer(canvas) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: !MOBILE, alpha: true, powerPreference: 'high-performance' });
  r.setPixelRatio(Math.min(devicePixelRatio, MOBILE ? 1.5 : 1.75));
  r.toneMapping = THREE.ACESFilmicToneMapping;
  r.toneMappingExposure = 1.08;
  r.outputColorSpace = THREE.SRGBColorSpace;
  return r;
}

function lights(scene, renderer) {
  const pm = new THREE.PMREMGenerator(renderer);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.55;
  const key = new THREE.DirectionalLight(0xffdcb0, 2.4); key.position.set(-5, 7, 8); scene.add(key);
  const rim = new THREE.DirectionalLight(0xe0782e, 3.2); rim.position.set(6, 2, -6); scene.add(rim);
  const fill = new THREE.DirectionalLight(0xfff3e4, 0.6); fill.position.set(2, -4, 6); scene.add(fill);
  scene.add(new THREE.AmbientLight(0xfff0e0, 0.25));
}

function scatterCowries(group, count, spread, rand) {
  const geo = cowrieGeometry(), mat = cowrieMat();
  const items = [];
  for (let i = 0; i < count; i++) {
    const m = new THREE.Mesh(geo, mat);
    const s = 0.32 + rand() * 0.28;
    m.scale.setScalar(s);
    m.position.set((rand() - 0.5) * spread.x, (rand() - 0.5) * spread.y, (rand() - 0.5) * spread.z);
    m.rotation.set(rand() * TAU, rand() * TAU, rand() * TAU);
    m.userData = { base: m.position.clone(), sp: 0.3 + rand() * 0.6, ph: rand() * TAU, rot: (rand() - 0.5) * 0.6 };
    group.add(m); items.push(m);
  }
  return items;
}

function scatterBeads(group, count, spread, rand) {
  const mat = gold();
  const items = [];
  for (let i = 0; i < count; i++) {
    const m = new THREE.Mesh(cuffGeometry(0.22, 0.26, 3), mat);
    m.position.set((rand() - 0.5) * spread.x, (rand() - 0.5) * spread.y, (rand() - 0.5) * spread.z);
    m.rotation.set(rand() * TAU, rand() * TAU, 0);
    m.userData = { base: m.position.clone(), sp: 0.2 + rand() * 0.5, ph: rand() * TAU, rot: (rand() - 0.5) * 0.8 };
    group.add(m); items.push(m);
  }
  return items;
}

function seeded(seed) {
  let s = seed >>> 0;
  return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296);
}

const BUILDERS = {
  hero(ctx) {
    const { scene, aspect, tone } = ctx;
    const wide = aspect > 1.1 && ctx.variant !== 'arch';
    // traces the arch photo like a crown: in from the top-right, over its curve, down its left edge
    const spine = new THREE.CatmullRomCurve3(wide ? [
      new THREE.Vector3(8.6, 3.7, -1), new THREE.Vector3(5.9, 2.25, 0.6), new THREE.Vector3(3.05, 2.85, 1.0),
      new THREE.Vector3(1.0, 1.8, 1.1), new THREE.Vector3(0.15, -0.6, 1.1), new THREE.Vector3(0.25, -3.0, 0.9),
      new THREE.Vector3(0.9, -5.3, 0.4), new THREE.Vector3(2, -7.6, -1),
    ] : [
      // mobile: the canvas wraps the arch itself, so trace its crown and left edge
      new THREE.Vector3(5.4, 6.8, -1), new THREE.Vector3(3.0, 4.1, 0.6), new THREE.Vector3(0, 5.35, 1.0),
      new THREE.Vector3(-2.95, 4.05, 1.1), new THREE.Vector3(-3.95, 1.0, 1.1), new THREE.Vector3(-3.9, -2.6, 0.9),
      new THREE.Vector3(-2.9, -5.6, 0.4), new THREE.Vector3(-1.4, -8.5, -1),
    ]);
    const root = new THREE.Group();
    const braid = buildBraid(spine, { tone, turns: wide ? 14 : 13, A: wide ? 0.36 : 0.3, B: wide ? 0.22 : 0.19, r: wide ? 0.235 : 0.2, taper: 0.12 });
    root.add(braid);
    const cm = gold();
    [0.12, 0.36, 0.64, 0.9].forEach((s, i) => {
      const c = new THREE.Mesh(cuffGeometry(0.62 - s * 0.05, i % 2 ? 0.34 : 0.5, i % 2 ? 3 : 5), cm);
      placeOnSpine(c, spine, s); root.add(c);
    });
    scene.add(root);
    const rand = seeded(7);
    const deco = new THREE.Group();
    const cow = scatterCowries(deco, MOBILE ? 3 : 7, new THREE.Vector3(wide ? 7.5 : 9, 9, 4), rand);
    const beads = scatterBeads(deco, MOBILE ? 2 : 5, new THREE.Vector3(wide ? 7.5 : 9, 9, 4), rand);
    if (!wide) {
      const spots = [[3.9, -1.5, 1.2], [3.6, 2.6, 0.6], [-1.6, -6.0, 1.4], [4.0, -5.2, 1], [-3.6, 6.3, 0]];
      [...cow, ...beads].forEach((m, i) => { const q = spots[i % spots.length]; m.position.set(q[0], q[1], q[2]); m.userData.base.copy(m.position); m.scale.multiplyScalar(0.8); });
    }
    if (wide) {
      // keep the shells around the photo's edges, never over the face
      const spots = [[6.5, -1.6, 1], [6.1, 1.2, -0.4], [1.9, -3.7, 1.6], [-1.1, -4.2, 1], [7.6, -3.9, 0.2], [4.8, -4.3, 1.8], [0.6, 3.4, -0.6], [6.9, 3.3, -1], [8, 0.2, 0], [3.4, -5.6, 1]];
      [...cow, ...beads].forEach((m, i) => { const q = spots[i % spots.length]; m.position.set(q[0], q[1], q[2]); m.userData.base.copy(m.position); });
    }
    scene.add(deco);
    ctx.camera.position.set(0, 0, 16);
    return (t, p, mouse) => {
      root.rotation.y = Math.sin(t * 0.25) * 0.18 + mouse.x * 0.25 + p * 0.9;
      root.rotation.x = mouse.y * 0.12 + p * 0.25;
      root.position.y = p * 3.2;
      deco.rotation.y = t * 0.03 + mouse.x * 0.15;
      deco.position.y = p * 5;
      for (const m of [...cow, ...beads]) {
        const u = m.userData;
        m.position.y = u.base.y + Math.sin(t * u.sp + u.ph) * 0.35;
        m.rotation.x += u.rot * 0.01; m.rotation.y += u.rot * 0.013;
      }
    };
  },

  weave(ctx) {
    const { scene, tone } = ctx;
    const spine = new THREE.CatmullRomCurve3([new THREE.Vector3(0, 5.2, 0), new THREE.Vector3(0.15, 2, 0), new THREE.Vector3(-0.1, -1, 0), new THREE.Vector3(0, -3.6, 0)]);
    const root = new THREE.Group();
    const braid = buildBraid(spine, { tone, turns: 6, A: 0.62, B: 0.38, r: 0.38, taper: 0.12 });
    root.add(braid);
    const top = new THREE.Mesh(cuffGeometry(1.08, 0.6, 5), gold());
    placeOnSpine(top, spine, 0.015); root.add(top);
    const tie = new THREE.Mesh(cuffGeometry(0.95, 0.36, 3), gold());
    root.add(tie);
    const looseMat = braid.userData.mat;
    let loose = [];
    const { fr, opt } = braid.userData;
    let last = -1;
    function rebuild(p) {
      loose.forEach((m) => { root.remove(m); m.geometry.dispose(); });
      loose = [];
      const s = Math.max(0.03, p);
      const end = spine.getPointAt(Math.min(1, s));
      for (let k = 0; k < 3; k++) {
        const pts0 = strandPoints(spine, fr, k, { turns: opt.turns, A: opt.A, B: opt.B, from: s, to: s, n: 1, taper: 0.12 });
        const a = pts0[0];
        const spread = (k - 1) * 1.5;
        const bottom = -6.4;
        const len = Math.max(0.5, a.y - bottom);
        const curve = new THREE.CatmullRomCurve3([
          a,
          new THREE.Vector3(a.x + spread * 0.35, a.y - len * 0.3, a.z + 0.3 * (k - 1)),
          new THREE.Vector3(a.x + spread * 0.8, a.y - len * 0.65, a.z),
          new THREE.Vector3(spread * 1.2 + Math.sin(k) * 0.3, bottom, 0),
        ]);
        const n = 40;
        const g = new THREE.TubeGeometry(curve, n, opt.r * 0.95, opt.radial, false);
        colorTube(g, tone, n, opt.radial, s, 1);
        const m = new THREE.Mesh(g, looseMat);
        root.add(m); loose.push(m);
      }
      tie.visible = p > 0.03 && p < 0.985;
      placeOnSpine(tie, spine, Math.min(0.999, s));
      for (const m of braid.userData.meshes) {
        const { n, radial } = m.userData;
        m.geometry.setDrawRange(0, Math.floor(s * n) * radial * 6);
      }
      void end;
    }
    scene.add(root);
    ctx.camera.position.set(0, 0, 17);
    return (t, p, mouse) => {
      const q = THREE.MathUtils.clamp((p - 0.12) / 0.76, 0, 1);
      if (Math.abs(q - last) > 0.003) { rebuild(q); last = q; }
      root.rotation.y = q * TAU * 0.5 + Math.sin(t * 0.4) * 0.1 + mouse.x * 0.3;
      root.rotation.x = mouse.y * 0.1;
    };
  },

  cowries(ctx) {
    const { scene, aspect } = ctx;
    const rand = seeded(21);
    const deco = new THREE.Group();
    const wide = aspect > 1.1;
    const edge = ctx.variant === 'edge'; // a photo sits in the right column: no centrepiece shell
    const cow = scatterCowries(deco, MOBILE ? 6 : (edge ? 9 : 11), new THREE.Vector3(wide ? 8.5 : 7, 9, 5), rand);
    const beads = scatterBeads(deco, MOBILE ? 3 : 6, new THREE.Vector3(wide ? 8.5 : 7, 9, 5), rand);
    if (wide) deco.position.x = 3.6; // keep clear of the headline column
    const big = new THREE.Mesh(cowrieGeometry(), cowrieMat());
    big.scale.setScalar(MOBILE ? 1.5 : 1.9);
    big.position.set(wide ? 0.4 : 0, wide ? 0 : -1.5, 2);
    big.visible = !edge && !(MOBILE && !wide);
    deco.add(big);
    scene.add(deco);
    ctx.camera.position.set(0, 0, 16);
    return (t, p, mouse) => {
      deco.rotation.y = mouse.x * 0.2 + p * 0.6;
      deco.position.y = p * 3;
      big.rotation.set(Math.PI * 0.72 + Math.sin(t * 0.5) * 0.3 + mouse.y * 0.4, Math.sin(t * 0.3) * 0.6 + mouse.x * 0.8, 0.5 + t * 0.12);
      for (const m of [...cow, ...beads]) {
        const u = m.userData;
        m.position.y = u.base.y + Math.sin(t * u.sp + u.ph) * 0.4;
        m.rotation.x += u.rot * 0.01; m.rotation.z += u.rot * 0.012;
      }
    };
  },

  pick(ctx) {
    const { scene, aspect } = ctx;
    const pick = afroPick();
    const holder = new THREE.Group();
    holder.add(pick);
    holder.scale.setScalar(MOBILE ? 1.15 : 1.35);
    holder.position.set(aspect > 1.1 ? 3.8 : 0, aspect > 1.1 ? 0 : -1, 0);
    holder.rotation.z = -0.35;
    scene.add(holder);
    const rand = seeded(5);
    const deco = new THREE.Group();
    const cow = scatterCowries(deco, MOBILE ? 5 : 9, new THREE.Vector3(aspect > 1.1 ? 8 : 7, 9, 4), rand);
    if (aspect > 1.1) deco.position.x = 3.8;
    scene.add(deco);
    ctx.camera.position.set(0, 0, 16);
    return (t, p, mouse) => {
      pick.rotation.y = t * 0.45 + mouse.x * 0.8;
      pick.rotation.x = Math.sin(t * 0.6) * 0.12 + mouse.y * 0.3;
      holder.position.y = (aspect > 1.1 ? 0 : -1) + Math.sin(t * 0.8) * 0.25 + p * 2.5;
      deco.position.y = p * 4;
      for (const m of cow) {
        const u = m.userData;
        m.position.y = u.base.y + Math.sin(t * u.sp + u.ph) * 0.4;
        m.rotation.x += u.rot * 0.01; m.rotation.y += u.rot * 0.012;
      }
    };
  },
};

/* ---------- runtime ---------- */
const mouse = { x: 0, y: 0, tx: 0, ty: 0 };
addEventListener('pointermove', (e) => {
  mouse.tx = (e.clientX / innerWidth) * 2 - 1;
  mouse.ty = (e.clientY / innerHeight) * 2 - 1;
}, { passive: true });

// scene hosts sit at the top of their page: 0 at rest, 1 once scrolled past
function progressOf(el) {
  const r = el.getBoundingClientRect();
  return THREE.MathUtils.clamp(-r.top / Math.max(1, r.height), 0, 1);
}
// for tall sticky sections: 0 when the section top hits the viewport top, 1 when its bottom reaches the viewport bottom
function stickyProgress(el) {
  const r = el.getBoundingClientRect();
  const span = r.height - innerHeight;
  if (span <= 0) return progressOf(el);
  return THREE.MathUtils.clamp(-r.top / span, 0, 1);
}

function mount(canvas) {
  const kind = canvas.dataset.scene;
  if (!BUILDERS[kind]) return;
  if (canvas.offsetParent === null && getComputedStyle(canvas.parentElement).display === 'none') return; // hidden variant for this screen size
  const host = canvas.closest('[data-scene-host]') || canvas.parentElement;
  const track = canvas.closest('[data-scene-track]');
  let renderer;
  try { renderer = makeRenderer(canvas); } catch (e) { canvas.remove(); return; }
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
  lights(scene, renderer);
  let w = host.clientWidth || 1, h = host.clientHeight || 1;
  const ctx = { scene, camera, aspect: w / h, tone: canvas.dataset.tone || 'espresso', variant: canvas.dataset.variant || '' };
  const update = BUILDERS[kind](ctx);
  const resize = () => {
    w = host.clientWidth || 1; h = host.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    // keep the composition: widen the view on narrow screens
    camera.fov = w / h < 0.8 || ctx.variant === 'arch' ? 44 : 30;
    camera.updateProjectionMatrix();
  };
  resize();
  new ResizeObserver(resize).observe(host);
  let visible = true;
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; }, { rootMargin: '120px' }).observe(host);
  const clock = new THREE.Clock();
  let shown = false;
  const frame = () => {
    requestAnimationFrame(frame);
    if (!visible && shown) return;
    const t = REDUCE ? 2 : clock.getElapsedTime();
    mouse.x += (mouse.tx - mouse.x) * 0.05;
    mouse.y += (mouse.ty - mouse.y) * 0.05;
    const p = track ? stickyProgress(track) : progressOf(host);
    update(t, p, REDUCE ? { x: 0, y: 0 } : mouse);
    renderer.render(scene, camera);
    if (!shown) { shown = true; canvas.classList.add('is-live'); }
  };
  frame();
}

document.querySelectorAll('canvas[data-scene]').forEach(mount);
