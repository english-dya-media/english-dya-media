"""Week 9: Sat 26 Dec 2026 – Fri 1 Jan 2027 (days 54–60): reels, trial reels and quote reels (batch of 14 Nov).
Day 60 (1 Jan) is New Year: the month names Persian speakers say the French way."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

TH = GLOW(f"صدای {{EN}}: زبون بین دندون{ZW}ها", "th", "tongue")
FL = lambda s: GLOW("اینجا {EN} شبیه «د»", s)
CL = lambda tip_en: GLOW("{EN} بدون «اِ» اولش", tip_en)
EA = GLOW("اینجا {EN} = «اِ»", "ea")

write_day(54,
    hook=H("این ۴ تا کلمه رو", "آمریکایی", "بگو", "t میشه «د»!", "speaker_high_volume", "مثل water که میشه «وادِر»", "light_bulb"),
    words=[
        W(FL("t"), "later", "t", "hourglass_not_done", "⏳", "/ˈleɪɾər/", "لِیتِر", "لِیدِر", "بعداً"),
        W(FL("t"), "meeting", "t", "spiral_notepad", "🗒️", "/ˈmiːɾɪŋ/", "میتینگ", "میدینگ", "جلسه"),
        W(FL("t"), "beautiful", "t", "sunflower", "🌻", "/ˈbjuːɾəfəl/", "بیوتیفول", "بیودِفِل", "زیبا"),
        W(FL("tt"), "little", "tt", "baby_chick", "🐤", "/ˈlɪɾəl/", "لیتِل", "لیدِل", "کوچیک، کم"),
    ],
    cap=("beautiful رو «بیوتیفول» نخون ❌", "آمریکایی‌ها t این ۴ تا کلمه رو «د» می‌گن 🇺🇸 سیو کن"),
    stories=[
        REC(54, 1),
        QZ("folk", "l", "guitar"),
        MC(54, 0, "دِیتا", "دیتا", 2, pron=True),
        AQ("یه کلمه با t وسطش", "که", "سخته؟", "ریپلای کن تا تلفظ آمریکاییشو\nتو ریلزهای بعدی بگم", "computer"),
    ])

write_day(55,
    hook=H("تو این ۴ تا کلمه", "حرف", "l", "رو نخون!", "zipper-mouth_face", "l این‌جا فقط برای ظاهره!", "light_bulb"),
    words=[
        W(SIL("l"), "would", "l", "crystal_ball", "🔮", "/wʊd/", "وولد", "وُد", "فعل کمکی شرطی"),
        W(SIL("l"), "should", "l", "backhand_index_pointing_up", "☝️", "/ʃʊd/", "شولد", "شُد", "باید (توصیه)"),
        W(SIL("l"), "chalk", "l", "school", "🏫", "/tʃɔːk/", "چالک", "چاک", "گچ"),
        W(SIL("l"), "almond", "l", "chestnut", "🌰", "/ˈɑːmənd/", "آلموند", "آمِند", "بادام"),
    ],
    cap=("would و should رو با «ل» نخون ❌", "l تو این ۴ تا کلمه خونده نمیشه 🤐 برای دوستت بفرست"),
    stories=[
        REC(55, 0),
        QZV("reason", "s", "thinking_face", "«ز»"),
        MC(55, 2, "زشت", "بزرگ", 1),
        AQ("کدوم حرف بی‌صدا", "بیشتر", "گیجت می‌کنه؟", "ریپلای کن؛ هفته‌ی بعد\nیه ریلز براش می‌سازم", "salmon"),
    ])

write_day(56,
    hook=H("این ۴ تا کلمه رو", "با", "«ت»", "نگو!", "cross_mark", "th تو nothing و something «ث»ه", "tongue"),
    words=[
        W(TH, "nothing", "th", "keycap_0", "0️⃣", "/ˈnʌθɪŋ/", "ناتینگ", "ناثینگ", "هیچی"),
        W(TH, "everything", "th", "globe_with_meridians", "🌐", "/ˈevriθɪŋ/", "اِوریتینگ", "اِوریثینگ", "همه‌چیز"),
        W(TH, "something", "th", "wrapped_gift", "🎁", "/ˈsʌmθɪŋ/", "سامتینگ", "سامثینگ", "یه چیزی"),
        W(TH, "truth", "th", "magnifying_glass_tilted_left", "🔍", "/truːθ/", "تروت", "تروث", "حقیقت"),
    ],
    cap=("nothing رو «ناتینگ» نگو ❌", "th این‌جا «ث»ه: زبون بین دندون‌ها و فوت 👅 برای دوستت بفرست"),
    stories=[
        REC(56, 2),
        QZ("calf", "l", "cow_face"),
        MC(56, 3, "گردو", "پسته", 0),
        AQ("یه کلمه با th که", "تلفظش", "سخته؟", "ریپلای کن تا تو ریلزهای بعدی\nبا هم تمرینش کنیم", "anything"),
    ])

write_day(57,
    hook=H("اسم این ۴ تا کشور", "رو", "اشتباه", "می‌گی!", "world_map", "انگلیسی‌ها این‌جوری می‌گن", "speaker_high_volume"),
    words=[
        W(FL("t"), "Italy", "t", "pizza", "🍕", "/ˈɪɾəli/", "ایتالیا", "ایدِلی", "ایتالیا"),
        W(GLOW("اینجا {EN} = «کس»", "x"), "Mexico", "x", "hot_pepper", "🌶️", "/ˈmeksɪkoʊ/", "مِکزیک", "مِکسیکو", "مکزیک"),
        W(GLOW("اینجا {EN} = «اَ»", "a"), "Canada", "a", "maple_leaf", "🍁", "/ˈkænədə/", "کانادا", "کَنِدا", "کانادا"),
        W(GLOW("اینجا {EN} = «اِی»", "a"), "Australia", "a", "koala", "🐨", "/ɔːˈstreɪliə/", "اِسترالیا", "آستْرِیلیا", "استرالیا", nth=1),
    ],
    cap=("ایتالیا و استرالیا به انگلیسی چی میشن؟ 😳", "Italy میشه «ایدِلی» و Australia میشه «آستْرِیلیا» 🌍 برای دوستت بفرست"),
    stories=[
        REC(57, 3),
        QZV("gentle", "g", "dove", "«ج»"),
        MC(57, 0, "همه‌چیز", "یه چیزی", 1),
        AQ("اسم کدوم کشور رو", "مطمئن", "نیستی؟", "ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی بگم", "Switzerland"),
    ])

write_day(58,
    hook=H("این ۴ تا کلمه رو", "با", "«ای»", "نخون!", "cross_mark", "ea این‌جا یه «اِ»ی کوتاهه", "light_bulb"),
    words=[
        W(EA, "bread", "ea", "bread", "🍞", "/bred/", "برید", "بْرِد", "نان"),
        W(EA, "head", "ea", "bust_in_silhouette", "👤", "/hed/", "هید", "هِد", "سر"),
        W(EA, "heavy", "ea", "person_lifting_weights", "🏋️", "/ˈhevi/", "هیوی", "هِوی", "سنگین"),
        W(EA, "breakfast", "ea", "bacon", "🥓", "/ˈbrekfəst/", "بریکفست", "بْرِکفِست", "صبحانه"),
    ],
    cap=("bread رو «برید» نخون ❌", "ea تو این ۴ تا کلمه یه «اِ»ی کوتاهه 💡 سیو کن"),
    stories=[
        REC(58, 2, pron=True),
        QZ("stalk", "l", "sunflower"),
        MC(58, 0, "ایتالیا", "ایتالی", 1, pron=True),
        AQ("یه کلمه با ea", "که", "گیجت می‌کنه؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "weather"),
    ])

write_day(59,
    hook=H("این ۴ تا کلمه رو", "با", "«اِ»", "شروع نکن!", "cross_mark", "sk و sw و str بدون «اِ»", "speaker_high_volume"),
    words=[
        W(CL("sk"), "sky", "sk", "cloud", "☁️", "/skaɪ/", "اِسکای", "سْکای", "آسمان"),
        W(CL("sw"), "swim", "sw", "person_swimming", "🏊", "/swɪm/", "اِسویم", "سْویم", "شنا کردن"),
        W(CL("str"), "strong", "str", "flexed_biceps", "💪", "/strɔːŋ/", "اِسترانگ", "سْترانگ", "قوی"),
        W(CL("spr"), "spring", "spr", "cherry_blossom", "🌸", "/sprɪŋ/", "اِسپرینگ", "سْپْرینگ", "بهار؛ فنر"),
    ],
    cap=("sky رو «اِسکای» نگو ❌", "مستقیم با s شروع کن: «سْکای» 💡 برای دوستت بفرست"),
    stories=[
        REC(59, 0),
        QZV("imagine", "g", "thought_balloon", "«ج»"),
        MC(59, 2, "سبک", "بلند", 0),
        AQ("یه کلمه که با", "«اِ»", "شروعش می‌کنی؟", "ریپلای کن تا تو ریلزهای بعدی\nتلفظ درستشو بگم", "Steve"),
    ])

write_day(60,
    hook=H("سال نو مبارک!", "اسم ماه‌ها", "رو", "درست بگو", "party_popper", "ژانویه و فوریه فرانسوی‌ان!", "calendar"),
    words=[
        W(GLOW("اینجا {EN} = «ج»", "J"), "January", "J", "calendar", "📅", "/ˈdʒænjueri/", "ژانویه", "جَنیوئِری", "ژانویه"),
        W(GLOW("اینجا {EN} = «یوئِری»", "ruary"), "February", "ruary", "snowflake", "❄️", "/ˈfebjueri/", "فوریه", "فِبیوئِری", "فوریه"),
        W(GLOW("اینجا {EN} = «ج»", "J"), "June", "J", "sun", "☀️", "/dʒuːn/", "ژوئن", "جون", "ژوئن"),
        W(GLOW("اینجا {EN} = «آگ»", "Aug"), "August", "Aug", "beach_with_umbrella", "🏖️", "/ˈɔːɡəst/", "اوت", "آگِست", "اوت"),
    ],
    cap=("سال نو میلادی مبارک 🎉 ژانویه به انگلیسی میشه January", "اسم این ۴ تا ماه رو فرانسوی نگو 💡 برای دوستت بفرست"),
    stories=[
        REC(60, 3),
        QZ("design", "g", "artist_palette"),
        MC(60, 1, "دویدن", "پریدن", 2),
        AQ("امسال می‌خوای", "چی", "یاد بگیری؟", "ریپلای کن؛ تو ریلزهای بعدی\nبراش محتوا می‌سازم", "speaking"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
SEND = "برای دوستت بفرست که اونم یاد بگیره 👇"

write_trial(54, "vocab", [
    dict(wrong="Are you okay?", right="You alright?", note="یعنی «خوبی؟ حالت خوبه؟»", emoji="hugging_face"),
    dict(wrong="What's wrong?", right="What's the matter?", note="یعنی «چی شده؟»", emoji="worried_face"),
    dict(wrong="Why?", right="How come?", note="یعنی «چطور مگه؟»", emoji="thinking_face"),
    dict(wrong="Everything is good.", right="All good!", note="یعنی «همه چی رو به راهه»", emoji="ok_hand"),
], ("این‌جوری حال دوستتو بپرس 😎", SEND), suffix="a")
write_trial(54, "mistakes", [
    dict(wrong="He mentioned about it.", right="He mentioned it.", note="بعد از mention حرف about نمیاد", emoji="speech_balloon"),
    dict(wrong="Emphasize on this.", right="Emphasize this.", note="emphasize خودش یعنی تأکید کردن روی", emoji="red_exclamation_mark"),
    dict(wrong="We reached to Tehran.", right="We reached Tehran.", note="بعد از reach حرف to نمیاد", emoji="round_pushpin"),
], ("این ۳ تا فعل حرف اضافه نمی‌خوان ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(55, "vocab", [
    dict(wrong="very good", right="superb", note="یعنی «عالی، معرکه»", emoji="trophy"),
    dict(wrong="very long", right="endless", note="یعنی «تموم‌نشدنی»", emoji="infinity"),
    dict(wrong="very new", right="brand-new", note="یعنی «نوِ نو، آک»", emoji="wrapped_gift"),
    dict(wrong="very tired", right="worn out", note="یعنی «خسته و کوفته»", emoji="tired_face"),
], ("very رو بذار کنار؛ این ۴ تا رو بگو 😎", SAVE), suffix="a")
write_trial(55, "mistakes", [
    dict(wrong="I suggest you to go.", right="I suggest you go.", note="بعد از suggest، to نمیاد", emoji="light_bulb"),
    dict(wrong="Make me to laugh.", right="Make me laugh.", note="بعد از make + کسی، to نمیاد", emoji="face_with_tears_of_joy"),
    dict(wrong="Let me to explain.", right="Let me explain.", note="بعد از let me، to نمیاد", emoji="person_tipping_hand"),
], ("این to ها اضافه‌ست ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(56, "vocab", [
    dict(wrong="raise (a child)", right="bring up", note="یعنی «بچه بزرگ کردن»", emoji="baby"),
    dict(wrong="explode", right="blow up", note="یعنی «منفجر شدن»", emoji="collision"),
    dict(wrong="invent (a story)", right="make up", note="یعنی «از خودت درآوردن»", emoji="open_book"),
    dict(wrong="manage (with little)", right="get by", note="یعنی «سر کردن، گذروندن»", emoji="coin"),
], ("بومی‌ها به جای این ۴ تا فعل این‌جوری می‌گن 😎", SAVE), suffix="a", headline="فعل‌هایی که بومی‌ها می‌گن")
write_trial(56, "mistakes", [
    dict(wrong="She is my brother.", right="He is my brother.", note="برای مرد he، برای زن she", emoji="boy"),
    dict(wrong="Her name is Ali.", right="His name is Ali.", note="برای مرد his", emoji="man"),
    dict(wrong="He is my sister.", right="She is my sister.", note="برای زن she", emoji="girl"),
], ("فارسی he و she نداره؛ واسه همین قاطی می‌کنیم ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(57, "vocab", [
    dict(wrong="timetable", right="schedule", note="یعنی «برنامه‌ی زمانی» به آمریکایی", emoji="spiral_calendar"),
    dict(wrong="garden", right="yard", note="یعنی «حیاط» به آمریکایی", emoji="house_with_garden"),
    dict(wrong="shop", right="store", note="یعنی «مغازه» به آمریکایی", emoji="convenience_store"),
    dict(wrong="aubergine", right="eggplant", note="یعنی «بادمجون» به آمریکایی", emoji="eggplant"),
], ("این ۴ تا کلمه رو آمریکایی بگو 🇺🇸", SAVE), suffix="a", headline="آمریکایی حرف بزن")
write_trial(57, "mistakes", [
    dict(wrong="Two hundreds", right="Two hundred", note="hundred بعد از عدد s نمی‌گیره", emoji="hundred_points"),
    dict(wrong="Three thousands", right="Three thousand", note="thousand هم بعد از عدد مفرده", emoji="money_bag"),
    dict(wrong="Millions people", right="Millions of people", note="بعد از millions حرف of میاد", emoji="busts_in_silhouette"),
], ("عددها رو این‌جوری نگو ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(58, "vocab", [
    dict(wrong="very expensive", right="costs an arm and a leg", note="یعنی «خیلی گرونه»", emoji="money_with_wings"),
    dict(wrong="stop working today", right="call it a day", note="یعنی «امروز دیگه بسه»", emoji="chequered_flag"),
    dict(wrong="undecided", right="on the fence", note="یعنی «مردد، دودل»", emoji="thinking_face"),
    dict(wrong="agree completely", right="see eye to eye", note="یعنی «کاملاً هم‌نظر بودن»", emoji="eyes"),
], ("این اصطلاح‌ها رو بومی‌ها هر روز می‌گن 😎", SAVE), suffix="a", headline="اصطلاح‌هایی که بومی‌ها می‌گن",
   head_emoji="speech_balloon")
write_trial(58, "mistakes", [
    dict(wrong="I'm in home.", right="I'm at home.", note="«خونه‌ام» = at home", emoji="house"),
    dict(wrong="In the weekend", right="On the weekend", note="به آمریکایی on the weekend", emoji="beach_with_umbrella"),
    dict(wrong="In 5 o'clock", right="At 5 o'clock", note="برای ساعت at میاد", emoji="alarm_clock"),
], ("in و on و at رو این‌جا اشتباه می‌ذاری ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(59, "vocab", [
    dict(wrong="I'm scared.", right="I'm freaking out.", note="یعنی «دارم وحشت می‌کنم»", emoji="face_screaming_in_fear"),
    dict(wrong="I'm a little sick.", right="I'm under the weather.", note="یعنی «یه کم ناخوشم»", emoji="face_with_thermometer"),
    dict(wrong="I'm busy.", right="I'm tied up.", note="یعنی «درگیرم، سرم شلوغه»", emoji="spiral_calendar"),
    dict(wrong="I'm nervous.", right="I've got butterflies.", note="یعنی «دلم شور می‌زنه»", emoji="butterfly"),
], ("حال‌تو مثل بومی‌ها بگو 😎", SAVE), suffix="a")
write_trial(59, "mistakes", [
    dict(wrong="Many money", right="A lot of money", note="money شمردنی نیست؛ many نمی‌گیره", emoji="money_bag"),
    dict(wrong="Much friends", right="Many friends", note="friends شمردنیه؛ many میاد", emoji="people_hugging"),
    dict(wrong="Less people", right="Fewer people", note="برای شمردنی‌ها fewer میاد", emoji="busts_in_silhouette"),
], ("much یا many؟ این ۳ تا رو اشتباه می‌گی ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(60, "vocab", [
    dict(wrong="Very good!", right="Way to go!", note="یعنی «آفرین! همین‌جوری ادامه بده»", emoji="clapping_hands"),
    dict(wrong="I wish you good luck.", right="All the best!", note="یعنی «بهترین‌ها رو برات آرزو دارم»", emoji="glowing_star"),
    dict(wrong="I'm happy for you.", right="Good for you!", note="یعنی «خوشحالم برات»", emoji="smiling_face_with_smiling_eyes"),
    dict(wrong="Happy new year.", right="To a great new year!", note="یعنی «به امید یه سال عالی»", emoji="party_popper"),
], ("برای سال نو این‌جوری تبریک بگو 🎉", SEND), suffix="a")
write_trial(60, "mistakes", [
    dict(wrong="Happy New Year for you", right="Happy New Year to you", note="تبریک با to میاد، نه for", emoji="party_popper"),
    dict(wrong="I wish you happy.", right="I wish you happiness.", note="بعد از wish you اسم میاد", emoji="glowing_star"),
    dict(wrong="The next year", right="Next year", note="«سال بعد» = next year بدون the", emoji="calendar"),
], ("سال نو این ۳ تا رو اشتباه نگو ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(54, "Breathe. You don't have to fix everything today.",
            "نفس بکش؛ لازم نیست امروز همه چیزو درست کنی.",
            [("fix", "درست کردن")], "سیو کن برای روزای شلوغ 📌", topic="peace of mind", sea=True)
write_quote(55, "It's okay to start again.",
            "اشکالی نداره از نو شروع کنی.",
            [("start again", "از نو شروع کردن")], "برای کسی که می‌خواد از نو شروع کنه بفرست 🌱", topic="trying again",
            figure=True)
write_quote(56, "Trust yourself. You've survived a lot.",
            "به خودت اعتماد کن؛ از کلی سختی رد شدی.",
            [("trust", "اعتماد کردن"), ("survived", "جون سالم به در بردی")], "برای کسی که به خودش شک داره بفرست 💪",
            topic="self-belief")
write_quote(57, "Good things come to those who wait.",
            "چیزای خوب به کسایی می‌رسه که صبر می‌کنن.",
            [("those who", "کسایی که")], "سیو کن 📌", topic="patience", trees=True)
write_quote(58, "Work quietly. Let your results speak.",
            "بی‌سروصدا کار کن؛ بذار نتیجه‌ت حرف بزنه.",
            [("quietly", "بی‌سروصدا"), ("results", "نتیجه‌ها")], "برای یه آدم سخت‌کوش بفرست 💪", topic="hard work",
            figure=True)
write_quote(59, "Friends are the family we choose.",
            "دوستا خانواده‌ای هستن که خودمون انتخابشون می‌کنیم.",
            [("choose", "انتخاب کردن")], "برای دوستت بفرست 🤍", topic="friendship", sea=True)
write_quote(60, "New year, new pages. Write a good story.",
            "سال نو، صفحه‌های نو؛ یه داستان خوب بنویس.",
            [("pages", "صفحه‌ها")], "سال نو میلادی مبارک 🎉 برای عزیزانت بفرست", topic="the future", palette="night")
