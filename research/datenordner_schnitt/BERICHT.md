# Der Schnitt durch den Datenordner — Erhebung und Werkzeug (TB-46)

**Frage:** Registertext 5 verlangt zwei Kursdatenbestände — einen fortgeschriebenen
Live-Bestand und einen unveränderlichen Snapshot. Was kostet dieser Schnitt, und
welcher der beiden vorgeschlagenen Zuschnitte ist der billigere?

**Diese Untersuchung fasst keinen Bot-Code an.** Sie liest `data/` (einmal, für den
Hash) und ändert dort nichts. Sie schlägt vor; die Entscheidung trifft der Betreiber.

---

## Was hier liegt

| Datei | was sie tut |
|---|---|
| `erhebung.py` | misst über den Syntaxbaum, **wie** die Module `data/` erreichen |
| `repopreis.py` | misst, was ein zweiter Bestand im Repo wirklich kostet |
| `basislauf.py` | führt jede Testdatei einmal aus, mit Zeitgrenze je Datei |
| `ergebnisse/*.json` | die Rohzahlen aller drei Messungen |

Das Werkzeug selbst — `shared/snapshot.py` — liegt nicht hier, sondern unter
`shared/`, weil es kein Untersuchungsgerät ist, sondern am Tag des signierten Tags
benutzt wird. Seine Wache ist `shared/test_snapshot.py`.

---

## 1. Die gemessene Zahl: **182**, nicht 101

⚠️ **Die 101 aus TB-34 ist nicht falsch — sie zählt etwas anderes.** Beide Zahlen
sind hier nachgemessen:

| Zählung | Zahl | was sie zählt |
|---|---:|---|
| TB-34 (`research/kursdaten_neuaufbau/datenwege.py`, unverändert erneut gelaufen) | **101** | 37 Module mit `read_csv` auf einem `DATA_DIR`-Pfad + 64 Module, die `load_all_symbol_data` importieren |
| TB-46 (`erhebung.py`) | **182** | jedes Modul mit mindestens einer Fundstelle zum echten Bestand — zusätzlich über `entscheidungskerze.lade()`, `herkunft.datenstand()`, `kursdaten.pruefe_ordner()` und über `DATA_DIR`-Benutzungen ohne eigenes `read_csv`. ⚠️ Die Erhebung findet heute **184**; zwei davon sind `shared/snapshot.py` und `shared/test_snapshot.py`, die es vor TB-46 nicht gab. Sie werden benannt, nicht abgezogen — 182 ist der Stand, den der Umbau vorfindet |

**Die 101 ist exakt reproduziert** (37 + 64), mit demselben Skript auf demselben
Baum. Der Unterschied ist der Zuschnitt der Frage, nicht ein Fehler.

Ein Modul zählt hier **nur dann**, wenn es den echten Bestand erreicht. Ein
Selbsttest, der sich unter `tempfile.mkdtemp()` ein eigenes `data` baut, zählt
nicht (ein Modul).

---

## 2. Die eigentliche Antwort: **der Zugriff ist heute schon fast überall mittelbar**

| | Module |
|---|---:|
| bauen den Pfad **selbst** aus einem Literal | **29** |
| beziehen ihn **nur mittelbar** (Konstante aus `shared/`, oder über einen Trichter) | **145** |
| **nennen** `data/` nur, ohne einen Pfad zu bauen (git-Filter, Meldungen) | **8** |

Und von den 29, die selbst bauen, sind **7 die gemeinsamen Stellen**:

| Stelle | Zeile | Ausdruck |
|---|---:|---|
| `shared/paths.py` | 15 | `os.path.join(BASE_DIR, "data")` |
| `shared/strategy_paths.py` | 49 | `os.path.join(base_dir, "data")` |
| `shared/entscheidungskerze.py` | 257 | `os.path.join(BASE_DIR, "data")` |
| `shared/kursdaten.py` | 156 | `os.path.join(os.path.dirname(_SHARED), "data")` |
| `shared/abrufschutz.py` | 501 | `os.path.join(os.path.dirname(_SHARED_DIR), "data")` |
| `shared/zeitabdeckung.py` | 659 | `os.path.join(os.path.dirname(_SHARED), "data")` |
| `research/vorregistrierung/herkunft.py` | 98 | `os.path.join(BASE_DIR, "data")` |

Die übrigen 22 sind 16 Untersuchungen unter `research/` und 6 Prüfwerkzeuge — keine
davon im Cron-Betrieb.

⚠️ **Es gibt also keine *eine* gemeinsame Stelle, sondern sieben.** Das ist der
Befund: nicht „hundert Änderungen" und nicht „eine", sondern sieben Stellen im
Betrieb plus zweiundzwanzig am Rand.

### Die Rollen

| Rolle | Module | soll lesen aus |
|---|---:|---|
| Selektion/Backtest | **90** | dem **Snapshot** |
| Untersuchung (`research/`) | 48 | je nach Zweck |
| Betrieb (neun Bots, Cron, Dashboard, Telegram) | 25 | dem **Live-Bestand** |
| Prüfwerkzeug | 19 | beidem, je nach Frage |

### Die Schreiber — 11, und zwei davon sind eine Überraschung

Neun sind die Abrufskripte (dieselben neun wie in TB-34). Dazu:

* ⚠️ **`shared/paths.py:18` — `os.makedirs(DATA_DIR, exist_ok=True)` beim Import.**
  Das ist kein `to_csv`, aber es schreibt: **jeder Import von `paths.py` legt
  `data/` wieder an, wenn es fehlt.** Unter Entwurf A entsteht dadurch stillschweigend
  ein leerer `data/`-Ordner neben `data/live/` (unten gemessen).
* `shared/test_entscheidungskerze.py:697` schreibt in ein nachgebautes `data` unter
  einem Temp-Ordner — kein Zugriff auf den Bestand.

### Die Dateimuster

⚠️ Es ist **`AAPL_1d.csv`**, nicht `AAPL.csv`. Gezählt über alle Module:
`f"{symbol}_{INTERVAL}.csv"` (16×), `f"{symbol}_{intervall}.csv"` (8×),
`f"{symbol}_1d.csv"` (5×), dazu feste Namen wie `BTCUSDT_1h.csv` (7×) und
`AAPL_1d.csv` (6×).

---

## 3. Die Hash-Berechnung — wie sie heute läuft

**Sie steht in einer Funktion:** `research/vorregistrierung/herkunft.py::datenstand`.
SHA-256 über die `*.csv` **direkt** im Ordner, in sortierter Namensfolge, je Datei
**Name + Größe + SHA-256 des Inhalts**.

Drei Eigenschaften, jede mit einer Folge für den Zuschnitt:

1. ⭐ **Sie ist nicht rekursiv.** `os.listdir` + `endswith(".csv")`. Ein
   `data/snapshots/` **innerhalb** von `data/` würde vom registrierten Hash **nicht**
   mitgezählt. *Gemessen in `shared/test_snapshot.py`, Probe 3j: derselbe Ordner mit
   und ohne Unterordner ergibt denselben Hash.* **Die Sorge aus der
   Aufgabenstellung — „läuft die Hash-Berechnung rekursiv, zählt sie den Snapshot
   mit" — trifft also nicht ein.**
2. **Sie zählt nur `*.csv`.** Das `MANIFEST.json` im Snapshot ändert dessen Hash
   nicht. ⚠️ Die Kehrseite: eine **hinzugefügte Nicht-`.csv`-Datei** verändert den
   Hash **nicht** — nur der Vergleich gegen das Manifest findet sie (Probe 3f).
3. **Sie hängt am übergebenen Ordner.** Die Voreinstellung ist `BASE_DIR/data`.

⚠️ **Befund: das Verfahren steht doppelt im Repo.** Ein zeichengleiches Duplikat
liegt in `research/registernachtrag_tb41/pruefe_register.py:319`. Heute liefern beide
dasselbe. Wer eines ändert, merkt den Unterschied nicht — dasselbe Muster, das bei
der Messkette (TB-27/TB-28) und bei den Ergebniskurven schon eingesammelt wurde.
`shared/snapshot.py` legt deshalb **kein drittes** an, sondern lädt `herkunft.py`.

---

## 4. Die beiden Entwürfe, gegeneinander gerechnet

| Frage | **Entwurf A** `data/live/` + `data/snapshots/<hash>/` | **Entwurf B** `data/` bleibt, `snapshots/<hash>/` daneben |
|---|---|---|
| Module mit eigenem Pfadbau, die umgestellt werden müssen | **29**, davon **7 gemeinsame Stellen** | **0** |
| Nennungen, die danach irreführend dastehen | **8** (u. a. zwei `forward_test.py`) | **0** |
| Müsste ein `forward_test.py` angefasst werden? | **nein** — keine der neun baut einen Pfad | **nein** |
| Hash-Berechnung | Snapshot liegt **innerhalb** `data/`, wird aber **nicht** mitgezählt (nicht rekursiv). ⚠️ Dafür zeigt die Voreinstellung von `datenstand()` auf einen Ordner **ohne eine einzige `.csv`** | unberührt |
| `git pull` / Cron | drei gemessene Ausfälle, siehe unten | keine Umbenennung, kein Ausfall |
| Preis im Repo | gleich | gleich |
| Register | **wörtlich** nach Registertext 5 | **Abweichung im Namen** |

### Die drei gemessenen Ausfälle von Entwurf A

Gemessen an einem nachgebauten Baum, in dem `data/live/` die Kursdateien trägt und
`data/` selbst leer ist — genau der Zustand nach dem Umzug (Rohausgabe
`entwurf_a_ausfaelle.txt` in der ZIP):

1. **`shared/paths.py` schweigt.** `DATA_DIR` zeigt auf `data/`, dort liegen
   **null** `.csv` — kein Fehler, keine Meldung. Und `os.makedirs` legt den leeren
   Ordner bei Bedarf wieder an.
2. **Die neun Bots fallen auf den Live-Abruf zurück.** `entscheidungskerze.lade()`
   meldet zwar ordentlich *„Rückfall auf den Live-Abruf für BTCUSDT: Kursdatei fehlt
   in data/"* — und ruft dann **über das Netz** ab. ⚠️ Genau das verbietet
   Registertext 5a: *„Kein Modul eines Laufs ruft Kurse über das Netz ab."*
3. **Der registrierte Datenstand-Hash wird der der leeren Menge.**
   `datenstand("data")` ergibt `e3b0c442…` bei **0** Dateien. Die Wache
   `research/etf_trendfolge/datenstand.py` meldet dann ABWEICHUNG — nicht weil sich
   Daten geändert haben, sondern weil der Ordner umgezogen ist.

Alle drei sind **behebbar** — sie sind der Preis, nicht ein Einwand. Aber sie sind
der Preis von Entwurf A, und Entwurf B zahlt ihn nicht.

### Der Preis im Repo: **die Zahl im Auftrag stimmt nicht**

⚠️ Der Auftrag nennt „rund 56 MB". Gemessen (`repopreis.py`):

* `data/` heute: **211,0 MB** in 223 Dateien; das Packfile des ganzen Projekts
  **119,6 MB**.
* Ein zweiter Bestand kostet im Repo aber **fast nichts**: eine byteidentische Kopie
  30 großer Kursdateien (76,8 MB) ließ das Packfile um **0,001 %** wachsen, eine um
  30 Zeilen je Datei auseinandergelaufene um **0,013 %**.
* Der Grund ist gemessen, nicht angenommen: gleicher Inhalt ergibt **denselben
  Blob**, ähnlicher Inhalt wird als Unterschied gepackt.

**Die Größe ist also kein Argument gegen den zweiten Bestand im Repo** — weder 56 MB
noch 211 MB werden fällig.

---

## 5. Die Empfehlung: **Entwurf B**, mit einem Zusatz

**Entwurf B kostet auf der Live-Seite null Änderungen, Entwurf A kostet 29.** Beide
kosten auf der Selektionsseite dasselbe (90 Module müssen auf den Snapshot zeigen —
das ist der eigentliche Umbau und in keinem der beiden Entwürfe billiger).

⚠️ **Entwurf B weicht vom Registertext ab, und das ist zu benennen.** Registertext 5a
nennt die Ordnernamen `data/live/` und `data/snapshots/<hash>/` ausdrücklich.

**Was bei Entwurf B vom registrierten Gehalt erhalten bleibt — vollständig:**

* **zwei Bestände**, getrennt und getrennt lesbar;
* **der Hash bezeichnet den Snapshot** (5b) — unberührt, `snapshot.py` benutzt das
  registrierte Verfahren;
* **nur der Selektionslauf liest aus dem Snapshot** (5a) — eine Frage der
  Verdrahtung, nicht des Ordnernamens;
* **ein zweiter Snapshot ist ein neuer Lauf** (5c) — `snapshot.py` überschreibt ein
  bestehendes `<hash>/` nie;
* **UTC** (5d) — unberührt.

**Was sich nur im Namen ändert:** `data/` heißt weiter `data/` statt `data/live/`,
und die Snapshots liegen als Geschwister neben `data/` statt darunter.

**Der Zusatz:** Entwurf B hat einen Vorteil, der im Register nicht steht und der die
Wache vereinfacht — **der Snapshot liegt außerhalb des Bestandes, den er beschreibt.**
Unter Entwurf A liegt er darin, und dass das heute harmlos ist, hängt an einer
Eigenschaft der Hash-Berechnung (nicht rekursiv), die niemand zugesichert hat. Wer
sie eines Tages rekursiv macht — etwa um Unterordner je Zeitrahmen zu unterstützen —
entwertet damit den registrierten Hash, ohne eine Kursdatei anzufassen.

**Die Entscheidung trifft der Betreiber.** Diese Untersuchung stellt keinen
Registertext um und stellt kein Modul auf einen neuen Pfad um.

---

## 6. Was hier ausdrücklich nicht passiert ist

* Kein echter Snapshot gezogen, keiner committet.
* `data/` nicht umbenannt, nicht verschoben, nicht angefasst — der Datenstand-Hash
  ist vor und nach der Arbeit `d9449faf51bffaaac96004e7a192978b4bef4498404f245421e7ccfcea995f84`
  bei 223 Dateien.
* Kein Modul auf einen neuen Pfad umgestellt.
* `forward_test.py`, `live_params.py`, `equity_simulation.py`,
  `shared/entscheidungskerze.py`: **unberührt**.
* Kein Registertext geändert.

---

*TB-46, 17.09.2026. Vorgänger: TB-45 (`7ff3aa7`). Ergebnisdokument:
`docs/ERGEBNIS_TB-46_datenordner.md`, Mac-Testauftrag:
`docs/TESTAUFTRAG_TB-46_datenordner.md`.*
