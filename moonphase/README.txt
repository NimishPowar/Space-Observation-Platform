This folder is intentionally empty by default.

script.js loads sun.jpg, earth_daymap.jpg, and moon.jpg from a CORS-enabled
CDN (real NASA-sourced imagery, CC BY 4.0 via solarsystemscope.com) so the
app works immediately over local HTTP without you needing to source files.

To run fully offline, download 2k-resolution versions of those three images
into this folder using the exact filenames above, then edit the loadTex(...)
calls near the top of script.js to point at "images/<name>.jpg" instead of
the CDN URL.
