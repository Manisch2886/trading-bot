## FG — TB-170: Register 65 (Fable 16c, R104–R105 zeichengleich), fünf Marken, 65.3 Voraussetzungen und Befunde; BACKLOG-Nachträge
*Quelle: `docs/ERGEBNIS_TB-170_register65_fable16c.md`, Commits `801a055` (S0), `7aecfe6` (R, Register 65), `c602a2f` (K), danach der Abgabe-Commit „TB-170 Abgabe: Ergebnis, BACKLOG, Journal FG“, der diesen Block enthält.*

**Quelle:** Fable-Antwort 16.10.c (`docs/projektfuehrung/FABLE_ANTWORT_2026-10-16c_r100c_elliott_abnahme.md`, md5 `ebde5e99…`, Registerblock Z. 21–26), R56 (b), Bauart 61/62; alles nur über `WZ` (Anhang A des Auftrags, sha256 `a75dc809…`). Freigabe: Karte des Betreibers im Chat 33, 17.10.2026, 06:06 („Freigeben“).

### Was gemessen ist
- 0a: Zweig `main`, HEAD = origin/main = `eff5b5a`, genau sieben Einträge wie Soll, Karte gefüllt; Anhang sha256 wie Soll (`Dateien 1`); `WZ md5` 5/0, rc 0. S0 = `801a055` mit den drei Fable-Dateien 16.10.c, UEBERGABE und EROEFFNUNG unverändert.
- V: 35 Prüfungen, NEIN 0, rc 0 — u. a. fünf Marken-Orte eindeutig, M3 bei 9 von 9 Bots ausserhalb der `multi_symbol_optimise.py`, Code beider Elliott-Zähler an Z. 192, 341, 352–353, 358–361, 363 wie erwartet, vier BACKLOG-Anker da.
- R: Probe 6/0, Eintrag 9/0, je rc 0. Abschnitt 65 ab Z. 12451, Marken an Z. 12003 (57.1), 12234 (61.1), 12306 (62.1), 12364 (62.5 (c)), 12446 (64.1); R104/R105 mit Quellenzeile je genau einmal zeichengleich; append-only bis auf die Marken (numstat 83/0).
- K: Registerkopie, Abschnitte 0–65 (66 Dateien), Prüfung je BYTEGLEICH (1 203 527 B); 65 in T6 (93 188 B); Index-Zeilen 466 umgeschrieben, 7 geändert (Verschiebung durch die Marken); Index Kopf 0–65, Zeile 65, Abschnitt 16 (5 Marken); Dialog-Index 66 von 66.

### Was offen bleibt
- R105 (c) Weg 1 bei `elliott_wave` und `elliott_wave_stocks` (Handelscode, eigener Auftrag mit Bau-Helfer und frischem Gegenleser, vor dem Tag); Weg 2 trägt am Code nicht (65.3 (c)) — zur Kenntnis an Fable mit der nächsten Anfrage.
- R105 (d) `t3_supertrend`; R102 (d), R92 (c)/R86 (e) vor der Neuerzeugung der Listen.
- Der Kopf von `REGISTER_INDEX.md` mischt weiter Stände (nur im BACKLOG vermerkt).

### In einfacher Sprache
Die neue Antwort des Verfahrensprüfers liegt jetzt mit Anfrage und Übergabe im Repo, und ihre zwei Regeltexte stehen wortgleich als Abschnitt 65 im Register. An fünf älteren Stellen weist ein kurzer Vermerk auf die neuen Regeln hin, sonst wurde nichts am Register verändert. Die Messungen vorab haben bestätigt, was die Regeln voraussetzen; nur ein vorgeschlagener zweiter Weg für die Elliott-Bots passt nicht zum Code und bleibt deshalb ein eigener Code-Auftrag. Es lief nichts auf Kursdaten, kein Handelscode wurde geändert.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-170. Quellenvermerk: siehe Kopf.*
