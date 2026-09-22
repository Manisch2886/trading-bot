# TB-86 — Schritt 2 von Fables Reihenfolge: `faltenplan.py main()` absichern

**Sitzungstitel:** `TB-86 faltenplan main() — Zielpfad und Einmal-Schreibsperre`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**Erstellt:** 22.09.2026, 09:40 Ortszeit · **Vorgänger:** TB-85
**Erwarteter Ausgangsstand:** `HEAD` = `origin/main`, nach der Abgabe von TB-85

⭐⭐ **BETREIBERFREIGABE LIEGT VOR:** 22.09.2026, 07:50 — für **Schritt 1 und 2**
von Fables Reihenfolge (36.3). ⚠️ **Dieser Auftrag ist Schritt 2.**

⛔⛔ **VORBEDINGUNG:** TB-85 muss **abgegeben** sein, und die Sperrlisten-Sonde
muss laufen. Ist sie nicht da: **ABBRUCH**, der Auftrag ist zu früh.

---

## 0. Der Anlass, in einem Satz

⚠️⚠️ **`faltenplan.py main()` schreibt heute fest verdrahtet nach
`ergebnisse/faltenplan.json` — Sperrlistenpunkt 2 (`0e54ac5c…`).** Ein einziges
`python3 faltenplan.py` zerstört die gesperrte Datei. Sie hält seit dem 14.09.
nur deshalb, weil niemand den Befehl getippt hat.

**Gemessen (22.09., HEAD `082c7b1`), `faltenplan.py` Zeilen 372–377:**

```python
    ziel = os.path.join(_HIER, "ergebnisse", "faltenplan.json")
    with open(ziel, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    print(f"\nGeschrieben: {ziel}")
    return 0
```

⭐ **Kein `argparse`, kein `sys.argv`** — `main()` hat heute keinerlei Schalter,
und sie gibt **immer `0`** zurück.

---

## 1. Was zu tun ist — Registertext 36.1 (3) und (4)

**Fable, zeichengleich:**

> **(3)** Ein anderes Ziel nur durch ausdrückliches Argument; die Voreinstellung eines Erzeugers ist nie ein Pfad, der auf der Sperrliste steht. **(4)** Für `faltenplan.py main()`: Voreinstellung weg von `ergebnisse/faltenplan.json` (Sperrlistenpunkt 2) auf einen nicht gesperrten Pfad, und die Einmal-Schreibsperre nach (2). Beides vor jeder weiteren Änderung an `faltenplan.py`, insbesondere vor Z. 336.

### 1a — Die neue Voreinstellung

⭐ **Handwerksvorschlag des steuernden Chats** (36.6 nennt Name und Form
ausdrücklich Handwerk — ⚠️ **du darfst abweichen, musst es dann aber begründen
und melden**):

```
ergebnisse/faltenplan_<JJJJ-MM-TT-HHMMSS>.json     (UTC)
```

⭐⭐ **Warum ein Zeitstempel und kein fester Name:** Die Einmal-Schreibsperre aus
36.1 (2) bricht ab, sobald die Zieldatei existiert. Bei einem **festen**
Voreinstellungsnamen liesse sich `main()` nach dem ersten Lauf **nie wieder**
aufrufen — die Sperre würde das Werkzeug unbrauchbar machen statt es zu
schützen. Mit Zeitstempel ist jeder Lauf ein neuer Name, die Sperre greift nie
versehentlich, **und der gesperrte Pfad ist nur noch über `--ziel` erreichbar —
wo die Sperre dann genau richtig zuschlägt.**

### 1b — Die Einmal-Schreibsperre (36.1 (2), zeichengleich)

> Jeder Erzeuger einer solchen Datei schreibt **einmalig**: Existiert die Zieldatei bereits, bricht er ab (Rückgabewert ≠ 0), nennt Pfad und Hash der vorhandenen Datei und schreibt nichts. Er überschreibt nie, auch nicht mit identischem Inhalt.

⚠️ **Berichtigt durch 36.5** (Fable 22c, zeichengleich): *„Der Erzeuger, der
wegen vorhandener Zieldatei nicht schreibt, endet mit **1** — er hat geprüft und
einen Befund. Nicht mit 2: Er konnte prüfen."*

⇒ **Die Rückgabewerte von `main()` nach dem Umbau:**

| Wert | Fall |
|---:|---|
| **0** | geschrieben, Ziel existierte nicht |
| **1** | ⭐ **Ziel existiert** — Pfad **und Hash** genannt, nichts geschrieben |
| **2** | nicht prüfbar (Zielordner fehlt, Pfad nicht lesbar, Plan nicht berechenbar) |

⛔ **Kein Inhaltsvergleich.** Fable, zeichengleich: *„Eine Sperre, die bei
gleichem Inhalt durchlässt, muss den Inhalt vergleichen — und wer den Vergleich
programmiert, entscheidet, was ‚gleich' heisst … **Die Sperre ist stärker, wenn
sie dümmer ist.**"*

### 1c — `--ziel`

```
python3 faltenplan.py [--ziel <pfad>]
```

⚠️ **Auch mit `--ziel` gilt die Sperre.** Ein ausdrückliches Argument erlaubt
einen **anderen** Pfad, **nicht** das Überschreiben.

---

## 2. ⛔ Was NICHT geändert wird

| ⛔ | |
|---|---|
| ⛔⛔ | **Zeile 336** (`bestaetigungsperiode`) — das ist **Schritt 3**, ein eigener Auftrag mit eigener Freigabe. ⚠️ Fable: *„Wer Schritt 3 vor Schritt 2 macht, hat genau den Fall, den ihr beschreibt."* |
| ⛔ | **Die Rechenlogik** — `_plan`, `erste_falte_4a`, Bedingung (i), alles oberhalb von `main()`. ⚠️ **Eine einzige geänderte Zahl im Plan wäre ein Abbruchgrund** |
| ⛔ | **Die Konsolenausgabe** in `main()` (Z. 361–371) — sie bleibt zeichengleich |
| ⛔ | `auswertung.py`, `herkunft.py`, `benchmark.py`, `registerdaten.py` |
| ⛔ | **Das Register** — dieser Auftrag trägt keinen Registertext ein |

---

## 3. ⭐⭐ Die Mutationsprobe (Fables Schritt 2, wörtlich)

> *„**Mutationsprobe:** `main()` gegen eine Kopie von `faltenplan.json` am neuen Zielpfad aufrufen → muss abbrechen; Sonde danach → grün."*

**Der Ablauf, genau so:**

| # | Tun | erwartet |
|---:|---|---|
| **M1** | `main()` ohne Argumente | ⭐ schreibt nach `faltenplan_<stempel>.json`, **Rückgabe 0** |
| **M2** | **Dieselbe** Datei als `--ziel` erneut angeben | ⭐⭐ **Rückgabe 1**, Pfad **und Hash** in der Ausgabe, Datei **byteweise unverändert** (Hash vorher/nachher gleich) |
| **M3** | ⚠️⚠️ **`--ziel` auf eine KOPIE** von `faltenplan.json` an einem nicht gesperrten Ort | ⭐ **Rückgabe 1** — genau Fables Fall |
| **M4** | ⛔⛔ **`--ziel ergebnisse/faltenplan.json`** (der echte gesperrte Pfad) | ⭐⭐ **Rückgabe 1**, und ⚠️ **der Hash `0e54ac5c…` ist nachher unverändert** — das ist der eigentliche Beweis |
| **M5** | Sperrlisten-Sonde nach allen vier Proben | ⭐ **derselbe Rückgabewert wie beim Nullpunkt in TB-85** |

⚠️ **M4 ist der Kern dieses Auftrags.** Er ist der einzige Test, der den echten
gesperrten Pfad berührt — ⛔ **und er darf ihn nicht verändern.** Miss den Hash
unmittelbar vorher und unmittelbar nachher.

⚠️ **Zusätzlich, Gegenprobe gegen den Ausgangszustand:** Belege durch einen Blick
in den Diff, dass **kein Plan-Wert** sich geändert hat — `main()` vor und nach
dem Umbau muss denselben Plan drucken (Konsolenausgabe vergleichen).

---

## 4. ⛔ Abbruchkriterien

| # | Wenn … | dann |
|---:|---|---|
| **1** | ⚠️⚠️ `ergebnisse/faltenplan.json` hat nach irgendeinem Schritt **nicht** `0e54ac5c…` | ⛔⛔ **SOFORT ABBRUCH.** Nichts committen, **nichts reparieren**, nur melden (36.2) |
| **2** | Die Sperrlisten-Sonde aus TB-85 fehlt oder läuft nicht | ⛔ ABBRUCH — Vorbedingung verletzt |
| **3** | M2, M3 oder M4 endet **nicht** mit `1` | ⛔ ABBRUCH — die Sperre greift nicht |
| **4** | Die Konsolenausgabe von `main()` unterscheidet sich vor/nach dem Umbau in **irgendeiner Planzahl** | ⛔ ABBRUCH — du hast mehr geändert als den Schreibteil |
| **5** | Du müsstest Zeile 336 oder die Rechenlogik anfassen | ⛔ ABBRUCH |
| **6** | Ein anderer Sperrlisten-Hash ändert sich (`a163c498…`, `4549395f…`) | ⛔ ABBRUCH |

---

## 5. Schritte

| # | Tun | Nachweis |
|---:|---|---|
| **0** | Schlüsselbund, Arbeitsbaum sauber, **drei Hashes vorher** | `schritt0_hashes_vorher.txt` |
| **1** | **Konsolenausgabe von `main()` VOR dem Umbau festhalten** — ⚠️ **mit `--ziel` auf einen Wegwerfpfad**, damit nichts Gesperrtes berührt wird. ⛔ **Nicht ohne Argument aufrufen!** | `schritt1_ausgabe_vorher.txt` |
| **2** | `argparse` und `--ziel` einbauen, Voreinstellung mit Zeitstempel (1a) | Commit |
| **3** | Einmal-Schreibsperre mit Hash-Meldung (1b), Rückgabewerte 0/1/2 | Commit |
| **4** | **M1–M5** durchführen | `schritt4_mutationsprobe.txt`, je Probe Befehl + Rückgabewert + Hash |
| **5** | **Konsolenausgabe NACH dem Umbau** und Vergleich mit Schritt 1 | `schritt5_ausgabe_vergleich.txt`, 0 Abweichungen |
| **6** | **Drei Hashes nachher** | `schritt6_hashes_nachher.txt` |
| **7** | `git diff` auf `faltenplan.py` — ⚠️ **nur `main()` und die Importzeile dürfen vorkommen** | Abschlussbeleg |
| **8** | **Sperrlisten-Sonde** laufen lassen | `schritt8_sonde.txt` |
| **9** | **`AKTUELLER_AUFTRAG.md`** — nur lesen | `grep -c "TB-86"` ≥ 1 |
| **10** | **Journalblock** und `docs/auftraege/ERGEBNIS_TB-86.md` | Commit |
| **11** | **Abgabe**: Status leer, `numstat` nachgetragen | Abschlussbeleg |

---

## 6. Ins Ergebnisdokument

1. Der Diff von `main()` — **vollständig**, er ist klein genug
2. **M1–M5** mit Befehl, Rückgabewert und Hash je Probe
3. ⚠️ **M4 hervorgehoben**: der gesperrte Pfad wurde angesprochen und ist
   **unverändert**
4. Der **Ausgabevergleich** vor/nach (Schritt 5) — 0 Abweichungen
5. Die **drei Hashes** vorher und nachher
6. ⭐ **Was NICHT getan wurde:** Zeile 336 unberührt, Rechenlogik unberührt,
   kein Registereintrag, keine andere Datei angefasst
7. ⚠️ **Der nächste Schritt, benannt:** Schritt 3 (Zeile 336, Bezeichner der
   Bestätigungsperiode nach 35.1) — ⛔ **braucht eine eigene Betreiberfreigabe**

---

## In einfacher Sprache

Das ist die Reparatur der Falle, die gestern gemeldet wurde.

Ein Programm im Projekt erzeugt den Auswertungsplan — und schreibt dabei
**immer** in dieselbe Datei, die eigentlich unveränderlich sein soll. Bisher ist
nichts passiert, weil niemand es gestartet hat. Das reicht nicht.

Zwei Änderungen, beide klein:

**Erstens** schreibt das Programm künftig standardmäßig in eine Datei mit
Zeitstempel im Namen — also jedes Mal in eine neue. Die geschützte Datei ist nur
noch erreichbar, wenn jemand sie ausdrücklich angibt.

**Zweitens** bekommt es eine Sperre: **Existiert die Zieldatei schon, schreibt es
gar nichts** und meldet stattdessen, was dort liegt. Auch dann, wenn der Inhalt
derselbe wäre — Fables Begründung: *„Die Sperre ist stärker, wenn sie dümmer
ist."*

⭐ **Der wichtigste Test:** Das Programm wird absichtlich auf die geschützte
Datei angesetzt — und muss sich weigern. Ihre Prüfsumme wird unmittelbar davor
und danach gemessen. Ändert sie sich, bricht die Sitzung sofort ab und
**repariert nichts**, sondern meldet nur.

⛔ **Was ausdrücklich nicht passiert:** Die Rechenregeln werden nicht angefasst.
Keine einzige Zahl im Plan darf sich bewegen — das wird durch einen Vergleich
der Bildschirmausgabe vorher und nachher belegt.
