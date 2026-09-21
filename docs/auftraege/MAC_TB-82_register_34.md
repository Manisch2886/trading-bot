# TB-82 — Registerabschnitt 34: Fables fünf Einträge aus 21l/21m plus eine Berichtigung von uns

**Sitzungstitel:** `TB-82 Register 34 — Faltenregeln, horizontbeginn, vier→neun`
**Auftraggeber:** der steuernde Chat (Sitzung vom 21.09.2026, 18:53)
**Erstellt:** 21.09.2026, 23:55 Ortszeit · **Vorgänger:** TB-81 (`6071f32`)
**Erwarteter Ausgangsstand:** `HEAD` = `origin/main` = `ad020b5` oder jünger

---

## 0. Was dieser Auftrag ist — und was er ausdrücklich NICHT ist

⭐ **Reines Eintragen von Registertext.** Sechs Einträge, fünf davon zeichengleich
von Fable, einer eine Berichtigung eines eigenen Satzes.

| ⛔ | **NICHT Gegenstand dieses Auftrags** |
|---|---|
| ⛔ | **Die Abbild-Datei erzeugen** — eigene Aufgabe, eigene Betreiberfreigabe |
| ⛔ | **Die Sonde schreiben** — dito |
| ⛔ | **Einen Hash auf die Sperrliste nehmen** — dito |
| ⛔ | **`faltenplan.py` oder irgendeine `.py` ändern** — ⚠️ **keine Freigabe erteilt**; die vom 21.09. galt für Bedingung (i) und ist verbraucht |
| ⛔ | **Die Wache aus 29.4 einbauen** — das ist TB-30b, nicht dieser Auftrag. Hier wird nur der **Registertext** berichtigt |

⚠️ **Wenn du an irgendeiner Stelle den Eindruck hast, Code ändern zu müssen:
brich ab und melde es.** Der Auftrag ist dann falsch geschnitten, nicht der Code.

---

## 1. Schritt 0 — vor allem anderen

1. **Schlüsselbund entsperren** (zweites Terminalfenster, `security unlock-keychain`).
   ⭐ Kopfzeile muss „Claude Max" nennen.
2. **Committe, was im Arbeitsbaum liegt**, bevor du anfängst. Erwartet werden
   **sechs untrackte Dateien** unter `docs/projektfuehrung/`:
   - `BESTANDSAUFNAHME_TB-30b.md`
   - `NACHTRAG_1_BESTANDSAUFNAHME_TB-30b.md`
   - `NACHTRAG_2_BESTANDSAUFNAHME_TB-30b.md`
   - `FABLE_ANFRAGE_2026-09-21g_berichtigung_und_bestaetigungsperiode.md`
   - `FABLE_ANTWORT_2026-09-21l_standpruefung.md`
   - `FABLE_ANTWORT_2026-09-21m_faltenplan_pruefung.md`

   *Falls der Betreiber sie bereits committet hat: gut, dann ist der Baum sauber.
   **Nicht erneut committen, nur prüfen.***
3. **Nachweis:** `git status --short` leer, `git rev-parse --short HEAD` notieren.
4. ⛔ **Erst danach** mit Schritt 1 beginnen.

---

## 2. ⭐⭐ Die tragende Regel dieses Auftrags: die Marke steht AM ALTEN ORT

**Fables Begründung zu Frage 3 in 21m, wörtlich:**

> *„Wer 30.2 (2) liest und abschreibt, sieht 33.2 nicht — genau der Fehler aus 21h. Eine Marke am falschen Satz kostet eine Zeile; ein Hinweis drei Abschnitte weiter kostet irgendwann eine Rücknahme."*

⇒ **Jeder der sechs Einträge wird an ZWEI Stellen sichtbar:**

| | wo | was |
|---|---|---|
| **(a)** | **Im neuen Abschnitt 34** | der volle Text, Herkunft, Begründung |
| **(b)** | ⭐ **Am alten Ort**, direkt unter dem berichtigten Satz | ein **eingerückter Hinweisblock** (`>`), zwei bis vier Zeilen, mit Verweis auf 34.x |

⚠️⚠️ **(b) fügt nur hinzu — es ändert und entfernt NICHTS.** Der alte Satz bleibt
zeichengleich. **Das ist die Bauart der Tatsachennotiz unter Sperrlistenpunkt 2**
(Abschnitt 10), an der es sich messen lässt.

⭐ **Prüfbar:** `git diff --numstat -- docs/VORREGISTRIERUNG_neuselektion.md`
⇒ **zweite Spalte muss `0` sein.** Jede Ausnahme wäre ein Fehler in diesem
Auftrag und ist einzeln zu melden, nicht zu erklären.

---

## 3. Die sechs Einträge

### 34.1 — Ergänzung zu 33.2: Falten mit Faltenlänge L > 1

**Herkunft:** `FABLE_ANTWORT_2026-09-21m_faltenplan_pruefung.md`, Frage 1 (1a),
**zeichengleich:**

> **Ergänzung zu 33.2:** Bei Faltenlänge L > 1 ist ein Kalenderjahr J erstes Jahr einer Selektionsfalte, wenn J die Bedingungen (i) und (ii) nach 25 erfüllt; die Falte umfasst J bis J + L − 1. Die erste Selektionsfalte beginnt mit dem ersten Kalenderjahr, das (i) und (ii) erfüllt; die folgenden Falten schliessen lückenlos an.

**Fables Grund, zeichengleich zu übernehmen:**

> *„(i) prüft den Vorlauf am 1. Januar — der einzige 1. Januar, an dem eine Falte beginnt, ist der ihres ersten Jahres. (ii) muss am ersten Jahr geprüft werden, weil die Falte sonst mit Jahren beginnen könnte, in denen der Bot nichts handelt — der Kapitalpfad (29) startet am 1. Januar der ersten Falte und braucht dort Handelbarkeit."*

⭐ **Tatsachennotiz, die du selbst misst** (Schritt 4): Betrifft nur
`elliott_wave` (L = 2); die acht übrigen haben L = 1. **Die Faltenliste ändert
sich durch diese Ergänzung nicht** — nachzuweisen durch Vergleich mit 33.2.

**Marke am alten Ort:** unter 33.2, nach dem Registertext-Block.

### 34.2 — Ergänzung zu 33.2: der Rest vor dem Go-Live-Schnitt

**Herkunft:** 21m, Frage 1 (1b), **zeichengleich:**

> **Ergänzung zu 33.2:** Ein Rest von weniger als L Kalenderjahren zwischen der letzten vollen Selektionsfalte und dem Go-Live-Schnitt ist keine Selektionsfalte. Sein Verhältnis zur Bestätigungsperiode regelt 21.4; 33.2 trifft dazu keine Aussage.

**Fables Grund, zeichengleich:**

> *„4a kennt nur ganze Falten; eine Teilfalte hätte weniger Beobachtungen als die übrigen und ginge mit gleichem Gewicht in den Faltenmedian — eine Verzerrung, die 4a nirgends zulässt."*

⭐⭐ **Eine Messung von uns gehört dazu — sie beantwortet Fables ausdrückliche
Unsicherheit** (*„ob 21.4 den Rest vor Go-Live bereits regelt — dann ist (1b) ein
Verweis statt einer Regel"*):

> **Tatsachennotiz (steuernder Chat, 21.09.2026, HEAD `ad020b5`):** Gesucht
> wurde im ganzen Register nach `Rest`, `Teilfalte` und `angebrochene`.
> **Null Treffer.** 21.4 führt ausschliesslich erste Falte, Faltenzahl,
> Faltenlänge und „Bestätigung ab". ⇒ **(1b) ist eine Regel, kein Verweis.**

⚠️ **Nachzumessen in Schritt 4** — die Zahl oben ist zu bestätigen, nicht zu
übernehmen. Weicht sie ab: eintragen, was du misst, und melden.

**Marke am alten Ort:** unter 33.2, zusammen mit 34.1.

### 34.3 — Berichtigung zu 30.2 (2): `3b (b)` lies `3b (a)`

**Herkunft:** 21m, Frage 3, **zeichengleich:**

> **Berichtigung zu 30.2 (2):** Die Fundstelle „Trockenlauf nach 3b (b)" lies „3b (a)". Gemeint ist der Trockenlauf aus 3b (a), der die `MIN_HISTORY_*`-Tabelle aus 3b (b) anwendet; ein zweiter Trockenlauf existiert nicht.

⚠️⚠️ **Marke am alten Ort ist hier PFLICHT und der eigentliche Punkt** — genau
dieser Eintrag ist der Grund für die Regel in Abschnitt 2 oben. Der Hinweisblock
steht **direkt unter 30.2 (2)**.

⭐ **Der Hinweis in 33.2** (TB-81, „Zitierhinweis") bleibt zeichengleich stehen
und bekommt einen Satz, dass die ausdrückliche Berichtigung jetzt in 34.3 steht.

### 34.4 — Ergänzung zu 33.3: `horizontbeginn` als Zeichenkette oder Datum

**Herkunft:** 21m, Frage 4, **zeichengleich:**

> **Ergänzung zu 33.3, Feld `horizontbeginn`:** Der Wert ist entweder ein Datum im Format `JJJJ-MM-TT` oder die Zeichenkette `"kein Horizont"` — genau eine der beiden Formen. JSON-`null`, ein fehlender Schlüssel oder eine leere Zeichenkette sind Fehlschläge der Sonde. Die Sonde prüft den Wert positiv gegen diese zwei Formen, nicht das Vorhandensein des Schlüssels.

**Fables Grund, zeichengleich:**

> *„Eine positive Prüfung gegen eine abschliessende Menge ersetzt ein Urteil über Abwesenheit. … ‚Gesetzt, nicht weggelassen' hiess: Wer die Datei liest, soll lesen, dass der Bot keinen Horizont hat — nicht schliessen, dass ihm einer fehlt. Eine Zeichenkette tut das; `null` verlangt Kenntnis der Konvention."*

⭐ **Folge, die Fable selbst zieht und die einzutragen ist:**
`faltenplan_tb80.json` (Schlüssel mit `null`) ist **auch daran** kein Abbild —
*„das war es nach 33.3 schon nicht."*

**Marke am alten Ort:** in der Feldliste 33.3, in der Zeile `horizontbeginn`.

### 34.5 — Berichtigung zu 29.4: „vier" → „neun" Optimierer

**Herkunft:** `FABLE_ANTWORT_2026-09-21l_standpruefung.md`, Punkt 4 (b),
**zeichengleich:**

> **Berichtigung zu 29.4:** Die Wache „frühester Einstieg ≥ Beginn der ersten Selektionsfalte" wird in **allen neun** `multi_symbol_optimise.py` eingebaut, nicht nur in den vier Aktien-Optimierern. Der Bericht führt je Bot Horizontbeginn (oder „kein Horizont"), Beginn der ersten Selektionsfalte und frühesten Einstieg nebeneinander auf.

**Fables Quelle des Grundes, zeichengleich:**

> *„Die Regel 29 (Kapitalpfad beginnt am 1. Januar der ersten Selektionsfalte) gilt je Bot für alle neun; 21c 3.2 hat den Fall für Krypto ausdrücklich benannt … ‚Die vier' stammt aus 21b, als die Wache noch gegen den Horizontbeginn prüfte, den nur Aktien-Bots haben. Mit dem Wechsel des Prüfdatums in 21c/29.4 hätte die Zahl mitwandern müssen; sie ist es nicht — mein Versehen."*

⭐ **Tatsachennotiz, von uns gemessen (21.09.2026, HEAD `6071f32`), zu
bestätigen in Schritt 4:** In **keinem** der neun `multi_symbol_optimise.py`
steht heute eine Wache (`assert`/`raise`/„Wache" je Datei: 0). ⇒ Der Einbau ist
ein **Ersteinbau**, keine Änderung — und er ist **TB-30b**, nicht dieser Auftrag.

**Marke am alten Ort:** unter 29.4, direkt am Satz „in den vier
`multi_symbol_optimise.py`".

### 34.6 — ⚠️ Berichtigung zu 33.4 Punkt 3: eine Fundstelle von uns war falsch

⚠️ **Das ist kein Fable-Eintrag, sondern die Berichtigung eines eigenen Satzes.**

**Was in 33.4 Punkt 3 steht** (bleibt zeichengleich): *„Sie steht **bereits** in
Register 21.4 und folgt aus Faltenlänge und Go-Live-Schnitt (`elliott_wave`
`2026-2027`, die acht übrigen `2026`)."*

**Einzutragen:**

> **Berichtigung zu 33.4 Punkt 3 (steuernder Chat, 21.09.2026).** Die Fundstelle
> „21.4" trägt den Satz nicht. **Gemessen:** 21.4 führt die Spalte
> **„Bestätigung ab"** mit dem Wert `2026-01-01` **für alle neun Bots**; die
> Werte `2026-2027` und `2026` kommen dort nicht vor. Gegenprobe über das ganze
> Register: `2026-2027` hat **genau einen** Treffer, und das ist der berichtigte
> Satz selbst. **Die Werte stammen aus `research/vorregistrierung/faltenplan.py:336`**
> (`falten[-1]["name"]`), also aus dem Code. **Registriert ist die
> Bestätigungsperiode gleichwohl** — ihr **Beginn** in 21.4 (`2026-01-01`), ihr
> **Ende** in 5.2 (Go-Live-Schnitt `2026-09-01`, ausschliesslich), also als
> **Datumsspanne statt als Faltenname**. ⭐ **Fables Schluss in 21m Frage 2 (3)
> bleibt davon unberührt:** Sein erster Halbsatz — *„33.2 nennt sie nicht"* —
> trägt allein; die Bestätigungsperiode ist **kein Feld** der Feldliste.

⚠️⚠️ **Dazu eine offene Frage, die als offen einzutragen ist — nicht zu
beantworten:**

> **Offen (an Fable, 21g Punkt 3):** Der Begriff „Bestätigungsperiode" trägt
> zwei Formen — im Register eine **Datumsspanne** (`2026-01-01` bis
> `2026-09-01`), in `faltenplan.py` einen **Faltennamen**. Für `elliott_wave`
> klaffen sie: Der Name lautet `2026-2027`, die Periode endet am `2026-09-01`.
> ⚠️ **Welche Form gilt, ist nicht registriert.** Die Frage liegt bei Fable
> (Anfrage 21g); **dieser Abschnitt entscheidet sie nicht.**

**Marke am alten Ort:** unter 33.4 Punkt 3.

---

## 4. ⭐ Die Messungen, die du selbst machst (nicht übernehmen — bestätigen)

| # | Messung | erwartet | wenn abweichend |
|---:|---|---|---|
| **M1** | `grep -n -i "\brest\b\|Teilfalte\|angebrochene" docs/VORREGISTRIERUNG_neuselektion.md` | **0 Treffer** (vor deinen Einträgen) | eintragen, was du misst; 34.2 anpassen; **melden** |
| **M2** | `grep -c "2026-2027" docs/VORREGISTRIERUNG_neuselektion.md` | **1** (nur 33.4) | dito für 34.6 |
| **M3** | 21.4: Spalte „Bestätigung ab" je Bot | **`2026-01-01` bei allen neun** | dito |
| **M4** | Wachen je Optimierer: `grep -c "assert \|raise \|Wache" strategies/<bot>/multi_symbol_optimise.py` für alle neun | **alle 0** | dito für 34.5 |
| **M5** | ⭐ **Die Faltenliste vor und nach dem Eintrag** — aus 33.2 abgeschrieben, gegen 21.4 geprüft | **identisch**, neun Bots, 0 Abweichungen | ⛔ **ABBRUCH** — siehe Abbruchkriterium 2 |

⭐ **M5 ist der Kern:** Dieser Auftrag ändert **Regeltext**, nicht Zahlen. Wenn
sich eine Faltenliste bewegt, ist etwas falsch verstanden worden.

**Belege:** je Messung eine Datei unter `docs/belege/TB-82/`
(`m1_rest.txt` … `m5_faltenlisten.txt`), mit dem ausgeführten Befehl in Zeile 1.

---

## 5. ⛔ Abbruchkriterien — bei jedem sofort anhalten und melden

| # | Wenn … | dann |
|---:|---|---|
| **1** | `git diff --numstat` auf das Register zeigt in der **zweiten Spalte etwas anderes als `0`** | ⛔ **ABBRUCH.** Kein Commit. Melden, welche Zeilen verschwunden sind |
| **2** | ⭐ **Irgendeine Faltenliste in 33.2 unterscheidet sich nach deiner Arbeit von vorher** | ⛔ **ABBRUCH.** Dieser Auftrag darf keine Zahl bewegen |
| **3** | Ein Fable-Zitat lässt sich **nicht zeichengleich** übernehmen (Sonderzeichen, Umbruch) | ⛔ Anhalten, melden — **nicht glätten** |
| **4** | Du meinst, eine `.py` ändern zu müssen | ⛔ **ABBRUCH** (Abschnitt 0) |
| **5** | Ein Sperrlisten-Hash ändert sich | ⛔ **ABBRUCH.** Die drei: `a163c498…`, `0e54ac5c…`, `4549395f…` |
| **6** | Abschnitt 34 existiert bereits | ⛔ Anhalten — der Auftrag lief schon einmal |

---

## 6. Schritte

| # | Tun | Nachweis |
|---:|---|---|
| **0** | Schlüsselbund, Arbeitsbaum, HEAD | `git status --short` leer |
| **1** | **M1–M4 messen**, Belege schreiben | vier Dateien unter `docs/belege/TB-82/` |
| **1b** | **M5 vorher**: Faltenliste aus 33.2 in `m5_faltenlisten.txt` festhalten | Datei |
| **2** | **Abschnitt 34 schreiben** — 34.1 bis 34.6, in dieser Reihenfolge, Fable-Text zeichengleich | Commit |
| **3** | **Die sechs Marken am alten Ort** setzen (33.2 ×2, 30.2 (2), 33.3, 29.4, 33.4) — ⚠️ **nur einfügen** | Commit |
| **4** | **M5 nachher** messen und gegen „vorher" halten | 0 Abweichungen in derselben Datei |
| **5** | **`numstat` prüfen** — zweite Spalte `0` | in den Abschlussbeleg |
| **6** | **Abschnitt 34 genau einmal** vorhanden (`grep -c "^## 34\."`) | `1` |
| **7** | **Sperrlisten-Hashes** nachrechnen | drei unverändert |
| **8** | **`AKTUELLER_AUFTRAG.md`**: ⭐ **Die Tabelle ist bereits auf TB-82 gesetzt** (steuernder Chat, 21.09.2026) — sonst hätte die Wache im Einfügesatz deinen Start abgebrochen. ⚠️ **Nur prüfen, nicht ändern:** nennt die Tabelle genau eine Zeile, und steht dort `TB-82`? | `grep -c "TB-82" docs/auftraege/AKTUELLER_AUFTRAG.md` ≥ 1, `wc -l` unverändert |
| **9** | **Journalblock** und **Ergebnisdokument** unter `docs/auftraege/ERGEBNIS_TB-82.md` | Commit |
| **10** | **Abgabe**: Status leer, `numstat` nachgetragen | Abschlussbeleg |

⚠️ **Zu Schritt 8:** An dieser Datei wurde am 21.09. schon einmal versehentlich
alles überschrieben (`1 86` im numstat). **Sie ist hier nur zu lesen.** Wenn
`numstat` für `AKTUELLER_AUFTRAG.md` überhaupt etwas zeigt, hast du sie
angefasst — dann anhalten und melden.

---

## 7. Was in das Ergebnisdokument gehört

1. Die sechs Einträge mit Fundstelle im Register (Zeilennummer nach dem Eintrag)
2. **M1–M5 mit gemessenem Wert**, nicht mit dem erwarteten
3. Der `numstat`-Nachweis, zweite Spalte
4. ⭐ **Ausdrücklich: was NICHT getan wurde** — kein Code, keine Abbild-Datei,
   keine Sonde, kein Hash, keine Wache eingebaut
5. ⚠️ **Die offene Frage aus 34.6** (zwei Formen der Bestätigungsperiode) als
   offen benannt, mit dem Vermerk, dass sie bei Fable liegt

---

## In einfacher Sprache

Fable hat den Auswertungsplan geprüft und fünf kleine Einträge ins Regelwerk
verlangt. Dazu kommt einer von uns: Ich hatte eine Angabe mit einer Fundstelle
belegt, die sie nicht trägt — das wird berichtigt, ohne den alten Satz zu
löschen.

**Dieser Auftrag schreibt nur Text.** Er ändert kein Programm, erzeugt keine
Datei und bewegt keine Zahl. **Wenn sich doch eine Zahl bewegt, bricht die
Sitzung ab** — das ist die wichtigste Sicherung.

Eine Neuerung: Jede Berichtigung wird **an zwei Stellen** sichtbar — im neuen
Abschnitt und **direkt beim alten Satz**. Fable hat den Grund geliefert: Wer den
alten Satz liest und abschreibt, blättert nicht drei Abschnitte weiter.
