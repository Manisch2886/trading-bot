# ERGEBNIS TB-174 — R106 (d) Weg 1: Fall nach R90 (g) bei t3_supertrend am Listen-Erzeuger herbeigeführt, über den Gleichstand (Probe mit Gegenprobe nach 40.7)

**Sitzung:** TB-174, Mac (Claude Code, Opus 5.5), 17.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-174_r106d_t3_fall.md` · **Zweig:** `main`
**Commits:** `015a6ac` (S0, Schritt 0) · `ae12719` (E, Probe und Belege) · der Abgabe-Commit „TB-174 Abgabe: Ergebnis, BACKLOG, Journal FK“, der dieses Ergebnis enthält · danach „TB-174 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-174/` · **Journal:** FK · **Kein Abbruch.**

## Kurz

Neu ist genau eine Testdatei: `research/tb24_haltedauern/test_t3_verdraengung.py`, sha256 `492421a7…` wie Anhang B. Sie führt bei `t3_supertrend` den Fall nach R90 (g) herbei. Dazu setzt sie in eine Kopie des Test-Snapshots von TB-169 einen Kursabschnitt in die 4h-Reihe von `AAA` ein: Einstieg E1 vor dem Handelbar-Tag, Position über den Tag offen, danach ein Kreuzen nach oben am Gleichstand T3 fast = T3 slow ohne vorheriges Kreuzen nach unten (s). Ohne Schranke wird der Einstieg bei s verdrängt; mit Schranke erscheint E2 bei s. Auf dem Mac (Python 3.9.6, numpy 2.0.2, pandas 2.3.3) bestanden **8 von 8**, rc 0, in 14 s. Die Rundung trifft den Gleichstand auf dem Mac bei derselben Wahl wie am Bau (Anker 2024-06-10, L 63.0). Die Gegenproben greifen: Schranke aus ⇒ die Wache R87 (c) endet mit 2; Schranke und Wachen aus ⇒ der Einstieg bei s fehlt; Mutante M1 mit der Schranke hinter der Zustandsmaschine ⇒ E2 fehlt bei s. Die 12 md5 von Handelscode und Erzeuger sind vor und nach dem Lauf unverändert. Kein Registereintrag, `data/` nicht gelesen, keine Listen neu erzeugt, kein Live, kein Broker.

## Schritt 0

`git status --porcelain` zeigte genau die zwei Soll-Einträge (`docs/belege/TB-174/0a_status.txt`). HEAD und origin/main standen auf `5a01d55099aa3a91ff7fa7487e359568d5d3a26e`, Zweig `main`, die Karte war gefüllt; letzte Zeile `0a gut (2 Eintraege)`. Der Holbefehl lieferte `tb174_werkzeug.py 0e9f70b3c4db245af18867cc1631a4d96d189c126cc924410b52d12c2b17ab41`, `test_t3_verdraengung.py 492421a7fe0c6ffc63b0856d3c0e8ed13af8e1346c95db37e6e5007a6d3ab805` und `Dateien 2`. S0 = `015a6ac`, gepusht, porcelain danach leer.

## Voraussetzungen (`v_voraussetzung.txt`, wörtlich)

```
ja    Handelscode/Erzeuger unveraendert: research/exposure_messung/bot_lauf.py md5 01fd9282ded2
ja    Handelscode/Erzeuger unveraendert: research/faltenplan_neun/faltenschranke_messung.py md5 584d9ff959da
ja    Handelscode/Erzeuger unveraendert: research/tb24_haltedauern/alle_bots.py md5 7bb90ef438d5
ja    Handelscode/Erzeuger unveraendert: research/tb24_haltedauern/positionen_holen.py md5 006375593b4b
ja    Handelscode/Erzeuger unveraendert: research/tb24_haltedauern/test_listen_erzeuger.py md5 d77e73ed5ff7
ja    Handelscode/Erzeuger unveraendert: shared/regimewache.py md5 82cd933f9ba9
ja    Handelscode/Erzeuger unveraendert: strategies/t3_supertrend/backtest_trend.py md5 896948ee3eca
ja    Handelscode/Erzeuger unveraendert: strategies/t3_supertrend/equity_simulation.py md5 be665a734328
ja    Handelscode/Erzeuger unveraendert: strategies/t3_supertrend/indicators.py md5 8452ad509b7a
ja    Handelscode/Erzeuger unveraendert: strategies/t3_supertrend/live_params.py md5 f28553e8deba
ja    Handelscode/Erzeuger unveraendert: strategies/t3_supertrend/multi_symbol_optimise.py md5 dc85993e8d42
ja    Handelscode/Erzeuger unveraendert: strategies/t3_supertrend/regime_filter.py md5 b02087926d7d
ja    Probe noch nicht im Repo: research/tb24_haltedauern/test_t3_verdraengung.py
ja    Register: R106 genau einmal, (d) Weg 1 bei t3_supertrend im Wortlaut (nach TB-173)
ja    Register: R105 genau einmal
ja    BACKLOG Rang 1 genau einmal, endet mit ' |', noch ohne TB-174
ja    Journal: hoechste FJ (FI am Bau-HEAD, FJ falls TB-173 eine Kennung setzt)
Pruefungen: 17, NEIN: 0
rc 0
```

## Schritt E — Probe

`trading-env/bin/python3 -B research/tb24_haltedauern/test_t3_verdraengung.py`, Laufzeit **14 s** (am Bau: Python 3.10.12, numpy 2.2.6, rund 25 s). `e_probe.txt` ohne die zwei Kopfzeilen der urllib3-Warnung (`NotOpenSSLWarning`, LibreSSL 2.8.3 — die bekannte Mac-Warnung, ohne Bezug zur Probe), sonst wörtlich:

```
ja    t3_supertrend: 0 Signalpfad: ohne Schranke E1 (2024-08-05 08:00:00) vor dem Tag 2024-08-15, kein Einstieg bei s (2025-01-01 00:00:00); mit Schranke kein Einstieg vor dem Tag, E2 bei s · (['2024-08-05 08:00:00'], ['2025-01-01 00:00:00'])
ja    t3_supertrend: 0b Gleichstand: E1 bis s-1 fast >= slow, fast == slow auf 496 Balken bis s-1, fast > slow bei s, ADX 100.0; use_t3_exit True, vom Erzeuger nicht uebergeben · ANKER 2024-06-10, L 63.0, Abschnitt-Einstiege ohne Schranke ['2024-06-19 16:00:00', '2024-08-05 08:00:00'], Ausstieg E1 2025-01-02 16:00:00
ja    t3_supertrend: 1 Erzeuger mit Schranke: rc 0, kein Einstieg von AAA vor dem Tag, E2 erscheint bei s · (0, ['2025-01-01 00:00:00'])
ja    t3_supertrend: 2 Gegenprobe 40.7: Schranke aus -> Wache R87 (c) beisst an einem Einstieg des Abschnitts vor dem Tag (2024-08-05 08:00:00) mit 2 · (2, '[positionen_holen] ABBRUCH t3_supertrend: Einstieg 2024-08-05 08:00:00 vor dem Handelbar-Tag 2024-08-15 bei AAA (R87 (c))')
ja    t3_supertrend: 3 Schranke und Wachen aus: E1 vor dem Tag, Ausstieg nach s, Einstieg bei s fehlt (verdraengt) · (0, ['2024-08-05 08:00:00'], '2025-01-02 16:00:00')
ja    t3_supertrend: 4 ohne Eingriff (Snapshot TB-169): AAA ohne Einstieg bei E1 und bei s · (0, [])
ja    t3_supertrend: 5 BBB/CCC/BTCUSDT mit und ohne Tag fuer AAA gleich
ja    t3_supertrend: 6 Mutante M1 (Kopie von backtest_trend.py, Schranke hinter der Zustandsmaschine): kein Einstieg vor dem Tag, aber E2 fehlt bei s - die Probe 1 schlaegt an · (True, 0, [])
Ergebnis: 8 von 8 bestanden
rc 0
```

**Wahl aus 0b:** Anker 2024-06-10, L 63.0 — dieselbe wie am Bau (erster Kandidat der festen Liste nach dem ersten Anker 2024-06-03). E1 2024-08-05 08:00, Tag 2024-08-15, s 2025-01-01 00:00, Gleichstand 496 Balken, ADX bei s 100.0, Ausstieg E1 ohne Schranke 2025-01-02 16:00. Ohne Schranke liegen im Abschnitt zwei Einstiege (2024-06-19 16:00 und E1); der erste schliesst vor E1.

`WZ nachher` (`e_nachher.txt`): 15 Prüfungen, NEIN 0, rc 0. Darin: die 12 md5 von Handelscode und Erzeuger unverändert, „Probe im Repo = Anhang (sha256 492421a7fe0c)“, „e_probe.txt endet mit 'Ergebnis: 8 von 8 bestanden' und 'rc 0'“ und „e_probe.txt: 8 ja-Zeilen, keine NEIN-Zeile“. Vor dem E-Commit zeigte `git status --porcelain --untracked-files=all` nur die neue Probe und die fünf Belege — die Probe hat im Repo nichts sonst verändert. E = `ae12719`, gepusht.

## BACKLOG und Journal

`WZ kennung` meldet „Kennung FK (hoechste FJ)“. `WZ backlog 17.10.2026 FK` hängt den TB-174-Stand an Rang 1 an: Probe, 8 von 8, Gegenproben und die offene Frage an den Verfahrensprüfer. Der Journal-Block `docs/belege/TB-174/a_block.md` steht vor `## Wiederkehrende Lehren`. Belege: `a_*.txt`.

## Zur Kenntnis (nicht entschieden)

Der Gleichstand entsteht nur durch Rundung (Gleitkomma-Fixpunkte der zwölf EMA-Ketten); am Bau trifft er in einer Testreihe bei 8 von 97 L-Werten (60 bis 71,875 in Schritten von 0,125, und 64). Ob er am Mac bei derselben Wahl trifft, ist nicht gemessen; die Probe sucht deshalb selbst, und 0b gibt die Wahl aus. Findet sie keinen Kandidaten, sind alle 8 Prüfungen NEIN (Abbruchweg E).

*Nachtrag nach dem Lauf:* Auf dem Mac trifft er bei derselben Wahl (Anker 2024-06-10, L 63.0) mit derselben Länge (496 Balken). Gemessen ist nur dieser eine Kandidat, nicht die Testreihe der 97 L-Werte.

## Offen

- **An den Verfahrensprüfer, mit der nächsten Anfrage:** Ist R106 (d) mit dieser Probe für `t3_supertrend` geschlossen, und ist die Abnahme nach R98 (d) in 64.1 für `t3_supertrend` damit vollständig?
- **Vor der Neuerzeugung der Listen:** R102 (d)-Befund aus TB-172 an den Verfahrensprüfer; vier Leser von `<bot>_positionen.csv` auf `<bot>_alle_trades.csv` umstellen (TB-173, offen).

## Abweichungen

Keine vom Auftrag. Beobachtungen:

- Die Karte nennt für die Gegenproben am Bau „3 bzw. 5 von 8“, der Auftragstext (Abschnitt „Die Probe“) „3 von 8“ und „4 von 8“ für die Schranke hinter der Zustandsmaschine. Am Mac nicht nachgemessen (der Auftrag sieht keine Repo-Mutation vor); nur festgehalten.
- Der Auftrag verlangt „die 8 Zeilen aus `e_probe.txt` wörtlich“. Die Datei hat 12 Zeilen: zwei Warnzeilen von urllib3, 8 ja-Zeilen, die Ergebniszeile und `rc 0`. Oben stehen alle Zeilen ausser den zwei Warnzeilen.
- Unter der vorgegebenen ersten Zeile tragen die Commit-Nachrichten die Zuschreibungszeilen (Co-Authored-By, Claude-Session), wie in den bisherigen TB-Commits.
- Die Laufzeit ist mit einer Shell-Uhr gemessen (`date +%s` vor und nach dem Lauf), nicht im Beleg selbst.

## In einfacher Sprache

Der T3-Bot darf vor dem Tag, ab dem ein Symbol handelbar ist, nicht einsteigen. Wäre er zu früh eingestiegen, könnte die offene Position ein späteres Kaufsignal blockieren. Das geht nur in einem Sonderfall: wenn die zwei T3-Linien genau gleich hoch liegen. Der neue Test baut diesen Fall gezielt in eine Kopie der erfundenen Testkurse ein, und auf dem Mac ist er ganz grün (8 von 8). Die Sorge, dass der Mac wegen anderer Bibliotheksfassungen den Gleichstand nicht trifft, hat sich nicht bestätigt. Mit der Sperre kommt das spätere Signal durch. Ohne die Sperre fehlt es, und sitzt die Sperre an der falschen Stelle, schlägt der Test an. Am Handelscode hat sich nichts geändert, und es lief nichts auf echten Kursdaten. Ob damit die offene Regel R106 (d) erledigt ist, entscheidet der Verfahrensprüfer.
