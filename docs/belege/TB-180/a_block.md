## FQ — TB-180: Startkapital am Ort (Nachtrag zu Punkt 9, STARTING_CAPITAL in shared/handelskosten.py, neues Abbild, Register 71, Probe am Ort)
*Quelle: `docs/ERGEBNIS_TB-180_startkapital_am_ort.md`, Auftrag `docs/auftraege/MAC_TB-180_startkapital_am_ort_punkt9_abbild_probe.md`, Belege `docs/belege/TB-180/`, Commits `ebee3ef` (S0, Auftrag), `f60f92b` (C, Handelscode und Probe), `fd8f277` (R, Nachtrag, Abbild, Abschnitt 71) und `321757e` (K, Registerkopie, Index, Dialog-Index), danach der Abgabe-Commit.*

### Was gemessen ist
- V: 35 Prüfungen, NEIN 0 (`v_voraussetzung.txt`); Sonde am alten Abbild `RUECKGABEWERT 2`, 37 Pfad-Bestandteile mit 0; `vergleich.py --pruefen` rc 1 wegen `_cutoff_je_symbol` (Ausgangslage).
- C: zwölf Dateien md5 = Soll; `STARTING_CAPITAL = 10_000.0` genau einmal in `shared/handelskosten.py` (Z. 39), neun Bots mit Import statt Zuweisung, Import 9/9 aus `shared/handelskosten.py`; `vergleich.py --pruefen` zeichengleich zu vorher, Gegenprobe (Ort 20_000.0) rc 1 mit 9 `STARTKAPITAL`-Zeilen (`c_pruefen.txt`, 35/0).
- N: `Ergebnis: 9 von 9 bytegleich (vorher gegen nachher)` (`n_vergleich.txt`).
- T: `test_ergebniskurven.py` 49 von 49, 0 fehlgeschlagen, etwa 216 s; Prüffall 11 fünfmal `[OK ]` (neun Kurven, Mutation am Ort einmal, alle neun weichen ab, zurückgesetzt bytegleich, Ort im Repo unberührt).
- R1/B/R2: Nachtrag zu Punkt 9 (Z. 1080–1082), Abbild `sperrliste_abbild_2026-10-17_tb180.json` (11 780 B, sha256 `f83f0323…d6d9`); Sonde neu 38 Bestandteile mit 0, `RUECKGABEWERT 2`; Sonde alt `RUECKGABEWERT 1` (Gegenprobe); Abschnitt 71 und Marke an 29.3.
- K: Registerkopie bytegleich (6 Teile, 72 Abschnittsdateien), Index Kopf 0–71 mit Zeile 71, Dialog-Index 71/71, 17d und 17e `offen: nein`.

### Was offen bleibt
- Punkt 9 bleibt in der Sonde bei 2 (Regel-Bestandteil, Wert) bis zum Tag (71.2 (c)); die Abweichung `_cutoff_je_symbol` gegen ERWARTUNG in `vergleich.py` besteht weiter (nicht Teil dieses Auftrags).
- Alte `__pycache__`-Ordner (cpython-310, September/Oktober, ignoriert) liegen im Arbeitsbaum; nicht aus diesem Lauf.

### In einfacher Sprache
Das Startkapital von 10 000 steht jetzt an genau einer Stelle, und diese Stelle ist gesperrt und mit Fingerabdruck registriert. Die neun Bots lesen es von dort. Ihre Ergebnisse sind vorher und nachher Byte für Byte gleich; ein Test beweist, dass eine Änderung an dieser einen Stelle alle neun trifft.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-180. Quellenvermerk: siehe Kopf.*
