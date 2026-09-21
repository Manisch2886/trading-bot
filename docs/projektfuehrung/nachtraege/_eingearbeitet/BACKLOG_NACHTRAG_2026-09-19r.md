# Backlog-Nachtrag (r) — 19.09.2026

**Quelle:** das fünfte Konzeptdokument des Betreibers,
*„Autonomous Adversarial Trading Lab / Strategy Red Team"*, wörtlich abgelegt als
`docs/vorlagen/vorlage_rotes_team_2026-09-19.md` (19 599 Bytes, `cmp` gegen die
Einreichung: byteidentisch).

⚠️ **Keine konkrete Nummer in diesem Nachtrag** (Regel **K2i**). Gemessener
Stand `d66a2ce`: höchster Block **`2r`**, höchste K-Nummer **`K2k`**, höchste
Kettenzeile **`0,97`**.

---

## Vorbemerkung — dieses Konzept ist von den fünf das einzige, das wir heute schon teilweise rechnen könnten

**Und genau das ist seine Gefahr, nicht seine Stärke.**

⭐ **§35 ist die Arbeitsweise dieses Projekts in einem Satz:**

> *„Don't ask whether a strategy works. Ask how hard it is to break."*

**Das tut das Projekt seit zwei Wochen — an seinen eigenen Nachweisen.** Heute,
19.09., hat TB-56 die Faltenschranke künstlich wieder eingesetzt, um zu belegen,
dass die Probe beißt: in einer Wegwerf-Kopie von `research/vorregistrierung`
begannen unmutiert `2017/2018`, mutiert **alle vier 2019**
(`docs/belege/TB-56/nachweise_1_3_4_8.txt`, Nachweis 4b). ⭐⭐ **Das ist ein
Red-Team-Angriff auf einen Beweis.** Die Sperrklinken, die Mutationsproben, die
Abbruchkriterien — alles Angriffe auf eigene Behauptungen.

⇒ ⭐ **Was fehlt, ist nicht die Haltung, sondern ihr Gegenstand: Das Projekt
greift seine Beweise an, nicht seine Strategien.** Genau diese Lücke füllt das
Konzept, und es füllt sie mit Mitteln, die überwiegend schon da sind.

---

# Block ⟨nächster freier⟩ — Epic RT: Autonomous Adversarial Trading Lab

**Einordnung:** eigenes Epic in Abschnitt 7, **direkt hinter AF und vor QR** —
Begründung unter **RT9**, und das ist eine Änderung meiner eigenen Empfehlung
von vor einer Stunde.

---

## RT0 — Was das Konzept richtig macht

| | |
|---|---|
| **§35** | ⭐⭐ die Umkehrung der Frage; die beste Formulierung in allen fünf Einreichungen |
| **§30** | ⭐⭐ *„Eine Verbesserung darf nur akzeptiert werden, wenn sie eine identifizierte Schwäche adressiert"* — damit ist Reparatur an eine **vorher benannte** Schwäche gebunden. Das ist Fables Drei-Kategorien-Regel, auf Strategien angewandt |
| **§28** | ⭐⭐ **den Angreifer bewerten.** Die beste Governance-Idee der fünf Konzepte — und sie fehlt in den anderen vier |
| **§10** | ⭐ *„Synthetic data darf nicht als Beweis für reale Profitabilität verwendet werden"* — richtig, und unvollständig (RT6) |
| **§9** | ⭐ *„Speichere nicht nur einen Backtest-Wert. Speichere eine Verteilung."* |
| **§13** | ⭐ harte, benannte Tests statt eines Gütemaßes |

---

## RT1 — ⚠️⚠️ Fünf der acht Kill Tests sind heute rechenbar. Deshalb müssen sie VOR der Selektion registriert werden

**Was auf dem vorhandenen Bestand ohne neue Daten, ohne LLM und ohne Agenten
rechenbar ist:**

| Kill Test (§13) | rechenbar aus | |
|---|---|---|
| **1** Performance verschwindet nach realistischen Kosten | Kostenmodell besteht bereits | ⭐ heute |
| **3** Performance hängt an einem Jahr | die 7–9 Selektionsfalten je Bot, heute gemessen | ⭐ heute |
| **4** Performance hängt an einem Asset | 3 bis 149 Symbole je Bot, Zerlegung vorhanden | ⭐ heute |
| **5** Kleine Parameteränderungen zerstören die Performance | **das Gitter selbst** — N = 653 je Bot ist die Parameternachbarschaft | ⭐ heute |
| **7** Ohne die besten fünf Trades bricht sie zusammen | Trade-Listen in den neun `paper_trading_*.db` | ⭐ heute |
| **2** Edge nur in-sample | braucht die OOS-Kette | nach dem Tag |
| **6** Ein Marktereignis erklärt die Rendite | braucht die Ereignisdatenbank (Epic KG) | später |
| **8** Kleine Ausführungsverzögerung zerstört den Edge | braucht Auflösung unter 1 h (KG5) | gesperrt |

⚠️⚠️ **Und hier liegt die Falle, und sie ist die wichtigste dieses Nachtrags:**

> **Ein Kill Test, der nach dem Blick auf den Gewinner gewählt wird, ist kein
> Kill Test. Er ist eine zweite Selektion.**

Wer nach dem Selektionslauf fünf Tests auf den Sieger rechnet und ihn
verwirft, hat den Zweitplatzierten gewählt — mit einem Verfahren, das niemand
vorher aufgeschrieben hat. **Das ist genau der Vorgang, gegen den das ganze
Register gebaut wurde**, nur mit besserem Wortschatz.

⇒ ⭐⭐ **Regel, und sie gehört in einen Registertext, nicht in den Backlog:**
Welche Kill Tests auf den Selektionslauf angewandt werden, **samt Schwellen**,
steht im Register **vor** dem Lauf — oder sie werden auf ihn **überhaupt nicht**
angewandt. Nach dem Lauf dürfen sie an neuen Kandidaten laufen, nie am
Ergebnis.

⚠️ **Praktische Folge für den Tag:** Das RT-MVP darf **nicht vor** dem
signierten Tag laufen, obwohl es könnte. Die Versuchung ist real, und sie ist
der Grund, warum dieser Punkt an erster Stelle steht.

---

## RT2 — ⚠️ §13 nennt Tests ohne Schwellen. Ein Test ohne Schwelle ist eine Meinung

*„Performance disappears after realistic transaction costs"* — **was heißt
disappears?** Null? Unter dem Zinssatz? Unter dem Buy-and-Hold? Ohne eine vorher
festgelegte Zahl entscheidet nach dem Lauf, wer hinsieht.

⇒ **Jeder Kill Test trägt drei Dinge, bevor er zum ersten Mal läuft:** die
Größe, die er misst · die Schwelle · und **was passiert, wenn sie gerissen
wird** (Status nach §13). ⭐ Das ist die Regel aus TB-55b: *ein Abbruchkriterium
benennt die Sache, nie ihren Stellvertreter.*

---

## RT3 — ⚠️⚠️ KILL TEST 7 ist so, wie er dasteht, statistisch falsch — und er würde vier unserer neun Bots erschlagen

**§13 KILL TEST 7 / §14:** *„Removing top 5 trades destroys the strategy."*

⚠️ **Das zerstört die Performance **jeder** Strategie mit rechtsschiefer
Renditeverteilung** — und bei Trendfolge ist es **definitorisch**: Trendfolge
verdient ihren gesamten Erwartungswert aus wenigen großen Gewinnern. **Vier der
neun Bots sind Breakout- oder Trendbots** (`volatility_breakout`,
`volatility_breakout_crypto`, `turtle_soup_*`). Wörtlich angewandt fällt jeder
davon durch — **nicht wegen eines Defekts, sondern wegen seiner Bauart.**

⇒ ⭐⭐ **Die richtige Form braucht ein Nullmodell:** Die Abhängigkeit von den
besten fünf Trades wird gegen die Abhängigkeit verglichen, die für **diese
Renditeverteilung** zu erwarten ist — etwa indem dieselbe Entnahme an
permutierten oder aus derselben Verteilung gezogenen Trade-Folgen gerechnet
wird. **Die Frage lautet nicht „bricht sie zusammen", sondern „bricht sie
stärker zusammen als ihre eigene Verteilung erwarten lässt".**

⚠️ **Ohne dieses Nullmodell misst KILL TEST 7 die Form der Renditeverteilung
und nennt das Ergebnis Fragilität.** ⭐ **§14 und KILL TEST 7 sind derselbe
Test** — ein Epic-Bestandteil, nicht zwei.

---

## RT4 — ⚠️ §8 und §9: der Bootstrap zerstört genau das, was die Strategie ausmacht

**§8 listet `shuffle trade sequence` und `bootstrap trades`.**

⚠️ Beides zerstört die Zeitordnung — und damit Autokorrelation, Regimestruktur
und Verlustserien. **Die resultierende Drawdown-Verteilung gehört zu einer
Strategie, deren Trades unabhängig sind.** Das ist keine dieser neun.

⭐ **§8 nennt `block bootstrap` und `regime resampling` selbst** — das ist die
richtige Antwort. ⚠️ **Aber die Blocklänge ist ein freier Parameter, der das
Ergebnis verschiebt.** Wer sie nach dem ersten Blick wählt, wählt die
Drawdown-Verteilung.

⇒ **Blocklänge und Resampling-Verfahren werden vor dem Lauf registriert.** Und
`shuffle trade sequence` wird **nicht** als Robustheitsnachweis geführt,
sondern höchstens als Vergleichsgröße — mit dem Satz daneben, was sie zerstört.

---

## RT5 — ⚠️⚠️ §18: sieben Kennzahlen ohne Gewichte sind sieben Freiheitsgrade

**§18 will die Fitness aus** Return Quality + Robustness + Parameter Stability +
Regime Coverage + Execution Robustness + Drawdown Stability + Failure
Resistance **bilden, und ergänzt:** *„Keine einzelne Kennzahl soll automatisch
über die anderen dominieren."*

⚠️⚠️ **Wer die Gewichte setzt, wählt den Sieger.** Das ist derselbe Vorgang wie
eine Zielfunktion, die nach dem Lauf angepasst wird — und dieses Projekt hat
genau deswegen **Verfahren B mit Faltenmedian in den Registertext geschrieben**,
damit niemand das Maß hinterher anfassen kann.

⇒ **Die Gewichte werden vor dem ersten Evolutionslauf registriert, oder es gibt
keine zusammengesetzte Fitness.** ⭐ **Die Alternative ist besser und billiger:
Schwellen statt Gewichte.** Eine Strategie besteht oder besteht nicht — jede
Kennzahl mit eigener, vorher festgelegter Schwelle. Das erzeugt keine Rangfolge,
die man frisieren kann, und das ist ein Vorteil, kein Mangel.

---

## RT6 — ⚠️⚠️ §11 hat kein Abbruchkriterium und kein Nullmodell. So gebaut zerstört es jede Strategie

**§11 will, dass das System selbst Marktbedingungen erzeugt, unter denen die
Strategie versagt.**

⚠️ **Ein Generator, der nach Versagensbedingungen sucht, findet sie immer** —
für jede Strategie, auch für eine gute. Mit genügend Freiheit in der Erzeugung
ist jede Strategie zerstörbar. **§11 hat damit keine Stoppregel:** das Ergebnis
„gefunden" trägt keine Information.

⭐ **§10 sagt richtig:** synthetische Daten sind kein Beweis für Profitabilität.
⚠️ **Der fehlende Satz ist die Umkehrung, und er ist der wichtigere:**

> **Synthetische Daten sind auch kein Beweis für Fragilität.**

⇒ **Damit §11 etwas messen kann, braucht es drei Dinge:**
1. eine **registrierte Zulässigkeitsmenge** — welche erzeugten Marktbedingungen
   gelten als möglich, weil ähnliche vorgekommen sind;
2. eine **Kontrolle**: derselbe Generator gegen eine als robust und eine als
   kaputt bekannte Strategie. ⚠️ **Versagen beide, misst er nichts;**
3. eine **Kostengrenze**, weil die Suche unbeschränkt ist.

⭐ **Deshalb ist §11 ein V2-Punkt, nicht MVP** — und im MVP hat er nichts zu
suchen.

---

## RT7 — ⭐⭐ §28 ist die beste Idee der fünf Konzepte, und sie ist heute umsetzbar

**§28 will die Angreifer bewerten:** echte Fehlermodi, falsch Positive, falsch
Negative, Redundanz, Kosten.

⚠️ *„später bestätigte Schwachstellen"* braucht Wahrheit, die erst in Jahren
eintrifft. **Kurzfristig messbar sind zwei Dinge:**

| | |
|---|---|
| **Redundanz** | finden zwei Angriffe dasselbe? |
| ⭐⭐ **Bissfestigkeit** | **feuert der Angriff auf einer absichtlich kaputten Strategie?** |

⇒ ⭐⭐ **Das ist Prüfprinzip B1, auf Angriffe angewandt, und es ist die erste
Fähigkeit des Epics:** **Jeder Angriff wird an einer bekannt kaputten Strategie
validiert, bevor er an eine echte darf.** Eine Kaputt-Strategie ist billig
herzustellen — eine mit eingebautem Look-ahead, eine, die nur ein Jahr
funktioniert, eine, die an einem Symbol hängt. ⭐ **Ein Angriff, der auf der
Kaputt-Strategie nicht feuert, kommt nicht in den Lauf.**

---

## RT8 — Überschneidung: ein Drittel ist neu, zwei Drittel stehen schon woanders

| Abschnitt | ist bereits |
|---|---|
| **§17** Repair Agent | **AF** — Strategy Evolution |
| **§18** Adversarial Evolution | **AF** — Strategy Genome + Fitness |
| **§19** Immune System, **§21** Health | **AF** Strategy Registry + **QR** Self-Healing Pool |
| **§20** Live Shadow Red Team | **QR** Edge Decay Monitor — ⚠️ **und trägt dieselbe Falle wie QR4**: Abschwächung ist auf einem Random Walk normal |
| **§27** Research Ledger | **QR2** = das Register — ⚠️ **zum fünften Mal in fünf Konzepten derselbe Baustein unter neuem Namen** |
| **§29** Research Budget | **QR5**, **KG-F12** |
| **§23 / §24 / §25 / §26** | Integrationen, keine Bausteine |

**Wirklich neu in (r):**

| | |
|---|---|
| **§3–§9** | ⭐ **die Angriffsmaschine selbst** — und der überwiegende Teil ist mit vorhandenen Daten rechenbar |
| **§16** | **Failure Mode Database** — billig, nützlich, ohne Vorbedingung |
| **§15** | **Drawdown-Forensik** — ⭐ die Zerlegung ist heute machbar; die KI-Erklärung ist V2 |
| **§10–§11** | synthetische und erzeugte Märkte — ⚠️ **V2, RT6** |
| **§28** | ⭐⭐ **Angreiferbewertung** — einzigartig unter den fünf |

⇒ ⭐ **Das Register kommt in fünf von fünf Konzepten vor, jedes Mal unter einem
anderen Namen** (Prediction Ledger, Data Lineage, Research Ledger,
Hypothesis Registry, Versuchsregister). **Es ist nicht ein Baustein von
mehreren; es ist der Baustein, auf dem alle fünf stehen.** Das ist der
stärkste Befund über die fünf Einreichungen zusammen.

---

## RT9 — ⚠️ Ich ändere meine Reihenfolge von vor einer Stunde

**Gesagt hatte ich:** `AF → QR → KG → MI`.

**Richtig ist:**

```
AF  →  RT  →  QR  →  KG  →  MI
```

| | Begründung |
|---|---|
| **AF zuerst** | trägt die Validierungskette |
| ⭐ **RT direkt danach** | **die billigste der fünf Schichten**: keine neue Datenquelle, kein Graph, keine Agenten für den Kern. Fünf Kill Tests sind heute rechenbar (RT1) |
| | ⭐⭐ **und sie macht AFs Ausgabe erst glaubwürdig** — eine Strategie, die Angriffe überlebt hat, ist etwas anderes als eine mit gutem Backtest |
| **QR danach** | Hypothesenlabor braucht beides: Erzeuger und Angreifer |
| **KG, MI** | wie in (q) |

⚠️ **Warum ich mich korrigiere:** Ich hatte RT nach seinem Anspruch eingeordnet
(autonomes Labor, Agenten, synthetische Märkte) statt nach seinen
Voraussetzungen. **Der Kern braucht fast nichts.**

---

## Merkmale (Features) — RT-F0 bis RT-F11

| | Merkmal | Vorbedingung |
|---|---|---|
| **F0** | ⭐⭐ **Kaputt-Strategien-Sammlung**: mindestens drei absichtlich defekte Strategien (Look-ahead, Ein-Jahr-Edge, Ein-Symbol-Edge) | — |
| **F1** | ⭐⭐ **Bissprüfung je Angriff** gegen F0 — kein Angriff läuft an einer echten Strategie, bevor er auf einer kaputten gefeuert hat | F0 |
| **F2** | **Registrierung eines Angriffslaufs**: welche Angriffe, welche Schwellen, welche Strategieversion, welcher Datenstand — vor dem Lauf | — |
| **F3** | **Kill Tests 1, 3, 4, 5 mit Schwellen** — die vier heute rechenbaren ohne Nullmodellbedarf | F2 |
| **F4** | **Kill Test 7 / §14 mit Nullmodell** (RT3) — Abhängigkeit gegen Verteilungserwartung, nicht gegen Null | F2 |
| **F5** | **Parameterstabilitätskarten** aus dem **vorhandenen** Gitter (N = 653), nicht aus neuen Läufen | F2 |
| **F6** | **Zeit- und Regimezerlegung** je Bot auf den gemessenen 7–9 Falten | F2 |
| **F7** | **Block-Bootstrap mit registrierter Blocklänge**; `shuffle` nur als benannte Vergleichsgröße | F2 |
| **F8** | **Drawdown-Zerlegung** — Start, Dauer, Tiefe, Erholung je Drawdown; ⚠️ **ohne KI-Erklärung** in Fassung 1 | — |
| **F9** | **Failure-Mode-Register** mit Verknüpfung Strategie ↔ Fehlermodus | F3, F4 |
| **F10** | **Angreiferbewertung**: Redundanz und Bissquote je Angriffsart | F1 |
| **F11** | **Schwellen statt Gewichte** für die Gesamtbeurteilung (RT5) — jede Kennzahl mit eigener registrierter Schwelle | F2 |

⚠️ **Ausdrücklich V2, nicht MVP:** §10 synthetische Szenarien · §11 erzeugte
Märkte (RT6) · §17 Repair Agent · §18 adversariale Evolution · §19 Immune
System · KI-Erklärungen für Drawdowns.

---

## Nicht verhandelbare Abhängigkeiten

1. ⚠️⚠️ **Der signierte Tag — und hier strenger als bei den anderen vier.**
   RT könnte heute rechnen. **Genau deshalb darf es nicht**, solange die
   Selektion offen ist (RT1).
2. ⚠️⚠️ **F0 und F1 vor jedem Angriff auf eine echte Strategie.** Ein Angriff,
   dessen Bissfestigkeit nicht belegt ist, erzeugt „bestanden"-Meldungen, die
   nichts bedeuten — **Prüfprinzip A1: ein fehlgeschlagener Nachweis und ein
   leeres Ergebnis sehen gleich aus.**
3. ⚠️ **Kill Tests, die auf den Selektionslauf wirken, stehen vorher im
   Register** — samt Schwellen (RT1).
4. ⚠️ **Kein Angriff ändert eine Strategie.** Das Red Team liest; die
   Reparatur ist ein getrennter, freigegebener Vorgang (§17, V2). Die
   Sperrliste gilt unverändert.
5. **Die neun `paper_trading_*.db` sind der einzige OOS-Beleg** und nicht
   nachrechenbar. ⚠️ **Jeder Angriff, der Trade-Listen liest, liest sie aus
   einer Kopie.**

---

## Risiken, nach Schadenshöhe

| | |
|---|---|
| **1** | ⚠️⚠️ **Kill Tests als zweite Selektion** (RT1) — der einzige Punkt, der den Tag beschädigen kann |
| **2** | ⚠️⚠️ **Angriffe ohne Bissfestigkeit** erzeugen falsche Sicherheit — schlimmer als kein Angriff (A1) |
| **3** | ⚠️⚠️ **KILL TEST 7 wörtlich** erschlägt vier gesunde Trendbots (RT3) |
| **4** | ⚠️⚠️ **§11 ohne Zulässigkeitsmenge** zerstört jede Strategie und misst nichts (RT6) |
| **5** | ⚠️ **Sieben Kennzahlen ohne Gewichte** (RT5) — Selektion nach Geschmack |
| **6** | ⚠️ **Bootstrap zerstört Zeitstruktur** und liefert eine Drawdown-Verteilung für eine andere Strategie (RT4) |
| **7** | ⚠️ **Reparatur, die Performance maximiert statt die Schwäche zu beheben** — §30 verbietet es ausdrücklich; die Verbotsstelle ist die Umsetzung |

---

## MVP — und es hat eine Ausgabezahl

| | |
|---|---|
| Gegenstand | die **neun bestehenden Bots** |
| Angriffe | **Kill Tests 1, 3, 4, 5, 7** — Schwellen vorher registriert |
| Vorschaltung | ⭐⭐ **F0 + F1**: drei Kaputt-Strategien, und jeder der fünf Angriffe muss auf ihnen feuern |
| Daten | vorhandene Kursdateien, vorhandenes Gitter, Kopien der neun Datenbanken |
| Zeitpunkt | ⚠️ **nach dem signierten Tag** |

**Die eine Zahl:**

> ⭐⭐ **Wie viele der neun Bots fallen durch einen Kill Test, den der Backtest
> nicht gezeigt hat?**

⚠️ **Null ist ein Ergebnis** — dann findet systematisches Angreifen nichts, was
die heutige Methode übersieht, und das Labor hat eine Woche gekostet statt eines
Jahres. ⭐ **Mehrere ist ein besseres Ergebnis** — dann ist belegt, dass der
Backtest allein nicht reicht, und zwar an unseren eigenen Bots.

---

## Ergänzungen zu Abschnitt 4 — ⟨nächste freie Nummern, von der Sitzung gemessen⟩

| Regel | |
|---|---|
| **⟨a⟩** | ⭐⭐ **Ein Prüfkriterium, das nach dem Blick auf das Ergebnis gewählt wird, ist eine Selektion.** Gilt für Kill Tests, Ausschlussregeln und Plausibilitätsprüfungen gleichermaßen — Quelle des Grundes, nicht Zeitpunkt (F17) |
| **⟨b⟩** | ⭐⭐ **Jede Probe wird an einem bekannt kaputten Gegenstand validiert, bevor sie an einen echten darf.** Die allgemeine Fassung von B1, über Mutationsproben hinaus |
| **⟨c⟩** | **Ein Test ohne vorher festgelegte Schwelle ist eine Meinung.** Größe, Schwelle und Folge stehen zusammen |
| **⟨d⟩** | **Zusammengesetzte Maße brauchen registrierte Gewichte — oder es werden Schwellen statt Gewichte verwendet.** Schwellen sind vorzuziehen |
| **⟨e⟩** | **Ein Verfahren, das Versagen sucht, braucht eine Zulässigkeitsmenge und eine Kontrolle.** Sonst findet es immer etwas |

---

## In einfacher Sprache

**Das fünfte Konzept dreht die Frage um:** Nicht „funktioniert die Strategie",
sondern „wie schwer ist sie kaputtzumachen". ⭐ **Das ist die beste
Formulierung in allen fünf Einreichungen** — und es ist genau, was dieses
Projekt seit zwei Wochen mit seinen eigenen Beweisen tut. Heute hat die
Mac-Sitzung eine Schranke absichtlich wieder eingebaut, nur um zu zeigen, dass
die Prüfung sie bemerkt. **Was fehlt, ist nicht die Haltung, sondern ihr
Gegenstand: Wir greifen unsere Nachweise an, nicht unsere Strategien.**

⭐ **Die gute Nachricht:** Fünf der acht harten Tests könnten wir **heute**
rechnen. Keine neuen Daten, keine KI, keine Agenten — die Trade-Listen,
das Parametergitter und die Faltenstruktur sind alle vorhanden.

⚠️⚠️ **Und das ist gleichzeitig die Gefahr, und sie ist die wichtigste Sache
in diesem Dokument.** Wenn wir diese Tests **nach** der Bot-Auswahl rechnen und
den Gewinner damit verwerfen, haben wir den Zweitplatzierten gewählt — mit einem
Maßstab, den niemand vorher aufgeschrieben hat. **Das ist genau der Fehler, gegen
den das ganze Regelwerk gebaut ist**, nur mit schöneren Wörtern. Deshalb: Welche
Tests auf die Auswahl wirken, steht **vorher** im Regelwerk, mit Zahlen — oder
sie wirken **gar nicht** auf sie.

⚠️ **Drei Stellen im Konzept sind so, wie sie dastehen, falsch:**

**Erstens** würde der Test *„nimm die fünf besten Trades weg"* wörtlich
angewandt **vier unserer neun Bots erschlagen** — nicht weil sie schlecht sind,
sondern weil Trendfolge ihr Geld nun einmal aus wenigen großen Gewinnern
verdient. Der Test muss fragen: bricht sie **stärker** zusammen, als ihre eigene
Renditeverteilung erwarten lässt.

**Zweitens** soll das System später selbst Marktbedingungen erzeugen, unter denen
eine Strategie versagt. **Das findet immer etwas** — für jede Strategie, auch für
eine gute. Das Konzept sagt richtig, dass künstliche Daten keine Profitabilität
beweisen. Der fehlende Satz ist die Umkehrung: **sie beweisen auch keine
Zerbrechlichkeit.**

**Drittens** soll die Bewertung aus sieben Kennzahlen bestehen, ohne dass steht,
wie sie gewichtet werden. **Wer die Gewichte setzt, wählt den Sieger.** Besser
sind Schwellen: jede Kennzahl mit ihrer eigenen, vorher festgelegten Grenze.

⭐⭐ **Die beste Einzelidee der fünf Konzepte steht in diesem:** auch den
Angreifer bewerten. Praktisch heißt das etwas, das wir sofort tun könnten —
**drei absichtlich kaputte Strategien bauen und jeden Angriff erst an ihnen
erproben.** Feuert ein Angriff dort nicht, darf er nicht an eine echte
Strategie. Sonst meldet er „bestanden", wo er nur nichts gemessen hat.

**Und ein Befund über alle fünf Einreichungen zusammen:** Das Regelwerk kommt in
jedem der fünf Konzepte vor — als Prediction Ledger, als Data Lineage, als
Research Ledger, als Hypothesis Registry. **Fünf Mal derselbe Baustein unter
einem anderen Namen. Er ist nicht einer von vielen; er ist der, auf dem alle
fünf stehen.**

**Meine Reihenfolge ändert sich:** erst die Validierungskette, **dann dieses
Labor** (weil es das billigste ist und alles andere glaubwürdig macht), dann das
Hypothesenlabor, dann das Ursachennetz, dann die Umschaltung. **Und alles nach
dem signierten Tag** — dieses hier besonders, weil es als einziges die
Versuchung mitbringt, vorher anzufangen.
