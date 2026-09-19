# TB-59 Backlog-Einarbeitung (n) bis (t) — an: Claude Code am Mac (lokale Sitzung)

**Sitzungstitel für Claude Code: `TB-59 Backlog-Einarbeitung`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, Zweig `main`, **direkt auf `main`** — kein
Zweig, kein PR (Regelweg für Dokumentation, `ARBEITSWEISE.md` Abschnitt 5b).
Ausgangsstand: `HEAD` = **`b600a65`**, Arbeitsbaum sauber (gemessen 19.09.2026,
23:0x Ortszeit).

---

## 0. Der Gegenstand in einem Satz

**Acht abgelegte Nachträge werden in `docs/projektfuehrung/BACKLOG.md`
eingearbeitet, und `ARBEITSWEISE.md` Abschnitt 10 wird durch einen Verweis
ersetzt.** Nichts ausserhalb von `docs/` wird angefasst.

⚠️ **Diese Aufgabe ändert keinen Code, keine Daten, keine Datenbank.** Sie
braucht deshalb **keine Datenbanksicherung und keinen Basislauf** — die
Auflagen aus `ARBEITSWEISE.md` Abschnitt 7c gelten für Aufgaben, die den
Betriebspfad berühren. Was stattdessen gilt, steht in Abschnitt 6 dieses
Auftrags.

---

## 1. Die harten Auflagen — sie gelten für jeden Schritt

| | |
|---|---|
| ⚠️⚠️ | **Nur `docs/`.** Nichts ausserhalb. Die Sperrliste gilt unverändert |
| ⚠️⚠️ | **`git diff --numstat` je geänderter Datei**, und **jede entfernte Zeile einzeln der Ersetzung zugeordnet**, die sie verursacht hat. Ausser beim Ersatz in Abschnitt 4 dieses Auftrags ist die erwartete zweite Spalte überall **0** |
| ⚠️⚠️ | **Nichts inhaltlich umformuliert.** Die Texte der Nachträge werden **übernommen**, nicht nacherzählt. ⭐ **Findest du einen Sachfehler: melden, nicht korrigieren** |
| ⚠️ | **`git status --porcelain` NACH dem letzten Commit** — nicht davor |
| ⚠️ | **Interpreter, falls überhaupt einer gebraucht wird: `trading-env/bin/python3`**, nie `/usr/bin/python3` |
| ⚠️ | **Abbruchkriterium:** Abbruch nur bei Fehlschlägen, **die den Gegenstand dieser Aufgabe betreffen** (T44.11). Ein vorbestehend roter Test ist keiner |
| ⛔ | **KEIN ZIP, nichts nach `~/Downloads`.** *Das überschreibt `ARBEITSWEISE.md` Abschnitt 2 und 7c, die noch ein ZIP verlangen — die Regel vom 19.09.2026 („Keine ZIPs, nichts nach `~/Downloads`; was fürs Projekt gebraucht wird, gehört ins Repo") ist die jüngere und gilt.* ⚠️ **Diesen Widerspruch bitte als Befund melden**, er gehört berichtigt |

---

## 2. ⭐⭐ Die Nummernregel — der wichtigste Teil dieses Auftrags

**Regel K2i:** *Ein Nachtrag nennt keine Nummer, die er nicht selbst gemessen
hat.*

⚠️⚠️ **Gemessen am 19.09.2026, 23:0x, in `docs/projektfuehrung/BACKLOG.md`
(951 Zeilen, Stand `fef279c`):**

| | gemessen | nächste freie |
|---|---|---|
| Blockbezeichner Abschnitt 2 | höchster **`2r`** (Überschrift Zeile 634) | **`2s`** |
| K-Nummern Abschnitt 4 | höchste **`K2k`** | **`K2l`** |
| Kettenzeilen Abschnitt 3 | höchste **`0,97`** | — |

### 2.1 Die Blocknummern tragen — in der richtigen Reihenfolge

`(n)` verlangt Block **`2t`**, *„nach Block 2s"*; `(o)` verlangt **`2u`**, `(p)`
verlangt **`2v`**. **Das ist richtig, sobald `(s)` den Block `2s` besetzt.**
⇒ **Die Einarbeitungsreihenfolge ist deshalb bindend** (Abschnitt 3).

### 2.2 ⚠️⚠️ Die K-Nummern tragen NICHT — und zwar keine einzige ab `K2r`

**Gemessen, welche K-Nummern die Nachträge nennen:**

| Nachtrag | genannt | Befund |
|---|---|---|
| `(n)` | `K2r` `K2s` `K2t` | ⚠️ **ohne Messung vergeben** |
| `(o)` | `K2r` `K2u` `K2v` `K2w` `K2x` | ⚠️ ohne Messung — **`K2r` kollidiert mit `(n)`** |
| `(p)` | `K2y` `K2z` | ⚠️ ohne Messung |
| `(q)` | `K2x` `K2y` `K2z` | ⚠️ **`K2x` kollidiert mit `(o)`, `K2y`/`K2z` mit `(p)`** |

⚠️ **Die Übergabe vom 19.09. nennt nur `(p)` als betroffen. Das ist zu eng —
betroffen sind `(n)`, `(o)`, `(p)` und `(q)`, mit drei Doppelbelegungen.**
Dieser Befund gehört in den Journal-Nachtrag.

> ⭐⭐ **Die Anweisung:** Behandle **jede K-Nummer ab `K2r` in (n), (o), (p) und
> (q) als Platzhalter ohne Geltung.** Vergib die K-Nummern **selbst**,
> fortlaufend ab der gemessenen freien, in der Einarbeitungsreihenfolge — und
> **schreibe zu jeder vergebenen Nummer den ursprünglich genannten Bezeichner in
> einen Vermerk**, nach dem Muster vom 19.09. Mittag:
>
> *„im Nachtrag (o) als `K2u` vorgeschlagen; `K2u` war zum Zeitpunkt der
> Einarbeitung nicht die nächste freie — vergeben als `K2<x>`, gemessen."*

⚠️ **`K2l`, `K2m` (Nachtrag `(s)`) und `K2n` (Nachtrag `(t)`) sind selbst
Vorschläge.** Auch sie werden gegen den gemessenen Stand geprüft, bevor sie
vergeben werden. Sie sind nur insofern besser, als sie **aus einer Messung
abgeleitet** wurden.

---

## 3. Die Einarbeitungsreihenfolge — bindend

| # | Nachtrag | Zielblock | Inhalt |
|---:|---|---|---|
| **1** | `(s)` | **`2s`** *(neu)* | TB-56b, die Registerberichtigung — T56b.1 bis T56b.8, dazu `K2l` (Reichweite der Geräteanbindung) und `K2m` (Fable-Abrufweg, verworfen). ⚠️ **`(s)` enthält am Ende eine Berichtigung zu seinem eigenen Punkt T56b.3 — es gilt die berichtigte Fassung** |
| **2** | `(t)` | **`2s`** *(derselbe Block)* | Fables Methodenantwort — T56b.9 bis T56b.16, dazu `K2n` (immer direkt weitermachen) und `K2o` (eine SOLL-Zahl ist gezaehlt, nicht geschaetzt) |
| **3** | `(n)` | **`2t`** | Epic **AF** — Autonome Strategie-Forschungspipeline |
| **4** | `(o)` | **`2u`** | Epic **MI** — KI-Marktverständnis und adaptive Allokation |
| **5** | `(p)` | **`2v`** | Epic **QR** — Alpha-Discovery-Labor |
| **6** | `(q)` + `(q_r_berichtigung)` | **`2w`** *(gemessen frei nach 2v)* | Epic **KG** — Kausalgraph. ⚠️ **Die Berichtigung wird ZUSAMMEN mit (q) eingearbeitet**, und die berichtigten Stellen tragen den Verweis darauf — an der Stelle des Fehlers, mit der Messung daneben |
| **7** | `(r)` + `(q_r_berichtigung)` | **`2x`** *(gemessen frei nach 2w)* | Epic **RT** — Rotes Team. ⚠️ Dieselbe Berichtigung betrifft auch `(r)` |

⚠️ **Prüfe vor jedem Schritt selbst nach, welcher Blockbezeichner frei ist** —
die Angaben oben sind aus dem Stand `b600a65` abgeleitet, und die Reihenfolge
verschiebt sie.

⭐ **Die Reihenfolge `AF → RT → QR → KG → MI` aus der Übergabe ist die
Reihenfolge der ARBEIT, nicht der Einarbeitung.** Eingearbeitet wird nach
Nachtragsbuchstaben, damit die Blockkette schliesst. **Die Arbeitsreihenfolge
gehört als eigener Satz in den Block von `(n)`**, mit der Begründung aus (r),
RT9: *RT braucht fast keine Vorbedingungen und macht AFs Ausgabe erst
glaubwürdig.*

---

## 4. Der Ersatz in `ARBEITSWEISE.md` — die einzige Stelle mit entfernten Zeilen

⚠️ **`docs/projektfuehrung/ARBEITSWEISE.md`, Zeilen 674 bis 743** (gemessen am
Stand `b600a65`: Abschnitt 10 beginnt in Zeile 674, Abschnitt 11 in Zeile 744;
die Datei hat 819 Zeilen).

**Ankertext Anfang, wörtlich:** `## 10. Die Sitzungsuebergabe`
**Ankertext Ende, wörtlich:** die Zeile **unmittelbar vor** `## 11. Änderungsverbote nennen ihren Zweck`

**Ersatztext, wörtlich zu übernehmen** (Quelle: `docs/projektfuehrung/UMZUG.md`,
Abschnitt 7 — von dort **zeichengleich** kopieren, nicht abtippen):

```markdown
## 10. Der Umzug in einen neuen Chat

⚠️⚠️ **Das Verfahren steht vollständig in
`docs/projektfuehrung/UMZUG.md`** (angelegt 19.09.2026). Es ersetzt die
frühere ZIP-und-Anhang-Übergabe, die durch zwei Anweisungen des Betreibers
vom 19.09.2026 überholt ist: *„Ich lese die Zipp und berichte nie"* und
die Weisung, ihn **frühzeitig** auf einen nötigen Umzug hinzuweisen.

**Die drei Sätze, die auch ohne das Dokument gelten:**

1. ⭐ **Die Übergabe wird laufend fortgeschrieben, nicht beim Umzug
   geschrieben.** Dann kostet ein überraschender Abbruch nichts.
2. ⚠️ **Nichts, was den Umzug überleben muss, steht in nur einem Träger —
   und niemals nur im Chatverlauf.** Träger sind: Erinnerung
   (Arbeitsweise), Projektablage (Stand), Repo (Belege).
   **`logs/auftraege/` ist kein Träger** — der Ordner ist gitignoriert.
3. ⚠️ **Nicht umziehen, während eine Sitzung läuft oder Arbeit
   uncommittet ist.**

**Und vor jedem Umzug unverändert:** der Betreiber wird gefragt, ob die
Arbeitsweise noch passt oder ergänzt werden soll — dazu wird jede in
diesem Chat vereinbarte Regel **gegen dieses Dokument geprüft, nicht
erinnert.**
```

⚠️ **Hier ist die zweite `numstat`-Spalte NICHT 0.** Erwartet werden **70
entfernte Zeilen** (674 bis 743 einschliesslich). **Ordne sie in deinem Bericht
dieser einen Ersetzung zu** — das ist der einzige zulässige Fall in dieser
Aufgabe.

⭐ **Und danach:** Die Fassung in der Projektablage muss gleich lauten. **Das
kann die Sitzung nicht; es geschieht in der Chat-Sitzung.** Bitte im Bericht
ausdrücklich daran erinnern.

---

## 5. Die zwei Querschnittsbefunde — zwei Punkte, nicht neun

⚠️ **Die fünf Sichtungsdurchgänge** (Kollision · Abhängigkeit · Widerspruch ·
Ausscheiden · Kette) sind **nicht vollständig gemacht**. Zwei Befunde stehen
fest und werden als **zwei Punkte mit Verweisen** eingetragen, nicht als neun
Einzelpunkte:

| | Befund | Form |
|---|---|---|
| **1** | ⭐ **Die Zerfallsfalle steckt in vier der fünf Konzepte** — „Edge Decay", „Relationship Decay", „Live Shadow Red Team", „Self-Healing Pool" | **ein** Punkt, mit Verweis auf die vier Stellen. ⚠️ **Mit dem Vermerk, dass Registerabschnitt 22.3 sie bereits entschieden hat:** Overlay-Kandidaten, keine Betriebsentscheidungen — und der „Self-Healing Pool" ist mit 6d **unvereinbar** |
| **2** | ⭐ **Das Register kommt in fünf von fünf Konzepten vor**, unter fünf Namen (Prediction Ledger, Data Lineage, Research Ledger, Hypothesis Registry, Versuchsregister) | **ein** Punkt, mit Verweis. ⚠️ **Mit dem Vermerk, dass Registerabschnitt 22.1 den Baustein inzwischen als allgemeine Prüfregel trägt** |

⚠️ **Die drei übrigen Durchgänge (Abhängigkeit, Ausscheiden, Kette) bleiben
offen** und werden als **offener Punkt** eingetragen, nicht stillschweigend
ausgelassen.

---

## 6. Die Nachweise, die diese Aufgabe schuldet

| # | Nachweis |
|---:|---|
| **1** | `git --no-optional-locks status --short` **vor** dem ersten Schreiben — erwartet: leer |
| **2** | `git diff --numstat` **je Datei**; zweite Spalte überall **0**, **ausser** `ARBEITSWEISE.md` mit **70** entfernten Zeilen, dieser einen Ersetzung zugeordnet |
| **3** | **Zeilenzahl von `BACKLOG.md` vorher und nachher.** Vorher gemessen: **951** |
| **4** | ⭐ **Der Nummernnachweis:** eine Tabelle *„ursprünglich genannt → vergeben, gemessen"* für **jede** umgeschriebene Nummer |
| **5** | **Gegenprobe auf Kollisionen:** nach der Einarbeitung kommt **jeder** Blockbezeichner und **jede** K-Nummer in `BACKLOG.md` **genau einmal** vor. Zähle es, behaupte es nicht |
| **6** | `git status --porcelain` **nach** dem letzten Commit |
| **7** | **Nichts ausserhalb `docs/` geändert** — `git diff --name-only <Ausgangscommit>..HEAD` und die Zusicherung, dass jeder Pfad mit `docs/` beginnt |

**Ablage der Ergebnisse:** `docs/ERGEBNIS_TB-59_backlog_einarbeitung.md` im
Repo, committet. ⛔ **Kein Archiv, kein `~/Downloads`.**

**Journal:** ein Nachtrag als `docs/projektfuehrung/nachtraege/JOURNAL_NACHTRAG_2026-09-19g.md`
*(gemessen: höchster Journal-Buchstabe ist `(f)`)* — mit dem Nummernbefund aus
Abschnitt 2.2 als eigenem Block, weil er die Übergabe korrigiert.

**Am Ende des Ergebnisdokuments: „In einfacher Sprache"** — was wir wissen
wollten, was herauskam, warum, was das bedeutet.

---

## 7. Was diese Aufgabe ausdrücklich NICHT tut

| | |
|---|---|
| ⛔ | **Keine der fünf Epic-Konzepte bewerten oder umsetzen.** Sie werden **eingetragen**, mehr nicht |
| ⛔ | **Nichts unter `research/`, `shared/`, `strategies/`, `broker/`, `config/`, `data/`** |
| ⛔ | **Kein Registertext.** Das Register ist mit Abschnitt 22 auf Stand |
| ⛔ | **Kein signierter Tag, kein Zeitanker, kein Selektionslauf** |
| ⚠️ | **Die drei offenen Sichtungsdurchgänge werden nicht nachgeholt**, sondern als offener Punkt eingetragen |

---

## In einfacher Sprache

**Was zu tun ist:** Acht Notizen, die in den letzten Tagen entstanden sind,
gehören in die grosse Aufgabenliste einsortiert — fünf davon beschreiben
Forschungsideen, die der Betreiber eingereicht hat, drei halten fest, was heute
Abend entschieden wurde.

**Worauf es dabei ankommt:** Jede Notiz schlägt Nummern für ihre Einträge vor.
**Diese Nummern sind grösstenteils geraten**, und drei davon sind doppelt
vergeben — es gäbe also zwei Einträge mit derselben Nummer, und jeder spätere
Verweis darauf träfe die falsche Stelle. **Deshalb werden alle Nummern neu
vergeben, nachgezählt statt übernommen, und zu jeder wird notiert, was
ursprünglich dastand.**

**Und eine Stelle wird wirklich ersetzt:** In der Arbeitsanweisung steht noch
ein Kapitel über Chatumzüge, das überholt ist. Es wird durch einen kurzen
Verweis ersetzt. Das ist die einzige Stelle in dieser Aufgabe, an der Zeilen
verschwinden dürfen — überall sonst wird nur hinzugefügt, und das wird
nachgewiesen.

---

## 8. Nachgetragen: ein achter Nachtrag

⚠️ **Nach dem Schreiben dieses Auftrags ist `(u)` entstanden** —
`docs/projektfuehrung/nachtraege/BACKLOG_NACHTRAG_2026-09-19u.md`, die Befunde
aus der Leseprüfung T46.1 (Beleg: `docs/ERGEBNIS_T46-1_ausstiegspfade.md`).

**Er wird als Schritt 2b eingearbeitet, unmittelbar nach `(t)`, in denselben
Block `2s`** — die Befunde stammen aus derselben Sitzung desselben Abends.
Die Punkte heissen `T46.1a` bis `T46.1d` und kollidieren mit nichts; sie
brauchen **keine** K-Nummer.

⚠️ **Die Reihenfolge in Abschnitt 3 verschiebt sich dadurch nicht** — `(n)`
bleibt Block `2t`.
