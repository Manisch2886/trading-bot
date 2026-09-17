# TB-45 — Stille Ausfälle

**Fünf Stellen hörten auf zu arbeiten, ohne es zu sagen. Alle fünf sind
behoben oder gemessen.**
Cloud, 17.09.2026 · Zweig `claude/new-session-l4l5k1` · frisch von `main`
(`97aea88`) · Python 3.11.15, pandas 2.3.3, numpy 2.0.2

---

## Die fünf Befunde

| | Befund | Stand |
|---|---|---|
| **1** | `shared/test_kursdaten.py` prüfte den Rückgabewert von `git` nicht — **rc 128, trotzdem „bestanden"** | ✅ **behoben** |
| **2** | `dashboard/test_portfolio_sicht.py` zählte einen Fehlschlag ausdrücklich als Erfolg (`returncode != 0 or …`) | ✅ **behoben** |
| **3** | `_ist_geraet` lieferte **True für jedes Verzeichnis** — und Prüfung B2 hing daran, ob die Bots hier schon gelaufen sind | ✅ **behoben** |
| **4** | Ein leerer Kursrahmen beendete `elliott_wave` und `elliott_wave_stocks` **hart** (`IndexError`) | ✅ **behoben** |
| **5** | `fromisoformat` im Live-Pfad aller neun Bots, 3.9 gegen 3.11 | 📏 **gemessen, nichts geändert** |

---

## Was die Tests sagen

**Jeder Befund wurde zuerst reproduziert, dann behoben.** Jeder Test ist am
unveränderten Stand rot:

| Test | neuer Stand | **unveränderter Stand** |
|---|---|---|
| `shared/test_stille_ausfaelle.py` (neu) | **27 / 27** | ⚠️ **6 rot** (Teil 1 und 2) |
| `shared/test_leeres_symbol.py` (neu) | **45 / 45** | ⚠️ **12 rot** (Teil 4) |
| `research/universum_trockenlauf/…`, Teil N (neu) | Teil des 356/356 | ⚠️ **5 rot** (Teil 3) |
| `shared/test_kursdaten.py` | **88 / 88** (vorher 81/81) | — |
| `research/universum_trockenlauf/test_universum_trockenlauf.py` | **356 / 356** (vorher 332/332) | — |
| `dashboard/test_portfolio_sicht.py` | **91 / 91** | — |

⚠️ **Und die Negativ-Prüfungen bleiben grün.** Ein leeres Ergebnis aus einem
*gelungenen* git-Aufruf **ist** der Nachweis — verschärft wurde nur der
*gescheiterte* Aufruf.

---

## Die drei Antworten, um die gebeten wurde

**1 · Welche Prüfungen sind welcher Sorte?**
⭐ **In `shared/test_kursdaten.py` sind alle fünf git-gestützten Prüfungen von
der `daten_unberuehrt`-Sorte.** Es gibt dort keine der zweiten Sorte — auch
die Schleifen über `forward_test.py` und `live_params.py` nicht: Läuft keine
Runde, weil die Datei unverändert ist, dann ist kein Handelsparameter
verändert, und der Nachweis trägt.

**2 · Löst die Drei-Punkt-Form T38.9?**
**Ja — aber sie kostet etwas anderes, und darum wurde sie nicht übernommen.**

| Form | `main` zieht weiter | unkommittierte Änderung |
|---|---|---|
| Zwei Punkte | ⚠️ falsch rot | ✅ sichtbar |
| **Drei Punkte** | ✅ still | ⚠️ **unsichtbar** |
| **Merge-Basis** | ✅ still | ✅ sichtbar |

In `research/fib_score_stufen/test_stufen.py` ist das unschädlich, weil direkt
daneben ein `git status --porcelain` steht. **In `test_kursdaten.py` gibt es
diese Begleitprüfung nicht.** ⭐ Der **Merge-Basis-Vergleich** löst beides —
Vorlage für eine eigene Aufgabe, nicht hier gemacht.

**3 · Was kommt bei `fromisoformat` an?**
**Genau ein Wert: `'2026-09-16T00:00:00'`** (Typ `str`), vom Code selbst aus
dem Börsenkalender gebaut. ⭐ Die Zeitstempel der **Kursdateien** kommen dort
gar nicht an (die liest `pandas`), und der **Krypto-Pfad** erreicht die Stelle
nie — betroffen wären **vier von neun** Bots, nicht neun.
Sechs Schreibweisen gehen auf 3.11 durch und scheitern auf 3.9; **keine davon
kann heute dort ankommen.**
Träte es ein: **kein stiller Rückfall, keine falsche Kerze, kein Abbruch** —
der Bot ließe jedes Symbol aus, schriebe je eine Zeile und handelte nicht.

---

## Zwei Befunde, die niemand gesucht hat

⭐ **`t3_supertrend` hat denselben harten Stopp** — `compute_indicators` bricht
auf einem leeren Rahmen mit `IndexError` ab. Es überlebt nur, weil der Aufruf
im `try` der Ladeschleife steht. **Die Meldung nennt das Symptom, nicht die
Ursache.** Nicht repariert — eigene Freigabe nötig.

⚠️ **Sechs der neun Bots überspringen ein leeres Symbol still.** Das
widerspricht dem Satz „Ein Lauf, der ein Symbol auslässt, sagt es. Immer."
Eine Zeile je Bot würde es beheben. Nicht gemacht — Teil 4 war nur für die
beiden Elliott-Bots freigegeben.

---

## Randbedingungen — eingehalten und nachgewiesen

| | |
|---|---|
| **Datenstand vorher = nachher** | `d9449faf51bffaaa…`, **223 Dateien** — als Test (`shared/test_stille_ausfaelle.py`, Abschnitt 4) |
| `shared/entscheidungskerze.py` | **unberührt** (`git diff` leer) |
| `live_params.py`, `broker/`, Crontab, `results/*.csv` | **unberührt** |
| `docs/VORREGISTRIERUNG_*`, `docs/projektfuehrung/*`, `docs/UMGEBUNGEN.md` | **unberührt** — Vorschläge stehen im Bericht |
| Bot-Module | **gelesen, nie importiert** — ein eigener Prozess je Bot |

---

## Zwei Korrekturen an der Liste „bekannt rot"

| Test | laut Aufgabe | **gemessen** |
|---|---|---|
| `dashboard/test_portfolio_sicht.py` | „rot, **beide**" | ⚠️ **in der Cloud grün (91/91)** — rot wird er auf dem Mac, wo die Live-Datenbanken liegen |
| `dashboard/test_dashboard.py` | „in der Cloud rot (780/780)" | ⚠️ **grün (784/784)** — `node` ist in dieser Cloud vorhanden |

---

## Was als Nächstes gebraucht wird

1. **Der Mac-Lauf** — `docs/TESTAUFTRAG_TB-45_stille_ausfaelle.md`.
   ⚠️ **Teil 3 und 5 sind in der Cloud strukturell nicht vollständig
   prüfbar.**
2. **Eine Entscheidung zu Teil 5** —
   `research/fromisoformat_registerfrage/BERICHT.md`, drei Wege.

---

## In einfacher Sprache

**Was wir wissen wollten.**
Fünf Stellen im Projekt hörten auf zu arbeiten, ohne es zu sagen. Drei davon
waren Prüfwerkzeuge, die „alles in Ordnung" meldeten, obwohl sie gar nicht
nachgesehen hatten. Eine war eine Hilfsfunktion mit einem irreführenden Namen.
Und eine war ein echter Ausfall: Fiel die Kursquelle für ein einziges
Wertpapier aus, arbeiteten **zwei von neun Handelsprogrammen** an dem Tag gar
nicht.

**Was herauskam.**
Vier sind repariert, die fünfte ist vermessen. Für jede gibt es einen Test,
der sie findet — und der am alten Stand wirklich durchfällt. Dazu zwei Dinge,
die niemand gesucht hat: Ein drittes Programm hat denselben Fehler, überlebt
ihn aber zufällig; und sechs Programme lassen ein Wertpapier stillschweigend
aus. Beides ist aufgeschrieben, nicht repariert.

**Warum das so ist.**
Ein Prüfwerkzeug, das bei einem Fehler „bestanden" sagt, ist schlimmer als
gar keines — man verlässt sich darauf. Deshalb bestand die Arbeit weniger aus
Reparieren als aus **Vorführen**: erst den Fehler sichtbar machen, dann
beheben, dann zeigen, dass er weg ist. Und dabei aufpassen, dass Prüfungen,
bei denen „nichts gefunden" das richtige Ergebnis ist, grün bleiben.

**Was das für dich heißt.**
Am Verhalten deiner Handelsprogramme hat sich **nichts** geändert — keine
Zahl, keine Regel, keine Schwelle; die Kursdaten sind nachweislich unberührt.
Was sich geändert hat: Fällt morgen eine Kursquelle aus, hören zwei Programme
nicht mehr auf zu arbeiten, sondern lassen das eine Wertpapier aus und
schreiben eine Zeile darüber. Und drei Prüfwerkzeuge sagen dir jetzt Bescheid,
wenn sie nicht mehr messen können. **Zwei Dinge brauchen dich:** der Testlauf
auf deinem Rechner und eine Entscheidung, die im Bericht zu Teil 5 steht.
