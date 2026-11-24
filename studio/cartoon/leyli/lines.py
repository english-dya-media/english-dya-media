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
 # ---- part 2 · The Proposal (Nizami: the chief asks for Leyli's hand with rich gifts and is refused: "your son is mad, cure him first";
 # the Hajj: at the door of the Kaaba Majnun prays for more love, "take what is left of my life and add it to Leyli's"; Leyli's tribe gets
 # the ruler's leave to kill him, and his father hurries to warn him)
 ("p2s1a",2,1,"MAJNUN","God… take whatever is left of my life…","خدایا… هرچه از عمرم مانده بگیر…","God... take whatever is left of my life..."),
 ("p2s1b",2,1,"MAJNUN","…and give it to Leyli.","…و به عمرِ لیلی بیفزا.","and give it to Laylee."),
 ("p2s3a",2,3,"NARRATOR","Years went by. Qays grew up… but he never forgot Leyli.","سال‌ها گذشت. قیس بزرگ شد… اما لیلی را هرگز فراموش نکرد.",
  "Years went by. Kayss grew up... but he never forgot Laylee."),
 ("p2s3b",2,3,"NARRATOR","He walked the desert day and night, saying her name.","روز و شب در بیابان راه می‌رفت و نامش را می‌گفت.",None),
 ("p2s3c",2,3,"MAJNUN","Leyli… you are my night, and my moon.","لیلی… تو شبِ منی، و ماهِ من.","Laylee... you are my night, and my moon."),
 ("p2s3d",2,3,"ELDER","Your son is lost to the desert, my chief.","پسرت در بیابان گم شده، سرورم.",None),
 ("p2s3e",2,3,"CHIEF","Then I will go to Leyli's father and ask for her hand.","پس نزدِ پدرِ لیلی می‌روم و دستش را برای پسرم می‌خواهم.",
  "Then I will go to Laylee's father, and ask for her hand."),
 ("p2s3f",2,3,"ELDER","Take your best gifts. He is a proud man.","بهترین هدیه‌هایت را ببر. او مردِ مغروری است.",None),
 ("p2s4a",2,4,"NARRATOR","So the chief went to Leyli's tribe with camels, gold and silk.","پس رئیسِ قبیله با شتر و طلا و ابریشم به قبیله‌ی لیلی رفت.",
  "So the chief went to Laylee's tribe, with camels, gold, and silk."),
 ("p2s4b",2,4,"CHIEF","I have come to ask for your daughter… for my son, Qays.","آمده‌ام دخترت را بخواهم… برای پسرم، قیس.",
  "I have come to ask for your daughter... for my son, Kayss."),
 ("p2s4c",2,4,"LEYLI_FATHER","Your gifts are rich, and your name is great.","هدیه‌هایت گران‌بهاست و نامت بزرگ.",None),
 ("p2s4d",2,4,"LEYLI_FATHER","But your son is mad. The whole desert calls him Majnun.","اما پسرت دیوانه است. همه‌ی بیابان او را مجنون می‌نامند.",
  "But your son is mad. The whole desert calls him Majnoon."),
 ("p2s4e",2,4,"CHIEF","He is not mad. He is in love.","او دیوانه نیست. عاشق است.",None),
 ("p2s4f",2,4,"LEYLI_FATHER","Cure him first. Then we will talk.","اول درمانش کن. بعد حرف می‌زنیم.",None),
 ("p2s5a",2,5,"NARRATOR","The father had one last hope: the Kaaba, in Mecca.","پدر یک امیدِ دیگر داشت: کعبه، در مکه.",None),
 ("p2s5b",2,5,"CHIEF","My son, hold the door and pray: \"God, free me from this love.\"","پسرم، درِ کعبه را بگیر و دعا کن: «خدایا، مرا از این عشق رها کن.»",
  "My son, hold the door, and pray: God, free me from this love."),
 ("p2s5c",2,5,"MAJNUN","God, they tell me to ask You to free me from love…","خدایا، به من می‌گویند از تو بخواهم مرا از عشق رها کنی…",
  "God, they tell me, to ask You to free me from love..."),
 ("p2s5d",2,5,"MAJNUN","But I ask You: make my love even greater.","اما من از تو می‌خواهم: عشقم را بیشتر کن.","But I ask You: make my love, even greater."),
 ("p2s5f",2,5,"NARRATOR","His father heard… and knew there was no cure.","پدر شنید… و دانست که درمانی در کار نیست.","His father heard... and knew there was no cure."),
 ("p2s6a",2,6,"NARRATOR","But Majnun's words about Leyli reached every tent… and her tribe was angry.",
  "اما حرف‌های مجنون درباره‌ی لیلی به همه‌ی چادرها رسید… و قبیله‌ی لیلی خشمگین شد.",
  "But Majnoon's words about Laylee reached every tent... and her tribe was angry."),
 ("p2s6b",2,6,"KINSMAN","This madman says our daughter's name in every camp!","این دیوانه نامِ دخترِ ما را در همه‌ی اردوها می‌گوید!",None),
 ("p2s6c",2,6,"RULER","Then stop him… any way you can.","پس جلویش را بگیرید… هر طور که می‌توانید.","Then stop him... any way you can."),
 ("p2s6d",2,6,"MESSENGER","Chief! Leyli's tribe wants to kill your son!","سرورم! قبیله‌ی لیلی می‌خواهد پسرت را بکشد!","Chief! Laylee's tribe wants to kill your son!"),
 ("p2s6e",2,6,"CHIEF","Qays! I must find him before they do!","قیس! باید پیش از آن‌ها پیدایش کنم!","Kayss! I must find him, before they do!"),
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
 # part 2 (428 ≈ 142 Hz, soft and lively: Majnun as a young man; 720 ≈ 95 Hz, slow and deep: the old elder of the Banu Amir; 805, a noble
 # voice one semitone down: the ruler; 360 ≈ 122 Hz: Leyli's angry kinsman; 550 one semitone up: the messenger)
 "MAJNUN": (428, 1.15, 0, 1.0), "ELDER": (720, 1.12, 0, 1.0), "RULER": (805, 1.1, -1, 1.0), "KINSMAN": (360, 1.1, 0, 1.0),
 "MESSENGER": (550, 1.05, 1, 1.0),
}
# slower takes for learners (per-line length factors, see voices.py)
SPEED = {lid: 1.15 for lid, part, *_ in LINES if part == 1}
SPEED.update({"p1s1a": 1.3, "p1s1b": 1.3, "p1s3a": 1.2, "p1s3c": 1.25, "p1s4b": 1.3, "p1s4j": 1.3, "p1s5a": 1.25, "p1s6f": 1.25,
              "p1s6g": 1.35, "p1s4h": 1.5, "p1s6a": 1.5, "p1s6c": 1.4, "p1s3e": 1.35, "p1s3f": 1.0, "p1s4a": 1.3, "p1s4c": 1.2,
              "p1s4d": 1.3, "p1s4d2": 1.3, "p1s4d3": 1.3, "p1s4i": 1.4, "p1s5c": 1.25, "p1s5d": 1.5, "p1s6b": 1.55})
SPEED.update({"p1s1a": 1.45, "p1s6g": 1.5, "p1s3e": 1.5, "p1s4f": 1.4, "p1s4a": 1.45, "p1s5d": 1.7, "p1s4i": 1.6, "p1s3d": 1.3, "p1s5a": 1.35})
# per-line ffmpeg filters (voices.py): Qays calls across the camp
FX = {"p1s6c": "aecho=0.8:0.5:140:0.25"}
# part 2: slower takes; the prayer at the Kaaba has a soft echo
SPEED.update({lid: 1.2 for lid, part, *_ in LINES if part == 2})
SPEED.update({"p2s1a": 1.35, "p2s1b": 1.35, "p2s3c": 1.35, "p2s5c": 1.3, "p2s5d": 1.3, "p2s5f": 1.3, "p2s4e": 1.3, "p2s4f": 1.3})
SPEED.update({"p2s1a": 1.5, "p2s1b": 1.7, "p2s5c": 1.75, "p2s6b": 1.55, "p2s6c": 1.6, "p2s3f": 1.45, "p2s5b": 1.05, "p2s4b": 1.1})
FX.update({lid: "aecho=0.8:0.5:120:0.22" for lid in ("p2s1a", "p2s1b", "p2s5c", "p2s5d")})
