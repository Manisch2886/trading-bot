# REGISTER-KOPIE Abschnitt 1 (von 0–50) — Register-Z. 52–95 — Commit db108a68ec57316250ca792a0673b5932dd0f0e8 — 2026-10-01 — Original sha256 b58046592205bfac803f2e590385924dc5c0fd80fa7943c9a9d5cff40cfbbea1 — KOPIE, nicht das Register

## 1. Die zwölf Festlegungen des Betreibers (14.09.2026)

Nicht neu verhandelt — eingetragen. Sie stehen maschinenlesbar in
`research/vorregistrierung/registerdaten.py::FESTLEGUNGEN`.

| # | Festlegung | Wert |
|---|---|---|
| 1 | Führendes Mass | **Kapital-Drawdown** aus `equity_simulation.py` |
| 2 | Selektionsstatistik | **Median des Netto-Sharpe über die Selektionsfalten** |
| 3 | Beurteilung | Netto-Calmar, daneben Mittelwert der **drei tiefsten** Drawdowns und Netto-Sharpe |
| 4 | Drawdown-Bedingung je Falte | **`erlaubt(f) = min(1,25 × DD_Benchmark(f), DD_Toleranz)`** — beide negativ, `min` ist der **tiefere** und damit grosszügigere Wert |
| 5 | `DD_Toleranz` | **Median der Benchmark-Drawdowns über alle Selektionsfalten, je Bot** |
| 6 | **Keine absolute Drawdown-Grenze** | Begründung in Abschnitt 4.3 |
| 7 | Schwelle für Zweijahres-Falten | **30 Trades je Jahr** |
| 8 | Spitzen-Schwelle der Plateau-Regel | **50 %** über dem Nachbarschaftsmittel |
| 9 | Cluster-Schwelle für N_eff | Korrelation **0,9** |
| 10 | DSR-Basis | **N = 653**, dieser Lauf zählt dazu |
| 11 | **DSR ist Bericht, nicht Tor** | Bleibt-Geht läuft über die Abbruchkriterien |
| 12 | Das zulässige Ergebnis | siehe unmittelbar unten — **wörtlich** |

> ⭐ **Festlegung 1 PRÄZISIERT durch Abschnitt 24 (TB-71, 20.09.2026, Betreiberentscheidung 18:15) — der Wortlaut bleibt stehen.** Führendes Mass bleibt der Kapital-Drawdown; gerechnet wird er für die Nebenbedingung auf der täglichen Mark-to-Market-Reihe des Kapitalpfads (Registertext 1a), nicht auf der ereignisindizierten Kurve aus `equity_simulation.py`, die Berichtswert bleibt.

> ⭐ **Festlegung 4 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (a), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **Festlegung 3 PRÄZISIERT durch R48 (48.16)** (Fable 29b R48, Unterpunkt (j), TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

> ⭐ **Festlegung 2 ERGÄNZT (Verweis) durch R51 (48.19)** (Fable 29b R51, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### Festlegung 12, wörtlich

> **Dieses Ergebnis ist zulässig: Es kann sein, dass kein einziger Bot die
> Schwelle erreicht.** Eine Aussage über den **Backtest**, nicht über die
> Bots. *Wer das vorher nicht aufschreibt, wird es nachher nicht
> akzeptieren.*

Der Satz steht als Zeichenkette in `registerdaten.py`, wird von
`auswertung.py` am Ende jeder Bleibt-Geht-Liste ausgegeben und ist damit
Bestandteil jedes Berichts — auch desjenigen, in dem er unangenehm ist.

---

