# TB-93 — `messgroessen.py` nach 36.1 absichern: **Block A ist vorgemessen, du misst nach und führst den Determinismusnachweis**

**Grundlage:** Fable, Antwort **23c**, Abschnitt 2 — Entscheidung: **ändern**, vor
dem Tag, mit Freigabe und Tatsachennotiz nach 37.3.
**Vorbereitet:** 23.09.2026 vom steuernden Chat · **Messstand:** HEAD `02f2574`

⭐ **Dieser Auftrag hängt NICHT an Anfrage 23e.** Der `auswertung.py`-Konflikt
betrifft Punkt 8 (TB-92), nicht diesen.

---

## 0. Der Anlass, in zwei Sätzen

`messgroessen.py` schrieb **fest verdrahtet** nach `ergebnisse/messgroessen.json`
— ohne Schalter, ohne Sperre. ⭐ Fable hat entschieden, dass 36.1 für **jeden**
Erzeuger gilt, und präzisiert: *„gesperrt" umfasst jeden Pfad, dessen Hash am Tag
bezeugt wird — auch die Einträge von `herkunft.py::EINGEFROREN`.*

> **Wörtlich, 23c:** *„Den Aufruf zu sperren und die Datei stehen zu lassen wäre
> (c) aus 22b: eine Regel, die niemand ausführt."*

---

## 1. ⭐⭐ Was der steuernde Chat vorgemessen hat

⚠️ **Vormessung in der Brücken-VM, nicht mit `trading-env`** (`A8`). **Du misst
jede Zahl nach.** Weicht etwas ab, **gilt deine Messung**.

**Der Arbeitsbaum trägt die Änderung uncommittet:** `research/vorregistrierung/messgroessen.py`, `numstat 66 6`.
**Beleg:** `docs/belege/TB-93/vormessung_absicherung_messgroessen.txt` (155 Zeilen).

### ⭐ Fables Unsicherheit aus 23c ist beantwortet

> *„Unsicher: ob `messgroessen.py` ausser `ergebnisse/messgroessen.json` weitere
> Dateien schreibt (dann gilt die Sperre für jede)."*

**Gemessen, per AST über das ganze Modul:** `open()` bei Z. 88 (lesend) und
Z. 283 (schreibend); **ein** `json.dump`; kein `to_csv`, kein `os.open`, kein
`write_text`. ⇒ ⭐ **Genau ein Schreibziel.**

### Die sechs Nachmessungen

| | zu prüfen | Vormessung sagt |
|---|---|---|
| **A-N1** | Hash `messgroessen.py` | `5f7075003c9dc291…` → **neuer Hash messen** |
| **A-N2** | ⭐⭐ AST-Vergleich der **acht** Messfunktionen | `universum`, `lies`, `rsi`, `adx`, `rma`, `je_zeitrahmen`, `haltedauern`, `datenbereiche` — **alle acht gleich** |
| **A-N3** | `json.dump`-Aufruf per AST | **zeichengleich**, nur Zeilennummer wandert (284 → 288). ⚠️ Ein `grep` auf `indent=2` meldet **2** statt 1 — der zweite steht im neuen Docstring |
| **A-N4** | Mutationsprobe auf den eingefrorenen Pfad | Abbruch `rc=1` **vor der Rechnung**, Datei byte-gleich, `ergebnisse/` bleibt bei 13 |
| **A-N5** | 36.1 (3) Voreinstellung | `messgroessen_<UTC-Stempel>.json`, **nicht** `messgroessen.json` |
| **A-N6** | ⭐ Erschien beim Ändern ein Genehmigungsdialog? | ⛔ **in der VM nicht messbar** — dort gilt `ask` nicht. *Dieselbe Lücke wie TB-91 A-N6; sie schliesst sich nur auf dem Mac* |

⚠️ **Für A-N2 stellst du den Vorher-Stand selbst her:**
`git show HEAD:research/vorregistrierung/messgroessen.py > /tmp/messgroessen_vorher.py`

---

## 2. Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt** — nicht verwerfen. Dort liegen ausser
`messgroessen.py` auch `ARBEITSWEISE.md` (Abschnitt 16), die Anfragen 23d/23e,
Fables Antwort 23c, TB-92, TB-93 und die Belege.

⭐ Prüfe auf verwaiste git-Sperrdateien im Scratchpad (TB-91 fand zwei).

---

## 3. Block B ⭐⭐⭐ — der Determinismusnachweis

**Das ist der Kern dieses Auftrags.** Fable, 23c, wörtlich:

> *„ein Lauf mit `--ziel` auf einen neuen Pfad reproduziert
> `ergebnisse/messgroessen.json` **bytegleich** — sonst Befund und Stopp."*

| | |
|---|---|
| **B1** | Hashes **vorher**: `ergebnisse/messgroessen.json`, Dateizahl in `ergebnisse/` |
| **B2** | `python3 messgroessen.py --ziel ergebnisse/messgroessen_<datum>_nachweis.json` — mit `trading-env`. ⚠️ Der Lauf dauert; nicht abbrechen |
| **B3** | ⭐⭐ **Bytevergleich** der neuen Datei gegen `ergebnisse/messgroessen.json`: `cmp` oder Hashvergleich |
| **B4** | **Bytegleich** → Nachweis erbracht. **Nicht bytegleich** → ⛔ **BEFUND UND STOPP.** Melde die erste abweichende Stelle und *was* sich unterscheidet (Schlüssel, Wert). ⛔ Nichts nachbessern |
| **B5** | Die alte Datei bleibt **unverändert** — Hash nachher gleich Hash vorher |

⚠️⚠️ **Wenn B4 einen Befund ergibt, ist das kein Scheitern.** Es hiesse, dass die
Messgrössen nicht reproduzierbar sind — und **das wäre vor dem Tag zu wissen die
wertvollste Auskunft dieses Auftrags.** Melden, nicht reparieren.

## 4. Block C — Tatsachennotiz und was mitwandert

| | |
|---|---|
| **C1** | Tatsachennotiz nach **37.3** mit **altem und neuem Hash** von `messgroessen.py` |
| **C2** | ⚠️ `messgroessen.py` steht **selbst** in `herkunft.py::EINGEFROREN` (Z. 59) ⇒ der Register-Gesamthash in `herkunft.json` wandert mit. ⭐ Fable: *„planmässig, vor dem Tag, benannt"* — also **benennen**, nicht verstecken |
| **C3** | Sondenlauf (lesend) vorher/nachher. ⭐ Erwartung nach Fables Auslegung aus 23c: Die Abschnitt-0-Gruppe meldet `messgroessen.py` als Abweichung — **ein** Übergang, **eine** Notiz |
| **C4** | ⛔ **Kein** neues Abbild. Der Befund bleibt sichtbar, bis 37.3 ihn am Tag schliesst |

---

## 5. ⛔ Was NICHT geschieht

- ⛔ **`ergebnisse/messgroessen.json` wird nicht ersetzt, nicht gelöscht, nicht angefasst.** Die Nachweisdatei liegt **daneben**
- ⛔ **Keine** Änderung an den acht Messfunktionen, am Ausgabeformat, an `GEBUEHR_PCT` — ⭐ Fable 23c: *„Mein Satz aus 22h galt `GEBUEHR_PCT` … Er gilt weiter für den Wert; für den Schreibpfad gilt 36.1"*
- ⛔ **Nichts** aus Punkt 8 / TB-92 — der wartet auf 23e
- ⛔ **Keine** Sonde „Schreibziele" — das ist ein eigener Auftrag

## 6. ⛔ Abbruchkriterien

| | |
|---|---|
| **1** | Der Arbeitsbaum ist nach Schritt 0 nicht leer |
| **2** | Eine der acht Messfunktionen weicht im AST ab |
| **3** | Der `json.dump`-Aufruf ist nicht zeichengleich |
| **4** | Die Mutationsprobe schreibt doch, oder gibt nicht `1` zurück |
| **5** | ⭐ Block B ist **kein** Abbruchkriterium — ein Befund dort wird **gemeldet**, und C entfällt |

---

## In einfacher Sprache

Das Programm, das die Messgrössen berechnet, konnte eine geschützte Datei bei
jedem Aufruf überschreiben — und hatte nicht einmal die Möglichkeit, woanders
hinzuschreiben. Der Verfahrensprüfer hat entschieden, dass es abgesichert wird,
mit denselben Nachweisen wie beim Vergleichsrechner.

**Die Absicherung selbst ist schon gemacht** und liegt im Arbeitsverzeichnis. Sie
war ohne die besondere Programmumgebung möglich, weil dabei nur Quelltext
geändert und nichts gerechnet wird. Deine Aufgabe ist es, sechs Punkte
nachzuprüfen — alle mit vorgerechnetem Vergleichswert.

**Die eigentliche Arbeit ist eine andere:** Das Programm soll einmal laufen und
dabei die alte Datei **Byte für Byte** wiederholen. Gelingt das, ist bewiesen,
dass die Messgrössen reproduzierbar sind. Gelingt es nicht, ist das ein Fund —
und zwar ein wichtiger, der vor dem Stichtag auf den Tisch gehört. In dem Fall
gilt: melden, nicht in Ordnung bringen.
