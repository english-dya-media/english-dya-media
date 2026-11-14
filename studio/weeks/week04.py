"""Week 4: Sat 21 Nov – Fri 27 Nov 2026 (days 19–25): reels, trial reels and quote reels in one file.
Written on 14 Nov with weeks 5–16 in one batch (owner's request: three months ahead). Steered by growth/learnings.md:
sounds Iranians replace (th), rule-based sounds (-ed, American t), odd vowels, names said the English way;
one silent-letter reel at most every other week; quiz stories now also ask which letter makes a sound."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

TH = GLOW(f"صدای {{EN}}: زبون بین دندون{ZW}ها", "th", "tongue")
FL = GLOW("اینجا {EN} شبیه «د»", "t")
EDT = GLOW("اینجا {EN} = «ت»", "ed")

write_day(19,
    hook=H("این ۴ تا کلمه رو", "آمریکایی", "بگو", "t میشه «د»!", "speaker_high_volume",
           "t بین دو صدادار نرم میشه", "light_bulb"),
    words=[
        W(FL, "water", "t", "droplet", "💧", "/ˈwɑːɾər/", "واتِر", "وادِر", "آب"),
        W(FL, "city", "t", "cityscape", "🏙️", "/ˈsɪɾi/", "سیتی", "سیدی", "شهر"),
        W(FL, "better", "tt", "thumbs_up", "👍", "/ˈbeɾər/", "بِتِر", "بِدِر", "بهتر"),
        W(FL, "party", "t", "party_popper", "🎉", "/ˈpɑːrɾi/", "پارتی", "پاردی", "مهمانی"),
    ],
    cap=("آمریکایی‌ها t این ۴ تا کلمه رو «د» می‌گن 🇺🇸", "واسه همینه که water رو «وادِر» می‌شنوی 💡 سیو کن"),
    stories=[
        REC(19, 3),
        QZ("knot", "k", "knot"),
        MC(19, 0, "گوش داد", "خوابید", 1),
        AQ("یه کلمه با t وسطش", "که", "سخته؟", "ریپلای کن تا تلفظ آمریکاییشو\nتو ریلزهای بعدی بگم", "butter"),
    ])

write_day(20,
    hook=H("این ۴ تا کلمه رو", "با", "«ای»", "نخون!", "cross_mark", "ea و eigh این‌جا میشن «اِی»", "light_bulb"),
    words=[
        W(GLOW("اینجا {EN} = «اِی»", "ea"), "great", "ea", "glowing_star", "🌟", "/ɡreɪt/", "گریت", "گْرِیت", "عالی، بزرگ"),
        W(GLOW("اینجا {EN} = «اِی»", "ea"), "break", "ea", "broken_heart", "💔", "/breɪk/", "بریک", "بْرِیک", "شکستن؛ استراحت"),
        W(GLOW("اینجا {EN} = «اِی»", "ea"), "steak", "ea", "cut_of_meat", "🥩", "/steɪk/", "استیک", "سْتِیک", "استیک"),
        W(GLOW("اینجا {EN} = «اِی»", "eigh"), "weight", "eigh", "balance_scale", "⚖️", "/weɪt/", "وایت", "وِیت", "وزن"),
    ],
    cap=("great و steak رو با «ای» نخون ❌", "ea و eigh تو این ۴ تا کلمه میشن «اِی» 💡 برای دوستت بفرست"),
    stories=[
        REC(20, 0),
        QZV("music", "s", "musical_note", "«ز»"),
        MC(20, 3, "تولد", "عروسی", 0),
        AQ("یه کلمه با ea", "که", "گیجت می‌کنه؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "bread"),
    ])

write_day(21,
    hook=H("این ۴ تا کلمه رو", "با", "«ت»", "نگو!", "cross_mark", "زبونتو بذار بین دندونات", "tongue"),
    words=[
        W(TH, "thank", "th", "folded_hands", "🙏", "/θæŋk/", "تَنک", "ثَنک", "تشکر کردن"),
        W(TH, "thirsty", "th", "cup_with_straw", "🥤", "/ˈθɜːrsti/", "تِرستی", "ثِرستی", "تشنه"),
        W(TH, "tooth", "th", "tooth", "🦷", "/tuːθ/", "توت", "توث", "دندان"),
        W(TH, "birthday", "th", "birthday_cake", "🎂", "/ˈbɜːrθdeɪ/", "بِرتدِی", "بِرثدِی", "تولد"),
    ],
    cap=("th این ۴ تا کلمه «ت» نیست ❌", "زبونتو بذار بین دندونات و فوت کن 👅 برای دوستت بفرست"),
    stories=[
        REC(21, 0),
        QZ("knit", "k", "yarn"),
        MC(21, 3, "قد", "سرعت", 2),
        AQ("یه کلمه با th که", "تلفظش", "سخته؟", "ریپلای کن تا تو ریلزهای بعدی\nبا هم تمرینش کنیم", "thirteen"),
    ])

write_day(22,
    hook=H("ed آخر این فعل‌ها", "رو", "«اِد»", "نخون!", "warning", "بعد از k، p، s و ch میشه «ت»", "light_bulb"),
    words=[
        W(EDT, "worked", "ed", "briefcase", "💼", "/wɜːrkt/", "وُرکِد", "وِرکت", "کار کرد"),
        W(EDT, "cooked", "ed", "cooking", "🍳", "/kʊkt/", "کوکِد", "کُکت", "آشپزی کرد"),
        W(EDT, "helped", "ed", "handshake", "🤝", "/helpt/", "هِلپِد", "هِلپت", "کمک کرد"),
        W(EDT, "danced", "ed", "woman_dancing", "💃", "/dænst/", "دَنسِد", "دَنست", "رقصید"),
    ],
    cap=("ed این ۴ تا فعل «اِد» نیست ❌", "بعد از صداهای k، p، s و ch آخرش میشه «ت» 💡 سیو کن"),
    stories=[
        REC(22, 1),
        QZV("easy", "s", "smiling_face_with_sunglasses", "«ز»"),
        MC(22, 0, "عذرخواهی کردن", "خداحافظی کردن", 2),
        AQ("یه فعل که", "گذشته‌اش", "گیجت می‌کنه؟", "ریپلای کن تا تلفظشو\nتو ریلزهای بعدی بگم", "watched"),
    ])

write_day(23,
    hook=H("این ۴ تا کلمه رو", "با", "«ا»", "نخون!", "cross_mark", "u این‌جا یه «اُ»ی کوتاهه", "light_bulb"),
    words=[
        W(GLOW("اینجا {EN} = «اُ»", "u"), "put", "u", "package", "📦", "/pʊt/", "پات", "پُت", "گذاشتن"),
        W(GLOW("اینجا {EN} = «اُ»", "u"), "push", "u", "shopping_cart", "🛒", "/pʊʃ/", "پاش", "پُش", "هل دادن"),
        W(GLOW("اینجا {EN} = «اُ»", "u"), "pull", "u", "magnet", "🧲", "/pʊl/", "پال", "پُل", "کشیدن"),
        W(GLOW("اینجا {EN} = «اُ»", "u"), "full", "u", "battery", "🔋", "/fʊl/", "فال", "فُل", "پُر"),
    ],
    cap=("put رو «پات» نخون ❌", "u تو این ۴ تا کلمه یه «اُ»ی کوتاهه، مثل «پُل» 💡 برای دوستت بفرست"),
    stories=[
        REC(23, 2),
        QZ("write", "w", "writing_hand"),
        MC(23, 3, "دوید", "آواز خوند", 1),
        AQ("یه کلمه با u که", "مطمئن", "نیستی؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "sugar"),
    ])

write_day(24,
    hook=H("اسم این ۴ تا شهر", "رو", "اشتباه", "می‌گی!", "world_map", "انگلیسی‌ها این‌جوری می‌گن", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «اَ»", "a"), "Paris", "a", "croissant", "🥐", "/ˈpærɪs/", "پاریس", "پَریس", "پاریس"),
        W(GLOW("اینجا {EN} = «ا»", "o"), "London", "o", "crown", "👑", "/ˈlʌndən/", "لُندُن", "لاندِن", "لندن"),
        W(GLOW("اینجا {EN} = «اُو»", "o"), "Rome", "o", "pizza", "🍕", "/roʊm/", "رُم", "رُوم", "رُم"),
        W(GLOW("اینجا {EN} = «آی»", "ai"), "Dubai", "ai", "camel", "🐫", "/duːˈbaɪ/", "دُبَی", "دوبای", "دُبی"),
    ],
    cap=("اسم این ۴ تا شهر رو اشتباه می‌گی 😳", "London میشه «لاندِن» و Dubai میشه «دوبای» 🌍 برای دوستت بفرست"),
    stories=[
        REC(24, 0),
        QZV("magic", "g", "magic_wand", "«ج»"),
        MC(24, 3, "خالی", "شکسته", 0),
        AQ("اسم کدوم شهر رو", "مطمئن", "نیستی؟", "ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی بگم", "Barcelona"),
    ])

write_day(25,
    hook=H("این ۴ تا کلمه رو", "مثل", "فارسی", "نگو!", "face_with_raised_eyebrow", "انگلیسی‌ها یه جور دیگه می‌گن",
           "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «آی»", "i"), "vitamin", "i", "pill", "💊", "/ˈvaɪɾəmɪn/", "ویتامین", "وایدِمین", "ویتامین"),
        W(GLOW("اینجا {EN} = «آی»", "i"), "virus", "i", "microbe", "🦠", "/ˈvaɪrəs/", "ویروس", "وایرِس", "ویروس"),
        W(GLOW("اینجا {EN} = «یو»", "u"), "museum", "u", "classical_building", "🏛️", "/mjuˈziːəm/", "موزه", "میوزیِم", "موزه"),
        W(GLOW("اینجا {EN} = «ج»", "j"), "pajamas", "j", "bed", "🛏️", "/pəˈdʒɑːməz/", "پیژامه", "پِجامِز", "لباس خواب"),
    ],
    cap=("ویتامین و ویروس و موزه به انگلیسی چی میشن؟ 😳", "این ۴ تا رو مثل فارسی نگو 🔊 برای دوستت بفرست"),
    stories=[
        REC(25, 1, pron=True),
        QZ("guide", "u", "world_map"),
        MC(25, 3, "دوبی", "دُبَی", 1, pron=True),
        AQ("یه کلمه که فارسی", "هم", "داریمش؟", "ریپلای کن تا تلفظ انگلیسیشو\nتو ریلزهای بعدی بگم", "sandwich"),
    ])

# ---------------------------------------------------------------- trial reels: "a" vocab 15:00, "b" mistakes 19:00
SAVE = "سیو کن که یادت بمونه 📌"
SEND = "برای دوستت بفرست که اونم یاد بگیره 👇"

write_trial(19, "vocab", [
    dict(wrong="very beautiful", right="stunning", note="یعنی «فوق‌العاده زیبا»", emoji="star-struck"),
    dict(wrong="very bad", right="awful", note="یعنی «خیلی بد، افتضاح»", emoji="confounded_face"),
    dict(wrong="very important", right="crucial", note="یعنی «خیلی مهم، حیاتی»", emoji="key"),
    dict(wrong="very interesting", right="fascinating", note="یعنی «خیلی جذاب»", emoji="telescope"),
], ("به جای very این ۴ تا کلمه رو بگو 😎", SAVE), suffix="a")
write_trial(19, "mistakes", [
    dict(wrong="Yesterday night", right="Last night", note="«دیشب» میشه last night", emoji="crescent_moon"),
    dict(wrong="Depend of you.", right="It depends on you.", note="بعد از depend میاد on", emoji="person_shrugging"),
    dict(wrong="I'm afraid from dogs.", right="I'm afraid of dogs.", note="بعد از afraid میاد of", emoji="dog_face"),
], ("این ۳ تا جمله رو تقریباً همه اشتباه می‌گن 😬", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(20, "vocab", [
    dict(wrong="Hello.", right="Hey there!", note="یعنی «سلام» خودمونی", emoji="waving_hand"),
    dict(wrong="How are you?", right="How's it going?", note="یعنی «چطوری؟ اوضاع چطوره؟»", emoji="grinning_face"),
    dict(wrong="I'm fine.", right="Not bad.", note="یعنی «بد نیستم، خوبم»", emoji="ok_hand"),
    dict(wrong="What's new?", right="What's up?", note="یعنی «چه خبر؟»", emoji="speech_balloon"),
], ("این‌جوری سلام و احوالپرسی کن تا مثل بومی‌ها به نظر بیای 😎", SEND), suffix="a")
write_trial(20, "mistakes", [
    dict(wrong="Where you live?", right="Where do you live?", note="تو سؤال do لازمه", emoji="house"),
    dict(wrong="What means it?", right="What does it mean?", note="سؤال با does میاد، نه means", emoji="thinking_face"),
    dict(wrong="I know where is he.", right="I know where he is.", note="وسط جمله ترتیب عادیه: he is", emoji="magnifying_glass_tilted_left"),
], ("۳ تا سؤال که از فارسی ترجمه می‌کنیم ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(21, "vocab", [
    dict(wrong="very big", right="enormous", note="یعنی «خیلی بزرگ، عظیم»", emoji="elephant"),
    dict(wrong="very sad", right="heartbroken", note="یعنی «دل‌شکسته»", emoji="broken_heart"),
    dict(wrong="very angry", right="livid", note="یعنی «از عصبانیت کبود»", emoji="pouting_face"),
    dict(wrong="very scared", right="petrified", note="یعنی «از ترس خشکش زده»", emoji="fearful_face"),
], ("very رو بذار کنار؛ این ۴ تا کلمه رو بگو 😎", SAVE), suffix="a")
write_trial(21, "mistakes", [
    dict(wrong="I have hungry.", right="I'm hungry.", note="گرسنه بودن با be میاد، نه have", emoji="fork_and_knife_with_plate"),
    dict(wrong="I have sleep.", right="I'm sleepy.", note="«خوابم میاد» میشه I'm sleepy", emoji="sleeping_face"),
    dict(wrong="It's cold to me.", right="I'm cold.", note="«سردمه» میشه I'm cold", emoji="cold_face"),
], ("این ۳ تا رو از فارسی ترجمه نکن ❌", "تو کدومشو می‌گفتی؟ برای دوستت بفرست 👇"), suffix="b")

write_trial(22, "vocab", [
    dict(wrong="continue", right="carry on", note="یعنی «ادامه دادن»", emoji="right_arrow"),
    dict(wrong="postpone", right="put off", note="یعنی «عقب انداختن»", emoji="hourglass_not_done"),
    dict(wrong="cancel", right="call off", note="یعنی «کنسل کردن، لغو کردن»", emoji="cross_mark"),
    dict(wrong="search for", right="look for", note="یعنی «دنبالِ چیزی گشتن»", emoji="magnifying_glass_tilted_right"),
], ("بومی‌ها به جای این ۴ تا فعل این‌جوری می‌گن 😎", SAVE), suffix="a", headline="فعل‌هایی که بومی‌ها می‌گن")
write_trial(22, "mistakes", [
    dict(wrong="I'm tiring.", right="I'm tired.", note="«خسته‌ام» میشه tired، نه tiring", emoji="tired_face"),
    dict(wrong="I'm exciting!", right="I'm excited!", note="«هیجان‌زده‌ام» میشه excited", emoji="partying_face"),
    dict(wrong="I'm confusing.", right="I'm confused.", note="«گیج شدم» میشه confused", emoji="confused_face"),
], ("ing یا ed؟ این ۳ تا رو همه اشتباه می‌گن 😬", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(23, "vocab", [
    dict(wrong="Thank you very much.", right="Thanks a lot!", note="یعنی «خیلی ممنون»", emoji="folded_hands"),
    dict(wrong="You're welcome.", right="Anytime!", note="یعنی «خواهش می‌کنم، هر وقت خواستی»", emoji="smiling_face_with_smiling_eyes"),
    dict(wrong="It was nothing.", right="Don't mention it.", note="یعنی «قابلی نداشت»", emoji="red_heart"),
    dict(wrong="Sorry.", right="My apologies.", note="یعنی «عذر می‌خوام» (مؤدبانه)", emoji="pleading_face"),
], ("تشکر و عذرخواهی مثل بومی‌ها 😎", SEND), suffix="a")
write_trial(23, "mistakes", [
    dict(wrong="Since two years", right="For two years", note="مدت زمان با for میاد", emoji="calendar"),
    dict(wrong="Before two days", right="Two days ago", note="«دو روز پیش» میشه two days ago", emoji="spiral_calendar"),
    dict(wrong="After two days", right="In two days", note="«دو روز دیگه» میشه in two days", emoji="hourglass_done"),
], ("زمان رو این‌جوری نگو ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(24, "vocab", [
    dict(wrong="lift", right="elevator", note="یعنی «آسانسور» به آمریکایی", emoji="building_construction"),
    dict(wrong="flat", right="apartment", note="یعنی «آپارتمان» به آمریکایی", emoji="house_with_garden"),
    dict(wrong="biscuit", right="cookie", note="یعنی «بیسکویت، کلوچه» به آمریکایی", emoji="cookie"),
    dict(wrong="holiday", right="vacation", note="یعنی «تعطیلات» به آمریکایی", emoji="beach_with_umbrella"),
], ("بریتانیایی یا آمریکایی؟ این ۴ تا رو آمریکایی بگو 🇺🇸", SAVE), suffix="a", headline="آمریکایی حرف بزن")
write_trial(24, "mistakes", [
    dict(wrong="Congratulation!", right="Congratulations!", note="همیشه با s آخرش", emoji="party_popper"),
    dict(wrong="Thanks God!", right="Thank God!", note="بدون s: Thank God", emoji="folded_hands"),
    dict(wrong="Good night! (hello)", right="Good evening!", note="good night فقط برای خداحافظیه", emoji="night_with_stars"),
], ("تبریک و سلام رو این‌جوری نگو ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(25, "vocab", [
    dict(wrong="I'm very tired.", right="I'm beat.", note="یعنی «خسته و کوفته‌ام»", emoji="tired_face"),
    dict(wrong="I'm very happy.", right="I'm on cloud nine.", note="یعنی «تو آسمونام، خیلی خوشحالم»", emoji="cloud"),
    dict(wrong="I'm sad.", right="I'm feeling down.", note="یعنی «حالم گرفته‌ست»", emoji="pensive_face"),
    dict(wrong="I'm angry.", right="I'm fed up.", note="یعنی «کلافه شدم، دیگه خسته شدم»", emoji="unamused_face"),
], ("حال‌تو مثل بومی‌ها بگو 😎", SAVE), suffix="a")
write_trial(25, "mistakes", [
    dict(wrong="I like it very.", right="I like it a lot.", note="very آخر جمله نمیاد", emoji="red_heart"),
    dict(wrong="Make a party.", right="Throw a party.", note="«مهمونی گرفتن» میشه throw a party", emoji="party_popper"),
    dict(wrong="Make my homework.", right="Do my homework.", note="تکلیف رو do می‌کنن، نه make", emoji="memo"),
], ("make یا do؟ این ۳ تا رو اشتباه می‌گی ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

# ---------------------------------------------------------------- quote reels (23:00), a different topic every day
write_quote(19, "Small steps every day add up to big results.",
            "قدم‌های کوچیکِ هر روز، کم‌کم نتیجه‌های بزرگ می‌سازن.",
            [("add up", "روی هم جمع شدن")], "سیو کن برای روزایی که خسته‌ای 📌", topic="hard work", figure=True)
write_quote(20, "Love grows when you share it.",
            "عشق وقتی تقسیمش کنی، بیشتر میشه.",
            [("grows", "رشد می‌کنه، بیشتر میشه"), ("share", "تقسیم کردن")], "برای کسی که دوستش داری بفرست 🤍", topic="love")
write_quote(21, "Home is wherever your family is.",
            "خونه هر جاییه که خانواده‌ت اون‌جاست.",
            [("wherever", "هر جا که")], "برای خانواده‌ت بفرست 🏡", topic="family")
write_quote(22, "Don't wait for the perfect moment. Take the moment and make it perfect.",
            "منتظر لحظه‌ی بی‌نقص نمون؛ همین لحظه رو بگیر و بی‌نقصش کن.",
            [("perfect", "بی‌نقص"), ("moment", "لحظه")], "سیو کن 📌", topic="time", sea=True)
write_quote(23, "Being brave doesn't mean you're not afraid.",
            "شجاع بودن یعنی با ترس هم جلو بری، نه این‌که نترسی.",
            [("brave", "شجاع"), ("afraid", "ترسیده")], "برای یه آدم شجاع بفرست 💪", topic="courage")
write_quote(24, "If nothing changes, nothing changes.",
            "اگه هیچی رو عوض نکنی، هیچی عوض نمیشه.",
            [("changes", "عوض میشه")], "سیو کن برای وقتی که دنبال یه شروع تازه‌ای 📌", topic="change", figure=True)
write_quote(25, "Happiness is found in small moments.",
            "خوشبختی تو لحظه‌های کوچیک پیدا میشه.",
            [("found", "پیدا میشه")], "برای کسی که لحظه‌های خوبت باهاشه بفرست 🤍", topic="happiness", sea=True)
