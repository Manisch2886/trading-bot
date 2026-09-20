# Journal-Nachtrag (a) — 20.09.2026: TB-60, das Backlog-Archiv

⚠️ **Nachgeholt durch die Chat-Sitzung** (A7). Die Mac-Sitzung wurde um **10:57**
durch einen Abbruch der SSH-Verbindung beendet. Beleg:
`docs/ERGEBNIS_TB-60_backlog_archiv.md`.

## Der Ergebnisblock

**TB-60 — Backlog-Archiv mit Verschiebenachweis.** Commit `c04b348` auf
`origin/main`.

| | gemessen |
|---|---|
| `BACKLOG.md` | **1 959 → 1 443 Zeilen**, `numstat` **44 / 561** |
| `BACKLOG_ARCHIV.md` | **600 Zeilen** neu |
| ⭐ **Verschiebenachweis** | **561 entfernte Zeilen, 0 nicht zeichengleich im Archiv**; 23 Archivzeilen sind Kopf und Verweise |
| ⭐ **Pflichtlektüre** | **469 837 → 346 695 Bytes (−26 %)** |
| Löschungen | beide Beleg-Dubletten entfernt, Inhalt wörtlich im Register |

## ⭐⭐ Die Lehre des Tages, und sie ist doppelt

**1. Ein Nachweis, der nur eine Richtung prüft, wird zum Anreiz in diese
Richtung.** Das Projekt wies Dokumentationsarbeit über `numstat`-Spalte
zwei = 0 nach. Diese Null ist ein Beweis — **und war zugleich die Ursache des
Wachstums.** Sie wurde in jeder Runde vorgezeigt und nie als Preis benannt.
*Dieselbe Familie wie A4: ein Nachweis, der nicht durchfallen kann, hört auf,
eine Wache zu sein.*

**2. Verschieben ist beweisbarer als Behalten.** Die neue Regel für diesen Fall
— *jede entfernte Zeile erscheint zeichengleich im Archiv* — prüft **beide
Seiten** statt einer.

⚠️ **Und ein eigener Fehler:** Der erste Prüflauf zählte **546** statt 561
Zeilen, weil der Filter entfernte Markdown-Trennlinien `---` mit Diff-Kopfzeilen
verwechselte. **Dritter Fall an diesem Tag, in dem ein Messmuster den Suchraum
nicht abdeckte** — nach dem `K2`-Muster, das keine `K3`-Nummern sah, und der
geschätzten Zeilenzahl 70 statt 67.

⇒ ⭐ **Regel, die daraus folgt: Ein Messergebnis wird gegen eine zweite,
unabhängige Zählung gehalten, bevor es als Nachweis gilt.** Hier war der
`numstat` diese zweite Zählung — und nur deshalb fiel der Fehler auf.

## ⚠️ Offen

Kollisionsprobe über `BACKLOG.md` und `BACKLOG_ARCHIV.md` zusammen; der Befund
zu Abschnitt 9 (was darin stand und in `ARBEITSWEISE.md` fehlt) ist **nicht
prüfbar**, weil die Sitzung vor dem Bericht endete.
