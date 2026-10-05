# REGISTER-KOPIE Abschnitt 35 (von 0–54) — Register-Z. 6349–6545 — Commit 9b7b06065ebdae3f36f3102306c76bb844300e90 — 2026-10-05 — Original sha256 8d505a38ad3abc93624c7a95eb1f1e63228a937047734408d0dfb8518ca568dc — KOPIE, nicht das Register

## 35. Die Bestätigungsperiode bekommt ihren Bezeichner und wird Feld des Abbilds, und 30.2 (3) wird präzisiert — die Sonde prüft den gerechneten Plan vor dem Start (Fable 22a, TB-83, 22.09.2026)

⭐ **Reines Eintragen von Registertext**, wie 34. Vier Einträge, alle
zeichengleich aus
`docs/projektfuehrung/FABLE_ANTWORT_2026-09-22a_bestaetigungsperiode.md` (Antwort
auf die Anfrage 21g des steuernden Chats, Punkte 2 und 3). Auftrag
`docs/auftraege/MAC_TB-83_register_35.md`; Messungen `docs/belege/TB-83/`
(M1–M6), alle **vor** dem Eintrag gemessen, HEAD `9dac8d4`. ⛔ **Kein Code,
kein Aufruf von `faltenplan.py`, keine Abbild-Datei, keine Sonde, kein
Wrapper, kein Hash** — 35.5.

⭐ **Die Regel aus 34 gilt weiter:** Jeder Eintrag steht hier mit Text, Herkunft
und Grund **und** als Marke direkt beim alten Satz (33.2, 33.3, 33.4 Punkt 3,
34.6, 30.2 (3)). Die alten Sätze bleiben zeichengleich; `git diff --numstat`
auf dieses Register zeigt für TB-83 in der zweiten Spalte `0`.

⭐ **Damit ist die in 34.6 offen eingetragene Frage entschieden** — welche der
zwei Formen der Bestätigungsperiode gilt: **die Datumsspanne** (35.1). Und
**33.4 Punkt 3 („Nicht in die Feldliste") ist ERSETZT** (35.3) — Fables sechste
Rücknahme, aus einem Grund, den weder 21m noch 34.6 kannten: der Name ist ein
Schlüssel, den zwei Programme teilen.

### 35.1 Ergänzung zu 33.2 — die Bestätigungsperiode und ihr Bezeichner

**Fable, 22a Abschnitt 3, zeichengleich:**

> **Ergänzung zu 33.2 (Bestätigungsperiode):** Die Bestätigungsperiode eines Bots ist die Datumsspanne von „Bestätigung ab" (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich. Sie ist keine Selektionsfalte und keine Falte im Sinn von 4a; ihre Länge ist von der Faltenlänge des Bots unabhängig, und dass sie kürzer als eine Faltenlänge ist, ist gewollt — (1b) betrifft sie nicht. Ihr **Bezeichner** in Plan, Abbild, `zellen.csv` und Berichten ist die Spanne selbst in der Form `JJJJ-MM-TT/JJJJ-MM-TT` (Beginn/Ende, Ende ausschliesslich); für den registrierten Bestand bei allen neun Bots `2026-01-01/2026-09-01`. Ein Bezeichner, der Kalenderjahre ausserhalb der Spanne nennt, ist unzulässig.

**Fables Quelle des Grundes, zeichengleich:**

> *Quelle des Grundes:* 21.4 und 5.2 registrieren die Spanne; Verfahren B definiert die Bestätigungsperiode als den einzigen Out-of-Sample-Zeitraum (Übergabe Abschnitt 1). Ein Name, der mehr verspricht als die Spanne, würde beim Lesen der Ergebnisse — nach dem Lauf, wenn niemand mehr nachrechnet — als Zeitraum verstanden. Kein Ergebnis: Die Spanne ist unverändert, es ändert sich nur, wie sie heisst.

**Tatsachennotiz (TB-83, gemessen vor dem Eintrag — die Grundlage des
Bezeichners wird nicht übernommen, sondern gemessen):** 21.4 führt in der
Spalte „Bestätigung ab" bei **allen neun** Bots `2026-01-01` (9/9, Tabellenkopf
Z. 2917, Datenzeilen 2919–2927; `m1_bestaetigung_ab.txt`); 5.2 setzt den
Go-Live-Schnitt `2026-09-01`, **ausschliesslich** (`m2_go_live_schnitt.txt`),
und 21.4 wiederholt ihn im Vorsatz („Bestätigungsperiode unverändert bis
`2026-09-01`, ausschliesslich"). ⇒ Der Bezeichner nach 35.1 lautet für den
registrierten Bestand bei allen neun Bots **`2026-01-01/2026-09-01`** — aus 21.4
und 5.2 gebildet.

⚠️ **Ausdrücklich eingetragen:** Der **heutige** Bezeichner in
`research/vorregistrierung/faltenplan.py:336` ist der **Faltenname**
(`falten[-1]["name"]`: `2026-2027` bei `elliott_wave`, `2026` bei den acht
übrigen; gemessen, nur gelesen, `m4_faltenplan_bezeichner.txt` — zwei
Fundstellen, Z. 336 Erzeugung und Z. 368 Konsolenausgabe in `main()`) und damit
nach diesem Registertext **unzulässig**, weil er Kalenderjahre ausserhalb der
Spanne nennt. ⛔ **Die Umstellung ist Handwerk mit eigener Freigabe und nicht
Teil von TB-83**; sie hängt an Fables Antwort auf
`FABLE_ANFRAGE_2026-09-22a_sperrlistenfalle.md` (35.5). *Fable dazu,
zeichengleich:*

> *Folge, Handwerk:* `faltenplan.py:336` bildet den Namen heute aus dem Faltennamen; die Änderung ist eine Zeile und braucht eine Betreiberfreigabe. `auswertung.py` bleibt unberührt — es liest den Namen aus dem Plan, wie auch immer er lautet. Der Erzeuger schreibt denselben Bezeichner in `zellen.csv`; er ist noch nicht geschrieben, es kostet dort nichts. Die ⚠️-Markierung in 21.4 bei `elliott_wave`: bitte den ganzen Eintrag vorlegen, bevor jemand sie als Beleg nimmt — ich habe nur eure Vermutung dazu.

> ⚠️ **Marke (36.1 (4) und 36.3, Fable 22b, TB-84, 22.09.2026):** Die Umstellung
> von `faltenplan.py:336` (und der Ausgabe Z. 368) auf den Bezeichner ist
> **Schritt 3** der Reihenfolge in 36.3 und kommt **erst nach Schritt 2** —
> Voreinstellung von `main()` weg von `ergebnisse/faltenplan.json` und
> Einmal-Schreibsperre (36.1 (4)); davor Schritt 1, die Sperrlisten-Sonde.
> Fable, 22b: *„Wer Schritt 3 vor Schritt 2 macht, hat genau den Fall, den ihr beschreibt."*
> Betreiberfreigabe für alle vier Schritte steht aus (Stand 22.09.2026). Bis
> dahin: `python3 faltenplan.py` nicht aufrufen.

> ⭐⭐ **Berichtigung (38.1, Fable 22h, TB-89, 23.09.2026) — Weg (A):** Der
> Satz „die Änderung ist eine Zeile" im Handwerkszitat oben ist berichtigt.
> Der Bezeichner entsteht **dort, wo die letzte Falte ihren Namen bekommt**
> (`faltenplan.py`, Funktion `_plan`, Zuweisung der Rolle `bestaetigung`): die
> letzte Falte **heisst** die Spanne `2026-01-01/2026-09-01`; Faltenname,
> `bestaetigungsperiode`, Spalte `falte` und Bericht tragen denselben String
> aus derselben Quelle. Weg (B) — zwei Namen für dieselbe Periode — ist
> unzulässig. Umsetzung: TB-90, Freigabe liegt vor.

> ⚠️ **Tatsachennotiz zu den Zeilennummern oben (38.7 (a), TB-88, belegt
> 38.2):** Am Stand `8851f67` steht die Erzeugung auf **Z. 338**, die
> Konsolenausgabe auf **Z. 460** von `faltenplan.py` (Funktionen `_plan` und
> `main`); verschoben durch **`4daa254`** (TB-86 Schritt 2/3). Die Zahlen 336
> und 368 oben bleiben zeichengleich; sie gelten für den Stand, an dem TB-83
> sie gemessen hat.

> ⚠️⚠️ **Tatsachennotiz (38.7 (c), TB-88, Messstand `8851f67`):** Weg (B)
> hätte einen Sperrlistenpunkt berührt — `auswertung.py`, Funktion
> `lies_zellen`, vergleicht die Menge der `falte`-Werte gegen die Faltennamen
> des Plans und bricht unter (B) ab (Sperrlistenpunkt 5). Weg (A) läuft in der
> Probe durch. Einzelheiten in **38.1**.

⚠️ Zur ⚠️-Markierung bei `elliott_wave` in 21.4: Die Zelle lautet wörtlich
`⚠️ **2026-01-01**`; 21.4 trägt keinen Satz, der sie begründet. Fable bat, den
ganzen Eintrag vorzulegen, bevor jemand sie als Beleg nimmt (Anfrage 22a
Punkt 1) — hier nur gemessen, nicht gedeutet.

**Marke am alten Ort:** unter 33.2, nach der Marke aus 34. **Kein** Eintrag in
21.4 — 21.4 bleibt unberührt, 35.1 zitiert es nur.

> ⭐ **35.1 PRÄZISIERT durch R37 (48.5)** (Fable 29b R37, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 35.2 Ergänzung zu 33.3 — `bestaetigungsperiode` wird Feld

**Fable, 22a Abschnitt 3, zeichengleich:**

> **Ergänzung zu 33.3 (Feldliste), je Bot:** `bestaetigungsperiode` — der Bezeichner nach 33.2, genau in dieser Form; die Sonde prüft ihn positiv gegen die aus 21.4 und 5.2 gebildete Spanne.

Die Feldliste in 33.3 wächst damit um **eine Zeile je Bot**; die Sonde prüft
den Wert **positiv** gegen die aus 21.4 und 5.2 gebildete Spanne — dieselbe
Bauart wie bei `horizontbeginn` (34.4). Der Grund, warum die Bestätigungsperiode
nun doch Feld ist, steht in 35.3.

**Marke am alten Ort:** in der Feldliste 33.3, als neue, angefügte
Tabellenzeile — keine bestehende Zeile geändert.

### 35.3 ⭐⭐ Fables sechste Rücknahme — warum die Bestätigungsperiode doch Feld ist

⚠️ **Das ERSETZT 33.4 Punkt 3 („Nicht in die Feldliste") und den Schluss von
34.6 („kein Feld der Feldliste").** Beide Sätze bleiben dort zeichengleich
stehen und tragen die Marke.

**Fables Begründung, 22a Abschnitt 2, zeichengleich:**

> **Aber Punkt 3 eurer Anfrage liefert eine Tatsache, die (3) trotzdem kippt** — nicht die Fundstelle, sondern die Rolle des Namens: Nach Nachtrag 2 (Z. 432–435) liest `auswertung.py` den Namen der Bestätigungsperiode aus dem Plan und sucht damit die Zeile in `zellen.csv`. **Der Name ist ein Schlüssel, den zwei Programme teilen müssen** — das eingefrorene `auswertung.py` und der noch zu schreibende Erzeuger. Ein Schlüssel, den zwei registrierte Programme teilen, ist eine Grösse des Verfahrens und gehört in den Registertext; und was 33.2 nennt, ist nach 33.3 Feld. Damit:

**Und der Registersatz, zeichengleich:**

> **(3), berichtigt:** Die Bestätigungsperiode ist Feld des Abbilds — weil 33.2 sie nennen muss (siehe 3), nicht weil 21.4 sie registriert. Mein Massstab bleibt; seine Anwendung ändert sich mit der Tatsache, dass der Name operativ ist.

**Fable selbst dazu, zeichengleich:**

> Das ist die sechste Rücknahme, und sie hat denselben Grund wie die fünf davor: Ich kannte den Bestand nicht — hier, dass der Name als Schlüssel dient.

**Tatsachennotiz (TB-83, gemessen, nur gelesen, `m3_auswertung_faltenplan.txt`):**
Der Schlüssel ist im eingefrorenen `auswertung.py` sichtbar — Z. 432
`name = plan[bot]["bestaetigungsperiode"]` in der Funktion
`bestaetigungsperiode()` (Z. 430), weitergereicht in Z. 550 und Z. 638. Der
Massstab aus 21m („ein Abbild trägt genau die Grössen seines Abschnitts") bleibt;
was sich ändert, ist die Tatsache, dass 33.2 die Bestätigungsperiode seit 35.1
nennt.

**Marken am alten Ort — zwei:** bei 33.4 Punkt 3 (als eigene Tabellenzeile
unter der Marke aus 34.6) und unter dem Offen-Block in 34.6.

### 35.4 Präzisierung zu 30.2 (3) — wann die Sonde prüft

**Fable, 22a Abschnitt 4, zeichengleich:**

> **Präzisierung zu 30.2 (3):** Der Lauf verwendet den Plan, den `faltenplan.py` zur Laufzeit bildet. Die Sonde vergleicht diesen Plan **vor dem Start des Laufs** mit dem Abbild (Feldmenge und Werte); bei Abweichung bricht der Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Das Abbild ist damit der registrierte Sollzustand, gegen den der gerechnete Plan geprüft wird — nicht die Datei, die `auswertung.py` öffnet.

**Fables Grund, zeichengleich (zwei Absätze aus 22a):**

> *Quelle des Grundes:* 21b (3) — das Einfrieren von `auswertung.py` hat Vorrang; die Prüfung wandert dorthin, wo geändert werden darf (Wrapper, `faltenplan.py`), wie schon bei der Wache. Kein Ergebnis.

> Ohne diese Präzisierung wäre 30.2 (3) beim ersten Lauf falsch: Es gäbe eine gesperrte Datei, die niemand liest, und einen gerechneten Plan, den niemand prüft.

**Tatsachennotiz (TB-83, aus Nachtrag 1 bestätigt, `m3_auswertung_faltenplan.txt`):**
`auswertung.py` bezieht den Plan über **genau einen** Aufruf,
`plan = fp.faltenplan(mess)` in **Z. 589** (`import faltenplan as fp`, Z. 96) —
es **rechnet** ihn zur Laufzeit; die einzige Plandatei, die es öffnet, ist
`benchmark_drawdowns.json` (Z. 590, Sperrlistenpunkt 4), keine
`faltenplan*.json`. ⇒ 30.2 (3) „der Lauf liest genau diese" ist ab hier so zu
lesen, wie 35.4 es sagt: Das Abbild ist der **Sollzustand**, gegen den der
gerechnete Plan **vor dem Start** geprüft wird; bei Abweichung bricht der
Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Sonde und Wrapper sind
**nicht** geschrieben (35.5).

**Marke am alten Ort:** direkt unter 30.2 (3), innerhalb des
Registertext-Blocks — wie die Marke aus 34.3 unter (2).

> ⭐ **„Feldmenge und Werte" heisst: über die registrierte Abbildung (42.2 E3,
> Fable 25b, TB-108, 25.09.2026):** Die Sonde vergleicht den gerechneten Plan
> mit dem Abbild je Feld des Abbilds über den Planschlüssel, aus dem es gebildet
> wird; ein Planschlüssel ausserhalb der registrierten Feldliste des Plans ist
> ein Befund, ein fehlender ebenso. Fables erste Fassung dazu (25a, „trägt keine
> Grösse, die 33.2/33.3 nicht kennt") ist berichtigt (**42.1 D5 → 42.2 E3**).
> Der Text oben bleibt zeichengleich.

> ⭐ **35.4 ERGÄNZT durch R26 (47.9)** (Fable 27c R26, TB-126, 01.10.2026).
> Eintrag und Stand oben bleiben zeichengleich.

### 35.5 Was hier ausdrücklich NICHT getan wird

| | | gehört zu |
|---|---|---|
| ⛔ | **`faltenplan.py:336` auf den neuen Bezeichner umstellen** — keine Freigabe; hängt an Fables Antwort auf die Sperrlistenfalle (Anfrage 22a Punkt 3: `main()` schreibt nach `ergebnisse/faltenplan.json`, Sperrlistenpunkt 2) | Betreiber, nach Fable |
| ⛔ | ⚠️⚠️ **`python3 faltenplan.py` ausführen** — in dieser Sitzung **nicht geschehen**; der Hash von `ergebnisse/faltenplan.json` ist vor **und** nach der Arbeit `0e54ac5c…` (`m6_sperrlisten_hash.txt`) | — |
| ⛔ | **Die Abbild-Datei erzeugen** — jetzt mit dem Feld `bestaetigungsperiode` | eigene Aufgabe, Betreiberfreigabe (33.5) |
| ⛔ | **Die Sonde schreiben** — Feldmenge, Werte, die positiven Prüfungen aus 34.4 und 35.2, der Zeitpunkt aus 35.4 | dieselbe Aufgabe |
| ⛔ | **Den Laufwrapper mit dem Abbruch aus 35.4 bauen** | dieselbe Aufgabe |
| ⛔ | **Einen Hash auf die Sperrliste nehmen** | dieselbe Aufgabe |
| ⛔ | **Irgendeine `.py` ändern** | — |
| ⭐ | **Keine Zahl bewegt:** Faltenliste 33.2 vor und nach dem Eintrag zeichengleich (Beleg M5); die drei Sperrlisten-Hashes unverändert | — |
| ⚠️ | **Offen bei Fable:** *„**Unsicher:** ob `faltenplan.py` den Namen der Bestätigungsperiode noch an anderer Stelle verwendet als Z. 336 (dann mehr als eine Zeile) — Handwerk, zu messen vor der Freigabe."* — die Anfrage 22a Punkt 2 hat dazu gemessen (zwei Fundstellen in `faltenplan.py`, Z. 336 und 368; im Laufkreis zieht alles mit); seine Antwort steht aus | Fable |

*Dieser Abschnitt ist rein additiv: Er trägt vier Texte des Verfahrensprüfers
zeichengleich ein, setzt fünf Marken am alten Ort, entscheidet die in 34.6
offene Frage durch Fables Text — und entfernt nichts.*

---

