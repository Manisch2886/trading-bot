# FABLE-Anfrage 17.10.b — R102 (d) Vorlauf; R106 (d) t3_supertrend; Selektionsmodus; Schatten-Bots; ausgeführte Trades

*Steuernder Chat, 17.10.2026, HEAD `5031cd0`. Anfrage 17.10.b an den bestehenden Chat „Fable Trading Bots-17.10.2026 a“. **Registerfrage.** Dateien in der Projektablage unter projektfuehrung/. Zitate per Skript aus dem Register (Commit `7fe6342`, 12 596 Zeilen, sha256 `945ba13f…` = HEAD).*

## Teil 0 — Kenntnis

Register 0–66, eingetragen bis R106 (66.1, Z. 12537); R107 0 Treffer — dein Block beginnt bei **R107**. Seit 17.10.a: TB-172 (Messung R102 (d), R92 (c)), TB-173 (Register 66), TB-174 (Probe t3, 8 von 8, rc 0).

## Frage (a) — R102 (d): Indikatorwerte vor dem Horizontbeginn

1. R102 (d), Z. 12326: „ob rsi2_mean_reversion, turtle_soup_stocks und volatility_breakout Indikatorwerte aus Zeilen vor dem Horizontbeginn bilden. Wenn ja, ist das ein Befund zu 28.6 und R57 und kommt als Frage an den Verfahrensprüfer;“
2. TB-172 M1 (belegt, `m1_r102d.md`): „ja“ bei allen drei; volle CSV, `entry_cutoff` nur als `start_i` (rsi2 Z. 131, turtle_soup Z. 122, breakout Z. 172). rsi2-Docstring Z. 75–76 (über den Zeilenumbruch): „KEINE Kappung auf RECENT_YEARS_ONLY vor der Indikator-Berechnung“ (gewollter SMA(200)-Vorlauf). elliott_wave_stocks schneidet (Z. 119, E-6).
3. 28.6, Z. 5358: „Der Indikator-Vorlauf nach (i) wird gegen den Horizontbeginn des Bots gerechnet, nicht gegen den ersten Kurs im Bestand.“ R102 (c): „Indikatorwerte aus Zeilen vor dem Horizontbeginn sind derselbe Zugriff (28.6).“

**Frage:** Zulässig nach 28.6/R57, und was gilt vor der Neuerzeugung? **Neigung:** nicht zulässig; Zeilenschnitt nach Bauart E-6 je Bot nach 37.3, vor R44. **Zur Kenntnis:** R102 (c) nennt „rsi2_mean_reversion, Z. 106 vor Z. 112“ als Bauart; Z. 112 ist kein Zeilenschnitt, sondern `entry_cutoff = horizontbeginn_ts(...)` (TB-172 Punkt 3).

## Frage (b) — R106 (d): Schliesst TB-174 den Fall bei t3_supertrend?

TB-174 (`e_probe.txt`): Fall über den Gleichstand (T3 fast = slow durch Rundung, 496 Balken) in der Kopie des Test-Snapshots; Mac 8 von 8, Wahl wie am Bau (Anker 2024-06-10, L 63.0; nur dieser Kandidat gemessen). Gegenproben: Schranke aus ⇒ Wache R87 (c) mit 2; Schranke und Wachen aus ⇒ Einstieg bei s fehlt; Mutante ⇒ E2 fehlt. `use_t3_exit` am HEAD: Vorgabe True `backtest_trend.py` Z. 70, Wirkung Z. 124; `multi_symbol_optimise.py` Z. 95–103 und `bot_lauf.py` Z. 151–152 übergeben ihn nicht.

**Frage:** Schliesst TB-174 R106 (d) Weg 1, und ist die Abnahme nach R98 (d) in 64.1 für t3_supertrend vollständig? **Neigung:** ja.

## Frage (c) — R86 (e)/R92 (c): Modus der Neuerzeugung

Am Code: `positionen_holen.py` Z. 324 `es.load_all_symbol_data()`; die Aktien-Optimierer nehmen `DATA_DIR = _P["DATA_DIR"]` (rsi2 Z. 32) aus `strategy_paths` (Z. 88 `import paths`). `shared/paths.py` Z. 679 `_MODUS = _modus_aus_umgebung()`; ohne Modus Z. 685 `DATA_DIR = _LIVE_DATA_DIR` (`data/`, Z. 194), mit Modus Z. 692 Snapshot-Wurzel. Der Erzeuger setzt den Modus nicht, er schreibt ihn nur (`_schreibe_herkunft` Z. 209–210, `<bot>_herkunft.json`); `alle_bots.py` Z. 50–52 ohne eigene Umgebung. R92 (c) ist am Snapshot `63e4b6c8…` gemessen. R78, Z. 11748: „„Im Snapshot“ heisst: gelesen über den Resolver unter dem Selektionsmodus“.

**Frage:** Muss die Neuerzeugung unter dem Selektionsmodus laufen, und ist R86 (e) damit für die Aktien-Bots erfüllt? **Neigung:** ja, Pflicht; Beleg `selektionsmodus` ≠ null in `<bot>_herkunft.json`. Offen: Wache im Erzeuger oder Auftrag.

## Frage (d) — Schatten-Bots vor dem Tag

Betreiber 17.10.: „Ich möchte gerne neue Bots ins pater trading bringen und diese im Dashboard tracken“, „Primär gerne KI Integrative bots“. 16.4 (a), Z. 2083: „**Schatten** (läuft, kein Portfoliogewicht, nicht in Portfolio-Zahlen und nicht am Crash-Knopf)“. 16.8 (e): Overlays „erst nach dem Selektionslauf“. EPICS MI1: LLM „erzeugt einen strukturierten Zustand, keine Order“, „Shadow Mode vor jedem Einsatz“. K24: KI-Strategieauswahl widersprochen. BACKLOG Z. 149 S-B1: „der Backtest erst nach Rang 1“.

**Frage:** Ist ein Schatten-Sammler (LLM schreibt nur Marktzustand in eigene DB, keine Order, Dashboard-Kachel) vor dem signierten Tag zulässig, ohne Register und Selektionslauf zu berühren? Darf S-B1 vor seinem Backtest als Schatten-Bot laufen?

## Frage (e) — R97: Quelle der ausgeführten Trades für drei Leser

Seit TB-169 schreibt `positionen_holen.py` nur `<bot>_alle_trades.csv` mit `trade_zeile`, symbol, entry_time, exit_time, result, pnl_pct, entry_price, exit_price, kerzen (Z. 342–346); Meta Z. 357–372 ohne `trades_ausgefuehrt`, `startkapital`. Leser: `tb24_haltedauern/auswertung.py` Z. 71, Z. 325 `trades_ausgefuehrt`; `faltenplan_neun/embargo_neun.py` Z. 232; `mtm_drawdown/grundlage.py` Z. 65, PFLICHTSPALTEN Z. 58 mit allocation, capital_after, Z. 198 `startkapital`. R97 (b), Z. 12106: „Solange die Rückgabe nicht gebaut ist, darf sie die Positionen aus einem Lauf mit unveränderten Trades aus Trade-Liste und equity_curve rekonstruieren;“

**Frage:** Woher kommen ausgefuehrt, allocation, capital_after ohne Doppellauf (R97 (b) oder R45), oder rechnen die Leser künftig auf allen gefundenen Trades?

## Lesen und Antwort

Projektablage: REGISTER_INDEX.md; REGISTER_KOPIE_ABSCHNITT_16, _28, _51, _55, _56, _57, _58, _62, _66; ERGEBNIS_TB-172, ERGEBNIS_TB-174; m1_r102d.md. Fehlt eine Kopie, melde das. Nicht lesen: BACKLOG*, ergebnisse/, sonst docs/belege/. Antwort höchstens 10 KB als projektfuehrung/FABLE_ANTWORT_2026-10-17b_<stichwort>.md: Kurz (je Frage „einverstanden“ oder „anders, weil …“), Registerblock zeichengleich kopierbar ab R107, Leseprotokoll nach R56 (b), Ampel.
