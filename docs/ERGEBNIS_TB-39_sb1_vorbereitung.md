# Ergebnis TB-39 — S-B1 Vorbereitung

**Stand: 16.09.2026. Kurzfassung zum Kopieren.**

> ⚠️ **Es wurde kein Backtest gerechnet.** Keine Ertragszahl, keine
> Sharpe-Zahl, keine Parametersuche, keine Auswahl von Instrumenten nach
> ihrem Ergebnis. `S-B1` steht auf Rang 4; ihr Backtest gehört hinter Rang 1.

---

## 1. Die drei Antworten zuerst

### Reicht die Historie ab 2007 für acht Instrumente über vier Anlageklassen?

> ⚠️ **Noch nicht gemessen — und zwar aus einem benennbaren Grund, nicht aus
> Versäumnis.** yfinance und Yahoo sind aus der Cloud gesperrt; der Proxy
> antwortet mit **403** (nachgewiesen für `query1` und `query2`). Eine Zahl
> hier wäre geraten, und die Aufgabe verlangt ausdrücklich „gemessen, nicht
> geschätzt".

**Was stattdessen geliefert ist:** das Werkzeug, das die Frage beantwortet,
und ein Testdokument, das sie am Mac beantwortet.

```bash
python3 research/etf_trendfolge/historie.py
```

**Die Erwartung** (Kenntnisstand, **keine Messung** — sie steht im Register
ausschliesslich als Wache gegen ein falsch geschriebenes Symbol):

| | Kandidaten | erste, die 2008 tragen |
|---|---|---|
| Aktien | SPY, IWM, EFA, EEM | alle vier |
| Zinsen | IEF, TLT | beide |
| Kredit | LQD, HYG | LQD; **HYG erst ab März 2008** |
| Metalle | GLD, SLV | beide |
| Rohstoffe | DBC, DBA | beide |
| Währungen | FXE, FXY | FXE; **FXY erst ab Februar 2008** |

**Erwartet: 12 von 14 Instrumenten über 6 Anlageklassen am 01.01.2008** —
also deutlich über der Untergrenze von 8 über 4. **Das ist zu prüfen, nicht
zu glauben.** Der Rückgabewert von `historie.py` ist die Antwort: **0** heisst
erfüllt, **1** heisst nicht erfüllt — und 1 ist ein zulässiges Ergebnis.

⚠️ **Die Fallgrube, die hier steckt:** „Historie reicht bis 2007" und „Signal
ab 2008" sind **nicht dasselbe**. Ein ETF braucht **252 Handelstage** Vorlauf,
bevor er ein Zwölf-Monats-Signal tragen kann. Deshalb lautet die
Datenanforderung auf 2007 und die erste Selektionsfalte auf 2008.

### Wie gross ist N?

> **N = 5.**

Gezählt aus der Liste der Rasterzellen (`raster.py`), nicht aus einer Angabe
im Text.

| | |
|---|---:|
| N (dieser Lauf) | **5** |
| N_historisch (Neuselektion) | 653 |
| **N gesamt, nominal** | **658** |

**Warum nur fünf:** Die Beschreibung von `S-B1` legt fast alles fest — die
Instrumente, die drei Signalfenster (3/6/12 Monate, aus der Literatur), den
Mehrheitsentscheid, die inverse Volatilitätsgewichtung, „Kasse als Rest", die
monatliche Umschichtung. **Was sie nicht festlegt, ist genau eine Zahl:** über
welchen Rückblick die Volatilität gemessen wird. Fünf geometrische Stufen:
**42, 66, 103, 161, 252** Handelstage.

**Was es kosten würde, mehr zu rastern:**

| Fall | N |
|---|---:|
| die drei Signalfenster je vierstufig statt fest | 320 |
| alle vier denkbaren Zusatzachsen zusammen | **5 760** |

*Die drei Literaturfenster ins Raster zu stellen kostet den **Faktor 64** —
und die Herkunft „aus der Literatur" gleich mit.*

### Was bleibt nach 0,30 Prozentpunkten je Round Trip?

> **Rund 0,15 bis 0,9 Prozentpunkte im Jahr — und die Instrumentenzahl kürzt
> sich heraus.**

Die naheliegende Sorge lautet: „monatliche Umschichtung von 8 bis 14
Positionen, das sind 12 × 14 Round Trips im Jahr". Das wäre richtig, **wenn
jeden Monat das ganze Buch umgeschlagen würde**. Wird es nicht: umgeschlagen
wird nur, was sich **ändert**.

```
Jahresumschlag =  n · w · (1/n)  =  w
Jahreskosten   =  w · 0,15 Prozentpunkte
```

`w` = Kippungen je Instrument und Jahr, `n` = Instrumentenzahl. **`n` kürzt
sich heraus.**

| `w` (Kippungen je Instrument und Jahr) | Jahreskosten (Prozentpunkte) |
|---:|---:|
| 1 | 0,15 |
| 2 | 0,30 |
| 3 | 0,45 |
| 4 | 0,60 |
| 6 | 0,90 |
| **jeden Monat kippt alles** (obere Schranke) | **1,80** |
| *Massstab: ein voller Round Trip je Monat (die Hürde von `S-E1`)* | *3,60* |

**Der Vergleich mit `S-E2` geht deshalb nicht auf.** Dort war die
Kostenrechnung der Grund, die Strategie zu verwerfen — dort wurde aber das
ganze Buch je Runde umgeschlagen. Bei `S-B1` liegt die **obere Schranke** bei
der Hälfte jener Hürde, und die realistische Last bei einem Viertel bis einem
Achtel davon.

⚠️ **`w` ist eine Eigenschaft der Kursreihen und wird hier bewusst NICHT
gemessen** — das wäre der Backtest. Die Tabelle lässt die Zeile offen, die
Rang 1 später füllt.

---

## 2. Die Entscheidungen, die getroffen wurden

| Frage | Entscheidung | Grund in einem Satz |
|---|---|---|
| **Wohin die Kursdateien?** | `research/etf_trendfolge/daten/`, **gitignoriert** | Ausserhalb von `data/` ist sicher gegen Absicht; **nicht im Repo** ist auch sicher gegen Versehen bei Merge und Rebase |
| **`auto_adjust`?** | **`True`** | Vier der vierzehn Kandidaten sind Anleihe-ETFs; auf der unbereinigten Reihe wäre ihr Zwölf-Monats-Momentum **strukturell negativ** — die Strategie mied Anleihen aus einem Buchhaltungsgrund |
| **… und die Nicht-Wiederholbarkeit?** | Dateien werden **einmal geholt und eingefroren**; `--neu` vergleicht und meldet, statt zu ersetzen; jede Datei bekommt eigenen SHA-256 im `manifest.json` | „1,2 × 10⁻⁶ ist klein genug" wäre eine Behauptung; eine eingefrorene Datei mit Hash ist keine |
| **Signalfenster fest oder im Raster?** | **fest** | Im Raster wüchse N um den Faktor 64 — und die Herkunft „aus der Literatur" ginge verloren |
| **Vol-Rückblick?** | **im Raster**, 5 Stufen, Grundlage `datenfrequenz` | Die einzige Zahl, die die Strategiebeschreibung offen lässt |
| **Kasse verzinst?** | **nein** | Festlegung des Projekts vom 15.09.2026; sie ist die konservative Richtung |
| **Umschichtungstag?** | **entschieden** am letzten Handelstag des Monats (Entscheidungskerze), **ausgeführt** zur Eröffnung des ersten Handelstags des Folgemonats | Zum Entscheidungs-Schluss zu handeln hiesse, auf einen Kurs zu handeln, den man beim Entscheiden noch nicht kennt — der Vorgriff, den TB-38 beseitigt hat |
| **Benchmark?** | **Dasselbe Buch ohne Signal** — gleiche Körbe, gleiche Gewichte, gleiche Kosten, immer voll investiert | Alles ausser dem **Timing** kürzt sich heraus, und das Timing ist das Einzige, was `S-B1` hinzufügt |

---

## 3. Die Befunde

| # | Befund |
|---|---|
| **B1** | ⚠️ **Die Budgetstufen-Leiter (Schatten / Grundbudget / Bestätigt) steht nirgends im Repo.** Sie ist nach dem Vorbild der Staging-Ebene von `S-E1` ausformuliert. Weicht das von der Fassung des Betreibers ab, gilt dessen Fassung — die Passage ist dann zu **ersetzen**, nicht zu ergänzen |
| **B2** | ⚠️ **Das Embargo lässt sich vor dem Lauf nicht beziffern.** `S-B1` hat keine Zeitbremse; es gilt die zweite Hälfte von Registertext 2d (95. Perzentil der Haltedauer + 1) — und die verlangt eine Positionshistorie, die es noch nicht gibt. Registriert ist deshalb die **Regel**, nicht die Zahl: gemessen auf den Selektionsfalten des Gewinners, protokolliert **bevor** die Bestätigungsperiode geöffnet wird |
| **B3** | ⚠️ **Die Rastergrenze ruht auf `datenfrequenz`, nicht auf einer Messung.** Die Neuselektion verlangt Grenzen als Regeln über *gemessene* Grössen (§2.1). Eine Volatilitätsmessung an den ETF-Reihen **wäre** aber genau die Beobachtung vor der Registrierung, die diese Aufgabe verbietet. Offen eingetragen als Abweichung A1 |
| **B4** | ⚠️ **Bei fünf Punkten auf einer Achse sind zwei davon Kanten.** Die Kanten-Markierung ist damit von vornherein wahrscheinlich, und die Plateau-Regel hat an den Rändern nur einen Nachbarn statt zwei. Kein Fehler — aber vor dem Ergebnis zu wissen |
| **B5** | ⚠️ **Eine Festlegung fiel beim Schreiben des Werkzeugs auf** (Abweichung A4): Zählt ein ETF ohne Zwölf-Monats-Historie als „kein Signal" (also Kasse) oder als „nicht vorhanden"? Eingetragen ist **„nicht vorhanden"** — die konservative Richtung: sie schreibt der Strategie keine Kassenquote zu, die aus einem Datenmangel stammt. Derselbe Typ Lücke wie A4 bei `S-E1` |
| **B6** | ⚠️ **Die Korrelation gegen das Neuner-Buch bekommt keine Schwelle** — obwohl sie der Grund ist, aus dem `S-B1` im Katalog steht. Zwei Gründe: für die Höhe gäbe es keine Grundlage ausser Geschmack, und das Neuner-Buch selbst ist beweglich (es hängt davon ab, welche Bots Rang 1 überleben). Sie wird **berichtet, nicht bewertet** |
| **B7** | Ein Namenskonflikt wurde umgangen: `research/vorregistrierung/beispieldaten.py` und `research/etf_trendfolge/beispieldaten.py` heissen gleich. Fremde Module werden deshalb über `register.lade_fremdes_modul` mit eigenem Namensraum geladen; der fremde Ordner kommt **nicht** auf `sys.path`. Dieselbe Falle wie bei den neun gleichnamigen `equity_simulation.py` |

---

## 4. Die Nachweise

| Was | wie geprüft | Ergebnis |
|---|---|---|
| **Datenstand-Hash vor und nach der Aufgabe identisch** | Der ganze Werkzeugsatz läuft als eigener Prozess; `data/` wird vorher und nachher gehasht (Teil A) | ✅ `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`, **223** Dateien, unverändert; `git status --porcelain data/` leer |
| **Die Wache ist keine Attrappe** | An einem **nachgebauten** `data/`: eine zusätzliche Datei ändert den Hash | ✅ |
| **Der Zielordner kann nicht nach `data/` wandern** | `datenlauf.py` mit einem Ziel innerhalb `data/` → Rückgabewert 1, **und es entsteht nichts** (Teil J) | ✅ |
| **Untergrenze wird geprüft, nicht angenommen** | 8/4 → 0; **7**/4 → 1; 8/**3** → 1 — jede Bedingung mit einem Fall, in dem nur sie greift (Teil B) | ✅ |
| **Keine Wache verdeckt die andere** | Mutationsprobe: Klassen-Wache entfernt → der Fall 8/3 geht durch; Instrumenten-Wache entfernt → der Fall 7/4 geht durch (Teil G) | ✅ |
| **Entscheidungskerze-Regel im Ablauf** | Der Ablauf von `datenlauf.hole` wird beobachtet: `abrufen → entferne_unvollstaendige → nur_entscheidbar → schreiben`, mit `1d`/`aktien` (Teil C) | ✅ laufende Kerze landet nicht in der Datei, beides wird **gezählt** |
| **Auch hier verdeckt keine Wache die andere** | Jede der beiden Wachen einzeln aus einer **Kopie** entfernt, als eigener Prozess: genau ihr Fehler tritt auf, die andere fängt ihn nicht auf (Teil H) | ✅ |
| **Rasterzellen abzählbar und gezählt** | `N == len(zellen())`; eine geänderte Achse in einem **eigenen Prozess** ändert N (Teil I) | ✅ |
| **Keine Zahl steht zweimal** | Eine geänderte Kostenkonvention im Register ändert die Kostenrechnung (Teil I) | ✅ |
| **Selbsttest** | `python3 research/etf_trendfolge/test_etf_trendfolge.py` | ✅ **64/64** |

⚠️ **Was der Cloud-Test nicht kann, offen statt still:** `pandas` und
`yfinance` fehlen. Teil C beobachtet deshalb den **Ablauf** mit
austauschbarem Abruf und Spitzeln über den beiden Wachen; der Nachbau der
Wachen liegt **ausschliesslich im Testmodul** und kann nie zum
Produktionspfad werden. Der Durchlauf mit den **echten** Funktionen und
**echten** Kursdaten steht als Schritt 4 und 8 im Testdokument.

---

## 5. Was NICHT angefasst wurde

`data/` · `docs/VORREGISTRIERUNG_neuselektion.md` ·
`research/vorregistrierung/auswertung.py` · `live_params.py` ·
`forward_test.py` · `equity_simulation.py` · `multi_symbol_optimise.py` ·
`multi_symbol_walk_forward.py` · `shared/*` · `broker/*` · Crontab ·
`results/*.csv` · `strategies/*`

Bot-Dateien wurden **gelesen, nie importiert**.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Drei Dinge: **Reichen die Kursdaten weit genug zurück?** · **Wie viele
Varianten werden ausprobiert?** · **Wie viel frisst die Handelsgebühr auf?**

**Was herauskam.**

* **Kursdaten:** noch nicht messbar — die Kursanbieter sind aus der
  Cloud-Umgebung gesperrt. Das Werkzeug dafür ist gebaut und getestet;
  gemessen wird auf deinem MacBook. Nach heutigem Kenntnisstand sollten
  **zwölf von vierzehn** Körben ab Anfang 2008 verfügbar sein — nötig sind
  acht. Aber das ist eine Erwartung, keine Messung, und das steht so
  überall dabei.
* **Varianten:** **fünf**. Das ist wenig, und das ist gut so.
* **Gebühren:** grob **0,15 bis 0,9 Prozent im Jahr**, im schlimmsten
  denkbaren Fall 1,8 Prozent. Überraschend wenig — und unabhängig davon, ob
  acht oder vierzehn Körbe im Buch liegen.

**Warum das so ist.**
Bei den Gebühren steckt eine Denkfalle: Man rechnet leicht „vierzehn
Positionen mal zwölf Monate mal Gebühr" und kommt auf eine erschreckende
Zahl. Aber umgeschichtet wird nur, **was sich ändert**. Ein Korb, dessen
Trend zwei Jahre hält, wird einmal gekauft und einmal verkauft — nicht
vierundzwanzigmal.

Bei den Varianten gilt: **je mehr man durchprobiert, desto wahrscheinlicher
ist die beste davon nur Glück.** Fünf Varianten sind deshalb keine Sparsamkeit,
sondern Beweiskraft. Die drei Zeitfenster (3, 6 und 12 Monate) wurden
bewusst **nicht** durchprobiert — sie stammen aus der Fachliteratur, und wer
sie durchprobiert, kann sich hinterher nicht mehr darauf berufen.

**Was das für dich heisst.**
Zwei Dinge liegen bei dir, und beide stehen ausdrücklich so im Dokument:

1. **Der Datenlauf** auf deinem MacBook — die Anleitung dafür ist
   `docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md`. Sie fasst nichts an, was mit
   deinen laufenden Programmen zu tun hat.
2. **Die Entscheidung, falls die Kursdaten nicht reichen.** Dann heisst es
   nicht „Strategie kaputt", sondern: später anfangen oder auf einen Bereich
   verzichten — **deine Wahl**, nicht die des Programms.

Und ein dritter Punkt, den du bestätigen solltest: die **Budgetstufen-Leiter**
(erst gar kein Geld, dann wenig, dann voll) ist hier nach bestem Wissen
nachgebaut worden, weil sie nirgends im Projekt aufgeschrieben stand. Wenn
deine Fassung anders lautet, gilt deine.
