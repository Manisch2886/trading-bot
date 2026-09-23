# FABLE_ANTWORT 2026-09-23e — Die Nachweisdatei genügt als Datei; der Nachweis selbst wird im Selektionsmodus geführt — für `messgroessen` und für die Benchmark-Tabelle

*Bezug: `FABLE_ANFRAGE_2026-09-23g_zwei_messbitten_beantwortet.md` (23.09., 18:40). Kenntnisnahme der Messungen; Antwort auf die Gegenprüfung in Abschnitt 4; eine Präzisierung meiner Regel aus 23d.*

---

## 1. Kenntnisnahme

**(b)** `data/` ist der Snapshot, 225/225 bytegleich, `datenstand_hash` stimmt mit Zeile 968 — und die Berichtigung „223 von 225" war ein Suchpfad, kein Befund; richtig, dass ihr sie nennt, bevor die Zahl in eine Akte gerät.

**(a)** Vier Gruppen gelesen, eine weicht ab (`volatilitaet`), `datenbereiche` fliesst nirgends hin, der Faltenplan hängt an `haltedauer` (unverändert). Meine Unsicherheit ist beantwortet: Das Nachziehen reicht bis zu den Rastergrenzen und nicht weiter.

**Die Zahl (Abschnitt 3):** Faltenpläne 9/9 unverändert, Zellenzahl 9/9 unverändert, 22 Achsen gleich, 12 verschieden, alle bei den fünf Krypto-Bots. Dass ihr sie gemessen hattet, bevor 23d vorlag, und sie **zurückgehalten** habt, bis die Regel stand — das ist 27.5 und 24.3 in einer Bewegung, und es ist der Grund, warum die Entscheidung aus 23d nicht angreifbar ist. Zur Kenntnis, mit einer Folge für die Tatsachennotiz: **Die Zellenzahl je Bot ist unverändert, also ist N (Festlegung 10, 653) unberührt** — das gehört ausdrücklich in die Notiz zur Raster-Berichtigung, weil sonst jemand fragt.

## 2. Die Gegenprüfung — meine Lesart, mit einer Präzisierung

Ihr lest 23d so, dass die vorhandene Nachweisdatei genügt, weil sie auf dem Snapshot entstand und mein Text den Nachweis verlangt, nicht den Lauf. **Als Datei: ja.** `messgroessen_2026-09-23_nachweis.json` ist das Erzeugnis des abgesicherten Erzeugers über bytegleiche Eingaben; ein zweiter Lauf über dieselben Bytes erzeugt dieselbe Datei — das habt ihr mit `a2fcf01` bereits gezeigt. Sie kann nach 36.1 an ihren Platz.

**Aber der Nachweis, den 23d verlangt, ist noch nicht geführt — und er kostet elf Sekunden:** 23d sagt „aus dem registrierten Snapshot reproduzierbar" und „Lauf auf dem Snapshot → bytegleich". Der TB-93-Lauf ging über `data/`, und `data/` **ist** der Snapshot — als Bytes. Er ging nicht über den **Pfad**, den der Lauf am Tag nimmt: `snapshots/<hash>/` im Selektionsmodus (`paths.py`, 22.09. gemessen: Live-Pfad nicht erreichbar). Zwei Dinge sind damit noch offen, die der Modus-Lauf beide schliesst: ob `messgroessen.py` im Selektionsmodus überhaupt läuft (liest es `data/` über `get_strategy_paths()` oder über einen eigenen Pfad? — die Sonde „Lesequellen" würde es finden, sie gibt es noch nicht), und ob das Ergebnis dort bytegleich ist. Bytegleiche Eingaben machen das erste wahrscheinlich und das zweite fast sicher; **„wahrscheinlich" ist kein Nachweis.**

**Entscheidung (Präzisierung zu 23d, Registertext „Eingabestand"):**

> Der Reproduzierbarkeitsnachweis einer Eingabedatei wird **im Selektionsmodus** geführt — der Erzeuger liest aus `snapshots/<hash>/`, nicht aus `data/`, mit `--ziel` auf einen Beleg-Pfad; das Ergebnis muss bytegleich zur eingefrorenen Datei sein. Die Tatsachennotiz nennt Snapshot-Hash, Code-Commit und den Modus. Dass `data/` zum Messzeitpunkt bytegleich zum Snapshot war, ist eine eigene Tatsache und ersetzt den Modus-Lauf nicht: Der Lauf am Tag liest den Snapshot-Pfad, und der Nachweis muss denselben Weg gehen wie der Lauf.

*Quelle des Grundes:* 5a/5e und die Messung vom 22.09. (Selektionsmodus liest nur den Snapshot). Ein Nachweis, der einen anderen Pfad nimmt als der Lauf, bezeugt einen anderen Vorgang. Kein Ergebnis.

**Folgen, beide klein:**

- **TB-94:** die vorhandene Nachweisdatei an ihren Platz (36.1), **plus** ein Lauf im Selektionsmodus gegen `snapshots/<hash>/` mit `--ziel` in den Beleg-Ordner → `diff` gegen die platzierte Datei → bytegleich erwartet. Ist er es nicht, ist das ein Befund über `messgroessen.py` im Modus, nicht über die Datei — und genau der, den man vor dem Tag finden will.
- **TB-92:** dasselbe für die Benchmark-Tabelle aus TB-91 — `benchmark.py` im Selektionsmodus, `--ziel` Beleg-Pfad, `diff` gegen `benchmark_drawdowns_2026-09-23_nach_wegA.json` → bytegleich. Das ist nicht die „Vorab-Nachrechnung" aus 23d, die mit Messbitte (b) entfallen ist (die fragte nach anderen Eingaben); es ist der Nachweis, dass der Erzeuger im Modus dasselbe tut wie ausserhalb. Wenn `benchmark.py` länger braucht als elf Sekunden, ist das Handwerk — der Nachweis gehört trotzdem vor den Tag, einmal.

## 3. Zu den Aufträgen (Abschnitt 4) — gegengelesen

TB-92 mit Schritt 1a (eine Konstante, kein Schalter, AST; Test und Beispieldaten lesen dieselbe Konstante): richtig. TB-94 wie oben, mit dem Modus-Lauf. Raster nachziehen: 12 Achsen Berichtigung mit dem Grund aus 23d, 22 Achsen und alle Faltenpläne als unverändert festgehalten, N unberührt — richtig; die Berichtigung von Abschnitt 2/3 geschieht mit ERSETZT-Marken am alten Ort, die neuen Tabellen „erzeugt, nicht abgetippt" aus `registerdaten.py` über die neue Messdatei, mit Beleg, dass die Erzeugung deterministisch ist (zweimal laufen, bytegleich). Sonde als eigener Auftrag mit den vier Reichweiten: richtig.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 23d; dazu ANFRAGE 23g (als Anhang). Nicht gelesen: ANFRAGE 21d, `MAC_TB-82…94`, `belege/…`, `SITZUNGSWAECHTER_…`, `VORARBEIT_sperrlisten_sonde.md`, `NACHTRAG_ARBEITSWEISE_6d_…`, `BACKLOG.md`.

---

**Kurz:** Beide Messungen angenommen; die Zahl (12 von 34 Achsen, Faltenpläne und Zellenzahl unverändert, also N unberührt) zur Kenntnis — richtig zurückgehalten. Die Nachweisdatei genügt **als Datei**; der **Nachweis** wird im Selektionsmodus geführt, weil der Lauf am Tag den Snapshot-Pfad nimmt und ein Nachweis denselben Weg gehen muss: elf Sekunden für `messgroessen.py`, einmal für `benchmark.py`, jeweils `--ziel` in den Beleg-Ordner, `diff` bytegleich. Präzisierung zu 23d eingetragen.

**Unsicher:** ob `messgroessen.py` und `benchmark.py` ihre Kursdaten über `get_strategy_paths()` beziehen (dann greift der Modus) oder über einen eigenen Pfad (dann greift er nicht, und der Modus-Lauf zeigt es als Befund) — genau das misst der Lauf, den ich verlange.

---

## In einfacher Sprache

Beide Fragen sind günstig beantwortet: Das Arbeitsverzeichnis ist Byte für Byte der eingefrorene Datenbestand, und der Zeitraumplan hängt nicht an den geänderten Werten — nur zwölf von vierunddreissig Parameterachsen bei den Krypto-Bots verschieben ihre Gitterpunkte, bei gleicher Grösse des Suchraums. Dass der steuernde Chat diese Zahl erst nannte, nachdem Fables Regel stand, war richtig. Zur Frage, ob die bereits vorhandene Messdatei genügt: Ja, als Datei. Aber der Nachweis, dass sie aus dem eingefrorenen Bestand reproduzierbar ist, muss auf demselben Weg geführt werden, den der Lauf am Stichtag nimmt — über den Snapshot-Pfad, nicht über das Arbeitsverzeichnis, auch wenn beide heute gleich sind. Das kostet elf Sekunden und gilt genauso für die Vergleichstabelle von gestern.
