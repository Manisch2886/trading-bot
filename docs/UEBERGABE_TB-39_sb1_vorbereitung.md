# Übergabe TB-39 — S-B1 Vorbereitung

**Stand: 16.09.2026. Branch `claude/new-session-s2jhcc`, Base `main`
(frisch aufgesetzt auf `90262a8`, TB-38/PR #111 — geprüft, enthalten).**

---

## Die drei Antworten, wie verlangt

### 1. Reicht die Historie ab 2007 für acht Instrumente über vier Anlageklassen?

> ⚠️ **Nicht gemessen — weil es aus der Cloud nicht messbar ist.** yfinance
> und Yahoo antworten mit **403** (nachgewiesen für `query1` und `query2`).
> Die Aufgabe verlangt „gemessen, nicht geschätzt"; eine Zahl an dieser Stelle
> wäre geraten.
>
> **Geliefert ist stattdessen, was die Aufgabe ebenfalls verlangt:** das
> Werkzeug (`research/etf_trendfolge/historie.py`) und ein Testdokument, das
> die Messung am Mac durchführt. Der Rückgabewert ist die Antwort: **0** =
> erfüllt, **1** = nicht erfüllt, und 1 ist ein zulässiges Ergebnis.

**Die Erwartung, ausdrücklich als solche:** 12 von 14 Instrumenten über alle 6
Anlageklassen am 01.01.2008 — `HYG` (März 2008) und `FXY` (Februar 2008)
kommen wenige Wochen später dazu. Das läge deutlich über der Untergrenze von
8 über 4. **Diese Erwartung steht im Register ausschliesslich als Wache**:
weicht das gemessene Datum ab, meldet `historie.py` das, und die **Messung**
gilt. Ein Tippfehler im Ticker liefert sonst eine gültige, aber falsche Reihe.

⚠️ **Die Unterscheidung, an der die Frage hängt:** „Historie reicht bis 2007"
und „Signal ab 2008" sind **nicht dasselbe**. Ein Instrument braucht **252
Handelstage** Vorlauf, bevor es ein Zwölf-Monats-Signal tragen kann. Deshalb
lautet die Datenanforderung auf **2007** und die erste Selektionsfalte auf
**2008** — und deshalb ist `HYG` mit Auflage April 2007 erst ab März 2008
dabei.

### 2. Wie gross ist N?

> **N = 5.** Gezählt aus der Zellenliste, nicht abgetippt.
> **N gesamt, nominal: 658** (653 der Neuselektion **plus** 5).

Die einzige Rasterachse ist der **Volatilitäts-Rückblick**: 42, 66, 103, 161,
252 Handelstage — geometrisch, Faktor 1,565, Grundlage `datenfrequenz`
(„vom Doppelten des Umschichtungsabstands bis zum längsten Signalfenster";
der Satz nennt keine Zahl, die Werte stehen im getrennten Feld).

**Alles andere ist fest**, und die drei Signalfenster ausdrücklich: im Raster
wüchse N um den **Faktor 64** (auf 320) — und die Herkunft „aus der
Literatur" ginge verloren. Eine gewählte Fensterlänge ist keine übernommene
mehr.

### 3. Was bleibt nach 0,30 Prozentpunkten je Round Trip?

> **Rund 0,15 bis 0,9 Prozentpunkte im Jahr. Obere Schranke 1,80.**
> Und: **die Instrumentenzahl kürzt sich heraus.**

```
Jahresumschlag =  n · w · (1/n)  =  w
Jahreskosten   =  w · 0,15 Prozentpunkte     (w = Kippungen je Instrument und Jahr)
```

| `w` | 1 | 2 | 3 | 4 | 6 | alles kippt monatlich |
|---|---:|---:|---:|---:|---:|---:|
| **Prozentpunkte p. a.** | 0,15 | 0,30 | 0,45 | 0,60 | 0,90 | **1,80** |

**Der Vergleich mit `S-E2` geht nicht auf.** Dort wurde je Runde das **ganze
Buch** umgeschlagen; bei `S-B1` nur der Teil, dessen Signal kippt. Zum
Massstab: die Hürde von `S-E1` (ein voller Round Trip je Monat) liegt bei
**3,60** Prozentpunkten — doppelt so hoch wie die **obere Schranke** von
`S-B1`.

⚠️ `w` ist eine Eigenschaft der Kursreihen. Es wird hier **bewusst nicht
gemessen** — das wäre der Backtest, und der gehört hinter Rang 1. Die Tabelle
lässt die Zeile offen.

---

## Was entstanden ist

| Datei | was |
|---|---|
| `docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md` | **Das Register.** Eigenes Dokument, **nicht** in `VORREGISTRIERUNG_neuselektion.md` |
| `docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md` | Der Mac-Lauf: Datenabruf und Messung, autonom ausführbar, 12 Schritte |
| `docs/ERGEBNIS_TB-39_sb1_vorbereitung.md` | Das Ergebnisdokument zum Kopieren |
| `docs/UEBERGABE_TB-39_sb1_vorbereitung.md` | dieses Dokument |
| `research/etf_trendfolge/register.py` | Die eingefrorenen Festlegungen als Code — **jede Zahl genau einmal** |
| `research/etf_trendfolge/raster.py` | Raster; N wird **gezählt** |
| `research/etf_trendfolge/kosten.py` | Die Kostenrechnung, ohne Kursdaten |
| `research/etf_trendfolge/historie.py` | **Misst** die Historie, prüft die Untergrenze, Rückgabewert 1 |
| `research/etf_trendfolge/datenlauf.py` | yfinance-Abruf (**nur am Mac**) |
| `research/etf_trendfolge/datenstand.py` | Die Wache über `data/` |
| `research/etf_trendfolge/beispieldaten.py` | Erzeugte Beispieldaten |
| `research/etf_trendfolge/test_etf_trendfolge.py` | Selbsttest, **64/64** |
| `research/etf_trendfolge/README.md` | Kurzanleitung |
| `research/etf_trendfolge/ergebnisse/*.json` | Raster, Kosten, Datenstand — erzeugt, nicht abgetippt |

**Reine Standardbibliothek** ausser `datenlauf.py`. Dasselbe Werkzeug läuft in
der Cloud und am Mac.

---

## Die Entscheidungen, die zu treffen waren

| Frage der Aufgabenstellung | Entscheidung | Grund |
|---|---|---|
| **Wohin mit den ETF-Kursdateien?** | `research/etf_trendfolge/daten/`, **gitignoriert** | Ausserhalb von `data/` ist sicher gegen Absicht. **Nicht im Repo** ist zusätzlich sicher gegen Versehen: was nicht mitgeführt wird, kann bei keinem Merge, keinem Rebase und keinem Aufräumen nach `data/` wandern. Vorbild: `research/turn_of_month/daten/` (TB-33) |
| **`auto_adjust` — und die Folge benennen** | **`True`** | **Vier der vierzehn Kandidaten sind Anleihe-ETFs** (IEF, TLT, LQD, HYG). Sie schütten ihren gesamten Ertrag aus; ihr Kurs allein hat keinen Aufwärtstrend. Ein Zwölf-Monats-Momentum auf der unbereinigten Reihe von HYG wäre **strukturell negativ** — die Strategie wäre in Anleihen fast dauerhaft in der Kasse, aus einem Buchhaltungsgrund. Und die Verzerrung träfe die Klassen **ungleich**: sie bevorzugte genau das Aktien-Übergewicht, das `S-B1` vermeiden soll |
| **… und die 1,2 × 10⁻⁶?** | **Einfrieren statt Abschätzen** | „Klein genug" wäre eine Behauptung. Stattdessen: einmal holen, nie überschreiben; `--neu` **vergleicht und meldet**; jede Datei mit eigenem SHA-256 im `manifest.json`. Eine eingefrorene Datei mit Hash ist keine Behauptung |
| **Signalfenster fest oder im Raster?** | **fest** | N × 64 und der Verlust der Literaturherkunft |
| **Gewichtung — welcher Rückblick?** | **Im Raster**, 5 geometrische Stufen | Die einzige Zahl, die die Strategiebeschreibung offen lässt |
| **Kasse verzinst?** | **nein** | Festlegung des Projekts vom 15.09.2026, hier unverändert übernommen. Sie ist die konservative Richtung: eine Verzinsung schriebe Ertrag gut, den die Strategie nicht erwirtschaftet |
| **Umschichtung — an welchem Tag?** | **Entschieden** auf der Entscheidungskerze des letzten Handelstags des Monats, **ausgeführt** zur Eröffnung des ersten Handelstags des Folgemonats | Zum Schluss des Entscheidungstags zu handeln hiesse, auf einen Kurs zu handeln, den man beim Entscheiden nicht kennt — genau der Vorgriff, den TB-38 für die neun Bots beseitigt hat |
| **Gegen was wird gemessen?** | **Dasselbe Buch ohne Signal** | Gleiche Körbe, gleiche inverse Volatilitätsgewichte, gleiche monatliche Umschichtung, gleiche Kosten — nur immer voll investiert. Alles ausser dem **Timing** kürzt sich heraus, und das Timing ist das Einzige, was `S-B1` hinzufügt. Drei weitere Vergleiche (60/40, SPY, Neuner-Buch) sind **Bilder ohne Weg ins Urteil** |

---

## Die Befunde — sieben, davon zwei mit Entscheidungsbedarf

| # | Befund | wer entscheidet |
|---|---|---|
| **B1** | ⚠️ Die **Budgetstufen-Leiter** (Schatten / Grundbudget / Bestätigt) steht **nirgends im Repo**. Sie ist nach dem Vorbild der Staging-Ebene von `S-E1` ausformuliert | **Betreiber.** Weicht seine Fassung ab, ist Abschnitt 8 des Registers zu **ersetzen** |
| **B2** | ⚠️ Das **Embargo** lässt sich vor dem Lauf nicht beziffern: `S-B1` hat keine Zeitbremse, und die Ersatzregel (P95 der Haltedauer + 1) verlangt eine Positionshistorie, die es nicht gibt. Registriert ist die **Regel**, gemessen wird auf den Selektionsfalten des Gewinners — **vor** dem Öffnen der Bestätigungsperiode | eingetragen als A2 |
| **B3** | ⚠️ Die Rastergrenze ruht auf **`datenfrequenz`**, nicht auf einer Messung. Die Neuselektion verlangt in §2.1 Grenzen als Regeln über *gemessene* Grössen — eine Volatilitätsmessung an den ETF-Reihen **wäre** aber die verbotene Beobachtung vor der Registrierung | eingetragen als A1 |
| **B4** | ⚠️ Bei **fünf** Punkten auf **einer** Achse sind zwei davon **Kanten**; die Plateau-Regel hat an den Rändern nur einen Nachbarn. Die Kanten-Markierung ist damit von vornherein wahrscheinlich | zur Kenntnis, **vor** dem Ergebnis |
| **B5** | ⚠️ **Eine Festlegung fiel beim Schreiben des Werkzeugs auf:** Zählt ein ETF ohne Zwölf-Monats-Historie als „kein Signal" (Kasse) oder als „nicht vorhanden"? Eingetragen: **„nicht vorhanden"**, die konservative Richtung — sie schreibt der Strategie keine Kassenquote zu, die aus einem Datenmangel stammt. **Derselbe Typ Lücke wie A4 bei `S-E1`** | eingetragen als A4 |
| **B6** | ⚠️ Die **Korrelation gegen das Neuner-Buch** bekommt **keine Schwelle**, obwohl sie der Grund ist, aus dem `S-B1` im Katalog steht. Für die Höhe gäbe es keine Grundlage ausser Geschmack — und das Neuner-Buch ist selbst beweglich, weil noch offen ist, welche Bots Rang 1 überleben. **Berichtet, nicht bewertet** | zur Kenntnis |
| **B7** | Namenskonflikt umgangen: `research/vorregistrierung/beispieldaten.py` heisst wie das hiesige. Fremde Module werden über `register.lade_fremdes_modul` mit eigenem Namensraum geladen, der fremde Ordner kommt **nicht** auf `sys.path`. Dieselbe Falle wie bei den neun gleichnamigen `equity_simulation.py` | erledigt |

---

## Die Tests

**`python3 research/etf_trendfolge/test_etf_trendfolge.py` → 64/64.**

| Teil | prüft |
|---|---|
| **A** | Datenstand-Hash vor und nach dem Lauf **identisch** — am Verhalten, mit dem ganzen Werkzeugsatz als eigenem Prozess. Dazu: die Wache reagiert überhaupt (nachgebautes `data/`) |
| **B** | Untergrenze **geprüft, nicht angenommen**: 8/4 → 0, **7**/4 → 1, 8/**3** → 1, jede Bedingung mit einem Fall, in dem nur sie greift. Der Vorlauf wird **abgezählt** |
| **C** | Entscheidungskerze im **Ablauf**: `abrufen → entferne_unvollstaendige → nur_entscheidbar → schreiben`, mit `1d`/`aktien`; die laufende Kerze landet nicht in der Datei; beides wird **gezählt** |
| **D** | N ist die **Länge der Zellenliste**; der Grenzsatz enthält keine Zahl; die Nachbarschaft ist ± eine Stufe in genau einer Dimension |
| **E** | Kosten monoton; obere Schranke = 12 volle Umschläge; **8 und 14 Instrumente kosten dasselbe** |
| **F** | Das Register ist in sich schlüssig — 15 Prüfungen, darunter: genau **ein** Benchmark hat einen Weg ins Urteil, und es ist nicht Buy-and-Hold |
| **G** | **Mutationsprobe:** Klassen-Wache entfernt → 8/3 geht durch; Instrumenten-Wache entfernt → 7/4 geht durch. **Keine verdeckt die andere.** Plus Gegenprobe ohne Mutation |
| **H** | **Mutationsprobe:** jede der beiden Datenwachen einzeln aus einer **Kopie** entfernt, als eigener Prozess — genau ihr Fehler tritt auf, die andere fängt ihn nicht auf |
| **I** | **Mutationsprobe:** eine geänderte Achse ändert N; eine geänderte Kostenkonvention ändert die Kostenrechnung. Keine Zahl steht zweimal |
| **J** | **Mutationsprobe:** Zielordner innerhalb `data/` → Rückgabewert 1, **und es entsteht nichts**; `data/` unverändert |

**Die zwei benannten Fallen sind berücksichtigt:** kein Test biegt eine
Variable im laufenden Prozess um und fragt sie dann ab — jede Probe kopiert
den Ordner, ändert **eine** Stelle und startet einen **eigenen Prozess**; und
jede Probe zeigt zuerst, dass sie ohne Mutation das Richtige sieht.

> ⚠️ **Was der Cloud-Test nicht kann, offen statt still:** `pandas` und
> `yfinance` fehlen, Yahoo ist gesperrt. Teil C beobachtet deshalb den
> **Ablauf** mit austauschbarem Abruf und Spitzeln über den beiden Wachen;
> der stdlib-Nachbau der Wachen liegt **ausschliesslich im Testmodul** und
> kann nie zum Produktionspfad werden. Der Durchlauf mit den **echten**
> Funktionen steht als Schritt 4 und 8 im Testdokument.

**Bestehende Tests:** unberührt. Bekannt rot und TB-39-fremd sind
`shared/test_drawdown_beide_masse.py` (Zeitüberschreitung),
`shared/test_kursdaten.py`, `shared/test_stabile_sortierung.py`,
`shared/test_wellenauswahl.py`, `dashboard/test_portfolio_sicht.py`,
`research/exposure_messung/test_exposure_kern.py`; ohne `node` meldet
`dashboard/test_dashboard.py` 780/780 statt 784.

---

## Was NICHT angefasst wurde

`data/` (Hash **und** Dateizahl unverändert, `git status --porcelain data/`
leer) · `docs/VORREGISTRIERUNG_neuselektion.md` ·
`research/vorregistrierung/auswertung.py` · `live_params.py` ·
`forward_test.py` · `equity_simulation.py` · `multi_symbol_optimise.py` ·
`multi_symbol_walk_forward.py` · `shared/entscheidungskerze.py`,
`umstellungstag.py`, `abrufschutz.py`, `kursdaten_neuaufbau.py`,
`zeitabdeckung.py`, `binance_historie.py`, `fetch_binance_data.py`,
`zuteilung.py`, `messkette.py`, `regimewache.py` (**benutzt**, nicht
geändert) · `broker/*` · Crontab · `results/*.csv` · `strategies/*`

Bot-Dateien wurden **gelesen, nie importiert**. Ein neuer Bot unter
`strategies/` ist **nicht** entstanden — `S-B1` ist ein Kandidat, kein Bot.

---

## Der nächste Schritt

1. **Register lesen und einfrieren** (`docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md`).
   Die zwei Stellen mit Entscheidungsbedarf sind **B1** (Budgetstufen-Leiter)
   und die Bestätigung von **A3** (Benchmark).
2. **`docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md` am Mac ausführen.** Das
   beantwortet Frage 1 — gemessen.
3. **Danach: Rang 1.** Der Backtest von `S-B1` beginnt erst, wenn die
   Selektion über die neun Bots auf dem reparierten Mass entschieden hat.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Ob sich eine zehnte Handelsstrategie bauen lässt, die etwas **anderes** tut
als deine neun heutigen Programme — und nach welchen Regeln das geprüft
werden soll. Die Regeln mussten **vorher** feststehen, sonst sind sie
hinterher wertlos.

**Was herauskam.**
Die Regeln stehen, aufgeschrieben und eingefroren. Dazu acht kleine
Hilfsprogramme und ein Selbsttest, der 64 Prüfungen besteht. Drei Zahlen:

* **Wie viele Varianten werden ausprobiert? Fünf.** Wenig ist hier gut.
* **Was kosten die Handelsgebühren? Ungefähr 0,15 bis 0,9 Prozent im Jahr**,
  schlimmstenfalls 1,8. Weniger, als man denkt.
* **Reichen die Kursdaten zurück bis 2007? Noch offen** — das lässt sich aus
  der Cloud nicht nachsehen, weil die Kursanbieter dort gesperrt sind.

Gerechnet, wie gut die Strategie **wäre**, wurde bewusst **nichts**.

**Warum das so ist.**
Drei Gründe, jeder für sich:

* **Reihenfolge.** Diese Strategie steht auf Platz vier einer Warteschlange.
  Vor ihr steht das Aufräumen bei den neun heutigen Programmen. Wer jetzt
  schon rechnet, hat ein Ergebnis im Kopf, wenn er später die Regeln
  festlegt — und merkt es selbst nicht.
* **Gebühren.** Die naheliegende Rechnung „vierzehn Positionen mal zwölf
  Monate" ist falsch, weil nur umgeschichtet wird, **was sich ändert**.
* **Kursdaten.** Die Cloud-Umgebung darf die Kursanbieter nicht erreichen.
  Deshalb gibt es hier ein Werkzeug statt einer Zahl — und eine Anleitung für
  dein MacBook.

**Was das für dich heisst.**
Drei Dinge, in dieser Reihenfolge:

1. **Anleitung ausführen** (`docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md`,
   rund 15 Minuten). Sie holt die Kursdaten und beantwortet die offene Frage.
   Sie verändert **nichts** an deinen laufenden Programmen.
2. **Zwei Dinge bestätigen oder korrigieren.** Die **Budgetstufen-Leiter**
   (erst gar kein Geld, dann wenig, dann voll) stand nirgends im Projekt
   aufgeschrieben und wurde hier nach bestem Wissen nachgebaut — wenn deine
   Fassung anders lautet, gilt deine. Und der **Vergleichsmassstab**: gemessen
   wird gegen „dieselben Wertpapierkörbe, aber ohne Ein- und Ausstiegssignal,
   also dauernd investiert". Gegen einen reinen Aktienindex zu messen, wäre
   sinnlos gewesen — die Strategie soll ja gerade etwas anderes tun.
3. **Nicht ungeduldig werden.** Wenn der Datenlauf meldet, die Kursdaten
   reichen nicht für acht Körbe aus vier Bereichen, ist nichts kaputt. Dann
   entscheidest **du**, ob später angefangen wird oder ob ein Bereich
   wegfällt. Das Programm entscheidet das ausdrücklich nicht — und die
   Strategie **gar nicht zu bauen** ist ein erlaubtes Ergebnis.
