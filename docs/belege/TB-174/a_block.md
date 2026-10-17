## FK — TB-174: R106 (d) Weg 1, Probe `test_t3_verdraengung.py` am Listen-Erzeuger (Fall nach R90 (g) bei t3_supertrend über den Gleichstand herbeigeführt), 8 von 8
*Quelle: `docs/ERGEBNIS_TB-174_r106d_t3_fall.md`, Commits `015a6ac` (S0), `ae12719` (E, Probe und Belege), danach der Abgabe-Commit „TB-174 Abgabe: Ergebnis, BACKLOG, Journal FK“, der diesen Block enthält.*

**Quelle:** R106 (d) Weg 1 (Register 66, mit TB-173 eingetragen), R105 (d), R90 (g), R98 (d), R87 (c), 40.7; BACKLOG Rang 1; Vorbild `research/tb24_haltedauern/test_elliott_verdraengung.py` (TB-171) und `test_listen_erzeuger.py` (TB-169). Eine neue Testdatei, alles nur über `WZ` (Anhang A des Auftrags, sha256 `0e9f70b3…`). Freigabe: Karte des Betreibers im Chat 33, 17.10.2026, 17:03 („Freigeben“). Kein Registereintrag (R106 (d): „Welcher Weg, ist Handwerk“).

### Was gemessen ist
- 0a: Zweig `main`, HEAD = origin/main = `5a01d55`, genau zwei Einträge wie Soll, Karte gefüllt; beide Anhänge mit den Soll-sha256 (`Dateien 2`). S0 = `015a6ac`, porcelain danach leer.
- V: 17 Prüfungen, NEIN 0, rc 0 (12 Dateien Handelscode und Erzeuger je md5 = Bau, Probe noch nicht im Repo, R106 mit (d) im Wortlaut, R105 genau einmal, BACKLOG Rang 1 ohne TB-174, Journal FJ).
- E: Probe `research/tb24_haltedauern/test_t3_verdraengung.py` (sha256 `492421a7…`) erstmals in `trading-env` (Python 3.9.6, numpy 2.0.2, pandas 2.3.3): **8 von 8, rc 0**, 14 s (am Bau 3.10.12, rund 25 s). Die Rundung trifft den Gleichstand auf dem Mac bei derselben Wahl wie am Bau: Anker 2024-06-10, L 63.0, E1 2024-08-05 08:00, Tag 2024-08-15, s 2025-01-01 00:00, fast == slow auf 496 Balken, ADX bei s 100.0, Ausstieg E1 ohne Schranke 2025-01-02 16:00. `use_t3_exit` True, vom Erzeuger nicht übergeben.
- E: Erzeuger mit Schranke ohne Einstieg von AAA vor dem Tag und mit E2 bei s; Gegenprobe 40.7 (Schranke aus ⇒ R87 (c) beisst an E1, rc 2); Schranke und Wachen aus ⇒ E1 über den Tag offen, Einstieg bei s verdrängt; ohne Eingriff kein Einstieg bei E1/s; BBB/CCC/BTCUSDT gleich; Mutante M1 (Schranke hinter der Zustandsmaschine, nur an einer Kopie) ⇒ E2 fehlt bei s.
- E: `WZ nachher` 15/0, rc 0 — die 12 md5 unverändert, Probe im Repo = Anhang, 8 ja-Zeilen.

### Was offen bleibt
- An den Verfahrensprüfer: ob R106 (d) damit geschlossen und die Abnahme nach R98 (d) in 64.1 für `t3_supertrend` vollständig ist.
- R102 (d)-Befund aus TB-172 als Frage an den Verfahrensprüfer; vor der Neuerzeugung vier Leser von `<bot>_positionen.csv` auf `<bot>_alle_trades.csv` umstellen.

### In einfacher Sprache
Der T3-Bot darf vor dem Tag, ab dem ein Symbol handelbar ist, nicht einsteigen. Wäre er zu früh eingestiegen, könnte die offene Position ein späteres Kaufsignal blockieren. Das geht nur in einem Sonderfall: wenn die zwei T3-Linien genau gleich hoch liegen. Der neue Test baut diesen Fall gezielt in eine Kopie der erfundenen Testkurse ein und ist auf dem Mac ganz grün (8 von 8). Mit der Sperre kommt das spätere Signal durch; ohne die Sperre fehlt es, und mit falsch gesetzter Sperre schlägt der Test an. Am Handelscode hat sich nichts geändert, und es lief nichts auf echten Kursdaten.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-174. Quellenvermerk: siehe Kopf.*
