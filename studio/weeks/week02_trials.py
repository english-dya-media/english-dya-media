"""Trial reels of week 2 (days 6-11, one a day). Kept as the example for writing trial reels.
From day 12 there are two a day: write_trial(N, "vocab", ..., suffix="a") and write_trial(N, "mistakes", ..., suffix="b")."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import write_trial, ZW

write_trial(6, "mistakes", [
    dict(wrong="I am agree.", right="I agree.", note=f"agree خودش فعله، am نمی{ZW}خواد", emoji="handshake"),
    dict(wrong="I have 25 years old.", right="I am 25 years old.", note="برای سن از am استفاده کن، نه have", emoji="birthday_cake"),
    dict(wrong="I'm boring.", right="I'm bored.", note=f"boring یعنی «خسته{ZW}کننده»! 😅", emoji="sleeping_face"),
], (f"۳ تا اشتباه که تقریباً همه می{ZW}کنن 😬", f"تو کدومشو می{ZW}گفتی؟ برای دوستت بفرست که اونم بدونه 👇"), slot="19:00")

write_trial(7, "vocab", [
    dict(wrong="very tired", right="exhausted", note="یعنی «خیلی خسته»", emoji="tired_face"),
    dict(wrong="very hungry", right="starving", note="یعنی «خیلی گرسنه»", emoji="face_savoring_food"),
    dict(wrong="very happy", right="thrilled", note=f"یعنی «خیلی خوشحال و هیجان{ZW}زده»", emoji="star-struck"),
    dict(wrong="very big", right="huge", note="یعنی «خیلی بزرگ»", emoji="elephant"),
], ("به جای very این ۴ تا کلمه رو بگو 😎", "کدومشو بلد نبودی؟ سیو کن و برای دوستت بفرست 👇"), slot="19:00")

write_trial(8, "mistakes", [
    dict(wrong="He is more taller.", right="He is taller.", note="taller خودش یعنی «بلندتر»", emoji="person_shrugging"),
    dict(wrong="I didn't went.", right="I didn't go.", note="بعد از didn't فعل ساده میاد", emoji="see-no-evil_monkey"),
    dict(wrong="I go to home.", right="I go home.", note="قبل از home حرف to نمیاد", emoji="house"),
], ("این ۳ تا جمله رو اشتباه نگو ❌", f"برای کسی که همیشه این{ZW}جوری می{ZW}گه بفرست 😅"), slot="19:00")

write_trial(9, "vocab", [
    dict(wrong="very scared", right="terrified", note="یعنی «خیلی ترسیده»", emoji="face_screaming_in_fear"),
    dict(wrong="very cold", right="freezing", note=f"یعنی «خیلی سرد، یخ{ZW}زده»", emoji="cold_face"),
    dict(wrong="very small", right="tiny", note="یعنی «خیلی کوچیک»", emoji="ant"),
    dict(wrong="very angry", right="furious", note="یعنی «خیلی عصبانی»", emoji="pouting_face"),
], ("دیگه نگو very scared یا very angry ❌", f"این کلمه{ZW}ها رو یاد بگیر و حرفه{ZW}ای{ZW}تر حرف بزن 😎 برای دوستت بفرست 👇"), slot="19:00")

write_trial(10, "mistakes", [
    dict(wrong="She don't like it.", right="She doesn't like it.", note="برای she و he از doesn't استفاده کن", emoji="person_facepalming"),
    dict(wrong="Say me the truth.", right="Tell me the truth.", note="«بهم بگو» میشه tell me، نه say me", emoji="face_with_tears_of_joy"),
    dict(wrong="Explain me.", right="Explain it to me.", note="بعد از explain حرف to لازمه", emoji="thinking_face"),
], (f"۳ اشتباه رایج تو مکالمه{ZW}ی انگلیسی 🙈", "سیو کن و برای دوستت بفرست 👇"), slot="19:00")

write_trial(11, "vocab", [
    dict(wrong="very good", right="excellent", note="یعنی «عالی»", emoji="trophy"),
    dict(wrong="very funny", right="hilarious", note=f"یعنی «خیلی خنده{ZW}دار»", emoji="rolling_on_the_floor_laughing"),
    dict(wrong="very beautiful", right="gorgeous", note="یعنی «خیلی زیبا»", emoji="rose"),
    dict(wrong="very bad", right="terrible", note="یعنی «افتضاح»", emoji="thumbs_down"),
], ("very good و very bad رو بذار کنار 😅", f"این ۴ تا کلمه خیلی قشنگ{ZW}ترن. سیو کن که یادت نره 📌"), slot="19:00")
