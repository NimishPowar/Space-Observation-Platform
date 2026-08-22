import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

/* ======================================================================
   CONSTANTS — real-world figures. Nothing derived from these is ever
   hardcoded again below; nested groups + scale() calls do the rest.
   ====================================================================== */

const DEG = Math.PI / 180;

const KM = {
  sunRadius: 696000,
  earthRadius: 6371,
  moonRadius: 1737.4,
  sunDistance: 149_600_000,   // 1 AU
  moonDistance: 384_400,      // Earth–Moon mean distance
};

const EARTH_AXIAL_TILT = 23.5 * DEG;
const MOON_ORBIT_INCLINATION = 5.1 * DEG;
const SYNODIC_MONTH_DAYS = 29.530588853;
const SECONDS_PER_DAY = 86400;
const EARTH_SIDEREAL_DAY_SECONDS = 86164; // spin period (independent of orbit)

// A known reference New Moon (2000-01-06 18:14 UTC) lets us compute the
// real, current Sun–Earth–Moon phase angle from the system clock, so
// "Sync to tonight's real Moon" isn't a lookup table — it's the same
// synodic-period math the sim already runs, just anchored to real time.
const REFERENCE_NEW_MOON_MS = Date.UTC(2000, 0, 6, 18, 14, 0);

function realWorldElapsedDays(nowMs = Date.now()) {
  const diffDays = (nowMs - REFERENCE_NEW_MOON_MS) / (SECONDS_PER_DAY * 1000);
  return ((diffDays % SYNODIC_MONTH_DAYS) + SYNODIC_MONTH_DAYS) % SYNODIC_MONTH_DAYS;
}

// Two scale "lenses" onto the same real system. "true" uses one uniform
// km-per-unit factor for everything (1 unit = 1000 km) so proportions are
// exact. "visual" exaggerates sizes/distances independently for legibility.
const SCALE_MODES = {
  true: {
    kmPerUnit: 1000,
    sunRadius: KM.sunRadius / 1000,
    earthRadius: KM.earthRadius / 1000,
    moonRadius: KM.moonRadius / 1000,
    sunDistance: KM.sunDistance / 1000,
    moonDistance: KM.moonDistance / 1000,
  },
  visual: {
    sunRadius: 42,
    earthRadius: 5,
    moonRadius: 1.35,
    sunDistance: 420,
    moonDistance: 22,
  },
};

/* ======================================================================
   RENDERER / SCENE / CAMERAS
   ====================================================================== */

const canvas = document.getElementById('main-canvas');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, logarithmicDepthBuffer: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.05;
renderer.outputColorSpace = THREE.SRGBColorSpace;

const scene = new THREE.Scene();

const godCamera = new THREE.PerspectiveCamera(45, 1, 0.05, 10);
godCamera.position.set(0, 26, 60);

const earthObserverCamera = new THREE.PerspectiveCamera(50, 1, 0.01, 10);

// Dedicated, always-straight-down camera for the inset when Earth Observer
// is the main view. Deliberately NOT the interactive God's-Eye camera —
// that one can be dragged to any oblique angle by the user, which defeats
// the point of a quick "here's why it looks like that" reference view.
// A fixed top-down diagram is what actually helps at a glance.
const topDownCamera = new THREE.PerspectiveCamera(50, 1, 0.01, 10);
topDownCamera.up.set(0, 0, -1); // fixes a stable "north" so it never spins between frames

const controls = new OrbitControls(godCamera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minDistance = 2;

// Inset "money shot" renderer — always Earth-observer, independent of main view
const insetCanvas = document.getElementById('inset-canvas');
const insetRenderer = new THREE.WebGLRenderer({ canvas: insetCanvas, antialias: true });
insetRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
insetRenderer.toneMapping = THREE.ACESFilmicToneMapping;
insetRenderer.outputColorSpace = THREE.SRGBColorSpace;

/* ======================================================================
   STATE
   ====================================================================== */

const state = {
  scaleMode: 'visual',
  cameraMode: 'god',
  playing: true,
  timeWarp: 86400,           // simulated seconds per real second
  elapsedDays: realWorldElapsedDays(), // boot already synced to tonight's real Moon
  S: null,                    // active scale-mode figures (see applyScale)
};

/* ======================================================================
   STARFIELD — custom GLSL shader (soft falloff + twinkle), not PointsMaterial
   ====================================================================== */

function buildStarfield() {
  const COUNT = 6000;
  const positions = new Float32Array(COUNT * 3);
  const sizes = new Float32Array(COUNT);
  const phases = new Float32Array(COUNT);

  for (let i = 0; i < COUNT; i++) {
    // random point on a unit sphere (rejection-free)
    const u = Math.random(), v = Math.random();
    const theta = 2 * Math.PI * u;
    const phi = Math.acos(2 * v - 1);
    positions[i * 3 + 0] = Math.sin(phi) * Math.cos(theta);
    positions[i * 3 + 1] = Math.sin(phi) * Math.sin(theta);
    positions[i * 3 + 2] = Math.cos(phi);
    sizes[i] = THREE.MathUtils.randFloat(1.0, 3.2);
    phases[i] = Math.random() * Math.PI * 2;
  }

  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geo.setAttribute('aSize', new THREE.BufferAttribute(sizes, 1));
  geo.setAttribute('aPhase', new THREE.BufferAttribute(phases, 1));

  const mat = new THREE.ShaderMaterial({
    uniforms: { uTime: { value: 0 } },
    vertexShader: `
      attribute float aSize;
      attribute float aPhase;
      varying float vPhase;
      uniform float uTime;
      void main() {
        vPhase = aPhase;
        vec4 mv = modelViewMatrix * vec4(position, 1.0);
        gl_Position = projectionMatrix * mv;
        gl_PointSize = aSize * (300.0 / -mv.z);
      }
    `,
    fragmentShader: `
      varying float vPhase;
      uniform float uTime;
      void main() {
        vec2 c = gl_PointCoord - vec2(0.5);
        float d = length(c);
        float falloff = smoothstep(0.5, 0.0, d);
        float twinkle = 0.55 + 0.45 * sin(uTime * (0.8 + fract(vPhase)) + vPhase * 6.2831);
        gl_FragColor = vec4(vec3(1.0, 0.98, 0.92), falloff * twinkle);
      }
    `,
    transparent: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
  });

  const points = new THREE.Points(geo, mat);
  points.frustumCulled = false;
  return points;
}

const starfield = buildStarfield();
scene.add(starfield);

/* ======================================================================
   TEXTURES — real NASA-sourced imagery, served locally from images/,
   downsampled from 8K sources to ~2048px for the web.
   ====================================================================== */

const TEX_BASE = 'images/';
const loader = new THREE.TextureLoader();

function loadTex(name, colorSpace) {
  const t = loader.load(TEX_BASE + name);
  if (colorSpace) t.colorSpace = colorSpace;
  t.anisotropy = 8;
  return t;
}

const sunTex = loadTex('sun.jpg', THREE.SRGBColorSpace);
const earthTex = loadTex('earth_daymap.jpg', THREE.SRGBColorSpace);
const earthNightTex = loadTex('earth_nightmap.jpg', THREE.SRGBColorSpace);
const moonTex = loadTex('moon.jpg', THREE.SRGBColorSpace);

/* ======================================================================
   SUN — unlit emissive sphere (it IS the light source's visual proxy);
   actual illumination of Earth/Moon comes from a separate DirectionalLight
   ====================================================================== */

const sunPivot = new THREE.Group();
scene.add(sunPivot);

const sunGeo = new THREE.SphereGeometry(1, 64, 64);
const sunMat = new THREE.MeshBasicMaterial({ map: sunTex });
const sunMesh = new THREE.Mesh(sunGeo, sunMat);
const BLOOM_LAYER = 1;
sunMesh.layers.enable(BLOOM_LAYER);
sunPivot.add(sunMesh);

// Distant DirectionalLight = parallel rays from the Sun's direction.
// This alone drives every terminator line in the scene — no faked phase textures.
const sunLight = new THREE.DirectionalLight(0xfff4e0, 3.2);
sunLight.target.position.set(0, 0, 0);
scene.add(sunLight);
scene.add(sunLight.target);

// Keep ambient vanishingly small so the unlit face stays genuinely dark.
const ambient = new THREE.AmbientLight(0x223355, 0.015);
scene.add(ambient);

/* ======================================================================
   EARTH — orbit pivot → tilt group → spin mesh (nested, never combined,
   so axial tilt and daily spin never fight each other via Euler order)
   ====================================================================== */

const earthOrbitPivot = new THREE.Group(); // reserved for a future heliocentric orbit; stationary here
scene.add(earthOrbitPivot);

const earthTiltGroup = new THREE.Group();
// Tilt about Z, sign chosen so the North Pole leans toward the Sun (+X) —
// the classic, immediately-recognizable solstice orientation. This also
// maximizes the visible lighting contrast between hemispheres, so the
// tilt reads clearly instead of getting lost edge-on to the camera.
earthTiltGroup.rotation.z = -EARTH_AXIAL_TILT;
earthOrbitPivot.add(earthTiltGroup);

const earthGeo = new THREE.SphereGeometry(1, 96, 96);
const earthMat = new THREE.MeshStandardMaterial({
  map: earthTex,
  roughness: 0.85,
  metalness: 0.0,
});

const earthSpinMesh = new THREE.Mesh(earthGeo, earthMat);
earthTiltGroup.add(earthSpinMesh);

// City lights on the unlit hemisphere only. Rather than reaching into
// MeshStandardMaterial's internals (fragile — depends on exact chunk/
// variable names that shift between three.js versions and are hard to
// verify without a browser to test in), this is a fully separate,
// self-contained overlay: a second unit sphere, same child of the spin
// mesh (so it automatically inherits Earth's tilt, spin, and scale with
// zero extra sync code), with its own tiny shader computing sun-facing
// purely from a world-space light-direction uniform we set every frame.
// Additive blending + no depth write means it only ever brightens the
// dark hemisphere and never fights the base Earth draw for the depth buffer.
const nightMat = new THREE.ShaderMaterial({
  uniforms: {
    nightTexture: { value: earthNightTex },
    sunDirection: { value: new THREE.Vector3(1, 0, 0) }, // world-space, Earth -> Sun
  },
  vertexShader: `
    varying vec3 vWorldNormal;
    varying vec2 vUv2;
    void main() {
      vUv2 = uv;
      vWorldNormal = normalize(mat3(modelMatrix) * normal);
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D nightTexture;
    uniform vec3 sunDirection;
    varying vec3 vWorldNormal;
    varying vec2 vUv2;
    void main() {
      float sunFacing = dot(normalize(vWorldNormal), normalize(sunDirection));
      // 1 (full night glow) below -0.2, fading to 0 (full day, no glow) by 0.15
      float nightMix = 1.0 - smoothstep(-0.2, 0.15, sunFacing);
      vec3 nightColor = texture2D(nightTexture, vUv2).rgb;
      gl_FragColor = vec4(nightColor * nightMix * 1.6, 1.0);
    }
  `,
  transparent: true,
  depthWrite: false,
  blending: THREE.AdditiveBlending,
});
const nightMesh = new THREE.Mesh(earthGeo, nightMat);
earthSpinMesh.add(nightMesh); // child of the spin mesh: inherits tilt+spin+scale for free

// Thin atmosphere shell — radius always derived from earthRadius, never literal
const atmoGeo = new THREE.SphereGeometry(1, 64, 64);
const atmoMat = new THREE.MeshBasicMaterial({
  color: 0x5588ff,
  transparent: true,
  opacity: 0.12,
  side: THREE.BackSide,
});
const atmosphere = new THREE.Mesh(atmoGeo, atmoMat);
earthTiltGroup.add(atmosphere);

/* ======================================================================
   MOON — orbit pivot (5.1° inclined) → angle group (theta) → mesh.
   Tidal lock falls out of the hierarchy for free: the mesh is a rigid
   child at a fixed local offset with a FIXED local rotation, so as the
   angle group sweeps theta, the mesh's world orientation sweeps with it
   and the same hemisphere always faces the pivot's origin (Earth).
   ====================================================================== */

const moonOrbitPivot = new THREE.Group();
moonOrbitPivot.rotation.x = MOON_ORBIT_INCLINATION;
earthOrbitPivot.add(moonOrbitPivot); // centered on Earth

const moonAngleGroup = new THREE.Group(); // rotation.y = theta, driven each frame
moonOrbitPivot.add(moonAngleGroup);

const moonGeo = new THREE.SphereGeometry(1, 64, 64);
const moonMat = new THREE.MeshStandardMaterial({
  map: moonTex,
  roughness: 1.0,
  metalness: 0.0,
});
const moonMesh = new THREE.Mesh(moonGeo, moonMat);
// Fixed local orientation -> automatic tidal lock (see hierarchy note above).
// π (not π/2): THREE.SphereGeometry maps texture u=0.5 (the conventional
// near-side center of a Moon equirectangular map) to local +X, and the
// constant "toward Earth" direction inside this rotating frame is local
// -X, so the mesh's own +X must be flipped 180° to align the two.
moonMesh.rotation.y = Math.PI;
moonAngleGroup.add(moonMesh);

// Faint orbit ring, radius always derived from the live moonDistance
const ringGeo = new THREE.RingGeometry(0.995, 1.0, 128);
const ringMat = new THREE.MeshBasicMaterial({
  color: 0x8892a4, transparent: true, opacity: 0.18,
  side: THREE.DoubleSide,
});
const orbitRing = new THREE.Mesh(ringGeo, ringMat);
orbitRing.rotation.x = Math.PI / 2;
moonOrbitPivot.add(orbitRing);

/* ======================================================================
   SCALE SYSTEM — the only place radii/distances are ever assigned.
   Every mesh keeps a unit-radius geometry; scale.setScalar() does the work,
   which is what avoids the "True-scale blowup" failure mode.
   ====================================================================== */

function applyScale(mode) {
  const S = SCALE_MODES[mode];
  state.scaleMode = mode;
  state.S = S;

  sunMesh.scale.setScalar(S.sunRadius);
  sunPivot.position.set(S.sunDistance, 0, 0);

  earthSpinMesh.scale.setScalar(S.earthRadius);
  atmosphere.scale.setScalar(S.earthRadius * 1.02);

  moonMesh.scale.setScalar(S.moonRadius);
  moonMesh.position.set(S.moonDistance, 0, 0);

  orbitRing.scale.setScalar(S.moonDistance);

  // Starfield + camera clipping always sized relative to the current
  // furthest feature (the Sun), never a hardcoded absolute number.
  const farEdge = Math.max(S.sunDistance * 2.4, S.moonDistance * 40);
  starfield.scale.setScalar(farEdge);
  godCamera.far = farEdge * 1.05;
  godCamera.near = mode === 'true' ? 0.05 : 0.01;
  godCamera.updateProjectionMatrix();
  earthObserverCamera.far = farEdge * 1.05;
  earthObserverCamera.updateProjectionMatrix();
  topDownCamera.far = farEdge * 1.05;
  topDownCamera.near = mode === 'true' ? 0.05 : 0.01;
  topDownCamera.updateProjectionMatrix();

  controls.maxDistance = farEdge * 0.5;

  // Frame a sensible default view for the mode
  if (mode === 'true') {
    godCamera.position.set(S.moonDistance * 0.9, S.moonDistance * 0.5, S.moonDistance * 1.3);
  } else {
    godCamera.position.set(S.moonDistance * 1.6, S.moonDistance * 0.9, S.moonDistance * 2.1);
  }
  controls.target.set(0, 0, 0);
  controls.update();

  // Straight overhead, framed to comfortably fit Earth's orbit ring —
  // distance derived from moonDistance, never a hardcoded absolute number.
  topDownCamera.position.set(0, S.moonDistance * 2.6, 0.0001);
  topDownCamera.lookAt(0, 0, 0);
}

/* ======================================================================
   SELECTIVE BLOOM — Sun only, near-zero bleed onto Earth/Moon.
   Standard two-pass technique: render everything else blacked-out into a
   bloom buffer, then additively composite that buffer over the base render.
   ====================================================================== */

const bloomLayer = new THREE.Layers();
bloomLayer.set(BLOOM_LAYER);
const darkMaterial = new THREE.MeshBasicMaterial({ color: 0x000000 });
const materialCache = new Map();

function darkenNonBloomed(obj) {
  if (obj.material && !bloomLayer.test(obj.layers)) {
    materialCache.set(obj, obj.material);
    obj.material = darkMaterial;
  }
}
function restoreMaterials(obj) {
  if (materialCache.has(obj)) {
    obj.material = materialCache.get(obj);
    materialCache.delete(obj);
  }
}

const renderSize = new THREE.Vector2(1, 1);

const bloomComposer = new EffectComposer(renderer);
bloomComposer.renderToScreen = false;
bloomComposer.addPass(new RenderPass(scene, godCamera));
const bloomPass = new UnrealBloomPass(renderSize, 1.15, 0.5, 0.86);
bloomComposer.addPass(bloomPass);

const mixShader = {
  uniforms: {
    baseTexture: { value: null },
    bloomTexture: { value: bloomComposer.renderTarget2.texture },
  },
  vertexShader: `
    varying vec2 vUv;
    void main() { vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }
  `,
  fragmentShader: `
    uniform sampler2D baseTexture;
    uniform sampler2D bloomTexture;
    varying vec2 vUv;
    void main() {
      vec4 base = texture2D(baseTexture, vUv);
      vec4 bloom = texture2D(bloomTexture, vUv);
      gl_FragColor = base + bloom;
    }
  `,
};
const mixPass = new ShaderPass(new THREE.ShaderMaterial({
  uniforms: mixShader.uniforms,
  vertexShader: mixShader.vertexShader,
  fragmentShader: mixShader.fragmentShader,
  defines: {},
}), 'baseTexture');
mixPass.needsSwap = true;

const finalComposer = new EffectComposer(renderer);
finalComposer.addPass(new RenderPass(scene, godCamera));
finalComposer.addPass(mixPass);
finalComposer.addPass(new OutputPass());

function renderWithSelectiveBloom(camera) {
  bloomComposer.passes[0].camera = camera;
  finalComposer.passes[0].camera = camera;

  scene.traverse(darkenNonBloomed);
  bloomComposer.render();
  scene.traverse(restoreMaterials);

  finalComposer.render();
}

/* ======================================================================
   PHASE ENGINE
   ====================================================================== */

const PHASE_NAMES = [
  'New Moon', 'Waxing Crescent', 'First Quarter', 'Waxing Gibbous',
  'Full Moon', 'Waning Gibbous', 'Last Quarter', 'Waning Crescent',
];

const phaseNameEl = document.getElementById('phase-name');
const phaseIllumEl = document.getElementById('phase-illum');
const phaseDayEl = document.getElementById('phase-day');
const dialTerminator = document.getElementById('dial-terminator');

const _sunWorld = new THREE.Vector3();
const _moonWorld = new THREE.Vector3();
const _earthWorld = new THREE.Vector3();
const _sunDir = new THREE.Vector3();
const _moonDir = new THREE.Vector3();
const _orbitNormal = new THREE.Vector3();
const _cross = new THREE.Vector3();
const _q = new THREE.Quaternion();

function computePhase() {
  sunMesh.getWorldPosition(_sunWorld);
  moonMesh.getWorldPosition(_moonWorld);
  earthSpinMesh.getWorldPosition(_earthWorld);

  _sunDir.subVectors(_sunWorld, _earthWorld).normalize();
  _moonDir.subVectors(_moonWorld, _earthWorld).normalize();

  const elongation = THREE.MathUtils.radToDeg(
    Math.acos(THREE.MathUtils.clamp(_sunDir.dot(_moonDir), -1, 1))
  ); // 0..180, no sign

  moonOrbitPivot.getWorldQuaternion(_q);
  _orbitNormal.set(0, 1, 0).applyQuaternion(_q);
  _cross.crossVectors(_sunDir, _moonDir);
  const sign = _cross.dot(_orbitNormal) >= 0 ? 1 : -1;

  let phaseAngle = sign >= 0 ? elongation : 360 - elongation;
  phaseAngle = ((phaseAngle % 360) + 360) % 360;

  const illum = (1 - Math.cos(phaseAngle * DEG)) / 2;
  const bucket = Math.round(phaseAngle / 45) % 8;

  return { phaseAngle, illum, name: PHASE_NAMES[bucket] };
}

function moonDialPath(illum, waxing) {
  const R = 40, cx = 50, cy = 50;
  const rx = R * Math.abs(1 - 2 * illum);
  const sweepLimb = waxing ? 1 : 0;
  const sweepTerm = illum < 0.5 ? sweepLimb : 1 - sweepLimb;
  return `M ${cx},${cy - R} A ${R},${R} 0 0 ${sweepLimb} ${cx},${cy + R} ` +
         `A ${rx},${R} 0 0 ${sweepTerm} ${cx},${cy - R} Z`;
}

function updatePhaseUI() {
  const { phaseAngle, illum, name } = computePhase();
  const waxing = phaseAngle < 180;

  phaseNameEl.textContent = name;
  phaseIllumEl.textContent = `${Math.round(illum * 100)}% illuminated`;
  phaseDayEl.textContent = `day ${state.elapsedDays.toFixed(1)} / ${SYNODIC_MONTH_DAYS.toFixed(2)}`;
  dialTerminator.setAttribute('d', moonDialPath(illum, waxing));
}

/* ======================================================================
   ORBITAL MOTION — true angular motion at the real synodic-month rate,
   no lerp/easing fakes.
   ====================================================================== */

function advanceTime(deltaSeconds) {
  state.elapsedDays = (state.elapsedDays + deltaSeconds / SECONDS_PER_DAY) % SYNODIC_MONTH_DAYS;
  applyMoonAngleFromDays();

  const spinFraction = deltaSeconds / EARTH_SIDEREAL_DAY_SECONDS;
  earthSpinMesh.rotation.y += spinFraction * Math.PI * 2;
}

function applyMoonAngleFromDays() {
  const theta = (state.elapsedDays / SYNODIC_MONTH_DAYS) * Math.PI * 2;
  moonAngleGroup.rotation.y = theta;
}

/* ======================================================================
   EARTH-OBSERVER CAMERA — snapped every frame, no lerp lag, positioned at
   the sub-lunar point on Earth's surface for the "as we actually see it" view
   ====================================================================== */

const _subLunarDir = new THREE.Vector3();

function updateEarthObserverCamera() {
  moonMesh.getWorldPosition(_moonWorld);
  earthSpinMesh.getWorldPosition(_earthWorld);

  _subLunarDir.subVectors(_moonWorld, _earthWorld).normalize();
  const r = state.S.earthRadius * 1.001;
  earthObserverCamera.position.copy(_earthWorld).addScaledVector(_subLunarDir, r);
  earthObserverCamera.up.set(0, 1, 0);
  earthObserverCamera.lookAt(_moonWorld);
}

/* ======================================================================
   UI WIRING
   ====================================================================== */

document.getElementById('scale-toggle').addEventListener('click', (e) => {
  const btn = e.target.closest('button[data-scale]');
  if (!btn) return;
  document.querySelectorAll('#scale-toggle button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  applyScale(btn.dataset.scale);
});

const insetLabelEl = document.getElementById('inset-label');

document.getElementById('camera-toggle').addEventListener('click', (e) => {
  const btn = e.target.closest('button[data-cam]');
  if (!btn) return;
  document.querySelectorAll('#camera-toggle button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  state.cameraMode = btn.dataset.cam;
  controls.enabled = state.cameraMode === 'god';
  // Inset always shows whichever view ISN'T the main one — so both the
  // "why" (God's Eye) and the "what we see" (Earth Observer) angles are
  // always on screen together, whichever is currently the big view.
  insetLabelEl.textContent = state.cameraMode === 'god'
    ? "Earth Observer — the Moon as we see it"
    : "Top-down — Sun · Earth · Moon geometry";
});

document.getElementById('speed-toggle').addEventListener('click', (e) => {
  const btn = e.target.closest('button[data-speed]');
  if (!btn) return;
  document.querySelectorAll('#speed-toggle button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  state.timeWarp = Number(btn.dataset.speed);
});

const playPauseBtn = document.getElementById('play-pause');
playPauseBtn.addEventListener('click', () => {
  state.playing = !state.playing;
  playPauseBtn.classList.toggle('is-paused', !state.playing);
  playPauseBtn.textContent = state.playing ? '❚❚' : '';
});

const nowReadout = document.getElementById('now-readout');
document.getElementById('sync-now').addEventListener('click', () => {
  state.elapsedDays = realWorldElapsedDays();
  applyMoonAngleFromDays();
  updatePhaseUI();
  const { name, illum } = computePhase();
  const stamp = new Date().toLocaleString(undefined, {
    month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit',
  });
  nowReadout.textContent = `Synced to ${stamp} — ${name}, ${Math.round(illum * 100)}%`;
});

const slider = document.getElementById('cycle-slider');
let scrubbing = false;
let wasPlayingBeforeScrub = false;
slider.addEventListener('pointerdown', () => {
  scrubbing = true;
  wasPlayingBeforeScrub = state.playing;
  state.playing = false;
});
window.addEventListener('pointerup', () => {
  if (!scrubbing) return;
  scrubbing = false;
  if (wasPlayingBeforeScrub) {
    state.playing = true;
  } else {
    playPauseBtn.classList.add('is-paused');
    playPauseBtn.textContent = '';
  }
});
slider.addEventListener('input', () => {
  const frac = Number(slider.value) / Number(slider.max);
  state.elapsedDays = frac * SYNODIC_MONTH_DAYS;
  applyMoonAngleFromDays();
  updatePhaseUI();
});

/* ======================================================================
   RESIZE
   ====================================================================== */

function resizeMain() {
  const w = window.innerWidth, h = window.innerHeight;
  godCamera.aspect = w / h;
  godCamera.updateProjectionMatrix();
  earthObserverCamera.aspect = w / h;
  earthObserverCamera.updateProjectionMatrix();
  renderer.setSize(w, h);
  bloomComposer.setSize(w, h);
  finalComposer.setSize(w, h);
  renderSize.set(w, h);
}

function resizeInset() {
  const w = insetCanvas.clientWidth, h = insetCanvas.clientHeight;
  insetRenderer.setSize(w, h, false);
}

window.addEventListener('resize', () => { resizeMain(); resizeInset(); });

/* ======================================================================
   ANIMATION LOOP
   ====================================================================== */

const clock = new THREE.Clock();

function tick() {
  requestAnimationFrame(tick);
  const dt = Math.min(clock.getDelta(), 0.1);

  if (state.playing && !scrubbing) {
    advanceTime(dt * state.timeWarp);
    slider.value = Math.round((state.elapsedDays / SYNODIC_MONTH_DAYS) * Number(slider.max));
  }

  starfield.material.uniforms.uTime.value += dt;
  sunLight.position.copy(sunPivot.position);
  nightMat.uniforms.sunDirection.value.copy(sunPivot.position).normalize();

  updatePhaseUI();
  updateEarthObserverCamera();

  controls.update(); // safe to call even when disabled; lets damping settle after a drag

  const insetIsEarthObserver = state.cameraMode === 'god';
  const mainCamera = insetIsEarthObserver ? godCamera : earthObserverCamera;
  const insetCamera = insetIsEarthObserver ? earthObserverCamera : topDownCamera;

  // main view: full selective-bloom pipeline
  renderer.setViewport(0, 0, window.innerWidth, window.innerHeight);
  renderWithSelectiveBloom(mainCamera);

  // inset always shows whichever camera ISN'T currently the main one,
  // plain render (no bloom, cheap) — snapped every frame like its main-view twin
  const iw = insetCanvas.clientWidth, ih = insetCanvas.clientHeight;
  insetCamera.aspect = iw / ih;
  insetCamera.updateProjectionMatrix();
  insetRenderer.render(scene, insetCamera);
  // restore the shared camera's aspect for next frame's main-canvas use
  insetCamera.aspect = window.innerWidth / window.innerHeight;
  insetCamera.updateProjectionMatrix();
}

/* ======================================================================
   BOOT
   ====================================================================== */

applyScale(state.scaleMode);
applyMoonAngleFromDays();
slider.value = Math.round((state.elapsedDays / SYNODIC_MONTH_DAYS) * Number(slider.max));
resizeMain();
resizeInset();
tick();
