# Übergabe: die Zielfunktion von Agent 2 (TB-22)

**Stand: 2026-09-13** · Branch `claude/new-session-auanhb`, Base `main` (`0f39e3b`).
**Es wurde nichts automatisch geändert, keine `live_params.py` angefasst, kein
Parameter übernommen, keine Ergebnisdatei überschrieben.**

---

## 1. Erst der Befund: wie Agent 2 heute zu seiner Rangfolge kommt

Das war ausdrücklich vor der Änderung festzustellen. Die vier Fragen, in der
Reihenfolge der Aufgabenstellung:

### Woher bezieht er seine Rangfolge?

**Weder aus einer abgelegten CSV noch aus einem eigenen `multi_symbol_optimise`-
Aufruf.** `run_agent_search(evaluate_fn, …)` bekommt eine **Funktion**
hereingereicht und ruft sie je Kombination auf. Alle sechs Aufrufer führen zur
selben Stelle:

| Aufrufer | Bots | Weg |
|---|---|---|
| `agent_optimise.py` | `elliott_wave`, `elliott_wave_stocks`, `t3_supertrend` | `evaluate_combination_multi(all_data, …)` direkt |
| `quarterly_review.py` | dieselben drei | `evaluate_params()` → `evaluate_combination_multi(…)` |

`results/<bot>/multi_symbol_optimisation_results.csv` wird dabei **nicht
gelesen**. Die Zahlen entstehen bei jedem Lauf neu.

### Welche Felder gehen in seinen Prompt ein?

**Alle.** `format_history()` macht `pd.DataFrame(history).to_string(index=False)`
— es gibt keine Auswahl. Das Modell sieht also seit PR #90 auch
`max_drawdown_chronologisch_pct`; es stand nur nirgends, was damit anzufangen
wäre. Der System-Prompt sagte bis TB-22 lediglich „auch … Max Drawdown (kleiner
= robuster)", ohne zu benennen, **welcher** der beiden gemeint ist.

### Sortiert er selbst, oder lässt er das Modell sortieren?

**Beides — an zwei getrennten Stellen, und das ist der Kern des Befunds:**

1. **Die Auswahl trifft Code, nicht das Modell.** Am Ende von
   `run_agent_search` stand
   `max(valid_results, key=lambda r: r["robustness_score"])`. Was das Modell
   vorschlägt, beeinflusst nur, *welche* Kombinationen überhaupt getestet
   werden — wer von den getesteten gewinnt, entscheidet allein diese Zeile.
2. **Die Suchrichtung steuert das Modell**, anhand der Tabelle und der
   Prompt-Anweisung.

Eine Umstellung nur an einer der beiden Stellen hätte Prompt und Auswahl
auseinanderlaufen lassen. Beide sind umgestellt, und beide beziehen den
Feldnamen jetzt aus **derselben Konstante**.

### Gibt es abgelegte Vorschläge aus früheren Läufen?

**Nein — im Repo liegt keine einzige.** Gesucht wurde in `results/**`,
`docs/**`, `logs/**` und über alle je hinzugefügten Dateinamen der Git-Historie.
Der Grund ist strukturell: `run_agent_search` gibt sein Ergebnis nur zurück,
`agent_optimise.py` **druckt** es, `quarterly_review.py` verschickt es per
Telegram. Keiner der drei schreibt eine Datei.

**Eine Einschränkung, die dazugehört:** Der Quartals-Cronjob leitet seine
Ausgabe in eine Logdatei um (`>> <log-pfad> 2>&1`, Protokoll Abschnitt 6.4).
`logs/` ist in `.gitignore` und in einem frischen Klon leer — auf dem Rechner
des Nutzers können dort also sehr wohl Vorschläge auf dem alten Maß stehen,
ebenso in den Telegram-Verläufen. **Beides ist nicht zu löschen.** Ab jetzt
trägt jeder neue Eintrag die Zielgrößen-Angabe und ist damit von den älteren
unterscheidbar.

Was **doch** auf dem alten Maß beruht und nicht gelöscht werden darf:

| Datei | Was daran auf dem alten Maß beruht |
|---|---|
| `results/<bot>/multi_symbol_optimisation_results.csv` (8 Dateien) | die abgelegte Rangfolge der **Rastersuche** — Beleg dafür, worauf frühere Parameterentscheidungen standen |
| `research/**/results/*.csv` | Rasterergebnisse der Untersuchungen |
| Telegram-Verläufe früherer Quartals-Reviews | liegen beim Nutzer, nicht im Repo |
| `logs/<bot>/…` auf dem Rechner des Nutzers | Ausgabe früherer Quartals-Läufe (gitignored, im Klon leer) |

**Nichts davon wurde angefasst.** Der Selbsttest weist per `git status` nach,
dass ein Testlauf im Repo nichts verändert.

---

## 2. Wo die Änderung greift

Genau zwei Stellen in `shared/param_search_agent.py`, plus die Ausgabe:

| Stelle | vorher | nachher |
|---|---|---|
| Auswahl (`max(...)`) | `robustness_score` | `robustness_score_chronologisch` |
| Prompt (User-Nachricht) | die Tabelle, ohne Angabe des Maßes | zusätzlich ein Abschnitt **„ZIELGROESSE DER AUSWAHL"**, der das Feld benennt und sagt, dass das Blockmaß *nicht* das Kriterium ist |
| Ausgabe | — | `zielmass_zeile()` — ein fest verdrahteter Satz, der beide Zahlen nennt und sagt, welche galt |

`robustness_score_chronologisch` wird **in `param_search_agent.py`** aus den
vorhandenen Spalten gerechnet:

```
avg_return_pct × √num_trades ÷ |max_drawdown_chronologisch_pct|
```

Zeichengleich zu `multi_symbol_optimise.calculate_robustness_score`, bis auf den
Drawdown im Nenner (inklusive der Sonderbehandlung `|0| → 1.0` und der Rundung
auf drei Stellen).

---

## 3. Die Entscheidung, die zu treffen und zu begründen war

Die Aufgabe stellte zwei Varianten zur Wahl: den Score **neu rechnen**
(eindeutig) oder dem Agenten **beide Werte zeigen** und im Prompt vorgeben,
welcher gilt (transparent).

**Umgesetzt sind beide — und zwar nicht als Kompromiss, sondern weil sie
verschiedene Stellen betreffen.** Die Auswahl trifft Code, die Suchrichtung
steuert das Modell (siehe Befund oben). Hätte man nur den Score neu gerechnet,
suchte das Modell weiter auf dem alten Maß, weil der Prompt nichts anderes
sagte. Hätte man nur den Prompt geändert, wählte `max(...)` weiter nach dem
alten Score — eine Anweisung, der die Mechanik widerspricht. Beides zusammen ist
die einzige Kombination, bei der Prompt und Auswahl dasselbe meinen.

Damit sie das auch bleiben, steht der Feldname **nicht zweimal** da: Rechnung,
Prompt und Ausgabe beziehen ihn aus `FELD_SCORE_CHRONO`. In diesem Repo sind
doppelt geführte Zahlen schon einmal unbemerkt auseinandergelaufen (Protokoll,
Abschnitt 7).

Der Zugewinn der zweiten Variante bleibt erhalten: beide Zahlen stehen weiter in
der Tabelle, und der Prompt erklärt, **warum** die eine gilt. Ein Modell, das
das sieht, kann in seiner Begründung darauf eingehen — was bei Vorschlägen, die
ohnehin als unvalidiert gekennzeichnet werden, etwas wert ist.

**Warum nicht in `multi_symbol_optimise.py`:** Die Datei ist in der Aufgabe
ausdrücklich ausgenommen, und das aus gutem Grund — eine zweite Score-Spalte
dort landete in jeder Rasterausgabe und jeder `results/*.csv` und wäre genau die
Einladung, nach ihr zu sortieren, die TB-18 bewusst vermieden hat. Die
Rastersuche behält ihr Maß; geändert hat sich **nur**, worauf Agent 2 schaut.

---

## 4. Die harte Randbedingung

> **Der Agent ändert weiterhin nichts automatisch.**

Unverändert in Kraft:

* Der Unvalidiert-Pflichthinweis (`⚠️ PARAMETER-VORSCHLAG (UNVALIDIERT)` +
  „Dieser Vorschlag wurde NICHT durch Walk-Forward-Validierung geprüft.") steht
  weiter fest verdrahtet in `shared/empfehlung_format.py` und wird weiter vom
  Bericht **vor** den Zahlen ausgegeben. Der Selbsttest hat eine Probe, die
  anschlägt, wenn er verschwindet.
* `live_params.py` wird nie geschrieben; der Schlusshinweis „Es wurde NICHTS
  automatisch geändert" steht unverändert im Bericht.
* Die Zielgrößen-Angabe ist **zusätzlich** und hängt nicht am Pflichthinweis —
  der Test weist beide Richtungen getrennt nach.

---

## 5. Geänderte Dateien

| Datei | Änderung |
|---|---|
| `shared/param_search_agent.py` | Zielgröße, Prompt-Abschnitt, Ausgabe-Satz, `call_fn`-Parameter |
| `strategies/{elliott_wave,elliott_wave_stocks,t3_supertrend}/agent_optimise.py` | geben die Zielgrößen-Angabe aus (je 3 Zeilen) |
| `strategies/{…}/quarterly_review.py` | reichen sie in den Bericht durch (je ~12 Zeilen) |
| `shared/test_agent2_zielfunktion.py` | **neu** — 41 Prüfungen |
| `docs/UEBERGABEPROTOKOLL.md` | Abschnitt 6.2 nachgezogen |

**Nicht angefasst:** `live_params.py`, `forward_test.py`, `equity_simulation.py`,
`multi_symbol_optimise.py`, `results/*`, alles unter `broker/`, Crontab,
launchd-Vorlagen, `research/*`.

---

## 6. Tests

`python3 shared/test_agent2_zielfunktion.py` → **41 von 41 Prüfungen bestanden**,
Laufzeit ~4 Sekunden, **kein einziger echter API-Aufruf**. Einzelheiten im
Testauftrag (`docs/TESTAUFTRAG_TB22_agent2_zielfunktion.md`).

Alle bestehenden Tests laufen unverändert — mit einem Basislauf auf
unverändertem `main` belegt; die verbleibenden Fehlschläge sind vorbestehend und
rein umgebungsbedingt (`fastapi`, `yfinance`, fehlende Zeitzonendaten). Tabelle
im Ergebnisdokument.

---

## 7. Was offen bleibt

* **Die Rastersuche wählt weiter auf dem Blockmaß.** Das ist Absicht: die
  Übergangsregel gilt, Agent 2 war die benannte Ausnahme. Schritt **M2** aus
  `research/drawdown_reihenfolge/BERICHT.md` (volle Kette für die vier Bots,
  deren Parameterwahl unter dem chronologischen Maß kippen würde) ist davon
  unberührt und weiterhin offen.
* **Die sechs Prototyp-Bots haben Agent 2 gar nicht** — kein `agent_optimise.py`,
  kein `quarterly_review.py`. Diese Änderung betrifft drei Bots.
* Ein Vorschlag von Agent 2 bleibt **unvalidiert**. Vor einer Übernahme steht
  weiterhin Walk-Forward → Equity-Simulation → Buy-and-Hold-Vergleich.
