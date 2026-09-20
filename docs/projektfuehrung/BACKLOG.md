# Backlog Trading-Bot-Projekt

**Stand: 18.09.2026.** Nur **aktive Punkte**. Alles Abgeschlossene steht im
`JOURNAL.md` und wird von dort **nicht** zurückgeholt.

> ⭐ **Rückblicke auf abgeschlossene Aufgaben stehen in
> `BACKLOG_ARCHIV.md`** (angelegt 20.09.2026, TB-60), Messprotokolle im
> `JOURNAL.md`. **Beide werden nur gelesen, wenn es um eine konkrete
> frühere Messung geht** — diese Datei trägt die aktiven Punkte.
> ⚠️ **Nichts davon ist gelöscht:** jede verschobene Zeile steht
> zeichengleich im Archiv, nachgewiesen in
> `docs/ERGEBNIS_TB-60_backlog_archiv.md`.

> **Diese Datei gehört in jede Sitzung. Das Journal nur, wenn es um eine
> konkrete Messung geht.**

> ⚠️ **Kürzel:** Punkte aus dem **Strategie-Katalog** tragen das Präfix `S-`
> (`S-B1`, `S-E1`, `S-G1`). Ohne Präfix meint ein Kürzel immer diese Datei.
> Insbesondere: **G1 = „Alles hängt an einem MacBook"** — das in Block U des
> Journals gestrichene „G1" war `S-G1` (Ko-Drawdown-Gewichtung).

**Der Massstab, an dem alles hier gemessen wird:**
*Ändert es etwas an der Frage, ob dieses System Geld verdient — und woher wir
das wissen?*

---

## 0 — Die Frist

**13.12.2026.** Bis dahin muss die Neuselektion auf dem reparierten Mass
gelaufen sein. Findet sie nicht statt, ist „beide Werte ausweisen" zum Zustand
geworden — also die Vertagung, die es zu vermeiden galt.

---

## 1 — Sofort, am Mac (rund eine Stunde)

| # | Punkt | Warum |
|---|---|---|
| ~~A1~~ | ~~Festplattenvollzugriff~~ **ERLEDIGT 14.09.** — Crontab wieder schreibbar ( fürs Terminal** — Systemeinstellungen → Datenschutz & Sicherheit | ⭐ **Der wertvollste Einzelpunkt im ganzen Backlog.** Blockiert A2, die vier Wächter-Cronjobs und die Log-Rotation. **15 Minuten** |
| ~~A9~~ | ~~`git push`~~ **ERLEDIGT 14.09.** — beide Commits auf GitHub ( — drei lokale Commits liegen ungepusht (`94b2e3c` Ergebniskurven u. a.) | Hat laut Journal AD.2 bereits eine Cloud-Sitzung auf eine **falsche Prämisse** geführt. **2 Minuten** |
| ~~A2~~ | ~~Cronjob Schliess-Benachrichtigung~~ **ERLEDIGT 14.09.** — eingetragen, Erstlauf **6 Meldungen** versendet ( eintragen *(hängt an A1)* | Der einzige Punkt mit **laufendem Schaden** — Schliessungen werden derzeit gar nicht gemeldet |
| **A3** | ~~`node` per Homebrew~~ **BEWUSST UEBERSPRUNGEN 14.09.** — Homebrew nicht installiert, und die vier Pruefungen laufen bei **jedem PR in der Cloud** mit. Der eigentliche Punkt (780 sieht aus wie ein volles Gruen) steht in den Testauftraegen. ( | Ohne node meldet `test_dashboard.py` 780/780 statt 784 — **ein falsches Grün**. 5 Minuten |
| **A4** | **Testauftrag Notbremse** (PR #73) lokal ausführen | Der Crash-Knopf ist die Sicherheitseinrichtung |
| **F3 + N3** | Tägliche Bot-Mails abschalten · in der Montagsmail **„LIVE-PORTFOLIO" durch „BACKTEST" ersetzen** | Eine Falschbeschriftung, die du **wöchentlich liest** |
| ~~A7~~ | ~~Cronjob Log-Rotation~~ **ERLEDIGT 14.09.** ( *(hängt an A1)* | klein |
| ~~Wächter als Cronjobs~~ **ERLEDIGT 14.09., 40 Crontab-Zeilen.** **TB-32 erledigt (PR #104)** — Journal **AL**. ⚠️ **Offen: fünf Crontab-Zeilen auf den Wrapper umstellen**, Zeilen im Testauftrag | `ergebniskurven.py --nur-abweichung` · `determinismus.py --schnell` · `versuchsregister.py --pruefen` · `tb27/vergleich.py --pruefen`, je mit Telegram-Meldung bei Befund | **Vier Cron-Zeilen ersetzen die geplante Systemgesundheits-Seite** |

*Gestrichen aus dem alten A-Block:* A5, A6, A8 (Sichtprüfungen und
Mutationsproben für Dashboard-Details, deren Oberfläche nicht weiter ausgebaut
wird).

---

## 2 — Vor TB-30b: die Vorregistrierung vervollständigen

Alles hier muss **vor** dem Selektionslauf stehen. Danach wäre es ein
Amendment.

| # | Punkt |
|---|---|
| **V1** | **ENTSCHIEDEN 14.09.: die absolute Drawdown-Grenze wird gestrichen.** Sie bindet nur, wenn der Benchmark selbst unter −28 % faellt — dann aber fuer **alle** Parametersaetze eines Bots gleichzeitig, wirft ihn also aus, **bevor gewaehlt wurde**. *„Ein Bot, der bei voller Exposure in 2022 −33 % macht, hat kein Parameterproblem, sondern ein Beta-Problem — und das entscheidet Rang 3."* Der Risikoappetit kommt an zwei anderen Stellen zu seinem Recht: als **Deckel je Bot im Netting** (Rang 5) und als **berichtete Zeile** in der Beurteilung |
| **V1** *(Vermerk 19.09.2026, Nachtrag (l))* | ⚠️ *„Die `V`-Nummern in Block 2o stammen aus der Vorprüfung vom 19.09.2026 und bilden eine **eigene Reihe** — sie sind nicht die `V`-Reihe aus Abschnitt 2. Beide Nummerierungen bleiben; keine wird geändert."* |
| **V1b** | **Stattdessen eine Toleranzuntergrenze** — die echte Luecke liegt in den **ruhigen** Falten (Benchmark −2 %, erlaubt −2,5 %, drei schlechte Tage entscheiden): `erlaubt(f) = min(1,25 x DD_Benchmark(f), DD_Toleranz)`, beide negativ, `min` = der tiefere Wert. **`DD_Toleranz` = Median der Benchmark-Drawdowns ueber alle Selektionsfalten**, **je Bot** — der Benchmark haengt an der Exposure, ein Bot mit 21 % und einer mit 100 % Zeit im Markt liegen auf verschiedenen Skalen |
| **V1c** | **Benchmark-Exposure = die des jeweiligen PARAMETERSATZES in der jeweiligen Falte**, nicht die heute gemessene des Bots. Dann verweist nichts im Register mehr auf den Live-Zustand; die Zahl liegt ohnehin vor, weil der Kapitalpfad sie erzeugt |
| **V2** | **TB-31 erledigt (PR #105), Ladelauf am Mac gestoppt — Journal AJ + AK.** ⚠️ **Der Trockenlauf verweigerte das Schreiben bei ALLEN 72 Dateien** — zu Recht: Sie enden mit einer **abschliessenden Teilkerze** (2026-08-31 12:00), die `--teilkerze-ersetzen` nicht abdeckt. **Ursache tiefer als erwartet:** Es gibt **keinen Cronjob, der die Kursdateien aktualisiert** — die `forward_test.py` holen live, `data/` wird nur von Hand gepflegt und ist zwei Wochen alt. → **TB-34** baut den Bestand sauber neu auf. **Erledigt:** `LOOKBACK` steht in beiden Dateien auf `"1 Jan, 2017"`, Kommentare nachgezogen. **Gemessen:** Die 13 Symbole am Fensterrand haben echte Historie dahinter (BTC/ETH ab **2017-08**, BNB 2017-11, ADA/XRP/TRX 2018, DOGE/LINK/ZEC 2019, SOL/UNI/AAVE/NEAR 2020); die 11 uebrigen stehen auf ihrem echten Listing |
| **V3** | **AB2 entscheiden: abbrechen.** `t3_supertrend` überspringt seinen BTC-Regimefilter **stillschweigend**, wenn `BTCUSDT` fehlt; `volatility_breakout_crypto` bricht ab. Ein Lauf, in dem ein Bot still ohne Filter rechnet, ist nicht deterministisch. **Vor dem Lauf = Bug-Fix, danach = Amendment** |
| **V4** | **Rasterregel aus Y3:** Die Obergrenze des Positionslimits ist `floor(1 / ALLOCATION_PCT)` — **abgeleitet, nicht willkürlich**. Ein Rasterpunkt darüber ist derselbe Punkt wie die Obergrenze. *(`volatility_breakout` hat Limit 15 bei zehn finanzierbaren Positionen — das Limit greift nie)* |
| **V5c** | **FABLES ANTWORT LIEGT VOR (15.09.2026)** — `registerfestlegungen_2026-09-15.md`. ⭐ **Kern: Verfahren B statt A.** Einmalige Selektion über das ganze Raster, Faltenmedian, Plateau-Regel; **kein Trainingsfenster**, N = Rastergrösse, **Out-of-Sample ist allein die Bestätigungsperiode**. Fables eigene Checkliste vom 14.09. enthielt beide Verfahren nebeneinander. ⚠️ **Folge für TB-30b: die sechs bot-eigenen Walk-Forward-Rechner werden ERSETZT durch einen Faltenauswerter, nicht umgestellt.** Registertexte 0, 1a/1b, 2a–2d, 4a–4d sind unstrittig und können ins Register |
| **W1** | ⭐⭐ **FABLE 15.09., Antwort auf die Wochenrückmeldung — drei Festlegungen.** **(2.1)** Der **Live-Betrieb folgt dem Backtest**: die fünf Krypto-Bots werden auf die letzte **abgeschlossene** Kerze umgestellt, über **eine gemeinsame Abruffunktion** mit `close_time`-Filter, die Backtest und Forward-Test beide benutzen. Begründung: den Backtest eine Teilkerze nachbilden zu lassen hiesse, **einen Bug zu modellieren**. ⚠️ **Der Live-Record der fünf zerfällt am Umstellungstag** — das Stück davor taugt nicht als Holdout, Umstellungstag ins Journal, **I5 beginnt für sie neu**. **(2.2) 2d neu:** Bestätigungsperiode beginnt am ersten Handelstag nach Go-Live, **an dem keine vor Go-Live eröffnete Position mehr offen ist** — Ablesung am Buch statt Schätzung. **(2.3) 3b neu:** Symbolzahl entsteht aus einem **Trockenlauf des Laufcodes** (`--nur-universum`), ein anderes Werkzeug ist unzulässig; `MIN_HISTORY_DAYS` fest für alle Rasterzellen. **(5) Ergänzung:** Der Lauf liest **nur Dateien**, kein Modul ruft Kurse über das Netz ab — damit ist der Hash trotz yfinance wieder eine Festschreibung |
| **TB-38** | erledigt (Cloud) 15.09.2026, Mac-Lauf offen — Befunde im Archiv (`BACKLOG_ARCHIV.md`, Abschnitt „Aus Abschnitt 2 — die neun ERLEDIGT-Zeilen"; verschoben 20.09.2026, TB-60) |
| **R1** | ⚠️⚠️⚠️ **REGISTERTEXTE 6 UND 7 STEHEN NIRGENDS IM REPO — unser Versäumnis, von TB-39 gefunden (B1).** Fable lieferte sie **nach** TB-36; TB-36 hat 0–5 eingetragen. **6 (Budgetstufen-Leiter) und 7 (Backtester-Prüfung) existieren seither nur im Chat und hier.** TB-39 hat sie deshalb **nachgebaut** und korrekt dazugeschrieben, dass die Betreiberfassung gilt und die Passage zu **ersetzen**, nicht zu ergänzen ist. ⚠️ **Systemisch, kein Einzelfall: jede künftige Aufgabe rät sie erneut, und jede etwas anders.** **Einzutragen, bevor die nächste Aufgabe formuliert wird** — mit **2d-Deckel** (P95+1 = 13, T38.2), **Kandidatenregeln** (K4), **Zellenbudget** (K2) und **Regulierungsschranke** (K11) |
| **T39.3** | ⚠️ **Buchungsfrage: TB-39 addiert „N gesamt, nominal 658".** Nach Fables Regel (K4) werden **Kandidaten nie gegeneinander gerankt** — dann gibt es keine Summe, sondern **Familienbuchführung**: zwei Kandidaten, je N = 1 bzw. 5. **Die Summe unterstellt einen Auswahltopf, den es nach der Regel nicht gibt.** Beim Registereintrag klären |
| **T39.4** | ⭐ **Meine Kostensorge war zu gross, und die Rechnung zeigt warum:** `Jahresumschlag = n · w · (1/n) = w` — **die Instrumentenzahl kürzt sich heraus.** Umgeschlagen wird nur, **was kippt**. Jahreskosten **0,15–0,90 pp**, obere Schranke **1,80 pp** — halb so viel wie die Hürde, an der `S-E2` scheiterte (3,60). ⚠️ `w` wird bewusst **nicht** gemessen, das wäre der Backtest |
| **T39.5** | **Offene Befunde aus TB-39:** **B3** — Rastergrenzen ruhen auf `datenfrequenz` statt auf einer Messung; die Neuselektion verlangt Grenzen über **gemessene** Grössen, aber eine Messung an den ETF-Reihen **wäre** die verbotene Beobachtung vor der Registrierung. Als Abweichung A1 eingetragen. **B4** — bei fünf Rasterpunkten sind **zwei Kanten**; die Plateau-Regel hat dort nur einen Nachbarn. **B6** — die Korrelation gegen das Neuner-Buch bekommt **keine Schwelle** (Höhe wäre Geschmack, und das Neuner-Buch ist selbst beweglich): **berichtet, nicht bewertet** |
| **TB-39** | erledigt (Cloud) 16.09.2026, PR #112, Datenlauf am Mac offen — Befunde im Archiv (`BACKLOG_ARCHIV.md`, Abschnitt „Aus Abschnitt 2 — die neun ERLEDIGT-Zeilen"; verschoben 20.09.2026, TB-60) |
| **T39.1** | ⚠️ **Die ETF-Kandidatenliste wird HEUTE zusammengestellt** — also mit dem Wissen, welche ETFs es heute noch gibt. **Dieselbe Survivorship-Verzerrung wie bei den Aktien**, mit vorhergesagter Richtung ins Register, nach dem Muster von Registertext 3c |
| **F1a** | ⭐⭐⭐ **FABLE 16.09.: Registertext 5 NEU — der Konflikt ist ein Ordnerproblem.** **Unsere Neigung (kein Cron) ist abgelehnt**, mit einem Argument, das wir nicht hatten: **Registertext 7 (Backtester-Vergleich) braucht den Dateiweg auf der Live-Seite** — solange die Bots live abrufen, existiert von ihrer Eingabe **keine Kopie**, und der Vergleich prüft gegen etwas, das nicht mehr nachsehbar ist. ⇒ **Zwei Bestände:** `data/live/` (täglich per Cron, Frischeprüfung; Forward-Tests **und** Registertext 7 lesen daraus) und **`data/snapshots/<hash>/`** (einmal erzeugt, **unveränderlich**; **nur** der Selektionslauf liest daraus). **Der Registerhash bezeichnet den Snapshot**, der Live-Bestand wird nicht registriert. **Snapshot am Tag des signierten Tags ziehen; ein zweiter Snapshot ist ein neuer Lauf.** ⭐ **Alle Daten- und Bot-Cronjobs auf `TZ=UTC`** (Folge aus dem Ortszeit-Fund) |
| **F1b** | ⚠️⚠️ **EINWAND: „Ein Ordnerproblem" verdeckt einen grossen Umbau.** **101 Module lesen `data/`** (aus TB-34 gemessen) — Backtests, Optimierer, `research/`, Ergebniskurven, Determinismusprüfung. **Und die Definition des Datenstand-Hashes ändert sich mit**, also auch die frisch eingetragene Tatsachennotiz. ⚠️ **Sein Reproduktionstest verlangt eine zweite Maschine — es gibt eine (G1).** ⭐ **Lösung für beides: Snapshot INS REPO, dann ist die Cloud die zweite Maschine** — der Lauf ruft nichts über das Netz ab, die Egress-Sperre ist kein Hindernis; Preis ~56 MB. **Neue eigene Aufgabe, konkurriert mit TB-30b um dieselben 88 Tage — die Stelle, an der der Zeitplan kippen kann** |
| **F2** | ⭐⭐ **Registertext 6, Zellenbudget — das Prinzip: „Die Leiter bewegt Bots. Sie bewegt keine Zellen."** OOS-Evidenz über einen Bot ist Evidenz über eine **Implementierung**, nicht darüber, dass seine Quelle mehr Kapital verdient; Kapital zwischen Zellen nach Ergebnis zu verschieben wäre **Regime-Allokation durch die Hintertür**. **Aktive Zellen teilen das Buch zu gleichen Teilen** (*die einzige Aufteilung, die kein Ergebnis verwendet*). Innerhalb der Zelle nach **Stufenfaktor: Schatten 0, Grundbudget 1, Bestätigt 2** (Faktor 2 willkürlich). **Aufstieg ⇒ mehr vom Zellenbudget, Zellenbudget unverändert. Abstieg ⇒ Zellenbudget bleibt; wird die Zelle inaktiv, geht es in die statische Benchmark-Position ihrer Anlage, NICHT an andere Zellen** — *sonst würde ein Bot für das Versagen eines anderen bestraft, und das Kapital ginge dorthin, wo es zufällig besser lief*. **Neue Zelle ⇒ alle Anteile sinken; die einzige Umverteilung, und sie folgt aus Zulassung, nicht aus Ergebnis.** **Umsetzung: Multiplikator `m_b` auf die heutige statische Positionsgrösse**, quartalsweise vom Leiter-Skript. **Test: aus jeder der 3⁹ Stufentabellen ein eindeutiger Vektor, ohne Betreibereingabe** |
| **F3a** | ⚠️ **Die Bots müssen `m_b` lesen — ZWEITE Änderung an allen neun `forward_test.py`, wieder freigabepflichtig** (dieselbe Klasse wie TB-38) |
| **T42.1** | ⭐⭐⭐ **DER BEFUND: Die neun `forward_test.py` führten ÜBERHAUPT KEINE Positionsgrösse.** Die Aufgabe fragte, ob der Multiplikator an *mehr als einer* Stelle angreifen müsse — **es war keine**. Die Trade-Tabellen halten Zeiten, Kurse, Stop, `pnl_pct` — **kein Stück, keinen Betrag, keinen Anteil**; die Grösse stand ausserhalb (`ALLOCATION_PCT`, `BINANCE_TESTNET_BETRAG_USDT`). *Eine Zahl, die eine Grösse halbieren soll, braucht eine Grösse.* ⭐ **Erklärt rückwirkend P2** — dass die fehlende Positionsgrösse zugleich den Multiplikator unmöglich macht, war nicht bekannt. **Gelöst: neue Spalte `groessenfaktor`, gefüllt beim Eröffnen, genau eine Stelle je Bot.** Am Ablauf geprüft: 1,0 gegen 0,5, **dieselben Ein- und Ausstiegszeitpunkte**, Spalte für Spalte, alle neun |
| **T42.2** | ⚠️⚠️ **EINWAND: Die neun LIVE-Datenbanken bekommen eine neue Spalte.** In der Cloud lief der Test gegen frische DBs — **auf dem Mac trifft es die echten.** Seit Verfahren B sind sie **die einzige OOS-Evidenz**, **nicht neu berechenbar**, und sie existieren **genau einmal** (T37.2). ⇒ **Vor dem Mac-Lauf: Sicherung aller neun**, wie TB-38 es gemacht hat (dort hinterher als **byteweise identisch** nachgewiesen). **Prüfen, ob der Testauftrag das enthält — sonst von Hand** |
| **T42.3** | ⚠️ **EINWAND: `shared/test_kursdaten.py` wurde von der Aufgabe gelockert, gegen die er schützt.** Er verbot bisher **jede** Änderung an `forward_test.py`; jetzt prüft er, ob ein **Handelsparameter** sich ändert und ob der Satz der aus `live_params.py` geholten Namen gleich bleibt. **Mutationsgeprobt** (Gebühr 0,1 → 0,2 fällt weiterhin auf), `equity_simulation.py` bleibt hart gesperrt. **Sachlich richtig** — die Alternative wäre eine dauerhaft rote und damit tote Wache (T38.9). ⚠️ **Aber es war NICHT Teil der Freigabe.** **Betreiberentscheidung; bei Annahme gehört die Lockerung samt Mutationsprobe ins Journal** |
| **T42.4** | ⚠️⚠️ **NEBENBEFUND mit eigener Aufgabe: Ein leerer Kursrahmen beendet `elliott_wave` und `elliott_wave_stocks` HART.** `IndexError` in `calculate_zigzag` (`highs[0]`) — **der ganze Lauf endet, nicht nur das eine Symbol**; die sieben anderen Bots überspringen und laufen weiter. **Fällt eine Kursquelle für ein einziges Symbol aus, handeln zwei von neun Bots an diesem Tag gar nicht.** ⚠️ Nach TB-42 würde es zwar gemeldet — **aber erst, nachdem der Lauf abgebrochen ist.** **Vor den Selektionslauf**, weil es den Papierpfad betrifft, aus dem die Bestätigungsperiode entsteht |
| **T42.5** | ⚠️ **Die Spalte wird geschrieben, aber von NIEMANDEM gelesen.** Solange Kapitalsimulation und Broker-Brücke sie nicht auswerten, **ändert der Multiplikator faktisch nichts am Handeln**. So freigegeben — **aber das Zellenbudget ist damit auch nach TB-42 nicht wirksam.** Nötig sind **zwei** Aufgaben: die **schreibende** Seite (mit `auswertung.py` auf Verfahren B) **und die wirkende Seite (Auswertung der Spalte) — letztere steht bisher in KEINER Aufgabe** |
| **T42.6** | ⚠️ **Achter Fehler meiner Art:** `shared/test_kursdaten.py` stand in der TB-42-Aufgabe als **„bekannt rot"** — **in der Cloud war er grün (82/82)**. Er wird erst rot, wenn jemand `forward_test.py` anfasst. Die Liste war aus früheren Aufgaben übernommen, ohne sie zu prüfen. *Dieselbe Ursache wie die sieben in Journalblock AX* |
| **T42.7** | **Nebenbefund: Ein Testlauf schrieb in den Projektordner, ohne es zu sagen.** Wurde der Wegwerf-Ordner eines laufenden Tests von aussen gelöscht, legte der Bot `paper_trading_rsi2_mean_reversion.db` im Projektordner an — leer, gitignoriert, entfernt. **Der Lauf meldete nur „0 Trades".** Zwei *fail closed*-Wachen dagegen, gegengeprobt. ⚠️ **Auf dem Mac wichtiger als in der Cloud, weil die Datenbanken dort wirklich existieren** |
| **TB-42** | erledigt (Cloud) 16.09.2026, Mac-Lauf offen — Befunde im Archiv (`BACKLOG_ARCHIV.md`, Abschnitt „Aus Abschnitt 2 — die neun ERLEDIGT-Zeilen"; verschoben 20.09.2026, TB-60) |
| **Q1** | ⭐⭐ **FESTER PUNKT: Fable-Querprüfung ZWISCHEN Auswerter-Umbau und signiertem Tag** (Betreiberentscheidung 17.09.2026). ⚠️ **Nicht früher:** Heute beschreibt das Register an **elf Stellen** Dinge, die der Code nicht kann (16.11) — eine Prüfung jetzt fände genau diese elf. ⚠️ **Nicht später:** Nach dem Tag wäre jede Änderung ein **Amendment**, und der Lauf begänne von vorn. **Fables eigener Vollständigkeitstest ist das Kriterium:** *„Lässt sich das Skript aus dem Register ohne Blick auf ein Ergebnis fertig schreiben? Wenn ja, ist das Register fertig, und dann kommt der Tag."* ⚠️ **Die Frage lautet NICHT „stimmt alles", sondern „was würde diesen Lauf im Nachhinein ungültig machen?"** — *„stimmt alles" liefert Zustimmung, die andere Frage liefert Befunde.* ⚠️ **Und die Klarstellung, die dazugehört: Ein Querchecken sichert das VERFAHREN, nicht das ERGEBNIS.** Nach der Asymmetrie kann der Lauf ohnehin nur ausschliessen — „zu 100 % richtig" ist keine Eigenschaft, die ein Selektionslauf haben kann |
| **Q2** | **Drei unabhängige Prüfungen, die die Fable-Runde NICHT ersetzt** und die vor dem Tag stehen müssen: **(1) Reproduktionstest** aus Registertext 5 — der Lauf auf dem Snapshot muss **auf einer zweiten Maschine bitidentisch reproduzieren**; findet ein Modul, das von woanders liest. ⭐ *Lösung für „zweite Maschine": Snapshot ins Repo, dann ist die Cloud die zweite Maschine (F1b)*. **(2) Leiter-Test** aus Registertext 6 — aus **jeder der 3⁹ = 19 683** Stufentabellen ein **eindeutiger** Multiplikatorvektor, **ohne Betreibereingabe**; *ein Fall, in dem es fragt, ist ein Fall, in dem das Register unvollständig ist*. **(3) Prüfung durch jemanden, der den Auswerter nicht gebaut hat** — steht als Regel in der Arbeitsweise und sollte beim wichtigsten Lauf des Projekts greifen |
| **Q3** | **Sammelliste für die Fable-Querprüfung** (wird bis dahin gefüllt): **E2** Mindestzahl Signale = 20, noch nicht im Register · **T39.3** Familienbuchführung statt N-Summe · **T40.3** Falte mit 3 von 24 Symbolen (beantwortet, Registertext steht) · **T44.5** `fromisoformat` im Live-Pfad — **Registerfrage: darf ein nicht verstandenes Datum zum Abbruch führen?** · **T44.6** Mindest-Python-Fassung des Projekts steht nirgends · **T42.5** die wirkende Seite des Multiplikators fehlt noch · Befunde aus TB-45, dem Datenordner-Umbau und dem Auswerter-Umbau |
| **T45.1** | ⭐⭐ **VIER BEHOBEN, EINER GEMESSEN — und jeder Test fällt auf dem alten Stand durch.** `shared/test_stille_ausfaelle.py` **27/27** (alt: **6 rot**), `shared/test_leeres_symbol.py` **45/45** (alt: **12 rot**), Trockenlauf Teil N (alt: **5 rot**); `test_kursdaten.py` **88/88** (vorher 81), Trockenlauf **356/356** (vorher 332), `test_portfolio_sicht.py` **91/91**. **Die Negativ-Prüfungen bleiben grün** — verschärft wurde nur der **gescheiterte** git-Aufruf. Datenstand vor = nach, `entscheidungskerze.py` unberührt |
| **T45.2** | ⚠️⚠️ **MEINE SORGE ZU `fromisoformat` WAR ÜBERZOGEN — in drei Punkten, gemessen.** **(1)** Betroffen sind **vier von neun** Bots, nicht neun — **der Krypto-Pfad erreicht die Stelle nie**, er rechnet die Kerzengrenze aus dem Intervall. **(2)** ⚠️ **Der Datenordner-Umbau berührt den Weg NICHT** — die Zeitstempel der Kursdateien liest **`pandas`**, `fromisoformat` sieht sie nie; betroffen ist nur der Weg des **Börsenkalenders**. **(3)** Es kommt **genau ein Wert** an: `'2026-09-16T00:00:00'`, **vom Code selbst gebaut** (`f"{tag}T00:00:00"` aus dem NYSE-Kalender) — keine Eingabe von aussen. ⇒ **Nicht knapp in Ordnung, sondern mit Abstand.** ⭐ **Und die Handarbeit am `Z`-Suffix ist der Grund, warum eine der sechs kritischen Formen heute keinen Schaden anrichtet** — nicht Kosmetik |
| **T45.3** | **Der Ausgang, falls es doch einträte:** **kein stiller Rückfall, keine falsche Kerze, kein Abbruch.** Der Fehler landet in der Ladeschleife, die ihn je Symbol abfängt — und weil der Wert für **jedes** Symbol derselbe ist, fällt **jedes** heraus: **Der Bot läuft zu Ende und handelt an dem Tag gar nicht.** ⚠️ *In den Zahlen sieht „alle 150 Symbole ausgelassen" genauso aus wie „kein Signal". Sichtbar nur in 150 Logzeilen, die niemand liest.* ⇒ **Genau die Ausfallform, gegen die TB-45 geschrieben war** |
| **T45.4** | ⚠️⚠️ **ZWEI BEFUNDE, DIE NIEMAND GESUCHT HAT.** **(1) `t3_supertrend` hat denselben harten Stopp wie die Elliott-Bots** — `compute_indicators` bricht auf einem leeren Rahmen mit `IndexError` ab; **es überlebt nur, weil der Aufruf zufällig im `try` der Ladeschleife steht**, und die Meldung nennt dann das Symptom statt der Ursache. **(2) Sechs der neun Bots überspringen ein leeres Symbol STILL** — ⚠️ **widerspricht der Regel, die TB-45 durchsetzen sollte** (*„Ein Lauf, der ein Symbol auslässt, sagt es. Immer."*). **Beides berichtet statt behoben** — Teil 4 war nur für die beiden Elliott-Bots freigegeben. **Eigene Aufgabe** |
| **T45.5** | **Zwei Antworten, die meine Aufgabenstellung korrigieren.** **(1)** ⭐ **Alle fünf git-gestützten Prüfungen in `shared/test_kursdaten.py` sind von der `daten_unberuehrt`-Sorte** — auch die Schleifen über `forward_test.py` und `live_params.py`: *läuft keine Runde, weil die Datei unverändert ist, dann ist kein Handelsparameter verändert, und der Nachweis trägt.* **Meine Unterscheidung war richtig, ihre Anwendung auf diese Datei falsch.** **(2)** Die **Drei-Punkt-Form** löst T38.9, **kostet aber die Sichtbarkeit unkommittierter Änderungen** — in `test_stufen.py` unschädlich (daneben steht `git status --porcelain`), in `test_kursdaten.py` nicht. ⭐ **Der Merge-Basis-Vergleich löst beides** — als Vorlage notiert, nicht gemacht |
| **T45.6** | ⚠️⚠️ **`docs/UMGEBUNGEN.md` HAT BEIM ERSTEN EINSATZ SELBST EINEN FEHLER PRODUZIERT.** Dort steht `node` als **„fehlt in der Cloud"** — in dieser Sitzung war es **vorhanden**, `dashboard/test_dashboard.py` **784/784 grün**. Und `dashboard/test_portfolio_sicht.py` stand als „rot, beide" — **in der Cloud grün (91/91)**, rot ist er auf dem **Mac**, wo die Live-Datenbanken liegen. ⇒ **Richtig ist: „wechselnd — je Sitzung prüfen".** *Die Cloud-Umgebung ist nicht eine Umgebung, sondern eine je Sitzung: Pakete liessen sich in TB-43 nachinstallieren, in TB-39 nicht.* **`UMGEBUNGEN.md` korrigieren.** ⭐ **Dazu ein vorbestehender roter Test, den bisher niemand sah:** `research/elliott_wave_params/test_params.py elliott_wave` — *„Kennzahlen identisch zum Bot-eigenen Raster"*, **auch mit den Fassungen aus `origin/main`**; fällt nur auf, weil er ein Argument braucht und ein Basislauf ihn sonst nie erreicht |
| **T45.7** | ⭐ **EMPFEHLUNG ZU TEIL 5: Weg 3 auf Grundlage von Weg 1 — so lassen und MELDEN.** Ein unlesbares Datum geht über dieselbe Telegram-Leitung wie `entscheidungskerze.melde()`. ⚠️ **Warum NICHT Weg 2** (`strptime` statt `fromisoformat`), obwohl sauberer: **`shared/entscheidungskerze.py` ist seit dem 16.09. 04:42:24Z der Live-Pfad, gegen den Registertext 7 den Backtest vergleicht** — jede Änderung dort ist eine Änderung an dem Objekt, dessen Übereinstimmung gerade gemessen wird, **für ein Risiko, das gemessen nicht existiert.** **Weg 3 ändert am Handeln nichts** (derselbe Typ Bug-Fix wie TB-42 Teil 1, kein Amendment) und behebt genau das, was stört: die Unsichtbarkeit. ⭐ **Weg 2 dann, wenn ohnehin jemand die Datei anfasst — nicht als eigener Anlass.** **Betreiberentscheidung** |
| **T45.8** | **Nebenbefund `os.fstat` aus TB-44 beantwortet:** Auf **allen fünf** Fassungen (3.9–3.13) ist `os.fstat` ein `builtin_function_or_method`, und **kein Klassenrumpf** der durchsuchten Standardbibliothek bindet es. ⚠️ **Heute stabil — aber aus demselben Grund, aus dem `_ist_geraet` harmlos war: Zufall der Umstände, nicht des Entwurfs.** *Genau die Bedingung, an der es hängt, hat sich bei `pathlib._NormalAccessor` zwischen zwei Fassungen geändert.* **Unterschied zu TB-44:** dort produktiver Schutzcode, hier ein **Test** — bricht er, wird er rot und lässt nichts still durch. **Empfehlung: dieselbe `_Wache`-Hülle benutzen**, dann ist die Frage gegenstandslos statt je Fassung neu zu beantworten. Nicht dringend |
| **TB-45** | **FORMULIERT 17.09.2026** — `CLOUD_TB-45_stille_ausfaelle.md`, Cloud. **Fünf stille Ausfälle in einem Zug**, alle aus TB-42/43/44. **Teil 1** `shared/test_kursdaten.py:438` — git-Rückgabewert ungeprüft, `rc=128` und trotzdem „bestanden"; ⚠️ **nur die Prüfungen verschärfen, bei denen ein leeres Ergebnis das FEHLEN eines Nachweises ist** — bei `daten_unberuehrt` **ist** es der Nachweis. Dazu: löst die **Drei-Punkt-Form** T38.9? **Teil 2** `dashboard/test_portfolio_sicht.py:217` — Fehler ausdrücklich als Erfolg. **Teil 3** `_ist_geraet` liefert True für **jedes Verzeichnis**; heute kein Loch (gemessen), aber ⚠️ *käme `chmod`/`utime`/ein Kopiervorgang dazu, würde der „Gerät"-Zweig sie durchwinken*; plus **B2 unabhängig vom Umgebungszustand** machen. **Teil 4** ⚠️ **freigegeben:** leerer Kursrahmen beendet `elliott_wave` und `elliott_wave_stocks` **hart** — künftig überspringen und melden, wie bei den sieben anderen; **nur das**, keine Signallogik. **Teil 5** `fromisoformat` im Live-Pfad — ⚠️ **misst und berichtet, ändert NICHT**; eine Änderung an der Entscheidungskerze braucht eigene Freigabe. **Vorarbeit für den Datenordner-Umbau**, weil Teil 1 genau die Wache betrifft, die dort „keine Kursdatei verändert" prüfen soll |
| **U1** | ⭐ **`docs/UMGEBUNGEN.md` FORMULIERT 17.09.2026** (`UMGEBUNGEN.md` + `CLAUDE_md_zeilen.md`) — setzt **T44.7** um. Tabelle **Mac gegen Cloud**: Python **3.9.6** gegen **3.11+**, `dateparser` 1.2.2 gegen 1.4.3, `pandas`/`numpy`, Binance und yfinance **in der Cloud gesperrt**, ⚠️ **`node`: Vermerk FALSCH — siehe T45.6**, ⚠️ **`gh` und Homebrew fehlen auf dem Mac** (daher lokale Merges, **E5**), GNU `timeout` fehlt, **Live-Datenbanken nur auf dem Mac**, `logs/` und `results/<bot>` in der Cloud nicht vorhanden. Dazu die **bekannten Verhaltensunterschiede** (`_NormalAccessor`, `fromisoformat`, `utcnow`, **C-Funktion gegen Python-Funktion als Deskriptor**) und die **Regel für Aufgabendokumente** — ⚠️ *bekannt rote Tests immer **mit Angabe des Rechners**, mehrere Listen waren falsch, weil sie unbesehen übernommen wurden*. **Plus ein Verweisblock für `CLAUDE.md`** — die einzige Datei, die jede Sitzung automatisch liest. **Vom Betreiber abzulegen; eine Sitzung kann es nicht selbst eintragen** |
| **T44.8** | ⭐ **MAC-LAUF TB-44: Die Reparatur hält auf Python 3.9.6.** Alter Stand fällt in **beiden Richtungen** durch, neuer Stand **alle sechs Zeilen wie erwartet**; echte Kette **9/9 Bots geladen**, kein `TypeError`, kein Schreibversuch; Tabellen **0** gegen 16.1.1 und **8** gegen 15.5; Registernachtrag `Quelle beleg: trockenlauf`, **kein Befund**; Datenstand identisch, `git status` leer. **Teile K, L, M — der TB-44-Gegenstand — vollständig grün** |
| **T44.9** | ⚠️ **Der eine Fehlschlag B2, und er erklärt rückwirkend TB-43:** `_ist_geraet()` liefert `not S_ISREG` — **True für JEDES existierende Verzeichnis**, nicht nur für Zeichengeräte. Auf dem Mac existieren `results/<bot>` und `logs/<bot>` (Cron läuft dort) ⇒ gelten als „erlaubt" ⇒ der `makedirs`-Versuch wird **nicht aufgezeichnet** ⇒ B2 findet seinen Beleg nicht. In der Cloud fehlen die Ordner ⇒ grün. ⭐ **Damit ist erklärt, warum TB-43 im Wegwerf-Arbeitsbaum 70/70 erreichte, im echten Checkout aber 68/70** — die zwei Fehlschläge waren B0 (pathlib) und B2. **Kein Schutzloch, gemessen:** `makedirs(exist_ok=True)` No-op, `mkdir` wirft, `open(dir,"w")` EISDIR, und `rmdir`/`rename`/`unlink`/`rmtree` sind **bedingungslos verboten** |
| **T44.10** | ⚠️ **MEIN EINWAND: `_ist_geraet` heisst nicht, was es tut.** Eine Funktion namens „ist ein Gerät", die für **jedes Verzeichnis** True liefert, führt den nächsten in die Irre, der die Wache erweitert. **Die Sicherheit ruht derzeit allein darauf, dass `_verboten` alles Gefährliche abdeckt und dass man in ein Verzeichnis nicht als Datei schreiben kann.** ⚠️ **Käme eine Operation dazu, die auf ein Verzeichnis wirken kann** (`chmod`, `utime`, ein Kopiervorgang hinein), **würde der „Gerät"-Zweig sie durchwinken.** *Dieselbe Familie wie alles andere heute: eine Prüfung, deren Name etwas anderes verspricht als ihr Verhalten.* **Abhilfe von der Sitzung vorgeschlagen, nicht umgesetzt:** `_ist_geraet` auf `S_ISCHR`/`S_ISBLK`/`S_ISFIFO` einschränken, oder den Versuch **vor** der Erlaubnisprüfung aufzeichnen. **Dazu: B2 selbst hat einen Entwurfsfehler** — *„B2 sollte nicht davon abhängen, ob die Bots in diesem Checkout schon gelaufen sind"* |
| **T44.11** | **Zum Abbruchkriterium:** Der Testauftrag verlangte bei einem Fehlschlag Abbruch; die Sitzung führte die Schritte 4–7 **trotzdem** aus (sie verändern nichts, B2 betrifft nachweislich nicht die Reparatur) und dokumentierte die Begründung. ⭐ **Entscheidung richtig** — ohne sie wüssten wir nicht, dass die echte Kette durchläuft. ⚠️ **Sollte die Ausnahme bleiben:** *Ein Abbruchkriterium, das mit guter Begründung übergangen wird, ist beim ersten Mal Urteilskraft und beim dritten Mal Gewohnheit.* **Richtiger: das Kriterium schärfen — Abbruch nur bei Fehlschlägen, die den Gegenstand der Aufgabe betreffen** |
| **T44.1** | ⚠️⚠️ **DER PATCHVORSCHLAG WAR FALSCH — gemessen.** Auf **Python 3.10** steht im Accessor nicht `os.open`, sondern **`io.open`**; `_NormalAccessor.open = staticmethod(wach_os_open)` hätte dort die **falsche Signatur** eingetragen und `Path.open("r")` **erst recht gebrochen**. **Verworfen.** *Die Mac-Sitzung hatte ihn korrekt als Vorschlag markiert — er war auf der Fassung richtig, die sie vor sich hatte, und auf der nächsten falsch* |
| **T44.2** | ⚠️⚠️⚠️ **DER BEFUND HATTE ZWEI RICHTUNGEN — TB-43 hat die gefährlichere übersehen, und sie korrigiert T43.1.** `pathlib` **vor** der Wache importiert: auf **3.9** legte `Path.touch()` die Datei **wirklich** an und `Path.mkdir()` das Verzeichnis **wirklich**; auf **3.10** schrieben `Path.open("w")` und `Path.write_text()` **wirklich**. `pathlib` **nach** der Wache: alles bricht ab, auch lesend. **Ab 3.11 beides in Ordnung.** ⇒ **Ein Abbruch fällt auf, ein stilles Schreiben nicht** — und die „vor"-Reihenfolge ist **genau die, in der der echte Trockenlauf läuft** und die **Teil K prüft**. **Teil K blieb grün** (13/13 auf dem alten Stand, nachgemessen). ⚠️ **Damit war der Schreibschutz auf dem Mac nie vollständig — weder vor noch nach TB-43** |
| **T44.3** | ⭐⭐ **DIE URSACHE HAT NICHTS MIT `pathlib` ZU TUN.** `os.open`/`io.open` sind **in C** geschrieben, Typ `builtin_function_or_method` — **kein Deskriptor**: im Klassenrumpf kommen sie unverändert zurück. **Eine Python-Funktion IST ein Deskriptor** und wird dort zur **gebundenen Methode**, die allen Argumenten die Instanz voranschiebt. ⇒ *Die Wache hatte das **Bindungsverhalten** geändert, nicht den Schreibschutz; `pathlib` war nur der erste Ort, an dem es auffiel.* **Reparatur: Wache als aufrufbare INSTANZ (kein Deskriptor) + `_bindungen_nachziehen` über IDENTITÄT.** Beide ohne ein Wort über `pathlib` ⇒ greifen auf 3.8–3.13 |
| **T44.4** | ⭐ **Zwei Löcher, die AUCH AUF 3.11 offen waren und die TB-43 nicht erfasste:** `bz2._builtin_open` und `tokenize._builtin_open` halten je eine **eigene Kopie** von `open`. Stehen jetzt im Bericht des Laufs (`bindungen_nachgezogen`). **Der Schutz ist dichter als je zuvor, nicht nur wieder heil.** ⚠️ **Und Teil M fand Unerwartetes: die beiden Wachen sind NICHT unabhängig** — fehlt die Hülle, arbeitet auch das Nachziehen falsch (als `M1c` festgehalten). Umgekehrt gilt es nicht |
| **T44.5** | ⚠️⚠️ **FUND IM LIVE-PFAD: `shared/entscheidungskerze.py:323` — `dt.datetime.fromisoformat`.** **3.11 akzeptiert viel mehr Schreibweisen als 3.9** (gemessen: `20260916T120000`, `2026-W38-3`, Nanosekunden, Dezimalkomma → auf 3.9 `ValueError`). **Das ist die Funktion, die ALLE NEUN BOTS seit dem Umstellungstag benutzen.** Heute harmlos (festes Format in den Kursdateien, `Z`-Suffix von Hand abgefangen) — ⚠️ **aber eine Falle, die zuschnappt, sobald sich ein Datenformat ändert, und der Datenordner-Umbau steht als Nächstes an.** Dazu: **`system/test_log_rotation.py:599` ersetzt `os.fstat` durch eine Python-Funktion — dasselbe Muster, heute harmlos**, und **`datetime.utcnow` an 34 Stellen** (seit 3.12 verwarnt, Entfernung angekündigt — ein Termin, kein Fehler) |
| **T44.6** | ⚠️ **DIE LÜCKE, AUS DER ALLES ENTSTAND: Die Mindest-Python-Fassung des Projekts steht NIRGENDS.** Kein `python_requires`, keine `sys.version_info`-Prüfung, keine Festlegung. **Zu entscheiden** |
| **T44.7** | ⭐ **VORSCHLAG zum Versionsvermerk, nicht ausgeführt (`docs/projektfuehrung/` war unberührt):** ein neues **`docs/UMGEBUNGEN.md`** mit Tabelle Mac gegen Cloud (Python, `pandas`, `dateparser`, gesperrte Endpunkte, fehlende Pakete) plus dem Satz **„Grün in der Cloud heisst strukturell nicht grün auf dem Mac."** — und **eine Zeile in `CLAUDE.md`**, die darauf verweist. **Begründung gegen `ARBEITSWEISE.md`:** *dort stehen stehende Anforderungen des Nutzers; eine Umgebungstatsache ändert sich, wenn sich ein **Rechner** ändert, nicht wenn sich die **Arbeitsweise** ändert.* **Begründung für `CLAUDE.md`:** *die einzige Datei, die jede Sitzung automatisch liest.* ⚠️ **Die Tatsache steht bereits im Repo — aber `docs/UEBERGABEPROTOKOLL.md` nennt 3.9.6 als Eigenschaft der IBKR-Brücke, nicht des Projekts; die Cloud-Fassung steht verstreut am Fuss einzelner Dokumente. Nirgends beide zusammen, nirgends die Folgerung** |
| **TB-44** | erledigt (Cloud) 16.09.2026, Mac-Lauf offen — Befunde im Archiv (`BACKLOG_ARCHIV.md`, Abschnitt „Aus Abschnitt 2 — die neun ERLEDIGT-Zeilen"; verschoben 20.09.2026, TB-60) |
| **T43.7** | ⚠️⚠️⚠️ **TB-43 NICHT MERGEN, WIE ES IST — die neue `os.open`-Wache bricht auf Python 3.9 jeden `pathlib`-Zugriff, auch LESENDE.** **Cloud 70/70, Mac 68/70.** Ursache: Python 3.9 hat `pathlib._NormalAccessor.open = os.open`, **gebunden beim Import von pathlib**; wird pathlib im Kindprozess **nach** dem Einschalten der Wache importiert, wird `wach_os_open` zum **Klassenattribut** ⇒ gebundene Methode ⇒ Argumente verrutschen ⇒ `TypeError`. **Ab 3.11 gibt es `_NormalAccessor` nicht mehr** — deshalb sieht die Cloud es nicht. **Echte Kette:** `elliott_wave_stocks` → `yfinance` → `curl_cffi` → `Path().read_text()`. **Fix liegt als 9-Zeilen-Patch vor** (`07_zusatz_patchvorschlag.diff`, in einem Wegwerf-Arbeitsbaum geprüft, **nichts committet**): pathlib vor der Wache importieren und `_NormalAccessor.open = staticmethod(wach_os_open)` setzen. **Damit auf dem Mac 70/70, Tabellen 0 / 8, `Quelle beleg: trockenlauf`, kein Befund** |
| **T43.8** | ⭐⭐ **DIE BEOBACHTUNG, DIE DEN KREIS SCHLIESST — von der Sitzung selbst:** *„Teil K besteht trotzdem, weil dort pathlib schon geladen ist, bevor die Wache angeht. **Teil K sieht diesen Fall also nicht — auch das ist eine blinde Stelle.**"* **Der Test gegen blinde Wachen hat selbst eine blinde Stelle.** ⇒ **Die fehlende Prüfung ist wichtiger als der Patch:** eine, die pathlib **erst NACH** der Wache importiert. Ohne sie fällt derselbe Fall beim nächsten Umbau wieder durch |
| **T43.9** | ⚠️⚠️ **SYSTEMISCH UND NEU: Mac und Cloud laufen auf VERSCHIEDENEN Python-Versionen.** Mac **3.9.6**, Cloud **3.11 oder neuer** — und `pathlib` hat sich zwischen beiden genau an dieser Stelle geändert. **Bisher standen in den Umgebungshinweisen nur fehlende Pakete und gesperrte Endpunkte.** ⇒ **„Grün in der Cloud" heisst strukturell NICHT „grün auf dem Mac"**, und der Mac ist der Rechner, auf dem es zählt. **Gehört in die Umgebungshinweise jeder künftigen Aufgabe.** *(Nebenbei: auch `dateparser` unterscheidet sich — Mac 1.2.2 nimmt den fraglichen Aufrufweg, Cloud 1.4.3 nicht mehr.)* **Offene Frage: Wie prüft man einen Fall, der nur auf 3.9 auftritt, in einer 3.11-Umgebung? Vermutlich nachstellen statt Version treffen** |
| **T43.10** | ⭐ **DIE REGEL „ERST MAC-LAUF, DANN MERGE" HAT SICH AM ERSTEN TAG BEZAHLT GEMACHT.** Eingeführt 16.09. nach T41.7 (TB-40 ohne Mac-Lauf gemergt). **Hätten wir TB-43 nach dem Cloud-Ergebnis gemergt, läge jetzt ein Werkzeug in `main`, das auf dem Mac bei zwei von neun Bots abbricht** — ausgerechnet das Werkzeug, das die Registerzahlen misst. **Zweiter Fall an einem Tag, in dem der Mac etwas fand, das die Cloud strukturell nicht sehen konnte** |
| **T43.1** | ⚠️⚠️ **DER SCHREIBSCHUTZ WAR AN VIER STELLEN LÖCHRIG, nicht an einer.** Der gemeldete `TypeError` war nur das **sichtbare** Symptom. Auf dem alten Stand entstanden **wirklich Dateien** über `io.open`, `pathlib.Path().open`, `Path().write_text` und `os.open`. ⭐ **Ursache:** `builtins.open is io.open` ist wahr — aber **zwei Namen für dasselbe Objekt**; den einen zu ersetzen lässt den anderen unberührt, und `pathlib` geht über `io.open`; `os.open` lag darunter und war **nie** bewacht. **Jetzt alle sieben Wege abgefangen** ⚠️ **— gemessen NUR auf Python 3.11; auf 3.9/3.10 ging `Path().write_text` in der echten Reihenfolge weiterhin durch, siehe T44.2**, Zeichengeräte (`/dev/null`) ausgenommen — *am Verhalten geprüft, weil `python-binance` sie lesend-schreibend öffnet und der Trockenlauf sonst abbricht*. ⚠️ **Mein Einwand war die falsche Sorge:** Ich befürchtete, die Reparatur könnte ein Loch reissen — die Löcher waren schon da |
| **T43.2** | ⭐⭐ **ZWEI MEINER DREI VORSCHLÄGE ZU FEHLER 2 LÖSEN IHN NICHT — nachgemessen.** **`git merge-base`:** bei einem **gemergten** Zweig ist `merge-base(HEAD, origin/main)` der **eigene Commit**, der Diff bleibt leer; es löst die *andere* Fehlerart (TB-34). **Ausdrückliche Basis verlangen:** wer eine gemergte Basis angibt, bekommt denselben leeren Diff und dieselbe stille Grün-Meldung. **Gewählt: leeren Vergleich melden** — Rückgabewert 1. ⭐ **Und die Unterscheidung, die ich nicht gemacht hatte:** Bei `daten_unberuehrt` **ist** ein leeres Ergebnis der Nachweis („nichts verändert" ist der Sollzustand); bei `null_entfernte_zeilen` ist es das **Fehlen** eines Nachweises. *Hätte ich „leerer Vergleich = immer Fehler" vorgegeben, wäre die erste Prüfung kaputtgegangen* |
| **T43.3** | ⚠️⚠️ **DRINGENDSTE der drei berichteten Wachen: `shared/test_kursdaten.py:438` prüft den git-Rückgabewert nicht.** Nachgemessen mit kaputter Referenz: **`rc=128`, trotzdem „bestanden"** — und die `live_params.py`-Schleife erzeugt dann **null Prüfungen**, ohne dass es auffällt. ⚠️ **Das ist derselbe Prüfer, den TB-42 heute gelockert hat (E4)** — *zwei Änderungen an derselben Wache an einem Tag, in entgegengesetzte Richtungen der Sicherheit.* **Nicht geändert (`shared/` ausgenommen), berichtet** |
| **T43.4** | **Zwei weitere Fundstellen, berichtet statt geändert:** `dashboard/test_portfolio_sicht.py:217` behandelt einen **gescheiterten git-Aufruf ausdrücklich als Erfolg** (`returncode != 0 or not stdout.strip()`) — derselbe blinde Fleck, bewusst hingeschrieben. `research/fib_score_stufen/test_stufen.py:244` **macht es richtig** (Drei-Punkt-Form gegen die Merge-Basis, mit Kommentar zur TB-34-Auflösung), nur der Rückgabewert bleibt ungeprüft. **Und `research/faltenplan_neun/test_faltenplan_neun.py:180`** liest die als „ERSETZT" gekennzeichnete Tabelle **15.5** — heute sachlich richtig (Lesart A gegen Lesart-A-Tabelle), **aber er sagt nicht, welche** |
| **T43.5** | ⭐⭐ **T41.6 IST GESCHLOSSEN.** In der Cloud liessen sich diesmal `pandas`, `python-binance` und `yfinance` installieren ⇒ `pruefe_register.py` lief **gegen eine frische Messung** statt gegen das committete Dokument und **bestätigt die TB-41-Zahlen in 16.1.1 vollständig** — unabhängig von der Diagnose-Kopie. **Und der Tabellenwechsel ist zweiseitig nachgewiesen:** gegen **16.1.1 null** Abweichungen, gegen **15.5 acht**, bei **zeichengleichen** Messwerten. *Damit ist belegt, dass das Werkzeug die Tabelle wirklich wechselt und nicht bloss schweigt* |
| **T43.6** | ⚠️ **Fehler 1 ist in der Cloud NICHT über die echte Kette nachweisbar** — die dort installierte `dateparser`-Fassung **1.4.3** nimmt den fraglichen Aufrufweg nicht mehr. **Auf dem Mac tut sie es.** ⇒ **Der Mac-Lauf ist hier nicht optional**, Erwartung `test_universum_trockenlauf.py` von 10/20 auf grün |
| **TB-43** | erledigt (Cloud) 16.09.2026, Mac-Lauf offen — Befunde im Archiv (`BACKLOG_ARCHIV.md`, Abschnitt „Aus Abschnitt 2 — die neun ERLEDIGT-Zeilen"; verschoben 20.09.2026, TB-60) |
| **E2** | **BETREIBERENTSCHEIDUNG 16.09.: Mindestzahl Signale in Registertext 7 = 20.** Abgeleitet aus der 95-%-Schwelle: `(n−1)/n ≥ 0,95 ⇒ n ≥ 20` — die kleinste Zahl, bei der **ein** Unterschied kein Durchfallen bedeutet. ⚠️ **Einschränkung, die dazugehört:** 20 ist die Untergrenze, unter der die Prüfung **unsinnig** wäre, nicht die Zahl, ab der sie **aussagekräftig** ist — bei genau 20 verträgt der Test **einen** Unterschied, bei zwei fällt er durch. **40 wäre die komfortable Marke** (verträgt zwei), mit derselben Rechnung. **Gewählt: 20**, weil die Regel ohnehin nur berichtet, was sie nicht bewerten kann, und ein zu hoher Boden mehr Bots in „nicht geprüft" schiebt als nötig. **Muss noch ins Register nachgetragen werden** |
| **T41.6** | ⭐ **MAC-LAUF TB-41: Die eingetragenen Symbolzahlen stimmen auch mit einer FRISCHEN MESSUNG auf dem Mac** — `Quelle beleg: trockenlauf — KEIN BEFUND`, alle neun Punkte, RC 0. ⚠️ **Aber nicht über das Repo-Werkzeug, sondern über eine Diagnose-Kopie ausserhalb des Repos mit drei geänderten Zeilen.** Die Sitzung stellt das ausdrücklich zur Entscheidung. **Meine Einschätzung: zwei verschiedene Behauptungen — „die Zahlen stimmen" ist belegt (echte Daten, echter Loader, echtes pandas; die drei Zeilen betreffen nur den Schreibschutz), „das Werkzeug funktioniert" ist nicht belegt.** ⇒ **Das Register steht; das Werkzeug braucht eine Reparatur** |
| **T41.7** | ⚠️⚠️ **MEIN VERSÄUMNIS: Der TB-40-Mac-Lauf hat nie stattgefunden.** Kein `TB-40_ergebnisse` unter `~/Downloads` — wir haben TB-40 gemergt und sind direkt zu TB-41 weiter, **ich habe den Testauftrag nicht angefordert**. Folge: Die Symbolzahlen wanderten aus einer **Cloud**-Messung ins Register, und dass das Werkzeug auf dem Mac gar nicht läuft, fiel erst durch eine Aufgabe auf, die etwas anderes prüfen sollte. **Gut ausgegangen, aber Glück statt Verfahren.** ⇒ **Arbeitsweise: Mac-Testauftrag VOR dem nächsten Merge anfordern, nicht danach** |
| **T41.8** | ⚠️ **WERKZEUGFEHLER aus TB-40: `loaderlauf.py` läuft auf dem Mac gar nicht.** Der Schreibschutz ersetzt `builtins.open` durch `wach_open(datei, modus="r", *a, **k)`; wird `open(pfad, mode="rb")` mit **Schlüsselwort** aufgerufen, landet `mode` in `**k` und wird **doppelt** übergeben ⇒ `TypeError`. **Kette:** `dateparser` ruft so auf → `python-binance` importiert `dateparser` → `elliott_wave`-Loader importiert `binance.client`. **Folge: Schritt 3 bricht ab, `test_universum_trockenlauf.py` fällt in 10 von 20 Prüfungen.** *In der Cloud unsichtbar, weil dort der Binance-Import ohnehin nicht durchkam.* **Reparatur: drei Zeilen, Patch liegt bei** |
| **T41.9** | ⚠️⚠️ **SYSTEMISCH, zum DRITTEN Mal in drei Tagen: Die Wache gegen gelöschte Registerzeilen ist nach jedem Merge trivial grün.** `pruefe_register.py:556` hat `origin/main` als Standardwert; ist der Zweig gemergt, ist der Diff leer, `numstat: []` — **die Prüfung prüft nichts mehr und meldet Erfolg**. ⭐ **Gefunden nur durch den Selbsttest B2 („der Diff wurde tatsächlich ausgewertet"), der daraufhin fehlschlug: 40/41.** Mit richtiger Basis (`c104abf`): `655 0` / `85 0`, **41/41**. *Eine Wache, die prüft, OB geprüft wurde — genau die Mutationsproben-Regel dieses Projekts.* **Dauerhaft beheben: ausdrückliche Basis verlangen oder leeren Vergleich melden** |
| **T41.10** | ⭐ **DAS MUSTER: drei Werkzeuge, die aufhören zu prüfen, ohne es zu sagen.** `loaderlauf.py` läuft gar nicht (T41.8) · `pruefe_register.py` prüft nach dem Merge nichts mehr (T41.9) · die TB-40-Vergleichstabelle zeigt auf den historischen Stand (T41.2). **Dieselbe Familie wie die drei lautlos aussortierenden Bots (T40.5), und dieselbe Regel: _Ein Werkzeug, das nicht mehr misst, sagt es._** ⇒ **Eine eigene kleine Cloud-Aufgabe wert** |
| **T41.1** | ⚠️ **VIERTER FEHLER, und er ist meiner: „die fünf Werte von `MIN_HISTORY_*`" — es sind VIER.** `17 520` (Kerzen) · `730` · `500` · `1 825` (Tage); drei Krypto-Bots teilen sich die 500. **Ich habe Gruppen gezählt statt Werte.** Stand so in meiner TB-40-Bewertung, im Backlog (T40.4, korrigiert) und in der TB-41-Aufgabenstellung. ⚠️ **Dritter Fehler dieser Art an einem Tag** — nach der Fünf-Minuten-Angabe und dem H/F-Widerspruch. **Alle drei entstanden gleich: eine Zahl aus einem Bericht übernommen oder abgeleitet, ohne sie an der Quelle zu prüfen.** *Die Lehre steht zweimal im Backlog und greift offenbar noch nicht* |
| **T41.2** | ⚠️ **FALLE, die gestellt bleibt:** Das TB-40-Werkzeug liest weiter die **historische** Tabelle in 15.5 und meldet bei einem erneuten Lauf **wieder acht Abweichungen**. Wer den Trockenlauf in vier Wochen nochmal startet, könnte die **bereits korrigierten** Zahlen erneut „korrigieren". **Beheben: entweder auf die neue Tabelle zeigen oder ausdrücklich melden, dass gegen den historischen Stand verglichen wird** |
| **T41.3** | ⭐ **Die letzte offene Zahl ist ABLEITBAR, nicht willkürlich.** Registertext 7 verlangt eine Mindestzahl Signale. Bei Schwelle **95 %** und **einem** Unterschied gilt `(n−1)/n ≥ 0,95` ⇒ **n ≥ 20**. **Vorschlag: 20 Signale** — die kleinste Zahl, bei der ein einzelner Unterschied kein Durchfallen bedeutet (8 ⇒ 87,5 % ⛔ · 15 ⇒ 93,3 % ⛔ · 20 ⇒ 95,0 % ✅). ⚠️ Vorbehalt: Die 95 % selbst bleiben willkürlich; die 20 sind nur **gegenüber den 95 %** ableitbar — *eine abgeleitete Zahl auf einer gesetzten ist immer noch besser als zwei gesetzte* |
| **T41.4** | ⚠️ **Vorbehalt der Sitzung, ernst zu nehmen:** In der Cloud fehlen `pandas`/`numpy`, Binance und yfinance gesperrt ⇒ **die Symbolzahlen wurden gegen das committete TB-40-Ergebnisdokument verglichen, NICHT gegen eine frische Messung**. **Der Mac-Testauftrag holt das nach (Schritt 3) — bis dahin ist die Übereinstimmung eine Dokumentenprüfung, keine Messung.** Der Mac-Lauf ist hier **nicht optional** |
| **T41.5** | **Elf Stellen, an denen Registertext und Umsetzung auseinanderfallen** (Register 16.11): ein Datenordner statt zwei (**101 Module**), kein Leiter-Skript (alle neun rechnen faktisch 1/9), kein Vergleichswerkzeug für Registertext 7, `auswertung.py` kennt nur das alte Embargo und ist eingefroren, drei Bots sortieren lautlos aus, `TZ=UTC` nicht geprüft. *„Ein Register, das etwas beschreibt, das der Code noch nicht kann, ist in Ordnung — solange es benannt ist."* **Jede der elf ist eine bereits freigegebene oder geplante Aufgabe** |
| **TB-41** | erledigt (Cloud) 16.09.2026, Mac-Lauf offen — Befunde im Archiv (`BACKLOG_ARCHIV.md`, Abschnitt „Aus Abschnitt 2 — die neun ERLEDIGT-Zeilen"; verschoben 20.09.2026, TB-60) |
| **E4** | **BETREIBERENTSCHEIDUNG 16.09.2026: Die Lockerung von `shared/test_kursdaten.py` ist angenommen.** Der Prüfer verbot bisher **jede** Änderung an `forward_test.py`; er prüft jetzt, ob ein **Handelsparameter** sich ändert und ob der Satz der aus `live_params.py` geholten Namen gleich bleibt. `equity_simulation.py` bleibt **hart gesperrt**. ⭐ **Belegt durch die Gegenprobe im Mac-Lauf:** `TRADING_FEE_PCT: 0.1 -> 0.2` in `t3_supertrend` wurde gefunden, die acht anderen Bots blieben `[OK]`, Datei danach zurückgesetzt. **Die Wache beisst noch.** Begründung für die Annahme: Die Alternative wäre ein Prüfer, der nach **jeder freigegebenen** Änderung dauerhaft rot ist — und **ein dauerhaft roter Test ist keine Wache** (T38.9). ⚠️ **Festgehalten, weil die Lockerung nicht Teil der ursprünglichen Freigabe war:** Sie kam von derselben Aufgabe, die `forward_test.py` änderte. Angenommen als **bewusste Entscheidung**, nicht als Nebenwirkung |
| **E5** | ⚠️ **Lücke in der Nachvollziehbarkeit, bewusst in Kauf genommen (16.09.2026): TB-42 wurde LOKAL gemergt, ohne Pull Request** — `gh` ist auf dem Mac nicht installiert, die Sitzungen können keinen anlegen, und Homebrew fehlt ebenfalls. Merge-Commit mit `--no-ff` und ausdrücklichem Hinweis im Text. ⚠️ **Die PR-Reihe endet damit bei #114** (TB-41); wer künftig nur die PR-Liste auf GitHub durchgeht, findet TB-42 nicht. **Beim nächsten Mal zu entscheiden: dabei bleiben oder `gh` installieren** |
| **E3** | ⭐ **BETREIBERENTSCHEIDUNG 16.09.2026 zum Termin des Selektionslaufs: „Wir lassen laufen, sobald wir soweit sind."** Der **13.12.2026 ist eine Obergrenze, kein Termin** — er stammt aus der Reparaturfrist vom 13.09. und sollte verhindern, dass die kaputte Kennzahl liegenbleibt. **Der Lauf selbst kostet 3–5 Stunden** (W5b); was Zeit kostet, ist die Vorarbeit: Datenordner trennen, `auswertung.py` auf Verfahren B, Snapshot, signierter Tag — **30 bis 45 Stunden Betreiberzeit**, realistisch zwei bis drei Wochen bei Dranbleiben. ⇒ **Gestartet wird, sobald die Vorarbeit steht, nicht am Stichtag.** ⚠️ **Und die eigentliche Schranke ist nicht der Dezember, sondern 2027:** Der Selektionslauf sagt, **welche Bots ausscheiden und mit welchen Parametern** die übrigen laufen — **nicht, ob sie Geld verdienen.** Dafür braucht es OOS-Evidenz, nach der Leiter frühestens **30 geschlossene Trades und sechs Monate**; bei Median-Haltedauern von 4 bis 21 Tagen ist das bei einigen Bots ein halbes Jahr. **Der Dezember ist der Punkt, an dem die Grundlage stimmt — nicht der, an dem eine Antwort vorliegt.** *Deshalb zählt jeder Tag Papierpfad ab dem Umstellungstag (16.09., 04:42:24Z), nicht ab Dezember* |
| **E1** | ⭐⭐⭐ **BETREIBERENTSCHEIDUNGEN 16.09.2026, alle drei getroffen.** **(1) Aktien/Krypto-Schlüssel: 80/20** — statt Fables 60/40. Begründung aus der Messung: grösster Rückgang praktisch gleich wie 90/10 (−33,9 gegen −33,7 %) bei doppeltem Krypto-Gewicht; nahe am Punkt gleicher Risikobeiträge (**79/21**), also **ableitbar statt willkürlich**; **letzte Stufe, auf der Krypto diversifiziert statt zu dominieren** (ab 70/30 kippt es auf −40,8 %). ⚠️ **Fable wurde bewusst NICHT gefragt** — er hat 60/40 ohne diese Messung vorgeschlagen und selbst als willkürlich markiert; die Frage ist keine methodische, sondern eine der Risikotragfähigkeit. **(2) FREIGABE: die neun `forward_test.py` dürfen den Multiplikator `m_b` aus der Leiter lesen** — Voraussetzung für das Zellenbudget, die Bots entscheiden dadurch nichts anders. **(3) FREIGABE: Logging-Fix in `multi_symbol_optimise.py`** für die drei lautlosen Bots — ändert Sichtbarkeit, kein Verhalten |
| **F4b** | ⭐⭐⭐ **GEMESSEN 16.09.: Der Aktien/Krypto-Schlüssel, 2 271 gemeinsame Handelstage.** **Krypto 74,7 % Jahresschwankung, Aktien 19,6 % ⇒ Verhältnis 3,82 ×.** Korrelation der Körbe **0,32**. Grösster Rückgang Krypto **−82,3 %**, Aktien −35,7 %. ⚠️ **Bei Fables 60/40 kommen 80 % des Risikos aus Krypto** — *keine ausgewogene Aufteilung, sondern eine Krypto-Wette mit Aktien-Beiwerk*. **Gleicher Risikobeitrag beider Seiten bei rund 79/21.** ⭐ **Unerwartet: 90/10 hat einen KLEINEREN grössten Rückgang als 100/0** (−33,7 % gegen −35,7 %) — bei Korrelation 0,32 federt eine kleine Krypto-Beimischung den Aktien-Einbruch ab. **Es kippt zwischen 80/20 (−33,9 %) und 70/30 (−40,8 %).** ⇒ **80/20 bis 90/10: Krypto diversifiziert. Ab 70/30: Krypto dominiert das Risiko.** ⚠️ **Der Ertrag wurde bewusst NICHT gemessen** — der Zeitraum 2017–2026 enthält einen der grössten Krypto-Aufschwünge; eine Renditemessung darauf sagte „mehr Krypto war besser" und wäre genau die Aussage, gegen die dieses Projekt anschreibt. **Risiko ist über Zeiträume einigermassen stabil, Ertrag nicht.** ⚠️ Vorbehalt: gemessen ist Kaufen-und-Halten, nicht das Botverhalten (mittlere Exposure 37,9 %) — **die absoluten Werte sind für das Buch zu hoch, das Verhältnis 3,82 bleibt.** **Entscheidungsvorlage: `ENTSCHEIDUNG_aktien_krypto_schluessel.md`** |
| **F4** | ⚠️⚠️ **DIE GRÖSSTE WILLKÜRLICHE ZAHL IM SYSTEM: der Aktien/Krypto-Schlüssel** (Registertext 6g, Vorschlag **60/40**, von Fable als willkürlich markiert). **Der Selektionslauf wählt Parameter INNERHALB von Bots; dieser Schlüssel entscheidet, wie viel Kapital überhaupt in welche Anlage geht** — bei einem Vielfachen an Volatilitätsunterschied. **Die Wirkung von 60/40 gegen 80/20 ist mit hoher Wahrscheinlichkeit grösser als die des gesamten Dezember-Laufs.** Nie gemessen. **Betreiberentscheidung, vor dem Tag** |
| **F5** | ⭐⭐ **ANTWORT AUF DIE REGIME-IDEE, dreiteilig.** **Tor** (Zellen einer Anlage Richtung Kasse skalieren, feste Literaturregel): **registrierbar, N = 1, gegen die NULL prüfbar — und weitgehend schon eingebaut**, Zugewinn klein. **Umschalten zwischen Quellen: ⛔ nicht registrierbar** — *„Die Historie enthält vielleicht acht Regimewechsel. Eine Regel, die aus acht Beobachtungen lernt, welche von zwei Quellen als Nächstes verdient, hat acht Datenpunkte für eine Frage, für die die Literatur mit Jahrzehnten keine belastbare Antwort hat."* ⚠️ **Und gegen die Idee selbst: Trend UND kurzfristige Umkehr verdienen beide in Hochvolatilitätsphasen mehr — sie mögen dieselben Phasen und lassen sich nicht gegeneinander timen.** **Sprachmodell im Pfad: ⛔ nie.** ⭐ **Der konstruktive Kern: regimeabhängige BERICHTERSTATTUNG** — die Leiter weist je Zelle aus, in welchem Regime sie verdient; ein informativer Agent darf das **beschreiben, nicht daraus handeln**. Nach 2–3 Jahren ist das der Bericht, aus dem sich sagen liesse, ob Umschalten je etwas gebracht **hätte** — **mit Etiketten, die beim Entstehen protokolliert werden statt rückblickend** |
| **F6** | ⭐ **NEUER BEGRIFF: gestapelte Selektion.** Ein Overlay über bereits selektierte Bots wird auf **denselben Daten** geprüft, auf denen die Bots gewählt wurden — sein In-Sample-Ergebnis hängt von dieser Wahl ab. ⇒ **Overlay-Kandidaten erst NACH dem Selektionslauf registrieren, Zulassung über die Bestätigungsperiode statt über die Falten.** Und: **„absolut" heisst gegen die NULL** (das Buch ohne die Regel), nicht gegen eine andere Regel — *„Die Null ist kein Kandidat, sondern der Vergleich, den jeder Kandidat hat."* Fable korrigiert damit seinen eigenen VIX-Vorschlag und erwartet selbst, dass das Tor das Abbruchkriterium knapp oder gar nicht besteht |
| **K23** | **AN FABLE 16.09.: vier offene Punkte** — `FABLE_ANFRAGE_vier_offene_punkte.md`. **(1)** Registertext 5 (*„der Lauf liest nur Dateien im registrierten Zustand"*) kollidiert mit seinem eigenen Punkt 2 (Daten-Cron vor den Bot-Läufen) — **223/223 Dateien veraltet, alle neun Bots fallen täglich zurück**. Unsere Neigung: kein Cron vor dem Lauf, Rückfall-Meldung **als erwartet vermerken**. **(2)** Zellenbudget × Leiter (**K6**): Steigt einer von drei Bots auf Bestätigt — mehr vom Zellen- oder Gesamtbudget? Fällt einer auf Schatten — behält die Zelle ihr Budget oder schrumpft es? **Vor dem Tag.** **(3)** Betreiberfrage zur **regimeabhängigen Gewichtung**, umformuliert zu: *Unter welchen Bedingungen ist sie registrierbar, ohne dass N sich multipliziert?* **(4)** Richtigstellung der Fünf-Minuten-Angabe |
| **K24** | **Betreiberidee 16.09.: „marktsituative Strategieauswahl, KI bewertet den Markt".** **Widersprochen, mit drei Gründen:** Die Idee steckt **dreimal im System** (BTC-Regimefilter bei `t3_supertrend` und `volatility_breakout_crypto`, SMA-150/200 bei den RSI-2-Bots, und `S-B1` ist im Kern eine Regimebewertung). Eine Ebene darüber **multipliziert N**, weil ein Umschalter eigene Parameter hat, die auf **denselben Daten** gewählt werden. **Regime sind im Nachhinein klar und im Moment nicht** — die meisten Belege beruhen auf rückblickend vergebenen Etiketten. ⚠️ Und ein **Sprachmodell im Entscheidungspfad ist nicht reproduzierbar** — gegen die Determinismus-Arbeit und gegen die harte Regel *„kein Agent löst einen Trade oder eine Parameteränderung aus"*; verwandt mit dem bereits verworfenen Sentiment-Handel. **Tragfähig wäre nur die mechanische, vorab festgelegte Form** |
| **K15** | ⚠️⚠️⚠️ **PRIIPS TRIFFT `S-B1` ALS GANZES, nicht nur `S-A2`.** Alle vierzehn Instrumente sind **US-domiziliert** und für einen EU-Privatanleger bei IBKR **nicht handelbar**. **Der Kandidat auf Rang 4 ist in der ausgearbeiteten Form nicht ausführbar** — und **TB-39 hat ihn am 16.09. genau so registriert** (`docs/VORREGISTRIERUNG_S-B1_etf_trendfolge.md`, PR #112). ⚠️ **Nachtrag nötig, BEVOR der Datenlauf startet.** Fable: *„Ich habe das nicht geprüft, und der neue siebte Vorab-Filter hätte es gefunden."* ⇒ **Vorab-Filter 7 bekommt eine zweite Klausel:** nicht nur *darf der Betreiber das handeln*, sondern *ist das KONKRETE INSTRUMENT für ihn zugelassen* — die erste Klausel erledigte Carry, die zweite hätte B1 und A2 erledigt |
| **K16** | **Lösung: Proxy-Handel.** **Signale auf den US-ETFs** rechnen (lange Historie = ihr Wert), **auf UCITS-Gegenstücken handeln**. Je Paar eine Registerzeile mit Korrelationsprüfung der Tagesrenditen, **unter 0,97 ist es kein Proxy**. **Abbruch unter acht handelbaren Paaren über vier Anlageklassen.** ⚠️ **Mein Einwand, von Fable nicht benannt: Die Prüfung läuft auf der GEMEINSAMEN Historie — und die beginnt bei den meisten UCITS-Produkten erst ab 2010.** Geprüft wird in den ruhigen Jahren, verlassen muss man sich in den Krisen, für die der Proxy **nicht prüfbar** ist. **Die Registerzeile muss nennen, AB WANN geprüft werden konnte**, und der Bericht, für welche Bärenepisoden der Proxy ungeprüft bleibt |
| **K17** | ⚠️ **Rang 1 (inverser UCITS-ETF) ist kein „Decay", sondern PFADABHÄNGIGKEIT.** Ein täglich zurückgesetztes Inversprodukt liefert über einen **Monat** nicht die negative Monatsrendite des Index, sondern das Produkt der täglichen Gegenbewegungen — bei −10 % mit starken Schwankungen **deutlich weniger als +10 %**, im Extremfall Verlust. **Trifft ausgerechnet den zerklüfteten Abwärtsmarkt, für den man das Short-Bein baut.** ⇒ **Der Short-Arm darf NICHT als „Index × (−1)" gerechnet werden**, sondern nur auf der **eigenen Kursreihe des Produkts** — die beginnt 2008–2010. ⚠️ **Damit hat der Short-Arm einen ANDEREN FALTENPLAN als der Long-Arm.** Gehört in den Nachtrag |
| **K18** | ⭐ **FRAGE GEKLÄRT: Short ist KEINE eigene Zelle.** Trend long und Trend short sind dieselbe Quelle mit umgekehrtem Vorzeichen — es ist die **Kassenseite der Zellen 1 und 5**, mit Vorzeichen: *„es macht aus ‚draussen sein' eine Position"*. ⇒ **Kein eigenes Zellenbudget, Teil des Sleeve-Budgets.** Klärt einen Teil von **K6**. **Der richtige Test (ohne Backtest):** Short-Signaltage gegen die Tage, an denen `volatility_breakout` und `t3_supertrend` **keine Position halten** — nicht Ko-Einstieg der Signale |
| **K19** | **Registerzeilen für short-fähige Sleeves (Fable):** (a) Short **nur in Indexinstrumenten**, nie Einzelaktien — S&P-Tagessprung historisch ≈ **+12 %**, Einzelaktien **+50 %** und mehr · (b) Notional-Obergrenze **20 %** des Sleeve-Budgets (willkürlich), Stress-Tagesverlust = Notional × grösster historischer Tagesanstieg, **aus den Daten** · (c) Stop **beim Broker**, Simulation nimmt Fill **zum Stress-Sprung** an · (d) Short-Notional zählt als Brutto-Exposure der Anlageklasse · ⭐ **(e) Abbruch unabhängig von jeder Kennzahl:** realisierter Tagesverlust über dem registrierten Stress-Tagesverlust ⇒ Sleeve auf Schatten. *„Keine Leistungsprüfung, sondern die Feststellung, dass das Risikomodell verletzt wurde."* ⇒ **Registertext 6 braucht dafür KEINE eigene Stufe** |
| **K20** | **Rangfolge der Formen (Fable):** **Rang 1** inverser UCITS-ETF **innerhalb von B1** — kein Eingriff ins System, nur ein Instrument mehr · **Rang 2** echtes Short des UCITS-ETF, `notional < 0` **nur in B1s eigener Simulation**; erst nach einer Bestätigungsperiode von Rang 1 · **Rang 3** Modul auf den Signalen der neun — *„Form (c) mit schlechterem Signal"*, nutzt Ausstiegsfilter für Einstiege in die Gegenrichtung · ⛔ **Rang 4 verworfen:** eigener Bot „Fortsetzung short × Aktien" — Einzelaktien-Short, Squeeze-Risiko, dokumentiert schwächere und crashanfälligere Hälfte der Prämie. **Gemeinsames Abbruchkriterium:** Short-Arm gegen Long-only-Arm desselben Sleeves; verworfen, wenn er den Sleeve-Calmar nicht hebt **oder** in den Bärenfalten nicht selbst positiv ist **oder** ausserhalb mehr kostet als Leihgebühr plus Decay. **Kein Raster** — das Short-Signal ist die Umkehrung |
| **K21** | ⭐ **„Es gibt in OHLCV long-only nur eine Quelle von Krisenalpha, und das ist Trend."** Optionen wären die zweite, und die schliesst der Rahmen aus. ⇒ Der Einwand „das Krisenalpha hängt an einem Kandidaten" ist **kein Mangel der Form, sondern eine Eigenschaft des Rahmens**. **Fable räumt ein: Rang 3 war „ein wenig" zu hoch** — die **Vermeidung** (in Kasse sein, wenn Aktien fallen) bekommt man long-only **vollständig**; es fehlt der Short-Aktien-Gewinn, **grob ein Drittel** des Krisenertrags, in Nicht-Krisenjahren nahe null (Grössenordnung, keine Messung). **Für Calmar ist die Vermeidung der grössere Hebel, weil sie den Nenner senkt** |
| **K22** | **Notiz für 2027: Micro-Futures** wären für Cross-Asset-Trend das eigentliche Instrument — echte Short-Seite, keine Leihe, keine PRIIPs-Frage, minimale Kosten. ⚠️ Aber saubere **Roll-Logik ist ein Datenprojekt** ausserhalb des Rahmens, **Margin ein zweites Risikomodell**. Von Fable ausdrücklich als **der richtige Weg für 2027** genannt, nicht als Ausweg jetzt |
| **K12** | **AN FABLE 16.09.: Long-only neu bewerten** — `FABLE_ANFRAGE_shortbein.md`. Er hatte long-only auf **Rang 3** gesetzt, Preis der Öffnung „hoch". **Der Preis war an einer falschen Annahme bemessen:** Über **IBKR** kann der Betreiber Aktien **direkt leerverkaufen**; Optionen und Futures sind nach Freischaltung einer Handelsberechtigung handelbar. **Gefragt: ändert das die Rangfolge, und was ist der kleinstmögliche Eingriff für ein Short-Bein?** Drei Formen vorgelegt: (a) eigener Bot „Fortsetzung short × Aktien" = Zelle 9 · (b) Modul wie `S-A2`, das nur die Regimephase nutzt — hängt aber an den Signalen der neun, also **nicht unabhängig** · (c) nur als Sleeve von `S-B1`. **Die eigentlichen Fragen:** Ist Short überhaupt eine eigene Zelle, oder dieselbe Quelle mit umgekehrtem Vorzeichen — *was heisst „unkorreliert", wenn die Antikorrelation eingebaut ist?* ⚠️ **Wie registriert man eine Strategie, deren Verlust nicht begrenzt ist?** Leiter und Abbruchkriterien rechnen mit einem nach unten begrenzten Kapitalpfad. Und: wieviel Krisenalpha bleibt long-only übrig — dann wäre Rang 3 **zu hoch** angesetzt |
| **K13** | ⚠️ **HEBELPRODUKTE SIND HANDELBAR, ABER NICHT REGISTRIERBAR.** Optionsscheine, Knock-outs, Faktor-Zertifikate: **keine durchgehende Kurshistorie** (verfallene Scheine), **Emittent stellt den Preis selbst**, Spanne hat mit den 0,30 pp nichts zu tun. *Ein Kandidat, den man nicht backtesten kann, kann nach den Projektregeln nicht zugelassen werden.* **Und ein Hebel erzeugt keine Zelle** — er skaliert eine vorhandene Wette samt Drawdown. ⭐ **Was der IBKR-Zugang lockert, ist Richtung, nicht Grösse.** Echte Optionen wären standardisiert und hätten Historie, aber der Rahmen schliesst Optionsdaten und implizite Volatilität aus — das wäre Datenbeschaffung, keine Strategie |
| **K14** | ⚠️ **`S-A2` (Inverse-ETF-Modul von `S-B1`) steht auf unsicherem Grund.** **US-domizilierte ETFs sind für EU-Privatanleger gesperrt** (PRIIPs, fehlendes Basisinformationsblatt) — **auch die gehebelten und inversen**. Sieht `S-A2` US-Ticker vor, ist es nicht handelbar. UCITS-Varianten existieren, mit **kürzerer Historie** — und Historie ist bei `S-B1` die bindende Grösse (Untergrenze: 8 Instrumente / 4 Anlageklassen ab 2007). **Gehört in TB-39 geprüft** |
| **K10** | ⛔ **ZELLE 7 (FUNDING-CARRY) IST TOT — verworfen am 16.09.2026, Grund: Regulierung.** Der Betreiber kann aufgrund seines **Wohnsitzes in Deutschland auf Binance keine Derivate handeln.** Damit ist die Strategie **nicht ausführbar** — unabhängig von Methodik, Sicherheitsarchitektur und Ergebnis. **Der von Fable vorgeschlagene Carry-Backtest entfällt ersatzlos:** Er war ausdrücklich damit begründet, dass ein positives Ergebnis später die Frage nach der Ausführungsschranke stellen würde; diese Frage **kann sich nicht mehr stellen**. Ein registrierter Lauf für eine nicht handelbare Strategie kostet N, Rechenzeit und Aufmerksamkeit und zeigt bestenfalls, dass etwas funktioniert hätte, was der Betreiber nicht darf. ⚠️ **Nicht erneut vorschlagen.** *(Schliesst auch `S-B2` endgültig, das bisher nur an der Spot-Beschränkung scheiterte.)* |
| **K11** | ⭐ **DIE SIEBTE SCHRANKE, die in keiner Liste stand: Regulierung am Wohnsitz.** Sie hat am 16.09. einen Kandidaten erledigt, **bevor** Aufwand hineinfloss. **Gehört als Vorab-Filter in die Kandidatenregeln (K4)**, neben den Ko-Einstiegstest: *Darf der Betreiber das überhaupt handeln?* — **vor** jeder Methodikprüfung, vor jedem Backtest. Die fünf Schranken aus der Katalog-Herausforderung (long-only · nur Spot · nur OHLCV · ≥ 1 h · ein Konto) und Fables sechste (**Betreiberaufmerksamkeit**) sind damit **sieben** |
| **K5** | ⚠️ **Verbotsliste: WO gilt sie?** — bleibt ein echter Mangel, **aber nicht mehr dringend**, seit der Anlass (Carry, K10) entfallen ist. Die harte Regel lautet *Endpunkt als Literal, Verbotsliste, nur `/api/`-Pfade*, sagt aber nicht, ob sie nur für Brücke und Betriebspfad gilt oder auch für Forschungsskripte. **Zu klären, wenn ein Anlass entsteht — nicht vorher, und nie beiläufig.** *Ursprünglicher Einwand: Fable hielt einen lesenden `/fapi/`-Abruf für „innerhalb der Schranke"; das trifft die Datenschranke, nicht die Sicherheitsarchitektur. Eine strukturelle Sperre, die einmal für einen guten Zweck umgangen wird, ist keine mehr.* |
| **K2** | ⭐⭐⭐ **FABLE 16.09.: Diversifikation hat ZWEI Achsen — Quelle × Anlage. Der Horizont ist keine.** *Zwei Trendfolger auf Aktien steigen gemeinsam ein (1,94 ×); ein Trendfolger auf Aktien und einer auf Anleihen nicht — der Unterschied liegt im Underlying.* **Neun Bots besetzen VIER Zellen:** ① Fortsetzung×Aktien: `volatility_breakout` (einer) · ② Umkehr×Aktien: `rsi2`, `turtle_soup_stocks`, `elliott_wave_stocks` (**drei**) · ③ Fortsetzung×Krypto: `t3_supertrend`, `volatility_breakout_crypto` (zwei) · ④ Umkehr×Krypto: `rsi2_crypto`, `turtle_soup_crypto`, `elliott_wave` (**drei**). ⇒ **Budget gehört an die ZELLE, nicht an den Bot** — Änderung an Registertext 6, **vor dem Tag**. Kein Bot verschwindet; das Portfolio hört auf, dieselbe Wette dreimal zu gewichten (heute bekämen die Umkehr-Zellen **zwei Drittel** des Buchs) |
| **K3** | ⭐⭐ **Der Rahmen hat SIEBEN Zellen, das Projekt sitzt in vieren.** Erreichbar: ⑤ Cross-Asset-Trend = **`S-B1`, sofort, innerhalb aller Schranken** · ⑥ Informationsdrift = **`S-D1`, braucht I10** · ⑦ **Carry × Krypto, braucht die Spot-Schranke**. Danach wiederholt auf OHLCV long-only alles eine vorhandene Wette — Kalendereffekte tot (`S-E1`), Mikrostruktur nicht verfügbar, Faktoren brauchen Fundamentaldaten, Volatilitätsprämien brauchen Optionen. **Der Katalog ist nicht zu kurz; der Rahmen ist endlich.** ⭐ **Vorab-Filter ohne N-Kosten:** Ko-Einstiegsquote der Signale gegen jeden Bot derselben Anlage — **über 1,5 ⇒ gleiche Zelle ⇒ Variante, kein Kandidat** |
| **K4** | ⭐⭐ **Die Regeln, die N klein halten.** **(a) Kandidaten werden NIE gegeneinander gerankt; Zulassung ist je Kandidat absolut** — Vielfachheit entsteht nur, wo unter Alternativen gewählt wird. **(b) N ist die Rastergrösse ⇒ neue Kandidaten bekommen KEIN Raster**, sie treten mit festem Literatursatz an (N = 1 wie `S-E1`); ein Raster frühestens nach der ersten Bestätigungsperiode, als eigener Lauf. **(c) Familienbuchführung** im Register (geprüft / zugelassen / erwartete Fehlzulassungen). **(d) Reihenfolge nach Prior ist zulässig** — eine Reihenfolge vor jedem Ergebnis ist eine Ressourcenentscheidung, keine Schwelle; sie steht im Register, bevor der erste Kandidat läuft |
| **K6** | ⚠️ **EINWAND: Zellenbudget und Leiter greifen ineinander, ungeklärt.** Steigt einer von drei Bots einer Zelle auf **Bestätigt** — mehr vom Zellen- oder vom Gesamtbudget? Fällt einer auf **Schatten** — behält die Zelle ihr Budget oder schrumpft es? **Verschiedene Portfolios. Vor dem Tag zu klären**, danach Amendment |
| **K7** | ⚠️ **EINWAND: Fables VIX-Vorschlag verstösst gegen seine eigene Regel.** `^VIX` gegen `^VIX3M` „als Herausforderer gegen den SMA-200-Filter" ist ein **Rangvergleich zwischen zwei Alternativen** — N wächst auf 2, unsichtbar. Die Ticker selbst sind gewöhnliche OHLCV-Reihen und berühren die Schranke nicht; **die Regel schon**. (Offen: ob `^VIX3M` bei yfinance lückenlos zurückreicht) |
| **K8** | ⭐⭐ **Die ehrliche Antwort auf „welcher Vorteil ist plausibel".** **Geduld** trägt — aber **nur in den Fortsetzungs- und Beta-Zellen** ①③⑤⑦, wo man für Drawdowns bezahlt wird, die Institutionen wegen Mandaten nicht halten können. **Nicht in den Umkehr-Zellen:** *„Kurzfristige Umkehr auf Tageskerzen ist ein Wettlauf gegen Teilnehmer, die dieselbe Umkehr in Minuten handeln. Wer den Schluss t+1 bekommt und 0,30 pp zahlt, ist die langsame Partei."* ⚠️ **Sechs von neun Bots sitzen dort** — und es sind die beiden dreifach besetzten Zellen; er traut **einem** einen Vorteil zu (`rsi2` Aktien). **Kapazität — der einzige strukturelle Vorteil der Kleinheit — ist wegdefiniert**, weil das Universum aus den liquidesten Instrumenten der Welt besteht. **Sein Name für das Ganze: „Risikoprämien-Ernte mit Timing", Erwartung netto Sharpe 0,3–0,7 (Einschätzung, keine Messung)** |
| **K9** | **Programm bis 13.12.: NULL Kandidatenläufe, DREI Vorbereitungen** (alle N = 1, Abbruchkriterium vorab, keine Betreiberzeit am Mac): **(1)** `S-B1` Register + ETF-Daten — **läuft als TB-39** · ⛔ **(2) Carry-Backtest ENTFÄLLT** — nicht handelbar, siehe **K10** · **(3) Form-4-Ereignisstudie** (Insiderkäufe Code P, 2010–2026, abnormale 60-Tage-Rendite; **Abbruch unter 1,0 %**, oder 90-%-Intervall schliesst null ein, oder Effekt nur 2020–21). ⚠️ **Die Falle bei Form 4 ist keine Kostenrechnung, sondern eine Auflösungsrechnung:** 60-Tage-σ eines Grosswerts ≈ 12 %, bei ~400 Ereignissen Standardfehler ≈ 0,6 % — **ein Effekt von 2 % ist nachweisbar, einer von 0,5 % nicht**, und 0,5 % ist für Mega-Caps realistischer. **Nach Dezember: ein Kandidat je Quartal** — die bindende Schranke ist die **Betreiberaufmerksamkeit**, die sechste, die in unserer Tabelle fehlte |
| **K1** | **KATALOG-HERAUSFORDERUNG an Fable (16.09.2026)** — `FABLE_ANFRAGE_katalog_challenge.md`, bestehender Chat. **Bewusst NICHT „nenn neue Strategien"** (acht sind mit Begründung verworfen; eine neunte Liste erhöht nur N). Fünf Fragen: **(1)** Welche der fünf **selbstgesetzten Schranken** (long-only · nur Spot · nur OHLCV · keine Auflösung unter 1 h · ein Konto) kostet am meisten Ertrag je Einheit Aufwand — *eine gelockerte Schranke öffnet eine Klasse, eine neue Strategie nur eine Variante*. **(2) SEC EDGAR** als einzige ungenutzte Quelle: trägt ein ereignisgetriebenes Signal innerhalb der Schranken, und **womit widerlegt man es am schnellsten**? **(3)** Die nie ausgeschriebene **Neubau-Antwort** („zwei Ertragsquellen in drei Sleeves") zu Ende denken: kleinste Menge Sleeves, grösste Orthogonalität. **(4)** Wie fügt man Kandidaten hinzu, **ohne N aufzublähen** — und ist „ein eigener Lauf je Kandidat" ehrlich oder nur unsichtbare Vielfachheit? **(5)** Welche **Klasse von Vorteil** ist für ein Einzelsystem auf Tageskerzen mit 0,30 pp Kosten überhaupt plausibel — *„wenn keine davon Kosten und Vielfachheit übersteht, sag es"* |
| **T39.2** | **Betreiber-Impuls 16.09.: „mehr Bots ins Testing, um aus grösstmöglicher Variation zu schöpfen."** ⚠️ **Widersprochen, mit Begründung:** Die Schwelle Sharpe ≈ 1,6 gilt für **N = 653** und **steigt mit jeder weiteren Kombination** — aus einer grösseren Auswahl zu schöpfen heisst, dass der Beste **zufällig** besser aussieht. Dazu: die neun Bots sind **zwei Ertragsquellen**, ein zehnter auf demselben Universum macht dieselbe Wette lauter. Und ein heute gestarteter Bot hätte im Dezember **null** Live-Record, käme nach der Leiter also nicht über Schatten. **Der Weg zu mehr Variation ist `S-B1` — eine andere Quelle, nicht mehr Varianten derselben zwei** |
| **D1** | ⚠️ **Das Dashboard zeigt KEIN einheitliches Gesamtbild — und kann es derzeit nicht.** Drei unabhängige Gründe: **(1)** Die **Ergebniskurven** melden nach TB-34 `5× ABWEICHEND` (Krypto) und wurden **bewusst nicht neu erzeugt** — das gehört in denselben Schritt wie die Neuselektion. **(2)** Die **Portfolio-Sicht liefert keine kombinierten Kennzahlen** (T35.6): zwei Bots über `MIN_LIVE_CLOSED_TRADES`, Fenster ab 04./09.09., **gemeinsames Fenster aller neun leer**. **(3)** Der Papierpfad **vor dem Umstellungstag** (T38.7) gilt als **nicht vergleichbar** — er beschreibt bei fünf Bots eine Strategie, die es im Backtest nicht gibt. ⚠️ **Dazu P2:** ohne mitgeschriebene Positionsgrösse existiert für KEINEN Zeitraum eine gewichtete Rendite. ⇒ **Ein „Gesamtbild über die Gesamtperiode" wäre eine Zusammenführung von Dingen, die nicht dasselbe messen.** **Das ehrliche Artefakt ist eine Kurve MIT sichtbarer Zäsur**, nicht eine geglättete. Betreiberentscheidung, gehört zu **C8** |
| **T38.7** | ⭐⭐⭐ **UMSTELLUNGSTAG FESTGEHALTEN: `2026-09-16T04:42:24Z`, alle neun Bots.** Ab hier läuft das einzige Vergleichsfenster Backtest gegen Live — **88 Tage bis 13.12.** Der Zeitpunkt liegt **nach** dem 06:00-Cronlauf von `elliott_wave` auf altem Code (folgenlos) und **vor** dem 07:00-Lauf über die neue Schicht. ⭐ **Der produktive Pfad ist einmal real durchlaufen:** Cron → `trading-env/bin/python3` → Abrufschicht → 24 Rückfall-Zeilen → je 1 Kerze nach der Entscheidungskerze verworfen → Telegram → kein Traceback. **130/130 + 25/25**, neun DBs gesichert und hinterher **byteweise identisch**, Datenstand unverändert |
| **T38.8** | ⚠️ **Die Umstellungstag-Datei liegt NUR im Zweig** `claude/new-session-xzh112` (`dc9d2ec`), nicht auf `main` — PR #111 war schon gemergt, sie braucht einen **neuen PR**. Bis dahin existiert der Beleg für den Beginn des Vergleichsfensters **nur lokal** |
| **T38.9** | ⚠️ **`shared/test_kursdaten.py` prüft den REPO-ZUSTAND, nicht das Verhalten** — per `git diff --name-only origin/main`, dass keine `forward_test.py` verändert ist. Sein Ergebnis hängt davon ab, wo `origin/main` steht (im Basislauf rot, danach grün, ohne Verhaltensänderung). **Er wird künftig jedes Mal rot, wenn eine Aufgabe `forward_test.py` legitim ändert.** Ein Test, der eine **Auflage** prüft statt einer **Eigenschaft**, macht jeden Basislauf unschärfer — heute: 5 statt 4 erwartete rote Tests |
| **T38.10** | ⚠️ **`system/test_log_rotation.py` flattert** — Rennbedingung zwischen Sichern und Leeren, einmal rot, danach viermal grün. **Ein flatternder Test untergräbt die Aussagekraft jedes Basislaufs.** Nicht dringend |
| **T38.11** | **Dokumentation falsch an zwei Stellen, jetzt erhoben:** Die Aktien-Crons laufen **gestaffelt** — 22:15 `elliott_wave_stocks` · 22:20 `rsi2_mean_reversion` · 22:50 `volatility_breakout` · **23:15 `turtle_soup_stocks`**, nicht alle 22:15 (betrifft `docs/UEBERGABEPROTOKOLL.md` Abschnitt 2 und den Kopf von `shared/entscheidungskerze.py`; an der Kalender-Schranke ändert das nichts, alle nach 20:00 UTC). Und die **Zuordnung der täglichen Krypto-Crons** ist geklärt: `20 23` rsi2_crypto · `50 23` volatility_breakout_crypto · `15 0` turtle_soup_crypto |
| **T38.12** | ⚠️ **Ab sofort meldet JEDER Bot täglich den Rückfall** — **223 von 223** Dateien ohne die erwartete Kerze (gestern 199; seit Tageswechsel sind auch die 24 Krypto-Tagesdateien veraltet). **So entworfen, und es bleibt so, bis T38.3 entschieden ist.** ⚠️ **Ohne einen Vermerk „erwartet" wird die Meldung binnen einer Woche zur Tapete — und dann fällt die echte nicht mehr auf.** Zu entscheiden zusammen mit T38.3 |
| **T38.13** | **Vom Nutzer zu prüfen: Telegram-Empfang.** Die Sitzung konnte den **Versand** bestätigen, nicht den **Empfang**. Erwartet: `[ABRUFSCHICHT] probe_tb38:` plus zwei echte Meldungen von 06:05 (`t3_supertrend`) und 06:06 (`turtle_soup_stocks`) |
| **T38.3** | ⚠️⚠️ **KONFLIKT: Der `data/`-Cron (offener Punkt 24) kollidiert mit Registertext 5.** TB-38 meldet: **199 von 223 Dateien ohne die erwartete Kerze**, sechs von neun Bots fallen auf den Live-Abruf zurück — `data/` wird von **keinem** Cronjob aktuell gehalten. Aber Registertext 5 sagt: *„Der Selektionslauf liest ausschliesslich die Dateien unter `data/` im registrierten Zustand."* Und **jeder Aktien-Abruf ändert den Hash** (T35.4). **Cron an ⇒ registrierter Zustand vor dem Lauf verloren. Cron aus ⇒ der gebaute Datenweg wirkt nie.** Drei Auswege: (1) eingefrorene Kopie `data_registriert/` — ⚠️ zwei Bestände nebeneinander · (2) Cron nur Krypto (reproduzierbar), Aktien eingefroren · (3) **Cron erst nach dem Selektionslauf**, Rückfall-Meldung als erwartet vermerken. **Neigung: (3). An Fable — der einzige Punkt, der eine fünfte Runde rechtfertigt** |
| **T38.4** | ⚠️ **EIGENER FEHLER, bis zu Fable gelaufen:** Die Angabe „Cron zur Minute 5, Teilkerze **fünf Minuten** alt" stimmt nicht. `5 */4` ist die **Broker-Brücke**, der Bot steht auf `0 */4`, und Cron zündet in **Ortszeit** — trifft also UTC 22/02/06/… statt des UTC-4h-Rasters. **Die Teilkerze war 2–3 Stunden alt (50–75 % gefüllt).** Aus dem TB-35-Bericht übernommen, ohne `crontab -l` zu prüfen. ⚠️ **Steht so in der Wochenrückmeldung**; Fables Argument in 2.1 („Hoch, Tief, Schluss noch fast auf der Eröffnung") stützt sich darauf. **Schlussfolgerung überlebt, Grössenordnung nicht — richtigstellen.** *Lehre (zweites Mal heute): Angaben aus fremden Berichten gegen die Quelle prüfen, bevor sie weitergereicht werden* |
| **T38.5** | **Offener Punkt 26 kann geschlossen werden:** Die Binance-Lesart von `close_time` (`open + Länge − 1 ms`, Feld 6) ist keine Auslegung, sondern die Definition. Die Alternative `open + Länge` wäre die **Öffnungszeit der nächsten** Kerze und hätte zur Folge, dass ein Lauf um 12:00:00 auf die 04:00-Kerze zurückgreifen müsste. **Bestätigen** |
| **T38.6** | **Offener Punkt 25:** Schreibpfad `<=` gegen Lesepfad `<` — **eine Millisekunde** je Kerze. Bewusst nicht angeglichen, weil eine Änderung an `abrufschutz` den Datenstand-Hash änderte. Kein Cron-Eintrag trifft diesen Zeitpunkt; als Test 11.2 festgehalten |
| **T38.1** | ⚠️ **Der Umstellungstag ist eine Zäsur:** Papierpfade **davor** gelten für den Vergleich Backtest gegen Live als **nicht vergleichbar**; **I5 beginnt für die fünf Krypto-Bots neu**. Ab da läuft das einzige Vergleichsfenster bis zum 13.12. |
| **T38.2** | **Entscheidung 3 (2d-Deckel) freigegeben:** Für Bots ohne Zeitbremse gilt **P95 + 1** als Obergrenze — `t3_supertrend` **13 Handelstage**. Fable hat ausdrücklich nicht widersprochen. **Gehört in den nächsten Registernachtrag**, nicht in TB-38 |
| **W9** | ⭐⭐⭐ **FABLE 15.09., Antwort zur OOS-Lage — der Satz, der die Lage ordnet:** **„In-Sample kann ausschliessen. Nur Out-of-Sample kann bestätigen."** Die Vielfachheit hat eine **Richtung**: Sie lässt Zufall wie Können aussehen, nie Können wie Zufall. Ein Satz, der als bester von 653 die vorab festgelegten Kriterien **reisst**, ist ein Befund; besteht er sie, heisst das **nicht widerlegt**, nicht **trägt**. ⇒ **Im Dezember entscheidbar:** Ausschlüsse, Parametersatz, **Grundbudget für alle Nicht-Ausgeschiedenen**. **Nicht entscheidbar:** „ist ein Verdiener", mehr als Grundbudget, Echtgeld. **Der Literatur-Prior ist bereits verbraucht** — er steckt im Benchmark (Rang 3, Kriterium c); ihn zusätzlich als Zulassungshürde anzulegen hiesse, eine Schwelle zu setzen, während man weiss, wen sie trifft. **`elliott_wave` bekommt dieselben Kriterien wie RSI-2** |
| **W10** | **Registertext 6 — Budgetstufen (Leiter).** Drei Stufen: **Schatten** (läuft, kein Gewicht, nicht in Portfolio-Zahlen) · **Grundbudget** (gleicher Anteil für alle) · **Bestätigt** (Rang-5-Gewichtung). Nach dem Lauf: kein Abbruchkriterium ⇒ Grundbudget, sonst Schatten mit Benchmark-Position. **Auf- und Abstieg quartalsweise durch dasselbe eingefrorene Skript**, Aufstieg frühestens nach **30 Trades und 6 Monaten**. ⭐ **Kein Betreiberentscheid setzt eine Stufe hinauf — nur hinunter (Notbremse).** **D5 setzt Stufe „Bestätigt" seit zwei Quartalsprüfungen voraus** |
| **W11** | ⭐⭐⭐ **Registertext 7 — und die ZEITKRITISCHE Folge.** Die einzige Evidenz, die bis Dezember noch aufgebaut werden kann, ist **OOS für den Backtester**, nicht für die Bots: Stimmt der simulierte Kapitalpfad mit dem Papierpfad überein, bei gleichen Kerzen und gleichen Parametern? ⚠️ **Das setzt voraus, dass die fünf Bots JETZT umgestellt werden, nicht im Dezember.** **15.09. → 13.12. sind 89 Tage — genau die drei Monate, die der Vergleich braucht. Jeder Tag Verzug kostet einen Tag, und es gibt kein zweites Fenster.** ⇒ **W3 (Freigabe Umbau) ist nicht aufschiebbar, sondern der dringendste Punkt im Projekt.** *(Korrektur: zuvor als „kann warten" eingeordnet.)* |
| **W12** | ⚠️ **Einwand zu Registertext 7: keine Mindestzahl Signale.** Unter 95 % Übereinstimmung ⇒ nicht über Schatten hinaus. Aber `volatility_breakout` Aktien erzeugt bei **21 Tagen Median** in drei Monaten vielleicht **zwölf** Signale — **bei acht reisst ein einziger Unterschied die Schwelle** (87,5 %). **Dieselbe Klasse Fehler wie die gestrichene 10-Trades-Regel:** trifft nach Handelsfrequenz statt nach Qualität. **Vorschlag:** unter einer Mindestzahl **berichten, nicht bewerten** — „Backtester nicht **geprüft**" statt „nicht **bestätigt**" |
| **W13** | ⚠️ **Einwand zu 6c: Die Aufstiegshürde hängt an einer selektionsverzerrten Zahl.** Bezug ist der **Netto-Calmar des Gewinners über die Selektionsfalten** — also der beste von 653, mit genau der Aufblähung, gegen die das Verfahren gebaut ist, und **je Bot verschieden gross**. Zwei Bots gleicher wahrer Güte bekommen **verschieden hohe Hürden**. **Vorschlag: den entblähten Wert als Anker** (DSR bei N_eff/N/2N wird ohnehin gerechnet), dann ist die Hürde über die neun Bots **vergleichbar** |
| **W14** | ⚠️ **Was vom Dezember zu erwarten ist, vorab gedacht:** Plausibel ist, dass die **Mehrzahl der neun Bots auf Schatten landet** und das Kapital in einer statischen Benchmark-Position liegt — die Projektunterlagen halten selbst fest, dass bei N = 653 die Schwelle bei **Sharpe ≈ 1,6** liegt und *„wahrscheinlich kein einziger der neun sie erreicht"*. **Das wäre kein Scheitern, sondern das System, das funktioniert.** Jetzt zu denken, nicht im Dezember unter Druck |
| **W8** | ⭐⭐ **DIE FRAGE, DIE AUS 2.1 FOLGT — an Fable gestellt 15.09.:** Seit Verfahren B ist der Live-Record die **einzige** OOS-Evidenz. Nach 2.1 taugt der Papierpfad der fünf Krypto-Bots **vor** dem Umstellungstag nicht als Holdout. Nach dem neuen 2d beginnt die Bestätigungsperiode erst nach Schliessen der letzten Alt-Position. **⇒ Für fünf von neun Bots gibt es zum Selektionszeitpunkt KEINE einzige OOS-Beobachtung.** Zwei Aktien-Bots haben gerade erst 10 bzw. 14 geschlossene Live-Trades. **Worauf stützt sich im Dezember die Entscheidung, ob ein Bot ins Buch kommt?** Drei Kandidaten vorgelegt: (a) selektieren, Buch später bestücken — Frist gehalten, nichts entschieden · (b) der **Prior** trägt allein — ehrlich, aber ein viel kleinerer Anspruch · (c) **Faltenrobustheit** trägt mehr als Verfahren B ihr zugesteht — dann muss **vor** dem Lauf stehen, woran man sie misst. **Bewusst nicht selbst festgelegt:** eine Regel, die nach dem Zusammenrechnen der Lage entsteht, weiss schon vom Ergebnis |
| **W2** | ⚠️ **Einwand: das neue 2d hat keine Obergrenze für `t3_supertrend`** — den **einzigen** Bot ohne Zeitbremse, und genau den, für den das P95 gerechnet wurde. Eine hängende Position verschiebt die Bestätigungsperiode **unbegrenzt**. **Vorschlag: P95 + 1 (= 13) als Deckel**, Ablesung bleibt die Regel |
| **W3** | ⚠️⚠️ **Der Umbau berührt alle neun `forward_test.py` — harte Projektregel, braucht ausdrückliche Freigabe des Betreibers.** Und er **bündelt Ausfallrisiko**: heute scheitern fünf Bots unabhängig, danach hängen neun an **einer** Funktion; ein Fehler dort sieht aus wie ein Marktereignis, nicht wie ein Bug |
| **W4** | ⚠️ **Fables Punkt 2 (Daten-Cron mit Frischeprüfung) kollidiert mit „melden, nicht stoppen".** Nur melden ⇒ dieselbe Lücke wie heute Morgen, nur mit Mail. Blockieren ⇒ ein ausgefallener Abruf legt neun Bots still. **Mittelweg: `data/` als Quelle, Rückfall auf Live-Abruf bei fehlender Frische, plus Meldung.** Betreiberentscheidung |
| **W5b** | ⭐⭐ **GEMESSEN 16.09.: Der Selektionslauf kostet STUNDEN, nicht Wochen.** **0,19 s je Kombination** (20 Symbole, 42 848 Zeilen), dreimal gemessen, keine Ausreisser. Hochrechnung des Skripts 18 min — **unterschätzt**, weil es alle neun Bots so teuer rechnet wie `rsi2_crypto`. Nach Zeilenzahl gewichtet (`elliott_wave` 1h ≈ 24×, `t3_supertrend` 4h ≈ 6×, vier Aktien-Bots je ≈ 7,5× wegen 150 statt 20 Symbolen): **Summe ≈ 63 statt 9 ⇒ rund 2 h Kern, mit Bootstrap und Reserve 3–5 h.** **Selbst bei Faktor zehn daneben ist es ein Tag.** ⇒ **W5 erledigt.** ⚠️ **Und meine Warnung von heute Morgen war falsch gewichtet:** Datenordner-Umbau und TB-30b konkurrieren um **Betreiberzeit und Cloud-Sitzungen**, nicht um Rechenzeit |
| **T40.1** | ⭐⭐⭐ **ACHT VON NEUN REGISTERZEILEN SIND FALSCH, alle zu hoch.** Nur `elliott_wave` stimmt exakt (unter Lesart H). ⭐ **Es kommt NIRGENDS ein Symbol hinzu — der Loader ist überall strenger: F ⊆ H ⊆ A.** **Korrigierte Tabelle (Lesart H)** liegt im Ergebnisdokument zum Kopieren: `elliott_wave` 6/13/13 · B 18 · `t3_supertrend` **3**/6/9/13/13/13/17 · B 18 · drei Krypto-Tagesbots 6/9/**10**/13/13/17/18 · B **20** · vier Aktien-Bots 137/137/139/139/140/142/**145** · B **147**. ⚠️ **Zweite betroffene Tatsachennotiz, in der Aufgabe nicht erwähnt: „Symbole ohne Faltenevidenz" sind Listen JE BOT, nicht je Markt** — `elliott_wave` **11**, `t3_supertrend` **7**, Krypto-Tagesbots 6, Aktien-Bots **5** (heute steht dort nur SNDK) |
| **T40.2** | ⚠️⚠️⚠️ **ENTSCHEIDUNG H ODER F — und sie ist keine freie mehr.** **Registertext 3b sagt H** (*„an mindestens einem Handelstag der Falte handelbar"*); **meine TB-40-Aufgabe verlangte F** (*„am Faltenbeginn geprüft"*) — **Widerspruch in meiner Aufgabenstellung, die Sitzung hat beides gemessen statt still aufzulösen**. **Unter F verliert `elliott_wave` seine erste Falte (0 Symbole) und steht bei 2 von 3 ⇒ „unterbestimmt", Schatten ausserhalb des Buchs.** ⚠️ **Wir kennen jetzt die Wirkung — ein Wechsel auf F wäre eine Wahl NACH dem Ergebnis, und sie träfe ausgerechnet den Bot mit dem schwächsten Prior.** **Empfehlung: bei H bleiben.** Falls doch F, gehört in den Registertext ausdrücklich, **dass die Änderung erfolgte, nachdem ihre Wirkung bekannt war** |
| **F7** | ⭐⭐⭐ **FABLE 16.09.: (a) — dünne Falten zählen wie jede andere, KEINE neue Schwelle.** Er gibt unseren Einwand zu (*„eine Falte mit drei Symbolen ist ein anderes Universum"*), **aber das tragende Argument ist ein drittes: „Ein Median hat keine Gewichte, nur Rangplätze — eine einzelne Falte kann ihn nie aus dem Bereich der übrigen herausbewegen."** ⇒ Unsere Sorge „mit vollem Gewicht in den Median" beschreibt einen **Mittelwert**; der Median wurde gegen genau diesen Fall gewählt. **Was die dünne Falte kostet, ist Auflösung, nicht Richtigkeit** — sie vergibt fast zufällige Rangplätze. **(b) verworfen:** eine Mindest-Symbolzahl träfe genau die frühen Falten, die als einzige Bärenmarkt-Vorgeschichte haben (2019 nach 2018). **(c) verworfen:** zwei Faltenbegriffe im Register erzeugen die Frage, welche Falte für welchen Zweck zählt — *und die wird irgendwann nach Sichtung beantwortet* |
| **F8** | ⚠️ **Ungenauigkeit in Fables Argument, betrifft ausgerechnet `elliott_wave`:** *„Bei drei Falten ist der Median einer der beiden verlässlichen Werte"* — **stimmt nicht.** Liegt die verrauschte Falte zwischen den beiden verlässlichen, **ist sie selbst der Median** (0,40 / 0,80 / **0,60** ⇒ Median 0,60). **Die Schlussfolgerung überlebt** — der Wert bleibt eingeklemmt und kann nichts ausserhalb des gemessenen Bereichs erzeugen —, aber es ist eine **Einklemmung, keine Auswahl**. Bei sieben Falten ist sein Argument hart, bei dreien nicht. **Kein Handlungsbedarf; die genaue Fassung gehört ins Journal, nicht seine** |
| **F9** | ⭐⭐ **Die Einordnung der dünnen Falte: „Die drei Symbole von 2019 sind nicht drei zufällige von 24. Es sind BTC, ETH und BNB — die drei, die überlebt haben."** Die Falte testet Parametersätze **auf Überlebenden im Aufschwung 2019** ⇒ **Survivorship aus Registertext 3c in stärkster Form, dort bereits eingetragen.** *Die dünnen frühen Falten sind kein neues Problem, sondern die Stelle, an der das bekannte am grössten ist.* ⭐ **Und das stärkste Argument für I10, das das Projekt hat:** ein point-in-time-Universum hätte 2019 rund 24 Paare gehabt — **andere als heute** |
| **F10** | **Registertext 3b, Ergänzung (a)–(e).** (a) Falte zählt ab **einem** handelbaren Symbol, keine Mindestzahl. (b) `MIN_HISTORY_*` je Bot **mit Namen und Einheit**, alle fünf Werte im Register; ⭐ **bei Kerzenzählung hängt Handelbarkeit an der Lückenfreiheit** — Snapshot friert ein, Live kann abweichen, **Registertext 7 zählt solche Fälle**. ⭐⭐ **(c) NEU und von uns übersehen: Der Benchmark einer Falte wird auf den IN DIESER FALTE geladenen Symbolen gerechnet, nicht auf dem vollen Universum — „Bot und Benchmark leben in derselben Menge."** *Sonst wäre die Differenz überwiegend die zwischen zwei Universen; betrifft Abbruchkriterium (c) aus Rang 3 unmittelbar.* ⭐ **(d) Faltenkohärenz:** Spearman-Rangkorrelation der Parametersatz-Rangfolge dieser Falte gegen die Rangfolge nach dem Median der übrigen — **berichtet, kein Kriterium daran**; *misst genau unsere Befürchtung, aber NACH dem Lauf, ohne dass vorher jemand eine Falte für unwürdig erklärt*. **Besser als alle drei Möglichkeiten, die wir vorgelegt hatten.** (e) Listen „ohne Faltenevidenz" je Bot |
| **F11** | ⭐ **H ist bestätigt — mit einem sachlichen Grund, den wir nicht hatten:** *„F beschreibt eine Strategie, die der Bot nicht handelt. Ein Symbol, das im März handelbar wird, wird ab März gehandelt — F würde es für das ganze Jahr streichen."* ⇒ **H ist nicht nur das Registrierte, sondern das, was der Loader tut.** Beides gehört ins Journal, **in dieser Reihenfolge**: erst die Disziplin-Begründung, dann die sachliche |
| **F12** | ⚠️ **Umfang, der dazukommt:** **(1)** Der Logging-Fix für die drei lautlosen Bots ist ein **Bug-Fix, kein Amendment** (*„ändert kein Verhalten, nur Sichtbarkeit"*) — ⚠️ **aber `multi_symbol_optimise.py` steht auf der Sperrliste, also dritte Freigabe dieser Woche.** **(2)** Registertext 3b(c) ist eine **zusätzliche Anforderung an den Auswerter**, der ohnehin auf Verfahren B umgebaut wird. ⭐ **Die Regel für den Backlog, wörtlich: „Ein Lauf, der ein Symbol auslässt, sagt es. Immer."** — *Der Befund, der den Trockenlauf auslöste, war nur sichtbar, weil einer von neun Bots das tut. Das ist keine Quote, mit der ein Register leben kann* |
| **T40.7** | **AN FABLE 16.09.: `FABLE_ANFRAGE_faltenzaehlung.md`** — die Frage aus T40.3, plus die Bestätigung unserer H-Entscheidung zur Kontrolle, plus die Registerseite von T40.5 (*gehört „ausgelassen, mit Grund" je Bot und Falte in den Ergebnisbericht?*). ⚠️ **Blockiert den Registernachtrag, und der blockiert TB-30b** |
| **T40.3** | ⚠️ **Auch unter H offen: `t3_supertrend` hat in der Falte 2019 nur DREI von 24 Symbolen**, `elliott_wave` in der ersten sechs. **Zählt eine solche Falte?** Weder 3b noch 4b sagt etwas. ⚠️ **Berührt die Streichung von Registertext 1c:** Die Mindestzahl von 10 Trades wurde gestrichen mit der Begründung, der Median fange dünne Falten ab und der Tages-Sharpe sei selbstbegrenzend. **Eine Falte mit 3 von 24 Symbolen ist aber keine dünne Falte, sondern ein anderes Universum** — das Selbstbegrenzungsargument handelt von wenigen Trades in derselben Menge. **An Fable** |
| **T40.4** | ⭐⭐ **`MIN_HISTORY_DAYS` ist nicht eine Zahl, sondern VIER (korrigiert 16.09., vorher stand hier fälschlich „fünf" — Gruppen gezählt statt Werte) — und bei einem Bot eine andere Grösse.** `elliott_wave`: **`MIN_HISTORY_HOURS` = 17 520, misst KERZENZAHL** · `t3_supertrend` 730 Tage · drei Krypto-Tagesbots 500 · vier Aktien-Bots 1 825. ⚠️ **Eine Reihe mit gleicher Zeitspanne, aber Lücken, fällt nur bei `elliott_wave` heraus** — gemessen. **Anknüpfung an T34.3:** 13 Krypto-1h-Dateien fehlen drei Stunden ab 2021-09-29, und `elliott_wave` ist genau der Bot auf 1h, der Kerzen zählt (folgenlos bei 3 von 17 520, aber der Mechanismus ist da). **Der Registereintrag muss beide Namen und beide Grössen nennen** |
| **T40.5** | ⚠️⚠️ **BETRIEBSPROBLEM, kein Registerproblem: Drei Bots sortieren völlig lautlos aus.** `rsi2_mean_reversion`, `turtle_soup_stocks`, `volatility_breakout` schreiben bei **zu kurzer Historie UND bei fehlender Kursdatei keine einzige Zeile**. **Der Befund, der TB-40 ausgelöst hat, war nur sichtbar, weil `rsi2_crypto` ihn meldet.** Fehlt morgen eine Aktien-Kursdatei, handeln drei Bots ein kleineres Universum und niemand erfährt es. Dazu: **eine leere Kursdatei ist bei acht von neun ein stiller Ausfall** (`if df.empty: continue`). Kein Mindestvolumen-Filter bei keinem der neun |
| **T40.6** | **Zwei Nebenbefunde ohne Handlungsdruck:** (1) ⚠️ **Der Import von `strategies/elliott_wave/multi_symbol_optimise.py` braucht Netz** — er holt `INTERVAL` aus `shared/fetch_multi_data.py`, das auf Modulebene `Client()` anlegt, und `python-binance` pingt im Konstruktor `api.binance.com`. **Eine Netzrunde für eine Konstante.** Kandidat für die nächste Aufräumrunde. (2) Die Klammer in Registerabschnitt 15.5 („26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`") rechnet falsch: Die Datei mit dem eingetragenen Hash hat **25 Zeilen**, `PAXGUSDT` steht nicht darin. **Ergebnis 24 richtig, Rechenweg falsch** |
| **TB-40** | erledigt 16.09.2026, PR #113 gemergt — Befunde im Archiv (`BACKLOG_ARCHIV.md`, Abschnitt „Aus Abschnitt 2 — die neun ERLEDIGT-Zeilen"; verschoben 20.09.2026, TB-60) |
| **T36.2b** | ⭐⭐⭐ **T36.2 IST KEINE VERMUTUNG MEHR — gemessen.** Der Bot-Loader meldet beim Laden: `ENSOUSDT 335 / PUMPUSDT 368 / ZKCUSDT 364 / UUSDT 244 Tage (< 500 noetig), wird uebersprungen` ⇒ **`MIN_HISTORY_DAYS = 500`, geladen werden 20 von 24 Symbolen.** **Im Register stehen 6/9/13/13/13/17/18 und Bestätigung 23** — nach der Lesart *„Symbol zählt, sobald Kursdaten vorliegen"*. **Der Code fragt etwas anderes.** ⚠️ **Und der Unterschied ist grösser als die vier Namen:** die 500-Tage-Schranke gilt **je Falte** — in der Falte 2019 müsste ein Symbol schon 2017 gelistet gewesen sein, die Zahl dürfte dort **deutlich unter 6** liegen. ⇒ **Fables Trockenlauf `--nur-universum` ist nachweislich nötig, und er gehört VOR den Registernachtrag**, sonst trägt der wieder falsche Zahlen ein. **Solange der Tag nicht steht, ist die Korrektur kostenlos** |
| **W5** | ⚠️⚠️ **Niemand hat die Laufzeit des Selektionslaufs geschätzt.** 653 Kombinationen × 9 Bots × 7 Falten, je mit voller Kapitalsimulation, dazu **Block-Bootstrap mit 2 000 Ziehungen je Rasterpunkt** — auf einem MacBook, dessen Datenbestand gerade um 39 % gewachsen ist. **Grösste unbekannte Grösse im Zeitplan bis 13.12., billig zu klären:** einen Rasterpunkt auf einer Falte rechnen und hochskalieren. **Erster Schritt in TB-30b, vor der Umstellung des Auswerters** |
| **W6** | **Reihenfolge bis zum Lauf (nach Fable, mit meinen Einwänden):** 0 Laufzeit schätzen · 1 **Freigabe** Umbau `forward_test.py` · 2 gemeinsame Abruffunktion · 3 **Entscheidung** Frischeprüfung · 4 Trockenlauf `--nur-universum` → 3b · 5 2d und 5 ersetzen · 6 `auswertung.py` auf Verfahren B · 7 **signierter Tag + Zeitanker (friert Register UND Skript gemeinsam ein)** · 8 Lauf. ⚠️ **Die Verankerung rutscht ans Ende** — ein Tag vor der Auswerter-Umstellung würde einen Zustand einfrieren, den das Register nicht beschreibt. *Vollständigkeitstest für „Register fertig": Lässt sich das Skript aus dem Register schreiben, ohne auf ein Ergebnis zu blicken?* |
| **W7** | **Nebenbefund Fable, für TB-30a-Raster:** `MAX_HOLD_HOURS = 90` Tagesbalken bei 7 Tagen Median ist ein **toter Parameter** wie **Y3**. Steht eine Zeitbremse im Raster, ist ihre Obergrenze aus der Haltedauerverteilung abzuleiten (etwa P99 × 2, aus heutigen Trades, **vor** dem Lauf), sonst steht sie in vier von fünf Stufen ausserhalb des Verhaltens |
| **T36.5** | TB-36 MAC-LAUF ERLEDIGT 15.09. — alle zehn Schritte grün, kein Befund — Befunde im Archiv (`BACKLOG_ARCHIV.md`, Abschnitt „Aus Abschnitt 2 — die neun ERLEDIGT-Zeilen"; verschoben 20.09.2026, TB-60) |
| **T36.6** | ⚠️ **Einzige rote Testdatei ohne Erklärung: `research/exposure_messung/test_exposure_kern.py`** (1 von ~30: „am Tag mit nur einem gültigen Kurs zählt dieser allein"). Auf dem Mac **vor** TB-36 ebenfalls rot ⇒ **vorbestehend**, aber *vorbestehend ist nicht erklärt*: seit wann, ist offen. ⚠️ **TB-34 hat alle Krypto-Kursdaten ersetzt** — ein Zusammenhang ist nicht geprüft. **Vor TB-30b ansehen**, weil Exposure in die Benchmark-Messung von Rang 3 eingeht |
| **T36.1** | ⚠️ **`elliott_wave_stocks`: `MAX_HOLD_HOURS = 90` wird als 90 TAGESBALKEN gelesen → Embargo 91 Handelstage**, gegenüber 11–16 bei allen anderen. Ein Parameter mit „HOURS" im Namen auf einem Tageskerzen-Bot. **Entweder gewollt** (Zeitbremse greift bei 7 Tagen Median nie — dann beginnt die Bestätigungsperiode für diesen Bot erst im **Frühjahr 2027**) **oder ein Einheitenfehler** (gemeint 90 Stunden ≈ 3,75 Tage, angewandt 90 Tage → Faktor 24 zu lang, **im Live-Betrieb**). **Vor dem signierten Tag klären** |
| **T36.2** | ⚠️⚠️ **Die eingetragenen Symbolzahlen könnten den Lauf nicht treffen.** Registertext 3b nennt 6/9/13/13/13/17/18 bzw. 140…149 — die Bots überspringen aber kurze Historien **selbst** (`MIN_HISTORY_DAYS`: `GEV`, `SNDK`, `CEG`, `ENSOUSDT`, `PUMPUSDT`, `ZKCUSDT`, `UUSDT`). Zusammen mit **Lesart A** (Symbol zählt, sobald Kursdaten vorliegen) heisst das: **der Bot-Code könnte beim Lauf weniger laden, als im Register steht.** **Eine Tatsachennotiz ist eine Behauptung über den kommenden Lauf.** ⇒ **In TB-30b als ERSTE Prüfung vor jeder Rechnung:** geladene Symbolliste je Falte gegen die eingetragene. Weicht sie ab, **nicht rechnen, sondern die Notiz korrigieren** — solange der Tag nicht gesetzt ist, kostet das nichts |
| **T36.3** | **`SNDK` ist das einzige Aktiensymbol ohne Faltenevidenz** — ein Titel in der Liste nach **heutiger** Marktkapitalisierung, den es 2019–2025 nicht durchgehend gab. Kein Handlungsbedarf; erster konkreter Beleg für die Vorhersage aus Registertext 3c im Aktienteil |
| **T36.4** | **Zwei Fehler in der TB-36-Aufgabenstellung, von der Sitzung gefunden:** (1) „AF.2 Nr. 6" existiert im Repo nicht — die Doppeljahr-Regel steht in **Abschnitt 5.1 Nr. 6** mit Auswertung in 5.4; aus dem Beratungstext übernommen, ohne zu prüfen. (2) Drei als „ersetzt" ausgewiesene Fassungen **standen nie im Register** (Mindestzahl 10 Trades, „mindestens 4", „behält heutige Parameter") — sie stammen aus Beratungsrunden und sind **Erstfassungen**. *Lehre: Fundstellen aus Beratungstexten gegen das Repo prüfen, bevor sie in eine Aufgabe gehen* |
| **TB-36** | erledigt (Cloud) 15.09.2026, Mac-Lauf offen — Befunde im Archiv (`BACKLOG_ARCHIV.md`, Abschnitt „Aus Abschnitt 2 — die neun ERLEDIGT-Zeilen"; verschoben 20.09.2026, TB-60) |
| **V5h** | ⭐ **ALLE VIER PUNKTE GEKLÄRT (15.09.2026, Fables Nachfrage-Antwort).** **1c gestrichen** (keine Mindestzahl Trades; Sharpe 0 nur bei Standardabweichung 0). **3a–3d ersetzt** — heutiges Universum, Symbolzahl je Falte als Tatsachennotiz, Survivorship-Vorbehalt **mit vorhergesagter Richtung**, **I10 als eigener späterer Lauf mit eigenem N, kein Amendment**. **4b: Mindestzahl 3 statt 4** (Fable korrigiert sich selbst: bei 3 Falten ist der Median der mittlere Wert, bei 4 das Mittel aus zweien) → **`elliott_wave` wird selektiert**. **4c: Schatten ausserhalb des Buchs** plus statische Benchmark-Position statt „heutige Parameter behalten". **Nichts mehr strittig — der Registernachtrag kann geschrieben werden** |
| **V5i** | ⚠️ **Vorhersage im Register, die die heutigen Bots betrifft:** Registertext 3c sagt, ein Überlebenden-Universum begünstige Sätze mit **weiten oder fehlenden Stops und langen Zeitbremsen**. Genau das sind `turtle_soup_stocks` (kein Stop, kein Limit), beide **RSI-2** (kein Stop) und `volatility_breakout_stocks` (Zeitbremse 15 Tage bei 21 Tagen Median). **Bestätigt die Neuselektion diese Einstellungen, ist das noch kein Beleg für sie** — gehört in die Beurteilung, nicht erst in den I10-Lauf |
| **V5j** | **Bewusst angenommene Verzerrung, vor Rang 5 wieder aufzurufen:** Der Tages-Sharpe skaliert grob mit **√(Anteil aktiver Tage)** — selektive Parametersätze werden benachteiligt, weil freies Kapital im Papier **null** verdient. Bei **37,9 %** mittlerer Brutto-Exposure stehen zwei Drittel des Kapitals rechnerisch still. Fable rät von einer Kassenverzinsung ab (macht die Selektion von einer strategiefremden Zahl abhängig); **angenommen**, aber bei **Rang 5 (Netting/Deckel)** erneut zu prüfen |
| **V5k** | ⚠️ **Eigener Prüfbefund zu Fables Argument:** Die Selbstbegrenzung des Falten-Sharpe bei einem einzigen Nicht-Null-Tag (**1/√(T−1)**, annualisiert ≈ 1,0) ist **nachgerechnet und korrekt**. Aber: **vier Trades erreichen bis zu 2,0** — oberhalb der Unterscheidbarkeitsschwelle von **Sharpe ≈ 1,6** bei N = 653. Das Glückstreffer-Szenario ist **begrenzt, nicht abgeschafft**; es trägt der **Median über sieben Falten**, nicht die √k-Grenze. Schlussfolgerung bleibt gültig |
| **V5f** | ⭐ **AUFGEKLÄRT 15.09.: Die „3 von 24" waren das MINDESTTRAINING, keine Survivorship-Verzerrung.** `faltenplan.py` Zeile 151 verlangt Historie `mindesttraining` Jahre **vor** Faltenbeginn. Ohne Mindesttraining (Verfahren B): **erste Falte 2019**, **7 Selektionsfalten** (Tagesbots), Symbole je Falte 6/9/13/13/13/17/18, Bestätigung 23. **Nur noch 6 von 24 Symbolen ohne Falte** — BMT, ENSO, PUMP, TRUMP, U, ZKC, alle **2025/2026 gelistet**. ⇒ **I10 ist KEINE Vorbedingung für TB-30b**, Frist 13.12. haltbar |
| **V5g** | ⚠️ **`elliott_wave` erreicht die Mindestzahl nicht:** nur **3** Doppeljahr-Falten (2019-20, 2021-22, 2023-24), Registertext 4b verlangt **4**. Nach 4c wäre er **„unterbestimmt"** — nicht selektiert, behält heutige Parameter. ⚠️ Das sind ausgerechnet die Parameter, die nach dem **negativ korrelierten** Mass gewählt wurden. **An Fable zurückgefragt** |
| **V5d** | ⚠️ **Drei Einwände gegen Fables Antwort, zurückzufragen:** (1) **Registertext 1c** — „Falte mit <10 Trades zählt 0" bevorzugt systematisch **häufig handelnde** Parametersätze; steht quer zum Kostenbefund von 0,30 pp je Round Trip. (2) **Registertext 3d ist ein Strategiewechsel** — er ändert das live gehandelte Universum von 25 festen Paaren bzw. Top-150 auf eine rollierende Volumenliste; Fable lehnt genau diese Klasse Änderung bei der Kernuniversum-Variante selbst ab. (3) **Registertext 3 zieht I10 vor TB-30b** — point-in-time-Universum für Krypto UND Aktien plus Beschaffung delisteter Historien. **89 Tage bis zur Frist. Umfang kürzen oder Frist verschieben — Betreiberentscheidung** |
| **V5e** | **Zwei von Fables drei Unsicherheiten erledigt (15.09.):** `elliott_wave`-Stundenhistorie reicht bis **2017-08-17** (TB-34 hat 1h nativ geladen) → bei Doppeljahren **4 Selektionsfalten**, Mindestzahl erfüllt, Bot **nicht** unterbestimmt. Und `data.binance.vision` führt mutmasslich delistete Paare — die offizielle Binance-Doku nutzt `ADABKRW` (seit 2020 delistet) als Beispiel; ⚠️ das Hilfsskript listet aber nur **laufende** Paare, die historische Symbolliste braucht das Verzeichnis des Speichers, **aus der Cloud nicht erreichbar** |
| **V5b+** | ⚠️ **Gebündelt an Fable, bestehender Chat (15.09.2026):** `RUECKFRAGE_registerluecken.md` stellt **vier** Fragen — A3 (Bootstrap, Mindest-Ereigniszahl), A4 (Faltenzuordnung an der Grenze), **T34.9** (11 von 24 Symbolen in keiner Selektionsfalte) und **T34.10** (Mindesttraining 4 oder 2 Jahre). *Alle vier lauten im Kern gleich: was muss im Register stehen, bevor selektiert wird* |
| **V5b** | ⚠️ **Vier Lücken aus TB-33 ins Register nachtragen, bevor TB-30b läuft** (Journal **AM**). **Aufgeteilt am 15.09.2026:** **A3** (Bootstrap-Verfahren, Mindest-Ereigniszahl — in TB-30a **gar nicht geregelt**) und **A4** (Faltenzuordnung an der Grenze) → **Fable, bestehender Chat**, weil das Register aus seinen Vorabfestlegungen stammt (AF/AH). **A1** (Instrument/Universum namentlich) und **A2** (Nebenzellen erschöpfend aufzählen statt als Bereich) → in dieser Sitzung formulieren. Der **Nachtrag selbst** ist eine eigene Cloud-Aufgabe, **erst nach TB-34**, weil er den neuen Datenstand-Hash tragen muss. ⚠️ **Korrektur zu Journal AM:** A4 ist dort als „klein und harmlos" eingeordnet — das gilt für S-E1 (395 nicht überlappende Monatswechsel), **nicht für TB-30b**: Trades mit 4 bis 21 Tagen Haltedauer und bis zu 20 gleichzeitigen Positionen liegen massenhaft auf Faltengrenzen, und die drei möglichen Regeln liefern **verschiedene Faltenmediane** — also verschiedene Selektionsergebnisse. *Der Nulltest hat sie gefunden, solange sie nichts kosten* |
| **V5** | **Das Rang-3-Skript und der Zufalls-Timing-Test gehören ins eingefrorene Auswertungsskript** — Abbruchkriterium (c) braucht die Beta-Bereinigung. Ohne sie ist der Vollständigkeitstest nicht bestanden |
| **V6** | **Agent 2 in den TB-30b-Umfang.** Er optimiert seit dem 13.09. auf dem **chronologischen** Mass, und der Satz *„es gilt das chronologische"* ist **fest verdrahtet** — seit der Entscheidung für den Kapital-Drawdown ist er falsch |
| **V7** | **Kürzel-Präfix `S-`** in den Journal-Blöcken I, U, V, X, AF setzen, damit „G1 gestrichen" nicht das falsche G1 trifft |

---

## Rückblicke 2b bis 2r — ins Archiv verschoben (20.09.2026, TB-60)

Die sechzehn Blöcke `2b` bis `2r` (Rückblicke auf TB-34 bis TB-55; ein Block `2l`
wurde nie vergeben) stehen seit dem 20.09.2026 **zeichengleich** in
`BACKLOG_ARCHIV.md`. Bezeichner und Nummern sind unverändert; Nachweis in
`docs/ERGEBNIS_TB-60_backlog_archiv.md`.

| Bezeichner | Titel | Datum | Archiv |
|---|---|---|---|
| `2b` | Aus TB-34 | 15.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2b` |
| `2c` | Aus TB-45 | 17.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2c` |
| `2d` | Aus TB-46 und den beiden Fable-Runden | 17.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2d` |
| `2e` | Aus TB-46b, TB-47 und den Fable-Runden | 18.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2e` |
| `2f` | Aus TB-47, Snapshotgrenze | 18.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2f` |
| `2g` | Aus TB-48, Registernachtrag | 18.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2g` |
| `2h` | Aus TB-49, die Ausnahme ins Werkzeug | 18.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2h` |
| `2i` | Aus TB-50, Dokumentationspflege | 18.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2i` |
| `2j` | Aus TB-51, Startdatei und Flackerstufe | 18.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2j` |
| `2k` | Aus TB-52, Resolver und AST-Masse | 18.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2k` |
| `2m` | Fable, Mindesttraining und Registerberichtigung | 18.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2m` |
| `2n` | TB-55: der Snapshot, der nicht gezogen wurde | 19.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2n` |
| `2o` | Vorprüfung vor TB-55 | 19.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2o` |
| `2p` | TB-55 Mac-Lauf: der registrierte Eingabezustand existiert | 19.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2p` |
| `2q` | TB-55b: Abschnitt 18, die Tatsachennotiz zum Snapshot | 19.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2q` |
| `2r` | TB-54: die acht Nachträge, und was dabei sichtbar wurde | 19.09.2026 | `BACKLOG_ARCHIV.md`, Abschnitt `2r` |

## 2s — Aus TB-56b, die Registerberichtigung (19.09.2026)

*Eingearbeitet durch TB-59 aus den Nachträgen (s), (t) und (u) — drei Nachträge derselben Sitzung desselben Abends, ein Block. Nummer `2s` im Nachtrag (s) vorgeschlagen und bei der Einarbeitung als nächste freie gemessen (höchster Block davor: `2r`).*

| # | Punkt |
|---|---|
| **T56b.1** | ⭐⭐ **DER SATZ BEGRÜNDETE SICH SELBST.** Abschnitt 15.6 Punkt 2 sagte *„die Schranke dafür ist das Register, nicht die Datenlage"*. **Gemessen: kein Registertext nennt eine Jahreszahl** — 4a sagt „erstes Jahr mit Daten und Vorlauf", 3b (a) sagt „ab einem handelbaren Symbol". `ERSTE_MOEGLICHE_FALTE = 2019` stand **nur im Code und in diesem Satz**. Berichtigt in **Abschnitt 21**, null entfernte Zeilen. *Fehlerklasse C4: eine Angabe, die nicht sagt, gegen was sie prüft* |
| **T56b.2** | ⭐ **BETREIBERENTSCHEIDUNG 19.09.2026: Wo 4a und 3b (a) verschiedene erste Falten ergeben, bindet 3b (a).** Betroffen genau ein Bot: `t3_supertrend`, dessen Zeile dadurch **unverändert** bei 2019 / 7 Falten bleibt (Loader `MIN_HISTORY_DAYS = 730`, BTC/ETH handelbar erst ab 2019-08-17, Falte 2018 hat 0 Symbole). ⚠️ Begründung **strukturell**, nicht ergebnisbezogen: eine Falte ohne handelbares Symbol erzeugt keinen Falten-Sharpe |
| **T56b.3** *(berichtigt)* | ⭐ **BETREIBERENTSCHEIDUNG 19.09.2026: Die Berichtigung der Benchmark-Tabelle (Sperrliste Punkt 4) wird EINMAL vollzogen, nach **TB-61**, für alle neun Bots.** *(Bis 20.09.2026 stand hier „nach TB-31“. TB-31 ist erledigt; der Lauf, auf den gewartet wird, heißt jetzt TB-61.)* `DD_Toleranz` wird dabei bei `rsi2_mean_reversion` und `volatility_breakout` **nachgiebiger** (100 % Exposure: −8,55 → **−12,89**); die Zahlen stehen gemessen in Registerabschnitt 21.6, die Entscheidung in **21.9**. ⭐ **Der Grund ist die Reihenfolge, nicht die Richtung:** fünf von neun Bots haben gemessen **keine** `DD_Toleranz` (Krypto, `status: platzhalter`), eine Berichtigung jetzt bewegte die gesperrte Zahl zweimal. *(Begriff nach Fable 20.09.2026, Register 23.6: vor dem Tag Berichtigung des Registers und Bug-Fix am Auswerter; „Amendment“ erst nach dem Tag. Bis TB-66 stand hier zweimal „Amendment“.)* ⚠️ **Ausdrücklich nicht entschieden wurde, die Lockerung zu vermeiden** — sie steht so oder so und wird durch Warten nicht kleiner |
| **T56b.4** | ⚠️ **Die vier Aktien-Bots teilen keinen Faltenplan mehr.** `elliott_wave_stocks` und `turtle_soup_stocks` beginnen **2017**, `rsi2_mean_reversion` und `volatility_breakout` **2018**. Abschnitt 3 des Registers sagt dreimal *„teilt Universum und Faltenplan mit den übrigen aktien-Bots — dieselbe Tabelle"*. **Diese Prämisse trägt nicht mehr**; gehört mit T56b.3 in denselben Zug |
| **T56b.5** *(berichtigt 20.09.2026)* | ⚠️ **Fünf von neun Bots haben KEINE `DD_Toleranz.`** Die Krypto-Bots stehen in **beiden** Benchmark-Tabellen als `status: platzhalter` mit leerer `dd_toleranz`. **Gemessen, nicht vermutet.** Die Drawdown-Bedingung (Abschnitt 4) braucht die Zahl — **vor dem Tag.** ⭐⭐ **Berichtigt: es hängt NICHT an TB-31** — der Halbsatz ist entfernt, nicht danebengestellt. **Der Platzhalter hängt an einer Codezeile:** `research/vorregistrierung/faltenplan.py:216` setzt in `plan_krypto()` hart `"status": "platzhalter"`; `benchmark.py:176` prüft `if p["status"] != "endgueltig"` und überspringt den Bot mit `continue`. ⇒ **TB-61** |
| **T56b.6** | **Zwei Code-Kopien der Schranke stehen noch:** `research/faltenplan_neun/faltenplan_neun.py:120` und `research/krypto_historie/faltenplan.py:64`. ⚠️ **Der Kommentar in `faltenplan_neun.py:119` verweist auf `registerdaten.py::ERSTE_MOEGLICHE_FALTE` — eine Konstante mit 0 Treffern im Quelltext.** Eigene Aufgabe **mit Mac-Lauf**; Freigabe liegt seit TB-56 vor, nicht in Anspruch genommen. ⚠️ **Dabei mit zu lösen: `test_faltenplan_neun.py:519` (Probe F) verfälscht genau diese Konstante** — fällt sie weg, misst die Probe nichts mehr (A5) |
| **T56b.7** | **„Änderung an Registertext 5f" ist nicht spezifiziert.** Die Übergabe vom 19.09. führt sie als Punkt; **gemessen: im gesamten Repo steht nirgends, worin sie bestehen soll** (einziger Treffer ist die Übergabezeile selbst). Der offene Teil von 5f — der fehlende Lock-Hash — ist mit Abschnitt 20 geschlossen. **Nichts erfunden; Rückfrage an den Betreiber** |
| **T56b.8** | **Abschnitte 18 und 20 bestehen den Tatsachennotiz-Test** (jeder Satz Messwert mit Herkunft oder Verweis, Schlussabsatz nennt die Grenzen). ⚠️ **Ein Formbefund:** beide verweisen auf *„die Form der Tatsachennotiz zu 4d (Abschnitt 15.6)"* — und genau diese Tabelle ist jetzt ERSETZT. Der Verweis bleibt gültig (er zeigt auf die Form), ist aber in Abschnitt 21.7 festgehalten, damit er nicht stillschweigend in die Irre führt |

*T56b.3 steht in der berichtigten Fassung aus dem Schlussblock des Nachtrags (s) („Berichtigung zu T56b.3 in diesem Nachtrag — die Entscheidung ist gefallen"); die ursprüngliche Fassung „OFFEN, BETREIBER" ist nicht übernommen, wie der Nachtrag es verlangt.*

⇒ ⚠️⚠️ **BERICHTIGT AM 20.09.2026 — der Satz, der hier stand, ist
entfernt.** Er lautete *„Damit rückt TB-31 (Krypto-Falten) auf die Kette vor den
Tag"* und setzte voraus, dass TB-31 noch aussteht. **Gemessen an `79742d1`: TB-31
ist erledigt (PR #105), TB-34 hat den Kursbestand neu aufgebaut (`data/`: 223
Dateien, gezählt), und die Krypto-Falten stehen in Registerabschnitt 21.** Die
Bedingung, auf die fünf Bots warten, ist eingetreten — **nur sagt es ihnen
niemand.**

⚠️⚠️ **Und dabei ein grösserer Befund, der vorher niemandem aufgefallen ist:
`benchmark_drawdowns.json` ist auch für die VIER AKTIEN-BOTS überholt.** Sie
stehen dort als `status: endgueltig` mit Falten **ab 2019** — nach
Registerabschnitt 21 beginnen sie **2017** (`elliott_wave_stocks`,
`turtle_soup_stocks`) bzw. **2018** (`rsi2_mean_reversion`,
`volatility_breakout`). Die Datei trägt noch die Falten der entfernten Schranke.
⭐ *Ein Zustand, der sich selbst als fertig bezeichnet, ist gefährlicher als
einer, der sich Platzhalter nennt.*

⇒ ⭐ **Damit erklärt sich der eine unerwartet rote Test vollständig:**
`auswertung.py:237` liest `eintrag["falten"][z["falte"]]`, sucht die Falte `2017`
und findet in der Tabelle erst `2019`. *Nicht gemessen, sondern erschlossen:
dass er nach dem neuen Lauf grün wird. Das ist zu prüfen, nicht vorauszusetzen.*

⇒ **Die Kette vor dem Tag heißt jetzt TB-61**
(`docs/auftraege/MAC_TB-61_benchmark_neun.md`, beauftragt am 20.09.2026 mit
`496bfa5`): Ausgabeschalter in `benchmark.py`, `plan_krypto()` liefert den
gemessenen Plan, Lauf **daneben** nach `benchmark_drawdowns_neu.json`.
⛔ **Die gesperrte Datei bleibt byteweise unverändert** (Registerabschnitt 21.9);
SHA-256 `a163c498…36d1ee`, am 20.09. nachgemessen, ist der Nachweis.
**Die Berichtigung der Tabelle selbst braucht danach eine eigene Betreiberfreigabe** *(bis TB-66: „Das Amendment selbst …“; Begriff nach Register 23.6)*. ⚠️ **Seit TB-66 (20.09.2026) ist TB-61 überholt:** die Tabelle nach Lesart VT liegt als `benchmark_drawdowns_vt.json` daneben (Register 23); vor dem Vollzug steht die Entscheidung W/C aus Register 23.3.

### Aus Fables Methodenantwort — Nachtrag (t)

| # | Punkt |
|---|---|
| **T56b.9** | ⭐⭐ **FABLE 19.09.: „Vorher feststehen" ist KEINE Eigenschaft von Verfahren B, sondern das, was ein Register IST.** *„Die Vorfestlegung der Prüfmenge, damit Vielfachheit zählbar bleibt."* Verfahren B ist eine Instanz; Hypothesen, Graphkanten und Kill Tests sind andere Instanzen mit anderem Index. ⇒ **Registertext, allgemeine Prüfregel**, eingetragen als **Abschnitt 22.1** — vor dem Tag, *„weil der Tag festlegt, was nach ihm die Selektion noch berühren darf."* ⭐ Damit ist der Baustein benannt, der in allen fünf Konzeptschichten unter fünf Namen vorkam |
| **T56b.10** | ⭐⭐ **DER ANLASSFALL IST MIT (B) BEANTWORTET — nachträgliche Wahl.** Zeigt ein Kill Test **nach** dem Tag, dass der Gewinner an einem Jahr hängt: Der **Befund** wird berichtet wie jeder Messwert; die **Handlung**, den Zweitplatzierten zu nehmen, ist eine nachträgliche Wahl. *„Ein Kriterium, das nicht registriert war, kann ihn nicht rückwirkend disqualifizieren — sonst ist jedes Kriterium, das jemand nach dem Lauf einfällt, eine ‚Berichtigung'."* ⭐ **(C) kollabiert** — aber in *„oder Bericht, und registriert für den nächsten Lauf"*, nicht in *„vorher registrieren oder nie"*. Der Zweitplatzierte **gewinnt oder gewinnt nicht**; gewählt wird er nie |
| **T56b.11** | ⭐ **BETREIBERENTSCHEIDUNG 19.09.2026: die drei Kill-Test-Werte kommen OHNE Schwelle ins Register** (Abschnitt 22.2) — Ertragsanteil der besten Falte, des besten Symbols, der fünf besten Trades. **N bleibt bei 653.** ⚠️ Preis benannt: Wer sie nach dem Tag zu einem Tor macht, trifft damit eine nachträgliche Wahl |
| **T56b.12** | ⚠️⚠️ **EIGENER BEFUND, der die Entscheidung im Nachhinein stützt — aber NICHT ihr Grund war:** Fables Antwort ist **vor** der Berichtigung in Abschnitt 21 entstanden. Seither hat `elliott_wave` **4** Falten, `t3_supertrend`/`rsi2_crypto` **7**, vier Bots **8**, zwei Bots **9**. ⇒ **„Ertragsanteil der besten Falte" ist über die neun Bots nicht gleich skaliert** — bei vier Falten strukturell grösser als bei neun, ohne dass der Bot schlechter wäre. Als Berichtswert unschädlich; **als Tor wäre es ein Fehler gewesen** |
| **T56b.13** | ⚠️ **ZWEI PRÄZISIERUNGEN AN FABLES BEGRÜNDUNGEN, an der Quelle nachgelesen (C1).** **(1)** *„Self-Healing Pool … den 6e ausschliesst"* — **6e verbietet dem BETREIBER das Hinaufsetzen**; ein automatisches Wiederzuschalten trifft **6d, letzter Satz** (*„Rückkehr nur über einen neuen registrierten Lauf"*). Fundstelle ungenau, Schluss überlebt. **(2)** *„sechs Falten nahe null ergeben Median ≤ 0"* — **nicht zwingend**: sind die sechs leicht positiv, ist der Median leicht positiv und (a) greift nicht. ⭐ **Der Faltenmedian ist gegen „hängt an einem Jahr" ein schwacher, kein exakter Kill Test**; Fable räumt die Lücke im nächsten Satz selbst ein. *Dieselbe Sorgfalt wie bei F8 — die genaue Fassung gehört ins Register, nicht seine* |
| **T56b.14** | ⚠️ **ABGRENZUNG, damit sie nicht verlorengeht:** Der Übergabepunkt *„die Drei-Kategorien-Regel in Registertext 0"* ist mit Abschnitt 22 **NICHT erledigt**, sondern als etwas anderes erkannt. Fable liefert die **allgemeine Prüfregel über die Prüfmenge**; **F17 bleibt eine Einordnungsregel für Änderungen** (Register Abschnitt 19). Beides zusammenzuwerfen wäre bequem und falsch |
| **T56b.15** | ⛔ **„Self-Healing Pool" aus Epic RT ist mit dem Register unvereinbar**, nicht nur unregistriert (Abschnitt 22.3). **Nicht erneut vorschlagen.** Die übrigen Decay-Regeln der Epics sind **Overlay-Kandidaten nach dem Tag**, keine Betriebsentscheidungen |
| **T56b.16** | ⭐ **Eine Falltür ist geschlossen** (Abschnitt 22.4): Die Notbremse aus 6e bleibt jederzeit zulässig — **auf einen Befund aus dem Selektionslauf gezogen, ist sie eine nachträgliche Wahl**, wird als solche protokolliert, und **niemand steigt dadurch auf** |

⇒ **Fables Anfrage vom 19.09. ist damit vollständig abgearbeitet.** Ein offener
Wartezustand auf ihn besteht nicht mehr.

### Aus T46.1, die Ausstiegspfade — Nachtrag (u)

| # | Punkt |
|---|---|
| **T46.1a** | ⭐⭐ **DER SICHERHEITSPUNKT IST GESCHLOSSEN — 9 von 9 gemessen.** Fables Frage: *„Schliesst der Bot offene Positionen, weil er sie ohne Kerze nicht bewerten kann?"* **Nein.** Jeder der neun `forward_test.py` trägt in der Ausstiegsschleife dieselbe Wache: `if symbol not in indicator_data: continue` (bei den beiden Elliott-Bots `price_data`). Zweite unabhängige Messung: **0 Treffer** für einen Schliess-Aufruf in einem Zweig, der einen leeren oder fehlenden Kursrahmen behandelt. ⇒ **Ein Parsing-Fehler oder eine fehlende Kursdatei macht bei keinem der neun einen Trade.** Beleg: `docs/ERGEBNIS_T46-1_ausstiegspfade.md`. ⚠️ Nebenbefund bestätigt: `t3_supertrend` hat den Leer-Zweig auf der **Ladeseite** nicht und überlebt nur durch das `try` (T45.3/T45.4) |
| **T46.1b** | ⚠️⚠️ **DIESELBE WACHE, ANDERE RICHTUNG — neu, niemand hat danach gesucht.** Wird der Trade übersprungen, wird an diesem Tag auch **sein Stop nicht geprüft**: Stop-Loss, Zeitbremse und Ausstiegssignal liegen sämtlich **hinter** dem `continue`. **Und die Wache ist still** — gemessen ein nacktes `continue` in **allen neun**, keine Protokollzeile, keine Meldung, kein Zähler. ⇒ **Fehlt die Kursdatei eines Symbols, ist die Verlustbegrenzung für dessen offene Position an diesem Tag ausser Kraft, und nichts sagt es.** ⭐ **Dieselbe Familie wie D1** (*„Ein Lauf, der ein Symbol auslässt, sagt es. Immer."*) — TB-45 hat die Regel auf der **Eingangsseite** durchgesetzt; die **Ausstiegsseite** hat sie nie erreicht. ⚠️ *Erschlossen, nicht gemessen: Datenausfälle und Marktbewegungen sind nicht unabhängig.* ⚠️ **Nicht gemessen: wie oft es real eingetreten ist** — das stünde in den Bot-Logs |
| **T46.1c** | ⭐ **Der Vorschlag, und ausdrücklich nicht der naheliegende.** ⛔ **Nicht** den `continue` entfernen — ohne Kerze liesse sich der Stop nur auf einem veralteten Kurs bewerten, **genau der Trade, den Fables Frage verhindern will**. ⭐ **Stattdessen melden:** eine Zeile über `shared/ladeprotokoll.py` mit Symbol, Trade-Kennung und Grund. **Ändert kein Verhalten, nur Sichtbarkeit** — dieselbe Klasse wie TB-42 Teil 1, **kein Amendment**. ⚠️ **Berührt alle neun `forward_test.py`, Sperrliste, freigabepflichtig — Betreiberentscheidung** |
| **T46.1d** | ⚠️ **REGISTERFRAGE, offen:** Registertext 7, Ergänzung I (Abschnitt 17.6) kennt den **Kein-Entscheid-Tag**. Ob ein Tag, an dem ein Symbol keine Kerze hatte und sein Stop deshalb ungeprüft blieb, darunter fällt, **steht nirgends**. Gehört geklärt, **bevor** der Backtester-Vergleich solche Tage zählt — sonst entscheidet es sich beim ersten Auftreten, und dann ist der Sieger bekannt |

## 2t — Epic AF: Autonome Strategie-Forschungspipeline

*Eingearbeitet durch TB-59 aus Nachtrag (n); Nummer `2t` dort vorgeschlagen und bei der Einarbeitung als nächste freie nach `2s` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_forschungspipeline_2026-09-19.md`.*

⭐ **Die Reihenfolge der ARBEIT an den fünf Epics ist `AF → RT → QR → KG → MI`** (Nachtrag (r), RT9): *RT braucht fast keine Vorbedingungen und macht AFs Ausgabe erst glaubwürdig.* Die Blöcke 2t bis 2x sind dagegen nach Nachtragsbuchstaben eingearbeitet, damit die Blockkette schliesst — die Blockfolge ist keine Rangfolge (TB-59).

| # | Punkt |
|---|---|
| **AF0** | ⭐⭐ **DAS EPIC IST AUFGENOMMEN UND HINTER DEM SIGNIERTEN TAG GEPARKT.** Zwei Gründe, beide strukturell: ⚠️ **(1)** Der Selektionslauf hat nicht stattgefunden; eine Maschine, die Strategien erzeugt, bevor das Verfahren einmal sauber durchlaufen ist, liefert Kandidaten **ohne registriertes Verfahren**. ⭐ **(2)** Die Pipeline ist die industrialisierte Fassung dessen, was heute von Hand geschieht — **sie erbt die Regeln dieses Registers, oder sie erbt nichts** |
| **AF1** | ⚠️⚠️ **DER TRAGENDE EINWAND: MEHRFACHTESTEN IST KEINE EIGENSCHAFT DES KANDIDATEN.** Die Vorlage führt „Multiple Testing" und „Data Snooping" als Prüfpunkte des Adversarial-Agenten. ⭐ **Ein Agent, der einen einzelnen Kandidaten ansieht, kann sie prinzipiell nicht feststellen.** ⭐⭐ *Wenn 1 000 Strategien getestet werden und 3 überleben, ist die Frage nicht, ob diese 3 gut aussehen — sondern wie viele von 1 000 zufälligen Strategien genauso gut ausgesehen hätten.* **Das ist eine Eigenschaft der Suche, nicht des Kandidaten** — und Abschnitt 16 der Vorlage (100 → 30 → 10 → 3) macht die Suche zum Kernmerkmal |
| **AF2** | ⭐⭐ **FOLGERUNG FÜR DIE ARCHITEKTUR, NICHT FÜR EINE PRÜFLISTE: die effektive Versuchszahl wird mitgeführt.** ⚠️ **Jede je getestete Variante wird gezählt, auch jede verworfene** — sonst ist der Nenner unbekannt und jede Kennzahl am Ende wertlos. **Die Signifikanzschwelle wird daran angepasst** (Deflated Sharpe Ratio, White's Reality Check, Harvey-Liu-Zhu-Abschlag — Verfahren zu prüfen, nicht vorausgesetzt). ⚠️ **Ohne diesen Zähler ist die Pipeline eine Maschine zur Erzeugung von Scheinbefunden** |
| **AF3** | ⚠️⚠️ **DIE SCHWELLEN MÜSSEN VOR DEM ERSTEN LAUF REGISTRIERT SEIN.** Abschnitt 7 der Vorlage sagt, sie sollen „nicht willkürlich festgelegt, sondern aus dem Projekt abgeleitet" werden. ⭐ **Gut gemeint — aber werden sie festgelegt, nachdem Ergebnisse vorliegen, ist es Auswahl nach Wirkung.** Genau davor schützt das Register. ⇒ **Jeder Forschungszyklus braucht seinen eigenen Zeitanker: Schwellen, Universum, Datenstand und Abbruchregeln registriert, bevor der Zyklus startet** |
| **AF4** | ⭐ **WAS DIE VORLAGE BESTÄTIGT — und das ist der grössere Teil.** *Strategy Registry mit Code Version, Data Version, Parameter Set* ⇒ **das sind Register + Snapshot (`63e4b6c8…`) + Lock (`96a5c572…`) + Codeherkunft (Abschnitt 19)**. *Adversarial Review Agent, der widerlegen soll* ⇒ **das ist Fables Rolle**, nachweislich wirksam. *Reproduzierbare Datenstände, Experiment-IDs, Artefakte* ⇒ vorhanden. *„Keine autonome KI setzt eigenständig Kapital ein"* ⇒ deckt sich mit der stehenden Betreiberregel |
| **AF5** | ⚠️ **WAS DER VORLAGE FEHLT: der Zeitanker.** Sie kennt Versionierung, aber keine **Vorregistrierung** — keine Festlegung, die vor dem Ergebnis steht und nachweislich nicht nachträglich geändert wurde. ⭐ **Das ist der Unterschied zwischen „nachvollziehbar" und „nicht nachträglich anpassbar"**, und es ist der teuerste Teil dessen, was dieses Projekt seit dem 15.09. gelernt hat |
| **AF6** | ⚠️ **NOCH NICHT GEMESSEN: die Bestandsaufnahme der Codebasis** gegen Abschnitt 13 der Vorlage (Backtesting, Datenpipeline, Bot-Runtime, Datenbank, Queue, Scheduler, API-Schicht, Logging, Experiment-Tracking, CI/CD, Tests). ⭐ **Rein lesend, ortsunabhängig, ohne Sitzung durchführbar** — sie gehört **vor** jede Feature- und Task-Struktur. *Ohne sie wäre die Backlog-Struktur geraten* |

---

### Epic AF — vorläufige Gliederung

⚠️ **Die Reihenfolge folgt technischen Abhängigkeiten, nicht dem Nutzen.**
⭐ **Alle Features sind hinter dem signierten Tag geparkt**, ausser AF-F0.

```
EPIC AF — Autonome Strategie-Forschungspipeline
 ├── AF-F0  Bestandsaufnahme und Architekturentscheidungen   [JETZT, rein lesend]
 │    ├── AF-T0.1  Codebasis gegen Abschnitt 13 der Vorlage messen
 │    ├── AF-T0.2  Überschneidungen mit Register/Snapshot/Lock benennen
 │    └── AF-T0.3  Offene Architekturfragen an Fable (AF1–AF3)
 ├── AF-F1  Versuchszählung und Signifikanz                  [Grundlage von allem]
 │    ├── AF-T1.1  Zähler über ALLE Varianten, auch verworfene
 │    ├── AF-T1.2  Verfahren zur Schwellenanpassung prüfen und eines registrieren
 │    └── AF-T1.3  Abbruchregeln, die den Zähler nicht verfälschen
 ├── AF-F2  Strategie-Spezifikation, deterministisch reproduzierbar
 ├── AF-F3  Automatisiertes Backtesting auf bestehender Infrastruktur
 ├── AF-F4  Robustheitsprüfung (OOS, Walk-Forward, Parameterstabilität, Regime)
 ├── AF-F5  Adversarial Review — Rolle, Abgrenzung zu Fable
 ├── AF-F6  Strategy Registry mit Statusmaschine
 ├── AF-F7  Research-Agent (Quellenlage, Kosten, xAI/Grok prüfen)
 ├── AF-F8  Paper Trading als Pflichtstufe
 ├── AF-F9  Generationen und Mutation            [bewusst spät]
 └── AF-F10 Portfolio-Ebene, Korrelation, gemeinsame Ausfälle  [bewusst spät]
```

**Abhängigkeiten, die nicht verhandelbar sind:**

| | |
|---|---|
| ⚠️⚠️ **AF-F1 vor allem anderen** | Ohne Versuchszählung erzeugen F3–F5 Zahlen, die niemand deuten kann |
| ⚠️ **AF-F2 vor AF-F3** | Eine Strategie, die nicht deterministisch reproduzierbar ist, ist nicht testbar |
| ⚠️ **AF-F6 vor AF-F7** | Ein Research-Agent ohne Registry erzeugt Ideen, die niemand wiederfindet |
| ⚠️ **AF-F8 vor jedem Live-Gedanken** | Betreiberregel, Abschnitt 12 der Vorlage |
| ⭐ **AF-F9 und F10 bewusst zuletzt** | Mutation über Generationen vervielfacht die Versuchszahl — **erst wenn F1 trägt** |

---

### Risiken, benannt

| | |
|---|---|
| ⚠️⚠️ **Scheinbefunde im industriellen Massstab** | AF1/AF2. **Das Hauptrisiko**, und es ist nicht durch Sorgfalt am Einzelfall behebbar |
| ⚠️ **Schwellen nach Ergebnis** | AF3 |
| ⚠️ **Kosten** | Abschnitt 17 der Vorlage. ⭐ Ein Budget je Zyklus **vor** dem Zyklus, nicht danach |
| ⚠️ **Aufmerksamkeit** | Der laufende Selektionslauf ist nicht fertig. **Ein zweites grosses Vorhaben parallel gefährdet das erste** |
| ⚠️ **Secrets in erzeugtem Code** | Abschnitt 18 der Vorlage nennt es selbst. ⭐ Deckt sich mit den stehenden Secrets-Regeln |

---

### MVP — die kleinste sinnvolle erste Fassung

⭐ **Nicht „eine Strategie automatisch erzeugen", sondern: EIN Forschungszyklus
mit N = 1, vollständig protokolliert** — Idee, Spezifikation, Implementierung,
Backtest, Robustheit, Adversarial Review, Ergebnis, **und der Versuchszähler
steht auf 1**.

⚠️ **Erst wenn dieser eine Zyklus reproduzierbar durchläuft, wird
parallelisiert.** *Die Vorlage sagt es selbst: „ohne dass die Ergebnisse nicht
reproduzierbar werden."*

## 2u — Epic MI: KI-Marktverständnis und adaptive Allokation

*Eingearbeitet durch TB-59 aus Nachtrag (o); Nummer `2u` dort vorgeschlagen und bei der Einarbeitung als nächste freie nach `2t` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_marktverstaendnis_2026-09-19.md`.*

| # | Punkt |
|---|---|
| **MI0** | ⭐⭐ **AUFGENOMMEN, GEPARKT — und zwar HINTER Epic AF.** ⚠️ **Der Allokator setzt einen Pool von 100–1 000 validierten Strategien voraus. Wir haben neun, und der Selektionslauf hat nicht stattgefunden.** ⭐ **Ohne Pool hat der Allokator nichts zu verteilen** — das ist keine Priorisierung, sondern eine Abhängigkeit |
| **MI1** | ⭐⭐ **WAS DIE VORLAGE RICHTIG ENTSCHEIDET, und es ist mehr als beim ersten Konzept.** *(a)* **Das LLM erzeugt einen strukturierten Zustand, keine Order** — deterministische Modelle entscheiden. *(b)* *„Ein LLM-generierter Text darf nicht als alleinige Begründung für eine Kapitalentscheidung dienen."* *(c)* **Die Risk Engine ist LLM-fest.** *(d)* **Shadow Mode vor jedem Einsatz.** ⭐ **Alle vier decken sich mit den stehenden Regeln dieses Projekts** |
| **MI2** | ⚠️⚠️ **DER STRUKTURELLE HAUPTBEFUND: Regime-bedingte Kennzahlen vervielfachen den Suchraum und zerlegen die Stichprobe.** Abschnitt 10 will je Strategie **eine Kennzahl je Regime** (`TREND_HIGH_VOL: 2.1`, `PANIC: −0.8`). ⚠️ **Wie viele PANIC-Episoden gibt es in den Daten? Eine Handvoll.** Bei 9 Regimen × 100 Strategien sind es **900 Zellen**, die meisten fast ohne Daten — ⭐⭐ **und es wird auf ihnen ausgewählt.** **Das ist Mehrfachtesten (K2p — *im Nachtrag (o) als `K2r` bezeichnet; die Regel aus Nachtrag (n) ist als `K2p` vergeben*), nur gefährlicher: die Zellen sehen aus wie Wissen, nicht wie eine Suche** |
| **MI3** | ⚠️⚠️ **VINTAGE-DATEN SIND EINE HARTE VORBEDINGUNG, KEIN PRÜFPUNKT.** Abschnitt 19 nennt *„revised macro data"* und *„delayed news"* in einer Aufzählung. ⭐ **Die Folge ist härter, als die Aufzählung nahelegt:** Makrodaten werden **nachträglich revidiert**; wer mit der revidierten Reihe backtestet, hat **Look-ahead per Konstruktion** — nicht abgeschwächt, sondern ungültig. **Dasselbe für Nachrichten:** der Zeitpunkt, zu dem eine Meldung **handelbar** war, ist nicht ihr Veröffentlichungsstempel. ⇒ ⚠️ **Ohne Daten „wie damals erstveröffentlicht" ist der Backtest des KI-Layers wertlos. Das ist eine Architekturentscheidung, die VOR allem anderen fällt** |
| **MI4** | ⚠️ **MARKET MEMORY IST EIN AUSWAHLVERFAHREN IN VERKLEIDUNG.** Abschnitt 7 sucht ähnliche historische Episoden und fragt, was danach funktionierte. ⭐ **Bei reichem Merkmalsraum und wenigen Episoden sieht immer irgendetwas ähnlich aus** — und **das Ähnlichkeitsmass ist selbst ein frei gewählter Parameter**. ⇒ **Das Mass wird vor der Benutzung registriert, und die Zahl der Vergleiche wird gezählt** (K2p — *im Nachtrag (o) als `K2r` bezeichnet; die Regel aus Nachtrag (n) ist als `K2p` vergeben*) |
| **MI5** | ⭐ **DER ALLOKATOR IST SELBST EINE STRATEGIE und wird wie eine getestet.** Seine Umschichtungsfrequenz, seine Schwellen, seine Korrelationsfenster sind **Parameter, die überangepasst werden können.** ⚠️ **Abschnitt 19 sieht das richtig** — der Nachtrag hält es als Regel fest: **dieselbe Registrierung, dieselbe Versuchszählung, derselbe Zeitanker wie für jede andere Strategie** |
| **MI6** | ⭐ **PREDICTION TARGETS: die Vorlage hat hier vermutlich recht, und es ist prüfbar.** *„P(Volatilitätsausweitung)"* statt *„steigt BTC morgen"* ist statistisch günstiger — mehr Ereignisse, symmetrischere Verteilung, weniger Abhängigkeit von der Driftschätzung. ⚠️ **Aber es ist eine Hypothese und keine Tatsache** — ⭐ **als Research-Task aufnehmen, nicht als Festlegung** |
| **MI7** | ⭐ **WAS HEUTE SCHON BILLIG UND NÜTZLICH WÄRE — und trotzdem warten muss:** „Strategy Performance by Regime" für **unsere neun Bots** ist eine reine Auswertung vorhandener OOS-Daten. ⚠️⚠️ **Nicht vor dem signierten Tag** — eine regimebedingte Auswertung der neun könnte die Selektionsentscheidung beeinflussen, und das wäre Auswahl nach Wirkung |
| **MI8** | ⚠️ **NOCH NICHT GEMESSEN: die Bestandsaufnahme** gegen Abschnitt 22 der Vorlage (Datenbank, Queue, Vector-DB, Feature Store, Experiment-Tracking, News-Daten, Execution Engine). ⭐ **Gemeinsam mit AF6 zu erheben** — rein lesend, ortsunabhängig, ohne Sitzung |

---

### Epic MI — vorläufige Gliederung

⚠️ **Reihenfolge nach Abhängigkeiten. Alles hinter Epic AF, und AF ist hinter
dem Tag.**

```
EPIC MI — KI-Marktverständnis und adaptive Allokation
 ├── MI-F0  Vintage-Datenarchitektur              [VOR allem anderen, MI3]
 │    ├── MI-T0.1  Welche Makroreihen gibt es als Erstveröffentlichung?
 │    ├── MI-T0.2  Nachrichten: Handelbarkeitszeitpunkt statt Veröffentlichung
 │    └── MI-T0.3  Architekturentscheidung: ohne Vintage kein KI-Layer-Backtest
 ├── MI-F1  Marktzustand aus quantitativen Merkmalen   [ohne LLM beginnen]
 ├── MI-F2  Regime-Erkennung + ⚠️ Stichprobengrösse je Regime messen (MI2)
 ├── MI-F3  Historische Episodendatenbank
 ├── MI-F4  Ähnlichkeitsmass — registriert vor Benutzung (MI4)
 ├── MI-F5  Strategieleistung je Regime          [nach dem Tag, MI7]
 ├── MI-F6  Allokator als registrierte Strategie (MI5)
 ├── MI-F7  Backtest des gesamten KI-Layers      [setzt MI-F0 voraus]
 ├── MI-F8  Shadow Mode
 ├── MI-F9  Risk Engine — Integration, LLM-fest
 ├── MI-F10 Ereignisextraktion (Grok/xAI prüfen)  [nach MI-F0]
 ├── MI-F11 Erklärbarkeit aus Messwerten, nicht aus Text
 ├── MI-F12 Portfolio-Ebene: Cluster erkennen
 └── MI-F13 Information Arbitrage                 [Research, spät]
```

**Abhängigkeiten, die nicht verhandelbar sind:**

| | |
|---|---|
| ⚠️⚠️ **MI-F0 vor MI-F7** | Ohne Vintage-Daten ist der KI-Layer-Backtest **ungültig**, nicht schwach |
| ⚠️⚠️ **Epic AF vor Epic MI** | Kein Pool, kein Allokator (MI0) |
| ⚠️ **MI-F2 misst die Stichprobe, bevor sie Zellen bildet** | Ein Regime mit fünf Episoden liefert keine Kennzahl (MI2) |
| ⭐ **MI-F1 beginnt OHNE LLM** | Quantitative Merkmale zuerst; das LLM kommt dazu, wenn die Grundlage misst |
| ⚠️ **MI-F5 nach dem signierten Tag** | MI7 |

---

### Risiken, benannt

| | |
|---|---|
| ⚠️⚠️ **Regime-Zellen als Scheinwissen** | MI2. ⭐ **Das Hauptrisiko dieses Epics**, und es ist schwerer zu sehen als beim Vorgänger, weil die Zahlen nach Erkenntnis aussehen |
| ⚠️⚠️ **Look-ahead durch revidierte Daten** | MI3. **Baut man darauf, ist alles Folgende ungültig** |
| ⚠️ **Ähnlichkeitssuche findet immer etwas** | MI4 |
| ⚠️ **Der Allokator überangepasst** | MI5 |
| ⚠️ **Kosten** | Mehrere LLM-Schichten, dauerhaft laufend. ⭐ Budget je Zyklus **vor** dem Zyklus |
| ⚠️ **Aufmerksamkeit** | **Zwei grosse Epics und ein unfertiger Selektionslauf.** *Das grösste Risiko ist nicht technisch* |

---

### MVP

⭐ **Nicht der Allokator. Sondern: ein Marktzustand aus rein quantitativen
Merkmalen, über die vorhandenen 223 Kursdateien, ohne LLM und ohne
Nachrichten** — und die Messung, **wie viele Episoden je Regime überhaupt
vorliegen** (MI2).

⚠️ **Ergibt diese Messung, dass die meisten Regime unter einer brauchbaren
Stichprobengrösse liegen, ist das kein Rückschlag, sondern das Ergebnis** —
und es verhindert, dass darauf ein Allokator gebaut wird.

## 2v — Epic QR: Alpha-Discovery-Labor

*Eingearbeitet durch TB-59 aus Nachtrag (p); Nummer `2v` dort vorgeschlagen und bei der Einarbeitung als nächste freie nach `2u` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_alpha_labor_2026-09-19.md`.*

| # | Punkt |
|---|---|
| **QR0** | ⭐⭐ **DAS METHODISCH REIFSTE DER DREI KONZEPTE.** Es nennt Mehrfachtesten als **eigenes technisches Thema** (§16, nicht als Prüflistenpunkt wie bei AF), verlangt einen **Prediction Ledger ohne nachträgliches Umschreiben** (§8/§9), **Agentenkalibrierung mit Brier Score** (§7) — ⭐ **und ein MVP-Erfolgskriterium, das ausdrücklich NICHT „wir haben eine profitable Strategie gefunden" lautet** (§24) |
| **QR1** | ⭐⭐ **DAS NULLMODELL IST GENANNT, ABER NICHT ENTWORFEN — und es ist der Kern.** §24 fragt: *„Sind die Hypothesen besser als zufällige Hypothesen?"* ⚠️ **Das verlangt, tatsächlich zufällige Hypothesen zu erzeugen und durch dieselbe Pipeline zu schicken** — nicht als Kontrolle nebenbei, sondern als **gleichrangige Komponente.** ⭐ **Es ist die billigste Art herauszufinden, dass das Ganze Rauschen ist**, und der Grund, warum solche Systeme es meist nicht tun: es ist demütigend und es funktioniert |
| **QR2** | ⚠️⚠️ **SPEICHERN IST NICHT BEWEISEN.** §9 verlangt, eine Prognose nach Kenntnis des Ergebnisses nicht zu verändern, und listet, was zu speichern ist. ⭐ **Speichern zeigt nicht, dass nichts verändert wurde.** Dafür braucht der Ledger **Anfügen-statt-Ändern und eine Hash-Kette** — jeder Eintrag trägt die Quersumme des vorigen. ⭐⭐ **Anders gesagt: der Prediction Ledger IST das Register, je Hypothese angewandt** — und die Maschinerie dafür steht seit heute (Snapshot, Lock, Codeherkunft, Zeitanker) |
| **QR3** | ⚠️ **EIN BRIER SCORE BRAUCHT EINE VORHER FESTGELEGTE AUFLÖSUNG.** §7 will Agenten kalibrieren. ⭐ **Das ist nur messbar, wenn Ereignis UND Auflösungszeitpunkt vor der Prognose feststehen** — sonst entsteht *„die Prognose ist irgendwie eingetreten"*. ⇒ **Jeder Ledger-Eintrag trägt eine maschinell prüfbare Auflösungsregel**, die ohne Ermessen auswertbar ist |
| **QR4** | ⚠️⚠️ **DER EDGE-DECAY-MONITOR HAT EINE FALLE.** §17 vergleicht erwartete mit tatsächlicher Leistung und schlägt bei Abweichung an. ⭐ **Drawdowns sind normal.** Ein Monitor auf blosse Abweichung schlägt **ständig** an und erkennt überwiegend Rauschen — ⚠️ **und wer daraufhin Strategien abschaltet, verkauft die Verlierer und behält die Gewinner auf einem Zufallspfad. Das ist selbst eine Strategie, und eine schlechte.** ⇒ **Die Abschaltschwelle wird aus der registrierten Eigenvarianz der Strategie abgeleitet, und die Abschaltregel wird wie jede Strategie backgetestet** |
| **QR5** | ⭐ **§25 IST DIE ZAHL, DIE ÜBER DAS GANZE PROGRAMM ENTSCHEIDET:** Kosten je validiertem Edge. ⚠️ **Ab dem ersten Tag des MVP messen, nicht später** — *ein Programm, das seine Kosten je Erkenntnis nicht kennt, kann nicht beendet werden, und genau das ist der häufigste Ausgang* |
| **QR6** | ⭐⭐ **REIHENFOLGE DER DREI EPICS, gegen die Einreichungsfolge.** Der Fluss ist **QR (Hypothesen) → AF (Strategien) → MI (Allokation)**. ⚠️ **Praktisch aber umgekehrt:** QR braucht **AFs Validierungsmaschine**, um seine Hypothesen zu prüfen — ⭐ **und AF kann mit handgeschriebenen Hypothesen arbeiten.** ⇒ **AF zuerst** (es trägt die Prüfung), **dann QR** (es industrialisiert die Ideenzufuhr), **dann MI** (es braucht einen Pool) |
| **QR7** | ⭐ **ALLE DREI KONZEPTE TEILEN EINE VORBEDINGUNG — und das ist selbst ein Befund:** Jedes setzt eine **funktionierende, registrierte Validierungskette** voraus. ⭐⭐ **Genau die bauen wir seit dem 15.09.** Die Konzepte sind nicht der nächste Schritt; **sie sind der Grund, warum der jetzige Schritt sich lohnt** |
| **QR8** | ⚠️ **NOCH NICHT GEMESSEN:** die Bestandsaufnahme (gemeinsam mit AF6/MI8) und die **vollständige Backlog-Sichtung** in fünf Durchgängen. ⭐ **Kollisions- und Ausscheidungsdurchgang fehlen für (n), (o) und (p)** — sie brauchen eine Messung am Backlog, nicht eine Einschätzung |

---

### Epic QR — vorläufige Gliederung

⚠️ **Hinter AF. Beide hinter dem Tag.**

```
EPIC QR — Alpha-Discovery-Labor
 ├── QR-F0  Nullmodell: zufällige Hypothesen durch dieselbe Pipeline  [QR1]
 ├── QR-F1  Prediction Ledger, anfügend, hash-verkettet               [QR2]
 │    ├── QR-T1.1  Eintragsformat mit maschinell prüfbarer Auflösungsregel (QR3)
 │    ├── QR-T1.2  Hash-Kette und Nachweis, dass nichts geändert wurde
 │    └── QR-T1.3  Auswertung: Brier Score, Kalibrierungskurve je Agent
 ├── QR-F2  Mehrfachtest- und FDR-Kontrolle                  [gemeinsam mit AF-F1]
 ├── QR-F3  Anomalieerkennung, quantitativ, ohne LLM
 ├── QR-F4  Hypothesenregister mit Statusmaschine
 ├── QR-F5  Hypothesenerzeugung durch Agenten                [nach QR-F0 und F1]
 ├── QR-F6  Agentenkalibrierung und Gewichtung
 ├── QR-F7  Edge-Validierung — nutzt AFs Kette, baut sie nicht neu
 ├── QR-F8  Edge-Decay-Monitor mit abgeleiteter Schwelle     [QR4]
 ├── QR-F9  Forschungskosten je validiertem Edge             [QR5, ab Tag 1]
 ├── QR-F10 Kausalitätslabor                                  [Research, spät]
 ├── QR-F11 Information Arbitrage                             [Research, spät]
 └── QR-F12 Selbstheilender Strategiepool                     [sehr spät, Governance]
```

**Abhängigkeiten, die nicht verhandelbar sind:**

| | |
|---|---|
| ⚠️⚠️ **QR-F0 und QR-F1 vor QR-F5** | **Erst das Nullmodell und der Ledger, dann die Agenten.** *Wer zuerst Hypothesen erzeugt und danach misst, hat keinen Vergleichsmassstab mehr* |
| ⚠️ **QR-F2 gemeinsam mit AF-F1** | Es ist **dieselbe Versuchszählung** — nicht zwei |
| ⚠️ **QR-F7 nutzt AFs Kette** | ⭐ **Keine zweite Validierungsmaschine.** Zwei Umsetzungen laufen auseinander (T55.8, T54.3) |
| ⚠️ **QR-F8 nach QR-F1** | Ohne Ledger keine Erwartung, gegen die abgewichen werden kann |
| ⭐ **QR-F12 zuletzt, mit Governance** | §18 der Vorlage sagt es selbst |

---

### Risiken, benannt

| | |
|---|---|
| ⚠️⚠️ **Kein Nullmodell** | QR1. **Ohne es ist jede Aussage über Agentenqualität unbelegbar** |
| ⚠️⚠️ **Ledger ohne Beweiskraft** | QR2. *Gespeichert heisst nicht unverändert* |
| ⚠️ **Kalibrierung ohne feste Auflösung** | QR3 |
| ⚠️ **Decay-Monitor als Verlustverkäufer** | QR4 |
| ⚠️ **Kosten ausser Kontrolle** | QR5. Mehrere Agenten, dauerhaft, je Zyklus |
| ⚠️⚠️ **Drei grosse Epics, ein unfertiger Lauf** | ⭐ **Das grösste Risiko, und es ist unverändert** |

---

### MVP

⭐ **Kleiner als in §23, und in dieser Reihenfolge:**

**1.** Prediction Ledger mit Hash-Kette und Auflösungsregel · **2.** Ein
quantitativer Anomaliedetektor, **ohne LLM** · **3.** ⭐⭐ **Ein Nullmodell, das
zufällige Hypothesen desselben Formats erzeugt** · **4.** Beide durch dieselbe
Prüfung · **5.** Die eine Zahl am Ende: **schlagen die echten Hypothesen die
zufälligen — und um wie viel?**

⚠️ **Ergibt sich kein Unterschied, ist das das Ergebnis des MVP**, und es hat
sich gelohnt. ⭐ *§24 sagt dasselbe; der Nachtrag macht daraus eine Komponente.*

## 2w — Epic KG: Market Causal Graph & Market Physics Engine

**Einordnung:** eigenes Epic in Abschnitt 7 (Architektur, offen), hinter AF, QR
und vor MI. Begründung unter **KG9**.

*Vermerk TB-59: nach Auftrag `MAC_TB-59` als Block `2w` in Abschnitt 2 eingearbeitet, nicht in Abschnitt 7; Nachtrag (q) nannte keine Nummer — `2w` bei der Einarbeitung als nächste freie nach `2v` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_kausalgraph_2026-09-19.md`.*

---

### KG0 — Was das Dokument richtig macht, und es ist mehr als bei den drei anderen

| Abschnitt | |
|---|---|
| **§18 „Falsification First"** | ⭐⭐ **Der beste Abschnitt aller vier Konzepte.** *„Versuche zuerst, die gefundene Beziehung zu zerstören."* Das ist die Methode dieses Projekts, in einem Satz, aus der Feder des Betreibers |
| **§17 Prediction vs Causality** | ⭐ Die Trennung ist richtig und wird fast überall verwischt |
| **§20 / §28** | ⭐ *„AI darf keine direkte Kapitalentscheidung treffen"* — und die Risk Engine bleibt unabhängig. Dasselbe Prinzip wie „kein Agent löst einen Trade aus" |
| **§1** | ⭐ *„Das System darf solche Beziehungen nicht als kausal betrachten, nur weil sie korrelieren"* — der Satz steht **vor** dem Entwurf, nicht als Fußnote danach |
| **§27** | ⭐ *„Keine subjektive ‚Profitability Score'-Bewertung erfinden"* — genau die Grenze, die ich heute Mittag selbst gezogen habe |

⚠️ **Und genau deshalb ist dieses Konzept das gefährlichste der vier.** Nicht
das schwächste — das gefährlichste. Es benennt jede Falle korrekt und entwirft
dann eine Maschine, deren Grundbetrieb das Hineinlaufen ist.

---

### KG1 — ⚠️⚠️ Die Zahl der geprüften Beziehungen muss VOR dem Lauf registriert werden

**§19 verlangt, `number_of_relationships_tested` zu *tracken*.** Das ist eine
Messung **nach** dem Lauf.

*„Eine Beispielrechnung mit 50 konkreten Knoten, 20
Verzögerungen und 4 Regimen — Annahmen des Verfassers, nicht des Konzepts —
ergibt 196 000 prüfbare Beziehungen und bei α = 0,05 rund 9 800 Scheintreffer.
Die Größenordnung, nicht die Zahl, ist die Aussage."*

⚠️ **Berichtigt 19.09.2026, 21:05** (`BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md`, Punkt 4): Im Nachtrag (q) stand hier *„Rechnung an der Struktur des Entwurfs selbst: §3 nennt 22 Knotenarten und 10 Kantenarten. Werden daraus nur 50 konkrete Knoten, 20 Verzögerungen (§4) und 4 Regime (§12) gebildet, sind das 50 × 49 × 20 × 4 = 196 000 prüfbare Beziehungen. Bei α = 0,05 liefern rund 9 800 davon ein „signifikantes" Ergebnis, wenn überhaupt kein Zusammenhang existiert."* — Das Konzept nennt 22 Knoten**arten** und 10 Kanten**arten**; die Zahlen 50, 20 und 4 sind Annahmen des Verfassers des Nachtrags, nicht des Konzepts. Der Satz oben ist die von der Berichtigung vorgegebene Ersatzfassung.

⚠️ **FDR-Kontrolle rettet das nicht**, solange die Zahl der Tests nicht vorher
feststeht. Wer 196 000 Tests rechnet, 400 „Treffer" behält und dann FDR über
diese 400 rechnet, hat den Nenner selbst gewählt — dieselbe Klasse Fehler wie
eine Selektion ohne registriertes N.

⇒ ⭐⭐ **Verfahren B, angewandt auf den Graphen:** Bevor ein Lauf beginnt, wird
registriert: welche Knoten, welche Kantenarten, welche Verzögerungen, welche
Regime, **und damit N**. Der Lauf darf N nicht verändern. Ein zweiter
Knotensatz ist ein **neuer Lauf**, mit eigener Registrierung — wortgleich zu
*„Ein zweiter Snapshot ist ein neuer Lauf."*

---

### KG2 — ⚠️⚠️ §18 ist eine Liste von Prüfungen. Eine Liste von Prüfungen ist keine Falsifikation

**§18 nennt 15 Prüfungen** — look-ahead, leakage, Zeitstempel, Survivorship,
Multiple Testing, Kosten, Slippage, Stichprobengröße, OOS-Stabilität und
weitere. ⭐ Die Liste ist gut.

⚠️ **Sie sagt nicht, welches Ergebnis die Beziehung verwirft.** Werden alle 15
gerechnet und niemand hat vorher gesagt, was „durchgefallen" heißt, überlebt
die Beziehung jedes Ergebnis — sie wird dann *eingeordnet*, nicht *geprüft*.

⇒ **Jede Beziehung braucht vor dem ersten Test ein maschinell prüfbares
Abbruchkriterium**, das die Sache benennt und nicht ihren Stellvertreter
(die Regel aus TB-55b). Und es muss **beißen können**: Prüfprinzip **B1** —
eine Probe, die nichts verwerfen kann, ist keine Probe. Praktisch: an einer
absichtlich zerstörten Beziehung (Zeitreihe permutiert) muss das Kriterium
auslösen, bevor es auf echte Daten darf.

---

### KG3 — ⚠️⚠️ `confidence` ist das gefährlichste Feld des ganzen Dokuments

**§3 führt im Graph-Eintrag ein Feld `confidence`.** Ohne Einheit, ohne
Schätzer, ohne Nullmodell.

⚠️ **Eine Zahl zwischen 0 und 1 neben dem Wort „Hypothese" wird als
Wahrscheinlichkeit gelesen, dass die Hypothese wahr ist.** Das ist sie nicht
und kann sie nicht sein. Nach zwei Wochen steht in Berichten „confidence 0,82"
und niemand weiß mehr, ob das ein p-Wert, ein Anteil, ein LLM-Urteil oder eine
Mischung ist.

⇒ **Zwei zulässige Wege, kein dritter:**
1. Das Feld nennt seinen **Schätzer** und sein **Nullmodell** im Namen
   (`oos_trefferquote_gegen_permutation`), oder
2. es gibt das Feld nicht.

⭐ **Dasselbe gilt für `stability_score` (§3) — und `confidence` ist nicht der
Einzelfall, sondern das Muster:** ein Name, der ein Urteil ausdrückt, ohne
seine Messung mitzuführen. Regel aus dem Register: **jede Zahl trägt ihre
Herkunft.**

---

### KG4 — ⚠️ §17 ist richtig, und §3 widerlegt es

**§17 verlangt:** prädiktive Beziehung und kausale Hypothese *„müssen separat
gespeichert werden"*.

**§3 speichert beide im selben Satz** — ein Eintrag mit `hypothesis`,
`relationship_type`, `confidence`, `observation_count`, `statistical_tests`,
`out_of_sample_results`.

⚠️ **`observation_count` neben `confidence` in einem Satz ist genau der
Mechanismus, der Korrelation still zu Kausalität befördert:** je öfter
beobachtet, desto höher die Zuversicht, und irgendwann liest jemand die
Kantenart `CAUSES`, wo `CO-MOVES_WITH` gemessen wurde.

⇒ **Zwei Kantenklassen, physisch getrennt, und keine Beförderung durch
Beobachtungszahl.** Eine Kante wechselt die Klasse nur durch ein Verfahren, das
vorher registriert wurde — nicht durch Anhäufung. ⭐ Praktisch heißt das: die
Kantenarten aus §3 werden in zwei Listen aufgeteilt (`CO-MOVES_WITH`,
`PRECEDES`, `CORRELATES_WITH`, `LEADS`, `FOLLOWS` → beobachtend;
`AMPLIFIES`, `SUPPRESSES`, `TRANSMITS_TO`, `REACTS_TO` → behauptend), und die
behauptenden tragen ein Pflichtfeld „Verfahren, das sie dorthin gebracht hat".

---

### KG5 — ⭐⭐ Der harte Befund: Lead/Lag ist auf den vorhandenen Daten nicht messbar

**Das ist der wichtigste Punkt dieses Nachtrags, und er ist gemessen, nicht
überlegt.**

§4 nennt als Beispiel *„Asset A → 2 min → Asset B"*. §5 verlangt
`reaction_30s`. §7 baut auf `Liquidity ↓ → Price Impact ↑ → Volatility ↑ →
Liquidations ↑`.

**Was das Projekt heute tatsächlich hat, gemessen:**

| | |
|---|---|
| Kursdateien | **223**, Namensform `{symbol}_{INTERVAL}.csv` |
| feinste vorhandene Auflösung | **1 Stunde** (`MIN_HISTORY_HOURS = 17520` bei `elliott_wave`); alle übrigen acht Bots rechnen auf **Tagesdaten** (`MIN_HISTORY_DAYS`) |
| Lückenhaftigkeit auch dort | BTCUSDT: **79 461 Kerzen, 147 fehlend**; lückenlos erst ab 2019-08-20 bei Handelsbeginn 2017-08-17 (TB-56 Teil A, `docs/belege/TB-56/teil_a_messung.txt`) |
| Orderbuch, Ticks, Funding, Open Interest, Liquidationen, Optionen | **nicht vorhanden** |

⚠️ **Berichtigt 19.09.2026, 21:05** (`BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md`, Punkt 1): Die Zeile „feinste vorhandene Auflösung" oben war **aus den Konstantennamen erschlossen, nicht aus den Daten gelesen** (`MIN_HISTORY_HOURS` sagt, dass eine Konstante Stunden zählt; es sagt nichts über die Auflösung der Daten). **Gemessen am 19.09.2026, 21:03, an den Dateinamen und den ersten Datenzeilen in `data/`:**

| Auflösung | Dateien | erste Spalte `open_time` |
|---|---:|---|
| `1d` | **174** | `1980-12-12` — Datum ohne Uhrzeit |
| `1h` | **25** | `2020-10-15 03:00:00`, Folgezeile `04:00:00` |
| `4h` | **24** | — |
| **Summe** | **223** | = der registrierte Datenstand `d9449faf…` |

⭐ **Die Aussage stimmt — und sie ist strenger als geschrieben:** *Eine Stundenauflösung existiert für 25 von 223 Dateien, sämtlich Krypto. Für alle 174 Aktiendateien ist die feinste vorhandene Auflösung ein Tag.* ⚠️⚠️ **Folge, die in (q) fehlt:** §7 des Konzepts (Cross-Asset-Übertragung `Macro Shock → Rates → USD → Equities / Crypto / Commodities`) ist die Stelle, an der Aktien und Krypto zusammenkommen. **Auf der Aktienseite gibt es dafür nur Tagesdaten.** Damit ist Cross-Asset-Übertragung nicht auf eine Stunde, sondern **auf einen Tag** beschränkt — und eine Übertragung, die innerhalb eines Handelstages abläuft, ist mit diesem Bestand grundsätzlich nicht messbar, nicht nur ungenau. ⇒ **KG-F2 wird ergänzt** (siehe Merkmalstabelle).

⇒ ⚠️⚠️ **Die kleinste auflösbare Verzögerung ist eine Stunde.** Damit sind
nicht messbar: §4 (2-Minuten-Beispiel), §5 (`reaction_30s`, `reaction_1m`,
`reaction_5m`), §7 vollständig (Liquidity-, Volatility-, Positioning-Feedback
sind Mikrostruktur), §4s *execution latency / spread / slippage / market
impact*.

⇒ **§26 Punkt 4 („Lead/Lag Discovery") ist im MVP keine Aufgabe, sondern eine
gesperrte Abhängigkeit.** ⭐ **Und das ist eine gute Nachricht, nicht eine
schlechte:** Es schrumpft das MVP auf das, was mit Tages- und Stundendaten
ehrlich untersuchbar ist — Ereignisreaktionen über Stunden bis Tage und
Cross-Asset-Übertragung. Das ist immer noch ein echtes Forschungsprogramm.

⚠️ **Die Falle, die es zu vermeiden gilt:** ein Lead/Lag auf Tagesdaten finden,
es als Mechanismus lesen und dabei nicht sagen, dass die Auflösung 24 Stunden
ist. **Jede Beziehung trägt ihre Auflösung als Pflichtfeld.**

---

### KG6 — ⚠️ §8 verspricht etwas, das mit diesen Mitteln niemand einlösen kann

**§8 sucht selbstverstärkende Schleifen `A → B → C → A`.** §8 sagt selbst
*„Nicht jede gefundene Schleife ist real"*. ⭐ Richtig — die ehrliche Fassung
ist strenger:

> ⚠️⚠️ **Keine in Zeitreihendaten gefundene Schleife kann mit diesen Mitteln
> als real gezeigt werden.** `A → B → C → A` ist von *einem gemeinsamen Treiber
> plus Autokorrelation* nicht unterscheidbar, bei keiner Stichprobengröße, ohne
> einen Eingriff. **In Marktdaten gibt es keine Eingriffe.**

⇒ **Was messbar ist, und das ist nicht wenig:** ob die von der Schleife
implizierte **bedingte Struktur** out-of-sample hält — und ob sie hält, wenn man
den vermuteten gemeinsamen Treiber herauspartialisiert. Das Epic muss das so
formulieren. ⭐ **Sonst verspricht es Mechanismus und liefert Beschreibung** —
und in einem Jahr liest jemand „validierter Feedback Loop" und glaubt, es gäbe
einen Beweis.

---

### KG7 — ⚠️ §10 und §6 sind dasselbe Verfahren, und es hat ein Freiheitsgrade-Problem

**§10 fragt:** *„Wäre die beobachtete Marktbewegung auch ohne das
identifizierte Event wahrscheinlich gewesen?"*

⚠️ **Mit einer realisierten Geschichte und ohne Kontrollgruppe ist ein
Kontrafaktum nicht messbar.** Messbar ist eine **Schätzung über eine
vergleichbare Stichprobe** — und die Auswahl dieser Stichprobe ist genau §6
(*Historical Event Similarity*).

⇒ **§6 und §10 sind ein Epic-Bestandteil, nicht zwei.** Und: ⭐⭐ **das
Ähnlichkeitsmaß muss vor seiner Anwendung registriert werden.** §6 nennt sieben
Dimensionen (Event, Surprise, Regime, Volatilität, Liquidität, Positionierung,
Cross-Asset-Zustand) ohne Gewichtung. Wer die Gewichtung nach dem ersten Blick
auf das Ergebnis wählt, hat die Vergleichsstichprobe so gewählt, dass sie die
Antwort liefert. **Das ist Selektion, nur an anderer Stelle** — und Fables
Drei-Kategorien-Regel gilt: die Grenze ist nicht die Zeit, sondern die Quelle
des Grundes.

---

### KG8 — ⭐ Die Überschneidung ist größer, als §29 C vermutet: die Hälfte ist schon da

**§29 C fragt nach Überschneidungen mit Strategy Factory, Market Intelligence
und Alpha Discovery. Die Antwort, Abschnitt für Abschnitt:**

| Abschnitt in (q) | ist bereits | |
|---|---|---|
| **§9** Causal Hypothesis Engine | **QR** — Hypothesis Registry | ⚠️ derselbe Gegenstand, anderes Substantiv |
| **§14** Relationship Lifecycle | **QR** Edge Decay + **AF** Strategy Registry | derselbe Lebenszyklus |
| **§15** Relationship Decay | **QR4** — und trägt **dieselbe Falle**: Abschwächung ist auf einem Random Walk normal | |
| **§19** Multiple Testing / FDR | **QR** — Multiple Testing | |
| **§24** Data Lineage | **QR2** Prediction Ledger — ⭐⭐ **und das ist das Register, angewandt je Hypothese** | `data_version`, `prompt_version`, `research_run_id` sind Registerfelder |
| **§25** Research Cost | **QR5** | |
| **§16** Research Council | **AF** Adversarial Review + **MI** Agents | |
| **§20 / §28** Governance | **AF/MI/QR** — und heute schon Projektregel | |

**Wirklich neu in (q), und nur das:**

| | |
|---|---|
| **§3** | der Graph als **persistente Datenstruktur** — die einzige echte Architekturneuheit |
| **§4** | Lead/Lag-Entdeckung — ⚠️ **datengesperrt, KG5** |
| **§5** | Ereignisreaktions-Datenbank — ⭐ **ohne Vorbedingung baubar** |
| **§6 + §10** | Ähnlichkeit und Kontrafaktum — ein Bestandteil, KG7 |
| **§8** | Schleifen — ⚠️ **Versprechen umformulieren, KG6** |

⇒ ⭐⭐ **Epic KG ist etwa halb so groß, wie es aussieht** — und die eigenständige
Hälfte hängt an Daten, die es nicht gibt. **Das ist der nützlichste Befund
dieses Nachtrags für die Planung:** nicht „zu viel Arbeit", sondern „ein großer
Teil ist schon eingeplant, und der Rest ist kleiner und ehrlicher, als das
Dokument vermutet".

---

### KG9 — Reihenfolge, und der eine Satz, der in §30 fehlt

**Reihenfolge der vier Schichten, begründet und nicht nach Reiz:**

```
AF  →  QR  →  KG  →  MI
```

| | |
|---|---|
| **AF zuerst** | trägt die Validierungskette und funktioniert mit handgeschriebenen Hypothesen — **ohne sie ist jede andere Schicht eine Hypothesenschleuder ohne Prüfer** |
| **QR danach** | liefert Ledger, FDR und Kalibrierung, die KG zwingend braucht (KG1, KG8) |
| **KG danach** | erzeugt Beziehungen, die MIs Regime-Engine benutzen kann; erzeugt sie vorher, fehlt der Prüfer |
| **MI zuletzt** | braucht einen Pool und einen Grund, zwischen Strategien umzuschalten |

**Und §30, der Schlussabschnitt, ist der Loop dieses Projekts mit mehr
Substantiven:**

```
OBSERVE → DETECT → CONNECT → HYPOTHESIZE → FALSIFY → VALIDATE → …
```

⚠️⚠️ **Dazwischen fehlt ein Schritt, und es ist derselbe, der diesem Projekt
zwei Wochen gekostet hat:**

```
HYPOTHESIZE  →  ⭐ REGISTER  →  FALSIFY
```

⭐ **Ohne REGISTER hat FALSIFY nichts Festgelegtes, an dem es scheitern
könnte.** Das ist der einzige Satz, den ich dem Dokument hinzufügen würde —
und mit ihm stimmt sein Schlussabschnitt.

---

### Merkmale (Features) — KG-F0 bis KG-F12

*Vermerk TB-59: die erste Spalte trägt das Präfix `KG-`, wie die Überschrift es nennt — im Nachtrag (q) stand dort `F0` bis `F12`; `F1` bis `F20` sind in dieser Datei bereits als Zeilenkennungen vergeben (Abschnitt 4, Block 2m). Verweise im Text („F0 + F8") sind wörtlich belassen und meinen die Zeilen dieser Tabelle. Betreiberentscheidung 19.09.2026.*

| | Merkmal | Vorbedingung |
|---|---|---|
| **KG-F0** | **Registrierung eines Graphenlaufs**: Knotensatz, Kantenarten, Verzögerungen, Regime, **N** — vor dem Lauf, inhaltsadressiert | — |
| **KG-F1** | **Relationship Registry** mit **zwei Kantenklassen** (beobachtend / behauptend), keine Beförderung durch Beobachtungszahl | F0 |
| **KG-F2** | **Pflichtfeld Auflösung** je Beziehung (1 h / 1 d), und ein Feld, das die feinste im Datenbestand vorhandene Auflösung nennt. ⚠️ *Ergänzt durch die Berichtigung vom 19.09.2026, 21:05, Punkt 1:* **Das Pflichtfeld Auflösung trägt je Anlageklasse einen Wert, nicht einen für den ganzen Lauf** | — |
| **KG-F3** | **Abbruchkriterium je Beziehung**, maschinell prüfbar, vor dem ersten Test, an permutierten Daten auf Bissfestigkeit geprüft (B1) | F0 |
| **KG-F4** | **Ereignisdatenbank** — Ereignisart, Zeitpunkt, Überraschung, Marktzustand; ⭐ mit Tagesdaten baubar | — |
| **KG-F5** | **Ereignisreaktion** auf den tatsächlich vorhandenen Horizonten: **1 h, 4 h, 1 d, 1 w** — ⚠️ **keine 30-s-, 1-min-, 5-min-Felder**, auch nicht leer | F2, F4 |
| **KG-F6** | **Ähnlichkeitsmaß**, vor seiner ersten Anwendung registriert, samt Gewichtung der sieben Dimensionen | F0, F4 |
| **KG-F7** | **Vergleichsstichproben-Schätzung** statt „Kontrafaktum" — mit ausgewiesener Stichprobengröße und Ausfallhäufigkeit | F6 |
| **KG-F8** | **FDR über registriertes N**, nicht über die Treffer | F0, **QR** |
| **KG-F9** | **Herkunft je Beziehung** (`data_version`, `research_run_id`, Commit, Snapshot-Name) — ⭐ dieselben Felder wie im Register | **QR2** |
| **KG-F10** | **Zerfallsüberwachung**, die zwischen „Abschwächung" und „normaler Schwankung" unterscheiden kann — ⚠️ sonst QR4s Falle | QR4 |
| **KG-F11** | **Alternativerklärungen als Pflichtfeld**, nicht als Bericht: jede behauptende Kante nennt mindestens eine geprüfte Alternative | F1 |
| **KG-F12** | **Kosten je Beziehung** — LLM, Compute, Daten; gemessen ab dem ersten Lauf | QR5 |

⚠️ **Nicht in diesem Epic und bis auf Weiteres gesperrt:** Lead/Lag unter einer
Stunde, Mikrostruktur-Feedback (§7 vollständig), Orderbuch-, Options- und
On-Chain-Auswertung, `execution latency` / `slippage` / `market impact` als
gemessene Größen. **Grund: KG5.**

---

### Nicht verhandelbare Abhängigkeiten

1. ⚠️⚠️ **Der signierte Tag.** Alle vier Schichten liegen dahinter.
2. ⚠️ **AF und QR vor KG** (KG9). KG ohne QRs Ledger und FDR ist eine
   Hypothesenschleuder.
3. ⚠️ **F0 vor jedem Lauf.** Ein Graphenlauf ohne registriertes N ist nicht
   auswertbar — nicht „schlechter auswertbar", **nicht auswertbar**.
4. ⚠️ **F2 vor F4/F5.** Wer Reaktionsfelder anlegt, die die Daten nicht
   hergeben, erzeugt Felder, die später mit irgendetwas gefüllt werden.
5. **Tick- oder Orderbuchdaten** sind Vorbedingung für §4 und §7 — und ihre
   Beschaffung ist ein eigenes Vorhaben mit eigenen Kosten, nicht ein Unterpunkt.

---

### Risiken, nach Schadenshöhe

| | Risiko | |
|---|---|---|
| **1** | ⚠️⚠️ **Falsche Entdeckungen in großer Zahl** — 196 000 Tests, ~9 800 Scheintreffer bei reinem Rauschen (KG1) | **F0 + F8** |
| **2** | ⚠️⚠️ **Kausalsprache ohne Kausalnachweis** — `AMPLIFIES`, `CAUSES`, „validierter Feedback Loop" (KG4, KG6) | **F1 + F11** |
| **3** | ⚠️⚠️ **Auflösungslüge** — ein Tagesdaten-Zusammenhang als Mikrostruktur-Mechanismus gelesen (KG5) | **F2** |
| **4** | ⚠️ **`confidence` als Wahrheitswahrscheinlichkeit gelesen** (KG3) | Feld streichen oder benennen |
| **5** | ⚠️ **Stichprobenwahl nach Ergebnis** in §6/§10 (KG7) | **F6 vor Anwendung registriert** |
| **6** | ⚠️ **LLM-Kostenexplosion** — sechs Research-Agents (§16) auf einem Graphen mit sechsstelliger Kantenzahl | **F12 ab Tag 1** |
| **7** | ⚠️ **Zeitstempelqualität** — §4 nennt sie als achte von acht Erwägungen; bei Verzögerungsforschung ist sie **die** Messung | **F2** |

---

### MVP — und es hat eine Ausgabezahl, nicht zehn

**Nicht** §26s zehn Punkte. Die kleinste Fassung, die eine echte Frage
beantwortet:

| | |
|---|---|
| Datenquellen | die **vorhandenen 223 Kursdateien**, keine neue Quelle |
| Ereignisse | **eine** Klasse, mit sicher datierbarem Zeitpunkt (z. B. FOMC-Termine) |
| Horizonte | **1 d und 1 w** — die Auflösung, die die Daten hergeben |
| Beziehungen | **vorher registriert**, zweistellige Zahl, nicht sechsstellig |
| Nullmodell | **permutierte Ereigniszeitpunkte**, gleiche Zahl, gleiche Pipeline |

**Die eine Zahl, die das MVP ausgibt:**

> ⭐⭐ **Wie viele der registrierten Beziehungen überleben out-of-sample, und wie
> viele überleben es bei zufällig verschobenen Ereigniszeitpunkten?**

⚠️ **Sind die beiden Zahlen gleich, ist die Maschine wertlos — und das ist ein
Ergebnis, kein Scheitern.** Es kostet dann eine Woche statt eines Jahres.

⭐ **Das MVP beantwortet ausdrücklich nicht:** ob sich damit Geld verdienen
lässt.

## 2x — Epic RT: Autonomous Adversarial Trading Lab

**Einordnung:** eigenes Epic in Abschnitt 7, **direkt hinter AF und vor QR** —
Begründung unter **RT9**, und das ist eine Änderung meiner eigenen Empfehlung
von vor einer Stunde.

*Vermerk TB-59: nach Auftrag `MAC_TB-59` als Block `2x` in Abschnitt 2 eingearbeitet, nicht in Abschnitt 7; Nachtrag (r) nannte keine Nummer — `2x` bei der Einarbeitung als nächste freie nach `2w` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_rotes_team_2026-09-19.md`.*

---

### RT0 — Was das Konzept richtig macht

| | |
|---|---|
| **§35** | ⭐⭐ die Umkehrung der Frage; die beste Formulierung in allen fünf Einreichungen |
| **§30** | ⭐⭐ *„Eine Verbesserung darf nur akzeptiert werden, wenn sie eine identifizierte Schwäche adressiert"* — damit ist Reparatur an eine **vorher benannte** Schwäche gebunden. Das ist Fables Drei-Kategorien-Regel, auf Strategien angewandt |
| **§28** | ⭐⭐ **den Angreifer bewerten.** Die beste Governance-Idee der fünf Konzepte — und sie fehlt in den anderen vier |
| **§10** | ⭐ *„Synthetic data darf nicht als Beweis für reale Profitabilität verwendet werden"* — richtig, und unvollständig (RT6) |
| **§9** | ⭐ *„Speichere nicht nur einen Backtest-Wert. Speichere eine Verteilung."* |
| **§13** | ⭐ harte, benannte Tests statt eines Gütemaßes |

---

### RT1 — ⚠️⚠️ Fünf der acht Kill Tests sind heute rechenbar. Deshalb müssen sie VOR der Selektion registriert werden

**Was auf dem vorhandenen Bestand ohne neue Daten, ohne LLM und ohne Agenten
rechenbar ist:**

| Kill Test (§13) | rechenbar aus | | gemessen / nicht gemessen *(Spalte aus der Berichtigung vom 19.09.2026, 21:05, Punkt 3)* |
|---|---|---|---|
| **1** Performance verschwindet nach realistischen Kosten | Kostenmodell besteht bereits | ⭐ heute | ⚠️ **nicht gemessen** |
| **3** Performance hängt an einem Jahr | die 7–9 Selektionsfalten je Bot, heute gemessen | ⭐ heute | ⚠️ **nicht gemessen** |
| **4** Performance hängt an einem Asset | 3 bis 149 Symbole je Bot, Zerlegung vorhanden | ⭐ heute | ⚠️ **nicht gemessen** |
| **5** Kleine Parameteränderungen zerstören die Performance | **das Gitter selbst** — N = 653 je Bot ist die Parameternachbarschaft | ⭐ heute | ⚠️ **nicht gemessen** |
| **7** Ohne die besten fünf Trades bricht sie zusammen | Trade-Listen in den neun `paper_trading_*.db` | ⭐ heute | ⚠️ **nicht gemessen** |
| **2** Edge nur in-sample | braucht die OOS-Kette | nach dem Tag | — |
| **6** Ein Marktereignis erklärt die Rendite | braucht die Ereignisdatenbank (Epic KG) | später | — |
| **8** Kleine Ausführungsverzögerung zerstört den Edge | braucht Auflösung unter 1 h (KG5) | gesperrt | — |

⚠️ **Berichtigt 19.09.2026, 21:05** (`BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md`, Punkt 3): *„Fünf der acht Kill Tests sind heute rechenbar"* speist Kill Test 7 aus den Trade-Listen und Kill Test 5 aus dem Parametergitter (N = 653). **Beides ist plausibel und nicht geprüft.** Ob die Datenbanken Trade-Listen in auswertbarer Form enthalten und ob die Gitterergebnisse je Parameterpunkt erhalten sind, ist **nicht nachgesehen** — während der TB-56-Sitzung waren die zwölf Datenbanken mit Quersummen gesichert; eine SQLite-Datei zu öffnen kann `-wal`- und `-shm`-Dateien anlegen und den Vergleich scheitern lassen. **Heute: alle fünf „nicht gemessen".** ⭐⭐ Das schwächt den Hauptbefund von RT1 nicht — es verstärkt ihn: die Regel gilt unabhängig davon, wie viele Tests rechenbar sind. **Was zu messen ist, bevor (r) als belegt gilt** (Berichtigung, Punkt 6): (1) Enthalten die neun `paper_trading_*.db` Trade-Listen mit Einzelergebnissen? — **auf einer Kopie**, nie am Original · (2) Hängt die Performance der vier Trendbots an wenigen Trades, und **stärker als ihre eigene Verteilung erwarten lässt**? — Kopie + Nullmodell · (3) Sind die Gitterergebnisse je Parameterpunkt erhalten (N = 653), oder nur die Sieger? — lesend. **Bis diese drei gemessen sind, trägt die Tabelle den Vermerk „nicht gemessen".**

⚠️⚠️ **Und hier liegt die Falle, und sie ist die wichtigste dieses Nachtrags:**

> **Ein Kill Test, der nach dem Blick auf den Gewinner gewählt wird, ist kein
> Kill Test. Er ist eine zweite Selektion.**

Wer nach dem Selektionslauf fünf Tests auf den Sieger rechnet und ihn
verwirft, hat den Zweitplatzierten gewählt — mit einem Verfahren, das niemand
vorher aufgeschrieben hat. **Das ist genau der Vorgang, gegen den das ganze
Register gebaut wurde**, nur mit besserem Wortschatz.

⇒ ⭐⭐ **Regel, und sie gehört in einen Registertext, nicht in den Backlog:**
Welche Kill Tests auf den Selektionslauf angewandt werden, **samt Schwellen**,
steht im Register **vor** dem Lauf — oder sie werden auf ihn **überhaupt nicht**
angewandt. Nach dem Lauf dürfen sie an neuen Kandidaten laufen, nie am
Ergebnis.

⚠️ **Praktische Folge für den Tag:** Das RT-MVP darf **nicht vor** dem
signierten Tag laufen, obwohl es könnte. Die Versuchung ist real, und sie ist
der Grund, warum dieser Punkt an erster Stelle steht.

---

### RT2 — ⚠️ §13 nennt Tests ohne Schwellen. Ein Test ohne Schwelle ist eine Meinung

*„Performance disappears after realistic transaction costs"* — **was heißt
disappears?** Null? Unter dem Zinssatz? Unter dem Buy-and-Hold? Ohne eine vorher
festgelegte Zahl entscheidet nach dem Lauf, wer hinsieht.

⇒ **Jeder Kill Test trägt drei Dinge, bevor er zum ersten Mal läuft:** die
Größe, die er misst · die Schwelle · und **was passiert, wenn sie gerissen
wird** (Status nach §13). ⭐ Das ist die Regel aus TB-55b: *ein Abbruchkriterium
benennt die Sache, nie ihren Stellvertreter.*

---

### RT3 — ⚠️⚠️ KILL TEST 7 ist so, wie er dasteht, statistisch falsch — und er würde vier unserer neun Bots erschlagen

**§13 KILL TEST 7 / §14:** *„Removing top 5 trades destroys the strategy."*

⚠️ **Das zerstört die Performance **jeder** Strategie mit rechtsschiefer
Renditeverteilung** — und bei Trendfolge ist es **definitorisch**: Trendfolge
verdient ihren gesamten Erwartungswert aus wenigen großen Gewinnern. *„Vier der neun Bots sind nach
ihrer Bauart Trendfolger; ob ihre Performance an wenigen Trades hängt, ist
**nicht gemessen**. Der Einwand gegen KILL TEST 7 gilt unabhängig davon, weil er
aus der Form rechtsschiefer Renditeverteilungen folgt und nicht aus diesen
Bots."*

⚠️ **Berichtigt 19.09.2026, 21:05** (`BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md`, Punkt 2): Im Nachtrag (r) stand hier *„Vier der neun Bots sind Breakout- oder Trendbots (`volatility_breakout`, `volatility_breakout_crypto`, `turtle_soup_*`). Wörtlich angewandt fällt jeder davon durch — nicht wegen eines Defekts, sondern wegen seiner Bauart."* — **aus den Bot-Namen erschlossen, nicht aus den Renditeverteilungen gemessen**; die Trade-Listen der neun `paper_trading_*.db` wurden nicht angesehen (gesicherte Datenbanken während der Mac-Sitzung). Der Satz oben ist die von der Berichtigung vorgegebene Ersatzfassung. ⚠️ *Die Überschrift dieses Punktes („er würde vier unserer neun Bots erschlagen") und Risiko 3 unten tragen dieselbe ungemessene Behauptung; sie stehen wörtlich, wie im Nachtrag, und gelten mit diesem Vermerk (A1: ein fehlgeschlagener Nachweis und ein leeres Ergebnis sehen gleich aus).*

⇒ ⭐⭐ **Die richtige Form braucht ein Nullmodell:** Die Abhängigkeit von den
besten fünf Trades wird gegen die Abhängigkeit verglichen, die für **diese
Renditeverteilung** zu erwarten ist — etwa indem dieselbe Entnahme an
permutierten oder aus derselben Verteilung gezogenen Trade-Folgen gerechnet
wird. **Die Frage lautet nicht „bricht sie zusammen", sondern „bricht sie
stärker zusammen als ihre eigene Verteilung erwarten lässt".**

⚠️ **Ohne dieses Nullmodell misst KILL TEST 7 die Form der Renditeverteilung
und nennt das Ergebnis Fragilität.** ⭐ **§14 und KILL TEST 7 sind derselbe
Test** — ein Epic-Bestandteil, nicht zwei.

---

### RT4 — ⚠️ §8 und §9: der Bootstrap zerstört genau das, was die Strategie ausmacht

**§8 listet `shuffle trade sequence` und `bootstrap trades`.**

⚠️ Beides zerstört die Zeitordnung — und damit Autokorrelation, Regimestruktur
und Verlustserien. **Die resultierende Drawdown-Verteilung gehört zu einer
Strategie, deren Trades unabhängig sind.** Das ist keine dieser neun.

⭐ **§8 nennt `block bootstrap` und `regime resampling` selbst** — das ist die
richtige Antwort. ⚠️ **Aber die Blocklänge ist ein freier Parameter, der das
Ergebnis verschiebt.** Wer sie nach dem ersten Blick wählt, wählt die
Drawdown-Verteilung.

⇒ **Blocklänge und Resampling-Verfahren werden vor dem Lauf registriert.** Und
`shuffle trade sequence` wird **nicht** als Robustheitsnachweis geführt,
sondern höchstens als Vergleichsgröße — mit dem Satz daneben, was sie zerstört.

---

### RT5 — ⚠️⚠️ §18: sieben Kennzahlen ohne Gewichte sind sieben Freiheitsgrade

**§18 will die Fitness aus** Return Quality + Robustness + Parameter Stability +
Regime Coverage + Execution Robustness + Drawdown Stability + Failure
Resistance **bilden, und ergänzt:** *„Keine einzelne Kennzahl soll automatisch
über die anderen dominieren."*

⚠️⚠️ **Wer die Gewichte setzt, wählt den Sieger.** Das ist derselbe Vorgang wie
eine Zielfunktion, die nach dem Lauf angepasst wird — und dieses Projekt hat
genau deswegen **Verfahren B mit Faltenmedian in den Registertext geschrieben**,
damit niemand das Maß hinterher anfassen kann.

⇒ **Die Gewichte werden vor dem ersten Evolutionslauf registriert, oder es gibt
keine zusammengesetzte Fitness.** ⭐ **Die Alternative ist besser und billiger:
Schwellen statt Gewichte.** Eine Strategie besteht oder besteht nicht — jede
Kennzahl mit eigener, vorher festgelegter Schwelle. Das erzeugt keine Rangfolge,
die man frisieren kann, und das ist ein Vorteil, kein Mangel.

---

### RT6 — ⚠️⚠️ §11 hat kein Abbruchkriterium und kein Nullmodell. So gebaut zerstört es jede Strategie

**§11 will, dass das System selbst Marktbedingungen erzeugt, unter denen die
Strategie versagt.**

⚠️ **Ein Generator, der nach Versagensbedingungen sucht, findet sie immer** —
für jede Strategie, auch für eine gute. Mit genügend Freiheit in der Erzeugung
ist jede Strategie zerstörbar. **§11 hat damit keine Stoppregel:** das Ergebnis
„gefunden" trägt keine Information.

⭐ **§10 sagt richtig:** synthetische Daten sind kein Beweis für Profitabilität.
⚠️ **Der fehlende Satz ist die Umkehrung, und er ist der wichtigere:**

> **Synthetische Daten sind auch kein Beweis für Fragilität.**

⇒ **Damit §11 etwas messen kann, braucht es drei Dinge:**
1. eine **registrierte Zulässigkeitsmenge** — welche erzeugten Marktbedingungen
   gelten als möglich, weil ähnliche vorgekommen sind;
2. eine **Kontrolle**: derselbe Generator gegen eine als robust und eine als
   kaputt bekannte Strategie. ⚠️ **Versagen beide, misst er nichts;**
3. eine **Kostengrenze**, weil die Suche unbeschränkt ist.

⭐ **Deshalb ist §11 ein V2-Punkt, nicht MVP** — und im MVP hat er nichts zu
suchen.

---

### RT7 — ⭐⭐ §28 ist die beste Idee der fünf Konzepte, und sie ist heute umsetzbar

**§28 will die Angreifer bewerten:** echte Fehlermodi, falsch Positive, falsch
Negative, Redundanz, Kosten.

⚠️ *„später bestätigte Schwachstellen"* braucht Wahrheit, die erst in Jahren
eintrifft. **Kurzfristig messbar sind zwei Dinge:**

| | |
|---|---|
| **Redundanz** | finden zwei Angriffe dasselbe? |
| ⭐⭐ **Bissfestigkeit** | **feuert der Angriff auf einer absichtlich kaputten Strategie?** |

⇒ ⭐⭐ **Das ist Prüfprinzip B1, auf Angriffe angewandt, und es ist die erste
Fähigkeit des Epics:** **Jeder Angriff wird an einer bekannt kaputten Strategie
validiert, bevor er an eine echte darf.** Eine Kaputt-Strategie ist billig
herzustellen — eine mit eingebautem Look-ahead, eine, die nur ein Jahr
funktioniert, eine, die an einem Symbol hängt. ⭐ **Ein Angriff, der auf der
Kaputt-Strategie nicht feuert, kommt nicht in den Lauf.**

---

### RT8 — Überschneidung: ein Drittel ist neu, zwei Drittel stehen schon woanders

| Abschnitt | ist bereits |
|---|---|
| **§17** Repair Agent | **AF** — Strategy Evolution |
| **§18** Adversarial Evolution | **AF** — Strategy Genome + Fitness |
| **§19** Immune System, **§21** Health | **AF** Strategy Registry + **QR** Self-Healing Pool |
| **§20** Live Shadow Red Team | **QR** Edge Decay Monitor — ⚠️ **und trägt dieselbe Falle wie QR4**: Abschwächung ist auf einem Random Walk normal |
| **§27** Research Ledger | **QR2** = das Register — ⚠️ **zum fünften Mal in fünf Konzepten derselbe Baustein unter neuem Namen** |
| **§29** Research Budget | **QR5**, **KG-F12** |
| **§23 / §24 / §25 / §26** | Integrationen, keine Bausteine |

**Wirklich neu in (r):**

| | |
|---|---|
| **§3–§9** | ⭐ **die Angriffsmaschine selbst** — und der überwiegende Teil ist mit vorhandenen Daten rechenbar |
| **§16** | **Failure Mode Database** — billig, nützlich, ohne Vorbedingung |
| **§15** | **Drawdown-Forensik** — ⭐ die Zerlegung ist heute machbar; die KI-Erklärung ist V2 |
| **§10–§11** | synthetische und erzeugte Märkte — ⚠️ **V2, RT6** |
| **§28** | ⭐⭐ **Angreiferbewertung** — einzigartig unter den fünf |

⇒ ⭐ **Das Register kommt in fünf von fünf Konzepten vor, jedes Mal unter einem
anderen Namen** (Prediction Ledger, Data Lineage, Research Ledger,
Hypothesis Registry, Versuchsregister). **Es ist nicht ein Baustein von
mehreren; es ist der Baustein, auf dem alle fünf stehen.** Das ist der
stärkste Befund über die fünf Einreichungen zusammen.

---

### RT9 — ⚠️ Ich ändere meine Reihenfolge von vor einer Stunde

**Gesagt hatte ich:** `AF → QR → KG → MI`.

**Richtig ist:**

```
AF  →  RT  →  QR  →  KG  →  MI
```

| | Begründung |
|---|---|
| **AF zuerst** | trägt die Validierungskette |
| ⭐ **RT direkt danach** | **die billigste der fünf Schichten**: keine neue Datenquelle, kein Graph, keine Agenten für den Kern. Fünf Kill Tests sind heute rechenbar (RT1) |
| | ⭐⭐ **und sie macht AFs Ausgabe erst glaubwürdig** — eine Strategie, die Angriffe überlebt hat, ist etwas anderes als eine mit gutem Backtest |
| **QR danach** | Hypothesenlabor braucht beides: Erzeuger und Angreifer |
| **KG, MI** | wie in (q) |

⚠️ **Warum ich mich korrigiere:** Ich hatte RT nach seinem Anspruch eingeordnet
(autonomes Labor, Agenten, synthetische Märkte) statt nach seinen
Voraussetzungen. **Der Kern braucht fast nichts.**

---

### Merkmale (Features) — RT-F0 bis RT-F11

*Vermerk TB-59: die erste Spalte trägt das Präfix `RT-`, wie die Überschrift es nennt — im Nachtrag (r) stand dort `F0` bis `F11`; `F1` bis `F20` sind in dieser Datei bereits als Zeilenkennungen vergeben (Abschnitt 4, Block 2m). Verweise im Text („F0 + F1") sind wörtlich belassen und meinen die Zeilen dieser Tabelle. Betreiberentscheidung 19.09.2026.*

| | Merkmal | Vorbedingung |
|---|---|---|
| **RT-F0** | ⭐⭐ **Kaputt-Strategien-Sammlung**: mindestens drei absichtlich defekte Strategien (Look-ahead, Ein-Jahr-Edge, Ein-Symbol-Edge) | — |
| **RT-F1** | ⭐⭐ **Bissprüfung je Angriff** gegen F0 — kein Angriff läuft an einer echten Strategie, bevor er auf einer kaputten gefeuert hat | F0 |
| **RT-F2** | **Registrierung eines Angriffslaufs**: welche Angriffe, welche Schwellen, welche Strategieversion, welcher Datenstand — vor dem Lauf | — |
| **RT-F3** | **Kill Tests 1, 3, 4, 5 mit Schwellen** — die vier heute rechenbaren ohne Nullmodellbedarf | F2 |
| **RT-F4** | **Kill Test 7 / §14 mit Nullmodell** (RT3) — Abhängigkeit gegen Verteilungserwartung, nicht gegen Null | F2 |
| **RT-F5** | **Parameterstabilitätskarten** aus dem **vorhandenen** Gitter (N = 653), nicht aus neuen Läufen | F2 |
| **RT-F6** | **Zeit- und Regimezerlegung** je Bot auf den gemessenen 7–9 Falten | F2 |
| **RT-F7** | **Block-Bootstrap mit registrierter Blocklänge**; `shuffle` nur als benannte Vergleichsgröße | F2 |
| **RT-F8** | **Drawdown-Zerlegung** — Start, Dauer, Tiefe, Erholung je Drawdown; ⚠️ **ohne KI-Erklärung** in Fassung 1 | — |
| **RT-F9** | **Failure-Mode-Register** mit Verknüpfung Strategie ↔ Fehlermodus | F3, F4 |
| **RT-F10** | **Angreiferbewertung**: Redundanz und Bissquote je Angriffsart | F1 |
| **RT-F11** | **Schwellen statt Gewichte** für die Gesamtbeurteilung (RT5) — jede Kennzahl mit eigener registrierter Schwelle | F2 |

⚠️ **Ausdrücklich V2, nicht MVP:** §10 synthetische Szenarien · §11 erzeugte
Märkte (RT6) · §17 Repair Agent · §18 adversariale Evolution · §19 Immune
System · KI-Erklärungen für Drawdowns.

---

### Nicht verhandelbare Abhängigkeiten

1. ⚠️⚠️ **Der signierte Tag — und hier strenger als bei den anderen vier.**
   RT könnte heute rechnen. **Genau deshalb darf es nicht**, solange die
   Selektion offen ist (RT1).
2. ⚠️⚠️ **F0 und F1 vor jedem Angriff auf eine echte Strategie.** Ein Angriff,
   dessen Bissfestigkeit nicht belegt ist, erzeugt „bestanden"-Meldungen, die
   nichts bedeuten — **Prüfprinzip A1: ein fehlgeschlagener Nachweis und ein
   leeres Ergebnis sehen gleich aus.**
3. ⚠️ **Kill Tests, die auf den Selektionslauf wirken, stehen vorher im
   Register** — samt Schwellen (RT1).
4. ⚠️ **Kein Angriff ändert eine Strategie.** Das Red Team liest; die
   Reparatur ist ein getrennter, freigegebener Vorgang (§17, V2). Die
   Sperrliste gilt unverändert.
5. **Die neun `paper_trading_*.db` sind der einzige OOS-Beleg** und nicht
   nachrechenbar. ⚠️ **Jeder Angriff, der Trade-Listen liest, liest sie aus
   einer Kopie.**

---

### Risiken, nach Schadenshöhe

| | |
|---|---|
| **1** | ⚠️⚠️ **Kill Tests als zweite Selektion** (RT1) — der einzige Punkt, der den Tag beschädigen kann |
| **2** | ⚠️⚠️ **Angriffe ohne Bissfestigkeit** erzeugen falsche Sicherheit — schlimmer als kein Angriff (A1) |
| **3** | ⚠️⚠️ **KILL TEST 7 wörtlich** erschlägt vier gesunde Trendbots (RT3) |
| **4** | ⚠️⚠️ **§11 ohne Zulässigkeitsmenge** zerstört jede Strategie und misst nichts (RT6) |
| **5** | ⚠️ **Sieben Kennzahlen ohne Gewichte** (RT5) — Selektion nach Geschmack |
| **6** | ⚠️ **Bootstrap zerstört Zeitstruktur** und liefert eine Drawdown-Verteilung für eine andere Strategie (RT4) |
| **7** | ⚠️ **Reparatur, die Performance maximiert statt die Schwäche zu beheben** — §30 verbietet es ausdrücklich; die Verbotsstelle ist die Umsetzung |

---

### MVP — und es hat eine Ausgabezahl

| | |
|---|---|
| Gegenstand | die **neun bestehenden Bots** |
| Angriffe | **Kill Tests 1, 3, 4, 5, 7** — Schwellen vorher registriert |
| Vorschaltung | ⭐⭐ **F0 + F1**: drei Kaputt-Strategien, und jeder der fünf Angriffe muss auf ihnen feuern |
| Daten | vorhandene Kursdateien, vorhandenes Gitter, Kopien der neun Datenbanken |
| Zeitpunkt | ⚠️ **nach dem signierten Tag** |

**Die eine Zahl:**

> ⭐⭐ **Wie viele der neun Bots fallen durch einen Kill Test, den der Backtest
> nicht gezeigt hat?**

⚠️ **Null ist ein Ergebnis** — dann findet systematisches Angreifen nichts, was
die heutige Methode übersieht, und das Labor hat eine Woche gekostet statt eines
Jahres. ⭐ **Mehrere ist ein besseres Ergebnis** — dann ist belegt, dass der
Backtest allein nicht reicht, und zwar an unseren eigenen Bots.

## 2y — Querschnitt über die fünf Epic-Nachträge (n) bis (r) — TB-59 (19.09.2026)

*Zwei Befunde, die über die fünf Konzepte hinweg feststehen (Auftrag `MAC_TB-59`, Abschnitt 5), als zwei Punkte mit Verweisen; die fünf Sichtungsdurchgänge sind nicht vollständig gemacht. Nummer `2y` bei der Einarbeitung als nächste freie nach `2x` gemessen.*

| # | Punkt |
|---|---|
| **QS1** | ⭐ **DIE ZERFALLSFALLE STECKT IN VIER DER FÜNF KONZEPTE** — „Edge Decay" (Block 2v, QR4 und QR-F8), „Relationship Decay" (Block 2w, KG8 §15 und KG-F10), „Live Shadow Red Team" (Block 2x, RT8 §20) und „Self-Healing Pool" (Block 2v, QR-F12; Block 2x, RT8 §19/§21): Abschwächung ist auf einem Random Walk normal, und wer daraufhin abschaltet, verkauft die Verlierer auf einem Zufallspfad. ⚠️ **Registerabschnitt 22.3 hat sie bereits entschieden:** Abschalt- und Zuschaltregeln sind **Overlay-Kandidaten nach dem Tag, keine Betriebsentscheidungen** — und der „Self-Healing Pool" ist mit Registertext **6d unvereinbar** (Block 2s, T56b.15) |
| **QS2** | ⭐ **DAS REGISTER KOMMT IN FÜNF VON FÜNF KONZEPTEN VOR, unter fünf Namen:** Prediction Ledger (Block 2v, QR2), Data Lineage (Block 2w, KG8 §24), Research Ledger (Block 2x, RT8 §27), Hypothesis Registry (Block 2w, KG8 §9), Versuchsregister / Strategy Registry (Block 2t, AF4). *Es ist nicht ein Baustein von mehreren; es ist der Baustein, auf dem alle fünf stehen* (RT8). ⚠️ **Registerabschnitt 22.1 trägt den Baustein inzwischen als allgemeine Prüfregel** (Block 2s, T56b.9) |
| **QS3** | ⚠️ **OFFEN: drei der fünf Sichtungsdurchgänge sind nicht gemacht** — Kollision und Widerspruch sind mit QS1/QS2 und der Nummernvergabe in TB-59 abgedeckt; **Abhängigkeit, Ausscheiden und Kette** stehen aus (QR8; Kettenzeile 0,97). Nicht stillschweigend ausgelassen, sondern hier eingetragen |

---

## 2z — Der Sitzungstag 20.09.2026: Start, Dokumentationsregel, Verbindungsabbrüche

*Aus Backlog-Nachtrag (v) (`nachtraege/BACKLOG_NACHTRAG_2026-09-19v.md`, 19./20.09.2026, fünf datierte Nachträge unter der ersten Tabelle, der letzte bis 15:10 fortgeschrieben), eingearbeitet 20.09.2026 durch TB-62. Die **22** Nummern `K3k`–`K4f` sind **unverändert** aus dem Nachtrag übernommen — gemessen mit `^\| \*\*(K\d[a-z])\*\*` (ohne Abschluss, ohne `-u`) über `BACKLOG.md` und `BACKLOG_ARCHIV.md`: keine davon war belegt. Bezeichner `2z` als nächste freie nach `2y` gemessen; **damit ist der `2x`-Namensraum erschöpft.** ⚠️ Die Zeilen tragen K-Nummern aus dem Namensraum von Abschnitt 4 („Laufend, klein"), stehen aber auf Vorgabe des Auftrags `MAC_TB-62` hier als Block — die Kollisionsprobe zählt über die ganze Datei, nicht je Abschnitt.*

| # | Punkt |
|---|---|
| **K3k** | ⭐⭐ **WIE EINE MAC-SITZUNG GESTARTET WIRD — vier Regeln, aus einem gemessenen Hänger.** Am 19.09.2026, 23:11, hat `claude --remote-control "<Anweisungstext>"` die Sitzung gestartet und **den Text nicht übergeben**; Eingabezeile leer, `/remote-control` aktiv. ⚠️ **Die Ursache ist NICHT gemessen** (Anführungszeichen zerlegt · Text abgeschnitten · Flag übergibt keinen ersten Zug) und wird nicht behauptet — die Abhilfe braucht sie nicht. **Die vier Regeln:** (1) **Der Anweisungstext reist nie im Startbefehl mit** — nackt starten, Text als eigener Block in die wartende Zeile. (2) **Fester Zeiger `docs/auftraege/AKTUELLER_AUFTRAG.md`**, damit der einzufügende Satz jedes Mal identisch ist, **mit Empfangszeile** am Ende. (3) **Commit und Start nie über zwei Nachrichten trennen** — jeder Auftrag trägt einen Schritt 0, der den Arbeitsbaum committet, und der Nachweis „sauber" wird danach geprüft. (4) ⭐ **Nach jedem Start messen, ob der Text angekommen ist.** Eingetragen in `ARBEITSWEISE.md` **Abschnitt 14 (neu)** mit Berichtigung von Abschnitt 1, und in die Erinnerung |
| **K3l** | ⚠️ **PRÄZISIERUNG ZU K3k (4), am selben Abend nötig geworden — die Messung beweist den EMPFANG, nicht den FORTSCHRITT.** Nach dem Schritt-0-Commit stand `HEAD` dreieinhalb Minuten still, während die Sitzung 1 544 Zeilen Nachträge und ein 951-Zeilen-Backlog las. **Die Unterscheidung:** nichts bewegt sich **und** Schritt 0 hat nicht committet ⇒ Text nicht angekommen; nichts bewegt sich, **aber** Schritt 0 hat committet ⇒ **sie liest, kein Befund**. ⭐ *Wer das nicht trennt, unterbricht eine arbeitende Sitzung — dieselbe Fehlerklasse wie Block 7, Punkt 2, wo aus einem UTC-Zeitstempel geschlossen wurde, eine Sitzung sei tot.* **Für eine lesende Sitzung ist der Fortschritt in Web und App sichtbar, nicht im Repo** |
| **K3m** | ⚠️ **WIDERSPRUCH IN `ARBEITSWEISE.md` AUFGEDECKT, berichtigt:** Abschnitt 1 verlangte *„IMMER als fertiger Einzeiler mit Dateipfad"* und *„ein Befehl, eine Zeile, ein Einfügen"* (ergänzt 15.09.2026) — **genau dieser Einzeiler hat den Hänger erzeugt**. Die Begründung von damals (zwei Schritte heissen zweimal kopieren) stimmt; die Folgerung trägt nicht mehr. ⭐ **Der Grundsatz „Pfad immer mitgeben, nie beschreiben" bleibt** — er gilt jetzt für den Text, nicht für die Befehlszeile |
| **K3n** | ⭐ **DIE TB-NUMMER STEHT IM SITZUNGSTITEL.** Anweisung 19.09.2026: *„Zukünftig sollen auch TB-Angaben im Titel der Claude-Sitzung stehen, damit ich diese in der Historie auseinanderhalten kann."* ⚠️⚠️ **Deckt eine Lücke auf, die `ARBEITSWEISE.md` seit dem 15.09. hatte:** Der Sitzungstitel war Pflicht — **aber nur im Kopf des Aufgabendokuments** (Abschnitt 3). Bei einer nackt gestarteten Mac-Sitzung erreicht er die Sitzungsliste nicht, und der am 19.09. eingeführte **immer identische** Einfügesatz (K3k, Regel 2) hätte **jeder Sitzung denselben Eintrag gegeben** — die Lücke wäre grösser geworden statt kleiner. **Behoben:** Die TB-Nummer steht als Präfix am Anfang des Einfügesatzes. ⭐⭐ **Und der angehängte Satz macht aus dem Titel eine Wache** — nennt `AKTUELLER_AUFTRAG.md` eine andere Nummer als die vorangestellte, bricht die Sitzung ab, statt den falschen Auftrag abzuarbeiten. *Der häufigste Fehler bei einem Zeiger ist ein Zeiger, den jemand zu aktualisieren vergisst.* ⚠️ **Nicht gemessen:** ob Claude Code den Historieneintrag wirklich aus der ersten Nachricht bildet — **kostet beim nächsten Start einen Blick** |
| **K3o** | ⭐⭐ **WAS MIT „ZUKÜNFTIG" GESAGT WIRD, WIRD EINGETRAGEN — ohne weitere Aufforderung.** Anweisung 19.09.2026: *„Füge zukünftig auch immer alle Angaben, die ich mit zukünftig erwähne, in die entsprechenden Dokumentationen nach."* ⇒ **Eine mit „zukünftig" eingeleitete Angabe ist eine stehende Anforderung, keine Bemerkung**, und wird **in derselben Antwort** in die zuständigen Träger eingetragen: Erinnerung immer · `ARBEITSWEISE.md`, `DOKUMENTATIONSSTANDARD.md` oder `UMZUG.md` je nach Gegenstand · Backlog-Nachtrag immer, mit gemessener Nummer · Projektablage nachziehen. ⚠️ **Läuft eine Mac-Sitzung, geht der Text ins Zwischenlager `logs/auftraege/` mit Bringschuld im Kopf** — kein Aufschub, sondern der Weg. Eingetragen als `ARBEITSWEISE.md` **Abschnitt 15 (neu)**. ⭐ *Warum nötig: Die Anweisungen dieses Tages sind mehrfach erst auf Nachfrage in die Dokumente gelangt — und der Chatverlauf ist nach `UMZUG.md` Abschnitt 2 ausdrücklich kein Träger* |
| **K3p** | ⭐⭐ **DER LESEPFAD HAT KEINE REGEL, DER AUFBEWAHRUNGSPFAD SCHON — und deshalb erbt er dessen Wachstum.** Gemessen 20.09.2026: Die sechs Dokumente des Eröffnungstextes umfassen **462 594 Bytes**, davon `BACKLOG.md` allein **350 403 Bytes = 75,7 %**. Darin entscheiden **131 240 Bytes = 37,5 %** nichts mehr: Abschnitte `2b`–`2r` (110 052 B, Rückblicke auf TB-34 bis TB-55), neun ERLEDIGT-Zeilen in Abschnitt 2 (14 120 B), Abschnitt 9 (5 946 B, ⚠️ **inhaltlich Doppel zu `ARBEITSWEISE.md` — der gefährlichere Teil, weil zwei Träger auseinanderlaufen**), Abschnitt 6 (1 122 B). ⭐ **Die Regel dagegen steht seit jeher in Zeile 2 der Datei selbst** (*„Nur aktive Punkte. Alles Abgeschlossene steht im JOURNAL.md"*) **und wurde seit Wochen gebrochen.** ⭐⭐ **Betreiberentscheidung 20.09.2026: Archiv anlegen, mit Verschiebenachweis** — `BACKLOG_ARCHIV.md`, und statt „null entfernte Zeilen" gilt für diese eine Operation *„jede entfernte Zeile erscheint zeichengleich im Archiv"*, per `diff` nachgewiesen. **Das ist der strengere Nachweis, weil er beide Seiten prüft statt einer.** Formuliert als `logs/auftraege/MAC_TB-60_backlog_archiv.md`. ⛔ **Abschnitt 8 (Gestrichen) und `PRUEFPRINZIPIEN.md` bleiben** — 1 990 Bytes, die Wochen sparen |
| **K3q** | ⚠️ **OFFEN, und bewusst so:** Die gewählte Variante räumt die heutigen 37,5 % ab, **hält das künftige Wachstum aber nicht auf.** Die Variante mit stehender Regel (*„jeder Nachtrag nennt nicht nur, was er hinzufügt, sondern auch, was er ablöst"*, in `DOKUMENTATIONSSTANDARD.md`) wurde am 20.09.2026 **nicht** gewählt. ⇒ **Das Archiv ist in einigen Wochen erneut fällig.** Hier festgehalten, damit es beim nächsten Mal keine Überraschung ist, sondern ein Termin |
| **K3r** | ⚠️ **EIGENER BEFUND ZUR EIGENEN ARBEIT:** Sämtliche Dokumentationsänderungen dieser Sitzung trugen `numstat X / 0`, und diese Null wurde jedes Mal **als Qualitätsnachweis vorgezeigt**. Sie ist einer — für die Beweiskraft. ⚠️ **Sie ist zugleich die Ursache des Wachstums, und das wurde kein einziges Mal benannt, bis der Betreiber danach fragte.** ⭐ **Die Lehre: Ein Nachweis, der nur eine Richtung prüft, wird zum Anreiz in diese Richtung.** *Dieselbe Familie wie A4 — ein dauerhaft grüner Nachweis, der nichts kosten kann, hört auf, eine Wache zu sein* |
| **K3s** | ⭐⭐ **DOKUMENTATION WIRD AKTUELL GEHALTEN, NICHT ANGEHÄUFT.** Anweisung des Betreibers 20.09.2026. **Jede Änderung sagt, was sie ablöst; das Abgelöste wird entfernt statt danebengestellt.** ⚠️ **Vier Träger ausgenommen, weil dort die Aufzeichnung das Produkt ist:** Register, `JOURNAL.md`, Backlog-Abschnitt 8, `PRUEFPRINZIPIEN.md` — *ein Register, aus dem etwas entfernt werden kann, beweist nichts mehr.* ⭐ **Faustregel sonst: die Regel behalten, den Fall streichen**, ein Satz Fall innerhalb der Regel genügt. ⚠️ **Gelöscht wird nur mit Nachweis.** Eingetragen als `DOKUMENTATIONSSTANDARD.md` Regel 9 und `ARBEITSWEISE.md` Abschnitt 16. ⭐ **Messbarer Anlass:** Zwischen der Frage des Betreibers um 09:50 und 10:36 ist die Pflichtlektüre um **+7 243 Bytes** gewachsen, während über ihre Verkleinerung geredet wurde |
| **K3t** | ⚠️⚠️ **ANMELDUNG IST REGEL 0 JEDER MAC-SITZUNG.** Gemessen 20.09.2026, 10:44: Der Start meldete *„`/remote-control` requires a claude.ai subscription. Run `/login`"*, Fusszeile **„Not logged in"**, Kopfzeile **„API Usage Billing"** statt „Claude Max" — **BERICHTIGT 20.09.2026: Die Anmeldung war nicht abgelaufen — der macOS-Schlüsselbund war gesperrt** (`security unlock-keychain`), vom Betreiber bestätigt. *Die zuvor hier stehende Ursachenvermutung war unbelegt.* ⚠️ **Zwei Folgen:** ohne sie fehlt `/remote-control` (Sitzung in App und Web unsichtbar), **und der Lauf wird direkt abgerechnet statt über das Abo**. ⭐ **Erster Befehl ist `/login`, nicht der Auftrag**; Kontrolle an der Kopfzeile „Claude Max". Eingetragen als `ARBEITSWEISE.md` Abschnitt 14 **Regel 0** und im Zeiger `AKTUELLER_AUFTRAG.md` |
| **K3u** | ⭐ **JEDE AUFGABE BEGINNT MIT EINEM SATZ IN EINFACHER SPRACHE.** Anweisung 20.09.2026: ein bis zwei Sätze, was jetzt gemacht wird, ohne auszuholen. ⚠️ **Nicht zu verwechseln mit Abschnitt 4** — das ist der Abschluss und gilt nur bei fremden Rückmeldungen; dies ist der Einstieg und gilt immer. Eingetragen als `ARBEITSWEISE.md` **Abschnitt 17** |
| **K3v** | ⛔ **`screen`/`tmux` und Mosh gegen Verbindungsabbrüche: VERWORFEN 20.09.2026, Betreiberentscheidung** — zu komplex bzw. zwei Installationen auf dem Betriebsrechner (Homebrew fehlt, `ARBEITSWEISE.md` 7b). **Nicht erneut vorschlagen.** ⚠️ **Eine Einstellung, die Abbrüche verhindert, gibt es nicht:** Keepalive wirkt nur gegen Leerlauf; beim Wechsel WLAN → Mobilfunk bekommt das Telefon eine neue IP und die TCP-Verbindung endet. ⭐ **Abhilfe vollständig auf der Auftragsseite: nach jedem fertigen Teil sofort committen und pushen** — kostet den Betreiber nichts. *Gemessen: TB-59 verlor so elf Stunden, TB-60 vierzig Minuten Arbeit* |
| **K3w** | ⭐⭐ **EINE NEUE REGEL GILT AUCH FÜR SCHON GESCHRIEBENE, NOCH NICHT GESTARTETE AUFTRÄGE.** `ARBEITSWEISE.md` Abschnitt 14, Regel 3 („sichern nach jedem fertigen Teil") entstand am 20.09. um 10:50; der TB-60-Auftrag war da fertig und wurde **nicht nachgezogen** — derselbe Verlust trat zum zweiten Mal ein. **Beim Formulieren einer Regel wird geprüft, welche offenen Aufträge sie betrifft** |
| **K3x** | ⭐ **Ein langer `&&`-Block verschluckt seine eigenen Prüfungen.** **Gemessen am 20.09.2026: verkettet zweimal nicht durchgelaufen, allein eingefügt zweimal sofort erfolgreich.** ⚠️ **Die Ursache ist NICHT gemessen** — eine Passphrase-Abfrage war es nicht, es erschien keine. ⇒ **Der Push kommt nie in einen `&&`-Block, sondern immer in eine eigene Zeile.** ⭐ **Und die Lehre darüber hinaus: Wenn die Abhilfe ohne Ursache auskommt, gehört keine Ursache in den Text.** *Am 20.09. wurde zweimal geschrieben, die Abhilfe brauche die Diagnose nicht — und beide Male trotzdem eine Diagnose geliefert, die sich als falsch erwies* |
| **K3y** | ⭐⭐ **EIN PLATZHALTER ERFÄHRT NICHT, DASS SEINE BEDINGUNG EINGETRETEN IST.** Gemessen 20.09.2026 an `79742d1`: `research/vorregistrierung/faltenplan.py:216` setzt in `plan_krypto()` hart `"status": "platzhalter"` mit dem Docstring *„keine Jahreszahlen bis TB-31 gemeldet hat"*; `benchmark.py:176` überspringt den Bot daraufhin mit `continue`. **TB-31 ist seit PR #105 erledigt, TB-34 hat den Kursbestand neu aufgebaut, und die Krypto-Falten stehen seit TB-56b in Registerabschnitt 21** — der Platzhalter stand trotzdem noch, und drei Dokumente schrieben *„das hängt an TB-31"* voneinander ab. ⭐ **Die Lehre: Wer einen Platzhalter setzt, nennt die Bedingung UND den Ort, an dem ihr Eintreten sichtbar wird.** *Sonst wartet der Code auf ein Ereignis, das längst stattgefunden hat, und niemand prüft es nach, weil die Begründung plausibel klingt.* ⚠️ **Fehlerklasse: ein Name statt einer Messung** (Block 7, Punkt 3) — hier ein **Aufgabenname**, der als Zustandsangabe gelesen wurde |
| **K3z** | ⚠️⚠️ **`endgueltig` IST GEFÄHRLICHER ALS `platzhalter`.** Bei derselben Messung gefunden, und es war **nicht** gesucht: In `benchmark_drawdowns.json` stehen die vier Aktien-Bots als `status: endgueltig` mit Falten **ab 2019** — nach Registerabschnitt 21 beginnen sie **2017** bzw. **2018**. Die Datei trägt noch die Falten der mit TB-56 entfernten Schranke. ⭐ **Gesucht wurde die leere `dd_toleranz` der fünf Krypto-Bots; die vier überholten Aktienzeilen fielen nur auf, weil die Gegenprobe ALLE NEUN ausgab statt nur der fünf.** ⭐⭐ **Die Lehre: Ein Zustand, der sich selbst als fertig bezeichnet, wird nicht nachgeprüft — ein Platzhalter schon.** ⇒ **Eine Gegenprobe gibt alle Zeilen aus, nicht nur die verdächtigen.** *Dieselbe Familie wie A1: ein leeres Ergebnis und ein blinder Sucher sehen gleich aus — hier: ein richtiges Feld und ein veraltetes sehen gleich aus, solange man nur die leeren ansieht* |
| **K4a** | ⚠️⚠️ **BERICHTIGUNG EINER ZAHL AUS COMMIT `79742d1` — die Kollisionsprobe von TB-60 war zu eng.** Dort steht *„24 Blockbezeichner und 38 K-Nummern, keine doppelt"*. **Nachgemessen am 20.09.2026: `K1o` und `K1q` stehen je ZWEIMAL** in `BACKLOG.md` (Zeilen 1331/1335 und 1333/1336). ⭐ **In der Sache harmlos:** es sind Fortschreibungen desselben Punktes von TB-50 zu TB-51, die zweite Zeile trägt *„(unverändert)"*. ⚠️ **In der Form nicht:** die ältere Zeile ist abgelöst und steht daneben statt entfernt — **genau das, was `DOKUMENTATIONSSTANDARD.md` Regel 9 seit dem 20.09. untersagt**, und der Grund, warum die Probe stolperte. ⇒ *Beim nächsten Durchgang zusammenführen: eine Zeile je Nummer, mit dem Fortschreibungsvermerk darin.* ⭐⭐ **Die eigentliche Lehre, und es ist der VIERTE Fall an zwei Tagen:** Die Probe hat `sort -u` über beide Dateien gelegt — **`-u` entfernt genau die Duplikate, die sie finden sollte.** *Nach `K2[a-z]` ohne `K3`, der geschätzten Zeilenzahl 70 statt 67 und dem `---`-Filter, der 546 statt 561 zählte, ist dies der vierte Fall eines Messmusters, das seinen eigenen Suchraum beschneidet.* ⇒ ⭐ **Eine Kollisionsprobe darf kein `-u` enthalten; sie zählt, statt zu vereinheitlichen.** ⚠️⚠️ **BERICHTIGUNG AN DIESEM PUNKT SELBST, 20.09.2026, 12:30 — die Zahlen, die eine Stunde zuvor in Commit `28eea5c` standen, waren ebenfalls falsch.** Dort hiess es „43 Tabellenzeilen, 41 verschiedene Nummern“. **Gemessen: 64 Zeilen, 62 verschiedene Nummern.** ⭐ **Die Ursache ist der FÜNFTE Fall derselben Familie an einem Tag:** das Muster verlangte `| **K2p** |` **mit schliessendem Balken** — im Backlog steht aber `| **K2p** *(im Nachtrag (n) als `K2r` vorgeschlagen …)* |`, und **jede Zeile mit Vergabevermerk fiel heraus**. Richtig ist `^\| \*\*(K\d[a-z])\*\*` **ohne Abschluss**. ⚠️ *Die Doppelbelegung `K1o`/`K1q` bleibt bestehen; sie war richtig gefunden.* ⭐⭐ **Die Lehre über der Lehre: Ein Messmuster, das an einem FORMAT hängt, fällt aus, sobald das Format eine Ausnahme bekommt** — und die Ausnahme war hier ausgerechnet der Vergabevermerk, den TB-59 eingeführt hat, **um diese Nummern nachvollziehbar zu machen**. *Die Sorgfaltsmassnahme hat die Kontrolle blind gemacht.* |
| **K4b** | ⚠️⚠️ **NACHTRAG (m) IST NIE EINGEARBEITET WORDEN — und seine sechs Nummern sind inzwischen anderweitig vergeben.** Gemessen 20.09.2026: `BACKLOG_NACHTRAG_2026-09-19m.md` führt `K2l`–`K2q`; die Zeilen `K2l`–`K2o` im Backlog tragen **Inhalte aus den Nachträgen (s)/(t)**, `K2p`/`K2q` tragen Inhalte aus **(n)**. ⭐ **Vier der sechs Regeln stehen inhaltlich anderswo:** `K2l` Downloads-Ordner → `ARBEITSWEISE.md`, `UMZUG.md`, Protokoll · `K2m` `[ortsunabhängig]`/`[Mac-pflichtig]` → Backlog · `K2p` nicht am Repo arbeiten, solange eine Mac-Sitzung läuft → `UMZUG.md` · `K2q` über die Anbindung nur lesend → `ARBEITSWEISE.md`. ⚠️⚠️ **ZWEI STEHEN NIRGENDS**, mit vier verschiedenen Mustern gesucht: **(1)** „Jede Rückfrage an den Betreiber und seine Antwort kommen wörtlich in den Bericht — sonst leben sie nur im Sitzungsverlauf, der mit der Sitzung verschwindet.“ **(2)** „Die Sitzung committet ihren eigenen Auftrag mit und ihre Belege.“ ⭐⭐ **Regel (1) ist die bitterste: sie ist genau die Vorschrift, die verhindert hätte, dass Betreiberentscheidungen nur im Chat leben — und sie ist selbst im Chat geblieben.** ⇒ **TB-62 arbeitet (m) UND (v) ein**, mit gemessenen Nummern |
| **K4c** *(entschieden)* | ⚠️⚠️ **`ARBEITSWEISE.md` WIDERSPRACH SICH SELBST ZUR ZIP-PFLICHT — vorgelegt und am selben Tag entschieden.** **Abschnitt 1, Zeilen 98–115:** „Immer gebündelt als ZIP — auch bei einer einzigen Datei“, dazu fünf Zeilen zu Benennung und Ablage, zuletzt verschärft am 15.09.2026. **Abschnitt 10, Zeile 699:** das Umzugsverfahren „ersetzt die frühere ZIP-und-Anhang-Übergabe, die durch zwei Anweisungen des Betreibers vom 19.09.2026 überholt ist: ‚Ich lese die Zipp und berichte nie‘“. **Dieselbe Datei, gegenteilige Vorschrift.** ⚠️ **Zwei Lesarten, und der Text entscheidet nicht:** **(a)** ZIP ist überall abgeschafft · **(b)** ZIP ist nur für die Übergabe beim Umzug abgeschafft und gilt für gewöhnliche Abgaben weiter. ⭐⭐ **BETREIBERENTSCHEIDUNG 20.09.2026, 12:40 auf Vorlage: (a) — ZIP wird ÜBERALL abgeschafft**, nicht nur beim Umzug. Ergebnisse kommen als Commit im Repo und als einzelne Dateien im Chat, **nie als Archiv**. ⚠️ **Der Zweck der alten Regel bleibt und wechselt nur das Mittel:** *ein Beleg muss die Sitzung überleben* — dafür sorgte bisher das Archiv, künftig der Commit. ⭐ **Das ist der stärkere Träger:** ein Archiv in `~/Downloads` ist in keiner Version, ein Commit schon. ⇒ **Umbau in `TB-62`, Schritt 4** — gemessen sind über zwanzig Fundstellen in `ARBEITSWEISE.md`, die Zahl wird dort NICHT vorgegeben, sondern von der Sitzung gezählt. ⭐ *Genau der Fall, den `K3p` als den gefährlicheren benannt hat: nicht Wachstum, sondern zwei Träger, die auseinanderlaufen — hier sogar zwei Abschnitte desselben Trägers* |
| **K4d** | ⚠️⚠️ **DIE ERFOLGSZAHL DES TAGES WAR AUF DER FALSCHEN LISTE GERECHNET — sechster Fall, und der teuerste, weil der Betreiber sie als Ergebnis verbucht hat.** Gemeldet wurden am 20.09.2026 nacheinander *462 594 → 469 837 → 350 847 Bytes*, also **−111 747**, jeweils als „Pflichtlektüre, sechs Dokumente“. ⚠️ **Gemessen: Der Eröffnungstext in `UMZUG.md` Abschnitt 6 nennt VIER Dokumente**, nicht sechs — `UEBERGABE_<datum>.md`, `ARBEITSWEISE.md`, `PRUEFPRINZIPIEN.md`, `BACKLOG.md`. **`UEBERGABEPROTOKOLL.md` (141 234 B) und `DOKUMENTATIONSSTANDARD.md` standen nie im Lesepfad** und waren trotzdem in der Summe. ⭐ **Der richtige Verlauf, je Commit nachgerechnet:** `aa05cc1` 19.09. 23:14 **348 090** · `0bb4c92` 20.09. 10:43 **443 587** (Höchststand) · `c04b348` 11:37 **318 005** (Tiefstand, nach dem Archiv) · `198fc32` 12:27 **324 330**. ⇒ **Vom Höchststand −119 257 (−26,9 %), vom Sitzungsbeginn aber nur −23 760 (−6,8 %)** — weil `ARBEITSWEISE.md` am selben Tag um **+12 571 Bytes** gewachsen ist, den Abschnitten 13 bis 18. ⭐⭐ **Und der Satz, der bleibt: seit dem Tiefstand um 11:37 ist die Pflichtlektüre in 50 Minuten wieder um 6 325 Bytes gewachsen** — genau das, was `K3q` vorhergesagt hat, als es festhielt, die gewählte Variante räume die Vergangenheit ab und halte das künftige Wachstum nicht auf. ⚠️ **Fehlerklasse: nicht ein zu enges Muster wie `K4a`, sondern eine Bezugsmenge, die nie am Quelltext geprüft wurde.** *Die Zahl war sechsmal richtig gerechnet — über die falschen Dateien.* ⇒ ⭐ **Eine Kennzahl nennt die Menge, über die sie läuft, und die Menge wird an ihrer Quelle nachgelesen, nicht erinnert** |
| **K4e** | ⚠️⚠️ **DIE PROJEKTABLAGE IST EIN TRÄGER OHNE NACHZIEHVERFAHREN — und sie war es heute drei Stunden lang.** `UMZUG.md` Abschnitt 2 führt drei Träger: Erinnerung, **Projektablage**, Repo. **Gemessen am 20.09.2026, 12:34:** Die Ablage trug `BACKLOG.md` im Stand von **09:43 UTC** — also **vor** den TB-61-Berichtigungen aus `28eea5c` (10:15 UTC). Wer eine neue Sitzung nach dem Eröffnungstext gestartet hätte, hätte gelesen: „das hängt an TB-31“ — **genau den Satz, den dieselbe Stunde als überholt nachgewiesen hat.** ⭐ **Die Ursache ist kein Versäumnis, sondern eine Lücke:** Das Repo wird per Commit nachgezogen, die Erinnerung beim Schreiben — **für die Ablage gibt es keinen Schritt, der sie auslöst.** Sie wurde bisher von Hand aktualisiert, wenn jemand daran dachte. ⇒ ⭐⭐ **Regel: Wer ein Führungsdokument committet, lädt es im selben Zug in die Projektablage** — der Commit ist der Auslöser, nicht die Erinnerung. ⚠️ **Nachgezogen am 20.09.2026, 12:34: alle sechs Dokumente** (`BACKLOG`, `ARBEITSWEISE`, `PRUEFPRINZIPIEN`, `UEBERGABE_2026-09-19`, `UMZUG`, `DOKUMENTATIONSSTANDARD`), Gegenprobe über die Suche: die Ablage führt jetzt den berichtigten Text. ⭐ *Dieselbe Familie wie `K3p`: nicht Wachstum, sondern zwei Träger, die auseinanderlaufen — und diesmal war der abweichende Träger genau der, den eine neue Sitzung zuerst liest.* |
| **K4f** | ⚠️⚠️ **DIE ERSETZTE VIER-JAHRES-REGEL STEHT AN ZWEI WEITEREN STELLEN — von TB-65 am Rande gemeldet, hier nachgemessen und bestätigt (20.09.2026, 15:10).** **(1)** `docs/VORREGISTRIERUNG_S-E1_nulltest.md:57–59`: „point-in-time (ein Titel geht in einen Monat nur ein, wenn seine Kursdaten mindestens vier Jahre vor Monatsbeginn einsetzen — **dieselbe Regel wie im Hauptregister**)“. ⚠️ **Der Verweis zeigt auf eine Regel, die im Hauptregister ERSETZT ist** (Abschnitt 5.3, Sperrliste Punkt 8). ⭐⭐ **Nicht umschreiben:** `S-E1` ist ein **abgeschlossener, durchgefallener Lauf** (15.09.2026, TB-33, PR #106) mit eigener Vorregistrierung; seine Regel galt für ihn und bleibt. ⇒ **Was fehlt, ist ein Vermerk**, dass der Halbsatz „dieselbe Regel wie im Hauptregister“ seit dem 16.09. nicht mehr zutrifft — *sonst liest ihn jemand als Beleg dafür, dass die Regel noch gilt.* **(2)** `research/krypto_historie/faltenplan.py:65` führt `MINDESTTRAINING_JAHRE = 4` — **eine dritte Kopie, die `T56b.6` nicht nennt.** T56b.6 führt aus derselben Datei nur Zeile 64 (`FRUEHESTE_FALTE = 2019`). ⇒ **T56b.6 um Zeile 65 ergänzen**, wenn die Aufgabe geschrieben wird. ⭐ *Fehlerklasse wie `K4a`: ein Messmuster (hier: die Suche nach `FRUEHESTE_FALTE`) sah die zweite Konstante in derselben Datei nicht, weil niemand nach ihr gesucht hat.* ⚠️ **Beide Stellen sind BERICHTET, nicht geändert** — TB-65 war rein lesend, und diese Sitzung schreibt keinen Code |
| **K4g** | ⭐ **NACHTRAG (m) NACHTRÄGLICH GEPRÜFT UND ABGESCHLOSSEN (20.09.2026, TB-62)** — Folge von `K4b`. Seine sechs Nummern `K2l`–`K2q` waren an (s)/(t)/(n) vergeben und bleiben dort; **keine der sechs Regeln wird hier noch einmal eingetragen.** Gemessen, wo die vier stehen, die schon anderswo geführt sind: `K2l` (Aufträge nie nach `~/Downloads`; Zwischenlager `logs/auftraege/`, endgültiger Ort das Repo) → `UEBERGABE_2026-09-19.md` Block 7 Punkt 9 und Block 8 Punkt 9, `ARBEITSWEISE.md` Abschnitt 14 Regel 2 (`docs/auftraege/`) · `K2m` (`[ortsunabhängig]`/`[Mac-pflichtig]`) → `UEBERGABE_2026-09-19.md` Block 8 Punkt 7 — ⚠️ **nur dort, nicht in `ARBEITSWEISE.md` und nicht als Regel in dieser Datei** · `K2p` (nicht am Repo arbeiten, solange eine Mac-Sitzung läuft) → `ARBEITSWEISE.md` Abschnitt 15 („`docs/` gesperrt"), `UEBERGABE_2026-09-19.md` Block 7 Punkt 10, `UMZUG.md` Abschnitt 3 · `K2q` (über die Geräteanbindung nie überschreiben, kein `git status`/`git log`) → `UEBERGABE_2026-09-19.md` Block 7 Punkte 7 und 8 sowie Abschnitt „Die Geräteanbindung", `ARBEITSWEISE.md` Abschnitt 14 Regel 4 (dort nur `git status`). *Der Auftrag TB-62 nannte als Fundorte `UMZUG.md` und das Protokoll; gemessen tragen beide nur Umzugs-Kontext bzw. eine Beschreibung, die Regeln selbst stehen in der Übergabe vom 19.09.* **Die zwei, die nirgends standen, sind nachgetragen:** `K2n` (Rückfrage an den Betreiber und Antwort wörtlich in den Bericht) → `ARBEITSWEISE.md` Abschnitt 15, Unterabschnitt am Ende; `K2o` (die Sitzung committet ihren Auftrag und ihre Belege mit) → `ARBEITSWEISE.md` Abschnitt 14, Regel 3. ⚠️ **Was (m) darüber hinaus enthält und der Auftrag nicht nennt:** einen Rückblick-Block „2s" mit 20 Zeilen (`T53.1`–`T53.4`, `T58.1`–`T58.6`, `T58b.1`–`T58b.3`, `B1`–`B7`) zu TB-53b, TB-58 und TB-58b, eine Berichtigung zu Rang 0,85 (überholt — Nachtrag (e) hat 0,85 schon ersetzt, `0,85b` trägt den T53.1-Befund) und drei Kettenzeilen-Vorschläge (Lese-Audit → steht als `0,85c` · TB-56 → erledigt · ⚠️ **„Laufreproduktion gegen den Lock — frischer Klon, `TB_SELEKTIONSCOMMIT` gesetzt, derselbe Lock; nicht in der Cloud möglich (B2)" steht nirgends und bleibt offen**). Der Rückblick-Block ist **nicht** eingearbeitet: TB-53b, TB-58 und TB-58b haben weder einen Journal-Block noch einen Archiv-Eintrag (gemessen: `T53.1`, `T58.1`, `T58b.3`, `index.lock` je 0 Treffer in `BACKLOG.md`, `BACKLOG_ARCHIV.md`, `JOURNAL.md`), und nach Zeile 2 dieser Datei und TB-60 gehört ein Rückblick nicht in den aktiven Teil — **der Ort (Journal-Nachtrag oder `BACKLOG_ARCHIV.md`) ist eine offene Betreiberentscheidung** |

---

## 3 — Die Kette (Ränge 1 bis 5)

| Rang | Schritt | Stand |
|---:|---|---|
| ~~0~~ | ~~TB-30a Vorregistrierung~~ | **ERLEDIGT, PR #103** — Journal **AI**. Offen: GPG-Tag + Zeitanker durch den Betreiber |
| ~~0,5~~ | ~~Krypto-Historie (V2)~~ | **ERLEDIGT** — TB-34 Cloud und Mac-Lauf, Datenstand `d9449faf…`/223 |
| ~~0,6~~ | ~~T46.1 — die Ausstiegspfade prüfen~~ | ⭐ **ERLEDIGT 18.09. durch TB-46b (`c5ad722`). KEIN Bot schliesst eine Position bei fehlenden Kursdaten** — strukturell unmöglich, nicht nur unbeobachtet. Siehe Block **2e** |
| ~~0,7~~ | ~~TB-46 Erhebung + Snapshot-Werkzeug~~ | **ERLEDIGT, gemergt `135c306`** |
| ~~0,8~~ | ~~TB-47 Snapshotgrenze~~ | **TEILWEISE ERLEDIGT, gemergt `a1e7fb4`** — Snapshot-Grenze, zwei Hashes, Teilkerzen-Prüfung, Prozessgruppe. ⚠️ **Der eigentliche Umbau der 90 Module steht noch aus** und ist jetzt Rang **0,85**. Siehe Block **2f** |
| ~~0,9~~ | ~~Registernachtrag~~ | **ERLEDIGT durch TB-48, gemergt `db8913a`** — Abschnitt 17, `506 0`. Siehe Block **2g** |
| ~~0,82~~ | ~~TB-49 — die Ausnahme ins Werkzeug~~ | ⭐ **ERLEDIGT 18.09.** — Cloud, Mac-Lauf (15:05–15:57, Python 3.9.6) und Merge `2f241d1`. **Beide Rechner liefern dieselben Zahlen.** Siehe Block **2h** |
| **0,84** | **Snapshot ziehen** | ⭐ **Technisch möglich seit TB-49** (`2f241d1`), auf beiden Rechnern nachgewiesen. ⚠️⚠️ **BETREIBERENTSCHEIDUNG 18.09.2026: er wird NICHT jetzt gezogen, sondern am Tag des signierten Tags** — Registertext 5 / **F1a**: *„Snapshot am Tag des signierten Tags ziehen; ein zweiter Snapshot ist ein neuer Lauf."* **Ein früherer Snapshot wäre entweder veraltet, wenn der Tag kommt, oder der Tag friert einen Zustand ein, den das Register nicht beschreibt** |
| **0,84** *(alter Wortlaut — ersetzt 19.09.2026 durch Nachtrag (d) vom 18.09.2026)* | **Snapshot ziehen** | ⭐ **nach dem Merge nicht mehr blockiert.** ⚠️ **Eigene Entscheidung mit eigener Freigabe** — TB-49 hat ihn ausdrücklich nicht gezogen |
| ~~0,85a~~ | ~~Resolver-Modus in `shared/paths.py` + zwei AST-Masse~~ | ⭐ **ERLEDIGT 18.09.** — Cloud, Mac-Lauf (22:29–23:03, Python 3.9.6) und Merge `7e48e1f`. **99 Pfade, 0 Unterschiede, auf beiden Rechnern.** Siehe Block **2k** |
| ~~0,85a~~ *(alter Wortlaut — ersetzt 19.09.2026 durch Nachtrag (f) vom 18.09.2026)* | ~~Resolver-Modus in `shared/paths.py` + zwei AST-Masse~~ | ⭐ **TB-52, Cloud fertig.** ⚠️ **Mac-Lauf und Merge offen.** Siehe Block **2k** |
| **0,85b** | ⭐ **TB-53 — die Selektionsseite auf den Resolver.** ⚠️ **NEU ZUZUSCHNEIDEN:** TB-52 hat gemessen, dass **keines der 90 Module `paths.py` importiert** und **71 von 90 ihre Pfade aus `shared/strategy_paths.py`** beziehen, das `DATA_DIR` selbst ableitet. **Erste Frage: bedient `strategy_paths.py` auch den Live-Pfad?** Wenn ja, braucht die Änderung dieselbe Zusicherung wie TB-52 | zu formulieren |
| **0,85c** | **TB-54 — Lese-Audit** als Gültigkeitsbedingung (Registertext 5e) · **Cache nach Snapshot-Hash UND Commit** (T46.7) | danach |
| **0,85c** *(Vermerk 19.09.2026, Nachtrag (l))* | ⚠️ *„Die Aufgabennummer TB-54 wurde am 19.09.2026 für die Einarbeitung der Backlog-Nachträge verbraucht. Das hier gemeinte Vorhaben (Lese-Audit) bekommt bei seiner Formulierung eine neue Nummer."* | — |
| **0,85** *(alter Wortlaut — ersetzt 19.09.2026 durch Nachtrag (e) vom 18.09.2026)* | ⭐ **Der grosse Umbau:** 90 Module der Selektionsseite auf den Snapshot · **Resolver-Modus in `shared/paths.py` als eigener kleiner Schritt mit Mac-Lauf** · **zwei AST-Tests** (kein eigener Datenpfad · **keine Wanduhr**) · **Lese-Audit** · Cache nach **Snapshot-Hash UND Commit** | zu formulieren nach dem Snapshot |
| **0,87** | ⚠️ **In einem Zug, braucht die Freigabe für `shared/entscheidungskerze.py`:** Gleichheitsprüfung aller Quellen · Datencron mit Prüfung vor den Bot-Läufen (**`TZ=UTC`**) · **Kein-Entscheid-Datensatz** in `melde()` · Datenstand-Hash und Kerzenwerte je Lauf ins Protokoll | Block **2e**, Betreiberfreigabe offen |
| **0,86** | ⭐⭐ **TB-55 — den Snapshot ziehen: ERLEDIGT 19.09.2026.** `63e4b6c8…cb2ceb2`, 225 Dateien, Commit `1075dec` auf `main`. Nachprüfung `UNVERAENDERT` | ✅ **abgeschlossen** |
| **0,86a** | ⭐⭐ **TB-55b — der Registereintrag: ERLEDIGT 19.09.2026.** Abschnitt 18, Commit `0fe61d7`, 62 Zeilen hinzu / 0 entfernt | ✅ **abgeschlossen** |
| **0,86b** | ⭐ **TB-54 — die acht Backlog-Nachträge (d)–(k) einarbeiten** · **TB-54b — Journal (c)–(e) und Prüfprinzip A7** | ⚠️ **als nächstes, vor TB-53** |
| **0,86c** *(Nummer am 19.09.2026 in TB-54b gemessen und vergeben — Nachtrag (l) nannte bewusst keine)* | ⭐ **Die Kette sortieren** (T54.7): aktive Zeilen numerisch, ersetzte Zeilen vollständig erhalten unter einer eigenen Überschrift „Ersetzte Kettenzeilen" am Abschnittsende. ⚠️ **Maschinell zu prüfen: jede entfernte Zeile taucht unten wörtlich wieder auf.** ⚠️ **Setzt eine Betreiberentscheidung voraus** | offen |
| **0,86a** *(alter Wortlaut — ersetzt 19.09.2026 durch Nachtrag (k) vom 19.09.2026)* | ⭐⭐ **TB-55b — der Registereintrag zum Snapshot** (Tatsachennotiz, keine Änderung eines Registertexts) | ⚠️ **als nächstes** |
| **0,86** *(alter Wortlaut — ersetzt 19.09.2026 durch Nachtrag (j) vom 19.09.2026)* | ⭐⭐ **TB-55 — den Snapshot ziehen** · Cloud-Lauf 19.09.: ⚠️ **NICHT gezogen** (falscher Rechner), jeder inhaltliche Sollwert getroffen, Name `63e4b6c8…` vorhergesagt · ⭐ **Auftrag v2 mit Schritt −1 Ortsprüfung liegt bereit, unverbraucht** | ⚠️ **auf dem Mac auszuführen** |
| **0,88** *(im Nachtrag (h) als 0,87 vergeben; 0,87 war bereits belegt — Betreiberentscheidung 19.09.2026: 0,88)* | ⭐ **TB-56 — die Faltenschranke messen und entfernen** (F14/F16) · **Berichtigung von 17.3 im Register** (F17, Kategorie Berichtigung) · **die Drei-Kategorien-Regel zu Registertext 0** | zu formulieren |
| **0,86** *(alter Wortlaut — ersetzt 19.09.2026 durch Nachtrag (h) vom 19.09.2026)* | ⭐ **TB-55 — die Faltenschranke messen und entfernen** (F14/F16) · **Berichtigung von 17.3 im Register** (F17, Kategorie Berichtigung) · **die Drei-Kategorien-Regel zu Registertext 0** | zu formulieren |
| **0,95** | **`auswertung.py` auf Verfahren B** | zu formulieren |
| **1** | **TB-30b Mass-Reparatur** — 9 + 6 + 3 Stellen auf den Kapital-Drawdown, **Walk-Forward einschliessen** (sechs Bots haben einen eigenen Rechner), Agent 2 mit | zu formulieren |
| **2** | **Neuselektion**, dann DSR **als Bericht** (N = 653) | nach 1 |
| **3** | **Beta-Bereinigung je Bot** — statisches Beta, Timing, Auswahl getrennt. **Diese Zahl entscheidet, welche Bots bleiben** | nach 2 |
| **4** | **`S-B1` Multi-Asset-ETF-Trend** — die **einzige** Quellen- **und** Horizontergänzung im Katalog. Vorbereitung (14 ETFs ab 2007 laden, Rastergrenzen, Register) **kann parallel laufen**; der Backtest erst nach Rang 1 | vorbereiten |
| **5** | **Netting/Deckel** — 72 gleichzeitige Positionen, bis zu vier Bots im selben Titel. Die Kaskade aus TB-26 wirkt nur **innerhalb** eines Bots | nach 3 |
| **0,96** *(Nummer in TB-59 gemessen und vergeben — Nachtrag (n) nannte bewusst keine; höchste Kettenzeile davor 0,95)* | ⭐ **AF-F0 — Bestandsaufnahme der Codebasis** gegen Abschnitt 13 der Vorlage. **Rein lesend, ortsunabhängig, ohne Sitzung.** ⚠️ Vor jeder Feature-Struktur | offen |
| **0,97** *(Nummer in TB-59 gemessen und vergeben — Nachtrag (p) nannte bewusst keine; höchste Kettenzeile davor 0,95)* | ⭐ **Backlog-Sichtung in fünf Durchgängen für (n), (o), (p)** — Kollision, Abhängigkeit, Widerspruch, Ausscheiden, Kette. ⚠️ **Rein lesend, gemessen am Backlog** (QR8) | offen |
| **0,98** *(Nummer in TB-59 gemessen und vergeben — Nachtrag (o) nannte bewusst keine; höchste Kettenzeile davor 0,95)* | ⭐ **MI-F0 / MI-T0.1 — Vintage-Datenlage erheben** (MI3). ⚠️ Rein lesende Recherche, ortsunabhängig. **Entscheidet, ob der KI-Layer überhaupt testbar ist** | offen |
| **0,99** *(Nummer am 20.09.2026 gemessen und vergeben — höchste Kettenzeile davor `0,98`)* | ⭐⭐ **LAUF-REPRODUKTION GEGEN DEN LOCK.** Frischer Klon in isolierter Umgebung, `TB_SELEKTIONSCOMMIT` gesetzt, **derselbe Lock**; gleiche Maschine zulässig. ⚠️ **In der Cloud nicht möglich** (B2). ⚠️⚠️ **Stand bisher NUR in `UEBERGABE_2026-09-19.md` Block 4 Punkt 6 und im nie eingearbeiteten Nachtrag (m)** — im Backlog gab es dafür keine Zeile (gemessen 20.09.2026, TB-62/`K4g`). ⭐ *Dritter Fall desselben Musters an einem Tag: eine Anforderung, die nur in der Übergabe lebt* — nach der ZIP-Regel und `[ortsunabhängig]`/`[Mac-pflichtig]`. ⚠️ **F1b/Q2 ist für die DATEN bewiesen** (SHA-256 ist pandas-unabhängig), **nicht für den LAUF** | **vor dem Tag** |
| **6** *(Nummer in TB-59 gemessen und vergeben — Nachtrag (n) nannte bewusst keine; höchste Kettenzeile davor 0,95; Betreiberentscheidung 19.09.2026: geparkte Epics hinter Rang 5)* | ⚠️ **Epic AF — autonome Forschungspipeline.** ⚠️⚠️ **Geparkt bis nach dem signierten Tag** (AF0) | geparkt |
| **7** *(Nummer in TB-59 gemessen und vergeben — Nachtrag (p) nannte bewusst keine; höchste Kettenzeile davor 0,95; Betreiberentscheidung 19.09.2026: geparkte Epics hinter Rang 5, in der Arbeitsreihenfolge AF → QR → MI)* | ⚠️ **Epic QR — Alpha-Discovery-Labor.** ⚠️⚠️ **Geparkt hinter Epic AF, das hinter dem Tag geparkt ist** (QR0/QR6) | geparkt |
| **8** *(Nummer in TB-59 gemessen und vergeben — Nachtrag (o) nannte bewusst keine; höchste Kettenzeile davor 0,95; Betreiberentscheidung 19.09.2026: geparkte Epics hinter Rang 5)* | ⚠️ **Epic MI — KI-Marktverständnis und adaptive Allokation.** ⚠️⚠️ **Geparkt hinter Epic AF, das hinter dem Tag geparkt ist** (MI0) | geparkt |

---

## 4 — Laufend, klein

| # | Punkt |
|---|---|
| **F2** | ⭐ **Lauf-Protokoll mit Zeitstempel.** Der Live-Record ist der Holdout — und ohne Protokoll ist nicht belegbar, welche Läufe stattfanden. **Ein Holdout mit unbelegten Lücken ist keiner** |
| **F6 / O2** | **`.env` ist nicht versioniert**, und `DASHBOARD_HOST` steht nur dort. Geht sie verloren, ist das Dashboard über Tailscale nicht mehr erreichbar — der einzige Fernzugriffsweg |
| **J6** | **WAL und `busy_timeout`** — **730 Prozessstarts am Tag** auf SQLite ohne WAL, gebündelt auf der Minute. Betrifft die drei bestehenden Nachverfolgungs-DBs. Eigener kleiner PR |
| **F1** | `broker/spiegel.py` protokolliert übersprungene Eröffnungen bei **jedem** Lauf neu |
| **P2** | ⭐ **Positionsgrösse je Trade mitschreiben** *(Nutzerwunsch 15.09.2026)*. Die Trade-Datenbanken halten heute **nur das Prozentergebnis**, nicht das eingesetzte Kapital — deshalb weist das Dashboard ausdrücklich „keine Equity-Kurve und keine Portfolio-Rendite" aus, und **−13,89 % ist eine Summe von Prozentpunkten, keine Bilanz**. ⚠️ **Berührt die neun `forward_test.py`** — nur mit ausdrücklicher Freigabe des Betreibers, eigene Aufgabe. ⚠️ **Der Preis des Wartens, einmal benannt:** Jeder Tag ohne Mitschrift ist ein Tag Live-Record, der später nur noch **geschätzt** werden kann — und der Live-Record ist der Holdout. **Vom Betreiber bewusst in den späteren Verlauf gelegt** |
| **Regel** | ⚠️ **Keine Kennzahlen in Code-Köpfen, nur Verweise.** TB-17 hat mit AST-Nachweis 330,18 % in `live_params.py` geschrieben — **24 Stunden später galt 419,07 %**. Der Prüfer aus Q.7 wird damit zur Wache dagegen, dass sie zurückkommen. *Erledigt vier Punkte auf einmal und verhindert die nächsten vier* |
| **K1a** | ⚠️ **Sechs der neun Bots überspringen ein leeres Symbol weiterhin STILL** (T45.4) — widerspricht *„Ein Lauf, der ein Symbol auslässt, sagt es. Immer."* **Freigabepflichtig, eigene Aufgabe** |
| **K1b** | **`t3_supertrend` ist nur durch die Einrückung sicher** — `compute_indicators` bricht auf leerem Rahmen ab und überlebt nur, weil der Aufruf im `try` der Ladeschleife steht (T45.3, **D4**) |
| **K1c** | **`target_price` kann `None` sein**, `strategies/elliott_wave/forward_test.py:129` (T46b.7) |
| **K1d** | **`broker/test_ibkr.py` benutzt `US/Eastern`** — veralteter Zonenname; `America/New_York` ist der aktuelle (T46.14) |
| **K1e** | **`shared/paths.py:18` legt `data/` beim Import an** (T46.8) — harmlos heute, **still im Fehlerfall** |
| **K1f** | **Das Hash-Verfahren steht doppelt im Repo**, zeichengleich in `pruefe_register.py:319` und `herkunft.py:96` (T46.6) |
| **K1g** | **Alter `stash@{0}` auf dem Mac** aus der Frühzeit des Projekts — vor dem Snapshot ansehen und wegräumen (T45.11) |
| **K1h** | ⚠️ **`reg.KURSDATEN_DIR_VERBOTEN`** — ein Rückfallwert mit einem Namen, der etwas anderes verspricht (T46.5, **D3**) |
| **K1i** | **Zweiter Umstellungstag ins Register**, sobald sein Datum existiert: der erste Tag, an dem **alle neun** Bots ohne Rückfall aus `data/` lesen — **aus den Logs zu belegen**, nicht zu setzen |
| **K1j** | ⚠️ **Buchstaben (a)(b)(c) doppelt belegt** — Register gegen Code, siehe **T49.12** |
| **K1k** | ⚠️ **Irreführende Fehlermeldung** in `test_stabile_sortierung.py` und `test_wellenauswahl.py`, siehe **T49.13** — gehört zu T45.6 |
| **K1l** | **Verwechselbare Ausgabe** in `shared/test_umstellungstag.py`, siehe **T49.14** |
| **K1m** | ⚠️ **`ERSTE_MOEGLICHE_FALTE = 2019` — steht diese Schranke im Register?** Siehe **T49.8**. *Nicht nachgesehen* |
| **K1n** | ⚠️ **`basislauf.py` braucht eine vierte Stufe „flackernd"** — siehe **T50.4**. Eigener kleiner Auftrag, mit Mutationsprobe |
| **K1o** | **Gealterte Zahlen im Docstring von `basislauf.py`** (1 312 und 62) — siehe **T50.6**. *Fortgeschrieben mit TB-51: jetzt **drei** Angaben, siehe **T51.6**.* *(Zwei Zeilen zu einer zusammengeführt 20.09.2026, TB-62, nach `DOKUMENTATIONSSTANDARD.md` Regel 9)* |
| **K1p** | **Journal-Inhaltsverzeichnis endet bei AG** — siehe **T50.7** |
| **K1q** | ⚠️ **`STRATEGIEN_uebersicht.md` liegt ebenfalls nicht unter `docs/projektfuehrung/`** — dieselbe Frage wie **T50.3**. *Fortgeschrieben mit TB-51: Entscheidung offen, siehe **T51.5**.* *(Zwei Zeilen zu einer zusammengeführt 20.09.2026, TB-62, nach `DOKUMENTATIONSSTANDARD.md` Regel 9)* |
| ~~K1n~~ | ~~`basislauf.py` braucht eine vierte Stufe~~ **ERLEDIGT durch TB-51 (T51.2)** |
| **K1r** | ⚠️ **`strategy_paths.get_strategy_paths()` legt `results/` und `logs/` an** — T46.8-Muster, siehe **T52.11** |
| **K1s** | ⚠️ **`CONFIG_DIR` im Selektionsmodus umfasst `email_config.py`** — siehe **T52.12** |
| **K1t** | **Modus deckt Verzeichnisse ab, keine Einzeldateien** — siehe **T52.13** |
| **K1u** | ⚠️ **Die Testdatei-Zahl in `UMGEBUNGEN.md` durch eine Regel ersetzen** — siehe **T52.19** |
| **K1v** | **`urllib3`/LibreSSL-Warnung in die Umgebungstabelle** — siehe **T52.20** |
| **K1w** | ⚠️ **Die Drei-Kategorien-Regel gehört auch in `docs/PRUEFPRINZIPIEN.md`** — sie ist eine Prüfregel, nicht nur eine Registerregel: *die Quelle des Grundes entscheidet, nicht der Zeitpunkt* |
| **K1x** | ⚠️⚠️ **Jeder `MAC_`-Auftrag beginnt mit Schritt −1 Ortsprüfung** (T55.6). ⭐ **Gegenstück für Cloud-Aufträge mitdenken**, wo der Ort bindet — dort ist die Prüfung „`trading-env/` existiert **nicht**" |
| **K1y** | **„Dreimal messen" heisst nicht „dreimal derselbe Aufruf."** Mindestens eine der Messungen rechnet **an der Quelle** — die registrierte Funktion direkt, nicht über das Werkzeug (T55.12) |
| **K1z** | ⚠️ **`docs/UMGEBUNGEN.md` ist wieder veraltet** — der Eintrag zur Zahl der Testdateien stammt aus TB-50 (**65**); TB-52 hat auf dem Mac **69** gemessen. *Die Datei veraltet schneller, als sie gepflegt wird — beim nächsten Mal mit Messdatum statt mit Zahl allein* |
| **K2a** | ⚠️ **`crontab -l` wird nie ungefiltert ausgegeben.** Zulässig: `awk '{print $1,$2,$3,$4,$5}'` (nur Zeitfelder) und `grep -c` (zählt, ohne zu zeigen). ⭐ **Gehört zu den Secrets-Regeln: Existenz wird geprüft, nie der Wert** |
| **K2b** | ⭐ **Vorprüfungen gehören vor die Sitzung, nicht in sie** — wenn ihr Ergebnis eine **Betreiberentscheidung** auslösen könnte. *Ein abgebrochener Mac-Lauf kostet eine Sitzung; drei lesende Befehle kosten drei Minuten* |
| **K2c** | ⭐⭐ **Prüfprinzip A7 gehört nach `docs/PRUEFPRINZIPIEN.md`, Gruppe A** (T55.16) |
| **K2d** | ⭐ **Eine Kostenmessung ist nie die Aussage, sondern ihr Stellvertreter.** Weicht der Stellvertreter ab, wird die eigentliche Aussage direkt geprüft — hier: „1 Blob" statt „+0,001 %" (T55.15) |
| **K2e** | ⚠️ **„Existiert schon ein Snapshot?" prüft den Ordnernamen `snapshots/<64 Hex>/`, nicht die Anwesenheit einer `MANIFEST.json`** (T55.18) |
| **K2f** | ⭐⭐ **Ein Abbruchkriterium benennt die Sache, nie ihren Stellvertreter** (T55b.5) — gehört auch in `docs/PRUEFPRINZIPIEN.md` |
| **K2g** | ⭐⭐ **Jede Behauptung im Register braucht ihren Beleg im Repo** (T55b.6) |
| **K2h** | ⭐ **Fallen Wortlaut und Zweck eines Abbruchkriteriums auseinander und ist jemand erreichbar: fragen** (T55b.5) — in ARBEITSWEISE §7c |
| **K2i** | ⚠️⚠️ **EIN NACHTRAG NENNT KEINE KONKRETE NUMMER, DIE ER NICHT SELBST GEMESSEN HAT.** Er sagt *„die nächste freie Nummer, gemessen"* und begründet nur die **Einordnung**; die Nummer vergibt die ausführende Sitzung. ⭐ **Herkunft: drei Kollisionen am 19.09. (0,87 · V1 · TB-54), alle aus Nachträgen, die eine Nummer nannten, ohne den Zielstand zu kennen** — der Betreuer kann das Repo nicht lesen und darf nicht so tun, als könnte er es |
| **K2j** | ⭐ **Eine Ersetzung im selben Arbeitsbaum ist gegen `HEAD` unsichtbar.** Wer Zeilen ersetzt, die dieselbe Sitzung angelegt hat, misst **zusätzlich** gegen eine Kopie des Standes davor (T54.3) |
| **K2k** | ⭐ **Ein Werkzeug, das vor dem Schreiben abbricht, ist besser als eines, das hinterher misst** — Anker müssen genau einmal vorkommen (T54.4) |
| **K2l** | ⚠️⚠️ **DIE GERÄTEANBINDUNG IST KEIN TERMINAL AUF DEM MACBOOK.** Gemessen am 19.09.2026: `uname -a` meldet **`Linux … Ubuntu 22.04.5 LTS`**, `python3 -V` **3.10.12**, das Repo hängt per **FUSE** unter `/sessions/…/mnt/trading-bot`. **`trading-env/bin/python3` ist als Datei da, lässt sich aber nicht ausführen** (`No such file or directory` — macOS-Binärdatei auf Linux). ⇒ ⭐ **Die Regel: _Die Anbindung liest das Repo, sie rechnet nicht darin._** Lesen, `grep`, `wc`, `cmp`, `shasum`, lesende git-Befehle und Ablage unter `docs/` gehen; Basislauf, Trockenlauf, Registerprüfer, `snapshot.py` und **jede Messung, deren Ergebnis ins Register soll**, brauchen weiterhin einen **Mac-Lauf**. ⚠️ **`UEBERGABE_2026-09-19.md`, Nachtrag 2 ist an dieser Stelle zu weit gefasst und gehört berichtigt** — dort steht „wo eine Sitzung über die Geräteanbindung auf `~/trading-bot` zugreifen kann, MESSE ICH SELBST", ohne die Grenze zu nennen |
| **K2m** | ⛔ **FABLE-ANTWORTEN SELBST ABHOLEN — GEPRÜFT UND VERWORFEN (19.09.2026).** Betreiberwunsch: statt Fables Antwort einzufügen nur „fable fertig" schicken, und die Sitzung holt sie sich. ⭐ **Gemessen, nicht vermutet:** Der Browser-Bereich der Claude-Desktop-App erreicht `claude.ai`, ist dort aber **nicht angemeldet** — er führt ein **eigenes Profil**, getrennt von Chrome und von der Desktop-App selbst (es erschien die Anmeldeseite, nicht die Unterhaltungsliste). ⇒ Der Weg wäre gangbar, aber **nur nach einer einmaligen Anmeldung durch den Betreiber** im Browser-Bereich; Zugangsdaten gibt die Sitzung grundsätzlich nicht ein. **Betreiberentscheidung 19.09.2026: so lassen** — Fables Antworten werden weiter als Text in den Chat eingefügt. ⚠️ **Nicht erneut vorschlagen.** Preis der Entscheidung, benannt: der Handgriff bleibt beim Betreiber. ⚠️ **Nebenbefund:** Für den Browser-Bereich wurde `claude.ai` mit Geltung „site" freigegeben; **diese Freigabe bleibt bestehen, bis sie in den Einstellungen der Desktop-App entfernt wird.** Der geöffnete Reiter ist geschlossen, angemeldet wurde nichts, gelesen wurde nur die Anmeldeseite |
| **K2n** | ⭐⭐ **IMMER DIREKT WEITERMACHEN.** Ausdrückliche Anweisung des Betreibers, 19.09.2026: *„Mache immer direkt weiter ohne das ich dich fragen muss wie geht es weiter."* **Eine Antwort endet nie mit einem Stillstand**; der nächste Handwerksschritt wird **getan**, nicht angekündigt und nicht zur Entscheidung gestellt. ⚠️ **Die Grenze bleibt unverändert:** Verfahrensfragen vor dem Tag gehen weiter an den Betreiber oder an Fable — aber als **anklickbare Entscheidungsvorlage neben der laufenden Arbeit**, nicht als Haltepunkt; und freigabepflichtige Befehle bleiben beim Betreiber. *„Weitermachen" heisst, alles bis zu ihnen fertig zu haben.* **Eingetragen in `ARBEITSWEISE.md` Abschnitt 13 (neu), in die Erinnerung und in Übergabe-Nachtrag 3 — drei Träger** |
| **K2o** | ⚠️ **EIGENER FEHLER, zweimal am selben Abend: eine SOLL-Zeilenzahl ausgegeben, die geschätzt und nicht gezählt war.** Beim Anhängen an das Register „SOLL 3108 / 92" (tatsächlich 3095 / 86) und beim Anhängen an den TB-59-Auftrag „SOLL 256" (tatsächlich 254). **Der Inhalt war beide Male richtig, die Vorhersage falsch** — und sie stand im Befehl wie eine Messung. ⭐ **Die Regel: Eine Zahl, die als SOLL ausgegeben wird, ist vorher gezählt worden. Sonst heisst sie ausdrücklich „geschätzt" oder entfällt.** ⚠️ **Warum das kein Formfehler ist:** Ein falsches SOLL neben einem richtigen IST sieht aus wie ein Befund und ist keiner — es verbraucht genau die Aufmerksamkeit, die ein echter Unterschied bräuchte. *Dieselbe Familie wie Block 7, Punkt 3: ein Name ist kein Messwert, und eine Schätzung ist keine Messung.* ⭐ **Was stattdessen trägt und beide Male getragen hat: die zweite `numstat`-Spalte.** Sie ist eine Messung, keine Vorhersage |
| **K2p** *(im Nachtrag (n) als `K2r` vorgeschlagen; `K2r` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2p`, gemessen)* | ⭐⭐ **Mehrfachtesten ist eine Eigenschaft der Suche, nicht des Kandidaten.** Wer viele Varianten prüft, muss **zählen**, wie viele — sonst ist keine Kennzahl am Ende deutbar. ⚠️ **Gilt auch für uns heute:** jede verworfene Parametervariante zählt |
| **K2q** *(im Nachtrag (n) als `K2s` vorgeschlagen; `K2s` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2q`, gemessen)* | ⚠️ **Schwellen werden vor dem Lauf registriert, nicht nach den Ergebnissen abgeleitet** (AF3) |
| **K2r** *(im Nachtrag (n) als `K2t` vorgeschlagen; `K2t` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2r`, gemessen)* | ⭐ **Eine Vorlage von aussen wird gegen das Register gemessen, bevor sie in den Backlog geht** — nicht danach |
| **K2s** *(im Nachtrag (o) als `K2u` vorgeschlagen; `K2u` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2s`, gemessen)* | ⚠️⚠️ **Eine Kennzahl je Regime ist eine Kennzahl auf einer Teilstichprobe.** ⭐ **Vor jeder regimebedingten Aussage wird die Zahl der Episoden im Regime gemessen und genannt** (MI2) |
| **K2t** *(im Nachtrag (o) als `K2v` vorgeschlagen; `K2v` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2t`, gemessen)* | ⚠️⚠️ **Revidierte Daten sind Look-ahead.** Makroreihen und Nachrichten nur „wie damals erstveröffentlicht" — sonst gar nicht (MI3) |
| **K2u** *(im Nachtrag (o) als `K2w` vorgeschlagen; `K2w` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2u`, gemessen)* | ⭐ **Ein Ähnlichkeitsmass ist ein Parameter.** Vor Benutzung registrieren, Vergleiche zählen (MI4) |
| **K2v** *(im Nachtrag (o) als `K2x` vorgeschlagen; `K2x` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2v`, gemessen)* | ⭐ **Wer Kapital zwischen Strategien verteilt, betreibt selbst eine Strategie** — dieselben Regeln, dieselbe Registrierung (MI5) |
| **K2w** *(im Nachtrag (p) als `K2y` vorgeschlagen; `K2y` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2w`, gemessen)* | ⭐⭐ **Wer behauptet, etwas sei besser als Zufall, baut das Zufallsmodell mit** — und schickt es durch dieselbe Prüfung (QR1) |
| **K2x** *(im Nachtrag (p) als `K2z` vorgeschlagen; `K2z` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2x`, gemessen)* | ⚠️⚠️ **Gespeichert ist nicht unverändert.** Eine Aufzeichnung, die Nachträglichkeit ausschliessen soll, braucht **Anfügen und Verkettung**, nicht nur Felder (QR2) |
| **K2y** *(im Nachtrag (p) als `K3a` vorgeschlagen; `K3a` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2y`, gemessen)* | ⭐ **Eine Prognose ohne vorher festgelegte Auflösungsregel ist nicht auswertbar** (QR3) |
| **K2z** *(im Nachtrag (p) als `K3b` vorgeschlagen; `K3b` war zum Zeitpunkt der Einarbeitung nicht die nächste freie — vergeben als `K2z`, gemessen)* | ⚠️ **Eine Abschaltregel ist selbst eine Strategie** und wird wie eine getestet (QR4) |
| **K3a** *(im Nachtrag (q) als `⟨a⟩` offen gelassen — vergeben als `K3a`, gemessen)* | **Eine Zahl in einem Datensatz trägt ihren Schätzer im Namen oder sie existiert nicht.** `confidence` und `stability_score` sind die Anlassfälle; die Regel gilt für jedes Feld, das ein Urteil ausdrückt |
| **K3b** *(im Nachtrag (q) als `⟨b⟩` offen gelassen — vergeben als `K3b`, gemessen)* | **Jede Messung trägt ihre Auflösung.** Wer eine Verzögerung nennt, nennt die feinste im Datenbestand vorhandene Zeitauflösung im selben Satz |
| **K3c** *(im Nachtrag (q) als `⟨c⟩` offen gelassen — vergeben als `K3c`, gemessen)* | **Die Zahl der Tests wird vor dem Lauf registriert, nicht nach dem Lauf gezählt.** Gilt für Selektionen, Hypothesen und Graphenkanten gleichermaßen |
| **K3d** *(im Nachtrag (q) als `⟨d⟩` offen gelassen — vergeben als `K3d`, gemessen)* | **Kausalsprache ist ein Pflichtfeld, kein Wortschatz.** Eine Kante oder ein Satz, der Wirkung behauptet (`verstärkt`, `verursacht`, `überträgt`), nennt das Verfahren, das ihn dorthin gebracht hat — oder er wird beschreibend formuliert |
| **K3e** *(aus der Berichtigung zu (q) und (r) vom 19.09.2026, 21:05, Punkt 5 — dort ohne Nummer; vergeben als `K3e`, gemessen)* | ⭐⭐ **Ein Nachtrag unterscheidet in jedem Satz zwischen gemessen und erschlossen — und markiert das Erschlossene als solches.** Ein Bezeichnername ist kein Messwert. `MIN_HISTORY_HOURS` sagt, dass eine Konstante Stunden zählt; es sagt nichts über die Auflösung der Daten. `volatility_breakout` sagt, wie ein Bot heißt; es sagt nichts über seine Renditeverteilung. ⚠️ *Dieselbe Klasse wie Fables Schicht-3-Befund: „Der Lese-Audit beweist, welche DATEN gelesen wurden. Er sagt nichts darüber, welcher CODE gelesen hat." Ein Name beweist, wie etwas heißt. Er sagt nichts darüber, was es tut* |
| **K3f** *(im Nachtrag (r) als `⟨a⟩` offen gelassen — vergeben als `K3f`, gemessen)* | ⭐⭐ **Ein Prüfkriterium, das nach dem Blick auf das Ergebnis gewählt wird, ist eine Selektion.** Gilt für Kill Tests, Ausschlussregeln und Plausibilitätsprüfungen gleichermaßen — Quelle des Grundes, nicht Zeitpunkt (F17) |
| **K3g** *(im Nachtrag (r) als `⟨b⟩` offen gelassen — vergeben als `K3g`, gemessen)* | ⭐⭐ **Jede Probe wird an einem bekannt kaputten Gegenstand validiert, bevor sie an einen echten darf.** Die allgemeine Fassung von B1, über Mutationsproben hinaus |
| **K3h** *(im Nachtrag (r) als `⟨c⟩` offen gelassen — vergeben als `K3h`, gemessen)* | **Ein Test ohne vorher festgelegte Schwelle ist eine Meinung.** Größe, Schwelle und Folge stehen zusammen |
| **K3i** *(im Nachtrag (r) als `⟨d⟩` offen gelassen — vergeben als `K3i`, gemessen)* | **Zusammengesetzte Maße brauchen registrierte Gewichte — oder es werden Schwellen statt Gewichte verwendet.** Schwellen sind vorzuziehen |
| **K3j** *(im Nachtrag (r) als `⟨e⟩` offen gelassen — vergeben als `K3j`, gemessen)* | **Ein Verfahren, das Versagen sucht, braucht eine Zulässigkeitsmenge und eine Kontrolle.** Sonst findet es immer etwas |
| **K4h** | ⭐ **JOURNAL-RÜCKSTAND ABGEARBEITET (20.09.2026, TB-67).** Zehn Blöcke `BK`–`BT` aus den acht offenen Journal-Nachträgen (f), (g), (20a)–(20f) — gemessen mit zwei Mustern je Nachtrag (TB-Nummer in der Kopfzeile, wörtlicher Satz); (f) war damit prüfbar und offen, **nicht prüfbar: keiner**. Das Messprotokoll des Rückblick-Blocks `2s` aus Nachtrag (m) (13 `T`-Zeilen) steht zeichengleich in `BK`/`BL`/`BM` — damit haben TB-53b, TB-58 und TB-58b einen Journalblock, und der in `K4g` offene Ort ist nach Zeile 3 dieser Datei das Journal. Jeder Block trägt die Quellenzeile `*Quelle: …/nachtraege/JOURNAL_NACHTRAG_<datum><buchstabe>.md`, bei `BG`–`BJ` nachgetragen (14 Zeilen: 10 neu, 4 nachgetragen, 0 nicht zuordenbar). Die sieben `B`-Zeilen aus (m) sind **nicht** als Regeln eingetragen; je Zeile geprüft in `docs/ERGEBNIS_TB-67_journal_einarbeitung.md`, Nachweis 6 (5 ja, B2 teilweise, B3 nein) |
| **K4i** | ⭐ **DER ERÖFFNUNGSTEXT STEHT NUR NOCH EINMAL (20.09.2026, TB-68).** Gemessen: beide Fassungen — `UMZUG.md` Abschnitt 6 (vier Dokumente, Platzhalter) und `UEBERGABE_2026-09-19.md` Block 9 (fünf, fester Name) — stammten aus **demselben Commit `2723c16`** und waren seither unverändert: *als Widerspruch geboren, nicht auseinandergelaufen*; **und `UMZUG.md` Schritt 3, Zeile 9 hatte die Kopie selbst angeordnet.** Beide zeigten auf `projektfuehrung/PRUEFPRINZIPIEN.md` — dort lag die Datei nie (`git log --all`, 0 Commits; sie liegt in `docs/`). ⭐ **Jetzt:** Abschnitt 6 ist die einzige, ausdrücklich verbindliche Fassung — fünf Dokumente, je mit Repo-Pfad in Klammern, `PRUEFPRINZIPIEN.md` ohne Ordner, Prüfung der Geräteanbindung im Text statt als Nachsatz in Abschnitt 8; Block 9 ist ein Verweis (Regel 9, 9/20 Zeilen, jede zugeordnet); Schritt 3, Zeile 9 verlangt den Verweis. Keine dritte Fassung in `docs/` (drei Muster, Zahlen im Ergebnisdokument); `START_HIER.md` trägt eine **andere** Leseliste für eine andere Leserschaft — an TB-69 vorgelegt. ⚠️ **Offen beim Betreiber:** `UEBERGABEPROTOKOLL.md` in den Lesepfad (gemessen: 0 Treffer in den Führungsdokumenten des Chats, 32 von 40 Ergebnisdokumenten ohne Erwähnung; Empfehlung „bei Bedarf“-Zeile) · Platzhalter oder fester Name (Empfehlung fest). **Regel:** *Ein Verfahren, das eine Vorlage und eine Abschrift verlangt, hat die zweite Fassung nicht zugelassen, sondern bestellt — die Reparatur muss die Anordnung ändern, nicht nur die Kopie.* `ERGEBNIS_TB-68_eroeffnungstext.md` |
| **K4j** | ⭐ **DREI CODE-STELLEN MÜSSEN REGISTER 24.2 FOLGEN, SOBALD DER LAUFCODE GESCHRIEBEN WIRD (20.09.2026, TB-71) — geführt, nicht ausgeführt.** Register 24 (Betreiberentscheidung 20.09., 18:15) präzisiert Festlegung 1: Der Kapital-Drawdown der Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe des Kapitalpfads gerechnet (1a), auf denselben Tagen wie der Benchmark; der ereignisindizierte Drawdown aus `equity_simulation.py` wird berichtet, nicht bewertet. Dem müssen folgen: **(1)** `research/vorregistrierung/auswertung.py`, Datenvertrag Z. 40–58 — `kapital_drawdown_pct` kommt aus derselben Tagesreihe wie der Sharpe (⚠️ Datei eingefroren, Register 15.8 Nr. 3 — gehört zu **TB-30b**); **(2)** `beispieldaten.py` Z. 24–26 und Z. 125 — rechnet den Drawdown heute ausdrücklich **nicht** aus der Tagesreihe und sagt im Kopf, das sei auch im echten Lauf so; **(3)** `registerdaten.py:70`, `FESTLEGUNGEN[1]` — Text präzisieren, sobald 1 und 2 stehen. ⭐ Der Laufcode selbst existiert nicht (gemessen 20.09.: nichts im Repo schreibt `zellen.csv` oder `tagesreihen/<zelle_id>.csv` ausser `beispieldaten.py`) — **Spezifikation, kein Umbau**. ⛔ Die Grösse der MtM-Abweichung (TB-73) ist nach Register 24.3 für keine dieser drei Stellen ein Argument. Nebenbei erledigt: die Wahl W/C aus Register 23.3 ist mit TB-71 gegenstandslos (Satz zur Zeitachse, keine Codeänderung) — der Halbsatz *„vor dem Vollzug steht die Entscheidung W/C aus Register 23.3"* im Schlussblock von Abschnitt 2 ist damit überholt; der Vollzug braucht nur noch die Betreiberfreigabe aus 21.9. `ERGEBNIS_TB-71_register_schliessen.md` |
| **K4k** | ⛔ **TB-72 IST ANGEHALTEN, NICHT ERLEDIGT (20.09.2026, Schritt 1 gemessen, Schritte 2–7 warten auf Fable).** Die Messung in beide Richtungen (`research/faltenplan_neun/erste_falte_trockenlauf.py`, zwei Anläufe byteweise gleich, zweite Methode `loader_lesart` 9/9) zeigt: Registertext 4a und 3b (a) laufen bei **sechs** Bots auseinander — `t3_supertrend` **später** (2018 → 2019, die im Auftrag erwartete Instanz), `rsi2_crypto` **früher** (2019 → 2018, `H = 2`) und die vier Aktien-Bots **früher** (2017/2018 → **1967**, `H = 16`; Kursdateien ab 1962-01-02 + 1 825 Tage). Register 21.3 (b) *„bindet 3b (a)"* hat keine Richtung, seine Begründung deckt nur die leere Falte, und 4a trägt mit *„Universum … liegt vor"* eine Bedingung, die der Trockenlauf nicht prüft. ⭐ **Offene Frage bei Fable** (`FABLE_ANFRAGE_2026-09-20e_erste_falte.md`, vorgelegte Lesart `erste Falte = max(4a, 3b (a))` — dann ändert sich genau `t3_supertrend`). Bis zur Antwort: kein Code geändert, `faltenplan.json` und beide Benchmark-Tabellen unberührt (`a163c498…`, `4549395f…`, `0e54ac5c…`). ⚠️ Für Schritt 3 vorgemerkt: `ergebnisse/faltenplan.json` ist TB-30a-Stand (TB-61 Z. 251) — die Gegenüberstellung *„genau ein Bot, genau eine Falte"* gilt nur gegen den Speicherstand (`docs/belege/TB-72/faltenplan_4a_stand_vor_tb72.json`). `ERGEBNIS_TB-72_schritt1_erste_falte.md`, Journal-Nachtrag `(20j)` |
| **K4l** | ✅ **TB-72 IST ERLEDIGT (20.09.2026, Schritte 2–7 nach Fables Konjunktions-Antwort) — `K4k` ist damit geschlossen.** Register Abschnitt 25 (Berichtigung mit Ersatztext, append-only 220/0): Fables Neufassung von 4a / 21.3 (b) als **Konjunktion** — ein Jahr ist Selektionsfalte, wenn (i) Datenhorizont und Vorlauf am 1. Januar **und** (ii) der Trockenlauf es tragen; 15.6 (a) und 21.3 (b) tragen die Marke ERSETZT, Wortlaut bleibt. Code (`e7a4108`): `faltenplan.py::erste_falte` ist die Konjunktion — Kandidaten ab `erste_falte_4a` (bisher `erste_falte`), Bedingung (ii) über `erste_falte_trockenlauf.erste_falte_nach_3b` (Loader im Kindprozess des TB-40-Werkzeugs, Falte für Falte, Schluss beim ersten `H ≥ 1`; keine Konstantenkopie). **Wirkung: genau ein Bot, `t3_supertrend` 2018 → 2019, sieben Falten**; `DD_Toleranz` −12,89 / −24,73 / −45,16 → **−13,90 / −26,57 / −48,10** (25/50/100 %, trifft TB-65 C1), acht Bots gegen `_vt.json` zeichengleich (6 900 Stufen). Neue Dateien **daneben**: `ergebnisse/faltenplan_tb72.json`, `ergebnisse/benchmark_drawdowns_tb72.json`; `faltenplan.json`, `benchmark_drawdowns.json`, `_vt.json` byteweise unberührt. Test `research/faltenplan_neun/test_erste_falte_trockenlauf.py` (50/50, ~3 min, Mutation am echten `faltenplan.py` 38/12 rot, zurückgenommen). ⚠️ **Offen und benannt:** Vollzug der Sperrliste (Betreiberfreigabe 21.9, jetzt mit der `_tb72`-Tabelle statt `_vt`; `registerbericht.py:178` dabei nachziehen); **TB-74** (Bedingung (i): `RECENT_YEARS_ONLY` als Datenuhr, `entry_cutoff` je Symbol gegen `fensteranker` je Markt); `faltenplan()` kostet je Prozess jetzt rund 25 s mehr (9 Kindprozesse) — `test_vorregistrierung.py` Teil H zahlt das sechsmal. `ERGEBNIS_TB-72_erste_falte_aus_trockenlauf.md`, Journal-Nachtrag `(20k)` |
| **K4m** | ✅ **TB-73 IST ERLEDIGT (20.09.2026) — DIE MtM-WIRKUNG IST GEMESSEN UND BERICHTET, NICHT BEWERTET.** Register **24.6** (Tatsachennotiz, append-only 124/0) trägt die Zahl, die 24.4 ankündigte; 24.3 bleibt die Entscheidungsregel, kein Satz wirft sie auf. Forschungsskript `research/mtm_drawdown/` (kein Laufcode; importiert Kosten, Startkapital, `messkette`, Exposure-Definition; `shared/`, `strategies/`, `research/vorregistrierung/` unberührt, drei Sperrlisten-Hashes und beide `_tb72`-Dateien unverändert). **Gemessen an den TB-24-Listen und `data/`, Falten aus `faltenplan_tb72.json`:** in **59 von 64** Falten mit Grundlage ist der tägliche MtM-Drawdown tiefer als der ereignisindizierte, Median der Differenzen je Bot −1,39 bis −3,09 pp, Faktor 1,04 / 1,30 / 1,88 (10./50./90. Perzentil); 2020 Aktien: `turtle_soup_stocks` −29,91 → −34,45, `volatility_breakout` −9,41 → −12,60, `rsi2_mean_reversion` −9,01 → −11,28; 2022: `turtle_soup_crypto` −27,86 → −30,38, `volatility_breakout` −23,97 → −25,80. ⚠️ **Zwei Tatsachen, die der Auftrag anders erwartete:** (1) **2020 ist bei keinem Krypto-Bot messbar** — die fünf TB-24-Krypto-Listen beginnen 2021-09 bis 2022-03 (Datenstand vor TB-34, 1 826 Tageszeilen); Falten 2018–2020 Krypto ohne Grundlage, nicht ersetzt. (2) *„M nie flacher als E"* ist eine Näherung, kein Satz der Rechnung: in **5 von 64** Falten ist M flacher (`elliott_wave_stocks` **2020** +3,90 pp und **2022** +1,20 pp, `t3_supertrend` 2023, `volatility_breakout_crypto` 2023, `volatility_breakout` 2026) — jeweils unrealisierte **Gewinne** in offenen Positionen am E-Tief, von Hand nachgerechnet (Probe 3), jeder Fall zerlegt (`ergebnisse/richtungsfaelle.md`). Proben 24/24, Mutationsprobe 3× rot. *„Bei 25/50/100 % Exposure"* nicht gerechnet: das ist das Benchmark-Argument, ein Bot hat je Falte eine Exposure (steht daneben). ⛔ **Keine Empfehlung, keine Abwägung** — Register 24.3. Offen und benannt: Krypto-Listen ab 2018 wären ein neuer Backtest (kein Auftrag); `K4j` unverändert. `ERGEBNIS_TB-73_mtm_wirkung.md`, Journal-Nachtrag `(20l)` |

⭐ **Die Fehlerregel zu K2l**, nach `DOKUMENTATIONSSTANDARD.md` Regel 3 (Nachtrag (s)):

| Fehler | ⇒ Regel |
|---|---|
| Beinahe „gemessen über die Geräteanbindung" geschrieben, ohne den **Interpreter** zu nennen — und `3.9.6` stand als Erwartung im Kopf, weil es im Register steht | ⭐ **Eine Messung nennt die Umgebung, in der sie lief, nicht die, in der sie hätte laufen sollen.** Eine Umgebung ist so wenig ein Messwert wie ein Name |

---

## 5 — Nach TB-30b

| # | Punkt |
|---|---|
| **C8** | **Portfolio-Sicht** — der einzige Punkt mit neuer Information, aber **erst mit dem reparierten Mass**. Vorher zeigt sie Zahlen, die im Dezember wieder falsch sind |
| **P3** | **Gewichtete Kurve rückwirkend rekonstruieren** — aus Allokation je Bot (2 / 5 / 10 / 25 %), Positionslimits und der Zuteilungskaskade aus TB-26; `equity_simulation.py` kann es bereits. ⚠️ **Trägt eine Annahme in sich:** Sie unterstellt, die heutigen Allokationswerte hätten auch damals gegolten. Ändert die Neuselektion sie, ändert sich **rückwirkend der Live-Ertrag der Vergangenheit** — eine Kennzahl, die sich nachträglich bewegt. Deshalb **nach** TB-30b, zusammen mit C8. Hängt an **P2** |
| **P4** | **Variable Positionsgrösse nach Marktlage** — vom Nutzer am 15.09.2026 wieder aufgeworfen. ⚠️ **Teilweise schon beantwortet:** Vol-Skalierung wurde gemessen und hat bei **8 von 9** Bots geschadet (erledigt, Block I8). Offen bleibt die allgemeinere Frage aus **I16**, ob eine Positionsgrössen-Ebene diesen Bots hilft — sie braucht ein Trade-Journal mit Einstiegsmerkmalen, also **P2**. Und sie ist erst sinnvoll, wenn **Rang 3** entschieden hat, welche Bots es überhaupt noch gibt |
| **I19** | **Staging-Ebene**, minimal: ein Bot mit einer Flagge, die ihn aus **jeder** Portfolio-Zahl und dem Crash-Knopf heraushält. **Ein Nachmittag — wenn es nicht an einer Ereignis-Datenbank hängt** |
| ~~S-E1~~ | **ERLEDIGT 15.09. (TB-33, PR #106) — DURCHGEFALLEN**, alle drei Bedingungen. Netto −0,0096 % je Ereignis ueber **395** Monatswechsel, Perzentil **86** statt 95. *Der Effekt aus McConnell/Xu ist nach Kosten nicht mehr da.* **Der Pfad hat funktioniert** — und die Sweep-Regel hat eine besser aussehende Variante korrekt abgewiesen. Journal **AM** |
| **I10** | **Point-in-time-Universum** nach Dollar-Volumen — behebt zugleich die Survivorship-Verzerrung aller vier Aktien-Bots *(I2 ist dieselbe Aufgabe)* |
| **S-D1** | **Gap-and-Volume-Drift** — beste Stichprobe (1 000–1 400 Ereignisse). Braucht I10 |
| **Z4 → Z1/Z2** | **Zufalls-Timing-Test zuerst.** Trägt der Zigzag-Detektor nichts, sind Welle-3 und Welle-4 gegenstandslos. Erst danach „Elliott Wave mit W2 + W4" als **neuer vorregistrierter Lauf** — mit dem Vermerk, dass Z.2 bereits gesehen wurde |
| **Z5** | `docs/UEBERSICHT_RESEARCH.md` **einmal nach TB-30b** aktualisieren, nicht jetzt |
| **E-Rest** | E3 (Zeitstempel bei Auto-Refresh) prüfen oder löschen · E4 (Favicon) zwei Minuten oder löschen |
| **Aufräumstunde** | F4 (Remote Control), F7 (Cron-Altlasten), F8, F9, O5, AD2 (`float` statt numpy), AB3/AB4 — **gebündelt oder gelöscht**, keiner verdient eine eigene Zeile |
| **H #61/#62** | #61 schliessen (kollidiert mit #62), #62 entscheiden. *Ein offener PR ist keine Aufgabe, sondern eine Verzögerung mit Nummer* |

---

## 6 — Geparkt, null Arbeit *(ins Archiv verschoben 20.09.2026, TB-60)*

Die Tabelle (D5, D2 / D3, I16, I.3d, I.3a / D4, AC 1–6) steht zeichengleich in `BACKLOG_ARCHIV.md`, Abschnitt 6.

---

## 7 — Architektur, offen

| # | Punkt |
|---|---|
| **G1** | ⚠️ **Alles hängt an einem MacBook, das aufgeklappt und wach bleiben muss.** *„Cron holt verpasste Läufe nie nach."* **Die eine Architekturfrage, die den Live-Record berührt** — und der Live-Record ist der Holdout |
| **G2** | Der Zugangstoken steht in der URL — Browserverlauf, Screenshots. Einzeiler |

*Gestrichen:* G3 („keine Daten" gegen „keine Verbindung"), G5 (PWA). **G4 ist
entschieden** — kein Crash-Knopf für Fremdplattformen.

---

## 8 — Gestrichen (14.09.2026, nach Fables Prüfung)

Damit nichts davon zurückkommt. Begründungen im Journal, Block **AG**.

**Der Trading-App-Bogen:** C0–C7, C9, C10 · J.1, J.2, J.4, J7 — *Monate Arbeit
an einer Oberfläche für Zahlen, deren Erzeugung gerade repariert wird.* C7
(Systemgesundheit) löst ausserdem das falsche Problem: Die Antwort sind vier
Cron-Zeilen, die an A1 hängen.

**Aus dem Strategie-Katalog:** `S-K1` (dieselbe Ertragsquelle **und** dieselbe
Horizont-Klasse wie vorhandene Bots; Krypto-Daten reichen nicht zurück) ·
`S-C1` (vierte Umkehrstrategie auf demselben Universum — Umkehr-Paare steigen
**2,58 ×** häufiger gemeinsam ein als der Zufall) · I17 HMM (*„ein
Herausforderer ohne Titelverteidiger"*) · I18-**Agent** (die Skripte bleiben) ·
I.3c Gewinnsicherung (*„keine Erkenntnis, das ist Arithmetik"*) · I.3e
Hebel-Simulation (Auslastung ist ein **Parameter**, kein Befund).

**Forschung:** K.4b HRP ein viertes Mal (*jede Gewichtungsebene ist
gegenstandslos, bis Rang 3 entschieden hat, welche Bots es gibt*) · N2
(HRP-Nachtragsskript, fällt mit) · K.5 `trend_overlay` als eigener Punkt
(Doppel zu `S-A1`) · **D1 Anbieter-Schnittstelle** (*lohnt erst mit einem
dritten Anbieter — den es vorerst nicht geben soll*).

**Anzeige:** E1 Eurobeträge (die Zahl behauptet mehr, als sie hergibt; kehrt
mit D5 zurück) · E2 Saldo im Crash-Dialog (*eine Notfalloberfläche ist keine
Anzeige*).

**Termine:** ⚠️ **Der Oktober-Prüftermin für Elliott Wave Aktien.** Ein Urteil
über den Bot **vor** dem vorregistrierten Lauf wäre eine Entscheidung
ausserhalb des Registers. Zulässig im Oktober ist nur, was **keine
Parameteränderung** ist — der Zufalls-Timing-Test als Messung, vorregistriert,
Ergebnis ins Journal.

**Als erledigt geschlossen:** I6 (gegenstandslos) · I.3g Sentiment
(geschlossen — **geprüft 14.09.: kein Cronjob, kein Dienst angelegt**) · I8 Vol-Skalierung · M2/M3 (durch TB-30b ersetzt und
entschieden) · I3, I5, I2 (in anderen Punkten aufgegangen).

---

## 9 — Arbeitsregeln *(ins Archiv verschoben 20.09.2026, TB-60)*

Die Arbeitsregeln führt `ARBEITSWEISE.md` (P.1 in Abschnitt 1, P.2 in Abschnitt 7, P.4 in Abschnitt 3, P.6 in Abschnitt 8). ⚠️ Der Wortlaut von P.1 bis P.6 liegt zeichengleich in `BACKLOG_ARCHIV.md`, Abschnitt 9, weil er Angaben enthält, die in `ARBEITSWEISE.md` nicht stehen (P.3, P.5 und der offene Punkt P1 vollständig; Fallbeispiele und Tabellen aus P.2, P.4 und P.6) — Befund in `docs/ERGEBNIS_TB-60_backlog_archiv.md`, Nachweis 7.
