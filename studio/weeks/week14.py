"""Week 14: Sat 30 Jan – Fri 5 Feb 2027 (days 89–95): reels, trial reels and quote reels (batch of 14 Nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

K = GLOW("اینجا {EN} = «ک»", "ch")
U = GLOW("اینجا {EN} = «یو»", "u")
ZH = GLOW("اینجا {EN} = «ژ»", "s")
G = GLOW("اینجا {EN} = «ج»", "g")

write_day(89,
    hook=H("تو این ۴ تا کلمه", "ch", "«ک»ه!", "نه «چ»", "light_bulb", "chemistry میشه «کِمِستری»", "speaker_high_volume"),
    words=[
        W(K, "chemistry", "ch", "alembic", "⚗️", "/ˈkemɪstri/", "چِمیستری", "کِمِستری", "شیمی"),
        W(K, "architect", "ch", "building_construction", "🏗️", "/ˈɑːrkɪtekt/", "آرچیتِکت", "آرکیتِکت", "معمار"),
        W(K, "stomach", "ch", "nauseated_face", "🤢", "/ˈstʌmək/", "استوماچ", "سْتامِک", "معده، شکم"),
        W(K, "echo", "ch", "loudspeaker", "📢", "/ˈekoʊ/", "اِچو", "اِکُو", "پژواک"),
    ],
    cap=("chemistry رو «چمیستری» نخون ❌", "ch تو این ۴ تا کلمه «ک»ه 💡 برای دوستت بفرست"),
    stories=[
        REC(89, 1),
        QZ("rhino", "h", "rhinoceros"),
        MC(89, 3, "مگس", "زنبور", 2),
        AQ("یه کلمه با ch", "که", "مطمئن نیستی؟", "ریپلای کن؛ «چ»ه یا «ک»؟\nبرات می‌گم", "character"),
    ])

write_day(90,
    hook=H("این ۴ تا لباس رو", "مثل", "فارسی", "نگو!", "cross_mark", "jacket «ژاکت» نیست!", "coat"),
    words=[
        W(GLOW("اینجا {EN} = «ج»", "j"), "jacket", "j", "coat", "🧥", "/ˈdʒækɪt/", "ژاکت", "جَکِت", "کاپشن، کت"),
        W(GLOW("اینجا {EN} = «آو»", "ou"), "blouse", "ou", "womans_clothes", "👚", "/blaʊs/", "بلوز", "بْلاوس", "بلوز زنانه",
          ph="blˈaʊs"),
        W(U, "uniform", "u", "backpack", "🎒", "/ˈjuːnɪfɔːrm/", "اونیفورم", "یونیفُرم", "لباس فرم"),
        W(GLOW("اینجا {EN} = «اُ»", "u"), "pullover", "u", "yarn", "🧶", "/ˈpʊloʊvər/", "پلیور", "پُلُووِر", "پلیور"),
    ],
    cap=("jacket رو «ژاکت» نگو ❌", "اسم این ۴ تا لباس رو انگلیسی بگو 🧥 برای دوستت بفرست"),
    stories=[
        REC(90, 0, pron=True),
        QZV("genius", "g", "brain", "«ج»"),
        MC(90, 1, "مهندس", "نقاش", 1),
        AQ("لباس مورد علاقه‌ت", "به", "انگلیسی؟", "ریپلای کن تا تلفظشو\nبرات بگم", "hoodie"),
    ])

write_day(91,
    hook=H("اسم این ۴ تا شهر", "به", "انگلیسی", "چی میشه؟", "world_map", "پکن به انگلیسی میشه Beijing!", "astonished_face"),
    words=[
        W(GLOW("اینجا {EN} = «آ»", "u"), "Brussels", "u", "waffle", "🧇", "/ˈbrʌsəlz/", "بروکسل", "بْراسِلز", "بروکسل"),
        W(GLOW("اینجا {EN} = «سا»", "saw"), "Warsaw", "saw", "castle", "🏰", "/ˈwɔːrsɔː/", "ورشو", "وُرسا", "ورشو"),
        W(GLOW("اینجا {EN} = «هِیگِن»", "hagen"), "Copenhagen", "hagen", "bicycle", "🚲", "/ˌkoʊpənˈheɪɡən/", "کپنهاگ",
          "کُوپِن‌هِیگِن", "کپنهاگ"),
        W(GLOW("اینجا {EN} = «ج»", "j"), "Beijing", "j", "panda", "🐼", "/beɪˈdʒɪŋ/", "پکن", "بِیجینگ", "پکن"),
    ],
    cap=("پکن و ورشو به انگلیسی چی میشن؟ 😳", "Beijing میشه «بِیجینگ» و Warsaw میشه «وُرسا» 🌍 برای دوستت بفرست"),
    stories=[
        REC(91, 2),
        QZ("scent", "c", "tulip"),
        MC(91, 0, "کفش", "شلوار", 0),
        AQ("اسم کدوم شهر رو", "بلد", "نیستی؟", "ریپلای کن تا تلفظ انگلیسیشو\nبرات بگم", "Amsterdam"),
    ])

write_day(92,
    hook=H("این ۴ تا کلمه رو", "با", "«او»", "نخون!", "cross_mark", "u این‌جا «یو»ه، مثل music", "light_bulb"),
    words=[
        W(U, "human", "u", "bust_in_silhouette", "👤", "/ˈhjuːmən/", "هومان", "هیومِن", "انسان"),
        W(U, "humor", "u", "face_with_tears_of_joy", "😂", "/ˈhjuːmər/", "هومور", "هیومِر", "شوخ‌طبعی، طنز"),
        W(U, "unit", "u", "triangular_ruler", "📐", "/ˈjuːnɪt/", "اونیت", "یونیت", "واحد"),
        W(U, "fuel", "u", "fuel_pump", "⛽", "/ˈfjuːəl/", "فوئل", "فیوئِل", "سوخت"),
    ],
    cap=("human رو «هومان» نخون ❌", "u تو این ۴ تا کلمه «یو»ه، مثل music 💡 سیو کن"),
    stories=[
        REC(92, 3, pron=True),
        QZV("future", "t", "crystal_ball", "«چ»"),
        MC(92, 1, "پراگ", "وین", 2),
        AQ("یه کلمه با u", "که", "گیجت می‌کنه؟", "ریپلای کن؛ «او»ه یا «یو»؟\nبرات می‌گم", "computer"),
    ])

write_day(93,
    hook=H("این ۴ تا کلمه‌ی", "ورزشی", "رو", "درست بگو", "sports_medal", "marathon «ماراتن» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «ی»", "e"), "karate", "e", "martial_arts_uniform", "🥋", "/kəˈrɑːɾi/", "کاراته", "کِرادی", "کاراته"),
        W(GLOW("اینجا {EN} = «ث»", "th"), "marathon", "th", "person_running", "🏃", "/ˈmærəθɑːn/", "ماراتن", "مَرِثان", "ماراتن"),
        W(GLOW("اینجا {EN} = «اِی»", "a"), "stadium", "a", "stadium", "🏟️", "/ˈsteɪdiəm/", "استادیوم", "سْتِیدیِم", "ورزشگاه"),
        W(G, "gymnastics", "g", "person_cartwheeling", "🤸", "/dʒɪmˈnæstɪks/", "ژیمناستیک", "جیمنَستیکس", "ژیمناستیک"),
    ],
    cap=("marathon رو «ماراتن» نگو ❌", "این ۴ تا کلمه‌ی ورزشی رو انگلیسی بگو 🏅 برای رفیق ورزشکارت بفرست"),
    stories=[
        REC(93, 0),
        QZ("limb", "b", "leg"),
        MC(93, 3, "آب", "برق", 0),
        AQ("ورزش مورد علاقه‌ت", "به", "انگلیسی؟", "ریپلای کن؛ تلفظشو\nبرات می‌فرستم", "volleyball"),
    ])

write_day(94,
    hook=H("تو این ۴ تا کلمه", "s", "«ژ»ه!", "نه «س»", "light_bulb", "measure میشه «مِژِر»", "speaker_high_volume"),
    words=[
        W(ZH, "Asia", "s", "globe_showing_asia-australia", "🌏", "/ˈeɪʒə/", "آسیا", "اِیژا", "آسیا"),
        W(ZH, "measure", "s", "straight_ruler", "📏", "/ˈmeʒər/", "میژر", "مِژِر", "اندازه گرفتن"),
        W(ZH, "treasure", "s", "gem_stone", "💎", "/ˈtreʒər/", "تریژر", "تْرِژِر", "گنج"),
        W(ZH, "usual", "s", "spiral_calendar", "🗓️", "/ˈjuːʒuəl/", "یوسوال", "یوژوئِل", "معمول"),
    ],
    cap=("measure رو «میژر» نخون ❌", "s تو این ۴ تا کلمه «ژ»ه 💡 برای دوستت بفرست"),
    stories=[
        REC(94, 1, pron=True),
        QZV("social", "c", "busts_in_silhouette", "«ش»"),
        MC(94, 2, "پارک", "باشگاه", 1),
        AQ("یه کلمه که", "صدای", "«ژ» داره؟", "ریپلای کن؛ تو ریلزهای بعدی\nتمرینش کنیم", "television"),
    ])

write_day(95,
    hook=H("این ۴ تا کلمه‌ی", "خونه", "رو", "درست بگو", "house", "toilet «توالت» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «اُی»", "oi"), "toilet", "oi", "toilet", "🚽", "/ˈtɔɪlət/", "توالت", "تُویلِت", "توالت"),
        W(GLOW("اینجا {EN} = «اَ»", "a"), "balcony", "a", "potted_plant", "🪴", "/ˈbælkəni/", "بالکن", "بَلکِنی", "بالکن"),
        W(GLOW("اینجا {EN} = «اِی»", "a"), "radiator", "a", "fire", "🔥", "/ˈreɪdieɪɾər/", "رادیاتور", "رِیدی‌اِیدِر", "شوفاژ، رادیاتور"),
        W(GLOW("اینجا {EN} = «آو»", "ow"), "shower", "ow", "shower", "🚿", "/ˈʃaʊər/", "شُوِر", "شاوِر", "دوش"),
    ],
    cap=("toilet رو «توالت» نگو ❌", "این ۴ تا کلمه‌ی خونه رو انگلیسی بگو 🏠 برای دوستت بفرست"),
    stories=[
        REC(95, 2),
        QZ("guilty", "u", "face_with_hand_over_mouth"),
        MC(95, 3, "عجیب", "جدید", 2),
        AQ("یه چیز تو خونه‌تون", "که", "اسمشو نمی‌دونی؟", "ریپلای کن؛ اسم انگلیسیشو\nبرات می‌گم", "drawer"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
CMT = "تو کدومشو می‌گفتی؟ کامنت کن 👇"

write_trial(89, "vocab", [
    dict(wrong="stop the car on side", right="pull over", note="یعنی «بزن کنار»", emoji="automobile"),
    dict(wrong="heavy traffic", right="traffic jam", note="یعنی «ترافیک سنگین»", emoji="vertical_traffic_light"),
    dict(wrong="busy traffic hours", right="rush hour", note="یعنی «ساعت شلوغی»", emoji="alarm_clock"),
    dict(wrong="put gas in the car", right="fill up", note="یعنی «باک رو پر کردن»", emoji="fuel_pump"),
], ("رانندگی به انگلیسی 🚗", SAVE), suffix="a", headline="انگلیسی رانندگی", head_emoji="automobile")
write_trial(89, "mistakes", [
    dict(wrong="I came with taxi.", right="I came by taxi.", note="با وسیله‌ی نقلیه = by", emoji="taxi"),
    dict(wrong="I go to work by foot.", right="I go to work on foot.", note="پیاده = on foot", emoji="person_walking"),
    dict(wrong="I'm in the bus.", right="I'm on the bus.", note="تو اتوبوس = on the bus", emoji="bus"),
], ("با تاکسی و پیاده رو این‌جوری نگو ❌", CMT), suffix="b")

write_trial(90, "vocab", [
    dict(wrong="wear (start wearing)", right="put on", note="یعنی «پوشیدن» (عمل)", emoji="coat"),
    dict(wrong="remove clothes", right="take off", note="یعنی «درآوردن لباس»", emoji="t-shirt"),
    dict(wrong="test clothes in a shop", right="try on", note="یعنی «پرو کردن»", emoji="shopping_bags"),
    dict(wrong="wear fancy clothes", right="dress up", note="یعنی «شیک کردن، لباس رسمی پوشیدن»", emoji="necktie"),
], ("لباس پوشیدن به انگلیسی 👕", SAVE), suffix="a")
write_trial(90, "mistakes", [
    dict(wrong="I wear clothes at 7.", right="I get dressed at 7.", note="لباس پوشیدن (صبح) = get dressed", emoji="alarm_clock"),
    dict(wrong="Put off your coat.", right="Take off your coat.", note="درآوردن = take off", emoji="coat"),
    dict(wrong="It comes to you!", right="It suits you!", note="«بهت میاد» = it suits you", emoji="t-shirt"),
], ("لباس رو این‌جوری نگو ❌", CMT), suffix="b")

write_trial(91, "vocab", [
    dict(wrong="tell me the news", right="keep me posted", note="یعنی «در جریانم بذار»", emoji="memo"),
    dict(wrong="start (a project)", right="get the ball rolling", note="یعنی «کار رو راه انداختن»", emoji="soccer_ball"),
    dict(wrong="start again from zero", right="back to square one", note="یعنی «برگشتن سر خونه‌ی اول»", emoji="keycap_1"),
    dict(wrong="not decided yet", right="up in the air", note="یعنی «هنوز معلوم نیست»", emoji="balloon"),
], ("اصطلاح‌های محیط کار 💼", SAVE), suffix="a", headline="انگلیسی محیط کار", head_emoji="briefcase")
write_trial(91, "mistakes", [
    dict(wrong="I'm working in Google.", right="I work at Google.", note="محل کار دائمی: work at", emoji="office_building"),
    dict(wrong="Send it until Monday.", right="Send it by Monday.", note="«تا دوشنبه» (مهلت) = by", emoji="spiral_calendar"),
    dict(wrong="Can I ask from you?", right="Can I ask a question?", note="بعد از ask حرف from نمیاد", emoji="person_raising_hand"),
], ("انگلیسی کاری رو این‌جوری نگو ❌", CMT), suffix="b")

write_trial(92, "vocab", [
    dict(wrong="two or three", right="a couple of", note="یعنی «یکی دو تا، چند تا»", emoji="victory_hand"),
    dict(wrong="a small number of", right="a handful of", note="یعنی «یه مشت، تعداد کمی»", emoji="raised_hand"),
    dict(wrong="very many", right="loads of", note="یعنی «کلی، یه عالمه»", emoji="package"),
    dict(wrong="more than enough", right="plenty of", note="یعنی «به اندازه‌ی کافی و بیشتر»", emoji="check_mark_button"),
], ("مقدار رو مثل بومی‌ها بگو 📦", SAVE), suffix="a")
write_trial(92, "mistakes", [
    dict(wrong="So many traffics!", right="So much traffic!", note="traffic شمردنی نیست", emoji="vertical_traffic_light"),
    dict(wrong="I eat many fruits.", right="I eat a lot of fruit.", note="fruit معمولاً مفرد میاد", emoji="red_apple"),
    dict(wrong="Police is here.", right="The police are here.", note="police همیشه جمعه", emoji="police_car_light"),
], ("این کلمه‌ها رو اشتباه جمع می‌بندی ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(93, "vocab", [
    dict(wrong="very", right="super", note="یعنی «خیلی» (خودمونی)", emoji="high_voltage"),
    dict(wrong="completely", right="totally", note="یعنی «کاملاً»", emoji="hundred_points"),
    dict(wrong="too much", right="way too", note="یعنی «خیلی زیادی» (way too hot)", emoji="hot_face"),
    dict(wrong="fairly", right="pretty", note="یعنی «نسبتاً» (pretty good)", emoji="ok_hand"),
], ("به جای very این‌ها رو هم بگو 😎", SAVE), suffix="a")
write_trial(93, "mistakes", [
    dict(wrong="I play yoga.", right="I do yoga.", note="یوگا رو do می‌کنن", emoji="person_in_lotus_position"),
    dict(wrong="I go to gym.", right="I go to the gym.", note="باشگاه = the gym", emoji="person_lifting_weights"),
    dict(wrong="I play swimming.", right="I go swimming.", note="ورزش‌های ing با go میان", emoji="person_swimming"),
], ("play، do یا go؟ ❌", CMT), suffix="b")

write_trial(94, "vocab", [
    dict(wrong="cut in small pieces", right="chop", note="یعنی «خرد کردن»", emoji="kitchen_knife"),
    dict(wrong="cut in thin pieces", right="slice", note="یعنی «ورقه‌ورقه کردن»", emoji="bread"),
    dict(wrong="remove the skin", right="peel", note="یعنی «پوست کندن»", emoji="banana"),
    dict(wrong="mix with a spoon", right="stir", note="یعنی «هم زدن»", emoji="spoon"),
], ("آشپزی به انگلیسی 🍳", SAVE), suffix="a", headline="انگلیسی آشپزی", head_emoji="cooking")
write_trial(94, "mistakes", [
    dict(wrong="Put the tea.", right="Make some tea.", note="«چای دم کردن» = make tea", emoji="teacup_without_handle"),
    dict(wrong="Cook a cake.", right="Bake a cake.", note="کیک رو bake می‌کنن", emoji="birthday_cake"),
    dict(wrong="Close the gas.", right="Turn off the stove.", note="«گاز رو ببند» = turn off the stove", emoji="fire"),
], ("تو آشپزخونه این‌جوری نگو ❌", CMT), suffix="b")

write_trial(95, "vocab", [
    dict(wrong="clean the room", right="tidy up", note="یعنی «مرتب کردن»", emoji="broom"),
    dict(wrong="wash the floor", right="mop the floor", note="یعنی «تِی کشیدن»", emoji="bucket"),
    dict(wrong="clean with a machine", right="vacuum", note="یعنی «جاروبرقی کشیدن»", emoji="dashing_away"),
    dict(wrong="throw away extra stuff", right="declutter", note="یعنی «اضافه‌ها رو دور ریختن»", emoji="wastebasket"),
], ("کارهای خونه به انگلیسی 🧹", SAVE), suffix="a")
write_trial(95, "mistakes", [
    dict(wrong="Fix the bed.", right="Make the bed.", note="«تخت رو مرتب کن» = make the bed", emoji="bed"),
    dict(wrong="Throw the trash.", right="Take out the trash.", note="«آشغالا رو ببر بیرون»", emoji="wastebasket"),
    dict(wrong="Make the laundry.", right="Do the laundry.", note="«لباس شستن» = do the laundry", emoji="soap"),
], ("کارهای خونه رو این‌جوری نگو ❌", "برای دوستت بفرست 👇"), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(89, "Don't just dream it. Plan it.",
            "فقط رویاشو نبین؛ براش برنامه بریز.",
            [("plan", "برنامه ریختن")], "سیو کن 📌", topic="dreams")
write_quote(90, "Every sunrise is a new beginning.",
            "هر طلوع، یه شروع تازه‌ست.",
            [("sunrise", "طلوع آفتاب")], "برای کسی که دنبال یه شروع تازه‌ست بفرست 🌅", topic="hope", sea=True)
write_quote(91, "Be with people who bring out the best in you.",
            "با آدمایی باش که بهترین نسخه‌ی تو رو بیرون میارن.",
            [("bring out", "بیرون آوردن")], "برای آدمای خوب زندگیت بفرست 🤍", topic="people", figure=True)
write_quote(92, "Holding on hurts more than letting go.",
            "نگه داشتن بیشتر از رها کردن درد داره.",
            [("holding on", "نگه داشتن"), ("letting go", "رها کردن")], "سیو کن 📌", topic="letting go")
write_quote(93, "Success starts with one brave decision.",
            "موفقیت با یه تصمیم شجاعانه شروع میشه.",
            [("decision", "تصمیم")], "برای کسی که می‌خواد شروع کنه بفرست 💪", topic="success", figure=True)
write_quote(94, "Don't be afraid of mistakes. Be afraid of not trying.",
            "از اشتباه نترس؛ از امتحان نکردن بترس.",
            [("afraid of", "ترسیدن از")], "سیو کن 📌", topic="mistakes", trees=True)
write_quote(95, "Kindness costs nothing, but it means everything.",
            "مهربونی هیچ هزینه‌ای نداره، ولی معنیش همه چیزه.",
            [("costs nothing", "هزینه‌ای نداره")], "برای یه آدم مهربون بفرست 🤍", topic="kindness", sea=True)
