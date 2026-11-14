"""Week 12: Sat 16 Jan – Fri 22 Jan 2027 (days 75–81): reels, trial reels and quote reels (batch of 14 Nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

FL = lambda s: GLOW("اینجا {EN} شبیه «د»", s)
CL = lambda tip_en: GLOW("{EN} بدون «اِ» اولش", tip_en)
TH = GLOW(f"صدای {{EN}}: زبون بین دندون{ZW}ها", "th", "tongue")
SIS = GLOW("آخرش {EN} = «سیس»", "sis")
G = GLOW("اینجا {EN} = «ج»", "g")
SH = lambda s: GLOW("اینجا {EN} = «ش»", s)

write_day(75,
    hook=H("اسم روزای هفته", "رو", "درست", "بگو!", "spiral_calendar", "Monday «موندی» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «آ»", "o"), "Monday", "o", "spiral_calendar", "🗓️", "/ˈmʌndeɪ/", "موندی", "ماندِی", "دوشنبه"),
        W(GLOW("اینجا {EN} = «ز»", "s"), "Tuesday", "s", "tear-off_calendar", "📆", "/ˈtuːzdeɪ/", "توسدی", "توزدِی", "سه‌شنبه"),
        W(FL("t"), "Saturday", "t", "party_popper", "🎉", "/ˈsæɾərdeɪ/", "ساتوردی", "سَدِردِی", "شنبه"),
        W(GLOW("اینجا {EN} = «آ»", "u"), "Sunday", "u", "sun", "☀️", "/ˈsʌndeɪ/", "سوندی", "ساندِی", "یکشنبه"),
    ],
    cap=("Monday رو «موندی» نخون ❌", "اسم این ۴ تا روز رو این‌جوری بگو 🔊 برای دوستت بفرست"),
    stories=[
        REC(75, 0, pron=True),
        QZ("rhyme", "h", "musical_notes"),
        MC(75, 1, "باتری", "بِیتِری", 2, pron=True),
        AQ("کدوم روز هفته", "رو", "دوست داری؟", "ریپلای کن؛ به انگلیسی\nبنویسش", "Friday"),
    ])

write_day(76,
    hook=H("این ۴ تا کلمه‌ی", "دانشگاهی", "رو", "درست بگو", "graduation_cap", "thesis «تز» نیست!", "speaker_high_volume"),
    words=[
        W(SIS, "crisis", "sis", "warning", "⚠️", "/ˈkraɪsɪs/", "کریز", "کْرایسیس", "بحران"),
        W(SIS, "thesis", "sis", "graduation_cap", "🎓", "/ˈθiːsɪs/", "تز", "ثیسیس", "پایان‌نامه"),
        W(SIS, "analysis", "sis", "bar_chart", "📊", "/əˈnæləsɪs/", "آنالیز", "اِنَلِسیس", "تحلیل"),
        W(SIS, "diagnosis", "sis", "stethoscope", "🩺", "/ˌdaɪəɡˈnoʊsɪs/", "دیاگنوز", "دایِگنُوسیس", "تشخیص (بیماری)"),
    ],
    cap=("thesis «تز» نیست و crisis «کریز» نیست ❌", "این ۴ تا کلمه آخرشون «سیس» داره 🎓 برای همکلاسیت بفرست"),
    stories=[
        REC(76, 2),
        QZV("picture", "t", "framed_picture", "«چ»"),
        MC(76, 3, "شنبه", "دوشنبه", 1),
        AQ("رشته‌ی تحصیلیت", "به", "انگلیسی؟", "ریپلای کن؛ اسم انگلیسیشو\nبرات می‌گم", "engineering"),
    ])

write_day(77,
    hook=H("اسم این ۴ تا کشور", "به", "انگلیسی", "چی میشه؟", "world_map", "اسپانیا میشه Spain!", "astonished_face"),
    words=[
        W(CL("Sp"), "Spain", "Sp", "woman_dancing", "💃", "/speɪn/", "اسپانیا", "سْپِین", "اسپانیا"),
        W(CL("Sw"), "Sweden", "Sw", "snowflake", "❄️", "/ˈswiːdən/", "سوئد", "سْویدِن", "سوئد"),
        W(GLOW("اینجا {EN} = «وِی»", "way"), "Norway", "way", "snow-capped_mountain", "🏔️", "/ˈnɔːrweɪ/", "نروژ", "نُروِی", "نروژ"),
        W(G, "Belgium", "g", "waffle", "🧇", "/ˈbeldʒəm/", "بلژیک", "بِلجِم", "بلژیک"),
    ],
    cap=("اسپانیا و سوئد به انگلیسی چی میشن؟ 😳", "Spain میشه «سْپِین» و Belgium میشه «بِلجِم» 🌍 برای دوستت بفرست"),
    stories=[
        REC(77, 1),
        QZ("subtle", "b", "pinching_hand"),
        MC(77, 0, "آرامش", "سرعت", 2),
        AQ("اسم کدوم کشور", "رو", "بلد نیستی؟", "ریپلای کن تا تلفظ درستشو\nبرات بگم", "Netherlands"),
    ])

write_day(78,
    hook=H("این ۴ تا عدد رو", "با", "«ت»", "تموم نکن!", "cross_mark", "th آخرشون «ث»ه: زبون بین دندون‌ها", "tongue"),
    words=[
        W(TH, "third", "th", "3rd_place_medal", "🥉", "/θɜːrd/", "تِرد", "ثِرد", "سوم"),
        W(TH, "fifth", "th", "keycap_5", "5️⃣", "/fɪfθ/", "فیفت", "فیفث", "پنجم"),
        W(TH, "sixth", "th", "keycap_6", "6️⃣", "/sɪksθ/", "سیکست", "سیکسث", "ششم"),
        W(TH, "twelfth", "th", "twelve_oclock", "🕛", "/twelfθ/", "توِلفت", "توِلفث", "دوازدهم"),
    ],
    cap=("fifth رو «فیفت» نگو ❌", "th آخر این عددها «ث»ه، نه «ت» 👅 سیو کن"),
    stories=[
        REC(78, 0, pron=True),
        QZV("vision", "s", "eye", "«ژ»"),
        MC(78, 3, "هلند", "سوئیس", 1),
        AQ("تو کلاس", "نفر", "چندم بودی؟", "ریپلای کن؛ به انگلیسی\nبنویس: first, second…", "first"),
    ])

write_day(79,
    hook=H("این ۴ تا کلمه‌ی", "علمی", "رو", "درست بگو", "test_tube", "energy «انرژی» نیست!", "speaker_high_volume"),
    words=[
        W(G, "oxygen", "g", "lungs", "🫁", "/ˈɑːksɪdʒən/", "اکسیژن", "آکسیجِن", "اکسیژن"),
        W(G, "energy", "g", "high_voltage", "⚡", "/ˈenərdʒi/", "انرژی", "اِنِرجی", "انرژی"),
        W(G, "genetic", "g", "dna", "🧬", "/dʒəˈnetɪk/", "ژنتیک", "جِنِدیک", "ژنتیکی"),
        W(GLOW("اینجا {EN} = «تُری»", "tory"), "laboratory", "tory", "microscope", "🔬", "/ˈlæbrətɔːri/", "لابراتوار", "لَبرِتُری",
          "آزمایشگاه"),
    ],
    cap=("energy رو «انرژی» نگو ❌", "این ۴ تا کلمه‌ی علمی رو انگلیسی بگو، نه فرانسوی 🔬 برای دوستت بفرست"),
    stories=[
        REC(79, 3),
        QZ("whole", "w", "pizza"),
        MC(79, 1, "چهارم", "ششم", 2),
        AQ("یه کلمه‌ی علمی", "که", "تلفظش سخته؟", "ریپلای کن؛ تو ریلزهای بعدی\nمی‌گمش", "physics"),
    ])

write_day(80,
    hook=H("تو این ۴ تا کلمه", "s", "«ش»ه!", "نه «س»", "light_bulb", "sugar میشه «شُگِر»", "speaker_high_volume"),
    words=[
        W(SH("s"), "sugar", "s", "candy", "🍬", "/ˈʃʊɡər/", "سوگار", "شُگِر", "شکر"),
        W(SH("ss"), "tissue", "ss", "roll_of_paper", "🧻", "/ˈtɪʃuː/", "تیسو", "تیشو", "دستمال کاغذی"),
        W(SH("ss"), "issue", "ss", "warning", "⚠️", "/ˈɪʃuː/", "ایسو", "ایشو", "مسئله، مشکل"),
        W(SH("s"), "insurance", "s", "shield", "🛡️", "/ɪnˈʃʊrəns/", "اینسورانس", "اینشورِنس", "بیمه"),
    ],
    cap=("sugar رو «سوگار» نخون ❌", "s تو این ۴ تا کلمه «ش»ه 💡 برای دوستت بفرست"),
    stories=[
        REC(80, 0, pron=True),
        QZV("graduate", "d", "graduation_cap", "«ج»"),
        MC(80, 3, "کتابخونه", "بیمارستان", 1),
        AQ("یه کلمه که", "صدای", "«ش» داره؟", "ریپلای کن؛ تو ریلزهای بعدی\nبا هم تمرینش کنیم", "machine"),
    ])

write_day(81,
    hook=H("سفارش تو کافه", "رو", "درست", "بگو!", "hot_beverage", "espresso «اکسپرسو» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «ی»", "ee"), "coffee", "ee", "hot_beverage", "☕", "/ˈkɔːfi/", "کافه", "کافی", "قهوه"),
        W(GLOW("اینجا {EN} = «س»، نه «کس»", "s"), "espresso", "s", "teacup_without_handle", "🍵", "/eˈspresoʊ/", "اکسپرسو",
          "اِسپرِسُو", "اسپرسو"),
        W(GLOW("اینجا {EN} = «ذ»", "th"), "smoothie", "th", "cup_with_straw", "🥤", "/ˈsmuːði/", "اسموتی", "سْموذی", "اسموتی"),
        W(GLOW("اینجا {EN} = «اِید»", "ade"), "lemonade", "ade", "lemon", "🍋", "/ˌleməˈneɪd/", "لیموناد", "لِمِنِید", "لیموناد"),
    ],
    cap=("espresso رو «اکسپرسو» نگو ❌", "تو کافه این ۴ تا رو این‌جوری سفارش بده ☕ برای رفیق کافه‌گردت بفرست"),
    stories=[
        REC(81, 1),
        QZ("cupboard", "p", "door"),
        MC(81, 2, "جواب", "سؤال", 0),
        AQ("تو کافه", "چی", "سفارش می‌دی؟", "ریپلای کن؛ تلفظ انگلیسیشو\nبرات می‌گم", "cappuccino"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
CMT = "تو کدومشو می‌گفتی؟ کامنت کن 👇"

write_trial(75, "vocab", [
    dict(wrong="look secretly", right="peek", note="یعنی «یواشکی نگاه کردن»", emoji="eyes"),
    dict(wrong="look angrily", right="glare", note="یعنی «چپ‌چپ نگاه کردن»", emoji="angry_face"),
    dict(wrong="look for a long time", right="gaze", note="یعنی «زل زدن، محو نگاه کردن»", emoji="smiling_face_with_heart-eyes"),
    dict(wrong="see suddenly", right="spot", note="یعنی «یهو دیدن، متوجه شدن»", emoji="magnifying_glass_tilted_left"),
], ("به جای look این ۴ تا رو بگو 👀", SAVE), suffix="a")
write_trial(75, "mistakes", [
    dict(wrong="I brush my tooths.", right="I brush my teeth.", note="جمع tooth میشه teeth", emoji="tooth"),
    dict(wrong="Five sheeps", right="Five sheep", note="sheep جمع و مفردش یکیه", emoji="ewe"),
    dict(wrong="Two womans", right="Two women", note="جمع woman میشه women", emoji="woman"),
], ("این کلمه‌ها جمع عجیب دارن ❌", CMT), suffix="b")

write_trial(76, "vocab", [
    dict(wrong="Yes, that's right!", right="Exactly!", note="یعنی «دقیقاً!»", emoji="bullseye"),
    dict(wrong="I agree 100%.", right="I couldn't agree more.", note="یعنی «کاملاً موافقم»", emoji="hundred_points"),
    dict(wrong="I don't agree.", right="I beg to differ.", note="یعنی «من نظر دیگه‌ای دارم» (مؤدبانه)", emoji="raised_hand"),
    dict(wrong="You're right.", right="You have a point.", note="یعنی «حرفت منطقیه»", emoji="light_bulb"),
], ("موافقت و مخالفت مثل بومی‌ها 🤝", SAVE), suffix="a", headline="موافقی یا مخالف؟", head_emoji="handshake")
write_trial(76, "mistakes", [
    dict(wrong="I spend a lot for food", right="I spend a lot on food.", note="spend ... on، نه for", emoji="money_bag"),
    dict(wrong="Take care about you.", right="Take care of yourself.", note="مراقب خودت باش = take care of", emoji="red_heart"),
    dict(wrong="I'll pay dinner.", right="I'll pay for dinner.", note="پول چیزی رو دادن = pay for", emoji="credit_card"),
], ("حرف اضافه‌ی این ۳ تا رو جا ننداز ❌", CMT), suffix="b")

write_trial(77, "vocab", [
    dict(wrong="Is it true?", right="For real?", note="یعنی «جدی؟ واقعاً؟»", emoji="face_with_raised_eyebrow"),
    dict(wrong="Really?!", right="Are you serious?", note="یعنی «جدی می‌گی؟»", emoji="astonished_face"),
    dict(wrong="Wow, unbelievable!", right="Get out of here!", note="یعنی «برو بابا! باورم نمیشه»", emoji="exploding_head"),
    dict(wrong="What?!", right="You're kidding!", note="یعنی «شوخی می‌کنی!»", emoji="face_with_open_mouth"),
], ("تعجب‌تو مثل بومی‌ها نشون بده 😲", SAVE), suffix="a")
write_trial(77, "mistakes", [
    dict(wrong="How many money?", right="How much money?", note="money شمردنی نیست؛ much", emoji="money_bag"),
    dict(wrong="How much people?", right="How many people?", note="people شمردنیه؛ many", emoji="busts_in_silhouette"),
    dict(wrong="A few water", right="A little water", note="برای غیرشمردنی: a little", emoji="droplet"),
], ("much یا many؟ این ۳ تا رو قاطی نکن ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(78, "vocab", [
    dict(wrong="laugh quietly", right="chuckle", note="یعنی «زیرلبی خندیدن»", emoji="grinning_face_with_smiling_eyes"),
    dict(wrong="laugh suddenly a lot", right="crack up", note="یعنی «از خنده منفجر شدن»", emoji="rolling_on_the_floor_laughing"),
    dict(wrong="cry a lot", right="weep", note="یعنی «زار زدن، اشک ریختن»", emoji="loudly_crying_face"),
    dict(wrong="almost cry", right="tear up", note="یعنی «اشک تو چشمات جمع شدن»", emoji="face_holding_back_tears"),
], ("به جای laugh و cry این ۴ تا رو بگو 😂", SAVE), suffix="a")
write_trial(78, "mistakes", [
    dict(wrong="I'm here since a year.", right="I've been here a year.", note="از گذشته تا حالا: present perfect", emoji="hourglass_not_done"),
    dict(wrong="I have went.", right="I have gone.", note="بعد از have شکل سوم فعل: gone", emoji="person_walking"),
    dict(wrong="I've met him last week", right="I met him last week.", note="با last week گذشته‌ی ساده میاد", emoji="calendar"),
], ("زمان فعل رو این‌جا اشتباه می‌گی ❌", CMT), suffix="b")

write_trial(79, "vocab", [
    dict(wrong="very big (room)", right="spacious", note="یعنی «جادار، دلباز»", emoji="house"),
    dict(wrong="very small (room)", right="cramped", note="یعنی «تنگ و کوچیک»", emoji="package"),
    dict(wrong="very big and heavy", right="massive", note="یعنی «غول‌پیکر، عظیم»", emoji="whale"),
    dict(wrong="very very small", right="minuscule", note="یعنی «ریز ریز، خیلی کوچیک»", emoji="ant"),
], ("به جای very big و very small این‌ها رو بگو 😎", SAVE), suffix="a")
write_trial(79, "mistakes", [
    dict(wrong="How much it costs?", right="How much is it?", note="قیمت رو این‌جوری بپرس", emoji="label"),
    dict(wrong="What time it is?", right="What time is it?", note="تو سؤال is قبل از it میاد", emoji="alarm_clock"),
    dict(wrong="Who did call you?", right="Who called you?", note="وقتی who فاعله، did نمی‌خواد", emoji="telephone_receiver"),
], ("این ۳ تا سؤال رو اشتباه می‌پرسی ❌", CMT), suffix="b")

write_trial(80, "vocab", [
    dict(wrong="smart and quick", right="sharp", note="یعنی «تیز، باهوش»", emoji="brain"),
    dict(wrong="naturally talented", right="gifted", note="یعنی «بااستعداد»", emoji="glowing_star"),
    dict(wrong="has no idea", right="clueless", note="یعنی «بی‌خبر، گیج»", emoji="face_with_spiral_eyes"),
    dict(wrong="not serious, funny", right="silly", note="یعنی «بامزه، لوس، احمقانه»", emoji="zany_face"),
], ("به جای smart و stupid این ۴ تا رو بگو 🧠", SAVE), suffix="a")
write_trial(80, "mistakes", [
    dict(wrong="Do a decision.", right="Make a decision.", note="تصمیم گرفتن = make a decision", emoji="thinking_face"),
    dict(wrong="Make me a favor.", right="Do me a favor.", note="لطف کردن = do a favor", emoji="folded_hands"),
    dict(wrong="Don't do noise.", right="Don't make noise.", note="سروصدا کردن = make noise", emoji="loudspeaker"),
], ("make یا do؟ این ۳ تا رو اشتباه می‌گی ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(81, "vocab", [
    dict(wrong="coffee to take away", right="to go", note="یعنی «بیرون‌بر»", emoji="hot_beverage"),
    dict(wrong="the bill (at a cafe)", right="the check", note="یعنی «صورت‌حساب» به آمریکایی", emoji="receipt"),
    dict(wrong="extra money for waiter", right="tip", note="یعنی «انعام»", emoji="coin"),
    dict(wrong="booking a table", right="reservation", note="یعنی «رزرو»", emoji="spiral_calendar"),
], ("تو کافه و رستوران این‌جوری حرف بزن ☕", SAVE), suffix="a", headline="انگلیسی کافه و رستوران",
   head_emoji="hot_beverage")
write_trial(81, "mistakes", [
    dict(wrong="I want the bill.", right="Can we get the check?", note="صورت‌حساب رو مؤدبانه بخواه", emoji="receipt"),
    dict(wrong="One water, please.", right="Some water, please.", note="water شمردنی نیست", emoji="droplet"),
    dict(wrong="It's very delicious.", right="It's really delicious.", note="delicious خودش قویه؛ very نمی‌خواد", emoji="face_savoring_food"),
], ("تو رستوران این‌جوری نگو ❌", CMT), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(75, "Happiness is a choice you make every morning.",
            "خوشحالی انتخابیه که هر روز صبح می‌کنی.",
            [("choice", "انتخاب")], "سیو کن 📌", topic="happiness", sea=True)
write_quote(76, "Let today be calm. Not every problem needs an answer now.",
            "بذار امروز آروم باشه؛ لازم نیست هر مشکلی همین الان جواب داشته باشه.",
            [("calm", "آروم")], "سیو کن برای روزای شلوغ 📌", topic="peace of mind")
write_quote(77, "Try again. This time with more experience.",
            "دوباره امتحان کن؛ این بار با تجربه‌ی بیشتر.",
            [("experience", "تجربه")], "برای کسی که می‌خواد دوباره شروع کنه بفرست 🌱", topic="trying again", figure=True)
write_quote(78, "You are capable of more than you know.",
            "تو از چیزی که فکر می‌کنی تواناتری.",
            [("capable", "توانا")], "برای کسی که به خودش شک داره بفرست 💪", topic="self-belief")
write_quote(79, "Patience is not just waiting. It's staying calm while you wait.",
            "صبر فقط منتظر موندن نیست؛ آروم موندن موقع انتظاره.",
            [("patience", "صبر"), ("while", "در حالی که")], "سیو کن 📌", topic="patience", trees=True)
write_quote(80, "Little by little, a little becomes a lot.",
            "کم‌کم، کمِ کم زیاد میشه.",
            [("little by little", "کم‌کم")], "برای یه آدم سخت‌کوش بفرست 💪", topic="hard work", figure=True)
write_quote(81, "A good friend makes the hard days easier.",
            "یه دوست خوب روزای سخت رو آسون‌تر می‌کنه.",
            [("easier", "آسون‌تر")], "برای دوستت بفرست 🤍", topic="friendship", sea=True)
