## FA — TB-164: Register 60 (Vollzug TB-163 nach 37.3) und Tatsachennotiz Posten 5 (R43)
*Quelle: `docs/ERGEBNIS_TB-164_register60_vollzug_tb163.md`, Commits `1d037f9` (S0), `92cb637` (N), `3dfa3ba` (K), F = der Abgabe-Commit „TB-164 Abgabe: Ergebnis, BACKLOG, Journal FA“, der diesen Block enthält.*

**Quelle:** Am Registerende steht Abschnitt 60. 60.1 übernimmt den Entwurf des Hash-Übergangs der vier Aktien-Optimierer aus `docs/ERGEBNIS_TB-163_register59_posten4_horizont.md` Z. 111–123 zeichengleich (Bauart 50.3), dazu den Satz zur Sperrlisten-Sonde. 60.2 ist die Tatsachennotiz zu Posten 5 nach R43: die neun `multi_symbol_optimise.py` stehen nicht im Laufpfad, die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ gehört in den Zellen-Erzeuger; die sha256 der neun Dateien am `1d037f9` stehen dabei. Kopien, Index und Dialog-Index sind nachgezogen. Freigabe: Karte des Betreibers vom 15.10.2026, 19:27.

### Was gemessen ist
- 0a: Zweig `main`, HEAD `89e58ef`, zwei Einträge wie Soll; Werkzeug-sha256 `7628b47e…` wie Soll.
- V: 23 Prüfungen, NEIN 0, rc 0.
- S: Sonde einmal lesend gegen `sperrliste_abbild_2026-09-26_tb117.json`, Rückgabe 2; Punkt 11 „nicht prüfbar“ (`2`), kein Befund; porcelain vor und nach gleich. Gewählte Fassung: „nicht prüfbar“. Die Erwartung in ERGEBNIS_TB-163 Z. 129 („Befund `1`“) ist damit richtiggestellt — sie war erschlossen, nicht gemessen; ERGEBNIS_TB-163 bleibt unverändert.
- N: Probe und Eintrag rc 0; 60 ab Z. 12153; numstat Register 42/0.
- K: alle sechs Schritte rc 0; 60 in T6 (Abschnitte 58–60, 29 416 B), keine neue Teildatei; Kopien bytegleich; Index 0–60; Dialog-Index 61/61.
- BACKLOG: Rang 1 nachgetragen; zwei neue Zeilen (Bindung der Scan-Schleifen offen, „vor E-6“ überholt; TypeError `backtest_breakout.py` Z. 211 bei tz-behaftetem `open_time`).

### Was offen bleibt
- Ein neues Sperrlisten-Abbild unter neuem Namen (37.3) — nicht Teil dieses Auftrags (Karte).
- Der Bau des Zellen-Erzeugers mit der Wache (Posten 5 nach R43).
- Nach der zweiten Karte vom 15.10.2026: neuer Fable-Chat zu Register 57.6 Nr. 4/5 (R90 (c), Rückfrage F1).

### In einfacher Sprache
Im Register stehen jetzt die alten und neuen Prüfsummen der vier Aktien-Optimierer, wortgleich aus dem Ergebnis von TB-163. Dazu steht dort, dass die neun Optimierer im späteren Lauf nicht vorkommen und die Wache gegen zu frühe Einstiege deshalb in einen neuen Baustein gehört. Die einmal gemessene Sperrlisten-Sonde sagt zu diesem Punkt „nicht prüfbar“ und nicht „Befund“, wie TB-163 vermutet hatte. Es lief nichts auf Kursdaten, kein Code wurde geändert.

*Geschrieben 15.10.2026 von der Mac-Sitzung TB-164. Quellenvermerk: siehe Kopf.*
