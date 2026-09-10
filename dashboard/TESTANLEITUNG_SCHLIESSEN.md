# Testanleitung: Position im Dashboard schliessen

Diese Anleitung ist fuer den manuellen Test **vor** dem Merge gedacht.

Das Dashboard war bis hierher **rein lesend** - so stand es in PR #35, #44,
#46, #53 und #60, und es wurde dort auch jedes Mal geprueft. Mit dieser
Aenderung gibt es schreibende Wege - nur fuer **`t3_supertrend`**, und nur
zum Schliessen offener Positionen:

| Weg | Bestaetigung in der Oberflaeche | Schritt in dieser Anleitung |
|---|---|---|
| **eine** Position | EIN Tap auf die Zusammenfassung | 2, 3, 4, 5 |
| **alle** Positionen (Notfall) | ZWEI Klicks, beide ohne Texteingabe | 6, 7 |

Beide sind ueber zwei getrennte Server-Aufrufe abgesichert, die ohne
einander wirkungslos sind. Der Notfallweg schliesst jede Position **einzeln**
ueber dieselbe Kernfunktion - und laeuft weiter, wenn eine davon scheitert.

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

## Schritt 3 - Der Abbruchweg (schreibt nichts)

Seit der Umstellung auf **einen Tap** gibt es nur noch EINEN Dialogschritt und
damit nur noch einen Abbruchweg - in drei Varianten, die alle dasselbe tun.
Die frueheren Faelle rund um die Texteingabe (`bestaetigen` klein tippen,
`BESTAETIGE` unvollstaendig) sind entfallen, weil es kein Textfeld mehr gibt.

Alle Faelle koennen gefahrlos an der **echten** Datenbank durchgespielt
werden; keiner davon fuehrt zu einem Schreibzugriff.

| # | Vorgehen | Erwartung |
|---|---|---|
| 1 | **Schliessen** -> im Dialog **Abbrechen** | Dialog schliesst, nichts passiert |
| 2 | **Schliessen** -> Esc-Taste | dito (Esc verwirft den Vorgang ebenfalls) |
| 3 | **Schliessen** -> Klick auf den verdunkelten Hintergrund | dito |
| 4 | **Schliessen** -> gut zwei Minuten warten, ohne zu tippen | Countdown laeuft ab, **Ja, schliessen** wird gesperrt, Hinweis "Die Bestaetigung ist abgelaufen" |

Wichtig bei Fall 4: Der Vorgang verfaellt weiterhin nach 120 Sekunden - daran
hat die Umstellung nichts geaendert. Wer den Dialog offen liegen laesst, muss
von vorn beginnen.

Der Dialog zeigt Symbol, Einstiegskurs, **aktuellen Kurs**, geschaetzten PnL,
die Warnung und den Countdown. Bitte pruefen, dass der angezeigte Kurs
plausibel ist (Vergleich mit der Spalte "Aktuell" in der Tabelle). Der Fokus
liegt beim Oeffnen auf **Abbrechen**, nicht auf dem Schliessen-Knopf - ein
versehentliches Enter darf nichts schreiben.

**Kontrolle:** Schritt 1 wiederholen. Ausgabe weiterhin identisch.

---

## Schritt 3b - Die API direkt, ohne Dialog (schreibt nichts)

Der Bestaetigungsdialog ist Bequemlichkeit, keine Sicherung. Dass die
Sicherung **serverseitig** liegt, laesst sich in drei Aufrufen nachpruefen -
`<TOKEN>` ist das `DASHBOARD_ACCESS_TOKEN` aus der `.env`:

```bash
# a) Ohne Token: 401, egal was im Koerper steht.
curl -s -o /dev/null -w "%{http_code}\n" -X POST \
  -H 'Content-Type: application/json' -d '{"vorgang":"x"}' \
  http://127.0.0.1:8787/api/bots/t3_supertrend/schliessen/ausfuehren

# b) Mit Token, aber ohne vorherigen Vorbereiten-Schritt: 409.
#    Ein EINZELNER Aufruf kann nichts schliessen - das ist der Kern, und
#    das ist seit dem Wegfall der Texteingabe DIE Absicherung. Das frueher
#    noetige "bestaetigung" ist hier absichtlich mitgeschickt: es wird nicht
#    mehr gelesen und oeffnet ohne gueltige Kennung auch nichts.
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

**Schliessen -> Ja, schliessen**

Das sind die zwei Taps: der erste oeffnet die Zusammenfassung (und legt
serverseitig den Vorgang an), der zweite schreibt. Ein Textfeld gibt es
nicht mehr.

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
   Anzeige und dem Tap koennen bis zu zwei Minuten liegen; in einem
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

---

## Schritt 6 - Notfallweg: Anzeige und Abbruch (schreibt nichts)

Gefahrlos an der **echten** Datenbank. Voraussetzung: `t3_supertrend` hat
mindestens eine offene Position - sonst erscheint der Knopf absichtlich gar
nicht (ein Knopf, der garantiert in "keine offene Position" endet, laedt bei
dieser Tragweite zum Klicken auf Vorrat ein).

Unterhalb der Positionstabelle steht jetzt eine eigene Leiste mit dem Knopf
**⚠ Notfall: alle N Positionen schliessen**.

| # | Vorgehen | Erwartung |
|---|---|---|
| 1 | Den Knopf mit dem Einzel-Knopf in der Tabelle vergleichen | Der Notfall-Knopf ist **vollflaechig rot** mit Warnzeichen, der Einzel-Knopf nur ein gedaempfter Umriss. Sie duerfen nicht verwechselbar aussehen |
| 2 | Notfall-Knopf antippen | Dialog **"Alle Positionen schliessen?"**, Kopfzeile **"Schritt 1 von 2"**, Liste ALLER offenen Positionen mit Einstieg, aktuellem Kurs und PnL, darunter **Ø je Position** mit Spannweite, Warnung und Countdown |
| 3 | Die Liste mit der Tabelle darueber vergleichen | Dieselben Symbole, dieselben Kurse. Positionen ohne Live-Kurs stehen als "wird uebersprungen: kein aktueller Kurs verfuegbar" drin und zaehlen nicht mit |
| 4 | **Abbrechen** in Stufe 1 | Dialog zu, nichts passiert |
| 5 | Knopf -> **Ja, alle schliessen** | Stufe 2: **"Wirklich ALLE N Positionen schliessen?"**, Knopf **Endgueltig bestaetigen**, Countdown laeuft weiter (er wird **nicht** neu gestartet - die Frist gilt ab dem Oeffnen) |
| 6 | **Abbrechen** in Stufe 2 | Dialog zu, nichts passiert |
| 7 | Knopf -> **Ja, alle schliessen** -> Esc-Taste | dito |
| 8 | Knopf -> gut zwei Minuten warten | Countdown laeuft ab, beide Knoepfe werden gesperrt, Hinweis "Die Bestaetigung ist abgelaufen" |

Wichtig bei 5: Der Fokus liegt in **beiden** Stufen auf **Abbrechen**, nicht
auf dem roten Knopf. Ein doppelter Klick oder ein Enter darf die zweite Stufe
nicht gleich mit erledigen - sonst waere es faktisch wieder ein Klick.

**Kontrolle:** Schritt 1 wiederholen. Ausgabe weiterhin identisch.

### Schritt 6b - Die API des Notfallwegs direkt (schreibt nichts)

```bash
# a) Ohne Token: 401.
curl -s -o /dev/null -w "%{http_code}\n" -X POST \
  -H 'Content-Type: application/json' -d '{"vorgang":"x"}' \
  http://127.0.0.1:8787/api/bots/t3_supertrend/alle-schliessen/ausfuehren

# b) Mit Token, aber ohne vorherigen Vorbereiten-Schritt: 409.
curl -s -X POST -H "X-Dashboard-Token: <TOKEN>" \
  -H 'Content-Type: application/json' -d '{"vorgang":"frei-erfunden"}' \
  http://127.0.0.1:8787/api/bots/t3_supertrend/alle-schliessen/ausfuehren

# c) Nicht freigeschalteter Bot: 403.
curl -s -X POST -H "X-Dashboard-Token: <TOKEN>" \
  -H 'Content-Type: application/json' -d '{}' \
  http://127.0.0.1:8787/api/bots/elliott_wave/alle-schliessen/vorbereiten
```

Erwartet: `401`, dann "Keine gueltige Bestaetigung offen", dann "nicht
freigeschaltet". Danach Schritt 1 wiederholen - weiterhin unveraendert.

---

## Schritt 7 - Notfallweg an einer KOPIE mit MEHREREN offenen Positionen

Das ist der eigentliche Test dieser Funktion. Kopie wie in Schritt 4 anlegen:

```bash
# 1. Laufendes Dashboard der Kopie beenden, falls noch eines laeuft.
# 2. Frische Kopie:
cp -R ~/trading-bot ~/trading-bot-probe
# 3. Pruefen, dass die Kopie eine EIGENE Datenbank hat:
ls -l ~/trading-bot-probe/paper_trading_t3_supertrend.db
# 4. Vorher-Zustand der Kopie festhalten:
sqlite3 ~/trading-bot-probe/paper_trading_t3_supertrend.db \
  "SELECT id, symbol, entry_price, status FROM trades WHERE status='open';"
```

Falls die Kopie nur eine oder keine offene Position hat, lassen sich fuer den
Test welche ergaenzen - **ausschliesslich in der KOPIE**:

```bash
sqlite3 ~/trading-bot-probe/paper_trading_t3_supertrend.db \
  "INSERT INTO trades (symbol, signal_time, entry_time, entry_price,
                       stop_price, status)
   VALUES ('BTCUSDT','2026-03-01 00:00:00','2026-03-01 00:00:00',
           100000.0, 95000.0,'open'),
          ('ETHUSDT','2026-03-01 00:00:00','2026-03-01 00:00:00',
           4000.0, 3800.0,'open');"
```

Dashboard aus der Kopie auf eigenem Port starten und den Weg gehen:

**⚠ Notfall -> Ja, alle schliessen -> Endgueltig bestaetigen**

Erwartet:
* eine **gruene** Meldung "N von N Positionen geschlossen" samt Liste jeder
  geschlossenen Position mit ihrem **eigenen** Ausstiegskurs,
* alle Positionen verschwinden **sofort** aus "Offene Positionen",
* der Notfall-Knopf verschwindet (keine offene Position mehr),
* alle Trades stehen unter "Zuletzt geschlossene Trades" mit `manual_close`.

### Schritt 7b - Der wichtigste Fall: TEILAUSFALL

Hier wird geprueft, dass ein Fehlschlag bei EINER Position die uebrigen nicht
mitnimmt. Dazu wird einer Position **nach** dem Oeffnen der Uebersicht der
Einstiegskurs entzogen - dann lehnt der Kern genau sie ab, weil der PnL nicht
berechenbar ist.

```bash
# 1. In der Kopie wieder drei offene Positionen herstellen (siehe oben).
# 2. Im Browser den Notfall-Dialog OEFFNEN und offen lassen (Stufe 1).
# 3. In einem zweiten Terminal EINER Position den Einstiegskurs entziehen -
#    <ID> ist eine der in der Uebersicht gezeigten Positionen:
sqlite3 ~/trading-bot-probe/paper_trading_t3_supertrend.db \
  "UPDATE trades SET entry_price=NULL WHERE id=<ID>;"
# 4. Im Browser weiterklicken: Ja, alle schliessen -> Endgueltig bestaetigen
```

Erwartet - und das ist der Kern:
* Die Meldung ist **orange, nicht gruen**, und lautet
  **"N-1 von N Positionen geschlossen; 1 fehlgeschlagen: SYMBOL (Einstiegskurs
  fehlt oder ist 0 - PnL nicht berechenbar.)"**.
* Die **uebrigen** Positionen sind wirklich geschlossen - auch die, die in der
  Reihenfolge **nach** der fehlgeschlagenen kam.
* Die fehlgeschlagene Position ist **weiterhin offen** und vollstaendig
  unberuehrt (`exit_price` leer).
* Im Protokoll steht fuer **jede** Position eine eigene Zeile - Erfolge als
  `ERFOLGREICH`, die eine als `ABGELEHNT`. Keine Sammelzeile.

```bash
sqlite3 ~/trading-bot-probe/paper_trading_t3_supertrend.db \
  "SELECT id, symbol, exit_price, result, status FROM trades ORDER BY id DESC LIMIT 5;"
cat ~/trading-bot-probe/logs/notifications/manuelle_eingriffe.log
```

Danach den Einstiegskurs in der Kopie zuruecksetzen, falls weitergetestet wird.

### Schritt 7c - Der Cronjob kommt dazwischen

```bash
# 1. Drei offene Positionen, Notfall-Dialog oeffnen und offen lassen.
# 2. Eine davon "wie der Bot" schliessen:
sqlite3 ~/trading-bot-probe/paper_trading_t3_supertrend.db \
  "UPDATE trades SET exit_time='2026-03-01 12:00:00', exit_price=99000.0,
     result='stop_loss', pnl_pct=-1.3, status='closed' WHERE id=<ID>;"
# 3. Im Browser weiterklicken.
```

Erwartet: Die Meldung nennt sie als **uebersprungen**, nicht als Fehlschlag -
"1 uebersprungen, weil der Bot sie selbst geschlossen hatte". Ihr
`result` bleibt **`stop_loss`**, wird also **nicht** mit `manual_close`
ueberschrieben. Die uebrigen werden geschlossen.

**Zum Schluss aufraeumen:** `rm -rf ~/trading-bot-probe`.

---

## Schritt 8 - Notfallweg im Ernstfall (echte Datenbank)

Nur wenn Schritt 6 und 7 durchgelaufen sind, und mit demselben Vorbehalt wie
Schritt 5: guenstiger Zeitpunkt ist kurz **nach** einem Cronjob-Lauf von
`t3_supertrend` (alle 4 Stunden), damit die Frist von 120 Sekunden nicht mit
dem Bot kollidiert.

Nicht rueckgaengig zu machen. Der Weg zurueck ist derselbe wie in Schritt 5 -
das SQL dort wirkt ueber `WHERE result='manual_close'` und nimmt deshalb nur
manuelle Eingriffe zurueck, nie einen Ausstieg des Bots. Bei **mehreren**
Positionen auf einmal ist das entsprechend mehr Handarbeit: genau deshalb
verlangt dieser Weg zwei Klicks.
