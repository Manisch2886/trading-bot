# Ergebnis TB-46 — Zwei Datenbestände: Erhebung, Werkzeug, Wache

**Stand 17.09.2026.** Vorgänger: TB-45 (gemergt `7ff3aa7`). Zweig
`claude/new-session-mmsrys`.
Untersuchung: `research/datenordner_schnitt/BERICHT.md`. Mac-Testauftrag:
`docs/TESTAUFTRAG_TB-46_datenordner.md`.

---

## Das Ergebnis in sechs Zeilen

1. **Gemessen sind 182 Module**, die den echten `data/`-Bestand erreichen — nicht
   101. Die 101 aus TB-34 ist **exakt reproduziert**; sie zählt eine engere Frage.
2. **Nur 29 dieser Module bauen den Pfad selbst**, und **7 davon sind die
   gemeinsamen Stellen**. 145 beziehen ihn mittelbar.
3. ⭐ **Keine der neun `forward_test.py`, keine `live_params.py` und keine
   `equity_simulation.py` baut einen Pfad auf `data/`.** Beide Entwürfe kommen
   ohne eine Änderung an ihnen aus.
4. **Die Hash-Berechnung ist nicht rekursiv.** Ein Snapshot *innerhalb* `data/`
   würde vom registrierten Hash nicht mitgezählt. Die Sorge der Aufgabenstellung
   trifft nicht ein — dafür eine andere (siehe 5).
5. **Empfohlen wird Entwurf B** (`data/` bleibt, `snapshots/<hash>/` daneben):
   **0 statt 29** Module auf der Live-Seite, und drei gemessene Ausfälle von
   Entwurf A entfallen. ⚠️ Das ist eine **Abweichung vom Registertext** — was
   erhalten bleibt, steht unten vollständig.
6. **`shared/snapshot.py` ist gebaut**, `shared/test_snapshot.py` bewacht es mit
   **69 von 69** Prüfungen auf vier Python-Fassungen. **Kein echter Snapshot
   gezogen, kein Byte unter `data/` angefasst.**

---

## 1. Der Datenstand — vorher und nachher

| | Hash | Dateien |
|---|---|---:|
| **vor** der Arbeit | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` | **223** |
| **nach** der Arbeit | `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84` | **223** |

Gemessen mit `research/vorregistrierung/herkunft.py::datenstand` — derselben
Funktion, die den registrierten Wert erzeugt hat. `git status --porcelain -- data`
ist leer. Unter `data/` ist nichts verändert, verschoben oder gelöscht worden.

---

## 2. Teil 1 — die Erhebung: **wie** erreichen die Module `data/`?

Gemessen über den Syntaxbaum, nicht mit Textsuche
(`research/datenordner_schnitt/erhebung.py`). ⚠️ Der Unterschied ist nicht
akademisch: **zwei der neun `forward_test.py` nennen `data/` in einer
Protokollzeile.** Eine Textsuche hätte gemeldet, der Umbau müsse die Bot-Dateien
anfassen, die er nicht anfassen darf.

### Die gemessene Zahl

| Zählung | Zahl |
|---|---:|
| Module mit mindestens einer Fundstelle | 185 |
| davon auf dem **echten** Bestand | 184 |
| ⚠️ davon **neu in TB-46** (`shared/snapshot.py`, `shared/test_snapshot.py`) | 2 |
| **= Bestand vor TB-46 — die Zahl, die der Umbau vorfindet** | **182** |
| davon nur ein nachgebautes `data/` unter einem Temp-Ordner | 1 |

⚠️ Die zwei Neuzugänge dieser Sitzung erreichen `data/` wirklich und werden
deshalb **nicht stillschweigend übergangen**; die Erhebung nennt beide Zahlen
selbst. Alle folgenden Zahlen sind die **ohne** sie.

⚠️ **Zur 101 aus TB-34:** sie ist mit dem TB-34-Skript unverändert
nachgemessen und kommt **genau** heraus (37 unmittelbar + 64 über
`load_all_symbol_data` = 101). Sie ist also **nicht veraltet** — sie zählt
eine engere Frage. TB-46 zählt zusätzlich die Wege über
`entscheidungskerze.lade()` (die neun Bots), `herkunft.datenstand()`,
`kursdaten.pruefe_ordner()` und `DATA_DIR`-Benutzungen ohne eigenes `read_csv`.
**Beide Zahlen sind richtig; sie beantworten verschiedene Fragen.**

### Die Antwort auf die Frage, die alles entscheidet

| | Module |
|---|---:|
| bauen den Pfad **selbst** aus einem Literal | **29** |
| beziehen ihn **nur mittelbar** | **145** |
| **nennen** `data/` nur, ohne Pfad zu bauen (git-Filter, Meldungen) | **8** |

**Es gibt nicht eine gemeinsame Stelle, sondern sieben:**

| Stelle | Zeile | Schreibweise |
|---|---:|---|
| `shared/paths.py` | 15 | `os.path.join(BASE_DIR, "data")` |
| `shared/strategy_paths.py` | 49 | `os.path.join(base_dir, "data")` |
| `shared/entscheidungskerze.py` | 257 | `os.path.join(BASE_DIR, "data")` |
| `shared/kursdaten.py` | 156 | `os.path.join(os.path.dirname(_SHARED), "data")` |
| `shared/abrufschutz.py` | 501 | `os.path.join(os.path.dirname(_SHARED_DIR), "data")` |
| `shared/zeitabdeckung.py` | 659 | `os.path.join(os.path.dirname(_SHARED), "data")` |
| `research/vorregistrierung/herkunft.py` | 98 | `os.path.join(BASE_DIR, "data")` |

Die übrigen 22 Selbstbauer sind 16 Untersuchungen unter `research/` und 6
Prüfwerkzeuge — **keine davon im Cron-Betrieb**.

### Summen je Schreibweise und je Rolle

| Schreibweise | Module |
|---|---:|
| Aufruf `load_all_symbol_data()` | 100 |
| `import load_all_symbol_data()` | 68 |
| Konstante `DATA_DIR` aus `shared/` | 44 |
| `os.path.join` + Literal | 34 |
| Nennung ohne Pfadbau | 13 |
| Aufruf `lade()` (die neun Bots) | 9 |
| Aufruf `datenstand()` | 7 |
| `import datenstand()` | 3 |
| Aufruf `pruefe_ordner()` | 3 |
| Konstante `STANDARD_DATENORDNER` | 1 |
| Umgebungsvariable | **0** |

| Rolle | Module | soll lesen aus |
|---|---:|---|
| **Selektion/Backtest** | **90** | dem **Snapshot** |
| Untersuchung (`research/`) | 48 | je nach Zweck |
| Betrieb (Bots, Cron, Dashboard, Telegram) | 25 | dem **Live-Bestand** |
| Prüfwerkzeug | 19 | beidem |

### Die Schreiber — 11, und einer ist ein Befund

Neun sind die Abrufskripte (dieselben neun wie in TB-34, Zeile für Zeile
bestätigt). Dazu:

* ⚠️ **`shared/paths.py:18` — `os.makedirs(DATA_DIR, exist_ok=True)` beim
  Import.** Kein `to_csv`, aber es schreibt: **jeder Import von `paths.py`
  legt `data/` wieder an, wenn es fehlt.** Das ist der stille Teil von
  Entwurf A (siehe 3).
* `shared/test_entscheidungskerze.py:697` schreibt in ein nachgebautes `data`
  unter einem Temp-Ordner — kein Zugriff auf den Bestand.

### Die Dateimuster

⚠️ Es ist **`AAPL_1d.csv`**, nicht `AAPL.csv`. Häufigste Muster:
`f"{symbol}_{INTERVAL}.csv"` (16×), `f"{symbol}_{intervall}.csv"` (8×),
`f"{symbol}_1d.csv"` (5×), `BTCUSDT_1h.csv` (7×), `AAPL_1d.csv` (6×).

---

## 3. Teil 2 — die beiden Entwürfe, gegeneinander gerechnet

| Frage | **Entwurf A** `data/live/` + `data/snapshots/<hash>/` | **Entwurf B** `data/` bleibt, `snapshots/<hash>/` daneben |
|---|---|---|
| Module mit eigenem Pfadbau, die umzustellen sind | **29**, davon **7** gemeinsame Stellen | **0** |
| Nennungen, die danach irreführend dastehen | **8** | **0** |
| ⚠️ **Müsste ein `forward_test.py` angefasst werden?** | **nein** | **nein** |
| Hash-Berechnung | Snapshot liegt **innerhalb** `data/` — wird **nicht** mitgezählt. Dafür: Voreinstellung zeigt auf einen Ordner ohne `.csv` | **unberührt** |
| `git pull` / Cron-Seite | **drei gemessene Ausfälle** (unten) | keine Umbenennung, kein Ausfall |
| Preis im Repo | gleich, und **viel kleiner als angenommen** | dito |
| Registertext 5a | **wörtlich erfüllt** | **Abweichung im Namen** |
| Selektionsseite zu verdrahten | **90** Module | **90** Module |

⚠️ **Die letzte Zeile ist die wichtigste:** der eigentliche Umbau — 90 Module der
Selektionsseite auf den Snapshot zu zeigen — kostet in **beiden** Entwürfen
dasselbe. Der Unterschied liegt ausschließlich auf der Live-Seite.

### 3.1 Die Hash-Berechnung — wie sie heute läuft

**An einer Stelle:** `research/vorregistrierung/herkunft.py::datenstand`.
SHA-256 über die `*.csv` **direkt** im Ordner, sortiert, je Datei **Name +
Größe + SHA-256 des Inhalts**.

> ⭐ **Zur Frage der Aufgabenstellung — „läuft die Hash-Berechnung rekursiv,
> zählt sie den Snapshot mit und der registrierte Wert ändert sich":
> Nein.** `os.listdir` + `endswith(".csv")` sieht keine Unterordner.
> **Gemessen**, nicht geschlossen: `shared/test_snapshot.py`, Probe 3j,
> vergleicht denselben Ordner mit und ohne Unterordner und erhält denselben
> Hash.

Zwei Folgen, die dafür **nicht** im Auftrag stehen:

1. ⚠️ **Die Voreinstellung ist der Fallstrick, nicht die Rekursion.**
   `datenstand()` zeigt ohne Argument auf `BASE_DIR/data`. Nach dem Umzug
   liegen dort **null** `.csv` — der Hash wird der der **leeren Menge**
   (`e3b0c442…`, 0 Dateien). Die Registerwache
   `research/etf_trendfolge/datenstand.py` meldet dann ABWEICHUNG, ohne dass
   eine Kursdatei sich geändert hat.
2. ⚠️ **Dass der Snapshot in `data/` heute harmlos ist, hat niemand
   zugesichert.** Es hängt an einer Eigenschaft der Berechnung. Wer sie eines
   Tages rekursiv macht — etwa für Unterordner je Zeitrahmen —, entwertet
   damit den registrierten Hash, ohne eine Kursdatei anzufassen.

> ⚠️ **Befund: das Verfahren steht doppelt im Repo.** Ein zeichengleiches
> Duplikat liegt in `research/registernachtrag_tb41/pruefe_register.py:319`.
> Heute liefern beide dasselbe; wer eines ändert, merkt es nicht. Dasselbe
> Muster wie bei der Messkette (TB-27/TB-28) und den Ergebniskurven.
> `shared/snapshot.py` legt deshalb **kein drittes** an, sondern lädt
> `herkunft.py` — und bricht ab, wenn das nicht geht, statt ersatzweise selbst
> zu rechnen.

### 3.2 Die drei gemessenen Ausfälle von Entwurf A

Gemessen an einem nachgebauten Baum, in dem `data/live/` die Kursdateien trägt
und `data/` leer ist (Rohausgabe `entwurf_a_ausfaelle.txt`):

| | was passiert | laut |
|---|---|---|
| 1 | **`shared/paths.py` schweigt.** `DATA_DIR` zeigt auf `data/` mit **null** `.csv` — keine Meldung, kein Fehler. `os.makedirs` legt den leeren Ordner bei Bedarf wieder an. | **still** |
| 2 | **Die neun Bots fallen auf den Live-Abruf zurück.** `entscheidungskerze.lade()` meldet *„Rückfall auf den Live-Abruf für BTCUSDT: Kursdatei fehlt in data/"* und ruft **über das Netz** ab. ⚠️ Genau das verbietet Registertext 5a: *„Kein Modul eines Laufs ruft Kurse über das Netz ab."* | laut, aber **registerwidrig** |
| 3 | **Der Datenstand-Hash wird der der leeren Menge** (`e3b0c442…`, 0 Dateien). | laut |

Alle drei sind behebbar. Sie sind **der Preis von Entwurf A**, nicht ein
Einwand gegen ihn — aber Entwurf B zahlt ihn nicht.

⚠️ **Für TB-46 war Nr. 2 zusätzlich eine Sperre:** die Behebung müsste
`shared/entscheidungskerze.py` ändern, und die ist in dieser Aufgabe
ausdrücklich unberührt zu lassen (Teil 5). Für den späteren Umbau ist sie
das nicht.

### 3.3 Der Preis im Repo — **die Zahl im Auftrag stimmt nicht**

⚠️ Der Auftrag nennt „rund 56 MB". Gemessen
(`research/datenordner_schnitt/repopreis.py`):

* `data/` heute: **211,0 MB** in 223 Dateien. Das Packfile des **ganzen**
  Projekts: **119,6 MB**.
* Ein zweiter Bestand kostet im Repo aber **fast nichts**. An 30 der größten
  Kursdateien (76,8 MB) gemessen:

| | Packfile | Zuwachs |
|---|---:|---|
| A nur der Bestand | 24,65 MB | — |
| B + **byteidentische** Kopie daneben | 24,65 MB | **+0,001 %** der Datenmenge |
| C + um 30 Zeilen je Datei **auseinandergelaufene** Kopie | 24,66 MB | **+0,013 %** |

* Der Grund ist gemessen, nicht angenommen: gleicher Inhalt ergibt **denselben
  Blob**, ähnlicher Inhalt wird als Unterschied gepackt.

**Die Größe ist damit kein Argument in dieser Frage** — weder 56 MB noch 211 MB
werden fällig. Was fällig wird, ist der **Platz auf der Platte** (202 MB je
Snapshot), nicht das Repo.

### 3.4 Die Empfehlung: **Entwurf B**

**Begründung, in der Reihenfolge des Gewichts:**

1. **0 statt 29 Module** auf der Live-Seite. Der Umbau der Selektionsseite (90
   Module) kostet in beiden Entwürfen dasselbe.
2. **Die drei Ausfälle aus 3.2 entfallen** — darunter einer, der still ist, und
   einer, der die Bots gegen Registertext 5a ins Netz schickt.
3. **Der Snapshot liegt außerhalb des Bestandes, den er beschreibt.** Unter
   Entwurf A liegt er darin, und das ist nur so lange harmlos, wie die
   Hash-Berechnung nicht rekursiv wird (3.1 Nr. 2).
4. **Acht Nennungen bleiben richtig** statt irreführend — darunter zwei in
   `forward_test.py`, die nach Regel 1 nicht korrigiert werden dürften und
   damit dauerhaft falsch dastünden.

> ⚠️ **Das ist eine Abweichung vom Register.** Registertext 5a nennt die
> Ordnernamen `data/live/` und `data/snapshots/<hash>/` ausdrücklich.

**Welcher registrierte Gehalt bei Entwurf B vollständig erhalten bleibt:**

| Registertext 5 | bei Entwurf B |
|---|---|
| **(a)** zwei Bestände, getrennt | **erhalten** — `data/` live, `snapshots/<hash>/` eingefroren |
| **(a)** nur der Selektionslauf liest aus dem Snapshot | **erhalten** — eine Frage der Verdrahtung, nicht des Ordnernamens |
| **(a)** kein Netzabruf im Lauf | **erhalten**, und leichter zu halten als unter A (3.2 Nr. 2) |
| **(b)** der Registerhash bezeichnet den Snapshot | **erhalten** — `snapshot.py` benutzt das registrierte Verfahren |
| **(c)** ein zweiter Snapshot ist ein neuer Lauf | **erhalten** — ein bestehendes `<hash>/` wird nie überschrieben |
| **(d)** alles in UTC | **unberührt** |

**Was sich nur im Namen ändert:** `data/` heißt weiter `data/` statt
`data/live/`; die Snapshots liegen als Geschwister **neben** `data/` statt
darunter.

> **Die Entscheidung trifft der Betreiber.** Diese Sitzung hat keinen
> Registertext geändert und kein Modul auf einen neuen Pfad umgestellt.

---

## 4. Teil 3 — das Werkzeug `shared/snapshot.py`

**Voreinstellung ist der Trockenlauf.** Kopiert wird nur mit `--ziehen` —
dieselbe Bauform wie `kursdaten_neuaufbau.py --schreiben` und die Broker-Brücken
(`--echt`).

```
python3 shared/snapshot.py --quelle data --ziel snapshots            # Trockenlauf
python3 shared/snapshot.py --quelle data --ziel snapshots --ziehen
python3 shared/snapshot.py --pruefen snapshots/<hash>
python3 shared/snapshot.py --nur-hash
```

**Die Reihenfolge beim Ziehen ist nicht beliebig:** Quelle prüfen → Hash der
Quelle bilden (er ist der **Name** des Ziels) → Ziel prüfen → kopieren mit
`copy2` (Zeitstempel bleiben) → **jede Datei byteweise** gegen die Quelle →
Hash der **Kopie** gegen den der Quelle → Manifest schreiben.

⚠️ Die letzten beiden Schritte sind nicht dasselbe: der Hashvergleich prüft den
**registrierten** Hash, und der zählt nur `*.csv`. Eine beschädigt angekommene
Datei, die keine Kursdatei ist (etwa eine `.json` daneben), geht dort nicht ein
— der byteweise Vergleich prüft **jede** Datei, unabhängig von ihrer Endung.

**Das Manifest** nennt je Datei Name, Größe und Quersumme, dazu Gesamtzahl,
Gesamthash, den Zeitpunkt in **UTC** und **das Verfahren, mit dem gerechnet
wurde**. Es wird über `os.replace` atomar eingesetzt — es gibt kein halb
geschriebenes Manifest, das beim Nachprüfen wie ein beschädigtes aussieht.

**Die acht Abbruchgründe** — keiner läuft still weiter:

| Fall | Verhalten |
|---|---|
| Ziel `<hash>/` existiert schon | Abbruch, **nie** Überschreiben (Registertext 5c) |
| Quelle leer | Abbruch — ein leerer Snapshot trägt den Hash der leeren Menge und **sieht gültig aus** |
| Quersumme nicht bildbar | Abbruch, die Datei wird genannt |
| Kopie weicht byteweise ab | Abbruch, der halb gezogene Ordner wird **entfernt** |
| Quelle enthält Unterordner | Abbruch — die Berechnung ist nicht rekursiv, der Name deckte den Inhalt nicht |
| Ziel liegt **in** der Quelle | Abbruch — der Lauf kopierte in den Bestand, den er beschreibt |
| Quelle enthält schon ein `MANIFEST.json` | Abbruch — das Manifest des Snapshots würde sie überschreiben |
| Hash-Verfahren nicht ladbar | Abbruch — **keine** Ersatzrechnung |

**Die drei Rückgabewerte:**

| Wert | Bedeutung |
|---:|---|
| **0** | gezogen, oder `--pruefen` findet den Stand **unverändert** |
| **1** | Befund: **verändert** (mit Liste) |
| **2** | **nicht prüfbar** / abgebrochen |

⚠️ **Die 2 ist der Grund, warum es sie gibt.** In TB-45 haben zwei Wachen
„bestanden" gemeldet, ohne etwas gemessen zu haben — ein gescheiterter Aufruf
und ein leeres Ergebnis sahen gleich aus.

---

## 5. Teil 4 — die Wache `shared/test_snapshot.py`

**69 von 69 Prüfungen bestanden**, auf **Python 3.10, 3.11, 3.12 und 3.13**
(je 69/69). ⚠️ **3.9 war in der Cloud nicht installiert** — dafür ist die
Syntax gegen 3.9 geprüft, und der Mac-Testauftrag holt den Lauf nach.

**Dreizehn Mutationsproben, und jede zeigt, dass sie beißt.** `snapshot.py` ist
neu; einen „Stand ohne die Reparatur" gibt es nicht als Commit. Er wird
hergestellt: der Test lädt den Quelltext, **entfernt eine einzelne Wache im
Speicher**, führt das Ergebnis als eigenes Modul aus und lässt dieselbe Probe
erneut laufen.

| Probe | echtes Modul | **ohne die Wache** |
|---|---|---|
| 3a Datei verändert (bei **gleicher Länge**) | VERÄNDERT (1) | gilt als unverändert |
| 3b Datei entfernt | VERÄNDERT (1) | fällt nicht auf |
| 3c Ziel existiert bereits | Abbruch (2), Spur des ersten Laufs unberührt | überschreibt den bestehenden Snapshot |
| 3d Quelle leer | Abbruch (2) | leerer Snapshot entsteht, Name `e3b0c442…` |
| 3e Quersumme nicht bildbar | NICHT PRÜFBAR (2), **behauptet nichts** | erfindet das Urteil „verändert" |
| 3f Datei hinzugefügt | VERÄNDERT (1) — auch die **Nicht-`.csv`** | die Nicht-`.csv` fällt nicht auf |
| 3g Manifest fehlt | NICHT PRÜFBAR (2) | gilt als **geprüft und unverändert** |
| 3h Manifest beschädigt (3 Formen) | NICHT PRÜFBAR (2) | leeres `dateien` gilt als geprüft |
| 3i Kopie weicht ab | Abbruch, halber Ordner entfernt | falscher Snapshot entsteht, **Name ≠ Inhalt** |
| 3j Unterordner in der Quelle | Abbruch (2) | Snapshot entsteht **ohne** den Unterordner, stillschweigend |
| 3k Ziel in der Quelle | Abbruch (2) | kopiert in die eigene Quelle |
| 3l `--pruefen` auf Datei / fehlenden Ordner | NICHT PRÜFBAR (2) | — |
| 3m Quelle hat schon ein `MANIFEST.json` | Abbruch (2) | Snapshot entsteht, **die Quelldatei ist überschrieben** |

**Dazu die Negativ-Probe:** der unberührte Snapshot muss **UNVERÄNDERT (0)**
sein. Ohne sie könnte jede Mutationsprobe grün sein, weil einfach alles rot ist.

⚠️ **Findet eine Probe ihren Ankertext nicht mehr, ist sie ROT, nicht
übersprungen.** Eine Wache, die umgezogen ist, ist eine Wache, die dieser Test
nicht mehr bewacht.

**Der gefährlichste Fall hat eine eigene Probe (3f):** eine hinzugefügte Datei,
die **nicht** `.csv` heißt, ändert den Datenstand-Hash **nicht** (das Verfahren
zählt nur `*.csv`). Wer nur die Manifesteinträge durchgeht **oder** nur den
Gesamthash vergleicht, sieht sie nie. Nur der Vergleich in **beide** Richtungen
findet sie — und Probe 3f weist erst nach, dass der Hash sie wirklich nicht
sieht, und dann, dass das Werkzeug sie trotzdem findet.

**Drei Proben waren im ersten Entwurf falsch gebaut** und sind hier
ausdrücklich genannt, statt still korrigiert zu werden:

* **3a** hängte eine Zeile an — das findet auch der **Größenvergleich**, die
  Probe sagte also nichts über die Quersumme. Jetzt wird ein Byte **ersetzt**.
* **3e** verglich den Ausgang statt die Aussage. Der Gesamthash bricht bei einer
  unlesbaren Datei ohnehin ab, der Ausgang blieb also in beiden Fassungen
  „nicht prüfbar". Verglichen wird jetzt die **Aussage über die Datei**: das
  echte Modul schreibt keine, die Fassung ohne Wache schreibt ein Urteil.
* **3m** behauptete, der überschriebene Quelldatei-Verlust bleibe **unentdeckt**.
  Gemessen bleibt er das **nicht**: das Manifest führt die Quelldatei
  `MANIFEST.json` mit ihrer alten Quersumme, und die stimmt danach nicht mehr —
  `--pruefen` meldet „verändert", **zeigt aber auf das Manifest statt auf die
  verlorene Datei**. Die Probe sagt jetzt das. Der Wert der Wache liegt darin,
  den Grund **vorher** zu nennen, nicht darin, der einzige Finder zu sein.

⚠️ **Die Probe 3m ist erst beim adversariellen Nachlesen des eigenen Moduls
entstanden**, nicht aus der Liste der Aufgabenstellung: eine Quelldatei namens
`MANIFEST.json` wäre vom Manifest des Snapshots **überschrieben** worden. Das
war eine echte Lücke im ersten Entwurf von `snapshot.py` und ist geschlossen.

---

## 6. Der Basislauf

`research/datenordner_schnitt/basislauf.py` führt jede Testdatei einmal aus, in
einem **eigenen Prozess** (neun Bots führen gleichnamige Module — TB-40), mit
Zeitgrenze je Datei und **Beendigung des Kindprozesses** danach.

⚠️ **Ein Python-Runner statt `timeout`,** weil der Mac kein GNU `timeout` hat.
⚠️ **`trading-env/` ausgeschlossen** — sonst 1 312 statt 63 Testdateien.

**63 Testdateien** (62 wie in der Aufgabenstellung, plus das neue
`shared/test_snapshot.py`).

*Die Zahlen des Laufs stehen in `research/datenordner_schnitt/ergebnisse/basislauf.json`
und in der Rohausgabe `basislauf_roh.txt` der ZIP.*

### Was **ungeprüft** heißt, und warum es nicht grün ist

Drei Tests verlangen ein Bot-Argument und geben ohne eines nur ihre
Nutzungszeile aus. Das ist ein Rückgabewert, **aber keine Messung** — der Lauf
führt sie als `ungeprueft`, nicht als `gruen`:
`research/drawdown_reihenfolge/test_drawdown.py`,
`research/fib_score_stufen/test_stufen.py`,
`research/elliott_wave_params/test_params.py`.

`shared/test_drawdown_beide_masse.py` terminiert nicht (bekannt) und läuft in
die Zeitgrenze; der Kindprozess wird danach beendet.

---

## 7. ⚠️ Jede Abweichung von der Umgebungstabelle des Auftrags

**Die Aufgabenstellung bittet ausdrücklich darum, Abweichungen zu melden.
Gemessen am 17.09.2026 (Rohausgabe `umgebung.txt`):**

| Punkt | Auftrag sagt | **gemessen** |
|---|---|---|
| **Python in der Cloud** | „3.11 oder neuer" | `python3` ist **3.11.15**, daneben liegen **3.10.20, 3.12.3 und 3.13.12**. ⚠️ **3.9 ist nicht dabei** — die Fassung des Betriebs war hier **nicht lauffähig prüfbar**, nur ihre Syntax |
| **`pandas`/`numpy`** | „wechselnd — prüfen, ggf. nachinstallieren" | ⚠️ **fehlten vollständig**, nachinstalliert: **pandas 3.0.5 / numpy 2.4.6**. Der Mac hat **pandas 2.3.3** — eine **Hauptversion** Unterschied |
| **`scipy`** | „vorhanden" | ⚠️ **fehlte**, nachinstalliert (1.17.1) |
| **`dateparser`** | `UMGEBUNGEN.md`: 1.4.3 | fehlte, nachinstalliert: 1.4.3 ✓ |
| **`node`** | „wechselnd" | **vorhanden**, v22.22.2 |
| **GNU `timeout`** | „vorhanden" | vorhanden ✓ (`/usr/bin/timeout`) |
| **Binance, yfinance** | „gesperrt (403)" | ⚠️ **schärfer als das:** die **Pakete selbst** fehlten (`binance`, `yfinance`). Nicht am Netz gescheitert, sondern am Import. Nachinstalliert: yfinance 1.7.0, binance 1.0.37. **Kein Abruf ausgelöst** |
| **`fastapi`, `pandas_market_calendars`, `python-telegram-bot`** | (nicht genannt) | ⚠️ **fehlten alle drei**; `dashboard/test_dashboard.py` brach deshalb beim Import ab. Nachinstalliert: 0.141.1 / 4.6.1 / 22.8 |
| **Zeitzonendaten** | (nicht genannt) | ⚠️ **`US/Eastern` fehlte.** `/usr/share/zoneinfo` ist eine Minimalfassung ohne die alten `US/`-Namen; `America/New_York` war da. `broker/test_ibkr.py` brach deshalb beim Import ab — mit `tzdata` behoben |

⚠️ **Die Paketlage ist damit die grösste Abweichung von der Tabelle**, und sie
hat den Basislauf zweimal verschoben: **vor** der Nachinstallation waren acht
Testdateien rot, die nach ihr grün sind. Beide Läufe liegen in der ZIP
(`basislauf_roh_vor_nachinstallation.txt` und `basislauf_roh.txt`), damit
nachvollziehbar bleibt, welche Zahl woher kommt.

### Und der Nachweis, dass keiner dieser roten Tests von dieser Arbeit kam

⚠️ **Nicht behauptet, sondern gemessen.** Die acht vor der Nachinstallation
roten Testdateien sind zweimal gelaufen: einmal im Arbeitsbaum dieser Sitzung
und einmal in einer Kopie desselben Commits (`7ff3aa7`) **ohne die fünf
Neuzugänge** dieser Sitzung. Die Ergebnisse sind **Zeile für Zeile gleich** —
gleiche Rückgabewerte, gleiche Prüfungszahlen (Rohausgaben
`vergleich_vorher.txt` / `vergleich_nachher.txt`).

Das war möglich, weil diese Sitzung **keine bestehende Datei geändert hat**:
`git diff HEAD` ist leer, alle Neuzugänge sind unversionierte neue Dateien. Der
Stand „ohne diese Arbeit" liess sich deshalb exakt herstellen.

**Und eine Abweichung in der Liste der bekannt roten Tests:**

⚠️ `research/exposure_messung/test_exposure_kern.py` ist in der Cloud **grün**,
in der Liste steht er als rot (Mac, 17.09.). Der Basislauf markiert das
ausdrücklich als `UNERWARTET` — **auch ein bekannt roter Test, der plötzlich
grün ist, ist eine Abweichung und wird gemeldet.** Welche Umgebung recht hat,
entscheidet Schritt 5 des Mac-Testauftrags.

**Eine Abweichung in der Aufgabenstellung selbst:** die „rund 56 MB" für den
zweiten Bestand (siehe 3.3). `data/` sind **211,0 MB**; der Zuwachs im Repo
liegt bei **weit unter einem Prozent** davon.

---

## 8. Was ausdrücklich nicht passiert ist

| | |
|---|---|
| ❌ | Kein echter Snapshot gezogen, keiner committet |
| ❌ | `data/` nicht umbenannt, nicht verschoben, nicht angefasst — Hash vorher = nachher |
| ❌ | Kein Modul auf einen neuen Pfad umgestellt |
| ❌ | `forward_test.py`, `live_params.py`, `equity_simulation.py`: **unberührt** |
| ❌ | `shared/entscheidungskerze.py`: **unberührt** |
| ❌ | Kein Registertext geändert — die Abweichung ist **berichtet**, nicht vollzogen |
| ❌ | Keine Bot-Datei importiert; kein Trade, kein Parameter, kein Broker-Abruf |
| ❌ | Keine Zugangsdaten gelesen (kein `cat`, kein `git show` auf Konfigurationsdateien) |

**Neu in diesem Zweig:** `shared/snapshot.py`, `shared/test_snapshot.py`,
`research/datenordner_schnitt/` (Erhebung, Repopreis, Basislauf, BERICHT,
Ergebnis-JSONs), dieses Dokument und der Mac-Testauftrag.

---

## 9. Was offen bleibt — und wem es gehört

| | Punkt | wem |
|---:|---|---|
| 1 | **Welcher Entwurf gilt.** Empfohlen ist B; das ist eine Abweichung vom Registertext und damit eine Entscheidung des Betreibers, keine dieser Sitzung | **Betreiber** |
| 2 | **Der Umbau selbst** — 90 Module der Selektionsseite auf den Snapshot zeigen, und bei Entwurf A zusätzlich 29 auf der Live-Seite. Eine eigene, große Aufgabe | eigene Aufgabe |
| 3 | **Das doppelt geführte Hash-Verfahren** (`pruefe_register.py:319` gegen `herkunft.py:96`). Heute gleich, morgen vielleicht nicht | eigene Aufgabe |
| 4 | **`shared/paths.py:18`** legt `data/` beim Import an. Harmlos heute, still im Fehlerfall | eigene Aufgabe |
| 5 | **Der Mac-Lauf auf Python 3.9.6** und der echte Snapshot über 223 Dateien | Mac-Testauftrag |
| 6 | **`broker/test_ibkr.py` benutzt `US/Eastern`**, einen veralteten Zonennamen, der in Minimal-tzdata fehlt | eigene Aufgabe |

---

## In einfacher Sprache

**Was wir wissen wollten.**
Das Register verlangt seit einem Nachtrag zwei Sammlungen von Kursdaten statt
einer: eine, die jeden Tag weitergeschrieben wird und aus der die Bots lesen,
und eine eingefrorene Kopie, aus der nur der große Auswahllauf liest. Der Grund
ist einfach: wer prüfen will, ob der Backtest und der laufende Bot dasselbe
rechnen, braucht die Eingabe von damals — und die gibt es heute nirgends mehr.
Bevor irgendetwas umgebaut wird, sollte jemand ausgemessen haben, was der Umbau
kostet. Bisher war das geschätzt, nie gezählt.

**Was herausgekommen ist.**
Die Schätzung lautete „hundertundein Programm liest diesen Ordner". Gezählt sind
es **hundertzweiundachtzig** — aber das ist die gute Nachricht, denn fast alle
holen sich den Ordnernamen von woanders. **Nur neunundzwanzig schreiben ihn
selbst hin, und sieben davon sind die Stellen, an denen er hingehört.** Vor
allem: **keine der neun Bot-Dateien, die nicht angefasst werden dürfen, nennt
den Ordner überhaupt.** Der Umbau ist also machbar, ohne sie anzurühren.

**Der Vorschlag.**
Es lagen zwei Zuschnitte auf dem Tisch. Der eine benennt den heutigen Ordner um
und legt die Kopie darunter — so steht es im Register. Der andere lässt den
heutigen Ordner, wie er ist, und legt die Kopie daneben. **Empfohlen wird der
zweite**, weil er auf der Bot-Seite **null** Änderungen kostet statt
neunundzwanzig, und weil beim ersten drei Dinge schiefgehen, die alle
nachgemessen sind — darunter eines, das nichts sagt: ein Programm findet dann
einen leeren Ordner und beschwert sich nicht. **Das ist eine Abweichung vom
Register, und deshalb entscheidest du das, nicht diese Sitzung.** Was inhaltlich
gleich bleibt, steht oben in einer Tabelle, Punkt für Punkt.

**Was gebaut wurde.**
Das Werkzeug, das die eingefrorene Kopie zieht. Es ist misstrauisch gebaut: es
kopiert nichts, solange man es nicht ausdrücklich dazu auffordert, es vergleicht
hinterher **jede Datei Byte für Byte** mit dem Original, es überschreibt eine
vorhandene Kopie **nie**, und es weigert sich, eine leere Kopie anzulegen — die
sähe nämlich täuschend gültig aus. Dazu gibt es eine Wache mit
neunundsechzig Prüfungen. Dreizehn davon machen absichtlich etwas kaputt und
schauen nach, ob das Werkzeug es merkt; und jede dieser dreizehn führt zusätzlich
vor, dass eine Fassung **ohne** die entsprechende Prüfung denselben Fehler
**übersieht**. Das ist der Unterschied zwischen „es ist grün" und „es ist
bewiesen".

**Was sich an deinen Daten geändert hat.**
Nichts. Der Fingerabdruck der 223 Kursdateien ist am Ende derselbe wie am
Anfang, und das steht oben in der ersten Tabelle. Es wurde keine Kopie
angelegt, die 200 Megabyte in dieses Projekt getragen hätte — die richtige
Kopie wird an dem Tag gezogen, an dem du den Auswahllauf startest. Nebenbei
ist eine Zahl aus der Aufgabenstellung korrigiert worden: die Kopie kostet im
Projektspeicher **so gut wie nichts**, weil git gleiche Dateien nur einmal
ablegt. Auf der Festplatte kostet sie 202 Megabyte.

**Was noch zu tun ist.**
Du entscheidest die Namensfrage. Und dein Rechner muss den Test noch einmal
laufen lassen — er benutzt eine ältere Python-Ausgabe, die es in der Cloud
nicht gibt, und dreimal an einem Tag hat genau dieser Unterschied etwas
gefunden, das die Cloud nicht sehen konnte. Der Auftrag dafür liegt bereit, mit
einem Startbefehl zum Kopieren.
