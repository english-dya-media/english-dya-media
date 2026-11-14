"""Week 6: Sat 5 Dec – Fri 11 Dec 2026 (days 33–39): reels, trial reels and quote reels (batch of 14 Nov)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

TH = GLOW(f"صدای {{EN}}: زبون بین دندون{ZW}ها", "th", "tongue")
FL = GLOW("اینجا {EN} شبیه «د»", "tt")
EDT = GLOW("اینجا {EN} = «ت»", "ed")
OA = GLOW("اینجا {EN} = «آ»ی کوتاه", "o")

write_day(33,
    hook=H("این ۴ تا کلمه رو", "آمریکایی", "بگو", "tt میشه «د»!", "speaker_high_volume",
           "تو آمریکایی، t وسط کلمه نرم میشه", "light_bulb"),
    words=[
        W(FL, "pretty", "tt", "rose", "🌹", "/ˈprɪɾi/", "پریتی", "پْریدی", "قشنگ"),
        W(FL, "letter", "tt", "envelope", "✉️", "/ˈleɾər/", "لِتِر", "لِدِر", "نامه؛ حرف الفبا"),
        W(FL, "bottle", "tt", "baby_bottle", "🍼", "/ˈbɑːɾəl/", "باتِل", "بادِل", "بطری"),
        W(FL, "butter", "tt", "pancakes", "🥞", "/ˈbʌɾər/", "باتِر", "بادِر", "کره"),
    ],
    cap=("آمریکایی‌ها tt این کلمه‌ها رو «د» می‌گن 🇺🇸", "butter میشه «بادِر» و bottle میشه «بادِل» 💡 برای دوستت بفرست"),
    stories=[
        REC(33, 1),
        QZV("lose", "s", "confused_face", "«ز»"),
        MC(33, 3, "چنگال", "چاقو", 1),
        AQ("یه کلمه با tt", "که", "مطمئن نیستی؟", "ریپلای کن تا تلفظ آمریکاییشو\nتو ریلزهای بعدی بگم", "little"),
    ])

write_day(34,
    hook=H("این ۴ تا کلمه رو", "با", "«اوق»", "نخون!", "cross_mark", "ough هر بار یه جور خونده میشه!", "face_with_spiral_eyes"),
    words=[
        W(GLOW("اینجا {EN} = «اف»", "ough"), "cough", "ough", "face_with_medical_mask", "😷", "/kɔːf/", "کوق", "کاف", "سرفه"),
        W(GLOW("اینجا {EN} = «اف»", "ough"), "tough", "ough", "flexed_biceps", "💪", "/tʌf/", "توق", "تاف", "سخت، سرسخت"),
        W(GLOW("اینجا {EN} = «آ»", "ough"), "bought", "ough", "shopping_bags", "🛍️", "/bɔːt/", "بوقت", "بات", "خرید (گذشته)"),
        W(GLOW("اینجا {EN} = «او»", "ough"), "through", "ough", "bridge_at_night", "🌉", "/θruː/", "تروق", "ثْرو", "از میانِ"),
    ],
    cap=("ough رو «اوق» نخون ❌", "cough، tough، bought و through: هر کدوم یه جورن 😵 سیو کن"),
    stories=[
        REC(34, 0),
        QZ("wreath", "w", "christmas_tree"),
        MC(34, 2, "لیوان", "قاشق", 0),
        AQ("یه کلمه با gh", "که", "گیجت می‌کنه؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "enough"),
    ])

write_day(35,
    hook=H("اسم این ۴ تا کشور", "رو", "اشتباه", "می‌گی!", "world_map", "انگلیسی‌ها این‌جوری می‌گن", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «ج»", "j"), "Japan", "j", "sushi", "🍣", "/dʒəˈpæn/", "ژاپُن", "جِپَن", "ژاپن"),
        W(GLOW("اینجا {EN} = «ج»", "g"), "Germany", "g", "pretzel", "🥨", "/ˈdʒɜːrməni/", "گِرمانی", "جِرمِنی", "آلمان"),
        W(GLOW("اینجا {EN} = «آی»", "i"), "China", "i", "panda", "🐼", "/ˈtʃaɪnə/", "چینا", "چاینا", "چین"),
        W(GLOW("اینجا {EN} = «ج»", "g"), "Egypt", "g", "desert", "🏜️", "/ˈiːdʒɪpt/", "اِگیپت", "ایجیپت", "مصر"),
    ],
    cap=("Germany رو «گِرمانی» نخون ❌", "ژاپن میشه «جِپَن» و آلمان میشه «جِرمِنی» 🌍 برای دوستت بفرست"),
    stories=[
        REC(35, 0),
        QZV("elephant", "ph", "elephant", "«ف»"),
        MC(35, 1, "آسون", "شیرین", 0),
        AQ("اسم کدوم کشور رو", "مطمئن", "نیستی؟", "ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی بگم", "Turkey"),
    ])

write_day(36,
    hook=H("این ۴ تا کلمه رو", "با", "«ت» و «س»", "نگو!", "cross_mark", "زبونتو بذار بین دندونات", "tongue"),
    words=[
        W(TH, "thousand", "th", "money_bag", "💰", "/ˈθaʊzənd/", "تاوزِند", "ثاوزِند", "هزار"),
        W(TH, "Thursday", "th", "spiral_calendar", "🗓️", "/ˈθɜːrzdeɪ/", "تِرزدِی", "ثِرزدِی", "پنجشنبه"),
        W(TH, "mouth", "th", "mouth", "👄", "/maʊθ/", "ماوت", "ماوث", "دهان"),
        W(TH, "health", "th", "stethoscope", "🩺", "/helθ/", "هِلت", "هِلث", "سلامتی"),
    ],
    cap=("Thursday رو «تِرزدِی» نگو ❌", "th این‌جا «ث»ه: زبون بین دندون‌ها و فوت 👅 برای دوستت بفرست"),
    stories=[
        REC(36, 1),
        QZ("two", "w", "keycap_2"),
        MC(36, 3, "عراق", "ترکیه", 2),
        AQ("یه کلمه با th که", "تلفظش", "سخته؟", "ریپلای کن تا تو ریلزهای بعدی\nبا هم تمرینش کنیم", "throat"),
    ])

write_day(37,
    hook=H("این ۴ تا کلمه رو", "با", "«او»", "نخون!", "cross_mark", "o این‌جا شبیه «آ»ی کوتاهه، مثل love", "light_bulb"),
    words=[
        W(OA, "honey", "o", "honey_pot", "🍯", "/ˈhʌni/", "هونی", "هانی", "عسل؛ عزیزم"),
        W(OA, "onion", "o", "onion", "🧅", "/ˈʌnjən/", "اونیون", "آنیِن", "پیاز"),
        W(OA, "glove", "o", "gloves", "🧤", "/ɡlʌv/", "گْلُو", "گْلاو", "دستکش"),
        W(OA, "oven", "o", "baguette_bread", "🥖", "/ˈʌvən/", "اووِن", "آوِن", "فِر"),
    ],
    cap=("honey رو «هونی» نخون ❌", "o تو این ۴ تا کلمه شبیه «آ»ی کوتاهه، مثل love 💡 سیو کن"),
    stories=[
        REC(37, 2),
        QZV("noise", "s", "loudspeaker", "«ز»"),
        MC(37, 3, "قدرت", "بیماری", 1),
        AQ("یه کلمه با o که", "گیجت", "می‌کنه؟", "ریپلای کن؛ شاید تو\nریلز بعدی باشه", "Monday"),
    ])

write_day(38,
    hook=H("تو این ۴ تا کلمه", "حرف", "u", "رو نخون!", "zipper-mouth_face", "این u فقط برای ظاهره!", "light_bulb"),
    words=[
        W(SIL("u"), "guess", "u", "thinking_face", "🤔", "/ɡes/", "گوِس", "گِس", "حدس زدن"),
        W(SIL("u"), "guest", "u", "bellhop_bell", "🛎️", "/ɡest/", "گوِست", "گِست", "مهمان"),
        W(SIL("u"), "guard", "u", "guard", "💂", "/ɡɑːrd/", "گوارد", "گارد", "نگهبان"),
        W(SIL("u"), "biscuit", "u", "cookie", "🍪", "/ˈbɪskɪt/", "بیسکوئیت", "بیسکِت", "بیسکویت"),
    ],
    cap=("guest رو «گوِست» نخون ❌", "u تو این ۴ تا کلمه خونده نمیشه 🤐 برای دوستت بفرست"),
    stories=[
        REC(38, 1),
        QZV("trophy", "ph", "trophy", "«ف»"),
        MC(38, 0, "شیر", "شکر", 2),
        AQ("کدوم حرف بی‌صدا", "بیشتر", "گیجت می‌کنه؟", "ریپلای کن؛ هفته‌ی بعد\nیه ریلز براش می‌سازم", "tongue"),
    ])

write_day(39,
    hook=H("ed آخر این فعل‌ها", "رو", "«اِد»", "نخون!", "warning", "بعد از s و sh میشه «ت»", "light_bulb"),
    words=[
        W(EDT, "kissed", "ed", "kiss_mark", "💋", "/kɪst/", "کیسِد", "کیست", "بوسید"),
        W(EDT, "washed", "ed", "soap", "🧼", "/wɑːʃt/", "واشِد", "واشت", "شست"),
        W(EDT, "finished", "ed", "chequered_flag", "🏁", "/ˈfɪnɪʃt/", "فینیشِد", "فینیشت", "تموم کرد"),
        W(EDT, "missed", "ed", "hourglass_done", "⌛", "/mɪst/", "میسِد", "میست", "از دست داد"),
    ],
    cap=("ed این ۴ تا فعل «اِد» نیست ❌", "بعد از s و sh و k، ed میشه «ت» 💡 سیو کن"),
    stories=[
        REC(39, 0),
        QZ("whose", "w", "red_question_mark"),
        MC(39, 1, "صاحبخانه", "همسایه", 0),
        AQ("یه فعل که", "گذشته‌اش", "گیجت می‌کنه؟", "ریپلای کن تا تلفظشو\nتو ریلزهای بعدی بگم", "fixed"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
SEND = "برای دوستت بفرست که اونم یاد بگیره 👇"

write_trial(33, "vocab", [
    dict(wrong="very surprised", right="stunned", note="یعنی «مات و مبهوت»", emoji="astonished_face"),
    dict(wrong="very sure", right="positive", note="یعنی «کاملاً مطمئن»", emoji="check_mark_button"),
    dict(wrong="very calm", right="serene", note="یعنی «آرام و آسوده»", emoji="person_in_lotus_position"),
    dict(wrong="very bright", right="dazzling", note="یعنی «خیره‌کننده»", emoji="sun_with_face"),
], ("به جای very این ۴ تا کلمه رو بگو 😎", SAVE), suffix="a")
write_trial(33, "mistakes", [
    dict(wrong="I'm good in math.", right="I'm good at math.", note="تو چیزی خوب بودن = good at", emoji="abacus"),
    dict(wrong="He's angry to me.", right="He's angry with me.", note="از کسی عصبانی = angry with", emoji="pouting_face"),
    dict(wrong="I'm proud to you.", right="I'm proud of you.", note="به کسی افتخار کردن = proud of", emoji="trophy"),
], ("حرف اضافه‌ی این ۳ تا رو اشتباه می‌گی ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(34, "vocab", [
    dict(wrong="Okay.", right="Sounds good!", note="یعنی «خوبه، موافقم»", emoji="thumbs_up"),
    dict(wrong="Of course.", right="Definitely!", note="یعنی «حتماً، قطعاً»", emoji="check_mark_button"),
    dict(wrong="Me too.", right="Same here.", note="یعنی «منم همین‌طور»", emoji="raising_hands"),
    dict(wrong="Thanks.", right="Cheers!", note="یعنی «مرسی» (خودمونی)", emoji="clinking_glasses"),
], ("این‌جوری جواب بده تا مثل بومی‌ها به نظر بیای 😎", SEND), suffix="a")
write_trial(34, "mistakes", [
    dict(wrong="Why you are sad?", right="Why are you sad?", note="تو سؤال are میاد قبل از you", emoji="crying_face"),
    dict(wrong="How old you are?", right="How old are you?", note="تو سؤال are میاد قبل از you", emoji="birthday_cake"),
    dict(wrong="You are Iranian?", right="Are you Iranian?", note="سؤال با are شروع میشه", emoji="red_question_mark"),
], ("سؤال رو این‌جوری نپرس ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(35, "vocab", [
    dict(wrong="film", right="movie", note="یعنی «فیلم» به آمریکایی", emoji="clapper_board"),
    dict(wrong="autumn", right="fall", note="یعنی «پاییز» به آمریکایی", emoji="fallen_leaf"),
    dict(wrong="football", right="soccer", note="یعنی «فوتبال» به آمریکایی", emoji="soccer_ball"),
    dict(wrong="chips", right="fries", note="یعنی «سیب‌زمینی سرخ‌کرده»", emoji="french_fries"),
], ("این ۴ تا کلمه رو آمریکایی بگو 🇺🇸", SAVE), suffix="a", headline="آمریکایی حرف بزن")
write_trial(35, "mistakes", [
    dict(wrong="He don't know.", right="He doesn't know.", note="با he و she میشه doesn't", emoji="person_shrugging"),
    dict(wrong="She go to work.", right="She goes to work.", note="با he/she فعل s می‌گیره", emoji="briefcase"),
    dict(wrong="It make me happy.", right="It makes me happy.", note="با it هم s لازمه", emoji="smiling_face_with_smiling_eyes"),
], ("این s رو همه جا می‌ندازن ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(36, "vocab", [
    dict(wrong="quit (a habit)", right="give up", note="یعنی «ترک کردن، دست کشیدن»", emoji="no_smoking"),
    dict(wrong="tolerate", right="put up with", note="یعنی «تحمل کردن»", emoji="face_with_rolling_eyes"),
    dict(wrong="recover from", right="get over", note="یعنی «کنار اومدن، خوب شدن»", emoji="adhesive_bandage"),
    dict(wrong="admire", right="look up to", note="یعنی «کسی رو الگو دونستن»", emoji="star"),
], ("بومی‌ها به جای این ۴ تا فعل این‌جوری می‌گن 😎", SAVE), suffix="a", headline="فعل‌هایی که بومی‌ها می‌گن")
write_trial(36, "mistakes", [
    dict(wrong="I'm not agree.", right="I don't agree.", note="agree فعله؛ با don't منفی میشه", emoji="thumbs_down"),
    dict(wrong="I'm believe you.", right="I believe you.", note="believe خودش فعله؛ am نمی‌خواد", emoji="handshake"),
    dict(wrong="I'm need help.", right="I need help.", note="need فعله؛ am لازم نیست", emoji="sos_button"),
], ("این am ها اضافه‌ست ❌", "برای دوستت بفرست 👇"), suffix="b")

write_trial(37, "vocab", [
    dict(wrong="book lover", right="bookworm", note="یعنی «کرم کتاب»", emoji="books"),
    dict(wrong="stays up late", right="night owl", note="یعنی «جغد شب، شب‌زنده‌دار»", emoji="owl"),
    dict(wrong="lazy at home", right="couch potato", note="یعنی «تنبلِ مبل‌نشین»", emoji="couch_and_lamp"),
    dict(wrong="gets up early", right="early bird", note="یعنی «سحرخیز»", emoji="bird"),
], ("تو کدوم یکی هستی؟ 😄 کامنت کن", SEND), suffix="a", headline="به این آدما چی میگن؟", head_emoji="thinking_face")
write_trial(37, "mistakes", [
    dict(wrong="more easy", right="easier", note="صفت‌های کوتاه er می‌گیرن", emoji="check_mark_button"),
    dict(wrong="more cheap", right="cheaper", note="صفت‌های کوتاه er می‌گیرن", emoji="coin"),
    dict(wrong="the most good", right="the best", note="good → better → best", emoji="trophy"),
], ("مقایسه رو این‌جوری نگو ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(38, "vocab", [
    dict(wrong="It's very tasty.", right="It's to die for.", note="یعنی «محشره، خیلی خوشمزه‌ست»", emoji="drooling_face"),
    dict(wrong="Let's eat something.", right="Let's grab a bite.", note="یعنی «بریم یه چیزی بخوریم»", emoji="hamburger"),
    dict(wrong="Good appetite.", right="Enjoy your meal!", note="یعنی «نوش جان»", emoji="fork_and_knife_with_plate"),
    dict(wrong="I'm very hungry.", right="I could eat a horse.", note="یعنی «از گرسنگی دارم می‌میرم»", emoji="horse_face"),
], ("سر سفره این‌جوری حرف بزن 😋", SAVE), suffix="a")
write_trial(38, "mistakes", [
    dict(wrong="one of my friend", right="one of my friends", note="بعد از one of اسم جمع میاد", emoji="people_hugging"),
    dict(wrong="two child", right="two children", note="جمع child میشه children", emoji="children_crossing"),
    dict(wrong="many person", right="many people", note="جمع person میشه people", emoji="busts_in_silhouette"),
], ("جمع این ۳ تا رو اشتباه می‌گی ❌", "تو کدومشو می‌گفتی؟ کامنت کن 👇"), suffix="b")

write_trial(39, "vocab", [
    dict(wrong="very dark", right="pitch-black", note="یعنی «تاریکِ تاریک»", emoji="new_moon"),
    dict(wrong="very loud", right="deafening", note="یعنی «گوش‌خراش»", emoji="loudspeaker"),
    dict(wrong="very slow", right="sluggish", note="یعنی «خیلی کُند»", emoji="snail"),
    dict(wrong="very crowded", right="packed", note="یعنی «پُرِ آدم، شلوغ»", emoji="busts_in_silhouette"),
], ("very رو بذار کنار؛ این ۴ تا رو بگو 😎", SAVE), suffix="a")
write_trial(39, "mistakes", [
    dict(wrong="I fell the exam.", right="I failed the exam.", note="رد شدن تو امتحان = fail", emoji="memo"),
    dict(wrong="I became late.", right="I was late.", note="«دیر کردم» = I was late", emoji="alarm_clock"),
    dict(wrong="I have head pain.", right="I have a headache.", note="«سردرد دارم» = a headache", emoji="face_with_head-bandage"),
], ("این ۳ تا رو از فارسی ترجمه نکن ❌", "برای دوستت بفرست 👇"), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(33, "Dream big, start small, but start today.",
            "بزرگ رؤیاپردازی کن، کوچیک شروع کن، ولی از همین امروز شروع کن.",
            [("dream", "رؤیا داشتن")], "سیو کن 📌", topic="dreams", figure=True)
write_quote(34, "The right people will love you for who you are.",
            "آدمای درست تو رو همون‌جوری که هستی دوست دارن.",
            [("right", "درست، مناسب")], "برای آدمای درستِ زندگیت بفرست 🤍", topic="people")
write_quote(35, "Let go of what you can't change.",
            "چیزی رو که نمی‌تونی عوضش کنی، رها کن.",
            [("let go", "رها کردن")], "سیو کن برای روزای سخت 📌", topic="letting go", sea=True)
write_quote(36, "Success is the sum of small efforts, repeated day after day.",
            "موفقیت جمعِ تلاش‌های کوچیکیه که روز به روز تکرار میشن.",
            [("success", "موفقیت"), ("efforts", "تلاش‌ها")], "برای کسی که داره تلاش می‌کنه بفرست 💪", topic="success")
write_quote(37, "Mistakes are proof that you are trying.",
            "اشتباه‌ها نشون میدن که داری تلاش می‌کنی.",
            [("proof", "نشونه، مدرک")], "سیو کن برای وقتی که از خودت ناامیدی 📌", topic="mistakes", figure=True)
write_quote(38, "Your future is created by what you do today.",
            "آینده‌ت با کاری که امروز می‌کنی ساخته میشه.",
            [("created", "ساخته میشه")], "سیو کن 📌", topic="the future", sea=True)
write_quote(39, "The truth is always the easiest thing to remember.",
            "حقیقت همیشه راحت‌ترین چیزیه که یادت می‌مونه.",
            [("truth", "حقیقت")], "برای یه آدم صادق بفرست 🤍", topic="honesty")
