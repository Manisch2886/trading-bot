# Übergabe TB-28 — Die Messkette an einer Stelle

> **`shared/ergebniskurven.py` meldet NICHT `9x AKTUELL` — es meldet `9x
> ABWEICHEND`, Rückgabewert 1, und hat das auf unverändertem `main` vor dieser
> Änderung genauso getan; der vollständige Bericht des Programms ist vorher und
> nachher Byte für Byte derselbe.**

**Rechneten die beiden Nachrechner vorher dasselbe?** Denselben **Wert** ja,
aber `shared/ergebniskurven.py::kennzahlen()` gibt einen anderen **Typ**
zurück (`float` statt `numpy.float64`) — genau der Fall U10 aus TB-27,
diesmal in `shared/` statt unter `research/`. Auf allen neun abgelegten
Kurven nachgemessen. **Nicht stillschweigend angeglichen.**
`shared/determinismus_lauf.py` rechnete nur die **Rendite** nach, und die
zeichengleich; den Drawdown hat es nie nachgerechnet, es liest ihn als
Variable `max_dd` aus den `__main__`-Globalen des Bots.

**Stand: 2026-09-13.** Umsetzung der Schritte 1 und 2 aus der Empfehlung von
TB-27 (`research/tb27_kapitalsimulation/BERICHT.md`, „Der kleinste Eingriff").
Schritt 3 — welches Mass führt — ist ausdrücklich **nicht** Teil dieser
Aufgabe und wurde nicht angefasst.

Kurzfassung zum Kopieren: `docs/ERGEBNIS_TB-28_messkette.md`.
Testauftrag: `docs/TESTAUFTRAG_TB-28_messkette.md`.

---

## 1. Warum die vorgesehene Prüfung nicht greift — und was an ihre Stelle tritt

Der Auftrag geht davon aus, die abgelegten Kurven seien „am 13.09. nach TB-26
erneuert" worden. **Auf `main` trifft das nicht zu:**

| | Commit | Datum |
|---|---|---|
| `results/*/equity_curve.csv` zuletzt erneuert | `0d1693e` | **2026-09-12** |
| TB-26 ändert die Zuteilungskaskade in allen neun Bots | `f6d9a28` | **2026-09-13** |

TB-26 hat geändert, **wer** bei knappem Kapital den Platz bekommt, und die
Kurven nicht neu erzeugt. Seither meldet `shared/ergebniskurven.py`
`9x ABWEICHEND`. Das ist **vorbestehend**, mit einem Basislauf auf
unverändertem `main` nachgewiesen (Testauftrag, Abschnitt 0), und wird von
TB-28 weder verursacht noch behoben — der Auftrag untersagt es ausdrücklich,
die Kurven neu zu erzeugen.

**Der Ersatznachweis ist strenger als der vorgesehene:**

1. Der vollständige Bericht von `ergebniskurven.py` ist vorher und nachher
   identisch — die `--json`-Datei hat denselben SHA-256
   (`0b45a09908a3ac2c83d5db512b18c63804fbd211c1dce30fc7fc1ad87c0c4ea8`).
2. Die **neun frisch gerechneten Kurven** sind vorher und nachher
   SHA-256-gleich, Datei für Datei.
3. Auch die gesamte Bildschirmausgabe jedes der neun Läufe ist identisch —
   bis auf die Zeile mit der gemessenen Rechenzeit.
4. `shared/determinismus.py --schnell` liefert denselben Bericht: neunmal
   `DETERMINISTISCH`, gleiche Renditen, gleiche Drawdowns, Rückgabewert 0.

`9x AKTUELL` hätte nur gesagt, dass neue und abgelegte Kurve zueinander
passen. Der Hash-Vergleich sagt, dass sich in den **neu gerechneten** Kurven
keine einzige Stelle bewegt hat.

> **Offener Punkt, der dem Nutzer gehört.** Die neun abgelegten Kurven
> beschreiben seit dem 13.09. Bots, die es so nicht mehr gibt. Montags-Mail,
> Dashboard-Portfoliosicht und praktisch jede Untersuchung unter `research/`
> lesen sie. Sie gehören mit `python3 shared/ergebniskurven.py --erzeugen`
> erneuert — als eigener, ausdrücklich freigegebener Schritt, denn dabei
> ändern sich ausgewiesene Zahlen.

---

## 2. Was jetzt wo steht

`shared/messkette.py` — neu, nach dem Muster von `shared/zuteilung.py`:

| Rechnung | vorher | jetzt |
|---|---|---|
| `calculate_max_drawdown()` | **9×** zeichengleich in `strategies/*/equity_simulation.py` | **1×**, neunmal importiert |
| Renditeformel | **9×** zeichengleich im `__main__`-Block | **1×** als `rendite_pct()` |

Die neun Dateien bleiben an ihren Pfaden, mit ihren Signaturen. Je Datei eine
Importzeile mehr, sieben Zeilen Rumpf weniger.

**Zwei Entwurfsentscheidungen, die die Zusicherung tragen:**

* **`rendite_pct()` rundet nicht.** Die drei Verbraucher runden heute
  verschieden: die neun `__main__`-Blöcke formatieren nur (`:.2f`), die
  beiden Nachrechner in `shared/` runden auf zwei Stellen. Rundete die
  gemeinsame Funktion selbst, müsste einer von ihnen sein heutiges Verhalten
  aufgeben — und die Zusicherung wäre dahin. Die Formel gehört ins gemeinsame
  Modul, die Darstellung zum Verbraucher.
* **`calculate_max_drawdown()` rundet dagegen weiterhin selbst.** Weil sie das
  heute tut: ihr Rückgabewert ist an über dreissig Stellen im Repo die Zahl,
  die ausgewiesen wird. Wer den ungerundeten Tiefstwert braucht — und
  `ergebniskurven.py` braucht ihn, weil es dort anders gerundet wird —, nimmt
  `max_drawdown_ungerundet()`.

**Der englische Name bleibt**, obwohl die neueren gemeinsamen Module deutsch
benennen: über dreissig Stellen rufen ihn als Attribut des Bot-Moduls auf
(`es.calculate_max_drawdown(...)`, `globalen["calculate_max_drawdown"](...)`).
Durch den Import bleibt er genau das, und keine dieser Stellen muss angefasst
werden.

---

## 3. Die drei Unterschiede zwischen den Nachrechnern — gemeldet, nicht geglättet

| # | Unterschied in `kennzahlen()` | Wirkung | warum er bleibt |
|---|---|---|---|
| 1 | `round(float(max_dd), 2)` statt `round(max_dd, 2)` | **gleicher Wert, anderer Typ** | Der Wert geht in `--json` und in die Tabellenausgabe; `repr()` eines numpy-Werts lautet ab numpy 2 `np.float64(-10.17)`. Ihn anzugleichen wäre eine Entscheidung über die Ausgabe. |
| 2 | `pd.to_numeric(df["capital_after"])` | für eine wohlgeformte Kurve **wirkungslos** | Diese Funktion liest aus einer CSV-Datei, der Bot bekommt die Kurve frisch aus der Simulation. Gehört zum Einlesen, nicht zur Formel. |
| 3 | leere Kurve → `None` statt `0.0` | anderer Rückgabewert, **anderer Zweig** | Hier wird eine leere Datei beschrieben, dort ein Bot, der nichts verloren hat. |

Nachgemessen auf allen neun abgelegten Kurven: Rendite und Drawdown stimmen
in allen neun Fällen auf die Stelle überein. `shared/test_messkette.py` hält
beides fest — die Gleichheit der Werte **und** den Unterschied im Typ. Wer
ihn später angleicht, soll das als Entscheidung tun und nicht aus Versehen.

---

## 4. Die drei Zeilennummern — und der Befund dahinter

`research/parameter_doku/pruefe_fundstellen.py` war auf `main` **bereits rot**
(35/38). Jetzt **38/38**:

| dokumentiert (alt) | jetzt |
|---|---|
| `t3_supertrend/equity_simulation.py:66` | `:78` |
| `volatility_breakout/equity_simulation.py:160` | `:151` |
| `volatility_breakout_crypto/equity_simulation.py:176` | `:166` |

Diese Zahlen stehen an **zwei** Stellen: im Prüfwerkzeug und im Dokublock der
jeweiligen `live_params.py`. Beide sind nachgezogen.

> **Abweichung vom „Nicht anfassen" des Auftrags, hier ausdrücklich benannt.**
> Der Auftrag sagt „keine `live_params.py`" und verlangt zugleich in Punkt 3,
> die verrutschten Zeilennummern zu reparieren. Beides zusammen geht nicht:
> die Zahl steht in `live_params.py`, das Prüfwerkzeug hält sie nur dagegen.
> Nur das Werkzeug zu reparieren hätte einen **grünen Wächter über einer
> falschen Dokumentation** ergeben — schlimmer als der rote Zustand vorher.
> Geändert wurde deshalb in jeder der drei Dateien **genau eine
> Kommentarzeile**; kein Handelsparameter ist berührt, und der Diff besteht
> aus drei geänderten Ziffernfolgen (Testauftrag, Abschnitt 6, prüft das
> maschinell).

**Der Befund dahinter — benannt, nicht entschieden:** Es gibt eine
Abhängigkeitsklasse, die bis TB-27 nirgends gelistet war: **Zeilennummern**.

* Sie bricht bei **jeder** Änderung an der Zieldatei, auch bei einer, die
  nichts an der Sache ändert; eine eingefügte Kommentarzeile genügt. TB-26 hat
  sie gebrochen, TB-28 hat sie erneut verschoben, die nächste Änderung wird es
  wieder tun.
* Damit ist sie strukturell eine Prüfung, die aus dem falschen Grund rot wird
  — und dieses Projekt hält ausdrücklich fest, dass eine ständig grundlos
  anschlagende Prüfung binnen Wochen ignoriert wird.
* **Der Gegenbeleg gehört dazu:** wirkungslos ist sie nicht. Beim Schreiben
  der Dokublocks waren zwei von zwanzig Angaben bereits falsch — gefunden nur
  durch sie. Und sie ist einer der wenigen Wächter, die ohne `pandas` laufen.
* Der naheliegende Ausweg wäre, auf **Namen** statt auf Zeilen zu zeigen; das
  Werkzeug sucht den Namen beim Fehlschlag ohnehin schon. Ob das die Aussage
  verwässert — eine Datei kann denselben Namen mehrfach nennen —, ist eine
  Abwägung, die dem Nutzer gehört.

---

## 5. Der Wächter aus TB-27 hat angeschlagen — wie vorgesehen

`research/tb27_kapitalsimulation/vergleich.py --pruefen` meldete
`FUNKTION FEHLT calculate_max_drawdown`. Der Grundzustand ist nachgezogen:

| | vorher | nachher |
|---|---|---|
| `ERWARTUNG` | fünf Einträge, darunter `calculate_max_drawdown` über alle neun | vier Einträge; der Eintrag ist mit Begründung entfallen |
| Probe „stille Divergenz" | `capital_series.cummax()` → `.expanding().max()` | Positionslimit still fallen lassen, in `simulate_portfolio` |
| Probe „harmloser Kommentar" | im Rumpf von `calculate_max_drawdown` | im Rumpf von `simulate_portfolio` |
| Selbsttest-Prüfung 1 | „steht als **eine** Gruppe da" | „wird in keiner der neun Dateien mehr **definiert**" |

**Und hier ist einer der beiden gesuchten Fallstricke tatsächlich
eingetreten.** Die Probe aus TB-27 verfälschte bis heute die Zeile
`capital_series.cummax()` in einer Kopie der neun Dateien. Diese Zeile ist
durch TB-28 aus den neun Dateien verschwunden — die Verfälschung hätte ab
sofort **ins Leere gegriffen und der Test wäre grün geblieben**, ohne noch
etwas zu prüfen. Aufgefallen ist es **nur**, weil jene Probe den Ablauf
beobachtet: `pruefe("die Verfaelschung greift ueberhaupt", verfaelscht !=
text)`. Das ist genau die Falle, vor der der Auftrag warnt, live vorgeführt.

Daraus folgt der Bau des neuen Tests (Abschnitt 6).

---

## 6. Der neue Test: `shared/test_messkette.py`, 93 Prüfungen

**Der Kern ist eine Mutationsprobe:** wird `shared/messkette.py` verfälscht,
muss **jeder** der neun Bots verfälscht mitrechnen. Ein Bot, der still eine
eigene Kopie behalten hätte, fällt durch.

Zwei Bauregeln, beide aus den genannten Fallen:

* **Jede Probe belegt beide Richtungen.** Ohne Mutation muss sie den echten
  Wert sehen, mit Mutation die Marke. Bliebe eine Richtung ungeprüft, könnte
  die Probe stumm sein, ohne dass es auffällt — siehe Abschnitt 5.
* **Keine zweite Wache.** Jede Bot-Probe läuft im **eigenen Unterprozess** mit
  **einer** Frage, und die Zusicherung „es ist eine Stelle" stützt sich
  **nicht** auf den Quelltext: kein `grep` auf `from messkette import`, kein
  AST-Vergleich. Ein Quelltext-Beleg bliebe grün, auch wenn der Import
  wirkungslos wäre. Geprüft wird ausschliesslich, welche Zahl herauskommt.

Der Testauftrag führt in Abschnitt 2.1 vor, wie man die Probe **scheitern**
sieht: baut man einem Bot seine eigene — zeichengleiche und damit korrekt
rechnende — Kopie zurück, meldet der Test rot und nennt genau diesen einen
Bot. Geprüft wird nicht „rechnet es richtig", sondern „steht es an einer
Stelle".

Dazu die drei tragenden Abhängigkeiten aus TB-27, alle am Verhalten:

* **Signaturabfrage** (zwölf Stellen im Repo): `inspect.signature` und
  `co_varnames` sagen für alle neun dasselbe, und genau **ein** Bot hat kein
  `max_concurrent_positions` — `elliott_wave`.
* **Der schreibende Weg**: `notifications/manual_close.py::allokation()`
  liefert für alle neun einen Anteil, und für `elliott_wave`,
  `elliott_wave_stocks`, `t3_supertrend` weiterhin aus
  `equity_simulation.py` — deren `live_params.py` führt den Wert nicht, es
  gibt dort keinen Rückfallweg, und die Zahl steht im Bestätigungsdialog des
  Dashboards.
* **Die Bot-Liste über die Dateiexistenz**: neun `equity_simulation.py` an
  ihren Pfaden, keine nach `shared/` gewandert.

---

## 7. Prüfstand

| Prüfung | `main` vorher | nachher |
|---|---|---|
| `shared/ergebniskurven.py` | 9x ABWEICHEND, RC 1 | **9x ABWEICHEND, RC 1 — Bericht byte-identisch** |
| `shared/determinismus.py --schnell` | 9x DETERMINISTISCH, RC 0 | **9x DETERMINISTISCH, RC 0 — Bericht identisch** |
| `research/parameter_doku/pruefe_fundstellen.py` | **35/38, RC 1** | **38/38, RC 0** |
| `research/tb27_kapitalsimulation/vergleich.py --pruefen` | UNVERÄNDERT, RC 0 | UNVERÄNDERT, RC 0 |
| `research/tb27_kapitalsimulation/test_vergleich.py` | 23/23 | 23/23 |
| `shared/test_messkette.py` | — | **93/93 (neu)** |
| `shared/test_ergebniskurven.py` | 44/44 | 44/44 |
| `shared/test_determinismus.py` | 54/54 | 54/54 |
| `shared/test_zuteilung.py` | 65, 0 fehlgeschlagen, 2 ausgelassen | 65, 0 fehlgeschlagen, 2 ausgelassen |
| `notifications/test_manual_close.py` | 118/118 | 118/118 |
| `dashboard/test_dashboard.py` | 784/784 | 784/784 |

Die beiden Auslassungen in `test_zuteilung.py` betreffen `elliott_wave` und
`t3_supertrend` und kommen davon, dass `shared/fetch_binance_data.py`
gitignored ist; auf dem Rechner des Nutzers liegt die Datei und sie laufen
mit. In dieser Umgebung waren `pandas`, `numpy`, `binance`, `yfinance`,
`scipy` und `fastapi` nachzuinstallieren; `node` war vorhanden, deshalb
784/784 statt 780/780.

---

## 8. Scope-Grenzen

**Geändert:** `shared/messkette.py` (neu), `shared/test_messkette.py` (neu),
die neun `strategies/*/equity_simulation.py`, `shared/ergebniskurven.py`,
`shared/determinismus_lauf.py`, `research/tb27_kapitalsimulation/vergleich.py`
und `test_vergleich.py`, `research/parameter_doku/pruefe_fundstellen.py`, drei
Kommentarzeilen in `live_params.py`, Dokumentation.

**Nicht angefasst:** `shared/zuteilung.py`, `forward_test.py`,
`multi_symbol_optimise.py`, `multi_symbol_walk_forward.py`, `optimise_*.py`,
`results/*/equity_curve.csv`, alles unter `broker/`, Symboldateien, Crontab,
launchd-Vorlagen, Bot-Datenbanken.

**Nicht entschieden:** welches Mass führt (Schritt 3 der TB-27-Empfehlung),
ob die 9 + 6 + 3 *auswählenden* Stellen mitwandern, ob der Typunterschied in
`kennzahlen()` angeglichen wird, ob eine Dokumentationsprüfung auf
Zeilennummern haltbar ist, und wann die abgelegten Kurven erneuert werden.
Alles fünf gehört dem Nutzer.
