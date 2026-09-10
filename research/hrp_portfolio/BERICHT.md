# Hierarchical Risk Parity (HRP) — Backtest-Only-Untersuchung für die Portfolio-Gewichtung

> ## ⚠ Nachtrag: korrigierte Kapitalkurven-Grundlage (Sync-Check PR #24)
>
> Die `equity_curve.csv`-Dateien, auf denen diese Studie aufbaut, beruhten bei
> **5 der 9 Bots nicht auf der Live-Konfiguration**. Die Untersuchung wurde
> deshalb mit korrigierten Kurven wiederholt.
>
> **Die Kernaussage hält — und zwar deutlicher als zuvor.** HRP bleibt
> risikoadjustiert hinter der einfachen Gleichgewichtung zurück; der Abstand
> wächst von **−0,19 auf −0,46 Calmar-Punkte**. Die absoluten Zahlen
> verschieben sich dagegen spürbar (Calmar 13,02 → **10,91**).
>
> **Zusätzlich gefunden:** die gespeicherte `elliott_wave`-Kurve
> (`results/equity_curve.csv`) stammt aus dem Initial Commit und deckt nur
> 5 Symbole / 144 Trades ab, während der heutige Code 782 Trades über 18
> Symbole erzeugt. Das ist **kein** Sync-Problem, sondern eine davon
> unabhängige Veralterung derselben Datengrundlage — sie wird getrennt
> ausgewiesen, nicht mit der Korrektur vermischt.
>
> Details, Regressionscheck (15/15) und Annahmen: Abschnitt **„Nachtrag N"** am
> Ende dieses Berichts.


> ## ⚠⚠ Zweiter Nachtrag: die Kernaussage kippt
>
> Die Kurven waren ein **zweites Mal** veraltet: seit der ersten Korrektur sind
> die Sync-Befunde selbst gemergt worden (PR #40–#42, #45, #51/#52), und die
> beiden Elliott-Bots haben einen **Look-Ahead-Fix** bekommen. Die Untersuchung
> wurde deshalb erneut wiederholt — mit Kurven, die die **heutige**
> `equity_simulation.py` erzeugt.
>
> **Die Kernaussage hält diesmal NICHT.** Mit den heutigen Kurven liegt HRP
> risikoadjustiert erstmals **vor** der Gleichgewichtung:
>
> | Grundlage | HRP − Gleichgewichtung (Calmar) | Kernaussage |
> |---|---:|---|
> | Erstfassung | −0,1905 | hält |
> | erste Korrektur | −0,4627 | hält |
> | **zweite Korrektur** | **+0,1424** | **hält nicht** |
>
> Der Vorzeichenwechsel ist kein Rechenfehler: 24/24 Referenzwerte der beiden
> früheren Fassungen werden exakt reproduziert, und die Robustheitsprobe mit
> Ward-Linkage kippt mit (+0,1157). Er hängt aber, wie sich in Nachtrag V
> herausgestellt hat, an der einen nicht live-konformen Kurve. Der **Abstand
> ist ausserdem klein** — +0,14 auf ein Calmar-Niveau von rund 6, also gut
> 2 %. Klein war er in den früheren Fassungen auch (−0,19 / −0,46).
>
> Hier wird das nur festgehalten, nicht weitergedeutet und nicht zum Anlass
> für eine dritte Runde genommen — die Einordnung liegt beim Nutzer.
>
> Details, Bestandsaufnahme und Dreifach-Vergleich: Abschnitt **„Nachtrag Z"**
> am Ende dieses Berichts.
>
> **⚠ Nachträglich geprüft und wieder umgekehrt — siehe Nachtrag V.** Der
> Nachtrag Z hat selbst benannt, dass die `volatility_breakout_crypto`-Kurve
> als einzige nicht live-konform ist (BTC-Regimefilter live aktiv, im Backtest
> nicht angewendet). Mit korrekt gefilterter Kurve liegt HRP wieder **hinten**:
> **−0,0432** statt +0,1424. Die Kernaussage hält damit doch — allerdings mit
> einem noch kleineren Abstand als der Vorsprung, den sie ersetzt. Der
> Vorzeichenwechsel aus Nachtrag Z war ein Artefakt genau dieser einen Lücke.


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
| HRP (Walk-Forward, Single-Linkage) | 63,26 % | -4,93 % | 12,83 ⚠ |
| Bestehende Gleichgewichtung (1/9, unrebalanciert) | 82,43 % | -6,33 % | 13,02 ⚠ |
| ↳ *dieselben zwei Zeilen mit korrigierten Kurven (siehe Nachtrag N)* | 76,47 % / 107,13 % | −7,32 % / −9,82 % | **10,45 / 10,91** |
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


---

# Nachtrag N: dieselbe Untersuchung auf korrigierter Kapitalkurven-Grundlage

## N0. Entscheidungsgrundlage

### Der Anlass

Der Sync-Check (PR #24) hat belegt: bei **5 der 9 Bots** weicht die Konfiguration
in `equity_simulation.py` von der Live-Konfiguration in `live_params.py` ab. Die
Dateien `results/<bot>/equity_curve.csv` sind die Ausgabe genau dieser Läufe —
und diese Studie baut ihr Portfolio ausschliesslich darauf auf. Sie ist damit
vollständig betroffen (Einstufung des Sync-Checks: **hoch**).

### Was geändert wurde — und was ausdrücklich nicht

**Nur die Kapitalkurven.** Rebalancing-Intervall (Kalenderquartale),
Linkage-Verfahren (Single, Ward als Illustration), Mindest-Datenbasis-Schwelle
(30 gemeinsame Handelstage), die Bootstrap-Fallback-Regel, die
Buy-and-Hold-Referenz und die komplette Auswertung werden **Funktion für
Funktion unverändert aus `run_walk_forward.py` importiert und aufgerufen**. Es
gibt in `nachtrag_sync_korrektur.py` keine zweite Umsetzung derselben Rechnung —
eine eigene Neufassung hätte die Vergleichbarkeit zur Erstfassung still
zerstören können.

Unangetastet bleiben ausserdem: `shared/portfolio_overview.py` (die Kurven
werden über seine unveränderten Funktionen geladen, nur die *Pfade* werden
vorher umgebogen), sämtliche `results/*/equity_curve.csv`, und jeder Bot-Code.

### Drei Grundlagen statt zwei

| Grundlage | Was getauscht wird | Rolle |
|---|---|---|
| `original` | nichts | **Regressionscheck** gegen `results/hrp_summary.json` |
| `korrigiert` | die 5 abweichenden Bots, Live-Konfiguration | **primär** — die auftragsgemässe Korrektur |
| `korrigiert_plus_veraltet` | zusätzlich `elliott_wave` neu erzeugt | eigenständiger Nebenfund, siehe N3 |

### Regressionschecks — zweifach, vor allem anderen

**1. Die vier synchronen Bots als Probe des Erzeugers.** Sie werden mitgerechnet,
obwohl sich bei ihnen nichts ändern *kann*. Drei von ihnen (`t3_supertrend`,
`rsi2_crypto`, `turtle_soup_crypto`) ergeben eine **byteweise identische** Datei
zur bestehenden `results/`-Kurve. Wäre das nicht so, wäre der Erzeuger falsch —
und nicht etwa die Korrektur wirksam. Der vierte (`elliott_wave`) weicht ab, aus
einem gemessenen und dokumentierten Grund (N3); das Skript **verlangt** diese
Abweichung ausdrücklich, statt sie durchzuwinken.

**2. Die fünf abweichenden Bots gegen den Sync-Check.** Alle fünf treffen die
dort veröffentlichten Kennzahlen der Live-Variante exakt:

| Bot | ausgeführt | Rendite | Max DD |
|---|---|---|---|
| `elliott_wave_stocks` | 288 | +3084,09 % | −9,79 % |
| `volatility_breakout` | 1454 | +224,41 % | −23,97 % |
| `turtle_soup_stocks` | 8915 | +145,59 % | −29,91 % |
| `rsi2_mean_reversion` | 4232 | +36,75 % | −21,05 % |
| `volatility_breakout_crypto` | 207 | +49,03 % | −16,29 % |

**3. Die Basis `original` gegen die Erstfassung: 15/15 exakt** — HRP,
Gleichgewichtung, Buy-and-Hold, Ward-Illustration (je Rendite, Drawdown,
Calmar), Symbolzahl, schlechtester Einzel-Bot und Gewichts-Stabilität. Ohne
diesen Durchlauf bricht das Skript ab.

### Was diesen Befund umstossen würde

* Eine andere Definition von „Live-Konfiguration". Sie ist hier wörtlich aus
  `research/sync_check/impact.py` übernommen, nicht neu erfunden.
* Die `elliott_wave`-Veralterung (N3): sie verschiebt die Zahlen weit stärker
  als die Sync-Korrektur, ist aber selbst durch den in PR #21 nachgewiesenen
  Zigzag-Look-Ahead verzerrt. Solange dieser Bias besteht, ist keine der beiden
  `elliott_wave`-Kurven eine belastbare Grundlage.
* Ein längeres gemeinsames Fenster. Es endet weiterhin 2026-06-27, weil die
  kürzeste Bot-Kurve dort aufhört.

---

## N1. Ergebnis: die Kernaussage hält, die Zahlen nicht

Rendite % / Max Drawdown % / Calmar:

| Grundlage | Fenster | HRP (Walk-Forward) | Gleichgewichtung | **HRP − Gleichgewichtung** |
|---|---|---|---|---|
| `original` | 2022-03-18 … 2026-06-27 | 63,26 / −4,93 / **12,83** | 82,43 / −6,33 / **13,02** | **−0,19** |
| **`korrigiert`** | 2022-03-18 … 2026-06-27 | 76,47 / −7,32 / **10,45** | 107,13 / −9,82 / **10,91** | **−0,46** |
| `korrigiert_plus_veraltet` | 2022-03-18 … 2026-08-20 | 132,93 / −5,39 / **24,66** | 255,95 / −4,82 / **53,10** | **−28,44** |

**Die Kernaussage dieser Studie — HRP bringt gegenüber der einfachen
Gleichgewichtung keinen risikoadjustierten Vorteil — hält in allen drei
Grundlagen.** Sie wird durch die Korrektur nicht schwächer, sondern
deutlicher: der Abstand verdoppelt sich von −0,19 auf −0,46 Calmar-Punkte.

Die absoluten Zahlen verschieben sich dagegen spürbar. Beide Varianten gewinnen
Rendite (die korrigierten Bots handeln mehr und grösser) und verlieren
gleichzeitig beim Drawdown; unter dem Strich fällt die Calmar-Ratio beider um
rund zwei Punkte. **Wer die Zahlen dieses Berichts zitiert, muss die korrigierte
Zeile nehmen.**

Die Ward-Robustheits-Illustration bleibt ebenfalls unauffällig: 10,40 gegen
10,45 (Single) — kein Instabilitätssignal, wie in der Erstfassung.

---

## N2. Was sich an den Gewichten ändert

Die Gewichte des letzten Quartals:

| Bot | `original` | `korrigiert` |
|---|---|---|
| `rsi2_mean_reversion` | 0,292 | **0,319** |
| `turtle_soup_stocks` | 0,129 | **0,180** |
| `volatility_breakout` | 0,159 | **0,096** |
| `elliott_wave`, `elliott_wave_stocks`, `rsi2_crypto` | je 0,111 | je 0,111 (Fallback) |
| `volatility_breakout_crypto` | 0,042 | 0,042 |
| `t3_supertrend` | 0,029 | 0,019 |
| `turtle_soup_crypto` | 0,016 | 0,011 |

Die Rangfolge bleibt im Kern erhalten. Auffällig ist `volatility_breakout`: mit
dem korrekten Positionslimit 15 (statt 8) handelt er mehr und schwankt stärker,
und HRP gewichtet ihn dafür **ab** (0,159 → 0,096). Das ist genau das Verhalten,
das der Bericht in „Warum HRP hier nicht besser abschneidet" beschreibt — HRP
stuft die renditestärkeren Bots als riskant ein. Die Korrektur verstärkt diesen
Mechanismus, statt ihn abzuschwächen.

Die Gewichts-Stabilität verbessert sich leicht (mittlere Quartalsverschiebung
0,116 → 0,095); die drei Bots im Datenbasis-Fallback (je 1/9) sind unverändert
dieselben. Der Befund „die Fallback-Regel war kein theoretischer Sonderfall"
bleibt bestehen.

---

## N3. Nebenfund: die gespeicherte `elliott_wave`-Kurve ist veraltet

`shared/portfolio_overview.py` liest für diesen Bot aus
`results/equity_curve.csv` (historischer Sonderpfad, `LEGACY_EQUITY_CSV_PATHS`).
Diese Datei stammt aus dem **Initial Commit** und wurde seither nie neu erzeugt:

| | gespeicherte Datei | heutiger Code |
|---|---|---|
| Trades | 144 | **782** |
| Symbole | 5 (BTC, ETH, BNB, SOL, XRP) | **18** |
| letzter Eintrag | 2026-06-27 | 2026-08-26 |

Das ist **keine** Folge der Sync-Abweichung — `elliott_wave` ist
konfigurationsseitig synchron — sondern eine davon unabhängige Veralterung
derselben Datengrundlage. Sie trifft beide Studien, die auf diesen Kurven
aufbauen.

**Deshalb wird sie getrennt ausgewiesen und nicht stillschweigend
mitkorrigiert.** Die Wirkung ist erheblich: die Gleichgewichtung springt auf
Calmar 53,10, weil die neu erzeugte `elliott_wave`-Kurve +2185 % bei −1,83 %
Drawdown liefert und das Portfolio dominiert.

**Diese Zahl ist jedoch nicht besser, sondern anders verzerrt.** PR #21 hat
gemessen, dass der Elliott-Wave-Backtest zum Zigzag-Wellenende einsteigt, dem
per Konstruktion rückwirkend eine Aufwärtsbewegung folgt — bei **100 % der
Trades**. Eine Kurve mit +2185 % und fast keinem Drawdown ist genau das
erwartete Erscheinungsbild dieses Look-Aheads. Die Basis
`korrigiert_plus_veraltet` wird deshalb ausgewiesen, um den Effekt sichtbar zu
machen, und **nicht** als die belastbarere Grundlage empfohlen.

Bemerkenswert bleibt: selbst unter dieser Verzerrung dreht sich die Kernaussage
nicht um — HRP liegt dort mit **−28,44 Calmar-Punkten** so weit zurück wie nie.

---

## N4. Getroffene Annahmen dieses Nachtrags

Zusätzlich zu den Annahmen der Erstfassung, die alle unverändert gelten:

**N-A1 — Die Definition von „Live-Konfiguration" wird übernommen, nicht neu
gefasst.** Die Fallunterscheidung je Bot stammt wörtlich aus
`research/sync_check/impact.py::build`. Eine eigene Neufassung hätte still eine
zweite, abweichende Definition erzeugt.

**N-A2 — `elliott_wave_stocks` behält seine Backtest-Allokation.**
`live_params.py` dokumentiert dort keine Allokation; getauscht wird nur
`USE_TAKE_PROFIT` und das Positionslimit. Dieselbe Annahme wie im Sync-Check.

**N-A3 — Die Veralterung wird getrennt geführt** (`KNOWN_STALE_BOTS`), damit
Sync-Korrektur und Veralterung nicht in einer Zahl verschmelzen.

**N-A4 — Das gemeinsame Fenster ergibt sich wie in der Erstfassung** aus dem
Schnitt aller Bot-Kurven und wurde nicht fixiert. In der Basis
`korrigiert_plus_veraltet` verlängert es sich dadurch bis 2026-08-20; die
beiden anderen Grundlagen enden unverändert am 2026-06-27.

**N-A5 — Die Buy-and-Hold-Referenz bleibt unverändert** (158,17 % / −23,77 % /
6,65). Sie hängt an Symbolen und Zeitfenster, nicht an den Bot-Kurven — was der
Lauf bestätigt: in den Basen `original` und `korrigiert` ist sie identisch.

---

## N5. Neue Dateien und Reproduktion

| Datei | Rolle |
|---|---|
| `corrected_curves.py` | erzeugt die neun korrigierten Kurven und biegt die Quellpfade um |
| `nachtrag_sync_korrektur.py` | rechnet die drei Grundlagen über die unveränderten Funktionen von `run_walk_forward.py` |
| `test_corrected_curves.py` | 14 Sanity-Checks der Tausch-Logik |
| `corrected_curves/` | die neun erzeugten Kurven + Kennzahlen je Bot |
| `results/nachtrag_sync_korrektur.json` | vollständige Ergebnisse aller drei Grundlagen |

```
python3 test_corrected_curves.py       # 14 Checks
python3 nachtrag_sync_korrektur.py     # erzeugt Kurven, prüft 15/15, rechnet 3 Grundlagen
```

Das Skript bricht ab, sobald eine der drei Proben fehlschlägt.

---

# Nachtrag Z — zweite Korrektur der Kapitalkurven (2026-09-08)

## Z0. Entscheidungsgrundlage

**Warum überhaupt ein zweiter Nachtrag.** Der erste Nachtrag hat von Hand
nachgebildet, wie die fünf damals abweichenden Bots *mit* Live-Konfiguration
gerechnet hätten. Inzwischen sind genau diese Befunde gemergt — die
Nachbildung ist damit nicht mehr die Korrektur, sondern selbst ein
historischer Stand. Dazu kommen Änderungen, die mit dem Sync-Thema nichts zu
tun haben und trotzdem dieselbe Datengrundlage treffen, allen voran ein
Look-Ahead-Fix bei beiden Elliott-Bots.

**Warum die Kurven diesmal nicht nachgebildet, sondern erzeugt werden.** Die
zweite Korrektur ruft nicht mehr einzelne Bot-Funktionen mit passend gesetzten
Parametern auf, sondern führt den `__main__`-Block der heutigen
`equity_simulation.py` aus (`corrected_curves.generate_heute`). Der
Unterschied ist nicht kosmetisch: eine Nachbildung ist eine zweite Fassung
derselben Rechnung und läuft still auseinander, sobald sich im Bot ein Aufruf
ändert — genau das ist inzwischen mehrfach passiert. Der `__main__`-Block ist
dagegen per Definition das, was die gespeicherte `results/`-Kurve erzeugt hat.

**Warum zwei Regressionsanker statt einem.** Ein Dreifach-Vergleich ist nur so
viel wert wie die Vergleichbarkeit seiner Spalten. Geprüft wird deshalb beides:
dass die Auswertung unverändert rechnet (Basis `original` trifft
`results/hrp_summary.json`) *und* dass die alte Grundlage exakt reproduziert
wird (Basis `korrigiert_v1` trifft `results/nachtrag_sync_korrektur.json`).
**24/24 Referenzwerte bestätigt, 0 abweichend.** Ohne den zweiten Anker wüsste
man nicht, ob eine Verschiebung von den neuen Kurven kommt oder davon, dass
die alte Spalte anders gerechnet wurde als damals.

**Was unverändert bleibt.** Rebalancing-Intervall, Linkage-Verfahren,
Mindest-Datenbasis-Schwelle, Bootstrap-Fallback, Buy-and-Hold-Referenz und die
gesamte Auswertung kommen unverändert aus `run_walk_forward.py` — aufgerufen
über `nachtrag_sync_korrektur.analyse()`, also wörtlich dieselbe Funktion, die
schon die erste Korrektur benutzt hat. Es gibt keine zweite Umsetzung
derselben Rechnung. `shared/portfolio_overview.py`, `results/*/equity_curve.csv`,
`corrected_curves/` und jeder Bot-Code bleiben unangetastet.

## Z1. Bestandsaufnahme: welche Bots rechnen heute anders?

Nicht aus den Commit-Titeln gelesen, sondern gemessen — Kurve gegen Kurve,
per SHA-256:

| Bot | ggü. `results/` | ggü. 1. Korrektur | ausgeführt (1. → 2.) | Rendite % (1. → 2.) | Max DD % (1. → 2.) |
|---|---|---|---:|---:|---:|
| `elliott_wave` | anders | **anders** | 782 → **130** | 2.184,96 → **67,77** | −1,83 → **−10,17** |
| `elliott_wave_stocks` | anders | **anders** | 288 → **395** | 3.084,09 → **352,72** | −9,79 → **−22,44** |
| `volatility_breakout_crypto` | identisch | **anders** | 207 → **310** | 49,03 → **71,26** | −16,29 → **−16,77** |
| `rsi2_crypto` | identisch | identisch | 392 | 28,37 | −13,30 |
| `rsi2_mean_reversion` | anders | identisch | 4.232 | 36,75 | −21,05 |
| `t3_supertrend` | identisch | identisch | 656 | 129,64 | −22,20 |
| `turtle_soup_crypto` | identisch | identisch | 1.414 | 177,59 | −32,40 |
| `turtle_soup_stocks` | anders | identisch | 8.915 | 145,59 | −29,91 |
| `volatility_breakout` | identisch | identisch | 1.454 | 224,41 | −23,97 |

**Drei Kurven haben sich bewegt**, und zwar aus zwei belegbaren Gründen:

* `elliott_wave` und `elliott_wave_stocks` — Commit `839500b`
  *„Elliott-Wave-Backtest korrigieren: beide Look-Ahead-Kanäle beheben"*.
  Das ist die mit Abstand grösste Verschiebung der ganzen Studie: die
  Renditen der beiden Elliott-Bots fallen um den Faktor 32 bzw. 9. Der alte
  Wert war nicht falsch parametriert, sondern durch Vorausschau überhöht.
* `volatility_breakout_crypto` — Commit `9bb230f` (PR #45), Kopplung der
  wirksamen Backtest-Defaults an `live_params.py`.

**Sechs Kurven sind unverändert** — darunter ausgerechnet die drei Bots aus
PR #40–#42 (`rsi2_mean_reversion`, `turtle_soup_stocks`,
`volatility_breakout`). Ihre gemergte Fassung trifft die Handnachbildung des
ersten Nachtrags **auf die Nachkommastelle**. Das ist eine unabhängige
Bestätigung, dass die erste Korrektur damals richtig gerechnet hat.

Ebenso unverändert: `rsi2_crypto`, `t3_supertrend` und `turtle_soup_crypto`.
Bei den ersten beiden hatten PR #51/#52 zugesagt, nur die *Quelle* der Werte
zu vereinheitlichen und keine Zahl anzufassen — die identischen Kurven
bestätigen das nachträglich von aussen.

**Nebenbeobachtung, hier nicht behoben:** bei **fünf** Bots weicht die im Repo
gespeicherte `results/<bot>/equity_curve.csv` vom heutigen Code ab. Sie wurde
nach den Korrekturen nie neu erzeugt. Diese Studie liest sie nur für die
Vergleichsspalte `original`; für alles andere sind die frisch erzeugten Kurven
massgeblich.

## Z2. Dreifach-Vergleich

Rendite % / Max Drawdown % / Calmar:

| Grundlage | Fenster | HRP (Walk-Forward) | Gleichgewichtung | Buy-and-Hold |
|---|---|---|---|---|
| Erstfassung | 2022-03-18 … 2026-06-27 | 63,26 / −4,93 / **12,83** | 82,43 / −6,33 / **13,02** | 158,17 / −23,77 / 6,65 |
| 1. Korrektur | 2022-03-18 … 2026-06-27 | 76,47 / −7,32 / **10,45** | 107,13 / −9,82 / **10,91** | 158,17 / −23,77 / 6,65 |
| 1. Korrektur + veraltet | 2022-03-18 … 2026-08-20 | 132,93 / −5,39 / **24,66** | 255,95 / −4,82 / **53,10** | 159,12 / −23,77 / 6,69 |
| **2. Korrektur** | 2022-03-18 … 2026-08-20 | 72,53 / −12,00 / **6,04** | 72,12 / −12,22 / **5,90** | 159,12 / −23,77 / 6,69 |

Das Gesamtbild verschiebt sich deutlich: das Portfolio ist mit den heutigen
Kurven **risikoreicher** (Max Drawdown −6,3 % → −12,2 % bei Gleichgewichtung)
und **weniger rentabel** (82,4 % → 72,1 %) als in der Erstfassung. Beides geht
im Wesentlichen auf die beiden Elliott-Bots zurück, deren überhöhte Kurven
bisher Rendite beisteuerten und Drawdown verwässerten.

Der Buy-and-Hold-Vergleich bleibt über alle vier Grundlagen bestehen: das
Portfolio liegt in der Rendite hinter Buy-and-Hold (72,1 % vs. 159,1 %), bei
deutlich kleinerem Drawdown (−12,2 % vs. −23,8 %).

## Z3. ⚠ Die Kernaussage kippt

Die Kernaussage dieser Studie lautete: **HRP bringt gegenüber der einfachen
Gleichgewichtung keinen risikoadjustierten Vorteil.** Gemessen wird sie am
Abstand der Calmar-Ratios.

| Grundlage | HRP − Gleichgewichtung (Calmar) | Ward-Linkage (Robustheitsprobe) | Kernaussage |
|---|---:|---:|---|
| Erstfassung | −0,1905 | −0,0850 | hält |
| 1. Korrektur | −0,4627 | −0,5078 | hält |
| 1. Korrektur + veraltet | −28,4394 | −28,6230 | hält |
| **2. Korrektur** | **+0,1424** | **+0,1157** | **hält nicht** |

**Zum ersten Mal in allen drei Fassungen liegt HRP vorn.** Der Befund ist
nicht auf eine Methodenwahl zurückzuführen: die im ursprünglichen Design
vorgesehene Robustheitsprobe mit Ward-Linkage kippt mit, in dieselbe Richtung
und in derselben Grössenordnung.

Zur Einordnung der Grösse — ohne Deutung: +0,1424 auf ein Calmar-Niveau von
rund 6,0 sind gut 2 %. In den früheren Fassungen war der Abstand mit −0,19 und
−0,46 ähnlich klein; gross war er nur in der Nebenspalte
„1. Korrektur + veraltet".

**Auftragsgemäss wird das hier nur festgehalten.** Es wird nicht
weitergedeutet, es wird keine dritte Runde angestossen, und es folgt keine
Empfehlung. Was daraus folgt, entscheidet der Nutzer.

## Z4. Getroffene Annahmen und Grenzen dieses Nachtrags

1. **„Heutiger Stand" heisst: was `equity_simulation.py` rechnet — nicht: was
   live läuft.** Bei `volatility_breakout_crypto` fallen die beiden
   auseinander: `live_params.py` setzt `BTC_REGIME_FILTER_ENABLED = True`, der
   Backtest wendet den Filter aber bewusst nicht an (dokumentiert im Kopf von
   `equity_simulation.py`, PR #45). Die v2-Kurve dieses Bots (71,26 %) ist
   damit **nicht** live-konform; die Live-Variante läge bei 49,03 % (Sync-Check
   PR #24). Für diesen einen Bot war die erste Korrektur näher an der
   Live-Konfiguration als die zweite. Eine Grundlage, die für diesen Bot die
   gefilterte Kurve einsetzt, wurde bewusst **nicht** zusätzlich gerechnet —
   das wäre die dritte Runde, die die Aufgabe ausdrücklich ausschliesst.
2. **Die erste Korrektur lässt sich nicht mehr wiederholen.**
   `nachtrag_sync_korrektur.py` prüft seine Kurven gegen die im Sync-Check
   veröffentlichten Kennzahlen; für `elliott_wave_stocks` trifft es sie nach
   dem Look-Ahead-Fix nicht mehr (395 statt 288 Trades, 352,72 % statt
   3.084,09 %) und bricht ab — **nachdem** es die CSVs bereits geschrieben hat.
   Ein Lauf auf `corrected_curves/` würde die gespeicherte v1-Grundlage also
   überschreiben und danach scheitern. Diese Prüfung wurde deshalb in einem
   temporären Verzeichnis gefahren; `corrected_curves/` ist unangetastet. Die
   v1-Spalte dieses Berichts stammt aus den **gespeicherten** Kurven, nicht aus
   einem neuen Lauf.
3. **Der Attrappen-Ansatz wurde verschärft.** Die Attrappen des zweiten
   Nachtrags **werfen** bei jedem Netzzugriff, statt leere Daten zu liefern.
   Eine Attrappe, die einen leeren DataFrame zurückgibt, lässt einen
   versehentlichen Abruf durchgehen: der Lauf rechnet mit weniger Symbolen
   weiter und meldet eine Kurve, die niemand als falsch erkennt. Ausnahme mit
   Grund: `binance.client.Client` muss sich **erzeugen** lassen, weil
   `shared/fetch_multi_data.py` auf Modulebene eine Instanz anlegt; geworfen
   wird stattdessen bei jedem Methodenaufruf.
4. **Fensterwechsel.** Die zweite Korrektur endet am 2026-08-20 statt am
   2026-06-27, weil die neu erzeugte `elliott_wave`-Kurve weiter reicht als
   die gespeicherte. Das gemeinsame Fenster ist damit rund zwei Monate länger
   als in Erstfassung und erster Korrektur — die Spalte
   „1. Korrektur + veraltet" nutzt dasselbe Fenster und ist deshalb der
   fenstergleiche Vergleichspartner der zweiten Korrektur.
5. Alles Übrige — Rebalancing, Linkage, Schwellen, Buy-and-Hold-Referenz —
   unverändert aus der Erstfassung; siehe Abschnitt „Getroffene Annahmen
   (vollständig)" und N4.

## Z5. Neue Dateien und Reproduktion

| Datei | Zweck |
|---|---|
| `corrected_curves.py` | ergänzt um `generate_heute()` und `vorhandene_kurven()` — der bestehende Erzeuger der ersten Korrektur bleibt unverändert daneben stehen |
| `nachtrag_sync_korrektur_v2.py` | dieser Nachtrag; ruft die Auswertung über `nachtrag_sync_korrektur.analyse()` auf |
| `corrected_curves_v2/` | die neun neu erzeugten Kurven samt Kennzahlen |
| `results/nachtrag_sync_korrektur_v2.json` | vollständige Zahlen aller vier Grundlagen |

```
python3 research/hrp_portfolio/nachtrag_sync_korrektur_v2.py
```

Erwartete Ausgabe: `24 Referenzwerte bestaetigt, 0 abweichend.` Der Lauf
erzeugt die neun Kurven neu (einige Minuten) und rührt weder `results/<bot>/`
noch `corrected_curves/` an.

---

# Nachtrag V — `volatility_breakout_crypto` mit BTC-Regimefilter (2026-09-08)

## V0. Die Frage und die Antwort

Nachtrag Z hat die Kernaussage kippen sehen — und im selben Atemzug die eine
Lücke benannt, die das Ergebnis tragen könnte: die
`volatility_breakout_crypto`-Kurve ist die einzige der neun, die **nicht
live-konform** ist. `live_params.py` setzt `BTC_REGIME_FILTER_ENABLED = True`,
`equity_simulation.py` wendet den Filter bewusst nicht an (dokumentiert seit
PR #45). Bei einem Vorsprung von nur gut 2 % konnte das den Ausschlag geben.

**Antwort: der HRP-Vorteil kippt zurück.**

| Grundlage | HRP − Gleichgewichtung (Calmar) | Ward-Linkage | HRP besser? |
|---|---:|---:|---|
| Erstfassung | −0,1905 | −0,0850 | nein |
| 1. Korrektur | −0,4627 | −0,5078 | nein |
| 2. Korrektur (Nachtrag Z) | **+0,1424** | +0,1157 | **ja** |
| **2. Korrektur, VBC live-konform** | **−0,0432** | **−0,0330** | **nein** |

Der Filter verschiebt den Abstand um **−0,1856** und dreht damit das
Vorzeichen. Die Robustheitsprobe mit Ward-Linkage dreht mit.

**Die ursprüngliche Kernaussage der Studie hält also doch** — HRP bringt
gegenüber der einfachen Gleichgewichtung keinen risikoadjustierten Vorteil.

**Mit einer Einschränkung, die zur Redlichkeit gehört:** der neue Abstand ist
noch kleiner als der Vorsprung, den er ersetzt. −0,0432 auf ein Calmar-Niveau
von rund 6,17 sind **0,7 %**; der Vorsprung in Nachtrag Z waren 2,4 %. Die
dritte in der Aufgabe genannte Möglichkeit — „kein klarer Unterschied mehr" —
beschreibt die Lage auf dieser Kurvengrundlage mindestens so gut wie ein
Richtungsurteil. Das Vorzeichen ist eindeutig; die Grösse ist es nicht.

## V1. Was genau getauscht wurde

Acht Kurven **unverändert** aus `corrected_curves_v2/`. Die neunte neu:

| | ausgeführt | Rendite % | Max DD % |
|---|---:|---:|---:|
| `volatility_breakout_crypto` ohne Filter (Nachtrag Z) | 310 | 71,26 | −16,77 |
| **mit BTC-Regimefilter** | **207** | **49,03** | **−16,29** |

Der Filter entfernt **126 der 359 gefundenen Trades** (359 → 233), nämlich
die, die in einem BTC-Abwärtsregime eingestiegen wären; ausgeführt werden
danach 207 statt 310. Die Kennzahlen der gefilterten Variante
treffen exakt die im Sync-Check (PR #24) veröffentlichten Live-Zahlen —
unabhängige Bestätigung, dass die richtige Variante gerechnet wurde.

## V2. Warum der Vergleich dem Filter zuzurechnen ist

Zwei Dinge mussten stimmen, sonst wäre die Differenz nicht dem Filter
zuzuschreiben, sondern dem Testaufbau.

**1. Die Nachbildung muss exakt der heutigen Rechnung entsprechen.**
`generate_heute()` führt den `__main__`-Block per `runpy` aus — genau deshalb
lässt sich dort nicht zwischen `collect_all_trades()` und
`simulate_portfolio()` eingreifen: beide Namen werden im ausgeführten Skript
selbst gebunden, ein Monkey-Patch von aussen erreicht sie nicht. Diese
Variante bildet die vier wirksamen Zeilen des `__main__`-Blocks deshalb nach —
denselben Weg, den `corrected_curves._WORKER` für diesen Bot schon gegangen
ist, mit `compute_btc_regime` / `filter_trades_by_regime` aus dem
unveränderten `regime_filter.py`.

Eine Nachbildung kann still abweichen. Sie läuft deshalb **immer zuerst ohne
Filter**, und das Ergebnis muss die v2-Kurve **byteweise** treffen. Es tut es
(310 / 71,26 % / −16,77 %). Schlägt diese Leerprobe fehl, bricht das Modul ab,
statt eine unbelastbare Zahl zu liefern.

**2. Die acht übernommenen Kurven müssen dieselbe Rechnung ergeben wie in
Nachtrag Z.** Dafür gibt es hier **drei** Regressionsanker statt zwei:

| Anker | trifft | |
|---|---|---|
| `original` | `results/hrp_summary.json` | Erstfassung |
| `korrigiert_v1` | `results/nachtrag_sync_korrektur.json` | 1. Korrektur |
| `korrigiert_v2` | `results/nachtrag_sync_korrektur_v2.json` | 2. Korrektur |

**27/27 Referenzwerte bestätigt, 0 abweichend** — inklusive der
Ward-Robustheitsprobe in allen drei Fassungen. Der dritte Anker ist hier der
entscheidende: er belegt, dass die neue Grundlage sich von Nachtrag Z
ausschliesslich in der einen getauschten Kurve unterscheidet.

## V3. Vollständige Zahlen

Rendite % / Max Drawdown % / Calmar:

| Grundlage | Fenster | HRP (Walk-Forward) | Gleichgewichtung |
|---|---|---|---|
| Erstfassung | 2022-03-18 … 2026-06-27 | 63,26 / −4,93 / **12,83** | 82,43 / −6,33 / **13,02** |
| 1. Korrektur | 2022-03-18 … 2026-06-27 | 76,47 / −7,32 / **10,45** | 107,13 / −9,82 / **10,91** |
| 2. Korrektur | 2022-03-18 … 2026-08-20 | 72,53 / −12,00 / **6,04** | 72,12 / −12,22 / **5,90** |
| **2. Korrektur, VBC live-konform** | 2022-03-18 … 2026-08-20 | 66,25 / −10,81 / **6,13** | 69,68 / −11,29 / **6,17** |

Der Filter nimmt beiden Ansätzen Rendite (HRP 72,53 → 66,25 %,
Gleichgewichtung 72,12 → 69,68 %) und senkt beide Drawdowns leicht. Er trifft
die Gleichgewichtung weniger hart — daher der Vorzeichenwechsel.

## V4. Getroffene Annahmen und Grenzen

1. **Untersucht wurde nur dieser eine Faktor.** Auftragsgemäss keine erneute
   Bestandsaufnahme der neun Bots, keine weiteren Varianten. Die acht anderen
   Kurven sind byteweise die aus `corrected_curves_v2/`.
2. **Der Regimefilter bleibt aus `equity_simulation.py` heraus.** Diese
   Untersuchung ändert keinen Bot-Code. Ob der Filter dort eingebaut werden
   soll, ist eine eigene, grössere Entscheidung und ausdrücklich nicht Teil
   dieser Arbeit.
3. **`corrected_curves/` und `corrected_curves_v2/` sind unangetastet.** Die
   neue Kurve liegt in `corrected_curves_v2_regimefilter/`, damit alle drei
   Kurvenstände nebeneinander nachvollziehbar bleiben.
4. **Kein Aktivierungsurteil.** Weder für HRP noch für den Regimefilter.
5. Alles Übrige — Rebalancing, Linkage, Schwellen, Buy-and-Hold-Referenz —
   unverändert aus der Erstfassung; siehe N4 und Z4.

## V5. Neue Dateien und Reproduktion

| Datei | Zweck |
|---|---|
| `vbc_regimefilter.py` | erzeugt die gefilterte Kurve; enthält die erzwungene Leerprobe |
| `nachtrag_vbc_regimefilter.py` | rechnet HRP auf der gemischten Grundlage, mit den drei Ankern |
| `corrected_curves_v2_regimefilter/` | die eine getauschte Kurve samt Kennzahlen |
| `results/nachtrag_vbc_regimefilter.json` | vollständige Zahlen aller vier Grundlagen |

`corrected_curves.py` bleibt **unverändert**: `vbc_regimefilter.py` übernimmt
dessen Attrappen-Vorspann zur Laufzeit aus `_WORKER_HEUTE`, statt eine dritte
Kopie zu führen. Das ist auch der Grund, warum diese Untersuchung ohne jede
Änderung in `research/trend_overlay/` auskommt — dort liegt dieselbe Datei als
byteweise identische Kopie, eine Änderung müsste beide treffen.

```
python3 research/hrp_portfolio/nachtrag_vbc_regimefilter.py
```

Erwartete Ausgabe: `27 Referenzwerte bestaetigt, 0 abweichend.` sowie die
Zeile `ANTWORT: Der HRP-Vorteil KIPPT ZURUECK …`.

---

# Nachtrag W — Erstfassungs-Anker eingefroren (Wartung, 2026-09-10)

## W0. Der Anlass

Reine Wartung am Prüfwerkzeug. **Kein inhaltlicher Befund, keine Neuanalyse,
keine geänderte Aussage** — wer nur an den Ergebnissen interessiert ist, kann
diesen Abschnitt überspringen.

`nachtrag_vbc_regimefilter.py` sichert sich mit drei Regressionsankern ab
(Abschnitt V2). Zwei davon lesen eingefrorene Schnappschüsse
(`corrected_curves/`, `corrected_curves_v2/`). Der dritte, `original`, las die
**neun lebenden Kurven** unter `results/<bot>/equity_curve.csv` — absichtlich,
denn genau die hatte die Erstfassung gelesen.

Diese eine Abhängigkeit ist inzwischen gerissen. PR #57 hat den BTC-Regimefilter
in den echten Backtest von `volatility_breakout_crypto` eingebaut und dabei
dessen lebende Kurve neu erzeugt. Seitdem verglich der Anker eine veränderte
Grundlage mit der unveränderten Referenz `results/hrp_summary.json` und schlug
in **7 von 9** Werten fehl; das Modul brach folgerichtig ab, obwohl inhaltlich
nichts falsch war. Aufgefallen ist das beim Nachziehen von PR #56 in PR #64.

## W1. Was geändert wurde

Der Anker `original` liest jetzt `corrected_curves_original/` — einen
eingefrorenen Schnappschuss derselben neun Dateien aus Commit `db11ba6`, also
dem Commit, in dem `results/hrp_summary.json` entstand. Damit hängt **keiner**
der drei Anker mehr an einer lebenden Datei, und das Modul bleibt
reproduzierbar, auch wenn ein Bot seine Kurve künftig erneut neu erzeugt.

Gewählt wurde damit der aufwändigere, aber haltbare Weg: den Anker wirklich zu
reparieren, statt ihn nur als „historisch, nicht mehr prüfbar" zu kommentieren.
Das war möglich, weil der Sollstand **exakt** rekonstruierbar ist (W2) — wäre
er es nicht gewesen, wäre die Kommentarlösung das Ehrlichere gewesen.

Bewusst **nicht** gewählt: nur die eine veränderte Kurve
(`volatility_breakout_crypto`) einzufrieren und die übrigen acht weiter live zu
lesen. Das hätte denselben Fehler beim nächsten Bot wieder eingefangen — die
Abhängigkeit von lebenden Dateien ist die Ursache, nicht diese eine Datei.

## W2. Warum der Schnappschuss der richtige Stand ist

Zwei unabhängige Belege:

1. **Die lebenden Kurven wurden im ganzen fraglichen Zeitraum nicht angefasst.**
   `git log -- 'results/*/equity_curve.csv' results/equity_curve.csv` zeigt
   zwischen `db11ba6` (Erstfassung) und `3770ca7` (PR #57) **keinen einzigen**
   Commit. Alle neun Dateien sind zwischen `db11ba6` und dem Commit unmittelbar
   vor PR #57 byteweise identisch — geprüft per SHA256. Auf dem heutigen `main`
   weicht **genau eine** ab: `volatility_breakout_crypto`
   (`5de7c5aba3…` → `060a54aea4…`).

2. **Der Anker reproduziert wieder exakt dieselben neun Werte** wie vor PR #57
   (63,26 / −4,93 / 12,8316 usw., Abschnitt V3) — also die Werte, die auch der
   Original-Stand des Nachtrags lieferte.

Der Schnappschuss ist zudem **selbstsichernd**: die Prüfsummen aller neun
Dateien stehen in `corrected_curves_original/MANIFEST.json` und werden bei
jedem Lauf geprüft. Weicht eine ab, bricht das Modul mit dem Sollstand im
Klartext ab (`git show db11ba6:results/<bot>/equity_curve.csv`) statt einen
still verschobenen Anker als grün zu melden — dieselbe Haltung wie bei der
erzwungenen Leerprobe in `vbc_regimefilter.py`.

## W3. Was unverändert bleibt

Die **Kernaussage ist nicht berührt**. Sie hängt am Vergleich `korrigiert_v2`
gegen `v2_mit_regimefilter` (Abschnitt V0/V3); beide Grundlagen lagen schon
vorher eingefroren unter `corrected_curves_v2/` bzw.
`corrected_curves_v2_regimefilter/` und sind von PR #57 nie berührt worden.
Nachgewiesen: `results/nachtrag_vbc_regimefilter.json` wird vom neuen Lauf
**byteweise identisch** neu erzeugt — alle vier Grundlagen, alle Kennzahlen,
der HRP-Vorteil weiterhin **−0,0432** (Ward −0,0330), Veränderung durch den
Filter **−0,1856**.

Ebenfalls unverändert: `corrected_curves.py`, `corrected_curves/`,
`corrected_curves_v2/`, `corrected_curves_v2_regimefilter/`, jeder Bot-Code,
jede `live_params.py`. Der Regimefilter wird weiterhin **nicht** in
`equity_simulation.py` eingebaut.

## W4. Neue Dateien und Reproduktion

| Datei | Zweck |
|---|---|
| `corrected_curves_original/*_equity_curve.csv` | eingefrorener Schnappschuss der neun Kurven der Erstfassung (Commit `db11ba6`) |
| `corrected_curves_original/MANIFEST.json` | Quell-Commit, Quellpfad und SHA256 je Kurve — Grundlage der Laufzeitprüfung |

Der Schnappschuss ist jederzeit gegen die Git-Historie nachprüfbar:

```
git show db11ba6:results/t3_supertrend/equity_curve.csv | sha256sum
```

muss die in `MANIFEST.json` hinterlegte Prüfsumme ergeben (für `elliott_wave`
ist der Quellpfad aus historischen Gründen `results/equity_curve.csv`, siehe
`portfolio_overview.LEGACY_EQUITY_CSV_PATHS`).

```
python3 research/hrp_portfolio/nachtrag_vbc_regimefilter.py
```

Erwartete Ausgabe jetzt wieder vollständig: die Zeile
`Schnappschuss Erstfassung: 9 Kurven, Pruefsummen OK`, danach
`27 Referenzwerte bestaetigt, 0 abweichend.` sowie
`ANTWORT: Der HRP-Vorteil KIPPT ZURUECK …`.
