# Regelblatt KI-Bot Regime — v1

Paper Trade, rein KI (MI1 (b) vom Betreiber 17.10.2026 nur für Paper gebrochen), streng getrennt von den neun: eigene DB, kein Eintrag in `ASSET_CLASS`/`discover_bots`, nie im Selektionslauf, nie Zulassungsgrund. Der Bot fragt selbst und liest den Sammler nicht. Fest vor dem Start; jede Änderung ist v2 und beginnt eine neue Reihe.

## Pflichtfelder

- **Version:** v1
- **Modell:** `claude-haiku-4-5-20251001` (`MODEL_HAIKU`), `tools=None`, keine Websuche
- **Topf:** `bots`, Deckel 3 $ je UTC-Monat, getrennt vom Sammler
- **Universum:** Krypto `BTCUSDT` (Binance-Spot); Aktien `IE00B5BMR087` iShares Core S&P 500 UCITS ETF (Acc), Xetra `SXR8`, EUR (Vorschlag: Instrument; ISIN aus allgemeiner Quelle, nicht im Repo belegt, vor dem Start äusserlich prüfen)
- **Entscheidungsregel:** einmal je Tag und Markt fragt der Bot das Modell nach dem Regime −2 … +2 auf eingefrorenen Eingaben (Krypto: BTCUSDT-Tageskerzen 200 Tage, Fear & Greed 30 Werte; Aktien: `^GSPC` und `^VIX` 200 Handelstage; beide: ALFRED `DFF`, `T10Y2Y`, `BAMLH0A0HYM2`); Regime ≥ +1 ⇒ long, Regime ≤ −1 ⇒ flach, 0 ⇒ keine Änderung
- **Positionsgrösse:** je Markt ein fester Teiltopf von 50 % des Startkapitals; long = Teiltopf voll investiert, flach = 0; kein Hebel, keine Leerverkäufe
- **Ausstieg:** nur über die Entscheidungsregel (Regime ≤ −1); kein Preisstopp (rein KI)
- **Startkapital:** 10 000 (Wert der neun: `STARTING_CAPITAL = 10_000.0` in allen neun `equity_simulation.py`). Ort des Startkapitals ist nach R110 (b) künftig `shared/handelskosten.py` (TB-180); die KI-Bots lesen nichts aus den neun. Krypto-Teiltopf in USDT, Aktien-Teiltopf in EUR (Vorschlag: Währung)
- **Kosten:** wie die neun: Gebühr 0,1 % je Seite (`TRADING_FEE_PCT`), Slippage 0,05 % (`SLIPPAGE_PCT`, alle neun `forward_test.py`)
- **Ausführung:** Entscheid 06:30 UTC (Vorschlag); Krypto zum Eröffnungskurs der nächsten Binance-Spot-Stundenkerze, Aktien zum Xetra-Eröffnungskurs desselben Handelstags (an Tagen ohne Xetra-Handel: nächster Handelstag)
- **Ausfall:** ungültige oder fehlende Antwort, Bremse oder Notschalter `ki_bots` ⇒ keine Änderung, Tag als `ausgefallen` gebucht; fünf Ausfalltage in Folge ⇒ Markt flach (Vorschlag)
- **Auswertedatum:** 30.04.2027 (Vorschlag); Messgrössen: Rendite, MaxDD, Zahl der Wechsel, Kosten des Modells, Vergleich mit Halten des Instruments über denselben Zeitraum
- **Abbruchregel:** Equity fällt 25 % unter ihren Höchststand ⇒ alles flach, Bot stoppt, Bericht (Vorschlag); Änderung an Blatt oder Prompt nach dem Start ⇒ Reihe v1 endet
- **Speicher:** `ki_forschung/ki_regime.db` (nur anfügend; nie `paper_trading_*`); Bau in BA4
- **Prompts:** `regime_bot.txt`
