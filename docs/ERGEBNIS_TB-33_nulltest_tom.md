# Ergebnis TB-33 — Nulltest S-E1 Turn-of-Month

**Stand: 15.09.2026.** Zum Kopieren.

---

## 1. Die Pfadfrage zuerst

> **Ist der Weg sauber gelaufen — und wenn nein, an welcher Stelle wurde eine
> Entscheidung nötig, die nicht im Register stand?**

**Ja, mit einem benannten Befund.** Alle neun Pfadkriterien P1–P9 bestehen
maschinell (`110/110`, Ausgabe `WEG SAUBER`). An **vier** Stellen musste
etwas festgelegt werden, das im TB-30a-Register nicht stand — **alle vier vor
dem Lauf**, keine einzige während.

| | Was fehlte | wer hat es gesetzt | wann |
|---|---|---|---|
| **A1** | Instrument: SPY statt des `sp500_top150`-Universums (TB-30a §4.1) | Auftraggeber, Aufgabenstellung | vor dem ersten Commit |
| **A2** | Sweep-Zellen: −2/+3, −1/+2, −1/+4 + QQQ/IWM/EFA statt „2 bis 6 Tage" (TB-30a §5.1) | Auftraggeber, Aufgabenstellung | vor dem ersten Commit |
| **A3** | Bootstrap-Verfahren und Mindest-Ereigniszahl — in TB-30a gar nicht geregelt | dieser Lauf | vor dem ersten Commit |
| **A4** | **Faltenzuordnung**: zu welchem Jahr gehört ein Wechsel Dezember→Januar? | dieser Lauf | beim Schreiben der Auswertung, **vor jeder Rechnung** |

> **A4 ist der eigentliche Befund.** Er ist klein und harmlos — und genau die
> Art Lücke, um derentwillen S-E1 gerechnet wird: eine Festlegung, die
> niemand vermisst, bis ein Skript sie braucht. Bei `S-B1` mit neun Bots und
> 2 416 Zellen wäre sie nicht aufgefallen, sondern stillschweigend im Code
> getroffen worden.

**Nicht bestanden ist der Weg nicht** — Pfadkriterium §2 der
Pfadkriterien lässt Ergänzungen ausdrücklich zu, **solange sie im Register
stehen, bevor gerechnet wurde**. Das ist hier bei allen vier der Fall.

---

## 2. Ergebnis der Strategie

> ⚠️ **Es gibt noch keines.** Der Datenlauf konnte nicht stattfinden:
> yfinance ist aus der Arbeitsumgebung nicht erreichbar (der Proxy antwortet
> mit **403**), `scipy` und die Zeitzone `US/Eastern` fehlen ebenfalls.

Die Auswertung wurde deshalb — wie in der Aufgabenstellung vorgesehen —
**gegen erzeugte Beispieldaten** geführt. Das ist dieselbe Zusicherung wie in
TB-30a: *das Auswertungsskript hat seinen Test bestanden, als es noch nichts
zu deuten gab.*

**Die Zahlen aus den Beispieldaten sagen nichts über SPY.** Sie sagen nur,
dass die Maschinerie in allen sechs geprüften Lagen das tut, was das Register
verlangt:

| Lage (erzeugte Kurse) | B1 | B2 | B3 | Urteil |
|---|:--:|:--:|:--:|---|
| Effekt deutlich vorhanden | ✓ | ✓ | ✓ | `BESTANDEN` |
| Kein Effekt (Fenster wie jeder Tag) | ✗ | ✗ | ✓ | `DURCHGEFALLEN` |
| Nur der Falten-Median fällt | ✗ | ✓ | ✓ | `DURCHGEFALLEN` |
| Nur das Bootstrap-Intervall fällt | ✓ | ✗ | ✓ | `DURCHGEFALLEN` |
| Nur das Perzentil fällt (reines Beta) | ✓ | ✓ | ✗ | `DURCHGEFALLEN` |
| Kern fällt, Sweep −2/+3 bestünde | ✗ | ✗ | ✗ | `DURCHGEFALLEN` |

**Der echte Lauf ist ein Schritt für den Mac** (Schritt 6 des Testdokuments):

```bash
python3 research/turn_of_month/datenlauf.py
python3 research/turn_of_month/auswertung.py \
    --json research/turn_of_month/ergebnisse/lauf.json --protokollieren
```

---

## 3. Was geprüft wurde

| Zusicherung | Ergebnis |
|---|---|
| Auswertung läuft **ohne menschliche Entscheidung** gegen Beispieldaten durch | ✓ `stdin` geschlossen, `input(` nirgends im Quelltext |
| **Sweep-Regel greift**: Kern fällt, −2/+3 bestünde → `DURCHGEFALLEN` | ✓ und strukturell: `urteil()` nimmt **nur** den Kern entgegen |
| **Staging geht in keine Portfolio-Zahl ein** — am Verhalten | ✓ Lauf ausgeführt; Bot-Liste, Crash-Knopf, Datenbanken, `results/` unverändert |
| **Handelstags-Regel** bei Feiertagen und verkürzten Tagen | ✓ 31.12. als Feiertag verschiebt „−1"; Halbtage zählen als volle Tage |
| **Wiederholbarkeit**: zweiter Lauf, gleiche Zahlen | ✓ bitweise, bei festem Seed aus dem Register |
| **Mutationsproben** (beide Fallen) | ✓ 11 Mutationen plus unveränderter Vergleichslauf, je eigener Prozess auf denselben Daten |
| Alle bestehenden Tests bestehen weiterhin | ✓ 38 grün / 7 vorbestehend rot (identisch zum Basislauf auf `main`) |
| `shared/ergebniskurven.py` | ✓ **9x AKTUELL** |

---

## 4. N-Buchführung

| Register | Beitrag | Begründung |
|---|---|---|
| **Versuchsregister** | **1 Eintrag** — bleibt vorerst unter „vorgemerkt" | *Ein Versuch ohne Wahl ist trotzdem ein Versuch.* Gebucht wird er, wenn eine Ergebnisdatei ihn belegt — *das Register ist ein Kassenbuch* |
| **DSR** | **kein Beitrag** | Multiplizität entsteht, wo unter Alternativen gewählt wird. Hier ist **N = 1** |
| **Sweep-Zellen** | in **keines** von beiden | Robustheit, nicht Auswahl — solange die Sweep-Regel gilt |

---

## 5. Was **nicht** angefasst wurde

`live_params.py` · `forward_test.py` · `equity_simulation.py` ·
`multi_symbol_optimise.py` · `multi_symbol_walk_forward.py` ·
`shared/zuteilung.py` · `shared/messkette.py` · `shared/regimewache.py` ·
`results/*.csv` · `broker/` · Crontab · launchd ·
`docs/VORREGISTRIERUNG_neuselektion.md` ·
`research/vorregistrierung/auswertung.py`

Der Cronjob der Staging-Ebene ist **nicht eingetragen** — die Zeile steht als
Vorschlag in `research/turn_of_month/README.md` und im Testdokument.
