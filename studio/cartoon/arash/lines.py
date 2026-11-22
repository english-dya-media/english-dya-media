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
}
# slower takes for learners (per-line length factors, see voices.py)
SPEED = {lid: 1.15 for lid, part, *_ in LINES if part == 1}
SPEED.update({"p1s1a": 1.5, "p1s1b": 1.3, "p1s3c": 1.4, "p1s3d": 1.35, "p1s3e": 1.4, "p1s3f": 1.3, "p1s4a": 1.2, "p1s4b": 1.35, "p1s5c": 1.4,
              "p1s5d": 1.45, "p1s5e": 1.3, "p1s5f": 1.25, "p1s6a": 1.3, "p1s6b": 1.3, "p1s6c": 1.35, "p1s6d": 1.3,
              "p1s4d": 1.3, "p1s5g": 1.5, "p1s5h": 1.2, "p1s6e": 1.3, "p1s6f": 1.45, "p1s6g": 1.3, "p1s6h": 1.55})
# per-line ffmpeg filters (voices.py)
FX = {lid: "atempo=0.88" for lid in ("p1s5c", "p1s5d", "p1s5e", "p1s5f")}
FX.update({"p1s4b": "atempo=0.9"})
