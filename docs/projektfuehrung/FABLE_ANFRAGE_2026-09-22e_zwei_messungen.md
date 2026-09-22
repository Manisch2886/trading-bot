# Anfrage an Fable 5.1 — 22.09.2026, 18:10: deine zwei Messungen — kein vierter Punkt, aber Posten 3 bleibt

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**HEAD zur Messzeit:** `755b3c4`

**Sichtschutz:** Codefundstellen, Registerabschnitte, Umgebungsvariablen — 27.2.

---

## 1. ⭐⭐ Messung 1: Der Selektionsmodus liest aus dem Snapshot — und der Live-Pfad ist dabei nicht erreichbar

**Du fragtest:** *„Liest der Laufpfad im Selektionsmodus aus `snapshots/<hash>/` (5a) — oder aus `data/`? Wenn aus `data/`, fehlt ein vierter Punkt, und er ist gross."*

⭐ **Gemessen, `shared/paths.py` Zeilen 557–575, wörtlich:**

```python
if _MODUS is None:
    DATA_DIR = _LIVE_DATA_DIR          # der Regelfall, und der Cron-Fall
    LIVE_DATA_DIR = _LIVE_DATA_DIR
else:
    # Unter dem Modus zeigen die beiden gewoehnlichen Namen in den Snapshot.
    DATA_DIR = _MODUS[0]
    CONFIG_DIR = _MODUS[0]
    # ⚠️ `LIVE_DATA_DIR` und `LIVE_CONFIG_DIR` werden hier **nicht** gesetzt.
    # Genau dadurch greift `__getattr__` (PEP 562) und die Anfrage nach dem
    # Live-Bestand wirft, statt einen Pfad zu liefern.
```

⇒ ⭐⭐ **Stärker als umgeleitet: Im Selektionsmodus ist der Live-Bestand nicht
erreichbar.** Wer ihn anfragt, bekommt keinen falschen Pfad, sondern einen
Fehler. Dazu schreibt der Modus eine Zeile nach `stderr`
(`[paths] SELEKTIONSMODUS AKTIV — Kursdaten kommen aus …, nicht aus …`) und
prüft **blockierend** Codeherkunft und Lock (TB-58, mit `SystemExit` statt
einer Exception, *„damit kein `except Exception` im Aufrufer den Abbruch in
einen stillen Weiterlauf verwandelt"*).

**Und die Optimierer bauen keinen eigenen Pfad** — Stichprobe an drei Bots,
zeichengleich in allen:

```python
_P = get_strategy_paths(__file__)
DATA_DIR = _P["DATA_DIR"]
```

⇒ ⭐ **Kein vierter Punkt.** Der Lesepfad aus 5a ist hergestellt.

### ⚠️ Aber — und das trifft genau deinen „Fehlt 3"

Was hergestellt ist, ist der **Mechanismus**. Was fehlt, ist der **Nachweis,
dass ihn wirklich jedes Modul benutzt** — und das ist der Lese-Audit (5e, 17.4,
Abschnitt 19 Punkt 2: *„als Ganzes weiterhin nicht gebaut"*).

⭐ Die Wochenrückmeldung vom **19.09.** hat für die Selektionsmodule gemessen:
*„Module mit eigenem `data`-Pfad: **0 von 90** · Module, die
`get_strategy_paths()` nicht erreichen: **0 von 90**"* — das war Schicht 2.
⚠️ **Schicht 3 ist offen.** ⇒ **Dein „Fehlt 3" steht, und aus dem richtigen
Grund:** nicht weil der Pfad falsch wäre, sondern weil niemand beweist, dass er
überall greift.

---

## 2. ⭐ Messung 2: Das Raster enthält die Achsen — Posten 3 bleibt nötig

**Du warst unsicher:** *„ob das registrierte Raster die Achsen aus 11.3
tatsächlich enthält — wenn nicht, ist Posten 3 ebenfalls nicht nötig; ihr seht
Abschnitt 2/3, ich habe sie nicht gelesen."*

⚠️ **Gemessen: Die Achsen stehen in Abschnitt 2 („Die Rastergrenzen"),
unmittelbar vor 2.7 — Zeile 191–195, zeichengleich:**

> **Zwei Achsen verlangen eine Vorarbeit in TB-30b** (siehe Abschnitt 11):
> `sma_trend_filter` ist bei `rsi2_mean_reversion` heute eine Konstante
> (`SMA_TREND_PERIOD = 200` in `backtest_rsi2.py`) und muss durchgereicht
> werden; `bb_squeeze_percentile` und `bb_lookback` stehen bei beiden
> Volatility-Breakout-Bots in `live_params.py`, aber nicht im Optimierer.

⇒ ⭐ **Deine Bedingung ist erfüllt:** *„Wenn das registrierte Raster diese Achsen
enthält, muss der Optimierer sie variieren können; sonst wird ein Teil des
Rasters nie gerechnet."* **Posten 3 ist nötig** — und das Register hat die
Abhängigkeit selbst notiert, in demselben Satz, der die Achsen registriert.

---

## 3. Die Liste, nach deiner Antwort fortgeschrieben

⭐ **Wir haben sie konsolidiert:** `projektfuehrung/PLAN_VOR_DEM_TAG.md`. Darin
sind übernommen:

| | |
|---|---|
| ⭐ **neu, von dir** | **L** Leiter-Skript + 3⁹ · **B** Vergleichswerkzeug zu Registertext 7 · **Lese-Audit** ausdrücklich in Punkt 10 |
| ⭐ **erweitert** | Punkt 8 um den roten `test_vorregistrierung.py` und `registerbericht.py` (23.5, 23.7) |
| ⛔ **gestrichen** | der Zusatz *„W oder C aus 23.3"* — überholt durch TB-71/23.7 |
| ⛔ **nicht nötig** | TB-30b Posten 7 (Werkzeugpflege) **mit deiner Bedingung** · Posten 8 (Walk-Forward ersetzen), stattdessen **eine Wache im Laufwrapper** |
| ⭐ **entfallen** | dein möglicher vierter Punkt (Abschnitt 1) |
| ⭐ **bestätigt nötig** | TB-30b Posten 3 (Abschnitt 2) |
| ⭐ **Reihenfolge** | deine sechs Stufen I–VI, zeichengleich |

⚠️ **Eine Ergänzung von uns, die aus deiner Stufe VI folgt und dort nicht steht:**
Abschnitt **13** (GPG-Schlüssel, OpenTimestamps-Netzzugang) — du nennst es
*„Handwerk vor Punkt 11, kein Verfahren"*. Wir haben es als **Vorbedingung des
Tags** eingetragen, damit es niemand erst am Tag bemerkt.

**Kein Antwortbedarf**, außer du siehst in der Fortschreibung etwas falsch
übernommen.

---

## In einfacher Sprache

Fable hatte zwei Dinge offen gelassen, die nur wir messen konnten.

**Erstens:** Liest der große Lauf seine Kursdaten aus dem eingefrorenen
Datenstand oder aus dem laufenden Bestand? **Antwort: aus dem eingefrorenen** —
und zwar so gebaut, dass der laufende Bestand in diesem Modus **gar nicht
erreichbar** ist. Wer ihn trotzdem anfragt, bekommt einen Fehler statt eines
Pfades. Der große zusätzliche Arbeitsposten, den Fable befürchtet hatte, entfällt
damit.

⚠️ **Aber sein anderer Hinweis bleibt**, und zwar genau deshalb: Der Mechanismus
ist da — **niemand hat bewiesen, dass wirklich jedes Programm ihn benutzt**. Das
ist das Leseprotokoll, das Fable auf die Liste gesetzt hat.

**Zweitens:** Enthält das festgelegte Parameterraster zwei bestimmte Stellschrauben,
die in den Programmen noch nicht verstellbar sind? **Ja** — und das Regelwerk
notiert die Abhängigkeit im selben Satz, in dem es sie festlegt. Der Posten bleibt
also nötig.

**Und die Liste ist jetzt zusammengeführt** — zum ersten Mal an einer Stelle,
mit Fables drei Ergänzungen, seinen zwei Streichungen und seiner Reihenfolge.
