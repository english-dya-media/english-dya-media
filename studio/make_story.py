"""Week 1 story: «قاشق گمشده» (The Missing Spoon), household items. Writes content/story_w01.json."""
import json

ZW = "‌"

story = {
    "week": 1,
    "theme": "household",
    "series_fa": "قاشق گمشده",
    "series_en": "The Missing Spoon",
    "characters": {
        "teapot": {"img": "teapot", "name_fa": "خانم قوری", "name_en": "Mrs. Teapot", "voice": "bf_emma", "lang": "en-gb",
                   "speed": 1.0, "color": "#E8457A",
                   # face placement in fractions of the image box
                   "eyes": [[0.40, 0.58], [0.61, 0.58]], "eye": 0.115, "mouth": [0.505, 0.73], "mw": 0.16},
        "mug": {"img": "hot_beverage", "name_fa": "کارآگاه ماگ", "name_en": "Detective Mug", "voice": "bm_george", "lang": "en-gb",
                "speed": 0.95, "color": "#6C5CE7",
                "eyes": [[0.41, 0.645], [0.585, 0.645]], "eye": 0.105, "mouth": [0.50, 0.765], "mw": 0.13, "hat": True},
    },
    "outline": [
        "Mrs. Teapot finds Little Spoon missing; Detective Mug finds a bubbly footprint.",
        "Suspect: Sponge. 'I clean things, I don't steal them!' Old Clock heard a noise at midnight.",
        "Old Clock: the drawer opened at midnight. The drawer key belongs to Salt.",
        "Grumpy Salt: 'I'm salty, not a thief!' His key is gone too. A shadow moves behind the fridge.",
        "Behind the fridge: a trail of sugar... and Knife says: 'You're too late.'",
        "Twist: Knife was helping Spoon. Spoon is planning something big for tonight.",
        "Little Spoon throws a surprise birthday party for Mrs. Teapot. Case closed!",
    ],
    "episodes": [
        {
            "ep": 1,
            "part_fa": "قسمت ۱ از ۷",
            "hook_fa": "کی قاشق کوچولو رو برده؟",
            "hook_en": "Who took Little Spoon?",
            "lines": [
                {"who": "teapot", "mood": "worried", "en": "Help! My little Spoon is *missing*!",
                 "fa": "کمک! قاشق کوچولوی من گم شده!"},
                {"who": "mug", "mood": "calm", "en": "Don't worry, Mrs. Teapot. I'm Detective Mug.",
                 "fa": "نگران نباشید خانم قوری. من کارآگاه ماگ هستم."},
                {"who": "teapot", "mood": "worried", "en": "He was in the drawer last night!",
                 "fa": "دیشب توی کشو بود!"},
                {"who": "mug", "mood": "thinking", "en": "Hmm... every mystery has a *clue*.",
                 "fa": "هوم... هر معمایی یه سرنخ داره.", "prop": "glass"},
                {"who": "mug", "mood": "surprised", "en": "Look! A wet *footprint*... full of bubbles!",
                 "fa": "نگاه کنید! یه ردپای خیس... پر از حباب!", "prop": "footprints", "look": "down"},
                {"who": "teapot", "mood": "shocked", "en": "Bubbles? But who...?",
                 "fa": "حباب؟ ولی کی...؟", "prop": "shock"},
            ],
            "tbc_fa": "ادامه دارد...",
            "next_fa": "قسمت ۲: فردا",
            "vocab_title": f"لغت{ZW}های این قسمت",
            "vocab": [["missing", f"گم{ZW}شده"], ["clue", "سرنخ"], ["footprint", "ردپا"]],
            "cta_fa": "به نظرت کار کیه؟ کامنت کن",
            "caption": "\n".join([
                "قاشق گمشده 🥄 | قسمت ۱ از ۷",
                f"قاشق کوچولوی خانم قوری گم شده و کارآگاه ماگ دنبال سرنخه 🕵️",
                "",
                f"لغت{ZW}های این قسمت:",
                f"🔎 missing = گم{ZW}شده",
                "🔎 clue = سرنخ",
                "🔎 footprint = ردپا",
                "",
                f"به نظرت کار کیه؟ تو کامنت بنویس 👇",
                f"قسمت ۲ فردا، فالو کن که از دستت نره 🔔",
                "",
                f"#داستان_انگلیسی #زبان_انگلیسی #آموزش_زبان_انگلیسی #لغت_انگلیسی #یادگیری_زبان",
            ]),
        }
    ],
}

json.dump(story, open("content/story_w01.json", "w"), ensure_ascii=False, indent=1)
for l in story["episodes"][0]["lines"]:
    print(f"{l['who']:7s} {l['en']:48s} | {l['fa']}")
