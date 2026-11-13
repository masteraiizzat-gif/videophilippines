"""Temporary music bed (tropical pop, 112 BPM, G major), built to the edit.

Placeholder until a licensed track is supplied. The bar grid is anchored so a
bar line lands on the "2027" drop (10.26 s). The bed is ducked under the voice
(sidechain from assets/voice.wav) and opens up on the end card.

Run from the project root after build_voice.py:  python3 edit/build_music.py
"""
import subprocess
import numpy as np

SR = 48000
BPM = 112
BEAT = 60 / BPM
BAR = 4 * BEAT
DROP = 10.26          # "2027" lands here
END_CARD = 20.36      # voice ends, end card hits
LENGTH = 24.2
T0 = DROP - 5 * BAR   # bar grid origin (negative is fine)
rng = np.random.default_rng(7)
N = int(LENGTH * SR)
mix = {k: np.zeros(N) for k in ("kick", "clap", "shaker", "bass", "uke", "pad", "fx")}


def put(track, t, sig, gain=1.0):
    i = int(round(t * SR))
    if i >= N or i + len(sig) <= 0:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: N - i]
    mix[track][i : i + len(sig)] += sig * gain


def env(n, a=0.005, r=None):
    e = np.ones(n)
    na = max(1, int(a * SR))
    e[:na] = np.linspace(0, 1, na)
    if r:
        e *= np.exp(-np.arange(n) / (r * SR))
    return e


def kick():
    n = int(0.35 * SR)
    t = np.arange(n) / SR
    f = 45 + 85 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.12)


def clap():
    n = int(0.25 * SR)
    x = rng.standard_normal(n)
    x = np.convolve(x, [1, 0, -1], "same")  # crude band-pass
    e = np.zeros(n)
    for d in (0, 0.011, 0.022):
        k = int(d * SR)
        e[k:] += np.exp(-np.arange(n - k) / (0.03 * SR))
    return x * e * 0.5


def shaker():
    n = int(0.07 * SR)
    x = np.diff(rng.standard_normal(n + 1))
    return x * env(n, 0.004, 0.018) * 0.25


def midi(m):
    return 440 * 2 ** ((m - 69) / 12)


def bass(m, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = midi(m)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)
    return x * env(n, 0.004, dur * 0.7) * 0.6


def pluck(m, dur=0.9, bright=0.5):
    """Karplus-Strong string: reads as a ukulele / nylon guitar."""
    p = int(SR / midi(m))
    n = int(dur * SR)
    buf = rng.uniform(-1, 1, p)
    blocks = []
    for _ in range(n // p + 1):
        blocks.append(buf)
        buf = 0.997 * (bright * buf + (1 - bright) * np.roll(buf, -1))
    return np.concatenate(blocks)[:n] * env(n, 0.002)


def pad(notes, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * midi(m) * t + rng.uniform(0, 6)) for m in notes)
    x += 0.25 * sum(np.sin(2 * np.pi * midi(m) * 1.003 * t) for m in notes)
    a = np.minimum(1, t / 0.3) * np.minimum(1, (dur - t) / 0.3)
    return x * a / len(notes) * 0.35


# G - D - Em - C
CHORDS = [
    (43, [67, 71, 74, 79]),
    (38, [66, 69, 74, 78]),
    (40, [67, 71, 76, 79]),
    (36, [64, 67, 72, 76]),
]

bar_idx = 0
t = T0
while t < LENGTH:
    root, notes = CHORDS[bar_idx % 4]
    build = DROP - 2 * BAR <= t < DROP          # two bars of lift before the drop
    big = t >= DROP - 1e-6
    for b in range(4):
        bt = t + b * BEAT
        # kick: four on the floor after the drop, half-time before
        if big or b in (0, 2):
            put("kick", bt, kick(), 0.9)
        if big and b in (1, 3):
            put("clap", bt, clap(), 0.8)
        # shaker on 8ths (16ths in the lift), with swing
        steps = 4 if build else 2
        for s in range(steps):
            sw = 0.04 * BEAT if s % 2 else 0
            put("shaker", bt + s * BEAT / steps + sw, shaker(), 0.9 if s % 2 else 0.6)
        # bass: root on 1, octave pop on the and-of-2
        if b == 0:
            put("bass", bt, bass(root, BEAT * 1.4))
        if b == 1:
            put("bass", bt + BEAT / 2, bass(root + 12, BEAT * 0.4), 0.7)
        if b == 2:
            put("bass", bt, bass(root, BEAT * 0.9), 0.9)
        # island upstrokes on the off-beats
        for k, m in enumerate(notes):
            put("uke", bt + BEAT / 2 + k * 0.012, pluck(m, 0.45, 0.6), 0.22)
    put("pad", t, pad(notes, BAR + 0.3), 0.8 if big else 0.6)
    t += BAR
    bar_idx += 1

# snare-ish roll into the drop
for i in range(16):
    tt = DROP - BAR + i * BAR / 16
    put("clap", tt, clap(), 0.15 + 0.5 * i / 16)

# final chord ring on the end card
put("uke", END_CARD + 0.04, sum(pluck(m, 3.5, 0.55) for m in [55, 59, 62, 67, 71]), 0.3)
put("pad", END_CARD, pad([55, 62, 67, 71, 74], 3.8), 1.0)

# --- mix ------------------------------------------------------------------
gains = dict(kick=0.9, clap=0.45, shaker=0.5, bass=0.75, uke=0.9, pad=0.6, fx=1)
music = sum(mix[k] * g for k, g in gains.items())

# sidechain duck under the voice: -11 dB while he talks, open on the end card
voice = np.frombuffer(
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", "assets/voice.wav", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        capture_output=True, check=True,
    ).stdout,
    np.float32,
)
v = np.zeros(N)
v[: min(N, len(voice))] = np.abs(voice[:N])
win = int(0.12 * SR)
venv = np.convolve(v, np.ones(win) / win, "same")
talking = (venv > 0.01).astype(float)
smooth = int(0.25 * SR)
talking = np.convolve(talking, np.ones(smooth) / smooth, "same")
duck = 1 - talking * (1 - 10 ** (-11 / 20))
t = np.arange(N) / SR
duck = np.where(t >= END_CARD, 1.0, duck)
music *= duck

# fade out the tail
fo = int(1.2 * SR)
music[-fo:] *= np.linspace(1, 0, fo)
music /= np.max(np.abs(music)) + 1e-9
music *= 0.89

pcm = (np.clip(music, -1, 1) * 32767).astype(np.int16)
subprocess.run(
    ["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "1", "-i", "-",
     "-af", "loudnorm=I=-20:TP=-2", "-ar", str(SR), "assets/music.wav"],
    input=pcm.tobytes(), check=True,
)
print("wrote assets/music.wav")
