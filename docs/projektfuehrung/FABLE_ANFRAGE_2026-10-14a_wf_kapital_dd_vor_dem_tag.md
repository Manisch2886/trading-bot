# FABLE-Anfrage 14.10.2026 a (neuer Fable-Chat) — an Fable, den Verfahrensprüfer: Kapital-Drawdown im Walk-Forward als Forschungsmessung vor dem signierten Tag?; drei Fragen

*Steuernder Chat, 14.10.2026, an einen neuen Fable-Chat. Schlank gehalten (Betreiber 13.10.2026). Die Zitate sind per Skript aus der Quelle gezogen (HEAD `4979589`; Register am Commit `3f2e97e`, 12 023 Zeilen, Abschnitte 0–57). Hervorhebungen entfernt; „REG Z.“ = Registerzeile.*

**Berührte Registerabschnitte:** 11 (11.2), 15 (15.1), 24 (24.2), 48 (48.4, 48.11, 48.13, 48.14).

**Form der Antwort:** je Frage die Entscheidung mit Grund aus dem Registertext; die Fragen tragen keine Neigung. Freie Nummern: R ab R94, Abschnitt ab 58.

## 1. Lage

Nach der Betreiberkarte vom 14.10.2026 ist der nächste Posten der Kapital-Drawdown im Walk-Forward. Die sechs bot-eigenen Walk-Forward-Rechner wählen ihren IS-Sieger heute nach `robustness_score`, nicht nach dem Kapital-Drawdown (ERGEBNIS_TB27 Z. 89–94). Sie stehen mit `equity_simulation.py`, `multi_symbol_optimise.py`, `shared/messkette.py` und `shared/zuteilung.py` auf der Sperrliste (`research/vorregistrierung/herkunft.py` Z. 102–106); ein Umbau darin ist nach 15.1 und Posten 8 des Plans Arbeit nach dem Tag und hier nicht gefragt. Ein Forschungsmodul ausserhalb des Laufpfads kann die Zahl ohne Öffnung einer gesperrten oder eingefrorenen Datei messen (erschlossen, kein Lauf). Offen ist, ob eine solche Messung vor dem Tag Ergebnisgrössen des Selektionsraums erzeugt.

## 2. Zwei Zuschnitte

**A.** Neues `research/wf_kapital_dd/` in der Bauart von `research/drawdown_reihenfolge/kapitalkurve.py` (Bot-Code als Bibliothek gelesen). Je Bot laufen der bot-eigene Split und die Rastersuche, der IS-Sieger wird nach `robustness_score` bestimmt, und seine IS- und OOS-Trades gehen durch das bot-eigene `simulate_portfolio` und `messkette.calculate_max_drawdown`. Gemessen wird der ereignisindizierte Kapital-Drawdown je Bot neben dem Blockmass, auf den Kursdaten der Bots (ob auf dem registrierten Snapshot und mit dem registrierten Raster: nicht gemessen); Teilmessung, weil der OOS-Beginn je Symbol verschieden ist.

**B.** A und dazu der tägliche MtM-Drawdown über `research/mtm_drawdown/mtm_kern.py` (`mtm_pfad`, `drawdown_falte`). Die ausgeführten Positionen kämen aus dem Doppellauf mit Zeilenkennung im Symbol aus TB-24 (`research/tb24_haltedauern/positionen_holen.py`) (R45 ist nicht vollzogen). Dazu je Rasterpunkt ein Kapital-Score und die Prüfung, ob der IS-Sieger kippt.

## 3. Die Stellen (Wortlaut)

- **15.1** (REG Z. 1404, Überschrift): „Die Vorabklärung: es gilt Verfahren B“; REG Z. 1418–1420: „[…] die sechs bot-eigenen Walk-Forward-Rechner werden später ersetzt, nicht umgestellt — das ist TB-30b und nicht dieser Nachtrag.“
- **PLAN_VOR_DEM_TAG.md** Z. 101, Posten 8: „Neun Walk-Forward-Rechner ersetzen | ⛔ nein — „nötig ist nur eine Wache, dass keiner im Lauf aufgerufen wird — eine Zeile im Laufwrapper. Das Ersetzen ist Aufräumen nach dem Tag"
- **TB-120, F-15** (Z. 178–180): „R5 (b) (Zeilenzahl, Nullzeile) ist erst an einem Lauf prüfbar; ein Lauf des Zellen-Erzeugers auf dem Snapshot erzeugt vor dem Tag Ergebnisgrössen des Selektionsraums. Womit wird er vor dem Tag abgenommen (synthetische Eingaben, Teilraster, nur Struktur)?“
- **24.2** (REG Z. 4336–4340): „Der Kapital-Drawdown einer Falte für die Nebenbedingung wird auf der täglichen Mark-to-Market-Reihe des Kapitalpfads gerechnet (1a), auf denselben Tagen wie der Benchmark (3b (c)). Der ereignisindizierte Drawdown aus `equity_simulation.py` wird berichtet, nicht bewertet.“ — PRÄZISIERT durch R36 (REG Z. 4350).
- **R36** (48.4, REG Z. 10863): „zellen.csv trägt je (Zelle, Falte) kapital_drawdown_mtm_pct — den Kapital-Drawdown der Nebenbedingung auf der täglichen MtM-Reihe (1a) auf den Tagen des Benchmarks (3b (c)) — und kapital_drawdown_ereignis_pct — den ereignisindizierten Drawdown, berichtet, nicht bewertet (24.2). […] Der Drawdown je Falte ist der Ausschnitt eines durchgehenden Kapitalpfads (29.3, 2a): gemessen innerhalb der Falte, mit dem Kapitalstand am Faltenbeginn als erstem Hochpunkt, ohne Neustart des Kapitals.“
- **R43** (48.11, REG Z. 10936): „[…] Tatsachennotiz zu 11.2: Die Voraussetzung „evaluate_combination_multi liefert den Kapital-Drawdown“ wird für den Lauf gegenstandslos; den Kapital-Drawdown liefert der Zellen-Kern (R36); Agent 2 ist Regelbetrieb.“
- **R45** (48.13, REG Z. 10959): „shared/zuteilung.py::simuliere_portfolio gibt zusätzlich die ausgeführten Positionen (Symbol, Einstiegs- und Ausstiegszeit, Grösse, Preise) heraus […] Eine Rekonstruktion der Positionen aus den Ereignissen der equity_curve ist ein zweiter Rechenweg und wird nicht gegangen.“
- **Zusätzlich gefunden — R46** (48.14, REG Z. 10969, Antwort auf F-15): „Vor dem signierten Tag läuft der Zellen-Erzeuger nicht auf dem registrierten Snapshot mit dem registrierten Raster. […] Geprüft werden Struktur und Verfahren: Zeilenzahl nach R33, Nullzeile, Feldlisten nach R39, Lese-Audit, Ausgänge nach 36.5, Schreibregel R40, Nachrechnung R36 — nie eine Zahl des Selektionsraums.“

## 4. Die Fragen

1. Ist Zuschnitt A vor dem signierten Tag zulässig, und wenn ja, unter welcher Bedingung (zum Beispiel nur Kapital-Drawdown, keine Rendite; nur Struktur; Teilraster; synthetische Kursdaten wie nach R46)?
2. Bindet R45 („wird nicht gegangen“) oder A9 ein Forschungsmodul ausserhalb des Laufs, das die Positionen wie in Zuschnitt B über den Doppellauf aus TB-24 holt?
3. Braucht ein zulässiger Zuschnitt vor dem Bau einen Registerblock, oder ist er Handwerk auf Betreiberkarte?

## 5. Leseprotokoll und Sichtschutz

- **Gelesen** (Helfer, nur lesend): die zitierten Zeilen, REGISTER_INDEX.md (Kopf), 57.6; die Zuschnitte stammen aus einem Bestandsbericht ausserhalb des Repos.
- **Nicht gelesen:** die Marken an R36 (R75, R85) und an R46 (R75, R90); `BACKLOG*.md`, `ergebnisse/`, `docs/belege/`, Trade-Listen.
- **Sichtschutz:** keine Kennzahl eines Parametersatzes, keine Zahl aus einem Lauf.
