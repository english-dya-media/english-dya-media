"""Week 10: Sat 2 Jan – Fri 8 Jan 2027 (days 61–67): reels, trial reels and quote reels (batch of 14 Nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

EDD = GLOW("اینجا {EN} = «د»", "ed")
TH = GLOW(f"صدای {{EN}}: زبون بین دندون{ZW}ها", "th", "tongue")
CL = lambda tip_en: GLOW("{EN} بدون «اِ» اولش", tip_en)
E = lambda s: GLOW("اینجا {EN} = «اِ»", s)
ES = GLOW("اینجا {EN} = «ایز»", "es")
AGE = GLOW("{EN} آخرش «ج»ه، نه «ژ»", "age")

write_day(61,
    hook=H("این ۴ تا فعل رو", "با", "«اِد»", "نخون!", "cross_mark", "loved میشه «لاوْد»، نه «لاوِد»", "light_bulb"),
    words=[
        W(EDD, "loved", "ed", "red_heart", "❤️", "/lʌvd/", "لاوِد", "لاوْد", "دوست داشت"),
        W(EDD, "rained", "ed", "cloud_with_rain", "🌧️", "/reɪnd/", "رِینِد", "رِیند", "بارون اومد"),
        W(EDD, "hugged", "ed", "people_hugging", "🫂", "/hʌɡd/", "هاگِد", "هاگْد", "بغل کرد"),
        W(EDD, "closed", "ed", "locked", "🔒", "/kloʊzd/", "کلوزِد", "کْلُوزد", "بست؛ بسته"),
    ],
    cap=("hugged رو «هاگِد» نخون ❌", "ed این ۴ تا فعل فقط یه «د»ه، بدون «اِ» 💡 سیو کن"),
    stories=[
        REC(61, 2),
        QZ("crumb", "b", "cookie"),
        MC(61, 1, "فوریه", "فِبْروئِری", 2, pron=True),
        AQ("کدوم فعل گذشته", "رو", "شک داری؟", "ریپلای کن؛ تو ریلزهای بعدی\nتلفظشو می‌گم", "changed"),
    ])

write_day(62,
    hook=H("این ۴ تا کلمه", "یه", "«اِ»", "دارن!", "light_bulb", "said میشه «سِد»، نه «سِید»", "speaker_high_volume"),
    words=[
        W(E("ai"), "said", "ai", "speech_balloon", "💬", "/sed/", "سِید", "سِد", "گفت"),
        W(E("ay"), "says", "ay", "speaking_head", "🗣️", "/sez/", "سِیز", "سِز", "می‌گه"),
        W(E("a"), "any", "a", "red_question_mark", "❓", "/ˈeni/", "آنی", "اِنی", "هیچ؛ هر"),
        W(E("a"), "many", "a", "hundred_points", "💯", "/ˈmeni/", "مَنی", "مِنی", "زیاد، خیلی"),
    ],
    cap=("said رو «سِید» و many رو «مَنی» نخون ❌", "این ۴ تا کلمه یه «اِ»ی کوتاه دارن 💡 برای دوستت بفرست"),
    stories=[
        REC(62, 0),
        QZV("nose", "s", "nose", "«ز»"),
        MC(62, 3, "باز کرد", "پوشید", 0),
        AQ("یه کلمه که", "تلفظش", "عجیبه؟", "ریپلای کن تا تو ریلزهای بعدی\nبا هم درستش کنیم", "friend"),
    ])

write_day(63,
    hook=H("این ۴ تا برند", "رو", "درست", "بگو!", "speaker_high_volume", "Nestle «نستله» نیست!", "astonished_face"),
    words=[
        W(SIL("l"), "Volkswagen", "l", "minibus", "🚐", "/ˈvoʊkswæɡən/", "فولکس واگن", "وُکس‌وَگِن", "برند ماشین",
          ph="vˈoʊkswˌæɡən"),
        W(SIL("t"), "Nestle", "t", "chocolate_bar", "🍫", "/ˈnesleɪ/", "نستله", "نِسلِی", "برند خوراکی", ph="nˈɛsleɪ"),
        W(SIL("t"), "Chevrolet", "t", "pickup_truck", "🛻", "/ˌʃevrəˈleɪ/", "شورولت", "شِوْرُلِی", "برند ماشین"),
        W(GLOW("اینجا {EN} = «ی»", "e"), "Adobe", "e", "artist_palette", "🎨", "/əˈdoʊbi/", "اَدوب", "اِدُوبی", "برند نرم‌افزار"),
    ],
    cap=("Nestle رو «نستله» نگو ❌", "اسم این ۴ تا برند رو این‌جوری بگو 🔊 برای دوستت بفرست"),
    stories=[
        REC(63, 1, pron=True),
        QZ("sword", "w", "crossed_swords"),
        MC(63, 3, "خیلی کم", "هیچ‌وقت", 1),
        AQ("اسم کدوم برند رو", "مطمئن", "نیستی؟", "ریپلای کن؛ تلفظ درستشو\nتو ریلزهای بعدی می‌گم", "Siemens"),
    ])

write_day(64,
    hook=H("این ۴ تا کلمه رو", "با", "«ت»", "نگو!", "cross_mark", "th این‌جا «ث»ه، با زبون بین دندون‌ها", "tongue"),
    words=[
        W(TH, "bathroom", "th", "bathtub", "🛁", "/ˈbæθruːm/", "باتروم", "بَثروم", "حموم؛ دستشویی"),
        W(TH, "math", "th", "abacus", "🧮", "/mæθ/", "مَت", "مَث", "ریاضی"),
        W(TH, "author", "th", "writing_hand", "✍️", "/ˈɔːθər/", "آتور", "آثِر", "نویسنده"),
        W(TH, "athlete", "th", "sports_medal", "🏅", "/ˈæθliːt/", "اَتلت", "اَثلیت", "ورزشکار"),
    ],
    cap=("math رو «مَت» نگو ❌", "th این‌جا «ث»ه: زبون بین دندون‌ها و فوت 👅 سیو کن"),
    stories=[
        REC(64, 0, pron=True),
        QZV("phrase", "ph", "speech_balloon", "«ف»"),
        MC(64, 1, "نستله", "نِستِل", 2, pron=True),
        AQ("درس مورد علاقه‌ت", "به", "انگلیسی؟", "ریپلای کن؛ تلفظشو\nبرات می‌فرستم", "chemistry"),
    ])

write_day(65,
    hook=H("es آخر این کلمه‌ها", "یه", "«ایز»", "کامله!", "speaker_high_volume", "houses میشه «هاوزیز»", "light_bulb"),
    words=[
        W(ES, "houses", "es", "houses", "🏘️", "/ˈhaʊzɪz/", "هاوسِس", "هاوزیز", "خونه‌ها"),
        W(ES, "horses", "es", "horse", "🐎", "/ˈhɔːrsɪz/", "هورسز", "هُرسیز", "اسب‌ها"),
        W(ES, "prizes", "es", "trophy", "🏆", "/ˈpraɪzɪz/", "پرایزز", "پرایزیز", "جایزه‌ها"),
        W(ES, "pages", "es", "page_facing_up", "📄", "/ˈpeɪdʒɪz/", "پِیجز", "پِیجیز", "صفحه‌ها"),
    ],
    cap=("houses رو «هاوسِس» نخون ❌", "بعد از صدای «س»، «ز» و «ج» جمع میشه «ایز» 💡 برای دوستت بفرست"),
    stories=[
        REC(65, 3),
        QZ("aisle", "s", "airplane"),
        MC(65, 2, "خواننده", "معلم", 0),
        AQ("یه کلمه‌ی جمع", "که", "سخته؟", "ریپلای کن تا تو ریلزهای بعدی\nتلفظشو بگم", "watches"),
    ])

write_day(66,
    hook=H("این ۴ تا کلمه رو", "با", "«اِ»", "شروع نکن!", "cross_mark", "st، squ، sl و sc بدون «اِ»", "speaker_high_volume"),
    words=[
        W(CL("st"), "station", "st", "station", "🚉", "/ˈsteɪʃən/", "اِستیشن", "سْتِیشِن", "ایستگاه"),
        W(CL("squ"), "square", "squ", "red_square", "🟥", "/skwer/", "اِسکوئر", "سْکوِر", "مربع؛ میدان"),
        W(CL("sl"), "slow", "sl", "snail", "🐌", "/sloʊ/", "اِسلو", "سْلُو", "آهسته"),
        W(CL("sc"), "scarf", "sc", "scarf", "🧣", "/skɑːrf/", "اِسکارف", "سْکارف", "شال گردن"),
    ],
    cap=("station رو «اِستیشن» نگو ❌", "مستقیم با s شروع کن: «سْتِیشِن» 💡 سیو کن"),
    stories=[
        REC(66, 1, pron=True),
        QZV("giant", "g", "t-rex", "«ج»"),
        MC(66, 3, "کتاب‌ها", "قدم‌ها", 1),
        AQ("سخت‌ترین کلمه", "برای", "تو؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "strength"),
    ])

write_day(67,
    hook=H("این ۴ تا کلمه رو", "با", "«اژ»", "نخون!", "cross_mark", "age آخرشون میشه «ایج»", "light_bulb"),
    words=[
        W(AGE, "village", "age", "house_with_garden", "🏡", "/ˈvɪlɪdʒ/", "ویلاژ", "ویلِج", "روستا"),
        W(AGE, "image", "age", "framed_picture", "🖼️", "/ˈɪmɪdʒ/", "ایماژ", "ایمِج", "تصویر"),
        W(AGE, "passage", "age", "open_book", "📖", "/ˈpæsɪdʒ/", "پاساژ", "پَسِج", "متن؛ گذرگاه"),
        W(AGE, "voyage", "age", "passenger_ship", "🛳️", "/ˈvɔɪɪdʒ/", "وویاژ", "وُیِج", "سفر دریایی"),
    ],
    cap=("passage «پاساژ» نیست ❌", "age آخر این ۴ تا کلمه «ج»ه، نه «ژ» 💡 برای دوستت بفرست"),
    stories=[
        REC(67, 3),
        QZ("knuckle", "k", "oncoming_fist"),
        MC(67, 0, "اتوبوس", "فرودگاه", 2),
        AQ("یه کلمه‌ی فرانسوی", "که", "انگلیسیش؟", "ریپلای کن؛ تلفظ انگلیسیشو\nبرات می‌گم", "massage"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
SEND = "برای دوستت بفرست که اونم یاد بگیره 👇"
CMT = "تو کدومشو می‌گفتی؟ کامنت کن 👇"

write_trial(61, "vocab", [
    dict(wrong="discover", right="find out", note="یعنی «فهمیدن، پی بردن»", emoji="magnifying_glass_tilted_left"),
    dict(wrong="understand (a problem)", right="figure out", note="یعنی «سر درآوردن، حل کردن»", emoji="thinking_face"),
    dict(wrong="have no more", right="run out of", note="یعنی «تموم کردن (چیزی)»", emoji="low_battery"),
    dict(wrong="refuse", right="turn down", note="یعنی «رد کردن (پیشنهاد)»", emoji="person_gesturing_no"),
], ("بومی‌ها به جای این ۴ تا فعل این‌جوری می‌گن 😎", SAVE), suffix="a", headline="فعل‌هایی که بومی‌ها می‌گن")
write_trial(61, "mistakes", [
    dict(wrong="I want that you come.", right="I want you to come.", note="want + کسی + to + فعل", emoji="raising_hands"),
    dict(wrong="I told him that come.", right="I told him to come.", note="tell + کسی + to + فعل", emoji="speaking_head"),
    dict(wrong="I hope you to win.", right="I hope you win.", note="بعد از hope جمله‌ی کامل میاد", emoji="crossed_fingers"),
], ("ساختار فارسی رو انگلیسی نکن ❌", CMT), suffix="b")

write_trial(62, "vocab", [
    dict(wrong="That's reasonable.", right="Fair enough.", note="یعنی «منطقیه، قبول»", emoji="ok_hand"),
    dict(wrong="I'll come too!", right="Count me in!", note="یعنی «منم هستم!»", emoji="raising_hands"),
    dict(wrong="It's not important.", right="No big deal.", note="یعنی «مهم نیست، چیزی نیست»", emoji="relieved_face"),
    dict(wrong="Of course!", right="You bet!", note="یعنی «معلومه! حتماً»", emoji="thumbs_up"),
], ("جواب‌هایی که بومی‌ها هر روز می‌دن 😎", SAVE), suffix="a", headline="مثل بومی‌ها جواب بده")
write_trial(62, "mistakes", [
    dict(wrong="The news are good.", right="The news is good.", note="news مفرده؛ is می‌گیره", emoji="newspaper"),
    dict(wrong="Her hairs are long.", right="Her hair is long.", note="موی سر شمردنی نیست", emoji="woman_red_hair"),
    dict(wrong="I did some researches.", right="I did some research.", note="research جمع بسته نمیشه", emoji="microscope"),
], ("این کلمه‌ها جمع نمی‌بندن ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(63, "vocab", [
    dict(wrong="It's raining a little.", right="It's drizzling.", note="یعنی «نم‌نم بارون میاد»", emoji="cloud_with_rain"),
    dict(wrong="It's a little cold.", right="It's chilly.", note="یعنی «هوا یه کم سرده»", emoji="cold_face"),
    dict(wrong="It's hot and humid.", right="It's muggy.", note="یعنی «هوا شرجی و دمه»", emoji="hot_face"),
    dict(wrong="It's very cloudy.", right="It's overcast.", note="یعنی «آسمون کاملاً ابریه»", emoji="cloud"),
], ("هوا رو مثل بومی‌ها توصیف کن ☁️", SAVE), suffix="a", headline="هوا رو حرفه‌ای توصیف کن")
write_trial(63, "mistakes", [
    dict(wrong="You are coming?", right="Are you coming?", note="تو سؤال فعل میاد اول", emoji="person_raising_hand"),
    dict(wrong="What you want?", right="What do you want?", note="سؤال با do ساخته میشه", emoji="thinking_face"),
    dict(wrong="Why you didn't come?", right="Why didn't you come?", note="didn't قبل از فاعل میاد", emoji="face_with_raised_eyebrow"),
], ("سؤال رو این‌جوری نپرس ❌", CMT), suffix="b")

write_trial(64, "vocab", [
    dict(wrong="walk slowly", right="stroll", note="یعنی «قدم زدن آروم و تفریحی»", emoji="person_walking"),
    dict(wrong="walk very quietly", right="tiptoe", note="یعنی «پاورچین رفتن»", emoji="footprints"),
    dict(wrong="run very fast", right="sprint", note="یعنی «با تمام سرعت دویدن»", emoji="person_running"),
    dict(wrong="walk with no plan", right="wander", note="یعنی «بی‌هدف گشتن»", emoji="world_map"),
], ("به جای walk این ۴ تا رو بگو 😎", SAVE), suffix="a")
write_trial(64, "mistakes", [
    dict(wrong="It's more better.", right="It's much better.", note="better خودش تفضیلیه؛ more نمی‌خواد", emoji="thumbs_up"),
    dict(wrong="It's the most big.", right="It's the biggest one.", note="صفت کوتاه: est می‌گیره", emoji="elephant"),
    dict(wrong="He's as tall than me.", right="He's as tall as me.", note="as ... as، نه as ... than", emoji="straight_ruler"),
], ("مقایسه رو این‌جوری نگو ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(65, "vocab", [
    dict(wrong="talk to you later", right="ttyl", note="یعنی «بعداً حرف می‌زنیم»", emoji="waving_hand"),
    dict(wrong="in my opinion", right="imo", note="یعنی «به نظر من»", emoji="speech_balloon"),
    dict(wrong="just kidding", right="jk", note="یعنی «شوخی کردم»", emoji="winking_face_with_tongue"),
    dict(wrong="never mind", right="nvm", note="یعنی «بی‌خیال، مهم نیست»", emoji="face_exhaling"),
], ("مخفف‌هایی که تو چت انگلیسی می‌بینی 📱", SAVE), suffix="a", headline="مخفف‌های چت", head_emoji="mobile_phone")
write_trial(65, "mistakes", [
    dict(wrong="My big brother", right="My older brother", note="برای سن older، نه big", emoji="boy"),
    dict(wrong="My small sister", right="My little sister", note="«خواهر کوچیکم» = little sister", emoji="girl"),
    dict(wrong="My mother's sister", right="My aunt", note="خاله و عمه هر دو aunt هستن", emoji="woman"),
], ("خانواده‌تو این‌جوری معرفی نکن ❌", CMT), suffix="b")

write_trial(66, "vocab", [
    dict(wrong="I'm very excited!", right="I'm stoked!", note="یعنی «خیلی هیجان‌زده‌ام!»", emoji="star-struck"),
    dict(wrong="I'm disappointed.", right="I'm bummed.", note="یعنی «پَکَرم، ناامید شدم»", emoji="disappointed_face"),
    dict(wrong="I miss my home.", right="I'm homesick.", note="یعنی «دلم برای خونه تنگ شده»", emoji="house"),
    dict(wrong="I'm very nervous.", right="I'm on edge.", note="یعنی «مضطربم، دلشوره دارم»", emoji="anxious_face_with_sweat"),
], ("حال‌تو مثل بومی‌ها بگو 😎", SAVE), suffix="a")
write_trial(66, "mistakes", [
    dict(wrong="Today morning", right="This morning", note="«امروز صبح» = this morning", emoji="sunrise"),
    dict(wrong="After tomorrow", right="The day after tomorrow", note="«پس‌فردا» این‌جوری گفته میشه", emoji="spiral_calendar"),
    dict(wrong="At the morning", right="In the morning", note="صبح و عصر با in میان", emoji="sun_behind_cloud"),
], ("زمان رو این‌جوری نگو ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(67, "vocab", [
    dict(wrong="I don't like it.", right="Not my cup of tea.", note="یعنی «سلیقه‌ی من نیست»", emoji="teacup_without_handle"),
    dict(wrong="very calm", right="cool as a cucumber", note="یعنی «خیلی خونسرد»", emoji="cucumber"),
    dict(wrong="briefly", right="in a nutshell", note="یعنی «خلاصه‌ش اینه که»", emoji="peanuts"),
    dict(wrong="go crazy", right="go bananas", note="یعنی «دیوونه شدن، قاطی کردن»", emoji="banana"),
], ("اصطلاح‌های خوراکی که بومی‌ها می‌گن 😋", SAVE), suffix="a", headline="اصطلاح‌هایی که بومی‌ها می‌گن",
   head_emoji="speech_balloon")
write_trial(67, "mistakes", [
    dict(wrong="I arrived to Tehran.", right="I arrived in Tehran.", note="برای شهر: arrive in", emoji="airplane_arrival"),
    dict(wrong="I'm worried for you.", right="I'm worried about you.", note="نگران کسی = worried about", emoji="worried_face"),
    dict(wrong="It's similar with mine", right="It's similar to mine.", note="similar to، نه with", emoji="left-right_arrow"),
], ("حرف اضافه‌ی این ۳ تا رو اشتباه می‌ذاری ❌", CMT), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(61, "Love is not what you say. Love is what you do.",
            "عشق چیزی نیست که می‌گی؛ کاریه که انجام می‌دی.",
            [("what you do", "کاری که می‌کنی")], "برای کسی که دوستش داری بفرست 🤍", topic="love", figure=True)
write_quote(62, "Take a break. The world can wait a little.",
            "یه کم استراحت کن؛ دنیا می‌تونه یه کم صبر کنه.",
            [("take a break", "استراحت کن")], "سیو کن برای روزای خسته‌کننده 📌", topic="rest", sea=True)
write_quote(63, "Say thank you more often. It changes more than you think.",
            "بیشتر تشکر کن؛ بیشتر از اونی که فکر می‌کنی چیزا رو عوض می‌کنه.",
            [("more often", "بیشتر، زیادتر")], "برای کسی که ازش ممنونی بفرست 🙏", topic="gratitude")
write_quote(64, "Do it scared. That's what courage is.",
            "با ترس هم انجامش بده؛ شجاعت یعنی همین.",
            [("scared", "ترسیده"), ("courage", "شجاعت")], "برای کسی که می‌ترسه شروع کنه بفرست 💪", topic="courage",
            figure=True)
write_quote(65, "Your dreams don't have an expiration date.",
            "رویاهات تاریخ انقضا ندارن.",
            [("expiration date", "تاریخ انقضا")], "سیو کن 📌", topic="dreams")
write_quote(66, "Stay close to people who feel like sunshine.",
            "کنار آدمایی بمون که حضورشون مثل آفتابه.",
            [("stay close", "نزدیک موندن")], "برای آفتاب زندگیت بفرست ☀️", topic="people", sea=True)
write_quote(67, "Some things are better left behind.",
            "بعضی چیزا رو بهتره پشت سر بذاری.",
            [("left behind", "پشت سر گذاشته")], "سیو کن 📌", topic="letting go", trees=True)
