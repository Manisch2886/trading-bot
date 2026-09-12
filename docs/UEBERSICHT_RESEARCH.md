# Übersicht: die Urteile aller `research/`-Untersuchungen

**Stand: 2026-09-12** · Erhebung, keine Untersuchung. Es wurde **kein Produktivcode
angefasst, keine Untersuchung wiederholt und keine Zahl neu gerechnet.** Jede Zahl
in diesem Dokument ist aus einem `BERICHT.md` **zitiert**; wo eine Angabe fehlt,
steht „nicht angegeben".

**Wozu.** Zu mehreren der Untersuchungen unter `research/` war nicht mehr bekannt,
wie sie ausgegangen sind. Das hatte bereits Folgen: eine externe Analyse brachte im
September 2026 **Volatilitäts-Skalierung** und **Hierarchical Risk Parity** als neue
Vorschläge ein — beides war längst untersucht, eines davon mit klar negativem
Ergebnis über alle neun Bots.

---

## 0. Lesehinweise

**Es sind achtzehn Ordner, nicht siebzehn.** Die Aufgabenstellung und
`docs/UEBERGABEPROTOKOLL.md` (Abschnitt 5, Verzeichnisbaum) nennen beide „17 Ordner".
`ls research/` listet **18**. Die beiden, die in keiner Zählung vorkommen dürften,
sind auch die beiden ohne `BERICHT.md` (siehe unten) — vermutlich die Ursache der
Abweichung.

**Nachträge haben Vorrang vor der Gesamteinschätzung.** Die Berichte folgen einem
Muster: Kurzfassung oder Entscheidungsgrundlage am Anfang, Gesamteinschätzung am
Ende, Nachträge als Blockzitate ganz oben und als eigene Abschnitte ganz unten. Bei
`hrp_portfolio` und bei `volatility_scaled_sizing` steht im Abschnitt
„Gesamteinschätzung" ein Urteil, das ein später eingefügter Nachtrag **umgekehrt**
hat. Wer nur den Zusammenfassungs-Abschnitt liest, bekommt dort den falschen Stand.

**Zwei Ordner haben gar keinen Bericht.** `research/parameter_doku/` und
`research/uebersprungene_trades/` enthalten je genau ein Python-Skript und kein
`BERICHT.md`. Ein Urteil lässt sich dort nur aus dem Modul-Docstring lesen — das ist
in diesem Dokument als solches gekennzeichnet.

**Untersuchung ist nicht gleich Untersuchung.** Sieben der achtzehn Ordner gehören
zu Pull Requests, die **Produktivcode geändert** haben (`backtest_defaults`,
`forward_test_sync`, `oos_take_profit`, `oos_positionslimit`,
`elliott_wave_lookahead` via Nachtrag K, `parameter_doku`,
`uebersprungene_trades`). Dort ist das „Urteil" eher ein Befund samt Korrektur als
ein Ja/Nein zu einem Vorschlag. Die Regel „Untersuchungen fassen keinen Bot-Code an"
(Protokoll, Prinzip 14) gilt für die elf übrigen.

---

## 1. Übersichtstabelle

| Ordner | Thema | Urteil | Urteil geändert | Datengrundlage überholt | Nutzer&shy;entscheidung offen |
|---|---|---|---|---|---|
| `backtest_defaults` | Welche `backtest_*.py`-Defaults wirken live? | **umgesetzt** — 9 Konstanten in 5 Bots gekoppelt, keine Wertabweichung | nein | teilweise (eine abgelegte Vergleichszahl) | ja — Punkt 5.2 (Parameter ohne `live_params`-Eintrag) |
| `datenluecke_wurzelkorrektur` | Letzten Kursbalken verwerfen oder Cronjob später legen? | **nein zur Wurzelkorrektur**, Weg B (Cron) ist die flachere Änderung | 1× (Prämisse aus PR #33 umgedreht) | nein | **ja** — der tatsächliche Cron-Zeitpunkt |
| `elliott_wave_lookahead` | Look-Ahead im Elliott-Backtest | **bestätigt**, gravierend; beide Kanäle im Bot behoben | 1× (Richtungs-Erwartung K-A5 korrigiert) | n. z. (Baseline ist per Konstruktion historisch) | ja — Weiterbetrieb `elliott_wave` |
| `elliott_wave_params` | Neubestimmung der Parameter beider Elliott-Bots | Krypto **ja** (10 %/6 %, live übernommen); Aktien **nein** — keine von 252 Kombinationen schlägt Buy-and-Hold | nein | **teilweise** — PR #81 berührt die Rasterläufe des Aktien-Bots | **ja** — Weiterbetrieb beider Bots, Stop-Kante 16 % |
| `exposure_messung` | Was misst der kombinierte Drawdown von −1,43 %? | **keine Risikokennzahl** — veraltet, falscher Nenner, Korrelation ein Messartefakt; die Vermutung „überwiegend Kasse" ist **falsch** | nein | nein (jüngster Bericht, frisch gerechnet) | ja — vier benannte Folgeaufgaben |
| `forward_test_sync` | `MAX_HOLD_DAYS` (rsi2) bzw. fünf Indikatorwerte (t3) zentralisieren | **umgesetzt**, Werte unverändert (11/11 bzw. 15/15) | nein | nein | teilweise — ATR-Literale in `t3/regime_filter.py` bewusst offen |
| `hrp_portfolio` | HRP statt Gleichgewichtung im 9-Bot-Portfolio | **offengelassen**; aktueller Stand: HRP **nicht** besser (−0,0432 Calmar ≈ 0,7 %) | **3×** (−0,19 → −0,46 → **+0,14** → **−0,04**) | **ja** — Kurvenstand 2026-09-08, zwei Merges seither | **ja** — ausdrücklich Nutzerentscheidung |
| `oos_positionslimit` | Positionslimit in der OOS-Simulation (Aktien-Elliott) | **Fehler behoben**; 14 von 128 Trades betroffen (10,9 %), frühere Schätzung „8" war eine Unterschätzung | 1× (eigene Schätzung korrigiert) | nein | ja — ob **8** die richtige Zahl ist, ist nie geprüft |
| `oos_take_profit` | `use_take_profit` wurde in der OOS-Prüfung nicht durchgereicht | **Fehler behoben** — es war kein „falscher Wert", sondern ein `TypeError`; keine Rückwirkung auf Entscheidungen | 1× (eigene Meldung aus PR #45 korrigiert) | **ja** — die Kennzahlen sind durch PR #48 überholt | nein |
| `order_sensitivity` | Reihenfolge gleichzeitiger Signale, alle 9 Bots | **betroffen, ja** — bei 3 Bots verschiebt die blosse Reihenfolge die Calmar um mehr als das Vierfache; **keine** der 6 geprüften Entscheidungen kippt | 1× (Drawdown-Invarianz früherer Studien widerlegt) | **ja** — gerechnet auf der Konfiguration **vor** der Sync-Reihe und **vor** dem Look-Ahead-Fix | ja — Tie-Breaking-Regel ausdrücklich offen |
| `parameter_doku` | Halten die dokumentierten Fundstellen (Datei + Zeile)? | **kein `BERICHT.md`** — Urteil nur aus dem Docstring: 2 von 20 Angaben waren beim Schreiben bereits falsch | nicht feststellbar | n. z. | nein |
| `pnl_2025_fixed_size` | P&L 2025 bei fixer Grösse von 1000 USD, alle 9 Bots | **bewusst kein Urteil** — reine Informationsauswertung, kein Ranking | nein | teilweise (Codestand 2026-09-07) | nein — 3 Beobachtungen |
| `sync_check` | Backtest- gegen Live-Konfiguration, alle 9 Bots | erst **5 von 9 abweichend**, nach der Sync-Reihe **alle neun synchron** | 1× (15 gemeldete „Abweichungen" waren Falschmeldungen des Prüfers) | teilweise (Wirkungstabelle historisch) | teilweise — fehlende `ALLOCATION_PCT`-Doku der Elliott-Bots |
| `trailing_stops` | ATR-kalibrierte Trailing-Stops, 5 in Frage kommende Bots | **nein** — nur die Drawdown-Wirkung ist belegbar, die risikoadjustierte Vorteilhaftigkeit bei **keinem** Bot; 2 Bots methodisch nicht auswertbar | **2×** (`volatility_breakout` Vorzeichen unbestimmt; VBC-Teilausnahme fällt weg) | nein (Live-Parameter-basiert, Nachtrag deckt den Filter ab) | ja |
| `trend_overlay` | Portfolioweiter Trend-Overlay (200-Tage-MA auf beiden Märkten) | **hält** in allen drei Teilaussagen: gesamt besser, out-of-sample wirkungslos, Wirkung auf 2022 konzentriert | 1× hin und 1× zurück (dieselbe Nuance) | **ja** — wie HRP, und **ohne** dessen Regimefilter-Nachtrag | ja |
| `uebersprungene_trades` | Limit oder Kapital — warum werden Trades übersprungen? | **kein `BERICHT.md`** — Docstring: alle 115 übersprungenen Trades gehen auf das **Limit** zurück, keiner auf Kapital | nicht feststellbar | n. z. | nein |
| `vbc_deepdive` | `volatility_breakout_crypto`: Vol-Sizing × ATR-Trailing | **die „doppelte Bestätigung" trägt nicht** — mit Live-Konfiguration bleibt nur die Drawdown-Reduktion | 1× (verschärft: Calmar-Befund P 95,0 % → 64,6 %) | nein | ja — Abwägung Rendite gegen Drawdown |
| `volatility_scaled_sizing` | Volatilitäts-skalierte Positionsgrössen, alle 9 Bots | **nein** — schadet bei **8 von 9** Bots; einziger Gewinner `rsi2_crypto` | 1× (von „7 von 9" auf „8 von 9") | **teilweise** — beide Elliott-Zeilen auf look-ahead-behafteter Grundlage | ja |

---

## 2. Der Querschnitts-Befund: worauf die Berichte rechnen

### 2.1 Drei Arten von Datengrundlage

Die Frage „beruht der Bericht auf den abgelegten `results/*/equity_curve.csv`?"
trennt die achtzehn Ordner sauber in drei Gruppen:

| Gruppe | Ordner | Risiko |
|---|---|---|
| **A — baut auf den abgelegten Kurven auf** | `hrp_portfolio`, `trend_overlay` | hoch: die Kurven veralten, ohne dass es jemandem auffällt |
| **B — rechnet selbst, liest `live_params.py`** | `volatility_scaled_sizing`, `trailing_stops`, `vbc_deepdive`, `pnl_2025_fixed_size`, `elliott_wave_params`, `exposure_messung`, `oos_*`, `backtest_defaults`, `sync_check`, `forward_test_sync` | mittel: veraltet mit dem Bot-Code, nicht mit den Dateien |
| **C — rechnet auf Kurs- oder Codestand, nicht auf Kapitalkurven** | `datenluecke_wurzelkorrektur`, `elliott_wave_lookahead`, `parameter_doku`, `uebersprungene_trades` | gering |

`order_sensitivity` ist der Sonderfall: es liest weder die abgelegten Kurven noch
`live_params.py`, sondern **ausdrücklich die Modulkonstanten von
`equity_simulation.py`** (Annahme 1 des Berichts) — also genau die Konfiguration,
die die Sync-Reihe danach beseitigt hat.

### 2.2 Die fünf veralteten Kurven

Der Befund ist im Repo bereits gemessen und steht in
`research/exposure_messung/BERICHT.md`, Abschnitt 7 — Zeilen der abgelegten Kurve
gegen Zeilen, die die **heutige** `equity_simulation.py` erzeugt:

| Bot | Zeilen abgelegt | Zeilen neu | identisch? |
|---|---:|---:|:---:|
| `elliott_wave` | 144 | 130 | **nein** |
| `elliott_wave_stocks` | 469 | 395 | **nein** |
| `rsi2_mean_reversion` | 2.641 | 4.232 | **nein** |
| `turtle_soup_stocks` | 1.887 | **8.915** | **nein** |
| `volatility_breakout` | 1.236 | 1.454 | **nein** |
| `t3_supertrend` | 656 | 656 | ja |
| `rsi2_crypto` | 392 | 392 | ja |
| `turtle_soup_crypto` | 1.414 | 1.414 | ja |
| `volatility_breakout_crypto` | 207 | 207 | ja |

Dieselbe Untersuchung beziffert, was das kostet: dieselbe Formel auf frisch
gerechneten Kurven ergibt statt **−1,43 %** einen kombinierten Drawdown von
**−9,41 %** (Abschnitt 7 ebendort). Die Dateien werden nur geschrieben, wenn jemand
`equity_simulation.py` von Hand aufruft — und sie werden weiter gelesen: von
`portfolio_correlation_analysis.py` und laut Protokoll 4.3b auch von
`shared/portfolio_overview.py`, also von der Montags-Mail und der
Dashboard-Portfolio-Sicht.

### 2.3 Merges seit den Berichten

| Datum | Merge | Was sich an der Bot-Konfiguration änderte |
|---|---|---|
| 2026-09-07 | `839500b` (PR #26) | **Look-Ahead-Fix beider Elliott-Bots** — grösste Verschiebung überhaupt: Renditen fallen um Faktor 32 bzw. 9 (`hrp_portfolio` Z1) |
| 2026-09-08 | PR #38–#42 | `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout`, `elliott_wave_stocks`: Backtest rechnet mit der Live-Konfiguration |
| 2026-09-08 | PR #45 (`9bb230f`) | wirksame Backtest-Defaults an `live_params.py` gekoppelt — verschiebt u. a. `volatility_breakout_crypto` |
| 2026-09-08 | PR #47, #48 | OOS-Simulation des Aktien-Elliott-Bots: `use_take_profit` und Positionslimit |
| 2026-09-08 | PR #51, #52 | fünf t3-Indikatorwerte und `rsi2_crypto/MAX_HOLD_DAYS` in `live_params.py` (Werte unverändert) |
| **2026-09-09** | **PR #57 (`3770ca7`)** | **BTC-Regimefilter jetzt auch im Backtest von `volatility_breakout_crypto`** — dessen `equity_curve.csv` wurde dabei neu erzeugt |
| **2026-09-12** | **PR #81 (`7bdf6e5`)** | **Kurslücken im Trade-Pfad**: `multi_symbol_optimise.py` **aller neun Bots** und vier `fetch_stock_data.py` geändert |

Die beiden letzten Zeilen sind die wichtigen: **jeder Bericht, der vor dem
2026-09-09 entstanden ist, rechnet auf einem `volatility_breakout_crypto`, den es so
nicht mehr gibt**, und **jeder Bericht vor dem 2026-09-12 kennt die
Kurslücken-Behandlung im Trade-Pfad nicht**. Wie gross der zweite Effekt ist, ist im
Repo nur für einen Bot beziffert: laut Nachtrag vom 12.09.2026 in
`research/elliott_wave_params/BERICHT.md` (Offener Punkt 2) war **1 von 150
Aktien-Symbolen** betroffen und **24 von 48 Rasterkombinationen** dieses Bots
erzeugten den NaN-Trade — die Live-Kombination allerdings **nicht**.

### 2.4 Die gefährdeten Untersuchungen

Die Frage, die dieses Dokument beantworten soll: *welche Untersuchungen stehen auf
einer inzwischen überholten Grundlage — und bei welchen davon ist das Urteil knapp
genug, dass es kippen könnte?*

#### Stufe A — Grundlage überholt **und** Urteil knapp

**1. `hrp_portfolio` — das mit Abstand grösste Risiko.**
Das Urteil hat bereits **dreimal** die Richtung oder die Grösse gewechselt
(−0,1905 → −0,4627 → **+0,1424** → **−0,0432** Calmar-Punkte). Der aktuelle
Abstand beträgt **0,7 %** eines Calmar-Niveaus von rund 6,17; der Bericht selbst
schreibt dazu: *„Das Vorzeichen ist eindeutig; die Grösse ist es nicht"* (V0). Der
Vorzeichenwechsel in Nachtrag Z hing an **einer einzigen Kurve**. Die heutige
Grundlage sind eingefrorene Kurven vom **2026-09-08** (`corrected_curves_v2/` plus
`corrected_curves_v2_regimefilter/`); PR #57 und PR #81 liegen danach. Bei diesem
Abstand kann eine erneut verschobene Kurve das Vorzeichen wieder drehen.

**2. `trend_overlay` — dieselbe Grundlage, eine Korrekturrunde weniger.**
Die Studie ist bei der **zweiten** Korrektur stehen geblieben und hat **kein**
Gegenstück zu HRPs Nachtrag V bekommen. Ihre eigene Annahme Z4.1 benennt die Lücke
wörtlich: die `volatility_breakout_crypto`-Kurve dieser Grundlage (71,26 %) ist
*„nicht live-konform"*, live läge sie bei 49,03 %. Genau diese Lücke hat bei HRP das
Ergebnis getragen. Zwei der drei Teilaussagen sind zusätzlich knapp:
– **T2** („out-of-sample keine Drawdown-Verbesserung") hält, weil der letzte aktive
Signaltag der **2025-04-21** ist und der Split am **2025-04-23** liegt — zwei Tage.
Der Bericht hält das selbst fest, *„damit die Zahlengleichheit nicht robuster wirkt,
als sie ist"*.
– Die Nuance, ob der Overlay out-of-sample Rendite kostet, ist bereits **einmal
gekippt und einmal zurückgekippt** (−0,41 → +0,81 → 0,00).
**T1** (+7,31 Calmar gesamt) und **T3** (85 % der Signaltage in 2022) sind dagegen
robust — T3 sogar strukturell, weil das Signal aus BTC und dem Aktien-Proxy kommt
und die Bot-Kurven gar nicht berührt.

**3. `order_sensitivity` — die Grundlage existiert nicht mehr.**
Der Bericht rechnet ausdrücklich auf den Konstanten von `equity_simulation.py`
(Annahme 1) und nennt in Abschnitt 8 selbst, dass diese bei vier Bots von
`live_params.py` abwichen. Genau diese vier sind seither angeglichen worden. Die
Zeile `rsi2_mean_reversion` — mit **12,1×** die Schlagzeile der Studie — ist mit
**Limit 8** gerechnet, live gilt **20** bei 5 % statt 10 % Allokation. Die
Elliott-Zeilen (`elliott_wave`: 783 Trades, Calmar 1193,97) stammen aus dem
**look-ahead-behafteten** Backtest; derselbe Wert steht in
`research/elliott_wave_lookahead/` als zu korrigierende Baseline.
**Was trotzdem hält:** die strukturelle Aussage — der Engpass ist das
Positionslimit, nicht das Kapital, und keine der sechs geprüften Entscheidungen
kippt — ist ein **gepaarter** Vergleich und damit gegen Niveauverschiebungen
weitgehend immun. Der Bericht begründet das selbst (Abschnitt 9). Gefährdet sind die
**absoluten** Kennzahlen, Perzentile und Einstufungen je Bot.

#### Stufe B — Grundlage teilweise überholt, Urteil mit Reserve

**4. `volatility_scaled_sizing`.** Beide Elliott-Zeilen stehen auf dem
look-ahead-behafteten Backtest (elliott_wave: 533 + 247 = 780 Trades, die Zahl vor
der Korrektur). Für `elliott_wave` kommt hinzu, dass Annahme 3 ein
`MAX_CONCURRENT_POSITIONS = 8` **unterstellt**, während der Bot laut
`research/order_sensitivity/` (Annahme 5) und `sync_check` S5 **bewusst kein
Positionslimit** hat. Die Kernaussage („schadet bei 8 von 9") ist davon nicht
bedroht — sie wird von sieben weiteren Bots getragen, und der einzige Gewinner
`rsi2_crypto` steht auf einer bis heute unveränderten Kurve (392 Trades). Aber die
beiden Elliott-Urteile selbst sind Zahlen ohne Boden.

**5. `elliott_wave_params`.** Die Urteile selbst sind gut abgestützt (Aktien: +398 %
gegen +756 % Buy-and-Hold — das ist keine knappe Sache). Zwei Vorbehalte stehen im
Bericht: die Krypto-Empfehlung beruht auf **130 Trades in fünf Jahren, davon 31
out-of-sample**, und das Aktien-Ergebnis schwankt allein durch die Zeilenreihenfolge
zwischen **+212 % und +509 %**. Dazu kommt PR #81: die Hälfte der Rasterläufe dieses
Bots war vom NaN-Trade betroffen (siehe 2.3) — die Rangfolge blieb laut Bericht
gültig, die Portfolio-Kennzahl daneben war unbrauchbar.

**6. `oos_take_profit`.** Kein Datengrundlagen-Problem, sondern ein direktes: seine
Kennzahlen (**+70,37 % / −10,11 % / Calmar 6,96**) sind durch den unmittelbar
folgenden PR #48 ersetzt worden (**+72,39 % / −9,69 % / Calmar 7,47**, siehe
`oos_positionslimit`). Wer die Zahlen dieses Berichts zitiert, zitiert einen
überholten Zwischenstand. Das Urteil („Fehler behoben, keine Rückwirkung") ist davon
unberührt.

**7. `sync_check`.** Die Schlussaussage („alle neun synchron", Nachtrag S vom
2026-09-09) ist aktuell; die **Wirkungstabelle** in Abschnitt 3 ist es nicht mehr —
sie enthält für `elliott_wave_stocks` die Zeile +3084,09 %, die der Look-Ahead-Fix
auf +352,72 % gedrückt hat. Der Bericht nennt in S2 ausserdem selbst, dass eine
abgelegte Vergleichszahl aus `backtest_defaults` seit PR #57 veraltet ist
(17.126,14 gegen 14.902,58).

#### Stufe C — Grundlage tragfähig

`exposure_messung` (jüngster Bericht, rechnet mit `shared/kursdaten.py` aus PR #81),
`vbc_deepdive` (seine gefilterte Fassung ist genau das, was der Bot seit PR #57
tut), `trailing_stops` (Live-Parameter-basiert, Nachtrag deckt den Filter ab),
`forward_test_sync`, `oos_positionslimit`, `datenluecke_wurzelkorrektur`,
`elliott_wave_lookahead`, `backtest_defaults`, `pnl_2025_fixed_size`.

**Nicht neu rechnen, nur benennen** — das ist auftragsgemäss die Grenze dieses
Dokuments. Welche der drei Untersuchungen der Stufe A eine Wiederholung wert ist,
entscheidet der Nutzer.

---

## 3. Die achtzehn Ordner im Einzelnen

### 3.1 `backtest_defaults`

*`BERICHT.md`, 321 Zeilen, 2026-09-08, keine Nachträge (1 Commit).*

**Was untersucht wurde.** Alle 9 Bots, 141 Funktions-Parameter mit Default plus alle
Modulkonstanten mit Gegenstück in `live_params.py`: welche davon bestimmen den
Live-Backtest tatsächlich über ihren Default? 29 wirken, 9 davon wurden in 5 Bots an
`live_params.py` gekoppelt.

**Urteil: umgesetzt.** Keine einzige neue Wertabweichung — alle 9 stimmten bereits
überein. Regressionscheck 5/5 identisch, Gegenprobe 5/5 reagieren. Nie geändert.

**Die strukturelle Einsicht.** Drei Fallen, an denen ein einfacherer Ansatz
gescheitert wäre: `equity_simulation.py` importiert die Backtest-Funktion aus
`multi_symbol_optimise.py` (eine Einteilung nach Dateiname hätte den entscheidenden
Aufruf als Grid-Search abgetan); Parameter werden **positionell** übergeben, eine
Textsuche nach `name=` findet sie nicht; und ein Wert kann direkt im **Rumpf** einer
Funktion gelesen werden, ohne je Parameter zu sein. Der Gegenpol: bei beiden
Elliott-Bots sehen `STOP_LOSS_PCT`/`TAKE_PROFIT_FIB` nach dramatischer Abweichung
aus, werden aber zur Laufzeit von aussen überschrieben — wer nur Zahlen vergleicht,
meldet dort einen Fehlalarm.

**Nutzerentscheidung offen: ja.** Punkt 5.2 — wirksame Parameter ohne Eintrag in
`live_params.py` (`VOLUME_FILTER_MULTIPLIER`, die Regimefilter-Konstanten,
`use_t3_exit`/`use_vwap_filter`, `calculate_vwap_daily(bars_per_day)`): aufnehmen
oder bewusst Implementierungsdetail bleiben? Die fünf t3-Indikatorwerte und
`rsi2_crypto/MAX_HOLD_DAYS` aus derselben Liste sind mit PR #51/#52 inzwischen
aufgenommen; Punkt 5.1 (OOS-`use_take_profit`) ist mit PR #47 erledigt.

**Datengrundlage.** Keine abgelegten Kurven — `regression.py` führt das echte
`equity_simulation.py` je Bot in einem eigenen Prozess aus. Überholt ist nur eine
abgelegte Vergleichsdatei: `results/regression_nachher.json` für
`volatility_breakout_crypto` seit PR #57 (belegt in `sync_check` S2).

---

### 3.2 `datenluecke_wurzelkorrektur`

*`BERICHT.md`, 236 Zeilen, 2026-09-08, keine Nachträge.*

**Was untersucht wurde.** Soll der Datenabruf den jüngsten Kursbalken verwerfen
(„Wurzelkorrektur"), weil er ein noch laufender Handelstag sein könnte? Geprüft an
150 Aktien-Dateien mit **1.417.557 Balken** und einer Nachspielung der Signalregel
über 166.749 Signalbalken.

**Urteil: nein — und die Prämisse trifft den beobachteten Fall gar nicht.** Genau
**ein** Balken aller 1.417.557 hat fehlende Preise (der bekannte APH-Fall), und
dieser Balken war **kein laufender Handelstag**: sein Volumen lag beim 1,40-fachen
des Üblichen. Weg **B** (Cronjob später legen) ist die deutlich flachere Änderung —
er verschiebt keine einzige Handelsentscheidung, Weg A verschiebt 166.749
Signalzeitpunkte.

**Einmal geändert: eine fremde Annahme.** PR #33 hielt fest, die Wurzelkorrektur
würde Signale „einen Tag früher" auslösen. Der Code sagt das Gegenteil: `iloc[-1]`
ist der jüngste Balken, fällt er weg, handelt der Bot einen Börsentag **später** und
bucht den Vortagsschluss.

**Die strukturelle Einsicht.** Beide Fehlerarten hängen am selben Punkt — ob zum
Abrufzeitpunkt ein abgeschlossener Handelstag vorliegt. Und: keiner der beiden Wege
ersetzt den Guard aus PR #33, weil der APH-Fall ein Datenfehler an einem
**abgeschlossenen** Tag war.

**Nutzerentscheidung offen: ja, und nur er kann sie treffen.** Läuft der Cronjob um
22:00 Berliner Zeit, startet er an **92,3 %** der Handelstage exakt zur
Schlussglocke; läuft er um 22:05 UTC, hat er mindestens 65 Minuten Abstand. Die
Crontab liegt auf dem Mac und war aus der Sitzung nicht lesbar.

**Datengrundlage.** Kursdateien und Kalenderrechnung, keine Kapitalkurven. Die CSVs
sind eine Momentaufnahme eines einzelnen Abrufs (2026-09-01/02).

---

### 3.3 `elliott_wave_lookahead`

*`BERICHT.md`, 744 Zeilen, 2026-09-07, ein Nachtrag (K) im selben Bericht.*

**Was untersucht wurde.** Der Verdacht, der Elliott-Wave-Backtest nutze
Zukunftswissen: ein Zigzag-Pivot **ist** erst dann ein Pivot, wenn der Kurs sich
danach um `deviation_pct` zurückbewegt hat — der Backtest stieg trotzdem zum
Zeitpunkt *und Preis* des Pivots ein.

**Urteil: bestätigt, und gravierender als vermutet.** Der Backtest kauft in **100 %
der Trades** günstiger, als es live möglich war; in **0 von 783** bzw. **0 von 519**
Trades konnte der Stop vor der Bestätigung auslösen. Wirkung:
`elliott_wave` +2184,96 % → **−25,73 %** (Calmar 1193,97 → −0,96),
`elliott_wave_stocks` +3084,09 % → **+352,72 %** (Calmar 315,02 → 15,72).
**Beide Kanäle sind im Bot-Code behoben** (Nachtrag K, PR #26), 1301 Trades einzeln
geprüft, 0 Kausalitätsverletzungen. `forward_test.py` und `live_params.py` blieben
unverändert — der Live-Bot war nie betroffen.

**Einmal geändert: die eigene Erwartung.** Annahme K-A5 sagte, die Kanal-1-Zahlen
seien eine Obergrenze. Für `elliott_wave` bestätigt, für `elliott_wave_stocks`
**nicht** (+14,46 pp statt weniger). Grund: die kausale Auswahl streicht keine Welle
mehr rückwirkend, es kommen **mehr** Trades zustande, und ausgewählt wurde nach dem
Fibonacci-Score — einem **Formmass, keinem Gewinnmass**.

**Die strukturelle Einsicht.** Die Aussagekraft eines Backtests hängt von der
Fragestellung ab, nicht nur von seiner Korrektheit: derselbe Backtest war für drei
frühere Untersuchungen brauchbar und für die Trailing-Stop-Frage unbrauchbar.

**Nutzerentscheidung offen: ja.** Folgeaufgabe 4 des Berichts — die
`equity_curve.csv`-Fallbacks in der Wochen-E-Mail entweder neu erzeugen oder als
„Backtest, nicht Live" kennzeichnen — deckt sich mit Protokoll-Punkt 15 und ist
offen. Folgeaufgaben 1–3 sind mit PR #26/#28 erledigt.

**Datengrundlage.** Eigene Läufe gegen eingefrorene Trade-Sätze
(`results/frozen_pr26/`); die Baseline ist per Konstruktion der historische Stand.

---

### 3.4 `elliott_wave_params`

*`BERICHT.md`, 457 Zeilen, 2026-09-07, ein Nachtrag am 2026-09-12 (2 Commits).*

**Was untersucht wurde.** Gibt es auf der look-ahead-bereinigten Grundlage eine
tragfähige Parametrisierung für die beiden Elliott-Bots? 252 Kombinationen je Bot
und Fenster, bewertet an fünf mechanischen Bedingungen (B1–B5), die vor dem Blick
auf die Ergebnisse in `summary.py` festgelegt wurden.

**Urteil, zweigeteilt und nie geändert.**
**Krypto: ja** — Zigzag 10 % / Stop 6 %, drei von sechs Kandidaten tragfähig;
+67,77 % / −10,17 % / Calmar 6,66 über fünf Jahre gegen Buy-and-Hold +12,19 % /
−79,76 % / 0,15. **Live übernommen** (PR #28).
**Aktien: nein** — genau ein Kandidat besteht formal, verliert aber im Walk-Forward
in zwei von drei Falten gegen Buy-and-Hold und bleibt mit +398 % weit hinter dessen
**+755,69 %**. *„Die aktuelle Live-Kombination ist nicht schlechter als die
Alternativen — sie ist nur genauso wenig überzeugend."*

**Die strukturelle Einsicht.** Der enge 2 %-Stop auf Stundenkerzen löst in **72,6 %**
aller Trades aus, bevor die erwartete Korrektur Zeit hatte — unsichtbar im alten
Backtest, weil der Stop dort bis zur Bestätigung gar nicht erreichbar war. Und:
Symbolauswahl ist **kein Hebel** (15 von 18 bzw. 132 von 147 Symbolen tragen
positiv bei, Top-3-Anteil 8 %).

**Nutzerentscheidung offen: ja, mehrfach.** Weiterbetrieb beider Bots (Punkt 5, und
Protokoll-Punkte 4/5); die Stop-Kante bei 16 % ist nicht ausgereizt (Punkt 1); der
Kommentar in `strategies/elliott_wave_stocks/live_params.py` hält weiterhin die
widerlegte Aussage „schlägt Buy-and-Hold klar (1458 % vs. 756 %)" fest (Punkt 4).

**Datengrundlage.** Bot-Funktionen direkt, keine abgelegten Kurven. Siehe aber 2.4
Stufe B zum PR-#81-Vorbehalt.

---

### 3.5 `exposure_messung`

*`BERICHT.md`, 537 Zeilen, 2026-09-12, keine Nachträge — der jüngste Bericht.*

**Was untersucht wurde.** Misst der oft zitierte kombinierte Drawdown von −1,43 %
überhaupt Risiko, oder beschreibt er ein Buch, das die meiste Zeit in Kasse liegt?
Alle neun Bots, 17.795 ausgeführte Positionen, tägliche Exposure über 1.618
Kalendertage.

**Urteil: der Verdacht trifft teilweise zu — aber nicht aus dem genannten Grund.**
Die Vermutung „überwiegend Kasse" ist **falsch**: das Neuner-Buch war an **keinem
einzigen** Tag flach und an keinem Tag unter 10 % Exposure. Die Schlussfolgerung
„−1,43 % ist keine Risikokennzahl" stimmt trotzdem, aus drei anderen Gründen:
(1) **veraltet** — mit heutigen Parametern −9,41 %; (2) **falscher Nenner** — am
investierten Kapital gemessen **−32,12 %**; (3) der Korrelationsbefund, auf dem die
Diversifikations-These ruhte, ist ein **Messartefakt** (Bot-Kapitalkurven bewegen
sich nur an Ausstiegstagen; zu Marktpreisen bewertet zeigt sich ein Beta bis
**+0,82**).

**Die strukturelle Einsicht.** Zwei überwiegend aus Nullen bestehende Reihen
korrelieren mechanisch nahe null, unabhängig davon, was die Märkte tun — *„eine
Messung, die etwas anderes misst als gemeint, und deren Ergebnis genau deshalb so
beruhigend aussieht"*. Und: der kleine Gesamt-Drawdown ist zum grössten Teil
**1/N-Gewichtung**, nicht Kompensation — die richtige Vergleichsgrösse ist der
**mittlere** Einzel-Bot-Drawdown (−17,93 %), nicht der schlechteste (−22,20 %).

**Nutzerentscheidung offen: ja**, vier benannte Folgeaufgaben — Kurven neu erzeugen,
Korrelations- und Drawdown-Angaben auf Marktpreise umstellen, Buy-and-Hold-Vergleiche
um die Exposure-Dimension ergänzen, Survivorship im Aktienuniversum.

**Datengrundlage.** Liest die abgelegten Kurven **nur**, um −1,43 % exakt zu
reproduzieren; alle eigenen Zahlen stammen aus frischen Läufen der echten
Bot-Funktionen mit den heutigen `live_params.py`. **Dieser Bericht ist die Quelle
der Tabelle in 2.2.**

---

### 3.6 `forward_test_sync`

*Zwei Berichte: `BERICHT_rsi2_crypto.md` (145 Zeilen) und `BERICHT_t3_supertrend.md`
(118 Zeilen), beide 2026-09-08, keine Nachträge.*

**Was untersucht wurde.** Zwei Umstellungen, die als einzige der Sync-Reihe das
**Live-Skript** anfassen: `MAX_HOLD_DAYS` bei `rsi2_crypto` und fünf Indikatorwerte
bei `t3_supertrend` wandern nach `live_params.py`, die Werte bleiben gleich.

**Urteil: umgesetzt, Verhalten nachweislich identisch.** 11/11 bzw. 15/15 Prüfungen
— Namensraum, Syntaxbaum und Verhalten auf echten Daten, DB-Inhalt und
Bildschirmausgabe zeichengenau gleich. Nie geändert.

**Die strukturelle Einsicht — die wertvollste dieser beiden Berichte.** Die
**Empfindlichkeitsprobe** macht die anderen Prüfungen erst aussagekräftig: die erste
Fassung des Werkzeugs prüfte, dass Positionen geschlossen wurden — sie wurden, aber
über den SMA-Exit. Der Zeit-Exit, der einzige Pfad, in dem `MAX_HOLD_DAYS` überhaupt
vorkommt, wurde nie durchlaufen (rund 1 % der Einstiegspunkte führen dorthin).
*„Ohne sie wäre ‚identisch' auch mit einem blinden Test zu bekommen."*

**Nutzerentscheidung offen: teilweise.** Die ATR-Literale in
`t3_supertrend/regime_filter.py` (22 / 3.0) sind **bewusst nicht** mitumgestellt:
der Regimefilter rechnet auf BTC, nicht auf dem Handelssymbol — gleiche Zahlen,
andere Grösse. Eine Gleichsetzung wäre eine inhaltliche Entscheidung.

**Datengrundlage.** Backtest-Regression gegen `origin/main`, stdout- und
`equity_curve.csv`-Hash. Die dort berichteten Trade-Zahlen (392 bzw. 656) sind bis
heute unverändert.

---

### 3.7 `hrp_portfolio`

*`BERICHT.md`, 994 Zeilen, 2026-09-06 bis 2026-09-10 (5 Commits), **vier Nachträge**
(N, Z, V, W) — der am stärksten überarbeitete Bericht des Repos.*

**Was untersucht wurde.** Hierarchical Risk Parity (López de Prado 2016) mit
quartalsweisem Walk-Forward-Rebalancing gegen die bestehende, nie rebalancierte
Gleichgewichtung des 9-Bot-Portfolios.

**Urteil: offengelassen — und viermal gerechnet.**

| Fassung | Datum | HRP − Gleichgewichtung (Calmar) | Kernaussage |
|---|---|---:|---|
| Erstfassung | 2026-09-06 | −0,1905 | HRP nicht besser |
| Nachtrag N (1. Korrektur) | 2026-09-07/08 | −0,4627 | hält, deutlicher |
| **Nachtrag Z (2. Korrektur)** | 2026-09-08 | **+0,1424** | **hält nicht** |
| **Nachtrag V (VBC live-konform)** | 2026-09-08 | **−0,0432** | **hält doch** |
| Nachtrag W | 2026-09-10 | unverändert −0,0432 | reine Wartung am Prüfwerkzeug |

**⚠ Wichtig für die Weitergabe:** die in der Aufgabenstellung mitgelieferte
Vorerhebung („die Kernaussage **kippte** beim dritten Mal, HRP liegt mit heutigen
Kurven +0,14 Calmar **vorn**") gibt den Stand von **Nachtrag Z** wieder.
**Nachtrag V hat diesen Vorsprung noch am selben Tag zurückgedreht**, und Nachtrag W
hat das Ergebnis am 2026-09-10 byteweise bestätigt. Der Vorzeichenwechsel aus
Nachtrag Z war *„ein Artefakt genau dieser einen Lücke"* — die
`volatility_breakout_crypto`-Kurve war die einzige der neun, die den live aktiven
BTC-Regimefilter nicht enthielt. **Gültig ist: HRP bringt keinen
risikoadjustierten Vorteil — mit einem Abstand von 0,7 %.** Damit stimmt zwar die
Richtung der ursprünglichen „Gesamteinschätzung" wieder, ihre Zahlen (12,83 gegen
13,02) sind aber dreifach überholt.

**Die strukturelle Einsicht.** HRP hilft hier nicht, weil (a) die neun Bots ohnehin
nur schwach korrelieren — die Diversifikationswirkung ist bei **jeder** vernünftigen
Gewichtung stark — und (b) HRP in diesem Datensatz ausgerechnet die
renditestärksten Bots als „riskant" einstuft und abwertet. Die Robustheitsprobe mit
Ward-Linkage bewegt sich in allen vier Fassungen **mit**, das Verfahren ist also
stabil; es liefert nur keinen Mehrwert. Methodischer Nebenbefund: die
30-Tage-Datenbasis-Schwelle greift in **17 von 18 Quartalen** — die Fallback-Logik
ist praktisch relevant, keine theoretische Absicherung.

**Nutzerentscheidung offen: ja, ausdrücklich.** Der Bericht sagt in V0 selbst, dass
die dritte in der Aufgabe genannte Möglichkeit — *„kein klarer Unterschied mehr"* —
die Lage mindestens so gut beschreibt wie ein Richtungsurteil.

**Datengrundlage: `results/*/equity_curve.csv` — der kritische Fall.** Aktuell
eingefroren unter `corrected_curves_v2/` (erzeugt 2026-09-08 aus dem damaligen
`__main__`-Block) plus `corrected_curves_v2_regimefilter/` für den einen getauschten
Bot. Bericht vom 06.–10.09.2026, Kurven vom 08.09.2026, seither PR #57 und PR #81.

---

### 3.8 `oos_positionslimit`

*`BERICHT.md`, 189 Zeilen, 2026-09-08, keine Nachträge.*

**Was untersucht wurde.** `oos_equity_simulation.py` des Aktien-Elliott-Bots
simulierte unbegrenzt viele gleichzeitige Positionen, während live 8 gelten — ein
Nebenbefund aus PR #47.

**Urteil: Fehler behoben, Kernaussage unverändert.** +70,37 % → **+72,39 %**,
Drawdown −10,11 % → **−9,69 %**, Calmar 6,96 → **7,47**. Der Trades-Hash ist vorher
wie nachher `277c1c2324422f60` — die Änderung hat nachweislich nur die
Portfolio-Ebene berührt.

**Einmal geändert: die eigene Schätzung.** Die Einschätzung aus PR #47 („nur 8 von
128 binden am Kapital, der Effekt dürfte klein sein") mass die falsche Grösse.
Tatsächlich betroffen: **14 von 128 Trades (10,9 %)** — eine Unterschätzung um
Faktor 1,75.

**Die strukturelle Einsicht.** Limit und Kapitalgrenze sind hier keine unabhängigen
Effekte, sondern **Quasi-Substitute**: 8 Positionen × 10 % binden höchstens 80 % des
Kapitals, es bleibt immer Geld übrig. Ohne Limit stieg die Belegung auf 9 — und
genau dort riss das Kapital acht Mal. Deshalb wird das Ergebnis mit sechs Trades
weniger nicht schlechter, sondern leicht besser.

**Nutzerentscheidung offen: ja.** Ob **8** die richtige Zahl ist, wurde nie geprüft
(Protokoll-Punkt 1) — im Gegensatz zum T3-Bot, wo 3/5/8/unbegrenzt systematisch
verglichen wurden.

**Datengrundlage.** Eigene Vorher-/Nachher-Läufe des echten Skripts in einem
isolierten Prozess; keine abgelegten Kurven.

---

### 3.9 `oos_take_profit`

*`BERICHT.md`, 281 Zeilen, 2026-09-08 (2 Commits), keine Nachträge.*

**Was untersucht wurde.** Die OOS-Validierung des Aktien-Elliott-Bots reichte
`use_take_profit` nicht an `collect_all_trades()` durch, obwohl das Suchraster genau
über diese Dimension optimiert.

**Urteil: Fehler behoben — und die eigene frühere Meldung korrigiert.** PR #45
meldete, die OOS-Prüfung laufe „immer mit Take-Profit". Der tatsächliche Lauf zeigt
etwas anderes: das Skript **stirbt** mit einem `TypeError`. Passend dazu existierte
`results/elliott_wave_stocks/oos_equity_curve.csv` gar nicht — das Skript ist für
diesen Bot nie durchgelaufen. Nach dem Fix: +70,37 % / −10,11 % / Calmar 6,96.
**Rückwirkung auf getroffene Entscheidungen: keine**, in drei Schritten belegt.

**Die strukturelle Einsicht.** Ob aus dem fehlenden Ziel ein `NaN` oder ein echtes
`None` wird, hängt davon ab, ob überhaupt eine Kombination mit festem Ziel die
Mindestfilter besteht — `NaN * float` geht **still** durch, `None * float` wirft. Eine
Lösung, die nur an `NaN` denkt, griffe zu kurz. Und Testgruppe E ist dem Autor
wichtiger als der Einzeiler-Fix: sie vergleicht, welche Dimensionen das Suchraster
**liefern** kann mit denen, die die OOS-Simulation **abholt** — sie fängt den
nächsten Fall dieser Art ab.

**Nutzerentscheidung offen: nein.**

**Datengrundlage.** Eigene Läufe. **Aber: die Kennzahlen sind überholt** — PR #48
(`oos_positionslimit`) hat sie unmittelbar danach auf +72,39 % / −9,69 % / 7,47
verschoben. Der in Abschnitt 8 selbst benannte „offene Punkt" ist genau der PR, der
darauf folgte.

---

### 3.10 `order_sensitivity`

*`BERICHT.md`, 409 Zeilen, 2026-09-07, keine Nachträge.*

**Was untersucht wurde.** Wie stark hängt ein Backtest-Ergebnis daran, in welcher
Reihenfolge gleichzeitige Signale verarbeitet werden? 9 Bots, 26.649 Trades, 500
Permutationen je Bot mit festem Seed.

**Urteil: betroffen, ja — deutlich stärker als vermutet.** Bei 3 von 9 Bots
verschiebt die blosse Reihenfolge die Calmar-Ratio um mehr als das Vierfache, bei
`rsi2_mean_reversion` um das **Zwölffache** (0,21 bis 2,54). Ablehnungsquoten bis
**84,4 %** (`turtle_soup_stocks`). **Keine der sechs geprüften, bereits umgesetzten
Entscheidungen kippt** dadurch.

**Einmal geändert: eine Aussage der Vorgänger-Studien.** Dort hiess es, der Max
Drawdown sei gegenüber der Reihenfolge „weitgehend invariant". Über alle 9 Bots gilt
das **nicht** — es gilt nur für die gering ausgelasteten Bots, also genau jene, die
dort betrachtet wurden.

**Die strukturelle Einsicht — die wertvollste dieser Untersuchung.** Der Engpass ist
fast nie das Kapital, sondern das **Positionslimit**: über alle 9 Bots sind
praktisch **100 %** der Ablehnungen limitbedingt, 0 kapitalbedingt (Ausnahme:
`elliott_wave`, der einzige Bot ohne Limit, mit genau einer). Die im Projekt
verbreitete Formulierung „nicht genug freies Kapital" beschreibt also nicht, was
passiert. Und der Grund, warum Entscheidungen trotzdem halten: sie sind **Vergleiche**
zwischen zwei Konfigurationen, und die Willkür trifft beide Seiten gleichermassen —
sie verzerrt die absoluten Kennzahlen erheblich, aber selten deren Rangfolge.

**Zwei Einzelbefunde, die man nicht vergessen sollte.** Der berichtete Wert von
`turtle_soup_crypto` liegt im **96,6. Perzentil** seiner Verteilung — die Zahl
stellt diesen Bot systematisch zu gut dar. Und live ist die Reihenfolge **nicht
zufällig, sondern systematisch**: alle Bots iterieren über nach Marktkapitalisierung
bzw. 24-Stunden-Volumen absteigend sortierte Listen — die grössten Werte bekommen
strukturell zuerst einen Platz.

**Nutzerentscheidung offen: ja.** Ob eine bewusste Tie-Breaking-Regel eingeführt
werden soll, ist ausdrücklich nicht Teil der Untersuchung.

**Datengrundlage: die Konfiguration von `equity_simulation.py` vor der Sync-Reihe.**
Siehe 2.4, Stufe A, Punkt 3.

---

### 3.11 `parameter_doku`

*Kein `BERICHT.md`. Ein Skript: `pruefe_fundstellen.py`, 2026-09-08, zuletzt
geändert 2026-09-09.*

**Was untersucht wurde** (laut Modul-Docstring): PR #45, Befund 7.2 dokumentierte
wirksame Parameter ohne `live_params.py`-Eintrag mit Wert **und exakter Fundstelle**
(Datei + Zeile). Das Skript hält jede dokumentierte Angabe gegen die Wirklichkeit —
zeigt `datei.py:ZEILE` noch auf den genannten Namen, stimmt die Zahl noch?

**Urteil: aus keinem Bericht herauszulesen.** Es gibt keine Gesamteinschätzung, kein
Ja/Nein. Der Docstring enthält den einzigen inhaltlichen Befund: *„Beim Schreiben
der Blocks waren zwei von zwanzig Angaben bereits falsch (die
`use_volume_filter`-Signaturen beider Breakout-Bots), nur durch diese Prüfung
aufgefallen."* Und die strukturelle Begründung, die über den Einzelfall hinausgeht:
*„Zeilennummern verrutschen bei der nächsten Änderung, und ein Kommentar, der auf
die falsche Zeile zeigt, ist schlimmer als keiner — er sieht präzise aus und ist es
nicht."*

**Wo das Urteil stehen müsste:** in einem `research/parameter_doku/BERICHT.md`. Die
Untersuchung gehört zu PR #49; eine Zusammenfassung könnte auch dort liegen.

**Nutzerentscheidung offen: nein.** Datengrundlage: Quelltext, rein lesend.

---

### 3.12 `pnl_2025_fixed_size`

*`BERICHT.md`, 272 Zeilen, 2026-09-07, keine Nachträge.*

**Was untersucht wurde.** P&L des Kalenderjahres 2025 für alle neun Bots bei einer
festen Positionsgrösse von 1000 USD — brutto (wie in der Aufgabe vorgegeben) und
netto (mit dem Kostenmodell der Bots, −3,00 USD je Trade).

**Urteil: bewusst keines.** *„Keine Bewertung, kein Ranking, keine
Handelsempfehlung"* — die Zeilenreihenfolge der Tabelle ist in `konfiguration.py`
festgelegt und folgt nicht dem Ergebnis. Nie geändert.

**Die strukturelle Einsicht.** Die Brutto-Formel **begünstigt systematisch Bots mit
vielen Trades**, weil sie deren Kosten weglässt — bei `turtle_soup_crypto` dreht der
Abzug das Vorzeichen (+108,04 → −1.159,40). Beim Elliott-Krypto-Vergleich dreht
netto das Bild um 400 USD zugunsten des neuen Parametersatzes, und der ganze
Unterschied kommt aus der Trade-Zahl: 150 Trades weniger sind 450 USD weniger
Kosten. Der Bericht warnt zugleich davor, ein einzelnes Kalenderjahr als Prüfstein
zu nehmen — über fünf Jahre liegt die alte Kombination bei −25,7 %, die neue bei
+67,8 %.

**Nutzerentscheidung offen: nein**, drei Beobachtungen: das Binance-Kostenmodell
gilt auch für die vier Aktien-Bots; `volatility_breakout_crypto` hat nach dem
13.08.2025 keinen Einstieg mehr (der BTC-Regimefilter blockiert **126 von 359**
Trades); die Zahlen sind kein Live-Ergebnis.

**Datengrundlage.** `collect_all_trades` der Bots mit Parametern aus
`live_params.py`, Codestand 2026-09-07; der BTC-Regimefilter wurde für
`volatility_breakout_crypto` **von Hand nachgezogen** — seit PR #57 tut der Bot das
selbst.

---

### 3.13 `sync_check`

*`BERICHT.md`, 481 Zeilen, 2026-09-07, ein Nachtrag (S) vom 2026-09-09.*

**Was untersucht wurde.** Stimmen `equity_simulation.py` und `live_params.py` bei
allen neun Bots überein — und welche der fünf Profitabilitäts-Studien sind von
Abweichungen betroffen?

**Urteil, in zwei Stufen.** Erstfassung: **5 von 9 Bots abweichend**, teils
erheblich (bei `elliott_wave_stocks` verdoppelt sich die Baseline-Rendite von
1500 % auf 3084 %). Nachtrag S (2026-09-09): **alle neun synchron**,
`ABWEICHEND (0), SYNCHRON (9)`.

**Einmal geändert — und zwar zugunsten des Repos.** Vor dem Nachtrag meldete der
Prüfer 15 Abweichungen bei 7 Bots. **Alle 15 waren Falschmeldungen**: die Werte
waren bereits gekoppelt, nur eben per `from live_params import …` statt als
Zuweisung — und der Prüfer las ausschliesslich `ast.Assign`. *„Der Prüfer bestrafte
also den Erfolg der Aufräumarbeit."* Geändert wurde der Prüfer, nicht der Bot.

**Die strukturelle Einsicht.** Die eine Abweichung, die **alle fünf** Studien
durchdrang, war der BTC-Regimefilter — *„gerade deshalb, weil er kein Parameter ist,
sondern fehlendes Verhalten"*. Eine Sync-Prüfung, die nur Konstanten vergleicht,
hätte ihn nie gefunden. Und die Herkunft aller fünf Abweichungen ist dieselbe:
`equity_simulation.py` stand in jedem Fall noch auf dem Stand des Prototyp-Commits,
die validierten Werte landeten nur in `live_params.py`. Die vier synchronen Bots
waren *„nicht synchron, weil jemand sie synchronisiert hätte, sondern weil sich bei
ihnen nichts geändert hat"*.

**Nutzerentscheidung offen: teilweise.** Von den vier empfohlenen Folgeaufgaben sind
drei erledigt (#22 wiederholt in `vbc_deepdive` N; die `volatility_breakout_crypto`-
Zeilen aus #18/#21 nachgerechnet; #19/#20 mit neuen Kurven wiederholt). Offen bleibt
Punkt 4: die fehlende `ALLOCATION_PCT`-Dokumentation bei beiden Elliott-Bots — in
Nachtrag S5 weiterhin als bewusster Nicht-Befund geführt.

**Datengrundlage.** Eigene Läufe mit den unveränderten Bot-Funktionen. Die
Wirkungstabelle in Abschnitt 3 ist durch den Look-Ahead-Fix teilweise historisch
(siehe 2.4 Stufe B).

---

### 3.14 `trailing_stops`

*`BERICHT.md`, 1027 Zeilen (der längste Bericht), 2026-09-07, 3 Commits; dazu
`NACHTRAG_REGIMEFILTER.md`, 199 Zeilen.*

**Was untersucht wurde.** Volatilitäts-kalibrierte ATR-Trailing-Stops statt fester
Prozent-Stops. 5 der 9 Bots kommen überhaupt in Frage; 2 davon (beide Elliott-Bots)
sind **methodisch nicht auswertbar**, weil ihr Backtest zum Zigzag-Wellenende
einsteigt — ein Trailing-Stop verwandelt genau diesen Look-Ahead in einen
quasi-sicheren Gewinn (Gewinnraten 98,7 % bzw. 99,4 %).

**Urteil: nein — und zwar nach zwei Korrekturen einheitlich.**

| Bot | Erstfassung | nach Ergänzung / Nachtrag |
|---|---|---|
| `t3_supertrend` | Verbesserung: nein | unverändert, jetzt belegt (P = 2,4 %) |
| `volatility_breakout` | Verbesserung: nein | **korrigiert: Vorzeichen unbestimmt** (P = 63/74/33 %) |
| `volatility_breakout_crypto` | unklar, OOS-Calmar besser | Drawdown ja (P ≥ 97,3 %), **Calmar nein** (P = 64,6 %) |

Der Schlusssatz — *„die Drawdown-Wirkung lässt sich beziffern, die risikoadjustierte
Vorteilhaftigkeit nicht"* — gilt nach dem Nachtrag **für alle drei auswertbaren Bots
ohne Ausnahme**; `volatility_breakout_crypto` war die einzige Teilausnahme und fällt
weg.

**Die strukturelle Einsicht — sie trägt über alle vier Backlog-Untersuchungen.**
*„Jeder Mechanismus, der die Ertragsverteilung an ihrem oberen Ende beschneidet,
kostet bei diesen Bots mehr, als er an Risiko spart."* Vol-Sizing verkleinert die
Position in volatilen Phasen, ein Trailing-Stop beendet sie, sobald die Bewegung
stockt — beide greifen dort an, wo diese Strategien ihren Ertrag erzeugen: in
wenigen, grossen, volatilen Bewegungen. Bei `t3_supertrend` sinkt der grösste
Einzeltrade von +321 % auf +57 %. Dazu ein Nebeneffekt, der leicht übersehen wird:
durch die rechtsschiefe Verteilung der ATR-Distanzen werden **einzelne Verluste
grösser** (bis −26,03 % gegen −8,30 %), obwohl die mediane Stopweite kalibriert
identisch ist. Und: der grösste Teil des Effekts stammt vom **Nachziehen** des
Stops, nicht von der ATR-Kalibrierung — für `volatility_breakout_crypto` dreht sich
genau das unter Live-Konfiguration um.

**Nutzerentscheidung offen: ja** (keine Handlungsempfehlung, Entscheidung
ausdrücklich beim Nutzer). Für die beiden Elliott-Bots ist die Frage **offen, nicht
beantwortet**.

**Datengrundlage.** Parameter aus `live_params.py` (belegt im `sync_check`,
Einstufung „gering"); die Elliott-Zahlen stammen aus dem look-ahead-behafteten
Backtest, sind aber ohnehin als nicht auswertbar gekennzeichnet.

---

### 3.15 `trend_overlay`

*`BERICHT.md`, 737 Zeilen, 2026-09-07/08, **zwei Nachträge** (N, Z).*

**Was untersucht wurde.** Ein aggregiertes „Krypto- UND Aktienmarkt gleichzeitig im
Abwärtstrend"-Signal (200-Tage-MA auf BTC/USDT und einem S&P-500-Top-150-Proxy),
retrospektiv auf das gleichgewichtete 9-Bot-Portfolio angewendet: Exponierung
reduzieren (50 %) oder pausieren (0 %)?

**Urteil: hält, in allen drei Teilaussagen und in allen vier Grundlagen.**
**T1** — über den Gesamtzeitraum verbessert der Overlay das Ergebnis (aktuell
+7,31 Calmar). **T2** — out-of-sample **keine** Drawdown-Verbesserung; in der
aktuellen Fassung sind alle drei Varianten out-of-sample sogar **zahlengleich**
(26,44 % / −4,53 % / 5,84), weil das Signal dort an **0 von 485 Tagen** aktiv ist.
**T3** — 255 der 300 aktiven Signaltage (85,0 %) liegen in 2022; das ist in allen
Fassungen zahlengleich, weil das Signal gar nicht von den Bot-Kurven abhängt.

**Eine Nuance ist gekippt und wieder zurückgekippt.** Die Erstfassung sagte, der
Overlay „kostet stattdessen leicht Rendite" (OOS-Calmar −0,41); die erste Korrektur
drehte das (+0,81); die zweite macht es gegenstandslos (0,00). Beide Formulierungen
der Erstfassung sind out-of-sample hinfällig: *„der Overlay kostet nichts und bringt
nichts."*

**Die strukturelle Einsicht.** *„Ein Signal, das retrospektiv gut aussieht, weil es
eine einzelne grosse historische Bewegung erwischt hat."* Und der Grund, warum jedes
Overlay hier wenig ausrichten kann: das gleichgewichtete 9-Bot-Portfolio ist bereits
so stark diversifiziert, dass es schlicht *„nicht mehr viel Drawdown gibt, den man
reduzieren könnte"* — die Verbesserungsmarge ist strukturell klein, unabhängig von
der Signal-Konstruktion.

**Nutzerentscheidung offen: ja.**

**Datengrundlage: `results/*/equity_curve.csv`, Stand 2026-09-08** — und im
Unterschied zu `hrp_portfolio` **ohne** den Regimefilter-Nachtrag. Siehe 2.4, Stufe
A, Punkt 2.

---

### 3.16 `uebersprungene_trades`

*Kein `BERICHT.md`. Ein Skript: `aufschluesselung.py`, 2026-09-08.*

**Was untersucht wurde** (laut Modul-Docstring): `simulate_portfolio()` kennt zwei
Abbruchgründe — Positionslimit und fehlendes Kapital — und wirft beide in dieselbe
Liste; die Ausgabezeile des Aktien-Elliott-Bots nannte jahrelang pauschal „nicht
genug freies Kapital".

**Urteil: aus dem Docstring eindeutig, aus keinem Bericht.** *„Ergebnis am
2026-09-08: alle 115 übersprungenen Trades gehen auf das Positionslimit zurück,
KEINER auf fehlendes Kapital. Der alte Klammerzusatz war also nicht bloss ungenau,
sondern nannte ausgerechnet den Grund, der nie zutraf."*

**Die strukturelle Einsicht — samt Gegenprobe.** Bei 10 % Allokation und höchstens 8
Positionen sind nie mehr als rund 80 % gebunden, das Limit greift praktisch immer
zuerst. Dass der zweite Zähler deshalb nicht bloss tot ist, zeigt eine Gegenprobe
mit anderen Limits: Limit 20 oder kein Limit → **85 Trades** scheitern sehr wohl am
Kapital. *„Ohne diese Gegenprobe wäre ‚0 wegen Kapital' auch mit einem kaputten
Zähler zu bekommen gewesen."*

**Wo das Urteil stehen müsste:** in einem `research/uebersprungene_trades/BERICHT.md`;
inhaltlich deckt es sich mit `oos_positionslimit`, Abschnitt 3, das dieselbe Frage
für die OOS-Simulation beantwortet.

**Nutzerentscheidung offen: nein.** Datengrundlage: eigener Lauf, rein lesend.

---

### 3.17 `vbc_deepdive`

*`BERICHT.md`, 838 Zeilen, 2026-09-07, ein Nachtrag (N) im selben Bericht.*

**Was untersucht wurde.** `volatility_breakout_crypto` galt als „doppelt bestätigt" —
er war sowohl der Vol-Sizing- als auch der Trailing-Stop-Gewinner. Diese
Vertiefungsstudie prüft die vier Kombinationen (2 × 2) mit Block-Bootstrap (2000
Replikate), 500 Reihenfolge-Permutationen, Quartals-Episoden und Walk-Forward.

**Urteil: die doppelte Bestätigung trägt nicht — und mit Live-Konfiguration noch
weniger.**

| Behauptung | ohne Filter | **mit Filter (live)** |
|---|---|---|
| Trailing senkt den Drawdown | 100,0 / 99,9 / 99,2 % | **99,2 / 99,3 / 97,3 %** → hält |
| Trailing verbessert die Calmar | 73,8 / 48,8 / **95,0 %** | 61,1 / 50,8 / **64,6 %** → fällt weg |
| Vol-Sizing verbessert etwas | 40,1 / 47,1 / 53,8 % | **16,1 / 21,1 / 38,7 %** → kippt ins Negative |
| Kombination schlägt Trailing allein | 31,1 / 27,6 / 71,2 % | **13,4 / 9,8 / 50,6 %** → kein Beleg |

*„Nein — als ‚mehrfach bestätigter' Kandidat trägt er nicht mehr."* Einmal
geändert, und zwar verschärfend.

**Die strukturelle Einsicht.** *„Es waren nie zwei Signale. Es war ein Effekt —
Drawdown-Reduktion durch früheres Aussteigen — plus ein zweiter, der bei genauer
Messung verschwindet."* Der Regimefilter, den der Bot bereits fährt, liefert
dieselbe Schutzwirkung; was der Trailing-Stop darüber hinaus beiträgt, wiegt den
Renditeverlust nicht auf. Dazu der Stichprobenhinweis, der jede OOS-Aussage relativiert:
der Filter senkt die Out-of-Sample-Basis von 103 auf **64** ausgeführte Trades.

**Nutzerentscheidung offen: ja** — die Abwägung „Versicherung, die zuverlässig
Rendite kostet, deren risikoadjustierter Nutzen nicht gesichert ist" ist laut
Bericht *„eine Präferenzfrage und keine Backtest-Frage"*.

**Datengrundlage.** `live_params.py` plus vendorierte Bausteine der beiden
Vorgängerstudien; 56/56 Referenzwerte aus vier unabhängigen Quellen, darunter die in
`live_params.py` dokumentierte Zahl *„70/30: -11,33 % -> -7,76 %"*, die exakt
getroffen wird. Die gefilterte Fassung entspricht dem, was der Bot seit PR #57 tut.

---

### 3.18 `volatility_scaled_sizing`

*`BERICHT.md`, 368 Zeilen, 2026-09-06/07; dazu `NACHTRAG_REGIMEFILTER.md`, 160
Zeilen.*

**Was untersucht wurde.** Inverse-Volatilitäts-Gewichtung der Positionsgrössen
(kalibriert auf mittleres Gewicht 1,0 — fairer Vergleich zur fixen Allokation)
gegen die bestehende feste Allokation, für alle neun Bots, In-Sample,
Out-of-Sample und über vier Walk-Forward-Fenster.

**Urteil: nein.** Erstfassung: schadet bei **7 von 9**, zwei Gewinner
(`rsi2_crypto`, `volatility_breakout_crypto`), einer unklar (`t3_supertrend`).
**Nachtrag: schadet bei 8 von 9** — mit dem live aktiven BTC-Regimefilter kippt
`volatility_breakout_crypto` von „Verbesserung: ja" auf **nein** (Calmar in-sample
1,26 → 0,72, out-of-sample 2,96 → 2,68). **Einziger Gewinner bleibt
`rsi2_crypto`.** Einmal geändert, für genau einen Bot.

**Die strukturelle Einsicht — der wertvollste Teil dieser Untersuchung.**
*„Vol-Skalierung reduziert die Positionsgrösse genau dann, wenn die Strategie am
meisten verdient, und kappt so überproportional die Gewinnseite."* Bei
Trendfolge-Bots fallen die grössten Gewinne in Phasen erhöhter Volatilität — die
Vermutung der Aufgabenstellung, gerade Trendfolger würden profitieren, wird durch
die Daten umgedreht. Die Trailing-Stop-Untersuchung hat dasselbe Muster später mit
einem völlig anderen Mechanismus unabhängig bestätigt. Zweite Einsicht aus dem
Nachtrag: die Vol-Skalierung war für diesen Bot *„nie ein eigener Effekt, sondern
eine zweite Messung derselben Schutzwirkung — nur die schlechtere von beiden"*.

**Nutzerentscheidung offen: ja** (Live-Aktivierung ausdrücklich Nutzersache).

**Datengrundlage.** `live_params.py` plus `collect_all_trades`; laut `sync_check`
Einstufung „gering", betroffen war nur `volatility_breakout_crypto` — und genau
diese Zeile hat der Nachtrag nachgerechnet. **Zwei Vorbehalte bleiben:** beide
Elliott-Zeilen stehen auf dem look-ahead-behafteten Backtest, und Annahme 3
unterstellt `elliott_wave` ein Positionslimit von 8, das der Bot nicht hat.

---

## 4. Widersprüche, Lücken und nicht eindeutige Stellen

Auftragsgemäss festgehalten statt aufgelöst:

1. **Die Vorerhebung zu `hrp_portfolio` ist selbst überholt.** Sie gibt Nachtrag Z
   wieder (+0,14 für HRP); Nachtrag V und W haben das auf −0,0432 zurückgedreht.
   Siehe 3.7. Das ist genau der Fehlertyp, den dieses Dokument verhindern soll —
   und ein Beleg dafür, dass die Regel „Nachträge haben Vorrang" auch für den
   **letzten** Nachtrag gelten muss, nicht nur für den auffälligsten.

2. **Zwei Ordner ohne Bericht** (`parameter_doku`, `uebersprungene_trades`): das
   Urteil steht nur im Modul-Docstring. Es ist dort eindeutig, aber es steht nicht,
   wo es stehen müsste.

3. **Die Ordnerzahl stimmt an zwei Stellen nicht.** Aufgabenstellung und
   `docs/UEBERGABEPROTOKOLL.md` Abschnitt 5 nennen 17, `ls research/` liefert 18.

4. **`order_sensitivity` und `volatility_scaled_sizing` widersprechen sich in einer
   Nebenannahme.** Vol-Sizing nimmt für `elliott_wave` ein
   `MAX_CONCURRENT_POSITIONS = 8` an (Annahme 3, als `max_concurrent_assumed: true`
   markiert); `order_sensitivity` (Annahme 5) und `sync_check` S5 halten fest, dass
   dieser Bot **bewusst kein Positionslimit** hat. Welche der beiden Lesarten die
   Vol-Sizing-Zahlen für diesen Bot trägt, ist ohne Neurechnung nicht zu sagen —
   und Neurechnen ist hier ausgeschlossen.

5. **`oos_take_profit` und `oos_positionslimit` beschreiben denselben Bot mit zwei
   Zahlensätzen.** Der zweite ersetzt den ersten. Wer den älteren Bericht isoliert
   liest, zitiert +70,37 % statt +72,39 %.

6. **Die `results/*/equity_curve.csv` werden weiter gelesen**, obwohl fünf von neun
   veraltet sind — laut `exposure_messung` (Abschnitt 11, Punkt 5) von
   `portfolio_correlation_analysis.py`, der Montags-Mail und der
   Dashboard-Portfolio-Sicht, solange ein Bot unter zehn geschlossenen Live-Trades
   liegt. Das tun derzeit alle neun. Das deckt sich mit Protokoll-Punkt 15.

---

## 5. Quellen

Ausschliesslich die `BERICHT.md`-Dateien unter `research/` (und die zwei
Modul-Docstrings), `docs/UEBERGABEPROTOKOLL.md` Abschnitte 5 und 9 sowie
`git log`/`git show` für Datums- und Merge-Angaben. Kein Skript wurde ausgeführt,
keine Kennzahl nachgerechnet.
