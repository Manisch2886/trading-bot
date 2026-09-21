# Nachtrag 2 zur Bestandsaufnahme TB-30b — der Kern von TB-30b ist ein Erzeuger, den es noch nicht gibt

**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53) · **Nr. 3 von 3**
(Vorgänger: `NACHTRAG_1_BESTANDSAUFNAHME_TB-30b.md`)
**Abgelegt:** 21.09.2026, 23:36 Ortszeit · **HEAD zur Messzeit:** `6071f32`
(= `origin/main`; jünger als `a0c6eb0`)
**Art:** lesende Messung. ⛔ **Kein Byte geändert.** Keine Freigabe verbraucht.

> ⚠️ **Berichtigung, 21.09.2026 nach Fable 21l Punkt 3:** Der Kopf nannte zuvor
> *„Stand: 23:40"* — **geschätzt, nicht gemessen**; abgelegt wurde die Datei um
> 23:36. Herkunftszeile und HEAD-Ordnung nachgetragen. **Am Inhalt ist nichts
> geändert.**
**Bezug:** `BESTANDSAUFNAHME_TB-30b.md` Posten 6; `NACHTRAG_1…` Abschnitt 3,
letzte Zeile (*„ob das nach dieser Messung noch stimmt, ist ungeprüft"*).

⚠️ **Das ist der ernüchternde Teil des Abends** — und er gehört neben die zwei
guten Befunde, nicht hinter sie.

---

## 1. Die Frage, die Nachtrag 1 offengelassen hat

Nachtrag 1 zeigte: `auswertung.py` folgt Verfahren B und muss nicht geöffnet
werden. **Offen blieb Posten 6** — Registertext **2d** (Embargo als Bedingung am
Bestand) und **3b (a)–(e)**. Die Registertabelle (Z. 2080/2081) nennt
`auswertung.py` als Ort. ⚠️ **Stimmt das?**

---

## 2. Gemessen: `auswertung.py` rechnet die Bestätigungsperiode nicht

**Der Datenvertrag, wörtlich aus `auswertung.py` Z. 38–43:**

> ```
> <wurzel>/<bot>/zellen.csv
>     zelle_id, <je Rasterachse eine Spalte>, falte, rolle, n_trades,
>     netto_sharpe, netto_rendite_pct, kapital_drawdown_pct, mittlere_exposure
>     -> genau eine Zeile je (Zelle x Falte), fuer ALLE Falten des
>        Faltenplans, Bestaetigungsperiode eingeschlossen.
> ```

**Und die Auswertung der Bestätigungsperiode, Z. 432–435:**

```python
name = plan[bot]["bestaetigungsperiode"]
...
zeile = df[(df["zelle_id"] == zid) & (df["falte"] == name)]
```

⇒ ⭐ **`auswertung.py` liest eine fertige Zeile.** Es rechnet nichts aus Trades,
es kennt keine Positionen, es bestimmt keinen Embargo-Tag. **Wo** die
Bestätigungsperiode beginnt — an der Faltengrenze oder erst am ersten Tag ohne
offene vor-Go-Live-Position (Registertext 2d, 16.6) — entscheidet, **wer die
`zellen.csv` schreibt.**

⇒ ⚠️ **Die Tabellenzeile 2080 nennt den falschen Ort.** Die Lücke ist real, aber
sie liegt nicht in `auswertung.py`. *(Zur Vorsicht: `embargo` kommt in
`auswertung.py` **null**-mal vor — es kennt also weder das alte noch das neue
Embargo, entgegen dem Wortlaut der Zeile.)*

---

## 3. ⭐⭐ Also: wer schreibt die `zellen.csv`?

**Gemessen über alle `.py` im Repo (ohne `trading-env/`):** drei Dateien nennen
`zellen.csv`.

| Datei | Rolle |
|---|---|
| `research/vorregistrierung/auswertung.py` | **liest** sie (Z. 154) |
| `research/vorregistrierung/test_vorregistrierung.py` | **liest** sie (Prüfungen) |
| ⚠️ `research/vorregistrierung/beispieldaten.py` | ⚠️⚠️ **schreibt** sie (Z. 132) — **mit frei erfundenen Werten für den Selbsttest** |

⇒ ⚠️⚠️ **Für den echten Lauf schreibt sie niemand.**

**`beispieldaten.py` sagt es im Kopf selbst** (Z. 24–26), wörtlich:

> *„der Kapital-Drawdown einer Falte steht in `zellen.csv`, weil er **im echten Lauf aus `equity_simulation.py` kommt**"*

**Gegenprobe, gemessen an allen neun `strategies/*/equity_simulation.py`:** Jede
schreibt genau eine Ausgabe — `result["equity_curve"].to_csv(output_path)`.
⇒ ⭐ **Sie liefern den Baustein, nicht die Zelle.** Keine schreibt `zellen.csv`.

---

## 4. ⚠️⚠️ Der Befund: TB-30b trägt den Bau des Laufgerüsts

**Was zwischen den vorhandenen Teilen fehlt**, ist ein Erzeuger, der je Bot über
**Raster × Falten** läuft, Optimierer und Equity-Simulation aufruft und daraus
die **vier** Dateien des Datenvertrags schreibt:

| | verlangt vom Datenvertrag | heute |
|---|---|---|
| 1 | `<bot>/zellen.csv` — eine Zeile je (Zelle × Falte) | ⛔ nur aus `beispieldaten.py` |
| 2 | `<bot>/tagesreihen/<zelle_id>.csv` | ⛔ dito |
| 3 | `<bot>/herkunft.json` | ⭐ `herkunft.py` existiert (Sperrliste 11/12) |
| 4 | `benchmark_tagesreihen/<markt>.csv` | ⭐ `benchmark.py` existiert (Sperrliste 4/6) |

⭐⭐ **Und damit fallen drei Posten an denselben Ort:**

| Posten | gehört zu | weil |
|---|---|---|
| **2** — Kapital-Drawdown (11.2) | ⭐ **dem Erzeuger** | der Datenvertrag verlangt `kapital_drawdown_pct` als Spalte; Agent 2 schaltet von selbst um, sobald sie da ist |
| **6a** — Embargo 2d | ⭐ **dem Erzeuger** | er entscheidet, welche Trades in die Zeile der Bestätigungsperiode gehen |
| **6b** — 3b (a)–(e) | ⭐ **dem Erzeuger** | Loader entscheidet über Faltenzählung, Benchmark auf den geladenen Symbolen, Faltenkohärenz |

⇒ ⚠️⚠️ **TB-30b ist nicht „sieben Posten am vorhandenen Code", sondern zu einem
guten Teil ein neues Skript.** Das war bisher nirgends so benannt.

---

## 5. Einordnung — was das heisst und was nicht

| | |
|---|---|
| ⭐ | **Es ist keine Überraschung im Sinne von „vergessen".** Register-Abschnitt 11 heisst „**Voraussetzungen des Laufs**"; dass der Laufcode noch kommt, weiss das Register. ⚠️ **Nicht benannt war sein Umfang** |
| ⭐ | **Die Teile sind da und geprüft:** neun Optimierer, neun Equity-Simulationen, `benchmark.py`, `herkunft.py`, `shared/zuteilung.py`, `regimewache.py`, `auswertung.py` samt 150 Prüfungen. ⭐ **Es fehlt das Bindeglied, nicht das Material** |
| ⭐ | **Der Datenvertrag ist geschrieben, bevor es den Erzeuger gibt** — das ist die richtige Reihenfolge, nicht die falsche. Wer zuerst den Erzeuger schreibt und dann den Vertrag, hat die Wahl nach dem Ergebnis |
| ⭐ | **Gegenprobe gemacht, und sie schliesst die Lücke:** Gesucht wurde nach `zelle_id` in **allen** `.py` des Repos ausserhalb von `research/vorregistrierung/` (ohne `trading-env/`). ⭐⭐ **Null Treffer** — die Zellen-Bauart existiert nirgends sonst. Die 20 `research/`-Werkzeuge, die `falte` kennen, sind Messwerkzeuge (Faltenplan, MTM-Drawdown, Registerprüfungen), **keine Raster-Läufer**. ⇒ **Es gibt keinen Teilerzeuger, auf dem sich aufbauen liesse** |
| ⛔ | **Nicht gemessen:** wie gross das Skript wird und wie lange der Lauf dauert |
| ⛔ | **Keine Empfehlung, kein Zeitplan.** Das ist Sache des Betreibers |

⚠️ **Eine Folge für die Frist:** Der signierte Tag setzt voraus, dass der Lauf
starten kann. Zwischen „Register fertig" und „Lauf kann starten" liegt dieses
Skript. **Das gehört in die Kursbetrachtung**, und es war dort bisher nicht
enthalten.

---

## In einfacher Sprache

Nach den zwei guten Nachrichten die unbequeme.

Das Auswertungsskript ist fertig, richtig gebaut und muss nicht angefasst werden
— das war Nachtrag 1. **Aber:** Dieses Skript **liest** nur. Es erwartet eine
Tabelle mit einer Zeile je Parametersatz und Zeitabschnitt, und aus dieser
Tabelle berechnet es die Auswahl.

**Diese Tabelle schreibt heute niemand.** Es gibt genau ein Programm, das sie
erzeugt — und das ist das **Testprogramm mit frei erfundenen Zahlen**, damit
sich die Auswertung prüfen lässt, ohne ein echtes Ergebnis zu sehen. Für den
echten Lauf fehlt das Gegenstück.

**Alle Bausteine dafür sind da** — die neun Optimierer, die neun
Kapitalsimulationen, die Vergleichsrechnung, die Herkunftsprotokolle. Was fehlt,
ist das Programm, das sie in der richtigen Reihenfolge aufruft und die Tabelle
schreibt.

⭐ **Das ist keine schlechte Nachricht über die Arbeit, sondern eine über den
Zeitplan:** Drei der Posten, die ich vorhin als „Kleinigkeiten am vorhandenen
Code" gelistet habe, gehören in Wirklichkeit in dieses neue Programm. Und
zwischen „Regelwerk fertig" und „Lauf kann starten" liegt es ebenfalls.

⚠️ **Wie gross es wird, habe ich nicht gemessen.** Aber ich habe nachgesehen, ob
Teile davon schon in den Forschungsordnern liegen: **Nein.** Die Bauart, auf der
die Auswertung beruht, kommt in **keinem** anderen Programm des Projekts vor.
