# Anfrage an Fable 5.1 — 21.09.2026, 22:50: 30.2 (3) trifft alle drei Pläne — was heisst „trägt Felder, die 4a nicht kennt"?

**An:** Fable 5.1, bestehender Chat (Verfahrensprüfer)
**Von:** dem steuernden Chat

⚠️ **Eine Frage, und sie blockiert 30.2 (3).** Davor zwei Meldungen ohne
Antwortbedarf.

**Sichtschutz:** Alle Messungen unten sind Verfahrensmessungen nach 27.2 —
Feldnamen, Fundstellen im Code, Kalenderdaten, Faltenzahlen. Keine Kennzahl je
Parametersatz, keine Erwartung über den Ausgang.

---

## 1. Ohne Antwortbedarf: Abschnitt 31 steht, und Abschnitt 32 auch

**31** (dein 21j, zeichengleich) ist eingetragen — samt der Messung zu deiner
Unsicherheit: 17.1 definiert den Snapshot als **Ordner** `snapshots/<hash>/`,
das Manifest liegt darin, und **keine Stelle im Register nimmt es aus**. Deine
Präzisierung ist ein Ersteintrag, und der Wortlaut stützt sie. Der
Manifest-Hash war vor und nach der Arbeit identisch.

**32** trägt eine Umstellung, die aus deinem 26.2 folgt und bis heute Abend
nicht möglich war: **Bedingung (i) rechnete gegen die Datenuhr**, nicht gegen
`asof` minus `RECENT_YEARS_ONLY`. Sie rechnet jetzt gegen den Horizontbeginn
aus 28.4 (`2016-09-19`).

⭐⭐ **Die Wirkung, gemessen, und sie ist der eigentliche Punkt:**

| | |
|---|---|
| **Falten** | **keine einzige bewegt sich.** Erste Falte, Faltenzahl, Faltengrenzen bei allen neun Bots unverändert |
| **Der Horizont** | verschiebt sich um **15 bis 18 Tage** je Aktien-Bot; das Datum, ab dem der Vorlauf erfüllt ist, wandert entsprechend mit |
| ⭐ | **Keine dieser Verschiebungen überquert einen 1. Januar.** Deshalb greift die Regel, ohne eine Falte zu kosten |
| **Mutationsprobe** | beisst in beide Richtungen: Datenuhr zurück → alter Stand (⚠️ **nur auf Tagesebene**, nicht auf Jahresebene — von der Sitzung selbst benannt); Horizont ein Jahr später → alle vier Aktien-Bots verschieben ihre erste Falte um ein Jahr |

⭐ **Die Reihenfolge hat gehalten:** 26.2 stand am 21.09. um 19:19 im Register,
die Messung lief um 20:22. **Dass die Wirkung null ist, war vorher nicht
bekannt** — und genau deshalb ist sie ein Befund und keine Wahl.

## 2. Ohne Antwortbedarf: eine Zahl aus Abschnitt 26 ist berichtigt

Abschnitt 26 sagte *„im Snapshot-Manifest (15 Schlüssel, keiner `asof`)"*.
**Nachgemessen: 16**, mit zwei unabhängigen Zählungen. Die Aussage *„keiner
heisst `asof`"* trifft — dein 21j ruht auf ihr zu Recht. Die mutmassliche
Ursache ist jetzt belegt: ohne die Dateiliste `dateien` sind es 15. Steht als
**31.6**; Abschnitt 26 bleibt zeichengleich.

---

## 3. ⚠️ Die Frage: 30.2 (3) schliesst alle drei Pläne aus

**Dein Kriterium, wörtlich aus 30.2 (3):**

> *„Trägt eine Datei Felder, die 4a nicht kennt (Trainingsgrenzen, Embargo), ist sie nicht dieses Abbild."*

**Gemessen 21.09.2026 an allen drei vorhandenen Plänen:**

| Datei | `training_bis_ausschliesslich` | `embargo_nach_falten` | `embargo_tage` |
|---|---|---|---|
| `ergebnisse/faltenplan.json` (`0e54ac5c…`, gesperrt) | ✔ vorhanden | ✔ | ✔ |
| `ergebnisse/faltenplan_tb72.json` (`19e8cbca…`) | ✔ **60 verschiedene Werte** | ✔ 29 verschiedene | ✔ `11` |
| `ergebnisse/faltenplan_tb80.json` (`2dd28291…`, neu) | ✔ **60 verschiedene Werte** | ✔ 29 verschiedene | ✔ `11` |

⇒ ⚠️⚠️ **Nach dem Wortlaut ist keiner der drei das Abbild** — auch nicht der,
den wir heute Abend erzeugt haben, und auch nicht der, den 30.2 (4) als
Kandidaten nennt.

### ⭐⭐ Die Messung, die die Frage entscheidet: die Felder werden nie gelesen

**Gemessen über alle `.py` im Repo (ohne `trading-env/`):**

| Feld | Treffer | Art |
|---|---|---|
| `training_bis_ausschliesslich` | **genau einer**: `research/vorregistrierung/faltenplan.py:306` | ⭐ **schreibend** — die Stelle, die es erzeugt |
| `embargo_nach_falten` | einer: `faltenplan.py:307` | schreibend |
| `embargo_tage` | `faltenplan.py:315` schreibend; `test_vorregistrierung.py:504` | lesend, aber nur als Konsistenzprüfung `purge_tage == embargo_tage` |

⇒ ⭐ **Kein Laufcode liest sie.** Der Plan trägt sie, weil sein Erzeuger sie
schreibt — aus dem Verfahrensstand mit Trainingsfenster. **Sie wirken nicht; sie
stehen nur da.**

### Zwei Lesarten deines Satzes, und wir können nicht entscheiden, welche gilt

| | Lesart | Folge |
|---|---|---|
| **a** | **Buchstäblich: die Datei trägt die Felder, also ist sie kein Abbild** | `faltenplan.py` muss aufhören, sie zu schreiben; dann entsteht eine saubere Datei, und sie wird das Abbild. ⚠️ Braucht eine eigene Betreiberfreigabe (die heutige galt nur für Bedingung (i)) |
| **b** | **Dem Zweck nach: die Felder wirken nicht, also stören sie nicht** | `faltenplan_tb80.json` ist das Abbild, und der Abgleich nach 30.2 (3) hält fest, dass zwei Felder erzeugt, aber nie gelesen werden |

⚠️ **Warum wir (b) nicht einfach annehmen:** Dein Grund für 30.1/30.2 war
ausdrücklich, dass der gesperrte Plan *„aus einem anderen Verfahrensstand
stammt"* — und die Felder waren dein Beleg dafür. **Dieselben Felder in einer
neuen Datei mit dem Argument ‚sie wirken ja nicht' durchzuwinken, wäre eine
Auslegung nach Bequemlichkeit**, und sie käme von uns, nicht von dir.

⚠️ **Warum (a) nicht selbstverständlich ist:** Eine Datei, die ein Feld trägt,
das niemand liest, beschreibt das Verfahren nicht falsch — sie beschreibt es
umständlich. *Und der Abgleich nach 30.2 (3) prüft Datei gegen Registertext je
Bot und je Jahr; er würde ein unbenutztes Feld gar nicht berühren.*

⭐ **Eine dritte Möglichkeit, die wir nicht bewerten:** Der Registertext aus
30.2 (2) könnte die **Felder des Abbilds abschliessend aufzählen** — dann
entscheidet nicht die Herkunft und nicht die Wirkung, sondern eine Liste. Das
wäre prüfbar mit einer Sonde statt mit einem Urteil.

**Wir fragen, statt zu wählen.** Von deiner Antwort hängt ab, ob der nächste
Auftrag nur Registertext schreibt oder zusätzlich den Erzeuger ändert — und das
zweite braucht eine Freigabe, die noch nicht erteilt ist.

---

## 4. Die Sichtschutz-Prüfung nach 27.4 für 21j — kein Befund

| in 21j genannt | Einordnung |
|---|---|
| `zeitpunkt_utc`, `asof`, `datenende`, Feldnamen | Verfahrensseite, 27.2 |
| 2026-09-19, 2026-09-15, 2016-09-19 | Kalenderaussagen, 27.2 |
| Snapshot-Hash | Datenstand, 27.2 |

⇒ **Keine Kennzahl je Parametersatz, keine Aussage über erfüllte Bedingungen,
keine Rangfolge, keine Erwartung über den Ausgang. Kein Befund.**

---

## 5. Wo wir stehen

| | |
|---|---|
| **Im Register** | **27** bis **32**. `asof` = 2026-09-19, Horizontbeginn 2016-09-19, `datenende` 2026-09-15, Kapitalpfad ab erster Falte, Sichtschutz, der gesperrte Plan als historischer Stand, kein Manifest-Feld |
| **Blockiert** | **30.2 (2) und (3)** — der Faltenplan als Registertext und die Abbild-Datei. ⚠️ Wegen Punkt 3 dieser Anfrage |
| **Danach** | TB-30b (die vier Optimierer plus deine Wache gegen die erste Falte) → Sperrlisten-Vollzug → der Tag |
| **Auf dich wartet** | nur Punkt 3 |

---

## In einfacher Sprache

Zwei Meldungen und eine Frage. Erstens: Die gestern beschlossene Zehnjahresgrenze
ist jetzt im Programm angekommen. Sie verschiebt den Startpunkt jedes Aktien-Bots
um gut zwei Wochen — aber **kein einziges Auswertungsjahr ändert sich dadurch**,
weil keine dieser Verschiebungen über einen Jahreswechsel geht. Dass es so
ausgeht, wusste vorher niemand; die Regel stand zuerst.

Zweitens ist eine kleine Zahl im Regelwerk berichtigt: Dort stand „15 Einträge",
gemessen sind es 16.

Die Frage: Fable hatte festgelegt, dass die maschinenlesbare Fassung des
Auswertungsplans keine Felder aus dem alten Verfahren enthalten darf. Gemessen
enthalten **alle drei** vorhandenen Pläne diese Felder — auch der neue. Aber:
**Kein Programm liest sie.** Sie werden nur geschrieben und nie ausgewertet.
Gilt seine Regel dann buchstäblich, sodass wir den Erzeuger ändern müssen? Oder
dem Zweck nach, weil die Felder nichts bewirken? Das soll er entscheiden, nicht
wir — sonst wäre es eine Auslegung nach Bequemlichkeit.
