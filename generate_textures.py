"""Custom PNG textures for the Laevateinn 'custom-tex TEST' build.

These are only used by laevateinn_custom.txt, which references them as PAC URL
materials. They only render if the server allows pac_enable_urltex; otherwise the
pieces show magenta (which is the answer to "can custom textures work here?").

  tex_molten.png : molten lava (hot yellow cracks over deep red-orange)
  tex_black.png  : near-black blade steel with faint scratches
  tex_metal.png  : dark gunmetal for the vertebrae hilt
  tex_edge.png   : bright white-hot energy streaks for the cutting edge
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUT = os.path.join(os.path.dirname(__file__), "textures")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(11)


def noise(w, h, base, amp):
    n = rng.normal(0, amp, (h, w, 1))
    return np.clip(np.array(base, float)[None, None, :] + n, 0, 255).astype(np.uint8)


# ---- molten lava (256, tileable-ish) ----
S = 256
lava = Image.fromarray(noise(S, S, (150, 26, 8), 12), "RGB")
d = ImageDraw.Draw(lava)
for _ in range(120):                       # glowing cracks
    x, y = int(rng.integers(0, S)), int(rng.integers(0, S))
    pts = [(x, y)]
    for _ in range(8):
        x += int(rng.integers(-12, 12)); y += int(rng.integers(-12, 12))
        pts.append((x % S, y % S))
    hot = (255, 180, 40) if rng.random() < 0.6 else (255, 120, 20)
    for a, bb in zip(pts, pts[1:]):
        if abs(a[0] - bb[0]) < S * .5 and abs(a[1] - bb[1]) < S * .5:
            d.line([a, bb], fill=hot, width=int(rng.integers(1, 3)))
for _ in range(200):                       # bright specks
    x, y = int(rng.integers(0, S)), int(rng.integers(0, S))
    d.ellipse([x, y, x + 2, y + 2], fill=(255, 232, 130))
lava = lava.filter(ImageFilter.GaussianBlur(0.6))
lava.save(os.path.join(OUT, "tex_molten.png"))

# ---- near-black blade steel ----
blk = Image.fromarray(noise(S, S, (22, 23, 27), 5), "RGB")
db = ImageDraw.Draw(blk)
for _ in range(60):
    x = int(rng.integers(0, S))
    db.line([x, 0, x + int(rng.integers(-6, 6)), S], fill=(38, 40, 46), width=1)
blk = blk.filter(ImageFilter.GaussianBlur(0.4))
blk.save(os.path.join(OUT, "tex_black.png"))

# ---- dark gunmetal hilt ----
met = Image.fromarray(noise(S, S, (58, 60, 68), 8), "RGB")
dm = ImageDraw.Draw(met)
for _ in range(90):
    x, y = int(rng.integers(0, S)), int(rng.integers(0, S))
    dm.line([x, y, x + int(rng.integers(-9, 9)), y + int(rng.integers(-9, 9))],
            fill=(88, 92, 102), width=1)
met = met.filter(ImageFilter.GaussianBlur(0.4))
met.save(os.path.join(OUT, "tex_metal.png"))

# ---- white-hot edge energy ----
edge = Image.fromarray(noise(128, 128, (255, 180, 70), 10), "RGB")
de = ImageDraw.Draw(edge)
for _ in range(60):
    x, y = int(rng.integers(0, 128)), int(rng.integers(0, 128))
    de.line([x, y, x + int(rng.integers(-14, 14)), y], fill=(255, 246, 200), width=1)
edge = edge.filter(ImageFilter.GaussianBlur(0.3))
edge.save(os.path.join(OUT, "tex_edge.png"))

for f in ("tex_molten.png", "tex_black.png", "tex_metal.png", "tex_edge.png"):
    p = os.path.join(OUT, f)
    print(f"  {f:16s} {Image.open(p).size}  {os.path.getsize(p)//1024} KB")
print("Done.")
