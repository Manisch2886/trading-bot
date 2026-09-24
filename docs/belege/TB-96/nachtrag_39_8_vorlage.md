⭐⭐ **Nachtrag zu 39.8 (40.5, Fable 24a, TB-96, 24.09.2026) — die Messbitte
oben ist beantwortet.** Gemessen in TB-95 (`069370d`; Belege
`docs/belege/TB-95/d1_wer_oeffnet.txt`, `d2_stoerprobe.txt`, `d3_antwort.md`),
im Modus-Lauf gegen den Snapshot `63e4b6c8…`, Sichtschutz 27.1 (keine
Ergebnisgrössen):

| | |
|---|---|
| **Wer öffnet** | **`benchmark.py` selbst**, kein Nebenweg: `benchmark.py::je_bot` → `faltenplan.py::faltenplan` → `_plan` → `faltenlaenge_jahre` → `gefundene_trades_je_jahr` (`read_csv`). Jede der neun Listen **genau einmal**, **nur im Hauptprozess**; die zehn Kindprozesse (Trockenlauf/Loader) und `registerdaten.py` öffnen keine davon |
| **Gehen sie ein?** | **Ja — über genau eine Grösse, die Faltenlänge.** Gelesen wird nur `entry_time`; gezählt je vollem Kalenderjahr, gemittelt, gegen die Schwelle aus 5.4 verglichen ⇒ Faltenlänge 1 oder 2 ⇒ Faltengrenzen ⇒ Tabellenzeilen. Sonst erreicht nichts aus den Listen die Tabelle |
| **Störprobe, in beide Richtungen** (auf Kopien, Originale vorher = nachher) | **eine Zeile weg ⇒ Tabelle bytegleich** (`64fb2912…`), weil die Schwelle nicht überschritten wird; **zwei von drei Zeilen weg ⇒ verschieden** (`97cf224f…`): **ein** Bot (`volatility_breakout_crypto`) kippt von Einjahres- auf Zweijahresfalten, die anderen **acht bleiben gleich** |
| **Herkunft** | ein einziger Commit, **`78e2bc6`, 13.09.2026, TB-24**, seitdem unverändert — die TB-24-Listen, gemessen an Pfad, Commit und Datum; vor TB-31/TB-34/TB-38 und vor dem Snapshot. **Nicht im Snapshot, nicht auf der Sperrliste**; im Register als Quelle genannt (5.4), **ohne Hash** |
| Nebenbefund | Derselbe Modus-Lauf lieferte die vollzogene Tabelle zum fünften Mal bytegleich (`64fb2912…`, 39.6) |

⚠️ **Der methodische Satz, der über den Fall hinausgeht:** Die Störprobe, wie
der Auftrag TB-95 sie vorschlug („eine Zeile entfernen genügt"), hätte
**allein das falsche „nein"** ergeben. Eine Eingabe, die über eine Schwelle
wirkt, zeigt bei kleinen Änderungen nichts; wer nur in eine Richtung stört,
misst die Schwelle nicht, sondern ihren Abstand. ⇒ Eine Störprobe nach „geht
es ein?" wird in **beide** Richtungen geführt: klein (bleibt gleich?) **und**
über eine bekannte Schwelle hinweg (ändert sich?).

⇒ **Die Einordnung steht in 40.6:** Die neun Listen sind Eingabedateien nach
23d in voller Form — Neu-Erzeugung auf dem Snapshot, Sperrlistenpunkt,
Ableitung der Faltenlänge nach 5.4 und Vergleich gegen 33.2 (TB-98). Die
Nummer 40.5 verweist hierher.
