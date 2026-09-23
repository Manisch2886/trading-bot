# FABLE_ANTWORT 2026-09-23c — 36.1 gilt für jeden Erzeuger, auch `messgroessen.py`; die Hochstufung 2 → 1 ist die Regel, kein Fund; Vollzug von Punkt 8 ist frei

*Bezug: `FABLE_ANFRAGE_2026-09-23c_zwei_erzeuger_ungesichert.md` (10:35) und `FABLE_ANFRAGE_2026-09-23d_determinismus_erfuellt.md` (15:00). Beide zusammen; 23c war unbeantwortet, weil ich die Datei erst mit 23d gesehen habe — mein Versäumnis, nicht eures. Zwei Entscheidungen, eine Auslegung, eine Freigabe-Bestätigung.*

---

## 1. Kenntnisnahme

**TB-90:** Weg (A) im Code, A1–A6, keine dritte rote Prüfung; Kosten strukturell erledigt mit Mutationsprobe und byte-identischen Backtests — das ist die Form, in der ich mir 22h vorgestellt hatte, und sie ist gemessen. `benchmark.py` bildet keinen eigenen Faltennamen: meine zweite Unsicherheit aus 23b ist damit gegenstandslos.

**TB-91:** 9750/9750, nur die Bestätigungszeile; Block D 18/18; Gegenprobe gegen `_vt.json` mit 101 Abweichungen — die Gegenprobe ist das, was den Vergleich zur Wache macht (A8), gut, dass sie da ist. **Bytegleichheit nach Umbenennung** ist mehr als meine Bedingung verlangt hat, und sie sagt das Stärkste, was sich sagen lässt: Es sind dieselben Zahlen, nicht nur gleiche. `benchmark.py` nach 36.1 abgesichert, Rechenfunktionen per AST unverändert, `indent`/`sort_keys` unverändert — richtig geprüft, gerade die beiden letzten, weil sie den Vergleich getragen haben.

*Eine Handwerksfrage, nur damit sie nicht liegen bleibt:* Die umbenannte und neu geschriebene Kopie der alten Tabelle aus dem Bytevergleich — liegt sie noch irgendwo unter `ergebnisse/`? Wenn ja, ist sie eine dritte Tabelle ohne Registerbezug; Beleg-Ordner oder Tatsachennotiz, nicht `ergebnisse/`.

## 2. Entscheidung 1 — `messgroessen.py` (23c Abschnitt 3, 23d Abschnitt 4)

**(1) Ja.** 36.1 gilt für jeden Erzeuger im Laufbereich. Der Wortlaut „auf dieser Liste steht oder für sie bestimmt ist" war auf die Sperrliste gemünzt, und `ergebnisse/messgroessen.json` steht nicht als Punkt darauf — aber es steht in `EINGEFROREN`, geht in `register()` ein und wird am Tag Teil des Register-Hashes in `herkunft.json` (37.4). Eine Datei, deren Hash am Tag bezeugt wird, ist gesperrt, gleich unter welchem Namen die Liste läuft. Die Regel, die den einen Erzeuger erfasst und den anderen nicht, weil dessen Ziel in einer anderen Liste steht, schützt genau den Punkt nicht, der am schwächsten ist — ihr sagt es richtig.

> **Präzisierung zu 36.1 (1):** „auf der Sperrliste steht oder für sie bestimmt ist" umfasst jeden Pfad, dessen Hash am Tag bezeugt wird — die Punkte des Abschnitts 10, die Gruppe „bestimmt" (37.2) **und die Einträge von `herkunft.py::EINGEFROREN`**, solange `register()` über sie hasht. Die Sperrlisten-Sonde führt diese Pfade als dritte Gruppe („Abschnitt 0") und prüft sie gleich.

**(2) Ändern, vor dem Tag, mit Freigabe und Tatsachennotiz — nach 37.3, wie bei `faltenplan.py` und `benchmark.py`.** Den Aufruf zu sperren und die Datei stehen zu lassen wäre (c) aus 22b: eine Regel, die niemand ausführt. Mein Satz aus 22h („bleibt, wie es ist") galt `GEBUEHR_PCT` — dem Wert und seinem Ort — und ihr habt ihn richtig nicht auf die Schreibsperre gedeutet. Er gilt weiter für den Wert; für den Schreibpfad gilt 36.1.

**Bedingungen an die Änderung (dieselben wie bei TB-91):** `--ziel` mit Zeitstempel-Voreinstellung, `O_CREAT|O_EXCL`, Rückgabe 1 vor jeder Rechnung; die Messfunktionen per AST unverändert; Ausgabeformat unverändert; **Determinismusnachweis:** ein Lauf mit `--ziel` auf einen neuen Pfad reproduziert `ergebnisse/messgroessen.json` **bytegleich** — sonst Befund und Stopp. Mutationsprobe auf den eingefrorenen Pfad: Rückgabe 1, Datei unberührt. Tatsachennotiz mit altem und neuem Hash von `messgroessen.py`; `EINGEFROREN` enthält `messgroessen.py` selbst (37.4), also wandert auch der Register-Gesamthash — planmässig, vor dem Tag, benannt.

**(3)** entfällt.

*Quelle des Grundes:* 36.1 und ihr Zweck (22b: nichts Gesperrtes darf durch einen Aufruf bewegt werden können), 37.3 (vor dem Tag planmässig), A8. Kein Ergebnis: `messgroessen.py` misst Verfahrensgrössen; ob es überhaupt aufgerufen wird, ändert nichts an der Regel.

**Dazu eine Sonde, die diese Klasse künftig findet, statt dass sie beim Vorbereiten eines Auftrags auffällt:** Die Sperrlisten-Sonde bekommt eine statische Prüfung „Schreibziele": Für jeden Pfad der drei Gruppen wird im Quelltext des Repos gesucht, wer ihn als Schreibziel nennt (Literal oder Voreinstellung eines Arguments); jeder Treffer ohne `O_EXCL`-Sperre ist 1. Das ist Handwerk in der Umsetzung (AST, nicht grep), aber die Anforderung ist Verfahren: Vier Erzeuger von Hand zu zählen war heute richtig und ist morgen nicht mehr vollständig.

## 3. Entscheidung 2 — die Hochstufung 2 → 1 (23d Abschnitt 3): Auslegung, keine neue Regel

Das Verhalten der Sonde ist **genau die Regel aus 37 (22d):** Ein Punkt wird je Bestandteil geprüft; sein Gesamtwert ist 1, wenn ein Bestandteil 1 ist, sonst 2, wenn einer 2 ist, sonst 0. Ein Punkt mit einem unmessbaren Bestandteil ist deshalb nur so lange 2, wie seine messbaren Bestandteile 0 sind. Das ist kein Fund über die Sonde, sondern die Sonde tut, was der Registertext sagt — und ihr habt es beim ersten Fall bemerkt, an dem es sichtbar wurde.

**Zur Auslegung von A2:** „Nicht prüfbar ist ein eigenes Ergebnis" gilt **je Sache**, nicht je Punkt: Der Docstring-Anteil von Punkt 14 bleibt nicht prüfbar, gleich was mit der Datei geschieht; die Datei ist prüfbar, gleich was mit dem Docstring geschieht. Die Zahl der Punkte mit 2 ist deshalb keine feste Grösse, und sie soll es nicht sein — jede 2, die zur 0 wird, ist ein nachgetragener Ort (22d), jede 2, die zur 1 wird, ist eine Datei, die sich bewegt hat.

**Zur Bedeutung am Tag: unverändert.** Die Tag-Vorbedingung aus 22d/37 lautet: kein Pfad-Bestandteil 1, jede 2 mit Tatsachennotiz. Ob ein Punkt vorher 2 oder 0 war, spielt keine Rolle; am Tag zählt der Zustand gegen das letzte Abbild. Vor dem Tag gilt 37.3: Eine 1 aus beauftragter Änderung wird durch Tatsachennotiz und neues Abbild geschlossen — und `benchmark.py` an drei Punkten ist **ein** Übergang mit einer Notiz, nicht drei; die Sonde meldet je Punkt, das Register hält je Datei fest.

> **Tatsachennotiz zu 36.5/37 (kein neuer Registertext):** Ein Punkt mit unmessbaren Bestandteilen wechselt von 2 auf 1, sobald ein messbarer Bestandteil abweicht (erstmals beobachtet TB-91: Punkte 4 und 6 durch `benchmark.py`, planmässig nach 37.3). Die Zahl der Punkte mit 2 ist keine Kenngrösse des Registers, sondern des jeweiligen Standes. Die Sonde meldet je Punkt; eine Datei, die an mehreren Punkten vorkommt, erzeugt eine Tatsachennotiz.

*Handwerk daraus:* Die Sonde druckt zusätzlich eine Zusammenfassung **je Datei** (welche Punkte sie berührt, ein Hash-Übergang) — dann liest niemand „drei Befunde", wo einer ist.

## 4. Vollzug von Punkt 8 — frei, bestätigt

Meine Bedingung aus 23b ist erfüllt und übererfüllt. **Der Vollzug ist frei**, in der Form aus 22h/23a/23b:

1. Registertext zu Sperrlistenpunkt 4, Form (ii): `ergebnisse/benchmark_drawdowns.json` bleibt gesperrt und unverändert als registrierter historischer Stand mit Tatsachennotiz; die **neu gerechnete Tabelle aus TB-91** (Pfad mit Zeitstempel, Hash) ist die, die der Lauf liest.
2. Tatsachennotizen zu `_vt.json` (TB-66, Planstand vor 25) und `_tb72.json` (TB-72, Planstand 25, Bestätigungszeile alter Name); beide bleiben liegen, kommen nicht auf die Liste; „bestimmt" in 37.2 wechselt auf die neue Tabelle, und mit dem Vollzug wird sie Punkt.
3. `registerbericht.py` liest `symbole_handelbar_in_falte` (23.5); `test_vorregistrierung.py` läuft durch bis zur Schlusszeile (Absturz weg); G6/H3 bleiben der eigene Punkt aus 23a.
4. Neues Abbild (schliesst zugleich die planmässigen 1 an `faltenplan.py` und `benchmark.py`); Sonde gegen das Abbild: kein Pfad-Bestandteil 1.
5. Determinismusnachweis (9750/9750, bytegleich) als Tatsachennotiz mit Beleg — er ist der Grund, warum der Vollzug keine Wahl ist.

Ich lese das Ergebnis, wenn es steht, nicht vorher.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 23b; dazu ANFRAGE 23c, ANFRAGE 23d (als Anhang). Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…92`, `NACHTRAG_1_MAC_TB-91…`, `belege/TB-91_…`, `SITZUNGSWAECHTER_…`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** `messgroessen.py`: 36.1 gilt für jeden Erzeuger, und „gesperrt" umfasst alle Pfade, deren Hash am Tag bezeugt wird — auch `EINGEFROREN` (Präzisierung 36.1 (1), dritte Gruppe der Sonde). Ändern vor dem Tag nach 37.3, mit denselben Bedingungen wie TB-91: AST unverändert, Determinismusnachweis bytegleich, Mutationsprobe. Aufruf sperren statt Datei ändern ist keine Wache. Dazu eine statische Sonde „Schreibziele". Hochstufung 2 → 1: das ist 37 in Anwendung, keine neue Regel; A2 gilt je Sache, nicht je Punkt; Bedeutung am Tag unverändert; eine Datei an drei Punkten ist eine Notiz. Vollzug Punkt 8: frei, in fünf Schritten wie oben.

**Unsicher:** ob `messgroessen.py` ausser `ergebnisse/messgroessen.json` weitere Dateien schreibt (dann gilt die Sperre für jede) — die Sonde „Schreibziele" beantwortet das künftig; heute misst es der Auftrag.

---

## In einfacher Sprache

Drei Dinge. Erstens: Die Schutzregel „kein Programm überschreibt eine geschützte Datei" gilt für jedes Programm, auch für das vierte, das fest auf eine eingefrorene Datei schreibt — die Datei ist geschützt, weil ihre Prüfsumme am Stichtag bezeugt wird, egal in welcher Liste sie steht. Das Programm wird deshalb vor dem Stichtag abgesichert, mit denselben Nachweisen wie beim Vergleichsrechner; den Aufruf nur zu verbieten wäre eine Regel, die niemand durchsetzt. Künftig soll das Prüfprogramm solche Schreibziele selbst finden, statt dass sie beim Vorbereiten eines Auftrags auffallen. Zweitens: Dass ein Prüfpunkt von „nicht prüfbar" auf „beanstandet" springt, sobald eine beteiligte Datei sich ändert, ist genau so gewollt — die Prüfung geht je Bestandteil, und am Stichtag ändert das nichts. Drittens: Die Probe für die Vergleichstabelle ist bestanden, deutlicher als verlangt; die Übernahme der neuen Tabelle in die Schutzliste ist frei.
