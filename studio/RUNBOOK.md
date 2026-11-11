# Runbook: @english_dya

**@english_dya** is an Instagram page teaching English words and pronunciation to Persian speakers in Iran, owned by Salar.
Everything is posted automatically by **Metricool** (brand id `7830959`, timezone Europe/Rome). This folder (`studio/`)
holds the whole pipeline. The owner's goal: **+5,000 followers every month**. The page was losing followers when we
started, so every week is built from what the numbers say (`growth/`).

Two scheduled jobs use this file: the **weekly run** (Thursdays, makes and schedules the next Saturday–Friday) and the
**daily check** (every day, monitors and logs). Each has its own section below.

## The format (keep it)

- A week runs **Saturday to Friday** (the Iranian week). Day N is published on 3 Nov 2026 + (N−1) days.
- Every day, all times **Tehran time** (plan.py converts them):
  - 10:00 story 1, **recall**: a word from yesterday's reel, followers reply with its meaning
  - 13:00 story 2, **quiz**: "which letter is silent?" for a new word (not used before)
  - 15:00 **trial reel a**, *vocab*: 4 basic phrases → a stronger word (very tired → exhausted), with the Persian meaning
  - 17:00 story 3, **mcq**: another word from yesterday's reel, 3 meanings to pick from
  - 19:00 **trial reel b**, *mistakes*: 3 sentences Persian speakers get wrong (I am agree → I agree) + a one-line why
  - 21:00 **reel**: 4 words on one pronunciation theme (hook banner, 4 words, "which one did you say wrong?")
  - 22:00 story 4, **ask**: invite replies (a word they find hard)
  - 23:00 **quote reel**: a short English quote on a generated night/sunset landscape, then its Persian meaning, over
    calm music (`quote_render.py`, ~6–8 s). Owner's choice: **music only, no voice, no word meanings in the video**;
    the 1–2 key words and their meanings go in the caption only. Made to be sent to friends; the late-night slot is
    when quote pages get shared most. Not AI-labelled (no synthetic voice).
- **Trial reels** are Instagram "Trial Reels": shown only to non-followers at first. They are how new people find the page,
  so they must be useful enough to share or save. Rendered by `trial_render.py` (~17–20 s).
- The daily reel uses layout **v2** (from day 12): no text-only intro, the first word is on screen and spoken from frame 0,
  the hook rides as a banner on top, 19.6 s long. Don't bring back the old 2.4 s hook scene: viewers left during it.
- Captions are **Persian only**, informal spoken style (می‌گن، نمیشه، خونده نمیشه), with hashtags (added automatically).
- Reels and trial reels carry Instagram's AI label (the voice is synthetic); quote reels don't. `plan.py` sets this.
- The 7-part story series (`make_story.py`, `story_render.py`) is **paused by the owner**. Don't make or post episodes.

## Weekly run

Work in `studio/`. Run each step, read its output, fix problems before moving on.

1. **Setup**: `bash setup.sh` (installs packages, voice model ~340 MB, fonts, emoji).

2. **Which days**: the last `content/dayNN.json` is the last scheduled day. Next week is days N+1 … N+7 and its
   first date (`python3 -c "from daygen import *; print(day_date(N+1))"`) must be the coming Saturday.
   If those day files already exist (a rerun), skip to step 6 and check Metricool for existing posts before scheduling anything.

3. **Read the numbers**: `python3 growth/update.py` and `growth/learnings.md`. Let them steer the week: more themes like
   the best reels, none like the worst; if one trial format has clearly beaten the other for a week (about 2× the views),
   use that format in both trial slots (pass `slot="15:00"` / `slot="19:00"` and suffixes "a"/"b" as usual).

4. **Write the week**: copy `weeks/week02.py` to `weeks/weekWW.py` and replace the 7 `write_day(...)` calls; then add the
   trial reels (see `weeks/week02_trials.py` for the shape): for each day `write_trial(N, "vocab", [...4 items], (line1, line2), suffix="a")`
   and `write_trial(N, "mistakes", [...3 items], (line1, line2), suffix="b")`.
   - Daily reels: one pronunciation theme per day, 4 words each, everyday words a learner meets (≤ 12 letters).
     Themes that work: sounds Iranians replace (th, w/v), silent letters (b, k, w, l, h, g, t, p, n), stress shifts,
     -ed endings, odd vowels (women, busy), extra syllables (comfortable). Avoid long academic words (they flopped).
     Don't repeat a theme from the last 3 weeks unless with all-new words.
   - Never reuse a word: `python3 -c "from daygen import used_words; print(sorted(used_words()))"`.
   - `wrong` is the typical Persian-speaker mistake, `right` the US pronunciation in Persian letters (light diacritics:
     ِ َ ُ), `ipa` US IPA, `fa` a short meaning. Use the ZWNJ (`{ZW}`) in می‌، ها، ی (e.g. `f"می{ZW}گن"`).
   - `mark` = indices of the letters to highlight. `SIL("b")` strikes a silent letter; `GLOW(tip, letters)` highlights
     stress/vowels/endings.
   - Stories: recall and mcq must use words from the **previous day's** reel (the checker enforces this; for the
     first day of the week that is last Friday's reel). Vary the mcq answer position. The quiz word must be new and
     have one silent letter. Vary the ask story text (see past weeks).
   - Trial *mistakes*: real errors that come from translating Persian word by word (I am agree, I have 25 years old,
     He said me, Open the light, My mother is teacher, I'm boring/bored, more better, How it is?, I didn't went…),
     correct natural English, sentences ≤ 22 characters, `note` ≤ 36 characters of Persian explaining why.
   - Trial *vocab*: very X → one strong word (exhausted, starving, terrified, freezing, gorgeous…), or a basic phrase →
     what natives say (I don't know → I have no idea). `note` = «یعنی «…» with the Persian meaning.
   - Trial captions: line 1 a hook, line 2 a share or save prompt (برای دوستت بفرست، سیو کن). Never reuse a `right`
     (`write_trial` refuses). Every `emoji` must be a Fluent emoji (step 5).
   - Quote reels (see `weeks/week02_quotes.py`): for each day `write_quote(N, en, fa, [(word, meaning)], share_line,
     author=None, palette=None, figure=False, sea=False)`. The word meanings appear only in the caption. A short line (≤ 110 characters) in simple English that
     people would send to a friend: calm, hopeful, about life, effort, people, peace of mind. The Persian is a natural,
     warm translation (spoken style is fine), not word for word. 1–2 key words a learner should know, with meanings.
     Use your own lines, common sayings or proverbs, or well-attested lines of long-dead authors (Seneca, Marcus
     Aurelius, Emerson, Thoreau…). Never song lyrics, film lines or lines from modern books; nothing political or
     religious; add `author` only when the attribution is certain (proverbs: "Japanese proverb" etc.).
     The palette rotates by itself; set `figure=True` (a small person on the hill) or `sea=True` on some days for variety.
   - Run `python3 weeks/weekWW.py`. It refuses bad input (lengths, marks, story rules, reused items); fix and rerun.

5. **Images**: `python3 fetch_emoji.py`. If a key is not found, pick another Fluent emoji
   (folder names: github.com/microsoft/fluentui-emoji/tree/main/assets). Avoid black/dark emoji (e.g. speaking_head):
   they vanish on the dark background.

6. **Voice**: `python3 tts.py content/dayNN.json` for each day. Compare the printed phonemes with the IPA.
   If a word is wrong, add `ph="<kokoro phonemes>"` to that word (see vegetable in day02) and rerun.

7. **Preview**: `python3 render.py content/dayNN.json --fit-check` for every day. It lists any line wider than the
   safe area (the renderer shrinks those automatically, but a listed line is better shortened in the week file).
   Then `python3 render.py content/dayNN.json --preview` for the 2 days with the longest words/hooks, and
   `python3 trial_render.py content/trialNNx.json --preview` for one vocab and one mistakes file, and
   `python3 quote_render.py content/quoteNN.json --preview` for the longest quote; look at
   `build/<tag>/prev*.jpg`. Fix anything that overlaps, then rerun the week file.
   (`render.py … --stories` re-renders only a day's 4 story images.)

8. **Render** (run in the background, a few at a time):
   - `python3 render.py content/dayNN.json` for all 7 days (≈60 s each) → `out/dayNN_reel.mp4` (~19.6 s) + 4 stories.
   - `python3 trial_render.py content/trialNNa.json` and `…b.json` for all 14 → `out/trialNNa.mp4` etc. (~45 s each).
   - `python3 quote_render.py content/quoteNN.json` for all 7 → `out/quoteNN.mp4` (~30 s each).
   Check each video is 1080×1920 with audio, and look at one frame of each kind.

9. **Upload media** to a new branch `media-<first date>` that holds only that week's files. Build it in a fresh,
   empty folder outside the clone (so it carries no history) and push in steps to keep each push small:
   ```
   B=media-2026-11-14                      # first date of the week
   mkdir <empty folder> && cd <empty folder> && git init -q && git checkout -q -b $B
   git config user.name english-dya-media && git config user.email english-dya-media@users.noreply.github.com
   git remote add origin https://github.com/english-dya-media/english-dya-media
   mkdir media && cp <clone>/studio/out/day{12..18}_reel.mp4 <clone>/studio/out/day{12..18}_story*.jpg <clone>/studio/out/trial1[2-8]*.mp4 <clone>/studio/out/quote1[2-8].mp4 media/
   git add media/*story* && git commit -qm "Stories" && git push -q origin $B
   git add media/quote*.mp4 && git commit -qm "Quote reels" && git push -q origin $B
   git add media/day*_reel.mp4 && git commit -qm "Reels" && git push -q origin $B
   git add media/trial*a.mp4 && git commit -qm "Trial reels a" && git push -q origin $B
   git add media && git commit -qm "Trial reels b" && git push -q origin $B
   ```
   Check one URL of each kind returns 200: `https://raw.githubusercontent.com/english-dya-media/english-dya-media/<branch>/media/<file>`.

10. **Schedule**: `python3 plan.py https://raw.githubusercontent.com/english-dya-media/english-dya-media/<branch>/media N+1 N+7 > build/plan.json`.
    First call Metricool `getScheduledPosts` for that date range: if posts already exist there, don't duplicate them.
    Then call `createScheduledPost` once per item with `blogId: "7830959"`, `date: item.date`, `info: item.info`
    (56 posts: 7 reels, 7 quote reels, 14 trial reels, 28 stories). Finally `getScheduledPosts` again: expect all of
    them PENDING, media copied to static.metricool.com, trial reels with type TRIAL_REEL.

11. **Save**: commit `content/` and `weeks/` to `main` (`git fetch origin main` and rebase first; the daily check also
    pushes to main) and push.

12. **Clean up**: delete media branches whose last day is before today (their posts are published and Metricool keeps its
    own copy): `git push origin --delete media-YYYY-MM-DD`. Never delete the branch of a week that still has posts to go.

13. **Report** (short, English): the 7 themes with their words, the trial reel topics, the 7 quotes, first post date/time,
    anything that failed.

## Daily check

Monitoring only: no new content. Work in `studio/` (no setup needed). "Now" is the Rome time when you run.

1. **Did yesterday's posts go out?** `getScheduledPosts` from yesterday 00:00 to now (Rome, `extendedRange` false).
   Every post whose time has passed should be PUBLISHED. For a post in ERROR (or still PENDING over an hour after its
   time): schedule it again once with `createScheduledPost` — same media (its static.metricool.com URL), text and
   instagramData type, `autoPublish` true, at least 20 minutes from now and not within 30 minutes of another post.
   Never touch posts that are PUBLISHED or still in the future. Don't repost something already re-posted the day before.

2. **Pull the numbers** with `getAnalyticsDataByMetrics` (brand 7830959):
   - followers, from 8 days ago to today: `IGEV01` followers, `IGEV43` gained, `IGEV44` lost, `IGEV06` reach.
     Each row is `[followers, gained, lost, reach, "YYYYMMDD"]`; the latest days are often null (not in yet).
   - reels, from 15 days ago to today: `IGRE02` published (UTC yyyyMMddHHmmss), `IGRE06` url, `IGRE11` reach,
     `IGRE23` views, `IGRE10` likes, `IGRE07` comments, `IGRE12` saves, `IGRE21` shares, `IGRE24` avg watch (s),
     `IGRE28` view rate (%, viewers past 3 s).
   - Tag each reel by matching its url with `publicUrl` of the published posts (`getScheduledPosts` over the same 15
     days, or the time if no match: daily reels go out at 21:00 Tehran, trial reels at 15:00/19:00): `dayNN` + kind
     `reel` for daily reels, `trialNN…` + kind `trial` for trial reels, `quoteNN` + kind `quote` for quote reels
     (23:00 Tehran; the media file name says which), anything else kind `promo` with a short tag (e.g. `presenter`).
   - Write them to `build/today.json` in the format at the top of `growth/update.py` and run
     `python3 growth/update.py build/today.json`. Its report has the month-to-date gain against the 5,000 goal.

3. **Learn**: update `growth/learnings.md` (keep it under ~40 lines, keep its sections): the best and worst reels of the
   last 14 days with theme/format and numbers, how trial reels compare with daily reels, and 1–3 concrete instructions
   for the next weekly run. Only claim what the numbers show. Add a line to "Changes made" only if something changed.

4. **Save**: commit `growth/` to `main` (`git pull --rebase origin main` first) and push.

5. **Message** (the final reply goes to Salar's phone; English, at most 4 short lines): followers and yesterday's change,
   month-to-date vs +5,000 and the daily pace needed, yesterday's best reel (views, view rate), and any post that failed
   or was re-scheduled.

## Rules

- Never publish immediately, edit or delete existing Metricool posts, or change account settings. (The one exception:
  the daily check re-schedules a post that failed, as a new post.)
- If something fails halfway (e.g. scheduling stops at post 20), stop, don't retry blindly, and report exactly which
  posts were created so nothing is duplicated.
- Keep the visual style and file formats; the owner approved them.
- Don't spend money (no boosts or ads) unless Salar asks for it.
