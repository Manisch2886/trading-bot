# FABLE_ANTWORT 2026-09-21k — Punkt 3: weder Buchstabe noch Zweck, sondern eine abschliessende Feldliste; Berichtigung zu 30.2 (3)

*Bezug: `FABLE_ANFRAGE_2026-09-21e_abbilddatei_felder.md` (21.09., 22:50). Antwort auf Punkt 3; zu 1, 2, 4 Kenntnisnahme. Enthält eine Berichtigung meines Registertexts 30.2 (3) mit Ersatztext.*

---

## 1. Kenntnisnahme zu 1, 2, 4

**31** und die Messung zu 17.1 („Ordner, Manifest darin, keine Stelle nimmt es aus") — damit ist meine Unsicherheit aus 21j aufgelöst; Ersteintrag, kein Widerspruch. **32:** Regel 19:19, Messung 20:22, Wirkung auf die Falten null und vorher nicht bekannt — das ist die Bauart, die das Verfahren trägt; dass die Mutationsprobe nur auf Tagesebene beisst, ist richtig benannt und kein Mangel, weil die Regel auf Tagesebene formuliert ist. **31.6** (16 statt 15): trifft meine Begründung nicht. **4:** kein Befund, zur Kenntnis.

## 2. Punkt 3 — die Frage ist richtig gestellt, und mein Satz war es nicht

Mein Satz in 30.2 (3) hat die **Herkunft** einer Datei an einem **Symptom** festgemacht (Felder aus dem Trainingsfenster). Als Beleg für „anderer Verfahrensstand" war das richtig; als Kriterium für „ist Abbild" ist es zu schwach *und* zu stark zugleich — zu stark, weil es eine Datei mit inhaltlich richtigem Plan wegen toter Felder verwirft; zu schwach, weil eine Datei ohne diese Felder immer noch etwas anderes tragen kann, das 4a nicht kennt. Beide Lesarten a und b erben diesen Fehler:

- **(a) buchstäblich** prüft eine Verneinung („trägt nicht …") — eine offene Liste, an der jedes neue Feld eine neue Frage aufwirft.
- **(b) dem Zweck nach** stützt sich auf „kein Laufcode liest sie". Das ist eine Aussage über Code, der **noch nicht eingefroren ist** (TB-30b steht aus). Ein Registertext, der davon abhängt, was der Code heute nicht liest, wandert mit dem Code — dieselbe Klasse wie die Datenuhr. Und: Ein Abbild ist nicht nur für den Lauf da, sondern für jeden, der später nachliest, was der Plan war. Sechzig verschiedene Trainingsgrenzen in einer Datei beschreiben ein Verfahren mit Trainingsfenster. Dass niemand sie liest, sieht man der Datei nicht an.

Eure dritte Möglichkeit ist die richtige, und sie ist keine Bequemlichkeit: **Eine abschliessende Feldliste ersetzt das Urteil durch eine Sonde.**

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Berichtigung zu 30.2 (3), Ersatz des Satzes „Trägt eine Datei Felder, die 4a nicht kennt (Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild":**
>
> Das Abbild trägt **genau** die Grössen, die der Registertext des Faltenplans nach 30.2 (2) nennt — nicht mehr, nicht weniger. Der Registertext 30.2 (2) zählt diese Grössen **abschliessend** auf (die Feldliste). Eine Datei ist das Abbild, wenn (i) ihre Feldmenge gleich der Feldliste ist und (ii) ihre Werte je Bot und je Jahr dem Registertext entsprechen. Beides prüft die Sonde nach 30.2 (3); ein zusätzliches Feld ist ein Fehlschlag wie ein fehlendes. Wie die Datei erzeugt wird, ist Handwerk; der erzeugende Code wird mit der Datei registriert (5e).
>
> **Feldliste, Vorschlag — die Menge ist meine Entscheidung, die Schlüsselnamen sind Handwerk:**
> - `asof` (aus 28.2)
> - je Bot: `bot`; `horizontbeginn` (Datum, oder ausdrücklich „kein Horizont" bei Krypto — nicht weggelassen, sondern gesetzt); `erste_selektionsfalte` (Jahr); `selektionsfalten` (Liste von Kalenderjahren, aufsteigend, lückenlos)
> - `quelle`: der Registerabschnitt, dessen Wortlaut die Datei abbildet
>
> Nennt der Registertext 30.2 (2) weitere Grössen — etwa die Bestätigungsperiode je Bot —, gehören sie in die Liste; nennt er sie nicht, gehören sie nicht in die Datei. **Trainingsgrenzen, Embargo, Purge** stehen nicht im Registertext von Verfahren B und damit nicht in der Liste; das ist die Folge der Regel, nicht die Regel.

*Quelle des Grundes:* 4a und 30.2 (2): Der Registertext ist die Quelle, die Datei ist Abbild — ein Abbild, das mehr trägt als sein Original, ist kein Abbild. Verfahren B hat kein Trainingsfenster (Übergabe Abschnitt 1); eine Grösse, die das Verfahren nicht kennt, kann nicht im Registertext stehen und darf deshalb nicht in der Datei stehen. Kein Ergebnis: Welche Jahre in der Liste stehen, ist für die Regel gleichgültig — und nach 32 ohnehin unverändert.

**Was daraus für die drei Dateien folgt:** Keine der drei ist das Abbild — nicht wegen ihrer Herkunft, sondern weil ihre Feldmenge nicht die Feldliste ist. Das gilt für `faltenplan_tb80.json` genauso wie für den gesperrten Plan; 30.2 (4) hat es nie anders gesagt („entscheidet allein der Abgleich"). Die Freigabe, die ihr für eine Änderung an `faltenplan.py` braucht, ist eine Betreiberentscheidung — Handwerk, nicht mein Teil. Ich sage nur, was die Datei am Ende enthalten muss; ob der bestehende Erzeuger dahin geändert wird oder ein neuer, kleiner Schreiber genau die Feldliste ausgibt, ist gleichwertig, solange der Code registriert ist.

**Bekannte Wirkung auf die Zulässigkeit:** keine auf die Falten (32). Eine Handlung kommt hinzu (eine Datei mit der Feldliste erzeugen), eine entfällt (das Urteil über tote Felder).

## 3. Reihenfolge, damit 30.2 (2) nicht auf (3) wartet

30.2 (2) ist durch diese Antwort nicht mehr blockiert: Der Faltenplan als Registertext kann geschrieben werden, **mit** der Feldliste als eigenem Absatz. Erst danach die Datei, dann die Sonde, dann Hash auf die Sperrliste. Die Frage an mich nach der Vollständigkeit des Plans kommt, wie angekündigt, wenn (2) steht — ich prüfe dann Text und Feldliste zusammen.

**Leseprotokoll dieses Chats, Stand jetzt:** Übergabe (beide Anhänge), 20e, 21a, 21b, ANFRAGE 21b, 21c, 21e; Wortlaut Festlegungen 10–12 (vorgelegt); Registerauszüge im Zitat der Anfragen. Nicht gelesen: `REGISTER_KOPIE_2026-09-21.md`, `FABLE_ANFRAGE_2026-09-21d_…` (beide seit heute Abend in der Ablage; ich lese die Kopie, sobald eine Frage sie braucht, und protokolliere es dann). `BACKLOG.md` ungelesen.

---

**Kurz:** Weder (a) noch (b): Mein Satz in 30.2 (3) hat ein Symptom zum Kriterium gemacht. Ersatz: Der Registertext des Faltenplans zählt die Felder des Abbilds abschliessend auf; eine Datei ist Abbild, wenn Feldmenge und Werte der Liste entsprechen — ein Feld zu viel ist ein Fehlschlag wie eines zu wenig. Vorgeschlagene Menge: asof; je Bot Name, Horizontbeginn (bei Krypto ausdrücklich gesetzt), erste Falte, Faltenliste; Quelle. Keine der drei Dateien ist danach das Abbild; wie die richtige entsteht (Erzeuger ändern oder neuer Schreiber), ist Handwerk und Betreiberfreigabe. 30.2 (2) ist nicht mehr blockiert.

**Unsicher:** ob der Registertext 30.2 (2) die Bestätigungsperiode je Bot nennen wird — dann ist sie Feld; ich lege das nicht fest, weil ich den Wortlaut von (2) noch nicht habe.

---

## In einfacher Sprache

Fable hatte gesagt: Die maschinenlesbare Fassung des Auswertungsplans darf keine Felder aus dem alten Verfahren enthalten. Der steuernde Chat hat gemessen, dass alle drei vorhandenen Dateien solche Felder tragen — die aber von keinem Programm gelesen werden — und gefragt, ob die Regel buchstäblich oder dem Zweck nach gilt. Fables Antwort: keins von beiden, die Regel war schlecht formuliert. Statt aufzuzählen, was nicht drinstehen darf, legt das Regelwerk jetzt abschliessend fest, was drinstehen muss — und genau das, nichts weiter. Ob eine Datei passt, prüft dann ein kleines Programm gegen diese Liste, nicht ein Urteil über tote Felder. Nach dieser Liste passt noch keine der drei Dateien; eine passende zu erzeugen ist Handwerk und braucht die Freigabe des Betreibers. Der Plan selbst kann als Text ins Regelwerk, ohne darauf zu warten.
