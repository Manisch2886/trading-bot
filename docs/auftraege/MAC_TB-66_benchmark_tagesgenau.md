# TB-66 Der Benchmark wird tagesgenau — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-66 Benchmark tagesgenau`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⚠️ **Diese Aufgabe rechnet.** Sie braucht `trading-env` und die Kursdateien.

⛔ **Sie ändert einen Registertext.** Das ist ausdrücklich freigegeben — siehe
Abschnitt 0.

---

## 0. Die Grundlage: Fables Festlegung vom 20.09.2026

**Vollständig in `docs/projektfuehrung/FABLE_ANTWORT_2026-09-20_benchmarkfenster.md`.**
Der Kern:

> **VT.** Der Benchmark einer Falte wird **tagesgenau** aus den Symbolen
> gebildet, die der Loader des Bots **an diesem Tag** handelbar macht.

⭐ **Sein Grund, und er kommt aus dem Register, nicht aus der Wirkung:**
*„Bot und Benchmark leben in derselben Menge. Die Menge, in der ein Bot lebt,
ist tagesgenau — er kann ein Symbol an keinem Tag halten, an dem sein Loader es
nicht geladen hat."*

**Zwei Folgen, die er benennt:**

| | |
|---|---|
| **1** | Unter der alten Lesart wäre der zulässige Drawdown in Falte 2018 `1,25 × −87,9 %` — **jeder Parametersatz besteht, egal was er tut** |
| **2** | Unter der alten Lesart erzeugt Rang 3 **+88 Prozentpunkte Alpha daraus, dass der Bot nichts halten konnte** |

⭐ **Einordnung nach F17: Berichtigung** — der Wortlaut wird an den Zweck
angeglichen, der im selben Registertext steht. ⚠️ **Die Wirkung ist bekannt und
geht gegen die Bots; sie wird vermerkt, sie ist nicht der Grund.**

---

## 1. Der neue Registertext 3b (c)

**Fundstelle: `docs/VORREGISTRIERUNG_neuselektion.md`, Zeile 1944**, Abschnitt
16.7, Ergänzung (c).

⭐⭐ **Der alte Wortlaut bleibt stehen und wird als ERSETZT gekennzeichnet** —
das Register ist append-only, hier gilt **nicht** `DOKUMENTATIONSSTANDARD.md`
Regel 9 (Register ist eine der vier Ausnahmen).

**Der neue Wortlaut, von Fable:**

> Der Benchmark einer Falte wird **tagesgenau** aus den Symbolen gebildet, die
> der Loader des Bots an diesem Tag handelbar macht: gleichgewichtet, täglich
> rebalanciert (Konvention; sie ist die einzige Gewichtung, die bei wechselnder
> Menge ohne weitere Regel auskommt). Tage, an denen kein Symbol handelbar ist,
> tragen Rendite 0. Derselbe Benchmark gilt für die Drawdown-Nebenbedingung
> (Abschnitt 4) und für Rang 3. Bot und Benchmark leben an jedem Tag in
> derselben Menge.

**Dazu die Berichtigungsnotiz** mit: Lesart VT · Wirkung gemessen und bekannt
(`turtle_soup_crypto` 2018: **−3,60 %** statt −87,92 % bei 100 % Exposure;
DD-Toleranz je nach Bot **2,4- bis 5,0-fach**) · Grund: der Zweck-Satz von
3b (c) · Herkunft: Fables Antwort vom 20.09.2026.

### ⚠️ Die eine Stelle, an der du NICHT einfach abschreibst

**Fable schreibt selbst dazu:** *„nur eines darf im Register stehen, und es muss
das sein, was der Code tut. Vor dem Eintrag nachsehen."*

**Nachgesehen am 20.09., `bh_tagesrenditen()`:**

```python
rahmen.pct_change().mean(axis=1, skipna=True).dropna()
```

| | |
|---|---|
| ⭐ | *„gleichgewichtet, täglich rebalanciert"* **trifft** — der Mittelwert der Tagesrenditen ist täglich rebalanciert, ein echtes Buy-and-Hold hätte driftende Gewichte |
| ⚠️ | *„Tage ohne handelbares Symbol tragen Rendite 0"* **trifft nicht** — `.dropna()` **entfernt** diese Tage |

⛔ **Entscheide das nicht selbst.** **Miss, ob es einen Zahlenunterschied
macht**, und lege beide Fassungen vor:

| | Fassung | |
|---|---|---|
| **W** | Wortlaut an den Code: *„Tage, an denen kein Symbol handelbar ist, gehen nicht in den Benchmark ein"* | keine Codeänderung |
| **C** | Code an den Wortlaut: `.dropna()` durch `.fillna(0)` ersetzen | ⚠️ ändert die berichtete `handelstage`-Zahl |

⭐ **Erwartung, zu prüfen:** Für den **Drawdown** gleichwertig (ein Tag mit 0 %
bewegt den Kapitalpfad nicht), für **`handelstage`** nicht. **Miss beides und
berichte die Differenz je Bot und Falte.** Ist sie überall null ausser bei
`handelstage`, sag das ausdrücklich.

⚠️ **Bis zur Entscheidung trägt der Registertext an dieser Stelle einen
sichtbaren Platzhalter**, keine der beiden Fassungen. *Ein Registertext, der
etwas anderes sagt als der Code, ist genau der Fehler, den TB-56b berichtigt
hat.*

---

## 2. Die Codeänderung

### 2a — `benchmark.py` auf VT

**Der Vierjahresfilter geht** — Fable: *„das Verfahren-A-Artefakt, das mit
`MINDESTTRAINING` schon einmal gegangen ist; Code an registrierte Regel,
Berichtigung."*

`point_in_time(…, rd.MINDESTTRAINING_JAHRE)` wird ersetzt durch die
tagesgenaue Menge nach dem Loader des Bots — `MIN_HISTORY_DAYS` **500** /
**730** / **1 825**, `MIN_HISTORY_HOURS` **17 520** (Kerzenzahl) je Bot, wie
Registertext 3b (b) sie führt.

⚠️ **Bei `elliott_wave` ist die Schranke eine Kerzenzahl, keine Zeitspanne.**
Geht das nicht sauber, **sag es und lass ihn aus** — ein ausgelassener Bot mit
Begründung ist besser als eine Zahl, die eine andere Grösse misst.

⛔ **Die vier Rechenfunktionen bleiben unberührt:** `drawdown_bei_exposure`,
`bh_tagesrenditen`, `erlaubt`, die Medianbildung. **Sperrliste Punkt 4 und 6.**

### 2b — Der irreführende Docstring

`bh_tagesrenditen()` heisst im Docstring *„Gleichgewichteter Buy-and-Hold"* —
**die Rechnung ist täglich rebalanciert.** ⭐ **Dieselbe Fehlerklasse wie `K1h`
und `T44.10`: ein Name, der etwas anderes verspricht als das Verhalten.**
Berichtigen, da die Datei ohnehin angefasst wird.

### 2c — Die dritte Konstantenkopie

`research/krypto_historie/faltenplan.py:65` führt `MINDESTTRAINING_JAHRE = 4`
(`K4f`). ⛔ **Nicht in dieser Aufgabe** — sie gehört zu `T56b.6`, mit eigener
Mutationsprobe. **Nur prüfen, dass sie nichts beeinflusst, was hier gerechnet
wird**, und das Ergebnis berichten.

---

## 3. Der Lauf

**Wie TB-61: daneben.**

```
trading-env/bin/python3 research/vorregistrierung/benchmark.py --ziel research/vorregistrierung/ergebnisse/benchmark_drawdowns_vt.json
```

⛔⛔ **`benchmark_drawdowns.json` bleibt byteweise unverändert.** SHA-256
`a163c49814b9af0c770dce689e8511249bb2c20011243d3aec34b4b84336d1ee`.

⚠️ **`benchmark_drawdowns_neu.json` aus TB-61 bleibt ebenfalls unverändert** —
es ist der Beleg des vorigen Laufs. **Der neue Lauf schreibt in eine dritte
Datei.**

---

## 4. Der Vergleich

**Je Bot und Exposure-Stufe 25 / 50 / 100 %:** die gesperrte Tabelle, TB-61,
und dieser Lauf — **drei Spalten nebeneinander.**

⭐ **Gegenprobe, die TB-65 vorgerechnet hat:** Für die **vier Aktien-Bots** darf
sich gegenüber TB-61 **nichts** ändern — dort waren V0 und die Loader-Fassung
auf allen 100 Stufen und in allen 40 Falten zeichengleich. ⚠️ **Weicht dort
etwas ab, ist das ein Befund und der Lauf ist nicht fertig.**

⭐ **Erwartet bei den fünf Krypto-Bots:** DD_Toleranz beim **2,4- bis
5,0-fachen** von TB-61. ⚠️ **Das ist eine Erwartung aus TB-65, keine Vorgabe** —
berichte die gemessene Zahl.

---

## 5. ⚠️ Eine Begriffsberichtigung, die Fable nebenbei angebracht hat

> *„Vor dem Tag ist es eine **Berichtigung des Registers** und ein **Bug-Fix am
> Auswerter**; **‚Amendment' gehört zur Sperrliste des Codes, nicht zum
> Register**."*

**Gemessen:** „Amendment" steht **24×** im Register und **10×** im Backlog.

⛔ **Nicht alle ändern.** ⭐ **Nur dort, wo es den Registerteil meint** — vor
allem Abschnitt **21.9** und Backlog-Zeile **`T56b.3`**, die den Vorgang
durchgehend so nennen. **Für `benchmark_drawdowns.json` (Sperrliste Punkt 4)
bleibt der Begriff richtig.**

⚠️ **Jede geänderte Stelle wird einzeln berichtet**, mit dem Satz davor und
danach. *Eine Begriffsänderung im Register ist eine Änderung am Register.*

---

## 6. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐ SHA-256 von `benchmark_drawdowns.json` — **unverändert**; und von `benchmark_drawdowns_neu.json` vor und nach der Aufgabe **gleich** |
| **3** | Registertext 3b (c): alter Wortlaut als ERSETZT markiert, neuer daneben, Berichtigungsnotiz vollständig — **null entfernte Zeilen** im Register |
| **4** | ⭐⭐ Die Messung aus Abschnitt 1: `dropna()` gegen `fillna(0)`, Differenz je Bot und Falte, getrennt für Drawdown und `handelstage` |
| **5** | ⭐ Der Dreispalten-Vergleich aus Abschnitt 4 — **mit der Gegenprobe, dass die vier Aktien-Bots unverändert sind** |
| **6** | `status` je Bot in der neuen Datei — erwartet neunmal `endgueltig` |
| **7** | Die Begriffsstellen aus Abschnitt 5, einzeln |
| **8** | ⭐ `trading-env/bin/python3 research/vorregistrierung/test_vorregistrierung.py` — **Ergebnis je Teil.** ⚠️ Der `KeyError: '2017'` bleibt, solange die gesperrte Tabelle gilt; **das ist erwartet und kein Befund** |
| **9** | `git diff --numstat` je Datei; nichts ausserhalb `research/vorregistrierung/` und `docs/` |

---

## 7. Die harten Auflagen

| | |
|---|---|
| ⛔ | **`benchmark_drawdowns.json` und `benchmark_drawdowns_neu.json` unverändert** |
| ⛔ | **Keine der vier gesperrten Rechenfunktionen anfassen** |
| ⛔ | **Die offene Formulierungsfrage aus Abschnitt 1 nicht entscheiden** — messen und vorlegen |
| ⛔ | **Im Register wird nichts entfernt** — der alte Wortlaut bleibt als ERSETZT stehen |
| ⭐ | **Sichern nach jedem fertigen Teil** |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** Er beruht auf dem Stand vom 20.09., 15:25 |

---

## 8. Was diese Aufgabe NICHT tut

| | |
|---|---|
| ⛔ | **Die Sperrlisten-Änderung vollziehen.** Eigene Betreiberfreigabe, nach dem Lauf |
| ⛔ | **Den Tag setzen** |
| ⛔ | **`T56b.6` erledigen** (die Konstantenkopien) |
| ⛔ | **Die zwei roten Tests aus TB-61 reparieren** (G6, H3) |
| ⛔ | **`docs/VORREGISTRIERUNG_S-E1_nulltest.md` ändern** — abgeschlossener Lauf, `K4f` |

---

## In einfacher Sprache

**Was entschieden ist:** Fable hat festgelegt, wie der Vergleichswert gerechnet
wird, gegen den jeder Bot gemessen wird. Ein Kurs zählt erst ab dem Tag, an dem
der Bot ihn überhaupt sehen kann — nicht rückwirkend für das ganze Jahr.

**Warum das wichtig ist:** Unter der anderen Lesart wäre die Drawdown-Regel in
den frühen Jahren wirkungslos gewesen — jeder Parametersatz hätte bestanden, egal
was er tut. Und der Bot hätte sich Gewinne anrechnen lassen, die nur daher
kamen, dass er nicht dabei war.

**Was diese Aufgabe macht:** Sie trägt Fables Text ins Register ein, stellt die
Rechnung um und lässt sie neu laufen — wieder **daneben**, die gesperrte Datei
bleibt unberührt.

**Was du danach entscheidest:** Eine einzige Formulierung. Fable hat geschrieben,
Tage ohne handelbaren Kurs sollen „Rendite 0 tragen"; der Code lässt sie
stattdessen weg. Für die Zahlen ist das gleichwertig — für die Angabe, wie viele
Handelstage eine Falte hatte, nicht. Die Aufgabe misst beides und legt es dir vor.
