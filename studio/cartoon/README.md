# Cartoon story series for @english_dya

Persian stories told as **2D cartoon reels in English** (English voices, English + Persian subtitles), in parts of
under 3 minutes, posted through Metricool (brand `7830959`) **after Rostam & Sohrab ends**: two parts a day at
**18:00 and 20:00 Tehran**, one series after another in the order of `queue.json`:

| # | series (folder) | parts | source | state |
|---|---|---|---|---|
| 1 | Babak Khorramdin · بابک خرمدین (`babak/`) | 8 | approved scripts `babak/SCRIPTS.md` (Iranica, Ibn al-Nadim, Tabari) | all 8 parts made |
| 2 | Zahhak & Fereydun · ضحاک و فریدون (`zahhak/`) | 10 | Shahnameh | outline |
| 3 | Arash the Archer · آرش کمانگیر (`arash/`) | 3 | Biruni, Iranica | outline |
| 4 | Leyli & Majnun · لیلی و مجنون (`leyli/`) | 8 | Nizami | outline |
| 5 | Khosrow & Shirin · خسرو و شیرین (`khosrow/`) | 10 | Nizami | outline |
| 6 | Hasan Kachal · حسن کچل (`hasan/`) | 4 | folk tale | outline |
| 7 | Mah Pishani · ماه‌پیشونی (`mahpishani/`) | 5 | folk tale | outline |

The owner (Salar) asked for all of these "like Rostam & Sohrab / Babak", chose the 2D cartoon look (he did not like
silhouettes for Babak) and left the number of parts to us (by the length of each story). Keep the format.
`python3 plan_parts.py status` shows what is made and scheduled.

## The format (keep it)

- Vertical 1080×1920, 30 fps, **≤ 2:50 including the end card** (never 3:00 or more), about 2:00–2:45.
- **2D cartoon drawn in code**: SVG character rig (`chars.py`) rendered with resvg, painted backgrounds (`bgs.py`),
  light, particles and grading (`film.py`). No images from outside, no famous film or book designs.
- Every frame carries the header **«قسمت N از داستان …»** at the top (`cards.part_header`, overlaid by `encode.py`),
  the page name small and moving (`@english_dya`, 30 px, 45 % white, changes place every 20 s: top left, middle
  right, top right, middle left), English dialogue with an English voice per character (`<series>/lines.py` VOICES,
  Piper libritts-high speakers), and subtitles in English with Persian under them (`subs.py`, SUB_Y 1040), plus
  place/year captions (`caption()`).
- Like a film: characters talk to each other; the narrator only links scenes and jumps in time. Short lines.
- Each part: a short hook (3–8 s, something striking from this part or later), the TITLE card (4–5 s, "SERIES · PART
  N · TITLE" over the picture), the story, the END card (4–6 s): "NEXT PART · next title … برای دیدن بقیه فالو کن";
  a series' last part gets "NEXT STORY · next series" (or "THE END" for the last series). Every part makes sense
  alone and ends on a question or a turn.
- Violence and death are never shown: shadows, sound, a closing door, a lamp going out. Nothing gory or frightening
  for children; romance stays modest.
- Captions (Persian, informal spoken style), built by `plan_parts.py` from `<series>/parts.json`: «🎬 قسمت N از
  داستان … | title», 2 short lines about the part (end on a hook, don't spoil), 6 English words from the part with an
  emoji, US pronunciation in Persian letters and the meaning (story words a learner can use; no names), the source
  line, when the next part comes («امشب ساعت ۸» / «فردا ساعت ۶ عصر») + follow line, 5 hashtags. A series' last part
  announces the next series. AI label on (synthetic voices).
- **YouTube**: every part also goes to the page's YouTube channel as a Short in the same Metricool post (providers
  instagram + youtube, `youtubeData` from `../youtube.py` kind "series", tags from `yt_tags` in parts.json), like all
  the page's videos (see `../RUNBOOK.md`).

## Files

Engine (this folder):

| file | what it is |
|---|---|
| `chars.py` | the rig: `spec()` (looks; helmet colours `helm`/`plume`, cloak colours `cloak2`/`cloak_hi`, `pattern="scales"` for lamellar armour), `pose()`, `person()` (heads with eyes, brows, lips and beards; hair; headwear helmet/fur_hat/turban/cap/scarf+diadem; garments; arms with presets or `("ik", x, y)` (`("ik", x, y, "down")`: elbow down, for handing things over); props lantern, bread, baby, stick, brush, sack, purse, sword, spear, pike, bowl, scroll, spear_red, banner_black, banner_red, tanbur, dagger, torch, shovel, pick, drumstick, or `(name, angle)`; `chains=True` or `"rope"` with `lead=(x, y)`), `lying_person()`, `horse()` (`packs`, `mule`), `elephant()` (`kneel` 0..1, riders move down by `kneel_drop()`), `dog()` (a saluki, `run`), `cow()`, `camel()` (a dromedary, pacing; a rider on the hump with `camel_rider` in `babak/p08_scenes.py`); prop `falcon` (perched on a gloved fist); pose `red`/`red_reveal` (Babak's red face, wiped on from left to right) |
| `stage.py` | placing people: `at_feet`, `at_neck`, `lying_at`, `crowd_row`, `back_heads`, `rider`, `howdah`, `fire_svg`, `Glow` |
| `film.py` | `Shot` (bg/mid/fg layers, camera, light, particles Snow/Motes/Embers, bloom, grade, fades), lip sync `mouth()`/`talk_pose()`, `render_scene()`, `stills()` |
| `bgs.py`, `wallbg.py` | painted backgrounds, cached in `build/bg` (Samarra, village, stable, bazaar, blizzard, interior, fortress above clouds, battle fog, bedroom, courtyard, throne hall, fortress wall at sunrise; Babak 3–4: the pass `gorge_floor`+`gorge_walls`, `cliff_up`, `ridge_view`, `gorge_down`, `ledge_fg`, `village_square`, `snow_pass`+`snow_fg`, `camp_rocks`, `map_dirt`, `stream_bg`, `feast_night`, `tent_interior`, `gold_hall`, `night_plain`, `night_sky_wall`; Babak 5–6: `command_tent`, `fort_road`, `army_camp`, `ridges_dusk` (+`RIDGE_FIRES`), `war_room`, `table_map`, `forest_road("day"/"night")`, `leaves_fg`, `woods_night`, `ravine("night"/"dawn")`, `ravine_up`, `side_gate_night`, `wall_outside`, `forest_stream`, `field_dawn`, `armenia_gate`; Babak 7: `forest_road("autumn")`, `sahl_room`, `winter_road`, `palace_court` (Samarra palace, gate x 80-470, ground from y 1080); Babak 8: `court_dusk` (the caliph's raised seat, torches), `shadow_wall`, `samarra_dawn`, `tigris_dawn`, `tower_night`, `prison_cell`, `bazz_ruins` (Bazz today, with `cloud_sea`); `boulder()` rocks, `pine()`, `oak()`, `bare_tree()`, `oil_lamp()`) |
| `voices.py`, `lips.py` | Piper voices → `build/<series>/voices/<id>.wav` + durations.json; lip-sync data (optional `SPEED` in `lines.py`: per-line length factors, e.g. slower takes for learners; optional `FX`: per-line ffmpeg filters, e.g. a trembling voice) |
| `audio.py`, `mix.py` | synthesized music and sound effects; mixing a part's lines, music and effects |
| `subs.py` | subtitle and caption events → .ass |
| `render.py`, `prev.py` | render a part's scenes in parallel; contact sheet of a scene |
| `cards.py`, `encode.py`, `assemble.py` | header/title/end cards; final encode (~3 Mbit/s, ~50 MB a part: GitHub takes < 100 MB); join scenes → `build/<series>/out/<series>_partNN.mp4` |
| `plan_parts.py`, `queue.json`, `series.py`, `paths.py` | captions, slots, status and Metricool items; series order; series selection; folders |

A series folder (`babak/`, `zahhak/` …): `parts.json` (names, hashtags, source, titles, registry of parts),
`OUTLINE.md` (what happens in each part, characters, places; Babak: `SCRIPTS.md`), `cast.py` (looks),
`lines.py` (`LINES` `(id, part, scene, speaker, english, persian, tts_text)` and `VOICES`), and per part
`pNN_scenes.py`, `pNN_audio.py`, `pNN_subs.py`. **Read `babak/p01_scenes.py`, `babak/p02_scenes.py`,
`babak/p02_audio.py` and `babak/p02_subs.py` before writing a new part**: they show how shots, timing, lip sync,
light, sound and captions are done. Every command takes the series first: `python3 render.py zahhak p01 all 2`.

## Making a part (N of series S)

1. `bash setup.sh` (packages, Piper voice model).
2. **Script** from `S/OUTLINE.md` (or `babak/SCRIPTS.md`): 4–7 scenes, ~2:10–2:40 in total, mostly dialogue, short
   lines (≤ 2 lines of English on screen; split long ones), names respelled for the voice in `tts_text`
   ("Baabak", "Fereydoon", "Zah-hawk", "Sheereen"). Add the lines to `S/lines.py` (ids `pNsKx`), new roles to
   VOICES (libritts speaker id, speed, semitones, volume: pick ids that fit and differ from the other roles in the
   same part; reuse the narrator `NARRATOR` of the series), new looks to `S/cast.py` (`spec()` from `chars.py`).
   `python3 voices.py S N`.
3. **Timing and sound**: `S/pNN_audio.py` like `babak/p02_audio.py` (TOTAL, scene starts, line start times `LINES`,
   music and sound cues) → `python3 S/pNN_audio.py`. Then `S/pNN_subs.py` → `build/S/out/pNN.ass` (subtitles +
   place/year captions; keep them off the title card and end card).
4. **Scenes** `S/pNN_scenes.py` with `SCENES = {"s1": fn, …}` in story order; each returns `Shot`s whose durations add
   up to that scene's length in `pNN_audio.py`. Reuse looks, props and backgrounds; add what the story needs to
   `chars.py`/`bgs.py`/`stage.py` (snakes on Zahhak's shoulders, a bow, a div, a yellow cow, a well, a tomb …) and keep
   every older part working (render one still of `babak p01_scenes s1` after changing the engine).
   Lip sync: `talk_pose(lines, t, seed)` with `lines` = [(line id, start in the shot)].
5. **Check** before rendering: `python3 prev.py S pNN_scenes sK t1,t2,t3` for every scene at its busiest moments
   (subtitles on screen), and look. Fix anything under *Layout rules*.
6. **Render**: `python3 render.py S pNN all 2` (≈ 30–40 min a part). Add the part to `S/parts.json` (title_fa,
   title_en, media `media-S-pNN/media/S_partNN.mp4`, cover_ms on the title card, duration, cards {"title": [start,
   end], "end": start, "wm_off": ""}, summary, words; date and slot null) and run `python3 assemble.py S N`. Check
   6 frames spread over the part (title card, subtitles, end card).
7. **Upload** to a new branch `media-S-pNN` from a fresh empty folder (as in `../RUNBOOK.md` step 9, one file per
   push) and check `https://raw.githubusercontent.com/english-dya-media/english-dya-media/media-S-pNN/media/S_partNN.mp4`
   answers 200/206.
8. **Save**: commit `S/` and engine changes to `main` (`git pull --rebase origin main` first). Never commit audio,
   renders, the voice model or `build/`.

## Daily run

The scheduled job "Story series: next part" runs this twice a day. Work in `studio/cartoon/`.

1. **Look**: `python3 plan_parts.py status`; Metricool `getScheduledPosts` (brand 7830959, Europe/Rome) from today to
   40 days ahead. Rostam & Sohrab captions start «🎬 قسمت … از داستان رستم و سهراب», cartoon series «🎬 قسمت … از
   داستان <series_fa>». Rostam & Sohrab has *finished scheduling* when its part 40 («قسمت ۴۰ از داستان رستم و
   سهراب») is in Metricool (pending or published) or `../rostam/parts.json` has a date for part 40.
2. **Make** the next part(s) in queue order (`next_to_make`), as above: two parts if there is time, else one done well.
3. **Schedule** (only when Rostam & Sohrab has finished scheduling): parts go out strictly in queue order (series by
   series, part by part); stop at the first part that isn't made. Fill the free slots up to 10 days ahead:
   `python3 plan_parts.py slots "<YYYY-MM-DD HH:MM Tehran of the last scheduled post among Rostam's part 40 and the
   cartoon parts>" <count>`, check in Metricool that nothing else is within 30 minutes of each slot, fill `date`/`slot`
   in `S/parts.json`, `python3 plan_parts.py S N …` and `createScheduledPost` for each (blogId "7830959", date = item
   date, info = item info). Expect PENDING on both networks (Instagram reel + YouTube Short) with the media copied to
   static.metricool.com. Commit.
4. **Clean up**: delete `media-<series>-*` branches whose parts are all published.
5. **Report** (short, English): parts made, parts scheduled with dates and slots, anything that failed.

If you can't finish a part, schedule nothing half-done and report what's missing. Never schedule a part twice or out of
order, never before Rostam & Sohrab's part 40, never publish immediately; never edit or delete existing Metricool posts.

## Layout rules (learned on Babak parts 1–2)

- Instagram covers the top ~270 px and the bottom ~670 px. The header sits at y≈218; subtitles at y≈1040–1240;
  place captions just under the header (y≈280–330). Keep faces, hands and props between y≈300 and ≈1000.
- The page name visits y 300 and 860 at the left and right edges: hide it (`wm_off`) while a caption sits there.
- People stand on the ground line of the background; set the scale with `at_feet` so feet never float; children's
  heads sit on their necks, riders sit in the saddle, nobody stands on an animal's back.
- Arms: use presets or `("ik", x, y)` for hands that hold or point; check elbows bend the natural way.
- Night and interiors need a visible light (fire, lamp, moon) and `rim_point` light on faces near it.
- Camera moves are slow push-ins; never pan past the painted edge of a background.
- Crowds: `crowd_row`/`back_heads`, darker and smaller in the back. Battles: two clear sides, a few big figures in
  front, fog and dust behind, motion in spears and banners; no blood.
- Speed: ~0.5–1 s a frame per process; cache static layers (`bgs.cached`).
