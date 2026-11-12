"""Quote reels of week 3 (days 12-18), a different topic every day."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import write_quote, ZW

write_quote(12, "Believe in yourself, even when no one else does.",
            f"به خودت باور داشته باش، حتی وقتی هیچ{ZW}کس دیگه باور نداره.",
            [("believe in", "باور داشتن به")],
            f"برای کسی که امروز باید اینو بشنوه بفرست 🤍", topic="self-belief", figure=True)

write_quote(13, "Be patient. Good things take time.",
            f"صبور باش؛ چیزای خوب زمان می{ZW}برن.",
            [("patient", "صبور"), ("take time", "زمان بردن")],
            f"سیو کن برای روزایی که عجله داری 📌", topic="patience")

write_quote(14, "A true friend stays when everyone else leaves.",
            f"دوست واقعی وقتی همه می{ZW}رن، می{ZW}مونه.",
            [("true friend", "دوست واقعی"), ("stays", f"می{ZW}مونه")],
            "برای دوست واقعیت بفرست 🤍", topic="friendship", sea=True)

write_quote(15, "Be kind. Everyone is fighting a battle you know nothing about.",
            f"مهربون باش؛ هر کسی داره با چیزی می{ZW}جنگه که تو ازش خبر نداری.",
            [("kind", "مهربان"), ("battle", "نبرد، جنگ")],
            f"برای یه آدم مهربون بفرست 🤍", topic="kindness")

write_quote(16, "The sun will rise again tomorrow.",
            f"فردا دوباره خورشید طلوع می{ZW}کنه.",
            [("rise", "طلوع کردن، بالا اومدن")],
            f"برای کسی که این روزا ناامیده بفرست 🌅", topic="hope", sea=True, figure=True)

write_quote(17, "Be thankful for small things. They make a happy life.",
            f"قدر چیزای کوچیک رو بدون؛ همینا یه زندگیِ شاد می{ZW}سازن.",
            [("thankful", "قدردان، سپاسگزار")],
            "برای مامانت بفرست 🤍", topic="gratitude")

write_quote(18, "Rest is not a waste of time.",
            "استراحت کردن وقت تلف کردن نیست.",
            [("rest", "استراحت"), ("waste of time", "اتلاف وقت")],
            f"برای کسی که همیشه خسته{ZW}ست بفرست 😴", topic="rest", figure=True)
