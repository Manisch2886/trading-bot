# Vorregistrierung S-E1 — Pfadkriterien (TB-33)

**Stand: 15.09.2026. Eingefroren vor dem Lauf.**

> **Gegenstand von TB-33 ist nicht die Strategie, sondern der Weg.**
>
> Register → Backtest → Forward-Test **ohne Live-Status** →
> Bestätigungsperiode → Bericht, **ohne dass unterwegs jemand eine Wahl hat.**

Das Ergebnis der Strategie wird gelesen werden — es ist nur **nicht das,
woran dieser Test gemessen wird**. Der zweite Registereintrag,
[`VORREGISTRIERUNG_S-E1_strategiekriterien.md`](VORREGISTRIERUNG_S-E1_strategiekriterien.md),
regelt die Strategie. Dieses Dokument regelt den Weg.

> **Der Test ist bestanden, wenn der Weg sauber läuft. Er ist nicht
> bestanden, wenn an irgendeiner Stelle eine Entscheidung nötig wurde, die
> im Register nicht steht** — unabhängig davon, ob S-E1 selbst besteht oder
> durchfällt.

---

## 1. Die neun Pfadkriterien

Jedes ist **maschinell** geprüft. Ein Pfadkriterium, das nur jemand beurteilen
kann, wäre selbst eine Entscheidung ausserhalb des Registers.

| # | Kriterium | geprüft durch |
|---|---|---|
| **P1** | **Das Auswertungsskript läuft ohne menschliche Entscheidung durch** — gegen erzeugte Beispieldaten, **bevor** echte Ergebnisse existieren. Kein Prompt, keine Rückfrage, kein „hier bitte einsetzen" | `test_turn_of_month.py`, Teil A |
| **P2** | **Jede berichtete Kennzahl ist aus dem Register ableitbar.** Jede Zahl im Bericht hat einen benannten Ursprung in `register.py`; keine Zahl entsteht erst im Auswertungsskript | `test_turn_of_month.py`, Teil G (maschineller Abgleich Bericht ↔ Register) |
| **P3** | **Die Herkunftsangaben stehen in JEDER Ergebnisdatei**: Commit-Hash, Datenstand-Hash, Register-Hash — nach dem Muster aus `research/vorregistrierung/herkunft.py` | `test_turn_of_month.py`, Teil F |
| **P4** | **Der Forward-Test erzeugt KEINEN Portfolio-Eintrag.** Am **Verhalten** geprüft: der Lauf wird wirklich ausgeführt, und danach sind Bot-Liste, Crash-Knopf-Liste, Datenbanken und `results/` unverändert — nicht am Vorhandensein einer Flagge im Quelltext | `test_turn_of_month.py`, Teil D |
| **P5** | **Die Sweep-Regel greift.** Fällt der Kern durch und besteht eine Sweep-Variante, lautet das Ergebnis `DURCHGEFALLEN` — nicht „Variante übernommen" | `test_turn_of_month.py`, Teil C |
| **P6** | **Die Handelstags-Regel greift** bei Feiertagen **und** bei verkürzten Tagen | `test_turn_of_month.py`, Teil B |
| **P7** | **Wiederholbarkeit**: zweiter Lauf, gleiche Zahlen — bei festem Seed bitweise gleich | `test_turn_of_month.py`, Teil E |
| **P8** | **Nichts Verbotenes angefasst**: keine `live_params.py`, `forward_test.py`, `equity_simulation.py`, `multi_symbol_*.py`; `shared/zuteilung.py`, `shared/messkette.py`, `shared/regimewache.py` unberührt; keine `results/*.csv` überschrieben; nichts unter `broker/`, keine Crontab | Schritt 1 des Testdokuments; `shared/ergebniskurven.py` meldet weiterhin **9x AKTUELL** |
| **P9** | **Frist und Entscheidungskriterium der Staging-Ebene stehen beim Anlegen fest** — nicht danach (Abschnitt 3) | `test_turn_of_month.py`, Teil D |

---

## 2. Was ein Pfadfehler ist — und was nicht

**Ein Pfadfehler** ist jede Stelle, an der der Lauf ohne eine Festlegung
nicht weiterkonnte und die Festlegung **während** des Laufs getroffen wurde.

**Kein Pfadfehler** ist:

* dass S-E1 **durchfällt** — das ist ein Ergebnis, kein Fehler;
* dass eine Zahl unangenehm ist;
* dass eine Festlegung **vor** dem Lauf ergänzt werden musste, **solange
  sie im Register steht, bevor gerechnet wurde** und der Bericht sie als
  Ergänzung ausweist.

> Die drei Ergänzungen dieses Laufs (A1 Instrument, A2 Sweep-Zellen, A3
> Bootstrap und Mindest-Ereigniszahl) stehen in Abschnitt 0 der
> Strategiekriterien. Sie sind **vor** dem Lauf festgelegt und im
> Übergabebericht unter der Pfadfrage ausdrücklich genannt. Das ist die
> zulässige Form; die unzulässige wäre, sie erst zu bemerken, wenn die
> Zahlen schon da sind.

---

## 3. Die Staging-Ebene — Frist und Kriterium, beim Anlegen

Die Staging-Ebene (**I19**) existiert noch nicht. Gebaut wird **minimal**,
was dieser Test braucht: eine Signalerzeugung, die **läuft und
protokolliert**, aber in **keine** Portfolio-Zahl eingeht und **nicht** im
Crash-Knopf auftaucht. **Nicht** an eine Ereignis-Datenbank gekoppelt — ein
Bot mit einer Flagge genügt.

### 3.1 Wo sie liegt — und warum genau dort

`research/turn_of_month/` — **nicht** unter `strategies/`. Das ist keine
Geschmacksfrage:

* `shared/ergebniskurven.finde_bots()` zählt die Ordner unter `strategies/`
  mit einer `equity_simulation.py`. Ein Ordner dort **wäre** ein zehnter Bot,
  Flagge hin oder her.
* `notifications/manual_close.SCHLIESSBARE_BOTS` ist die Liste, aus der der
  Crash-Knopf seine Bots nimmt. Sie wird **nicht** angefasst.
* Es entsteht **keine** `paper_trading_*.db` und **kein** Eintrag unter
  `results/`.

Die Staging-Ebene ist damit nicht deshalb unsichtbar, weil eine Flagge sie
versteckt, sondern weil sie in keiner der Listen steht, aus denen
Portfolio-Zahlen und Crash-Knopf gebildet werden. **Genau das prüft P4 am
Verhalten.**

### 3.2 Die Frist

> **Bestätigungsperiode: 12 protokollierte Monatswechsel ab dem ersten
> Signal, spätestens bis zum 2027-09-30.**

Was zuerst eintritt, beendet die Periode. Eine Verlängerung ist **kein
Ermessen**, sondern ein **neuer vorregistrierter Lauf**.

### 3.3 Das Entscheidungskriterium

Nach Ablauf der Frist bekommt S-E1 ein Portfoliogewicht **nur**, wenn
**alle drei** gelten:

| | Bedingung |
|---|---|
| **S1** | **Rang 3 hat über die neun Bots entschieden.** Vorher nicht — sonst käme ein zehnter Beta-Baustein vor die Beta-Bereinigung, nur durch die Hintertür |
| **S2** | Der **Backtest** hat bestanden (B1, B2, B3 der Strategiekriterien) |
| **S3** | Die **Forward-Periode** hat mindestens **12** Ereignisse, und die **untere** Grenze ihres 95-%-Bootstrap-Intervalls der Netto-Rendite je Ereignis liegt **> 0** — dieselbe Bedingung B2, angewandt auf die Forward-Ereignisse, mit demselben Seed-Verfahren |

Trifft eines davon nicht zu, wird der Staging-Eintrag **geschlossen** und
S-E1 bleibt draussen. Es gibt kein „vorerst behalten" — dieselbe
Schattenregel wie bei den neun Bots.

### 3.4 Der Cronjob

**Wird nicht eingetragen.** Die Zeile steht als **Vorschlag** im Testdokument
und in `research/turn_of_month/README.md`; der **Betreiber** trägt sie selbst
ein. Ein Forschungslauf, der sich selbst in die Crontab schreibt, hat den
Unterschied zwischen Staging und Buch schon verloren.

---

## 4. Wie das Pfadurteil zustande kommt

Der Selbsttest gibt das Pfadurteil **maschinell** aus: `WEG SAUBER` nur dann,
wenn **alle neun** Kriterien P1 bis P9 bestanden sind. Fällt eines durch,
nennt die Ausgabe **welches** — und der Übergabebericht beginnt mit dieser
Stelle, nicht mit dem Ergebnis der Strategie.

```bash
python3 research/turn_of_month/test_turn_of_month.py
```

Rückgabewert **0** heisst: der Weg ist sauber gelaufen. **1** heisst: an
einer benannten Stelle wurde eine Entscheidung nötig, die nicht im Register
stand.

---

*Erstellt in TB-33, vor dem Lauf. Zweiter von zwei Registereinträgen.*
