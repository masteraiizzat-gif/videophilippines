"""One-shot generator for compositions/captions.html.

Word times are on the edited timeline (whisper on assets/voice.wav, checked by
ear-free energy analysis). Words that a big title already says (hook, 2027,
unforgettable experience, Mabuhay callback, Bye) are left out on purpose.
"""
import html

GROUPS = [
    [("I", 2.10), ("AM", 2.18), ("MOHD", 2.62)],
    [("ABIDDIN", 3.02), ("BIN", 3.46), ("AHMAD,", 3.62)],
    [("CALL", 4.16), ("ME", 4.34), ("PAK", 4.48), ("SU", 4.76), ("DEN", 4.95)],
    [("FROM", 5.22), ("MALAYSIA.", 5.44)],
    [("I", 6.08), ("AM", 6.24), ("HONOURED", 6.42)],
    [("TO", 6.74), ("BE", 7.08), ("JOINING", 7.40)],
    [("THE", 7.96), ("PHILIPPINES", 8.30)],
    [("WORLD", 8.96), ("MASSAGE", 9.30), ("SUMMIT", 9.94)],
    [("IN", 12.20), ("MANILA.", 12.66)],
    [("AND", 13.22), ("LET", 13.66), ("ME", 14.08)],
    [("MAKE", 14.60), ("AN", 15.10)],
    [("SEE", 17.86), ("YOU", 18.08), ("IN", 18.48)],
    [("THE", 18.90), ("PHILIPPINES!", 19.00)],
]
ENDS = [3.02, 4.10, 5.20, 6.00, 6.74, 7.90, 8.96, 10.24, 13.16, 14.50, 15.46, 18.90, 19.56]

BASE, MAXW = 76, 900


def est_width(words, size):
    chars = sum(len(w) for w, _ in words)
    return size * (0.80 * chars + 0.32 * (len(words) - 1)) * 1.12  # active word scales 1.12


css, divs, js = [], [], []
for gi, (words, end) in enumerate(zip(GROUPS, ENDS)):
    gid = f"cap-{gi + 1:02d}"
    start = round(max(words[0][1] - 0.06, ENDS[gi - 1] if gi else 0), 2)
    size = BASE
    while est_width(words, size) > MAXW and size > 42:
        size -= 2
    spans = " ".join(
        f'<span id="{gid}-w{k}" class="cap-w">{html.escape(w)}</span>' for k, (w, _) in enumerate(words)
    )
    divs.append(
        f'    <div id="{gid}" class="clip cap" data-start="{start}" data-duration="{round(end - start, 2)}" '
        f'data-track-index="0" style="font-size: {size}px">{spans}</div>'
    )
    js.append(f'    tl.fromTo("#{gid}", {{ scale: 0.82, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.14, ease: "back.out(2)" }}, {start});')
    for k, (w, t) in enumerate(words):
        js.append(f'    tl.to("#{gid}-w{k}", {{ color: "#F2C14E", scale: 1.12, duration: 0.07, ease: "power2.out" }}, {t});')
        if k + 1 < len(words):
            js.append(f'    tl.to("#{gid}-w{k}", {{ color: "#FFFFFF", scale: 1, duration: 0.07, ease: "power2.out" }}, {words[k + 1][1]});')
    js.append(f'    tl.to("#{gid}", {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, {round(end - 0.09, 2)});')
    js.append(f'    tl.set("#{gid}", {{ opacity: 0 }}, {end});')

out = f"""<template>
  <style>
    @font-face {{ font-family: "PS Montserrat"; font-weight: 900; src: url("assets/fonts/montserrat-latin-900-normal.woff2") format("woff2"); }}
    #root {{ position: absolute; inset: 0; overflow: visible; }}
    .cap {{ position: absolute; left: 0; top: 1200px; width: 1080px; text-align: center; white-space: nowrap; overflow: visible;
      font-family: "PS Montserrat", sans-serif; font-weight: 900; line-height: 1.15; }}
    .cap-w {{ display: inline-block; margin: 0 0.1em; color: #fff; -webkit-text-stroke: 10px #0b1e4a; paint-order: stroke fill;
      text-shadow: 0 7px 0 #0b1e4a, 0 12px 26px rgba(0, 0, 0, 0.55); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(divs)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
open("compositions/captions.html", "w").write(out)
print("compositions/captions.html:", len(GROUPS), "groups")
