# Laevateinn (Stage 4) — PAC3 assets

Original fan recreation of Matthias' **Laevateinn** (Limbus Company), Stage 4 energy
blade, for Garry's Mod **PAC3**. Modelled from scratch (no ripped assets).

## Contents
- `obj/` — the blade pieces (hilt, red-hot base, amber blade, glowing edge sheet) as
  URL-streamable OBJ models.
- `laevateinn.txt` — the PAC3 outfit. Load it in the PAC3 editor via **Load → URL**:
  `https://raw.githubusercontent.com/gamerboyz123/laevateinn/main/laevateinn.txt`

## How it works
Each piece is a legacy `model` part streaming an OBJ from this repo, tinted with a flat
**fullbright** colour through a built-in engine material (the target server blocks PAC's
URL-texture system, so all "glow" is faked with bold colours + an oversized bright edge
sheet). The `melee2` holdtype gives a two-handed blade stance and a swing on attack.

## Regenerating
```
python3 generate_blade.py   # writes obj/*.obj
python3 generate_pac.py     # writes laevateinn.txt
python3 render_preview.py   # optional: preview.png
```

Show the blade by equipping the configured weapon (`csgo_bayonet_bluesteel`); change
`WEAPON_CLASS` in `generate_pac.py` to use a different slot.
