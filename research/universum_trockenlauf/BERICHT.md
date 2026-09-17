# Universum-Trockenlauf (TB-40)

**Abgeschlossene Untersuchung.** Sie fasst **keinen** Bot-Code an, ändert keine
Kursdatei und keinen Parameter. Das Register
(`docs/VORREGISTRIERUNG_neuselektion.md`) ist hier **nur gelesen** worden — die
Korrektur der Tatsachennotiz ist ausdrücklich **nicht** Teil dieser Arbeit.

Ergebnis zum Kopieren: **`docs/ERGEBNIS_TB-40_universum_trockenlauf.md`**
Testauftrag für den Mac: **`docs/TESTAUFTRAG_TB-40_universum_trockenlauf.md`**

---

## 1. Der Anlass

Beim Laden der Kursdaten meldet `strategies/rsi2_crypto/multi_symbol_optimise.py`
auf dem Mac (16.09.2026):

```
ENSOUSDT deckt nur 335 Tage ab (< 500 noetig), wird uebersprungen.
PUMPUSDT deckt nur 368 Tage ab (< 500 noetig), wird uebersprungen.
ZKCUSDT  deckt nur 364 Tage ab (< 500 noetig), wird uebersprungen.
UUSDT    deckt nur 244 Tage ab (< 500 noetig), wird uebersprungen.

Daten geladen: 20 Symbole
```

Im Register steht für denselben Bot in der Bestätigungsperiode **23**.

Der Grund: **zwei Implementierungen beantworten dieselbe Frage.**
`research/faltenplan_neun/faltenplan_neun.py` fragt „liegen Kursdaten vor?"
(Registertext 3a, Lesart A). Der Loader des Bots fragt „reicht die Historie?"
(`MIN_HISTORY_DAYS`). Sie sind auseinandergelaufen.

Registertext 3b (Beratungsantwort vom 15.09.2026) entscheidet, welche gilt:

> Ein Symbol gehört zu einer Selektionsfalte, wenn **der Loader des Bots** es mit
> den registrierten Einstellungen an mindestens einem Handelstag der Falte
> handelbar macht. Die Symbolzahl je Falte wird durch einen **Trockenlauf des
> Laufcodes** (`--nur-universum`) erzeugt; ein anderes Werkzeug ist dafür nicht
> zulässig.

---

## 2. Das Werkzeug

```bash
python3 research/universum_trockenlauf/universum_trockenlauf.py --nur-universum
python3 research/universum_trockenlauf/universum_trockenlauf.py --stille-filter
python3 research/universum_trockenlauf/test_universum_trockenlauf.py
```

| Datei | Zweck |
|---|---|
| `universum_trockenlauf.py` | Der Trockenlauf und der Vergleich gegen das Register |
| `loaderlauf.py` | Der Kindprozess: führt **einen** Bot-Loader aus, isoliert |
| `test_universum_trockenlauf.py` | Selbsttest, 42 Prüfungen |

### 2.1 Wohin das Werkzeug gehört — die Entscheidung

Die Festlegung nennt `--nur-universum`, lässt aber offen, ob das ein Argument
eines vorhandenen Programms ist oder ein eigenes Werkzeug. Entschieden ist:
**eigenständig unter `research/`, aufgerufen mit `--nur-universum`.**

1. **Das Programm, an das die Option gehört hätte, gibt es noch nicht.** Der
   spätere Auswerter ist `research/vorregistrierung/auswertung.py` — und der ist
   **eingefroren** (Register 15.8 Nr. 3), rechnet nach Verfahren A und wird erst
   in TB-30b umgestellt. Eine Option an eine eingefrorene Datei zu hängen, wäre
   ein Verstoss gegen die Randbedingung dieser Aufgabe.
2. **Die Frage wird vor dem Lauf gebraucht, nicht während.** Die Symbolzahl je
   Falte ist eine Tatsachennotiz, die vor dem signierten Tag ins Register kommt.
   Sie muss ohne Raster, ohne Kennzahl und ohne Auswerter erzeugbar sein.
3. **Die Option bleibt trotzdem die registrierte.** Entsteht der Auswerter in
   TB-30b, ruft er dieses Werkzeug auf oder importiert `messe_bot()` — statt die
   Frage ein viertes Mal zu beantworten.

### 2.2 Der Befund zum Import — und wie er aufgelöst ist

Die Aufgabe verlangt zugleich **„der Laufcode entscheidet"** und **„Bot-Dateien
werden gelesen, nie importiert"**. Beides zusammen geht nicht:
`load_all_symbol_data()` ist eine Funktion in einem Modul und läuft nur, wenn das
Modul geladen wird. Wer sie nachbaut, hat die dritte Implementierung derselben
Frage — genau das, wogegen die Festlegung gerichtet ist.

**Gemeldet und aufgelöst:** der Import findet statt, aber in einem **eigenen
Prozess je Bot**. Damit kann keine der neun gleichnamigen Dateien eine andere in
`sys.modules` verdrängen — nicht weil jemand aufpasst, sondern weil jeder Prozess
seinen eigenen `sys.modules` hat. Das ist strenger als jede Namensvergabe im
selben Prozess und erzwungen, nicht versprochen.

### 2.3 Was am Laufcode verändert wurde — und was nicht

Genau zwei Eingriffe, beide an der **Eingabe**, keiner an der **Entscheidung**:

1. `pandas.read_csv` liefert die Kursdatei **bis zum Stichtag**. Das ist die
   Übersetzung von „je Falte, nicht nur heute". Die Schranke selbst, der
   Leerlauf-Test, die Streichung unvollständiger Kerzen und das
   Zehnjahresfenster laufen unverändert im Bot-Code.
2. `binance.client.Client.ping` ist stillgelegt (siehe Nebenbefund 5.1).

Zusätzlich läuft ein **Schreibschutz**: jeder Schreibversuch auf eine Datei
ausserhalb der Ergebnisdatei bricht den Lauf ab. `os.makedirs` wird nicht
abgebrochen, sondern folgenlos gemacht — `shared/strategy_paths.py` legt beim
Import `results/<bot>` und `logs/<bot>` an, und ein harter Abbruch dort liesse
den Loader gar nicht erst starten. Angelegt wird trotzdem nichts; der Selbsttest
prüft, dass danach kein `logs/` existiert.

### 2.4 Die zwei Lesarten von „je Falte"

Aufgabenbeschreibung und Registertext sagen nicht dasselbe, und das ändert
Zahlen:

* **H** — *„an mindestens einem Handelstag der Falte"* (Registertext 3b,
  wörtlich). Gemessen am letzten Zeitpunkt der Falte.
* **F** — *„die Schranke wird am Faltenbeginn geprüft"* (Aufgabenbeschreibung
  TB-40). Gemessen am ersten Zeitpunkt der Falte.

F ist strenger als H, und gemessen gilt überall F ⊆ H ⊆ A. Beide werden gemessen und nebeneinander ausgewiesen;
**welche eingetragen wird, ist eine Registerfrage** und wird hier nicht
entschieden.

Dass H am Faltenende genügt, ist keine Annahme: jede der neun Schranken
vergleicht eine **nicht fallende** Grösse mit einer Konstanten. Das Werkzeug
verlässt sich darauf nicht, sondern **prüft die Monotonie über alle Stichtage
nach** und meldet jede Verletzung. Gemessen: keine.

---

## 3. Das Ergebnis

Vollständig in `docs/ERGEBNIS_TB-40_universum_trockenlauf.md`. In Kürze:

* **Acht der neun eingetragenen Zahlenreihen sind falsch**, alle **zu hoch**.
  `elliott_wave` stimmt unter Lesart H exakt.
* **Es kommt nirgends ein Symbol hinzu** — in keiner Falte eines Bots. Der Loader
  ist überall strenger: F ⊆ H ⊆ A.
* **`MIN_HISTORY_DAYS` ist nicht je Bot gleich** — fünf Werte, und
  `elliott_wave` hat stattdessen `MIN_HISTORY_HOURS = 17520` und misst
  **Kerzenzahl** statt Zeitspanne.
* **Mindestgrenze 4b:** unter Lesart H unterschreitet **kein** Bot die drei
  Falten. Unter Lesart F fällt `elliott_wave` auf **2 von 3** — seine erste Falte
  hat null Symbole. Dann griffe Regel 4c („unterbestimmt").
* **Die Tatsachennotiz „Symbole ohne Faltenevidenz" ist ebenfalls betroffen** und
  zerfällt von zwei Listen (je Markt) in Listen **je Bot**.

---

## 4. Die stillen Filter — gemessen, nicht gelesen

`--stille-filter` hält jedem Loader dieselben sieben Fälle hin und beobachtet,
was er damit macht. Die Ausgabe des Laufs wird mitgeschrieben; **„STILL raus"**
heisst: aussortiert, ohne dass der Loader das Symbol überhaupt nennt.

Die tragenden Befunde:

* **Die Grenze ist einschliesslich** — exakt `MIN_HISTORY_DAYS` Tage bzw. exakt
  `MIN_HISTORY_HOURS` Kerzen werden geladen, eine Einheit weniger nicht.
* **Drei Bots melden gar nichts**: `rsi2_mean_reversion`, `turtle_soup_stocks`,
  `volatility_breakout` schreiben bei zu kurzer Historie und bei fehlender
  Kursdatei keine Zeile. Der auslösende Befund war nur deshalb sichtbar, weil
  `rsi2_crypto` es meldet.
* **Der Fall „gleiche Zeitspanne, jede zehnte Kerze"** trennt die beiden
  Schrankenarten am Verhalten: `elliott_wave` wirft ihn heraus, die übrigen acht
  laden ihn. Kein Quelltext nötig.

---

## 5. Nebenbefunde

### 5.1 Der Import von `elliott_wave` braucht Netz

`strategies/elliott_wave/multi_symbol_optimise.py` holt `INTERVAL` aus
`shared/fetch_multi_data.py`. Diese Datei legt auf Modulebene ein
`client = Client()` an (`fetch_multi_data.py:46`), und `python-binance` pingt im
Konstruktor `api.binance.com`. In der Cloud scheitert das mit 403; auf dem Mac
kostet es bei **jedem** Import eine Netzrunde — für eine Konstante.

Der Trockenlauf legt den Ping still. **Kein Handlungsbedarf für TB-40**, aber ein
Kandidat für die nächste Aufräumrunde: `INTERVAL` liesse sich aus einer Datei
ohne Client lesen.

### 5.2 Die Klammer hinter der Universumsgrösse stimmt rechnerisch nicht

Registerabschnitt 15.5 schreibt für `config/top25_symbols.txt`
„24 (26 Zeilen abzüglich `XAUTUSDT`, `PAXGUSDT`)". Die Datei mit dem
**eingetragenen Hash** `3afc95a4…` hat **25 Zeilen**, und `PAXGUSDT` steht nicht
darin; `shared/symbols_config.py` streicht nur `XAUTUSDT`. **Das Ergebnis 24 ist
richtig**, der Rechenweg in der Klammer nicht. Der Hash wurde geprüft und ist
identisch — es ist dieselbe Datei.

---

## 6. Der Selbsttest

`python3 research/universum_trockenlauf/test_universum_trockenlauf.py` →
**42/42**.

| Teil | Was er zeigt |
|---|---|
| A | der auslösende Befund wird reproduziert: 20 von 24, namentlich dieselben vier |
| B | Datenstand-Hash vor und nach dem Lauf identisch; der Schreibschutz war nachweislich aktiv |
| C | wiederholbar — Symbol für Symbol, nicht nur gleiche Anzahl |
| D | ein verkürztes Symbol fällt heraus; die Grenze ist einschliesslich — an **zwei** Bots mit verschiedener Schrankenart |
| E | eine veränderte Registerzahl wird als Abweichung gemeldet, die Messung bleibt stehen |
| F | Mutationsprobe: Stichtag wirkungslos → jede Falte misst den heutigen Stand |
| G | Mutationsprobe: der Schreibschutz **allein** bricht ab |
| H | Mutationsprobe: ohne ihn läuft derselbe Defekt klaglos durch, und der Datenstand-Hash **allein** findet ihn |
| I | Monotonie über alle Stichtage |

**Zu den beiden wiederkehrenden Fallen.** Keine Probe biegt eine Variable im
laufenden Prozess um und fragt dieselbe Variable ab. Jede kopiert das Werkzeug in
ein Wegwerf-Verzeichnis, ändert dort **eine** Zeile und startet es als eigenen
Prozess — beobachtet wird der **Ablauf**. Und weil eine zweite Wache das Fehlen
der ersten verdecken kann, sind die beiden Wachen gegen dasselbe Risiko (G und H)
**einzeln** geprüft: erst der Schreibschutz ohne Hash, dann der Hash ohne
Schreibschutz. Beide greifen für sich.

---

## 7. Was diese Untersuchung nicht tut

* **Kein Registereintrag.** `docs/VORREGISTRIERUNG_neuselektion.md` ist
  unberührt; der Nachtrag erfolgt in einem Zug mit den übrigen offenen
  Registertexten.
* **Keine Entscheidung zwischen H und F.** Das ist eine Registerfrage.
* **Kein Selektionslauf, kein Raster, keine Parameterübernahme.**
* **Keine Kursdatei angefasst.** Datenstand unverändert `d9449faf51bffaaa…`,
  223 Dateien — am Verhalten nachgewiesen.
* **`research/faltenplan_neun/` unberührt** — es ist der Vergleichsgegenstand und
  wird nur aufgerufen.

---

## In einfacher Sprache

**Was wir wissen wollten.** Ob die im Vorab-Dokument („Register") notierten
Zahlen stimmen — nämlich, wie viele Handelswerte in jedem Prüfzeitraum
mitgerechnet werden können.

**Was herauskam.** Acht von neun Zahlenreihen sind zu hoch. Das Programm, das
später wirklich rechnet, nimmt weniger Werte als gedacht. Nirgends kommt ein Wert
hinzu, es fallen nur welche weg.

**Warum das so ist.** Zwei Programme beantworteten dieselbe Frage
unterschiedlich: Das eine fragt „gibt es Kursdaten?", das andere „gibt es genug
Kursdaten?". Ab jetzt antwortet nur noch das Programm, das später auch rechnet.

**Was das für dich heisst.** Die korrigierten Zahlen liegen fertig zum Kopieren
bereit; eingetragen werden sie später, gemeinsam mit den anderen offenen Punkten.
Eine Entscheidung bleibt bei dir: Zählt ein Wert zu einem Jahr, wenn er
*irgendwann* in diesem Jahr handelbar war, oder erst, wenn er es schon am
1. Januar war? Beide Zahlenreihen liegen vor. Die Wahl entscheidet, ob ein
bestimmter Bot (`elliott_wave`) neu eingestellt werden darf oder nicht.

---

*TB-40, 16.09.2026.*

---

## Nachtrag TB-43 (16.09.2026) — das Werkzeug wurde repariert

Die Befunde oben bleiben, wie sie sind. Zwei Dinge am **Werkzeug** haben sich
seither geändert; wer es erneut laufen lässt, sieht deshalb ein anderes Bild als
dieser Bericht beschreibt:

1. **Verglichen wird jetzt gegen Registerabschnitt 16.1.1**, nicht mehr gegen
   die erste Tabelle mit passender Kopfzeile. Seit dem Registernachtrag TB-41
   wäre das die historische, als „ERSETZT" gekennzeichnete Fassung in 15.5
   gewesen — ein erneuter Lauf hätte wieder acht Abweichungen gemeldet, obwohl
   das Register stimmt. Der benutzte Abschnitt steht jetzt in der Ausgabe;
   `--register-abschnitt 15.5` stellt den hier dokumentierten Stand wieder her.
2. **Der Schreibschutz in `loaderlauf.py` kannte vier Aufrufwege nicht**
   (`io.open`, `pathlib.Path.open`, `Path.write_text`, `os.open`) und brach
   ausserdem bei `open(pfad, mode="rb")` mit einem `TypeError` ab. Beides ist
   behoben. Für die Messungen dieses Berichts ist das folgenlos — geschrieben
   wurde nachweislich nichts —, aber der Schutz war dünner, als hier steht.

Einzelheiten: `docs/ERGEBNIS_TB-43_blinde_wachen.md`.

---

## Nachtrag TB-44 (16.09.2026) — der Schreibschutz war versionsabhängig

Der Nachtrag TB-43 oben sagt, der Schreibschutz kenne jetzt alle Aufrufwege.
Das stimmt — **auf Python 3.11 und neuer.** Auf den Fassungen davor stimmte es
in beide Richtungen nicht, und das ist gemessen worden:

| Fassung | `pathlib` **vor** der Wache | `pathlib` **nach** der Wache |
|---|---|---|
| **3.9** | `Path.touch()` legte die Datei **wirklich** an, `Path.mkdir()` das Verzeichnis **wirklich** | jeder Zugriff brach ab, auch ein **lesender** |
| **3.10** | `Path.open("w")` und `Path.write_text()` **schrieben wirklich** | jeder Zugriff brach ab, auch ein **lesender** |
| **3.11+** | in Ordnung | in Ordnung |

Die Ursache liegt nicht in `pathlib`, sondern im Bindungsverhalten: `os.open`
und `io.open` sind C-Funktionen und damit **keine Deskriptoren**; die Wache war
eine Python-Funktion und damit einer. Steht sie im Rumpf einer Klasse — und
genau das tut `pathlib._NormalAccessor` beim Import —, wird daraus eine
gebundene Methode, und die Argumente verrutschen.

**Für die Messungen dieses Berichts ist das folgenlos** — sie sind in der Cloud
auf Python 3.11 entstanden, der Datenstand-Hash ist unverändert, und
geschrieben wurde nachweislich nichts. Aber der Schutz hing an der
Python-Fassung, und das stand nirgends.

Behoben durch zwei Wachen, von denen keine `pathlib` kennt: `_Wache` (die
Wache ist eine aufrufbare Instanz statt einer Funktion, bindet sich also wie
das C-Original) und `_bindungen_nachziehen` (Kopien, die vor der Wache gebunden
wurden, werden über Identität gesucht und ersetzt). Geprüft von **Teil L** und
**Teil M** des Selbsttests, unter jeder Python-Fassung, die auf dem Rechner
liegt.

> ⚠️ **Teil K sieht diesen Fall nicht** — dort ist `pathlib` schon geladen,
> bevor die Wache angeht. Auf dem TB-43-Stand blieb Teil K grün, während Teil L
> 118 von 251 Prüfungen rot meldete.

Einzelheiten: `docs/ERGEBNIS_TB-44_wache_beide_pythons.md`.
