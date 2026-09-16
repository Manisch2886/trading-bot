# Ergebnis TB-43 — Blinde Wachen

**Stand:** 16.09.2026 · **Zweig:** `claude/new-session-lwi4bi` · **Basis:** `4b0852e` (TB-41, PR #114)

> **Ein Werkzeug, das nicht mehr misst, sagt es.**

Drei Prüfwerkzeuge hatten aufgehört zu prüfen, ohne es zu melden. Alle drei sind
repariert; für jeden Fehler gibt es eine Prüfung, die auf dem **unveränderten**
Stand durchfällt.

---

## Die drei Antworten zuerst

### 1. Welcher Test findet welchen Fehler auf dem unveränderten Stand?

| Fehler | Test | Auf `origin/main` |
|---|---|---|
| **1** Schreibschutz | `test_universum_trockenlauf.py`, Teil **K** | **K2, K3, K4 (5 Zeilen), K6 fallen durch** — und vier verbotene Dateien entstehen wirklich |
| **2** leerer Vergleich | `test_registernachtrag_tb41.py`, Teil **K** | **K4, K5, K6, K7 fallen durch** (K0–K3, K8 bestehen: die Lage ist echt) |
| **3** falsche Tabelle | `test_universum_trockenlauf.py`, Teil **J** + A4/E0/E2 | **Teil J bricht ab** (`TABELLE_GUELTIG` gibt es dort nicht), **A4, E0, E2 fallen durch** |

Zusammen: **13 der 70 Prüfungen** scheitern auf dem alten Stand, **0 auf dem neuen.**

### 2. Erfasst der Schreibschutz nach der Reparatur noch alle Aufrufwege?

**Ja — und er erfasst jetzt vier mehr als vorher.** Beim Nachmessen kamen Wege
ans Licht, die er gar nicht kannte:

| Aufrufweg | vorher | nachher |
|---|---|---|
| `open(pfad, "w")` | abgefangen | abgefangen |
| `open(pfad, mode="w")` | **TypeError** | abgefangen |
| `open(file=…, mode="w")` | **TypeError** | abgefangen |
| `io.open(pfad, "w")` | **Datei entstand** | abgefangen |
| `pathlib.Path(pfad).open("w")` | **Datei entstand** | abgefangen |
| `Path(pfad).write_text(…)` | **Datei entstand** | abgefangen |
| `os.open(pfad, O_WRONLY\|O_CREAT)` | **Datei entstand** | abgefangen |

Der Grund für die vier Löcher: `builtins.open is io.open` ist zwar wahr, aber es
sind **zwei Namen für dasselbe Objekt**. Den einen zu ersetzen lässt den anderen
unberührt — und `pathlib` geht über `io.open`. `os.open` lag darunter und war
nie bewacht.

**Ausgenommen sind Zeichengeräte** (`/dev/null`): darauf zu schreiben verändert
nichts, was der Datenstand-Hash je sehen könnte. Ohne diese Ausnahme bricht der
echte Trockenlauf ab — `python-binance` öffnet `/dev/null` lesend-schreibend.
Das ist am Ablauf geprüft, nicht angenommen.

### 3. Welche weiteren Werkzeuge vergleichen gegen `origin/main` oder gegen 15.5?

**Gegen `origin/main`** — drei weitere Fundstellen, **keine davon geändert**
(`shared/` und `dashboard/` sind in dieser Aufgabe unberührt):

| Datei | Befund | Dringlichkeit |
|---|---|---|
| `shared/test_kursdaten.py:438` | **Dieselbe Fehlerfamilie, andere Ursache.** Der leere Diff ist hier *richtig* (es ist eine Negativ-Prüfung: „nichts verändert"). Aber der **Rückgabewert von git wird nicht geprüft**. Schlägt der Aufruf fehl (`origin/main` nicht geholt, flacher Klon), ist `stdout` leer, und dann melden beide Prüfungen `BESTANDEN` — **und die `live_params.py`-Schleife erzeugt null Prüfungen, ohne dass das irgendwo auffällt.** Nachgemessen mit kaputter Referenz: `rc=128`, trotzdem „bestanden". Zusätzlich der bekannte T38.9: der Zwei-Punkt-Vergleich wird bei jeder legitimen Änderung rot. | **hoch** |
| `dashboard/test_portfolio_sicht.py:217` | Behandelt einen **gescheiterten git-Aufruf ausdrücklich als Erfolg**: `lauf.returncode != 0 or not lauf.stdout.strip()`. Das ist derselbe blinde Fleck, nur bewusst hingeschrieben. | mittel |
| `research/fib_score_stufen/test_stufen.py:244` | **Macht es richtig** — Drei-Punkt-Form `origin/main...HEAD`, also gegen die Merge-Basis. Der Kommentar dort dokumentiert genau die TB-34-Auflösung. Nur der Rückgabewert bleibt auch hier ungeprüft. | gering |

**Gegen Abschnitt 15.5** — eine weitere Fundstelle, **nicht geändert**
(`research/faltenplan_neun/` ist unberührt):

| Datei | Befund |
|---|---|
| `research/faltenplan_neun/test_faltenplan_neun.py:180` | Verankert auf `**Die Symbolzahl je Falte** (Tatsachennotiz zu 3b)` — diese Zeichenkette kommt im Register **genau einmal** vor, nämlich in **15.5**. Der Test ist heute **grün (145/145)**, und zwar zu Recht: er prüft **Lesart A** gegen die **Lesart-A-Tabelle**. Aber er liest eine als „ERSETZT" gekennzeichnete Tabelle und **sagt nicht, welche** — dieselbe Form wie Fehler 3. Zu klären, wenn der Auswerter kommt. |

Alle übrigen 15.5-Nennungen sind **Prosa in abgeschlossenen Berichten**
(`docs/ERGEBNIS_TB-36/40/41_*`, `docs/UEBERGABE_TB-36/40/41_*`,
`research/universum_trockenlauf/BERICHT.md`, `research/faltenplan_neun/BERICHT.md`)
und beschreiben den historischen Stand richtig. Die 15.5-Stellen in
`pruefe_register.py:73–79` sind die **„ERSETZT"-Marker** und sollen dort stehen.

---

## Was geändert wurde

| Datei | Änderung |
|---|---|
| `research/universum_trockenlauf/loaderlauf.py` | `wach_open` liest die Argumente nur noch und reicht den Aufruf **unverändert** weiter; `io.open` und `os.open` werden mitbewacht; Zeichengeräte ausgenommen |
| `research/universum_trockenlauf/universum_trockenlauf.py` | liest einen **benannten** Registerabschnitt (Standard **16.1.1**), versteht Blockzitat-Tabellen, nennt den Abschnitt in Ausgabe und Bericht, warnt gegen 15.5; neue Option `--register-abschnitt` |
| `research/registernachtrag_tb41/pruefe_register.py` | leerer Vergleich = **Befund**, Rückgabewert 1; Basis = `git merge-base`; Basis und ihre Herkunft stehen im Bericht; neue Option `--basis-zweig` |
| beide `test_*.py` | Teile **J** und **K** neu; ein abstürzender Teil wird als Fehlschlag gemeldet statt die übrigen zu verschlucken |

**Nicht angefasst:** beide `VORREGISTRIERUNG_*.md`, jede Kursdatei, `shared/`,
`broker/`, `dashboard/`, `research/faltenplan_neun/`, `research/etf_trendfolge/`,
`research/vorregistrierung/auswertung.py`, `live_params.py`, `forward_test.py`,
Crontab, `results/*.csv`.

---

## Die Wegentscheidung bei Fehler 2 — und warum

Zur Wahl standen drei Wege. Gewählt wurde **„leeren Vergleich melden"**, und
zwar als **einziger**, der den Fehler schliesst:

| Weg | Urteil |
|---|---|
| **Leeren Vergleich melden** | **gewählt.** Setzt genau an der Stelle an, an der die Messung ausfällt. Der leere Diff erzeugt jetzt Rückgabewert 1 und eine Meldung, die auch sagt, was zu tun ist. |
| **Die Basis selbst finden** (`git merge-base`) | **zusätzlich übernommen, aber nicht als Lösung dieses Fehlers.** Nachgemessen: bei einem gemergten Zweig ist `merge-base(HEAD, origin/main)` der eigene Commit — **der Diff bleibt leer**. Es löst die *andere* Fehlerart (TB-34: fremde Commits im Diff, wenn `main` weitergelaufen ist). Als Prüfung `K8` festgehalten. |
| **Ausdrückliche Basis verlangen** | **verworfen.** Schliesst den Fehler nicht: wer eine bereits gemergte Basis ausdrücklich angibt, bekommt denselben leeren Diff und dieselbe stille Grün-Meldung. Es verschiebt die Last auf den Aufrufer, statt die Wache zu reparieren — und bricht dabei jeden bestehenden Aufruf. |

**Der Unterschied, auf den es ankommt:** Bei `daten_unberuehrt` *ist* ein leeres
Ergebnis der Nachweis („nichts verändert" ist der Sollzustand). Bei
`null_entfernte_zeilen` ist es das **Fehlen** eines Nachweises — die Änderung,
die man begutachten wollte, steht gar nicht im Diff. Deshalb wurde nur die
zweite Prüfung verschärft.

---

## Gemessene Ergebnisse (Cloud)

| Prüfung | alter Stand | neuer Stand |
|---|---|---|
| `test_universum_trockenlauf.py` | 43 bestanden, **13 gescheitert** | **70/70** |
| `test_registernachtrag_tb41.py` | 46 bestanden, **4 gescheitert** | **50/50** |
| `pruefe_register.py` (alle neun, richtige Basis) | — | **KEIN BEFUND**, `Quelle beleg: trockenlauf` |
| Trockenlauf gegen **16.1.1** | — | **0 Abweichungen von 9** |
| Trockenlauf gegen **15.5** | — | **8 Abweichungen von 9** (nur `elliott_wave` stimmt) |
| Datenstand `data/` | `d9449faf51bffaaa…`, 223 | **identisch** |

Die gemessenen Symbolzahlen sind in beiden Läufen **Zeichen für Zeichen gleich** —
bewegt hat sich nur die Vergleichstabelle. Damit ist belegt, dass das Werkzeug
die Tabelle wirklich wechselt und nicht bloss schweigt.

> **Nebenbefund:** Da in der Cloud diesmal `pandas`, `python-binance` und
> `yfinance` installiert werden konnten, lief `pruefe_register.py` gegen eine
> **frische Messung** statt gegen das committete Dokument — und bestätigt die
> TB-41-Zahlen in 16.1.1 vollständig.

---

## Was offen bleibt

1. **`shared/test_kursdaten.py`** prüft den git-Rückgabewert nicht (siehe oben).
   `shared/` ist in dieser Aufgabe unberührt — **berichtet, nicht geändert.**
2. **`dashboard/test_portfolio_sicht.py`** wertet einen gescheiterten git-Aufruf
   als Erfolg. Ebenfalls unberührt.
3. **`research/faltenplan_neun/test_faltenplan_neun.py`** liest die ersetzte
   Tabelle 15.5, ohne es zu sagen. Heute sachlich richtig, aber stumm.
4. **Fehler 1 ist in der Cloud nicht über die echte Kette nachweisbar.** Die
   installierte `dateparser`-Fassung 1.4.3 nimmt den fraglichen Aufrufweg nicht
   mehr. Der Nachweis über die volle Kette steht im **Mac-Testauftrag**.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Dieses Projekt hat mehrere kleine Programme, deren einzige Aufgabe es ist,
aufzupassen — so etwas wie Rauchmelder. Bei dreien davon gab es den Verdacht,
dass sie nur noch so tun als ob: Sie meldeten „alles in Ordnung", obwohl sie in
Wirklichkeit gar nichts mehr geprüft hatten.

**Was herauskam.**
Der Verdacht stimmte, bei allen dreien. Und beim genauen Nachsehen war einer
sogar schlimmer als gedacht: Ein Programm sollte verhindern, dass bei einer
Messung versehentlich Dateien verändert werden — es kannte aber vier von sieben
Wegen gar nicht, auf denen man eine Datei beschreiben kann. Auf diesen vier
Wegen sind im Test tatsächlich Dateien entstanden. Alle drei sind jetzt
repariert, der Wächter kennt alle sieben Wege.

**Warum das so ist.**
Alle drei Fehler haben dieselbe Form: Etwas geht kaputt, aber niemand sagt es.
Ein Rauchmelder mit leerer Batterie piept nicht — er schweigt, und Schweigen
sieht genauso aus wie „kein Feuer". Beim ersten Programm scheiterte der Wächter
ausgerechnet an einem harmlosen *Lesevorgang*. Beim zweiten verglich ein
Programm die neue Fassung eines Dokuments mit der alten — aber sobald die
Änderung offiziell übernommen war, verglich es die neue Fassung mit sich selbst,
fand erwartungsgemäss keinen Unterschied und meldete Erfolg. Beim dritten gibt
es seit kurzem zwei Tabellen mit gleicher Überschrift; das Programm nahm
stillschweigend die alte, überholte.

**Was das für dich heisst.**
Es wurde **kein** Handelsparameter angefasst, **keine** Kursdatei verändert
(nachgewiesen: derselbe Prüfwert vorher und nachher) und **keine** Order
ausgelöst. Verändert wurden nur die drei Prüfprogramme selbst. Wichtig ist der
Zeitpunkt: Als Nächstes stehen die beiden grössten Umbauten des Projekts an, und
die hätte man sonst mit Rauchmeldern ohne Batterie begonnen.
Drei weitere Programme haben denselben Schwachpunkt — die durfte diese Aufgabe
laut Auftrag nicht anfassen, sie sind oben aufgelistet und warten auf eine
Freigabe.
