"""Procedurally generate Matthias' Laevateinn (Limbus Company) - Stage 4.

Accurate pass from the reference: a slender BLACK blade whose lower ~half and cutting
edge glow with MOLTEN orange-red, fading to a black tip; a small angular guard; and a
segmented "vertebrae" black handle. Original fan recreation, modelled from scratch.

Pieces (each = one flat/engine-material draw in PAC):
  laev_hilt.obj   -> segmented handle + guard + pommel   (dark metal)
  laev_molten.obj -> glowing lower blade section         (molten energy)
  laev_blade.obj  -> black upper blade + tip             (dark metal)
  laev_edge.obj   -> glowing cutting-edge line           (bright energy)

Grip-centred (hand grips near z=0) so it sits in the hand with Position/AngleOffset ~0.
"""

import math
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "obj")
os.makedirs(OUT_DIR, exist_ok=True)


class Mesh:
    def __init__(self, name):
        self.name = name
        self.v, self.vt, self.f = [], [], []

    def vert(self, p):
        self.v.append((float(p[0]), float(p[1]), float(p[2])))
        return len(self.v)

    def uv(self, u, w):
        self.vt.append((u, w))
        return len(self.vt)

    def face(self, pairs):
        self.f.append(pairs)

    def write(self, path):
        ntri = 0
        with open(path, "w") as fp:
            for (x, y, z) in self.v:
                fp.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
            for (u, w) in self.vt:
                fp.write(f"vt {u:.4f} {w:.4f}\n")
            for face in self.f:
                for k in range(1, len(face) - 1):
                    a, b, c = face[0], face[k], face[k + 1]
                    fp.write(f"f {a[0]}/{a[1]} {b[0]}/{b[1]} {c[0]}/{c[1]}\n")
                    ntri += 1
        print(f"  {self.name:16s} -> {len(self.v):4d} verts, {ntri:4d} tris")


# ---- blade profile (grip centred, blade points +Z) ----
GUARD_Z = 3.0
MID_Z = 26.0        # molten -> black transition
TIP_Z = 52.0
T = 0.5             # blade half-thickness

_WPTS = [(GUARD_Z, 2.7), (14.0, 2.62), (MID_Z, 2.15),
         (38.0, 1.4), (46.0, 0.72), (TIP_Z, 0.22)]


def wfun(z):
    pts = _WPTS
    if z <= pts[0][0]:
        return pts[0][1]
    if z >= pts[-1][0]:
        return pts[-1][1]
    for (z0, w0), (z1, w1) in zip(pts, pts[1:]):
        if z0 <= z <= z1:
            f = (z - z0) / (z1 - z0)
            return w0 + (w1 - w0) * f
    return pts[-1][1]


def tfun(z):
    return T * max(0.45, 1.0 - 0.4 * (z - GUARD_Z) / (TIP_Z - GUARD_Z))


def ring(mesh, z, u):
    w, t = wfun(z), tfun(z)
    return [
        (mesh.vert((-w, 0, z)), mesh.uv(u, 0.0)),     # -x cutting edge
        (mesh.vert((0, t, z)), mesh.uv(u, 0.33)),     # front ridge
        (mesh.vert((w, 0, z)), mesh.uv(u, 0.66)),     # +x spine
        (mesh.vert((0, -t, z)), mesh.uv(u, 1.0)),     # back ridge
    ]


def blade_span(mesh, z0, z1, steps, cap_bottom, tip):
    zs = [z0 + (z1 - z0) * i / steps for i in range(steps + 1)]
    rings = [ring(mesh, z, (z - GUARD_Z) / (TIP_Z - GUARD_Z)) for z in zs]
    for a, b in zip(rings, rings[1:]):
        for i in range(4):
            j = (i + 1) % 4
            mesh.face([a[i], a[j], b[j], b[i]])
    if cap_bottom:
        r = rings[0]
        mesh.face([r[0], r[1], r[2], r[3]])
    if tip:
        apex = (mesh.vert((0, 0, z1 + 1.5)), mesh.uv(1, 0.5))
        r = rings[-1]
        for i in range(4):
            mesh.face([r[i], r[(i + 1) % 4], apex])


def box(mesh, x0, x1, y0, y1, z0, z1):
    p = [mesh.vert(v) for v in [
        (x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
        (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]]
    uv = mesh.uv(0, 0)
    q = [(i, uv) for i in p]
    for a, b, c, d in [(0, 1, 2, 3), (7, 6, 5, 4), (0, 4, 5, 1),
                       (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]:
        mesh.face([q[a], q[b], q[c], q[d]])


# ---------- hilt: segmented vertebrae handle + guard + pommel ----------
hilt = Mesh("hilt")
z = -15.0
seg = 0
while z < -0.5:
    bulge = 0.95 if seg % 2 == 0 else 0.72      # alternate vertebra width
    taper = 1.0 - 0.02 * seg
    hw, hy = bulge * taper, 0.72 * taper
    box(hilt, -hw, hw, -hy, hy, z, z + 1.5)
    z += 1.85
    seg += 1
box(hilt, -1.15, 1.15, -0.95, 0.95, -16.2, -15.0)               # pommel
# small angular guard where blade meets handle
box(hilt, -2.35, 2.35, -0.95, 0.95, -0.5, GUARD_Z)
box(hilt, -2.9, -2.35, -0.7, 0.7, 0.4, GUARD_Z - 0.3)           # guard wing L
box(hilt, 2.35, 2.9, -0.7, 0.7, 0.4, GUARD_Z - 0.3)            # guard wing R
hilt.write(os.path.join(OUT_DIR, "laev_hilt.obj"))

# ---------- molten glowing lower blade ----------
molten = Mesh("molten")
blade_span(molten, GUARD_Z, MID_Z, 5, cap_bottom=True, tip=False)
molten.write(os.path.join(OUT_DIR, "laev_molten.obj"))

# ---------- black upper blade + tip ----------
blade = Mesh("blade")
blade_span(blade, MID_Z, TIP_Z, 6, cap_bottom=False, tip=True)
blade.write(os.path.join(OUT_DIR, "laev_blade.obj"))

# ---------- glowing cutting-edge line (thin strip along -x edge, full length) ----------
edge = Mesh("edge")
zs = [GUARD_Z + (48.0 - GUARD_Z) * i / 24 for i in range(25)]
top, bot = [], []
for i, z in enumerate(zs):
    w = wfun(z) + 0.05
    u = i / (len(zs) - 1)
    top.append((edge.vert((-w, 0.16, z)), edge.uv(u, 1)))
    bot.append((edge.vert((-w, -0.16, z)), edge.uv(u, 0)))
for i in range(len(zs) - 1):
    edge.face([bot[i], top[i], top[i + 1], bot[i + 1]])
edge.write(os.path.join(OUT_DIR, "laev_edge.obj"))

print("Laevateinn stage-4 pieces written to", OUT_DIR)
