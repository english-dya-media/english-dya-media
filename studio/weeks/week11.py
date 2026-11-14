"""Week 11: Sat 9 Jan – Fri 15 Jan 2027 (days 68–74): reels, trial reels and quote reels (batch of 14 Nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

FL = lambda s: GLOW("اینجا {EN} شبیه «د»", s)
E = lambda s: GLOW("اینجا {EN} = «اِ»", s)
OW = GLOW("اینجا {EN} = «آو»", "ow")

write_day(68,
    hook=H("t این ۴ تا کلمه", "شبیه", "«د»ه!", "آمریکایی بگو", "speaker_high_volume", "tomato میشه «تِمِیدُو»", "tomato"),
    words=[
        W(FL("t"), "computer", "t", "laptop", "💻", "/kəmˈpjuːɾər/", "کامپیوتِر", "کِمپیودِر", "کامپیوتر"),
        W(FL("t"), "sweater", "t", "coat", "🧥", "/ˈsweɾər/", "سوییتِر", "سوِدِر", "پلیور"),
        W(FL("t"), "tomato", "t", "tomato", "🍅", "/təˈmeɪɾoʊ/", "توماتو", "تِمِیدُو", "گوجه‌فرنگی", nth=1),
        W(FL("t"), "potato", "t", "potato", "🥔", "/pəˈteɪɾoʊ/", "پوتیتو", "پِتِیدُو", "سیب‌زمینی", nth=1),
    ],
    cap=("tomato رو «توماتو» نگو ❌", "آمریکایی‌ها t این ۴ تا کلمه رو شبیه «د» می‌گن 🇺🇸 سیو کن"),
    stories=[
        REC(68, 0),
        QZV("ocean", "c", "water_wave", "«ش»"),
        MC(68, 1, "قاب عکس", "صدا", 2),
        AQ("یه کلمه با t", "که", "گیجت می‌کنه؟", "ریپلای کن تا تلفظ آمریکاییشو\nبرات بگم", "eating"),
    ])

write_day(69,
    hook=H("تو این ۴ تا کلمه", "حرف", "t", "رو نخون!", "zipper-mouth_face", "whistle میشه «ویسِل»", "light_bulb"),
    words=[
        W(SIL("t"), "whistle", "t", "bird", "🐦", "/ˈwɪsəl/", "ویستِل", "ویسِل", "سوت؛ سوت زدن"),
        W(SIL("t"), "fasten", "t", "seat", "💺", "/ˈfæsən/", "فَستِن", "فَسِن", "بستن (کمربند)"),
        W(SIL("t"), "soften", "t", "feather", "🪶", "/ˈsɔːfən/", "سافتِن", "سافِن", "نرم کردن"),
        W(SIL("t"), "mortgage", "t", "house", "🏠", "/ˈmɔːrɡɪdʒ/", "مورتگیج", "مُرگِج", "وام مسکن"),
    ],
    cap=("whistle رو «ویستِل» نخون ❌", "t تو این ۴ تا کلمه خونده نمیشه 🤐 برای دوستت بفرست"),
    stories=[
        REC(69, 2, pron=True),
        QZ("sandwich", "d", "sandwich"),
        MC(69, 3, "گوجه‌فرنگی", "پیاز", 0),
        AQ("یه حرف بی‌صدا", "که", "تازه فهمیدی؟", "ریپلای کن؛ با هم بیشتر\nیادشون می‌گیریم", "island"),
    ])

write_day(70,
    hook=H("اسم این ۴ تا شهر", "به", "انگلیسی", "چی میشه؟", "world_map", "Venice «ونیز» نیست!", "astonished_face"),
    words=[
        W(GLOW("اینجا {EN} = «ک»", "ch"), "Munich", "ch", "pretzel", "🥨", "/ˈmjuːnɪk/", "مونیخ", "میونیک", "مونیخ"),
        W(GLOW("اینجا {EN} = «س»", "c"), "Venice", "c", "canoe", "🛶", "/ˈvenɪs/", "ونیز", "وِنیس", "ونیز"),
        W(GLOW("اینجا {EN} = «اِی»", "a"), "Naples", "a", "pizza", "🍕", "/ˈneɪpəlz/", "ناپل", "نِیپِلز", "ناپل"),
        W(GLOW("اینجا {EN} = «ج»", "G"), "Geneva", "G", "watch", "⌚", "/dʒəˈniːvə/", "ژنو", "جِنیوا", "ژنو"),
    ],
    cap=("ونیز و ژنو به انگلیسی چی میشن؟ 😳", "Venice میشه «وِنیس» و Geneva میشه «جِنیوا» 🌍 برای دوستت بفرست"),
    stories=[
        REC(70, 1),
        QZV("sure", "s", "check_mark_button", "«ش»"),
        MC(70, 3, "خونه", "اجاره", 2),
        AQ("دوست داری", "کدوم", "شهر بری؟", "ریپلای کن؛ تلفظ انگلیسیشو\nبرات می‌گم", "Barcelona"),
    ])

write_day(71,
    hook=H("اسم این ۴ تا شغل", "رو", "درست", "بگو!", "briefcase", "lawyer «لاویِر» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «اُ»", "aw"), "lawyer", "aw", "balance_scale", "⚖️", "/ˈlɔɪər/", "لاویِر", "لُویِر", "وکیل"),
        W(E("eo"), "surgeon", "eo", "health_worker", "🧑‍⚕️", "/ˈsɜːrdʒən/", "سِرجیون", "سِرجِن", "جراح"),
        W(FL("t"), "waiter", "t", "fork_and_knife", "🍴", "/ˈweɪɾər/", "ویتِر", "وِیدِر", "گارسون"),
        W(GLOW("اینجا {EN} = «اِری»", "ary"), "secretary", "ary", "file_folder", "📁", "/ˈsekrəteri/", "سکرتر", "سِکرِتِری",
          "منشی", ph="sˈɛkɹətˌɛɹi"),
    ],
    cap=("lawyer و secretary رو درست بگو 💼", "اسم این ۴ تا شغل رو این‌جوری بگو 🔊 برای دوستت بفرست"),
    stories=[
        REC(71, 0, pron=True),
        QZ("scene", "c", "clapper_board"),
        MC(71, 2, "رم", "میلان", 1),
        AQ("شغل تو", "به", "انگلیسی؟", "ریپلای کن؛ اسم شغلتو\nبه انگلیسی برات می‌گم", "engineer"),
    ])

write_day(72,
    hook=H("این ۴ تا خوراکی", "رو", "فرانسوی", "نگو!", "cross_mark", "dessert «دسر» نیست!", "shortcake"),
    words=[
        W(GLOW("اینجا {EN} = «ز»", "ss"), "dessert", "ss", "shortcake", "🍰", "/dɪˈzɜːrt/", "دِسِر", "دیزِرت", "دسر"),
        W(GLOW("اینجا {EN} = «اُو»", "oa"), "cocoa", "oa", "chocolate_bar", "🍫", "/ˈkoʊkoʊ/", "کاکائو", "کُوکُو", "کاکائو"),
        W(GLOW("اینجا {EN} = «آ»", "au"), "sauce", "au", "hot_pepper", "🌶️", "/sɔːs/", "سُس", "ساس", "سس"),
        W(GLOW("{EN} آخرش خونده میشه", "t"), "croissant", "t", "croissant", "🥐", "/krəˈsɑːnt/", "کروسان", "کْرِسانت",
          "کروسان", ph="kɹəsˈɑːnt"),
    ],
    cap=("dessert «دسر» نیست ❌", "این ۴ تا خوراکی رو انگلیسی بگو، نه فرانسوی 🔊 سیو کن"),
    stories=[
        REC(72, 3),
        QZV("enough", "gh", "ok_hand", "«ف»"),
        MC(72, 1, "پرستار", "دندون‌پزشک", 2),
        AQ("غذای مورد علاقه‌ت", "به", "انگلیسی؟", "ریپلای کن تا تلفظشو\nبرات بفرستم", "lasagna"),
    ])

write_day(73,
    hook=H("این ۴ تا کلمه رو", "با", "«اُو»", "نخون!", "cross_mark", "ow این‌جا «آو»ه، مثل now", "light_bulb"),
    words=[
        W(OW, "allow", "ow", "check_mark_button", "✅", "/əˈlaʊ/", "اَلُو", "اِلاو", "اجازه دادن"),
        W(OW, "crowd", "ow", "busts_in_silhouette", "👥", "/kraʊd/", "کرُود", "کْراود", "جمعیت"),
        W(OW, "towel", "ow", "soap", "🧼", "/ˈtaʊəl/", "تُوِل", "تاوِل", "حوله"),
        W(OW, "owl", "ow", "owl", "🦉", "/aʊl/", "اُول", "آوْل", "جغد"),
    ],
    cap=("allow رو «اَلُو» نخون ❌", "ow تو این ۴ تا کلمه «آو»ه، مثل now 💡 برای دوستت بفرست"),
    stories=[
        REC(73, 0),
        QZ("wrinkle", "w", "older_person"),
        MC(73, 2, "کره", "عسل", 0),
        AQ("یه کلمه با ow", "که", "مطمئن نیستی؟", "ریپلای کن؛ «اُو»ه یا «آو»؟\nبرات می‌گم", "bowl"),
    ])

write_day(74,
    hook=H("این ۴ تا کلمه رو", "مثل", "فارسی", "نگو!", "cross_mark", "charger «شارژر» نیست!", "electric_plug"),
    words=[
        W(GLOW("اینجا {EN} = «چ»", "ch"), "charger", "ch", "mobile_phone_with_arrow", "📲", "/ˈtʃɑːrdʒər/", "شارژر", "چارجِر",
          "شارژر"),
        W(FL("tt"), "battery", "tt", "battery", "🔋", "/ˈbæɾəri/", "باتری", "بَدِری", "باتری"),
        W(GLOW("اینجا {EN} = «اِی»", "a"), "cable", "a", "electric_plug", "🔌", "/ˈkeɪbəl/", "کابل", "کِیبِل", "کابل"),
        W(GLOW("اینجا {EN} = «اِ»", "a"), "adapter", "a", "high_voltage", "⚡", "/əˈdæptər/", "آداپتور", "اِدَپتِر", "آداپتور"),
    ],
    cap=("charger رو «شارژر» نگو ❌", "این ۴ تا کلمه رو انگلیسی بگو، نه فرانسوی 🔊 برای دوستت بفرست"),
    stories=[
        REC(74, 1),
        QZV("exam", "x", "memo", "«گز»"),
        MC(74, 3, "عقاب", "طوطی", 1),
        AQ("یه کلمه‌ی فرنگی", "که", "تو فارسی داریم؟", "ریپلای کن؛ تلفظ انگلیسیشو\nبهت می‌گم", "television"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
CMT = "تو کدومشو می‌گفتی؟ کامنت کن 👇"

write_trial(68, "vocab", [
    dict(wrong="work friend", right="colleague", note="یعنی «همکار»", emoji="briefcase"),
    dict(wrong="last day to finish", right="deadline", note="یعنی «مهلت، ضرب‌الاجل»", emoji="hourglass_not_done"),
    dict(wrong="travel to work", right="commute", note="یعنی «رفت‌وآمد هرروزه به کار»", emoji="bus"),
    dict(wrong="a free day", right="a day off", note="یعنی «یه روز مرخصی»", emoji="beach_with_umbrella"),
], ("انگلیسی محیط کار رو حرفه‌ای بگو 💼", SAVE), suffix="a", headline="انگلیسی محیط کار", head_emoji="briefcase")
write_trial(68, "mistakes", [
    dict(wrong="I no understand.", right="I don't understand.", note="منفی با don't ساخته میشه", emoji="confused_face"),
    dict(wrong="I don't have nothing.", right="I don't have anything.", note="دو تا منفی با هم نمیان", emoji="cross_mark"),
    dict(wrong="I didn't see nobody.", right="I didn't see anybody.", note="بعد از didn't، anybody میاد", emoji="see-no-evil_monkey"),
], ("جمله‌ی منفی رو این‌جوری نساز ❌", CMT), suffix="b")

write_trial(69, "vocab", [
    dict(wrong="sleep a little", right="take a nap", note="یعنی «چرت زدن»", emoji="sleeping_face"),
    dict(wrong="sleep by accident", right="doze off", note="یعنی «ناخواسته خوابت بردن»", emoji="yawning_face"),
    dict(wrong="wake up too late", right="oversleep", note="یعنی «خواب موندن»", emoji="alarm_clock"),
    dict(wrong="move a lot in bed", right="toss and turn", note="یعنی «غلت زدن، خوابت نبردن»", emoji="bed"),
], ("خواب و بیداری مثل بومی‌ها 😴", SAVE), suffix="a")
write_trial(69, "mistakes", [
    dict(wrong="I'm knowing him.", right="I know him.", note="know حالت ing نمی‌گیره", emoji="handshake"),
    dict(wrong="I'm wanting coffee.", right="I want coffee.", note="want هم ing نمی‌گیره", emoji="hot_beverage"),
    dict(wrong="I'm understanding.", right="I understand.", note="فعل‌های ذهنی ing نمی‌گیرن", emoji="brain"),
], ("این فعل‌ها ing نمی‌گیرن ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(70, "vocab", [
    dict(wrong="very cheap", right="dirt cheap", note="یعنی «مفت، خیلی ارزون»", emoji="coin"),
    dict(wrong="too expensive", right="a rip-off", note="یعنی «گرون‌فروشی، کلاه‌برداری»", emoji="angry_face"),
    dict(wrong="a very good price", right="a bargain", note="یعنی «یه خرید به‌صرفه»", emoji="shopping_bags"),
    dict(wrong="spend a lot", right="splurge", note="یعنی «ولخرجی کردن»", emoji="credit_card"),
], ("خرید رو مثل بومی‌ها توصیف کن 🛍️", SAVE), suffix="a", headline="انگلیسی خرید", head_emoji="shopping_bags")
write_trial(70, "mistakes", [
    dict(wrong="Don't be tired!", right="Thanks for today!", note="«خسته نباشید» رو این‌جوری بگو", emoji="folded_hands"),
    dict(wrong="Your hand not hurt!", right="Thanks a million!", note="«دستت درد نکنه» رو این‌جوری بگو", emoji="raising_hands"),
    dict(wrong="Eat with health!", right="Enjoy!", note="«نوش جان» رو این‌جوری بگو", emoji="fork_and_knife_with_plate"),
], ("تعارف‌های فارسی رو کلمه به کلمه ترجمه نکن 😅", CMT), suffix="b")

write_trial(71, "vocab", [
    dict(wrong="eat in small bites", right="nibble", note="یعنی «نوک زدن، کم‌کم خوردن»", emoji="mouse_face"),
    dict(wrong="eat very hungrily", right="devour", note="یعنی «با ولع بلعیدن»", emoji="hamburger"),
    dict(wrong="drink very fast", right="gulp", note="یعنی «یه‌نفس سر کشیدن»", emoji="cup_with_straw"),
    dict(wrong="drink with noise", right="slurp", note="یعنی «هورت کشیدن»", emoji="steaming_bowl"),
], ("به جای eat و drink این ۴ تا رو بگو 😋", SAVE), suffix="a")
write_trial(71, "mistakes", [
    dict(wrong="I have car.", right="I have a car.", note="قبل از اسم مفرد a لازمه", emoji="automobile"),
    dict(wrong="I had a breakfast.", right="I had breakfast.", note="وعده‌های غذا a نمی‌گیرن", emoji="cooking"),
    dict(wrong="He's at the work.", right="He's at work.", note="at work بدون the", emoji="office_building"),
], ("a و the رو این‌جا اشتباه می‌ذاری ❌", CMT), suffix="b")

write_trial(72, "vocab", [
    dict(wrong="study hard", right="hit the books", note="یعنی «حسابی درس خوندن»", emoji="books"),
    dict(wrong="study the night before", right="cram", note="یعنی «شب امتحانی خوندن»", emoji="crescent_moon"),
    dict(wrong="memorize", right="learn by heart", note="یعنی «حفظ کردن»", emoji="brain"),
    dict(wrong="get a perfect score", right="ace the test", note="یعنی «امتحانو ترکوندن»", emoji="hundred_points"),
], ("فصل امتحاناته؛ این ۴ تا رو یاد بگیر 📚", SAVE), suffix="a", headline="انگلیسی درس و امتحان", head_emoji="books")
write_trial(72, "mistakes", [
    dict(wrong="Don't laugh to me.", right="Don't laugh at me.", note="به کسی خندیدن = laugh at", emoji="face_with_tears_of_joy"),
    dict(wrong="I agree to you.", right="I agree with you.", note="با کسی موافق بودن = agree with", emoji="handshake"),
    dict(wrong="I'm thinking to you.", right="I'm thinking of you.", note="به کسی فکر کردن = think of", emoji="thought_balloon"),
], ("حرف اضافه‌ی این ۳ تا فعل ❌", CMT), suffix="b")

write_trial(73, "vocab", [
    dict(wrong="two-way ticket", right="round trip", note="یعنی «بلیت رفت و برگشت»", emoji="ticket"),
    dict(wrong="a stop between flights", right="layover", note="یعنی «توقف بین دو پرواز»", emoji="airplane_departure"),
    dict(wrong="tired after a flight", right="jet lag", note="یعنی «به‌هم‌ریختگی ساعت خواب»", emoji="sleeping_face"),
    dict(wrong="small bag on the plane", right="carry-on", note="یعنی «چمدون دستی»", emoji="luggage"),
], ("قبل از سفر این ۴ تا رو یاد بگیر ✈️", SAVE), suffix="a", headline="انگلیسی سفر", head_emoji="airplane")
write_trial(73, "mistakes", [
    dict(wrong="It's an university.", right="It's a university.", note="university با صدای «یو» شروع میشه", emoji="school"),
    dict(wrong="It takes a hour.", right="It takes an hour.", note="h تو hour خونده نمیشه", emoji="hourglass_done"),
    dict(wrong="It's an useful app.", right="It's a useful app.", note="useful هم با «یو» شروع میشه", emoji="mobile_phone"),
], ("a یا an؟ صداش مهمه، نه حرفش ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(74, "vocab", [
    dict(wrong="He stopped answering.", right="He ghosted me.", note="یعنی «یهو غیبش زد، جواب نداد»", emoji="ghost"),
    dict(wrong="It got famous online.", right="It went viral.", note="یعنی «تو اینترنت ترکوند»", emoji="fire"),
    dict(wrong="Send me a message.", right="Text me.", note="یعنی «بهم پیام بده»", emoji="speech_balloon"),
    dict(wrong="My internet finished.", right="I'm out of data.", note="یعنی «بسته‌ی اینترنتم تموم شده»", emoji="mobile_phone"),
], ("انگلیسی اینترنت و موبایل 📱", SAVE), suffix="a", headline="انگلیسی اینترنت", head_emoji="mobile_phone")
write_trial(74, "mistakes", [
    dict(wrong="Why are you nervous?", right="Why are you upset?", note="«عصبانی» = upset، نه nervous", emoji="pouting_face"),
    dict(wrong="Control your answers.", right="Check your answers.", note="«کنترل کردن» این‌جا یعنی check", emoji="check_mark_button"),
    dict(wrong="Pass a good time!", right="Have a good time!", note="«خوش بگذره» = have a good time", emoji="party_popper"),
], ("کلمه به کلمه از فارسی ترجمه نکن ❌", CMT), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(68, "Success is not luck. It's what you do every day.",
            "موفقیت شانس نیست؛ کاریه که هر روز انجام می‌دی.",
            [("luck", "شانس")], "سیو کن 📌", topic="success", figure=True)
write_quote(69, "A mistake is a lesson, not a failure.",
            "اشتباه یه درسه، نه یه شکست.",
            [("lesson", "درس"), ("failure", "شکست")], "برای کسی که از اشتباهش ناراحته بفرست 🤍", topic="mistakes")
write_quote(70, "Be honest, even when it's hard.",
            "صادق باش، حتی وقتی سخته.",
            [("honest", "صادق")], "سیو کن 📌", topic="honesty", sea=True)
write_quote(71, "Being alone is not the same as being lonely.",
            "تنها بودن با احساس تنهایی فرق داره.",
            [("lonely", "احساس تنهایی")], "برای کسی که این روزا تنهاست بفرست 🤍", topic="being alone", figure=True)
write_quote(72, "No act of kindness is ever too small.",
            "هیچ مهربونی‌ای کوچیک نیست.",
            [("kindness", "مهربونی")], "برای یه آدم مهربون بفرست 🤍", topic="kindness")
write_quote(73, "Even the darkest night will end.",
            "حتی تاریک‌ترین شب هم تموم میشه.",
            [("darkest", "تاریک‌ترین")], "برای کسی که منتظر صبحه بفرست 🌅", topic="hope")
write_quote(74, "Small changes today, big changes tomorrow.",
            "تغییرای کوچیک امروز، تغییرای بزرگ فردا.",
            [("changes", "تغییرها")], "سیو کن 📌", topic="change", trees=True)
