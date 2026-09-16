# Übergabe TB-43 — Blinde Wachen

**Zweig:** `claude/new-session-lwi4bi` · **Basis:** `4b0852e` (TB-41, PR #114, geprüft)
**Stand:** 16.09.2026

---

## 1. Welcher Test findet welchen Fehler auf dem unveränderten Stand?

Das ist die erste der drei verlangten Angaben — jeder Fehler wurde **zuerst
reproduziert**, dann behoben.

### Fehler 1 — `loaderlauf.py`

`test_universum_trockenlauf.py`, **Teil K**. Auf `origin/main`:

```
FEHL K2: open(pfad, mode="rb") … TypeError: argument for open() given by name ('mode') and position (2)
FEHL K3: und beide liefern dasselbe Ergebnis   False
FEHL K4 open(pfad, mode="w")   wird abgefangen  TypeError: …
FEHL K4 open(file=…, mode="w") wird abgefangen  TypeError: …
FEHL K4 io.open(pfad, "w")     wird abgefangen  durchgelassen
FEHL K4 pathlib.Path(pfad).open("w")            durchgelassen
FEHL K4 Path(pfad).write_text(…)                durchgelassen
FEHL K4 os.open(pfad, O_WRONLY|O_CREAT)         durchgelassen
FEHL K6: keine verbotene Datei entstanden  ['verboten.txt4','…5','…6','…7']
```

`K6` ist der härteste Beleg: **vier Dateien sind wirklich entstanden.** Geprüft
wird am Dateibestand, nicht an der ausgebliebenen Ausnahme.

Die Prüfung greift den Aufrufweg **direkt** an, nicht über `python-binance` —
sonst fände sie den Fehler nur auf einem Rechner.

### Fehler 2 — `pruefe_register.py`

`test_registernachtrag_tb41.py`, **Teil K**. Auf `origin/main`:

```
ok    K0: der Zweig ist wirklich gemergt
ok    K3: der Vergleich gegen den gemergten Zweig ist wirklich leer
FEHL  K4: und genau das wird als BEFUND gemeldet, nicht als Erfolg  []
FEHL  K5: der Rueckgabewert sagt dasselbe - 1, nicht 0   rc=0
FEHL  K6: der Bericht sagt, wogegen verglichen wurde     None
FEHL  K7: es meldet genau die Wache null_entfernte_zeilen []
```

**K0–K3 bestehen auf beiden Ständen** — sie stellen fest, dass der Zweig
wirklich gemergt und der Diff wirklich leer ist. Ohne sie könnte K4 auch aus
einem ganz anderen Grund rot sein. Die Probe stellt ihren Zustand nicht von Hand
her, sondern legt ein echtes git-Repo an, zweigt ab, ändert, merged und
**beobachtet den Ablauf** eines eigenen Prozesses.

### Fehler 3 — `universum_trockenlauf.py`

`test_universum_trockenlauf.py`, **Teil J**, dazu **A4, E0, E2**. Auf `origin/main`:

```
FEHL Teil J stuerzt ab: AttributeError: module 'universum_trockenlauf' has no attribute 'TABELLE_GUELTIG'
FEHL A4: … Bestaetigungsperiode ist 20 …   23
FEHL E0: … eingetragene Reihe 6/9/10/13/13/17/18 …   {'falten': [6,9,13,13,13,17,18], …}
FEHL E2: eine veraenderte eingetragene Zahl aendert die gemeldete Differenz   0 -> 0
```

`E2` ist aufschlussreich: die Mutation an der 15.5-Zeile bleibt **wirkungslos**,
sobald 16.1.1 gelesen wird — der Beleg, dass die Tabelle wirklich gewechselt hat.

**Gesamt: 13 von 70 Prüfungen scheitern auf `origin/main`, 0 auf dem neuen Stand.**

---

## 2. Erfasst der Schreibschutz nach der Reparatur noch alle Aufrufwege?

**Ja — und vier mehr als vorher.**

Die Reparatur selbst ist klein: `wach_open` **liest** Datei und Modus nur noch
heraus (gleich ob positional oder benannt) und reicht den Aufruf dann
**unverändert** durch. Damit kann nichts mehr doppelt ankommen.

Der eigentliche Fund liegt daneben. Der Schutz ersetzte nur `builtins.open`:

* `builtins.open is io.open` ist **wahr** — aber es sind zwei **Namen** für
  dasselbe Objekt. Den einen zu ersetzen lässt den anderen unberührt.
* `pathlib.Path.open` ruft `io.open` auf, nicht `builtins.open`. Damit waren
  auch `Path.write_text` und `Path.write_bytes` offen.
* `os.open` liegt unter beiden und war nie bewacht.

Alle sieben Wege sind jetzt zu, geprüft am Dateibestand. Zwei Dinge sind
absichtlich **nicht** verboten:

* **Zeichengeräte** (`/dev/null`) — sie ändern nichts auf der Platte. Ohne diese
  Ausnahme bricht der echte Trockenlauf ab (`python-binance` öffnet `/dev/null`
  lesend-schreibend). Das kam erst beim Durchlauf heraus und ist am Verhalten
  belegt, nicht angenommen.
* **Dateideskriptoren** — sie bleiben „nicht beurteilbar, also erlaubt". Das ist
  jetzt *vertretbar*, weil `os.open` bewacht wird: ein Schreib-Deskriptor kann
  gar nicht mehr entstehen, ohne vorher an der Wache vorbeizumüssen.

Ein erlaubter Schreibvorgang geht weiter durch (`K5`) — der Schutz ist kein
Totalverbot geworden.

---

## 3. Welche weiteren Werkzeuge vergleichen gegen `origin/main` oder 15.5?

### Gegen `origin/main` — drei, keine davon geändert

**`shared/test_kursdaten.py:438` — der nächste Kandidat, und der dringendste.**
Anders als vermutet ist der *leere Diff* dort nicht das Problem: die Prüfung
fragt „ist `forward_test.py` unverändert?", und leer heisst dort zu Recht „ja".
Das Problem ist eine Stufe davor: **der Rückgabewert von git wird nicht
geprüft.** Nachgemessen mit einer kaputten Referenz:

```
ref=origin/main        rc=0    stdout-Zeilen=5  -> BESTANDEN
ref=origin/gibtsnicht  rc=128  stdout-Zeilen=0  -> BESTANDEN
```

Scheitert der Aufruf — `origin/main` nicht geholt, flacher Klon, frischer
CI-Checkout —, meldet die Wache Erfolg. Schlimmer noch: die Schleife über
`live_params.py` läuft dann **null Mal**, es entstehen also gar keine Prüfungen,
und nichts sagt, dass sie fehlen. Dazu der bekannte **T38.9**: der
Zwei-Punkt-Vergleich wird bei jeder legitimen Änderung rot. **`shared/` ist in
dieser Aufgabe unberührt — berichtet, nicht geändert.**

**`dashboard/test_portfolio_sicht.py:217`** behandelt einen gescheiterten
git-Aufruf **ausdrücklich** als Erfolg (`lauf.returncode != 0 or not
lauf.stdout.strip()`). Derselbe blinde Fleck, nur bewusst hingeschrieben.
Ebenfalls unberührt.

**`research/fib_score_stufen/test_stufen.py:244`** macht es **richtig**:
Drei-Punkt-Form `origin/main...HEAD`, also gegen die Merge-Basis. Der Kommentar
dort hält genau die TB-34-Auflösung fest. Nur der Rückgabewert bleibt ungeprüft.

### Gegen 15.5 — eine, nicht geändert

**`research/faltenplan_neun/test_faltenplan_neun.py:180`** verankert auf
`**Die Symbolzahl je Falte** (Tatsachennotiz zu 3b)`. Diese Zeichenkette kommt im
Register **genau einmal** vor — in 15.5. Der Test ist heute **grün (145/145)**
und sachlich im Recht: er prüft **Lesart A** gegen die **Lesart-A-Tabelle**, und
das ist 15.5. Aber er liest eine als „ERSETZT" gekennzeichnete Tabelle und sagt
nicht, welche — dieselbe Form wie Fehler 3. `research/faltenplan_neun/` ist
unberührt; zu klären, wenn der Auswerter kommt.

Alle übrigen 15.5-Nennungen sind Prosa in abgeschlossenen Berichten und
beschreiben den historischen Stand korrekt. Die Nennungen in
`pruefe_register.py:73–79` sind die „ERSETZT"-Marker und gehören dorthin.

---

## 4. Die Wegentscheidung bei Fehler 2

Gewählt: **„leeren Vergleich melden"** — als einziger Weg, der den Fehler
schliesst.

`git merge-base` wurde **zusätzlich** übernommen, aber ausdrücklich **nicht** als
Lösung dieses Fehlers, denn es löst ihn nicht. Nachgemessen:

```
HEAD 4b0852e   origin/main 4b0852e   merge-base 4b0852e   -> Diff leer
merge-base(1bc2d57, origin/main) = 1bc2d57               -> Diff leer
```

Ist der Zweig gemergt, ist die Merge-Basis der eigene Commit. Was `merge-base`
löst, ist die *andere* Fehlerart — die aus TB-34, bei der fremde Commits in den
Diff geraten, sobald `main` weitergelaufen ist. Beides ist jetzt getrennt
behandelt und als Prüfung `K8` festgehalten.

**„Ausdrückliche Basis verlangen" wurde verworfen:** Wer eine bereits gemergte
Basis ausdrücklich angibt, bekommt denselben leeren Diff und dieselbe stille
Grün-Meldung. Der Weg verschiebt die Last auf den Aufrufer, statt die Wache zu
reparieren — und bricht dabei jeden bestehenden Aufruf.

**Der Unterschied, auf den es ankommt:** Bei `daten_unberuehrt` ist ein leeres
Ergebnis der **Nachweis** („nichts verändert" ist der Sollzustand). Bei
`null_entfernte_zeilen` ist es das **Fehlen** eines Nachweises. Deshalb wurde nur
die zweite Prüfung verschärft — ein pauschales „leer ist immer schlecht" hätte
die erste kaputtgemacht.

---

## 5. Zahlen

| Prüfung | alt | neu |
|---|---|---|
| `test_universum_trockenlauf.py` | 43 / **13 gescheitert** | **70/70** |
| `test_registernachtrag_tb41.py` | 46 / **4 gescheitert** | **50/50** |
| Trockenlauf gegen **16.1.1** | — | **0 Abweichungen von 9** |
| Trockenlauf gegen **15.5** | — | **8 Abweichungen von 9** |
| `pruefe_register.py`, alle neun | — | **KEIN BEFUND**, `beleg: trockenlauf` |
| Datenstand `data/` | `d9449faf51bffaaa…` / 223 | **identisch** |

Nachbarsuiten unverändert grün: `research/vorregistrierung` 150/150,
`research/faltenplan_neun` 145/145, `research/krypto_historie` 38/38.

Die gemessenen Symbolzahlen sind in beiden Tabellenläufen **identisch** — bewegt
hat sich nur die Vergleichstabelle. Damit ist belegt, dass das Werkzeug die
Tabelle wechselt und nicht bloss schweigt.

---

## 6. Was der Mac noch beisteuern muss

`docs/TESTAUFTRAG_TB-43_blinde_wachen.md`, autonom ausführbar.

**Fehler 1 ist in der Cloud nicht über die echte Kette nachweisbar.** Die dort
installierte `dateparser`-Fassung 1.4.3 nimmt den Aufrufweg `open(pfad,
mode="rb")` nicht mehr; auf dem Mac liegt eine ältere. Die neuen Prüfungen
greifen den Weg deshalb **direkt** an — das läuft überall. Was nur der Mac
beweisen kann, ist, dass damit auch die **volle Kette** wieder durchläuft:
`test_universum_trockenlauf.py` soll dort von **10/20** auf vollständig grün
gehen. Der Auftrag verlangt genau dafür einen Lauf gegen den alten Stand
(Schritt 2a) — **besteht der, ist der Rest wertlos und das ist zu melden.**

---

## 7. Randbedingungen — eingehalten

* `docs/VORREGISTRIERUNG_neuselektion.md` und `…_S-B1_etf_trendfolge.md`
  **unberührt** (git-Status leer, nur gelesen).
* **Keine Kursdatei verändert** — `d9449faf51bffaaa…`, 223 Dateien, vor und nach
  der Aufgabe identisch, **als Test nachgewiesen**.
* `research/vorregistrierung/auswertung.py` eingefroren, nicht angefasst.
* Kein `live_params.py`, `forward_test.py`, `equity_simulation.py`,
  `multi_symbol_optimise.py`, `multi_symbol_walk_forward.py`.
* `research/faltenplan_neun/`, `research/etf_trendfolge/` unberührt.
* Nichts unter `broker/`, `shared/` oder `dashboard/`; keine Crontab, kein
  `results/*.csv`.
* Berührt wurden **ausschliesslich** `research/universum_trockenlauf/` und
  `research/registernachtrag_tb41/` — plus die drei neuen Dokumente unter
  `docs/`. Keine Überschneidung mit TB-42.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Drei kleine Prüfprogramme im Projekt sollten aufpassen, dass beim Arbeiten nichts
kaputtgeht. Der Verdacht war, dass sie stillschweigend aufgehört hatten zu
prüfen und trotzdem „alles in Ordnung" meldeten. Wir wollten wissen, ob das
stimmt, und es abstellen.

**Was herauskam.**
Der Verdacht stimmte bei allen dreien. Einer war sogar schlimmer als gemeldet:
Das Programm, das verhindern soll, dass bei einer Messung versehentlich Dateien
verändert werden, kannte nur drei von sieben Wegen, auf denen man in eine Datei
schreiben kann. Auf den anderen vier sind im Test wirklich Dateien entstanden.
Alle drei sind repariert. Drei weitere Programme haben denselben Schwachpunkt —
die durfte diese Aufgabe laut Auftrag nicht anfassen; sie stehen im Bericht.

**Warum das so ist.**
Alle drei Fehler haben dieselbe Form: etwas hört auf zu funktionieren, aber
niemand sagt es. Ein Rauchmelder mit leerer Batterie piept nicht — und Schweigen
sieht genauso aus wie „kein Feuer". Damit ein Test nicht selbst zu so einem
stummen Melder wird, haben wir jeden neuen Test **zweimal** laufen lassen:
einmal gegen den alten, kaputten Stand (dort muss er Alarm schlagen) und einmal
gegen den reparierten (dort muss er ruhig bleiben). Erst beides zusammen zeigt,
dass er wirklich hinsieht. 13 Prüfungen schlagen auf dem alten Stand an.

**Was das für dich heisst.**
Es wurde kein Handelsparameter verändert, keine Kursdatei angefasst und keine
Order ausgelöst — nur die Prüfprogramme selbst. Ein Schritt fehlt noch, und den
kann nur Ihr Mac machen: Einer der drei Fehler lässt sich auf dem Server nicht
in voller Länge vorführen, weil ein dafür nötiges Zusatzprogramm dort gar nicht
startet. Dafür liegt eine Schritt-für-Schritt-Anleitung bereit, die am Ende eine
ZIP-Datei in `~/Downloads` ablegt.
Der Zeitpunkt ist der eigentliche Punkt: Als Nächstes stehen die beiden grössten
Umbauten des Projekts an. Die hätte man sonst mit Rauchmeldern ohne Batterie
begonnen.
