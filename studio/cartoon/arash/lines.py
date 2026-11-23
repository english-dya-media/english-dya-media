# Lines of this series: (id, part, scene, speaker, display_en, fa, tts_text or None)
# ids: p<part>s<scene><letter>, e.g. "p1s2a". tts_text only when the voice needs a respelling of names.
LINES = [
 # ---- part 1 · The Siege (Biruni, al-Athar al-Baqiya, Tirgan: Afrasiab besieges Manuchehr in Tabaristan; peace for one arrow's flight)
 ("p1s1a",1,1,"NARRATOR","This is the arrow that drew a border…","این تیری است که یک مرز را کشید…","This is the arrow, that drew a border..."),
 ("p1s1b",1,1,"NARRATOR","…and this is the story of the man who shot it.","…و این داستانِ مردی است که آن را رها کرد.",
  "and this is the story, of the man who shot it."),
 ("p1s3a",1,3,"NARRATOR","Long ago, Iran and Turan fought a long, hard war.","روزگاری دور، ایران و توران جنگی دراز و سخت داشتند.",
  "Long ago, Eeraan and Tooraan fought a long, hard war."),
 ("p1s3b",1,3,"NARRATOR","Afrasiab, the king of Turan, surrounded King Manuchehr…","افراسیاب، شاهِ توران، منوچهر شاه را محاصره کرد…",
  "Afraaseeyaab, the king of Tooraan, surrounded King Manoochehr..."),
 ("p1s3c",1,3,"NARRATOR","…in the green mountains of Tabaristan.","…در کوه‌های سبزِ تبرستان.","in the green mountains of Tabarestaan."),
 ("p1s3d",1,3,"NARRATOR","Months went by. There was no more bread in the fortress.","ماه‌ها گذشت. دیگر در دژ نانی نمانده بود.",None),
 ("p1s3e",1,3,"BOY","Mother, I'm hungry.","مادر، گرسنه‌ام.",None),
 ("p1s3f",1,3,"MOTHER","I know, my son. Be patient.","می‌دانم، پسرم. صبر کن.",None),
 ("p1s4d",1,4,"MANUCHEHR","Look… their fires are everywhere.","ببین… آتش‌هایشان همه‌جا هست.","Look... their fires are everywhere."),
 ("p1s4a",1,4,"MANUCHEHR","My people are hungry… and my soldiers are tired.","مردمم گرسنه‌اند… و سربازانم خسته.",
  "My people are hungry... and my soldiers are tired."),
 ("p1s4b",1,4,"GENERAL","Then ask for peace, my king. His men are tired too.","پس صلح بخواه، سرورم. سربازانِ او هم خسته‌اند.",None),
 ("p1s4c",1,4,"MANUCHEHR","Send a messenger to Afrasiab.","پیکی نزدِ افراسیاب بفرست.","Send a messenger to Afraaseeyaab."),
 ("p1s5g",1,5,"TURAN_SOLDIER","So many years in these cold mountains… I want to go home.","این همه سال در این کوه‌های سرد… می‌خواهم به خانه برگردم.",
  "So many years in these cold mountains... I want to go home."),
 ("p1s5a",1,5,"MESSENGER","Great king, King Manuchehr asks for peace.","شاهِ بزرگ، منوچهر شاه صلح می‌خواهد.",
  "Great king, King Manoochehr asks for peace."),
 ("p1s5b",1,5,"AFRASIAB","Peace? Ha! Now that he is hungry, he wants peace!","صلح؟ ها! حالا که گرسنه است، صلح می‌خواهد!",None),
 ("p1s5h",1,5,"ADVISOR","My king, our men are tired too. They want to go home.","سرورم، سربازانِ ما هم خسته‌اند. می‌خواهند به خانه برگردند.",None),
 ("p1s5c",1,5,"AFRASIAB","Very well. Tell your king to shoot one arrow.","باشد. به شاهت بگو یک تیر بیندازد.",None),
 ("p1s5d",1,5,"AFRASIAB","Where it falls, there will be the border.","هرجا افتاد، همان‌جا مرز است.",None),
 ("p1s5e",1,5,"AFRASIAB","Before it, Iran. After it, Turan.","این سویش ایران، آن سویش توران.","Before it, Eeraan. After it, Tooraan."),
 ("p1s5f",1,5,"AFRASIAB","One arrow! How far can one arrow fly?","یک تیر! یک تیر تا کجا می‌تواند برود؟",None),
 ("p1s6a",1,6,"MANUCHEHR","One arrow… for all of Iran.","یک تیر… برای همه‌ی ایران.","One arrow... for all of Eeraan."),
 ("p1s6b",1,6,"MANUCHEHR","Who can shoot that arrow?","چه کسی می‌تواند آن تیر را بیندازد؟",None),
 ("p1s6e",1,6,"SOLDIER_W","No one can shoot that far…","هیچ‌کس نمی‌تواند تیری به آن دوری بیندازد…","No one can shoot that far..."),
 ("p1s6c",1,6,"ARASH","I can, my king.","من می‌توانم، سرورم.",None),
 ("p1s6g",1,6,"MANUCHEHR","This arrow must fly farther than any arrow ever flew.","این تیر باید از هر تیری که تا امروز رها شده دورتر برود.",None),
 ("p1s6h",1,6,"ARASH","I know, my king.","می‌دانم، سرورم.",None),
 ("p1s6d",1,6,"NARRATOR","His name was Arash.","نامش آرش بود.","His name was, Aarash."),
 ("p1s6f",1,6,"NARRATOR","And he knew what this arrow would cost him.","و می‌دانست این تیر برایش چه بهایی دارد.",None),
 # ---- part 2 · The Bow (Biruni: Spandarmad tells how the bow and arrow must be made; Arash shows himself to both armies before the shot)
 ("p2s1a",2,1,"NARRATOR","To shoot that arrow, Iran needed a bow like no other…","برای انداختنِ آن تیر، ایران کمانی بی‌همتا لازم داشت…",
  "To shoot that arrow, Eeraan needed a bow, like no other..."),
 ("p2s1b",2,1,"NARRATOR","…and a man like no other.","…و مردی بی‌همتا.","and a man, like no other."),
 ("p2s3a",2,3,"NARRATOR","That night, King Manuchehr could not sleep.","آن شب، منوچهر شاه خوابش نمی‌برد.","That night, King Manoochehr could not sleep."),
 ("p2s3b",2,3,"MANUCHEHR","No bow in Iran can shoot that far…","هیچ کمانی در ایران تیری به آن دوری نمی‌اندازد…","No bow in Eeraan can shoot that far..."),
 ("p2s3c",2,3,"MANUCHEHR","Who is there?","چه کسی آن‌جاست؟",None),
 ("p2s3d",2,3,"SPANDARMAD","Do not be afraid, King of Iran.","نترس، شاهِ ایران.","Do not be afraid, King of Eeraan."),
 ("p2s3e",2,3,"SPANDARMAD","I am Spandarmad, the guardian of this earth.","من سپندارمذم، نگهبانِ این زمین.","I am Spandaarmad, the guardian of this earth."),
 ("p2s3f",2,3,"SPANDARMAD","Cut wood from the oldest tree in the forest.","از کهن‌ترین درختِ جنگل چوب ببُرید.",None),
 ("p2s3g",2,3,"SPANDARMAD","Take feathers from the wing of an eagle.","از بالِ عقاب پَر بگیرید.",None),
 ("p2s3h",2,3,"SPANDARMAD","And make the point from the finest iron.","و نوکِ تیر را از بهترین آهن بسازید.",None),
 ("p2s3i",2,3,"MANUCHEHR","And who will shoot it?","و چه کسی آن را می‌اندازد؟",None),
 ("p2s3j",2,3,"SPANDARMAD","He has already stepped forward.","او خودش پا پیش گذاشته است.",None),
 ("p2s4a",2,4,"NARRATOR","For days and nights, the best craftsmen of Iran worked.","روزها و شب‌ها، بهترین استادکارانِ ایران کار کردند.",
  "For days and nights, the best craftsmen of Eeraan worked."),
 ("p2s4b",2,4,"BOWYER","This tree is older than any king.","این درخت از هر پادشاهی پیرتر است.",None),
 ("p2s4c",2,4,"SMITH","The finest iron… for one arrow.","بهترین آهن… برای یک تیر.","The finest iron... for one arrow."),
 ("p2s4d",2,4,"BOWYER","It is ready. But who can draw a bow like this?","آماده است. اما چه کسی می‌تواند چنین کمانی را بکشد؟",None),
 ("p2s5a",2,5,"MANUCHEHR","Arash. This bow is yours.","آرش. این کمان مالِ توست.","Aarash. This bow is yours."),
 ("p2s5b",2,5,"MANUCHEHR","You know what this shot will cost you.","می‌دانی این تیر برایت چه بهایی دارد.",None),
 ("p2s5c",2,5,"ARASH","I have seen the children in our streets, my king.","من بچه‌های کوچه‌هایمان را دیده‌ام، سرورم.",None),
 ("p2s5d",2,5,"ARASH","They are hungry. And I am an archer.","آن‌ها گرسنه‌اند. و من کمان‌دارم.",None),
 ("p2s5e",2,5,"MANUCHEHR","Iran will never forget your name.","ایران هرگز نامت را فراموش نمی‌کند.","Eeraan will never forget your name."),
 ("p2s6a",2,6,"ARASH_MOTHER","Arash… is it true?","آرش… راست است؟","Aarash... is it true?"),
 ("p2s6b",2,6,"ARASH","It is true, Mother. At sunrise.","راست است، مادر. سپیده‌دم.",None),
 ("p2s6c",2,6,"ARASH_MOTHER","My son… you were always brave.","پسرم… تو همیشه شجاع بودی.","My son... you were always brave."),
 ("p2s6d",2,6,"ARASH_MOTHER","Go. And let your arrow fly far.","برو. و بگذار تیرت تا دوردست‌ها برود.",None),
 ("p2s7a",2,7,"NARRATOR","Before dawn, Arash climbed the mountain.","پیش از سپیده، آرش از کوه بالا رفت.","Before dawn, Aarash climbed the mountain."),
 ("p2s7b",2,7,"NARRATOR","Below, both armies waited.","پایینِ کوه، هر دو سپاه منتظر ماندند.",None),
 ("p2s7c",2,7,"WITNESS_A","Look. A light, near the top.","نگاه کن. یک روشنایی، نزدیکِ قله.","Look. A light, near the top."),
 ("p2s7d",2,7,"WITNESS_B","Let him climb. It is only one arrow.","بگذار بالا برود. فقط یک تیر است.",None),
 ("p2s7e",2,7,"BOY","Mother, will Arash come back?","مادر، آرش برمی‌گردد؟","Mother, will Aarash come back?"),
 ("p2s7f",2,7,"MOTHER","Watch the mountain, my son.","به کوه نگاه کن، پسرم.",None),
 ("p2s8a",2,8,"ARASH","People of Iran! People of Turan!","ای مردمِ ایران! ای مردمِ توران!","People of Eeraan! People of Tooraan!"),
 ("p2s8b",2,8,"ARASH","Look at me. I am healthy and strong.","به من نگاه کنید. تنم سالم و نیرومند است.",None),
 ("p2s8c",2,8,"ARASH","After this shot… I will not be.","پس از این تیر… دیگر نخواهم بود.","After this shot... I will not be."),
]
# speaker -> (libritts speaker id, length_scale, semitone shift, volume). The narrator is the same in every series.
# Pick ids that fit each role and differ from the other roles of the same part; "_W" roles are whispers.
VOICES = {
 "NARRATOR": (90, 1.12, 0, 1.0),
 # part 1 (720 ≈ 95 Hz, slow and deep: the tired king; 640 two semitones down: Afrasiab, quick and mocking; 360 ≈ 122 Hz: the general;
 # 550: the young messenger; 300 one semitone down, gentle and warm: Arash; 75: the mother; 765 four semitones up: the boy)
 "MANUCHEHR": (720, 1.1, 0, 1.0), "AFRASIAB": (640, 1.2, -2, 1.0), "GENERAL": (360, 1.15, 0, 1.0), "MESSENGER": (550, 1.05, 1, 1.0),
 "ARASH": (300, 1.1, -1, 1.0), "MOTHER": (75, 1.05, 0, 1.0), "BOY": (765, 1.0, 4, 1.0),
 # (350 one semitone down: a tired soldier of Turan; 680 one semitone down, an old warm voice: Afrasiab's advisor; 400 whispering: a soldier of Iran)
 "TURAN_SOLDIER": (350, 1.1, -1, 1.0), "ADVISOR": (680, 1.12, -1, 1.0), "SOLDIER_W": (400, 1.25, 0, 0.7),
 # part 2 (880 ≈ 179 Hz, soft, with an echo (FX): Spandarmad; 200 ≈ 112 Hz, quiet and old: the bowyer; 380 ≈ 89 Hz, deep: the smith;
 # 260 ≈ 176 Hz, a low warm woman: Arash's mother; 660 two semitones down and 270, quick: the two witnesses of Turan)
 "SPANDARMAD": (880, 1.15, 0, 0.9), "BOWYER": (200, 1.1, -1, 1.0), "SMITH": (380, 1.05, 0, 1.0), "ARASH_MOTHER": (260, 1.08, 0, 0.9),
 "WITNESS_A": (660, 1.05, -2, 1.0), "WITNESS_B": (270, 1.05, 0, 1.0),
}
# slower takes for learners (per-line length factors, see voices.py)
SPEED = {lid: 1.15 for lid, part, *_ in LINES if part == 1}
SPEED.update({"p1s1a": 1.5, "p1s1b": 1.3, "p1s3c": 1.4, "p1s3d": 1.35, "p1s3e": 1.4, "p1s3f": 1.3, "p1s4a": 1.2, "p1s4b": 1.35, "p1s5c": 1.4,
              "p1s5d": 1.45, "p1s5e": 1.3, "p1s5f": 1.25, "p1s6a": 1.3, "p1s6b": 1.3, "p1s6c": 1.35, "p1s6d": 1.3,
              "p1s4d": 1.3, "p1s5g": 1.5, "p1s5h": 1.2, "p1s6e": 1.3, "p1s6f": 1.45, "p1s6g": 1.3, "p1s6h": 1.55})
# per-line ffmpeg filters (voices.py)
FX = {lid: "atempo=0.88" for lid in ("p1s5c", "p1s5d", "p1s5e", "p1s5f")}
FX.update({"p1s4b": "atempo=0.9"})
# part 2
SPEED.update({lid: 1.15 for lid, part, *_ in LINES if part == 2})
SPEED.update({"p2s1a": 1.35, "p2s1b": 1.35, "p2s3a": 1.3, "p2s3b": 1.3, "p2s3c": 1.3, "p2s3d": 1.35, "p2s3e": 1.3, "p2s3f": 1.4,
              "p2s3g": 1.5, "p2s3h": 1.45, "p2s3i": 1.5, "p2s3j": 1.45, "p2s4a": 1.25, "p2s4b": 1.45, "p2s4c": 1.5, "p2s4d": 1.5,
              "p2s5a": 1.3, "p2s5b": 1.35, "p2s5c": 1.5, "p2s5d": 1.45, "p2s5e": 1.35, "p2s6a": 1.5, "p2s6b": 1.3, "p2s6c": 1.5, "p2s6d": 1.4,
              "p2s7a": 1.3, "p2s7b": 1.45, "p2s7c": 1.35, "p2s7d": 1.25, "p2s7e": 1.3, "p2s7f": 1.35, "p2s8a": 1.2, "p2s8b": 1.5, "p2s8c": 1.55})
FX.update({lid: "aecho=0.8:0.6:70|140:0.22|0.12" for lid in ("p2s3d", "p2s3e", "p2s3f", "p2s3g", "p2s3h", "p2s3j")})
FX.update({lid: "atempo=0.92,aecho=0.8:0.6:70|140:0.22|0.12" for lid in ("p2s3g", "p2s3h")})
FX.update({"p2s4d": "atempo=0.9", "p2s5c": "atempo=0.88", "p2s6c": "atempo=0.9", "p2s8c": "atempo=0.9", "p2s8a": "aecho=0.8:0.5:240:0.18"})
