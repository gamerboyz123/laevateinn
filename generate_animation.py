"""Custom attack-swing bone animation for Laevateinn (hosted JSON).

PAC custom animations are JSON of keyframed bone poses. Per bone/frame:
  MU/MF/MR translate, RU/RF/RR rotate (applied as Angle(RR, RU, RF)) in degrees.
Type "gesture" plays ONCE then stops - perfect for an attack, since it's triggered
by an animation_event("attack primary") that shows it for ~0.6s on each swing.

A quick diagonal overhead slash of the right arm + a torso twist. Amplitudes are
sizeable so the swing is clearly visible; tune with the part's Rate / BonePower.
"""

import json
import os

OUT = os.path.join(os.path.dirname(__file__), "animations")
os.makedirs(OUT, exist_ok=True)

SPINE = "ValveBiped.Bip01_Spine2"
R_ARM = "ValveBiped.Bip01_R_UpperArm"
R_FORE = "ValveBiped.Bip01_R_Forearm"
R_HAND = "ValveBiped.Bip01_R_Hand"


def bone(mu=0, mf=0, mr=0, ru=0, rf=0, rr=0):
    return {"MU": mu, "MF": mf, "MR": mr, "RU": ru, "RF": rf, "RR": rr}


def frame(rate, bones):
    return {"FrameRate": rate, "BoneInfo": bones}


RATE = 7.0  # fast: whole 4-frame slash in ~0.55s

anim = {
    "Type": "gesture",
    "Interpolation": "cosine",
    "FrameData": [
        # windup - raise the blade up and back
        frame(RATE, {
            SPINE: bone(ru=-12, rr=-6),
            R_ARM: bone(ru=-22, rf=-38, rr=-24),
            R_FORE: bone(rf=-32, rr=-10),
            R_HAND: bone(ru=-10),
        }),
        # strike - swing down and across
        frame(RATE, {
            SPINE: bone(ru=16, rr=8),
            R_ARM: bone(ru=26, rf=46, rr=30),
            R_FORE: bone(rf=24, rr=12),
            R_HAND: bone(ru=14),
        }),
        # follow-through - continue the arc low
        frame(RATE, {
            SPINE: bone(ru=20, rr=10),
            R_ARM: bone(ru=32, rf=56, rr=40),
            R_FORE: bone(rf=36),
            R_HAND: bone(ru=18),
        }),
        # recover back toward the hold
        frame(RATE, {
            SPINE: bone(ru=4),
            R_ARM: bone(ru=6, rf=10, rr=6),
            R_FORE: bone(rf=6),
            R_HAND: bone(),
        }),
    ],
}

path = os.path.join(OUT, "swing.json")
with open(path, "w") as fp:
    json.dump(anim, fp, separators=(",", ":"))
print("wrote", path, os.path.getsize(path), "bytes")
