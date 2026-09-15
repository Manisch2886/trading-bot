# Übergabe TB-33 — Nulltest S-E1 Turn-of-Month

**Stand: 15.09.2026.** Zweig `claude/new-session-kqgzcx`, Basis `main`
(`9afac63`).

---

## 1. Die Pfadfrage — zuerst, weil sie der Gegenstand ist

> **Ist der Weg sauber gelaufen — und wenn nein, an welcher Stelle wurde eine
> Entscheidung nötig, die nicht im Register stand?**

**Der Weg ist sauber gelaufen, soweit er hier laufen konnte.** Der Selbsttest
bildet das Urteil maschinell aus den neun Pfadkriterien und meldet:

```
110/110 Pruefungen bestanden.
WEG SAUBER - alle neun Pfadkriterien P1 bis P9 bestanden.
Keine Stelle, an der eine Entscheidung ausserhalb des Registers noetig war.
```

**Zwei Einschränkungen, beide gehören zur Antwort und nicht ins Kleingedruckte:**

### 1.1 Vier Festlegungen fehlten im TB-30a-Register

Alle vier liegen **vor** dem Lauf, keine einzige in ihm.

| | Was fehlte | wer | wann |
|---|---|---|---|
| **A1** | Instrument **SPY** statt des `sp500_top150`-Universums (TB-30a §4.1) | Auftraggeber | vor dem ersten Commit |
| **A2** | Sweep-Zellen **−2/+3, −1/+2, −1/+4 + QQQ/IWM/EFA** statt „2 bis 6 Tage" (TB-30a §5.1) | Auftraggeber | vor dem ersten Commit |
| **A3** | **Bootstrap-Verfahren und Mindest-Ereigniszahl** — in TB-30a gar nicht geregelt | dieser Lauf | vor dem ersten Commit |
| **A4** | **Faltenzuordnung**: zu welchem Jahr gehört ein Wechsel Dezember→Januar? | dieser Lauf | beim Schreiben der Auswertung, **vor jeder Rechnung** |

**A1 und A2 sind keine Überraschung** — sie stehen so in der
Aufgabenstellung; bemerkenswert ist nur, dass sie dem eingefrorenen Register
aus TB-30a **widersprechen**. Deshalb stehen sie als Abweichung mit Grund und
Urheber in Abschnitt 0 der Strategiekriterien und nicht still im Code.

**A3 war eine echte Lücke.** TB-30a nannte „Bootstrap-Intervall" als Wort,
aber kein Verfahren, keine Ziehungszahl, keinen Startwert und keine
Mindest-Ereigniszahl. Ohne Startwert gäbe es keine Wiederholbarkeit — und die
ist selbst ein Pfadkriterium.

### 1.2 **A4 ist der eigentliche Befund dieses Nulltests**

Ein Turn-of-Month-Ereignis um den Jahreswechsel liegt in **zwei**
Kalenderjahren. Zu welcher Falte gehört es? Das TB-30a-Register regelt
Faltenlängen, Purge und Embargo — aber nicht das.

Die Lücke fiel auf, als das Auswertungsskript die Zeile `"jahr": ...`
brauchte. Sie ist klein, sie ist harmlos, und die gewählte Richtung
(Zuordnung über den **Einstiegstag**, Dezember→Januar fällt ins alte Jahr)
ist die konservative: sie schiebt keine Beobachtung in die
Bestätigungsperiode hinein, die dort nicht anfängt.

> **Und genau darum wurde S-E1 gerechnet.** Eine Festlegung, die niemand
> vermisst, bis ein Skript sie braucht. Bei `S-B1` — neun Bots, 2 416 Zellen,
> viel Code — wäre sie nicht aufgefallen. Sie wäre im Vorbeigehen im Code
> getroffen worden, hätte in keinem Register gestanden, und niemand hätte
> hinterher sagen können, ob sie vor oder nach den ersten Zahlen entstand.
>
> Der Nulltest hat also getan, wofür er da war: **er hat eine Lücke im
> Verfahren gefunden, und zwar an der billigsten möglichen Stelle.**

**Ist der Weg damit durchgefallen?** Nein. Abschnitt 2 der Pfadkriterien
regelt das ausdrücklich: eine Ergänzung ist zulässig, **solange sie im
Register steht, bevor gerechnet wurde**, und der Bericht sie als Ergänzung
ausweist. Beides ist bei allen vier der Fall. Unzulässig wäre gewesen, sie
erst zu bemerken, wenn die Zahlen schon da sind.

### 1.3 Der Weg ist nicht zu Ende gelaufen — aus einem anderen Grund

Register → Backtest → Forward-Test → Bestätigungsperiode → Bericht: der
**Backtest auf echten Daten fehlt**. Nicht, weil eine Entscheidung offen
gewesen wäre, sondern weil **yfinance aus der Arbeitsumgebung nicht
erreichbar ist** (der Proxy antwortet mit 403). Das ist ein Umgebungsproblem,
kein Pfadfehler — aber es heisst, dass der letzte Abschnitt des Weges erst
auf dem Mac belegt ist.

---

## 2. Das Ergebnis der Strategie

> ⚠️ **Es gibt noch keines.** Kein einziger Kurs von SPY ist in diese Arbeit
> eingegangen.

Die Auswertung lief — wie in der Aufgabenstellung für diesen Fall vorgesehen
— **gegen erzeugte Beispieldaten**. Das ist dieselbe Zusicherung wie in
TB-30a: *das Auswertungsskript hat seinen Test bestanden, als es noch nichts
zu deuten gab.*

**Die Zahlen aus den Beispieldaten sagen nichts über den
Turn-of-Month-Effekt.** Sie zeigen nur, dass die Maschinerie in sechs
gebauten Lagen genau das tut, was das Register verlangt — insbesondere, dass
**jede der drei Bedingungen ihren eigenen Fall trägt**:

| Lage (erzeugte Kurse) | B1 | B2 | B3 | Urteil |
|---|:--:|:--:|:--:|---|
| Effekt deutlich vorhanden | ✓ | ✓ | ✓ | `BESTANDEN` |
| Kein Effekt — das Fenster ist wie jeder Tag | ✗ | ✗ | ✓ | `DURCHGEFALLEN` |
| Nur der Falten-Median fällt | ✗ | ✓ | ✓ | `DURCHGEFALLEN` |
| Nur das Bootstrap-Intervall fällt | ✓ | ✗ | ✓ | `DURCHGEFALLEN` |
| Nur das Perzentil fällt — **reines Beta** | ✓ | ✓ | ✗ | `DURCHGEFALLEN` |
| Kern fällt, Sweep −2/+3 bestünde | ✗ | ✗ | ✗ | `DURCHGEFALLEN` |

Die fünfte Zeile ist die interessanteste: ein Markt mit kräftiger Drift, in
dem das Turn-of-Month-Fenster **netto positiv** ist — und trotzdem schlechter
als praktisch jedes andere Vier-Tage-Fenster desselben Instruments. Genau
dafür ist Test 2 da, und er zieht.

**Der echte Lauf** ist Schritt 6 und 7 des Testdokuments.

---

## 3. Was gebaut wurde

Alles unter `research/turn_of_month/` und in `docs/`. **Kein Bot-Code.**

| Datei | was sie tut |
|---|---|
| `register.py` | Die Festlegungen als Code. Jede Zahl genau einmal |
| `handelstage.py` | Handelstage statt Kalendertage — **ohne zweiten Kalender** |
| `kennzahlen.py` | Bootstrap und Platzhalter-Verteilung, fester Seed, **ohne `scipy`** |
| `herkunft.py` | Drei Hashes, append-only-Protokoll — nach dem Muster aus TB-30a |
| `auswertung.py` | Das eingefrorene Auswertungsskript |
| `beispieldaten.py` | Erzeugte Kurse — gesetzt werden **Kurse**, nie Ergebnisse |
| `datenlauf.py` | yfinance → eigener Datenordner (**Schritt für den Mac**) |
| `staging.py` | Die Staging-Ebene (I19), minimal |
| `test_turn_of_month.py` | Der Selbsttest, 110 Prüfungen, bildet das Pfadurteil |

### Drei Entwurfsentscheidungen, die den Unterschied machen

**1. Die Sweep-Regel steht in der Signatur, nicht im Kommentar.**
`urteil()` nimmt **genau ein** Argument entgegen: den Kern. Es gibt keinen
Parameter, über den eine Sweep-Zelle hineinkäme. Eine Regel im Kommentar wäre
bei der nächsten Änderung weg; eine in der Signatur muss jemand ausdrücklich
aufbrechen. Probe H4 bricht sie einmal auf und zeigt, dass das Urteil dann
kippt.

**2. Die Staging-Ebene ist nicht durch eine Flagge unsichtbar, sondern durch
ihren Ort.** `shared/ergebniskurven.finde_bots()` zählt Ordner unter
`strategies/`; `notifications/manual_close.SCHLIESSBARE_BOTS` speist den
Crash-Knopf. S-E1 liegt unter `research/` und steht in keiner der beiden
Listen. Teil D des Selbsttests **führt den Staging-Lauf wirklich aus** und
sieht danach nach, ob sich an Bot-Liste, Crash-Knopf, Datenbanken und
`results/` etwas geändert hat. Eine Flagge im Quelltext wäre eine Behauptung
gewesen.

**3. Kein zweiter Kalender.** Handelstage kommen aus der Kursreihe selbst.
Es gibt einen `dashboard/boersenkalender.py`, er wird hier absichtlich nicht
benutzt: er wäre eine zweite Quelle für dieselbe Zahl, und die sind in diesem
Projekt schon unbemerkt auseinandergelaufen (CLAUDE.md). Als Nebenwirkung
braucht das Modul keine Feiertagstabelle und keine Zeitzone — und läuft
deshalb auch dort, wo `US/Eastern` fehlt.

---

## 4. Die zwei Mutationsfallen — was sie diesmal gefangen haben

Die Aufgabenstellung nennt zwei wiederkehrende Fallen. **Beide haben in
dieser Sitzung wirklich zugeschlagen**, und zwar an meinem eigenen Test:

### 4.1 „Eine zweite Wache verdeckt das Fehlen der ersten"

Probe H7 sollte zeigen, dass entfallene Ereignisse gezählt werden. Sie
mutierte die Lückenlosigkeits-Prüfung — und blieb **grün**, obwohl die Wache
entfernt war. Grund: `handelstage.ereignisse` hat **drei** Streich-Wege, und
in der geprüften Lage schlug ein anderer an.

Jetzt wird der mutiert, der wirklich trägt, und **H7c** weist ausdrücklich
nach, dass der dritte in dieser Lage **nichts** beiträgt. Eine Wache, deren
Wegfall nichts ändert, wäre keine — und eine Probe, die das nicht merkt, erst
recht nicht.

### 4.2 „Eine Probe, deren Zustand der Test von Hand herstellt, bestätigt sich selbst"

Deshalb setzt `beispieldaten.py` **Kurse** und niemals Ereignisse,
Mittelwerte oder Urteile. Welcher Tag „−1" ist, was die Kosten abziehen, wie
der Bootstrap streut, welche Bedingung fällt — das rechnet die Auswertung
selbst aus. Alle elf Mutationsproben kopieren den Ordner, ändern **eine**
Zeile und starten `auswertung.py` als **eigenen Prozess** auf **denselben**
Daten. Beobachtet wird der Ablauf, nicht eine gesetzte Variable.

Dasselbe gilt für Teil B: die Feiertagsprobe sucht ausdrücklich Jahre, in
denen der 31.12. auf einen **Wochentag** fällt — an einem Samstag läge „−1"
ohnehin früher, und die Probe hätte sich selbst bestätigt, ohne die Regel zu
berühren.

---

## 5. N-Buchführung

| Register | Beitrag | Stand |
|---|---|---|
| **Versuchsregister** | **1 Eintrag** | bleibt vorerst unter „vorgemerkt" (Abschnitt 6a) |
| **DSR** | **kein Beitrag** | **N = 1** — es wird unter keinen Alternativen gewählt |
| **Sweep-Zellen** | in **keines** von beiden | Robustheit, nicht Auswahl |

**Warum V2 noch nicht gebucht ist:** der Datenlauf steht aus. *Das Register
ist ein Kassenbuch* — eine Zahlung, die noch nicht geflossen ist, wird nicht
gebucht, auch wenn alles andere fertig ist. Die vier Handgriffe für danach
stehen ausgeschrieben in `research/versuchsregister/REGISTER.md`,
Abschnitt 6a. Der Wächter meldet weiterhin `RC 0` (53 Angaben unverändert) —
absichtlich: ein Wächter, der aus Vorfreude rot leuchtet, wird bald nicht
mehr gelesen.

---

## 6. Prüfstand

| | |
|---|---|
| `research/turn_of_month/test_turn_of_month.py` | **110/110**, `WEG SAUBER`, RC 0 |
| `shared/ergebniskurven.py` | **9x AKTUELL** |
| `research/versuchsregister/versuchsregister.py --pruefen` | RC **0**, 53 Angaben unverändert |
| Gesamte Testsuite in der Cloud | **38 grün / 7 rot** |
| Basislauf auf unverändertem `main` | **37 grün / 7 rot** — *dieselben sieben* |

Die sieben roten sind vorbestehend und umgebungsbedingt: `US/Eastern` fehlt
(`broker/test_ibkr.py`), `fastapi` fehlt (`dashboard/test_dashboard.py`),
`scipy` fehlt (`research/hrp_portfolio/test_hrp_core.py`),
`dashboard/test_portfolio_sicht.py` und
`research/drawdown_reihenfolge/test_drawdown.py` scheitern an fehlenden
Bot-Abhängigkeiten, und zwei Tests
(`research/elliott_wave_params/test_params.py`,
`research/fib_score_stufen/test_stufen.py`) verlangen ein Argument und geben
ohne eines `1` samt Benutzungshinweis zurück.

> **Hinweis zur Umgebung:** `pip install yfinance` hat in dieser Sitzung
> `numpy` auf 2.4.6 und `pandas` auf 3.0.5 gehoben. Der Basislauf oben wurde
> **nach** dieser Hebung gemacht, damit der Vergleich trägt; die sieben roten
> Tests sind dieselben wie davor. Auf dem Mac ändert das nichts, dort ist die
> Umgebung unberührt.

---

## 7. Was **nicht** angefasst wurde

`live_params.py` · `forward_test.py` · `equity_simulation.py` ·
`multi_symbol_optimise.py` · `multi_symbol_walk_forward.py` ·
`shared/zuteilung.py` · `shared/messkette.py` · `shared/regimewache.py` ·
`results/*.csv` · `broker/` · Crontab · launchd-Vorlagen ·
`docs/VORREGISTRIERUNG_neuselektion.md` ·
`research/vorregistrierung/auswertung.py` (beide **gelesen**, nicht geändert)

Der geänderte Dateibaum umfasst genau zwei Wurzeln: `docs/` und `research/`.
Berührungspunkte mit TB-31 (`data/`) und TB-32 (`shared/`,
`notifications/`) gibt es keine — die Staging-Ebene liest `shared/kursdaten`
und `shared/ergebniskurven`, ändert aber nichts davon.

---

## 8. Offene Punkte

1. **Der Datenlauf steht aus.** Schritt 6 und 7 des Testdokuments, auf dem
   Mac. Erst danach gibt es ein Ergebnis der Strategie — und erst danach
   wandert V2 im Versuchsregister aus „vorgemerkt" heraus.
2. **Der Cronjob der Staging-Ebene ist nicht eingetragen.** Die Zeile
   (`15 23 * * 1-5`) steht als Vorschlag in
   `research/turn_of_month/README.md` und im Testdokument. Hängt wie die
   offenen Punkte 2, 10, 14 und 16 des Übergabeprotokolls am
   Festplattenvollzugriff fürs Terminal.
3. **A4 gehört ins Hauptregister.** Die Faltenzuordnung um den Jahreswechsel
   ist bei S-E1 aufgefallen, betrifft aber jede Strategie, deren Haltedauer
   über einen Monatswechsel reicht — also auch die vier Aktien-Bots in
   `S-B1`. Das ist ein Vorschlag, keine Änderung: `S-B1` wird von dieser
   Arbeit **nicht** angefasst.
4. **Die Staging-Ebene ist minimal**, wie verlangt: ein Instrument, eine
   Flagge, kein Anschluss an eine Ereignis-Datenbank. Was I19 darüber hinaus
   braucht, ist damit **nicht** entschieden.
