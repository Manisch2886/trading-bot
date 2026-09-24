# TB-102 — Ergebnis: Läuft `messgroessen.py` im Selektionsmodus? — Nein. Und mit den Modus-Variablen der Bots läuft es, liefert bytegleich und liest dabei ausschliesslich aus dem Repo

**Sitzungstitel:** `TB-102` · **Stand:** 24.09.2026 · **Auftrag:**
`docs/auftraege/MAC_TB-102_messgroessen_im_modus.md` · **Belege:** `docs/belege/TB-102/`
**Eingang:** `bba6f25` (TB-98-Abgabe) · Commits: `1c09f3e` (Schritt 0), Abgabe-Commit (Belege,
dieses Dokument, Journalblock DA).
**Grundlage:** Fable 23d/23e (Eingabestand, Nachweis im Modus), Register 40.6.
**Umgebung aller Messungen:** Mac, `trading-env/bin/python3` (3.9.6). Lesehaken aus TB-98
(`docs/belege/TB-98/haken/sitecustomize.py`, unverändert).

⭐ **Kurz:** Der Nachweis aus 23e ist **im Selektionsmodus nicht geführt**, und zwar in beiden
Lesarten von „Modus“ nicht:

| Lesart von „im Modus“ | Ausgang | woher gelesen |
|---|---|---|
| **`TB30A_BASE_DIR` = Snapshot** (der einzige Schalter, den `messgroessen.py` kennt) — **B1** | ⚠️ **Abbruch rc 1**, `FileNotFoundError` bei `messgroessen.py:209` (aus `:329`), 1 s, keine Datei | Snapshot: 2 Universumsdateien; Haltedauer-Datei **fehlt** |
| **`TB_SELEKTIONS*`** (der Modus der Bots, `shared/paths.py`) — **Z3** | ⚠️⚠️⚠️ **rc 0, bytegleich `7f46d5f5`** | **100 % Repo**: 222 × `data/`, 2 × `config/`, 1 × `research/`; **0 × Snapshot** |
| ohne Modus — **B2** | rc 0, bytegleich `7f46d5f5` | Repo, wie Z3 |

- ⚠️⚠️⚠️ **Der Fund, auf den es ankommt (Z3):** `messgroessen.py` importiert `shared/paths.py`
  nicht. Die Modus-Variablen der Bots wirken dort **gar nicht**. Ein Lauf, der „im Modus“
  gestartet wird, rechnet still auf dem Repo. Dass trotzdem bytegleich herauskommt, liegt nur
  daran, dass `data/` **heute** dem Snapshot gleicht (222/222 Kursdateien und 2/2
  Universumsdateien byteweise gleich, `b2_ohne_modus.txt`). Nach der nächsten Auffrischung von
  `data/` wäre das nicht mehr so, und der Lauf würde es nicht melden. Das ist dieselbe Klasse wie
  Befund 1 aus TB-98.
- ⚠️ **Hinter dem Abbruch aus B1 liegt eine zweite Hürde (Z1).** Wird die Haltedauer-Datei
  ergänzt, bricht der Lauf trotzdem ab: „Keine Kursdaten fuer Suffix 1d gefunden.“ Der Snapshot
  ist **flach**, `messgroessen.py` sucht `BASE_DIR/data/`. `TB30A_BASE_DIR` ist laut
  `registerdaten.py:52–57` als Ersatz für die **Repo-Wurzel** gebaut (für Mutationsproben) und
  nicht als Snapshot-Schalter.
- ⭐ **Der Inhalt trägt (Z2).** Liegt der Snapshot-Inhalt in der Anordnung des Repos (`data/` →
  Snapshot-Wurzel, `config/` → Snapshot-`config/`) und dazu die Haltedauer-Datei aus dem Repo,
  gibt es zweimal rc 0 und zweimal bytegleich `7f46d5f5`. **Einzige Eingabe von ausserhalb des
  Snapshots ist dann `haltedauern_je_bot.csv`.**
- ⭐ **A7:** `messgroessen.py` liest genau **drei Klassen** nicht registrierter Eingaben:
  Kursdaten (222), Universumsdateien (2) und `haltedauern_je_bot.csv` (1). **Eine vierte gibt
  es nicht.**
- ⭐ **Block C:** `haltedauern_je_bot.csv` fliesst an **zwei** Stellen weiter, nicht an einer.
  `max_tage` geht in `purge_tage`: Das verschiebt **keine Faltengrenze**, nur Purge, Embargo und
  Trainingsende sowie Inhalt und Hash von `faltenplan.json`. `median_balken` geht in die
  **Untergrenze der Donchian-Achse** von `turtle_soup_crypto` und `turtle_soup_stocks`, also ins
  Raster. Ausserdem entsteht die CSV aus den **ausgeführten** Trades (`*_positionen.csv`). Die
  Faltenlänge dagegen zählt absichtlich die **gefundenen**, weil die ausgeführten am
  Positionslimit hängen.

Nichts hat sich bewegt: Summenhash über alle 1528 versionierten Dateien ausserhalb von `docs/`
vorher = nachher, `git status` ausserhalb von `docs/` leer, in `ergebnisse/` nichts neu,
`messgroessen.json` `2a9b9166` und Nachweis `7f46d5f5` unverändert, Snapshot-Summenhash gleich,
Sonde vorher = nachher (`b_hashes.txt`).

---

## 0. Schritt 0

Arbeitsbaum committet als `1c09f3e` (Zeiger, Auftrag TB-102, Fable-Anfrage 24d).
`find .git -name '*.lock'` → keine. HEAD am Eingang `bba6f25`, wie im Auftrag.

## 1. Block A — Vormessung nachgemessen (`a_vormessung.txt`, `a7_lesequellen.txt`)

| | Vormessung | gemessen |
|---|---|---|
| **A1** | Z. 207–209 liest `haltedauern_je_bot.csv` | ✅ bestätigt, dynamisch `messgroessen.py:209 < :329 < :360` |
| **A2** | aus `auswertung.py` Z. 310, einziger Commit `78e2bc6` | ✅ bestätigt. **Ergänzt:** gerechnet aus `<bot>_positionen.csv`, also aus den **ausgeführten** Trades (`auswertung.py:71`, `:296`). `auswertung.py` schreibt fest nach `ergebnisse/` und liest fest aus `daten/`, ohne `--ziel` |
| **A3** | nicht im Snapshot | ✅ 0 Treffer. Der Snapshot hat **kein** `data/` und **kein** `research/`: 223 CSV flach, `MANIFEST.json`, `config/` |
| **A4** | `faltenplan.py:272` → `purge_tage` | ✅ bestätigt |
| **A5** | `2a9b9166…` / `7f46d5f5…` | ✅ bestätigt |
| **A6** | vier Gruppen gelesen, nur `volatilitaet` weicht ab, `datenbereiche` fliesst nirgends hin | ✅ für die **gelesenen** Gruppen (`kosten`, `datenfrequenz`, `volatilitaet`, `haltedauer`). **Präzisiert:** `datenbereiche` weicht **auch** ab (9 von 20 Blättern; `volatilitaet` 39 von 56; zusammen die 48 aus TB-93), hat aber keinen Leser. Ebenfalls ohne Leser: `universum`, `median_tage`, `n_positionen`. **Ergänzt:** `haltedauer` fliesst ausser über `purge_tage` noch über `median_balken` → `registerdaten.py:231` → Donchian-Untergrenze |

**A7 — die Lesequellen (ein Lauf ohne Modus, = B2):**

| Herkunft | Dateien | geöffnet von |
|---|---|---|
| `data/*.csv` (Repo) | 222 (444 Öffnungen) | `messgroessen.py:100` |
| `config/*.txt` (Repo) | 2 | `messgroessen.py:91` (aus `:314/315` und `:233`) |
| `research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv` (Repo) | 1 | `messgroessen.py:209` |
| Code | 1 (`messgroessen.py` selbst, kein Modul aus `shared/`) | — |
| anderswo | `SystemVersion.plist`, `/dev/urandom`, `zoneinfo/UTC` (Import von pandas, Z. 48), die Ausgabedatei | — |

⇒ **Genau die zwei bekannten Eingaben plus die Universumsdateien. Eine vierte gibt es nicht.**
⚠️ Grenze des Hakens: `os.path.exists` (Z. 98) ist kein `open`-Ereignis. Welche Symboldatei
**fehlt**, sieht der Haken nicht, nur, welche gelesen wurde. `lies()` überspringt ein fehlendes
Symbol still, und die Zahl steht nur als `symbole_gemessen` in der Ausgabe.

## 2. Block B — Läuft es im Modus?

| | Lauf | rc | Ergebnis | Beleg |
|---|---|---|---|---|
| **B1** | `TB30A_BASE_DIR` = Snapshot **und** `TB_SELEKTIONS*` | **1** | `FileNotFoundError: …/snapshots/63e4b6c8…/research/tb24_haltedauern/ergebnisse/haltedauern_je_bot.csv` bei `messgroessen.py:209` (aus `:329`, nach `universum()` aus Snapshot-`config/`). Keine Datei | `b1_modus.txt` |
| **B2** | ohne Modus | 0 | **bytegleich** Nachweis `7f46d5f5`; gegen `2a9b9166` erste Abweichung Zeichen 260 (wie TB-93) | `b2_ohne_modus.txt` |
| **B3** | B1 zweimal wiederholt | 1, 1 | dreimal derselbe Abbruch an derselben Stelle. „Zweimal bytegleich“ ist im Modus **nicht prüfbar** | `b3_zweimal.txt` |

**Zusatzproben** (Hilfsbäume aus Verknüpfungen im Scratchpad, nichts im Repo; alle in `b1_modus.txt`):

| | Aufbau | rc | Ergebnis | woher |
|---|---|---|---|---|
| **Z1** | Snapshot unverändert + nur die Haltedauer-Datei | 1 | „Keine Kursdaten fuer Suffix 1d gefunden.“ `datenbereiche()` lief davor still auf `{}` | Snapshot-`config/`, Repo-CSV |
| **Z2** | Snapshot-Inhalt in Repo-Anordnung + Haltedauer-Datei aus dem Repo, **zweimal** | 0, 0 | **bytegleich `7f46d5f5`**, beide Male | 224 × Snapshot, 1 × Repo (`haltedauern_je_bot.csv`) |
| **Z3** | **nur** `TB_SELEKTIONS*`, ohne `TB30A_BASE_DIR` | **0** | **bytegleich `7f46d5f5`** | ⚠️⚠️⚠️ **222 × `data/`, 2 × `config/`, 1 × `research/` im Repo; 0 × Snapshot** |

Der Auftrag nennt vier Ausgänge. **Gemessen ist der zweite (Abbruch, Datei nicht gefunden) für
`TB30A_BASE_DIR` und der vierte (bytegleich, aber aus dem Repo) für die Modus-Variablen der
Bots.** Welche Lesart Fable meint, entscheidet, welcher der beiden gilt (Abschnitt 5, Frage 1).

## 3. Block C — Was die Kette bewegt (`c_kette.txt`, `c_stoerprobe.py`, `c_stoerprobe_lauf.txt`)

Störprobe **nur im Speicher**: `faltenplan.py` importiert, `faltenplan()` und `rd.raster()` auf
veränderten Kopien der eingefrorenen `messgroessen.json` aufgerufen, `main()` nie.
`faltenplan.json` vorher = nachher `0e54ac5c`.

| | Frage | Antwort |
|---|---|---|
| **C1** | Welche Felder, wer liest? | Vier je Bot. `max_tage` → `faltenplan.py:272` und G8. `median_balken` → `registerdaten.py:231`. `median_tage` und `n_positionen` → **kein Leser** (Probe P3: 0 Blätter bewegt). Zusätzlich liest `test_faltenplan_neun.py:346` die CSV **direkt** (D4, `tage_p90`) |
| **C2** | `max_tage` → `purge_tage` → was? | Probe P1 (+400 Tage, alle Bots): **95 Blätter**, genau `purge_tage` (9), `embargo_tage` (9), `falten[*]/training_bis_ausschliesslich` (77). **0** × `von`, `bis_ausschliesslich`, `name`, `rolle`, `faltenlaenge_jahre`, `erste_falte`. ⇒ **nur der Rand, keine Faltengrenze.** `training_bis_ausschliesslich` hat im Code **0 Leser**. `benchmark.py` liest kein Purge-Feld ⇒ **die Benchmark-Tabelle hängt nicht an `purge_tage`**, wohl aber der Inhalt von `faltenplan.json`, der Registerbericht (`registerbericht.py:147`) und G8/G9 |
| **C3** | `median_balken` — wer sonst? | **Genau ein Leser:** `registerdaten.py:231` → Untergrenze von `donchian_period` bei `turtle_soup_crypto` und `turtle_soup_stocks`. Probe P2 (×3): Faltenplan 0 Blätter, **Raster 7 Blätter**, nur diese Achse, Zellenzahl gleich (4 Stufen bleiben 4). Weiter über `auswertung.gitterachsen` in die Zellnamen. ⚠️ **Abweichung zur Vormessung:** G8 prüft **nicht** `median_balken`, sondern `purge_tage >= max_tage` (`test_vorregistrierung.py:614–615`) |
| **C4** | Ein Weg ausser 5.4 und Purge? | **In den Faltenplan: kein dritter Eingang gefunden.** Aus `tb24_haltedauern/` öffnet `faltenplan()` nur die neun `*_alle_trades.csv` (Z. 133) und mittelbar `messgroessen.json`; `positionen.csv`, `meta.json` und die zwei Leser in `faltenplan_neun/` werden nicht berührt. **Gefunden wurde eine Verzweigung von Weg 1:** Die Faltenlänge geht auch als Argument in `erste_falte(bot, laenge, …)` (Z. 302), bestimmt also die erste Falte mit. **Und ausserhalb des Faltenplans Weg 3:** `median_balken` → Donchian-Achse (C3) |

⛔ Gemeldet sind nur Feldnamen, Anzahlen und Codestellen (27.2). Keine Haltedauer-, Trade- oder
Purge-Zahl ist genannt.

## 4. Abgabe — D1

| | |
|---|---|
| Hashes | 9 Einzeldateien, Listing beider `ergebnisse/`-Ordner, Summenhash über 1528 versionierte Dateien ausserhalb `docs/`, Snapshot-Summenhash: **vorher = nachher** (`b_hashes_vorher.txt`, `b_hashes_nachher.txt`, `b_hashes.txt`). Die Nachher-Messung lief **nach** dem letzten Lauf (Z3) |
| `git status` ausserhalb `docs/` | leer, vorher und nachher |
| `ergebnisse/` | nichts neu; alle Ausgaben lagen im Scratchpad |
| Sonde gegen `sperrliste_abbild_2026-09-23.json` | vorher = nachher (ohne Kopfzeile zeichengleich), rc 2 aus den Regel-Bestandteilen, 15 Pfad-Bestandteile mit 0, wie in TB-98 (`d1_sonde_*.txt`) |
| Abbruchkriterien 1–3 | nicht ausgelöst. Kriterium 4 (B1 bricht ab) ist eingetreten; Block C ist trotzdem ausgeführt |

## 5. Für Fable — ohne Kontext lesbar ⭐⭐

*Bezug: deine Antworten 23d (jede Eingabe des Laufs muss aus dem registrierten Snapshot
reproduzierbar sein) und 23e (Nachweis für `messgroessen.json` im Selektionsmodus, zweimal
bytegleich, rund elf Sekunden). Sichtschutz 27.1 gewahrt: keine Haltedauer- und keine
Trade-Zahl.*

**Läuft der Nachweis aus 23e im Modus? — Nein. In einer Lesart bricht er ab, in der anderen
läuft er, liest aber aus dem Repo.**

`messgroessen.py` kennt den Selektionsmodus der Bots nicht. Es importiert `shared/paths.py`
nicht. Sein einziger Schalter ist `TB30A_BASE_DIR`, und der ist als Ersatz für die
**Repo-Wurzel** gebaut (für Mutationsproben), nicht für den Snapshot.

1. **Mit `TB30A_BASE_DIR` auf den Snapshot:** Abbruch nach 1 s, weil
   `haltedauern_je_bot.csv` im Snapshot fehlt. Ergänzt man sie, folgt der nächste Abbruch: Der
   Snapshot ist flach, das Skript sucht `data/`.
2. **Mit den Modus-Variablen der Bots (`TB_SELEKTIONSWURZEL` usw.):** rc 0, **bytegleich** zum
   Nachweis vom 23.09., und **jede einzelne Eingabe kommt aus dem Repo**, keine aus dem Snapshot.
   Bytegleich ist das nur, weil `data/` heute zufällig dem Snapshot gleicht (222/222 gemessen).
   ⚠️ **Das ist der Fall „richtiges Ergebnis, falscher Ort“** aus TB-98, hier in reiner Form.
3. **Der Inhalt selbst trägt:** Mit dem Snapshot-Inhalt in der Repo-Anordnung und der
   Haltedauer-Datei aus dem Repo gibt es zweimal bytegleich. Einzige Eingabe von ausserhalb des
   Snapshots bleibt `haltedauern_je_bot.csv`.

⚠️ **Drei Anordnungen, keine passt zur anderen:** Der Snapshot hat Kurse flach und
Universumsdateien unter `config/`. `shared/paths.py` erwartet beides flach (TB-98 Befund 1).
`messgroessen.py` erwartet Kurse unter `data/` und Universumsdateien unter `config/`.

**Die Kette, die an `haltedauern_je_bot.csv` hängt:**

```
Erzeuger (positionen_holen.py)
 ├─ <bot>_alle_trades.csv  (gefundene Trades)
 │    └─> Faltenlänge (5.4) ──> Faltengrenzen UND erste Falte ──> Benchmark-Tabelle
 └─ <bot>_positionen.csv   (ausgeführte Trades – hängen am Positionslimit)
      └─> tb24_haltedauern/auswertung.py  (fester Ausgabepfad, kein --ziel)
           └─> haltedauern_je_bot.csv  (78e2bc6, NICHT im Snapshot)
                └─> messgroessen.py ──> messgroessen.json (eingefroren)
                     ├─ max_tage ──────> purge_tage ──> Purge/Embargo/Trainingsende
                     │                   (KEINE Faltengrenze; Inhalt und Hash von faltenplan.json)
                     └─ median_balken ─> Untergrenze donchian_period
                                         (turtle_soup_crypto, turtle_soup_stocks – Raster)
```

**Fragen:**

1. **Welcher Modus ist gemeint?** Soll der Nachweis aus 23e unter `TB30A_BASE_DIR` laufen, dann
   braucht es einen Snapshot in Repo-Anordnung oder ein Skript, das die flache Anordnung liest.
   Oder soll `messgroessen.py` auf den Resolver in `shared/paths.py` umgestellt werden, damit die
   Modus-Variablen der Bots wirken? Bis das entschieden ist, beweist ein „bytegleich“ aus Lauf 2
   nichts über den Snapshot.
2. **Ist `haltedauern_je_bot.csv` nach 23d eine Eingabedatei, die neu erzeugt werden muss?**
   Gemessene Fakten dazu: Sie ist die einzige Eingabe ausserhalb des Snapshots. Sie entsteht aus
   den **ausgeführten** Trades, also aus derselben Kennzeichnungsstufe, an der der Erzeuger seit
   TB-26 scheitert (TB-98 Befund 2). Ihr Erzeuger `auswertung.py` schreibt noch fest und ohne
   Sperre nach 36.1. Wird sie neu erzeugt, bewegen sich `messgroessen.json` (eingefroren),
   Inhalt und Hash von `faltenplan.json` sowie die Donchian-Untergrenze zweier Bots. Die
   Faltengrenzen und die Benchmark-Tabelle bewegen sich dadurch **nicht**.
3. **Ist die Mischung beabsichtigt?** Die Faltenlänge zählt ausdrücklich die gefundenen Trades,
   *„eine Faltenlaenge, die vom Positionslimit abhinge, waere keine Festlegung vor dem Lauf“*
   (`faltenplan.py:129–130`). Purge und Donchian-Untergrenze ruhen dagegen auf den
   **ausgeführten** Trades. Die hängen am Positionslimit, das im Raster eine Achse ist.

## 6. Abweichungen vom Auftrag

| | |
|---|---|
| Zusatzproben Z1–Z3 | Nicht bestellt. Nach dem Abbruch aus B1 war sonst nicht zu klären, ob dahinter noch etwas liegt (Z1), ob der Snapshot-Inhalt trägt (Z2) und ob der Modus der Bots greift (Z3). Alle nur im Scratchpad |
| C3-Vormessung | „G8 prüft `median_balken`“ ist widerlegt, G8 prüft `max_tage` (A6, C3) |
| B2 „diff gegen B1“ | nicht möglich, weil B1 keine Datei schrieb. Stattdessen gegen Z2 und Z3 verglichen: bytegleich |
| Belegdateien | zusätzlich zu den bestellten: `b_hashes_vorher/nachher.txt`, `d1_sonde_*.txt`, `c_stoerprobe_lauf.txt` und die Skripte (`lauf.sh`, `lesequellen.py`, `hashes.sh`, `c_lauf.sh`, `c_stoerprobe.py`, `belege_sammeln.sh`). `rm` ist gesperrt, deshalb liegen die Vorher/Nachher-Einzeldateien neben `b_hashes.txt` |
| Handwerk | Ein direkter Einzeiler mit `env PYTHONPATH=…` wurde abgelehnt (wie in TB-98). Als Skriptdatei (`c_lauf.sh`) ging er |

## 7. Was NICHT geschah

Nichts nach `ergebnisse/` geschrieben. `messgroessen.py`, `registerdaten.py`,
`faltenplan.py` und `auswertung.py` sind nicht geändert. Kein Registertext, keine Rasterachse,
keine Tatsachennotiz. `python3 faltenplan.py` wurde nie ausgeführt. Kein Snapshot-Hilfsbaum
liegt im Repo. Es ist keine Zahl der Selektionsseite gemeldet.

## 8. Für die Folgesitzung vorbereitet

- **TB-100 (Pfadkonstante):** Die Ausgaben von TB-24 haben jetzt **fünf** Leser mit eigenem
  Pfad: `faltenplan.py:121`, `faltenplan_neun.py:207`, `embargo_neun.py:68`,
  `messgroessen.py:207` und `test_faltenplan_neun.py:346`. Die Konstante muss alle treffen, die
  zu den neu erzeugten Listen gehören, und dazu `tb24_haltedauern/auswertung.py`, das zwischen
  Listen und `haltedauern_je_bot.csv` steht (fest, ohne `--ziel`).
- **TB-101 (Abbild des Faltenplans):** Der Hash von `faltenplan.json` hängt über `purge_tage` an
  `messgroessen.json`, also an `haltedauern_je_bot.csv`. Ein Abbild vor der Entscheidung zu
  Frage 2 würde einen Wert einfrieren, der sich mit 40.6 ändert.
- **Randbefund:** Schon der Import von `registerdaten.py` (Z. 62, `from manual_close import
  allokation`) öffnet `logs/notifications/manuelle_eingriffe.log` im Anhängemodus
  (`RotatingFileHandler`, `notifications/manual_close.py:242`). Geschrieben wurde nichts
  (1204 B, mtime 11.09.). Aber jede Mess- und Testsitzung hält damit das Betriebsprotokoll der
  manuellen Eingriffe offen.
- **Handwerk:** `docs/belege/TB-102/lauf.sh` kennt die Arten `ohne`, `modus`, `basis` und
  `selektion`, und `lesequellen.py` löst Verknüpfungen auf und markiert fehlgeschlagene
  Öffnungsversuche. Beides ist für den nächsten Nachweis wiederverwendbar.

## In einfacher Sprache

Der Verfahrensprüfer wollte sehen, dass sich eine eingefrorene Messdatei aus dem eingefrorenen
Datenbestand genau wiederherstellen lässt, und zwar im geschützten Modus, in dem auch der
spätere Lauf rechnet.

Das Ergebnis hat zwei Seiten. Stellt man das Messprogramm auf den eingefrorenen Bestand um,
bricht es sofort ab. Ihm fehlt eine Auswertungsdatei, die nie eingefroren wurde. Dahinter käme
es auch an den Kursdaten nicht vorbei, weil sie dort anders abgelegt sind, als es erwartet.
Schaltet man dagegen den Modus ein, den die Handelsprogramme benutzen, läuft es ohne Fehler und
liefert genau die richtige Datei. Es hat aber kein einziges Byte aus dem eingefrorenen Bestand
gelesen, sondern alles aus dem laufenden Arbeitsordner. Das Ergebnis stimmt heute nur, weil
beide Bestände gerade gleich sind.

Die Datei, die fehlt, hat Folgen. Sie legt fest, wie breit der Sicherheitsabstand vor jedem
Prüfzeitraum ist und wo die untere Grenze eines Suchbereichs für zwei Programme liegt. Die
Prüfzeiträume selbst und die Vergleichstabelle verschiebt sie nicht.
