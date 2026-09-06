# Hierarchical Risk Parity (HRP) — Backtest-Only-Untersuchung für die Portfolio-Gewichtung

**Status: reine Backtest-Untersuchung, KEINE Live-Aktivierung, KEINE
Änderung an `shared/portfolio_overview.py` oder irgendeiner anderen
Live-Datei.** Alle neuen Skripte liegen ausschliesslich unter
`research/hrp_portfolio/`. Verifiziert per `git status`: keine Datei
ausserhalb dieses neuen Verzeichnisses wurde angefasst.

## Kurzfassung

Für das kombinierte 9-Bot-Portfolio (aktuell in `shared/portfolio_overview.py`
gleichgewichtet, je 11,1 %) wurde eine Hierarchical-Risk-Parity-Gewichtung
(HRP, López de Prado 2016) mit **quartalsweisem Walk-Forward-Rebalancing**
gegen (a) die bestehende, nie rebalancierte Gleichgewichtung und (b) eine
gemeinsame Buy-and-Hold-Referenz auf Symbol-Ebene verglichen.

**Ergebnis in einem Satz:** HRP reduziert den maximalen Drawdown gegenüber
der bestehenden Gleichgewichtung nur geringfügig (-4,93 % vs. -6,33 %),
kostet dafür aber spürbar Rendite (63,3 % vs. 82,4 % über den gemeinsamen
Vergleichszeitraum) — die risikoadjustierte Calmar-Ratio ist bei HRP sogar
minimal SCHLECHTER als bei der bestehenden einfachen Gleichgewichtung
(12,83 vs. 13,02). Beide Varianten schlagen die Buy-and-Hold-Referenz und
reduzieren den Drawdown gegenüber dem schlechtesten Einzel-Bot drastisch
(-32,4 % → unter -7 %) — die Diversifikationswirkung selbst ist also
unabhängig von der genauen Gewichtungsmethode bereits sehr stark. **Keine
Handlungsempfehlung** — die Entscheidung über eine etwaige Anwendung liegt
beim Nutzer in einer separaten, künftigen Session.

## Methodik

### Algorithmus (HRP nach López de Prado 2016)

Deterministisches hierarchisches Clustering nach Korrelations-Distanz
(`dist = sqrt(0.5*(1-corr))`), Quasi-Diagonalisierung (ähnliche Bots landen
im Dendrogramm nebeneinander), rekursive Bisektion der Kapitalzuteilung
(Kapital wird zuerst zwischen den unähnlichsten Ober-Clustern verteilt,
dann rekursiv innerhalb, umgekehrt proportional zur Cluster-Varianz unter
Inverse-Varianz-Gewichtung). Kein trainiertes/lernendes Modell, keine
Zufallskomponente — passt zum regelbasierten "kein ML"-Grundsatz des
Projekts (CLAUDE.md). Implementiert in `hrp_core.py`, 20 Sanity-/
Regressionstests in `test_hrp_core.py`, alle grün (u. a.: unkorrelierte
Assets gleicher Volatilität → Gewichte nahe 1/N; ein Cluster aus zwei
stark korrelierten Assets bekommt gemeinsam weniger Gewicht als bei naiver
1/N-Gewichtung).

### Walk-Forward-Rebalancing (entscheidend gegen Look-Ahead-Bias)

HRP-Gewichte werden **quartalsweise** neu berechnet, jeweils **nur aus
Renditen VOR Quartalsbeginn** (expandierendes Trainingsfenster — das
5. Quartal nutzt die gesamte Historie der ersten 4 Quartale, nicht nur das
4.), und dann auf das nächste, zum Berechnungszeitpunkt noch unbekannte
Quartal angewendet. Das allererste Quartal hat naturgemäss keine
Trainingshistorie und läuft gleichgewichtet (Bootstrap, siehe Annahmen).
Die kombinierte Equity-Kurve wird aus den TATSÄCHLICHEN täglichen
Bot-Renditen jedes Quartals unter den jeweils vorab festgelegten Gewichten
aufgebaut — kein rückwirkendes "Schönrechnen".

### Datenquelle

Wiederverwendet **unverändert** die bestehende Logik aus
`shared/portfolio_overview.py` (`discover_bots()`, `load_all_curves()`,
`load_trade_dates()`) — Live-DB bevorzugt ab `MIN_LIVE_CLOSED_TRADES=10`
geschlossenen Live-Trades, sonst `equity_curve.csv`-Fallback. In dieser
Sandbox existiert keine Live-Datenbank (`*.db` ist gitignored, siehe
CLAUDE.md), daher lief die Untersuchung durchgehend auf dem
Backtest-Fallback aller 9 Bots — in einer Umgebung mit echten Live-DBs
würde `run_walk_forward.py` automatisch dieselbe, bereits validierte
Live-Priorisierung übernehmen, ohne Codeänderung.

### Fallback-Regel für Bot-Paare unter der Datenbasis-Schwelle

Dieselbe Schwelle wie `portfolio_overview.py` (`MIN_COMMON_TRADING_DAYS =
30` gemeinsame Handelstage) wird **pro Quartal auf das jeweilige
Trainingsfenster** angewendet. Ist ein Bot-Paar darunter, gilt es als
"nicht belastbar". Über alle Bot-Paare wird das **grösste Teil-Universum**
gesucht, in dem AUSNAHMSLOS jedes Paar die Schwelle erreicht (Brute-Force
über alle 2⁹=512 Teilmengen, bei 9 Bots trivial in der Laufzeit) — HRP wird
NUR auf diesem Teil-Universum berechnet. Bots ausserhalb behalten GENAU ihr
normales 1/N-Gewicht; das verbleibende Kapital (Anteil = Grösse des
Teil-Universums / 9) wird gemäss HRP unter den eingeschlossenen Bots
verteilt. Begründung: es gibt keine belastbare Grundlage, ausgeschlossene
Bots anders als beim Status quo zu behandeln — ein Abweichen davon wäre
eine unbegründete Vermutung; das ist die konservativere, methodisch
sauberere Variante gegenüber einer Neuverteilung des gesamten Kapitals
unter Ignorieren der betroffenen Bots.

**Diese Fallback-Regel wurde NICHT nur theoretisch gebraucht:** siehe
Abschnitt "Wichtiger Befund" unten — sie griff in 17 von 18 Quartalen.

## Getroffene Annahmen (vollständig)

1. **Rebalancing-Intervall: Kalender-Quartale.** Von der Aufgabenstellung
   selbst als Beispiel vorgeschlagen. Begründet durch (a) Konsistenz mit
   dem im Projekt bereits etablierten Rhythmus (`quarterly_review.py` bei
   `elliott_wave`/`elliott_wave_stocks`/`t3_supertrend`), (b) einen
   Kompromiss zwischen genug Trägheit (tägliche Bot-Renditen sind
   verrauscht — monatliches Rebalancing würde stärker auf Rauschen statt
   echte Regimewechsel reagieren) und genug Reaktionsfähigkeit
   (jährliches Rebalancing wäre zu träge). Keine Optimierung über mehrere
   Intervalle durchgeführt (nur eine begründete Wahl, wie gefordert).
2. **Clustering-Methode: Single-Linkage.** Die im Original-Paper (López de
   Prado 2016) verwendete Methode. Ward-Linkage wurde AUSSCHLIESSLICH zur
   Robustheits-Illustration zusätzlich berechnet (siehe Ergebnis-Tabelle) —
   NICHT um das bessere Ergebnis auszuwählen, wie von der Aufgabenstellung
   ausdrücklich gefordert.
3. **Bootstrap-Quartal (das allererste Quartal im gemeinsamen
   Vergleichsfenster) läuft gleichgewichtet**, da noch keine
   Trainingshistorie existiert, aus der HRP etwas lernen könnte. Betrifft
   1 von 18 Quartalen.
4. **Fallback-Zuteilung bei unzureichender Datenbasis:** siehe Methodik
   oben (ausgeschlossene Bots behalten ihr normales 1/N-Gewicht,
   verbleibendes Kapital wird nur unter dem verlässlichen Teil-Universum
   gemäss HRP verteilt). Konservativste unter den plausiblen Varianten.
5. **Kombinierte Buy-and-Hold-Referenz:** gleichgewichtetes,
   NICHT-rebalanciertes Buy-and-Hold über die UNION der beiden bereits im
   Projekt etablierten Symbol-Universen (`config/top25_symbols.txt` fürs
   Krypto-Universum, `config/sp500_top150.txt` fürs Aktien-Universum) —
   175 Symbole, davon 161 mit durchgehenden Kursdaten im gemeinsamen
   Vergleichsfenster. Bewusst NICHT 9 einzelne, bot-spezifische
   Buy-and-Hold-Kurven gemittelt, da Krypto- bzw. Aktien-Bots sich jeweils
   dasselbe Symbol-Universum teilen und eine bot-weise Mittelung
   gemeinsame Symbole implizit mehrfach werten würde.
6. **Alle 9 Bots als EIN gemeinsames Universum behandelt** (nicht getrennt
   nach "live" vs. "Prototyp" wie in `portfolio_overview.py`'s zwei
   getrennten Analyse-Gruppen) — konsistent mit der Aufgabenstellung, die
   explizit von "allen 9 Bots gleich (je 11,1 %)" spricht (1/9 ≈ 11,1 %
   ergibt sich nur bei allen 9 zusammen, nicht bei der kleineren
   "nur live"-Teilmenge).
7. **Kennzahl:** Calmar-Ratio (Rendite % / |Max Drawdown| %), konsistent
   zur vorherigen Vol-Sizing-Untersuchung — keine der 9 Bots verwendet
   Sharpe/Sortino, daher wurde (wie dort) keine dieser Kennzahlen neu
   eingeführt.
8. **Live-DB vs. Backtest-Fallback:** in dieser Sandbox lief die
   Untersuchung durchgehend auf dem `equity_curve.csv`-Fallback (siehe
   Datenquelle oben) — dieselbe, bereits im Projekt validierte
   Priorisierungslogik würde in einer Umgebung mit befüllten Live-DBs
   automatisch (ohne Codeänderung) auf echte Live-Trades umschalten,
   sobald ein Bot `MIN_LIVE_CLOSED_TRADES` erreicht.

## Ergebnis

### Übergreifende Tabelle (gemeinsames Vergleichsfenster: 2022-03-18 bis 2026-06-27)

| Variante | Rendite | Max Drawdown | Calmar-Ratio |
|---|---|---|---|
| HRP (Walk-Forward, Single-Linkage) | 63,26 % | -4,93 % | 12,83 |
| Bestehende Gleichgewichtung (1/9, unrebalanciert) | 82,43 % | -6,33 % | 13,02 |
| Buy-and-Hold-Referenz (161 Symbole) | 158,17 % | -23,77 % | 6,65 |
| HRP (Robustheits-Illustration, Ward-Linkage) | 63,78 % | -4,93 % | 12,94 |
| Schlechtester Einzel-Bot (nur Max Drawdown, zum Vergleich) | — | -32,40 % | — |

(Maschinenlesbar identisch in `results/hrp_summary.json`; tägliche Kurven
in `results/combined_curves.csv`; alle 18 Quartals-Gewichte in
`results/quarterly_weights.csv`.)

### Einzel-Bot-Kennzahlen im selben Fenster (zur Einordnung)

| Bot | Rendite | Max Drawdown |
|---|---|---|
| Elliott Wave (Krypto) | 61,6 % | -0,2 % |
| Elliott Wave (Aktien) | 286,7 % | -1,7 % |
| rsi2_crypto | 29,4 % | -13,1 % |
| RSI-2 Mean-Reversion (Aktien, Prototyp) | 21,5 % | -11,6 % |
| T3/SuperTrend (Krypto) | 110,9 % | -22,2 % |
| turtle_soup_crypto | 112,5 % | **-32,4 %** |
| turtle_soup_stocks | 18,3 % | -23,0 % |
| volatility_breakout | 31,2 % | -22,4 % |
| volatility_breakout_crypto | 69,8 % | -16,8 % |

### Wichtiger Befund: die Datenbasis-Fallback-Regel war KEIN theoretischer Sonderfall

Ausgehend von der Annahme, mit ~4 Jahren gemeinsamer Historie und
hunderten bis tausenden Trades pro Bot würde die 30-Tage-Schwelle kaum je
greifen, wurde das explizit geprüft — mit einem deutlich anderen Ergebnis:
**17 von 18 Quartalen hatten mindestens einen ausgeschlossenen Bot**, und
sogar die vollständige, ungeschmälerte Gesamthistorie aller 9 Bots (nicht
nur ein einzelnes Trainingsfenster) zeigt bei rund der Hälfte aller 36
Bot-Paare "zu wenig Datenbasis" nach genau derselben, unveränderten
Konvention aus `portfolio_overview.py`. Grund: die Schwelle verlangt
gemeinsame **Handelstage** (Tage, an denen BEIDE Bots am selben Kalendertag
einen Trade abschliessen) — Bots mit vergleichsweise wenigen Trades
(`elliott_wave`: 144 Exits/106 Tage über 5 Jahre; `elliott_wave_stocks`:
469/322; `rsi2_crypto`: 392/224) koinzidieren mit anderen ebenso selten
handelnden Bots rein statistisch selten genug am selben Tag, um auch nach
Jahren nicht zuverlässig über 30 gemeinsame Tage zu kommen. `elliott_wave`,
`elliott_wave_stocks` und `rsi2_crypto` blieben deshalb in den letzten 6
Quartalen durchgehend ausserhalb des HRP-Teil-Universums (behielten aber
korrekt ihr normales 1/9-Gewicht) — nicht, weil sie generell zu wenig
Handelstage mit JEDEM anderen Bot hätten (einzelne Paare erreichen die
Schwelle durchaus), sondern weil das GRÖSSTE gegenseitig verlässliche
Teil-Universum ohne sie grösser ausfällt als jedes Teil-Universum, das sie
einschliesst. Das ist die korrekte, erwartbare Konsequenz einer
Clique-Suche, kein Fehler.

**Einordnung:** diese Häufigkeit ist eine direkte Folge der von der
Aufgabenstellung vorgegebenen, unveränderten Handelstage-Definition aus
`portfolio_overview.py` (in Teil 3 des Original-Skripts, ausserhalb dieser
Untersuchung, ohnehin bereits sichtbar) — keine Eigenheit der neuen
HRP-Untersuchung. Sie zeigt aber, dass die geforderte Fallback-Regel für
DIESES 9-Bot-Portfolio praxisrelevant und nicht nur ein hypothetischer
Randfall ist.

### Warum HRP hier nicht besser abschneidet als die bestehende Gleichgewichtung

Ein Blick auf die tatsächlich berechneten HRP-Gewichte in späteren
Quartalen (z. B. 2026-04-01, letztes Quartal) erklärt das Ergebnis: HRP
gewichtet **rein nach Varianzstruktur, blind gegenüber erzielter
Rendite**. In diesem Portfolio korrelieren gerade die beiden Bots mit dem
höchsten individuellen Drawdown (`turtle_soup_crypto`, -32,4 %;
`t3_supertrend`, -22,2 %) zugleich mit den zweit- und dritthöchsten
Einzelrenditen (112,5 % bzw. 110,9 %) — HRP reduziert deren Gewicht
konsequent auf 1,6–4,2 % (statt der naiven 11,1 %) und verteilt das
freiwerdende Kapital u. a. auf `rsi2_mean_reversion` (Gewicht bis zu
29,2 % statt 11,1 %) — den Bot mit der schwächsten Einzelrendite (21,5 %)
im gesamten Portfolio. HRP "bezahlt" damit in diesem konkreten Datensatz
systematisch Rendite für etwas weniger Volatilität, weil hohe Vola hier
zufällig mit hoher Rendite einherging — ein bekanntes, erwartbares
Charakteristikum eines rein risikobasierten (nicht renditegewichteten)
Verfahrens wie HRP, keine Fehlfunktion.

### Diversifikation: bereits die einfache Gleichgewichtung ist sehr stark

Sowohl HRP als auch die bestehende Gleichgewichtung drücken den maximalen
Drawdown drastisch unter den des schlechtesten Einzel-Bots
(-32,4 % → -4,9 % bzw. -6,3 %) — die Diversifikationswirkung des
Zusammenschlusses ALLER 9 unkorrelierten bis schwach korrelierten Bots
(siehe Korrelationsmatrix von `portfolio_overview.py`: praktisch alle
berechenbaren Paare liegen zwischen -0,09 und +0,10) ist hier so stark,
dass die GENAUE Gewichtungsmethode einen vergleichsweise kleinen
zusätzlichen Unterschied macht.

### Parameter-Stabilität / Overfitting-Signal

- **Clustering-Methode (Single- vs. Ward-Linkage):** nahezu identisches
  Ergebnis (Rendite 63,26 % vs. 63,78 %, Max Drawdown in beiden Fällen
  exakt -4,93 %, Calmar 12,83 vs. 12,94) — **kein
  Instabilitäts-/Overfitting-Warnsignal** bezüglich der Wahl der
  Clustering-Methode.
- **Quartal-zu-Quartal-Gewichtsverschiebung:** im Schnitt 0,116 (Summe der
  absoluten Gewichtsänderungen über alle 9 Bots pro Rebalancing), maximal
  0,390 an einem einzelnen Quartalsübergang. Das ist ein moderates, aber
  nicht alarmierendes Mass an Schwankung für ein auf nur ~9 Assets
  basierendes Clustering mit wachsender, aber anfangs noch dünner
  Trainingshistorie — am ehesten in den frühen Quartalen zu erwarten, wenn
  sich das Teil-Universum durch neu erreichte Datenbasis-Schwellen noch
  verändert (siehe "Wichtiger Befund" oben).

## Gesamteinschätzung (unaufgeregt, ohne Handlungsempfehlung)

Für dieses konkrete 9-Bot-Portfolio über den verfügbaren Vergleichszeitraum
bringt HRP keinen klaren Vorteil gegenüber der bestehenden, einfachen
Gleichgewichtung — die Calmar-Ratio ist nahezu identisch (marginal
schlechter bei HRP), bei spürbar niedrigerer absoluter Rendite. Der
Hauptgrund liegt nicht in einer Schwäche der HRP-Implementierung, sondern
darin, dass (a) die 9 Bots bereits von Haus aus nur sehr schwach
miteinander korrelieren (die Diversifikationswirkung ist bei JEDER
vernünftigen Gewichtung stark) und (b) HRP in diesem speziellen Datensatz
ausgerechnet die renditestärksten Bots als "riskant" identifiziert und
entsprechend abwertet. Die Wahl der Clustering-Methode (Single- vs.
Ward-Linkage) verändert das Ergebnis kaum — das Verfahren ist in diesem
Sinne robust, auch wenn es hier keinen Mehrwert liefert.

Ein methodisch bemerkenswerter Nebenbefund ist die Häufigkeit, mit der die
bestehende 30-Tage-Datenbasis-Schwelle greift (17 von 18 Quartalen
betroffen) — das ist eine direkte, bereits im Original-Skript angelegte
Eigenschaft der Handelstage-Definition, kein neues Problem dieser
Untersuchung, aber ein Hinweis darauf, dass die Fallback-Logik für dieses
Portfolio praktisch relevant und nicht nur eine theoretische
Absicherung ist.

**Keine der beobachteten Effekte ist so gross oder eindeutig, dass sich
daraus eine generelle Empfehlung für oder gegen eine HRP-Gewichtung
ableiten liesse — diese Entscheidung liegt bewusst beim Nutzer in einer
separaten, künftigen Session.**

## Explizit ausserhalb des Scopes dieser Untersuchung

Trend-Overlay, Trailing-Stops (separate Backlog-Punkte), jegliche
Live-Code-Änderung, jegliche Aktivierungsempfehlung. Keine Optimierung
über mehrere Rebalancing-Intervalle oder Clustering-Methoden — nur je eine
begründete Wahl plus eine einzelne Robustheits-Illustration, wie von der
Aufgabenstellung gefordert.

## Reproduzierbarkeit

```
cd research/hrp_portfolio
python3 test_hrp_core.py      # 20 Sanity-/Regressionstests des HRP-Kernmoduls
python3 run_walk_forward.py   # vollstaendige Walk-Forward-Untersuchung, schreibt results/
```
