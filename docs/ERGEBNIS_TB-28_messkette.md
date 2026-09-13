# Ergebnis: Die Messkette an einer Stelle (TB-28)

**Stand: 2026-09-13** · Umsetzung der Schritte 1 und 2 aus der Empfehlung von
TB-27 (`research/tb27_kapitalsimulation/BERICHT.md`, „Der kleinste Eingriff").
Testauftrag: `docs/TESTAUFTRAG_TB-28_messkette.md`.

---

## Die Antwort zuerst

> **Meldet `shared/ergebniskurven.py` weiterhin `9x AKTUELL`?**
>
> **Nein — aber es hat das auf unverändertem `main` auch vorher nicht getan.**
> Es meldet **`9x ABWEICHEND`, Rückgabewert 1**, davor wie danach. Der
> vollständige Bericht dieses Programms ist vor und nach dieser Änderung
> **Byte für Byte derselbe** (SHA-256 der `--json`-Datei:
> `0b45a09908a3ac2c…`).
>
> Die Zusicherung dieser Aufgabe — **keine einzige Zahl ändert sich** — ist
> damit erfüllt, nur an einem anderen Nachweis als vorgesehen. Siehe unten,
> „Warum die vorgesehene Prüfung nicht greift".
>
> **Rechneten die beiden Nachrechner vorher dasselbe?**
>
> **Denselben Wert, ja — aber `shared/ergebniskurven.py::kennzahlen()`
> liefert einen anderen TYP.** Genau der Fall U10 aus TB-27 („behauptet
> identisch, wickelt zusätzlich in `float()`"), diesmal nicht unter
> `research/`, sondern in `shared/`. Auf allen neun abgelegten Kurven
> nachgemessen: Werte gleich, Typ verschieden (`float` gegen
> `numpy.float64`). **Nicht stillschweigend angeglichen** — siehe
> „Die drei Unterschiede".

---

## Was getan wurde

### 1. Die Messkette steht an einer Stelle: `shared/messkette.py`

| Rechnung | vorher | jetzt |
|---|---|---|
| `calculate_max_drawdown()` | **9×** zeichengleich in `strategies/*/equity_simulation.py` | **1×** in `shared/messkette.py`, neunmal importiert |
| Renditeformel | **9×** zeichengleich im `__main__`-Block | **1×** als `rendite_pct()`, neunmal aufgerufen |

Die neun Dateien bleiben an ihren Pfaden, mit ihren Signaturen. Es wandert
ausschliesslich der gemeinsame Rechenteil; jede Datei bekommt eine
Importzeile und verliert sieben Zeilen Rumpf.

Der Name `calculate_max_drawdown` bleibt englisch, obwohl die neueren
gemeinsamen Module deutsch benennen: über dreissig Stellen im Repo rufen sie
als Attribut des Bot-Moduls auf (`es.calculate_max_drawdown(...)`). Durch den
Import bleibt sie genau das.

### 2. Die beiden Nachrechner benutzen dieselbe Quelle

* `shared/ergebniskurven.py::kennzahlen()` — die ausgeschriebene
  Drawdown-Formel und die Renditeformel sind durch Aufrufe ersetzt.
* `shared/determinismus_lauf.py` — die Renditeformel ist durch einen Aufruf
  ersetzt. **Den Drawdown hat dieses Werkzeug nie nachgerechnet**: es liest
  ihn als Variable `max_dd` aus den `__main__`-Globalen des Bots. Diese
  unsichtbare Namensschnittstelle (TB-27, Abschnitt 4.2) bleibt, wie sie ist.

### 3. Drei verrutschte Zeilennummern repariert

`research/parameter_doku/pruefe_fundstellen.py` war auf `main` **bereits rot**
(35/38) — seit TB-26 verrutscht, ohne dass es aufgefallen wäre. Jetzt
**38/38**.

| dokumentiert (alt) | jetzt |
|---|---|
| `t3_supertrend/equity_simulation.py:66` | `:78` |
| `volatility_breakout/equity_simulation.py:160` | `:151` |
| `volatility_breakout_crypto/equity_simulation.py:176` | `:166` |

Diese Zahlen stehen an **zwei** Stellen: im Prüfwerkzeug und im
Dokublock der jeweiligen `live_params.py`. Beide sind nachgezogen — in
`live_params.py` ausschliesslich die Kommentarzeile, kein Parameter. Nur eine
Seite zu reparieren hätte einen grünen Wächter über einer falschen
Dokumentation ergeben.

---

## Warum die vorgesehene Prüfung nicht greift

Der Auftrag geht davon aus, die abgelegten Kurven seien „am 13.09. nach TB-26
erneuert" worden. **Das ist auf `main` nicht der Fall:**

| | Commit | Datum |
|---|---|---|
| Kurven zuletzt erneuert | `0d1693e` | **2026-09-12** |
| TB-26 ändert die Zuteilungskaskade in allen neun Bots | `f6d9a28` | **2026-09-13** |

TB-26 hat die Reihenfolge geändert, in der bei knappem Kapital zugeteilt wird
— und die Kurven nicht neu erzeugt. `shared/ergebniskurven.py` meldet deshalb
seit dem 13.09. **`9x ABWEICHEND`**; dieser Zustand ist **vorbestehend** und
wird durch TB-28 weder verursacht noch behoben. Ein Basislauf auf
unverändertem `main` weist ihn nach (Testauftrag, Abschnitt 1).

**Der Ersatznachweis ist strenger als der vorgesehene.** Statt „das Urteil
lautet weiterhin AKTUELL" wird gezeigt: **alle neun frisch gerechneten Kurven
sind vor und nach der Änderung SHA-256-gleich**, und der vollständige Bericht
von `ergebniskurven.py` ist byte-identisch. `9x AKTUELL` hätte nur gesagt,
dass neue und abgelegte Kurve zueinander passen; der Hash-Vergleich sagt, dass
sich in den neu gerechneten Kurven **keine einzige Stelle** bewegt hat.

| Bot | Kurve vorher/nachher (SHA-256, 16 Stellen) | Rendite | Max DD |
|---|---|---:|---:|
| `elliott_wave` | `0ac94d2a2aeb9cd4` | 67,77 % | −10,17 % |
| `elliott_wave_stocks` | `7ab94aa92332eeaf` | 419,07 % | −22,97 % |
| `rsi2_crypto` | `bce76ccd78ab1c2b` | 27,19 % | −13,94 % |
| `rsi2_mean_reversion` | `ef362dd66c514945` | 36,28 % | −19,53 % |
| `t3_supertrend` | `cacc20ffe5ae4668` | 121,70 % | −22,40 % |
| `turtle_soup_crypto` | `224d2f30371863cc` | 152,84 % | −34,85 % |
| `turtle_soup_stocks` | `f2a7bab7c446848d` | 138,15 % | −29,07 % |
| `volatility_breakout` | `fb38978a45d9207e` | 209,59 % | −22,46 % |
| `volatility_breakout_crypto` | `5902183834626c10` | 68,13 % | −16,29 % |

Je Bot ist auch die **gesamte Bildschirmausgabe** des Laufs identisch, bis auf
die Zeile mit der gemessenen Rechenzeit.

> **Offener Punkt für den Nutzer:** Die neun abgelegten
> `results/*/equity_curve.csv` beschreiben seit dem 13.09. Bots, die es so
> nicht mehr gibt. Montags-Mail, Dashboard-Portfoliosicht und praktisch jede
> Untersuchung unter `research/` lesen sie. TB-28 fasst sie **nicht** an (der
> Auftrag untersagt es ausdrücklich). Sie gehören mit
> `python3 shared/ergebniskurven.py --erzeugen` erneuert — als eigener,
> ausdrücklich freigegebener Schritt, denn dabei ändern sich ausgewiesene
> Zahlen.

---

## Die drei Unterschiede zwischen den Nachrechnern — gemeldet, nicht geglättet

`shared/determinismus_lauf.py` rechnete die Rendite **zeichengleich** nach;
dort gibt es nichts zu berichten. `shared/ergebniskurven.py::kennzahlen()`
unterscheidet sich an drei Stellen von der Bot-Fassung. Alle drei sind
nachgemessen, keine ändert einen Wert, alle drei bleiben stehen:

| # | Unterschied | Wirkung | warum er bleibt |
|---|---|---|---|
| 1 | `round(float(max_dd), 2)` statt `round(max_dd, 2)` | **gleicher Wert, anderer Typ** (`float` statt `numpy.float64`) | Der Wert geht in `--json` und in die Tabellenausgabe; `repr()` eines numpy-Werts lautet ab numpy 2 `np.float64(-10.17)`. Ihn anzugleichen wäre eine Entscheidung über die Ausgabe, keine Aufräumarbeit. **Das ist U10 aus TB-27, diesmal in `shared/`.** |
| 2 | `pd.to_numeric(df["capital_after"])` | für eine wohlgeformte Kurve **wirkungslos** | Diese Funktion liest aus einer CSV-Datei, der Bot bekommt die Kurve frisch aus der Simulation. Die Umwandlung gehört zum Einlesen, nicht zur Formel. |
| 3 | leere Kurve → `None` statt `0.0` | anderer Rückgabewert, **anderer Zweig** | Hier wird eine Datei beschrieben, die nichts enthält; dort ein Bot, der nichts verloren hat. Die Fallunterscheidung stand schon vorher an beiden Stellen verschieden. |

Nachgemessen auf allen neun abgelegten Kurven: **Rendite und Drawdown stimmen
in allen neun Fällen auf die Stelle überein.** `shared/test_messkette.py`
hält beides fest — die Gleichheit der Werte **und** den Unterschied im Typ.
Wer ihn später angleicht, soll das als Entscheidung tun.

---

## Der Befund hinter den Zeilennummern

**Es gibt eine Abhängigkeitsklasse, die bis TB-27 nirgends gelistet war:
Zeilennummern.** `research/parameter_doku/pruefe_fundstellen.py` hält
dokumentierte Fundstellen (Datei **plus Zeile**) gegen die Wirklichkeit.

Gefragt war, ob eine Dokumentationsprüfung, die auf Zeilennummern zeigt,
überhaupt haltbar ist. **Benannt, nicht entschieden:**

* Sie bricht bei **jeder** Änderung an der Zieldatei — auch bei einer, die
  nichts an der Sache ändert. Eine eingefügte Kommentarzeile genügt. TB-26 hat
  sie gebrochen, TB-28 hat sie erneut verschoben, und die nächste Änderung
  wird es wieder tun.
* Sie ist damit **strukturell** eine Prüfung, die aus dem falschen Grund rot
  wird — und dieses Projekt hat den Grundsatz, dass eine Prüfung, die ständig
  grundlos anschlägt, binnen Wochen ignoriert wird (`shared/ergebniskurven.py`
  begründet ihre eigene Zweiteilung genau damit).
* **Der Gegenbeleg gehört dazu:** sie ist nicht wirkungslos. Beim Schreiben
  der Dokublocks waren zwei von zwanzig Angaben bereits falsch — gefunden nur
  durch sie. Und sie ist einer der wenigen Wächter des Repos, die ohne
  `pandas` laufen.
* Der naheliegende Ausweg wäre, auf **Namen** statt auf Zeilen zu zeigen
  („`compute_btc_regime` wird in `equity_simulation.py` ohne Argumente
  aufgerufen"). Das Werkzeug sucht den Namen beim Fehlschlag ohnehin schon.
  Ob das die Aussage verwässert — eine Datei kann denselben Namen mehrfach
  nennen —, ist eine Abwägung, die dem Nutzer gehört.

**Nicht Gegenstand dieser Aufgabe; hier nur benannt.**

---

## Was ausdrücklich NICHT geschah

* **Kein Mass wurde gewechselt.** Schritt 3 der TB-27-Empfehlung — welches
  Mass führt und ob die 9 + 6 + 3 *auswählenden* Stellen mitwandern — ist
  nicht Teil dieser Aufgabe und nicht angefasst.
* **Kein `multi_symbol_optimise.py`, kein `multi_symbol_walk_forward.py`,
  kein `optimise_*.py`.** Dort entsteht der `robustness_score`, nach dem
  Parameter gewählt werden.
* **Keine `results/*/equity_curve.csv` neu erzeugt.**
* **Keine `forward_test.py`**, nichts unter `broker/`, keine Symboldatei,
  keine Crontab, keine launchd-Vorlage, `shared/zuteilung.py` unberührt.
* **Keine `live_params.py`** — mit **einer benannten Ausnahme**: in drei
  Dateien wurde je **eine Kommentarzeile** mit einer verrutschten
  Zeilennummer richtiggestellt (Punkt 3 des Auftrags verlangt die Reparatur;
  die Zahl steht dort und im Prüfwerkzeug). Kein Handelsparameter berührt;
  der Diff besteht aus drei geänderten Ziffernfolgen in Kommentaren.

---

## Prüfstand

| Prüfung | `main` vorher | nachher |
|---|---|---|
| `shared/ergebniskurven.py` | 9x ABWEICHEND, RC 1 | **9x ABWEICHEND, RC 1 — Bericht byte-identisch** |
| `shared/determinismus.py --schnell` | 9x DETERMINISTISCH, RC 0 | **9x DETERMINISTISCH, RC 0 — Bericht identisch** |
| `research/parameter_doku/pruefe_fundstellen.py` | **35/38, RC 1** | **38/38, RC 0** |
| `research/tb27_kapitalsimulation/vergleich.py --pruefen` | UNVERÄNDERT, RC 0 | UNVERÄNDERT, RC 0 (Grundzustand nachgezogen) |
| `research/tb27_kapitalsimulation/test_vergleich.py` | 23/23 | 23/23 (zwei Proben umgestellt) |
| `shared/test_messkette.py` | — | **93/93 (neu)** |
| `shared/test_ergebniskurven.py` | 44/44 | 44/44 |
| `shared/test_determinismus.py` | 54/54 | 54/54 |
| `shared/test_zuteilung.py` | 65 + 2 ausgelassen | 65 + 2 ausgelassen |
| `notifications/test_manual_close.py` | 118/118 | 118/118 |
| `dashboard/test_dashboard.py` | 784/784 | 784/784 |
