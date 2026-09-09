# Testanleitung: `/schliessen` (Telegram Phase 3)

Diese Anleitung ist fuer den manuellen Test **vor** dem Merge gedacht.
`/schliessen` ist die erste Funktion des Projekts, die in eine
**Live-Datenbank eines Bots schreibt**. Sie ist nur fuer einen einzigen Bot
freigeschaltet: **`t3_supertrend`** (T3/ADX/SuperTrend, Krypto, 4h).

Die Reihenfolge unten ist bewusst so gewaehlt, dass die ersten drei Schritte
**gar nichts** veraendern koennen, der vierte nur eine **Kopie** anfasst, und
erst der fuenfte die echte Datenbank beruehrt.

---

## Schritt 0 - Automatische Tests (30 Sekunden, ohne Risiko)

```bash
cd ~/trading-bot
python3 notifications/test_manual_close.py
```

Erwartet: `129 Pruefungen bestanden, 0 fehlgeschlagen.`
Die Tests legen sich ihre eigenen Wegwerf-Datenbanken unter `/tmp` an und
fassen **keine** echte Bot-Datenbank an.

---

## Schritt 1 - Zustand der echten Datenbank festhalten (nur lesend)

Vorher wissen, was drinsteht - sonst laesst sich hinterher nicht pruefen, ob
sich genau das Erwartete geaendert hat.

```bash
cd ~/trading-bot
sqlite3 paper_trading_t3_supertrend.db \
  "SELECT id, symbol, entry_time, entry_price, status, result FROM trades WHERE status='open';"
```

Diese Ausgabe irgendwo hinkopieren. Zusaetzlich eine vollstaendige Sicherung
der Tabelle, als Netz fuer den Notfall:

```bash
sqlite3 paper_trading_t3_supertrend.db .dump > ~/t3_sicherung_$(date +%Y%m%d_%H%M).sql
```

---

## Schritt 2 - Nur die Anzeige testen (schreibt nichts)

Der Bot muss laufen (`notifications/README.md`, Abschnitt "Einrichtung").
In Telegram:

```
/schliessen
```

Erwartet:
* eine Liste der offenen Positionen mit Symbol, Einstiegskurs, **aktuellem
  Live-Kurs** und geschaetztem PnL,
* je offener Position eine Schaltflaeche, plus "Abbrechen",
* `SOLUSDT`-artige, bereits geschlossene Trades tauchen **nicht** auf.

Weitere Anzeige-Tests, alle folgenlos:

| Eingabe | Erwartung |
|---|---|
| `/schliessen elliott_wave` | "nicht freigeschaltet", nennt `t3_supertrend` |
| `/schliessen` ohne offene Position | "Keine offenen Positionen - nichts zu schliessen" |
| `/help` | `/schliessen` ist jetzt aufgefuehrt |

**Kontrolle:** Schritt 1 noch einmal ausfuehren - die Ausgabe muss identisch
sein. Bis hierher wurde nichts geschrieben.

---

## Schritt 3 - Beide Abbruchwege testen (schreibt nichts)

Alle vier Faelle koennen gefahrlos an der **echten** Datenbank durchgespielt
werden, denn keiner davon fuehrt zu einem Schreibzugriff:

1. `/schliessen` -> **"Abbrechen"** antippen.
   Erwartet: "Abgebrochen. Es wurde nichts geaendert."
2. `/schliessen` -> Position antippen -> Zusammenfassung erscheint ->
   **"Abbrechen"** antippen.
   Erwartet: dieselbe Meldung.
3. `/schliessen` -> Position antippen -> **"Ja, schliessen"** ->
   Aufforderung erscheint -> irgendetwas anderes tippen, z.B. `ja`.
   Erwartet: "Abgebrochen - der Text stimmte nicht."
   Danach `BESTAETIGEN` tippen: **es darf nichts mehr passieren** (die
   Bestaetigung ist verbraucht, der Ablauf muss von vorn beginnen).
4. `/schliessen` -> Position -> "Ja, schliessen" -> **zwei Minuten warten** ->
   dann `BESTAETIGEN` tippen.
   Erwartet: keine Reaktion (die Bestaetigung ist abgelaufen).

Zusaetzlich: `bestaetigen` in Kleinbuchstaben muss **abgelehnt** werden - der
Vergleich ist absichtlich case-sensitiv (Begruendung in `manual_close.py`).

**Kontrolle:** Schritt 1 wiederholen. Ausgabe weiterhin identisch.

---

## Schritt 4 - Der eigentliche Schliessvorgang, aber nur an einer KOPIE

Erst hier wird tatsaechlich geschrieben - und zwar in einer vollstaendig
getrennten Kopie des Projekts. Es wird **kein** Konfigurationsschalter
gebraucht: das Modul leitet den Datenbankpfad aus seinem eigenen
Verzeichnis ab, eine Kopie des Baums schreibt also automatisch in die
Datenbank der Kopie.

```bash
# 1. Den laufenden Bot beenden. ZWINGEND: Telegram erlaubt pro Bot-Token nur
#    EINEN aktiven Long-Poller. Zwei Prozesse gleichzeitig fuehren zu
#    "Conflict: terminated by other getUpdates request" (siehe README.md).
launchctl unload ~/Library/LaunchAgents/com.manisch.telegram-tradesignal-bot.plist

# 2. Kopie anlegen (inkl. .env und der Datenbanken - beides ist gitignored,
#    aber lokal vorhanden).
rm -rf ~/trading-bot-probe
cp -R ~/trading-bot ~/trading-bot-probe

# 3. Sicherstellen, dass die Kopie wirklich eine EIGENE Datenbank hat.
ls -l ~/trading-bot/paper_trading_t3_supertrend.db \
      ~/trading-bot-probe/paper_trading_t3_supertrend.db

# 4. Den Bot AUS DER KOPIE starten (im Vordergrund, damit alles sichtbar ist).
cd ~/trading-bot-probe
python3 notifications/telegram_bot.py
```

Jetzt in Telegram den vollstaendigen Ablauf durchspielen:

```
/schliessen  ->  Position antippen  ->  "Ja, schliessen"  ->  BESTAETIGEN
```

Erwartet: "✅ Position geschlossen" mit Symbol, Ausstiegskurs, PnL und dem
Vermerk `manual_close`.

**Danach beide Datenbanken vergleichen** - die Kopie muss sich geaendert
haben, das Original **nicht**:

```bash
sqlite3 ~/trading-bot-probe/paper_trading_t3_supertrend.db \
  "SELECT id, symbol, exit_time, exit_price, result, pnl_pct, status FROM trades WHERE result='manual_close';"

sqlite3 ~/trading-bot/paper_trading_t3_supertrend.db \
  "SELECT COUNT(*) AS darf_null_sein FROM trades WHERE result='manual_close';"
```

Und das Protokoll der Kopie ansehen:

```bash
cat ~/trading-bot-probe/logs/notifications/manuelle_eingriffe.log
```

Erwartet: eine Zeile, die mit dem Zeitstempel und `MANUELLER-EINGRIFF
ERFOLGREICH` beginnt und Vorher- wie Nachher-Zustand enthaelt - plus je eine
`ABGELEHNT`-Zeile fuer die Fehlversuche aus Schritt 3, sofern die in der
Kopie wiederholt wurden.

**Zum Schluss aufraeumen:**

```bash
# Bot in der Kopie mit Strg-C beenden, dann:
rm -rf ~/trading-bot-probe
launchctl load ~/Library/LaunchAgents/com.manisch.telegram-tradesignal-bot.plist
```

---

## Schritt 5 - Der Ernstfall an der echten Datenbank

Erst ausfuehren, wenn Schritt 0-4 durchgelaufen sind.

**Guenstiger Zeitpunkt:** `t3_supertrend` laeuft alle 4 Stunden per Cronjob.
Am wenigsten Ueberschneidungsgefahr besteht **kurz nach** einem Lauf. Wann er
zuletzt lief:

```bash
crontab -l | grep t3_supertrend
ls -lt ~/trading-bot/logs/t3_supertrend/ | head -3
```

(Der genaue Dateiname haengt davon ab, wohin die Cron-Zeile umleitet - die
Log-Verzeichnisse liegen nach `logs/<strategie_name>/`, siehe
`shared/strategy_paths.py`. Ersatzweise verraet auch der juengste
`entry_time`/`exit_time`-Wert in der Datenbank, wann zuletzt geschrieben
wurde.)

Falls der Cronjob doch genau dazwischenfunkt, ist das abgesichert: die
Funktion meldet dann entweder "Die Datenbank ist gerade gesperrt" oder "Der
Trade ist nicht mehr offen" und schreibt **nichts** (getestet, siehe 9a-9d in
der Testsuite).

Danach den Ablauf wie in Schritt 4 durchspielen und mit Schritt 1 vergleichen:
**genau eine Zeile** darf sich geaendert haben, und zwar nur in
`exit_time`, `exit_price`, `result`, `pnl_pct`, `status`.

```bash
sqlite3 ~/trading-bot/paper_trading_t3_supertrend.db \
  "SELECT id, symbol, entry_price, exit_time, exit_price, result, pnl_pct, status
     FROM trades WHERE result='manual_close';"
```

---

## Falls doch die falsche Position geschlossen wurde

Es gibt bewusst **keinen** Telegram-Befehl zum Rueckgaengigmachen (siehe
Risiko 1 unten). Von Hand geht es, mit der `id` aus der Ausgabe oben:

```bash
sqlite3 ~/trading-bot/paper_trading_t3_supertrend.db \
  "UPDATE trades SET exit_time=NULL, exit_price=NULL, result=NULL,
          pnl_pct=NULL, status='open' WHERE id=<ID> AND result='manual_close';"
```

Die Bedingung `result='manual_close'` sorgt dafuer, dass sich damit **nur**
ein manueller Eingriff zuruecknehmen laesst, niemals ein Ausstieg, den der
Bot selbst gebucht hat. Der Bot nimmt die Position beim naechsten Lauf wieder
in seine Pruefung auf und schliesst sie regulaer, sobald sein eigenes
Ausstiegssignal kommt.

Alternativ die Sicherung aus Schritt 1 einspielen (verwirft allerdings auch
alles, was der Bot seither gebucht hat).

---

## Die groessten verbleibenden Risiken

Ehrlich benannt, weil sie bekannt sein sollten, bevor die Funktion live geht:

1. **Der Eingriff ist im Bot nicht rueckgaengig zu machen.** Absicht: ein
   `/wiedereroeffnen` waere ein Codepfad, der Positionen *oeffnet* - genau
   das schliesst die Aufgabe aus, und es waere die gefaehrlichere Faehigkeit
   von beiden. Der Weg zurueck fuehrt ueber SQL von Hand (siehe oben).

2. **Geschlossen wird zu dem Kurs, den der Nutzer in der Zusammenfassung
   gesehen hat, nicht zu einem beim Ausfuehren neu geholten.** Zwischen
   Anzeige und `BESTAETIGEN` koennen bis zu zwei Minuten liegen; in einem
   schnellen Kryptomarkt kann der echte Kurs dann spuerbar abweichen. Die
   Alternative - still zu einem anderen Kurs als dem bestaetigten schliessen -
   waere die groessere Ueberraschung. Die zwei Minuten begrenzen den Effekt,
   beseitigen ihn aber nicht.

3. **Der Ausstiegskurs ist ein Momentanpreis, kein Kerzenschluss.** Der Bot
   selbst bucht Ausstiege immer auf `close` einer 4h-Kerze (oder auf den
   Stop-Preis). Eine manuell geschlossene Position bricht mit dieser
   Konvention. In Auswertungen ist sie an `result='manual_close'` erkennbar -
   wer Kennzahlen des Bots mit denen der Backtests vergleicht, sollte
   manuelle Ausstiege bewusst ein- oder ausschliessen.

4. **Die Statistik des Bots verschiebt sich.** Win-Rate und Summen-PnL in
   `/pnl`, im Dashboard und in den Tagesmails rechnen ueber **alle**
   geschlossenen Trades, unabhaengig vom Grund. Ein manueller Ausstieg geht
   also in die gemessene Strategie-Performance ein, obwohl er nicht von der
   Strategie stammt. Kein Fehler, aber eine Verzerrung, die mit jedem
   Eingriff waechst.

5. **Zugriffsschutz ist genau eine Zahl.** Es gilt weiterhin nur die
   `TELEGRAM_USER_ID`-Pruefung. Wer Zugriff auf das entsperrte Telefon mit
   dem Telegram-Konto hat, kann Positionen schliessen - die beiden
   Bestaetigungen schuetzen vor Versehen, nicht vor einer fremden Person.
   Der Bot-Token in `.env` ist davon unberuehrt: mit ihm allein kann man
   Nachrichten senden, aber keinen Handler ausloesen.

6. **Der Freitext-Handler sieht jede Nachricht.** Damit die zweite Stufe
   funktioniert, ist ein Handler fuer beliebigen Text registriert. Er tut
   nur etwas, wenn gerade eine Bestaetigung aussteht (getestet), aber er
   *sieht* jede Nachricht an den Bot. Deshalb ist der Vergleich
   case-sensitiv: ein beilaeufiges "bestaetigen" soll nichts ausloesen.

7. **Ein sehr langsamer Cronjob-Lauf laesst den Befehl auflaufen.** Haelt ein
   anderer Prozess die Schreibsperre laenger als 15 Sekunden, bricht
   `/schliessen` ab - korrekt und ohne Schaden, aber der Nutzer muss es
   erneut versuchen.

8. **Nur `t3_supertrend` ist freigeschaltet.** Fuer die uebrigen acht Bots
   ist die Funktion gesperrt und meldet das. Die Freischaltung weiterer Bots
   ist ein Eintrag in `SCHLIESSBARE_BOTS` - dabei muss aber jeweils geprueft
   werden, ob deren Schema zusaetzliche Spalten hat (Elliott- und
   rsi2-Bots haben welche) und ob die Kursquelle rund um die Uhr taugt (bei
   den Aktien-Bots nicht).
