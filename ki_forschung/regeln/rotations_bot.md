# Regelblatt KI-Bot Rotation — v1

Paper Trade, rein KI (MI1 (b) vom Betreiber 17.10.2026 nur für Paper gebrochen), streng getrennt von den neun: eigene DB, kein Eintrag in `ASSET_CLASS`/`discover_bots`, nie im Selektionslauf, nie Zulassungsgrund. Fest vor dem Start; jede Änderung ist v2 und beginnt eine neue Reihe.

## Pflichtfelder

- **Version:** v1
- **Modell:** `claude-haiku-4-5-20251001` (`MODEL_HAIKU`), `tools=None`, keine Websuche
- **Topf:** `bots`, Deckel 3 $ je UTC-Monat, getrennt vom Sammler
- **Universum:** ETF (nur UCITS, Xetra, EUR; Vorschlag: Auswahl, ISIN aus allgemeiner Quelle, nicht im Repo belegt, vor dem Start äusserlich prüfen): `IE00B4L5Y983` iShares Core MSCI World (EUNL); `IE00B5BMR087` iShares Core S&P 500 (SXR8); `IE00B53SZB19` iShares Nasdaq 100 (SXRV); `IE00B53L3W79` iShares Core EURO STOXX 50 Acc (SXRT); `DE0005933931` iShares Core DAX (EXS1); `IE00B4L5YX21` iShares Core MSCI Japan IMI (SJPA); `IE00BKM4GZ66` iShares Core MSCI EM IMI (IS3N); `IE00B52MJY50` iShares Core MSCI Pacific ex Japan (SXR1); `IE00BF4RFH31` iShares MSCI World Small Cap (IUSN); `IE00B3WJKG14` iShares S&P 500 Information Technology Sector (QDVE). Krypto (Binance-Spot, Vorschlag: Auswahl): `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `SOLUSDT`, `XRPUSDT`, `ADAUSDT`, `DOGEUSDT`, `AVAXUSDT`, `LINKUSDT`, `DOTUSDT`
- **Entscheidungsregel:** jeden Montag je Universum ein Aufruf: das Modell ordnet die zehn Werte nach erwarteter relativer Stärke für die nächste Woche, nur auf eingefrorenen Kennzahlen, die vor dem Aufruf aus den Kursen berechnet werden (Rendite 4, 12, 26 Wochen; Volatilität 20 Tage; Abstand zum SMA 50 und SMA 200; Vorschlag: Kennzahlen); gehalten werden die ersten drei
- **Positionsgrösse:** je Universum ein Teiltopf von 50 % des Startkapitals; die drei Werte je ein Drittel des Teiltopfs, wöchentlich auf gleiche Gewichte zurückgesetzt
- **Ausstieg:** ein Wert fällt am Montag aus den ersten drei ⇒ Verkauf; kein Preisstopp (rein KI)
- **Startkapital:** 10 000 (Wert der neun: `STARTING_CAPITAL = 10_000.0` in allen neun `equity_simulation.py`). Ort des Startkapitals ist nach R110 (b) künftig `shared/handelskosten.py` (TB-180); die KI-Bots lesen nichts aus den neun. Krypto-Teiltopf in USDT, ETF-Teiltopf in EUR (Vorschlag: Währung)
- **Kosten:** wie die neun: Gebühr 0,1 % je Seite (`TRADING_FEE_PCT`), Slippage 0,05 % (`SLIPPAGE_PCT`)
- **Ausführung:** Entscheid montags 06:45 UTC (Vorschlag); Krypto zum Eröffnungskurs der nächsten Binance-Spot-Stundenkerze, ETF zum Xetra-Eröffnungskurs desselben Tags (Feiertag: nächster Handelstag)
- **Ausfall:** ungültige Antwort (nicht genau zehn verschiedene Werte des Universums) oder fehlender Aufruf ⇒ Bestand bleibt eine Woche, Woche als `ausgefallen` gebucht; zwei Ausfallwochen in Folge ⇒ Teiltopf flach (Vorschlag)
- **Auswertedatum:** 30.04.2027 (Vorschlag); Messgrössen: Rendite, MaxDD, Umschlag, Kosten des Modells, Vergleich mit gleichgewichtetem Halten aller zehn
- **Abbruchregel:** Equity fällt 25 % unter ihren Höchststand ⇒ alles flach, Bot stoppt, Bericht (Vorschlag); Änderung an Blatt, Universum oder Prompt nach dem Start ⇒ Reihe v1 endet
- **Speicher:** `ki_forschung/ki_rotation.db` (nur anfügend; nie `paper_trading_*`); Bau in BA4
- **Prompts:** `rotations_bot.txt`
