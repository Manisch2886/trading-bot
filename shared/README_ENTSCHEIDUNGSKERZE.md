# Die gemeinsame Abrufschicht (TB-38)

`shared/entscheidungskerze.py` · `shared/umstellungstag.py`

---

## Die Regel, in einem Satz

> **Entscheidungskerze ist die letzte Kerze, deren `close_time` vor der
> Startzeit des Laufs liegt.**

Ausgeschrieben: `schluss < startzeit`, wobei `schluss` der **letzte
Augenblick ist, der noch zur Kerze gehört** — bei Binance ist das
`open + Länge − 1 ms` (Feld 6 der Rohkerze), bei einer NYSE-Tageskerze der
Sitzungsschluss.

Warum die Lesart von `close_time` hier kein Detail ist: Läge der Schluss der
08:00-Kerze eines Vier-Stunden-Charts bei `12:00:00` statt bei
`11:59:59.999`, dürfte ein Lauf um 12:00:00 sie nicht nehmen und müsste auf
die 04:00-Kerze zurückgreifen — acht Stunden alt. Mit der Lesart der
Datenquelle bedeutet die Regel das Richtige: **die soeben fertig gewordene
Kerze wird genommen, die laufende nicht.**

Die Grenze ist damit ebenfalls festgelegt: eine Kerze, deren `close_time`
**genau** auf der Startzeit liegt, wird **nicht** genommen (striktes `<`).

---

## Was die Schicht tut

```python
from entscheidungskerze import lade, melde, KRYPTO

df = lade(symbol, INTERVAL, KRYPTO,
          abruf=lambda: fetch_historical_data(symbol, INTERVAL, LOOKBACK))
...
melde()          # einmal am Ende des Laufs
```

1. `data/<symbol>_<intervall>.csv` lesen.
2. Kerzen ohne Kurse streichen (`kursdaten.entferne_unvollstaendige`).
3. **Frische prüfen.** Fehlt die erwartete Entscheidungskerze → `abruf()`,
   also genau der bisherige Live-Abruf des Bots.
4. **Auf beide Quellen dieselbe Regel anwenden.**

`df` endet danach auf der Entscheidungskerze. `df.iloc[-1]` in den neun Bots
bleibt stehen und bedeutet ab jetzt das, was es immer bedeuten sollte.

---

## Die vier Entscheidungen — und ihre Begründung

### 1. Eigenes Modul, aber **keine** zweite Regel

Die Regel selbst steht weiter genau einmal, in
`shared/abrufschutz.abgeschlossen_maske` (TB-35), zeichengleich mit
`shared/kursdaten_neuaufbau.abgeschlossene_kerzen` (TB-34). Für Krypto ruft
diese Schicht sie auf und rechnet sie **nicht nach**.

Neu ist nicht die Regel, sondern die **Tür**: woher die Daten kommen, welche
Startzeit gilt, und dass eine Abweichung gemeldet wird.

Warum trotzdem ein eigenes Modul: `abrufschutz` schützt den **Schreibpfad**
der acht `fetch_*.py` — dort kostet zu langes Warten nichts. Hier geht es um
den **Lesepfad** der neun Bots — dort kostet zu langes Warten einen ganzen
Handelstag. Zwei entgegengesetzte Risikoprofile in einer Datei wären
schwerer zu lesen als zwei Dateien mit je einem.

### 2. Aktien: dieselbe Regel, **andere Schranke**

`abrufschutz` setzt den Schluss einer Tageskerze auf `D 23:59:59` — eine
bewusst konservative Schranke, für den Schreibpfad richtig.

Für den Entscheidungspfad wäre sie **falsch**, und zwar messbar:

| | |
|---|---|
| Cron der vier Aktien-Bots | werktags **22:15 Uhr** Ortszeit (`crontab -l`, 11.09.2026) |
| das ist in UTC | 20:15 (Sommer) bzw. 21:15 (Winter) |
| NYSE-Schluss in UTC | 20:00 (Sommer) bzw. 21:00 (Winter) |
| Abstand | **15 Minuten nach Handelsschluss** |
| mit `D 23:59:59` | die Kerze von heute gilt als „nicht fertig" → **jedes Signal einen Handelstag zu spät** |

Die Frage ist hier also **zweiseitig teuer** — genau der Fall, von dem der
Kopf von `abrufschutz.py` sagt, dass eine Faustregel ihn nicht trägt.
Zuständig ist deshalb `notifications/boersenkalender.py`: der echte
NYSE-Kalender, mit Feiertagen, verkürzten Handelstagen und
US-Zeitumstellung. Kosten: **eine** Abfrage je Lauf, nicht eine je Zeile.

**Kann der Kalender nicht antworten** (Bibliothek fehlt), wird nicht
geraten — der Kopf von `boersenkalender.py` verbietet eine Faustregel als
Rückfallebene ausdrücklich. Stattdessen gilt die sichere Schranke aus
`abrufschutz`, **und der Lauf meldet, dass er sie benutzt hat.** Preis: ein
um einen Tag verspätetes Signal. Gewinn: nie eine Teilkerze, und die
Abweichung ist sichtbar statt still.

### 3. Die Startzeit: **ein** Wert für den ganzen Lauf

`laufbeginn()` merkt sich den Zeitpunkt beim ersten Gebrauch im Prozess.

Ein Wert, der sich während des Laufs ändert, erzeugt innerhalb desselben
Laufs verschiedene Entscheidungskerzen: bei 25 Symbolen über eine
Stundengrenze hinweg bekämen die ersten Symbole Kerze N und die restlichen
Kerze N+1 — und weil alle neun Bots ihr Positionslimit laufend hochzählen,
hinge das Ergebnis dann auch von der Reihenfolge der Symbole ab.

**Bewusst keine Umgebungsvariable.** Ein `export`, das jemand einmal ins
Shell-Profil schreibt und vergisst, würde alle neun Bots dauerhaft auf einer
alten Kerze einfrieren — lautlos, denn ein eingefrorener Lauf sieht in den
Zahlen genauso aus wie „kein Signal". Für Selbsttests und für das
Nachstellen eines Laufs gibt es `setze_laufbeginn()` und das Argument
`startzeit`.

### 4. Die Meldung: dieselbe Leitung und dieselbe Dämpfung wie TB-32

Eine Meldung in einer Protokollzeile ist keine Meldung — `logs/` sieht
niemand an. Gemeldet wird deshalb über `notify.send_alert()`, **die eine**
Telegram-Leitung des Projekts; keine zweite Anbindung, kein Crontab-Eintrag,
keine Änderung an `notify.py`.

Gedämpft wird mit den **Funktionen** aus `notifications/waechter_melden.py`
(nicht mit einer zweiten Fassung derselben vier Regeln):

| # | Regel | |
|---|---|---|
| 1 | **neu** | melden |
| 2 | **geändert** | melden |
| 3 | **Nachholung** (letzte Meldung ging nicht raus) | melden |
| 4 | **Erinnerung** (unverändert, ≥ 7 Tage her) | melden |
| — | sonst | **schweigen** |

Drei harte Bedingungen, alle aus TB-32:

* Der Meldeteil **bringt den Bot nie zum Scheitern** — alles in einem `try`.
* Ein fehlgeschlagener Versand gilt als **nicht zugestellt** und wird
  nachgeholt.
* **Genau einmal je Lauf**, mit allen betroffenen Symbolen in einer
  Nachricht — nicht 25 Nachrichten.

Fehlt `waechter_melden`, wird **ungedämpft** gemeldet statt gar nicht: eine
Nachricht zu viel, nie eine verschluckte.

Zustand: `notifications/rueckfall_zustand.json` (in `.gitignore`).

---

## Der Umstellungstag

`shared/umstellungstag.py` hält je Bot fest, ab wann er auf der
Entscheidungskerze entscheidet.

```bash
python3 shared/umstellungstag.py --festhalten --alle
python3 shared/umstellungstag.py --zeigen
python3 shared/umstellungstag.py --pruefen      # 1, wenn ein Bot fehlt
```

Maschinenlesbar in **`docs/umstellungstag_entscheidungskerze.json`**,
Prosa-Fassung in `docs/DATENLUECKEN.md`. Gelesen wird die Datei **vom
Vergleich, nicht von den Bots** — deshalb liegt sie in `docs/` und nicht in
`shared/` oder `strategies/`.

Ein zweiter Aufruf rückt den Zeitpunkt **nicht** vor: der Umstellungstag ist
eine Tatsache, kein Zustand. `--erneut` überschreibt ausdrücklich und bewahrt
den alten Wert als `frueher`.

---

## Als Werkzeug

```bash
python3 shared/entscheidungskerze.py
python3 shared/entscheidungskerze.py --stand "2026-09-15 12:00:00"
python3 shared/entscheidungskerze.py --json bericht.json
```

Zeigt je Bot die erwartete Entscheidungskerze und listet die Kursdateien, für
die sie in `data/` fehlt. Rein lesend. Rückgabewert 1 bei Befund — dieselbe
Hausregel wie `shared/kursdaten.py`.

---

## Selbsttests

```bash
python3 shared/test_entscheidungskerze.py      # 130 Prüfungen
python3 shared/test_umstellungstag.py          #  25 Prüfungen
```

Drei der neun `forward_test.py` werden dabei **wirklich ausgeführt**, in
einem Miniatur-Abbild des Projekts unter `/tmp`, gegen erzeugte
Beispieldaten — beobachtet wird, was danach in ihrer Datenbank steht. Ohne
Netz; Binance, yfinance und Telegram laufen gegen Attrappen. Kein Test fasst
`data/` dieses Repos an.

`pandas_market_calendars` ist für den Aktien-Abschnitt nötig; fehlt es,
überspringt der Test ihn und prüft stattdessen den dokumentierten
Rückfall auf die sichere Schranke.
