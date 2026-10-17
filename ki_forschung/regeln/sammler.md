# Regelblatt Sammler (Marktzustand) — Katalog v1

Fest vor dem ersten Lauf (R108 (b) (2)): dieses Blatt und die Prompts unter `ki_forschung/prompts/` liegen mit sha256 (`prompts/manifest.json`) im Repo, bevor der erste Lauf schreibt. Jede Änderung an Blatt, Frage oder Prompt ist Katalog v2 und beginnt eine neue Reihe. „Vorschlag“ = vom Plan nicht festgelegt, vom Bau vorgeschlagen, mit der Freigabe-Karte bestätigt oder geändert.

## Pflichtfelder

- **Version:** v1
- **Modell:** `claude-haiku-4-5-20251001` (`MODEL_HAIKU`, `shared/claude_client.py`); Websuche aus, `tools=None`
- **Topf:** `sammler`, Deckel 3 $ je UTC-Monat (`aufrufe.DECKEL_USD`), getrennt vom Topf `bots`
- **Märkte:** `krypto` (gilt für die fünf Krypto-Bots der neun), `aktien` (gilt für die vier Aktien-Bots der neun); Zuordnung wie `ASSET_CLASS` in `notifications/monitor.py`
- **Fragen:** sechs je Markt, in dieser Reihenfolge: F1 Risikoneigung, F2 Trend, F3 Vola-Regime, F4 Makro, F5 Liquidität, F6 Ereignisrisiko 7 Tage (Wortlaut je Frage in `prompts/sammler_f<n>_*.txt`)
- **Skala:** ganze Zahl −2, −1, 0, +1, +2 je Frage (−2 = deutlich ungünstig für Long-Risiko, 0 = neutral, +2 = deutlich günstig); dazu Zuversicht `niedrig`/`mittel`/`hoch` und Begründung höchstens 300 Zeichen, die nur eingefrorene Eingaben nennt
- **Antwortformat:** ein JSON-Objekt je Markt mit den Schlüsseln `f1` … `f6`, je `{"wert": int, "zuversicht": str, "begruendung": str}`; jede andere Antwort ist ungültig und wird als `ungueltig` gebucht (kein Wert, keine Wiederholung)
- **Quellen:** Krypto: Binance-Spot Tageskerzen BTCUSDT und ETHUSDT (letzte 200 geschlossene UTC-Tage), alternative.me Fear & Greed (letzte 30 Werte); Aktien: yfinance `^GSPC`, `^STOXX50E`, `^VIX` (letzte 200 geschlossene Handelstage); beide Märkte: ALFRED `DFF`, `T10Y2Y`, `BAMLH0A0HYM2`, `WALCL`, `DTWEXBGS` (Vorschlag: Serienauswahl) und FRED-Release-Termine der nächsten 7 Tage (Vorschlag: Quelle für F6; Release-Auswahl legt BA2 fest, bevor der erste Lauf schreibt)
- **Vintage:** jede Eingabe stammt aus `ki_forschung/abrufe.py` (`abrufe.db`, Rohkopie + sha256 + `abgerufen_utc`); der Prompt liest nur `stand(quelle, schluessel, bis=Laufzeit)`; ALFRED mit `realtime_start = realtime_end = Abruftag`; bei yfinance, Binance und Fear & Greed ist der Abruftag die Vintage (spätere Revision der Quelle ändert die Reihe nicht)
- **Lauf:** einmal je Tag, Cron am Mac, 06:15 UTC (Vorschlag), zwei Aufrufe (ein Aufruf je Markt, alle sechs Fragen in einem Aufruf), `max_tokens` 900 (Vorschlag); Kosten erschlossen 2 × 30 × rund 0,0125 $ (rund 8 000 Token Eingabe, 900 Ausgabe) = rund 0,75 $ je Monat (nicht gemessen, BA7 misst)
- **Ausfall:** fehlt eine Eingabe, greift die Bremse, ist der Notschalter `ki_sammler` gesetzt oder schläft der Mac, wird der Tag je Markt als `ausgefallen` gebucht; nichts wird nachgeholt oder geschätzt
- **Speicher:** `marktzustand/marktzustand.db` (oberste Ebene, nur anfügend; jede Zeile mit Zeitstempel, Quellen-Hash, Prompt-Hash, Katalogversion, Modell angefordert/geliefert, Tokens); Bau in BA2
- **Leseregel:** R108 (b): der Sammler liest keine Ausgabe eines Bots (`results/`, Bot-DBs, Listen, `ergebnisse/`) und schreibt nichts unter `data/`; ein Zustand ist aufgezeichnete Modellantwort, nie herleitbare Grösse; Zustände werden gegen Bot-Ergebnisse nur aus der Bestätigungsperiode gelesen, nie gegen Selektionsfalten; Auswertung ist Bericht, kein Tor. Ausnahme vom Betreiber (17.10.2026): der Filtervergleich nach `filter.md` mit vorher fester Regel
- **Prompts:** `sammler_system.txt`, `sammler_f1_risikoneigung.txt`, `sammler_f2_trend.txt`, `sammler_f3_vola_regime.txt`, `sammler_f4_makro.txt`, `sammler_f5_liquiditaet.txt`, `sammler_f6_ereignisrisiko.txt`

## Zusammenbau eines Aufrufs

System-Prompt = `sammler_system.txt`. Nachricht = Kopfzeile `Markt: <krypto|aktien>; Stand: <Laufzeit UTC>`, dann die sechs Fragetexte in der Reihenfolge F1 … F6, dann die eingefrorenen Eingaben des Markts als Tabellen (Quelle, Schlüssel, `abgerufen_utc`, sha256, Werte). Der Prompt-Hash (`aufrufe.prompt_hash`) wird je Aufruf gebucht.
