# audio

Put the Laevateinn track here named **`theme.mp3`** (a direct `.mp3` or `.wav`).

The PAC outfit (`laevateinn.txt`) already references:
`https://raw.githubusercontent.com/gamerboyz123/laevateinn/main/audio/theme.mp3`

Once `theme.mp3` exists in this folder, reload the outfit URL in PAC and it plays
(looping, volume 0.2) while the blade is equipped. To change the file name/volume,
edit `MUSIC_URL` / `MUSIC_VOLUME` in `generate_pac.py` and re-run it.
