"""Week 2: Sat 7 Nov – Fri 13 Nov 2026 (days 5–11)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import *  # noqa

CLAIM = f"تو کامنت بنویس 👇"

write_day(5,
    hook=dict(l1="این ۴ تا کلمه رو", l2a="به", l2b="فرانسوی", l3="نگو!", l3emoji="face_with_raised_eyebrow",
              sub=f"انگلیسی{ZW}ها یه جور دیگه می{ZW}گن", subemoji="speaker_high_volume"),
    words=[
        dict(GLOW("تأکید روی {EN}", "ol"), en="biology", mark=[2, 3], emoji="dna", uni="🧬",
             ipa="/baɪˈɑːlədʒi/", wrong="بیولوژی", right="بایالِجی", fa=f"زیست{ZW}شناسی"),
        dict(GLOW("تأکید روی {EN}", "nol"), en="technology", mark=[4, 5, 6], emoji="robot", uni="🤖",
             ipa="/tekˈnɑːlədʒi/", wrong="تکنولوژی", right="تِکنالِجی", fa="فناوری"),
        dict(GLOW("تأکید روی {EN}", "chol"), en="psychology", mark=[3, 4, 5, 6], emoji="brain", uni="🧠",
             ipa="/saɪˈkɑːlədʒi/", wrong="پسیکولوژی", right="سایکالِجی", fa=f"روان{ZW}شناسی"),
        dict(GLOW("تأکید روی {EN}", "og"), en="geography", mark=[2, 3], emoji="globe_showing_europe-africa", uni="🌍",
             ipa="/dʒiˈɑːɡrəfi/", wrong="ژئوگرافی", right=f"جی{ZW}آگرِفی", fa="جغرافیا"),
    ],
    cap=("این ۴ تا کلمه رو به فرانسوی نگو 🙅", f"انگلیسی{ZW}ها تأکید رو روی بخش دوم می{ZW}ذارن 🔊"),
    stories=[
        dict(RECALL, word="think", ipa="/θɪŋk/", answer="فکر کردن"),
        dict(QUIZ, emoji="flexed_biceps", word="muscle", answer="c"),
        dict(MCQ, word="clothes", options=["غذا", f"لباس{ZW}ها", "کفش"], answer=1),
        dict(ASK, t1=f"یه کلمه{ZW}ی دیگه که", t2a="فرانسوی", t2b=f"می{ZW}گیم؟",
             body="ریپلای کن تا تلفظ انگلیسیشو\nتو ریلزهای بعدی بگم", example="garage"),
    ])

write_day(6,
    hook=dict(l1="تو این ۴ تا کلمه", l2a="حرف", l2b="b", l3="رو نخون!", l3emoji="cross_mark",
              sub="یه قانون ساده یاد بگیر", subemoji="light_bulb"),
    words=[
        dict(SIL("b"), en="climb", mark=[4], emoji="person_climbing", uni="🧗",
             ipa="/klaɪm/", wrong="کلایمب", right="کلایم", fa="بالا رفتن"),
        dict(SIL("b"), en="thumb", mark=[4], emoji="thumbs_up", uni="👍",
             ipa="/θʌm/", wrong="ثامب", right="ثام", fa="انگشت شست"),
        dict(SIL("b"), en="lamb", mark=[3], emoji="ewe", uni="🐑",
             ipa="/læm/", wrong="لَمب", right="لَم", fa="بره"),
        dict(SIL("b"), en="debt", mark=[2], emoji="money_with_wings", uni="💸",
             ipa="/det/", wrong="دِبت", right="دِت", fa="بدهی"),
    ],
    cap=("تو این ۴ تا کلمه حرف b رو نخون ❌", f"قانون: b بعد از m یا قبل از t معمولاً بی{ZW}صداست 🤫"),
    stories=[
        dict(RECALL, word="psychology", ipa="/saɪˈkɑːlədʒi/", answer=f"روان{ZW}شناسی"),
        dict(QUIZ, emoji="smiling_face_with_sunglasses", word="handsome", answer="d"),
        dict(MCQ, word="geography", options=["تاریخ", "ریاضی", "جغرافیا"], answer=2),
        dict(ASK, t1="کدوم کلمه رو", t2a="فردا تو ریلز", t2b="بیارم؟",
             body=f"یه کلمه که تلفظش برات سؤاله\nریپلای کن؛ شاید تو ریلز بعدی باشه", example="though"),
    ])

write_day(7,
    hook=dict(l1="ed آخر این فعل‌ها", l2a="رو", l2b="«اِد»", l3="نخون!", l3emoji="warning",
              sub=f"فقط بعد از t و d «اِد» خونده میشه", subemoji="light_bulb"),
    words=[
        dict(GLOW("اینجا {EN} = «ت»", "ed"), en="walked", mark=[4, 5], emoji="person_walking", uni="🚶",
             ipa="/wɔːkt/", wrong="واکِد", right="واکت", fa="راه رفت"),
        dict(GLOW("اینجا {EN} = «د»", "ed"), en="played", mark=[4, 5], emoji="video_game", uni="🎮",
             ipa="/pleɪd/", wrong="پلِیِد", right="پلِید", fa="بازی کرد"),
        dict(GLOW("اینجا {EN} = «ت»", "ed"), en="stopped", mark=[5, 6], emoji="stop_sign", uni="🛑",
             ipa="/stɑːpt/", wrong="استاپِد", right="استاپت", fa="متوقف شد"),
        dict(GLOW("اینجا {EN} = «د»", "ed"), en="cleaned", mark=[5, 6], emoji="sponge", uni="🧽",
             ipa="/kliːnd/", wrong="کلینِد", right="کلیند", fa="تمیز کرد"),
    ],
    cap=("ed آخر این ۴ فعل رو «اِد» نخون ❌", f"فقط بعد از t و d صدای «اِد» میده 💡"),
    stories=[
        dict(RECALL, word="debt", ipa="/det/", answer="بدهی"),
        dict(QUIZ, emoji="books", word="knowledge", answer="k"),
        dict(MCQ, word="climb", options=["بالا رفتن", "دویدن", "شنا کردن"], answer=0),
        dict(ASK, t1="یه فعل که", t2a=f"گذشته{ZW}اش", t2b="سخته؟",
             body="ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی یادت بدم", example="watched"),
    ])

write_day(8,
    hook=dict(l1="این ۴ تا کلمه رو", l2a="بدون", l2b="L", l3="بگو!", l3emoji="zipper-mouth_face",
              sub=f"حرف L این{ZW}جا بی{ZW}صداست", subemoji="shushing_face"),
    words=[
        dict(SIL("l"), en="calm", mark=[2], emoji="relieved_face", uni="😌",
             ipa="/kɑːm/", wrong="کالم", right="کام", fa="آرام"),
        dict(SIL("l"), en="half", mark=[2], emoji="watermelon", uni="🍉",
             ipa="/hæf/", wrong="هالف", right="هَف", fa="نصف"),
        dict(SIL("l"), en="talk", mark=[2], emoji="speech_balloon", uni="💬",
             ipa="/tɔːk/", wrong="تالک", right="تاک", fa="صحبت کردن"),
        dict(SIL("l"), en="could", mark=[3], emoji="flexed_biceps", uni="💪",
             ipa="/kʊd/", wrong="کولد", right="کُد", fa=f"می{ZW}تونست"),
    ],
    cap=("حرف l تو این ۴ کلمه خونده نمیشه 🤐", "مثل salmon که روز اول دیدیم 🐟"),
    stories=[
        dict(RECALL, word="stopped", ipa="/stɑːpt/", answer="متوقف شد"),
        dict(QUIZ, emoji="classical_building", word="column", answer="n"),
        dict(MCQ, word="played", options=["خورد", "خوابید", "بازی کرد"], answer=2),
        dict(ASK, t1=f"کدوم کلمه{ZW}ی انگلیسی", t2a="همیشه", t2b=f"گیجت می{ZW}کنه؟",
             body="ریپلای کن تا تلفظ درستشو\nتو ریلزهای بعدی یادت بدم", example="said"),
    ])

write_day(9,
    hook=dict(l1="این ۴ تا کلمه یه", l2a="h", l2b=f"بی{ZW}صدا", l3="دارن", l3emoji="ghost",
              sub="حتی وسط کلمه!", subemoji="exploding_head"),
    words=[
        dict(SIL("h"), en="hour", mark=[0], emoji="hourglass_done", uni="⌛",
             ipa="/ˈaʊər/", wrong="هاوِر", right="آوِر", fa="یک ساعت"),
        dict(SIL("h"), en="honest", mark=[0], emoji="handshake", uni="🤝",
             ipa="/ˈɑːnɪst/", wrong="هانِست", right="آنِست", fa="صادق"),
        dict(SIL("h"), en="vehicle", mark=[2], emoji="automobile", uni="🚗",
             ipa="/ˈviːəkəl/", wrong="وِهیکِل", right="ویِکِل", fa=f"وسیله{ZW}ی نقلیه"),
        dict(SIL("h"), en="exhausted", mark=[2], emoji="tired_face", uni="😫",
             ipa="/ɪɡˈzɔːstɪd/", wrong="اِکسهاستِد", right="ایگزاستِد", fa="خیلی خسته"),
    ],
    cap=(f"این ۴ تا کلمه یه h بی{ZW}صدا دارن 👻", f"حتی وسط کلمه هم پیداش می{ZW}شه 🤯"),
    stories=[
        dict(RECALL, word="calm", ipa="/kɑːm/", answer="آرام"),
        dict(QUIZ, emoji="ghost", word="ghost", answer="h"),
        dict(MCQ, word="half", options=["دوبرابر", "نصف", "کامل"], answer=1),
        dict(ASK, t1="یه کلمه که همیشه", t2a="تلفظش برات", t2b="سخته؟",
             body="برام ریپلای کن تا تو ریلزهای بعدی\nتلفظ درستشو یادت بدم", example="world"),
    ])

write_day(10,
    hook=dict(l1="این ۴ تا کلمه رو", l2a="تقریباً", l2b="همه", l3=f"اشتباه می{ZW}گن", l3emoji="grimacing_face",
              sub="حرف صدادارشون عجیبه!", subemoji="eyes"),
    words=[
        dict(GLOW("اینجا {EN} = «ای»", "o"), en="women", mark=[1], emoji="woman", uni="👩",
             ipa="/ˈwɪmɪn/", wrong="وومِن", right="ویمِن", fa=f"زن{ZW}ها"),
        dict(GLOW("اینجا {EN} = «ای»", "u"), en="busy", mark=[1], emoji="laptop", uni="💻",
             ipa="/ˈbɪzi/", wrong="بیوزی", right="بیزی", fa="سرشلوغ"),
        dict(GLOW("اینجا {EN} = «اِ»", "u"), en="bury", mark=[1], emoji="gem_stone", uni="💎",
             ipa="/ˈberi/", wrong="بیوری", right="بِری", fa="دفن کردن"),
        dict(GLOW("اینجا {EN} = «اِ»", "u"), en="minute", mark=[3], emoji="timer_clock", uni="⏲️",
             ipa="/ˈmɪnɪt/", wrong="مینیوت", right="مینِت", fa="دقیقه"),
    ],
    cap=(f"این ۴ تا کلمه رو تقریباً همه اشتباه می{ZW}گن 😬", f"حرف صدادارشون اون{ZW}جوری که فکر می{ZW}کنی خونده نمیشه 👀"),
    stories=[
        dict(RECALL, word="honest", ipa="/ˈɑːnɪst/", answer="صادق"),
        dict(QUIZ, emoji="watch", word="wrist", answer="w"),
        dict(MCQ, word="exhausted", options=["خیلی خوشحال", "خیلی گرسنه", "خیلی خسته"], answer=2),
        dict(ASK, t1="کدوم کلمه رو", t2a="فردا تو ریلز", t2b="بیارم؟",
             body=f"یه کلمه که تلفظش برات سؤاله\nریپلای کن؛ شاید تو ریلز بعدی باشه", example="squirrel"),
    ])

write_day(11,
    hook=dict(l1=f"g تو این کلمه{ZW}ها", l2a="اصلاً", l2b="خونده", l3="نمیشه!", l3emoji="shushing_face",
              sub="قانون: gn یعنی «ن»", subemoji="light_bulb"),
    words=[
        dict(SIL("g"), en="sign", mark=[2], emoji="writing_hand", uni="✍️",
             ipa="/saɪn/", wrong="سایگن", right="ساین", fa="امضا کردن"),
        dict(SIL("g"), en="foreign", mark=[5], emoji="airplane", uni="✈️",
             ipa="/ˈfɔːrən/", wrong="فورِیگن", right="فارِن", fa="خارجی"),
        dict(SIL("g"), en="campaign", mark=[6], emoji="megaphone", uni="📣",
             ipa="/kæmˈpeɪn/", wrong="کَمپِیگن", right="کَمپِین", fa="کارزار"),
        dict(SIL("g"), en="reign", mark=[3], emoji="crown", uni="👑",
             ipa="/reɪn/", wrong="رِیگن", right="رِین", fa="سلطنت"),
    ],
    cap=("g تو این ۴ تا کلمه اصلاً خونده نمیشه 🤫", "قانون: gn معمولاً یعنی «ن» 💡"),
    stories=[
        dict(RECALL, word="busy", ipa="/ˈbɪzi/", answer="سرشلوغ"),
        dict(QUIZ, emoji="wrench", word="plumber", answer="b"),
        dict(MCQ, word="minute", options=["ساعت", "دقیقه", "ثانیه"], answer=1),
        dict(ASK, t1=f"از کلمه{ZW}های این هفته", t2a="کدوم", t2b=f"سخت{ZW}تر بود؟",
             body=f"ریپلای کن؛ هفته{ZW}ی بعد\nبیشتر تمرینش می{ZW}کنیم", example="vehicle"),
    ])
