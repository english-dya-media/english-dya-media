# Civil engineering page: daily reels

A second Instagram page owned by Salar (PhD candidate in geotechnical engineering) that teaches civil engineering.
It has its **own Metricool brand** (not @english_dya, brand 7830959). Owner's choices (15 Nov 2026):

- **One reel every day**, posted automatically.
- **Bilingual on screen**: every line in Persian, with the English line under it (technical terms in both languages).
- **Mixed audience**, rotating day by day: **concept** (مفهوم روز, students) → **process** (فرآیند اجرا: a
  schematic film of machines doing the work, e.g. a rig driving a pile, an excavator digging with soil nailing;
  owner's request) → **site tip** (نکته‌ی کارگاهی, site engineers) → **quiz** (تست روز, exam-style question with a
  5 s countdown, "comment your answer").

Brand: `BRAND_ID` = **(not connected yet: fill in when the page is connected)**, handle `HANDLE`.

## Format (keep it)

- 1080×1920 reel, 18–27 s, blueprint look: badge (kind + running number), hook question (fa + en), an animated
  diagram, a timeline of bottom captions (fa + en, short), then a 2.6 s follow card. Music bed (`../music.py`) and
  sound effects (`../assets/sfx`), **no voice**, so no AI label.
- Process reels: a side-view cross-section (soil layers, building, pit) with machines drawn in flat construction
  yellow (`YEL`, dark outline): they drive in, raise masts, dig, drill; the work advances in visible stages
  (blow counter, lifts removed one by one), then the reel explains how it works (load paths, why it is stable).
  Draw each machine in its working position and animate it with `move` / `turn` / `keyed` (SMIL); see
  `b002.py` (truck rig, pile driven blow by blow, impact flashes) and `b003.py` (excavator arm by inverse
  kinematics, soil removed with an animated clipPath, nails, shotcrete). Sounds in `sfx/`: thud, rumble, drill, spray.
- Quiz reels: question, small diagram, 4 options (الف ب ج د), countdown ring with «جوابتو کامنت کن», reveal at
  t_count + 5 s (right answer turns green and moves up, the others fade), then 1–2 explanation panels.
- Caption: Persian, informal spoken style; first line = the hook; a few lines of explanation (quiz captions never
  give the answer); an «📘 اصطلاحات» block of 3–4 `English = فارسی` terms; the follow line; hashtags (Persian and
  English, ~8–10). Posted at **20:30 Tehran** unless the numbers say otherwise.
- Keep everything that matters between y = 190 and 1500 (Instagram's buttons and caption cover the rest);
  `reel.py --preview` checks this.

## Files

- `kit.py`: helpers for diagrams (beam outlines that bend, supports, arrows, labels fa+en, cracks, dimension
  lines, concrete and hatch patterns, SMIL morphs and moves) and `write_reel` / `write_quiz`, which check lengths.
- `batches/bNNN.py`: the content of a batch of reels (`b001.py`: concept, site tip and quiz samples; `b002.py`,
  `b003.py`: process samples). Copy their patterns.
- `sfx/`: extra sounds made for these reels (the rest come from `../assets/sfx`).
- `content/cNNN.json`: one file per reel (written by the batch files). `out/cNNN.mp4`: renders (not committed).
- `reel.py`: `--preview` writes stills and `build/cNNN/sheet.jpg` (contact sheet) and prints layout problems;
  without it, renders the reel.
- `plan.py`: `dates` gives reels their days; `posts` builds the Metricool items.
- `TOPICS.md`: topic backlog and what is done.

## Weekly run (make and schedule the next 7 days)

Work in `studio/civil/`. Run each step, read its output, fix problems before moving on.

1. **Setup**: in `studio/`, `bash setup.sh` (or at least: `pip install --break-system-packages soundfile`, the fonts
   part of setup.sh, plus `@fontsource/jetbrains-mono` 500/700 copied into `assets/fonts/`).
2. **What's needed**: `getScheduledPosts` for BRAND_ID over the next 10 days. If 7 or more days ahead are already
   covered, report and stop. Otherwise make the missing days (up to 7). Continue the numbering after the last
   `content/cNNN.json` and the kind rotation after the last reel's kind.
3. **Write** `batches/bNNN.py` (copy the patterns of `b001.py`): one reel per day, topics from `TOPICS.md` in
   rotation, each a single clear idea a viewer can say back after one watch. Diagram first: what moves, what
   appears, in which order, matched to the captions (each caption ≈ 2.5–4 s on screen). Run it.
4. **Accuracy**: check every statement and number against a reliable source (textbook values, the standard's own
   numbers). Prefer principles that hold everywhere; a number that depends on a design code (cover, hook length,
   stripping times…) must name the code in the caption (ACI 318, Eurocode 2, مبحث نهم مقررات ملی ساختمان), or leave
   it out. Quiz: exactly one right answer under the stated assumptions (write the assumptions in the sub-line).
5. **Preview** every reel: `python3 reel.py content/cNNN.json --preview`, look at `build/cNNN/sheet.jpg` and at
   two full-size stills (`build/cNNN/prev_*.jpg`). Fix overlaps, labels hidden under captions, arrows that don't
   touch what they point at, text that wraps badly; rerun the batch and preview again.
6. **Render**: `python3 reel.py content/cNNN.json` for each (≈1–2 min each). Check 1080×1920, audio present.
7. **Dates**: `python3 plan.py dates cFIRST cLAST <first free date>`.
8. **Upload** to a new branch `media-civil-<first date>` holding only these files (fresh empty folder, as in
   `../RUNBOOK.md` step 9), and check one URL returns 200:
   `https://raw.githubusercontent.com/english-dya-media/english-dya-media/<branch>/media/cNNN.mp4`.
9. **Schedule**: `python3 plan.py posts <base url> cFIRST cLAST > build/plan.json`; check `getScheduledPosts` for
   duplicates, then `createScheduledPost` once per item with `blogId: BRAND_ID`, `date: item.date`,
   `info: item.info`. Then `getScheduledPosts` again: all PENDING.
10. **Save**: move the used topics to "Done" in `TOPICS.md`; commit `civil/` (not `build/` or `out/`) to `main`
    (`git pull --rebase origin main` first) and push. Delete `media-civil-*` branches whose last day has passed.
11. **Report** (English, ≤ 5 lines): the 7 topics with dates, anything that failed.

## Rules

- Never publish immediately; never edit or delete existing Metricool posts; never post to brand 7830959.
- If scheduling fails halfway, stop and report exactly which posts exist.
- Don't spend money. Keep the approved look; change it only when the owner asks.
