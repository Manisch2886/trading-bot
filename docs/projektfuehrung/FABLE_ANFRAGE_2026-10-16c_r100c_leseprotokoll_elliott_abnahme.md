# FABLE-Anfrage 16.10.c — R100 (c): Leseprotokoll TB-148 trifft Fundstellen aus R90 bis R92; Abnahme R90 (g)/R98 (d) bei den Elliott-Bots als Tatsachennotiz (Registerfrage)

*Steuernder Chat, 16.10.2026, Repo-Stand `eff5b5a`. Erste Anfrage im neuen Chat „Fable Trading Bots-16.10.2026 b“; Übergabe 16.10.c gilt. **Registerfrage.** Die genannten Dateien liegen in der Projektablage unter projektfuehrung/ (Projekt-Werkzeug, nicht der Ordner auf dem Mac). Zitate per Skript aus dem Register (Commit `3cbcdee`, 12 434 Zeilen, sha256 `f5510c4b…` = Stand HEAD).*

## Teil 0 — Kenntnis

1. Register 0–64, eingetragen bis R103 (62.4, Z. 12316). Dein Block hier beginnt bei **R104**.
2. Betreiberkarte 16.10.2026 („Mit nächster Anfrage“): der Befund zu R100 (c) geht mit dieser Anfrage.

## Frage 1 — Befund R100 (c) (belegt)

1. R100 (c), 62.1 Z. 12297: „berühren die Blöcke R90 bis R92 nur, wenn eine dort genannte Fundstelle in einer geänderten Zelle liegt.“ Voraussetzung: „[Voraussetzung, zu messen: dass keine in R90 (e), R91 (a) bis (c) und R92 (a) genannte Fundstelle in einer der geänderten Zellen liegt; sonst wird gemeldet.]“
2. Gemessen in TB-167 (62.5 Z. 12342): „geaenderte Zellen (bestehende Spalten) in d9f8489 (leseprotokoll.md): 38“. 62.5 (c), Z. 12353: „R100 (c): Fundstellen und geänderte Zeilen wie oben gemessen; Befund, zu melden:“ — 11 Einträge: die neun `strategies/<bot>/multi_symbol_optimise.py` (R92 (a), M2) je „Messpunkt M2 (auch M3, M4)→M2 (auch M4)“; „research/faltenplan_neun/faltenschranke_messung.py: Zeilenbereich 1–534 (ganz)→1–533 (ganz)“ (R90 (e), M5); „shared/zuteilung.py: Zeilenbereich 1–799 (ganz)→1–798 (ganz)“ (R91 (c), M1).
3. Erschlossen (Helfer BESTAND_E3B, nicht im Register): jede Änderung berichtigt die Endzeile einer ganz gelesenen Datei auf ihre Zeilenzahl oder streicht einen Neben-Messpunkt; keine Fundstelle fällt aus dem gelesenen Bereich, M2 bleibt. Zählweise: 38 geänderte Zellen in 32 Dateizeilen (BESTAND_E3B Z. 27 zählt Zeilen, 62.5 Zellen).

**Frage:** Was folgt nach R100 (c)? **Neigung:** Tatsachennotiz ohne Folge für R90 bis R92 (Berichtigungen der Zeilenzahl und eines Neben-Messpunkts, kein Inhalt) — oder anders, weil …

## Frage 2 — R90 (g)/R98 (d) bei elliott_wave und elliott_wave_stocks

1. R90 (g), 57.1 Z. 11997: „Kann der Fall der Verdrängung bei einem Bot nach seinem Scan nicht entstehen, sagt das eine Tatsachennotiz mit Fundstelle, und der Fall entfällt für diesen Bot.“
2. R98 (d), 61.1 Z. 12228: „(d) Abnahme. Die Prüfung nach R90 (g) läuft am Erzeuger: für den Zellen-Erzeuger in der Abnahme nach R46, für den Listen-Erzeuger in der Probe nach R86 (d), je auf dem Test-Snapshot, geprüft an den Ausgaben des Erzeugers, mit der Gegenprobe über die Wache nach R87 (c);“ und „Eine Prüfung unmittelbar am Signalpfad ist Handwerk daneben und ersetzt sie nicht.“
3. 64 Z. 12432: „Fall nach R90 (g), Tatsachennotiz für t3_supertrend und die zwei Elliott-Bots im Beleg“. Beleg `docs/belege/TB-169/e_abnahme.txt` Z. 97/110: Punkt 3a bei beiden „Tatsachennotiz: Teilmessung“ — die Trade-Schleife führt keinen Positionszustand (`backtest_elliott.py` Z. 113 bzw. 122), verdrängt wird nur in der Wellenauswahl (`elliott_wave_counter.py` Z. 363 `traded.add`), die Schranke steht davor (Z. 361). Am Erzeuger ist der Fall nicht herstellbar (je 3 Versuche ohne verdrängten Einstieg); kein Einstieg vor dem Tag.
4. Am Signalpfad belegt (TB-166, `docs/belege/TB-166/e_test_schranke.txt` Z. 40/46, 47/47): „gesperrte Welle hinterlaesst keinen traded-Eintrag“, Mutationsprobe beisst (Z. 41/47).

**Frage:** Genügt die Tatsachennotiz als Abnahme, oder ist vor dem Tag eine weitere Probe nötig? **Neigung:** genügt — der Fall nach R90 (g) entsteht in der Trade-Schleife nicht, und die Verdrängung in der Wellenauswahl trägt die Schranke am Signalpfad (Z. 361 vor Z. 363). **Gegen die Neigung:** der Wortlaut von R98 (d) Satz 2 (Signalpfad ersetzt die Prüfung am Erzeuger nicht); bei den Elliott-Bots kann die Verdrängung nach dem Scan entstehen (Wellenauswahl), sie ist nur am Erzeuger nicht herstellbar; die Tatsachennotiz nach R90 (g) setzt voraus, dass der Fall nicht entstehen kann.

## Zur Kenntnis (keine Frage)

- 64 Z. 12434: „gemessen in TB-169 am Stand `69539db`“; gelaufen ist die Sonde am `8520d9e` (nach dem E-Commit). Tatsachennotiz im nächsten Abschnitt; für Punkt 11 ohne Folge.
- `kerzen_je_trade` (TB-169): `searchsorted` mit `.to_datetime64()` für pandas 2.3.3; Probe 25 861 / 25 861 Trades gleich, 0 abweichend (`e_kerzen.txt`).
- `<bot>_positionen.csv` entfällt mit E-3b; `research/mtm_drawdown/grundlage.py` Z. 65 liest sie noch (BACKLOG).

## Lesen und Antwort

Projektablage: REGISTER_INDEX.md; REGISTER_KOPIE_ABSCHNITT_51 (R56), _57 (R90–R92), _61 (R98), _62 (R100, 62.5), _64; die Übergabe 16.10.c. Fehlt eine Kopie, melde das. Nicht lesen: BACKLOG*, ergebnisse/, docs/belege/ (Brauchst du etwas, nenne es). Antwort höchstens 10 KB als projektfuehrung/FABLE_ANTWORT_2026-10-16c_<stichwort>.md: Kurz (je Frage „einverstanden“ oder „anders, weil …“), Registerblock zeichengleich kopierbar ab R104, Leseprotokoll nach R56 (b), Ampel.
