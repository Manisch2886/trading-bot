## FD — TB-168: Register 63 (Vollzug TB-167 nach 37.3, Abhilfe G6 elliott_wave_stocks) und Dialog-Index 16a
*Quelle: `docs/ERGEBNIS_TB-168_register63_vollzug_tb167.md`, Commits `a2768a1` (S0), `02f19f5` (N), `becab61` (K), F = der Abgabe-Commit „TB-168 Abgabe: Ergebnis, BACKLOG, Journal FD“, der diesen Block enthält.*

**Quelle:** Am Registerende steht Abschnitt 63. 63.1 übernimmt den Entwurf des Hash-Übergangs von `strategies/elliott_wave_stocks/multi_symbol_optimise.py` (`3b775700…` ⇒ `0298263c…`, Commit `b6aaa24`) aus `docs/ERGEBNIS_TB-167_g6_ews_schranke_vor_schnitt.md` Z. 47–51 zeichengleich (Bauart 60.1), dazu die Freigabe-Karte von TB-167 (MAC_TB-167 Z. 13) mit Bedingung (Z. 15), die neun Belege aus TB-167 Schritt M und den Satz zur Sperrlisten-Sonde. Vollzieht 62.5 (a). Kopien, Index und Dialog-Index sind nachgezogen; Zeile 16a trägt jetzt `offen` = `nein`. Freigabe: Karte des Betreibers vom 16.10.2026, 14:10.

### Was gemessen ist
- 0a: Zweig `main`, HEAD `2ccec1c`, zwei Einträge wie Soll, Karte gefüllt; Werkzeug-sha256 `b55789f1…` wie Soll.
- V: 30 Prüfungen, NEIN 0, rc 0.
- S: Sonde einmal lesend gegen `sperrliste_abbild_2026-09-26_tb117.json`, Rückgabe 2; Punkt 11 „nicht prüfbar“ (`2`), kein Befund; porcelain vor und nach gleich. Gewählte Fassung: „nicht prüfbar“ (wie in TB-164 erschlossen).
- N: Probe und Eintrag rc 0; 63 ab Z. 12368; append-only, Register 22/0.
- K: alle acht Schritte rc 0; 63 in T6 (Abschnitte 58–63, 68 427 B), keine neue Teildatei; Kopien bytegleich (sha256 `5fa3ff3c…`); Zeilenangaben 464, davon 0 geändert; Index 0–63; Dialog-Index 65/65 (vorher 64/65).
- BACKLOG: Rang 1 nachgetragen.

### Was offen bleibt
- Ein neues Sperrlisten-Abbild unter neuem Namen (37.3) — nicht Teil dieses Auftrags.
- R102 (d) (62.5 (b)); TB-166 E-3a neu auf diesem Stand; Urteil zum Befund R100 (c).
- Die Sicherung `$HOME/tb167_sicherung` bleibt liegen.

### In einfacher Sprache
Im Register stehen jetzt die alte und die neue Prüfsumme der Datei des Bots elliott_wave_stocks, die TB-167 mit Freigabe geändert hat, wortgleich aus dem Ergebnis von TB-167 und mit der Freigabe im Wortlaut. Die einmal gemessene Sperrlisten-Sonde sagt dazu „nicht prüfbar“, weil das Abbild diese Datei gar nicht führt. Im Verzeichnis der Fable-Antworten ist die fehlende Angabe bei der Antwort vom 16.10. a ergänzt, die Prüfung ist dort jetzt vollständig grün. Es lief nichts auf Kursdaten, kein Code wurde geändert.

*Geschrieben 16.10.2026 von der Mac-Sitzung TB-168. Quellenvermerk: siehe Kopf.*
