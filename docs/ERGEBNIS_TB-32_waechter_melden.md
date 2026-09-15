# Ergebnis TB-32 — Wächter melden

**Stand: 2026-09-14.** Basis `main` (`9afac63`).
Testauftrag: `docs/TESTAUFTRAG_TB-32_waechter_melden.md`.
Übergabe: `docs/UEBERGABE_TB-32_waechter_melden.md`.

---

## Die Entscheidung in einem Satz

**Gemeldet wird ein Befund und ein Absturz — geschwiegen wird bei „in Ordnung",
ausnahmslos, und bei einem unveränderten Befund, den man schon kennt, bis auf
eine Erinnerung alle sieben Tage.**

---

## Drei Ausgänge, nicht zwei

| Rückgabewert | Ausgang | Folge |
|---|---|---|
| `0` | in Ordnung | **Schweigen**, auch beim ersten Lauf |
| `1` | Befund | melden, gedämpft |
| alles andere | **abgestürzt** | melden, eigener Kopf `[ABGESTUERZT]` |

Der dritte Fall ist der gefährlichste: ein abgestürzter Wächter meldet nie
wieder etwas, und Schweigen sieht von aussen genau aus wie „alles in Ordnung".
Bei einem Befund **weiss** man etwas, bei einem Absturz weiss man **nichts**.

**Der Sonderfall, der sonst durchgerutscht wäre:** ein unbehandelter
Python-Fehler endet mit Rückgabewert **1** — demselben Wert wie ein Befund.
Unterschieden wird an der **Fehler**ausgabe: alle fünf Werkzeuge drucken die
Traceback eines von *ihnen* gestarteten Unterprozesses in ihre *normale*
Ausgabe, eine Traceback in `stderr` bedeutet also, dass das Werkzeug selbst
gestorben ist. Das hat sich sofort bewährt — in der Cloud-Umgebung ohne
`pandas` stirbt `ergebniskurven.py` mit Rückgabewert 1 und wird korrekt als
Absturz gemeldet, nicht als Befund.

## Die Wiederholungsdämpfung

| # | Regel | Entscheidung |
|---|---|---|
| 1 | **neu** — nichts vermerkt | melden |
| 2 | **geändert** — liest sich anders als zuletzt | melden |
| 3 | **Nachholung** — letzte Meldung ging nicht raus | melden |
| 4 | **Erinnerung** — unverändert, letzte Meldung ≥ 7 Tage her | melden |
| — | sonst | **schweigen** |

Verglichen wird **genau das, was gesendet würde** — nicht die ganze Ausgabe.
Alle vier Wächter drucken Laufzeiten; ein Fingerabdruck darüber wäre täglich
ein anderer, und die Dämpfung griffe nie. Das wäre erst nach einer Woche
täglicher Nachrichten aufgefallen.

**Sieben Tage**, weil das der grösste Abstand ist, bei dem ein bestehender
Befund in *jeder* Woche mindestens einmal vorkommt — und klein genug für
höchstens rund vier Nachrichten je Wächter und Monat.

## Die harte Bedingung

Der Rückgabewert ist **immer** der des Wächters. Die Ausgabe geht unverändert
durch, **bevor** der Meldeteil beginnt; der steht vollständig in einem `try`.
Ein Sendefehler wird protokolliert, nicht weitergereicht — und der Befund gilt
dann als *nicht* zugestellt und wird beim nächsten Lauf nachgeholt.

---

## Was gebaut wurde

| Datei | Art |
|---|---|
| `notifications/waechter_melden.py` | neu, 695 Zeilen (gut die Hälfte davon Begründung im Kopf) |
| `notifications/test_waechter_melden.py` | neu, 149 Prüfungen inkl. 9 Mutationsproben |
| `notifications/README_WAECHTER_MELDEN.md` | neu |
| `docs/TESTAUFTRAG_TB-32_waechter_melden.md` | neu |
| `docs/ERGEBNIS_TB-32_waechter_melden.md` | neu (dieses Dokument) |
| `docs/UEBERGABE_TB-32_waechter_melden.md` | neu |
| `notifications/README.md` | eine Zeile |
| `docs/UEBERGABEPROTOKOLL.md` | Abschnitt 4.7, offene Punkte 22 und 23 |
| `.gitignore` | Zustandsdatei ausgenommen |

**Nicht angefasst:** die fünf Wächter, `notify.py`, `live_params.py`,
`forward_test.py`, `equity_simulation.py`, `broker/`, `results/` — und die
**Crontab**.

---

## Eine Nachricht, wie sie ankommt

```
[BEFUND] Ergebniskurven - neu
Zusammenfassung: 3x ABWEICHEND, 6x AKTUELL
BEFUND: 3 von 9 Kurven passen nicht zur heutigen Konfiguration.
Nachsehen: tail -n 60 ~/trading-bot/logs/system/ergebniskurven.log
```

```
[ABGESTUERZT] Ergebniskurven - neu
Rueckgabewert 1, aber mit einer Traceback in der Fehlerausgabe. Das Werkzeug
selbst ist gescheitert, es liegt KEIN Befund vor.
ModuleNotFoundError: No module named 'pandas'
Nachsehen: tail -n 60 ~/trading-bot/logs/system/ergebniskurven.log
```

Drei Teile: **wer**, **was**, **Befehl zum Nachsehen**. Höchstens zwei Zeilen
aus der Ausgabe; der Rest bleibt im Log.

---

## Testergebnis

```
python3 notifications/test_waechter_melden.py
149 von 149 Pruefungen bestanden, 0 fehlgeschlagen.
```

Kein einziger echter Telegram-Aufruf; der Sendeweg ist ein Parameter. Ohne
`pandas`/`numpy` lauffähig.

**Neun Mutationsproben**, jede mit der Erwartung, welche Abschnitte anschlagen
müssen — *nicht mehr und nicht weniger*:

| Mutante | schlägt an in |
|---|---|
| die Null-Regel fällt weg | 2, 2b, 7, 9 |
| die Dämpfung fällt weg | 5, 5b, 5c, 9 |
| die wöchentliche Erinnerung fällt weg | 5, 9 |
| fehlgeschlagener Versand gilt als zugestellt | 4, 5, 5c |
| ein Absturz wird wie ein Befund gemeldet | 3, 8 |
| Traceback mit Rückgabewert 1 gilt als Befund | 3 |
| erst melden, dann das Log schreiben | 4, 4b |
| ein Sendefehler wird weitergereicht | 4 |
| Fingerabdruck über die ganze Ausgabe | 5b |

> **Die Proben haben einen echten Fehler im Wrapper gefunden.** Die Regel
> „0 heisst schweigen" stand anfangs an **zwei** Stellen — in `entscheidung()`
> und noch einmal in `_melden()`. Eine davon zu entfernen änderte nichts: die
> zweite Wache verdeckte das Fehlen der ersten. Genau die Falle, gegen die die
> Proben gebaut sind, im eigenen Code. Sie steht jetzt einmal.

**Basislauf auf unverändertem `main`** (Cloud-Umgebung, 2026-09-14): **44**
Testdateien, davon **11 `OK`** und **33 `FEHLER`** — durchweg
`ModuleNotFoundError` für `pandas`, `scipy`, `binance`, `yfinance`, `fastapi`.
Vorbestehend und von TB-32 unberührt. Nach der Änderung: 45 Dateien, **12 `OK`**
(die neue kommt hinzu) und **dieselben 33 `FEHLER`**.

Auf dem Rechner des Nutzers ist die Lage umgekehrt — dort fehlen die
Abhängigkeiten nicht, und `dashboard/test_dashboard.py` meldet ohne `node`
780/780 statt 784. Der Basislauf aus Schritt 0 des Testauftrags zeigt das.

---

## Offene Punkte

1. **Eine behobene Abweichung wird nicht gemeldet.** Fällt ein Wächter von
   Befund zurück auf `0`, wird der Vermerk stillschweigend geräumt. Folgt
   zwingend aus „0 heisst schweigen", kostet aber die Bestätigung, dass etwas
   behoben ist. Kleinste Änderung, falls das im Betrieb zu still ist: eine
   **einmalige** „behoben"-Meldung, die pro Befund nur einmal auftreten kann.
   *Benannt, nicht entschieden.*

2. **Die Markenlisten sind gegen die Ausgabe der Wächter geprüft, nicht gegen
   einen echten Befund** von `ergebniskurven.py` und `determinismus.py` — beide
   brauchen `pandas`, das in der Cloud fehlt. Greift keine Marke, fällt der
   Wrapper auf die letzten Ausgabezeilen zurück **und schreibt das in die
   Nachricht**; still falsch ist er nie. Schritt 4 des Testauftrags holt die
   Prüfung auf dem Rechner des Nutzers nach.

3. **Die Crontab wurde nicht geändert.** Die fünf neuen Zeilen stehen als
   Vorschlag in `notifications/README_WAECHTER_MELDEN.md` und in Schritt 7 des
   Testauftrags; der Betreiber trägt sie selbst ein.
