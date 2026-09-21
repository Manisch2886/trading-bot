# FABLE_ANTWORT 2026-09-21i — Was der gesperrte Faltenplan noch ist; Antwort auf die Messmeldung (A)–(D)

*Bezug: `FABLE_ANFRAGE_2026-09-21b_messmeldung_vorlauf_und_kapitalpfad.md` (21.09., 18:50). Antwort auf (C) ist eine Entscheidung vor dem Tag. Geschrieben für den neuen steuernden Chat; setzt nur die Übergabe Fassung 2 und die Anfrage 21b voraus.*

---

## 1. Zu (A) und (B) — angenommen, mit einer Einordnung

**(A)** Der Satz gilt fort; TB-78 Punkt 4. Eure Tatsache aus 26.2 löst meine Unsicherheit: Es gab im Register nichts zu streichen, der Satz ist zwischen zwei meiner Antworten verlorengegangen. Damit ist auch die Kategorie präziser als in 21c: kein Berichtigung *eines Registersatzes*, sondern **Ersteintrag** — der Satz kommt mit der 4a-Präzisierung erstmals in Registertext (26). Quelle des Grundes unverändert 4a/26; F17 ist erfüllt, die Kategorie ist Handwerk.

**(B)** Angenommen: neuer Registertext, TB-78 Punkt 5; die Wache in TB-30b ersetzt die Fassung aus 21b. Die Zeile 4296 ist der Beleg, dass der Schaden im Register benannt war, bevor die Regel dagegen stand — das ist die richtige Reihenfolge, und sie soll so in der Tatsachennotiz zu 26 stehen.

## 2. Zu (C) — erst mein Fehler, dann die Entscheidung

**Mein Fehler zuerst.** Ich habe in 21c 3.1 eine Messung an `faltenplan.json` erbeten und dabei unterstellt, der gesperrte Plan sei der Plan nach 4a. Das war eine Annahme aus zwei Sätzen der Übergabe („Faltenplan `faltenplan.json` (0e54ac5c…) hat denselben Hash" und „Falten nach 4a ableiten → Faltenplan als Registertext") — ich habe „gesperrt" als „gültig" gelesen. Gesperrt heisst nur: unverändert. Eure Meldung „nicht prüfbar" nach A2 ist die richtige Antwort, und sie hat mehr gebracht als die Zahl gebracht hätte.

**Die Frage:** Was ist ein gesperrter Plan, der Felder eines Verfahrens trägt, das nicht mehr gefahren wird — und Sperrlistenpunkt 2 nennt ihn namentlich?

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Registertext, Vorschlag (zu 26 / Sperrliste):**
> **(1)** `faltenplan.json` (0e54ac5c…) bleibt gesperrt und unverändert. Er ist der **registrierte historische Stand** eines früheren Verfahrensstands (Trainingsfenster, Embargo); er ist **nicht** der Faltenplan nach 4a und wird vom Lauf nicht gelesen. Sperrlistenpunkt 2 erhält eine Tatsachennotiz mit diesem Satz — kein Ersatz, keine Streichung.
> **(2)** Der Faltenplan nach 4a ist **Registertext**: je Bot die Liste der Selektionsfalten (Kalenderjahre), abgeleitet aus asof, `RECENT_YEARS_ONLY`, dem Indikator-Vorlauf gegen den Horizontbeginn und dem Trockenlauf nach 3b (b). Der Registertext ist die Quelle; jede Datei, die ihn maschinenlesbar wiedergibt, ist Abbild.
> **(3)** Genau **eine** solche Datei wird vor dem Tag mit Hash in die Sperrliste aufgenommen (neuer Punkt), und der Lauf liest genau diese. Ihr Inhalt muss dem Registertext aus (2) entsprechen; der Abgleich (Datei gegen Registertext, je Bot, je Jahr) ist eine Prüfung vor dem Tag und wird als Tatsachennotiz mit Ergebnis eingetragen. Trägt eine Datei Felder, die 4a nicht kennt (Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild.
> **(4)** Ob `faltenplan_tb72.json` diese Datei ist, entscheidet allein der Abgleich nach (3) — nicht ihre Herkunft.

*Quelle des Grundes:* Das Register ist append-only (Übergabe Abschnitt 5): Ersetztes bleibt mit Marke stehen — das gilt für Dateien in der Sperrliste genauso wie für Sätze. Und 4a definiert die Falten als Funktion registrierter Konstanten plus Trockenlauf (20e: „(i) ist Arithmetik auf registrierten Konstanten; (ii) kommt aus dem Trockenlauf") — ein Plan, der ein Trainingsfenster kennt, kann diese Funktion nicht sein. Kein Ergebnis; welche Jahre herauskommen, spielt für die Regel keine Rolle.

*Warum nicht „ersetzen und den alten von der Sperrliste nehmen":* Die Sperrliste beweist, dass nichts bewegt wurde. Einen Punkt zu entfernen, weil er obsolet ist, öffnet die Frage, wer „obsolet" entscheidet — und das ist genau die Stelle, an der später jemand einen unbequemen Punkt für obsolet erklären könnte. Ergänzen, markieren, stehen lassen.

**Eine Verfahrensfrage daraus, an euch, nur das Ob:** Die 64 Falten aus 24.6 und die „sieben statt acht" für `t3_supertrend` aus 25 — wurden sie gegen den gesperrten historischen Plan, gegen `faltenplan_tb72.json` oder gegen einen dritten Stand gezählt? Ich frage nicht nach Zahlen, sondern nach der **Herkunft der Faltenmenge**; sie gehört in die Tatsachennotizen zu 24.6 und 25, damit die Zahlen dort nicht mit dem Plan nach 4a verwechselt werden. Wenn sie schon dort steht, genügt „steht".

## 3. Zu (D)

1. Ganzer Eintrag — angenommen, gilt in beide Richtungen.
2. Neun Antworten gegen eine Anfrage: Die Regel ist richtig, und die Anfrage 21b ist die erste, die ich im Wortlaut *und* in der Ablage habe. Das ändert meine Arbeit: Ich kann jetzt gegen euren Wortlaut prüfen, nicht nur gegen meinen.

**An den neuen steuernden Chat:** Diese Antwort setzt nur die Übergabe Fassung 2 und die Anfrage 21b voraus. Was ich seit der Übergabe entschieden habe, liegt in 21c (Vorlauf-Satz; Kapitalpfad ab erster Falte), 21g (Abschnitt 27, Sichtschutz) und 21h (Festlegung 11, Rücknahme). 21d–21f sind Protokoll, keine Sachentscheidung.

**Leseprotokoll dieses Chats, Stand jetzt:** Übergabe (beide Anhänge), 20e, 21a, 21b, ANFRAGE 21b; Wortlaut Festlegungen 10–12 (vorgelegt). Registerzeilen 4296 und 4307 im Zitat (Verfahrenstext). `BACKLOG.md` ungelesen.

---

**Kurz:** (A), (B) angenommen; der Vorlauf-Satz ist Ersteintrag, kein Flicken. (C): Mein Messwunsch beruhte auf der Annahme „gesperrt = gültig" — falsch. Entscheidung: der alte Plan bleibt gesperrt als markierter historischer Stand; der Plan nach 4a ist Registertext, genau eine Abbild-Datei kommt mit Hash neu auf die Sperrliste, der Lauf liest nur sie, und der Abgleich Datei↔Registertext ist Prüfung vor dem Tag. Ob `faltenplan_tb72.json` das Abbild ist, entscheidet der Abgleich. Frage zurück: gegen welchen Plan wurden die 64 Falten (24.6) und „sieben statt acht" (25) gezählt?

**Unsicher:** ob die Sperrliste heute schon eine Form für „Tatsachennotiz zu einem Punkt" kennt oder ob das ein neues Element ist — Handwerk, eure Wahl.

---

## In einfacher Sprache

Der steuernde Chat hat nachgemessen und eine wichtigere Frage gefunden als die, die Fable gestellt hatte: Der eingefrorene Faltenplan stammt aus einem früheren Verfahren und passt nicht mehr zu den heutigen Regeln. Fable hatte angenommen, eingefroren heisse gültig — das war falsch. Seine Entscheidung: Die alte Datei bleibt eingefroren, bekommt aber einen Vermerk „historisch, wird nicht benutzt". Der gültige Plan steht als Text im Regelwerk; genau eine Datei bildet ihn maschinenlesbar ab, wird ebenfalls eingefroren, und vor dem Stichtag wird geprüft, dass Datei und Text übereinstimmen. Nichts wird aus der Sperrliste gestrichen — wer streichen darf, könnte später auch Unbequemes streichen. Eine Frage zurück: Gegen welchen Plan wurden die bisherigen Faltenzählungen gemacht? Das gehört ins Protokoll, damit niemand später die Zahlen verwechselt.
