## FH — TB-171: R105 (c) Weg 1, Probe `test_elliott_verdraengung.py` am Listen-Erzeuger (Fall nach R90 (g) bei elliott_wave und elliott_wave_stocks herbeigeführt), 16 von 16
*Quelle: `docs/ERGEBNIS_TB-171_r105c_elliott_fall.md`, Commits `8201947` (S0), `76cb3e4` (E, Probe und Belege), danach der Abgabe-Commit „TB-171 Abgabe: Ergebnis, BACKLOG, Journal FH“, der diesen Block enthält.*

**Quelle:** R105 (c) Weg 1 (Register Z. 12464), Register 65 (c), R90 (g), R98 (d), R87 (c), 40.7; BACKLOG Rang 1; Vorbild `research/tb24_haltedauern/test_listen_erzeuger.py` (TB-169). Eine neue Testdatei, alles nur über `WZ` (Anhang A des Auftrags, sha256 `6f049b91…`). Freigabe: Karte des Betreibers im Chat 33, 17.10.2026, 09:12 („Freigeben“). Kein Registereintrag (R105 (c): „Welcher Weg, ist Handwerk“).

### Was gemessen ist
- 0a: Zweig `main`, HEAD = origin/main = `241ca0b`, genau zwei Einträge wie Soll, Karte gefüllt; beide Anhänge mit den Soll-sha256 (`Dateien 2`). S0 = `8201947`, porcelain danach leer.
- V: 20 Prüfungen, NEIN 0, rc 0 (15 Dateien Handelscode und Erzeuger je md5 = Bau, Probe noch nicht im Repo, R105 und 65 (c) im Wortlaut, BACKLOG Rang 1 Stand TB-170, Journal FG).
- E: Probe `research/tb24_haltedauern/test_elliott_verdraengung.py` (sha256 `59f6c90b…`) erstmals in `trading-env` (Python 3.9.6): **16 von 16, rc 0**, 36 s (am Bau 3.10.12, rund 60 s). Je Bot: Signalpfad k+1 ohne / k+4 mit Schranke, W dieselbe Welle (fib_score 1.0) und ohne Schranke über den Tag offen, Erzeuger mit Schranke ohne Einstieg vor dem Tag und mit W bei k+4, Gegenprobe 40.7 (Schranke aus ⇒ R87 (c) beisst an W, rc 2), Schranke und Wachen aus ⇒ k+4 verdrängt, ohne Eingriff kein Einstieg bei k+1/k+4, BBB/CCC gleich, Mutante M1 (Schranke hinter `traded.add`, nur an einer Kopie) ⇒ W fehlt bei k+4.
- E: `WZ nachher` 18/0, rc 0 — die 15 md5 unverändert, Probe im Repo = Anhang, 16 ja-Zeilen.

### Was offen bleibt
- An den Verfahrensprüfer: ob R105 (c) damit für beide Bots geschlossen ist und ob „eine spätere Welle“ in R105 (c) den späteren Einstieg derselben Welle trägt (Schlüssel `end_time`, Register 65 (c)).
- R105 (d) `t3_supertrend` unberührt; R102 (d), R92 (c)/R86 (e) vor der Neuerzeugung der Listen.

### In einfacher Sprache
Die zwei Elliott-Bots dürfen vor dem Tag, ab dem ein Symbol handelbar ist, nicht einsteigen; eine zu frühe Welle wird gesperrt und darf später noch einsteigen. Dieser Fall kam in den erfundenen Testkursen nie von selbst vor. Der neue Test baut ihn gezielt in eine Kopie der Testkurse ein und ist auf dem Mac ganz grün (16 von 16): mit der Sperre steigt die Welle später ein, ohne die Sperre steigt sie zu früh ein und der spätere Einstieg fehlt, und mit falsch gesetzter Sperre fällt der Test auf. Am Handelscode hat sich nichts geändert, es lief nichts auf echten Kursdaten.

*Geschrieben 17.10.2026 von der Mac-Sitzung TB-171. Quellenvermerk: siehe Kopf.*
