## FF — TB-169: E-3b Listen-Erzeuger (Schnitt an der Eingabe, Wachen, Doppellauf weg), Abnahme E-3a nach R98 (d), Register 64 (Vollzug TB-166 nach 37.3)
*Quelle: `docs/ERGEBNIS_TB-169_e3b_listen_erzeuger.md`, Commits `69539db` (S0), `8520d9e` (E), `3cbcdee` (N, Register 64), `fd70e54` (K), F = der Abgabe-Commit „TB-169 Abgabe: Ergebnis, BACKLOG, Journal FF“, der diesen Block enthält.*

**Quelle:** E-3b nach PLAN_E3 Teil 2b, Register R86 (b)–(d), R87 (c), R81 (c), R90 (g), R97 (a), R98 (d), 37.3. Zwei Dateien ausserhalb der Sperrliste geändert (`research/tb24_haltedauern/positionen_holen.py`, `alle_bots.py`), ein neuer Test (`test_listen_erzeuger.py`), alles nur über `WZ e3b`. Freigabe: Karte des Betreibers im Chat 32, 16.10.2026, 20:25 („Bedingt freigeben“).

### Was gemessen ist
- 0a: Zweig `main`, HEAD `b9a6202`, vier Einträge wie Soll, Karte gefüllt; die fünf Anhänge mit den Soll-sha256.
- V: 39 Prüfungen, NEIN 0, rc 0 (u. a. `e_notiz.md` md5 und 20 Dateien heute = nachher, zuletzt in `15f28e4`).
- E: `WZ e3b --probe` 6/0, `WZ e3b` 9/0, drei sha256 nachher wie im Bau. Alter Test `test_haltedauer_kern.py` vorher und nachher rc 1 mit derselben einen Fehlzeile (Prüfung 13, schon am HEAD rot); `WZ altvergleich` rc 0.
- E: Kerzen-Probe auf dem Snapshot `63e4b6c8…` erstmals in `trading-env` (Python 3.9.6): 25 861 Trades, 0 abweichend oder ohne Kursreihe, alle neun Bots voll abgedeckt.
- E: Abnahme nach R98 (d) `test_listen_erzeuger.py` 117 von 117, rc 0; `WZ abnahme` 9 × 13 ja, rc 0.
- S: Sonde einmal lesend, Punkt 11 „nicht prüfbar“ (`2`), porcelain vor/nach gleich.
- N: Register 64 append-only ab Z. 12390 (numstat 46/0), 64.1 mit `e_notiz.md` zeichengleich; Probe und Eintrag je rc 0.
- K: Registerkopie, Abschnitte 0–64, Prüfung BYTEGLEICH; Index-Zeilen 466 umgeschrieben, 0 geändert; Index Kopf 0–64, Zeile 64, Pflegezeile TB-169.

### Was offen bleibt
- Vor der Neuerzeugung der neun Listen: R102 (d), R92 (c); `research/tb24_haltedauern/auswertung.py` (Z. 71, 325) und `research/faltenplan_neun/embargo_neun.py` (Z. 35, Lesestelle Z. 232) lesen noch `<bot>_positionen.csv` bzw. `trades_ausgefuehrt`, die mit E-3b entfallen; ebenso `research/mtm_drawdown/grundlage.py` (Z. 65), im Auftrag nicht genannt.
- Das Abbild tb117 führt die neun `daten/<bot>_alle_trades.csv`; ein neues Abbild unter neuem Namen erst vor dem Tag (37.3).
- Der Sondensatz in 64 nennt den Stand `69539db` (S0); gelaufen ist die Sonde nach dem E-Commit am Stand `8520d9e`.

### In einfacher Sprache
Das Programm, das die Handelslisten der neun Bots erzeugt, liest jetzt nur noch Kurse vor dem Go-Live-Tag und hält mit einem Fehler an, sobald etwas Späteres oder ein zu früher Einstieg durchrutscht. Ein neuer Test auf erfundenen Kursen prüft das an den fertigen Listen und ist ganz grün (117 von 117). Die Kerzenzählung wurde an einer Stelle für die Mac-Fassung von pandas angepasst und liefert für alle 25 861 alten Trades dieselben Zahlen. Weil der Test grün war, stehen die 20 Prüfsummen-Wechsel aus TB-166 jetzt im Register (Abschnitt 64). Die echten Listen wurden nicht neu erzeugt, es lief nichts auf echten Kursdaten.

*Geschrieben 16.10.2026 von der Mac-Sitzung TB-169. Quellenvermerk: siehe Kopf.*
