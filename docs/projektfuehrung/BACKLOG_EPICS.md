# Backlog-Epics Trading-Bot-Projekt

## 2t — Epic AF: Autonome Strategie-Forschungspipeline

*Eingearbeitet durch TB-59 aus Nachtrag (n); Nummer `2t` dort vorgeschlagen und bei der Einarbeitung als nächste freie nach `2s` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_forschungspipeline_2026-09-19.md`.*

⭐ **Die Reihenfolge der ARBEIT an den fünf Epics ist `AF → RT → QR → KG → MI`** (Nachtrag (r), RT9): *RT braucht fast keine Vorbedingungen und macht AFs Ausgabe erst glaubwürdig.* Die Blöcke 2t bis 2x sind dagegen nach Nachtragsbuchstaben eingearbeitet, damit die Blockkette schliesst — die Blockfolge ist keine Rangfolge (TB-59).

| # | Punkt |
|---|---|
| **AF0** | ⭐⭐ **DAS EPIC IST AUFGENOMMEN UND HINTER DEM SIGNIERTEN TAG GEPARKT.** Zwei Gründe, beide strukturell: ⚠️ **(1)** Der Selektionslauf hat nicht stattgefunden; eine Maschine, die Strategien erzeugt, bevor das Verfahren einmal sauber durchlaufen ist, liefert Kandidaten **ohne registriertes Verfahren**. ⭐ **(2)** Die Pipeline ist die industrialisierte Fassung dessen, was heute von Hand geschieht — **sie erbt die Regeln dieses Registers, oder sie erbt nichts** |
| **AF1** | ⚠️⚠️ **DER TRAGENDE EINWAND: MEHRFACHTESTEN IST KEINE EIGENSCHAFT DES KANDIDATEN.** Die Vorlage führt „Multiple Testing" und „Data Snooping" als Prüfpunkte des Adversarial-Agenten. ⭐ **Ein Agent, der einen einzelnen Kandidaten ansieht, kann sie prinzipiell nicht feststellen.** ⭐⭐ *Wenn 1 000 Strategien getestet werden und 3 überleben, ist die Frage nicht, ob diese 3 gut aussehen — sondern wie viele von 1 000 zufälligen Strategien genauso gut ausgesehen hätten.* **Das ist eine Eigenschaft der Suche, nicht des Kandidaten** — und Abschnitt 16 der Vorlage (100 → 30 → 10 → 3) macht die Suche zum Kernmerkmal |
| **AF2** | ⭐⭐ **FOLGERUNG FÜR DIE ARCHITEKTUR, NICHT FÜR EINE PRÜFLISTE: die effektive Versuchszahl wird mitgeführt.** ⚠️ **Jede je getestete Variante wird gezählt, auch jede verworfene** — sonst ist der Nenner unbekannt und jede Kennzahl am Ende wertlos. **Die Signifikanzschwelle wird daran angepasst** (Deflated Sharpe Ratio, White's Reality Check, Harvey-Liu-Zhu-Abschlag — Verfahren zu prüfen, nicht vorausgesetzt). ⚠️ **Ohne diesen Zähler ist die Pipeline eine Maschine zur Erzeugung von Scheinbefunden** |
| **AF3** | ⚠️⚠️ **DIE SCHWELLEN MÜSSEN VOR DEM ERSTEN LAUF REGISTRIERT SEIN.** Abschnitt 7 der Vorlage sagt, sie sollen „nicht willkürlich festgelegt, sondern aus dem Projekt abgeleitet" werden. ⭐ **Gut gemeint — aber werden sie festgelegt, nachdem Ergebnisse vorliegen, ist es Auswahl nach Wirkung.** Genau davor schützt das Register. ⇒ **Jeder Forschungszyklus braucht seinen eigenen Zeitanker: Schwellen, Universum, Datenstand und Abbruchregeln registriert, bevor der Zyklus startet** |
| **AF4** | ⭐ **WAS DIE VORLAGE BESTÄTIGT — und das ist der grössere Teil.** *Strategy Registry mit Code Version, Data Version, Parameter Set* ⇒ **das sind Register + Snapshot (`63e4b6c8…`) + Lock (`96a5c572…`) + Codeherkunft (Abschnitt 19)**. *Adversarial Review Agent, der widerlegen soll* ⇒ **das ist Fables Rolle**, nachweislich wirksam. *Reproduzierbare Datenstände, Experiment-IDs, Artefakte* ⇒ vorhanden. *„Keine autonome KI setzt eigenständig Kapital ein"* ⇒ deckt sich mit der stehenden Betreiberregel |
| **AF5** | ⚠️ **WAS DER VORLAGE FEHLT: der Zeitanker.** Sie kennt Versionierung, aber keine **Vorregistrierung** — keine Festlegung, die vor dem Ergebnis steht und nachweislich nicht nachträglich geändert wurde. ⭐ **Das ist der Unterschied zwischen „nachvollziehbar" und „nicht nachträglich anpassbar"**, und es ist der teuerste Teil dessen, was dieses Projekt seit dem 15.09. gelernt hat |
| **AF6** | ⚠️ **NOCH NICHT GEMESSEN: die Bestandsaufnahme der Codebasis** gegen Abschnitt 13 der Vorlage (Backtesting, Datenpipeline, Bot-Runtime, Datenbank, Queue, Scheduler, API-Schicht, Logging, Experiment-Tracking, CI/CD, Tests). ⭐ **Rein lesend, ortsunabhängig, ohne Sitzung durchführbar** — sie gehört **vor** jede Feature- und Task-Struktur. *Ohne sie wäre die Backlog-Struktur geraten* |

---

### Epic AF — vorläufige Gliederung

⚠️ **Die Reihenfolge folgt technischen Abhängigkeiten, nicht dem Nutzen.**
⭐ **Alle Features sind hinter dem signierten Tag geparkt**, ausser AF-F0.

```
EPIC AF — Autonome Strategie-Forschungspipeline
 ├── AF-F0  Bestandsaufnahme und Architekturentscheidungen   [JETZT, rein lesend]
 │    ├── AF-T0.1  Codebasis gegen Abschnitt 13 der Vorlage messen
 │    ├── AF-T0.2  Überschneidungen mit Register/Snapshot/Lock benennen
 │    └── AF-T0.3  Offene Architekturfragen an Fable (AF1–AF3)
 ├── AF-F1  Versuchszählung und Signifikanz                  [Grundlage von allem]
 │    ├── AF-T1.1  Zähler über ALLE Varianten, auch verworfene
 │    ├── AF-T1.2  Verfahren zur Schwellenanpassung prüfen und eines registrieren
 │    └── AF-T1.3  Abbruchregeln, die den Zähler nicht verfälschen
 ├── AF-F2  Strategie-Spezifikation, deterministisch reproduzierbar
 ├── AF-F3  Automatisiertes Backtesting auf bestehender Infrastruktur
 ├── AF-F4  Robustheitsprüfung (OOS, Walk-Forward, Parameterstabilität, Regime)
 ├── AF-F5  Adversarial Review — Rolle, Abgrenzung zu Fable
 ├── AF-F6  Strategy Registry mit Statusmaschine
 ├── AF-F7  Research-Agent (Quellenlage, Kosten, xAI/Grok prüfen)
 ├── AF-F8  Paper Trading als Pflichtstufe
 ├── AF-F9  Generationen und Mutation            [bewusst spät]
 └── AF-F10 Portfolio-Ebene, Korrelation, gemeinsame Ausfälle  [bewusst spät]
```

**Abhängigkeiten, die nicht verhandelbar sind:**

| | |
|---|---|
| ⚠️⚠️ **AF-F1 vor allem anderen** | Ohne Versuchszählung erzeugen F3–F5 Zahlen, die niemand deuten kann |
| ⚠️ **AF-F2 vor AF-F3** | Eine Strategie, die nicht deterministisch reproduzierbar ist, ist nicht testbar |
| ⚠️ **AF-F6 vor AF-F7** | Ein Research-Agent ohne Registry erzeugt Ideen, die niemand wiederfindet |
| ⚠️ **AF-F8 vor jedem Live-Gedanken** | Betreiberregel, Abschnitt 12 der Vorlage |
| ⭐ **AF-F9 und F10 bewusst zuletzt** | Mutation über Generationen vervielfacht die Versuchszahl — **erst wenn F1 trägt** |

---

### Risiken, benannt

| | |
|---|---|
| ⚠️⚠️ **Scheinbefunde im industriellen Massstab** | AF1/AF2. **Das Hauptrisiko**, und es ist nicht durch Sorgfalt am Einzelfall behebbar |
| ⚠️ **Schwellen nach Ergebnis** | AF3 |
| ⚠️ **Kosten** | Abschnitt 17 der Vorlage. ⭐ Ein Budget je Zyklus **vor** dem Zyklus, nicht danach |
| ⚠️ **Aufmerksamkeit** | Der laufende Selektionslauf ist nicht fertig. **Ein zweites grosses Vorhaben parallel gefährdet das erste** |
| ⚠️ **Secrets in erzeugtem Code** | Abschnitt 18 der Vorlage nennt es selbst. ⭐ Deckt sich mit den stehenden Secrets-Regeln |

---

### MVP — die kleinste sinnvolle erste Fassung

⭐ **Nicht „eine Strategie automatisch erzeugen", sondern: EIN Forschungszyklus
mit N = 1, vollständig protokolliert** — Idee, Spezifikation, Implementierung,
Backtest, Robustheit, Adversarial Review, Ergebnis, **und der Versuchszähler
steht auf 1**.

⚠️ **Erst wenn dieser eine Zyklus reproduzierbar durchläuft, wird
parallelisiert.** *Die Vorlage sagt es selbst: „ohne dass die Ergebnisse nicht
reproduzierbar werden."*

## 2u — Epic MI: KI-Marktverständnis und adaptive Allokation

*Eingearbeitet durch TB-59 aus Nachtrag (o); Nummer `2u` dort vorgeschlagen und bei der Einarbeitung als nächste freie nach `2t` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_marktverstaendnis_2026-09-19.md`.*

| # | Punkt |
|---|---|
| **MI0** | ⭐⭐ **AUFGENOMMEN, GEPARKT — und zwar HINTER Epic AF.** ⚠️ **Der Allokator setzt einen Pool von 100–1 000 validierten Strategien voraus. Wir haben neun, und der Selektionslauf hat nicht stattgefunden.** ⭐ **Ohne Pool hat der Allokator nichts zu verteilen** — das ist keine Priorisierung, sondern eine Abhängigkeit |
| **MI1** | ⭐⭐ **WAS DIE VORLAGE RICHTIG ENTSCHEIDET, und es ist mehr als beim ersten Konzept.** *(a)* **Das LLM erzeugt einen strukturierten Zustand, keine Order** — deterministische Modelle entscheiden. *(b)* *„Ein LLM-generierter Text darf nicht als alleinige Begründung für eine Kapitalentscheidung dienen."* *(c)* **Die Risk Engine ist LLM-fest.** *(d)* **Shadow Mode vor jedem Einsatz.** ⭐ **Alle vier decken sich mit den stehenden Regeln dieses Projekts** |
| **MI2** | ⚠️⚠️ **DER STRUKTURELLE HAUPTBEFUND: Regime-bedingte Kennzahlen vervielfachen den Suchraum und zerlegen die Stichprobe.** Abschnitt 10 will je Strategie **eine Kennzahl je Regime** (`TREND_HIGH_VOL: 2.1`, `PANIC: −0.8`). ⚠️ **Wie viele PANIC-Episoden gibt es in den Daten? Eine Handvoll.** Bei 9 Regimen × 100 Strategien sind es **900 Zellen**, die meisten fast ohne Daten — ⭐⭐ **und es wird auf ihnen ausgewählt.** **Das ist Mehrfachtesten (K2p — *im Nachtrag (o) als `K2r` bezeichnet; die Regel aus Nachtrag (n) ist als `K2p` vergeben*), nur gefährlicher: die Zellen sehen aus wie Wissen, nicht wie eine Suche** |
| **MI3** | ⚠️⚠️ **VINTAGE-DATEN SIND EINE HARTE VORBEDINGUNG, KEIN PRÜFPUNKT.** Abschnitt 19 nennt *„revised macro data"* und *„delayed news"* in einer Aufzählung. ⭐ **Die Folge ist härter, als die Aufzählung nahelegt:** Makrodaten werden **nachträglich revidiert**; wer mit der revidierten Reihe backtestet, hat **Look-ahead per Konstruktion** — nicht abgeschwächt, sondern ungültig. **Dasselbe für Nachrichten:** der Zeitpunkt, zu dem eine Meldung **handelbar** war, ist nicht ihr Veröffentlichungsstempel. ⇒ ⚠️ **Ohne Daten „wie damals erstveröffentlicht" ist der Backtest des KI-Layers wertlos. Das ist eine Architekturentscheidung, die VOR allem anderen fällt** |
| **MI4** | ⚠️ **MARKET MEMORY IST EIN AUSWAHLVERFAHREN IN VERKLEIDUNG.** Abschnitt 7 sucht ähnliche historische Episoden und fragt, was danach funktionierte. ⭐ **Bei reichem Merkmalsraum und wenigen Episoden sieht immer irgendetwas ähnlich aus** — und **das Ähnlichkeitsmass ist selbst ein frei gewählter Parameter**. ⇒ **Das Mass wird vor der Benutzung registriert, und die Zahl der Vergleiche wird gezählt** (K2p — *im Nachtrag (o) als `K2r` bezeichnet; die Regel aus Nachtrag (n) ist als `K2p` vergeben*) |
| **MI5** | ⭐ **DER ALLOKATOR IST SELBST EINE STRATEGIE und wird wie eine getestet.** Seine Umschichtungsfrequenz, seine Schwellen, seine Korrelationsfenster sind **Parameter, die überangepasst werden können.** ⚠️ **Abschnitt 19 sieht das richtig** — der Nachtrag hält es als Regel fest: **dieselbe Registrierung, dieselbe Versuchszählung, derselbe Zeitanker wie für jede andere Strategie** |
| **MI6** | ⭐ **PREDICTION TARGETS: die Vorlage hat hier vermutlich recht, und es ist prüfbar.** *„P(Volatilitätsausweitung)"* statt *„steigt BTC morgen"* ist statistisch günstiger — mehr Ereignisse, symmetrischere Verteilung, weniger Abhängigkeit von der Driftschätzung. ⚠️ **Aber es ist eine Hypothese und keine Tatsache** — ⭐ **als Research-Task aufnehmen, nicht als Festlegung** |
| **MI7** | ⭐ **WAS HEUTE SCHON BILLIG UND NÜTZLICH WÄRE — und trotzdem warten muss:** „Strategy Performance by Regime" für **unsere neun Bots** ist eine reine Auswertung vorhandener OOS-Daten. ⚠️⚠️ **Nicht vor dem signierten Tag** — eine regimebedingte Auswertung der neun könnte die Selektionsentscheidung beeinflussen, und das wäre Auswahl nach Wirkung |
| **MI8** | ⚠️ **NOCH NICHT GEMESSEN: die Bestandsaufnahme** gegen Abschnitt 22 der Vorlage (Datenbank, Queue, Vector-DB, Feature Store, Experiment-Tracking, News-Daten, Execution Engine). ⭐ **Gemeinsam mit AF6 zu erheben** — rein lesend, ortsunabhängig, ohne Sitzung |

---

### Epic MI — vorläufige Gliederung

⚠️ **Reihenfolge nach Abhängigkeiten. Alles hinter Epic AF, und AF ist hinter
dem Tag.**

```
EPIC MI — KI-Marktverständnis und adaptive Allokation
 ├── MI-F0  Vintage-Datenarchitektur              [VOR allem anderen, MI3]
 │    ├── MI-T0.1  Welche Makroreihen gibt es als Erstveröffentlichung?
 │    ├── MI-T0.2  Nachrichten: Handelbarkeitszeitpunkt statt Veröffentlichung
 │    └── MI-T0.3  Architekturentscheidung: ohne Vintage kein KI-Layer-Backtest
 ├── MI-F1  Marktzustand aus quantitativen Merkmalen   [ohne LLM beginnen]
 ├── MI-F2  Regime-Erkennung + ⚠️ Stichprobengrösse je Regime messen (MI2)
 ├── MI-F3  Historische Episodendatenbank
 ├── MI-F4  Ähnlichkeitsmass — registriert vor Benutzung (MI4)
 ├── MI-F5  Strategieleistung je Regime          [nach dem Tag, MI7]
 ├── MI-F6  Allokator als registrierte Strategie (MI5)
 ├── MI-F7  Backtest des gesamten KI-Layers      [setzt MI-F0 voraus]
 ├── MI-F8  Shadow Mode
 ├── MI-F9  Risk Engine — Integration, LLM-fest
 ├── MI-F10 Ereignisextraktion (Grok/xAI prüfen)  [nach MI-F0]
 ├── MI-F11 Erklärbarkeit aus Messwerten, nicht aus Text
 ├── MI-F12 Portfolio-Ebene: Cluster erkennen
 └── MI-F13 Information Arbitrage                 [Research, spät]
```

**Abhängigkeiten, die nicht verhandelbar sind:**

| | |
|---|---|
| ⚠️⚠️ **MI-F0 vor MI-F7** | Ohne Vintage-Daten ist der KI-Layer-Backtest **ungültig**, nicht schwach |
| ⚠️⚠️ **Epic AF vor Epic MI** | Kein Pool, kein Allokator (MI0) |
| ⚠️ **MI-F2 misst die Stichprobe, bevor sie Zellen bildet** | Ein Regime mit fünf Episoden liefert keine Kennzahl (MI2) |
| ⭐ **MI-F1 beginnt OHNE LLM** | Quantitative Merkmale zuerst; das LLM kommt dazu, wenn die Grundlage misst |
| ⚠️ **MI-F5 nach dem signierten Tag** | MI7 |

---

### Risiken, benannt

| | |
|---|---|
| ⚠️⚠️ **Regime-Zellen als Scheinwissen** | MI2. ⭐ **Das Hauptrisiko dieses Epics**, und es ist schwerer zu sehen als beim Vorgänger, weil die Zahlen nach Erkenntnis aussehen |
| ⚠️⚠️ **Look-ahead durch revidierte Daten** | MI3. **Baut man darauf, ist alles Folgende ungültig** |
| ⚠️ **Ähnlichkeitssuche findet immer etwas** | MI4 |
| ⚠️ **Der Allokator überangepasst** | MI5 |
| ⚠️ **Kosten** | Mehrere LLM-Schichten, dauerhaft laufend. ⭐ Budget je Zyklus **vor** dem Zyklus |
| ⚠️ **Aufmerksamkeit** | **Zwei grosse Epics und ein unfertiger Selektionslauf.** *Das grösste Risiko ist nicht technisch* |

---

### MVP

⭐ **Nicht der Allokator. Sondern: ein Marktzustand aus rein quantitativen
Merkmalen, über die vorhandenen 223 Kursdateien, ohne LLM und ohne
Nachrichten** — und die Messung, **wie viele Episoden je Regime überhaupt
vorliegen** (MI2).

⚠️ **Ergibt diese Messung, dass die meisten Regime unter einer brauchbaren
Stichprobengrösse liegen, ist das kein Rückschlag, sondern das Ergebnis** —
und es verhindert, dass darauf ein Allokator gebaut wird.

## 2v — Epic QR: Alpha-Discovery-Labor

*Eingearbeitet durch TB-59 aus Nachtrag (p); Nummer `2v` dort vorgeschlagen und bei der Einarbeitung als nächste freie nach `2u` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_alpha_labor_2026-09-19.md`.*

| # | Punkt |
|---|---|
| **QR0** | ⭐⭐ **DAS METHODISCH REIFSTE DER DREI KONZEPTE.** Es nennt Mehrfachtesten als **eigenes technisches Thema** (§16, nicht als Prüflistenpunkt wie bei AF), verlangt einen **Prediction Ledger ohne nachträgliches Umschreiben** (§8/§9), **Agentenkalibrierung mit Brier Score** (§7) — ⭐ **und ein MVP-Erfolgskriterium, das ausdrücklich NICHT „wir haben eine profitable Strategie gefunden" lautet** (§24) |
| **QR1** | ⭐⭐ **DAS NULLMODELL IST GENANNT, ABER NICHT ENTWORFEN — und es ist der Kern.** §24 fragt: *„Sind die Hypothesen besser als zufällige Hypothesen?"* ⚠️ **Das verlangt, tatsächlich zufällige Hypothesen zu erzeugen und durch dieselbe Pipeline zu schicken** — nicht als Kontrolle nebenbei, sondern als **gleichrangige Komponente.** ⭐ **Es ist die billigste Art herauszufinden, dass das Ganze Rauschen ist**, und der Grund, warum solche Systeme es meist nicht tun: es ist demütigend und es funktioniert |
| **QR2** | ⚠️⚠️ **SPEICHERN IST NICHT BEWEISEN.** §9 verlangt, eine Prognose nach Kenntnis des Ergebnisses nicht zu verändern, und listet, was zu speichern ist. ⭐ **Speichern zeigt nicht, dass nichts verändert wurde.** Dafür braucht der Ledger **Anfügen-statt-Ändern und eine Hash-Kette** — jeder Eintrag trägt die Quersumme des vorigen. ⭐⭐ **Anders gesagt: der Prediction Ledger IST das Register, je Hypothese angewandt** — und die Maschinerie dafür steht seit heute (Snapshot, Lock, Codeherkunft, Zeitanker) |
| **QR3** | ⚠️ **EIN BRIER SCORE BRAUCHT EINE VORHER FESTGELEGTE AUFLÖSUNG.** §7 will Agenten kalibrieren. ⭐ **Das ist nur messbar, wenn Ereignis UND Auflösungszeitpunkt vor der Prognose feststehen** — sonst entsteht *„die Prognose ist irgendwie eingetreten"*. ⇒ **Jeder Ledger-Eintrag trägt eine maschinell prüfbare Auflösungsregel**, die ohne Ermessen auswertbar ist |
| **QR4** | ⚠️⚠️ **DER EDGE-DECAY-MONITOR HAT EINE FALLE.** §17 vergleicht erwartete mit tatsächlicher Leistung und schlägt bei Abweichung an. ⭐ **Drawdowns sind normal.** Ein Monitor auf blosse Abweichung schlägt **ständig** an und erkennt überwiegend Rauschen — ⚠️ **und wer daraufhin Strategien abschaltet, verkauft die Verlierer und behält die Gewinner auf einem Zufallspfad. Das ist selbst eine Strategie, und eine schlechte.** ⇒ **Die Abschaltschwelle wird aus der registrierten Eigenvarianz der Strategie abgeleitet, und die Abschaltregel wird wie jede Strategie backgetestet** |
| **QR5** | ⭐ **§25 IST DIE ZAHL, DIE ÜBER DAS GANZE PROGRAMM ENTSCHEIDET:** Kosten je validiertem Edge. ⚠️ **Ab dem ersten Tag des MVP messen, nicht später** — *ein Programm, das seine Kosten je Erkenntnis nicht kennt, kann nicht beendet werden, und genau das ist der häufigste Ausgang* |
| **QR6** | ⭐⭐ **REIHENFOLGE DER DREI EPICS, gegen die Einreichungsfolge.** Der Fluss ist **QR (Hypothesen) → AF (Strategien) → MI (Allokation)**. ⚠️ **Praktisch aber umgekehrt:** QR braucht **AFs Validierungsmaschine**, um seine Hypothesen zu prüfen — ⭐ **und AF kann mit handgeschriebenen Hypothesen arbeiten.** ⇒ **AF zuerst** (es trägt die Prüfung), **dann QR** (es industrialisiert die Ideenzufuhr), **dann MI** (es braucht einen Pool) |
| **QR7** | ⭐ **ALLE DREI KONZEPTE TEILEN EINE VORBEDINGUNG — und das ist selbst ein Befund:** Jedes setzt eine **funktionierende, registrierte Validierungskette** voraus. ⭐⭐ **Genau die bauen wir seit dem 15.09.** Die Konzepte sind nicht der nächste Schritt; **sie sind der Grund, warum der jetzige Schritt sich lohnt** |
| **QR8** | ⚠️ **NOCH NICHT GEMESSEN:** die Bestandsaufnahme (gemeinsam mit AF6/MI8) und die **vollständige Backlog-Sichtung** in fünf Durchgängen. ⭐ **Kollisions- und Ausscheidungsdurchgang fehlen für (n), (o) und (p)** — sie brauchen eine Messung am Backlog, nicht eine Einschätzung |

---

### Epic QR — vorläufige Gliederung

⚠️ **Hinter AF. Beide hinter dem Tag.**

```
EPIC QR — Alpha-Discovery-Labor
 ├── QR-F0  Nullmodell: zufällige Hypothesen durch dieselbe Pipeline  [QR1]
 ├── QR-F1  Prediction Ledger, anfügend, hash-verkettet               [QR2]
 │    ├── QR-T1.1  Eintragsformat mit maschinell prüfbarer Auflösungsregel (QR3)
 │    ├── QR-T1.2  Hash-Kette und Nachweis, dass nichts geändert wurde
 │    └── QR-T1.3  Auswertung: Brier Score, Kalibrierungskurve je Agent
 ├── QR-F2  Mehrfachtest- und FDR-Kontrolle                  [gemeinsam mit AF-F1]
 ├── QR-F3  Anomalieerkennung, quantitativ, ohne LLM
 ├── QR-F4  Hypothesenregister mit Statusmaschine
 ├── QR-F5  Hypothesenerzeugung durch Agenten                [nach QR-F0 und F1]
 ├── QR-F6  Agentenkalibrierung und Gewichtung
 ├── QR-F7  Edge-Validierung — nutzt AFs Kette, baut sie nicht neu
 ├── QR-F8  Edge-Decay-Monitor mit abgeleiteter Schwelle     [QR4]
 ├── QR-F9  Forschungskosten je validiertem Edge             [QR5, ab Tag 1]
 ├── QR-F10 Kausalitätslabor                                  [Research, spät]
 ├── QR-F11 Information Arbitrage                             [Research, spät]
 └── QR-F12 Selbstheilender Strategiepool                     [sehr spät, Governance]
```

**Abhängigkeiten, die nicht verhandelbar sind:**

| | |
|---|---|
| ⚠️⚠️ **QR-F0 und QR-F1 vor QR-F5** | **Erst das Nullmodell und der Ledger, dann die Agenten.** *Wer zuerst Hypothesen erzeugt und danach misst, hat keinen Vergleichsmassstab mehr* |
| ⚠️ **QR-F2 gemeinsam mit AF-F1** | Es ist **dieselbe Versuchszählung** — nicht zwei |
| ⚠️ **QR-F7 nutzt AFs Kette** | ⭐ **Keine zweite Validierungsmaschine.** Zwei Umsetzungen laufen auseinander (T55.8, T54.3) |
| ⚠️ **QR-F8 nach QR-F1** | Ohne Ledger keine Erwartung, gegen die abgewichen werden kann |
| ⭐ **QR-F12 zuletzt, mit Governance** | §18 der Vorlage sagt es selbst |

---

### Risiken, benannt

| | |
|---|---|
| ⚠️⚠️ **Kein Nullmodell** | QR1. **Ohne es ist jede Aussage über Agentenqualität unbelegbar** |
| ⚠️⚠️ **Ledger ohne Beweiskraft** | QR2. *Gespeichert heisst nicht unverändert* |
| ⚠️ **Kalibrierung ohne feste Auflösung** | QR3 |
| ⚠️ **Decay-Monitor als Verlustverkäufer** | QR4 |
| ⚠️ **Kosten ausser Kontrolle** | QR5. Mehrere Agenten, dauerhaft, je Zyklus |
| ⚠️⚠️ **Drei grosse Epics, ein unfertiger Lauf** | ⭐ **Das grösste Risiko, und es ist unverändert** |

---

### MVP

⭐ **Kleiner als in §23, und in dieser Reihenfolge:**

**1.** Prediction Ledger mit Hash-Kette und Auflösungsregel · **2.** Ein
quantitativer Anomaliedetektor, **ohne LLM** · **3.** ⭐⭐ **Ein Nullmodell, das
zufällige Hypothesen desselben Formats erzeugt** · **4.** Beide durch dieselbe
Prüfung · **5.** Die eine Zahl am Ende: **schlagen die echten Hypothesen die
zufälligen — und um wie viel?**

⚠️ **Ergibt sich kein Unterschied, ist das das Ergebnis des MVP**, und es hat
sich gelohnt. ⭐ *§24 sagt dasselbe; der Nachtrag macht daraus eine Komponente.*

## 2w — Epic KG: Market Causal Graph & Market Physics Engine

**Einordnung:** eigenes Epic in Abschnitt 7 (Architektur, offen), hinter AF, QR
und vor MI. Begründung unter **KG9**.

*Vermerk TB-59: nach Auftrag `MAC_TB-59` als Block `2w` in Abschnitt 2 eingearbeitet, nicht in Abschnitt 7; Nachtrag (q) nannte keine Nummer — `2w` bei der Einarbeitung als nächste freie nach `2v` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_kausalgraph_2026-09-19.md`.*

---

### KG0 — Was das Dokument richtig macht, und es ist mehr als bei den drei anderen

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

### KG1 — ⚠️⚠️ Die Zahl der geprüften Beziehungen muss VOR dem Lauf registriert werden

**§19 verlangt, `number_of_relationships_tested` zu *tracken*.** Das ist eine
Messung **nach** dem Lauf.

*„Eine Beispielrechnung mit 50 konkreten Knoten, 20
Verzögerungen und 4 Regimen — Annahmen des Verfassers, nicht des Konzepts —
ergibt 196 000 prüfbare Beziehungen und bei α = 0,05 rund 9 800 Scheintreffer.
Die Größenordnung, nicht die Zahl, ist die Aussage."*

⚠️ **Berichtigt 19.09.2026, 21:05** (`BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md`, Punkt 4): Im Nachtrag (q) stand hier *„Rechnung an der Struktur des Entwurfs selbst: §3 nennt 22 Knotenarten und 10 Kantenarten. Werden daraus nur 50 konkrete Knoten, 20 Verzögerungen (§4) und 4 Regime (§12) gebildet, sind das 50 × 49 × 20 × 4 = 196 000 prüfbare Beziehungen. Bei α = 0,05 liefern rund 9 800 davon ein „signifikantes" Ergebnis, wenn überhaupt kein Zusammenhang existiert."* — Das Konzept nennt 22 Knoten**arten** und 10 Kanten**arten**; die Zahlen 50, 20 und 4 sind Annahmen des Verfassers des Nachtrags, nicht des Konzepts. Der Satz oben ist die von der Berichtigung vorgegebene Ersatzfassung.

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

### KG2 — ⚠️⚠️ §18 ist eine Liste von Prüfungen. Eine Liste von Prüfungen ist keine Falsifikation

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

### KG3 — ⚠️⚠️ `confidence` ist das gefährlichste Feld des ganzen Dokuments

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

### KG4 — ⚠️ §17 ist richtig, und §3 widerlegt es

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

### KG5 — ⭐⭐ Der harte Befund: Lead/Lag ist auf den vorhandenen Daten nicht messbar

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

⚠️ **Berichtigt 19.09.2026, 21:05** (`BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md`, Punkt 1): Die Zeile „feinste vorhandene Auflösung" oben war **aus den Konstantennamen erschlossen, nicht aus den Daten gelesen** (`MIN_HISTORY_HOURS` sagt, dass eine Konstante Stunden zählt; es sagt nichts über die Auflösung der Daten). **Gemessen am 19.09.2026, 21:03, an den Dateinamen und den ersten Datenzeilen in `data/`:**

| Auflösung | Dateien | erste Spalte `open_time` |
|---|---:|---|
| `1d` | **174** | `1980-12-12` — Datum ohne Uhrzeit |
| `1h` | **25** | `2020-10-15 03:00:00`, Folgezeile `04:00:00` |
| `4h` | **24** | — |
| **Summe** | **223** | = der registrierte Datenstand `d9449faf…` |

⭐ **Die Aussage stimmt — und sie ist strenger als geschrieben:** *Eine Stundenauflösung existiert für 25 von 223 Dateien, sämtlich Krypto. Für alle 174 Aktiendateien ist die feinste vorhandene Auflösung ein Tag.* ⚠️⚠️ **Folge, die in (q) fehlt:** §7 des Konzepts (Cross-Asset-Übertragung `Macro Shock → Rates → USD → Equities / Crypto / Commodities`) ist die Stelle, an der Aktien und Krypto zusammenkommen. **Auf der Aktienseite gibt es dafür nur Tagesdaten.** Damit ist Cross-Asset-Übertragung nicht auf eine Stunde, sondern **auf einen Tag** beschränkt — und eine Übertragung, die innerhalb eines Handelstages abläuft, ist mit diesem Bestand grundsätzlich nicht messbar, nicht nur ungenau. ⇒ **KG-F2 wird ergänzt** (siehe Merkmalstabelle).

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

### KG6 — ⚠️ §8 verspricht etwas, das mit diesen Mitteln niemand einlösen kann

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

### KG7 — ⚠️ §10 und §6 sind dasselbe Verfahren, und es hat ein Freiheitsgrade-Problem

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

### KG8 — ⭐ Die Überschneidung ist größer, als §29 C vermutet: die Hälfte ist schon da

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

### KG9 — Reihenfolge, und der eine Satz, der in §30 fehlt

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

### Merkmale (Features) — KG-F0 bis KG-F12

*Vermerk TB-59: die erste Spalte trägt das Präfix `KG-`, wie die Überschrift es nennt — im Nachtrag (q) stand dort `F0` bis `F12`; `F1` bis `F20` sind in dieser Datei bereits als Zeilenkennungen vergeben (Abschnitt 4, Block 2m). Verweise im Text („F0 + F8") sind wörtlich belassen und meinen die Zeilen dieser Tabelle. Betreiberentscheidung 19.09.2026.*

| | Merkmal | Vorbedingung |
|---|---|---|
| **KG-F0** | **Registrierung eines Graphenlaufs**: Knotensatz, Kantenarten, Verzögerungen, Regime, **N** — vor dem Lauf, inhaltsadressiert | — |
| **KG-F1** | **Relationship Registry** mit **zwei Kantenklassen** (beobachtend / behauptend), keine Beförderung durch Beobachtungszahl | F0 |
| **KG-F2** | **Pflichtfeld Auflösung** je Beziehung (1 h / 1 d), und ein Feld, das die feinste im Datenbestand vorhandene Auflösung nennt. ⚠️ *Ergänzt durch die Berichtigung vom 19.09.2026, 21:05, Punkt 1:* **Das Pflichtfeld Auflösung trägt je Anlageklasse einen Wert, nicht einen für den ganzen Lauf** | — |
| **KG-F3** | **Abbruchkriterium je Beziehung**, maschinell prüfbar, vor dem ersten Test, an permutierten Daten auf Bissfestigkeit geprüft (B1) | F0 |
| **KG-F4** | **Ereignisdatenbank** — Ereignisart, Zeitpunkt, Überraschung, Marktzustand; ⭐ mit Tagesdaten baubar | — |
| **KG-F5** | **Ereignisreaktion** auf den tatsächlich vorhandenen Horizonten: **1 h, 4 h, 1 d, 1 w** — ⚠️ **keine 30-s-, 1-min-, 5-min-Felder**, auch nicht leer | F2, F4 |
| **KG-F6** | **Ähnlichkeitsmaß**, vor seiner ersten Anwendung registriert, samt Gewichtung der sieben Dimensionen | F0, F4 |
| **KG-F7** | **Vergleichsstichproben-Schätzung** statt „Kontrafaktum" — mit ausgewiesener Stichprobengröße und Ausfallhäufigkeit | F6 |
| **KG-F8** | **FDR über registriertes N**, nicht über die Treffer | F0, **QR** |
| **KG-F9** | **Herkunft je Beziehung** (`data_version`, `research_run_id`, Commit, Snapshot-Name) — ⭐ dieselben Felder wie im Register | **QR2** |
| **KG-F10** | **Zerfallsüberwachung**, die zwischen „Abschwächung" und „normaler Schwankung" unterscheiden kann — ⚠️ sonst QR4s Falle | QR4 |
| **KG-F11** | **Alternativerklärungen als Pflichtfeld**, nicht als Bericht: jede behauptende Kante nennt mindestens eine geprüfte Alternative | F1 |
| **KG-F12** | **Kosten je Beziehung** — LLM, Compute, Daten; gemessen ab dem ersten Lauf | QR5 |

⚠️ **Nicht in diesem Epic und bis auf Weiteres gesperrt:** Lead/Lag unter einer
Stunde, Mikrostruktur-Feedback (§7 vollständig), Orderbuch-, Options- und
On-Chain-Auswertung, `execution latency` / `slippage` / `market impact` als
gemessene Größen. **Grund: KG5.**

---

### Nicht verhandelbare Abhängigkeiten

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

### Risiken, nach Schadenshöhe

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

### MVP — und es hat eine Ausgabezahl, nicht zehn

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

## 2x — Epic RT: Autonomous Adversarial Trading Lab

**Einordnung:** eigenes Epic in Abschnitt 7, **direkt hinter AF und vor QR** —
Begründung unter **RT9**, und das ist eine Änderung meiner eigenen Empfehlung
von vor einer Stunde.

*Vermerk TB-59: nach Auftrag `MAC_TB-59` als Block `2x` in Abschnitt 2 eingearbeitet, nicht in Abschnitt 7; Nachtrag (r) nannte keine Nummer — `2x` bei der Einarbeitung als nächste freie nach `2w` gemessen. Die Vorlage liegt im Repo unter `docs/vorlagen/vorlage_rotes_team_2026-09-19.md`.*

---

### RT0 — Was das Konzept richtig macht

| | |
|---|---|
| **§35** | ⭐⭐ die Umkehrung der Frage; die beste Formulierung in allen fünf Einreichungen |
| **§30** | ⭐⭐ *„Eine Verbesserung darf nur akzeptiert werden, wenn sie eine identifizierte Schwäche adressiert"* — damit ist Reparatur an eine **vorher benannte** Schwäche gebunden. Das ist Fables Drei-Kategorien-Regel, auf Strategien angewandt |
| **§28** | ⭐⭐ **den Angreifer bewerten.** Die beste Governance-Idee der fünf Konzepte — und sie fehlt in den anderen vier |
| **§10** | ⭐ *„Synthetic data darf nicht als Beweis für reale Profitabilität verwendet werden"* — richtig, und unvollständig (RT6) |
| **§9** | ⭐ *„Speichere nicht nur einen Backtest-Wert. Speichere eine Verteilung."* |
| **§13** | ⭐ harte, benannte Tests statt eines Gütemaßes |

---

### RT1 — ⚠️⚠️ Fünf der acht Kill Tests sind heute rechenbar. Deshalb müssen sie VOR der Selektion registriert werden

**Was auf dem vorhandenen Bestand ohne neue Daten, ohne LLM und ohne Agenten
rechenbar ist:**

| Kill Test (§13) | rechenbar aus | | gemessen / nicht gemessen *(Spalte aus der Berichtigung vom 19.09.2026, 21:05, Punkt 3)* |
|---|---|---|---|
| **1** Performance verschwindet nach realistischen Kosten | Kostenmodell besteht bereits | ⭐ heute | ⚠️ **nicht gemessen** |
| **3** Performance hängt an einem Jahr | die 7–9 Selektionsfalten je Bot, heute gemessen | ⭐ heute | ⚠️ **nicht gemessen** |
| **4** Performance hängt an einem Asset | 3 bis 149 Symbole je Bot, Zerlegung vorhanden | ⭐ heute | ⚠️ **nicht gemessen** |
| **5** Kleine Parameteränderungen zerstören die Performance | **das Gitter selbst** — N = 653 je Bot ist die Parameternachbarschaft | ⭐ heute | ⚠️ **nicht gemessen** |
| **7** Ohne die besten fünf Trades bricht sie zusammen | Trade-Listen in den neun `paper_trading_*.db` | ⭐ heute | ⚠️ **nicht gemessen** |
| **2** Edge nur in-sample | braucht die OOS-Kette | nach dem Tag | — |
| **6** Ein Marktereignis erklärt die Rendite | braucht die Ereignisdatenbank (Epic KG) | später | — |
| **8** Kleine Ausführungsverzögerung zerstört den Edge | braucht Auflösung unter 1 h (KG5) | gesperrt | — |

⚠️ **Berichtigt 19.09.2026, 21:05** (`BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md`, Punkt 3): *„Fünf der acht Kill Tests sind heute rechenbar"* speist Kill Test 7 aus den Trade-Listen und Kill Test 5 aus dem Parametergitter (N = 653). **Beides ist plausibel und nicht geprüft.** Ob die Datenbanken Trade-Listen in auswertbarer Form enthalten und ob die Gitterergebnisse je Parameterpunkt erhalten sind, ist **nicht nachgesehen** — während der TB-56-Sitzung waren die zwölf Datenbanken mit Quersummen gesichert; eine SQLite-Datei zu öffnen kann `-wal`- und `-shm`-Dateien anlegen und den Vergleich scheitern lassen. **Heute: alle fünf „nicht gemessen".** ⭐⭐ Das schwächt den Hauptbefund von RT1 nicht — es verstärkt ihn: die Regel gilt unabhängig davon, wie viele Tests rechenbar sind. **Was zu messen ist, bevor (r) als belegt gilt** (Berichtigung, Punkt 6): (1) Enthalten die neun `paper_trading_*.db` Trade-Listen mit Einzelergebnissen? — **auf einer Kopie**, nie am Original · (2) Hängt die Performance der vier Trendbots an wenigen Trades, und **stärker als ihre eigene Verteilung erwarten lässt**? — Kopie + Nullmodell · (3) Sind die Gitterergebnisse je Parameterpunkt erhalten (N = 653), oder nur die Sieger? — lesend. **Bis diese drei gemessen sind, trägt die Tabelle den Vermerk „nicht gemessen".**

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

### RT2 — ⚠️ §13 nennt Tests ohne Schwellen. Ein Test ohne Schwelle ist eine Meinung

*„Performance disappears after realistic transaction costs"* — **was heißt
disappears?** Null? Unter dem Zinssatz? Unter dem Buy-and-Hold? Ohne eine vorher
festgelegte Zahl entscheidet nach dem Lauf, wer hinsieht.

⇒ **Jeder Kill Test trägt drei Dinge, bevor er zum ersten Mal läuft:** die
Größe, die er misst · die Schwelle · und **was passiert, wenn sie gerissen
wird** (Status nach §13). ⭐ Das ist die Regel aus TB-55b: *ein Abbruchkriterium
benennt die Sache, nie ihren Stellvertreter.*

---

### RT3 — ⚠️⚠️ KILL TEST 7 ist so, wie er dasteht, statistisch falsch — und er würde vier unserer neun Bots erschlagen

**§13 KILL TEST 7 / §14:** *„Removing top 5 trades destroys the strategy."*

⚠️ **Das zerstört die Performance **jeder** Strategie mit rechtsschiefer
Renditeverteilung** — und bei Trendfolge ist es **definitorisch**: Trendfolge
verdient ihren gesamten Erwartungswert aus wenigen großen Gewinnern. *„Vier der neun Bots sind nach
ihrer Bauart Trendfolger; ob ihre Performance an wenigen Trades hängt, ist
**nicht gemessen**. Der Einwand gegen KILL TEST 7 gilt unabhängig davon, weil er
aus der Form rechtsschiefer Renditeverteilungen folgt und nicht aus diesen
Bots."*

⚠️ **Berichtigt 19.09.2026, 21:05** (`BACKLOG_NACHTRAG_2026-09-19q_r_berichtigung.md`, Punkt 2): Im Nachtrag (r) stand hier *„Vier der neun Bots sind Breakout- oder Trendbots (`volatility_breakout`, `volatility_breakout_crypto`, `turtle_soup_*`). Wörtlich angewandt fällt jeder davon durch — nicht wegen eines Defekts, sondern wegen seiner Bauart."* — **aus den Bot-Namen erschlossen, nicht aus den Renditeverteilungen gemessen**; die Trade-Listen der neun `paper_trading_*.db` wurden nicht angesehen (gesicherte Datenbanken während der Mac-Sitzung). Der Satz oben ist die von der Berichtigung vorgegebene Ersatzfassung. ⚠️ *Die Überschrift dieses Punktes („er würde vier unserer neun Bots erschlagen") und Risiko 3 unten tragen dieselbe ungemessene Behauptung; sie stehen wörtlich, wie im Nachtrag, und gelten mit diesem Vermerk (A1: ein fehlgeschlagener Nachweis und ein leeres Ergebnis sehen gleich aus).*

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

### RT4 — ⚠️ §8 und §9: der Bootstrap zerstört genau das, was die Strategie ausmacht

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

### RT5 — ⚠️⚠️ §18: sieben Kennzahlen ohne Gewichte sind sieben Freiheitsgrade

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

### RT6 — ⚠️⚠️ §11 hat kein Abbruchkriterium und kein Nullmodell. So gebaut zerstört es jede Strategie

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

### RT7 — ⭐⭐ §28 ist die beste Idee der fünf Konzepte, und sie ist heute umsetzbar

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

### RT8 — Überschneidung: ein Drittel ist neu, zwei Drittel stehen schon woanders

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

### RT9 — ⚠️ Ich ändere meine Reihenfolge von vor einer Stunde

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

### Merkmale (Features) — RT-F0 bis RT-F11

*Vermerk TB-59: die erste Spalte trägt das Präfix `RT-`, wie die Überschrift es nennt — im Nachtrag (r) stand dort `F0` bis `F11`; `F1` bis `F20` sind in dieser Datei bereits als Zeilenkennungen vergeben (Abschnitt 4, Block 2m). Verweise im Text („F0 + F1") sind wörtlich belassen und meinen die Zeilen dieser Tabelle. Betreiberentscheidung 19.09.2026.*

| | Merkmal | Vorbedingung |
|---|---|---|
| **RT-F0** | ⭐⭐ **Kaputt-Strategien-Sammlung**: mindestens drei absichtlich defekte Strategien (Look-ahead, Ein-Jahr-Edge, Ein-Symbol-Edge) | — |
| **RT-F1** | ⭐⭐ **Bissprüfung je Angriff** gegen F0 — kein Angriff läuft an einer echten Strategie, bevor er auf einer kaputten gefeuert hat | F0 |
| **RT-F2** | **Registrierung eines Angriffslaufs**: welche Angriffe, welche Schwellen, welche Strategieversion, welcher Datenstand — vor dem Lauf | — |
| **RT-F3** | **Kill Tests 1, 3, 4, 5 mit Schwellen** — die vier heute rechenbaren ohne Nullmodellbedarf | F2 |
| **RT-F4** | **Kill Test 7 / §14 mit Nullmodell** (RT3) — Abhängigkeit gegen Verteilungserwartung, nicht gegen Null | F2 |
| **RT-F5** | **Parameterstabilitätskarten** aus dem **vorhandenen** Gitter (N = 653), nicht aus neuen Läufen | F2 |
| **RT-F6** | **Zeit- und Regimezerlegung** je Bot auf den gemessenen 7–9 Falten | F2 |
| **RT-F7** | **Block-Bootstrap mit registrierter Blocklänge**; `shuffle` nur als benannte Vergleichsgröße | F2 |
| **RT-F8** | **Drawdown-Zerlegung** — Start, Dauer, Tiefe, Erholung je Drawdown; ⚠️ **ohne KI-Erklärung** in Fassung 1 | — |
| **RT-F9** | **Failure-Mode-Register** mit Verknüpfung Strategie ↔ Fehlermodus | F3, F4 |
| **RT-F10** | **Angreiferbewertung**: Redundanz und Bissquote je Angriffsart | F1 |
| **RT-F11** | **Schwellen statt Gewichte** für die Gesamtbeurteilung (RT5) — jede Kennzahl mit eigener registrierter Schwelle | F2 |

⚠️ **Ausdrücklich V2, nicht MVP:** §10 synthetische Szenarien · §11 erzeugte
Märkte (RT6) · §17 Repair Agent · §18 adversariale Evolution · §19 Immune
System · KI-Erklärungen für Drawdowns.

---

### Nicht verhandelbare Abhängigkeiten

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

### Risiken, nach Schadenshöhe

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

### MVP — und es hat eine Ausgabezahl

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

## 2y — Querschnitt über die fünf Epic-Nachträge (n) bis (r) — TB-59 (19.09.2026)

*Zwei Befunde, die über die fünf Konzepte hinweg feststehen (Auftrag `MAC_TB-59`, Abschnitt 5), als zwei Punkte mit Verweisen; die fünf Sichtungsdurchgänge sind nicht vollständig gemacht. Nummer `2y` bei der Einarbeitung als nächste freie nach `2x` gemessen.*

| # | Punkt |
|---|---|
| **QS1** | ⭐ **DIE ZERFALLSFALLE STECKT IN VIER DER FÜNF KONZEPTE** — „Edge Decay" (Block 2v, QR4 und QR-F8), „Relationship Decay" (Block 2w, KG8 §15 und KG-F10), „Live Shadow Red Team" (Block 2x, RT8 §20) und „Self-Healing Pool" (Block 2v, QR-F12; Block 2x, RT8 §19/§21): Abschwächung ist auf einem Random Walk normal, und wer daraufhin abschaltet, verkauft die Verlierer auf einem Zufallspfad. ⚠️ **Registerabschnitt 22.3 hat sie bereits entschieden:** Abschalt- und Zuschaltregeln sind **Overlay-Kandidaten nach dem Tag, keine Betriebsentscheidungen** — und der „Self-Healing Pool" ist mit Registertext **6d unvereinbar** (Block 2s, T56b.15) |
| **QS2** | ⭐ **DAS REGISTER KOMMT IN FÜNF VON FÜNF KONZEPTEN VOR, unter fünf Namen:** Prediction Ledger (Block 2v, QR2), Data Lineage (Block 2w, KG8 §24), Research Ledger (Block 2x, RT8 §27), Hypothesis Registry (Block 2w, KG8 §9), Versuchsregister / Strategy Registry (Block 2t, AF4). *Es ist nicht ein Baustein von mehreren; es ist der Baustein, auf dem alle fünf stehen* (RT8). ⚠️ **Registerabschnitt 22.1 trägt den Baustein inzwischen als allgemeine Prüfregel** (Block 2s, T56b.9) |
| **QS3** | ⚠️ **OFFEN: drei der fünf Sichtungsdurchgänge sind nicht gemacht** — Kollision und Widerspruch sind mit QS1/QS2 und der Nummernvergabe in TB-59 abgedeckt; **Abhängigkeit, Ausscheiden und Kette** stehen aus (QR8; Kettenzeile 0,97). Nicht stillschweigend ausgelassen, sondern hier eingetragen |

