# Ergebnis — TB-17: Veraltete Zahlen in `live_params`

Branch `claude/new-session-btix48`, Basis `origin/main` (`74d4f55`, nach Merge
von PR #88). Ein Commit.

**Es wurde ausschliesslich Kommentartext geändert. Kein Parameterwert.** Der
Nachweis steht unten und ist stärker als ein Blick in den Diff.

---

## Zuerst die Antwort auf Punkt 3: nur eine Datei war betroffen

Alle **neun** `live_params.py` wurden auf die gemeldete Fehlerklasse geprüft —
Backtest-Zahlen in Kommentaren, die aus der Zeit vor PR #26 (Look-Ahead), vor
der Sync-Reihe (PR #38–#59) oder vor PR #81 (Kurslücken) stammen.

| Bot | Zahlen im Kommentar? | Auf heutiger Grundlage? |
|---|---|---|
| `elliott_wave_stocks` | ja | **NEIN — zwei Einträge betroffen** |
| `elliott_wave` | ja | ja, belegt |
| `turtle_soup_stocks` | ja | ja, belegt |
| `volatility_breakout_crypto` | ja | ja, belegt |
| `rsi2_crypto` | ja (Skip-Raten) | ja, belegt |
| `rsi2_mean_reversion` | nein | — |
| `t3_supertrend` | nein | — |
| `turtle_soup_crypto` | nein | — |
| `volatility_breakout` | nein (nur qualitativ) | Aussage trägt, belegt |

**Keine weitere veraltete Zahl.** Jede in den übrigen acht Dateien genannte
Kennzahl liess sich auf ihren Bericht zurückführen — Einzelnachweis unten. Es
wurde nichts geraten und nichts ergänzt.

**Der eigentliche Befund ist grösser als gemeldet:** in
`elliott_wave_stocks/live_params.py` war nicht nur der Eintrag vom
**2026-09-02** falsch, sondern auch der vom **2026-09-03** — und der war noch
nie korrigiert worden.

---

## Was in `elliott_wave_stocks/live_params.py` falsch war

### Eintrag 2026-09-02 — der gemeldete Befund

Behauptet wurde: „schlaegt Buy-and-Hold klar (1458% vs. 756% Rendite, -1.32%
vs. -34.83% Max Drawdown)".

| | behauptet | gültig |
|---|---:|---:|
| Strategie, Rendite | +1458 % | **+330,18 %** |
| Strategie, Max Drawdown | −1,32 % | **−22,70 %** |
| Buy-and-Hold, Rendite | +756 % | +755,69 % ✓ |
| Buy-and-Hold, Max Drawdown | −34,83 % | −34,83 % ✓ |

**Der Vergleichsmassstab stand von Anfang an richtig in der Zeile.** Falsch war
nur die eigene Zahl daneben — um mehr als den Faktor vier. Das ist die
unangenehmere Variante: eine Zeile, in der die Hälfte stimmt, liest sich
geprüft.

Quelle der gültigen Zahlen: `research/elliott_wave_params/BERICHT.md`
Abschnitt 4. Buy-and-Hold schlägt diesen Bot in der Rendite **und** im
Calmar-Verhältnis (21,70 gegen 14,55); keine der 252 geprüften Kombinationen
kommt an die +755 % heran.

### Eintrag 2026-09-03 — nicht gemeldet, aber dieselbe Fehlerklasse

Dort standen acht Kennzahlen zur Entscheidung `USE_TAKE_PROFIT = False`:
„+3084% statt +1500% Gesamtzeitraum, +204% statt +108% OOS" bei Drawdowns von
„-9.79%/-5.04% statt -1.90%/-1.65%".

Alle acht stammen aus `results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md` und
damit aus **derselben** Look-Ahead-Grundlage. PR #86 hat die abgelegte
Ergebniskurve nachgerechnet: statt **+1500,53 % / −1,90 %** sind es
**+352,72 % / −22,44 %**.

**Die Entscheidung hält, die Zahlen dazu nicht.** `USE_TAKE_PROFIT = False`
ruht seit PR #28 auf einer Rangfolge, nicht auf diesen Zahlen: unter den 116
Kombinationen, die die Mindestfilter bestehen, arbeiten die vorderen zehn
praktisch ausnahmslos ohne festes Kursziel. Ein sauber gerechnetes Gegenstück
zum Paar „mit/ohne Kursziel" existiert **nicht** — deshalb steht dort jetzt
**keine neue Zahl**, sondern der Hinweis, dass der gemessene Hebel der
Entscheidung unbekannt ist.

### Warum die Korrektur von 2026-09-08 nicht gereicht hat

Am 2026-09-08 war die Buy-and-Hold-Aussage schon einmal richtiggestellt
worden — aber **an anderer Stelle als dort, wo sie stand**. Der Eintrag vom
2026-09-02 trug seine Behauptung weiter im Wortlaut und verwies per „ACHTUNG"
auf eine Richtigstellung sechs Tage weiter unten. Wer die Datei von oben
liest, hatte die widerlegte Aussage gelesen und geglaubt, bevor die Korrektur
kam.

Die gültigen Zahlen stehen deshalb jetzt **im Kopf der Datei, vor der
Historie**. Die zurückgezogenen Zahlen bleiben absichtlich stehen, jetzt aber
an ihrer Stelle als zurückgezogen markiert: sie sind in Berichten, E-Mails und
im Übergabeprotokoll zitiert worden und verschwinden nicht dadurch, dass man
sie hier löscht.

Und: dieselbe Korrektur hat 2026-09-08 den Eintrag vom 2026-09-03 nicht
mitgenommen. **Genau dieselbe Fehlerklasse wie am 12.09.2026 in
`broker/README.md` und `broker/README_IBKR.md`** — eine Korrektur, die nur die
gemeldete Zeile anfasst, lässt die Geschwister stehen.

---

## Die Entscheidung, die dazugehört (Punkt 2)

Festgehalten in `live_params.py` und im Übergabeprotokoll (Abschnitt 3.3, die
Entscheidungstabelle in Abschnitt 8 und Abschnitt 9 Punkt 4, der bis heute
„Bewusst noch nicht entschieden" trug):

> **Der Bot läuft weiter — als Diversifikator, nicht weil er den Markt
> schlägt.** Gemessen wird er künftig an seinem Beitrag zum Portfolio, nicht
> an der Einzelrendite. (Nutzer, 12.09.2026)

**Prüftermine:** Quartals-Review Oktober 2026 als Zwischenstand, ein
belastbares Urteil eher Januar 2027 — die Live-Historie ist zu kurz (kein Bot
erreicht `MIN_LIVE_CLOSED_TRADES = 10`; die Portfolio-Zahlen stammen also
weiterhin aus Backtest-Kurven).

**Schärferes Prüfkriterium:** der Bot bei **gleicher Zeit im Markt** gegen das
**95. Perzentil von Zufalls-Timing**. Dieses Kriterium ist gewählt, aber
**noch nicht gemessen** — es ist als Auftrag an den Prüftermin vermerkt, nicht
als Ergebnis.

### Ein Vorbehalt, der mitnotiert werden musste

`research/exposure_messung/BERICHT.md` misst für diesen Bot **95,4 % Zeit im
Markt** und **+0,46 Korrelation** zu einem gleichgewichteten Buy-and-Hold des
Aktienuniversums (tägliche Bewertung zu Marktpreisen). Ein Bot, der fast immer
investiert ist und sich dabei deutlich mit dem Markt bewegt, ist **kein
selbstverständlicher Diversifikator**.

Dasselbe Dokument zeigt zudem: gerade die aussergewöhnlich flache **abgelegte**
Kurve dieses Bots (−1,65 %) hat den kombinierten Vierer-Drawdown getragen;
frisch gerechnet sind es **−21,16 %**. Die Diversifikations-Begründung stützt
sich also teilweise auf dieselbe Zahlenbasis, die diese Korrektur gerade
zurückzieht. Das ist der eigentliche Grund, das schärfere Kriterium anzulegen
— und der Vorbehalt steht in `live_params.py`, damit die Begründung beim
Prüftermin nicht ungeprüft durchläuft.

---

## Nachweis: kein Parameterwert berührt

Nicht per Diff, sondern am ausgewerteten Ergebnis — zwei unabhängige Wege.

**1. Alle Konstanten vor und nach der Änderung.** Die neun Dateien wurden per
AST gelesen (`ast.literal_eval` auf jede Zuweisung auf Modulebene), vor der
Änderung und danach:

```
IDENTISCH: alle 9 live_params.py liefern exakt dieselben Konstanten
61 Konstanten in 9 Bots
```

`LAST_UPDATED` ist dabei mitgeprüft und bleibt bei `elliott_wave_stocks` auf
`2026-09-03` — der Wert bezeichnet den Stand der **Parameter** und wird in
`research/pnl_2025_fixed_size/extract.py` so ausgewertet.

**2. Der Code-AST ohne Docstrings, gegen `HEAD`.** Strenger als der
Wertevergleich: er würde auch eine geänderte Struktur zeigen, die zufällig
dieselben Werte liefert.

```
  elliott_wave                 Code-AST identisch   Docstring unveraendert
  elliott_wave_stocks          Code-AST identisch   Docstring geaendert
  rsi2_crypto                  Code-AST identisch   Docstring unveraendert
  rsi2_mean_reversion          Code-AST identisch   Docstring unveraendert
  t3_supertrend                Code-AST identisch   Docstring unveraendert
  turtle_soup_crypto           Code-AST identisch   Docstring unveraendert
  turtle_soup_stocks           Code-AST identisch   Docstring unveraendert
  volatility_breakout          Code-AST identisch   Docstring unveraendert
  volatility_breakout_crypto   Code-AST identisch   Docstring unveraendert

Ergebnis: nur Kommentartext geaendert
```

**Genau ein Docstring geändert, null Code.** Nicht angefasst wurden ausserdem
`forward_test.py`, `equity_simulation.py`, `multi_symbol_optimise.py`, alles
unter `broker/` und `results/`, die Crontab und die launchd-Vorlagen.

**3. Unabhängige Bestätigung der Zahl, die jetzt im Dateikopf steht.**
`research/elliott_wave_params/test_params.py elliott_wave_stocks` rechnet die
Live-Kombination aus dem Bot-Code neu durch und meldet **330.18 % / -22.7 %** —
genau die Werte, die nun im Kopf von `live_params.py` stehen. Die Korrektur
stützt sich also nicht nur auf den Bericht, sondern auf einen Lauf gegen den
Bot selbst (18/18 Prüfungen).

---

## Einzelnachweis der übrigen acht Dateien

Jede Zahl auf ihre Quelle zurückgeführt. **Nur gemeldet, nichts geraten.**

| Bot | Zahl im Kommentar | Quelle | Urteil |
|---|---|---|---|
| `elliott_wave` | +67,8 % bei −10,2 % gegen B&H +12,2 % bei −79,8 % | `research/elliott_wave_params/BERICHT.md` (+67,77 %/−10,17 %, +12,19 %/−79,76 %) | **stimmt** — und deckt sich exakt mit der in PR #86 erneuerten Kurve |
| `elliott_wave` | 72,6 % / 130 statt 791 Trades / 31 OOS / 4 bzw. 15 von 18 Coins | derselbe Bericht (PR #28) | **stimmt**, nach der Look-Ahead-Korrektur entstanden |
| `turtle_soup_stocks` | 2020-COVID-Drawdown −32,22 % (Basis) → −29,91 % (neu) | `results/turtle_soup_stocks/PROTOTYPE_FINDINGS.md`, Z. 132/242/244 | **stimmt**; die −29,91 % sind zugleich der Gesamt-MaxDD der in PR #86 erneuerten Kurve |
| `volatility_breakout_crypto` | +18,45 % vs. +20,04 % (Split 75/25) | `results/volatility_breakout_crypto/PROTOTYPE_FINDINGS.md`, Z. 230/231 | **stimmt** |
| `volatility_breakout_crypto` | −11,33 % → −7,76 % (Split 70/30) | ebenda, Abschnitt 9a | **stimmt** |
| `volatility_breakout_crypto` | 2022: −12,35 % → −1,60 %, −16,55 % → −6,07 %, 91,3 % → 84,2 % | ebenda, Abschnitt 9c | **stimmt** |
| `rsi2_crypto` | Skip-Rate 10,7 % / 2,9 % OOS | `results/rsi2_crypto/PROTOTYPE_FINDINGS.md`, Z. 103/104 | **stimmt** |
| `volatility_breakout` | „deutlich höhere Rendite bei nur leicht höherem Drawdown" (Limit 15 statt 8) | `results/volatility_breakout/PROTOTYPE_FINDINGS.md`, Z. 359/360: +224,41 %/−23,97 % gegen +142,06 %/−22,39 % | **Aussage trägt**; die Zahlen decken sich exakt mit der in PR #86 erneuerten Kurve |
| `rsi2_mean_reversion`, `t3_supertrend`, `turtle_soup_crypto` | keine Kennzahlen im Kommentar | — | nichts zu korrigieren |

**Die Gegenprobe, die das belastbar macht:** von den fünf Bots, deren
Grundlage sich seit ihrem `live_params`-Eintrag verschoben hat (PR #86: die
beiden Elliott-Bots über den Look-Ahead, `rsi2_mean_reversion`,
`turtle_soup_stocks` und `volatility_breakout` über die Sync-Reihe bzw. die
Kurslücken), nennen drei überhaupt Zahlen — und bei `elliott_wave`,
`turtle_soup_stocks` und `volatility_breakout` decken sich diese Zahlen exakt
mit den **erneuerten** Kurven. Die Einträge sind also nach der jeweiligen
Korrektur geschrieben worden. Nur `elliott_wave_stocks` blieb zurück.

---

## Tests

| Test | Ergebnis |
|---|---|
| **`shared/test_live_params_werte.py`** (neu) | **69/69** |
| `dashboard/test_dashboard.py` | 784/784 |
| `research/pnl_2025_fixed_size/test_pnl.py` | 93/93 |
| `research/elliott_wave_params/test_params.py elliott_wave_stocks` | 18/18 |
| `shared/test_kursdaten.py` | 64/68 — die 4 Fehlschläge sind Umgebung, siehe unten |
| alle übrigen Selbsttests | unverändert bestanden |

### Der neue Test: `shared/test_live_params_werte.py`

Drei Prüfungen, `python3 shared/test_live_params_werte.py`:

1. **Wertetabelle** — alle **61 Konstanten aller neun Bots** stehen als
   Sollwert in der Datei. Weicht eine ab, verschwindet oder kommt eine hinzu,
   schlägt es an und nennt den Bot und den Parameter. Das ist die eigentliche
   Zusicherung dieser Aufgabe, und sie gilt ab jetzt dauerhaft, nicht nur für
   diesen Commit.
2. **Rein deklarativ** — jede der neun Dateien darf nur Zuweisungen enthalten,
   und jeder Wert muss ein Literal sein. Damit kann sich in einer
   „Nur-Kommentar"-Änderung auch keine Logik einschleichen, die die
   Sollwert-Tabelle umgeht.
3. **Buy-and-Hold-Behauptungen** — siehe unten.

Die Sollwerte wurden per AST aus dem Stand von `main` **vor** der Korrektur
gelesen, nicht abgeschrieben.

### Zur zweiten, freigestellten Prüfung: ja, sie ist machbar — aber nur eng

Der Auftrag liess offen, ob eine Prüfung auf unbelegte
Buy-and-Hold-Behauptungen sinnvoll ist. **Sie ist umgesetzt, in bewusst enger
Fassung.**

**Die Regel:** Eine Zeile, die „Buy-and-Hold" **und** eine Prozentzahl trägt,
muss im **selben Historien-Eintrag** entweder eine Quelle unter `research/`
bzw. `results/` nennen oder als zurückgezogen gekennzeichnet sein.

**Warum nur dieselbe Zeile und nicht ein Fenster von zwei oder drei Zeilen** —
das ist die eigentliche Entscheidung: Sechs der neun Dateien nennen
Buy-and-Hold nur als Glied der Validierungskette („Backtest → Walk-Forward →
… → Buy-and-Hold →"), und in `volatility_breakout/live_params.py` folgt zwei
Zeilen darunter „8% Stop-Loss". Ein Fenster von zwei Zeilen würde dort also
Alarm schlagen, wo überhaupt keine Behauptung steht. **Ein Prüfer, der bei
sechs von neun Dateien grundlos anspringt, wird abgeschaltet — und schützt
danach nichts mehr.** Die enge Regel kostet Trennschärfe und behält dafür ihre
Glaubwürdigkeit.

**Was sie also nicht leistet, ausdrücklich:** eine Behauptung, die sich über
einen Zeilenumbruch zwischen Wort und Zahl verteilt, entgeht ihr. Und ob eine
Zahl inhaltlich stimmt, kann kein Textprüfer beantworten — dafür gibt es den
Bericht, auf den er zu verweisen verlangt.

**Der Prüfer ist gegen sich selbst geprüft** (Abschnitt 3b, fünf Fälle): der
Originalbefund TB-17 wird erkannt; dieselbe Zeile mit Quelle im Eintrag wird
durchgelassen; als zurückgezogen markiert wird durchgelassen; die
Validierungskette löst **nicht** aus; und eine Quelle in einem **fremden**
Eintrag belegt nichts.

### Eine bestehende Prüfung musste präzisiert werden

Drei bestehende Tests führen eine Sperre „keine Live-Datei angefasst". **Zwei
davon vergleichen gegen `HEAD`** und werden mit dem Commit von selbst wieder
grün — nachgewiesen: `research/pnl_2025_fixed_size/test_pnl.py` steht nach dem
Commit bei **93/93**, `research/elliott_wave_params/test_params.py
elliott_wave_stocks` bei **18/18** („live_params.py und forward_test.py
unveraendert — leerer Diff").

**Die dritte vergleicht gegen `origin/main`:** `shared/test_kursdaten.py`
(PR #81). Sie verglich die **Dateibytes** und hätte damit jede
Kommentar-Korrektur als Befund gemeldet — auch diese, und im Unterschied zu
den beiden anderen bis zum Merge.

Sie vergleicht jetzt die per AST ausgewerteten **Werte** statt der Bytes.
**Das ist strenger als vorher, nicht lockerer:** eine geänderte Zahl fällt
weiterhin auf — nachgewiesen mit einer Gegenprobe (`STOP_LOSS_PCT` 3.0 → 4.0
wurde erkannt und namentlich gemeldet) — und zusätzlich fällt jetzt auf, wenn
eine Konstante verschwindet oder neu hinzukommt. Was sie nicht mehr meldet,
ist der Satz daneben; ein Kommentar ändert kein Handelsverhalten. Die Sperren
für `forward_test.py`, `equity_simulation.py`, `broker/` und `data/` bleiben
byte-exakt.

Dies ist die erste reine Dokumentations-Änderung an einer `live_params.py`
seit dem Bestehen dieser Sperre — die Korrektur vom 2026-09-08 liegt vier Tage
vor PR #81. Die Sperre ist also nie gegen einen legitimen Fall gelaufen.

### Offene Fehlschläge, alle umgebungsbedingt

`shared/test_kursdaten.py` meldet 4 Fehlschläge (`test_am_echten_bot`,
`test_gegenprobe`, `simulate_portfolio`, `fetch_historical_data`) und
`system/test_dienst_plists.py` 4 „offene (Platzhalter)". **Beide sind
vorbestehend** — nachgewiesen durch einen Basislauf auf unverändertem `main`
vor der Änderung, der dieselben Fehlschläge zeigt (dort 63/67, weil die
präzisierte Sperre jetzt eine Prüfung mehr ausführt). Ursache sind im
Testcontainer fehlende Bot-Abhängigkeiten, nicht diese Änderung.

*Hinweis zur Testumgebung:* In diesem Container **ist** `node` installiert,
deshalb 784/784 statt der 780/780, die Sie auf Ihrem Rechner sehen. Die vier
zusätzlichen Prüfungen sind hier also tatsächlich gelaufen.

---

## Geänderte Dateien

| Datei | Art der Änderung |
|---|---|
| `strategies/elliott_wave_stocks/live_params.py` | **nur Docstring** — Kopf mit gültigen Zahlen, zwei Einträge richtiggestellt, neuer Eintrag 2026-09-13 mit der Entscheidung |
| `docs/UEBERGABEPROTOKOLL.md` | Abschnitt 3.3 (Entscheidung + Vorbehalt), 4.2 (neuer Test), 8 (Entscheidungszeile), 9 Punkt 4 (entschieden) und Punkt 18 (neu: `EXPERIMENT_FINDINGS.md`), Nachtrag im Kopf |
| `shared/test_live_params_werte.py` | **neu**, 69 Prüfungen |
| `shared/test_kursdaten.py` | Sperre für `live_params.py` auf Wertevergleich präzisiert |

---

## Was offen bleibt

1. **Das schärfere Prüfkriterium ist nicht gemessen.** „Gleiche Zeit im Markt
   gegen das 95. Perzentil von Zufalls-Timing" ist als Auftrag an den
   Prüftermin Oktober 2026 notiert. Eine Messung wäre eine eigene
   Untersuchung unter `research/`.
2. **Kein Gegenstück zu „mit/ohne Kursziel" auf sauberer Grundlage.** Die
   Entscheidung `USE_TAKE_PROFIT = False` ist durch die Rangfolge gestützt,
   ihr gemessener Hebel bleibt unbekannt.

---

## Nachtrag 2026-09-13: Warnhinweis in `EXPERIMENT_FINDINGS.md`

Auf Wunsch des Nutzers nachgetragen — die ursprüngliche Aufgabe hatte
`results/` ausgenommen.

`results/elliott_wave_stocks/EXPERIMENT_FINDINGS.md` trägt jetzt einen Kasten
am Dateianfang und je eine Zeile unter den vier betroffenen Abschnitten sowie
unter der Empfehlung. Der Kasten nennt die Ursache (Look-Ahead, PR #26), die
heute gültigen Zahlen (+330,18 % / −22,70 % gegen Buy-and-Hold
+755,69 % / −34,83 %) und was von den Befunden bleibt.

**Die Zahlen der Datei wurden NICHT umgerechnet — mit Absicht.** Sie haben
eine aktive Aufgabe: `research/elliott_wave_lookahead/` benutzt sie als
*veröffentlichte Baseline* und weist damit nach, dass die
Look-Ahead-Reproduktion den damaligen Lauf wirklich trifft
(`decisions.py` → `PUBLISHED_CELLS` mit +1500,53 % / −1,90 % und
+3084,09 % / −9,79 %; `verify_baseline.py` → `PUBLISHED`). Wer die Tabellen
überschreibt, zerstört diesen Nachweis. Der Warnhinweis sagt das ausdrücklich,
damit die nächste Sitzung nicht „aufräumt".

Geprüft, dass die Datei von keinem Programm **gelesen** wird: alle Fundstellen
von `EXPERIMENT_FINDINGS` im Repo sind Fliesstext in Kommentaren oder
hartcodierte Vergleichszahlen — keine Stelle parst die Datei. Ein Kasten am
Anfang kann also nichts brechen.

### Ein Nebenbefund beim Anbringen des Hinweises

Die abgelegte Ergebniskurve des Bots trug bis PR #86 **+1500,53 % bei
−1,90 %** — das ist die Zahl der Variante **mit** Take-Profit, obwohl
`USE_TAKE_PROFIT` am 2026-09-03 auf `False` gesetzt wurde. Belegt über die
Trade-Zahl: die alte Kurve hatte 469 Zeilen, und genau 469 ausgeführte Trades
nennt die Zelle „mit Take-Profit, Limit 8".

**Die Kurve war also aus zwei unabhängigen Gründen veraltet** — dem Look-Ahead
**und** einem Parameterwechsel, nach dem sie nie neu erzeugt wurde. PR #86
hatte nur den ersten Grund genannt. Das ist ein Argument dafür,
`shared/ergebniskurven.py` nach jeder Parameterübernahme laufen zu lassen,
nicht nur nach einer Methodik-Korrektur.

**Eigene Korrektur:** In der ersten Fassung dieses Dokuments und im Kommentar
vom 2026-09-03 stand, PR #86 habe „für diese Konfiguration" statt
+1500,53 % / −1,90 % nun +352,72 % / −22,44 % gemessen. Das war ungenau — die
+1500,53 % gehören zur Variante *mit* Take-Profit, die +352,72 % zur heutigen
*ohne*. Beide Stellen sind jetzt präzisiert.
