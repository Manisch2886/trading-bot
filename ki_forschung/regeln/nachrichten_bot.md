# Regelblatt KI-Bot Nachrichten — v1

Paper Trade, KI mit Preisbedingung (MI1 (b) vom Betreiber 17.10.2026 nur für Paper gebrochen), streng getrennt von den neun: eigene DB, kein Eintrag in `ASSET_CLASS`/`discover_bots`, nie im Selektionslauf, nie Zulassungsgrund. Einziger Bot mit RSS. Fest vor dem Start; jede Änderung ist v2 und beginnt eine neue Reihe.

## Pflichtfelder

- **Version:** v1
- **Modell:** `claude-haiku-4-5-20251001` (`MODEL_HAIKU`), `tools=None`, keine Websuche
- **Topf:** `bots`, Deckel 3 $ je UTC-Monat, getrennt vom Sammler
- **Universum:** Krypto (Binance-Spot, Vorschlag: Auswahl): `BTCUSDT`, `ETHUSDT`, `SOLUSDT`, `XRPUSDT`, `BNBUSDT`; ETF (nur UCITS, Xetra, EUR; Vorschlag: Auswahl, ISIN aus allgemeiner Quelle, nicht im Repo belegt, vor dem Start äusserlich prüfen): `IE00B5BMR087` S&P 500 (SXR8), `IE00B53SZB19` Nasdaq 100 (SXRV), `IE00B53L3W79` EURO STOXX 50 (SXRT), `DE0005933931` DAX (EXS1), `IE00BKM4GZ66` MSCI EM IMI (IS3N)
- **Nachrichtenquelle:** RSS, je Lauf eingefroren über `abrufe.py` (Quelle `rss`); Vorschlag: CoinDesk und Cointelegraph (Krypto), Yahoo-Finance-Schlagzeilen je Index (ETF); Feed-Adressen legt BA4 fest, bevor der erste Lauf schreibt; nur Titel und Kurztext der letzten 24 Stunden, höchstens 30 Meldungen je Symbol (Vorschlag)
- **Entscheidungsregel:** einmal je Tag und Symbol bewertet das Modell die eingefrorenen Meldungen mit −2 … +2; Einstieg long, wenn Wert = +2 **und** Schlusskurs des Vortags > SMA 20 (Tageskerzen, eingefroren); sonst kein Einstieg; höchstens eine offene Position je Symbol
- **Positionsgrösse:** 10 % des Startkapitals je Einstieg (1 000), höchstens zehn offene Positionen (Vorschlag)
- **Ausstieg:** nach 5 Handelstagen zum Eröffnungskurs, oder vorher bei −5 % gegen den Einstiegskurs (Stopp, auf Schlusskursbasis geprüft — Vorschlag: Prüfweise); der Ausstieg braucht kein Modell
- **Startkapital:** 10 000 (Wert der neun: `STARTING_CAPITAL = 10_000.0` in allen neun `equity_simulation.py`). Ort des Startkapitals ist nach R110 (b) künftig `shared/handelskosten.py` (TB-180); die KI-Bots lesen nichts aus den neun. Krypto-Teil in USDT, ETF-Teil in EUR (Vorschlag: Währung)
- **Kosten:** wie die neun: Gebühr 0,1 % je Seite (`TRADING_FEE_PCT`), Slippage 0,05 % (`SLIPPAGE_PCT`)
- **Ausführung:** Entscheid 07:00 UTC (Vorschlag); Krypto zum Eröffnungskurs der nächsten Binance-Spot-Stundenkerze, ETF zum Xetra-Eröffnungskurs desselben Handelstags
- **Ausfall:** ungültige oder fehlende Antwort, leerer Feed, Bremse oder Notschalter `ki_bots` ⇒ kein Einstieg an diesem Tag, gebucht als `ausgefallen`; Ausstiege laufen weiter
- **Auswertedatum:** 30.04.2027 (Vorschlag); Messgrössen: Zahl der Einstiege, Trefferquote, Netto-PnL, MaxDD, Kosten des Modells, Vergleich mit derselben Preisbedingung ohne Nachrichtenwert (Kurs > SMA 20 allein)
- **Abbruchregel:** Equity fällt 25 % unter ihren Höchststand ⇒ alles flach, Bot stoppt, Bericht (Vorschlag); Änderung an Blatt, Universum, Feeds oder Prompt nach dem Start ⇒ Reihe v1 endet
- **Speicher:** `ki_forschung/ki_nachrichten.db` (nur anfügend; nie `paper_trading_*`); Bau in BA4
- **Prompts:** `nachrichten_bot.txt`
