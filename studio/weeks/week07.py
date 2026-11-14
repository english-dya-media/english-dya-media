"""Week 7: Sat 12 Dec – Fri 18 Dec 2026 (days 40–46): reels, trial reels and quote reels (batch of 14 Nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

UI = lambda s: GLOW(f"اینجا {{EN}} = {s}", "ui")
CL = lambda tip_en: GLOW("{EN} بدون «اِ» اولش", tip_en)
SZ = GLOW("اینجا {EN} = «ز»", "s")

write_day(40,
    hook=H("این ۴ تا کلمه رو", "با", "«ویی»", "نخون!", "cross_mark", "ui این‌جا فقط یه صداست", "light_bulb"),
    words=[
        W(UI("«او»"), "fruit", "ui", "red_apple", "🍎", "/fruːt/", "فرویت", "فْروت", "میوه"),
        W(UI("«او»"), "juice", "ui", "beverage_box", "🧃", "/dʒuːs/", "جویس", "جوس", "آبمیوه"),
        W(UI("«او»"), "suit", "ui", "necktie", "👔", "/suːt/", "سویت", "سوت", "کت و شلوار"),
        W(UI("«ای»"), "build", "ui", "building_construction", "🏗️", "/bɪld/", "بویلد", "بیلد", "ساختن"),
    ],
    cap=("juice رو «جویس» نخون ❌", "ui تو این ۴ تا کلمه فقط یه صداست 💡 برای دوستت بفرست"),
    stories=[
        REC(40, 1),
        QZV("cheese", "s", "cheese_wedge", "«ز»"),
        MC(40, 2, "شروع کرد", "خوابید", 0),
        AQ("یه کلمه با ui", "که", "گیجت می‌کنه؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "guitar"),
    ])

write_day(41,
    hook=H("این ۴ تا عدد رو", "با هم", "قاطی", "نکن!", "warning", "teen: تأکید آخر • ty: t نرم", "light_bulb"),
    words=[
        W(GLOW("تأکید روی {EN}", "teen"), "thirteen", "teen", "input_numbers", "🔢", "/θɜːrˈtiːn/", "تِرتین", "ثِرتین", "سیزده"),
        W(GLOW("اینجا {EN} شبیه «د»", "t"), "thirty", "t", "shortcake", "🍰", "/ˈθɜːrɾi/", "تِرتی", "ثِردی", "سی", nth=1),
        W(GLOW("تأکید روی {EN}", "teen"), "eighteen", "teen", "id_button", "🆔", "/eɪˈtiːn/", "ایتین", "اِیتین", "هجده"),
        W(GLOW("اینجا {EN} شبیه «د»", "t"), "eighty", "t", "older_person", "🧓", "/ˈeɪɾi/", "ایتی", "اِیدی", "هشتاد"),
    ],
    cap=("thirteen یا thirty؟ این ۴ تا عدد رو قاطی نکن ⚠️", "teen تأکیدش آخره؛ ty تأکیدش اوله و t نرم میشه 💡 سیو کن"),
    stories=[
        REC(41, 2),
        QZ("knew", "k", "light_bulb"),
        MC(41, 0, "سبزی", "نان", 1),
        AQ("کدوم عدد انگلیسی", "تلفظش", "سخته؟", "ریپلای کن تا تو ریلزهای بعدی\nتلفظ درستشو بگم", "fifteen"),
    ])

write_day(42,
    hook=H("اسم این ۴ تا برند", "رو", "اشتباه", "می‌گی!", "astonished_face", "انگلیسی‌ها این‌جوری می‌گن", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «آی»", "I"), "IKEA", "I", "couch_and_lamp", "🛋️", "/aɪˈkiːə/", "ایکیا", "آیکیا", "برند مبلمان",
          ph="aɪkˈiːə"),
        W(GLOW("اینجا {EN} = «و»", "Hu"), "Huawei", "Hu", "mobile_phone", "📱", "/ˈwɑːweɪ/", "هوآوی", "واوِی", "برند موبایل",
          ph="wˈɑːweɪ"),
        W(GLOW("اینجا {EN} = «شاو»", "Xia"), "Xiaomi", "Xia", "laptop", "💻", "/ʃaʊˈmiː/", "شیائومی", "شاومی", "برند موبایل",
          ph="ʃaʊmˈiː"),
        W(GLOW("اینجا {EN} شبیه «د»", "t"), "Toyota", "t", "automobile", "🚗", "/tɔɪˈoʊɾə/", "تویوتا", "تُیُودا",
          "خودروساز ژاپنی", nth=1),
    ],
    cap=("IKEA و Huawei رو اشتباه می‌گی 😳", "انگلیسی‌ها این‌جوری تلفظشون می‌کنن 🔊 برای دوستت بفرست"),
    stories=[
        REC(42, 1, pron=True),
        QZV("gym", "g", "person_lifting_weights", "«ج»"),
        MC(42, 3, "اِیتی", "ایتی", 0, pron=True),
        AQ("اسم کدوم برند رو", "مطمئن", "نیستی؟", "ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی بگم", "Porsche"),
    ])

write_day(43,
    hook=H("این ۴ تا کلمه رو", "با", "«ایق»", "نخون!", "cross_mark", "eigh معمولاً «اِی»ه، ولی نه همیشه!", "light_bulb"),
    words=[
        W(GLOW("اینجا {EN} = «اِی»", "eigh"), "eight", "eigh", "keycap_8", "8️⃣", "/eɪt/", "ایت", "اِیت", "هشت"),
        W(GLOW("اینجا {EN} = «آی»", "eigh"), "height", "eigh", "straight_ruler", "📏", "/haɪt/", "هِیت", "هایت", "قد، ارتفاع"),
        W(GLOW("اینجا {EN} = «اِی»", "eigh"), "neighbor", "eigh", "house_with_garden", "🏡", "/ˈneɪbər/", "نایبِر", "نِیبِر", "همسایه"),
        W(GLOW("اینجا {EN} = «اِی»", "eigh"), "weigh", "eigh", "balance_scale", "⚖️", "/weɪ/", "وِیق", "وِی", "وزن کردن"),
    ],
    cap=("eight رو «ایت» نخون ❌", "eigh معمولاً میشه «اِی»؛ ولی height میشه «هایت» 😵 سیو کن"),
    stories=[
        REC(43, 2, pron=True),
        QZ("known", "k", "brain"),
        MC(43, 3, "برند ورزشی", "برند موبایل", 2),
        AQ("یه کلمه با gh", "که", "گیجت می‌کنه؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "daughter"),
    ])

write_day(44,
    hook=H("s آخر این کلمه‌ها", "رو", "«س»", "نخون!", "warning", "بعد از صداهای نرم میشه «ز»", "light_bulb"),
    words=[
        W(SZ, "keys", "s", "old_key", "🗝️", "/kiːz/", "کیس", "کیز", "کلیدها"),
        W(SZ, "phones", "s", "mobile_phone", "📱", "/foʊnz/", "فونِس", "فُونز", "گوشی‌ها"),
        W(SZ, "cars", "s", "racing_car", "🏎️", "/kɑːrz/", "کارس", "کارز", "ماشین‌ها"),
        W(SZ, "boys", "s", "boy", "👦", "/bɔɪz/", "بویس", "بویز", "پسرها"),
    ],
    cap=("s آخر این ۴ کلمه رو «س» نخون ❌", "بعد از صداهای نرم، s جمع میشه «ز» 💡 برای دوستت بفرست"),
    stories=[
        REC(44, 1),
        QZV("please", "s", "folded_hands", "«ز»"),
        MC(44, 2, "دوست", "فامیل", 1),
        AQ("یه کلمه‌ی جمع که", "گیجت", "می‌کنه؟", "ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی یادت بدم", "clothes"),
    ])

write_day(45,
    hook=H("این ۴ تا کلمه رو", "با", "«اِ»", "شروع نکن!", "cross_mark", "قبل از st و sp و sw «اِ» نذار", "speaker_high_volume"),
    words=[
        W(CL("st"), "student", "st", "man_student", "👨‍🎓", "/ˈstuːdənt/", "اِستودِنت", "سْتودِنت", "دانش‌آموز، دانشجو"),
        W(CL("st"), "story", "st", "open_book", "📖", "/ˈstɔːri/", "اِستوری", "سْتُری", "داستان؛ استوری"),
        W(CL("sp"), "special", "sp", "sparkles", "✨", "/ˈspeʃəl/", "اِسپِشیال", "سْپِشِل", "خاص، ویژه"),
        W(CL("sw"), "sweet", "sw", "candy", "🍬", "/swiːt/", "اِسوییت", "سْویت", "شیرین"),
    ],
    cap=("story رو «اِستوری» نگو ❌", "مستقیم با s شروع کن: «سْتُری» 💡 سیو کن"),
    stories=[
        REC(45, 3),
        QZ("written", "w", "memo"),
        MC(45, 0, "قفل‌ها", "درها", 2),
        AQ("یه کلمه که با", "«اِ»", "شروعش می‌کنی؟", "ریپلای کن تا تو ریلزهای بعدی\nتلفظ درستشو بگم", "Scotland"),
    ])

write_day(46,
    hook=H("این ۴ تا کلمه رو", "هر روز", "می‌گی", "ولی اشتباه!", "grimacing_face", "انگلیسیش یه جور دیگه‌ست", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «اَ»", "a"), "taxi", "a", "taxi", "🚕", "/ˈtæksi/", "تاکسی", "تَکسی", "تاکسی"),
        W(GLOW("اینجا {EN} = «اِ»", "a"), "garage", "a", "wrench", "🔧", "/ɡəˈrɑːʒ/", "گاراژ", "گِراژ", "پارکینگ، تعمیرگاه"),
        W(GLOW("اینجا {EN} = «اِی»", "e"), "cafe", "e", "hot_beverage", "☕", "/kæˈfeɪ/", "کافه", "کَفِی", "کافه"),
        W(GLOW("اینجا {EN} = «یو»", "u"), "menu", "u", "scroll", "📜", "/ˈmenjuː/", "مِنو", "مِنیو", "منو"),
    ],
    cap=("تاکسی، کافه و منو به انگلیسی چی میشن؟ 😳", "این ۴ تا رو مثل فارسی نگو 🔊 برای دوستت بفرست"),
    stories=[
        REC(46, 1),
        QZV("president", "s", "classical_building", "«ز»"),
        MC(46, 2, "معمولی", "قدیمی", 0),
        AQ("یه کلمه که فارسی", "هم", "داریمش؟", "ریپلای کن تا تلفظ انگلیسیشو\nتو ریلزهای بعدی بگم", "pizza"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
SEND = "برای دوستت بفرست که اونم یاد بگیره 👇"

write_trial(40, "vocab", [
    dict(wrong="very thirsty", right="parched", note="یعنی «از تشنگی هلاک»", emoji="desert"),
    dict(wrong="very tasty", right="mouth-watering", note="یعنی «دهن‌آب‌کن»", emoji="drooling_face"),
    dict(wrong="very wet", right="drenched", note="یعنی «خیسِ آب»", emoji="cloud_with_rain"),
    dict(wrong="very dry", right="bone-dry", note="یعنی «خشکِ خشک»", emoji="cactus"),
], ("به جای very این ۴ تا کلمه رو بگو 😎", SAVE), suffix="a")
write_trial(40, "mistakes", [
    dict(wrong="Thanks for help me.", right="Thanks for helping me.", note="بعد از for فعل ing می‌گیره", emoji="folded_hands"),
    dict(wrong="Before go, call me.", right="Before going, call me.", note="بعد از before هم ing میاد", emoji="telephone_receiver"),
    dict(wrong="I enjoy to dance.", right="I enjoy dancing.", note="بعد از enjoy فعل ing میاد", emoji="woman_dancing"),
], ("این ۳ تا فعل ing لازم دارن ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(41, "vocab", [
    dict(wrong="Good luck! (on stage)", right="Break a leg!", note="یعنی «موفق باشی» قبل از اجرا", emoji="performing_arts"),
    dict(wrong="I hope so.", right="Fingers crossed!", note="یعنی «امیدوارم که بشه»", emoji="crossed_fingers"),
    dict(wrong="Well done!", right="Nailed it!", note="یعنی «ترکوندی!»", emoji="hammer"),
    dict(wrong="Don't give up.", right="Hang in there.", note="یعنی «طاقت بیار، کم نیار»", emoji="flexed_biceps"),
], ("این‌جوری به دوستت انرژی بده 💪", SEND), suffix="a")
write_trial(41, "mistakes", [
    dict(wrong="Say a joke.", right="Tell a joke.", note="جوک رو tell می‌کنن", emoji="face_with_tears_of_joy"),
    dict(wrong="Make a photo.", right="Take a photo.", note="عکس گرفتن = take a photo", emoji="camera_with_flash"),
    dict(wrong="Do a mistake.", right="Make a mistake.", note="اشتباه کردن = make a mistake", emoji="cross_mark"),
], ("فعل این ۳ تا رو اشتباه انتخاب می‌کنی ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(42, "vocab", [
    dict(wrong="I don't know", right="IDK", note="یعنی «نمی‌دونم»", emoji="person_shrugging"),
    dict(wrong="oh my god", right="OMG", note="یعنی «وای خدای من»", emoji="face_screaming_in_fear"),
    dict(wrong="laughing out loud", right="LOL", note="یعنی «دارم از خنده می‌میرم»", emoji="face_with_tears_of_joy"),
    dict(wrong="be right back", right="BRB", note="یعنی «الان برمی‌گردم»", emoji="right_arrow_curving_left"),
], ("IDK و BRB یعنی چی؟ مخفف‌های چت 🤔", SAVE), suffix="a", headline="مخفف‌های چت انگلیسی", head_emoji="mobile_phone")
write_trial(42, "mistakes", [
    dict(wrong="I always am late.", right="I'm always late.", note="always بعد از am میاد", emoji="alarm_clock"),
    dict(wrong="I speak well English.", right="I speak English well.", note="well میره آخر جمله", emoji="speaking_head"),
    dict(wrong="Very thank you.", right="Thank you very much.", note="very تنها قبل از thank نمیاد", emoji="folded_hands"),
], ("ترتیب کلمه‌های این ۳ تا جمله غلطه ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(43, "vocab", [
    dict(wrong="say quietly", right="whisper", note="یعنی «پچ‌پچ کردن»", emoji="shushing_face"),
    dict(wrong="say loudly", right="shout", note="یعنی «داد زدن»", emoji="loudspeaker"),
    dict(wrong="look for a long time", right="stare", note="یعنی «خیره شدن»", emoji="eyes"),
    dict(wrong="look quickly", right="glance", note="یعنی «یه نگاه سریع انداختن»", emoji="eye"),
], ("به جای say و look این فعل‌های دقیق رو بگو 😎", SAVE), suffix="a", headline="فعل دقیق‌تر بگو", head_emoji="bullseye")
write_trial(43, "mistakes", [
    dict(wrong="Sorry for late.", right="Sorry I'm late.", note="«ببخشید دیر کردم» = Sorry I'm late", emoji="alarm_clock"),
    dict(wrong="Where is toilet?", right="Where's the restroom?", note="restroom مؤدبانه‌تره و the لازمه", emoji="restroom"),
    dict(wrong="Give me a water.", right="Can I have water?", note="water شمردنی نیست؛ a نمی‌گیره", emoji="droplet"),
], ("تو سفر این ۳ تا رو اشتباه نگو ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(44, "vocab", [
    dict(wrong="trousers", right="pants", note="یعنی «شلوار» به آمریکایی", emoji="jeans"),
    dict(wrong="sweets", right="candy", note="یعنی «آبنبات، شیرینی» به آمریکایی", emoji="lollipop"),
    dict(wrong="lorry", right="truck", note="یعنی «کامیون» به آمریکایی", emoji="articulated_lorry"),
    dict(wrong="pavement", right="sidewalk", note="یعنی «پیاده‌رو» به آمریکایی", emoji="person_walking"),
], ("این ۴ تا کلمه رو آمریکایی بگو 🇺🇸", SAVE), suffix="a", headline="آمریکایی حرف بزن")
write_trial(44, "mistakes", [
    dict(wrong="I'm born in 1995.", right="I was born in 1995.", note="«به دنیا اومدم» = I was born", emoji="baby"),
    dict(wrong="I have married.", right="I'm married.", note="«متأهلم» = I'm married", emoji="ring"),
    dict(wrong="I'm study English.", right="I'm studying English.", note="بعد از am فعل ing می‌گیره", emoji="books"),
], ("این ۳ تا جمله رو تقریباً همه اشتباه می‌گن 😬", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(45, "vocab", [
    dict(wrong="Let me think.", right="Let me sleep on it.", note="یعنی «بذار روش فکر کنم»", emoji="thinking_face"),
    dict(wrong="I forgot.", right="It slipped my mind.", note="یعنی «از ذهنم پرید»", emoji="brain"),
    dict(wrong="I'm coming.", right="I'm on my way.", note="یعنی «تو راهم، دارم میام»", emoji="person_walking"),
    dict(wrong="I'm ready.", right="I'm all set.", note="یعنی «همه چی آماده‌ست»", emoji="check_mark_button"),
], ("این ۴ تا جمله رو مثل بومی‌ها بگو 😎", SAVE), suffix="a")
write_trial(45, "mistakes", [
    dict(wrong="I go to the school.", right="I go to school.", note="رفتن به مدرسه the نمی‌خواد", emoji="school"),
    dict(wrong="at the night", right="at night", note="at night همیشه بدون the", emoji="crescent_moon"),
    dict(wrong="on the Monday", right="on Monday", note="قبل از روزهای هفته the نمیاد", emoji="spiral_calendar"),
], ("این the ها اضافه‌ست ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(46, "vocab", [
    dict(wrong="very sharp", right="razor-sharp", note="یعنی «تیزِ تیز»", emoji="kitchen_knife"),
    dict(wrong="very fast", right="lightning-fast", note="یعنی «برق‌آسا»", emoji="high_voltage"),
    dict(wrong="very strong", right="mighty", note="یعنی «پرزور، قدرتمند»", emoji="flexed_biceps"),
    dict(wrong="very weak", right="feeble", note="یعنی «خیلی ضعیف»", emoji="adhesive_bandage"),
], ("very رو بذار کنار؛ این ۴ تا رو بگو 😎", SAVE), suffix="a")
write_trial(46, "mistakes", [
    dict(wrong="He drives careful.", right="He drives carefully.", note="برای «چطوری» ly لازمه", emoji="automobile"),
    dict(wrong="You speak good.", right="You speak well.", note="خوب حرف زدن = speak well", emoji="speech_balloon"),
    dict(wrong="Run quick!", right="Run quickly!", note="برای «چطوری» ly لازمه", emoji="person_running"),
], ("این ۳ تا جمله یه ly کم دارن ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(40, "Peace begins when you stop comparing yourself to others.",
            "آرامش از وقتی شروع میشه که خودتو با بقیه مقایسه نکنی.",
            [("comparing", "مقایسه کردن")], "سیو کن 📌", topic="peace of mind", figure=True)
write_quote(41, "A new day is a new chance.",
            "هر روزِ تازه، یه فرصت تازه‌ست.",
            [("chance", "فرصت")], "برای کسی که دیروز روز خوبی نداشت بفرست 🌅", topic="trying again", sea=True)
write_quote(42, "Don't let anyone tell you what you can't do.",
            "نذار کسی بهت بگه چه کاری از دستت برنمیاد.",
            [("let", "اجازه دادن")], "برای کسی که بهش شک کردن بفرست 💪", topic="self-belief")
write_quote(43, "Trees that grow slowly have the strongest roots.",
            "درختایی که آهسته رشد می‌کنن، محکم‌ترین ریشه‌ها رو دارن.",
            [("slowly", "آهسته"), ("roots", "ریشه‌ها")], "سیو کن 📌", topic="patience", trees=True)
write_quote(44, "Talent opens the door; hard work keeps it open.",
            "استعداد درو باز می‌کنه؛ تلاش، بازش نگه می‌داره.",
            [("talent", "استعداد")], "برای یه آدم سخت‌کوش بفرست 💪", topic="hard work")
write_quote(45, "A friend is someone who knows you and still loves you.",
            "دوست کسیه که همه چیزتو می‌دونه و بازم دوستت داره.",
            [("still", "بازم، هنوز")], "برای اون دوستت بفرست 🤍", topic="friendship", figure=True)
write_quote(46, "Love is in the small things.",
            "عشق تو چیزای کوچیکه.",
            [("small things", "چیزای کوچیک")], "برای کسی که دوستش داری بفرست 🤍", topic="love", sea=True)
