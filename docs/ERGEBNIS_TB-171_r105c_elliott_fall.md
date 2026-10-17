# ERGEBNIS TB-171 — R105 (c) Weg 1: Fall nach R90 (g) bei elliott_wave und elliott_wave_stocks am Listen-Erzeuger herbeigeführt (Probe mit Gegenprobe nach 40.7)

**Sitzung:** TB-171, Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-171_r105c_elliott_fall.md` · **Zweig:** `main`
**Commits:** `8201947` (S0, Schritt 0) · `76cb3e4` (E, Probe und Belege) · der Abgabe-Commit „TB-171 Abgabe: Ergebnis, BACKLOG, Journal FH“, der dieses Ergebnis enthält · danach „TB-171 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-171/` · **Journal:** FH · **Kein Abbruch.**

## Kurz

Neu ist genau eine Testdatei: `research/tb24_haltedauern/test_elliott_verdraengung.py`, sha256 `59f6c90b…` wie Anhang B. Sie führt bei beiden Elliott-Bots den Fall nach R90 (g) herbei. Dazu setzt sie in eine Kopie des Test-Snapshots von TB-169 einen Kursabschnitt ein: eine Welle W vor dem Handelbar-Tag, die mit Schranke am Tag oder später einsteigt. Ohne Schranke steigt W vor dem Tag ein, und ihr späterer Einstieg wird verdrängt. Auf dem Mac (Python 3.9.6) bestanden **16 von 16**, rc 0, in 36 s. Die Gegenproben greifen: Schranke aus ⇒ die Wache R87 (c) endet mit 2; Schranke und Wachen aus ⇒ der Einstieg bei k+4 fehlt; Mutante M1 mit der Schranke hinter `traded.add` ⇒ W fehlt bei k+4. Die 15 md5 von Handelscode und Erzeuger sind vor und nach dem Lauf unverändert. Kein Registereintrag, `data/` nicht gelesen, keine Listen neu erzeugt, kein Live, kein Broker.

## Schritt 0

`git status --porcelain` zeigte genau die zwei Soll-Einträge (`docs/belege/TB-171/0a_status.txt`). HEAD und origin/main standen auf `241ca0b0d22b748dcaf7ca5f9fb07d1a6076e99e`, Zweig `main`, die Karte war gefüllt; letzte Zeile `0a gut (2 Eintraege)`. Der Holbefehl lieferte `tb171_werkzeug.py 6f049b915d314d287eb791a71e5c7a72953de67cb3bce6f9fcce2c6f1fac7ad0`, `test_elliott_verdraengung.py 59f6c90bde98a04da20fd52f314399a6e35443cacbfc3e2225d00eab3227d573` und `Dateien 2`. S0 = `8201947`, gepusht, porcelain danach leer.

## Voraussetzungen (`v_voraussetzung.txt`, wörtlich)

```
ja    Handelscode/Erzeuger unveraendert: research/exposure_messung/bot_lauf.py md5 01fd9282ded2
ja    Handelscode/Erzeuger unveraendert: research/faltenplan_neun/faltenschranke_messung.py md5 584d9ff959da
ja    Handelscode/Erzeuger unveraendert: research/tb24_haltedauern/alle_bots.py md5 7bb90ef438d5
ja    Handelscode/Erzeuger unveraendert: research/tb24_haltedauern/positionen_holen.py md5 006375593b4b
ja    Handelscode/Erzeuger unveraendert: research/tb24_haltedauern/test_listen_erzeuger.py md5 d77e73ed5ff7
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave/backtest_elliott.py md5 df5c314e9268
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave/elliott_wave_counter.py md5 75b26dd79237
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave/equity_simulation.py md5 a058c69a7a6c
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave/multi_symbol_optimise.py md5 bf11370b140d
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave/zigzag_indicator.py md5 6e9a91ccc131
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave_stocks/backtest_elliott.py md5 f1979557a945
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave_stocks/elliott_wave_counter.py md5 b7fd099124b4
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave_stocks/equity_simulation.py md5 4ff525c50514
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave_stocks/multi_symbol_optimise.py md5 571076168d56
ja    Handelscode/Erzeuger unveraendert: strategies/elliott_wave_stocks/zigzag_indicator.py md5 407cd69fb5c2
ja    Probe noch nicht im Repo: research/tb24_haltedauern/test_elliott_verdraengung.py
ja    Register: R105 genau einmal, (c) Weg 1 im Wortlaut
ja    Register 65 (c): Weg 2 traegt nicht, Weg 1 bleibt (genau einmal)
ja    BACKLOG Rang 1 genau einmal, Stand TB-170, nennt R105 (c) Weg 1
ja    Journal: hoechste FG (naechste FH)
Pruefungen: 20, NEIN: 0
rc 0
```

## Schritt E — Probe

`trading-env/bin/python3 -B research/tb24_haltedauern/test_elliott_verdraengung.py`, Laufzeit **36 s** (am Bau: Python 3.10.12, rund 60 s). `e_probe.txt` ohne die zwei Kopfzeilen der urllib3-Warnung (`NotOpenSSLWarning`, LibreSSL 2.8.3 — die bekannte Mac-Warnung, ohne Bezug zur Probe), sonst wörtlich:

```
ja    elliott_wave: 0 Signalpfad: ohne Schranke W bei k+1 (2025-03-04 23:00:00), mit Schranke ab Tag 2025-03-05 W bei k+4 (2025-03-05 02:00:00) · (['2025-03-04 23:00:00'], ['2025-03-05 02:00:00'])
ja    elliott_wave: 0b W ist dieselbe Welle (signal_time = P5 2025-03-04 22:00:00, fib_score 1.0), ohne Schranke Ausstieg am Tag oder spaeter · [('2025-03-04 22:00:00', 1.0, '2025-03-14 23:00:00'), ('2025-03-04 22:00:00', 1.0, '2025-03-05 13:00:00')]
ja    elliott_wave: 1 Erzeuger mit Schranke: rc 0, kein Einstieg von AAA vor dem Tag, W erscheint bei k+4 · (0, ['2025-03-05 02:00:00'])
ja    elliott_wave: 2 Gegenprobe 40.7: Schranke aus -> Wache R87 (c) beisst an W (Einstieg k+1 2025-03-04 23:00:00) mit 2 · (2, '[positionen_holen] ABBRUCH elliott_wave: Einstieg 2025-03-04 23:00:00 vor dem Handelbar-Tag 2025-03-05 bei AAA (R87 (c))')
ja    elliott_wave: 3 Schranke und Wachen aus: W bei k+1 vor dem Tag, Ausstieg am Tag oder spaeter, Einstieg bei k+4 fehlt (verdraengt) · (0, ['2025-03-04 23:00:00'], '2025-03-14 23:00:00')
ja    elliott_wave: 4 ohne Eingriff (Snapshot TB-169): AAA ohne Einstieg bei k+1 und k+4 · (0, [])
ja    elliott_wave: 5 BBB/CCC mit und ohne Tag fuer AAA gleich
ja    elliott_wave: 6 Mutante M1 (Kopie des Counters, Schranke hinter traded.add): W fehlt bei k+4 - die Probe 1 schlaegt an · (True, 0, [])
ja    elliott_wave_stocks: 0 Signalpfad: ohne Schranke W bei k+1 (2025-04-04 00:00:00), mit Schranke ab Tag 2025-04-07 W bei k+4 (2025-04-09 00:00:00) · (['2025-04-04 00:00:00'], ['2025-04-09 00:00:00'])
ja    elliott_wave_stocks: 0b W ist dieselbe Welle (signal_time = P5 2025-04-03 00:00:00, fib_score 1.0), ohne Schranke Ausstieg am Tag oder spaeter · [('2025-04-03 00:00:00', 1.0, '2025-08-08 00:00:00'), ('2025-04-03 00:00:00', 1.0, '2025-04-10 00:00:00')]
ja    elliott_wave_stocks: 1 Erzeuger mit Schranke: rc 0, kein Einstieg von AAA vor dem Tag, W erscheint bei k+4 · (0, ['2025-04-09 00:00:00'])
ja    elliott_wave_stocks: 2 Gegenprobe 40.7: Schranke aus -> Wache R87 (c) beisst an W (Einstieg k+1 2025-04-04 00:00:00) mit 2 · (2, '[positionen_holen] ABBRUCH elliott_wave_stocks: Einstieg 2025-04-04 00:00:00 vor dem Handelbar-Tag 2025-04-07 bei AAA (R87 (c))')
ja    elliott_wave_stocks: 3 Schranke und Wachen aus: W bei k+1 vor dem Tag, Ausstieg am Tag oder spaeter, Einstieg bei k+4 fehlt (verdraengt) · (0, ['2025-04-04 00:00:00'], '2025-08-08 00:00:00')
ja    elliott_wave_stocks: 4 ohne Eingriff (Snapshot TB-169): AAA ohne Einstieg bei k+1 und k+4 · (0, [])
ja    elliott_wave_stocks: 5 BBB/CCC mit und ohne Tag fuer AAA gleich
ja    elliott_wave_stocks: 6 Mutante M1 (Kopie des Counters, Schranke hinter traded.add): W fehlt bei k+4 - die Probe 1 schlaegt an · (True, 0, [])
Ergebnis: 16 von 16 bestanden
rc 0
```

`WZ nachher` (`e_nachher.txt`): 18 Prüfungen, NEIN 0, rc 0. Darin: die 15 md5 von Handelscode und Erzeuger unverändert, „Probe im Repo = Anhang (sha256 59f6c90bde98)“, „e_probe.txt endet mit 'Ergebnis: 16 von 16 bestanden' und 'rc 0'“ und „e_probe.txt: 16 ja-Zeilen, keine NEIN-Zeile“. E = `76cb3e4`, gepusht.

Bei `elliott_wave_stocks` fällt k+1 auf Freitag, 04.04.2025; der Handelbar-Tag (Balken k+2) ist deshalb Montag, 07.04.2025. Bei `elliott_wave` ist Balken k+2 auf 05.03.2025, 00:00 gelegt.

## BACKLOG und Journal

`WZ kennung` meldet „Kennung FH (hoechste FG)“. `WZ backlog 17.10.2026 FH` hängt den TB-171-Stand an Rang 1 an: Probe, 16 von 16, Gegenproben und die offene Frage an den Verfahrensprüfer. Der Journal-Block `docs/belege/TB-171/a_block.md` steht vor `## Wiederkehrende Lehren`. Belege: `a_*.txt`.

## Zur Kenntnis (nicht entschieden, nicht gebaut)

R105 (c) spricht von einer Welle, „deren Eintrag in traded ohne Schranke eine spätere Welle verdrängt“; am Code verdrängt der Eintrag den späteren Einstieg derselben Welle (Schlüssel `end_time`, Register 65 (c)). Die Probe zeigt diesen Fall. Ob das R105 (c) für beide Bots schliesst, entscheidet der Verfahrensprüfer. R105 (d) (`t3_supertrend`) bleibt unberührt.

## Offen

- **An den Verfahrensprüfer, mit der nächsten Anfrage:** Ist R105 (c) mit dieser Probe für `elliott_wave` und `elliott_wave_stocks` geschlossen? Trägt „eine spätere Welle“ den späteren Einstieg derselben Welle (Schlüssel `end_time`)?
- **R105 (d)** `t3_supertrend`.
- **Vor der Neuerzeugung der Listen:** R102 (d) und R92 (c)/R86 (e).

## Abweichungen

Keine vom Auftrag. Beobachtungen:

- Der Auftrag verlangt für das Ergebnis „die 12 Zeilen aus `e_probe.txt` wörtlich“. Die Datei hat 20 Zeilen: zwei Warnzeilen von urllib3, 16 ja-Zeilen, die Ergebniszeile und `rc 0`. Oben stehen alle Zeilen ausser den zwei Warnzeilen. Die Zahl 12 passt zu keiner Zählung der Datei, vermutlich ein Versehen im Auftrag.
- Unter der vorgegebenen ersten Zeile tragen die Commit-Nachrichten die Zuschreibungszeilen (Co-Authored-By, Claude-Session), wie in den bisherigen TB-Commits.
- Die Laufzeit ist mit einer Shell-Uhr gemessen (`date +%s` vor und nach dem Lauf), nicht im Beleg selbst.

## In einfacher Sprache

Die zwei Elliott-Bots dürfen vor dem Tag, ab dem ein Symbol handelbar ist, nicht einsteigen. Eine Welle, die zu früh kommt, wird gesperrt und darf später noch einsteigen. In den erfundenen Testkursen kam dieser Fall nie von selbst vor. Der neue Test baut ihn deshalb gezielt in eine Kopie der Testkurse ein, und auf dem Mac ist er ganz grün (16 von 16). Mit der Sperre steigt die Welle später ein. Ohne die Sperre steigt sie zu früh ein, und der spätere Einstieg fehlt. Sitzt die Sperre an der falschen Stelle, schlägt der Test an. Am Handelscode hat sich nichts geändert, und es lief nichts auf echten Kursdaten. Ob damit die offene Regel R105 (c) ganz erledigt ist, entscheidet der Verfahrensprüfer.
