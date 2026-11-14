"""Week 5: Sat 28 Nov – Fri 4 Dec 2026 (days 26–32): reels, trial reels and quote reels (batch of 14 Nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

TD = GLOW("صدای {EN}: نرم، شبیه «ذ»", "th", "tongue")
EDD = GLOW("اینجا {EN} = «د»", "ed")
CL = lambda tip_en: GLOW("{EN} بدون «اِ» اولش", tip_en)

write_day(26,
    hook=H("این ۴ تا کلمه رو", "با", "«آو»", "نخون!", "cross_mark", "ow این‌جا میشه «اُو»، مثل know", "light_bulb"),
    words=[
        W(GLOW("اینجا {EN} = «اُو»", "ow"), "bowl", "ow", "bowl_with_spoon", "🥣", "/boʊl/", "باول", "بُول", "کاسه"),
        W(GLOW("اینجا {EN} = «اُو»", "ow"), "own", "ow", "key", "🔑", "/oʊn/", "آون", "اُون", "مالِ خود"),
        W(GLOW("اینجا {EN} = «اُو»", "ow"), "grow", "ow", "seedling", "🌱", "/ɡroʊ/", "گراو", "گْرُو", "رشد کردن"),
        W(GLOW("اینجا {EN} = «اُو»", "ow"), "snow", "ow", "snowflake", "❄️", "/snoʊ/", "اِسناو", "سْنُو", "برف"),
    ],
    cap=("snow رو «اسناو» نخون ❌", "ow تو این ۴ تا کلمه میشه «اُو»، مثل know 💡 سیو کن"),
    stories=[
        REC(26, 0, pron=True),
        QZ("kneel", "k", "person_kneeling"),
        MC(26, 3, "کت و شلوار", "لباس ورزشی", 2),
        AQ("یه کلمه با ow", "که", "گیجت می‌کنه؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "towel"),
    ])

write_day(27,
    hook=H("es آخر این کلمه‌ها", "رو", "«س»", "نخون!", "warning", "بعد از s، x، sh و ch میشه «ایز»", "light_bulb"),
    words=[
        W(GLOW("اینجا {EN} = «ایز»", "es"), "boxes", "es", "package", "📦", "/ˈbɑːksɪz/", "باکسس", "باکسیز", "جعبه‌ها"),
        W(GLOW("اینجا {EN} = «ایز»", "es"), "glasses", "es", "glasses", "👓", "/ˈɡlæsɪz/", "گلاسس", "گْلَسیز", "عینک؛ لیوان‌ها"),
        W(GLOW("اینجا {EN} = «ایز»", "es"), "dishes", "es", "fork_and_knife_with_plate", "🍽️", "/ˈdɪʃɪz/", "دیشس", "دیشیز", "ظرف‌ها"),
        W(GLOW("اینجا {EN} = «ایز»", "es"), "faces", "es", "grinning_face", "😀", "/ˈfeɪsɪz/", "فِیسس", "فِیسیز", "صورت‌ها"),
    ],
    cap=("es آخر این ۴ کلمه رو «س» نخون ❌", "بعد از s، x، sh و ch، جمع میشه «ایز» 💡 برای دوستت بفرست"),
    stories=[
        REC(27, 3),
        QZV("visit", "s", "airplane", "«ز»"),
        MC(27, 2, "افتادن", "دویدن", 0),
        AQ("یه کلمه‌ی جمع که", "گیجت", "می‌کنه؟", "ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی یادت بدم", "watches"),
    ])

write_day(28,
    hook=H("این ۴ تا کلمه رو", "با", "«د» و «ت»", "نگو!", "cross_mark", "th این‌جا نرمه، شبیه «ذ»", "tongue"),
    words=[
        W(TD, "together", "th", "people_hugging", "🫂", "/təˈɡeðər/", "تُگِدِر", "تُگِذِر", "با هم"),
        W(TD, "other", "th", "busts_in_silhouette", "👥", "/ˈʌðər/", "آدِر", "آذِر", "دیگر"),
        W(TD, "breathe", "th", "wind_face", "🌬️", "/briːð/", "بْریت", "بْریذ", "نفس کشیدن"),
        W(TD, "smooth", "th", "butter", "🧈", "/smuːð/", "اِسموت", "سْموذ", "صاف، نرم"),
    ],
    cap=("th این ۴ تا کلمه «د» یا «ت» نیست ❌", "این‌جا th نرمه، شبیه «ذ»: زبونتو بذار بین دندونات 👅 سیو کن"),
    stories=[
        REC(28, 1),
        QZ("wrong", "w", "cross_mark"),
        MC(28, 2, "قاشق‌ها", "میزها", 1),
        AQ("یه کلمه با th که", "مطمئن", "نیستی؟", "ریپلای کن تا تو ریلزهای بعدی\nبا هم تمرینش کنیم", "clothes"),
    ])

write_day(29,
    hook=H("این ۴ تا خوراکی رو", "حتماً", "اشتباه", "می‌گی!", "astonished_face", "تلفظ درستشون این‌جوریه", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «اِس»", "uce"), "lettuce", "uce", "leafy_green", "🥬", "/ˈleɾɪs/", "لِتوس", "لِدِس", "کاهو"),
        W(GLOW("اینجا {EN} = «آ»", "o"), "broccoli", "o", "broccoli", "🥦", "/ˈbrɑːkəli/", "بروکلی", "بْراکِلی", "کلم بروکلی"),
        W(GLOW("اینجا {EN} = «یو»", "u"), "cucumber", "u", "cucumber", "🥒", "/ˈkjuːkʌmbər/", "کوکومبر", "کیوکامبِر", "خیار"),
        W(GLOW("اینجا {EN} = «ایِ»", "ea"), "cereal", "ea", "ear_of_corn", "🌽", "/ˈsɪriəl/", "سِرآل", "سیریِل", "غلات صبحانه"),
    ],
    cap=("کاهو و خیار و بروکلی به انگلیسی چی میشن؟ 🥗", "تلفظ درستشون رو یاد بگیر 🔊 برای دوستت بفرست"),
    stories=[
        REC(29, 1),
        QZV("result", "s", "bar_chart", "«ز»"),
        MC(29, 0, "از هم جدا", "تنها", 2),
        AQ("اسم کدوم خوراکی رو", "مطمئن", "نیستی؟", "ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی بگم", "yogurt"),
    ])

write_day(30,
    hook=H("این ۴ تا کلمه رو", "با", "«ایر»", "نخون!", "cross_mark", "ear این‌جا میشه «اِر»", "light_bulb"),
    words=[
        W(GLOW("اینجا {EN} = «اِر»", "ear"), "learn", "ear", "books", "📚", "/lɜːrn/", "لیرن", "لِرن", "یاد گرفتن"),
        W(GLOW("اینجا {EN} = «اِر»", "ear"), "early", "ear", "sunrise", "🌅", "/ˈɜːrli/", "ایرلی", "اِرلی", "زود"),
        W(GLOW("اینجا {EN} = «اِر»", "ear"), "bear", "ear", "bear", "🐻", "/ber/", "بیر", "بِر", "خرس"),
        W(GLOW("اینجا {EN} = «اِر»", "ear"), "wear", "ear", "jeans", "👖", "/wer/", "ویر", "وِر", "پوشیدن"),
    ],
    cap=("learn رو «لیرن» نخون ❌", "ear تو این ۴ تا کلمه میشه «اِر» 💡 سیو کن"),
    stories=[
        REC(30, 2),
        QZ("rhythm", "h", "drum"),
        MC(30, 3, "نان تست", "شیر", 1),
        AQ("یه کلمه با ear", "که", "سخته؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "heart"),
    ])

write_day(31,
    hook=H("ed این ۴ تا فعل", "رو", "«اِد»", "نخون!", "warning", "این‌جا ed فقط یه «د»ِ کوتاهه", "light_bulb"),
    words=[
        W(EDD, "opened", "ed", "door", "🚪", "/ˈoʊpənd/", "اوپِنِد", "اُوپِند", "باز کرد"),
        W(EDD, "called", "ed", "telephone_receiver", "📞", "/kɔːld/", "کالِد", "کالد", "زنگ زد؛ صدا زد"),
        W(EDD, "moved", "ed", "delivery_truck", "🚚", "/muːvd/", "مووِد", "موود", "جابه‌جا شد"),
        W(EDD, "cried", "ed", "crying_face", "😢", "/kraɪd/", "کرایِد", "کْراید", "گریه کرد"),
    ],
    cap=("opened رو «اوپِنِد» نخون ❌", "بعد از صداهای نرم ed فقط یه «د»ه 💡 برای دوستت بفرست"),
    stories=[
        REC(31, 0),
        QZV("season", "s", "maple_leaf", "«ز»"),
        MC(31, 1, "دیر", "همیشه", 2),
        AQ("یه فعل که", "گذشته‌اش", "سخته؟", "ریپلای کن تا تلفظشو\nتو ریلزهای بعدی بگم", "listened"),
    ])

write_day(32,
    hook=H("این ۴ تا کلمه رو", "با", "«اِ»", "شروع نکن!", "cross_mark", "انگلیسی‌ها مستقیم با s شروع می‌کنن",
           "speaker_high_volume"),
    words=[
        W(CL("st"), "star", "st", "star", "⭐", "/stɑːr/", "اِستار", "سْتار", "ستاره"),
        W(CL("sn"), "snake", "sn", "snake", "🐍", "/sneɪk/", "اِسنیک", "سْنِیک", "مار"),
        W(CL("sl"), "sleep", "sl", "sleeping_face", "😴", "/sliːp/", "اِسلیپ", "سْلیپ", "خوابیدن"),
        W(CL("sp"), "spoon", "sp", "spoon", "🥄", "/spuːn/", "اِسپون", "سْپون", "قاشق"),
    ],
    cap=("star رو «اِستار» نگو ❌", "اول کلمه «اِ» نذار؛ مستقیم با s شروع کن 💡 سیو کن"),
    stories=[
        REC(32, 3),
        QZ("who", "w", "thinking_face"),
        MC(32, 2, "خوابید", "نشست", 0),
        AQ("یه کلمه که با", "«اِ»", "شروعش می‌کنی؟", "ریپلای کن تا تو ریلزهای بعدی\nتلفظ درستشو بگم", "Spain"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
SEND = "برای دوستت بفرست که اونم یاد بگیره 👇"

write_trial(26, "vocab", [
    dict(wrong="very small", right="microscopic", note="یعنی «خیلی ریز»", emoji="microscope"),
    dict(wrong="very happy", right="overjoyed", note="یعنی «خیلی خوشحال، ذوق‌زده»", emoji="grinning_face_with_big_eyes"),
    dict(wrong="very hungry", right="famished", note="یعنی «خیلی گرسنه»", emoji="fork_and_knife_with_plate"),
    dict(wrong="very hot", right="scorching", note="یعنی «داغِ داغ» (برای هوا)", emoji="sun"),
], ("به جای very این ۴ تا کلمه رو بگو 😎", SAVE), suffix="a")
write_trial(26, "mistakes", [
    dict(wrong="Listen me.", right="Listen to me.", note="بعد از listen میاد to", emoji="ear"),
    dict(wrong="Wait me.", right="Wait for me.", note="بعد از wait میاد for", emoji="hourglass_not_done"),
    dict(wrong="Look me.", right="Look at me.", note="بعد از look میاد at", emoji="eyes"),
], ("این ۳ تا فعل بدون حرف اضافه غلطن ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(27, "vocab", [
    dict(wrong="Really?", right="No way!", note="یعنی «نه بابا! جدی؟»", emoji="astonished_face"),
    dict(wrong="I understand.", right="Got it.", note="یعنی «گرفتم، فهمیدم»", emoji="ok_hand"),
    dict(wrong="I don't understand.", right="You lost me.", note="یعنی «گیجم کردی، نفهمیدم»", emoji="confused_face"),
    dict(wrong="What did you say?", right="Come again?", note="یعنی «چی گفتی؟»", emoji="ear"),
], ("این‌جوری جواب بده تا مثل بومی‌ها به نظر بیای 😎", SEND), suffix="a")
write_trial(27, "mistakes", [
    dict(wrong="Yesterday I go.", right="Yesterday I went.", note="گذشته‌ی go میشه went", emoji="person_walking"),
    dict(wrong="Did you went?", right="Did you go?", note="بعد از did فعل ساده میاد", emoji="red_question_mark"),
    dict(wrong="I've seen it yesterday", right="I saw it yesterday.", note="با yesterday گذشته‌ی ساده میاد", emoji="eyes"),
], ("گذشته رو این‌جوری نگو ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(28, "vocab", [
    dict(wrong="Help me.", right="Give me a hand.", note="یعنی «یه کمکی بهم بکن»", emoji="raising_hands"),
    dict(wrong="Wait a minute.", right="Just a sec.", note="یعنی «یه لحظه»", emoji="stopwatch"),
    dict(wrong="Hurry up.", right="Let's get going.", note="یعنی «بجنب، بریم»", emoji="person_running"),
    dict(wrong="Calm down.", right="Take it easy.", note="یعنی «آروم باش، سخت نگیر»", emoji="relieved_face"),
], ("این ۴ تا جمله رو مثل بومی‌ها بگو 😎", SAVE), suffix="a")
write_trial(28, "mistakes", [
    dict(wrong="informations", right="information", note="information جمع نمی‌بنده", emoji="information"),
    dict(wrong="advices", right="advice", note="advice هم s نمی‌گیره", emoji="speech_balloon"),
    dict(wrong="furnitures", right="furniture", note="furniture همیشه مفرده", emoji="couch_and_lamp"),
], ("این ۳ تا کلمه هیچ‌وقت s نمی‌گیرن ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(29, "vocab", [
    dict(wrong="by the way", right="BTW", note="یعنی «راستی»", emoji="speech_balloon"),
    dict(wrong="as soon as possible", right="ASAP", note="یعنی «هر چه زودتر»", emoji="high_voltage"),
    dict(wrong="for your information", right="FYI", note="یعنی «محض اطلاعت»", emoji="information"),
    dict(wrong="to be honest", right="TBH", note="یعنی «راستش رو بخوای»", emoji="handshake"),
], ("BTW و ASAP یعنی چی؟ مخفف‌های چت 🤔", SAVE), suffix="a", headline="مخفف‌های چت انگلیسی", head_emoji="mobile_phone")
write_trial(29, "mistakes", [
    dict(wrong="The life is hard.", right="Life is hard.", note="برای مفهوم کلی the نمیاد", emoji="mountain"),
    dict(wrong="I play the football.", right="I play football.", note="قبل از اسم ورزش‌ها the نمیاد", emoji="soccer_ball"),
    dict(wrong="He is engineer.", right="He's an engineer.", note="قبل از شغل an یا a لازمه", emoji="man_technologist"),
], ("the و a رو این‌جا اشتباه می‌ذاری ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(30, "vocab", [
    dict(wrong="petrol", right="gas", note="یعنی «بنزین» به آمریکایی", emoji="fuel_pump"),
    dict(wrong="rubbish", right="trash", note="یعنی «آشغال» به آمریکایی", emoji="wastebasket"),
    dict(wrong="mobile", right="cell phone", note="یعنی «گوشی موبایل» به آمریکایی", emoji="mobile_phone"),
    dict(wrong="queue", right="line", note="یعنی «صف» به آمریکایی", emoji="busts_in_silhouette"),
], ("این ۴ تا کلمه رو آمریکایی بگو 🇺🇸", SAVE), suffix="a", headline="آمریکایی حرف بزن")
write_trial(30, "mistakes", [
    dict(wrong="I can to swim.", right="I can swim.", note="بعد از can فعل ساده میاد", emoji="person_swimming"),
    dict(wrong="Let's to go.", right="Let's go.", note="بعد از let's، to نمیاد", emoji="person_walking"),
    dict(wrong="I must to study.", right="I must study.", note="بعد از must هم to نمیاد", emoji="books"),
], ("این to‌ها اضافه‌ست ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(31, "vocab", [
    dict(wrong="very funny", right="hysterical", note="یعنی «از خنده روده‌بُر»", emoji="rolling_on_the_floor_laughing"),
    dict(wrong="very rich", right="loaded", note="یعنی «پولدارِ پولدار»", emoji="money_bag"),
    dict(wrong="very poor", right="broke", note="یعنی «بی‌پول، آس و پاس»", emoji="money_with_wings"),
    dict(wrong="very easy", right="a breeze", note="یعنی «آب خوردن، خیلی آسون»", emoji="wind_face"),
], ("very رو بذار کنار؛ این‌جوری بگو 😎", SAVE), suffix="a")
write_trial(31, "mistakes", [
    dict(wrong="Borrow me your pen.", right="Lend me your pen.", note="«قرض دادن» میشه lend", emoji="pen"),
    dict(wrong="He robbed my phone.", right="He stole my phone.", note="دزدیدن یه چیز میشه steal", emoji="mobile_phone"),
    dict(wrong="Remember me to call.", right="Remind me to call.", note="«یادم بنداز» میشه remind", emoji="alarm_clock"),
], ("این ۳ تا فعل رو با هم قاطی نکن ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(32, "vocab", [
    dict(wrong="find (online)", right="look up", note="یعنی «تو دیکشنری یا نت پیدا کردن»", emoji="magnifying_glass_tilted_left"),
    dict(wrong="visit (short)", right="drop by", note="یعنی «یه سر زدن»", emoji="house"),
    dict(wrong="arrive", right="show up", note="یعنی «پیدا شدن، اومدن»", emoji="person_walking"),
    dict(wrong="relax", right="chill out", note="یعنی «ریلکس کردن»", emoji="beach_with_umbrella"),
], ("بومی‌ها به جای این ۴ تا فعل این‌جوری می‌گن 😎", SAVE), suffix="a", headline="فعل‌هایی که بومی‌ها می‌گن")
write_trial(32, "mistakes", [
    dict(wrong="My charge finished.", right="My phone is dead.", note="«شارژم تموم شد» = my phone is dead", emoji="battery"),
    dict(wrong="Close the tap.", right="Turn off the tap.", note="شیر آب رو turn off می‌کنن", emoji="droplet"),
    dict(wrong="Give me the salt.", right="Pass me the salt.", note="سر سفره pass the salt می‌گن", emoji="salt"),
], ("این ۳ تا رو از فارسی ترجمه نکن ❌", "برای دوستت بفرست 👇"), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(26, "Not every thought deserves your attention.",
            "هر فکری لیاقت توجه تو رو نداره.",
            [("deserves", "لیاقتشو داره"), ("attention", "توجه")], "سیو کن برای شبایی که ذهنت شلوغه 📌",
            topic="peace of mind", figure=True)
write_quote(27, "Every expert was once a beginner.",
            "هر استادی یه روزی تازه‌کار بوده.",
            [("expert", "متخصص، استاد"), ("beginner", "تازه‌کار")], "برای کسی که تازه شروع کرده بفرست 🌱",
            topic="trying again")
write_quote(28, "You are stronger than you think.",
            "تو از چیزی که فکر می‌کنی قوی‌تری.",
            [("stronger", "قوی‌تر")], "برای کسی که این روزا خسته‌ست بفرست 💪", topic="self-belief", sea=True)
write_quote(29, "Slow progress is still progress.",
            "پیشرفتِ آهسته هم بازم پیشرفته.",
            [("progress", "پیشرفت")], "سیو کن 📌", topic="patience", figure=True)
write_quote(30, "Good friends are like stars. You don't always see them, but they're always there.",
            "دوستای خوب مثل ستاره‌ها هستن؛ همیشه نمی‌بینیشون، ولی همیشه هستن.",
            [("stars", "ستاره‌ها")], "برای دوست خوبت بفرست ⭐", topic="friendship")
write_quote(31, "A kind word can change someone's whole day.",
            "یه حرف مهربون می‌تونه کل روز یه نفر رو عوض کنه.",
            [("kind", "مهربون"), ("whole", "کل، تمام")], "امروز به یه نفر یه حرف خوب بزن 🤍", topic="kindness")
write_quote(32, "After the rain, the flowers grow.",
            "بعد از بارون، گل‌ها رشد می‌کنن.",
            [("rain", "بارون")], "برای کسی که روزای سختی داره بفرست 🌸", topic="hope", sea=True)
