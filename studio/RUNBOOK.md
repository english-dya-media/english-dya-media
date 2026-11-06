# Weekly run: @english_dya

You prepare and schedule next week's Instagram posts for **@english_dya**, an English-pronunciation page for
Persian speakers in Iran, owned by Salar. Everything is posted automatically by **Metricool**
(brand id `7830959`, timezone Europe/Rome). This folder (`studio/`) holds the whole pipeline.

## The format (already approved by the owner, keep it)

- A week runs **Saturday to Friday** (the Iranian week). Day N is published on 3 Nov 2026 + (N−1) days.
- Every day: **1 reel + 4 stories**, all times **Tehran time**:
  - 10:00 story 1, **recall**: a word from yesterday's reel, followers reply with its meaning
  - 13:00 story 2, **quiz**: "which letter is silent?" for a new word (not used before)
  - 17:00 story 3, **mcq**: another word from yesterday's reel, 3 meanings to pick from
  - 21:00 **reel**: 4 words on one pronunciation theme (hook → 4 words → "which one did you say wrong?")
  - 22:00 story 4, **ask**: invite replies (a word they find hard)
- Captions are **Persian only**, informal spoken style (می‌گن، نمیشه، خونده نمیشه), with hashtags (added automatically).
- Reels carry Instagram's AI label (the pronunciation voice is synthetic). `plan.py` sets this.
- The 7-part story series (`make_story.py`, `story_render.py`) is **paused by the owner**. Don't make or post episodes.

## Steps

Work in `studio/`. Run each step, read its output, fix problems before moving on.

1. **Setup**: `bash setup.sh` (installs packages, voice model ~340 MB, fonts, emoji).

2. **Which days**: the last `content/dayNN.json` is the last scheduled day. Next week is days N+1 … N+7 and its
   first date (`python3 -c "from daygen import *; print(day_date(N+1))"`) must be the coming Saturday.
   If those day files already exist (a rerun), skip to step 5 and check Metricool for existing posts before scheduling anything.

3. **Write the week**: copy `weeks/week02.py` to `weeks/weekWW.py` and replace the 7 `write_day(...)` calls.
   - One pronunciation theme per day, 4 words each, everyday words a learner meets (≤ 12 letters).
     Themes that work: a silent letter (b, k, w, l, h, g, t, p, n), stress shifts, words Iranians say the French way
     (biology → «بایالِجی» not «بیولوژی»), -ed endings, odd vowels (women, busy), th sounds, extra syllables
     (comfortable). Don't repeat a theme from the last 3 weeks unless with all-new words.
   - Never reuse a word: `python3 -c "from daygen import used_words; print(sorted(used_words()))"`.
   - `wrong` is the typical Persian-speaker mistake, `right` the US pronunciation in Persian letters (light diacritics:
     ِ َ ُ), `ipa` US IPA, `fa` a short meaning. Use the ZWNJ (`{ZW}`) in می‌، ها، ی (e.g. `f"می{ZW}گن"`).
   - `mark` = indices of the letters to highlight. `SIL("b")` strikes a silent letter; `GLOW(tip, letters)` highlights
     stress/vowels/endings.
   - Stories: recall and mcq must use words from the **previous day's** reel (the checker enforces this; for the
     first day of the week that is last Friday's reel). Vary the mcq answer position. The quiz word must be new and
     have one silent letter. Vary the ask story text (see past weeks).
   - Run `python3 weeks/weekWW.py`. It refuses bad input (lengths, marks, story rules); fix and rerun.

4. **Images**: `python3 fetch_emoji.py`. If a key is not found, pick another Fluent emoji
   (folder names: github.com/microsoft/fluentui-emoji/tree/main/assets). Avoid black/dark emoji (e.g. speaking_head):
   they vanish on the dark background.

5. **Voice**: `python3 tts.py content/dayNN.json` for each day. Compare the printed phonemes with the IPA.
   If a word is wrong, add `ph="<kokoro phonemes>"` to that word (see vegetable in day02) and rerun.

6. **Preview**: `python3 render.py content/dayNN.json --preview` for the 2 days with the longest words/hooks.
   Look at `build/dayNN/preview_*.jpg`. Fix any text that overflows or overlaps, then rerun the week file.

7. **Render**: `python3 render.py content/dayNN.json` for all 7 days (≈75 s each; run in the background).
   Check each `out/dayNN_reel.mp4` is 1080×1920, ~25.6 s, with audio, and look at one frame per reel.

8. **Upload media** to a new branch `media-<first date>` that holds only that week's files. Build it in a fresh,
   empty folder outside the clone (so it carries no history) and push in 3 steps to keep each push small:
   ```
   B=media-2026-11-14                      # first date of the week
   mkdir <empty folder> && cd <empty folder> && git init -q && git checkout -q -b $B
   git config user.name english-dya-media && git config user.email english-dya-media@users.noreply.github.com
   git remote add origin https://github.com/english-dya-media/english-dya-media
   mkdir media && cp <clone>/studio/out/day{12..18}_reel.mp4 <clone>/studio/out/day{12..18}_story*.jpg media/
   git add media/*story* && git commit -qm "Stories" && git push -q origin $B
   git add media/day1[2-5]_reel.mp4 && git commit -qm "Reels 1-4" && git push -q origin $B
   git add media && git commit -qm "Reels 5-7" && git push -q origin $B
   ```
   Check one URL returns 200: `https://raw.githubusercontent.com/english-dya-media/english-dya-media/<branch>/media/dayNN_reel.mp4`.

9. **Schedule**: `python3 plan.py https://raw.githubusercontent.com/english-dya-media/english-dya-media/<branch>/media N+1 N+7 > build/plan.json`.
   First call Metricool `getScheduledPosts` for that date range: if posts already exist there, don't duplicate them.
   Then call `createScheduledPost` once per item with `blogId: "7830959"`, `date: item.date`, `info: item.info` (35 posts).
   Finally `getScheduledPosts` again: expect 35 posts, all PENDING, media copied to static.metricool.com.

10. **Save**: commit `content/` and `weeks/` to `main` (`git fetch origin main` first) and push.

11. **Clean up**: delete media branches whose last day is before today (their posts are published and Metricool keeps its
    own copy): `git push origin --delete media-YYYY-MM-DD`. Never delete the branch of a week that still has posts to go.

12. **Report** (short, English): the 7 themes with their words, first post date/time, anything that failed.

## Rules

- Never publish immediately, edit or delete existing Metricool posts, or change account settings.
- If something fails halfway (e.g. scheduling stops at post 20), stop, don't retry blindly, and report exactly which
  posts were created so nothing is duplicated.
- Keep the visual style and file formats unchanged; the owner approved them.
