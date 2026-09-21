# FABLE_ANTWORT 2026-09-21m — Prüfung des Faltenplans (33.2) und der Feldliste (33.3): vollständig bis auf zwei Sätze; vier Antworten

*Bezug: `FABLE_ANFRAGE_2026-09-21f_registertext_und_feldliste.md` (21.09., 23:26). Die angekündigte Prüfung von Text und Feldliste zusammen. Antworten auf die Fragen 1–4; Frage 1 enthält zwei Ergänzungen zum Registertext, die vor dem Tag gebraucht werden.*

---

## Vorab: die vierte Rücknahme

Ihr zählt richtig: Festlegung 11, Manifest-Feld, Wache in `auswertung.py`, Feldkriterium — und mit 21l die fünfte („vier" → „neun"). Alle fünf haben dasselbe Muster: Ich habe eine Regel an einem Bestand formuliert, den ich nicht gesehen hatte. Die Regel aus 21h (ganzer Eintrag) deckt nur den ersten Fall. Die allgemeinere lautet: **Wo mein Registertext eine Tatsache über den Bestand voraussetzt (ein Feld, eine Datei, eine Zahl von Modulen), nenne ich sie als Voraussetzung, und ihr messt sie, bevor der Text eingetragen wird.** Das kostet euch eine Messung je Text und spart eine Rücknahme je Messung.

## Frage 1 — Ist der Registertext vollständig?

**Für die neun registrierten Bots: ja.** Je Bot stehen Horizontbeginn (oder „kein Horizont"), Faltenlänge, erste Selektionsfalte, Liste; die Werte sind gegen 21.4 und gegen 32 abgesichert; `t3_supertrend` 2019 ist der Fall aus 25.3 und richtig so.

**Als Regeltext: nicht geschlossen — zwei Sätze fehlen**, und beide fehlen nur deshalb nicht *sichtbar*, weil der registrierte Bestand sie zufällig nicht braucht. Ein Registertext darf nicht von diesem Zufall leben.

**(1a) Wie (i) und (ii) auf eine Falte mit Faltenlänge > 1 wirken.** 4a/25 sind für **ein** Kalenderjahr formuliert („Ein Kalenderjahr ist Selektionsfalte, wenn (i) … und (ii) …"). Für `elliott_wave` ist die Falte zwei Jahre. 33.2 sagt „in Schritten der Faltenlänge", sagt aber nicht, auf welches Jahr der Falte (i) und (ii) angewandt werden.

> **Ergänzung zu 33.2:** Bei Faltenlänge L > 1 ist ein Kalenderjahr J erstes Jahr einer Selektionsfalte, wenn J die Bedingungen (i) und (ii) nach 25 erfüllt; die Falte umfasst J bis J + L − 1. Die erste Selektionsfalte beginnt mit dem ersten Kalenderjahr, das (i) und (ii) erfüllt; die folgenden Falten schliessen lückenlos an.

*Grund:* (i) prüft den Vorlauf am 1. Januar — der einzige 1. Januar, an dem eine Falte beginnt, ist der ihres ersten Jahres. (ii) muss am ersten Jahr geprüft werden, weil die Falte sonst mit Jahren beginnen könnte, in denen der Bot nichts handelt — der Kapitalpfad (29) startet am 1. Januar der ersten Falte und braucht dort Handelbarkeit.

**(1b) Der Rest vor dem Go-Live-Schnitt.** „Lückenlos vom Beginn der ersten Falte bis zum Go-Live-Schnitt" ist nur dann eindeutig, wenn die Jahre zwischen erster Falte und Go-Live ein Vielfaches von L sind. Für `elliott_wave` sind es 2018–2025 = 8 Jahre = 4 Falten — es geht auf. Wäre die erste Falte 2019 gewesen, bliebe 2025 als Rest. Der Text muss sagen, was ein Rest ist.

> **Ergänzung zu 33.2:** Ein Rest von weniger als L Kalenderjahren zwischen der letzten vollen Selektionsfalte und dem Go-Live-Schnitt ist keine Selektionsfalte. Sein Verhältnis zur Bestätigungsperiode regelt 21.4; 33.2 trifft dazu keine Aussage.

*Grund:* 4a kennt nur ganze Falten; eine Teilfalte hätte weniger Beobachtungen als die übrigen und ginge mit gleichem Gewicht in den Faltenmedian — eine Verzerrung, die 4a nirgends zulässt. Kein Ergebnis: Für den registrierten Bestand tritt der Fall nicht ein; die Faltenliste ändert sich um nichts.

**Zwei kleinere Dinge, ohne Textänderung:**
- `erste_falte_4a = 2018` bei `t3_supertrend` steht in der Datei. Es ist **kein Feld der Feldliste** und gehört auch nicht hinein — die Herleitung (Bedingung (i) allein: 2018; mit (ii): 2019) ist Tatsachennotiz zu 25.3, nicht Abbildinhalt. Die künftige Abbild-Datei trägt es nicht; das ist die Feldliste in Anwendung.
- Der Go-Live-Schnitt (2026-09-01) wird in 33.2 genannt, aber nicht als Feld geführt — richtig, er ist in 5.2 registriert; 33.2 zitiert ihn, führt ihn nicht.

## Frage 2 — Die drei Anpassungen

**(1) „in Schritten der Faltenlänge":** richtig. Mein „Liste von Kalenderjahren" war an acht Bots gemessen und am neunten falsch; die Anpassung ist eine Berichtigung meines Wortlauts, mit den Ergänzungen aus Frage 1 wird sie geschlossen.

**(2) `faltenlaenge_jahre` in der Feldliste:** richtig, und aus dem richtigen Grund — ohne Schrittweite kann die Sonde Lückenlosigkeit nicht prüfen. Das ist kein „zweiter Ort" im Sinn von (3), weil 33.2 die Faltenlänge selbst als Grösse des Faltenplans nennt; das Abbild bildet 33.2 ab.

**(3) Bestätigungsperiode nicht in der Feldliste:** so, wie ich es sehe. Der Massstab ist derselbe wie bei (2), nur mit umgekehrtem Ergebnis: 33.2 nennt sie nicht, 21.4 registriert sie — also kein Feld. Ein Abbild trägt genau die Grössen seines Abschnitts.

## Frage 3 — `3b (a)` statt `3b (b)`: ausdrückliche Berichtigung

**Eigener Registersatz, ein Satz:**

> **Berichtigung zu 30.2 (2):** Die Fundstelle „Trockenlauf nach 3b (b)" lies „3b (a)". Gemeint ist der Trockenlauf aus 3b (a), der die `MIN_HISTORY_*`-Tabelle aus 3b (b) anwendet; ein zweiter Trockenlauf existiert nicht.

*Warum nicht nur der Hinweis in 33.2:* Wer 30.2 (2) liest und abschreibt, sieht 33.2 nicht — genau der Fehler aus 21h. Eine Marke am falschen Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann eine Rücknahme. Meine Zitierregel (nur vorgelegte Fundstellen) hat hier versagt, weil ich „3b (b)" aus 20e übernommen hatte, wo es um die Handelbarkeitstage ging — dieselbe Unternummer, andere Sache.

## Frage 4 — `null` oder Zeichenkette: Zeichenkette

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Ergänzung zu 33.3, Feld `horizontbeginn`:** Der Wert ist entweder ein Datum im Format `JJJJ-MM-TT` oder die Zeichenkette `"kein Horizont"` — genau eine der beiden Formen. JSON-`null`, ein fehlender Schlüssel oder eine leere Zeichenkette sind Fehlschläge der Sonde. Die Sonde prüft den Wert positiv gegen diese zwei Formen, nicht das Vorhandensein des Schlüssels.

*Grund:* Derselbe wie bei der Feldliste — eine **positive** Prüfung gegen eine abschliessende Menge ersetzt ein Urteil über Abwesenheit. `null` ist genau das Gegenteil: ein Wert, der „nichts" bedeutet und in einer Bibliothek von „fehlt" unterscheidbar ist, in der nächsten nicht (euer Befund). „Gesetzt, nicht weggelassen" hiess: Wer die Datei liest, soll *lesen*, dass der Bot keinen Horizont hat — nicht schliessen, dass ihm einer fehlt. Eine Zeichenkette tut das; `null` verlangt Kenntnis der Konvention. Folge: `faltenplan_tb80.json` (Schlüssel mit `null`) ist auch daran kein Abbild; das war es nach 33.3 schon nicht.

## Zusammen: was vor der Abbild-Datei ins Register muss

1. Ergänzung 33.2 (1a) — Falten mit L > 1.
2. Ergänzung 33.2 (1b) — Rest vor Go-Live.
3. Berichtigung 30.2 (2) — `3b (a)`.
4. Ergänzung 33.3 — `horizontbeginn` als Zeichenkette oder Datum.
5. Berichtigung 29.4 — „vier" → „neun" (aus 21l).

Danach: Abbild-Datei, Sonde, Hash — je mit Betreiberfreigabe, Handwerk. Die Frage „darf der Tag gesetzt werden" beantworte ich erst, wenn Sonde und Hash stehen **und** der Erzeuger aus Nachtrag 2 registriert ist (21l, 4a); vorher ist der Tag nicht setzbar, weil der Lauf nicht starten könnte.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 21l; dazu nichts Neues. Nicht gelesen: `REGISTER_KOPIE_2026-09-21.md`, ANFRAGE 21d, `BACKLOG.md`.

---

**Kurz:** Der Plan ist für die neun Bots vollständig und die Werte sind abgesichert. Der Regeltext braucht zwei Sätze, die der Bestand zufällig nicht braucht: wie (i)/(ii) bei Faltenlänge 2 wirken (auf das erste Jahr) und was ein Rest vor Go-Live ist (keine Falte). Anpassungen (1), (2), (3): alle richtig. `3b (a)`: eigener Berichtigungssatz, nicht nur Hinweis. `horizontbeginn`: Zeichenkette `"kein Horizont"` oder Datum, `null` ist Fehlschlag. Fünf Registereinträge vor der Abbild-Datei; der Tag frühestens, wenn auch der Erzeuger registriert ist.

**Unsicher:** ob 21.4 den Rest vor Go-Live bereits regelt — dann ist (1b) ein Verweis statt einer Regel; ihr seht es im Register, und die Kopie liegt inzwischen in der Ablage, ich lese sie bei der nächsten Frage, die sie braucht.

---

## In einfacher Sprache

Der Auswertungsplan im Regelwerk ist für alle neun Bots vollständig und die Zahlen stimmen. Fable findet trotzdem zwei Lücken im Regeltext — nicht in den Zahlen: Bei dem einen Bot, der in Zwei-Jahres-Abschnitten rechnet, sagt der Text nicht, auf welches der beiden Jahre die Startbedingungen geprüft werden; und er sagt nicht, was mit einem übrig bleibenden einzelnen Jahr vor dem Stichtag geschieht. Beides trifft die heutigen Zahlen zufällig nicht — aber eine Regel darf nicht vom Zufall leben. Die drei Änderungen an Fables Vorgabe sind alle richtig. Der falsche Verweis bekommt einen eigenen Korrektursatz, damit niemand ihn abschreibt. Und bei den Krypto-Bots soll in der Datei ausgeschrieben „kein Horizont" stehen, kein leerer Wert — damit man es lesen kann, statt es wissen zu müssen. Fünf kleine Einträge ins Regelwerk, dann kann die maschinenlesbare Datei gebaut werden.
