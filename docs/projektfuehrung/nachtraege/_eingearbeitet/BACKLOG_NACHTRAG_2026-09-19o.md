# Backlog-Nachtrag 19.09.2026 (o) — Epic: KI-Marktverständnis und adaptive Allokation

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(n) voraus.** Einzufügen als **Block 2u**, nach Block 2t.
⭐ **Keine konkreten Kettennummern genannt** (K2i).

**Vorlage:** Betreiberdokument *„AI Market Intelligence & Adaptive Strategy
Allocation"*, eingereicht 19.09.2026. ⚠️ **Zur Aufnahme, nicht zur Umsetzung.**

---

### 2u — Epic MI: KI-Marktverständnis und adaptive Allokation

| # | Punkt |
|---|---|
| **MI0** | ⭐⭐ **AUFGENOMMEN, GEPARKT — und zwar HINTER Epic AF.** ⚠️ **Der Allokator setzt einen Pool von 100–1 000 validierten Strategien voraus. Wir haben neun, und der Selektionslauf hat nicht stattgefunden.** ⭐ **Ohne Pool hat der Allokator nichts zu verteilen** — das ist keine Priorisierung, sondern eine Abhängigkeit |
| **MI1** | ⭐⭐ **WAS DIE VORLAGE RICHTIG ENTSCHEIDET, und es ist mehr als beim ersten Konzept.** *(a)* **Das LLM erzeugt einen strukturierten Zustand, keine Order** — deterministische Modelle entscheiden. *(b)* *„Ein LLM-generierter Text darf nicht als alleinige Begründung für eine Kapitalentscheidung dienen."* *(c)* **Die Risk Engine ist LLM-fest.** *(d)* **Shadow Mode vor jedem Einsatz.** ⭐ **Alle vier decken sich mit den stehenden Regeln dieses Projekts** |
| **MI2** | ⚠️⚠️ **DER STRUKTURELLE HAUPTBEFUND: Regime-bedingte Kennzahlen vervielfachen den Suchraum und zerlegen die Stichprobe.** Abschnitt 10 will je Strategie **eine Kennzahl je Regime** (`TREND_HIGH_VOL: 2.1`, `PANIC: −0.8`). ⚠️ **Wie viele PANIC-Episoden gibt es in den Daten? Eine Handvoll.** Bei 9 Regimen × 100 Strategien sind es **900 Zellen**, die meisten fast ohne Daten — ⭐⭐ **und es wird auf ihnen ausgewählt.** **Das ist Mehrfachtesten (K2r), nur gefährlicher: die Zellen sehen aus wie Wissen, nicht wie eine Suche** |
| **MI3** | ⚠️⚠️ **VINTAGE-DATEN SIND EINE HARTE VORBEDINGUNG, KEIN PRÜFPUNKT.** Abschnitt 19 nennt *„revised macro data"* und *„delayed news"* in einer Aufzählung. ⭐ **Die Folge ist härter, als die Aufzählung nahelegt:** Makrodaten werden **nachträglich revidiert**; wer mit der revidierten Reihe backtestet, hat **Look-ahead per Konstruktion** — nicht abgeschwächt, sondern ungültig. **Dasselbe für Nachrichten:** der Zeitpunkt, zu dem eine Meldung **handelbar** war, ist nicht ihr Veröffentlichungsstempel. ⇒ ⚠️ **Ohne Daten „wie damals erstveröffentlicht" ist der Backtest des KI-Layers wertlos. Das ist eine Architekturentscheidung, die VOR allem anderen fällt** |
| **MI4** | ⚠️ **MARKET MEMORY IST EIN AUSWAHLVERFAHREN IN VERKLEIDUNG.** Abschnitt 7 sucht ähnliche historische Episoden und fragt, was danach funktionierte. ⭐ **Bei reichem Merkmalsraum und wenigen Episoden sieht immer irgendetwas ähnlich aus** — und **das Ähnlichkeitsmass ist selbst ein frei gewählter Parameter**. ⇒ **Das Mass wird vor der Benutzung registriert, und die Zahl der Vergleiche wird gezählt** (K2r) |
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

---

## Neue Kettenzeilen

```
| ⟨frei⟩ | ⚠️ **Epic MI — KI-Marktverständnis und adaptive Allokation.** ⚠️⚠️ **Geparkt hinter Epic AF, das hinter dem Tag geparkt ist** (MI0) | geparkt |
| ⟨frei⟩ | ⭐ **MI-F0 / MI-T0.1 — Vintage-Datenlage erheben** (MI3). ⚠️ Rein lesende Recherche, ortsunabhängig. **Entscheidet, ob der KI-Layer überhaupt testbar ist** | offen |
```

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K2u** | ⚠️⚠️ **Eine Kennzahl je Regime ist eine Kennzahl auf einer Teilstichprobe.** ⭐ **Vor jeder regimebedingten Aussage wird die Zahl der Episoden im Regime gemessen und genannt** (MI2) |
| **K2v** | ⚠️⚠️ **Revidierte Daten sind Look-ahead.** Makroreihen und Nachrichten nur „wie damals erstveröffentlicht" — sonst gar nicht (MI3) |
| **K2w** | ⭐ **Ein Ähnlichkeitsmass ist ein Parameter.** Vor Benutzung registrieren, Vergleiche zählen (MI4) |
| **K2x** | ⭐ **Wer Kapital zwischen Strategien verteilt, betreibt selbst eine Strategie** — dieselben Regeln, dieselbe Registrierung (MI5) |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **entfernte
   Zeilen: 0.**
2. ⭐ **Vergebene Kettennummern im Bericht nennen**, mit der Messung.
3. ⚠️ **Die Vorlage ins Repo**, als
   `docs/vorlagen/2026-09-19_marktverstaendnis.md`.
