# ERGEBNIS TB-60 — Das Backlog-Archiv

⚠️ **Kein Selbstbericht der ausführenden Sitzung.** Sie wurde am 20.09.2026 um
**10:57** durch einen Abbruch der SSH-Verbindung beendet, bevor sie die Abgabe
schreiben konnte. **Die Nachweise hier sind von der Chat-Sitzung unabhängig
nachgemessen** (Prüfprinzip A7: nachgeholt, und das steht dabei). ⭐ Nach
Backlog `Q2` wiegt eine Prüfung durch jemanden, der die Arbeit nicht gemacht
hat, mehr als ein Selbstbericht — **hier trifft das zu.**

Commit **`c04b348`**, auf `origin/main`.

---

## Die acht Nachweise

| # | Nachweis | Ergebnis |
|---:|---|---|
| **1** | `numstat` je Datei | `44  561  BACKLOG.md` · `600  0  BACKLOG_ARCHIV.md` · `0  269` und `0  204` für die zwei gelöschten Dubletten |
| **2** | ⭐⭐ **Verschiebenachweis** | **561 entfernte Zeilen, davon 0 nicht zeichengleich im Archiv.** Gegenprobe: 23 Archivzeilen stammen nicht aus dem Backlog — Kopf und Verweise, erwartet |
| **3** | `BACKLOG.md` vorher → nachher | **1 959 → 1 443 Zeilen**, 350 403 → **223 021 Bytes** |
| **4** | `BACKLOG_ARCHIV.md` | **600 Zeilen**, 133 487 Bytes |
| **5** | ⭐ **Pflichtlektüre je Sitzung** | **469 837 → 346 695 Bytes**, **−123 142 (−26 %)** |
| **6** | Kollisionsprobe | offen — siehe unten |
| **7** | Befund zu Abschnitt 9 | ⚠️ **NICHT PRÜFBAR** — die Sitzung wurde vor dem Bericht beendet, und ob sie den Vergleich gemacht hat, ist nachträglich nicht feststellbar. *Nicht grün, nicht rot* (A2) |
| **8** | Nichts ausserhalb `docs/` | **0 Dateien** |

⚠️ **Zu Nachweis 2, in eigener Sache:** Mein erster Prüflauf zählte **546** statt
561 Zeilen — der Filter verwechselte entfernte Markdown-Trennlinien `---` mit
Diff-Kopfzeilen. **Korrigiert und wiederholt: 561, deckungsgleich mit dem
`numstat`.** *Dritter Fall an diesem Tag, in dem ein Messmuster den Suchraum
nicht abdeckte.*

---

## Die beiden Löschungen

Freigegeben durch den Betreiber am 20.09.2026, nach `DOKUMENTATIONSSTANDARD.md`
Regel 9. `docs/belege/TB-56b/abschnitt_21.md` (269 Z.) und `abschnitt_22.md`
(204 Z.) sind entfernt; ihr Inhalt steht **wörtlich** als Abschnitt 21 und 22 in
`docs/VORREGISTRIERUNG_neuselektion.md`. Der Ordner existiert nicht mehr.

## ⚠️ Offen

| | |
|---|---|
| **1** | **Kollisionsprobe über beide Dateien** (Nachweis 6) — noch nicht gemacht |
| **2** | **Der Befund zu Abschnitt 9** (Nachweis 7) — was darin stand und in `ARBEITSWEISE.md` fehlt, ist nicht berichtet |
| **3** | ⚠️ **Der Archivkopf verweist auf dieses Dokument**, das es bis jetzt nicht gab — mit diesem Eintrag geschlossen |

---

## In einfacher Sprache

**Was wir wissen wollten:** Lässt sich die Aufgabenliste halbieren, ohne dass
etwas verlorengeht?

**Was herauskam:** Ja. Sie ist von 350 auf 223 Kilobyte geschrumpft, und was ein
neuer Chat zu Beginn lesen muss, ist um ein Viertel kleiner. **Keine einzige
Zeile ist verschwunden** — alle 561 stehen zeichengleich in der Archivdatei,
maschinell geprüft.

**Was das für dich heisst:** Jede künftige Sitzung startet billiger. Und der
Nachweis ist strenger als die alte Regel „es wurde nichts entfernt", weil er
**beide Seiten** prüft statt nur einer.
