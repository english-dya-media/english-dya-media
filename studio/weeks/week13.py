"""Week 13: Sat 23 Jan – Fri 29 Jan 2027 (days 82–88): reels, trial reels and quote reels (batch of 14 Nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

OUS = GLOW("اینجا {EN} = «اِس»", "ous")
TURE = GLOW("اینجا {EN} = «چِر»", "ture")
OU = GLOW("اینجا {EN} = «اُو»", "o")
G = GLOW("اینجا {EN} = «ج»", "g")

write_day(82,
    hook=H("این ۴ تا کلمه رو", "با", "«اوس»", "تموم نکن!", "cross_mark", "ous آخرش فقط «اِس»ه", "light_bulb"),
    words=[
        W(OUS, "jealous", "ous", "green_heart", "💚", "/ˈdʒeləs/", "جِلوس", "جِلِس", "حسود"),
        W(OUS, "nervous", "ous", "anxious_face_with_sweat", "😰", "/ˈnɜːrvəs/", "نِرووس", "نِروِس", "مضطرب، نگران"),
        W(OUS, "curious", "ous", "face_with_monocle", "🧐", "/ˈkjʊriəs/", "کیوریوس", "کیوریِس", "کنجکاو"),
        W(OUS, "famous", "ous", "glowing_star", "🌟", "/ˈfeɪməs/", "فِیموس", "فِیمِس", "معروف"),
    ],
    cap=("famous رو «فیموس» نخون ❌", "ous آخر این ۴ تا کلمه فقط «اِس»ه 💡 برای دوستت بفرست"),
    stories=[
        REC(82, 0, pron=True),
        QZV("choose", "s", "thinking_face", "«ز»"),
        MC(82, 3, "آب‌پرتقال", "چای", 1),
        AQ("یه کلمه که با", "ous", "تموم میشه؟", "ریپلای کن؛ تلفظ درستشو\nبرات می‌گم", "delicious"),
    ])

write_day(83,
    hook=H("تو این ۴ تا کلمه", "gh", "رو نخون!", "صداش نیست!", "zipper-mouth_face", "daughter میشه «دادِر»", "light_bulb"),
    words=[
        W(SIL("gh"), "daughter", "gh", "girl", "👧", "/ˈdɔːɾər/", "داگتِر", "دادِر", "دختر (فرزند)"),
        W(SIL("gh"), "caught", "gh", "fishing_pole", "🎣", "/kɔːt/", "کاگت", "کات", "گرفت؛ گیر انداخت"),
        W(SIL("gh"), "taught", "gh", "teacher", "🧑‍🏫", "/tɔːt/", "تاگت", "تات", "یاد داد"),
        W(SIL("gh"), "straight", "gh", "straight_ruler", "📏", "/streɪt/", "استرِیگت", "سْترِیت", "مستقیم، صاف"),
    ],
    cap=("daughter رو «داگتِر» نخون ❌", "gh تو این ۴ تا کلمه خونده نمیشه 🤐 سیو کن"),
    stories=[
        REC(83, 2),
        QZ("raspberry", "p", "blueberries"),
        MC(83, 1, "خوشحال", "عصبانی", 0),
        AQ("کدوم حرف بی‌صدا", "از همه", "عجیب‌تره؟", "ریپلای کن؛ ریلز بعدی\nشاید درباره‌ی اون باشه", "knife"),
    ])

write_day(84,
    hook=H("این ۴ تا برند رو", "انگلیسی", "بگو", "این‌جوری!", "speaker_high_volume", "Siemens تو انگلیسی «سیمِنز»ه", "light_bulb"),
    words=[
        W(GLOW("اینجا {EN} = «اِی»", "A"), "Asus", "A", "laptop", "💻", "/ˈeɪsuːs/", "آسوس", "اِیسوس", "برند لپ‌تاپ",
          ph="ˈeɪsuːs"),
        W(GLOW("اینجا {EN} = «س»", "S"), "Siemens", "S", "gear", "⚙️", "/ˈsiːmənz/", "زیمنس", "سیمِنز", "برند لوازم برقی"),
        W(GLOW("اینجا {EN} = «آ»", "o"), "Bosch", "o", "hammer_and_wrench", "🛠️", "/bɑːʃ/", "بوش", "باش", "برند ابزار"),
        W(GLOW("اینجا {EN} = «ای»", "e"), "Nivea", "e", "lotion_bottle", "🧴", "/nɪˈviːə/", "نیوآ", "نیویا", "برند کرم",
          ph="nɪvˈiːə"),
    ],
    cap=("Siemens و Bosch رو انگلیسی‌ها چطوری می‌گن؟ 🔊", "اسم این ۴ تا برند به انگلیسی این‌جوریه 💡 برای دوستت بفرست"),
    stories=[
        REC(84, 0),
        QZV("emotion", "t", "smiling_face_with_hearts", "«ش»"),
        MC(84, 3, "خمیده", "دور", 2),
        AQ("برند مورد علاقه‌ت", "رو", "بنویس", "ریپلای کن تا تلفظ انگلیسیشو\nبرات بگم", "Lacoste"),
    ])

write_day(85,
    hook=H("ture آخر کلمه", "«تور»", "نیست!", "«چِر»ه", "cross_mark", "culture میشه «کالچِر»", "light_bulb"),
    words=[
        W(TURE, "culture", "ture", "classical_building", "🏛️", "/ˈkʌltʃər/", "کولتور", "کالچِر", "فرهنگ"),
        W(TURE, "temperature", "ture", "thermometer", "🌡️", "/ˈtemprətʃər/", "تمپراتور", "تِمپرِچِر", "دما"),
        W(TURE, "literature", "ture", "books", "📚", "/ˈlɪtərətʃər/", "لیتراتور", "لیدِرِچِر", "ادبیات"),
        W(TURE, "adventure", "ture", "compass", "🧭", "/ədˈventʃər/", "آوانتور", "اِدوِنچِر", "ماجراجویی"),
    ],
    cap=("temperature رو «تمپراتور» نخون ❌", "ture آخر کلمه «چِر» خونده میشه 💡 سیو کن"),
    stories=[
        REC(85, 1, pron=True),
        QZ("numb", "b", "cold_face"),
        MC(85, 2, "بوش", "بُش", 0, pron=True),
        AQ("یه کلمه با ture", "که", "سخته؟", "ریپلای کن؛ تو ریلزهای بعدی\nمی‌گمش", "furniture"),
    ])

write_day(86,
    hook=H("این ۴ تا کلمه رو", "با", "«آ»", "نخون!", "cross_mark", "o این‌جا «اُو»ه، مثل go", "light_bulb"),
    words=[
        W(OU, "only", "o", "index_pointing_up", "☝️", "/ˈoʊnli/", "آنلی", "اُونلی", "فقط"),
        W(OU, "both", "o", "people_hugging", "🫂", "/boʊθ/", "باث", "بُوث", "هر دو"),
        W(OU, "most", "o", "chart_increasing", "📈", "/moʊst/", "ماست", "مُوست", "بیشترین"),
        W(OU, "won't", "o", "no_entry", "⛔", "/woʊnt/", "وانت", "وُونت", "نخواهد کرد"),
    ],
    cap=("won't رو «وانت» نخون ❌", "won't = «وُونت» و want = «وانت» 💡 o این ۴ تا کلمه «اُو»ه؛ سیو کن"),
    stories=[
        REC(86, 0),
        QZV("pleasant", "s", "smiling_face", "«ز»"),
        MC(86, 3, "سرزمین", "سفر", 1),
        AQ("want و won't رو", "قاطی", "می‌کنی؟", "ریپلای کن؛ با یه جمله\nتمرینش کنیم", "I won't go"),
    ])

write_day(87,
    hook=H("این ۴ تا کلمه‌ی", "پزشکی", "رو", "درست بگو", "stethoscope", "allergy «آلرژی» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «سین»", "cine"), "vaccine", "cine", "syringe", "💉", "/vækˈsiːn/", "واکسن", "وَکسین", "واکسن"),
        W(G, "allergy", "g", "sneezing_face", "🤧", "/ˈælərdʒi/", "آلرژی", "اَلِرجی", "حساسیت"),
        W(GLOW("اینجا {EN} = «بای»", "bi"), "antibiotic", "bi", "pill", "💊", "/ˌæntibaɪˈɑːɾɪk/", "آنتی‌بیوتیک", "اَنتی‌بایادیک",
          "آنتی‌بیوتیک"),
        W(GLOW("اینجا {EN} = «آی»", "i"), "migraine", "i", "face_with_head-bandage", "🤕", "/ˈmaɪɡreɪn/", "میگرن", "مایگرِین",
          "میگرن"),
    ],
    cap=("allergy رو «آلرژی» نگو ❌", "این ۴ تا کلمه‌ی پزشکی رو انگلیسی بگو 🩺 برای دوستت بفرست"),
    stories=[
        REC(87, 1),
        QZ("knob", "k", "door"),
        MC(87, 2, "کمترین", "همیشه", 0),
        AQ("یه کلمه‌ی پزشکی", "که", "تلفظش سخته؟", "ریپلای کن تا تو ریلزهای بعدی\nبگمش", "ambulance"),
    ])

write_day(88,
    hook=H("اسم این ۴ تا حیوون", "رو", "درست", "بگو!", "paw_prints", "giraffe «زرافه» نیست!", "speaker_high_volume"),
    words=[
        W(G, "giraffe", "g", "giraffe", "🦒", "/dʒəˈræf/", "زرافه", "جِرَف", "زرافه"),
        W(GLOW("اینجا {EN} = «ک»", "ch"), "chameleon", "ch", "lizard", "🦎", "/kəˈmiːliən/", "شامِلئون", "کِمیلیِن", "آفتاب‌پرست"),
        W(GLOW("اینجا {EN} = «اِ»", "o"), "gorilla", "o", "gorilla", "🦍", "/ɡəˈrɪlə/", "گوریل", "گِریلا", "گوریل"),
        W(GLOW("اینجا {EN} = «کی»", "qui"), "mosquito", "qui", "mosquito", "🦟", "/məˈskiːɾoʊ/", "موسکوئیتو", "مِسکیدُو", "پشه"),
    ],
    cap=("chameleon رو «شامِلئون» نخون ❌", "اسم این ۴ تا حیوون رو این‌جوری بگو 🦒 برای دوستت بفرست"),
    stories=[
        REC(88, 3, pron=True),
        QZV("anchor", "ch", "anchor", "«ک»"),
        MC(88, 0, "آمپول", "قرص", 2),
        AQ("حیوون مورد علاقه‌ت", "به", "انگلیسی؟", "ریپلای کن؛ تلفظشو\nبرات می‌فرستم", "penguin"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
CMT = "تو کدومشو می‌گفتی؟ کامنت کن 👇"

write_trial(82, "vocab", [
    dict(wrong="very good", right="terrific", note="یعنی «فوق‌العاده»", emoji="star-struck"),
    dict(wrong="the best quality", right="top-notch", note="یعنی «درجه‌یک، عالی»", emoji="1st_place_medal"),
    dict(wrong="better than all others", right="outstanding", note="یعنی «برجسته، بی‌نظیر»", emoji="trophy"),
    dict(wrong="amazingly good", right="phenomenal", note="یعنی «خارق‌العاده»", emoji="sparkles"),
], ("به جای very good این ۴ تا رو بگو 😎", SAVE), suffix="a")
write_trial(82, "mistakes", [
    dict(wrong="Me and my friend went.", right="My friend and I went.", note="فاعل I میشه و اسم بقیه اول میاد", emoji="people_hugging"),
    dict(wrong="He is a friend of me.", right="He's a friend of mine.", note="a friend of mine، نه of me", emoji="handshake"),
    dict(wrong="Between you and I", right="Between you and me", note="بعد از between: me", emoji="shushing_face"),
], ("ضمیرها رو این‌جوری نگو ❌", CMT), suffix="b")

write_trial(83, "vocab", [
    dict(wrong="very bad", right="dreadful", note="یعنی «افتضاح، وحشتناک»", emoji="face_screaming_in_fear"),
    dict(wrong="bad quality", right="lousy", note="یعنی «بنجل، مزخرف»", emoji="thumbs_down"),
    dict(wrong="not good, not bad", right="mediocre", note="یعنی «معمولی، متوسط»", emoji="neutral_face"),
    dict(wrong="very weak and sad", right="pathetic", note="یعنی «رقت‌انگیز، ضعیف»", emoji="pensive_face"),
], ("به جای bad این ۴ تا رو بگو 👎", SAVE), suffix="a")
write_trial(83, "mistakes", [
    dict(wrong="Close the music.", right="Turn off the music.", note="خاموش کردن = turn off", emoji="musical_note"),
    dict(wrong="Open the radio.", right="Turn on the radio.", note="روشن کردن = turn on", emoji="radio"),
    dict(wrong="Make the volume high.", right="Turn it up.", note="صدا رو زیاد کردن = turn up", emoji="speaker_high_volume"),
], ("open و close رو این‌جا نگو ❌", CMT), suffix="b")

write_trial(84, "vocab", [
    dict(wrong="like very much", right="adore", note="یعنی «عاشق چیزی بودن»", emoji="smiling_face_with_hearts"),
    dict(wrong="I like music.", right="I'm into music.", note="یعنی «اهل موسیقی‌ام»", emoji="headphone"),
    dict(wrong="hate", right="can't stand", note="یعنی «اصلاً تحمل نکردن»", emoji="face_with_symbols_on_mouth"),
    dict(wrong="like (kindly)", right="be fond of", note="یعنی «علاقه داشتن، دوست داشتن»", emoji="red_heart"),
], ("به جای like و hate این‌ها رو بگو ❤️", SAVE), suffix="a")
write_trial(84, "mistakes", [
    dict(wrong="I saw it in TV.", right="I saw it on TV.", note="تو تلویزیون = on TV", emoji="television"),
    dict(wrong="He's in the phone.", right="He's on the phone.", note="پشت تلفن = on the phone", emoji="telephone_receiver"),
    dict(wrong="It's in the radio.", right="It's on the radio.", note="از رادیو = on the radio", emoji="radio"),
], ("in یا on؟ این ۳ تا رو اشتباه می‌گی ❌", CMT), suffix="b")

write_trial(85, "vocab", [
    dict(wrong="very soon", right="in no time", note="یعنی «تو یه چشم به هم زدن»", emoji="high_voltage"),
    dict(wrong="for a long time", right="for ages", note="یعنی «یه عمره، خیلی وقته»", emoji="hourglass_done"),
    dict(wrong="sometimes", right="now and then", note="یعنی «گاهی وقتا»", emoji="spiral_calendar"),
    dict(wrong="immediately", right="right away", note="یعنی «همین الان، فوراً»", emoji="stopwatch"),
], ("زمان رو مثل بومی‌ها بگو ⏰", SAVE), suffix="a")
write_trial(85, "mistakes", [
    dict(wrong="I go always there.", right="I always go there.", note="always قبل از فعل میاد", emoji="repeat_button"),
    dict(wrong="I yesterday saw him.", right="I saw him yesterday.", note="yesterday آخر جمله میاد", emoji="calendar"),
    dict(wrong="He can very well swim.", right="He can swim very well.", note="very well بعد از فعل میاد", emoji="person_swimming"),
], ("کلمه‌ها رو به ترتیب فارسی نچین ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(86, "vocab", [
    dict(wrong="be patient", right="hold your horses", note="یعنی «صبر کن، عجله نکن»", emoji="horse"),
    dict(wrong="feel out of place", right="a fish out of water", note="یعنی «غریب و ناجور»", emoji="fish"),
    dict(wrong="raining very hard", right="raining cats and dogs", note="یعنی «بارون شدید»", emoji="cloud_with_rain"),
    dict(wrong="get too scared to do", right="chicken out", note="یعنی «از ترس جا زدن»", emoji="chicken"),
], ("اصطلاح‌های حیوونی که بومی‌ها می‌گن 🐴", SAVE), suffix="a", headline="اصطلاح‌هایی که بومی‌ها می‌گن",
   head_emoji="speech_balloon")
write_trial(86, "mistakes", [
    dict(wrong="I win money at work.", right="I earn money at work.", note="پول درآوردن = earn", emoji="money_bag"),
    dict(wrong="Borrow me your pen.", right="Can I borrow your pen?", note="borrow = قرض گرفتن، نه دادن", emoji="pen"),
    dict(wrong="Rise your hand.", right="Raise your hand.", note="بالا بردن چیزی = raise", emoji="person_raising_hand"),
], ("این فعل‌ها رو با هم قاطی نکن ❌", CMT), suffix="b")

write_trial(87, "vocab", [
    dict(wrong="I'm getting better.", right="I'm on the mend.", note="یعنی «دارم خوب میشم»", emoji="relieved_face"),
    dict(wrong="My head is turning.", right="I feel dizzy.", note="یعنی «سرم گیج میره»", emoji="face_with_spiral_eyes"),
    dict(wrong="My throat hurts.", right="I have a sore throat.", note="یعنی «گلوم درد می‌کنه»", emoji="face_with_thermometer"),
    dict(wrong="very very tired", right="dog-tired", note="یعنی «خسته و کوفته»", emoji="dog_face"),
], ("حال جسمی‌تو مثل بومی‌ها بگو 🤒", SAVE), suffix="a")
write_trial(87, "mistakes", [
    dict(wrong="I have cold.", right="I have a cold.", note="سرماخوردگی = a cold", emoji="sneezing_face"),
    dict(wrong="I took a cold.", right="I caught a cold.", note="سرما خوردن = catch a cold", emoji="snowflake"),
    dict(wrong="I went to doctor.", right="I went to the doctor.", note="رفتن پیش دکتر = the doctor", emoji="stethoscope"),
], ("سرما خوردی؟ این‌جوری نگو ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(88, "vocab", [
    dict(wrong="suddenly", right="out of the blue", note="یعنی «یهویی، بی‌مقدمه»", emoji="blue_circle"),
    dict(wrong="very jealous", right="green with envy", note="یعنی «از حسادت ترکیدن»", emoji="green_heart"),
    dict(wrong="sad", right="feeling blue", note="یعنی «دلگیر، غمگین»", emoji="blue_heart"),
    dict(wrong="a small harmless lie", right="a white lie", note="یعنی «دروغ مصلحتی»", emoji="white_heart"),
], ("اصطلاح‌های رنگی انگلیسی 🎨", SAVE), suffix="a", headline="اصطلاح‌هایی که بومی‌ها می‌گن",
   head_emoji="artist_palette")
write_trial(88, "mistakes", [
    dict(wrong="The movie was bored.", right="The movie was boring.", note="چیزی که حوصله سر می‌بره = boring", emoji="yawning_face"),
    dict(wrong="I'm interesting in art", right="I'm interested in art.", note="علاقه داشتن = interested in", emoji="artist_palette"),
    dict(wrong="I was very exciting.", right="I was so excited.", note="حس آدم = excited", emoji="star-struck"),
], ("ed یا ing؟ این ۳ تا رو اشتباه می‌گی ❌", CMT), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(82, "Family is not always blood. It's the people who stay.",
            "خانواده همیشه هم‌خون نیست؛ آدماییه که می‌مونن.",
            [("blood", "خون")], "برای خانواده‌ی واقعیت بفرست 🤍", topic="family")
write_quote(83, "Time is the most valuable thing you can give.",
            "زمان باارزش‌ترین چیزیه که می‌تونی به کسی بدی.",
            [("valuable", "باارزش")], "سیو کن 📌", topic="time", sea=True)
write_quote(84, "Plant seeds today for the flowers of tomorrow.",
            "امروز بذر بکار، برای گل‌های فردا.",
            [("seeds", "بذرها")], "سیو کن 📌", topic="the future", trees=True)
write_quote(85, "Gratitude turns what we have into enough.",
            "قدردانی، هر چی داریم رو کافی می‌کنه.",
            [("gratitude", "قدردانی"), ("enough", "کافی")], "برای کسی که ازش ممنونی بفرست 🙏", topic="gratitude")
write_quote(86, "A tired mind can't see clearly. Rest first.",
            "ذهن خسته نمی‌تونه درست ببینه؛ اول استراحت کن.",
            [("tired", "خسته"), ("clearly", "واضح")], "سیو کن برای وقتی که خسته‌ای 📌", topic="rest", figure=True)
write_quote(87, "Love makes ordinary days feel special.",
            "عشق روزای معمولی رو خاص می‌کنه.",
            [("ordinary", "معمولی")], "برای کسی که روزاتو خاص می‌کنه بفرست 🤍", topic="love")
write_quote(88, "Courage is one step ahead of fear.",
            "شجاعت یعنی یه قدم جلوتر از ترس بودن.",
            [("ahead of", "جلوتر از")], "برای یه آدم شجاع بفرست 💪", topic="courage", figure=True)
