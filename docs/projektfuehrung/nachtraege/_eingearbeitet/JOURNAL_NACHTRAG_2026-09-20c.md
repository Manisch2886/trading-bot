# Journal-Nachtrag (c) — 20.09.2026, TB-61: die Benchmark-Tabelle für neun Bots, und drei Befunde, die keiner bestellt hat

**Quelle:** Mac-Sitzung **TB-61 Benchmark neun Bots**, 20.09.2026, 11:05 bis
etwa 12:00 UTC, `trading-env/bin/python3` 3.9.6, Ausgang `c493b1b`, Commits
`3c3e2c8`, `d1b2175`, `3d46a7b`, `b29f695` und der Abgabe-Commit.
Ergebnisdokument `docs/ERGEBNIS_TB-61_benchmark_neun.md`, Belege
`docs/belege/TB-61/`.

---

## Was der Auftrag wollte und was er bekam

Die Benchmark-Tabelle neu rechnen, **daneben**, für alle neun Bots. Das ist
geschehen: `benchmark_drawdowns_neu.json`, neunmal `endgueltig`, die gesperrte
Datei viermal nachgemessen unverändert (`a163c498…`). Die vier Vorhersagen aus
Register 21.6 treffen auf die Stelle, und drei Gegenproben bestätigen jede
Aktienzahl unabhängig — die 21.6-Zahlen stammten, anders als der Auftrag
annahm, aus **derselben** Rechnung.

**Und der Test bleibt rot.** `test_vorregistrierung.py:82` liest die gesperrte
Datei. Solange die Sperre gilt, kann ihn kein Lauf grün machen — der Auftrag
hatte das als *„erschlossen, nicht gemessen"* markiert und die Prüfung
verlangt. Gemessen: rot, aus genau dem Grund, den die Sperre erzwingt.

---

## Drei Befunde, und warum sie nicht im Auftrag standen

### 1. Der Krypto-Benchmark ist bis 2021 leer

`MINDESTTRAINING_JAHRE = 4` verlangt vier Jahre Kursgeschichte, bevor ein
Symbol point-in-time in eine Falte eingeht. Krypto-Daten beginnen 2017-08-17.
Folge: **die Falten 2018 bis 2021 haben null Symbole**, der Median der
DD_Toleranz läuft bei vier von fünf Krypto-Bots über vier Nullen und vier
echte Zahlen. Der Lauf brach daran zunächst mit `TypeError` ab (leere Reihe
ohne Zeitindex); die kleinste Wache, die ihn durchlässt, ist eingesetzt und im
Ergebnis als Abweichung von *„Nur der Schalter"* benannt.

⇒ ⭐⭐ **Der Auftrag führte den Vier-Jahres-Wert als „Befund zum Melden, nicht
zum Lösen" — und er ist ergebnisbestimmend.** *Eine Frage, die man vorab als
Nebensache einstuft, hat man noch nicht gemessen.* Die Meldepflicht war
richtig; die Einstufung „Nebensache" hat der Lauf widerlegt.

### 2. Register 21.3 (b) steht in keinem Code

*„Ergeben 4a und 3b (a) verschiedene erste Falten, bindet 3b (a)."* Das steht
seit TB-56b im Register. `plan_aktien()` rechnet nur 4a — bei Aktien fällt das
nicht auf, weil beide Lesarten dasselbe Jahr geben. Bei `t3_supertrend` nicht:
4a sagt 2018, 3b (a) sagt 2019 (Loader `MIN_HISTORY_DAYS = 730`), und die neue
Tabelle trägt 8 statt 7 Falten. Der Auftrag verlangte *„dieselbe Regel wie
`plan_aktien`"*; genau das erzeugt die Abweichung.

⇒ ⭐ **Eine Registerregel, die der Code nicht rechnet, gilt nur dort, wo sie
zufällig nichts ändert.** Das Register sagt, was der Code tun soll (21.8) — der
Code tut es nicht, und es ist erst heute aufgefallen, weil erstmals ein Bot
betroffen war.

### 3. Schritt 1 des Auftrags hätte zum Abbruch geführt — und der wäre falsch gewesen

*„Rechne `faltenplan_neun.py` und halte es gegen die Tabelle in Abschnitt 0;
stimmt es nicht, brich ab."* Das Werkzeug trägt auf der Platte noch die
Schranke 2019 (der Auftrag nennt sie selbst als eigene Aufgabe): mit Schranke
2/9 Treffer, ohne 8/9. Die Tabelle in Abschnitt 0 ist die 3b (a)-Tabelle aus
21.4; das Werkzeug rechnet 4a. Beide haben exakt den gemessenen Stand — der
Auftrag verglich zwei Lesarten und hätte die erwartbare Differenz als Befund
gelesen.

⇒ ⭐ **Eine Abbruchklausel nennt, wogegen sie prüft — und mit welcher Lesart.**
Hier half die Auflage *„Widersprich dem Auftrag, wo er falsch ist"*: nicht
abgebrochen, sondern beide Zählungen ausgewiesen und weitergemacht.

---

## Ein vierter, kleiner, aber mit Datum

In einer Wegwerf-Kopie mit der neuen Tabelle an der Stelle der gesperrten
läuft der Test durch: **163 bestanden, 2 gescheitert**, der `KeyError` ist dort
weg. Die zwei Roten sind neu: **G6** prüft `"2020" in namen and "2022" in
namen`, Doppeljahr-Falten heissen aber `2020-2021` und `2022-2023` — bis heute
erreichte kein Doppeljahr-Bot G6, weil Krypto Platzhalter war. **H3** setzt vier
Falten ohne Trade und erwartet einen verschobenen Median — gebaut für sieben
Falten; `turtle_soup_stocks` hat seit TB-56 neun, vier Nullen bewegen den Median
nicht mehr. **Nach dem Amendment wird der Test aus zwei neuen Gründen rot.** Wer
das Amendment vollzieht, repariert beides vorher.

⇒ *Ein Test, der seit Tagen aus einem bekannten Grund rot ist, versteckt jeden
neuen Grund dahinter.* Prüfprinzip A4 in Reinform — und der Grund, den Test in
der Kopie laufen zu lassen, statt auf das Amendment zu warten.

---

## Was aus dieser Sitzung an Regeln bleibt

| | Regel |
|---|---|
| ⭐⭐ | **Ein Wert, den ein Auftrag als „nur melden" einstuft, wird trotzdem am Ergebnis gemessen** — die Einstufung ist eine Vermutung, bis der Lauf sie bestätigt |
| ⭐ | **Registerregeln, die Code betreffen, bekommen eine Probe, die sie an einem Bot beisst, bei dem sie etwas ändern** — sonst ist ihre Umsetzung nicht prüfbar |
| ⭐ | **Eine Abbruchklausel nennt Instrument, Bezugstabelle und Lesart.** „Stimmt es nicht überein" ohne diese drei ist ein Abbruch auf Verdacht |
| | Nachweis 7 „pytest je Testdatei" war in `trading-env` nicht ausführbar (kein pytest, Skript mit `main()`); der Skriptstart ist der Weg, den TB-56 auch gegangen ist — gehört nach `UMGEBUNGEN.md` |

*Nachgetragen 20.09.2026 aus der Mac-Sitzung TB-61. Quellenvermerk: siehe Kopf.*
