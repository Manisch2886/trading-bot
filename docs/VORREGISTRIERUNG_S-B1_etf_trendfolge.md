# Vorregistrierung S-B1 — Multi-Asset-ETF-Trendfolge (TB-39)

**Stand: 16.09.2026. Eingefroren vor jeder Rechnung.**

> ⚠️ **Hier wurde nichts gerechnet.** Dieses Dokument legt fest, was gerechnet
> werden **wird** — nicht, was herausgekommen ist. Kein Backtest, keine
> Ertragszahl, keine Sharpe-Zahl, keine Parametersuche, keine Auswahl von
> Instrumenten nach ihrem Ergebnis.
>
> Der Grund ist nicht Ordnungsliebe. `S-B1` steht auf **Rang 4** der
> Reparaturkette; ihr Backtest gehört **hinter Rang 1** — die Selektion auf
> dem reparierten Mass. Jede Zahl, die vor der Registrierung gerechnet würde,
> wäre eine Beobachtung, von der hinterher niemand belegen könnte, dass sie
> die Festlegung nicht beeinflusst hat.

Dieses Dokument ist **nicht** Teil von
[`VORREGISTRIERUNG_neuselektion.md`](VORREGISTRIERUNG_neuselektion.md). Jenes
ist das Register des **Neuselektionslaufs** und wird gerade verankert; es
bleibt von TB-39 unberührt. `S-B1` bekommt ein eigenes Dokument — und ein
eigenes N.

Es folgt dem Muster von Abschnitt 15 der Neuselektion (TB-36) und übernimmt
die dort am 15.09.2026 getroffenen Festlegungen sinngemäss. Wo es davon
abweicht, steht die Abweichung **offen, nicht still** — Abschnitt 0.

**Herkunft der Zahlen.** Jede Zahl dieses Dokuments steht genau einmal, und
zwar in `research/etf_trendfolge/register.py`. Sie wird hier zitiert, nicht
geführt. Die abgeleiteten Grössen erzeugen:

| | |
|---|---|
| Raster, Zellenzahl N | `research/etf_trendfolge/raster.py` → `ergebnisse/raster.json` |
| Kostenrechnung | `research/etf_trendfolge/kosten.py` → `ergebnisse/kosten.json` |
| Historie und Untergrenze | `research/etf_trendfolge/historie.py` (**braucht den Mac-Lauf**) |
| Wache über `data/` | `research/etf_trendfolge/datenstand.py` → `ergebnisse/datenstand_vorher.json` |
| Selbsttest, inkl. Mutationsproben | `research/etf_trendfolge/test_etf_trendfolge.py` |
| Datenstand | `d9449faf51bffaaa…`, **223** Kursdateien — **unverändert** |

---

## 0. Die Abweichungen von der Neuselektion — offen, nicht still

| # | Neuselektion sagt | S-B1 setzt | Grund |
|---|---|---|---|
| **A1** | Rastergrenzen sind Regeln über **gemessene** Grössen (Volatilität, Haltedauer) — §2.1/2.2 | Die einzige Rastergrenze ruht auf `datenfrequenz`, **nicht** auf einer Messung an den Kursreihen | Eine Volatilitätsmessung an den ETF-Reihen **wäre** eine Beobachtung vor der Registrierung — genau das, was diese Aufgabe verbietet. Die Frequenzen der Strategie (monatliche Umschichtung, längstes Signalfenster) sind dagegen aus ihrer eigenen Beschreibung bekannt und brauchen keine Kursdaten |
| **A2** | Embargo = längste Zeitbremse + 1, ersatzweise P95 der Haltedauer + 1 (Registertext 2d) | Dieselbe Regel, aber die **Zahl steht nicht im Register** — sie wird auf den Selektionsfalten des Gewinners gemessen und protokolliert, **bevor** die Bestätigungsperiode geöffnet wird | `S-B1` hat keine Zeitbremse und keine Positionshistorie. Eine hier eingetragene Zahl wäre geraten. Die Regel ist eingefroren, ihr Wert ist ein Messergebnis |
| **A3** | Benchmark: gleichgewichtetes point-in-time-Universum des Bots (§7c, §10 Nr. 6) | Benchmark: **dasselbe Buch ohne Signal** (Abschnitt 6) | Eine Multi-Asset-Trendfolge gegen Aktien-Buy-and-Hold zu messen, sagt nichts — sie soll ja gerade etwas anderes tun |
| **A4** | — (nicht geregelt) | Ein Instrument tritt ins Universum ein, sobald es **252 abgeschlossene Handelstage** hinter sich hat; vorher fehlt es, es steht nicht mit Gewicht 0 da | Fiel beim Schreiben von `historie.py` auf, **vor** jeder Rechnung. Ohne diese Festlegung hätte das Skript an genau einer Stelle eine Wahl gehabt: zählt ein ETF ohne Zwölf-Monats-Historie als „kein Signal" (also Kasse) oder als „nicht vorhanden"? Die gewählte Richtung ist die konservative — sie schreibt der Strategie keine Kassenquote zu, die aus einem Datenmangel stammt |
| **A5** | Budgetstufen-Leiter (Schatten / Grundbudget / Bestätigt) | dieselbe Leiter, **sinngemäss** — Abschnitt 8 | ⚠️ **Befund:** Die Leiter steht nirgends im Repo. Sie wird hier nach dem Vorbild der Staging-Ebene von `S-E1` (`VORREGISTRIERUNG_S-E1_pfadkriterien.md`, Abschnitt 3) ausformuliert. Weicht das von der Fassung des Betreibers ab, gilt dessen Fassung — und diese Passage ist zu ersetzen, nicht zu ergänzen |

> **A4 ist der Befund dieses Vorlaufs**, genauso wie A4 der Befund des
> Nulltests `S-E1` war: eine Festlegung, die niemand vermisst, bis ein Skript
> sie braucht. Sie ist klein, sie ist harmlos — und sie wäre im Code
> getroffen worden, wenn niemand vorher hingesehen hätte.

---

## 1. Was `S-B1` ist — und warum sie und kein zehnter Bot

`S-B1` ist die Multi-Asset-ETF-Trendfolge: **14 Kandidaten** über Aktien,
Zinsen, Kredit, Metalle, Rohstoffe und Währungen · **3/6/12-Monats-
Mehrheitssignal** · **inverse Volatilitätsgewichtung** · **Kasse als Rest** ·
**monatliche** Umschichtung.

| | |
|---|---|
| **Die einzige nicht-Beta-Quelle im Katalog** | Gemessen (`research/exposure_messung/`): mittlere Paarkorrelation der neun Bots **+0,112**, `turtle_soup_stocks` gegen Aktien-Buy-and-Hold **+0,82**, mittlere Brutto-Exposure **37,91 %**, an **keinem** von 1 618 Tagen flach |
| **Die einzige Horizontergänzung** | Sie arbeitet **monatlich** — ausserhalb aller neun heutigen Mediane (3,9 bis 21 Tage). Sechs von neun halten 3,9 bis 7,0 Tage; über 30 Tage ist das Portfolio leer |
| **Untergrenze** | **Acht Instrumente über mindestens vier Anlageklassen.** Darunter degeneriert sie zu Aktien-Timing mit Beiwerk — dann wird sie **nicht gebaut**, und das ist ein zulässiges Ergebnis |
| **Enthält** | `S-A2` (Inverse-ETF) als **Modul**, nicht als eigener Bot. TB-39 legt dafür nichts fest: das Modul kommt frühestens mit dem Backtest, und was vorher darüber entschieden würde, wäre eine Festlegung ohne Anlass |

---

## 2. Die Kandidatenliste

14 Kandidaten über **sechs** Anlageklassen. Die Liste steht in
`register.KANDIDATEN` und ist damit hashbar; sie ist Teil der Sperrliste
(Abschnitt 9).

| Anlageklasse | Symbole |
|---|---|
| Aktien | `SPY` (US-Standardwerte), `IWM` (US-Nebenwerte), `EFA` (entwickelte Märkte ausser USA), `EEM` (Schwellenländer) |
| Zinsen | `IEF` (US-Staatsanleihen 7–10 J), `TLT` (US-Staatsanleihen 20+ J) |
| Kredit | `LQD` (Unternehmensanleihen guter Bonität), `HYG` (Hochzinsanleihen) |
| Metalle | `GLD` (Gold), `SLV` (Silber) |
| Rohstoffe | `DBC` (breiter Rohstoffkorb), `DBA` (Agrarrohstoffe) |
| Währungen | `FXE` (Euro), `FXY` (japanischer Yen) |

### 2.1 Registertext 1 — Universum

> **(a)** Das Universum ist die Liste in `register.KANDIDATEN`. Sie wird vor
> dem Lauf eingefroren; ihr Hash geht in den Register-Hash ein.
>
> **(b)** Ein Instrument ist ab dem Umschichtungstag im Universum, an dem es
> **`VORLAUF_TAGE` abgeschlossene Handelstage** hinter sich hat
> (`VORLAUF_TAGE` = längstes Signalfenster bzw. längster Vol-Rückblick,
> gerechnet, nicht getippt: **252**). Vorher **fehlt** es; die inversen
> Volatilitätsgewichte werden über die anwesenden Instrumente normiert. Ein
> fehlendes Instrument erzeugt **keine** Kasse.
>
> **(c)** Die **Zahl der Instrumente und der Anlageklassen je Selektionsfalte**
> wird vor dem Lauf gemessen (`historie.py`) und als Tatsachennotiz
> eingetragen.
>
> **(d)** Ein Wechsel auf ein point-in-time-Universum (also eine Liste, die
> auch aufgelöste ETFs enthält) ist eine **Strategieänderung und ein neuer
> registrierter Lauf mit eigenem N**. Er ist **kein Amendment** dieses Laufs.

### 2.2 Registertext 2 — der Survivorship-Vorbehalt, wörtlich

> „Die Kandidatenliste ist **heute** zusammengestellt, also mit dem Wissen,
> welche ETFs es heute noch gibt. Aufgelöste und verschmolzene Fonds sind
> darin nicht enthalten. **Erwartete Richtung: Bevorzugung von Anlageklassen,
> deren Produkte die Finanzkrise überlebt haben** — also der breiten, liquiden
> Körbe gegenüber engen Nischenprodukten, und damit eine **zu günstige**
> Einschätzung der Diversifikationsbreite, die `S-B1` im Jahr 2008
> tatsächlich hätte herstellen können; Grösse unbekannt. Die
> Bestätigungsperiode unterliegt dieser Verzerrung nicht."

*Dieselbe Form wie Registertext 3c der Neuselektion, mit vorhergesagter
Richtung. Der Unterschied zum Aktienuniversum ist einer des Grades, nicht der
Art: ein ETF wird nicht wegen schlechter Wertentwicklung geschlossen, sondern
wegen zu geringen Volumens — die Verzerrung trifft deshalb weniger die
Rendite als die **Breite**.*

### 2.3 Die harte Frage — und warum sie hier offen steht

**Für welche dieser ETFs reicht die Historie tatsächlich bis 2007 zurück?**

Der Zeitraum ist nicht beliebig gewählt: er muss die **Finanzkrise 2008**
enthalten, sonst hat eine Trendfolgestrategie nie einen echten Bärenmarkt
gesehen. Viele ETFs sind jünger.

> ⚠️ **Diese Frage lässt sich aus der Cloud nicht beantworten.** Binance und
> yfinance sind gesperrt (der Proxy antwortet mit 403, nachgewiesen für
> `query1` und `query2`). TB-39 liefert deshalb **das Werkzeug**
> (`historie.py`) und ein **Testdokument**; gemessen wird am Mac.
>
> Was `register.KANDIDATEN` als `erwartete_auflage` führt, ist
> **ausdrücklich keine Messung.** Es ist eine Wache: weicht das gemessene
> erste Datum ab, meldet `historie.py` das, und **die Messung gilt**. Ein
> Tippfehler im Ticker liefert sonst eine gültige, aber falsche Reihe.

**Drei Daten, die nicht dasselbe sind** — und deren Verwechslung die ganze
Frage falsch beantwortet:

| | |
|---|---|
| **erstes Datum** | die erste Kerze der Reihe |
| **Signal ab** | das Datum der 252. Kerze. Vorher gibt es kein Zwölf-Monats-Fenster, also kein Signal — rund **zwölf Monate nach** der Auflage |
| **im Universum** | ab dem ersten Umschichtungstag nach „Signal ab" |

Genau deshalb lautet die Datenanforderung auf **2007** und die erste
Selektionsfalte auf **2008**.

> ⚠️ **Falls die Untergrenze nicht erfüllbar ist:** Das ist ein **Befund**,
> kein Grund für einen Rückzieher auf einen kürzeren Zeitraum. Ob stattdessen
> ein späterer Start oder ein Verzicht auf einzelne Anlageklassen richtig
> ist, entscheidet der **Betreiber**. `historie.py` meldet dann
> **Rückgabewert 1** und nennt getrennt, welche der beiden Bedingungen
> gefallen ist.

---

## 3. Die Daten

| | |
|---|---|
| **Quelle** | yfinance, dieselbe Quelle wie die vier Aktien-Bots |
| **Umfang** | **nur OHLCV**, Tageskerzen |
| **Ablage** | `research/etf_trendfolge/daten/<SYMBOL>_1d.csv` — ⚠️ **nicht** `data/`, siehe Abschnitt 3.1 |
| **Kursart** | `auto_adjust=True` — siehe Abschnitt 3.2 |
| **Kursaufbereitung** | `shared/kursdaten.entferne_unvollstaendige`, dann `shared/entscheidungskerze.nur_entscheidbar` — siehe Abschnitt 3.3 |
| **Zeitraum des Abrufs** | was da ist (ab 1990). Abgeschnitten wird erst in der Auswertung, damit der Datenbestand nicht an einer Wahl hängt |

### 3.1 Die Randbedingung, an der diese Aufgabe scheitern konnte

**Der Datenstand-Hash der Vorregistrierung ist der SHA-256 über die Dateien
in `data/`:** `d9449faf51bffaaa…` bei **223** Dateien, am 15.09.2026 als
Tatsachennotiz eingetragen (Neuselektion, Abschnitt 10). **Eine einzige
zusätzliche Datei dort ändert ihn** und entwertet den registrierten Zustand,
bevor der Selektionslauf stattgefunden hat.

**Entschieden: `research/etf_trendfolge/daten/`, gitignoriert.** Drei Gründe,
und der dritte ist der tragende:

1. Der Ordner liegt ausserhalb von `data/` — der Hash kann sich nicht ändern.
2. Er folgt dem Vorbild von `research/turn_of_month/daten/` (TB-33), das aus
   demselben Grund entstand.
3. **Gitignoriert** heisst: die Dateien liegen nicht im Repo. Was nicht im
   Repo liegt, kann bei keinem Merge, keinem Rebase und keinem „mal eben
   aufräumen" nach `data/` wandern. Ein Ordner *neben* `data/` wäre sicher
   gegen Absicht; einer, der gar nicht mitgeführt wird, ist auch sicher gegen
   Versehen.

**Zwei Wachen setzen das durch, und beide wirken am Verhalten:**

* `datenstand.py --pruefen` rechnet den Hash über `data/` nach und vergleicht
  ihn mit dem Register. Abweichung heisst **Rückgabewert 1**. Gerechnet wird
  er von `research/vorregistrierung/herkunft.py::datenstand` — **derselben**
  Funktion, die ihn für die Vorregistrierung erzeugt hat, nicht von einer
  zweiten.
* `datenlauf.py` **bricht ab**, wenn sein Zielordner (aufgelöst, also auch
  über einen symbolischen Link) innerhalb von `data/` liegt — **bevor**
  irgendetwas geschrieben wird. Diese Wache wirkt vor dem Schaden; der Hash
  meldet ihn erst danach.

Der Selbsttest weist beides am Ablauf nach (Teile A und J), und
`register.py` bricht schon beim Import ab, wenn `DATEN_DIR` unter `data/`
läge.

### 3.2 `auto_adjust` — die Entscheidung und was sie kostet

yfinance liefert mit `auto_adjust=True` **bereinigte** Kurse: jede
Ausschüttung und jeder Split werden rückwirkend in die ganze Historie
eingerechnet. Beim Aktienbestand dieses Projekts wurde gemessen, dass zwei
Abrufe im Abstand von **Minuten** um bis zu **1,2 × 10⁻⁶** relativer
Abweichung auseinanderliegen. **Bei ausschüttenden ETFs ist die Bereinigung
grösser als bei Aktien.**

**Entschieden: `auto_adjust=True`.** Nicht aus Bequemlichkeit — die
Alternative ist für die Hälfte des Universums schlicht falsch:

* **Vier der vierzehn Kandidaten sind Anleihe-ETFs** (`IEF`, `TLT`, `LQD`,
  `HYG`). Sie schütten ihren gesamten Ertrag aus; ihr Kurs **allein** hat
  deshalb keinen Aufwärtstrend, sondern schwankt um ein Niveau. Ein
  Zwölf-Monats-Momentum auf der unbereinigten Reihe von `HYG` wäre
  strukturell negativ — die Strategie wäre in Anleihen fast dauerhaft in der
  Kasse, und zwar **aus einem Buchhaltungsgrund, nicht aus einem
  Marktgrund**.
* Dieselbe Verzerrung träfe die Klassen **ungleich**: Aktien-ETFs schütten
  wenig aus, Anleihe- und Kredit-ETFs viel. Eine unbereinigte Reihe
  bevorzugte damit systematisch genau die Anlageklasse, deren Übergewicht
  `S-B1` gerade vermeiden soll. Die Strategie würde also an der Aufgabe
  scheitern, für die sie gebaut wird — an einem Datenformat.

**Was die Entscheidung kostet, und wie es bezahlt wird:**

| Kosten | Abhilfe |
|---|---|
| Die Reihe ist **nicht wiederholbar** | Sie wird **einmal** geholt und dann **eingefroren**. `datenlauf.py` überschreibt eine vorhandene Datei **nicht**. Ein erneuter Abruf läuft nur mit `--neu`, und der **vergleicht und meldet**, statt zu ersetzen; übernommen wird erst mit `--uebernehmen` |
| Was sich geändert hat, wäre unsichtbar | Jede Datei bekommt in `daten/manifest.json` ihren **eigenen SHA-256**, ihre Zeilenzahl und ihr erstes und letztes Datum. Ein späterer Abruf, der abweicht, fällt damit auf |
| Die Grösse der Abweichung wäre eine Behauptung | `--neu` **gibt sie aus**, Symbol für Symbol |

> **Der Punkt ist nicht, dass 1,2 × 10⁻⁶ klein ist.** Der Punkt ist, dass
> „klein genug" eine Behauptung wäre. Eine eingefrorene Datei mit eigenem
> Hash ist keine.

### 3.3 Die Entscheidungskerze-Regel gilt auch hier

**Nur Kerzen, deren Zeitraum vor der Startzeit des Laufs endete** (TB-38).
Die Regel steht in **einer** Funktion — `shared/entscheidungskerze.py` — und
wird hier **benutzt**, nicht nachgebaut. Sie läuft **nach**
`shared/kursdaten.entferne_unvollstaendige`:

| Wache | streicht | Eigenschaft |
|---|---|---|
| `entferne_unvollstaendige` | Zeilen mit fehlenden Kursfeldern | der **Zeile** |
| `nur_entscheidbar` | Zeilen, deren Zeitraum noch läuft | der **Zeit** |

Zwei Wachen, zwei verschiedene Fragen. Der Selbsttest nimmt jede **einzeln**
heraus und weist nach, dass genau ihr Fehler auftritt und die jeweils andere
ihn **nicht** auffängt (Teil H).

---

## 4. Die Rastergrenzen — vor jeder Rechnung

### 4.1 Was **fest** ist, und warum

| | Festlegung | Grund |
|---|---|---|
| **Signalfenster** | **fest** {3, 6, 12} Monate = {63, 126, 252} Handelstage | Sie stammen aus der Literatur (Zeitreihen-Momentum, Mehrheitsentscheid). **Ständen sie im Raster, wüchse N — und die Herkunft „aus der Literatur" ginge verloren:** eine gewählte Fensterlänge ist keine übernommene mehr |
| **Mehrheit** | **fest** 2 von 3 | Das ist keine Wahl, sondern das, was das Wort „Mehrheit" bedeutet. Gerechnet: `len(Fenster) // 2 + 1` |
| **Signalmass** | **fest** Vorzeichen der Fensterrendite | Die Alternative (Kurs über gleitendem Durchschnitt) ist ein **anderes Verfahren**, kein anderer Wert. Sie steht als Robustheitsbild ohne Weg ins Urteil (Abschnitt 7) |
| **Gewichtung** | **fest** inverse Volatilität, Standardabweichung täglicher Renditen | Teil der Strategiebeschreibung |
| **Gewichtsdeckel** | **fest: keiner** | Ein Deckel wäre eine zweite freie Zahl ohne Vorbild in der Literatur; die Konzentration ist bei mindestens acht Instrumenten durch die Bauart schon begrenzt |
| **Kasse** | **fest: unverzinst** | ⚠️ Das Projekt hat am 15.09.2026 entschieden, freies Kapital nicht zu verzinsen. Hier gilt dieselbe Festlegung. Sie ist die **konservative**: eine Verzinsung schriebe der Strategie einen Ertrag gut, den sie nicht erwirtschaftet — und zwar ausgerechnet in den Zeiten, in denen sie am meisten Kasse hält |
| **Umschichtung** | **fest** monatlich. **Entschieden** auf der Entscheidungskerze des **letzten Handelstags des Kalendermonats**, **ausgeführt** zur **Eröffnung des ersten Handelstags des Folgemonats** | Zum Schluss des Entscheidungstags zu handeln hiesse, auf einen Kurs zu handeln, den man im Augenblick der Entscheidung noch nicht kennt — genau der Vorgriff, den TB-38 für die neun Bots beseitigt hat |

### 4.2 Die **eine** Rasterachse

Die Beschreibung von `S-B1` legt fast alles fest. Was sie **nicht** festlegt,
ist eine einzige Zahl: **über welchen Rückblick die Volatilität gemessen
wird.** Genau diese eine Zahl steht im Raster.

> **Grenzsatz (Grundlage `datenfrequenz`), wörtlich:**
> „Der Volatilitäts-Rückblick reicht vom Doppelten des Umschichtungsabstands
> bis zum längsten Signalfenster. Geometrisch gestuft nach der Projektregel."

Der Satz nennt **keine Zahl**; die Werte stehen im getrennten Feld — dieselbe
Form wie in Abschnitt 2.1/2.2 der Neuselektion. Die Stufungsregel
(geometrisch, Faktor 1,5 bis 2,0, drei bis fünf Stufen) wird **nicht
abgeschrieben**, sondern aus `research/vorregistrierung/registerdaten.py`
**benutzt**; der Selbsttest hält die erzeugten Stufen zusätzlich auf ihren
Literalen fest, damit eine Änderung dort hier **rot** wird statt still
durchzuschlagen.

| | |
|---|---|
| unten | 2 × Umschichtungsabstand = **42** Handelstage |
| oben | längstes Signalfenster = **252** Handelstage |
| Stufen | **5**, Faktor 1,565 |
| **Werte** | **42, 66, 103, 161, 252** Handelstage |

⚠️ **A1:** Diese Grenze ruht auf `datenfrequenz`, nicht auf einer Messung.
Das ist eine bewusste Abweichung von §2.1 der Neuselektion — begründet in
Abschnitt 0.

### 4.3 N

> **N = 5.** Gezählt aus der Liste der Zellen (`raster.py`), nicht aus einer
> Angabe im Text. Der Selbsttest weist am Ablauf nach, dass eine geänderte
> Achse N ändert (Teil I).

**N kommt zu den 653 der Neuselektion hinzu** (`research/versuchsregister/
REGISTER.md`, Stand 13.09.2026) — es wird nicht dagegen aufgerechnet:

| | |
|---|---:|
| N (dieser Lauf) | **5** |
| N_historisch | 653 |
| **N gesamt, nominal** | **658** |

**Was weitere Achsen kosten würden** — ein Bild für den Betreiber, **keine
Alternative**: eine andere Achsenwahl ist ein neuer vorregistrierter Lauf mit
eigenem N.

| Fall | N |
|---|---:|
| die drei Signalfenster je vierstufig im Raster (statt fest) | 320 |
| zusätzlich ein Gewichtsdeckel mit drei Stufen | 15 |
| zusätzlich der Umschichtungstag mit drei Stufen | 15 |
| zusätzlich das Signalmass mit zwei Stufen | 10 |
| alles davon zusammen | **5 760** |

*Die erste Zeile ist die wichtige: die drei Literaturfenster ins Raster zu
stellen, kostet den Faktor **64**. Jede Zelle erhöht die Schwelle, ab der ein
Ergebnis vom Besten-von-N-Rauschen unterscheidbar ist.*

### 4.4 Die Kantenregel

> Liegt der Gewinner auf einer Rasterkante, wird **nicht erweitert.** Der
> Kantenwert gilt, `S-B1` bekommt die Markierung „Kante". Eine Erweiterung
> wäre ein **neuer vorregistrierter Lauf**, dessen Zellen zu N addiert
> werden.

⚠️ **Befund, offen:** Bei fünf Punkten auf einer Achse sind **zwei** von
ihnen Kanten. Die Wahrscheinlichkeit einer Kanten-Markierung ist hier also
von vornherein hoch, und die Plateau-Regel (Abschnitt 5) hat an den Rändern
nur **einen** Nachbarn statt zwei. Das ist kein Fehler, aber es ist zu
wissen, bevor das Ergebnis da ist — und es ist der Preis dafür, dass die
Literaturfenster fest bleiben.

---

## 5. Falten, Plateau, Bootstrap, Abbruch

**Verfahren B**, wie im Registernachtrag TB-36 festgelegt:

> Die Selektion ist eine **einmalige Auswahl über das vollständige Raster**.
> Jeder Rasterpunkt wird auf jeder Selektionsfalte ausgewertet;
> Selektionsstatistik ist der **Median der Falten-Sharpes**; Gewinner nach
> **Plateau-Regel**. Es gibt **kein Trainingsfenster** und keine faltenweise
> Auswahl. Out-of-Sample ist allein die **Bestätigungsperiode**.

| | |
|---|---|
| **Falten** | Kalenderjahre. **Kein Mindesttraining. Mindestzahl 3.** Trägt die Untergrenze in weniger als drei Kalenderjahren, greift Abbruchkriterium (b) |
| **Faltenzuordnung** | Jeder Handelstag gehört zu der Falte, in die sein Datum fällt. Positionen, die eine Faltengrenze überschreiten, werden **nicht** zugeordnet, geschlossen oder ausgeschlossen. Zwischen Selektionsfalten gibt es weder Purge noch Embargo |
| **Selektionsfalten** | bis einschliesslich **2025** |
| **Go-Live-Schnitt** | **2026-09-01** |
| **Embargo** | 95. Perzentil der Haltedauer des Gewinners in Handelstagen, aufgerundet, **plus 1** — gemessen auf den Selektionsfalten und protokolliert, **bevor** die Bestätigungsperiode geöffnet wird (⚠️ A2) |
| **Plateau-Regel** | Gewinner ist **nicht das Maximum**, sondern der Punkt, dessen Nachbarschaft (± eine Stufe in genau einer Dimension) den höchsten **Mittelwert** hat. Das Plateau-Mittel zählt den Punkt selbst mit; der Spitzentest vergleicht **ohne** ihn: `x` ist Spitze ⟺ `S(x) − M > 0,5 · |M|`. Ist `N(x)` leer, ist `x` keine Spitze |
| **Gleichstand** | erst höhere eigene Statistik, dann der alphabetisch erste Zellenname |
| **Bootstrap** | **stationärer Block-Bootstrap** auf den **täglichen Netto-Mark-to-Market-Renditen des Kapitalpfads**, nie auf Trade-Listen. Flache Tage stehen mit Rendite 0 in der Reihe. **2 000 Ziehungen** |
| **Blocklänge** | `L = max(mediane Haltedauer in Handelstagen, ⌈T^(1/3)⌉)`, `T` = Länge der Reihe. **L wird berechnet und protokolliert; es ist kein Eingabewert** |
| **Trades je Falte** | **Keine Mindestzahl.** Ist die Standardabweichung 0 (kein Trade in der Falte), ist der Falten-Sharpe 0. Die Anzahl Trades wird **berichtet, nicht bewertet** |
| **Falten-Sharpe** | Mittel / Standardabweichung der täglichen Netto-Renditen der Falte × √252. **Ohne Zinsabzug** — eine Zinsannahme wäre eine weitere Wahl |

### 5.1 Die Abbruchkriterien

`S-B1` wird **nicht gebaut**, wenn für den Plateau-Gewinner gilt:

| | |
|---|---|
| **(a)** | Falten-Median des Netto-Sharpe **≤ 0** |
| **(b)** | Die **Untergrenze** (acht Instrumente über vier Anlageklassen) ist in **weniger als drei** Selektionsfalten erfüllt |
| **(c)** | **Beta-Bereinigung:** Netto-Alpha gegen den **Urteilsbenchmark ≤ 0 UND** Calmar unter dem des Urteilsbenchmarks. **Es verlangt beides** — ein Satz mit `alpha ≤ 0`, aber besserem Calmar fällt **nicht** durch |
| **(d)** | Der Gewinner ist eine **Spitze** **und** der beste Nicht-Spitzen-Punkt erfüllt (a) |

**Calmar bei Drawdown 0 ist 0,0, nicht unendlich** — sonst gewänne ein Satz,
der gar nicht handelt.

**Die Kapitalregel bei Ausfall, wörtlich, wie bei den neun Bots:**

- ⚠️ **Das Ergebnis ist KEIN Grund, eine Schwelle zu ändern.**
- `S-B1` läuft **als Schatten weiter** und kehrt nur über einen **neuen
  vorregistrierten Lauf mit veränderter Hypothese** zurück. **Kein „vorerst
  behalten."**

---

## 6. Der Benchmark — der entscheidende Eintrag

**Eine Multi-Asset-Trendfolge gegen Aktien-Buy-and-Hold zu messen, sagt
nichts** — sie soll ja gerade etwas anderes tun. Ein positives Alpha gegen
`SPY` bewiese bei einem Buch aus Gold, Anleihen und Währungen nur, dass
Gold, Anleihen und Währungen nicht `SPY` sind.

### 6.1 Der Urteilsbenchmark: **dasselbe Buch ohne Signal**

> Dieselben Kandidaten, dieselbe inverse Volatilitätsgewichtung, dieselbe
> monatliche Umschichtung, dieselben Kosten — **aber ohne Signal, also immer
> voll investiert.** Die Gewichte werden über dieselben Instrumente normiert,
> die an diesem Umschichtungstag im Universum sind.

**Begründung.** Alles, was `S-B1` von diesem Vergleich unterscheidet, ist das
**Timing** — und das Timing ist das Einzige, was sie hinzufügt. Die
Instrumentenauswahl, die Gewichtungsregel, der Umschichtungsrhythmus und die
Kosten sind in beiden gleich und kürzen sich heraus. Was übrig bleibt, ist
genau die Hypothese.

Das ist die sinngemässe Übertragung dessen, was die Neuselektion für die neun
Bots tut: dort ist der Benchmark das gleichgewichtete point-in-time-Universum
**des Bots** (§7c), also „dieselben Papiere, nur ohne Auswahl der Zeitpunkte".
Hier heisst dasselbe „dieselben Körbe, nur ohne Signal".

⚠️ **Es ist der einzige Benchmark mit einem Weg ins Urteil.** Die anderen drei
sind Bilder; die Urteilsfunktion bekommt sie **gar nicht erst übergeben**.
Der Selbsttest hält das fest (F7/F8).

### 6.2 Die drei Bilder — ohne Weg ins Urteil

| Benchmark | wofür |
|---|---|
| **statisch 60/40** (60 % `SPY`, 40 % `IEF`, monatlich zurückgesetzt, gleiche Kosten) | Das Vergleichsportfolio, das der Betreiber sonst hätte. Die praktische Frage: *lohnt der Aufwand gegenüber dem Einfachsten, was es gibt?* |
| **Aktien-Buy-and-Hold** (`SPY`, gehalten) | Berichtet, **damit sichtbar bleibt, dass dieser Vergleich nichts aussagt** — und weil die **Korrelation** gegen ihn der eigentliche Grund ist, aus dem `S-B1` überhaupt gebaut würde (gemessen: `turtle_soup_stocks` **+0,82**) |
| **Das Neuner-Buch** (gleichgewichtete Tagesreihe der neun heutigen Bots) | Berichtet wird die **Korrelation** gegen `S-B1`. ⚠️ **Berichtet, nicht bewertet:** eine Schwelle dafür wäre eine getippte Zahl, und dieses Register enthält keine getippten Zahlen |

> ⚠️ **Warum die Korrelation trotz allem keine Schwelle bekommt.** Sie ist der
> Grund, aus dem `S-B1` im Katalog steht — es wäre naheliegend, sie zur
> Bedingung zu machen. Dagegen sprechen zwei Dinge: Erstens gäbe es für die
> Höhe der Schwelle keine Grundlage ausser Geschmack. Zweitens **ist die
> Korrelation gegen das Neuner-Buch selbst eine bewegliche Grösse** — sie
> hängt davon ab, welche der neun Bots Rang 1 überlebt, und Rang 1 ist noch
> nicht gelaufen. Eine heute gesetzte Schwelle bezöge sich auf ein Buch, das
> es beim Urteil nicht mehr gibt.

---

## 7. Die Robustheitsbilder — keine Auswahl

Gerechnet wird in jeder Zelle dasselbe wie im Kern, **mit denselben Kosten**:

* **Umschichtungstag:** Anfang / Mitte / Ende des Monats
* **Signalmass:** Kurs über gleitendem Durchschnitt statt Vorzeichen der
  Fensterrendite
* **Gewichtung:** gleichgewichtet statt inverse Volatilität
* **Kassenregel:** Gewichte über die **signalisierenden** Instrumente
  normiert (immer voll investiert, solange ein Signal steht) statt „Kasse als
  Rest"

> ⚠️ **Ins Register, vor dem Lauf:**
>
> **Fällt der Kern durch und besteht ein Robustheitsbild, wird das Bild NICHT
> übernommen. Das Ergebnis lautet dann `DURCHGEFALLEN`.**
>
> *Sonst sind es viele Versuche und nicht fünf, und N wäre eine andere Zahl.*

Die Bilder haben **keine Schwelle** und **keinen Weg ins Urteil**. Wird diese
Bedingung je aufgehoben, ist das ein **neuer vorregistrierter Lauf**, und dann
zählen alle Zellen — zum Versuchsregister **und** zur DSR.

---

## 8. Die Budgetstufen-Leiter

⚠️ **A5:** sinngemäss, nach dem Vorbild der Staging-Ebene von `S-E1`. Weicht
das von der Fassung des Betreibers ab, gilt dessen Fassung.

| Stufe | Kapital | Bedingung |
|---|---|---|
| **Schatten** | keines | `S-B1` erzeugt Signale, protokolliert sie und geht in **keine** Portfolio-Zahl und in **keinen** Crash-Knopf ein |
| **Grundbudget** | die kleinste Stufe, die der Betreiber vergibt | **Rang 1 hat über die neun Bots entschieden** UND der Backtest hat die Abbruchkriterien überstanden UND die Bestätigungsperiode ist abgelaufen |
| **Bestätigt** | volles Gewicht | Die Bestätigungsperiode hat ihrerseits bestanden |

**Trifft eine Bedingung nicht zu, wird der Eintrag geschlossen.** Es gibt kein
„vorerst behalten" — dieselbe Schattenregel wie bei den neun Bots.

> **Warum „Rang 1 zuerst" in der Leiter steht und nicht nur im Vorwort:** Ein
> zehnter Baustein, der vor der Beta-Bereinigung ein Gewicht bekommt, käme
> durch die Hintertür ins Buch. Dieselbe Bedingung steht bei `S-E1` als
> **S1**.

---

## 9. Die Sperrliste

Ab dem Einfrieren dieses Dokuments sind unveränderlich:

1. **Die Kandidatenliste und die Universumsregel** — `register.KANDIDATEN`,
   Registertext 1
2. **Der Survivorship-Vorbehalt** — `register.SURVIVORSHIP_VORBEHALT`,
   Registertext 2
3. **Die Untergrenze** — acht Instrumente über vier Anlageklassen,
   `register.UNTERGRENZE_*`
4. **Der Vorlauf und die Eintrittsregel** — `register.VORLAUF_TAGE`,
   `register.UNIVERSUM_EINTRITT`
5. **Die festen Werte des Signals** — Fenster, Mehrheit, Signalmass
6. **Die Rasterachse und ihr Grenzsatz** —
   `register.VOL_RUECKBLICK_GRENZSATZ`, `register.VOL_RUECKBLICK_TAGE`
7. **N und die Zählregel** — `raster.zellen()`, `raster.n()`
8. **Die Plateau-Regel und die Spitzen-Schwelle** —
   `register.SPITZEN_SCHWELLE = 0,5`
9. **Die Kassenfestlegung** — `register.KASSE_VERZINST = False`
10. **Die Umschichtungsregel** — Entscheidungstag und Ausführungszeitpunkt
11. **Kosten (0,30 %) und Fill-Konvention** — `TRADING_FEE_PCT = 0,1` und
    `SLIPPAGE_PCT = 0,05` je Order
12. **Falten, Mindestzahl, Go-Live-Schnitt, Embargo-Regel**
13. **Bootstrap-Verfahren, Ziehungen und die Blocklängen-Formel**
14. **Die Benchmark-Definitionen und die Regel, dass genau einer ins Urteil
    führt**
15. **Die Abbruchkriterien und die Kapitalregel**
16. **Die Budgetstufen-Leiter**
17. **Der Datenstand-Hash** — `d9449faf51bffaaa…`, 223 Dateien
18. **`auto_adjust = True` und die Einfrier-Regel für die ETF-Kursdateien**
19. **Die Reihenfolge Selektion → Bestätigungsperiode → Bericht**

**Amendment-Regel:** dieselbe wie im Hauptregister (§10.1). Eine Änderung
nach dem Lauf ist ein **neuer registrierter Lauf mit eigenem N**, kein
Amendment.

---

## 10. Was dieser Lauf ausdrücklich NICHT tut

* **Kein Backtest, keine Ertragsrechnung, keine Sharpe-Zahl.**
* **Keine Parametersuche, keine Optimierung, kein „mal schnell ausprobieren".**
* **Keine Auswahl von Instrumenten nach ihrem Ergebnis.**
* Er legt **keinen Bot** unter `strategies/` an. `S-B1` ist ein Kandidat, kein
  Bot — dort landet sie erst, wenn Rang 4 erreicht ist.
* Er ändert **keine** `live_params.py`, keinen `forward_test.py`, keine
  `equity_simulation.py`, keine `multi_symbol_*.py`, nichts unter `broker/`,
  keine Crontab, kein `results/*.csv`.
* Er legt **keine Datei unter `data/`** an, ändert und löscht keine.
* Er rührt `docs/VORREGISTRIERUNG_neuselektion.md` nicht an und lässt
  `research/vorregistrierung/auswertung.py` eingefroren.
* Bot-Dateien werden **gelesen, nie importiert**.

---

## 11. Die Reihenfolge

1. Dieses Register einfrieren — **eigener Commit, vor jeder Rechnung**.
2. Werkzeuge gegen **erzeugte Beispieldaten** prüfen, **bevor** echte Daten
   existieren. *(erledigt: 64/64 Prüfungen)*
3. **Datenlauf am Mac** (`docs/TESTAUFTRAG_TB-39_sb1_vorbereitung.md`).
4. `historie.py` — **Messung** der Historie und der Untergrenze. Fällt sie
   durch: Befund, Ende, Entscheidung beim Betreiber.
5. **Rang 1** — die Selektion auf dem reparierten Mass über die neun Bots.
6. **Erst danach:** der Backtest von `S-B1` über die 5 Rasterzellen.
7. Bestätigungsperiode, einmal.
8. Bericht — alle Zahlen, auch die unangenehmen.

**Zwischen 1 und 6 gibt es keine Stelle, an der jemand etwas entscheidet.**
Das ist der ganze Zweck.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Ob sich aus vierzehn Wertpapierkörben („ETFs") — Aktien, Anleihen, Gold,
Rohstoffen, Währungen — eine Handelsstrategie bauen lässt, die etwas
**anderes** tut als deine neun heutigen Programme. Und, weil man so etwas
hinterher nicht mehr ehrlich beantworten kann: **vorher aufschreiben**, nach
welchen Regeln das geprüft wird.

**Was herauskam.**
Die Regeln stehen. Es gibt genau **eine** Zahl, die noch frei ist (über wie
viele Tage die Schwankung gemessen wird), und dafür **fünf** mögliche Werte.
Alles andere ist festgeschrieben: welche vierzehn Körbe, wann umgeschichtet
wird, dass nicht angelegtes Geld **keine** Zinsen bekommt, und wogegen am
Ende verglichen wird.

Gerechnet wurde **nichts**. Kein Gewinn, kein Verlust, keine Kennzahl.

**Warum das so ist.**
Wer erst rechnet und dann die Regeln aufschreibt, kann sich selbst nicht mehr
glauben — die Regeln passen dann immer zufällig zum schönsten Ergebnis. Fünf
mögliche Werte statt vieler hundert ist dabei kein Geiz, sondern
Beweiskraft: **je mehr Möglichkeiten man durchprobiert, desto
wahrscheinlicher ist die beste davon nur Glück.**

Zwei Punkte sind noch offen, und beide gehören **dir**, nicht der Anleitung:

* **Reicht die Kurshistorie bis 2007 zurück?** Das lässt sich aus der
  Cloud nicht nachsehen — die Kursanbieter sind dort gesperrt. Das Werkzeug
  dafür ist gebaut; gemessen wird auf deinem MacBook.
* **Was passiert, wenn sie nicht reicht?** Dann meldet das Werkzeug das, und
  **du** entscheidest, ob später angefangen oder auf eine Anlageklasse
  verzichtet wird. Die Anleitung entscheidet das nicht.

**Was das für dich heisst.**
Dieses Dokument nicht mehr ändern, sobald gerechnet wird — das ist sein
ganzer Zweck. Und die Reihenfolge einhalten: **erst** die Aufräumarbeit an den
neun heutigen Programmen (Rang 1), **dann** der Rechendurchgang für diese
neue Strategie. Andersherum käme ein zehnter Baustein ins Buch, bevor
geklärt ist, ob die neun anderen überhaupt bleiben.

---

*Erstellt in TB-39, vor jeder Rechnung. Ergänzt die Neuselektion, ersetzt sie
nicht.*
