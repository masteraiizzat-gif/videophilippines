"""One-shot generator for index.html from edit/cuts.json.

index.html is the source of truth after this runs (Studio edits it); re-run only
when the cut list changes, and re-apply any hand edits.
"""
import json

cuts = json.load(open("edit/cuts.json"))["segments"]
END_SPEECH = sum(s["out"] - s["in"] for s in cuts)
DURATION = 23.6
ORIGIN = "31% 37%"  # his face in the 1080x1920 frame

videos, zooms, t = [], [], 0.0
for i, s in enumerate(cuts):
    d = round(s["out"] - s["in"], 3)
    videos.append(
        f'        <video id="v-{s["id"]}" class="clip" src="assets/raw.mp4" muted playsinline\n'
        f'          data-start="{t:.2f}" data-duration="{d:.2f}" data-media-start="{s["in"]:.2f}" data-track-index="0"></video>'
    )
    zooms.append((round(t, 2), s["zoom"], s["id"]))
    t += d

# (time, file, volume, id) — each placed so its peak lands on the picture
SFX = [
    (0.00, "impact-bass-1", 0.16, "sfx-hook-hit"),
    (0.81, "whoosh", 0.45, "sfx-hook-whoosh"),
    (2.49, "whoosh-high", 0.40, "sfx-plate"),
    (4.36, "pop", 0.60, "sfx-chip"),
    (5.12, "ping", 0.55, "sfx-flag"),
    (6.79, "riser-soft", 0.14, "sfx-riser"),
    (7.71, "whoosh-low", 0.50, "sfx-broll-in"),
    (8.32, "sparkle", 0.22, "sfx-badge"),
    (10.19, "impact-bass-1", 0.2, "sfx-2027"),
    (11.98, "whoosh", 0.40, "sfx-pan"),
    (12.54, "pop", 0.55, "sfx-pin"),
    (12.63, "ping", 0.45, "sfx-date"),
    (13.89, "whoosh-high", 0.40, "sfx-broll-out"),
    (15.52, "sparkle", 0.24, "sfx-unforget"),
    (16.27, "whoosh-low", 0.40, "sfx-experience"),
    (16.93, "whoosh", 0.45, "sfx-callback"),
    (17.86, "whoosh-cinematic", 0.11, "sfx-end-build"),
    (18.32, "impact-swell", 0.22, "sfx-end-hit"),
]
audio = [
    '      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-track-index="10" data-volume="1"></audio>',
    f'      <audio id="music" class="clip" src="assets/music.wav" data-start="0" data-duration="{DURATION}" data-track-index="11" data-volume="0.6"></audio>',
]
import subprocess
lanes = []  # end time per sfx lane
for st, f, v, i in SFX:
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                f"assets/sfx/{f}.mp3"], capture_output=True, text=True).stdout)
    lane = next((k for k, e in enumerate(lanes) if e <= st), None)
    if lane is None:
        lanes.append(0.0)
        lane = len(lanes) - 1
    lanes[lane] = st + dur
    fade = ""
    if f == "impact-bass-1":
        dur, fade = 1.1, ' data-fade-out="0.7"'
    audio.append(
        f'      <audio id="{i}" class="clip" src="assets/sfx/{f}.mp3" data-start="{st:.2f}" data-duration="{dur:.2f}" data-track-index="{12 + lane}" data-volume="{v}"{fade}></audio>'
    )

SCENES = [
    ("hook", 0, 1.9, 2),
    ("intro", 1.86, 4.16, 2),
    ("summit", 7.92, 6.10, 3),
    ("unforget", 14.02, 3.0, 2),
    ("callback", 17.02, 3.34, 2),
    ("endcard", 20.36, round(DURATION - 20.36, 2), 3),
]
hosts = []
for sid, st, d, tr in SCENES:
    hosts.append(
        f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html"\n'
        f'        data-start="{st}" data-duration="{d}" data-track-index="{tr}" data-track-kind="graphics"\n'
        f'        data-width="1080" data-height="1920" style="z-index: 5"></div>'
    )
hosts.append(
    '      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"\n'
    f'        data-start="0" data-duration="{END_SPEECH:.2f}" data-track-index="5" data-track-kind="captions"\n'
    '        data-width="1080" data-height="1920" style="z-index: 8"></div>'
)

zoom_js = []
for k, (st, z, sid) in enumerate(zooms):
    if sid == "s01":  # hook: snap in from wide
        zoom_js.append(f'      tl.fromTo("#cam", {{ scale: 1.25 }}, {{ scale: {z}, duration: 0.35, ease: "expo.out" }}, {st});')
    elif sid == "s15":  # Mabuhay callback: snap
        zoom_js.append(f'      tl.fromTo("#cam", {{ scale: 1.38 }}, {{ scale: {z}, duration: 0.3, ease: "expo.out", immediateRender: false }}, {st});')
    else:  # hard punch-in on the jump cut
        zoom_js.append(f'      tl.set("#cam", {{ scale: {z} }}, {st});')

html = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0b1e4a; }}
      #cam {{ position: absolute; inset: 0; overflow: hidden; }}
      #cam video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{DURATION}"
      data-width="1080" data-height="1920">
      <!-- A-roll: {len(cuts)} cuts from assets/raw.mp4 (edit/cuts.json); #cam carries the punch-ins -->
      <div id="cam" style="z-index: 1">
{chr(10).join(videos)}
      </div>

      <!-- Graphics scenes -->
{chr(10).join(hosts)}

      <!-- Sound: cleaned voice, music bed, effects -->
{chr(10).join(audio)}
    </div>

    <script>
      const tl = gsap.timeline({{ paused: true }});
      gsap.set("#cam", {{ transformOrigin: "{ORIGIN}" }});
      // punch-in per cut so every jump cut reads as intentional
{chr(10).join(zoom_js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(html)
print(f"index.html written; speech ends {END_SPEECH:.2f}s, video {DURATION}s")
