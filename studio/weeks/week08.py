"""Week 8: Sat 19 Dec – Fri 25 Dec 2026 (days 47–53): reels, trial reels and quote reels (batch of 14 Nov).
Day 49 (21 Dec) is Yalda night: a Yalda reel and a family quote."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

TH = GLOW(f"صدای {{EN}}: زبون بین دندون{ZW}ها", "th", "tongue")
EDT = GLOW("اینجا {EN} = «ت»", "ed")
OA = lambda tip_en: GLOW("اینجا {EN} = «آ»ی کوتاه", tip_en)

write_day(47,
    hook=H("این ۴ تا کلمه رو", "با", "«ت»", "نگو!", "cross_mark", "نوک زبون بین دندون‌ها، بعد فوت", "tongue"),
    words=[
        W(TH, "thin", "th", "pencil", "✏️", "/θɪn/", "تین", "ثین", "لاغر، نازک"),
        W(TH, "thick", "th", "books", "📚", "/θɪk/", "تیک", "ثیک", "ضخیم، کلفت"),
        W(TH, "throw", "th", "baseball", "⚾", "/θroʊ/", "ترو", "ثْرُو", "پرت کردن"),
        W(TH, "earth", "th", "globe_showing_americas", "🌎", "/ɜːrθ/", "اِرت", "اِرث", "زمین (سیاره)"),
    ],
    cap=("thin و thick رو «تین» و «تیک» نگو ❌", "th یعنی زبون بین دندون‌ها و فوت 👅 برای دوستت بفرست"),
    stories=[
        REC(47, 1),
        QZ("wrote", "w", "memo"),
        MC(47, 0, "تاکسی", "تاکسِی", 2, pron=True),
        AQ("یه کلمه با th که", "مطمئن", "نیستی؟", "ریپلای کن تا تو ریلزهای بعدی\nبا هم تمرینش کنیم", "thumb"),
    ])

write_day(48,
    hook=H("این ۴ تا خوراکی رو", "مثل", "فارسی", "نگو!", "face_with_raised_eyebrow", "انگلیسیشون فرق داره", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «یج»", "age"), "sausage", "age", "hot_dog", "🌭", "/ˈsɔːsɪdʒ/", "سوسیس", "ساسیج", "سوسیس"),
        W(GLOW("اینجا {EN} = «اِی»", "ay"), "mayonnaise", "ay", "sandwich", "🥪", "/ˈmeɪəneɪz/", "مایونِز", "مِیِنِیز", "سس مایونز"),
        W(GLOW("اینجا {EN} شبیه «د»", "tt"), "spaghetti", "tt", "spaghetti", "🍝", "/spəˈɡeɾi/", "اِسپاگِتی", "سْپِگِدی", "اسپاگتی"),
        W(GLOW("اینجا {EN} = «ِر»", "ur"), "yogurt", "ur", "glass_of_milk", "🥛", "/ˈjoʊɡərt/", "یوگورت", "یُوگِرت", "ماست"),
    ],
    cap=("سوسیس و ماست و اسپاگتی به انگلیسی چی میشن؟ 😳", "تلفظ درستشون رو یاد بگیر 🔊 برای دوستت بفرست"),
    stories=[
        REC(48, 2),
        QZV("husband", "s", "man", "«ز»"),
        MC(48, 3, "ماه", "خورشید", 0),
        AQ("اسم کدوم خوراکی رو", "مطمئن", "نیستی؟", "ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی بگم", "croissant"),
    ])

write_day(49,
    hook=H("شب یلدا مبارک!", "این ۴ تا", "کلمه رو", "درست بگو", "watermelon", "هندوونه، انار، شعر و پسته", "red_heart"),
    words=[
        W(GLOW("اینجا {EN} شبیه «د»", "t"), "watermelon", "t", "watermelon", "🍉", "/ˈwɔːɾərmelən/", "واتِرمِلون", "وادِرمِلِن", "هندوانه"),
        W(GLOW("اینجا {EN} = «آ»", "o"), "pomegranate", "o", "gem_stone", "💎", "/ˈpɑːmɪɡrænɪt/", "پومِگرانات", "پامِگرَنِت", "انار"),
        W(GLOW("اینجا {EN} = «اُوِ»", "oe"), "poem", "oe", "feather", "🪶", "/ˈpoʊəm/", "پوئم", "پُوِم", "شعر"),
        W(GLOW("اینجا {EN} = «ش»", "ch"), "pistachio", "ch", "peanuts", "🥜", "/pɪˈstæʃioʊ/", "پیستاچیو", "پیستَشیو", "پسته"),
    ],
    cap=("شب یلدا مبارک 🍉❤️ این ۴ تا کلمه‌ی یلدایی رو درست بگو", "برای کسی که امشب کنارشی بفرست 🤍"),
    stories=[
        REC(49, 3),
        QZ("honor", "h", "sports_medal"),
        MC(49, 2, "اِسپاگِتی", "سْپاگِتی", 1, pron=True),
        AQ("شب یلدا", "چی", "می‌خوری؟", "ریپلای کن تا اسم انگلیسیشو\nبرات بگم 🍉", "nuts"),
    ])

write_day(50,
    hook=H("ed آخر این فعل‌ها", "رو", "«اِد»", "نخون!", "warning", "بعد از p، k و x میشه «ت»", "light_bulb"),
    words=[
        W(EDT, "jumped", "ed", "kangaroo", "🦘", "/dʒʌmpt/", "جامپِد", "جامپت", "پرید"),
        W(EDT, "liked", "ed", "red_heart", "❤️", "/laɪkt/", "لایکِد", "لایکت", "لایک کرد"),
        W(EDT, "fixed", "ed", "hammer_and_wrench", "🛠️", "/fɪkst/", "فیکسِد", "فیکست", "درست کرد"),
        W(EDT, "relaxed", "ed", "relieved_face", "😌", "/rɪˈlækst/", "ریلَکسِد", "ریلَکست", "آروم، ریلکس"),
    ],
    cap=("ed این ۴ تا فعل «اِد» نیست ❌", "بعد از p، k و x ed میشه «ت» 💡 سیو کن"),
    stories=[
        REC(50, 1),
        QZV("dolphin", "ph", "dolphin", "«ف»"),
        MC(50, 2, "داستان", "آهنگ", 1),
        AQ("یه فعل که", "گذشته‌اش", "گیجت می‌کنه؟", "ریپلای کن تا تلفظشو\nتو ریلزهای بعدی بگم", "stopped"),
    ])

write_day(51,
    hook=H("این ۴ تا کلمه رو", "با", "«او»", "نخون!", "cross_mark", "oo و ou این‌جا شبیه «آ»ی کوتاهن", "light_bulb"),
    words=[
        W(OA("oo"), "blood", "oo", "drop_of_blood", "🩸", "/blʌd/", "بلود", "بْلاد", "خون"),
        W(OA("oo"), "flood", "oo", "water_wave", "🌊", "/flʌd/", "فلود", "فْلاد", "سیل"),
        W(OA("ou"), "young", "ou", "baby", "👶", "/jʌŋ/", "یونگ", "یانگ", "جوان"),
        W(OA("ou"), "cousin", "ou", "people_hugging", "🫂", "/ˈkʌzən/", "کوزین", "کازِن", "پسرعمو، دخترخاله…"),
    ],
    cap=("blood رو «بلود» نخون ❌", "oo و ou تو این ۴ تا کلمه شبیه «آ»ی کوتاهن 💡 برای دوستت بفرست"),
    stories=[
        REC(51, 2),
        QZ("leopard", "o", "leopard"),
        MC(51, 0, "دوید", "خندید", 2),
        AQ("یه کلمه با oo", "که", "گیجت می‌کنه؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "door"),
    ])

write_day(52,
    hook=H("اسم این ۴ تا شهر", "رو", "اشتباه", "می‌گی!", "world_map", "انگلیسیش شبیه فارسی نیست", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «آو»", "ow"), "Moscow", "ow", "snowman", "☃️", "/ˈmɑːskaʊ/", "مُسکو", "ماسکاو", "مسکو"),
        W(GLOW("اینجا {EN} = «اَ»", "a"), "Istanbul", "a", "mosque", "🕌", "/ˌɪstænˈbʊl/", "اِستانبول", "ایستَنبُل", "استانبول"),
        W(GLOW("اینجا {EN} = «ث»", "th"), "Athens", "th", "amphora", "🏺", "/ˈæθɪnz/", "آتِن", "اَثِنز", "آتن"),
        W(GLOW("اینجا {EN} = «اِنا»", "enna"), "Vienna", "enna", "violin", "🎻", "/viˈenə/", "وین", "ویِنا", "وین"),
    ],
    cap=("وین به انگلیسی میشه Vienna 😳", "اسم این ۴ تا شهر رو این‌جوری بگو 🌍 برای دوستت بفرست"),
    stories=[
        REC(52, 1),
        QZV("alphabet", "ph", "input_latin_letters", "«ف»"),
        MC(52, 2, "پیر", "قوی", 1),
        AQ("اسم کدوم شهر رو", "مطمئن", "نیستی؟", "ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی بگم", "Prague"),
    ])

write_day(53,
    hook=H("این ۴ تا کلمه رو", "مثل", "فارسی", "نخون!", "face_with_raised_eyebrow", "انگلیسی‌ها یه جور دیگه می‌گن",
           "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} شبیه «د»", "t"), "data", "t", "bar_chart", "📊", "/ˈdeɪɾə/", "دیتا", "دِیدا", "داده‌ها"),
        W(GLOW("اینجا {EN} = «اِی»", "a"), "label", "a", "label", "🏷️", "/ˈleɪbəl/", "لیبل", "لِیبِل", "برچسب"),
        W(GLOW("اینجا {EN} = «آ»", "o"), "model", "o", "dress", "👗", "/ˈmɑːdəl/", "مُدِل", "مادِل", "مدل"),
        W(GLOW("اینجا {EN} شبیه «د»", "t"), "motor", "t", "gear", "⚙️", "/ˈmoʊɾər/", "موتور", "مُودِر", "موتور"),
    ],
    cap=("دیتا و موتور به انگلیسی چی میشن؟ 😳", "این ۴ تا رو مثل فارسی نخون 🔊 برای دوستت بفرست"),
    stories=[
        REC(53, 3, pron=True),
        QZ("science", "c", "test_tube"),
        MC(53, 1, "اِستانبول", "استانبُل", 0, pron=True),
        AQ("یه کلمه که فارسی", "هم", "داریمش؟", "ریپلای کن تا تلفظ انگلیسیشو\nتو ریلزهای بعدی بگم", "video"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
SEND = "برای دوستت بفرست که اونم یاد بگیره 👇"

write_trial(47, "vocab", [
    dict(wrong="very cute", right="adorable", note="یعنی «خیلی بامزه، ناز»", emoji="smiling_face_with_hearts"),
    dict(wrong="very scary", right="terrifying", note="یعنی «وحشتناک، خیلی ترسناک»", emoji="ghost"),
    dict(wrong="very upset", right="devastated", note="یعنی «داغون، از پا افتاده»", emoji="broken_heart"),
    dict(wrong="very worried", right="anxious", note="یعنی «خیلی نگران، مضطرب»", emoji="anxious_face_with_sweat"),
], ("به جای very این ۴ تا کلمه رو بگو 😎", SAVE), suffix="a")
write_trial(47, "mistakes", [
    dict(wrong="I want go.", right="I want to go.", note="بعد از want حرف to لازمه", emoji="person_walking"),
    dict(wrong="I need sleep now.", right="I need to sleep.", note="بعد از need (فعل) to میاد", emoji="sleeping_face"),
    dict(wrong="I'd like eat.", right="I'd like to eat.", note="بعد از would like هم to میاد", emoji="fork_and_knife_with_plate"),
], ("این ۳ تا جمله یه to کم دارن ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(48, "vocab", [
    dict(wrong="It's very cold.", right="It's freezing out.", note="یعنی «بیرون یخبندونه»", emoji="cold_face"),
    dict(wrong="It's raining a lot.", right="It's pouring.", note="یعنی «داره شُرشُر می‌باره»", emoji="cloud_with_rain"),
    dict(wrong="It's very hot.", right="It's boiling today.", note="یعنی «امروز داغِ داغه»", emoji="hot_face"),
    dict(wrong="very bad weather", right="nasty weather", note="یعنی «هوای خیلی بد»", emoji="cloud_with_lightning_and_rain"),
], ("درباره‌ی هوا مثل بومی‌ها حرف بزن 🌧️", SAVE), suffix="a")
write_trial(48, "mistakes", [
    dict(wrong="homeworks", right="homework", note="homework جمع نمی‌بنده", emoji="memo"),
    dict(wrong="luggages", right="luggage", note="luggage همیشه مفرده", emoji="luggage"),
    dict(wrong="moneys", right="money", note="money هم s نمی‌گیره", emoji="money_bag"),
], ("این ۳ تا کلمه هیچ‌وقت s نمی‌گیرن ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(49, "vocab", [
    dict(wrong="Good night.", right="Sweet dreams!", note="یعنی «خوابای خوب ببینی»", emoji="crescent_moon"),
    dict(wrong="Go to sleep.", right="Hit the sack.", note="یعنی «برو بخواب»", emoji="bed"),
    dict(wrong="Wake up!", right="Rise and shine!", note="یعنی «پاشو، صبح شده»", emoji="sunrise"),
    dict(wrong="I'm going to sleep.", right="I'm going to crash.", note="یعنی «دارم بیهوش میشم از خستگی»", emoji="sleeping_face"),
], ("شب و صبح رو مثل بومی‌ها بگو 🌙", SEND), suffix="a")
write_trial(49, "mistakes", [
    dict(wrong="This night", right="Tonight", note="«امشب» میشه tonight", emoji="night_with_stars"),
    dict(wrong="Tell to me.", right="Tell me.", note="بعد از tell، to نمیاد", emoji="speech_balloon"),
    dict(wrong="Call to me.", right="Call me.", note="بعد از call هم to نمیاد", emoji="telephone_receiver"),
], ("امشب این ۳ تا رو اشتباه نگو ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(50, "vocab", [
    dict(wrong="eat quickly", right="gobble", note="یعنی «هول‌هولکی خوردن»", emoji="hamburger"),
    dict(wrong="drink slowly", right="sip", note="یعنی «جرعه‌جرعه خوردن»", emoji="hot_beverage"),
    dict(wrong="laugh quietly", right="giggle", note="یعنی «ریز ریز خندیدن»", emoji="smiling_face_with_smiling_eyes"),
    dict(wrong="cry loudly", right="sob", note="یعنی «هق‌هق گریه کردن»", emoji="loudly_crying_face"),
], ("به جای eat و laugh این فعل‌های دقیق رو بگو 😎", SAVE), suffix="a", headline="فعل دقیق‌تر بگو", head_emoji="bullseye")
write_trial(50, "mistakes", [
    dict(wrong="My actual job", right="My current job", note="actual یعنی واقعی، نه فعلی", emoji="briefcase"),
    dict(wrong="I'm sensible.", right="I'm sensitive.", note="«حساسم» میشه sensitive", emoji="pleading_face"),
    dict(wrong="Control the tickets.", right="Check the tickets.", note="«بررسی کردن» میشه check", emoji="ticket"),
], ("این ۳ تا کلمه اون معنی‌ای که فکر می‌کنی نیستن ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(51, "vocab", [
    dict(wrong="Let me pay.", right="It's on me.", note="یعنی «مهمون من»", emoji="money_with_wings"),
    dict(wrong="How much is it?", right="What's the damage?", note="یعنی «چقدر شد؟» (خودمونی)", emoji="receipt"),
    dict(wrong="I want to pay.", right="Check, please!", note="یعنی «صورتحساب لطفاً»", emoji="credit_card"),
    dict(wrong="Give me a coffee.", right="Can I get a coffee?", note="یعنی «یه قهوه می‌دید؟»", emoji="hot_beverage"),
], ("تو کافه این‌جوری حرف بزن ☕", SAVE), suffix="a")
write_trial(51, "mistakes", [
    dict(wrong="I don't. – Me too.", right="Me neither.", note="بعد از جمله‌ی منفی میشه me neither", emoji="person_gesturing_no"),
    dict(wrong="Both of us is ready.", right="Both of us are ready.", note="both جمعه؛ are لازمه", emoji="people_hugging"),
    dict(wrong="Everyone are here.", right="Everyone is here.", note="everyone مفرده؛ is میاد", emoji="busts_in_silhouette"),
], ("این ۳ تا رو تقریباً همه اشتباه می‌گن 😬", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(52, "vocab", [
    dict(wrong="post", right="mail", note="یعنی «پست، نامه» به آمریکایی", emoji="envelope"),
    dict(wrong="tap", right="faucet", note="یعنی «شیر آب» به آمریکایی", emoji="droplet"),
    dict(wrong="car park", right="parking lot", note="یعنی «پارکینگ» به آمریکایی", emoji="automobile"),
    dict(wrong="underground", right="subway", note="یعنی «مترو» به آمریکایی", emoji="metro"),
], ("این ۴ تا کلمه رو آمریکایی بگو 🇺🇸", SAVE), suffix="a", headline="آمریکایی حرف بزن")
write_trial(52, "mistakes", [
    dict(wrong="Repeat again.", right="Repeat that.", note="repeat خودش یعنی «دوباره بگو»", emoji="repeat_button"),
    dict(wrong="Return back.", right="Come back.", note="return یعنی برگشتن؛ back اضافه‌ست", emoji="right_arrow_curving_left"),
    dict(wrong="Enter inside.", right="Come in.", note="enter یعنی وارد شدن؛ inside اضافه‌ست", emoji="door"),
], ("این ۳ تا جمله یه کلمه‌ی اضافه دارن ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(53, "vocab", [
    dict(wrong="rarely", right="once in a blue moon", note="یعنی «به ندرت، سالی یه بار»", emoji="full_moon"),
    dict(wrong="tell a secret", right="spill the beans", note="یعنی «رازو لو دادن»", emoji="shushing_face"),
    dict(wrong="start talking", right="break the ice", note="یعنی «یخِ جمع رو شکستن»", emoji="ice"),
    dict(wrong="in trouble", right="in hot water", note="یعنی «تو دردسر»", emoji="hot_springs"),
], ("این اصطلاح‌ها رو بومی‌ها هر روز می‌گن 😎", SAVE), suffix="a", headline="اصطلاح‌هایی که بومی‌ها می‌گن",
   head_emoji="speech_balloon")
write_trial(53, "mistakes", [
    dict(wrong="The trip was funny.", right="The trip was fun.", note="fun = خوش‌گذرون؛ funny = خنده‌دار", emoji="airplane"),
    dict(wrong="I'm hearing music.", right="I'm listening to music.", note="با دقت گوش دادن = listen to", emoji="headphone"),
    dict(wrong="I see TV.", right="I watch TV.", note="تلویزیون رو watch می‌کنن", emoji="television"),
], ("این ۳ تا رو با هم قاطی نکن ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(47, "Be the reason someone smiles today.",
            "امروز دلیل لبخند یه نفر باش.",
            [("reason", "دلیل")], "برای کسی که لبخندت می‌کنه بفرست 🤍", topic="kindness", figure=True)
write_quote(48, "Every winter turns into spring.",
            "هر زمستونی بالاخره بهار میشه.",
            [("turns into", "تبدیل میشه به")], "برای کسی که منتظر بهاره بفرست 🌸", topic="hope")
write_quote(49, "Long nights are shorter with the people you love.",
            "شبای بلند، کنار کسایی که دوستشون داری کوتاه‌تر میشن.",
            [("shorter", "کوتاه‌تر")], "شب یلدا مبارک 🍉 برای عزیزانت بفرست", topic="family", palette="night")
write_quote(50, "The best time to start was yesterday. The next best time is now.",
            "بهترین زمان برای شروع دیروز بود؛ بهترینِ بعدی همین الانه.",
            [("start", "شروع کردن")], "سیو کن 📌", topic="time", sea=True)
write_quote(51, "Your fear is smaller than you think.",
            "ترست از چیزی که فکر می‌کنی کوچیک‌تره.",
            [("fear", "ترس")], "برای کسی که می‌ترسه شروع کنه بفرست 💪", topic="courage", figure=True)
write_quote(52, "New beginnings often start with small decisions.",
            "شروع‌های تازه معمولاً با تصمیم‌های کوچیک شروع میشن.",
            [("beginnings", "شروع‌ها"), ("decisions", "تصمیم‌ها")], "سیو کن 📌", topic="change")
write_quote(53, "Happiness is a warm cup of tea on a cold day.",
            "خوشبختی یعنی یه چای داغ تو یه روز سرد.",
            [("warm", "گرم")], "برای کسی که باهاش چای می‌خوری بفرست ☕", topic="happiness", sea=True)
