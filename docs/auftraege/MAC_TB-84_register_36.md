# TB-84 — Registerabschnitt 36: die Schreibregel für Sperrlistenpfade, die Sperrlisten-Sonde und die Reihenfolge

**Sitzungstitel:** `TB-84 Register 36 — Schreibregel und Sperrlisten-Sonde`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**Erstellt:** 22.09.2026, 07:40 Ortszeit · **Vorgänger:** TB-83 (`fdb181a`)
**Erwarteter Ausgangsstand:** `HEAD` = `origin/main` = `fdb181a` oder jünger

---

## 0. Was dieser Auftrag ist — und was er NICHT ist

⭐ **Reines Eintragen von Registertext**, wie TB-82 und TB-83. **Vier Einträge**
aus `FABLE_ANTWORT_2026-09-22b_schreibregel_sperrliste.md`.

| ⛔ | **NICHT Gegenstand** |
|---|---|
| ⛔ | **Die Sperrlisten-Sonde schreiben** — Schritt 1 von Fables Reihenfolge, ⚠️ **Freigabe steht aus** |
| ⛔ | **`faltenplan.py main()` absichern** — Schritt 2, Freigabe steht aus |
| ⛔ | **`faltenplan.py:336`** (Bezeichner) — Schritt 3, ⚠️⚠️ **darf nach 36.1 (4) erst nach Schritt 2 kommen** |
| ⛔ | ⚠️⚠️ **`python3 faltenplan.py` ausführen** — **NIEMALS.** `main()` überschreibt `ergebnisse/faltenplan.json`, Sperrlistenpunkt 2. Abbruchkriterium 5 |
| ⛔ | `herkunft.py` anfassen — ⚠️ **steht selbst auf der Sperrliste** (Punkte 11, 12) |
| ⛔ | Irgendeine `.py` ändern |

---

## 1. Schritt 0

1. **Schlüsselbund entsperren**, Kopfzeile „Claude Max".
2. **Committe, was im Arbeitsbaum liegt** — erwartet: zwei untrackte Dateien
   (`FABLE_ANTWORT_2026-09-22b_schreibregel_sperrliste.md`,
   `FABLE_ANFRAGE_2026-09-22b_sonde_bestand.md`); *falls schon committet: nur
   prüfen.*
3. **Nachweis:** `git status --short` leer, HEAD notieren.

---

## 2. Die Regel aus TB-82/83 gilt weiter: Marke AM ALTEN ORT

Voller Text in **Abschnitt 36**, dazu ein eingerückter Hinweisblock (`>`) oder
eine Tabellenzeile **direkt beim betroffenen Satz**. ⚠️ **Nur hinzufügen.**
⭐ `numstat` Spalte 2 = **`0`**.

---

## 3. Die vier Einträge

### 36.1 — Schreibregel für Sperrlistenpfade (Ersteintrag)

**Herkunft:** `FABLE_ANTWORT_2026-09-22b_schreibregel_sperrliste.md`,
Abschnitt 2, **zeichengleich:**

> **Registertext, Ersteintrag — Schreibregel für Sperrlistenpfade:**
> **(1)** Kein Programm im Repo schreibt an einen Pfad, der auf der Sperrliste steht oder für sie bestimmt ist. **(2)** Jeder Erzeuger einer solchen Datei schreibt **einmalig**: Existiert die Zieldatei bereits, bricht er ab (Rückgabewert ≠ 0), nennt Pfad und Hash der vorhandenen Datei und schreibt nichts. Er überschreibt nie, auch nicht mit identischem Inhalt. **(3)** Ein anderes Ziel nur durch ausdrückliches Argument; die Voreinstellung eines Erzeugers ist nie ein Pfad, der auf der Sperrliste steht. **(4)** Für `faltenplan.py main()`: Voreinstellung weg von `ergebnisse/faltenplan.json` (Sperrlistenpunkt 2) auf einen nicht gesperrten Pfad, und die Einmal-Schreibsperre nach (2). Beides vor jeder weiteren Änderung an `faltenplan.py`, insbesondere vor Z. 336.

**Fables Grund, zeichengleich:**

> *„Zweck der Sperrliste (‚nichts Gesperrtes ist bewegt worden', Übergabe Abschnitt 5) und A8 (eine Wache ist, was jemand ausführt). Die Einmal-Schreibsperre braucht keine Sperrlistenkenntnis — sie schützt auch die Abbild-Datei, die noch nicht auf der Liste steht, und sie schützt gegen den Fall, den niemand vorausgesehen hat."*

**Und sein Satz zur Härte der Sperre, zeichengleich:**

> *„Eine Sperre, die bei gleichem Inhalt durchlässt, muss den Inhalt vergleichen — und wer den Vergleich programmiert, entscheidet, was ‚gleich' heisst (Schlüsselreihenfolge, Zeilenende, `sort_keys`). Die Sperre ist stärker, wenn sie dümmer ist."*

⭐ **Fables Tatsachennotiz, zeichengleich zu übernehmen:**

> *„`ergebnisse/faltenplan.json` (Hash `0e54ac5c…`) ist seit dem 14.09. unverändert, obwohl `faltenplan.py main()` seit demselben Tag bei jedem Aufruf dorthin schreibt; TB-72 und TB-80 haben eigene Belegskripte verwendet. Der Bestand hielt durch Übung, nicht durch Regel. Der Hash ist am 22.09. gemessen und stimmt."*

**Marke am alten Ort:** unter **Sperrliste Punkt 2** (Abschnitt 10), als
eingerückter Block — ⚠️ **die vorhandene Tatsachennotiz aus Abschnitt 30 bleibt
zeichengleich stehen**, der neue Block kommt darunter.

### 36.2 — Die Sperrlisten-Sonde (Ersteintrag)

**Herkunft:** 22b, Abschnitt 2, **zeichengleich:**

> **Registertext, Ersteintrag — Sperrlisten-Sonde:**
> Vor dem signierten Tag existiert ein Prüfskript, das für **jeden** Sperrlistenpunkt Pfad und Hash gegen den Registertext prüft und bei einer Abweichung mit Rückgabewert ≠ 0 endet und den Punkt nennt. Der Registertext der Sperrliste ist die Quelle; eine maschinenlesbare Fassung ist Abbild und wird von der Sonde selbst gegen den Registertext geprüft (Bauart 33.3). Die Sonde läuft (a) als Nachweis vor dem Tag, (b) im Laufwrapper vor `auswertung.py`, (c) am Ende jedes Auftrags, der Sperrlisten-nahen Code berührt. Ein Sperrlistenbruch, den die Sonde findet, ist eine Tatsachennotiz — nie eine stille Reparatur.

⭐⭐ **Dazu drei Tatsachennotizen von uns, die Fable vorliegen und die du
NACHMESSEN musst (M3–M5). ⚠️ Sie sind ihm mit
`FABLE_ANFRAGE_2026-09-22b_sonde_bestand.md` vorgelegt; seine Antwort steht aus
und wird hier ausdrücklich als ausstehend vermerkt:**

> **(a) Das Muster existiert, die Sache nicht.** `shared/snapshot.py --pruefen`
> prüft Datenstände und hat **drei** Ausgänge: `0` in Ordnung, `1` Befund,
> **`2` NICHT PRÜFBAR / abgebrochen**. Begründung im Kopf der Datei: *„In TB-45
> haben zwei Wachen ‚bestanden' gemeldet, ohne etwas gemessen zu haben."*
> ⚠️ **Der Registertext oben sagt nur „Rückgabewert ≠ 0" und unterscheidet die
> beiden roten Fälle nicht** — nach `A2` sind sie verschieden. **Offen bei
> Fable.**
>
> **(b) `herkunft.py` scheidet als Ort aus.** Sein `--pruefen` meldet die vier
> Verankerungen, nicht Sperrlisten-Hashes — **und die Datei steht selbst auf der
> Sperrliste** (Punkte 11, 12). Die Sonde braucht eine eigene Datei.
>
> **(c) ⚠️ Zwei maschinenlesbare Listen liegen bereits in `herkunft.py`** und
> decken sich **nicht** mit dem Registertext: `EINGEFROREN` (Z. 57, zehn
> Einträge) und `SPERRLISTE_DATEIEN` (Z. 66, fünf Muster) gegen **14**
> Registerpunkte. `ergebnisse/benchmark_drawdowns_vt.json` (`4549395f…`) und die
> beiden Universumsdateien aus Punkt 8 fehlen dort; umgekehrt führt
> `EINGEFROREN` Dateien, die der Registertext nicht als eigene Punkte nennt.
> ⛔ **Nicht bewertet** — ob `EINGEFROREN` überhaupt als Sperrlisten-Abbild
> gemeint war, steht nirgends. **Offen bei Fable.**

**Marke am alten Ort:** unter der **Überschrift von Abschnitt 10**, als
Hinweisblock — *„Ab 36.2 prüft eine Sonde diese Liste; die maschinenlesbare
Fassung ist Abbild, nicht Quelle."*

### 36.3 — Die Reihenfolge der Handwerksschritte

**Herkunft:** 22b, Abschnitt 3, **zeichengleich:**

> 1. **Sperrlisten-Sonde** schreiben und einmal laufen lassen — Nachweis, dass heute alles stimmt (der Nullpunkt).
> 2. **`faltenplan.py main()`:** Voreinstellung ändern, Einmal-Schreibsperre einbauen. **Mutationsprobe:** `main()` gegen eine Kopie von `faltenplan.json` am neuen Zielpfad aufrufen → muss abbrechen; Sonde danach → grün.
> 3. **Erst jetzt** Z. 336 (Bezeichner der Bestätigungsperiode, 22a). Prüfen über `main()` ist ab jetzt ungefährlich; Sonde danach → grün.
> 4. Abbild-Datei, Faltenplan-Sonde (33.3), Hash auf die Sperrliste — wie geplant; der Erzeuger des Abbilds unterliegt der Schreibregel von Anfang an.

**Fables Satz dazu, zeichengleich:**

> *„Wer Schritt 3 vor Schritt 2 macht, hat genau den Fall, den ihr beschreibt. Deshalb steht die Reihenfolge hier und nicht nur im Auftrag."*

⛔ **Einzutragen ist auch:** Alle vier Schritte brauchen **Betreiberfreigabe**;
am 22.09.2026, 07:40 ist **keine** erteilt.

**Marke am alten Ort:** in **35.1**, beim Satz über den heutigen unzulässigen
Bezeichner — Verweis, dass die Umstellung nach 36.3 erst nach Schritt 2 kommt.

### 36.4 — Tatsachennotiz zu 21.4: die `⚠️`-Markierung ohne Erklärung

**Herkunft:** 22b, Abschnitt 1, **zeichengleich:**

> *„Die ⚠️-Markierung in 21.4 hat keinen Text. Dann ist sie eine Markierung ohne Bedeutung, und das gehört als Tatsachennotiz zu 21.4: ‚⚠️ bei `elliott_wave`, Spalte Bestätigung ab, trägt keine Erklärung; nicht als Beleg verwendbar.' Sonst nimmt sie in einem Jahr jemand für einen Vorbehalt, den es nie gab."*

⭐ **Und unsere Rücknahme dazu, einzutragen:** Die Deutung aus
`FABLE_ANFRAGE_2026-09-21g` Punkt 3 (*„Möglicherweise ist das der Grund für die
⚠️-Markierung"*) ist **zurückgezogen** — sie war eine Vermutung und taugt nicht
als Beleg.

**Marke am alten Ort:** ⚠️ **direkt in 21.4**, als Zeile unter der Tabelle —
*die Tabellenzeile selbst bleibt zeichengleich, samt `⚠️`.*

---

## 4. Die Messungen (bestätigen, nicht übernehmen)

| # | Messung | erwartet |
|---:|---|---|
| **M1** | `grep -c "^[0-9]\+\." ` im Sperrlisten-Abschnitt | **14 Punkte** |
| **M2** | Hash `research/vorregistrierung/ergebnisse/faltenplan.json` **vor und nach** | **`0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339`** beide Male |
| **M3** | `grep -n "^0\|^1\|^2" `-Block im Kopf von `shared/snapshot.py` (Z. 214–232) | **drei Ausgänge, `2` = NICHT PRÜFBAR** |
| **M4** | `grep -n "EINGEFROREN\|SPERRLISTE_DATEIEN" research/vorregistrierung/herkunft.py` | **Z. 57 und Z. 66** |
| **M5** | ⭐ Steht `ergebnisse/benchmark_drawdowns_vt.json` in einer der beiden Listen? | **nein** |
| **M6** | Die Faltenlisten in 33.2 vor und nach | **identisch** |

**Belege:** `docs/belege/TB-84/m1…m6.txt`, Befehl in Zeile 1.

⚠️ **M3–M5 sind die Grundlage der drei Tatsachennotizen in 36.2.** Weichen sie
ab: **eintragen, was du misst**, und melden.

---

## 5. ⛔ Abbruchkriterien

| # | Wenn … | dann |
|---:|---|---|
| **1** | `numstat` Register Spalte 2 ≠ `0` | ⛔ ABBRUCH, kein Commit |
| **2** | Eine Faltenliste in 33.2 unterscheidet sich nachher | ⛔ ABBRUCH |
| **3** | Ein Fable-Zitat nicht zeichengleich übernehmbar | ⛔ Anhalten, melden, **nicht glätten** |
| **4** | Du meinst, eine `.py` ändern zu müssen | ⛔ ABBRUCH |
| **5** | ⚠️⚠️ **Hash von `ergebnisse/faltenplan.json` weicht ab (M2)** | ⛔⛔ **SOFORT ABBRUCH.** Nichts committen, nichts reparieren, **nur melden** — nach 36.2 ist ein Bruch eine Tatsachennotiz, **nie eine stille Reparatur** |
| **6** | Abschnitt 36 existiert bereits | ⛔ Anhalten |
| **7** | Ein anderer Sperrlisten-Hash ändert sich (`a163c498…`, `4549395f…`) | ⛔ ABBRUCH |

---

## 6. Schritte

| # | Tun | Nachweis |
|---:|---|---|
| **0** | Schlüsselbund, Arbeitsbaum, HEAD | Status leer |
| **1** | **M1–M5 und M2 (vorher)** messen | fünf Belege |
| **1b** | **M6 vorher**: Faltenlisten festhalten | `m6_faltenlisten.txt` |
| **2** | **Abschnitt 36** schreiben — 36.1 bis 36.4, Fable zeichengleich, dazu Schlussteil „Was hier NICHT getan wird" | Commit |
| **3** | **Die vier Marken am alten Ort**: Sperrliste Punkt 2, Überschrift Abschnitt 10, 35.1, 21.4 — ⚠️ **nur einfügen** | Commit |
| **4** | **M6 und M2 nachher** | 0 Abweichungen, Hash gleich |
| **5** | `numstat` Spalte 2 = `0` | Abschlussbeleg |
| **6** | `grep -c "^## 36\."` = `1` | Beleg |
| **7** | Alle drei Sperrlisten-Hashes | unverändert |
| **8** | **`AKTUELLER_AUFTRAG.md`**: ⭐ **bereits auf TB-84 gesetzt** — ⚠️ **nur lesen.** Zeigt `numstat` dafür etwas, hast du sie angefasst: anhalten | `grep -c "TB-84"` ≥ 1 |
| **9** | **Journalblock** und `docs/auftraege/ERGEBNIS_TB-84.md` | Commit |
| **10** | **Abgabe**: Status leer, `numstat` nachgetragen | Abschlussbeleg |

---

## 7. Ins Ergebnisdokument

1. Die vier Einträge mit Zeilennummer
2. **M1–M6 mit gemessenem Wert**
3. Der `numstat`-Nachweis
4. ⚠️ **M2 hervorheben** — Hash der gesperrten Datei vor und nach
5. ⭐ **Was NICHT getan wurde**: keine Sonde, kein `main()`-Umbau, kein Z. 336,
   kein `python3 faltenplan.py`, `herkunft.py` unberührt
6. ⚠️ **Offen und benannt:** Fables zwei Fragen aus unserer Anfrage 22b (drei
   Ausgänge? welche Liste wird Abbild?) und die **fehlende Betreiberfreigabe**
   für Fables Schritte 1–4

---

## In einfacher Sprache

Fable hat auf die gestern gemeldete Falle geantwortet — und statt einen der drei
vorgeschlagenen Wege zu wählen, macht er aus zweien eine **allgemeine Regel**:
Kein Programm darf an einen geschützten Pfad schreiben; und jedes Programm, das
solche Dateien erzeugt, schreibt **nur einmal** — existiert die Datei schon,
bricht es ab. Auch dann, wenn der Inhalt identisch wäre. Sein Satz dazu: *„Die
Sperre ist stärker, wenn sie dümmer ist."*

Dazu kommt ein **Prüfprogramm**, das alle geschützten Dateien gegen ihre
Prüfsummen kontrolliert — vor dem Stichtag, vor jedem Lauf und nach jedem
Auftrag in ihrer Nähe. Und eine **Reihenfolge**: erst das Prüfprogramm, dann die
Absicherung, **erst dann** die Zeile ändern, die er vorgestern angeordnet hat.
Wer die Reihenfolge umdreht, löst genau den Unfall aus, den wir gemeldet haben.

**Dieser Auftrag schreibt nur Text.** Er baut weder Prüfprogramm noch
Absicherung — dafür fehlt die Freigabe des Betreibers.

⚠️⚠️ **Dieselbe Warnung wie zuletzt:** `faltenplan.py` darf nicht gestartet
werden. Die Prüfsumme der geschützten Datei wird vorher und nachher gemessen.
Weicht sie ab, bricht die Sitzung sofort ab — **und repariert nichts**, sondern
meldet nur. Das ist Fables ausdrückliche Anweisung.
