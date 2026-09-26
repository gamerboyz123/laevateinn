"""Generate the PAC3 outfit .txt for Matthias' Laevateinn (Stage 4 energy blade).

Tree: group -> weapon_class event -> {4 OBJ pieces + melee2 hold animation}. Each
piece is a legacy "model" part streaming an OBJ from GitHub, tinted with a flat
FULLBRIGHT colour via a built-in engine material (no URL textures - the server
blocks them). The melee2 holdtype gives a two-handed blade stance AND a native
swing on attack. Edit CONFIG, run, load the .txt in PAC3.
"""

import os

# ============================ CONFIG ============================
HOST_BASE = "https://raw.githubusercontent.com/gamerboyz123/laevateinn/main"

# Equip this weapon to show the blade (same knife slot as the staff).
WEAPON_CLASS = "csgo_bayonet_bluesteel"

# melee2 = two-handed blade hold in front + a swing on primary attack.
HOLDTYPE = "melee2"

# Bump when the OBJ geometry changes so GitHub's CDN / PAC can't serve stale meshes.
ASSET_VERSION = 2

# Grip-centred model, so keep these near zero and fine-tune in the editor.
SIZE = 0.95
POSITION = (0.0, 0.0, 0.0)
ANGLE_OFFSET = (0.0, 0.0, 0.0)

# --- Engine materials (NOT URL textures - those are blocked on the server) --------
# These are built-in HL2 materials, which load fine here (the wood pole proves HL2
# content is mounted). The Combine energy-ball / portal-storm textures are ANIMATED
# glowing plasma - tinted, they make the blade look like a living energy weapon.
ENERGY = "models/props_combine/portalball001_sheet"  # animated glowing energy sheet
METAL = "models/props_combine/metal_combinebridge001"  # dark industrial metal
# If any piece shows magenta, that material isn't mounted -> swap it here and re-run.

# key, obj, material, color(0-255), fullbright, doubleface, drawpriority
PIECES = [
    ("hilt",  "laev_hilt.obj",  METAL,  (54, 55, 62),    False, False, 0),
    ("base",  "laev_base.obj",  ENERGY, (255, 60, 12),   True,  False, 1),
    ("blade", "laev_blade.obj", ENERGY, (255, 138, 30),  True,  False, 2),
    ("glow",  "laev_glow.obj",  ENERGY, (255, 236, 150), True,  True,  3),
]
NAMES = {
    "hilt": "hilt + guard",
    "base": "red-hot base",
    "blade": "amber blade",
    "glow": "glowing edge",
}

UIDS = {
    "group": "3a91c47e0d6b52f8194a7ce0b25d83f6710c9e4482ad35bf01e7c6d29a4b1f02",
    "event": "7c2d918a4e6f03b5182c9de74a6f10b3821dab5593be46cf12f8d73ea5c6e934",
    "hilt":  "b14e77a2c96d0358f1275a8be4c39d0762a1edb43268fa7b25f81c6e48331157",
    "base":  "d29f118b6c4d73091825b8df3c6e94a7821dab5593be46cf12f8d73ea5c69a48",
    "blade": "e5fa128b6c4d73091825b8df3c6e94a7821dab5593be46cf12f8d73ea5c69df1",
    "glow":  "f6ab239c7d5e84102936c9ef4d7fa5b8932ebc6604cf57da23f9e84fb6d7ae05",
    "anim":  "a70bc34ad8e6f5192047daf0b36e94b7043cd5e593ae46bf02e7d63ea5c7bf16",
}
# ===============================================================


def vec(t):
    return f"Vector({t[0]}, {t[1]}, {t[2]})"


def ang(t):
    return f"Angle({t[0]}, {t[1]}, {t[2]})"


def b(x):
    return "true" if x else "false"


def model_part(key, obj, material, color, fullbright, doubleface, draw, indent):
    t = "\t" * indent
    model_url = f"{HOST_BASE}/obj/{obj}?v={ASSET_VERSION}"
    return f"""{t}["children"] = {{
{t}}},
{t}["self"] = {{
{t}\t["Skin"] = 0,
{t}\t["UniqueID"] = "{UIDS[key]}",
{t}\t["Fullbright"] = {b(fullbright)},
{t}\t["Name"] = "{NAMES[key]}",
{t}\t["PositionOffset"] = Vector(0, 0, 0),
{t}\t["DrawOrder"] = {draw},
{t}\t["Alpha"] = 1,
{t}\t["Material"] = "{material}",
{t}\t["DoubleFace"] = {b(doubleface)},
{t}\t["Bone"] = "right hand",
{t}\t["Angles"] = Angle(0, 0, 0),
{t}\t["AngleOffset"] = {ang(ANGLE_OFFSET)},
{t}\t["BoneMerge"] = false,
{t}\t["Color"] = {vec(color)},
{t}\t["Position"] = {vec(POSITION)},
{t}\t["ClassName"] = "model",
{t}\t["Brightness"] = 1,
{t}\t["Hide"] = false,
{t}\t["Scale"] = Vector(1, 1, 1),
{t}\t["EditorExpand"] = false,
{t}\t["Size"] = {SIZE},
{t}\t["Translucent"] = false,
{t}\t["Model"] = "{model_url}",
{t}}},"""


def anim_part(indent):
    t = "\t" * indent
    return f"""{t}["children"] = {{
{t}}},
{t}["self"] = {{
{t}\t["UniqueID"] = "{UIDS['anim']}",
{t}\t["Name"] = "greatsword hold",
{t}\t["ClassName"] = "animation",
{t}\t["WeaponHoldType"] = "{HOLDTYPE}",
{t}\t["SequenceName"] = "",
{t}\t["Loop"] = true,
{t}\t["PingPongLoop"] = false,
{t}\t["Rate"] = 1,
{t}\t["Offset"] = 0,
{t}\t["Min"] = 0,
{t}\t["Max"] = 1,
{t}\t["OwnerCycle"] = false,
{t}\t["InvertFrames"] = false,
{t}\t["ResetOnHide"] = true,
{t}\t["Hide"] = false,
{t}\t["EditorExpand"] = false,
{t}}},"""


def build():
    children = []
    for idx, (key, obj, mat, color, fb, df, draw) in enumerate(PIECES, 1):
        body = model_part(key, obj, mat, color, fb, df, draw, 5)
        children.append(f"\t\t\t\t[{idx}] = {{\n{body}\n\t\t\t\t}},")
    children.append(f"\t\t\t\t[{len(PIECES) + 1}] = {{\n{anim_part(5)}\n\t\t\t\t}},")
    kids = "\n".join(children)
    return f"""[1] = {{
\t["children"] = {{
\t\t[1] = {{
\t\t\t["children"] = {{
{kids}
\t\t\t}},
\t\t\t["self"] = {{
\t\t\t\t["AffectChildrenOnly"] = false,
\t\t\t\t["DrawOrder"] = 0,
\t\t\t\t["Name"] = "while blade is equipped",
\t\t\t\t["Event"] = "weapon_class",
\t\t\t\t["Hide"] = false,
\t\t\t\t["RootOwner"] = true,
\t\t\t\t["EditorExpand"] = true,
\t\t\t\t["ClassName"] = "event",
\t\t\t\t["Arguments"] = "{WEAPON_CLASS}",
\t\t\t\t["Invert"] = true,
\t\t\t\t["Operator"] = "find simple",
\t\t\t\t["UniqueID"] = "{UIDS['event']}",
\t\t\t\t["ZeroEyePitch"] = false,
\t\t\t}},
\t\t}},
\t}},
\t["self"] = {{
\t\t["DrawOrder"] = 0,
\t\t["UniqueID"] = "{UIDS['group']}",
\t\t["Hide"] = false,
\t\t["EditorExpand"] = true,
\t\t["OwnerName"] = "self",
\t\t["Name"] = "laevateinn stage 4",
\t\t["Duplicate"] = false,
\t\t["ClassName"] = "group",
\t}},
}},
"""


if __name__ == "__main__":
    path = os.path.join(os.path.dirname(__file__), "laevateinn.txt")
    with open(path, "w") as fp:
        fp.write(build())
    print("wrote", path)
