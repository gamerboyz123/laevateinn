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

# Music that plays while the blade is out. Drop your track at audio/theme.mp3 in the
# repo (any direct .mp3/.wav URL works). Loops, gated by the same weapon as the blade.
MUSIC_URL = f"{HOST_BASE}/audio/theme.mp3"
MUSIC_VOLUME = 0.2

# Bump when the OBJ geometry changes so GitHub's CDN / PAC can't serve stale meshes.
ASSET_VERSION = 5

# Grip-centred model. ANGLE_OFFSET is (pitch, yaw, roll). Screenshot at pitch 180
# showed the blade pointing DOWN through the legs, so 0 points it UP/away (correct).
SIZE = 0.95
POSITION = (0.0, 0.0, 0.0)
ANGLE_OFFSET = (0.0, 0.0, 0.0)

# --- Materials -----------------------------------------------------------------
# ENGINE build: built-in HL2 materials (load reliably - the wood pole proves HL2
#   content is mounted). Animated Combine energy texture = glowing molten look.
# CUSTOM build: hosted PNGs via PAC's URL-texture system. This is the TEST build -
#   it only shows if the server allows pac_enable_urltex; otherwise it goes magenta.
ENERGY = "models/props_combine/portalball001_sheet"   # animated glowing energy
METAL = "models/props_combine/metal_combinebridge001"  # dark industrial metal

# key, obj, engine_mat, url_png, color_engine(0-255), fullbright, doubleface, draw
PIECES = [
    ("hilt",   "laev_hilt.obj",   METAL,  "tex_metal.png",  (60, 62, 70),    False, False, 0),
    ("blade",  "laev_blade.obj",  METAL,  "tex_black.png",  (24, 25, 30),    False, False, 1),
    ("molten", "laev_molten.obj", ENERGY, "tex_molten.png", (255, 96, 24),   True,  False, 2),
    ("edge",   "laev_edge.obj",   ENERGY, "tex_edge.png",   (255, 216, 120), True,  True,  3),
]
NAMES = {
    "hilt": "vertebrae hilt",
    "blade": "black blade",
    "molten": "molten glow",
    "edge": "edge glow",
}

UIDS = {
    "group": "3a91c47e0d6b52f8194a7ce0b25d83f6710c9e4482ad35bf01e7c6d29a4b1f02",
    "event": "7c2d918a4e6f03b5182c9de74a6f10b3821dab5593be46cf12f8d73ea5c6e934",
    "hilt":  "b14e77a2c96d0358f1275a8be4c39d0762a1edb43268fa7b25f81c6e48331157",
    "blade": "e5fa128b6c4d73091825b8df3c6e94a7821dab5593be46cf12f8d73ea5c69df1",
    "molten": "d29f118b6c4d73091825b8df3c6e94a7821dab5593be46cf12f8d73ea5c69a48",
    "edge":  "f6ab239c7d5e84102936c9ef4d7fa5b8932ebc6604cf57da23f9e84fb6d7ae05",
    "anim":  "a70bc34ad8e6f5192047daf0b36e94b7043cd5e593ae46bf02e7d63ea5c7bf16",
    "sound": "b81cd45be9f70620158cdb01c47f05c8154de6f6a4bf57c013f8e74fb6d8bf27",
}
# Distinct UIDs for the custom-texture build so both can coexist without clashing.
UIDS_CUSTOM = {k: ("c" + v[1:]) for k, v in UIDS.items()}
# ===============================================================


def vec(t):
    return f"Vector({t[0]}, {t[1]}, {t[2]})"


def ang(t):
    return f"Angle({t[0]}, {t[1]}, {t[2]})"


def b(x):
    return "true" if x else "false"


def model_part(key, obj, material, color, fullbright, doubleface, draw, indent, uids):
    t = "\t" * indent
    model_url = f"{HOST_BASE}/obj/{obj}?v={ASSET_VERSION}"
    return f"""{t}["children"] = {{
{t}}},
{t}["self"] = {{
{t}\t["Skin"] = 0,
{t}\t["UniqueID"] = "{uids[key]}",
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


def sound_part(indent, uids):
    t = "\t" * indent
    return f"""{t}["children"] = {{
{t}}},
{t}["self"] = {{
{t}\t["Path"] = "{MUSIC_URL}",
{t}\t["UniqueID"] = "{uids['sound']}",
{t}\t["Pitch"] = 1,
{t}\t["Name"] = "laevateinn theme",
{t}\t["PlayOnFootstep"] = false,
{t}\t["Radius"] = 600,
{t}\t["DrawOrder"] = 0,
{t}\t["PlayCount"] = 0,
{t}\t["Bone"] = "head",
{t}\t["StopOnHide"] = true,
{t}\t["PauseOnHide"] = false,
{t}\t["Doppler"] = false,
{t}\t["Volume"] = {MUSIC_VOLUME},
{t}\t["Position"] = Vector(0, 0, 0),
{t}\t["Overlapping"] = false,
{t}\t["EditorExpand"] = false,
{t}\t["Hide"] = false,
{t}\t["PositionOffset"] = Vector(0, 0, 0),
{t}\t["ClassName"] = "sound2",
{t}\t["Angles"] = Angle(0, 0, 0),
{t}}},"""


def anim_part(indent, uids):
    t = "\t" * indent
    return f"""{t}["children"] = {{
{t}}},
{t}["self"] = {{
{t}\t["UniqueID"] = "{uids['anim']}",
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


def build(use_url):
    uids = UIDS_CUSTOM if use_url else UIDS
    group_name = "laevateinn (custom-tex TEST)" if use_url else "laevateinn stage 4"
    children = []
    for idx, (key, obj, emat, png, ecolor, fb, df, draw) in enumerate(PIECES, 1):
        if use_url:
            material = f"{HOST_BASE}/textures/{png}?v={ASSET_VERSION}"
            color = (255, 255, 255)          # let the PNG provide the colour
        else:
            material, color = emat, ecolor
        body = model_part(key, obj, material, color, fb, df, draw, 5, uids)
        children.append(f"\t\t\t\t[{idx}] = {{\n{body}\n\t\t\t\t}},")
    children.append(f"\t\t\t\t[{len(PIECES) + 1}] = {{\n{anim_part(5, uids)}\n\t\t\t\t}},")
    children.append(f"\t\t\t\t[{len(PIECES) + 2}] = {{\n{sound_part(5, uids)}\n\t\t\t\t}},")
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
\t\t\t\t["UniqueID"] = "{uids['event']}",
\t\t\t\t["ZeroEyePitch"] = false,
\t\t\t}},
\t\t}},
\t}},
\t["self"] = {{
\t\t["DrawOrder"] = 0,
\t\t["UniqueID"] = "{uids['group']}",
\t\t["Hide"] = false,
\t\t["EditorExpand"] = true,
\t\t["OwnerName"] = "self",
\t\t["Name"] = "{group_name}",
\t\t["Duplicate"] = false,
\t\t["ClassName"] = "group",
\t}},
}},
"""


if __name__ == "__main__":
    here = os.path.dirname(__file__)
    with open(os.path.join(here, "laevateinn.txt"), "w") as fp:
        fp.write(build(use_url=False))
    with open(os.path.join(here, "laevateinn_custom.txt"), "w") as fp:
        fp.write(build(use_url=True))
    print("wrote laevateinn.txt (engine materials) + laevateinn_custom.txt (URL PNGs)")
