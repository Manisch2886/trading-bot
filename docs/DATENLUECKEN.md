# Register bekannter Datenlücken

**Wozu dieses Dokument da ist.** Die neun Bots laufen ausschliesslich per Cron.
**Cron holt verpasste Läufe nicht nach** — ein Lauf, der ausfällt, findet nicht
später statt, sondern gar nicht. Ein Signal, das in einem solchen Fenster
entstanden wäre, wird **nie** erkannt, und die Forward-Test-Ergebnisse des
betroffenen Zeitraums beschreiben danach eine Strategie, die so nicht gelaufen
ist. Nicht falsch gerechnet — mit Lücken in den Eingangsdaten.

Das fällt beim Auswerten nicht auf. Es gibt keine Fehlermeldung, keine
Fehlzeile, keinen leeren Wert: der Bot hat in dieser Stunde schlicht nichts
getan, und das sieht genauso aus wie „kein Signal". Deshalb dieses Register.
Es ist **fortlaufend** — jeder künftige Ausfall bekommt einen eigenen Eintrag.

## Wann ein Eintrag entsteht

Bei **jedem Ausfall, bei dem geplante Läufe nicht stattgefunden haben und nicht
nachgeholt wurden.** Ob die Ursache ein schlafender Rechner, ein Stromausfall,
ein abgestürzter Dienst, ein Netzausfall oder ein Fehler im Cron-Eintrag war,
spielt für die Datenlage keine Rolle — sie ist in allen Fällen dieselbe.

Ein Eintrag entsteht auch dann, wenn der Ausfall **teilweise** nachgeholt
wurde. Gerade dann: dass ein Teil nachgeholt wurde, ist genau die Information,
die man beim Auswerten braucht.

## Was hier **nicht** hineingehört

- **Kurslücken in den Eingangsdaten** — also fehlende oder fehlerhafte Werte
  von Binance oder yfinance. Dafür gibt es `shared/data_quality.py` (Lehre aus
  dem APH-Vorfall, PR #33/#43) und den Bericht
  `research/datenluecke_wurzelkorrektur/BERICHT.md`. Der Unterschied ist
  wesentlich: dort lief der Bot, aber die Daten waren löchrig; hier lief der
  Bot gar nicht.
- **Bewusst abgeschaltete Läufe.** Die neun täglichen E-Mail-Cronjobs sind seit
  PR #36 auskommentiert. Das ist eine Entscheidung, kein Ausfall, und steht im
  Übergabeprotokoll (Abschnitt 5 und 8).

## Was hier bewusst **nicht** gebaut ist — und warum

Es gibt **keine Markierung der Lücken in den Ergebnis-CSVs**, **keine Änderung
an den Auswertungen** und **keinen Code, der Lücken selbsttätig erkennt**. Das
ist eine Entscheidung, keine Auslassung.

Eine maschinenlesbare Lückenmarkierung bräuchte zuerst ein Konzept dafür, *wie*
eine Lücke überhaupt dargestellt wird — und zwar konsistent über neun Bots mit
drei verschiedenen Taktungen, über Backtest, Forward-Test, Equity-Simulation
und Quartals-Review hinweg. Ist eine Stunde ohne Lauf eine Zeile mit einem
Sonderwert? Ein eigener Zeitraum-Datensatz? Etwas, das der Kennzahlen-Rechner
kennen muss? Jede dieser Antworten greift in die Auswertungslogik ein, also
genau dort, wo eine falsche Zahl anschliessend als Strategie-Ergebnis gelesen
wird. Der Aufwand stünde in keinem Verhältnis zum Nutzen, solange es einen
einzigen bekannten Vorfall gibt.

Eine Textdatei an einer Stelle, die man beim Auswerten aufschlägt, löst das
eigentliche Problem — nämlich dass die Lücke **vergessen** wird — für einen
Bruchteil des Aufwands. Wenn dieses Register eines Tages viele Einträge hat,
ist das der Moment, die Frage neu zu stellen.

## Vorlage für einen neuen Eintrag

```
### JJJJ-MM-TT — kurze Bezeichnung

| | |
|---|---|
| **Zeitraum** | von–bis, mit Zeitzone; „ca." wenn nicht genau bekannt |
| **Ursache** | was den Ausfall verursacht hat |
| **Betroffen** | welche Bots und Dienste, mit ihrer Taktung |
| **Nachgeholt** | was von Hand nachgeholt wurde — und was nicht |
| **Auswirkung** | was das für die Auswertung bedeutet |
| **Belegt durch** | Quelle im Repo bzw. Angabe des Nutzers |
```

---

# Einträge

## 2026-09-11 — Mac schlief nach macOS-Update

| | |
|---|---|
| **Zeitraum** | Freitag, 11.09.2026, **ca. 08:50 bis 12:06** Ortszeit (rund 3¼ Stunden) |
| **Ursache** | Nach einem macOS-Update war das **von Hand gestartete `caffeinate` ersatzlos verschwunden**, ohne Hinweis. Der Mac ging in den Idle-Sleep; Cron lief damit nicht. |
| **Betroffen** | `elliott_wave` (Krypto, 1h-Takt): **mehrere** stündliche Forward-Test-Läufe. Binance-Testnet-Brücke (`broker/spiegel.py`, 4h-Takt zur Minute 5): der **12:05-Lauf**, vollständig. |
| **Nachgeholt** | Der **12:05-Lauf der Brücke wurde später von Hand nachgeholt**, mit demselben Aufruf wie der Cronjob. Die **Forward-Test-Läufe nicht** — siehe unten. |
| **Auswirkung** | Signale, die in diesem Fenster entstanden wären, wurden nie erkannt. Die `elliott_wave`-Forward-Test-Daten dieses Tages sind für das Fenster **lückenhaft**. |
| **Belegt durch** | `system/README_CAFFEINATE.md` (Ursache, Zeitraum, betroffene Läufe); `docs/UEBERGABEPROTOKOLL.md` Abschnitt 4.5. Die Angabe zum nachgeholten Brücken-Lauf stammt vom Nutzer und ist im Repo nicht nachweisbar (`logs/` ist gitignored). |

### Warum die Forward-Tests nicht nachholbar sind

Ein Forward-Test-Lauf ist **an seine Kerzenzeit gebunden**. `elliott_wave`
arbeitet auf Stundenkerzen: der Lauf um 10:00 prüft die eben geschlossene
10:00-Kerze und bucht einen Einstieg zum dann aktuellen Marktpreis. Um 13:00
nachgestartet, würde derselbe Aufruf die 13:00-Kerze ansehen und zum
13:00-Preis buchen — das ist kein nachgeholter Lauf, sondern ein neuer. Die
Läufe von 09:00 bis 12:00 sind damit endgültig ausgefallen.

Der Brücken-Lauf ist ein anderer Fall: er spiegelt, was in der Bot-Datenbank
**bereits steht**. Diese Aufgaben bleiben offen, bis sie gespiegelt sind — ein
späterer Lauf erledigt sie nachträglich, genau dafür ist die Brücke gebaut.

### Zwei Folgen, die man kennen sollte

1. **Der nachgeholte Brücken-Lauf hat zu einem späteren Kurs ausgeführt** als
   dem Simulationspreis des Bots. Das ist kein Fehler und wird nicht
   verschwiegen, sondern gemessen: `broker/abgleich.py` weist je Trade die
   Spalte **`Abw %`** aus (Ausführungspreis gegen Simulationspreis). Bei den
   Trades aus diesem Fenster ist dort mit einer grösseren Abweichung als üblich
   zu rechnen — sie beschreibt den Verzug, nicht die Qualität der Brücke.
2. **Die Lücke wirkt sich nur auf `elliott_wave` aus, nicht auf den Backtest.**
   Backtests rechnen auf gespeicherten Kursdaten, die vollständig sind. Nur die
   **Forward-Test-Datenbank** (`paper_trading_elliott_wave.db`) hat für dieses
   Fenster keine Einträge — und mit ihr alles, was daraus abgeleitet wird:
   Dashboard, Telegram-Zahlen, Equity-Simulation über Live-Trades,
   Quartals-Review.

### Offene Fragen zu diesem Eintrag

Diese Punkte lassen sich aus dem Repo **nicht** klären und sind deshalb
ausdrücklich benannt statt ausgefüllt:

1. **Die genaue Zahl der ausgefallenen `elliott_wave`-Läufe ist nicht belegt.**
   „Mehrere" ist die Angabe, die in `system/README_CAFFEINATE.md` steht. Rein
   rechnerisch lägen bei stündlichem Takt vier Läufe im Fenster — aber der
   genaue Cron-Minutenwert steht nirgends im Repo, und die Fenstergrenzen sind
   selbst nur „ca." bekannt. Eine konkrete Zahl wäre hier geraten. Klären liesse
   sich das an `logs/elliott_wave/cron.log` auf dem Mac: die Lücke zwischen zwei
   Zeitstempeln zeigt die ausgefallenen Läufe direkt.
2. **Ob auch der `t3_supertrend`-Forward-Test von 12:05 ausgefallen ist, ist
   offen.** `broker/README.md` bietet zwei Cron-Varianten an: entweder Bot und
   Brücke in **einer** Zeile (`5 */4 * * * … forward_test.py … && … spiegel.py
   --echt`) oder die Brücke in einem eigenen Eintrag ein paar Minuten später.
   Ist die kombinierte Zeile eingerichtet, fiel der 12:05-Lauf des Bots
   **ebenfalls** aus — und der ist, anders als der Brücken-Lauf, nicht
   nachholbar. `system/README_CAFFEINATE.md` nennt nur die Brücke. `crontab -l |
   grep t3_supertrend` klärt es in einer Minute; das Ergebnis gehört dann hier
   nachgetragen.
3. **Ob die täglichen Krypto-Bots betroffen waren, ist offen.** Für
   `rsi2_crypto`, `turtle_soup_crypto` und `volatility_breakout_crypto` ist im
   Repo nur „täglich" dokumentiert, keine Uhrzeit. Liegt ihr Lauf zwischen 08:50
   und 12:06, sind sie ebenfalls betroffen. Die vier Aktien-Bots laufen
   werktags 22:15 und liegen damit klar ausserhalb des Fensters; der 11.09.2026
   war ein Freitag.

---

*Nächster Eintrag hier darunter, neueste zuerst oder chronologisch — solange es
ein einziger ist, ist die Frage noch offen.*
