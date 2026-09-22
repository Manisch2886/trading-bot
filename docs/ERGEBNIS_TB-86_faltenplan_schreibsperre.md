# TB-86 — `faltenplan.py main()`: Zielpfad und Einmal-Schreibsperre

**Sitzung:** Mac, 22.09.2026 · **Auftrag:** `docs/auftraege/MAC_TB-86_faltenplan_schreibsperre.md`
**Vorgänger:** TB-85 · **Ausgangsstand:** `2144825` · **Betreiberfreigabe:** 22.09.2026, 07:50 (Schritt 1 und 2 von Fables Reihenfolge 36.3)
**Belege:** `docs/belege/TB-86/`

> ⚠️ **Ablageort:** Der Auftrag nennt `docs/auftraege/ERGEBNIS_TB-86.md`. Dieses
> Dokument liegt unter `docs/` und heisst wie die Reihe seit TB-80
> (`ERGEBNIS_TB-<nr>_<thema>.md`). Wie in TB-85 wird die Abweichung hier
> vermerkt statt stillschweigend vollzogen.

> ⚠️ **Die Sitzung wurde durch einen Verbindungsabbruch geteilt.** Teil 2 hat
> vor allem anderen den Stand nachgemessen: Commit `4daa254`, die sechs Belege,
> M1–M4 bestanden, `faltenplan.json` unverändert `0e54ac5c…`. Erst danach
> Schritt 9 bis 11.

---

## 1. Der Anlass in einem Satz

`faltenplan.py main()` schrieb fest verdrahtet nach
`ergebnisse/faltenplan.json` — **Sperrlistenpunkt 2**. Ein einziges
`python3 faltenplan.py` hätte die gesperrte Datei überschrieben. Sie hielt seit
dem 14.09. nur deshalb, weil niemand den Befehl getippt hat. **Das ist jetzt
repariert.**

---

## 2. Der Diff von `main()` — vollständig

Commit `4daa254`, `research/vorregistrierung/faltenplan.py`, **100 Zeilen
hinzugefügt, 10 entfernt**, eine einzige Datei.

### 2a — Der Importblock

```diff
+import argparse
+import hashlib
 import json
 import math
 import os
 import sys
-from datetime import date, timedelta
+from datetime import date, datetime, timedelta, timezone
```

### 2b — Drei neue Funktionen vor `main()`

```python
def _sha256_datei(pfad: str) -> str:
    h = hashlib.sha256()
    with open(pfad, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def voreinstellung_ziel() -> str:
    """Das voreingestellte Schreibziel - Registertext 36.1 (3), (4). …"""
    stempel = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")
    return os.path.join(_HIER, "ergebnisse", f"faltenplan_{stempel}.json")


def schreibe_plan(plan: dict, ziel: str):
    """Schreibt den Plan GENAU EINMAL. Liefert (rueckgabewert, text). …

        0   geschrieben, das Ziel existierte nicht
        1   BEFUND: Ziel existiert - Pfad und Hash genannt, nichts geschrieben
        2   NICHT PRUEFBAR: Zielordner fehlt, Ziel nicht anlegbar
    """
    if os.path.exists(ziel):
        try:
            h = _sha256_datei(ziel)
        except OSError:
            h = "(nicht lesbar)"
        return 1, (f"\nABBRUCH (36.1 (2)): Ziel existiert, nichts geschrieben."
                   f"\n  Pfad:    {ziel}\n  SHA-256: {h}")
    ordner = os.path.dirname(os.path.abspath(ziel))
    if not os.path.isdir(ordner):
        return 2, f"\nABBRUCH: Zielordner fehlt: {ordner}"
    try:
        # O_EXCL statt open(..., "w"): faengt auch ein Ziel ab, das zwischen
        # der Pruefung oben und dem Schreiben entsteht.
        fd = os.open(ziel, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return 1, (f"\nABBRUCH (36.1 (2)): Ziel entstand waehrend des Laufs, "
                   f"nichts geschrieben.\n  Pfad:    {ziel}"
                   f"\n  SHA-256: {_sha256_datei(ziel)}")
    except OSError as e:
        return 2, f"\nABBRUCH: Ziel nicht anlegbar: {ziel} ({e})"
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    return 0, f"\nGeschrieben: {ziel}"
```

### 2c — `main()` selbst

```diff
-def main():
-    mess = rd._mess()
-    plan = faltenplan(mess)
+def main(argv=None):
+    z = argparse.ArgumentParser(
+        description="Rechnet den Faltenplan und schreibt ihn einmalig. "
+                    "Voreinstellung ist ein Name mit Zeitstempel (36.1 (3)); "
+                    "ein vorhandenes Ziel wird nie ueberschrieben (36.1 (2)).")
+    z.add_argument("--ziel", default=None, metavar="PFAD",
+                   help="Schreibziel (Standard: ergebnisse/faltenplan_<UTC-Stempel>.json). "
+                        "⚠️ Auch mit --ziel gilt die Sperre: ein ausdrueckliches "
+                        "Argument erlaubt einen ANDEREN Pfad, nicht das Ueberschreiben.")
+    a = z.parse_args(argv)
+    try:
+        mess = rd._mess()
+        plan = faltenplan(mess)
+    except Exception:                       # nicht berechenbar ist 2, nie 0
+        import traceback
+        traceback.print_exc()
+        print("\nABBRUCH: Plan nicht berechenbar - nichts geschrieben.",
+              file=sys.stderr)
+        return 2
     print(__doc__.strip().split("\n")[0])
     …                                       ⛔ die Konsolenausgabe: Kontext, unverändert
-    ziel = os.path.join(_HIER, "ergebnisse", "faltenplan.json")
-    with open(ziel, "w", encoding="utf-8") as f:
-        json.dump(plan, f, indent=2, ensure_ascii=False, sort_keys=True)
-        f.write("\n")
-    print(f"\nGeschrieben: {ziel}")
-    return 0
+    ziel = a.ziel or voreinstellung_ziel()
+    rc, text = schreibe_plan(plan, ziel)
+    print(text, file=sys.stderr if rc else sys.stdout)
+    return rc
```

⭐ **Vorher gab `main()` immer `0` zurück** — auch dann, wenn die Rechnung
geworfen hätte (der Aufruf wäre gar nicht so weit gekommen, aber es gab keinen
Weg, ein „konnte nicht" auszudrücken). Jetzt gibt es drei Ausgänge.

### Warum ein Zeitstempel und kein fester Name

Die Einmal-Schreibsperre bricht ab, sobald die Zieldatei existiert. Bei einem
**festen** Voreinstellungsnamen liesse sich `main()` nach dem ersten Lauf **nie
wieder** aufrufen — die Sperre machte das Werkzeug unbrauchbar, statt es zu
schützen. Mit Zeitstempel ist jeder Lauf ein neuer Name, **und der gesperrte
Pfad ist nur noch über `--ziel` erreichbar, wo die Sperre dann genau richtig
zuschlägt.**

### Warum `O_EXCL` und kein `os.path.exists`

`os.path.exists` steht am Anfang und ist damit ein Wettlauf: Zwischen der
Prüfung und dem `open(..., "w")` kann das Ziel entstehen. `O_EXCL` legt die
Prüfung in denselben Systemaufruf wie das Anlegen. Die `exists`-Prüfung bleibt
trotzdem davor stehen — sie liefert die **Hash-Meldung**, die 36.1 (2) verlangt,
und braucht dafür ohnehin einen Lesezugriff.

---

## 3. M1–M5 — die Mutationsproben

Beleg: `docs/belege/TB-86/schritt4_mutationsprobe.txt` (mit vollständiger
Konsolenausgabe je Probe). Gesperrte Datei zu Beginn: `0e54ac5c…`.

| # | Befehl | rc | erw. | Hash am Ziel |
|---:|---|:---:|:---:|---|
| **M1** | `python3 faltenplan.py` | **0** | 0 | schrieb `ergebnisse/faltenplan_2026-09-22-161505.json`, `2dd28291…` |
| **M2** | `python3 faltenplan.py --ziel …/faltenplan_2026-09-22-161505.json` | **1** | 1 | `2dd28291…` vorher = nachher, 38 684 B = 38 684 B |
| **M3** | `python3 faltenplan.py --ziel <Kopie von faltenplan.json>` | **1** | 1 | `0e54ac5c…` vorher = nachher |
| **M4** | ⛔ `python3 faltenplan.py --ziel ergebnisse/faltenplan.json` | **1** | 1 | `0e54ac5c…` vorher = nachher |
| **M5** | `python3 shared/sperrlistensonde.py --abbild …_2026-09-22.json` | **1** | *2* | ⚠️ siehe 3b |

In M2, M3 und M4 meldete das Werkzeug jeweils:

```
ABBRUCH (36.1 (2)): Ziel existiert, nichts geschrieben.
  Pfad:    …
  SHA-256: …
```

— **Pfad und Hash**, wie 36.1 (2) verlangt, und **kein Inhaltsvergleich**: M2
schrieb nicht, obwohl der Inhalt derselbe gewesen wäre. Fable, zeichengleich:
*„Die Sperre ist stärker, wenn sie dümmer ist."*

### 3a — ⭐⭐ M4: der gesperrte Pfad wurde angesprochen und ist unverändert

Das ist der Kern dieses Auftrags — der einzige Test, der den echten gesperrten
Pfad berührt, und er darf ihn nicht verändern.

| | unmittelbar **vorher** | unmittelbar **nachher** |
|---|---|---|
| SHA-256 | `0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` | **dasselbe** |
| Bytes | 18 736 | **18 736** |
| mtime | `1789401317` = Sep 14 17:55:17 2026 | **`1789401317`** |

⭐ **Die mtime ist der schärfere Beleg als der Hash.** Ein Hash bliebe auch dann
gleich, wenn die Datei geöffnet und mit identischem Inhalt neu geschrieben
worden wäre. Die unveränderte mtime zeigt: **sie wurde nicht einmal zum
Schreiben geöffnet.**

### 3b — ⚠️ M5 weicht von der Erwartung des Auftrags ab — mit Ansage

Der Auftrag erwartet für M5 *„denselben Rückgabewert wie beim Nullpunkt in
TB-85"*, also **2**. Gemessen: **1**, Befund in Punkt 2.

**Das ist kein Fehlschlag, sondern der zweite Pfad von Sperrlistenpunkt 2.**
Punkt 2 nennt zwei Dateien:

| Pfad | Abbild TB-85 | jetzt | |
|---|---|---|---|
| `ergebnisse/faltenplan.json` | `0e54ac5c…` | `0e54ac5c…` | **gleich** |
| `faltenplan.py` | `6f96b95d…` | `fd3e5018…` | ⚠️ **ABWEICHUNG** |

Die Sonde hat eine Änderung an einer gesperrten Datei gefunden und beim Namen
genannt — genau das, wofür sie in TB-85 gebaut wurde. **Dass die Änderung
beauftragt und freigegeben war, kann sie nicht wissen, und sie soll es nicht.**

Inhaltlich schützt Punkt 2 *„Faltengrenzen, Go-Live-Schnitt, Purge-Längen,
Faltenlängen"*. **Keine dieser Grössen hat sich bewegt** (Abschnitt 4).
Geändert wurde allein, **wohin** `main()` schreibt.

Die Bilanz im Vergleich:

| | in Ordnung (0) | Befund (1) | nicht prüfbar (2) | rc |
|---|---:|---:|---:|---:|
| Nullpunkt TB-85 | 2 | 0 | 12 | **2** |
| nach TB-86 | 1 | **1** | 12 | **1** |

Die zwölf nicht prüfbaren Punkte sind unverändert dieselben.

⛔ **Was daraufhin NICHT getan wurde:** das Abbild wurde **nicht** neu erzeugt,
der Hash in der Sperrliste **nicht** nachgezogen, **kein** Registereintrag.
Registertext 36.2: ein Sperrlistenbruch ist *„eine Tatsachennotiz — nie eine
stille Reparatur"*.

---

## 4. Der Ausgabevergleich vor/nach — 0 Abweichungen

Beleg: `docs/belege/TB-86/schritt5_ausgabe_vergleich.txt`.

| | |
|---|---|
| **vorher** | Schritt 1, Stand `2144825`, `main()` über `_HIER` auf einen Wegwerfordner |
| **nachher** | Schritt 4 / M1, Stand `4daa254`, `main()` ohne Argument |
| `diff` des Planteils | **0 Zeilen** — zeichengleich |

Verglichen wurde alles ausser der letzten Zeile (`Geschrieben: <pfad>`), die den
Zielpfad nennt und sich zwangsläufig unterscheidet — genau dieser Pfad ist der
Gegenstand des Auftrags.

### ⭐⭐ Die schärfere Probe: nicht der Bildschirm, sondern der Plan

Die Konsolenausgabe zeigt je Bot nur sechs Felder und schneidet die
Selektionsfalten bei 40 Zeichen ab (`sel[:40]`). **Ein Unterschied in einem
nicht gedruckten Feld wäre dort unsichtbar.** Deshalb zusätzlich die erzeugten
JSON-Dateien:

| Lauf | SHA-256 |
|---|---|
| vorher (Wegwerflauf vor dem Umbau) | `2dd28291497e1233f6854651688f77d5d0a268370ef1ce423a42820917316794` |
| nachher (M1-Vorlauf, 16:13:05 UTC) | **dasselbe** |
| nachher (M1, 16:15:05 UTC) | **dasselbe** |

`diff` der JSON-Dateien: **0 Zeilen**. Drei Läufe, ein Hash. **Keine Planzahl
hat sich bewegt** — Abbruchkriterium 4 ist nicht erfüllt.

---

## 5. Die drei Sperrlisten-Hashes vorher und nachher

Belege: `schritt0_hashes_vorher.txt` (18:09:16), `schritt6_hashes_nachher.txt`
(18:21:13), Nachmessung bei der Abgabe (18:36:21).

| Datei | Soll | vorher | nachher | Abgabe |
|---|---|:---:|:---:|:---:|
| `ergebnisse/faltenplan.json` | `0e54ac5c…` | ✅ | ✅ | ✅ |
| `ergebnisse/benchmark_drawdowns.json` | `a163c498…` | ✅ | ✅ | ✅ |
| `ergebnisse/benchmark_drawdowns_vt.json` | `4549395f…` | ✅ | ✅ | ✅ |

**Drei Messungen an einem Tag, alle gleich.** Abbruchkriterium 1 und 6 sind
nicht erfüllt.

⚠️ **Der vierte Hash, den dieser Auftrag sehr wohl verändert hat**, ist
`faltenplan.py` selbst (`6f96b95d…` → `fd3e5018…`) — die beauftragte und
freigegebene Änderung. Siehe 3b und Abschnitt 8.

---

## 6. Der Umfang des Diffs (Schritt 7)

`git diff 2144825 HEAD -- research/vorregistrierung/faltenplan.py`, drei Hunks:

| Hunk | Ort | |
|---|---|---|
| `@@ -93,0 +94,2` | Importblock | `argparse`, `hashlib` |
| `@@ -98 +100` | Importblock | `datetime`, `timezone` ergänzt |
| `@@ -359,3 +361,93` | vor `main()` | die drei neuen Funktionen |
| `@@ -372,6 +464,4` | Ende von `main()` | der Schreibteil |

**Nichts dazwischen.** Die Rechenlogik (`_plan`, `erste_falte_4a`, Bedingung
(i)) und die Konsolenausgabe stehen im Diff nur als Kontext.

**Zeile 336** (`"bestaetigungsperiode": falten[-1]["name"] if falten else None,`)
steht heute in Zeile **338** — um genau die zwei neuen Importzeilen verschoben,
**im Wortlaut unverändert**. `grep -c "bestaetigungsperiode"` im Diff: **0**.

---

## 7. ⭐ Was NICHT getan wurde

| ⛔ | |
|---|---|
| ⛔⛔ | **Zeile 336 / `bestaetigungsperiode` nicht angefasst** — das ist Schritt 3 von 36.3, eigener Auftrag, eigene Freigabe |
| ⛔ | **Die Rechenlogik nicht angefasst** — belegt durch drei byteweise identische Pläne (Abschnitt 4) |
| ⛔ | **Die Konsolenausgabe nicht angefasst** — zeichengleich |
| ⛔ | **Kein Registereintrag.** Dieser Auftrag trägt keinen Registertext ein |
| ⛔ | **`auswertung.py`, `herkunft.py`, `benchmark.py`, `registerdaten.py` nicht angefasst** |
| ⛔ | **Das Abbild der Sperrliste nicht neu erzeugt**, der abweichende Hash nicht nachgezogen (36.2) |
| ⛔ | **Nichts repariert** — der Befund der Sonde steht als Befund da |

---

## 8. Die untrackten Dateien — vier Entscheidungen

Beim Aufräumen des Arbeitsbaums lagen fünf untrackte Dinge. Die ersten beiden
Entscheidungen hat der Betreiber getroffen, die dritte ausdrücklich als
Handwerk offengelassen.

### (1) Die Berechtigungsdatei — **eigener Commit** `6278888`

`.claude/settings.local.json` und `docs/projektfuehrung/settings.local.json.vorschlag`,
**getrennt von der TB-86-Arbeit**.

> **Begründung des Betreibers:** Die Berechtigungsdatei sagt, welche Befehle
> eine Sitzung **vor dem signierten Tag** ausführen durfte — ein Nachweis
> derselben Art wie die Sperrliste.

Gemessen vor der Aufnahme: **Geheimnisfelder (`token`/`key`/`secret`/
`password`): 0** in beiden Dateien; ein Mac im Betrieb, also kein
Maschinenkonflikt.

⚠️ **Befund:** `.claude/settings.local.json` wird **nicht** von der `.gitignore`
dieses Repos ignoriert, sondern von der **globalen** `~/.config/git/ignore`
(Zeile 1, `**/.claude/settings.local.json`). Die Aufnahme brauchte `git add -f`.
Ab jetzt ist die Datei verfolgt — Ignoriermuster wirken auf verfolgte Dateien
nicht, spätere Änderungen erscheinen also normal in `git status`.

⚠️ **Offener Punkt, nur benannt:** Die beiden Dateien sind **zeichengleich**
(`diff`: 0 Zeilen). Zwei identische Fassungen derselben Zahl nebeneinander sind
das Muster, vor dem CLAUDE.md warnt (*„doppelt geführte Zahlen sind hier schon
einmal unbemerkt auseinandergelaufen"*). Solange `.claude/` global ignoriert
ist, hat der `.vorschlag` einen Zweck — er ist die sichtbare Fassung. Ab jetzt
ist die echte Datei verfolgt, und der Zweck entfällt. **Ob der `.vorschlag`
bleibt, entscheidet der Betreiber.**

### (2) Die Handsicherung — **nicht committet**, `*.bak` in `.gitignore`

`.claude/settings.local.json.2026-09-22_vor_TB86.bak`. Der Stand vor einer
Änderung steht in der Historie; eine zweite Fassung daneben wäre wieder eine
doppelt geführte Zahl.

### (3) ⭐ Die zwei Laufdateien — **Beleg UND Ignoriermuster** (meine Wahl)

`ergebnisse/faltenplan_2026-09-22-161305.json` und `…-161505.json`, beide
`2dd28291…`, byteweise identisch. Die erste stammt aus einem Vorlauf von M1, bei
dem der Rückgabewert nicht mitgeschrieben wurde; die zweite ist die
protokollierte Probe M1.

**Gewählt: beides.** Kopie nach `docs/belege/TB-86/`, Muster für den
Entstehungsort. Begründung:

| | |
|---|---|
| (a) | Sie sind der **Beleg für M1** — dass `main()` ohne Argument in einen Zeitstempelpfad schreibt und `0` liefert. Beleg gehört zum Auftrag, nicht in den Arbeitsordner |
| (b) | `research/vorregistrierung/ergebnisse/` steht **unter Sperrlisten-Aufsicht**. Seit dem Umbau legt **jeder** Lauf dort eine neue Datei an — das ist Absicht (siehe Abschnitt 2), füllt den Ordner aber mit Laufresten. Ohne Muster verwischt der Unterschied zwischen registriertem Ergebnis und Laufrest |
| (c) | Das Muster `…/ergebnisse/faltenplan_*.json` verlangt den **Unterstrich** und trifft die gesperrte `ergebnisse/faltenplan.json` **nicht** — gemessen: `git check-ignore` rc **1**. `sperrliste_abbild_*.json` bleibt ebenfalls unberührt |

⚠️ **Die Originale bleiben auf der Platte liegen** — `rm` steht auf der
Sperrliste der Sitzungsberechtigungen, ein Löschen wurde abgelehnt. Sie sind ab
jetzt ignoriert und erscheinen nicht mehr in `git status`; ihr Inhalt ist als
Beleg gesichert.

### (4) ⚠️⚠️ Das Abbild aus TB-85 ist überholt — **nur benannt, nicht getan**

Der Befund aus 3b hat eine Folge, die **nicht Teil dieses Auftrags** ist und
hier ausdrücklich nur festgehalten wird:

> **`research/vorregistrierung/ergebnisse/sperrliste_abbild_2026-09-22.json`
> ist überholt.** `faltenplan.py` ist der zweite Pfad von Sperrlistenpunkt 2 und
> hat sich **beauftragt** geändert (`6f96b95d…` → `fd3e5018…`). Das Abbild
> beschreibt damit einen Stand, den es nicht mehr gibt.

Nach **Registertext 36.6** erzeugt jede Fortschreibung ein **neues Abbild unter
neuem Namen**; das alte bleibt stehen. Der Erzeuger schreibt einmalig — ein
neues Abbild ist also zwingend ein neuer Dateiname, kein Überschreiben.

⛔ **Dieser Auftrag tut das nicht.** Solange kein neues Abbild existiert, meldet
die Sonde bei **jedem** Lauf den Befund in Punkt 2. Das ist kein Fehler,
sondern der richtige Zustand: ein Befund, der offen dasteht, bis er
ausdrücklich fortgeschrieben wird.

---

## 9. Der nächste Schritt, benannt

| | |
|---|---|
| ⭐⭐ **Schritt 3 von 36.3** | Zeile 336 — der **Bezeichner der Bestätigungsperiode** nach 35.1. ⛔ **Braucht eine eigene Betreiberfreigabe.** Die Freigabe vom 22.09., 07:50 deckt nur Schritt 1 und 2 |
| **TB-87** | Der **Registereintrag des Abbild-Hashes** `6a1b732e…` (aus TB-85) |
| ⚠️ **neu, aus 8 (4)** | Ein **neues Sperrlisten-Abbild** unter neuem Namen (36.6), weil `faltenplan.py` sich beauftragt geändert hat. Ohne Auftrag und ohne Freigabe |
| offen, aus 8 (1) | Ob `docs/projektfuehrung/settings.local.json.vorschlag` neben der jetzt verfolgten Originaldatei bestehen bleibt |

---

## 10. In einfacher Sprache

Ein Programm im Projekt rechnet den Auswertungsplan aus — und schrieb ihn dabei
**immer** in dieselbe Datei, die eigentlich unveränderlich sein soll. Es ist nie
etwas passiert, weil niemand das Programm gestartet hat. Das reichte nicht als
Schutz.

Zwei Änderungen, beide klein:

**Erstens** schreibt das Programm jetzt standardmässig in eine Datei, deren Name
die Uhrzeit enthält — also jedes Mal in eine neue. Die geschützte Datei ist nur
noch erreichbar, wenn jemand sie ausdrücklich angibt.

**Zweitens** hat es eine Sperre bekommen: **Gibt es die Zieldatei schon,
schreibt es gar nichts** und meldet stattdessen, was dort liegt. Auch dann,
wenn der Inhalt derselbe wäre.

⭐ **Der wichtigste Test ist gelaufen:** Das Programm wurde absichtlich auf die
geschützte Datei angesetzt und hat sich geweigert. Ihre Prüfsumme war davor und
danach dieselbe — und sogar ihr Änderungszeitpunkt, was heisst: sie wurde nicht
einmal geöffnet.

**Keine Zahl im Plan hat sich bewegt.** Das wurde nicht nur am Bildschirm
verglichen, sondern an den erzeugten Dateien selbst: drei Läufe, eine einzige
Prüfsumme.

Ein Nebenbefund zum Schluss: Das Prüfwerkzeug aus der Vorsitzung meldet jetzt
einen Treffer — weil genau die Datei geändert wurde, die repariert werden
sollte. **Das ist richtig so.** Das Werkzeug kann nicht wissen, dass die
Änderung erlaubt war, und soll es auch nicht. Der Treffer bleibt stehen, bis
jemand ihn ausdrücklich fortschreibt. Repariert wurde er nicht.

---

*Geschrieben 22.09.2026 von der Mac-Sitzung TB-86 selbst.*
