# Sun · Earth · Moon — Phase Visualization

A real-time, physically-driven Moon phase simulator. Phases are never faked
with swapped textures — they emerge purely from a `DirectionalLight` shining
across a correctly-tilted, correctly-orbiting Earth/Moon system, exactly as
they do in reality.

## Running it

Textures are loaded via `<script type="module">`, so this **must** be served
over HTTP — opening `index.html` directly (`file://`) will fail with a CORS
error in most browsers. From this folder:

```
python3 -m http.server 8000
# or: npx serve .
```

Then open `http://localhost:8000`.

## What's implemented

- **Sun** — unlit textured sphere (it's its own light source visually); a
  separate `DirectionalLight` positioned at the Sun and aimed at Earth
  produces genuinely parallel rays, which is what actually draws the
  terminator line on both Earth and the Moon.
- **Earth** — `orbitPivot → tiltGroup (23.5°, North Pole toward the Sun —
  the classic solstice orientation, chosen for maximum visible lighting
  contrast) → spinMesh`, three nested `Group`s so axial tilt and the ~24 h
  day/night spin never interfere with each other through combined Euler
  rotations. City lights on the unlit hemisphere are a separate, fully
  self-contained overlay mesh (additive blending, no depth write) — its own
  tiny shader compares surface normal against a world-space Sun-direction
  uniform we set every frame, rather than reaching into
  `MeshStandardMaterial`'s internal shader chunks, which is fragile across
  three.js versions and hard to verify without a browser to test against.
- **Moon** — `orbitPivot (5.1° inclined) → angleGroup (θ) → mesh`. Tidal
  locking isn't simulated with extra code — the Moon mesh is a rigid child
  sitting at a fixed local offset with a fixed local rotation, so as the
  parent sweeps through θ over the month, the same hemisphere automatically
  stays pointed at Earth.
- **Orbital motion** — θ is driven directly by real elapsed time divided by
  the synodic month (29.530588853 days), i.e. true angular motion, not an
  eased/lerped animation.
- **Phase detection** — computed every frame from the actual Sun→Earth and
  Moon→Earth vectors (an `acos` of their dot product, signed via the orbit's
  normal), not inferred from a timer. Drives the phase name, illuminated %,
  and the small dial icon in the header.
- **Two scale modes**:
  - *Visual* — sizes and distances exaggerated independently for legibility.
  - *True* — one uniform km-per-unit factor (1 unit = 1000 km) applied to
    everything, so the Earth–Moon distance, the AU, and all three body radii
    keep their real proportions. Nothing is a hardcoded absolute geometry
    radius — every mesh keeps a unit-sphere geometry and is scaled via
    `mesh.scale.setScalar(...)` from the active mode's numbers, which is what
    keeps True mode from blowing up.
- **Two camera modes** — "God's Eye" (free `OrbitControls`, shows *why*
  phases happen) and "Earth Observer" (camera snapped every frame — no
  lerp/damping — to the sub-lunar point on Earth's surface, looking at the
  Moon: shows the phase *as we actually see it*). Whichever one is the main
  view, the small inset always shows the *other* one. When Earth Observer is
  main, the inset is a **dedicated, fixed, always-straight-down camera** —
  deliberately not the interactive God's-Eye camera, which the user could
  have dragged to any oblique angle. A stable top-down diagram is what
  actually helps at a glance.
- **Current phase / real-time sync** — "Sync to tonight's real Moon"
  computes today's actual Sun–Earth–Moon phase angle from a known reference
  New Moon (2000-01-06 18:14 UTC) and the real synodic period — same math
  the sim runs internally, just anchored to `Date.now()`. Pair it with the
  "Real-time" speed preset (1 simulated second per real second) and the
  scene stays perpetually in sync with the actual sky. The sim also boots
  already synced to tonight's real phase.
- **Selective bloom** — the classic two-composite technique: the whole scene
  is rendered with every non-Sun material swapped to solid black into a
  bloom buffer, blurred, then additively composited over the normal render.
  Only the Sun blooms; a high `UnrealBloomPass` threshold is extra insurance.
- **Starfield** — a custom `ShaderMaterial` on `THREE.Points` (not
  `PointsMaterial`) with a soft radial falloff and a per-star sine-wave
  twinkle, so it's not a flat static skybox.

## Controls

- Drag / scroll to orbit in God's Eye mode.
- **Scale**: Visual ↔ True.
- **Camera**: God's Eye ↔ Earth Observer.
- **Time**: play/pause, four warp-speed presets, and a slider that scrubs
  directly through one full 29.53-day synodic month (dragging it pauses
  playback; releasing resumes it if it was already playing).

## Textures

Fully local and offline — `images/` ships with `sun.jpg`, `earth_daymap.jpg`,
`earth_nightmap.jpg`, and `moon.jpg`, downsampled from the source 8K maps to
2048px on the long edge for the web. No CDN, no network request, no CORS
concerns (as long as you're serving over HTTP rather than `file://`).

## Out of scope (by design)

No other planets, no asteroid belt, no full solar system — just the Sun,
Earth, Moon, and the phase mechanic, done correctly.
