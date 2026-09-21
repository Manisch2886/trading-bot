# TB-77 Der Datenhorizont wird eine Zahl je Bot — und zwei Stellen, an die heute niemand fassen darf

**an: Claude Code am Mac (lokale Sitzung)**

**Sitzungstitel für Claude Code: `TB-77 Horizont je Bot`**
**Modell: Opus 5, Aufwand hoch.**

Repo: `Manisch2886/trading-bot`, direkt auf `main`.

⭐ **Rechnet nicht.** ⛔ **Fasst keinen Bot-Code an.** Registertext plus zwei
gemessene Befunde.

---

## 0. Warum es diese Aufgabe gibt

**Fable hat am 21.09. entschieden** (`FABLE_ANTWORT_2026-09-21a_horizont_und_grenzfall.md`):

> **4a, Präzisierung (ersetzt die Fassung vom 20.09.).** Der Datenhorizont eines
> Bots ist ein absolutes Datum je Bot: Horizontbeginn = `asof` (5a) minus
> `RECENT_YEARS_ONLY` des Bots; Bots ohne diese Konstante haben keinen Horizont
> (Krypto). Das Datum steht je Bot in der Tatsachennotiz zu 4d. Es gilt für alle
> Symbole des Bots gleich; ein Symbol trägt vor dem Horizontbeginn keinen
> Einstieg bei, unabhängig davon, wann seine Kursdatei beginnt oder endet. Das
> Ende der Kursdatei eines Symbols bestimmt nach 3b (b), an welchen Tagen es
> handelbar ist — nie sein Fenster.

⭐⭐ **Sein Grund, und er ist der eigentliche Befund:** Ein Symbol mit früherem
Fenster erzeugt Trades aus Jahren **vor der ersten Falte**. Die tauchen in keiner
Falte auf — *„aber sie laufen durch den Kapitalpfad, belegen Plätze, verändern
das Kapital, mit dem die erste Falte beginnt. Das ist ein Lesezugriff auf Zeiten
ausserhalb des registrierten Horizonts, nur nicht über eine Datei, sondern über
ein Fenster. Der Lese-Audit (5e) sieht ihn nicht, weil die Datei im Manifest
steht."*

---

## 1. ⛔ Zwei Blocker, im Chat gemessen — nachprüfen, nicht übernehmen

**Fable schlägt zwei Dinge vor, die heute nicht ausführbar sind.** Beide sind am
21.09. um 16:25 gemessen worden; ⚠️ **miss sie selbst nach und sag, ob du
dasselbe findest.**

| | Fables Vorschlag | gemessen |
|---|---|---|
| **A** | Horizontbeginn `= asof − RECENT_YEARS_ONLY` | ⛔ **`asof` ist nirgends als Wert gesetzt.** `grep` über alle `.py` und `.json`: die einzigen Treffer sind `pd.merge_asof`, etwas anderes. Register 16.3: *„Das Bezugsdatum des Laufs (`asof`) kommt aus dem Register, nie aus der Uhr"* — **aber es steht dort keine Zahl** |
| **B** | *„Eine Wache, billig, in den Auswerter"* | ⛔ **`auswertung.py` ist eingefroren** — Register Z. 31 nennt die Datei namentlich; ihre Umstellung ist **TB-30b** |

⭐⭐ **Daraus folgt der Schnitt dieser Aufgabe:**

| | |
|---|---|
| ✅ **jetzt** | Der **Registertext**. Er ist eine Regel und braucht keinen Wert |
| ⛔ **nicht jetzt** | Die **Tatsachennotiz zu 4d mit absoluten Daten** — ohne `asof` gibt es kein Datum. **Ein Platzhalter, sichtbar, wie in Abschnitt 23.3** |
| ⛔ **nicht jetzt** | Die **vier Optimierer** — sie brauchen denselben Wert |
| ⛔ **nicht jetzt** | Die **Wache** — eingefrorene Datei |

⚠️ *Ein Registertext, der auf einen Wert zeigt, den es nicht gibt, ist kein
Fehler — solange er sagt, dass es ihn nicht gibt.* **Genau das ist zu tun.**

---

## 2. Die Schritte

### Schritt 0 — vor allem anderen

**Committe, was im Arbeitsbaum liegt**, getrennt nach Urheber.

### Schritt 1 — die beiden Blocker nachmessen

**A:** Gibt es `asof` irgendwo als Wert — im Register, im Code, in einer
`ergebnisse/`-Datei, in einem Snapshot-Manifest? **Nenne, wo du gesucht hast.**
**B:** Ist `auswertung.py` eingefroren, und wo steht das?

⚠️ **Findest du `asof` doch**, ändert das den Schnitt — dann sag es, **bevor** du
weiterschreibst.

**Sichern: commit und push.**

### Schritt 2 — Registerabschnitt 26

| | Inhalt |
|---|---|
| **26.1** | Der Befund: Fenster je Symbol erzeugt Einstiege ausserhalb aller Falten, die durch den Kapitalpfad laufen. **Fables Begründung wörtlich**, mit den Fundstellen aus der Anfrage (`multi_symbol_optimise.py` Z. 54/52/46/49 und 93/93/81/88; `faltenplan_neun.py::fensteranker` Z. 271–278) |
| **26.2** | **Der Registertext**, zeichengleich aus Abschnitt 0 oben. ⭐ **Er ersetzt die Fassung vom 20.09.**, die in `FABLE_ANTWORT_2026-09-20e_konjunktion.md` steht und **in keinen Registertext übernommen wurde** — prüfe das und sag es |
| **26.3** | ⚠️ **Der Platzhalter:** die Tatsachennotiz zu 4d bekommt **keine** Daten, weil `asof` nicht gesetzt ist. Sichtbar, nach dem Muster von 23.3 |
| **26.4** | Die Ergänzung zu **3c**: *„Der Survivorship-Vorbehalt gilt für die Jahre im Horizont; dass der Horizont zehn Jahre umfasst, begrenzt die Reichweite des Vorbehalts, ändert ihn nicht"* |
| **26.5** | Die **Tatsachennotiz zur Herkunft**: alle bisherigen Ergebnisdateien der vier Aktien-Bots wurden mit Fenstern **je Symbol** gerechnet — ein Grund mehr, warum sie mit den Zahlen des Laufs nicht vergleichbar sind |
| **26.6** | ⛔ **Was folgen muss und hier nicht getan wird:** `asof` setzen · Tatsachennotiz 4d füllen · die vier Optimierer (`entry_cutoff` einmal je Bot aus dem Register statt je Symbol aus `df["open_time"].max()`) · die Wache *„kein Einstieg vor Horizontbeginn"* samt Mutationsprobe (per-Symbol-Fenster wieder einschalten) — **beide letzten gehören zu TB-30b** |

⛔ **Append-only**, `numstat` Spalte zwei = **0**.

⚠️⚠️ **Zwei Aktenzeichen aus Fables Antwort sind falsch und dürfen nicht
übernommen werden** — im Chat gemessen, **prüfe es nach**:

| Fable sagt | richtig ist |
|---|---|
| „Festlegung 10 lässt Bleibt/Geht über die Abbruchkriterien laufen" | **Festlegung 11** (10 ist die DSR-Basis, N = 653) |
| „Festlegung 11 deckt ‚mehrere oder alle'" | **Festlegung 12** |

**Sichern: commit und push.**

### Schritt 3 — der Grenzfall gehört auch ins Register

**Fables Teil 2 ist entschieden und steht nirgends im Register:** Abbruchkriterium
**(b)** → **Schatten** (Registertext 6b), Budget in die statische
Benchmark-Position, heutige Parameter nur als Schatten, Rückkehr über einen
**neuen registrierten Lauf**.

⭐ **Das ist ein Verweis, keine Berichtigung** — (b) steht bereits in Abschnitt 7,
6b bereits in 16.x. **Prüfe beides nach** und schreib einen kurzen Abschnitt
**26.7**, der die Kette benennt: (b) → Festlegung 11 → Registertext 6b → Schatten.

⚠️ **Fable verweist auf ein Dokument `FABLE_ANTWORT_2026-09-20a_grenzfall`, das
im Repo nicht existiert** (gemessen 21.09., 13:50). ⛔ **Zitiere es nicht.**
**Quelle ist seine Kurzfassung vom 21.09.** — und das steht so da.

⭐ **Und eine Berichtigung zu 24.6:** Fable stellt klar, *„der Snapshot enthält
Krypto 2018–2020, die Nebenbedingung wird dort gerechnet"*. Die Lücke aus 24.6
betrifft **nur die TB-24-Trade-Listen** der Messung, **nicht den Lauf**. **Als
Nachtragszeile unter 24.6**, append-only.

**Sichern: commit und push.**

### Schritt 4 — der Journalblock und die Abgabe

⭐ **Block DIREKT ins Journal**, Buchstabe gemessen, Quellenzeile auf das eigene
Ergebnisdokument.

`docs/ERGEBNIS_TB-77_horizont_je_bot.md` und **eine** Backlog-Zeile in
Abschnitt 4 (K-Nummer selbst gemessen, Muster `^\| \*\*(K\d[a-z])\*\*` **ohne
schliessenden Balken**, **kein `sort -u`**, über `BACKLOG.md`,
`BACKLOG_ARCHIV.md` **und `BACKLOG_EPICS.md`**).

**Sichern: commit und push.**

---

## 3. Die Nachweise

| # | Nachweis |
|---:|---|
| **1** | `git status --short` vor dem ersten Schreiben |
| **2** | ⭐⭐ Schritt 1: **wo überall nach `asof` gesucht wurde**, und das Ergebnis je Ort |
| **3** | `auswertung.py` eingefroren — Fundstelle |
| **4** | ⭐ Die beiden Festlegungsnummern, **selbst nachgemessen** an `registerdaten.FESTLEGUNGEN` und der Registertabelle |
| **5** | Abbruchkriterium (b) und Registertext 6b: Fundstelle je Zeile |
| **6** | ⭐ Ob die 4a-Fassung vom 20.09. je in einen Registertext kam — **Trefferzahl, auch wenn null** (`A1`) |
| **7** | Register: `numstat` Spalte zwei = **0** |
| **8** | SHA-256 von `benchmark_drawdowns.json` (`a163c498…`) und `faltenplan.json` (`0e54ac5c…`) — unverändert |
| **9** | `git diff --numstat` je Datei; **nichts ausserhalb `docs/`** |

---

## 4. Die harten Auflagen

| | |
|---|---|
| ⛔ | **Kein Bot-Code.** Die vier `multi_symbol_optimise.py` bleiben unberührt |
| ⛔ | **`auswertung.py` bleibt eingefroren** — auch der Docstring |
| ⛔ | **Kein erfundenes `asof`.** Wo ein Datum stehen müsste, steht ein sichtbarer Platzhalter |
| ⛔ | **Fables falsche Aktenzeichen nicht übernehmen** |
| ⛔ | **Das fehlende Dokument nicht zitieren** |
| ⭐ | **Sichern nach jedem fertigen Teil** |
| ⚠️ | **`git push` steht allein, nie in einem `&&`-Block** |
| ⚠️ | **Widersprich diesem Auftrag, wo er falsch ist.** ⭐ *Die letzten zwölf Aufträge lagen je an mehreren Stellen daneben — zuletzt TB-69, das nachgewiesen hat, dass 6d die Form seit dem 20.09. sehr wohl nennt und mein Abschnitt 0 sie zu Unrecht als fehlend führte* |

---

## In einfacher Sprache

**Was entschieden ist:** Die „letzten zehn Jahre", auf die ein Bot schaut, gelten
künftig für den ganzen Bot — nicht für jedes Wertpapier einzeln. Sonst handelt
er in Jahren, die offiziell gar nicht ausgewertet werden, und verändert damit
still das Startkapital des ersten Jahres.

**Was dabei auffällt:** Die Regel braucht ein Stichtagsdatum, das es noch nicht
gibt. Und die Wache, die sie überwachen soll, gehört in eine Datei, die
eingefroren ist.

**Was diese Aufgabe deshalb tut:** Sie schreibt die Regel auf — und sagt
ausdrücklich, was fehlt, statt eine Zahl zu erfinden. Der Rest folgt, wenn der
Stichtag steht.
