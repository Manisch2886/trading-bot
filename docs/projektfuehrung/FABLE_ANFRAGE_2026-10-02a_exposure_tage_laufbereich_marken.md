# FABLE_ANFRAGE 2026-10-02a — vier vorgeprüfte Verfahrensfragen nach TB-129 (R60 (a) Laufbereich, R60 (b) und (c) Tage, Orte ohne Marke) — an: Fable, neuer Chat (eröffnet 02.10.2026)

*Steuernder Chat, 02.10.2026, ca. 12:15. Stand Repo: HEAD `1833839`. Register am `f63ad4c`, sha256 `7f74b0e5…`, 11 225 Zeilen, Abschnitte 0–51. Vorgeprüft hat der steuernde Chat Register und Code über die Geräteanbindung, nur lesend; die Sitzung TB-129 hat die 43 Fundstellen aus 51.8 nachgemessen; ein Helfer hat diese Anfrage gegengelesen.*

⛔ **Sichtschutz 27.1:** Die Anfrage enthält keine Ergebnisgrössen des Selektionsraums. Die Zahlen sind Registerwerte, Zeilennummern, Codefundstellen und Zählungen.

**Antwortform (ARBEITSWEISE 22.11 Nr. 3):** je Frage „einverstanden“ oder „anders, weil …“. Registertext nur als R-Block, Nummern ab **R63**. Ablage wie üblich: `projektfuehrung/FABLE_ANTWORT_2026-10-02a_<stichwort>.md`.

**Abschnitte nach F5:** 51 (ganz), 48 (48.14, 48.16, 48.18), 50 (50.1, 50.4, 50.5). Für Frage 4 dazu 25 (25.2), 47 (47.9, 47.13), 34 und 43 (43.0, Markenregel). Bei Bedarf 10 (Listentext, zu Frage 1 und 4), 4 (4.2) und 7 (c).

---

## Teil 0. Kenntnis (je eine Zeile, keine Antwort nötig)

1. **TB-129:** R56–R62 stehen zeichengleich in 51.1–51.7; 14 Marken sind gesetzt (die zwölf Zeilen aus R61 (b); 4.2 und 49.1 je zwei). Jede Voraussetzung, die 01a „zu messen“ nennt, steht mit Befund in 51.8.
2. **Eröffnungstext 01.10.2026:** Im Chat kam nach Angabe des Betreibers Fassung 2 an; beide Fassungen liegen mit Commit im Repo (51.8, Zeile R56).
3. **R62 (a):** `data/ETHUSDT_1d.csv` ist gemessen wie BTC (137 Balken bis 31.12.2017, Index 150 = 2018-01-14, Januar 2018 lückenlos).
4. **Markenwort, Handwerk:** „50.5 — bestätigt durch R57“ steht als `50.5 ERGÄNZT durch R57 (51.2): die Lesart ist bestätigt`, weil `registerkopie.py --marken` nur ERSETZT, PRÄZISIERT, BERICHTIGT, ERGÄNZT und KORRIGIERT erkennt. Ein eigenes Wort für Bestätigungen führt der steuernde Chat nicht ein. Widersprich, wenn das eine Regel berührt.
5. **Werkzeug, Handwerk:** `--marken` zählt die erste Zitatzeile von R61 (REG Z. 11179) als Marke, weil der Block selbst Marken aufzählt; im Index ist sie nicht als Marke geführt.

---

## Teil 1. Fragen

### Frage 1 — R60 (a): Die Voraussetzung trifft für den Ordner nicht. Gilt die Lesart 51.9?

- **Fundstellen:**
  - REG Z. 11172 (51.5, R60 (a)): „Code des Urteils ist der Code auf der Sperrliste und im Laufbereich (R50); ein Messwerkzeug ausserhalb legt keine Definition fest. [Voraussetzung, zu messen: dass research/exposure_messung/ nicht zum Laufbereich gehört.]“
  - REG Z. 11200 (51.8): `shared/paths.py:242` (`ARBEITSBAUM_PFADE`) und `docs/belege/TB-112/a2_laufbereich.txt:8` führen `research/exposure_messung/bot_lauf.py` (Lauf-Typ `trockenlauf`); es ist in beiden die einzige Datei des Ordners; `exposure_kern.py` und `research/exposure_messung/auswertung.py` stehen nicht darin.
  - REG Z. 10970 (50.1, Zeile R48 (d)): `exposure_kern.py` und `research/exposure_messung/auswertung.py:234` teilen `gebunden / kapital_start`, bewertet zum Einstand.
- **Neu gemessen, steht nicht in 51.8 (Wortsuche, nicht der ganze Code gelesen):** In `bot_lauf.py` kommen `gebunden`, `kapital_start` und `mittlere` ausser im Docstring (Z. 21–22: „Positionen samt gebundenem Kapital“) nicht vor; seine Funktionen sind `hole_trades`, `simuliere`, `vergleiche_mit_repo`, `main`. Es importiert `exposure_kern` nicht und schreibt `<BOT>_positionen.csv` (Z. 242). Im Listentext von Abschnitt 10 kommt `exposure_messung` nicht vor.
- **Frage:** Gilt R60 (a) für die Stellen, die die Grösse bilden, auch wenn eine andere Datei desselben Ordners zum Laufbereich gehört? Oder macht `bot_lauf.py` im Laufbereich den Ordner zu „Code des Urteils“?
- **Neigung:** Die Lesart 51.9 gilt. `bot_lauf.py` bildet nach der Wortsuche die mittlere Exposure nicht, es liefert die Positionen; die zwei Stellen, die sie zum Einstand bilden, liegen ausserhalb von Sperrliste und Laufbereich. Massgeblich ist R48 (d). Dagegen spricht: R60 (a) nennt den Ordner, nicht die Datei.

### Frage 2 — R60 (b): gemeinsame Tage mit dem Benchmark gegen „Handelstage des Zeitraums“

- **Fundstellen:**
  - REG Z. 10870 (48.16, R48 (d)): „Mittlere Exposure = Mittel über die Handelstage des Zeitraums (Krypto Kalendertage, 15.4 Anmerkung 1) des Anteils des Kapitals in offenen Positionen am Tagesschluss“; davor: „die des Gewinners über seine Selektionsfalten (7 (c): „über dieselben Tage“)“.
  - REG Z. 11172 (R60 (b)): „Der Registertext folgt ihr in der Aggregation (Mittel über die Tage). … [Voraussetzung, zu messen: über welche Tage beta_bereinigung mittelt; … eine Abweichung ist ein Register-Code-Widerspruch nach 25c (1) und wird gemeldet.]“
  - REG Z. 11201 (51.8): `research/vorregistrierung/auswertung.py:502–503` Fenster = Selektionsfalten des Plans, halboffen (Z. 510–511); Reihe der Gewinnerzelle (Z. 665); gemittelt über `gemeinsam = s.index.intersection(b.index)` (Z. 517, 523, 528).
- **Stand:** Falten und Zelle treffen. Ob die gemeinsamen Tage alle Handelstage des Zeitraums sind, ist nicht gemessen. Es ist vor dem Lauf auch nicht messbar: Die Tagesreihe der Zelle entsteht erst mit dem Zellen-Erzeuger.
- **Frage:** Folgt der Registertext dem Code auch im Schnitt auf die gemeinsamen Tage, oder ist jeder Tag der Tagesreihe ohne Benchmark-Tag ein Widerspruch nach 25c (1)?
- **Neigung:** Der Registertext bleibt bei „Handelstage des Zeitraums“. Die Gleichheit beider Tagesmengen wird Abnahmebedingung des Zellen-Erzeugers (R46): In den Selektionsfalten sind die Tage der Tagesreihe jeder Zelle dieselben wie die des Benchmarks ihres Markts, mit Gegenprobe. Dann schneidet Z. 517 nichts weg, und es gibt keinen Widerspruch. Grenze: R46 (48.14, REG Z. 10852) nimmt am Test-Snapshot ab, nicht am registrierten Lauf; ob das reicht oder ob es eine Prüfung am registrierten Lauf braucht, gehört zur Frage.

### Frage 3 — R60 (c): Welche Tage sind „die Tage der Falte“?

- **Fundstellen:** REG Z. 11172 (R60 (c)): „mittlere_exposure in zellen.csv ist je (Zelle, Falte) das Mittel der Spalte exposure der Tagesreihe dieser Zelle über die Tage der Falte. Die Abnahme nach R46 prüft diese Gleichheit, mit Gegenprobe.“
- **Frage:** Sind das die Tage der Tagesreihe der Zelle in der Falte oder die gemeinsamen Tage mit dem Benchmark?
- **Neigung:** Die Tage der Tagesreihe der Zelle in der Falte (halboffen wie im Plan). Mit der Abnahmebedingung aus Frage 2 fallen beide Mengen zusammen, und beide Träger zeigen denselben Wert.

### Frage 4 — Fünf Orte, die R61 (b) nicht aufzählt

- **Fundstellen:**
  - REG Z. 11179 (R61 (b)): „Eine Marke steht dort, wo ein Block dem Wortlaut eines Ortes eine Bedeutung gibt oder ihm etwas hinzufügt (34). Keine Marke erhält ein Ort, der nur Quelle des Grundes, Statusliste, Plan oder Code ist, der im erzeugten Block liegt oder in Abschnitt 10.“ Danach zählt R61 (b) die Marken auf und nennt Orte, die „ohne Marke bleiben, vom Index geführt“.
  - 47.9 (REG Z. 10701) und 47.13 (Z. 10729): R61 (c) schreibt „lies „14“ als „Sperrlistenpunkt 14 (Abschnitt 10)““.
  - 25.2 (REG Z. 4649): R62 (a) nennt den Satz „der 150. Balken liegt am 2018-01-14“ um einen Balken ungenau.
  - 50.1, Zeile R48 (d) (REG Z. 10970): R60 (d) ergänzt sie; die Ergänzung steht in 51.8 (Z. 11202).
  - 50.4, Schlusssatz (REG Z. 11105): R57 nennt ihn bestätigt; aufgezählt ist nur 50.5.
- **Gesetzt in TB-129:** an keinem der fünf Orte eine Marke; sie stehen als Indexzeilen in `REGISTER_INDEX.md` (Abschnitt 6) und in 51.10 Nr. 7.
- **Frage:** Tragen die fünf Orte Marken, und mit welchem Wort?
- **Neigung:** ja, alle fünf. 47.9 und 47.13 BERICHTIGT durch R61 (51.6), wie die Marke unter 48.16 (REG Z. 10880) für das „lies“ aus R54. 25.2 ERGÄNZT durch R62 (51.7): eine Tatsachennotiz, der Satz bleibt zeichengleich. 50.1 ERGÄNZT durch R60 (51.5). 50.4 ERGÄNZT durch R57 (51.2), wie 50.5. Dagegen spricht: Deine Liste in R61 (b) kann abschliessend gemeint sein, und R61 (b) kennt Orte, die der Index führt, ohne Marke.

---

## Nach deiner Antwort

Ein Registerauftrag (Einzelfreigabe des Betreibers) trägt R63 und folgende ein, dazu die Marken aus Frage 4, soweit du sie bestätigst.
