# Backlog-Nachtrag (q) — 19.09.2026

**Quelle:** das vierte Konzeptdokument des Betreibers,
*„Market Causal Graph & Market Physics Engine"*, wörtlich abgelegt als
`docs/vorlagen/vorlage_kausalgraph_2026-09-19.md` (23 292 Bytes, byteidentisch
zur eingereichten Fassung — `cmp` bestätigt).

⚠️⚠️ **Dieser Nachtrag nennt keine konkrete Nummer.** Nicht aus Vorsicht,
sondern weil ich es viermal falsch gemacht habe. Jede Einordnung unten sagt
**wohin** etwas gehört und **warum**; die Nummer vergibt die Sitzung, nachdem
sie den Zielstand gemessen hat (Regel **K2i**).

---

## Vorbemerkung 1 — ⚠️ Vier Nummernkollisionen, alle meine, und die vierte ist die jüngste

**Gemessen in `docs/projektfuehrung/BACKLOG.md` am 19.09.2026, 20:47 Ortszeit,
Stand `d66a2ce`:**

| | gemessen |
|---|---|
| höchster Blockbezeichner in Abschnitt 2 | **`2r`** (TB-54) |
| höchste K-Nummer in Abschnitt 4 | **`K2k`** |
| höchste Kettenzeile in Abschnitt 3 | **`0,97`** |

**Daraus folgt für die noch uneingearbeiteten Nachträge:**

| Nachtrag | nennt selbst | frei wäre, in Einarbeitungsfolge |
|---|---|---|
| (n) — Epic AF | Block 2t | **`2s`** |
| (o) — Epic MI | Block 2u | **`2t`** |
| (p) — Epic QR | **Block 2v**, `K2y`, `K2z`, `K3a`, `K3b` | **`2u`**; K-Nummern ab **`K2l`** |
| **(q) — Epic KG** | **nichts** | die Sitzung misst und vergibt |

⚠️ **`K2y` und `K2z` in (p) überspringen `K2l` bis `K2x`.** Keine Kollision,
aber erfundene Nummern in einem Dokument, dessen Zweck Nachvollziehbarkeit ist.

⇒ **Aufgabe für die einarbeitende Sitzung:** Blockbezeichner und K-Nummern in
(n), (o), (p) beim Einfügen **auf die gemessene nächste freie Nummer
umschreiben** und die ursprünglich genannte im Vermerk nennen — genau wie bei
`0,88` am Mittag (*„im Nachtrag (h) als 0,87 vergeben; 0,87 war bereits
belegt"*). ⭐ **Nicht stillschweigend korrigieren.**

---

## Vorbemerkung 2 — wo diese vier Schichten stehen

**Alle vier Konzepte (AF, MI, QR, KG) liegen hinter dem signierten Tag.**
Keines davon ist der nächste Schritt. Sie sind der Grund, warum der jetzige
Schritt sich lohnt — und der jetzige Schritt ist die Selektion mit einer
Methode, die hält.

⚠️ **Das ist keine Formalie.** Alle vier Konzepte setzen dieselbe Sache voraus:
eine funktionierende, registrierte Validierungskette. Wer sie vorher baut, baut
eine Maschine, die sehr schnell sehr viele unüberprüfbare Aussagen erzeugt.

---

# Block ⟨nächster freier⟩ — Epic KG: Market Causal Graph & Market Physics Engine

**Einordnung:** eigenes Epic in Abschnitt 7 (Architektur, offen), hinter AF, QR
und vor MI. Begründung unter **KG9**.

---

## KG0 — Was das Dokument richtig macht, und es ist mehr als bei den drei anderen

| Abschnitt | |
|---|---|
| **§18 „Falsification First"** | ⭐⭐ **Der beste Abschnitt aller vier Konzepte.** *„Versuche zuerst, die gefundene Beziehung zu zerstören."* Das ist die Methode dieses Projekts, in einem Satz, aus der Feder des Betreibers |
| **§17 Prediction vs Causality** | ⭐ Die Trennung ist richtig und wird fast überall verwischt |
| **§20 / §28** | ⭐ *„AI darf keine direkte Kapitalentscheidung treffen"* — und die Risk Engine bleibt unabhängig. Dasselbe Prinzip wie „kein Agent löst einen Trade aus" |
| **§1** | ⭐ *„Das System darf solche Beziehungen nicht als kausal betrachten, nur weil sie korrelieren"* — der Satz steht **vor** dem Entwurf, nicht als Fußnote danach |
| **§27** | ⭐ *„Keine subjektive ‚Profitability Score'-Bewertung erfinden"* — genau die Grenze, die ich heute Mittag selbst gezogen habe |

⚠️ **Und genau deshalb ist dieses Konzept das gefährlichste der vier.** Nicht
das schwächste — das gefährlichste. Es benennt jede Falle korrekt und entwirft
dann eine Maschine, deren Grundbetrieb das Hineinlaufen ist.

---

## KG1 — ⚠️⚠️ Die Zahl der geprüften Beziehungen muss VOR dem Lauf registriert werden

**§19 verlangt, `number_of_relationships_tested` zu *tracken*.** Das ist eine
Messung **nach** dem Lauf.

**Rechnung an der Struktur des Entwurfs selbst:** §3 nennt **22 Knotenarten**
und **10 Kantenarten**. Werden daraus nur 50 konkrete Knoten, 20 Verzögerungen
(§4) und 4 Regime (§12) gebildet, sind das

```
50 × 49 × 20 × 4  =  196 000 prüfbare Beziehungen
```

Bei α = 0,05 liefern **rund 9 800 davon ein „signifikantes" Ergebnis, wenn
überhaupt kein Zusammenhang existiert.**

⚠️ **FDR-Kontrolle rettet das nicht**, solange die Zahl der Tests nicht vorher
feststeht. Wer 196 000 Tests rechnet, 400 „Treffer" behält und dann FDR über
diese 400 rechnet, hat den Nenner selbst gewählt — dieselbe Klasse Fehler wie
eine Selektion ohne registriertes N.

⇒ ⭐⭐ **Verfahren B, angewandt auf den Graphen:** Bevor ein Lauf beginnt, wird
registriert: welche Knoten, welche Kantenarten, welche Verzögerungen, welche
Regime, **und damit N**. Der Lauf darf N nicht verändern. Ein zweiter
Knotensatz ist ein **neuer Lauf**, mit eigener Registrierung — wortgleich zu
*„Ein zweiter Snapshot ist ein neuer Lauf."*

---

## KG2 — ⚠️⚠️ §18 ist eine Liste von Prüfungen. Eine Liste von Prüfungen ist keine Falsifikation

**§18 nennt 15 Prüfungen** — look-ahead, leakage, Zeitstempel, Survivorship,
Multiple Testing, Kosten, Slippage, Stichprobengröße, OOS-Stabilität und
weitere. ⭐ Die Liste ist gut.

⚠️ **Sie sagt nicht, welches Ergebnis die Beziehung verwirft.** Werden alle 15
gerechnet und niemand hat vorher gesagt, was „durchgefallen" heißt, überlebt
die Beziehung jedes Ergebnis — sie wird dann *eingeordnet*, nicht *geprüft*.

⇒ **Jede Beziehung braucht vor dem ersten Test ein maschinell prüfbares
Abbruchkriterium**, das die Sache benennt und nicht ihren Stellvertreter
(die Regel aus TB-55b). Und es muss **beißen können**: Prüfprinzip **B1** —
eine Probe, die nichts verwerfen kann, ist keine Probe. Praktisch: an einer
absichtlich zerstörten Beziehung (Zeitreihe permutiert) muss das Kriterium
auslösen, bevor es auf echte Daten darf.

---

## KG3 — ⚠️⚠️ `confidence` ist das gefährlichste Feld des ganzen Dokuments

**§3 führt im Graph-Eintrag ein Feld `confidence`.** Ohne Einheit, ohne
Schätzer, ohne Nullmodell.

⚠️ **Eine Zahl zwischen 0 und 1 neben dem Wort „Hypothese" wird als
Wahrscheinlichkeit gelesen, dass die Hypothese wahr ist.** Das ist sie nicht
und kann sie nicht sein. Nach zwei Wochen steht in Berichten „confidence 0,82"
und niemand weiß mehr, ob das ein p-Wert, ein Anteil, ein LLM-Urteil oder eine
Mischung ist.

⇒ **Zwei zulässige Wege, kein dritter:**
1. Das Feld nennt seinen **Schätzer** und sein **Nullmodell** im Namen
   (`oos_trefferquote_gegen_permutation`), oder
2. es gibt das Feld nicht.

⭐ **Dasselbe gilt für `stability_score` (§3) — und `confidence` ist nicht der
Einzelfall, sondern das Muster:** ein Name, der ein Urteil ausdrückt, ohne
seine Messung mitzuführen. Regel aus dem Register: **jede Zahl trägt ihre
Herkunft.**

---

## KG4 — ⚠️ §17 ist richtig, und §3 widerlegt es

**§17 verlangt:** prädiktive Beziehung und kausale Hypothese *„müssen separat
gespeichert werden"*.

**§3 speichert beide im selben Satz** — ein Eintrag mit `hypothesis`,
`relationship_type`, `confidence`, `observation_count`, `statistical_tests`,
`out_of_sample_results`.

⚠️ **`observation_count` neben `confidence` in einem Satz ist genau der
Mechanismus, der Korrelation still zu Kausalität befördert:** je öfter
beobachtet, desto höher die Zuversicht, und irgendwann liest jemand die
Kantenart `CAUSES`, wo `CO-MOVES_WITH` gemessen wurde.

⇒ **Zwei Kantenklassen, physisch getrennt, und keine Beförderung durch
Beobachtungszahl.** Eine Kante wechselt die Klasse nur durch ein Verfahren, das
vorher registriert wurde — nicht durch Anhäufung. ⭐ Praktisch heißt das: die
Kantenarten aus §3 werden in zwei Listen aufgeteilt (`CO-MOVES_WITH`,
`PRECEDES`, `CORRELATES_WITH`, `LEADS`, `FOLLOWS` → beobachtend;
`AMPLIFIES`, `SUPPRESSES`, `TRANSMITS_TO`, `REACTS_TO` → behauptend), und die
behauptenden tragen ein Pflichtfeld „Verfahren, das sie dorthin gebracht hat".

---

## KG5 — ⭐⭐ Der harte Befund: Lead/Lag ist auf den vorhandenen Daten nicht messbar

**Das ist der wichtigste Punkt dieses Nachtrags, und er ist gemessen, nicht
überlegt.**

§4 nennt als Beispiel *„Asset A → 2 min → Asset B"*. §5 verlangt
`reaction_30s`. §7 baut auf `Liquidity ↓ → Price Impact ↑ → Volatility ↑ →
Liquidations ↑`.

**Was das Projekt heute tatsächlich hat, gemessen:**

| | |
|---|---|
| Kursdateien | **223**, Namensform `{symbol}_{INTERVAL}.csv` |
| feinste vorhandene Auflösung | **1 Stunde** (`MIN_HISTORY_HOURS = 17520` bei `elliott_wave`); alle übrigen acht Bots rechnen auf **Tagesdaten** (`MIN_HISTORY_DAYS`) |
| Lückenhaftigkeit auch dort | BTCUSDT: **79 461 Kerzen, 147 fehlend**; lückenlos erst ab 2019-08-20 bei Handelsbeginn 2017-08-17 (TB-56 Teil A, `docs/belege/TB-56/teil_a_messung.txt`) |
| Orderbuch, Ticks, Funding, Open Interest, Liquidationen, Optionen | **nicht vorhanden** |

⇒ ⚠️⚠️ **Die kleinste auflösbare Verzögerung ist eine Stunde.** Damit sind
nicht messbar: §4 (2-Minuten-Beispiel), §5 (`reaction_30s`, `reaction_1m`,
`reaction_5m`), §7 vollständig (Liquidity-, Volatility-, Positioning-Feedback
sind Mikrostruktur), §4s *execution latency / spread / slippage / market
impact*.

⇒ **§26 Punkt 4 („Lead/Lag Discovery") ist im MVP keine Aufgabe, sondern eine
gesperrte Abhängigkeit.** ⭐ **Und das ist eine gute Nachricht, nicht eine
schlechte:** Es schrumpft das MVP auf das, was mit Tages- und Stundendaten
ehrlich untersuchbar ist — Ereignisreaktionen über Stunden bis Tage und
Cross-Asset-Übertragung. Das ist immer noch ein echtes Forschungsprogramm.

⚠️ **Die Falle, die es zu vermeiden gilt:** ein Lead/Lag auf Tagesdaten finden,
es als Mechanismus lesen und dabei nicht sagen, dass die Auflösung 24 Stunden
ist. **Jede Beziehung trägt ihre Auflösung als Pflichtfeld.**

---

## KG6 — ⚠️ §8 verspricht etwas, das mit diesen Mitteln niemand einlösen kann

**§8 sucht selbstverstärkende Schleifen `A → B → C → A`.** §8 sagt selbst
*„Nicht jede gefundene Schleife ist real"*. ⭐ Richtig — die ehrliche Fassung
ist strenger:

> ⚠️⚠️ **Keine in Zeitreihendaten gefundene Schleife kann mit diesen Mitteln
> als real gezeigt werden.** `A → B → C → A` ist von *einem gemeinsamen Treiber
> plus Autokorrelation* nicht unterscheidbar, bei keiner Stichprobengröße, ohne
> einen Eingriff. **In Marktdaten gibt es keine Eingriffe.**

⇒ **Was messbar ist, und das ist nicht wenig:** ob die von der Schleife
implizierte **bedingte Struktur** out-of-sample hält — und ob sie hält, wenn man
den vermuteten gemeinsamen Treiber herauspartialisiert. Das Epic muss das so
formulieren. ⭐ **Sonst verspricht es Mechanismus und liefert Beschreibung** —
und in einem Jahr liest jemand „validierter Feedback Loop" und glaubt, es gäbe
einen Beweis.

---

## KG7 — ⚠️ §10 und §6 sind dasselbe Verfahren, und es hat ein Freiheitsgrade-Problem

**§10 fragt:** *„Wäre die beobachtete Marktbewegung auch ohne das
identifizierte Event wahrscheinlich gewesen?"*

⚠️ **Mit einer realisierten Geschichte und ohne Kontrollgruppe ist ein
Kontrafaktum nicht messbar.** Messbar ist eine **Schätzung über eine
vergleichbare Stichprobe** — und die Auswahl dieser Stichprobe ist genau §6
(*Historical Event Similarity*).

⇒ **§6 und §10 sind ein Epic-Bestandteil, nicht zwei.** Und: ⭐⭐ **das
Ähnlichkeitsmaß muss vor seiner Anwendung registriert werden.** §6 nennt sieben
Dimensionen (Event, Surprise, Regime, Volatilität, Liquidität, Positionierung,
Cross-Asset-Zustand) ohne Gewichtung. Wer die Gewichtung nach dem ersten Blick
auf das Ergebnis wählt, hat die Vergleichsstichprobe so gewählt, dass sie die
Antwort liefert. **Das ist Selektion, nur an anderer Stelle** — und Fables
Drei-Kategorien-Regel gilt: die Grenze ist nicht die Zeit, sondern die Quelle
des Grundes.

---

## KG8 — ⭐ Die Überschneidung ist größer, als §29 C vermutet: die Hälfte ist schon da

**§29 C fragt nach Überschneidungen mit Strategy Factory, Market Intelligence
und Alpha Discovery. Die Antwort, Abschnitt für Abschnitt:**

| Abschnitt in (q) | ist bereits | |
|---|---|---|
| **§9** Causal Hypothesis Engine | **QR** — Hypothesis Registry | ⚠️ derselbe Gegenstand, anderes Substantiv |
| **§14** Relationship Lifecycle | **QR** Edge Decay + **AF** Strategy Registry | derselbe Lebenszyklus |
| **§15** Relationship Decay | **QR4** — und trägt **dieselbe Falle**: Abschwächung ist auf einem Random Walk normal | |
| **§19** Multiple Testing / FDR | **QR** — Multiple Testing | |
| **§24** Data Lineage | **QR2** Prediction Ledger — ⭐⭐ **und das ist das Register, angewandt je Hypothese** | `data_version`, `prompt_version`, `research_run_id` sind Registerfelder |
| **§25** Research Cost | **QR5** | |
| **§16** Research Council | **AF** Adversarial Review + **MI** Agents | |
| **§20 / §28** Governance | **AF/MI/QR** — und heute schon Projektregel | |

**Wirklich neu in (q), und nur das:**

| | |
|---|---|
| **§3** | der Graph als **persistente Datenstruktur** — die einzige echte Architekturneuheit |
| **§4** | Lead/Lag-Entdeckung — ⚠️ **datengesperrt, KG5** |
| **§5** | Ereignisreaktions-Datenbank — ⭐ **ohne Vorbedingung baubar** |
| **§6 + §10** | Ähnlichkeit und Kontrafaktum — ein Bestandteil, KG7 |
| **§8** | Schleifen — ⚠️ **Versprechen umformulieren, KG6** |

⇒ ⭐⭐ **Epic KG ist etwa halb so groß, wie es aussieht** — und die eigenständige
Hälfte hängt an Daten, die es nicht gibt. **Das ist der nützlichste Befund
dieses Nachtrags für die Planung:** nicht „zu viel Arbeit", sondern „ein großer
Teil ist schon eingeplant, und der Rest ist kleiner und ehrlicher, als das
Dokument vermutet".

---

## KG9 — Reihenfolge, und der eine Satz, der in §30 fehlt

**Reihenfolge der vier Schichten, begründet und nicht nach Reiz:**

```
AF  →  QR  →  KG  →  MI
```

| | |
|---|---|
| **AF zuerst** | trägt die Validierungskette und funktioniert mit handgeschriebenen Hypothesen — **ohne sie ist jede andere Schicht eine Hypothesenschleuder ohne Prüfer** |
| **QR danach** | liefert Ledger, FDR und Kalibrierung, die KG zwingend braucht (KG1, KG8) |
| **KG danach** | erzeugt Beziehungen, die MIs Regime-Engine benutzen kann; erzeugt sie vorher, fehlt der Prüfer |
| **MI zuletzt** | braucht einen Pool und einen Grund, zwischen Strategien umzuschalten |

**Und §30, der Schlussabschnitt, ist der Loop dieses Projekts mit mehr
Substantiven:**

```
OBSERVE → DETECT → CONNECT → HYPOTHESIZE → FALSIFY → VALIDATE → …
```

⚠️⚠️ **Dazwischen fehlt ein Schritt, und es ist derselbe, der diesem Projekt
zwei Wochen gekostet hat:**

```
HYPOTHESIZE  →  ⭐ REGISTER  →  FALSIFY
```

⭐ **Ohne REGISTER hat FALSIFY nichts Festgelegtes, an dem es scheitern
könnte.** Das ist der einzige Satz, den ich dem Dokument hinzufügen würde —
und mit ihm stimmt sein Schlussabschnitt.

---

## Merkmale (Features) — KG-F0 bis KG-F12

| | Merkmal | Vorbedingung |
|---|---|---|
| **F0** | **Registrierung eines Graphenlaufs**: Knotensatz, Kantenarten, Verzögerungen, Regime, **N** — vor dem Lauf, inhaltsadressiert | — |
| **F1** | **Relationship Registry** mit **zwei Kantenklassen** (beobachtend / behauptend), keine Beförderung durch Beobachtungszahl | F0 |
| **F2** | **Pflichtfeld Auflösung** je Beziehung (1 h / 1 d), und ein Feld, das die feinste im Datenbestand vorhandene Auflösung nennt | — |
| **F3** | **Abbruchkriterium je Beziehung**, maschinell prüfbar, vor dem ersten Test, an permutierten Daten auf Bissfestigkeit geprüft (B1) | F0 |
| **F4** | **Ereignisdatenbank** — Ereignisart, Zeitpunkt, Überraschung, Marktzustand; ⭐ mit Tagesdaten baubar | — |
| **F5** | **Ereignisreaktion** auf den tatsächlich vorhandenen Horizonten: **1 h, 4 h, 1 d, 1 w** — ⚠️ **keine 30-s-, 1-min-, 5-min-Felder**, auch nicht leer | F2, F4 |
| **F6** | **Ähnlichkeitsmaß**, vor seiner ersten Anwendung registriert, samt Gewichtung der sieben Dimensionen | F0, F4 |
| **F7** | **Vergleichsstichproben-Schätzung** statt „Kontrafaktum" — mit ausgewiesener Stichprobengröße und Ausfallhäufigkeit | F6 |
| **F8** | **FDR über registriertes N**, nicht über die Treffer | F0, **QR** |
| **F9** | **Herkunft je Beziehung** (`data_version`, `research_run_id`, Commit, Snapshot-Name) — ⭐ dieselben Felder wie im Register | **QR2** |
| **F10** | **Zerfallsüberwachung**, die zwischen „Abschwächung" und „normaler Schwankung" unterscheiden kann — ⚠️ sonst QR4s Falle | QR4 |
| **F11** | **Alternativerklärungen als Pflichtfeld**, nicht als Bericht: jede behauptende Kante nennt mindestens eine geprüfte Alternative | F1 |
| **F12** | **Kosten je Beziehung** — LLM, Compute, Daten; gemessen ab dem ersten Lauf | QR5 |

⚠️ **Nicht in diesem Epic und bis auf Weiteres gesperrt:** Lead/Lag unter einer
Stunde, Mikrostruktur-Feedback (§7 vollständig), Orderbuch-, Options- und
On-Chain-Auswertung, `execution latency` / `slippage` / `market impact` als
gemessene Größen. **Grund: KG5.**

---

## Nicht verhandelbare Abhängigkeiten

1. ⚠️⚠️ **Der signierte Tag.** Alle vier Schichten liegen dahinter.
2. ⚠️ **AF und QR vor KG** (KG9). KG ohne QRs Ledger und FDR ist eine
   Hypothesenschleuder.
3. ⚠️ **F0 vor jedem Lauf.** Ein Graphenlauf ohne registriertes N ist nicht
   auswertbar — nicht „schlechter auswertbar", **nicht auswertbar**.
4. ⚠️ **F2 vor F4/F5.** Wer Reaktionsfelder anlegt, die die Daten nicht
   hergeben, erzeugt Felder, die später mit irgendetwas gefüllt werden.
5. **Tick- oder Orderbuchdaten** sind Vorbedingung für §4 und §7 — und ihre
   Beschaffung ist ein eigenes Vorhaben mit eigenen Kosten, nicht ein Unterpunkt.

---

## Risiken, nach Schadenshöhe

| | Risiko | |
|---|---|---|
| **1** | ⚠️⚠️ **Falsche Entdeckungen in großer Zahl** — 196 000 Tests, ~9 800 Scheintreffer bei reinem Rauschen (KG1) | **F0 + F8** |
| **2** | ⚠️⚠️ **Kausalsprache ohne Kausalnachweis** — `AMPLIFIES`, `CAUSES`, „validierter Feedback Loop" (KG4, KG6) | **F1 + F11** |
| **3** | ⚠️⚠️ **Auflösungslüge** — ein Tagesdaten-Zusammenhang als Mikrostruktur-Mechanismus gelesen (KG5) | **F2** |
| **4** | ⚠️ **`confidence` als Wahrheitswahrscheinlichkeit gelesen** (KG3) | Feld streichen oder benennen |
| **5** | ⚠️ **Stichprobenwahl nach Ergebnis** in §6/§10 (KG7) | **F6 vor Anwendung registriert** |
| **6** | ⚠️ **LLM-Kostenexplosion** — sechs Research-Agents (§16) auf einem Graphen mit sechsstelliger Kantenzahl | **F12 ab Tag 1** |
| **7** | ⚠️ **Zeitstempelqualität** — §4 nennt sie als achte von acht Erwägungen; bei Verzögerungsforschung ist sie **die** Messung | **F2** |

---

## MVP — und es hat eine Ausgabezahl, nicht zehn

**Nicht** §26s zehn Punkte. Die kleinste Fassung, die eine echte Frage
beantwortet:

| | |
|---|---|
| Datenquellen | die **vorhandenen 223 Kursdateien**, keine neue Quelle |
| Ereignisse | **eine** Klasse, mit sicher datierbarem Zeitpunkt (z. B. FOMC-Termine) |
| Horizonte | **1 d und 1 w** — die Auflösung, die die Daten hergeben |
| Beziehungen | **vorher registriert**, zweistellige Zahl, nicht sechsstellig |
| Nullmodell | **permutierte Ereigniszeitpunkte**, gleiche Zahl, gleiche Pipeline |

**Die eine Zahl, die das MVP ausgibt:**

> ⭐⭐ **Wie viele der registrierten Beziehungen überleben out-of-sample, und wie
> viele überleben es bei zufällig verschobenen Ereigniszeitpunkten?**

⚠️ **Sind die beiden Zahlen gleich, ist die Maschine wertlos — und das ist ein
Ergebnis, kein Scheitern.** Es kostet dann eine Woche statt eines Jahres.

⭐ **Das MVP beantwortet ausdrücklich nicht:** ob sich damit Geld verdienen
lässt.

---

## Ergänzungen zu Abschnitt 4 — ⟨nächste freie Nummern, von der Sitzung gemessen⟩

Vier Arbeitsregeln, die aus diesem Konzept folgen und über es hinaus gelten.
⚠️ **Nummern werden beim Einfügen gemessen; die höchste heute vergebene ist
`K2k`.**

| Regel | |
|---|---|
| **⟨a⟩** | **Eine Zahl in einem Datensatz trägt ihren Schätzer im Namen oder sie existiert nicht.** `confidence` und `stability_score` sind die Anlassfälle; die Regel gilt für jedes Feld, das ein Urteil ausdrückt |
| **⟨b⟩** | **Jede Messung trägt ihre Auflösung.** Wer eine Verzögerung nennt, nennt die feinste im Datenbestand vorhandene Zeitauflösung im selben Satz |
| **⟨c⟩** | **Die Zahl der Tests wird vor dem Lauf registriert, nicht nach dem Lauf gezählt.** Gilt für Selektionen, Hypothesen und Graphenkanten gleichermaßen |
| **⟨d⟩** | **Kausalsprache ist ein Pflichtfeld, kein Wortschatz.** Eine Kante oder ein Satz, der Wirkung behauptet (`verstärkt`, `verursacht`, `überträgt`), nennt das Verfahren, das ihn dorthin gebracht hat — oder er wird beschreibend formuliert |

⭐ **⟨d⟩ ist die allgemeine Fassung eines Fehlers, den dieses Projekt schon
gemacht hat:** *„Die erste Falte ist 2019, und die Schranke dafür ist das
Register, nicht die Datenlage"* (Abschnitt 15.6, Punkt 2) — ein
Ursachensatz ohne Messung dahinter. **TB-56 Teil A hat heute gemessen, dass er
falsch ist.**

---

## In einfacher Sprache

**Das vierte Konzept will erforschen, welche Marktmechanismen welche Bewegungen
nach sich ziehen** — ein Netz aus Ursachen und Wirkungen, das laufend geprüft
und bei Bedarf verworfen wird.

⭐ **Es ist das methodisch aufmerksamste der vier.** Es warnt selbst davor,
Korrelation für Ursache zu nehmen, verlangt, jede gefundene Beziehung zuerst
zerstören zu wollen, und verbietet der KI ausdrücklich, über Geld zu
entscheiden. Der Satz *„Versuche zuerst, die gefundene Beziehung zu zerstören"*
ist der beste in allen vier Einreichungen.

⚠️ **Und genau deshalb muss ich beim Rest deutlich werden. Drei Dinge:**

**Erstens: die Menge.** Aus den vorgeschlagenen Bausteinen entstehen leicht
zweihunderttausend prüfbare Beziehungen. Von denen sehen etwa zehntausend
„bedeutsam" aus, **auch wenn überhaupt kein Zusammenhang existiert**. Dagegen
hilft nur, die Zahl der Prüfungen **vorher** festzuschreiben — dieselbe Regel,
die wir gerade für die Bot-Auswahl aufgeschrieben haben.

**Zweitens: die Daten.** Das Konzept möchte Beziehungen im Zwei-Minuten- und
Halb-Minuten-Bereich untersuchen. **Wir haben Stunden- und Tagesdaten.** Damit
ist die feinste messbare Verzögerung eine Stunde, und ein ganzer Zweig des
Konzepts — Liquidität, Liquidationen, Orderfluss — ist mit dem heutigen
Datenbestand nicht untersuchbar. ⭐ **Das ist keine schlechte Nachricht**: es
macht den ersten Schritt kleiner und ehrlich. Ereignisreaktionen über Stunden
und Tage lassen sich untersuchen, und das ist schon ein echtes Programm.

**Drittens: die Hälfte ist schon geplant.** Hypothesenregister,
Zerfallsüberwachung, Mehrfachtest-Korrektur, Herkunftsnachweis und
Kostenmessung stehen bereits im dritten Konzept, nur mit anderen Wörtern.
Wirklich neu sind das Netz selbst und die Ereignisdatenbank.

**Ein einziger Satz fehlt dem Dokument**, und er steht in seinem letzten
Abschnitt: zwischen *Hypothese aufstellen* und *widerlegen versuchen* gehört
**eintragen**. Ohne das Eintragen gibt es nichts Festes, an dem das Widerlegen
scheitern könnte.

**Die Reihenfolge der vier Schichten:** erst die Validierungskette, dann das
Hypothesenlabor, dann dieses Netz, dann die Umschaltung zwischen Strategien.
**Und alle vier erst nach dem signierten Tag** — sie sind nicht der nächste
Schritt, sie sind der Grund, warum der jetzige sich lohnt.
