# Wächter melden — aus einem Rückgabewert wird eine Nachricht

Am 14.09.2026 wurden fünf Werkzeuge in die Crontab eingetragen. Vier davon sind
Wächter: sie prüfen etwas und geben **bei Befund Rückgabewert 1**. Das fünfte
(die Log-Rotation) meldet auf demselben Weg einen echten Fehlschlag.

Alle fünf schreiben ihre Ausgabe in eine Logdatei unter `logs/system/` — **und
dorthin sieht niemand.** Ein Wächter, dessen Befund in einer Datei landet, die
nie jemand öffnet, ist ein Wächter, den es nicht gibt.

`notifications/waechter_melden.py` ist die eine Stelle, die das ändert: sie
führt das Werkzeug aus, lässt dessen Ausgabe **unverändert** ins Log durch und
schickt bei Befund **eine kurze Telegram-Nachricht** über das bestehende
`notify.send_alert()`.

---

## Die Entwurfsentscheidung: wann wird gemeldet, wann geschwiegen

**Drei Ausgänge, nicht zwei.** Das ist der Kern.

| Rückgabewert | Ausgang | Was passiert |
|---|---|---|
| `0` | in Ordnung | **Schweigen.** Ausnahmslos, auch beim ersten Lauf. |
| `1` | Befund | Melden — mit Wiederholungsdämpfung (siehe unten). |
| alles andere | **abgestürzt** | Melden, **unterscheidbar gekennzeichnet**. |

**Warum `0` ausnahmslos schweigt.** Ein tägliches „alles gut" ist nach einer
Woche ungelesen, und ein Kanal mit 364 belanglosen Nachrichten verbirgt die
eine, auf die es ankommt. Der Kanal trägt nur, was Handeln verlangt.

**Warum der Absturz einen eigenen Kopf bekommt.** Das ist der gefährlichste der
drei Fälle: ein abgestürzter Wächter meldet nie wieder etwas, und Schweigen
sieht von aussen genau aus wie „alles in Ordnung". Bei einem Befund **weiss**
man etwas, bei einem Absturz weiss man **nichts** — zwei Nachrichten, die
dasselbe Aussehen hätten, wären dieselbe Nachricht.

> **Der Sonderfall, der leicht durchgerutscht wäre:** Ein unbehandelter
> Python-Fehler beendet den Prozess mit Rückgabewert **1** — demselben Wert,
> mit dem ein Wächter einen Befund meldet. Der Wrapper unterscheidet die beiden
> an der Fehlerausgabe: alle fünf Werkzeuge fangen die Traceback eines von
> *ihnen* gestarteten Unterprozesses ab und drucken sie in ihre *normale*
> Ausgabe (`determinismus.py:174`, `ergebniskurven.py:191`). Steht eine
> Traceback in der **Fehler**ausgabe, ist das Werkzeug selbst gestorben. Die
> Probe ist bewusst eng, und ihr Irrtum fiele in die harmlose Richtung: falsch
> eingeordnet würde eine Meldung, verschluckt würde keine.

---

## Die Wiederholungsdämpfung — und warum genau diese

Ein Wächter, der dieselbe Abweichung dreissig Tage lang täglich meldet, wird
stummgeschaltet — und damit ist auch die einunddreissigste, **neue** Meldung
weg. Die Dämpfung ist kein Komfort, sie schützt den Kanal.

Vier Regeln, in dieser Reihenfolge geprüft:

| # | Regel | Entscheidung |
|---|---|---|
| 1 | **Neu** — zu diesem Wächter ist nichts vermerkt | melden |
| 2 | **Geändert** — der Befund liest sich anders als zuletzt | melden |
| 3 | **Nachholung** — die letzte Meldung ging nicht raus | melden |
| 4 | **Erinnerung** — unverändert, letzte Meldung ≥ 7 Tage her | melden |
| — | sonst | **schweigen** |

**Zu 1.** Der erste Befund *ist* die Nachricht. Würde er gedämpft, hätte die
Dämpfung den Zweck des ganzen Wrappers aufgehoben.

**Zu 2.** Der *Inhalt* des Befundes ist die Information, nicht sein
Vorhandensein. „3 von 9 Kurven passen nicht" und „9 von 9 Kurven passen nicht"
sind zwei verschiedene Nachrichten; eine Dämpfung, die nur auf „es gibt einen
Befund" schaut, verschluckt die Eskalation. Verglichen wird deshalb **genau
das, was gesendet würde** — nicht die ganze Ausgabe. Das ist wichtiger, als es
klingt: alle vier Wächter drucken Laufzeiten (`Gesamtlaufzeit: 41.2s`), und ein
Fingerabdruck darüber wäre jeden Tag ein anderer. Die Dämpfung griffe nie, und
das wäre erst nach einer Woche täglicher Nachrichten aufgefallen.

**Zu 3.** Schlägt der Versand fehl (Netz weg, Token falsch), darf der Befund
**nicht** als gemeldet gelten — sonst verschluckt ein Netzausfall genau die
Nachricht, für die es diesen Wrapper gibt. Vermerkt wird erst, wenn die Wirkung
eingetreten ist. Dieselbe Lehre, die `schliess_benachrichtigung.py` aus dem
Fehler von `monitor.py` gezogen hat.

**Zu 4.** Die Erinnerung ist der *Preis* der Dämpfung. Ohne sie wäre ein
bestehender Befund ab Tag zwei nicht mehr von „alles in Ordnung" zu
unterscheiden — und damit wäre genau der Zustand wiederhergestellt, gegen den
dieser Wrapper geschrieben ist.

**Warum sieben Tage.** Nicht `1` — das ist die tägliche Meldung, also gar keine
Dämpfung. Nicht `30` — dann kann ein Befund einen ganzen Monat lang unerwähnt
bleiben. Sieben Tage ist der grösste Abstand, bei dem ein bestehender Befund in
**jeder** Woche mindestens einmal vorkommt, und zugleich klein genug, dass er
nie mehr als rund vier Nachrichten je Wächter und Monat erzeugt. Die Erinnerung
trägt Standzeit und Laufzahl mit („unverändert seit 8 Tagen, 9 Läufe"), damit
der Verlauf in der Nachricht selbst sichtbar ist. Einstellbar über
`--erinnerung-tage N`.

Ein **Absturz** wird nach denselben vier Regeln gedämpft. Der Ausgang ist Teil
des Fingerabdrucks: der Übergang Befund → Absturz (und zurück) fällt deshalb
immer unter Regel 2 und wird gemeldet.

**Was bewusst nicht gemeldet wird: die Auflösung.** Fällt ein Wächter von
Befund zurück auf `0`, wird der Vermerk stillschweigend gelöscht. Das folgt aus
„0 heisst schweigen" und kostet eine Bestätigung, dass etwas behoben ist — der
Kanal bleibt dafür frei von allem, was kein Handeln verlangt. Siehe offener
Punkt in der Übergabe.

---

## Die harte Bedingung: der Wrapper bringt den Wächter nie zum Scheitern

Der Rückgabewert dieses Programms ist **immer** der des Wächters, und dessen
Ausgabe geht unverändert nach `stdout`/`stderr` — **bevor** auch nur der
Versuch einer Meldung unternommen wird. Erst danach folgt der Meldeteil, und
der steht vollständig in einem `try`.

Ob Telegram erreichbar ist, ob der Token stimmt, ob die Zustandsdatei lesbar
ist: nichts davon erreicht den Rückgabewert, und nichts davon verhindert, dass
das Log geschrieben wird. Ein Sendefehler wird protokolliert (mit dem Präfix
`[waechter_melden]` in der Fehlerausgabe, also in derselben Logdatei), nicht
weitergereicht.

Die einzige Ausnahme ist ein **ausdrücklich gesetztes** `--zeitlimit`: dann
wird ein hängender Wächter abgebrochen und als Absturz gemeldet
(Rückgabewert 124, wie bei `timeout(1)`). Ohne die Option — und so lauten die
Zeilen unten — gibt es kein Zeitlimit und damit kein Verhalten, das der Wächter
heute nicht schon hätte.

---

## Was in der Nachricht steht

Kurz genug fürs Telefon, vollständig genug zum Handeln. Drei Teile: **wer**,
**was**, und der Befehl zum **Nachsehen**.

```
[BEFUND] Ergebniskurven - neu
Zusammenfassung: 3x ABWEICHEND, 6x AKTUELL
BEFUND: 3 von 9 Kurven passen nicht zur heutigen Konfiguration.
Nachsehen: tail -n 60 ~/trading-bot/logs/system/ergebniskurven.log
```

```
[ABGESTUERZT] Determinismus der Backtests - neu
Rueckgabewert 2 - weder 0 (in Ordnung) noch 1 (Befund). Das Werkzeug selbst
ist gescheitert, es liegt KEIN Befund vor.
ModuleNotFoundError: No module named 'scipy'
Nachsehen: tail -n 60 ~/trading-bot/logs/system/determinismus.log
```

Höchstens **zwei** Zeilen aus der Ausgabe gehen mit; die volle Ausgabe bleibt
im Log. Eine Telegram-Nachricht, die man scrollen muss, wird nicht gelesen.

Welche Zeilen mitgehen, entscheidet je Wächter eine Liste von **Marken** in
`waechter_melden.py` (`WAECHTER`). Sie steht dort und nicht im Werkzeug — die
Wächter werden aufgerufen, nicht geändert. Greift keine Marke, weil ein
Werkzeug seine Ausgabe umformuliert hat, fallen die letzten Ausgabezeilen ein
**und die Nachricht sagt das ausdrücklich**; die Verschlechterung ist sichtbar
und nicht still.

Verschickt wird **ohne** `parse_mode`. Der Text enthält fremde Werkzeugausgabe
mit `_`, `*` und Pfaden, und Telegrams Legacy-Markdown kennt kein Escaping —
die Root-Cause-Notiz dazu steht in `notify.py::send_report`.

---

## Die fünf Crontab-Zeilen (Vorschlag — **nicht eingetragen**)

Die Crontab liegt beim Nutzer und wurde von dieser Änderung **nicht**
angefasst. Die folgenden fünf Zeilen **ersetzen** die am 14.09.2026
eingetragenen: gleiche Zeiten, gleiche Logdateien, gleiche Rückgabewerte —
nur mit Meldung.

```cron
30 3 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py log_rotation >> logs/system/log_rotation.log 2>&1
50 3 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py ergebniskurven >> logs/system/ergebniskurven.log 2>&1
10 4 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py determinismus >> logs/system/determinismus.log 2>&1
30 4 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py versuchsregister >> logs/system/versuchsregister.log 2>&1
40 4 * * * cd ~/trading-bot && /usr/bin/python3 notifications/waechter_melden.py kapitalsimulation >> logs/system/kapitalsimulation.log 2>&1
```

Vorher einmalig: `mkdir -p ~/trading-bot/logs/system`.

**Warum die Log-Rotation mitläuft, obwohl sie kein Wächter ist.** Sie gibt bei
einem echten Fehlschlag denselben Rückgabewert 1 und schreibt in dasselbe
stille Verzeichnis. Eine Rotation, die scheitert und schweigt, füllt die
Platte. Es ist ein Registereintrag mehr und kein Sonderfall im Code; wer sie
nicht wünscht, lässt die erste Zeile unverändert stehen.

**Der Wächter läuft mit demselben Python wie der Wrapper** (`sys.executable`),
und immer mit dem Projektwurzelverzeichnis als Arbeitsverzeichnis — das `cd`
ist damit nicht mehr nötig, steht aber drin, weil die Logdatei relativ
angegeben ist.

---

## Nachsehen und ausprobieren

```bash
# Was ist bekannt, und was steht gerade offen?
python3 notifications/waechter_melden.py --status

# Einen Waechter ausfuehren und die Nachricht sehen, OHNE zu senden
# und OHNE etwas zu vermerken:
python3 notifications/waechter_melden.py ergebniskurven --trockenlauf

# Scharf, von Hand (schickt wirklich, falls es einen Befund gibt):
python3 notifications/waechter_melden.py ergebniskurven
```

**Zustandsdatei:** `notifications/waechter_zustand.json`. Sie hält je Wächter
fest, welcher Befund zuletzt gemeldet wurde und wann. Reine Laufzeitdaten, kein
Secret — steht wie `notifications/state.json` und
`notifications/warteauftraege.json` in `.gitignore`.

Geht sie verloren, gilt ein bestehender Befund wieder als *neu* und wird einmal
erneut gemeldet. Das ist die **sichere Richtung**: eine Meldung zu viel, nie
eine verschluckte.

**Selbsttests:** `python3 notifications/test_waechter_melden.py` — ohne einen
einzigen echten Telegram-Aufruf und ohne `pandas`/`numpy`.

**Testauftrag:** `docs/TESTAUFTRAG_TB-32_waechter_melden.md`.
