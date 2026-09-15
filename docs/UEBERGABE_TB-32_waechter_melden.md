# Übergabe TB-32 — Wächter melden

**Stand: 2026-09-14.** Basis `main` (`9afac63`), Branch
`claude/quirky-meitner-gw4k3o`.
Ergebnis: `docs/ERGEBNIS_TB-32_waechter_melden.md` ·
Testauftrag: `docs/TESTAUFTRAG_TB-32_waechter_melden.md` ·
Anleitung: `notifications/README_WAECHTER_MELDEN.md`

---

# 1. Die Entwurfsentscheidung: wann wird gemeldet, wann geschwiegen, und warum genau so

Das war die eigentliche Aufgabe, und sie hat drei Teile.

## 1.1 Drei Ausgänge, nicht zwei

Der naheliegende Entwurf hat zwei Fälle: Befund oder kein Befund. Er ist falsch,
und zwar genau an der Stelle, an der es weh tut.

| Rückgabewert | Ausgang | Folge | Warum |
|---|---|---|---|
| `0` | in Ordnung | **Schweigen**, ausnahmslos | Ein tägliches „alles gut" ist nach einer Woche ungelesen. Ein Kanal mit 364 belanglosen Nachrichten verbirgt die eine, auf die es ankommt. Der Kanal trägt nur, was Handeln verlangt. |
| `1` | Befund | melden, gedämpft | Das Werkzeug hat gearbeitet und etwas gefunden. |
| alles andere | **abgestürzt** | melden, eigener Kopf | Das Werkzeug hat **nicht** gearbeitet. |

**Warum der dritte Fall einen eigenen Kopf bekommt und nicht einfach „auch eine
Meldung" ist:** ein abgestürzter Wächter meldet nie wieder etwas, und Schweigen
sieht von aussen genau aus wie „alles in Ordnung". Bei einem Befund **weiss**
man etwas — bei einem Absturz weiss man **nichts**. Zwei Nachrichten, die
gleich aussähen, wären dieselbe Nachricht; die Unterscheidung muss also im
ersten Wort stehen, nicht im Kleingedruckten. Deshalb `[BEFUND]` gegen
`[ABGESTUERZT]`, und im Absturzfall zusätzlich der Satz „Das Werkzeug selbst ist
gescheitert, es liegt KEIN Befund vor."

**Der Sonderfall, der beinahe durchgerutscht wäre.** Ein unbehandelter
Python-Fehler beendet den Prozess mit Rückgabewert **1** — demselben Wert, mit
dem ein Wächter einen Befund meldet. Ein Wrapper, der nur auf die Zahl sieht,
meldet einen sterbenden Wächter also als „fündig geworden". Unterschieden wird
an der **Fehler**ausgabe: alle fünf Werkzeuge fangen die Traceback eines von
*ihnen* gestarteten Unterprozesses ab und drucken sie in ihre *normale* Ausgabe
(`determinismus.py:174`, `ergebniskurven.py:191`). Steht eine Traceback in
`stderr`, ist das Werkzeug selbst gestorben. Die Probe ist bewusst eng, und ihr
Irrtum fiele in die harmlose Richtung: falsch eingeordnet würde eine Meldung,
verschluckt würde keine.

> Das hat sich sofort bewährt. In der Cloud-Umgebung fehlt `pandas`;
> `ergebniskurven.py` stirbt dort mit Rückgabewert 1 und wird korrekt als
> Absturz gemeldet — nicht als Befund. Ohne diese Probe hätte die erste echte
> Nachricht eine Falschmeldung sein können.

## 1.2 Die Wiederholungsdämpfung — vier Regeln

Ein Wächter, der dieselbe Abweichung dreissig Tage lang täglich meldet, wird
stummgeschaltet. Damit ist auch die **einunddreissigste, neue** Meldung weg. Die
Dämpfung ist kein Komfort, sie schützt den Kanal.

| # | Regel | Entscheidung | Begründung |
|---|---|---|---|
| 1 | **neu** — nichts vermerkt | melden | Der erste Befund *ist* die Nachricht. Würde er gedämpft, hätte die Dämpfung den Zweck des Wrappers aufgehoben. |
| 2 | **geändert** | melden | Der *Inhalt* ist die Information, nicht das Vorhandensein. „3 von 9" und „9 von 9" sind zwei Nachrichten; eine Dämpfung auf „es gibt einen Befund" verschluckt die Eskalation. |
| 3 | **Nachholung** — letzte Meldung ging nicht raus | melden | Sonst verschluckt ein Netzausfall genau die Nachricht, für die es diesen Wrapper gibt. |
| 4 | **Erinnerung** — unverändert, ≥ 7 Tage her | melden | Der Preis der Dämpfung. Ohne sie wäre ein bestehender Befund ab Tag zwei nicht mehr von „alles in Ordnung" zu unterscheiden — genau der Zustand, gegen den dieser Wrapper geschrieben ist. |
| — | sonst | **schweigen** | |

**Verglichen wird genau das, was gesendet würde** — nicht die ganze Ausgabe.
Das ist die wichtigste Einzelentscheidung an der Dämpfung: alle vier Wächter
drucken Laufzeiten (`Gesamtlaufzeit: 41.2s`) und Zeitstempel. Ein Fingerabdruck
darüber wäre jeden Tag ein anderer, die Dämpfung griffe **nie** — und das wäre
erst nach einer Woche täglicher Nachrichten aufgefallen. Der Fingerabdruck
läuft deshalb über Ausgang, Rückgabewert und die ein bis zwei Zeilen, die in
der Nachricht stehen würden. Die Regel lässt sich in einem Satz erklären: *was
gleich aussähe, wird nicht zweimal geschickt.*

**Warum sieben Tage.** Nicht `1` — das ist die tägliche Meldung, also gar keine
Dämpfung. Nicht `30` — dann kann ein Befund einen ganzen Monat unerwähnt
bleiben. Sieben Tage ist der **grösste** Abstand, bei dem ein bestehender Befund
in *jeder* Woche mindestens einmal vorkommt, und zugleich klein genug, dass er
nie mehr als rund vier Nachrichten je Wächter und Monat erzeugt. Die Frist läuft
ab der letzten **erfolgreichen** Meldung, nicht ab dem ersten Auftreten — ein
geänderter Befund setzt sie also zurück, was richtig ist: er ist eine neue
Sache. Einstellbar über `--erinnerung-tage N`.

Die Erinnerung trägt Standzeit und Laufzahl mit („unverändert seit 8 Tagen,
9 Läufe"). Damit ist der Verlauf in der Nachricht selbst sichtbar und nicht nur
die Momentaufnahme.

**Ein Absturz wird nach denselben vier Regeln gedämpft.** Der Ausgang ist Teil
des Fingerabdrucks, der Übergang Befund → Absturz (und zurück) fällt deshalb
immer unter Regel 2 und wird gemeldet — auch am selben Tag.

## 1.3 Was bewusst *nicht* gemeldet wird: die Auflösung

Fällt ein Wächter von Befund zurück auf `0`, wird der Vermerk stillschweigend
geräumt. Keine „behoben"-Nachricht.

Das folgt zwingend aus „0 heisst schweigen", und es hat einen Preis, der hier
offen benannt gehört: nach einer Meldung erfährt man das Ende des Befundes nur
daran, dass die wöchentliche Erinnerung **ausbleibt** — und das Ausbleiben
einer Nachricht ist kein Signal. Dagegen steht, dass eine „behoben"-Meldung
nichts verlangt, was man tun müsste, und der Kanal ausschliesslich tragen soll,
was Handeln verlangt.

**Falls sich das im Betrieb als zu still erweist**, ist die kleinste Änderung
eine **einmalige** „behoben"-Meldung genau dann, wenn zuvor etwas gemeldet
wurde. Sie kann pro Befund nur einmal auftreten und ist damit keine Quelle
täglicher Nachrichten. Steht als offener Punkt 22 im Übergabeprotokoll —
**benannt, nicht entschieden**.

---

# 2. Die harte Bedingung

> **Der Wrapper darf den Wächter nie zum Scheitern bringen.**

Umgesetzt in drei Schichten:

1. **Der Rückgabewert ist immer der des Wächters.** Auch wenn im Meldeteil
   alles brennt.
2. **Die Ausgabe geht durch, bevor der Meldeteil beginnt.** `durchreichen()`
   steht im Ablauf vor `_melden()`. Damit ist das Log geschrieben, bevor
   irgendetwas passieren kann, das mit Telegram zu tun hat. Geprüft wird das
   am **Ablauf**: eine Sende-Attrappe hält fest, was zum Zeitpunkt des Versands
   schon im Log stand.
3. **Der ganze Meldeteil steht in einem `try`.** Zusätzlich fängt
   `_versuche_senden()` Sendefehler eigens ab — nicht aus Vorsicht, sondern für
   die **Unterscheidung**: ein Netzfehler wird als Sendefehler protokolliert und
   führt zu einem sauberen Vermerk, aus dem am nächsten Tag eine *Nachholung*
   wird; ein zusammengebrochener Meldeteil wird als solcher protokolliert.

Protokolliert wird mit dem Präfix `[waechter_melden]` nach `stderr`, also in
dieselbe Logdatei, die der Cronjob ohnehin schreibt (`2>&1`).

**Die einzige Ausnahme** ist ein ausdrücklich gesetztes `--zeitlimit`: dann wird
ein hängender Wächter abgebrochen und als Absturz gemeldet (Rückgabewert 124,
wie `timeout(1)`). Ohne die Option — und so lauten die vorgeschlagenen
Crontab-Zeilen — gibt es kein Zeitlimit und damit kein Verhalten, das der
Wächter heute nicht schon hätte.

---

# 3. Was in der Nachricht steht

Drei Teile: **wer**, **was**, **Befehl zum Nachsehen**.

```
[BEFUND] Ergebniskurven - neu
Zusammenfassung: 3x ABWEICHEND, 6x AKTUELL
BEFUND: 3 von 9 Kurven passen nicht zur heutigen Konfiguration.
Nachsehen: tail -n 60 ~/trading-bot/logs/system/ergebniskurven.log
```

Der Wächter steht **im Klartext** („Ergebniskurven", nicht
`shared/ergebniskurven.py`), höchstens **zwei** Zeilen aus der Ausgabe gehen
mit, jede auf 180 Zeichen gekürzt. Die volle Ausgabe bleibt im Log — eine
Telegram-Nachricht, die man scrollen muss, wird nicht gelesen.

Welche Zeilen mitgehen, entscheidet je Wächter eine Liste von **Marken** in
`WAECHTER` (`waechter_melden.py`). Sie steht dort und nicht im Werkzeug: die
Wächter werden aufgerufen, nicht geändert. Greift keine Marke, fallen die
letzten Ausgabezeilen ein **und die Nachricht sagt das ausdrücklich** — die
Verschlechterung ist sichtbar, nicht still.

Eine Kleinigkeit mit Wirkung: `determinismus.py` nennt jeden betroffenen Bot
**zweimal** (Fortschrittszeile und Tabelle). Ohne Entdopplung kosteten die
beiden Zeilen über denselben Bot den Platz der Zeile über den *zweiten*
betroffenen Bot. Es wird deshalb je Erstwort höchstens eine Zeile übernommen.

Verschickt wird **ohne** `parse_mode`. Der Text enthält fremde Werkzeugausgabe
mit `_`, `*` und Pfaden; Telegrams Legacy-Markdown kennt kein Escaping — die
Root-Cause-Notiz dazu steht seit dem damaligen Live-Bug in
`notify.py::send_report`.

---

# 4. Was gebaut wurde — und was nicht angefasst

| Datei | Art |
|---|---|
| `notifications/waechter_melden.py` | **neu** — der Wrapper |
| `notifications/test_waechter_melden.py` | **neu** — 149 Prüfungen, 9 Mutationsproben |
| `notifications/README_WAECHTER_MELDEN.md` | **neu** — Anleitung, Begründungen, Cron-Zeilen |
| `docs/TESTAUFTRAG_TB-32_waechter_melden.md` | **neu** — eigenständig ausführbar |
| `docs/ERGEBNIS_TB-32_waechter_melden.md` | **neu** — kurzer Ergebnisbericht |
| `docs/UEBERGABE_TB-32_waechter_melden.md` | **neu** — dieses Dokument |
| `notifications/README.md` | eine Zeile in der Struktur-Tabelle |
| `docs/UEBERGABEPROTOKOLL.md` | Abschnitt 4.7, offene Punkte 22 und 23 |
| `.gitignore` | `notifications/waechter_zustand.json` ausgenommen |

**Nicht angefasst:** die fünf Wächter, `notify.py` (`send_alert()` wird
**benutzt**, es gibt keinen zweiten Sendeweg), `live_params.py`,
`forward_test.py`, `equity_simulation.py`, `broker/`, `results/` — und die
**Crontab**.

**Der Wrapper importiert ausschliesslich Standardbibliothek und `notify`.** Das
prüft der Selbsttest per AST, nicht per Textsuche.

## Der fünfte Eintrag: warum die Log-Rotation mitläuft

Die Aufgabe nennt **vier** Wächter, die Crontab hat **fünf** Zeilen.
`system/log_rotation.py` ist kein Wächter — es *tut* etwas —, aber es gibt bei
einem echten Fehlschlag denselben Rückgabewert 1 und schreibt in dasselbe stille
Verzeichnis. Eine Rotation, die scheitert und schweigt, füllt die Platte. Es ist
ein Registereintrag mehr und kein Sonderfall im Code; wer sie nicht wünscht,
lässt die erste Crontab-Zeile unverändert stehen.

---

# 5. Die Tests

```
python3 notifications/test_waechter_melden.py
149 von 149 Pruefungen bestanden, 0 fehlgeschlagen.
```

Kein echter Telegram-Aufruf — der Sendeweg ist ein Parameter, die Attrappe
zählt, hält fest und lässt sich gezielt kaputtmachen (liefert `False`, *oder*
wirft). Ohne `pandas`/`numpy` lauffähig, also auch in der Cloud.

## Die zwei wiederkehrenden Fallen, ausdrücklich adressiert

**Falle 1 — die Probe, die ihren eigenen Zustand herstellt.** Ein Test, der die
Zustandsdatei von Hand schreibt und danach prüft, dass gedämpft wird, bestätigt
nur seine eigene Datei; er bestünde auch dann, wenn der Wrapper gar nichts
vermerkt. **Kein Test hier schreibt eine Zustandsdatei.** Jeder Zustand
entsteht durch einen vorherigen echten Lauf des Wrappers gegen einen echten
Unterprozess, und geprüft wird der **Ablauf** über mehrere Läufe hinweg:
Tag 0 meldet, Tag 1–6 schweigen, Tag 7 erinnert, Tag 8–13 schweigen, Tag 14
erinnert erneut.

**Falle 2 — eine zweite Wache verdeckt das Fehlen der ersten.** Die wichtigste
Zusicherung ist „Rückgabewert 0 → keine Meldung". Prüfte man sie an einem
Wächter, der vorher schon einen Befund vermerkt hatte, könnte das Schweigen
auch von der **Dämpfung** kommen — ein Wrapper, der die Null-Regel gar nicht
kennt, bestünde den Test. `test_null_schweigt` beginnt deshalb mit **leerem**
Zustand: dann gibt es nichts zu dämpfen, und nur die geprüfte Regel kann noch
schweigen. Umgekehrt arbeitet `test_daempfung` durchgehend mit Rückgabewert 1,
wo die Null-Regel nichts verschweigen kann.

## Neun Mutationsproben — und ein echter Fund im eigenen Code

Jede Mutante baut eine kaputte Fassung des Wrappers und lässt die Testdatei
dagegen laufen. Erwartet wird **genau**, welche Abschnitte fehlschlagen —
*nicht mehr und nicht weniger*. „Nicht mehr" ist der schärfere Teil: er belegt,
dass die Abschnitte unabhängig voneinander messen.

> **Die Proben haben einen echten Fehler gefunden.** Die Regel „0 heisst
> schweigen" stand in der ersten Fassung an **zwei** Stellen: in
> `entscheidung()` und noch einmal als Abkürzung in `_melden()`. Die Mutante
> „die Null-Regel fällt weg" veränderte deshalb **nichts** — die zweite Wache
> verdeckte das Fehlen der ersten, im eigenen Code, genau die Falle, gegen die
> diese Proben gebaut sind. Die Abkürzung ist entfernt; ob gesendet wird,
> entscheidet jetzt ausschliesslich `entscheidung()`.

Zusätzlich fällt eine Mutante auf, die gar nicht erst läuft (Syntaxfehler):
ohne diese Prüfung sähe „nicht gelaufen" aus wie „nichts schlägt an" — dieselbe
Selbstbestätigung, nur eine Ebene höher.

---

# 6. Was der Nutzer tun muss

1. **Testauftrag durchgehen**: `docs/TESTAUFTRAG_TB-32_waechter_melden.md`.
   Schritt 6 verschickt wirklich eine Telegram-Nachricht und ist als solcher
   gekennzeichnet; alle übrigen Schritte nicht.
2. **Schritt 4 ernst nehmen.** Meldet dort ein Wächter, bitte hinsehen: steht
   in der Nachricht die Befundzeile — oder
   `(keine bekannte Befundzeile erkannt - letzte Ausgabezeilen:)`? Im zweiten
   Fall gehört die Markenliste des betreffenden Wächters nachgezogen. Die
   Befund-Ausgabe von `ergebniskurven.py` und `determinismus.py` liess sich in
   der Cloud nicht erzeugen (`pandas` fehlt dort), die Marken sind insoweit
   gegen die Quelltexte geschrieben und nicht gegen einen echten Befund.
3. **Die fünf Crontab-Zeilen eintragen** (Schritt 7 des Testauftrags oder
   `notifications/README_WAECHTER_MELDEN.md`). Sie **ersetzen** die am
   14.09.2026 eingetragenen. Vorher `mkdir -p ~/trading-bot/logs/system`.
4. **Am Morgen danach** `python3 notifications/waechter_melden.py --status`.
   `NIE - steht aus` bedeutet: ein Befund liegt vor, die Nachricht ist aber
   nicht zugestellt worden.

---

# 7. Offene Punkte

| # | Punkt | Stand |
|---|---|---|
| 22 | Eine **behobene** Abweichung wird nicht gemeldet (Abschnitt 1.3) | benannt, nicht entschieden |
| 23 | Die **Markenlisten** sind gegen die Quelltexte geprüft, nicht gegen einen echten Befund | Schritt 4 des Testauftrags holt es nach |
| — | Die **Crontab** ist nicht geändert | der Betreiber trägt die fünf Zeilen selbst ein |

Beide inhaltlichen Punkte stehen als 22 und 23 in Abschnitt 9 des
Übergabeprotokolls.
