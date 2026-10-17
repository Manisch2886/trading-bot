# REGISTER-KOPIE Abschnitt 64 (von 0–67) — Register-Z. 12429–12483 — Commit 3a00cf8c9f5f7080c75a94e2a44518ed721fed09 — 2026-10-17 — Original sha256 8f464607b313cfe74132bf244fcc94fe3618d9171d8b3cbf44fa7a207eae235a — KOPIE, nicht das Register

## 64. Vollzug TB-166 (Tatsachennotiz nach 37.3; E-3a Schranke je Symbol) mit Abnahme nach R98 (d) (TB-169)

Reines Eintragen, Bauart 63.1 (Register Z. 12372 ff.); Karte des Betreibers (Auftrag TB-169, Abschnitt Freigabe, wörtlich): „Karte des Betreibers im Chat 32 („Opus Trading Bots-16.10.2026 b“), 16.10.2026, 20:25, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript): Your questions have been answered: "Gibst du TB-169 frei? E-3b ändert zwei Dateien ausserhalb der Sperrliste (positionen_holen.py, alle_bots.py): Schnitt an der Eingabe, Wachen mit Ausgang 2, der Doppellauf fällt weg. Die neue Probe test_listen_erzeuger.py ist die Abnahme von E-3a nach R98 (d). Danach folgt der Vollzug nach 37.3: Die 20 Hash-Übergänge aus TB-166 (e_notiz.md, Hashes nachgemessen) kommen als Register 64 ins Register, Bauart 60/63. Bedingungen: Der frische Gegenleser findet keinen A-Befund, alle Tests sind grün, die Simulation ist gut. Der Vollzug läuft nur, wenn die Abnahme grün ist. Es werden keine Listen neu erzeugt, es gibt keinen Lauf auf Kursdaten, kein Live und kein Geld. Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: bedingt freigeben. Das spart eine Mac-Runde, und der Vollzug hängt maschinell an der grünen Abnahme."="Bedingt freigeben (Recommended)". You can now continue with these answers in mind.“ Eingetragen am 16.10.2026 mit TB-169 (Stand `69539db`). Nichts entfernt, kein bestehender Satz umgeschrieben; kein neues Abbild; keine Marke.

### 64.1 Vollzug TB-166 (Tatsachennotiz nach 37.3)

*Übernommen zeichengleich aus `docs/belege/TB-166/e_notiz.md` (Commit `4a51876`, md5 `e28885ae5e10e158860fb457671ce900`), dem Entwurf aus TB-166 (Ergebnis TB-166, Abschnitt „Entwurf Tatsachennotiz nach 37.3“). Vollzogen in Commit `15f28e4` (TB-166 E). „Entwurf, nicht eingetragen“ darin beschreibt den Stand in TB-166; eingetragen ist der Übergang mit diesem Abschnitt.*

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

**Freigabe-Karte TB-166, wörtlich** (zu R98 (c); aus `docs/auftraege/MAC_TB-166_e3a_schranke_je_symbol.md` Z. 14, Commit `57a1062`, md5 `57d05b949318d95e5ef28a5692ef1241`):

> Karte des Betreibers im Chat 31 („Opus Trading Bots-16.10.2026 a“), 16.10.2026, 15:12, Frage und Antwort im Wortlaut (aus logs/steuernder_chat/2026-10-16_BETREIBER_chat31_karten.md, per Skript): Your questions have been answered: "Neue Freigabe für TB-166 (E-3a) auf dem neuen Stand e654b08? Deine Karte vom 15.10. lautete: „Es ändert 18 Dateien der Sperrliste, Punkte 9/11 … Bedingungen: Der frische Gegenleser findet keinen A-Befund, alle Tests sind grün, und die Simulation ist gut. Es gibt keinen Lauf auf Kursdaten, kein Live, kein Geld; die Hashes alt/neu je Datei kommen ins Register.“ Sie nennt keinen Hash und keinen Commit, wurde aber für den alten Stand gegeben. Seitdem hat sich nur der ews-Optimierer geändert, durch die Abhilfe TB-167 (von mir nachgemessen). E-3a läuft dort unverändert durch und lässt die Abhilfe unberührt; ews hat nachher 341b1712… statt früher 4f1ed9c0…. Alles andere bleibt gleich. Meine Empfehlung: neue Karte, mit denselben Bedingungen, auf den neuen Stand bezogen. So steht im Register eindeutig, welchen Stand du freigegeben hast. Der Gegenleser läuft schon; senden kommt erst nach einer eigenen Karte „Senden?“."="Neu, bedingt (Recommended)"

**Abnahme nach R98 (d)** (gemessen in TB-169 Schritt E am Erzeuger, Commit `8520d9e`): `research/tb24_haltedauern/test_listen_erzeuger.py` auf einem Test-Snapshot, geprüft an den Ausgaben von `positionen_holen.py` (Probe nach R86 (d) mit und ohne Zeilen ab dem Schnitt; Wachen nach R86 (d) und R87 (c) je allein beissend, 41.1 A5; Fall nach R90 (g), Tatsachennotiz für t3_supertrend und die zwei Elliott-Bots im Beleg; Symbol nach R81 (h); offene Position nach R86 (c)); Beleg `docs/belege/TB-169/e_abnahme.txt`: „Ergebnis: 117 von 117 bestanden“, `rc 0`; Kerzen-Probe `docs/belege/TB-169/e_kerzen.txt`: „Ergebnis: 25861 Trades verglichen, 0 abweichend oder ohne Kursreihe“.

> ⭐ **64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R105 (65.2)** (Fable 16c R105, Unterpunkt (c), TB-170, 17.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R106 (66.1)** (Fable 17a R106, Unterpunkt (c), TB-173, 17.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **64.1, Absatz „Abnahme nach R98 (d)“ ERGÄNZT durch R107 (67.1)** (Fable 17b R107, Unterpunkt (b), TB-175, 17.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

**Sperrlisten-Sonde zu Punkt 11** (gemessen in TB-169 am Stand `69539db`; Aufruf wie TB-168 Schritt S: `trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`, Abbild `46f0ad5d…`; Beleg `docs/belege/TB-169/s_sonde.txt`): Punkt 11 „nicht prüfbar“ (`2`). Das Abbild führt keine der 20 Dateien — wie bei 60.1 und 63.1. Der Übergang steht deshalb nur hier und in den Commits.

