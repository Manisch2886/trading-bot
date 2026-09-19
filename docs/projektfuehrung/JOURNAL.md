# Journal — Trading-Bot-Projekt

**Chronologisches Archiv abgeschlossener Untersuchungen und Entscheidungen.**
Wird **nie umgeschrieben**, nur ergaenzt. Die aktiven Punkte stehen in
`BACKLOG.md`.

**Diese Datei gehoert nicht in jede Sitzung** — nur, wenn es um eine konkrete
Messung geht. Sie ist rund 3 500 Zeilen lang.

> ⚠️ **Kuerzel-Warnung:** Die Bloecke U, V, X und AF verwenden Kuerzel aus dem
> **Strategie-Katalog** (A1, A2, B1, B2, C1, D1, E1, E2, F1, F2, G1, K1) — sie
> bedeuten dort **etwas anderes** als die gleichnamigen Punkte im Backlog. Im
> Backlog tragen sie das Praefix **`S-`**. Insbesondere: *„G1 gestrichen"* in
> U.2 meint die **Ko-Drawdown-Gewichtung** (`S-G1`), **nicht** „Alles haengt an
> einem MacBook" (Backlog G1, weiterhin offen und wichtig).

## Inhalt

| Block | Thema | PR |
|---|---|---|
| **L** | Exposure-Messung | #84 |
| **M** | Drawdown-Untersuchung | #83 |
| **N** | Ergebniskurven erneuert | #86 |
| **O** | Dienst-Vorlagen | TB-15/16 |
| **Q** | Veraltete Zahlen in `live_params` | #89 |
| **R** | Beide Drawdown-Masse | #90 |
| **S** | Stabile Sortierung | #91 |
| **T** | Wellenauswahl | TB-20 |
| **U** | Fable-Rueckmeldung: die Antwort | — |
| **V** | Fable, zweite Rueckfragenrunde | — |
| **W** | Agent 2 Zielfunktion | #94 |
| **X** | Haltedauern und Zeithorizonte | #95 |
| **Y** | Determinismus | #96 |
| **Z** | Fib-Score-Stufen | #97 |
| **AA** | Zuteilungskaskade | #99 |
| **AB** | Bestandsaufnahme Kapitalsimulation | #100 |
| **AC** | Strategy-Discovery-Pipeline | — |
| **AD** | Messkette an eine Stelle | #101 |
| **AE** | Versuchsregister | #102 |
| **AF** | Vorabfestlegung vor der Neuselektion | — |
| **AG** | Backlog-Pruefung durch Fable (14.09.) | — |

Am Ende: **die wiederkehrenden Lehren.**

## L — Ergebnis der Exposure-Messung (PR #84, 12.09.2026)

`research/exposure_messung/BERICHT.md`. Erledigt **I1**. 17.795 ausgefuehrte
Positionen, neun Bots, Fenster 2022-03-17 bis 2026-08-20.

### L.1 — Die Antwort: teilweise zutreffend, aber nicht aus dem genannten Grund

| | mittlere Brutto-Exposure | Exposure 2022 | Tage ohne Position |
|---|---:|---:|---:|
| urspruengliche **vier** Bots | 25,85 % | 23,10 % | **0 von 1.794** |
| heutige **neun** Bots | 37,91 % | 31,09 % | **0 von 1.618** |

**Der vermutete Mechanismus ist widerlegt.** Das Buch ist *nicht* ueberwiegend
Kasse: an keinem Tag flach, an keinem Tag unter 10 % Exposure, kein
Monatsmittel unter 27,1 %. An den 10 % schlechtesten Buy-and-Hold-Tagen ist die
Exposure sogar **hoeher** als im Mittel (38,1 % gegen 37,9 %) — das Buch weicht
dem Stress nicht aus.

*Warum der Denkfehler naheliegt:* **Einzelne** Bots sind oft flach
(`elliott_wave` an 78,7 % der Tage), aber vier der neun sind praktisch
dauerhaft investiert (`turtle_soup_stocks` 100 %, `volatility_breakout`
99,4 %). Neun solche Blaetter uebereinandergelegt ergeben ein Buch, das nie
Pause macht.

### L.2 — Die −1,43 % sind trotzdem keine Risikokennzahl: drei Fehler

| Messung (dieselben vier Bots) | Wert |
|---|---:|
| urspruenglich berichtet | **−1,43 %** |
| dieselbe Formel, **heutige** `live_params.py` | −9,41 % |
| am **investierten** Kapital gemessen | **−32,12 %** |
| mittlerer Einzel-Bot-Drawdown *(der richtige Vergleich)* | −17,93 % |
| schlechtester Einzelbot *(der bisher benutzte Vergleich)* | −22,20 % |

1. **Veraltet** — die Zahl stammt aus abgelegten `results/*/equity_curve.csv`.
2. **Falscher Nenner** — gemessen am ganzen Buch statt am Kapital, das im Markt war.
3. **Falsche Vergleichsgroesse** — bei 1/N-Gewichtung schlaegt ein Bot mit
   −32 % nur mit −3,6 % durch. Der Sprung „−22,20 % auf −1,43 %" hat **nie zwei
   vergleichbare Groessen** nebeneinandergestellt.

**Was Diversifikation real bringt: rund 6 Prozentpunkte** (−17,93 % auf
−11,47 %). Ein Effekt, kein Wunder.

### L.3 — Zwei Nebenbefunde, die schwerer wiegen als die Hauptfrage

| # | Befund | Folge |
|---|---|---|
| **L1** | **Die niedrigen Korrelationen sind ein Messartefakt.** Eine Kapitalkurve bewegt sich nur an Ausstiegstagen; dazwischen ist die Tagesrendite exakt 0, und zwei ueberwiegend aus Nullen bestehende Reihen korrelieren mechanisch nahe null. **Zu Marktpreisen bewertet:** mittlere Paar-Korrelation **+0,112**, `turtle_soup_stocks` gegen Aktien-B&H **+0,82**. Das gemeinsame Beta war immer da, nur unsichtbar | Die **0,085**, auf denen die Diversifikationsthese ruhte, messen nichts. Korrelations- und Drawdown-Angaben der Beobachtungsebene auf **Marktpreis-Bewertung** umstellen |
| **L2** | **Fuenf von neun abgelegten Ergebniskurven beschreiben nicht mehr den laufenden Bot.** `turtle_soup_stocks` 1.887 abgelegte gegen **8.915** heutige Zeilen; `rsi2_mean_reversion` 2.641 gegen 4.232; dazu `elliott_wave`, `elliott_wave_stocks`, `volatility_breakout`. Die Sync-Reihe hat den **Code** in Ordnung gebracht, die **Ergebnisdateien** nicht | ⚠️ **Diese Dateien speisen die Montags-Mail UND die Dashboard-Portfolio-Sicht** (Protokoll 4.3b), solange ein Bot unter zehn geschlossenen Live-Trades liegt — und das tun **alle neun**. Die +80,52 %, die das Dashboard heute zeigt, stammen aus veralteten Kurven |

### L.4 — Korrektur an der Elliott-Wave-Aktien-Entscheidung von heute

Die Begruendung, den Bot als Diversifikator weiterlaufen zu lassen, ist
schwaecher als angenommen. Er ist **an 95,4 % der Tage im Markt**, bei 47,6 %
eigener Exposure und **+0,46 Korrelation** zum Aktien-Buy-and-Hold.

Damit trifft **weder** Fables Erklaerung („strukturell kleines Buch, das im
Baerenmarkt wenig verliert") **noch** das Diversifikator-Argument aus diesem
Chat. Der Bot ist fast durchgehend investiert, traegt echten Drawdown und
bleibt trotzdem hinter Buy-and-Hold.

**Nicht sofort umkehren** — aber das Pruefkriterium im Oktober muss ein anderes
sein als der Drawdown-Beitrag. Der Zeit-im-Markt-Test aus **I3** ist jetzt die
naheliegende Messung.

### L.5 — Konzentration

Im Median **72 gleichzeitig offene Positionen**, 99. Perzentil 103. An
**98,4 %** der Tage haelt mindestens ein Symbol mehr als einen Bot, bis zu vier
gleichzeitig. Staerkstes Paar: `rsi2_mean_reversion` und `turtle_soup_stocks`
mit bis zu **19 gleichen Titeln** an 79,4 % der Tage.

> Die Diversifikation ist also kleiner, als die Bot-Zahl suggeriert — und das
> ist ein zusaetzliches Argument fuer das gemeinsame Konto (**I7**), das genau
> solche Ueberschneidungen deckeln koennte.

### L.6 — Folgeaufgaben aus dem Bericht

| # | Aufgabe | Dringlichkeit |
|---|---|---|
| ~~L3~~ | ~~**Abgelegte `results/*/equity_curve.csv` neu erzeugen**~~ **ERLEDIGT, PR #86 — siehe Block N.** und pruefen, welche Aussagen sich verschieben | **SEHR HOCH** — betrifft Montags-Mail und Dashboard-Portfolio-Sicht, **und** hat laut K.4b bereits zweimal eine Untersuchung entwertet und einmal ein Urteil gekippt. Wiederkehrender Stolperstein, kein Einzelfall |
| **L4** | Korrelations- und Drawdown-Angaben der Beobachtungsebene auf **Marktpreis-Bewertung** umstellen | mittel |
| **L5** | Buy-and-Hold-Vergleiche um die **Exposure-Dimension** ergaenzen | mittel — betrifft alle Pflicht-Gegenchecks der Methodik |

### L.7 — Was die Messung nicht beantwortet

Ob die Strategien gut sind · Survivorship im Aktienuniversum (nur benannt,
eigene Aufgabe **I2**) · Look-ahead in adjustierten Kursen · Fill-Annahmen ·
Feb–Apr 2020 fuer das gemeinsame Buch (Krypto-Kursdaten beginnen erst 09/2021;
ersatzweise die vier Aktien-Bots ab 2016: Exposure im Corona-Quartal 36,2 %
gegen 61,2 % im Mittel) · Forward-Test-Vergleich (alle neun Bots unter zehn
geschlossenen Live-Trades)

### L.8 — In einfacher Sprache

**Was wir wissen wollten:** Die Zahl −1,43 % galt als Beweis, dass sich die Bots
gegenseitig absichern. Stimmt das?

**Was herauskam:** Nein — aber anders als vermutet. Die Bots sind sehr wohl
dauerhaft im Markt (an **keinem** von 1 618 Tagen war das Buch leer). Die Zahl
war trotzdem falsch, aus **drei** Gruenden: Sie stammte aus veralteten Dateien,
sie war auf das falsche Kapital bezogen, und sie verglich zwei Dinge, die nicht
vergleichbar sind — einen einzelnen Bot mit voller Groesse gegen ein Buch, in
dem derselbe Bot nur ein Viertel ausmacht.

**Was wirklich gilt:** Diversifikation bringt rund **6 Prozentpunkte** weniger
Verlust (−17,9 % statt −11,5 %). Ein echter Effekt, aber kein Wunder.

**Und ein zweiter Fund:** Die Bots aehneln sich viel staerker, als die Zahlen
zeigten. Die alte Messung sah sie nur an Verkaufstagen — dazwischen stand sie
still. Rechnet man taeglich zu Marktpreisen, korreliert ein Bot zu **0,82** mit
einfachem Kaufen-und-Halten.

**Was das fuer dich heisst:** Die Bots sind weniger unabhaengig voneinander als
gedacht. Das ist der Grund, warum seither so viel gemessen statt gebaut wird.

---

## M — Ergebnis der Drawdown-Untersuchung (12.09.2026)

`research/drawdown_reihenfolge/BERICHT.md`. **Untersuchung, keine Korrektur** —
es wurde nichts geaendert.

### M.1 — Die Kernfrage: Ja, bei vier von neun Bots

| Bot | heute live | Wahl unter dem chronologischen Drawdown |
|---|---|---|
| `turtle_soup_crypto` | Donchian 10 / Stop **structural** | Donchian 10 / **kein Stop** |
| `turtle_soup_stocks` | Donchian 10 / **kein Stop** | Donchian 10 / **Stop 5 %** |
| `elliott_wave_stocks` | dev 5 % / Stop 3 % / kein Ziel | dev 5 % / **Stop 2 %** — die Live-Einstellung **verbessert** sich dabei von Rang 6 auf Rang 2 |
| `elliott_wave` | dev 10 % / Stop 6 % / Fib 0,618 | Die Kandidatenliste aus PR #28 enthaelt sie nicht mehr: In-Sample-Top-5 rutschen von Stop 4–6 % auf **Stop 2–4 %**. Die Zigzag-Schwelle 10 % haelt |

**Unveraendert bei fuenf Bots:** `rsi2_crypto`, `rsi2_mean_reversion`,
`volatility_breakout`, `volatility_breakout_crypto`, `t3_supertrend`.

> **Korrektur eines Irrtums in diesem Chat:** `elliott_wave` laeuft **bereits**
> auf dev 10 % / Stop 6 % / Fib 0,618 (per `grep` in `live_params.py` bestaetigt,
> 12.09.2026). Die Umstellung auf die vom Elliott-Wave-Bericht empfohlene
> Parametrisierung ist also **schon erfolgt**. Die frueher hier gefuehrte offene
> Entscheidung „auf 10/6 umstellen?" ist **erledigt**.

`t3_supertrend` rechnet heute schon chronologisch — aber **versehentlich**:
`regime_filter.filter_trades_by_regime` sortiert intern nach `entry_time`, weil
`pd.merge_asof` das braucht. Zur Zeit seiner Parameterwahl war das noch nicht so;
dort kippt der Sieger aber ebenfalls nicht.

### M.2 — Es ist kein Rauschen, und der Befund ist groesser als gefragt

Der chronologische Drawdown liegt bei **13 von 15** Bot-Fenstern **ausserhalb**
der Spanne aus 200 Permutationen der Symbol-Blockreihenfolge. Selbst die
guenstigste Reihenfolge kommt nicht an ihn heran.

**Die haertere Pruefung — wie oft gewinnt unter 200 Symbol-Reihenfolgen dieselbe
Kombination?**

| Bot | Block-Sieger stabil |
|---|---:|
| `turtle_soup_crypto` | 94,5 % |
| `volatility_breakout_crypto` | 92,5 % |
| `rsi2_crypto` | 59,5 % |
| `rsi2_mean_reversion` | 53,0 % |
| `volatility_breakout` | **40,0 %** |
| `t3_supertrend` (vor Regimefilter) | 38,5 % |
| `elliott_wave_stocks` | **34,5 %** |
| `turtle_soup_stocks` | **30,5 %** |

> ⚠️ Bei den drei markierten Bots ist die Rangfolge des heutigen Masses **schon
> gegen die Sortierung der eigenen Symboldatei nicht stabil.** Waere
> `config/sp500_top150.txt` alphabetisch statt nach Marktkapitalisierung
> sortiert, haette dort eine andere Kombination gewonnen — nicht weil die
> Strategie anders waere, sondern weil die Datei anders sortiert ist.

**Groessenordnung:** Faktor 1,8 bis **13,1**; drei war die Untergrenze, nicht der
Normalfall. Der Faktor waechst mit der Zahl parallel laufender Symbole — weil
chronologisch die Verlustphasen **aller** Symbole zusammenfallen, und genau
dieses gleichzeitige Verlieren korrelierter Positionen ist das Risiko, das die
Kennzahl messen soll. Die Blockreihenfolge mittelt es heraus.

### M.3 — Die Wendung: auch der chronologische Drawdown ist nicht die Wahrheit

Beide Masse addieren Einzeltrade-Prozente zu **je einer ganzen Einheit**, obwohl
der Bot mit 2–10 % Kapital je Trade und meist einem Positionslimit arbeitet.
**−2 135 % ist als Kapitalverlust unmoeglich.**

Das richtige Mass hat das Projekt laengst: `equity_simulation.py`. Rangkorrelation
der beiden Masse zum echten Kapital-Drawdown:

| Bot | Blockreihenfolge | chronologisch |
|---|---:|---:|
| `volatility_breakout_crypto` | 0,400 | **1,000** |
| `elliott_wave` | 0,871 | **0,983** |
| `rsi2_crypto` | 0,371 | **0,886** |
| `rsi2_mean_reversion` | **−0,314** | 0,829 |
| `volatility_breakout` | **−0,200** | 0,800 |
| `turtle_soup_crypto` | **−0,333** | 0,690 |
| `elliott_wave_stocks` | 0,265 | 0,645 |
| `turtle_soup_stocks` | 0,259 | 0,559 |

> ⚠️ Bei **drei** Bots steht das heutige Mass in **umgekehrtem** Verhaeltnis zum
> echten Kapital-Drawdown. Wer es dort minimiert, waehlt systematisch den
> **schlechteren** Kapitalverlauf. Naeher am Kapital-Drawdown als die
> chronologische Reihenfolge liegt das heutige Mass bei **keinem** Bot.

**Die eigentliche Inkonsistenz:** Das Projekt waehlt Parameter nach dem einen
Mass und beurteilt Bots nach dem anderen — Calmar steht in jeder
Buy-and-Hold-Tabelle.

### M.4 — Beschlossenes Vorgehen (Nutzer, 12.09.2026)

**Weg 3 als Sofortmassnahme, Weg 2 als Ziel — in drei Schritten.**

| # | Schritt | Begruendung |
|---|---|---|
| ~~M1~~ | ~~**Beide Werte ausweisen**~~ **ERLEDIGT, PR #90 (TB-18)** — siehe Block R | Kein Bruch der Vergleichbarkeit. `research/elliott_wave_params/` macht es bereits so. Jede alte Zahl bleibt lesbar, jede neue Entscheidung sieht den richtigen Wert daneben |
| **M2** | **Volle Kette fuer die vier betroffenen Bots rechnen** (Walk-Forward → Equity-Simulation → Buy-and-Hold) | Laut Abschnitt 6 des Berichts nicht gelaufen. Offen ist, **ob die chronologisch besseren Kombinationen auch die besseren Bots sind** |
| **M3** | **Danach** ueber den Wechsel auf den Kapital-Drawdown entscheiden | Erst mit den Zahlen aus M2 |

**Warum nicht Weg 1** (nur die Blockreihenfolge aufgeben, eine Zeile): Behebt den
offensichtlichen Fehler und laesst den tieferen stehen — die Einzeltrade-Summe
bleibt. Man ersetzte eine kaputte Kennzahl durch eine weniger kaputte und
bezahlte den Bruch trotzdem.

**Der Preis eines Masswechsels, benannt:** Er entwertet neun gespeicherte
`multi_symbol_optimisation_results.csv`, alle Score-Angaben in sechs
`PROTOTYPE_FINDINGS.md` und in `EXPERIMENT_FINDINGS.md`, die Rangfolgen in
`research/elliott_wave_params/` und `research/elliott_wave_lookahead/`, **die
Zielfunktion von Agent 2** und jede Score-Zeile kuenftiger Quartalsberichte.
Derselbe Bruch, den die Look-Ahead-Korrektur schon einmal erzeugt hat — und an
dem bis heute eine falsche Zahl in `elliott_wave_stocks/live_params.py` steht.

**Vorbehalt:** Der Kapital-Drawdown gewinnt nicht ueberall. Bei
`turtle_soup_crypto` stimmt der Kapital-Calmar mit dem **Block**-Sieger ueberein,
bei `volatility_breakout` mit **keinem** von beiden, bei `elliott_wave_stocks`
sind beide Korrelationen praktisch gleich.

### M.5 — Belastbarkeit und offene Punkte

**Stark belegt:** keine eigene Backtest-Kopie (echte Bot-Funktionen) · 18/18
Selbsttests je Bot inklusive fuenf Gegenproben · **bitgenaue Reproduktion** der
gespeicherten Bot-Ergebnisdateien bei sechs Bots · der Ausloeser ist
**unabhaengig bestaetigt** (−82,50 gegen −259,86 bei `elliott_wave_stocks`, und
alle sieben Zahlen der Krypto-Live-Kombination treffen bis auf die letzte
Stelle) · gerechnet **nach** PR #81, Wirkung gemessen.

**Schwach:** `volatility_breakout` und `volatility_breakout_crypto` haben nur
vier Rasterpunkte — deren Rangkorrelationen sind **nicht belastbar**. Der
Stabilitaetsanteil von `elliott_wave_stocks` springt durch 0,01 Prozentpunkte in
sechs Ø-PnL-Werten von 17,5 % auf 34,5 %; die qualitative Aussage haelt, der
Einzelwert nicht.

**Nicht beantwortet:** ob die chronologisch besseren Kombinationen die besseren
Bots sind (→ M2) · bei `elliott_wave` das **Urteil** ueber die neuen Kandidaten
(Bedingungen B1–B5 aus PR #28; dev 10 % / Stop 2–3 % wurde nie bis zum Urteil
gefuehrt) · die Zielfunktion von Agent 2 wurde nicht neu bewertet, obwohl der
Score auch dessen Suchrichtung bestimmt.

### M.6 — In einfacher Sprache

**Was wir wissen wollten:** Nach welcher Zahl wurden die Parameter deiner Bots
eigentlich ausgesucht?

**Was herauskam:** Nach einer Zahl, die nichts misst. Das Auswahlskript legt die
Trades **nach Symbol sortiert** hintereinander statt **nach Datum** — und
rechnet den groessten Verlust auf dieser Reihenfolge. Diese Reihenfolge hat es
nie gegeben; sie ist ein Nebenprodukt davon, wie das Skript seine Teilergebnisse
aneinanderhaengt.

**Wie gross der Unterschied ist:** Faktor 1,8 bis **13** — dieselben Trades,
zwei voellig verschiedene Zahlen.

**Was daran am meisten stoert:** Bei drei Bots laeuft die Zahl sogar **verkehrt
herum**. Wer sie verbessert, waehlt den schlechteren Kapitalverlauf.

**Und ein Detail, das die Sache greifbar macht:** Bei drei Bots haette eine
alphabetisch sortierte Symboldatei zu **anderen Live-Parametern** gefuehrt. Nicht
weil die Strategie anders waere — nur weil die Datei anders sortiert ist.

**Was das fuer dich heisst:** Vier der neun Bots haetten andere Einstellungen
bekommen. Das Mass muss repariert werden, bevor irgendetwas neu ausgewaehlt
wird. Frist dafuer: **13. Dezember**.

---

## N — Ergebniskurven erneuert (PR #86, 12.09.2026)

Erledigt **L3**. `shared/ergebniskurven.py`, `shared/kurven_lauf.py`,
`shared/README_ERGEBNISKURVEN.md`, 44 Selbsttests.

### N.1 — Die Zahlen, die der Nutzer wöchentlich liest, waren zu gut

| | vorher | nachher |
|---|---:|---:|
| Vergleichsfenster | 2022-03-18 – 2026-06-27 | 2022-03-18 – **2026-08-20** |
| Rendite im Fenster | +80,52 % | **+69,68 %** |
| **Max Drawdown kombiniert** | **−6,24 %** | **−11,29 %** |

Kombinierter Vierer-Drawdown: **−1,43 % → −9,34 %.** Damit ist die Vorhersage
der Exposure-Messung (−9,41 %) bestätigt.

> **Der Kernsatz des Berichts:** Der kombinierte Drawdown „war nie eine
> Eigenschaft des Portfolios, sondern zu grossen Teilen eine Eigenschaft
> veralteter Dateien."

**Keine bereits getroffene Entscheidung hängt daran** — die −1,43 % waren durch
PR #84 ohnehin als Risikokennzahl verworfen, und die Montags-Mail löst nichts
aus. Was sich ändert, ist die Grundlage **künftiger** Entscheidungen, und die
Korrektur geht durchweg in die unangenehme Richtung.

### N.2 — Fünf Kurven beschrieben einen Bot, den es nicht mehr gibt

| Bot | Zeilen alt → neu | Rendite alt → neu | MaxDD alt → neu |
|---|---|---|---|
| `elliott_wave` | 144 → 130 | +84,33 % → +67,77 % | **−0,69 % → −10,17 %** |
| `elliott_wave_stocks` | 469 → 395 | **+1500,53 % → +352,72 %** | **−1,90 % → −22,44 %** |
| `rsi2_mean_reversion` | 2 641 → 4 232 | +29,91 % → +36,75 % | −21,82 % → −21,05 % |
| `turtle_soup_stocks` | 1 887 → 8 915 | +133,01 % → +145,59 % | −32,54 % → −29,91 % |
| `volatility_breakout` | 1 236 → 1 454 | +142,06 % → +224,41 % | −22,39 % → −23,97 % |

**„Veraltet" trifft es nicht** — bei vier der fünf laufen die Kurven schon in
der **ersten Zeile** auseinander. Die Drawdowns von −0,69 % und −1,90 % bei den
Elliott-Bots waren ein **Rechenfehler** aus der Zeit vor der
Look-Ahead-Korrektur, keine Strategieeigenschaft. Ursachen insgesamt: PR #26
(Look-Ahead), PR #38–#59 (Sync-Reihe, Allokation 10 % → 5 % bzw. 2 %), PR #81
(Kurslücken).

> Damit ist auch die Herkunft der falschen „1458 % vs 756 %" in
> `elliott_wave_stocks/live_params.py` geklärt — dieselbe Quelle. Der
> Korrektur-PR dafür steht weiterhin aus.

**Gegenprobe, die überzeugt:** Vier Bots kommen **byteweise identisch** neu
heraus (`rsi2_crypto`, `t3_supertrend`, `turtle_soup_crypto`,
`volatility_breakout_crypto`). Ein Verfahren, das alle neun verändert hätte,
hätte nichts bewiesen.

**Auf dem Mac verifiziert (12.09.2026):** `9x AKTUELL`, alle neun Kurven Zeile
für Zeile identisch mit denen aus der Cloud-Sitzung.

### N.3 — Die Wiederholungssperre

```
python3 shared/ergebniskurven.py                    # prüfen, Rückgabewert 1 bei Befund
python3 shared/ergebniskurven.py --erzeugen         # neu schreiben
python3 shared/ergebniskurven.py --nur-abweichung   # nur der ernste Fall (für Cron)
```

**Sie erzeugt die Kurve neu und vergleicht Zeile für Zeile** — nicht die
Zeilenzahl, keinen Parameter-Fingerabdruck, keinen Zeitstempel. Begründung aus
dem HRP-Fall: Der fehlende Regimefilter war **kein Wert in `live_params.py`**,
sondern eine Aufrufstelle im `__main__`-Block. Der `live_params.py`-Diff von
PR #57 bestand aus **einer geänderten Kommentar-Zeilennummer**.

**Zwei Arten von Befund**, und die Trennung ist entscheidend:

- `VERALTET` — die abgelegte Kurve ist ein exakter **Anfang** der heutigen, nur
  neue Kursdaten sind dazugekommen. Unvollständig, nicht falsch
- `ABWEICHEND` — schon der gemeinsame Teil läuft auseinander. Jede daraus
  abgeleitete Zahl ist neu zu prüfen

Ohne diese Trennung meldete ein Cronjob **täglich** (die Kursdaten wachsen) und
wäre binnen einer Woche nicht mehr gelesen.

Dauer rund 50 Sekunden. Cron-Vorschlag `50 3 * * *` mit `--nur-abweichung`,
**nicht eingetragen** (Crontab klemmt, siehe A1). Von Hand: **vor jeder
Auswertung, die `results/` liest**, und nach jedem Merge, der `strategies/`
anfasst.

### N.4 — Vier Folgepunkte

| # | Punkt | Dringlichkeit |
|---|---|---|
| ~~N1~~ | ~~`sort_values("time")` nicht stabil~~ **ERLEDIGT, PR #91 (TB-19)** — siehe Block S. Die Zahlen sind jetzt −9,41 % und −11,41 %, exakt wie vorhergesagt |
| **N2** | **`research/hrp_portfolio/nachtrag_vbc_regimefilter.py` bricht ab.** Der Anker `korrigiert_v1` liest vier Kurven (darunter `elliott_wave`) **live** aus `results/`, statt sie eingefroren zu halten — dieselbe Bauart-Lücke, die Abschnitt W1 für den Anker `original` schon geschlossen hatte, eine Stufe tiefer. Abhilfe: die vier synchronen Kurven als `corrected_curves_v1_clean/` mit `MANIFEST.json` einfrieren. **Die Kernaussage des HRP-Berichts ist nicht betroffen** — sie hängt an `korrigiert_v2`, und `volatility_breakout_crypto` ist byteweise unverändert | mittel |
| **N3** | Die Montags-Mail nennt weiterhin eine Backtest-Zahl **„LIVE-PORTFOLIO"** (Protokoll 9.15) | niedrig |
| **N4** | **Die Kurven veralten weiter** — das Werkzeug meldet es, aber nur, wenn es läuft. Hängt an A1/A2 (Crontab) | siehe A |

### N.5 — Zwei Ordnungspunkte vom Mac *(erledigt 12.09.2026, siehe O)*

- **`dashboard/com.manisch.trading-dashboard.plist`** liegt unversioniert im
  Projektordner und verweist auf `dashboard/server.py` — das Dashboard ist
  inzwischen eine FastAPI-Anwendung in `app.py`. Entweder veraltet und
  irreführend, oder sie gehört versioniert nach `system/`, wie die
  caffeinate-Vorlage. **Zu klären**
- Eine Datei namens **`=21.0`** liegt im Projektordner — entstanden durch einen
  Tippfehler bei einer Ausgabeumleitung (`pip install ... >=21.0`). Harmlos,
  kann weg

### N.6 — In einfacher Sprache

**Was wir wissen wollten:** Beschreiben die gespeicherten Ergebniskurven noch
den Bot, der heute laeuft?

**Was herauskam:** Bei **fuenf von neun** nicht. Manche waren so alt, dass sie
schon in der **ersten Zeile** auseinanderlaufen. Bei einem Bot standen 1 887
Zeilen in der Datei, waehrend der heutige Code 8 915 erzeugt.

**Was sich dadurch verschoben hat:** Die Portfolio-Zahl im Dashboard faellt von
+80,5 % auf **+69,7 %**, der groesste Verlust steigt von −6,2 % auf **−11,3 %**.
Ein Bot stand mit **+1 500 %** Rendite in der Ablage — tatsaechlich sind es
+353 %.

**Warum das passiert ist:** Der Code wurde mehrfach korrigiert (Look-Ahead,
Allokationen, Kursluecken) — die daneben liegenden Ergebnisdateien blieben
einfach stehen.

**Was jetzt anders ist:** Ein Werkzeug rechnet jede Kurve neu und vergleicht sie
**Zeile fuer Zeile** mit der gespeicherten. Es unterscheidet dabei „nur
unvollstaendig" von „laeuft auseinander" — sonst wuerde es taeglich melden und
nach einer Woche niemand mehr hinsehen.

**Was das fuer dich heisst:** Die Zahlen, die du montags per Mail und im
Dashboard liest, waren zu gut. Jetzt stimmen sie — und der Fehler kann sich
nicht unbemerkt wiederholen.

---

## O — Dienst-Vorlagen versioniert (TB-15, 12.09.2026)

`system/README_DIENSTE.md`, `system/TESTAUFTRAG_DIENSTE.md`,
`system/test_dienst_plists.py` (127 Prüfungen). Erledigt **N.5**.

### O.1 — Der Bestand war umgekehrt, als ich angenommen hatte

| Vorlage | meine Annahme in TB-15 | tatsächlich |
|---|---|---|
| Telegram | fehlt im Repo, Platzhalter anlegen | **war da**, versioniert unter `notifications/` → per `git mv` nach `system/` verschoben, Historie erhalten |
| Dashboard | Kopie liegt in `dashboard/`, nur verschieben | **gab es nie im Repo** — auch nicht in der Git-Historie. Die Datei lag nur im Arbeitsordner des Mac |

Ich hatte von dem, was auf dem Mac liegt, auf das Repo geschlossen. Das
Übergabeprotokoll hatte es korrekt vermerkt: in Abschnitt 4.5 stand für die
Dashboard-Vorlage ein Strich.

**Die „Bitte nicht raten"-Regel hat gegriffen — nur bei der anderen Datei.**
Drei Werte wurden als `PLATZHALTER__` markiert statt erfunden, weil launchd
eine erfundene Fassung klaglos annähme und der Dienst danach anders liefe, ohne
dass es jemand merkt.

**Der Test kennt deshalb drei Ergebnisse statt zwei:** `0` in Ordnung, `1`
kaputt, `2` ehrlich noch offen. Ein Platzhalter landet nie im OK-Topf.

### O.2 — Zwei Funde, die ohne die Mutationsproben durchgerutscht wären

- **Die Probe „Einstiegspunkt umbenannt" blieb zunächst grün:** Die
  Existenzprüfung sah die *erwartete* Datei an statt der, auf die die Vorlage
  *zeigt*. Sie hätte nie bemerkt, dass eine Vorlage veraltet — genau wofür sie
  da ist.
- **Beim Verschieben der Telegram-Vorlage wäre eine Prüfung in
  `test_caffeinate_plist.py` stillschweigend weggefallen**, weil sie hinter
  einem `if os.path.isfile(...)` auf den alten Ort stand. Der Test wäre grün
  geblieben (52 → 53 Prüfungen nach der Korrektur).

### O.3 — Auf dem Mac ausgeführt und geprüft (12.09.2026)

Die Vorlage wurde aus der laufenden Fassung befüllt, die verirrte Kopie unter
`dashboard/` und eine Müll-Datei `=21.0` entfernt. Ergebnis:
**125 von 127, 0 offen, 2 fehlgeschlagen.**

| # | Befund | Bewertung |
|---|---|---|
| **O1** | Die Prüfungen „Vorlage setzt `DASHBOARD_HOST`" und „… `DASHBOARD_PORT`" schlagen fehl | **Keine Fehlkonfiguration, sondern eine falsche Erwartung im Test.** TB-15 hatte beide Werte ausdrücklich als *erschlossen, nicht belegt* markiert — die Annahme ist damit widerlegt. Korrektur als **TB-16** formuliert |
| **O2** | `DASHBOARD_HOST` steht **nur in der `.env`**, `DASHBOARD_PORT` nirgends (Standardwert 8787 aus `konfig.py`) | ⚠️ **Ergänzt F6:** Die `.env` ist **nicht versioniert**. Geht sie verloren, startet das Dashboard auf der Voreinstellung `127.0.0.1` und ist über Tailscale nicht mehr erreichbar. **Der einzige Fernzugriffsweg des Projekts hängt an einer Datei, die in keinem Backup des Repos liegt** |

### O.4 — Was in der Anleitung steht, weil es heute mehrfach zu Fehlschlüssen führte

Alle vier haben heute mindestens einmal einen falschen Schluss ausgelöst — bei
mir zuerst:

1. **Das Dashboard lauscht nicht auf `localhost`**, sondern auf
   `100.106.38.8:8787`. Ein `curl localhost:8787` läuft ins Leere, obwohl der
   Dienst einwandfrei läuft.
2. **`303` ohne Token ist die richtige Antwort** — sie *beweist*, dass der
   Dienst läuft. Erst *keine* Antwort ist ein Problem.
3. **Die `-15` in `launchctl list` ist kein Fehler**, sondern der Exit-Status
   des **Vorgängers**: durch Signal 15 beendet, also genau das, was
   `kickstart -k` tut. Entscheidend ist die **erste** Spalte — eine PID heisst
   „läuft".
4. **LaunchAgents starten erst nach der grafischen Anmeldung.** Nach einem
   Neustart läuft keiner der drei Dienste, bis sich jemand anmeldet — auch
   `caffeinate` nicht, also laufen dann auch die **Cronjobs** nicht. Dieselbe
   Klasse stillen Ausfalls wie der Schlaf-Vorfall.

### O.5 — Nebenbefund, bewusst nicht geändert

Der Kopfkommentar von `dashboard/server.py` sagt noch „Kein Hintergrunddienst
und kein launchd-Eintrag — das kann später eingerichtet werden". Der Dienst
läuft seit Monaten. `server.py` stand auf der Nicht-anfassen-Liste.

### O.6 — Offen

| # | Punkt |
|---|---|
| ~~O1~~ | ~~TB-16~~ **ERLEDIGT, PR #88.** Die Prüfung ist jetzt **bedingt**: Wenn die Vorlage Host oder Port setzt, muss der Wert stimmen (Port 8787, Host im Tailscale-Bereich **`100.64.0.0/10`** — der CGNAT-Bereich, aus dem Tailscale vergibt; `100.7.x` sähe ähnlich aus, wäre aber eine gewöhnliche öffentliche Adresse). Setzt sie ihn nicht, ist das in Ordnung. **Kein eigener Ergebnistopf**, weil `OFFEN` „jemand muss etwas tun" heisst und den Rückgabewert 2 treibt — ein nicht gesetzter Host ist aber ein fertiger, gültiger Zustand; als `OFFEN` käme der Test auf dem Mac nie mehr auf 0. Verifiziert: 144/144 mit der echten Vorlage, 1 Fehler bei falschem Port 8080, 7 Mutationsproben |
| **O3** | WARNUNG **Commit liegt lokal, `git push` fehlt.** Die befuellte Vorlage ist committet (`3798157`, 12.09.2026), aber **nicht gepusht** - GitHub fragte nach Zugangsdaten, weil der macOS-Schluesselbund per SSH gesperrt ist. Der Commit ist sicher und geht nicht verloren. **Am Mac nachholen:** `cd ~/trading-bot && git push`. Gehoert zum **A-Block** |
| ~~O4~~ | ~~Logdateinamen unbelegt~~ **GEKLAERT 12.09.2026** durch Vergleich mit der laufenden Fassung: `logs/dashboard/launchd.out.log` und `launchd.err.log`. Ebenfalls geklaert: Der Python-Pfad ist `trading-env/bin/python3` - **dieselbe Umgebung wie der Telegram-Bot**, was TB-15 ausdruecklich als nicht belegt offengelassen hatte |
| **O5** | **Der Kommentarkopf der PR-Fassung ging beim Befuellen verloren.** Er enthielt die vollstaendige Trennung **belegt / widerlegt / erschlossen / offen** samt Begruendung, warum der `EnvironmentVariables`-Block ueberfluessig ist. Die laufende Fassung hat ihn nicht. Als kleiner PR nachziehen - **aber ohne die Zeile "DIESE VORLAGE IST NOCH EIN PLATZHALTER"**, die stimmt nicht mehr. Das Wissen darin ist zu wertvoll, um es zu verlieren |
| **O2** | **Die `.env`-Abhängigkeit der Bindungsadresse.** Jetzt als **Punkt 17** im Übergabeprotokoll, Abschnitt 9. Zwei Wege stehen zur Wahl, **Entscheidung des Nutzers**: (a) `DASHBOARD_HOST` zusätzlich in `EnvironmentVariables` der plist führen — der Wert steht dann doppelt, überlebt aber den Verlust der `.env`; (b) wenigstens die **Namen** der benötigten `.env`-Schlüssel versioniert festhalten. Die **Werte** gehören in keinem Fall ins Repo. Gehört zu **F6**. ⚠️ Das Tückische daran: Der Dienst läuft dabei **einwandfrei und meldet nichts** — es fällt erst auf, wenn jemand von aussen zugreifen will |

---

## Q — TB-17: Veraltete Zahlen in `live_params` (PR #89, 13.09.2026)

### Q.1 — Das Wichtigste: in den anderen acht Dateien steht nichts Falsches

Alle neun `live_params.py` geprüft. **Jede genannte Zahl liess sich auf ihren
Bericht zurückführen**, mit Datei und Zeilennummer. Nichts geraten, nichts
ergänzt.

Die belastbarste Gegenprobe: Fünf Bots haben eine Grundlagen-Verschiebung
hinter sich (PR #86). Drei davon nennen Zahlen — und bei `elliott_wave`,
`turtle_soup_stocks` und `volatility_breakout` decken sich diese **exakt mit
den erneuerten Kurven**. Die Einträge sind also nach der jeweiligen Korrektur
geschrieben worden. **Nur `elliott_wave_stocks` blieb zurück.**

### Q.2 — Dort waren es zwei Einträge, nicht einer

| Eintrag | Inhalt | Status |
|---|---|---|
| **02.09.2026** *(gemeldet)* | „schlaegt Buy-and-Hold klar (1458 % vs. 756 %)" | korrigiert: **+330,18 % / −22,70 %** gegen B&H **+755,69 % / −34,83 %** |
| **03.09.2026** *(nicht gemeldet)* | acht Kennzahlen zu `USE_TAKE_PROFIT = False`, alle aus derselben Look-Ahead-Grundlage | korrigiert |

**Warum die Korrektur vom 08.09. nicht gereicht hat:** Sie stand an anderer
Stelle als der Fehler. Der Eintrag vom 02.09. trug die Behauptung **im
Wortlaut weiter** und verwies per „ACHTUNG" sechs Tage nach unten — wer von
oben las, hatte die falsche Aussage vorher geglaubt. Und den Eintrag vom 03.09.
hatte sie gar nicht mitgenommen.

> **Genau die Fehlerklasse, die am 12.09.2026 zweimal in den Broker-READMEs
> auftrat.** Die gültigen Zahlen stehen jetzt **im Kopf der Datei**.

**`USE_TAKE_PROFIT = False` hält** — die Entscheidung ruht seit PR #28 auf
einer **Rangfolge** (unter den 116 Kombinationen, die die Mindestfilter
bestehen, arbeiten die vorderen zehn praktisch ausnahmslos ohne festes
Kursziel), nicht auf diesen Zahlen. Ein sauber gerechnetes Gegenstück zu
„mit/ohne Kursziel" gibt es **nicht** — der gemessene Hebel bleibt unbekannt,
und genau das steht jetzt dort.

### Q.3 — Der Nebenbefund, der über die Aufgabe hinausgeht

> **Die abgelegte Ergebniskurve trug bis PR #86 die Zahl der Variante *mit*
> Take-Profit** — obwohl `USE_TAKE_PROFIT` am 03.09.2026 auf `False` gesetzt
> wurde. Belegt über die Trade-Zahl: die alte Kurve hatte **469 Zeilen**, und
> genau 469 ausgeführte Trades nennt jene Zelle.

Die Kurve war also aus **zwei unabhängigen Gründen** veraltet: dem Look-Ahead
**und** einem Parameterwechsel, nach dem sie nie neu erzeugt wurde. **PR #86
hatte nur den ersten genannt.**

| # | Daraus folgt |
|---|---|
| **Q1** | **`shared/ergebniskurven.py` gehört nach JEDER Parameterübernahme ausgeführt**, nicht nur nach einer Methodik-Korrektur. Bisher nirgends als Regel festgehalten — gehört in den Ablauf einer Parameterentscheidung |

### Q.4 — Warnhinweis in `EXPERIMENT_FINDINGS.md`, Zahlen bewusst nicht umgerechnet

Auf Rückfrage nachgetragen; die Aufgabe hatte `results/` ausgenommen, die
Sitzung hat **gefragt statt sich zu ermächtigen**. Kasten am Dateianfang plus
je eine Zeile unter den vier betroffenen Abschnitten und der Empfehlung.

**Die Zahlen sind nicht umgerechnet — und das ist der Punkt:**

> `research/elliott_wave_lookahead/` benutzt sie als **veröffentlichte
> Baseline** und weist damit nach, dass die Look-Ahead-Reproduktion den
> damaligen Lauf wirklich trifft (`decisions.py` → `PUBLISHED_CELLS`;
> `verify_baseline.py` → `PUBLISHED`). **Wer die Tabellen überschreibt,
> zerstört diesen Nachweis.** Der Warnhinweis sagt das ausdrücklich, damit die
> nächste Sitzung nicht „aufräumt".

Vorher geprüft: Keine Stelle im Repo **parst** die Datei — alle Fundstellen
sind Fliesstext oder hartcodierte Vergleichszahlen. Ein Kasten kann nichts
brechen.

### Q.5 — Ein Vorbehalt für den Prüftermin im Oktober

> Die aussergewöhnlich flache **abgelegte** Kurve dieses Bots (−1,65 %) war
> es, die den kombinierten Vierer-Drawdown **getragen** hat. Frisch gerechnet
> sind es **−21,16 %**.

Die Diversifikations-Begründung, mit der der Bot weiterläuft, stützt sich also
teilweise auf **dieselbe Zahlenbasis, die diese Korrektur zurückzieht**. Dazu
die Exposure-Messung: **95,4 % Zeit im Markt**, **+0,46 Korrelation** zum
Aktien-Buy-and-Hold. Ein selbstverständlicher Diversifikator ist er nicht.

Genau deshalb das schärfere Kriterium (**I3**) — und genau deshalb steht der
Vorbehalt jetzt **in der Datei**, damit die Begründung nicht ungeprüft
durchläuft.

### Q.6 — Die harte Randbedingung, dreifach belegt

| Nachweis | Ergebnis |
|---|---|
| Alle **61 Konstanten aller neun Bots**, per AST vor und nach der Änderung | `IDENTISCH`, `LAST_UPDATED` unverändert |
| **Code-AST ohne Docstrings** gegen `HEAD`, alle neun Dateien | identisch — genau ein Docstring geändert, null Code |
| Lauf gegen den Bot-Code: `test_params.py elliott_wave_stocks` | **330,18 % / −22,7 %** — genau die Zahlen im neuen Dateikopf (18/18) |

**Neu: `shared/test_live_params_werte.py`** (69 Prüfungen) hält alle 61
Konstanten als Sollwerte fest — die eigentliche Zusicherung, ab jetzt dauerhaft.

**Eine bestehende Sperre musste präzisiert werden:** `shared/test_kursdaten.py`
verbot jede **Byte**-Änderung an einer `live_params.py` gegen `origin/main` und
hätte diese Korrektur bis zum Merge als Befund gemeldet. Sie vergleicht jetzt
die ausgewerteten **Werte** — **strenger als vorher**: Eine geänderte Zahl
fällt weiterhin auf (Gegenprobe: `STOP_LOSS_PCT` 3.0 → 4.0 wurde namentlich
gemeldet), **zusätzlich** fällt jetzt eine verschwundene oder neue Konstante
auf.

### Q.7 — Zur freigestellten zweiten Prüfung: ja, aber eng

Der Prüfer schlägt nur an, wenn eine Buy-and-Hold-Behauptung mit Prozentzahl
**in derselben Zeile** ohne Quelle steht — kein Fenster über mehrere Zeilen.

> Sechs der neun Dateien nennen Buy-and-Hold bloss als Glied der
> Validierungskette, und bei `volatility_breakout` steht zwei Zeilen darunter
> „8 % Stop-Loss". **Ein Zwei-Zeilen-Fenster hätte bei sechs von neun Dateien
> grundlos angeschlagen — und so ein Prüfer wird abgeschaltet und schützt
> danach nichts.**

Gegen sich selbst geprüft, fünf Fälle.

---

## R — TB-18: Beide Drawdown-Masse (PR #90, 13.09.2026)

Umsetzung von **M1**. Kein Mass gewechselt, keine Parametrisierung geaendert,
keine gespeicherte Ergebnisdatei ueberschrieben.

### R.1 — Die Zusicherung, zweifach belegt

> **`robustness_score` und Rangfolge sind unveraendert — fuer alle neun Bots, am
> Verhalten geprueft, nicht am Diff.** Wer heute optimiert, bekommt dieselben
> Parameter wie gestern.

1. **Am Verhalten, ohne Kursdaten:** Derselbe Bot bewertet zweimal dieselbe
   Trade-Menge — einmal mit den urspruenglichen `entry_time`-Werten, einmal mit
   denselben Zeitstempeln, nur **anders auf die Zeilen verteilt**. PnL,
   Zeilenreihenfolge und Trade-Zahl bleiben gleich. Ergebnis: Score, Drawdown
   und Rangfolge identisch — waehrend der neue Wert sich nachweislich
   unterscheidet.
2. **An echten Kursdaten:** Der geaenderte Bot liefert fuer dieselbe Kombination
   weiterhin denselben `max_drawdown_pct` wie die Raster, die
   `research/drawdown_reihenfolge/` **vor** der Aenderung abgelegt hat.

### R.2 — Was neu ist

`max_drawdown_chronologisch_pct` — derselbe Drawdown auf der nach `entry_time`
**stabil** sortierten Trade-Menge. Benennung aus
`research/elliott_wave_params/engine.py` **uebernommen**, nicht neu erfunden.

Der Wert steht in der Rasterausgabe, in
`results/<bot>/multi_symbol_optimisation_results.csv` (als **letzte** Spalte,
damit die bisherige Spaltenreihenfolge unberuehrt bleibt) und bei drei Bots
zusaetzlich im „Beste Kombination"-Block.

> **Bewusst NICHT ergaenzt: ein `robustness_score_chronologisch`.** Eine zweite
> Score-Spalte haette genau die Einladung geschaffen, nach ihr zu sortieren —
> und das ist Gegenstand von **M2** und der Entscheidung danach, nicht von M1.
> Die Zahl ist aus den vorhandenen Spalten ohnehin ableitbar
> (`avg_return_pct × √num_trades ÷ |Drawdown|`).

### R.3 — Die neun Dateien waren nie identisch

| Baustein | Fassungen ueber die neun Bots |
|---|---|
| `calculate_robustness_score` | **1** — identisch in allen neun |
| `evaluate_combination_multi` | **9** — je eigene Parameterliste; `t3_supertrend` filtert zusaetzlich nach BTC-Regime, sechs Bots fuehren `avg_holding_days` |
| `run_multi_optimisation` | **8** — `turtle_soup_crypto` und `turtle_soup_stocks` teilen eine Fassung |

**Gemeinsam war ihnen genau die Stelle, um die es ging:** Die zwei Zeilen der
Drawdown-Berechnung standen in allen neun **zeichengleich** da.
**Vereinheitlicht wurde nichts** — das waere eine eigene Entscheidung.

### R.4 — Rechenzeit: erledigt

**0,5 bis 2,1 ms je Rasterkombination**, ueber ein ganzes Raster des teuersten
Bots rund 25 ms. Ende zu Ende nicht messbar — die Unterschiede liegen bei
wenigen Prozent und zeigen in **beide** Richtungen, sind also Laufzeitrauschen.
Bei den Elliott-Bots verschwindet der Schritt vollends: dort gehen 23 bzw. 175
Sekunden je Kombination in die Wellenerkennung.

Zum Vergleich: Der **Kapital**-Drawdown (das eigentlich richtige Mass) haette
laut Untersuchung das **1,5- bis 2-Fache** gekostet.

### R.5 — Nebenbefund: `t3_supertrend` rechnet schon chronologisch

Beide Werte sind dort **gleich** (−296,68 % gegen −296,68 %). Kein Fehler:
Der Bot filtert nach dem Zusammenfuegen nach BTC-Regime, und
`filter_trades_by_regime` sortiert dabei selbst nach `entry_time`. **Er rechnet
heute schon chronologisch — nur hat das nie jemand entschieden.** Bestaetigt
Abschnitt 2.3 des Berichts unabhaengig.

Umgekehrt der groesste Abstand: `turtle_soup_stocks` mit **−163,70 %** (Bloecke)
gegen **−2 135,83 %** (chronologisch).

### R.6 — Tests

**253 von 253**, darunter **27 Mutationsproben** — jede Wache wird einzeln
entfernt, und die zugehoerige Pruefung muss dann anschlagen. Rund 7 Minuten;
mit `--ohne-kursdaten` rund 1 Minute. Der Selbsttest weist per `git status`
nach, dass ein Testlauf an Bot-Code, Ergebnisdateien, Kursdaten, Logs und
Datenbanken **nichts** veraendert.

`kind="stable"` ist von Anfang an gesetzt und im Test abgesichert — **N1** ist
an dieser neuen Stelle also gar nicht erst entstanden. Die beiden alten Stellen
(`portfolio_correlation_analysis.py`, `shared/portfolio_overview.py`) bleiben
offen.

### R.7 — Wie es weitergeht

| # | Schritt | Stand |
|---|---|---|
| ~~M1~~ | beide Werte ausweisen | **erledigt** |
| **M2** | volle Kette (Backtest → Walk-Forward → Equity-Simulation → Buy-and-Hold) fuer die **vier** Bots, deren Wahl gekippt waere: `turtle_soup_crypto`, `turtle_soup_stocks`, `elliott_wave_stocks`, `elliott_wave` | offen |
| **M3** | Entscheidung, welches Mass kuenftig fuehrt — mit beiden Zahlen vor Augen | nach M2 |

### R.8 — In einfacher Sprache

**Was wir gemacht haben:** Das Auswahlskript weist ab jetzt **beide** Zahlen aus
— die alte und die richtige, nach Datum sortierte.

**Warum nicht gleich umstellen:** Weil sonst neun gespeicherte Ergebnisdateien,
sechs Berichte und zwei Forschungsordner auf einen Schlag unvergleichbar
wuerden. Mit beiden Zahlen bleibt jede alte Angabe lesbar, und jede neue
Entscheidung sieht den richtigen Wert daneben.

**Was sich dabei zeigte:** Bei einem Bot stehen **−164 %** (alte Rechnung) gegen
**−2 136 %** (nach Datum). Und bei einem anderen sind beide Zahlen gleich — weil
der dort ohnehin schon nach Datum sortiert, was aber nie jemand entschieden hat.

**Was ausdruecklich nicht passiert ist:** Kein Bot hat andere Parameter
bekommen. Das wurde fuer alle neun nachgewiesen.

**Was das fuer dich heisst:** Ab jetzt siehst du bei jeder Optimierung beide
Zahlen. Die Entscheidung, welche kuenftig gilt, faellt bis zum 13. Dezember.

---

## S — TB-19: Stabile Sortierung (PR #91, 13.09.2026)

Erledigt **N1**. Zwei Zeilen geaendert — und dabei drei Befunde gehoben, die
groesser sind als die Aufgabe.

### S.1 — Die Zahlen, exakt wie vorhergesagt

| Kennzahl | vorher | nachher |
|---|---:|---:|
| Kombinierter Vierer-Drawdown | −9,34 % | **−9,41 %** |
| Montags-Mail / Dashboard-Portfolio-Sicht | −11,29 % | **−11,41 %** |

**Die Portfolio-Sicht zeigt ab jetzt −11,41 %.** Kein neuer Fehler — die
Korrektur.

Mit verschoben, ohne dass es angekuendigt war: Einzel-Drawdowns von
`rsi2_crypto` (−13,11 → −13,30 %), `turtle_soup_stocks` (−18,67 → −18,71 %),
`rsi2_mean_reversion` (−11,17 → −11,73 %) sowie **21 der 26** bezifferten
Korrelationen. Keine ueberschreitet die Schwelle 0,3 (groesster Betrag
0,14 → 0,16) — **es aendert sich keine Aussage, nur Nachkommastellen.**
Renditen unveraendert.

### S.2 — Was der Fehler war, und warum die neuen Zahlen die richtigen sind

`sort_values("time")` ohne `kind="stable"` vertauscht Zeilen mit gleichem
Zeitstempel. `groupby("date").last()` greift dann **einen Zwischenstand mitten
im Tag** ab statt des Tagesschlusses.

> **Der Nachweis haengt nicht an Geschmack:** Alle neun `equity_curve.csv`
> stehen bereits **in Ereignisreihenfolge** — nachgemessen — und eine stabile
> Sortierung laesst sie unveraendert.

**Betroffen waren alle neun Bots**, nicht nur die Aktien-Bots: von **1**
abweichenden Tag (`elliott_wave`) bis **698 von 2 022** (`turtle_soup_stocks`).

### S.3 — Die drei Folgebefunde aus der Gesamtsuche

**144** `sort_values`-Aufrufe auf `main`, **31** bereits stabil, **113** ohne
`kind=`. TB-19 stellt **2** um — **111 bleiben.**

| # | Befund | Dringlichkeit |
|---|---|---|
| ~~S1~~ | ~~`elliott_wave_counter.py` entscheidet per Quicksort~~ **ERLEDIGT, TB-20** — siehe Block T. Ergebnis: **Absicherung, keine Korrektur** — null Trades betroffen |
| **S2** | **19 weitere Stellen haben denselben Fehler** — dieselbe `build_daily_capital_curve`-Vorlage steht **21-mal** im Repo. Nicht angefasst, weil ihre Ausgaben in bereits veroeffentlichten Experiment- und `research/`-Dokumenten stehen | mittel |
| **S3** | **`equity_simulation.py` ist gefaehrdet, heute aber unauffaellig.** `collect_all_trades` sortiert `entry_time` instabil (fast alle Zeilen teilen einen Zeitstempel), liefert bei zwei nachgemessenen Bots aber **heute** dieselbe Reihenfolge wie stabil — deshalb meldet `ergebniskurven.py` weiterhin `9x AKTUELL`. **Nicht garantiert.** Auf der Sperrliste | mittel |

**Ungefaehrdet:** die 27 `open_time`-Stellen auf Kursdaten — **0 Dubletten** in
allen 242 `data/*.csv`, gemessen.

### S.4 — Geprueft

`shared/test_stabile_sortierung.py` **46/46** · `shared/ergebniskurven.py`
weiterhin **9x AKTUELL** · beide Skripte zweimal byteweise identisch ·
bestehende Selbsttests unveraendert gegenueber einem Basislauf auf `main`.

Der Test prueft **Verhalten, nicht Quelltext**, und weist an mutierten Kopien
der echten Dateien nach, dass er rot werden kann.

### S.5 — In einfacher Sprache

**Was wir wissen wollten:** An zwei Stellen sortiert das System Daten, ohne
festzulegen, was bei Gleichstand passiert. Macht das einen Unterschied?

**Was herauskam:** Ja, aber einen kleinen — und einen viel groesseren woanders.

**Der kleine:** Die Portfolio-Zahl im Dashboard aendert sich von −11,29 % auf
**−11,41 %**. Der Grund: Wenn mehrere Eintraege denselben Zeitstempel haben,
griff die Auswertung nicht zwingend den **letzten** des Tages, sondern einen
beliebigen dazwischen. Bei einem Bot betraf das **698 von 2 022 Tagen**.

**Der grosse:** Bei der Suche nach aehnlichen Stellen kam heraus, dass auch
**die Wellenauswahl** von Elliott Wave so sortiert — also die Entscheidung,
**welches Kursmuster tatsaechlich gehandelt wird**. Von 144 Sortierungen im
Projekt sind **113** nicht festgelegt.

**Was das fuer dich heisst:** Die Dashboard-Zahl ist jetzt richtig. Und es gibt
eine Liste von Stellen, die noch nachgezogen werden muessen — die wichtigste
davon wurde direkt danach bearbeitet.

---

## T — TB-20: Wellenauswahl (13.09.2026)

Erledigt **S1**. **Absicherung, keine Korrektur** — das Verhalten bleibt, die
Abhaengigkeit von der Sortierimplementierung verschwindet.

### T.1 — Gleichstaende sind der Normalfall, nicht der Randfall

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Muster nach `remove_overlapping` | 283 | 6 439 |
| **davon in einer Gleichstandsgruppe** | **247 (87,3 %)** | **6 372 (99,0 %)** |
| Symbole mit mindestens einem Gleichstand | 23 von 23 | 150 von 150 |
| groesste Gruppe eines Symbols | 17 | **69** |

### T.2 — ⚠️ Der eigentliche Fund: `fib_score` ordnet praktisch nicht

> `fibonacci_score()` addiert drei feste Teilpunkte (0,34 / 0,33 / 0,33) und
> rundet auf zwei Stellen. Oberhalb von `min_fib_score = 0.3` gibt es genau
> **fuenf** moegliche Werte: **0,33 · 0,34 · 0,66 · 0,67 · 1,0**.

**6 439 Aktien-Muster werden auf fuenf Werte abgebildet.** Das heisst: Der
`fib_score` ist **kein Rangkriterium**, sondern eine Vierfach-Klassifikation mit
einer Schwelle — und die eigentliche Auswahl trifft danach etwas anderes.

**Das ist eine Aussage ueber die Strategie, nicht ueber die Sortierung**, und
sie war nicht Gegenstand der Aufgabe. Offener Punkt: **Traegt ein Mass, das
tausende Muster auf fuenf Stufen abbildet, ueberhaupt eine Auswahl?** Gehoert in
die Fable-Rueckmeldung.

### T.3 — Warum trotzdem null Trades betroffen waren

| Frage | Antwort |
|---|---|
| Haengt die **Menge** der Muster an der Sortierung? | **Nein** — `start_time` ist je Symbol eindeutig (0 Dubletten in 173 Symbolen) |
| Hing die **Reihenfolge** an der Implementierung? | **Ja** — Quicksort gegen stabil: 19 von 23 Krypto- und 147 von 150 Aktiensymbolen weichen ab; bei **35** Aktiensymbolen stand ein anderes Muster auf Platz 1 |
| Wertet ein Verbraucher die Reihenfolge aus? | **Nein** — in **0 von 20 114** nachgebildeten Laeufen standen je zwei **neue** Muster desselben Symbols gleichzeitig zur Wahl |

Strukturell, nicht zufaellig: Zwei Muster, deren Welle 5 innerhalb desselben
Frische-Fensters endet (48 h bzw. 5 Tage), ueberlappen sich zwangslaeufig — und
`remove_overlapping` streicht sie auf einen Vertreter zusammen.

**Verhalten unveraendert:** `find_causal_waves` liefert vorher/nachher ueber 173
Symbole und 2 611 Trades **Zeile fuer Zeile identisch**; `ergebniskurven.py`
meldet **9x AKTUELL** (auf dem Mac nachgeprueft, 13.09.2026).

### T.4 — Die eingefuehrte Regel

`RANGFOLGE = ["fib_score", "end_time", "start_time"]`, alle absteigend — bei
Gleichstand gewinnt das **juengere** Muster, bei gleichem Ende das kuerzere.

**Warum das juengere:** Keine neue Regel, sondern die feinere Fassung einer
vorhandenen. `forward_test.py` verwirft ohnehin Muster, deren Welle 5 laenger
als 48 h bzw. 5 Tage zurueckliegt — weil der Einstieg zum **aktuellen** Kurs
erfolgt, nicht zum Kurs am Wellenende. Das Projekt bevorzugt Frische bereits,
bisher nur grob.

**Warum nicht Amplitude:** Sie bestimmt ueber
`target_price = entry + total_move × TAKE_PROFIT_FIB` das Kursziel. Sie zum
Rangkriterium zu machen hiesse, **systematisch die weitesten Ziele zu
bevorzugen** — eine Verschiebung des Risikoprofils, also eine
Strategieentscheidung des Nutzers.

**Nicht geaendert: die Ueberlappungsregel.** Dort gewinnt weiterhin das
**frueher** erkannte Muster — ein spaeteres darf ein frueheres nicht
nachtraeglich verdraengen (Look-Ahead).

### T.5 — Nebenbefund: `kind="stable"` traegt bei mehrspaltiger Sortierung nichts

pandas wertet `kind` bei einer **mehrspaltigen** `sort_values` **nicht aus** —
der Pfad laeuft ueber `lexsort` und ist ohnehin stabil (nachgemessen mit pandas
3.0.5). Der Parameter bleibt als **Absichtserklaerung, nicht als Wache**;
wirksam wuerde er erst, wenn `RANGFOLGE` je wieder auf eine Spalte schrumpft —
der Selbsttest faengt genau diesen Rueckschritt als Mutante ab.

### T.6 — `forward_test.py:168` beurteilt, nicht angefasst

- **Innerhalb eines Symbols erledigt:** Die Auswahlliste hat bei
  `elliott_wave_stocks` in allen 18 253 nachgebildeten Laeufen die Laenge 1.
- **Zwischen Symbolen** entscheidet die Reihenfolge von
  `config/sp500_top150.txt`, wer einen der acht Plaetze bekommt. Die Liste ist
  **absteigend nach Marktkapitalisierung** sortiert — eine feste, systematische
  Ordnung, keine Willkuer einer Sortierimplementierung. **Bei vollem Limit
  bekommen strukturell immer die groessten Werte den Platz.**

> `research/order_sensitivity/BERICHT.md` (Abschnitt 7) beschreibt das bereits
> und bewertet es ausdruecklich nicht. Die Groessenordnung steht dort:
> **21,8 % der Trades dieses Bots sind „umstritten", die Calmar-Spanne reicht
> von 476 bis 920.**

### T.7 — In einfacher Sprache

**Was wir wissen wollten:** Elliott Wave sucht Kursmuster und bewertet sie mit
einem Punktwert. Wenn zwei Muster denselben Wert haben — entscheidet dann der
Zufall, welches gehandelt wird?

**Was herauskam:** Gleichstaende sind nicht die Ausnahme, sondern die Regel:
**99 %** der Aktien-Muster teilen ihren Wert mit mindestens einem anderen.
Trotzdem hat das **keinen einzigen** Trade veraendert — weil eine andere Regel
vorher schon aussortiert und praktisch nie zwei Muster gleichzeitig zur Wahl
stehen.

**Es wurde trotzdem abgesichert:** Bei Gleichstand gewinnt jetzt das **juengere**
Muster. Das ist keine neue Regel, sondern eine feinere Fassung einer
vorhandenen — der Bot bevorzugt frische Muster ohnehin, bisher nur grob.

**Der eigentliche Fund ist ein anderer:** Der Punktwert kann ueberhaupt nur
**fuenf verschiedene Werte** annehmen. **6 439 Muster** werden darauf abgebildet.
Ein Wert, der tausende Faelle in fuenf Schubladen sortiert, ordnet nicht — er
filtert nur.

**Was das fuer dich heisst:** Die Sortierung ist abgesichert. Aber es ist jetzt
eine offene Frage, ob dieser Punktwert ueberhaupt etwas ueber die Qualitaet
eines Musters aussagt. Das wird gerade geprueft.

---

## U — Fable-Rueckmeldung: die Antwort (13.09.2026)

`antwort_rueckmeldung_2026-09-13.md`. Die folgenreichste Antwort der Serie —
sie **stellt die Reihenfolge des Projekts um** und macht mehrere Backlog-Punkte
gegenstandslos.

### U.1 — Die Pointe, die keiner gesehen hatte: die kaputte Auswahl hat die Zahlen geschuetzt

> Selektionsverzerrung entsteht, wenn auf dem Mass **Y** ausgewaehlt und auf
> **Y** berichtet wird. Hier wurde auf **X** (Block-Drawdown) ausgewaehlt und
> auf **Y** (Kapital-Calmar in den Buy-and-Hold-Tabellen) berichtet. Sind X und
> Y unkorreliert, ist das berichtete Y **nahezu unverzerrt**.

**Folge: Die DSR-Korrektur fuer die Historie ist weitgehend gegenstandslos.** Es
gab keine Auswahl auf Y, die zu deflationieren waere. *(Einschraenkung: Der
Betreiber hat die Tabellen gesehen und informell mit-selektiert — Auswahl auf Y
durch das Auge, mit unbekanntem N. Klein, nicht null.)*

**Der Satz, der daraus folgt:**

> **„Die Parameter der neun wurden nie optimiert."** Sie wurden nach einem Mass
> gewaehlt, das mit dem Zielmass **unkorreliert** (sechs Bots) oder **negativ
> korreliert** (drei Bots) ist. Statistisch eine **quasi-zufaellige Auswahl**
> mit Neigung zum Schlechteren bei dreien. Fuer die vier betroffenen Bots ist
> der heutige Satz nicht „der beste von N", sondern **„einer von N"**.

**Und es dreht sich um, sobald das Mass repariert ist:** Die erste Selektion auf
dem Kapitalpfad waere die **erste echte Optimierung in der Geschichte des
Projekts** — ab dann gilt alles zu DSR/PBO/CPCV, **nicht rueckwirkend**.

**Warum die Rangkorrelation bei drei Bots negativ ist** (nicht zufaellig): Ein
Parametersatz mit vielen kleinen Trades je Symbol erzeugt lange Bloecke kleiner
Verluste (hoher Block-Drawdown) und zugleich chronologisch verteilt einen
glatten Kapitalpfad. **Das Mass bestraft Diversifikation ueber die Zeit.**

### U.2 — Die neue Rangfolge, ohne Diplomatie

**F1 zerfaellt.** Vol-Skalierung erledigt (**K.4c**), das Konto als
Messgrundlage **existiert faktisch** (`equity_simulation.py` + H1-Messung).
Uebrig bleibt Netting — Sicherheitsfunktion, kein Renditehebel.

| Rang | Schritt | Backlog |
|---:|---|---|
| **1** | **Das Mass reparieren** — ein chronologischer Kapitalpfad mit echter Positionsgroesse, deterministische Sortierung, Permutationstest. **Das ist NICHT H2** | **M3** + neu |
| **2** | **Neu selektieren** unter dem reparierten Mass, mit Walk-Forward — **und dann erstmals H2** | M2/M3, dann **I4** |
| **3** | **Beta-Bereinigung je Bot**: Rendite und Drawdown gegen **exposure-gleiches** Buy-and-Hold, plus Regressions-Alpha. **Diese Zahl entscheidet, welche Bots bleiben** | neu |
| **4** | **B1 (ETF-Trend)** — die einzige vorgeschlagene Strategie, deren Begruendung durch A3 **staerker** geworden ist: Das Buch ist reiner Aktien-/Krypto-Beta, die einzige nicht-Beta-Quelle im Katalog gewinnt an Gewicht | **I13** |
| **5** | Netting/Deckel als Sicherheit | **I7** |
| 6 | Rest des Katalogs, **G1 gestrichen** | — |

> **„Ihr habt kein gueltiges Mass. H2 kommt danach."**

### U.3 — Die Messregeln, praezisiert (fuer alle kuenftigen Pruefplaene)

**Das Objekt:** Alle Kennzahlen auf **einem chronologischen Kapitalpfad** mit
tatsaechlicher Positionsgroesse, Kosten, Positionslimit und Zuteilungsregel —
also `equity_simulation.py`, **nie eine Trade-Liste**. **Selektion und
Beurteilung auf demselben Objekt.** Das ist die eine Regel, die verletzt wurde,
und sie ist wichtiger als die Wahl der Kennzahl.

**Beurteilung:** Netto-Calmar — aber daneben **Mittelwert der drei tiefsten
Drawdowns** (oder CDaR 5 %) und Netto-Sharpe. *Begruendung:* Der Max-Drawdown
ist eine **Ein-Ereignis-Statistik**; ueber zehn Jahre fast immer 2020 oder 2022.
Zwei Parametersaetze, die sich nur darin unterscheiden, wie sie an drei Tagen im
Maerz 2020 gefuellt wurden, haben verschiedene Calmar-Werte.

**Selektion — bewusst NICHT dieselbe Kennzahl:** **Median des Netto-Sharpe ueber
die Walk-Forward-Falten**, unter der Nebenbedingung, dass der Max-Drawdown je
Falte unter einer **vorab** gesetzten Schwelle bleibt.

> **Warum nicht Calmar fuer die Selektion:** Ein Optimierer auf Calmar findet
> den Parametersatz, der die **eine** schlimmste Episode am gluecklichsten
> umschifft — Overfitting mit Ansage.

**Und die Regel, die zwei Zeilen kostet:**

> **Nicht das Maximum nehmen, sondern die Mitte des Plateaus.** Gewinnt
> Parameter p, sind aber p−1 und p+1 deutlich schlechter, ist p ein
> Zufallstreffer. Sind sie aehnlich, ist die Region real. **Verhindert mehr
> Overfitting als jede DSR.**

**Der Determinismus-Test, neu und fuer alles:** Backtest mit **20 zufaelligen
Permutationen der Symboldatei**; Ergebnis muss **bitidentisch** sein. Sonst gibt
es versteckten Zustand. **Gehoert in die CI, nicht als einmalige Untersuchung.**
Bei jeder Auswahl nach einer Spalte mit moeglichen Gleichstaenden ein zweiter,
**oekonomisch bestimmter** Schluessel — *nicht der Symbolname, das ist
Dateireihenfolge in Verkleidung*.

### U.4 — Der zweite Grund fuer den Permutationsbefund

Der 30-%-Stabilitaetsbefund hat eine **zweite Ursache**, die mit dem Mass nichts
zu tun hat:

> **Wenn ein Positionslimit bindet, entscheidet die Symbolreihenfolge, welches
> Signal den Platz bekommt.** Versteckter Zustand im Backtester.

Deshalb steht in allen fuenf Strategie-Ausarbeitungen die Regel „gleichzeitige
Signale ueber dem Limit: **Rang nach Signalstaerke**" — **dieselbe Regel gehoert
in die neun bestehenden Bots.** Das adressiert **T.6** (`sp500_top150.txt`
entscheidet bei vollem Limit) an der Wurzel.

### U.5 — Der Live-Record ist der Holdout

> **Der laufende Paper-Trading-Record ist die einzige selektionsfreie Evidenz,
> die das Projekt hat.** Er entstand unter Parametern, die auf keinem gueltigen
> Mass gewaehlt wurden — als Test der **Parameter** schwach, als Test des
> **Backtesters** wertvoll: Stimmt der Kapitalpfad des Backtests fuer den
> Live-Zeitraum mit dem Live-Pfad ueberein?
>
> **Nie zur Neuselektion verwenden. Er ist der Holdout, und er waechst.**

Deckt sich mit **I5**.

### U.6 — Zu M1/M2/M3: „Richtig als Uebergang mit Datum. Falsch als Zustand."

**Das Argument gegen die Dauerloesung:** Zwei Masse im Repo bedeuten, dass der
naechste Mensch — oder der naechste Agent — auf dem optimiert, das gerade
bequemer ist. Und das alte Mass ist **keine andere Sicht auf dieselbe Sache**:
nicht-chronologisch, in Prozent-Einheiten, die als Kapitalverlust unmoeglich
sind. **Es gibt keine Frage, auf die es die Antwort ist.**

**Zu den Kosten des Wechsels:** Die neun Ergebnisdateien, sechs Berichte und
zwei Forschungsordner sind **bereits entwertet** — nicht durch den Masswechsel,
sondern durch die Erkenntnis, dass ihr Mass nichts misst. Das doppelte Ausweisen
rettet sie nicht, es **verschiebt nur den Zeitpunkt, an dem das ausgesprochen
wird**. Was sich retten laesst: eine **Archivtabelle** mit altem und neuem Wert
nebeneinander — ein Dokument, kein Live-Output.

| | |
|---|---|
| **Frist** | Beide Werte **bis zur ersten Neuselektion** auf dem neuen Mass. Ein Ereignis, kein Datum |
| **Danach** | Altes Mass aus jedem Live-Pfad **entfernen**, nur in der Archivtabelle behalten |
| ⚠️ **Warnung** | „Findet die Neuselektion nicht innerhalb eines Quartals statt, ist ‚beide ausweisen' zum Zustand geworden — dann ist es die Vertagung." **Also bis 13.12.2026** |
| ⚠️ **Ausnahme** | **Die Zielfunktion von Agent 2 ist der eine Fall, wo Warten aktiv schadet.** Ein Agent, der auf dem alten Mass vorschlaegt, schlaegt bei drei Bots **systematisch den schlechteren Kapitalverlauf** vor. **Sofort umstellen, nicht auf die Frist warten** |

### U.7 — Sentiment: tot, „und zwar nicht knapp"

**Die Literatur** (fremde Messungen): Tetlock 2007 — Marktsignal, klein, Umkehr
binnen einer Woche. Tetlock/Saar-Tsechansky/Macskassy 2008 — staerker bei
**kleinen** Firmen, bei Grosswerten schwach und schnell eingepreist.
Heston & Sinha 2017 — **taeglich** ein bis zwei Tage Vorlauf, **woechentlich
aggregiert** bis zu einem Quartal; bei grossen Firmen schneller und schwaecher.
Ke/Kelly/Xiu 2019 — Halbwertszeit ~2 Tage, groesster Teil aus der **Short**-Seite
und kleinen Titeln. Lopez-Lira & Tang 2023 — dito, und **schwaecher werdend,
sobald das Verfahren bekannt war**. Krypto: **keine** Arbeit bekannt, die
Tages-Sentiment fuer BTC/ETH nach Kosten als tragfaehig zeigt.

**Nach 0,30 Prozentpunkten:** Ein Tageseffekt mit Halbwertszeit 1–2 Tage braucht
taegliche Umschichtung = 250 Round Trips = **75 pp/Jahr**. Die Literatureffekte
liegen, auf Long-only-Grosswerte heruntergerechnet, bei **einigen Basispunkten
pro Tag** — eine Groessenordnung unter den Kosten.

**Die Stichprobenrechnung ist vernichtend:** 10 Symbole × 250 Tage = 2 500
Symbol-Tage. Tagesvol ≈ 1,5 %, Standardfehler ≈ 3 Basispunkte — aber die zehn
Titel sind an Markttagen **nicht unabhaengig**, effektiv eher √250 → **9–10
Basispunkte**. Nachweisbar waere erst ein Effekt von **20 Basispunkten
taeglich**. Das ist eine Groessenordnung ueber allem, was die Literatur fuer
Grosswerte findet.

> **Urteil: „340 $ fuer taegliche Scores auf zehn Symbolen bezahlen eine
> beantwortete Frage mit einer Stichprobe, die sie ohnehin nicht beantworten
> koennte."**

**→ I.3g wird geschlossen.** Das einzige echte Argument fuers Sammeln
(forward-gesammeltes Sentiment ist point-in-time, historische Datensaetze oft
nicht) zaehlt nur, wenn die Frage offen waere.

### U.8 — ⚠️ Der Ersatzvorschlag: Nachrichten-**Anwesenheit** als Filter (NEU, U1)

**Chan (2003, JFE):** Grosse Kursbewegungen **mit** Nachricht driften weiter;
grosse Bewegungen **ohne** Nachricht **kehren um**.

> **D1 und C1 handeln genau solche Bewegungen — und wissen nicht, welche.** D1
> (grosser Sprung nach oben, Fortsetzung erwartet) sollte bei
> **Nachrichten**-Gaps besser funktionieren, C1 (grosser Einbruch, Umkehr
> erwartet) bei **Nicht-Nachrichten**-Einbruechen.

Ein Aufruf, der **nur** fragt: „Gab es zu diesem Titel an diesem Tag eine
Nachricht, und welcher Art?" — **keine Tonalitaet**, nur Anwesenheit und Klasse.

| | |
|---|---|
| Ereignisse | D1 + C1 zusammen ~**150–250** Aktienereignisse im Jahr |
| Kosten | ~0,13 $ je Symbol-Aufruf → **20–35 $ im Jahr** |
| Verhaeltnis | **Ein Prozent der 340 $** — fuer eine Frage, die **nicht** beantwortet ist |
| Stichprobe | 150–250 Ereignisse reichen fuer einen **Zweigruppenvergleich**, wenn der Chan-Unterschied in dieser Groessenordnung existiert |

**Zwei Einschraenkungen:** (1) „Keine Nachrichten" war eine Randbedingung des
Systems — ob ein Agent, der Ereignistage klassifiziert, diese Grenze verletzt,
ist ein **Betreiberentscheid**. (2) Der Filter kann **nur nach** dem Backtest von
D1/C1 auf reinem OHLCV geprueft werden — als Frage, ob er die Trefferquote hebt.
**Ohne die reine Version gibt es keine Basislinie.**

### U.9 — Die drei geparkten Ideen

**Hebel (I.3e):** „Das Buch ist zu 38 % investiert. **Der erste Faktor 1,5 ist
kein Hebel, sondern Auslastung**" — er nutzt Kasse, die da ist, und braucht kein
Margin. Erst ueber **~2,6×** waere es Hebel im Wortsinn. Die Frage aendert sich
zu: *warum ist die Auslastung so tief, und ist mehr davon gut?* Antwort offen —
ein Buch, das an seinen schlechtesten Tagen **mehr** investiert ist als im
Mittel (38,1 gegen 37,9), skaliert seinen Drawdown proportional mit.

*Konstanter Hebel verbessert den Calmar nicht* (Rendite ~linear, Drawdown etwas
mehr als linear; −32 % auf investiertem Kapital wuerden mit 1,5× zu ~−45 %) —
**Risikoappetit-Frage, keine Strategiefrage**.

*Mein Argument greift doch, aber woanders:* **„in bestimmten Phasen" ist ein
Timing-Signal.** Ex-post ist Look-Ahead, ex-ante ein Parameter mehr auf
denselben zwei bis drei Regimen. **B3 legt die Regel nahe — mit der Vol
skalieren statt gegen sie** — aber „ein Befund ueber das Vorzeichen ist noch
keine Regel". Abbruch: Schlaegt die bedingte 1,5× die **konstante** 1,5× im
Falten-Median nicht, war die Phasendefinition nichts wert.

**Gewinnsicherung (I.3c): andere Familie, und keine Forschungsfrage.**
Vol-Skalierung und Trailing Stops greifen in den **Handelsprozess** ein; eine
Reserve veraendert die **Kapitalbasis**, auf der derselbe Prozess laeuft. Eine
**Entnahmepolitik** kann den Sharpe weder verbessern noch verschlechtern. „Ein
Backtest wird trivial zeigen: weniger Rendite, weniger Drawdown auf
Gesamtvermoegen. **Das ist keine Erkenntnis, das ist Arithmetik.**" Zwei
Punkte trotzdem: **Der Nenner muss festgelegt sein** (Drawdown auf
Handelskapital sieht nach Entnahmen groesser aus, auf Gesamtvermoegen kleiner —
wer beides vermischt, verwechselt Politik mit Leistung). Und **im
Paper-Trading ohne Wirkung**.

**Haltedauern (I.3f): eigene Dimension, aber die zweite.** Die Ertragsquelle
sagt **warum**, der Horizont **wann**, wie kostenempfindlich und an welches
Rauschen gekoppelt. *Fremde Messung:* In der Trendfolge-Literatur sind Signale
auf 1-, 3- und 12-Monats-Horizont untereinander nur maessig korreliert (Grund,
warum Hurst/Ooi/Pedersen sie kombinieren). **Aber:** Horizont-Streuung ohne
Quellen-Streuung schuetzt nicht — 2022 hat Long-only-Aktientrend **auf jedem
Horizont** verloren.

*Konkret und billig, nur aus den Trade-Logs:* je Bot die Verteilung der
Haltedauern (Median, Quartile), dann eine **Ueberlappungsmatrix** — welcher
Anteil der Tage, an denen Bot A haelt, haelt auch Bot B im selben Titel oder
derselben Klasse, und wie oft oeffnen sie **innerhalb von drei Tagen**
nacheinander. *Fables ungemessene Erwartung:* **Sechs der neun haben
Median-Haltedauern zwischen drei und zehn Tagen und bespielen ein Fenster.**
Traefe das zu, waere es ein Befund derselben Art wie A3 — **vermeintliche
Streuung, die keine ist**.

### U.10 — Die sieben Ruecknahmen

1. **„80–95 % Kasse"** — aus einer einzigen Zahl einen Mechanismus abgeleitet,
   ohne zu fragen, ob die Zahl richtig berechnet war. Richtig waere gewesen:
   *„Entweder ist das Buch fast leer, oder die Zahl ist falsch — messt beides."*
2. **F1 auf Platz eins mit Vol-Skalierung als Kern.** Die zitierte Literatur
   (Moreira/Muir, Harvey et al.) misst Vol-Targeting auf **Anlagen und
   Faktoren**, nicht auf **Strategie-Positionen innerhalb eines Trends**.
   Trendfolge-Renditen sind **konvex in der Volatilitaet**.
3. **Inverse Vol als Voreinstellung** in den Ausarbeitungen (Clips 0,5–1,5 in
   D1/C1, 1/σ im Neubau) — **Test-Arm, nicht Standard**. In B1 bleibt die
   Literaturform.
4. **Elliott Wave als „strukturell kleines Buch"** — falsch. Urteil aendert
   sich von „streichen" zu **„unentschieden, Prior skeptisch"**. *Neue
   Ueberschlagsrechnung:* 47,6 % Exposure an einem Universum mit +756 % ergaebe
   grob +190–200 %; EW hat **+353 %** — **mehr Rendite je Exposure-Einheit**.
   Aber −22,4 % Drawdown, wo exposure-gleiches B&H etwa −13 bis −15 % gehabt
   haette — **mehr Risiko je Exposure-Einheit**. Risikoadjustiert ~Gleichstand.
   **Der Zufalls-Timing-Test (I3) entscheidet es und ist nicht gelaufen.**
5. **G1 und die ganze Tail-Abhaengigkeits-Erzaehlung — gegenstandslos.** „Es
   gab kein verstecktes Tail-Risiko zu modellieren, es gab schlichtes Beta, das
   die Messung nicht sehen konnte. Eine 9×9-Matrix aus 75 Stresstagen war die
   komplizierte Antwort auf eine Frage, die ein Mark-to-Market geloest hat."
   **→ I6 entfaellt.**
6. **H2 an der falschen Stelle.** „Die richtige erste Frage an das Projekt waere
   gewesen: **‚Zeigt mir das Skript, das die Parameter auswaehlt.'**"
7. **Befund 1 („Kapitalmanagement ist der Engpass")** — mit demselben Mass
   gerechnet, das B1 verwirft. **Bis zur Wiederholung auf dem Kapitalpfad nicht
   belegt.**

**Nicht zurueckgenommen:** „Messung vor zehntem Bot", die fuenf Strategien mit
ihren Abbruchkriterien, der Neubau-Entwurf in seiner Struktur, die
Zuteilungsregel nach Signalstaerke, das Sentiment-Urteil.

> **Der Schlusssatz:** „Die Schlussfolgerung hat gehalten, weil ihr besser
> gemessen habt, als ich gedacht habe — nicht, weil ich besser gedacht haette,
> als ihr gemessen habt."

### U.11 — Was sich im Backlog aendert

| Punkt | Neuer Stand |
|---|---|
| **I.3g** Sentiment | **GESCHLOSSEN** — U.7. Ersetzt durch **U1** (Nachrichten-Anwesenheit als Filter, 20–35 $/Jahr) |
| **I6** Stress-Korrelation A1/G1 | **ENTFAELLT** — U.10 Punkt 5, gegenstandslos |
| **I4** DSR/PBO/CPCV | **VERSCHOBEN nach hinten** — erst nach Mass-Reparatur und Neuselektion. Fuer die **Historie** weitgehend gegenstandslos (U.1) |
| **I7** gemeinsames Konto | **Bleibt, aber Rang 5** — reduziert auf **Netting/Deckel** als Sicherheitsfunktion |
| **I8** Vol-Skalierung | bleibt erledigt; Fable nimmt sie ausdruecklich zurueck |
| **M3** Mass-Entscheidung | **NEUE FRIST: 13.12.2026.** Danach ist „beide ausweisen" zur Vertagung geworden |
| ~~Agent 2~~ Zielfunktion | ✅ **ERLEDIGT, PR #94 (TB-22)** — siehe Block W |
| **I13** B1 ETF-Trend | **hochgestuft auf Rang 4** — die einzige Strategie, deren Begruendung **staerker** geworden ist |
| **I.3c** Gewinnsicherung | **Keine Forschungsfrage** — Betreiberentscheidung fuer echtes Geld, im Paper-Trading ohne Wirkung |
| **I.3e** Hebel | **Umformuliert:** bis 2,6× ist es **Auslastung**, kein Hebel. Die Frage lautet „warum so tief investiert" |
| **I.3f** Haltedauern | **Bestaetigt als eigene Dimension**, aber zweitrangig. Konkrete Untersuchung skizziert (U.9) |
| **T.6** `sp500_top150.txt` | **Wurzelloesung benannt:** Zuteilung nach **Signalstaerke** statt Dateireihenfolge — gehoert in alle neun Bots (U.4) |
| **NEU** | **Determinismus-Test in die CI** (20 Permutationen, bitidentisch) — U.3 |
| **NEU** | **Beta-Bereinigung je Bot** — exposure-gleiches B&H + Regressions-Alpha. **Diese Zahl entscheidet, welche Bots bleiben** (Rang 3) |

---

## V — Fable, zweite Rueckfragenrunde (13.09.2026)

`antwort_rueckfragen_2026-09-13_teil2.md`. **Praezisiert alles, was in Block U
offen blieb** — und ersetzt den Sentiment-Zweig durch etwas Besseres.

### V.1 — Der `fib_score` ist gar kein Score, sondern eine Zaehlung

> Drei feste Teilpunkte (0,34 / 0,33 / 0,33), aufsummiert und gerundet, ergeben
> eine **Zaehlung erfuellter Bedingungen** — null, eine, zwei oder drei — mit
> einer kosmetischen Verkleidung als Dezimalzahl. **Die fuenf Werte sind in
> Wahrheit drei Stufen.**

**Und der Unterschied 0,33 gegen 0,34 ist ein Rundungsartefakt:** Er haengt
davon ab, welcher der drei Teilpunkte zufaellig auf 1,0 aufrundet. Er wirkt
trotzdem — bei genau einer erfuellten Bedingung wird das Muster mit der
0,34-Bedingung **systematisch vorgezogen**. *„Ein Tie-Break, den niemand
gewaehlt hat und der nichts bedeutet."*

`min_fib_score = 0.3` heisst damit: **mindestens eine von drei Bedingungen** —
ein Drittel der Kriterien reicht. Ein schwacher Filter.

**Was ein Drei-Stufen-Mass kann und was nicht:**

| | |
|---|---|
| ✅ **Filter** (Schwelle ≥ 1, ≥ 2 oder = 3) | tut es heute |
| ✅ **Ordinalskala innerhalb eines Symbols** | legitim — **sofern** die Hypothese „mehr erfuellte Bedingungen → bessere Trades" stimmt |
| ❌ **150 Symbole ranken** | Bei 6 439 Mustern auf drei Stufen hat jede Stufe im Mittel ueber **2 000** Mitglieder. Ein Ranking ueber Symbole ist eine **Zufallsziehung innerhalb der Stufe** |

**→ V1 (NEUE AUFGABE, in einer Stunde machbar): Ereignisrendite je Stufe.**
Alle 6 439 Muster nach Stufe gruppieren, Nettorendite ueber die Bot-Haltedauer
je Gruppe mitteln, Bootstrap-Intervalle. Drei moegliche Ausgaenge:

1. **Rendite steigt monoton** → echte Ordinalskala; Schwelle koennte auf ≥ 2
   gehoben werden, Auswahl innerhalb eines Symbols begruendet
2. **Kein Unterschied** → der Score traegt nichts; die Schwelle ist eine
   Zufallsstichprobe. *„Dann bleibt vom Elliott-Wave-Bot ein Zigzag-Detektor
   mit Stop."*
3. **Nur die 3-von-3-Gruppe unterscheidet sich** → Ja/Nein-Filter mit der
   **falschen** Schwelle

**Offene Nebenfrage (Fable kennt den Code nicht):** Sind die drei Bedingungen
**Schwellen auf kontinuierlichen Groessen** (etwa „Retracement innerhalb ±5 %
von 0,618")? Wenn ja, existiert **unter** dem Score eine stetige Groesse — der
Abstand zum Zielverhaeltnis —, die weggeworfen wird, indem man sie auf 0/1
schneidet. **Davon haengt V.2 ab.**

### V.2 — Die Zuteilungskaskade (ersetzt „Rang nach Signalstaerke")

**Vier Eigenschaften, die ein Zuteilungskriterium haben muss:**

1. **Oekonomisch bestimmt** — notwendig, aber **nicht hinreichend** (der
   `fib_score` ist es und versagt trotzdem)
2. **Aufloesung** — bei bindendem Limit darf in hoechstens **2 %** *(willkuerlich)*
   der Faelle ein Gleichstand an der Kante zwischen Platz und Nicht-Platz
   auftreten. *Eine stetige Groesse erfuellt das automatisch; eine Zaehlung nie*
3. **Point-in-time und skalenfrei** — Gap in σ, nicht in Prozent; Volumen als
   Vielfaches des Medians, nicht absolut
4. **Reihenfolge-invariant** — der Permutationstest (**TB-23**) ist die
   operative Definition davon

> Umgekehrt reicht Aufloesung allein auch nicht: **Der Symbolname hat perfekte
> Aufloesung und ist oekonomisch leer.**

**Die Kaskade fuer alle neun Bots und die fuenf Strategien:**

| Rang | Kriterium |
|---:|---|
| 1 | **Strategieeigene stetige Signalstaerke**, falls vorhanden |
| 2 | **Diversifikationsbeitrag** — 60-Tage-Korrelation des Kandidaten mit dem aktuellen Buch des Bots, **niedriger zuerst**; bei leerem Buch entfaellt er |
| 3 | **Liquiditaet** — 20-Tage-Median-Dollar-Volumen, hoeher zuerst |
| 4 | **Seeded Zufall**, Seed protokolliert |

*Warum Diversifikation an zweiter Stelle:* stetig, point-in-time, oekonomisch
klar, und **bevorzugt keinen Titel systematisch**. *Warum Liquiditaet erst
dritt:* Ausfuehrungskriterium ohne Alpha-Anspruch, aber mit **Schlagseite zu
Mega-Caps**. *Warum seeded Zufall statt Symbolname:*

> **„Ehrliche Beliebigkeit schlaegt versteckte."** Ein protokollierter Zufall
> ist **sichtbar** willkuerlich und reproduzierbar; die Dateireihenfolge ist
> **unsichtbar** willkuerlich.

**Fuer `elliott_wave_stocks` konkret:** Liegen unter dem Score stetige Abstaende
(V.1-Nebenfrage), ist die **Summe der normierten Abstaende zu den
Zielverhaeltnissen** der Primaerschluessel — mit dem Vorbehalt, dass „naeher am
Fibonacci-Ideal = besserer Trade" eine **Hypothese** ist, die derselbe
Stufentest erst pruefen muss. Wenn nicht, beginnt die Kaskade beim
Sekundaerschluessel:

> *„Das ist dann kein Mangel der Regel, sondern eine ehrliche Aussage ueber den
> Bot: **Er hat keine Signalstaerke, nur ein Signal.**"*

### V.3 — B1 beantwortet: Ja, es reicht — mit zwei Bedingungen und einer Reihenfolge

> **„Der Korrektheitsfehler liegt in der Zielfunktion, nicht in der
> Architektur."** Neun Fassungen von `multi_symbol_optimise.py` sind ein
> **Wartungs**problem; die Summe von Trade-Prozenten in Blockreihenfolge ist ein
> **Mess**problem. Das Messproblem ist in jeder Fassung **dieselbe Stelle**: der
> Aufruf, der aus der Trade-Liste eine Zahl macht.

Ein gemeinsamer Backtester ist **Schritt 0 des Neubaus** und gehoert auf eine
eigene Spur — **danach, nicht davor**.

**Bedingung 1 — `diff` ueber die neun `equity_simulation.py`, erster Arbeitstag.**
Sind sie identisch: in ein gemeinsames Modul ziehen (loest zugleich
Importkollision und Subprozesse). Sind sie es nicht, ist jeder Unterschied
entweder bot-spezifisch noetig oder eine **stille Divergenz** — genau die
Fehlerart, die die Kurven-Erneuerung gefunden hat. *„Neun Masse in neun
Fassungen waeren dasselbe Problem noch einmal."*

**Bedingung 2 — die Zuteilungskaskade VOR der Neuselektion.** Sonst waehlt die
Auswahlschleife Parameter auf einem Objekt, das **noch von der Dateireihenfolge
abhaengt** — die Neuselektion wuerde das Artefakt **einbauen statt beseitigen**.

> **Reihenfolge: Zuteilungskaskade + Permutationstest → Zielfunktion tauschen →
> laufen lassen.**

**Zum Rechenaufwand — der groesste Hebel war nicht auf dem Schirm:**

| Massnahme | Wirkung |
|---|---|
| **Raster trennen in Erkennungs- und Handelsparameter** | Deviation und Wellenregeln bestimmen, **welche Muster existieren**; Stop, Ziel, Haltedauer und Limit, **was mit ihnen geschieht**. Erkennung je Erkennungs-Parametersatz **einmal** rechnen und cachen. Bei 5×5×4×4 faellt sie **25-mal statt 400-mal** an. *„Der einzelne groesste Hebel, und er ist unabhaengig vom Masswechsel richtig."* |
| **Grob rastern, Plateau suchen** | Die Plateau-Regel braucht kein feines Raster, sie braucht **Nachbarn**. Drei bis fuenf Stufen je Dimension reichen |
| Walk-Forward | **multipliziert die Laufzeit nicht** — Signale einmal ueber die volle Historie, die Kapitalsimulation je Falte ist ein Zeitschnitt |

**Aufwandsschaetzung (ohne Gewaehr):**

| Woche | Inhalt |
|---|---|
| **1** | `diff` der Simulationen, gemeinsames Modul, Zuteilungskaskade, Permutationstest in die CI |
| **2** | Raster trennen und cachen, Zielfunktion in den neun Optimierern tauschen, Ausgabe = Falten-Median Netto-Sharpe + Max-DD + Calmar + Nachbarschaft |
| **3–4** | Laeufe, Neuselektion, Archivtabelle alt/neu |

> Damit bleibt vor dem **13.12.** Luft fuer das, was dabei herauskommt und nicht
> geplant war — *„bei diesem Projekt bisher immer etwas."*

**Am ersten Tag zu klaeren:** Was rechnet `calculate_robustness_score`? Ist es
eine Plateau-Logik, gehoert es in die neue Zielfunktion; rechnet es auf der
Block-Trade-Liste, ist es **Teil des Problems**.

### V.4 — Die Beta-Bereinigung: beide Benchmarks, und ihre Differenz ist die dritte Antwort

| Benchmark | Beantwortet |
|---|---|
| **Konstante Exposure** (gemessenes Mittel, dauerhaft) | „Ist der Bot besser als eine **statische Position derselben Groesse**?" Robust, ein Wert |
| **Tagesgenau nachgebildete Exposure** | „Gegeben **wann** der Bot investiert war — hat seine **Titelauswahl** etwas beigetragen?" Isoliert Auswahl vom Timing |
| **Die Differenz** | **Der Beitrag des Timings**: Was hat es gebracht, an **diesen** Tagen investiert zu sein statt konstant? |

> Damit zerlegt sich die Bot-Rendite in **statisches Beta + Timing + Auswahl**
> (+ Rest aus Kosten und Pfad). *„Mehr wert als ein einzelnes Alpha, weil sie
> sagt, **wo** ein Bot etwas kann — ein Trendfolger sollte im Timing verdienen,
> ein Mean-Reverter in der Auswahl."*

**Wogegen regressieren:** gegen das **gleichgewichtete point-in-time-Universum
des Bots** — die 150 Aktien bzw. 25 Krypto-Paare, die er handeln **darf**. Das
ist die Alternative „nichts tun, alles halten", die ihm offenstand. *SPY enthaelt
350 Titel, die er nicht handelt; BTC ist ein Titel von 25.* Beide trotzdem als
**Zweitbenchmark** ausweisen. Standardfehler nach **Newey-West mit Lag gleich
der Median-Haltedauer** (Strategierenditen sind autokorreliert).

**Die Schwellen — und warum es keine Signifikanzschwellen sein koennen:** Bei
130 Trades und ~10 % Tracking Error hat ein wahres Alpha von 2 % p. a. eine
t-Statistik um **0,6**.

> *„Wer ‚signifikant' zur Bedingung macht, behaelt alle oder keinen."*

| Klasse | Kriterium *(alle Zahlen willkuerlich)* |
|---|---|
| **Geht** | Netto-Alpha ≤ 0 **und** Calmar unter dem der konstanten Exposure. *Der Bot ist Buy-and-Hold mit Umschlagskosten.* Budget geht in den Benchmark |
| **Bewaehrung** | Alpha > 0, aber Vorzeichen haelt **nicht** in ≥ 3 von 4 Zeitvierteln. Bot bleibt, wird aber **als Beta gezaehlt, nicht als Diversifikator**; Budget waechst nicht |
| **Bleibt** | Alpha > 0, Vorzeichen in 3 von 4 Vierteln, **Block-Bootstrap-80-%-Intervall** (bewusst schwaecher als 90/95) schliesst null aus |

### V.5 — Der Zufalls-Timing-Test, definiert

**Objekt:** die tatsaechliche Trade-Liste — je Trade Symbol, Einstiegstag,
Haltedauer, Groesse.

| Variante | Was permutiert wird |
|---|---|
| **Timing-Test** | Symbol, Groesse, Haltedauer bleiben; der **Einstiegstag** wird neu gezogen, gleichverteilt **innerhalb desselben Kalenderjahres**, ohne Ueberlappung gleicher Symbole. *Warum dasselbe Jahr:* Es erhaelt Jahres-Exposure und Regime und befreit nur die Wahl des Tages — **genau das, was ein Wellensignal zu leisten behauptet**. Quartalsfenster als strengerer Test-Arm |
| **Auswahl-Test** | Einstiegstage und Haltedauern bleiben; die **Symbole** werden aus dem point-in-time-Universum desselben Tages neu gezogen |

**Fuer Elliott Wave ist der Timing-Test der entscheidende** — die Behauptung des
Bots **ist** eine Timing-Behauptung.

**1 000 Ziehungen je Bot und Variante.** Braucht keine Signalerkennung, nur die
Kapitalsimulation auf synthetischen Trade-Listen — **Minuten, nicht Stunden**.

**Kennzahl: Netto-Calmar des Kapitalpfads**, dieselbe wie zur Beurteilung.
**Nicht** das Alpha aus V.4: Der Zufallstest ist **beta-neutral durch
Konstruktion** (Zufalls-Trades in denselben Symbolen tragen dasselbe Beta) und
survivorship-neutral — *„genau deshalb ergaenzt er B2, statt es zu
wiederholen."*

**Warum das 95. Perzentil:** *„Der Median ist keine Latte: Die Haelfte aller
zufaelligen Trade-Listen schlaegt ihn."* Das Perzentil **ist** ein p-Wert — 95
heisst einseitiger Test auf 5 %. **Konvention, nicht Ableitung.**

**Auslegung, mit Effektgroesse** (Calmar des Bots − Median der Zufallsverteilung,
geteilt durch deren Standardabweichung):

| Ergebnis | Bedeutung |
|---|---|
| **≥ 95. Perzentil** | Timing nachgewiesen bei dieser Stichprobe |
| **80.–95.** | Nicht unterscheidbar von Zufall **bei dieser Stichprobe** — bei 130 Trades der **wahrscheinlichste Ausgang auch fuer einen guten Bot**. Bedeutung: **Bewaehrung, nicht Verwerfen** |
| **< 80. bei positiver Effektgroesse** | Timing schwach |
| **< 80. bei negativer Effektgroesse** | ⚠️ **Das Timing schadet** — der Bot waere mit **zufaelligen** Einstiegstagen besser gewesen. **Verwerfungsgrund, unabhaengig von Signifikanz** |

**Grenzen:** Ein Timing, das nur in seltenen Episoden wirkt (2022), ist bei 130
Trades kaum zu sehen. Und die Ziehung innerhalb des Jahres unterstellt, dass die
**Jahres**-Exposure keine Timing-Leistung ist — Regime-Timing wird hier nicht
getestet, sondern in V.4 als Differenz der Benchmarks.

### V.6 — ⚠️ SEC EDGAR ersetzt den Modellaufruf (ersetzt U1)

> Die Frage „gab es zu diesem Titel an diesem Tag ein wesentliches
> Unternehmensereignis, und welcher Art" hat fuer US-Grosswerte eine
> **amtliche, kostenlose, mit Zeitstempel versehene Antwort: SEC EDGAR.**

Ein **Form 8-K** ist per Definition die Meldung eines wesentlichen Ereignisses;
die **Item-Nummer ist die Klasse** (2.02 Ergebnisse · 1.01 wesentliche Vertraege
· 5.02 Fuehrungswechsel · 7.01 Regulation FD · 8.01 Sonstiges), dazu 10-Q und
10-K. Der Volltextindex ist per API abrufbar, Einreichungen tragen einen
**Annahme-Zeitstempel**, die Historie reicht ueber den ganzen Backtest-Zeitraum.

**Chans Trennung wird zu einer Regel ohne Modell:**

```
"mit Nachricht":  8-K / 10-Q / 10-K mit Annahmezeit im Fenster
                  [Vortag nach Boersenschluss, Ereignistag vor Boersenschluss]
Klasse:           Item-Nummer
"ohne Nachricht": kein Filing im Fenster
```

| gegenueber dem Modellaufruf | |
|---|---|
| Kosten | **null** statt 20–35 $/Jahr |
| Historie | **voll** statt zwoelf Monate → **1 000–1 400** D1- und **2 000–2 500** C1-Ereignisse statt 150–250 |
| Look-Ahead | **keine Frage** — der Zeitstempel ist der Zeitstempel |
| Reproduzierbarkeit | vollstaendig, kein Modell im Pfad |

**Zwei Grenzen:** (1) 8-K erfasst **Unternehmens**ereignisse, nicht
Marktnachrichten — eine Analystenherabstufung, ein Geruecht, ein
Wettbewerber-Ereignis erzeugen kein Filing. *Fuer Chans Zweck (Fundament gegen
Rauschen) ist das die **richtige** Trennung.* (2) Es ist eine **neue
Datenquelle** — ob ein Filing-Kalender die Randbedingung „keine
Fundamentaldaten" beruehrt, ist ein **Betreiberentscheid**. Es sind keine Zahlen
aus den Filings, nur **Existenz und Klasse**.

**Krypto hat kein EDGAR.** Dort bliebe der Modellaufruf — *„ich wuerde den
Filter fuer C1-Krypto zunaechst nicht bauen; die Stichprobe (200 Ereignisse) ist
ohnehin an der Grenze."*

**Ergaenzungen fuer Marktnachrichten, falls gewuenscht:** GDELT (frei,
zeitgestempelt, aber grob und laut); kommerzielle News-APIs mit Zeitstempeln
(Polygon/Benzinga, Finnhub, Tiingo — einige zehn Dollar monatlich,
Historientiefe unterschiedlich, **Konditionen unbelegt**). Factiva und RavenPack
institutionell bepreist.

### V.7 — Und der Einwand, der die urspruengliche Idee ohnehin erledigt haette

> **„Fuer Mega-Caps gibt es an fast jedem Tag Nachrichten. Die Anwesenheitsfrage
> ist fuer AAPL oder NVDA trivial mit Ja zu beantworten."**

Das brauchbare Label ist nicht **Anwesenheit**, sondern **Klasse und
Wesentlichkeit**: geplantes Unternehmensereignis (Ergebnis, Ausblick),
ungeplantes wesentliches (Uebernahme, Regulierung, Rechtsstreit, Produkt), oder
keines davon. *„Das ist die 8-K-Taxonomie, nur ohne das 8-K."*

**Drei Selbsttests, falls doch ein Modell im Pfad bleibt (Live oder Krypto):**

1. **Kontrolltage blind mitklassifizieren** — je Ereignistag ein zufaelliger
   Nicht-Ereignistag desselben Titels, ununterscheidbar im Aufruf. Basisrate
   fuer Grosswerte grob **3–6 %** *(Ueberschlag, keine Messung)*. Meldet das
   Modell an 30 % der Kontrolltage ein Ereignis, **ueberlabelt es**
2. **Quellenpflicht mit Datum** — jede Quelle, die **nach** dem Ereignistag
   datiert ist, ist ein Look-Ahead-Treffer; die **Rate** ist die Kennzahl. Ueber
   wenigen Prozent unbrauchbar — *„was bei Suche im offenen Web meine Erwartung
   ist"*
3. **Wiederholbarkeit** — dieselbe Anfrage an zwei Tagen, plus eine
   **Handstichprobe von 50 Ereignissen**, vom Nutzer blind gelabelt

### V.8 — Die Architektur-Korrektur zu meiner Kostenmessung

> **„Die Konsequenz ist nicht ‚anderes Modell', sondern andere Architektur:
> Die Suche gehoert nicht ins Modell."**

Der Kostentreiber war, dass das Modell **selbst** sucht und die Treffer als
Eingabe zurueckbekommt (18 801 von 19 885 Token). *„Ein Begrenzungsparameter,
der ignoriert wird, ist ein Parameter, den du nicht hast."*

**Die Loesung:** Retrieval selbst machen, Klassifikation dem Modell **mit
abgeschalteter Suche** ueberlassen. Schlagzeilen fuer den Ereignistag holen
(EDGAR-Index oder News-API mit Zeitstempel), dem Modell geben, feste
JSON-Ausgabe verlangen. **Wenige hundert Token je Titel → Cent statt Dollar.**

> **Und der eigentliche Gewinn:** *„Die Look-Ahead-Frage ist geloest, weil **du**
> den Zeitstempelfilter anwendest, bevor das Modell etwas sieht."*

**Ein Modell ohne Suchwerkzeug ist dabei kein Nachteil, sondern die Bedingung.**
Die vier vorhandenen Claude-API-Agenten koennen das — **ein zusaetzlicher
Anbieter ist dafuer nicht noetig**.

**Zuschnitt:** ein Aufruf **je Tag ueber alle Ereignistitel**, nicht je
Ereignis. Bei D1 und C1 zusammen typisch 0–10 Titel am Tag.

### V.9 — Was Fable selbst als unsicher benennt

Ob unter dem `fib_score` stetige Groessen liegen (Code unbekannt — davon haengt
ab, ob EW Aktien ueberhaupt einen Primaerschluessel hat) · die Wochenschaetzung
in V.3 · die Basisrate 3–6 % · Preise und Historientiefe der kommerziellen
News-APIs · **alle Klassenschwellen in V.4 und V.5** (drei von vier Vierteln,
80-%-Intervall, 80./95. Perzentil) sind **Konventionen fuer dieses
Datenvolumen, keine abgeleiteten Werte**.

### V.10 — Was sich im Backlog aendert

| Punkt | Neuer Stand |
|---|---|
| **NEU: V1** | **Ereignisrendite je `fib_score`-Stufe** — in einer Stunde machbar, und der Ausgang entscheidet ueber die Einstiegslogik eines laufenden Bots. **Hohe Prioritaet** |
| **NEU: V2** | **Zuteilungskaskade** in allen neun Bots (V.2) — **Voraussetzung fuer die Neuselektion**, nicht danach |
| **U1** Nachrichtenfilter per Modell | **ERSETZT durch V.6 (SEC EDGAR)** — null Kosten, volle Historie, kein Look-Ahead. Der Modellaufruf bleibt nur fuer Krypto und den Live-Fall, und dort **zunaechst nicht bauen** |
| **M3** Mass-Reparatur | **Umfang geklaert (V.3): Kapitalsimulation in die Auswahlschleife reicht.** Vier Wochen. Bedingung 1: `diff` der neun Simulationen. Bedingung 2: **Zuteilungskaskade zuerst** |
| **I3** EW-Pruefkriterium | **Definiert (V.5)** — Timing-Test, 1 000 Ziehungen, Netto-Calmar, 95. Perzentil, Effektgroesse daneben |
| **NEU** | **Raster in Erkennungs- und Handelsparameter trennen** — 25 statt 400 Wellenerkennungen. *Unabhaengig vom Masswechsel richtig*, groesster Laufzeithebel |
| **NEU** | **Beta-Zerlegung** statt einzelnem Alpha: statisches Beta + Timing + Auswahl (V.4) |
| **TB-23** Determinismus | **bestaetigt als operative Definition** von Eigenschaft 4 eines Zuteilungskriteriums |
| **Grok** | Kein eigener Einsatzfall mehr. Guthaben aufbrauchen, Schluessel behalten, **nichts darauf aufbauen**. Falls je noetig: Suche **ausserhalb** des Modells, und die vier Claude-Agenten koennen dasselbe |

### V.11 — In einfacher Sprache (beide Fable-Runden)

**Was wir gemacht haben:** Alle Messergebnisse an einen aussenstehenden
Analysten geschickt — mit der ausdruecklichen Bitte, zu sagen, was er
zuruecknimmt.

**Die wichtigste Antwort, und sie ist ueberraschend:** Weil die Parameter nach
einer **unbrauchbaren** Zahl ausgewaehlt wurden, sind die **berichteten**
Ergebnisse deiner Bots ehrlicher als gedacht. Man kann sich nicht etwas
schoenrechnen, wenn man nach etwas anderem ausgewaehlt hat.

**Der Satz dazu:** „Die Parameter der neun wurden nie optimiert." Sie sind
**einer von vielen**, nicht der beste von vielen.

**Und die Kehrseite:** Sobald das Mass repariert und neu ausgewaehlt wird,
beginnt die Schoenrechnerei — dann erst braucht es die Korrekturverfahren, ueber
die vorher gesprochen wurde.

**Die neue Reihenfolge:** erst das Mass in Ordnung bringen, dann neu auswaehlen,
dann pruefen, wie viel jeder Bot **ueber** das reine Mitlaufen mit dem Markt
hinaus verdient. Diese letzte Zahl entscheidet, welche Bots bleiben.

**Zum Thema Nachrichten-Auswertung:** erledigt. Taegliches Stimmungssignal auf
grossen Aktien traegt nach Handelskosten nichts — „nicht knapp". **Aber** es gab
einen besseren Ersatz: Die amerikanische Boersenaufsicht veroeffentlicht jede
wesentliche Unternehmensmeldung mit amtlichem Zeitstempel, kostenlos und
rueckwirkend. Damit laesst sich dieselbe Frage besser beantworten — ohne Modell,
ohne Kosten, ueber die volle Historie statt zwoelf Monate.

**Was das fuer dich heisst:** Die 340 Dollar sind gespart. Die Reihenfolge der
naechsten Wochen steht. Und der Analyst hat sieben eigene Aussagen
zurueckgenommen — darunter die, die den ganzen Anstoss gegeben hatte.

---

## W — TB-22: Agent 2 Zielfunktion (PR #94, 13.09.2026)

Erledigt die als **sofort** markierte Ausnahme aus **U.6**. Kein Parameter
uebernommen, keine `live_params.py` angefasst, keine Ergebnisdatei
ueberschrieben.

### W.1 — Die Rangfolge entstand an ZWEI Stellen, nicht einer

| | wer entschied | worauf |
|---|---|---|
| **Auswahl** — wer von den getesteten gewinnt | Code: `max(valid_results, key=...robustness_score)` | **Blockmass** |
| **Suchrichtung** — was ueberhaupt getestet wird | **das Modell**, anhand der Tabelle | „auch … Max Drawdown (kleiner = robuster)" — **ohne zu sagen, welcher** |

Seit PR #90 sah das Modell `max_drawdown_chronologisch_pct` bereits in der
Tabelle. **Es stand nur nirgends, was damit anzufangen waere.**

> Beide umzustellen war deshalb kein Kompromiss: *„Nur eine der beiden Stellen
> umzustellen haette Prompt und Mechanik gegeneinander laufen lassen."*

**Agent 2 liest keine abgelegte CSV** — alle sechs Aufrufer reichen eine
Funktion herein, die Zahlen entstehen bei jedem Lauf neu.

### W.2 — Die Groessenordnung, an einem echten Beispiel

Die **Live**-Parameter von `elliott_wave` (dev 10,0 / Stop 6,0 / Fib 0,618)
erreichen:

| Mass | Score |
|---|---:|
| **chronologisch** | **1,624** |
| Blockreihenfolge | 0,245 |

**Faktor 6,6.** Ein Agent, der auf dem zweiten Wert optimiert, sucht in einer
anderen Landschaft.

### W.3 — Wo der neue Score gerechnet wird, und warum dort

**In `shared/param_search_agent.py`**, nicht in `multi_symbol_optimise.py` —
`avg_return_pct × √num_trades ÷ |max_drawdown_chronologisch_pct|`, zeichengleich
zur bestehenden Formel bis auf den Nenner.

> **Begruendung:** Eine zweite Score-Spalte in `multi_symbol_optimise` landete in
> **jeder** `results/*.csv` und waere genau die Einladung, nach ihr zu
> sortieren, die **TB-18 bewusst vermieden** hat.

Der Feldname steht **einmal** (`FELD_SCORE_CHRONO`) und wird von Rechnung,
Prompt und Ausgabe importiert.

### W.4 — Die Zielgroessen-Angabe ist fest verdrahtet

Im Prompt steht jetzt ein Abschnitt **„ZIELGROESSE DER AUSWAHL"** mit dem Satz:
*„wenn beide Masse in verschiedene Richtungen zeigen, gilt das chronologische."*
In der Ausgabe ein fester Satz mit **beiden** Zahlen und dem Hinweis, welche
galt.

> **Nicht vom Modell formuliert** — aus demselben Grund, aus dem der
> Unvalidiert-Pflichthinweis eine Konstante ist: *„Ein Modell koennte sie
> variieren, abschwaechen oder vergessen, ein Konstanten-String nicht."*

### W.5 — Der Schaden war kleiner als befuerchtet

- **Nur drei Bots haben Agent 2** (`elliott_wave`, `elliott_wave_stocks`,
  `t3_supertrend`) — die sechs Prototyp-Bots nicht.
- **Keine abgelegten Vorschlaege im Repo.** `run_agent_search` gibt zurueck,
  `agent_optimise.py` druckt, `quarterly_review.py` verschickt — **keiner
  schreibt eine Datei**. Auf dem Mac koennen welche in `logs/<bot>/`
  (gitignored) und in Telegram-Verlaeufen stehen.
- Was auf dem alten Mass beruht, bleibt **unangetastet**: diese Logs, die acht
  `multi_symbol_optimisation_results.csv` und die Rasterergebnisse unter
  `research/`. **Ab jetzt traegt jeder neue Vorschlag die Zielgroessen-Angabe
  und ist von den aelteren unterscheidbar.**

### W.6 — Unveraendert

Der Agent aendert weiterhin **nichts automatisch**; Vorschlaege bleiben
**unvalidiert** und brauchen Walk-Forward. Der Unvalidiert-Pflichthinweis in
`shared/empfehlung_format.py` unveraendert, mit Testprobe gegen sein
Verschwinden. **Die Rastersuche waehlt weiter auf dem Blockmass** — die
Uebergangsregel gilt fuer Ausgaben und Berichte, Agent 2 war die benannte
Ausnahme, **weil er eine Auswahl trifft**.

### W.7 — Tests

**41/41**, rund 4 Sekunden, **kein einziger echter API-Aufruf** (Sendeweg als
Parameter; zusaetzlich wirft `call_claude` fuer die Dauer jedes Laufs eine
Ausnahme). Darunter **5 Mutationsproben**.

Die Zusicherung wurde ueber **31 erzeugte Datensaetze** nachgewiesen, in denen
die Masse auseinandergehen, plus eine Probe **ganz ohne Formel**: zwei Zeilen
mit gleicher Rendite und gleicher Trade-Zahl, Drawdowns ueber Kreuz — es gewinnt
der kleinere **chronologische** Rueckgang.

Alle bestehenden Tests gegen einen **Basislauf auf `main` (`0f39e3b`)** belegt —
jeder Fehlschlag vorbestehend und rein umgebungsbedingt (`fastapi`, `yfinance`,
Zeitzone `US/Eastern`).

### W.8 — In einfacher Sprache

**Was das Problem war:** Einer deiner vier KI-Agenten schlaegt Parameter vor. Er
tat das anhand der Zahl, die sich als unbrauchbar erwiesen hat — bei drei Bots
sogar **verkehrt herum**. Er haette also systematisch das Schlechtere empfohlen.

**Was ueberraschte:** Die Entscheidung fiel an **zwei** Stellen. Der Code waehlte
den Sieger nach der alten Zahl — und gleichzeitig steuerte das Modell die Suche
anhand einer Tabelle, in der stand „auch der groesste Verlust zaehlt", ohne zu
sagen, **welcher** davon. Nur eine Stelle zu aendern haette beide gegeneinander
laufen lassen.

**Wie gross der Unterschied ist:** Bei den aktuellen Einstellungen eines Bots
ergibt die richtige Rechnung **1,62**, die alte **0,25**. Faktor 6,6 — der Agent
suchte in einer voellig anderen Landschaft.

**Die gute Nachricht:** Nur **drei** der neun Bots nutzen diesen Agenten
ueberhaupt, und er hat nie eine Datei geschrieben. Der Schaden blieb also in
Vorschlaegen stecken, die du gelesen und nicht uebernommen hast.

**Was jetzt anders ist:** Der Agent schreibt in jeden Vorschlag hinein, nach
welcher Zahl er ausgewaehlt hat, und zeigt beide Werte. Dieser Satz ist fest
verdrahtet — ein Modell koennte ihn sonst abschwaechen oder vergessen.

**Was unveraendert bleibt:** Der Agent aendert nach wie vor **nichts**
automatisch. Jeder Vorschlag ist als ungeprueft gekennzeichnet.

---

## X — TB-24: Haltedauern und Zeithorizonte (PR #95, 13.09.2026)

Erledigt **I.3f**. 17 795 ausgefuehrte Positionen, neun Bots, 2016-09-01 bis
2026-09-01.

### X.1 — Die Vermutung trifft auf die Zahl genau zu

**Genau sechs der neun** haben Median-Haltedauern zwischen drei und zehn
Kalendertagen — in einem noch engeren Band als vermutet: **3,9 bis 7,0 Tage**.

| Bot | Rahmen | n | **Median** | Klasse |
|---|---|---:|---:|---|
| `t3_supertrend` | 4 h | 656 | **2,67** | bis 2 Tage |
| `elliott_wave` | 1 h | 130 | **3,90** | **3–10** |
| `rsi2_crypto` | 1 d | 392 | **4,00** | **3–10** |
| `turtle_soup_crypto` | 1 d | 1 414 | **4,00** | **3–10** |
| `rsi2_mean_reversion` | 1 d | 4 232 | **5,00** | **3–10** |
| `volatility_breakout_crypto` | 1 d | 207 | **6,00** | **3–10** |
| `elliott_wave_stocks` | 1 d | 395 | **7,00** | **3–10** |
| `turtle_soup_stocks` | 1 d | 8 915 | **14,00** | 11–30 |
| `volatility_breakout` | 1 d | 1 454 | **21,00** | 11–30 |

> **Das ganze Portfolio spielt innerhalb von drei Wochen. Ueber 30 Tage ist es
> leer.** Zwischen dem ersten und dem siebten Median liegen **4,3 Tage**; bei
> einer Klassengrenze von 2 statt 3 Tagen waeren es **sieben von neun** in einem
> Fenster.

### X.2 — Der Grund ist ein Parameter, keine Markteigenschaft

**Sieben von neun Bots haben eine Zeitbremse** (10 bis 15 Tage bzw.
Handelstage), und **bei jedem liegt der Median seiner Zeitausstiege exakt
darauf**. Acht von neun Verteilungen sind **zweigipflig**, getrennt nach
Ausstiegsart:

| Bot | frueher Gipfel (Stop) | Anteil | spaeterer Gipfel (Zeitbremse) | Anteil |
|---|---:|---:|---:|---:|
| `elliott_wave` | 0,88 T | 53,8 % | 10,0 T | 33,8 % |
| `turtle_soup_crypto` | 2,00 T | 69,0 % | 10,0 T | 31,0 % |
| `volatility_breakout_crypto` | 3,00 T | 71,0 % | 15,0 T | 29,0 % |
| `elliott_wave_stocks` | 5,00 T | 79,2 % | **131,0 T** | 20,8 % |
| `turtle_soup_stocks` | *kein Stop* | — | 14,0 T | **100,0 %** |
| `volatility_breakout` | 12,00 T | 19,8 % | 22,0 T | **80,2 %** |

> **„Der Median eines Bots ist im Wesentlichen die Antwort auf eine Frage: *wie
> oft feuert der Stop, bevor die Uhr ablaeuft?*"**

### X.3 — ⚠️ Der eigentliche Befund: der Horizont erklaert nichts

Gemessen als gemeinsame Einstiege im selben Titel binnen drei Tagen, gegen den
Zufallswert (200 Ziehungen **und** geschlossene Form — beide stimmen in allen
32 Paaren auf 0,1 Prozentpunkte ueberein):

| | Median-Ueberschuss gegen Zufall |
|---|---:|
| **gleiche Ertragsquelle** (6 Paare) | **1,94 ×** |
| verschiedene Ertragsquelle (26 Paare) | 0,32 × |
| **gleiche Horizont-Klasse** (16 Paare) | **0,32 ×** |
| verschiedene Horizont-Klasse (16 Paare) | 1,10 × |

**Gleiche Horizont-Klasse zeigt sogar WENIGER gemeinsame Einstiege als
verschiedene.** Alle sechs Paare gleicher Quelle liegen ueber **1,68 ×**, alle
zwoelf Trend-Umkehr-Paare unter **0,95 ×**.

Nach Quellen-Paar:

| Paar | Median-Ueberschuss |
|---|---:|
| Umkehr + Umkehr | **2,58 ×** |
| Trend + Trend | **1,71 ×** |
| Muster + Umkehr | 1,43 × |
| Trend + Umkehr | **0,32 ×** |
| Muster + Trend | **0,18 ×** |

> **Fables Einordnung — Horizont als *zweite* Dimension — ist damit bestaetigt,
> aber schwaecher als gedacht: Bei diesem Portfolio ist sie gar keine
> Dimension.** Was gemeinsames Verhalten erklaert, ist die Ertragsquelle.

### X.4 — Der Einzelfall, der die Messmethode in Frage stellt

`elliott_wave_stocks` und `rsi2_mean_reversion` steigen in **0 von 395** Faellen
binnen drei Tagen gemeinsam ein — obwohl sie **127 Titel** teilen und der Zufall
etwa **20** Treffer erwarten liesse.

**Der Grund ist ein systematischer Versatz:** Der naechstgelegene
RSI-2-Einstieg liegt im Median **14 Tage vor** dem Elliott-Einstieg, und die
Klassen von **−3 bis +3 Tagen sind leer**.

| Versatz (Tage) | < −30 | −30…−20 | −20…−10 | −10…−3 | **−3…+3** | +3…+10 | +10…+20 | +20…+30 | ≥ +30 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Anzahl (von 395) | 213 | 21 | 36 | 15 | **0** | 1 | 3 | 7 | 99 |

> **Sie handeln denselben Kursrueckgang — nur nacheinander.** Ein
> Drei-Tage-Fenster allein haette das Paar als **unabhaengig** eingeordnet.
> **Gleichzeitig ist nicht dasselbe wie abhaengig** — und Unabhaengigkeit im
> engen Fenster ist kein Beleg fuer Unabhaengigkeit.

### X.5 — Die Titel-Ueberlappung

**Tages-Ueberlappung:** Median ueber alle 72 geordneten Paare **89,5 %**; die
Spalte `turtle_soup_stocks` durchgehend **100 %** (haelt an allen 3 653 Tagen).
*Die Zahl misst vor allem, wie oft ein Bot im Markt ist — Nenner, kein Befund.*

**Titel-Ueberlappung**, staerkste Paare:

| A → B | Anteil |
|---|---:|
| `rsi2_mean_reversion` → `turtle_soup_stocks` | **48,6 %** |
| `rsi2_crypto` → `turtle_soup_crypto` | 39,3 % |
| `elliott_wave` → `turtle_soup_crypto` | 25,5 % |
| `elliott_wave_stocks` → `turtle_soup_stocks` | 24,9 % |

### X.6 — Die Luecke

- **Ueber 30 Tage ist das Portfolio leer** — kein Median ueber 21 Tagen.
- **B1 / ETF-Trend (monatlich)** laege ausserhalb aller neun Mediane — eine
  **echte Horizontergaenzung**, zusaetzlich zur Quellenergaenzung. *Stuetzt
  Fables Rang 4.*
- **K1 (Wochenfrist) ist zweideutig:** Heisst es *Haltedauer* eine Woche, landet
  es **mitten im gedraengten Fenster** und ist keine Horizontergaenzung; heisst
  es *woechentlicher Entscheidungstakt* mit mehrwoechiger Haltedauer, liegt es
  bei `turtle_soup_stocks`/`volatility_breakout`. **Aus dem Repo nicht zu
  klaeren** — der Strategie-Katalog liegt nicht dort.

### X.7 — Belastbarkeit

| | |
|---|---|
| Quelle | Backtest-Trades ueber die **Original-Bot-Funktionen** und die heutigen `live_params.py` |
| Pflicht-Gegencheck | Fuer **alle neun** Bots stimmt der Positionssatz **Zeile fuer Zeile** mit `research/exposure_messung/daten/` ueberein |
| Gegenprobe Positionslimit | Median ueber **alle** Trades statt nur der ausgefuehrten: Abweichung **0,00 Tage** bei acht Bots, 0,25 bei `t3_supertrend` — **keine Klassenzuordnung aendert sich** |
| Live-Seite | **nicht gemessen** — die neun `paper_trading_*.db` sind gitignored; ausserdem erreicht kein Bot `MIN_LIVE_CLOSED_TRADES = 10`. `live_haltedauern.py` liegt lauffaehig bereit |
| Selbsttests | **51/51** — 35 Gegenproben, 5 zum Live-Weg gegen eine gebaute Datenbank, **10 Mutationsproben**, 1 Repo-Wache |

### X.8 — In einfacher Sprache

**Was wir wissen wollten:** Handeln deine neun Bots ueber verschiedene
Zeitraeume — oder machen sie alle ungefaehr dasselbe, nur mit anderen Namen?

**Was herauskam:** Sie machen ungefaehr dasselbe. Sechs von neun halten ihre
Positionen im Schnitt **vier bis sieben Tage**. Laenger als drei Wochen haelt
keiner.

**Warum das so ist:** Nicht weil der Markt es so will, sondern weil du es so
eingestellt hast. Sieben Bots haben eine eingebaute Uhr, die nach 10 bis 15
Tagen schliesst. Fast alle Trades enden entweder am Stop-Loss oder an dieser
Uhr.

**Die wichtigere Erkenntnis:** Der Zeitraum ist gar nicht das Entscheidende.
Zwei Bots verhalten sich dann aehnlich, wenn sie **dieselbe Marktbewegung
ausnutzen** — nicht, wenn sie gleich lange halten. Gemessen: Bots mit derselben
Strategie-Idee kaufen doppelt so oft gleichzeitig wie der Zufall. Bots mit
gleicher Haltedauer dagegen **seltener** als der Zufall.

**Und ein Detail, das nachdenklich macht:** Zwei deiner Bots kaufen **nie**
gleichzeitig — aber nur, weil der eine im Schnitt zwei Wochen frueher dran ist.
Sie reagieren auf denselben Kursrutsch, nur nacheinander. Wer nur auf
„gleichzeitig" schaut, haelt sie fuer unabhaengig. Sie sind es nicht.

**Was das fuer dich heisst:** Ein zehnter Bot mit anderer Haltedauer bringt
wenig. Einer mit einer anderen Ertragsquelle bringt etwas. Und die
ETF-Trendfolge, die monatlich handelt, waere in beidem neu.

---

---

## Y — TB-23: Determinismus (PR #96, 13.09.2026)

**Messung, keine Korrektur.** 20 Permutationen der Symbolreihenfolge, sonst
alles identisch — dieselben Kursdaten, dieselben Parameter, derselbe Code.

### Y.1 — Acht von neun Bots sind nicht deterministisch

| Bot | Urteil | umstrittene Trades | Rendite-Spanne | Drawdown-Spanne |
|---|---|---:|---|---|
| `elliott_wave` | **nur Reihenfolge** | **0,0 %** | 67,77 .. 67,77 % | −10,17 .. −10,17 % |
| `volatility_breakout_crypto` | nicht det. | 11,6 % | 46,29 .. 73,45 % | −16,29 .. −16,29 % |
| `rsi2_crypto` | nicht det. | 14,4 % | 25,58 .. 34,07 % | −13,96 .. −12,66 % |
| `t3_supertrend` | nicht det. | 14,6 % | 117,87 .. 138,12 % | −22,57 .. −22,14 % |
| `rsi2_mean_reversion` | nicht det. | 27,1 % | 27,90 .. 45,62 % | −22,15 .. −18,93 % |
| `elliott_wave_stocks` | nicht det. | 28,2 % | 321,80 .. 424,42 % | −23,22 .. −22,19 % |
| `turtle_soup_crypto` | nicht det. | 30,6 % | 123,77 .. 190,23 % | −41,24 .. −32,40 % |
| `turtle_soup_stocks` | nicht det. | 36,4 % | 121,84 .. 164,68 % | −30,58 .. −28,45 % |
| `volatility_breakout` | nicht det. | **46,6 %** | **145,16 .. 269,47 %** | −25,64 .. −22,89 % |

*„Umstritten" = Trades, die nur in einem Teil der Permutationen ausgefuehrt
werden — weder immer noch nie. Dieselbe Definition wie in
`research/order_sensitivity/`.*

**`elliott_wave` ist der einzige Sonderfall:** alle 130 Trades in jeder
Permutation, Endkapital und Drawdown **auf den Cent identisch**. Nur die
**Zeilenreihenfolge** seiner `equity_curve.csv` unterscheidet sich — wirtschaftlich
folgenlos, aber relevant, weil `shared/ergebniskurven.py` diese Datei Zeile fuer
Zeile vergleicht.

### Y.2 — Drei Zahlen, die die Sache greifbar machen

| | |
|---|---|
| **`volatility_breakout`: 145 % bis 269 % Rendite.** | Die abgelegte Kurve nennt **224,41 %** — eine von zwanzig. Welche dort steht, entscheidet allein die Sortierung von `config/sp500_top150.txt` |
| **`volatility_breakout_crypto`: Drawdown in allen 20 Permutationen exakt −16,29 %, exakt 207 Trades — Rendite 46,3 bis 73,5 %.** | ⚠️ *„Wer nur Kennzahlen vergleicht, sieht hier nichts."* Deshalb ist das Leitkriterium die **Menge der ausgefuehrten Trades**, nicht die Kennzahl |
| **`turtle_soup_stocks` hat gar kein Positionslimit — und ist mit 36,4 % zweitschlimmster Fall.** | Dort bindet die **Kapitalschranke**: bei 2 % Allokation hoechstens 50 Positionen finanzierbar; gemessen 50–51 offen, **ueber 3 100 Trades abgelehnt** |

### Y.3 — Die Ursache sitzt an EINER Stelle

> **Die Zuteilung in `simulate_portfolio()`.** Wird ein Platz knapp
> (Positionslimit **oder** freies Kapital), entscheidet die Zeilenreihenfolge
> des Trade-DataFrames, wer ihn bekommt — und die ist die **Symbolreihenfolge**.
> **Es gibt kein benanntes Zweitkriterium.**

Die fehlende stabile Sortierung (`combined.sort_values("entry_time")` ohne
`kind="stable"`, in **allen neun** Bots) kommt hinzu, **ist aber nicht die
Wurzel**: Auch eine stabile Sortierung erhielte die Eingabereihenfolge — also
die Symbolreihenfolge.

**Nicht die Ursache ist die Signalerzeugung:** Bei allen neun Bots ist die Menge
der **erzeugten** Trades ueber alle zwanzig Permutationen **bitidentisch**.
`get_trades_for_symbol()` laeuft je Symbol unabhaengig.

> **Der Fehler ist an einer Stelle behebbar, nicht in neun Strategien
> verstreut.**

**Wo es eng wird:**

| bindend ist … | Bots |
|---|---|
| das **Positionslimit** (20/20 Laeufe erreicht) | `elliott_wave_stocks`, `rsi2_crypto`, `rsi2_mean_reversion`, `t3_supertrend`, `turtle_soup_crypto`, `volatility_breakout_crypto` |
| die **Kapitalschranke** | `turtle_soup_stocks` (kein Limit), `volatility_breakout` (Limit 15, aber nur 10 finanzierbar) |
| **nichts** | `elliott_wave` (0 abgelehnte Trades) |

### Y.4 — Die offene Frage — und warum sie schon beantwortet ist

**Gemessen:** Eine Zuteilung nach Signalstaerke reicht **nicht**.

- Bei `elliott_wave_stocks` teilen **300 von 510** Trades ihren
  Einstiegszeitpunkt mit mindestens einem anderen; groesste Gruppe **20 Titel**.
  Nach einer Rangregel auf dem `fib_score` bleiben **144 Trades (48,0 % der
  gleichzeitigen) weiterhin gleichauf**.
- **Sieben der neun Bots fuehren ueberhaupt kein Mass fuer Signalstaerke mit.**
  Eines einzufuehren waere eine **Strategieaenderung**, keine Rangregel.
- Das TB-20-Zweitkriterium (`end_time`) hilft nicht: Es entscheidet zwischen
  Wellenmustern **eines** Symbols; bei der Zuteilung konkurrieren
  **verschiedene** Symbole zum **selben** Balken.

> ✅ **Die Antwort liegt bereits vor — in V.2, zwei Stunden vorher formuliert.**
> Fables Kaskade hat den Primaerschluessel ausdruecklich als *„falls vorhanden"*
> markiert. Fehlt er, beginnt sie beim **Diversifikationsbeitrag**
> (60-Tage-Korrelation mit dem aktuellen Buch, niedriger zuerst), dann
> **Liquiditaet**, dann **protokollierter Zufall**.
>
> *„Das ist dann kein Mangel der Regel, sondern eine ehrliche Aussage ueber den
> Bot: Er hat keine Signalstaerke, nur ein Signal."*

### Y.5 — Das Werkzeug

```
python3 shared/determinismus.py --schnell            # alle 9 Bots, 101 s, Rueckgabewert 1 bei Befund
python3 shared/determinismus.py --voll --perms 20    # die Bestandsaufnahme, ~13 min
python3 shared/test_determinismus.py                 # 49 Selbsttests, ~40 s
```

- Symboldateien werden **nur gelesen**; permutiert wird im Speicher.
- `RESULTS_DIR` zeigt waehrend jedes Laufs in einen temporaeren Ordner — **das
  Werkzeug kann `results/<bot>/equity_curve.csv` gar nicht ueberschreiben**.
  Danach weiterhin **9× AKTUELL**.
- **Pflicht-Gegencheck bestanden:** Lauf 0 (Originalreihenfolge) trifft bei
  **9 von 9** Bots die abgelegte `equity_curve.csv` exakt.
- **Gegenprobe bestanden:** Eine gehaertete Kopie wird als *deterministisch*
  gemeldet; dieselbe Kopie plus **genau einem** eingebauten Fehler wieder als
  Befund.
- **Falsche Entwarnung ausgeschlossen:** Eine Kopie, die die Permutation
  **ignoriert**, wird als `UNKLAR` gemeldet — nicht als `DETERMINISTISCH`.

### Y.6 — Vier Folgepunkte

| # | Punkt |
|---|---|
| **Y1** | **Die Zuteilungsregel** — Kaskade aus V.2 einbauen. **Voraussetzung fuer jede Neuselektion** |
| **Y2** | Die **19 weiteren** `sort_values`-Aufrufe ohne `kind="stable"` (aus TB-19) |
| **Y3** | ⚠️ **`volatility_breakout`: `MAX_CONCURRENT_POSITIONS = 15` bei rechnerisch hoechstens 10 finanzierbaren Positionen — das Limit greift nie.** Ein toter Parameter |
| **Y4** | `shared/determinismus.py --schnell` als naechtlicher Cronjob *(haengt an A1/A2, Crontab)* |

### Y.7 — In einfacher Sprache

**Was wir wissen wollten:** Wenn man die Reihenfolge der Symbole in einer
Textdatei umsortiert — aendert sich dann das Ergebnis eines Backtests?

**Was herauskam:** Bei **acht von neun** Bots ja, und zwar erheblich. Ein Bot
liefert je nach Sortierung zwischen **145 % und 269 %** Rendite.

**Warum:** Wenn nicht genug Platz oder Geld fuer alle Signale da ist, bekommt den
Platz einfach der, der zufaellig weiter oben in der Datei steht. **Es gibt keine
Regel, wer Vorrang hat.**

**Was das fuer die Zahlen bedeutet:** Sie sind nicht falsch — sie sind **eine
von vielen moeglichen**. Die gespeicherte Zahl ist ein Los aus einem breiten
Topf.

**Die gute Nachricht:** Es liegt an **genau einer Stelle** im Code, nicht an den
Strategien selbst. Die Signale, die die Bots finden, sind immer dieselben.

**Was als Naechstes kommt:** Eine Regel, wer bei Platzmangel Vorrang hat. Die
Antwort dafuer liegt schon vor — und sie funktioniert auch bei den sieben Bots,
die gar keine Signalstaerke messen.

---

## Z — TB-25: Fib-Score-Stufen (PR #97, 13.09.2026)

Beantwortet **V1**. Untersuchung, keine Aenderung.

### Z.1 — Ausgang 2, bei BEIDEN Bots: der Score traegt nichts

> *„Dann bleibt vom Elliott-Wave-Bot ein Zigzag-Detektor mit Stop."*

Die Punktwerte steigen monoton — **kein einziger Schritt** ist von null zu
unterscheiden, und der **bestbelegte** Schritt ist exakt null:

| Schritt | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Stufe 1 gegen 0 | +3,83 pp, CI [−0,04; +7,91], p = 0,059 | +0,99 pp, CI [−1,90; +4,06], p = 0,54 |
| **Stufe 2 gegen 1** | **+0,12 pp**, p = 0,97 | **+0,21 pp**, p = 0,92 |
| Stufe 3 gegen 2 | +6,40 pp, CI [−7,79; +20,77], p = 0,36 | +3,72 pp, p = 0,44 |

**Stufe 3 traegt keine Aussage** (5 bzw. 20 Trades). **Eine Anhebung der
Schwelle auf ≥ 2 ist von den Daten nicht gestuetzt.**

> **Der Median ist in sieben von acht Gruppen exakt der Stop.** Was sich
> zwischen den Stufen bewegt, ist **nicht der typische Trade, sondern der Rand
> der Verteilung.**

### Z.2 — ⚠️ Der eigentliche Befund: die drei Bedingungen sind nicht gleichwertig

| Bedingung | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| **Welle 4 / Welle 3** ∈ [0,236; 0,382] | **+4,88 pp**, CI [+0,85; +9,13], **p = 0,012** | +1,82 pp, p = 0,22 |
| Welle 2 / Welle 1 ∈ [0,5; 0,618] | +3,53 pp, p = 0,10 | +1,68 pp, p = 0,33 |
| **Welle 3 / Welle 1** ∈ [1,4; 1,8] | **−0,24 pp**, p = 0,91 | **−0,79 pp**, p = 0,63 |

> **Dieselbe Reihenfolge bei beiden Bots — Welle 4 > Welle 2 > Welle 3 — und
> die Welle-3-Bedingung liegt bei beiden UNTER NULL.**

**Der auffaellige Krypto-Schwellenbefund loest sich damit auf:** Stufe ≥ 1 gegen
Stufe 0 ergab dort +4,12 pp (p = 0,028) — *ein auffaelliger Vergleich unter 22,
rein zufaellig waere gut einer zu erwarten* — und er stammt **fast vollstaendig
aus der Welle-4-Bedingung allein**, nicht aus dem Zaehlen.

*Vorbehalt:* Beim Aktien-Bot ist **keine** der drei Bedingungen von null zu
unterscheiden, und das Cluster-Intervall des Krypto-Welle-4-Befundes beruehrt die
Null ([−0,05; +9,80]).

### Z.3 — Das Rundungsartefakt: bestaetigt, und schlimmer als gedacht

**Kein Renditeunterschied** zwischen 0,33 und 0,34 (p = 0,87 bzw. 0,34) — wie
erwartet.

**Aber:** Die 0,34 wird **ausschliesslich** von der **Welle-2**-Bedingung
getragen (exhaustiv geprueft; dasselbe fuer 0,67). Der Tie-Break ist damit
**deterministisch, nicht zufaellig** — und die 0,33-Gruppe ist eine Mischung aus
der **schlechtesten und der besten** Einzelbedingung:

| Stufe-1-Untergruppe | Score | Krypto | Aktien |
|---|---:|---|---|
| nur Welle 2 | **0,34** | n = 27, 4,30 % | n = 75, 6,79 % |
| nur Welle 3 | 0,33 | n = 23, **−0,06 %** | n = 94, **1,94 %** |
| nur Welle 4 | 0,33 | n = 33, **6,34 %** | n = 194, **5,03 %** |

> *„Ein Tie-Break, den niemand gewaehlt hat — und der, wenn ueberhaupt, in die
> falsche Richtung zeigt."*

### Z.4 — Die Nebenfrage, und was sie fuer TB-26 bedeutet

**Ja, es gibt eine stetige Groesse unter dem Score.** Alle drei Bedingungen
pruefen ein Wellenlaengen-**Verhaeltnis** gegen ein Intervall — allerdings
**Intervalle, keine Toleranzen um ein Ziel**: Die kanonischen Fibonacci-Werte
liegen bei Welle 2 (0,618) und Welle 4 (0,382) auf dem **oberen Rand**, bei
Welle 3 (1,618) unsymmetrisch im Inneren.

**Gemessen traegt sie nicht mehr als die Stufe:**

| Groesse | `elliott_wave` | `elliott_wave_stocks` |
|---|---|---|
| Stufe (0–3) | ρ = +0,164, p = 0,014 | ρ = +0,039, p = 0,27 |
| stetige Naehe | ρ = +0,109, p = 0,10 | ρ = +0,038, p = 0,28 |
| stetige Naehe, weiche Fassung | ρ = +0,130, p = 0,052 | ρ = +0,054, p = 0,12 |

**Als Primaerschluessel taugt sie — als Auswahlkriterium nicht:**

| | `elliott_wave` | `elliott_wave_stocks` |
|---|---:|---:|
| Gleichstaende je Symbol, `fib_score` | 85,8 % | 73,6 % |
| dasselbe, weiche stetige Naehe | **0,0 %** | **0,0 %** |

> **„Eindeutigkeit ohne Trennschaerfe ersetzt einen willkuerlichen Tie-Break
> durch einen sauberer aussehenden, nicht durch einen begruendeten."**

✅ **Das bestaetigt die Vorgabe in TB-26: kein Primaerschluessel fuer Elliott
Wave.** Die Kaskade beginnt dort beim Diversifikationsbeitrag.

### Z.5 — Was folgt, und was nicht

| Frage | Antwort |
|---|---|
| Filtert `min_fib_score = 0.3` etwas? | **Aktien: nein** (+1,19 pp, CI [−1,45; +3,93]). **Krypto: ja, aber aus dem falschen Grund** — der Effekt ist die Welle-4-Bedingung, nicht die Anzahl |
| Schwelle auf ≥ 2 anheben? | **Von den Daten nicht gestuetzt** (Schritt 1 → 2: +0,12 bzw. +0,21 pp) |
| Ist die Rangfolge nach `fib_score` begruendet? | **Nein.** Praktisch folgt daraus heute nichts — TB-20 hat gemessen, dass sie in **0 von 20 114** Laeufen eine Auswahl traf |
| Gibt es einen stetigen Primaerschluessel? | **Ja, eindeutig — aber ohne gemessene Trennschaerfe** |

**Fuenf offene Punkte, benannt und nicht ausgefuehrt:**

| # | Punkt |
|---|---|
| **Z1** | **Die Welle-4-Bedingung getrennt untersuchen** — die einzige, die ueber beide Bots in dieselbe Richtung zeigt. Als Ja/Nein-Filter statt als Drittel eines Scores waere eine **Strategieaenderung** und braeuchte den vollen Validierungsweg: Backtest → Walk-Forward → Equity-Simulation → Buy-and-Hold |
| **Z2** | **Die Welle-3-Bedingung ist ein Streichkandidat** — bei beiden Bots leicht negativ. Ebenfalls Strategieaenderung |
| **Z3** | **Die Schwelle `min_fib_score = 0.3`** filtert beim Aktien-Bot **nichts** (+1,19 pp, CI [−1,45; +3,93]) und wirft dabei **303 von 813** Mustern weg |
| **Z4** | **Die Frage unter der Frage: traegt der Zigzag-Detektor etwas?** Fuer `elliott_wave_stocks` liegt genau dieser Massstab bereits vor — der Zufalls-Timing-Test aus **I3** / **V.5** |
| **Z5** | ⚠️ **`docs/UEBERSICHT_RESEARCH.md` ist veraltet** (Stand 12.09.2026) und kennt weder TB-25 noch die uebrigen seither hinzugekommenen `research/`-Ordner. **Wer sie aktualisiert, sollte es fuer alle tun** — inzwischen mindestens `fib_score_stufen`, `tb24_haltedauern`, `tb27_kapitalsimulation`, `versuchsregister`, `drawdown_reihenfolge`, `exposure_messung` |

### Z.5b — Belastbarkeit und die Grenze, die dazugehoert

| | |
|---|---|
| Datengrundlage | **225 Muster** (Krypto, 18 Symbole, 2021-09 bis 2026-08) · **813 Muster** (Aktien, 147 Symbole, 2016-08 bis 2026-09) |
| Bot-Funktionen | **aufgerufen, nicht nachgebaut** — Zigzag, kausale Wellenauswahl, Trade-Simulation aus unveraendertem Bot-Code |
| Nachbildung geprueft | nur die **Zerlegung** des Scores — 0 Abweichungen auf allen 1 038 Mustern und 40 000 Zufallspunkten |
| Uebereinstimmung mit `elliott_wave_params` | 130 bzw. 510 Trades oberhalb der Schwelle — **dieselben Zahlen** |
| **Stufe 0 sauber danebengestellt** | Lauf mit `min_fib_score = 0.0`; Stufen 1–3 **Zeile fuer Zeile identisch** zum Bot-Lauf |
| Look-Ahead | korrigierter Pfad (PR #26), mechanisch nachgewiesen |
| Selbsttests | 29/29 je Bot · `ergebniskurven.py` 9× AKTUELL vor und nach dem Lauf |

> ⚠️ **Die Grenze, die dazugehoert:** Ein Unterschied von **1–2 Prozentpunkten
> waere bei diesen Stichproben gar nicht auffindbar gewesen** — noetig waeren
> ~740 (Krypto) bzw. ~1 560 (Aktien) Trades **je Gruppe**. „Kein Unterschied"
> heisst hier: **keiner ab rund 5 Prozentpunkten.**
>
> **Fuer den Schritt Stufe 1 → 2 ist das trotzdem aussagekraeftig**, weil der
> Punktwert dort bei **+0,12** bzw. **+0,21 pp** liegt — also weit unterhalb
> dessen, was die Stichprobe verdecken koennte.

### Z.5c — Die Reichweite des Rundungsartefakts

> **Ein Konstruktionsfehler ohne gemessene Wirkung.** TB-20 hat belegt, dass die
> Rangfolge innerhalb eines Symbols heute **keinen einzigen Live-Trade
> verschiebt** (0 von 20 114 nachgebildeten Laeufen). Er wuerde erst wirken,
> **wenn je eine Zuteilungsregel ueber Symbole hinweg auf `fib_score` rankt**.

✅ **Und genau das tut die Kaskade aus TB-26 nicht** — bei beiden Elliott-Bots
beginnt sie beim Diversifikationsbeitrag, weil der `fib_score` die
Aufloesungsbedingung nicht erfuellt. Der Fehler bleibt damit **wirkungslos**,
solange diese Entscheidung steht.

### Z.6 — In einfacher Sprache

**Was wir wissen wollten:** Elliott Wave prueft drei Bedingungen an einem
Kursmuster und zaehlt, wie viele erfuellt sind. Sind Muster mit mehr erfuellten
Bedingungen tatsaechlich besser?

**Was herauskam:** Nein. Ein Muster mit zwei erfuellten Bedingungen verdient
praktisch genau so viel wie eines mit einer. **Die Zaehlung sagt nichts.**

**Aber die einzelnen Bedingungen sind nicht gleich:** Eine davon — das
Verhaeltnis von Welle 4 zu Welle 3 — traegt tatsaechlich etwas. Eine andere, das
Verhaeltnis von Welle 3 zu Welle 1, ist bei **beiden** Bots sogar leicht
**schaedlich**. Sie werden nur zusammengezaehlt, also hebt sich das gegenseitig
auf.

**Was das heisst:** Von der Wellenzaehlung bleibt nicht viel. Der Bot erkennt
Kursbewegungen und setzt einen Stop-Loss — das funktioniert. Die aufwendige
Fibonacci-Bewertung darueber traegt nach dieser Messung nichts bei.

**Was das nicht heisst:** Dass der Bot schlecht ist. Nur dass sein wirksamer
Teil ein **anderer** ist als der, den er dem Namen nach hat.

---

## AA — TB-26: Zuteilungskaskade (PR #99, 13.09.2026)

Behebt den Befund aus **TB-23**. Zusammen mit PR #98 (TB-25-Nachtrag:
Bereichspruefung gegen die Merge-Basis statt gegen die Spitze).

### AA.1 — Die Zusicherung: neun von neun deterministisch

`python3 shared/determinismus.py --voll --perms 20` → **Rueckgabewert 0**,
781 s (vorher 616 s).

| Bot | vorher | umstrittene Trades | nachher |
|---|---|---:|---|
| `elliott_wave` | NUR REIHENFOLGE | 0,0 % | **DETERMINISTISCH** |
| `volatility_breakout_crypto` | nicht det. | 11,6 % → **0,0 %** | **DETERMINISTISCH** |
| `rsi2_crypto` | nicht det. | 14,4 % → **0,0 %** | **DETERMINISTISCH** |
| `t3_supertrend` | nicht det. | 14,6 % → **0,0 %** | **DETERMINISTISCH** |
| `rsi2_mean_reversion` | nicht det. | 27,1 % → **0,0 %** | **DETERMINISTISCH** |
| `elliott_wave_stocks` | nicht det. | 28,2 % → **0,0 %** | **DETERMINISTISCH** |
| `turtle_soup_crypto` | nicht det. | 30,6 % → **0,0 %** | **DETERMINISTISCH** |
| `turtle_soup_stocks` | nicht det. | 36,4 % → **0,0 %** | **DETERMINISTISCH** |
| `volatility_breakout` | nicht det. | 46,6 % → **0,0 %** | **DETERMINISTISCH** |

Alle drei Vergleichsebenen — **Signalmenge, ausgefuehrte Trades,
Kapitalpfad** — ueber alle 20 Permutationen identisch. **Die Menge der
erzeugten Trades ist bei allen neun unveraendert** — keine Strategieaenderung.

### AA.2 — Die neuen Zahlen, und wo sie in der alten Spanne liegen

| Bot | Spanne vorher | bisher abgelegt | **nachher** | Lage |
|---|---|---:|---:|---:|
| `elliott_wave` | 67,77 (ein Wert) | 67,77 % | **67,77 %** | unveraendert |
| `elliott_wave_stocks` | 321,80 … 424,42 | 352,72 % | **419,07 %** | 95 % |
| `rsi2_crypto` | 25,58 … 34,07 | 28,37 % | **27,19 %** | 19 % |
| `rsi2_mean_reversion` | 27,90 … 45,62 | 36,75 % | **36,28 %** | 47 % |
| `t3_supertrend` | 117,87 … 138,12 | 129,64 % | **121,70 %** | 19 % |
| `turtle_soup_crypto` | 123,77 … 190,23 | 177,59 % | **152,84 %** | 44 % |
| `turtle_soup_stocks` | 121,84 … 164,68 | 145,59 % | **138,15 %** | 38 % |
| `volatility_breakout` | 145,16 … 269,47 | 224,41 % | **209,59 %** | 52 % |
| `volatility_breakout_crypto` | 46,29 … 73,45 | 49,03 % | **68,13 %** | 80 % |

**Alle neun liegen innerhalb der gemessenen Spanne**, Median der Lagen **44 %**
— die Kaskade landet nicht systematisch am oberen Rand.

> ⚠️ **Eine Ausnahme, ehrlich benannt:** Der Drawdown von
> `volatility_breakout` liegt mit **−22,46 %** *flacher als in jeder* der
> zwanzig Permutationen (beste vorher −22,89 %). Das ist die erwartete Wirkung
> von Stufe 2 — weniger Klumpen, flacherer Drawdown —, aber **20 Permutationen
> sind eine Stichprobe, keine Randverteilung**. Dass die Kaskade den Drawdown
> *systematisch* senkt, ist **nicht gezeigt**; bei drei anderen Bots liegt der
> neue Drawdown in der schlechteren Haelfte.

> **Keine dieser Zahlen ist eine Verbesserung der Strategie.** Vorher gab es
> keine einzelne richtige Zahl, sondern eine Spanne, von der die
> Dateisortierung eine auswaehlte. **Jetzt gibt es eine, und sie hat einen
> benannten Grund.**

### AA.3 — Die Regel, an EINER Stelle: `shared/zuteilung.py`

| Rang | Kriterium | Richtung |
|---:|---|---|
| 1 | strategieeigene stetige **Signalstaerke**, falls vorhanden | staerker zuerst |
| 2 | **Diversifikationsbeitrag** — 60-Tage-Korrelation mit dem allokationsgewichteten Buch | niedriger zuerst; entfaellt bei leerem Buch |
| 3 | **Liquiditaet** — Median Dollar-Volumen 20 Tage | hoeher zuerst |
| 4 | **seeded Zufall**, `SEED = 20260913` | — |

**Fehlende Angaben bekommen den Median der Kandidaten** — nicht das Ende
(benachteiligte junge Symbole) und nicht die 0 (bevorzugte sie).

**Dieselbe Regel legt jetzt auch die Reihenfolge gleichzeitiger Ausstiege
fest.** Sie entscheidet ueber niemandes Platz, aber ueber die Zwischenstaende
der Kapitalkurve und damit ueber den gemessenen Drawdown; vorher galt auch dort
die Dateireihenfolge. *Das erledigt zugleich den Sonderfall `NUR REIHENFOLGE`
bei `elliott_wave`.*

### AA.4 — Abweichung vom Auftrag, ehrlich benannt

Mein Auftrag nahm an, **sieben** Bots fuehrten keine Signalstaerke. Tatsaechlich:

| | Bots |
|---|---|
| **mit brauchbarem Primaerschluessel** | `rsi2_crypto` (`rsi_at_entry`, 330 Werte, **0,0 %** Gleichstaende) · `rsi2_mean_reversion` (442 Werte, **2,1 %** — knapp ueber der 2-%-Marke, **Ermessensentscheidung**) |
| mit untauglichem Kandidaten | `elliott_wave` (`fib_score`, 5 Werte, 38,6 % gleichauf) · `elliott_wave_stocks` (72,7 % gleichauf) |
| ohne | `turtle_soup_crypto`/`_stocks` (`setup_day_low` ist ein **Kursniveau**, keine Signalstaerke, und nicht skalenfrei) · `t3_supertrend` · `volatility_breakout` · `volatility_breakout_crypto` |

> **Der RSI(2) ist keine neue Groesse** — `backtest_rsi2.py` schreibt ihn seit
> jeher mit, er **ist** die Signalstaerke dieser Strategie (tiefer =
> ueberverkaufter = staerker), und die Richtung kommt aus der Strategielogik,
> nicht aus dem Backtest-Ergebnis. **Umkehrbar in einer Zeile:**
> `SIGNALSPALTE = None`.

✅ Die Elliott-Wave-Einordnung deckt sich mit **TB-25 (Block Z)**: kein
Primaerschluessel, die Kaskade beginnt dort bei Stufe 2.

### AA.5 — Wie oft welche Stufe entscheidet

| Stufe | Faelle | Anteil |
|---|---:|---:|
| 1 Signalstaerke | 744 | 20,1 % |
| **2 Diversifikation** | **2 932** | **79,2 %** |
| 3 Liquiditaet | 22 | 0,6 % |
| **4 Zufall** | **6** | **0,16 %** |
| **Summe** | **3 704** | |

> **Der Zufall entscheidet sechsmal.** Das ist die Antwort auf den
> naheliegenden Einwand, eine Regel mit Zufall auf der letzten Stufe sei „doch
> auch nur willkuerlich": **Sie ist es an 0,16 % der Entscheidungen — und dort
> sichtbar und protokolliert.**

**Die Zahl der umstrittenen Zuteilungen ist viel kleiner als die der
gleichzeitigen Trades** (3 704 gegen zehntausende): Passen alle Kandidaten
eines Zeitpunkts ohnehin hinein, wird die Kaskade **gar nicht erst befragt**.

**Aufwand vernachlaessigbar:** 3,45 s Kaskade ueber alle neun Bots, dazu 8,1 s
einmaliger Aufbau der Tagesreihen.

### AA.6 — Was bewusst NICHT gemacht wurde

**Die neun `equity_simulation.py` wurden nicht zusammengelegt**, obwohl der
Auftrag es zur Entscheidung stellte. Die Begruendung ist besser als die Frage:

- Die `collect_all_trades()` haben **verschiedene Signaturen** (jede Strategie
  andere Parameter).
- Die `__main__`-Bloecke unterscheiden sich **sachlich** —
  `volatility_breakout_crypto` wendet seinen BTC-Regimefilter dort an, nicht in
  `collect_all_trades()` (PR #57).
- **`shared/determinismus.py`, `shared/ergebniskurven.py`,
  `shared/portfolio_overview.py` und mehrere `research/`-Programme haengen an
  der heutigen Form** — ein `equity_simulation.py` je Bot, je Unterprozess
  importiert, mit `inspect.signature`-Abfragen darauf.
- `elliott_wave` behaelt aus demselben Grund seine Signatur **ohne**
  `max_concurrent_positions`: `portfolio_overview.py` und
  `research/order_sensitivity/run_one_bot.py` erkennen genau daran, welcher Bot
  kein Limit hat.

**Kein Parameter geaendert** — auch nicht `MAX_CONCURRENT_POSITIONS` bei
`volatility_breakout`. Der Lauf bestaetigt **Y3** erneut: 0 von 20
Permutationen erreichen das Limit, alle 3 049 abgelehnten Trades gehen auf
fehlendes Kapital zurueck.

### AA.6b — Die Kurven wurden sofort neu erzeugt (13.09.2026)

Vorher **9x ABWEICHEND** — darunter auch `elliott_wave`, obwohl sich dessen
Kennzahlen nicht aendern: Die neue **Ausstiegsreihenfolge** veraendert den
Zeilenaufbau der Datei.

Nachher **9x AKTUELL**, Rueckgabewert 0. Die alten Fassungen bleiben ueber die
Git-Historie nachvollziehbar (9 Dateien, 17 458 Einfuegungen / 17 466
Loeschungen).

*Vorbehalt, bewusst in Kauf genommen:* Nach der Mass-Reparatur werden die
Kurven vermutlich **noch einmal** neu erzeugt werden muessen. Das kostet einen
Befehl und ein paar Minuten — kein Argument fuers Warten.

### AA.7 — In einfacher Sprache

**Was das Problem war:** Wenn mehrere Bots gleichzeitig kaufen wollten und nicht
genug Platz oder Geld da war, bekam den Zuschlag einfach der, der zufaellig
weiter oben in einer Textdatei stand.

**Was jetzt gilt:** Eine Regel in vier Stufen. Zuerst zaehlt die Staerke des
Signals — das gibt es aber nur bei zwei Bots. Dann: Welcher Kandidat passt am
wenigsten zu dem, was schon im Depot liegt? Dann: Welcher laesst sich leichter
handeln? Und ganz zuletzt, falls immer noch Gleichstand: ein Zufall mit festem
Startwert, protokolliert.

**Wie oft der Zufall wirklich entscheidet:** Sechsmal. Bei 3 704 strittigen
Faellen.

**Was sich an den Zahlen aendert:** Sie verschieben sich, aber alle bleiben
innerhalb dessen, was vorher schon moeglich war. Vorher gab es keine richtige
Zahl, sondern zwanzig — und die Dateisortierung hat eine davon ausgewaehlt.
Jetzt gibt es eine, und sie hat einen Grund.

**Was sich nicht aendert:** Kein Bot handelt andere Signale. Kein Parameter
wurde angefasst.

### AA.8 — Offen

| # | Punkt |
|---|---|
| ~~AA1~~ | ✅ **ERLEDIGT am 13.09.2026, direkt im Anschluss.** Alle neun Kurven neu erzeugt, `9x AKTUELL`, Rueckgabewert 0. Commit `94b2e3c` liegt lokal (Push fehlt, siehe A9). Dashboard neu gestartet. **Begruendung fuer sofort statt spaeter:** Der Zwischenzustand ist gefaehrlicher als beide Endzustaende — Anzeige und Code haetten sonst wochenlang auseinandergelegen. Und `ergebniskurven.py` haette dauerhaft `ABWEICHEND` gemeldet und damit **seine Warnfunktion verloren**: ein Melder, der immer meldet, wird abgeschaltet |
| **AA2** | Die Ermessensentscheidung bei `rsi2_mean_reversion` (2,1 % Gleichstaende, knapp ueber der 2-%-Marke) — bewusst so gesetzt, umkehrbar in einer Zeile |
| ~~Y1~~ | **ERLEDIGT** — die Zuteilungsregel ist eingebaut |

---

## AB — TB-27: Bestandsaufnahme Kapitalsimulation (PR #100, 13.09.2026)

Vorarbeit zur Mass-Reparatur. **Untersuchung, keine Aenderung.**

### AB.1 — Die Antwort: weder eine Stelle noch neun

> **In den neun `equity_simulation.py`: zwei Stellen, und beide sind schon
> einheitlich.** Die Kapitalrechnung steht seit TB-26 einmal in
> `shared/zuteilung.py`; das Drawdown-Mass steht neunmal da, aber
> **zeichengleich**. Die Renditeformel ebenso.
>
> **Die Zahl, die eine Entscheidung traegt, entsteht dort aber nicht.**
> Parameter werden nach `robustness_score` ausgewaehlt — und der entsteht in
> `multi_symbol_optimise.py` (**9×**), `multi_symbol_walk_forward.py` (**6×**)
> und den aelteren `optimise_*.py` (**3×**).
>
> **Fuer die Mass-Reparatur: 9 + 6 + 3 — und keine davon in
> `equity_simulation.py`.**

**Der Vergleich, Funktion fuer Funktion** (AST ohne Docstrings):

| Funktion | Gruppen | Befund |
|---|---:|---|
| `calculate_max_drawdown` | **1** | alle neun **zeichengleich** |
| `simulate_portfolio` | **2** | acht zeichengleich; `elliott_wave` allein (kein Positionslimit) |
| `apply_btc_regime_filter` | 1 | nur bei `volatility_breakout_crypto` |
| `__main__` | 8 | nach Abzug der Bildschirmausgabe bleiben **drei** Unterschiede |
| `collect_all_trades` | **9** | jede Fassung fuer sich |

Die drei verbleibenden `__main__`-Unterschiede sind **alle bot-eigen noetig**.
**Die Messkette selbst ist in allen neun identisch.**

### AB.2 — ⚠️ M1 hat den Walk-Forward nie erreicht

> PR #90 hat `max_drawdown_chronologisch_pct` in die neun
> `multi_symbol_optimise.py` gebracht. **Sechs der neun Bots haben aber einen
> eigenen Walk-Forward-Rechner, und der kennt nur das Blockmass.**
>
> Der Walk-Forward ist **Pflichtstufe der Methodik**. Faellt die Entscheidung
> fuer das chronologische Mass, waehlt er bei sechs Bots **weiter nach dem
> alten**.

**Das betrifft den Zeitplan bis 13.12.2026** und gehoert in die
Mass-Reparatur aufgenommen.

### AB.3 — Die stillen Divergenzen

**Eine mit moeglicher Zahlenwirkung:**

| # | Befund |
|---|---|
| **U5** | Fehlt `BTCUSDT` in den Kursdaten, **ueberspringt `t3_supertrend` seinen BTC-Regimefilter stillschweigend**; `volatility_breakout_crypto` **bricht ab** und begruendet das ausdruecklich („wird NICHT stillschweigend ungefiltert weitergerechnet"). **Dieselbe Frage, zwei entgegengesetzte Antworten, nirgends entschieden.** *Eingrenzung:* `t3_supertrend/forward_test.py` verhaelt sich live genauso — **keine** Backtest-gegen-Live-Abweichung, sondern eine **zwischen zwei Bots**. Erreichbar, wenn `data/BTCUSDT_4h.csv` fehlt |

**Drei ohne Zahlenwirkung, aber irrefuehrend:**

| # | Befund |
|---|---|
| **U9** | `rsi2_mean_reversion/equity_simulation.py:48` verweist auf `run_from_walk_forward_best()` — **die Funktion gibt es im ganzen Repo nicht** |
| **U10** | Zwei von drei `research/`-Kopien von `calculate_max_drawdown()` behaupten, „identisch" zur Bot-Fassung zu sein, und sind es nicht (zusaetzliches `float()`). Zahlenwirkung nicht zu erwarten, **nicht nachgemessen** |
| **U6/U8** | `elliott_wave` traegt als einziger der drei Bots mit hart verdrahtetem `ALLOCATION_PCT` keinen erklaerenden Kommentar; die in PR #48 korrigierte Erklaerung zu uebersprungenen Trades ist nur bei **einem** der acht Limit-Bots angekommen |

**Als unklar gemeldet, nicht geraten:**

| # | Befund |
|---|---|
| **U11** | `elliott_wave_stocks` kappt die Historie **vor** der Indikatorberechnung, die drei anderen Aktien-Bots nur den Einstiegszeitpunkt — und begruenden genau das. Ob das fuer Elliott noetig ist oder ein Rueckstand, **ist aus dem Code nicht entscheidbar**. In `docs/` und `research/` steht nichts dazu |

**Nicht gefunden:** keine abweichende Rechenformel, keine abweichende Rundung,
keine abweichende Reihenfolge, kein zweiter Startkapital-Wert.

### AB.4 — Die Abhaengigkeiten: 123, nicht fuenf

154 Python-Dateien nennen `equity_simulation`, **125** fassen sie als Code an,
**123 davon von aussen**. **TB-26 nannte fuenf.**

| Klasse | Anzahl | die wichtigsten |
|---|---:|---|
| **Signaturabfrage** auf `simulate_portfolio` (erkennt „hat kein Limit") | **12** | `shared/portfolio_overview.py`, `shared/determinismus_lauf.py`, `shared/test_zuteilung.py`, 9× `research/` |
| Bot-Liste ueber Dateiexistenz | 3 | `shared/ergebniskurven.py`, `shared/determinismus.py` |
| ⚠️ **Datei-Inhalt per AST** | 1 | **`notifications/manual_close.py`** — liest `ALLOCATION_PCT` als Literal und ist fuer **drei Bots die einzige Quelle der Positionsgroesse im SCHREIBENDEN Schliess-Dialog** |
| **Zeilennummern** | 1 | `research/parameter_doku/pruefe_fundstellen.py` — **heute rot** (3 Fundstellen seit TB-26 verrutscht) |
| `runpy` / `importlib` ueber den Pfad | 8 | `shared/kurven_lauf.py`, `shared/determinismus_lauf.py` |
| Unterprozess | 34 | wegen der `sys.modules`-Kollision |
| Direktimport nach `sys.path`-Umbiegung | 65 | 37 `strategies/`, 25 `research/`, 3 `shared/` |

> **Eine Abhaengigkeitsklasse „Zeilennummern" war bisher nirgends gelistet.**

### AB.5 — Der empfohlene Weg: keiner der beiden zur Wahl gestellten

| | **Weg A: zusammenlegen** | **Weg B: Zielfunktion tauschen** |
|---|---|---|
| Gewinn | **klein** — der gemeinsame Teil ist schon einheitlich | genau das, was die Reparatur will |
| bricht | ≥ 12 Signaturabfragen, 3 Bot-Listen, `manual_close.py`, 3 Zeilennummern | nichts davon |
| loest NICHT | — | die auswaehlende Kennzahl (9 + 6 + 3) |

**Der kleinste Eingriff, der die Zusicherung traegt:**

1. `calculate_max_drawdown()` und die Renditeformel **einmal** nach `shared/`
   ziehen (Muster `shared/zuteilung.py`), die neun importieren sie. Signatur,
   Dateipfad, `ALLOCATION_PCT` und **alle zwoelf Signaturabfragen bleiben
   unberuehrt**.
2. `shared/ergebniskurven.py::kennzahlen()` und `shared/determinismus_lauf.py`
   auf dieselbe Quelle umstellen, statt nachzurechnen.
3. **Getrennt danach:** welches Mass fuehrt — und ob die 9 + 6 + 3 auswaehlenden
   Stellen mitwandern.

> **Schritt 1 und 2 aendern keine Zahl** (pruefbar: `ergebniskurven.py` muss
> danach weiter `9× AKTUELL` melden). **Schritt 3 aendert Zahlen** und gehoert
> hinter den Vergleich, nicht davor.

**Nicht entschieden** — Entscheidung des Nutzers, Frist **13.12.2026**.

### AB.6 — Was entstanden ist

`research/tb27_kapitalsimulation/vergleich.py` ist mit `--pruefen` ein
**Waechter**, der kuenftige stille Divergenz meldet; `test_vergleich.py` belegt
mit 23 Pruefungen, dass er auch **rot** wird. Dazu `abhaengigkeiten.py`, die die
Liste mechanisch und wiederholbar erzeugt. **Alle laufen ohne `pandas`, ohne
Kursdaten, ohne Netz und schreiben nichts.**

**Vorbestehend rot auf `main`:** `research/parameter_doku/pruefe_fundstellen.py`
(35/38) — drei dokumentierte Zeilennummern, seit TB-26 verrutscht. Mit drei
Zahlen zu beheben.

### AB.7 — In einfacher Sprache

**Was wir wissen wollten:** Bevor wir das Messverfahren reparieren — an wie
vielen Stellen im Code steht es eigentlich?

**Was herauskam:** An der Stelle, wo wir gesucht haben, ist schon alles
einheitlich. Die eigentliche Zahl, nach der deine Bot-Einstellungen ausgewaehlt
wurden, entsteht aber **ganz woanders** — an achtzehn Stellen in drei
verschiedenen Dateitypen.

**Der wichtigste Nebenbefund:** Eine Korrektur von letzter Woche ist nur zur
**Haelfte** angekommen. Sechs deiner Bots pruefen ihre Einstellungen in einem
zweiten Durchgang — und der rechnet noch mit der alten, kaputten Zahl.

**Was ausserdem auffiel:** Zwei Bots gehen mit demselben Problem
unterschiedlich um. Fehlt eine bestimmte Kursdatei, rechnet der eine einfach
ohne Filter weiter und sagt nichts; der andere bricht ab und erklaert warum.
Beides ist vertretbar — nur hat es nie jemand entschieden.

**Was das fuer dich heisst:** Die Reparatur ist kleiner als befuerchtet, aber
sie muss an **anderer Stelle** ansetzen als gedacht. Und es gibt einen
Zwischenschritt, der **ueberhaupt keine Zahl veraendert** — den kann man
risikolos vorziehen.

### AB.8 — Offen

| # | Punkt |
|---|---|
| **AB1** | ⚠️ **Der Walk-Forward muss in die Mass-Reparatur** — sechs eigene Rechner kennen nur das Blockmass (AB.2) |
| **AB2** | **U5 entscheiden:** stillschweigend ohne Filter weiterrechnen oder abbrechen? Zwei Bots, zwei Antworten |
| **AB3** | `research/parameter_doku/pruefe_fundstellen.py` reparieren (3 Zeilennummern) |
| **AB4** | U9, U10, U6/U8 — irrefuehrende Kommentare und Verweise |
| **AB5** | **U11 klaeren:** Warum kappt `elliott_wave_stocks` die Historie frueher als die drei anderen Aktien-Bots? Aus dem Code nicht entscheidbar |

---

## AC — Strategy-Discovery-Pipeline: gepruefte Fremdlieferung (13.09.2026)

Ein auf X gefundenes Setup, von Fable als eigenstaendiges Modul nachgebaut
(`strategy_discovery.zip`, 5 Python-Dateien, 2 048 Zeilen) und anschliessend in
zwei Runden geprueft.

### AC.1 — Was das Modul ist

Vier entkoppelte Prozesse ueber JSON-Dateien:
`candidates/live.json → hypotheses/ → backtests/ → validated/ → Telegram`.
Vier Strategiekategorien (Stat-Arb, Vol-Regime, Faktor-Alpha,
Insider-Cluster), sieben Validierungsschwellen.

**Was ueberzeugt:** Kein Zugriff auf das bestehende Repo, keine Bot-Aenderung,
**keine Orderausfuehrung** · `SafeExpressionEvaluator` statt `eval()` (die
Bedingungen kommen als Strings aus Dateien) · der **Backtest-Kern ist kausal
sauber** (Einstieg zum Schluss von Balken *i*, der Ertrag von *i* wird nicht
mitgenommen; Features rollierend) · Kosten 0,003 wie im Projekt · Kill-Switch ·
`--once` fuer Cron · HAC-Standardfehler · eine **DSR ueberhaupt vorhanden**.

### AC.2 — ⚠️ Der Befund, der den Fall entscheidet: der Holdout

`compute_metrics()` nimmt immer `r.iloc[-n_oos:]` — die **letzten 30 % derselben
Reihe**. Jeder Kandidat wird gegen **denselben Zeitraum** geprueft, und
`min_oos_sharpe = 0.75` ist eine der sieben Schwellen.

**Die Rechnung** *(Naeherung; Annahmen: unabhaengige Kandidaten,
normalverteilte Renditen — beide gelten nicht, die Zahlen sind eine Obergrenze
der noetigen Korrektur)*:

| | |
|---|---|
| 30 % von fuenf Jahren | ≈ **378 Tagesbalken** |
| Sharpe 0,75 dort | ≈ **0,92 Sigma** ueber null — *ungefaehr das Niveau, das eine einzige Rauschstrategie im Mittel erreicht* |
| erwartetes Maximum reinen Rauschens nach **30** Abfragen | ≈ 2,0 Sigma ≈ **Sharpe 1,7** |
| nach **100** Abfragen | ≈ 2,5 Sigma ≈ **Sharpe 2,0** |

> **„Der Holdout ist nach wenigen Kandidaten kein Holdout mehr, und das System
> weiss es nicht."**

**Drei Konstruktionen, die nicht daran scheitern — keine kostenlos:**

| # | Konstruktion | Preis |
|---|---|---|
| **1** | **Gar nicht auf den Holdout selektieren.** Auswahl nur in-sample mit Multiplizitaetskorrektur; der Rest geht in den **Forward-Test**, der je Kandidat nur **einmal** befragt wird (er beginnt ab dem Erzeugungszeitpunkt) | Der Durchsatz wird nicht vom Rechner begrenzt, sondern von der Forward-Test-Kapazitaet — *„und die waechst mit einem Tag pro Tag"*. Das „erste Alert nach sechs Stunden" aus dem Artikel ist genau das Versprechen, das diese Konstruktion **nicht** abgeben kann |
| **2** | **Den Holdout budgetieren** (Dwork u. a. 2015, „The reusable holdout", *Science* — fremde Messung, i.i.d.-Annahme gilt fuer Finanzreihen nicht). „Thresholdout": Der Holdout gibt **nie** seinen Wert heraus, sondern beantwortet nur „weicht OOS von IS um mehr als τ ab?"; **jede Ja-Antwort verbraucht Budget** | Ab aufgebrauchtem Budget ist der Zeitraum verbraucht |
| 3 | **Combinatorial Purged CV** | ❌ **Loest ein anderes Problem** — die Pfadabhaengigkeit *einer* Strategie, nicht die Wiederverwendung ueber Kandidaten hinweg. Bringt hier nichts |

> **Die Antwort auf „wie zaehlt man die Nutzung":** **Nicht die Schwelle
> anheben, sondern Budget verbrauchen.** Eine angehobene Schwelle muesste die
> Zahl der effektiv **unabhaengigen** Kandidaten kennen — und die kennt niemand.

**Empfehlung:** Konstruktion 1, mit dem Zaehler aus 2 als Diagnose. OOS raus aus
der Konjunktion, rein in den Bericht, mit der Zeile „dieser Zeitraum wurde
n-mal abgefragt".

### AC.3 — Gehoert das Modul ins Projekt? „Jetzt nicht, und wahrscheinlich nie in dieser Form."

| Grund | |
|---|---|
| **Falsches Mass** | Die Maschine produziert Kandidaten auf dem Mass, dessen Reparatur bis Dezember aussteht. **Keine Vorarbeit, sondern Nacharbeit** |
| ⚠️ **Selektion auf Beta** | Der Validator selektiert auf **rohen Sharpe**; die Alpha-t-Statistik wird nur **berichtet**. In einem Buch, das bereits stark mit Buy-and-Hold korreliert (**+0,82** beim staerksten Bot, siehe **L1**), wuerde eine long-only Entdeckungsmaschine in einer Aufwaertsphase **bevorzugt Beta validieren** — genau das, was **Rang 3** herausfiltern soll |
| **Wechsel der Gattung** | Von neun Bots, die einzeln verstanden und begruendet werden, zu einem Prozess, der Dinge **erzeugt**. Mit der Entscheidung gegen ML aus Gruenden der Nachvollziehbarkeit nur vereinbar, wenn die **menschliche Pruefung je Kandidat** bleibt — und dann ist es keine 24/7-Maschine, sondern ein **Kandidatengenerator fuer die Research-Stufe** |

**Wenn ueberhaupt, dann nach Rang 3**, mit zwei Bedingungen: Der Validator misst
mit dem **reparierten** Mass statt mit den sieben Schwellen, und er selektiert
auf **Alpha nach Beta-Bereinigung** statt auf Sharpe.

**Als eigenes System daneben: nein** — *„ein getrenntes System versteckt die
Versuchszahl nur vor dem Hauptprojekt."*

**Zur Konfiguration „Auswahl auf Y und Bericht auf Y": ja, ohne Abschwaechung.**
Was per Telegram hinausgeht, sind die Zahlen, auf denen selektiert wurde — und
die sind bei Ueberlebenden systematisch nach oben verzerrt.

### AC.4 — Die Schwellen, auseinandergenommen

| Schwelle | Urteil |
|---|---|
| **Trefferquote > 55 %** | ❌ **Streichen.** Um 55 % von 50 % bei 80 % Power einseitig auf dem 5-%-Niveau zu unterscheiden, braucht es rund **600 Trades**. Kein Tagesbot liefert das. Ausserdem **strategietypabhaengig** — Trendfolge gewinnt mit 35 % und grossen Gewinnern |
| **`min_trades = 30`** | Bleibt **nur als Untergrenze**, damit Kennzahlen nicht aus drei Trades stammen. **Evidenz liefert sie keine** |
| **Sharpe > 1,5** | Nach Lo 2002 *(fremde Messung, i.i.d.)*: SE ≈ √((1 + SR²/2) / T Jahre) ≈ **0,65** bei fuenf Jahren → 95-%-Intervall **0,2 bis 2,8**. *„Ein Sieb, kein Nachweis"* — und so zu benennen |
| **Drawdown < 15 %** | Pfadmass aus **einem** Pfad. Als **Risikopraeferenz** legitim, als statistische Schwelle wertlos |
| **t und DSR** | ✅ Tragen — **beide skalieren mit der Stichprobenlaenge** |

> **Ehrliche Konjunktion: drei Glieder** — t, DSR, und eine als **Praeferenz
> gekennzeichnete** Drawdown-Grenze.

**DSR und gemischte Verteilungen:** Werden Familien unterschiedlicher Streuung
gepoolt, geht die **Zwischen-Gruppen-Varianz** in die Schaetzung ein → das
erwartete Maximum steigt → die Schwelle wird fuer **alle** strenger, am
staerksten fuer die Familie mit der **geringsten** Eigenstreuung. Zusaetzlich
wurden Per-Periode-Sharpes aus **1h und 1d** gemischt, die auf verschiedenen
Skalen liegen — *„Die Richtung war nicht bestimmbar, weil sie nicht bestimmbar
ist."* **Korrektur (Vorschlag, keine Literatur):** N aus **allen** Versuchen
(Multiplizitaet zaehlt familienunabhaengig), **Varianz aus der eigenen
(Kategorie, Zeitrahmen)-Gruppe**, Untergrenze 1/T solange unter zehn Eintraegen.

**Korrektur an meinem eigenen Einwand zu `maxlags`:** Er war zu scharf. Die
Autokorrelation ueberlappender Positionen schlaegt **voll durch, wenn auf
Trade-PnLs gerechnet wird**. Hier laeuft es auf **Balkenrenditen** — dem Produkt
aus Position und Marktrendite —, und das bleibt bei annaehernd unkorrelierten
Marktrenditen weitgehend unkorreliert. `max(T^0.25, Median-Haltedauer)` bleibt
trotzdem die **sichere Vorgabe**, sie kostet fast keine Power.

### AC.5 — ⚠️ Was daraus fuer DIESES Projekt folgt: das Versuchsregister

> **„Was heute schon Wert hat, ist nicht der Validator, sondern `history.json`
> als Versuchsregister: Jede getestete Hypothese wird gezaehlt, auch die
> verworfene. Das fehlt fuer die neun Bots und ihre verworfenen Vorlaeufer. Die
> Versuchszahl rueckwirkend zu schaetzen ist die billigste ehrliche Massnahme,
> die das Projekt jetzt treffen kann."**

**Wozu die Zahl gebraucht wird:** Sobald die Mass-Reparatur durch ist und neu
selektiert wird, ist das laut **U.1** die **erste echte Optimierung** in der
Geschichte des Projekts — ab dann beginnt die Selektionsverzerrung, und die DSR
korrigiert dafuer. Sie braucht als Eingabe genau diese Zahl.

**→ TB-29 formuliert und uebergeben (13.09.2026).**

### AC.6 — Zwei kleinere Befunde

| | |
|---|---|
| **`confidence_percent`** | Mittelwert aus vier normierten Komponenten, auf eine Nachkommastelle gerundet, geht per **Telegram** hinaus. Sieht praezise aus und ist eine Konstruktion. **Wird gestrichen** — *„sie hat keinen Traeger"* |
| **Der Scanner fehlt** | `candidates/live.json` wird von nichts befuellt → die Pipeline hat **keinen Eingang**. Ausserdem brauchen **zwei von vier** Kategorien Daten, die es nicht gibt (implizite Volatilitaet, Fama-French, Form 4). Auf reinem OHLCV laufen nur Stat-Arb und Vol-Regime — und Stat-Arb braucht ein Paar, das der Scanner finden muesste |

### AC.7 — Vorgeschlagene Aenderungen am Modul (nicht eingearbeitet)

1. OOS-Sharpe aus der Validierungs-Konjunktion **entfernen**; nur berichten
2. **Nutzungszaehler** je (Instrument, OOS-Zeitraum), Stilllegung ab Budget
3. DSR: N ueber alle Versuche, Varianz je (Kategorie, Zeitrahmen), Untergrenze 1/T
4. `maxlags = max(int(T ** 0.25), Median-Haltedauer)`
5. **Trefferquote als Schwelle streichen**; `min_trades` als reine Untergrenze
6. `confidence_percent` entfernen; Telegram berichtet t, DSR-p, Versuchszahl, Holdout-Nutzungen
7. Selektion auf **Alpha nach Beta-Bereinigung** statt auf rohen Sharpe — **erst nach Rang 3** und mit dem reparierten Mass

**Empfehlung: Modul so belassen, als Beleg der Diskussion, bis Rang 3 erledigt
ist.** Aenderungen 1–6 sind vorbereitet und koennen auf Zuruf eingearbeitet
werden.

### AC.8 — In einfacher Sprache

**Was das Ding ist:** Eine Pruefmaschine. Man wirft Strategie-Ideen hinein, sie
rechnet sie durch und meldet die, die sieben Huerden nehmen.

**Wo das Problem liegt:** Jede Idee wird gegen denselben letzten Zeitabschnitt
geprueft. Die Huerde liegt ungefaehr dort, wo **reiner Zufall** landet — nach
dreissig Versuchen produziert Zufall regelmaessig Besseres. Die Pruefung wird
also nicht streng genug; sie wird **von der Wiederholung ausgehoehlt**.

**Die Loesung ist nicht, die Huerde hoeher zu setzen.** Dafuer muesste man
wissen, wie viele *wirklich verschiedene* Ideen man probiert hat — und das
weiss niemand. Stattdessen: den Zeitabschnitt wie ein **Konto** behandeln. Jede
Abfrage kostet, irgendwann ist er verbraucht.

**Gehoert es in dein Projekt?** Jetzt nicht. Es wuerde Kandidaten nach einem
Mass auswaehlen, das gerade repariert wird — und bevorzugt Strategien
durchwinken, die **nur mit dem Markt mitlaufen**. Genau das, was du als
Naechstes aussortieren willst.

**Was du trotzdem mitnehmen solltest:** Die Maschine fuehrt Buch ueber *jeden*
Versuch, auch die gescheiterten. Fuer deine neun Bots gibt es so ein Buch
nicht — niemand weiss, wie viele Varianten damals ausprobiert wurden, bevor die
heutigen uebrig blieben. **Das nachzuschaetzen waere billig und ehrlich.**

---

## AD — TB-28: Messkette an eine Stelle (PR #101, 13.09.2026)

Umsetzung der **Schritte 1 und 2** aus der TB-27-Empfehlung. Schritt 3 — welches
Mass fuehrt — ist ausdruecklich nicht Teil.

### AD.1 — Die Zusicherung, ueber einen strengeren Nachweis erfuellt

Mein Auftrag verlangte: `ergebniskurven.py` meldet weiterhin `9x AKTUELL`.
**Auf `main` meldet es `9x ABWEICHEND` — davor wie danach.** Der Grund ist nicht
TB-28 (siehe AD.2).

**Der Ersatznachweis ist strenger als der vorgesehene:**

> Alle neun **frisch gerechneten** Kurven sind vor und nach der Aenderung
> **SHA-256-gleich**, und der vollstaendige `--json`-Bericht ist **byteweise
> identisch** (`0b45a09908a3ac2c…`). Je Bot ist auch die gesamte
> Bildschirmausgabe identisch, bis auf die Zeile mit der Rechenzeit.

*„`9x AKTUELL` haette nur gesagt, dass neue und abgelegte Kurve zueinander
passen; der Hash-Vergleich sagt, dass sich in den neu gerechneten Kurven keine
einzige Stelle bewegt hat."*

| Bot | Kurve vorher/nachher (SHA-256) | Rendite | Max DD |
|---|---|---:|---:|
| `elliott_wave` | `0ac94d2a2aeb9cd4` | 67,77 % | −10,17 % |
| `elliott_wave_stocks` | `7ab94aa92332eeaf` | 419,07 % | −22,97 % |
| `rsi2_crypto` | `bce76ccd78ab1c2b` | 27,19 % | −13,94 % |
| `rsi2_mean_reversion` | `ef362dd66c514945` | 36,28 % | −19,53 % |
| `t3_supertrend` | `cacc20ffe5ae4668` | 121,70 % | −22,40 % |
| `turtle_soup_crypto` | `224d2f30371863cc` | 152,84 % | −34,85 % |
| `turtle_soup_stocks` | `f2a7bab7c446848d` | 138,15 % | −29,07 % |
| `volatility_breakout` | `fb38978a45d9207e` | 209,59 % | −22,46 % |
| `volatility_breakout_crypto` | `5902183834626c10` | 68,13 % | −16,29 % |

### AD.2 — ⚠️ Warum `main` und der Mac auseinanderlaufen: der ungepushte Commit

Die Sitzung schliesst aus `main`, die Kurven seien seit dem **12.09.**
(`0d1693e`) nicht erneuert worden und TB-26 (`f6d9a28`, 13.09.) habe sie
veraltet zurueckgelassen. **Auf `main` stimmt das. Auf dem Mac nicht.**

> Die Kurven wurden am **13.09. abends nach TB-26 erneuert** und als Commit
> **`94b2e3c`** festgehalten — **aber nie gepusht** (**A9**, gescheitert am
> gesperrten Schluesselbund).

| Stand | `ergebniskurven.py` meldet |
|---|---|
| GitHub `main` | **9x ABWEICHEND** |
| Mac des Nutzers | **9x AKTUELL** *(nach dem Pull von PR #101 erneut bestaetigt)* |

**Beides ist richtig — fuer verschiedene Staende.** Dies ist die erste
praktische Folge von A9, die ueber „ein Commit fehlt" hinausgeht: **Eine
Cloud-Sitzung kann aus `main` einen Zustand ableiten, den es lokal nicht
gibt** — und daraus, wie hier, eine falsche Praemisse in einem Bericht.

> **Folgerung fuer kuenftige Aufgaben:** Ungepushte Commits, die Ergebnisdateien
> betreffen, gehoeren in die Aufgabenbeschreibung — sonst rechnet die Sitzung
> gegen einen anderen Stand als der Nutzer.

### AD.3 — Was jetzt an einer Stelle steht

| Rechnung | vorher | jetzt |
|---|---|---|
| `calculate_max_drawdown()` | **9×** zeichengleich | **1×** in `shared/messkette.py`, neunmal importiert |
| Renditeformel | **9×** zeichengleich im `__main__` | **1×** als `rendite_pct()` |

Die neun Dateien bleiben an ihren Pfaden, mit ihren Signaturen — jede bekommt
eine Importzeile und verliert sieben Zeilen Rumpf. **Alle 123 Abhaengigkeiten
aus AB.4 bleiben unberuehrt.**

**Der englische Name bleibt**, obwohl die neueren gemeinsamen Module deutsch
benennen: **ueber dreissig Stellen** rufen ihn als Attribut des Bot-Moduls auf
(`es.calculate_max_drawdown(...)`). Durch den Import bleibt er genau das.

**Nebenbefund:** `shared/determinismus_lauf.py` hat den Drawdown **nie**
nachgerechnet — es liest ihn als Variable `max_dd` aus den `__main__`-Globalen
des Bots. Diese **unsichtbare Namensschnittstelle** (TB-27, 4.2) bleibt, wie
sie ist.

### AD.4 — U10 zum zweiten Mal, diesmal in `shared/`

`shared/ergebniskurven.py::kennzahlen()` rechnete **denselben Wert**, lieferte
aber einen **anderen Typ**: `round(float(max_dd), 2)` statt `round(max_dd, 2)`
→ `float` statt `numpy.float64`. Auf allen neun abgelegten Kurven nachgemessen.

**Nicht stillschweigend angeglichen**, weil der Wert in die `--json`-Ausgabe
geht und `repr()` eines numpy-Werts seit numpy 2 `np.float64(-10.17)` lautet.
*„Ihn anzugleichen waere eine Entscheidung ueber die Ausgabe, keine
Aufraeumarbeit."*

### AD.5 — Die Zeilennummern: an ZWEI Stellen repariert

`research/parameter_doku/pruefe_fundstellen.py` war auf `main` **bereits rot**
(35/38) — seit TB-26 verrutscht, ohne dass es aufgefallen waere. Jetzt
**38/38** *(auf dem Mac bestaetigt, 13.09.2026)*.

| dokumentiert (alt) | jetzt |
|---|---|
| `t3_supertrend/equity_simulation.py:66` | `:78` |
| `volatility_breakout/equity_simulation.py:160` | `:151` |
| `volatility_breakout_crypto/equity_simulation.py:176` | `:166` |

Die Zahlen stehen an **zwei** Stellen — im Pruefwerkzeug **und** im Dokublock
der jeweiligen `live_params.py`. Beide nachgezogen, in `live_params.py`
ausschliesslich die Kommentarzeile, **kein Parameter**.

> *„Nur eine Seite zu reparieren haette einen gruenen Waechter ueber einer
> falschen Dokumentation ergeben."*

### AD.6 — In einfacher Sprache

**Was gemacht wurde:** Zwei Rechenformeln, die neunmal identisch im Code
standen, stehen jetzt **einmal** da. Die neun Bots holen sie sich von dort.

**Was dabei zu beweisen war:** Dass sich **keine einzige Zahl** aendert. Das ist
gelungen — die Pruefung fiel sogar strenger aus als geplant: Jede der neun
Ergebniskurven ist vorher und nachher **bis aufs letzte Zeichen** gleich.

**Was nebenbei auffiel:** Drei Verweise in der Dokumentation zeigten auf
falsche Codezeilen — seit vorgestern, ohne dass es jemand gemerkt haette.
Repariert, und zwar an **beiden** Stellen, wo sie stehen.

**Ein Hinweis fuer dich:** Die Sitzung glaubte, deine Ergebniskurven seien
veraltet. **Auf GitHub stimmt das** — weil dein Commit von gestern Abend noch
nicht hochgeladen ist. **Auf deinem Mac ist alles in Ordnung**, mit
`9x AKTUELL` bestaetigt.

### AD.7 — Offen

| # | Punkt |
|---|---|
| **AD1** | ⚠️ **A9 hat jetzt eine zweite Folge:** Solange `94b2e3c` nicht gepusht ist, sehen Cloud-Sitzungen veraltete Ergebniskurven und leiten daraus falsche Praemissen ab. **Push nachholen** |
| **AD2** | U10 in `shared/ergebniskurven.py` — Typ `float` statt `numpy.float64`. Bewusst stehengelassen; **Entscheidung ueber die Ausgabe**, nicht Aufraeumarbeit |

---

## AE — TB-29: Versuchsregister (PR #102, 13.09.2026)

Erhebung, keine Aenderung. Antwort auf **AC.5** — die Eingabe, die die Deflated
Sharpe Ratio braucht.

### AE.1 — Die Zahl

> **2 798 belegbare Rasterauswertungen** ueber die gesamte Projektgeschichte.
> Konservativer, nach Abzug jeder Wiederholung derselben Kombination:
> **653 verschiedene Parameter-Kombinationen.**
>
> **Beides sind Untergrenzen.**

| Bot | Rasterauswertungen | verschiedene Kombinationen |
|---|---:|---:|
| `elliott_wave_stocks` | 1 085 | 264 |
| `elliott_wave` | 977 | 252 |
| `t3_supertrend` | 406 | 81 |
| `rsi2_crypto` | 73 | 18 |
| `turtle_soup_crypto` | 49 | 12 |
| `turtle_soup_stocks` | 49 | 12 |
| `rsi2_mean_reversion` | 25 | 6 |
| `volatility_breakout` | 17 | 4 |
| `volatility_breakout_crypto` | 17 | 4 |
| bot-uebergreifend | 100 | — |
| **Gesamt** | **2 798** | **653** |

Zusammensetzung: 237 aus den neun Bot-Rastern · 246 aus den neun
Walk-Forward-Laeufen · 153 aus den drei aelteren Einzelsymbol-Rastern ·
**2 162 aus den Rasterlaeufen unter `research/`**.

### AE.2 — ✅ Die Entwarnung: die Unvollstaendigkeit kippt die Sache nicht

Erwartetes Maximum reinen Rauschens bei N Versuchen: **√(2 ln N)**
Standardabweichungen, auf Jahres-Sharpe umgerechnet:

| N | √(2 ln N) | Schwelle bei 1 Jahr | **Schwelle bei 5 Jahren** |
|---:|---:|---:|---:|
| 36 | 2,677 | 2,68 | **1,20** |
| 237 | 3,307 | 3,31 | **1,48** |
| **653** | **3,600** | 3,60 | **1,61** |
| **2 798** | **3,984** | 3,98 | **1,78** |

> **Die Multiplizitaet waechst mit dem Logarithmus.** Von N = 36 auf N = 2 798
> steigt die Fuenf-Jahres-Schwelle nur von **1,20 auf 1,78** — *„eine
> Groessenordnung Unsicherheit in N verschiebt die Schwelle nur wenig."*
>
> **Genau deshalb ist eine belegte Untergrenze brauchbar, obwohl sie
> unvollstaendig ist.**

*Zwei Vorbehalte, die dazugehoeren:* Die Naeherung setzt **unabhaengige**
Versuche voraus — benachbarte Rasterpunkte sind es nicht, die Schwelle ist eher
zu hoch. Und N ist eine **Untergrenze**, was in die Gegenrichtung zieht.

### AE.3 — ⚠️ Zwei Befunde ueber Bots, die gerade live handeln

| Bot | Befund |
|---|---|
| **`elliott_wave`** | Die Ergebnisdatei, aus der die heutigen Parameter stammen, ist von **vor der Look-Ahead-Korrektur**. Auf korrigierter Grundlage besteht **keine einzige** der 36 Kombinationen mehr den Mindestfilter |
| **`t3_supertrend`** | Die abgelegte Ergebnisdatei (23 Zeilen) passt zum Bot-Zustand **ohne** BTC-Regimefilter — mit ihm bestuenden **64 von 81** Kombinationen den Mindestfilter, ohne ihn genau **23**. Die Datei, die die Parameterwahl getragen hat, beschreibt einen Zustand, den es nicht mehr gibt |

**Ordnungsbefund:** `results/elliott_wave/` **existiert nicht**. Der Bot legt
seit der Umstellung auf `strategy_paths.py` keine Optimierungsergebnisse mehr
ab; seine Datei liegt bis heute unter dem alten Pfad in der Wurzel von
`results/`.

### AE.4 — Was sich nicht rekonstruieren liess

| # | Luecke |
|---|---|
| 1 | **Die Runden vor dem 02.09.2026.** Die Git-Historie **beginnt mit einem Commit, der bereits drei fertige Bots** samt Rastern und Ergebnisdateien enthaelt. Mechanisch nachgerechnet fuer **jeden** Commit: **0 Rasteraenderungen** ueber alle 21 Optimierungsstellen. Die Runden liegen davor |
| 2 | **Ueberschriebene Ergebnisdateien.** Jede der neun `multi_symbol_optimisation_results.csv` wurde **genau einmal** committet — beim Anlegen des Bots — und nie wieder |
| 3 | ⚠️ **Ein verlorenes Werkzeug mit Namen.** `elliott_wave_stocks/multi_symbol_optimise.py:39` begruendet eine **verschobene Rastergrenze** mit „Erkenntnis aus `compare_exit_rules.py`". Diese Datei hat **nie** im Repo gelegen. *„Die Selektion ist belegt, ihr Umfang nicht."* |
| 4 | **Informelle Versuche von Hand** — Zeitrahmen-Suche des T3-Bots, Universumserweiterung 25 → 50 → 100 → 150, verworfene 503-Werte-Variante. Nicht ueberliefert |

### AE.5 — Das Werkzeug

`research/versuchsregister/` — fuenf Dateien:

| Datei | Inhalt |
|---|---|
| `REGISTER.md` | eine Zeile je Versuchsblock, Summen je Bot, Gesamtsumme |
| `BERICHT.md` | Methodik, Befunde, Luecken, DSR-Einordnung |
| `raster.py` | AST-Zaehler fuer Rastergroessen — ohne `pandas`, ohne Netz |
| `versuchsregister.py` | Erhebung, Waechter, Historie, DSR |
| `test_versuchsregister.py` | 41 Zusicherungen, zwei Mutationsproben |

```bash
python3 research/versuchsregister/versuchsregister.py --pruefen   # RC 1 bei Befund
```

Der Waechter prueft **53 Angaben** — 21 Rastergroessen, 10 Ergebnisdateien,
22 Rasterlaeufe — und meldet, sobald eine waechst, ohne dass das Register
nachgezogen wurde.

### AE.6 — In einfacher Sprache

**Was wir wissen wollten:** Wie viele Varianten wurden ausprobiert, bevor die
heutigen Bot-Einstellungen uebrig blieben?

**Die Antwort:** Mindestens **653 verschiedene**, insgesamt **2 798**
Durchrechnungen. Wahrscheinlich mehr — die fruehen Versuche sind nicht mehr
auffindbar.

**Warum die Zahl wichtig ist:** Wer oft genug probiert, findet zufaellig etwas,
das gut aussieht. Je mehr Versuche, desto hoeher muss die Huerde liegen, damit
ein Ergebnis etwas bedeutet.

**Die gute Nachricht:** Die Huerde steigt **sehr langsam**. Ob es 36 Versuche
waren oder 2 798, verschiebt sie nur von 1,2 auf 1,8. Die Luecken im Register
sind also verkraftbar.

**Die schlechte:** Bei **zwei** Bots stammen die Zahlen, aus denen die heutigen
Einstellungen gewaehlt wurden, aus einer Rechnung, die inzwischen als
fehlerhaft bekannt ist. Bei einem davon wuerde heute **keine einzige** der
damals geprueften Varianten die eigenen Mindestanforderungen bestehen.

### AE.7 — Offen

| # | Punkt |
|---|---|
| **AE1** | ⚠️ **`elliott_wave`: keine der 36 Kombinationen besteht auf korrigierter Grundlage den Mindestfilter.** Gehoert in die Neuselektion nach der Mass-Reparatur — und ist ein eigenes Argument dafuer, sie nicht zu verschieben |
| **AE2** | **`t3_supertrend`: die Ergebnisdatei beschreibt den Zustand ohne BTC-Regimefilter.** Mit Filter bestuenden 64 von 81 statt 23 |
| **AE3** | `results/elliott_wave/` existiert nicht — die Datei liegt unter dem alten Pfad in der Wurzel von `results/`. Ordnungspunkt |
| **AE4** | Die DSR-Eingabe steht jetzt bereit: **N = 653** (verschiedene Kombinationen) bzw. **2 798** (Auswertungen). Welche der beiden gilt, gehoert zur Mass-Entscheidung |

---

## AF — Vorabfestlegung vor der Neuselektion (Fable, 14.09.2026)

Auf die Frage, was **vor** dem ersten Selektionslauf feststehen muss, damit er
nicht selbst zur Datenausbeutung wird. **Die folgenreichste Antwort des
Projekts** — sie hat TB-30 in zwei Aufgaben geteilt.

### AF.1 — Das Prinzip

> **Datenausbeutung entsteht nicht dort, wo ein Mensch die Zukunft kennt,
> sondern dort, wo ein Mensch NACH dem Ergebnis noch eine Wahl hat.** Jede
> Stelle, an der nach dem Lauf jemand entscheidet — eine Schwelle
> „nachjustiert", ein Rastersegment „ergaenzt", ein Bot „vorerst behalten" —,
> ist eine zusaetzliche Selektion, **die in keinem N auftaucht**.
>
> **Ziel: Nach dem Lauf gibt es keine Entscheidung mehr, nur eine Lektuere.**

**Der Weg dorthin ist Code, nicht Prosa:** Das Skript, das aus den
Rohergebnissen die Auswahl und die Bleibt-Geht-Liste berechnet, wird **vor** dem
Lauf geschrieben und eingefroren. Der Mensch liest danach die **Ausgabe**.

> **Der Vollstaendigkeitstest:** *„Laesst sich das Auswertungsskript ohne Blick
> auf ein Ergebnis fertig schreiben? Wenn nicht, fehlt eine Festlegung."*

### AF.2 — Die elf Festlegungen des Betreibers (14.09.2026)

| # | Festlegung | Wert |
|---|---|---|
| 1 | Fuehrendes Mass | **Kapital-Drawdown** aus `equity_simulation.py` |
| 2 | Selektionsstatistik | **Median des Netto-Sharpe ueber die Selektionsfalten** |
| 3 | Beurteilung | Netto-Calmar + Mittelwert der **drei tiefsten** Drawdowns + Netto-Sharpe |
| 4 | Drawdown-Faktor gegen Benchmark je Falte | **1,25 ×** |
| 5 | Absolute Drawdown-Grenze je Falte | **−35 %** *(statt −30 %)* |
| 6 | Schwelle fuer Zweijahres-Falten | **30 Trades/Jahr** |
| 7 | Spitzen-Schwelle der Plateau-Regel | **50 %** ueber dem Nachbarschaftsmittel |
| 8 | Cluster-Schwelle fuer N_eff | Korrelation **0,9** |
| 9 | DSR-Basis | **N = 653**, dieser Lauf zaehlt dazu |
| 10 | **DSR ist Bericht, nicht Tor** | Bleibt-Geht laeuft ueber die Abbruchkriterien |
| **11** | **Dieses Ergebnis ist zulaessig** | *„Es kann sein, dass kein einziger Bot die Schwelle erreicht."* |

> **Warum −35 % statt der vorgeschlagenen −30 %:** Bei −30 % fiele
> `turtle_soup_crypto` mit seinem heutigen Kapital-Drawdown von **−34,85 %**
> heraus, **bevor die Selektion beginnt**. Eine Nebenbedingung, die einen Bot
> ausschliesst, bevor gewaehlt wird, ist eine verkleidete Entscheidung ueber den
> Bot.

**Festlegung 11 gehoert woertlich ins Register** — *„Wer das vorher nicht
aufschreibt, wird es nachher nicht akzeptieren."*

### AF.3 — Die Konstruktionen, die ich hervorheben wuerde

**Die Drawdown-Schwelle ist relativ und aus Nicht-Bot-Daten abgeleitet:**
hoechstens **1,25 ×** der Drawdown einer **konstanten Position mit dem heute
gemessenen mittleren Exposure** in derselben Falte. Sie passt sich damit dem
Regime an (2022 erlaubt mehr als 2017), stuetzt sich auf Daten, die keine
Bot-Ergebnisse sind, und stellt die richtige Frage. **Vorab berechenbar** — und
das zeigt vor dem Lauf, ob sie in 2020/2022 ueberhaupt erfuellbar ist.

**Die Kantenregel:**

> Liegt der Gewinner auf einer Rasterkante, wird **nicht erweitert.** Der
> Kantenwert wird genommen, der Bot bekommt die Markierung „Kante". Eine
> Erweiterung waere ein **neuer vorregistrierter Lauf**, dessen Zellen zu N
> addiert werden.

*Genau das ist in der Vergangenheit unterblieben (**AE.4**, Punkt 3).*

**Jede Rastergrenze braucht einen Begruendungssatz, der kein Ergebnis nennt** —
gestuetzt nur auf Handelskosten, Datenfrequenz, Volatilitaet des Universums oder
die Haltedauer-Hypothese. Und: **Der heutige Live-Wert ist kein Bezugspunkt.**
Maschinell pruefbar — kein Grenzsatz darf ihn erwaehnen.

**Falten ohne Trade zaehlen mit Sharpe 0**, nicht ausgelassen. *„Auslassen
belohnt Saetze, die in schweren Jahren nicht handeln."*

**Die letzte Falte wird nicht selektiert.** Sie ist die **Bestaetigungsperiode**
— einmal ausgewertet, nachdem die Auswahl steht, Ergebnis berichtet wie es
ausfaellt. Kein Veto, aber die einzige Zahl ohne Selektion. **Und sie waechst
jeden Monat.** Dazu gehoert der Vergleich des Backtest-Kapitalpfads der **alten**
Parameter ueber dieselbe Periode gegen den **echten** Paper-Trading-Pfad —
*„das ist der Test des Backtesters, nicht des Bots"*.

**Die Amendment-Regel:**

> Ein **Bug-Fix ist ein Amendment**: dokumentiert, **der Lauf beginnt von
> vorn**, und die Ergebnisse vor dem Fix werden **nicht** neben die danach
> gelegt. *„Wer Vorher und Nachher vergleicht, hat wieder eine Wahl."*

**Wenn mehrere Bots ausscheiden** — die drei Regeln, weil dort der Druck am
groessten sein wird:

- ⚠️ **Die Anzahl ausscheidender Bots ist KEIN Grund, eine Schwelle zu aendern.**
- Das **Kapital** geht in eine **statische Benchmark-Position** in Hoehe des
  mittleren Exposures — nicht in Kasse, nicht zu den Ueberlebenden. So bleibt
  das Portfolio-Beta unveraendert und der Effekt isoliert messbar.
- Der Bot laeuft **als Schatten weiter**, kehrt aber nur ueber einen **neuen
  vorregistrierten Lauf mit veraenderter Hypothese** zurueck. **Kein „vorerst
  behalten", kein „wir schauen im Fruehjahr".**

### AF.4 — Die Verankerung: reicht ein Commit?

**Noetig, nicht hinreichend** — Git-Zeitstempel sind editierbar. Vier Stufen,
die ersten drei zusammen etwa eine Stunde:

| | |
|---|---|
| **Signierter Tag** (GPG) | bindet den Zustand an einen Schluessel statt an einen Zeitstempel |
| **Externer Zeitanker** | **OpenTimestamps** (Bitcoin-Verankerung, kostenlos, ein Aufruf) fuer Register-Hash + Datenstand-Hash |
| **Herkunft in jeder Ergebnisdatei** | Commit-Hash, Datenstand-Hash, Register-Hash; **append-only**-Log statt Ueberschreiben |
| **Das Urteil ist Code** | die eigentliche Absicherung, **und sie ist keine kryptografische** |

*Als fuenfte Stufe moeglich:* einen der informativen Agenten als **Auditor**
einsetzen, der vor dem Lauf die Konfiguration gegen das Register prueft. *„Das
ersetzt kein Vier-Augen-Prinzip, aber es ist das, was ein Einzelbetreiber davon
haben kann."*

### AF.5 — ⚠️ Die Antwort auf „was, wenn keiner die Schwelle erreicht"

> **„Es ist das wahrscheinliche Ergebnis."**

`√(2 ln N)` ist die erwartete Hoechstleistung von N **reinen Rauschstrategien** —
eine Latte, die sagt: *um vom Besten von 653 Zufallslaeufen unterscheidbar zu
sein, brauchst du ueber fuenf Jahre Sharpe 1,6.* Ein privater Long-only-Bot auf
Tages-OHLCV hat, wenn er gut ist, einen wahren Netto-Sharpe **zwischen 0,4 und
0,9** *(Einschaetzung, keine Messung)*. Die Korrelation benachbarter Zellen
(N_eff) senkt die Latte vielleicht auf 1,2–1,4, **nicht auf 0,8**.

> **Die ehrliche Konsequenz ist nicht „alle Bots sind Rauschen".** Sie ist:
> **Der Backtest kann bei dieser Stichprobe keinen der Bots vom
> Besten-von-N-Rauschen unterscheiden.** Das ist eine Aussage ueber den
> **Backtest**, nicht ueber die Bots — und der Grund, warum DSR Bericht und
> nicht Tor ist.

**Was dann traegt, ist dreierlei:** der **Prior** (ist die Ertragsquelle in der
Literatur dokumentiert? — *das unterscheidet RSI-2 von Elliott Wave*), die
**Robustheit ueber Falten**, und der **Live-Record**, der jeden Monat waechst und
keiner Selektion unterliegt.

> **Die Beweislast wandert vom Backtest zur Bestaetigungsperiode. Das ist
> unbequem, weil es Jahre dauert, und es ist richtig.**

**Und falls die Beta-Bereinigung zum selben Schluss kommt** — die Bots sind ihr
Exposure mal Buy-and-Hold, mit Kosten —, waere die Konsequenz: **das Beta direkt
halten, gesteuert**, und die Bots als Schattenexperimente weiterlaufen lassen,
bis einer im Live-Record etwas zeigt, was der Backtest nicht zeigen konnte.
*„Das waere kein Scheitern des Projekts. Es waere das erste Ergebnis, das auf
einem gueltigen Mass steht."*

### AF.6 — In einfacher Sprache

**Worum es ging:** Bevor wir die Bot-Einstellungen zum ersten Mal auf einem
sauberen Mass neu auswaehlen — was muss vorher feststehen, damit wir uns nicht
selbst betruegen?

**Die Antwort:** Alles. Und zwar nicht als Notiz, sondern als **fertiges
Auswertungsprogramm**, das vor dem Lauf festgeschrieben wird. Danach liest man
nur noch ab, was herauskommt.

**Der Test dafuer, ob man fertig ist:** Kann man das Auswertungsprogramm
komplett schreiben, **ohne ein einziges Ergebnis gesehen zu haben**? Wenn nein,
fehlt noch eine Festlegung.

**Die ehrliche Warnung:** Es ist **wahrscheinlich**, dass am Ende kein einziger
Bot die statistische Huerde nimmt. Das heisst **nicht**, dass sie schlecht
sind — es heisst, dass zehn Jahre Kursdaten zu wenig sind, um es zu beweisen.

**Und der wichtigste Rat:** Schreib **jetzt** auf, dass dieses Ergebnis in
Ordnung waere. Sonst akzeptierst du es spaeter nicht.

### AF.7 — Folge: TB-30 ist geteilt

| | |
|---|---|
| **TB-30a Vorregistrierung** | Register, **eingefrorenes Auswertungsskript**, Rastergrenzen mit Begruendungssaetzen, Vorab-Berechnungen, Verankerung. **Kein Selektionslauf.** *(formuliert und uebergeben, 14.09.2026)* |
| **TB-30b Mass-Reparatur und Lauf** | Die 9 + 6 + 3 Stellen umstellen, Walk-Forward einschliessen (**AB1**), dann der Lauf gegen das eingefrorene Skript. **Erst nach TB-30a** |

---

---

## AG — Backlog-Pruefung durch Fable (14.09.2026)

Grundlage: das damalige `BACKLOG_trading_bot.md`, **4 736 Zeilen, vollstaendig
gelesen**. Die schaerfste Pruefung, die das Projekt bekommen hat — und sie
beginnt beim Dokument selbst.

### AG.1 — Das Backlog war das Problem geworden

> **277 KB sind rund 70 000 Token.** Eine Sitzung, die damit beginnt, hat ihr
> Kontextfenster zu einem grossen Teil verbraucht, **bevor die erste Frage
> kommt** — und liest die eigentlichen offenen Punkte neben 4 000 Zeilen
> abgeschlossener Ergebnisberichte. Etwa ein Drittel des Textes waren die
> „In einfacher Sprache"-Abschnitte, die keine Sitzung braucht.
>
> *„4 400 Zeilen in zwei Tagen sind kein Backlog mehr, sondern ein Journal, das
> sich Backlog nennt."*

**Und das war die Ursache der meisten Widersprueche:** *„Ein Dokument, das an
einem Tag um zwanzig Bloecke waechst, wird angehaengt, nicht gepflegt. Die
fruehen Bloecke sagen, was am 12.09. galt, die spaeten, was am 14.09. gilt, und
niemand hat die fruehen angefasst."*

**✅ Umgesetzt am 14.09.2026:** Aufteilung in `BACKLOG.md` (**299 Zeilen**, nur
aktive Punkte) und `JOURNAL.md` (diese Datei, chronologisch, nie
umgeschrieben).

### AG.2 — ⚠️ Die Etikettenkollision

Dieselben Kuerzel bedeuteten zweierlei:

| Kuerzel | im Backlog | im Strategie-Katalog |
|---|---|---|
| **A1** | Festplattenvollzugriff am Mac | Portfolio-Regime-Gate |
| **B1** | „B1 entwirft das" — eine Sitzung | **Multi-Asset-ETF-Trend, Rang 4** |
| **E1** | Eurobetraege im Dashboard | Turn-of-Month |
| **F1/F2** | `spiegel.py`-Logs / Lauf-Protokoll | Kapitalkonto / Meta-Labeling |
| **G1** | ⚠️ **„Alles haengt an einem MacBook"** | Ko-Drawdown-Gewichtung |

> **Der gefaehrliche Fall:** *„G1 gestrichen"* steht in U.2. Wer das im Backlog
> umsetzt, streicht **„Alles haengt an einem MacBook"** — die eine
> Architekturfrage, die fuer den Live-Record tatsaechlich zaehlt.

**✅ Abhilfe umgesetzt:** Katalog-Kuerzel tragen im Backlog das Praefix `S-`.

### AG.3 — Widersprueche, die eine Entscheidung verlangten

**⚠️ Die −35 % waren ein Regelbruch mit Begruendung.** Die absolute
Drawdown-Grenze wurde von −30 % auf −35 % gesetzt, *„weil bei −30 %
`turtle_soup_crypto` mit seinem heutigen Kapital-Drawdown von −34,85 %
herausfiele"*. Drei Einwaende:

> 1. **Die Begruendung dreht sich um:** *„Eine Schwelle, die verschoben wird,
>    damit ein Bot **drin bleibt**, ist genauso eine Entscheidung ueber den Bot
>    wie eine, die ihn ausschliesst — nur die zweite ist sichtbar, die erste
>    steht in keinem N."*
> 2. **Kategorienfehler:** Die Nebenbedingung gilt **je Falte und je
>    Parametersatz**; −34,85 % ist der **Vollperioden**-Drawdown der
>    **heutigen** Parameter.
> 3. Es bricht die Regel aus AF.3 — *„der heutige Live-Wert ist kein
>    Bezugspunkt"* — **im selben Block**.

→ **V1** im neuen Backlog.

**⚠️ Die Krypto-Daten beginnen 09/2021.** Der Faltenplan setzte Training ab 2018
an. Nach Mindesttraining blieben **zwei Testfalten** — keine Selektionsstatistik.
*Fable dazu: „Das ist mein Fehler: Ich habe ‚zehn Jahre Tagesdaten' aus dem
ersten Prompt auf beide Klassen bezogen."* → **neuer Rang 0,5**, Binance
`/api/v3/klines` ab 2017, Spot, kostenlos.

**⚠️ Agent 2 optimiert seit dem 13.09. auf dem falschen Mass.** TB-22 hat den
Satz *„es gilt das chronologische"* **fest verdrahtet**; am selben Abend wurde
der **Kapital-Drawdown** als fuehrend entschieden. *„Genau die Konstellation,
fuer die U.6 die Ausnahme ‚sofort umstellen' gemacht hat."* → **V6**.

**Weitere:** AB2/U5 vor dem Lauf auf „abbrechen" entscheiden (**V3**) ·
Y3-Rasterregel `floor(1 / ALLOCATION_PCT)` ergaenzen (**V4**) · das Rang-3-Skript
und der V.5-Test gehoeren ins eingefrorene Auswertungsskript (**V5**) · der
**Oktober-Termin** fuer Elliott Wave gestrichen, weil ein Urteil vor dem
vorregistrierten Lauf eine Entscheidung ausserhalb des Registers waere.

### AG.4 — Zwei Lehren im Dokument waren falsch

| Lehre | Korrektur |
|---|---|
| *„Der Engpass ist das Positionslimit, nicht das Kapital — praktisch 100 % der Ablehnungen"* | **Falsch fuer zwei Bots.** Sie stammte aus einer Datei mit 115 Ueberspruengen; TB-23 hat auf dem **Kapitalpfad** gemessen: Bei `turtle_soup_stocks` und `volatility_breakout` bindet die **Kapitalschranke** (3 100 bzw. 3 049 abgelehnte Trades) |
| *„Die plausiblere Erklaerung ist, dass das gemeinsame Buch meist aus Kasse besteht"* | **Widerlegt durch L.1.** Die tatsaechlichen Ursachen: veraltete Dateien, falscher Nenner, **falscher Vergleichspartner** |

**✅ Beide im Journal korrigiert** (durchgestrichen mit Korrekturvermerk, nicht
geloescht).

### AG.5 — Die Zahl, die viermal verschieden dastand

| Rendite `elliott_wave_stocks` | Quelle |
|---|---|
| +1 500,53 % | alt, vor der Look-Ahead-Korrektur |
| **+330,18 %** | **Q.2 — mit AST-Nachweis in `live_params.py` geschrieben** |
| +352,72 % | N.2 |
| **+419,07 %** | AA.2 / AD.1 — gilt heute |

> **Die in TB-17 mit Aufwand in den Dateikopf geschriebene Zahl war 24 Stunden
> spaeter wieder falsch**, weil TB-26 die Zuteilung geaendert hat. Q1
> („`ergebniskurven.py` nach jeder Parameteruebernahme") reicht nicht — **die
> Zahl aendert sich auch ohne Parameteruebernahme.**
>
> **Folgerung: keine Kennzahlen in Code-Koepfen, nur Verweise.** Das erledigt
> eine ganze Fehlerklasse (F5, Q1, AB3, AD.5, TB-17) **auf einmal** — und der
> Pruefer aus Q.7 wird zur Wache dagegen, dass sie zurueckkommen.

### AG.6 — Die Antworten auf die beiden offenen Fragen

**Bots anhalten? Nein — einfrieren und beschriften.**

> Was AE.3 zeigt, ist eine Aussage ueber die **Selektion**, nicht ueber das
> **Verhalten**. Laut U.1 trifft das auf **alle neun** zu; bei diesen zweien ist
> es nur belegter. Beide handeln Papier — ein Anhalten spart kein Geld, kostet
> aber die **Kontinuitaet des Live-Records**, der als Test des Backtesters fuer
> *jede* feste Parametrisierung taugt, auch fuer eine schlechte. **Anhalten
> heisst, den Holdout zu unterbrechen.**

Stattdessen: **keine Parameteraenderung an irgendeinem Bot vor TB-30b**, und im
Dashboard den Vermerk „Parameter ohne gueltige Auswahlgrundlage". Die eine
Ausnahme ist ein **Bug**, kein Parameter: AB2/U5.

**Welle-3 danach, nicht davor.** p = 0,91 und 0,63 — *„kein Befund, das ist
Rauschen mit Vorzeichen."* Z.5b sagt: Unter fuenf Prozentpunkten waere bei diesen
Stichproben ohnehin nichts auffindbar. **Reihenfolge: Z4 vor Z1 und Z2** — erst
der Zufalls-Timing-Test entscheidet, ob der Zigzag-Detektor ueberhaupt etwas
traegt.

### AG.7 — Die Streichliste: 15 aktive Punkte statt 100

> *„Nicht, weil die uebrigen falsch waeren — die meisten sind sorgfaeltig
> begruendet —, sondern weil ein Einzelbetreiber mit einer Frist am 13.12. jede
> Stunde, die er in einen Zeitstrahl oder eine Anbieter-Schnittstelle steckt,
> aus TB-30b nimmt."*

**Block C und J — gestrichen bis auf zwei Punkte.** Die Begruendung geht ueber
„die Zahlen sind noch nicht gueltig" hinaus:

- **Die Oberflaeche hat einen Nutzer, ein Geraet, einen Zweck.** Block G warnt
  selbst: *„Eine Notfalloberflaeche muss in zwei Sekunden bedienbar sein."*
  Zeitstrahl, Benachrichtigungs-Zentrale und Trade-Journal arbeiten dagegen.
- **C7 loest das falsche Problem.** Die Antwort auf „acht Befehle von Hand" ist
  **nicht eine Seite**, sondern **F2 plus die vier Waechter, die schon
  existieren** — als Cronjobs mit Telegram-Meldung. *„Das sind vier Cron-Zeilen,
  und sie haengen alle an A1 — einem Klick in den Systemeinstellungen."*
- **Die Kopplung ist das Teure.** I19 und I9 sollten „zusammen mit C0
  entworfen" werden — damit haengt der Forward-Test fuer `S-B1` an einer
  Ereignis-Datenbank. **Entkoppeln:** I19 ist ein Bot mit einer Flagge. *„Ein
  Nachmittag, wenn es nicht an C0 haengt."*

**Behalten:** **C8** (nach TB-30b) und **J6** (WAL — 730 Prozessstarts taeglich
auf SQLite ohne WAL).

**Aus dem eigenen Katalog gestrichen** *(Fable korrigiert sich)*: `S-K1`
(dieselbe Ertragsquelle **und** Horizont-Klasse; Krypto-Daten reichen nicht) ·
`S-C1` (vierte Umkehrstrategie — Umkehr-Paare steigen **2,58 ×** haeufiger
gemeinsam ein als der Zufall) · I17 HMM (*„ein Herausforderer ohne
Titelverteidiger"*) · I18-Agent · I.3c · I.3e · K.4b HRP.

**D5 nicht streichen, sondern sperren** — mit methodischen Vorbedingungen
(Rang 1–3, mindestens ein Jahr Bestaetigungsperiode, Backtest-Pfad stimmt mit
Papierpfad ueberein). *„Die ‚Anforderungen' in D5 sind technische, keine
methodischen."*

### AG.8 — In einfacher Sprache

**Was geprueft wurde:** Der gesamte Backlog, 4 736 Zeilen, von jemandem, der
ihn zum ersten Mal am Stueck liest.

**Der erste Befund betrifft die Datei selbst:** Sie ist zu gross geworden. Wer
sie einer neuen Sitzung mitgibt, verbraucht deren halbes Gedaechtnis, bevor die
erste Frage gestellt ist. Deshalb jetzt zwei Dateien — eine mit den offenen
Punkten, eine mit dem Archiv.

**Der gefaehrlichste Befund:** Dieselben Kuerzel bedeuteten zweierlei. „G1
gestrichen" haette beinahe die falsche Sache gestrichen.

**Ein Fehler von mir:** Ich hatte empfohlen, eine Grenze zu lockern, damit ein
Bot nicht vorzeitig herausfaellt. Das ist genauso eine Entscheidung ueber den
Bot wie ihn auszuschliessen — nur eine unsichtbare.

**Und die unbequemste Antwort:** Von hundert Punkten bleiben **fuenfzehn**. Der
Rest ist entweder erledigt, doppelt, oder Arbeit an einer Oberflaeche fuer
Zahlen, deren Gueltigkeit gerade erst geprueft wird.

### AG.9 — Was Fable selbst als unsicher benennt

Kennt nur das Dokument, nicht den Code · ~~ob die Sentiment-Sammlung tatsaechlich angelegt wurde~~ **GEPRUEFT am 14.09.2026: nein.** Weder Cronjob noch launchd-Dienst (je 0 Treffer). Die Entscheidung „sofort beginnen“ vom 13.09. wurde **nie umgesetzt** — `crontab -` ist seit dem macOS-Update ohnehin blockiert (A1). **Kein Handlungsbedarf** · ob unter `data/` doch laengere Krypto-Historien
liegen *(dann entfaellt Rang 0,5)* · die Einschaetzung zur Kapitalschranke
stuetzt sich auf Y.3/AA.6 gegen die aeltere Lehre — *„ich halte die spaetere
Messung fuer die richtige, ohne beide Dateien gesehen zu haben"*.

---

## AH — Zwei offene Stellen, beantwortet (Fable, 14.09.2026)

### AH.1 — Die absolute Drawdown-Grenze: streichen

**Sie bindet nur, wenn `1,25 × DD_Benchmark` tiefer liegt als der absolute
Wert** — also wenn der Benchmark selbst unter **−28 %** fällt. Das passiert bei
Bots mit hoher Exposure in der Krisenfalte (`turtle_soup_stocks` 2022, jeder
Krypto-Bot 2022). Dort bindet sie dann aber **für alle Parametersätze
gleichzeitig** und wirft den Bot aus, **bevor gewählt wurde**.

> *„Ein Bot, der bei voller Exposure in 2022 −33 % macht, hat kein
> Parameterproblem, sondern ein Beta-Problem — und das entscheidet Rang 3, nicht
> eine Nebenbedingung der Rasterselektion. Eine Grenze, die entweder redundant
> ist oder einen ganzen Bot vorab erledigt, gehört nicht ins
> Selektionsregister."*

**Der Risikoappetit kommt an zwei anderen Stellen zu seinem Recht:** als Deckel
je Bot im **Netting** (Rang 5), und als **berichtete Zeile** in der Beurteilung.

### AH.2 — Die echte Lücke liegt auf der anderen Seite

Nicht bei tiefen Drawdowns, sondern in **ruhigen Falten**: 2017 oder H1 2021,
Benchmark −2 %, erlaubt −2,5 %, ein Satz mit −4 % fällt durch. **Bei so kleinen
Zahlen ist das Verhältnis Rauschen** — drei schlechte Tage entscheiden über den
Ausschluss.

**Die Abhilfe ist keine Obergrenze, sondern eine Toleranzuntergrenze:**

```
erlaubt(f) = min( 1,25 x DD_Benchmark(f) ,  DD_Toleranz )
```

beide negativ, `min` ist der **tiefere** Wert — also die grosszügigere Grenze.

**`DD_Toleranz` = Median der Benchmark-Drawdowns über alle Selektionsfalten.**
In einer ruhigen Falte darf ein Parametersatz damit so viel verlieren wie eine
statische Position in einem **typischen** Jahr. Aus Nicht-Bot-Daten, vorab
berechenbar, Krisenfalten unberührt.

**Je Bot, zwingend** — der Benchmark hängt an der Exposure; ein Bot mit 21 %
Zeit im Markt und einer mit 100 % liegen auf verschiedenen Skalen. *„Ein
gemeinsamer Wert wäre für den einen bindend und für den anderen nie."*

### AH.3 — Eine Präzisierung zum Benchmark-Exposure

In der Checkliste stand „das heute gemessene mittlere Exposure des Bots". Das
ist zwar kein Selektionsergebnis, **aber ein Wert der heutigen Parameter**.

> **Sauberer: Benchmark-Exposure = mittlere Exposure des jeweiligen
> PARAMETERSATZES in der jeweiligen Falte.** Der Benchmark wandert dann mit dem
> Satz — ein Satz, der weniger investiert, bekommt weniger Spielraum —, und
> **nichts im Register verweist mehr auf den Live-Zustand**. Die Zahl liegt
> ohnehin vor, weil der Kapitalpfad sie erzeugt.

**✅ Übernommen** in TB-30a.

### AH.4 — Der Nulltest ist ausgenommen, aus drei Gründen

Die Regel „Kandidaten nach Rang 3" existiert, weil eine Selektion auf rohem
Sharpe in einem beta-lastigen Buch Beta durchwinkt. Bei **`S-E1`**:

| | |
|---|---|
| **Keine Selektion** | Das Fenster stammt aus McConnell/Xu; es gibt **keinen Parametersatz zu wählen**, also nichts, das Beta bevorzugen könnte |
| **Beta-Bereinigung eingebaut** | Sein Test 2 vergleicht das Fenster gegen **alle anderen Vier-Tage-Fenster desselben Instruments** — das ist exposure-gleiches Buy-and-Hold als Kontrolle. **Rang 3 muss nichts nachholen** |
| **Berührt nichts** | weder die neun Bots noch das Mass in Reparatur; seine Kennzahlen sind Ereignis-Mittelwerte mit Bootstrap, keine Kapitalpfad-Selektion |

> **Was er prüft, ist der Weg:** Register → Forward-Test ohne Live-Status →
> Bestätigungsperiode → Bericht, **ohne dass unterwegs jemand eine Wahl hat**.
> *„Wenn dieser Weg beim einfachsten möglichen Fall — ein Instrument, zwölf
> Termine im Jahr, null Parameter — nicht sauber läuft, läuft er bei B1 auch
> nicht."*

**Zählt seine Zelle zu N?** Zum **Versuchsregister ja**, als ein Eintrag — *das
Register ist ein Kassenbuch, und ein Versuch ohne Wahl ist trotzdem ein
Versuch.* Zur **DSR nein** — Multiplizität entsteht, wo unter Alternativen
gewählt wird, und dort ist **N = 1**.

**⚠️ Die Stelle, an der das kippen kann:** der Robustheits-Sweep (−2/+3, −1/+2,
−1/+4, QQQ/IWM/EFA).

> **Die Sweep-Zellen sind Robustheit, nicht Auswahl.** Vorab festhalten: **Fällt
> das Kernfenster durch und besteht eine Sweep-Variante, wird die Variante NICHT
> übernommen.** *Sonst sind es acht Versuche und nicht einer, und die Ausnahme
> wäre keine mehr.*

**Zwei Bedingungen, damit die Ausnahme eine bleibt:**

- `S-E1` geht nach dem Backtest in die **Staging-Ebene**, nicht ins Buch —
  *„sonst kommt ein zehnter Beta-Baustein vor die Beta-Bereinigung, nur durch
  die Hintertür."*
- **Zwei Registereinträge:** die Strategiekriterien aus dem Katalog **und** die
  Pfadkriterien. *„Das Ergebnis der Strategie wird gelesen werden — es soll nur
  nicht das sein, woran der Test gemessen wird."*

**Praktische Folge:** `S-E1` kann **parallel zu TB-30b** laufen — er kostet
einen Tag Betreiberzeit und keine Rechenzeit, die TB-30b braucht.

### AH.5 — In einfacher Sprache

**Frage 1 war:** Brauchen wir neben der regimeabhängigen Verlustgrenze noch eine
feste?

**Antwort: nein — und zwar aus einem Grund, den ich falsch herum hatte.** Eine
feste Grenze greift nur in Krisenjahren, und dann wirft sie einen ganzen Bot
raus, **bevor man überhaupt ausgewählt hat**. Genau deshalb hatte ich sie
gelockert — was derselbe Fehler in die andere Richtung war.

**Das echte Problem ist umgekehrt:** In **ruhigen** Jahren ist die Grenze zu
scharf. Wenn der Markt nur 2 % verliert, darf ein Bot 2,5 % verlieren — und drei
schlechte Tage reichen, um durchzufallen. Deshalb jetzt eine Untergrenze: In
einem ruhigen Jahr darf ein Bot so viel verlieren wie der Markt in einem
**normalen** Jahr.

**Frage 2 war:** Darf der einfache Turn-of-Month-Test vorgezogen werden?

**Ja.** Er wählt nichts aus — sein Fenster steht in der Literatur —, und seine
Kontrolle gegen den Markt ist eingebaut. Er prüft nicht, ob eine Strategie
taugt, sondern **ob der Weg funktioniert**, auf dem später echte Strategien
geprüft werden.

**Mit einer Bedingung:** Wenn das Hauptfenster durchfällt und eine Variante
besteht, wird die Variante **nicht** genommen. Sonst hätte man acht Versuche
gemacht und den besten behalten.

---

## AI — TB-30a: Vorregistrierung (PR #103, 14.09.2026)

**Kein Selektionslauf.** Register, eingefrorenes Auswertungsskript,
Vorab-Berechnungen, zwei Bug-Fixes, Verankerung.

### AI.1 — Der Vollstaendigkeitstest: bestanden

> *Liess sich das Auswertungsskript fertig schreiben, ohne ein einziges Ergebnis
> gesehen zu haben?* — **Ja.**

`research/vorregistrierung/auswertung.py` laeuft gegen erzeugte Beispieldaten
mit frei erfundenen Werten und gibt aus: Plateau-Gewinner je Bot, Markierungen
(Spitze, Kante, nicht zulaessig), Bleibt-Geht-Liste nach (a)–(d), die drei
DSR-Werte, alle Kennzahlen der Beurteilung, zuletzt die Bestaetigungsperiode.

> **„Es hat keinen Schalter, der eine Schwelle verschiebt, einen Bot ausnimmt
> oder eine Kennzahl unterdrueckt."**

**Fertigschreiben hiess an sieben Stellen: eine Lesart festlegen**, wo die zwoelf
Festlegungen zwei zuliessen. Alle sieben im Register, Abschnitt 12. Die
tragende: **`DD_Toleranz` traegt ein Exposure-Argument, weil ein Median
exposure-abhaengiger Groessen selbst exposure-abhaengig ist.**

### AI.2 — ✅ Die Drawdown-Bedingung wirkt genau wie konstruiert

Bei 50 % Exposure:

| Falte | `DD_Benchmark` | `1,25 x` | `DD_Toleranz` | **erlaubt** | wer bindet |
|---|---:|---:|---:|---:|---|
| 2019 | −3,69 % | −4,61 % | −4,33 % | **−4,61 %** | relativ |
| **2020** | −18,93 % | −23,66 % | −4,33 % | **−23,66 %** | relativ |
| 2021 | −2,38 % | −2,98 % | −4,33 % | **−4,33 %** | **`DD_Toleranz`** |
| **2022** | −10,09 % | −12,61 % | −4,33 % | **−12,61 %** | relativ |
| 2023 | −4,33 % | −5,41 % | −4,33 % | **−5,41 %** | relativ |
| 2024 | −3,47 % | −4,34 % | −4,33 % | **−4,34 %** | relativ (knapp) |
| 2025 | −8,89 % | −11,11 % | −4,33 % | **−11,11 %** | relativ |

> **Die Krisenfalten sind die grosszuegigsten des ganzen Plans.** Gebunden wird
> in den **ruhigen** Jahren — und dort erst oberhalb der Rauschgrenze, weil
> `DD_Toleranz` 2021 die relative Grenze abloest. **Genau die Luecke, die
> Festlegung 5 schliessen sollte.**

### AI.3 — Die Zahlen

| | |
|---|---:|
| Rasterzellen dieses Laufs, neun Bots | **2 416** |
| N historisch (Versuchsregister) | 653 |
| **N nominal** | **3 069** |
| Bots mit Zweijahres-Falten | **1** — `elliott_wave`, 26,0 gefundene Trades/Jahr |
| Selektionsfalten je Aktien-Bot | **7** (2019–2025) |
| Bestaetigungsperiode | 2026-01-01 bis Go-Live-Schnitt **2026-09-01**, waechst monatlich |
| Krypto-Faltenplaene | **Platzhalter mit Regel** — haengen an TB-31 |
| Purge = Embargo | **10 bis 134 Tage**, je Bot die maximale gemessene Haltedauer (TB-24) |

### AI.4 — Zwei Wachen haben angeschlagen

**1. Ein Grenzsatz nannte einen Live-Wert.** Der Satz zur Obergrenze der
T3-Laengen enthielt „20-Balken-Spanne"; `t3_supertrend` fuehrt
`ADX_THRESHOLD = 20.0`. Umformuliert zu „Zwanzig-Balken-Spanne".

> *„Die Uebereinstimmung war unschuldig — und deshalb ein guter Beleg, dass die
> Wache etwas tut."*

**2. ⚠️ Die Wache aus TB-29 war falsch gebaut.**
`research/versuchsregister/test_versuchsregister.py` prueft(e), dass `git
status` nichts ausserhalb von `research/` und `docs/` meldet.

> **Das prueft nicht TB-29, sondern den Arbeitsbaum** — und meldete die
> beauftragte Aenderung an `shared/` als TB-29-Verstoss. Umgestellt auf das, was
> TB-29 zugesichert hat: *ein Lauf der Untersuchung veraendert nichts* —
> **beobachtet am Ablauf, nicht am Zustand.**

*Dieselbe Fehlerklasse wie „eine Probe, deren Zustand der Test von Hand
herstellt".*

### AI.5 — Was erstellt wurde

| | |
|---|---|
| **Register** | `docs/VORREGISTRIERUNG_neuselektion.md` |
| **Nulltest** | `docs/VORREGISTRIERUNG_S-E1_nulltest.md` — eigener Eintrag, beide Bedingungen |
| **Eingefrorenes Skript** | `research/vorregistrierung/auswertung.py` — inkl. Beta-Bereinigung und Zufalls-Timing-Test |
| **Vorab-Berechnungen** | `research/vorregistrierung/ergebnisse/` — Messgroessen, Faltenplan, Benchmark-Drawdowns ueber die ganze Exposure-Achse |
| **Wachen** | `pruefe_grenzsaetze.py` (**395** Pruefungen), `registerbericht.py --pruefen`, `herkunft.py` |
| **Tests** | `test_vorregistrierung.py` (150), `shared/test_regimewache.py` (16), `shared/test_agent2_kapitalmass.py` (34) |
| **Bug-Fix AB2/U5** | `shared/regimewache.py` — Entscheidung **abbrechen**, Mechanik fertig; **Einbau an drei Stellen ist TB-30b** |
| **Bug-Fix Agent 2** | `shared/param_search_agent.py` — **dreistufige Zielmass-Kaskade** statt fest verdrahtetem „es gilt das chronologische". **Er schaltet von selbst um**, sobald TB-30b `max_drawdown_kapital_pct` ergaenzt |

### AI.6 — Der Satz, der nicht vergessen werden kann

> **„Dieses Ergebnis ist zulaessig: Es kann sein, dass kein einziger Bot die
> Schwelle erreicht."**

Er steht als Zeichenkette in `registerdaten.py` und wird am Ende **jeder**
Bleibt-Geht-Liste ausgegeben — **auch dann, wenn kein Bot ausscheidet.**

### AI.7 — Was noch fehlt

**Der Betreiber:** signierter GPG-Tag (Testauftrag Schritt 8) und externer
Zeitanker per OpenTimestamps (Schritt 9). `python3
research/vorregistrierung/herkunft.py` meldet den Stand.

**Vor dem Lauf, alles TB-30b:**

| # | |
|---|---|
| 1 | ⚠️ **Regimewache einbauen** — drei Stellen; `regimewache.pruefe_einbau()` meldet den Stand. **Bis dahin darf der Lauf nicht starten** |
| 2 | **`max_drawdown_kapital_pct`** in `evaluate_combination_multi` — dann schaltet Agent 2 von selbst um |
| 3 | **Zwei Achsen durchreichen** — `SMA_TREND_PERIOD` bei `rsi2_mean_reversion`, `BB_SQUEEZE_PERCENTILE`/`BB_LOOKBACK` bei beiden Volatility-Breakout-Bots |
| 4 | **TB-31 abwarten** — ohne zurueckgeladene Krypto-Historie bleiben fuenf Faltenplaene Platzhalter |

### AI.8 — In einfacher Sprache

**Was gemacht wurde:** Alles, was vor dem grossen Auswahllauf feststehen muss,
ist aufgeschrieben — und zwar als **Programm**, das nachher nur noch abliest.

**Die Pruefung, ob es vollstaendig ist:** Das Programm liess sich fertig
schreiben, **ohne ein einziges Ergebnis zu kennen**. An sieben Stellen war
unklar, wie eine Regel gemeint war — die sind jetzt eindeutig.

**Die wichtigste Bestaetigung:** Die Verlustgrenze funktioniert wie gedacht. In
Krisenjahren ist sie grosszuegig, in ruhigen Jahren greift sie — aber erst
oberhalb dessen, was Zufall erklaert.

**Was du noch tun musst:** Zwei Schritte am Mac, die den Stand faelschungssicher
festhalten — eine Signatur und ein externer Zeitstempel.

---

## AJ — TB-31: Krypto-Historie (PR #105, 14.09.2026)

Datenaufgabe. **Kein Bot-Code, keine Parametrisierung, keine Kursdatei
veraendert.** Der Binance-Endpunkt ist aus der Cloud gesperrt (403 der
Egress-Richtlinie) — geliefert sind das geprueft Ladeskript und alle Messungen,
die ohne Endpunkt moeglich waren. **Der Ladelauf ist Schritt 12 des
Testauftrags und gehoert auf den Mac.**

### AJ.1 — ⚠️ Der Befund, der nicht im Auftrag stand: die Tagesdateien sind abgeleitet

> **Alle 24 `*_1d.csv` sind aus den 1h-Daten zusammengerechnet, nicht
> abgerufen.** Nachgewiesen: Der Eroeffnungskurs der ersten Tageskerze ist bei
> **allen 24** auf die letzte Stelle identisch mit dem der ersten Stundenkerze.

**Daraus folgen Teilkerzen, die wie normale Kerzen aussehen:**

| | |
|---|---|
| Die **erste** Tageskerze jeder Datei | deckt **6 bis 16** statt 24 Stunden ab (bei den 13 langen Historien: der 2021-09-01 mit **11** Stunden) |
| Die **letzte** | deckt am 2026-08-31 **13** Stunden ab |
| Bei **23 von 24** Symbolen | enthaelt die letzte 4h-Kerze Kursbewegung, die in der 1h-Datei **fehlt** — die beiden Dateien enden zu **verschiedenen realen Zeitpunkten** |

> **`shared/kursdaten.py` findet das nicht:** Es prueft auf **fehlende** Kurse,
> und eine Teilkerze hat vier gefuellte Kursspalten. **Sie ist nicht leer, sie
> ist falsch.**

⚠️ **Und das ist der Grund, warum es jetzt zaehlt:** *„Solange die Datei dort
beginnt, sitzt die Teilkerze am Rand; wird Historie davorgesetzt, sitzt sie
mitten im Trainingsbereich."*

### AJ.2 — Zwei Korrekturen an den Annahmen des Auftrags

| Annahme | Richtig |
|---|---|
| „Die Krypto-Daten beginnen 09/2021" — gelesen als **Listing-Grenze** | **Es ist der Rand des Fensters** `LOOKBACK = "1825 day ago UTC"` in `shared/fetch_multi_data.py` und `strategies/t3_supertrend/fetch_4h_data.py`. **Die Daten waren nie durch Verfuegbarkeit begrenzt, sondern durch einen Parameter** |
| „Heute blieben **zwei** Testfalten" | **Heute sind es null.** Die zwei ergeben sich bei **zwei** Jahren Mindesttraining; das Register legt **vier** fest. Bleibt nur eine Falte, ist sie nach Regel 7 die **Bestaetigungsperiode** — es wird nichts selektiert |

### AJ.3 — Die Wirkung: von null auf vier Falten

| Bot | Faltenlaenge | heute | nach dem Laden |
|---|---|---:|---:|
| `elliott_wave` | 2 J | **0** | **2** (2022–2023, 2024–2025) |
| `t3_supertrend` | 1 J | **0** | **4** (2022–2025) |
| `rsi2_crypto` | 1 J | **0** | **4** |
| `turtle_soup_crypto` | 1 J | **0** | **4** |
| `volatility_breakout_crypto` | 1 J | **0** | **4** |

`elliott_wave` bleibt bei zwei Falten — **nicht wegen der Daten**, sondern wegen
seiner Zweijahres-Faltenlaenge (26,0 gefundene Trades je Jahr, unter der
30er-Schwelle).

| Marktphase | heute | nach dem Laden |
|---|---|---|
| Zyklus 2018 | fehlt | vorhanden (**nur BTC, ETH, BNB**) |
| Einbruch Maerz 2020 | fehlt | vorhanden |
| Baerenmarkt 2022 | vorhanden | vorhanden |

⚠️ **Beide neuen Phasen liegen im TRAININGS-Bereich, nicht in einer Testfalte**
— die erste Testfalte ist 2022.

### AJ.4 — Die Verzerrung, gemessen

| Selektionsfalte | Symbole in der Falte |
|---|---:|
| **2022** | **3** von 24 |
| 2023 | 6 von 24 |
| 2024 | 9 von 24 |
| 2025 | 13 von 24 |

- **Die frueheste Selektionsfalte wird von drei Coins entschieden** — `BTCUSDT`,
  `ETHUSDT`, `BNBUSDT`.
- ⚠️ **11 von 24 Symbolen kommen in KEINER Selektionsfalte vor**, auch nach dem
  Laden nicht: PROM, SUI, PEPE, WLD, ENA, TRUMP, BMT, PUMP, ZKC, ENSO, U. Das
  fruehste unter ihnen waere erst ab einer Falte **2028** zulaessig.

> Ausgewaehlt wird auf den Paaren, die lange genug gelistet sind und den Zyklus
> 2018 sowie 2022 **ueberlebt** haben; gehandelt wird anschliessend ein
> Universum, das **zur Haelfte** aus Paaren besteht, die in der Auswahl nie
> vorkamen.
>
> **„Mehr Historie macht diese Verzerrung nicht kleiner — sie macht sie
> messbar."**

### AJ.5 — Der Lader

`shared/binance_historie.py`, ausschliesslich
`https://api.binance.com/api/v3/klines`, oeffentlich, **ohne Schluessel** (kein
`/sapi/`, kein `/fapi/`).

| | |
|---|---|
| **Ratenbegrenzung** | Mindestpause 0,25 s, Auswertung von `x-mbx-used-weight-1m`, Pause ab 70 % des Budgets, `429` mit `Retry-After` abwarten, **`418` abbrechen** |
| **Verlaengern statt ueberschreiben** | vorhandene Zeilen als **Rohtext** gelesen und **zeichengleich** zurueckgeschrieben; nur davor kommt etwas dazu |
| **Ueberlappungsbeweis** | Zeile fuer Zeile; **eine Kursabweichung verhindert das Schreiben** |
| **Teilkerzen-Sonderfall** | in der Voreinstellung wird **nicht** geschrieben; `--teilkerze-ersetzen` ersetzt **genau die eine** fuehrende Zeile |
| **Wiederholbar** | beginnt die Datei bereits am Datenbeginn, wird gar nicht geschrieben |

**Geprueft:** `test_binance_historie.py` **75/75** · `test_faltenplan.py`
**38/38** · `probelauf.py --alle` (24 Symbole x 3 Zeitrahmen, echte
Repo-Dateien) **453/453** · `determinismus.py --schnell` **9x DETERMINISTISCH**.

### AJ.6 — In einfacher Sprache

**Was wir wollten:** Mehr Krypto-Historie, damit die Bots genug Zeitraeume zum
Pruefen haben.

**Was dabei herauskam:** Die Daten waren nie knapp — es war eine **Einstellung**,
die fuenf Jahre zurueckblickt und alles davor wegschneidet.

**Der eigentliche Fund:** Die Tagesdateien wurden nie geladen, sondern aus
Stundendaten zusammengerechnet. Dabei sind am Anfang und Ende **halbe Tage**
entstanden, die aussehen wie ganze. Solange sie am Rand sitzen, faellt es nicht
auf. **Sobald man aeltere Daten davorsetzt, sitzen sie mittendrin.**

**Und eine unangenehme Wahrheit:** Selbst mit mehr Historie wird die frueheste
Pruefperiode von **drei** Coins entschieden. Die Haelfte der 24 Paare kommt in
der Auswahl ueberhaupt nicht vor — gehandelt werden sie trotzdem.

### AJ.7 — Offen

| # | Punkt |
|---|---|
| **AJ1** | ⚠️ **Der Ladelauf** — Schritt 12 des Testauftrags, **nur am Mac moeglich** |
| **AJ2** | ⚠️ **Die Teilkerzen entscheiden, bevor geladen wird.** Voreinstellung schreibt nicht; `--teilkerze-ersetzen` ersetzt die fuehrende Zeile. **Ohne Entscheidung sitzt eine falsche Kerze im Trainingsbereich** |
| **AJ3** | **`shared/kursdaten.py` erkennt Teilkerzen nicht** — es prueft auf fehlende Werte. Eine Wache auf **Zeitabdeckung** waere die Ergaenzung |
| **AJ4** | ⚠️ **Die 11 Symbole ohne Selektionsfalte** — eine Entscheidung des Nutzers: im Universum belassen (und wissen, dass sie nie mitgewaehlt wurden) oder herausnehmen |
| **AJ5** | **`LOOKBACK = "1825 day ago UTC"`** in zwei Dateien — nach dem Laden waere es die Grenze, die die neue Historie wieder wegschneidet |

---

## AK — Der Ladelauf am Mac: gestoppt, und warum (14.09.2026)

Fortsetzung von **AJ**. Der Betreiber hat `shared/binance_historie.py` am Mac
ausgefuehrt — der Endpunkt ist von dort erreichbar.

### AK.1 — Die Messung: hinter dem Fensterrand liegt echte Historie

| Symbole | Endpunkt liefert ab |
|---|---|
| **BTC, ETH** | **2017-08-17** — vier Jahre mehr als heute |
| **BNB** | 2017-11-06 |
| **ADA, XRP, TRX** | 2018 |
| **DOGE, LINK, ZEC** | 2019 |
| **SOL, UNI, AAVE, NEAR** | 2020 |
| die uebrigen **11** | stehen bereits auf ihrem **echten Listing-Datum** — `UUSDT` ab 2026-01-13 ist der juengste |

**72 Anfragen, 0 Zwangspausen.** Der Ratenverbrauch ist unproblematisch.

### AK.2 — ⚠️ Der Trockenlauf verweigerte das Schreiben — bei ALLEN 72 Dateien

> `3 harte Abweichung(en) im ueberlappenden Bereich - nicht geschrieben`

**Auch bei Dateien, die gar keine Historie dazubekaemen** (`+ 0 Zeilen`). Die
Sicherung greift, sobald irgendeine Abweichung im gemeinsamen Bereich steht —
und das ist richtig.

**Zwei Gruppen, beide erklaerbar:**

| Wo | Was |
|---|---|
| **2026-08-31 12:00**, alle Symbole und Zeitrahmen | Die **abschliessende Teilkerze**. Die Datei haelt einen abgeschnittenen Tag fest, der Endpunkt liefert den vollstaendigen. `--teilkerze-ersetzen` deckt **nur die fuehrende** ab |
| **2021-09-01, Spalte `open`**, nur die 13 langen `*_1d.csv` | Die **fuehrende Teilkerze**: Die abgeleitete Zeile beginnt um 13:00, die echte Tageskerze um 00:00 — deshalb weicht ausgerechnet `open` ab |

1 772 Volumen-Abweichungen wurden ausdruecklich als **Gleitkomma-Summe**
eingeordnet, kein Befund.

### AK.3 — ⚠️ Die eigentliche Ursache: es gibt keinen Aktualisierungs-Cronjob

Die Crontab (40 Zeilen) enthaelt **keinen** Datenabruf. Gepruefte Folge:

> Die neun `forward_test.py` holen sich ihre Daten **live beim Lauf**. Die
> Dateien unter `data/` werden **nur von Hand** aktualisiert — zuletzt am
> **31.08.2026, mitten am Tag**.
>
> **Jeder Backtest, jede Optimierung und jede Untersuchung rechnet auf Daten,
> die zwei Wochen alt sind und mit einer halben Kerze enden. Und niemand hat es
> gemerkt, weil nichts danach fragt.**

### AK.4 — Ein Nebenbefund: zwei Wege zu denselben Daten

`shared/fetch_multi_data.py` und `strategies/t3_supertrend/fetch_4h_data.py`
nutzen **`python-binance`** (`from binance.client import Client`) — jene
Bibliothek, die fuer die **Bruecke** verworfen wurde (PR #68), weil ihr
`testnet=True` ein Laufzeit-Flag im Aufrufpfad gewesen waere.

Fuer die reine Datenbeschaffung ohne Schluessel ist das weniger kritisch —
**stand aber nirgends**. `shared/binance_historie.py` aus TB-31 nutzt bewusst
nur stdlib. **Es gibt jetzt zwei Wege zu denselben Daten.**

### AK.5 — Was der Betreiber geaendert hat

`LOOKBACK = "1825 day ago UTC"` steht in beiden Dateien jetzt auf
**`"1 Jan, 2017"`**, Kommentare nachgezogen (*„Binance-Start; frueher 1825 Tage,
siehe TB-31"*).

> **Ohne diese Aenderung haette der naechste regulaere Abruf jede neu geladene
> Historie wieder weggeschnitten.** Und der alte Kommentar („5 Jahre, wie
> zuvor") waere dieselbe Fehlerklasse wie in TB-17 gewesen — ein Wert geaendert,
> die Erklaerung daneben stehengelassen.

### AK.6 — In einfacher Sprache

**Was passieren sollte:** Aeltere Krypto-Kurse nachladen, damit die Bots mehr
Zeitraeume zum Pruefen haben.

**Was das Werkzeug gemeldet hat:** Es weigert sich zu schreiben — und zwar bei
**jeder** Datei. Der Grund: Alle Dateien enden mitten in einem Tag. Der
Endpunkt liefert den ganzen Tag, die Datei hat nur ein Stueck davon, und das
sieht wie ein Widerspruch aus.

**Warum das nicht am Werkzeug liegt:** Niemand aktualisiert diese Dateien
regelmaessig. Es gibt keinen automatischen Abruf — die Bots holen ihre Daten
beim Handeln selbst, die gespeicherten Dateien sind nur fuer Auswertungen da.
Zuletzt wurden sie am 31. August von Hand geholt, mittags.

**Was das heisst:** Jede Auswertung der letzten zwei Wochen lief auf
veralteten Daten mit einem halben Tag am Ende. Das faellt nicht auf, weil
nichts danach fragt.

**Was jetzt kommt:** Der Datenbestand wird einmal sauber neu aufgebaut — mit
echten Tageskerzen statt zusammengerechneten —, und es bekommt eine Pruefung,
die halbe Kerzen kuenftig meldet.

### AK.7 — Offen

| # | Punkt |
|---|---|
| **AK1** | **TB-34** — Neuaufbau des Kursdatenbestands mit Sicherung, Vergleich und Teilkerzen-Wache. **Formuliert und uebergeben** |
| **AK2** | ⚠️ **Der Datenstand-Hash der Vorregistrierung aendert sich dadurch.** Er steht auf der Sperrliste — **deshalb muss TB-34 VOR TB-30b laufen**, sonst waere es ein Amendment |
| **AK3** | **Die Faltenplaene aus TB-31 sind danach neu zu rechnen** (`research/krypto_historie/faltenplan.py`) |
| **AK4** | **Zwei Wege zu denselben Daten** — `python-binance` gegen stdlib. Entscheidung, ob das so bleibt |

---

## AL — TB-32: Waechter melden (PR #104, 14.09.2026)

Anlass: Am 14.09. wurden fuenf Cronjobs eingetragen — **und ihre Befunde landeten
in Logdateien, in die niemand sieht.**

### AL.1 — Die Regel in einem Satz

> **Gemeldet wird ein Befund und ein Absturz — geschwiegen wird bei „in Ordnung",
> ausnahmslos, und bei einem unveraenderten Befund, den man schon kennt, bis auf
> eine Erinnerung alle sieben Tage.**

| Rueckgabewert | Ausgang | Folge |
|---|---|---|
| `0` | in Ordnung | **Schweigen**, auch beim ersten Lauf |
| `1` | Befund | melden, gedaempft |
| alles andere | **abgestuerzt** | melden, eigener Kopf `[ABGESTUERZT]` |

> *„Bei einem Befund **weiss** man etwas, bei einem Absturz weiss man
> **nichts**."*

### AL.2 — ⚠️ Der Sonderfall, der sonst durchgerutscht waere

**Ein unbehandelter Python-Fehler endet mit Rueckgabewert 1 — demselben Wert wie
ein Befund.**

Unterschieden wird an der **Fehlerausgabe**: Alle fuenf Werkzeuge drucken die
Traceback eines von *ihnen* gestarteten Unterprozesses in ihre *normale*
Ausgabe. **Eine Traceback in `stderr` bedeutet also, dass das Werkzeug selbst
gestorben ist.**

> **Und es hat sich sofort bewaehrt:** In der Cloud-Umgebung ohne `pandas` stirbt
> `ergebniskurven.py` mit Rueckgabewert 1 — und wird **korrekt als Absturz
> gemeldet, nicht als Befund**.

### AL.3 — ⚠️ Die Entwurfsentscheidung, die ich uebersehen haette

> **Verglichen wird genau das, was gesendet wuerde — nicht die ganze Ausgabe.**
> Alle vier Waechter drucken **Laufzeiten**; ein Fingerabdruck darueber waere
> taeglich ein anderer, und die Daempfung griffe **nie**.
>
> *„Das waere erst nach einer Woche taeglicher Nachrichten aufgefallen."*

### AL.4 — Die Wiederholungsdaempfung

| # | Regel | Entscheidung |
|---|---|---|
| 1 | **neu** — nichts vermerkt | melden |
| 2 | **geaendert** — liest sich anders als zuletzt | melden |
| 3 | **Nachholung** — letzte Meldung ging nicht raus | melden |
| 4 | **Erinnerung** — unveraendert, letzte Meldung ≥ 7 Tage her | melden |
| — | sonst | **schweigen** |

**Sieben Tage**, weil das der groesste Abstand ist, bei dem ein bestehender
Befund in *jeder* Woche mindestens einmal vorkommt — und klein genug fuer
hoechstens rund vier Nachrichten je Waechter und Monat.

### AL.5 — Die harte Bedingung haelt

**Der Rueckgabewert ist immer der des Waechters.** Die Ausgabe geht unveraendert
durch, **bevor** der Meldeteil beginnt; der steht vollstaendig in einem `try`.

Ein Sendefehler wird protokolliert, nicht weitergereicht — **und der Befund gilt
dann als NICHT zugestellt und wird beim naechsten Lauf nachgeholt.**

### AL.6 — Wie eine Nachricht ankommt

```
[BEFUND] Ergebniskurven - neu
Zusammenfassung: 3x ABWEICHEND, 6x AKTUELL
BEFUND: 3 von 9 Kurven passen nicht zur heutigen Konfiguration.
Nachsehen: tail -n 60 ~/trading-bot/logs/system/ergebniskurven.log
```

Drei Teile: **wer**, **was**, **Befehl zum Nachsehen**. Hoechstens zwei Zeilen
aus der Ausgabe; der Rest bleibt im Log.

### AL.7 — Geprueft

`notifications/test_waechter_melden.py` — **149/149**, **kein einziger echter
Telegram-Aufruf** (Sendeweg als Parameter), ohne `pandas`/`numpy` lauffaehig.

**Neun Mutationsproben**, jede mit der Erwartung, **welche Abschnitte anschlagen
muessen — nicht mehr und nicht weniger**: Null-Regel faellt weg · Daempfung faellt
weg · woechentliche Erinnerung faellt weg · fehlgeschlagener Versand gilt als
zugestellt · Absturz wird wie Befund gemeldet · Traceback mit Rueckgabewert 1
gilt als Befund · erst melden, dann das Log schreiben · Sendefehler wird
weitergereicht.

### AL.8 — In einfacher Sprache

**Das Problem:** Seit dem 14.09. laufen fuenf Pruefungen taeglich. Ihre Meldungen
landen in Logdateien, in die niemand sieht.

**Die Loesung:** Ein Zwischenstueck, das die Pruefung startet und bei einem
Befund eine Telegram-Nachricht schickt.

**Die eigentliche Arbeit steckte in der Frage, wann geschwiegen wird.** Eine
taegliche „alles gut"-Nachricht liest nach einer Woche niemand mehr. Also:
Schweigen, wenn alles stimmt. Melden, wenn etwas neu ist oder sich geaendert
hat. Und einmal pro Woche daran erinnern, dass ein bekannter Befund noch
besteht.

**Ein Fall war heikel:** Wenn eine Pruefung selbst abstuerzt, meldet sie danach
nie wieder etwas — und Schweigen sieht von aussen aus wie „alles in Ordnung".
Deshalb gibt es jetzt **drei** Meldungsarten statt zwei.

### AL.9 — Offen

| # | Punkt |
|---|---|
| **AL1** | **Fuenf Crontab-Zeilen ersetzen** — die Waechter laufen bisher direkt, nicht ueber den Wrapper. Zeilen im Testauftrag. **Nur am Mac** |

---

## AM — TB-33: Nulltest S-E1 Turn-of-Month (PR #106, 15.09.2026)

**Gegenstand war nicht die Strategie, sondern der Weg:** Register → Backtest →
Forward-Test ohne Live-Status → Bestaetigungsperiode → Bericht, ohne dass
unterwegs jemand eine Wahl hat.

### AM.1 — Die Pfadfrage: ja, mit einem benannten Befund

**Alle neun Pfadkriterien P1–P9 bestehen maschinell** — `110/110`, Ausgabe
**`WEG SAUBER`**.

An **vier** Stellen musste etwas festgelegt werden, das im TB-30a-Register nicht
stand — **alle vier vor dem Lauf, keine einzige waehrend**:

| | Was fehlte | wer | wann |
|---|---|---|---|
| **A1** | Instrument: SPY statt des `sp500_top150`-Universums | Aufgabenstellung | vor dem ersten Commit |
| **A2** | Sweep-Zellen: −2/+3, −1/+2, −1/+4 + QQQ/IWM/EFA statt „2 bis 6 Tage" | Aufgabenstellung | vor dem ersten Commit |
| **A3** | Bootstrap-Verfahren und Mindest-Ereigniszahl — in TB-30a **gar nicht geregelt** | dieser Lauf | vor dem ersten Commit |
| **A4** | ⚠️ **Faltenzuordnung: zu welchem Jahr gehoert ein Wechsel Dezember→Januar?** | dieser Lauf | beim Schreiben der Auswertung, **vor jeder Rechnung** |

> **A4 ist der eigentliche Befund.** *„Er ist klein und harmlos — und genau die
> Art Luecke, um derentwillen S-E1 gerechnet wird: eine Festlegung, die niemand
> vermisst, bis ein Skript sie braucht. Bei `S-B1` mit neun Bots und 2 416
> Zellen waere sie nicht aufgefallen, sondern stillschweigend im Code getroffen
> worden."*

**Der Weg ist damit nicht durchgefallen** — Pfadkriterium §2 laesst Ergaenzungen
ausdruecklich zu, **solange sie im Register stehen, bevor gerechnet wurde**. Bei
allen vier der Fall.

> **Das ist der Beleg, dass der Nulltest seinen Zweck erfuellt hat.** Er hat vier
> Loecher gefunden, solange sie nichts kosten.

### AM.2 — Ein Strategieergebnis gibt es noch nicht

**yfinance ist aus der Cloud gesperrt** (Proxy antwortet **403**); `scipy` und
die Zeitzone `US/Eastern` fehlen ebenfalls.

Die Auswertung lief deshalb **gegen erzeugte Beispieldaten** — dieselbe
Zusicherung wie in TB-30a: *das Auswertungsskript hat seinen Test bestanden, als
es noch nichts zu deuten gab.* **Die Zahlen sagen nichts ueber SPY.**

Sechs Lagen geprueft, alle korrekt beurteilt:

| Lage (erzeugte Kurse) | B1 | B2 | B3 | Urteil |
|---|:--:|:--:|:--:|---|
| Effekt deutlich vorhanden | ✓ | ✓ | ✓ | `BESTANDEN` |
| Kein Effekt | ✗ | ✗ | ✓ | `DURCHGEFALLEN` |
| Nur der Falten-Median faellt | ✗ | ✓ | ✓ | `DURCHGEFALLEN` |
| Nur das Bootstrap-Intervall faellt | ✓ | ✗ | ✓ | `DURCHGEFALLEN` |
| Nur das Perzentil faellt (reines Beta) | ✓ | ✓ | ✗ | `DURCHGEFALLEN` |
| **Kern faellt, Sweep −2/+3 bestuende** | ✗ | ✗ | ✗ | **`DURCHGEFALLEN`** |

> **Die Sweep-Regel ist strukturell abgesichert, nicht nur getestet:**
> `urteil()` nimmt **nur den Kern** entgegen. Die Variante kann gar nicht
> gewinnen.

### AM.3 — Geprueft

| Zusicherung | |
|---|---|
| Auswertung laeuft **ohne menschliche Entscheidung** durch | ✓ `stdin` geschlossen, `input(` nirgends im Quelltext |
| Sweep-Regel greift | ✓ und **strukturell** |
| **Staging geht in keine Portfolio-Zahl ein** — am Verhalten | ✓ Bot-Liste, Crash-Knopf, Datenbanken, `results/` unveraendert |
| Handelstags-Regel bei Feiertagen und Halbtagen | ✓ 31.12. als Feiertag verschiebt „−1"; Halbtage zaehlen als volle Tage |
| Wiederholbarkeit | ✓ **bitweise**, bei festem Seed aus dem Register |
| Mutationsproben | ✓ **11** plus unveraenderter Vergleichslauf, je eigener Prozess auf denselben Daten |
| `shared/ergebniskurven.py` | ✓ **9x AKTUELL** |

### AM.4 — N-Buchfuehrung

| Register | Beitrag | Begruendung |
|---|---|---|
| **Versuchsregister** | **1 Eintrag**, vorerst „vorgemerkt" | *Ein Versuch ohne Wahl ist trotzdem ein Versuch.* Gebucht, wenn eine Ergebnisdatei ihn belegt — *das Register ist ein Kassenbuch* |
| **DSR** | **kein Beitrag** | Multiplizitaet entsteht, wo unter Alternativen gewaehlt wird. Hier **N = 1** |
| **Sweep-Zellen** | in **keines** von beiden | Robustheit, nicht Auswahl — solange die Sweep-Regel gilt |

### AM.5 — In einfacher Sprache

**Was geprueft wurde:** Nicht ob die Strategie funktioniert, sondern ob der
**Pruefweg** funktioniert — Register schreiben, rechnen, bewerten, ohne dass
unterwegs jemand eine Entscheidung treffen muss.

**Ergebnis: Der Weg laeuft.** Aber er hat eine Luecke gezeigt: An vier Stellen
fehlte im grossen Register eine Festlegung. Eine davon — wie ein Jahreswechsel
zugeordnet wird — haette beim echten Lauf niemand bemerkt. Sie waere einfach im
Code entschieden worden, und niemand haette es gewusst.

**Genau dafuer war der Test da.** Er hat vier Loecher gefunden, solange sie nichts
kosten.

**Was noch fehlt:** Die eigentliche Rechnung auf echten Kursdaten — die geht nur
am Mac.

### AM.5b — Der Datenlauf am Mac (15.09.2026): DURCHGEFALLEN, alle drei Bedingungen

**Daten:** SPY **8 463** Handelstage (rund 33 Jahre), dazu QQQ/IWM/EFA fuer den
Sweep — **0 unvollstaendige Kerzen**.

| Test 1 — der Effekt selbst | SPY −1/+3 |
|---|---|
| Ereignisse | **395** |
| Mittlere **Netto**-Rendite | **−0,0096 %** je Ereignis |
| Bootstrap 95 % | [−0,2179 % ; 0,1946 %] — **umschliesst die Null** |
| Falten-Median | **−0,1921 %** |

| Test 2 — die eingebaute Beta-Kontrolle | |
|---|---|
| Vergleichsfenster | **8 459** moegliche Startdaten, je 4 Handelstage, gleiche Kosten |
| **Perzentil des Kernfensters** | **85,99** (Schwelle 95) |

> **Besser als der Durchschnitt — aber nicht besser als ein beliebiges
> Vier-Tage-Fenster.** Genau das sollte Test 2 feststellen.

**Alle drei Bedingungen gefallen → URTEIL: `DURCHGEFALLEN`.**

**Der Sweep bestaetigt es** (Bild, kein Urteil): keine Variante ueber **92,6**;
`IWM −1/+3` bei **38,5** — bei Nebenwerten existiert der Effekt gar nicht.

| Zelle | N | Mittel % | Perzentil |
|---|---:|---:|---:|
| SPY −2/+3 | 395 | **+0,0860** | 92,62 |
| SPY −1/+2 | 395 | −0,0660 | 85,14 |
| SPY −1/+4 | 395 | +0,0188 | 79,23 |
| QQQ −1/+3 | 322 | +0,0959 | 87,44 |
| **IWM −1/+3** | 308 | **−0,1695** | **38,52** |
| EFA −1/+3 | 293 | −0,0681 | 77,78 |

> ⚠️ **Die Sweep-Regel hat gehalten — und das war der eigentliche Test.**
> `SPY −2/+3` sieht mit **+0,086 %** besser aus als der Kern. Ohne die vorab
> festgelegte Regel waere daraus „die Variante funktioniert" geworden.
> **Sonst sind es acht Versuche und nicht einer.**

**Bestaetigungsperiode**, getrennt ausgewiesen: 8 Ereignisse, Mittel 0,9298 %,
Bootstrap [−0,2777 % ; 2,2614 %] — **zu klein fuer eine Aussage**, und genau
deshalb kein Veto.

**Herkunft protokolliert:** Commit `1650fbf47cd7` (sauber), Daten
`721194d13c41`, Register `b48d40d31e5a`.

> **In einfacher Sprache:** Ein bekannter Kalendereffekt — Aktien steigen
> angeblich rund um den Monatswechsel staerker — **ist nicht mehr da**. Ueber 395
> Monatswechsel seit 1993 verdient das Fenster nach Kosten praktisch nichts.
> *Die Studie, aus der er stammt, endet 2005.*
>
> **Wertvoll ist es trotzdem:** Der Weg hat funktioniert — vorher festgelegt,
> gerechnet, Urteil abgelesen, niemand musste unterwegs entscheiden. Und eine
> Falle wurde abgefangen: Eine Nebenvariante sah besser aus als die
> Hauptvariante, und die Regel hat verhindert, dass man sie nimmt.

### AM.6 — Offen

| # | Punkt |
|---|---|
| **AM1** | **Der Datenlauf am Mac** — Schritt 6 des Testdokuments: `datenlauf.py`, dann `auswertung.py --protokollieren`. Braucht `yfinance`, `scipy`, Zeitzone `US/Eastern` |
| **AM2** | ⚠️ **Die vier Luecken A1–A4 gehoeren ins TB-30a-Register nachgetragen**, bevor TB-30b laeuft — insbesondere **A3** (Bootstrap und Mindest-Ereigniszahl fehlen dort ganz) und **A4** (Faltenzuordnung am Jahreswechsel) |
| **AM3** | Cronjob der Staging-Ebene — Zeile als Vorschlag in `research/turn_of_month/README.md`, **nicht eingetragen** |

---

## AN — TB-34: Kursdaten nativ neu aufgebaut (PR #107, 15.09.2026)

**Der Befund, der die Aufgabe auslöste:** Alle 72 Krypto-Kursdateien endeten mit
einer **Teilkerze**. Die Tagesdateien waren **nicht abgerufen, sondern aus
Stundendaten abgeleitet** — die erste Tageskerze deckte 6 bis 16 statt 24
Stunden ab. Und **kein Cronjob aktualisierte `data/`**: Der Bestand war zwei
Wochen alt.

**Warum es niemand bemerkt hat — das ist die eigentliche Erkenntnis:** Die neun
`forward_test.py` holen ihre Kurse **live beim Lauf** und lesen `data/` nie.
Nach `data/` greifen **101 Module** — Backtests, Optimierer,
`research/`-Untersuchungen —, und keines prüft den Stand.

> **Der Teil des Systems, der täglich läuft, fragt die Daten nie; der Teil, der
> fragt, läuft nur gelegentlich.**

**Ergebnis des Laufs am Mac:** 72 von 72 Dateien neu geladen, **0 Abweichungen
ausserhalb der Ränder**, 85 Randzeilen sämtlich erklärt, **72 laufende Kerzen
strukturell verworfen**. Zweiter Lauf **byteweise identisch**. Sicherung
(53,7 MiB) zurückgespielt **und wieder vorgespielt** — am Verhalten geprüft.
`ergebniskurven.py` meldete **5× ABWEICHEND (Krypto), 4× AKTUELL (Aktien)** —
exakt die Vorhersage; ein ABWEICHEND bei einem Aktien-Bot wäre der Abbruchgrund
gewesen.

**Zugewinn:** 986 070 → **1 368 109 Zeilen (+39 %)**. BTC und ETH ab
**2017-08-17** statt 2021-09-01.

**Datenstand-Hash:** `6258cbc3…` → `d9449faf…` bei **223** Dateien (nach
Entfernen von 19 verwaisten `*_15m.csv`). Als **Tatsachennotiz** eingetragen —
kein Amendment, weil kein Lauf davon berührt war. **Genau dafür kam TB-34 vor
TB-30b.**

**Nebenbefunde:** Keines der acht Abrufskripte schloss die laufende Kerze aus,
alle überschrieben vollständig ⇒ **der Neuaufbau war nicht haltbar** (→ AO).
Echte Datenlücke: 13 Krypto-1h-Dateien fehlen drei Stunden ab **2021-09-29**.

### In einfacher Sprache

*Was wir wissen wollten:* Ob die Kursdaten, auf denen alles rechnet, in Ordnung
sind. *Was herauskam:* Nein — sie endeten mit halben Kerzen, die Tagesdaten
waren zusammengerechnet statt abgeholt, und der Bestand war zwei Wochen alt.
*Warum es niemand merkte:* Die täglich laufenden Bots schauen in diese Dateien
gar nicht hinein. *Was das bedeutet:* Der Bestand ist jetzt sauber und 40
Prozent länger; alle daraus abgeleiteten Kennzahlen ändern sich, und das ist
richtig so.

---

## AO — TB-35: Abrufskripte haltbar gemacht (PR #108, 15.09.2026)

**Acht von acht Abrufskripten geändert.** Die laufende Kerze entsteht in der
Datei gar nicht erst; die beiden mitwandernden Zeitfenster (`3650 day ago UTC`)
sind weg; eine Wache meldet, wenn ein Abruf eine Datei **kürzer** zurücklässt.

**Zwei Entwurfsentscheidungen mit Begründung:**

**Überschreiben bleibt.** *Ein anhängendes Werkzeug, das sich irrt, lässt den
Fehler dauerhaft stehen; ein überschreibendes ist beim nächsten Lauf wieder
sauber.* Dazu: Anhängen bräuchte eine **unentscheidbare Konfliktregel** — was
gilt, wenn der Endpunkt eine gespeicherte Kerze anders liefert als beim letzten
Mal?

**Kein Börsenkalender bei den Aktien**, und die Begründung ist die beste Stelle
des Dokuments: *Ein Börsenkalender beantwortet „ist die Börse jetzt offen?" —
eine Frage mit **zwei** teuren Fehlerrichtungen. Der Abrufschutz beantwortet
„ist dieser Zeitraum sicher vorbei?" — **eine** Richtung, und zu spät „ja" zu
sagen kostet nichts.* `D+1 00:00 UTC` liegt beweisbar nach jedem NYSE-Schluss.

**Der Mac-Lauf** bestätigte: Krypto-Abruf **0 abweichende Zeilen**, laufende
Tageskerze korrekt verworfen, Wache mit vier Befunden nach künstlicher
Verkürzung, Datenstand vor = nach.

**⚠️ Der Befund des Laufs: yfinance liefert keine reproduzierbaren Kursdaten.**
Beim echten Aktien-Abruf wichen **9 766 von rund 11 000** Bestandszeilen ab
(AAPL), maximal **1,2 × 10⁻⁶** relativ, **ausschliesslich vor dem letzten
Ex-Dividenden-Tag**. Ursache: `auto_adjust=True`, schwankende Rundung des
Bereinigungsfaktors. **Zwei Läufe im Abstand von Minuten ergaben verschieden
viele abweichende Zeilen** (9 766 → 9 746).

> **Bereinigte Aktienkurse sind veränderliche Geschichte.** Ein Hash über
> yfinance-Dateien kann **konstruktionsbedingt** nicht stabil sein; Runden beim
> Schreiben beseitigt nur das Rauschen, nicht die legitime Neuskalierung bei
> jeder Dividende.

**Nebenbefund N1**, der grösser war als die Aufgabe: **Die fünf Krypto-Bots
entscheiden auf der laufenden Kerze** (`df.iloc[-1]`) — der Backtest rechnet auf
abgeschlossenen (→ AR).

### In einfacher Sprache

*Was wir wissen wollten:* Ob sich die Abrufprogramme so umbauen lassen, dass sie
den neu geladenen Bestand nicht wieder verderben. *Was herauskam:* Ja, alle
acht. *Der unbestellte Fund:* Der Aktien-Datenanbieter liefert bei jedem Abruf
minimal andere Zahlen — weil bei jeder Dividende die gesamte Kursgeschichte
rückwirkend umgerechnet wird und dabei jedes Mal etwas anders gerundet wird.
*Was das bedeutet:* Der Fingerabdruck des Datenstands funktioniert bei Krypto,
bei Aktien nicht. Das gehört ins Register, sonst sieht es später wie ein
gebrochenes Versprechen aus.

---

## AP — TB-36: Faltenplan für alle neun Bots und Registernachtrag (PR #109, 15.09.2026)

**Die Gegenprobe war richtig gebaut:** Verglichen wurde nicht die **Anzahl**,
sondern die **Symbolliste je Falte, namentlich**, und beide Werkzeuge liefen als
eigener Prozess. *Eine Gegenprobe, die nur Zahlen vergleicht, hätte zwei
verschiedene Listen gleicher Länge nicht bemerkt.*

**Ergebnis:** Aktien **7 Selektionsfalten** 2019–2025, Symbole
140/142/145/147/148/148/149, Bestätigung 150. Kein Bot unterbestimmt —
`elliott_wave` erreicht mit drei Doppeljahr-Falten die Schwelle genau.

**Embargo je Bot:** 11 bis 16 Handelstage, ausser `elliott_wave_stocks` mit
**91**. `MAX_HOLD_HOURS = 90` wird dort als **90 Tagesbalken** gelesen — **kein
Einheitenfehler**, der Kommentar sagt es ausdrücklich, und `forward_test.py`
verweist darauf. ⚠️ **Folge: Die Bestätigungsperiode beginnt für diesen Bot rund
vier Monate später als für die anderen acht.**

**Das Register:** Abschnitt 15 neu, **null entfernte Zeilen**, vier Verweise im
alten Text.

**Zwei Fehler in der Aufgabenstellung, von der Sitzung gefunden statt
stillschweigend gelöst:** „AF.2 Nr. 6" existiert im Repo nicht (die
Doppeljahr-Regel steht in 5.1 Nr. 6). Und drei als „ersetzt" ausgewiesene
Fassungen hatten **nie im Register gestanden** — sie stammten aus
Beratungsrunden und sind Erstfassungen.

**Der Mac-Lauf** bestätigte alle zehn Schritte, und die Sitzung bemerkte
selbst, dass der Zweig bereits gemergt war — `git diff origin/main` musste leer
sein — und prüfte zusätzlich gegen `e23e38f^1`. **Ohne diesen Hinweis wäre ein
leerer Diff als bestandene Prüfung durchgegangen** (→ AU, wo genau das später
zum dritten Mal auftrat).

### In einfacher Sprache

*Was wir wissen wollten:* In welche Zeitabschnitte die Vergangenheit zerlegt
wird, welche Wertpapiere in jedem vorkommen, und wie lange nach dem Stichtag
gewartet wird. *Was herauskam:* Acht Bots bekommen sieben Abschnitte, einer drei.
*Die Auffälligkeit:* Ein Aktien-Bot hat 91 Tage Wartezeit statt 11 bis 16 — wegen
einer Einstellung, deren Name „Stunden" sagt und die als „Tage" verwendet wird.
Das ist so gewollt, hat aber zur Folge, dass seine Prüfphase Monate später
beginnt.

---

## AQ — TB-37: Zugangsdaten getrennt (PR #110, 15.09.2026)

**Der Befund:** `shared/fetch_binance_data.py` lag **in keinem Commit, in keinem
Zweig, auf keinem Server** — nur auf dem MacBook. **Neun Module hingen daran,
fünf im täglichen Betrieb.**

**Ergebnis:** Code versioniert, Schlüssel aus der Umgebung. ⭐ **Kein einziger
Aufrufer musste geändert werden** — die Signatur wurde über den **Syntaxbaum**
der neun Aufrufer erschlossen, nicht gesetzt. **Ersetzung statt zweiter Datei**,
weil die neun sie als Top-Level-Modul binden und eine zweite niemand gefunden
hätte.

**Fehlender Schlüssel:** läuft weiter, meldet sich **einmal** nach `stderr`,
liefert **nie still leer** — `AbrufLeer` wird geworfen, *denn ein leeres
Ergebnis sieht im Bot aus wie „kein Signal"*.

**⚠️ Zwei Befunde, die grösser sind als die Aufgabe:**

**`git pull` überschreibt eine gitignorierte Datei kommentarlos** — gemessen,
nicht vermutet. Fügt ein Commit eine Datei an einem Pfad hinzu, an dem lokal
eine gitignorierte liegt, ersetzt der Pull sie ohne Rückfrage. **Beim Lauf am
Mac ist genau das passiert**, und nur die vorher angelegte Sicherung hat die
Datei gerettet.

**`*.db` ist gitignoriert — die Handelsdatenbanken aller neun Bots.** Der
gesamte Forward-Test-Verlauf, **nicht neu berechenbar**: Die Signale entstanden
zu Zeitpunkten, die vorbei sind. ⚠️ **Seit der Verfahren-B-Festlegung ist genau
das der einzige Vermögenswert des Projekts.**

**Und eine Korrektur:** Die Datei enthielt **nie** Zugangsdaten — nur
`Client()` ohne Argumente. Der `grep -c`-Treffer von 2 war ein Fehlalarm. **TB-37
war trotzdem richtig, aber aus dem anderen der beiden Gründe.** ⚠️
`broker/zugang.py:101` und das Übergabeprotokoll **beschreiben sie weiterhin als
schlüsseltragend** — eine dokumentierte Annahme, die nie geprüft wurde und der
wir einen halben Tag gefolgt sind.

⭐ **Die Verwechslungssperre in `broker/zugang.py` konnte deshalb nie greifen:**
Sie prüft, ob ein Testnet-Schlüssel mit einem Produktivschlüssel übereinstimmt —
aber die Schlüssel standen in einer Python-Datei, nicht in der Umgebung.

### In einfacher Sprache

*Was wir wissen wollten:* Wie man eine Datei absichert, die es nur einmal gibt.
*Was herauskam:* Das Programm liegt jetzt im Sicherungssystem, die Passwörter
nicht — und es stellte sich heraus, dass gar keine darin standen. *Der wichtigere
Fund:* Die Aufzeichnungen **aller Testgeschäfte seit Beginn** liegen ebenfalls
nur auf dem MacBook und lassen sich nicht neu berechnen. Nach dem, was seither
festgelegt wurde, sind genau diese Aufzeichnungen die einzige unabhängige
Grundlage der Dezember-Entscheidung.

---

## AR — TB-38: Die gemeinsame Abrufschicht (PR #111, 16.09.2026)

**Die erste Aufgabe, die `forward_test.py` ändern durfte** — mit ausdrücklicher
Freigabe, und nur für den Datenbezug.

**Die Regel, in einem Satz:** *Entscheidungskerze ist die letzte Kerze, deren
`close_time` vor der Startzeit des Laufs liegt.* Als Filter in **einer**
gemeinsamen Funktion, die Backtest **und** Forward-Test benutzen — *fünf Stellen
mit `iloc[-2]` sind fünf Stellen, an denen es beim nächsten Cron-Zeitwechsel
wieder kippt.*

⭐ **Der Nachweis, der zählt:** Dieselben dreizehn Prüfungen liefen gegen die
**unveränderten** Bots von `main` — **sieben fielen durch**. `t3_supertrend`
schloss dort eine Position als `stop_loss` mit Ausstiegszeit
`2026-09-15 20:00:00`, **der laufenden Kerze**. *Das ist der Unterschied
zwischen „die Tests bestehen" und „die Tests würden den Fehler finden".*

**Die Aktien-Bots als Gegenprobe:** Sie nehmen nach der Umstellung **dieselbe**
Kerze wie vorher. Hätte die Sitzung die konservative `23:59:59`-Schranke aus
`abrufschutz` benutzt, wären alle vier auf die Kerze von **gestern** gefallen —
jedes Signal einen Handelstag zu spät. ⭐ **Die Abwägung dahinter:**
*`abrufschutz` schützt den **Schreib**pfad, zu langes Warten kostet nichts.
Diese Schicht schützt den **Lese**pfad, zu langes Warten kostet einen
Handelstag. Zwei entgegengesetzte Risikoprofile gehören nicht in eine Datei.*

**Diff je `forward_test.py`: +14/−1 bzw. +15/−1**, davon neun Kommentarzeilen.

**Der Mac-Lauf:** Der produktive Pfad ist **einmal real durchlaufen** — Cron →
Abrufschicht → 24 Rückfall-Zeilen → je eine Kerze verworfen → Telegram → kein
Traceback. Neun Datenbanken gesichert und hinterher **byteweise identisch**.

> **Umstellungszeitpunkt: `2026-09-16T04:42:24Z`, alle neun Bots.** Er liegt
> **nach** dem 06:00-Cronlauf auf altem Code (folgenlos) und **vor** dem
> 07:00-Lauf über die neue Schicht. Ab hier läuft das einzige Vergleichsfenster
> Backtest gegen Live.

⚠️ **Papierpfade vor diesem Tag gelten für den Vergleich als nicht
vergleichbar.**

**Eine Richtigstellung, die hierher gehört:** Die Angabe, der Cron laufe „zur
Minute 5 nach der Vier-Stunden-Grenze", die Teilkerze sei also **fünf Minuten**
alt, **war falsch**. `5 */4` ist die **Broker-Brücke**; der Bot steht auf
`0 */4`, und weil Cron in **Ortszeit** zündet, trifft er UTC 22/02/06/… statt
des UTC-Rasters. **Die Kerze war zwei bis drei Stunden alt, also zu 50–75 %
gefüllt.** Die Schlussfolgerung überlebt — halbfertig ist halbfertig —, die
Grössenordnung nicht.

### In einfacher Sprache

*Was wir wissen wollten:* Fünf Bots entschieden auf einem Zeitabschnitt, der noch
nicht zu Ende war, der Test der Vergangenheit dagegen auf fertigen. *Was
herauskam:* Alle neun schauen jetzt auf fertige Abschnitte, und der erste echte
automatische Lauf über den neuen Weg hat fehlerfrei funktioniert. *Was es kostet:*
Der bisherige Echtbetrieb der fünf zählt ab dem Umstellungstag nicht mehr als
Vergleichsgrundlage — er beschreibt eine Strategie, die es im Test nicht gibt.

---

## AS — TB-39: `S-B1` vorbereitet (PR #112, 16.09.2026)

**Vorbereitung ohne Backtest**, weil Vorgezogenes nichts auswählen darf.

⭐ **Die Sitzung hat sich an der Kernfrage geweigert zu raten:** yfinance ist aus
der Cloud gesperrt, die Historienfrage blieb deshalb **ungemessen** — die
Erwartung (12 von 14 Instrumenten ab 2008) ist ausdrücklich als Kenntnisstand
markiert, nicht als Messung.

**Eine Falle, die sie benannt hat:** *„Historie bis 2007" und „Signal ab 2008"
sind nicht dasselbe.* Ein ETF braucht **252 Handelstage Vorlauf** für ein
Zwölf-Monats-Signal.

**N = 5.** Nur der Volatilitäts-Rückblick ist offen. Die drei Signalfenster ins
Raster zu stellen hätte **Faktor 64** gekostet — *und die Herkunft „aus der
Literatur" gleich mit.*

**Die Kostenrechnung, die eine Sorge auflöste:** `Jahresumschlag = n · w · (1/n)
= w` — **die Instrumentenzahl kürzt sich heraus.** Umgeschlagen wird nur, **was
kippt**: 0,15 bis 0,90 pp im Jahr, obere Schranke 1,80 — *halb so viel wie die
Hürde, an der `S-E2` scheiterte.*

**Drei Entscheidungen mit Begründung:** `auto_adjust = True`, **weil
Anleihe-ETFs auf unbereinigten Reihen strukturell negatives
Zwölf-Monats-Momentum hätten** — die Strategie hätte Anleihen aus einem
Buchhaltungsgrund gemieden. Die Dateien werden **eingefroren mit SHA-256 je
Datei**, statt die Nicht-Wiederholbarkeit wegzuargumentieren. Und der
**Benchmark ist dasselbe Buch ohne Signal** — *alles ausser dem Timing kürzt
sich heraus, und das Timing ist das Einzige, was `S-B1` hinzufügt.*

**⚠️ Ein Befund über uns:** Die **Budgetstufen-Leiter stand nirgends im Repo** —
sie kam aus einer Beratungsrunde **nach** TB-36. Die Sitzung musste sie
**nachbauen** und schrieb korrekt dazu, dass die Betreiberfassung gilt.
*Systemisch: Jede Aufgabe, die sie nicht vorfindet, rät sie neu — und jede rät
anders.*

**⚠️ Und die Aufgabe selbst war auf Sand gebaut:** Alle vierzehn Instrumente sind
**US-domiziliert** und für einen EU-Privatanleger wegen fehlendem
PRIIPs-Basisinformationsblatt **nicht handelbar** (→ AV).

### In einfacher Sprache

*Was wir wissen wollten:* Reicht die Kursgeschichte weit genug zurück, wie viele
Varianten werden ausprobiert, und was frisst die Gebühr? *Was herauskam:* Die
Kursfrage ist noch offen — die Sitzung hat **nicht geschätzt**, sondern das
Werkzeug gebaut und die Messung auf den Mac verlegt. Varianten: fünf, bewusst
wenig. Gebühren: deutlich weniger als befürchtet, weil nur umgeschichtet wird,
was sich ändert. *Der Haken:* Keiner der vierzehn Fonds ist in der EU für
Privatanleger kaufbar.

---

## AT — TB-40: Universum-Trockenlauf (PR #113, 16.09.2026)

**Auslöser:** Bei einer Laufzeitmessung meldete der Bot-Loader beiläufig, dass
er **vier Symbole überspringt** — `MIN_HISTORY_DAYS = 500`, geladen werden
**20 von 24**. Im Register standen andere Zahlen.

⭐ **Die Klemme elegant aufgelöst:** Die Aufgabe verlangte zugleich *„der
Laufcode entscheidet"* und *„Bot-Dateien werden nie importiert"* — beides
zusammen geht nicht. **Lösung: Import ja, aber in einem eigenen Prozess je
Bot.** *Nicht weil jemand aufpasst, sondern weil jeder Prozess seinen eigenen
`sys.modules` hat.* Strenger als jede Namensvergabe.

**Ergebnis: acht der neun eingetragenen Zahlenreihen sind falsch, alle zu hoch.**
Nur `elliott_wave` stimmt. ⭐ **Es kommt nirgends ein Symbol hinzu — der Loader
ist überall strenger: F ⊆ H ⊆ A.**

**⚠️ Ein Widerspruch in der Aufgabenstellung, von der Sitzung gemessen statt
aufgelöst:** Registertext 3b sagt **H** („an mindestens einem Handelstag der
Falte handelbar"), die Aufgabe verlangte **F** („am Faltenbeginn geprüft").
**Unter F verliert `elliott_wave` seine erste Falte und steht bei 2 von 3 —
„unterbestimmt", Schatten ausserhalb des Buchs.**

> **Entscheidung: H.** Nicht weil H sachlich besser wäre, sondern weil **H
> registriert war** und die Wirkung von F zum Entscheidungszeitpunkt **bekannt**
> war. *Eine Wahl nach dem Ergebnis wurde bewusst vermieden — und sie hätte
> ausgerechnet den Bot mit dem schwächsten Prior getroffen.*
>
> **Und H ist zusätzlich in der Sache richtig:** F beschreibt eine Strategie, die
> der Bot nicht handelt — ein Symbol, das im März handelbar wird, wird ab März
> gehandelt; F würde es für das ganze Jahr streichen.

**Zwei Befunde über den Code:**

**`MIN_HISTORY_*` ist nicht eine Zahl, sondern vier** — 17 520 (Kerzen) · 730 ·
500 · 1 825 (Tage). ⚠️ **`elliott_wave` zählt Kerzen, die anderen acht messen
Zeitspanne.** Eine Reihe mit gleicher Spanne, aber **Lücken**, fällt nur bei ihm
heraus.

**⚠️ Drei Bots sortieren völlig lautlos aus.** `rsi2_mean_reversion`,
`turtle_soup_stocks` und `volatility_breakout` schreiben bei zu kurzer Historie
**und bei fehlender Kursdatei keine einzige Zeile**. *Der Befund, der diesen
Trockenlauf ausgelöst hat, war nur sichtbar, weil `rsi2_crypto` ihn meldet.*

### In einfacher Sprache

*Was geprüft wurde:* Ob die Zahlen im Vorab-Dokument stimmen — wie viele Werte in
jedem Prüfzeitraum tatsächlich mitgerechnet werden. *Was herauskam:* Acht von
neun Reihen sind zu hoch. Zwei Programme beantworteten dieselbe Frage: eines
fragt „gibt es Kursdaten?", das andere strenger „gibt es genug?". *Die
Entscheidung:* Es gibt zwei vertretbare Auslegungen, und der Unterschied
entscheidet, ob ein Bot überhaupt neu eingestellt wird. Gewählt wurde die, die
schon im Dokument stand — **weil wir inzwischen wussten, was die andere bewirkt.**

---

## AU — TB-41: Der grosse Registernachtrag (PR #114, 16.09.2026)

**Zehn Registerblöcke**, fünf davon ersetzt und als ersetzt gekennzeichnet:
**5** (zwei Datenbestände, `TZ=UTC`), **6** (Budgetstufen, Zellenbudget,
Klassenschlüssel 80/20), **7** (Backtester-Prüfung), **2d** (Embargo als
Ablesung am Buch), **3b (a)–(e)**, **Kandidatenregeln**, **Vorab-Filter**,
**Short-Vorbedingung**, **`S-B1`-Proxy-Tabelle**.

⭐ **Null entfernte Zeilen** — `git diff --numstat`: `655 0` und `85 0`.

⭐ **Die Symbolzahlen wurden von zwei getrennten Parsern auf zwei Dateien
maschinell verglichen, nicht abgetippt**; die `MIN_HISTORY_*`-Werte aus den
Bot-Dateien **gelesen**. **Genau deshalb fiel ein vierter Fehler auf:** „die
**fünf** Werte" — es sind **vier**; drei Krypto-Bots teilen sich die 500.
*Gruppen gezählt statt Werte.*

**Elf Stellen, an denen Registertext und Umsetzung auseinanderfallen**, in
16.11 einzeln benannt. *Ein Register, das etwas beschreibt, das der Code noch
nicht kann, ist in Ordnung — solange es benannt ist.*

**Der Mac-Lauf brachte drei Werkzeugfehler ans Licht:**

**`loaderlauf.py` läuft auf dem Mac gar nicht.** Der Schreibschutz ersetzt
`builtins.open` durch `wach_open(datei, modus="r", *a, **k)`; wird
`open(pfad, mode="rb")` mit **Schlüsselwort** aufgerufen, landet `mode` in
`**k` und wird **doppelt** übergeben. *Ein Schreibschutz, der an einem
Leseversuch scheitert.* In der Cloud unsichtbar.

**⚠️ Die Wache gegen gelöschte Registerzeilen ist nach jedem Merge trivial
grün** — `origin/main` als Standardwert, Diff leer, `numstat: []`, Prüfung
meldet Erfolg. **Zum dritten Mal in drei Tagen derselbe Mechanismus** (AP, AT,
AU). ⭐ **Gefunden nur durch den Selbsttest B2 — „der Diff wurde tatsächlich
ausgewertet".**

**Und die TB-40-Vergleichstabelle zeigt weiter auf den historischen Stand** und
meldet acht längst korrigierte Abweichungen.

> **Drei Prüfungen, die aufhören zu prüfen, ohne es zu sagen** — dieselbe
> Familie wie die drei lautlos aussortierenden Bots.

**Die Kernfrage ist trotzdem beantwortet:** Die eingetragenen Symbolzahlen
stimmen auch mit einer **frischen Messung auf dem Mac** — allerdings über eine
Diagnose-Kopie ausserhalb des Repos mit drei geänderten Zeilen. **Die Zahlen
sind belegt, das Werkzeug nicht.**

### In einfacher Sprache

*Was gemacht wurde:* Das Vorab-Dokument ist vollständig — zehn neue Regelblöcke,
vier falsche Angaben korrigiert, **keine einzige Zeile gelöscht**. *Was der
Durchlauf am Mac zeigte:* Die Zahlen stimmen auch mit echten Daten. Aber drei
Prüfprogramme hören auf zu prüfen, ohne es zu sagen — eines läuft gar nicht,
eines vergleicht nach dem Zusammenführen mit sich selbst, eines schaut auf eine
veraltete Tabelle. *Warum das zählt:* Eine Prüfung, die nichts mehr prüft, ist
schlimmer als keine — weil man sich auf sie verlässt.

---

## AV — Sechs Beratungsrunden (Fable, 15./16.09.2026)

### AV.1 — Verfahren B statt A

Die Vorabfestlegung vom 14.09. enthielt **zwei sich ausschliessende Verfahren**
nebeneinander. **Es gilt B:** eine **einmalige** Auswahl über das ganze Raster,
Gewinner nach Faltenmedian, **kein Trainingsfenster**, N = Rastergrösse.

**Die Begründung:** Unter A gäbe es je Falte einen Gewinner, und die Regel,
welcher live geht, schaut praktisch immer auf die OOS-Ergebnisse. **Damit wäre
die Endauswahl wieder In-Sample.**

**Folgen:** Die Frage nach dem Mindesttraining löst sich auf. Die
Faltenzuordnung vereinfacht sich, weil das Objekt der **Kapitalpfad** ist und
nie eine Trade-Liste. **Und die sechs bot-eigenen Walk-Forward-Rechner werden
ersetzt, nicht umgestellt.**

### AV.2 — Die Asymmetrie

> **In-Sample kann ausschliessen. Nur Out-of-Sample kann bestätigen.**

Die Vielfachheit hat eine **Richtung**: Sie lässt Zufall wie Können aussehen,
nie Können wie Zufall. **Ein Parametersatz, der selbst als bester von 653 die
vorab festgelegten Kriterien reisst, ist kein Pech, sondern ein Befund.**
Umgekehrt gilt es nicht: Bestehen heisst **nicht widerlegt**, nicht **trägt**.

**Daraus: Im Dezember entscheidbar** sind Ausschlüsse, Parametersatz und
Grundbudget für alle Nicht-Ausgeschiedenen. **Nicht entscheidbar:** „ist ein
Verdiener", mehr als Grundbudget, Echtgeld.

**Und der Prior ist bereits verbraucht** — er steckt im Benchmark, gegen den
Rang 3 misst. Ihn zusätzlich als Zulassungshürde anzulegen hiesse, eine
Schwelle zu setzen, während man weiss, wen sie trifft. **`elliott_wave` bekommt
dieselben Kriterien wie RSI-2.**

### AV.3 — Die Zellen-Landkarte

**Diversifikation hat zwei Achsen: Quelle × Anlage. Der Horizont ist keine**
(0,32 × — eigene Messung). *Zwei Trendfolger auf Aktien steigen gemeinsam ein;
ein Trendfolger auf Aktien und einer auf Anleihen nicht.*

**Neun Bots besetzen vier Zellen**, zwei davon dreifach. ⇒ **Budget gehört an
die Zelle, nicht an den Bot.** Nach heutiger Regel bekämen die Umkehr-Zellen
zusammen **zwei Drittel** des Buchs.

**Der Rahmen hat sieben Zellen**, drei erreichbar: `S-B1`, `S-D1`, Carry.
**Danach wiederholt auf OHLCV long-only alles eine vorhandene Wette.**

⭐ **Vorab-Filter ohne N-Kosten:** Ko-Einstiegsquote der Signale gegen jeden Bot
derselben Anlage — **über 1,5 ⇒ gleiche Zelle ⇒ Variante, kein Kandidat.**

### AV.4 — Die Regeln, die N klein halten

**Kandidaten werden nie gegeneinander gerankt**; Zulassung ist absolut, **gegen
die Null** — das Buch ohne diesen Kandidaten. *Die Null ist kein Kandidat,
sondern der Vergleich, den jeder Kandidat hat.* **N ist die Rastergrösse ⇒ neue
Kandidaten bekommen kein Raster** (N = 1). **Familienbuchführung** im Register.
**Overlay-Kandidaten erst nach dem Selektionslauf** — *gestapelte Selektion.*

### AV.5 — Was die Leiter bewegt

> **Die Leiter bewegt Bots. Sie bewegt keine Zellen.**

OOS-Evidenz über einen Bot ist Evidenz über eine **Implementierung**. **Fällt
ein Bot auf Schatten, bleibt sein Geld in seiner Zelle;** wird die Zelle leer,
geht es in die statische Benchmark — **nicht an eine andere Zelle.** *Sonst
würde ein Bot für das Versagen eines anderen bestraft, und das Kapital ginge
dorthin, wo es zufällig besser lief.*

### AV.6 — Regimeabhängige Umschaltung: nicht registrierbar

> **Die Historie enthält vielleicht acht Regimewechsel. Eine Regel, die aus acht
> Beobachtungen lernt, welche von zwei Quellen als Nächstes verdient, hat acht
> Datenpunkte für eine Frage, für die die Literatur mit Jahrzehnten keine
> belastbare Antwort hat.**

**Und gegen die Idee selbst:** Trend **und** kurzfristige Umkehr verdienen beide
in Hochvolatilitätsphasen mehr — *sie mögen dieselben Phasen und lassen sich
nicht gegeneinander timen.*

**Ein Sprachmodell im Entscheidungspfad: nie** — nicht reproduzierbar, nicht
falsifizierbar, und es bricht die Regel, dass kein Agent einen Trade oder eine
Grösse auslöst.

⭐ **Der konstruktive Kern: regimeabhängige Berichterstattung.** Die Leiter weist
je Zelle aus, in welchem Regime sie verdient. **Ein informativer Agent darf das
beschreiben — er darf nur nichts daraus tun.** *Nach zwei, drei Jahren ist das
der Bericht, aus dem sich sagen liesse, ob Umschalten je etwas gebracht hätte —
mit Etiketten, die beim Entstehen protokolliert werden statt rückblickend.*

### AV.7 — Die ehrliche Einordnung

**Geduld** trägt — aber **nur in den Fortsetzungs- und Beta-Zellen**, wo man für
Drawdowns bezahlt wird, die Institutionen wegen Mandaten nicht halten können.
**Nicht in den Umkehr-Zellen:**

> **Kurzfristige Umkehr auf Tageskerzen ist ein Wettlauf gegen Teilnehmer, die
> dieselbe Umkehr in Minuten handeln. Wer den Schluss t+1 bekommt und 0,30 pp
> zahlt, ist die langsame Partei.**

⚠️ **Sechs von neun Bots sitzen dort.** Einem davon wird ein Vorteil zugetraut.
**Kapazität — der einzige strukturelle Vorteil der Kleinheit — ist wegdefiniert**,
weil das Universum aus den liquidesten Instrumenten der Welt besteht.

**Der Name für das, was übrig bleibt: „Risikoprämien-Ernte mit Timing",
Erwartung netto Sharpe 0,3 bis 0,7** — ausdrücklich als Einschätzung markiert.

### In einfacher Sprache

*Worum es ging:* Nach welchen Regeln im Dezember entschieden wird — und was
überhaupt entschieden werden darf. *Der wichtigste Satz:* Aus den vorhandenen
Daten kann man **ausschliessen**, aber nicht **bestätigen**. Scheitert ein Bot an
vorher festgelegten Anforderungen, ist das ein echtes Ergebnis; besteht er sie,
heisst das nur, dass er nicht widerlegt wurde. *Die praktischste Erkenntnis:*
Neun Bots sind in Wahrheit vier verschiedene Wetten — also wird das Geld auf die
Wetten verteilt, nicht auf die Bots. *Die unbequemste:* Sechs der neun setzen
darauf, dass sich Kurse schnell drehen — und dabei konkurriert man mit Leuten,
die dasselbe in Minuten handeln.

---

## AW — Zwei Messungen des Betreibers (16.09.2026)

### AW.1 — Die Laufzeit des Selektionslaufs: Stunden, nicht Wochen

**0,19 s je Kombination** (20 Symbole, 42 848 Zeilen), dreimal gemessen, keine
Ausreisser. Nach Zeilenzahl gewichtet — `elliott_wave` 1h ≈ 24 ×,
`t3_supertrend` 4h ≈ 6 ×, vier Aktien-Bots je ≈ 7,5 × wegen 150 statt 20
Symbolen — ergibt **rund 2 Stunden Kern, mit Bootstrap und Reserve 3 bis 5
Stunden.**

> **Selbst bei einem Irrtum um den Faktor zehn ist es ein Tag.** Die grösste
> Unbekannte im Zeitplan ist damit erledigt.

**Und der Nebenbefund dieser Messung löste TB-40 aus** (→ AT).

### AW.2 — Der Aktien/Krypto-Schlüssel

Gemessen auf **2 271 gemeinsamen Handelstagen** (2017-08-18 bis 2026-09-01),
23 Krypto- und 150 Aktienreihen, gleichgewichtet:

| | |
|---|---:|
| Jahresschwankung **Krypto** | **74,7 %** |
| Jahresschwankung **Aktien** | **19,6 %** |
| **Verhältnis** | **3,82 ×** |
| Korrelation | **0,32** |
| Grösster Rückgang Krypto / Aktien | **−82,3 %** / −35,7 % |

**⚠️ Bei 60/40 kämen 80 % des Risikos aus Krypto** — *keine ausgewogene
Aufteilung, sondern eine Krypto-Wette mit Aktien-Beiwerk.* **Gleicher
Risikobeitrag beider Seiten läge bei 79/21.**

⭐ **Unerwartet: 90/10 hat einen kleineren grössten Rückgang als 100/0**
(−33,7 % gegen −35,7 %). Bei einer Korrelation von 0,32 **federt eine kleine
Krypto-Beimischung den Aktien-Einbruch ab.** Es kippt zwischen 80/20 (−33,9 %)
und 70/30 (−40,8 %).

**⚠️ Der Ertrag wurde bewusst nicht gemessen.** Der Zeitraum enthält einen der
grössten Krypto-Aufschwünge der Geschichte; eine Renditemessung darauf sagte
„mehr Krypto war besser". **Risiko ist über Zeiträume einigermassen stabil,
Ertrag nicht.**

**Betreiberentscheidung: 80/20**, mit der Begründung aus der Messung — nahe am
Punkt gleicher Risikobeiträge, letzte Stufe, auf der Krypto diversifiziert statt
zu dominieren.

### In einfacher Sprache

*Erste Messung:* Der grosse Auswahllauf rechnet drei bis fünf Stunden, nicht
Wochen. Damit ist der Zeitplan nicht gefährdet. *Zweite Messung:* Krypto
schwankt fast viermal so stark wie Aktien. Ein Euro Krypto wiegt im Risiko wie
vier Euro Aktien. *Der überraschende Teil:* Eine **kleine** Beimischung macht das
Ganze **ruhiger** als reine Aktien, weil beide nicht gleichzeitig fallen.

---

## AX — Fehler dieser Arbeitsphase, festgehalten

**Nicht als Selbstkritik, sondern weil sie ein Muster bilden.**

| # | Fehler | Ursache |
|---|---|---|
| 1 | „Teilkerze **fünf Minuten** alt" — tatsächlich 2–3 Stunden | Zahl aus dem TB-35-Bericht übernommen, ohne `crontab -l` zu prüfen. ⚠️ **Stand so in der Wochenrückmeldung an Fable** und stützte sein Argument |
| 2 | „AF.2 Nr. 6" existiert im Repo nicht | Fundstelle aus einem Beratungstext übernommen, ohne sie gegen das Repo zu prüfen |
| 3 | Drei Fassungen als „ersetzt" ausgewiesen, die nie im Register standen | dasselbe |
| 4 | In TB-40 **F** verlangt, während dieselbe Aufgabe **H** zitierte | Widerspruch im eigenen Dokument nicht bemerkt |
| 5 | „die **fünf** Werte von `MIN_HISTORY_*`" — es sind **vier** | Gruppen gezählt statt Werte |
| 6 | Dateimuster `AAPL.csv` angenommen — es ist `AAPL_1d.csv` | nicht nachgesehen |
| 7 | **Der TB-40-Mac-Testauftrag wurde nie angefordert** | gemergt und weitergegangen; dass das Werkzeug dort nicht läuft, fiel erst durch eine andere Aufgabe auf |
| 8 | `shared/test_kursdaten.py` als „bekannt rot" geführt | war in der Cloud grün (82/82) und auf dem Mac grün (**88/88**) — aus einer alten Liste übernommen |
| 9 | `docs/UMGEBUNGEN.md`: `node` als „fehlt in der Cloud" | ⚠️ **Der Vermerk, der gegen genau diese Fehlerklasse angelegt wurde, enthielt sie am Tag seiner Anlage selbst.** Richtig ist **„wechselnd — je Sitzung prüfen"** |
| 10 | `</parameter>` am Ende eines Bash-Befehls | Syntaxfehler, der Befehl lief nicht — Unachtsamkeit beim Zusammensetzen |
| 11 | **Der TB-45-Auftrag schrieb `python3` vor**, wo `trading-env/bin/python3` gehört | ⚠️ Steht seit demselben Morgen in `docs/UMGEBUNGEN.md` — **beim ersten Einsatz übergangen**. Folge: Trockenlauf und `test_leeres_symbol` fielen rot aus, **ohne dass etwas kaputt war**. ⭐ Die Sitzung hat es **gemeldet** und richtig gewechselt |
| 12 | „**sechs** Schreibweisen scheitern auf 3.9" | Zahl aus dem Cloud-Bericht übernommen — der Mac misst **acht von vierzehn** |

> **Acht von zwölf haben dieselbe Ursache: eine Zahl oder ein Muster aus einem
> Bericht übernommen, statt es an der Quelle zu prüfen.** Gefunden wurden sie
> sämtlich von den Sitzungen — **weil deren Aufträge verlangen, Belege aus dem
> Repo zu lesen statt aus dem Aufgabendokument abzuschreiben.**
>
> ⚠️ **Fehler 9 und 11 gehören zusammen und sind die unangenehmsten:** Die Datei,
> die gegen diese Fehlerklasse angelegt wurde, enthielt sie selbst — und wurde im
> ersten Auftrag danach übergangen. *Ein Vermerk hilft nur, wenn er gelesen wird
> und wenn Abweichungen gemeldet werden. Beides ist inzwischen als Regel darin
> eingetragen, und beim TB-45-Maclauf hat es funktioniert.*

**Fehler 7 hat eine eigene Lehre:** Der Mac-Testauftrag wird **vor** dem nächsten
Merge angefordert, nicht danach.

### In einfacher Sprache

*Was hier steht:* Zwölf Fehler aus der Planungsseite dieser Arbeitsphase, mit
ihrer Ursache. *Warum sie aufgeschrieben sind:* Acht davon sind derselbe Fehler
— eine Zahl aus einem Bericht übernommen, statt sie in der Quelle nachzusehen.
*Was daran gut ist:* Alle sieben wurden gefunden, und zwar von den Programmen,
die den Auftrag hatten, im Projektarchiv nachzulesen statt abzuschreiben.

---

## AY — Die Sichtbarkeitsreihe: TB-42 bis TB-45 (16./17.09.2026)

**Vier Aufgaben, ein Satz:** *Ein Werkzeug, das nicht mehr misst, sagt es.*

Der Anlass war jedes Mal derselbe: eine Prüfung, die **grün meldet, ohne etwas
gemessen zu haben**. Das ist die gefährlichste Fehlerform dieses Projekts, weil
sie in den Zahlen genauso aussieht wie ein gelungener Lauf.

### AY.1 — TB-42: Der Grössenfaktor wird sichtbar

Der Faktor stand als Konstante im Bot und tauchte in keiner Datenbankzeile auf.
Nach TB-42 legt `groessenfaktor.spalte_anlegen(conn)` die Spalte **auch in
Alt-Datenbanken** an, und `groessenfaktor.lies(__file__)` holt den Wert dort, wo
er gilt. ⚠️ **Änderung an allen neun `forward_test.py`** — mit ausdrücklicher
Freigabe, als **Fehlerbehebung eingestuft, nicht als Amendment**.

### AY.2 — TB-43: Drei blinde Wachen

Drei Schreibschutz-Wachen liessen Schreibvorgänge **still durch**. Sie meldeten
weiter „bestanden".

### AY.3 — TB-44: Die Wache auf beiden Pythons

⭐ **Der lehrreichste Befund der Reihe, und er ist ein Sprachdetail:**

```python
def wach_open(datei, modus="r", *a, **k):
    return echtes_open(datei, modus, *a, **k)   # mode= landet doppelt
```

**Eine Python-Funktion ist ein Deskriptor, eine C-Funktion nicht.** Wer im
Klassenrumpf eine C-Funktion durch eine Python-Funktion ersetzt, ändert damit
**das Bindungsverhalten mit** — die Argumente verschieben sich um eins.

**Reparatur:** `_Wache` als aufrufbare **Instanz** (kein Deskriptor), dazu
`_bindungen_nachziehen` über **Identität** statt über den Namen.

⚠️ **In der Cloud war die Sache auf fünf Python-Fassungen grün und brach auf dem
Mac bei zwei von neun Bots ab.** Daraus entstand `docs/UMGEBUNGEN.md` — und die
Regel: **Der Mac-Testauftrag wird vor dem Merge angefordert.**

### AY.4 — TB-45: Zwei Wachen, die bei kaputtem git „bestanden" melden

⭐ **Der stärkste Einzelbefund der ganzen Reihe, gemessen am alten Stand:**

> `shared/test_kursdaten.py` meldet bei fehlendem `origin/main` **„bestanden"**
> — **mit 28 grünen Prüfungen, hinter denen keine einzige Messung steht.**
> Dieselbe Verwechslung in `dashboard/test_portfolio_sicht.py` (6 Prüfungen).

Die Ursache: Ein **gescheiterter** git-Aufruf liefert eine **leere** Ausgabe —
und eine leere Ausgabe wurde gelesen als „keine Datei verändert".

**Verschärft wurde nur der gescheiterte Aufruf, nicht das leere Ergebnis eines
gelungenen.** Die Negativ-Prüfungen bleiben grün.

**Gegenprobe am alten Stand, alle drei bestätigt:** `test_stille_ausfaelle.py`
27/27 (alt: 6 rot) · `test_leeres_symbol.py` 45/45 (alt: **23/35**) ·
Trockenlauf Teil N 156/156 (alt: `_ist_geraet(<Verzeichnis>)` = `True`).

### AY.5 — Der Datumsbefund, der kleiner war als befürchtet

Ich hatte gewarnt, `datetime.fromisoformat` treffe **alle neun Bots** und der
anstehende Datenordner-Umbau verschärfe es. **Beides gemessen falsch:**

| Meine Annahme | Gemessen (Mac, 3.9.6) |
|---|---|
| alle neun Bots | ⚠️ **vier von neun** — der Krypto-Pfad erreicht die Stelle nie |
| der Datenordner-Umbau berührt den Weg | ⚠️ **nein** — die Zeitstempel der Kursdateien liest `pandas` |
| „ein Datum kommt an" | ⚠️ **genau ein Wert**, `'2026-09-16T00:00:00'`, **vom Code selbst gebaut** |

**Acht von vierzehn Schreibweisen scheitern auf 3.9** (die Cloud nannte sechs;
der Mac-Katalog ist breiter). ⭐ **Keine davon kann die Stelle erreichen.**

**Und der Ausgang, falls es doch einträte — auf dem Mac gemessen, nicht
hergeleitet:** Der Bot **läuft durch**, schreibt **je Symbol eine Fehlerzeile**
und hält **null Positionen**. Kein stiller Rückfall, keine falsche Kerze, kein
Abbruch.

> **Entscheidung des Betreibers: Weg 3** — so lassen und melden.
> `shared/entscheidungskerze.py` ist seit dem 16.09., 04:42:24Z der Live-Pfad,
> gegen den Registertext 7 den Backtest vergleicht. **Dort zu ändern heisst, am
> Objekt zu ändern, dessen Übereinstimmung gerade gemessen wird** — für ein
> Risiko, das gemessen nicht existiert.

### AY.6 — Was der Mac-Lauf zusätzlich fand

| Befund | Warum es zählt |
|---|---|
| ⚠️ `shared/test_drawdown_beide_masse.py` **terminiert nicht** und hinterlässt einen Kindprozess, der **20 Minuten weiterrechnet** | Auf dem Rechner, auf dem die neun Bots per Cron laufen |
| ⚠️ **Drei** Tests erreicht ein Basislauf nie (Bot-Argument nötig) | Sie sind **ungeprüft, nicht rot** — aus der Cloud war einer sichtbar |
| `t3_supertrend` hat denselben harten Stopp wie die Elliott-Bots | **Am Mac an beiden Ständen bestätigt** — nicht cloud-spezifisch |
| Sechs der neun Bots überspringen ein leeres Symbol **still** | Widerspricht genau der Regel, die TB-45 durchsetzen sollte |
| ⚠️ Bei GitHub war **kein einziger Schlüssel** hinterlegt | Der geplante signierte Tag wäre als **unverifiziert** geführt worden |

### AY.7 — Die Randbedingungen, die getragen haben

| | |
|---|---|
| Neun Datenbanken vorher/nachher | ✅ **byteweise identisch** |
| Datenstand `d9449faf…`, 223 Dateien | ✅ unverändert |
| Rücknahme des Alt-Stands nach Teil 4 | ✅ restlos |
| ZIP zum manuellen Download | ✅ **geliefert** — die am 16.09. eingeführte Regel greift |

### In einfacher Sprache

*Worum es in allen vier Aufgaben ging:* Prüfprogramme, die „alles in Ordnung"
melden, **ohne etwas geprüft zu haben**. Das ist schlimmer als ein Fehler, weil
es wie Erfolg aussieht.

*Der deutlichste Fall:* Ein Prüfprogramm vergleicht den aktuellen Code mit dem
auf GitHub. Kommt dieser Vergleich gar nicht zustande, kam bisher eine **leere
Antwort** zurück — und leer wurde gelesen als „nichts verändert". Es meldete
dann **28 grüne Häkchen**, hinter denen nichts stand.

*Ein Lehrstück über Sprachdetails:* Eine Schutzfunktion war auf dem einen
Rechner in Ordnung und auf dem anderen kaputt — wegen eines Unterschieds
zwischen zwei Arten von Funktionen, den man nicht sieht, wenn man nur den Code
liest. Daher gibt es seit dem 17.09. eine eigene Datei, die festhält, worin sich
die beiden Rechner unterscheiden.

*Und eine Sorge, die sich aufgelöst hat:* Ich hatte befürchtet, ein
Datumsproblem könnte alle neun Programme treffen. Der Mac hat gezeigt: Es
betrifft vier, und die einzige Zahl, die dort ankommt, **baut das Programm
selbst**. Niemand von aussen kann sie beeinflussen.

---

## AZ — TB-46 und die beiden Fable-Runden: der Zuschnitt der Datenbestände (17.09.2026)

**Der Tag, an dem aus einer Schätzung eine Messung wurde — und aus einem
Ordnernamen eine Registerfrage.**

### AZ.1 — Der Auftrag war bewusst klein geschnitten

Registertext 5a verlangt zwei Datenbestände. Wie teuer der Umbau würde, war seit
Wochen **geschätzt und nie gezählt**: *„101 Module lesen `data/`."* TB-46 durfte
deshalb **nichts umbauen** — nur erheben, zwei Entwürfe gegeneinander rechnen und
das Snapshot-Werkzeug bauen.

⭐ **Die Sitzung hat drei Zahlen der Aufgabenstellung korrigiert, statt sie
abzuschreiben** — und alle drei waren meine.

### AZ.2 — Die Messung, und warum die Methode zählte

| | |
|---:|---|
| **182** | Module erreichen `data/` |
| **29** | bauen den Pfad selbst, **7** davon sind die gemeinsamen Stellen |
| **145** | beziehen ihn mittelbar |
| ⭐ **0** | Bot-Dateien bauen einen Pfad |

⭐ **Gemessen über den Syntaxbaum, nicht mit Textsuche — und der Unterschied war
nicht akademisch:** Zwei `forward_test.py` **nennen** `data/` in einer
Protokollzeile. **Eine Textsuche hätte gemeldet, der Umbau müsse die Bot-Dateien
anfassen, die er nicht anfassen darf** — und damit die ganze Aufgabe blockiert.

⚠️ **Zur 101:** Sie ist mit dem TB-34-Skript unverändert nachgemessen und kommt
**genau** heraus. **Sie ist nicht veraltet, sie zählt eine engere Frage.** Beide
Zahlen sind richtig.

### AZ.3 — Was die Zahlen kosteten, und was sie wert waren

| meine Angabe | gemessen |
|---|---|
| „rund 56 MB" | `data/` sind **211,0 MB**; im Repo kostet die Kopie **+0,001 %**, weil git gleiche Inhalte einmal ablegt. Auf der Platte **202 MB** |
| „läuft die Hash-Berechnung rekursiv?" | **Nein** — `os.listdir` + `.csv`. ⭐ **Der Fallstrick ist die Voreinstellung**, nicht die Rekursion: `datenstand()` zeigt ohne Argument auf `BASE_DIR/data`, und nach einem Umzug läge dort **null** `.csv` — der Hash der leeren Menge |

### AZ.4 — Die Entscheidung: Zuschnitt B

**Zwei Entwürfe standen zur Wahl.** A benennt `data/` in `data/live/` um, wie im
Register. B lässt `data/` und legt `snapshots/<hash>/` daneben.

**Drei Ausfälle von A wurden an einem nachgebauten Baum gemessen:**

| | |
|---|---|
| 1 | **`shared/paths.py` schweigt** — null `.csv`, keine Meldung, und `os.makedirs` legt den leeren Ordner wieder an |
| 2 | ⚠️ **Die neun Bots fallen auf den Live-Abruf zurück und rufen über das Netz ab** — **Registertext 5a verbietet genau das** |
| 3 | **Der Datenstand-Hash wird der der leeren Menge** |

> ⭐ **Fables Urteil:** *„B ist zulässig, und zwar nicht als Abweichung, sondern
> als die bessere Erfüllung."* Der Ordnername stand im Register, *„weil ich ihn
> hingeschrieben habe, nicht weil er etwas sichert"*.
>
> **Und der Satz, der die Sache entscheidet:** *„Ein Zuschnitt, der die Live-Seite
> anfasst, um die Selektionsseite zu isolieren, isoliert die falsche Seite."*

### AZ.5 — ⚠️ Mein Einwand war halb richtig

**Ich hatte eingewandt**, der Bericht stelle eine Frage nicht: *Was, wenn beim
Umbau eines der 90 Selektionsmodule vergessen wird?* Unter A fände es einen
leeren Ordner; **unter B den vollen Live-Bestand und rechnete still falsch.**

**Mein Vorschlag war eine Eingangswache.** Fables Antwort:

> ⚠️ *„Die Wache prüft die Eingabe, nicht das Verhalten."* Ein Modul, das seinen
> Pfad **selbst baut**, sieht die übergebene Wurzel **nie** — es liest `data/`,
> und die Eingangswache hat nichts zu beanstanden, **weil der Snapshot in Ordnung
> ist.**

⭐ **Und die Diagnose dahinter war die eigentliche Einsicht:** Was A „laut"
gemacht hätte, war **nicht der Name, sondern die Leere**.

**Drei Schichten statt einer** — der Resolver mit Selektionsmodus (fängt die
145), ein AST-Test (fängt die 22 Selbstbauer, ⭐ **und er ist rot, bis die 90
verdrahtet sind — das ist gewollt, er misst den Umbau**), und der Lese-Audit als
Ausgangsnachweis. *„Drei Schichten, jede mechanisch, keine davon eine
Beteuerung."*

### AZ.6 — Die zwei Hashes, und die Falle darin

**Fables neuer 5a definierte den Snapshot-Hash zunächst über die
Manifest-Einträge.** Wir haben widersprochen, weil der registrierte Hash etwas
anderes umfasst — **nur `*.csv`, mit Grösse** — und `d9449faf…` seit dem 15.09.
die einzige verankerte Zahl des Projekts ist.

**Er hat die Trennung angenommen und dabei seine eigene Definition korrigiert:**

> ⭐ *„Der Snapshot-Hash läuft über die **Dateien**, nicht über das Manifest."*
> Sonst **hinge der Name von der Metadaten-Formatierung ab** und wäre bei jedem
> Feld, das jemand ergänzt, ein anderer.

**Das Ergebnis:** Snapshot-Hash = der **Name** (*„ist das derselbe
Eingabesatz?"*), Datenstand-Hash = die **Herkunft** (*„sind das dieselben
Kursdateien?"*), beide im Manifest unter unverwechselbaren Feldnamen, je von
**einer** Funktion erzeugt.

⚠️ **Und warum die Umkehrung nicht ginge:** Zwei Snapshots mit identischen
Kursdateien, aber geänderter Symbolliste bekämen denselben Namen — **eine
Sicherung würde zum Fehler.**

### AZ.7 — Drei Befunde, die keiner von uns gesucht hatte

**1. ⚠️ Die Wanduhr im Selektionspfad** — Fable hält sie für die wahrscheinlichste
Ursache, die den Lauf im Nachhinein ungültig machen könnte:

> Ein `datetime.now()`, das die Historie kappt oder das „letzte vollständige
> Jahr" bestimmt. **Derselbe Snapshot ergibt dann an zwei Tagen zwei Ergebnisse**,
> und der Reproduktionstest findet es **nur, wenn er an einem anderen Tag läuft.**
> *„Weil er in jedem Backtester steckt, der je ‚bis heute' gerechnet hat."*

**2. ⚠️ Die Snapshot-Grenze war zu eng gedacht.** *„Alles, was nicht Code ist"* —
Symbollisten, NYSE-Kalender, Konfigurationsdateien. *„Wenn die ausserhalb liegen,
ist der Lauf nicht reproduzierbar, obwohl der Kurshash stimmt."*

**3. ⚠️ Snapshot vor Datencron.** Läuft der Cron zuerst, meldet der
Registerprüfer **jeden Tag ABWEICHUNG** — *„derselbe Fehler wie Ausfall 3, nur
mit umgekehrtem Vorzeichen"*. Ein Alarm, an den man sich gewöhnt.

### AZ.8 — ⚠️ Die wichtigste Zeile ist eine Frage, die wir nicht gestellt haben

> *„‚Hält null Positionen' — heisst das **keine neuen** Positionen, oder
> **schliesst** der Bot offene, weil er sie ohne Kerze nicht bewerten kann? Im
> zweiten Fall macht ein Parsing-Fehler einen Trade."*
>
> *„Ein Bot, der bei fehlender Kerze verkauft, hat kein Holdout-Problem, sondern
> ein Sicherheitsproblem."*

**Sie stammt aus unserer eigenen TB-45-Messung.** Wir haben die Zahl berichtet
(*„Offene Papier-Positionen: 0"*) und **nicht gefragt, wie sie zustande kommt.**

### AZ.9 — Zwei Ableitungen, beide nachgerechnet

**Die Mindestzahl Signale ist keine Wahl:**

> **n ≥ 20 = 1 / (1 − Schwelle).** Bei n = 19 reisst **eine** Abweichung die
> 95 % (18/19 = 94,7 %); bei n = 20 nicht (19/20 = 95,0 %).
> ⭐ **Die Mindestzahl ist eine Eigenschaft der Schwelle, kein zweiter Parameter.**
> *Wer die 95 % ändert, ändert die 20 mit.*

**Und die Paketlage — an der Quelle geprüft, nachdem Fable sich selbst als
unsicher markiert hatte:**

| | `requires_python` laut PyPI |
|---|---|
| pandas **3.0.x** | ⚠️ **`>=3.11`** — nicht 3.10, wie vermutet |
| pandas **2.3.3** (Mac) | `>=3.9` |

⭐ **Sein Vorbehalt war berechtigt, und die geprüfte Zahl hat seinen Vorschlag
gestärkt:** Der Mac kann pandas 3.x **nicht bekommen**. Also läuft der
Selektionslauf auf dem Mac, und die Cloud reproduziert **im selben Lock auf einem
3.9-Interpreter** — erst so sehen beide Seiten dieselbe pandas-Hauptversion.

### AZ.10 — Was wir an TB-46 beanstandet haben

| | |
|---|---|
| ⚠️ | **`git status` am Ende war nicht leer** — drei Dateien nach dem Commit geändert, während die Rohausgabe „(leer = sauber)" schreibt |
| ⚠️ | **Eine Rohausgabe ist veraltet** — `test_snapshot_lauf.txt` zeigt **64/64**, das Dokument **69/69**; die 64 stammt aus einem Lauf vor Probe 3m |

*Beides sind Schlampigkeiten der Ablage, keine Fehler der Arbeit — aber die
zweite ist dieselbe Familie, die uns diese Woche zwölfmal erwischt hat.*

### AZ.11 — Was aus dieser Runde ins Register geht

**Fünf Texte, alle ausformuliert:** **5a neu** (Struktur statt Name,
Snapshot-Grenze, Hash über Dateien, `asof`) · **5e neu** (Lese-Audit als
Gültigkeitsbedingung) · **5f neu** (Umgebung als dritte Achse, Lock-Hash,
Reproduktion auf gleicher Umgebung) · **7 Ergänzung I** (Kein-Entscheid-Tag) ·
**7 Ergänzung II** (Ereignismenge, n ≥ 20, „unbestimmt") · **datierter Nachtrag**
zur Tatsachennotiz vom 15.09.

⭐ **Die Identität eines Laufs ist seither ein Tripel:** **Commit** (Code) ·
**Snapshot** (Eingaben) · **Lock** (Umgebung). *„Der Snapshot ist das, was der
Lauf liest; das Lock ist das, worauf er läuft."*

### In einfacher Sprache

*Worum es ging:* Das Register verlangt zwei Sammlungen von Kursdaten — eine
laufende und eine eingefrorene. Bevor jemand umbaut, sollte gezählt sein, was der
Umbau kostet. Bisher war es geschätzt.

*Was herauskam:* Hundertzweiundachtzig Programme lesen den Ordner, nicht
hundertundeins — **aber fast alle holen sich den Namen von woanders.** Und
**keine der neun Bot-Dateien, die nicht angefasst werden dürfen, nennt den Ordner
überhaupt.** Damit ist die grösste Sperre weg.

*Die Entscheidung:* Der bequemere Zuschnitt gilt — bestätigt von dem, der den
Registertext geschrieben hat, mit der Begründung, der Ordnername sichere nichts.

*Wo ich danebenlag:* Ich hatte eine Wache am Eingang vorgeschlagen. Ein
vergessenes Programm, das sich seinen Pfad selbst baut, kommt an dieser Wache gar
nicht vorbei. Es braucht drei Wachen, und jede fängt eine andere Art von
Vergessen.

*Die unangenehmste Erkenntnis:* Wir haben gemessen, dass ein Bot bei fehlenden
Kursdaten „null Positionen" hält — und **nicht gefragt, ob das heisst „kauft
nichts" oder „verkauft alles".** Im zweiten Fall löst ein Datumsfehler einen
echten Verkauf aus. Das ist jetzt der erste Punkt vor dem Umbau.

---

## BA — TB-46 gemergt, Zuschnitt B entschieden, zwei Fable-Runden

**17.09.2026. Gemergt `135c306`.**

`shared/snapshot.py` und `shared/test_snapshot.py` (69 Prüfungen, dreizehn
Mutationsproben) sind im Repo. **Erhebung, Werkzeug, Wache — kein Umbau.**

**Die Messung, die alles Weitere trägt:**

| | |
|---:|---|
| **182** | Module erreichen `data/` — die frühere Zahl **101** ist exakt reproduziert und **nicht falsch**, sie zählt eine engere Frage |
| ⭐ **0** | **Bot-Dateien bauen einen Pfad.** Der Umbau kommt ohne `forward_test.py`, `live_params.py` und `equity_simulation.py` aus |
| **90** | Module der Selektionsseite, die auf den Snapshot zu zeigen sind |

⭐ **Gemessen über den Syntaxbaum, nicht mit Textsuche** — zwei `forward_test.py`
**nennen** `data/` in einer Protokollzeile. Eine Textsuche hätte gemeldet, der
Umbau müsse genau die Dateien anfassen, die er nicht anfassen darf.
**Prüfprinzip B5.**

### Die Entscheidung: Zuschnitt B

**`data/` bleibt der lebende Bestand, `snapshots/<hash>/` kommt daneben.**
Fable hat das bestätigt — *„nicht als Abweichung, sondern als die bessere
Erfüllung"* von Registertext 5.

### Die zweite Fable-Runde: der Hash

**Frage:** Worüber läuft der Snapshot-Hash — über das Manifest oder über die
Dateien?

**Antwort, angenommen:** ⭐ **über die sortierten (Pfad, Inhalts-Hash)-Paare der
DATEIEN.** *Liefe er über das Manifest, hinge der Name des Snapshots an der
Formatierung seiner Metadaten — und ein geänderter Zeitstempelformat erzeugte
einen anderen Snapshot bei identischen Daten.*

### Und der Vorschlag von mir, der verworfen wurde

**Ich hatte eine „Eingangswache" vorgeschlagen:** beim Start des Laufs das
Manifest prüfen. **Fable:** *„Die Wache prüft die Eingabe, nicht das Verhalten."*
Ein Modul, das seinen Pfad selbst baut, sieht die übergebene Wurzel nie.

⭐ **Angenommen stattdessen: drei Schichten.** **(1)** Resolver-Modus in
`shared/paths.py`, der die Snapshot-Wurzel liefert und bei jeder Anfrage nach dem
Live-Bestand **wirft** · **(2)** **AST-Test**, dass kein Selektionsmodul einen
Datenpfad ausserhalb des Resolvers baut — ⭐ *er ist rot, bis die 90 verdrahtet
sind, und das ist gewollt: er misst den Umbau* · **(3)** **Lese-Audit** als
Ausgangsnachweis.

### In einfacher Sprache

**Was wir wissen wollten:** Wie viele Programmteile lesen die Kursdaten, und
müssen wir dafür die Bot-Dateien anfassen, die nicht angefasst werden dürfen?

**Was herauskam:** 182 Programmteile lesen die Daten, aber **kein einziger der
neun Bots baut selbst einen Dateipfad**. Der Umbau kommt ohne sie aus.

**Warum das so ist:** Gemessen wurde nicht mit einer Textsuche, sondern an der
Struktur des Programms. Zwei Bots **erwähnen** den Datenordner in einer
Protokollzeile — eine Textsuche hätte daraus geschlossen, man müsse sie ändern.

**Was das für dich heisst:** Der grosse Umbau ist ungefährlicher als befürchtet.
Und die eingefrorene Kopie der Daten kommt **neben** den lebenden Bestand, nicht
an seine Stelle.

---

## BB — TB-46b: der Sicherheitspunkt ist beantwortet

**18.09.2026. Gemergt `c5ad722`.**

**Die Frage kam von Fable, und wir hatten sie nicht gestellt:**
*„‚Hält null Positionen' — heisst das **keine neuen** Positionen, oder
**schliesst** der Bot offene, weil er sie ohne Kerze nicht bewerten kann?"*
⚠️ *„Ein Bot, der bei fehlender Kerze verkauft, hat kein Holdout-Problem,
sondern ein Sicherheitsproblem."*

### Die Antwort

> ⭐⭐⭐ **KEIN Bot schliesst eine Position, weil Kursdaten fehlen. Nicht
> „wurde nicht beobachtet", sondern strukturell unmöglich.**

**Gelesen an neun von neun Bots über fünf Ausstiegspfade. Die gemeinsame
Bauform:**

```
__main__          für jedes Symbol:  df = entscheidungskerze.lade(...)
                                     → in price_data / indicator_data
                  alles in einem try/except Exception je Symbol

check_open_trades  für jeden offenen Trade:
                     if symbol not in <daten>:  continue     ← die Tür
                     future = df[df["open_time"] > entry_time]
                     nur bei Treffer:  UPDATE ... status='closed'
```

⭐ **Es gibt kein `else`.** Ein Symbol ohne Kursdaten erreicht die UPDATE-Zeile
nicht.

### Der offene Punkt, der aus der Prüfung entstand

⚠️⚠️ **`shared/entscheidungskerze.py`, `lade()`: der Rückfall auf die zweite
Quelle wird nicht auf Frische geprüft.**

```
658    if art is not None:                       # data/ fehlt, veraltet oder unklar
659        sammler.erfasse(symbol, art, grund)
663        df = abruf()                          # ← die zweite Quelle
667    gefiltert, _verworfen, hinweis = nur_entscheidbar(df, …)
```

`_aus_datei()` fragt `ist_frisch()` (Zeile 690). **`abruf()` fragt niemand.**
⚠️ *Das ist der einzige Weg, auf dem eine falsche Kerze bis zur Entscheidung
kommt.*

### Fables Antwort darauf: Gleichheit statt Frische

**Mein Vorschlag war eine Frischeprüfung. Verworfen.**

⭐ **Angenommen: der `close_time` der gelieferten Kerze muss dem erwarteten Wert
GLEICHEN — aus jeder Quelle, ohne Ausnahme. Stimmt er nicht, ist es ein
Kein-Entscheid.**

> *„Die Gleichheit braucht keinen Parameter. Eine Toleranz wäre eine zweite
> willkürliche Zahl an genau der Stelle, an der das Register keine mehr
> verträgt."*

**Vier Dinge gehören deshalb in EINEN Zug** — und der braucht die
Betreiberfreigabe für `shared/entscheidungskerze.py`: Gleichheitsprüfung ·
Datencron mit Prüfung vor den Bot-Läufen (`TZ=UTC`) · Kein-Entscheid-Datensatz in
`melde()` · Datenstand-Hash und Kerzenwerte je Lauf ins Protokoll.

### Der Mac-Lauf und die eine abweichende Datenbank

**Eine** der neun Datenbanken wich ab. ⭐ **Die Erklärung ist belegt, nicht
plausibilisiert:** `turtle_soup_crypto` hat einen Cronjob `15 0 * * *`; die
Änderungszeit 00:15:24 Ortszeit = **22:15:24 UTC** liegt im Prüffenster, und der
Inhaltsunterschied deckt sich **Zeile für Zeile** mit der Logzeile desselben
Laufs.

### In einfacher Sprache

**Was wir wissen wollten:** Kann es passieren, dass ein Bot eine offene Position
verkauft, nur weil die Kursdaten für dieses Wertpapier gerade fehlen?

**Was herauskam:** **Nein, und zwar nicht zufällig.** In allen neun Bots führt
der Weg zur Verkaufszeile über eine Abfrage, die ein Wertpapier ohne Kursdaten
vorher überspringt. Es gibt keinen Zweig, der „sonst verkaufe" sagt.

**Warum das so ist:** Der Code ist so gebaut, dass fehlende Daten den Bot beim
betroffenen Wertpapier weitergehen lassen. Das war nicht als Sicherheitsmassnahme
gedacht, wirkt aber wie eine.

**Was das für dich heisst:** Der Punkt, der vor allem anderen stand, ist vom
Tisch. **Geblieben ist ein kleinerer:** Wenn die gespeicherten Daten veraltet
sind, holt der Bot sie live nach — und **dabei prüft niemand, ob das Gelieferte
wirklich die richtige Kerze ist.** Das wird behoben, sobald du die Änderung an
dieser einen Datei freigibst.

---

## BC — TB-47: die Snapshotgrenze, gemessen

**18.09.2026. Gemergt `a1e7fb4`.**

| | |
|---|---|
| ⭐ **Die Grenze** | **transitive Hülle über 142 Module ⇒ genau ZWEI** Nicht-Kursdaten-Eingaben: `config/top25_symbols.txt` und `config/sp500_top150.txt`. Kein Handelskalender als Datei — er kommt aus dem Paket, also aus dem Lock |
| ⭐ **Die zwei Hashes** | `datenstand` = `d9449faf…` bei 223 Dateien, **trifft den Anker vom 15.09.** · `snapshot_hash` = `4fee547dccd4c5e41df1f4dfa5d8e00c927c053fdfa31c57cb44022f0a1f3608`, **verschieden**. *Zwei Zahlen, zwei Fragen* |
| ⚠️ **36 von 223** | Kursdateien mit Befund **`rand_erste`** — die **erste** Kerze deckt ihren Zeitraum nicht voll ab. ⭐ **Die Prüfung stellt je Datei fest, dass die Kerze auf die letzte Stelle das Aggregat genau der vorhandenen feineren Kerzen ist: abgeleitet, nicht unvollständig geschrieben** |
| ⭐ **Letzte Kerze** | **bei keiner Datei betroffen** — der gefährliche Rand ist sauber |
| ⚠️ **175 von 223** | tragen **`kein_zeuge`** — 150 Aktien, 25 Krypto-1h. **Keine feinere Datei zum Vergleich ⇒ nicht belegbar.** Das ist *„kein Befund"*, nicht *„geprüft"* |
| **Prüfungen** | `shared/test_snapshot.py` **69 → 110**, dreizehn Mutationsproben, jede mit Gegenprobe |

**Beide Rechner, dieselben Zahlen** — Cloud 3.11.15, Mac 3.9.6.

### Prüfprinzip B4, neue Variante: eine Probe kann sich selbst SEHEN

**Die Zählung überlebender Enkelprozesse meldete zuerst `4`.** Das wäre der
Gegenbeweis gewesen. **Die Sitzung hat nicht weitergemacht, sondern
nachgesehen — die Zählung zählte sich selbst:** Das Suchmuster stand in der
eigenen Befehlszeile, also fand `ps` die eigene Shell.

| Gegenprobe | Ergebnis |
|---|---|
| nur Python-Prozesse | 1 |
| Zählung aus einer **Datei** heraus, eigener Prozess ausgeschlossen | 1 |
| ⭐ **Aufruf ohne Heredoc — das Muster steht nicht mehr in der Befehlszeile** | **0** |

> ⭐ **Wir kannten: „eine Probe kann sich selbst blind machen." Hier galt: eine
> Probe kann sich selbst sehen — und meldet dann einen Fehler, den es nicht
> gibt.**

### Zwei Korrekturen am Rand

- ⚠️ **`system/test_log_rotation.py` stand als „bekannt rot" — er ist 117/117
  grün auf beiden Rechnern.** Der Eintrag kam aus einem Lauf auf einem alten
  Checkout. **Gestrichen, mit Kommentar:** *„Ein falscher Eintrag in dieser Liste
  ist teurer als gar keiner."*
- **`pandas_market_calendars` 4.6.1** auf dem Mac — ⭐ die Fassung, von der der
  Handelskalender kommt, und damit eine Zahl für `requirements.lock` und den
  Registereintrag nach 5f.

### In einfacher Sprache

**Was wir wissen wollten:** Was genau muss in die eingefrorene Kopie hinein,
damit der Selektionslauf später bitgenau wiederholbar ist?

**Was herauskam:** Ausser den Kursdateien nur **zwei** weitere Dateien — zwei
Symbollisten. Alles andere kommt entweder aus dem Programmcode oder aus einem
Paket, dessen Version wir festschreiben.

**Warum das so ist:** Gemessen wurde nicht „welche Dateien fallen uns ein",
sondern was die Programme wirklich lesen, über alle Aufrufwege hinweg.

**Was das für dich heisst:** Die Kopie ist überschaubar und vollständig
beschreibbar. **Ein Vorbehalt bleibt ehrlich benannt:** Bei 175 der 223
Kursdateien lässt sich nicht beweisen, dass die Randkerzen vollständig sind — es
gibt keine feinere Datei zum Vergleich. Dafür bürgt eine andere Schutzschicht,
und das steht so im Register.

---

## BD — Registertext 5a: die Ausnahme `rand_erste`

**18.09.2026. Registereintrag, eingetragen mit TB-48 als Abschnitt 17.3.**

**Die Teilkerzen-Prüfung schlägt bei 36 der 223 Kursdateien an und verweigert
damit jeden Snapshot. Die Ausnahme ist registriert — nach drei Bedingungen:**

| | |
|---|---|
| **(a)** | Der Befund betrifft ausschliesslich die **erste** Kerze. ⚠️ **Für `rand_letzte` gilt die Ausnahme nicht** |
| **(b)** | Die Kerze ist nachweislich **das Aggregat genau der vorhandenen feineren Kerzen** |
| **(c)** | Die Ausnahme wird **im Manifest des Snapshots** je Datei aufgeführt |

> ⚠️ **Die Prüfung selbst wird nicht abgeschwächt. Es gibt keine
> Übergehen-Flagge.** Sie schlägt weiter an und liefert weiter Rückgabewert 1;
> das Ziehen erfolgt **gegen diesen Eintrag**, nicht gegen ein Schweigen der
> Prüfung.

**Die Folgenlosigkeit ist hergeleitet, nicht behauptet:**

| | |
|---:|---|
| **20 von 36** | erste Kerze **2017–2020** — reiner Vorlauf vor der ersten Selektionsfalte |
| **16 von 36** | erste Kerze **ab 2023**, gehörend zu **genau 11 Symbolen**: `BMT ENA ENSO PEPE PROM PUMP SUI TRUMP U WLD ZKC` |
| ⭐ | **Diese Menge ist identisch mit der Liste aus T34.9** — den Symbolen, die **in keiner Selektionsfalte vorkommen** |

**Kein Symbol-Jahr-Beitrag des Selektionslaufs hängt an einer der 36 kurzen
ersten Kerzen.** ⭐ **Und TB-48 hat das direkt gemessen statt hergeleitet:**
*„kurze erste Kerze in einer GELADENEN Falte: Soll 0, Ist 0"*, über alle neun
Bots.

**Warum nicht reparieren:**

| | |
|---|---|
| ⚠️ **Teurer** | Abschneiden oder Neuaufbau ändert `data/` — und damit `d9449faf…`, die Tatsachennotiz vom 15.09. samt der darauf gemessenen Symbolzahlen je Falte |
| ⚠️ **Nicht dauerhaft** | **Jedes neu gelistete Symbol bringt den Befund wieder mit** |

> ⚠️ **Fällt künftig ein `rand_erste`-Befund an einer Datei an, deren Symbol in
> einer Selektionsfalte vorkommt, greift diese Ausnahme nicht automatisch.**

### In einfacher Sprache

**Was wir wissen wollten:** 36 von 223 Kursdateien haben eine erste Kerze, die
ihren Zeitraum nicht ganz abdeckt. Ist das ein Fehler, der die eingefrorene
Kopie unbrauchbar macht?

**Was herauskam:** **Nein.** Die kurze erste Kerze entsteht, weil die Geschichte
eines Wertpapiers mitten in einem Tag oder einer Stunde beginnt — der erste
Handelstag hat dann weniger Stunden. Das Prüfprogramm rechnet selbst nach, dass
die Kerze genau die Summe der vorhandenen feineren Kerzen ist.

**Warum das so ist:** Der gefährliche Fall wäre die **letzte** Kerze — dort
könnte ein Abruf mitten hineingeschrieben haben. Die ist bei **keiner** der 223
Dateien betroffen.

**Was das für dich heisst:** Die Ausnahme steht im Register, eng gefasst und
begründet. Sie gilt nur für die erste Kerze und nur, wenn nachgerechnet ist, dass
die Zahlen stimmen. **Und das Prüfprogramm wird nicht weicher gemacht** — es
meldet weiter; erlaubt wird die Ausnahme durch einen Eintrag daneben, den ein
Prüfer lesen kann.

---

## BE — TB-48: der Registernachtrag, und zwei Fehler von mir

**18.09.2026. Gemergt `db8913a`.**

⭐ **`git diff --numstat`: `506 0`.** 506 Zeilen hinzugefügt, **null entfernt**,
genau eine Datei berührt. Der Registerprüfer aus TB-41 läuft über alle neun
Prüfungen einschliesslich `null_entfernte_zeilen`: **kein Befund.**

**19 Zahlen an ihrer Quelle nachgerechnet, je mit Datei und Fundstelle. 18
stimmen.** Darunter: die 11 Symbole als Menge identisch mit T34.9 · beide Hashes ·
36 Befunde der Art `rand_erste` · letzte Kerze nicht betroffen · 175 `kein_zeuge`,
davon 150 Aktien und 25 Krypto-1h · `18/19 = 94,7 %` reisst die Schwelle,
`19/20 = 95,0 %` nicht, `1/(1−0,95) = 20`.

### Fehler 1 — meine Jahreszahl

**Ich hatte geschrieben: „die erste Selektionsfalte beginnt 2022."**
**`research/faltenplan_neun/daten/faltenplan.json` sagt 2019.**

⭐ **Die Sitzung hat nicht still korrigiert, sondern als BEFUND gemeldet — und
mein indirektes Argument durch eine direkte Messung ersetzt.** Statt *„2017–2020
liegt vor 2022, also Vorlauf"* steht jetzt die Messung selbst im Register: **keine
der 36 kurzen ersten Kerzen liegt in einer Falte, in der ihr Symbol geladen
ist.**

> ⭐ **Die Schlussfolgerung hängt damit nicht mehr an meiner Jahreszahl.**

⚠️ **Woher meine 2022 vermutlich kam** — und *vermutlich*, weil ich es nicht
nachgemessen habe: T34.9 nennt *„Symbole je Falte: 3 (2022) → 6 → 9 → 13
(2025)"*, und das ist der **Krypto**-Faltenplan. **2019 dürfte die früheste
Falte über alle neun sein.** ⚠️ **Zwei Zahlen, zwei Fragen — TB-49 Teil 4
misst es.**

### Fehler 2 — meine Regel

**Ich hatte verboten, unter `research/` etwas zu ändern.** Die Sitzung hat sich
daran gehalten — und **den Prüfer, der die neunzehn Zahlen nachrechnet, deshalb
NICHT ins Repo gelegt:**

> *„`pruefe_abschnitt17.py` — **absichtlich nicht im Repo**: der Auftrag
> untersagt Änderungen unter `research/`."*

⚠️ **Folge: Der einzige Prüfer, der Abschnitt 17 nachrechnet, existiert nur in
einem ZIP-Archiv.** ⭐ **Die Sitzung hat sich korrekt verhalten; meine Regel war
zu breit.** **Daraus `ARBEITSWEISE.md` §11 (neu):** Ein Änderungsverbot nennt,
wovor es schützt — und Prüfwerkzeuge, die eine Aufgabe erzeugt, gehören
ausdrücklich ins Repo.

### Fehler 3, zum zweiten Mal — `git status` vor dem letzten Commit

**Wie in TB-46:** Die Statusausgabe im Beleg war **vor** dem abschliessenden
Commit entstanden. Beide Male trug der Zweig die aktuellen Fassungen; **beide
Male war der Beleg wertlos.** **Daraus die Regel in `ARBEITSWEISE.md` §7.**

### In einfacher Sprache

**Was wir wissen wollten:** Kommen die neuen Register-Festlegungen sauber in das
2065 Zeilen lange Vorregistrierungs-Dokument, ohne dass eine alte Zeile
verschwindet?

**Was herauskam:** **Ja — 506 Zeilen hinzugefügt, keine einzige entfernt.** Das
ist mit der git-Zeile belegt, und das eigene Prüfprogramm des Registers findet
keinen Fehler.

**Warum das so ist:** Neunzehn Zahlen wurden nicht abgeschrieben, sondern an
ihrer Quelle nachgerechnet.

**Was das für dich heisst:** ⚠️ **Eine der neunzehn war meine, und sie war
falsch.** Ich hatte geschrieben, der Auswahlzeitraum beginne 2022; der Plan sagt
2019. Die Sitzung hat das gemeldet statt stillschweigend auszubessern — und meine
indirekte Begründung durch eine direkte Messung ersetzt. **Die Aussage, auf die
es ankommt, gilt jetzt unabhängig davon, welche Jahreszahl richtig ist.**

---

## BF — TB-49: das Werkzeug lernt die Ausnahme

**18.09.2026. Cloud-Zweig `claude/new-session-kfbw56`, Mac-Lauf und Merge offen.**

**Die Lage vorher, in einem Satz:** *Das Register erlaubt die Ausnahme. Das
Werkzeug weiss nichts davon.*

### Der Nachweis in zwei Zahlen

| | |
|---|---|
| **am Stand von TB-48**, gegen dasselbe `data/` | `ABBRUCH: … 36 Datei(en) mit Befund …` · **`RC_ALT=2`** |
| **mit diesem Zweig**, derselbe Bestand | `36 Datei(en) mit Befund … davon zugelassen 36 … Abschnitt 17.3` · **`RC_TROCKENLAUF=0`** |

> ⭐ **2 → 0, bei unverändert 36 gemeldeten Befunden.** Die Prüfung ist nicht
> weicher geworden; sie bricht nur nicht mehr deswegen ab. **Und es gibt keine
> Übergehen-Flagge** — drei erfundene ergeben **2**, der Quelltext kennt keine.

**Am Wegwerf-Bestand wirklich gezogen:** 225 Dateien, 211,0 MB, **jede byteweise
gegen die Quelle geprüft**, beim Nachprüfen `UNVERAENDERT`. ⭐ **Der Anker hielt
ohne `--kein-anker`:** die Kopie trägt `d9449faf…` bei 223 Kursdateien.

### Die Regel, und die drei Bedingungen

**Zugelassen ist ein Befund genau dann, wenn alle drei zutreffen**
(`shared/snapshot.py::_zulassung`): Art `rand_erste` · **erste** Kerze der
Datei · Urteil `ABGELEITETE_TEILKERZE` **und** `aggregat_passt is True`.

⭐ **Als Regel, nicht als Liste der 36 Dateien** — ein neu gelistetes Symbol ist
damit automatisch gedeckt, ein `rand_letzte` nie.

**Das Manifest führt auf, was erlaubt wurde:** `zugelassene_befunde` mit **36**
Einträgen (Datei, Art, erste Kerze, Urteil, Text), `zugelassene_befunde_anzahl`
und ⭐ **`zugelassene_befunde_herkunft`** mit `fundstelle` → *Abschnitt 17.3* und
dem **Wortlaut des Registereintrags im Klartext**. Daneben unverändert
`teilkerzen_befunde` mit allen 36 und `frei_von_teilkerzen: false` — *der
Snapshot verschweigt nicht, dass die Prüfung angeschlagen hat.*

### ⭐⭐ Entschieden wird je BEFUND, nicht je DATEI

**Im `rand_letzte`-Versuch trägt `BTCUSDT_1d.csv` beides:** einen zugelassenen
`rand_erste` an ihrer ersten Kerze **und** den gestellten `rand_letzte`. Der
zugelassene bleibt in der Zählung (*„Zugelassen waren daneben 36 Befund(e)"*),
**die Datei bricht trotzdem ab.**

> ⚠️ **Eine Zulassung je Datei hätte den gefährlichen Rand durchgelassen, sobald
> derselbe Name auch einen erlaubten Befund trägt.** Das stand nicht im Auftrag.
> Probe `3x` misst genau diesen Fall.

**Zwei weitere Entscheidungen, die niemand verlangt hatte:**

**(b) wird eigens nachgestellt**, obwohl `rand_erste` heute nur an der ersten
Kerze entsteht — *„die Bedingung des Registers lautet ‚die erste Kerze der
Datei', nicht ‚ein Befund, der sich so nennt'. Wer die Herkunft des Namens für
den Nachweis nimmt, prüft nichts."*

**(c) holt das Urteil aus dem geladenen Modul**, statt es abzuschreiben — kennt
`zeitabdeckung.py` den Namen künftig nicht mehr, ist die Bedingung **nicht
prüfbar** ⇒ Rückgabewert **2**. *Eine Abschrift liefe gegen ein Urteil, das die
Prüfung gar nicht mehr vergibt: die Ausnahme griffe dann entweder nie oder
immer.*

### Der fünfte Fall: `kein_zeuge`

**Entschieden: nicht belegbar ist nicht zugelassen.** Und es ist **folgenlos**:

| | |
|---|---|
| Dateien mit `kein_zeuge` | **175** von 223 — 150 Aktien, 25 Krypto-1h |
| davon mit **irgendeinem** Befund | ⭐ **null** |

**Der Grund liegt im Aufbau von `pruefe_datei`:** Fehlt der feinere Zeuge, kehrt
die Funktion **vor** der Deckungsprüfung um und hinterlässt einen **Hinweis**,
keinen Befund. `rand_erste` entsteht ausschliesslich aus dieser Deckungsprüfung.
**Wo `kein_zeuge` steht, kann es keinen `rand_erste` geben.**

⚠️ **Streng wird die Regel erst in dem Fall, für den sie gedacht ist:** wenn eine
Eingabe von aussen einen Befund ohne Deckung behauptet, oder wenn einer Datei der
Zeuge künftig abhandenkommt. Probe `3aa`.

### Die Wache

**`shared/test_snapshot.py`: 110 → 164 Prüfungen**, rc=0. Acht neue Proben,
⭐ **sechs mit beissender Mutation** (die Fassung mit entfernter Bedingung muss
den Fehler **übersehen**). ⭐ **Die beiden übrigen ausdrücklich nicht, mit
Begründung:** `3ac` ist die Negativprobe — *„eine Probe, die nur rot sein kann,
beweist nichts"* —, `3ad` misst die **Abwesenheit** einer Flagge: *„eine Wache,
die man entfernen könnte, gibt es dort nicht."*

**Zwei Fälle liessen sich aus echten Kursdateien nicht herstellen** (ein
`rand_erste` an einer späteren Kerze, einer ohne Deckungsprüfung) — die heutige
`zeitabdeckung.py` vergibt beides nicht. **Sie werden gestellt**, weil
`snapshot.py` sich nicht darauf verlassen darf, dass seine Eingabe wohlgeformt
ist. Dass sie dennoch beissen, zeigen ihre Mutationen.

### ⚠️ Der Prüfer für Abschnitt 17 — und der Preis eines Fehlers von gestern

**Der Auftrag sagte: die Datei aus dem TB-48-Paket kommt ins Repo.** ⚠️ **Sie lag
den Unterlagen der Sitzung nicht bei** — das Archiv enthielt allein den
Auftragstext, und im Repo war sie nirgends, **weil die TB-48-Auflage sie draussen
gehalten hat.**

**Sie wurde aus der Belegtabelle des TB-48-Ergebnisses neu geschrieben**, und das
steht in der Datei selbst:

> ⭐ ***„Ein neu geschriebenes Werkzeug ist kein wiederhergestelltes."***

**Die Auflage „unverändert in der Sache" ist am Ergebnis geprüft, nicht am
Quelltext:** 19 Zahlen, `uebersprungen` leer, `nicht_pruefbar` leer, **genau eine
Abweichung**, Rückgabewert **1** — wie in TB-48. Selbsttest **24/24**.

⭐ **Zwei Zahlen fasst der Prüfer bewusst nicht an**, und das ist der Befund, nicht
seine Umgehung: `pandas_market_calendars` (17.5 sagt *„auf dem
Betriebsrechner"*) und die Drift-Messung aus 17.8 (braucht einen echten
yfinance-Abruf, nach T35.4 untersagt). ⭐ **Und die Jahreszahl 2022 wird aus dem
Registertext gelesen, nicht im Werkzeug hinterlegt** — sonst prüfte es seine
eigene Abschrift und meldete nach einer Berichtigung weiter die alte Abweichung.
**Verschwindet der Satz, ist das `nicht pruefbar` (2), nicht „in Ordnung".**

### ⚠️ Die 2019/2022-Frage — die Vermutung trägt nicht

**Vermutet war:** 2022 ist die früheste **Krypto**-Falte, 2019 die über alle
neun.

```
erstes Faltenjahr ueber alle neun Bots:        [2019]
erstes Faltenjahr ueber die fuenf Krypto-Bots: [2019]
```

⚠️ **Alle neun beginnen 2019, Krypto eingeschlossen.** Es sind nicht zwei
Fragen, sondern **eine Frage und zwei Antworten aus zwei
Faltenplan-Generationen.**

| | |
|---|---|
| **2019** | `research/faltenplan_neun/daten/faltenplan.json` — alle neun Bots, nach der Schranke `ERSTE_MOEGLICHE_FALTE = 2019` |
| ⚠️ **2022** | `research/krypto_historie/daten/faltenplan_nach_tb34.json` — **`mindesttraining: 4`, nur Krypto**, Symbolreihe `[3, 6, 9, 13]` — ⭐ **zeichengleich die Reihe aus T34.9** |

> ⭐ **Der schlagende Beleg stand im Register selbst.** Abschnitt **15.6** führt
> eine Faltenliste je Bot und nennt für die Krypto-Bots **ebenfalls 2019**. **Die
> 2022 in 17.3 widerspricht nicht einer Datei unter `research/`, sondern dem
> eigenen Registertext an einer zweiten Stelle.** *Damit ist „welche der beiden
> ist falsch" nicht mehr Auslegung, sondern abgelesen.*

⭐ **Der eigentliche Gehalt ist nicht die Jahreszahl, sondern dass zwei
Faltenpläne mit verschiedenen ersten Falten im Repo liegen und nur einer im
Register steht.** Das ist **T34.10**, seit dem 15.09. offen.

⭐ **Und die Schlussfolgerung trägt unabhängig davon:** Prüfung 16 rechnet
maschinell nach — **null** der 36 kurzen ersten Kerzen fällt in ein
Faltenfenster, in dem ihr Symbol geladen ist, über alle neun Bots und alle
Falten.

⚠️ **Eine Nebenbeobachtung, nicht aufgelöst:** `erstes_faltenjahr_ohne_schranke`
steht bei **acht von neun** Bots auf **2017 oder 2018**. Die 2019 kommt also aus
einer Schranke, nicht aus den Daten. **Ob diese Schranke im Register steht, ist
nicht nachgesehen.**

⚠️ **Kein Registertext ist geändert worden.** Der Auftrag sagte berichten.

### Die Randbedingungen

| | |
|---|---|
| Datenstand vorher = nachher | ✅ `d9449faf…`, 223 |
| Snapshot gezogen | ✅ **nein** — nur in Wegwerf-Verzeichnisse, aus einer **Kopie** von `data/` |
| Sperrlisten-Dateien | ✅ maschinell geprüft, **keine im Diff** |
| Basislauf | **58 grün / 3 rot / 3 ungeprüft / 1 Zeitgrenze = 65** — ⭐ einer mehr grün als in TB-48, und es ist der neue Test |
| ⭐ `git status --porcelain` | **zweimal genommen, vor und nach dem letzten Commit, beide im Beleg** — die zweite leer. *Dritter Versuch nach TB-46 und TB-48, erstes Mal richtig* |
| ⭐ Nebenbeweis aus TB-47 | überlebende Prozesse nach der Zeitgrenze: **0** |

### Der Mac-Lauf, 18.09. 15:05–15:57, Python 3.9.6

**Alles bestätigt, in jedem Punkt:**

| | |
|---|---|
| Trockenlauf | **rc 0**, 36 zugelassene Befunde mit Registerverweis |
| `rand_letzte` · nicht-abgeleiteter `rand_erste` | je **rc 2**, Datei genannt, **kein Snapshot** |
| `shared/test_snapshot.py` | **164/164**, ⭐ kein einziges `[FEHL` in der Ausgabe |
| ⭐ **die neunzehn Zahlen, erstmals auf dem Betriebsrechner** | **19 von 19 geprüft, genau eine Abweichung (Nr. 15), rc 1 — zeichengleich zur Cloud**, keine `nicht pruefbar` |
| Selbsttest des Prüfers | **24/24** |
| ⭐ `pandas_market_calendars` | **4.6.1** — Registertext 5f (17.5) trifft zu |
| Früheste Falte je Bot | **alle neun 2019** |
| Neun Datenbanken | ⭐ `diff vorher/nachher` **leer**, 9 Zeilen |
| Datenstand, `git status`, Snapshot-Ordner | identisch · leer · existiert nicht |

### ⚠️⚠️ Und der Mac fand einen Fehler, den die Cloud nicht sehen konnte — meinen

**In TB-47 hatte ich `system/test_log_rotation.py` aus `BEKANNT_ROT` gestrichen:**
*„auf BEIDEN Rechnern grün, 117/117. Ein falscher Eintrag in dieser Liste ist
teurer als gar keiner."*

**Zehn Einzelläufe auf dem Mac:**

| Lauf | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| | ⚠️ **116** | 117 | ⚠️ **116** | 117 | ⚠️ **116** | 117 | 117 | 117 | 117 | 117 |

**Immer `116 von 117`, immer eine zeitabhängige Probe zum Restfenster beim
Rotieren, ein bis zwei fehlende Zeilen von 238–512 — und die gefallene Probe
wechselt.** Rate **~30 %**.

> ⭐ ***„Die Streichung stützt sich auf je EINE Messung pro Rechner; bei ~30 %
> Flackerrate trifft eine Einzelmessung mit 70 % Wahrscheinlichkeit grün."***

⚠️ **Und es stand längst im Backlog — T38.10, seit dem 15.09.:** *„flattert —
Rennbedingung zwischen Sichern und Leeren."* **Ich habe einen dokumentierten
Befund mit einer Einzelmessung überstimmt, ohne im Backlog nachzusehen.**

**Beide Listen sind damit falsch, in entgegengesetzte Richtungen:**
`UMGEBUNGEN.md` sagt „bekannt rot", `basislauf.py` sagt „auf beiden Rechnern
gruen". ⭐ **Richtig: grün im Regelfall, zeitabhängig flackernd — kein
Zweigbefund, aber auch nicht „grün".**

⭐ **Daraus das neue Prüfprinzip A6: Eine Einzelmessung kann die Abwesenheit
eines flackernden Fehlers nicht belegen.**

### Drei Stellen, an denen der Lauf die Vorgabe korrigiert hat

| | |
|---|---|
| ⭐ **`$TMPDIR` statt nur `/tmp`** | Mein Testauftrag prüfte nur `/tmp` auf Wegwerf-Reste; die Sitzung mass zusätzlich `/var/folders/b_/…/T/`, *„wo `mkdtemp` auf dem Mac wirklich liegt"*. **Beide null.** *Ohne die Ergänzung hätte die Prüfung an der falschen Stelle gesucht und „sauber" gemeldet* — **A1** |
| **62 → 65 Testdateien** | die Zahl in `UMGEBUNGEN.md` stammt aus TB-45 und ist gealtert |
| **`pandas_market_calendars` fehlt in der Paketzeile** | obwohl Registertext 5f darauf verweist. Mac **4.6.1**, Cloud **5.4.0** |

⭐ **Gegenrichtung ebenfalls belegt:** `shared/test_zuteilung.py` ist auf dem Mac
**grün** — der Cloud-Rotbefund war eine Netzsperre, kein Fehler. Und nach der
Zeitgrenze von `test_drawdown_beide_masse.py`: **null überlebende Prozesse**,
wie seit TB-47.

### In einfacher Sprache

**Was wir wissen wollten:** Kann die eingefrorene Kopie der Kursdaten jetzt
gezogen werden — und bleibt die Prüfung dabei so streng wie vorher?

**Was herauskam:** Ja zu beidem. Der Nachweis ist eine einzige Zahl, die von 2
auf 0 gesprungen ist, **bei unverändert 36 gemeldeten Fällen.** Die Prüfung ist
also nicht weicher geworden, nur klüger. Eine Abkürzung zum Übergehen gibt es
ausdrücklich nicht; es wurde eigens nachgemessen, dass es sie nicht gibt.

**Warum das trägt:** Die Regel wurde an einer **absichtlich beschädigten Kopie**
der echten Daten ausprobiert. Wird die **letzte** Kerze angeschnitten — der
gefährliche Fall —, bricht das Programm ab und nennt die Datei. Die
Originaldaten wurden nicht angefasst.

⚠️ **Was falsch war:** Die Vermutung, die Jahreszahl 2022 in den Regeln sei für
die Kryptowährungen richtig. **Alle neun Programme beginnen 2019.** Die 2022
stammt aus einer älteren Planung mit einer anderen Vorgabe. ⭐ **Der Beweis stand
im Regeldokument selbst**, das an anderer Stelle für die Krypto-Programme
ebenfalls 2019 nennt.

**Der eigentliche Punkt ist nicht die Jahreszahl**, sondern dass zwei Planungen
mit verschiedenen Jahren im Projekt liegen — und welche gelten soll, ist eine
offene Entscheidung des Betreibers.

⚠️ **Und der Lauf auf dem MacBook hat noch einen zweiten Fehler von mir
gefunden.** Gestern hatte ich einen Testeintrag aus einer Liste gestrichen mit
der Begründung, dieser Test sei „auf beiden Rechnern grün". **Von zehn Läufen
waren drei rot** — jedes Mal an einer zeitabhängigen Stelle, jedes Mal an einer
anderen. Ich hatte **eine** Messung je Rechner; bei einem Fehler, der in drei von
zehn Fällen auftritt, sieht eine einzelne Messung mit 70 Prozent
Wahrscheinlichkeit gut aus. **Und im Projektplan stand seit dem 15. September,
dass dieser Test flattert.**

⭐ **Daraus wird eine Regel, und sie fehlte: Eine einzelne Messung kann nicht
belegen, dass ein sprunghafter Fehler nicht da ist.** Sie zeigt nur, dass er
diesmal nicht auftrat.
---

## BG — TB-55: die Sitzung, deren Ergebnis ein Nichthandeln ist

**19.09.2026. Cloud-Sitzung, Basis `main` = `origin/main` = `7e48e1f`.
Nichts committet ausser dem Ergebnisdokument.**

⭐ **Dies ist die erste Sitzung dieses Projekts, deren Ergebnis darin besteht,
dass sie die beauftragte Handlung nicht ausgeführt hat.**

---

### Was gemessen wurde, und es war alles in Ordnung

| | |
|---|---|
| `datenstand_hash` | `d9449faf…a995f84` · **223** Kursdateien — ⭐ **dreimal gemessen, dreimal identisch** |
| Dateien gesamt | **225** — genau `config/sp500_top150.txt` und `config/top25_symbols.txt`, ⚠️ **keine dritte** |
| Teilkerzen | **36** Befunde von **223** geprüften Dateien |
| davon zugelassen | ⭐ **36**, Herkunft *Abschnitt 17.3* · Arten `{'rand_erste': 36}` · Urteile `{'abgeleitete_teilkerze': 36}` |
| `nicht_zugelassen` | ⭐ **`[]` — leer** |
| Rückgabewert / stderr | **0** / **0 Byte** |

⭐ **Damit ist die Ausnahme aus 17.3 vollständig gedeckt:** kein Befund wäre
ohne sie durchgerutscht, und keiner ist von ihr nicht gedeckt.

⭐ **Und Messung 2 rechnet an der Quelle:** `herkunft.py::datenstand('data')`
importiert und direkt aufgerufen — nicht dreimal dasselbe Werkzeug.

---

### Warum trotzdem nicht gezogen wurde

**Nicht eine der Abweichungen betrifft eine Zahl. Alle betreffen die
Umgebung.**

| | Soll (Auftrag) | Tatsächlich |
|---|---|---|
| Interpreter | `trading-env/bin/python3` (**3.9.6** auf dem Mac) | `/usr/local/bin/python3`, **3.11.15** — `trading-env/` existiert hier nicht |
| Schritt 0 | neun `*.db` quersummen **und kopieren** | ⚠️ **keine einzige vorhanden** (gitignoriert, nur auf dem Mac) — die Sicherung ist **strukturell nicht herstellbar** |
| Zweig | `main`, kein eigener Zweig | Sitzungsmandat: eigener Zweig, Push auf `main` untersagt |
| Ort | *„diese Aufgabe **ist** der Mac-Lauf"* | **kein Mac-Lauf** |

> ⭐ **Der Satz, auf den es ankam, und er stammt aus dem Bericht:** *„Daraus
> folgt: ein Zug auf dem Mac wird sehr wahrscheinlich denselben `snapshot_hash`
> ergeben. Es folgt aber **nicht**, dass dieser Lauf ihn ziehen durfte."*

⭐ **Die Sitzung hat die Gegenargumente selbst aufgeschrieben**, statt sie zu
verschweigen — Arbeitsbaum sauber, alle 225 Dateien versioniert,
`.gitattributes` nicht vorhanden, Rechnung nur mit Standardbibliothek. **Und
hat trotzdem nicht gezogen.**

**Der Betreiber hat auf Rückfrage bestätigt:** *„Nicht ziehen, nur
berichten."*

---

### ⭐⭐ Der Gewinn, der nicht bestellt war

```
63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
```

**Dieselbe Zahl, dreimal gerechnet, auf zwei Maschinen:**

| Lauf | Maschine | Interpreter | Art |
|---|---|---|---|
| **TB-49**, 18.09. | Cloud | 3.11.x | ⭐ **echter Zug**: `GEZOGEN - 225 Datei(en), 211.0 MB, jede byteweise gegen die Quelle geprueft`, Nachprüfung `UNVERAENDERT` |
| **TB-49**, 18.09. | MacBook | **3.9.6** | Trockenlauf, rc 0 |
| **TB-55**, 19.09. | Cloud | 3.11.15 | Trockenlauf, rc 0 |

⚠️ **Was das nicht ist:** nicht F1b/Q2 — die fragt nach der Reproduktion des
**gezogenen** Snapshots aus dem Repo, und es gibt bis heute **einen** echten
Zug, in ein Wegwerf-Verzeichnis. ⚠️ **Und nichts über den Bestand:** alle drei
lasen denselben. *Gleiche Eingabe → gleiche Ausgabe ist das Mindeste einer
Hash-Funktion.*

⭐ **Was es ist:** Der Name ist **unabhängig von Maschine und
Python-Nebenversion** — und er steht **vor** dem Zug fest. ⚠️ **Meldet der Mac
etwas anderes, wird nicht gezogen, sondern geklärt.**

---

### ⚠️⚠️ Der Befund über die Projektführung

**Der Auftrag nennt den Mac an drei Stellen — und macht den Ort an keiner zum
Abbruchkriterium.** Die Abbruchkriterien nannten ausschliesslich Zahlen.

⭐ **Die Sitzung hat den Abbruch selbst abgeleitet und zusätzlich gefragt.**
⚠️ **Bei der einen unwiederholbaren Handlung dieses Projekts darf die
Absicherung nicht am Urteil der Sitzung und an der Anwesenheit des Betreibers
hängen.**

⇒ ⭐ **Schritt −1 Ortsprüfung**, ab sofort in jedem `MAC_`-Auftrag:
`uname -s` = `Darwin` · `test -x trading-env/bin/python3` · Version 3.9.x ·
neun `*.db` auffindbar · `~/trading-bot` auf `main`. ⚠️ **Weicht eine ab:
Auftrag beendet** — nicht ziehen, nicht ersatzweise trocken laufen, nicht den
Interpreter austauschen.

> ⭐ **Der Satz, der die Regel trägt:** *Der Zug ist nicht wiederholbar; der
> Abbruch ist es.*

**`MAC_TB-55_snapshot_ziehen_v2.md`:** **+31 Zeilen, 0 entfernt, 2
Einfügestellen** — mit `diff` gemessen, nicht geschätzt.

---

### ⚠️ Zwei Berichtigungen an eigenen Aussagen

| | |
|---|---|
| **1** | Ich hatte behauptet, `63e4b6c8…` sei **auch in den TB-52-Berichten** aufgetaucht. **Gegengezählt: 0 Treffer in beiden TB-52-Archiven.** Er kommt aus TB-49 (Cloud **und** Mac) und TB-55. *Der Beleg wird dadurch nicht schwächer, aber die Aussage war falsch* |
| **2** | ⚠️ **Nummernkollision im Backlog:** Nachtrag (g) hat Rang **0,86** für „TB-55 = Faltenschranke + Berichtigung 17.3" vergeben; **formuliert und ausgeführt wurde unter TB-55 der Snapshot.** Aufgelöst in Nachtrag (h): **0,86 = Snapshot**, **0,87 = TB-56 Faltenschranke**. Nach F17 eine **Berichtigung** — sie löst einen Widerspruch innerhalb des Backlogs auf |

---

### ⚠️ Was der Registerprüfer nicht gesagt hat

Er meldet **`KEIN BEFUND`** — und im Nebensatz:
`Quelle beleg: dokument (Trockenlauf nicht lauffaehig: No module named
'pandas')`.

⚠️⚠️ **Fall von A1: ein fehlgeschlagener Aufruf und ein leeres Ergebnis sehen
gleich aus.** Das Urteil ist nicht falsch — auf dem Mac rechnet er wirklich —,
**aber ein Glied der Kette ist Papier statt Messung, und das steht nicht im
Urteil, sondern daneben.** ⇒ **T55.7.**

---

### Der Stand nach dieser Sitzung

| | |
|---|---|
| `data/` | ⭐ **unberührt** — `git status --porcelain -- data` leer, dreimal derselbe Hash |
| `snapshots/` | **existiert nicht** — weder dort noch unter `data/snapshots/` |
| `.gitignore` | **nicht geändert** — `git check-ignore` Rückgabewert **1**, von keinem Muster erfasst |
| Sperrliste, `shared/snapshot.py`, `shared/paths.py` | **unberührt** |
| Register | **kein Text geändert** |
| `size-pack` | **114.77 MiB** · `in-pack` **2496** — ⭐ Ausgangswert für die Zuwachsmessung auf dem Mac |
| Auftrag | ⭐ **unverbraucht**, jetzt als v2 mit Ortsprüfung |

---

### In einfacher Sprache

**Die eingefrorene Kopie der Kursdaten wurde nicht angelegt — und das war
richtig.** Alle inhaltlichen Prüfungen waren in Ordnung, jede einzelne. Aber
der Lauf fand auf dem falschen Rechner statt: In der Cloud fehlen das
vorgeschriebene Python und die neun Datenbanken, die vorher gesichert werden
sollen.

**Der Fehler lag in der Aufgabenstellung.** Sie sagte dreimal, dass sie für den
Mac ist, aber nie: *prüfe das zuerst und höre sonst auf.* Ab jetzt steht das als
erster Schritt in jedem Mac-Auftrag.

**Und es kam etwas heraus, das nicht bestellt war:** Der Name, den die Kopie
tragen wird, ist inzwischen auf zwei verschiedenen Rechnern mit zwei
verschiedenen Python-Versionen gerechnet worden und dreimal gleich
herausgekommen. ⚠️ **Nennt der Mac sie anders, wird nicht gezogen, sondern
nachgeforscht.**

---

## BH — TB-55: der Eingabezustand existiert

**19.09.2026, auf dem MacBook. `main`, Basis `7e48e1f` → Commits `1075dec`
(Snapshot) und `4c80588` (Ergebnisdokument), beide gepusht.
Interpreter durchgehend `trading-env/bin/python3` = Python 3.9.6.**

⭐⭐ **Die eine Handlung dieses Projekts, die sich nicht wiederholen lässt, ist
vollzogen.**

```
63e4b6c8bb71dc3749dd566172ca16d24f9dda0f904d058eacb440653cb2ceb2
```

---

### Die Zahlen, aus dem Manifest gelesen

| | |
|---|---|
| Dateien | **225** = 223 Kursdateien + `config/sp500_top150.txt` + `config/top25_symbols.txt` — **keine dritte** |
| Bytes gesamt | **211 040 678** |
| Zeitpunkt (UTC) | **2026-09-19T06:49:32+00:00** |
| `datenstand_hash` | `d9449faf…a995f84`, **223** — ⭐ **dreimal gemessen** (06:46, 06:49, 06:52 UTC), dreimal gleich |
| Zugelassene Befunde | **36**, alle `rand_erste`, *Abschnitt 17.3* · `nicht_zugelassen` **leer** |
| Zug | `GEZOGEN - 225 Datei(en), 211.0 MB, **jede byteweise gegen die Quelle geprueft**`, rc 0 |
| Nachprüfung | ⭐ **`UNVERAENDERT`**, Soll = Ist für **beide** Hashes, rc 0 |
| `.gitignore` | **nicht geändert** — `snapshots/` war nie erfasst |
| Datenbanken | **12** gesichert (nicht neun), am Ende **12/12** byteweise identisch |

---

### ⭐⭐ Fünf unabhängige Belege — und der stärkste war nicht bestellt

| # | |
|---|---|
| **1** | Byteweise Prüfung **beim Kopieren**, alle 225 |
| **2** | `--pruefen` **danach**: `UNVERAENDERT` |
| **3** | ⭐⭐ **`git rev-list` + `cat-file`: 1 Commit, 4 Trees, 1 Blob — der eine Blob ist das Manifest.** *Für keine der 225 Dateien wurde ein neuer Blob angelegt. git adressiert über den Inhalt — es bezeugt die Byte-Gleichheit mit `data/`, ohne unser Werkzeug zu kennen* |
| **4** | Der Registerprüfer lief in einem Worktree auf `7e48e1f` und mass dort ebenfalls `d9449faf…`/223 — ⭐ **der versionierte Inhalt ist gleich dem Arbeitsbaum**, vorher nie gemessen |
| **5** | Der Name ist **viermal** gerechnet: TB-49 Cloud (echter Zug, 3.11) · TB-49 Mac (3.9.6) · TB-55 Cloud (3.11.15) · **TB-55 Mac (3.9.6, dieser Zug)** |

⭐ **Beleg 3 entstand aus der Zuwachsmessung, die nur die Kosten prüfen sollte.**

---

### ⚠️ Die Abweichung von TB-46, und wie sie behandelt wurde

**Erwartet +0,001 %. Gemessen: +6 lose Objekte, +0,04 MiB (0,026 %), `du`
+80 KiB (0,048 %), `size-pack` unverändert.**

**Erklärung:** TB-46 mass den *Packfile*-Zuwachs von 30 Dateien **ohne
Manifest**; hier kommen ein 133-KB-Manifest und vier Tree-Objekte für 226
Einträge mit 64-stelligen Pfadnamen hinzu — und der Nenner ist ein Repo aus
**156 MiB losen** Objekten bei 3,4 MiB Packfile.

> ⭐⭐ **Der Schluss, von der Sitzung selbst gezogen:** *„Die strukturelle
> Aussage, auf die es ankam — gleiche Inhalte einmal — ist mit ‚1 Blob' direkt
> belegt."*
>
> ⭐ **Eine Kostenmessung ist nie die Aussage, sondern ihr Stellvertreter.
> Weicht der Stellvertreter ab, wird die Aussage direkt geprüft.**

---

### ⭐⭐ Ein offengelegter Fehler, und daraus ein neues Prüfprinzip

> *„Der ‚vorher'-Lauf wurde erst **nach** dem Commit nachgeholt, weil ich ihn
> vor dem Commit übersprungen hatte. Statt zu behaupten, er wäre gleichwertig,
> habe ich den Stand `7e48e1f` als Worktree ausgecheckt und den Prüfer dort
> laufen lassen."*

⭐ **Nicht als „gemacht" verbucht. Nicht als gleichwertig behauptet.
Rekonstruiert — und als Rekonstruktion benannt.**

⇒ **A7:** *„Eine nachgeholte Vorher-Messung ist nur dann eine Vorher-Messung,
wenn der Zustand inhaltsadressiert wiederherstellbar ist — und sie muss sagen,
dass sie nachgeholt wurde."* ⚠️ **Bei Uhrzeit, Umgebung oder laufenden
Prozessen wäre dasselbe Vorgehen wertlos gewesen.**

**Ein zweiter benannter Fehler:** das erste Leseskript der Sitzung nahm an, die
Kursdateien stünden im Manifest mit Präfix `data/`; sie stehen flach. ⭐ *„Das
Manifest selbst war nie in Frage — nur meine Annahme über seine Form."*

---

### Was die Cron-Prüfung ergab

**22 aktive Einträge**, nur Zeitfelder ausgegeben, **kein Befehl**.
Abruf-Zähler **0**. `*/5` und `*/15` feuerten um 08:45 und 08:50 **während**
der Sitzung — ⭐ **ohne Wirkung auf eine einzige der 12 Datenbanken.**
`broker_testnet_t3_supertrend.db` um 08:05 passt zu `5 */4 * * *`.

⭐ **T46.4 („kein Datencron") war eine Regel. Jetzt ist sie gemessen.**

---

### ⚠️ Zwei fremde `MANIFEST.json`

`data_sicherung/2026-09-15_115131/` (TB-34-Sicherung, gitignoriert) und
`research/hrp_portfolio/corrected_curves_original/` (versioniert). **Beide sind
keine Snapshots.** ⚠️ **Die Abbruchregel „existiert schon einer" hätte hier
falsch auslösen können** — das Kennzeichen ist der Ordnername
`snapshots/<64 Hex>/`, nicht die Anwesenheit einer Manifestdatei.

---

### Der Stand nach dieser Sitzung

| | |
|---|---|
| Snapshot | ⭐ **existiert**, versioniert, gepusht, `UNVERAENDERT` |
| `data/` | unberührt, dreimal gemessen |
| Sperrliste, `shared/snapshot.py`, `shared/paths.py` | **unberührt** |
| Register | ⚠️ **noch kein Eintrag** — TB-55b folgt |
| Die 0-Byte-Doppelgängerin | **mitgesichert, nicht gelöscht** — Beweismaterial für TB-53 |
| Registerprüfer | vorher **und** nachher **KEIN BEFUND** |
| `git status --porcelain` | **0 Zeilen** |

---

### In einfacher Sprache

**Die eingefrorene Kopie aller Kursdaten existiert.** Sie heisst nach ihrem
Inhalt, liegt im Projekt und ist hochgeladen. Ab jetzt ist sie die Grundlage
des Auswahllaufs — und sie lässt sich Jahre später noch nachprüfen.

**Fünf getrennte Gründe sprechen dafür, dass sie stimmt.** Der schönste: beim
Einchecken brauchte git für keine einzige der 225 Dateien neuen Speicher. git
legt gleiche Inhalte nur einmal ab — **dass es nichts Neues anlegte, heisst,
die Kopie ist identisch, und das sagt ein Programm, das unser Werkzeug gar
nicht kennt.**

**Was noch fehlt:** Die Zahl muss ins Regelwerk. Das ist klein — aber es ist
der Schritt, auf den alles andere wartet.

---

## BI — TB-55b: der Snapshot steht im Register

**19.09.2026. `main`, `4c80588` → `0fe61d7`, gepusht. Python 3.9.6.**

`docs/VORREGISTRIERUNG_neuselektion.md` hat einen neuen **Abschnitt 18** —
eine **Tatsachennotiz** zu Registertext 5 / 5a, in der Form von 15.6.
**62 Zeilen hinzugefügt, 0 entfernt.**

⭐⭐ **Keine Zahl im Eintrag ist getippt.** Ein Skript liest `MANIFEST.json`
per `json.load`, holt den Commit aus `git log -- snapshots/`, prüft
`origin/main` per `git branch -r --contains` und misst die höchste
Abschnittsnummer selbst (`assert neu == 18`). Vorher **8/8 Werte maschinell**
gegen die Auftragsliterale verglichen, String- **und** Typgleichheit.

### ⭐⭐ Aus einer Falle wurde Dokumentation

Abschnitt **17.9** führt `snapshot_hash` = **`4fee547d…`** — die TB-47-Messung
über die **223 Kursdateien allein**, vor dem Ziehen. ⚠️ **Das ist die Stelle,
an der später jemand die falsche Zahl abschreibt.**

Abschnitt 18 grenzt sie ausdrücklich ab: *„`63e4b6c8…` läuft über die 225
Dateien; `4fee547d…` lief nur über die 223 Kursdateien und bezeichnet nicht
diesen Snapshot. Beide bleiben richtig; sie beantworten verschiedene Fragen."*

### ⚠️⚠️ Und dort wurde gegen den Wortlaut eines Abbruchkriteriums entschieden

Der Auftrag sagte: *„Gibt es einen Snapshot-Abschnitt **mit einer Zahl darin**:
ABBRUCH."* 17.9 enthält eine. ⭐ **Die Sitzung entschied nach dem Zweck, schrieb
es hin und nannte den Commit zur Nachprüfung.**

| | |
|---|---|
| ⭐ | **Die Entscheidung war richtig** — `4fee547d…` ist kein Duplikat |
| ⚠️⚠️ | **Die Regel war schlecht geschrieben, und das liegt beim Auftraggeber.** *„Eine Zahl darin"* war ein **Stellvertreter** für *„ein Eintrag, der DIESEN Snapshot bezeichnet"* |

⇒ **Zwei Regeln:** *Ein Abbruchkriterium benennt die Sache, nie ihren
Stellvertreter.* · *Fallen Wortlaut und Zweck auseinander und ist der Betreiber
erreichbar — fragen, nicht entscheiden.*

⚠️ **Ein Befund über ein Dokument des Betreuers:** Die Angabe „Python 3.11.15"
in Abschnitt 18 hat **keinen Beleg im Repo**. ⇒ **Jede Behauptung im Register
braucht ihren Beleg im Repo. Ein Beleg in `~/Downloads` ist kein Beleg.**

⭐ **Warum Abschnitt 18 und nicht 17.12** — besser begründet als beauftragt:
Abschnitt 17 ist der TB-48-Nachtrag vom 18.09. und sagt in **17.11**
ausdrücklich *„Kein Snapshot gezogen"*.

---

## BJ — TB-54: acht Nachträge, eine Rückfrage

**19.09.2026. `main`, `1124880` → `d9f3c4b` (d–g) → `3121ec2` (h–k), gepusht.**

**`BACKLOG.md` 764 → 929 Zeilen, 167 hinzu / 2 entfernt.** Sieben neue Blöcke
**2j, 2k, 2m, 2n, 2o, 2p, 2q**, sechs ersetzte Kettenzeilen — ⭐ **jede alte
Zeile steht wörtlich darunter**, als ersetzt gekennzeichnet und datiert.

### ⭐⭐ Die Regel aus TB-55b hielt, eine Stunde nach ihrer Formulierung

Nachtrag (h) wollte die Faltenschranke als **`0,87`** eintragen. **`0,87` war
belegt.** ⭐ **Die Sitzung fragte, statt zu entscheiden.** Betreiberentscheidung:
**`0,88` mit Vermerk.** **(d)–(g) waren bereits als Teilerfolg committet** —
der Teilerfolg war der eingebaute Weg, kein Notbehelf.

### ⭐⭐ Ein A1-Fall, den die Sitzung selbst fand

Vier Nachträge ersetzen Kettenzeilen, die **derselbe Arbeitsbaum** erst angelegt
hatte. ⚠️ **Gegen `HEAD` sind solche Ersetzungen unsichtbar** — `numstat` hätte
„0 entfernt" gemeldet. ⭐ **Deshalb zweifach gemessen**: kumulativ gegen `HEAD`
**und** gegen eine Kopie des Standes davor. **171/6 in Schritten, 167/2 gesamt;
die Differenz 4/4 vollständig zugeordnet.**

⭐ **Jede Einfügung lief über einen Anker, der genau einmal vorkommen muss** —
zwei Abbrüche **vor dem Schreiben**, Datei unverändert.

### ⚠️⚠️ Drei Nummernkollisionen, alle aus Nachträgen des Betreuers

`0,87` doppelt · **`V1` jetzt zweimal** (Abschnitt 2 und Block 2o) ·
**„TB-54" bezeichnet zwei Vorhaben** (Lese-Audit und Backlog-Nachträge).

⇒ ⭐ **Ein Nachtrag nennt keine konkrete Nummer, die er nicht selbst gemessen
hat.** Er sagt *„die nächste freie Nummer, gemessen"*; die Nummer vergibt die
ausführende Sitzung.

### ⚠️⚠️ Und ein Befund über die Arbeitsweise selbst

**Die Kette ist numerisch unsortiert** — `0,87` vor `0,86`, ersetzte Zeilen
zwischen aktiven. ⭐ **Die Sitzung hat bewusst nicht umsortiert**, weil das
entfernte Zeilen erzeugt hätte.

> ⭐⭐ **Der Kern: Wir wenden Register-Disziplin auf ein Arbeitsdokument an.**
> „Nur hinzufügen" ist richtig für `VORREGISTRIERUNG_neuselektion.md` — dort
> schützt es die Nachvollziehbarkeit des Laufs. ⚠️ **`BACKLOG.md` ist kein
> Registertext; dort schützt dieselbe Regel nichts und kostet Lesbarkeit.**

**Betreiberentscheidung erforderlich.**

⭐ **Ohne Auftrag getan, und richtig:** Sieben Nachtragsdateien wanderten nach
`docs/projektfuehrung/nachtraege/`, byteidentisch per `cmp` — *„Ein Beleg in
`~/Downloads` ist kein Beleg."*

---

### Der Stand am Ende des 19.09.

| | |
|---|---|
| Snapshot | ⭐ gezogen (`1075dec`), **registriert** (Abschnitt 18), `--pruefen` `UNVERAENDERT` |
| Backlog | ⭐ **(d)–(k) eingearbeitet**, 929 Zeilen |
| Datenstand | `d9449faf…`/223 — an diesem Tag **neunmal** gemessen, neunmal gleich |
| 12 Datenbanken | in allen drei Sitzungen **12/12** byteweise identisch |
| Registerprüfer | in jeder Sitzung vorher und nachher **KEIN BEFUND**, `Quelle beleg: trockenlauf` |
| Offen | Journal · A7 · die drei Kollisionen · die Kettensortierung · F1b/Q2 · TB-53 · die Faltenschranke |

---

### In einfacher Sprache

**Das Regelwerk weiss jetzt, worauf gerechnet wird**, und die Vorhabenliste ist
auf dem Stand von heute. Nichts ist verloren gegangen: Wo eine Zeile ersetzt
wurde, steht die alte darunter, mit Datum.

⭐ **Zweimal an diesem Tag hat eine Sitzung gefragt, statt zu entscheiden** —
einmal beim Ziehen, einmal bei einer doppelt vergebenen Nummer. **Beide Male
war die Frage die richtige Antwort.**

⚠️ **Und dreimal haben sich Nummern überschnitten, alle drei durch den
Betreuer**, der Nummern vergab, ohne den Zielstand zu kennen. Ab jetzt sagt er
nur noch „die nächste freie" und begründet, wohin etwas gehört.

---

## Wiederkehrende Lehren

- **Frontend-Prüfungen je Funktion, nicht im ganzen Dokument.** Diese
  Fehlerklasse trat in #62, #66, #67, #73 und #77 auf — fünfmal.
- **Mutationsproben, die den Zustand von Hand herstellen, bestätigen sich
  selbst.** Aufgetreten bei #73 (M7/M12), #77 (M6), #78 (M2), **#79 (M12)**. Die
  Prüfung muss den **Ablauf** beobachten, nicht das Ergebnis.
- **Eine zweite Wache verdeckt das Fehlen der ersten.** In #73 maskierte eine
  dritte Notbremsen-Prüfung die fehlende zweite; in #79 deckte die Pfadgrenze
  den fehlenden Symlink-Schutz ab, weil der Testfall nach *aussen* zeigte. Wer
  eine Zusicherung prüfen will, muss den Fall so wählen, dass **nur** sie greifen
  kann. *(neu aus #79)*
- **Eine Probe kann sich selbst blind machen.** In #79 verlangsamte die Probe
  `os.fsync`, um eine Reihenfolge zu prüfen — und verhinderte damit, dass die
  Rotation den geprüften Schritt überhaupt erreichte. Grün, ohne etwas geprüft zu
  haben. *(neu aus #79)*
- **Eine geschätzte Obergrenze ist keine Zusicherung.** In #79 hätte die zuerst
  geschätzte Verlustgrenze die Mutation durchgelassen; erst die Messung beider
  Fälle (richtig: max 1, mutiert: min 6) ergab eine Grenze mit Trennschärfe.
  *(neu aus #79)*
- **Nach Neustart oder Update immer `pmset -g assertions` prüfen.** Eine reine
  Dienst- und Cron-Prüfung übersieht, ob der Mac überhaupt wachgehalten wird.
- **Cron holt verpasste Läufe nie nach.** Ein schlafender Mac heisst nicht
  „später", sondern „gar nicht".
- **Zahlen in Dokumentation veralten unbemerkt.** Eine Zahl, die es nicht gibt,
  kann nicht veralten. *(Beispiel aus diesem Nachzug: A3 nannte „über 100
  Prüfungen" — es sind 4 übersprungene Prüfungen der Suite über 143 einzelnen
  JS-Zusicherungen. Beides stimmt, die Zahlen bedeuten aber Verschiedenes.)*
- **Ein grüner Testlauf kann eine fehlende Abhängigkeit verbergen.** Ohne `node`
  meldet die Dashboard-Suite 780/780 — nicht „4 übersprungen". *(neu, bei A3
  geprüft)*
- ⚠️ **Ein gescheiterter Aufruf und ein leeres Ergebnis sehen gleich aus — und
  werden als Erfolg gelesen.** Bei einem git-Vergleich, der mit `rc=128`
  abbricht, kommt dieselbe leere Ausgabe zurück wie bei „keine Datei verändert".
  Zwei Wachen meldeten dadurch **„bestanden", eine davon mit 28 grünen
  Prüfungen, ohne etwas gemessen zu haben.** **Der Rückgabewert wird geprüft,
  bevor das Ergebnis gelesen wird.** *(neu aus TB-45)*
- ⚠️ **Ein Test, der ein Argument verlangt, ist nicht rot, sondern ungeprüft.**
  Drei Tests im Repo geben ohne Bot-Argument nur ihre Nutzungszeile aus und
  beenden mit `rc=1`. Ein Basislauf erreicht sie **nie** — wer „alle Tests grün"
  schreibt, meint sie nicht. *(neu aus dem TB-45-Maclauf)*
- ⚠️ **Eine C-Funktion ist kein Deskriptor, eine Python-Funktion schon.** Wer im
  Klassenrumpf die eine durch die andere ersetzt, verschiebt die Argumente um
  eins — und die Wache lässt still durch, was sie verhindern sollte. *(neu aus
  TB-44)*
- **Grün in der Cloud heisst strukturell nicht grün auf dem Mac**, und
  **die Cloud ist nicht eine Umgebung, sondern eine je Sitzung.** Daher
  `docs/UMGEBUNGEN.md` — ⚠️ **und die Regel, Abweichungen davon zu MELDEN**, weil
  die Datei altert und am Tag ihrer Anlage bereits zwei falsche Angaben enthielt.
  *(neu aus TB-44/TB-45)*
- ⚠️ **Eine Wache am Eingang prüft die Eingabe, nicht das Verhalten.** Wer seinen
  Pfad selbst baut, kommt an ihr vorbei — sie hat nichts zu beanstanden, **weil
  das Geprüfte in Ordnung ist.** Es braucht eine Schicht je Art des Vergessens:
  den Resolver, der verweigert · den statischen Test, der die Selbstbauer findet ·
  den Audit, der zeigt, was wirklich gelesen wurde. *(neu aus TB-46)*
- ⚠️ **Ein Name darf nicht aus einer Beschreibung gerechnet werden, sondern aus
  der Sache.** Ein Hash über Manifest-Einträge hinge von der
  Metadaten-Formatierung ab — ein Feld mehr, ein anderer Name für denselben
  Inhalt. *(neu aus TB-46)*
- ⚠️ **Die Wanduhr im Auswertungspfad.** Ein `now()` oder `today()`, das die
  Historie kappt, macht denselben Datenbestand an zwei Tagen zu zwei Ergebnissen
  — **und die Gegenprobe findet es nur, wenn sie an einem anderen Tag läuft.**
  Das Bezugsdatum kommt aus dem Register, nie aus der Uhr. *(neu aus TB-46)*
- ⭐ **Am Syntaxbaum messen, nicht mit Textsuche.** Zwei `forward_test.py`
  **nennen** `data/` in einer Protokollzeile, ohne einen Pfad zu bauen. Eine
  Textsuche hätte den ganzen Umbau blockiert. *(neu aus TB-46)*
- ⚠️ **Eine Zahl berichten heisst nicht, sie verstanden zu haben.** Wir haben
  gemessen „Offene Papier-Positionen: 0" und **nicht gefragt, wie die Null
  zustande kommt** — „kauft nichts" und „verkauft alles" sehen darin gleich aus.
  *(neu aus der Fable-Runde zu TB-45/46)*
- ⚠️ **Vor dem Merge gegen die Merge-Basis vergleichen.** `git diff main..zweig`
  zeigt alles Neuere auf `main` als Löschung — fünfmal aufgetreten. Die
  Drei-Punkt-Form löst das, sieht dafür **unkommittierte** Änderungen nicht mehr;
  nur `git merge-base` löst beides. *(gemessen in TB-45)*

- **Eine gute Zahl ist zuerst verdaechtig, nicht erfreulich.** Die −1,43 %
  kombinierter Drawdown galten zwei Wochen lang als Beleg fuer Diversifikation.
  ⚠️ **KORRIGIERT am 14.09.2026:** Die urspruengliche Vermutung („das Buch
  besteht meist aus Kasse") ist **widerlegt** (L.1) — an keinem von 1 618 Tagen
  war es flach. Die tatsaechlichen Ursachen waren **drei andere**: veraltete
  Dateien, falscher Nenner (gemessen am ganzen Buch statt am investierten
  Kapital) und ein **falscher Vergleichspartner** (ein Bot bei voller Gewichtung
  gegen ein Buch, in dem er ein Viertel wiegt).
- **Ein Zeitfenster-Filter behebt keine Auswahlverzerrung.**
  `RECENT_YEARS_ONLY=10` begrenzt, wie weit zurück gerechnet wird — nicht,
  welche Titel im Universum sind. „Top 150 nach heutiger Marktkapitalisierung"
  bleibt survivorship-verzerrt, und der Buy-and-Hold-Gegencheck auf demselben
  Universum ebenso. *(neu, 12.09.2026)*
- **Diversifikation über Indikatoren ist keine über Ertragsquellen.** Neun Bots
  mit neun Indikatoren können zwei Wetten sein. *(neu, 12.09.2026)*
- **Zwei Zahlen nebeneinanderstellen heisst nicht, dass sie vergleichbar
  sind.** „−22,20 % beim schlechtesten Einzelbot gegen −1,43 % kombiniert" hat
  einen Bot bei voller Gewichtung mit einem Buch verglichen, in dem derselbe Bot
  ein Viertel wiegt. Der richtige Vergleich (mittlerer Einzelbot gegen
  kombiniert) ergibt −17,93 % gegen −11,47 %. *(neu aus PR #84)*
- **Kennzahlen aus Kapitalkurven, die nur an Ausstiegstagen springen, sind
  mechanisch verzerrt.** Korrelationen nahe null entstehen dort aus den Nullen
  dazwischen, nicht aus Unabhaengigkeit. Wer Zusammenhang messen will, muss zu
  Marktpreisen bewerten. *(neu aus PR #84)*
- **Code-Synchronitaet ist nicht Ergebnis-Synchronitaet.** Die Sync-Reihe hat
  Backtest und Live-Konfiguration in Ordnung gebracht — die daneben liegenden
  `results/*.csv` blieben stehen und speisen bis heute zwei Anzeigen.
  *(neu aus PR #84)*
- **Eine Rangfolge, die gegen die Sortierung einer Konfigurationsdatei nicht
  stabil ist, ist keine Rangfolge.** Bei drei Bots haette eine alphabetisch
  sortierte `sp500_top150.txt` zu anderen Live-Parametern gefuehrt.
  *(neu aus der Drawdown-Untersuchung)*
- **Parameter nach dem einen Mass waehlen und Bots nach dem anderen beurteilen**
  ist eine Inkonsistenz, die jahrelang unbemerkt bleibt. Bei drei Bots laeuft das
  Auswahlmass sogar **umgekehrt** zum Beurteilungsmass.
  *(neu aus der Drawdown-Untersuchung)*
- **Ein späterer Nachtrag schlägt einen früheren — nicht nur die
  Gesamteinschätzung.** Beim HRP-Bericht drehte Nachtrag V am selben Tag zurück,
  was Nachtrag Z ergeben hatte. Wer bei Z aufhört, liest das Gegenteil des
  gültigen Urteils. *(neu aus TB-13, und mir selbst passiert)*
- **Jeder Mechanismus, der die Ertragsverteilung oben beschneidet, kostet bei
  diesen Bots mehr, als er an Risiko spart.** Vol-Skalierung verkleinert die
  Position, wenn Trendfolger am meisten verdienen; ein Trailing-Stop beendet sie,
  sobald die Bewegung stockt. Zwei völlig verschiedene Mechanismen, unabhängig
  dasselbe Muster. *(neu aus TB-13)*
- ~~**Der Engpass ist das Positionslimit, nicht das Kapital**~~ ⚠️ **KORRIGIERT
  am 14.09.2026:** Diese Lehre stammte aus einer Datei mit 115 Ueberspruengen.
  **TB-23 hat auf dem Kapitalpfad gemessen und das Gegenteil gefunden:** Bei
  `turtle_soup_stocks` (kein Positionslimit) und `volatility_breakout` (Limit 15
  bei zehn finanzierbaren Positionen) bindet die **Kapitalschranke** — ueber
  **3 100** bzw. **3 049** abgelehnte Trades. Die richtige Fassung: **Welcher
  Engpass bindet, ist je Bot verschieden und muss gemessen werden.**
- **Eine Abweichung, die kein Parameter ist, findet keine Konstanten-Prüfung.**
  Der BTC-Regimefilter fehlte im Backtest als *Verhalten* und durchdrang dadurch
  alle fünf Profitabilitäts-Studien. *(neu aus TB-13)*
- **Eine Zahl, die von der Sortierimplementierung abhängt, ist keine Messung.**
  `sort_values("time")` ohne `kind="stable"` liefert bei gleichen Zeitstempeln
  eine beliebige Reihenfolge — und damit einen anderen Drawdown.
  *(neu aus PR #86)*
- **Was auf dem Mac liegt, liegt nicht zwingend im Repo.** Ich habe in TB-15
  vom Arbeitsordner auf den versionierten Stand geschlossen — die
  Dashboard-Vorlage gab es dort nie, dafür war die Telegram-Vorlage längst da.
  Eine Cloud-Sitzung sieht **nur** den versionierten Stand.
  *(neu aus TB-15)*
- **Eine als „erschlossen" markierte Annahme ist eine Schuld, keine
  Zusicherung.** Sie hält genau so lange, bis jemand nachsieht. Die
  Kennzeichnung **belegt / erschlossen / offen** aus TB-15 war der Grund, warum
  die Korrektur in TB-16 eine halbe Stunde und keine Fehlersuche gekostet hat.
  *(neu aus TB-16)*
- **Abgebrochene Pulls kommen meist vom eigenen Rechner, nicht von der
  Cloud-Sitzung.** Beide Faelle am 12.09.2026 waren lokale Aenderungen —
  einmal ein Berechnungsergebnis des Dashboards, einmal eine von Hand kopierte
  Datei. `git status --short` **vor** dem Pull haette beide vorher gezeigt.
  *(neu)*
- **Eine Korrektur an der falschen Stelle korrigiert nichts.** Der Hinweis vom
  08.09. stand sechs Tage unterhalb der falschen Aussage, und die Aussage
  selbst blieb im Wortlaut stehen. Wer von oben liest, glaubt sie vorher.
  Korrekturen gehoeren **an die Stelle des Fehlers** oder in den Kopf der Datei.
  *(neu aus TB-17)*
- **Ein Pruefer, der bei sechs von neun Faellen grundlos anschlaegt, wird
  abgeschaltet und schuetzt danach nichts.** Lieber eng und wirksam als breit
  und ignoriert. *(neu aus TB-17)*
- **Eine zweite Kennzahl neben der ersten ist eine Einladung, nach ihr zu
  sortieren.** TB-18 hat deshalb bewusst *keinen* zweiten Score ergaenzt,
  sondern nur den Rohwert — die Entscheidung, welches Mass fuehrt, gehoert an
  eine Stelle und nicht in eine Spaltenueberschrift. *(neu aus TB-18)*
- **Eine instabile Sortierung ist kein Schoenheitsfehler, wenn eine Auswahl
  daran haengt.** In `elliott_wave_counter.py` entscheidet sie, **welches
  Wellenmuster gehandelt wird** — bei acht von elf Zeilen mit demselben
  Punktwert. Dieselbe Klasse wie die Symboldatei-Sortierung, nur eine Ebene
  tiefer und mitten im Live-Betrieb. *(neu aus TB-19)*
- **Ein Score, der tausende Faelle auf fuenf Werte abbildet, ordnet nicht.**
  `fibonacci_score()` kann oberhalb seiner Schwelle nur 0,33 / 0,34 / 0,66 /
  0,67 / 1,0 annehmen — 6 439 Aktien-Muster landen darauf. Was danach
  entscheidet, ist nicht der Score. *(neu aus TB-20)*
- **Auf X auswaehlen und auf Y berichten schuetzt die Zahlen — bis man es
  repariert.** Sind Auswahl- und Berichtsmass unkorreliert, ist das berichtete
  Ergebnis nahezu unverzerrt. Die **erste** Selektion auf einem gueltigen Mass
  ist die erste echte Optimierung — ab dann beginnt die Selektionsverzerrung,
  nicht vorher. *(neu aus der Fable-Antwort)*
- **Nicht das Maximum nehmen, sondern die Mitte des Plateaus.** Gewinnt
  Parameter p, sind aber p−1 und p+1 deutlich schlechter, ist p ein
  Zufallstreffer. Zwei Zeilen Code, die mehr Overfitting verhindern als jede
  DSR. *(neu aus der Fable-Antwort)*
- **Selektionsmass und Beurteilungsmass duerfen verschieden sein — das OBJEKT
  nicht.** Beide gehoeren auf denselben chronologischen Kapitalpfad, nie auf
  eine Trade-Liste. *(neu aus der Fable-Antwort)*
- **Die richtige erste Frage an ein fremdes System lautet: „Zeigt mir das
  Skript, das die Parameter auswaehlt."** Erst zeigen lassen, wie eine Zahl
  entsteht — dann eine Theorie darueber bauen, was sie bedeutet.
  *(Fables eigene Ruecknahme, und die mit dem groessten Gewicht)*
- **Ehrliche Beliebigkeit schlaegt versteckte.** Ein protokollierter Zufall als
  letzter Tie-Break ist sichtbar willkuerlich und reproduzierbar; die
  Dateireihenfolge ist unsichtbar willkuerlich. *(neu aus der zweiten
  Fable-Runde)*
- **Oekonomisch begruendet reicht nicht — ein Auswahlkriterium braucht auch
  Aufloesung.** Der `fib_score` ist begruendet und versagt trotzdem, weil er
  6 439 Faelle auf drei Stufen abbildet. Umgekehrt hat der Symbolname perfekte
  Aufloesung und ist oekonomisch leer. *(neu aus der zweiten Fable-Runde)*
- **Wer „signifikant" zur Bedingung macht, behaelt alle oder keinen.** Bei 130
  Trades hat ein wahres Alpha von 2 % p. a. eine t-Statistik um 0,6. Entscheiden
  heisst hier: nach Punktschaetzung und Robustheit, nicht nach Signifikanz.
  *(neu aus der zweiten Fable-Runde)*
- **Die Suche gehoert nicht ins Modell.** Wer das Modell selbst suchen laesst,
  bezahlt die Treffer als Eingabe-Token und verliert die Kontrolle ueber den
  Zeitstempel. Retrieval selbst machen, Klassifikation ohne Suchwerkzeug — Cent
  statt Dollar, und die Look-Ahead-Frage ist geloest. *(neu aus der zweiten
  Fable-Runde)*
- **Ein Mass kann an zwei Stellen wirken: im Code und im Prompt.** Bei Agent 2
  waehlte der Code auf dem einen Mass, waehrend das Modell die Suchrichtung
  anhand einer Tabelle steuerte, die nicht sagte, welches gilt. Wer nur eine der
  beiden Stellen umstellt, laesst Mechanik und Prompt gegeneinander laufen.
  *(neu aus TB-22)*
- **Was ein Modell formulieren darf, kann es auch abschwaechen.** Pflichtangaben
  — Unvalidiert-Hinweise, Zielgroessen — gehoeren als Konstanten-String in den
  Code, nicht in die Zustaendigkeit des Modells. *(neu aus TB-22)*
- **Eine Haltedauer ist meist ein Parameter, keine Markteigenschaft.** Bei
  sieben von neun Bots liegt der Median der Zeitausstiege **exakt** auf der
  eingestellten Zeitbremse. Wer Horizonte vergleicht, vergleicht oft
  Konfigurationen. *(neu aus TB-24)*
- **Gleichzeitig ist nicht dasselbe wie abhaengig.** Zwei Bots koennen in 0 von
  395 Faellen binnen drei Tagen gemeinsam einsteigen und trotzdem denselben
  Kursrueckgang handeln — mit 14 Tagen Versatz. **Unabhaengigkeit im engen
  Fenster ist kein Beleg fuer Unabhaengigkeit.** *(neu aus TB-24)*
- **Diversifikation haengt an der Ertragsquelle, nicht am Zeithorizont** —
  jedenfalls bei diesem Portfolio: gleiche Quelle 1,94 × Zufall, gleiche
  Horizont-Klasse 0,32 ×. *(neu aus TB-24)*
- **Gleiche Kennzahlen sind kein Beleg fuer gleiche Ergebnisse.** Bei
  `volatility_breakout_crypto` sind Drawdown und Trade-Zahl in allen zwanzig
  Permutationen identisch — und die Rendite schwankt um 27 Prozentpunkte. Wer
  Kennzahlen vergleicht statt der **Menge der ausgefuehrten Trades**, sieht
  nichts. *(neu aus TB-23)*
- **Eine Zahl ohne Zuteilungsregel ist ein Los, kein Ergebnis.** Acht von neun
  Bots liefern je nach Sortierung einer Textdatei verschiedene Renditen; die
  gespeicherte ist eine von zwanzig. *(neu aus TB-23)*
- **Ein Score, der mehrere Bedingungen zusammenzaehlt, kann eine schaedliche
  Bedingung hinter einer nuetzlichen verstecken.** Bei Elliott Wave traegt die
  Welle-4-Bedingung etwas, die Welle-3-Bedingung ist bei beiden Bots leicht
  negativ — die Summe sieht neutral aus. **Bedingungen einzeln messen, nicht nur
  ihre Zahl.** *(neu aus TB-25)*
- **Eindeutigkeit ist nicht Trennschaerfe.** Eine stetige Groesse beseitigt zwar
  jeden Gleichstand, ersetzt aber einen willkuerlichen Tie-Break nur durch einen
  sauberer aussehenden, wenn sie nichts misst. *(neu aus TB-25)*
- **Eine Regel mit Zufall auf der letzten Stufe ist nicht willkuerlich, wenn der
  Zufall fast nie drankommt.** Bei 3 704 strittigen Zuteilungen entschied er
  sechsmal — 0,16 %, sichtbar und protokolliert. Die Frage ist nicht, ob eine
  Regel einen willkuerlichen Rest hat, sondern **wie gross er ist und ob man ihn
  sieht**. *(neu aus TB-26)*
- **Ein Auftrag, der eine Zusammenlegung zur Entscheidung stellt, kann eine
  schlechtere Frage sein als das Nein darauf.** TB-26 hat begruendet abgelehnt,
  die neun `equity_simulation.py` zu vereinen — weil mehrere Werkzeuge per
  `inspect.signature` an ihrer heutigen Form haengen. *(neu aus TB-26)*
- **Eine Korrektur kann an der halben Stelle ankommen.** PR #90 hat das
  chronologische Mass in die neun Optimierer gebracht — aber sechs Bots haben
  einen **eigenen** Walk-Forward-Rechner, den niemand angefasst hat. **Wer eine
  Kennzahl aendert, muss alle Stellen suchen, an denen sie entsteht** — nicht
  nur die naheliegende. *(neu aus TB-27)*
- **Zeilennummern sind eine Abhaengigkeitsklasse.** Eine Dokumentationspruefung
  verwies auf Zeilen in `equity_simulation.py` und wurde durch TB-26 rot, ohne
  dass jemand etwas kaputt gemacht haette. *(neu aus TB-27)*
- **Ein Holdout, der automatisiert abgefragt wird, ist nach wenigen Abfragen
  keiner mehr.** Und die Abhilfe ist **nicht**, die Schwelle anzuheben — dafuer
  muesste man die Zahl der effektiv unabhaengigen Versuche kennen. Sondern: den
  Zeitraum **budgetieren** und die Nutzung zaehlen. *(neu aus der
  Strategy-Discovery-Pruefung)*
- **Wer auf rohen Sharpe selektiert, waehlt in einer Aufwaertsphase Beta aus.**
  Eine long-only Maschine in einem Buch mit +0,82 Korrelation zum Markt wuerde
  bevorzugt genau das durchwinken, was die Beta-Bereinigung aussortieren soll.
  *(neu aus der Strategy-Discovery-Pruefung)*
- **Eine Trefferquote taugt nicht als Schwelle.** Um 55 % von 50 % zu
  unterscheiden, braucht es rund 600 Trades — und Trendfolge gewinnt ohnehin mit
  35 %. *(neu aus der Strategy-Discovery-Pruefung)*
- **Ein ungepushter Commit laesst `main` und den eigenen Rechner
  auseinanderlaufen — und eine Cloud-Sitzung leitet daraus falsche Praemissen
  ab.** TB-28 schloss aus `main`, die Ergebniskurven seien veraltet; auf dem Mac
  waren sie es nicht. **Ungepushte Commits, die Ergebnisdateien betreffen,
  gehoeren in die Aufgabenbeschreibung.** *(neu aus TB-28)*
- **Eine Zahl in der Dokumentation steht selten nur an einer Stelle.** Die drei
  verrutschten Zeilennummern standen im Pruefwerkzeug **und** im Dokublock der
  `live_params.py`. Nur eine Seite zu reparieren ergaebe einen gruenen Waechter
  ueber falscher Dokumentation. *(neu aus TB-28)*
- **Multiplizitaet waechst mit dem Logarithmus — Unsicherheit ueber die
  Versuchszahl ist deshalb ertraeglich.** Von 36 auf 2 798 Versuche steigt die
  noetige Sharpe-Huerde nur von 1,2 auf 1,8. Eine **belegte Untergrenze** ist
  brauchbar, auch wenn sie unvollstaendig ist. *(neu aus TB-29)*
- **Eine begruendete Selektion ohne auffindbare Begruendung ist trotzdem eine
  Selektion.** Eine Rastergrenze wird im Code mit „Erkenntnis aus
  `compare_exit_rules.py`" begruendet — diese Datei hat nie im Repo gelegen.
  *„Die Selektion ist belegt, ihr Umfang nicht."* *(neu aus TB-29)*
- **Datenausbeutung entsteht dort, wo nach dem Ergebnis noch eine Wahl besteht.**
  Deshalb: das Auswertungsskript **vor** dem Lauf einfrieren. Vollstaendigkeitstest
  — *laesst es sich fertig schreiben, ohne ein Ergebnis gesehen zu haben?*
  *(neu aus der Vorabfestlegung)*
- **Ein Bug-Fix mitten im Lauf ist ein Amendment: der Lauf beginnt von vorn, und
  Vorher und Nachher werden nicht verglichen.** Wer sie vergleicht, hat wieder
  eine Wahl. *(neu aus der Vorabfestlegung)*
- **„Kein Bot erreicht die Schwelle" ist eine Aussage ueber den Backtest, nicht
  ueber die Bots.** Und sie ist das **wahrscheinliche** Ergebnis — deshalb muss
  vorher aufgeschrieben werden, dass sie zulaessig ist. *(neu aus der
  Vorabfestlegung)*

- **Eine Zahl aus einem Bericht ist kein Beleg.** Sechs von sieben Fehlern der
  Planungsseite am 15./16.09. hatten dieselbe Ursache: eine Zahl oder eine
  Fundstelle aus einem Dokument übernommen, statt sie an der Quelle zu prüfen.
  Gefunden wurden sie sämtlich von Sitzungen, deren Auftrag verlangte, **Belege
  aus dem Repo zu lesen statt aus dem Aufgabendokument abzuschreiben.**
  *(neu aus TB-38 bis TB-41)*
- **Ein Werkzeug, das nicht mehr misst, sagt es.** Drei Prüfungen hörten auf zu
  prüfen und meldeten weiter Erfolg: ein Schreibschutz, der an einem Leseversuch
  scheiterte; eine Wache gegen gelöschte Zeilen, die nach dem Merge trivial grün
  ist; eine Vergleichstabelle, die auf den ersetzten Stand zeigt. **Dieselbe
  Familie wie drei Bots, die Symbole lautlos auslassen.** *(neu aus TB-40/TB-41)*
- **Ein Vergleich gegen `origin/main` ist nach dem Merge leer — und damit
  trivial grün.** Dreimal in drei Tagen aufgetreten. Gefunden nur durch eine
  Prüfung, die fragt, **ob** geprüft wurde. *(neu aus TB-36, TB-40, TB-41)*
- **Der Teil, der täglich läuft, fragt die Daten nie; der Teil, der fragt, läuft
  nur gelegentlich.** So blieb ein zwei Wochen alter Kursdatenbestand mit
  Teilkerzen unbemerkt — 101 Module lasen ihn, keines prüfte den Stand.
  *(neu aus TB-34)*
- **Bereinigte Aktienkurse sind veränderliche Geschichte.** Ein Hash über
  yfinance-Dateien kann konstruktionsbedingt nicht stabil sein — bei jeder
  Dividende wird die gesamte Reihe zu Recht neu skaliert, und die Rundung
  schwankt zwischen zwei Abrufen im Abstand von Minuten. *(neu aus TB-35)*
- **In-Sample kann ausschliessen. Nur Out-of-Sample kann bestätigen.** Die
  Vielfachheit hat eine Richtung: Sie lässt Zufall wie Können aussehen, nie
  Können wie Zufall. Wer als bester von N die vorab festgelegten Kriterien
  reisst, ist ein Befund; wer sie besteht, ist **nicht widerlegt** — nicht
  **tragfähig**. *(neu aus der Beratung, 15.09.)*
- **Diversifikation hat zwei Achsen: Quelle × Anlage. Der Horizont ist keine.**
  Zwei Trendfolger auf Aktien steigen gemeinsam ein; ein Trendfolger auf Aktien
  und einer auf Anleihen nicht. **Budget gehört deshalb an die Zelle, nicht an
  den Bot.** *(neu aus der Beratung, 16.09.)*
- **Wer die Wirkung einer Auslegung kennt, darf sie nicht mehr frei wählen.**
  Bei der Lesart H gegen F war bekannt, dass F einen bestimmten Bot
  ausgeschlossen hätte. Registriert war H — also blieb es bei H. *Eine Wahl nach
  dem Ergebnis wurde bewusst vermieden; dass H ausserdem sachlich richtig ist,
  kam hinzu und war nicht der Grund.* *(neu aus TB-40)*
- **Ein Schreibschutz, der einen Aufrufweg nicht kennt, ist an diesem Weg kein
  Schreibschutz.** *(neu aus TB-41)*
- **Risiko ist über Zeiträume einigermassen stabil, Ertrag nicht.** Deshalb wurde
  der Aktien/Krypto-Schlüssel an gemessener Schwankung entschieden und
  ausdrücklich **nicht** an gemessener Rendite — der Messzeitraum enthält einen
  der grössten Krypto-Aufschwünge der Geschichte. *(neu aus AW.2)*
