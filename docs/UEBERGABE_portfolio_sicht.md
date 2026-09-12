# Übergabe: Echte Portfolio-Sicht im Dashboard

**Branch** `claude/new-session-uqjk8h`, Basis `origin/main` (`d5be46e`, nach
Merge von #79). **PR #80.**

Neu: `dashboard/portfolio_sicht.py`, `dashboard/static/portfolio.html`,
`dashboard/test_portfolio_sicht.py`, `dashboard/test_portfolio_anzeige.js`.
Geändert: `dashboard/app.py` (zwei Endpunkte, eine Seitenroute),
`static/app.js` (fünf Anzeigefunktionen), `static/index.html` (ein Link),
`static/style.css`, `static/sw.js`, `dashboard/test_dashboard.py`
(Positivliste), `dashboard/README.md`, `docs/UEBERGABEPROTOKOLL.md`,
`.gitignore`.

**`shared/portfolio_overview.py` ist unverändert** — nur gelesen und
aufgerufen, wie verlangt. Ein Selbsttest prüft das gegen `origin/main`.

---

## 1. Die Ehrlichkeit der Zahlen — die eigentliche Anforderung

### Was gewählt wurde

**Beides aus dem Aufgabentext, nicht eines von beiden:** je Bot eine
Quellenmarke **und** zwei getrennte Gruppenergebnisse.

| | |
|---|---|
| Je Bot | `echte Trades (25)` · `Backtest (3 von 10)` · `keine Kurve` |
| Gruppe 1 | **Nur echte Trades** — nur Bots über der Schwelle |
| Gruppe 2 | **Alle Bots (teils Backtest)** — vollständig, gekennzeichnet |

Begründung für beides zusammen: die Marke allein beantwortet nicht, *welche*
Zahl man jetzt glauben darf; zwei Zahlen allein sagen nicht, *welcher Bot* die
zweite verwässert. Erst zusammen ist die Frage „ist das echt?" ohne Rückfrage
beantwortbar.

Jede Gruppe trägt zusätzlich **einen Satz**, woraus sie besteht — bei der
Backtest-Gruppe wörtlich „das ist keine erzielte Rendite". Eine Rendite ohne
diesen Satz gibt es auf der Seite nicht; der Frontend-Test prüft genau das
(Abschnitt 6 dort: Zahl der Renditen ≤ Zahl der Herkunftssätze).

Die Marke nennt bei Backtest **auch den Abstand zur Schwelle** (`3 von 10`).
„Backtest" allein lässt offen, ob das ein Dauerzustand ist oder in sieben
Trades vorbei.

### Der Befund, der die Wortwahl entschied

`shared/portfolio_overview.py` nennt seine erste Gruppe **„LIVE-PORTFOLIO (nur
aktivierte Bots)"** — „live" heisst dort *„hat eine `live_params.py`"*, also
**aktiviert**. Alle neun Bots haben eine, und keiner erreicht bisher die
Schwelle von zehn geschlossenen Trades.

**Die „LIVE-PORTFOLIO"-Zahl der Montags-Mail stammt heute also zu 100 % aus
Backtest-Kurven.** Genau die Verwechslung, die diese Aufgabe verhindern soll —
und sie steckt schon im Bestand.

Konsequenz hier: die Gruppen heissen **nicht** „live", sondern „Nur echte
Trades" und „Alle Bots". Die Mail selbst ist unverändert (durfte nicht
angefasst werden); der Befund steht als offener Punkt 15 im Übergabeprotokoll.

### Der zweite Befund: ein Bot kann lautlos verschwinden

`load_all_curves()` fängt Lesefehler ab, gibt eine `print`-Warnung aus und
lässt den Bot **aus dem Ergebnis fallen**. Die Summe läuft dann über weniger
Bots. Im Terminal sieht man die Warnung; in einer Oberfläche wäre es ein
stiller Verlust.

Aufgefallen nicht durch Nachdenken, sondern praktisch: in dieser Cloud-Sitzung
scheiterte der Live-Subprozess von `t3_supertrend` (das Paket `binance` fehlt
hier), und der Bot war einfach weg.

`portfolio_sicht.berechne()` vergleicht deshalb `discover_bots()` mit
`load_all_curves()` und führt jeden fehlenden Bot als `quelle="fehlt"` samt
Hinweis, dass er in **keiner** Summe enthalten ist — oben auf der Seite und in
der Tabelle.

---

## 2. Ort im Dashboard: eigene Seite `/portfolio`

Nicht aus Geschmack. **Auf der Übersicht liegt der Crash-Knopf**, und die
Rechnung dauert Sekunden. Eine eigene Seite macht es *strukturell* unmöglich,
dass diese Rechnung je in den Ladepfad des Notfallwegs gerät — aus einer Frage
der Sorgfalt wird eine der Architektur. Auf der Übersicht steht nur ein Link
(vor der Bot-Tabelle, **unterhalb** des Crash-Bereichs), der nichts nachlädt.

Der Preis ist ein Tap. Dafür ist die Seite ruhig, und sie lädt und
aktualisiert sich nicht im 60-Sekunden-Takt mit.

Ein Test belegt die Trennung mit **wirklich blockierter Abhängigkeit** (ein
Finder in `sys.meta_path` lässt den Import von `portfolio_overview`
scheitern): der Rechen-Endpunkt meldet 503, während Übersichtsseite,
`/api/portfolio` und der Crash-Weg weiter antworten. Zusätzlich per AST
geprüft, dass `portfolio_sicht.py` auf Modulebene **nur** Standardbibliothek
importiert — ein fehlendes `pandas` kann das Dashboard also nicht am Start
hindern, obwohl `app.py` das Modul oben importiert.

---

## 3. Laufzeit: gemessen, dann entschieden

| Fall | Zeit |
|---|---|
| `import portfolio_overview` (kalt, wegen pandas) | **5,2 s**, einmalig je Prozess |
| `discover_bots()` | 0,2–1 ms |
| `load_all_curves()`, alle Bots auf Backtest-Kurve | **134 ms** |
| `load_all_curves()`, **7 Bots auf dem Live-Weg** | **2,9 s** (≈ 0,42 s je Bot) |
| hochgerechnet auf 9 Live-Bots | **≈ 3,8 s** |

Der Live-Weg startet je Bot einen Python-Subprozess — das ist der Mechanismus,
mit dem `portfolio_overview` die `sys.modules`-Kollision umgeht, und genau
deshalb ist er teuer.

*Messhinweis:* die Live-Datenbanken liegen (zu Recht) nicht im Repo. Für die
Messung wurden synthetische `paper_trading_<bot>.db` mit je zwölf
geschlossenen Trades angelegt, gemessen und **wieder entfernt**. Zwei Bots
(`elliott_wave`, `t3_supertrend`) liessen sich hier nicht messen, weil ihr
`equity_simulation.py` `binance` importiert; auf dem Mac ist das Paket
vorhanden.

**Entscheidung: Zwischenspeicher, und das Dashboard rechnet nie von selbst.**
`GET` liest nur; neu gerechnet wird per Knopf, per Skriptaufruf oder per
Cronjob. Das Alter steht immer dabei, über 24 Stunden als *veraltet*
gekennzeichnet.

Der Ausschlag kam aber nicht von der Laufzeit, sondern von einem
**Richtigkeitsargument**: `portfolio_overview` legt seine Zwischendateien unter
einem **festen** Namen ab (`results/portfolio_overview/_live_trades_cache.csv`).
Zwei gleichzeitige Rechnungen — Dashboard und Montags-Mail — würden sich diese
Datei gegenseitig überschreiben und wären dann beide falsch. `portfolio_sicht`
lenkt `RESULTS_DIR` für die Dauer der Rechnung auf einen eigenen Ordner um
(kein Umbau der Datei, nur ein anderer Wert von aussen) und serialisiert sich
über eine Sperrdatei mit `O_EXCL`.

---

## 4. Was sonst gezeigt wird — und was bewusst nicht

**Gezeigt:** Gesamtergebnis je Gruppe mit Herkunft · max. Drawdown je Gruppe ·
Zeitraum mit Tageszahl und dem Hinweis, dass es die **Schnittmenge** aller
Kurven ist · je Bot Quelle, Beitrag in Prozentpunkten und offene Positionen ·
offene Positionen gesamt · Rechenzeitpunkt und Alter.

Der **Drawdown** ist der einzige Zusatz, den ich vorgeschlagen habe: er kostet
nichts (wird ohnehin berechnet), ist eine Zahl je Gruppe, und er ist die einzige
Kennzahl, die eine hohe Rendite relativiert.

Der Hinweis auf die **Schnittmenge** ist keine Fussnote-Kosmetik: hat ein Bot
eine kurze Live-Historie und die anderen fünfjährige Backtest-Kurven, schrumpft
das Fenster für **alle** auf diese kurze Zeit. Ohne den Hinweis wäre unklar,
warum die Rendite plötzlich klein ist.

**Nicht gezeigt, mit Begründung:**

* **Korrelationen je Bot-Paar** — `portfolio_overview` verlangt dafür 30
  gemeinsame Handelstage und sagt sonst „zu wenig Datenbasis"; heute wäre das
  bei fast jedem Paar so. Eine 9×9-Matrix ist auf 390 px ohnehin unlesbar.
* **Eurobeträge** — die Bots führen kein Kapital je Trade. Jeder Betrag wäre
  aus Annahmen abgeleitet und wirkte echter als eine Prozentzahl (Backlog E1).
* **Tageszusammenfassung** — der nächste der drei Dashboard-Schritte, fasst
  dieselben Dateien an, bewusst getrennt.

---

## 5. Tests

| Suite | Ergebnis |
|---|---|
| `dashboard/test_portfolio_sicht.py` *(neu)* | **90 / 90** ✅ |
| davon `dashboard/test_portfolio_anzeige.js` *(neu, über node)* | **67 / 67** ✅ |
| `dashboard/test_dashboard.py` | 784 / 784 ✅ |
| `notifications/test_schliess_benachrichtigung.py` | 99 / 99 ✅ |
| `system/test_log_rotation.py` | 117 / 117 ✅ |
| `broker/test_broker.py` · `broker/test_ibkr.py` | 163 · 200 ✅ |
| `shared/test_empfehlung_format.py` · `system/test_caffeinate_plist.py` | 70 · 52 ✅ |

**Alle fünf geforderten Datenlagen** sind geprüft: alle Bots über der
Schwelle, alle darunter, gemischt (der heutige Fall), ein Bot ohne
geschlossene Trades, ein Bot ohne Datenbank — dazu der Bot, dessen Kurve
ausfällt.

Hergestellt über eine Attrappe von `portfolio_overview`; anders lassen sich
diese Lagen nicht erzeugen, weil die Live-Datenbanken nicht im Repo liegen. Die
**Rechnung** läuft dabei echt (dieselbe pandas-Logik), und Abschnitt 9 schliesst
die Lücke, die eine Attrappe offen lässt: er ruft das **echte**
`shared/portfolio_overview.py` auf und vergleicht dessen Textausgabe Zahl für
Zahl — Rendite **80,52 %**, Drawdown **−6,24 %**, Fenster
**2022-03-18 bis 2026-06-27**, alle drei identisch.

**22 Mutationsproben, alle 22 im ersten Durchlauf erkannt.** Die beiden
wiederkehrenden Fallen aus #73/#77/#78/#79 wurden vorab adressiert:

* *Zustand von Hand hergestellt:* die Endpunkt-Tests zählen die echten Aufrufe
  von `load_all_curves` (0 bei `GET`, 1 bei `POST`), statt ein Ergebnis zu
  vergleichen. Die Atomarität des Schreibens wird durch einen **abgebrochenen**
  Schreibvorgang geprüft, nicht durch „es liegt keine Nebendatei herum" — das
  allein hätte ein direktes Schreiben in die Zieldatei durchgelassen.
* *Zweite Wache verdeckt die erste:* der Notfallweg wird mit **echt
  blockiertem** Import geprüft, nicht mit einer Attrappe.

---

## 6. Drei Fehler, die die Tests gefunden haben

**Ein symmetrisches Fixture prüfte nichts.** Meine drei Testkurven hatten
Steigungen 4/5/6 %; „nur echte Trades" und „alle Bots" kommen dadurch
zwangsläufig auf denselben Mittelwert, und der Vergleich der beiden Gruppen war
wertlos. Backtest-Kurven steigen im Fixture jetzt deutlich steiler — was der
Wirklichkeit auch näher kommt.

**Der Zeitpunkt wurde als rohes `Date`-Objekt ausgegeben.** `zeitpunkt()` in
`app.js` liefert ein `Date`, nicht Text; im Template landete daraus
`Sat Sep 12 2026 09:00:00 GMT+0000 (Coordinated Universal Time)` — auf einem
deutschen iPhone gleich doppelt falsch. Gefunden beim Lesen der Testausgabe,
nicht durch eine fehlgeschlagene Zusicherung; die Prüfung auf das Format
`TT.MM., HH:MM` ist deshalb nachgezogen (Mutation M19 bewacht sie).

**Mein eigener Test veränderte das Repo.** Der Abgleichlauf in Abschnitt 9
startete `shared/portfolio_overview.py`, und dessen `main()` schreibt seine
Kurven-CSVs nach `results/portfolio_overview/` — eingecheckte Dateien. Jeder
Testlauf hinterliess eine schmutzige Arbeitskopie. Jetzt läuft dasselbe
Programm mit umgelenktem `RESULTS_DIR`.

---

## 7. Offene Punkte

* **Die Überschrift „LIVE-PORTFOLIO" in der Montags-Mail** bleibt irreführend
  (offener Punkt 15 im Protokoll). Zu ändern wäre eine Zeile in
  `portfolio_overview.py` — hier ausdrücklich nicht erlaubt.
* **Der Cronjob ist nicht eingetragen** (Punkt 16). Unkritisch: die Seite zeigt
  den letzten Stand samt Alter, der Knopf rechnet neu.
* **Kein Test gegen eine echte Live-Datenbank über der Schwelle.** Es gibt im
  Repo keine, und die synthetischen aus der Laufzeitmessung wurden bewusst
  wieder entfernt. Der Testauftrag holt das auf dem Mac nach — dort liegen die
  echten Datenbanken, und dort wird die Schwelle irgendwann überschritten.
* **Die Seite wurde nie in echtem iOS-Safari geöffnet** — wie die Punkte 8 und
  A6 im Backlog. Geprüft ist, was die Funktionen *erzeugen*, nicht wie Safari
  es darstellt.
