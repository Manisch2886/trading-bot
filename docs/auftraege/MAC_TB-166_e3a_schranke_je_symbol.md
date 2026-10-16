# TB-166 E-3a: Schranke je Symbol im Signalpfad und gemeinsame Tag-Rechnung (R90 (c)–(e), R98 (a)–(c)) — an: Mac-Sitzung (Claude Code)

**Stand: Entwurf vom 16.10.2026, 07:34** (Helfer BAU166, per Skript aus Bausteinen, `$HOME/sc/tb166/bau/bau.sh`), gebaut ausserhalb des Repos, nur lesend am Repo; an Kopien simuliert. Urteil und Freigabe beim steuernden Chat; danach liest ein frischer Gegenleser (W1). **Gebaut am HEAD `4a3d6cf`.**

**Sitzungstitel:** `TB-166` · **Modell:** Opus 5.5, Aufwand hoch · **Repo:** `Manisch2886/trading-bot`, `main` am HEAD `4a3d6cf9619fe5f2c6f79aa7284d79018366fb78` (kommt ein Commit dazu, baut der steuernde Chat neu) · **Start:** über den Sitzungswächter (`starte_TB-166`).
**Dieser Auftrag:** `docs/auftraege/MAC_TB-166_e3a_schranke_je_symbol.md` (in Schritt 0 mitcommittet). **Interpreter:** `trading-env/bin/python3 -B`, kurz `PY`; Werkzeug `docs/belege/TB-166/tb166_werkzeug.py` (Anhang D) kurz `WZ`. **Belege:** `docs/belege/TB-166/`, kurz `BEL`. **Ergebnis:** `docs/ERGEBNIS_TB-166_e3a_schranke_je_symbol.md`. **Journal:** nächste freie Kennung (`WZ kennung`; am Bau-HEAD FB ⇒ FC).
**Grundlage:** Plan `PLAN_E3` Teil E-3a (Zuschnitt in zwei Aufträge; E-3b Listen-Erzeuger folgt), Bestand `BESTAND_E3`, Register R90 (57.1), R98 (61.1, Z. 12210), 37.3. **Zeitgrenze:** jeder Bash-Aufruf mit `timeout` 600000 ms; jeder Befehl in einem eigenen Aufruf.
**Reihenfolge:** Schritt 0 ⇒ V ⇒ S (Vorab-Messung) ⇒ E (E-3a mit Tests) ⇒ A (Ergebnis mit Entwurf der Tatsachennotiz, BACKLOG, Journal, Abgabe). Kein Registereintrag in diesem Auftrag.

## Freigabe des Betreibers (R98 (c)) — Karte, wörtlich

> Karte des Betreibers im Chat 29 („Opus Trading Bots-15.10.2026 b“), 15.10.2026 ~22:35, Frage und Antwort im Wortlaut (aus logs/steuernder_chat/2026-10-15_BETREIBER_chat29_karten.md, per Skript): "TB-166 (E-3a, Schranke je Symbol): Es ändert 18 Dateien der Sperrliste, Punkte 9/11, und braucht deine Einzelfreigabe nach R98 (c). Darf ich den Auftrag heute Nacht senden, unter Bedingungen? Bedingungen: Der frische Gegenleser findet keinen A-Befund, alle Tests sind grün, und die Simulation ist gut. Es gibt keinen Lauf auf Kursdaten, kein Live, kein Geld; die Hashes alt/neu je Datei kommen ins Register."="Ja, bedingt freigeben (Recommended)"
>
> Bedingungen gemessen am 16.10.2026 vom steuernden Chat 30 („Opus Trading Bots-15.10.2026 c“): frischer Gegenleser GEGEN166 ohne A-Befund, Urteil sendefähig (Bericht md5 35a2deecad2d8328b77bd74cbfdd179f); neue Tests 11/11 und 47/47; Simulation 4/4 GUT; vier alte Tests (test_vorregistrierung, test_ersatzwerte, test_universum_trockenlauf, test_arbeitsbaum_laufbereich) am Gerät nicht belegt, am Mac vor dem Commit Pflicht. Karte des Betreibers dazu im Chat 30, 16.10.2026, Antwort im Wortlaut: „Ja, senden (Recommended)“. Erster Lauf 07:01 in 0a abgebrochen (6 statt 4 Einträge), nichts committet; Berichtigung BAU166B (nur 0a-Soll und Schritt 0), enger Gegenleser GEGEN166B ohne A-Befund (Bericht md5 d1badc7069fed9ba1a0946376fb03f7a).

R98 (c) (Register Z. 12210): „(c) Freigabe. Wird für die Schranke Code der Sperrliste geändert, genügt eine Freigabe des Betreibers je Bauauftrag für alle darin genannten Dateien, wenn sie jede Datei mit ihrem Sperrlistenpunkt und ihren Tests nennt (R31 (b), nach der Wiedergabe in 56.8 Nr. 8) und die Tatsachennotiz nach 37.3 je Datei alten und neuen Hash führt; ein neues Abbild unter neuem Namen schliesst den Befund. Eine Freigabe je Datei verlangt 37.3 nicht.“ R98 (d): „(d) Abnahme. Die Prüfung nach R90 (g) läuft am Erzeuger: für den Zellen-Erzeuger in der Abnahme nach R46, für den Listen-Erzeuger in der Probe nach R86 (d), je auf dem Test-Snapshot, geprüft an den Ausgaben des Erzeugers, mit der Gegenprobe über die Wache nach R87 (c); sie steht neben der Probe des Schnitts nach R86 (d), jede beisst allein (41.1 A5). Eine Prüfung unmittelbar am Signalpfad ist Handwerk daneben und ersetzt sie nicht.“ Regel 37.3 (Z. 7022): „**Ergänzung zu 36.2/36.6, Vorschlag:** Ein Befund 1 der Sperrlisten-Sonde **vor dem signierten Tag** ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein **neues Abbild unter neuem Namen** geschlossen, nie durch Anpassung des alten. Ein Befund 1 **nach dem Tag** ist ein Sperrlistenbruch und wird nach 10.1 behandelt (Amendment, Lauf von vorn). Das **letzte Abbild vor dem Tag** wird nach der letzten Codeänderung erzeugt, trägt die Hashes des Tag-Commits und steht selbst mit Hash im Register; der Tag setzt voraus, dass die Sonde gegen dieses Abbild 0 liefert (oder 2 mit Tatsachennotiz nach 22d).“ Sperrlistenpunkt 9 (Z. 1074): „9. **Kosten (0,30 %) und Fill-Konvention** — `TRADING_FEE_PCT = 0,1` und `SLIPPAGE_PCT = 0,05` je Order, Ein- und Ausstieg; Einstieg zum …“; Punkt 11 (Z. 1103): „11. **Commit-Hashes von Simulation, Erkennung, Optimierern und Auswertungsskript** — `herkunft.py::register()` und der Repo-Commit …“. Die Zuordnung je Datei ist erschlossen (PLAN_E3 2a; REGISTER_INDEX: Schranke = Punkte 9 und 11); das Abbild tb117 trägt an 9 nichts, an 11 nur `herkunft.py` — die Sonde meldet „nicht prüfbar“ (Bauart 50.3, Z. 11198).

## Die Dateien — jede mit Sperrlistenpunkt und Tests (R98 (c))

| Datei | Punkt | sha256 vorher | sha256 nachher (Bau) |
|---|---|---|---|
| `research/exposure_messung/bot_lauf.py` | — | `203d96203aa8e86a…` | `95e4c567680b1588…` |
| `research/faltenplan_neun/faltenschranke_messung.py` | — | `049bb657ff9d4f81…` | `5383f4ed41a86b7b…` |
| `strategies/elliott_wave/elliott_wave_counter.py` | 11 | `8209e503b2f979f8…` | `a57ab89413968aee…` |
| `strategies/elliott_wave/equity_simulation.py` | 11 | `f45e92cdac5a4f03…` | `79d0a611bc8b4cae…` |
| `strategies/elliott_wave/multi_symbol_optimise.py` | 11 | `ba3f5fdcf42537d5…` | `d470a8b3d877dcd9…` |
| `strategies/elliott_wave_stocks/elliott_wave_counter.py` | 11 | `ed97e0f1bfbcb8c1…` | `6ce7966f07d3bb33…` |
| `strategies/elliott_wave_stocks/equity_simulation.py` | 11 | `80ea2a331538bbe6…` | `1ebde5ec7c067e73…` |
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | 11 | `3b7757004b1c2db5…` | `4f1ed9c0f2d14937…` |
| `strategies/rsi2_crypto/backtest_rsi2.py` | 9/11 | `84930445e3494077…` | `8de8a3fe35c31624…` |
| `strategies/rsi2_crypto/equity_simulation.py` | 11 | `1406de58ad920116…` | `30d3b2873883a6a2…` |
| `strategies/rsi2_mean_reversion/backtest_rsi2.py` | 9/11 | `836b032a5962c776…` | `484a964c0b80c026…` |
| `strategies/t3_supertrend/backtest_trend.py` | 9/11 | `7a764353d092e521…` | `aade6aa8effc3fa9…` |
| `strategies/t3_supertrend/equity_simulation.py` | 11 | `0aed45b7e8d1a038…` | `2ffe378ff0b67efb…` |
| `strategies/t3_supertrend/multi_symbol_optimise.py` | 11 | `e314d7bf7bb35854…` | `af458d97fd77d805…` |
| `strategies/turtle_soup_crypto/backtest_turtle_soup.py` | 9/11 | `0704c9a96898ede9…` | `3f5faf8d3e00e9a9…` |
| `strategies/turtle_soup_crypto/equity_simulation.py` | 11 | `f0638e8e92ae9868…` | `836f985229284f70…` |
| `strategies/turtle_soup_stocks/backtest_turtle_soup.py` | 9/11 | `0de39bf20bbbd3c0…` | `b7922129a00d2917…` |
| `strategies/volatility_breakout/backtest_breakout.py` | 9/11 | `3fd0cef6c284a880…` | `feb8875d484513b0…` |
| `strategies/volatility_breakout_crypto/backtest_breakout.py` | 9/11 | `3c7ccbe792ea5eb8…` | `3743abd829843593…` |
| `strategies/volatility_breakout_crypto/equity_simulation.py` | 11 | `1109438768c00e10…` | `e16cf02297e2a616…` |

Volle Hashes im Werkzeug (`VOR`, `NACH`). Änderung allein über `WZ e3a` (Anhang C `e3a_patch.py`; jede Ersetzung genau einmal, sonst rc 2 und nichts geschrieben):
- `faltenschranke_messung.py`: neue `handelbar_ab(bot, schnitt=None)` — eine Rechnung des Handelbar-Tags je Symbol an der Reihe **ohne Zeilen ab dem Schnitt** (`faltenplan_neun.GO_LIVE`); Tag ≥ Schnitt ⇒ None (R87 (a), R90 (e)); `loader_lesart` ruft sie statt eigener Rechnung, `benchmark.je_bot` damit auch (unverändert).
- sechs `backtest_*.py`: der Filter nach dem Ausstieg wird **Wache** (Einstieg vor `entry_cutoff` ⇒ Abbruch mit 2), kein Streichen (R90 (d)); Scanbeginn bleibt.
- drei Krypto- und zwei Elliott-/eine T3-`equity_simulation.py`: `collect_all_trades(..., entry_cutoffs=None)` reicht den Cutoff je Symbol durch (R98 (b)); geladenes Symbol ohne Wert ⇒ 2 (R81 (c)).
- `elliott_wave_counter.py` (2×): `find_causal_waves(..., min_entry_idx=None)` — Welle vor dem Tag übergangen **vor** `traded.add` (kein Zustand); `multi_symbol_optimise.py` (2×) übersetzt `entry_cutoff` in den ersten Balken ≥ Tag.
- `t3_supertrend/backtest_trend.py`: `entry_cutoff=None`, Einstieg erst ab dem ersten Balken ≥ Tag (nur Zweig `position is None`); `multi_symbol_optimise.py` reicht durch.
- `research/exposure_messung/bot_lauf.py`: `hole_trades(es, all_data, handelbar=None)`; Cutoff je Symbol = späterer von Horizontbeginn und Handelbar-Tag (R98 (b) (i)); ohne `handelbar` die alte Bahn.
- **Nicht geändert:** `benchmark.py`, die vier Aktien-Lader, `positionen_holen.py`, `alle_bots.py` (E-3b).

Tests: die 11 alten Testdateien (Schritt E) und zwei neue (Anhang A, B): `research/faltenplan_neun/test_handelbar_tag.py` (Zeitspanne/Kerzen, Zeilen ab Schnitt ändern keinen Tag, Tag ≥ Schnitt ⇒ None, `loader_lesart` = `handelbar_ab`, Mutationsprobe); `shared/test_schranke_signalpfad.py` je Bot im eigenen Prozess: (1) alte Bahn byte-gleich zur Referenz aus dem unveränderten Stand, (2) kein Einstieg vor dem Cutoff, (3) Tag in einer alten Position ⇒ Einstieg ab dem Tag, (4) Indikatoren ungekürzt (Symbol ohne Signal vor dem Tag gleich mit/ohne Schranke), (5) Elliott: gesperrte Welle ohne `traded`-Rest, (6) Mutationsprobe in einer Kopie beisst je Bot. Nur synthetisch.

## Verboten

Kein Lauf eines Optimierers, Walk-Forward-Rechners, einer `equity_simulation` oder von `bot_lauf.py` auf Kursdaten; keine Rastersuche; keine Neuerzeugung der Listen; kein Registereintrag; kein neues Abbild; `positionen_holen.py` nie. `data/` liest nur `s0_vorab.py` (Schritt S, Zeitstempel je Zeile). **Schreiben darf die Sitzung nur:** die 20 Dateien (nur `WZ e3a`), die zwei neuen Tests, `BEL`, `docs/projektfuehrung/BACKLOG.md` (`WZ backlog`), `docs/projektfuehrung/JOURNAL.md` (`WZ journal`), das Ergebnis. Kein Netz, kein `pip`.

## Lage nach dem Auslegen

Beim Start genau 6 Einträge (Soll in 0a).

## Belegt · erschlossen · offen (am Bau)

**Belegt (Vorab-Messung am Gerät, `s0_vorab.py`, Wiederholung in Schritt S):**
```
Symbole je Bot: {'elliott_wave': 24, 't3_supertrend': 24, 'rsi2_crypto': 24, 'turtle_soup_crypto': 24, 'volatility_breakout_crypto': 24, 'elliott_wave_stocks': 150, 'rsi2_mean_reversion': 150, 'turtle_soup_stocks': 150, 'volatility_breakout': 150}
Dateien mit Zeilen ab Schnitt: 222 von 222 max 345
Abweichungen alt/neu: 30
FLIP t3_supertrend ENSOUSDT 2027-10-14 None
FLIP t3_supertrend TRUMPUSDT 2027-01-19 None
FLIP t3_supertrend PUMPUSDT 2027-09-11 None
FLIP t3_supertrend ZKCUSDT 2027-09-15 None
FLIP t3_supertrend UUSDT 2028-01-13 None
FLIP t3_supertrend BMTUSDT 2027-03-18 None
FLIP rsi2_crypto ENSOUSDT 2027-02-26 None
FLIP rsi2_crypto PUMPUSDT 2027-01-24 None
FLIP rsi2_crypto ZKCUSDT 2027-01-28 None
FLIP rsi2_crypto UUSDT 2027-05-28 None
FLIP turtle_soup_crypto ENSOUSDT 2027-02-26 None
FLIP turtle_soup_crypto PUMPUSDT 2027-01-24 None
FLIP turtle_soup_crypto ZKCUSDT 2027-01-28 None
FLIP turtle_soup_crypto UUSDT 2027-05-28 None
FLIP volatility_breakout_crypto ENSOUSDT 2027-02-26 None
FLIP volatility_breakout_crypto PUMPUSDT 2027-01-24 None
FLIP volatility_breakout_crypto ZKCUSDT 2027-01-28 None
FLIP volatility_breakout_crypto UUSDT 2027-05-28 None
FLIP elliott_wave_stocks GEV 2029-03-26 None
FLIP elliott_wave_stocks SNDK 2030-02-12 None
FLIP elliott_wave_stocks CEG 2027-01-18 None
FLIP rsi2_mean_reversion GEV 2029-03-26 None
FLIP rsi2_mean_reversion SNDK 2030-02-12 None
FLIP rsi2_mean_reversion CEG 2027-01-18 None
FLIP turtle_soup_stocks GEV 2029-03-26 None
FLIP turtle_soup_stocks SNDK 2030-02-12 None
FLIP turtle_soup_stocks CEG 2027-01-18 None
FLIP volatility_breakout GEV 2029-03-26 None
FLIP volatility_breakout SNDK 2030-02-12 None
FLIP volatility_breakout CEG 2027-01-18 None
alte Rechnung >= Schnitt: 30
```
**Erschlossen:** `benchmark_drawdowns.json` (Punkt 4) kann sich nicht ändern — alle 30 Wechsel lagen schon in der alten Rechnung am/nach dem Schnitt, hinter der letzten Falte (endet 2026-09-01 ausschl.); `tagesgenau` verwarf sie alt wie neu; `handelbar_ab` steht nicht in der Datei. **An einer Kopie (Python 3.10):** `test_handelbar_tag.py` 11/11, `test_schranke_signalpfad.py` 47/47; alte Tests vorher = nachher. **Offen, nur am Mac:** test_vorregistrierung, test_ersatzwerte, test_universum_trockenlauf (Laufzeit > 3 min am Gerät), test_arbeitsbaum_laufbereich (am Gerät K0 rc 2 vorher wie nachher, Umgebung); Python 3.9.

## Schritt 0 — Ausgang

**0a.** `git status --porcelain > "$TMPDIR/tb166_0a.txt"`, `git rev-parse HEAD`, `git rev-parse --abbrev-ref HEAD`. Soll: Zweig `main`, HEAD `4a3d6cf9619fe5f2c6f79aa7284d79018366fb78`, genau diese 6 Einträge, und die Freigabe-Karte oben ist gefüllt; sonst **ABBRUCH** (vor ⟨S0⟩).

```
 M docs/auftraege/AKTUELLER_AUFTRAG.md
 M docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
 M docs/projektfuehrung/UEBERGABE.md
?? docs/auftraege/MAC_TB-166_e3a_schranke_je_symbol.md
?? docs/projektfuehrung/FABLE_ANFRAGE_2026-10-15b_f4_wortlaut_sb1_paare_10a.md
?? docs/projektfuehrung/FABLE_ANTWORT_2026-10-15b_marken_tb150_etc_kein_ucits_korrelation_vor_pruefung.md
```

Anhänge holen (genau dieser Befehl):

```
trading-env/bin/python3 -B - docs/auftraege/MAC_TB-166_e3a_schranke_je_symbol.md "$TMPDIR" <<'EOF'
import hashlib, re, sys
t = open(sys.argv[1], encoding='utf-8').read(); n = 0
for name, inhalt in re.findall(r'<!-- DATEI (\S+) -->\n````python\n(.*?)````\n', t, re.S):
    open(sys.argv[2] + '/' + name, 'w', encoding='utf-8').write(inhalt); n += 1
    print(name, hashlib.sha256(inhalt.encode('utf-8')).hexdigest())
print('Dateien', n)
EOF
```

Soll: 5 Zeilen „<name> <sha256>“ mit genau diesen Werten, dann `Dateien 5`: `tb166_werkzeug.py` `685288bd1f0a106c4b3a9d383b202cd6aa288be54dc3587ace474053cb8d3ece`; `e3a_patch.py` `e7817c4883fd9b0b96a7c21c357f7b2e9343d5f415a9bf1e80e3fe8bab59dc8b`; `s0_vorab.py` `e3dcf85d5c12af1a5a91673914ceba53c0bd8516f5aaca4a8c7fb42cc8d63fac`; `test_handelbar_tag.py` `d90934f89a686c008bcb9e36ae8fac2ab76e9e2f564a51d19f659cd4acee23ce`; `test_schranke_signalpfad.py` `fc4581dc4486b34847d2c34ad5ef001af5c9136650db7ca0d42ba2fb74417c6f`; sonst **ABBRUCH**. Dann genau diese 6 `git add` (die 0a-Pfade mit Namen, darunter `docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md` und `docs/projektfuehrung/UEBERGABE.md` aus dem Umzug 15.10.2026, 23:14):

```
git add docs/auftraege/AKTUELLER_AUFTRAG.md
git add docs/projektfuehrung/EROEFFNUNG_STEUERNDER_CHAT.md
git add docs/projektfuehrung/UEBERGABE.md
git add docs/auftraege/MAC_TB-166_e3a_schranke_je_symbol.md
git add docs/projektfuehrung/FABLE_ANFRAGE_2026-10-15b_f4_wortlaut_sb1_paare_10a.md
git add docs/projektfuehrung/FABLE_ANTWORT_2026-10-15b_marken_tb150_etc_kein_ucits_korrelation_vor_pruefung.md
```

Commit `TB-166 Schritt 0: Stand des steuernden Chats vor TB-166 (EROEFFNUNG, UEBERGABE, Fable 15.10.b)`, pushen ⇒ **⟨S0⟩**. Dann `mkdir -p docs/belege/TB-166/`, `cp "$TMPDIR/tb166_0a.txt" docs/belege/TB-166/0a_status.txt` und:

```
cp "$TMPDIR/tb166_werkzeug.py" docs/belege/TB-166/tb166_werkzeug.py
cp "$TMPDIR/e3a_patch.py" docs/belege/TB-166/e3a_patch.py
cp "$TMPDIR/s0_vorab.py" docs/belege/TB-166/s0_vorab.py
```

## Schritt V — Voraussetzungen

`trading-env/bin/python3 -B docs/belege/TB-166/tb166_werkzeug.py voraussetzung > docs/belege/TB-166/v_voraussetzung.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/v_voraussetzung.txt` — Soll letzte Zeile `rc 0` (sha256 vorher aller 20 Dateien, Register endet mit 61, R98 genau einmal, neue Tests fehlen, TB-166 frei); sonst **ABBRUCH**.

## Schritt S — Vorab-Messung

`trading-env/bin/python3 -B docs/belege/TB-166/s0_vorab.py docs/belege/TB-166/s0_vorab.json > docs/belege/TB-166/s0_vorab.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/s0_vorab.txt` — Soll `rc 0` und dieselben Zeilen wie oben. Weicht die Liste ab (anderer Datenstand): kein Abbruch, im Ergebnis melden; liegt ein Wechsel **vor** dem Schnitt oder `alte Rechnung >= Schnitt` ≠ Zahl der Abweichungen: **ABBRUCH** (dann kann sich Punkt 4 ändern; Rückfrage). Commit `TB-166 S: Voraussetzungen und Vorab-Messung`, pushen ⇒ **⟨S⟩**.

```
git add docs/belege/TB-166/v_voraussetzung.txt
git add docs/belege/TB-166/s0_vorab.json
git add docs/belege/TB-166/s0_vorab.txt
```

## Schritt E — E-3a

```
cp "$TMPDIR/test_handelbar_tag.py" research/faltenplan_neun/test_handelbar_tag.py
cp "$TMPDIR/test_schranke_signalpfad.py" shared/test_schranke_signalpfad.py
trading-env/bin/python3 -B -W ignore shared/test_schranke_signalpfad.py --referenz-schreiben docs/belege/TB-166/e_ref_alt.json > docs/belege/TB-166/e_ref.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_ref.txt
trading-env/bin/python3 -B docs/belege/TB-166/tb166_werkzeug.py e3a --probe > docs/belege/TB-166/e_e3a_probe.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_e3a_probe.txt
trading-env/bin/python3 -B docs/belege/TB-166/tb166_werkzeug.py e3a > docs/belege/TB-166/e_e3a.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_e3a.txt
trading-env/bin/python3 -B -W ignore research/faltenplan_neun/test_handelbar_tag.py > docs/belege/TB-166/e_test_handelbar.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_test_handelbar.txt
trading-env/bin/python3 -B -W ignore shared/test_schranke_signalpfad.py --referenz docs/belege/TB-166/e_ref_alt.json > docs/belege/TB-166/e_test_schranke.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_test_schranke.txt
trading-env/bin/python3 -B -W ignore strategies/rsi2_mean_reversion/test_posten3_durchreichung.py > docs/belege/TB-166/e_alt_strategies_rsi2_mean_reversion_test_posten3_durchreichung.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_strategies_rsi2_mean_reversion_test_posten3_durchreichung.txt
trading-env/bin/python3 -B -W ignore strategies/volatility_breakout/test_posten3_durchreichung.py > docs/belege/TB-166/e_alt_strategies_volatility_breakout_test_posten3_durchreichung.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_strategies_volatility_breakout_test_posten3_durchreichung.txt
trading-env/bin/python3 -B -W ignore strategies/volatility_breakout_crypto/test_posten3_durchreichung.py > docs/belege/TB-166/e_alt_strategies_volatility_breakout_crypto_test_posten3_durchreichung.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_strategies_volatility_breakout_crypto_test_posten3_durchreichung.txt
trading-env/bin/python3 -B -W ignore research/faltenplan_neun/test_horizontbeginn.py > docs/belege/TB-166/e_alt_research_faltenplan_neun_test_horizontbeginn.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_research_faltenplan_neun_test_horizontbeginn.txt
trading-env/bin/python3 -B -W ignore research/faltenplan_neun/test_min_history.py > docs/belege/TB-166/e_alt_research_faltenplan_neun_test_min_history.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_research_faltenplan_neun_test_min_history.txt
trading-env/bin/python3 -B -W ignore research/vorregistrierung/test_vorregistrierung.py > docs/belege/TB-166/e_alt_research_vorregistrierung_test_vorregistrierung.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_research_vorregistrierung_test_vorregistrierung.txt
trading-env/bin/python3 -B -W ignore research/vorregistrierung/test_ersatzwerte.py > docs/belege/TB-166/e_alt_research_vorregistrierung_test_ersatzwerte.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_research_vorregistrierung_test_ersatzwerte.txt
trading-env/bin/python3 -B -W ignore shared/test_zuteilung.py > docs/belege/TB-166/e_alt_shared_test_zuteilung.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_shared_test_zuteilung.txt
trading-env/bin/python3 -B -W ignore shared/test_arbeitsbaum_laufbereich.py > docs/belege/TB-166/e_alt_shared_test_arbeitsbaum_laufbereich.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_shared_test_arbeitsbaum_laufbereich.txt
trading-env/bin/python3 -B -W ignore research/backtest_defaults/test_backtest_defaults.py > docs/belege/TB-166/e_alt_research_backtest_defaults_test_backtest_defaults.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_research_backtest_defaults_test_backtest_defaults.txt
trading-env/bin/python3 -B -W ignore research/universum_trockenlauf/test_universum_trockenlauf.py > docs/belege/TB-166/e_alt_research_universum_trockenlauf_test_universum_trockenlauf.txt 2>&1; echo "rc $?" >> docs/belege/TB-166/e_alt_research_universum_trockenlauf_test_universum_trockenlauf.txt
```

Reihenfolge bindend: die Referenz der alten Bahn entsteht **vor** `WZ e3a` am unveränderten Stand. Soll: jede Belegdatei endet mit `rc 0`; `e_test_handelbar.txt` „11 von 11“, `e_test_schranke.txt` „47 von 47“. **Endet `e_ref.txt`, `e_e3a_probe.txt`, `e_e3a.txt`, ein neuer oder ein alter Test nicht mit `rc 0`: ABBRUCH ohne Commit der 20 Dateien und der zwei Tests.** Sonst Commit `TB-166 E: E-3a Schranke je Symbol, handelbar_ab, Wache`, pushen ⇒ **⟨E⟩**; dann `trading-env/bin/python3 -B docs/belege/TB-166/tb166_werkzeug.py notiz ⟨E⟩ > docs/belege/TB-166/e_notiz.md`.

```
git add research/exposure_messung/bot_lauf.py
git add research/faltenplan_neun/faltenschranke_messung.py
git add strategies/elliott_wave/elliott_wave_counter.py
git add strategies/elliott_wave/equity_simulation.py
git add strategies/elliott_wave/multi_symbol_optimise.py
git add strategies/elliott_wave_stocks/elliott_wave_counter.py
git add strategies/elliott_wave_stocks/equity_simulation.py
git add strategies/elliott_wave_stocks/multi_symbol_optimise.py
git add strategies/rsi2_crypto/backtest_rsi2.py
git add strategies/rsi2_crypto/equity_simulation.py
git add strategies/rsi2_mean_reversion/backtest_rsi2.py
git add strategies/t3_supertrend/backtest_trend.py
git add strategies/t3_supertrend/equity_simulation.py
git add strategies/t3_supertrend/multi_symbol_optimise.py
git add strategies/turtle_soup_crypto/backtest_turtle_soup.py
git add strategies/turtle_soup_crypto/equity_simulation.py
git add strategies/turtle_soup_stocks/backtest_turtle_soup.py
git add strategies/volatility_breakout/backtest_breakout.py
git add strategies/volatility_breakout_crypto/backtest_breakout.py
git add strategies/volatility_breakout_crypto/equity_simulation.py
git add research/faltenplan_neun/test_handelbar_tag.py
git add shared/test_schranke_signalpfad.py
git add docs/belege/TB-166/e_ref_alt.json
git add docs/belege/TB-166/e_ref.txt
git add docs/belege/TB-166/e_e3a_probe.txt
git add docs/belege/TB-166/e_e3a.txt
git add docs/belege/TB-166/e_test_handelbar.txt
git add docs/belege/TB-166/e_test_schranke.txt
git add docs/belege/TB-166/e_alt_strategies_rsi2_mean_reversion_test_posten3_durchreichung.txt
git add docs/belege/TB-166/e_alt_strategies_volatility_breakout_test_posten3_durchreichung.txt
git add docs/belege/TB-166/e_alt_strategies_volatility_breakout_crypto_test_posten3_durchreichung.txt
git add docs/belege/TB-166/e_alt_research_faltenplan_neun_test_horizontbeginn.txt
git add docs/belege/TB-166/e_alt_research_faltenplan_neun_test_min_history.txt
git add docs/belege/TB-166/e_alt_research_vorregistrierung_test_vorregistrierung.txt
git add docs/belege/TB-166/e_alt_research_vorregistrierung_test_ersatzwerte.txt
git add docs/belege/TB-166/e_alt_shared_test_zuteilung.txt
git add docs/belege/TB-166/e_alt_shared_test_arbeitsbaum_laufbereich.txt
git add docs/belege/TB-166/e_alt_research_backtest_defaults_test_backtest_defaults.txt
git add docs/belege/TB-166/e_alt_research_universum_trockenlauf_test_universum_trockenlauf.txt
```

## Schritt A — Ergebnis, BACKLOG, Journal, Abgabe

`WZ kennung` (Soll „Kennung FC …“). `trading-env/bin/python3 -B docs/belege/TB-166/tb166_werkzeug.py backlog ⟨DATUM⟩ ⟨Kennung⟩ --probe`, dann ohne `--probe` (je `rc 0`). Block nach `docs/belege/TB-166/a_block.md` (erste Zeile `## ⟨Kennung⟩ — TB-166: …`, Quellenzeile, `**Quelle:**`, `### Was gemessen ist`, `### Was offen bleibt`, `### In einfacher Sprache`), `trading-env/bin/python3 -B docs/belege/TB-166/tb166_werkzeug.py journal docs/belege/TB-166/a_block.md --probe`, dann ohne. **Ergebnis** `docs/ERGEBNIS_TB-166_e3a_schranke_je_symbol.md`: Kopf mit Commits (⟨S0⟩ trägt die 6 0a-Pfade, darunter `EROEFFNUNG_STEUERNDER_CHAT.md` und `UEBERGABE.md`) · Kurz · `v_voraussetzung.txt` und `s0_vorab.txt` wörtlich · E: Testzeilen (letzte Zeile je Beleg) · **Entwurf Tatsachennotiz nach 37.3** = `e_notiz.md` wörtlich, Freigabe = Karte oben, mit dem Satz: „Die Abnahme nach R98 (d) erfolgt erst mit E-3b am Erzeuger.“ · **Offen:** Registereintrag (Folgeauftrag, wie TB-122 → 50.3), neues Abbild unter neuem Namen erst vor dem Tag, E-3b · Abweichungen · **In einfacher Sprache**. Commit `TB-166 Abgabe: Ergebnis, BACKLOG, Journal ⟨Kennung⟩`, pushen ⇒ **⟨F⟩**; dann `git status --porcelain > docs/belege/TB-166/f_porcelain.txt`, `git diff --numstat ⟨S0⟩ ⟨F⟩ > docs/belege/TB-166/f_numstat.txt`, Commit `TB-166 F: porcelain und numstat`, pushen.

## Abbruchkriterien — melden, nicht reparieren

0a weicht ab oder Karte leer; Holbefehl-Soll weicht ab; V, S (s. o.), E (s. o.), backlog/journal nicht `rc 0`; `git push` scheitert zweimal; Claude Code verlangt eine Bestätigung. **Abbruchweg:** vor ⟨S0⟩ nichts schreiben, nur melden. Danach `printf '%s\n' "<Schritt>: <Grund>" > docs/belege/TB-166/abbruch.txt` — in E nach `WZ e3a` mit zweiter Zeile wörtlich „Arbeitsbaum: die 20 Dateien bleiben geändert, die zwei neuen Tests unverfolgt (Abbruch in E nach WZ e3a).“ —, `git add` dieser Datei und jeder entstandenen Belegdatei unter `docs/belege/TB-166/` mit Namen (nie `-A`, nie `-f`, **nie** eine Datei unter `strategies/`, `research/` ausser `docs/belege/TB-166/`, `shared/`), Commit `TB-166 Abbruch: <Schritt>`, pushen, melden. Scheitert Commit oder Push des Abbruch-Commits: anhalten, melden. Nichts zurückdrehen.

## In einfacher Sprache

Die neun Bots dürfen ein Symbol erst handeln, wenn es „handelbar“ ist (genug Kursgeschichte). Bisher strichen sechs Bots zu frühe Trades erst hinterher, drei kannten gar keine Sperre. Jetzt rechnet eine einzige Funktion den Handelbar-Tag je Symbol, nur aus Daten vor dem 01.09.2026, und jeder Bot lässt im Scan vor diesem Tag keinen Einstieg zu; ein späteres Signal steigt normal ein. Geprüft wird mit erfundenen Kursreihen; kein Bot läuft auf echten Daten. Weil gesperrte Dateien geändert werden, gilt die Freigabe des Betreibers; alte und neue Prüfsummen stehen als Entwurf im Ergebnis. Abgenommen wird erst mit E-3b am Listen-Erzeuger.

## Anhänge

### Anhang A — `test_handelbar_tag.py` (sha256 `d90934f89a686c008bcb9e36ae8fac2ab76e9e2f564a51d19f659cd4acee23ce`)

<!-- DATEI test_handelbar_tag.py -->
````python
#!/usr/bin/env python3
"""TB-166 (E-3a; R87 (a)/(c), R90 (e)): faltenschranke_messung.handelbar_ab - EINE Rechnung des
Handelbar-Tags je Symbol, an der Reihe ohne Zeilen ab dem Schnitt. Synthetisch: Ersatzwurzel im
Temp-Ordner (TB36_BASE_DIR) mit eigenen Universen und Kursdateien; data/ wird nicht gelesen.
Aufruf aus der Repo-Wurzel: python3 -B research/faltenplan_neun/test_handelbar_tag.py  (rc 0 = alle bestanden)"""
import datetime as dt, os, shutil, subprocess, sys, tempfile
WURZEL = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
S = dt.date(2026, 9, 1)
KIND = r'''
import sys, json, datetime as dt
sys.path.insert(0, sys.argv[1]); import faltenschranke_messung as f
aus = {b: f.handelbar_ab(b) for b in ("elliott_wave", "rsi2_crypto", "t3_supertrend", "rsi2_mean_reversion")}
aus["lesart_gleich"] = {b: f.loader_lesart(b)["handelbar_ab"] == aus[b] for b in ("elliott_wave", "rsi2_crypto", "rsi2_mean_reversion")}
aus["ohne_schnitt"] = f.handelbar_ab("rsi2_crypto", schnitt=dt.date(2100, 1, 1))
print(json.dumps(aus))
'''
def baue(d, ab_schnitt):
    for b in ("elliott_wave", "rsi2_crypto", "t3_supertrend", "rsi2_mean_reversion"):
        os.makedirs(os.path.join(d, "strategies", b))
        shutil.copy(os.path.join(WURZEL, "strategies", b, "multi_symbol_optimise.py"), os.path.join(d, "strategies", b))
    os.makedirs(os.path.join(d, "config")); os.makedirs(os.path.join(d, "data"))
    open(os.path.join(d, "config", "top25_symbols.txt"), "w").write("AAA\nSPAET\nKURZ\n")
    open(os.path.join(d, "config", "sp500_top150.txt"), "w").write("XX\nFEHLT\n")
    def schreibe(name, start, schritt, n):
        z = ["open_time,open,high,low,close,volume"]; t = start
        while len(z) <= n:
            if ab_schnitt or t.date() < S: z.append("%s,1,1,1,1,1" % t.strftime("%Y-%m-%d %H:%M:%S"))
            elif not ab_schnitt: break
            t += schritt
        open(os.path.join(d, "data", name), "w").write("\n".join(z) + "\n")
    tag, std = dt.timedelta(days=1), dt.timedelta(hours=1)
    schreibe("AAA_1d.csv", dt.datetime(2020, 1, 1), tag, 2500)            # 500 Tage nach 2020-01-01: 2021-05-15
    schreibe("SPAET_1d.csv", dt.datetime(2025, 6, 1), tag, 600)           # +500 Tage = 2026-10-14 >= Schnitt -> None
    schreibe("KURZ_1d.csv", dt.datetime(2026, 8, 1), tag, 10)
    schreibe("AAA_4h.csv", dt.datetime(2023, 1, 1), dt.timedelta(hours=4), 8000)
    schreibe("AAA_1h.csv", dt.datetime(2023, 1, 1, 0), std, 19000)       # Luecke: Stunde 5 fehlt je Tag (23 Kerzen/Tag)
    p = os.path.join(d, "data", "AAA_1h.csv"); z = open(p).read().split("\n")
    open(p, "w").write("\n".join([z[0]] + [l for l in z[1:] if l and l[11:13] != "05"]) + "\n")
    schreibe("SPAET_1h.csv", dt.datetime(2025, 1, 1), std, 17600)
    schreibe("XX_1d.csv", dt.datetime(2015, 3, 2), tag, 4300)
def lauf(ab_schnitt, mutation=False):
    with tempfile.TemporaryDirectory() as d:
        baue(d, ab_schnitt)
        quelle = os.path.join(WURZEL, "research", "faltenplan_neun")
        if mutation:   # Mutation: der Schnitt wirkt nicht (Zeilen ab dem Schnitt zaehlen mit)
            m = os.path.join(d, "mut"); shutil.copytree(quelle, m)
            p = os.path.join(m, "faltenschranke_messung.py"); s = open(p).read()
            s = s.replace("if tag is None or tag >= schnitt:", "if tag is None:", 1).replace(" and t < schnitt else None", " else None", 1)
            open(p, "w").write(s); quelle = m
        env = dict(os.environ, TB36_BASE_DIR=d)
        r = subprocess.run([sys.executable, "-B", "-c", KIND, quelle], capture_output=True, text=True, env=env, cwd=WURZEL)
        if r.returncode != 0: return {"fehler": r.stderr.strip().split("\n")[-1][:200]}
        import json; return json.loads(r.stdout.strip().split("\n")[-1])
n = [0, 0]
def pruefe(name, ok, info=""):
    n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + name + (" · " + str(info) if info else ""))
a, b = lauf(True), lauf(False)
pruefe("Lauf ohne Fehler", "fehler" not in a and "fehler" not in b, a.get("fehler", "") or b.get("fehler", ""))
if "fehler" not in a and "fehler" not in b:
    pruefe("Zeitspanne: erster Kurstag + MIN_HISTORY_DAYS (rsi2_crypto AAA = 2021-05-15)", a["rsi2_crypto"]["AAA"] == "2021-05-15", a["rsi2_crypto"]["AAA"])
    pruefe("4h-Bot t3_supertrend: 2023-01-01 + 730 Tage = 2024-12-31", a["t3_supertrend"]["AAA"] == "2024-12-31", a["t3_supertrend"]["AAA"])
    pruefe("Kerzen: elliott_wave AAA = Datum der 17 520. Kerze trotz Luecken (2023-01-01 + 17519 // 23 = 761 Tage, nicht 730)", a["elliott_wave"]["AAA"] == (dt.date(2023, 1, 1) + dt.timedelta(days=17519 // 23)).isoformat(), a["elliott_wave"]["AAA"])
    pruefe("Tag >= Schnitt -> None (SPAET 1d, SPAET 1h, KURZ)", a["rsi2_crypto"]["SPAET"] is None and a["elliott_wave"]["SPAET"] is None and a["rsi2_crypto"]["KURZ"] is None)
    pruefe("Datei fehlt -> None (FEHLT)", a["rsi2_mean_reversion"]["FEHLT"] is None)
    pruefe("Aktien: XX = 2015-03-02 + 1825", a["rsi2_mean_reversion"]["XX"] == "2020-02-29", a["rsi2_mean_reversion"]["XX"])
    pruefe("Zeilen ab dem Schnitt aendern keinen Tag (mit gegen ohne Zeilen ab Schnitt)", all(a[k] == b[k] for k in ("elliott_wave", "rsi2_crypto", "t3_supertrend", "rsi2_mean_reversion")))
    pruefe("loader_lesart ruft dieselbe Rechnung (R90 (e))", all(a["lesart_gleich"].values()), a["lesart_gleich"])
    pruefe("Gegenprobe Schnitt 2100: SPAET bekommt einen Tag (der Schnitt beisst)", a["ohne_schnitt"]["SPAET"] == "2026-10-14", a["ohne_schnitt"]["SPAET"])
    m = lauf(True, mutation=True)
    pruefe("Mutationsprobe (Schnitt in handelbar_ab entfernt): Abweichung erkannt", "fehler" in m or m["elliott_wave"] != a["elliott_wave"] or m["rsi2_crypto"] != a["rsi2_crypto"])
print("%d von %d Pruefungen bestanden" % (n[1], n[0])); sys.exit(0 if n[0] == n[1] and n[0] > 0 else 1)
````

### Anhang B — `test_schranke_signalpfad.py` (sha256 `fc4581dc4486b34847d2c34ad5ef001af5c9136650db7ca0d42ba2fb74417c6f`)

<!-- DATEI test_schranke_signalpfad.py -->
````python
#!/usr/bin/env python3
"""TB-166 (E-3a; R90 (c), (d), (g), R98 (a), (b)): die Schranke im Signalpfad der neun Bots - synthetisch.
Je Bot ein Kindprozess: Zufallspfade im Temp-Ordner (DATA_DIR/SYMBOLS des Laders umgebogen), Trades ueber
research/exposure_messung/bot_lauf.hole_trades(es, all_data[, handelbar]). data/ wird nicht gelesen,
kein Optimierer-Lauf, keine Rastersuche.
  1  alte Bahn (ohne handelbar) byte-gleich zur Referenz aus dem unveraenderten Stand (--referenz-schreiben)
  2  kein Einstieg vor dem entry_cutoff des Symbols (spaeterer von Horizontbeginn und Handelbar-Tag)
  3  Tag mitten in einer alten Position: ein Signal ab dem Tag steigt ein, frueher als der alte naechste
     Einstieg (Positions-Bots); Elliott: alle alten Trades ab dem Tag bleiben, gesperrte Welle ohne Rest
  4  Indikatoren ungekuerzt: Symbol ohne Signal vor seinem Tag gleich mit und ohne Schranke
  5  Mutationsprobe in einer Kopie: Scanbeginn bzw. Scan-Schranke entfernt -> die Probe beisst
Aufruf aus der Repo-Wurzel: python3 -B shared/test_schranke_signalpfad.py [--referenz DATEI | --referenz-schreiben DATEI]"""
import hashlib, json, os, shutil, subprocess, sys, tempfile
WURZEL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOTS = ["rsi2_crypto", "turtle_soup_crypto", "volatility_breakout_crypto", "rsi2_mean_reversion", "turtle_soup_stocks",
        "volatility_breakout", "t3_supertrend", "elliott_wave", "elliott_wave_stocks"]
SECHS = BOTS[:6]
AKTIEN = ("rsi2_mean_reversion", "turtle_soup_stocks", "volatility_breakout", "elliott_wave_stocks")
def kind(bot, wurzel, modus):
    import numpy as np, pandas as pd
    sys.argv = ["bot_lauf", bot]; sys.path.insert(0, os.path.join(wurzel, "research", "exposure_messung"))
    import bot_lauf as bl; import equity_simulation as es; import multi_symbol_optimise as mso
    tf = {"elliott_wave": "1h", "t3_supertrend": "4h"}.get(bot, "1d")
    if bot in AKTIEN: t = pd.bdate_range("2008-01-02", "2026-08-31")
    else: t = pd.date_range({"1d": "2019-01-01", "4h": "2021-06-01", "1h": "2022-01-01"}[tf], "2026-08-31 23:00", freq=tf.replace("d", "D"))
    syms = ["AAA", "BBB", "CCC"] + ([] if bot in AKTIEN else ["BTCUSDT"]); d = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
    for k, s in enumerate(syms):
        r = np.random.default_rng(166 + k); v = {"1h": 0.012, "4h": 0.012}.get(tf, 0.025)
        c = 50 * np.exp(np.cumsum(r.normal(0.0001, v, len(t)))); o = c * (1 + r.normal(0, v / 5, len(t)))
        h = np.maximum(o, c) * (1 + np.abs(r.normal(0, v / 3, len(t)))); lo = np.minimum(o, c) * (1 - np.abs(r.normal(0, v / 3, len(t))))
        fmt = "%Y-%m-%d" if tf == "1d" else "%Y-%m-%d %H:%M:%S"
        pd.DataFrame({"open_time": t.strftime(fmt), "open": o, "high": h, "low": lo, "close": c, "volume": r.integers(10**5, 10**6, len(t))}).to_csv(os.path.join(d, "%s_%s.csv" % (s, getattr(mso, "INTERVAL", tf))), index=False)
    mso.DATA_DIR = d; mso.SYMBOLS = syms
    import io, contextlib
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        data = es.load_all_symbol_data()
    def lauf(handelbar=None):
        with contextlib.redirect_stdout(io.StringIO()):
            x = bl.hole_trades(es, dict(data)) if handelbar is None else bl.hole_trades(es, dict(data), handelbar)
        if x is None or x.empty: return pd.DataFrame(columns=["entry_time", "exit_time", "symbol"])
        x = x.copy(); x["entry_time"] = pd.to_datetime(x["entry_time"]); x["exit_time"] = pd.to_datetime(x["exit_time"])
        return x.reset_index(drop=True)
    alt = lauf()
    if modus == "referenz":
        print("REF " + json.dumps({"n": len(alt), "sha256": hashlib.sha256(alt.to_csv(index=False).encode()).hexdigest()})); return
    hb = pd.Timestamp("2016-09-19") if bot in AKTIEN else None
    erst = {s: (data[s][0] if isinstance(data[s], tuple) else data[s])["open_time"].min() for s in data}
    früh = {s: str(erst[s].date()) for s in data}
    n = [0, 0]
    def pruefe(name, ok, info=""):
        n[0] += 1; n[1] += bool(ok); print(("ja    " if ok else "NEIN  ") + bot + ": " + name + (" · " + str(info) if info else ""))
    if modus.startswith("ref="):
        ref = json.loads(open(modus[4:]).read())[bot]
        pruefe("1 alte Bahn ohne handelbar byte-gleich zum unveraenderten Stand", ref["sha256"] == hashlib.sha256(alt.to_csv(index=False).encode()).hexdigest(), "%d Trades" % len(alt))
    def schnitt(x, s): return x[x["symbol"] == s].reset_index(drop=True)
    def cut(tag): return tag if hb is None else max(hb, tag)
    # 3: Tag mitten in einer alten Position des Symbols mit den meisten alten Trades (S3)
    S3 = max(["AAA", "BBB"], key=lambda s: len(schnitt(alt, s))); b = schnitt(alt, S3); kand = []
    for _, z in b.iterrows():
        tag = z["entry_time"].normalize() + pd.Timedelta(days=1)
        if tag < z["exit_time"] and z["entry_time"] >= cut(pd.Timestamp("1900-01-01")): kand.append((tag, z["exit_time"]))
    gefunden, verletzt, geprueft = None, [], 0
    for tag, aus in kand[:12]:
        h = dict(früh); h[S3] = str(tag.date()); neu = lauf(h); geprueft += 1
        for s in data:
            c = cut(pd.Timestamp(h[s])); x = schnitt(neu, s)
            if len(x) and x["entry_time"].min() < c: verletzt.append((s, str(x["entry_time"].min()), str(c)))
        nb = schnitt(neu, S3); ab = b[b["entry_time"] >= tag]
        if bot.startswith("elliott"):
            alt_ab = set(map(tuple, ab[["entry_time", "exit_time"]].astype(str).values)); neu_m = set(map(tuple, nb[["entry_time", "exit_time"]].astype(str).values))
            if not alt_ab <= neu_m: verletzt.append((S3, "alter Trade ab Tag fehlt", str(tag)))
            if len(nb) and gefunden is None: gefunden = (S3, str(tag.date()), str(nb["entry_time"].min()), "%d alte Trades ab Tag erhalten" % len(ab))
        elif len(nb) and nb["entry_time"].min() >= tag and (bot == "t3_supertrend" or nb["entry_time"].min() <= aus) and gefunden is None:
            # t3_supertrend: Einstieg nur am Kreuzen nach oben, die alte Position endet am Kreuzen nach unten -
            # ein Einstieg vor ihrem Ende ist dort nicht moeglich; geprueft wird, dass ab dem Tag eingestiegen wird.
            gefunden = (S3, str(tag.date()), str(nb["entry_time"].min()), "alte Position bis " + str(aus))
        if gefunden and geprueft >= 3: break
    pruefe("2 kein Einstieg vor dem entry_cutoff je Symbol (%d Laeufe)" % geprueft, geprueft > 0 and not verletzt, verletzt[:2])
    pruefe("3 Tag in alter Position: ab dem Tag wird eingestiegen" + (" (Elliott: alte Trades ab Tag bleiben)" if bot.startswith("elliott") else (" (nach Kreuzen)" if bot == "t3_supertrend" else ", vor dem Ende der alten Position")), gefunden is not None, gefunden or "%d Kandidaten, %d alte Trades %s" % (len(kand), len(b), S3))
    # 4: CCC mit Tag am ersten alten Einstieg (kein Signal davor) -> gleich mit/ohne Schranke
    c0 = schnitt(alt, "CCC")
    if len(c0):
        h = dict(früh); h["CCC"] = str(c0["entry_time"].min().date()); neu = schnitt(lauf(h), "CCC")
        pruefe("4 Indikatoren ungekuerzt: CCC (Tag %s, kein Signal davor) gleich mit/ohne Schranke" % h["CCC"], neu.equals(c0), "%d/%d" % (len(neu), len(c0)))
    else:
        pruefe("4 CCC hat alte Trades", False)
    if bot.startswith("elliott"):   # 3b: gesperrte Welle ohne Rest (find_causal_waves direkt, freshness None)
        import elliott_wave_counter as ewc
        df = data[S3][0] if isinstance(data[S3], tuple) else data[S3]
        zz = mso.calculate_zigzag_with_confirmation(df, deviation_pct=getattr(es, "DEVIATION_PCT", 10.0))
        w0 = ewc.find_causal_waves(zz, min_fib_score=0.3, freshness_bars=None, direction="bearish"); ok = None
        for _, w in w0.iterrows():
            w1 = ewc.find_causal_waves(zz, min_fib_score=0.3, freshness_bars=None, direction="bearish", min_entry_idx=int(w["entry_idx"]) + 1)
            m = w1[w1["end_time"] == w["end_time"]]
            if len(m) == 1 and int(m["entry_idx"].iloc[0]) >= int(w["entry_idx"]) + 1: ok = (str(w["end_time"]), int(w["entry_idx"]), int(m["entry_idx"].iloc[0])); break
        pruefe("5 gesperrte Welle hinterlaesst keinen traded-Eintrag: sie steigt am ersten Lauf >= Schranke ein", ok is not None, ok)
    print("KIND %d %d" % tuple(n))
def mutiere(bot, ziel):
    for e in os.listdir(WURZEL):
        if e not in ("strategies", ".git"): os.symlink(os.path.join(WURZEL, e), os.path.join(ziel, e))
    os.makedirs(os.path.join(ziel, "strategies"))
    for b in os.listdir(os.path.join(WURZEL, "strategies")):
        q = os.path.join(WURZEL, "strategies", b)
        if b == bot: shutil.copytree(q, os.path.join(ziel, "strategies", b), ignore=shutil.ignore_patterns("__pycache__", "results"))
        else: os.symlink(q, os.path.join(ziel, "strategies", b))
    if bot in SECHS:
        p = [f for f in os.listdir(os.path.join(ziel, "strategies", bot)) if f.startswith("backtest_")][0]; alt = 'start_i = max(start_i, int((df["open_time"] < entry_cutoff).sum()))'; neu = "pass  # MUTATION: Scanbeginn aus"
    elif bot == "t3_supertrend": p, alt, neu = "backtest_trend.py", " and i >= erster_einstieg:", ":  # MUTATION"
    else: p, alt, neu = "elliott_wave_counter.py", "if min_entry_idx is not None and run_bar < min_entry_idx:\n                continue\n            traded.add(end_time)", "traded.add(end_time)\n            if min_entry_idx is not None and run_bar < min_entry_idx:  # MUTATION: nach traded.add\n                continue"
    f = os.path.join(ziel, "strategies", bot, p); s = open(f).read(); k = s.count(alt); open(f, "w").write(s.replace(alt, neu)); return k
if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "--kind":
        kind(sys.argv[2], sys.argv[3], sys.argv[4]); sys.exit(0)
    ref = sys.argv[2] if len(sys.argv) == 3 and sys.argv[1] in ("--referenz", "--referenz-schreiben") else None
    def starte(bot, wurzel, modus):
        return subprocess.run([sys.executable, "-B", "-W", "ignore", os.path.join(wurzel, "shared", "test_schranke_signalpfad.py"), "--kind", bot, wurzel, modus], capture_output=True, text=True, cwd=wurzel)
    if ref and sys.argv[1] == "--referenz-schreiben":
        aus = {}
        for b in BOTS:
            shutil.copy(os.path.abspath(__file__), os.path.join(WURZEL, "shared", "test_schranke_signalpfad.py")) if not os.path.exists(os.path.join(WURZEL, "shared", "test_schranke_signalpfad.py")) else None
            r = starte(b, WURZEL, "referenz"); z = [l for l in r.stdout.split("\n") if l.startswith("REF ")]
            if r.returncode or not z: print("NEIN  %s: Referenz rc %d %s" % (b, r.returncode, r.stderr.strip()[-200:])); sys.exit(1)
            aus[b] = json.loads(z[0][4:]); print("REF  %s %s" % (b, aus[b]))
        open(ref, "w").write(json.dumps(aus, indent=1, sort_keys=True) + "\n"); print("rc 0"); sys.exit(0)
    gesamt = [0, 0]
    for b in BOTS:
        r = starte(b, WURZEL, "ref=" + os.path.abspath(ref) if ref else "pruefen")
        print("\n".join(l for l in r.stdout.split("\n") if l.startswith(("ja ", "NEIN", "INFO"))))
        k = [l for l in r.stdout.split("\n") if l.startswith("KIND ")]
        if r.returncode or not k: print("NEIN  %s: Kindprozess rc %d: %s" % (b, r.returncode, r.stderr.strip()[-300:])); gesamt[0] += 1; continue
        a, ok = map(int, k[0].split()[1:]); gesamt[0] += a; gesamt[1] += ok
        with tempfile.TemporaryDirectory() as z:   # 5/6 Mutationsprobe in einer Kopie
            treffer = mutiere(b, z); m = starte(b, z, "pruefen")
            mk = [l for l in m.stdout.split("\n") if l.startswith("KIND ")]; beisst = m.returncode == 2 or (mk and mk[0].split()[1] != mk[0].split()[2]) or ("ABBRUCH (Wache R90 (d))" in m.stderr)
            wie = "Wache rc 2" if (m.returncode == 2 or "ABBRUCH (Wache" in m.stderr) else ("NEIN-Zeilen: " + "; ".join(l[6:90] for l in m.stdout.split("\n") if l.startswith("NEIN"))[:200])
            gesamt[0] += 1; gesamt[1] += bool(treffer == 1 and beisst)
            print(("ja    " if treffer == 1 and beisst else "NEIN  ") + "%s: 6 Mutationsprobe (%s) beisst · %s" % (b, "Scanbeginn aus" if b in SECHS else "Scan-Schranke aus/nach traded.add", wie))
    print("%d von %d Pruefungen bestanden" % (gesamt[1], gesamt[0])); sys.exit(0 if gesamt[0] == gesamt[1] and gesamt[0] > 0 else 1)
````

### Anhang C — `e3a_patch.py` (sha256 `e7817c4883fd9b0b96a7c21c357f7b2e9343d5f415a9bf1e80e3fe8bab59dc8b`)

<!-- DATEI e3a_patch.py -->
````python
"""TB-166 (E-3a) Werkzeugteil: aendert die 20 Dateien des Plans E-3a (PLAN_E3 2a) in einem Repo-Baum.
Aufruf: python3 -B e3a_patch.py <wurzel> [--probe]   --probe: nur pruefen, nichts schreiben.
Jede Ersetzung muss genau einmal treffen, sonst rc 2 und nichts geschrieben. Ausgabe: sha256 vorher/nachher je Datei."""
import hashlib, os, sys
W = sys.argv[1]; PROBE = "--probe" in sys.argv
FEHLER, NEU, VOR = [], {}, {}
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def lies(rel):
    if rel not in NEU:
        s = open(os.path.join(W, rel), encoding="utf-8").read(); VOR[rel] = sha(s); NEU[rel] = s
    return NEU[rel]
def ers(rel, alt, neu):
    s = lies(rel); k = s.count(alt)
    if k != 1: FEHLER.append("%s: %d Treffer fuer %r" % (rel, k, alt[:70])); return
    NEU[rel] = s.replace(alt, neu)
# --- 1 gemeinsame Tag-Rechnung (R90 (e)) -------------------------------------------------------
FSM = "research/faltenplan_neun/faltenschranke_messung.py"
HB = '''def handelbar_ab(bot: str, schnitt=None) -> dict:
    """TB-166 (E-3a; R87 (a)/(c), R90 (e), R98): der Handelbar-Tag je Symbol - EINE Rechnung
    fuer Wache, Benchmark (`benchmark.je_bot` ueber `loader_lesart`) und Schranke.

    Gerechnet an der Reihe OHNE Zeilen ab dem Schnitt (`schnitt`, Voreinstellung
    `faltenplan_neun.GO_LIVE`, ausschliesslich): Zeitspannen-Bots erster Kurstag +
    MIN_HISTORY_DAYS, Kerzen-Bot Datum der N-ten Kerze vor dem Schnitt. Ein Tag am oder
    nach dem Schnitt ist None - vor dem Schnitt nie handelbar. Fehlt die Datei: None.
    """
    schnitt = fp.GO_LIVE if schnitt is None else schnitt
    eig = fp.BOTS[bot]
    name, n = _min_history(bot)
    aus = {}
    for symbol in fp.symbole(eig["markt"]):
        pfad = fp.kursdatei(symbol, eig["zeitrahmen"])
        if not os.path.exists(pfad):
            aus[symbol] = None
            continue
        erster = nte = None
        zahl = 0
        with open(pfad, encoding="utf-8") as f:
            f.readline()
            for zeile in f:
                tag = fp._zeitstempel(zeile)
                if tag is None or tag >= schnitt:
                    continue
                if erster is None:
                    erster = tag
                zahl += 1
                if zahl == n:
                    nte = tag
        if name == "MIN_HISTORY_HOURS":
            t = nte
        else:
            t = None if erster is None else erster + dt.timedelta(days=n)
        aus[symbol] = t.isoformat() if t is not None and t < schnitt else None
    return aus


def loader_lesart(bot: str) -> dict:'''
ers(FSM, "def loader_lesart(bot: str) -> dict:", HB)
s = lies(FSM); a = s.index('    if name == "MIN_HISTORY_HOURS":\n        k = kerzen_elliott_wave()')
e_txt = '        aus["fensteranker"] = anker.isoformat() if anker else None\n'; e = s.index(e_txt, a) + len(e_txt)
NEU[FSM] = s[:a] + '''    # TB-166 (E-3a, R90 (e)): dieselbe Rechnung wie Wache und Schranke - an der Reihe
    # ohne Zeilen ab dem Schnitt; bis TB-166 rechnete hier eine eigene Schleife an der
    # ganzen Datei (Kerzen-Bot ueber kerzen_elliott_wave).
    aus["handelbar_ab"] = handelbar_ab(bot)
    if name != "MIN_HISTORY_HOURS":
        anker = fp.fensteranker(eig["markt"])
        aus["fensteranker"] = anker.isoformat() if anker else None
''' + s[e:]
# --- 2 sechs Backtests: Filter nach dem Ausstieg -> Wache (R90 (d)) -----------------------------
SECHS = ["strategies/rsi2_crypto/backtest_rsi2.py", "strategies/turtle_soup_crypto/backtest_turtle_soup.py",
         "strategies/volatility_breakout_crypto/backtest_breakout.py", "strategies/rsi2_mean_reversion/backtest_rsi2.py",
         "strategies/turtle_soup_stocks/backtest_turtle_soup.py", "strategies/volatility_breakout/backtest_breakout.py"]
FILTER = "        if entry_cutoff is None or entry_time >= np.datetime64(entry_cutoff):"
WACHE = '''        # TB-166 (E-3a, R90 (d)): Wache statt Streichen. Der Scan beginnt am ersten Balken
        # >= entry_cutoff (start_i oben); ein Einstieg davor ist ein Fehler im Signalpfad -
        # Abbruch mit Befund, kein Trade, der nach dem Ausstieg still entfaellt.
        if entry_cutoff is not None and entry_time < np.datetime64(entry_cutoff):
            sys.stderr.write("[%s] ABBRUCH (Wache R90 (d)): Einstieg %s vor entry_cutoff %s\\n"
                             % (__name__, entry_time, entry_cutoff))
            raise SystemExit(2)'''
for rel in SECHS:
    z = lies(rel).split("\n"); i = [k for k, l in enumerate(z) if l == FILTER]
    if len(i) != 1: FEHLER.append("%s: Filterzeile %d mal" % (rel, len(i))); continue
    i = i[0]; j = i + 1
    while j < len(z) and (z[j].strip() == "" or len(z[j]) - len(z[j].lstrip()) > 8): j += 1
    while z[j - 1].strip() == "": j -= 1
    NEU[rel] = "\n".join(z[:i] + WACHE.split("\n") + [l[4:] if l.strip() else l for l in z[i + 1:j]] + z[j:])
# --- 3 Durchreichung je Symbol (R98 (b)) ------------------------------------------------------
HELFER = '''
def _cutoff_je_symbol(entry_cutoffs, symbol):
    """TB-166 (E-3a, R98 (b)): entry_cutoff des Symbols aus `entry_cutoffs` ({symbol: Zeitpunkt},
    spaeterer von Horizontbeginn und Handelbar-Tag). Ohne `entry_cutoffs` None - die alte Bahn.
    Fehlt ein geladenes Symbol oder ist sein Wert None, hat es keinen Handelbar-Tag: Abbruch
    mit 2 (R81 (c)), kein stilles Weiterrechnen ohne Schranke."""
    if entry_cutoffs is None:
        return None
    wert = entry_cutoffs.get(symbol)
    if wert is None:
        sys.stderr.write("[equity_simulation] ABBRUCH: %s ohne entry_cutoff (kein Handelbar-Tag)\\n" % symbol)
        raise SystemExit(2)
    return wert

'''
EC = "entry_cutoff=_cutoff_je_symbol(entry_cutoffs, symbol)"
for rel, paare in {
    "strategies/rsi2_crypto/equity_simulation.py": [
        ("                        stop_loss_pct: float = None) -> pd.DataFrame:\n    all_trades = []",
         "                        stop_loss_pct: float = None, entry_cutoffs: dict = None) -> pd.DataFrame:\n    all_trades = []"),
        ("        trades = get_trades_for_symbol(price_df, rsi_threshold, sma_trend_period, stop_loss_pct)",
         "        trades = get_trades_for_symbol(price_df, rsi_threshold, sma_trend_period, stop_loss_pct,\n                                       " + EC + ")")],
    "strategies/turtle_soup_crypto/equity_simulation.py": [
        ("def collect_all_trades(all_data: dict, donchian_period: int, stop_mode=None) -> pd.DataFrame:",
         "def collect_all_trades(all_data: dict, donchian_period: int, stop_mode=None,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:"),
        ("        trades = get_trades_for_symbol(price_df, donchian_period, stop_mode)",
         "        trades = get_trades_for_symbol(price_df, donchian_period, stop_mode,\n                                       " + EC + ")")],
    "strategies/volatility_breakout_crypto/equity_simulation.py": [
        ("                        squeeze_percentile: float = BB_SQUEEZE_PERCENTILE) -> pd.DataFrame:\n    all_trades = []",
         "                        squeeze_percentile: float = BB_SQUEEZE_PERCENTILE,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:\n    all_trades = []"),
        ("                                       squeeze_percentile=squeeze_percentile)\n        if not trades.empty:",
         "                                       squeeze_percentile=squeeze_percentile,\n                                       " + EC + ")\n        if not trades.empty:")],
    "strategies/elliott_wave/equity_simulation.py": [
        ("                        stop_loss_pct: float, take_profit_fib: float) -> pd.DataFrame:",
         "                        stop_loss_pct: float, take_profit_fib: float,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:"),
        ("        trades = get_trades_for_symbol(price_df, deviation_pct)",
         "        trades = get_trades_for_symbol(price_df, deviation_pct, " + EC + ")")],
    "strategies/elliott_wave_stocks/equity_simulation.py": [
        ("                        take_profit_fib: float, use_take_profit: bool = True) -> pd.DataFrame:",
         "                        take_profit_fib: float, use_take_profit: bool = True,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:"),
        ("        trades = get_trades_for_symbol(price_df, deviation_pct, use_take_profit)",
         "        trades = get_trades_for_symbol(price_df, deviation_pct, use_take_profit,\n                                       " + EC + ")")],
    "strategies/t3_supertrend/equity_simulation.py": [
        ("                        adx_threshold: float, stop_loss_pct: float) -> pd.DataFrame:",
         "                        adx_threshold: float, stop_loss_pct: float,\n                        entry_cutoffs: dict = None) -> pd.DataFrame:"),
        ("        trades = get_trades_for_symbol(price_df, t3_fast, t3_slow, adx_threshold, stop_loss_pct)",
         "        trades = get_trades_for_symbol(price_df, t3_fast, t3_slow, adx_threshold, stop_loss_pct,\n                                       " + EC + ")")],
}.items():
    ers(rel, "\ndef collect_all_trades(", HELFER + "\ndef collect_all_trades(")
    for a, n in paare: ers(rel, a, n)
# --- 4 Schranke im Scan: Elliott (2x), T3 (R90 (c), R98 (a)) --------------------------------
for b in ("elliott_wave", "elliott_wave_stocks"):
    rel = "strategies/%s/elliott_wave_counter.py" % b
    ers(rel, '                       freshness_bars: int = None, direction: str = "bearish") -> pd.DataFrame:',
        '                       freshness_bars: int = None, direction: str = "bearish",\n                       min_entry_idx: int = None) -> pd.DataFrame:')
    ers(rel, "                continue\n            traded.add(end_time)",
        "                continue\n"
        "            # TB-166 (E-3a, R90 (c), R98 (a)): Schranke im Scan - vor dem Handelbar-Tag\n"
        "            # (min_entry_idx: erster Balken >= entry_cutoff) kein Einstieg. VOR traded.add: die\n"
        "            # gesperrte Welle hinterlaesst keinen Zustand und kann an einem spaeteren Lauf\n"
        "            # >= min_entry_idx (noch frisch) einsteigen.\n"
        "            if min_entry_idx is not None and run_bar < min_entry_idx:\n"
        "                continue\n            traded.add(end_time)")
    rel = "strategies/%s/multi_symbol_optimise.py" % b
    if b == "elliott_wave":
        ers(rel, "def get_trades_for_symbol(price_df: pd.DataFrame, deviation_pct: float) -> pd.DataFrame:",
            "def get_trades_for_symbol(price_df: pd.DataFrame, deviation_pct: float,\n                          entry_cutoff=None) -> pd.DataFrame:")
    else:
        ers(rel, "def get_trades_for_symbol(price_df: pd.DataFrame, deviation_pct: float, use_take_profit: bool = True) -> pd.DataFrame:",
            "def get_trades_for_symbol(price_df: pd.DataFrame, deviation_pct: float, use_take_profit: bool = True,\n                          entry_cutoff=None) -> pd.DataFrame:")
    ers(rel, '        direction="bearish")   # Long-only, wie zuvor festgelegt',
        '        direction="bearish",   # Long-only, wie zuvor festgelegt\n'
        '        # TB-166 (E-3a, R98 (a)/(b)): Schranke je Symbol - erster Balken >= entry_cutoff\n'
        '        min_entry_idx=(None if entry_cutoff is None\n'
        '                       else int((price_df["open_time"] < entry_cutoff).sum())))')
BT = "strategies/t3_supertrend/backtest_trend.py"
ers(BT, "stop_loss_pct=STOP_LOSS_PCT, use_t3_exit=True, use_vwap_filter=False) -> pd.DataFrame:",
    "stop_loss_pct=STOP_LOSS_PCT, use_t3_exit=True, use_vwap_filter=False,\n                  entry_cutoff=None) -> pd.DataFrame:")
ers(BT, "    trades = []\n    position = None  # None oder dict mit entry-Infos",
    "    # TB-166 (E-3a, R90 (c), R98 (a)): Schranke im Scan - ein Einstieg erst ab dem ersten\n"
    "    # Balken >= entry_cutoff; Indikatoren ueber die ganze Reihe; vor dem Tag entsteht keine\n"
    "    # Position, also kein Zustand, der ein spaeteres Signal sperrt.\n"
    "    erster_einstieg = 0 if entry_cutoff is None else int((data[\"open_time\"] < entry_cutoff).sum())\n\n"
    "    trades = []\n    position = None  # None oder dict mit entry-Infos")
ers(BT, "            if crossed_up and adx[i] > adx_threshold and vwap_ok:",
    "            if crossed_up and adx[i] > adx_threshold and vwap_ok and i >= erster_einstieg:")
MT = "strategies/t3_supertrend/multi_symbol_optimise.py"
ers(MT, "                           adx_threshold: float, stop_loss_pct: float) -> pd.DataFrame:\n    if t3_fast >= t3_slow:",
    "                           adx_threshold: float, stop_loss_pct: float,\n                           entry_cutoff=None) -> pd.DataFrame:\n    if t3_fast >= t3_slow:")
ers(MT, "        stop_loss_pct=stop_loss_pct,\n    )", "        stop_loss_pct=stop_loss_pct,\n        entry_cutoff=entry_cutoff,  # TB-166 (E-3a)\n    )")
# --- 5 Erzeuger-Seite: bot_lauf.hole_trades(..., handelbar=) ---------------------------------
BL = "research/exposure_messung/bot_lauf.py"
ers(BL, "\n\ndef hole_trades(es, all_data):", '''

def _schranke_je_symbol(all_data, handelbar):
    """TB-166 (E-3a, R90 (e), R98 (b) (i)): entry_cutoff je Symbol = spaeterer von Horizontbeginn
    und Handelbar-Tag (`handelbar`: {symbol: Tag} aus faltenschranke_messung.handelbar_ab).
    Aktien-Bots mit Tupel {symbol: (df, Horizontbeginn)}: Tupel (df, max(...)); sonst
    {symbol: df} und {"entry_cutoffs": {symbol: ...}} fuer collect_all_trades. Ein geladenes
    Symbol ohne Tag: Abbruch mit 2 (R81 (c)). Der Tag folgt der Zeitzone der Spalte open_time."""
    neu, cut = {}, {}
    for symbol, wert in all_data.items():
        df, alt = wert if isinstance(wert, tuple) else (wert, None)
        tag = handelbar.get(symbol)
        if tag is None:
            sys.stderr.write("[bot_lauf] ABBRUCH: %s (%s) geladen, aber ohne Handelbar-Tag (R81 (c))\\n" % (symbol, BOT))
            raise SystemExit(2)
        tag = pd.Timestamp(tag)
        tz = getattr(df["open_time"].dt, "tz", None)
        if tz is not None and tag.tzinfo is None:
            tag = tag.tz_localize(tz)
        if BOT == "elliott_wave_stocks":
            import multi_symbol_optimise as mso   # Zeilen am Horizontbeginn gekappt (TB-163)
            alt = mso.horizontbeginn_ts(df["open_time"])
        c = tag if alt is None else max(alt, tag)
        if isinstance(wert, tuple):
            neu[symbol] = (df, c)
        else:
            neu[symbol] = df
            cut[symbol] = c
    return neu, ({"entry_cutoffs": cut} if cut else {})


def hole_trades(es, all_data, handelbar=None):''')
ers(BL, "    anwendet (`apply_btc_regime_filter`, eigener Kommentarblock dort).\"\"\"\n",
    "    anwendet (`apply_btc_regime_filter`, eigener Kommentarblock dort).\n\n"
    "    TB-166 (E-3a): mit `handelbar` traegt jeder Bot die Schranke je Symbol\n"
    "    (`_schranke_je_symbol`); ohne `handelbar` die alte Bahn, unveraendert.\"\"\"\n"
    "    kw = {}\n    if handelbar is not None:\n        all_data, kw = _schranke_je_symbol(all_data, handelbar)\n")
for a in ["es.TAKE_PROFIT_FIB)\n    if BOT == \"elliott_wave_stocks\":", "es.TAKE_PROFIT_FIB, es.USE_TAKE_PROFIT)",
          "es.ADX_THRESHOLD, es.STOP_LOSS_PCT)", "es.SMA_TREND_PERIOD,\n                                      es.STOP_LOSS_PCT)",
          "es.collect_all_trades(all_data, es.DONCHIAN_PERIOD, es.STOP_MODE)", "trades = es.collect_all_trades(all_data, es.STOP_LOSS_PCT)",
          "es.collect_all_trades(all_data, es.RSI_THRESHOLD, es.STOP_LOSS_PCT)", "return es.collect_all_trades(all_data, es.STOP_LOSS_PCT)"]:
    k = a.index(")"); ers(BL, a, a[:k] + ", **kw" + a[k:])
# --- Ende ------------------------------------------------------------------------------------
if FEHLER:
    print("\n".join("FEHLER " + f for f in FEHLER)); print("rc 2"); sys.exit(2)
for rel in sorted(NEU):
    if not PROBE:
        with open(os.path.join(W, rel), "w", encoding="utf-8") as f: f.write(NEU[rel])
    print("%s  vorher %s  nachher %s" % (rel, VOR[rel], sha(NEU[rel])))
print("Dateien: %d%s" % (len(NEU), " (Probe, nichts geschrieben)" if PROBE else "")); print("rc 0")
````

### Anhang D — `tb166_werkzeug.py` (sha256 `685288bd1f0a106c4b3a9d383b202cd6aa288be54dc3587ace474053cb8d3ece`)

<!-- DATEI tb166_werkzeug.py -->
````python
#!/usr/bin/env python3
"""TB-166 Werkzeug (Anhang D): Voraussetzungen, E-3a (20 Dateien ueber e3a_patch.py), Entwurf Tatsachennotiz nach 37.3, BACKLOG, Journal.
Stdlib, Python 3.9, Aufruf aus der Repo-Wurzel. --probe schreibt nichts. Rueckgabe: 0 gut, 1 Pruefung NEIN, 2 Aufruf falsch.
  voraussetzung | e3a [--probe] | notiz <E> | kennung | backlog <DATUM> <KENNUNG> [--probe] | journal <BLOCK> [--probe]"""
import hashlib, os, re, subprocess, sys
REG, BL, JO = "docs/VORREGISTRIERUNG_neuselektion.md", "docs/projektfuehrung/BACKLOG.md", "docs/projektfuehrung/JOURNAL.md"
BEL = "docs/belege/TB-166/"
PUNKT = {"research/exposure_messung/bot_lauf.py": "\u2014", "research/faltenplan_neun/faltenschranke_messung.py": "\u2014", "strategies/elliott_wave/elliott_wave_counter.py": "11", "strategies/elliott_wave/equity_simulation.py": "11", "strategies/elliott_wave/multi_symbol_optimise.py": "11", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "11", "strategies/elliott_wave_stocks/equity_simulation.py": "11", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "11", "strategies/rsi2_crypto/backtest_rsi2.py": "9/11", "strategies/rsi2_crypto/equity_simulation.py": "11", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "9/11", "strategies/t3_supertrend/backtest_trend.py": "9/11", "strategies/t3_supertrend/equity_simulation.py": "11", "strategies/t3_supertrend/multi_symbol_optimise.py": "11", "strategies/turtle_soup_crypto/backtest_turtle_soup.py": "9/11", "strategies/turtle_soup_crypto/equity_simulation.py": "11", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "9/11", "strategies/volatility_breakout/backtest_breakout.py": "9/11", "strategies/volatility_breakout_crypto/backtest_breakout.py": "9/11", "strategies/volatility_breakout_crypto/equity_simulation.py": "11"}
VOR = {"research/exposure_messung/bot_lauf.py": "203d96203aa8e86a32610bbae40fcca911554f56a98b971f5cc8c475c766f50a", "research/faltenplan_neun/faltenschranke_messung.py": "049bb657ff9d4f81e8fcfda94559d4e40668bcca7a76bc07488dce80510cf91b", "strategies/elliott_wave/elliott_wave_counter.py": "8209e503b2f979f8900f49d458ff538009c2da94bb86240cce710f3870fb66fe", "strategies/elliott_wave/equity_simulation.py": "f45e92cdac5a4f03d3bd2f10165034d27b20603846e3072d02a7baf807cd127b", "strategies/elliott_wave/multi_symbol_optimise.py": "ba3f5fdcf42537d586144174401c6dbf1e93a1f62476083fb3184028c3b2ce6c", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "ed97e0f1bfbcb8c1fe5676b64f5d8a4cbdaf8be8448062616edfe20bdda62cbf", "strategies/elliott_wave_stocks/equity_simulation.py": "80ea2a331538bbe6270a97c03627c3393c56848bfff00d9a9d44024fc0768a21", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232", "strategies/rsi2_crypto/backtest_rsi2.py": "84930445e34940775f6fcc6715616eb77589fc960f988a19b26199f1393e1aca", "strategies/rsi2_crypto/equity_simulation.py": "1406de58ad920116d15a08384b88b78d37ee4944c925ff36fddedd123963e9ab", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "836b032a5962c7766e7ed00a75b90ded4155b769fce54a84fead3c4cd5f3b7fc", "strategies/t3_supertrend/backtest_trend.py": "7a764353d092e521cc24b80ae97193d624224b38a6a62a45394360fe50cb04bb", "strategies/t3_supertrend/equity_simulation.py": "0aed45b7e8d1a0386c381fc462f96233723ff9036e863e70741e2c224fc6ef1b", "strategies/t3_supertrend/multi_symbol_optimise.py": "e314d7bf7bb35854c9280a5b51362f2c8a6c33771a06188a14afee7c8ff39f14", "strategies/turtle_soup_crypto/backtest_turtle_soup.py": "0704c9a96898ede99e9cf2b153da33d0cb885bf16c89e642d8514f277e8a0089", "strategies/turtle_soup_crypto/equity_simulation.py": "f0638e8e92ae98683385ea3082fbc8c56db4bc74631001c147eef54f70d7ea03", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "0de39bf20bbbd3c0988b270262728a08cddc79a448fd0300c2f6b94998df50bb", "strategies/volatility_breakout/backtest_breakout.py": "3fd0cef6c284a8806cace3663c241295edbb1ef8ee79092abfd0dc55e2bf6a76", "strategies/volatility_breakout_crypto/backtest_breakout.py": "3c7ccbe792ea5eb8dcbc76ae27079f4d7c47ca34bd3ad5edd332d4fdad3c403e", "strategies/volatility_breakout_crypto/equity_simulation.py": "1109438768c00e10710740775a30de8f3ac9f4309e24b3c54b13266d07df9fad"}
NACH = {"research/exposure_messung/bot_lauf.py": "95e4c567680b15889b1d80b6827dcbac6cdde8de639767eb7521546dc2876e71", "research/faltenplan_neun/faltenschranke_messung.py": "5383f4ed41a86b7bc0e3ba15c51adf96520bb1e54d58507f2503cab70301572f", "strategies/elliott_wave/elliott_wave_counter.py": "a57ab89413968aee9dbe5f256f44e0dde11131cb373b357de0da2d4c9a57a3a1", "strategies/elliott_wave/equity_simulation.py": "79d0a611bc8b4caed00db798e625f71e46b551af5e70a194323933d7b103ba00", "strategies/elliott_wave/multi_symbol_optimise.py": "d470a8b3d877dcd91b9e33ea40ba390e19200a4923140b54a532a561b5d9d209", "strategies/elliott_wave_stocks/elliott_wave_counter.py": "6ce7966f07d3bb3348f0f6ab1d335a547707da088010c740a0427b5a312755e5", "strategies/elliott_wave_stocks/equity_simulation.py": "1ebde5ec7c067e73639c00495d481c09f130ebec23e51c3e90a3f79ea447dd5b", "strategies/elliott_wave_stocks/multi_symbol_optimise.py": "4f1ed9c0f2d149377be3568b016adec33d1f452eec43dd3aae63cbc102da1829", "strategies/rsi2_crypto/backtest_rsi2.py": "8de8a3fe35c31624d2a85495f9d73cf88a08d537fd0c22b3e889e55e09266691", "strategies/rsi2_crypto/equity_simulation.py": "30d3b2873883a6a2b2dc09e72d01bbd6b0db82551a745882481e1fec810c0b5a", "strategies/rsi2_mean_reversion/backtest_rsi2.py": "484a964c0b80c0260d81e0a49195466f4f3d6aab1c0121a8abbd6cca840cc10b", "strategies/t3_supertrend/backtest_trend.py": "aade6aa8effc3fa9e095e8b57d6059ffb51d12091bbfa03dc937ab4f7c31797e", "strategies/t3_supertrend/equity_simulation.py": "2ffe378ff0b67efb63490f70a1bfae384044d096da40825788568e37db0c970a", "strategies/t3_supertrend/multi_symbol_optimise.py": "af458d97fd77d8057e292f500e8b9c7584d93bccc8d43274a0b541a6f35932cb", "strategies/turtle_soup_crypto/backtest_turtle_soup.py": "3f5faf8d3e00e9a92e6d61caa7684513343c99972693c497cf1cadf539e2ab3f", "strategies/turtle_soup_crypto/equity_simulation.py": "836f985229284f703a9a915434a60fa8b24579e63ddca9a303e8c3fd9c43237f", "strategies/turtle_soup_stocks/backtest_turtle_soup.py": "b7922129a00d2917d1d0750fb796f3e939e075c9f95cf5988b1849f8bb05b0f2", "strategies/volatility_breakout/backtest_breakout.py": "feb8875d484513b0289f563aee964387063b0cc413be612db43e2b3e8b0931fd", "strategies/volatility_breakout_crypto/backtest_breakout.py": "3743abd82984359328b125f9c3c221fe5d0e70ef5f2a2b066a6f40879df1b30c", "strategies/volatility_breakout_crypto/equity_simulation.py": "e16cf02297e2a6161307c4d398b3ac73db3db6fa249afa06185ead1b6e9bdc62"}
NEU = ["research/faltenplan_neun/test_handelbar_tag.py", "shared/test_schranke_signalpfad.py"]
OUT = []
def p(ok, t): OUT.append(("ja    " if ok else "NEIN  ") + t); return ok
def lies(f): return open(f, encoding="utf-8").read()
def sha(f): return hashlib.sha256(open(f, "rb").read()).hexdigest()
def ende():
    n = sum(l.startswith("NEIN") for l in OUT); print("\n".join(OUT)); print("Pruefungen: %d, NEIN: %d" % (len(OUT), n)); print("rc %d" % (1 if n else 0)); sys.exit(1 if n else 0)
def voraussetzung():
    for f in sorted(VOR): p(os.path.exists(f) and sha(f) == VOR[f], "sha256 vorher %s" % f)
    r = lies(REG); z = r.split("\n")
    p(any(l.startswith("## 61. ") for l in z) and not any(l.startswith("## 62. ") for l in z), "Register endet mit 61, 62 fehlt")
    p(r.count("> R98 — Ergänzung zu R90 (c), (f) und (g)") == 1, "R98 genau einmal im Register")
    for f in NEU: p(not os.path.exists(f), "%s noch nicht da" % f)
    p("TB-166" not in lies(BL) and "TB-166" not in lies(JO), "TB-166 weder in BACKLOG noch in JOURNAL")
    ende()
def e3a(probe):
    r = subprocess.run([sys.executable, "-B", BEL + "e3a_patch.py", "."] + (["--probe"] if probe else []), capture_output=True, text=True)
    print(r.stdout.rstrip()); p(r.returncode == 0, "e3a_patch.py rc %d" % r.returncode)
    for l in r.stdout.split("\n"):
        m = re.match(r"(\S+)  vorher ([0-9a-f]{64})  nachher ([0-9a-f]{64})$", l)
        if m: p(VOR.get(m.group(1)) == m.group(2) and NACH.get(m.group(1)) == m.group(3), "%s vorher/nachher wie im Bau" % m.group(1))
    p(sum(1 for l in OUT if " vorher/nachher " in l) == len(VOR), "alle %d Dateien" % len(VOR))
    if not probe:
        for f in sorted(NACH): p(sha(f) == NACH[f], "auf der Platte nachher %s" % f)
    ende()
def notiz(e):
    if not re.fullmatch(r"[0-9a-f]{7}", e): sys.exit(2)
    z = ["**Hash-Übergänge nach 37.3** (R98 (c): eine Freigabe je Bauauftrag; Sperrlistenpunkte 9/11) — Entwurf, nicht eingetragen; volle Hashes (39.5):", "",
         "| Datei | Punkt | vorher | nachher | Commit | vollzieht |", "|---|---|---|---|---|---|"]
    for f in sorted(VOR): z.append("| `%s` | %s | `%s` | `%s` | `%s` | E-3a (R90 (c)–(e), R98 (a), (b)) |" % (f, PUNKT[f], VOR[f], sha(f), e))
    z += ["", "Neu (kein Vorher), Commit `%s`: " % e + ", ".join("`%s` `%s`" % (f, sha(f)) for f in NEU) + ".",
          "Abnahme: nach R98 (d) erst mit E-3b am Listen-Erzeuger (Probe nach R86 (d) mit Gegenprobe über die Wache nach R87 (c)); die Prüfung am Signalpfad in diesem Auftrag ist Handwerk daneben und ersetzt sie nicht.",
          "Abbild: ein neues Abbild unter neuem Namen schliesst den Befund (37.3; Bauart 50.3) — erst vor dem Tag, nicht in diesem Auftrag.",
          "Vorab gemessen (`docs/belege/TB-166/s0_vorab.txt`): 30 Symbole wechseln von einem Handelbar-Tag am oder nach dem Schnitt auf None, keines liegt vor dem Schnitt; `benchmark_drawdowns.json` (Punkt 4) bleibt unberührt (letzte Falte endet am Schnitt; `handelbar_ab` steht nicht in der Datei)."]
    print("\n".join(z))
def kennung():
    k = re.findall(r"^## ([A-Z]{2}) — TB-", lies(JO), re.M); h = max(k)
    n = h[0] + chr(ord(h[1]) + 1) if h[1] != "Z" else chr(ord(h[0]) + 1) + "A"; print("Kennung %s (letzte %s)" % (n, h)); return n
def backlog(datum, kenn, probe):
    if not re.fullmatch(r"\d\d\.\d\d\.\d{4}", datum) or not re.fullmatch(r"[A-Z]{2}", kenn): sys.exit(2)
    z = lies(BL).split("\n"); a = [i for i, l in enumerate(z) if l.startswith("| **1** | **TB-30b Mass-Reparatur**")]
    if p(len(a) == 1 and z[a[0]].endswith("mit der Messung nach R98 (b) |"), "BACKLOG Rang 1 genau einmal, endet mit 'R98 (b) |'"):
        z[a[0]] = z[a[0]][:-2] + " · E-3a (Schranke je Symbol, gemeinsame Tag-Rechnung `handelbar_ab`, Wache statt Filter; 20 Dateien, 18 auf der Sperrliste) gebaut mit TB-166 (%s, Journal %s); Abnahme nach R98 (d) mit E-3b, Tatsachennotiz 37.3 als Entwurf im Ergebnis |" % (datum, kenn)
    if not probe and not any(l.startswith("NEIN") for l in OUT): open(BL, "w", encoding="utf-8").write("\n".join(z))
    ende()
def journal(block, probe):
    t = lies(block); z = lies(JO).split("\n"); neu = kennung(); b = t.rstrip("\n").split("\n"); i = [n for n, l in enumerate(z) if l == "## Wiederkehrende Lehren"]
    p(b[0].startswith("## %s — TB-166: " % neu), "Kopfzeile ## %s — TB-166: …" % neu); p(len(i) == 1 and z[i[0] - 1] == "" and z[i[0] - 2] == "---", "Anker genau einmal, davor '---' und Leerzeile")
    p(sum(l.startswith("## ") for l in b) == 1 and "---" not in b, "eine ## -Zeile, kein ---"); p("### Was gemessen ist" in b and "### In einfacher Sprache" in b, "Teile vorhanden")
    if not probe and not any(l.startswith("NEIN") for l in OUT): z[i[0] - 2:i[0] - 2] = b + [""]; open(JO, "w", encoding="utf-8").write("\n".join(z))
    ende()
if __name__ == "__main__":
    a = sys.argv[1:]; pr = "--probe" in a; a = [x for x in a if x != "--probe"]
    if a == ["voraussetzung"]: voraussetzung()
    elif a == ["e3a"]: e3a(pr)
    elif len(a) == 2 and a[0] == "notiz": notiz(a[1])
    elif a == ["kennung"]: kennung()
    elif len(a) == 3 and a[0] == "backlog": backlog(a[1], a[2], pr)
    elif len(a) == 2 and a[0] == "journal": journal(a[1], pr)
    else: print(__doc__); sys.exit(2)
````

### Anhang E — `s0_vorab.py` (sha256 `e3dcf85d5c12af1a5a91673914ceba53c0bd8516f5aaca4a8c7fb42cc8d63fac`)

<!-- DATEI s0_vorab.py -->
````python
"""TB-166 Vorab-Messung (S); Aufruf: python3 -B s0_vorab.py <ausgabe.json> (aus der Repo-Wurzel)
: Handelbar-Tag je Bot und Symbol, alte Rechnung
(ganze Datei, loader_lesart) gegen neue (nur Zeilen < Schnitt, Tag >= Schnitt -> None).
Eigenes Skript, stdlib, liest nur data/ und config/ des Repos."""
import datetime as dt, json, os, sys, hashlib
R = os.getcwd()  # Aufruf aus der Repo-Wurzel
SCHNITT = dt.date(2026, 9, 1)
BOTS = {"elliott_wave": ("krypto", "1h", "H", 17520), "t3_supertrend": ("krypto", "4h", "D", 730),
        "rsi2_crypto": ("krypto", "1d", "D", 500), "turtle_soup_crypto": ("krypto", "1d", "D", 500),
        "volatility_breakout_crypto": ("krypto", "1d", "D", 500), "elliott_wave_stocks": ("aktien", "1d", "D", 1825),
        "rsi2_mean_reversion": ("aktien", "1d", "D", 1825), "turtle_soup_stocks": ("aktien", "1d", "D", 1825),
        "volatility_breakout": ("aktien", "1d", "D", 1825)}
UNI = {"krypto": "config/top25_symbols.txt", "aktien": "config/sp500_top150.txt"}
def syms(m):
    l = [z.strip() for z in open(os.path.join(R, UNI[m])) if z.strip()]
    return [s for s in l if s not in ("XAUTUSDT", "PAXGUSDT")] if m == "krypto" else l
def tage(p):
    with open(p) as f:
        f.readline()
        for z in f:
            z = z.strip()
            if z: yield dt.date.fromisoformat(z.split(",")[0][:10])
aus = {}; flips = []; zeilen_ab = {}
for bot, (m, tf, art, n) in BOTS.items():
    aus[bot] = {}
    for s in syms(m):
        p = os.path.join(R, "data", f"{s}_{tf}.csv")
        if not os.path.exists(p): aus[bot][s] = {"alt": None, "neu": None, "datei": "fehlt"}; continue
        alle = list(tage(p)); vor = [t for t in alle if t < SCHNITT]
        zeilen_ab[f"{s}_{tf}"] = len(alle) - len(vor)
        if art == "H":
            alt = alle[n - 1] if len(alle) >= n else None
            neu = vor[n - 1] if len(vor) >= n else None
        else:
            alt = (alle[0] + dt.timedelta(days=n)) if alle else None
            neu = (vor[0] + dt.timedelta(days=n)) if vor else None
        if neu is not None and neu >= SCHNITT: neu = None
        a = alt.isoformat() if alt else None; b = neu.isoformat() if neu else None
        aus[bot][s] = {"alt": a, "neu": b}
        if a != b: flips.append((bot, s, a, b))
json.dump({"schnitt": str(SCHNITT), "je_bot": aus, "zeilen_ab_schnitt": zeilen_ab}, open(sys.argv[1], "w"), indent=1, sort_keys=True)
print("Symbole je Bot:", {b: len(v) for b, v in aus.items()})
print("Dateien mit Zeilen ab Schnitt:", sum(1 for v in zeilen_ab.values() if v), "von", len(zeilen_ab), "max", max(zeilen_ab.values()))
print("Abweichungen alt/neu:", len(flips))
for f in flips: print("FLIP", *f)
alt_ab = [(b, s, v["alt"]) for b, d in aus.items() for s, v in d.items() if v["alt"] and v["alt"] >= str(SCHNITT)]
print("alte Rechnung >= Schnitt:", len(alt_ab))
````
