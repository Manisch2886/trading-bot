# FABLE_ANTWORT 2026-09-22c — Drei Ausgänge für jede Sonde; kein vorhandener Listenrest wird das Abbild der Sperrliste

*Bezug: `FABLE_ANFRAGE_2026-09-22b_sonde_bestand.md` (22.09., 07:35). Antworten auf Frage 1 und 2; zu 0 Kenntnisnahme. Frage 1 berichtigt meinen eigenen Text aus 22b.*

---

## 0. Kenntnisnahme

TB-83 durch, (6) und (7) zeichengleich; TB-84 mit Schreibregel, Sonde, Reihenfolge und 21.4-Notiz — einverstanden. Schritt 1 ist Neubau nach Muster, `herkunft.py` scheidet als Ort aus: angenommen, und es bestätigt die Bauart aus 22b (Sonde als eigene, nicht gesperrte Datei).

## Frage 1 — Drei Ausgänge: ja, und nicht nur für diese Sonde

Mein „Rückgabewert ≠ 0" war zu grob, und der Kopf von `snapshot.py` sagt genau, warum: Ein gescheiterter Aufruf und ein Befund sahen in TB-45 gleich aus. A2 verlangt, dass „konnte nicht messen" ein eigenes Ergebnis ist; ein Rückgabewert, der Befund und Nichtprüfbarkeit zusammenlegt, ist keine Wache im Sinn von A8, weil niemand am Wert erkennen kann, ob gemessen wurde.

**Entscheidung — Berichtigung zu 22b (Sperrlisten-Sonde) und allgemeine Regel (Begründung nennt kein Ergebnis):**

> **Registertext, Ersteintrag — Ausgänge von Sonden und Wachen:**
> Jede Sonde und jede Wache des Verfahrens (Sperrlisten-Sonde, Faltenplan-Sonde nach 33.3, Einmal-Schreibsperre der Erzeuger, Wache nach 29.4, Laufwrapper) endet mit genau einem von drei Rückgabewerten, Bauart `snapshot.py --pruefen`: **0** = geprüft und in Ordnung; **1** = geprüft und **Befund** (Abweichung, Verweigerung, Abbruch nach Regel); **2** = **nicht prüfbar** (Eingabe fehlt, Quelle nicht lesbar, Aufruf gescheitert). Ein Wrapper behandelt 1 und 2 verschieden: 1 ist eine Tatsachennotiz mit dem genannten Punkt; 2 ist kein Ergebnis und darf nirgends als „bestanden" oder „nicht bestanden" geführt werden. Kein Aufruf endet mit 0, ohne dass gemessen wurde.
>
> **Berichtigung zu 22b, Sperrlisten-Sonde:** „mit Rückgabewert ≠ 0 endet und den Punkt nennt" lies „mit Rückgabewert 1 endet und den Punkt nennt; kann ein Punkt nicht geprüft werden (Datei fehlt, Registertext nicht lesbar), endet sie mit 2 und nennt ihn".

*Quelle des Grundes:* A2 und A8, im Register vorhanden; der Vorfall TB-45, im Kopf von `snapshot.py` dokumentiert. Kein Ergebnis.

*Zur Einmal-Schreibsperre:* Der Erzeuger, der wegen vorhandener Zieldatei nicht schreibt, endet mit **1** — er hat geprüft und einen Befund („Ziel existiert, Hash …"). Nicht mit 2: Er konnte prüfen. Das ist die Wache, die ihre Arbeit tut; der Wert 1 sagt es dem Aufrufer.

## Frage 2 — Keine der beiden Listen wird das Abbild

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Registertext, Ersteintrag — Abbild der Sperrliste:**
> Das Abbild der Sperrliste ist eine **eigene, neue Datei** (Handwerk: Name, Form), die genau die Punkte des Registerabschnitts 10 mit Pfad und Hash trägt — nicht mehr, nicht weniger (Bauart 33.3). Sie wird einmalig geschrieben (Schreibregel 22b); jede Fortschreibung der Sperrliste vor dem Tag erzeugt ein neues Abbild unter neuem Namen, das alte bleibt. Das aktuelle Abbild steht selbst mit Hash im Register. Die Sperrlisten-Sonde prüft (i) jeden Punkt des Abbilds gegen die Datei im Repo und (ii) das Abbild gegen den Registertext von Abschnitt 10; weicht das Abbild vom Registertext ab, ist das ein Befund (1), kein Anlass zur Anpassung des Abbilds ohne Registereintrag.
>
> `herkunft.py` `EINGEFROREN` (Z. 57) und `SPERRLISTE_DATEIEN` (Z. 66) sind **nicht** das Abbild der Sperrliste und werden nicht dazu. Beide erhalten eine Tatsachennotiz zu Abschnitt 10: Was sie sind, wer sie liest, was daraus entsteht, und dass sie mit dem Registertext an fünf Stellen nicht übereinstimmen (zwei Dateien fehlen, drei stehen zusätzlich).

*Quelle des Grundes — drei, alle aus dem Bestand:* **(1)** Beide Listen liegen in `herkunft.py`, das mit Punkt 11/12 auf der Sperrliste steht. Ein Abbild, das mit der Sperrliste wachsen muss (Abbild-Datei, Erzeuger, Sonde kommen noch hinzu), kann nicht in einer Datei liegen, die nicht geöffnet werden darf. **(2)** Sie weichen heute vom Registertext ab, und ihr Zweck ist nirgends registriert — eine Liste, von der man nicht weiss, was sie darstellen soll, kann nicht zum Abbild von etwas erklärt werden. **(3)** Der Registertext ist die Quelle (30.2 (2) sinngemäss): Ein Abbild wird aus ihm gebildet und gegen ihn geprüft, nicht aus einer vorhandenen Datei übernommen, weil sie schon da ist. Kein Ergebnis.

**Was der Fund bedeutet, und was er nicht bedeutet:** Der Zustand „maschinenlesbare Fassung weicht vom Registertext ab, und niemand hat sie geprüft" besteht — ihr sagt es richtig — heute schon. Er ist **kein Sperrlistenbruch**: Die Dateien selbst sind unverändert (Hashes stimmen). Er ist eine **Lücke im Nachweis**, wenn `herkunft.py` aus diesen Listen die Hashes bildet, die in `herkunft.json` als Herkunft des Laufs stehen — dann fehlen dort `benchmark_drawdowns_vt.json` und die beiden Universumsdateien, und drei Dateien stehen drin, die kein Sperrlistenpunkt sind. Ob das so ist, weiss ich nicht — **das ist die Messung, die ich brauche:**

> **Nur das Ob:** Welche Funktionen von `herkunft.py` lesen `EINGEFROREN` und `SPERRLISTE_DATEIEN`, und in welche Ausgabe (Datei, Feld) gehen die daraus gebildeten Hashes ein? Läuft `register()` oder `datenstand()` (Punkt 11/12) über diese Listen?

Erst danach lässt sich die Tatsachennotiz schreiben — und erst danach die Frage stellen, ob `herkunft.py` vor dem Tag geöffnet werden muss. **Meine Linie dazu, vorab und nicht als Entscheidung:** Nach 21b (3) nicht öffnen, wenn die Sperrlisten-Sonde die Lücke schliesst — `herkunft.json` bezeugt dann eine Teilmenge, die Sonde die ganze Sperrliste, und die Tatsachennotiz sagt, welches Dokument was bezeugt. Öffnen nur, wenn `herkunft.json` ohne die fehlenden Punkte als Herkunftsnachweis des Laufs nicht taugt. Das entscheide ich, wenn die Messung vorliegt.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 22b; dazu ANFRAGE 22b. Nicht gelesen: ANFRAGE 21d, `MAC_TB-82_…`, `MAC_TB-83_…`, `BACKLOG.md`; `REGISTER_KOPIE_2026-09-21.md` nur bis Abschnitt 27 (Kopie steht bei 31, zu alt für den Abgleich).

---

**Kurz:** Frage 1: ja — drei Ausgänge (0 in Ordnung / 1 Befund / 2 nicht prüfbar) als Regel für **alle** Sonden und Wachen, Bauart `snapshot.py`; mein „≠ 0" aus 22b ist berichtigt; die Schreibsperre endet mit 1. Frage 2: keine der beiden Listen — sie liegen in gesperrtem Code, weichen vom Registertext ab, und ihr Zweck ist nicht registriert. Neues Abbild, einmalig geschrieben, selbst mit Hash im Register, von der Sonde gegen Repo **und** Registertext geprüft; die alten Listen bekommen eine Tatsachennotiz. Dafür eine Messung: Wer liest die beiden Listen, und was entsteht daraus? Danach entscheide ich, ob `herkunft.py` geöffnet werden muss — Linie: nicht, wenn die Sonde die Lücke schliesst.

**Unsicher:** ob Abschnitt 10 in einer Form vorliegt, aus der ein Programm Pfad und Hash je Punkt zuverlässig lesen kann (Prüfung (ii) der Sonde). Wenn nicht, ist der Abgleich Abbild↔Registertext eine Prüfung mit Beleg im Auftrag statt einer Codezeile — Handwerk, aber ihr müsst es wissen, bevor ihr die Sonde beauftragt.

---

## In einfacher Sprache

Zwei Fragen. Erstens: Soll das neue Prüfprogramm wie das vorhandene Vorbild drei Antworten kennen — „in Ordnung", „Abweichung gefunden", „konnte nicht prüfen"? Ja, und zwar nicht nur dieses Programm, sondern jede Prüfung im Verfahren. Der Grund steht im Vorbild selbst: Früher haben zwei Prüfungen „bestanden" gemeldet, obwohl sie gar nichts gemessen hatten. Fables eigene Vorgabe von gestern war zu grob und ist berichtigt.

Zweitens: In einem geschützten Programm liegen schon zwei Listen geschützter Dateien, die aber nicht zum Regelwerk passen. Soll eine davon die offizielle maschinenlesbare Liste werden? Nein — sie liegen in einer Datei, die man nicht mehr anfassen darf, sie stimmen nicht, und niemand hat aufgeschrieben, wozu sie da sind. Es wird eine neue Liste aus dem Regelwerk gebildet und von der Prüfung sowohl gegen die Dateien als auch gegen das Regelwerk kontrolliert. Die alten Listen bekommen einen Vermerk. Offen ist, ob aus ihnen heute der Herkunftsnachweis des Laufs gebildet wird — dann fehlen dort zwei Dateien. Das soll nachgemessen werden, bevor Fable entscheidet, ob das geschützte Programm dafür geöffnet werden muss.
