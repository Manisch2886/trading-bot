# Übergabe — TB-17: Veraltete Zahlen in `live_params`

Branch `claude/new-session-btix48`, Basis `origin/main` (`74d4f55`, nach PR #88).

---

## 1. Das Ergebnis der Prüfung aller neun Dateien — zuerst, wie gefordert

**In welchen weiteren `live_params.py` stehen veraltete Zahlen? In keiner.**

Alle neun wurden geprüft. Vier der übrigen acht nennen überhaupt Kennzahlen im
Kommentar (`elliott_wave`, `turtle_soup_stocks`, `volatility_breakout_crypto`,
`rsi2_crypto`), eine macht eine qualitative Aussage über Rendite und Drawdown
(`volatility_breakout`), drei nennen keine Zahlen
(`rsi2_mean_reversion`, `t3_supertrend`, `turtle_soup_crypto`).

**Jede einzelne genannte Zahl liess sich auf ihren Bericht zurückführen** —
mit Datei und Zeilennummer, siehe die Tabelle im Ergebnisdokument. Nichts
geraten, nichts ergänzt.

Die belastbarste Gegenprobe dazu: Fünf Bots haben eine Grundlagen-Verschiebung
hinter sich (PR #86 — die beiden Elliott-Bots über den Look-Ahead,
`rsi2_mean_reversion`, `turtle_soup_stocks` und `volatility_breakout` über die
Sync-Reihe bzw. die Kurslücken). Drei davon nennen Zahlen, und bei
`elliott_wave`, `turtle_soup_stocks` und `volatility_breakout` decken sich
diese Zahlen **exakt mit den erneuerten Kurven** (+67,77 %/−10,17 %;
−29,91 %; +224,41 %/−23,97 %). Diese Einträge sind also nach der jeweiligen
Korrektur geschrieben worden.

**Nur `elliott_wave_stocks` blieb zurück — und dort waren es zwei Einträge,
nicht einer.**

---

## 2. Was in der gemeldeten Datei stand

**Eintrag 2026-09-02 (der gemeldete Befund).** „schlaegt Buy-and-Hold klar
(1458% vs. 756%)". Gültig: **+330,18 % bei −22,70 %** gegen Buy-and-Hold
**+755,69 % bei −34,83 %**. Der Vergleichsmassstab war von Anfang an richtig —
falsch war nur die eigene Zahl daneben, um mehr als den Faktor vier.

**Eintrag 2026-09-03 (nicht gemeldet, dieselbe Fehlerklasse).** Acht
Kennzahlen zu `USE_TAKE_PROFIT = False` („+3084% statt +1500%", „−1.90%" …),
alle aus `results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md` und damit aus
derselben Look-Ahead-Grundlage. PR #86 hat für diese Konfiguration
**+352,72 % / −22,44 %** nachgerechnet statt +1500,53 % / −1,90 %.

Die **Entscheidung** `USE_TAKE_PROFIT = False` hält — sie ruht seit PR #28 auf
einer Rangfolge (unter den 116 Kombinationen, die die Mindestfilter bestehen,
arbeiten die vorderen zehn praktisch ausnahmslos ohne festes Kursziel), nicht
auf diesen Zahlen. Ein sauber gerechnetes Gegenstück zum Paar „mit/ohne
Kursziel" gibt es **nicht**, deshalb steht dort jetzt keine neue Zahl, sondern
der Hinweis, dass der gemessene Hebel unbekannt ist.

**Warum die Korrektur vom 2026-09-08 nicht gereicht hat.** Sie stand an
anderer Stelle als der Fehler: der Eintrag vom 2026-09-02 trug die Behauptung
weiter im Wortlaut und verwies per „ACHTUNG" sechs Tage nach unten. Wer von
oben liest, hat die falsche Aussage vorher geglaubt. Die gültigen Zahlen
stehen jetzt **im Kopf der Datei**. Und dieselbe Korrektur hatte den Eintrag
vom 2026-09-03 nicht mitgenommen — **genau die Fehlerklasse, die am
12.09.2026 in `broker/README.md` und `broker/README_IBKR.md` zweimal
aufgetreten ist.**

---

## 3. Die festgehaltene Entscheidung

> **Der Bot läuft weiter — als Diversifikator, nicht weil er den Markt
> schlägt.** Gemessen wird künftig der Beitrag zum Portfolio, nicht die
> Einzelrendite. (Nutzer, 12.09.2026)

Vermerkt in `live_params.py` und im Übergabeprotokoll: Abschnitt 3.3,
Entscheidungstabelle Abschnitt 8, und Abschnitt 9 Punkt 4 — der bis heute
„Bewusst noch nicht entschieden" trug und jetzt die Entscheidung samt offener
Prüfung ausweist.

**Prüftermine:** Oktober 2026 (Zwischenstand), belastbar eher Januar 2027.
**Kriterium:** gleiche Zeit im Markt gegen das 95. Perzentil von
Zufalls-Timing — gewählt, aber **noch nicht gemessen**, und als solches
vermerkt.

**Ein Vorbehalt, den Sie beim Prüftermin brauchen werden:** Die
Exposure-Messung weist für diesen Bot **95,4 % Zeit im Markt** und **+0,46
Korrelation** zu Aktien-Buy-and-Hold aus. Ein selbstverständlicher
Diversifikator ist er damit nicht. Und die aussergewöhnlich flache *abgelegte*
Kurve dieses Bots (−1,65 %) war es, die den kombinierten Vierer-Drawdown
getragen hat; frisch gerechnet sind es −21,16 %. Die Diversifikations-
Begründung stützt sich also teilweise auf dieselbe Zahlenbasis, die diese
Korrektur zurückzieht. Genau deshalb das schärfere Kriterium — und genau
deshalb steht der Vorbehalt in der Datei, damit die Begründung nicht
ungeprüft durchläuft.

---

## 4. Die harte Randbedingung: belegt

**Kein Parameterwert wurde berührt.** Drei unabhängige Nachweise:

1. **Alle 61 Konstanten aller neun Bots**, per AST vor und nach der Änderung
   gelesen: `IDENTISCH`. `LAST_UPDATED` mitgeprüft, bleibt auf `2026-09-03`.
2. **Der Code-AST ohne Docstrings, gegen `HEAD`**: bei allen neun Dateien
   identisch. Genau ein Docstring geändert, null Code.
3. **Ein Lauf gegen den Bot-Code selbst**:
   `research/elliott_wave_params/test_params.py elliott_wave_stocks` rechnet
   die Live-Kombination neu durch und meldet **330.18 % / -22.7 %** — genau
   die Zahlen, die jetzt im Dateikopf stehen (18/18 Prüfungen).

Nicht angefasst: `forward_test.py`, `equity_simulation.py`,
`multi_symbol_optimise.py`, alles unter `broker/` und `results/`, Crontab,
launchd-Vorlagen.

---

## 5. Tests

| Test | Ergebnis |
|---|---|
| **`shared/test_live_params_werte.py`** (neu) | **69/69** |
| `dashboard/test_dashboard.py` | 784/784 |
| `research/pnl_2025_fixed_size/test_pnl.py` | 93/93 |
| `research/elliott_wave_params/test_params.py elliott_wave_stocks` | 18/18 |
| alle übrigen Selbsttests | unverändert bestanden |

**Der neue Test** hält alle 61 Konstanten aller neun Bots als Sollwerte fest
(die eigentliche Zusicherung dieser Aufgabe, ab jetzt dauerhaft), prüft dass
jede Datei rein deklarativ bleibt, und schlägt an, wenn eine
Buy-and-Hold-Behauptung mit Prozentzahl ohne Quelle unter `research/` bzw.
`results/` dasteht.

**Zur freigestellten zweiten Prüfung: ja, machbar — aber nur eng.** Sie prüft
nur dieselbe Zeile, nicht ein Fenster. Grund: sechs der neun Dateien nennen
Buy-and-Hold bloss als Glied der Validierungskette, und bei
`volatility_breakout` steht zwei Zeilen darunter „8% Stop-Loss" — ein
Zwei-Zeilen-Fenster hätte dort grundlos Alarm geschlagen. Ein Prüfer, der bei
sechs von neun Dateien anspringt, wird abgeschaltet und schützt danach
nichts. Die Regel ist gegen sich selbst geprüft (fünf Fälle, Abschnitt 3b):
der Originalbefund wird erkannt, die Validierungskette löst nicht aus, und
eine Quelle in einem fremden Eintrag belegt nichts.

**Eine bestehende Sperre musste präzisiert werden.** `shared/test_kursdaten.py`
(PR #81) verbot jede Byte-Änderung an einer `live_params.py` gegen
`origin/main` — sie hätte diese Korrektur bis zum Merge als Befund gemeldet
(die gleichartigen Sperren in `test_pnl.py` und `test_params.py` vergleichen
gegen `HEAD` und werden mit dem Commit von selbst grün). Sie vergleicht jetzt
die ausgewerteten **Werte** statt der Bytes: **strenger als vorher** — eine
geänderte Zahl fällt weiterhin auf (mit Gegenprobe nachgewiesen:
`STOP_LOSS_PCT` 3.0 → 4.0 wurde namentlich gemeldet), und zusätzlich fällt
jetzt eine verschwundene oder neue Konstante auf. Dies ist die erste reine
Dokumentations-Änderung an einer `live_params.py`, seit diese Sperre besteht.

**Vorbestehende Fehlschläge, nicht von dieser Änderung:**
`shared/test_kursdaten.py` 4 Fehlschläge und `system/test_dienst_plists.py`
4 „offene (Platzhalter)" — nachgewiesen durch einen Basislauf auf
unverändertem `main`. Ursache sind im Testcontainer fehlende
Bot-Abhängigkeiten.

*Zur Testumgebung:* Hier **ist** `node` installiert, daher 784/784 statt der
780/780, die Sie auf Ihrem Rechner sehen — die vier zusätzlichen Prüfungen
sind tatsächlich gelaufen.

---

## 6. Was offen bleibt

1. **Das schärfere Prüfkriterium ist nicht gemessen** — eigene Untersuchung
   unter `research/` nötig.
2. **Kein sauberes Gegenstück zu „mit/ohne Kursziel".** Die Entscheidung ist
   durch die Rangfolge gestützt, ihr gemessener Hebel bleibt unbekannt.
3. **Neu aufgefallen: die Ergebniskurven hängen an der Parameterübernahme.**
   Siehe den Nebenbefund im Nachtrag unten — `shared/ergebniskurven.py` sollte
   nach **jeder** Parameterübernahme laufen, nicht nur nach einer
   Methodik-Korrektur. Nicht umgesetzt, nur beobachtet.

---

## 7. Geänderte Dateien

| Datei | Art |
|---|---|
| `strategies/elliott_wave_stocks/live_params.py` | **nur Docstring** |
| `docs/UEBERGABEPROTOKOLL.md` | Abschnitte 3.3, 4.2, 8, 9 (Punkte 4 und 18), Nachtrag im Kopf |
| `shared/test_live_params_werte.py` | **neu**, 69 Prüfungen |
| `shared/test_kursdaten.py` | Sperre auf Wertevergleich präzisiert |
| `docs/ERGEBNIS_TB17_veraltete_zahlen_live_params.md` | Ergebnisdokument |
| `results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md` | **Warnhinweis** — Kasten am Anfang plus Zeile je Abschnitt; **keine Zahl umgerechnet** |
| `docs/UEBERGABE_TB17_veraltete_zahlen_live_params.md` | dieses Dokument |

---

## 8. Nachtrag 2026-09-13: Warnhinweis in `EXPERIMENT_FINDINGS.md`

Auf Ihren Wunsch nachgetragen; die ursprüngliche Aufgabe hatte `results/`
ausgenommen. Damit ist Punkt 18 des Übergabeprotokolls **entschieden** statt
offen.

**Was die Datei jetzt trägt:** einen Kasten am Dateianfang (Ursache, die heute
gültigen Zahlen, was von den Befunden bleibt) und je eine Zeile unter den vier
betroffenen Abschnitten sowie unter der Empfehlung. Wer von oben liest **oder**
direkt zu einer Tabelle springt, sieht den Hinweis.

**Die Zahlen sind bewusst NICHT umgerechnet.** Das ist der wichtigste Punkt
dieses Nachtrags: `research/elliott_wave_lookahead/` benutzt sie als
*veröffentlichte Baseline* und weist damit nach, dass die
Look-Ahead-Reproduktion den damaligen Lauf wirklich trifft
(`decisions.py` → `PUBLISHED_CELLS`: +1500,53 %/−1,90 % und
+3084,09 %/−9,79 %; `verify_baseline.py` → `PUBLISHED`). Wer die Tabellen
überschreibt, zerstört diesen Nachweis — der Warnhinweis sagt das ausdrücklich,
damit die nächste Sitzung nicht „aufräumt". Vorher geprüft: keine Stelle im
Repo **parst** die Datei, alle Fundstellen sind Fliesstext oder hartcodierte
Vergleichszahlen. Ein Kasten kann also nichts brechen.

**Nebenbefund, der dabei aufgefallen ist — und der Ihnen wichtig sein dürfte:**
Die abgelegte Ergebniskurve trug bis PR #86 **+1500,53 % bei −1,90 %**, also
die Zahl der Variante **mit** Take-Profit — obwohl `USE_TAKE_PROFIT` am
2026-09-03 auf `False` gesetzt wurde. Belegt über die Trade-Zahl: die alte
Kurve hatte 469 Zeilen, und genau 469 ausgeführte Trades nennt jene Zelle. Die
Kurve war also aus **zwei** unabhängigen Gründen veraltet — dem Look-Ahead
**und** einem Parameterwechsel, nach dem sie nie neu erzeugt wurde. PR #86
hatte nur den ersten Grund genannt.

**Eigene Korrektur:** Im Kommentar vom 2026-09-03 und in der ersten Fassung des
Ergebnisdokuments stand, PR #86 habe „für diese Konfiguration" statt
+1500,53 %/−1,90 % nun +352,72 %/−22,44 % gemessen. Ungenau — die +1500,53 %
gehören zur Variante *mit* Take-Profit, die +352,72 % zur heutigen *ohne*.
Beide Stellen sind präzisiert.

**Nachweis erneut geführt:** alle 61 Konstanten unverändert, Code-AST aller
neun Dateien gegen `origin/main` identisch, nur Kommentartext geändert.
