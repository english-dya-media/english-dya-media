# Rostam & Sohrab: a shadow-play series for @english_dya

Ferdowsi's story of Rostam and Sohrab told in **20 animated parts of about 5 minutes**, one part a day at
**20:00 Tehran** (17:30 or 16:30 Rome, depending on daylight saving), posted as an Instagram Reel through Metricool
(brand `7830959`). The owner (Salar) chose every part of this format; keep it.

## The format (keep it)

- Vertical 1080×1920, 30 fps, ≤ 5:00 (Instagram's API takes reels up to 15 min; we keep 5).
- **Shadow-play animation**: black puppet silhouettes with a warm rim light, over coloured skies and lit interiors,
  drawn in code (`anim.py`, `puppets.py`, `sets.py`). No images from outside.
- Every frame carries the header **«قسمت N از داستان رستم و سهراب»** at the top (render.py draws it when the
  script has `"part"`), the page name small and moving (watermark), English dialogue with an English voice per
  character (`cast.json`, Kokoro via sherpa-onnx), and subtitles in English with Persian under them.
- Like a film: characters talk to each other; the narrator only links scenes and jumps in time.
- 1–3 real couplets of Ferdowsi per part, shown as a gold verse card while the narrator gives the meaning in English.
  **Only verses checked on Ganjoor** (https://ganjoor.net/ferdousi/shahname/sohrab/ and its sh1…sh29 pages); never
  invent or "fix" a verse. If you can't verify one, use none.
- Each part: a short cold-open hook (8–15 s, something dramatic from this part), then the TITLE card (5–6 s:
  "PART N · TITLE"), the story, and the END card (6 s: "NEXT PART · next title", «برای دیدن بقیه فالو کن», + FOLLOW).
- Captions (Persian, informal spoken style), built by `plan_parts.py` from `parts.json`: title line, 2 short lines
  about what happens (end on a hook, don't spoil the ending), 5–6 English words from the part with an emoji, US
  pronunciation in Persian letters and the meaning (story words a learner can use: hero, fate, saddle, guest…; no
  names), the source line, «قسمت بعد … فردا ساعت ۸ شب 🌙» + follow line, 5 hashtags. AI label on (synthetic voices).

## Files

| file | what it is |
|---|---|
| `anim.py` | engine: pen passes (mask → glow, rim, fill), `Cam` push-ins/parallax, `Talk` (jaw from loudness), `figures()`, anchors + `rope()`, `SHIFTS`, and episode 1's cold-open world |
| `puppets.py` | `person()` (LOOKS: rostam, rostam_bare, rostam_robe, young_rostam, sohrab, tahmineh, maid, king, kavus, afrasiab, gordafarid, warrior_ir, warrior_tu, rider, guard, noble, herdsman, mobed, poet, musician; modes stand/walk/sit/kneel/lie/ride; props mace, oxmace, spear, staff, lamp, candle, cup, lasso, pen, saddle, quiver) and `horse()` (stand/walk/gallop/rear/graze, rider, saddle; kind "onager") |
| `sets.py` | skies, sun/moon/stars, ridges, clouds, storm, trees, reeds, water, tents, city skyline, fire, rain, birds, dust, arches, lattice, lamps |
| `ep01_scenes.py` | every shot of parts 1–2: **read it before writing a new part** (how scenes, timing and layout are done) |
| `render.py` | compositor: `full` / `preview` / `still` (subtitles, verse cards, title/end cards, header, watermark, audio) |
| `voices_ep.py` | script → `audio/episode.wav` + `audio/timeline.json` |
| `plan_parts.py`, `parts.json` | captions and Metricool items; registry of parts (date, media, words, summary) |
| `OUTLINE.md` | what happens in each of the 20 parts + continuity notes |
| `ep01/script.json` | the script of parts 1–2 (one long episode that was cut in two with `split_parts.py`) |

From part 3 on, each part is its own folder `pNN/` (`p03`, `p04` …) with `script.json`, and its scenes are in
`pNN_scenes.py` (render.py loads the module named after the folder).

## Daily part run

The scheduled job "Rostam & Sohrab: next part" runs this every morning. Work in `studio/rostam/`.

1. **Buffer check**: Metricool `getScheduledPosts` (brand 7830959, Europe/Rome) from now to 10 days ahead. Count
   PENDING posts whose media file is `rostam_partNN.mp4` (or whose caption starts with «🎬 قسمت … از داستان رستم و سهراب»).
   If the next 2 days at 20:00 Tehran already have a part each, or the last part (20) is scheduled, stop and report.
   The next part number is the highest in `parts.json` + 1; its day is the first day after the last scheduled part
   (never today if 20:00 Tehran is less than 2 hours away).
2. **Setup**: `bash setup.sh`.
3. **Script** `pNN/script.json` (same shape as `ep01/script.json`, plus `"part": N`, `"next_label": "NEXT PART"`,
   `next_en`/`next_fa` = the next part's title from `parts.json` "titles", `"episode"` = (N+1)//2). Follow
   `OUTLINE.md` for part N and the continuity notes. Hook scene `S01`, then `{"id": "TITLE", "card": "title",
   "dur": 5.0, "lines": []}`, then 10–16 shots (`S02`…), then `{"id": "END", "card": "end", "dur": 6.0, "lines": []}`.
   Short lines (≤ 2 lines of English on screen each; split long ones), mostly dialogue, verses with `"verse": [h1, h2]`
   and `"pre": 2.0`. New speaking roles go in `cast.json` with an unused Kokoro voice (b… = British, a… = American)
   and, for names, a respelling in `_say`; add the role's Persian name to `ROLE_FA` in render.py.
4. **Voices**: `python3 -I voices_ep.py cast.json pNN/script.json pNN/audio`. The total (printed) must be
   4:30–4:55 (end card included). Too long or short: edit the script and rerun.
5. **Scenes** `pNN_scenes.py`: one function per shot id, plus "TITLE" (usually the hook's world continuing, like
   `cold_open`) and "END" (the last shot continuing); register them with `anim.SCENES.update({...})` and set
   `anim.SHIFTS` where needed. Time the action to the lines (`audio/timeline.json`; use `jaw(an, ROLE, t)` for
   talking). Reuse puppets and sets; add new looks or props to `puppets.py`/`sets.py` when the story needs them
   (keep old ones working: parts 1–2 must still render).
6. **Check** before rendering: `python3 -I render.py still pNN pNN/images /tmp/sN.jpg <t>` at the busiest moment of
   every shot (subtitle and verse card on screen); put them on one contact sheet and look. Fix anything listed
   under *Layout rules*. Then a quick crash test of every shot (render `bg_frame` every ~1 s).
7. **Render**: `python3 -I render.py full pNN pNN/images pNN/rostam_partNN.mp4` (≈ 10 min). Check: ≤ 300 s,
   1080×1920, audio present, header on screen; look at 6 frames spread over the part.
8. **Upload** the mp4 to a new branch `media-rostam-pNN` from a fresh empty folder (as in studio/RUNBOOK.md step 9,
   one file per push) and check `https://raw.githubusercontent.com/english-dya-media/english-dya-media/media-rostam-pNN/media/rostam_partNN.mp4` answers 200/206.
9. **Schedule**: add part N to `parts.json` (title_fa, title_en, date = its Tehran day, media =
   `media-rostam-pNN/media/rostam_partNN.mp4`, cover_ms = a striking frame, e.g. on the title card, summary, words),
   run `python3 plan_parts.py N`, check again in Metricool that the slot is free, then `createScheduledPost`
   (blogId "7830959", date = item date, info = item info). Expect PENDING with the media copied to static.metricool.com.
10. **Save**: commit `parts.json`, `pNN/script.json`, `pNN_scenes.py`, `cast.json` and any engine changes to `main`
    (`git pull --rebase origin main` first). Never commit audio, renders or the voice model (see .gitignore).
    Delete `media-rostam-*` branches whose part is already published.
11. **Report** (short, English): part N title, its date, the 6 words, anything that failed.

If you can't finish a part (time, errors), schedule nothing half-done; report what's missing so the next run or the
owner can pick it up. Never schedule the same part twice; never edit or delete existing Metricool posts.

## Layout rules (learned on parts 1–2)

- Instagram covers the top ~270 px and the bottom ~670 px. The header sits at y≈218, the verse card at y 350–690,
  subtitles fill y≈800–1240 (higher when the line is long). Keep faces, hands and props between y≈300 and ≈860.
- Ground/horizon at y≈860–880, feet there. When a verse card is on screen, shift the shot down (`anim.SHIFTS[sid]`
  = 120–270) so people stand under the card; when subtitles are long, shift up (−60 … −110).
- Silhouettes are black: on dark ground they vanish. A lying body, a fallen fruit, hoofprints, a bed: put a lighter
  backdrop behind them (water, sky, a lit wall or curtain).
- Overlapping silhouettes merge into one blob: keep figures apart, profiles facing, arms away from the body.
- Close-ups: scale 1.6–3.0 with the feet below the frame; two-shots work at 1.5–1.65.
- Night/interiors need a light source (lamp, candle, fire, moon) with `S.glow`, and the figures' glow colour to match.
- One glow colour per `an.figures()` call; a second call for a figure that needs its own rim (Rakhsh got a rose rim).
- `tag("name:")` before a puppet names its anchors (`hand`, `rhand`, `neck`, `head`, `mouth`, `flame`, `cup`…);
  call `an.figures(..., anchors=True)` to use them (ropes, flames, lamp light).
- Speed: 80–200 ms a frame; avoid full-frame blurs or hundreds of gradient shapes per frame (cache static layers in
  `an.cache` with `get()`).
