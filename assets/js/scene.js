/* Mama Africa — the braid.
   One fixed canvas, one braid for the whole visit. Its shape is computed on the GPU from a handful of
   uniforms, so braiding, sliding and recolouring never rebuild geometry (smooth on phones).
   Home: three loose strands beside the headline braid themselves as you scroll the hero, then the braid
   slims into a rail in the right margin and follows you down the site.
   Other pages: the rail weaves itself in on arrival. Colour swatches anywhere on the site recolour it. */
import * as THREE from 'three';
import { RoomEnvironment } from './vendor/addons/RoomEnvironment.js';

const MOBILE = matchMedia('(max-width: 760px)').matches;
const REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;
const TAU = Math.PI * 2;

// hair colour codes used by braiding hair brands: [root, tip]
const SHADES = {
  '1B': [0x0b0705, 0x1a120d], '2': [0x0e0805, 0x2e1b10], '4': [0x100905, 0x4a2b17],
  '27': [0x140c06, 0x9c6631], '30': [0x120905, 0x733718], '350': [0x130905, 0x863a17],
  '613': [0x2e2113, 0xcfb27a], 'BUG': [0x100506, 0x581321], '99J': [0x0d0406, 0x440e26],
};

/* ---------------------------------------------------------------- materials */
function hairBump() {
  const c = document.createElement('canvas');
  c.width = 128; c.height = 1024;
  const g = c.getContext('2d');
  g.fillStyle = '#808080'; g.fillRect(0, 0, c.width, c.height);
  for (let i = 0; i < 2600; i++) {
    const y = Math.random() * c.height;
    g.strokeStyle = Math.random() > 0.5 ? `rgba(255,255,255,${0.06 + Math.random() * 0.22})` : `rgba(0,0,0,${0.08 + Math.random() * 0.26})`;
    g.lineWidth = 0.5 + Math.random() * 1.1;
    g.beginPath(); g.moveTo(0, y);
    g.bezierCurveTo(40, y + (Math.random() - 0.5) * 3, 90, y + (Math.random() - 0.5) * 3, c.width, y);
    g.stroke();
  }
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.anisotropy = 4;
  return t;
}

const U = {
  uLen: { value: 40 }, uEnd: { value: 40 }, uFront: { value: 0 }, uTipLen: { value: 1.6 },
  uSep: { value: 1.2 }, uSway: { value: 0.25 }, uOff: { value: 0 }, uTime: { value: 0 },
  uA: { value: 0.58 }, uB: { value: 0.35 }, uP: { value: 2.5 }, uR: { value: 0.37 },
  uRoot: { value: new THREE.Color(SHADES['350'][0]) }, uTip: { value: new THREE.Color(SHADES['350'][1]) },
  uOmbreLen: { value: 14 }, uRail: { value: 0 },
  uBend: { value: 0 }, uTop: { value: 5 }, uSpan: { value: 10 },
};

const BRAID_GLSL = /* glsl */`
uniform float uLen, uEnd, uFront, uTipLen, uSep, uSway, uOff, uTime, uA, uB, uP, uR;
attribute float aS; attribute float aA; attribute float aK;
varying float vY; varying float vK; varying float vA;
vec3 braided(float y, float k) {
  float ph = ((y + uOff) / uP) * 6.2831853 + k * 2.0943951;
  return vec3(uA * sin(ph), -y, uB * sin(2.0 * ph));
}
vec3 loose(float y, float k) {
  float d = max(y - uFront, 0.0);
  vec3 b = braided(uFront, k);
  float open = 1.0 - exp(-d * 0.45);
  float sw = sin(uTime * 0.8 + y * 0.3 + k * 2.1) * uSway * min(d * 0.14, 1.0);
  return vec3(b.x * exp(-d * 0.6) + (k - 1.0) * uSep * open + sw, -y,
              b.z * exp(-d * 0.8) + (k - 1.0) * 0.2 * open);
}
vec3 centerAt(float y, float k) {
  float w = 1.0 - smoothstep(uFront - 0.5, uFront + 0.35, y);
  return mix(loose(y, k), braided(y, k), w);
}
`;

const BEND_GLSL = `
  vec4 mvPosition = vec4( transformed, 1.0 );
  mvPosition = modelViewMatrix * mvPosition;
  float bt = clamp( ( uTop - mvPosition.y ) / uSpan, 0.0, 1.0 );
  mvPosition.x += uBend * bt * bt;
  gl_Position = projectionMatrix * mvPosition;`;

function bendInject(sh) {
  sh.uniforms.uBend = U.uBend; sh.uniforms.uTop = U.uTop; sh.uniforms.uSpan = U.uSpan;
  sh.vertexShader = 'uniform float uBend;\nuniform float uTop;\nuniform float uSpan;\n' + sh.vertexShader.replace('#include <project_vertex>', BEND_GLSL);
}

function braidMaterial() {
  const m = new THREE.MeshPhysicalMaterial({
    color: 0xffffff, roughness: 0.42, metalness: 0,
    sheen: 0.7, sheenColor: new THREE.Color(0x9a6a3c), sheenRoughness: 0.38,
    clearcoat: 0.22, clearcoatRoughness: 0.5,
    bumpMap: hairBump(), bumpScale: 1.6,
  });
  m.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, U);
    bendInject(sh);
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', '#include <common>\n' + BRAID_GLSL)
      .replace('#include <beginnormal_vertex>', `
        float gY = aS * uLen;
        vec3 gC = centerAt(gY, aK);
        vec3 gT = normalize(centerAt(gY + 0.04, aK) - gC);
        vec3 gN = normalize(cross(gT, vec3(0.0, 0.0, 1.0)));
        vec3 gB = normalize(cross(gT, gN));
        vec3 objectNormal = normalize(cos(aA) * gN + sin(aA) * gB);
        float gOpen = 1.0 - exp(-max(gY - uFront, 0.0) * 0.5);
        float gR = uR * (1.0 - 0.32 * gOpen) * (1.0 - smoothstep(uEnd - uTipLen, uEnd, gY)) * step(gY, uEnd);
        vY = gY; vK = aK; vA = aA;`)
      .replace('#include <begin_vertex>', 'vec3 transformed = gC + gR * objectNormal;');
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', '#include <common>\nuniform vec3 uRoot; uniform vec3 uTip; uniform float uOmbreLen; uniform float uRail;\nvarying float vY; varying float vK; varying float vA;')
      .replace('#include <color_fragment>', `
        float og = mix(smoothstep(0.1, 1.0, vY / uOmbreLen), 0.55, uRail);
        // fibres and strand bundles, so it reads as hair rather than a smooth tube
        float fib = 0.8 + 0.2 * sin(vA * 26.0 + sin(vY * 2.3 + vK * 1.7) * 3.0);
        float bundle = 0.84 + 0.16 * sin(vA * 7.0 + vK * 2.1 + vY * 0.9);
        diffuseColor.rgb *= mix(uRoot, uTip, og) * fib * bundle;`);
  };
  return m;
}

function strandsGeometry(len, perUnit, radial) {
  const seg = Math.max(60, Math.round(len * perUnit));
  const per = (seg + 1) * (radial + 1);
  const n = per * 3;
  const aS = new Float32Array(n), aA = new Float32Array(n), aK = new Float32Array(n), uv = new Float32Array(n * 2);
  const idx = [];
  for (let k = 0; k < 3; k++) {
    for (let i = 0; i <= seg; i++) {
      for (let j = 0; j <= radial; j++) {
        const v = k * per + i * (radial + 1) + j;
        aS[v] = i / seg; aA[v] = (j / radial) * TAU; aK[v] = k;
        uv[v * 2] = (i / seg) * len * 0.5; uv[v * 2 + 1] = j / radial;
      }
    }
    for (let i = 0; i < seg; i++) {
      for (let j = 0; j < radial; j++) {
        const a = k * per + i * (radial + 1) + j, b = a + radial + 1;
        idx.push(a, b, a + 1, b, b + 1, a + 1);
      }
    }
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(new Float32Array(n * 3), 3));
  g.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(n * 3), 3));
  g.setAttribute('uv', new THREE.BufferAttribute(uv, 2));
  g.setAttribute('aS', new THREE.BufferAttribute(aS, 1));
  g.setAttribute('aA', new THREE.BufferAttribute(aA, 1));
  g.setAttribute('aK', new THREE.BufferAttribute(aK, 1));
  g.setIndex(idx);
  return g;
}

function cuffGeometry(R, h, ridges) {
  const pts = [], N = 60;
  for (let i = 0; i <= N; i++) {
    const t = i / N;
    pts.push(new THREE.Vector2(R + Math.pow(Math.abs(Math.sin(t * Math.PI * ridges)), 0.6) * 0.055 + Math.sin(t * Math.PI) * 0.05, -h / 2 + h * t));
  }
  for (let i = N; i >= 0; i--) pts.push(new THREE.Vector2(R - 0.035, -h / 2 + h * (i / N)));
  return new THREE.LatheGeometry(pts, 72);
}

function cowrieGeometry() {
  const g = new THREE.SphereGeometry(1, 48, 32);
  const p = g.attributes.position;
  const col = new Float32Array(p.count * 3);
  const ivory = new THREE.Color(0xf2e7d2), cream = new THREE.Color(0xd9c3a0), dark = new THREE.Color(0x3a2416), c = new THREE.Color();
  for (let i = 0; i < p.count; i++) {
    let x = p.getX(i), y = p.getY(i), z = p.getZ(i);
    const pinch = 1 - 0.28 * Math.pow(Math.abs(x), 3);
    y *= 0.64 * pinch; z *= 0.52 * pinch;
    if (z < 0) z *= 0.38;
    const d = Math.abs(y) / 0.64;
    if (z <= 0 && d < 0.2) { const gr = 1 - d / 0.2; z += 0.07 * gr; y *= 1 - 0.25 * gr; }
    p.setXYZ(i, x, y, z);
    c.copy(ivory).lerp(cream, THREE.MathUtils.clamp(0.5 - z * 0.9 + Math.abs(x) * 0.25, 0, 1));
    if (z <= 0.02 && d < 0.16 && !(Math.cos(x * 34) > 0.15 && d > 0.05)) c.copy(dark);
    col.set([c.r, c.g, c.b], i * 3);
  }
  g.setAttribute('color', new THREE.BufferAttribute(col, 3));
  g.computeVertexNormals();
  return g;
}

/* ---------------------------------------------------------------- stage */
function start() {
  const canvas = document.createElement('canvas');
  canvas.className = 'braid3d';
  canvas.setAttribute('aria-hidden', 'true');
  document.body.appendChild(canvas);
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true, powerPreference: 'high-performance' });
  } catch (e) { canvas.remove(); return; }
  renderer.setPixelRatio(Math.min(devicePixelRatio, MOBILE ? 2 : 1.75));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  scene.environment = new THREE.PMREMGenerator(renderer).fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = 0.45;
  const key = new THREE.DirectionalLight(0xffdcb0, 2.6); key.position.set(-5, 7, 8); scene.add(key);
  const rim = new THREE.DirectionalLight(0xf08a3a, 2.4); rim.position.set(6, 2, -6); scene.add(rim);
  const fill = new THREE.DirectionalLight(0xfff3e4, 0.7); fill.position.set(2, -4, 6); scene.add(fill);
  scene.add(new THREE.AmbientLight(0xfff0e0, 0.25));
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 100);
  camera.position.set(0, 0, 20);

  const WIDTH = 2 * (U.uA.value + U.uR.value);
  const UNIT = U.uP.value * (MOBILE ? 4 : 3), REPEAT = UNIT * 2;
  const holder = new THREE.Group(), spin = new THREE.Group();
  holder.add(spin); scene.add(holder);
  const mat = braidMaterial();
  let mesh = null;
  const gold = new THREE.MeshStandardMaterial({ color: 0xdba64c, metalness: 1, roughness: 0.2 });
  gold.onBeforeCompile = bendInject;
  const cowMat = new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.28, clearcoat: 0.8, clearcoatRoughness: 0.2 });
  cowMat.onBeforeCompile = bendInject;
  const cuffBig = cuffGeometry(1.02, 0.6, 5), cuffSmall = cuffGeometry(1.0, 0.36, 3), cowGeo = cowrieGeometry();
  const deco = [];
  for (let i = 0; i < 26; i++) {
    const c = new THREE.Mesh(i % 2 ? cuffSmall : cuffBig, gold);
    c.userData = { i, kind: 'cuff' }; spin.add(c); deco.push(c);
    if (i % 2 === 1) {
      const s = new THREE.Mesh(cowGeo, cowMat);
      s.scale.setScalar(0.42); s.rotation.set(0, Math.PI, Math.PI / 2);
      s.userData = { i, kind: 'cowrie' }; spin.add(s); deco.push(s);
    }
  }
  const finisher = new THREE.Mesh(cuffBig, gold); // the cuff that closes the hero braid
  spin.add(finisher);

  const heroEl = document.querySelector('[data-braid-hero]');
  const st = {};
  const probe = document.createElement('div');
  probe.style.cssText = 'position:fixed;top:0;left:0;width:0;height:100vh;height:100lvh;visibility:hidden;pointer-events:none';
  document.body.appendChild(probe);

  function layout() {
    const vw = innerWidth;
    const vh = MOBILE ? Math.max(probe.offsetHeight || 0, innerHeight) : innerHeight;
    const wrap = document.querySelector('main .wrap');
    let contentRight = vw - 40;
    if (wrap) { const r = wrap.getBoundingClientRect(); contentRight = r.right - parseFloat(getComputedStyle(wrap).paddingRight); }
    const free = Math.max(0, vw - contentRight);
    if (MOBILE) {
      Object.assign(st, { railW: 22, railCx: vw - 17, heroW: 64, heroCx: vw - 58 });
    } else {
      const railW = THREE.MathUtils.clamp(free - 18, 20, 64);
      const slot = heroEl && heroEl.querySelector('[data-braid-slot]');
      let heroCx = vw * 0.74, heroW = THREE.MathUtils.clamp(vw * 0.12, 140, 220);
      if (slot) { const r = slot.getBoundingClientRect(); heroCx = r.left + r.width / 2; heroW = THREE.MathUtils.clamp(r.width * 0.42, 130, 230); }
      Object.assign(st, { railW, railCx: Math.min(contentRight + free / 2, vw - railW / 2 - 8), heroW, heroCx });
    }
    st.vw = vw; st.vh = vh;
    renderer.setSize(vw, vh, false);
    canvas.style.width = vw + 'px'; canvas.style.height = vh + 'px';
    camera.aspect = vw / vh; camera.updateProjectionMatrix();
    st.worldH = 2 * camera.position.z * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    st.upp = st.worldH / vh;
    U.uTop.value = st.worldH / 2; U.uSpan.value = st.worldH;
    const railScale = (st.railW * st.upp) / WIDTH;
    const len = Math.ceil((st.worldH / railScale + REPEAT * 1.5) / REPEAT) * REPEAT;
    if (!mesh || Math.abs(len - U.uLen.value) > 0.01) {
      if (mesh) { spin.remove(mesh); mesh.geometry.dispose(); }
      U.uLen.value = len;
      mesh = new THREE.Mesh(strandsGeometry(len, MOBILE ? 11 : 17, MOBILE ? 12 : 18), mat);
      mesh.frustumCulled = false;
      spin.add(mesh);
    }
  }
  layout();
  let lastW = innerWidth;
  addEventListener('resize', () => {
    if (MOBILE && Math.abs(innerWidth - lastW) < 2) return; // address bar only
    lastW = innerWidth; layout();
  });

  // colour
  const want = { root: U.uRoot.value.clone(), tip: U.uTip.value.clone() };
  function setColor(code, instant) {
    const s = SHADES[code]; if (!s) return;
    want.root.set(s[0]); want.tip.set(s[1]);
    if (instant) { U.uRoot.value.copy(want.root); U.uTip.value.copy(want.tip); }
    try { sessionStorage.setItem('ma-color', code); } catch (e) {}
    document.documentElement.dataset.shade = code;
  }
  let saved = null;
  try { saved = sessionStorage.getItem('ma-color'); } catch (e) {}
  setColor(saved && SHADES[saved] ? saved : '4', true);
  document.addEventListener('ma:color', (e) => setColor(e.detail));

  let seen = false;
  try { seen = sessionStorage.getItem('ma-braid') === '1'; sessionStorage.setItem('ma-braid', '1'); } catch (e) {}
  const introDur = REDUCE ? 0 : (seen ? 0.9 : 1.8);
  const clock = new THREE.Clock();
  let lastY = scrollY, vel = 0, bend = 0, bendV = 0, spinOff = 0, opacity = 0;
  const smooth = (x) => x * x * (3 - 2 * x);
  const clamp01 = (x) => Math.min(1, Math.max(0, x));
  const ease = (x) => 1 - Math.pow(1 - x, 3);

  function frame() {
    requestAnimationFrame(frame);
    const t = clock.getElapsedTime();
    const y = Math.max(0, scrollY);
    const dy = THREE.MathUtils.clamp(y - lastY, -80, 80); lastY = y;
    vel += (dy - vel) * 0.2;
    U.uTime.value = t;
    U.uRoot.value.lerp(want.root, 0.06); U.uTip.value.lerp(want.tip, 0.06);

    // hp 0..1 through the pinned hero (home only)
    let braid = 1, toRail = 1, railY = y;
    if (heroEl) {
      const r = heroEl.getBoundingClientRect();
      const span = Math.max(1, r.height - st.vh);
      const hp = clamp01(-r.top / span);
      braid = REDUCE ? 1 : smooth(clamp01(hp / 0.62));
      toRail = smooth(clamp01((hp - 0.66) / 0.34));
      railY = Math.max(0, -r.top - span);
    }
    const intro = introDur ? ease(clamp01((t - 0.2) / introDur)) : 1;
    const W = THREE.MathUtils.lerp(st.heroW, st.railW, heroEl ? toRail : 1);
    const cx = THREE.MathUtils.lerp(st.heroCx, st.railCx, heroEl ? toRail : 1);
    const s = (W * st.upp) / WIDTH;
    holder.scale.setScalar(s);
    holder.position.x = (cx - st.vw / 2) * st.upp;
    const drop = heroEl ? (1 - intro) * 3 : 0; // on arrival the strands drop in
    holder.position.y = st.worldH / 2 + 0.8 * s + drop;

    const visible = st.worldH / s; // local units from the top of the screen to the bottom
    const heroEnd = visible * (MOBILE ? 0.8 : 0.86);
    const railEnd = visible + 2;
    U.uOmbreLen.value = heroEl ? THREE.MathUtils.lerp(heroEnd, railEnd, toRail) : railEnd;
    U.uRail.value = heroEl ? toRail : 1;
    if (heroEl) {
      U.uEnd.value = THREE.MathUtils.lerp(heroEnd, railEnd, toRail);
      // starts a quarter braided so the first frame already reads as a braid in progress
      U.uFront.value = THREE.MathUtils.lerp(heroEnd * 0.26 + braid * (heroEnd * 0.74 - 2.6), railEnd + 1, toRail);
      U.uSep.value = (1 - toRail) * (MOBILE ? 0.9 : 1.25);
      U.uTipLen.value = THREE.MathUtils.lerp(2.2, 0.01, toRail);
    } else {
      U.uEnd.value = railEnd;
      U.uFront.value = REDUCE ? railEnd + 1 : intro * (railEnd + 1);
      U.uSep.value = 0.55;
      U.uTipLen.value = 0.01;
    }
    U.uSway.value = REDUCE ? 0 : 0.22;
    U.uOff.value = (railY * 0.42 * st.upp) / s;

    // gold cuffs and cowries ride on the braided part, sliding with it
    const slide = ((U.uOff.value % REPEAT) + REPEAT) % REPEAT;
    for (const d of deco) {
      const ly = d.userData.i * UNIT + UNIT * 0.5 - slide + (d.userData.kind === 'cowrie' ? UNIT * 0.5 : 0);
      d.position.set(0, -ly, d.userData.kind === 'cowrie' ? 0.86 : 0);
      d.visible = ly < U.uFront.value - 1.2 && ly > -1.5 && ly < U.uEnd.value - 1 && (!heroEl || toRail > 0.05);
    }
    finisher.visible = !!heroEl && braid > 0.35 && toRail < 0.6;
    finisher.position.set(0, -Math.max(0.6, U.uFront.value - 0.2), 0);
    finisher.scale.setScalar(0.4 + 0.6 * clamp01((braid - 0.35) / 0.2));

    if (!REDUCE) {
      const maxSpin = MOBILE ? 0.45 : 1.0;
      spinOff = THREE.MathUtils.clamp((spinOff + vel * (MOBILE ? 0.0012 : 0.002)) * 0.965, -maxSpin, maxSpin);
      const maxPx = MOBILE ? 7 : 20;
      const target = THREE.MathUtils.clamp(-vel * 0.35, -maxPx, maxPx) + Math.sin(t * 0.7) * (MOBILE ? 1 : 2.5);
      bendV += (target - bend) * 0.06; bendV *= 0.86; bend += bendV;
    }
    spin.rotation.y = Math.sin(t * 0.35) * (MOBILE ? 0.28 : 0.36) + spinOff;
    U.uBend.value = bend * st.upp;

    const hide = document.body.classList.contains('menu-open') || document.body.classList.contains('sheet-open');
    opacity += ((hide ? 0 : 1) - opacity) * 0.1;
    canvas.style.opacity = opacity.toFixed(3);
    if (opacity > 0.01) renderer.render(scene, camera);
  }
  frame();
  window.MA3D = { setColor: (c) => setColor(c) };
}

start();
