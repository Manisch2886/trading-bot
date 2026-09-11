# Mac dauerhaft wachhalten (caffeinate als launchd-Dienst)

Diese Vorlage haelt den Mac wach, auf dem die neun Paper-Trading-Bots per
Cron laufen — **ohne** dass ein Terminalfenster offen bleiben muss.

## Das Problem

Die Bots werden ausschliesslich von Cron gestartet. Cron laeuft nur, wenn
der Rechner wach ist, und **holt verpasste Laeufe nicht nach**. Ein
schlafender Mac bedeutet also nicht "spaeter", sondern "gar nicht".

Am **11.09.2026** ist genau das passiert: nach einem macOS-Update war das
von Hand gestartete `caffeinate` verschwunden, der Mac schlief zwischen ca.
**08:50 und 12:06**. In dieser Zeit fielen aus:

- der **12:05-Lauf der Binance-Bruecke** — komplett,
- mehrere **stuendliche `elliott_wave`-Forward-Tests**.

Das ist nicht nur eine Luecke im Log. Ein Signal, das waehrend einer
Schlafphase entsteht, wird **nie** erkannt — die Paper-Trading-Auswertung
zeigt danach eine Strategie, die so nie gelaufen ist. Fehlende Laeufe
verfaelschen die Ergebnisse, still und ohne Fehlermeldung.

## Warum ein Dienst und kein Terminalbefehl

Ein von Hand gestartetes `caffeinate` haengt am Terminalfenster und an der
laufenden Sitzung. Es ueberlebt weder einen Neustart noch das Schliessen
des Fensters, und beim macOS-Update vom 11.09. war es ersatzlos weg — ohne
Hinweis. Als launchd-Dienst dagegen:

- startet es bei jeder Anmeldung automatisch (`RunAtLoad`),
- wird es neu gestartet, falls der Prozess stirbt (`KeepAlive`),
- braucht es kein offenes Fenster.

## Die gewaehlten Flags

Der Dienst ruft `/usr/bin/caffeinate -i -m -s` auf — die Flags stehen als
**einzelne** Argumente in der `plist`, nicht zu `-ims` zusammengefasst.

| Flag | Wirkung | Warum |
|---|---|---|
| `-i` | verhindert System-Idle-Sleep | der eigentliche Zweck: der Rechner darf bei Untaetigkeit nicht einschlafen, sonst faellt der naechste Cronjob aus |
| `-m` | verhindert Festplatten-Sleep | eine schlafende Platte verzoegert DB- und Log-Zugriffe der Bots |
| `-s` | verhindert Sleep bei Netzbetrieb | greift genau im Dauerbetriebsfall, fuer den diese Einrichtung gedacht ist |

**Bewusst nicht verwendet:**

| Flag | Wirkung | Warum nicht |
|---|---|---|
| `-d` | haelt das **Display** dauerhaft wach | im Dauerbetrieb unnoetiger Stromverbrauch und Belastung des Displays |
| `-u` | schaltet das Display aktiv **ein** | dasselbe, zusaetzlich noch aktiv statt nur passiv |

Auf die Cronjobs hat das **keinen** Einfluss: ein dunkles Display ist kein
Schlaf. Solange System und Platte wach sind, laufen die Bots.

## Installation

Die Befehle einzeln ausfuehren und zwischendurch die Ausgabe anschauen.
Alle laufen im Projektordner (`cd ~/trading-bot`).

**1. Log-Ordner anlegen** (fehlt er, startet der Dienst nicht — launchd
kann die Log-Dateien dann nicht oeffnen):

```
mkdir -p ~/trading-bot/logs/system
```

**2. Pruefen, ob noch ein von Hand gestartetes `caffeinate` laeuft:**

```
pgrep -fl caffeinate
```

Kommt hier eine Zeile zurueck, vor dem Laden des Dienstes beenden — siehe
Abschnitt "Manuelles caffeinate beenden". Keine Ausgabe heisst: nichts
laeuft, weiter mit Schritt 3.

**3. Vorlage nach `~/Library/LaunchAgents/` kopieren:**

```
cp system/com.manisch.caffeinate.plist ~/Library/LaunchAgents/
```

**4. Dienst laden und starten:**

```
launchctl load ~/Library/LaunchAgents/com.manisch.caffeinate.plist
```

**5. Pruefen, ob der Dienst laeuft:**

```
launchctl list | grep com.manisch.caffeinate
```

Erwartet: eine Zeile mit der Prozess-ID links und `0` (letzter
Beendigungsstatus) in der Mitte.

## Wirkung pruefen

```
pmset -g assertions
```

Erwartet in der Liste — beide Werte auf **1**:

```
   PreventUserIdleSystemSleep     1
   PreventSystemSleep             1
```

`PreventUserIdleSystemSleep` kommt von `-i`, `PreventSystemSleep` von `-s`.
Darunter nennt `pmset` die verantwortlichen Prozesse; dort muss
`caffeinate` auftauchen. Steht bei beiden `0`, laeuft der Dienst nicht —
zurueck zu Schritt 4 und in `logs/system/caffeinate.err.log` schauen.

`PreventUserIdleDisplaySleep` bleibt erwartungsgemaess auf **0**: das
Display darf schlafen, siehe Flag-Begruendung oben.

## Manuelles caffeinate beenden

Damit nicht zwei Prozesse parallel laufen (der Dienst und ein alter
Terminal-Aufruf), zuerst nachsehen, dann gezielt beenden:

```
pgrep -fl caffeinate
```

```
pkill -f '^/usr/bin/caffeinate' ; pkill -x caffeinate
```

Danach erneut `pgrep -fl caffeinate` — nach dem Laden des Dienstes darf
**genau eine** Zeile uebrig bleiben, und zwar die mit `-i -m -s`. Laeuft der
Dienst zu diesem Zeitpunkt schon, startet `KeepAlive` ihn nach dem `pkill`
innerhalb weniger Sekunden von selbst neu; das ist richtig so.

## Deaktivieren und entfernen

**1. Dienst stoppen:**

```
launchctl unload ~/Library/LaunchAgents/com.manisch.caffeinate.plist
```

**2. Vorlage entfernen** (nur noetig, wenn er dauerhaft weg soll — ohne
diesen Schritt startet er bei der naechsten Anmeldung wieder):

```
rm ~/Library/LaunchAgents/com.manisch.caffeinate.plist
```

**3. Kontrolle:**

```
pmset -g assertions
```

Erwartet: `PreventSystemSleep` und `PreventUserIdleSystemSleep` stehen
wieder auf `0`. Der Mac schlaeft ab jetzt wieder ein — und verpasst dann
auch wieder Cronjobs.

## Grenzen — bekannt, hier bewusst nicht geloest

1. **Zugeklapptes MacBook schlaeft trotzdem.** Beim Schliessen des Deckels
   geht der Mac in den Clamshell-Sleep, sofern kein externer Monitor
   angeschlossen ist. Dagegen hilft `caffeinate` nicht — es verhindert
   Idle-Sleep, nicht den vom Nutzer ausgeloesten. Der Mac muss also
   aufgeklappt bleiben.
2. **Ein LaunchAgent startet erst nach der grafischen Anmeldung.** Nach
   einem Neustart muss sich jemand am Mac anmelden, sonst laeuft der Dienst
   nicht. Das gilt heute schon fuer Dashboard und Telegram-Bot und ist
   damit keine neue Einschraenkung.
3. **Ein LaunchDaemon in `/Library/LaunchDaemons` wuerde schon beim
   Systemstart greifen** — also ohne Anmeldung. Er braucht aber `sudo`,
   Eigentuemer `root` und andere Rechte an der Datei. Das ist hier nur als
   **Option erwaehnt und bewusst nicht umgesetzt**.
4. **Bei reinem Batteriebetrieb wirkt `-s` nicht.** Das Flag bezieht sich
   ausdruecklich auf Netzbetrieb. Fuer den Dauerbetrieb gehoert der Mac
   also ans Netzteil.

## Test

Die Vorlage wird automatisch geprueft (gueltiges XML, erwartete Schluessel,
korrekte Flags, kein `-d`/`-u`):

```
python3 system/test_caffeinate_plist.py
```

Der Test laeuft ueberall, auch ohne macOS — er prueft die Datei, nicht den
laufenden Dienst. Die Pruefung auf dem Mac selbst steht in
[`TESTAUFTRAG_CAFFEINATE.md`](TESTAUFTRAG_CAFFEINATE.md).

## Was diese Einrichtung nicht anfasst

Nichts ausserhalb dieses Ordners. Keine `live_params.py`, keine
`forward_test.py`, keine Crontab, und insbesondere **nicht** die
bestehenden launchd-Dienste fuer Dashboard und Telegram-Bot. Das Kopieren
nach `~/Library/LaunchAgents/` fuehrt der Nutzer selbst aus — das Repo
enthaelt nur die Vorlage.
