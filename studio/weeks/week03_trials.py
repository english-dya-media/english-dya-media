"""Trial reels of week 3 (days 12-18): "a" = vocab at 15:00, "b" = mistakes at 19:00.
No format has 2x the views of the other yet (trial06-08: 121-132 views), so both formats stay."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from daygen import write_trial, ZW

# day 12
write_trial(12, "vocab", [
    dict(wrong="very sad", right="miserable", note="یعنی «خیلی ناراحت»", emoji="crying_face"),
    dict(wrong="very dirty", right="filthy", note="یعنی «خیلی کثیف»", emoji="wastebasket"),
    dict(wrong="very clean", right="spotless", note="یعنی «تمیزِ تمیز»", emoji="sparkles"),
    dict(wrong="very old", right="ancient", note="یعنی «خیلی قدیمی»", emoji="moai"),
], ("به جای very sad و very old اینا رو بگو 😎", "سیو کن که یادت نره 📌"), suffix="a")
write_trial(12, "mistakes", [
    dict(wrong="Open the light.", right="Turn on the light.", note=f"چراغ رو turn on می{ZW}کنن، نه open", emoji="light_bulb"),
    dict(wrong="He said me.", right="He told me.", note=f"«بهم گفت» میشه told me", emoji="speech_balloon"),
    dict(wrong="She is teacher.", right="She is a teacher.", note="قبل از شغل a لازمه", emoji="woman_teacher"),
], (f"۳ تا جمله که از فارسی ترجمه می{ZW}کنیم ❌", f"تو کدومشو می{ZW}گفتی؟ برای دوستت بفرست 👇"), suffix="b")

# day 13
write_trial(13, "vocab", [
    dict(wrong="I don't know.", right="I have no idea.", note=f"یعنی «اصلاً نمی{ZW}دونم»", emoji="person_shrugging"),
    dict(wrong="Goodbye.", right="See you later!", note="یعنی «بعداً می‌بینمت»", emoji="waving_hand"),
    dict(wrong="Thank you.", right="I appreciate it.", note="یعنی «واقعاً ممنونم»", emoji="folded_hands"),
    dict(wrong="Wait.", right="Hang on.", note="یعنی «یه لحظه صبر کن»", emoji="raised_hand"),
], (f"این{ZW}جوری حرف بزن تا مثل بومی{ZW}ها به نظر بیای 😎", "برای دوستت بفرست که اونم یاد بگیره 👇"), suffix="a")
write_trial(13, "mistakes", [
    dict(wrong="How it is?", right="How is it?", note="تو سؤال is میاد قبل از it", emoji="thinking_face"),
    dict(wrong="I am waiting you.", right="I'm waiting for you.", note="بعد از wait حرف for میاد", emoji="hourglass_not_done"),
    dict(wrong="Close the TV.", right="Turn off the TV.", note=f"تلویزیون رو turn off می{ZW}کنن", emoji="television"),
], (f"این ۳ تا رو تقریباً همه اشتباه می{ZW}گن 😬", "سیو کن و برای دوستت بفرست 👇"), suffix="b")

# day 14
write_trial(14, "vocab", [
    dict(wrong="very hot", right="boiling", note=f"یعنی «خیلی داغ، جوشان»", emoji="hot_face"),
    dict(wrong="very wet", right="soaked", note="یعنی «خیسِ خیس»", emoji="umbrella_with_rain_drops"),
    dict(wrong="very quiet", right="silent", note="یعنی «کاملاً ساکت»", emoji="zipper-mouth_face"),
    dict(wrong="very clever", right="brilliant", note="یعنی «خیلی باهوش»", emoji="light_bulb"),
], ("very رو بذار کنار؛ این ۴ تا کلمه رو بگو 😎", "سیو کن که یادت نره 📌"), suffix="a")
write_trial(14, "mistakes", [
    dict(wrong="I went to shopping.", right="I went shopping.", note="قبل از shopping حرف to نمیاد", emoji="shopping_bags"),
    dict(wrong="I'm married with her.", right="I'm married to her.", note="married to درسته، نه with", emoji="ring"),
    dict(wrong="Take a photo from me.", right="Take a photo of me.", note=f"عکس «از» کسی میشه of", emoji="camera_with_flash"),
], (f"تو هم این ۳ تا رو این{ZW}جوری می{ZW}گی؟ 🙈", f"برای کسی که همیشه این{ZW}جوری می{ZW}گه بفرست 😅"), suffix="b")

# day 15
write_trial(15, "vocab", [
    dict(wrong="very important", right="essential", note="یعنی «خیلی مهم، ضروری»", emoji="star"),
    dict(wrong="very rich", right="wealthy", note="یعنی «خیلی پولدار»", emoji="money_bag"),
    dict(wrong="very surprised", right="shocked", note="یعنی «شوکه»", emoji="astonished_face"),
    dict(wrong="very tasty", right="delicious", note="یعنی «خیلی خوشمزه»", emoji="face_savoring_food"),
], ("به جای very این ۴ تا کلمه رو بگو 😎", "کدومشو بلد نبودی؟ سیو کن و برای دوستت بفرست 👇"), suffix="a")
write_trial(15, "mistakes", [
    dict(wrong="I very like it.", right="I really like it.", note="very قبل از فعل نمیاد؛ really بگو", emoji="red_heart"),
    dict(wrong="I forgot it at home.", right="I left it at home.", note=f"«جا گذاشتم» میشه left", emoji="house"),
    dict(wrong="I lost the bus.", right="I missed the bus.", note=f"اتوبوس رو miss می{ZW}کنی، نه lose", emoji="bus"),
], (f"۳ اشتباه رایج تو مکالمه{ZW}ی انگلیسی ❌", f"تو کدومشو می{ZW}گفتی؟ برای دوستت بفرست 👇"), suffix="b")

# day 16
write_trial(16, "vocab", [
    dict(wrong="very easy", right="a piece of cake", note="یعنی «خیلی آسون»", emoji="shortcake"),
    dict(wrong="very busy", right="swamped", note=f"یعنی «سرم خیلی شلوغه»", emoji="laptop"),
    dict(wrong="very full", right="stuffed", note=f"یعنی «خیلی سیر» (بعد از غذا)", emoji="pizza"),
    dict(wrong="very sleepy", right="drowsy", note=f"یعنی «خیلی خواب{ZW}آلود»", emoji="yawning_face"),
], (f"بومی{ZW}ها این{ZW}جوری حرف می{ZW}زنن 😎", "سیو کن که یادت نره 📌"), suffix="a")
write_trial(16, "mistakes", [
    dict(wrong="Learn me English.", right="Teach me English.", note=f"یاد دادن teach، یاد گرفتن learn", emoji="books"),
    dict(wrong="I gave my exam.", right="I took my exam.", note=f"«امتحان دادم» میشه took", emoji="memo"),
    dict(wrong="Rain is coming.", right="It's raining.", note=f"«بارون میاد» میشه It's raining", emoji="cloud_with_rain"),
], (f"اینا رو کلمه به کلمه از فارسی ترجمه نکن ❌", f"برای دوستت بفرست که اونم بدونه 👇"), suffix="b")

# day 17
write_trial(17, "vocab", [
    dict(wrong="very ugly", right="hideous", note="یعنی «خیلی زشت»", emoji="ogre"),
    dict(wrong="very strong", right="powerful", note="یعنی «خیلی قوی»", emoji="flexed_biceps"),
    dict(wrong="very boring", right="tedious", note=f"یعنی «خیلی خسته{ZW}کننده»", emoji="sleeping_face"),
    dict(wrong="very fast", right="rapid", note="یعنی «خیلی سریع»", emoji="high_voltage"),
], ("دیگه نگو very fast یا very boring ❌", f"این کلمه{ZW}ها رو یاد بگیر و سیو کن 📌"), suffix="a")
write_trial(17, "mistakes", [
    dict(wrong="I make my homework.", right="I do my homework.", note=f"برای تکلیف do می{ZW}گن، نه make", emoji="pencil"),
    dict(wrong="I eat medicine.", right="I take medicine.", note=f"دارو رو take می{ZW}کنن، نه eat", emoji="pill"),
    dict(wrong="Did you ate?", right="Did you eat?", note="بعد از did فعل ساده میاد", emoji="fork_and_knife_with_plate"),
], (f"این ۳ تا جمله رو اشتباه نگو ❌", f"برای کسی که همیشه این{ZW}جوری می{ZW}گه بفرست 😅"), suffix="b")

# day 18
write_trial(18, "vocab", [
    dict(wrong="No problem.", right="No worries!", note="یعنی «اشکالی نداره»", emoji="ok_hand"),
    dict(wrong="Of course.", right="Absolutely!", note="یعنی «حتماً، صد در صد»", emoji="thumbs_up"),
    dict(wrong="I'm sorry.", right="My bad!", note="یعنی «تقصیر من بود» (خودمونی)", emoji="face_with_hand_over_mouth"),
    dict(wrong="Very good!", right="Awesome!", note="یعنی «عالیه!»", emoji="star-struck"),
], (f"این{ZW}جوری بگی، خیلی خودمونی{ZW}تر به نظر میای 😎", "برای دوستت بفرست 👇"), suffix="a")
write_trial(18, "mistakes", [
    dict(wrong="We discussed about it.", right="We discussed it.", note="بعد از discuss حرف about نمیاد", emoji="speech_balloon"),
    dict(wrong="I listen music.", right="I listen to music.", note="بعد از listen حرف to لازمه", emoji="headphone"),
    dict(wrong="Enter to the room.", right="Enter the room.", note="بعد از enter حرف to نمیاد", emoji="door"),
], (f"۳ تا اشتباه که تقریباً همه می{ZW}کنن 😬", "سیو کن و برای دوستت بفرست 👇"), suffix="b")
