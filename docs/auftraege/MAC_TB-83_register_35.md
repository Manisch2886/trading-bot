# TB-83 — Registerabschnitt 35: die Bestätigungsperiode bekommt einen Bezeichner, und 30.2 (3) wird präzisiert

**Sitzungstitel:** `TB-83 Register 35 — Bestaetigungsperiode und Sondenzeitpunkt`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**Erstellt:** 22.09.2026, 07:10 Ortszeit · **Vorgänger:** TB-82 (`f1a0dc7`)
**Erwarteter Ausgangsstand:** `HEAD` = `origin/main` = `f1a0dc7` oder jünger

---

## 0. Was dieser Auftrag ist — und was er NICHT ist

⭐ **Reines Eintragen von Registertext**, wie TB-82. **Vier Einträge**, alle aus
`FABLE_ANTWORT_2026-09-22a_bestaetigungsperiode.md`.

| ⛔ | **NICHT Gegenstand** |
|---|---|
| ⛔ | **`faltenplan.py:336` ändern** (der neue Bezeichner) — ⚠️ **keine Freigabe**, und es hängt an Fables Antwort auf `FABLE_ANFRAGE_2026-09-22a_sperrlistenfalle.md` |
| ⛔ | ⚠️⚠️ **`python3 faltenplan.py` ausführen** — **NIEMALS in diesem Auftrag.** `main()` überschreibt `ergebnisse/faltenplan.json`, **Sperrlistenpunkt 2** (`0e54ac5c…`). Siehe Abbruchkriterium 5 |
| ⛔ | Abbild-Datei, Sonde, Hash, Wrapper — jedes mit eigener Freigabe |
| ⛔ | Irgendeine `.py` ändern |

---

## 1. Schritt 0

1. **Schlüsselbund entsperren**, Kopfzeile muss „Claude Max" nennen.
2. **Committe, was im Arbeitsbaum liegt.** Erwartet: ein bis zwei untrackte
   Dateien unter `docs/projektfuehrung/`
   (`FABLE_ANTWORT_2026-09-22a_bestaetigungsperiode.md`,
   `FABLE_ANFRAGE_2026-09-22a_sperrlistenfalle.md`) — *falls der Betreiber sie
   schon committet hat: nur prüfen.*
3. **Nachweis:** `git status --short` leer, HEAD notieren.

---

## 2. Die Regel aus TB-82 gilt weiter: Marke AM ALTEN ORT

Jeder Eintrag wird **zweimal** sichtbar: voller Text in **Abschnitt 35**, dazu
ein **eingerückter Hinweisblock** (`>`) oder eine **Tabellenzeile** direkt beim
berichtigten Satz. ⚠️ **Nur hinzufügen, nichts ändern, nichts entfernen.**

⭐ **Prüfbar:** `git diff --numstat -- docs/VORREGISTRIERUNG_neuselektion.md`
⇒ **zweite Spalte `0`.**

---

## 3. Die vier Einträge

### 35.1 — Ergänzung zu 33.2: die Bestätigungsperiode und ihr Bezeichner

**Herkunft:** `FABLE_ANTWORT_2026-09-22a_bestaetigungsperiode.md`, Abschnitt 3,
**zeichengleich:**

> **Ergänzung zu 33.2 (Bestätigungsperiode):** Die Bestätigungsperiode eines Bots ist die Datumsspanne von „Bestätigung ab" (21.4) bis zum Go-Live-Schnitt (5.2), Ende ausschliesslich. Sie ist keine Selektionsfalte und keine Falte im Sinn von 4a; ihre Länge ist von der Faltenlänge des Bots unabhängig, und dass sie kürzer als eine Faltenlänge ist, ist gewollt — (1b) betrifft sie nicht. Ihr **Bezeichner** in Plan, Abbild, `zellen.csv` und Berichten ist die Spanne selbst in der Form `JJJJ-MM-TT/JJJJ-MM-TT` (Beginn/Ende, Ende ausschliesslich); für den registrierten Bestand bei allen neun Bots `2026-01-01/2026-09-01`. Ein Bezeichner, der Kalenderjahre ausserhalb der Spanne nennt, ist unzulässig.

**Fables Quelle des Grundes, zeichengleich:**

> *„21.4 und 5.2 registrieren die Spanne; Verfahren B definiert die Bestätigungsperiode als den einzigen Out-of-Sample-Zeitraum (Übergabe Abschnitt 1). Ein Name, der mehr verspricht als die Spanne, würde beim Lesen der Ergebnisse — nach dem Lauf, wenn niemand mehr nachrechnet — als Zeitraum verstanden."*

⭐ **Tatsachennotiz, von dir zu messen (M1/M2):** dass 21.4 bei **allen neun**
Bots `2026-01-01` führt und 5.2 den Go-Live-Schnitt `2026-09-01` ausschliesslich
setzt — **das ist die Grundlage des Bezeichners und wird nicht übernommen,
sondern gemessen.**

⚠️ **Dazu, ausdrücklich einzutragen:** Der heutige Bezeichner in
`faltenplan.py:336` ist der **Faltenname** (`2026-2027` bei `elliott_wave`,
`2026` bei den acht übrigen) und damit nach diesem Registertext **unzulässig**.
⛔ **Die Umstellung ist Handwerk mit eigener Freigabe und NICHT dieser Auftrag.**

**Marke am alten Ort:** unter 33.2; zusätzlich in 21.4 **kein** Eintrag (21.4
bleibt unberührt — 35.1 zitiert es nur).

### 35.2 — Ergänzung zu 33.3: `bestaetigungsperiode` wird Feld

**Herkunft:** 22a, Abschnitt 3, **zeichengleich:**

> **Ergänzung zu 33.3 (Feldliste), je Bot:** `bestaetigungsperiode` — der Bezeichner nach 33.2, genau in dieser Form; die Sonde prüft ihn positiv gegen die aus 21.4 und 5.2 gebildete Spanne.

**Marke am alten Ort:** in der Feldliste 33.3, als neue Zeile ⭐ *(Achtung:
Die Feldliste ist eine Tabelle — die neue Zeile wird **angefügt**, keine
bestehende geändert.)*

### 35.3 — ⭐⭐ Fables sechste Rücknahme: warum die Bestätigungsperiode doch Feld ist

⚠️ **Das ersetzt 33.4 Punkt 3 („Nicht in die Feldliste") und den Rest von 34.6.**

**Fables Begründung, zeichengleich:**

> *„Punkt 3 eurer Anfrage liefert eine Tatsache, die (3) trotzdem kippt — nicht die Fundstelle, sondern die Rolle des Namens: Nach Nachtrag 2 (Z. 432–435) liest `auswertung.py` den Namen der Bestätigungsperiode aus dem Plan und sucht damit die Zeile in `zellen.csv`. **Der Name ist ein Schlüssel, den zwei Programme teilen müssen** — das eingefrorene `auswertung.py` und der noch zu schreibende Erzeuger. Ein Schlüssel, den zwei registrierte Programme teilen, ist eine Grösse des Verfahrens und gehört in den Registertext; und was 33.2 nennt, ist nach 33.3 Feld."*

**Und der Registersatz, zeichengleich:**

> **(3), berichtigt:** Die Bestätigungsperiode ist Feld des Abbilds — weil 33.2 sie nennen muss (siehe 3), nicht weil 21.4 sie registriert. Mein Massstab bleibt; seine Anwendung ändert sich mit der Tatsache, dass der Name operativ ist.

⭐ **Fable selbst dazu:** *„Das ist die sechste Rücknahme, und sie hat denselben
Grund wie die fünf davor: Ich kannte den Bestand nicht — hier, dass der Name als
Schlüssel dient."*

**Marken am alten Ort — hier sind es ZWEI:**
- bei **33.4 Punkt 3**: „Nicht in die Feldliste" ist **ersetzt** durch 35.3
- bei **34.6**: der Vermerk *„Welche der zwei Formen gilt, ist offen — bei
  Fable"* ist **beantwortet** (35.1), und *„Die Folge bleibt: kein Feld"* ist
  **ersetzt** (35.3)

### 35.4 — Präzisierung zu 30.2 (3): wann die Sonde prüft

**Herkunft:** 22a, Abschnitt 4, **zeichengleich:**

> **Präzisierung zu 30.2 (3):** Der Lauf verwendet den Plan, den `faltenplan.py` zur Laufzeit bildet. Die Sonde vergleicht diesen Plan **vor dem Start des Laufs** mit dem Abbild (Feldmenge und Werte); bei Abweichung bricht der Laufwrapper ab, bevor `auswertung.py` aufgerufen wird. Das Abbild ist damit der registrierte Sollzustand, gegen den der gerechnete Plan geprüft wird — nicht die Datei, die `auswertung.py` öffnet.

**Fables Grund, zeichengleich:**

> *„21b (3) — das Einfrieren von `auswertung.py` hat Vorrang; die Prüfung wandert dorthin, wo geändert werden darf (Wrapper, `faltenplan.py`), wie schon bei der Wache. … Ohne diese Präzisierung wäre 30.2 (3) beim ersten Lauf falsch: Es gäbe eine gesperrte Datei, die niemand liest, und einen gerechneten Plan, den niemand prüft."*

⭐ **Tatsachennotiz aus Nachtrag 1, zu bestätigen (M3):** `auswertung.py` bezieht
den Plan über **genau einen** Aufruf, `fp.faltenplan(mess)`, Zeile 589 — es
**rechnet** ihn, es liest keine Plandatei.

**Marke am alten Ort:** unter 30.2 (3).

---

## 4. Die Messungen (bestätigen, nicht übernehmen)

| # | Messung | erwartet |
|---:|---|---|
| **M1** | 21.4, Spalte „Bestätigung ab", alle neun Bots | **`2026-01-01` bei allen neun** |
| **M2** | 5.2, Go-Live-Schnitt | **`2026-09-01`, ausschliesslich** |
| **M3** | `grep -n "fp.faltenplan" research/vorregistrierung/auswertung.py` | **genau ein Treffer, Z. 589** |
| **M4** | `grep -n "bestaetigungsperiode" research/vorregistrierung/faltenplan.py` | **zwei Treffer: 336 (Erzeugung), 369 (nur Ausgabe)** |
| **M5** | ⭐ **Die Faltenlisten in 33.2 vor und nach deiner Arbeit** | **identisch** — dieser Auftrag bewegt keine Zahl |
| **M6** | ⚠️ **Hash von `research/vorregistrierung/ergebnisse/faltenplan.json`** vor UND nach der Arbeit | **`0e54ac5cf6d554d271c891d7d3ee0f9ebb60b6042b5234ad8d31bfaf60d32339` beide Male** |

**Belege:** `docs/belege/TB-83/m1…m6.txt`, Befehl in Zeile 1.

---

## 5. ⛔ Abbruchkriterien

| # | Wenn … | dann |
|---:|---|---|
| **1** | `numstat` auf das Register zeigt in Spalte 2 etwas anderes als `0` | ⛔ ABBRUCH, kein Commit |
| **2** | Eine Faltenliste in 33.2 unterscheidet sich nachher | ⛔ ABBRUCH |
| **3** | Ein Fable-Zitat lässt sich nicht zeichengleich übernehmen | ⛔ Anhalten, melden, **nicht glätten** |
| **4** | Du meinst, eine `.py` ändern zu müssen | ⛔ ABBRUCH |
| **5** | ⚠️⚠️ **Der Hash von `ergebnisse/faltenplan.json` weicht ab (M6)** | ⛔⛔ **SOFORT ABBRUCH und melden.** Das hiesse, `faltenplan.py main()` wurde ausgeführt — **Sperrlistenpunkt 2 gebrochen.** Nichts committen, nichts reparieren, nur melden |
| **6** | Abschnitt 35 existiert bereits | ⛔ Anhalten — der Auftrag lief schon |
| **7** | Ein anderer Sperrlisten-Hash ändert sich (`a163c498…`, `4549395f…`) | ⛔ ABBRUCH |

---

## 6. Schritte

| # | Tun | Nachweis |
|---:|---|---|
| **0** | Schlüsselbund, Arbeitsbaum, HEAD | `git status --short` leer |
| **1** | **M1–M4 und M6 (vorher)** messen, Belege schreiben | fünf Dateien |
| **1b** | **M5 vorher**: Faltenlisten aus 33.2 festhalten | `m5_faltenlisten.txt` |
| **2** | **Abschnitt 35** schreiben — 35.1 bis 35.4, Fable-Text zeichengleich, dazu ein Schlussteil „Was hier NICHT getan wird" | Commit |
| **3** | **Die fünf Marken am alten Ort**: 33.2, 33.3, 33.4 Punkt 3, 34.6, 30.2 (3) — ⚠️ **nur einfügen** | Commit |
| **4** | **M5 nachher** und **M6 nachher** | 0 Abweichungen, Hash gleich |
| **5** | `numstat` prüfen — Spalte 2 = `0` | Abschlussbeleg |
| **6** | `grep -c "^## 35\."` = `1` | Beleg |
| **7** | Alle drei Sperrlisten-Hashes | unverändert |
| **8** | **`AKTUELLER_AUFTRAG.md`**: ⭐ **bereits auf TB-83 gesetzt** — ⚠️ **nur lesen, nicht ändern.** Zeigt `numstat` für diese Datei irgendetwas, hast du sie angefasst: anhalten | `grep -c "TB-83"` ≥ 1 |
| **9** | **Journalblock** und `docs/auftraege/ERGEBNIS_TB-83.md` | Commit |
| **10** | **Abgabe**: Status leer, `numstat` nachgetragen | Abschlussbeleg |

---

## 7. Ins Ergebnisdokument

1. Die vier Einträge mit Zeilennummer im Register
2. **M1–M6 mit gemessenem Wert**
3. Der `numstat`-Nachweis
4. ⚠️ **M6 ausdrücklich hervorheben** — der Hash der gesperrten Datei vor und nach
5. ⭐ **Was NICHT getan wurde**: kein Code, kein `python3 faltenplan.py`, keine
   Abbild-Datei, keine Sonde, kein Wrapper, kein Hash auf die Sperrliste
6. **Offen und benannt:** die Umstellung von `faltenplan.py:336` auf den neuen
   Bezeichner — hängt an Fables Antwort auf die Sperrlisten-Falle

---

## In einfacher Sprache

Fable hat zwei weitere Einträge verlangt und dabei eine eigene frühere Aussage
zurückgenommen — die sechste in dieser Woche.

**Erstens:** Die „Bestätigungsphase" bekommt einen eindeutigen Namen. Bisher hiess
sie bei einem Bot „2026-2027", obwohl sie im September 2026 endet. Künftig heisst
sie schlicht nach ihrer Zeitspanne: `2026-01-01/2026-09-01`. **Zweitens:** Dieser
Name ist zugleich der Schlüssel, über den zwei Programme dieselbe Tabellenzeile
finden — deshalb gehört er ins Regelwerk und in die maschinenlesbare Datei.
Fable hatte zuvor das Gegenteil entschieden und korrigiert sich. **Drittens:**
Er stellt klar, wann die Prüfsonde läuft — **vor** dem Start, und bei Abweichung
bricht alles ab, bevor die Auswertung überhaupt beginnt.

**Dieser Auftrag schreibt nur Text.** Kein Programm wird geändert, keine Zahl
bewegt.

⚠️⚠️ **Eine Warnung steht gross darin:** Das Programm `faltenplan.py` darf in
dieser Sitzung **nicht gestartet** werden. Es überschreibt beim normalen Aufruf
eine Datei, die unveränderlich bleiben muss. Deshalb wird deren Prüfsumme vor
**und** nach der Arbeit gemessen — weichen sie ab, bricht die Sitzung sofort ab.
