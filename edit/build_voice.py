"""Cut the speech track from edit/cuts.json and clean it up.

Writes assets/voice.wav (the voice on the edited timeline) and prints each
segment's start on the edited timeline, for the <video> clips in index.html.

Run from the project root:  python3 edit/build_voice.py
"""
import json
import subprocess

cuts = json.load(open("edit/cuts.json"))
segs = cuts["segments"]
src = cuts["source"]
FADE = 0.012  # short fades on every cut so no edge clicks

parts, labels, t = [], [], 0.0
for i, s in enumerate(segs):
    d = s["out"] - s["in"]
    parts.append(
        f"[0:a]atrim={s['in']}:{s['out']},asetpts=PTS-STARTPTS,"
        f"afade=t=in:d={FADE},afade=t=out:st={d - FADE:.3f}:d={FADE}[a{i}]"
    )
    labels.append(f"[a{i}]")
    print(f"{s['id']}  start={t:6.2f}  dur={d:5.2f}  media-start={s['in']:6.2f}  {s['text']}")
    t += d
print(f"total {t:.2f}s")

chain = (
    ";".join(parts)
    + ";"
    + "".join(labels)
    + f"concat=n={len(segs)}:v=0:a=1,"
    # clean phone audio: rumble cut, gentle denoise, presence, glue, loudness
    + "highpass=f=85,afftdn=nf=-28,"
    + "equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=250:t=q:w=1:g=-2,"
    + "acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=2,"
    + "loudnorm=I=-16:TP=-1.5:LRA=7,aresample=48000[out]"
)
subprocess.run(
    ["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", chain,
     "-map", "[out]", "-ac", "1", "assets/voice.wav"],
    check=True,
)
print("wrote assets/voice.wav")
