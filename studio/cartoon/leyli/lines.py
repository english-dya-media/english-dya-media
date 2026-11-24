# Lines of this series: (id, part, scene, speaker, display_en, fa, tts_text or None)
# ids: p<part>s<scene><letter>, e.g. "p1s2a". tts_text only when the voice needs a respelling of names.
# Names for the voice: Qays "Kayss", Leyli "Laylee", Majnun "Majnoon", Banu Amir "Banoo Aamir".
LINES = [
 # ---- part 1 · The School (Nizami: Qays, the son of the chief of the Banu Amir, and Leyli at the same school; the talk of the tribes;
 # Leyli is kept at home; Qays walks among the tents calling her name and the boys call him Majnun)
 ("p1s1a",1,1,"NARRATOR","Every day, he wrote one name in the sand…","هر روز، یک نام را روی شن می‌نوشت…","Every day, he wrote one name in the sand..."),
 ("p1s1b",1,1,"NARRATOR","…and every day, the wind took it away.","…و هر روز، باد آن را با خود می‌برد.","and every day, the wind took it away."),
 ("p1s3a",1,3,"NARRATOR","Long ago, in the deserts of Arabia, lived a tribe called the Banu Amir.",
  "روزگاری دور، در بیابان‌های عربستان، قبیله‌ای به نامِ بنی‌عامر زندگی می‌کرد.",
  "Long ago, in the deserts of Arabia, lived a tribe called the Banoo Aamir."),
 ("p1s3b",1,3,"NARRATOR","Their chief had gold, camels… and one son.","رئیسِ قبیله طلا داشت، شتر داشت… و یک پسر.",
  "Their chief had gold, camels... and one son."),
 ("p1s3c",1,3,"NARRATOR","Before the world called him Majnun, his name was Qays.","پیش از آن‌که دنیا او را مجنون بنامد، نامش قیس بود.",
  "Before the world called him Majnoon, his name was Kayss."),
 ("p1s3d",1,3,"CHIEF","Qays, my son. Today you go to school.","قیس، پسرم. امروز به مکتب می‌روی.","Kayss, my son. Today you go to school."),
 ("p1s3e",1,3,"QAYS","Will there be other children, Father?","بچه‌های دیگر هم آن‌جا هستند، پدر؟",None),
 ("p1s3f",1,3,"CHIEF","Many children, from many tribes. Learn well!","بچه‌های زیادی، از قبیله‌های زیاد. خوب درس بخوان!",None),
 ("p1s4a",1,4,"NARRATOR","Among the children was a girl from another tribe.","میانِ بچه‌ها دختری از قبیله‌ای دیگر بود.",None),
 ("p1s4b",1,4,"NARRATOR","Her name was Leyli.","نامش لیلی بود.","Her name was, Laylee."),
 ("p1s4c",1,4,"TEACHER","Children, repeat after me. Alif… ba… ta…","بچه‌ها، با من تکرار کنید. الف… ب… ت…",
  "Children, repeat after me. Aleef. Baa. Taa."),
 ("p1s4d",1,4,"CHILD_A","Alif… ba… ta…","الف… ب… ت…","Aleef. Baa. Taa."),
 ("p1s4d2",1,4,"CHILD_B","Alif… ba… ta…","الف… ب… ت…","Aleef. Baa. Taa."),
 ("p1s4d3",1,4,"CHILD_C","Alif… ba… ta…","الف… ب… ت…","Aleef. Baa. Taa."),
 ("p1s4e",1,4,"GIRL_W","Look! Qays is looking at Leyli again.","نگاه کن! قیس باز به لیلی نگاه می‌کند.","Look! Kayss is looking at Laylee again."),
 ("p1s4f",1,4,"BOY_W","And she is looking at him!","و لیلی هم به او نگاه می‌کند!",None),
 ("p1s4g",1,4,"TEACHER","Qays! What comes after ta?","قیس! بعد از «ت» چه می‌آید؟","Kayss! What comes after taa?"),
 ("p1s4h",1,4,"QAYS","…Leyli?","…لیلی؟","Laylee?"),
 ("p1s4i",1,4,"TEACHER","Everyone here is learning to read… except you two.","همه این‌جا خواندن یاد می‌گیرند… جز شما دو نفر.",
  "Everyone here is learning to read... except you two."),
 ("p1s4j",1,4,"NARRATOR","The other children learned letters. These two learned love.","بچه‌های دیگر الفبا یاد می‌گرفتند… و این دو، عشق را.",
  "The other children learned letters. These two, learned love."),
 ("p1s5a",1,5,"NARRATOR","But in the desert, words travel faster than the wind.","اما در بیابان، حرف از باد هم تندتر می‌رود.",None),
 ("p1s5b",1,5,"MOTHER","Leyli, people are talking about you and that boy, Qays.","لیلی، مردم درباره‌ی تو و آن پسر، قیس، حرف می‌زنند.",
  "Laylee, people are talking about you, and that boy, Kayss."),
 ("p1s5c",1,5,"LEYLI","But Mother, we have done nothing wrong.","ولی مادر، ما کارِ بدی نکرده‌ایم.",None),
 ("p1s5d",1,5,"LEYLI_FATHER","My daughter will not be the talk of the tribes.","دخترِ من نُقلِ زبانِ قبیله‌ها نمی‌شود.",None),
 ("p1s5e",1,5,"LEYLI_FATHER","From tomorrow, she stays at home.","از فردا، در خانه می‌ماند.",None),
 ("p1s6a",1,6,"QAYS","Where is Leyli?","لیلی کجاست؟","Where is Laylee?"),
 ("p1s6b",1,6,"TEACHER","She will not come anymore, my boy.","او دیگر نمی‌آید، پسرم.",None),
 ("p1s6c",1,6,"QAYS","Leyli! Leyli!","لیلی! لیلی!","Laylee! Laylee!"),
 ("p1s6d",1,6,"BOY_A","Look! Majnun! The madman!","نگاه کنید! مجنون! دیوانه!","Look! Majnoon! The madman!"),
 ("p1s6e",1,6,"BOY_B","Majnun! Majnun!","مجنون! مجنون!","Majnoon! Majnoon!"),
 ("p1s6f",1,6,"NARRATOR","From that day, no one called him Qays.","از آن روز، دیگر کسی او را قیس صدا نکرد.",
  "From that day, no one called him Kayss."),
 ("p1s6g",1,6,"NARRATOR","They called him Majnun… the one who is mad with love.","او را مجنون نامیدند… دیوانه‌ی عشق.",
  "They called him Majnoon... the one who is mad with love."),
]
# speaker -> (libritts speaker id, length_scale, semitone shift, volume). The narrator is the same in every series.
# Pick ids that fit each role and differ from the other roles of the same part; "_W" roles are whispers.
VOICES = {
 "NARRATOR": (90, 1.12, 0, 1.0),
 # part 1 (765 two semitones up: Qays as a boy; 849 ≈ 242 Hz, two semitones up, clear and gentle: Leyli as a girl; 680 one semitone
 # down, an old warm voice: Qays's father, the chief; 200, quiet and old, slowed: the teacher; 75: Leyli's mother; 500, cold and flat:
 # Leyli's father; 12 ≈ 242 Hz: a whispering girl; children: 12/519/550 two to five semitones up)
 "QAYS": (765, 1.08, 2, 1.0), "LEYLI": (849, 1.12, 2, 0.95), "CHIEF": (680, 1.12, -1, 1.0), "TEACHER": (200, 1.25, 0, 1.0),
 "MOTHER": (75, 1.05, 0, 1.0), "LEYLI_FATHER": (500, 1.2, 0, 1.0),
 "GIRL_W": (12, 1.2, 2, 0.7), "BOY_W": (519, 1.2, 5, 0.7),
 "CHILD_A": (12, 1.15, 2, 0.8), "CHILD_B": (519, 1.1, 5, 0.75), "CHILD_C": (550, 1.1, 4, 0.75),
 "BOY_A": (550, 1.0, 4, 1.0), "BOY_B": (519, 1.0, 5, 1.0),
}
# slower takes for learners (per-line length factors, see voices.py)
SPEED = {lid: 1.15 for lid, part, *_ in LINES if part == 1}
SPEED.update({"p1s1a": 1.3, "p1s1b": 1.3, "p1s3a": 1.2, "p1s3c": 1.25, "p1s4b": 1.3, "p1s4j": 1.3, "p1s5a": 1.25, "p1s6f": 1.25,
              "p1s6g": 1.35, "p1s4h": 1.5, "p1s6a": 1.5, "p1s6c": 1.4, "p1s3e": 1.35, "p1s3f": 1.0, "p1s4a": 1.3, "p1s4c": 1.2,
              "p1s4d": 1.3, "p1s4d2": 1.3, "p1s4d3": 1.3, "p1s4i": 1.4, "p1s5c": 1.25, "p1s5d": 1.5, "p1s6b": 1.55})
SPEED.update({"p1s1a": 1.45, "p1s6g": 1.5, "p1s3e": 1.5, "p1s4f": 1.4, "p1s4a": 1.45, "p1s5d": 1.7, "p1s4i": 1.6, "p1s3d": 1.3, "p1s5a": 1.35})
# per-line ffmpeg filters (voices.py): Qays calls across the camp
FX = {"p1s6c": "aecho=0.8:0.5:140:0.25"}
