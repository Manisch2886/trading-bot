# ERGEBNIS TB-166 — E-3a: Schranke je Symbol im Signalpfad und gemeinsame Tag-Rechnung (R90 (c)–(e), R98 (a)–(c)), Neubau auf e654b08

**Sitzung:** TB-166, Mac (Claude Code, Opus 5.5), 16.10.2026 · **Auftrag:** `docs/auftraege/MAC_TB-166_e3a_schranke_je_symbol.md` · **Zweig:** `main`
**Commits:** `57a1062` (S0, Schritt 0: trägt die 2 0a-Pfade `docs/auftraege/AKTUELLER_AUFTRAG.md` und diesen Auftrag) · `ad6ea95` (S, Voraussetzungen und Vorab-Messung) · `15f28e4` (E, E-3a Schranke je Symbol, `handelbar_ab`, Wache) · danach der Abgabe-Commit „TB-166 Abgabe: Ergebnis, BACKLOG, Journal FE“, der dieses Ergebnis enthält, und „TB-166 F: porcelain und numstat“.
**Belege:** `docs/belege/TB-166/` · **Journal:** FE · **Kein Abbruch.**

Die alte `abbruch.txt` (5167e96) in `docs/belege/TB-166/` bleibt liegen (Löschen gesperrt) und ist Geschichte.

## Kurz

0a entsprach dem Soll: Zweig `main`, HEAD `e654b08`, genau 2 Einträge, die Freigabe-Karte war gefüllt. Die fünf Anhänge kamen mit den Soll-sha256. V: 25 Prüfungen, kein NEIN. S: Die Vorab-Messung ist zeilengleich mit dem Bau (30 Wechsel, alle am oder nach dem Schnitt). E: Die Referenz der alten Bahn entstand vor dem Patch. `WZ e3a` hat die 20 Dateien mit den Hashes aus dem Bau geschrieben. Beide neuen Tests sind grün (11 von 11, 47 von 47), dazu alle elf alten Tests mit rc 0, darunter `test_vorregistrierung.py` mit 196/196 (G6 grün nach TB-167). Kein Lauf auf Kursdaten, kein Registereintrag, kein neues Abbild.

## V — `v_voraussetzung.txt` (wörtlich)

```
ja    sha256 vorher research/exposure_messung/bot_lauf.py
ja    sha256 vorher research/faltenplan_neun/faltenschranke_messung.py
ja    sha256 vorher strategies/elliott_wave/elliott_wave_counter.py
ja    sha256 vorher strategies/elliott_wave/equity_simulation.py
ja    sha256 vorher strategies/elliott_wave/multi_symbol_optimise.py
ja    sha256 vorher strategies/elliott_wave_stocks/elliott_wave_counter.py
ja    sha256 vorher strategies/elliott_wave_stocks/equity_simulation.py
ja    sha256 vorher strategies/elliott_wave_stocks/multi_symbol_optimise.py
ja    sha256 vorher strategies/rsi2_crypto/backtest_rsi2.py
ja    sha256 vorher strategies/rsi2_crypto/equity_simulation.py
ja    sha256 vorher strategies/rsi2_mean_reversion/backtest_rsi2.py
ja    sha256 vorher strategies/t3_supertrend/backtest_trend.py
ja    sha256 vorher strategies/t3_supertrend/equity_simulation.py
ja    sha256 vorher strategies/t3_supertrend/multi_symbol_optimise.py
ja    sha256 vorher strategies/turtle_soup_crypto/backtest_turtle_soup.py
ja    sha256 vorher strategies/turtle_soup_crypto/equity_simulation.py
ja    sha256 vorher strategies/turtle_soup_stocks/backtest_turtle_soup.py
ja    sha256 vorher strategies/volatility_breakout/backtest_breakout.py
ja    sha256 vorher strategies/volatility_breakout_crypto/backtest_breakout.py
ja    sha256 vorher strategies/volatility_breakout_crypto/equity_simulation.py
ja    Register endet mit 63, 64 fehlt
ja    R98 genau einmal im Register
ja    research/faltenplan_neun/test_handelbar_tag.py noch nicht da
ja    shared/test_schranke_signalpfad.py noch nicht da
ja    TB-166 noch nicht abgegeben (BACKLOG ohne 'gebaut mit TB-166', kein Journal-Block, kein Ergebnis)
Pruefungen: 25, NEIN: 0
rc 0
rc 0
```

## S — `s0_vorab.txt` (wörtlich)

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
rc 0
```

Zeilengleich mit der Liste im Auftrag; kein Wechsel vor dem Schnitt, `alte Rechnung >= Schnitt` = Zahl der Abweichungen (30).

## E — Testzeilen (letzte Zeile je Beleg, davor die Zählzeile)

| Beleg | Zählzeile | letzte Zeile |
|---|---|---|
| `e_ref.txt` | 9 Bots `REF …` (n 246/520/83/73/247/84/89/21/30) | rc 0 |
| `e_e3a_probe.txt` | Pruefungen: 22, NEIN: 0 | rc 0 |
| `e_e3a.txt` | Pruefungen: 42, NEIN: 0 | rc 0 |
| `e_test_handelbar.txt` | 11 von 11 Pruefungen bestanden | rc 0 |
| `e_test_schranke.txt` | 47 von 47 Pruefungen bestanden | rc 0 |
| `e_alt_strategies_rsi2_mean_reversion_test_posten3_durchreichung.txt` | 16/16 Pruefungen bestanden. | rc 0 |
| `e_alt_strategies_volatility_breakout_test_posten3_durchreichung.txt` | 43/43 Pruefungen bestanden. | rc 0 |
| `e_alt_strategies_volatility_breakout_crypto_test_posten3_durchreichung.txt` | 42/42 Pruefungen bestanden. | rc 0 |
| `e_alt_research_faltenplan_neun_test_horizontbeginn.txt` | 61/61 Pruefungen bestanden. | rc 0 |
| `e_alt_research_faltenplan_neun_test_min_history.txt` | 14/14 Pruefungen bestanden. | rc 0 |
| `e_alt_research_vorregistrierung_test_vorregistrierung.txt` | 196/196 Pruefungen bestanden. | rc 0 |
| `e_alt_research_vorregistrierung_test_ersatzwerte.txt` | 99/99 Pruefungen bestanden. | rc 0 |
| `e_alt_shared_test_zuteilung.txt` | Ergebnis: 71 bestanden, 0 fehlgeschlagen | rc 0 |
| `e_alt_shared_test_arbeitsbaum_laufbereich.txt` | 26 von 26 Pruefungen bestanden, 0 fehlgeschlagen. | rc 0 |
| `e_alt_research_backtest_defaults_test_backtest_defaults.txt` | 59/59 Pruefungen bestanden. | rc 0 |
| `e_alt_research_universum_trockenlauf_test_universum_trockenlauf.txt` | 163/163 Pruefungen bestanden. | rc 0 |

Gegenüber den Belegen aus dem Lauf von `5167e96` änderten sich nur fünf Dateien. `e_ref.txt`/`e_ref_alt.json` und acht der elf alten Testbelege sind bytegleich. `e_e3a*.txt` zeigen den neuen ews-Hash vorher `0298263c…` ⇒ nachher `341b1712…`. `test_vorregistrierung` ist jetzt 196/196, vorher 195/1. In `test_horizontbeginn` ist die erste Falte von elliott_wave_stocks jetzt 2017 statt 2021 (Folge von TB-167). In `test_arbeitsbaum_laufbereich` unterscheiden sich nur Temp-Pfad und Prüfstand des Klons.

## Entwurf Tatsachennotiz nach 37.3 (`e_notiz.md`, wörtlich)

**Hash-Übergänge nach 37.3** (R98 (c): eine Freigabe je Bauauftrag; Sperrlistenpunkte 9/11) — Entwurf, nicht eingetragen; volle Hashes (39.5):

| Datei | Punkt | vorher | nachher | Commit | vollzieht |
|---|---|---|---|---|---|
| `research/exposure_messung/bot_lauf.py` | — | `203d96203aa8e86a32610bbae40fcca911554f56a98b971f5cc8c475c766f50a` | `95e4c567680b15889b1d80b6827dcbac6cdde8de639767eb7521546dc2876e71` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `research/faltenplan_neun/faltenschranke_messung.py` | — | `049bb657ff9d4f81e8fcfda94559d4e40668bcca7a76bc07488dce80510cf91b` | `5383f4ed41a86b7bc0e3ba15c51adf96520bb1e54d58507f2503cab70301572f` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/elliott_wave/elliott_wave_counter.py` | 11 | `8209e503b2f979f8900f49d458ff538009c2da94bb86240cce710f3870fb66fe` | `a57ab89413968aee9dbe5f256f44e0dde11131cb373b357de0da2d4c9a57a3a1` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/elliott_wave/equity_simulation.py` | 11 | `f45e92cdac5a4f03d3bd2f10165034d27b20603846e3072d02a7baf807cd127b` | `79d0a611bc8b4caed00db798e625f71e46b551af5e70a194323933d7b103ba00` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/elliott_wave/multi_symbol_optimise.py` | 11 | `ba3f5fdcf42537d586144174401c6dbf1e93a1f62476083fb3184028c3b2ce6c` | `d470a8b3d877dcd91b9e33ea40ba390e19200a4923140b54a532a561b5d9d209` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/elliott_wave_stocks/elliott_wave_counter.py` | 11 | `ed97e0f1bfbcb8c1fe5676b64f5d8a4cbdaf8be8448062616edfe20bdda62cbf` | `6ce7966f07d3bb3348f0f6ab1d335a547707da088010c740a0427b5a312755e5` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/elliott_wave_stocks/equity_simulation.py` | 11 | `80ea2a331538bbe6270a97c03627c3393c56848bfff00d9a9d44024fc0768a21` | `1ebde5ec7c067e73639c00495d481c09f130ebec23e51c3e90a3f79ea447dd5b` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | 11 | `0298263c755c5d24ccff09c35aa447efd4fff70f05223942813361955e0362e6` | `341b1712bfe9334d592e6680804b7f0344008f13d7711ce3a822749ca84b8811` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/rsi2_crypto/backtest_rsi2.py` | 9/11 | `84930445e34940775f6fcc6715616eb77589fc960f988a19b26199f1393e1aca` | `8de8a3fe35c31624d2a85495f9d73cf88a08d537fd0c22b3e889e55e09266691` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/rsi2_crypto/equity_simulation.py` | 11 | `1406de58ad920116d15a08384b88b78d37ee4944c925ff36fddedd123963e9ab` | `30d3b2873883a6a2b2dc09e72d01bbd6b0db82551a745882481e1fec810c0b5a` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/rsi2_mean_reversion/backtest_rsi2.py` | 9/11 | `836b032a5962c7766e7ed00a75b90ded4155b769fce54a84fead3c4cd5f3b7fc` | `484a964c0b80c0260d81e0a49195466f4f3d6aab1c0121a8abbd6cca840cc10b` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/t3_supertrend/backtest_trend.py` | 9/11 | `7a764353d092e521cc24b80ae97193d624224b38a6a62a45394360fe50cb04bb` | `aade6aa8effc3fa9e095e8b57d6059ffb51d12091bbfa03dc937ab4f7c31797e` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/t3_supertrend/equity_simulation.py` | 11 | `0aed45b7e8d1a0386c381fc462f96233723ff9036e863e70741e2c224fc6ef1b` | `2ffe378ff0b67efb63490f70a1bfae384044d096da40825788568e37db0c970a` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/t3_supertrend/multi_symbol_optimise.py` | 11 | `e314d7bf7bb35854c9280a5b51362f2c8a6c33771a06188a14afee7c8ff39f14` | `af458d97fd77d8057e292f500e8b9c7584d93bccc8d43274a0b541a6f35932cb` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/turtle_soup_crypto/backtest_turtle_soup.py` | 9/11 | `0704c9a96898ede99e9cf2b153da33d0cb885bf16c89e642d8514f277e8a0089` | `3f5faf8d3e00e9a92e6d61caa7684513343c99972693c497cf1cadf539e2ab3f` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/turtle_soup_crypto/equity_simulation.py` | 11 | `f0638e8e92ae98683385ea3082fbc8c56db4bc74631001c147eef54f70d7ea03` | `836f985229284f703a9a915434a60fa8b24579e63ddca9a303e8c3fd9c43237f` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/turtle_soup_stocks/backtest_turtle_soup.py` | 9/11 | `0de39bf20bbbd3c0988b270262728a08cddc79a448fd0300c2f6b94998df50bb` | `b7922129a00d2917d1d0750fb796f3e939e075c9f95cf5988b1849f8bb05b0f2` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/volatility_breakout/backtest_breakout.py` | 9/11 | `3fd0cef6c284a8806cace3663c241295edbb1ef8ee79092abfd0dc55e2bf6a76` | `feb8875d484513b0289f563aee964387063b0cc413be612db43e2b3e8b0931fd` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/volatility_breakout_crypto/backtest_breakout.py` | 9/11 | `3c7ccbe792ea5eb8dcbc76ae27079f4d7c47ca34bd3ad5edd332d4fdad3c403e` | `3743abd82984359328b125f9c3c221fe5d0e70ef5f2a2b066a6f40879df1b30c` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |
| `strategies/volatility_breakout_crypto/equity_simulation.py` | 11 | `1109438768c00e10710740775a30de8f3ac9f4309e24b3c54b13266d07df9fad` | `e16cf02297e2a6161307c4d398b3ac73db3db6fa249afa06185ead1b6e9bdc62` | `15f28e4` | E-3a (R90 (c)–(e), R98 (a), (b)) |

Neu (kein Vorher), Commit `15f28e4`: `research/faltenplan_neun/test_handelbar_tag.py` `d90934f89a686c008bcb9e36ae8fac2ab76e9e2f564a51d19f659cd4acee23ce`, `shared/test_schranke_signalpfad.py` `fc4581dc4486b34847d2c34ad5ef001af5c9136650db7ca0d42ba2fb74417c6f`.
Abnahme: nach R98 (d) erst mit E-3b am Listen-Erzeuger (Probe nach R86 (d) mit Gegenprobe über die Wache nach R87 (c)); die Prüfung am Signalpfad in diesem Auftrag ist Handwerk daneben und ersetzt sie nicht.
Abbild: ein neues Abbild unter neuem Namen schliesst den Befund (37.3; Bauart 50.3) — erst vor dem Tag, nicht in diesem Auftrag.
Vorab gemessen (`docs/belege/TB-166/s0_vorab.txt`): 30 Symbole wechseln von einem Handelbar-Tag am oder nach dem Schnitt auf None, keines liegt vor dem Schnitt; `benchmark_drawdowns.json` (Punkt 4) bleibt unberührt (letzte Falte endet am Schnitt; `handelbar_ab` steht nicht in der Datei).

**Freigabe** (Karte des Betreibers, wörtlich aus dem Auftrag, Abschnitt „Freigabe des Betreibers (R98 (c))“):

> Karte des Betreibers im Chat 31 („Opus Trading Bots-16.10.2026 a“), 16.10.2026, 15:12, Frage und Antwort im Wortlaut (aus logs/steuernder_chat/2026-10-16_BETREIBER_chat31_karten.md, per Skript): Your questions have been answered: "Neue Freigabe für TB-166 (E-3a) auf dem neuen Stand e654b08? Deine Karte vom 15.10. lautete: „Es ändert 18 Dateien der Sperrliste, Punkte 9/11 … Bedingungen: Der frische Gegenleser findet keinen A-Befund, alle Tests sind grün, und die Simulation ist gut. Es gibt keinen Lauf auf Kursdaten, kein Live, kein Geld; die Hashes alt/neu je Datei kommen ins Register.“ Sie nennt keinen Hash und keinen Commit, wurde aber für den alten Stand gegeben. Seitdem hat sich nur der ews-Optimierer geändert, durch die Abhilfe TB-167 (von mir nachgemessen). E-3a läuft dort unverändert durch und lässt die Abhilfe unberührt; ews hat nachher 341b1712… statt früher 4f1ed9c0…. Alles andere bleibt gleich. Meine Empfehlung: neue Karte, mit denselben Bedingungen, auf den neuen Stand bezogen. So steht im Register eindeutig, welchen Stand du freigegeben hast. Der Gegenleser läuft schon; senden kommt erst nach einer eigenen Karte „Senden?“."="Neu, bedingt (Recommended)"

Die Abnahme nach R98 (d) erfolgt erst mit E-3b am Erzeuger.

## Offen

- Registereintrag der Tatsachennotiz (Folgeauftrag, wie TB-122 → 50.3).
- Neues Sperrlisten-Abbild unter neuem Namen erst vor dem Tag (37.3).
- E-3b (Listen-Erzeuger: `benchmark.py`, die vier Aktien-Lader, `positionen_holen.py`, `alle_bots.py`) mit der Abnahme nach R98 (d).

## Abweichungen

- Keine Abweichung vom Soll. `test_vorregistrierung.py` lief länger als 600 s (wie in TB-167 gemessen). Damit die Zeitgrenze von 600 000 ms ihn nicht abbricht, lief der Befehl unverändert als Hintergrundaufruf derselben Sitzung, rc 0. Die übrigen Befehle liefen jeweils in einem eigenen Aufruf im Vordergrund.
- `test_arbeitsbaum_laufbereich.py` ist am Gerät grün (26/26, K0 rc 0). Der Auftrag führte ihn als offen („K0 rc 2 vorher wie nachher, Umgebung“). Ein Vorher-Lauf auf diesem Stand ist nicht gemessen.
- Die Belege `e_ref_alt.json`, `e_ref.txt`, `s0_vorab.json`, `s0_vorab.txt` und acht alte Testbelege sind bytegleich zu den in `5167e96` verfolgten Fassungen und erscheinen deshalb nicht als geändert in den Commits.

## In einfacher Sprache

Ab jetzt rechnen alle neun Bots den Tag, ab dem ein Symbol genug Kursgeschichte hat, mit einer einzigen gemeinsamen Funktion. Dafür zählen nur Kursdaten vor dem 01.09.2026. Im Scan lässt jeder Bot vor diesem Tag keinen Einstieg mehr zu; ein späteres Signal steigt normal ein. Sechs Bots haben früher zu frühe Trades erst hinterher gestrichen. Diese Bots brechen jetzt mit einem Fehler ab, falls doch einmal so ein Trade entsteht. Geprüft wurde mit erfundenen Kursreihen: Beide neuen Tests und alle elf alten sind grün. Kein Bot lief auf echten Daten. Die 18 gesperrten Dateien wurden mit der Freigabe des Betreibers geändert. Ihre alten und neuen Prüfsummen stehen oben als Entwurf; ins Register kommen sie in einem eigenen Auftrag. Abgenommen wird erst mit E-3b.
