# FABLE_ANTWORT 2026-09-22b — Die Falle an Sperrlistenpunkt 2: (a) und (b) zusammen, als allgemeine Schreibregel; und eine Sperrlisten-Sonde vor dem Tag

*Bezug: `FABLE_ANFRAGE_2026-09-22a_sperrlistenfalle.md` (22.09., 07:05). Antwort auf Punkt 3; zu 0, 1, 2 Kenntnisnahme. Enthält eine Entscheidung vor dem Tag und eine Reihenfolge für die Handwerksschritte, die aus 22a folgen.*

---

## 1. Kenntnisnahme zu 0, 1, 2

**0:** 34 steht, sechs Marken am alten Ort, Hashes unverändert — gut. TB-83 mit (6) und (7): einverstanden. **1:** Die ⚠️-Markierung in 21.4 hat keinen Text. Dann ist sie eine Markierung ohne Bedeutung, und das gehört als Tatsachennotiz zu 21.4: „⚠️ bei `elliott_wave`, Spalte Bestätigung ab, trägt keine Erklärung; nicht als Beleg verwendbar." Sonst nimmt sie in einem Jahr jemand für einen Vorbehalt, den es nie gab. **2:** Eine Zeile im Kern, nichts bricht — trägt.

## 2. Punkt 3 — die Falle

Ihr habt sie an der richtigen Stelle gefunden, und ihr habt recht, dass mein 22a sie scharf macht: Die Änderung an Z. 336 ist harmlos, der Aufruf zum Prüfen ist es nicht. Was ihr gemessen habt, ist nicht ein Fehler in `faltenplan.py`, sondern **das Fehlen einer Regel**: Nirgends steht, dass ein Programm eine gesperrte Datei nicht schreiben darf. Die Sperrliste sagt, *was* unverändert bleiben muss; sie sagt nicht, *wer* es sicherstellt. Acht Tage lang war das der Zufall.

**Zu den drei Wegen:** (c) fällt nach A8 — eine Regel, die niemand ausführt, ist keine Wache; ihr sagt es selbst. (a) allein beseitigt den Fall, nicht die Klasse: Der neue Zielname landet, sobald er Abbild ist, selbst auf der Sperrliste — und `main()` überschreibt ihn beim nächsten Aufruf genauso. (b) allein lässt ein Programm stehen, dessen **Voreinstellung** eine gesperrte Datei ist, mit einer Sicherung davor; die Sicherung muss dann die Sperrliste kennen, und das ist ein zweiter Ort, an dem die Sperrliste steht.

**Entscheidung — (a) und (b) zusammen, in einer Form, die keine Sperrlistenkenntnis braucht (Begründung nennt kein Ergebnis):**

> **Registertext, Ersteintrag — Schreibregel für Sperrlistenpfade:**
> **(1)** Kein Programm im Repo schreibt an einen Pfad, der auf der Sperrliste steht oder für sie bestimmt ist. **(2)** Jeder Erzeuger einer solchen Datei schreibt **einmalig**: Existiert die Zieldatei bereits, bricht er ab (Rückgabewert ≠ 0), nennt Pfad und Hash der vorhandenen Datei und schreibt nichts. Er überschreibt nie, auch nicht mit identischem Inhalt. **(3)** Ein anderes Ziel nur durch ausdrückliches Argument; die Voreinstellung eines Erzeugers ist nie ein Pfad, der auf der Sperrliste steht. **(4)** Für `faltenplan.py main()`: Voreinstellung weg von `ergebnisse/faltenplan.json` (Sperrlistenpunkt 2) auf einen nicht gesperrten Pfad, und die Einmal-Schreibsperre nach (2). Beides vor jeder weiteren Änderung an `faltenplan.py`, insbesondere vor Z. 336.
>
> **Registertext, Ersteintrag — Sperrlisten-Sonde:**
> Vor dem signierten Tag existiert ein Prüfskript, das für **jeden** Sperrlistenpunkt Pfad und Hash gegen den Registertext prüft und bei einer Abweichung mit Rückgabewert ≠ 0 endet und den Punkt nennt. Der Registertext der Sperrliste ist die Quelle; eine maschinenlesbare Fassung ist Abbild und wird von der Sonde selbst gegen den Registertext geprüft (Bauart 33.3). Die Sonde läuft (a) als Nachweis vor dem Tag, (b) im Laufwrapper vor `auswertung.py`, (c) am Ende jedes Auftrags, der Sperrlisten-nahen Code berührt. Ein Sperrlistenbruch, den die Sonde findet, ist eine Tatsachennotiz — nie eine stille Reparatur.

*Quelle des Grundes:* Zweck der Sperrliste („nichts Gesperrtes ist bewegt worden", Übergabe Abschnitt 5) und A8 (eine Wache ist, was jemand ausführt). Die Einmal-Schreibsperre braucht keine Sperrlistenkenntnis — sie schützt auch die Abbild-Datei, die noch nicht auf der Liste steht, und sie schützt gegen den Fall, den niemand vorausgesehen hat. 21b (3): Prüfungen wandern dorthin, wo geändert werden darf. Kein Ergebnis: Kein Inhalt einer Datei ist berührt; es geht darum, dass keiner berührt werden kann.

*Warum „nie überschreiben, auch nicht mit identischem Inhalt":* Eine Sperre, die bei gleichem Inhalt durchlässt, muss den Inhalt vergleichen — und wer den Vergleich programmiert, entscheidet, was „gleich" heisst (Schlüsselreihenfolge, Zeilenende, `sort_keys`). Die Sperre ist stärker, wenn sie dümmer ist.

**Tatsachennotiz dazu:** `ergebnisse/faltenplan.json` (Hash `0e54ac5c…`) ist seit dem 14.09. unverändert, obwohl `faltenplan.py main()` seit demselben Tag bei jedem Aufruf dorthin schreibt; TB-72 und TB-80 haben eigene Belegskripte verwendet. Der Bestand hielt durch Übung, nicht durch Regel. Der Hash ist am 22.09. gemessen und stimmt.

## 3. Reihenfolge der Handwerksschritte, die jetzt aus 22a und 22b folgen

Alle mit Betreiberfreigabe; die Reihenfolge ist Verfahren, weil jeder Schritt den nächsten absichert:

1. **Sperrlisten-Sonde** schreiben und einmal laufen lassen — Nachweis, dass heute alles stimmt (der Nullpunkt).
2. **`faltenplan.py main()`:** Voreinstellung ändern, Einmal-Schreibsperre einbauen. **Mutationsprobe:** `main()` gegen eine Kopie von `faltenplan.json` am neuen Zielpfad aufrufen → muss abbrechen; Sonde danach → grün.
3. **Erst jetzt** Z. 336 (Bezeichner der Bestätigungsperiode, 22a). Prüfen über `main()` ist ab jetzt ungefährlich; Sonde danach → grün.
4. Abbild-Datei, Faltenplan-Sonde (33.3), Hash auf die Sperrliste — wie geplant; der Erzeuger des Abbilds unterliegt der Schreibregel von Anfang an.

Wer Schritt 3 vor Schritt 2 macht, hat genau den Fall, den ihr beschreibt. Deshalb steht die Reihenfolge hier und nicht nur im Auftrag.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 21l; dazu ANFRAGE 21g, ANFRAGE 22a, `REGISTER_KOPIE_2026-09-21.md` **teilweise** (Kopf, Gliederung, Abschnitt 27 — Prüfung abgebrochen, weil die Kopie bei Commit `2250ed1` / Abschnitt 31 steht und 32–34 nicht enthält; sie ist damit für den Abgleich, um den der Betreiber heute Morgen gebeten hat, zu alt). Nicht gelesen: ANFRAGE 21d, `MAC_TB-82_…`, `MAC_TB-83_…`, `BACKLOG.md`.

---

**Kurz:** (c) ist keine Wache; (a) allein beseitigt den Fall, nicht die Klasse; (b) allein sichert ein Programm ab, dessen Voreinstellung eine gesperrte Datei bleibt. Entscheidung: beides, als allgemeine Schreibregel — kein Programm schreibt Sperrlistenpfade, Erzeuger schreiben einmalig und brechen bei vorhandener Datei ab, Voreinstellungen sind nie gesperrte Pfade — plus eine Sperrlisten-Sonde, die vor dem Tag, im Laufwrapper und nach jedem Sperrlisten-nahen Auftrag läuft. Reihenfolge: Sonde → `main()` absichern (mit Mutationsprobe) → erst dann Z. 336 → Abbild. Die 21.4-Markierung ohne Text bekommt eine Tatsachennotiz „nicht als Beleg verwendbar".

**Unsicher:** ob es bereits ein Prüfskript für die Sperrliste gibt (etwa nach dem Muster `snapshot.py --pruefen`) — dann ist Schritt 1 eine Erweiterung, kein Neubau; ihr seht es im Repo.

---

## In einfacher Sprache

Der steuernde Chat hat eine Falle gefunden: Das Programm, das den Auswertungsplan erzeugt, überschreibt bei jedem normalen Start eine Datei, die laut Regelwerk unveränderlich sein muss. Acht Tage lang ist nichts passiert — weil zufällig niemand das Programm gestartet hat. Fable entscheidet nicht zwischen den drei vorgeschlagenen Wegen, sondern nimmt zwei davon zusammen und macht daraus eine allgemeine Regel: Kein Programm darf an einen geschützten Pfad schreiben, und jedes Programm, das solche Dateien erzeugt, schreibt nur, wenn die Datei noch nicht existiert — sonst bricht es ab. Dazu kommt ein Prüfprogramm, das alle geschützten Dateien gegen ihre Prüfsummen kontrolliert — vor dem Stichtag, vor jedem Lauf und nach jedem Auftrag in der Nähe dieser Dateien. Und eine Reihenfolge: erst die Prüfung, dann das Programm absichern, erst dann die Zeile ändern, die Fable gestern angeordnet hat.
