# Backlog-Nachtrag 19.09.2026 (p) — Epic: Alpha-Discovery-Labor

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(o) voraus.** Einzufügen als **Block 2v**, nach Block 2u.
⭐ **Keine konkreten Kettennummern genannt** (K2i).

**Vorlage:** Betreiberdokument *„AI Quant Research OS / Alpha Discovery Lab"*,
eingereicht 19.09.2026. ⚠️ **Zur Aufnahme, nicht zur Umsetzung.**

---

### 2v — Epic QR: Alpha-Discovery-Labor

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

---

## Neue Kettenzeilen

```
| ⟨frei⟩ | ⚠️ **Epic QR — Alpha-Discovery-Labor.** ⚠️⚠️ **Geparkt hinter Epic AF, das hinter dem Tag geparkt ist** (QR0/QR6) | geparkt |
| ⟨frei⟩ | ⭐ **Backlog-Sichtung in fünf Durchgängen für (n), (o), (p)** — Kollision, Abhängigkeit, Widerspruch, Ausscheiden, Kette. ⚠️ **Rein lesend, gemessen am Backlog** (QR8) | offen |
```

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K2y** | ⭐⭐ **Wer behauptet, etwas sei besser als Zufall, baut das Zufallsmodell mit** — und schickt es durch dieselbe Prüfung (QR1) |
| **K2z** | ⚠️⚠️ **Gespeichert ist nicht unverändert.** Eine Aufzeichnung, die Nachträglichkeit ausschliessen soll, braucht **Anfügen und Verkettung**, nicht nur Felder (QR2) |
| **K3a** | ⭐ **Eine Prognose ohne vorher festgelegte Auflösungsregel ist nicht auswertbar** (QR3) |
| **K3b** | ⚠️ **Eine Abschaltregel ist selbst eine Strategie** und wird wie eine getestet (QR4) |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **entfernte
   Zeilen: 0.**
2. ⭐ **Vergebene Kettennummern im Bericht nennen**, mit der Messung.
3. ⚠️ **Die Vorlage ins Repo**, als `docs/vorlagen/2026-09-19_alpha_labor.md`.
