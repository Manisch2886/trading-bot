# FABLE_ANTWORT 2026-09-25a — Das Register ist ganz gelesen; vier Messungen angenommen; Umgebungsdateien sind kein „ausserhalb"; die Liste ist gleich, die Menge ist registriert; der Laufbereich bekommt eine Definition, und die vier Rückfälle gehören vor den Tag

*Bezug: `FABLE_ANFRAGE_2026-09-25a_tagblocker_weg_zwei_lesarten.md`. Vier Messantworten, TB-103, drei Fragen, ein Plan-Punkt. Reihenfolge: Leseprotokoll zuerst (Abschnitt 0), weil die Tatsachennotiz zu 27 daran hängt; dann in der Reihenfolge der Anfrage.*

---

## 0. Leseprotokoll und die Tatsachennotiz zu 27

**Vollständig gelesen, in diesem Chat:** `REGISTER_KOPIE_2026-09-24_teil2_24_bis_36.md` und `…_teil3_37_bis_40.md` am Stück; die Abschnitte 0 bis Anfang 25.1 hatte ich gestern aus der ganzen Kopie am Stück (24d). Damit ist das Register **0 bis 40 vollständig gelesen**, 24 bis 25.1 doppelt. Dazu: ANFRAGE 25a (Anhang). Alles andere wie 24d. **Nicht gelesen:** `BACKLOG.md`, `belege/`, `ergebnisse/`, Trade-Listen, `MAC_TB-103_…`, `SITZUNGSWAECHTER_…`, `NACHTRAG_ARBEITSWEISE_6d_…`, `PLAN_VOR_DEM_TAG.md`, `ARBEITSWEISE.md`, `UMZUG.md`.

**Für die Tatsachennotiz zu 27:** Anfangsbestand wie in 24d beschrieben; **ab dieser Antwort (25.09.2026) das Register 0–40 vollständig.** Was mir in den Teilen 2 und 3 an Zahlen begegnet ist, ist Benchmark-, Falten-, Kalender- und Datenbestandsseite (25.4, 28.4, 31.5, 32.2) und die MtM-Wirkung in 24.6 nach Bauart 24.3 — nichts nach 27.1. Ich melde einen Punkt, weil 27.4 es verlangt: 26.7 zitiert meine eigene Antwort, dass die Zahl zulässiger Sätze je Bot nicht vorab gemessen wird; ich habe sie nicht gesehen, und sie steht nirgends.

**Ein Nebenertrag des Ganzlesens, der zu Abschnitt 4 gehört:** In 11.1 steht als Voraussetzung des Laufs, dass der BTC-Regimefilter von `t3_supertrend` nicht mehr still übersprungen wird (`shared/regimewache.py`, „Solange er es nicht ist, darf der Lauf nicht starten"), und der Schlusssatz von Abschnitt 10 wiederholt es. Euer Rückfall (b) unten ist also kein neuer Fund, sondern ein seit dem 14.09. registrierter Tagblocker, der noch offen ist.

---

## 1. Die vier Messbitten — angenommen, mit den Folgen

**(1) `purge_tage` hat keinen Leser im Lauf** — Fall „historischer Stand". Eintrag e aus 24d ist damit entschieden: Tatsachennotiz, keine Neuherleitung, `G8` prüft ein Relikt. **Aber die Messung zeigt mehr, als sie beantwortet:** `faltenplan.py::_plan` schreibt die Felder `purge_tage`, `embargo_tage` und `training_bis_ausschliesslich` je Falte in **den Plan, den der Lauf zur Laufzeit bildet** (35.4: `auswertung.py` rechnet ihn über `fp.faltenplan(mess)`). Die Faltenplan-Sonde vergleicht nach 35.4 genau diesen gerechneten Plan mit dem Abbild, **Feldmenge und Werte**, und 33.3 sagt: ein zusätzliches Feld ist ein Fehlschlag wie ein fehlendes. Ein Plan, der Verfahren-A-Felder trägt, fällt also durch die eigene Sonde — oder die Sonde müsste nur eine Projektion vergleichen, und das stünde nirgends.

> **Präzisierung zu 33.3/35.4 (Ersteintrag):** Der Plan, den `faltenplan.py` zur Laufzeit bildet, trägt keine Grösse, die 33.2/33.3 nicht kennt. Die Faltenplan-Sonde vergleicht den ganzen gerechneten Plan gegen das Abbild, nicht eine Auswahl seiner Felder. Verfahren-A-Felder (`purge_tage`, `embargo_tage`, `training_bis_ausschliesslich`) werden vor dem Tag aus `faltenplan.py` entfernt — Berichtigung des Codes an 2c/4a, planmässig nach 37.3 (Sperrlistenpunkt 2, Freigabe, alter und neuer Hash, neues Abbild). `G8` wird nicht gelöscht, sondern angepasst (23a): es prüft künftig, dass der gerechnete Plan je Falte keine Felder ausserhalb der Feldliste trägt — dieselbe Stelle, die registrierte Erwartung.

*Quelle des Grundes:* 33.1 (Fables Satz: „Sechzig verschiedene Trainingsgrenzen in einer Datei beschreiben ein Verfahren mit Trainingsfenster. Dass niemand sie liest, sieht man der Datei nicht an") — er gilt für den gerechneten Plan wie für die Datei. Kein Ergebnis. Wann das geschieht (mit dem Abbild-Auftrag oder davor), ist Handwerk; **vor** der Sonde muss es sein, sonst ist ihr erster Lauf rot aus einem Grund, der keiner ist.

**(2) Die Zeitbremse wirkt in jeder Zelle** — angenommen; die Voraussetzung aus 24d trägt. Zwei Sätze dazu: Erstens ist „aus dem Quelltext gelesen, kein Lauf je Zelle" die richtige Kennzeichnung, und für diese Frage reicht sie — ob eine Konstante von einer Achse abgeschaltet wird, steht im Code, nicht im Ergebnis. Zweitens der Durchreichparameter `max_hold_days` bei den zwei Volatility-Bots: Er ist keine Achse, also im registrierten Raster wirkungslos — **solange `registerdaten.py::raster_definition()` ihn nicht nennt.** 2.6 sagt, die Zeitbremse ist Konstante des Laufs; dass sie es bleibt, hängt an einer Achsenliste, die niemand prüft. Das ist dieselbe Kopplung wie `G6` an 5.1 Nr. 4, nur ungesichert. Eine Prüfung „keine Achsenliste nennt `max_hold_days`/`max_hold_hours`" hält 2.6 fest; ob sie in `test_vorregistrierung.py` gehört, ist Handwerk. Ich trage sie als Vorschlag ein, nicht als Regel.

**(3) Der Lesehaken ist von TB-92; euer Satz war falsch, das Register hatte recht.** Angenommen, und die Ursache benennt ihr richtig: eine Nummer übernommen statt geprüft — meine falsche Nummer, eure ungeprüfte Übernahme, eine Kette. Die Folgerung steht: Der Benchmark-Nachweis ist 2 aus seinem eigenen Protokoll; führbar nach beiden Eingaben, dann als Neurechnung mit beiden Teilen. **Ein Fund in eurer Tabelle, den 39.8 schon trug und den ich dort überlesen hatte:** der Modus-Lauf öffnet `logs/notifications/manuelle_eingriffe.log` **im Modus `a`** — zum Anhängen, aus dem Repo, über einen Import aus `notifications/`. Die Datei blieb unverändert, aber ein Lauf, der eine Repo-Datei zum Schreiben öffnet, hat ein Schreibziel ausserhalb seines `--ziel`. Das gehört nicht zur Lesequellen-, sondern zur **Schreibziele-Sonde** (23c), und es ist dort ein Befund 1, unabhängig davon, ob Bytes geschrieben wurden: Ein Import, der beim Laden eine Datei zum Schreiben öffnet, ist eine Nebenwirkung, die im Laufbereich nichts zu suchen hat. Vor dem Tag; Handwerk mit Freigabe (`notifications/` ist Live-Code).

**(4) 16.6, „Journal":** Ihr habt gemessen, dass der Wortlaut beide Lesarten trägt. Die Entstehung von 16.6 kenne ich **nicht** — der Satz stammt vom 16.09. (TB-41), vor jedem Chat, den dieser Anfangsbestand kennt; ich kann nicht sagen, ob damals der Papierpfad gemeint war, und ich werde es nicht erschliessen. Nach eurer Messung ist Eintrag c eine **Präzisierung**, und F17 ist so oder so erfüllt; die Kategorie ist Handwerk (30.6). Sie bleibt Präzisierung.

---

## 2. TB-103 — Kenntnisnahme, und was die Tag-Vorbedingung jetzt ist

**Resolver:** `CONFIG_DIR = <snapshot>/config`, Prüfung beim Import gegen das, was **das MANIFEST** unter `config/` nennt, `SystemExit(2)` bei fehlend/leer/nicht genannt, Dateinamen nicht in `paths.py`, ohne Modus 99 Pfade 0 Unterschiede, vier Mutationsproben, jede beisst allein, 35/35 und 191/191. Das ist die Bauart aus 24b A2, und der Punkt, dass das MANIFEST der eine Ort ist, der die Anordnung kennt, ist besser als das, was ich vorgeschlagen hatte („Kurse flach, Universum unter `config/`" stand bei mir als Beschreibung, nicht als Quelle). Die fünf Symboldateien mit dem eingebauten Rückfall sind unverändert; ihr Rückfall ist unter dem Modus unerreichbar — solange `paths.py` so bleibt. Das ist eine Tatsachennotiz mit Bedingung, und sie gehört so ins Register.

**Trockenlauf aller neun:** über `TB_SELEKTIONSWURZEL`, mit Lesehaken und Aufrufstapel, 9 × 0, Liste = Universumsdatei 9/9, Kurs- und Universumsdateien ausserhalb 0, Standardliste 0. **Der Tagblocker ist weg — für den Stand `836865f`.** Die Tag-Vorbedingung aus 24b A2 ist damit in ihren Teilen erfüllt, mit zwei Präzisierungen, die eure Fragen A und B verlangen (Abschnitt 3), und mit einem Satz, den ich in 24b nicht geschrieben hatte:

> **Ergänzung zur Tag-Vorbedingung (24b A2):** Der Trockenlauf aller neun Bots im Modus wird **am Tag-Commit** wiederholt — wie das letzte Abbild (37.3) trägt sein Protokoll die Hashes des Standes, den der Tag signiert. Ein Trockenlauf an einem früheren Stand ist eine Tatsachennotiz, keine Tag-Vorbedingung.

*Quelle des Grundes:* 37.3 (das letzte Abbild passt zum Tag-Commit); zwischen `836865f` und dem Tag ändern sich `paths.py`-nahe Module noch (Plan-Punkt 2, die Rückfälle aus Abschnitt 4). Kein Ergebnis.

**`messgroessen.py`:** im Modus zweimal bytegleich, 222 + 2 aus dem Snapshot, 0 aus `data/`/`config/`, genau ein Zugriff ausserhalb (`haltedauern_je_bot.csv`) ⇒ **2, nicht geführt**, wie ihr sagt. Der eine Zugriff ist der erwartete: 24c hat die Haltedauern auf die neuen Listen gelegt; bis Plan-Punkt 3 kann der Nachweis nicht anders ausgehen. Er steht damit hinter Punkt 3 — zusammen mit dem Benchmark-Nachweis.

---

## 3. Die drei Fragen

### (A) Umgebungsdateien zählen nicht als „ausserhalb" — und die Liste ist Teil des Nachweises

Eure Neigung ist richtig, und ich mache sie zur Regel, mit einem Zusatz, den eure Tabelle nahelegt:

> **Präzisierung zu 24c (b) und zur Tag-Vorbedingung 24b A2 — drei Klassen von Zugriffen:** Jeder Datei-Zugriff eines Modus-Laufs fällt in genau eine von drei Klassen. **(i) Eingaben** — Kurs-, Universums-, Ergebnis- und Eingabedateien: zulässig nur innerhalb `snapshots/<hash>/` oder als registrierte Eingabedatei; jeder andere ist Befund 1 des Nachweisteils (b). **(ii) Umgebung** — `requirements.lock`, Interpreter- und Plattformdateien, Zufallsquelle, Zeitzonendaten, vom Import der registrierten Pakete geöffnet: zulässig; die Liste dieser Zugriffe je Lauf-Typ steht **mit Aufrufstapel als Tatsachennotiz**, und ein Umgebungszugriff, der in dieser Liste nicht steht, ist ein Befund 1 — nicht weil er die Rechnung berührt, sondern weil niemand weiss, ob er es tut. **(iii) Schreibzugriffe** — ein Modus-Lauf öffnet zum Schreiben nur sein `--ziel` und Belegpfade; jedes andere Schreibziel ist Befund 1 der Schreibziele-Sonde, auch ohne geschriebene Bytes. „0 Zugriffe ausserhalb `snapshots/<hash>/`" in 24b A2 lies „0 Zugriffe der Klasse (i) ausserhalb; Klasse (ii) nach Liste; Klasse (iii) leer".

*Quelle des Grundes:* 5f — die Umgebung ist registriert (Lock mit Hash, Abschnitt 20), und `requirements.lock` ist die Datei, mit der der Modus die Umgebung **prüft**; ein Nachweis, der die Prüfung als Verstoss zählt, widerspricht sich. Warum die Liste trotzdem geführt wird: `/dev/urandom` beim pandas-Import ist harmlos, solange die Neurechnung bytegleich ist — und genau das ist Nachweisteil (a); ein Lauf, der plötzlich eine sechste Umgebungsdatei öffnet, hat ein Paket oder einen Importpfad gewechselt, und das sieht man sonst nirgends. Kein Ergebnis.

### (B) Die Liste ist gleich; die geladene Menge ist registriert — und das ist die stärkere Prüfung

Wörtlich verlangte mein Satz Unmögliches; gemeint war die **Liste** — der Rückfall aus TB-98 war eine Listen-Ersetzung. Eure Lesart ist richtig, und ich mache aus dem dritten Teil etwas Besseres als „mit und ohne Modus gleich": Die geladene Menge je Bot ist **registriert** — 16.1.1, Spalte Bestätigung: 18 / 18 / 20 / 20 / 20 / 147 / 147 / 147 / 147. Eure Zahlen („Krypto 18 bzw. 20 von 24, Aktien 147 von 150") sind genau diese. Ein Vergleich Modus-gegen-ohne-Modus vergleicht zwei ungeregelte Dinge; ein Vergleich gegen 16.1.1 vergleicht gegen das Register.

> **Präzisierung zu 24b A2 („geladene Symbolmenge gleich Universumsdatei"):** (1) Die **Liste**, die der Bot erhält, ist gleich der Universumsdatei des Snapshots nach `EXCLUDE_SYMBOLS` (16.1.3: 24 von 25; 150). (2) Die **geladene Menge** ist gleich der in 16.1.1 für die Bestätigungsperiode registrierten Zahl je Bot *[Voraussetzung, zu messen: dass der Trockenlauf den Loader am Datenende aufruft, wie die Bestätigungsspalte von 16.1.1 gemessen wurde]*. (3) Jede Differenz zwischen (1) und (2) steht im Ladeprotokoll je Symbol mit Grund. (4) Das Ladeprotokoll nennt die Länge der Liste, die Zeilenzahl der Universumsdatei und die **Quelle** der Liste (Pfad). Gleichheit mit und ohne Modus ist Tatsachennotiz, keine Bedingung.

*Quelle des Grundes:* 3b (b) — welche Symbole geladen werden, entscheidet die registrierte `MIN_HISTORY_*`-Tabelle, und ihr Ergebnis ist in 16.1.1 gemessen und eingetragen; eine Vorbedingung prüft gegen das Register, nicht gegen einen zweiten Lauf. Kein Ergebnis. **Zu (4):** Das Ladeprotokoll nennt heute weder die Zeilenzahl der Datei noch die Quelle — ihr habt es gemessen. Bis das nachgezogen ist (Handwerk mit Freigabe, `shared/ladeprotokoll.py`), ist die Vorbedingung in Teil (4) **nicht** erfüllt; das steht so in der Tatsachennotiz zu TB-103, nicht als Mangel des Laufs, sondern als das, was noch fehlt.

### (C) Der Wortlaut der Resolver-Pflicht — einverstanden, mit einer Frage zum Nebeneffekt

Angenommen: *„über den Resolver (`shared/paths.py`, direkt oder über `strategy_paths.get_strategy_paths()`)"*. Meine Fundstelle `shared/paths.py::get_strategy_paths()` war falsch — eine Funktion in der falschen Datei genannt, nicht gemessen. **Achter Fall**, dieselbe Klasse. Berichtigung zu 24c Abschnitt 2 mit eurem Wortlaut.

Was ihr nebenbei gemessen habt, ist selbst ein Befund: `get_strategy_paths()` legt `results/<name>/` und `logs/<name>/` per `makedirs` an. Für die neun Bots ist das Regelbetrieb. **Unter dem Modus** ist es ein Schreibzugriff ins Repo (Klasse (iii) oben), auch wenn nur Ordner entstehen. *[Messbitte, nur das Ob: legt ein Modus-Lauf eines Bots heute Ordner unter `results/` oder `logs/` des Repos an, oder existieren sie schon und `makedirs` tut nichts?]* Wenn ja, ist es ein Schreibziel ausserhalb `--ziel` und gehört zur Schreibziele-Sonde; die Behebung ist Handwerk (Ordner unter dem Modus in den Belegpfad oder gar nicht).

---

## 4. Plan-Punkt 2 — der Laufbereich bekommt eine Definition; `herkunft.py`; die vier Rückfälle

**Was „Laufbereich" heisst.** Ihr habt gut 50 Fundstellen eingebauter Rückfälle gemessen. Die Regel aus 24b A2 gilt „unter dem Modus" — sie gilt also für Code, der unter dem Modus **läuft**, nicht für jede Datei im Repo. Das Register definiert den Laufbereich bisher nicht; der Lese-Audit (5e) definiert ihn implizit, nämlich durch das, was ein Lauf tatsächlich lädt.

> **Registertext, Ersteintrag — Laufbereich:** Der Laufbereich ist die Menge der Module, die ein Modus-Lauf lädt oder ausführt (Trockenlauf aller neun Bots, Erzeuger, `benchmark.py`, `faltenplan.py`, `auswertung.py` und ihre Kindprozesse), gemessen am Aufrufstapel des Lese-Audits. Die Regeln „kein Fallback unter dem Modus" (24b A2), die Resolver-Pflicht (24c) und die drei Ausgänge (36.5) gelten für genau diese Menge; die Sonde „Lesequellen" führt sie. Ein Rückfall in einem Modul ausserhalb des Laufbereichs ist eine Tatsachennotiz, kein Befund — bis das Modul geladen wird.

*Quelle des Grundes:* 5e (der Lauf belegt, woraus er gelesen hat — und damit, was er ist) und A8 (eine Regel braucht eine Menge, auf der jemand sie prüfen kann). Kein Ergebnis. **Folge für die 50:** Welche davon im Laufbereich liegen, sagt der Aufrufstapel von TB-103 und der künftigen Erzeuger-Läufe; die übrigen bekommen eine Notiz und warten.

**Die fünf Leser mit eigener Pfadlogik** (`benchmark.py`, `faltenplan.py`/`faltenplan_neun.py`, Trockenlauf/Loader, `herkunft.py::datenstand()`): je ein Befund der Resolver-Pflicht, ein Auftrag vor dem Erzeuger — einverstanden; die Reihenfolge ist eure.

**`herkunft.py` — „nicht öffnen" bleibt, unter einer Bedingung, die zu messen ist.** Die Entscheidung aus 22d/37.4 hatte einen Grund: die Sperrlisten-Sonde schliesst die Lücke, die `herkunft.py` sonst schlösse. Die Resolver-Pflicht ist ein anderer Grund, und sie greift nur, wenn `datenstand()` **selbst** entscheidet, woher es liest. *[Messbitte, nur das Ob: nimmt `herkunft.py::datenstand()` das Verzeichnis als Argument (wie der Aufruf aus `research/etf_trendfolge/datenstand.py`, 37.4, nahelegt), oder liest es fest `data/`?]* Wenn Argument: Der Erzeuger (neuer Code) übergibt den Pfad des Resolvers; `herkunft.py` bleibt zu, seine Voreinstellung ist unter dem Modus tot, Tatsachennotiz. Wenn fest: Dann kann der Erzeuger den Datenstand-Hash des Snapshots damit nicht bilden, und die Alternative — dieselbe Hash-Regel ein zweites Mal im Erzeuger — wäre ein zweiter Ort für dieselbe Funktion; dann wird `herkunft.py` **planmässig geöffnet** (37.3: Auftrag, Freigabe, alter und neuer Hash an Punkt 11/12, neues Abbild), genau einmal, für diese eine Zeile. Die Resolver-Pflicht geht in diesem Fall vor, weil die andere Wahl das Verbot „ein Wert, ein Ort" bräche, das älter ist als „nicht öffnen".

**Die vier weiteren Rückfälle — alle vier vor den Tag, in dieser Rangfolge, jeder mit Gegenprobe (Rückfall erreichbar gemacht ⇒ Rückgabe 2):**

| | Rückfall | Warum vor den Tag |
|---|---|---|
| **1** | **(b)** `t3_supertrend`: BTC-Regimefilter fällt still weg, wenn BTCUSDT nicht geladen ist | ⚠️ **Schon registriert als Voraussetzung des Laufs** — 11.1 (`shared/regimewache.py`, `pruefe_einbau()`, „Solange er es nicht ist, darf der Lauf nicht starten") und Schlusssatz von Abschnitt 10. Kein neuer Beschluss nötig; euer Fund ist die Messung, dass 11.1 offen ist. Dass BTCUSDT im Trockenlauf geladen war, ändert nichts: 11.1 begründet den Abbruch mit Determinismus, nicht mit dem heutigen Bestand |
| **2** | **(c)** Backtest-Skripte enden bei „Keine Daten gefunden" mit `exit()`, rc 0 | Das ist TB-45 in Reinform — 0 ohne Messung —, und 36.5 gilt für jede Wache und jeden Lauf: „Kein Aufruf endet mit 0, ohne dass gemessen wurde." Unter dem Modus: 2 |
| **3** | **(d)** Stille Ersatzwerte für Schwellen in `faltenplan.py`, `benchmark.py`, `auswertung.py` | Ein Ersatzwert für eine registrierte Schwelle ist ein Fallback für einen Parameter (24b A2 nennt Schwellen ausdrücklich) — und er ist schlimmer als ein Schalter, den 12 für `auswertung.py` ausschliesst: Ein Schalter ist sichtbar, ein `.get(…, default)` nicht. Vorab je Stelle Tatsachennotiz, ob die registrierte Eingabe den Schlüssel je auslässt; unabhängig davon Ersatz durch Abbruch 2. `auswertung.py` ist Sperrlistenpunkt 3/5/14 — planmässig nach 37.3, wie TB-92 |
| **4** | **(a)** Krypto-Liste nach `EXCLUDE_SYMBOLS` leer ⇒ Standardliste | Auf dem registrierten Snapshot unerreichbar — aber die Regel gilt für den Modus, nicht für diesen Snapshot; ein Rückfall, den erst der nächste Snapshot erreicht, ist genau „gleich welcher Art". Kleinster Aufwand (eine Prüfung „leer ⇒ 2" in `symbols_config.py`, Live-Code, eigene Freigabe); kleinster Rang, aber nicht als Notiz abgetan |

*Quelle des Grundes:* 24b A2 im Wortlaut, 36.5, 11.1. Kein Ergebnis: Keiner der vier verändert, was der Lauf rechnet, wenn alles da ist; sie verändern, was er tut, wenn etwas fehlt — und das ist das Einzige, was der Modus regelt.

---

## 5. Meine Berichtigungen aus dieser Antwort, gesammelt

| | an | Art |
|---|---|---|
| a | 24c Abschnitt 2: „`shared/paths.py::get_strategy_paths()`" lies „`shared/paths.py`, direkt oder über `strategy_paths.get_strategy_paths()`" | Berichtigung einer Fundstelle — **achter Fall** |
| b | 24b A2, Tag-Vorbedingung: „0 Zugriffe ausserhalb `snapshots/<hash>/`" lies nach den drei Klassen (3 (A)) | Präzisierung des eigenen Wortlauts |
| c | 24b A2: „geladene Symbolmenge gleich Universumsdatei" lies nach (1)–(4) in 3 (B) | Präzisierung des eigenen Wortlauts |
| d | 24b A2: Wiederholung am Tag-Commit | Ergänzung |
| e | 24d Eintrag e: entschieden als historischer Stand; dazu die Präzisierung zu 33.3/35.4 (Plan ohne fremde Felder, `G8` angepasst) | Ergänzung |

**Für Register 41/42 kommen hinzu** (zu 24c Abschnitt 6 und 24d Abschnitt 4): die drei Klassen (3 (A)), die vier Teile der Symbolbedingung (3 (B)), der Laufbereich (4), die Präzisierung zu 33.3/35.4 (1 (1)), die Tatsachennotiz zu TB-103 (Resolver mit MANIFEST als Ort; Trockenlauf mit Umgebungsliste; Ladeprotokoll-Teil (4) offen), die Tatsachennotiz zum Lesehaken (TB-92, `a1b_lesehaken.py`; eure Berichtigung), die Schreibziel-Notiz zu `manuelle_eingriffe.log`, die Einordnung der vier Rückfälle mit dem Verweis auf 11.1.

---

**Kurz:** Register 0–40 jetzt ganz gelesen — ab 25a vollständiger Bestand. Die vier Messungen sind angenommen; aus (1) folgt mehr, als sie fragt: Der zur Laufzeit gerechnete Plan darf keine Verfahren-A-Felder tragen, sonst fällt er durch die eigene Sonde — `faltenplan.py` gibt sie ab, `G8` wird angepasst, nicht gelöscht. Der Lesehaken ist von TB-92; eure Kette (meine Nummer, eure Übernahme) ist benannt; der Modus-Lauf öffnet ein Log im Repo zum Schreiben — Schreibziele-Sonde. (A) Umgebungsdateien sind kein „ausserhalb"; drei Klassen: Eingaben, Umgebung nach Liste, Schreibziele leer. (B) Die Liste ist gleich der Datei; die geladene Menge wird gegen 16.1.1 geprüft, nicht gegen einen zweiten Lauf; Teil (4) des Ladeprotokolls fehlt noch. (C) Euer Wortlaut, meine Fundstelle war falsch — achter Fall. Der Laufbereich ist die Menge, die ein Modus-Lauf lädt; die 50 Fundstellen sortieren sich daran. `herkunft.py` bleibt zu, wenn `datenstand()` den Pfad nimmt; sonst planmässig öffnen. Die vier Rückfälle gehören alle vor den Tag — (b) steht dort seit dem 14.09. (11.1), (c) und (d) sind TB-45, (a) ist klein, aber „gleich welcher Art".

**Unsicher:** (1) ob `datenstand()` das Verzeichnis als Argument nimmt; (2) ob ein Modus-Lauf Ordner unter `results/`/`logs/` anlegt; (3) ob der Trockenlauf am Datenende lädt, wie 16.1.1 gemessen wurde; (4) ob ein `.get(…, default)` in `auswertung.py` mit den registrierten Eingaben je erreichbar ist — für die Regel ohne Belang, für die Tatsachennotiz nicht.

---

## In einfacher Sprache

Der neue Chat hat das Regelwerk jetzt ganz gelesen; das wird festgehalten. Die vier Nachmessungen sind angenommen, eine davon zeigt einen weiteren Fehler auf unserer Seite, den das Regelwerk schon richtig hatte. Der wichtigste Fund heute: Das Programm, das den Zeitplan der Auswertung berechnet, schreibt noch Werte aus einem alten Verfahren hinein, die niemand liest — und die Wache, die den Plan gegen das Abbild prüft, würde genau daran scheitern. Also raus damit, bevor die Wache gebaut wird.

Auf die drei Fragen: Systemdateien, die jedes Programm beim Start öffnet, sind kein Regelverstoss — aber es wird festgehalten, welche es sind, damit eine neue auffällt. Die Werteliste muss gleich der eingefrorenen Datei sein; wie viele Werte davon tatsächlich geladen werden, steht schon im Regelwerk, und dagegen wird geprüft. Die genauere Formulierung der Pfadregel übernehme ich; meine alte Fundstelle war falsch.

Und die übrigen Notlösungen im Code: alle vier kommen vor den Stichtag. Eine davon steht seit dem ersten Tag als Bedingung im Regelwerk und ist bis heute offen; zwei sind der bekannte Fehler „meldet Erfolg, ohne gemessen zu haben"; die vierte ist klein, aber die Regel kennt keine Ausnahme nach Grösse.
