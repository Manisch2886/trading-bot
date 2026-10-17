## FO — TB-178: Register 69 (Fable 17d, R109) und 70 (Fable 17e, R110) mit zehn Marken; Abnahme des späten Symbolfalls am Erzeuger (R110 (a)) für drei Bots
*Quelle: `docs/ERGEBNIS_TB-178_register69_70_spaetes_symbol.md`, Commits `14833dd` (S0, Fable 17.10.d und 17.10.e und Auftrag), `47f184b` (R, Register 69 und 70, zehn Marken), `0d6ac21` (K, Registerkopie, Index, Dialog-Index), `ffbf069` (P, Probe am Erzeuger), danach der Abgabe-Commit „TB-178 Abgabe: Ergebnis, BACKLOG, Journal FO“, der diesen Block enthält.*

**Quelle:** Fable-Antwort 17.10.d (md5 `3b886ee7…`, Registerblock R109) und 17.10.e (md5 `1d964b31…`, Registerblock R110), je mit Anfrage (md5 `00719693…`, `36389b78…`) und Übergabe (md5 `b968fc12…`, `a204bed1…`), R56 (b), Bauart 67/68 (TB-175, TB-176a). Alles nur über `WZ` (Anhang A des Auftrags, sha256 `552f5c4d…`), Probe aus Anhang B (sha256 `1fe6f12e…`). Freigabe: Karte des Betreibers im Chat 35, 17.10.2026 („Freigeben“).

### Was gemessen ist
- 0a: Zweig `main`, HEAD = origin/main = `e79ca2c`, genau zwei Einträge wie Soll, Karte gefüllt; zwei Anhänge mit den Soll-sha256 (`Dateien 2`). Sechs Fable-Dateien aus `data_sicherung/steuernder_chat_tmp/f17d/` und `f17e/` kopiert, md5 vorher = nachher (6/0, rc 0). S0 = `14833dd`, porcelain danach leer.
- V: 34 Prüfungen, NEIN 0, rc 0. R109 (b) Voraussetzung gemessen (kein Urteil): `test_listen_erzeuger.py` überschreibt in `hb()` die Rechnung mit den vom Test übergebenen Tagen (`x.update(t)`, Z. 76), Prüfung 3b setzt den Tag von CCC (Z. 161) — gesetzt, wie R110 (a) es einträgt.
- R (Python 3.9.6): Probe 7/0, Eintrag 11/0, je rc 0. Abschnitt 69 ab Z. 12814, 70 ab Z. 12875; R109 und R110 mit Quellenzeile je genau einmal zeichengleich; zehn Marken an 29.3 (Z. 5459, 5462), 37.2 (Z. 7041), 37.5 (Z. 7298), 38.5 (Z. 7567), 66.1 (Z. 12606, 12609), 67.1 (Z. 12681), 68.1 (Z. 12750), 69.1 (Z. 12823); sonst append-only (numstat 109/0).
- K: alle acht Belegdateien rc 0; Registerkopie bytegleich (sha256 `640ee3a0…`, 1 274 246 B), 69 und 70 in Teil 6, 71 Abschnittsdateien; Index 0–70 mit Zeilen 69/70 und neuem Abschnitt 20 (zehn Marken); Dialog-Index 71 von 71 Zeilen, 17d und 17e eingetragen.
- P (Python 3.9.6): Probe 18 von 18, rc 0; je Bot 6 von 6. Tage aus der Rechnung nach 23.5, kein Tag gesetzt; mit und ohne Schranke bytegleich, 0 entfernt (t3_supertrend 58/58, elliott_wave 11/11, elliott_wave_stocks 36/36), SPAET-Trades erst ab dem Tag; Lesehaken nur Snapshot-Dateien. Gegenprobe beide Seiten: ohne Schranke rc 2 (R87 (c)), mit Schranke rc 0 und 60 / 11 / 25 Zeilen nur ohne Schranke und Wachen. `WZ nachher` 13/0 (Erzeuger-Dateien unverändert).

### Was offen bleibt
- R110 (b): Bauauftrag nach 37.3 in vier Schritten (Nachtrag zu Punkt 9 mit `shared/handelskosten.py`, Konstante `STARTING_CAPITAL`, neues Abbild, Ergänzung zu 29.3 mit den neun Fundstellen); Handelscode, Vorschlag TB-180, frischer Gegenleser.
- R110 (c): Probe in `shared/test_ergebniskurven.py` (Mutation am Ort, alle neun Kurven weichen ab); mit TB-180.
- R109 (a): Registertext zu 29.3 nicht eingetragen; folgt dem Bauauftrag nach R110 (b).
- Das Ob aus R110 (a): ob eine andere Abnahme in 64.1 allein auf 3b steht — nicht gemessen.

### In einfacher Sprache
Zwei neue Antworten des Verfahrensprüfers liegen mit Anfrage und Übergabe unverändert im Repo; ihre Regeltexte R109 und R110 stehen wortgleich als Abschnitte 69 und 70 im Register, mit zehn Hinweisen an älteren Stellen. An erfundenen Kursdaten mit einem spät beginnenden Symbol hat die Mac-Sitzung gezeigt, dass die Schranke am Handelbar-Tag bei t3_supertrend und beiden Elliott-Bots nichts ändert, wenn vor dem Tag kein Signal liegt, und dass sie greift, wenn eines vorliegt. Damit ist die Bedingung des Tags für alle drei Bots erfüllt. Wo das Startkapital im Code seinen festen Ort bekommt, ist Handelscode und kommt als eigener Auftrag.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-178. Quellenvermerk: siehe Kopf.*
