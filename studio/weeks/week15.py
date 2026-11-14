"""Week 15: Sat 6 Feb – Fri 12 Feb 2027 (days 96–102): reels, trial reels and quote reels (batch of 14 Nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

EI = GLOW("اینجا {EN} = «اِی»", "a")
AI = GLOW("اینجا {EN} = «آی»", "i")
EY = GLOW("آخرش {EN} = «ی»", "e")

write_day(96,
    hook=H("این ۴ تا کلمه رو", "با", "«آ»", "نخون!", "cross_mark", "a این‌جا «اِی»ه، مثل name", "light_bulb"),
    words=[
        W(EI, "angel", "a", "baby_angel", "👼", "/ˈeɪndʒəl/", "آنجل", "اِینجِل", "فرشته"),
        W(EI, "danger", "a", "warning", "⚠️", "/ˈdeɪndʒər/", "دانجر", "دِینجِر", "خطر"),
        W(EI, "major", "a", "graduation_cap", "🎓", "/ˈmeɪdʒər/", "ماژور", "مِیجِر", "رشته‌ی اصلی؛ مهم"),
        W(EI, "chaos", "a", "tornado", "🌪️", "/ˈkeɪɑːs/", "چائوس", "کِی‌آس", "هرج و مرج"),
    ],
    cap=("angel رو «آنجل» نخون ❌", "a تو این ۴ تا کلمه «اِی»ه، مثل name 💡 برای دوستت بفرست"),
    stories=[
        REC(96, 1),
        QZV("headphones", "ph", "headphone", "«ف»"),
        MC(96, 3, "وان", "حوله", 1),
        AQ("یه کلمه با a", "که", "مطمئن نیستی؟", "ریپلای کن؛ «آ»ه یا «اِی»؟\nبرات می‌گم", "data"),
    ])

write_day(97,
    hook=H("اسم این ۴ تا ساز", "رو", "درست", "بگو!", "musical_score", "violin «ویولن» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «وایِ»", "vio"), "violin", "vio", "violin", "🎻", "/ˌvaɪəˈlɪn/", "ویولن", "وایِلین", "ویولن"),
        W(GLOW("اینجا {EN} = «چ»", "c"), "cello", "c", "musical_note", "🎵", "/ˈtʃeloʊ/", "سِلو", "چِلُو", "ویولن‌سل"),
        W(GLOW("اینجا {EN} = «ک»", "ch"), "orchestra", "ch", "musical_score", "🎼", "/ˈɔːrkɪstrə/", "ارکستر", "اُرکِسترا", "ارکستر"),
        W(GLOW("اینجا {EN} = «اِکُ»", "acco"), "accordion", "acco", "accordion", "🪗", "/əˈkɔːrdiən/", "آکاردئون", "اِکُردیِن",
          "آکاردئون"),
    ],
    cap=("violin رو «ویولن» نگو ❌", "اسم این ۴ تا ساز رو انگلیسی بگو 🎻 برای رفیق موزیسینت بفرست"),
    stories=[
        REC(97, 0, pron=True),
        QZ("ballet", "t", "ballet_shoes"),
        MC(97, 2, "رشته‌ی فرعی", "دانشگاه", 0),
        AQ("چه سازی", "دوست داری", "بزنی؟", "ریپلای کن؛ اسم انگلیسیشو\nبرات می‌گم", "guitar"),
    ])

write_day(98,
    hook=H("اسم این ۴ تا ماه", "رو", "فرانسوی", "نگو!", "cross_mark", "مارس و آوریل فرانسوی‌ان!", "calendar"),
    words=[
        W(GLOW("اینجا {EN} = «چ»", "ch"), "March", "ch", "seedling", "🌱", "/mɑːrtʃ/", "مارس", "مارچ", "مارس (ماه)"),
        W(GLOW("اینجا {EN} = «اِی»", "A"), "April", "A", "umbrella_with_rain_drops", "☔", "/ˈeɪprəl/", "آوریل", "اِیپرِل", "آوریل"),
        W(GLOW("اینجا {EN} = «لای»", "ly"), "July", "ly", "ice_cream", "🍦", "/dʒʊˈlaɪ/", "ژوئیه", "جولای", "ژوئیه"),
        W(GLOW("اینجا {EN} = «اُو»", "o"), "November", "o", "fallen_leaf", "🍂", "/noʊˈvembər/", "نوامبر", "نُووِمبِر", "نوامبر"),
    ],
    cap=("مارس و آوریل به انگلیسی چی میشن؟ 📅", "اسم این ۴ تا ماه رو انگلیسی بگو، نه فرانسوی 💡 سیو کن"),
    stories=[
        REC(98, 3),
        QZV("magician", "c", "magic_wand", "«ش»"),
        MC(98, 1, "سِلو", "کِلو", 2, pron=True),
        AQ("تولدت", "چه", "ماهیه؟", "ریپلای کن؛ به انگلیسی\nبنویسش", "September"),
    ])

write_day(99,
    hook=H("این ۴ تا کلمه رو", "با", "«ای»", "نخون!", "cross_mark", "i این‌جا «آی»ه، مثل five", "light_bulb"),
    words=[
        W(AI, "pilot", "i", "airplane", "✈️", "/ˈpaɪlət/", "پیلوت", "پایلِت", "خلبان"),
        W(AI, "iron", "i", "magnet", "🧲", "/ˈaɪərn/", "ایرون", "آیِرن", "آهن؛ اتو"),
        W(AI, "license", "i", "identification_card", "🪪", "/ˈlaɪsəns/", "لیسانس", "لایسِنس", "گواهینامه، مجوز"),
        W(AI, "climate", "i", "globe_showing_americas", "🌎", "/ˈklaɪmət/", "کلیمات", "کْلایمِت", "آب و هوا، اقلیم"),
    ],
    cap=("license «لیسانس» نیست ❌", "i تو این ۴ تا کلمه «آی»ه 💡 license یعنی «مجوز»، نه مدرک دانشگاهی؛ سیو کن"),
    stories=[
        REC(99, 1, pron=True),
        QZ("fascinate", "c", "star-struck"),
        MC(99, 2, "ژوئن", "اوت", 0),
        AQ("یه کلمه که", "معنیش", "فرق داره؟", "ریپلای کن؛ مثل license\nکه «لیسانس» نیست", "doctor"),
    ])

write_day(100,
    hook=H("این ۴ تا وسیله", "رو", "انگلیسی", "بگو!", "speaker_high_volume", "bicycle «بیسیکلت» نیست!", "bicycle"),
    words=[
        W(AI, "bicycle", "i", "bicycle", "🚲", "/ˈbaɪsɪkəl/", "بیسیکلت", "بایسیکِل", "دوچرخه"),
        W(GLOW("آخرش {EN} = «سایکِل»", "cycle"), "motorcycle", "cycle", "motorcycle", "🏍️", "/ˈmoʊɾərsaɪkəl/", "موتورسیکلت",
          "مُودِرسایکِل", "موتورسیکلت"),
        W(GLOW("اینجا {EN} = «بیِ»", "bu"), "ambulance", "bu", "ambulance", "🚑", "/ˈæmbjələns/", "آمبولانس", "اَمبیِلِنس",
          "آمبولانس"),
        W(SIL("ch"), "yacht", "ch", "motor_boat", "🛥️", "/jɑːt/", "یاچت", "یات", "قایق تفریحی"),
    ],
    cap=("bicycle «بیسیکلت» نیست ❌", "این ۴ تا وسیله رو انگلیسی بگو 🚲 yacht هم میشه «یات»؛ برای دوستت بفرست"),
    stories=[
        REC(100, 2),
        QZV("question", "t", "red_question_mark", "«چ»"),
        MC(100, 0, "مهندس", "مهماندار", 2),
        AQ("با چی", "میری", "سر کار؟", "ریپلای کن؛ به انگلیسی\nبنویسش", "by bus"),
    ])

write_day(101,
    hook=H("e آخر این کلمه‌ها", "خونده", "میشه!", "«ی»", "speaker_high_volume", "recipe میشه «رِسِپی»", "light_bulb"),
    words=[
        W(EY, "recipe", "e", "spiral_notepad", "🗒️", "/ˈresəpi/", "رِسایپ", "رِسِپی", "دستور پخت", nth=1),
        W(EY, "sesame", "e", "bagel", "🥯", "/ˈsesəmi/", "سِسام", "سِسِمی", "کنجد", nth=1),
        W(EY, "karaoke", "e", "microphone", "🎤", "/ˌkæriˈoʊki/", "کارائوکه", "کَری‌اُوکی", "کارائوکه"),
        W(EY, "catastrophe", "e", "volcano", "🌋", "/kəˈtæstrəfi/", "کاتاستروف", "کِتَسترِفی", "فاجعه"),
    ],
    cap=("recipe رو «رِسایپ» نخون ❌", "e آخر این ۴ تا کلمه «ی» خونده میشه 💡 سیو کن"),
    stories=[
        REC(101, 3, pron=True),
        QZ("glisten", "t", "sparkles"),
        MC(101, 1, "ماشین", "کامیون", 0),
        AQ("یه کلمه که", "e آخرش", "خونده میشه؟", "ریپلای کن؛ تو ریلزهای بعدی\nمی‌گمش", "coffee"),
    ])

write_day(102,
    hook=H("اسم این ۴ تا میوه", "رو", "درست", "بگو!", "red_apple", "banana «بانانا» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «اَ»", "a"), "banana", "a", "banana", "🍌", "/bəˈnænə/", "بانانا", "بِنَنا", "موز", nth=1),
        W(GLOW("اینجا {EN} = «اِ»", "o"), "lemon", "o", "lemon", "🍋", "/ˈlemən/", "لِمون", "لِمِن", "لیمو"),
        W(GLOW("اینجا {EN} = «آ»", "o"), "olive", "o", "olive", "🫒", "/ˈɑːlɪv/", "اولیو", "آلیو", "زیتون"),
        W(GLOW("اینجا {EN} = «اَوِ»", "avo"), "avocado", "avo", "avocado", "🥑", "/ˌævəˈkɑːdoʊ/", "آووکادو", "اَوِکادُو", "آووکادو"),
    ],
    cap=("banana رو «بانانا» نخون ❌", "اسم این ۴ تا میوه رو این‌جوری بگو 🍌 برای دوستت بفرست"),
    stories=[
        REC(102, 0),
        QZV("Persia", "s", "classical_building", "«ژ»"),
        MC(102, 1, "بادام", "گردو", 2),
        AQ("میوه‌ی مورد علاقه‌ت", "به", "انگلیسی؟", "ریپلای کن؛ تلفظشو\nبرات می‌فرستم", "pineapple"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
CMT = "تو کدومشو می‌گفتی؟ کامنت کن 👇"

write_trial(96, "vocab", [
    dict(wrong="No.", right="I'll pass.", note="یعنی «من نیستم، ممنون»", emoji="raised_hand"),
    dict(wrong="I don't want to.", right="I'd rather not.", note="یعنی «ترجیح می‌دم نه»", emoji="person_gesturing_no"),
    dict(wrong="Not now.", right="Maybe another time.", note="یعنی «شاید یه وقت دیگه»", emoji="spiral_calendar"),
    dict(wrong="No, thanks.", right="I'm good, thanks.", note="یعنی «نه مرسی، لازم ندارم»", emoji="ok_hand"),
], ("مؤدبانه «نه» بگو 🙅", SAVE), suffix="a", headline="مؤدبانه نه بگو", head_emoji="raised_hand")
write_trial(96, "mistakes", [
    dict(wrong="I think no.", right="I don't think so.", note="«فکر نکنم» = I don't think so", emoji="thinking_face"),
    dict(wrong="I think yes.", right="I think so.", note="«فکر کنم آره» = I think so", emoji="thumbs_up"),
    dict(wrong="Yes, I don't like it.", right="No, I don't like it.", note="جواب منفی با No شروع میشه", emoji="cross_mark"),
], ("آره و نه رو این‌جوری نگو ❌", CMT), suffix="b")

write_trial(97, "vocab", [
    dict(wrong="watch many episodes", right="binge-watch", note="یعنی «پشت سر هم سریال دیدن»", emoji="television"),
    dict(wrong="telling the ending", right="spoiler", note="یعنی «لو دادن داستان»", emoji="speaking_head"),
    dict(wrong="surprise in the story", right="plot twist", note="یعنی «پیچش داستان»", emoji="exploding_head"),
    dict(wrong="part two of a movie", right="sequel", note="یعنی «قسمت بعدی فیلم»", emoji="clapper_board"),
], ("انگلیسی فیلم و سریال 🎬", SAVE), suffix="a", headline="انگلیسی فیلم و سریال", head_emoji="clapper_board")
write_trial(97, "mistakes", [
    dict(wrong="I went to cinema.", right="I went to the movies.", note="«سینما رفتم» به آمریکایی", emoji="popcorn"),
    dict(wrong="I'm fan of him.", right="I'm a big fan of his.", note="طرفدار کسی بودن = a fan of", emoji="star-struck"),
    dict(wrong="Put a song.", right="Play a song.", note="«آهنگ بذار» = play a song", emoji="musical_note"),
], ("فیلم و آهنگ رو این‌جوری نگو ❌", CMT), suffix="b")

write_trial(98, "vocab", [
    dict(wrong="very near", right="around the corner", note="یعنی «همین نزدیکی، سر کوچه»", emoji="round_pushpin"),
    dict(wrong="other side of street", right="across the street", note="یعنی «اون طرف خیابون»", emoji="world_map"),
    dict(wrong="It's easy to find.", right="You can't miss it.", note="یعنی «راحت پیداش می‌کنی»", emoji="eyes"),
    dict(wrong="5 minutes on foot", right="a five-minute walk", note="یعنی «پنج دقیقه پیاده»", emoji="person_walking"),
], ("آدرس دادن به انگلیسی 🗺️", SAVE), suffix="a", headline="انگلیسی آدرس دادن", head_emoji="world_map")
write_trial(98, "mistakes", [
    dict(wrong="Go direct.", right="Go straight.", note="«مستقیم برو» = go straight", emoji="up_arrow"),
    dict(wrong="Turn to left.", right="Turn left.", note="بعد از turn حرف to نمیاد", emoji="left_arrow"),
    dict(wrong="It's near to here.", right="It's near here.", note="بعد از near حرف to نمیاد", emoji="round_pushpin"),
], ("آدرس رو این‌جوری نده ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(99, "vocab", [
    dict(wrong="Sorry, sorry!", right="I owe you an apology.", note="یعنی «بهت یه عذرخواهی بدهکارم»", emoji="folded_hands"),
    dict(wrong="It was by mistake.", right="I didn't mean it.", note="یعنی «منظوری نداشتم»", emoji="pensive_face"),
    dict(wrong="I said it wrong.", right="I take it back.", note="یعنی «حرفمو پس می‌گیرم»", emoji="repeat_button"),
    dict(wrong="You're not angry?", right="No hard feelings?", note="یعنی «از دستم ناراحت نیستی؟»", emoji="handshake"),
], ("عذرخواهی مثل بومی‌ها 🙏", SAVE), suffix="a")
write_trial(99, "mistakes", [
    dict(wrong="Sorry for disturb.", right="Sorry to bother you.", note="«ببخشید مزاحم شدم»", emoji="person_bowing"),
    dict(wrong="Excuse me for late.", right="Sorry for being late.", note="«ببخشید دیر کردم»", emoji="alarm_clock"),
    dict(wrong="Welcome!", right="You're welcome!", note="جواب «مرسی» = you're welcome", emoji="smiling_face"),
], ("عذرخواهی و تشکر رو این‌جوری نگو ❌", CMT), suffix="b")

write_trial(100, "vocab", [
    dict(wrong="Help me, please.", right="Can you help me out?", note="یعنی «می‌تونی کمکم کنی؟»", emoji="raising_hands"),
    dict(wrong="Do you have time?", right="Got a minute?", note="یعنی «یه دقیقه وقت داری؟»", emoji="stopwatch"),
    dict(wrong="Is it a problem?", right="Would you mind?", note="یعنی «اشکالی نداره؟»", emoji="thinking_face"),
    dict(wrong="Can I sit here?", right="Is this seat taken?", note="یعنی «این صندلی خالیه؟»", emoji="seat"),
], ("مؤدبانه درخواست کن 🙏", SAVE), suffix="a")
write_trial(100, "mistakes", [
    dict(wrong="Who are you?", right="Who's calling?", note="پشت تلفن این‌جوری بپرس", emoji="telephone_receiver"),
    dict(wrong="Wait a little.", right="Hold on, please.", note="«گوشی دستت» = hold on", emoji="hourglass_not_done"),
    dict(wrong="I'm Ali.", right="This is Ali.", note="پشت تلفن: this is، نه I'm", emoji="mobile_phone"),
], ("پشت تلفن این‌جوری نگو ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(101, "vocab", [
    dict(wrong="talk unclearly", right="mumble", note="یعنی «زیر لب و نامفهوم حرف زدن»", emoji="zipper-mouth_face"),
    dict(wrong="talk proudly", right="brag", note="یعنی «پز دادن، لاف زدن»", emoji="smiling_face_with_sunglasses"),
    dict(wrong="talk about others", right="gossip", note="یعنی «غیبت کردن»", emoji="speaking_head"),
    dict(wrong="say you're unhappy", right="complain", note="یعنی «شکایت کردن، غر زدن»", emoji="pouting_face"),
], ("به جای say و talk این‌ها رو بگو 🗣️", SAVE), suffix="a")
write_trial(101, "mistakes", [
    dict(wrong="She have a car.", right="She has a car.", note="برای she و he: has", emoji="automobile"),
    dict(wrong="Does he likes it?", right="Does he like it?", note="بعد از does فعل ساده میاد", emoji="thinking_face"),
    dict(wrong="He can drives.", right="He can drive.", note="بعد از can فعل ساده میاد", emoji="oncoming_automobile"),
], ("این s ها جاشون اشتباهه ❌", CMT), suffix="b")

write_trial(102, "vocab", [
    dict(wrong="talk to people (party)", right="mingle", note="یعنی «با همه گپ زدن»", emoji="busts_in_silhouette"),
    dict(wrong="very fun", right="a blast", note="یعنی «فوق‌العاده خوش گذشت»", emoji="party_popper"),
    dict(wrong="invite friends home", right="have people over", note="یعنی «مهمون دعوت کردن»", emoji="house"),
    dict(wrong="leave (a place)", right="head out", note="یعنی «راه افتادن، رفتن»", emoji="door"),
], ("مهمونی به انگلیسی 🎉", SAVE), suffix="a")
write_trial(102, "mistakes", [
    dict(wrong="I bought two breads.", right="I bought some bread.", note="bread شمردنی نیست", emoji="bread"),
    dict(wrong="Give me a rice.", right="Give me some rice.", note="rice شمردنی نیست", emoji="cooked_rice"),
    dict(wrong="I have a good news!", right="I have good news!", note="news شمردنی نیست؛ a نمی‌گیره", emoji="newspaper"),
], ("این کلمه‌ها a نمی‌گیرن ❌", CMT), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(96, "You can't change the past, but you can change today.",
            "نمی‌تونی گذشته رو عوض کنی، ولی می‌تونی امروزو عوض کنی.",
            [("the past", "گذشته")], "سیو کن 📌", topic="change", figure=True)
write_quote(97, "Happiness is better when it's shared.",
            "خوشحالی وقتی تقسیم بشه قشنگ‌تره.",
            [("shared", "تقسیم شده")], "برای کسی که خوشحالیتو باهاش تقسیم می‌کنی بفرست 🤍", topic="happiness")
write_quote(98, "A small truth is better than a big lie.",
            "یه حقیقت کوچیک بهتر از یه دروغ بزرگه.",
            [("truth", "حقیقت"), ("lie", "دروغ")], "سیو کن 📌", topic="honesty", sea=True)
write_quote(99, "Your peace is more important than being right.",
            "آرامشت از حق با تو بودن مهم‌تره.",
            [("peace", "آرامش")], "سیو کن برای وقتایی که بحث پیش میاد 📌", topic="peace of mind", trees=True)
write_quote(100, "You don't need everyone to believe in you. Just you.",
            "لازم نیست همه بهت ایمان داشته باشن؛ فقط خودت.",
            [("believe in", "ایمان داشتن به")], "برای کسی که به خودش شک داره بفرست 💪", topic="self-belief", figure=True)
write_quote(101, "Falling down is part of learning to walk.",
            "زمین خوردن بخشی از یاد گرفتنِ راه رفتنه.",
            [("falling down", "زمین خوردن")], "برای کسی که تازه زمین خورده بفرست 🌱", topic="trying again")
write_quote(102, "Flowers don't bloom in one day.",
            "گل‌ها یه روزه شکوفه نمی‌دن.",
            [("bloom", "شکوفه دادن")], "سیو کن 📌", topic="patience", trees=True)
