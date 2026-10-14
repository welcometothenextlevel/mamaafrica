/* Mama Africa — procedural 3D.
   1. The companion: one braid that hangs along the right edge for the whole visit. It weaves itself in
      on load, sits wider beside the hero, slims into a rail in the margin as you scroll, slides with the
      page and swings with scroll speed. Fixed canvas, so it is never cut by a section edge.
   2. canvas[data-scene="weave"]: the home page braiding story (inside a sticky, full-viewport stage). */
import * as THREE from 'three';
import { RoomEnvironment } from './vendor/addons/RoomEnvironment.js';

const MOBILE = matchMedia('(max-width: 760px)').matches;
const REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
const TAU = Math.PI * 2;

const HAIR = {
  espresso: { root: 0x150b06, tip: 0x4a2a15, sheen: 0xb98552 },
};

/* ---------- shared textures & materials ---------- */
let hairBump = null;
function getHairBump() {
  if (hairBump) return hairBump;
  const c = document.createElement('canvas');
  c.width = 128; c.height = 1024;
  const g = c.getContext('2d');
  g.fillStyle = '#808080'; g.fillRect(0, 0, c.width, c.height);
  // fine fibres running along the strand (u = along the tube, v = around it)
  for (let i = 0; i < 2600; i++) {
    const y = Math.random() * c.height;
    g.strokeStyle = Math.random() > 0.5 ? `rgba(255,255,255,${0.06 + Math.random() * 0.22})` : `rgba(0,0,0,${0.08 + Math.random() * 0.26})`;
    g.lineWidth = 0.5 + Math.random() * 1.1;
    g.beginPath(); g.moveTo(0, y);
    g.bezierCurveTo(40, y + (Math.random() - 0.5) * 3, 90, y + (Math.random() - 0.5) * 3, c.width, y);
    g.stroke();
  }
  hairBump = new THREE.CanvasTexture(c);
  hairBump.wrapS = hairBump.wrapT = THREE.RepeatWrapping;
  hairBump.anisotropy = 4;
  return hairBump;
}

function hairMaterial(repeatU = 12) {
  const h = HAIR.espresso;
  const bump = getHairBump().clone();
  bump.needsUpdate = true;
  bump.repeat.set(repeatU, 2);
  return new THREE.MeshPhysicalMaterial({
    color: 0xffffff, vertexColors: true,
    roughness: 0.42, metalness: 0,
    sheen: 1, sheenColor: new THREE.Color(h.sheen), sheenRoughness: 0.35,
    clearcoat: 0.3, clearcoatRoughness: 0.5,
    bumpMap: bump, bumpScale: 1.5,
  });
}
const gold = () => new THREE.MeshStandardMaterial({ color: 0xd9a54c, metalness: 1, roughness: 0.2 });

function shadeTube(geo, radial, seed = 0) {
  const h = HAIR.espresso;
  const a = new THREE.Color(h.root), b = new THREE.Color(h.tip), c = new THREE.Color();
  const n = geo.attributes.position.count;
  const col = new Float32Array(n * 3);
  for (let v = 0; v < n; v++) {
    const i = Math.floor(v / (radial + 1)), j = v % (radial + 1);
    // periodic warmth so repeated sections stay seamless
    c.copy(a).lerp(b, 0.45 + 0.25 * Math.sin(i * 0.05 + seed));
    const shade = 0.8 + 0.2 * Math.sin((j / radial) * TAU * 3 + seed);
    col[v * 3] = c.r * shade; col[v * 3 + 1] = c.g * shade; col[v * 3 + 2] = c.b * shade;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
}

function cuffGeometry(R = 1.05, h = 0.46, ridges = 5) {
  const pts = [];
  const N = 60;
  for (let i = 0; i <= N; i++) {
    const t = i / N;
    const y = -h / 2 + h * t;
    const ridge = Math.pow(Math.abs(Math.sin(t * Math.PI * ridges)), 0.6) * 0.055;
    const edge = Math.sin(t * Math.PI) * 0.05;
    pts.push(new THREE.Vector2(R + ridge + edge, y));
  }
  for (let i = N; i >= 0; i--) pts.push(new THREE.Vector2(R - 0.035, -h / 2 + h * (i / N)));
  return new THREE.LatheGeometry(pts, 72);
}

let _cowrie = null;
function cowrieGeometry() {
  if (_cowrie) return _cowrie;
  const g = new THREE.SphereGeometry(1, 64, 40);
  const p = g.attributes.position;
  const col = new Float32Array(p.count * 3);
  const ivory = new THREE.Color(0xf2e7d2), cream = new THREE.Color(0xd9c3a0), dark = new THREE.Color(0x3a2416), c = new THREE.Color();
  for (let i = 0; i < p.count; i++) {
    let x = p.getX(i), y = p.getY(i), z = p.getZ(i);
    const pinch = 1 - 0.28 * Math.pow(Math.abs(x), 3);
    y *= 0.64 * pinch; z *= 0.52 * pinch;
    if (z < 0) z *= 0.38;
    const d = Math.abs(y) / 0.64;
    if (z <= 0 && d < 0.2) { const groove = 1 - d / 0.2; z += 0.07 * groove; y *= 1 - 0.25 * groove; }
    if (z > 0) z *= 1 + 0.12 * (1 - Math.abs(x));
    p.setXYZ(i, x, y, z);
    c.copy(ivory).lerp(cream, THREE.MathUtils.clamp(0.5 - z * 0.9 + Math.abs(x) * 0.25, 0, 1));
    if (z <= 0.02 && d < 0.16 && !(Math.cos(x * 34) > 0.15 && d > 0.05)) c.copy(dark);
    col[i * 3] = c.r; col[i * 3 + 1] = c.g; col[i * 3 + 2] = c.b;
  }
  g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  g.computeVertexNormals();
  _cowrie = g;
  return g;
}
const cowrieMat = () => new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.28, clearcoat: 0.8, clearcoatRoughness: 0.2, sheen: 0.4, sheenColor: new THREE.Color(0xffe2b5) });

function lights(scene, renderer) {
  const pm = new THREE.PMREMGenerator(renderer);
  scene.environment = pm.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.6;
  const key = new THREE.DirectionalLight(0xffdcb0, 2.6); key.position.set(-5, 7, 8); scene.add(key);
  const rim = new THREE.DirectionalLight(0xe0782e, 3.0); rim.position.set(6, 2, -6); scene.add(rim);
  const fill = new THREE.DirectionalLight(0xfff3e4, 0.7); fill.position.set(2, -4, 6); scene.add(fill);
  scene.add(new THREE.AmbientLight(0xfff0e0, 0.25));
}

function makeRenderer(canvas, dprCap) {
  const r = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  r.setPixelRatio(Math.min(devicePixelRatio, dprCap));
  r.toneMapping = THREE.ACESFilmicToneMapping;
  r.toneMappingExposure = 1.1;
  r.outputColorSpace = THREE.SRGBColorSpace;
  return r;
}

/* ---------- a straight plait, analytic so it can repeat seamlessly ---------- */
class PlaitCurve extends THREE.Curve {
  constructor(k, len, { A, B, P }) { super(); Object.assign(this, { k, len, A, B, P }); }
  getPoint(t, target = new THREE.Vector3()) {
    const y = t * this.len;
    const ph = (y / this.P) * TAU + (this.k * TAU) / 3;
    return target.set(this.A * Math.sin(ph), -y, this.B * Math.sin(2 * ph));
  }
}

// hair "swing": bends everything sideways in view space, more towards the bottom of the screen
const bendU = { uBend: { value: 0 }, uTop: { value: 5 }, uSpan: { value: 10 } };
function withBend(mat) {
  mat.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, bendU);
    sh.vertexShader = 'uniform float uBend;\nuniform float uTop;\nuniform float uSpan;\n' + sh.vertexShader.replace('#include <project_vertex>', `
      vec4 mvPosition = vec4( transformed, 1.0 );
      mvPosition = modelViewMatrix * mvPosition;
      float bt = clamp( ( uTop - mvPosition.y ) / uSpan, 0.0, 1.0 );
      mvPosition.x += uBend * bt * bt;
      gl_Position = projectionMatrix * mvPosition;`);
  };
  return mat;
}

/* ================================================================ companion */
function mountCompanion() {
  const canvas = document.createElement('canvas');
  canvas.className = 'companion';
  canvas.setAttribute('aria-hidden', 'true');
  document.body.appendChild(canvas);
  let renderer;
  try { renderer = makeRenderer(canvas, 2); } catch (e) { canvas.remove(); return; }
  const scene = new THREE.Scene();
  lights(scene, renderer);
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
  camera.position.set(0, 0, 20);

  // plait in local units: width = 2 (A + R); a gold cuff every UNIT, a cowrie every second UNIT
  const G = { A: 0.58, B: 0.35, P: 2.5 }; // period ≈ 1.3× the width: lobes sit at ~45°, like a real plait
  const R = 0.37, WIDTH = 2 * (G.A + R), UNIT = G.P * (MOBILE ? 4 : 3), REPEAT = UNIT * 2;
  const holder = new THREE.Group(), spin = new THREE.Group();
  holder.add(spin); scene.add(holder);
  const hairMat = withBend(hairMaterial());
  const goldMat = withBend(gold());
  const cowMat = withBend(cowrieMat());
  const cuffGeo = cuffGeometry(1.02, 0.6, 5), cuffGeoS = cuffGeometry(1.0, 0.36, 3);
  let strands = [], deco = [], L = 0, segs = 0;
  const radial = MOBILE ? 14 : 18;

  function build(len) {
    strands.forEach((m) => { spin.remove(m); m.geometry.dispose(); });
    deco.forEach((m) => spin.remove(m));
    strands = []; deco = [];
    L = len;
    segs = Math.round((len / G.P) * 44);
    hairMat.bumpMap.repeat.set(len / G.P * 1.2, 2);
    for (let k = 0; k < 3; k++) {
      const geo = new THREE.TubeGeometry(new PlaitCurve(k, len, G), segs, R, radial, false);
      shadeTube(geo, radial, k * 2.1);
      const m = new THREE.Mesh(geo, hairMat);
      spin.add(m); strands.push(m);
    }
    for (let y = UNIT * 0.5, i = 0; y < len; y += UNIT, i++) {
      const c = new THREE.Mesh(i % 2 ? cuffGeoS : cuffGeo, goldMat);
      c.position.y = -y; c.userData.y = y;
      spin.add(c); deco.push(c);
      if (i % 2 === 1) {
        const s = new THREE.Mesh(cowrieGeometry(), cowMat);
        s.scale.setScalar(0.44);
        s.rotation.set(0, Math.PI, Math.PI / 2);
        s.position.set(0, -(y + UNIT * 0.5), 0.86);
        s.userData.y = y + UNIT * 0.5;
        spin.add(s); deco.push(s);
      }
    }
  }

  const st = { cw: 0, vh: 0, worldH: 0, upp: 0, heroW: 0, heroCx: 0, railW: 0, railCx: 0, minScale: 1 };
  function layout() {
    const vw = innerWidth, vh = innerHeight;
    const wrap = document.querySelector('main .wrap') || document.querySelector('.wrap');
    let contentRight = vw - 40;
    if (wrap) { const r = wrap.getBoundingClientRect(); contentRight = r.right - parseFloat(getComputedStyle(wrap).paddingRight); }
    const free = Math.max(0, vw - contentRight);
    if (MOBILE) {
      st.railW = 22; st.railCx = vw - 17;
      st.heroW = 46; st.heroCx = vw - 29;
    } else {
      st.railW = THREE.MathUtils.clamp(free - 18, 20, 64);
      st.railCx = Math.min(contentRight + free / 2, vw - st.railW / 2 - 8);
      st.heroW = THREE.MathUtils.clamp(vw * 0.095, Math.max(st.railW, 90), 168);
      st.heroCx = vw - st.heroW * 0.6;
    }
    st.cw = Math.min(vw, Math.round(Math.max(st.heroW + 190, vw - st.railCx + st.railW / 2 + 160)));
    st.vh = vh;
    renderer.setSize(st.cw, vh, false);
    canvas.style.width = st.cw + 'px';
    canvas.style.height = vh + 'px';
    camera.aspect = st.cw / vh;
    camera.updateProjectionMatrix();
    st.worldH = 2 * camera.position.z * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    st.upp = st.worldH / vh;
    st.minScale = (Math.min(st.railW, st.heroW) * st.upp) / WIDTH;
    bendU.uTop.value = st.worldH / 2;
    bendU.uSpan.value = st.worldH;
    const need = st.worldH / st.minScale + REPEAT * 1.5;
    const len = Math.ceil(need / REPEAT) * REPEAT;
    if (len !== L) build(len);
  }
  layout();
  addEventListener('resize', layout);

  // intro: the plait weaves itself down the edge (full on the first page of a visit, quick afterwards)
  let seen = false;
  try { seen = sessionStorage.getItem('ma-braid') === '1'; sessionStorage.setItem('ma-braid', '1'); } catch (e) {}
  const introDur = REDUCE ? 0 : (seen ? 0.7 : 2.2);
  const clock = new THREE.Clock();
  let lastY = scrollY, vel = 0, bend = 0, bendV = 0, spinOff = 0, rot = 0, opacity = 0;
  const weave = document.querySelector('.weave');
  const ease = (x) => 1 - Math.pow(1 - x, 3);
  const smooth = (x) => x * x * (3 - 2 * x);

  function frame() {
    requestAnimationFrame(frame);
    const t = clock.getElapsedTime();
    const y = scrollY;
    const dy = y - lastY; lastY = y;
    vel += (dy - vel) * 0.2;

    // hero → rail
    const hp = smooth(THREE.MathUtils.clamp(y / (st.vh * 0.85), 0, 1));
    const W = THREE.MathUtils.lerp(st.heroW, st.railW, hp);
    const cx = THREE.MathUtils.lerp(st.heroCx, st.railCx, hp) - (innerWidth - st.cw);
    const s = (W * st.upp) / WIDTH;
    holder.scale.setScalar(s);
    holder.position.x = (cx - st.cw / 2) * st.upp;

    // slides with the page (slower than the content), wrapping on the repeat unit
    const off = ((y * 0.42 * st.upp) / s) % REPEAT;
    const topLocal = UNIT * 0.5 + off;
    holder.position.y = st.worldH / 2 + topLocal * s;

    // weave itself in
    const ip = introDur ? ease(THREE.MathUtils.clamp((t - 0.25) / introDur, 0, 1)) : 1;
    const drawnTo = topLocal + ip * (st.worldH / s + UNIT);
    const cut = Math.min(segs, Math.ceil((drawnTo / L) * segs));
    for (const m of strands) m.geometry.setDrawRange(0, cut * radial * 6);
    for (const d of deco) {
      const on = d.userData.y < drawnTo - 0.3;
      d.visible = on;
    }

    // spin with time and scroll speed, swing like hair
    if (!REDUCE) {
      // sway around the front view (a plait seen side-on reads as a rope), nudged by scroll speed
      spinOff = THREE.MathUtils.clamp((spinOff + vel * 0.0022) * 0.965, -1.1, 1.1);
      rot = Math.sin(t * 0.35) * 0.38 + spinOff;
      const target = THREE.MathUtils.clamp(-vel * 0.045, -1.6, 1.6) + Math.sin(t * 0.7) * 0.06;
      bendV += (target - bend) * 0.06; bendV *= 0.88; bend += bendV;
    }
    spin.rotation.y = rot;
    bendU.uBend.value = bend * (s / ((st.heroW * st.upp) / WIDTH));

    // step aside for the big braid of the home story, and when menus are open
    let target = 1;
    if (weave) { const r = weave.getBoundingClientRect(); if (r.top < st.vh * 0.75 && r.bottom > st.vh * 0.25) target = 0; }
    if (document.body.classList.contains('menu-open')) target = 0;
    opacity += (target - opacity) * 0.08;
    canvas.style.opacity = opacity.toFixed(3);
    if (opacity > 0.01) renderer.render(scene, camera);
  }
  frame();
}

/* ================================================================ weave (home story) */
function strandPoints(spine, fr, k, { turns, A, B, from = 0, to = 1, n, taper = 0.12 }) {
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

function mountWeave(canvas) {
  const host = canvas.closest('[data-scene-host]') || canvas.parentElement;
  const track = canvas.closest('[data-scene-track]');
  let renderer;
  try { renderer = makeRenderer(canvas, MOBILE ? 1.75 : 1.75); } catch (e) { canvas.remove(); return; }
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
  camera.position.set(0, 0, 17);
  lights(scene, renderer);
  const spine = new THREE.CatmullRomCurve3([new THREE.Vector3(0, 5.2, 0), new THREE.Vector3(0.15, 2, 0), new THREE.Vector3(-0.1, -1, 0), new THREE.Vector3(0, -3.6, 0)]);
  const fr = spine.computeFrenetFrames(400, false);
  const opt = { turns: 6, A: 0.62, B: 0.38, r: 0.38, radial: MOBILE ? 14 : 18 };
  const n = Math.round(opt.turns * 52);
  const mat = hairMaterial(n / 14);
  const root = new THREE.Group();
  const meshes = [];
  for (let k = 0; k < 3; k++) {
    const geo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(strandPoints(spine, fr, k, { ...opt, n })), n, opt.r, opt.radial, false);
    shadeTube(geo, opt.radial, k * 2.1);
    const m = new THREE.Mesh(geo, mat); root.add(m); meshes.push(m);
  }
  const top = new THREE.Mesh(cuffGeometry(1.08, 0.6, 5), gold());
  top.position.copy(spine.getPointAt(0.015)); root.add(top);
  const tie = new THREE.Mesh(cuffGeometry(0.95, 0.36, 3), gold()); root.add(tie);
  let loose = [], last = -1;
  function rebuild(p) {
    loose.forEach((m) => { root.remove(m); m.geometry.dispose(); });
    loose = [];
    const s = Math.max(0.03, p);
    for (let k = 0; k < 3; k++) {
      const a = strandPoints(spine, fr, k, { ...opt, from: s, to: s, n: 1 })[0];
      const spread = (k - 1) * 1.5, bottom = -6.4, len = Math.max(0.5, a.y - bottom);
      const curve = new THREE.CatmullRomCurve3([
        a, new THREE.Vector3(a.x + spread * 0.35, a.y - len * 0.3, a.z + 0.3 * (k - 1)),
        new THREE.Vector3(a.x + spread * 0.8, a.y - len * 0.65, a.z), new THREE.Vector3(spread * 1.2 + Math.sin(k) * 0.3, bottom, 0),
      ]);
      const g = new THREE.TubeGeometry(curve, 40, opt.r * 0.95, opt.radial, false);
      shadeTube(g, opt.radial, k * 2.1);
      const m = new THREE.Mesh(g, mat); root.add(m); loose.push(m);
    }
    tie.visible = p > 0.03 && p < 0.985;
    tie.position.copy(spine.getPointAt(Math.min(0.999, s)));
    for (const m of meshes) m.geometry.setDrawRange(0, Math.floor(s * n) * opt.radial * 6);
  }
  scene.add(root);
  const resize = () => {
    const w = host.clientWidth || 1, h = host.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.fov = w / h < 0.8 ? 40 : 30;
    camera.updateProjectionMatrix();
  };
  resize();
  new ResizeObserver(resize).observe(host);
  let visible = true;
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; }, { rootMargin: '120px' }).observe(host);
  const clock = new THREE.Clock();
  const mouse = { x: 0, tx: 0 };
  addEventListener('pointermove', (e) => { mouse.tx = (e.clientX / innerWidth) * 2 - 1; }, { passive: true });
  const frame = () => {
    requestAnimationFrame(frame);
    if (!visible) return;
    const t = clock.getElapsedTime();
    mouse.x += (mouse.tx - mouse.x) * 0.05;
    const r = track.getBoundingClientRect();
    const p = THREE.MathUtils.clamp(-r.top / Math.max(1, r.height - innerHeight), 0, 1);
    const q = THREE.MathUtils.clamp((p - 0.12) / 0.76, 0, 1);
    if (Math.abs(q - last) > 0.003) { rebuild(q); last = q; }
    root.rotation.y = q * TAU * 0.5 + (REDUCE ? 0 : Math.sin(t * 0.4) * 0.1 + mouse.x * 0.3);
    renderer.render(scene, camera);
    canvas.classList.add('is-live');
  };
  frame();
}

mountCompanion();
document.querySelectorAll('canvas[data-scene="weave"]').forEach(mountWeave);
