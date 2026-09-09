# Testanleitung: Position im Dashboard schliessen

Diese Anleitung ist fuer den manuellen Test **vor** dem Merge gedacht.

Das Dashboard war bis hierher **rein lesend** - so stand es in PR #35, #44,
#46, #53 und #60, und es wurde dort auch jedes Mal geprueft. Mit dieser
Aenderung gibt es **genau einen** schreibenden Weg: eine offene Position von
Hand schliessen, nur fuer **`t3_supertrend`**, nur nach zwei Bestaetigungen.

Die Reihenfolge unten ist so gebaut, dass die Schritte 0-3 **gar nichts**
veraendern koennen, Schritt 4 nur eine **Kopie** anfasst, und erst Schritt 5
die echte Datenbank beruehrt.

---

## Schritt 0 - Automatische Tests (ohne jedes Risiko)

```bash
cd ~/trading-bot
python3 dashboard/test_dashboard.py
python3 notifications/test_manual_close.py
```

Erwartet:
* `217/217 Pruefungen bestanden.`
* `85 Pruefungen bestanden, 0 fehlgeschlagen.` (mit dem Hinweis, dass vier
  Telegram-Abschnitte uebersprungen wurden - die Telegram-Oberflaeche ist
  Teil einer anderen, nicht gemergten Aenderung.)

Beide Suiten legen sich eigene Wegwerf-Datenbanken unter `/tmp` an und
fassen **keine** echte Bot-Datenbank an.

---

## Schritt 1 - Zustand der echten Datenbank festhalten (nur lesend)

Vorher wissen, was drinsteht - sonst laesst sich hinterher nicht pruefen,
ob sich genau das Erwartete geaendert hat.

```bash
cd ~/trading-bot
sqlite3 paper_trading_t3_supertrend.db \
  "SELECT id, symbol, entry_time, entry_price, status, result FROM trades WHERE status='open';"
```

Diese Ausgabe irgendwo hinkopieren, und zusaetzlich eine vollstaendige
Sicherung als Netz fuer den Notfall:

```bash
sqlite3 paper_trading_t3_supertrend.db .dump > ~/t3_sicherung_$(date +%Y%m%d_%H%M).sql
```

---

## Schritt 2 - Nur die Anzeige ansehen (schreibt nichts)

Dashboard starten (siehe `dashboard/README.md`) und die Detailseite von
**T3/ADX/SuperTrend (Krypto)** oeffnen.

Erwartet:
* Die Tabelle "Offene Positionen" hat eine **sechste Spalte "Aktion"** mit
  je einem Knopf **Schliessen**.
* Darunter steht eine Fussnote, die sagt, was der Knopf tut.
* Ist gerade kein Live-Kurs verfuegbar ("Preis nicht verfuegbar"), erscheint
  der Knopf trotzdem - der Server holt den Kurs erst beim Klick und lehnt
  ab, wenn keiner zu bekommen ist.

Bei **jedem anderen Bot** (z.B. Elliott Wave) darf es die Spalte, den Knopf
und die Fussnote **nicht** geben. Bitte an mindestens zwei anderen Bots
nachsehen.

**Kontrolle:** Schritt 1 noch einmal ausfuehren - die Ausgabe muss identisch
sein.

---

## Schritt 3 - Beide Abbruchwege (schreibt nichts)

Alle Faelle koennen gefahrlos an der **echten** Datenbank durchgespielt
werden; keiner davon fuehrt zu einem Schreibzugriff.

| # | Vorgehen | Erwartung |
|---|---|---|
| 1 | **Schliessen** -> im Dialog **Abbrechen** | Dialog schliesst, nichts passiert |
| 2 | **Schliessen** -> **Ja, schliessen** -> **Abbrechen** | dito |
| 3 | **Schliessen** -> **Ja, schliessen** -> Esc-Taste | dito (Esc verwirft den Vorgang ebenfalls) |
| 4 | Im Textfeld `bestaetigen` (klein) tippen | Knopf **Endgueltig schliessen** bleibt gesperrt |
| 5 | `BESTAETIGE` (unvollstaendig) tippen | Knopf bleibt gesperrt |
| 6 | **Ja, schliessen** -> gut zwei Minuten warten | Countdown laeuft ab, Feld und Knopf werden gesperrt, Hinweis "Bestaetigung ist abgelaufen" |

Der Dialog zeigt in Stufe 1 Symbol, Einstiegskurs, **aktuellen Kurs**,
geschaetzten PnL und die Warnung. Bitte pruefen, dass der angezeigte Kurs
plausibel ist (Vergleich mit der Spalte "Aktuell" in der Tabelle).

**Kontrolle:** Schritt 1 wiederholen. Ausgabe weiterhin identisch.

---

## Schritt 3b - Die API direkt, ohne Dialog (schreibt nichts)

Der Bestaetigungsdialog ist Bequemlichkeit, keine Sicherung. Dass die
Sicherung **serverseitig** liegt, laesst sich in drei Aufrufen nachpruefen -
`<TOKEN>` ist das `DASHBOARD_ACCESS_TOKEN` aus der `.env`:

```bash
# a) Ohne Token: 401, egal was im Koerper steht.
curl -s -o /dev/null -w "%{http_code}\n" -X POST \
  -H 'Content-Type: application/json' \
  -d '{"vorgang":"x","bestaetigung":"BESTAETIGEN"}' \
  http://127.0.0.1:8787/api/bots/t3_supertrend/schliessen/ausfuehren

# b) Mit Token, aber ohne vorherigen Vorbereiten-Schritt: 409.
#    Ein EINZELNER Aufruf kann nichts schliessen - das ist der Kern.
curl -s -X POST -H "X-Dashboard-Token: <TOKEN>" \
  -H 'Content-Type: application/json' \
  -d '{"vorgang":"frei-erfunden","bestaetigung":"BESTAETIGEN"}' \
  http://127.0.0.1:8787/api/bots/t3_supertrend/schliessen/ausfuehren

# c) Ein nicht freigeschalteter Bot: 403.
curl -s -X POST -H "X-Dashboard-Token: <TOKEN>" \
  -H 'Content-Type: application/json' -d '{"trade_id":1}' \
  http://127.0.0.1:8787/api/bots/elliott_wave/schliessen/vorbereiten
```

Erwartet: `401`, dann eine 409-Meldung "Keine gueltige Bestaetigung offen",
dann eine 403-Meldung "nicht freigeschaltet". Danach Schritt 1 wiederholen -
weiterhin unveraendert.

Im Protokoll steht jetzt bereits etwas:

```bash
tail -3 ~/trading-bot/logs/notifications/manuelle_eingriffe.log
```

Erwartet: `ABGELEHNT quelle=dashboard ... | Datenbank unveraendert`.

---

## Schritt 4 - Der eigentliche Schliessvorgang, aber nur an einer KOPIE

Erst hier wird tatsaechlich geschrieben - in einer vollstaendig getrennten
Kopie des Projekts. Es wird **kein** Konfigurationsschalter gebraucht: die
Module leiten den Datenbankpfad aus ihrem eigenen Verzeichnis ab, eine Kopie
des Baums schreibt also automatisch in die Datenbank der Kopie.

```bash
# 1. Laufendes Dashboard beenden (Strg-C im Terminal, in dem server.py laeuft).

# 2. Kopie anlegen - inkl. .env und der Datenbanken (beides ist gitignored,
#    aber lokal vorhanden).
rm -rf ~/trading-bot-probe
cp -R ~/trading-bot ~/trading-bot-probe

# 3. Sicherstellen, dass die Kopie wirklich eine EIGENE Datenbank hat.
ls -l ~/trading-bot/paper_trading_t3_supertrend.db \
      ~/trading-bot-probe/paper_trading_t3_supertrend.db

# 4. Das Dashboard AUS DER KOPIE starten, auf einem anderen Port, damit es
#    sich nicht mit dem echten beisst.
cd ~/trading-bot-probe
DASHBOARD_PORT=8788 python3 dashboard/server.py
```

Im Browser `http://127.0.0.1:8788` oeffnen (dasselbe Token) und den
vollstaendigen Weg gehen:

**Schliessen -> Ja, schliessen -> `BESTAETIGEN` tippen -> Endgueltig schliessen**

Erwartet:
* gruene Erfolgsmeldung mit Symbol, Kurs, PnL und dem Vermerk `manual_close`,
* die Position verschwindet **sofort** aus "Offene Positionen" (ohne dass
  die Seite neu geladen wird),
* die Kachel "Offene Positionen" zaehlt eins herunter,
* der Trade taucht unter "Zuletzt geschlossene Trades" mit Ergebnis
  `manual_close` auf.

**Danach beide Datenbanken vergleichen** - die Kopie muss sich geaendert
haben, das Original **nicht**:

```bash
sqlite3 ~/trading-bot-probe/paper_trading_t3_supertrend.db \
  "SELECT id, symbol, exit_time, exit_price, result, pnl_pct, status
     FROM trades WHERE result='manual_close';"

sqlite3 ~/trading-bot/paper_trading_t3_supertrend.db \
  "SELECT COUNT(*) AS darf_null_sein FROM trades WHERE result='manual_close';"

cat ~/trading-bot-probe/logs/notifications/manuelle_eingriffe.log
```

Erwartet in der Protokollzeile: `ERFOLGREICH quelle=dashboard bot=t3_supertrend
trade_id=… symbol=… benutzer=dashboard@127.0.0.1 … | VORHER status=open … |
NACHHER status=closed result=manual_close …`.

**Zum Schluss aufraeumen:**

```bash
# Dashboard der Kopie mit Strg-C beenden, dann:
rm -rf ~/trading-bot-probe
```

---

## Schritt 5 - Der Ernstfall an der echten Datenbank

Erst ausfuehren, wenn Schritt 0-4 durchgelaufen sind.

**Guenstiger Zeitpunkt:** `t3_supertrend` laeuft alle 4 Stunden per Cronjob.
Am wenigsten Ueberschneidungsgefahr besteht **kurz nach** einem Lauf:

```bash
crontab -l | grep t3_supertrend
ls -lt ~/trading-bot/logs/t3_supertrend/ | head -3
```

Falls der Cronjob doch genau dazwischenfunkt, ist das abgesichert: der
Endpunkt meldet dann entweder "Die Datenbank ist gerade gesperrt" oder "Der
Trade ist nicht mehr offen" und schreibt **nichts** (getestet, siehe
Abschnitt 8 der Dashboard-Testsuite).

Danach den Ablauf wie in Schritt 4 durchspielen und mit Schritt 1
vergleichen: **genau eine Zeile** darf sich geaendert haben, und zwar nur in
`exit_time`, `exit_price`, `result`, `pnl_pct`, `status`.

```bash
sqlite3 ~/trading-bot/paper_trading_t3_supertrend.db \
  "SELECT id, symbol, entry_price, exit_time, exit_price, result, pnl_pct, status
     FROM trades WHERE result='manual_close';"
```

---

## Falls doch die falsche Position geschlossen wurde

Es gibt bewusst **keinen** Knopf zum Rueckgaengigmachen (siehe Risiko 1
unten). Von Hand geht es, mit der `id` aus der Ausgabe oben:

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

---

## Die groessten verbleibenden Risiken

Ehrlich benannt, weil sie bekannt sein sollten, bevor die Funktion live geht.
Die Punkte 1 bis 4 gelten unabhaengig von der Oberflaeche, 5 bis 8 sind neu
oder anders als bei der Telegram-Variante.

1. **Der Eingriff ist im Dashboard nicht rueckgaengig zu machen.** Absicht:
   ein "Wieder oeffnen" waere ein Codepfad, der Positionen *oeffnet* - genau
   das schliesst die Aufgabe aus, und es waere die gefaehrlichere Faehigkeit
   von beiden. Der Weg zurueck fuehrt ueber SQL von Hand (siehe oben).

2. **Geschlossen wird zu dem Kurs, den der Server beim Oeffnen des Dialogs
   geholt hat**, nicht zu einem beim Ausfuehren neu geholten. Zwischen
   Anzeige und `BESTAETIGEN` koennen bis zu zwei Minuten liegen; in einem
   schnellen Kryptomarkt kann der echte Kurs dann spuerbar abweichen. Die
   Alternative - still zu einem anderen Kurs als dem bestaetigten schliessen -
   waere die groessere Ueberraschung. Die zwei Minuten begrenzen den Effekt,
   beseitigen ihn nicht.

3. **Der Ausstiegskurs ist ein Momentanpreis, kein Kerzenschluss.** Der Bot
   selbst bucht Ausstiege immer auf `close` einer 4h-Kerze (oder auf den
   Stop-Preis). Eine manuell geschlossene Position bricht mit dieser
   Konvention; erkennbar ist sie an `result='manual_close'`.

4. **Die Statistik des Bots verschiebt sich.** Trefferquote, Ø pro Trade und
   Summe PnL - im Dashboard, in `/pnl` und in den Tagesmails - rechnen ueber
   **alle** geschlossenen Trades, unabhaengig vom Grund. Ein manueller
   Ausstieg geht also in die gemessene Strategie-Performance ein, obwohl er
   nicht von der Strategie stammt.

5. **Der Zugriffsschutz ist genau ein Token, und es liegt im Browser.** Das
   `DASHBOARD_ACCESS_TOKEN` steht nach dem ersten Login 90 Tage lang als
   Cookie im Browser. Wer Zugriff auf das entsperrte Geraet hat, kann
   Positionen schliessen - die beiden Bestaetigungen schuetzen vor Versehen,
   nicht vor einer fremden Person. Das war vorher schon so, wog aber
   weniger: bis jetzt konnte man mit dem Token nur *lesen*.

6. **Der Server bindet weiterhin nur an localhost.** Wird das ueber
   `DASHBOARD_HOST` geaendert (oder spaeter Tailscale eingerichtet), ist der
   schreibende Endpunkt aus dem Netz erreichbar - abgesichert nur durch das
   Token. Vor einer solchen Umstellung lohnt ein zweiter Blick auf Punkt 5.

7. **Der Vorgangsspeicher liegt im Arbeitsspeicher des Servers.** Ein
   Neustart des Dashboards verwirft alle angefangenen Bestaetigungen. Das
   ist beabsichtigt - ein halb bestaetigter Schreibzugriff soll einen
   Neustart nicht ueberdauern -, kann aber im Betrieb so aussehen, als
   "vergesse" der Dialog etwas.

8. **Nur `t3_supertrend` ist freigeschaltet.** Fuer die uebrigen acht Bots
   ist die Funktion gesperrt (403). Die Freischaltung weiterer Bots ist ein
   Eintrag in `SCHLIESSBARE_BOTS` in `notifications/manual_close.py` - dabei
   muss aber jeweils geprueft werden, ob deren Schema zusaetzliche Spalten
   hat (Elliott- und rsi2-Bots haben welche) und ob die Kursquelle rund um
   die Uhr taugt (bei den Aktien-Bots nicht).
