# REGISTER-KOPIE Abschnitt 60 (von 0–71) — Register-Z. 12240–12284 — Commit fd8f27705d7c47212587c0d7b475c3be206dd989 — 2026-10-17 — Original sha256 df17ea87835b662c960e35a530035f06359fb7ac6d0042bef5d37fe0c00ef837 — KOPIE, nicht das Register

## 60. Vollzug TB-163 (Tatsachennotiz nach 37.3) und Tatsachennotiz Posten 5 (TB-164)

Reines Eintragen, Bauart 50.3 (Register Z. 11198–11242); Karte des Betreibers 15.10.2026, 19:27: „TB-164 bauen — Registerabschnitt 60 „Vollzug TB-163“ (Hash-Übergang 37.3, Bauart 50.3, Entwurf ERGEBNIS_TB-163 Z. 109–123 zeichengleich) + Tatsachennotiz Posten 5 (R43); vorher Sonde lesend messen, Z. 129 richtigstellen; kein neues Abbild; ohne Prüferrunde (Ja, Recommended).“ Eingetragen am 15.10.2026 mit TB-164 (Stand `1d037f9`). Nichts entfernt, kein bestehender Satz umgeschrieben; kein neues Abbild; keine Marke.

### 60.1 Vollzug TB-163 (Tatsachennotiz nach 37.3)

*Übernommen zeichengleich aus dem Entwurf in `docs/ERGEBNIS_TB-163_register59_posten4_horizont.md` Z. 111–123 (Commit `d81dc88`, md5 `9e4c8f7df087bb25f3b7dba93e51119e`); Z. 109 ist die Überschrift des Entwurfs und gehört nicht dazu; Z. 113–123 sind `docs/belege/TB-163/e_uebergang.md`. Vollzogen in Commit `11a267f` (TB-163 E). „Entwurf, nicht eingetragen“ darin beschreibt den Stand im Ergebnis; eingetragen ist der Übergang mit diesem Abschnitt.*

Freigabe: dritte Karte des Betreibers, 15.10.2026, 18:24: „Einzelfreigabe nach 37.3 für E-6 (Posten 4, Horizont je Bot, vier Aktien-Optimierer), Auftrag mit R81 (d) und Tatsachennotiz TB-162 als Abschnitt 59 (Ja, Recommended).“

**Hash-Übergänge nach 37.3** (Sperrlistenpunkt 11, „Commit-Hashes von Simulation, Erkennung, Optimierern“) — Entwurf, nicht eingetragen; volle Hashes (39.5):

| Datei | vorher | nachher | Commit | vollzieht |
|---|---|---|---|---|
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | `275273776fafb2453cdb41f634b86bacffd5994f8b5508ef034400cd7c5ede9d` | `3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232` | `11a267f` | E-6 (Posten 4; R44, R81 (d)) |
| `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | `777f5cb0a637bb8770d1cd4a89aac03c6b29db98d13ce47eac6de29db279c661` | `61838aca901cabeace70511b71742d10cba4de6575a999aecf5a492f938ad6dc` | `11a267f` | E-6 (Posten 4; R44, R81 (d)) |
| `strategies/turtle_soup_stocks/multi_symbol_optimise.py` | `e4277f013be6d0af85647f5d32d8cdb60ef086d06c6e041853c6da571c96ddd4` | `29e7f10c3eb79f8316c53c9a31ee3ea0dd450d44bb9904dc2ba9944df003c0cc` | `11a267f` | E-6 (Posten 4; R44, R81 (d)) |
| `strategies/volatility_breakout/multi_symbol_optimise.py` | `f0a4ee43dca133e89272e48d80280d8a22f57d751d2ddac06751fd091198af2d` | `24c182ae1cf7c882c9e3aec31c5088348e2fa44c5cc2e99eab54ecf29b337585` | `11a267f` | E-6 (Posten 4; R44, R81 (d)) |

Neu (kein Vorher), Commit `11a267f`: `research/posten4_horizont/test_posten4_horizont.py` `ed13dd2cbbde0bed0e83f06f363da3f6c1c8d588d25f0fd71c73b4196039534c`.
Unverändert: `research/vorregistrierung/faltenplan.py` `63dafeb44e027cb5d93ac19cddfc7d4e98b468cece116512c2b3f1601bd4a4c7`, `strategies/volatility_breakout/backtest_breakout.py` `3fd0cef6c284a8806cace3663c241295edbb1ef8ee79092abfd0dc55e2bf6a76`.

**Sperrlisten-Sonde zu Punkt 11** (gemessen in TB-164 am Stand `1d037f9`; Aufruf wie TB-122 0b: `trading-env/bin/python3 -B -W ignore shared/sperrlistensonde.py --abbild research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-26_tb117.json`, Abbild `46f0ad5d…`; Beleg `docs/belege/TB-164/s_sonde.txt`): Punkt 11 „nicht prüfbar“ (`2`). Das Abbild führt keinen der Optimierer (kein Pfad `strategies/*/multi_symbol_optimise.py` darin) — wie bei 50.3. Der Übergang steht deshalb nur hier und in den Commits.

> ⭐ **60.1 ERGÄNZT durch R102 (62.3) und R103 (62.4)** (Fable 16b R103 (c): R102 Unterpunkte (b) und (c), R103 Unterpunkt (b), TB-167, 16.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 60.2 Tatsachennotiz Posten 5 (R43)

R43 (Register Z. 10942): „Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ (29.4, 34.5) steht im Zellen-Erzeuger — an einer Stelle, für alle neun Bots, mit dem Bericht je Bot aus 34.5 —, nicht in den neun multi_symbol_optimise.py; „in allen neun multi_symbol_optimise.py“ lies „im Zellen-Erzeuger, für alle neun Bots“; die neun Optimierer erhalten eine Tatsachennotiz „nicht im Laufpfad“.“ — „Posten 5 des Plans ist neu zu fassen (Handwerk).“ Posten 5 lautete (`docs/auftraege/MAC_TB-120_erzeuger_bestandsaufnahme.md` Z. 128): „Posten 5: Wache 29.4 in allen neun Optimierern (34.5).“ Bestand: 0 von 9 (`docs/ERGEBNIS_TB-120_erzeuger_bestandsaufnahme.md` Z. 101).

**Tatsachennotiz „nicht im Laufpfad“:** Die neun `multi_symbol_optimise.py` stehen nicht im Laufpfad der Neuselektion; die Wache 29.4/34.5 kommt in keinen von ihnen. Posten 5 heisst nach R43: die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte“ im Zellen-Erzeuger, an einer Stelle, für alle neun Bots, mit dem Bericht je Bot aus 34.5; sie kommt mit dem Bau des Zellen-Erzeugers. Stand der neun Dateien am `1d037f9` (sha256, 39.5):

| Datei | sha256 |
|---|---|
| `strategies/elliott_wave/multi_symbol_optimise.py` | `ba3f5fdcf42537d586144174401c6dbf1e93a1f62476083fb3184028c3b2ce6c` |
| `strategies/elliott_wave_stocks/multi_symbol_optimise.py` | `3b7757004b1c2db527262cbacf0f86c095729080074e73ced750b82fc8677232` |
| `strategies/rsi2_crypto/multi_symbol_optimise.py` | `7a6378a49cdf993da79d3223cc3255d027e24cc5dac25c9d12c8acd61f1350d3` |
| `strategies/rsi2_mean_reversion/multi_symbol_optimise.py` | `61838aca901cabeace70511b71742d10cba4de6575a999aecf5a492f938ad6dc` |
| `strategies/t3_supertrend/multi_symbol_optimise.py` | `e314d7bf7bb35854c9280a5b51362f2c8a6c33771a06188a14afee7c8ff39f14` |
| `strategies/turtle_soup_crypto/multi_symbol_optimise.py` | `e638e1121116e7197445b774a438e1ecc79fffc991156e6094c15f47977b42d0` |
| `strategies/turtle_soup_stocks/multi_symbol_optimise.py` | `29e7f10c3eb79f8316c53c9a31ee3ea0dd450d44bb9904dc2ba9944df003c0cc` |
| `strategies/volatility_breakout/multi_symbol_optimise.py` | `24c182ae1cf7c882c9e3aec31c5088348e2fa44c5cc2e99eab54ecf29b337585` |
| `strategies/volatility_breakout_crypto/multi_symbol_optimise.py` | `02548e2eb95e34a0afcdbacfa0d806c7406fd4b066d0b26ef3c9839bf83a082b` |

