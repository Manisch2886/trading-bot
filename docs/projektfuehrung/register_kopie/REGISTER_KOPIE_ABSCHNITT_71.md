# REGISTER-KOPIE Abschnitt 71 (von 0–71) — Register-Z. 12902–12963 — Commit fd8f27705d7c47212587c0d7b475c3be206dd989 — 2026-10-17 — Original sha256 df17ea87835b662c960e35a530035f06359fb7ac6d0042bef5d37fe0c00ef837 — KOPIE, nicht das Register

## 71. Bauauftrag nach R110 (b) und Probe nach R110 (c) — Startkapital am Ort (TB-180)

Eingetragen mit TB-180 am 17.10.2026 (Auftrag `docs/auftraege/MAC_TB-180_startkapital_am_ort_punkt9_abbild_probe.md`): Bauauftrag nach 37.3 aus R110 (b) (70.1, Fable 17e), vier Schritte, dann die Probe nach R110 (c). Handelscode mit Freigabe des Betreibers, Karte wörtlich:

> Karte des Betreibers im Chat 35 („Opus Trading Bots-17.10.2026 b“), 17.10.2026, Frage und Antwort im Wortlaut (aus dem Sitzungsprotokoll, per Skript, Zeit 2026-10-17T21:29:06.142Z UTC): Your questions have been answered: "Gibst du TB-180 frei? Das ist Handelscode. Das Startkapital zieht an den Ort, den R110 (b) festlegt. (1) shared/handelskosten.py kommt mit Pfad und Hash auf die Sperrliste (Nachtrag zu Punkt 9). (2) Dort steht die Konstante STARTING_CAPITAL = 10_000.0; die neun Bots lesen sie mit je einer geänderten Zeile aus diesem Modul. (3) Ein neues Abbild der Sperrliste. (4) Registertext zu 29.3 mit den neun Fundstellen und Commit, als Abschnitt 71. Dazu kommt die Probe in test_ergebniskurven.py am neuen Ort: Sie ändert den Wert einmal und prüft, dass alle neun Kurven abweichen. research/tb27/vergleich.py liest den Wert künftig dort. Ergebnis der Simulation: Die Kurven der neun Bots sind vorher und nachher bytegleich, das Verhalten ändert sich also nicht. Ein frischer Gegenleser hat nichts gefunden, das geändert werden muss oder sollte; es gab nur drei kleine Hinweise der Stufe „kann“. Keine Kursdaten werden geschrieben, kein Live, kein Geld. Ich ziehe den Auftrag gerade nur noch auf den Stand nach TB-179 nach, am Code ändert sich dabei nichts. Gesendet wird erst nach einer eigenen Karte „Senden?“. Empfehlung: freigeben. Damit ist das Startkapital registriert und gesperrt."="Freigeben (Recommended)". You can now continue with these answers in mind.

Commits: Stand vor dem Umbau `ebee3ef`, Umbau `f60f92b`. R109 und R110 bleiben zeichengleich.

### 71.1 Nachtrag zu Punkt 9 (Schritt (1))

⭐ **Der Punkttext von Abschnitt 10, Punkt 9, ist geändert — additiv** (Bauart 39.2). Die drei Zeilen davor und die Kästen darunter sind zeichengleich (38.4). Nach der Zeile `   Schlusskurs des Bestätigungsbalkens` stehen drei neue Folgezeilen:

```
   — Ort: `shared/handelskosten.py` mit `TRADING_FEE_PCT`, `SLIPPAGE_PCT`
   und `STARTING_CAPITAL` (sha256 `b2efabe4…` am Commit `f60f92b`; Nachtrag
   nach 38.5 und R110 (b), 71.1, TB-180, 17.10.2026)
```

| Datei | Bezeichner | Werte am Commit `f60f92b` | sha256 (Stand nach Schritt (2)) |
|---|---|---|---|
| `shared/handelskosten.py` | `TRADING_FEE_PCT`, `SLIPPAGE_PCT`, `STARTING_CAPITAL` | 0.1 / 0.05 / 10000.0 | `b2efabe4a51b26d6b9f34b1b8b9d0f5bc45b463aabd6b9bbd95237f560273a5e` |

### 71.2 Tatsachennotiz zu Schritt (2) und zur Sonde

**(a)** `STARTING_CAPITAL = 10_000.0` steht am Commit `f60f92b` in `shared/handelskosten.py` Z. 39; die neun `strategies/<bot>/equity_simulation.py` tragen keine eigene Zuweisung mehr, sondern an deren Stelle `from handelskosten import STARTING_CAPITAL` (Fundstellen vorher in 71.3).
**(b)** Kurven der neun mit `shared/kurven_lauf.py` (ohne neue Kursdaten) am Stand `ebee3ef` und nach dem Umbau, sha256 je Bot (`docs/belege/TB-180/m_vorher.txt`, `docs/belege/TB-180/n_nachher.txt`, `docs/belege/TB-180/n_vergleich.txt`): Ergebnis: 9 von 9 bytegleich (vorher gegen nachher)
**(c)** Sonde (R110 (b), 37.5 (1)): Der Datei-Hash ist die Sperre. Bis zum Tag bleibt Punkt 9 bei 2 (Regel-Bestandteil), mit dieser Notiz (37.1): Wert in Datei gleich Registerwert, am Commit `f60f92b` — `STARTING_CAPITAL` 10000.0 = 10 000 (71.3), `TRADING_FEE_PCT` 0.1 = 0,1, `SLIPPAGE_PCT` 0.05 = 0,05 (Punkt 9). Keine neue Bauart der Sonde.

### 71.3 Ergänzung zu 29.3 (Schritt (4), Fassung R110 (b))

> Das registrierte Startkapital ist 10 000, wie der Code es am Commit der Tatsachennotiz in den neun strategies/<bot>/equity_simulation.py trägt; sein Ort ist die Konstante STARTING_CAPITAL in shared/handelskosten.py (38.5), sobald dieses Modul nach 38.5 als Nachtrag zu Punkt 9 mit Pfad und Hash auf der Sperrliste steht; die Sonde prüft Datei und Wert (37.5 (1)).

**Tatsachennotiz (R108 (d) (1), 68.2 (a)) — die neun Fundstellen am Commit der Tatsachennotiz `ebee3ef`:**

- `strategies/elliott_wave/equity_simulation.py` Z. 66 `STARTING_CAPITAL = 10_000.0`
- `strategies/elliott_wave_stocks/equity_simulation.py` Z. 71 `STARTING_CAPITAL = 10_000.0`
- `strategies/rsi2_crypto/equity_simulation.py` Z. 51 `STARTING_CAPITAL = 10_000.0`
- `strategies/rsi2_mean_reversion/equity_simulation.py` Z. 62 `STARTING_CAPITAL = 10_000.0`
- `strategies/t3_supertrend/equity_simulation.py` Z. 54 `STARTING_CAPITAL = 10_000.0`
- `strategies/turtle_soup_crypto/equity_simulation.py` Z. 45 `STARTING_CAPITAL = 10_000.0`
- `strategies/turtle_soup_stocks/equity_simulation.py` Z. 68 `STARTING_CAPITAL = 10_000.0`
- `strategies/volatility_breakout/equity_simulation.py` Z. 61 `STARTING_CAPITAL = 10_000.0`
- `strategies/volatility_breakout_crypto/equity_simulation.py` Z. 61 `STARTING_CAPITAL = 10_000.0`

Der Nachtrag zu Punkt 9 steht (71.1); damit ist die Bedingung „sobald“ erfüllt.

### 71.4 Neues Abbild (Schritt (3))

`research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-10-17_tb180.json` (11780 B, sha256 `f83f0323ed2e900406f908b8ba39155fd6c6472696a1b454d2bbf238a8a2d6d9`), einmalig geschrieben mit `research/vorregistrierung/sperrliste_abbild.py` (36.6), nach 71.1. Sonde dagegen (`docs/belege/TB-180/b_sonde_neu.txt`), wörtlich: `Pfad-Bestandteile: 38 geprueft, davon 38 mit 0 / 0 mit 1 / 0 mit 2  (punkte 16, bestimmt 0, eingefroren 22)` · `RUECKGABEWERT 2 NICHT PRUEFBAR - NICHT PRUEFBAR: Punkt(e) [1, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14]`. Gegenprobe, das Abbild davor (`sperrliste_abbild_2026-09-26_tb117.json`) gegen das Register nach 71.1 (`docs/belege/TB-180/b_sonde_alt.txt`): `RUECKGABEWERT 1 BEFUND - BEFUND in Punkt(en) [] und in (ii) Abbild/Registertext`.

### 71.5 Probe nach R110 (c)

`shared/test_ergebniskurven.py` (Handwerk in der Freigabe, R31 (b)), Prüffall 11 (`docs/belege/TB-180/t_test.txt`), wörtlich:

    [OK ] neun Kurven vor der Mutation erzeugt   9 von 9
    [OK ] Mutation am Ort, genau einmal   1
    [OK ] alle neun Kurven weichen ab   9 von 9
    [OK ] zurueckgesetzt: alle neun bytegleich   9 von 9
    [OK ] der Ort im Repo blieb unberuehrt
    49 von 49 Pruefungen bestanden, 0 fehlgeschlagen.

**Kette:** R109 (a) → R110 (b) → 37.3 → 71.1 bis 71.4; R110 (c) → 71.5. Ohne Marke: R109, R110, 37.5, 38.5, Abschnitt 10 ausser dem Nachtrag.
