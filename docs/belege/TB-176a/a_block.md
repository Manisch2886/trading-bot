## FM — TB-176a: Register 68 (Fable 17c, R108, neun Marken, S-B1 Nachtrag 10a.5) und Leser `auswertung.py`/`embargo_neun.py` auf `alle_trades` (E2)
*Quelle: `docs/ERGEBNIS_TB-176a_register68_fable17c_leser.md`, Commits `17648ad` (S0, Fable 17.10.c und Auftrag), `53e8d54` (R, Register 68, neun Marken, S-B1 10a.5), `9f95602` (K, Registerkopie, Index, Dialog-Index), `8465533` (E2, zwei Leser), danach der Abgabe-Commit „TB-176a Abgabe: Ergebnis, BACKLOG, Journal FM“, der diesen Block enthält.*

**Quelle:** Fable-Antwort 17.10.c (md5 `a2b38226…`, Registerblock R108) mit Anfrage 17.10.c (md5 `0a559c88…`) und Übergabe 17.10.c (md5 `db41d912…`), R56 (b), Bauart 67 (TB-175). Alles nur über `WZ` (Anhang A des Auftrags, sha256 `169283de…`), Leser aus Anhang B/C (sha256 `9de89e6d…`, `f35119ba…`), Probe aus Anhang D (sha256 `e99c4664…`). Freigabe: Karte des Betreibers im Chat 35, 17.10.2026, 20:40 („Freigeben“).

### Was gemessen ist
- 0a: Zweig `main`, HEAD = origin/main = `6da15e0`, genau vier Einträge wie Soll, Karte gefüllt; vier Anhänge mit den Soll-sha256 (`Dateien 4`). Fable 17.10.c aus `data_sicherung/steuernder_chat_tmp/f17c/` kopiert, md5 vorher = nachher (3/0, rc 0). S0 = `17648ad`, porcelain danach leer.
- V: 35 Prüfungen, NEIN 0, rc 0. R108 (d) gemessen (kein Urteil): Register am Stand `7fe6342` nennt das Startkapital an einer Stelle (Z. 12167, 59.1, „Startkapital 10 000“); alle neun `equity_simulation.py` tragen `STARTING_CAPITAL = 10_000.0`.
- R (Python 3.9.6): Probe 7/0, Eintrag 11/0, je rc 0. Abschnitt 68 ab Z. 12717; R108 mit Quellenzeile je genau einmal zeichengleich; neun Marken an 16.4 (Z. 2259), 16.6 (Z. 2371), 16.8 (Z. 2478), 29.3 (Z. 5456), 37.5 (Z. 7286), 41.3 C2 (Z. 8943), 62.2 (Z. 12358), 66.1 (Z. 12588), 67.1 (Z. 12657); sonst append-only (numstat 97/0). S-B1: Marke an 10a.2 (Z. 606), Nachtrag 10a.5 (Z. 639) im Wortlaut aus R108 (a), sonst zeichengleich (numstat 9/0).
- K: alle acht Belegdateien rc 0; Registerkopie bytegleich (sha256 `c968a0ec…`, 1 254 111 B), Abschnitt 68 in Teil 6, 69 Abschnittsdateien; Index 0–68 mit Zeile 68 und Abschnitt 19; Dialog-Index 69 von 69 Zeilen, 17c eingetragen.
- E2 (Python 3.9.6): Probe an einer Kopie im Temp-Ordner 9 von 9 (n = 6 je Bot inkl. der zwei `ausgefuehrt=False`, Median 3,5, P95 t3 9,0 → Embargo 10; beide HEAD-Fassungen scheitern an `<bot>_positionen.csv`); `test_haltedauer_kern.py` „Alle Pruefungen bestanden.“, rc 0, Gegenprobe 13 an `auswertung.py` trifft; `WZ nachher2` 17/0 (übrige Gruppe unverändert, beide Leser lesen kein Startkapital).

### Was offen bleibt
- R108 (d) Wert und Ort des Startkapitals (TB-176b, Handelscode), nach der Frage an den Verfahrensprüfer zur Voraussetzung (68.2 (a)).
- R108 (e) nachgeholte Prüfung mit gegen ohne Schranke (t3_supertrend, zwei Elliott-Bots); wartet auf Fable 17.10.d.
- R108 (a): Tatsachennotiz mit äusserer Quelle und Datum zu 10a.5 (kein UCITS-Fonds auf ein einzelnes Edelmetall) fehlt.
- R108 (c): D4 in `test_faltenplan_neun.py` bleibt bei t3_supertrend auf den alten Listen rot, bis die Listen neu erzeugt werden; 16.6 bleibt 13. Der Test lief hier nicht (liest Kursdateien).
- `research/mtm_drawdown/grundlage.py`, `messung.py`, `test_mtm_kern.py` unverändert (R94 (b); Startkapital erst mit TB-176b).

### In einfacher Sprache
Die neue Antwort des Verfahrensprüfers liegt mit Anfrage und Übergabe unverändert im Repo; ihr Regeltext R108 steht wortgleich als Abschnitt 68 im Register, mit neun Hinweisen an älteren Stellen. Die Vorregistrierung des ETF-Vorhabens hat einen datierten Nachtrag: Gold und Silber laufen über ETCs, weil es keinen UCITS-Fonds auf ein einzelnes Metall gibt – die äussere Quelle dafür fehlt noch. Wo das Startkapital steht, ist nur gemessen (überall 10 000), nicht entschieden. Zwei Auswertungen der Haltedauern rechnen jetzt auf allen gefundenen Trades; am Handelscode hat sich nichts geändert, auf Kursdaten lief nichts.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-176a. Quellenvermerk: siehe Kopf.*
