# SPEC: Pak Su Den, Malaysia Judge, Philippines World Massage Summit 2027

GOAL:    In under 25 s the viewer knows who Pak Su Den is, that he judges the Philippines World Massage Summit 2027 in Manila, and feels invited ("see you in Manila").
OUTPUT:  HyperFrames, 1080 x 1920 (9:16 Reels/TikTok/Shorts), 30 fps
TIME:    23.6 s x 30 = 708 frames. Music 112 BPM (16.07 frames a beat), bar line anchored on the "2027" drop at 10.26 s.

## Source and cuts (edit/cuts.json)

Raw 34.5 s → spoken edit 20.36 s + 3.2 s end card.

| Removed | Why |
|---|---|
| 0.00–2.44 | dead air before he speaks |
| "Hello everyone" (5.2–6.2) | second greeting straight after "Mabuhay, Philippines!" |
| "See you there" (21.7–22.4) | said again in the closing "see you in the Philippines" |
| ~12 pauses of 0.3–0.9 s | hesitations, mainly in "and… let… me… make… an… unforgettable" |

HOOK: frame 0 is his face plus "MABUHAY," already on screen, with the two flags. The greeting in Tagalog from a Malaysian is the stop-scroll moment.

## Look (taken from the poster itself)

- Navy #0B1E4A plates with a double gold rule (the poster's name plates), gold #F2C14E → #B8862B gradient, white ink.
- Display: Playfair Display 900 / 900 italic (the poster's serif). Captions: Montserrat 900 uppercase. Labels: Oswald 600, +12% tracking.
- Imagery: crops of the poster (flags, summit badge, his portrait, judges, Philippines landscape). No invented graphics where the poster has the real thing.

## Shots (edited timeline, seconds)

| Time | Picture | Text | Sound |
|---|---|---|---|
| 0.00–1.86 | Face, snap zoom 1.25→1.0; MY flag from left, PH flag from right (top band) | "MABUHAY," slam (frame 0) → "PHILIPPINES!" whip-in at 0.94 | bass impact 0.07, whoosh 0.94 |
| 1.86–6.02 | Face, punch-ins on every cut (1.10 / 1.22 / 1.08) | Name plate in at 2.62: portrait + "MOHD ABIDDIN BIN HJ AHMAD" / "MALAYSIA JUDGE"; chip "PAK SU DEN" at 4.48; MY flag chip at 5.44 | whoosh-high 2.62, pop 4.48, ping 5.44 |
| 6.02–7.92 | Face 1.16 | captions | riser starts 6.79 (crests 10.26) |
| 7.92–14.02 | Poster B-roll: whip in on the summit badge → pan to the title → "2027" slam → pan down to the Manila landscape | "2027" giant gold at 10.26; pin "MANILA, PHILIPPINES" 12.66; "17–18 APRIL 2027" 12.95 | whoosh-low 7.92, sparkle 8.35, impact 10.26, whoosh 12.14, pop 12.66, ping 12.95 |
| 14.02–17.02 | Face, alternating zooms on each word cut (1.18 / 1.06 / 1.24 / 1.12 / 1.30) | "UNFORGETTABLE" letters at 15.54, "EXPERIENCE" at 16.40 | sparkle 15.54, whoosh-high 16.40 |
| 17.02–20.36 | Face zoom 1.35→1.18; flags fly back in (callback) | "MABUHAY!" callback; captions; "BYE!" | whoosh 17.08, cinematic whoosh + swell into 20.36 |
| 20.36–23.60 | End card: summit badge, "MALAYSIA JUDGES", the 4 judges, his plate ringed in gold | "SEE YOU IN MANILA!" + "17–18 APRIL 2027" | impact swell 20.39, music opens up, chord rings out |

Captions: 2–3 words, Montserrat 900, 74 px, white with dark stroke, the spoken word turns gold; centred at y≈1250 (inside the 168–1330 safe band). Not shown where a big title says the same words (hook, 2027, unforgettable experience).

## Audio

- Voice: cut with 12 ms fades, high-pass 85 Hz, denoise, presence +2.5 dB, compression, −16 LUFS (edit/build_voice.py).
- Music: TEMPORARY tropical-pop bed generated in code (edit/build_music.py), ducked −11 dB under the voice, opens on the end card. Replace with a licensed track.
- SFX: HyperFrames bundled library (Pixabay licence), ~0.35–0.55 volume, pitched variants so no two whooshes are the same.

## BANNED

Glow orbs and particles; glass cards; everything fading and sliding up; titles that keep drifting after they land; text over his face; the logo docked in a corner.

## QA frames

0.0 (thumbnail: face + MABUHAY), 0.95, 2.9 (name plate), 4.7 (chip), 8.5 (badge), 10.4 (2027), 13.3 (Manila + date), 15.9 (UNFORGETTABLE), 17.3 (callback), 21.5 (end card).
