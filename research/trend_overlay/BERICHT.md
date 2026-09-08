# Portfolioweiter Trend-Overlay — Backtest-Only-Untersuchung

> ## ⚠ Nachtrag: korrigierte Kapitalkurven-Grundlage (Sync-Check PR #24)
>
> Die `equity_curve.csv`-Dateien, auf denen das Baseline-Portfolio dieser Studie
> beruht, waren bei **5 der 9 Bots nicht auf der Live-Konfiguration**. Die
> Untersuchung wurde mit korrigierten Kurven wiederholt.
>
> **Die Kernaussage hält in allen drei Teilaussagen** — der Overlay verbessert
> den Gesamtzeitraum, bringt out-of-sample **keine** Drawdown-Verbesserung
> (identischer Max Drawdown in allen drei Varianten), und die Wirkung bleibt auf
> die 2022-Episode konzentriert.
>
> **Eine Nuance kippt:** out-of-sample *kostete* der Overlay in der Erstfassung
> leicht Rendite (Calmar −0,41); mit korrigierten Kurven *gewinnt* er dort leicht
> (**+0,81**). Das ändert nichts am Drawdown-Befund — der bleibt exakt null —,
> aber der Halbsatz „und kostet stattdessen leicht Rendite" gilt so nicht mehr.
>
> Die absoluten Zahlen verschieben sich deutlich (Calmar Baseline 13,02 →
> **10,91**, Overlay 15,02 → **18,02**).
>
> **Zusätzlich gefunden:** die gespeicherte `elliott_wave`-Kurve stammt aus dem
> Initial Commit (5 Symbole / 144 Trades statt 18 / 782). Kein Sync-Problem,
> sondern eine unabhängige Veralterung — getrennt ausgewiesen.
>
> Details, Regressionscheck (39/39) und Annahmen: Abschnitt **„Nachtrag N"** am
> Ende dieses Berichts.


> ## ⚠ Zweiter Nachtrag: die Kernaussage hält auch hier
>
> Die Kurven waren ein **zweites Mal** veraltet: seit der ersten Korrektur sind
> die Sync-Befunde selbst gemergt worden (PR #40–#42, #45, #51/#52), und die
> beiden Elliott-Bots haben einen **Look-Ahead-Fix** bekommen. Die Untersuchung
> wurde deshalb erneut wiederholt — mit Kurven, die die **heutige**
> `equity_simulation.py` erzeugt.
>
> **Alle drei Teilaussagen halten.** Der Overlay verbessert den Gesamtzeitraum
> (Calmar +7,31), bringt out-of-sample **keine** Drawdown-Verbesserung, und die
> Wirkung bleibt auf die 2022-Episode konzentriert (85 % der Signaltage).
>
> **Die in der ersten Korrektur gekippte Nuance kippt zurück** — und zwar in
> die schärfste denkbare Form: out-of-sample sind alle drei Varianten
> **zahlengleich** (26,44 % / −4,53 % / 5,84). Das Signal ist im
> Out-of-Sample-Fenster an keinem einzigen Tag aktiv; der Overlay tut dort
> buchstäblich nichts. Der Calmar-Unterschied ist deshalb exakt 0,00 statt
> +0,81 wie in der ersten Korrektur.
>
> Die absoluten Zahlen verschieben sich deutlich (Calmar Baseline 10,91 →
> **5,90**, Overlay 18,02 → **13,21**), das Portfolio ist mit den heutigen
> Kurven risikoreicher und weniger rentabel.
>
> Regressionscheck: **91/91** Referenzwerte beider früherer Fassungen exakt
> reproduziert. Details: Abschnitt **„Nachtrag Z"** am Ende dieses Berichts.


**Status: reine, retrospektive Backtest-Untersuchung, KEINE Live-Aktivierung,
KEINE Änderung an Live-Dateien.** Alle neuen Skripte liegen ausschliesslich
unter `research/trend_overlay/`. Verifiziert per `git status`: keine Datei
ausserhalb dieses neuen Verzeichnisses wurde angefasst.

## Kurzfassung

Ein aggregiertes "Krypto- UND Aktienmarkt gleichzeitig im
Abwärtstrend"-Signal (200-Tage-gleitender-Durchschnitt auf BTC/USDT bzw.
einem gleichgewichteten S&P-500-Top-150-Proxy) wurde retrospektiv auf das
bestehende, gleichgewichtete 9-Bot-Portfolio angewendet: Wäre die
Gesamt-Exponierung an aktiven Signaltagen reduziert (50 %) oder pausiert
(0 %) worden, statt sie unverändert zu lassen?

**Ergebnis in einem Satz:** Über den GESAMTEN verfügbaren Zeitraum
verbessert der Overlay sowohl Rendite als auch Max Drawdown leicht
(Calmar-Ratio 13,02 → 15,02 bei voller Pausierung) — **aber dieser
gesamte beobachtbare Effekt stammt fast ausschliesslich aus EINER
einzigen, langen Signal-Episode (April 2022 bis Januar 2023, 265 der 300
aktiven Tage)** und liegt praktisch vollständig im In-Sample-Abschnitt.
Out-of-Sample dreht sich das Bild: der Overlay bringt dort **keinerlei
Drawdown-Verbesserung** (identischer Max Drawdown -4,32 % in allen drei
Varianten) und kostet stattdessen leicht Rendite. **Keine
Handlungsempfehlung** — die Entscheidung liegt beim Nutzer in einer
separaten, künftigen Session.

## Methodik

### Signal-Konstruktion

- **Krypto-Referenz:** BTC/USDT-Tagesschlusskurs — dieselbe Wahl wie im
  bereits bestehenden BTC-Regimefilter von `t3_supertrend`
  (`strategies/t3_supertrend/regime_filter.py`), dort aber über einen
  eigenen SuperTrend-Indikator, hier bewusst über den in der
  Aufgabenstellung vorgeschlagenen, einfacheren gleitenden Durchschnitt —
  ein eigenständiges, PORTFOLIOWEITES Signal, keine Wiederholung des
  bot-spezifischen Filters.
- **Aktien-Referenz:** kein Marktindex-Proxy (z. B. SPY) ist im Projekt
  bereits vorhanden — daher ein gleichgewichteter, nicht rebalancierter
  Durchschnitt aus den bestehenden 150 S&P-500-Symbolen
  (`config/sp500_top150.txt`), wie von der Aufgabenstellung als Fallback
  vorgeschlagen.
- **Trend-Definition:** Kurs unter seinem eigenen 200-Tage-gleitenden-
  Durchschnitt = Abwärtstrend für diesen Markt. Kein Look-Ahead-Bias: der
  Durchschnitt zum Zeitpunkt T nutzt ausschliesslich Kurse bis
  einschliesslich T (`pandas.rolling()`, per Konstruktion
  backward-schauend) — explizit regressionsgetestet (`test_trend_core.py`:
  eine Änderung zukünftiger Kurse verändert vergangene Signal-Werte
  nachweislich NICHT).
- **Aggregation:** logisches UND — das Signal ist nur aktiv, wenn BEIDE
  Märkte gleichzeitig im Abwärtstrend sind (nicht ODER, wie in der
  Aufgabenstellung gefordert).
- **Anlaufphase:** Tage, an denen der gleitende Durchschnitt mangels
  200 Tagen Historie noch nicht definiert ist, gelten konservativ als
  NICHT im Abwärtstrend (volle Exponierung) — es gibt keine belastbare
  Grundlage, ohne einen fertigen Durchschnitt einen Abwärtstrend zu
  behaupten.

### Retrospektive Anwendung

Die "bestehende Gleichgewichtung" (1/9 je Bot, nie rebalanciert) wird
EXAKT wie in `research/hrp_portfolio/run_walk_forward.py` aus den
9 Bot-Kapitalkurven gebildet (Datenquelle unverändert aus
`shared/portfolio_overview.py` übernommen, nur lesend). An Tagen mit
aktivem Signal wird die tägliche Portfolio-Rendite linear um den
Reduktionsfaktor skaliert (0,5 bzw. 0,0) — dieselbe lineare
Skalierungs-Annahme wie bei der Positionsgrössen-Skalierung der
vorherigen Vol-Sizing-Untersuchung. **Kein Look-Ahead:** das Signal an
Tag T basiert ausschliesslich auf Kursen bis T, die Overlay-Reduktion
wird nur auf die tatsächliche Rendite VON Tag T angewendet — keine
rückwirkende Anpassung.

## Getroffene Annahmen (vollständig)

1. **Fenstergrösse des gleitenden Durchschnitts: 200 Handelstage.** Der
   von der Aufgabenstellung selbst vorgeschlagene, in der Praxis
   etablierte Wert ("200-Tage-Linie"). Keine Optimierung über mehrere
   Fenster — 150 Tage wurde AUSSCHLIESSLICH zur Robustheits-Illustration
   zusätzlich berechnet (siehe Ergebnis-Tabelle), nicht um das "bessere"
   Ergebnis auszuwählen.
2. **Zwei Reduktions-Varianten (50 % / 0 %), beide berichtet, nicht
   gegeneinander optimiert** — von der Aufgabenstellung selbst als
   gleichwertige Optionen genannt, keine Parameter-Wahl mit
   Overfitting-Risiko wie die Fenstergrösse.
3. **Aktien-Marktproxy: gleichgewichteter Durchschnitt der S&P-500-Top-150,
   begrenzt auf `RECENT_YEARS_ONLY = 10` Jahre** (dieselbe Konvention wie
   in den bestehenden Aktien-Bots, z. B. `elliott_wave_stocks/
   multi_symbol_optimise.py` — Survivorship-Bias-Begründung dort
   übernommen). Zusätzlicher, hier spezifischer Grund: erst mit einem
   FESTEN, gemeinsamen Normierungs-Ankerdatum für alle einbezogenen
   Symbole entsteht eine stabile, kompositionsartefakt-freie Preis-Niveau-
   Serie — würden Symbole erst ab ihrem jeweils eigenen (unterschiedlichen)
   ersten Handelstag einzeln in den Durchschnitt eintreten, entstünden
   künstliche Niveau-Sprünge beim Eintritt jedes neuen Symbols, die für
   einen TREND-Indikator (der genau auf Niveau-Bewegungen reagiert)
   besonders verzerrend wären. Symbole, die erst nach dem Ankerdatum an
   die Börse gingen, werden komplett ausgeschlossen statt anteilig
   aufgenommen — die konservativere Wahl.
4. **Lineare Renditen-Skalierung bei Overlay-Reduktion** (Faktor
   0,5/0,0 direkt auf die tägliche Portfolio-Rendite) — konsistent zur
   Positionsgrössen-Skalierung der Vol-Sizing-Untersuchung, keine neue
   Methodik eingeführt.
5. **Buy-and-Hold-artiges Rendite-/Drawdown-Referenzsystem und
   Calmar-Ratio-Konvention** identisch zu den beiden vorherigen
   Untersuchungen (Vol-Sizing, HRP) übernommen, für Konsistenz.
6. **In-/Out-of-Sample-Split:** derselbe `TRAIN_SPLIT_RATIO = 0.7` wie in
   allen 9 Bots (`multi_symbol_walk_forward.py`), angewendet als
   chronologischer Split auf den kombinierten Portfolio-Zeitraum.
7. **Datenquelle für die Bot-Kapitalkurven:** unverändert aus
   `shared/portfolio_overview.py` übernommen (Live-DB-Priorität ab
   `MIN_LIVE_CLOSED_TRADES`, sonst `equity_curve.csv`-Fallback) — in
   dieser Sandbox lief die Untersuchung durchgehend auf dem
   Backtest-Fallback, da keine Live-DBs vorhanden sind (gitignored).

## Ergebnis

### Übergreifende Tabelle (gemeinsames Vergleichsfenster: 2022-03-18 bis 2026-06-27)

| Zeitraum | Variante | Rendite | Max Drawdown | Calmar-Ratio |
|---|---|---|---|---|
| Gesamt | Baseline (kein Overlay) | 82,43 % | -6,33 % | 13,02 |
| Gesamt | Reduziert auf 50 % | 82,56 % | -5,90 % | 13,99 |
| Gesamt | Pausiert (0 %) | 82,63 % | -5,50 % | 15,02 |
| In-Sample (bis 2025-03-16) | Baseline | 51,82 % | -6,33 % | 8,19 |
| In-Sample | Reduziert auf 50 % | 53,05 % | -5,90 % | 8,99 |
| In-Sample | Pausiert (0 %) | 54,24 % | -5,50 % | 9,86 |
| Out-of-Sample (ab 2025-03-16) | Baseline | 20,16 % | **-4,32 %** | 4,67 |
| Out-of-Sample | Reduziert auf 50 % | 19,29 % | **-4,32 %** | 4,47 |
| Out-of-Sample | Pausiert (0 %) | 18,41 % | **-4,32 %** | 4,26 |

(Maschinenlesbar identisch in `results/trend_overlay_summary.json`;
tägliche Signal-Zeitreihe in `results/signal_timeline.csv`;
Baseline-Kurve in `results/baseline_curve.csv`.)

**Wichtigste Beobachtung: der komplette Out-of-Sample-Abschnitt zeigt
einen IDENTISCHEN Max Drawdown von -4,32 % in ALLEN drei Varianten** —
der Overlay hatte dort schlicht KEINE Gelegenheit zu wirken, weil der
schlechteste OOS-Drawdown-Zeitpunkt an keinem einzigen Tag mit dem
Signal zusammenfiel. Im Out-of-Sample-Abschnitt kostet der Overlay
stattdessen leicht Rendite (20,16 % → 18,41 % bei voller Pausierung),
ohne jeden kompensierenden Nutzen.

### Signal-Aktivität und Deckung mit 2022 (Aufgaben-Vorgabe Punkt 3)

Das 200-Tage-Signal war insgesamt an 300 von 1562 Tagen (19,2 %) aktiv,
verteilt auf 9 Episoden. **Die mit Abstand grösste Episode lief vom
2022-04-08 bis 2022-11-23 (229 Tage am Stück)** — ergänzt um drei
kürzere Nachläufer-Episoden bis 2023-01-11 (weitere 36 Tage). Zusammen
entfallen **265 der 300 aktiven Tage (88 %) auf das Jahr 2022** — im
gemeinsamen Fenster liegen 288 Tage in 2022, davon waren 255 (88,5 %)
Signal-aktiv.

Das deckt sich SEHR GENAU mit der bereits im Projekt dokumentierten
Schwächephase 2022 (siehe `results/rsi2_mean_reversion/
PROTOTYPE_FINDINGS.md`, Abschnitt 7b: T3/SuperTrend -12,28 % Drawdown,
RSI-2 -11,16 % Drawdown in 2022, während die Elliott-Wave-Bots als
Hedge fungierten). Das Signal hätte also GENAU in der bereits bekannten
Stress-Phase angeschlagen — ein methodisch ermutigendes Zeichen für die
Signal-KONSTRUKTION selbst.

Die übrigen 5 Episoden sind kurz (1 bis 25 Tage) und liegen im
März/April 2025 — direkt um die IS/OOS-Trennlinie (2025-03-16) herum,
faktisch fast vollständig im Out-of-Sample-Abschnitt.

### Robustheits-Illustration (150- statt 200-Tage-Fenster)

| Variante | Rendite | Max Drawdown | Calmar-Ratio |
|---|---|---|---|
| Baseline | 82,43 % | -6,33 % | 13,02 |
| Reduziert auf 50 % | 85,49 % | -5,36 % | 15,95 |
| Pausiert (0 %) | 88,53 % | -4,53 % | 19,54 |

Mit dem kürzeren Fenster fällt der beobachtete Effekt SOGAR noch etwas
grösser aus (Calmar 13,02 → 19,54 statt → 15,02) — kein
Instabilitäts-Warnsignal in dem Sinne, dass sich das Vorzeichen des
Effekts umkehren würde, ABER die Grössenordnung reagiert spürbar auf die
Fenster-Wahl. Da beide Fenster denselben 2022-Signal-Block als
dominanten Treiber erfassen (14 statt 9 Episoden, 286 statt 300 aktive
Tage insgesamt — ähnliches Gesamtbild), ist das primär eine Frage der
genauen Episoden-Grenzen um den 2022-Block, keine grundsätzlich andere
Schlussfolgerung.

## Strukturelle Einordnung (Aufgaben-Vorgabe, explizit gefordert)

**Ist die Verbesserungsmarge strukturell klein, weil das Portfolio schon
so gut diversifiziert ist?** Ja, eindeutig. Der bestehende, gleichgewichtete
9-Bot-Portfolio-Max-Drawdown liegt bereits bei nur -6,33 % (siehe HRP-
Untersuchung: der schlechteste EINZEL-Bot kommt auf -32,4 %) — die
Diversifikationswirkung des Zusammenschlusses ist also schon vor jedem
Overlay sehr stark. Der beste hier gemessene Overlay (volle Pausierung,
Gesamtzeitraum) reduziert den Max Drawdown um **0,83 Prozentpunkte**
(-6,33 % → -5,50 %) — eine reale, aber absolut kleine Verbesserung, weil
es schlicht nicht mehr viel Drawdown gibt, den man reduzieren könnte.
Ein Overlay auf ein UNDIVERSIFIZIERTES Portfolio (z. B. einen einzelnen
Bot mit -32,4 % Drawdown) hätte rein rechnerisch deutlich mehr Raum für
einen wahrnehmbaren Effekt — das wäre aber eine andere Fragestellung
als die hier untersuchte (portfolioweite Anwendung auf das bereits
diversifizierte Gesamtportfolio).

**Das ist selbst ein wertvolles Ergebnis, kein Fehlschlag der
Untersuchung:** die Diversifikation der 9 unterschiedlichen, schwach
korrelierten Bots leistet bereits den grössten Teil der
Drawdown-Kontrolle. Ein zusätzlicher, grober Markt-Timing-Layer kann
darauf nur noch einen vergleichsweise kleinen Beitrag oben drauf
leisten — UND dieser kleine Beitrag stammt hier fast vollständig aus
einer einzigen historischen Episode (2022), nicht aus einer über die
Zeit gleichmässig verteilten, robusten Schutzwirkung.

## Gesamteinschätzung (unaufgeregt, ohne Handlungsempfehlung)

Der aggregierte Trend-Overlay hätte retrospektiv über den GESAMTEN
verfügbaren Zeitraum eine leichte, in beide Richtungen (Rendite UND
Drawdown) positive Wirkung gehabt. Bei genauerer Aufschlüsselung zeigt
sich aber ein wichtiges Caveat: **fast der gesamte beobachtbare Nutzen
stammt aus einer einzigen, bereits bekannten Stress-Episode (2022)**, die
fast vollständig im In-Sample-Abschnitt liegt. Im Out-of-Sample-Abschnitt
hatte das Signal keine Gelegenheit, Schutz zu bieten (der schlechteste
OOS-Drawdown-Moment fiel mit keinem Signal-Tag zusammen) und kostete
stattdessen leicht Rendite. Das ist ein klassisches Muster: ein Signal,
das retrospektiv gut aussieht, weil es eine einzelne grosse historische
Bewegung erwischt hat, ohne dass sich daraus eine verlässliche,
zeitlich gleichmässig verteilte Schutzwirkung ableiten liesse. Gleichzeitig
ist die 2022-Deckung methodisch ermutigend, da sie sich mit unabhängig
bereits dokumentierten Schwächephasen deckt (nicht nur eine zufällige
rückwirkende Übereinstimmung).

Unabhängig vom OOS-Befund gilt strukturell: das bestehende, gleichgewichtete
9-Bot-Portfolio ist bereits so stark diversifiziert (Max Drawdown -6,33 %
gegenüber -32,4 % beim schlechtesten Einzel-Bot), dass die
Verbesserungsmarge für JEDEN zusätzlichen Overlay-Mechanismus strukturell
klein ist — das gilt unabhängig von der genauen Signal-Konstruktion.

**Keine der beobachteten Effekte ist so gross oder zeitlich gleichmässig
verteilt, dass sich daraus eine generelle Empfehlung für oder gegen einen
Trend-Overlay ableiten liesse — diese Entscheidung liegt bewusst beim
Nutzer in einer separaten, künftigen Session.**

## Explizit ausserhalb des Scopes dieser Untersuchung

Trailing-Stops (letzter verbleibender Backlog-Punkt, kommt planmässig
erst danach), jegliche Live-Code-Änderung, jegliche
Aktivierungsempfehlung. Keine Optimierung über mehrere gleitende
Durchschnitte oder Reduktionsstufen — nur je eine begründete Wahl plus
eine einzelne Robustheits-Illustration für die Fenstergrösse, wie von der
Aufgabenstellung gefordert.

## Reproduzierbarkeit

```
cd research/trend_overlay
python3 test_trend_core.py       # 17 Sanity-/Regressionstests des Trend-Kernmoduls
python3 run_overlay_analysis.py  # vollstaendige retrospektive Untersuchung, schreibt results/
```


---

# Nachtrag N: dieselbe Untersuchung auf korrigierter Kapitalkurven-Grundlage

## N0. Entscheidungsgrundlage

### Der Anlass

Der Sync-Check (PR #24) hat belegt: bei **5 der 9 Bots** weicht die Konfiguration
in `equity_simulation.py` von der Live-Konfiguration in `live_params.py` ab. Die
Dateien `results/<bot>/equity_curve.csv` sind die Ausgabe genau dieser Läufe —
und das Baseline-Portfolio dieser Studie ist nichts anderes als die
gleichgewichtete Summe eben dieser Kurven. Einstufung des Sync-Checks: **hoch**.

### Was geändert wurde — und was ausdrücklich nicht

**Nur die Kapitalkurven.** Signal-Konstruktion (200-Tage-MA, logisches UND
beider Märkte), Marktreferenzen, Fenstergrössen, die beiden
Exponierungs-Varianten, der IS/OOS-Split und die 2022-Stressperiode werden
**Funktion für Funktion unverändert aus `run_overlay_analysis.py` und
`trend_core.py` importiert und aufgerufen**.

Die einzige Neuschreibung ist `baseline_curve_for()`: das Original
`load_baseline_portfolio_curve()` hat keine Stelle, an der sich die Kurvenquelle
übergeben liesse. Die Zeilen darin sind wörtlich von dort übernommen — und dass
die Übernahme stimmt, wird geprüft und nicht behauptet (siehe Regressionscheck).

Unangetastet bleiben: `shared/portfolio_overview.py`, sämtliche
`results/*/equity_curve.csv` und jeder Bot-Code.

### Drei Grundlagen statt zwei

| Grundlage | Was getauscht wird | Rolle |
|---|---|---|
| `original` | nichts | **Regressionscheck** gegen `results/trend_overlay_summary.json` |
| `korrigiert` | die 5 abweichenden Bots, Live-Konfiguration | **primär** |
| `korrigiert_plus_veraltet` | zusätzlich `elliott_wave` neu erzeugt | eigenständiger Nebenfund, siehe N3 |

### Regressionschecks — dreifach, vor allem anderen

**1. Die vier synchronen Bots als Probe des Erzeugers.** Drei von ihnen
(`t3_supertrend`, `rsi2_crypto`, `turtle_soup_crypto`) ergeben eine **byteweise
identische** Datei zur bestehenden `results/`-Kurve. Der vierte
(`elliott_wave`) weicht ab, aus einem gemessenen Grund (N3) — das Skript
**verlangt** diese Abweichung ausdrücklich.

**2. Die fünf abweichenden Bots treffen die im Sync-Check veröffentlichten
Kennzahlen exakt** (288 / +3084,09 % / −9,79 % · 1454 / +224,41 % / −23,97 % ·
8915 / +145,59 % / −29,91 % · 4232 / +36,75 % / −21,05 % · 207 / +49,03 % /
−16,29 %).

**3. Die Basis `original` gegen die Erstfassung: 39/39 exakt** — alle drei
Varianten in Gesamtzeitraum, In-Sample, Out-of-Sample und der
150-Tage-Robustheitsprüfung, plus Signaltage, Episodenzahl und
2022-Deckung. Ohne diesen Durchlauf bricht das Skript ab.

**Das Erzeugermodul `corrected_curves.py` ist byteweise identisch mit dem der
HRP-Untersuchung** (PR #19, `research/hrp_portfolio/corrected_curves.py`,
MD5 `488e3cd8…`). Beide Studien rechnen also nachweislich auf derselben
korrigierten Grundlage — geprüft, nicht angenommen.

### Was diesen Befund umstossen würde

* Ein zweiter Bärenmarkt im Out-of-Sample-Abschnitt. Der OOS-Zeitraum enthält
  **keine einzige** Signal-Episode nennenswerter Länge — deshalb ist der
  OOS-Drawdown in allen Varianten identisch. Das ist kein Beleg dafür, dass der
  Overlay nicht wirkt, sondern dafür, dass er dort nichts zu tun hatte.
* Die `elliott_wave`-Veralterung (N3), die die Zahlen weit stärker verschiebt
  als die Sync-Korrektur — selbst aber durch den in PR #21 nachgewiesenen
  Zigzag-Look-Ahead verzerrt ist.

---

## N1. Die Kernaussage, in ihre drei Teilaussagen zerlegt

Bewusst nicht zu einem einzigen Ja/Nein verrechnet — die Teile verhalten sich
unterschiedlich, und genau das ist das Ergebnis.

| Grundlage | **T1** Calmar-Gewinn gesamt | **T2** OOS-Drawdown | OOS-Calmar-Gewinn | **T3** Signaltage in 2022 |
|---|---|---|---|---|
| `original` | **+2,00** | identisch (−4,32 %) | −0,41 | 85,0 % |
| **`korrigiert`** | **+7,11** | identisch (−2,96 %) | **+0,81** | 85,0 % |
| `korrigiert_plus_veraltet` | **+108,07** | identisch (−1,38 %) | ±0,00 | 85,0 % |

**T1 — der Overlay verbessert den Gesamtzeitraum: hält**, und deutlicher als
zuvor (Calmar 10,91 → 18,02 bei voller Pausierung, statt 13,02 → 15,02).

**T2 — out-of-sample keine Drawdown-Verbesserung: hält exakt.** Der Max Drawdown
ist in allen drei Varianten auf die zweite Nachkommastelle identisch, in jeder
der drei Grundlagen. Das ist die substanzielle Hälfte des Befunds, denn Drawdown
zu vermeiden ist der Zweck eines Overlays.

**T3 — die Wirkung ist auf eine Episode konzentriert: hält unverändert**, und
zwar aus einem strukturellen Grund: **das Signal hängt gar nicht von den
Bot-Kurven ab.** Es kommt aus BTC/USDT und dem Aktien-Proxy. 255 der 300 aktiven
Signaltage (85,0 %) liegen in 2022, die längste Episode dauert 229 Tage — in
allen drei Grundlagen zahlengleich. Eine Korrektur der Kapitalkurven konnte
diesen Befund nicht berühren.

### Die eine Nuance, die kippt

Die Kurzfassung der Erstfassung sagt out-of-sample: *„keinerlei
Drawdown-Verbesserung … und kostet stattdessen leicht Rendite."* Der erste Teil
hält. **Der zweite nicht mehr:** mit korrigierten Kurven bringt der Overlay
out-of-sample leicht *mehr* Rendite (36,65 % → 39,04 %) und damit +0,81
Calmar-Punkte statt −0,41.

Das ist eine Richtungsumkehr im Vorzeichen, keine im Wesen: bei identischem
Drawdown und ohne eine einzige nennenswerte Signal-Episode im OOS-Abschnitt ist
der Unterschied das Ergebnis weniger vermiedener Verlusttage, nicht einer
nachgewiesenen Schutzwirkung. **Die Aussage „out-of-sample kein belastbarer
Nutzen" bleibt richtig — die Begründung muss nur von „kostet Rendite" auf
„verändert den Drawdown nicht" umgestellt werden.**

---

## N2. Vollständige Zahlen

Rendite % / Max Drawdown % / **Calmar**:

### Gesamtzeitraum

| Grundlage | Baseline | reduziert 50 % | pausiert 0 % |
|---|---|---|---|
| `original` | 82,43 / −6,33 / **13,02** | 82,56 / −5,90 / **13,99** | 82,63 / −5,50 / **15,02** |
| **`korrigiert`** | 107,13 / −9,82 / **10,91** | 117,05 / −8,36 / **14,00** | 127,37 / −7,07 / **18,02** |
| `korrigiert_plus_veraltet` | 255,95 / −4,82 / **53,10** | 253,74 / −2,44 / **103,99** | 251,43 / −1,56 / **161,17** |

### In-Sample

| Grundlage | Baseline | reduziert 50 % | pausiert 0 % |
|---|---|---|---|
| `original` | 51,82 / −6,33 / **8,19** | 53,05 / −5,90 / **8,99** | 54,24 / −5,50 / **9,86** |
| **`korrigiert`** | 51,58 / −8,12 / **6,35** | 57,46 / −7,59 / **7,57** | 63,53 / −7,07 / **8,99** |
| `korrigiert_plus_veraltet` | 108,77 / −4,82 / **22,57** | 107,47 / −2,44 / **44,05** | 106,12 / −1,56 / **68,03** |

### Out-of-Sample

| Grundlage | Baseline | reduziert 50 % | pausiert 0 % |
|---|---|---|---|
| `original` | 20,16 / −4,32 / **4,67** | 19,29 / −4,32 / **4,47** | 18,41 / −4,32 / **4,26** |
| **`korrigiert`** | 36,65 / −2,96 / **12,38** | 37,84 / −2,96 / **12,78** | 39,04 / −2,96 / **13,19** |
| `korrigiert_plus_veraltet` | 70,50 / −1,38 / **51,09** | 70,50 / −1,38 / **51,09** | 70,50 / −1,38 / **51,09** |

In der dritten Grundlage sind die drei OOS-Zeilen **exakt gleich**: dort liegt
kein einziger aktiver Signaltag im Out-of-Sample-Fenster, der Overlay greift
also gar nicht ein. Deutlicher lässt sich T2 kaum illustrieren.

**Wer die Zahlen dieses Berichts zitiert, muss die Zeile `korrigiert` nehmen.**

---

## N3. Nebenfund: die gespeicherte `elliott_wave`-Kurve ist veraltet

`shared/portfolio_overview.py` liest für diesen Bot aus
`results/equity_curve.csv` (historischer Sonderpfad). Diese Datei stammt aus dem
**Initial Commit**:

| | gespeicherte Datei | heutiger Code |
|---|---|---|
| Trades | 144 | **782** |
| Symbole | 5 (BTC, ETH, BNB, SOL, XRP) | **18** |
| letzter Eintrag | 2026-06-27 | 2026-08-26 |

Das ist **keine** Folge der Sync-Abweichung — `elliott_wave` ist
konfigurationsseitig synchron — sondern eine davon unabhängige Veralterung
derselben Datengrundlage. Sie wird deshalb getrennt ausgewiesen und **nicht
stillschweigend mitkorrigiert**.

Ihre Wirkung ist erheblich (Baseline-Calmar 10,91 → 53,10), aber **nicht
belastbarer, sondern anders verzerrt**: PR #21 hat gemessen, dass der
Elliott-Wave-Backtest zum Zigzag-Wellenende einsteigt, dem per Konstruktion
rückwirkend eine Aufwärtsbewegung folgt — bei **100 % der Trades**. Eine Kurve
mit +2185 % bei −1,83 % Drawdown ist genau das erwartete Erscheinungsbild dieses
Look-Aheads. Die dritte Grundlage macht den Effekt sichtbar; sie wird **nicht**
als die bessere empfohlen.

---

## N4. Getroffene Annahmen dieses Nachtrags

Zusätzlich zu den Annahmen der Erstfassung, die alle unverändert gelten:

**N-A1 — Die Definition von „Live-Konfiguration" wird übernommen, nicht neu
gefasst** (wörtlich aus `research/sync_check/impact.py::build`).

**N-A2 — `elliott_wave_stocks` behält seine Backtest-Allokation.**
`live_params.py` dokumentiert dort keine; getauscht werden nur
`USE_TAKE_PROFIT` und das Positionslimit. Dieselbe Annahme wie im Sync-Check.

**N-A3 — Die Veralterung wird getrennt geführt** (`KNOWN_STALE_BOTS`), damit
Sync-Korrektur und Veralterung nicht in einer Zahl verschmelzen.

**N-A4 — Das gemeinsame Fenster und damit der IS/OOS-Trennpunkt ergeben sich
wie in der Erstfassung** aus dem Schnitt aller Bot-Kurven und wurden nicht
fixiert. In `korrigiert` bleiben beide unverändert (2022-03-18 … 2026-06-27,
Split 2025-03-16); nur in `korrigiert_plus_veraltet` verschieben sie sich.

**N-A5 — `baseline_curve_for()` ist die einzige übernommene Codestelle** und
wird ausschliesslich durch den Regressionscheck der Basis `original`
abgesichert. Fiele er aus, wäre kein Ergebnis dieses Nachtrags verwendbar —
deshalb bricht das Skript dort ab statt zu warnen.

---

## N5. Neue Dateien und Reproduktion

| Datei | Rolle |
|---|---|
| `corrected_curves.py` | erzeugt die neun korrigierten Kurven und biegt die Quellpfade um (byteweise identisch mit der Kopie in PR #19) |
| `nachtrag_sync_korrektur.py` | rechnet die drei Grundlagen über die unveränderten Funktionen von `run_overlay_analysis.py` |
| `test_corrected_curves.py` | 14 Sanity-Checks der Tausch-Logik |
| `corrected_curves/` | die neun erzeugten Kurven + Kennzahlen je Bot |
| `results/nachtrag_sync_korrektur.json` | vollständige Ergebnisse aller drei Grundlagen |

```
python3 test_corrected_curves.py       # 14 Checks
python3 nachtrag_sync_korrektur.py     # erzeugt Kurven, prüft 39/39, rechnet 3 Grundlagen
```

---

# Nachtrag Z — zweite Korrektur der Kapitalkurven (2026-09-08)

## Z0. Entscheidungsgrundlage

**Warum überhaupt ein zweiter Nachtrag.** Der erste Nachtrag hat von Hand
nachgebildet, wie die fünf damals abweichenden Bots *mit* Live-Konfiguration
gerechnet hätten. Inzwischen sind genau diese Befunde gemergt — die
Nachbildung ist damit nicht mehr die Korrektur, sondern selbst ein
historischer Stand. Dazu kommen Änderungen ohne Bezug zum Sync-Thema, die
dieselbe Datengrundlage treffen, allen voran ein Look-Ahead-Fix bei beiden
Elliott-Bots.

**Warum die Kurven diesmal nicht nachgebildet, sondern erzeugt werden.** Die
zweite Korrektur führt den `__main__`-Block der heutigen
`equity_simulation.py` aus (`corrected_curves.generate_heute`), statt einzelne
Bot-Funktionen mit passend gesetzten Parametern aufzurufen. Eine Nachbildung
ist eine zweite Fassung derselben Rechnung und läuft still auseinander, sobald
sich im Bot ein Aufruf ändert — genau das ist inzwischen mehrfach passiert.

**Warum zwei Regressionsanker statt einem.** Ein Dreifach-Vergleich ist nur so
viel wert wie die Vergleichbarkeit seiner Spalten. Geprüft wird deshalb beides:
dass die Auswertung unverändert rechnet (Basis `original` trifft
`results/trend_overlay_summary.json`) *und* dass die alte Grundlage exakt
reproduziert wird (Basis `korrigiert_v1` trifft
`results/nachtrag_sync_korrektur.json`). **91/91 Referenzwerte bestätigt, 0
abweichend.**

**Was unverändert bleibt.** Signal-Konstruktion (200-Tage-MA, logisches UND
beider Märkte), Marktreferenzen, Fenstergrössen, Exponierungs-Varianten,
IS/OOS-Split und die 2022-Stressperiode kommen unverändert aus
`run_overlay_analysis.py` / `trend_core.py` — aufgerufen über
`nachtrag_sync_korrektur.analyse()`, also wörtlich dieselbe Funktion wie in der
ersten Korrektur. `shared/portfolio_overview.py`, `results/*/equity_curve.csv`,
`corrected_curves/` und jeder Bot-Code bleiben unangetastet.

## Z1. Bestandsaufnahme: welche Bots rechnen heute anders?

Gemessen, nicht aus Commit-Titeln gelesen — Kurve gegen Kurve, per SHA-256:

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

**Drei Kurven haben sich bewegt**, aus zwei belegbaren Gründen:

* `elliott_wave` und `elliott_wave_stocks` — Commit `839500b`
  *„Elliott-Wave-Backtest korrigieren: beide Look-Ahead-Kanäle beheben"*. Die
  grösste Verschiebung der Studie: die Renditen fallen um den Faktor 32 bzw. 9.
  Der alte Wert war nicht falsch parametriert, sondern durch Vorausschau
  überhöht.
* `volatility_breakout_crypto` — Commit `9bb230f` (PR #45).

**Sechs Kurven sind unverändert** — darunter die drei Bots aus PR #40–#42, deren
gemergte Fassung die Handnachbildung des ersten Nachtrags auf die
Nachkommastelle trifft. Eine unabhängige Bestätigung, dass die erste Korrektur
damals richtig gerechnet hat.

**Nebenbeobachtung, hier nicht behoben:** bei fünf Bots weicht die gespeicherte
`results/<bot>/equity_curve.csv` vom heutigen Code ab — sie wurde nach den
Korrekturen nie neu erzeugt.

## Z2. Dreifach-Vergleich

Rendite % / Max Drawdown % / Calmar.

**Gesamtzeitraum**

| Grundlage | Baseline | reduziert 50 % | pausiert 0 % |
|---|---|---|---|
| Erstfassung | 82,43 / −6,33 / **13,02** | 82,56 / −5,90 / **13,99** | 82,63 / −5,50 / **15,02** |
| 1. Korrektur | 107,13 / −9,82 / **10,91** | 117,05 / −8,36 / **14,00** | 127,37 / −7,07 / **18,02** |
| 1. Korrektur + veraltet | 255,95 / −4,82 / **53,10** | 253,74 / −2,44 / **103,99** | 251,43 / −1,56 / **161,17** |
| **2. Korrektur** | 72,12 / −12,22 / **5,90** | 86,74 / −9,51 / **9,12** | 102,52 / −7,76 / **13,21** |

**In-Sample**

| Grundlage | Baseline | reduziert 50 % | pausiert 0 % |
|---|---|---|---|
| Erstfassung | 51,82 / −6,33 / **8,19** | 53,05 / −5,90 / **8,99** | 54,24 / −5,50 / **9,86** |
| 1. Korrektur | 51,58 / −8,12 / **6,35** | 57,46 / −7,59 / **7,57** | 63,53 / −7,07 / **8,99** |
| 1. Korrektur + veraltet | 108,77 / −4,82 / **22,57** | 107,47 / −2,44 / **44,05** | 106,12 / −1,56 / **68,03** |
| **2. Korrektur** | 36,12 / −12,22 / **2,96** | 47,69 / −9,51 / **5,01** | 60,17 / −7,76 / **7,75** |

**Out-of-Sample**

| Grundlage | Baseline | reduziert 50 % | pausiert 0 % |
|---|---|---|---|
| Erstfassung | 20,16 / −4,32 / **4,67** | 19,29 / −4,32 / **4,47** | 18,41 / −4,32 / **4,26** |
| 1. Korrektur | 36,65 / −2,96 / **12,38** | 37,84 / −2,96 / **12,78** | 39,04 / −2,96 / **13,19** |
| 1. Korrektur + veraltet | 70,50 / −1,38 / **51,09** | 70,50 / −1,38 / **51,09** | 70,50 / −1,38 / **51,09** |
| **2. Korrektur** | 26,44 / −4,53 / **5,84** | 26,44 / −4,53 / **5,84** | 26,44 / −4,53 / **5,84** |

Das Portfolio ist mit den heutigen Kurven **risikoreicher** (Max Drawdown
−6,3 % → −12,2 %) und **weniger rentabel** (82,4 % → 72,1 %) als in der
Erstfassung — im Wesentlichen wegen der beiden Elliott-Bots, deren überhöhte
Kurven bisher Rendite beisteuerten und Drawdown verwässerten.

## Z3. Die drei Teilaussagen — einzeln geprüft

Bewusst nicht zu einem einzigen Ja/Nein verrechnet: die Teilaussagen können
sich unterschiedlich verhalten, und in der ersten Korrektur haben sie das
getan.

| Grundlage | T1 Calmar-Gewinn (gesamt) | T2 OOS-Drawdown | OOS-Calmar-Differenz | T3 Signaltage in 2022 |
|---|---:|---|---:|---:|
| Erstfassung | +2,0015 | identisch (−4,32 %) | −0,4051 | 85,0 % |
| 1. Korrektur | +7,1062 | identisch (−2,96 %) | **+0,8074** | 85,0 % |
| 1. Korrektur + veraltet | +108,0714 | identisch (−1,38 %) | 0,0000 | 85,0 % |
| **2. Korrektur** | **+7,3095** | identisch (−4,53 %) | **0,0000** | 85,0 % |

**T1 — der Overlay verbessert den Gesamtzeitraum: hält** in allen vier
Grundlagen, in der zweiten Korrektur mit +7,31 sogar etwas deutlicher als in
der ersten.

**T2 — out-of-sample keine Drawdown-Verbesserung: hält** in allen vier
Grundlagen. In der zweiten Korrektur in der schärfsten denkbaren Form: alle
drei Varianten sind out-of-sample **zahlengleich**, nicht nur im Drawdown. Der
Grund steht in den Signalstatistiken — im OOS-Fenster (ab 2025-04-23) ist das
Signal an **keinem einzigen Tag** aktiv. Der Overlay tut dort buchstäblich
nichts.

Nachgezählt statt aus der Zahlengleichheit geschlossen: **0 von 485
OOS-Tagen** aktiv, alle 300 aktiven Tage liegen im In-Sample-Bereich.

**Dabei ist es knapp:** der letzte aktive Signaltag ist der **2025-04-21**,
zwei Tage vor dem Split am 2025-04-23. T2 hält in dieser Fassung also nicht,
weil das Signal weit von der Grenze entfernt läge, sondern weil es sie um zwei
Tage verfehlt. Ein etwas anderes gemeinsames Fenster — und damit ein etwas
anderer Split — hätte einige Signaltage in den OOS-Bereich gelegt. Das ist eine
Eigenschaft des Testaufbaus (fester 70/30-Split auf dem gemeinsamen Fenster),
keine Aussage über den Overlay, und es wird hier festgehalten, damit die
Zahlengleichheit nicht robuster wirkt, als sie ist.

**T3 — die Wirkung konzentriert sich auf 2022: hält**, und zwar unverändert
zahlengleich. Das Signal wird aus BTC und dem Aktien-Proxy gebildet und hängt
gar nicht von den Bot-Kurven ab: 300 aktive Tage in 9 Episoden, davon 255
(85 %) im 2022-Fenster, längste Episode 229 Tage.

**Die eine Nuance, die in der ersten Korrektur gekippt war, kippt zurück.**
Damals *gewann* der Overlay out-of-sample leicht an Calmar (+0,81), was den
Halbsatz der Erstfassung („und kostet stattdessen leicht Rendite") ausser Kraft
setzte. Mit den heutigen Kurven ist der Unterschied exakt **0,00** — weil das
Signal dort nie aktiv ist. Beide Formulierungen der Erstfassung sind damit
out-of-sample gegenstandslos: der Overlay kostet nichts und bringt nichts.

## Z4. Getroffene Annahmen und Grenzen dieses Nachtrags

1. **„Heutiger Stand" heisst: was `equity_simulation.py` rechnet — nicht: was
   live läuft.** Bei `volatility_breakout_crypto` fallen die beiden
   auseinander: `live_params.py` setzt `BTC_REGIME_FILTER_ENABLED = True`, der
   Backtest wendet den Filter bewusst nicht an (dokumentiert im Kopf von
   `equity_simulation.py`, PR #45). Die v2-Kurve dieses Bots (71,26 %) ist
   damit **nicht** live-konform; live läge sie bei 49,03 % (Sync-Check PR #24).
   Für diesen einen Bot war die erste Korrektur näher an der
   Live-Konfiguration. Eine zusätzliche Grundlage mit der gefilterten Kurve
   wurde bewusst **nicht** gerechnet — das wäre die dritte Runde, die die
   Aufgabe ausschliesst.
2. **Die erste Korrektur lässt sich nicht mehr wiederholen.**
   `nachtrag_sync_korrektur.py` prüft seine Kurven gegen die im Sync-Check
   veröffentlichten Kennzahlen; für `elliott_wave_stocks` trifft es sie nach
   dem Look-Ahead-Fix nicht mehr und bricht ab — **nachdem** es die CSVs
   geschrieben hat. Ein Lauf auf `corrected_curves/` würde die gespeicherte
   v1-Grundlage überschreiben und danach scheitern. Die Prüfung dieser Aussage
   lief deshalb in einem temporären Verzeichnis; `corrected_curves/` ist
   unangetastet, und die v1-Spalte stammt aus den **gespeicherten** Kurven.
3. **Die Attrappen werfen** bei jedem Netzzugriff, statt leere Daten zu
   liefern — sonst liefe ein versehentlicher Abruf still mit weniger Symbolen
   weiter. Ausnahme mit Grund: `binance.client.Client` muss sich **erzeugen**
   lassen, weil `shared/fetch_multi_data.py` auf Modulebene eine Instanz
   anlegt; geworfen wird bei jedem Methodenaufruf.
4. **Fensterwechsel.** Die zweite Korrektur endet am 2026-08-20 statt am
   2026-06-27, weil die neu erzeugte `elliott_wave`-Kurve weiter reicht.
   Dadurch verschiebt sich auch der IS/OOS-Split von 2025-03-16 auf
   2025-04-23 — genau dieser Fensterwechsel ist der Grund, warum das Signal
   im OOS-Bereich nicht mehr vorkommt. Die Spalte „1. Korrektur + veraltet"
   nutzt dasselbe Fenster und ist deshalb der fenstergleiche
   Vergleichspartner; sie zeigt denselben Effekt.
5. Alles Übrige unverändert aus der Erstfassung; siehe „Getroffene Annahmen
   (vollständig)" und N4.

## Z5. Neue Dateien und Reproduktion

| Datei | Zweck |
|---|---|
| `corrected_curves.py` | ergänzt um `generate_heute()` und `vorhandene_kurven()` — der Erzeuger der ersten Korrektur bleibt unverändert daneben stehen |
| `nachtrag_sync_korrektur_v2.py` | dieser Nachtrag; ruft die Auswertung über `nachtrag_sync_korrektur.analyse()` auf |
| `corrected_curves_v2/` | die neun neu erzeugten Kurven samt Kennzahlen |
| `results/nachtrag_sync_korrektur_v2.json` | vollständige Zahlen aller vier Grundlagen |

```
python3 research/trend_overlay/nachtrag_sync_korrektur_v2.py
```

Erwartete Ausgabe: `91 Referenzwerte bestaetigt, 0 abweichend.` Der Lauf
erzeugt die neun Kurven neu (einige Minuten) und rührt weder `results/<bot>/`
noch `corrected_curves/` an.
