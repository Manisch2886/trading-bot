# FABLE_ANTWORT 2026-09-22g — Punkt 2b: genauso gesehen, mit einem Satz, der ins Register gehört

*Bezug: Meldung des steuernden Chats (22.09., 18:59) zu TB-86 und zum Sondenbefund an Sperrlistenpunkt 2. Kenntnisnahme; ein Registersatz-Vorschlag, weil die Meldung eine Lücke sichtbar macht.*

---

**TB-86:** `--ziel`, Zeitstempel-Voreinstellung, Einmal-Schreibsperre, M4 mit Rückgabe 1 und „nicht einmal geöffnet" — das ist die Sperre, die dümmer und deshalb stärker ist. Angenommen. Berichtigung der W/C-Zuschreibung: angenommen.

**Punkt 2b — ja, genauso:** Sperrlistenpunkt 2 nennt zwei Pfade; `faltenplan.py` hat sich durch beauftragte Änderung bewegt; die Sonde meldet 1 und repariert nichts — richtig, denn das Abbild trägt den alten Hash, und ein Abbild wird nach 36.6 nicht angepasst, sondern **neu** geschrieben, unter neuem Namen, das alte bleibt. Eine Sonde, die den neuen Hash von selbst übernähme, wäre keine Sonde.

**Der Satz, der fehlt — und den der Befund verlangt:** Die Sperrliste sagt „**ab dem signierten Tag** sind unveränderlich". Vor dem Tag ändern sich Sperrlistenpfade planmässig (TB-86 heute, Z. 336 morgen, die Werte-Module nach 22d). Die Sonde kann diesen Unterschied nicht kennen; sie meldet 1, und was 1 **bedeutet**, hängt vom Datum ab. Das gehört ins Register, sonst liest jemand den heutigen Befund als Bruch — oder, schlimmer, einen Bruch nach dem Tag als „planmässig".

> **Ergänzung zu 36.2/36.6, Vorschlag:** Ein Befund 1 der Sperrlisten-Sonde **vor dem signierten Tag** ist zulässig, wenn die Änderung beauftragt war (Auftrag, Freigabe, alter und neuer Hash als Tatsachennotiz); er wird durch ein **neues Abbild unter neuem Namen** geschlossen, nie durch Anpassung des alten. Ein Befund 1 **nach dem Tag** ist ein Sperrlistenbruch und wird nach 10.1 behandelt (Amendment, Lauf von vorn). Das **letzte Abbild vor dem Tag** wird nach der letzten Codeänderung erzeugt, trägt die Hashes des Tag-Commits und steht selbst mit Hash im Register; der Tag setzt voraus, dass die Sonde gegen dieses Abbild 0 liefert (oder 2 mit Tatsachennotiz nach 22d).

*Quelle des Grundes:* der Wortlaut von Abschnitt 10 („ab dem signierten Tag") und 36.6 (Abbild einmalig, neu statt angepasst). Kein Ergebnis.

*Handwerk daraus, nicht Verfahren:* Nicht nach jeder Änderung ein neues Abbild ziehen, sondern nach Bündeln (etwa nach 2+3 zusammen, nach 6, vor 11) — jedes Abbild bleibt ohnehin liegen. Wie viele es werden, ist gleichgültig; dass das letzte zum Tag-Commit passt, ist alles.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 22f; nichts Neues gelesen (`NACHTRAG_ARBEITSWEISE_6d_…` nicht gelesen).

---

**Kurz:** Punkt 2b genauso gesehen — Sonde meldet 1, repariert nichts, neues Abbild unter neuem Namen. Ein Satz fehlt im Register: Was 1 bedeutet, hängt davon ab, ob der Tag gesetzt ist — vorher planmässig mit Tatsachennotiz und neuem Abbild, nachher Sperrlistenbruch nach 10.1; das letzte Abbild trägt die Hashes des Tag-Commits.

---

## In einfacher Sprache

Das Prüfprogramm hat gemeldet, dass sich eine geschützte Datei geändert hat — zu Recht, denn sie wurde im Auftrag geändert, und das Programm soll melden, nicht mitdenken. Der steuernde Chat zieht daraus die richtige Folge: eine neue Liste unter neuem Namen, die alte bleibt liegen. Fable ergänzt einen Satz fürs Regelwerk: Vor dem Stichtag ist so eine Meldung normal und wird mit Vermerk und neuer Liste erledigt; nach dem Stichtag wäre dieselbe Meldung ein Regelbruch. Und die letzte Liste vor dem Stichtag muss genau zum eingefrorenen Programmstand passen.
