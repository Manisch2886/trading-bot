# Regelblatt Filter (Sperre bei Risikoneigung −2) — v1

Fest vor dem ersten Zustand (Betreiber 17.10.2026: „Regel vorher fest“; R108 (b) für diesen Vergleich vom Betreiber gebrochen). Der Filter greift **nicht** in die neun ein: er wird neben ihnen nachgerechnet und nur im Dashboard-Bereich „KI-Forschung“ gezeigt.

## Pflichtfelder

- **Version:** v1
- **Frage:** F1 Risikoneigung des Sammlers (Katalog v1, `sammler.md`), je Markt
- **Schwelle:** Sperre neuer Einstiege eines Bots, wenn der letzte gültige Zustand seines Markts vor der Einstiegszeit den Wert −2 hat; −1 bis +2 sperren nicht; bestehende Positionen und Ausstiege bleiben unberührt
- **Märkte:** `krypto` für elliott_wave, t3_supertrend, rsi2_crypto, turtle_soup_crypto, volatility_breakout_crypto; `aktien` für elliott_wave_stocks, rsi2_mean_reversion, turtle_soup_stocks, volatility_breakout (`ASSET_CLASS`, `notifications/monitor.py`)
- **Startzeitpunkt:** die erste Sammlerzeile nach dem Commit dieses Blatts (`abgerufen_utc` des ersten gültigen Zustands); Einstiege davor werden nicht verglichen
- **Ausfall:** ist der letzte Sammlerlauf vor der Einstiegszeit `ausgefallen` oder `ungueltig`, oder älter als 36 Stunden (Vorschlag), gilt keine Sperre
- **Messgrössen:** je Bot der neun und gesamt: Zahl der Einstiege; Zahl der gesperrten Einstiege; Netto-PnL der gesperrten Einstiege (nach Gebühr und Slippage, wie der Bot sie bucht); Equity am Auswertedatum ohne und mit Filter; MaxDD ohne und mit Filter. „Mit Filter“ = Equity-Kurve des Bots ohne die gesperrten Trades (deren PnL herausgenommen; frei gewordenes Kapital wird nicht neu angelegt — Vorschlag)
- **Quelle der Bot-Zahlen:** nur lesend über `broker/bot_db.py` (`mode=ro`); Ergebnis in `ki_forschung/ki_filtervergleich.db` (Bau in BA5)
- **Auswertedatum:** 30.04.2027 (Vorschlag); Zwischenstände nur als Anzeige, ohne Urteil
- **Status:** Bericht im Bereich „KI-Forschung“, nie Zulassungsgrund, nie Tor, nie im Selektionslauf; die Zahlen werden in keiner Neuselektion zitiert (24.3); eine Regel, die daraus entsteht, ist höchstens ein Overlay-Kandidat nach 16.8 (e) mit eigener Vorregistrierung
- **Prompts:** keine (der Filter ruft kein Modell; er liest nur die Sammlerzeilen)
