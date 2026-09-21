# Backlog-Nachtrag 19.09.2026 (n) — Epic: Autonome Strategie-Forschungspipeline

**Nachzutragen in `docs/projektfuehrung/BACKLOG.md`.**
⚠️ **Setzt (a)–(m) voraus.** Einzufügen als **Block 2t**, nach Block 2s.
⭐ **Keine konkreten Kettennummern genannt** (K2i) — die vergibt die
ausführende Sitzung nach Messung.

**Vorlage:** Betreiberdokument *„Autonomous Trading Strategy Research & Bot
Evolution Pipeline"*, eingereicht 19.09.2026. ⚠️ **Ausdrücklich zur Aufnahme in
den Backlog, nicht zur Umsetzung.**

---

### 2t — Epic AF: Autonome Strategie-Forschungspipeline

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

---

## Neue Kettenzeilen

⭐ **Die nächsten freien Nummern, gemessen:**

```
| ⟨frei⟩ | ⭐ **AF-F0 — Bestandsaufnahme der Codebasis** gegen Abschnitt 13 der Vorlage. **Rein lesend, ortsunabhängig, ohne Sitzung.** ⚠️ Vor jeder Feature-Struktur | offen |
| ⟨frei⟩ | ⚠️ **Epic AF — autonome Forschungspipeline.** ⚠️⚠️ **Geparkt bis nach dem signierten Tag** (AF0) | geparkt |
```

---

## Ergänzungen zu Abschnitt 4 („Laufend, klein")

| # | Punkt |
|---|---|
| **K2r** | ⭐⭐ **Mehrfachtesten ist eine Eigenschaft der Suche, nicht des Kandidaten.** Wer viele Varianten prüft, muss **zählen**, wie viele — sonst ist keine Kennzahl am Ende deutbar. ⚠️ **Gilt auch für uns heute:** jede verworfene Parametervariante zählt |
| **K2s** | ⚠️ **Schwellen werden vor dem Lauf registriert, nicht nach den Ergebnissen abgeleitet** (AF3) |
| **K2t** | ⭐ **Eine Vorlage von aussen wird gegen das Register gemessen, bevor sie in den Backlog geht** — nicht danach |

---

## Zum Schluss: was nach dem Einfügen zu prüfen ist

1. `git diff --numstat docs/projektfuehrung/BACKLOG.md` — ⚠️ **entfernte
   Zeilen: 0.** Dieser Nachtrag fügt nur ein.
2. ⭐ **Welche Kettennummern vergeben wurden, steht im Bericht** — mit der
   Messung, wie sie ermittelt wurden.
3. ⚠️ **Die Vorlage selbst gehört ins Repo**, als
   `docs/vorlagen/2026-09-19_forschungspipeline.md` — *ein Beleg in einem
   Anhang ist kein Beleg* (T54.5).
