"""Week 16: Sat 13 Feb – Fri 19 Feb 2027 (days 103–109): reels, trial reels and quote reels (batch of 14 Nov).
Day 104 (14 Feb) is Valentine's Day; day 108 (18 Feb, 29 Bahman) is Sepandarmazgan."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

FL = lambda s: GLOW("اینجا {EN} شبیه «د»", s)
OO = GLOW("اینجا {EN} = «اُ»ی کوتاه", "oo")
OR = lambda s: GLOW("اینجا {EN} = «اُر»", s)

write_day(103,
    hook=H("این ۴ تا کلمه رو", "با", "«او»ی کشیده", "نخون!", "cross_mark", "oo این‌جا یه «اُ»ی کوتاهه", "light_bulb"),
    words=[
        W(OO, "book", "oo", "closed_book", "📕", "/bʊk/", "بوک", "بُک", "کتاب"),
        W(OO, "foot", "oo", "footprints", "👣", "/fʊt/", "فوت", "فُت", "پا (کف پا)"),
        W(OO, "wood", "oo", "wood", "🪵", "/wʊd/", "وود", "وُد", "چوب"),
        W(OO, "wool", "oo", "ewe", "🐑", "/wʊl/", "وول", "وُل", "پشم"),
    ],
    cap=("book رو «بوک» نخون ❌", "oo تو این ۴ تا کلمه یه «اُ»ی کوتاهه، نه «او»ی کشیده 💡 سیو کن"),
    stories=[
        REC(103, 3, pron=True),
        QZ("knapsack", "k", "backpack"),
        MC(103, 2, "انگور", "خرما", 1),
        AQ("یه کلمه با oo", "که", "مطمئن نیستی؟", "ریپلای کن؛ کوتاهه یا کشیده؟\nبرات می‌گم", "good"),
    ])

write_day(104,
    hook=H("ولنتاین مبارک!", "این ۴ تا رو", "درست", "بگو!", "red_heart", "Valentine میشه «وَلِنتاین»", "heart_with_ribbon"),
    words=[
        W(GLOW("اینجا {EN} = «اَ»", "a"), "Valentine", "a", "heart_with_ribbon", "💝", "/ˈvæləntaɪn/", "والنتاین", "وَلِنتاین",
          "ولنتاین"),
        W(GLOW("اینجا {EN} = «اُو»", "o"), "romantic", "o", "love_letter", "💌", "/roʊˈmæntɪk/", "رمانتیک", "رُومَنتیک", "عاشقانه"),
        W(GLOW("اینجا {EN} = «آیِ»", "ia"), "diamond", "ia", "ring", "💍", "/ˈdaɪəmənd/", "دیاموند", "دایِمِند", "الماس"),
        W(GLOW("اینجا {EN} = «اُو»", "o"), "rose", "o", "rose", "🌹", "/roʊz/", "رُز", "رُوز", "گل رز"),
    ],
    cap=("ولنتاین مبارک ❤️ این ۴ تا کلمه رو درست بگو", "برای کسی که دوستش داری بفرست 🌹"),
    stories=[
        REC(104, 0),
        QZV("present", "s", "wrapped_gift", "«ز»"),
        MC(104, 3, "پنبه", "ابریشم", 2),
        AQ("به عشقت", "به انگلیسی", "چی می‌گی؟", "ریپلای کن؛ یه جمله‌ی عاشقانه‌ی\nانگلیسی یادت می‌دم", "I love you"),
    ])

write_day(105,
    hook=H("اسم این ۴ تا شهر", "رو", "اشتباه", "می‌گی!", "airplane", "Toronto «تورنتو» نیست!", "astonished_face"),
    words=[
        W(GLOW("اینجا {EN} = «اِ»", "o"), "Toronto", "o", "maple_leaf", "🍁", "/təˈrɑːntoʊ/", "تورنتو", "تِرانتُو", "تورنتو",
          ph="təɹˈɑːntoʊ"),
        W(GLOW("اینجا {EN} = «ری‌آل»", "real"), "Montreal", "real", "ice_hockey", "🏒", "/ˌmɑːntriˈɔːl/", "مونترال", "مانتْری‌آل",
          "مونترال"),
        W(GLOW("اینجا {EN} = «بِرن»", "bourne"), "Melbourne", "bourne", "kangaroo", "🦘", "/ˈmelbərn/", "ملبورن", "مِلبِرن", "ملبورن"),
        W(FL("tt"), "Seattle", "tt", "umbrella_with_rain_drops", "☔", "/siˈæɾəl/", "سیاتل", "سی‌یَدِل", "سیاتل"),
    ],
    cap=("تورنتو و ملبورن به انگلیسی چی میشن؟ ✈️", "اسم این ۴ تا شهر رو این‌جوری بگو 🌍 برای دوستت بفرست"),
    stories=[
        REC(105, 1, pron=True),
        QZ("handkerchief", "d", "sneezing_face"),
        MC(105, 2, "طلا", "مروارید", 0),
        AQ("دوست داری", "کجا", "زندگی کنی؟", "ریپلای کن؛ تلفظ انگلیسیشو\nبرات می‌گم", "Vancouver"),
    ])

write_day(106,
    hook=H("اسم این ۴ تا جا", "رو", "درست", "بگو!", "office_building", "restaurant «رستوران» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «آی»", "i"), "library", "i", "books", "📚", "/ˈlaɪbreri/", "لیبراری", "لایبرِری", "کتابخانه"),
        W(GLOW("اینجا {EN} = «رانت»", "rant"), "restaurant", "rant", "fork_and_knife_with_plate", "🍽️", "/ˈrestərɑːnt/", "رستوران",
          "رِستِرانت", "رستوران"),
        W(FL("t"), "hospital", "t", "hospital", "🏥", "/ˈhɑːspɪɾəl/", "هاسپیتال", "هاسپیدِل", "بیمارستان"),
        W(GLOW("اینجا {EN} = «اِی»", "a"), "bakery", "a", "baguette_bread", "🥖", "/ˈbeɪkəri/", "باکِری", "بِیکِری", "نونوایی"),
    ],
    cap=("restaurant رو «رستوران» نگو ❌", "اسم این ۴ تا جا رو این‌جوری بگو 🏙️ برای دوستت بفرست"),
    stories=[
        REC(106, 3, pron=True),
        QZV("casual", "s", "t-shirt", "«ژ»"),
        MC(106, 1, "مونترال", "مونتریال", 2, pron=True),
        AQ("کجای شهر", "بیشتر", "می‌ری؟", "ریپلای کن؛ اسم انگلیسیشو\nبرات می‌گم", "gym"),
    ])

write_day(107,
    hook=H("این ۴ تا کلمه رو", "با", "«او»", "نخون!", "cross_mark", "oor و our این‌جا «اُر»ه", "light_bulb"),
    words=[
        W(OR("oor"), "door", "oor", "door", "🚪", "/dɔːr/", "دور", "دُر", "در"),
        W(OR("oor"), "floor", "oor", "broom", "🧹", "/flɔːr/", "فلور", "فْلُر", "کف؛ طبقه"),
        W(OR("our"), "four", "our", "keycap_4", "4️⃣", "/fɔːr/", "فور", "فُر", "چهار"),
        W(OR("our"), "pour", "our", "teapot", "🫖", "/pɔːr/", "پور", "پُر", "ریختن (مایع)"),
    ],
    cap=("door رو «دور» نخون ❌", "oor و our تو این ۴ تا کلمه «اُر»ه 💡 برای دوستت بفرست"),
    stories=[
        REC(107, 0),
        QZ("climber", "b", "person_climbing"),
        MC(107, 3, "قصابی", "کافه", 2),
        AQ("یه کلمه با or", "که", "مطمئن نیستی؟", "ریپلای کن؛ «اُر»ه یا «اور»؟\nبرات می‌گم", "course"),
    ])

write_day(108,
    hook=H("این ۴ تا دسر رو", "انگلیسی", "بگو", "مثل بومی‌ها!", "custard", "caramel «کارامل» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «اَ»", "a"), "caramel", "a", "candy", "🍬", "/ˈkærəmel/", "کارامل", "کَرِمِل", "کارامل"),
        W(GLOW("اینجا {EN} = «اِ»", "a"), "vanilla", "a", "soft_ice_cream", "🍦", "/vəˈnɪlə/", "وانیل", "وِنیلا", "وانیل"),
        W(GLOW("اینجا {EN} = «اُ»", "u"), "pudding", "u", "custard", "🍮", "/ˈpʊdɪŋ/", "پودینگ", "پُدینگ", "پودینگ"),
        W(GLOW("اینجا {EN} = «مِلُو»", "mallow"), "marshmallow", "mallow", "cloud", "☁️", "/ˈmɑːrʃmeloʊ/", "مارشمالو", "مارشمِلُو",
          "مارشمالو"),
    ],
    cap=("caramel رو «کارامل» نگو ❌", "اسم این ۴ تا دسر رو انگلیسی بگو 🍮 برای رفیق شکموت بفرست"),
    stories=[
        REC(108, 2, pron=True),
        QZV("closet", "s", "door", "«ز»"),
        MC(108, 3, "جارو کردن", "شستن", 0),
        AQ("دسر مورد علاقه‌ت", "به", "انگلیسی؟", "ریپلای کن؛ تلفظشو\nبرات می‌فرستم", "cheesecake"),
    ])

write_day(109,
    hook=H("اسم این ۴ تا برند", "رو", "انگلیسی", "بگو!", "speaking_head", "Tissot «تیسوت» نیست!", "speaker_high_volume"),
    words=[
        W(GLOW("اینجا {EN} = «ک»", "c"), "Lacoste", "c", "crocodile", "🐊", "/ləˈkɔːst/", "لاگوست", "لِکُست", "برند پوشاک",
          ph="ləkˈɔːst"),
        W(GLOW("اینجا {EN} = «سِی»", "ce"), "Mercedes", "ce", "automobile", "🚗", "/mərˈseɪdiːz/", "مرسدس", "مِرسِیدیز", "برند ماشین",
          ph="mɚsˈeɪdiːz"),
        W(GLOW("اینجا {EN} = «ج»", "J"), "Jaguar", "J", "leopard", "🐆", "/ˈdʒæɡwɑːr/", "ژاگوار", "جَگوار", "برند ماشین؛ جگوار"),
        W(SIL("t"), "Tissot", "t", "watch", "⌚", "/ˈtiːsoʊ/", "تیسوت", "تیسُو", "برند ساعت", nth=1, ph="tˈiːsoʊ"),
    ],
    cap=("Lacoste و Tissot رو اشتباه نگو ❌", "اسم این ۴ تا برند رو این‌جوری بگو 🔊 برای دوستت بفرست"),
    stories=[
        REC(109, 3, pron=True),
        QZ("align", "g", "straight_ruler"),
        MC(109, 1, "شکلات", "دارچین", 1),
        AQ("کدوم ریلز", "بیشتر", "کمکت کرد؟", "ریپلای کن تا از اون مدل\nبیشتر بسازم", "th"),
    ])

# ---------------------------------------------------------------- trial reels
SAVE = "سیو کن که یادت بمونه 📌"
CMT = "تو کدومشو می‌گفتی؟ کامنت کن 👇"
LOVE = "برای عشقت بفرست 💌"

write_trial(103, "vocab", [
    dict(wrong="rich", right="well-off", note="یعنی «وضعش خوبه، پولداره»", emoji="money_bag"),
    dict(wrong="spend less", right="cut back", note="یعنی «خرجو کم کردن»", emoji="chart_decreasing"),
    dict(wrong="save money for", right="save up for", note="یعنی «پس‌انداز کردن برای»", emoji="coin"),
    dict(wrong="have just enough money", right="make ends meet", note="یعنی «دخل و خرج رو جور کردن»", emoji="balance_scale"),
], ("پول و خرج به انگلیسی 💰", SAVE), suffix="a", headline="انگلیسی پول و خرج", head_emoji="money_bag")
write_trial(103, "mistakes", [
    dict(wrong="How much is the price?", right="What's the price?", note="price خودش یعنی قیمت", emoji="label"),
    dict(wrong="Give me discount.", right="Can I get a discount?", note="تخفیف رو مؤدبانه بخواه", emoji="shopping_bags"),
    dict(wrong="I have money enough.", right="I have enough money.", note="enough قبل از اسم میاد", emoji="money_bag"),
], ("موقع خرید این‌جوری نگو ❌", CMT), suffix="b")

write_trial(104, "vocab", [
    dict(wrong="like someone secretly", right="have a crush on", note="یعنی «یواشکی کسی رو دوست داشتن»", emoji="smiling_face_with_heart-eyes"),
    dict(wrong="invite on a date", right="ask someone out", note="یعنی «کسی رو به قرار دعوت کردن»", emoji="love_letter"),
    dict(wrong="in love very much", right="head over heels", note="یعنی «دیوونه‌وار عاشق»", emoji="two_hearts"),
    dict(wrong="get married", right="tie the knot", note="یعنی «ازدواج کردن»", emoji="ring"),
], ("ولنتاین مبارک ❤️ عشق به انگلیسی", LOVE), suffix="a", headline="اصطلاح‌های عاشقانه", head_emoji="red_heart")
write_trial(104, "mistakes", [
    dict(wrong="Marry with me?", right="Will you marry me?", note="بعد از marry حرف with نمیاد", emoji="ring"),
    dict(wrong="I'm in love to you.", right="I'm in love with you.", note="عاشق کسی = in love with", emoji="red_heart"),
    dict(wrong="I dated with him.", right="I dated him.", note="بعد از date حرف with نمیاد", emoji="two_hearts"),
], ("ولنتاین این‌جوری نگو ❌", LOVE), suffix="b")

write_trial(105, "vocab", [
    dict(wrong="very hot days", right="a heat wave", note="یعنی «موج گرما»", emoji="hot_face"),
    dict(wrong="sudden cold days", right="a cold snap", note="یعنی «سرمای ناگهانی»", emoji="cold_face"),
    dict(wrong="a little windy", right="It's breezy.", note="یعنی «نسیم میاد»", emoji="wind_face"),
    dict(wrong="very hot and humid", right="It's sweltering.", note="یعنی «گرمای خفه‌کننده»", emoji="sun"),
], ("هوا رو حرفه‌ای توصیف کن 🌤️", SAVE), suffix="a", headline="هوا رو حرفه‌ای توصیف کن")
write_trial(105, "mistakes", [
    dict(wrong="The air is very hot.", right="It's very hot today.", note="برای هوا از It's استفاده کن", emoji="thermometer"),
    dict(wrong="The weather is rain.", right="It's rainy.", note="«بارونیه» = it's rainy", emoji="cloud_with_rain"),
    dict(wrong="What a nice weather!", right="What nice weather!", note="weather شمردنی نیست؛ a نمی‌گیره", emoji="sun_behind_cloud"),
], ("درباره‌ی هوا این‌جوری نگو ❌", CMT), suffix="b")

write_trial(106, "vocab", [
    dict(wrong="enter the hotel", right="check in", note="یعنی «پذیرش و تحویل گرفتن اتاق»", emoji="bellhop_bell"),
    dict(wrong="leave the hotel", right="check out", note="یعنی «تحویل دادن اتاق و رفتن»", emoji="luggage"),
    dict(wrong="room for one person", right="single room", note="یعنی «اتاق یک‌نفره»", emoji="bed"),
    dict(wrong="phone call to wake up", right="wake-up call", note="یعنی «زنگ بیدارباش هتل»", emoji="alarm_clock"),
], ("انگلیسی هتل 🏨", SAVE), suffix="a", headline="انگلیسی هتل و سفر", head_emoji="hotel")
write_trial(106, "mistakes", [
    dict(wrong="I have a reserve.", right="I have a reservation.", note="رزرو (اسم) = reservation", emoji="spiral_calendar"),
    dict(wrong="I go to trip.", right="I'm going on a trip.", note="سفر رفتن = go on a trip", emoji="airplane"),
    dict(wrong="Is breakfast inside?", right="Is breakfast included?", note="«شامل میشه» = included", emoji="croissant"),
], ("تو سفر این‌جوری نگو ❌", CMT), suffix="b")

write_trial(107, "vocab", [
    dict(wrong="I'm listening.", right="I'm all ears.", note="یعنی «سراپا گوشم»", emoji="ear"),
    dict(wrong="help", right="lend a hand", note="یعنی «کمک کردن»", emoji="raising_hands"),
    dict(wrong="watch it", right="keep an eye on it", note="یعنی «حواست بهش باشه»", emoji="eyes"),
    dict(wrong="I'm joking.", right="I'm pulling your leg.", note="یعنی «سربه‌سرت می‌ذارم»", emoji="leg"),
], ("اصطلاح‌های بدن که بومی‌ها می‌گن 👂", SAVE), suffix="a", headline="اصطلاح‌هایی که بومی‌ها می‌گن",
   head_emoji="speech_balloon")
write_trial(107, "mistakes", [
    dict(wrong="I feel myself tired.", right="I feel tired.", note="بعد از feel، myself نمیاد", emoji="tired_face"),
    dict(wrong="I'm come from Iran.", right="I come from Iran.", note="با come، am لازم نیست", emoji="globe_showing_asia-australia"),
    dict(wrong="I'm live in Tehran.", right="I live in Tehran.", note="با live، am لازم نیست", emoji="house"),
], ("این am و myself ها اضافه‌ست ❌", CMT), suffix="b")

write_trial(108, "vocab", [
    dict(wrong="I love sweets.", right="I have a sweet tooth.", note="یعنی «عاشق شیرینی‌ام»", emoji="lollipop"),
    dict(wrong="very delicious", right="scrumptious", note="یعنی «فوق‌العاده خوشمزه»", emoji="face_savoring_food"),
    dict(wrong="old (bread)", right="stale", note="یعنی «بیات»", emoji="bread"),
    dict(wrong="no taste", right="bland", note="یعنی «بی‌مزه»", emoji="neutral_face"),
], ("طعم‌ها رو حرفه‌ای توصیف کن 😋", SAVE), suffix="a")
write_trial(108, "mistakes", [
    dict(wrong="The car of my father", right="My father's car", note="مالکیت آدم‌ها با 's", emoji="automobile"),
    dict(wrong="The house of Ali", right="Ali's house", note="خونه‌ی علی = Ali's house", emoji="house"),
    dict(wrong="The name of my teacher", right="My teacher's name", note="اسم معلمم = my teacher's name", emoji="teacher"),
], ("مالکیت رو این‌جوری نگو ❌", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

write_trial(109, "vocab", [
    dict(wrong="Good luck!", right="Best of luck!", note="یعنی «موفق باشی!»", emoji="four_leaf_clover"),
    dict(wrong="See you soon!", right="Catch you later!", note="یعنی «بعداً می‌بینمت!»", emoji="waving_hand"),
    dict(wrong="Goodbye, be well!", right="Take care!", note="یعنی «مراقب خودت باش!»", emoji="red_heart"),
    dict(wrong="I'm going now.", right="I'm off!", note="یعنی «من دیگه رفتم!»", emoji="person_walking"),
], ("خداحافظی مثل بومی‌ها 👋", SAVE), suffix="a")
write_trial(109, "mistakes", [
    dict(wrong="I will go to travel.", right="I'm going to travel.", note="برنامه‌ی قطعی = going to", emoji="airplane"),
    dict(wrong="I'm going to home.", right="I'm going home.", note="قبل از home حرف to نمیاد", emoji="house"),
    dict(wrong="I come back tomorrow.", right="I'll be back tomorrow.", note="برای آینده: I'll", emoji="spiral_calendar"),
], ("درباره‌ی آینده این‌جوری نگو ❌", CMT), suffix="b")

# ---------------------------------------------------------------- quote reels
write_quote(103, "Today's effort is tomorrow's result.",
            "تلاش امروز، نتیجه‌ی فرداست.",
            [("effort", "تلاش")], "سیو کن 📌", topic="hard work", palette="forest", figure=True)
write_quote(104, "Love is the best thing we can give each other.",
            "عشق بهترین چیزیه که می‌تونیم به هم بدیم.",
            [("each other", "همدیگه")], "ولنتاین مبارک ❤️ برای کسی که دوستش داری بفرست", topic="love", palette="rose",
            figure=True)
write_quote(105, "Real friends are rare. Keep them close.",
            "دوستای واقعی کمیابن؛ نگهشون دار.",
            [("rare", "کمیاب")], "برای دوست واقعیت بفرست 🤍", topic="friendship", sea=True)
write_quote(106, "Home is not a place. It's a feeling.",
            "خونه یه مکان نیست؛ یه حسه.",
            [("feeling", "حس")], "برای کسی که برات حکم خونه رو داره بفرست 🤍", topic="family")
write_quote(107, "The best time is the time you spend with people you love.",
            "بهترین زمان، زمانیه که با کسایی که دوستشون داری می‌گذرونی.",
            [("spend", "گذروندن")], "سیو کن 📌", topic="time", trees=True)
write_quote(108, "Be gentle with yourself, too.",
            "با خودتم مهربون باش.",
            [("gentle", "مهربون، ملایم")], "سپندارمذگان مبارک 🤍 برای کسی که بهش اهمیت می‌دی بفرست", topic="kindness",
            figure=True)
write_quote(109, "Better days are coming.",
            "روزای بهتری در راهه.",
            [("coming", "در راهه")], "برای کسی که منتظر روزای بهتره بفرست 🌱", topic="hope", sea=True)
