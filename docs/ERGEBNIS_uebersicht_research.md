# Ergebnis: die Urteile aller `research`-Untersuchungen (Kurzfassung)

Stand 2026-09-12 · Vollständig: `docs/UEBERSICHT_RESEARCH.md`

**Es sind 18 Ordner, nicht 17.** Zwei davon (`parameter_doku`,
`uebersprungene_trades`) haben kein `BERICHT.md`.

---

## Die drei Sätze, auf die es ankommt

1. **`hrp_portfolio` ist heute anders zu lesen, als die Aufgabenstellung annahm.**
   Der Vorsprung von +0,14 Calmar für HRP stammt aus Nachtrag Z. **Nachtrag V hat
   ihn zurückgedreht: −0,0432.** Nachtrag W bestätigt das. Gültig: HRP bringt
   keinen Vorteil — Abstand 0,7 %, also kaum ein Unterschied.

2. **`trend_overlay` steht auf genau der Lücke, die HRPs Ergebnis gedreht hat.** Es
   fehlt dort der Regimefilter-Nachtrag; die eigene Annahme Z4.1 benennt die Lücke.

3. **`order_sensitivity` misst eine Konfiguration, die es nicht mehr gibt** (vor der
   Sync-Reihe, vor dem Look-Ahead-Fix). Die Schlussfolgerungen halten trotzdem, weil
   sie gepaarte Vergleiche sind — die absoluten Zahlen nicht.

---

## Urteile

| Ordner | Urteil | Grundlage überholt | Nutzer&shy;entscheidung offen |
|---|---|---|---|
| `hrp_portfolio` | offengelassen; aktuell HRP **nicht** besser (−0,04) — **3× gekippt** | **ja** | ja |
| `trend_overlay` | hält: gesamt besser, OOS wirkungslos, Wirkung nur 2022 | **ja** | ja |
| `order_sensitivity` | betroffen ja (bis 12,1×); keine der 6 Entscheidungen kippt | **ja** | ja |
| `volatility_scaled_sizing` | **nein** — schadet bei 8 von 9; Gewinner nur `rsi2_crypto` | teilweise | ja |
| `elliott_wave_params` | Krypto **ja** (10 %/6 %); Aktien **nein** | teilweise | ja |
| `oos_take_profit` | Fehler behoben (Absturz, kein falscher Wert) | ja (durch PR #48 ersetzt) | nein |
| `sync_check` | erst 5 von 9 abweichend → **alle neun synchron** | teilweise | teilweise |
| `trailing_stops` | **nein** — nur Drawdown belegbar, Calmar bei keinem Bot | nein | ja |
| `vbc_deepdive` | „doppelte Bestätigung" trägt nicht; übrig: Drawdown-Reduktion | nein | ja |
| `exposure_messung` | −1,43 % ist keine Risikokennzahl; „überwiegend Kasse" ist falsch | nein | ja |
| `elliott_wave_lookahead` | Look-Ahead bestätigt, beide Kanäle behoben | n. z. | ja |
| `oos_positionslimit` | behoben; 14 von 128 Trades betroffen, nicht 8 | nein | ja |
| `backtest_defaults` | 9 Konstanten gekoppelt, keine Wertabweichung | teilweise | ja |
| `forward_test_sync` | umgesetzt, Verhalten identisch (11/11, 15/15) | nein | teilweise |
| `datenluecke_wurzelkorrektur` | **nein** zur Wurzelkorrektur; Cron später ist flacher | nein | **ja** (Cron-Zeit) |
| `pnl_2025_fixed_size` | bewusst kein Urteil | teilweise | nein |
| `parameter_doku` | *kein Bericht* — 2 von 20 Fundstellen sofort falsch | n. z. | nein |
| `uebersprungene_trades` | *kein Bericht* — 115 Übersprünge, alle wegen **Limit** | n. z. | nein |

---

## Die veralteten Kapitalkurven (Quelle: `exposure_messung`, Abschnitt 7)

Fünf von neun `results/*/equity_curve.csv` beschreiben nicht mehr den laufenden Bot:
`elliott_wave` 144 → 130 · `elliott_wave_stocks` 469 → 395 · `rsi2_mean_reversion`
2.641 → 4.232 · `turtle_soup_stocks` 1.887 → **8.915** · `volatility_breakout`
1.236 → 1.454. Mit frischen Kurven wird aus dem kombinierten Drawdown von −1,43 %
ein Wert von **−9,41 %**. Dieselben Dateien speisen die Montags-Mail und die
Dashboard-Portfolio-Sicht.

**Zwei Merges nach fast allen Berichten:** PR #57 (2026-09-09, BTC-Regimefilter im
VBC-Backtest) und PR #81 (2026-09-12, Kurslücken im Trade-Pfad **aller neun Bots**).

---

## Die Einsichten, die bleiben

* Was die Ertragsverteilung **oben** beschneidet, kostet mehr, als es an Risiko
  spart — Vol-Skalierung verkleinert die Position genau dann, wenn Trendfolger am
  meisten verdienen. Zwei unabhängige Untersuchungen, dasselbe Muster.
* Der Engpass ist das **Positionslimit**, nicht das Kapital (praktisch 100 % der
  Ablehnungen über alle neun Bots).
* Eine Messung, die etwas anderes misst als gemeint, sieht **besonders beruhigend**
  aus: Bot-Kapitalkurven bewegen sich nur an Ausstiegstagen, deshalb korrelieren sie
  mechanisch nahe null. Zu Marktpreisen bewertet: Beta bis +0,82.
* Eine Abweichung, die kein Parameter ist, findet keine Konstanten-Prüfung — der
  BTC-Regimefilter durchdrang alle fünf Profitabilitäts-Studien.
