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

## ⚠️ Offener Punkt: die Bots protokollieren ihre Läufe nicht

**Dieses Register lässt sich derzeit nicht vollständig belegen.** Die Bots
schreiben **keine Lauf-Zeitstempel**. `logs/elliott_wave/` etwa enthält
`forward_test.log` (Trade-Zeilen mit Kerzenzeiten, aber ohne Lauf-Zeitpunkt)
und `email_summary.log`; eine eigene Cron-Logdatei gibt es dort nicht.

Nach einem Ausfall ist deshalb **nicht belegbar, welche Läufe tatsächlich
stattgefunden haben** — und genau diese Information braucht man, um einen
Eintrag hier überhaupt füllen zu können. Beim ersten Eintrag (11.09.2026) ist
das sofort aufgeschlagen: die Zahl der ausgefallenen `elliott_wave`-Läufe liess
sich nicht auf eine Zahl festlegen, und ob ein zweiter Bot betroffen war,
bleibt offen.

Bei einem System, das vollständig von Cron abhängt und bei dem verpasste Läufe
echte Datenlücken erzeugen, ist das eine Lücke in der Protokollierung selbst.

> **Ein einheitliches Lauf-Protokoll — eine Zeile je Start und Ende, mit
> Zeitstempel — wäre die Voraussetzung dafür, künftige Einträge in diesem
> Register belegen zu können. Nicht umgesetzt, als Aufgabe vorgemerkt.**

Solange es fehlt, sind Angaben in diesem Register teilweise Rekonstruktion aus
Dateizeitstempeln und Cron-Einträgen. Wo das der Fall ist, steht es beim
jeweiligen Eintrag dabei. Der Punkt steht auch in `docs/UEBERGABEPROTOKOLL.md`,
Abschnitt 9.

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
| **Nicht betroffen** | was nachweislich ausserhalb lag — eine geprüfte Entwarnung ist so viel wert wie ein Befund |
| **Ungeklärt** | was weder belegt noch ausgeschlossen ist; lieber hier als stillschweigend unter „nicht betroffen" |
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
| **Betroffen** | `elliott_wave` (Krypto, 1h-Takt): **drei bis vier** stündliche Forward-Test-Läufe — die genaue Zahl ist nicht belegbar, siehe unten. Binance-Testnet-Brücke (`broker/spiegel.py`, 4h-Takt zur Minute 5): der **12:05-Lauf**, vollständig. |
| **Nicht betroffen** | Die drei täglichen Krypto-Bots (alle drei Cron-Einträge liegen nachts) und die vier Aktien-Bots (werktags 22:15). Belegt am 11.09.2026 mit `crontab -l`. |
| **Ungeklärt** | Ob der `t3_supertrend`-Forward-Test von **12:00** ebenfalls ausgefallen ist — sein Cron-Eintrag `0 */4 * * *` legt einen Lauf genau ins Fenster. Siehe unten. |
| **Nachgeholt** | Der **12:05-Lauf der Brücke wurde später von Hand nachgeholt**, mit demselben Aufruf wie der Cronjob. Die **Forward-Test-Läufe nicht** — siehe unten. |
| **Auswirkung** | Signale, die in diesem Fenster entstanden wären, wurden nie erkannt. Die `elliott_wave`-Forward-Test-Daten dieses Tages sind für das Fenster **lückenhaft**. |
| **Belegt durch** | `system/README_CAFFEINATE.md` (Ursache, Zeitraum, betroffene Läufe); `docs/UEBERGABEPROTOKOLL.md` Abschnitt 4.5. Die Cron-Zeiten wurden am 11.09.2026 auf dem Mac des Nutzers mit `crontab -l` geprüft. Die Angabe zum nachgeholten Brücken-Lauf stammt vom Nutzer und ist im Repo nicht nachweisbar (`logs/` ist gitignored). |

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

### Was nachträglich geprüft wurde

Als dieser Eintrag entstand, waren drei Fragen offen, weil sie sich aus dem Repo
nicht beantworten liessen. Sie wurden **am 11.09.2026 auf dem Mac des Nutzers
mit `crontab -l` geprüft**. Zwei sind eindeutig geklärt, die dritte so weit, wie
sie sich klären lässt.

**1. Bot und Brücke sind NICHT gekoppelt** ✅ geklärt — **aber die Frage nach
dem `t3_supertrend`-Lauf ist damit nicht erledigt** ⚠️

Geklärt ist: Bot und Brücke stehen in **getrennten** Cron-Einträgen, nicht in
der kombinierten Zeile, die `broker/README.md` als Variante anbietet:

```
crontab -l | grep -c "forward_test.py.*spiegel.py"
→ 0
```

Die Zeitangaben sind `0 */4 * * *` für den Bot und `5 */4 * * *` für die
Brücke. Ein Ausfall des Bot-Laufs **als Nebenwirkung der Brücken-Zeile** ist
damit ausgeschlossen — das war die ursprüngliche Sorge, und sie ist ausgeräumt.

**Was daraus aber nicht folgt:** dass der Bot-Lauf stattgefunden hat. `0 */4 *
* *` bedeutet Läufe um 00:00, 04:00, 08:00, **12:00**, 16:00, 20:00. Das
Schlaffenster reichte von ca. 08:50 bis 12:06 — der **12:00-Lauf liegt also
darin**, unabhängig davon, in welcher Cron-Zeile er steht. Ein eigener
Cron-Eintrag schützt nicht vor einem schlafenden Rechner.

Belastbar ist damit:

| | |
|---|---|
| ausgeschlossen | ein Ausfall **durch die gekoppelte Cron-Zeile** — die gibt es nicht |
| offen | ob der `t3_supertrend`-Lauf um 12:00 **trotzdem** ausgefallen ist |

Die Auflösung hängt an derselben Frage wie Punkt 3: ob beim Aufwachen um 12:06
verpasste Läufe verspätet nachgeholt wurden. Der Zeitstempel 12:06 in
`logs/elliott_wave/forward_test.log` spricht dafür — dann hätte es auch den
`t3_supertrend`-Lauf getroffen und beide wären nachgeholt. Spricht er nicht
dafür, fehlen **beide**. Ohne Lauf-Protokoll lässt sich das nicht entscheiden;
siehe den offenen Punkt oben.

`system/README_CAFFEINATE.md` nennt nur den Brücken-Lauf. Ob der Bot-Lauf
damals geprüft und für in Ordnung befunden wurde oder schlicht nicht angesehen
wurde, geht daraus nicht hervor. **Ein Blick in `logs/t3_supertrend/` würde es
klären, falls dort Zeitstempel liegen** — beim Krypto-Bot war das nicht der
Fall, bei diesem ist es ungeprüft.

**2. Die täglichen Krypto-Bots lagen NICHT im Fenster.** ✅ geklärt

Alle drei Einträge liegen nachts, weit ausserhalb von 08:50–12:06: `20 23 * * *`,
`50 23 * * *` und `15 0 * * *`. Welcher Eintrag zu welchem der drei Bots
(`rsi2_crypto`, `turtle_soup_crypto`, `volatility_breakout_crypto`) gehört,
wurde nicht erhoben — für die Frage hier genügt, dass **alle drei** nachts
laufen.

**3. Die genaue Zahl der ausgefallenen `elliott_wave`-Läufe bleibt offen.**
⚠️ nicht belegbar

Der Cron-Eintrag ist `0 * * * *`, also stündlich zur vollen Stunde. Rechnerisch
lagen damit die Läufe um **9:00, 10:00, 11:00 und 12:00** im Fenster — vier
Stück. Allerdings trägt `logs/elliott_wave/forward_test.log` einen Zeitstempel
von **12:06**, was dafür spricht, dass der 12:00-Lauf beim Aufwachen des Mac
verspätet stattgefunden hat. Dann wären es drei.

Ein **Hinweis**, kein Beleg: der Zeitstempel sagt, wann zuletzt geschrieben
wurde, nicht, welcher Lauf das war. Auflösen lässt sich das nicht, und zwar aus
einem Grund, der über diesen Eintrag hinausreicht:

> **Der Bot protokolliert keine Lauf-Zeitstempel.** `logs/elliott_wave/`
> enthält `forward_test.log` (Trade-Zeilen mit Kerzenzeiten, kein
> Lauf-Zeitpunkt) und `email_summary.log`. Eine eigene Cron-Logdatei gibt es
> für diesen Bot nicht.

**Verbindliche Angabe für diesen Eintrag ist deshalb „drei bis vier Läufe".**
Eine der beiden Zahlen zu wählen hiesse, sich für eine zu entscheiden, ohne
etwas zu wissen. Siehe dazu den offenen Punkt oben.

---

*Nächster Eintrag hier darunter, neueste zuerst oder chronologisch — solange es
ein einziger ist, ist die Frage noch offen.*
