# FABLE-Anfrage 17.10.d — R108 (d): Startkapital-Wert in 59.1; R108 (e): Prüfung am späten Symbol weicht ab

*Steuernder Chat, 17.10.2026, HEAD `6da15e0`. **Registerfrage**, zwei Befunde beim Bau zu R108 (TB-176, an einer Kopie gemessen, nichts gebaut). Dateien in der Projektablage unter projektfuehrung/.*

## Teil 0 — Kenntnis

Register `docs/VORREGISTRIERUNG_neuselektion.md`, Commit `3a00cf8` (= HEAD), 12 688 Zeilen, sha256 `8f464607b313cfe7…`, Abschnitte 0–67, eingetragen bis R107. R108 steht in FABLE_ANTWORT_2026-10-17c (noch nicht eingetragen; Abschnitt 68 mit TB-176a). Dein Block beginnt bei **R109**.

## Frage (a) — R108 (d): nennt 59.1 einen Wert?

R108 (d): „einen Wert nennt das Register nach 29.2 nicht. [Voraussetzung, zu messen: dass am Stand 7fe6342 kein Abschnitt einen Wert für das Startkapital nennt; nennt einer ihn, ist er der Ort, und dieser Unterpunkt gilt für ihn.]“

Gemessen (Volltextsuche Startkapital / STARTING_CAPITAL / 10 000): 59.1 (Tatsachennotiz TB-162, zeichengleich aus ERGEBNIS_TB-162) nennt den Wert — 7fe6342 Z. 12167, HEAD Z. 12185: „auf dem einen durchgehenden Kapitalpfad je Bot (Startkapital 10 000, ohne Neustart, R36)“. Übrige Treffer ohne Wert (29.2 „0“, 29.3, 49.2, Z. 11486 es.STARTING_CAPITAL). Code: `STARTING_CAPITAL = 10_000.0` in allen neun `strategies/<bot>/equity_simulation.py` (gleich). Modul aus 38.5 = `shared/handelskosten.py` (1 445 B, Docstring „EIN Ort, zwei Konstanten“).

**Erschlossen:** 59.1 ist eine Messnotiz, die den Wert beschreibt, nicht festlegt; sie nennt weder Modul noch Konstante (37.5 (1)).

**Frage:** Gilt 59.1 als Wert im Sinn von 29.2 / 37.5, sodass die Voraussetzung nicht erfüllt ist? Wo steht dann der Ort — 59.1, das Modul aus 38.5 oder ein Registertext neu?

## Frage (b) — R108 (e): wie ist die Prüfung zu führen?

R108 (e): „derselbe späte Symbolfall, Lauf mit Schranke am Tag gegen Lauf ohne Schranke, Wachen nach R86 (d) und R87 (c) eingeschaltet, Ausgaben bytegleich, Zählzeile der von der Schranke entfernten Zeilen (0) … weicht die Prüfung ab, ist das ein Befund daran [R106 (c)] und kommt als Frage.“

Gemessen (Simulation an einer Kopie, Seeds aus TB-169 e_abnahme.txt, Modus „schranke_aus“ des Listen-Erzeugers, Wachen an; Bericht BAU176 Abschnitt 4):
- elliott_wave_stocks: 6/6, bytegleich, entfernt 0.
- t3_supertrend und elliott_wave: Lauf ohne Schranke endet mit 2 (Wache R87 (c)). Variante a (Wortlaut 3b): t3 an AAA (Einstieg 2021-05-18 vor Tag 2023-05-18). Variante b (nur CCC mit Tag): an CCC, Schranke entfernt t3 8, elliott_wave 2 CCC-Trades.
- CCC ist im Fall von TB-169 3b kein spätes Symbol: seine Daten beginnen vor dem Tag (2021-05-18 bzw. 2021-06-13).

**Erschlossen:** das ist die Schranke bei der Arbeit, kein Fehler im Code. **Offen:** ein Fall, dessen Daten erst am oder nach dem Tag beginnen (nicht gemessen).

**Frage:** Wie ist die Prüfung nach R108 (e) zu führen — welcher späte Symbolfall gilt, und gilt die Wache nach R87 (c) im Lauf ohne Schranke? Was folgt für R106 (c) und die Bedingung des Tags aus R105 (c) für t3_supertrend?

## Lesen und Antwort

Projektablage: REGISTER_INDEX.md; REGISTER_KOPIE_ABSCHNITT_29, _37, _38, _56, _59, _66, _67; FABLE_ANTWORT_2026-10-17c_sb1_festlegungen_sammler_t3_r44_startkapital_ort.md. Abschnitt 68 gibt es erst nach TB-176a. Fehlt eine Kopie, melde das. Nicht lesen: BACKLOG*, ergebnisse/, docs/belege/. Antwort höchstens 6 KB als projektfuehrung/FABLE_ANTWORT_2026-10-17d_<stichwort>.md: Kurz je Frage, Registerblock ab R109, Leseprotokoll nach R56 (b), Ampel.
