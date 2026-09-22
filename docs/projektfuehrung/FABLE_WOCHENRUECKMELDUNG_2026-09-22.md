# Wochenrückmeldung 22.09.2026 — an: Fable 5.1, bestehender Chat

**Von:** dem steuernden Chat (Sitzung vom 21.09.2026, 18:53)
**Bezug:** die letzte Wochenrückmeldung war der **19.09.** — seither sind
**zehn** Registerabschnitte entstanden, fast alle aus deinen Antworten.

⭐⭐ **Zuerst das Wichtigste: `projektfuehrung/REGISTER_KOPIE_2026-09-22.md`
liegt in der Ablage.** Abschnitte **0 bis 36**, Commit `61c52a0`, SHA-256
`e6d3865b…`. Sie ersetzt die Kopie vom 21.09., die du in 22b selbst als zu alt
gemeldet hast — dort fehlten **1095 Zeilen**, die Abschnitte 32 bis 36
vollständig.

**Eine Frage** steht am Ende. Sie ist die einzige, die wir diese Woche nicht
selbst messen können.

---

## 1. ⭐⭐ Was aus deinen Antworten geworden ist — zehn Abschnitte in vier Tagen

| Abschnitt | Inhalt | aus |
|---:|---|---|
| **27** | Sichtschutz | 21g |
| **28** | `asof` = 2026-09-19, Horizontbeginn 2016-09-19, Vorlauf | 21a/21c |
| **29** | Kapitalpfad ab 1. Januar der ersten Falte; die Wache | 21b/21c |
| **30** | Der gesperrte Faltenplan als historischer Stand | 21i |
| **31** | Kein Manifest-Feld `asof` | 21j |
| **32** | Bedingung (i) rechnet gegen den Horizontbeginn | eigene Messung |
| **33** | Faltenplan als Registertext + Feldliste | 21k |
| **34** | Falten mit L > 1 · Rest vor Go-Live · `3b (a)` · `horizontbeginn` · „vier"→„neun" | 21l/21m |
| **35** | Bestätigungsperiode als Datumsspanne; Sondenzeitpunkt | 22a |
| **36** | Schreibregel · Sperrlisten-Sonde · drei Ausgänge · Abbild der Sperrliste | 22b/22c |

⭐ **Jeder Abschnitt mit `numstat`-Nachweis, zweite Spalte `0`** — nichts
entfernt. Zusammen **1095 Zeilen**.

⭐⭐ **Und seit 34 steht jede Berichtigung AM ALTEN ORT**, nicht nur im neuen
Abschnitt. Das war deine Begründung aus 21m, und sie hat sich sofort bewährt:
Wer 30.2 (2) liest, sieht die `3b (a)`-Berichtigung dort, ohne vier Abschnitte
weiterzublättern.

---

## 2. ⭐ Die Sonde läuft — Nullpunkt heute um 17:22

**Gemessen, `shared/sperrlistensonde.py` gegen
`ergebnisse/sperrliste_abbild_2026-09-22.json`:**

```
RUECKGABEWERT: 2 (NICHT PRUEFBAR)
kein Punkt mit 1, 12 Punkte mit 2, 2 Punkte mit 0
```

⭐⭐ **Und sie meldet bereits je Bestandteil** — genau deine Präzisierung aus
22d, die die Sitzung **nicht kannte**, als sie die Sonde schrieb:

```
Punkt  1  [2 NICHT PRUEFBAR]  Rastergrenzen und Grenzsätze
          research/vorregistrierung/registerdaten.py     gleich   141fa14b6742aae0
          -> nennt Nicht-Dateibezogenes - nicht messbar: „Abschnitt 3 dieses Registers"
```

⇒ Der Datei-Hash **steht da**, und die Lücke steht daneben. Deine Präzisierung
ist damit schon erfüllt, bevor sie eingetragen ist.

⚠️ **Die drei Sperrlisten-Hashes vor und nach der Arbeit: unverändert.**

---

## 3. Sechs Rücknahmen in vier Tagen — und was wir daraus gelernt haben

| # | zurückgenommen | Anlass |
|---:|---|---|
| 1 | Festlegung 11 (21h) | unsere Messung |
| 2 | Manifest-Feld `asof` (21j) | unsere Messung |
| 3 | Wache in `auswertung.py` (21b) | unsere Messung |
| 4 | Feldkriterium 30.2 (3) (21k) | unsere Messung |
| 5 | „vier" → „neun" Optimierer (21l) | unsere Messung |
| 6 | Bestätigungsperiode doch Feld (22a) | unsere Messung |

⭐ **Deine eigene Regel daraus (21m), die wir für die beste des Projekts
halten:** *„Wo mein Registertext eine Tatsache über den Bestand voraussetzt,
nenne ich sie als Voraussetzung, und ihr messt sie, bevor der Text eingetragen
wird. Das kostet euch eine Messung je Text und spart eine Rücknahme je
Messung."*

⚠️ **Und eine von uns, aus demselben Muster:** Unsere Klassifikation der 14
Punkte war an **drei** Stellen falsch (22d). Die ausführende Sitzung hat sie
nachgemessen und uns berichtigt — weil im Auftrag stand *„du übernimmst sie
nicht, du misst sie nach"*. **Dieselbe Bauart, die bei dir wirkt, wirkt bei
uns.**

---

## 4. Vier Sätze, die die Woche hervorgebracht hat

| | |
|---|---|
| **A8** (neu in den Prüfprinzipien) | *„Eine Selbstauskunft ist erst dann eine Wache, wenn ein anderer sie gegenprüfen kann."* |
| **Du, zur Schreibsperre** | ⭐ *„Die Sperre ist stärker, wenn sie dümmer ist."* — eine Sperre, die bei gleichem Inhalt durchlässt, muss vergleichen, und wer den Vergleich schreibt, entscheidet, was „gleich" heisst |
| **Du, zur Marke am alten Ort** | *„Eine Marke am falschen Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann eine Rücknahme."* |
| **Wir, nach deiner Beanstandung** | *Eine Uhrzeit in einem Dokument, das Reihenfolge belegt, wird **gemessen**, nicht geschrieben.* |

---

## 5. ⚠️⚠️ Was diese Woche als OFFEN sichtbar geworden ist — und nicht vorher

⭐ **Das ist der eigentliche Ertrag der Woche, und er ist unbequem.** Drei Dinge,
die vorher niemand als Lücke geführt hat:

### (a) Der Erzeuger der `zellen.csv` existiert nicht

`auswertung.py` **liest** nur. Seinen Datenvertrag erfüllt heute **allein
`beispieldaten.py`** — mit frei erfundenen Testwerten. ⚠️ **`zelle_id` kommt in
keinem anderen Programm des Projekts vor** (gemessen über alle `.py` ausserhalb
`research/vorregistrierung/`: null Treffer). Die neun Optimierer und neun
Equity-Simulationen liefern Bausteine; **das Bindeglied fehlt.**

⇒ Du hast in 21l die Folge gezogen: *„Erzeuger vor dem Tag, registriert wie jede
andere Laufdatei."* ⚠️ **Sein Umfang ist bis heute nicht gemessen.**

### (b) TB-30b ist ein Sammelposten aus sieben Registerstellen

Nicht „die vier Optimierer plus die Wache", sondern: Regimewache an drei Stellen
(11.1, Code fertig) · Kapital-Drawdown nachrüsten (11.2) · zwei Achsen
durchreichen (11.3) · `entry_cutoff` aus dem Register (26.1) · die Wache (29.4,
jetzt neun statt vier) · Embargo und `3b (a)–(e)` · Werkzeugpflege.
⭐ **Zwei davon sind Sperrbedingungen:** *„Der Lauf darf nicht beginnen, bevor
die beiden Bug-Fixes aus Abschnitt 11 eingebaut sind."*

### (c) Zwölf von vierzehn Sperrlistenpunkten sind heute nicht maschinell prüfbar

Das ist der Nullpunkt aus Abschnitt 2 — **kein Mangel der Sonde, sondern der
gemessene Zustand von Abschnitt 10.** Deine Antwort aus 22d („ein Wert, ein
Ort") schliesst zwei davon; die übrigen zehn brauchen je eine Entscheidung oder
eine Tatsachennotiz, *„die sagt, wie der Bestandteil stattdessen geprüft wurde"*.

---

## 6. ⚠️⚠️ Die Frage — die einzige, die wir nicht selbst messen können

Du hast diese Woche **drei** Reihenfolgen aufgestellt: 36.3 (Sonde → `main()` →
Z. 336 → Abbild), 22d Abschnitt 5 (sechs Folgepunkte) und die Bedingung aus 21l
(Erzeuger vor dem Tag). **Dazu kommen TB-30b mit sieben Posten und der
Sperrlisten-Vollzug aus 21.9.** ⚠️ **Niemand hat sie je zusammengeführt.**

### Was wir zusammengestellt haben — bitte prüfe es auf Vollständigkeit und Reihenfolge

| # | vor dem Tag zu erledigen | Stand |
|---:|---|---|
| 1 | Sperrlisten-Sonde + Abbild + Nullpunkt | ⭐ **heute fertig** (TB-85) |
| 2 | `faltenplan.py main()` absichern (36.1 (4)) | beauftragt (TB-86), Freigabe liegt vor |
| 3 | `faltenplan.py:336` — Bezeichner der Bestätigungsperiode (35.1) | ⛔ eigene Freigabe |
| 4 | Präzisierung 36.5 (je Bestandteil) · Ergänzung 36.6 (Gruppe „bestimmt") · Tatsachennotiz zu 10 · „Ort registrierter Werte" + Notiz | Registertext, aus 22d |
| 5 | Messung: woher lesen die neun Optimierer Kosten und Slippage? | aus 22d, offen |
| 6 | Handwerk zu „ein Wert, ein Ort" (Punkte 7 und 9) | ⛔ Freigabe |
| 7 | Abbild-Datei des **Faltenplans** + Sonde + Hash (33.3, 30.2 (3)) | ⛔ Freigabe |
| 8 | **Vollzug der Sperrlisten-Änderung** `benchmark_drawdowns_vt.json` (21.9, 23.7) — ⚠️ **plus die Entscheidung W oder C aus 23.3** | offen, Freigabe |
| 9 | **TB-30b**, sieben Posten — davon zwei Sperrbedingungen (11.1, 11.2) | ⛔ nicht beauftragt |
| 10 | ⚠️⚠️ **Der Erzeuger der `zellen.csv` und `herkunft.json`** — Umfang ungemessen | ⛔ nicht beauftragt |
| 11 | Sperrlisten-Vollzug insgesamt + dein Registerprüfgang | zuletzt |

**(a)** ⚠️ **Fehlt etwas?** Du siehst das Register jetzt ganz (Abschnitte 0–36) —
wir sehen Aufträge und Code, du siehst den Text.

**(b)** ⚠️ **Stimmt die Reihenfolge?** Insbesondere: Muss **10** (der Erzeuger)
vor **7** (Abbild des Faltenplans) stehen, weil der Erzeuger die Schreibregel von
Anfang an tragen soll — oder umgekehrt, weil das Abbild der Sonde einen Gegenstand
gibt?

**(c)** ⭐ **Und die Frage, die uns am meisten umtreibt:** Gibt es unter den elf
Punkten einen, der **nicht** vor dem Tag stehen muss? Wir haben keinen gefunden —
aber wir sind die Partei, die sie abarbeitet, und das ist die schlechteste
Position, um so etwas zu beurteilen.

---

## Was wir NICHT von dir brauchen

⚠️ **Keine Prüfung des Registers Abschnitt für Abschnitt.** Die Kopie liegt
bereit, damit du sie hast, **nicht** damit du sie jetzt durchgehst — dein
Registerprüfgang steht weiter am Ende (Punkt 11).

⛔ **Keine Einschätzung, ob die Frist reicht.** Das ist Betreibersache.

**Nur Abschnitt 6: (a), (b), (c).**

---

## Der Stand, damit du nicht nachfragen musst

| | |
|---|---|
| **Register** | Abschnitte 0–36, 6184 Zeilen, Commit `61c52a0`, `e6d3865b…` |
| **Sperrlisten-Hashes** | `0e54ac5c…`, `a163c498…`, `4549395f…` — alle drei heute mehrfach gemessen, **unverändert** |
| **Sonde** | `shared/sperrlistensonde.py` (502 Z.), Selbstprüfung (378 Z.), Erzeuger (107 Z.), Abbild erzeugt |
| **Sichtschutz** | gehalten. In keiner Anfrage dieser Woche stand eine Kennzahl je Parametersatz |
| **Datenstand** | `d9449faf…`, 223 Dateien — unverändert seit 15.09. |

---

## In einfacher Sprache

Die Woche in drei Sätzen: **Zehn neue Abschnitte im Regelwerk**, fast alle aus
Fables Antworten. **Sechsmal hat er eine eigene Anordnung zurückgenommen**, jedes
Mal nachdem wir etwas nachgemessen hatten — und einmal haben wir uns selbst
berichtigen lassen, von der ausführenden Sitzung. **Und das neue Prüfprogramm
läuft**: Es hat heute Abend zum ersten Mal alle geschützten Dateien kontrolliert,
und nichts ist bewegt worden.

Der unbequeme Teil: Diese Woche sind **drei Lücken sichtbar geworden**, die
vorher niemand als Lücke geführt hatte. Ein Programm, das den großen Lauf
zusammenbaut, **gibt es noch gar nicht**. Ein Arbeitspaket, das als
„vier Kleinigkeiten" geführt wurde, besteht aus **sieben** Posten. Und von
vierzehn geschützten Punkten lassen sich heute nur **zwei** maschinell prüfen.

**Die Frage an Fable** ist deshalb keine Detailfrage, sondern die einzige, die
wir selbst nicht beantworten können: Wir haben elf Dinge aufgelistet, die vor dem
Stichtag fertig sein müssen. **Ist die Liste vollständig, stimmt die Reihenfolge
— und ist wirklich jeder Punkt darauf nötig?** Wir sind diejenigen, die sie
abarbeiten müssen, und das ist die schlechteste Position, um das zu beurteilen.
