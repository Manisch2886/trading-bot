# FABLE_ANFRAGE 2026-10-01a — sieben vorgeprüfte Verfahrensfragen nach E-2 (Anfangsbestand 27, Lesarten 50.5 und R48 (d), R53, Marken) — an: Fable, bestehender Chat (eröffnet 01.10.2026)

*Steuernder Chat, 01.10.2026, ca. 23:20. Stand Repo: HEAD `eeee21d`. Register am `db108a6`, sha256 `b5804659…`, 11 094 Zeilen. Vorgeprüft hat ein Helfer Register und Code, nur lesend; ein zweiter hat gegengelesen. „REG Z.“ sind Registerzeilen; die Abschnittsdatei nennt der Index. AW = `research/vorregistrierung/auswertung.py`.*

⛔ **Sichtschutz 27.1:** Die Anfrage enthält keine Ergebnisgrössen des Selektionsraums. Die Zahlen sind Registerwerte, Codekonstanten, Zeilennummern und Zählungen.

**Antwortform (ARBEITSWEISE 22.11 Nr. 3):** je Frage „einverstanden“ oder „anders, weil …“. Registertext nur als R-Block, Nummern ab **R56**. Ablage wie üblich: `projektfuehrung/FABLE_ANTWORT_2026-10-01a_<stichwort>.md`.

**Abschnitte nach F5:** 3, 25, 26, 27, 28, 32, 43, 47, 48, 49, 50. Für Frage 6 dazu die Markenzeilen in 1, 4, 5, 7, 9, 10, 11, 12, 15. Für Frage 7 bei Bedarf 6, 8, 16, 40, 41, 45.

---

## Teil 0. Kenntnis (je eine Zeile, keine Antwort nötig)

1. **R28, Nebenbefund:** `SOLL_DATENSTAND` in `research/registernachtrag_tb48/pruefe_abschnitt17.py:97` ist ein weiteres Literal des Datenstands ohne eigene Registerprobe. R28 nennt es nicht (REG Z. 10687, 10926). 50.7 Nr. 6 führt es als „Fable zur Kenntnis, dann Handwerk“.
2. **ERZEUGT-Block in Abschnitt 3:** `registerbericht.py --pruefen` meldet rc 1, schon vor TB-126. Das Register regelt den Fall (REG Z. 253–255; Z. 9635: Neuerzeugung mit dem Raster-Nachzug, 40.8 (h)). Keine Frage.

---

## Teil 1. Fragen

### Frage 1 — 27: Darf der Anfangsbestand eines neuen Chats durch Eröffnungstext und Leseprotokoll festgehalten werden statt durch einen R-Block je Chat?

- **Fundstellen:**
  - REG Z. 5117 (27.4): „Der Verfahrensprüfer führt in jeder Antwort ein Leseprotokoll (welche Dateien er in diesem Chat gelesen hat). Das Protokoll ist Selbstauskunft.“
  - REG Z. 5129–5133 (27.6): „Die Protokollkette beginnt nicht mit 21d, sondern mit der Tatsachennotiz oben.“
  - REG Z. 10720–10721 (47.15, R32): „Der Chat des Verfahrensprüfers wurde am 29.09.2026 neu begonnen; er kennt aus dem Vorgängerchat nichts. Sein Wissensstand ist: der Wortlaut von `FABLE_UEBERGABE_2026-09-29_neuer_chat.md`; …“
  - REG Z. 10886–10887 (R52 (c)): hält eine Verdichtung fest.
- **Anlass:** Betreiberentscheid 01.10.2026 (Tokensparen): Probe über zwei Anfragen mit einem Fable-Chat je Anfrage. Sie beginnt erst nach deiner Antwort. Bisher hält ein R-Block den Anfangsbestand eines neuen Chats fest (R32). Mit einem Chat je Anfrage wäre das ein R-Block je Anfrage.
- **Frage:** Darf der Anfangsbestand festgehalten werden durch (i) den Wortlaut des Eröffnungstextes, der mit Commit im Repo liegt, und (ii) das Leseprotokoll deiner ersten Antwort im Chat (27.4), ohne eigenen R-Block je Chat?
- **Neigung:** ja, unter zwei Bedingungen. Die Regel selbst steht einmal als R-Block im Register (Ergänzung zu 27.6). Ein eigener R-Block bleibt nötig, wenn ein Chat mehr weiss, als Eröffnung und Leseprotokoll nennen (Verdichtung wie R52 (c), Wissen aus einem Vorgänger). Dagegen spricht: 27.4 nennt das Leseprotokoll „Selbstauskunft“.
- **Dein jetziger Chat** hat noch keinen Eintrag. Bei „einverstanden“ trägt R56 die Regel; bei „anders“ trägt R56 die Tatsachennotiz zu diesem Chat nach Bauart R32.

### Frage 2 — 50.5: Zählt der Vorlauf nach R53 als L + 19 oder als L + 20?

- **Fundstellen:**
  - REG Z. 10897 (49.1, R53): „je Rückblick-Achse die oberste registrierte Stufe (Abschnitt 3) zuzüglich der festen Fenster des Bots (etwa Bollinger-Fenster, Donchian-Zusatz), gerechnet gegen den Horizontbeginn (28.6)“
  - REG Z. 11070–11072 (50.5): „Vorläufig, bis Fable bestätigt (Bauart 46.9).“ und „Wörtlich addiert ergäbe „oberste Stufe zuzüglich der festen Fenster“ bei den zwei Volatility-Breakout-Bots L + 20 (Bollinger-Fenster 20). Aus dem Code hergeleitet ist der erste Balken, an dem die Einstiegsbedingung einer Zelle definiert ist, `BB_PERIOD + L − 1`, also L + 19.“
  - REG Z. 11064–11066 (50.4): „Der Scanbeginn der Zelle liegt an ihrem Vorlauf (Fable 30a, R53): er ist der erste Index, an dem die Einstiegsbedingung der Zelle definiert ist — bei den Breakout-Bots `BB_PERIOD + L − 1`, nie früher, nicht später.“
- **Frage:** Liest R53 den Vorlauf als ersten definierten Index (L + 19) oder als Summe der Fensterlängen (L + 20)?
- **Neigung:** L + 19. Die zwei rollenden Fenster liegen hintereinander und teilen sich einen Balken (50.5). 50.4 setzt diese Lesart schon voraus. Ausserhalb von 50.4 und 50.5 hat die Vorprüfung keine Stelle gefunden, die das wörtlich entscheidet.

### Frage 3 — R48 (d): Lesart, wo der Code `mittlere_exposure` nicht bildet, und eine Stelle, die 50.1 nicht nennt

- **Fundstellen:**
  - REG Z. 10840 (48.16, R48 (d)): „[Voraussetzung, zu messen: Bildung von mittlere_exposure im Vertrag/auswertung.py und in mtm_kern.py; der Registertext folgt dem Code, wo er ihn hat.]“
  - REG Z. 10931 (50.1): „nicht gebildet: `auswertung.py:405` liest sie als Eingabe; `mtm_kern.py` führt keine Exposure“ und „An den drei Orten, die R48 (d) nennt, nicht gebildet; ausserhalb davon zum Einstand bewertet. **Lesart des steuernden Chats:** Wo der Code die Grösse nicht hat, gilt der Registertext“
- **Neu gemessen, steht nicht in 50.1:** In `beta_bereinigung` bildet AW:528 `exposure_mittel = float(np.mean(se))` aus der Tagesreihen-Spalte `exposure` (AW:523) und gibt den Wert unter dem Schlüssel `"mittlere_exposure"` zurück (AW:537). Wie die Spalte `exposure` selbst bewertet ist, ist damit nicht gemessen.
- **Frage (a):** Einverstanden mit der Lesart „wo der Code die Grösse nicht hat, gilt der Registertext“?
- **Frage (b):** Ist AW:528 eine „Bildung von mittlere_exposure in auswertung.py“ im Sinn von R48 (d)? Wenn ja, braucht die Zeile in 50.1 eine Berichtigung.
- **Neigung:** (a) ja. (b) ja; die Zeile in 50.1 ist dann unvollständig und wird als Tatsachennotiz berichtigt.

### Frage 4 — R53: Gilt „nicht als Literal“ ohne Rückfall auf „Literal mit Test nach 32.5 (c)“?

- **Fundstellen:**
  - REG Z. 10897 (R53): „Er wird aus registerdaten.py gerechnet, nicht als Voreinstellung geführt und nicht als Literal gesetzt; der Faltenplan trägt ihn je Bot als Feld.“
  - Deine Antwort 30a, Z. 17–18 („Unsicher“): „[Voraussetzung, zu messen: dass die oberste Stufe jeder Rückblick-Achse und die festen Fenster je Bot maschinell aus registerdaten.py lesbar sind; sonst Literal mit Test nach 32.5 (c).]“
  - REG Z. 5811 (32.5 (c)), Z. 10937 (50.1), Z. 11093 (50.7 Nr. 12).
- **Frage:** Gilt R53 ohne Rückfall, oder bleibt „Literal mit Test“ zulässig, wenn die Voraussetzung aus 30a für einen Bot nicht erfüllt ist?
- **Neigung:** ohne Rückfall. Der Rückfall steht nur unter „Unsicher“, nicht im R-Block. Für das Bollinger-Fenster ist die Voraussetzung erfüllt (`registerdaten.py:213–216`, Regel `bollinger_fenster`, Wert 20.0). Insgesamt misst 50.1 sie als „teilweise“ (REG Z. 10937): „Für weitere feste Fenster (`VOLUME_AVG_PERIOD`, fester Warm-up der Turtle-Soup-Bots) gibt es keinen Eintrag“. Nach meiner Neigung bekommt `registerdaten.py` diese Einträge (Handwerk mit R53 (a)), statt dass ein Literal gesetzt wird.

### Frage 5 — 25.3 (i): Präzisiert R53 die Fassung 26.2, oder steht R53 neben ihr?

- **Fundstellen:**
  - REG Z. 4649: „(i) „im registrierten Datenhorizont des Bots" PRÄZISIERT durch Abschnitt 26 (TB-77, 21.09.2026), 26.2 — der Wortlaut bleibt stehen.“
  - REG Z. 4651–4652: „4a (i) in 25.3 PRÄZISIERT durch R53 (49.1) (Fable 30a R53, TB-126, 01.10.2026).“
  - REG Z. 4860–4863 (26.2): „Der Datenhorizont eines Bots ist ein absolutes Datum je Bot“
  - Der R53-Block (REG Z. 10897–10898) nennt unter anderem 25.3, 28.6, 25.2, 15.5 und 21.4; „26.2“ kommt darin nicht vor.
- **Frage:** Wie verhalten sich die zwei Marken an Bedingung (i)?
- **Neigung:** R53 steht neben 26.2. 26.2 legt den Datenhorizont fest, R53 den Indikator-Vorlauf, gerechnet gegen den Horizontbeginn. Beide gelten; der Index führt beide Marken.

### Frage 6 — Marken: eine Marke je Ort, wo R51 und R48/R49/R50 denselben Ort nennen

- **Fundstellen:** REG Z. 10879 (48.19, R51): „3, Zahlenteil und 4.4 → 39.2 (Tabelle des Laufs), 40.8 (h), R49 (c) … 9 → R48 (b) … 11 → R49 (h) … 12 → R50. Kopf → R49 (f)“; REG Z. 10837 (R48 (a)): „Marke an Festlegung 4 (R51).“
- **Gesetzt in TB-126:** Acht Orte nennen beide Seiten (Festlegung 4, Abschnitt 9, 3 Zahlenteil, 4.4, 11, 12, Kopf, 10). Sieben tragen für diesen Verweis je eine Marke des Blocks R48/R49/R50, Abschnitt 10 steht als Indexzeile. Abschnitt 12 trägt daneben eine zweite Marke aus R49, Unterpunkt (d) (REG Z. 1303). Die R51-eigenen Orte tragen „ERGÄNZT (Verweis) durch R51 (48.19)“ (fünf Marken: REG Z. 80, 516, 688, 801, 1714).
- **Frage:** Einverstanden mit „eine Marke je Ort, keine Doppelung“?
- **Neigung:** ja.

### Frage 7 — Orte ohne Marke

- **Liste B (vier Einträge; der R-Block nennt einen Ort, den das Register nicht hat, oder keinen Bezugsort):**
  - R27 (47.10): „Ergänzung zu den Tag-Vorbedingungen“
  - R28 (47.11): „Tatsachennotiz zu … Plan-Punkt 6“ (der Plan steht nicht im Register)
  - R30 (47.13): wie R27
  - R48 (d), (e) (48.16): Lesarten ohne Bezugsort
- **Liste C (zehn Punkte; der Ort hat keine Bezugsform, trägt die Marke an anderer Stelle oder liegt ausserhalb des Registers):**
  - R21: 16.4, „#### Prüfung vor dem Tag“ (REG Z. 2200–2202, dort „3⁹“; R21 nennt 4⁹). Die R21-Marken stehen an 16.4 (b), (i), (j) (REG Z. 2076, 2159, 2162).
  - R36 (Festlegung 3, Abschnitt 8), R37 (7 (b)), R54 (7 (c), 8.1), R55
  - R33 (43-7), R52 (b) (45.5 (b))
  - R38 (16.11 Zeile 7)
  - R41 (41.2 B3)
  - R47 (5.4, gelesen als Teil von 40.6)
  - R48 (h) (im ERZEUGT-Block, dort steht nie eine Marke)
  - R49 (c) (40.8 (b)), R49 (e) (Abschnitt 6)
  - R31 (a), (e)
  - R39, R43, R25 (Code bzw. Plan, kein Registerort)
- **Frage:** Einverstanden, dass diese Orte ohne Marke bleiben und nur der Index sie führt? Wenn anders: je Eintrag Ort und Markenart als R-Block.
- **Neigung:** einverstanden für Liste B und Liste C, mit einer Ausnahme. Bei R21 neige ich zu einer Marke an REG Z. 2200, weil der Absatz den Wert „3⁹“ trägt, den R21 ändert.

---

## Nach deiner Antwort

Ein Registerauftrag (Einzelfreigabe des Betreibers) trägt R56 und folgende ein. Die Probe „ein Chat je Anfrage“ beginnt mit der nächsten Anfrage, wenn Frage 1 das zulässt.
