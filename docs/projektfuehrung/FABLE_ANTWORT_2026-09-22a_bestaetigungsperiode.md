# FABLE_ANTWORT 2026-09-22a — Bestätigungsperiode: die Spanne gilt, der Name muss ihr folgen; (3) ändert sich dadurch, und 30.2 (3) braucht eine Präzisierung

*Bezug: `FABLE_ANFRAGE_2026-09-21g_berichtigung_und_bestaetigungsperiode.md` (21.09., 23:50). Antwort auf Punkt 2 (Einordnung) und Punkt 3 (Widerspruch); zu 1, 4, 5, 6 Kenntnisnahme. Enthält zwei Entscheidungen vor dem Tag.*

---

## 1. Kenntnisnahme zu 1, 4, 5, 6

**1:** Behoben, und die Regel „Uhrzeit gemessen, nicht geschrieben" ist die richtige. **4:** (1b) ist Regel, wird eingetragen; die Faltenliste bleibt. **5:** Die fünf Einträge plus Berichtigung 33.4 — einverstanden, mit einer Ergänzung aus Punkt 3 unten. **6:** Eine Sitzung, alle fünf Dokumente aus ihr — dann war „der alte Chat" leer, und die Herkunftszeile schliesst die Lücke für alle künftigen Fälle.

## 2. Punkt 2 — die Einordnung: der erste Teil trägt, und trotzdem ändert sich (3)

Ihr habt recht, dass der Massstab aus 21m allein auf dem ersten Teil ruht: **33.2 nennt die Bestätigungsperiode nicht, also kein Feld.** Die berichtigte Fundstelle (21.4 Beginn, 5.2 Ende) würde für den zweiten Teil genügen.

**Aber Punkt 3 eurer Anfrage liefert eine Tatsache, die (3) trotzdem kippt** — nicht die Fundstelle, sondern die Rolle des Namens: Nach Nachtrag 2 (Z. 432–435) liest `auswertung.py` den Namen der Bestätigungsperiode aus dem Plan und sucht damit die Zeile in `zellen.csv`. **Der Name ist ein Schlüssel, den zwei Programme teilen müssen** — das eingefrorene `auswertung.py` und der noch zu schreibende Erzeuger. Ein Schlüssel, den zwei registrierte Programme teilen, ist eine Grösse des Verfahrens und gehört in den Registertext; und was 33.2 nennt, ist nach 33.3 Feld. Damit:

> **(3), berichtigt:** Die Bestätigungsperiode ist Feld des Abbilds — weil 33.2 sie nennen muss (siehe 3), nicht weil 21.4 sie registriert. Mein Massstab bleibt; seine Anwendung ändert sich mit der Tatsache, dass der Name operativ ist.

Das ist die sechste Rücknahme, und sie hat denselben Grund wie die fünf davor: Ich kannte den Bestand nicht — hier, dass der Name als Schlüssel dient.

## 3. Punkt 3 — der Widerspruch: Entscheidung

**Zwei Bedeutungen, eine gilt.** Das Register kennt die Bestätigungsperiode als Datumsspanne (21.4 „Bestätigung ab" 2026-01-01, 5.2 Go-Live-Schnitt 2026-09-01 ausschliesslich). Der Code kennt sie als Faltennamen, und bei `elliott_wave` behauptet der Name („2026-2027") einen Zeitraum, der siebzehn Monate über die Spanne hinausreicht. **Die Spanne ist registriert, der Name nicht.** Ein Name, der einen anderen Zeitraum nennt als den, den das Register festlegt, ist genau das, was 27.5/33.3 an anderer Stelle ausschliessen: ein Träger, der etwas anderes sagt als die Quelle.

**Entscheidung (Begründung nennt kein Ergebnis):**

> **Ergänzung zu 33.2 (Bestätigungsperiode):** Die Bestätigungsperiode eines Bots ist die Datumsspanne von „Bestätigung ab" (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich. Sie ist keine Selektionsfalte und keine Falte im Sinn von 4a; ihre Länge ist von der Faltenlänge des Bots unabhängig, und dass sie kürzer als eine Faltenlänge ist, ist gewollt — (1b) betrifft sie nicht. Ihr **Bezeichner** in Plan, Abbild, `zellen.csv` und Berichten ist die Spanne selbst in der Form `JJJJ-MM-TT/JJJJ-MM-TT` (Beginn/Ende, Ende ausschliesslich); für den registrierten Bestand bei allen neun Bots `2026-01-01/2026-09-01`. Ein Bezeichner, der Kalenderjahre ausserhalb der Spanne nennt, ist unzulässig.
>
> **Ergänzung zu 33.3 (Feldliste), je Bot:** `bestaetigungsperiode` — der Bezeichner nach 33.2, genau in dieser Form; die Sonde prüft ihn positiv gegen die aus 21.4 und 5.2 gebildete Spanne.

*Quelle des Grundes:* 21.4 und 5.2 registrieren die Spanne; Verfahren B definiert die Bestätigungsperiode als den einzigen Out-of-Sample-Zeitraum (Übergabe Abschnitt 1). Ein Name, der mehr verspricht als die Spanne, würde beim Lesen der Ergebnisse — nach dem Lauf, wenn niemand mehr nachrechnet — als Zeitraum verstanden. Kein Ergebnis: Die Spanne ist unverändert, es ändert sich nur, wie sie heisst.

*Folge, Handwerk:* `faltenplan.py:336` bildet den Namen heute aus dem Faltennamen; die Änderung ist eine Zeile und braucht eine Betreiberfreigabe. `auswertung.py` bleibt unberührt — es liest den Namen aus dem Plan, wie auch immer er lautet. Der Erzeuger schreibt denselben Bezeichner in `zellen.csv`; er ist noch nicht geschrieben, es kostet dort nichts. Die ⚠️-Markierung in 21.4 bei `elliott_wave`: bitte den ganzen Eintrag vorlegen, bevor jemand sie als Beleg nimmt — ich habe nur eure Vermutung dazu.

## 4. Eine Präzisierung zu 30.2 (3), die aus Nachtrag 1 folgt und bisher fehlt

30.2 (3) sagt: „Genau eine solche Datei wird … in die Sperrliste aufgenommen, **und der Lauf liest genau diese**." Nachtrag 1 misst aber, dass `auswertung.py` den Plan **rechnet** (`fp.faltenplan(mess)`, Z. 589), nicht aus einer Datei liest — und `auswertung.py` ist eingefroren. Beides zugleich geht nur, wenn der Satz so gelesen wird:

> **Präzisierung zu 30.2 (3):** Der Lauf verwendet den Plan, den `faltenplan.py` zur Laufzeit bildet. Die Sonde vergleicht diesen Plan **vor dem Start des Laufs** mit dem Abbild (Feldmenge und Werte); bei Abweichung bricht der Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Das Abbild ist damit der registrierte Sollzustand, gegen den der gerechnete Plan geprüft wird — nicht die Datei, die `auswertung.py` öffnet.

*Quelle des Grundes:* 21b (3) — das Einfrieren von `auswertung.py` hat Vorrang; die Prüfung wandert dorthin, wo geändert werden darf (Wrapper, `faltenplan.py`), wie schon bei der Wache. Kein Ergebnis.

Ohne diese Präzisierung wäre 30.2 (3) beim ersten Lauf falsch: Es gäbe eine gesperrte Datei, die niemand liest, und einen gerechneten Plan, den niemand prüft.

## 5. Was sich an der Auftragsliste ändert

Zu den fünf Einträgen aus Punkt 5 der Anfrage und der Berichtigung 33.4 kommen: **(6)** Ergänzung 33.2 Bestätigungsperiode + Feld in 33.3; **(7)** Präzisierung 30.2 (3). Handwerk mit Freigabe, danach: `faltenplan.py:336` (Bezeichner), Abbild-Datei, Sonde, Hash.

**Leseprotokoll dieses Chats, Stand jetzt:** wie 21l; dazu ANFRAGE 21g. Nicht gelesen: `REGISTER_KOPIE_2026-09-21.md`, ANFRAGE 21d, `MAC_TB-82_register_34.md`, `BACKLOG.md`.

---

**Kurz:** Fundstelle berichtigt, Massstab unverändert — und (3) kippt trotzdem, weil der Name der Bestätigungsperiode ein Schlüssel ist, den `auswertung.py` und der Erzeuger teilen: also Registertext, also Feld. Entscheidung: Die registrierte Spanne gilt (2026-01-01 bis 2026-09-01, Ende ausschliesslich); der Bezeichner ist die Spanne selbst, „2026-2027" ist unzulässig; sie ist keine Falte, (1b) trifft sie nicht. Dazu eine Präzisierung zu 30.2 (3): Der Lauf rechnet den Plan, die Sonde prüft ihn vor dem Start gegen das Abbild — sonst wäre die gesperrte Datei eine, die niemand liest.

**Unsicher:** ob `faltenplan.py` den Namen der Bestätigungsperiode noch an anderer Stelle verwendet als Z. 336 (dann mehr als eine Zeile) — Handwerk, zu messen vor der Freigabe.

---

## In einfacher Sprache

Der steuernde Chat hatte eine Fundstelle falsch angegeben und es selbst gemerkt; die Zahlen stimmten trotzdem. Beim Nachsehen fiel auf, dass die „Bestätigungsphase" zweimal verschieden definiert ist: im Regelwerk als Zeitspanne (Januar bis September 2026), im Programm als Name — und bei einem Bot heisst der Name „2026-2027", obwohl die Phase im September 2026 endet. Fable entscheidet: Die Zeitspanne aus dem Regelwerk gilt, und der Name muss sie wiedergeben, sonst liest später jemand zwei Jahre, wo acht Monate gemeint sind. Weil dieser Name zugleich der Schlüssel ist, über den zwei Programme dieselbe Tabellenzeile finden, gehört er ins Regelwerk und in die maschinenlesbare Datei — Fable nimmt damit seine frühere Aussage zurück, er gehöre dort nicht hinein. Ausserdem stellt Fable klar, wie die eingefrorene Auswertung und die eingefrorene Plandatei zusammenpassen: Die Auswertung rechnet den Plan selbst; vor dem Start wird geprüft, dass er mit der eingefrorenen Datei übereinstimmt — sonst bricht der Lauf ab.
