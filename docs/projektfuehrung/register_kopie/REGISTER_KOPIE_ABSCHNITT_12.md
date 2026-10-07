# REGISTER-KOPIE Abschnitt 12 (von 0–55) — Register-Z. 1261–1337 — Commit ad1fc0d3e5397cec6eb75c5e62de3b1bb7868c24 — 2026-10-07 — Original sha256 ab97ae1e31da161bc1aebed6b00bb2ec6eec07f760c45c645b9801e6e916b9cd — KOPIE, nicht das Register

## 12. Der Vollständigkeitstest

**Ja — das Auswertungsskript liess sich fertig schreiben, ohne ein Ergebnis
gesehen zu haben.** Es läuft gegen erzeugte Beispieldaten mit frei
erfundenen Werten (`beispieldaten.py`), und `test_vorregistrierung.py` prüft
jede Regel einzeln am Ablauf: 150 Prüfungen, davon acht Mutationsproben.

Fertigschreiben hiess allerdings an **sieben** Stellen: eine Lesart
festlegen, wo die Festlegungen zwei zuliessen. Jede steht oben im Text; hier
die Liste, damit keine davon unbemerkt bleibt.

| # | Offene Stelle | Festgelegte Lesart | Abschnitt |
|---|---|---|---|
| 1 | Trägt `DD_Toleranz` ein Exposure-Argument? | Ja — sonst passt Festlegung 5 nicht zu Festlegung 4 | 4.2 |
| 2 | Zählt das Plateau-Mittel den Punkt selbst mit? | Ja | 6 |
| 3 | Zählt der Spitzentest den Punkt selbst mit? | Nein | 6 |
| 4 | Was ist eine Spitze, wenn das Nachbarmittel ≤ 0 ist? | `S(x) − M > 0,5·|M|`, total definiert | 6 |
| 5 | Muss der Gewinner zulässig sein, und was gilt bei (b)? | Ja; bei (b) Bericht des Gesamt-Gewinners mit Markierung | 7 |
| 6 | Gehen unzulässige Nachbarn ins Plateau-Mittel ein? | Ja — die Regel misst Glattheit, nicht Zulässigkeit | 6 |
| 7 | Wie wird Gleichstand aufgelöst? | Statistik, dann Zellenname — kein Zufall | 6 |

Zwei weitere Stellen betreffen **nicht** die Auswertung, sondern den Lauf,
und sind deshalb als Voraussetzung eingetragen statt als Lesart: die beiden
Bug-Fixes aus Abschnitt 11.

**Was die Vollständigkeit trägt, ist nicht die Länge dieses Dokuments,
sondern dass `auswertung.py` keinen Schalter hat.** Es gibt keine Option, die
eine Schwelle verschiebt, keine, die einen Bot ausnimmt, und keine, die eine
Kennzahl unterdrückt. Wo die Rohergebnisse den Vertrag verletzen, bricht es
ab — es füllt nichts auf und überspringt nichts.

> ⭐ **Mit welchem Wert es abbricht (43.1, 43-1, Fable 25d, TB-110,
> 26.09.2026):** `auswertung.py` hat zwei Ausgänge — 0, wenn es gerechnet und
> berichtet hat; **2**, wenn es nicht rechnen konnte (jeder Bruch des
> Datenvertrags). Einen Ausgang 1 hat es nicht; die Abbruchkriterien (a)–(d)
> sind Ergebnisse eines gelungenen Laufs. Wortlaut in **43.1, 43-1**. Heute
> endet `Abbruch` noch mit 1 (zwölf Stellen); die Umstellung kommt mit der
> nächsten planmässigen Öffnung von `auswertung.py`. Der Satz oben bleibt
> zeichengleich.

> ⭐ **Ergänzung (40.7, Fable 24a, TB-96, 24.09.2026) — jede Mutationsprobe
> hat eine Gegenprobe**, die zeigt, dass sie rot werden kann; eine
> Mutationsprobe ohne Gegenprobe zählt nicht als Prüfung. Vor dem Tag wird
> die Gegenprobe für alle acht einmal geführt und als Tatsachennotiz
> festgehalten (TB-97). Anlass: `F4` hat mit `<=` statt `<` drei Wochen
> „bestanden", ohne je gemessen zu haben. Wortlaut in **40.7**. Die Zahlen
> oben („150 Prüfungen, davon acht Mutationsproben") bleiben zeichengleich;
> der Test zählt heute 165 Prüfungen (40.1).

> ⭐⭐ **Berichtigung und zwei Regeln (41.1 A1, A4, A5, A7, Fable 24b, TB-108,
> 25.09.2026):** „davon acht Mutationsproben" lies nach Fables Berichtigung
> „davon **sieben Mutationsproben, H1 bis H7** (Teil H)"; H0 ist der Grundlauf,
> F4 keine Mutationsprobe. Die **Namen** sind Registertext, die Zahl der
> Prüfungen eine Tatsachennotiz mit Stand (heute 196, 41.1 A1). Jede
> Mutationsprobe beisst **allein** (41.1, A4) — ⚠️ H6 tut es bis heute nicht,
> vor dem Tag offen. Störproben werden in **beide** Richtungen geführt (41.1,
> A5). Der Testrahmen (`beispieldaten.py`) deckt seit 24c beide Faltenlängen ab
> (41.1, A7). Die Sätze oben bleiben zeichengleich.

> ⭐ **Herkunftsprüfung in `auswertung.py`: siehe 46.5, Lesart 46.9** (Fable
> 27a R14, TB-117, 26.09.2026). Die Sätze und die Marken oben bleiben
> zeichengleich.

> ⭐ **Abschnitt 12 ERGÄNZT durch R25 (47.8)** (Fable 27c R25, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **Abschnitt 12 ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **Abschnitt 12 ERGÄNZT durch R49 (48.17)** (Fable 29b R49, Unterpunkt (d), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **Abschnitt 12 ERGÄNZT durch R50 (48.18)** (Fable 29b R50, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

---

