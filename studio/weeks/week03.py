"""Week 3: Sat 14 Nov – Fri 20 Nov 2026 (days 12–18). Steered by growth/learnings.md: sounds Iranians replace
(like day04 th), rule-based sound themes (-s, -ed), only one silent-letter reel, everyday words."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

TH = GLOW(f"صدای {{EN}}: زبون بین دندون{ZW}ها", "th", "tongue")

write_day(12,
    hook=dict(l1="این ۴ تا کلمه رو", l2a="با", l2b="«د» و «ز»", l3="نگو!", l3emoji="cross_mark",
              sub="زبونتو بذار بین دندونات", subemoji="tongue"),
    words=[
        dict(TH, en="mother", mark=[2, 3], emoji="woman", uni="👩",
             ipa="/ˈmʌðər/", wrong="مادِر", right="مَذِر", fa="مادر"),
        dict(TH, en="brother", mark=[3, 4], emoji="boy", uni="👦",
             ipa="/ˈbrʌðər/", wrong="برادِر", right="بْرَذِر", fa="برادر"),
        dict(TH, en="weather", mark=[3, 4], emoji="sun_behind_cloud", uni="⛅",
             ipa="/ˈweðər/", wrong="وِدِر", right="وِذِر", fa="آب و هوا"),
        dict(TH, en="father", mark=[2, 3], emoji="man", uni="👨",
             ipa="/ˈfɑːðər/", wrong="فادِر", right="فاذِر", fa="پدر"),
    ],
    cap=("این ۴ تا کلمه رو با «د» و «ز» نگو ❌", f"th این{ZW}جا یه صدای نرمه: زبونتو بذار بین دندونات 👅"),
    stories=[
        dict(RECALL, word="foreign", ipa="/ˈfɔːrən/", answer="خارجی"),
        dict(QUIZ, emoji="barber_pole", word="comb", answer="b"),
        dict(MCQ, word="sign", options=["امضا کردن", "خوابیدن", "نوشیدن"], answer=0),
        dict(ASK, t1="یه کلمه با th که", t2a="تلفظش", t2b="سخته؟",
             body="ریپلای کن تا تو ریلزهای بعدی\nبا هم تمرینش کنیم", example="breathe"),
    ])

write_day(13,
    hook=dict(l1="اسم این ۴ تا برند", l2a="رو", l2b="اشتباه", l3=f"می{ZW}گی!", l3emoji="astonished_face",
              sub=f"انگلیسی{ZW}ها این{ZW}جوری می{ZW}گن", subemoji="speaker_high_volume"),
    words=[
        dict(GLOW("{EN} آخر = «ای»", "e"), en="Nike", mark=[3], emoji="running_shoe", uni="👟",
             ipa="/ˈnaɪki/", wrong="نایک", right="نایکی", fa="برند ورزشی", ph="nˈaɪki"),
        dict(GLOW("تأکید روی {EN}", "di"), en="Adidas", mark=[2, 3], emoji="soccer_ball", uni="⚽",
             ipa="/əˈdiːdəs/", wrong="آدیداس", right="اِدیدِس", fa="برند ورزشی", ph="ədˈidəs"),
        dict(GLOW("اینجا {EN} = «هان»", "Hyun"), en="Hyundai", mark=[0, 1, 2, 3], emoji="automobile", uni="🚗",
             ipa="/ˈhʌndeɪ/", wrong="هیوندای", right="هاندِی", fa=f"خودروساز کره{ZW}ای", tts="Hunday"),
        dict(GLOW("اینجا {EN} = «سانگ»", "sung"), en="Samsung", mark=[3, 4, 5, 6], emoji="mobile_phone", uni="📱",
             ipa="/ˈsæmsʌŋ/", wrong="سامسونگ", right="سَمسانگ", fa="برند موبایل"),
    ],
    cap=(f"اسم این ۴ تا برند رو اشتباه می{ZW}گی 😳", f"انگلیسی{ZW}ها این{ZW}جوری تلفظشون می{ZW}کنن 🔊 برای دوستت بفرست"),
    stories=[
        dict(RECALL, word="weather", ipa="/ˈweðər/", answer="آب و هوا"),
        dict(QUIZ, emoji="speech_balloon", word="answer", answer="w"),
        dict(MCQ, word="brother", options=["خواهر", "پدر", "برادر"], answer=2),
        dict(ASK, t1="اسم کدوم برند رو", t2a="مطمئن", t2b="نیستی؟",
             body=f"ریپلای کن؛ شاید تو\nریلز بعدی باشه", example="Porsche"),
    ])

write_day(14,
    hook=dict(l1=f"s آخر این کلمه{ZW}ها", l2a="رو", l2b="«س»", l3="نخون!", l3emoji="warning",
              sub=f"بیشتر وقتا صدای «ز» میده", subemoji="light_bulb"),
    words=[
        dict(GLOW("اینجا {EN} = «ز»", "s"), en="dogs", mark=[3], emoji="dog_face", uni="🐶",
             ipa="/dɔːɡz/", wrong="داگس", right="داگز", fa=f"سگ{ZW}ها"),
        dict(GLOW("اینجا {EN} = «ز»", "s"), en="eyes", mark=[3], emoji="eyes", uni="👀",
             ipa="/aɪz/", wrong="آیس", right="آیز", fa=f"چشم{ZW}ها"),
        dict(GLOW("اینجا {EN} = «ایز»", "es"), en="buses", mark=[3, 4], emoji="bus", uni="🚌",
             ipa="/ˈbʌsɪz/", wrong="باسس", right="باسِز", fa=f"اتوبوس{ZW}ها"),
        dict(GLOW("اینجا {EN} = «ایز»", "es"), en="oranges", mark=[5, 6], emoji="tangerine", uni="🍊",
             ipa="/ˈɔːrɪndʒɪz/", wrong="اورنجس", right="اورِنجِز", fa=f"پرتقال{ZW}ها"),
    ],
    cap=("s آخر این ۴ کلمه رو «س» نخون ❌", f"بعد از صداهای نرم میشه «ز»، بعد از s و ch و j میشه «ایز» 💡"),
    stories=[
        dict(RECALL, word="Hyundai", ipa="/ˈhʌndeɪ/", answer="هاندِی",
             q="چطوری خونده میشه؟", cta="تلفظشو ریپلای کن"),
        dict(QUIZ, emoji="palm_tree", word="palm", answer="l"),
        dict(MCQ, word="Nike", q=f"درستش کدومه؟", options=["نایک", "نایکی", "نیک"], answer=1),
        dict(ASK, t1=f"یه کلمه{ZW}ی جمع که", t2a="گیجت", t2b=f"می{ZW}کنه؟",
             body="ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی یادت بدم", example="children"),
    ])

write_day(15,
    hook=dict(l1="این ۴ تا کلمه رو", l2a="با", l2b="«اِ»", l3="شروع نکن!", l3emoji="cross_mark",
              sub=f"انگلیسی{ZW}ها مستقیم با s شروع می{ZW}کنن", subemoji="speaker_high_volume"),
    words=[
        dict(GLOW("{EN} بدون «اِ» اولش", "sch"), en="school", mark=[0, 1, 2], emoji="school", uni="🏫",
             ipa="/skuːl/", wrong="اِسکول", right="سْکول", fa="مدرسه"),
        dict(GLOW("{EN} بدون «اِ» اولش", "str"), en="street", mark=[0, 1, 2], emoji="motorway", uni="🛣️",
             ipa="/striːt/", wrong="اِستریت", right="سْتْریت", fa="خیابان"),
        dict(GLOW("{EN} بدون «اِ» اولش", "sm"), en="smile", mark=[0, 1], emoji="smiling_face_with_smiling_eyes", uni="😊",
             ipa="/smaɪl/", wrong="اِسمایل", right="سْمایل", fa="لبخند"),
        dict(GLOW("{EN} بدون «اِ» اولش", "sp"), en="sport", mark=[0, 1], emoji="basketball", uni="🏀",
             ipa="/spɔːrt/", wrong="اِسپُرت", right="سْپُرت", fa="ورزش"),
    ],
    cap=("این ۴ تا کلمه رو با «اِ» شروع نکن ❌", f"s اول کلمه بدون «اِ» گفته میشه؛ بلند تکرار کن 🔊"),
    stories=[
        dict(RECALL, word="oranges", ipa="/ˈɔːrɪndʒɪz/", answer=f"پرتقال{ZW}ها"),
        dict(QUIZ, emoji="wrapped_gift", word="wrap", answer="w"),
        dict(MCQ, word="eyes", options=[f"گوش{ZW}ها", f"دست{ZW}ها", f"چشم{ZW}ها"], answer=2),
        dict(ASK, t1="یه کلمه که با", t2a="«اِ»", t2b=f"شروعش می{ZW}کنی؟",
             body="ریپلای کن تا تو ریلزهای بعدی\nتلفظ درستشو بگم", example="Spain"),
    ])

write_day(16,
    hook=dict(l1="تو این ۴ تا کلمه", l2a="حرف", l2b="k", l3="رو نخون!", l3emoji="zipper-mouth_face",
              sub="قانون: kn یعنی «ن»", subemoji="light_bulb"),
    words=[
        dict(SIL("k"), en="knee", mark=[0], emoji="leg", uni="🦵",
             ipa="/niː/", wrong="کْنی", right="نی", fa="زانو"),
        dict(SIL("k"), en="know", mark=[0], emoji="thinking_face", uni="🤔",
             ipa="/noʊ/", wrong="کْنو", right="نُو", fa="دونستن"),
        dict(SIL("k"), en="knock", mark=[0], emoji="door", uni="🚪",
             ipa="/nɑːk/", wrong="کْناک", right="ناک", fa="در زدن"),
        dict(SIL("k"), en="knight", mark=[0], emoji="horse_face", uni="🐴",
             ipa="/naɪt/", wrong="کْنایت", right="نایت", fa="شوالیه"),
    ],
    cap=("تو این ۴ تا کلمه k رو نخون 🤐", "قانون: kn اول کلمه یعنی «ن» 💡"),
    stories=[
        dict(RECALL, word="street", ipa="/striːt/", answer="خیابان"),
        dict(QUIZ, emoji="scissors", word="scissors", answer="c"),
        dict(MCQ, word="smile", options=["لبخند", "گریه", "فریاد"], answer=0),
        dict(ASK, t1=f"کدوم حرف بی{ZW}صدا", t2a="بیشتر", t2b=f"گیجت می{ZW}کنه؟",
             body=f"ریپلای کن؛ هفته{ZW}ی بعد\nیه ریلز براش می{ZW}سازم", example="wrestle"),
    ])

write_day(17,
    hook=dict(l1="این ۴ تا کلمه رو", l2a="مثل", l2b="فارسی", l3="نگو!", l3emoji="face_with_raised_eyebrow",
              sub=f"انگلیسیش یه جور دیگه{ZW}ست", subemoji="speaker_high_volume"),
    words=[
        dict(GLOW("اینجا {EN} = «اِی»", "a"), en="radio", mark=[1], emoji="radio", uni="📻",
             ipa="/ˈreɪdioʊ/", wrong="رادیو", right="رِیدیو", fa="رادیو"),
        dict(GLOW("اینجا {EN} = «اَ»", "a"), en="camera", mark=[1], emoji="camera", uni="📷",
             ipa="/ˈkæmərə/", wrong="کامِرا", right="کَمرا", fa="دوربین"),
        dict(GLOW("اینجا {EN} = «اِ»", "a"), en="salad", mark=[3], emoji="green_salad", uni="🥗",
             ipa="/ˈsæləd/", wrong="سالاد", right="سَلِد", fa="سالاد"),
        dict(GLOW("اینجا {EN} = «اَ»", "a"), en="piano", mark=[2], emoji="musical_keyboard", uni="🎹",
             ipa="/piˈænoʊ/", wrong="پیانو", right="پیَنُو", fa="پیانو"),
    ],
    cap=("این ۴ تا کلمه رو مثل فارسی نگو 🙅", f"تو فارسی هم داریمشون، ولی انگلیسیش فرق داره 🔊"),
    stories=[
        dict(RECALL, word="knee", ipa="/niː/", answer="زانو"),
        dict(QUIZ, emoji="egg", word="yolk", answer="l"),
        dict(MCQ, word="knock", options=["دویدن", "در زدن", "پریدن"], answer=1),
        dict(ASK, t1=f"یه کلمه که فارسی", t2a="هم", t2b="داریمش؟",
             body="ریپلای کن تا تلفظ انگلیسیشو\nتو ریلزهای بعدی بگم", example="pajamas"),
    ])

write_day(18,
    hook=dict(l1="این ۴ تا فعل رو", l2a="با", l2b="«اِد»", l3="نگو!", l3emoji="warning",
              sub="فقط بعد از t و d «اِد» داریم", subemoji="light_bulb"),
    words=[
        dict(GLOW("اینجا {EN} = «ت»", "ed"), en="watched", mark=[5, 6], emoji="television", uni="📺",
             ipa="/wɑːtʃt/", wrong="واچِد", right="واچت", fa="تماشا کرد"),
        dict(GLOW("اینجا {EN} = «ت»", "ed"), en="laughed", mark=[5, 6], emoji="face_with_tears_of_joy", uni="😂",
             ipa="/læft/", wrong="لافِد", right="لَفت", fa="خندید"),
        dict(GLOW("اینجا {EN} = «ت»", "ed"), en="asked", mark=[3, 4], emoji="person_raising_hand", uni="🙋",
             ipa="/æskt/", wrong="اَسکِد", right="اَسکت", fa="پرسید"),
        dict(GLOW("اینجا {EN} = «د»", "ed"), en="lived", mark=[3, 4], emoji="house", uni="🏠",
             ipa="/lɪvd/", wrong="لیوِد", right="لیود", fa="زندگی کرد"),
    ],
    cap=("این ۴ تا فعل رو با «اِد» نگو ❌", f"یادته؟ فقط بعد از t و d صدای «اِد» میده 💡"),
    stories=[
        dict(RECALL, word="camera", ipa="/ˈkæmərə/", answer="دوربین"),
        dict(QUIZ, emoji="guitar", word="guitar", answer="u"),
        dict(MCQ, word="radio", q=f"درستش کدومه؟", options=["رِیدیو", "رادیو", "رادیِو"], answer=0),
        dict(ASK, t1="این هفته کدوم کلمه", t2a="برات", t2b="جدید بود؟",
             body=f"ریپلای کن؛ هفته{ZW}ی بعد\nکلمه{ZW}های بیشتری میارم", example="Hyundai"),
    ])
