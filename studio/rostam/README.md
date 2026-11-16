# Rostam & Sohrab: a shadow-play series for @english_dya

Ferdowsi's story of Rostam and Sohrab told in **40 animated parts of under 3 minutes**, **two parts a day at
18:00 and 20:00 Tehran**, posted as Instagram Reels and YouTube Shorts (same Metricool post; `plan_parts.py` adds YouTube) through
Metricool (brand `7830959`). The owner (Salar) chose
every part of this format; keep it. Under 3 minutes because Instagram does not recommend longer reels to people
who don't follow the page, and new followers are the page's goal.

## The format (keep it)

- Vertical 1080×1920, 30 fps, **≤ 2:50 including the end card** (never 3:00 or more).
- **Shadow-play animation**: black puppet silhouettes with a warm rim light, over coloured skies and lit interiors,
  drawn in code (`anim.py`, `puppets.py`, `sets.py`). No images from outside.
- Every frame carries the header **«قسمت N از داستان رستم و سهراب»** at the top (render.py draws it when the
  script has `"part"`), the page name small and moving (watermark), English dialogue with an English voice per
  character (`cast.json`, Kokoro via sherpa-onnx), and subtitles in English with Persian under them.
- Like a film: characters talk to each other; the narrator only links scenes and jumps in time.
- 1–3 real couplets of Ferdowsi per part, shown as a gold verse card while the narrator gives the meaning in English.
  **Only verses checked on Ganjoor** (https://ganjoor.net/ferdousi/shahname/sohrab/ and its sh1…sh29 pages); never
  invent or "fix" a verse. If you can't verify one, use none.
- Each part: a short hook (3–8 s, something dramatic from this part), then the TITLE card (4 s: "PART N · TITLE"),
  the story, and the END card (6 s: "NEXT PART · next title", «برای دیدن بقیه فالو کن», + FOLLOW). Every part
  must make sense to someone who sees only that part, and end on a question or a turn.
- Captions (Persian, informal spoken style), built by `plan_parts.py` from `parts.json`: title line, 2 short lines
  about what happens (end on a hook, don't spoil the ending), 5–6 English words from the part with an emoji, US
  pronunciation in Persian letters and the meaning (story words a learner can use: hero, fate, saddle, guest…; no
  names), the source line, when the next part comes («امشب ساعت ۸» after an 18:00 part, «فردا ساعت ۶ عصر» after a
  20:00 part) + follow line, 5 hashtags. AI label on (synthetic voices).

## Files

| file | what it is |
|---|---|
| `anim.py` | engine: pen passes (mask → glow, rim, fill), `Cam` push-ins/parallax, `Talk` (jaw from loudness), `figures()`, anchors + `rope()`, `SHIFTS`, and episode 1's cold-open world |
| `puppets.py` | `person()` (LOOKS: rostam, rostam_bare, rostam_robe, young_rostam, sohrab, tahmineh, maid, king, kavus, afrasiab, gordafarid, warrior_ir, warrior_tu, rider, guard, noble, herdsman, mobed, poet, musician, div; modes stand/walk/sit/kneel/lie/ride; props mace, oxmace, spear, staff, lamp, candle, cup, lasso, pen, saddle, quiver, sword, club) and `horse()` (stand/walk/gallop/rear/graze, rider, saddle; kind "onager") |
| `sets.py` | skies, sun/moon/stars, ridges, clouds, storm, trees, reeds, water, tents, city skyline, fire, rain, birds, dust, arches, lattice, lamps |
| `ep01_scenes.py` | every shot of parts 1–2: **read it before writing a new part** (how scenes, timing and layout are done) |
| `p05_scenes.py` | parts 5–6 (`p06_scenes.py` only registers part 6) and sets to reuse: Rostam's bedchamber `room()` with an opening `door()`, `in_bed()` (sit up / lie back under a blanket), `corridor()`, `city_night()`, `moon_window()`, `king_room()`, `shadow_layer()` (stories cast on a lit curtain), `ghost_layer()` (a vision in the sky), `eagle()` |
| `p07_scenes.py` | parts 7–8 (`p08_scenes.py` registers part 8) and helpers to reuse: `LN(part, sid, k)` (line times read from the timeline, so the action follows the voices), `dissolve()` (a cross-fade inside one shot), `gem()` (Rostam's jewel, glowing over the silhouettes), `baby()`, `seated()` (a person sitting on the floor), `dawn_window()`, `months_window()` (moon phases, leaves, snow, blossom), `Coins`, `lamp_row()`, `courtyard()`, `cypress()`, `birth_room()` |
| `render.py` | compositor: `full` / `preview` / `still` (subtitles, verse cards, title/end cards, header, watermark, audio) |
| `voices_ep.py` | script → `audio/episode.wav` + `audio/timeline.json` |
| `plan_parts.py`, `parts.json` | captions and Metricool items; registry of parts (date, media, words, summary) |
| `OUTLINE.md` | what happens in each of the 20 parts + continuity notes |
| `ep01/script.json` | the script of parts 1–4 (one long episode, cut into four with `split_n.py`) |
| `split_n.py` | cuts a long render into short parts (header, clean starts, end cards) |

From part 5 on, each part is its own folder `pNN/` (`p05`, `p06` …) with `script.json`, and its scenes are in
`pNN_scenes.py` (render.py loads the module named after the folder). Two parts made in the same run may share
one scenes module: make `p06_scenes.py` a one-liner that imports `p05_scenes` and registers its own ids.

## Daily part run

The scheduled job "Rostam & Sohrab: next part" runs this every morning and makes **two parts** (one row of
`OUTLINE.md`, told in two halves). Work in `studio/rostam/`.

1. **Buffer check**: Metricool `getScheduledPosts` (brand 7830959, Europe/Rome) from now to 10 days ahead. Count
   PENDING **Instagram** posts whose caption starts with «🎬 قسمت … از داستان رستم و سهراب» (ignore YouTube-only
   copies: parts 1–4 also have separate YouTube posts at the same times). If the next 4 slots (18:00 and 20:00
   Tehran) are all filled, or part 40 is scheduled, stop and report. The next part number is the highest in
   `parts.json` + 1; parts go into the free slots after the last scheduled part, in order (never a slot less than
   2 hours away).
2. **Setup**: `bash setup.sh`.
3. **Scripts** `pNN/script.json` for both parts (same shape as `ep01/script.json`, plus `"part": N`,
   `"next_label": "NEXT PART"`, `next_en`/`next_fa` = the next part's title from `parts.json` "titles",
   `"episode"` = the OUTLINE row). Row r of `OUTLINE.md` is parts 2r−1 and 2r: split its events in two so each
   half has a turn at its end. Hook scene `S01`, then `{"id": "TITLE", "card": "title", "dur": 4.0, "lines": []}`,
   then 5–9 shots (`S02`…), then `{"id": "END", "card": "end", "dur": 6.0, "lines": []}`.
   Short lines (≤ 2 lines of English on screen each; split long ones), mostly dialogue, verses with `"verse": [h1, h2]`
   and `"pre": 2.0`. New speaking roles go in `cast.json` with an unused Kokoro voice (b… = British, a… = American)
   and, for names, a respelling in `_say`; add the role's Persian name to `ROLE_FA` in render.py.
4. **Voices**: `python3 -I voices_ep.py cast.json pNN/script.json pNN/audio` for each part. The total (printed)
   must be 2:15–2:48 (end card included), never 2:50 or more. Too long or short: edit the script and rerun.
5. **Scenes** `pNN_scenes.py`: one function per shot id, plus "TITLE" (usually the hook's world continuing, like
   `cold_open`) and "END" (the last shot continuing); register them with `anim.SCENES.update({...})` and set
   `anim.SHIFTS` where needed. Time the action to the lines (`audio/timeline.json`; use `jaw(an, ROLE, t)` for
   talking). Reuse puppets and sets; add new looks or props to `puppets.py`/`sets.py` when the story needs them
   (keep old ones working: parts 1–2 must still render).
6. **Check** before rendering: `python3 -I render.py still pNN pNN/images /tmp/sN.jpg <t>` at the busiest moment of
   every shot (subtitle and verse card on screen); put them on one contact sheet and look. Fix anything listed
   under *Layout rules*. Then a quick crash test of every shot (render `bg_frame` every ~1 s).
7. **Render** each part: `python3 -I render.py full pNN pNN/images pNN/rostam_partNN.mp4` (≈ 5 min each). Check:
   < 170 s, 1080×1920, audio present, header on screen; look at 6 frames spread over the part.
8. **Upload** both mp4s to a new branch `media-rostam-pNN` (NN = the first of the two) from a fresh empty folder
   (as in studio/RUNBOOK.md step 9, one file per push) and check that
   `https://raw.githubusercontent.com/english-dya-media/english-dya-media/media-rostam-pNN/media/rostam_partNN.mp4` answers 200/206.
9. **Schedule**: add both parts to `parts.json` (title_fa, title_en, date = its Tehran day, slot "18:00" or
   "20:00", media = `media-rostam-pNN/media/rostam_partMM.mp4`, cover_ms = a striking frame, e.g. on the title card,
   summary, words), run `python3 plan_parts.py N N+1`, check again in Metricool that the slots are free, then
   `createScheduledPost` for each (blogId "7830959", date = item date, info = item info). Expect PENDING with the
   media copied to static.metricool.com.
10. **Save**: commit `parts.json`, `pNN/script.json`, `pNN_scenes.py`, `cast.json` and any engine changes to `main`
    (`git pull --rebase origin main` first). Never commit audio, renders or the voice model (see .gitignore).
    Delete `media-rostam-*` branches whose part is already published.
11. **Report** (short, English): the two parts' titles, their dates and slots, anything that failed.

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
- `person(mode="sit")` draws the seated robe below the feet (it shows in the rim colour): sit people on the floor with
  `seated()` (p07_scenes) or in bed with `in_bed()`, which clip it away.
- A baby, a cup or a jewel held in the hands: draw it after the figure, at the hand anchors (`A("x:hand")`,
  `A("x:rhand")`, `A("x:hand_up")` = upper arm), inside the same `an.figures()` call (each call with `anchors=True`
  clears the anchors of the previous one).
- In scheduled runs the web fetch of ganjoor.net can be refused (a permission prompt nobody answers); then the part
  has no verses (parts 5–8 have none).
