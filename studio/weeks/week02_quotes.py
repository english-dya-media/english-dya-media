"""Quote reels of week 2 (days 10-11; quotes start on 12 Nov). Kept as the example for writing quotes."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import write_quote, ZW

write_quote(10, "Stop overthinking. You can't control everything.",
            f"انقدر فکر و خیال نکن؛ نمی{ZW}تونی همه{ZW}چیز رو کنترل کنی.",
            [("overthinking", "فکر و خیالِ زیاد")],
            f"برای کسی که این روزا زیادی فکر می{ZW}کنه بفرست 🤍", topic="peace of mind", palette="night", figure=True)

write_quote(11, "Fall seven times, stand up eight.",
            "اگه هفت بار زمین خوردی، هشت بار بلند شو.",
            [("fall", "زمین خوردن"), ("stand up", "بلند شدن")],
            f"سیو کن برای روزایی که خسته{ZW}ای 📌", topic="trying again", author="Japanese proverb", palette="sunset", sea=True, figure=True)
